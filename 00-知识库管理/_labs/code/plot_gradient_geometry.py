#!/usr/bin/env python3
"""Generate a deterministic SVG for gradients, metrics, and steepest directions.

Panel A shows one differential represented by two metric-dependent gradients.
Panel B compares steepest directions for l1, l2, and linfinity unit balls.
Panel C compares matrix steepest directions under Frobenius, spectral, and nuclear norms.
Only the Python standard library is required.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


WIDTH = 1380
HEIGHT = 570
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = round(HEIGHT * CANVAS_WIDTH / WIDTH)
SCALE = CANVAS_WIDTH / WIDTH
BG = "#FFFEFB"
INK = "#1F2937"
MUTED = "#64748B"
GRID = "#D7DEE8"
BLUE = "#2563eb"
PURPLE = "#0F766E"
ORANGE = "#B7791F"
GREEN = "#0F766E"
PINK = "#B7791F"
RED = "#B7791F"


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


def rounded_rect(x, y, w, h, fill, stroke, radius=10, width=1.5):
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def defs():
    parts = ["<defs>"]
    for name, color in (
        ("blue", BLUE),
        ("purple", PURPLE),
        ("orange", ORANGE),
        ("green", GREEN),
        ("red", RED),
    ):
        parts.append(
            f'<marker id="arrow-{name}" markerWidth="8" markerHeight="8" '
            'refX="7" refY="4" orient="auto">'
            f'<path d="M0,0 L8,4 L0,8 z" fill="{color}"/></marker>'
        )
    parts.append("</defs>")
    return "".join(parts)


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

    def frame(self, out, x_label="x₁", y_label="x₂"):
        out.append(
            f'<rect x="{self.x:.1f}" y="{self.y:.1f}" width="{self.w:.1f}" '
            f'height="{self.h:.1f}" fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
        )
        out.append(line(self.x, self.py(0), self.x + self.w, self.py(0), GRID, 1.0))
        out.append(line(self.px(0), self.y, self.px(0), self.y + self.h, GRID, 1.0))
        out.append(text(self.x + self.w, self.y + self.h + 20, x_label, 11, 600, "end"))
        out.append(text(self.x - 5, self.y + 12, y_label, 11, 600, "end"))


def arrow(out, axes, start, vector, color, marker, scale=1.0, width=2.8):
    p0 = axes.point(*start)
    p1 = axes.point(start[0] + scale * vector[0], start[1] + scale * vector[1])
    out.append(line(*p0, *p1, color, width, marker=marker))
    return p0, p1


def norm_ball_points(kind, radius=1.0, samples=240):
    if kind == "l2":
        return [
            (radius * math.cos(2 * math.pi * i / samples), radius * math.sin(2 * math.pi * i / samples))
            for i in range(samples + 1)
        ]
    if kind == "l1":
        return [(radius, 0), (0, radius), (-radius, 0), (0, -radius), (radius, 0)]
    if kind == "linf":
        return [
            (-radius, -radius),
            (radius, -radius),
            (radius, radius),
            (-radius, radius),
            (-radius, -radius),
        ]
    raise ValueError(kind)


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">梯度依赖度量，最陡方向依赖范数</title>',
        '<desc id="desc">三个面板展示同一微分的不同梯度表示、不同向量范数下的最陡方向，以及矩阵范数下不同的最陡更新奇异值结构。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        defs(),
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: same covector, two metric gradients.
    x0 = 38
    out.append(text(x0, 38, "A  同一个微分，不同度量给出不同梯度", 19, 700))
    out.append(text(x0, 64, "df[h]=gᵀh，g=(2,1)；M=diag(4,1)", 13, fill=MUTED))
    ax = Axes(x0 + 36, 96, 330, 290, -2.2, 2.2, -1.8, 1.8)
    ax.frame(out)
    # Level sets 2x+y=c.
    for c, opacity in ((-2.0, 0.32), (-1.0, 0.50), (0.0, 0.85), (1.0, 0.50), (2.0, 0.32)):
        pts = []
        for i in range(81):
            xx = -2.2 + 4.4 * i / 80
            yy = c - 2 * xx
            if -1.8 <= yy <= 1.8:
                pts.append(ax.point(xx, yy))
        if len(pts) >= 2:
            out.append(polyline(pts, GRID if c else INK, 1.5 if c else 2.2, opacity=opacity))
    # Euclidean and weighted unit balls.
    ellipse_e = [ax.point(math.cos(2 * math.pi * i / 180), math.sin(2 * math.pi * i / 180)) for i in range(181)]
    ellipse_m = [ax.point(0.5 * math.cos(2 * math.pi * i / 180), math.sin(2 * math.pi * i / 180)) for i in range(181)]
    out.append(polyline(ellipse_e, BLUE, 1.5, opacity=0.45, dash="5 4"))
    out.append(polyline(ellipse_m, PURPLE, 1.8, opacity=0.55, dash="5 4"))
    p0, p_e = arrow(out, ax, (0, 0), (2, 1), BLUE, "arrow-blue", scale=0.62)
    _, p_m = arrow(out, ax, (0, 0), (0.5, 1), PURPLE, "arrow-purple", scale=0.95)
    out.append(circle(*p0, 4.0, INK))
    out.append(text(p_e[0] + 5, p_e[1] - 6, "∇₂f=g", 11, 700, fill=BLUE))
    out.append(text(p_m[0] + 6, p_m[1] - 5, "∇ₘf=M⁻¹g", 11, 700, fill=PURPLE))
    out.append(text(ax.x + 7, ax.y + 20, "黑线：df[h]=0 的切方向", 10, 600))
    out.append(text(x0 + 8, 425, "欧氏：df[h]=hᵀg；加权：df[h]=hᵀM(M⁻¹g)。", 12, 600))
    out.append(text(x0 + 8, 450, "梯度箭头变了，微分对每个 h 的标量作用没有变。", 12, fill=MUTED))
    out.append(text(x0 + 8, 475, "“垂直”等几何词也必须先声明内积。", 12, 700, fill=PURPLE))

    # Panel B: three norm balls.
    x1 = 470
    out.append(text(x1, 38, "B  同一协向量，不同范数给出不同方向", 19, 700))
    out.append(text(x1, 64, "g=(1,0.55)；最小化 gᵀv，约束 ‖v‖≤1", 13, fill=MUTED))
    kinds = [
        ("l1", "ℓ₁ 球", (-1.0, 0.0), ORANGE, "稀疏坐标方向"),
        ("l2", "ℓ₂ 球", (-1 / math.sqrt(1 + 0.55**2), -0.55 / math.sqrt(1 + 0.55**2)), BLUE, "负归一化梯度"),
        ("linf", "ℓ∞ 球", (-1.0, -1.0), GREEN, "−sign(g)"),
    ]
    centers = [x1 + 73, x1 + 217, x1 + 361]
    for (kind, label, direction, color, caption), cx in zip(kinds, centers):
        cy = 237
        scale = 57
        pts = [(cx + scale * xx, cy - scale * yy) for xx, yy in norm_ball_points(kind)]
        out.append(polygon(pts, "#ffffff", color, 2.0, 0.95))
        out.append(line(cx - 70, cy, cx + 70, cy, GRID, 1.0))
        out.append(line(cx, cy - 70, cx, cy + 70, GRID, 1.0))
        end = (cx + scale * direction[0], cy - scale * direction[1])
        out.append(line(cx, cy, *end, color, 3.0, marker={"orange": "arrow-orange", "blue": "arrow-blue", "green": "arrow-green"}.get(
            "orange" if color == ORANGE else "blue" if color == BLUE else "green"
        )))
        out.append(circle(*end, 4.2, color))
        out.append(text(cx, 141, label, 13, 700, "middle", color))
        out.append(text(cx, 327, caption, 10, 700, "middle", color))
    out.append(text(x1 + 10, 375, "最大一阶下降率统一等于对偶范数 ‖g‖*。", 12, 700))
    out.append(text(x1 + 10, 402, "ℓ₁↔ℓ∞；ℓ₂↔ℓ₂。单位球的形状决定接触点。", 12, fill=MUTED))
    out.append(text(x1 + 10, 438, "负梯度只是在欧氏球上最陡；SignSGD 对应 ℓ∞ 几何。", 12, 600))
    out.append(text(x1 + 10, 465, "若最大分量并列或范数球有平面，最陡方向可能不唯一。", 12, fill=MUTED))

    # Panel C: matrix steepest directions through singular values.
    x2 = 925
    out.append(text(x2, 38, "C  矩阵范数改变最陡更新", 19, 700))
    out.append(text(x2, 64, "G=U diag(4,1)Vᵀ；比较单位更新 Δ 的奇异值", 12, fill=MUTED))
    rows = [
        ("Frobenius 球", "Δ ∝ −G", (4 / math.sqrt(17), 1 / math.sqrt(17)), BLUE, "保留相对奇异值"),
        ("谱范数球", "Δ = −UVᵀ", (1.0, 1.0), PURPLE, "全部活跃奇异方向等幅"),
        ("核范数球", "Δ = −u₁v₁ᵀ", (1.0, 0.0), ORANGE, "只取最大奇异方向"),
    ]
    y_start = 118
    for i, (label, formula, sigmas, color, note) in enumerate(rows):
        yy = y_start + i * 112
        out.append(rounded_rect(x2 + 10, yy, 420, 88, "#ffffff", color, 11))
        out.append(text(x2 + 25, yy + 25, label, 12, 700, fill=color))
        out.append(text(x2 + 25, yy + 50, formula, 13, 700))
        # singular-value bars
        bar_x = x2 + 187
        out.append(text(bar_x - 8, yy + 22, "σ₁", 9, 600, "end", MUTED))
        out.append(text(bar_x - 8, yy + 48, "σ₂", 9, 600, "end", MUTED))
        out.append(rounded_rect(bar_x, yy + 12, 145, 13, "#eef2f7", "#eef2f7", 5, 0))
        out.append(rounded_rect(bar_x, yy + 38, 145, 13, "#eef2f7", "#eef2f7", 5, 0))
        out.append(rounded_rect(bar_x, yy + 12, 145 * sigmas[0], 13, color, color, 5, 0))
        if sigmas[1] > 0:
            out.append(rounded_rect(bar_x, yy + 38, 145 * sigmas[1], 13, color, color, 5, 0))
        out.append(text(x2 + 344, yy + 25, f"{sigmas[0]:.2f}", 9, 700, fill=color))
        out.append(text(x2 + 344, yy + 51, f"{sigmas[1]:.2f}", 9, 700, fill=color))
        out.append(text(x2 + 25, yy + 75, note, 10, fill=MUTED))
    out.append(text(x2 + 12, 476, "谱范数约束的对偶是核范数；其最陡方向是极因子。", 12, 700, fill=PURPLE))
    out.append(text(x2 + 12, 501, "这解释 Muon 的几何入口，不等于已证明训练收敛。", 12, fill=MUTED))

    out.append(text(WIDTH / 2, 550, "微分决定“变化多少” · 内积决定“哪个向量代表它” · 范数决定“每单位步长谁最陡”", 13, 700, "middle"))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    target = (
        Path(__file__).resolve().parents[2]
        / "_assets"
        / "figures"
        / "gradient-geometry"
        / "fig-gradient-metric-steepest-v2.svg"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_svg(), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
