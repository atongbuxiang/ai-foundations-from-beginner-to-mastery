#!/usr/bin/env python3
"""Generate a deterministic SVG explaining Jacobians, JVPs, and VJPs.

Panel A: one derivative operator and its Jacobian coordinate matrix.
Panel B: tangent pushforward, cotangent pullback, and the adjoint test.
Panel C: column-by-column versus row-by-row Jacobian construction costs.
Only the Python standard library is required.
"""

from __future__ import annotations

import html
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
ORANGE = "#B7791F"
GREEN = "#0F766E"
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


def matrix_grid(out, x, y, rows, cols, cell_w, cell_h, values, highlights=None):
    highlights = highlights or {}
    for i in range(rows):
        for j in range(cols):
            fill = highlights.get((i, j), "#ffffff")
            out.append(rect(x + j * cell_w, y + i * cell_h, cell_w, cell_h, fill, GRID, 0, 1.0))
            value = values[i][j] if values else ""
            if value != "":
                out.append(text(x + (j + 0.5) * cell_w, y + (i + 0.67) * cell_h, value, 13, 650, "middle"))


def build_svg():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Jacobian、JVP 与 VJP 的对象、方向和成本</title>',
        '<desc id="desc">三个面板展示导数算子在坐标中成为 Jacobian，JVP 推送切向量、VJP 回拉协向量，以及完整 Jacobian 的列式和行式构造成本。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif;}</style>',
        defs(),
        f'<rect width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="{BG}"/>',
        f'<g transform="scale({SCALE:.8f})">',
    ]

    # Panel A.
    x0 = 35
    out.append(text(x0, 38, "A  一个导数算子，三种观察方式", 19, 700))
    out.append(text(x0, 64, "DF(x): R³ → R²；选基后才写成 J∈R²ˣ³", 12, fill=MUTED))
    out.append(rect(x0 + 5, 102, 110, 86, "#eff6ff", BLUE, 12, 2))
    out.append(text(x0 + 60, 131, "输入扰动", 12, 700, "middle", BLUE))
    out.append(text(x0 + 60, 158, "h ∈ R³", 17, 700, "middle"))
    out.append(line(x0 + 120, 145, x0 + 205, 145, BLUE, 3, marker="arrow-blue"))
    out.append(text(x0 + 163, 129, "DF(x)", 12, 700, "middle", BLUE))
    out.append(rect(x0 + 210, 102, 110, 86, "#ecfdf5", GREEN, 12, 2))
    out.append(text(x0 + 265, 131, "输出扰动", 12, 700, "middle", GREEN))
    out.append(text(x0 + 265, 158, "k ∈ R²", 17, 700, "middle"))

    values = [["1", "2", "−1"], ["0", "1", "2"]]
    colors = {(0, 0): "#dbeafe", (1, 0): "#dbeafe", (0, 1): "#f3e8ff", (1, 1): "#f3e8ff", (0, 2): "#ffedd5", (1, 2): "#ffedd5"}
    matrix_grid(out, x0 + 67, 235, 2, 3, 54, 42, values, colors)
    out.append(text(x0 + 25, 265, "J =", 16, 700))
    out.append(text(x0 + 148, 342, "第 j 列 = DF(x)[eⱼ]", 12, 700, "middle"))
    out.append(text(x0 + 148, 368, "完整矩阵依赖输入/输出坐标与布局", 11, fill=MUTED, anchor="middle"))
    out.append(rect(x0 + 12, 408, 318, 88, "#ffffff", "#cbd5e1", 10, 1.3))
    out.append(text(x0 + 28, 435, "算子：DF(x)", 12, 700, fill=INK))
    out.append(text(x0 + 28, 460, "作用：Jv（不必存 J）", 12, 700, fill=BLUE))
    out.append(text(x0 + 28, 485, "表示：J（选基后的 m×n 数组）", 12, 700, fill=PURPLE))

    # Panel B.
    x1 = 430
    out.append(text(x1, 38, "B  JVP 向前推切向量，VJP 向后拉协向量", 19, 700))
    out.append(text(x1, 64, "两条路径由配对恒等式锁在一起", 12, fill=MUTED))
    cx = x1 + 225
    cy = 235
    out.append(rect(cx - 70, cy - 48, 140, 96, "#ffffff", INK, 14, 2))
    out.append(text(cx, cy - 10, "A = DF(x)", 18, 700, "middle"))
    out.append(text(cx, cy + 20, "Rⁿ → Rᵐ", 13, 600, "middle", MUTED))

    # JVP top/forward.
    out.append(circle(x1 + 38, cy - 82, 25, BLUE))
    out.append(text(x1 + 38, cy - 76, "v", 18, 700, "middle", "#ffffff"))
    out.append(line(x1 + 67, cy - 82, cx - 75, cy - 28, BLUE, 3, marker="arrow-blue"))
    out.append(line(cx + 75, cy - 28, x1 + 405, cy - 82, BLUE, 3, marker="arrow-blue"))
    out.append(circle(x1 + 432, cy - 82, 29, GREEN))
    out.append(text(x1 + 432, cy - 76, "Av", 15, 700, "middle", "#ffffff"))
    out.append(text(cx, cy - 94, "JVP / pushforward", 13, 700, "middle", BLUE))
    out.append(text(cx, cy - 72, "输入切向量 → 输出切向量", 11, fill=MUTED, anchor="middle"))

    # VJP bottom/backward.
    out.append(circle(x1 + 432, cy + 96, 25, PURPLE))
    out.append(text(x1 + 432, cy + 102, "u*", 15, 700, "middle", "#ffffff"))
    out.append(line(x1 + 402, cy + 96, cx + 75, cy + 30, PURPLE, 3, marker="arrow-purple"))
    out.append(line(cx - 75, cy + 30, x1 + 68, cy + 96, PURPLE, 3, marker="arrow-purple"))
    out.append(circle(x1 + 38, cy + 96, 30, ORANGE))
    out.append(text(x1 + 38, cy + 102, "A′u*", 12, 700, "middle", "#ffffff"))
    out.append(text(cx, cy + 93, "VJP / pullback", 13, 700, "middle", PURPLE))
    out.append(text(cx, cy + 115, "输出协向量 → 输入协向量", 11, fill=MUTED, anchor="middle"))

    out.append(rect(x1 + 18, 398, 424, 100, "#ffffff", "#cbd5e1", 10, 1.3))
    out.append(text(cx, 429, "u*(Av) = (A′u*)(v)", 18, 700, "middle"))
    out.append(text(cx, 456, "欧氏坐标：uᵀ(Jv) = (Jᵀu)ᵀv", 13, 700, "middle", PURPLE))
    out.append(text(cx, 481, "这是最重要的伴随点积测试", 12, 650, "middle", MUTED))

    # Panel C.
    x2 = 930
    out.append(text(x2, 38, "C  完整 Jacobian：按列推，按行拉", 19, 700))
    out.append(text(x2, 64, "F:R⁸→R³，J 有 3×8=24 个坐标", 12, fill=MUTED))
    vals = [["" for _ in range(8)] for _ in range(3)]
    col_hi = {(i, 1): "#dbeafe" for i in range(3)}
    matrix_grid(out, x2 + 18, 116, 3, 8, 38, 35, vals, col_hi)
    out.append(text(x2 + 170, 105, "一列 = J eⱼ", 11, 700, "middle", BLUE))
    out.append(text(x2 + 170, 246, "forward：8 个基方向 / 8 次列式作用", 12, 700, "middle", BLUE))

    row_hi = {(1, j): "#f3e8ff" for j in range(8)}
    matrix_grid(out, x2 + 18, 285, 3, 8, 38, 35, vals, row_hi)
    out.append(text(x2 + 170, 274, "一行 = eᵢᵀ J", 11, 700, "middle", PURPLE))
    out.append(text(x2 + 170, 415, "reverse：3 个输出种子 / 3 次行式回拉", 12, 700, "middle", PURPLE))

    out.append(rect(x2 + 8, 447, 324, 58, "#ecfdf5", GREEN, 10, 1.5))
    out.append(text(x2 + 170, 471, "若 F:Rⁿ→R，m=1", 12, 700, "middle", GREEN))
    out.append(text(x2 + 170, 493, "一次 VJP（种子 1）得到梯度", 12, 700, "middle"))

    out.append(text(WIDTH / 2, 555, "Jacobian 是坐标表 · JVP 计算 DF(x)[v] · VJP 计算对偶回拉 · 需要作用时通常不要物化整张表", 13, 700, "middle"))
    out.append(text(WIDTH / 2, 578, "形成全 J：forward 约按输入维数计，reverse 约按输出维数计；真实成本仍受程序结构、批处理和内存影响", 11, 500, "middle", MUTED))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    root = Path(__file__).resolve().parents[2]
    target = root / "_assets" / "figures" / "jacobian-jvp-vjp" / "fig-jacobian-jvp-vjp-v2.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_svg(), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
