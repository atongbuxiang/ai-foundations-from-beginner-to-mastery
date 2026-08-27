#!/usr/bin/env python3
"""Generate a deterministic SVG for derivatives and mean value theorems.

Panel A: secant slopes of x^2 converge to the tangent slope at a = 1.
Panel B: the mean-value point for x^3 on [0, 2].
Panel C: ReLU's unequal one-sided derivatives versus a smooth Softplus.
No third-party packages are required.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


WIDTH = 1380
HEIGHT = 520
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

    def frame(self, out, x_label="x", y_label="f(x)"):
        out.append(
            f'<rect x="{self.x:.1f}" y="{self.y:.1f}" width="{self.w:.1f}" '
            f'height="{self.h:.1f}" fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
        )
        if self.ymin <= 0 <= self.ymax:
            out.append(line(self.x, self.py(0), self.x + self.w, self.py(0), INK, 1.1))
        if self.xmin <= 0 <= self.xmax:
            out.append(line(self.px(0), self.y, self.px(0), self.y + self.h, INK, 1.1))
        out.append(text(self.x + self.w, self.y + self.h + 24, x_label, 12, 600, "end"))
        out.append(
            f'<text x="{self.x - 32:.1f}" y="{self.y + self.h / 2:.1f}" '
            f'font-size="18" font-weight="600" text-anchor="middle" fill="{INK}" '
            f'transform="rotate(-90 {self.x - 32:.1f} {self.y + self.h / 2:.1f})">'
            f"{esc(y_label)}</text>"
        )

    def curve(self, fn, start=None, stop=None, samples=240):
        left = self.xmin if start is None else start
        right = self.xmax if stop is None else stop
        return [
            self.point(
                left + (right - left) * i / samples,
                fn(left + (right - left) * i / samples),
            )
            for i in range(samples + 1)
        ]


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">导数的局部极限、中值定理与 ReLU 光滑化</title>',
        '<desc id="desc">三个面板分别展示割线趋近切线、中值定理的平行切线，以及 ReLU 左右导数和 Softplus 平滑近似。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: secants converge to tangent.
    x0 = 45
    out.append(text(x0, 38, "A  割线极限：差商 → 导数", 19, 700))
    out.append(text(x0, 63, "f(x)=x²，a=1；割线斜率 2+h → 2", 13, fill=MUTED))
    ax = Axes(x0 + 45, 100, 330, 270, 0.0, 2.2, 0.0, 4.8)
    ax.frame(out)
    out.append(polyline(ax.curve(lambda x: x * x), BLUE, 2.8))
    a = 1.0
    pa = ax.point(a, a * a)
    out.append(circle(*pa, 4.7, INK))
    out.append(text(pa[0] - 5, pa[1] - 12, "a=1", 11, 700, "end"))
    # Tangent y = 2x - 1.
    tangent = [ax.point(0.35, -0.3), ax.point(2.2, 3.4)]
    out.append(polyline(tangent, PURPLE, 2.3, dash="8 5"))
    out.append(text(ax.px(1.75), ax.py(2.6), "切线 m=2", 11, 700, fill=PURPLE))
    secants = [(0.9, ORANGE), (0.45, GREEN), (0.2, PINK)]
    for h, color in secants:
        b = a + h
        pb = ax.point(b, b * b)
        slope = 2 + h
        x_left = 0.55
        x_right = min(2.2, b + 0.15)
        y_left = a * a + slope * (x_left - a)
        y_right = a * a + slope * (x_right - a)
        out.append(polyline([ax.point(x_left, y_left), ax.point(x_right, y_right)], color, 1.7))
        out.append(circle(*pb, 3.7, color))
        out.append(text(pb[0] + 3, pb[1] - 8, f"h={h:g}", 10, 700, fill=color))
    out.append(text(x0 + 6, 408, "差商在 h≠0 时定义；导数是 h→0 的有限极限。", 13, 600))
    out.append(text(x0 + 6, 433, "局部模型：f(1+h)=1+2h+o(|h|)。", 12, fill=MUTED))

    # Panel B: MVT for x^3.
    x1 = 492
    out.append(text(x1, 38, "B  中值定理：局部斜率 = 整体斜率", 19, 700))
    out.append(text(x1, 63, "f(x)=x³ on [0,2]；割线 m=4", 13, fill=MUTED))
    bx = Axes(x1 + 45, 100, 330, 270, 0.0, 2.05, 0.0, 8.4)
    bx.frame(out)
    out.append(polyline(bx.curve(lambda x: x**3, 0.0, 2.02), BLUE, 2.8))
    # Secant y=4x.
    out.append(polyline([bx.point(0, 0), bx.point(2, 8)], ORANGE, 2.2, dash="8 5"))
    out.append(circle(*bx.point(0, 0), 4.5, INK))
    out.append(circle(*bx.point(2, 8), 4.5, INK))
    c = 2 / math.sqrt(3)
    yc = c**3
    # Tangent slope 4.
    left = max(0, c - 0.63)
    right = min(2.05, c + 0.73)
    out.append(
        polyline(
            [bx.point(left, yc + 4 * (left - c)), bx.point(right, yc + 4 * (right - c))],
            PURPLE,
            2.5,
        )
    )
    pc = bx.point(c, yc)
    out.append(circle(*pc, 5.0, PURPLE))
    out.append(line(pc[0], pc[1], pc[0], bx.py(0), PURPLE, 1.3, "5 4"))
    out.append(text(pc[0] + 7, pc[1] - 12, "f′(c)=4", 11, 700, fill=PURPLE))
    out.append(text(pc[0], bx.py(0) + 19, "c=2/√3", 10, 700, "middle", PURPLE))
    out.append(text(x1 + 6, 408, "连续 [0,2] + 可微 (0,2) ⇒ 至少一个 c。", 13, 600))
    out.append(text(x1 + 6, 433, "存在性不等于 c 是中点，也不自动保证唯一。", 12, fill=MUTED))

    # Panel C: ReLU and Softplus.
    x2 = 938
    out.append(text(x2, 38, "C  AI 边界：ReLU 折点与光滑近似", 19, 700))
    out.append(text(x2, 63, "ReLU 在 0 左右导数为 0/1；Softplus 可微", 13, fill=MUTED))
    cx = Axes(x2 + 45, 100, 330, 270, -2.2, 2.2, -0.3, 2.35)
    cx.frame(out)
    relu = cx.curve(lambda x: max(x, 0.0), -2.2, 2.2)
    beta = 4.0
    softplus = cx.curve(lambda x: math.log1p(math.exp(beta * x)) / beta, -2.2, 2.2)
    out.append(polyline(relu, INK, 2.8))
    out.append(polyline(softplus, GREEN, 2.5))
    p0 = cx.point(0, 0)
    out.append(circle(*p0, 5.0, ORANGE))
    out.append(line(cx.px(-1.35), cx.py(0), cx.px(-0.1), cx.py(0), ORANGE, 2.2))
    out.append(line(cx.px(0.1), cx.py(0.1), cx.px(1.3), cx.py(1.3), PINK, 2.2))
    out.append(text(cx.px(-1.55), cx.py(0) - 9, "左导数 0", 10, 700, fill=ORANGE))
    out.append(text(cx.px(0.7), cx.py(0.85) - 5, "右导数 1", 10, 700, fill=PINK))
    out.append(text(cx.px(-1.95), cx.py(0.3), "ReLU", 11, 700, fill=INK))
    out.append(text(cx.px(-1.95), cx.py(0.56), "Softplus β=4", 11, 700, fill=GREEN))
    out.append(text(x2 + 6, 408, "框架可在 0 返回约定值，但经典双侧导数仍不存在。", 13, 600))
    out.append(text(x2 + 6, 433, "光滑化改变函数、梯度与曲率，而不只是视觉外观。", 12, fill=MUTED))

    out.append(text(WIDTH - 34, 500, "确定性解析数据；生成日期 2026-08-16", 11, anchor="end", fill=MUTED))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    knowledge_root = Path(__file__).resolve().parents[2]
    output = (
        knowledge_root
        / "_assets"
        / "figures"
        / "derivative-mvt"
        / "fig-derivative-mvt-local-global-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
