#!/usr/bin/env python3
"""Generate LT-37--40 paper-ink figures for PAC-Bayes and information bounds."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def pac_bayes_measure_change():
    out = begin(
        "PAC-Bayes：先验矩、测度变换与 Bernoulli-KL 证书",
        "先在数据随机性下控制 prior 平均指数矩，再以 KL 为代价把 prior 换成任意 data-dependent posterior，最后利用 Bernoulli KL 联合凸性聚合 Gibbs 风险。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先控制 prior 平均矩", BLUE)
    for x, r, col in ((85, 24, BLUE), (155, 38, TEAL), (245, 18, BLUE), (315, 30, TEAL)):
        out += [circle(x, 175, r, col, BG, 2.5)]
    out += [text(200, 270, "h ~ P fixed before S", 16, 700, "middle", fill=BLUE)]
    out += [text(45, 330, "E_S E_P exp[m kl(Rhat(h)||R(h))]", 15, 650, cls="math")]
    out += [text(45, 370, "<= m + 1", 20, 700, fill=TEAL, cls="math")]
    out += [line(55, 420, 340, 420, GRID, 2)]
    out += [text(45, 460, "Markov turns expectation into one good event", 14, 650)]
    out += [text(45, 515, "the prior cannot be refit on this same S。", 15, fill=MUTED)]

    heading(out, 430, "B", "换到 posterior，支付 KL", TEAL)
    out += [circle(520, 190, 82, BLUE, BG, 3), circle(655, 250, 68, TEAL, BG, 3)]
    out += [text(520, 195, "P", 25, 700, "middle", fill=BLUE), text(655, 255, "Q_S", 23, 700, "middle", fill=TEAL)]
    out += [line(570, 185, 620, 220, RED, 3, marker="a2")]
    out += [text(610, 145, "measure change", 14, 700, "middle", fill=RED)]
    out += [text(430, 350, "E_Q f <= KL(Q||P) + log E_P exp(f)", 14, 650, cls="math")]
    out += [text(430, 405, "Q may depend on S", 16, 700, fill=TEAL)]
    out += [text(430, 450, "Q not << P  =>  KL = infinity", 15, 650, cls="math")]
    out += [text(430, 515, "posterior means a certificate distribution。", 15, fill=MUTED)]

    heading(out, 830, "C", "聚合成可反演的证书", RED)
    node(out, 840, 100, 290, 70, "empirical Gibbs risk", BLUE, size=16)
    out += [line(985, 175, 985, 210, INK, 2.5, marker="a3")]
    node(out, 840, 220, 290, 88, "binary kl <= (KL + confidence) / m", RED, size=15)
    out += [line(985, 313, 985, 348, INK, 2.5, marker="a3")]
    node(out, 840, 360, 290, 70, "invert for population risk", TEAL, size=16)
    out += [text(830, 475, "Pinsker gives a looser square-root corollary", 14, 650)]
    out += [text(830, 515, "the statement is simultaneous over every Q。", 15, fill=MUTED)]
    return finish(out, "PAC-Bayes 的三步：prior 矩控制、KL 测度变换、binary-kl 风险反演。")


def prior_posterior_contract():
    out = begin(
        "PAC-Bayes 的先验、后验与数据依赖合同",
        "标准 theorem 允许 posterior 看训练样本，但 prior 必须相对证书样本保持独立。独立预训练、样本切分、预声明混合与专门 DP 定理提供不同的合法路线。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "时间线决定合法性", BLUE)
    out += [line(65, 230, 340, 230, INK, 3, marker="a3")]
    for x, lab, col in ((90, "choose P", BLUE), (205, "observe S", RED), (315, "choose Q_S", TEAL)):
        out += [circle(x, 230, 9, col, col), text(x, 190, lab, 15, 700, "middle", fill=col)]
    out += [text(45, 310, "legal: P before the certificate sample", 15, 700, fill=BLUE)]
    out += [text(45, 360, "legal: Q after S, chosen by optimization", 15, 700, fill=TEAL)]
    out += [text(45, 420, "illegal: center P at w_S without correction", 15, 700, fill=RED)]
    out += [text(45, 515, "ordering is a probability condition, not notation。", 15, fill=MUTED)]

    heading(out, 430, "B", "四条可审计路线", TEAL)
    items = (
        (100, "independent pretraining prior", BLUE),
        (205, "split S0 -> P ; certify on S1", TEAL),
        (310, "fixed mixture with code weights", BLUE),
        (415, "special DP-prior theorem + cost", RED),
    )
    for y, lab, col in items:
        node(out, 445, y, 310, 62, lab, col, size=15)
    out += [text(430, 515, "the same held-out point cannot serve twice。", 15, fill=MUTED)]

    heading(out, 830, "C", "Gaussian posterior 的真实权衡", RED)
    out += [line(850, 390, 1130, 390, GRID, 2), line(850, 100, 850, 390, GRID, 2)]
    out += [path("M860 125C930 160 1020 270 1120 360", BLUE, 3)]
    out += [path("M860 350C930 300 1020 190 1120 125", RED, 3)]
    out += [text(870, 160, "KL cost", 15, 700, fill=BLUE)]
    out += [text(1010, 160, "perturbed risk", 15, 700, fill=RED)]
    out += [text(985, 425, "posterior noise scale", 14, 650, "middle")]
    out += [text(830, 465, "sigma -> 0: point mass, often infinite KL", 14, 650, cls="math")]
    out += [text(830, 495, "sigma large: simple but inaccurate Gibbs predictor", 14, 650)]
    out += [text(830, 515, "report the distribution you actually certify。", 15, fill=MUTED)]
    return finish(out, "合法先验提供参照；后验在经验风险、随机化与相对熵之间寻找可验证平衡。")


def information_generalization():
    out = begin(
        "互信息泛化：学习算法作为 sample-to-output channel",
        "学习算法把样本映射为随机输出 W。transport lemma 比较 joint law 与独立 product law；互信息度量二者距离，从而控制期望 signed generalization gap。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "算法是一条随机信道", BLUE)
    node(out, 55, 105, 125, 64, "sample S", BLUE, size=17)
    node(out, 230, 105, 125, 64, "output W", TEAL, size=17)
    out += [line(185, 137, 225, 137, INK, 2.5, marker="a3")]
    out += [text(205, 112, "A", 15, 700, "middle", fill=RED)]
    for j in range(5):
        out += [circle(80 + 55 * j, 250, 13, BLUE, BG, 2), text(80 + 55 * j, 255, f"z{j+1}", 13, 650, "middle")]
    out += [text(45, 330, "complexity = I(S;W)", 20, 700, fill=TEAL, cls="math")]
    out += [text(45, 380, "algorithm randomness belongs to P(W|S)", 14, 650, cls="math")]
    out += [text(45, 430, "post-processing cannot increase information", 14, 650)]
    out += [text(45, 515, "exact continuous outputs may leak infinite bits。", 15, fill=MUTED)]

    heading(out, 430, "B", "Joint law 对比 product law", TEAL)
    node(out, 445, 105, 135, 72, "P_(W,Z)", RED, size=17)
    node(out, 640, 105, 115, 72, "P_W x P_Z", BLUE, size=15)
    out += [line(585, 142, 635, 142, RED, 3, marker="a2")]
    out += [text(610, 110, "KL", 14, 700, "middle", fill=RED)]
    out += [text(430, 245, "|E_joint f - E_product f|", 16, 700, cls="math")]
    out += [text(430, 290, "<= sqrt(2 sigma^2 KL)", 18, 700, fill=TEAL, cls="math")]
    out += [line(450, 345, 740, 345, GRID, 2)]
    out += [text(430, 390, "product law means W does not know this Z", 14, 650)]
    out += [text(430, 440, "sub-Gaussian loss makes the transport finite", 14, 650)]
    out += [text(430, 515, "dependence is averaged under the data law。", 15, fill=MUTED)]

    heading(out, 830, "C", "信息预算给出期望间隙", RED)
    out += [text(830, 120, "|E gen| <= sqrt[2 sigma^2 I(S;W) / m]", 15, 700, fill=RED, cls="math")]
    for y, lab, col in (
        (190, "K outputs: I <= log K", BLUE),
        (285, "b-bit transcript: I <= b log 2", TEAL),
        (380, "k adaptive rounds: use chain rule", RED),
    ):
        node(out, 840, y, 290, 62, lab, col, size=15)
    out += [text(830, 475, "expected signed != high probability", 15, 700, fill=RED)]
    out += [text(830, 515, "I(X;representation) is a different object。", 15, fill=MUTED)]
    return finish(out, "输出关于训练样本携带得越少，平均训练—总体偏差越难被自适应选择放大。")


def certificate_comparison():
    out = begin(
        "五类泛化证书：对象、量词与失败模式",
        "容量、稳定性、样本压缩、PAC-Bayes 与互信息都可产生泛化界，但它们控制不同对象、使用不同概率量词。比较前必须统一数据、损失、输出、置信度和随机性。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一 risk，五种复杂度", BLUE)
    node(out, 145, 235, 120, 70, "risk gap", RED, size=19)
    items = (
        (55, 95, "capacity", BLUE), (235, 95, "stability", TEAL),
        (45, 390, "compression", BLUE), (245, 390, "PAC-Bayes", TEAL),
    )
    for x, y, lab, col in items:
        node(out, x, y, 110, 55, lab, col, size=15)
        out += [line(x + 55, y + (55 if y < 235 else 0), 205, 235 if y < 235 else 305, col, 2)]
    node(out, 150, 450, 100, 45, "mutual info", RED, size=15)
    out += [line(205, 305, 200, 450, RED, 2)]
    out += [text(45, 515, "the numerator is not a universal currency。", 15, fill=MUTED)]

    heading(out, 430, "B", "先对齐量词，再比较数值", TEAL)
    rows = (
        (100, "class sup", "capacity", BLUE),
        (185, "neighboring S", "stability", TEAL),
        (270, "short decoder", "compression", BLUE),
        (355, "all posterior Q", "PAC-Bayes", TEAL),
        (440, "average channel", "information", RED),
    )
    for y, left, right, col in rows:
        out += [text(445, y + 22, left, 15, 650, fill=col), line(570, y + 15, 625, y + 15, GRID, 2), text(645, y + 22, right, 15, 700, fill=col)]
    out += [text(430, 515, "uniform / algorithmic / randomized are distinct。", 15, fill=MUTED)]

    heading(out, 830, "C", "选择证书也会产生选择偏差", RED)
    node(out, 845, 100, 275, 58, "predeclare valid certificates", BLUE, size=15)
    out += [line(982, 163, 982, 198, INK, 2.5, marker="a3")]
    node(out, 845, 210, 275, 72, "align loss, data, confidence", TEAL, size=15)
    out += [line(982, 287, 982, 322, INK, 2.5, marker="a3")]
    node(out, 845, 335, 275, 72, "union-budget selection or fixed rule", RED, size=15)
    out += [text(830, 465, "do not take an uncorrected post-hoc minimum", 14, 700, fill=RED)]
    out += [text(830, 495, "a vacuous bound is still logically valid", 14, 650)]
    out += [text(830, 515, "no single theory explains every deep net。", 15, fill=MUTED)]
    return finish(out, "证书选择不是看谁公式最漂亮，而是先匹配对象与量词，再检查能否非空、可算和可复现。")


FIGURES = {
    "fig-pac-bayes-measure-change-v2.svg": pac_bayes_measure_change,
    "fig-pac-bayes-prior-posterior-contract-v2.svg": prior_posterior_contract,
    "fig-mutual-information-generalization-v2.svg": information_generalization,
    "fig-generalization-certificates-comparison-v2.svg": certificate_comparison,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
