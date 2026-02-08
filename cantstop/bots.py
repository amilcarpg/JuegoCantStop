from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Protocol, Sequence, Tuple

from .engine import HEIGHTS, Move, GameState


class BotPolicy(Protocol):
    def choose_move(self, state: GameState, dice: Tuple[int, int, int, int], legal_moves: Sequence[Move]) -> Move:
        ...

    def decide_stop(self, state: GameState, rolls_this_turn: int) -> bool:
        ...


def _move_sort_key(move: Move):
    return (
        len(move.advances),
        tuple(col for col, _ in move.advances),
        tuple(step for _, step in move.advances),
    )


def _would_win_with_bank(state: GameState) -> bool:
    p = state.players[state.current_player]
    wins = len(p.completed)
    for col, step in state.turn.temp.items():
        if col not in p.completed and p.permanent[col] + step >= HEIGHTS[col]:
            wins += 1
    return wins >= 3


@dataclass
class AlwaysContinue:
    def choose_move(self, state: GameState, dice: Tuple[int, int, int, int], legal_moves: Sequence[Move]) -> Move:
        return sorted(legal_moves, key=_move_sort_key)[0]

    def decide_stop(self, state: GameState, rolls_this_turn: int) -> bool:
        return False


@dataclass
class GreedyAggressive:
    completion_bonus: float = 2.0
    winning_bonus: float = 5.0

    def choose_move(self, state: GameState, dice: Tuple[int, int, int, int], legal_moves: Sequence[Move]) -> Move:
        p = state.players[state.current_player]
        best_move = None
        best_score = float("-inf")

        for move in legal_moves:
            score = 0.0
            completed_now = 0
            for col, step in move.advances:
                prog = p.permanent[col] + state.turn.temp.get(col, 0) + step
                score += prog / HEIGHTS[col]
                if col not in p.completed and prog >= HEIGHTS[col]:
                    score += self.completion_bonus
                    completed_now += 1
            if len(p.completed) + completed_now >= 3:
                score += self.winning_bonus

            key = (move.total_steps(), move.column_sum())
            if score > best_score or (score == best_score and key > (best_move.total_steps(), best_move.column_sum()) if best_move else True):
                best_score = score
                best_move = move

        assert best_move is not None
        return best_move

    def decide_stop(self, state: GameState, rolls_this_turn: int) -> bool:
        return _would_win_with_bank(state)


@dataclass
class GreedyConservative:
    open_penalty: float = 0.7
    active_bonus: float = 0.1
    completion_bonus: float = 1.0

    def choose_move(self, state: GameState, dice: Tuple[int, int, int, int], legal_moves: Sequence[Move]) -> Move:
        p = state.players[state.current_player]
        active = state.turn.active_cols

        best_move = None
        best_score = float("-inf")
        best_tie = None

        for move in legal_moves:
            score = 0.0
            opens = 0
            for col, step in move.advances:
                prog = p.permanent[col] + state.turn.temp.get(col, 0) + step
                score += prog / HEIGHTS[col]
                if col in active:
                    score += self.active_bonus
                else:
                    opens += 1
                    score -= self.open_penalty
                if col not in p.completed and prog >= HEIGHTS[col]:
                    score += self.completion_bonus

            tie = (opens == 0, len(move.advances) == 1, tuple(col for col, _ in move.advances))
            if score > best_score or (score == best_score and (best_tie is None or tie > best_tie)):
                best_score = score
                best_tie = tie
                best_move = move

        assert best_move is not None
        return best_move

    def decide_stop(self, state: GameState, rolls_this_turn: int) -> bool:
        return _would_win_with_bank(state)


@dataclass
class MaxNRolls:
    n: int
    move_policy: BotPolicy = field(default_factory=GreedyConservative)

    def choose_move(self, state: GameState, dice: Tuple[int, int, int, int], legal_moves: Sequence[Move]) -> Move:
        return self.move_policy.choose_move(state, dice, legal_moves)

    def decide_stop(self, state: GameState, rolls_this_turn: int) -> bool:
        if _would_win_with_bank(state):
            return True
        return rolls_this_turn >= self.n


@dataclass
class RandomDeterministic:
    seed: int = 0

    def __post_init__(self):
        self.rng = random.Random(self.seed)

    def choose_move(self, state: GameState, dice: Tuple[int, int, int, int], legal_moves: Sequence[Move]) -> Move:
        return self.rng.choice(list(legal_moves))

    def decide_stop(self, state: GameState, rolls_this_turn: int) -> bool:
        if _would_win_with_bank(state):
            return True
        return rolls_this_turn >= 2
