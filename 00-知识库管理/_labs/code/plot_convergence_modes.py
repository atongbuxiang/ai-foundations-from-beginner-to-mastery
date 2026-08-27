#!/usr/bin/env python3
"""Generate the deterministic SVG for limits and convergence modes.

Panel A visualizes the epsilon-N tail definition for a_n = 1/n.
Panel B shows pointwise but non-uniform convergence of x^n on [0, 1].
Panel C shows continuous spikes with pointwise limit zero and fixed L1 mass.
No third-party Python packages are required.
"""

from __future__ import annotations

import html
from pathlib import Path


WIDTH = 1380
HEIGHT = 500
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = round(HEIGHT * CANVAS_WIDTH / WIDTH)
SCALE = CANVAS_WIDTH / WIDTH
BG = "#FFFEFB"
INK = "#1F2937"
MUTED = "#64748B"
GRID = "#D7DEE8"
BLUE = "#2563eb"
PURPLE = "#2563EB"
ORANGE = "#0F766E"
GREEN = "#0F766E"
PINK = "#C24135"


def esc(value):
    return html.escape(str(value))


def text(x, y, value, size=14, weight=400, anchor="start", fill=INK):
    size = 22 if size >= 19 else max(size, 18)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        f"{esc(value)}</text>"
    )


def line(x1, y1, x2, y2, color=GRID, width=1.0, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}"{dash_attr}/>'
    )


def polyline(points, color, width=2.0, fill="none", opacity=1.0, dash=None):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{color}" '
        f'stroke-width="{width}" opacity="{opacity}"{dash_attr}/>'
    )


def panel_axes(out, x, y, w, h, x_label, y_label):
    out.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        'fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
    )
    out.append(line(x, y + h, x + w, y + h, INK, 1.2))
    out.append(line(x, y, x, y + h, INK, 1.2))
    out.append(text(x + w, y + h + 25, x_label, 12, 600, "end"))
    out.append(
        f'<text x="{x - 34:.1f}" y="{y + h / 2:.1f}" font-size="18" '
        f'font-weight="600" text-anchor="middle" fill="{INK}" '
        f'transform="rotate(-90 {x - 34:.1f} {y + h / 2:.1f})">'
        f"{esc(y_label)}</text>"
    )


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">极限量词、逐点与一致收敛、尖峰反例</title>',
        '<desc id="desc">三个面板分别展示 epsilon-N 尾部、x 的 n 次方逐点但非一致收敛，以及面积不消失的连续尖峰。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: epsilon-N.
    x0 = 48
    out.append(text(x0, 38, "A  ε–N：控制整个无限尾部", 19, 700))
    out.append(text(x0, 63, "a_n=1/n；取 ε=0.15，可选 N=7", 13, fill=MUTED))
    ax, ay, aw, ah = x0 + 40, 103, 330, 250
    panel_axes(out, ax, ay, aw, ah, "n", "|a_n−0|")
    y_max = 1.05
    epsilon = 0.15
    eps_y = ay + ah * (1 - epsilon / y_max)
    out.append(
        f'<rect x="{ax:.1f}" y="{eps_y:.1f}" width="{aw:.1f}" '
        f'height="{ay + ah - eps_y:.1f}" fill="{BLUE}" opacity="0.10"/>'
    )
    out.append(line(ax, eps_y, ax + aw, eps_y, BLUE, 1.8, "6 4"))
    out.append(text(ax + aw - 4, eps_y - 8, "ε 带", 11, 600, "end", BLUE))
    points = []
    for n in range(1, 81):
        px = ax + aw * (n - 1) / 79
        py = ay + ah * (1 - (1 / n) / y_max)
        points.append((px, py))
    out.append(polyline(points, PURPLE, 2.2))
    for n in (1, 2, 3, 5, 7, 10, 20, 40, 80):
        px, py = points[n - 1]
        out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2.6" fill="{PURPLE}"/>')
    n7x = points[6][0]
    out.append(line(n7x, ay, n7x, ay + ah, ORANGE, 1.7, "5 4"))
    out.append(text(n7x + 5, ay + 17, "N=7", 11, 700, fill=ORANGE))
    out.append(text(x0 + 10, 392, "不是“命中一次”，而是 n≥N 后永远合格。", 13, 600))
    out.append(text(x0 + 10, 417, "有限前缀可以很坏；定义只约束尾部。", 12, fill=MUTED))

    # Panel B: x^n.
    x1 = 495
    out.append(text(x1, 38, "B  逐点收敛 ≠ 一致收敛", 19, 700))
    out.append(text(x1, 63, "f_n(x)=x^n on [0,1]；坏区向 x=1 逃逸", 13, fill=MUTED))
    bx, by, bw, bh = x1 + 42, 103, 330, 250
    panel_axes(out, bx, by, bw, bh, "x", "f_n(x)")
    colors = [(1, BLUE), (2, GREEN), (5, ORANGE), (20, PINK)]
    for n, color in colors:
        pts = []
        for k in range(201):
            x = k / 200
            y = x**n
            pts.append((bx + bw * x, by + bh * (1 - y)))
        out.append(polyline(pts, color, 2.0))
    # Pointwise limit: zero on [0,1), one at 1.
    out.append(line(bx, by + bh, bx + bw, by + bh, PURPLE, 2.0, "5 4"))
    out.append(f'<circle cx="{bx + bw:.1f}" cy="{by:.1f}" r="4.2" fill="{PURPLE}"/>')
    out.append(text(bx + 18, by + 23, "n=1", 11, 700, fill=BLUE))
    out.append(text(bx + 69, by + 23, "n=2", 11, 700, fill=GREEN))
    out.append(text(bx + 120, by + 23, "n=5", 11, 700, fill=ORANGE))
    out.append(text(bx + 171, by + 23, "n=20", 11, 700, fill=PINK))
    out.append(text(x1 + 10, 392, "每个固定 x<1 最终趋零；共同等待时间不存在。", 13, 600))
    out.append(text(x1 + 10, 417, "sup_x |f_n−f|=1，且极限函数在 1 不连续。", 12, fill=MUTED))

    # Panel C: spike functions.
    x2 = 940
    out.append(text(x2, 38, "C  点态/a.s. 好，不等于 L¹ 好", 19, 700))
    out.append(text(x2, 63, "连续尖峰：高度 n、底宽 2/n、面积恒为 1", 13, fill=MUTED))
    cx, cy, cw, ch = x2 + 43, 103, 330, 250
    panel_axes(out, cx, cy, cw, ch, "x", "h_n(x)")
    n_values = [(2, BLUE), (5, ORANGE), (12, PINK)]
    max_y = 12.5
    for n, color in n_values:
        pts_xy = [(0.0, 0.0), (1 / n, float(n)), (2 / n, 0.0), (1.0, 0.0)]
        pts = [
            (cx + cw * x, cy + ch * (1 - y / max_y))
            for x, y in pts_xy
        ]
        out.append(polyline(pts, color, 2.3))
        peak_x, peak_y = pts[1]
        out.append(text(peak_x + 4, peak_y - 7, f"n={n}", 11, 700, fill=color))
    out.append(text(x2 + 10, 392, "对每个固定 x，尖峰最终离开；但总面积不减少。", 13, 600))
    out.append(text(x2 + 10, 417, "∫h_n=1：逐点收敛不能直接交换积分/期望。", 12, fill=MUTED))

    out.append(text(WIDTH - 34, 480, "确定性解析数据；生成日期 2026-08-16", 11, anchor="end", fill=MUTED))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    knowledge_root = Path(__file__).resolve().parents[2]
    output = (
        knowledge_root
        / "_assets"
        / "figures"
        / "convergence-modes"
        / "fig-convergence-modes-quantifiers-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
