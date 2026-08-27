#!/usr/bin/env python3
"""Generate LT-41--44 paper-ink figures for classical statistical models."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def bias_variance_noise():
    out = begin(
        "偏差、方差与噪声：先固定概率对象",
        "在固定测试输入处，重复训练产生预测分布；其中心与真实条件均值之差是偏差，散布是方差，fresh response 的条件随机性是噪声。积分到新输入后才得到 Random-X risk。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "固定 x0，重复训练", BLUE)
    out += [line(65, 330, 345, 330, GRID, 2)]
    out += [line(210, 95, 210, 360, GRID, 2, "6 5")]
    out += [text(210, 82, "f*(x0)", 15, 700, "middle", fill=RED)]
    preds = ((115, 265), (145, 210), (165, 300), (180, 245), (195, 190), (225, 280), (245, 225), (265, 255), (290, 205))
    for x, y in preds:
        out += [circle(x, y, 6, BLUE, BLUE)]
    out += [line(190, 170, 190, 315, TEAL, 3)]
    out += [text(180, 390, "mean prediction", 14, 700, "middle", fill=TEAL)]
    out += [text(45, 435, "bias = E_S fhat(x0) - f*(x0)", 14, 650, cls="math")]
    out += [text(45, 475, "variance = spread over repeated S and seeds", 14, 650)]
    out += [text(45, 515, "one fitted curve cannot reveal this distribution。", 15, fill=MUTED)]

    heading(out, 430, "B", "平方误差的三个正交来源", TEAL)
    for y, lab, col in (
        (105, "irreducible noise  Var(Y|x0)", RED),
        (225, "squared bias  [E fhat - f*]^2", BLUE),
        (345, "estimator variance  Var(fhat)", TEAL),
    ):
        node(out, 445, y, 310, 72, lab, col, size=15)
    out += [text(430, 460, "expected test MSE = noise + bias^2 + variance", 14, 700, cls="math")]
    out += [text(430, 495, "cross terms vanish only under the declared centering", 14, 650)]
    out += [text(430, 515, "the identity is loss-specific。", 15, fill=MUTED)]

    heading(out, 830, "C", "Trade-off 不是单调定律", RED)
    out += [line(850, 390, 1125, 390, GRID, 2), line(850, 105, 850, 390, GRID, 2)]
    out += [path("M860 130C930 180 1020 285 1115 360", BLUE, 3)]
    out += [path("M860 355C930 290 1020 180 1115 125", TEAL, 3)]
    out += [path("M860 300C930 220 1010 215 1115 305", RED, 3)]
    out += [text(875, 165, "bias^2", 14, 700, fill=BLUE)]
    out += [text(1050, 165, "variance", 14, 700, fill=TEAL)]
    out += [text(1000, 270, "total", 14, 700, fill=RED)]
    out += [text(985, 425, "flexibility", 14, 650, "middle")]
    out += [text(830, 465, "double descent can change the risk shape", 14, 650)]
    out += [text(830, 515, "decomposition is an identity, not a universal curve。", 15, fill=MUTED)]
    return finish(out, "先声明测试点、训练随机性和 loss，再谈 bias、variance 与可约误差。")


def cross_validation_selection():
    out = begin(
        "交叉验证：估计 procedure、选择配置、独立验收",
        "K-fold 在每一折用其余数据训练并在 held-out fold 评价；nested CV 把内层选择与外层评估分开。复用验证结果生成新候选会把固定候选比较变成自适应 transcript。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "K-fold 轮换训练与验证", BLUE)
    colors = [RED, BLUE, BLUE, BLUE, BLUE]
    for k in range(5):
        y = 100 + k * 78
        for j in range(5):
            col = RED if j == k else BLUE
            out += [rect(55 + j * 60, y, 48, 42, col, BG, 5, 2)]
            out += [text(79 + j * 60, y + 27, "V" if j == k else "T", 14, 700, "middle", fill=col)]
    out += [text(45, 500, "each row trains on 4 folds and validates on 1", 14, 650)]
    out += [text(45, 515, "fold errors share data and are correlated。", 15, fill=MUTED)]

    heading(out, 430, "B", "Nested CV 隔离选择与评估", TEAL)
    node(out, 445, 92, 310, 60, "outer training split", BLUE, size=16)
    out += [line(600, 157, 600, 187, INK, 2.5, marker="a3")]
    node(out, 445, 197, 310, 70, "inner CV chooses lambda and pipeline", TEAL, size=15)
    out += [line(600, 272, 600, 302, INK, 2.5, marker="a3")]
    node(out, 445, 312, 310, 60, "refit on outer training", BLUE, size=16)
    out += [line(600, 377, 600, 407, INK, 2.5, marker="a3")]
    node(out, 445, 417, 310, 55, "outer test: evaluate once", RED, size=15)
    out += [text(430, 505, "outer scores estimate the whole selected procedure。", 14, fill=MUTED)]

    heading(out, 830, "C", "选择与泄漏的两条风险", RED)
    node(out, 845, 100, 285, 64, "M fixed candidates", BLUE, size=16)
    out += [line(987, 169, 987, 205, INK, 2.5, marker="a3")]
    node(out, 845, 215, 285, 75, "min validation error is optimistic", RED, size=15)
    out += [text(830, 340, "legal: simultaneous radius includes log M", 14, 650, cls="math")]
    out += [text(830, 390, "leakage: fit scaler / features before splitting", 14, 700, fill=RED)]
    out += [text(830, 435, "adaptive search: transcript exceeds final model id", 14, 650)]
    out += [text(830, 475, "group and time data need structural folds", 14, 650)]
    out += [text(830, 515, "a final untouched test remains a separate role。", 15, fill=MUTED)]
    return finish(out, "CV 是一套数据使用协议：内层选择，外层评价，所有 preprocessing 都必须进入训练折。")


def linear_regression_theory():
    out = begin(
        "线性回归：总体投影、有限样本估计与新点风险",
        "总体最优线性预测器是 L2 投影；固定设计 OLS 的 sampling covariance 由 X^T X 控制；Random-X risk 还要用新输入协方差度量参数误差。异方差与小奇异值分别破坏 naive inference 和数值稳定。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "总体目标是 L2 投影", BLUE)
    out += [path("M65 365C120 120 250 115 340 320", GRID, 3)]
    out += [line(80, 340, 335, 170, BLUE, 3)]
    out += [circle(235, 235, 7, TEAL, TEAL)]
    out += [line(235, 235, 285, 285, RED, 2.5, "6 5")]
    out += [text(95, 125, "all measurable regression functions", 14, 650)]
    out += [text(245, 220, "f_H*", 15, 700, fill=TEAL)]
    out += [text(290, 305, "residual orthogonal to X", 14, 700, fill=RED)]
    out += [text(45, 430, "E[X(Y-X^T beta*)] = 0", 16, 700, cls="math")]
    out += [text(45, 475, "this does not require E[residual|X]=0", 14, 650)]
    out += [text(45, 515, "projection target and true mechanism can differ。", 15, fill=MUTED)]

    heading(out, 430, "B", "Fixed-X：无偏与 covariance", TEAL)
    node(out, 445, 100, 310, 64, "betahat = (X^T X)^-1 X^T y", BLUE, size=15)
    out += [line(600, 170, 600, 205, INK, 2.5, marker="a3")]
    node(out, 445, 215, 310, 80, "Cov(betahat|X) = sigma^2 (X^T X)^-1", TEAL, size=14)
    out += [line(600, 300, 600, 335, INK, 2.5, marker="a3")]
    node(out, 445, 345, 310, 72, "new mean: x0^T Cov x0", RED, size=15)
    out += [text(430, 460, "new response adds irreducible sigma^2", 14, 650)]
    out += [text(430, 495, "normality is not needed for Gauss-Markov BLUE", 14, 650)]
    out += [text(430, 515, "biased estimators are outside BLUE。", 15, fill=MUTED)]

    heading(out, 830, "C", "谱、异方差与 Random-X", RED)
    for y, s, filt in ((105, "large s_j", "OLS 1/s_j ; ridge stable"), (205, "small s_j", "OLS amplifies noise"), (305, "s_j = 0", "nonidentifiable direction")):
        out += [rect(840, y, 290, 65, RED if y > 200 else BLUE, BG, 7, 2)]
        out += [text(855, y + 27, s, 14, 700, fill=RED if y > 200 else BLUE)]
        out += [text(855, y + 52, filt, 14, 650)]
    out += [text(830, 405, "heteroskedastic Cov: inverse X^T Omega X inverse", 14, 650, cls="math")]
    out += [text(830, 450, "Random-X excess = ||betahat-beta*||_Sigma^2", 14, 700, fill=TEAL, cls="math")]
    out += [text(830, 490, "QR/SVD protects computation, not model validity", 14, 650)]
    out += [text(830, 515, "d >= n requires a new implicit-bias contract。", 15, fill=MUTED)]
    return finish(out, "线性回归必须同时报告总体投影、设计条件性、噪声结构、推断公式与新输入风险。")


def logistic_regression_probability():
    out = begin(
        "逻辑回归：概率目标、凸风险与 separation",
        "logit link 把线性 score 映到概率；conditional log loss 等于 binary entropy 加 KL，因此真实概率是唯一总体最优。有限样本 separation 会让无正则 MLE 沿参数射线逃向无穷。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Score 经 sigmoid 变成概率", BLUE)
    out += [line(60, 380, 345, 380, GRID, 2), line(200, 95, 200, 405, GRID, 2)]
    out += [path("M65 365C125 360 160 320 190 230C220 140 270 115 340 110", BLUE, 3)]
    out += [line(65, 230, 340, 230, GRID, 2, "6 5")]
    out += [text(335, 215, "0.5", 14, 650, "end")]
    out += [text(245, 145, "q = sigmoid(s)", 16, 700, fill=BLUE)]
    out += [text(45, 440, "s = x^T beta = log[q/(1-q)]", 15, 700, cls="math")]
    out += [text(45, 480, "threshold belongs to the decision-cost layer", 14, 650)]
    out += [text(45, 515, "a large logit is not a causal effect。", 15, fill=MUTED)]

    heading(out, 430, "B", "Log loss 是严格 proper", TEAL)
    node(out, 445, 100, 310, 68, "conditional cross-entropy", BLUE, size=16)
    out += [line(600, 173, 600, 208, INK, 2.5, marker="a3")]
    node(out, 445, 218, 310, 78, "H_b(eta) + kl(eta || q)", TEAL, size=17)
    out += [line(600, 301, 600, 336, INK, 2.5, marker="a3")]
    node(out, 445, 346, 310, 68, "unique optimum q = eta(x)", RED, size=16)
    out += [text(430, 460, "linear log-odds restricts representable eta", 14, 650)]
    out += [text(430, 495, "misspecification yields a KL projection", 14, 650)]
    out += [text(430, 515, "accuracy discards probability quality。", 15, fill=MUTED)]

    heading(out, 830, "C", "Convex 不等于 finite MLE", RED)
    out += [line(850, 390, 1130, 390, GRID, 2), line(850, 100, 850, 390, GRID, 2)]
    out += [path("M860 130C930 280 1010 360 1120 370", RED, 3)]
    out += [text(880, 155, "separable data", 14, 700, fill=RED)]
    out += [text(970, 315, "loss -> 0 as ||beta|| -> infinity", 14, 650)]
    out += [path("M865 365C930 250 1000 175 1120 130", TEAL, 3)]
    out += [text(1010, 165, "L2 penalty", 14, 700, fill=TEAL)]
    out += [text(830, 430, "gradient = X^T(p-y) ; Hessian = X^T W X", 14, 650, cls="math")]
    out += [text(830, 470, "stable softplus prevents overflow, not separation", 14, 650)]
    out += [text(830, 515, "regularization restores a target but changes it。", 15, fill=MUTED)]
    return finish(out, "逻辑回归连接概率估计、凸优化与决策；properness、可表示性和 MLE 存在性必须分别检查。")


FIGURES = {
    "fig-bias-variance-noise-contract-v2.svg": bias_variance_noise,
    "fig-cross-validation-selection-protocol-v2.svg": cross_validation_selection,
    "fig-linear-regression-statistical-contract-v2.svg": linear_regression_theory,
    "fig-logistic-regression-probability-separation-v2.svg": logistic_regression_probability,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
