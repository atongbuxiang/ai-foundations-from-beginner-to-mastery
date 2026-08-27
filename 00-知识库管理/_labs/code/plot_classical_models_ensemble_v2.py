#!/usr/bin/env python3
"""Generate LT-45--48 paper-ink figures for kernels, trees, and ensembles."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def svm_margin_kernel():
    out = begin(
        "SVM：几何间隔、凸对偶与 kernel representation",
        "canonical scaling 下 hard margin 宽度由 ||w|| 控制；soft margin 用 hinge/slack 允许违约；Lagrange dual 把解压到 support-vector span，并只通过 Gram entries 访问 feature geometry。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Hard margin 的 canonical 几何", BLUE)
    out += [line(70, 395, 350, 130, INK, 3)]
    out += [line(50, 355, 330, 90, BLUE, 2, "7 6"), line(110, 455, 390, 190, BLUE, 2, "7 6")]
    for x, y in ((85, 190), (120, 235), (150, 165), (185, 270)):
        out += [circle(x, y, 7, BLUE, BLUE)]
    for x, y in ((245, 350), (285, 390), (310, 315), (345, 410)):
        out += [circle(x, y, 7, RED, RED)]
    out += [text(60, 105, "y=+1", 15, 700, fill=BLUE), text(325, 455, "y=-1", 15, 700, fill=RED)]
    out += [text(45, 475, "y_i(<w,phi_i>+b) >= 1", 15, 700, cls="math")]
    out += [text(45, 510, "margin width = 2 / ||w||", 15, 650, cls="math")]

    heading(out, 430, "B", "Primal、Dual 与 KKT", TEAL)
    node(out, 445, 95, 310, 75, "min 1/2 ||w||^2 + C sum xi_i", BLUE, size=15)
    out += [line(600, 175, 600, 205, INK, 2.5, marker="a3")]
    node(out, 445, 215, 310, 75, "0 <= alpha_i <= C ; y^T alpha = 0", TEAL, size=15)
    out += [line(600, 295, 600, 325, INK, 2.5, marker="a3")]
    node(out, 445, 335, 310, 75, "w = sum alpha_i y_i phi(x_i)", RED, size=15)
    out += [text(430, 455, "0 < alpha_i < C: exactly on margin", 15, 650)]
    out += [text(430, 490, "alpha_i = C: inside margin or misclassified", 15, 650)]
    out += [text(430, 515, "support-vector status is sample dependent。", 15, fill=MUTED)]

    heading(out, 830, "C", "Kernel trick 的合同", RED)
    node(out, 845, 95, 285, 65, "PSD Gram K_ij = k(x_i,x_j)", BLUE, size=15)
    out += [line(987, 165, 987, 195, INK, 2.5, marker="a3")]
    node(out, 845, 205, 285, 80, "f(x) = sum alpha_i y_i k(x_i,x) + b", TEAL, size=14)
    out += [line(987, 290, 987, 320, INK, 2.5, marker="a3")]
    node(out, 845, 330, 285, 70, "only support vectors remain", RED, size=15)
    out += [text(830, 445, "small bandwidth: local / near-identity Gram", 15, 650)]
    out += [text(830, 480, "large bandwidth: near-constant / low rank", 15, 650)]
    out += [text(830, 515, "PSD legality does not choose a useful kernel。", 15, fill=MUTED)]
    return finish(out, "SVM 同时是一种 margin geometry、regularized convex program 与 finite kernel expansion。")


def krr_gp_interface():
    out = begin(
        "KRR 与 Gaussian Process：同一均值公式，不同统计对象",
        "KRR 把 RKHS norm 作为 deterministic regularizer；Gaussian process 把 kernel 作为 prior covariance。Gaussian noise 下两者可共享 Gram inverse 的 posterior/estimator mean，但 GP 还定义 posterior covariance 与 joint predictive law。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "KRR 是谱滤波", BLUE)
    out += [line(65, 390, 350, 390, GRID, 2), line(65, 105, 65, 390, GRID, 2)]
    xs = (95, 145, 195, 245, 295, 335)
    mus = (255, 215, 170, 125, 85, 55)
    for x, h in zip(xs, mus):
        out += [rect(x, 390-h, 24, h, BLUE, BG, 3, 2)]
        shrink = int(h * (h / (h + 80)))
        out += [rect(x+27, 390-shrink, 18, shrink, TEAL, TEAL, 3, 1)]
    out += [text(75, 95, "kernel eigenvalues", 15, 700, fill=BLUE)]
    out += [text(80, 430, "blue: mu_j   teal: mu_j/(mu_j+n lambda)", 15, 650, cls="math")]
    out += [text(45, 475, "small directions are suppressed first", 15, 650)]
    out += [text(45, 515, "effective dimension = trace of the smoother。", 15, fill=MUTED)]

    heading(out, 430, "B", "共享的 Mean Formula", TEAL)
    node(out, 445, 95, 310, 72, "KRR: min mean SSE + lambda ||f||_H^2", BLUE, size=15)
    out += [line(600, 172, 600, 205, INK, 2.5, marker="a3")]
    node(out, 445, 215, 310, 78, "fhat(x) = k_x^T (K+n lambda I)^-1 y", TEAL, size=15)
    out += [line(600, 298, 600, 330, INK, 2.5, marker="a3")]
    node(out, 445, 340, 310, 72, "GP match: n lambda = sigma^2 / tau^2", RED, size=15)
    out += [text(430, 455, "same algebra after a declared scale convention", 15, 650)]
    out += [text(430, 490, "representer theorem makes the solution finite", 15, 650)]
    out += [text(430, 515, "same mean is not the same probability model。", 15, fill=MUTED)]

    heading(out, 830, "C", "GP 多出的对象与风险", RED)
    node(out, 845, 95, 285, 65, "posterior covariance at x,x'", TEAL, size=15)
    node(out, 845, 190, 285, 65, "marginal likelihood: fit + log-det", BLUE, size=15)
    node(out, 845, 285, 285, 65, "joint samples and decision uncertainty", RED, size=15)
    out += [text(830, 400, "wrong prior / noise -> wrong uncertainty", 15, 700, fill=RED)]
    out += [text(830, 440, "Cholesky: O(n^3) time, O(n^2) memory", 15, 650)]
    out += [text(830, 478, "jitter stabilizes algebra; noise is statistical", 15, 650)]
    out += [text(830, 515, "low-rank approximation adds a new error layer。", 15, fill=MUTED)]
    return finish(out, "先匹配 normalization，再区分 estimator、prior、uncertainty、hyperparameter selection 与 computation。")


def decision_tree_pruning():
    out = begin(
        "决策树：递归分区、局部增益与全树剪枝",
        "树把输入空间递归切成叶区域并输出局部常数；每次 split 只最大化当前 node 的 impurity decrease。maximal tree 再沿 cost-complexity path 剪枝，选择必须放入独立 validation/CV protocol。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "递归轴对齐划分", BLUE)
    out += [rect(60, 100, 290, 300, GRID, BG, 2, 2)]
    out += [line(185, 100, 185, 400, BLUE, 3), line(185, 245, 350, 245, TEAL, 3), line(60, 315, 185, 315, RED, 3)]
    out += [text(120, 180, "R1", 17, 700, "middle", fill=BLUE)]
    out += [text(270, 180, "R2", 17, 700, "middle", fill=TEAL)]
    out += [text(270, 335, "R3", 17, 700, "middle", fill=RED)]
    out += [text(120, 365, "R4", 17, 700, "middle", fill=RED)]
    out += [text(45, 450, "f_T(x) = sum_m c_m 1{x in R_m}", 15, 700, cls="math")]
    out += [text(45, 490, "leaf means minimize within-leaf squared error", 15, 650)]
    out += [text(45, 515, "piecewise constants do not extrapolate trends。", 15, fill=MUTED)]

    heading(out, 430, "B", "局部分裂与剪枝", TEAL)
    node(out, 445, 92, 310, 68, "gain = I(parent) - weighted child I", BLUE, size=15)
    out += [line(600, 165, 600, 195, INK, 2.5, marker="a3")]
    node(out, 445, 205, 310, 68, "grow a large tree greedily", TEAL, size=15)
    out += [line(600, 278, 600, 308, INK, 2.5, marker="a3")]
    node(out, 445, 318, 310, 72, "R_alpha(T) = R(T) + alpha |leaves|", RED, size=15)
    out += [line(600, 395, 600, 425, INK, 2.5, marker="a3")]
    node(out, 445, 435, 310, 55, "CV chooses subtree / alpha", BLUE, size=15)
    out += [text(430, 515, "greedy growth is not global partition search。", 15, fill=MUTED)]

    heading(out, 830, "C", "不稳定性与选择偏差", RED)
    out += [line(865, 105, 865, 390, GRID, 2), line(1095, 105, 1095, 390, GRID, 2)]
    out += [path("M875 160C930 120 980 180 1085 135", BLUE, 3)]
    out += [path("M875 175C930 215 995 145 1085 195", RED, 3)]
    out += [line(975, 105, 975, 390, TEAL, 3)]
    out += [line(995, 105, 995, 390, RED, 3, "7 6")]
    out += [text(835, 420, "small data change -> different root split", 15, 700, fill=RED)]
    out += [text(835, 460, "many candidate cuts inflate apparent gain", 15, 650)]
    out += [text(835, 495, "leaf frequency is not automatically calibrated", 15, 650)]
    out += [text(835, 515, "importance depends on correlation and protocol。", 15, fill=MUTED)]
    return finish(out, "树的可解释性来自明确 partition；其代价是局部贪心、离散不稳定与 data-dependent selection。")


def ensembles_bagging_boosting():
    out = begin(
        "Bagging、Random Forest 与 Boosting：三种不同的集成机制",
        "Bagging 对 bootstrap perturbations 的 predictors 做平均；random forest 进一步随机化 candidate features 以降低 tree correlation；boosting 则顺序拟合当前 loss 的错误方向。它们不是同一个 bias–variance 口号的三个别名。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Bagging：Bootstrap 平均", BLUE)
    node(out, 55, 90, 285, 55, "training sample S", BLUE, size=16)
    for x in (60, 155, 250):
        out += [line(197, 150, x+42, 195, INK, 2, marker="a3")]
        out += [rect(x, 205, 84, 55, TEAL, BG, 6, 2), text(x+42, 238, "S*", 15, 700, "middle", fill=TEAL)]
        out += [line(x+42, 265, x+42, 300, INK, 2, marker="a3")]
        out += [rect(x, 310, 84, 55, BLUE, BG, 6, 2), text(x+42, 343, "A(S*)", 15, 700, "middle", fill=BLUE)]
    out += [line(102, 370, 197, 410, INK, 2), line(197, 370, 197, 410, INK, 2), line(292, 370, 197, 410, INK, 2)]
    node(out, 85, 420, 225, 58, "average / vote", RED, size=16)
    out += [text(45, 515, "best for unstable base procedures; not universal。", 15, fill=MUTED)]

    heading(out, 430, "B", "Random Forest：去相关", TEAL)
    node(out, 445, 92, 310, 60, "bootstrap observations", BLUE, size=15)
    out += [line(600, 157, 600, 190, INK, 2.5, marker="a3")]
    node(out, 445, 200, 310, 68, "random feature subset at every split", TEAL, size=15)
    out += [line(600, 273, 600, 306, INK, 2.5, marker="a3")]
    node(out, 445, 316, 310, 65, "strong trees + lower correlation", RED, size=15)
    out += [text(430, 425, "B -> infinity removes Monte Carlo error", 15, 700)]
    out += [text(430, 462, "OOB: each point uses trees that excluded it", 15, 650)]
    out += [text(430, 495, "OOB reuse can still overfit hyperparameters", 15, 650)]
    out += [text(430, 515, "more trees do not erase dataset uncertainty。", 15, fill=MUTED)]

    heading(out, 830, "C", "Boosting：序列下降", RED)
    node(out, 845, 92, 285, 55, "current function F_(m-1)", BLUE, size=15)
    out += [line(987, 152, 987, 185, INK, 2.5, marker="a3")]
    node(out, 845, 195, 285, 70, "pseudo-residual = - d loss / dF", RED, size=15)
    out += [line(987, 270, 987, 303, INK, 2.5, marker="a3")]
    node(out, 845, 313, 285, 65, "fit h_m and add nu rho_m h_m", TEAL, size=15)
    out += [text(830, 420, "AdaBoost: exponential loss and reweighting", 15, 650)]
    out += [text(830, 458, "depth, shrinkage, subsampling, stopping", 15, 650)]
    out += [text(830, 495, "training descent is not test-risk descent", 15, 700, fill=RED)]
    out += [text(830, 515, "noise and outliers can dominate late rounds。", 15, fill=MUTED)]
    return finish(out, "并行平均降低随机扰动，特征随机化改变相关性，顺序加法模型逼近 loss descent。")


FIGURES = {
    "fig-svm-margin-dual-kernel-v2.svg": svm_margin_kernel,
    "fig-krr-gp-shared-mean-contract-v2.svg": krr_gp_interface,
    "fig-decision-tree-split-pruning-v2.svg": decision_tree_pruning,
    "fig-ensemble-bagging-forest-boosting-v2.svg": ensembles_bagging_boosting,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
