#!/usr/bin/env python3
"""Generate a deterministic SVG for Hessians, curvature, and HVPs.

Panel A: the second derivative as a bilinear form and a Hessian matrix.
Panel B: positive/negative directional curvature and spectral axes.
Panel C: matrix-free HVP and exact Hessian versus GGN structure.
Only the Python standard library is required.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


WIDTH = 1380
HEIGHT = 590
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


def line(x1, y1, x2, y2, color=GRID, width=1.5, dash=None, marker=None, opacity=1.0):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"'
        f'{dash_attr}{marker_attr}/>'
    )


def rect(x, y, w, h, fill="#ffffff", stroke=GRID, radius=10, width=1.5):
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def circle(x, y, r, fill, stroke="#ffffff", width=1.2):
    return (
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}"/>'
    )


def ellipse(x, y, rx, ry, stroke, width=1.7, dash=None, fill="none", opacity=1.0):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{dash_attr}/>'
    )


def path(points, stroke, width=1.7, fill="none", dash=None, marker=None):
    d = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y) in enumerate(points))
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{dash_attr}{marker_attr}/>'


def defs():
    out = ["<defs>"]
    for name, color in (("blue", BLUE), ("purple", PURPLE), ("orange", ORANGE), ("green", GREEN), ("red", RED)):
        out.append(
            f'<marker id="arrow-{name}" markerWidth="8" markerHeight="8" '
            'refX="7" refY="4" orient="auto">'
            f'<path d="M0,0 L8,4 L0,8 z" fill="{color}"/></marker>'
        )
    out.append("</defs>")
    return "".join(out)


def matrix(out, x, y):
    values = [["4", "1"], ["1", "2"]]
    colors = [["#dbeafe", "#f3e8ff"], ["#f3e8ff", "#dcfce7"]]
    for i in range(2):
        for j in range(2):
            out.append(rect(x + 58 * j, y + 48 * i, 58, 48, colors[i][j], GRID, 0, 1.0))
            out.append(text(x + 29 + 58 * j, y + 31 + 48 * i, values[i][j], 15, 700, "middle"))


def saddle_curve(cx, cy, scale, branch=1):
    pts = []
    for k in range(-35, 36):
        x = k / 35 * scale
        if branch > 0:
            y = 0.012 * x * x - 22
        else:
            y = -0.012 * x * x + 22
        pts.append((cx + x, cy - y))
    return pts


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Hessian、二阶微分、方向曲率与矩阵自由 HVP</title>',
        '<desc id="desc">三个面板展示二阶导数的双线性类型、Hessian 的特征方向曲率，以及无需形成完整 Hessian 的 HVP 和 GGN 作用链。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        defs(),
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A: type and representation.
    x0 = 34
    out.append(text(x0, 38, "A  二阶导数的本体是双线性型", 19, 700))
    out.append(text(x0, 64, "先接收两个方向，再得到一个标量", 12, fill=MUTED))
    out.append(rect(x0 + 8, 104, 114, 72, "#eff6ff", BLUE, 12, 2))
    out.append(text(x0 + 65, 134, "方向 u", 13, 700, "middle", BLUE))
    out.append(text(x0 + 65, 157, "u ∈ Rⁿ", 13, 650, "middle"))
    out.append(rect(x0 + 8, 203, 114, 72, "#f5f3ff", PURPLE, 12, 2))
    out.append(text(x0 + 65, 233, "方向 v", 13, 700, "middle", PURPLE))
    out.append(text(x0 + 65, 256, "v ∈ Rⁿ", 13, 650, "middle"))
    out.append(line(x0 + 128, 140, x0 + 205, 169, BLUE, 2.7, marker="arrow-blue"))
    out.append(line(x0 + 128, 239, x0 + 205, 199, PURPLE, 2.7, marker="arrow-purple"))
    out.append(rect(x0 + 210, 137, 153, 102, "#ffffff", INK, 14, 2))
    out.append(text(x0 + 287, 172, "D²f(x)[u,v]", 17, 700, "middle"))
    out.append(text(x0 + 287, 202, "= uᵀHv ∈ R", 14, 700, "middle", ORANGE))
    out.append(text(x0 + 287, 224, "对 u、v 分别线性", 11, 500, "middle", MUTED))

    out.append(text(x0 + 14, 322, "选定欧氏坐标后：", 12, 700))
    matrix(out, x0 + 102, 344)
    out.append(text(x0 + 73, 402, "H =", 17, 700, "middle"))
    out.append(text(x0 + 160, 463, "H = Hᵀ", 14, 700, "middle", GREEN))
    out.append(text(x0 + 160, 487, "Hᵢⱼ = ∂ᵢ∂ⱼ f", 12, 600, "middle", MUTED))

    # Panel B: spectral directional curvature.
    x1 = 445
    out.append(text(x1, 38, "B  二次局部模型把曲率分到特征方向", 19, 700))
    out.append(text(x1, 64, "mₓ(h)=f(x)+gᵀh+½hᵀHh", 12, fill=MUTED))
    cx, cy = x1 + 207, 237
    for rx, ry, alpha in ((150, 72, 0.45), (115, 55, 0.55), (78, 37, 0.7), (42, 20, 0.9)):
        out.append(ellipse(cx, cy, rx, ry, BLUE, 1.7, opacity=alpha))
    out.append(line(cx - 168, cy, cx + 170, cy, GRID, 1.2))
    out.append(line(cx, cy + 96, cx, cy - 98, GRID, 1.2))
    out.append(circle(cx, cy, 5, INK))
    out.append(line(cx, cy, cx + 144, cy, BLUE, 3, marker="arrow-blue"))
    out.append(text(cx + 145, cy - 12, "q₁", 13, 700, "middle", BLUE))
    out.append(text(cx + 103, cy + 24, "λ₁ 小：平缓", 11, 650, "middle", BLUE))
    out.append(line(cx, cy, cx, cy - 87, RED, 3, marker="arrow-red"))
    out.append(text(cx + 16, cy - 86, "q₂", 13, 700, fill=RED))
    out.append(text(cx + 75, cy - 58, "λ₂ 大：陡峭", 11, 650, "middle", RED))
    out.append(text(cx, cy + 126, "hᵀHh = Σᵢ λᵢ zᵢ²", 15, 700, "middle"))

    out.append(rect(x1 + 16, 396, 391, 102, "#ffffff", "#cbd5e1", 10, 1.3))
    out.append(text(x1 + 35, 425, "λmin > 0：局部碗形 / 驻点严格极小", 12, 700, fill=GREEN))
    out.append(text(x1 + 35, 451, "λmin < 0 < λmax：存在负曲率 / 鞍形", 12, 700, fill=RED))
    out.append(text(x1 + 35, 477, "有 λ = 0：二阶判别可能不充分", 12, 700, fill=ORANGE))

    # Panel C: HVP and GGN chain.
    x2 = 902
    out.append(text(x2, 38, "C  大模型只调用曲率算子，不形成整张表", 19, 700))
    out.append(text(x2, 64, "H 有 n² 个坐标；HVP 只返回 n 个坐标", 12, fill=MUTED))

    out.append(circle(x2 + 38, 141, 26, BLUE))
    out.append(text(x2 + 38, 147, "v", 17, 700, "middle", "#ffffff"))
    out.append(line(x2 + 69, 141, x2 + 157, 141, BLUE, 3, marker="arrow-blue"))
    out.append(rect(x2 + 162, 104, 142, 74, "#ffffff", INK, 12, 2))
    out.append(text(x2 + 233, 132, "JVP of grad", 14, 700, "middle"))
    out.append(text(x2 + 233, 157, "D(∇f)(x)[v]", 12, 600, "middle", MUTED))
    out.append(line(x2 + 309, 141, x2 + 393, 141, GREEN, 3, marker="arrow-green"))
    out.append(circle(x2 + 424, 141, 31, GREEN))
    out.append(text(x2 + 424, 147, "Hv", 15, 700, "middle", "#ffffff"))

    out.append(rect(x2 + 12, 214, 438, 78, "#fff7ed", ORANGE, 10, 1.5))
    out.append(text(x2 + 231, 241, "精确 Hessian 作用：可能含负曲率", 13, 700, "middle", RED))
    out.append(text(x2 + 231, 267, "Hv = JᵀHℓJv + Σᵢ gᵢ Hᵢv", 14, 700, "middle"))

    out.append(text(x2 + 12, 329, "GGN 的矩阵自由三段作用", 13, 700))
    centers = [x2 + 50, x2 + 222, x2 + 397]
    labels = [("JVP", "a = Jv", BLUE), ("输出曲率", "b = Hℓa", ORANGE), ("VJP", "Jᵀb", PURPLE)]
    for cx2, (top, bottom, color) in zip(centers, labels):
        out.append(rect(cx2 - 56, 352, 112, 70, "#ffffff", color, 10, 1.8))
        out.append(text(cx2, 379, top, 13, 700, "middle", color))
        out.append(text(cx2, 402, bottom, 12, 650, "middle"))
    out.append(line(centers[0] + 59, 387, centers[1] - 61, 387, BLUE, 2.5, marker="arrow-blue"))
    out.append(line(centers[1] + 59, 387, centers[2] - 61, 387, PURPLE, 2.5, marker="arrow-purple"))
    out.append(rect(x2 + 12, 452, 438, 48, "#ecfdf5", GREEN, 10, 1.4))
    out.append(text(x2 + 231, 482, "若 Hℓ ⪰ 0，则 GGN = JᵀHℓJ ⪰ 0", 13, 700, "middle", GREEN))

    out.append(text(WIDTH / 2, 550, "二阶本体：D²f[u,v]  ·  方向曲率：vᵀHv  ·  矩阵自由作用：Hv = D(∇f)[v]", 14, 700, "middle"))
    out.append(text(WIDTH / 2, 576, "精确 Hessian 保留模型二阶项与负曲率；GN / GGN / Fisher 是有条件、有结构、目标不同的替代曲率", 11, 550, "middle", MUTED))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    root = Path(__file__).resolve().parents[2]
    target = root / "_assets" / "figures" / "hessian-curvature-hvp" / "fig-hessian-curvature-hvp-v2.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_svg(), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
