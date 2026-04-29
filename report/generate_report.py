"""
Generate EG5041_uXXXXXXX_report.pdf  – replace STUDENT_ID below.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

STUDENT_ID = "uXXXXXXX"          # <-- replace with your student ID
OUTPUT     = f"/mnt/user-data/outputs/EG5041_{STUDENT_ID}_report.pdf"

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def make_styles():
    header = ParagraphStyle(
        'header', fontName='Helvetica-Bold', fontSize=13,
        spaceAfter=4, leading=16
    )
    sub = ParagraphStyle(
        'sub', fontName='Helvetica-Bold', fontSize=11,
        spaceAfter=2, spaceBefore=6, leading=14
    )
    body = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=11,
        spaceAfter=3, leading=14, alignment=TA_JUSTIFY
    )
    mono = ParagraphStyle(
        'mono', fontName='Courier', fontSize=10,
        spaceAfter=2, leading=13
    )
    right = ParagraphStyle(
        'right', fontName='Helvetica', fontSize=10,
        alignment=2   # right-align
    )
    return header, sub, body, mono, right

# ---------------------------------------------------------------------------
def build_report():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=MARGIN,
    )

    H, S, B, M, R = make_styles()
    story = []

    # ---- Right-aligned student ID (required by brief) --------------------
    story.append(Paragraph(f"Student ID: <b>{STUDENT_ID}</b>", R))
    story.append(Spacer(1, 2*mm))

    # ---- Title -----------------------------------------------------------
    story.append(Paragraph("EG5041 Applied Programming – Maze Navigator", H))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 3*mm))

    # ---- 1. Architecture -------------------------------------------------
    story.append(Paragraph("1  Code Architecture", S))
    story.append(Paragraph(
        "The project is split into four modules under <font name='Courier'>src/</font> "
        "so that the GUI and terminal driver share identical logic without duplication.",
        B
    ))

    # Module table
    tdata = [
        ["Module", "Responsibility"],
        ["grid.py",        "Load level files, locate S/G, walkability checks"],
        ["game.py",        "Player movement (move_player), win detection, GameState"],
        ["pathfinding.py", "A* algorithm (find_path, heuristic)"],
        ["text_mode.py",   "Terminal driver for marking / debugging"],
        ["gui.py",         "tkinter window; reuses the three modules above"],
    ]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('FONTNAME',   (0,1), (0,-1), 'Courier'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
        ('GRID',       (0,0), (-1,-1), 0.4, colors.grey),
        ('LEFTPADDING',(0,0), (-1,-1), 5),
        ('RIGHTPADDING',(0,0),(-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ])
    col_w = [(PAGE_W - 2*MARGIN) * r for r in [0.25, 0.75]]
    t = Table(tdata, colWidths=col_w, style=ts)
    story.append(t)
    story.append(Spacer(1, 3*mm))

    # ---- 2. Pathfinding --------------------------------------------------
    story.append(Paragraph("2  Pathfinding: A*", S))
    story.append(Paragraph(
        "A* was chosen over plain BFS because it uses a heuristic to direct the search "
        "toward the goal, expanding fewer nodes while still guaranteeing the shortest path. "
        "On a uniform-cost grid (every walkable step costs 1) the Manhattan distance "
        "h(n) = |&Delta;row| + |&Delta;col| is both admissible (never over-estimates) "
        "and consistent, so A* returns an optimal result. "
        "The priority queue (Python <font name='Courier'>heapq</font>) is keyed on "
        "f = g + h, where g is the exact cost from the start and h is the heuristic. "
        "The algorithm correctly returns an empty list when no path exists.",
        B
    ))

    # ---- 3. GUI design decision ------------------------------------------
    story.append(Paragraph("3  GUI Design Decision", S))
    story.append(Paragraph(
        "The tkinter layer in <font name='Courier'>gui.py</font> contains no game logic. "
        "It instantiates a <font name='Courier'>GameState</font> object from "
        "<font name='Courier'>game.py</font> and calls "
        "<font name='Courier'>find_path</font> from "
        "<font name='Courier'>pathfinding.py</font> directly. "
        "This separation ensures the core logic is fully testable without a display, "
        "and the GUI cannot diverge from the rules enforced by the movement functions. "
        "Cell size (48 px), colours, and the win banner are the only GUI-specific concerns.",
        B
    ))

    # ---- 4. Testing ------------------------------------------------------
    story.append(Paragraph("4  Testing", S))
    story.append(Paragraph(
        "40 unit tests across three files cover: grid loading and validation, "
        "walkability edge cases, movement blocking (walls, boundaries), "
        "win detection, <font name='Courier'>GameState</font> reset, "
        "A* optimality, path connectivity, and the no-path case. "
        "Run with <font name='Courier'>python -m unittest discover -v</font> from "
        "<font name='Courier'>tests/</font>.",
        B
    ))

    # ---- 5. How to run ---------------------------------------------------
    story.append(Paragraph("5  Running the Game", S))
    for cmd, desc in [
        ("python src/gui.py",                    "Launch GUI (default built-in level)"),
        ("python src/gui.py examples/easy.txt",  "GUI with easy level"),
        ("python src/text_mode.py",              "Terminal mode (w/a/s/d, p = path, r = reset)"),
        ("python -m unittest discover -v",       "Run all tests (from tests/)"),
    ]:
        story.append(Paragraph(
            f"<font name='Courier'>{cmd}</font> &nbsp;&nbsp; <i>{desc}</i>", B
        ))

    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 2*mm))

    # ---- GitHub & certificate (outside 1-page limit per brief) ----------
    story.append(Paragraph(
        "<b>GitHub:</b> https://github.com/YOUR_USERNAME/EG5041_maze_game", B
    ))
    story.append(Paragraph(
        "<b>freeCodeCamp Python Certificate:</b> https://freecodecamp.org/certification/YOUR_USERNAME/python-v9", B
    ))

    doc.build(story)
    print(f"Report written to {OUTPUT}")

if __name__ == '__main__':
    build_report()
