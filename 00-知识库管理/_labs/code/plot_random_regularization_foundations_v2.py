#!/usr/bin/env python3
"""Generate deterministic NN-57--60 random-regularization textbook figures."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def dropout_expectation():
    out = begin(
        "Dropout：均值匹配、方差代价与非线性边界",
        "Inverted Dropout 用 Bernoulli keep mask 除以 q；被 mask 张量条件均值保持，但二阶矩放大，经过非线性后的预测均值一般不由一次 evaluation pass 精确给出。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "mask、scale 与条件期望", BLUE)
    labels = (("2", BLUE), ("-1", BLUE), ("3", BLUE))
    for i, (lab, color) in enumerate(labels):
        x = 54 + i * 94
        out += [rect(x, 104, 72, 44, color, "#EFF6FF", 4, 1.8),
                text(x + 36, 132, lab, 16, 700, "middle", color)]
    out += [text(50, 180, "x", 17, 700, fill=MUTED),
            text(200, 180, "q = .5", 15, 650, "middle", AMBER)]
    masks = (("1", TEAL), ("0", RED), ("1", TEAL))
    for i, (lab, color) in enumerate(masks):
        x = 54 + i * 94
        out += [circle(x + 36, 231, 21, color, BG, 2),
                text(x + 36, 237, lab, 15, 700, "middle", color)]
    out += [line(200, 258, 200, 292, INK, 2.2, marker="a3")]
    ys = (("4", TEAL), ("0", RED), ("6", TEAL))
    for i, (lab, color) in enumerate(ys):
        x = 54 + i * 94
        out += [rect(x, 305, 72, 44, color, BG, 4, 1.8),
                text(x + 36, 333, lab, 16, 700, "middle", color)]
    out += [rect(50, 389, 310, 84, TEAL, "#ECFDF5", 5, 2),
            text(205, 419, "y = (m / q) ⊙ x", 17, 700, "middle", TEAL),
            text(205, 449, "E[y | x] = x", 18, 700, "middle", INK)]

    heading(out, 430, "B", "均值不免费：variance amplifier", TEAL)
    x0, y0, w, h = 468, 126, 260, 260
    out += [line(x0, y0 + h, x0 + w, y0 + h, INK, 2),
            line(x0, y0, x0, y0 + h, INK, 2),
            text(x0 + w, y0 - 12, "keep q →", 15, 650, "end", MUTED),
            text(x0 + 4, y0 - 12, "p / q", 15, 650, fill=MUTED)]
    qs = [0.2 + 0.1 * i for i in range(8)]
    vals = [(1 - q) / q for q in qs]
    points = []
    for q, v in zip(qs, vals):
        px = x0 + (q - 0.2) / 0.7 * w
        py = y0 + h - min(v, 4.0) / 4.0 * h
        points.append((px, py))
        out += [circle(px, py, 4.5, RED, RED, 1)]
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    out += [path(d, RED, 3),
            line(x0, y0 + h / 2, x0 + w, y0 + h / 2, GRID, 1.5, "6 5"),
            text(x0 + 6, y0 + h + 30, ".2", 15, 600, fill=MUTED),
            text(x0 + w - 5, y0 + h + 30, ".9", 15, 600, "end", MUTED),
            rect(445, 425, 315, 60, AMBER, "#FFFBEB", 5, 2),
            text(602, 451, "Var(y_i | x) = (p/q) x_i²", 16, 700, "middle", AMBER),
            text(602, 476, "small q creates rare large activations", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "非线性后不能交换 E 与 f", RED)
    out += [rect(846, 98, 126, 54, BLUE, "#EFF6FF", 4, 2),
            text(909, 131, "y = 0", 17, 700, "middle", BLUE),
            rect(1004, 98, 126, 54, TEAL, "#ECFDF5", 4, 2),
            text(1067, 131, "y = 2", 17, 700, "middle", TEAL),
            text(988, 184, "each with probability .5", 15, 600, "middle", MUTED),
            rect(846, 218, 284, 90, RED, "#FFF5F2", 5, 2),
            text(988, 248, "f(y) = ReLU(y - 1)", 16, 700, "middle", RED),
            text(988, 280, "E f(y) = .5  ≠  f(Ey) = 0", 17, 700, "middle", INK),
            rect(846, 352, 284, 58, TEAL, "#ECFDF5", 5, 2),
            text(988, 387, "train: random mask / eval: identity", 15, 700, "middle", TEAL),
            rect(846, 438, 284, 48, AMBER, "#FFFBEB", 4, 2),
            text(988, 468, "state + RNG belong to the contract", 15, 700, "middle", AMBER)]
    return finish(out, "Dropout 保持被 mask 张量的条件均值，却放大二阶矩；一次 deterministic evaluation 不是一般非线性随机网络的精确平均。")


def dropout_evidence_boundaries():
    out = begin(
        "Dropout 解释地图：方差、显式正则与 Bayesian 近似",
        "同一训练算子可从二阶矩、expected noisy risk 与变分近似三个层级研究；层级之间有条件桥梁，不能把启发性共适应叙述直接升级为 posterior 定理。",
        (TEAL, BLUE, AMBER),
    )
    heading(out, 42, "A", "随机输入的完整 variance 账", TEAL)
    out += [rect(52, 98, 310, 78, BLUE, "#EFF6FF", 5, 2),
            text(207, 128, "E[y] = μ", 18, 700, "middle", BLUE),
            text(207, 157, "y = (m/q) x", 15, 600, "middle", MUTED),
            line(207, 185, 207, 216, INK, 2.1, marker="a3"),
            rect(52, 226, 310, 92, TEAL, "#ECFDF5", 5, 2),
            text(207, 257, "Var(y) = (σ² + p μ²) / q", 16, 700, "middle", TEAL),
            text(207, 289, "mask noise + data variation", 15, 600, "middle", MUTED),
            rect(52, 364, 310, 106, AMBER, "#FFFBEB", 5, 2),
            text(207, 394, "linear score u = wᵀy", 16, 700, "middle", AMBER),
            text(207, 424, "Var(u | x) = (p/q) Σ wᵢ²xᵢ²", 15, 700, "middle", INK),
            text(207, 453, "shared masks also create covariance", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "平方损失中的精确 penalty", BLUE)
    out += [rect(445, 100, 315, 72, BLUE, "#EFF6FF", 5, 2),
            text(602, 128, "prediction = wᵀ[(m/q)⊙x]", 15, 700, "middle", BLUE),
            text(602, 156, "target = t", 15, 600, "middle", MUTED),
            line(602, 181, 602, 216, INK, 2.1, marker="a3"),
            rect(445, 226, 315, 120, TEAL, "#ECFDF5", 5, 2),
            text(602, 256, "E[(t - wᵀy)²]", 17, 700, "middle", TEAL),
            text(602, 288, "= (t - wᵀx)²", 16, 650, "middle", INK),
            text(602, 319, "+ (p/q) Σ wᵢ²xᵢ²", 16, 700, "middle", RED),
            rect(445, 394, 315, 88, AMBER, "#FFFBEB", 5, 2),
            text(602, 424, "exact here; GLM often local", 15, 700, "middle", AMBER),
            text(602, 454, "deep-network equivalence is not free", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "Bayesian claim 的证据阶梯", AMBER)
    levels = (
        ("1  stochastic predictor", BLUE),
        ("2  MC mean / variance", TEAL),
        ("3  specified variational family", AMBER),
        ("4  calibrated posterior claim", RED),
    )
    for i, (label, color) in enumerate(levels):
        y = 94 + i * 82
        out += [rect(846, y, 284, 54, color, BG, 4, 1.8),
                text(988, y + 34, label, 15, 700, "middle", color)]
        if i < len(levels) - 1:
            out += [line(988, y + 58, 988, y + 78, INK, 1.8, marker="a3")]
    out += [rect(846, 435, 284, 50, RED, "#FFF5F2", 4, 2),
            text(988, 466, "more MC samples ≠ less model bias", 15, 700, "middle", RED)]
    return finish(out, "先说明研究层级：moment 恒等式、expected-risk penalty、变分近似或经验机制；不同证据不能越级互相替代。")


def noise_location_covariance():
    out = begin(
        "Noise Location：相同边际方差，不同联合结构",
        "Activation dropout、DropConnect 与 additive weight/activation noise 把随机变量放在不同计算对象上。即使单个输出方差匹配，输出协方差、梯度共享与 kernel 成本仍可不同。",
        (BLUE, RED, TEAL),
    )
    heading(out, 42, "A", "随机变量放在哪里？", BLUE)
    out += [rect(52, 92, 310, 72, BLUE, "#EFF6FF", 5, 2),
            text(207, 122, "activation noise", 17, 700, "middle", BLUE),
            text(207, 151, "z = W [(m/q) ⊙ x]", 16, 650, "middle", INK),
            rect(52, 202, 310, 72, RED, "#FFF5F2", 5, 2),
            text(207, 232, "DropConnect", 17, 700, "middle", RED),
            text(207, 261, "z = [(M/q) ⊙ W] x", 16, 650, "middle", INK),
            rect(52, 312, 310, 72, TEAL, "#ECFDF5", 5, 2),
            text(207, 342, "additive noise", 17, 700, "middle", TEAL),
            text(207, 371, "W+σE  or  x+σε", 16, 650, "middle", INK),
            rect(52, 424, 310, 60, AMBER, "#FFFBEB", 5, 2),
            text(207, 451, "mask axes define the joint law", 15, 700, "middle", AMBER),
            text(207, 477, "not just a scalar noise rate", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "toy output covariance", RED)
    out += [text(602, 102, "W = [[1,2],[-1,1]],  x = [2,1]", 15, 700, "middle", INK),
            text(602, 132, "q = .5; both give E[z] = [4,-1]", 15, 600, "middle", MUTED),
            rect(445, 182, 315, 112, BLUE, "#EFF6FF", 5, 2),
            text(602, 212, "activation mask shared by outputs", 15, 700, "middle", BLUE),
            text(602, 250, "Cov(z|x) = [[8, -2],", 17, 700, "middle", INK),
            text(602, 278, "             [-2, 5]]", 17, 700, "middle", INK),
            rect(445, 338, 315, 112, RED, "#FFF5F2", 5, 2),
            text(602, 368, "independent DropConnect entries", 15, 700, "middle", RED),
            text(602, 406, "Cov(z|x) = [[8, 0],", 17, 700, "middle", INK),
            text(602, 434, "             [0, 5]]", 17, 700, "middle", INK)]

    heading(out, 830, "C", "目标、估计器与系统分账", TEAL)
    cards = (
        ("expected noisy loss", "which objective?", BLUE),
        ("local reparameterization", "which estimator?", TEAL),
        ("mask / dequant kernel", "which runtime?", AMBER),
    )
    for i, (title, sub, color) in enumerate(cards):
        y = 96 + i * 112
        out += [rect(846, y, 284, 82, color, BG, 5, 2),
                text(988, y + 31, title, 15, 700, "middle", color),
                text(988, y + 61, sub, 15, 600, "middle", MUTED)]
    out += [rect(846, 438, 284, 48, RED, "#FFF5F2", 4, 2),
            text(988, 468, "gradient masking is another contract", 15, 700, "middle", RED)]
    return finish(out, "比较噪声方法时至少固定：随机对象、共享轴、缩放、expected objective、gradient estimator 与实际 kernel。")


def stochastic_depth_paths():
    out = begin(
        "Stochastic Depth / DropPath：随机残差分支与有效深度",
        "Residual rail 允许对整条 branch 采 Bernoulli gate。Inverted scaling 匹配单块条件均值；活跃块数是 Poisson-binomial 变量，而实际计算是否减少取决于是否真正短路 branch。",
        (TEAL, BLUE, RED),
    )
    heading(out, 42, "A", "rail 保留，branch 随机", TEAL)
    y = 280
    xs = [55, 132, 209, 286]
    out += [line(50, y, 355, y, TEAL, 4, marker="a0")]
    gates = ((1, TEAL), (0, RED), (1, TEAL), (1, TEAL))
    for i, (gate, color) in enumerate(gates):
        x = xs[i]
        out += [circle(x + 23, y, 17, TEAL, BG, 2),
                path(f"M{x+23} {y-18}V{y-88}H{x+62}V{y-18}", color, 2.4),
                rect(x + 33, y - 121, 58, 38, color, BG, 4, 1.8),
                text(x + 62, y - 96, f"F{i+1}", 15, 700, "middle", color),
                text(x + 62, y - 137, f"b={gate}", 15, 700, "middle", color)]
    out += [rect(52, 360, 310, 112, TEAL, "#ECFDF5", 5, 2),
            text(207, 391, "x[l+1] = x[l] + (b_l/q_l) F_l(x[l])", 16, 700, "middle", TEAL),
            text(207, 423, "b=0: parameter gradient is zero", 15, 650, "middle", INK),
            text(207, 452, "input still has the identity rail", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "survival schedule → depth law", BLUE)
    x0, y0, w, h = 475, 110, 245, 210
    out += [line(x0, y0 + h, x0 + w, y0 + h, INK, 2),
            line(x0, y0, x0, y0 + h, INK, 2),
            text(x0 - 2, y0 - 12, "q_l", 16, 700, fill=MUTED),
            text(x0 + w, y0 - 12, "block l →", 15, 650, "end", MUTED)]
    qs = [0.875, 0.75, 0.625, 0.5]
    pts = []
    for i, q in enumerate(qs):
        px = x0 + i * w / 3
        py = y0 + h - (q - 0.4) / 0.6 * h
        pts.append((px, py))
        out += [circle(px, py, 6, BLUE, BLUE, 1),
                text(px, y0 + h + 28, str(i + 1), 15, 600, "middle", MUTED)]
    out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts), BLUE, 3),
            rect(445, 365, 315, 118, AMBER, "#FFFBEB", 5, 2),
            text(602, 395, "D = sum_l b_l", 18, 700, "middle", AMBER),
            text(602, 427, "E[D] = 2.75", 16, 700, "middle", INK),
            text(602, 458, "Var(D) = .78125", 16, 700, "middle", INK)]

    heading(out, 830, "C", "实现语义决定收益", RED)
    items = (
        ("batch gate", "one decision for all samples", BLUE),
        ("row gate", "one gate per sample", TEAL),
        ("mask after F", "usually no FLOP saving", RED),
        ("true short-circuit", "expected compute ≈ sum_l q_l C_l", AMBER),
    )
    for i, (title, sub, color) in enumerate(items):
        yv = 88 + i * 93
        out += [rect(846, yv, 284, 68, color, BG, 4, 1.8),
                text(988, yv + 27, title, 15, 700, "middle", color),
                text(988, yv + 53, sub, 15, 600, "middle", MUTED)]
    out += [text(988, 485, "train/eval scale and RNG must match", 15, 700, "middle", RED)]
    return finish(out, "有效深度是随机路径统计，不是物理网络变浅的同义词；均值、梯度、branch compute 与 normalization state 必须分别验收。")


FIGURES = {
    "fig-dropout-expectation-inverted-scaling-v2.svg": dropout_expectation,
    "fig-dropout-variance-evidence-boundaries-v2.svg": dropout_evidence_boundaries,
    "fig-noise-location-output-covariance-v2.svg": noise_location_covariance,
    "fig-stochastic-depth-effective-paths-v2.svg": stochastic_depth_paths,
}


def audit_numbers() -> None:
    x = [2.0, -1.0, 3.0]
    q = 0.5
    assert [v / q for v in (2.0, 0.0, 3.0)] == [4.0, 0.0, 6.0]
    assert [((1 - q) / q) * v * v for v in x] == [4.0, 1.0, 9.0]
    nonlinear_mean = 0.5 * max(0.0 - 1.0, 0.0) + 0.5 * max(2.0 - 1.0, 0.0)
    assert nonlinear_mean == 0.5 and max(1.0 - 1.0, 0.0) == 0.0
    cov_activation = ((8.0, -2.0), (-2.0, 5.0))
    cov_dropconnect = ((8.0, 0.0), (0.0, 5.0))
    assert cov_activation[0][0] == cov_dropconnect[0][0]
    assert cov_activation[1][1] == cov_dropconnect[1][1]
    qs = [0.875, 0.75, 0.625, 0.5]
    assert math.isclose(sum(qs), 2.75)
    assert math.isclose(sum(qv * (1 - qv) for qv in qs), 0.78125)


def main() -> None:
    audit_numbers()
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
