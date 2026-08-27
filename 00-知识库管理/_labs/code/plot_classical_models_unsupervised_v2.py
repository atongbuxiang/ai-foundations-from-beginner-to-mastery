#!/usr/bin/env python3
"""Generate LT-49--52 paper-ink figures for unsupervised models and misspecification."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def pca_subspace_risk():
    out = begin(
        "PCA：经验主轴、总体主子空间与谱间隙",
        "PCA在样本上最大化投影方差并最小化正交重构误差；统计问题是经验协方差主子空间能否逼近总体主子空间。误差由协方差扰动与eigengap共同控制，重复特征值时只能识别子空间。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "样本主轴会旋转", BLUE)
    pts = ((85, 335), (115, 300), (145, 305), (175, 255), (205, 245),
           (235, 205), (265, 185), (300, 150), (325, 165), (150, 350))
    for x, y in pts:
        out.append(circle(x, y, 5, BLUE, BLUE, 1))
    out += [line(70, 390, 345, 105, TEAL, 3), line(75, 365, 350, 135, RED, 3, "8 6")]
    out += [text(65, 430, "population axis u1", 15, 700, fill=TEAL)]
    out += [text(65, 466, "sample axis uhat1", 15, 700, fill=RED)]
    out += [text(65, 505, "sign is arbitrary; angle is the object", 15, fill=MUTED)]

    heading(out, 430, "B", "三个等价经验目标", TEAL)
    node(out, 445, 92, 310, 65, "maximize w^T Sigmahat w, ||w||=1", BLUE, size=15)
    out += [line(600, 162, 600, 195, INK, 2.5, marker="a3")]
    node(out, 445, 205, 310, 70, "minimize sum ||x_i - P_U x_i||^2", TEAL, size=15)
    out += [line(600, 280, 600, 313, INK, 2.5, marker="a3")]
    node(out, 445, 323, 310, 70, "top right singular vectors of centered X", RED, size=15)
    out += [text(430, 438, "variance explained = reconstruction accounting", 15, 650)]
    out += [text(430, 475, "centering and scaling define the estimator", 15, 650)]
    out += [text(430, 515, "high variance need not be task-relevant。", 15, fill=MUTED)]

    heading(out, 830, "C", "误差合同：扰动 / Gap", RED)
    node(out, 845, 92, 285, 58, "||Sigmahat - Sigma||_op", BLUE, size=15)
    out += [line(987, 155, 987, 188, INK, 2.5, marker="a3")]
    node(out, 845, 198, 285, 62, "divide by population eigengap", RED, size=15)
    out += [line(987, 265, 987, 298, INK, 2.5, marker="a3")]
    node(out, 845, 308, 285, 64, "sin Theta(Uhat_r, U_r)", TEAL, size=15)
    out += [text(830, 420, "gap = 0: basis directions are not identifiable", 15, 700, fill=RED)]
    out += [text(830, 458, "tails / dependence control covariance error", 15, 650)]
    out += [text(830, 495, "choose r inside the evaluation protocol", 15, 650)]
    out += [text(830, 515, "projection stability is not semantic validity。", 15, fill=MUTED)]
    return finish(out, "PCA先是一个经验谱优化；进入统计学习后，必须报告总体对象、谱间隙、子空间损失与选择协议。")


def kmeans_risk_nonidentifiability():
    out = begin(
        "K-Means：量化风险、Lloyd下降与聚类语义",
        "K-Means优化到最近中心的平方距离；assignment与center updates交替降低经验目标，但只保证到局部固定点。中心集合只定义到排列，低objective也不自动对应外部类别或下游任务。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "中心集定义 Voronoi 分区", BLUE)
    left = ((75, 170), (105, 145), (130, 200), (95, 235), (150, 240))
    right = ((250, 300), (285, 275), (320, 330), (300, 370), (345, 280))
    for x, y in left:
        out.append(circle(x, y, 5, BLUE, BLUE, 1))
    for x, y in right:
        out.append(circle(x, y, 5, RED, RED, 1))
    out += [circle(115, 200, 11, BLUE, BG, 3), circle(300, 310, 11, RED, BG, 3)]
    out += [line(55, 390, 360, 85, TEAL, 3, "8 6")]
    out += [text(45, 430, "R(C)=E min_j ||X-c_j||^2", 16, 700, cls="math")]
    out += [text(45, 470, "nearest-center cells are metric dependent", 15, 650)]
    out += [text(45, 510, "cluster names 1 and 2 can be swapped。", 15, fill=MUTED)]

    heading(out, 430, "B", "Lloyd 是交替局部下降", TEAL)
    node(out, 445, 92, 310, 60, "assign each point to nearest center", BLUE, size=15)
    out += [line(600, 157, 600, 190, INK, 2.5, marker="a3")]
    node(out, 445, 200, 310, 62, "replace each center by cluster mean", TEAL, size=15)
    out += [line(600, 267, 600, 300, INK, 2.5, marker="a3")]
    node(out, 445, 310, 310, 62, "empirical distortion never increases", RED, size=15)
    out += [line(600, 377, 600, 410, INK, 2.5, marker="a3")]
    node(out, 445, 420, 310, 58, "stop at a local fixed point", BLUE, size=15)
    out += [text(430, 515, "seeding and empty-cluster rules change output。", 15, fill=MUTED)]

    heading(out, 830, "C", "三套评价不能混用", RED)
    node(out, 845, 92, 285, 62, "internal: distortion / silhouette", BLUE, size=15)
    out += [line(987, 159, 987, 192, INK, 2.5, marker="a3")]
    node(out, 845, 202, 285, 62, "external: ARI / NMI vs labels", TEAL, size=15)
    out += [line(987, 269, 987, 302, INK, 2.5, marker="a3")]
    node(out, 845, 312, 285, 62, "utility: retrieval / routing outcome", RED, size=15)
    out += [text(830, 420, "K is part of the inductive bias", 15, 700, fill=RED)]
    out += [text(830, 458, "consistency needs a unique population optimum", 15, 650)]
    out += [text(830, 495, "representation shift changes the geometry", 15, 650)]
    out += [text(830, 515, "clustering is not label discovery by default。", 15, fill=MUTED)]
    return finish(out, "K-Means的定理对象是平方距离量化风险；算法收敛、总体相合与语义恢复必须逐层另证。")


def latent_mixture_em():
    out = begin(
        "潜变量、混合模型与 EM：后验责任度到单调似然",
        "潜变量模型通过对Z求和或积分定义observed likelihood。EM在当前参数下构造latent posterior，再最大化expected complete log-likelihood；ELBO/KL恒等式解释单调性，但不保证全局最优或可辨识。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Observed X 隐藏了 Z", BLUE)
    for y, lab, col in ((125, "component 1", BLUE), (225, "component 2", TEAL), (325, "component 3", RED)):
        node(out, 55, y, 135, 55, lab, col, size=15)
        out.append(line(195, y + 28, 250, 250, col, 2.2, marker="a3"))
    node(out, 255, 215, 105, 70, "observed x", RED, size=16)
    out += [text(45, 420, "r_ik = P(Z_i=k | x_i, theta)", 15, 700, cls="math")]
    out += [text(45, 458, "responsibility is a posterior soft assignment", 15, 650)]
    out += [text(45, 495, "Z is model-declared, not directly observed", 15, 650)]
    out += [text(45, 515, "component labels are permutation symmetric。", 15, fill=MUTED)]

    heading(out, 430, "B", "ELBO 恒等式与 E / M", TEAL)
    node(out, 445, 92, 310, 58, "log p = F(q,theta) + KL(q || posterior)", BLUE, size=15)
    out += [line(600, 155, 600, 188, INK, 2.5, marker="a3")]
    node(out, 445, 198, 310, 64, "E: q <- p_(theta_old)(z|x)", TEAL, size=15)
    out += [line(600, 267, 600, 300, INK, 2.5, marker="a3")]
    node(out, 445, 310, 310, 64, "M: theta <- argmax F(q,theta)", RED, size=15)
    out += [line(600, 379, 600, 412, INK, 2.5, marker="a3")]
    node(out, 445, 422, 310, 56, "observed log-likelihood does not decrease", BLUE, size=15)
    out += [text(430, 515, "generalized / approximate EM needs a new contract。", 15, fill=MUTED)]

    heading(out, 830, "C", "单调不等于正确", RED)
    node(out, 845, 92, 285, 58, "local stationary point / initialization", BLUE, size=15)
    node(out, 845, 178, 285, 58, "label switching / quotient symmetry", TEAL, size=15)
    node(out, 845, 264, 285, 58, "variance collapse / no finite MLE", RED, size=15)
    node(out, 845, 350, 285, 58, "weak separation / slow EM", BLUE, size=15)
    out += [text(830, 448, "likelihood convergence != parameter convergence", 15, 700, fill=RED)]
    out += [text(830, 482, "posterior class != causal or semantic class", 15, 650)]
    out += [text(830, 515, "selection and held-out prediction remain separate。", 15, fill=MUTED)]
    return finish(out, "EM是一条对声明模型的坐标上升路线；必须把latent语义、可辨识、奇异性、优化与预测验收分开。")


def identifiability_selection_misspec():
    out = begin(
        "可辨识性、模型选择与错设：参数、分布和预测的分账",
        "可辨识性检查parameter-to-distribution map是否一一；错设时MLE趋向模型族内的KL projection而非真实机制；AIC、BIC与CV对应不同选择目标和条件，不能共享一个无条件最优解释。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "参数 Fiber 与 Quotient", BLUE)
    node(out, 55, 95, 105, 55, "theta_1", BLUE, size=15)
    node(out, 55, 195, 105, 55, "theta_2", TEAL, size=15)
    out += [line(165, 122, 245, 190, BLUE, 2.5, marker="a3"), line(165, 222, 245, 190, TEAL, 2.5, marker="a3")]
    node(out, 250, 155, 105, 70, "same P_theta", RED, size=15)
    out += [text(45, 305, "identifiable: P_theta=P_theta' => theta=theta'", 15, 700, cls="math")]
    out += [text(45, 350, "mixtures: equality only up to permutation", 15, 650)]
    out += [text(45, 390, "neural nets: many parameter symmetries", 15, 650)]
    out += [text(45, 432, "prediction may be identifiable when parameters are not", 15, 650)]
    out += [text(45, 475, "Fisher singularity is an estimation warning", 15, 650)]
    out += [text(45, 515, "choose an invariant target or quotient。", 15, fill=MUTED)]

    heading(out, 430, "B", "错设投影与 Sandwich", TEAL)
    out += [path("M465 360C500 275 560 180 725 125", BLUE, 3)]
    out += [circle(515, 165, 9, RED, RED), text(530, 160, "true P0 outside model", 15, 700, fill=RED)]
    out += [circle(585, 235, 9, TEAL, TEAL), text(600, 230, "P_(theta*) KL projection", 15, 700, fill=TEAL)]
    out += [line(520, 172, 580, 228, RED, 2, "7 6", "a2")]
    out += [text(430, 410, "theta* = argmin KL(P0 || P_theta)", 15, 700, cls="math")]
    out += [text(430, 452, "asymptotic covariance = H^-1 J H^-1", 15, 650, cls="math")]
    out += [text(430, 488, "correct model often gives H=J", 15, 650)]
    out += [text(430, 515, "in-distribution projection is not shift robustness。", 15, fill=MUTED)]

    heading(out, 830, "C", "选择准则优化不同目标", RED)
    node(out, 845, 92, 285, 62, "AIC: -2 log L + 2d  | prediction", BLUE, size=15)
    node(out, 845, 180, 285, 62, "BIC: -2 log L + d log n | evidence", TEAL, size=15)
    node(out, 845, 268, 285, 62, "CV: held-out loss | declared split", RED, size=15)
    out += [text(830, 382, "regular dimension formulas fail in singular models", 15, 700, fill=RED)]
    out += [text(830, 420, "candidate search creates additional optimism", 15, 650)]
    out += [text(830, 458, "selection is not post-selection inference", 15, 650)]
    out += [text(830, 495, "deployment utility may differ from likelihood", 15, 650)]
    out += [text(830, 515, "there is no target-free best criterion。", 15, fill=MUTED)]
    return finish(out, "先声明要识别的对象与选择目标；再判断模型正确性、正则条件、数据复用和部署分布。")


FIGURES = {
    "fig-pca-subspace-risk-v2.svg": pca_subspace_risk,
    "fig-kmeans-risk-nonidentifiability-v2.svg": kmeans_risk_nonidentifiability,
    "fig-latent-mixture-em-v2.svg": latent_mixture_em,
    "fig-identifiability-selection-misspecification-v2.svg": identifiability_selection_misspec,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
