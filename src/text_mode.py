"""
text_mode.py – Terminal driver for testing core logic independently of the GUI.

Controls
--------
    w / a / s / d  – move up / left / down / right
    p              – compute and show A* path from player to goal
    r              – reset to start
    q              – quit
"""

import os
import sys
from typing import List, Optional, Tuple

# Allow running directly from /src or from project root
sys.path.insert(0, os.path.dirname(__file__))

from grid        import load_grid, find_start_goal
from game        import GameState
from pathfinding import find_path


# ---------------------------------------------------------------------------
# Built-in fallback level (used when no filename is provided)
# ---------------------------------------------------------------------------
DEFAULT_LEVEL = """\
###########
#S........#
#.#######.#
#.#.....#.#
#.#.###.#.#
#...#.#...#
#####.###.#
#.....#.#.#
#.#####.#.#
#.......#G#
###########"""


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render_grid(
    grid:       List[List[str]],
    player_pos: Tuple[int, int],
    path:       Optional[List[Tuple[int, int]]] = None,
) -> str:
    """
    Return a string representation of the grid.

    Overlays:
      P  – player position
      o  – path cell (excluding S and G positions)
    """
    path_set = set(path) if path else set()
    lines = []

    for r, row in enumerate(grid):
        line = []
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == player_pos:
                line.append('P')
            elif pos in path_set and cell not in ('S', 'G'):
                line.append('o')
            else:
                line.append(cell)
        lines.append(' '.join(line))   # space between cells for readability

    return '\n'.join(lines)


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main(level_source: Optional[str] = None) -> None:
    """
    Run the text-mode game.

    Parameters
    ----------
    level_source : path to a .txt level file, or None to use the default level.
    """
    # ---- Load grid -------------------------------------------------------
    source = level_source if level_source else DEFAULT_LEVEL
    grid   = load_grid(source)
    start, goal = find_start_goal(grid)

    state = GameState(grid, start, goal)

    print("=== Maze Navigator – Text Mode ===")
    print("Controls: w/a/s/d = move | p = show path | r = reset | q = quit\n")

    while True:
        clear_screen()
        print("=== Maze Navigator – Text Mode ===")
        print("Controls: w/a/s/d = move | p = show path | r = reset | q = quit\n")
        print(render_grid(state.grid, state.player_pos, state.path))
        print(f"\nMoves: {state.move_count}  |  Position: {state.player_pos}")

        if state.won:
            print(f"\n🎉  You reached the goal in {state.move_count} moves!  🎉")
            again = input("Play again? (y/n): ").strip().lower()
            if again == 'y':
                state.reset()
                continue
            else:
                break

        cmd = input("\nCommand: ").strip().lower()

        if cmd == 'q':
            print("Goodbye!")
            break

        elif cmd == 'r':
            state.reset()
            print("Game reset.")

        elif cmd == 'p':
            # Compute A* path from current player position to goal
            path = find_path(state.grid, state.player_pos, state.goal_pos)
            if path:
                state.path = path
                print(f"Path found: {len(path) - 1} steps remaining.")
            else:
                state.path = []
                print("No path found – you may be trapped!")

        elif cmd in ('w', 'a', 's', 'd'):
            moved = state.apply_move(cmd)
            if not moved:
                print("Can't move that way.")

        else:
            print(f"Unknown command: '{cmd}'")


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Optionally pass a level file as a command-line argument:
    #   python text_mode.py ../examples/medium.txt
    level = sys.argv[1] if len(sys.argv) > 1 else None
    main(level)
