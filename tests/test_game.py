"""
test_game.py – Unit tests for player movement and game state (game.py).
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grid import load_grid, find_start_goal
from game import move_player, check_win, GameState


SIMPLE = """\
#####
#S..#
#..G#
#####"""


class TestMovePlayer(unittest.TestCase):

    def setUp(self):
        self.grid = load_grid(SIMPLE)

    def test_valid_move_right(self):
        new_pos, moved = move_player(self.grid, (1, 1), 'd')
        self.assertTrue(moved)
        self.assertEqual(new_pos, (1, 2))

    def test_valid_move_down(self):
        new_pos, moved = move_player(self.grid, (1, 1), 's')
        self.assertTrue(moved)
        self.assertEqual(new_pos, (2, 1))

    def test_blocked_by_wall(self):
        new_pos, moved = move_player(self.grid, (1, 1), 'w')  # wall above
        self.assertFalse(moved)
        self.assertEqual(new_pos, (1, 1))

    def test_blocked_by_wall_left(self):
        new_pos, moved = move_player(self.grid, (1, 1), 'a')  # wall to left
        self.assertFalse(moved)
        self.assertEqual(new_pos, (1, 1))

    def test_unknown_direction_unchanged(self):
        new_pos, moved = move_player(self.grid, (1, 1), 'x')
        self.assertFalse(moved)
        self.assertEqual(new_pos, (1, 1))

    def test_arrow_key_names(self):
        new_pos, moved = move_player(self.grid, (1, 1), 'Right')
        self.assertTrue(moved)
        self.assertEqual(new_pos, (1, 2))

    def test_cannot_move_out_of_bounds(self):
        # Place player at edge floor cell and try to move out
        new_pos, moved = move_player(self.grid, (1, 3), 'd')  # wall at (1,4)
        self.assertFalse(moved)


class TestCheckWin(unittest.TestCase):

    def test_win_detected(self):
        self.assertTrue(check_win((2, 3), (2, 3)))

    def test_no_win(self):
        self.assertFalse(check_win((1, 1), (2, 3)))


class TestGameState(unittest.TestCase):

    def setUp(self):
        self.grid = load_grid(SIMPLE)
        start, goal = find_start_goal(self.grid)
        self.state = GameState(self.grid, start, goal)

    def test_initial_position(self):
        self.assertEqual(self.state.player_pos, (1, 1))

    def test_move_increments_counter(self):
        self.state.apply_move('d')
        self.assertEqual(self.state.move_count, 1)

    def test_failed_move_does_not_increment(self):
        self.state.apply_move('w')   # wall
        self.assertEqual(self.state.move_count, 0)

    def test_path_cleared_on_move(self):
        self.state.path = [(1, 1), (1, 2)]
        self.state.apply_move('d')
        self.assertEqual(self.state.path, [])

    def test_win_detected_on_arrival(self):
        # Navigate from (1,1) → (1,2) → (1,3) → (2,3)
        self.state.apply_move('d')   # (1,2)
        self.state.apply_move('d')   # (1,3)
        self.state.apply_move('s')   # (2,3) = G
        self.assertTrue(self.state.won)

    def test_no_moves_after_win(self):
        self.state.apply_move('d')
        self.state.apply_move('d')
        self.state.apply_move('s')   # wins here
        count_before = self.state.move_count
        self.state.apply_move('d')   # should be ignored
        self.assertEqual(self.state.move_count, count_before)

    def test_reset(self):
        self.state.apply_move('d')
        self.state.apply_move('d')
        self.state.apply_move('s')
        self.state.reset()
        self.assertEqual(self.state.player_pos, (1, 1))
        self.assertFalse(self.state.won)
        self.assertEqual(self.state.move_count, 0)
        self.assertEqual(self.state.path, [])


if __name__ == '__main__':
    unittest.main()
