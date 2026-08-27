#!/usr/bin/env python3
"""Generate deterministic NN-17--20 activation-function textbook figures."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def polyline(points, color=INK, width=2.5, dash=None):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>'


def activation_choice_contract():
    out = begin(
        "激活函数选择：从局部属性到系统证据",
        "局部函数属性经权重与深度组合成传播行为；最终选择还必须同时满足任务输出、初始化、归一化、精度、成本与公平实验合同。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "六个局部观察窗", BLUE)
    cx, cy = 200, 270
    lenses = (
        (200, 120, "range", BLUE), (315, 170, "slope", TEAL),
        (320, 350, "smooth", RED), (200, 420, "symmetry", AMBER),
        (82, 350, "moments", TEAL), (78, 170, "cost", RED),
    )
    for x, y, label, color in lenses:
        out += [line(cx, cy, x, y, GRID, 2)]
    out += [circle(cx, cy, 47, BLUE, "#EFF6FF", 2.5), text(cx, cy + 7, "phi", 23, 700, "middle", BLUE)]
    for x, y, label, color in lenses:
        out += [circle(x, y, 31, color, BG, 2), text(x, y + 5, label, 15, 650, "middle", color)]
    out += [text(48, 482, "一个属性不能替代另一个属性。", 16, 650, fill=MUTED)]

    heading(out, 430, "B", "深层传播是算子乘积", TEAL)
    xs = (445, 520, 595, 670, 745)
    labels = ("W1", "D1", "W2", "D2", "...")
    colors = (BLUE, TEAL, BLUE, TEAL, RED)
    for i, (x, label, color) in enumerate(zip(xs, labels, colors)):
        out += [rect(x, 122, 52, 50, color, BG, 6, 2), text(x + 26, 153, label, 16, 700, "middle", color)]
        if i < len(xs) - 1:
            out += [line(x + 54, 147, xs[i + 1] - 4, 147, INK, 2, marker="a3")]
    out += [text(445, 215, "J = D_L W_L ... D_1 W_1", 18, 700, fill=INK, cls="math")]
    gains = ((275, "activation slope", 0.48, TEAL), (335, "weight gain", 0.72, BLUE), (395, "direction alignment", 0.58, RED))
    for y, label, frac, color in gains:
        out += [text(445, y, label, 15, 650, fill=color), rect(570, y - 17, 175, 18, GRID, "#F8FAFC", 3, 1), rect(570, y - 17, 175 * frac, 18, color, color, 3, 0)]
    out += [rect(445, 440, 310, 48, RED, "#FFF5F2", 6, 2), text(600, 470, "local fact != deep guarantee", 16, 700, "middle", RED)]

    heading(out, 830, "C", "联合选择合同", RED)
    rows = (
        (108, "task / output support", BLUE),
        (173, "initialization / depth", TEAL),
        (238, "normalization / residual", AMBER),
        (303, "dtype / kernel / cost", RED),
        (368, "matched budget / seeds", BLUE),
        (433, "claim boundary", TEAL),
    )
    for i, (y, label, color) in enumerate(rows):
        out += [rect(845, y, 285, 46, color, BG, 6, 2), circle(865, y + 23, 9, color, color, 1), text(885, y + 29, label, 16, 650, fill=INK)]
        if i < len(rows) - 1:
            out += [line(987, y + 48, 987, rows[i + 1][0] - 3, GRID, 1.5)]
    return finish(out, "选择顺序：先确认局部函数事实，再分析深层组合，最后用匹配预算的系统证据验收。")


def _curve_points(fn, x0, x1, y0, y1, xmin=-6.0, xmax=6.0, ymin=-1.2, ymax=1.2, n=180):
    pts = []
    for i in range(n + 1):
        x = xmin + (xmax - xmin) * i / n
        y = max(ymin, min(ymax, fn(x)))
        px = x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
        py = y1 - (y - ymin) / (ymax - ymin) * (y1 - y0)
        pts.append((px, py))
    return pts


def sigmoid_tanh_saturation():
    out = begin(
        "Sigmoid 与 Tanh：值域、导数窗口和深度乘积",
        "两条 S 形曲线都在两端饱和；sigmoid 最大斜率为四分之一且对称输入输出均值二分之一，tanh 中心斜率为一且对称输入输出均值为零。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "输出曲线与中心", BLUE)
    x0, x1, y0, y1 = 65, 350, 110, 425
    out += [line(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, GRID, 2), line((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, GRID, 2)]
    sig = lambda x: 1 / (1 + math.exp(-x))
    out += [polyline(_curve_points(sig, x0, x1, y0, y1, ymin=-1.2, ymax=1.2), BLUE, 3.5)]
    out += [polyline(_curve_points(math.tanh, x0, x1, y0, y1, ymin=-1.2, ymax=1.2), TEAL, 3.5)]
    out += [text(300, 145, "tanh", 16, 700, fill=TEAL), text(300, 235, "sigmoid", 16, 700, fill=BLUE)]
    out += [text(68, 472, "sigmoid center: (0, 1/2)", 15, 650, fill=BLUE), text(68, 496, "tanh center: (0, 0)", 15, 650, fill=TEAL)]

    heading(out, 430, "B", "有效导数只在有限窗口", TEAL)
    xx0, xx1, yy0, yy1 = 445, 755, 120, 420
    out += [line(xx0, yy1, xx1, yy1, GRID, 2), line((xx0 + xx1) / 2, yy0, (xx0 + xx1) / 2, yy1, GRID, 2)]
    sd = lambda x: sig(x) * (1 - sig(x))
    td = lambda x: 1 - math.tanh(x) ** 2
    out += [polyline(_curve_points(sd, xx0, xx1, yy0, yy1, ymin=0, ymax=1.05), BLUE, 3.2)]
    out += [polyline(_curve_points(td, xx0, xx1, yy0, yy1, ymin=0, ymax=1.05), TEAL, 3.2)]
    out += [text(610, 145, "tanh' max = 1", 16, 700, "middle", TEAL), text(610, 335, "sigmoid' max = 1/4", 16, 700, "middle", BLUE)]
    out += [text(445, 475, "tails: derivative -> 0 exponentially", 15, 650, fill=RED)]

    heading(out, 830, "C", "深层账本与角色边界", RED)
    factors = ((110, "activation slope", "q_l"), (175, "weight singular gain", "s_l"), (240, "depth product", "product(q_l s_l)"))
    for i, (y, key, val) in enumerate(factors):
        color = BLUE if i == 0 else TEAL if i == 1 else RED
        out += [rect(845, y, 285, 50, color, BG, 6, 2), text(858, y + 21, key, 15, 700, fill=color), text(858, y + 42, val, 15, 500, fill=INK, cls="math")]
        if i < 2:
            out += [line(987, y + 52, 987, factors[i + 1][0] - 3, INK, 2, marker="a3")]
    out += [line(845, 318, 1130, 318, GRID, 2)]
    out += [rect(845, 345, 135, 62, TEAL, "#ECFDF5", 7, 2), text(912, 371, "gate", 17, 700, "middle", TEAL), text(912, 394, "0..1 control", 15, 500, "middle", MUTED)]
    out += [rect(995, 345, 135, 62, BLUE, "#EFF6FF", 7, 2), text(1062, 371, "output link", 17, 700, "middle", BLUE), text(1062, 394, "Bernoulli", 15, 500, "middle", MUTED)]
    out += [rect(845, 435, 285, 52, RED, "#FFF5F2", 7, 2), text(987, 466, "hidden-layer warning != universal ban", 15, 700, "middle", RED)]
    return finish(out, "饱和诊断必须同时定位输入分布、导数窗口、权重增益与函数在系统中的角色。")


def relu_family_boundaries():
    out = begin(
        "ReLU 家族：区域边界、死亡单元与负侧斜率",
        "ReLU 网络在固定 mask 的区域内为仿射；死亡单元要求跨数据与时间定义；leaky 和 PReLU 打开负侧通道但按斜率改变深层尺度与稀疏性。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "超平面切出两个 Jacobian", BLUE)
    out += [line(65, 435, 350, 435, GRID, 2), line(90, 470, 90, 105, GRID, 2)]
    out += [path("M75 140L335 400", RED, 3), text(280, 418, "x1+x2=1", 15, 700, "middle", RED)]
    out += [path("M170 220L225 165", TEAL, 3, marker="a1"), path("M240 300L295 245", TEAL, 3, marker="a1")]
    out += [text(295, 205, "active: grad=(1,1)", 15, 700, "middle", TEAL), text(125, 335, "inactive", 17, 700, "middle", BLUE), text(125, 362, "grad=(0,0)", 15, 500, "middle", MUTED)]
    out += [rect(66, 466, 280, 38, RED, "#FFF5F2", 6, 2), text(206, 491, "boundary: no unique classical gradient", 15, 650, "middle", RED)]

    heading(out, 430, "B", "dead 必须跨数据与时间定义", TEAL)
    timeline = ((455, "active", TEAL), (545, "batch off", AMBER), (650, "long-window off", RED))
    for i, (x, label, color) in enumerate(timeline):
        out += [circle(x, 190, 28, color, BG, 2.5), text(x, 196, str(i + 1), 16, 700, "middle", color), text(x, 245, label, 15, 650, "middle", color)]
        if i < 2:
            out += [line(x + 30, 190, timeline[i + 1][0] - 32, 190, INK, 2.3, marker="a3")]
    out += [text(445, 305, "dead claim requires:", 16, 700, fill=RED)]
    for i, label in enumerate(("all valid data", "K consecutive steps", "zero parameter VJP")):
        y = 335 + i * 48
        out += [rect(445, y, 310, 37, GRID, "#F8FAFC", 5, 1.5), circle(462, y + 18, 6, RED, RED, 1), text(478, y + 24, label, 15, 600)]

    heading(out, 830, "C", "负侧通道与尺度账本", RED)
    x0, x1, y0, y1 = 845, 1130, 105, 295
    out += [line(x0, 220, x1, 220, GRID, 2), line(987, y0, 987, y1, GRID, 2)]
    relu = lambda x: max(0.0, x)
    leaky = lambda x: max(x, 0.1 * x)
    out += [polyline(_curve_points(relu, x0, x1, y0, y1, xmin=-3, xmax=3, ymin=-2, ymax=3), BLUE, 3.4)]
    out += [polyline(_curve_points(leaky, x0, x1, y0, y1, xmin=-3, xmax=3, ymin=-2, ymax=3), TEAL, 3.2)]
    out += [text(1090, 132, "ReLU", 15, 700, fill=BLUE), text(868, 245, "leaky", 15, 700, fill=TEAL)]
    rows = ((335, "negative slope", "0 / a / learned a"), (390, "second moment", "(1+a^2) q / 2"), (445, "k negative gates", "gain = a^k"))
    for y, key, val in rows:
        out += [text(845, y, key, 15, 700, fill=RED), text(980, y, val, 15, 600, fill=INK, cls="math"), line(845, y + 13, 1130, y + 13, GRID, 1)]
    return finish(out, "Leaky/PReLU 修复的是负侧 exact-zero 局部通道；深度乘积、初始化与系统稀疏仍需独立验收。")


def elu_selu_self_normalizing():
    out = begin(
        "ELU 与 SELU：负饱和、Moment Fixed Point 和条件边界",
        "ELU 负侧指数趋于负常数；SELU 选择 alpha 与 lambda 使理想化均值方差映射在零均值单位方差附近具有吸引结构，并依赖配套初始化与 alpha dropout。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "负侧机制不同", BLUE)
    x0, x1, y0, y1 = 65, 350, 110, 390
    out += [line(x0, 265, x1, 265, GRID, 2), line(205, y0, 205, y1, GRID, 2)]
    elu = lambda x: x if x > 0 else math.exp(x) - 1
    leaky = lambda x: x if x > 0 else 0.15 * x
    out += [polyline(_curve_points(elu, x0, x1, y0, y1, xmin=-5, xmax=4, ymin=-1.8, ymax=4), TEAL, 3.5)]
    out += [polyline(_curve_points(leaky, x0, x1, y0, y1, xmin=-5, xmax=4, ymin=-1.8, ymax=4), BLUE, 2.8, "7 5")]
    out += [path("M65 265L205 265L345 130", RED, 2.8, "none", "4 5")]
    out += [text(80, 335, "ELU -> -alpha", 15, 700, fill=TEAL), text(80, 363, "leaky -> -infinity", 15, 650, fill=BLUE), text(80, 391, "ReLU -> 0", 15, 650, fill=RED)]
    out += [rect(65, 432, 285, 56, TEAL, "#ECFDF5", 7, 2), text(207, 456, "negative output + saturation", 16, 700, "middle", TEAL), text(207, 478, "not positive homogeneous", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "Moment map 指向 (0,1)", TEAL)
    bx0, bx1, by0, by1 = 455, 750, 110, 440
    out += [line(600, by0, 600, by1, GRID, 2), line(bx0, 300, bx1, 300, GRID, 2)]
    out += [text(740, 324, "mean", 15, 650, fill=MUTED), text(570, 125, "variance", 15, 650, fill=MUTED)]
    fixed = (600, 210)
    starts = ((485, 145), (710, 145), (485, 390), (720, 385), (530, 270), (675, 285))
    for x, y in starts:
        ex = fixed[0] + 0.28 * (x - fixed[0]); ey = fixed[1] + 0.28 * (y - fixed[1])
        out += [line(x, y, ex, ey, TEAL, 2.2, marker="a1")]
    out += [circle(*fixed, 11, RED, "#FFF5F2", 3), text(fixed[0] + 22, fixed[1] - 10, "(0,1)", 17, 700, fill=RED, cls="math")]
    out += [rect(455, 455, 295, 42, RED, "#FFF5F2", 6, 2), text(602, 481, "fixed point + invariant domain + contraction", 15, 700, "middle", RED)]

    heading(out, 830, "C", "配套合同与 Alpha Dropout", RED)
    out += [text(845, 106, "required together", 15, 700, fill=RED)]
    reqs = ((125, "weight var ~ 1/fan-in", BLUE), (177, "zero bias / scaled input", TEAL), (229, "plain feedforward assumptions", AMBER))
    for y, label, color in reqs:
        out += [rect(845, y, 285, 40, color, BG, 5, 2), text(987, y + 26, label, 15, 650, "middle", color)]
    out += [line(845, 291, 1130, 291, GRID, 2)]
    out += [text(845, 322, "drop -> c = -lambda alpha", 16, 700, fill=TEAL, cls="math")]
    out += [line(987, 338, 987, 365, TEAL, 2.5, marker="a1")]
    out += [rect(845, 372, 285, 62, TEAL, "#ECFDF5", 7, 2), text(987, 398, "affine correction a*x_tilde+b", 15, 700, "middle", TEAL, "math"), text(987, 421, "restores ideal mean / variance", 15, 500, "middle", MUTED)]
    out += [rect(845, 455, 285, 42, RED, "#FFF5F2", 6, 2), text(987, 481, "residual / attention changes the map", 15, 700, "middle", RED)]
    return finish(out, "自归一化是一条带假设的均值—方差动力系统结论，不是逐 batch 标准化或 Jacobian 谱保证。")


FIGURES = {
    "fig-activation-choice-contract-v2.svg": activation_choice_contract,
    "fig-sigmoid-tanh-saturation-v2.svg": sigmoid_tanh_saturation,
    "fig-relu-family-boundaries-v2.svg": relu_family_boundaries,
    "fig-elu-selu-self-normalizing-v2.svg": elu_selu_self_normalizing,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
