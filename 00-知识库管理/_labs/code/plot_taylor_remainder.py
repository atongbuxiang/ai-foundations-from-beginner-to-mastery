#!/usr/bin/env python3
"""Generate a deterministic SVG for Taylor approximation and error budgets.

Panel A compares exp(x) with its first three nonconstant Maclaurin models.
Panel B compares the true T2 error with a certified Lagrange upper bound.
Panel C shows the truncation/roundoff balance for a central difference.
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
ORANGE = "#C24135"
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


def line(x1, y1, x2, y2, color=GRID, width=1.0, dash=None, opacity=1.0):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"{dash_attr}/>'
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
    def __init__(self, x, y, w, h, xmin, xmax, ymin, ymax, log_x=False, log_y=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.log_x = log_x
        self.log_y = log_y

    def _tx(self, value):
        return math.log10(value) if self.log_x else value

    def _ty(self, value):
        return math.log10(value) if self.log_y else value

    def px(self, value):
        lo, hi = self._tx(self.xmin), self._tx(self.xmax)
        return self.x + self.w * (self._tx(value) - lo) / (hi - lo)

    def py(self, value):
        lo, hi = self._ty(self.ymin), self._ty(self.ymax)
        return self.y + self.h * (hi - self._ty(value)) / (hi - lo)

    def point(self, x, y):
        return self.px(x), self.py(y)

    def frame(self, out, x_label="x", y_label="f(x)"):
        out.append(
            f'<rect x="{self.x:.1f}" y="{self.y:.1f}" width="{self.w:.1f}" '
            f'height="{self.h:.1f}" fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
        )
        if not self.log_y and self.ymin <= 0 <= self.ymax:
            out.append(line(self.x, self.py(0), self.x + self.w, self.py(0), INK, 1.0))
        if not self.log_x and self.xmin <= 0 <= self.xmax:
            out.append(line(self.px(0), self.y, self.px(0), self.y + self.h, INK, 1.0))
        out.append(text(self.x + self.w, self.y + self.h + 25, x_label, 12, 600, "end"))
        out.append(
            f'<text x="{self.x - 31:.1f}" y="{self.y + self.h / 2:.1f}" '
            f'font-size="18" font-weight="600" text-anchor="middle" fill="{INK}" '
            f'transform="rotate(-90 {self.x - 31:.1f} {self.y + self.h / 2:.1f})">'
            f"{esc(y_label)}</text>"
        )

    def curve(self, fn, samples=260, geometric=False):
        points = []
        for i in range(samples + 1):
            ratio = i / samples
            if geometric:
                value = self.xmin * (self.xmax / self.xmin) ** ratio
            else:
                value = self.xmin + (self.xmax - self.xmin) * ratio
            points.append(self.point(value, fn(value)))
        return points


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Taylor 多项式、Lagrange 余项与有限差分误差平衡</title>',
        '<desc id="desc">三个面板展示指数函数的逐阶局部近似、真实误差与严格上界，以及中心差分的截断误差和舍入误差平衡。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: local Taylor models.
    x0 = 45
    out.append(text(x0, 38, "A  多项式阶数：匹配更多局部导数", 19, 700))
    out.append(text(x0, 63, "eˣ 与 T₁、T₂、T₃（中心 a=0）", 13, fill=MUTED))
    ax = Axes(x0 + 45, 100, 330, 285, -1.5, 1.5, -0.1, 4.8)
    ax.frame(out)
    out.append(polyline(ax.curve(math.exp), INK, 3.0))
    out.append(polyline(ax.curve(lambda x: 1 + x), ORANGE, 1.9, dash="7 5"))
    out.append(polyline(ax.curve(lambda x: 1 + x + x * x / 2), GREEN, 2.0))
    out.append(polyline(ax.curve(lambda x: 1 + x + x * x / 2 + x**3 / 6), BLUE, 2.2))
    p0 = ax.point(0, 1)
    out.append(circle(*p0, 4.7, PURPLE))
    out.append(text(ax.px(-1.34), ax.py(4.25), "eˣ", 11, 700, fill=INK))
    out.append(text(ax.px(0.93), ax.py(1.72), "T₁", 11, 700, fill=ORANGE))
    out.append(text(ax.px(1.18), ax.py(2.75), "T₂", 11, 700, fill=GREEN))
    out.append(text(ax.px(1.20), ax.py(3.45), "T₃", 11, 700, fill=BLUE))
    out.append(text(x0 + 6, 425, "中心处各阶导数逐级匹配；离中心越远，余项越重要。", 13, 600))
    out.append(text(x0 + 6, 451, "高阶通常扩大可信区，但不自动保证任意区间更准。", 12, fill=MUTED))

    # Panel B: actual error and certified bound for T2 on [0, 1].
    x1 = 492
    out.append(text(x1, 38, "B  余项证书：真实误差 ≤ 可计算上界", 19, 700))
    out.append(text(x1, 63, "eˣ 的 T₂；0.02≤x≤1，纵轴为对数尺度", 13, fill=MUTED))
    bx = Axes(x1 + 45, 100, 330, 285, 0.02, 1.0, 1e-7, 1.0, log_y=True)
    bx.frame(out, x_label="x", y_label="absolute error (log₁₀)")
    true_error = lambda x: math.exp(x) - (1 + x + x * x / 2)
    bound = lambda x: math.e * x**3 / 6
    out.append(polyline(bx.curve(true_error), BLUE, 2.8))
    out.append(polyline(bx.curve(bound), ORANGE, 2.3, dash="8 5"))
    for tick in (1e-6, 1e-4, 1e-2, 1.0):
        py = bx.py(tick)
        out.append(line(bx.x, py, bx.x + bx.w, py, GRID, 0.8))
        out.append(text(bx.x - 7, py + 4, f"10^{int(math.log10(tick))}", 10, 500, "end", MUTED))
    out.append(text(bx.px(0.54), bx.py(true_error(0.54)) - 10, "真实 |R₂|", 11, 700, fill=BLUE))
    out.append(text(bx.px(0.58), bx.py(bound(0.58)) - 9, "e·x³/3!", 11, 700, fill=ORANGE))
    out.append(text(x1 + 6, 425, "上界不必贴紧真实误差；它的职责是可靠覆盖。", 13, 600))
    out.append(text(x1 + 6, 451, "证书依赖整个 [0,x] 上的三阶导数界 eᵗ≤e。", 12, fill=MUTED))

    # Panel C: finite-difference error budget.
    x2 = 938
    out.append(text(x2, 38, "C  总误差：截断下降，舍入上升", 19, 700))
    out.append(text(x2, 63, "中心差分模型 E(h)=h²+u/h，u=10⁻¹²", 13, fill=MUTED))
    cx = Axes(x2 + 45, 100, 330, 285, 1e-6, 1.0, 1e-12, 2.0, log_x=True, log_y=True)
    cx.frame(out, x_label="step h (log₁₀)", y_label="error scale (log₁₀)")
    u = 1e-12
    truncation = lambda h: h * h
    roundoff = lambda h: u / h
    total = lambda h: truncation(h) + roundoff(h)
    out.append(polyline(cx.curve(truncation, geometric=True), GREEN, 2.2))
    out.append(polyline(cx.curve(roundoff, geometric=True), PINK, 2.2))
    out.append(polyline(cx.curve(total, geometric=True), PURPLE, 3.0))
    h_star = (u / 2) ** (1 / 3)
    p_star = cx.point(h_star, total(h_star))
    out.append(line(p_star[0], p_star[1], p_star[0], cx.y + cx.h, PURPLE, 1.3, "5 4"))
    out.append(circle(*p_star, 5.2, PURPLE))
    out.append(text(p_star[0] + 7, p_star[1] - 10, "最佳窗口 h∝u¹ᐟ³", 10, 700, fill=PURPLE))
    out.append(text(cx.px(3e-3), cx.py(truncation(3e-3)) - 8, "h²", 11, 700, fill=GREEN))
    out.append(text(cx.px(3e-6), cx.py(roundoff(3e-6)) - 8, "u/h", 11, 700, fill=PINK))
    out.append(text(x2 + 6, 425, "h→0 只消除解析截断误差，却会放大函数值舍入。", 13, 600))
    out.append(text(x2 + 6, 451, "图中 u 为教学尺度；double 的实际窗口约在 10⁻⁶。", 12, fill=MUTED))

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
        / "taylor-remainder"
        / "fig-taylor-remainder-error-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
