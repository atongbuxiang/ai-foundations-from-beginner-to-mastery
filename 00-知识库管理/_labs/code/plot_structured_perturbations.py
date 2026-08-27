#!/usr/bin/env python3
"""Create the deterministic SVG for structured matrix perturbations.

Panel A shows exact Frobenius projections of a scalar functional's gradient.
Panel B distinguishes a tangent step from a finite feasible retraction.
Panel C plots the exact restricted condition numbers ||P_S G||_F.
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
BG = "#fffefb"
INK = "#172033"
MUTED = "#5d6978"
GRID = "#d9e0e8"
BLUE = "#2563eb"
PURPLE = "#0f766e"
PINK = "#64748b"
ORANGE = "#b7791f"
GREEN = "#0f766e"


def normalize(x):
    nrm = math.sqrt(sum(v * v for v in x))
    return [v / nrm for v in x]


def outer(u, v):
    return [[a * b for b in v] for a in u]


def frobenius(a):
    return math.sqrt(sum(x * x for row in a for x in row))


def symmetric_projection(a):
    n = len(a)
    return [[0.5 * (a[i][j] + a[j][i]) for j in range(n)] for i in range(n)]


def diagonal_projection(a):
    n = len(a)
    return [[a[i][j] if i == j else 0.0 for j in range(n)] for i in range(n)]


def band_projection(a, bandwidth=1):
    n = len(a)
    return [
        [a[i][j] if abs(i - j) <= bandwidth else 0.0 for j in range(n)]
        for i in range(n)
    ]


def toeplitz_projection(a):
    m, n = len(a), len(a[0])
    out = [[0.0 for _ in range(n)] for _ in range(m)]
    for k in range(-(m - 1), n):
        values = [a[i][j] for i in range(m) for j in range(n) if j - i == k]
        mean = sum(values) / len(values)
        for i in range(m):
            j = i + k
            if 0 <= j < n:
                out[i][j] = mean
    return out


def esc(value):
    return html.escape(str(value))


def text(x, y, value, size=14, weight=400, anchor="start", fill=INK):
    size = max(size, 18)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        f"{esc(value)}</text>"
    )


def lerp_color(value, limit):
    t = max(-1.0, min(1.0, value / limit))
    if t >= 0:
        a, b = (255, 255, 255), (183, 121, 31)
    else:
        t = -t
        a, b = (255, 255, 255), (37, 99, 235)
    rgb = tuple(round(a[i] + t * (b[i] - a[i])) for i in range(3))
    return "#%02x%02x%02x" % rgb


def heatmap(matrix, x, y, label, limit):
    n = len(matrix)
    cell = 21
    parts = [text(x + n * cell / 2, y - 11, label, 12, 600, "middle")]
    for i in range(n):
        for j in range(n):
            value = matrix[i][j]
            parts.append(
                f'<rect x="{x + j * cell:.1f}" y="{y + i * cell:.1f}" '
                f'width="{cell}" height="{cell}" fill="{lerp_color(value, limit)}" '
                'stroke="#ffffff" stroke-width="1"/>'
            )
    parts.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{n * cell}" height="{n * cell}" '
        'fill="none" stroke="#aeb8c5" stroke-width="1"/>'
    )
    return parts


def arrow(x1, y1, x2, y2, color, width=2.4, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#arrow-{color[1:]})"'
        f"{dash_attr}/>"
    )


def build_svg():
    u = normalize([1.0, 2.0, -1.0, 0.5])
    v = normalize([-1.0, 0.5, 2.0, 1.5])
    gradient = outer(u, v)
    projections = {
        "无结构": gradient,
        "对称": symmetric_projection(gradient),
        "带宽 1": band_projection(gradient),
        "Toeplitz": toeplitz_projection(gradient),
        "对角": diagonal_projection(gradient),
    }
    condition = {name: frobenius(value) for name, value in projections.items()}
    assert abs(condition["无结构"] - 1.0) < 1e-12

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" '
        f'viewBox="0 0 {OUTPUT_WIDTH} {OUTPUT_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">结构化扰动、切空间与受限条件数</title>',
        '<desc id="desc">左侧展示梯度的结构投影，中间区分切向步与有限回缩，右侧比较精确结构化条件数。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<rect width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({OUTPUT_SCALE:.8f})">',
        "<defs>",
    ]
    for color in (BLUE, PURPLE, PINK, ORANGE, GREEN):
        out.append(
            f'<marker id="arrow-{color[1:]}" markerWidth="9" markerHeight="9" '
            'refX="7" refY="3.5" orient="auto">'
            f'<polygon points="0 0, 7 3.5, 0 7" fill="{color}"/></marker>'
        )
    out.append("</defs>")

    # Panel A
    x0 = 48
    out.append(text(x0, 38, "A  环境梯度如何收缩到合法结构", 19, 700))
    out.append(text(x0, 63, "F(A)=uᵀAv；G=uvᵀ，结构梯度为 PₛG", 13, fill=MUTED))
    limit = max(abs(x) for row in gradient for x in row)
    out.extend(heatmap(gradient, x0 + 10, 118, "G", limit))
    out.append(arrow(x0 + 105, 160, x0 + 147, 160, PURPLE, 2.0))
    out.extend(heatmap(projections["对称"], x0 + 158, 118, "P对称G", limit))
    out.extend(heatmap(projections["Toeplitz"], x0 + 306, 118, "PToeplitzG", limit))
    out.append(
        f'<path d="M {x0 + 94} 207 Q {x0 + 226} 231, {x0 + 306} 207" '
        f'fill="none" stroke="{ORANGE}" stroke-width="2" '
        'marker-end="url(#arrow-ea580c)"/>'
    )
    out.append(text(x0 + 10, 237, "蓝：负值    白：零    红：正值", 12, fill=MUTED))
    out.append(text(x0 + 10, 270, "同一个输出导数", 13, 700))
    out.append(text(x0 + 10, 293, "允许方向越少，最坏一阶增益不增。", 13, fill=MUTED))
    out.append(text(x0 + 10, 330, "线性结构：Pₛ 是固定正交投影", 13, 600, fill=PURPLE))
    out.append(text(x0 + 10, 355, "流形结构：投影随基点 A 改变", 13, 600, fill=ORANGE))

    # Panel B
    x1 = 475
    out.append(text(x1, 38, "B  切向合法 ≠ 有限步可行", 19, 700))
    out.append(text(x1, 63, "以曲面 M 上的基点 A 为例", 13, fill=MUTED))
    out.append(
        f'<path d="M {x1 + 25} 335 C {x1 + 70} 195, {x1 + 240} 170, '
        f'{x1 + 365} 310" fill="none" stroke="{PURPLE}" stroke-width="4"/>'
    )
    ax, ay = x1 + 190, 215
    out.append(f'<circle cx="{ax}" cy="{ay}" r="6" fill="{INK}"/>')
    out.append(text(ax - 4, ay - 15, "A", 13, 700, "middle"))
    out.append(
        f'<line x1="{x1 + 82}" y1="{ay + 54}" x2="{x1 + 306}" y2="{ay - 59}" '
        'stroke="#8290a3" stroke-width="1.6" stroke-dasharray="6 5"/>'
    )
    out.append(text(x1 + 298, ay - 70, "TₐM", 13, 600, "middle", MUTED))
    tangent_x, tangent_y = ax + 92, ay - 46
    out.append(arrow(ax, ay, tangent_x, tangent_y, ORANGE, 3.0))
    out.append(text(tangent_x + 8, tangent_y - 3, "hZ（切向）", 12, 600, fill=ORANGE))
    out.append(
        f'<circle cx="{tangent_x}" cy="{tangent_y}" r="5" fill="#ffffff" '
        f'stroke="{ORANGE}" stroke-width="2"/>'
    )
    retract_x, retract_y = ax + 82, ay + 25
    out.append(
        f'<path d="M {tangent_x} {tangent_y} Q {tangent_x + 20} {ay + 2}, '
        f'{retract_x} {retract_y}" fill="none" stroke="{GREEN}" stroke-width="2.4" '
        'stroke-dasharray="5 4" marker-end="url(#arrow-059669)"/>'
    )
    out.append(
        f'<circle cx="{retract_x}" cy="{retract_y}" r="5" fill="{GREEN}" '
        'stroke="#ffffff" stroke-width="1.4"/>'
    )
    out.append(text(retract_x + 9, retract_y + 18, "Rₐ(hZ)", 12, 600, fill=GREEN))
    out.append(text(x1 + 28, 374, "直线点 A+hZ 通常离开 M；", 13, fill=MUTED))
    out.append(text(x1 + 28, 398, "retraction 把有限步送回结构集合。", 13, fill=MUTED))

    # Panel C
    x2 = 925
    out.append(text(x2, 38, "C  受限条件数的精确比较", 19, 700))
    out.append(text(x2, 63, "condₛ=||PₛG||F；同一 Frobenius 尺度", 13, fill=MUTED))
    chart_x, chart_y, chart_w, chart_h = x2 + 54, 100, 335, 285
    out.append(
        f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" '
        'fill="#ffffff" stroke="#cad2dc" stroke-width="1"/>'
    )
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        py = chart_y + chart_h * (1.0 - tick)
        out.append(
            f'<line x1="{chart_x}" y1="{py:.1f}" x2="{chart_x + chart_w}" y2="{py:.1f}" '
            'stroke="#edf0f4" stroke-width="1"/>'
        )
        out.append(text(chart_x - 9, py + 4, f"{tick:.2f}", 11, anchor="end", fill=MUTED))
    labels = list(condition)
    colors = (BLUE, PURPLE, GREEN, ORANGE, PINK)
    slot = chart_w / len(labels)
    for i, (label, color) in enumerate(zip(labels, colors)):
        value = condition[label]
        bar_w = 39
        bx = chart_x + slot * (i + 0.5) - bar_w / 2
        by = chart_y + chart_h * (1.0 - value)
        out.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" '
            f'height="{chart_y + chart_h - by:.1f}" fill="{color}" opacity="0.9"/>'
        )
        out.append(text(bx + bar_w / 2, by - 9, f"{value:.3f}", 11, 700, "middle"))
        out.append(text(bx + bar_w / 2, chart_y + chart_h + 22, label, 11, 600, "middle"))
    out.append(
        f'<text x="{chart_x - 40}" y="{chart_y + chart_h / 2}" font-size="18" '
        f'font-weight="600" text-anchor="middle" fill="{INK}" '
        f'transform="rotate(-90 {chart_x - 40} {chart_y + chart_h / 2})">一阶最坏增益</text>'
    )
    out.append(text(x2 + 54, 441, "结构最强不必最好；柱高只回答局部敏感性。", 12, fill=MUTED))
    out.append(text(WIDTH - 34, 480, "确定性解析数据；n=4", 11, anchor="end", fill=MUTED))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    knowledge_root = Path(__file__).resolve().parents[2]
    output = (
        knowledge_root
        / "_assets"
        / "figures"
        / "structured-perturbation"
        / "fig-structured-perturbation-tangent-v2.svg"
    )
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
