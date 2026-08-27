#!/usr/bin/env python3
"""Generate deterministic NN-61--64 regularization-interface textbook figures."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def label_smoothing_target_bias() -> str:
    out = begin(
        "Label Smoothing：目标混合、有限 Margin 与估计偏置",
        "Uniform label smoothing 把 one-hot target 与 label prior 混合；交叉熵因此分解为 hard fit 与 prior fit，并把 population target 从真实条件分布推向 prior。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "one-hot → smoothed target", BLUE)
    vals_hard = (1.0, 0.0, 0.0)
    vals_smooth = (0.933, 0.033, 0.033)
    for row, (label, vals, color) in enumerate((("hard y", vals_hard, BLUE), ("eps=.1", vals_smooth, TEAL))):
        y = 112 + row * 132
        out += [text(54, y + 27, label, 16, 700, fill=color)]
        for i, value in enumerate(vals):
            x = 140 + i * 78
            out += [rect(x, y, 62, 48, color, BG, 4, 1.8),
                    text(x + 31, y + 30, f"{value:.3f}" if row else f"{value:.0f}", 15, 700, "middle", color),
                    text(x + 31, y + 74, f"c{i+1}", 15, 600, "middle", MUTED)]
    out += [rect(52, 395, 310, 76, TEAL, "#ECFDF5", 5, 2),
            text(207, 424, "y_eps = (1-eps)y + eps u", 16, 700, "middle", TEAL),
            text(207, 454, "u = (1/K,...,1/K)", 15, 600, "middle", INK)]

    heading(out, 430, "B", "loss 与 logit margin", TEAL)
    out += [rect(445, 100, 310, 78, BLUE, "#EFF6FF", 5, 2),
            text(600, 130, "CE(y_eps,p)", 18, 700, "middle", BLUE),
            text(600, 158, "= (1-eps) CE(y,p) + eps CE(u,p)", 15, 650, "middle", INK),
            line(600, 181, 600, 220, INK, 2.2, marker="a3"),
            rect(445, 232, 310, 104, AMBER, "#FFFBEB", 5, 2),
            text(600, 263, "K=3, eps=.1", 16, 700, "middle", AMBER),
            text(600, 293, "p* = (.9333,.0333,.0333)", 15, 650, "middle", INK),
            text(600, 321, "optimal margin = log 28 = 3.332", 15, 650, "middle", INK),
            rect(445, 385, 310, 86, RED, "#FFF5F2", 5, 2),
            text(600, 416, "CE(u,p) = log K + KL(u || p)", 15, 700, "middle", RED),
            text(600, 448, "not KL(p || u), not entropy itself", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "低置信度不是 uncertainty", RED)
    items = (
        ("target bias", "r = (1-eps) eta + eps u", TEAL),
        ("calibration", "must be measured on held-out data", BLUE),
        ("label noise", "transition model must be declared", AMBER),
        ("distillation", "teacher information can change", RED),
    )
    for i, (title, sub, color) in enumerate(items):
        y = 92 + i * 93
        out += [rect(845, y, 286, 68, color, BG, 4, 1.8),
                text(988, y + 27, title, 15, 700, "middle", color),
                text(988, y + 53, sub, 15, 600, "middle", MUTED)]
    return finish(out, "Label Smoothing 精确改变监督目标；置信度、校准、抗噪与蒸馏效果必须分开验收。")


def mixup_vicinal_geometry() -> str:
    out = begin(
        "Mixup：Vicinal Chord、Beta 强度与 Hidden-Space 边界",
        "Mixup 用同一 lambda 插值输入与标签；Beta alpha 决定 chord interior 的采样强度。输入 chord 或 hidden chord 都是归纳偏置，不自动等于真实语义流形。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一 lambda 混 x 与 y", BLUE)
    x0, y0 = 76, 374
    out += [line(x0, y0, 350, y0, INK, 2), line(x0, y0, x0, 105, INK, 2),
            text(350, y0 + 28, "x[1]", 15, 600, "end", MUTED),
            text(x0 + 4, 100, "x[2]", 15, 600, fill=MUTED)]
    a = (260, 342)
    b = (100, 138)
    m = (140, 189)
    out += [line(a[0], a[1], b[0], b[1], GRID, 3, "7 5"),
            circle(a[0], a[1], 9, BLUE, BLUE, 1), circle(b[0], b[1], 9, RED, RED, 1),
            circle(m[0], m[1], 10, TEAL, BG, 3),
            text(a[0] + 12, a[1] + 6, "x1=(2,0)", 15, 650, fill=BLUE),
            text(b[0] + 12, b[1] - 10, "x2=(0,4)", 15, 650, fill=RED),
            text(m[0] + 15, m[1] + 5, "x~=(.5,3)", 15, 700, fill=TEAL),
            rect(52, 421, 310, 62, TEAL, "#ECFDF5", 5, 2),
            text(207, 447, "lambda=.25 → y~=(.25,0,.75)", 15, 700, "middle", TEAL),
            text(207, 473, "same lambda, paired permutation", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "Beta(alpha,alpha) 决定混合强度", TEAL)
    px0, py0, w, h = 470, 355, 245, 215
    out += [line(px0, py0, px0 + w, py0, INK, 2), line(px0, py0, px0, py0 - h, INK, 2),
            text(px0 + w, py0 - h - 12, "alpha →", 15, 600, "end", MUTED),
            text(px0 + 2, py0 - h - 12, "E[lam(1-lam)]", 15, 650, fill=MUTED)]
    alphas = [0.1, 0.2, 0.5, 1.0, 2.0, 10.0]
    pts = []
    for alpha in alphas:
        strength = alpha / (2 * (2 * alpha + 1))
        xx = px0 + math.log10(alpha / 0.1) / 2.0 * w
        yy = py0 - strength / 0.25 * h
        pts.append((xx, yy))
        out += [circle(xx, yy, 4.5, TEAL, TEAL, 1)]
    out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts), TEAL, 3),
            text(px0, py0 + 29, ".1", 15, 600, "middle", MUTED),
            text(px0 + w / 2, py0 + 29, "1", 15, 600, "middle", MUTED),
            text(px0 + w, py0 + 29, "10", 15, 600, "middle", MUTED),
            rect(445, 405, 315, 78, AMBER, "#FFFBEB", 5, 2),
            text(602, 435, "E[lambda]=.5", 16, 700, "middle", AMBER),
            text(602, 464, "Var(lambda)=1 / {4(2 alpha+1)}", 15, 650, "middle", INK)]

    heading(out, 830, "C", "三份实现合同", RED)
    items = (
        ("input mixup", "pixel/token chord can leave semantics", BLUE),
        ("manifold mixup", "choose layer, suffix and target", TEAL),
        ("normalization", "mixed batch changes statistics", AMBER),
        ("distributed pair", "pairing + RNG define the method", RED),
    )
    for i, (title, sub, color) in enumerate(items):
        y = 90 + i * 94
        out += [rect(845, y, 286, 70, color, BG, 4, 1.8),
                text(988, y + 28, title, 15, 700, "middle", color),
                text(988, y + 55, sub, 15, 600, "middle", MUTED)]
    return finish(out, "Mixup 训练的是 vicinal distribution；chord 的统计、语义、目标与系统实现必须同时声明。")


def jacobian_gradient_lipschitz() -> str:
    out = begin(
        "Jacobian、Gradient Penalty 与 Lipschitz：对象层级与证书缺口",
        "Loss input-gradient、model Jacobian、sampled gradient penalty、layer spectral norm 与 global Lipschitz certificate 是不同对象；有限点和方向的测量不能替代定义域上的 supremum。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先写清被惩罚对象", BLUE)
    items = (
        ("loss gradient", "||grad_x ell(f(x),y)||", BLUE),
        ("model Jacobian", "||J_f(x)||_F or operator norm", TEAL),
        ("WGAN-GP", "(||grad_x D(xhat)||-1)^2", AMBER),
        ("parameter grad", "||grad_theta ell||^2", RED),
    )
    for i, (title, sub, color) in enumerate(items):
        y = 92 + i * 93
        out += [rect(52, y, 310, 68, color, BG, 4, 1.8),
                text(207, y + 27, title, 15, 700, "middle", color),
                text(207, y + 53, sub, 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "一个方向可漏掉 worst case", TEAL)
    cx, cy = 600, 267
    out += [line(455, cy, 750, cy, GRID, 2), line(cx, 105, cx, 410, GRID, 2),
            path(f"M{cx-120} {cy} C{cx-120} {cy-55} {cx+120} {cy-55} {cx+120} {cy} C{cx+120} {cy+55} {cx-120} {cy+55} {cx-120} {cy}Z", BLUE, 3, "#EFF6FF"),
            line(cx, cy, cx + 120, cy, RED, 4, marker="a2"),
            line(cx, cy, cx, cy - 55, TEAL, 4, marker="a1"),
            text(cx + 125, cy + 6, "J e1: 3", 15, 700, fill=RED),
            text(cx + 8, cy - 61, "J e2: 1", 15, 700, fill=TEAL),
            rect(445, 414, 310, 68, AMBER, "#FFFBEB", 5, 2),
            text(600, 440, "J = diag(3,1)", 16, 700, "middle", AMBER),
            text(600, 467, "||J||_2=3,  ||J||_F=sqrt(10)", 15, 650, "middle", INK)]

    heading(out, 830, "C", "local penalty ≠ global bound", RED)
    items2 = (
        ("sample points", "where was x or xhat drawn?", BLUE),
        ("sample directions", "Hutchinson estimates Frobenius", TEAL),
        ("layer bounds", "product/sum can be very loose", AMBER),
        ("global claim", "needs domain supremum or certificate", RED),
    )
    for i, (title, sub, color) in enumerate(items2):
        y = 91 + i * 93
        out += [rect(845, y, 286, 68, color, BG, 4, 1.8),
                text(988, y + 27, title, 15, 700, "middle", color),
                text(988, y + 53, sub, 15, 600, "middle", MUTED)]
    return finish(out, "导数正则只对声明的输出、norm、点和方向成立；global Lipschitz 与鲁棒泛化需要额外证书。")


def regularization_interactions() -> str:
    out = begin(
        "网络级正则化：干预位置、交互效应与证据阶梯",
        "正则化可作用于 target、input、activation/path、parameter/update 或 function derivative；联合使用会改变目标、噪声、优化与计算，必须用 factorial interaction 和分层证据审计。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "五个干预位置", BLUE)
    items = (
        ("target", "label smoothing", BLUE),
        ("input / hidden", "mixup", TEAL),
        ("activation / path", "dropout / DropPath", AMBER),
        ("parameter / update", "L2 / AdamW", RED),
        ("function", "Jacobian / consistency", TEAL),
    )
    for i, (title, sub, color) in enumerate(items):
        y = 82 + i * 82
        out += [rect(52, y, 310, 58, color, BG, 4, 1.8),
                text(67, y + 25, title, 15, 700, fill=color),
                text(347, y + 25, sub, 15, 600, "end", MUTED)]

    heading(out, 430, "B", "2×2 才看得见 interaction", TEAL)
    xs = (478, 624)
    ys = (140, 286)
    vals = ((0.30, 0.27), (0.26, 0.20))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            color = BLUE if (i, j) == (0, 0) else TEAL if i + j == 1 else RED
            out += [rect(x, y, 112, 94, color, BG, 5, 2),
                    text(x + 56, y + 35, f"risk {vals[i][j]:.2f}", 16, 700, "middle", color),
                    text(x + 56, y + 67, f"A={i}, B={j}", 15, 600, "middle", MUTED)]
    out += [text(534, 112, "B=0", 15, 700, "middle", BLUE), text(680, 112, "B=1", 15, 700, "middle", BLUE),
            text(455, 190, "A=0", 15, 700, "end", TEAL), text(455, 336, "A=1", 15, 700, "end", TEAL),
            rect(445, 414, 310, 68, AMBER, "#FFFBEB", 5, 2),
            text(600, 440, "Delta_AB=(-.06)-(-.03)=-.03", 15, 700, "middle", AMBER),
            text(600, 468, "synergy on risk in this protocol only", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "claim 逐级升级", RED)
    levels = (
        ("1 exact", "operator / objective identity", BLUE),
        ("2 local", "Taylor / finite-sample estimate", TEAL),
        ("3 mechanism", "controlled mediator + ablation", AMBER),
        ("4 benchmark", "multi-seed held-out comparison", RED),
        ("5 deployment", "shift, cost, monitoring", TEAL),
    )
    for i, (title, sub, color) in enumerate(levels):
        y = 82 + i * 82
        out += [rect(845, y, 286, 58, color, BG, 4, 1.8),
                text(861, y + 22, title, 15, 700, fill=color),
                text(1115, y + 47, sub, 15, 600, "end", MUTED)]
    return finish(out, "联合正则化不是把系数相加；要记录干预位置、交互、调参预算、计算成本与证据等级。")


FIGURES = {
    "fig-label-smoothing-target-bias-v2.svg": label_smoothing_target_bias,
    "fig-mixup-vicinal-geometry-v2.svg": mixup_vicinal_geometry,
    "fig-jacobian-gradient-lipschitz-v2.svg": jacobian_gradient_lipschitz,
    "fig-network-regularization-interactions-v2.svg": regularization_interactions,
}


def audit_numbers() -> None:
    eps, k = 0.1, 3
    target = [1 - eps + eps / k, eps / k, eps / k]
    assert math.isclose(sum(target), 1.0)
    assert math.isclose(math.log(target[0] / target[1]), math.log(28.0))
    alpha = 0.2
    assert math.isclose(1 / (4 * (2 * alpha + 1)), 0.17857142857142858)
    assert math.isclose(alpha / (2 * (2 * alpha + 1)), 0.07142857142857144)
    lam = 0.25
    assert [lam * 2 + (1 - lam) * 0, lam * 0 + (1 - lam) * 4] == [0.5, 3.0]
    assert math.isclose(math.sqrt(3 * 3 + 1 * 1), math.sqrt(10))
    interaction = (0.20 - 0.26) - (0.27 - 0.30)
    assert math.isclose(interaction, -0.03)


def main() -> None:
    audit_numbers()
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
