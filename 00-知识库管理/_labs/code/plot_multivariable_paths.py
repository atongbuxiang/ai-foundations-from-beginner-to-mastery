#!/usr/bin/env python3
"""Generate a deterministic SVG for multivariable paths and directional derivatives.

Panel A shows coordinate and arbitrary directions on level sets.
Panel B shows why all fixed straight paths can miss a curved-path failure.
Panel C visualizes a vector-valued line slice and its JVP tangent.
No third-party packages are required.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


WIDTH = 1380
HEIGHT = 540
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


def circle(x, y, radius, color, stroke="#ffffff", stroke_width=1.2):
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


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

    def frame(self, out, x_label="x", y_label="y"):
        out.append(
            f'<rect x="{self.x:.1f}" y="{self.y:.1f}" width="{self.w:.1f}" '
            f'height="{self.h:.1f}" fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
        )
        if self.ymin <= 0 <= self.ymax:
            out.append(line(self.x, self.py(0), self.x + self.w, self.py(0), INK, 1.0))
        if self.xmin <= 0 <= self.xmax:
            out.append(line(self.px(0), self.y, self.px(0), self.y + self.h, INK, 1.0))
        out.append(text(self.x + self.w, self.y + self.h + 24, x_label, 12, 600, "end"))
        out.append(text(self.x - 8, self.y + 12, y_label, 12, 600, "end"))


def arrow_defs():
    return (
        "<defs>"
        '<marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{BLUE}"/></marker>'
        '<marker id="arrow-orange" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{ORANGE}"/></marker>'
        '<marker id="arrow-purple" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{PURPLE}"/></marker>'
        "</defs>"
    )


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">多元函数的等高线、路径反例与 JVP</title>',
        '<desc id="desc">三个面板分别展示坐标方向和一般方向、直线路径无法发现的弯曲路径极限失败，以及向量函数输入方向映射为输出切向量。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        arrow_defs(),
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: level sets and directions.
    x0 = 45
    out.append(text(x0, 38, "A  坐标偏导只是少数方向切片", 19, 700))
    out.append(text(x0, 63, "f(x,y)=x²+2y²；等高线上的同值与不同方向", 13, fill=MUTED))
    ax = Axes(x0 + 45, 100, 330, 285, -1.7, 1.7, -1.35, 1.35)
    ax.frame(out)
    for c, color, opacity in [(0.25, GRID, 1.0), (0.7, GREEN, 0.72), (1.4, BLUE, 0.55), (2.2, PURPLE, 0.42)]:
        pts = []
        for i in range(241):
            theta = 2 * math.pi * i / 240
            pts.append(ax.point(math.sqrt(c) * math.cos(theta), math.sqrt(c / 2) * math.sin(theta)))
        out.append(polyline(pts, color, 1.8, opacity=opacity))
    a = (0.45, -0.32)
    pa = ax.point(*a)
    out.append(circle(*pa, 5.2, INK))
    out.append(text(pa[0] + 7, pa[1] + 19, "a", 11, 700))
    ex = ax.point(a[0] + 0.72, a[1])
    ey = ax.point(a[0], a[1] + 0.66)
    vv = ax.point(a[0] - 0.58, a[1] + 0.58)
    out.append(line(*pa, *ex, ORANGE, 2.4, marker="arrow-orange"))
    out.append(line(*pa, *ey, BLUE, 2.4, marker="arrow-blue"))
    out.append(line(*pa, *vv, PURPLE, 2.7, marker="arrow-purple"))
    out.append(text(ex[0] - 4, ex[1] - 8, "e₁：∂₁f", 10, 700, "end", ORANGE))
    out.append(text(ey[0] + 7, ey[1] + 3, "e₂：∂₂f", 10, 700, fill=BLUE))
    out.append(text(vv[0] - 3, vv[1] - 8, "v：Dᵥf", 10, 700, "end", PURPLE))
    out.append(text(x0 + 6, 425, "偏导只看坐标基 e₁、e₂；方向导数可看任意固定 v。", 13, 600))
    out.append(text(x0 + 6, 451, "等高线描述同值集合，不等于函数在该点已经可微。", 12, fill=MUTED))

    # Panel B: all lines pass, curved path fails.
    x1 = 492
    out.append(text(x1, 38, "B  路径陷阱：全部直线通过，曲线仍失败", 19, 700))
    out.append(text(x1, 63, "g=x⁶y/(x¹²+y²)；原点补 0", 13, fill=MUTED))
    bx = Axes(x1 + 45, 100, 330, 285, -1.05, 1.05, -0.25, 1.12)
    bx.frame(out)
    for slope in (-0.7, -0.28, 0.25, 0.72):
        extent = min(1.0, 0.22 / abs(slope))
        out.append(
            polyline(
                [bx.point(-extent, -slope * extent), bx.point(extent, slope * extent)],
                GRID,
                1.4,
                dash="6 5",
            )
        )
    curve = [bx.point(-1 + 2 * i / 240, (-1 + 2 * i / 240) ** 6) for i in range(241)]
    out.append(polyline(curve, PINK, 3.0))
    origin = bx.point(0, 0)
    out.append(circle(*origin, 5.0, INK))
    out.append(text(bx.px(-0.95), bx.py(0.96), "弯曲路径 y=x⁶", 11, 700, fill=PINK))
    out.append(text(bx.px(-0.95), bx.py(0.82), "沿此路径 g=1/2", 10, 600, fill=PINK))
    out.append(text(bx.px(0.30), bx.py(-0.11), "任意固定直线：g→0", 10, 700, fill=MUTED))
    out.append(text(x1 + 6, 425, "直线固定方向；弯曲路径可让方向随尺度改变。", 13, 600))
    out.append(text(x1 + 6, 451, "路径可反证极限；有限或固定方向检查不能证明极限。", 12, fill=MUTED))

    # Panel C: vector-valued slice and JVP.
    x2 = 938
    out.append(text(x2, 38, "C  向量方向导数：输入切向量 → 输出切向量", 19, 700))
    out.append(text(x2, 63, "F(x,y)=(x²−y, x+y²)；t↦F(a+tv)", 13, fill=MUTED))
    # Two compact planes inside panel.
    left = Axes(x2 + 20, 130, 145, 210, -0.5, 1.3, -0.55, 1.25)
    right = Axes(x2 + 226, 130, 145, 210, -0.9, 1.0, -0.55, 1.35)
    left.frame(out, "x₁", "x₂")
    right.frame(out, "F₁", "F₂")
    a = (0.2, 0.1)
    v = (0.8, 0.5)
    pin = left.point(*a)
    pin2 = left.point(a[0] + 0.7 * v[0], a[1] + 0.7 * v[1])
    out.append(circle(*pin, 4.8, INK))
    out.append(line(*pin, *pin2, BLUE, 2.7, marker="arrow-blue"))
    out.append(text(pin2[0] - 2, pin2[1] - 9, "v", 11, 700, "end", BLUE))
    out.append(text(pin[0] + 6, pin[1] + 16, "a", 10, 700))

    def f_map(x, y):
        return x * x - y, x + y * y

    out_curve = []
    for i in range(241):
        t = -0.68 + 1.36 * i / 240
        xx, yy = a[0] + t * v[0], a[1] + t * v[1]
        out_curve.append(right.point(*f_map(xx, yy)))
    out.append(polyline(out_curve, GREEN, 2.8))
    fa = f_map(*a)
    pout = right.point(*fa)
    # Jv = (2*x*v1-v2, v1+2*y*v2) at a.
    jv = (2 * a[0] * v[0] - v[1], v[0] + 2 * a[1] * v[1])
    scale = 0.48
    pout2 = right.point(fa[0] + scale * jv[0], fa[1] + scale * jv[1])
    out.append(circle(*pout, 5.0, INK))
    out.append(line(*pout, *pout2, PURPLE, 2.8, marker="arrow-purple"))
    out.append(text(pout2[0] + 4, pout2[1] - 6, "J_F(a)v", 10, 700, fill=PURPLE))
    out.append(text(pout[0] + 6, pout[1] + 17, "F(a)", 10, 700))
    out.append(line(x2 + 187, 224, x2 + 215, 224, ORANGE, 2.2, marker="arrow-orange"))
    out.append(text(x2 + 201, 208, "F", 11, 700, "middle", ORANGE))
    out.append(text(x2 + 6, 390, "切片 φ(t)=F(a+tv) 把高维映射变成一元向量曲线。", 13, 600))
    out.append(text(x2 + 6, 416, "可微时 φ′(0)=J_F(a)v；输出形状与 F 相同。", 12, fill=MUTED))
    out.append(text(x2 + 6, 451, "JVP 可沿程序传播，不必显式物化整个 Jacobian。", 12, fill=MUTED))

    out.append(text(WIDTH - 34, 517, "确定性解析数据；生成日期 2026-08-17", 11, anchor="end", fill=MUTED))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    knowledge_root = Path(__file__).resolve().parents[2]
    output = (
        knowledge_root
        / "_assets"
        / "figures"
        / "multivariable-paths"
        / "fig-multivariable-paths-directions-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
