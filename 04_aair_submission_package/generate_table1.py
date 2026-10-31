"""
generate_table1.py
Creates a clean, publication-quality (300 DPI) ablation study table as a PNG.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "table1_ablation.png")

# ── DATA ──────────────────────────────────────────────────────────────────────
headers = [
    "Prefix\nHorizon M",
    "Threshold\n\u03c4 (nats)",
    "PopQA\nEM (%)",
    "Bypass\nRate (%)",
    "Gating\nLatency (ms)",
    "Total\nLatency (ms)"
]

rows = [
    # Section A: Varying M (tau fixed at 2.0)
    ["M = 1", "\u03c4 = 2.0", "59.8", "61.2", "4.2",  "245.1"],
    ["M = 2", "\u03c4 = 2.0", "62.4", "70.5", "8.1",  "231.8"],
    ["M = 3", "\u03c4 = 2.0", "64.5", "74.8", "12.4", "224.8"],   # optimal row
    ["M = 4", "\u03c4 = 2.0", "64.6", "75.1", "16.8", "229.4"],
    ["M = 5", "\u03c4 = 2.0", "64.7", "75.4", "21.2", "234.1"],
    # Section B: Varying tau (M fixed at 3)
    ["M = 3", "\u03c4 = 1.6", "61.8", "58.2", "12.4", "262.1"],
    ["M = 3", "\u03c4 = 1.8", "63.4", "67.4", "12.4", "241.5"],
    ["M = 3", "\u03c4 = 2.0", "64.5", "74.8", "12.4", "224.8"],   # optimal row
    ["M = 3", "\u03c4 = 2.2", "62.9", "81.6", "12.4", "211.2"],
    ["M = 3", "\u03c4 = 2.4", "60.1", "88.2", "12.4", "198.5"],
]

# Rows that are the "selected optimal" configuration
optimal_rows = {2, 7}   # 0-indexed in `rows`

# ── FIGURE SETUP ─────────────────────────────────────────────────────────────
NCOLS = len(headers)
NROWS = len(rows)

COL_WIDTHS = [1.55, 1.55, 1.30, 1.30, 1.55, 1.55]   # inches
ROW_H      = 0.42   # inches per data row
HEADER_H   = 0.60   # inches for header

fig_w = sum(COL_WIDTHS) + 0.1
fig_h = HEADER_H + NROWS * ROW_H + 0.25

fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.axis('off')
fig.patch.set_facecolor('white')

# ── COLOUR PALETTE ────────────────────────────────────────────────────────────
COL_HEADER_BG  = '#2C3E50'
COL_HEADER_FG  = 'white'
ROW_ODD        = '#F8F9FA'
ROW_EVEN       = '#FFFFFF'
ROW_OPTIMAL    = '#EAF4FB'     # light blue highlight for optimal rows
BORDER         = '#BDC3C7'
OPTIMAL_BORDER = '#2980B9'
SECTION_SEP    = '#7F8C8D'     # colour for divider between section A and B
TXT            = '#2C3E50'

# ── HELPERS ───────────────────────────────────────────────────────────────────
def col_x_edges():
    """Returns list of x positions for left edge of each column."""
    xs = [0.0]
    for w in COL_WIDTHS:
        xs.append(xs[-1] + w)
    return xs

xs = col_x_edges()

def row_y(row_idx):
    """Bottom y of data row row_idx (0 = top data row)."""
    return fig_h - HEADER_H - (row_idx + 1) * ROW_H

def draw_cell(x, y, w, h, fc, ec=BORDER, lw=0.5):
    rect = mpatches.FancyBboxPatch((x, y), w, h,
                                   boxstyle="square,pad=0",
                                   facecolor=fc, edgecolor=ec,
                                   linewidth=lw, zorder=2)
    ax.add_patch(rect)

def cell_text(cx, cy, text, fs=8.5, fw='normal', fc=TXT, va='center'):
    ax.text(cx, cy, text, ha='center', va=va,
            fontsize=fs, fontweight=fw, color=fc,
            zorder=4, multialignment='center', linespacing=1.3)

# ── DRAW HEADER ───────────────────────────────────────────────────────────────
header_y = fig_h - HEADER_H
for c, (hdr, w, x0) in enumerate(zip(headers, COL_WIDTHS, xs)):
    draw_cell(x0, header_y, w, HEADER_H, COL_HEADER_BG, ec='white', lw=0.8)
    cell_text(x0 + w/2, header_y + HEADER_H/2, hdr, fs=8.5, fw='bold', fc=COL_HEADER_FG)

# ── DRAW DATA ROWS ────────────────────────────────────────────────────────────
for r, row in enumerate(rows):
    ry = row_y(r)
    is_opt = (r in optimal_rows)

    # Section divider before row 5 (between section A and B)
    if r == 5:
        ax.plot([0, fig_w], [ry + ROW_H, ry + ROW_H],
                color=SECTION_SEP, lw=1.2, zorder=5, linestyle='--')

    for c, (cell, w, x0) in enumerate(zip(row, COL_WIDTHS, xs)):
        bg = ROW_OPTIMAL if is_opt else (ROW_ODD if r % 2 == 0 else ROW_EVEN)
        ec = OPTIMAL_BORDER if is_opt else BORDER
        lw = 0.9 if is_opt else 0.4
        draw_cell(x0, ry, w, ROW_H, bg, ec=ec, lw=lw)

        fw = 'bold' if is_opt else 'normal'
        cell_text(x0 + w/2, ry + ROW_H/2, cell, fs=8.5, fw=fw)

# ── OUTER BORDER ─────────────────────────────────────────────────────────────
outer = mpatches.FancyBboxPatch(
    (0, row_y(NROWS - 1)), fig_w, fig_h - row_y(NROWS - 1),
    boxstyle="square,pad=0",
    facecolor='none', edgecolor='#2C3E50', linewidth=1.6, zorder=6)
ax.add_patch(outer)

# ── VERTICAL COLUMN DIVIDERS ─────────────────────────────────────────────────
top_y    = fig_h
bottom_y = row_y(NROWS - 1)
for x in xs[1:-1]:
    ax.plot([x, x], [bottom_y, top_y], color=BORDER, lw=0.5, zorder=3)

# ── SECTION ANNOTATIONS ───────────────────────────────────────────────────────
# Label section A (rows 0-4) and B (rows 5-9) on the left margin
sec_a_mid = (row_y(0) + ROW_H + row_y(4)) / 2
sec_b_mid = (row_y(5) + ROW_H + row_y(9)) / 2

for ymid, lbl in [(sec_a_mid, 'Part A\n(vary M)'), (sec_b_mid, 'Part B\n(vary \u03c4)')]:
    ax.text(-0.08, ymid, lbl, ha='right', va='center',
            fontsize=7, color='#555', style='italic',
            multialignment='center', linespacing=1.3, zorder=5)

# ── LEGEND NOTE ───────────────────────────────────────────────────────────────
ax.text(fig_w / 2, row_y(NROWS - 1) - 0.14,
        'Highlighted rows (\u25a0) = selected optimal configuration  (M = 3, \u03c4 = 2.0 nats)',
        ha='center', va='top', fontsize=7.5, color='#2980B9', style='italic', zorder=5)

# ── SAVE ──────────────────────────────────────────────────────────────────────
plt.savefig(OUT, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"[OK] Saved -> {OUT}")

