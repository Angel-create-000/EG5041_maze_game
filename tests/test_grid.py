"""
test_grid.py – Unit tests for grid.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grid import load_grid, find_start_goal, is_walkable, validate_grid


SIMPLE = """\
#####
#S..#
#..G#
#####"""


class TestLoadGrid(unittest.TestCase):

    def test_returns_list_of_lists(self):
        grid = load_grid(SIMPLE)
        self.assertIsInstance(grid, list)
        self.assertIsInstance(grid[0], list)

    def test_dimensions(self):
        grid = load_grid(SIMPLE)
        self.assertEqual(len(grid), 4)
        self.assertEqual(len(grid[0]), 5)

    def test_characters_preserved(self):
        grid = load_grid(SIMPLE)
        self.assertEqual(grid[0][0], '#')
        self.assertEqual(grid[1][1], 'S')
        self.assertEqual(grid[2][3], 'G')

    def test_empty_source_raises(self):
        with self.assertRaises((ValueError, SystemExit)):
            load_grid("")


class TestValidateGrid(unittest.TestCase):

    def test_valid_grid_passes(self):
        grid = load_grid(SIMPLE)
        # Should not raise or exit
        validate_grid(grid)

    def test_missing_start_exits(self):
        bad = """\
#####
#...#
#..G#
#####"""
        grid = load_grid(bad)
        with self.assertRaises(SystemExit):
            validate_grid(grid)

    def test_missing_goal_exits(self):
        bad = """\
#####
#S..#
#...#
#####"""
        grid = load_grid(bad)
        with self.assertRaises(SystemExit):
            validate_grid(grid)

    def test_duplicate_start_exits(self):
        bad = """\
#####
#SS.#
#..G#
#####"""
        grid = load_grid(bad)
        with self.assertRaises(SystemExit):
            validate_grid(grid)


class TestFindStartGoal(unittest.TestCase):

    def test_correct_positions(self):
        grid = load_grid(SIMPLE)
        start, goal = find_start_goal(grid)
        self.assertEqual(start, (1, 1))
        self.assertEqual(goal,  (2, 3))


class TestIsWalkable(unittest.TestCase):

    def setUp(self):
        self.grid = load_grid(SIMPLE)

    def test_wall_not_walkable(self):
        self.assertFalse(is_walkable(self.grid, 0, 0))

    def test_floor_walkable(self):
        self.assertTrue(is_walkable(self.grid, 1, 2))

    def test_start_walkable(self):
        self.assertTrue(is_walkable(self.grid, 1, 1))

    def test_goal_walkable(self):
        self.assertTrue(is_walkable(self.grid, 2, 3))

    def test_out_of_bounds_not_walkable(self):
        self.assertFalse(is_walkable(self.grid, -1, 0))
        self.assertFalse(is_walkable(self.grid, 100, 100))


if __name__ == '__main__':
    unittest.main()
