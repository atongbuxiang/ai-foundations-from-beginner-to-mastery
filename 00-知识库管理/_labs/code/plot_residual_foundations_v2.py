#!/usr/bin/env python3
"""Generate deterministic NN-41--44 residual-network textbook figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def residual_identity_degradation():
    out = begin(
        "Residual Learning：恒等基线与证据层",
        "残差块把目标映射改写为输入加增量；只有完整块允许零分支且捷径为恒等时，加深才可保留原函数；可表示、可优化和可泛化属于不同证据层。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "学习整映射，还是学习偏离量", BLUE)
    node(out, 55, 108, 86, 50, "x", BLUE)
    node(out, 245, 96, 112, 62, "H(x)", RED)
    out += [line(145, 133, 240, 128, INK, 2.4, marker="a3"),
            text(198, 112, "plain", 15, 700, "middle", MUTED)]
    node(out, 55, 240, 86, 50, "x", BLUE)
    node(out, 190, 225, 96, 52, "F(x)", TEAL)
    out += [line(145, 255, 185, 251, TEAL, 2.4, marker="a1"),
            path("M98 294V355H324", BLUE, 2.8, "none", None, "a0"),
            line(238, 281, 238, 350, TEAL, 2.4, marker="a1"),
            circle(324, 355, 8, INK, BG, 2),
            text(200, 402, "residual: H(x) = x + F(x)", 16, 700, "middle", BLUE),
            text(200, 438, "target branch: F*(x) = H(x) - x", 15, 650, "middle", TEAL),
            text(200, 477, "identity baseline: F = 0", 16, 700, "middle", RED)]

    heading(out, 430, "B", "shortcut 名字不能替代合同", TEAL)
    node(out, 445, 100, 132, 55, "x + 0 = x", TEAL, size=16)
    out += [text(760, 137, "true identity", 15, 700, "end", TEAL)]
    node(out, 445, 215, 132, 55, "P x + 0", RED, size=16)
    out += [text(760, 250, "projection != I", 15, 700, "end", RED)]
    node(out, 445, 330, 132, 55, "ReLU(x+0)", RED, size=15)
    out += [text(760, 365, "negative x lost", 15, 700, "end", RED)]
    out += [rect(442, 425, 328, 64, BLUE, "#EFF6FF", 5, 2),
            text(606, 451, "x_L = x_0 + sum F_l(x_l)", 16, 700, "middle", BLUE),
            text(606, 477, "exact sum; branch inputs stay coupled", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "从存在到效果：四道证据门", RED)
    levels = (
        ("1  representation", "zero branch preserves function", BLUE),
        ("2  optimization", "algorithm reaches a good point", TEAL),
        ("3  training evidence", "deeper train error improves", AMBER),
        ("4  generalization", "held-out task and protocol", RED),
    )
    for idx, (lab, desc, color) in enumerate(levels):
        y = 98 + idx * 100
        out += [rect(845, y, 285, 70, color, BG, 5, 2),
                text(860, y + 28, lab, 15, 700, fill=color),
                text(1115, y + 54, desc, 15, 600, "end", MUTED)]
        if idx < 3:
            out += [line(987, y + 73, 987, y + 94, INK, 1.8, marker="a3")]
    return finish(out, "残差首先提供恒等基线；它是否更易训练、更能泛化，必须逐级补证。")


def residual_jacobian_rail():
    out = begin(
        "Residual Jacobian：rail、干涉与有序路径",
        "残差块的 JVP 和 VJP 都是恒等项加分支项；两项可以相长或相消；深层 Jacobian 是 I 加局部算子的有序乘积。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一 accumulator 的两条贡献", BLUE)
    node(out, 52, 105, 82, 48, "v", BLUE)
    out += [line(138, 129, 345, 129, BLUE, 4, marker="a0"),
            text(240, 111, "identity: v", 15, 700, "middle", BLUE)]
    node(out, 165, 210, 92, 50, "J_F", TEAL)
    out += [path("M95 157V235H160", TEAL, 2.5, "none", None, "a1"),
            path("M262 235H345V134", TEAL, 2.5, "none", None, "a1"),
            text(257, 286, "branch: J_F v", 15, 700, "middle", TEAL),
            circle(345, 129, 8, INK, BG, 2),
            text(200, 342, "JVP = v + J_F v", 18, 700, "middle", INK)]
    out += [rect(52, 395, 296, 78, RED, "#FFF5F2", 5, 2),
            text(200, 424, "VJP = g + J_F^T g", 17, 700, "middle", RED),
            text(200, 453, "rail exists; sum may cancel", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "I + J_F 仍可塌缩或放大", TEAL)
    cases = (
        ("J_F = -I", "gain = 0", RED),
        ("J_F = +0.5 I", "gain = 1.5", TEAL),
        ("non-normal", "sigma: 3.00 / .003", BLUE),
    )
    for idx, (lab, result, color) in enumerate(cases):
        y = 105 + idx * 112
        out += [rect(445, y, 310, 78, color, BG, 6, 2),
                text(465, y + 31, lab, 16, 700, fill=color),
                text(735, y + 58, result, 15, 650, "end", MUTED)]
    out += [text(600, 455, "eigenvalues do not replace singular values", 15, 700, "middle", RED)]

    heading(out, 830, "C", "product 展开为不同长度的路径", RED)
    out += [text(845, 112, "(I+A3)(I+A2)(I+A1)", 17, 700, fill=INK)]
    rows = (
        ("length 0", "I", BLUE),
        ("length 1", "A1 + A2 + A3", TEAL),
        ("length 2", "A2A1 + A3A1 + A3A2", AMBER),
        ("length 3", "A3A2A1", RED),
    )
    for idx, (lab, expr, color) in enumerate(rows):
        y = 160 + idx * 78
        out += [rect(845, y, 285, 56, color, "#F8FAFC", 5, 1.8),
                text(862, y + 24, lab, 15, 700, fill=color),
                text(1115, y + 44, expr, 15, 600, "end", INK)]
    out += [text(987, 490, "ordered terms; not independent subnetworks", 15, 650, "middle", MUTED)]
    return finish(out, "I 是加法项，不是稳定证书；总增益取决于方向、奇异值与跨层有序乘积。")


def resnet_euler_stability():
    out = begin(
        "ResNet as Euler：step、稳定域与极限条件",
        "带尺度残差步与显式 Euler 同形；固定时间区间需要 h=T/N；连续衰减并不保证大步 Euler 稳定；ODE 极限还需一致向量场与误差控制。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "固定 horizon 才叫网格加密", BLUE)
    xs = [65, 135, 205, 275, 345]
    for idx, x in enumerate(xs):
        out += [circle(x, 145, 11, BLUE if idx < 4 else RED, BG, 2),
                text(x, 181, f"x{idx}" if idx < 4 else "xN", 15, 650, "middle", BLUE if idx < 4 else RED)]
        if idx < len(xs) - 1:
            out += [line(x + 14, 145, xs[idx + 1] - 15, 145, TEAL, 2.5, marker="a1")]
    out += [text(200, 105, "h = T / N", 17, 700, "middle", TEAL),
            rect(55, 225, 300, 72, BLUE, "#EFF6FF", 5, 2),
            text(205, 254, "x_(k+1) = x_k + h f_k(x_k)", 16, 700, "middle", BLUE),
            text(205, 282, "residual magnitude must be O(h)", 15, 600, "middle", MUTED),
            text(55, 365, "fixed h + more layers", 16, 700, fill=RED),
            text(55, 397, "usually extends time, not resolution", 15, 650, fill=MUTED),
            text(55, 450, "local defect O(h^2)", 16, 700, fill=TEAL),
            text(55, 480, "global error O(h), under assumptions", 15, 650, fill=MUTED)]

    heading(out, 430, "B", "Euler 稳定圆盘", TEAL)
    cx, cy, rad = 645, 285, 105
    out += [circle(cx, cy, rad, TEAL, "#ECFDF5", 2.5),
            line(445, cy, 775, cy, GRID, 2),
            line(750, 145, 750, 425, GRID, 2),
            text(775, cy - 12, "Re(z)", 15, 600, "end", MUTED),
            text(760, 158, "Im(z)", 15, 600, fill=MUTED),
            text(cx, cy + 30, "-1", 15, 700, "middle", TEAL),
            text(750, cy + 30, "0", 15, 700, "middle", INK)]
    out += [circle(645, cy, 7, BLUE, BLUE, 2),
            text(645, 455, "stable: |1+z| <= 1", 16, 700, "middle", TEAL),
            circle(485, cy, 7, RED, RED, 2),
            text(485, cy - 18, "z=-2.5", 15, 700, "middle", RED),
            text(600, 490, "Re(lambda)<0 is not enough when h is large", 15, 650, "middle", MUTED)]

    heading(out, 830, "C", "从公式同形到 ODE limit", RED)
    gates = (
        ("1  algebra", "x + h f", BLUE),
        ("2  scaling", "h=T/N", TEAL),
        ("3  family", "consistent f_N", AMBER),
        ("4  analysis", "regular + stable", RED),
        ("5  evidence", "error rate + compute", BLUE),
    )
    for idx, (lab, desc, color) in enumerate(gates):
        y = 94 + idx * 80
        out += [rect(845, y, 285, 54, color, BG, 5, 1.8),
                text(860, y + 24, lab, 15, 700, fill=color),
                text(1115, y + 40, desc, 15, 600, "end", MUTED)]
        if idx < 4:
            out += [line(987, y + 57, 987, y + 75, INK, 1.6, marker="a3")]
    return finish(out, "ResNet–Euler 是精确模板对应；连续极限必须补齐 step、族、一致性与稳定性。")


def residual_scaling_lipschitz():
    out = begin(
        "Residual Scaling：乘积、耗散与 forcing",
        "残差链的最坏扰动由 exp(sum alpha L) 控制；一除以 N 与一除以根号 N 对应不同账本；收缩还需要方向耗散；每层误差按剩余增益累积。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "两种 scale，两本账", BLUE)
    out += [rect(52, 100, 300, 86, BLUE, "#EFF6FF", 5, 2),
            text(202, 130, "worst case", 16, 700, "middle", BLUE),
            text(202, 160, "product <= exp(sum alpha L)", 15, 650, "middle", INK),
            rect(52, 220, 300, 86, TEAL, "#ECFDF5", 5, 2),
            text(202, 250, "alpha = 1/N", 16, 700, "middle", TEAL),
            text(202, 280, "exponent O(1)", 15, 650, "middle", INK),
            rect(52, 340, 300, 100, RED, "#FFF5F2", 5, 2),
            text(202, 370, "alpha = 1/sqrt(N)", 16, 700, "middle", RED),
            text(202, 400, "worst exponent O(sqrt(N))", 15, 650, "middle", INK),
            text(202, 426, "variance O(1), if uncorrelated", 15, 600, "middle", MUTED),
            text(202, 480, "deterministic != stochastic ledger", 15, 700, "middle", AMBER)]

    heading(out, 430, "B", "小 branch 不自动收缩", TEAL)
    node(out, 445, 105, 140, 60, "F(x)=+beta x", RED, size=15)
    out += [line(590, 135, 742, 135, RED, 3, marker="a2"),
            text(600, 185, "gain = 1 + alpha beta", 16, 700, "middle", RED)]
    node(out, 445, 250, 140, 60, "F(x)=-beta x", TEAL, size=15)
    out += [line(590, 280, 680, 280, TEAL, 3, marker="a1"),
            text(600, 330, "gain = |1 - alpha beta|", 16, 700, "middle", TEAL),
            rect(442, 385, 326, 82, BLUE, "#EFF6FF", 5, 2),
            text(605, 415, "one-sided mu < 0", 16, 700, "middle", BLUE),
            text(605, 444, "1 + 2 alpha mu + alpha^2 L^2 < 1", 15, 600, "middle", INK)]

    heading(out, 830, "C", "每层误差带着剩余尾巴", RED)
    ys = 180
    pts = [850, 930, 1010, 1090]
    for idx, x in enumerate(pts):
        out += [circle(x, ys, 12, BLUE if idx < 3 else RED, BG, 2),
                text(x, ys - 28, f"d{idx}", 15, 650, "middle", BLUE if idx < 3 else RED)]
        if idx < 3:
            out += [line(x + 15, ys, pts[idx + 1] - 15, ys, INK, 2.2, marker="a3"),
                    text((x + pts[idx + 1]) / 2, ys - 12, f"q{idx}", 15, 650, "middle", MUTED)]
    out += [line(895, 275, 895, 205, TEAL, 2.4, marker="a1"),
            text(895, 300, "xi0", 15, 700, "middle", TEAL),
            line(975, 345, 975, 205, AMBER, 2.4, marker="a1"),
            text(975, 370, "xi1", 15, 700, "middle", AMBER),
            rect(845, 405, 285, 76, RED, "#FFF5F2", 5, 2),
            text(987, 432, "d_N <= product q * d_0", 15, 700, "middle", RED),
            text(987, 458, "+ sum tail-product * xi_k", 15, 600, "middle", MUTED)]
    return finish(out, "稳定缩放要同时控制最坏乘积、方向耗散和逐层误差；三者不能共用一句直觉。")


FIGURES = {
    "fig-residual-identity-degradation-v2.svg": residual_identity_degradation,
    "fig-residual-jacobian-rail-v2.svg": residual_jacobian_rail,
    "fig-resnet-euler-stability-v2.svg": resnet_euler_stability,
    "fig-residual-scaling-lipschitz-v2.svg": residual_scaling_lipschitz,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
