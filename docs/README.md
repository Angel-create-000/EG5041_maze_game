# EG5041 – Maze Navigator

A grid-based maze game with A\* pathfinding, a terminal driver, and a tkinter GUI.

---

## Requirements

Python 3.8 or later. No third-party packages needed — only the standard library (`tkinter`, `heapq`, `unittest`).

To confirm tkinter is available:
```bash
python -m tkinter
```
On Ubuntu/Debian if it is missing:
```bash
sudo apt-get install python3-tk
```

---

## Running the game

### GUI mode (recommended)
```bash
cd src
python gui.py                          # default built-in level
python gui.py ../examples/easy.txt     # load a level file
python gui.py ../examples/medium.txt
python gui.py ../examples/hard.txt
```

### Text / terminal mode (for testing core logic)
```bash
cd src
python text_mode.py                    # default level
python text_mode.py ../examples/easy.txt
```

**Controls (both modes)**

| Key | Action |
|-----|--------|
| Arrow keys / w a s d | Move player |
| P | Compute & display A\* shortest path |
| R | Reset to start |
| Q / Escape | Quit |

---

## Running the tests
```bash
cd tests
python -m unittest discover -v
```
Or run individual files:
```bash
python test_grid.py
python test_pathfinding.py
python test_game.py
```

---

## Project structure

```
EG5041_maze_game/
├── src/
│   ├── grid.py          # Grid I/O, S/G detection, walkability checks
│   ├── game.py          # Player movement, GameState, win detection
│   ├── pathfinding.py   # A* algorithm (find_path)
│   ├── text_mode.py     # Terminal driver (testing + marking)
│   └── gui.py           # tkinter GUI (reuses the above)
├── tests/
│   ├── test_grid.py
│   ├── test_pathfinding.py
│   └── test_game.py
├── examples/
│   ├── easy.txt
│   ├── medium.txt
│   └── hard.txt
└── docs/
    └── README.md        # (this file)
```

---

## Pathfinding algorithm: A\*

A\* is used in preference to plain BFS or Dijkstra's because:

- **Optimal**: guaranteed to find the shortest path on a uniform-cost grid.
- **Efficient**: the Manhattan-distance heuristic (`|Δrow| + |Δcol|`) directs the search toward the goal, so fewer cells are expanded than with BFS.
- **Admissible & consistent**: the heuristic never over-estimates cost (no diagonal moves), so optimality is preserved.

The implementation lives entirely in `pathfinding.py` and is accessed through the single public function `find_path(grid, start, goal) -> list[(row, col)]`.

---

## Level file format

Plain text, one row per line. Use exactly one `S` (start) and one `G` (goal).

```
#########
#S......#
#.###...#
#.....#G#
#########
```

| Character | Meaning |
|-----------|---------|
| `#` | Wall (not walkable) |
| `.` | Floor (walkable) |
| `S` | Start position |
| `G` | Goal position |
