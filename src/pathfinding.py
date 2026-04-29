"""
pathfinding.py – A* search algorithm for maze navigation.

A* is chosen over plain BFS because it uses a heuristic (Manhattan
distance) to guide the search toward the goal, expanding fewer nodes
on average while still guaranteeing the shortest path on a uniform-cost
grid.  On a grid where all walkable cells have equal movement cost,
A* with Manhattan distance is both optimal and complete.

Public interface
----------------
    find_path(grid, start, goal) -> list[(row, col)] | []
"""

import heapq
from typing import Dict, List, Optional, Tuple

from grid import is_walkable

# The four cardinal neighbours (up, down, left, right)
_NEIGHBOURS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# ---------------------------------------------------------------------------
# Heuristic
# ---------------------------------------------------------------------------
def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """
    Manhattan distance between two grid cells.

    Because diagonal moves are not allowed, this is both admissible and
    consistent – required for A* to return an optimal path.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------------------------------------
# A* core
# ---------------------------------------------------------------------------
def find_path(
    grid,
    start: Tuple[int, int],
    goal:  Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Find the shortest path from *start* to *goal* using A*.

    Parameters
    ----------
    grid  : 2-D list of characters (walls = '#', walkable = '.', 'S', 'G')
    start : (row, col) starting cell – must be walkable
    goal  : (row, col) target cell  – must be walkable

    Returns
    -------
    Ordered list of (row, col) positions from start to goal (both inclusive).
    Returns an empty list if no path exists.
    """
    if start == goal:
        return [start]

    # ------------------------------------------------------------------ #
    # Open set: min-heap of (f_score, g_score, node)                     #
    # g_score = exact cost from start                                     #
    # f_score = g_score + heuristic (estimated total cost)               #
    # ------------------------------------------------------------------ #
    open_heap: List[Tuple[int, int, Tuple[int, int]]] = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0, start))

    # came_from maps each visited node to its predecessor on the best path
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    # g_score[node] = lowest cost found so far to reach node
    g_score: Dict[Tuple[int, int], int] = {start: 0}

    while open_heap:
        _f, g, current = heapq.heappop(open_heap)

        # Goal reached – reconstruct and return the path
        if current == goal:
            return _reconstruct_path(came_from, goal)

        # Skip if we have already found a cheaper route to this node
        if g > g_score.get(current, float('inf')):
            continue

        # Expand all four cardinal neighbours
        for dr, dc in _NEIGHBOURS:
            neighbour = (current[0] + dr, current[1] + dc)

            if not is_walkable(grid, neighbour[0], neighbour[1]):
                continue                       # wall or out-of-bounds

            tentative_g = g + 1                # uniform cost grid → +1 per step

            if tentative_g < g_score.get(neighbour, float('inf')):
                # Found a better path to this neighbour
                g_score[neighbour] = tentative_g
                came_from[neighbour] = current
                f = tentative_g + heuristic(neighbour, goal)
                heapq.heappush(open_heap, (f, tentative_g, neighbour))

    # Open set exhausted without reaching goal → no path exists
    return []


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _reconstruct_path(
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
    current:   Tuple[int, int]
) -> List[Tuple[int, int]]:
    """Walk the came_from map backwards to build the path start → goal."""
    path = []
    node: Optional[Tuple[int, int]] = current
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path
