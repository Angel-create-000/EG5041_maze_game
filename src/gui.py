"""
gui.py – Tkinter GUI for the Maze Navigator game.

Design principles
-----------------
* The GUI reuses grid.py, game.py, and pathfinding.py entirely.
* No pathfinding logic, movement rules, or grid state live in this file.
* This file is responsible ONLY for rendering and wiring input events.

Controls
--------
    Arrow keys        – move player
    P                 – compute & display A* shortest path
    R                 – reset game
    Escape / Q        – quit
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import List, Optional, Tuple

# Ensure src/ modules are importable when launched from any directory
sys.path.insert(0, os.path.dirname(__file__))

from grid        import load_grid, find_start_goal
from game        import GameState
from pathfinding import find_path


# ---------------------------------------------------------------------------
# Visual constants
# ---------------------------------------------------------------------------
CELL_SIZE   = 48          # pixels per grid cell
PADDING     = 2           # gap between cells

# Colour palette
COLOURS = {
    'wall':       '#1a1a2e',   # deep navy
    'floor':      '#e8e8f0',   # off-white
    'start':      '#4caf50',   # green
    'goal':       '#f44336',   # red
    'player':     '#2196f3',   # blue
    'path':       '#ffc107',   # amber
    'bg':         '#12121f',   # very dark background
    'text_light': '#ffffff',
    'text_dark':  '#1a1a2e',
    'btn_bg':     '#2a2a4a',
    'btn_hover':  '#3a3a6a',
    'win_bg':     '#4caf50',
}

# Default level embedded in GUI (same as text_mode fallback)
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
# Main application class
# ---------------------------------------------------------------------------
class MazeApp(tk.Tk):
    """Top-level window; owns the GameState and orchestrates all widgets."""

    def __init__(self, level_source: Optional[str] = None):
        super().__init__()

        self.title("Maze Navigator – EG5041")
        self.configure(bg=COLOURS['bg'])
        self.resizable(False, False)

        # ---- Load game ----------------------------------------------------
        source = level_source if level_source else DEFAULT_LEVEL
        grid   = load_grid(source)
        start, goal = find_start_goal(grid)
        self.state = GameState(grid, start, goal)

        # ---- Build UI ---------------------------------------------------------
        self._build_header()
        self._build_canvas()
        self._build_controls()
        self._build_status()

        # ---- Key bindings -------------------------------------------------
        self.bind('<Up>',    lambda e: self._handle_move('Up'))
        self.bind('<Down>',  lambda e: self._handle_move('Down'))
        self.bind('<Left>',  lambda e: self._handle_move('Left'))
        self.bind('<Right>', lambda e: self._handle_move('Right'))
        self.bind('<p>',     lambda e: self._handle_pathfind())
        self.bind('<P>',     lambda e: self._handle_pathfind())
        self.bind('<r>',     lambda e: self._handle_reset())
        self.bind('<R>',     lambda e: self._handle_reset())
        self.bind('<Escape>',lambda e: self.quit())
        self.bind('<q>',     lambda e: self.quit())

        self.focus_set()
        self._redraw()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_header(self) -> None:
        frame = tk.Frame(self, bg=COLOURS['bg'])
        frame.pack(fill='x', padx=16, pady=(12, 0))
        tk.Label(
            frame, text="MAZE NAVIGATOR",
            font=('Courier New', 20, 'bold'),
            fg=COLOURS['text_light'], bg=COLOURS['bg']
        ).pack(side='left')

    def _build_canvas(self) -> None:
        rows, cols = len(self.state.grid), len(self.state.grid[0])
        w = cols * CELL_SIZE
        h = rows * CELL_SIZE
        self.canvas = tk.Canvas(
            self, width=w, height=h,
            bg=COLOURS['bg'], highlightthickness=0
        )
        self.canvas.pack(padx=16, pady=12)

    def _build_controls(self) -> None:
        frame = tk.Frame(self, bg=COLOURS['bg'])
        frame.pack(fill='x', padx=16, pady=(0, 8))

        btn_cfg = dict(
            font=('Courier New', 11, 'bold'),
            fg=COLOURS['text_light'],
            bg=COLOURS['btn_bg'],
            activebackground=COLOURS['btn_hover'],
            activeforeground=COLOURS['text_light'],
            relief='flat', bd=0, padx=14, pady=6, cursor='hand2'
        )

        tk.Button(frame, text="[P] Find Path",
                  command=self._handle_pathfind, **btn_cfg).pack(side='left', padx=4)
        tk.Button(frame, text="[R] Reset",
                  command=self._handle_reset,    **btn_cfg).pack(side='left', padx=4)
        tk.Button(frame, text="Load Level",
                  command=self._load_level,      **btn_cfg).pack(side='left', padx=4)
        tk.Button(frame, text="[Q] Quit",
                  command=self.quit,             **btn_cfg).pack(side='right', padx=4)

        # Legend
        legend = tk.Frame(self, bg=COLOURS['bg'])
        legend.pack(fill='x', padx=16, pady=(0, 4))
        items = [
            ('S Start', 'start'), ('G Goal', 'goal'),
            ('Player',  'player'),('Path',   'path'),
            ('Wall',    'wall'),
        ]
        for label, key in items:
            dot = tk.Label(legend, text='  ', bg=COLOURS[key], relief='flat')
            dot.pack(side='left', padx=(0, 2))
            tk.Label(legend, text=label + '  ',
                     font=('Courier New', 9),
                     fg=COLOURS['text_light'], bg=COLOURS['bg']
                     ).pack(side='left')

    def _build_status(self) -> None:
        self.status_var = tk.StringVar(value="Use arrow keys to move.")
        self.status_bar = tk.Label(
            self, textvariable=self.status_var,
            font=('Courier New', 10),
            fg=COLOURS['text_light'], bg=COLOURS['bg'],
            anchor='w'
        )
        self.status_bar.pack(fill='x', padx=16, pady=(0, 10))

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _redraw(self) -> None:
        """Clear and repaint the entire canvas from current game state."""
        self.canvas.delete('all')
        grid       = self.state.grid
        player_pos = self.state.player_pos
        path_set   = set(self.state.path)

        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                x0 = c * CELL_SIZE + PADDING
                y0 = r * CELL_SIZE + PADDING
                x1 = x0 + CELL_SIZE - PADDING * 2
                y1 = y0 + CELL_SIZE - PADDING * 2
                pos = (r, c)

                # Determine fill colour
                if pos == player_pos:
                    colour = COLOURS['player']
                    label  = 'P'
                elif cell == '#':
                    colour = COLOURS['wall']
                    label  = ''
                elif cell == 'S':
                    colour = COLOURS['start']
                    label  = 'S'
                elif cell == 'G':
                    colour = COLOURS['goal']
                    label  = 'G'
                elif pos in path_set:
                    colour = COLOURS['path']
                    label  = '·'
                else:
                    colour = COLOURS['floor']
                    label  = ''

                # Draw cell rectangle
                self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=colour, outline='', tags='cell'
                )

                # Draw label text inside cell
                if label:
                    text_colour = COLOURS['text_light'] if colour in (
                        COLOURS['wall'], COLOURS['player'],
                        COLOURS['goal'],  COLOURS['start']
                    ) else COLOURS['text_dark']
                    self.canvas.create_text(
                        (x0 + x1) // 2, (y0 + y1) // 2,
                        text=label,
                        font=('Courier New', int(CELL_SIZE * 0.35), 'bold'),
                        fill=text_colour
                    )

        # Update move counter in status bar
        self.status_var.set(
            f"Moves: {self.state.move_count}  |  "
            f"Position: {self.state.player_pos}  |  "
            f"Arrow keys = move  |  P = path  |  R = reset"
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _handle_move(self, direction: str) -> None:
        if self.state.won:
            return
        moved = self.state.apply_move(direction)
        if not moved:
            self.status_var.set("Blocked! Can't move that way.")
        self._redraw()
        if self.state.won:
            self._celebrate()

    def _handle_pathfind(self) -> None:
        """Run A* from current player position to goal and display the path."""
        if self.state.won:
            return
        path = find_path(self.state.grid, self.state.player_pos, self.state.goal_pos)
        if path:
            self.state.path = path
            steps = len(path) - 1
            self.status_var.set(f"Shortest path found: {steps} steps remaining.")
        else:
            self.state.path = []
            self.status_var.set("No path to goal – you may be trapped!")
        self._redraw()

    def _handle_reset(self) -> None:
        self.state.reset()
        self.status_var.set("Game reset. Use arrow keys to move.")
        self._redraw()

    def _load_level(self) -> None:
        """Let the user pick a .txt level file from disk."""
        path = filedialog.askopenfilename(
            title="Open level file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            grid  = load_grid(path)
            start, goal = find_start_goal(grid)
        except SystemExit:
            messagebox.showerror("Invalid level", "Level file must have exactly one S and one G.")
            return
        except Exception as exc:
            messagebox.showerror("Error loading level", str(exc))
            return

        # Rebuild canvas for new grid size
        self.state  = GameState(grid, start, goal)
        rows, cols  = len(grid), len(grid[0])
        self.canvas.config(width=cols * CELL_SIZE, height=rows * CELL_SIZE)
        self.status_var.set("Level loaded! Use arrow keys to move.")
        self._redraw()

    def _celebrate(self) -> None:
        """Overlay a win banner on the canvas."""
        rows = len(self.state.grid)
        cols = len(self.state.grid[0])
        cx   = (cols * CELL_SIZE) // 2
        cy   = (rows * CELL_SIZE) // 2

        self.canvas.create_rectangle(
            cx - 160, cy - 50, cx + 160, cy + 50,
            fill=COLOURS['win_bg'], outline='white', width=3
        )
        self.canvas.create_text(
            cx, cy - 12,
            text="🎉  YOU WIN!  🎉",
            font=('Courier New', 18, 'bold'),
            fill='white'
        )
        self.canvas.create_text(
            cx, cy + 18,
            text=f"Solved in {self.state.move_count} moves",
            font=('Courier New', 12),
            fill='white'
        )
        self.status_var.set(
            f"Congratulations! Solved in {self.state.move_count} moves. Press R to play again."
        )


# ---------------------------------------------------------------------------
def main(level_source: Optional[str] = None) -> None:
    app = MazeApp(level_source)
    app.mainloop()


if __name__ == '__main__':
    level = sys.argv[1] if len(sys.argv) > 1 else None
    main(level)
