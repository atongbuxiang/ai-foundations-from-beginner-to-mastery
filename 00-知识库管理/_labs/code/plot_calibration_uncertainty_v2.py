#!/usr/bin/env python3
"""Generate LT-61--64 paper-ink figures for calibration and uncertainty."""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def calibration_contract():
    out = begin(
        "概率校准：总体对象、Proper Risk 与有限样本决策",
        "校准是条件频率等式；proper loss同时奖励诚实概率与分辨率；可靠性图、ECE和temperature scaling只是数据依赖的估计与后处理。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先声明 Calibration 对象", BLUE)
    node(out, 55, 92, 300, 58, "full Q(x) in probability simplex", BLUE, size=15)
    out += [line(205, 155, 205, 188, INK, 2.5, marker="a3")]
    node(out, 55, 198, 140, 58, "top label", TEAL, size=15)
    node(out, 215, 198, 140, 58, "confidence", TEAL, size=15)
    out += [text(45, 310, "strong: P(Y=k | Q) = Q_k", 15, 700)]
    out += [text(45, 350, "classwise: P(Y=k | Q_k=p) = p", 15, 650)]
    out += [text(45, 390, "top-label: P(correct | C=p) = p", 15, 650)]
    out += [text(45, 442, "strong => classwise / top-label", 15, 700, fill=TEAL)]
    out += [text(45, 482, "accuracy does not imply calibration", 15, 650)]
    out += [text(45, 515, "an ECE number is not the definition。", 15, fill=MUTED)]

    heading(out, 430, "B", "Proper Loss 约束诚实概率", TEAL)
    node(out, 445, 92, 310, 58, "log regret = KL(p || q)", BLUE, size=16)
    node(out, 445, 176, 310, 58, "Brier regret = ||p - q||^2", TEAL, size=16)
    out += [line(600, 239, 600, 270, INK, 2.5, marker="a3")]
    node(out, 445, 280, 310, 76, "Brier = reliability - resolution + uncertainty", RED, size=15)
    out += [text(430, 408, "calibrated constant predictor can be unsharp", 15, 700)]
    out += [text(430, 448, "different proper losses value errors differently", 15, 650)]
    out += [text(430, 488, "population optimum != finite fitted model", 15, 650)]
    out += [text(430, 515, "report probability quality on several axes。", 15, fill=MUTED)]

    heading(out, 830, "C", "估计、后处理、行动分开", RED)
    out += [line(865, 300, 865, 105, GRID, 2), line(865, 300, 1115, 300, GRID, 2)]
    out += [line(875, 290, 1100, 115, TEAL, 3)]
    for x, y, c in ((900, 270, RED), (945, 232, BLUE), (995, 205, RED), (1045, 155, BLUE), (1090, 132, TEAL)):
        out.append(circle(x, y, 6, c, c, 2))
    out += [text(880, 330, "reliability bins need counts + intervals", 15, 650)]
    out += [text(830, 378, "fit T on calibration: softmax(z / T)", 15, 700)]
    out += [text(830, 418, "lock selection before final test", 15, 650)]
    out += [text(830, 458, "decision threshold comes from costs", 15, 650)]
    out += [text(830, 495, "monitor group, time and deployment shift", 15, 650)]
    out += [text(830, 515, "source calibration is not shift immunity。", 15, fill=MUTED)]
    return finish(out, "校准先定义条件频率，再用proper risk与独立数据估计；概率只有进入成本和shift合同后才成为可靠行动依据。")


def uncertainty_layers():
    out = begin(
        "不确定性：信息集、层级分解与可证伪评价",
        "aleatoric和epistemic只在已声明的信息集与层级模型下有精确含义；likelihood错设、推断近似和分布偏移不能被一个方差或熵数字自动覆盖。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一事件，不同信息状态", BLUE)
    node(out, 55, 92, 300, 58, "Y | X : unresolved variation", BLUE, size=16)
    out += [line(205, 155, 205, 188, INK, 2.5, marker="a3")]
    node(out, 55, 198, 300, 58, "Y | X,Z : better sensor / information", TEAL, size=15)
    out += [text(45, 310, "aleatoric is conditional on what is observed", 15, 700)]
    out += [text(45, 350, "epistemic belongs to an agent + model state", 15, 650)]
    out += [text(45, 398, "parameter / function / model-form", 15, 650)]
    out += [text(45, 438, "approximation / optimization / shift", 15, 650)]
    out += [text(45, 482, "different causes require different remedies", 15, 650)]
    out += [text(45, 515, "uncertainty has no context-free scalar。", 15, fill=MUTED)]

    heading(out, 430, "B", "两个精确但条件化的分解", TEAL)
    node(out, 445, 92, 310, 72, "total variance = E[variance] + Var[mean]", BLUE, size=15)
    out += [text(455, 205, "within-model", 15, 700, fill=BLUE)]
    out += [text(645, 205, "between-model", 15, 700, fill=TEAL)]
    out += [line(500, 225, 500, 275, BLUE, 8), line(690, 225, 690, 315, TEAL, 8)]
    node(out, 445, 338, 310, 68, "H(mean p) = E H(p_theta) + I(Y;theta)", TEAL, size=15)
    out += [text(430, 452, "identity is exact for the declared hierarchy", 15, 700)]
    out += [text(430, 490, "semantic labels are model/measure dependent", 15, 650)]
    out += [text(430, 515, "MI is disagreement, not a universal truth。", 15, fill=MUTED)]

    heading(out, 830, "C", "三道遗漏检查", RED)
    node(out, 845, 92, 285, 58, "likelihood / label misspecification", RED, size=15)
    node(out, 845, 176, 285, 58, "posterior / ensemble approximation", BLUE, size=15)
    node(out, 845, 260, 285, 58, "support gap / deployment shift", TEAL, size=15)
    out += [text(830, 362, "evaluate proper score + calibration", 15, 700)]
    out += [text(830, 402, "coverage + width / set size", 15, 650)]
    out += [text(830, 442, "risk-coverage + decision utility", 15, 650)]
    out += [text(830, 482, "stratify by group, time and severity", 15, 650)]
    out += [text(830, 515, "OOD is not synonymous with epistemic。", 15, fill=MUTED)]
    return finish(out, "先固定预测对象和信息集，再解释分解项；任何uncertainty方法最终都要接受校准、coverage、shift和行动价值检验。")


def posterior_approximations():
    out = begin(
        "Posterior Predictive：成员生成、概率混合与三类误差",
        "精确目标是likelihood对posterior的积分；MC dropout、SWAG和deep ensemble产生成员的机制不同；增加成员主要减少既定近似分布下的Monte Carlo误差。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Bayesian 目标链", BLUE)
    node(out, 55, 92, 130, 54, "prior p(theta)", BLUE, size=15)
    node(out, 225, 92, 130, 54, "likelihood", TEAL, size=15)
    out += [line(120, 151, 205, 205, INK, 2), line(290, 151, 205, 205, INK, 2)]
    node(out, 55, 215, 300, 58, "posterior p(theta | D)", BLUE, size=16)
    out += [line(205, 278, 205, 309, INK, 2.5, marker="a3")]
    node(out, 55, 319, 300, 72, "posterior predictive integral", TEAL, size=15)
    out += [text(45, 440, "parameter mean plug-in is a different object", 15, 700)]
    out += [text(45, 480, "function symmetries can collapse parameter modes", 15, 650)]
    out += [text(45, 515, "average predictions before interpreting spread。", 15, fill=MUTED)]

    heading(out, 430, "B", "成员来自不同机制", TEAL)
    node(out, 445, 92, 145, 58, "MC dropout masks", BLUE, size=15)
    node(out, 610, 92, 145, 58, "SWAG trajectory", TEAL, size=15)
    node(out, 445, 184, 145, 58, "deep ensemble", RED, size=15)
    node(out, 610, 184, 145, 58, "bootstrap / VI", BLUE, size=15)
    out += [line(600, 257, 600, 292, INK, 2.5, marker="a3")]
    node(out, 445, 302, 310, 62, "probability mixture: mean_m p_m(y|x)", TEAL, size=15)
    out += [text(430, 414, "probability average != logit average", 15, 700)]
    out += [text(430, 454, "members may be correlated or misspecified", 15, 650)]
    out += [text(430, 492, "report strongest member and total compute", 15, 650)]
    out += [text(430, 515, "ensemble is not automatically posterior。", 15, fill=MUTED)]

    heading(out, 830, "C", "误差不能用 Members 数混掉", RED)
    node(out, 845, 92, 285, 56, "1  MC integration error ~ 1/sqrt(M)", TEAL, size=15)
    out += [line(987, 153, 987, 177, INK, 2, marker="a3")]
    node(out, 845, 184, 285, 56, "2  posterior approximation q != p", BLUE, size=15)
    out += [line(987, 245, 987, 269, INK, 2, marker="a3")]
    node(out, 845, 276, 285, 56, "3  model misspecification / shift", RED, size=15)
    out += [text(830, 382, "more samples directly reduce only account 1", 15, 700)]
    out += [text(830, 422, "correlation lowers effective member count", 15, 650)]
    out += [text(830, 462, "audit NLL, Brier, calibration and abstention", 15, 650)]
    out += [text(830, 500, "evaluate along real shift-severity curves", 15, 650)]
    out += [text(830, 520, "clean performance is not deployment trust。", 15, fill=MUTED)]
    return finish(out, "只有先说明成员从哪里来，predictive mixture才可解释；M、近似偏差、模型错设与shift必须进入四个独立账户。")


def conformal_ranks():
    out = begin(
        "Split Conformal：交换秩、集合形状与 Coverage 量词",
        "proper training固定score，untouched calibration提供order statistic，future score凭exchangeability获得有限样本marginal coverage；集合效率和条件覆盖是额外目标。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "保证来自 m+1 个交换位置", BLUE)
    node(out, 55, 92, 300, 54, "proper train -> fixed score s(x,y)", BLUE, size=15)
    out += [line(205, 151, 205, 180, INK, 2.5, marker="a3")]
    node(out, 55, 190, 300, 54, "m untouched calibration scores", TEAL, size=15)
    out += [text(45, 285, "k = ceil((m+1)(1-alpha))", 16, 700)]
    for i, (x, h) in enumerate(((65, 28), (100, 42), (135, 42), (170, 60), (205, 75), (240, 96), (275, 112), (310, 145))):
        out.append(line(x, 465, x, 465-h, BLUE if i < 7 else RED, 8))
    out += [text(45, 495, "future rank uniform without ties", 15, 650)]
    out += [text(45, 515, "ties enter conservatively with <=。", 15, fill=MUTED)]

    heading(out, 430, "B", "同一 Rank，多个集合形状", TEAL)
    node(out, 445, 92, 310, 58, "residual: f(x) +/- q_hat", BLUE, size=15)
    node(out, 445, 176, 310, 58, "normalized: local scale x q_hat", TEAL, size=15)
    node(out, 445, 260, 310, 58, "CQR: [q_lo-q_hat, q_hi+q_hat]", RED, size=15)
    node(out, 445, 344, 310, 58, "classification: score-threshold label set", BLUE, size=15)
    out += [text(430, 452, "base model quality mainly changes efficiency", 15, 700)]
    out += [text(430, 490, "report length, set size, empty/full rates", 15, 650)]
    out += [text(430, 515, "coverage alone admits the full label space。", 15, fill=MUTED)]

    heading(out, 830, "C", "Coverage Claim 的四道门", RED)
    node(out, 845, 92, 285, 56, "marginal != pointwise conditional", RED, size=15)
    node(out, 845, 174, 285, 56, "exchangeable unit: patient / session", BLUE, size=15)
    node(out, 845, 256, 285, 56, "no adaptive calibration reuse", TEAL, size=15)
    node(out, 845, 338, 285, 56, "shift breaks rank symmetry", RED, size=15)
    out += [text(830, 438, "group and simultaneous events are stronger", 15, 700)]
    out += [text(830, 478, "weighted/online variants need new assumptions", 15, 650)]
    out += [text(830, 515, "distribution-free does not mean shift-free。", 15, fill=MUTED)]
    return finish(out, "Conformal的有限样本力量来自交换秩而非基础模型正确；量词、数据复用、依赖与效率决定最终结论能走多远。")


FIGURES = {
    "fig-calibration-proper-score-v2.svg": calibration_contract,
    "fig-aleatoric-epistemic-v2.svg": uncertainty_layers,
    "fig-posterior-ensemble-approx-v2.svg": posterior_approximations,
    "fig-conformal-rank-coverage-v2.svg": conformal_ranks,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
