"""
game.py – Player movement, game state management, and win detection.

All functions are pure (no I/O) so they can be called identically
from text_mode.py and gui.py without duplication.
"""

from typing import Optional, Tuple
from grid import is_walkable

# Direction vectors keyed by common command strings
DIRECTIONS = {
    'w': (-1,  0),   # up
    's': ( 1,  0),   # down
    'a': ( 0, -1),   # left
    'd': ( 0,  1),   # right
    # Arrow-key names used by tkinter
    'Up':    (-1,  0),
    'Down':  ( 1,  0),
    'Left':  ( 0, -1),
    'Right': ( 0,  1),
}


def move_player(
    grid,
    current_pos: Tuple[int, int],
    direction: str
) -> Tuple[Tuple[int, int], bool]:
    """
    Attempt to move the player one step in the given direction.

    Parameters
    ----------
    grid        : 2-D list of characters (from grid.py)
    current_pos : (row, col) of the player before the move
    direction   : one of 'w', 'a', 's', 'd' or 'Up', 'Down', 'Left', 'Right'

    Returns
    -------
    (new_pos, moved)
        new_pos – updated (row, col); unchanged if the move was invalid
        moved   – True if the move succeeded, False otherwise
    """
    if direction not in DIRECTIONS:
        return current_pos, False

    dr, dc = DIRECTIONS[direction]
    new_row = current_pos[0] + dr
    new_col = current_pos[1] + dc

    if is_walkable(grid, new_row, new_col):
        return (new_row, new_col), True

    return current_pos, False


def check_win(
    player_pos: Tuple[int, int],
    goal_pos:   Tuple[int, int]
) -> bool:
    """Return True when the player has reached the goal cell."""
    return player_pos == goal_pos


class GameState:
    """
    Convenience wrapper that holds all mutable game state.

    Both the text driver and the GUI instantiate one of these so they
    share identical logic without maintaining separate variables.
    """

    def __init__(self, grid, start_pos, goal_pos):
        self.grid        = grid
        self.start_pos   = start_pos
        self.goal_pos    = goal_pos
        self.player_pos  = start_pos
        self.won         = False
        self.move_count  = 0
        self.path        = []          # last computed path (list of (r,c))

    # ------------------------------------------------------------------
    def apply_move(self, direction: str) -> bool:
        """
        Try to move the player.  Updates state and returns True on success.
        Does nothing (returns False) once the game is already won.
        """
        if self.won:
            return False

        new_pos, moved = move_player(self.grid, self.player_pos, direction)
        if moved:
            self.player_pos = new_pos
            self.move_count += 1
            self.path = []            # clear path hint after every move
            if check_win(self.player_pos, self.goal_pos):
                self.won = True
        return moved

    def reset(self) -> None:
        """Restart the game from the beginning."""
        self.player_pos = self.start_pos
        self.won        = False
        self.move_count = 0
        self.path       = []
