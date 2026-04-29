"""
grid.py – Grid loading, validation, and cell utilities.

Handles reading maze level files, finding special cells (S, G),
and providing helpers that other modules rely on.
"""

import sys
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WALL      = '#'
FLOOR     = '.'
START     = 'S'
GOAL      = 'G'
WALKABLE  = {FLOOR, START, GOAL}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def load_grid(source: str) -> List[List[str]]:
    """
    Load a maze from a text file path OR a multi-line string literal.

    Each row becomes a list of single-character strings.
    Raises ValueError if the grid is empty.
    """
    # Try to treat source as a filename first
    try:
        with open(source, 'r') as fh:
            lines = [line.rstrip('\n') for line in fh.readlines()]
    except (FileNotFoundError, OSError):
        # Fall back: treat the string itself as level data
        lines = [line.rstrip('\n') for line in source.splitlines()]

    lines = [l for l in lines if l]          # drop blank lines
    if not lines:
        raise ValueError("Grid is empty – check your level file.")

    grid = [list(row) for row in lines]
    return grid


def validate_grid(grid: List[List[str]]) -> None:
    """
    Ensure the grid contains exactly one S and one G.
    Prints an error message and exits if either is missing or duplicated.
    """
    flat = [cell for row in grid for cell in row]
    s_count = flat.count(START)
    g_count = flat.count(GOAL)

    errors = []
    if s_count == 0:
        errors.append("No start cell 'S' found.")
    elif s_count > 1:
        errors.append(f"Multiple start cells 'S' found ({s_count}).")
    if g_count == 0:
        errors.append("No goal cell 'G' found.")
    elif g_count > 1:
        errors.append(f"Multiple goal cells 'G' found ({g_count}).")

    if errors:
        for msg in errors:
            print(f"[ERROR] {msg}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Cell queries
# ---------------------------------------------------------------------------
def find_start_goal(
    grid: List[List[str]]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Scan the grid and return ((start_row, start_col), (goal_row, goal_col)).
    Calls validate_grid first so callers get a clean error if cells are missing.
    """
    validate_grid(grid)
    start: Optional[Tuple[int, int]] = None
    goal:  Optional[Tuple[int, int]] = None

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == START:
                start = (r, c)
            elif cell == GOAL:
                goal = (r, c)

    # validate_grid already guarantees both exist, but keep the assertion
    assert start is not None and goal is not None
    return start, goal


def is_walkable(grid: List[List[str]], row: int, col: int) -> bool:
    """Return True if (row, col) is inside the grid and not a wall."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False
    return grid[row][col] in WALKABLE


def grid_dimensions(grid: List[List[str]]) -> Tuple[int, int]:
    """Return (num_rows, num_cols)."""
    return len(grid), len(grid[0]) if grid else 0
