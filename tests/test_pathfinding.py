"""
test_pathfinding.py – Unit tests for the A* pathfinding implementation.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grid        import load_grid
from pathfinding import find_path, heuristic


# ---------------------------------------------------------------------------
# Helper mazes
# ---------------------------------------------------------------------------
OPEN_GRID = """\
#####
#S..#
#..G#
#####"""

CORRIDOR = """\
#######
#S....#
######G"""   # No path – G is unreachable through walls

STRAIGHT = """\
#######
#S...G#
#######"""

MAZE = """\
#########
#S#.....#
#.#.###.#
#...#..G#
#########"""


class TestHeuristic(unittest.TestCase):

    def test_same_cell(self):
        self.assertEqual(heuristic((0, 0), (0, 0)), 0)

    def test_adjacent(self):
        self.assertEqual(heuristic((0, 0), (0, 1)), 1)
        self.assertEqual(heuristic((0, 0), (1, 0)), 1)

    def test_manhattan_distance(self):
        self.assertEqual(heuristic((0, 0), (3, 4)), 7)


class TestFindPath(unittest.TestCase):

    def test_start_equals_goal(self):
        grid = load_grid(OPEN_GRID)
        path = find_path(grid, (1, 1), (1, 1))
        self.assertEqual(path, [(1, 1)])

    def test_straight_corridor_length(self):
        grid = load_grid(STRAIGHT)
        path = find_path(grid, (1, 1), (1, 5))
        self.assertEqual(len(path), 5)          # S + 3 floor + G
        self.assertEqual(path[0], (1, 1))
        self.assertEqual(path[-1], (1, 5))

    def test_no_path_returns_empty(self):
        grid = load_grid(CORRIDOR)
        path = find_path(grid, (1, 1), (2, 6))
        self.assertEqual(path, [])

    def test_path_avoids_walls(self):
        grid = load_grid(OPEN_GRID)
        path = find_path(grid, (1, 1), (2, 3))
        for r, c in path:
            self.assertNotEqual(grid[r][c], '#',
                msg=f"Path passes through wall at ({r},{c})")

    def test_path_is_connected(self):
        """Each consecutive pair of cells must be exactly one step apart."""
        grid = load_grid(MAZE)
        path = find_path(grid, (1, 1), (3, 7))
        self.assertTrue(len(path) > 0, "Expected a valid path in MAZE")
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            distance = abs(r1 - r2) + abs(c1 - c2)
            self.assertEqual(distance, 1,
                msg=f"Non-adjacent steps in path: ({r1},{c1}) -> ({r2},{c2})")

    def test_path_is_shortest(self):
        """A* must return the shortest path (BFS-equivalent length)."""
        grid = load_grid(OPEN_GRID)
        path = find_path(grid, (1, 1), (2, 3))
        # Manhattan distance = |2-1| + |3-1| = 3, so path length = 4
        self.assertEqual(len(path), 4)

    def test_path_starts_and_ends_correctly(self):
        grid = load_grid(MAZE)
        start = (1, 1)
        goal  = (3, 7)
        path  = find_path(grid, start, goal)
        if path:
            self.assertEqual(path[0],  start)
            self.assertEqual(path[-1], goal)


if __name__ == '__main__':
    unittest.main()
