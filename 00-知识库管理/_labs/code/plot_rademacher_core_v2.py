#!/usr/bin/env python3
"""Generate LT-25--28 paper-ink figures for the Rademacher core chain."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def symmetrization_map():
    out = begin(
        "Ghost sample、随机交换与对称化",
        "总体期望先由独立 ghost sample 的条件期望替代；成对交换保持联合分布不变，并把双样本差编码为 Rademacher signs；最后拆成两个同分布的单样本随机过程。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "未知总体量换成独立样本", BLUE)
    node(out, 55, 95, 290, 64, "sup_f (P f - P_m f)", BLUE, size=16)
    out += [line(200, 163, 200, 205, INK, 2, marker="a3")]
    node(out, 55, 218, 290, 76, "E_{S'} sup_f (P'_m f - P_m f)", TEAL, size=15)
    out += [text(45, 350, "Jensen moves E_{S'} inside the supremum", 14, 650)]
    out += [text(45, 395, "S' has the same law and is independent", 14, 650, fill=BLUE)]
    out += [text(45, 455, "ghost data is only a proof device", 15, 700, fill=RED)]
    out += [text(45, 515, "the learner never receives S'。", 15, fill=MUTED)]

    heading(out, 430, "B", "每一对样本随机交换", TEAL)
    for i, x in enumerate((470, 550, 630, 710)):
        out += [rect(x - 27, 105, 54, 38, BLUE, BG, 5, 2), text(x, 130, f"Z{i+1}", 13, 650, "middle")]
        out += [rect(x - 27, 205, 54, 38, TEAL, BG, 5, 2), text(x, 230, f"Z'{i+1}", 13, 650, "middle")]
        if i % 2 == 0:
            out += [path(f"M{x-8} 150C{x-20} 170 {x-20} 185 {x-8} 198", RED, 2, "none", "5 4", "a2")]
            out += [text(x + 15, 178, "+", 15, 700, fill=RED)]
        else:
            out += [path(f"M{x+8} 150C{x+20} 170 {x+20} 185 {x+8} 198", BLUE, 2, "none", "5 4", "a0")]
            out += [text(x + 15, 178, "-", 15, 700, fill=BLUE)]
    out += [text(430, 315, "(Z_i,Z'_i) is exchangeable", 15, 700, fill=TEAL)]
    out += [text(430, 360, "sigma_i records which member is first", 14, 650)]
    out += [text(430, 415, "difference = m^-1 sum sigma_i(f(Z'_i)-f(Z_i))", 13, 650, cls="math")]
    out += [text(430, 470, "condition on the pooled sample before counting", 14, 650)]
    out += [text(430, 515, "exchangeability—not magic—creates signs。", 15, fill=MUTED)]

    heading(out, 830, "C", "拆成两个单样本随机过程", RED)
    node(out, 840, 95, 300, 72, "sup_f sum sigma_i(f'_i-f_i)", RED, size=15)
    out += [line(990, 171, 990, 210, INK, 2, marker="a3")]
    out += [rect(840, 222, 300, 80, TEAL, BG, 8, 2)]
    out += [text(990, 252, "<= sup_f sum sigma_i f'_i", 13, 650, "middle", fill=TEAL, cls="math")]
    out += [text(990, 282, "+ sup_f sum (-sigma_i) f_i", 13, 650, "middle", fill=TEAL, cls="math")]
    out += [text(830, 360, "the two expectations are identical", 15, 650)]
    out += [text(830, 405, "one-sided expected gap <= 2 R_m(F)", 14, 700, fill=BLUE)]
    out += [text(830, 450, "absolute gap needs an absolute/symmetric class", 14, 650, fill=RED)]
    out += [text(830, 490, "high probability adds concentration", 14, 650)]
    out += [text(830, 515, "symmetrization alone is an expectation bound。", 15, fill=MUTED)]
    return finish(out, "对称化的每一步都改变随机对象：总体期望、双样本差、随机符号过程不能在公式中被悄悄等同。")


def rademacher_complexity():
    out = begin(
        "经验 Rademacher 复杂度：在真实样本上拟合随机符号",
        "固定样本后给每个观测独立正负号，函数类与纯噪声的最大相关即经验 Rademacher 复杂度；它同时受样本几何与类的 restrictions 影响，并通过额外集中项形成风险证书。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "固定 S，再随机贴 signs", BLUE)
    signs = ((85, "+", BLUE), (135, "-", RED), (185, "+", BLUE), (235, "+", BLUE), (285, "-", RED), (335, "-", RED))
    for x, s, col in signs:
        out += [circle(x, 170, 18, col, BG, 2.5), text(x, 176, s, 16, 700, "middle", fill=col)]
    out += [path("M65 300C110 260 150 335 195 280C235 230 285 330 350 245", TEAL, 3)]
    out += [text(45, 375, "choose f after seeing sigma", 15, 700, fill=TEAL)]
    out += [text(45, 420, "score = m^-1 sum sigma_i f(z_i)", 15, 650, cls="math")]
    out += [text(45, 465, "then average the best score over sigma", 14, 650)]
    out += [text(45, 515, "labels are synthetic; sample locations are real。", 15, fill=MUTED)]

    heading(out, 430, "B", "复杂度同时依赖类与样本", TEAL)
    out += [rect(445, 95, 145, 88, BLUE, BG, 8, 2), text(517, 127, "same class", 15, 700, "middle", fill=BLUE), text(517, 157, "clustered S", 14, 650, "middle")]
    out += [rect(610, 95, 145, 88, RED, BG, 8, 2), text(682, 127, "same class", 15, 700, "middle", fill=RED), text(682, 157, "spread S", 14, 650, "middle")]
    for x, y in ((470, 245), (495, 255), (520, 240), (545, 250)):
        out += [circle(x, y, 6, BLUE, BLUE)]
    for x, y in ((625, 210), (665, 290), (705, 230), (740, 325)):
        out += [circle(x, y, 6, RED, RED)]
    out += [text(430, 385, "hat R_S(F) is observable up to sign Monte Carlo", 13, 650)]
    out += [text(430, 430, "R_m(F)=E_S hat R_S(F) is distributional", 14, 650)]
    out += [text(430, 475, "data-dependent does not mean assumption-free", 14, 650, fill=RED)]
    out += [text(430, 515, "sign-estimation error is a separate budget。", 15, fill=MUTED)]

    heading(out, 830, "C", "从随机符号到风险证书", RED)
    out += [rect(840, 90, 300, 72, BLUE, BG, 8, 2), text(990, 120, "empirical loss", 16, 700, "middle", fill=BLUE), text(990, 150, "P_m f", 15, 650, "middle")]
    out += [text(990, 200, "+", 22, 700, "middle")]
    out += [rect(840, 220, 300, 72, TEAL, BG, 8, 2), text(990, 250, "2 hat R_S(F)", 16, 700, "middle", fill=TEAL), text(990, 279, "selection complexity", 14, 650, "middle")]
    out += [text(990, 330, "+", 22, 700, "middle")]
    out += [rect(840, 350, 300, 72, RED, BG, 8, 2), text(990, 380, "confidence term", 16, 700, "middle", fill=RED), text(990, 409, "order sqrt(log(1/delta)/m)", 14, 650, "middle")]
    out += [text(830, 470, "certificate must use the loss class", 14, 650)]
    out += [text(830, 515, "a small estimate still needs a valid theorem。", 15, fill=MUTED)]
    return finish(out, "它度量真实样本上的随机符号拟合；风险证书还需要正确的损失类、有界性与集中项。")


def contraction_map():
    out = begin(
        "收缩引理：Lipschitz 损失不能制造过多随机符号复杂度",
        "若逐坐标变换在相关区间上 L-Lipschitz，中心化后其 Rademacher 复杂度由原函数类复杂度乘 L 控制；平方损失、cross-entropy 与 vector logits 必须另审范围或使用向量收缩。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先确定原始 score class", BLUE)
    out += [path("M60 365C120 315 160 150 220 205C275 255 300 115 350 145", BLUE, 3)]
    out += [line(60, 405, 350, 405, GRID, 2), line(60, 100, 60, 405, GRID, 2)]
    out += [text(45, 455, "F: z -> score f(z)", 16, 700, fill=BLUE)]
    out += [text(45, 490, "complexity is measured on f(z_i)", 14, 650)]
    out += [text(45, 515, "not yet on the training loss。", 15, fill=MUTED)]

    heading(out, 430, "B", "Lipschitz map controls distortion", TEAL)
    out += [line(465, 395, 745, 395, GRID, 2), line(465, 105, 465, 395, GRID, 2)]
    out += [path("M465 340L540 300L610 240L680 175L745 130", TEAL, 3)]
    out += [path("M465 370L540 335L610 280L680 225L745 180", RED, 2, "none", "7 5")]
    out += [text(490, 135, "|phi(u)-phi(v)| <= L|u-v|", 14, 700, fill=TEAL)]
    out += [text(430, 440, "center: psi_i(t)=phi_i(t)-phi_i(0)", 14, 650)]
    out += [text(430, 480, "hat R(phi o F) <= 2 L hat R(F)", 14, 700, fill=BLUE)]
    out += [text(430, 515, "some conventions sharpen the factor 2。", 15, fill=MUTED)]

    heading(out, 830, "C", "不同损失需要不同合同", RED)
    rows = (
        ("absolute / hinge", "L = 1", TEAL),
        ("logistic margin", "L <= 1", BLUE),
        ("squared loss", "L needs bounded scores and y", RED),
        ("softmax CE", "vector contraction / logit control", BLUE),
    )
    for i, (loss, cond, col) in enumerate(rows):
        y = 90 + i * 95
        out += [rect(840, y, 300, 66, col, BG, 8, 2)]
        out += [text(855, y + 27, loss, 15, 700, fill=col), text(855, y + 54, cond, 13, 600)]
    out += [text(830, 485, "margin ramp pays L=1/gamma", 14, 650, fill=RED)]
    out += [text(830, 515, "global Lipschitzness must hold on the used range。", 15, fill=MUTED)]
    return finish(out, "收缩引理是一座组合桥：先控制 score class，再用损失的 Lipschitz 几何传递复杂度；它不负责尾部、校准或分布偏移。")


def norm_linear_class():
    out = begin(
        "范数约束线性类：Rademacher 复杂度化为对偶范数",
        "线性函数对随机符号和的最大相关由权重球的 support function 给出，即 B 乘样本符号和的对偶范数；L2 得到能量半径，L1 得到坐标最大值与 log d，RKHS 得到 kernel diagonal。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Supremum = 支撑函数", BLUE)
    out += [circle(195, 270, 115, BLUE, "#EFF6FF", 2.5)]
    out += [line(195, 270, 310, 170, RED, 3, marker="a2")]
    out += [line(195, 270, 260, 215, TEAL, 3)]
    out += [text(315, 165, "v=sum sigma_i x_i", 14, 700, fill=RED)]
    out += [text(210, 220, "w", 15, 700, fill=TEAL)]
    out += [text(45, 425, "sup_{||w||<=B} <w,v> = B ||v||_*", 15, 700, cls="math")]
    out += [text(45, 475, "dual norm identifies the hardest direction", 14, 650)]
    out += [text(45, 515, "optimization geometry becomes capacity geometry。", 15, fill=MUTED)]

    heading(out, 430, "B", "L2：样本能量而非参数个数", TEAL)
    for x, y in ((480, 300), (540, 210), (605, 335), (675, 170), (735, 265)):
        out += [line(600, 300, x, y, GRID, 2), circle(x, y, 7, TEAL, TEAL)]
    out += [text(430, 105, "hat R_S(F_B)", 16, 700, fill=TEAL)]
    out += [text(430, 145, "= (B/m) E_sigma ||sum sigma_i x_i||_2", 13, 650, cls="math")]
    out += [text(430, 405, "<= (B/m) sqrt(sum ||x_i||_2^2)", 14, 700, fill=BLUE, cls="math")]
    out += [text(430, 455, "<= B R / sqrt(m) if ||x_i||_2<=R", 14, 650, cls="math")]
    out += [text(430, 515, "dimension may hide inside the data radius R。", 15, fill=MUTED)]

    heading(out, 830, "C", "更换范数就更换复杂度坐标", RED)
    rows = (
        ("||w||_1 <= B", "B R_inf sqrt(log d / m)", BLUE),
        ("||w||_2 <= B", "B R_2 / sqrt(m)", TEAL),
        ("RKHS ||f||_H <= B", "B sqrt(tr K) / m", RED),
    )
    for i, (constraint, bound, col) in enumerate(rows):
        y = 95 + i * 112
        out += [rect(840, y, 300, 82, col, BG, 8, 2)]
        out += [text(855, y + 31, constraint, 15, 700, fill=col), text(855, y + 63, bound, 14, 650)]
    out += [text(830, 455, "affine bias adds its own radius", 14, 650)]
    out += [text(830, 485, "regularization must imply an output norm bound", 13, 650, fill=RED)]
    out += [text(830, 515, "feature scaling changes B and R together。", 15, fill=MUTED)]
    return finish(out, "范数界的核心是权重球与数据几何的对偶配对；只报参数维数或正则化名称，无法得到数值风险证书。")


FIGURES = {
    "fig-ghost-sample-symmetrization-v2.svg": symmetrization_map,
    "fig-rademacher-empirical-complexity-v2.svg": rademacher_complexity,
    "fig-contraction-lipschitz-loss-v2.svg": contraction_map,
    "fig-dual-norm-linear-complexity-v2.svg": norm_linear_class,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
