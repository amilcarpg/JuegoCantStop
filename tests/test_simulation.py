import os
import unittest

from cantstop.bots import GreedyAggressive, GreedyConservative, MaxNRolls, RandomDeterministic
from cantstop.engine import CantStopGame
from cantstop.runner import simulate_games


class TestSimulation(unittest.TestCase):
    def test_deterministic_full_game(self):
        bots = [
            MaxNRolls(2, GreedyConservative()),
            MaxNRolls(2, GreedyConservative()),
            MaxNRolls(2, GreedyConservative()),
            MaxNRolls(2, GreedyConservative()),
        ]
        g1 = CantStopGame(bots, seed=777)
        w1 = g1.play(max_total_turns=3000)

        bots2 = [
            MaxNRolls(2, GreedyConservative()),
            MaxNRolls(2, GreedyConservative()),
            MaxNRolls(2, GreedyConservative()),
            MaxNRolls(2, GreedyConservative()),
        ]
        g2 = CantStopGame(bots2, seed=777)
        w2 = g2.play(max_total_turns=3000)

        self.assertEqual(w1, w2)
        self.assertLess(g1.state.total_turns, 3000)

    def test_repetitive_metrics(self):
        x = int(os.getenv('CANTSTOP_X_REPS', '200'))

        def table_bots():
            return [
                MaxNRolls(3, GreedyConservative()),
                MaxNRolls(3, GreedyAggressive()),
                MaxNRolls(2, GreedyConservative()),
                RandomDeterministic(seed=42),
            ]

        result = simulate_games(table_bots, n_games=x, base_seed=12345)
        self.assertEqual(sum(result.win_counts.values()), x)

        ga_rate = result.win_counts[1] / x
        gc_rate = result.win_counts[0] / x
        self.assertGreaterEqual(ga_rate, 0.05)
        self.assertLessEqual(ga_rate, 0.85)
        self.assertGreaterEqual(gc_rate, 0.05)
        self.assertLessEqual(gc_rate, 0.85)

        self.assertGreaterEqual(result.bust_rate, 0.01)
        self.assertLessEqual(result.bust_rate, 0.80)
        self.assertGreaterEqual(result.avg_turns_per_game, 30)
        self.assertLessEqual(result.avg_turns_per_game, 400)


if __name__ == '__main__':
    unittest.main()
