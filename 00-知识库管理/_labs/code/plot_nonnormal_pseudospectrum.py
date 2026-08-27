#!/usr/bin/env python3
"""Deterministic SVG for the nonnormal-pseudospectrum chapter.

The first two panels evaluate sigma_min(zI-A_K) on a Cartesian grid and use
marching squares for its epsilon-level sets.  The third panel uses the exact
2-by-2 spectral-norm formula for exp(t A_K).  No plotting dependency is needed.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


WIDTH = 1380
HEIGHT = 500
OUTPUT_WIDTH = 1200
OUTPUT_HEIGHT = 435
OUTPUT_SCALE = OUTPUT_WIDTH / WIDTH
PANEL_W = 400
PANEL_H = 330
TOP = 88
LEFTS = (58, 490, 922)
X_DOMAIN = (-4.0, 1.5)
Y_DOMAIN = (-2.6, 2.6)
EPS_LEVELS = (0.03, 0.1, 0.3, 1.0)
COLORS = ("#2563eb", "#0f766e", "#64748b", "#c24135")
GRID_NX = 151
GRID_NY = 143


def smin_shifted_ak(x: float, y: float, k: float) -> float:
    """Return sigma_min(zI-A_K), A_K=[[-1,k],[0,-2]], z=x+iy."""
    a2 = (x + 1.0) ** 2 + y * y
    d2 = (x + 2.0) ** 2 + y * y
    trace = a2 + k * k + d2
    determinant_squared = a2 * d2
    disc = math.sqrt(max(0.0, trace * trace - 4.0 * determinant_squared))
    denominator = trace + disc
    if denominator == 0.0:
        return 0.0
    # This product-over-large-root form avoids cancellation near eigenvalues.
    smallest_squared = 2.0 * determinant_squared / denominator
    return math.sqrt(max(0.0, smallest_squared))


def exp_norm_ak(t: float, k: float) -> float:
    """Return ||exp(t A_K)||_2 from the exact upper-triangular exponential."""
    a = math.exp(-t)
    d = math.exp(-2.0 * t)
    b = k * (a - d)
    trace = a * a + b * b + d * d
    determinant_squared = (a * d) ** 2
    largest_squared = 0.5 * (
        trace + math.sqrt(max(0.0, trace * trace - 4.0 * determinant_squared))
    )
    return math.sqrt(max(0.0, largest_squared))


def sx(x: float, left: float) -> float:
    lo, hi = X_DOMAIN
    return left + PANEL_W * (x - lo) / (hi - lo)


def sy(y: float) -> float:
    lo, hi = Y_DOMAIN
    return TOP + PANEL_H * (hi - y) / (hi - lo)


def interpolate(p0, p1, q0: float, q1: float):
    if abs(q1 - q0) < 1e-15:
        t = 0.5
    else:
        t = -q0 / (q1 - q0)
    t = min(1.0, max(0.0, t))
    return (p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]))


def contour_segments(k: float, epsilon: float):
    xs = [
        X_DOMAIN[0] + i * (X_DOMAIN[1] - X_DOMAIN[0]) / (GRID_NX - 1)
        for i in range(GRID_NX)
    ]
    ys = [
        Y_DOMAIN[0] + j * (Y_DOMAIN[1] - Y_DOMAIN[0]) / (GRID_NY - 1)
        for j in range(GRID_NY)
    ]
    values = [
        [smin_shifted_ak(x, y, k) - epsilon for x in xs]
        for y in ys
    ]
    segments = []
    for j in range(GRID_NY - 1):
        for i in range(GRID_NX - 1):
            points = (
                (xs[i], ys[j]),
                (xs[i + 1], ys[j]),
                (xs[i + 1], ys[j + 1]),
                (xs[i], ys[j + 1]),
            )
            q = (
                values[j][i],
                values[j][i + 1],
                values[j + 1][i + 1],
                values[j + 1][i],
            )
            edge_pairs = ((0, 1), (1, 2), (2, 3), (3, 0))
            crossings = []
            for edge, (u, v) in enumerate(edge_pairs):
                if q[u] == 0.0 or q[v] == 0.0 or (q[u] < 0.0) != (q[v] < 0.0):
                    crossings.append((edge, interpolate(points[u], points[v], q[u], q[v])))
            if len(crossings) == 2:
                segments.append((crossings[0][1], crossings[1][1]))
            elif len(crossings) == 4:
                # Resolve the saddle consistently from the cell-center sign.
                center_negative = sum(q) < 0.0
                corner_negative = q[0] < 0.0
                by_edge = {edge: point for edge, point in crossings}
                if center_negative == corner_negative:
                    pairs = ((0, 1), (2, 3))
                else:
                    pairs = ((0, 3), (1, 2))
                for e0, e1 in pairs:
                    segments.append((by_edge[e0], by_edge[e1]))
    return segments


def text(x, y, value, size=14, weight=400, anchor="start", fill="#172033"):
    size = max(size, 18)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        f"{html.escape(str(value))}</text>"
    )


def pseudospectrum_panel(left: float, k: float, label: str, subtitle: str):
    out = []
    out.append(text(left, 38, label, 19, 700))
    out.append(text(left, 63, subtitle, 13, 400, fill="#526070"))
    out.append(
        f'<rect x="{left}" y="{TOP}" width="{PANEL_W}" height="{PANEL_H}" '
        'fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
    )
    for x in (-4, -3, -2, -1, 0, 1):
        px = sx(x, left)
        out.append(
            f'<line x1="{px:.2f}" y1="{TOP}" x2="{px:.2f}" y2="{TOP + PANEL_H}" '
            'stroke="#edf0f4" stroke-width="1"/>'
        )
        out.append(text(px, TOP + PANEL_H + 22, x, 12, anchor="middle", fill="#526070"))
    for y in (-2, -1, 0, 1, 2):
        py = sy(y)
        out.append(
            f'<line x1="{left}" y1="{py:.2f}" x2="{left + PANEL_W}" y2="{py:.2f}" '
            'stroke="#edf0f4" stroke-width="1"/>'
        )
        out.append(text(left - 10, py + 4, y, 12, anchor="end", fill="#526070"))
    out.append(
        f'<line x1="{sx(0, left):.2f}" y1="{TOP}" x2="{sx(0, left):.2f}" '
        f'y2="{TOP + PANEL_H}" stroke="#788596" stroke-width="1.2" stroke-dasharray="5 4"/>'
    )
    out.append(
        f'<line x1="{left}" y1="{sy(0):.2f}" x2="{left + PANEL_W}" y2="{sy(0):.2f}" '
        'stroke="#788596" stroke-width="1.2"/>'
    )
    for epsilon, color in zip(EPS_LEVELS, COLORS):
        pieces = []
        for p0, p1 in contour_segments(k, epsilon):
            pieces.append(
                f"M {sx(p0[0], left):.2f} {sy(p0[1]):.2f} "
                f"L {sx(p1[0], left):.2f} {sy(p1[1]):.2f}"
            )
        out.append(
            f'<path d="{" ".join(pieces)}" fill="none" stroke="{color}" '
            'stroke-width="1.8" stroke-linecap="round"/>'
        )
    for eigenvalue in (-2.0, -1.0):
        px, py = sx(eigenvalue, left), sy(0)
        out.append(
            f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4.2" fill="#111827" '
            'stroke="#ffffff" stroke-width="1.2"/>'
        )
    out.append(text(left + PANEL_W / 2, TOP + PANEL_H + 46, "Re z", 13, 600, "middle"))
    out.append(
        f'<text x="{left - 41:.1f}" y="{TOP + PANEL_H / 2:.1f}" font-size="18" '
        'font-weight="600" text-anchor="middle" fill="#172033" '
        f'transform="rotate(-90 {left - 41:.1f} {TOP + PANEL_H / 2:.1f})">Im z</text>'
    )
    return out


def transient_panel(left: float):
    out = []
    out.append(text(left, 38, "C  相同点谱，不同瞬态", 19, 700))
    out.append(text(left, 63, "||exp(tA_K)||₂；两者 α(A) = −1", 13, 400, fill="#526070"))
    out.append(
        f'<rect x="{left}" y="{TOP}" width="{PANEL_W}" height="{PANEL_H}" '
        'fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
    )
    times = [5.0 * i / 300 for i in range(301)]
    series = [(0.0, "#2563eb"), (8.0, "#c24135")]
    values = {k: [exp_norm_ak(t, k) for t in times] for k, _ in series}
    ymax = 1.1 * max(max(v) for v in values.values())

    def tx(t):
        return left + PANEL_W * t / 5.0

    def ty(v):
        return TOP + PANEL_H * (ymax - v) / ymax

    for t in range(0, 6):
        px = tx(t)
        out.append(
            f'<line x1="{px:.2f}" y1="{TOP}" x2="{px:.2f}" y2="{TOP + PANEL_H}" '
            'stroke="#edf0f4" stroke-width="1"/>'
        )
        out.append(text(px, TOP + PANEL_H + 22, t, 12, anchor="middle", fill="#526070"))
    ystep = 0.5
    y = 0.0
    while y <= ymax + 1e-12:
        py = ty(y)
        out.append(
            f'<line x1="{left}" y1="{py:.2f}" x2="{left + PANEL_W}" y2="{py:.2f}" '
            'stroke="#edf0f4" stroke-width="1"/>'
        )
        out.append(text(left - 10, py + 4, f"{y:.1f}", 12, anchor="end", fill="#526070"))
        y += ystep
    out.append(
        f'<line x1="{left}" y1="{ty(1):.2f}" x2="{left + PANEL_W}" y2="{ty(1):.2f}" '
        'stroke="#788596" stroke-width="1.2" stroke-dasharray="5 4"/>'
    )
    for k, color in series:
        points = " ".join(
            f"{tx(t):.2f},{ty(v):.2f}" for t, v in zip(times, values[k])
        )
        out.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" '
            'stroke-width="2.6" stroke-linejoin="round"/>'
        )
        if k == 8.0:
            peak_i = max(range(len(times)), key=lambda i: values[k][i])
            peak_t = times[peak_i]
            peak_v = values[k][peak_i]
            out.append(
                f'<circle cx="{tx(peak_t):.2f}" cy="{ty(peak_v):.2f}" r="4.0" '
                f'fill="{color}" stroke="#ffffff" stroke-width="1.2"/>'
            )
            out.append(
                text(
                    tx(peak_t) + 10,
                    ty(peak_v) + 22,
                    f"峰值≈{peak_v:.2f}",
                    12,
                    600,
                    fill=color,
                )
            )
    out.append(text(left + PANEL_W / 2, TOP + PANEL_H + 46, "时间 t", 13, 600, "middle"))
    out.append(
        f'<text x="{left - 43:.1f}" y="{TOP + PANEL_H / 2:.1f}" font-size="18" '
        'font-weight="600" text-anchor="middle" fill="#172033" '
        f'transform="rotate(-90 {left - 43:.1f} {TOP + PANEL_H / 2:.1f})">传播范数</text>'
    )
    legend_y = TOP + 19
    for idx, (k, color) in enumerate(series):
        x0 = left + 18 + 117 * idx
        out.append(
            f'<line x1="{x0}" y1="{legend_y}" x2="{x0 + 25}" y2="{legend_y}" '
            f'stroke="{color}" stroke-width="2.6"/>'
        )
        out.append(text(x0 + 32, legend_y + 4, f"K={int(k)}", 12, 600))
    return out


def build_svg() -> str:
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" '
        f'viewBox="0 0 {OUTPUT_WIDTH} {OUTPUT_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">正规与非正规矩阵的伪谱和瞬态增长</title>',
        '<desc id="desc">前两面板比较 A_0 和 A_8 的二范数伪谱，第三面板比较相同点谱下矩阵指数的传播范数。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<rect width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" fill="#fffefb"/>',
        f'<g transform="scale({OUTPUT_SCALE:.8f})">',
        *pseudospectrum_panel(
            LEFTS[0],
            0.0,
            "A  正规基线：A₀ = diag(−1,−2)",
            "ε-伪谱是特征值周围的 ε 圆盘",
        ),
        *pseudospectrum_panel(
            LEFTS[1],
            8.0,
            "B  非正规耦合：A₈",
            "点谱不变，σmin(zI−A) 等值线显著鼓出",
        ),
        *transient_panel(LEFTS[2]),
    ]
    legend_x = 58
    legend_y = 480
    out.append(text(legend_x, legend_y, "绝对 2-范数伪谱边界：", 12, 600))
    cursor = legend_x + 157
    for epsilon, color in zip(EPS_LEVELS, COLORS):
        out.append(
            f'<line x1="{cursor}" y1="{legend_y - 4}" x2="{cursor + 24}" '
            f'y2="{legend_y - 4}" stroke="{color}" stroke-width="2"/>'
        )
        out.append(text(cursor + 30, legend_y, f"ε={epsilon:g}", 12))
        cursor += 82
    out.append(text(570, legend_y, "黑点：λ=−2,−1；虚线：稳定边界 Re z=0", 12, fill="#526070"))
    out.append(text(1348, legend_y, "网格 151×143", 11, anchor="end", fill="#6b7280"))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    knowledge_root = Path(__file__).resolve().parents[2]
    output = (
        knowledge_root
        / "_assets"
        / "plots"
        / "pseudospectra"
        / "plot-normal-vs-nonnormal-pseudospectrum-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
