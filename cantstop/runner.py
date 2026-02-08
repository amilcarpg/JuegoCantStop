from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence

from .bots import BotPolicy
from .engine import CantStopGame


@dataclass
class SimulationResult:
    win_counts: Dict[int, int]
    bust_rate: float
    avg_rolls_per_turn: float
    avg_banked_steps_per_turn: float
    avg_turns_per_game: float


def simulate_games(bot_factory: Callable[[], Sequence[BotPolicy]], n_games: int, base_seed: int = 12345) -> SimulationResult:
    sample_bots = bot_factory()
    players = len(sample_bots)

    wins = {i: 0 for i in range(players)}
    total_busts = 0
    total_turns = 0
    total_rolls = 0
    total_banked_steps = 0

    for i in range(n_games):
        bots = bot_factory()
        game = CantStopGame(bots, seed=base_seed + i)
        w = game.play()
        wins[w] += 1

        total_busts += sum(game.bust_count)
        total_turns += sum(game.turn_count)
        total_rolls += game.roll_count
        total_banked_steps += game.banked_steps

    safe_turns = max(total_turns, 1)
    return SimulationResult(
        win_counts=wins,
        bust_rate=total_busts / safe_turns,
        avg_rolls_per_turn=total_rolls / safe_turns,
        avg_banked_steps_per_turn=total_banked_steps / safe_turns,
        avg_turns_per_game=total_turns / n_games,
    )
