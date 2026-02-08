from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .bots import BotPolicy

HEIGHTS: Dict[int, int] = {2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 11, 9: 9, 10: 7, 11: 5, 12: 3}
COLUMNS: Tuple[int, ...] = tuple(range(2, 13))


@dataclass(frozen=True)
class Move:
    advances: Tuple[Tuple[int, int], ...]

    def as_dict(self) -> Dict[int, int]:
        return dict(self.advances)

    def total_steps(self) -> int:
        return sum(step for _, step in self.advances)

    def column_sum(self) -> int:
        return sum(col for col, _ in self.advances)


@dataclass
class PlayerState:
    permanent: Dict[int, int] = field(default_factory=lambda: {c: 0 for c in COLUMNS})
    completed: set[int] = field(default_factory=set)


@dataclass
class TurnState:
    temp: Dict[int, int] = field(default_factory=dict)
    active_cols: set[int] = field(default_factory=set)
    rolls_this_turn: int = 0


@dataclass
class GameState:
    players: List[PlayerState]
    current_player: int
    turn: TurnState
    winner: Optional[int] = None
    total_turns: int = 0


class CantStopGame:
    def __init__(self, bots: Sequence['BotPolicy'], seed: int = 0):
        self.bots = list(bots)
        self.rng = random.Random(seed)
        self.state = GameState(players=[PlayerState() for _ in bots], current_player=0, turn=TurnState())

        self.bust_count = [0 for _ in bots]
        self.turn_count = [0 for _ in bots]
        self.roll_count = 0
        self.banked_steps = 0

    @staticmethod
    def pairings(dice: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        d1, d2, d3, d4 = dice
        return [
            (d1 + d2, d3 + d4),
            (d1 + d3, d2 + d4),
            (d1 + d4, d2 + d3),
        ]

    def roll_dice(self) -> Tuple[int, int, int, int]:
        return tuple(self.rng.randint(1, 6) for _ in range(4))  # type: ignore[return-value]

    def _effective_steps(self, player: PlayerState, col: int, raw_steps: int) -> int:
        remaining = HEIGHTS[col] - (player.permanent[col] + self.state.turn.temp.get(col, 0))
        if remaining <= 0:
            return 0
        return min(raw_steps, remaining)

    def legal_moves(self, dice: Tuple[int, int, int, int]) -> List[Move]:
        player = self.state.players[self.state.current_player]
        active = self.state.turn.active_cols
        generated: dict[Tuple[Tuple[int, int], ...], Move] = {}

        for a, b in self.pairings(dice):
            raw_options = [{a: 2}] if a == b else [{a: 1}, {b: 1}, {a: 1, b: 1}]
            for option in raw_options:
                effective: Dict[int, int] = {}
                valid = True
                opens = 0
                for col, steps in option.items():
                    if col in player.completed:
                        valid = False
                        break
                    if col not in active:
                        opens += 1
                    eff = self._effective_steps(player, col, steps)
                    if eff <= 0:
                        valid = False
                        break
                    effective[col] = eff
                if not valid:
                    continue
                if len(active) + opens > 3:
                    continue
                mv = Move(tuple(sorted(effective.items())))
                generated[mv.advances] = mv

        return sorted(generated.values(), key=lambda m: (len(m.advances), m.advances))

    def apply_move(self, move: Move) -> None:
        player = self.state.players[self.state.current_player]
        for col, step in move.advances:
            eff = self._effective_steps(player, col, step)
            if eff <= 0:
                continue
            self.state.turn.temp[col] = self.state.turn.temp.get(col, 0) + eff
            self.state.turn.active_cols.add(col)

    def bust(self) -> None:
        p = self.state.current_player
        self.bust_count[p] += 1
        self.state.turn = TurnState()
        self._next_player()

    def bank(self) -> None:
        player = self.state.players[self.state.current_player]
        turn_steps = 0
        for col, step in self.state.turn.temp.items():
            player.permanent[col] = min(HEIGHTS[col], player.permanent[col] + step)
            turn_steps += step
            if player.permanent[col] >= HEIGHTS[col]:
                player.completed.add(col)
        self.banked_steps += turn_steps

        if len(player.completed) >= 3:
            self.state.winner = self.state.current_player
            self.state.turn = TurnState()
            return

        self.state.turn = TurnState()
        self._next_player()

    def _next_player(self) -> None:
        self.state.current_player = (self.state.current_player + 1) % len(self.bots)
        self.state.total_turns += 1

    def can_win_with_bank(self, player_idx: Optional[int] = None) -> bool:
        idx = self.state.current_player if player_idx is None else player_idx
        p = self.state.players[idx]
        wins = len(p.completed)
        for col, step in self.state.turn.temp.items():
            if col in p.completed:
                continue
            if p.permanent[col] + step >= HEIGHTS[col]:
                wins += 1
        return wins >= 3

    def play(self, max_total_turns: int = 5000) -> int:
        while self.state.winner is None and self.state.total_turns < max_total_turns:
            p = self.state.current_player
            self.turn_count[p] += 1
            bot = self.bots[p]

            while True:
                dice = self.roll_dice()
                self.state.turn.rolls_this_turn += 1
                self.roll_count += 1
                legal = self.legal_moves(dice)
                if not legal:
                    self.bust()
                    break

                chosen = bot.choose_move(self.state, dice, legal)
                self.apply_move(chosen)
                if bot.decide_stop(self.state, self.state.turn.rolls_this_turn):
                    self.bank()
                    break

            if self.state.winner is not None:
                return self.state.winner

        if self.state.winner is None:
            raise RuntimeError("Game exceeded max turns without winner")
        return self.state.winner
