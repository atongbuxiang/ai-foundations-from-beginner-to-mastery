#!/usr/bin/env python3
"""Generate v2 textbook figures for PROB-14--17.

The figures are deterministic, use only the Python standard library, and share
the repository's restrained paper-ink visual grammar.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER,
    BG,
    BLUE,
    GRID,
    INK,
    MUTED,
    RED,
    TEAL,
    begin,
    circle,
    finish,
    heading,
    line,
    node,
    path,
    text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "probability"


def polyline(points, color, width=2.5, dash=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, color, width, "none", dash)


def gaussian_curve(x0, x1, baseline, center, scale, height):
    pts = []
    for i in range(101):
        x = x0 + (x1 - x0) * i / 100
        y = baseline - height * math.exp(-0.5 * ((x - center) / scale) ** 2)
        pts.append((x, y))
    return pts


def monte_carlo():
    out = begin(
        "Monte Carlo 的平均、重要性权重与方差设计",
        "简单 Monte Carlo 的误差由被积函数方差决定；重要性采样要求支持覆盖并诊断权重集中；control variate 通过相关辅助量削减残差方差。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "样本平均：误差按平方根缩小", BLUE)
    for i, lab in enumerate(("f1", "f2", "f3", "...", "fn")):
        x = 48 + i * 66
        node(out, x, 115, 48, 44, lab, BLUE, size=15)
        out.append(line(x + 24, 161, 200, 220, GRID, 2))
    node(out, 92, 222, 216, 62, "mu_hat = (1/n) sum fi", TEAL, size=16)
    out += [
        text(45, 340, "E[mu_hat]=mu", 17, 650, cls="math"),
        text(45, 378, "SE(mu_hat)=sigma_f/sqrt(n)", 17, 650, cls="math"),
        text(45, 422, "误差减半  ->  样本预算约乘 4", 17, 650, fill=RED),
        text(45, 460, "前提：iid 与有限二阶矩；一次运行仍会波动。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "重要性采样：覆盖比 ESS 更先", TEAL)
    out += [line(440, 345, 770, 345, GRID, 2), line(455, 365, 455, 105, GRID, 2)]
    p = gaussian_curve(455, 760, 345, 575, 67, 205)
    q = gaussian_curve(455, 760, 345, 625, 45, 165)
    out += [polyline(p, BLUE, 3), polyline(q, TEAL, 3, "8 5")]
    out += [
        text(535, 145, "target p", 15, 700, fill=BLUE),
        text(650, 215, "proposal q", 15, 700, fill=TEAL),
        circle(490, 318, 6, RED, RED),
        text(500, 312, "q 很小 -> w=p/q 很大", 15, 650, fill=RED),
        text(430, 405, "mu = E_q[w f]", 17, 650, cls="math"),
        text(430, 440, "ESS = (sum w)^2 / sum w^2", 16, 650, cls="math"),
        text(430, 475, "ESS 只看权重集中，不是误差证书。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "Control variate：削减残差方差", RED)
    out += [line(845, 370, 1145, 370, GRID, 2), line(870, 400, 870, 105, GRID, 2)]
    pts = [(890, 330), (925, 315), (955, 280), (990, 275), (1020, 235), (1060, 225), (1095, 185), (1120, 175)]
    out.append(line(882, 340, 1130, 160, TEAL, 3))
    for i, (x, y) in enumerate(pts):
        out.append(line(x, y, x, 340 - 0.73 * (x - 882), GRID, 1.5, "4 4"))
        out.append(circle(x, y, 5, BLUE if i % 2 == 0 else RED, BG, 2))
    out += [
        text(855, 126, "f(X)", 15, 650),
        text(1128, 395, "h(X)", 15, 650),
        text(830, 430, "f_cv = f - beta(h-Eh)", 17, 650, cls="math"),
        text(830, 466, "beta* = Cov(f,h)/Var(h)", 16, 650, cls="math"),
        text(830, 500, "减掉可预测部分；代价是 Eh 必须已知。", 15, fill=MUTED),
    ]
    return finish(out, "Monte Carlo 可信度来自误差预算、支持与尾部诊断，而不是只报告样本数。")


def statistical_model():
    out = begin(
        "统计模型、估计器、重复抽样与风险",
        "参数索引数据分布；估计器把随机数据映射为动作；重复抽样产生 sampling distribution；损失的期望才定义 risk。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "模型先规定数据怎样随机", BLUE)
    node(out, 55, 105, 110, 52, "theta 固定", BLUE, size=16)
    node(out, 220, 105, 130, 52, "P_theta", TEAL, size=17)
    out += [line(168, 131, 215, 131, INK, 2.5, marker="a3")]
    for i, lab in enumerate(("X^(1)", "X^(2)", "X^(3)")):
        y = 215 + i * 78
        node(out, 165, y, 150, 48, lab, BLUE, size=16)
        out.append(line(285, 160, 240, y - 3, GRID, 2, marker="a3"))
    out += [text(45, 472, "同一 theta 下，重复样本仍不同。", 16, fill=MUTED)]

    heading(out, 430, "B", "估计器把每份数据映成一个点", TEAL)
    for i, y in enumerate((112, 196, 280)):
        node(out, 435, y, 98, 46, f"X^({i+1})", BLUE, size=15)
        node(out, 650, y, 110, 46, f"theta_hat{i+1}", TEAL, size=15)
        out.append(line(536, y + 23, 645, y + 23, INK, 2.2, marker="a3"))
    out += [line(445, 405, 755, 405, GRID, 2)]
    for x in (590, 625, 658, 690, 715):
        out.append(circle(x, 405, 5, TEAL, TEAL))
    out += [text(600, 442, "sampling distribution of theta_hat", 15, 650, "middle"), text(430, 477, "一次估计值不是估计器的全部表现。", 15, fill=MUTED)]

    heading(out, 830, "C", "Loss 局部计分，risk 重复平均", RED)
    out += [line(850, 260, 1140, 260, GRID, 2)]
    out += [circle(x, 260, 5, BLUE, BLUE) for x in (930, 950, 970, 995, 1015, 1040, 1060)]
    out += [
        line(900, 225, 900, 295, RED, 3),
        line(995, 225, 995, 295, TEAL, 3),
        text(900, 214, "theta", 15, 700, "middle", RED),
        text(995, 214, "E[theta_hat]", 15, 700, "middle", TEAL),
        line(903, 320, 992, 320, RED, 2.5),
        text(947, 346, "bias", 15, 700, "middle", RED),
        text(830, 400, "R(theta,T)=E_theta[L(theta,T(X))]", 16, 650, cls="math"),
        text(830, 440, "MSE = variance + bias^2", 17, 650, cls="math"),
        text(830, 480, "错设模型会让风险精确回答错误目标。", 15, fill=MUTED),
    ]
    return finish(out, "数据、参数、估计器、sampling distribution 与 risk 是五层对象，不能互相替代。")


def mle_map():
    out = begin(
        "MLE、MAP、后验 mode 与参数坐标",
        "固定参数时密度在数据空间归一化；固定数据时 likelihood 只表达参数间相对支持；prior 改变 posterior，而 MAP 只保留一个且依赖坐标的 mode。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一 p(x|theta)，两种阅读", BLUE)
    out += [line(55, 245, 355, 245, GRID, 2), line(70, 270, 70, 90, GRID, 2)]
    dens = gaussian_curve(70, 345, 245, 190, 48, 130)
    out.append(polyline(dens, BLUE, 3))
    out += [
        text(215, 110, "固定 theta：x 变化", 16, 700, "middle", BLUE),
        text(215, 290, "integral_x p(x|theta) dx = 1", 16, 650, "middle", cls="math"),
        line(55, 390, 355, 390, GRID, 2),
        path("M70 390C125 360 150 230 220 250C280 268 305 330 345 350", TEAL, 3),
        text(215, 338, "固定 x_obs：theta 变化", 16, 700, "middle", TEAL),
        text(45, 470, "L(theta;x_obs) 只需相对比较，不是参数概率。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "Prior 改变 posterior", TEAL)
    out += [line(445, 365, 770, 365, GRID, 2), line(460, 390, 460, 95, GRID, 2)]
    like = gaussian_curve(460, 760, 365, 650, 55, 190)
    prior = gaussian_curve(460, 760, 365, 535, 65, 115)
    post = gaussian_curve(460, 760, 365, 610, 42, 220)
    out += [polyline(like, BLUE, 2.5, "8 5"), polyline(prior, TEAL, 2.5, "4 5"), polyline(post, RED, 3)]
    out += [
        text(686, 205, "likelihood", 15, 700, fill=BLUE),
        text(500, 245, "prior", 15, 700, fill=TEAL),
        text(620, 120, "posterior", 15, 700, fill=RED),
        line(650, 365, 650, 170, BLUE, 2, "5 4"),
        line(610, 365, 610, 145, RED, 2, "5 4"),
        text(650, 405, "MLE", 15, 700, "middle", BLUE),
        text(610, 435, "MAP", 15, 700, "middle", RED),
        text(430, 480, "posterior ∝ likelihood × prior", 16, 650, cls="math"),
    ]

    heading(out, 830, "C", "Mode 丢掉宽度与多峰", RED)
    out += [line(840, 305, 1140, 305, GRID, 2), line(855, 330, 855, 90, GRID, 2)]
    pts = []
    for i in range(101):
        x = 855 + 2.75 * i
        y = 305 - 125 * math.exp(-0.5 * ((x - 935) / 32) ** 2) - 185 * math.exp(-0.5 * ((x - 1060) / 42) ** 2)
        pts.append((x, y))
    out += [polyline(pts, RED, 3), circle(1060, 120, 7, RED, RED), text(1060, 105, "MAP", 15, 700, "middle", RED)]
    out += [
        text(830, 365, "theta -> phi=g(theta): density gains Jacobian", 16, 650, cls="math"),
        text(830, 405, "mode generally does not transform equivariantly", 15, 650),
        text(830, 445, "点估计不保存宽度、相关性或另一峰。", 15, fill=MUTED),
        text(830, 480, "“penalty = prior”还需尺度与参数化对齐。", 15, fill=MUTED),
    ]
    return finish(out, "MLE 与 MAP 都是优化得到的点；likelihood、posterior 与不确定性是更丰富的对象。")


def bernoulli_computation_inference_bridge():
    out = begin(
        "同一个 Bernoulli 平均：有限样本、概率计算与参数推断",
        "共同成功指标 Y 的样本平均可被浓缩界控制；已知目标分布时可设计 importance proposal；未知参数时则用 sampling risk、likelihood 与 posterior 评价。",
        (BLUE, TEAL, AMBER),
    )

    heading(out, 42, "A", "有限样本：失败概率合同", BLUE)
    node(out, 52, 98, 300, 58, "Y_i ~ Bernoulli(3/10)", BLUE, size=17)
    out += [line(202, 158, 202, 198, INK, 2.3, marker="a3")]
    node(out, 52, 208, 300, 60, "q_hat = (1/n) sum Y_i", TEAL, size=17)
    out += [
        text(45, 325, "n=50, epsilon=1/5", 16, 700),
        text(45, 366, "Chebyshev: 21/200 = 0.105", 16, 650, fill=RED, cls="math"),
        text(45, 405, "Hoeffding: 2 exp(-4) = 0.0366", 16, 650, fill=TEAL, cls="math"),
        text(45, 447, "delta=0.05  ->  n >= 47 is sufficient", 15, 700, fill=BLUE),
        text(45, 484, "上界不是精确尾概率，也不是渐近正态近似。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "概率计算：proposal 决定方差", TEAL)
    rows = (
        (105, "direct p: r=3/10", "variance 21/100", BLUE),
        (220, "good proposal: r=3/4", "variance 3/100", TEAL),
        (335, "bad proposal: r=1/20", "variance 171/100", RED),
    )
    for y, label, variance, color in rows:
        node(out, 440, y, 315, 64, label, color, size=16)
        out.append(text(598, y + 92, variance, 16, 700, "middle", color, "math"))
    out += [
        text(440, 475, "good weights: w(1)=2/5; w(0)=14/5", 15, 650, cls="math"),
        text(440, 505, "support first; ESS alone cannot certify f-specific error", 14, fill=MUTED),
    ]

    heading(out, 830, "C", "参数推断：likelihood 与 risk", AMBER)
    node(out, 840, 96, 300, 58, "observed n=10, K=3", BLUE, size=17)
    out += [line(990, 156, 990, 196, INK, 2.3, marker="a3")]
    node(out, 840, 206, 140, 62, "MLE = 3/10", TEAL, size=17)
    node(out, 1000, 206, 140, 62, "prior Beta(2,2)", AMBER, size=15)
    out += [line(1070, 270, 1070, 310, INK, 2.3, marker="a3")]
    node(out, 840, 320, 300, 66, "posterior Beta(5,9)", AMBER, size=17)
    out += [
        text(840, 430, "MAP=1/3; posterior mean=5/14", 16, 700, cls="math"),
        text(840, 468, "at q=3/10: shrinkage MSE < MLE MSE", 15, 650, fill=TEAL),
        text(840, 502, "积分难算与参数未知不是同一种未知。", 15, fill=MUTED),
    ]
    return finish(
        out,
        "先声明概率合同：界控制随机偏差，Monte Carlo 设计采样，统计推断则在未知参数下评价数据程序。",
    )


def fisher_information():
    out = begin(
        "Score、Fisher 信息、Cramér–Rao 与 MLE 渐近链",
        "正则模型中 score 均值为零，Fisher 信息是 score 二阶矩与期望曲率；它给无偏估计下界，并通过 score CLT 与 Hessian LLN 决定 MLE 一阶渐近协方差。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Score 随数据变，Fisher 再平均", BLUE)
    out += [line(55, 240, 355, 240, GRID, 2), line(205, 205, 205, 275, INK, 2)]
    scores = (-115, -80, -48, -20, 15, 42, 73, 105)
    for i, s in enumerate(scores):
        out.append(circle(205 + s, 240, 5, BLUE if i < 4 else TEAL, BG, 2))
    out += [
        text(205, 195, "E[s_theta(X)]=0", 17, 700, "middle", cls="math"),
        text(45, 325, "I(theta)=E[s s^T]", 17, 650, cls="math"),
        text(45, 365, "= -E[ Hessian log p_theta(X) ]", 16, 650, cls="math"),
        text(45, 415, "observed 随样本变；Fisher 是总体平均。", 15, fill=MUTED),
        text(45, 458, "等式需要固定支持与微分—积分可交换。", 15, fill=RED),
    ]

    heading(out, 430, "B", "CRLB：只在声明的类别内比较", TEAL)
    out += [line(445, 355, 770, 355, GRID, 2), line(460, 380, 460, 95, GRID, 2)]
    wide = gaussian_curve(460, 760, 355, 610, 70, 150)
    narrow = gaussian_curve(460, 760, 355, 610, 39, 230)
    out += [polyline(wide, BLUE, 2.5), polyline(narrow, TEAL, 3)]
    out += [
        text(690, 260, "larger variance", 15, 700, fill=BLUE),
        text(625, 105, "efficient boundary", 15, 700, fill=TEAL),
        text(430, 405, "Var(T) >= [g'(theta)]^2 / (n I(theta))", 16, 650, cls="math"),
        text(430, 445, "标量式：无偏、正则、有限信息。", 15, fill=MUTED),
        text(430, 480, "有偏估计可用偏差换更小 MSE。", 15, fill=RED),
    ]

    heading(out, 830, "C", "MLE 渐近正态性是一条证明链", RED)
    steps = (
        ("score CLT", BLUE),
        ("Hessian / n -> -I", TEAL),
        ("Taylor at theta0", RED),
        ("sqrt(n)(theta_hat-theta0)", BLUE),
    )
    for i, (lab, color) in enumerate(steps):
        y = 96 + i * 88
        node(out, 845, y, 280, 54, lab, color, size=16)
        if i < len(steps) - 1:
            out.append(line(985, y + 56, 985, y + 82, INK, 2.2, marker="a3"))
    out += [
        text(970, 452, "-> N(0, I^-1)", 17, 700, "middle", RED, "math"),
        text(830, 490, "还需一致性、内点真值、非奇异信息与余项控制。", 15, fill=MUTED),
    ]
    return finish(out, "Fisher 理论是正则局部模型的精密结论；边界、奇异与不可辨识会改变整条链。")


def validate_bernoulli_computation_inference_example():
    """Exact and deterministic gate for the shared PROB-13—16 example."""
    q = Fraction(3, 10)
    variance = q * (1 - q)
    assert variance == Fraction(21, 100)

    n_bound = 50
    epsilon = Fraction(1, 5)
    chebyshev = variance / (n_bound * epsilon * epsilon)
    hoeffding = 2 * math.exp(-2 * n_bound * float(epsilon * epsilon))
    required = math.ceil(math.log(2 / 0.05) / (2 * float(epsilon * epsilon)))
    selected_required = math.ceil(math.log(2 * 100 / 0.05) / (2 * float(epsilon * epsilon)))
    assert chebyshev == Fraction(21, 200)
    assert abs(hoeffding - 2 * math.exp(-4)) < 1e-15
    assert hoeffding < 0.05
    assert required == 47
    assert selected_required == 104

    proposal = Fraction(3, 4)
    w_one = q / proposal
    w_zero = (1 - q) / (1 - proposal)
    is_mean = proposal * w_one
    is_variance = proposal * w_one * w_one - q * q
    weight_second_moment = proposal * w_one * w_one + (1 - proposal) * w_zero * w_zero
    assert w_one == Fraction(2, 5)
    assert w_zero == Fraction(14, 5)
    assert is_mean == q
    assert is_variance == Fraction(3, 100)
    assert variance / is_variance == 7
    assert weight_second_moment == Fraction(52, 25)
    assert 1 / weight_second_moment == Fraction(25, 52)

    bad_proposal = Fraction(1, 20)
    bad_w_one = q / bad_proposal
    bad_variance = bad_proposal * bad_w_one * bad_w_one - q * q
    assert bad_w_one == 6
    assert bad_variance == Fraction(171, 100)

    n = 10
    k = 3
    mle = Fraction(k, n)
    map_estimate = Fraction(k + 1, n + 2)
    posterior_mean = Fraction(k + 2, n + 4)
    mle_risk = variance / n
    shrink_bias = Fraction(1 - 2 * q, n + 2)
    shrink_variance = n * variance / (n + 2) ** 2
    shrink_risk = shrink_variance + shrink_bias * shrink_bias
    assert mle == Fraction(3, 10)
    assert map_estimate == Fraction(1, 3)
    assert posterior_mean == Fraction(5, 14)
    assert shrink_bias == Fraction(1, 30)
    assert mle_risk == Fraction(21, 1000)
    assert shrink_risk == Fraction(113, 7200)
    assert shrink_risk < mle_risk
    assert Fraction(1, (n + 2) ** 2) > 0
    print("PROB-13—16 exact gate: concentration + IS + risk + MLE/MAP passed")


FIGURES = {
    "fig-monte-carlo-importance-v2.svg": monte_carlo,
    "fig-statistical-model-estimator-risk-v2.svg": statistical_model,
    "fig-mle-map-geometry-v2.svg": mle_map,
    "fig-fisher-crlb-asymptotic-v2.svg": fisher_information,
    "fig-bernoulli-computation-inference-v2.svg": bernoulli_computation_inference_bridge,
}


def main():
    validate_bernoulli_computation_inference_example()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
