#!/usr/bin/env python3
"""Generate a deterministic SVG for total and Frechet derivatives.

Panel A compares a surface with its tangent-plane linearization.
Panel B visualizes pointwise directional convergence versus a uniform remainder.
Panel C decomposes the differential of matrix multiplication by perturbation order.
Only the Python standard library is required.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


WIDTH = 1380
HEIGHT = 560
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = round(HEIGHT * CANVAS_WIDTH / WIDTH)
SCALE = CANVAS_WIDTH / WIDTH
BG = "#FFFEFB"
INK = "#1F2937"
MUTED = "#64748B"
GRID = "#D7DEE8"
BLUE = "#2563eb"
PURPLE = "#0F766E"
ORANGE = "#0F766E"
GREEN = "#0F766E"
PINK = "#B7791F"
RED = "#C24135"


def esc(value):
    return html.escape(str(value))


def text(x, y, value, size=14, weight=400, anchor="start", fill=INK):
    size = 22 if size >= 19 else max(size, 18)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        f"{esc(value)}</text>"
    )


def line(x1, y1, x2, y2, color=GRID, width=1.0, dash=None, opacity=1.0, marker=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"'
        f'{dash_attr}{marker_attr}/>'
    )


def polyline(points, color, width=2.0, fill="none", opacity=1.0, dash=None):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{color}" '
        f'stroke-width="{width}" opacity="{opacity}"{dash_attr}/>'
    )


def polygon(points, fill, stroke, width=1.5, opacity=1.0):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" opacity="{opacity}"/>'
    )


def circle(x, y, radius, fill, stroke="#ffffff", stroke_width=1.2):
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def rounded_rect(x, y, w, h, fill, stroke, radius=12, width=1.5):
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def defs():
    return (
        "<defs>"
        '<marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{BLUE}"/></marker>'
        '<marker id="arrow-purple" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{PURPLE}"/></marker>'
        '<marker id="arrow-orange" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{ORANGE}"/></marker>'
        '<marker id="arrow-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{GREEN}"/></marker>'
        "</defs>"
    )


def project(x, y, z, ox, oy, scale=78):
    """Simple oblique projection used for the tangent-plane panel."""
    px = ox + scale * (x - 0.66 * y)
    py = oy - scale * (0.42 * x + 0.38 * y + z)
    return px, py


class Axes:
    def __init__(self, x, y, w, h, xmin, xmax, ymin, ymax):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def px(self, value):
        return self.x + self.w * (value - self.xmin) / (self.xmax - self.xmin)

    def py(self, value):
        return self.y + self.h * (self.ymax - value) / (self.ymax - self.ymin)

    def point(self, x, y):
        return self.px(x), self.py(y)

    def frame(self, out):
        out.append(
            f'<rect x="{self.x:.1f}" y="{self.y:.1f}" width="{self.w:.1f}" '
            f'height="{self.h:.1f}" fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
        )
        for value in (0.0, 0.25, 0.5):
            if self.ymin <= value <= self.ymax:
                out.append(line(self.x, self.py(value), self.x + self.w, self.py(value), GRID, 1.0))
        if self.ymin <= 0 <= self.ymax:
            out.append(line(self.x, self.py(0), self.x + self.w, self.py(0), INK, 1.0))


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">全微分与 Fréchet 导数的统一线性化</title>',
        '<desc id="desc">三个面板展示切平面线性化、逐方向收敛与统一余项的差异，以及矩阵乘法微分的一阶和二阶项。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        defs(),
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: surface and tangent plane.
    x0 = 38
    out.append(text(x0, 38, "A  同一个仿射模型逼近全部小扰动", 19, 700))
    out.append(text(x0, 64, "f(x,y)=0.60x²+0.35y²；a=(0.65,0.35)", 13, fill=MUTED))
    ox, oy = x0 + 214, 325
    a = (0.65, 0.35)

    def fun(x, y):
        return 0.60 * x * x + 0.35 * y * y

    fa = fun(*a)
    gx, gy = 1.20 * a[0], 0.70 * a[1]

    def plane(x, y):
        return fa + gx * (x - a[0]) + gy * (y - a[1])

    corners = [(-1.0, -0.8), (1.15, -0.8), (1.15, 1.0), (-1.0, 1.0)]
    plane_poly = [project(x, y, plane(x, y), ox, oy) for x, y in corners]
    out.append(polygon(plane_poly, "#dbeafe", BLUE, 1.5, 0.62))

    for j in range(9):
        y = -0.8 + 1.8 * j / 8
        pts = [project(-1.0 + 2.15 * i / 55, y, fun(-1.0 + 2.15 * i / 55, y), ox, oy) for i in range(56)]
        out.append(polyline(pts, PURPLE, 1.25, opacity=0.75))
    for i in range(9):
        x = -1.0 + 2.15 * i / 8
        pts = [project(x, -0.8 + 1.8 * j / 55, fun(x, -0.8 + 1.8 * j / 55), ox, oy) for j in range(56)]
        out.append(polyline(pts, PURPLE, 1.0, opacity=0.45))

    pa = project(a[0], a[1], fa, ox, oy)
    out.append(circle(*pa, 5.5, INK))
    out.append(text(pa[0] + 8, pa[1] - 7, "(a,f(a))", 10, 700))
    h = (0.48, -0.32)
    ps = project(a[0] + h[0], a[1] + h[1], fun(a[0] + h[0], a[1] + h[1]), ox, oy)
    pp = project(a[0] + h[0], a[1] + h[1], plane(a[0] + h[0], a[1] + h[1]), ox, oy)
    out.append(circle(*ps, 4.3, PURPLE))
    out.append(circle(*pp, 4.3, BLUE))
    out.append(line(ps[0], ps[1], pp[0], pp[1], RED, 2.2, dash="4 3"))
    out.append(text(ps[0] + 7, (ps[1] + pp[1]) / 2, "r(h)", 10, 700, fill=RED))
    out.append(text(x0 + 10, 430, "F(a+h)=F(a)+DF(a)[h]+r(h)", 13, 700))
    out.append(text(x0 + 10, 455, "关键不是“误差小”，而是 ‖r(h)‖/‖h‖ → 0。", 12, fill=MUTED))
    out.append(text(x0 + 10, 480, "蓝色平面同时解释所有足够小的方向。", 12, 600, fill=BLUE))

    # Panel B: normalized remainder with a moving spike.
    x1 = 482
    out.append(text(x1, 38, "B  每个固定方向成立，不等于方向上一致", 19, 700))
    out.append(text(x1, 64, "固定方向皆趋零，但 sup_θ 不趋零", 12, fill=MUTED))
    ax = Axes(x1 + 28, 104, 368, 280, -0.30, 0.30, -0.54, 0.54)
    ax.frame(out)
    colors = [ORANGE, PURPLE, BLUE, GREEN]
    radii = [0.82, 0.55, 0.36, 0.23]
    for radius, color in zip(radii, colors):
        pts = []
        for i in range(601):
            theta = -0.30 + 0.60 * i / 600
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            den = x**12 + y * y
            value = x**6 * y / den if den else 0.0
            pts.append(ax.point(theta, value))
        out.append(polyline(pts, color, 2.0, opacity=0.9))
    out.append(text(ax.x + 10, ax.y + 28, "q_r(θ)", 11, 700))
    out.append(text(ax.x + ax.w - 3, ax.y + ax.h + 22, "θ", 11, 700, "end"))
    out.append(text(ax.x - 6, ax.py(0.5) + 4, "1/2", 10, 600, "end", RED))
    out.append(line(ax.x, ax.py(0.5), ax.x + ax.w, ax.py(0.5), RED, 1.1, dash="5 4", opacity=0.55))
    for idx, (radius, color) in enumerate(zip(radii, colors)):
        out.append(text(x1 + 44 + idx * 83, 410, f"r={radius:.2f}", 10, 700, fill=color))
    out.append(text(x1 + 10, 443, "固定 θ 时 q_r(θ)→0；峰值位置却随 r 向 θ=0 移动。", 12, 600))
    out.append(text(x1 + 10, 468, "sup_θ |q_r(θ)|=1/2 不下降，因此没有统一 o(r)。", 12, 700, fill=RED))
    out.append(text(x1 + 10, 493, "Hadamard/Fréchet 会追踪“方向也在变化”的序列。", 12, fill=MUTED))

    # Panel C: matrix multiplication differential.
    x2 = 927
    out.append(text(x2, 38, "C  矩阵乘法：按扰动次数分层", 19, 700))
    out.append(text(x2, 64, "M(A,B)=AB；按 E、F 的次数分解", 12, fill=MUTED))
    out.append(rounded_rect(x2 + 12, 108, 112, 54, "#ffffff", INK))
    out.append(text(x2 + 68, 141, "(A+E)", 15, 700, "middle"))
    out.append(text(x2 + 137, 141, "×", 18, 700, "middle"))
    out.append(rounded_rect(x2 + 151, 108, 112, 54, "#ffffff", INK))
    out.append(text(x2 + 207, 141, "(B+F)", 15, 700, "middle"))
    out.append(line(x2 + 275, 135, x2 + 323, 135, BLUE, 2.4, marker="arrow-blue"))
    out.append(rounded_rect(x2 + 326, 108, 84, 54, "#eef2ff", PURPLE))
    out.append(text(x2 + 368, 141, "输出", 14, 700, "middle", PURPLE))

    rows = [
        ("0 次", "AB", "原值", INK, "#ffffff"),
        ("1 次", "EB + AF", "DM(A,B)[E,F]", BLUE, "#eff6ff"),
        ("2 次", "EF", "余项 r(E,F)", RED, "#fef2f2"),
    ]
    y0 = 202
    for i, (order, formula, meaning, color, fill) in enumerate(rows):
        yy = y0 + i * 76
        out.append(rounded_rect(x2 + 20, yy, 76, 48, fill, color, 9))
        out.append(text(x2 + 58, yy + 30, order, 12, 700, "middle", color))
        out.append(line(x2 + 104, yy + 24, x2 + 137, yy + 24, color, 2.0, marker="arrow-blue" if i == 1 else None))
        out.append(rounded_rect(x2 + 143, yy, 110, 48, fill, color, 9))
        out.append(text(x2 + 198, yy + 30, formula, 14, 700, "middle", color))
        out.append(text(x2 + 270, yy + 20, meaning, 11, 700, fill=color))
        if i == 1:
            out.append(text(x2 + 270, yy + 39, "对 (E,F) 整体线性", 10, fill=MUTED))
        if i == 2:
            out.append(text(x2 + 270, yy + 39, "‖EF‖/‖(E,F)‖→0", 10, fill=MUTED))

    out.append(text(x2 + 10, 447, "A∈Rᵐˣⁿ, B∈Rⁿˣᵖ, E/F 与 A/B 同形状。", 12, 600))
    out.append(text(x2 + 10, 472, "导数输出在 Rᵐˣᵖ；它不是“对矩阵除法”。", 12, 700, fill=PURPLE))
    out.append(text(x2 + 10, 497, "同一规则正是计算图中 matmul 节点的 JVP。", 12, fill=MUTED))

    out.append(text(WIDTH / 2, 540, "统一线性化 = 一个有界线性算子 + 相对输入尺度可忽略的余项", 13, 700, "middle", INK))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    target = (
        Path(__file__).resolve().parents[2]
        / "_assets"
        / "figures"
        / "frechet-derivative"
        / "fig-frechet-uniform-linearization-v2.svg"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_svg(), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
