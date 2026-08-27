#!/usr/bin/env python3
"""Generate deterministic NN-25--28 initialization textbook figures."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def polyline(points, color=INK, width=2.5, dash=None):
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>'


def wide_layer_moment_recursion():
    out = begin(
        "宽随机层：从求和、Gaussian Approximation 到 Moment Recursion",
        "零均值独立权重消去交叉项；宽度支持 Gaussian 与经验矩集中近似；训练后相关性和有限宽误差必须单独审计。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Affine sum 的二阶账本", BLUE)
    ys = (120, 190, 260, 330, 400)
    for index, y in enumerate(ys):
        out += [circle(76, y, 18, BLUE, BG, 2), text(76, y + 5, f"h{index+1}", 15, 650, "middle", BLUE)]
        out += [circle(165, y, 18, TEAL, BG, 2), text(165, y + 5, f"w{index+1}", 15, 650, "middle", TEAL)]
        out += [line(96, y, 143, y, INK, 1.8, marker="a3"), line(187, y, 267, 260, GRID, 1.5)]
    node(out, 270, 228, 72, 64, "sum + b", RED, size=15)
    out += [text(55, 455, "E[z^2] = n Var(w) E[h^2] + Var(b)", 16, 700, fill=INK, cls="math")]
    out += [rect(55, 474, 290, 35, RED, "#FFF5F2", 5, 1.8), text(200, 497, "cross terms need a reason to vanish", 15, 650, "middle", RED)]

    heading(out, 430, "B", "Moment operator：q -> r -> q'", TEAL)
    node(out, 447, 105, 90, 54, "q_l", BLUE, size=17)
    node(out, 558, 105, 90, 54, "sqrt(q) Z", TEAL, size=15)
    node(out, 669, 105, 80, 54, "phi", TEAL, size=18)
    out += [line(539, 132, 554, 132, INK, 2, marker="a3"), line(650, 132, 665, 132, INK, 2, marker="a3")]
    node(out, 560, 220, 142, 55, "r = E[phi^2]", BLUE, size=15)
    out += [line(708, 161, 660, 216, TEAL, 2.3, marker="a1")]
    node(out, 485, 335, 230, 62, "q' = sw^2 r + sb^2", RED, size=16)
    out += [line(605, 278, 605, 331, BLUE, 2.3, marker="a0")]
    out += [path("M485 366C430 366 430 132 443 132", RED, 2.2, "none", "7 5", "a2")]
    out += [text(600, 445, "fixed point: q* = F(q*)", 16, 700, "middle", TEAL, "math"), text(600, 478, "attraction requires local/domain stability", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "三个随机性层级不能混写", RED)
    levels = (
        (105, "population / ensemble", "theory expectation", BLUE),
        (205, "one finite network", "empirical across neurons", TEAL),
        (305, "one batch / sample", "conditional statistic", BLUE),
        (405, "after training", "weights and signals correlate", RED),
    )
    for index, (y, title, detail, color) in enumerate(levels):
        out += [rect(845, y, 285, 68, color, BG, 7, 2), text(862, y + 27, title, 16, 700, fill=color), text(862, y + 51, detail, 15, 500, fill=MUTED)]
        if index < len(levels) - 1:
            out += [line(987, y + 71, 987, levels[index + 1][0] - 4, GRID, 1.5)]
    return finish(out, "Moment recursion 是带随机对象与近似层级的算子；固定点、有限宽实现和训练后网络必须分别验证。")


def xavier_fan_compromise():
    out = begin(
        "Xavier / Glorot：Forward 与 Backward 的非方阵折中",
        "Forward 每坐标累加 fan-in 项，reverse 每坐标累加 fan-out 项；Xavier 采用两者算术平均的倒数，并不让非方层两边同时守恒。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一矩阵，两条求和方向", BLUE)
    node(out, 55, 115, 80, 50, "n_in", BLUE, size=15)
    node(out, 268, 115, 80, 50, "n_out", TEAL, size=15)
    node(out, 160, 205, 82, 60, "W", RED, size=21)
    out += [line(138, 140, 174, 201, BLUE, 2.7, marker="a0"), line(228, 201, 265, 140, TEAL, 2.7, marker="a1")]
    out += [text(60, 305, "forward", 17, 700, fill=BLUE), text(60, 337, "v = 1 / n_in", 17, 650, fill=INK, cls="math")]
    out += [text(218, 305, "backward", 17, 700, fill=TEAL), text(218, 337, "v = 1 / n_out", 17, 650, fill=INK, cls="math")]
    out += [rect(55, 382, 292, 72, RED, "#FFF5F2", 7, 2), text(201, 411, "Xavier compromise", 17, 700, "middle", RED), text(201, 437, "v = 2 / (n_in + n_out)", 16, 650, "middle", INK, "math")]
    out += [text(201, 488, "exact on both sides only when square", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "Normal / Uniform：同方差合同", TEAL)
    x0, x1, y0, y1 = 450, 590, 130, 300
    out += [line(x0, y1, x1, y1, GRID, 2)]
    bell = []
    for i in range(101):
        x = -3 + 6 * i / 100
        y = math.exp(-0.5 * x * x)
        bell.append((x0 + i / 100 * (x1 - x0), y1 - y * 120))
    out += [polyline(bell, BLUE, 3)]
    out += [text(520, 330, "Gaussian", 16, 700, "middle", BLUE)]
    out += [line(630, 180, 630, 300, TEAL, 3), line(630, 180, 755, 180, TEAL, 3), line(755, 180, 755, 300, TEAL, 3), line(620, 300, 765, 300, GRID, 2)]
    out += [text(692, 330, "Uniform", 16, 700, "middle", TEAL)]
    out += [rect(445, 370, 310, 54, BLUE, BG, 6, 2), text(600, 402, "std = sqrt(2 / fan_sum)", 15, 650, "middle", BLUE, "math")]
    out += [rect(445, 440, 310, 54, TEAL, BG, 6, 2), text(600, 472, "bound = sqrt(6 / fan_sum)", 15, 650, "middle", TEAL, "math")]

    heading(out, 830, "C", "Aspect ratio 让乘数对向变化", RED)
    x0, x1, y0, y1 = 850, 1125, 115, 340
    out += [line(x0, y1, x1, y1, GRID, 2), line(x0, y0, x0, y1, GRID, 2), line(x0, 228, x1, 228, GRID, 1.5, "5 5")]
    points_f, points_b = [], []
    for i in range(121):
        t = i / 120
        log_r = -2.3 + 4.6 * t
        ratio = math.exp(log_r)
        forward = 2 / (1 + ratio)
        backward = 2 * ratio / (1 + ratio)
        x = x0 + t * (x1 - x0)
        points_f.append((x, y1 - forward / 2.0 * (y1 - y0)))
        points_b.append((x, y1 - backward / 2.0 * (y1 - y0)))
    out += [polyline(points_f, BLUE, 3), polyline(points_b, TEAL, 3)]
    out += [text(865, 140, "forward multiplier", 15, 700, fill=BLUE), text(865, 169, "backward multiplier", 15, 700, fill=TEAL)]
    out += [text(850, 370, "n_out << n_in", 15, 600, fill=MUTED), text(1125, 370, "n_out >> n_in", 15, 600, "end", MUTED)]
    out += [rect(845, 404, 285, 88, RED, "#FFF5F2", 7, 2), text(987, 431, "layout audit", 16, 700, "middle", RED), text(987, 456, "helper assumes x @ W^T", 15, 500, "middle", MUTED), text(987, 479, "transpose if code uses x @ W", 15, 500, "middle", MUTED)]
    return finish(out, "Xavier 是明确的前后向尺度折中；必须同时记录 aspect ratio、distribution、gain 与实际矩阵布局。")


def kaiming_rectifier_moments():
    out = begin(
        "He / Kaiming：半轴二阶矩、Rectifier Gain 与 Fan Mode",
        "对 symmetric input，positive 与 negative half-axis 各承载一半 squared energy；negative slope a 经过平方后贡献 a^2，给出 Kaiming gain。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Squared energy 按半轴分账", BLUE)
    x0, x1, y0, y1 = 60, 350, 105, 320
    out += [line(x0, y1, x1, y1, GRID, 2), line(205, y0, 205, y1, GRID, 2)]
    curve = []
    for i in range(161):
        x = -3.2 + 6.4 * i / 160
        y = math.exp(-0.5 * x * x)
        curve.append((x0 + i / 160 * (x1 - x0), y1 - y * 160))
    out += [polyline(curve, INK, 2.8)]
    out += [path("M60 320 " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in curve[:81]) + " L205 320Z", TEAL, 1.5, "#ECFDF5")]
    out += [path("M205 320 " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in curve[80:]) + " L350 320Z", BLUE, 1.5, "#EFF6FF")]
    out += [text(130, 352, "negative half", 15, 700, "middle", TEAL), text(280, 352, "positive half", 15, 700, "middle", BLUE)]
    out += [rect(55, 392, 292, 66, RED, "#FFF5F2", 7, 2), text(201, 419, "factor = (1 + a^2) / 2", 17, 700, "middle", RED, "math"), text(201, 444, "slope is squared in a second moment", 15, 500, "middle", MUTED)]
    out += [text(201, 493, "ReLU: a = 0  ->  factor = 1/2", 15, 650, "middle", BLUE, "math")]

    heading(out, 430, "B", "Gain 补偿 Rectifier Factor", TEAL)
    node(out, 455, 108, 292, 58, "gain^2 = 2 / (1 + a^2)", TEAL, size=17)
    out += [line(600, 170, 600, 205, INK, 2.4, marker="a3")]
    node(out, 455, 218, 292, 62, "Var(W) = gain^2 / fan", BLUE, size=17)
    out += [line(600, 284, 600, 319, INK, 2.4, marker="a3")]
    out += [rect(455, 325, 295, 48, BLUE, BG, 6, 2), text(602, 355, "normal: std = gain / sqrt(fan)", 15, 650, "middle", BLUE, "math")]
    out += [rect(455, 389, 295, 48, TEAL, BG, 6, 2), text(602, 419, "uniform: bound = gain sqrt(3/fan)", 15, 650, "middle", TEAL, "math")]
    out += [rect(455, 453, 295, 41, RED, "#FFF5F2", 6, 2), text(602, 479, "second moment != centered variance", 15, 700, "middle", RED)]

    heading(out, 830, "C", "Fan、Mode 与训练后 Drift", RED)
    out += [rect(845, 105, 285, 70, BLUE, BG, 7, 2), text(862, 132, "dense", 16, 700, fill=BLUE), text(862, 157, "fan-in = input width", 15, 500, fill=MUTED)]
    out += [rect(845, 195, 285, 70, TEAL, BG, 7, 2), text(862, 222, "convolution", 16, 700, fill=TEAL), text(862, 247, "channels x kernel area", 15, 500, fill=MUTED)]
    out += [line(845, 294, 1130, 294, GRID, 2)]
    out += [text(845, 329, "fan-in mode", 15, 700, fill=BLUE), text(1115, 329, "forward target", 15, 600, "end", MUTED)]
    out += [text(845, 370, "fan-out mode", 15, 700, fill=TEAL), text(1115, 370, "backward target", 15, 600, "end", MUTED)]
    out += [rect(845, 410, 285, 82, RED, "#FFF5F2", 7, 2), text(987, 438, "PReLU drift", 16, 700, "middle", RED), text(987, 463, "gain_t / gain_0 depends on a_t", 15, 500, "middle", MUTED)]
    return finish(out, "Kaiming 的二倍来自 half-axis squared energy；fan mode、tensor layout、bias 和 learned slope 决定公式是否仍适用。")


def forward_backward_fan_tradeoff():
    out = begin(
        "Forward / Backward Fan Tradeoff：标量增益、深度乘积与谱边界",
        "同一层的 forward multiplier 使用 fan-in 与 activation moment，backward multiplier 使用 fan-out 与 derivative moment；小偏差沿深度相乘。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "W 与 W^T 交换求和宽度", BLUE)
    node(out, 55, 105, 85, 52, "h: n_in", BLUE, size=15)
    node(out, 265, 105, 85, 52, "z: n_out", TEAL, size=15)
    node(out, 160, 198, 82, 55, "W", RED, size=20)
    out += [line(143, 132, 174, 194, BLUE, 2.5, marker="a0"), line(228, 194, 262, 132, TEAL, 2.5, marker="a1")]
    out += [path("M265 294C225 330 180 330 140 294", TEAL, 2.8, "none", "7 5", "a1")]
    out += [text(205, 282, "reverse uses W^T", 16, 700, "middle", TEAL)]
    out += [rect(55, 356, 292, 55, BLUE, BG, 6, 2), text(201, 389, "chi_f = n_in Var(W) c(q)", 15, 650, "middle", BLUE, "math")]
    out += [rect(55, 430, 292, 55, TEAL, BG, 6, 2), text(201, 463, "chi_b = n_out Var(W) d(q)", 15, 650, "middle", TEAL, "math")]

    heading(out, 430, "B", "Depth 把小偏差变成乘积", TEAL)
    x0, x1, y0, y1 = 450, 750, 112, 340
    out += [line(x0, y1, x1, y1, GRID, 2), line(x0, y0, x0, y1, GRID, 2), line(x0, 228, x1, 228, GRID, 1.5, "5 5")]
    up, down = [], []
    for i in range(101):
        depth = i
        u = min(150.0, 1.05 ** depth)
        d = 0.95 ** depth
        x = x0 + i / 100 * (x1 - x0)
        # log scale from 1e-2 to 1.5e2
        def yy(value):
            lv = math.log10(max(1e-2, min(150.0, value)))
            return y1 - (lv + 2) / (math.log10(150.0) + 2) * (y1 - y0)
        up.append((x, yy(u)))
        down.append((x, yy(d)))
    out += [polyline(up, RED, 3), polyline(down, BLUE, 3)]
    out += [text(465, 137, "1.05^L", 16, 700, fill=RED), text(465, 317, "0.95^L", 16, 700, fill=BLUE), text(750, 367, "depth L", 15, 600, "end", MUTED)]
    out += [rect(450, 394, 300, 92, TEAL, "#ECFDF5", 7, 2), text(600, 422, "bottleneck example", 16, 700, "middle", TEAL), text(600, 448, "512 -> 128: chi_b = 1/4", 15, 500, "middle", MUTED), text(600, 471, "128 -> 512: chi_b = 4", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "证据阶梯：平均矩不是终点", RED)
    gates = (
        (105, "1  scalar second moments", BLUE),
        (172, "2  random-direction JVP / VJP", TEAL),
        (239, "3  extreme singular estimates", RED),
        (306, "4  residual / norm full block", BLUE),
        (373, "5  loss + AMP + distributed scale", TEAL),
    )
    for index, (y, label, color) in enumerate(gates):
        out += [rect(845, y, 285, 45, color, BG, 6, 2), text(987, y + 28, label, 15, 650, "middle", color)]
        if index < len(gates) - 1:
            out += [line(987, y + 47, 987, gates[index + 1][0] - 3, INK, 1.8, marker="a3")]
    out += [rect(845, 447, 285, 52, RED, "#FFF5F2", 7, 2), text(987, 470, "bounded conclusion", 16, 700, "middle", RED), text(987, 491, "initialization neighborhood only", 15, 500, "middle", MUTED)]
    return finish(out, "先校准 forward/backward 标量增益，再检查深度乘积、方向谱与完整训练系统；每一级支持不同强度的结论。")


FIGURES = {
    "fig-wide-layer-moment-recursion-v2.svg": wide_layer_moment_recursion,
    "fig-xavier-fan-compromise-v2.svg": xavier_fan_compromise,
    "fig-kaiming-rectifier-moments-v2.svg": kaiming_rectifier_moments,
    "fig-forward-backward-fan-tradeoff-v2.svg": forward_backward_fan_tradeoff,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
