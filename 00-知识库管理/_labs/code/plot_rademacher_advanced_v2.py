#!/usr/bin/env python3
"""Generate LT-29--32 paper-ink figures for margins, entropy, localization and fat-shattering."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def margin_bound():
    out = begin(
        "分类间隔、ramp loss 与风险证书",
        "函数间隔先经过阈值化的 ramp loss 转成可收缩的有界损失；经验低间隔比例、按一除以 gamma 增长的复杂度项和置信项共同构成分类风险上界。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "分对不等于远离边界", BLUE)
    out += [line(70, 300, 350, 170, INK, 3)]
    out += [line(115, 390, 315, 105, GRID, 2, "7 6")]
    for x, y, col, lab in (
        (105, 215, BLUE, "+"), (155, 245, BLUE, "+"), (220, 195, BLUE, "+"),
        (135, 335, RED, "−"), (230, 315, RED, "−"), (320, 275, RED, "−"),
    ):
        out += [circle(x, y, 15, col, BG, 2.5), text(x, y + 5, lab, 15, 700, "middle", fill=col)]
    out += [line(245, 240, 275, 220, TEAL, 3, marker="a1")]
    out += [text(285, 223, "margin", 15, 700, fill=TEAL)]
    out += [text(45, 440, "rho_i = y_i f(x_i)", 16, 700, fill=BLUE, cls="math")]
    out += [text(45, 480, "linear geometry divides by ||w||", 14, 650)]
    out += [text(45, 515, "functional margin alone is scale-sensitive。", 15, fill=MUTED)]

    heading(out, 430, "B", "Ramp 把 0–1 变成 Lipschitz", TEAL)
    out += [line(470, 395, 755, 395, GRID, 2), line(470, 105, 470, 395, GRID, 2)]
    out += [path("M470 145L560 145L690 365L755 365", TEAL, 3)]
    out += [line(560, 145, 560, 395, GRID, 1.5, "5 5"), line(690, 365, 690, 395, GRID, 1.5, "5 5")]
    out += [text(560, 420, "0", 14, 650, "middle"), text(690, 420, "gamma", 14, 650, "middle")]
    out += [text(490, 130, "phi_gamma", 15, 700, fill=TEAL)]
    out += [text(430, 455, "1{rho<=0} <= phi_gamma(rho)", 14, 650, cls="math")]
    out += [text(430, 490, "L = 1/gamma", 15, 700, fill=RED, cls="math")]
    out += [text(430, 515, "smaller gamma means a larger penalty。", 15, fill=MUTED)]

    heading(out, 830, "C", "三个可审计的风险项", RED)
    for y, col, title, sub in (
        (92, BLUE, "empirical low-margin rate", "P_m{y f(x) <= gamma}"),
        (225, TEAL, "capacity at scale gamma", "4 hat R_S(F) / gamma"),
        (358, RED, "confidence budget", "order sqrt(log(1/delta)/m)"),
    ):
        out += [rect(840, y, 300, 94, col, BG, 8, 2)]
        out += [text(990, y + 36, title, 15, 700, "middle", fill=col)]
        out += [text(990, y + 70, sub, 14, 650, "middle", cls="math")]
    out += [text(830, 495, "choose gamma on a declared grid", 14, 650)]
    out += [text(830, 520, "SVM geometry is one interface, not the theorem。", 15, fill=MUTED)]
    return finish(out, "分类证书同时读取经验 margin 分布、函数类复杂度与置信预算；最小训练间隔不是全部证据。")


def metric_entropy():
    out = begin(
        "覆盖数、Metric Entropy 与 Chaining",
        "经验度量把函数压成样本上的向量；单尺度覆盖只保留一张网，而 chaining 在逐渐变细的网之间累加增量，最终把离散层级和写成熵积分。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先固定度量与分辨率", BLUE)
    for x, y in ((90, 145), (140, 195), (205, 125), (260, 210), (315, 155), (175, 285), (290, 325)):
        out += [circle(x, y, 5, INK, INK)]
    for x, y in ((115, 170), (230, 165), (235, 300)):
        out += [circle(x, y, 55, BLUE, "#EFF6FF", 2), circle(x, y, 7, BLUE, BLUE)]
    out += [text(45, 390, "epsilon-cover: every restriction is nearby", 14, 650)]
    out += [text(45, 430, "H(epsilon) = log N(epsilon)", 16, 700, fill=BLUE, cls="math")]
    out += [text(45, 475, "d_S uses values on the current sample", 14, 650)]
    out += [text(45, 515, "entropy is geometric, not Shannon entropy。", 15, fill=MUTED)]

    heading(out, 430, "B", "Chaining 累加多尺度增量", TEAL)
    levels = ((115, 3, BLUE), (225, 5, TEAL), (335, 9, RED))
    for y, count, col in levels:
        out += [text(445, y + 5, f"epsilon_{(y-5)//110}", 14, 700, fill=col)]
        for j in range(count):
            x = 550 + j * (190 / max(1, count - 1))
            out += [circle(x, y, 6, col, col)]
    for j in range(3):
        out += [line(550 + j * 95, 121, 550 + j * 47.5, 219, GRID, 1.6)]
    for j in range(5):
        out += [line(550 + j * 47.5, 231, 550 + j * 23.75, 329, GRID, 1.4)]
    out += [text(430, 395, "f = coarse + sum of increments", 14, 650)]
    out += [text(430, 440, "each scale pays sqrt(log N)", 15, 700, fill=TEAL)]
    out += [text(430, 480, "fine residual is stopped at alpha", 14, 650)]
    out += [text(430, 515, "one net cannot reveal every useful scale。", 15, fill=MUTED)]

    heading(out, 830, "C", "离散层级和变成熵积分", RED)
    out += [line(855, 350, 1125, 350, GRID, 2), line(855, 105, 855, 350, GRID, 2)]
    out += [path("M855 125C900 145 930 180 965 220C1010 270 1060 315 1125 330", RED, 3)]
    out += [text(875, 125, "sqrt(log N(epsilon))", 14, 700, fill=RED)]
    out += [text(855, 400, "hat R <= 4 alpha", 15, 700, fill=BLUE, cls="math")]
    out += [text(855, 435, "+ 12/sqrt(m) integral sqrt(log N)", 13, 650, cls="math")]
    out += [text(830, 480, "optimize the cutoff alpha", 14, 650)]
    out += [text(830, 515, "constants follow the chosen convention。", 15, fill=MUTED)]
    return finish(out, "覆盖数回答每个尺度需要多少代表；chaining 把所有尺度的近似误差组织成一个复杂度预算。")


def local_rademacher():
    out = begin(
        "局部 Rademacher 复杂度、固定点与快率",
        "全局复杂度查看整个损失类；局部复杂度只查看二阶矩或 excess risk 较小的切片。sub-root envelope 与对角线的固定点给出自洽误差尺度，但快率仍需要 Bernstein 或曲率条件。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "全局类与局部切片", BLUE)
    out += [circle(200, 275, 150, BLUE, "#EFF6FF", 2.5)]
    out += [circle(200, 275, 72, TEAL, "#ECFDF5", 2.5)]
    out += [circle(200, 275, 8, RED, RED)]
    out += [text(212, 268, "f*", 15, 700, fill=RED)]
    out += [text(70, 120, "global class", 15, 700, fill=BLUE)]
    out += [text(220, 210, "G(r)", 15, 700, fill=TEAL)]
    out += [text(45, 445, "far-away bad functions need not set the rate", 14, 650)]
    out += [text(45, 485, "localize loss geometry, not just parameters", 14, 650)]
    out += [text(45, 515, "identifiability and curvature matter。", 15, fill=MUTED)]

    heading(out, 430, "B", "Sub-root fixed point", TEAL)
    out += [line(465, 390, 755, 390, GRID, 2), line(465, 100, 465, 390, GRID, 2)]
    out += [line(465, 390, 745, 110, BLUE, 2.5)]
    out += [path("M465 335C530 270 610 225 745 185", TEAL, 3)]
    out += [circle(620, 235, 7, RED, RED)]
    out += [line(620, 235, 620, 390, GRID, 1.5, "5 5")]
    out += [text(635, 230, "r*", 16, 700, fill=RED)]
    out += [text(700, 140, "r", 15, 700, fill=BLUE)]
    out += [text(680, 200, "psi(r)", 15, 700, fill=TEAL)]
    out += [text(430, 440, "psi(r*) = r*", 16, 700, fill=RED, cls="math")]
    out += [text(430, 480, "psi(r)/sqrt(r) is nonincreasing", 14, 650)]
    out += [text(430, 515, "the fixed point is a complexity scale。", 15, fill=MUTED)]

    heading(out, 830, "C", "什么时候可能出现快率", RED)
    out += [line(855, 390, 1125, 390, GRID, 2), line(855, 105, 855, 390, GRID, 2)]
    out += [path("M865 125C930 180 1000 270 1115 350", BLUE, 3)]
    out += [path("M865 145C930 235 1010 325 1115 375", TEAL, 3)]
    out += [text(885, 155, "m^-1/2", 15, 700, fill=BLUE)]
    out += [text(1015, 315, "m^-1", 15, 700, fill=TEAL)]
    out += [text(830, 430, "localization + Bernstein / curvature", 14, 700, fill=RED)]
    out += [text(830, 470, "peeling makes the statement uniform", 14, 650)]
    out += [text(830, 515, "localization alone does not promise m^-1。", 15, fill=MUTED)]
    return finish(out, "固定点把“当前半径内的复杂度”与“可证明的误差半径”闭合；快率还要由噪声或曲率提供。")


def fat_shattering():
    out = begin(
        "Fat-Shattering：带数值间隔的实值打散",
        "每个样本点有自己的阈值；函数类若能在阈值上下至少 gamma 的位置实现所有正负模式，就在该尺度 fat-shatter 这些点。尺度容量再通过 covering 和 Rademacher 进入回归风险。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "阈值上下必须留出间隔", BLUE)
    xs = (90, 170, 250, 330)
    rs = (235, 190, 270, 215)
    signs = (1, -1, 1, -1)
    for i, (x, r, s) in enumerate(zip(xs, rs, signs)):
        out += [line(x - 20, r, x + 20, r, GRID, 2)]
        out += [circle(x, r - s * 55, 7, BLUE if s > 0 else RED, BLUE if s > 0 else RED)]
        out += [line(x, r - 35, x, r + 35, TEAL, 2, "4 4")]
        out += [text(x, r + 10, f"r{i+1}", 13, 650, "middle")]
    out += [text(45, 380, "s_i ( f_s(x_i) - r_i ) >= gamma", 14, 700, fill=BLUE, cls="math")]
    out += [text(45, 425, "one function may be chosen for each sign pattern", 14, 650)]
    out += [text(45, 470, "thresholds are fixed before the pattern", 14, 650)]
    out += [text(45, 515, "our convention uses margin gamma。", 15, fill=MUTED)]

    heading(out, 430, "B", "容量随分辨率变粗而下降", TEAL)
    out += [line(465, 390, 755, 390, GRID, 2), line(465, 105, 465, 390, GRID, 2)]
    out += [path("M475 130H535V185H600V245H665V310H735V365", TEAL, 3)]
    out += [text(490, 115, "fat_gamma(F)", 15, 700, fill=TEAL)]
    out += [text(705, 420, "gamma", 14, 650)]
    out += [text(430, 455, "gamma_1 < gamma_2", 14, 650, cls="math")]
    out += [text(430, 485, "fat_gamma1 >= fat_gamma2", 14, 700, fill=BLUE, cls="math")]
    out += [text(430, 515, "pseudo-dimension forgets this scale profile。", 15, fill=MUTED)]

    heading(out, 830, "C", "从尺度容量到回归风险", RED)
    for y, col, title, sub in (
        (95, BLUE, "fat dimension", "sign patterns with margin"),
        (225, TEAL, "covering / entropy", "how many representatives"),
        (355, RED, "Lipschitz risk", "complexity + confidence"),
    ):
        out += [rect(840, y, 300, 82, col, BG, 8, 2)]
        out += [text(990, y + 31, title, 15, 700, "middle", fill=col)]
        out += [text(990, y + 62, sub, 14, 650, "middle")]
    out += [line(990, 180, 990, 218, INK, 2, marker="a3"), line(990, 310, 990, 348, INK, 2, marker="a3")]
    out += [text(830, 480, "squared loss needs bounded range or tails", 14, 650)]
    out += [text(830, 515, "gamma is resolution, not risk itself。", 15, fill=MUTED)]
    return finish(out, "Fat-shattering 保留函数值的分辨率；只有接上度量熵、损失合同与采样条件，才成为风险证书。")


FIGURES = {
    "fig-margin-ramp-risk-certificate-v2.svg": margin_bound,
    "fig-covering-entropy-chaining-v2.svg": metric_entropy,
    "fig-local-rademacher-fixed-point-v2.svg": local_rademacher,
    "fig-fat-shattering-regression-bridge-v2.svg": fat_shattering,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
