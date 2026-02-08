import unittest

from cantstop.bots import AlwaysContinue
from cantstop.engine import CantStopGame, Move, HEIGHTS


class TestRules(unittest.TestCase):
    def make_game(self):
        return CantStopGame([AlwaysContinue() for _ in range(4)], seed=1)

    def test_pairings(self):
        p = CantStopGame.pairings((1, 2, 3, 4))
        self.assertEqual(p, [(3, 7), (4, 6), (5, 5)])

    def test_legal_moves_open_and_limit_three_active(self):
        g = self.make_game()
        legal_open = g.legal_moves((1, 1, 1, 2))
        self.assertTrue(any(2 in m.as_dict() or 3 in m.as_dict() for m in legal_open))

        g.state.turn.active_cols = {4, 5, 6}
        g.state.turn.temp = {4: 1, 5: 1, 6: 1}
        legal_blocked = g.legal_moves((1, 1, 1, 2))
        self.assertEqual(legal_blocked, [])

    def test_legal_moves_disallow_completed(self):
        g = self.make_game()
        p = g.state.players[g.state.current_player]
        p.permanent[7] = HEIGHTS[7]
        p.completed.add(7)
        legal = g.legal_moves((3, 4, 1, 1))
        self.assertTrue(all(7 not in m.as_dict() for m in legal))

    def test_double_sum_represents_two_steps(self):
        g = self.make_game()
        legal = g.legal_moves((1, 2, 1, 2))
        self.assertIn(Move(((3, 2),)), legal)

    def test_bust_resets_turn(self):
        g = self.make_game()
        g.state.turn.temp = {2: 1}
        g.state.turn.active_cols = {2}
        g.bust()
        self.assertEqual(g.state.turn.temp, {})
        self.assertEqual(g.state.turn.active_cols, set())

    def test_bank_updates_and_completion(self):
        g = self.make_game()
        p = g.state.players[g.state.current_player]
        p.permanent[2] = HEIGHTS[2] - 1
        g.state.turn.temp = {2: 1, 3: 2}
        g.state.turn.active_cols = {2, 3}
        g.bank()
        self.assertEqual(p.permanent[2], HEIGHTS[2])
        self.assertIn(2, p.completed)
        self.assertEqual(g.state.turn.temp, {})

    def test_win_condition_after_bank(self):
        g = self.make_game()
        p = g.state.players[g.state.current_player]
        p.completed.update({2, 3})
        p.permanent[2] = HEIGHTS[2]
        p.permanent[3] = HEIGHTS[3]
        p.permanent[4] = HEIGHTS[4] - 1
        g.state.turn.temp = {4: 1}
        g.bank()
        self.assertEqual(g.state.winner, 0)


if __name__ == '__main__':
    unittest.main()
