from __future__ import annotations

import argparse

from .bots import GreedyAggressive, GreedyConservative, MaxNRolls, RandomDeterministic
from .runner import simulate_games


def default_bots():
    return [
        MaxNRolls(3, GreedyConservative()),
        MaxNRolls(3, GreedyAggressive()),
        MaxNRolls(2, GreedyConservative()),
        RandomDeterministic(seed=99),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Can't Stop simulation runner")
    parser.add_argument("-n", "--games", type=int, default=200, help="Number of games")
    parser.add_argument("--seed", type=int, default=12345, help="Base seed")
    args = parser.parse_args()

    result = simulate_games(default_bots, n_games=args.games, base_seed=args.seed)
    print(f"Games: {args.games}")
    print(f"Win counts: {result.win_counts}")
    print(f"Bust rate: {result.bust_rate:.3f}")
    print(f"Avg rolls/turn: {result.avg_rolls_per_turn:.3f}")
    print(f"Avg banked steps/turn: {result.avg_banked_steps_per_turn:.3f}")
    print(f"Avg turns/game: {result.avg_turns_per_game:.3f}")


if __name__ == "__main__":
    main()
