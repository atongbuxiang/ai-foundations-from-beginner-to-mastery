#!/usr/bin/env python3
"""Generate v2 textbook figures for PROB-18--20."""

from __future__ import annotations

import math
import random
import statistics
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


def normal_points(x0, x1, baseline, center, scale, height):
    points = []
    for i in range(121):
        x = x0 + (x1 - x0) * i / 120
        y = baseline - height * math.exp(-0.5 * ((x - center) / scale) ** 2)
        points.append((x, y))
    return points


def bayesian():
    out = begin(
        "Bayesian 联合模型、条件更新与后验预测",
        "联合模型先生成参数与数据；观测后通过 evidence 归一化得到 posterior；未来预测对 posterior 参数不确定性积分，并需与模型检查和外部验证区分。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先写联合模型，再条件化", BLUE)
    node(out, 60, 105, 125, 54, "Theta ~ prior", BLUE, size=16)
    node(out, 245, 105, 105, 54, "Y | Theta", TEAL, size=16)
    out += [line(188, 132, 240, 132, INK, 2.5, marker="a3"), text(215, 112, "likelihood", 15, 650, "middle")]
    node(out, 148, 235, 160, 60, "observe Y=y", RED, size=16)
    out += [line(297, 162, 245, 230, RED, 2.5, marker="a2")]
    node(out, 70, 365, 280, 62, "posterior p(Theta|y)", TEAL, size=17)
    out += [line(228, 298, 210, 358, RED, 2.5, marker="a2")]
    out += [
        text(45, 326, "p(theta,y)=p(theta)p(y|theta)", 16, 650, cls="math"),
        text(45, 470, "evidence p(y) 必须有限；支持必须匹配。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "预测要积分参数不确定性", TEAL)
    node(out, 440, 105, 125, 52, "Theta^(s)|y", TEAL, size=16)
    node(out, 650, 105, 110, 52, "Y_new^(s)", BLUE, size=16)
    out += [line(568, 131, 645, 131, INK, 2.5, marker="a3")]
    for i, (x, y) in enumerate(((480, 235), (535, 255), (590, 220), (645, 275), (700, 240))):
        out.append(circle(x, y, 7, BLUE if i % 2 == 0 else TEAL, BG, 2.5))
    out += [
        line(455, 310, 750, 310, GRID, 2),
        text(600, 345, "posterior predictive samples", 15, 650, "middle"),
        text(430, 385, "p(y_new|y) = integral p(y_new|theta)", 15, 650, cls="math"),
        text(430, 415, "                  p(theta|y) dtheta", 15, 650, cls="math"),
        text(430, 455, "total variance = aleatoric + parameter uncertainty", 15, 650),
        text(430, 490, "plug-in p(y_new|theta_hat) 会丢掉后一项。", 15, fill=RED),
    ]

    heading(out, 830, "C", "检查与验证回答不同问题", RED)
    rows = (
        ("prior predictive", "数据前：生成范围？", BLUE),
        ("posterior predictive", "给定数据：能复现？", TEAL),
        ("held-out evaluation", "新数据：能外推？", RED),
    )
    for i, (label, question, color) in enumerate(rows):
        y = 105 + i * 112
        node(out, 835, y, 150, 50, label, color, size=15)
        out.append(line(988, y + 25, 1020, y + 25, INK, 2.2, marker="a3"))
        out.append(text(1030, y + 31, question, 15, 650))
    out += [
        text(830, 450, "Posterior 概率始终条件于模型与已观测数据。", 15, fill=MUTED),
        text(830, 485, "PPC 不是 held-out generalization 证书。", 15, fill=RED),
    ]
    return finish(out, "Bayesian 推断从联合模型出发；更新、预测、检查与决策必须保持对象分层。")


def testing():
    out = begin(
        "检验尾概率、区间覆盖与多重比较",
        "p 值是 null 下统计量尾概率；置信水平属于重复抽样的区间程序；查看多个候选后选择赢家必须控制整个 family 的错误率。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "p 值：null 下更极端尾概率", BLUE)
    out += [line(55, 340, 355, 340, GRID, 2), line(70, 365, 70, 105, GRID, 2)]
    curve = normal_points(70, 345, 340, 205, 55, 205)
    out.append(polyline(curve, BLUE, 3))
    t_obs = 287
    out += [line(t_obs, 340, t_obs, 250, RED, 2.5, "6 4"), text(t_obs, 235, "t_obs", 15, 700, "middle", RED)]
    tail = [(x, y) for x, y in curve if x >= t_obs]
    out.append(polyline(tail, RED, 4))
    out += [
        text(45, 400, "p = P_H0(T >= t_obs)", 17, 650, cls="math"),
        text(45, 440, "valid p: P_H0(p <= alpha) <= alpha", 16, 650, cls="math"),
        text(45, 480, "不是 P(H0 为真 | data)。", 16, fill=RED),
    ]

    heading(out, 430, "B", "95% 属于区间程序的覆盖率", TEAL)
    theta_x = 610
    out += [line(theta_x, 95, theta_x, 430, TEAL, 3), text(theta_x, 82, "theta", 15, 700, "middle", TEAL)]
    intervals = ((470, 660), (520, 700), (555, 665), (640, 745), (485, 635), (575, 730))
    for i, (a, b) in enumerate(intervals):
        y = 125 + i * 54
        color = RED if a > theta_x or b < theta_x else BLUE
        out += [line(a, y, b, y, color, 3), line(a, y - 7, a, y + 7, color, 2), line(b, y - 7, b, y + 7, color, 2)]
    out += [
        text(430, 470, "P_theta(theta in C(X)) = 0.95", 16, 650, cls="math"),
        text(430, 500, "固定数据后的一个区间不再随机。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "选择赢家前，要定义整个 family", RED)
    out += [line(850, 340, 1135, 340, GRID, 2), line(870, 370, 870, 100, GRID, 2)]
    pvals = (0.015, 0.03, 0.07, 0.12, 0.20, 0.31, 0.52, 0.80)
    for i, p in enumerate(pvals, 1):
        x = 885 + (i - 1) * 32
        y = 340 - 265 * p
        color = RED if i <= 2 else BLUE
        out.append(circle(x, y, 5, color, color))
    out += [line(880, 330, 1120, 125, TEAL, 2.5, "7 5"), text(1105, 132, "BH line", 15, 700, fill=TEAL)]
    out += [
        text(830, 395, "FWER: P(at least one false rejection)", 15, 650),
        text(830, 430, "FDR: E[V/max(R,1)]", 16, 650, cls="math"),
        text(830, 470, "optional stopping / seed 挑选也属于选择。", 15, fill=RED),
    ]
    return finish(out, "显著性声明必须把统计量、重复抽样程序与所有数据依赖选择一起定义。")


def mcmc():
    out = begin(
        "MCMC 的不变性、相关样本与多链诊断",
        "目标 invariant 不等于当前链已混合；自相关降低有效样本量并抬高 MCSE；多链 R-hat、bulk/tail ESS、trace/rank 与算法诊断必须联合使用。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Invariant 不等于已从初值混合", BLUE)
    node(out, 55, 105, 100, 50, "nu_0", BLUE, size=17)
    node(out, 190, 105, 100, 50, "nu_t", TEAL, size=17)
    node(out, 55, 235, 100, 50, "pi", RED, size=17)
    node(out, 190, 235, 100, 50, "pi", RED, size=17)
    out += [
        line(158, 130, 185, 130, INK, 2.4, marker="a3"),
        text(172, 112, "K^t", 15, 650, "middle"),
        line(158, 260, 185, 260, RED, 2.4, marker="a2"),
        text(172, 242, "K", 15, 650, "middle", RED),
        line(240, 160, 240, 225, TEAL, 2, "6 4", marker="a1"),
        text(250, 195, "mixing?", 15, 650, fill=TEAL),
        text(45, 340, "pi K = pi  只说明保持目标", 17, 650, cls="math"),
        text(45, 382, "还需 irreducibility、recurrence / drift 等条件。", 15, fill=MUTED),
        text(45, 430, "多峰间不跳转时，局部平稳也会误导。", 15, fill=RED),
    ]

    heading(out, 430, "B", "自相关把 N 次迭代压成较小 ESS", TEAL)
    out += [line(440, 250, 770, 250, GRID, 2), line(455, 270, 455, 92, GRID, 2)]
    trace = []
    for i in range(121):
        x = 455 + 2.5 * i
        y = 185 - 42 * math.sin(i / 11) - 18 * math.sin(i / 29)
        trace.append((x, y))
    out.append(polyline(trace, TEAL, 2.5))
    out += [text(735, 102, "sticky trace", 15, 700, fill=TEAL)]
    for k in range(8):
        h = 95 * math.exp(-k / 2.4)
        x = 470 + k * 34
        out.append(line(x, 385, x, 385 - h, BLUE, 6))
    out += [
        line(450, 385, 750, 385, GRID, 2),
        text(740, 415, "lag", 15, 650),
        text(430, 455, "ESS = N / (1 + 2 sum rho_k)", 16, 650, cls="math"),
        text(430, 490, "MCSE 由目标函数 f 的长程方差决定。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "多链诊断要组合，不看单一数字", RED)
    out += [line(840, 250, 1140, 250, GRID, 2), line(855, 270, 855, 92, GRID, 2)]
    for j, (color, phase, offset) in enumerate(((BLUE, 0.0, -8), (TEAL, 0.7, 8), (RED, 1.4, 0))):
        pts = []
        for i in range(101):
            x = 855 + 2.65 * i
            y = 175 + offset + 25 * math.sin(i / 8 + phase) * math.exp(-i / 65)
            pts.append((x, y))
        out.append(polyline(pts, color, 2))
    checks = (
        "rank / folded split R-hat",
        "bulk ESS + tail ESS + MCSE",
        "trace / rank plots + divergences",
    )
    for i, label in enumerate(checks):
        y = 320 + i * 56
        out += [circle(850, y - 5, 5, (BLUE, TEAL, RED)[i], (BLUE, TEAL, RED)[i]), text(865, y, label, 16, 650)]
    out += [text(830, 490, "看似 R-hat≈1 仍不能证明发现了遗漏模态。", 15, fill=MUTED)]
    return finish(out, "MCMC 可信报告必须同时说明目标、链构造、混合、有效样本与算法失败信号。")


def bernoulli_inference_bridge():
    out = begin(
        "同一 Bernoulli 数据的三层不确定性",
        "局部 Fisher 信息约束重复抽样精度；Bayesian posterior/predictive 与 frequentist p-value/coverage 使用不同条件；MCMC 再为 posterior 积分增加数值误差层。",
        (BLUE, TEAL, AMBER),
    )

    heading(out, 42, "A", "局部信息与 sampling 精度", BLUE)
    node(out, 52, 96, 300, 58, "score = (Y-q)/[q(1-q)]", BLUE, size=16)
    out += [line(202, 156, 202, 196, INK, 2.3, marker="a3")]
    node(out, 52, 206, 300, 60, "I_1(q)=1/[q(1-q)]", TEAL, size=17)
    out += [line(202, 268, 202, 308, INK, 2.3, marker="a3")]
    node(out, 52, 318, 300, 64, "CRLB = q(1-q)/n", AMBER, size=17)
    out += [
        text(45, 430, "q=3/10, n=10: I_n=1000/21", 16, 650, cls="math"),
        text(45, 469, "Var(q_hat)=21/1000: sample mean attains bound", 15, 700, fill=TEAL),
        text(45, 502, "正则无偏类别中的局部基准，不是万能最优性。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "后验概率不等于 p 值或 coverage", TEAL)
    node(out, 440, 96, 315, 62, "posterior Q|y ~ Beta(5,9)", TEAL, size=17)
    out += [
        text(440, 205, "predictive M=0,1,2: (3/7, 3/7, 1/7)", 15, 650, cls="math"),
        text(440, 248, "P(Q<1/2|y)=7099/8192", 16, 700, fill=TEAL, cls="math"),
        line(440, 280, 755, 280, GRID, 2),
        text(440, 327, "exact two-sided p-value = 11/32", 16, 700, fill=BLUE, cls="math"),
        text(440, 370, "Hoeffding 95% CI: [0, 0.7295]", 16, 650, fill=AMBER),
        text(440, 420, "posterior: condition on data + model", 15, 650, fill=TEAL),
        text(440, 455, "p / coverage: repeat data under fixed q", 15, 650, fill=BLUE),
        text(440, 493, "数字可同时正确，因为条件事件不同。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "MCMC 再增加计算误差层", AMBER)
    node(out, 840, 96, 300, 58, "target Beta(5,9)", AMBER, size=17)
    out += [line(990, 156, 990, 196, INK, 2.3, marker="a3")]
    node(out, 840, 206, 300, 62, "proposal Beta(2,2) + MH", TEAL, size=16)
    out += [line(990, 270, 990, 310, INK, 2.3, marker="a3")]
    node(out, 840, 320, 300, 64, "correlated posterior draws", BLUE, size=17)
    out += [
        text(840, 425, "truth gates: mean=5/14; var=3/196", 15, 650, cls="math"),
        text(840, 462, "tail P(Q>1/2)=1093/8192", 15, 650, cls="math"),
        text(840, 497, "multi-chain R-hat + bulk/tail ESS + MCSE", 14, fill=MUTED),
    ]
    return finish(
        out,
        "数据随机性、参数不确定性与有限链计算误差必须分层报告；一种诊断不能替另一层作保证。",
    )


def split_rhat(chains):
    split = []
    for chain in chains:
        half = len(chain) // 2
        split.extend((chain[:half], chain[-half:]))
    n = len(split[0])
    means = [statistics.fmean(chain) for chain in split]
    variances = [statistics.variance(chain) for chain in split]
    grand = statistics.fmean(means)
    between = n * sum((value - grand) ** 2 for value in means) / (len(split) - 1)
    within = statistics.fmean(variances)
    variance_hat = (n - 1) * within / n + between / n
    return math.sqrt(variance_hat / within)


def approximate_ess(chains, max_lag=500):
    n = len(chains[0])
    centered = []
    variances = []
    for chain in chains:
        mean = statistics.fmean(chain)
        values = [value - mean for value in chain]
        centered.append(values)
        variances.append(sum(value * value for value in values) / n)
    base = statistics.fmean(variances)
    rhos = []
    for lag in range(1, min(max_lag, n - 1) + 1):
        covariance = statistics.fmean(
            sum(values[t] * values[t + lag] for t in range(n - lag)) / (n - lag)
            for values in centered
        )
        rhos.append(covariance / base)
    kept = []
    for index in range(0, len(rhos) - 1, 2):
        pair = rhos[index] + rhos[index + 1]
        if pair <= 0:
            break
        kept.extend((rhos[index], rhos[index + 1]))
    tau = max(1.0, 1 + 2 * sum(kept))
    return len(chains) * n / tau


def beta_independence_mh(seed=20260827, warmup=2000, draws=6000):
    starts = (0.03, 0.20, 0.75, 0.97)
    chains = []
    acceptance_rates = []

    def log_likelihood(q):
        return 3 * math.log(q) + 7 * math.log1p(-q)

    for chain_id, start in enumerate(starts):
        rng = random.Random(seed + chain_id)
        current = start
        accepted = 0
        kept = []
        for iteration in range(warmup + draws):
            candidate = rng.betavariate(2, 2)
            log_alpha = min(0.0, log_likelihood(candidate) - log_likelihood(current))
            if math.log(rng.random()) < log_alpha:
                current = candidate
                accepted += 1
            if iteration >= warmup:
                kept.append(current)
        chains.append(kept)
        acceptance_rates.append(accepted / (warmup + draws))
    return chains, acceptance_rates


def validate_bernoulli_inference_example():
    """Exact inference identities plus a deterministic MCMC calibration."""
    q = Fraction(3, 10)
    n = 10
    information_one = 1 / (q * (1 - q))
    information_n = n * information_one
    crlb = 1 / information_n
    assert information_one == Fraction(100, 21)
    assert information_n == Fraction(1000, 21)
    assert crlb == Fraction(21, 1000)

    posterior_mean = Fraction(5, 14)
    posterior_variance = Fraction(5 * 9, 14 * 14 * 15)
    posterior_mode = Fraction(4, 12)
    evidence_count = Fraction(16, 143)
    predictive = (Fraction(3, 7), Fraction(3, 7), Fraction(1, 7))
    assert posterior_variance == Fraction(3, 196)
    assert posterior_mode == Fraction(1, 3)
    assert sum(predictive) == 1
    assert evidence_count == Fraction(16, 143)
    assert predictive[-1] != posterior_mean * posterior_mean

    lower_tail_null = Fraction(sum(math.comb(10, k) for k in range(4)), 2**10)
    two_sided_p = 2 * lower_tail_null
    posterior_upper_half = Fraction(sum(math.comb(13, k) for k in range(5)), 2**13)
    posterior_lower_half = 1 - posterior_upper_half
    assert lower_tail_null == Fraction(11, 64)
    assert two_sided_p == Fraction(11, 32)
    assert posterior_upper_half == Fraction(1093, 8192)
    assert posterior_lower_half == Fraction(7099, 8192)

    radius = math.sqrt(math.log(40) / 20)
    assert abs(radius - 0.4294694083467376) < 1e-15
    assert min(1.0, 0.3 + radius) < 0.73

    chains, acceptance_rates = beta_independence_mh()
    pooled = [value for chain in chains for value in chain]
    mean_estimate = statistics.fmean(pooled)
    variance_estimate = statistics.variance(pooled)
    tail_estimate = statistics.fmean(value > 0.5 for value in pooled)
    rhat = split_rhat(chains)
    ess = approximate_ess(chains)
    mcse = math.sqrt(variance_estimate / ess)
    acceptance = statistics.fmean(acceptance_rates)
    assert abs(mean_estimate - float(posterior_mean)) < 0.005
    assert abs(variance_estimate - float(posterior_variance)) < 0.002
    assert abs(tail_estimate - float(posterior_upper_half)) < 0.01
    assert rhat < 1.01
    assert ess > 2000
    assert 0.2 < acceptance < 0.9
    print(
        "PROB-17—20 inference gate: "
        f"mean={mean_estimate:.6f} var={variance_estimate:.6f} "
        f"tail={tail_estimate:.6f} accept={acceptance:.3f} "
        f"split_rhat={rhat:.4f} ess≈{ess:.0f} mcse≈{mcse:.6f}"
    )


FIGURES = {
    "fig-bayesian-posterior-predictive-v2.svg": bayesian,
    "fig-testing-ci-multiplicity-v2.svg": testing,
    "fig-mcmc-kernel-diagnostics-v2.svg": mcmc,
    "fig-bernoulli-inference-layers-v2.svg": bernoulli_inference_bridge,
}


def main():
    validate_bernoulli_inference_example()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
