#!/usr/bin/env python3
"""Render the matrix-exponential transient experiment in v2 research-plot style."""

from __future__ import annotations

from html import escape
from math import log
from pathlib import Path

from plot_matrix_exponential_transient import K_VALUES, peak, spectral_norm


W, H = 1200, 600
BG = "#FFFEFB"
INK = "#1F2937"
MUTED = "#64748B"
GRID = "#D7DEE8"
BLUE = "#2563EB"
TEAL = "#0F766E"
RED = "#C24135"
LEFT, TOP = 72, 92
PW, PH = 750, 400
T_MIN, T_MAX = 0.0, 5.0
Y_MIN, Y_MAX = 0.0, 5.4
COLORS = {0.0: BLUE, 5.0: TEAL, 20.0: RED}


def xmap(t: float) -> float:
    return LEFT + (t - T_MIN) / (T_MAX - T_MIN) * PW


def ymap(y: float) -> float:
    return TOP + PH - (y - Y_MIN) / (Y_MAX - Y_MIN) * PH


def curve(k: float, steps: int = 600) -> str:
    pts = []
    for i in range(steps + 1):
        t = T_MIN + (T_MAX - T_MIN) * i / steps
        pts.append(f"{xmap(t):.2f},{ymap(spectral_norm(t, k)):.2f}")
    return "M" + " L".join(pts)


def txt(x: float, y: float, value: str, size: int = 16, weight: int = 400,
        anchor: str = "start", fill: str = INK, cls: str = "") -> str:
    klass = f' class="{cls}"' if cls else ""
    return (f'<text x="{x}" y="{y}" font-size="{max(15, size)}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{klass}>'
            f'{escape(value)}</text>')


def build() -> str:
    peaks = {k: peak(k) for k in K_VALUES}
    assert abs(peaks[0.0][0] - 1.0) < 1e-12
    assert peaks[20.0][0] > 5.0 and 0.5 < peaks[20.0][1] < 0.9
    assert abs(20.0 * (0.5 - 0.25) - 5.0) < 1e-12
    assert spectral_norm(5.0, 20.0) < 0.14

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">相同稳定特征值仍可产生不同有限时间瞬态</title>',
        '<desc id="desc">精确绘制 A_K=[[-1,K],[0,-2]] 在 K 等于零、五、二十时的矩阵指数二范数。三者谱横坐标都为负一，但非正规耦合增大时有限时间峰值显著上升，随后仍渐近衰减。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.math{font-family:"STIX Two Text","Times New Roman",serif}</style></defs>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        txt(42, 50, "相同稳定谱，不同有限时间放大", 23, 700),
        txt(810, 50, "证据合同", 21, 700, fill=RED),
    ]

    for y in range(0, 6):
        yy = ymap(float(y))
        out += [f'<line x1="{LEFT}" y1="{yy:.2f}" x2="{LEFT+PW}" y2="{yy:.2f}" stroke="{GRID}" stroke-width="1.2"/>', txt(LEFT-14, yy+5, str(y), 15, 500, "end", MUTED)]
    for t in range(0, 6):
        xx = xmap(float(t))
        out += [f'<line x1="{xx:.2f}" y1="{TOP}" x2="{xx:.2f}" y2="{TOP+PH}" stroke="{GRID}" stroke-width="1"/>', txt(xx, TOP+PH+27, str(t), 15, 500, "middle", MUTED)]
    out += [
        f'<line x1="{LEFT}" y1="{TOP+PH}" x2="{LEFT+PW}" y2="{TOP+PH}" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{TOP+PH}" stroke="{INK}" stroke-width="1.8"/>',
        txt(LEFT+PW/2, 542, "time  t", 16, 650, "middle"),
        txt(20, TOP+PH/2, "||exp(t A_K)||_2", 16, 650, "middle", INK, "math").replace('<text ', f'<text transform="rotate(-90 20 {TOP+PH/2})" '),
    ]

    ln2x = xmap(log(2.0))
    out += [f'<line x1="{ln2x:.2f}" y1="{TOP}" x2="{ln2x:.2f}" y2="{TOP+PH}" stroke="{RED}" stroke-width="1.8" stroke-dasharray="7 6"/>', txt(260, TOP+24, "t=ln 2: off-diagonal = K/4", 15, 650, fill=RED)]
    for k in K_VALUES:
        out.append(f'<path d="{curve(k)}" fill="none" stroke="{COLORS[k]}" stroke-width="3"/>')
        value, when = peaks[k]
        out.append(f'<circle cx="{xmap(when):.2f}" cy="{ymap(value):.2f}" r="5" fill="{COLORS[k]}" stroke="{BG}" stroke-width="2"/>')

    out += [f'<rect x="92" y="108" width="156" height="100" rx="8" fill="{BG}" fill-opacity="0.96" stroke="{GRID}" stroke-width="1.5"/>']
    for i, k in enumerate(K_VALUES):
        yy = 137 + i * 29
        out += [f'<line x1="108" y1="{yy}" x2="143" y2="{yy}" stroke="{COLORS[k]}" stroke-width="3"/>', txt(154, yy+5, f"K={int(k)}", 15, 650)]

    out += [f'<line x1="850" y1="78" x2="850" y2="512" stroke="{GRID}" stroke-width="2"/>']
    cards = (
        ("对象", "A_K = [ -1  K ; 0  -2 ]", BLUE),
        ("共同渐近结论", "σ(A_K)={-1,-2}; α=-1", TEAL),
        ("改变的结构", "K controls nonnormal coupling", RED),
    )
    for i, (label, value, color) in enumerate(cards):
        y = 88 + i * 104
        out += [f'<rect x="880" y="{y}" width="280" height="78" rx="8" fill="{BG}" stroke="{color}" stroke-width="2"/>', txt(898, y+27, label, 15, 700, fill=color), txt(898, y+57, value, 15, 600, cls="math")]
    p20, t20 = peaks[20.0]
    out += [
        txt(880, 420, "K=20 finite-time peak", 16, 700, fill=RED),
        txt(880, 452, f"max_t ||exp(tA)||_2 = {p20:.3f}", 16, 650, cls="math"),
        txt(880, 480, f"at t = {t20:.3f};  norm at t=5 < 0.14", 15, 650),
        txt(880, 518, "same spectrum != same transient", 16, 700, fill=RED),
        f'<line x1="60" y1="558" x2="1140" y2="558" stroke="{GRID}" stroke-width="2"/>',
        txt(600, 587, "谱横坐标控制最终衰减；有限时间最坏放大还取决于非正规几何与方向。", 17, 650, "middle"),
        '</svg>',
    ]
    return "\n".join(out)


def main() -> None:
    target = (Path(__file__).resolve().parents[2] / "_assets" / "plots" / "matrix-functions" / "plot-matrix-exponential-transient-v2.svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build(), encoding="utf-8")
    print(target)
    for k in K_VALUES:
        value, when = peak(k)
        print(f"K={k:.0f}, peak={value:.6f}, time={when:.6f}, norm_t5={spectral_norm(5.0, k):.6f}")


if __name__ == "__main__":
    main()
