#!/usr/bin/env python3
"""Generate v2 textbook figures for NUM-05--08 stable kernels and direct methods."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
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
    rect,
    text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "numerical-analysis"


def stable_reductions():
    out = begin(
        "稳定求和、补偿点积与混合精度矩阵乘",
        "顺序归约的舍入深度随 n 增长，平衡树将深度降为对数；消去使求和与点积本身病态，补偿算法只减少额外舍入；矩阵乘的 storage、multiply、accumulate 与 output precision 必须分别声明。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "归约树决定舍入深度", BLUE)
    # Serial chain.
    for i in range(5):
        x = 50 + i * 55
        node(out, x, 110, 38, 38, f"x{i+1}", BLUE, size=15)
        if i < 4:
            out.append(line(x + 40, 129, x + 52, 129, RED, 2, marker="a2"))
    out += [text(45, 180, "serial: depth n-1 -> gamma_(n-1)", 15, 650, fill=RED)]
    # Pairwise tree.
    for x, lab in ((65, "x1"), (145, "x2"), (225, "x3"), (305, "x4")):
        node(out, x, 250, 42, 38, lab, BLUE, size=15)
    for x in (105, 265):
        node(out, x, 330, 50, 38, "+", TEAL)
    node(out, 185, 410, 50, 38, "+", TEAL)
    out += [line(86, 290, 125, 327, INK, 2), line(166, 290, 135, 327, INK, 2), line(246, 290, 285, 327, INK, 2), line(326, 290, 295, 327, INK, 2), line(130, 370, 205, 407, INK, 2), line(290, 370, 215, 407, INK, 2)]
    out += [text(45, 480, "pairwise: depth ceil(log2 n)", 15, 650, fill=TEAL), text(45, 505, "tree shape also affects reproducibility。", 15, fill=MUTED)]

    heading(out, 430, "B", "补偿减少算法误差，不消除病态", TEAL)
    out += [line(450, 300, 760, 300, GRID, 2), line(605, 105, 605, 440, GRID, 2)]
    out += [line(605, 300, 735, 150, BLUE, 3, marker="a0"), line(605, 300, 470, 420, RED, 3, marker="a2"), line(605, 300, 630, 275, TEAL, 4, marker="a1")]
    out += [text(690, 140, "positive terms", 15, 700, fill=BLUE), text(445, 446, "negative terms", 15, 700, fill=RED), text(635, 265, "tiny exact sum", 15, 700, fill=TEAL)]
    out += [text(430, 185, "kappa_sum = sum |x_i| / |sum x_i|", 15, 650, cls="math"), text(430, 480, "Kahan / Neumaier track a lost low-order tail", 15, 650), text(430, 507, "input quantization already lost cannot be recovered。", 15, fill=MUTED)]

    heading(out, 830, "C", "GEMM 是许多点积的精度合同", RED)
    stages = (("storage", "A,B", BLUE), ("multiply", "a_ik b_kj", RED), ("accumulate", "sum over k", TEAL), ("output", "cast C", BLUE))
    for i, (label, desc, color) in enumerate(stages):
        yy = 98 + i * 86
        out += [text(830, yy, label, 16, 700, fill=color), line(830, yy + 17, 895, yy + 17, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(910, yy + 23, desc, 15, 650)]
    out += [line(830, 430, 1145, 430, GRID, 2), text(830, 462, "|Delta C| <= gamma_k |A| |B|", 16, 650, cls="math"), text(830, 492, "precision != determinism != reproducibility", 15, 650, fill=RED), text(830, 516, "report backend + reduction + accumulator。", 15, fill=MUTED)]
    return finish(out, "稳定内核要同时审计问题条件性、归约结构、补偿机制和实际累加精度。")


def stable_linear_solve():
    out = begin(
        "稳定线性求解的 pivot、growth 与解质量证书",
        "可靠线性求解从结构与尺度选择开始，经 pivoted factorization 和 triangular solves 得到候选解，再用真实残差、分量后向误差和条件估计验收；部分选主元的风险受元素增长控制。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "求解器是一条验收流水线", BLUE)
    stages = (("structure", BLUE), ("scale", TEAL), ("factor", RED), ("triangular", BLUE), ("residual", TEAL))
    for i, (label, color) in enumerate(stages):
        y = 92 + i * 82
        node(out, 55, y, 285, 50, label, color, size=16)
        if i < 4:
            out.append(line(198, y + 52, 198, y + 76, INK, 2.2, marker="a3"))
    out += [text(45, 502, "never form A^-1；solve and certify。", 15, fill=MUTED)]

    heading(out, 430, "B", "small pivot 与 pivot growth", TEAL)
    # Two matrix sketches.
    out += [rect(450, 110, 125, 125, BLUE, BG, 0, 2), line(512, 110, 512, 235, GRID, 2), line(450, 172, 575, 172, GRID, 2)]
    out += [text(481, 150, "eps", 17, 700, "middle", fill=RED), text(544, 150, "1", 17, 650, "middle"), text(481, 212, "1", 17, 650, "middle"), text(544, 212, "1", 17, 650, "middle")]
    out += [line(590, 172, 640, 172, RED, 3, marker="a2"), text(615, 150, "swap", 15, 700, "middle", fill=RED)]
    out += [rect(655, 110, 125, 125, TEAL, BG, 0, 2), line(717, 110, 717, 235, GRID, 2), line(655, 172, 780, 172, GRID, 2)]
    out += [text(686, 150, "1", 17, 700, "middle", fill=TEAL), text(748, 150, "1", 17, 650, "middle"), text(686, 212, "eps", 17, 650, "middle"), text(748, 212, "1", 17, 650, "middle")]
    out += [text(430, 290, "partial pivoting keeps |l_ik| <= 1", 16, 650), text(430, 330, "but U entries may grow: pivot growth rho", 16, 650, fill=RED)]
    out += [line(430, 365, 770, 365, GRID, 2), text(430, 407, "computed factors solve P(A+Delta A)=L U", 15, 650, cls="math"), text(430, 445, "|Delta A| bounded by u |L||U|", 15, 650, cls="math"), text(430, 487, "GEPP is usually reliable, not universally safe。", 15, fill=MUTED)]

    heading(out, 830, "C", "BERR 与 FERR 回答不同问题", RED)
    node(out, 840, 105, 300, 58, "true residual r=b-A x_hat", BLUE)
    out += [line(990, 166, 990, 205, INK, 2.5, marker="a3")]
    node(out, 840, 218, 300, 68, "BERR: scaled componentwise residual", TEAL, size=16)
    out += [line(990, 289, 990, 328, INK, 2.5, marker="a3")]
    node(out, 840, 340, 300, 68, "FERR: condition-informed solution risk", RED, size=16)
    out += [text(830, 452, "equilibration changes coordinates, not sensitivity", 15, 650), text(830, 485, "fallback: pivoting / QR / SVD / higher precision", 15, fill=MUTED)]
    return finish(out, "稳定求解不是得到一个 x：它必须同时交付分解风险、后向误差和条件解释。")


def iterative_refinement():
    out = begin(
        "混合精度迭代改进的误差方程、三精度与回退边界",
        "高精度残差观测当前误差，低精度因子近似作用逆矩阵得到修正，工作精度更新解；收敛取决于近似逆质量、条件性、残差地板和校正求解器，GMRES-IR 只能扩展而不能消除失败区间。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "反复求解误差方程 A d=r", BLUE)
    node(out, 55, 100, 285, 55, "current x_k", BLUE)
    out += [line(198, 158, 198, 195, INK, 2.5, marker="a3")]
    node(out, 55, 208, 285, 62, "r_k=b-A x_k  (high precision)", TEAL, size=16)
    out += [line(198, 273, 198, 310, INK, 2.5, marker="a3")]
    node(out, 55, 322, 285, 62, "solve M d_k=r_k  (low factors)", RED, size=16)
    out += [line(198, 387, 198, 424, INK, 2.5, marker="a3")]
    node(out, 55, 437, 285, 55, "x_(k+1)=x_k+d_k", BLUE, size=16)
    out += [path("M340 465C380 465 380 125 342 125", TEAL, 2.5, "none", "7 5", "a1")]

    heading(out, 430, "B", "三种精度承担不同职责", TEAL)
    rows = (("u_f", "factor + correction solve", RED), ("u", "store and update x", BLUE), ("u_r", "recompute residual", TEAL))
    for i, (label, desc, color) in enumerate(rows):
        yy = 112 + i * 105
        out += [circle(460, yy, 22, color, BG, 2.5), text(460, yy + 6, label, 16, 700, "middle", fill=color), line(485, yy, 525, yy, color, 2.5), text(540, yy + 6, desc, 16, 650)]
    out += [text(430, 420, "typical hierarchy: u_r <= u <= u_f", 16, 700, cls="math"), text(430, 457, "high-precision residual lowers the observable floor", 15, 650), text(430, 490, "it cannot repair a useless approximate inverse。", 15, fill=MUTED)]

    heading(out, 830, "C", "收敛、停滞与回退合同", RED)
    out += [text(830, 105, "error map", 17, 700, fill=BLUE), text(830, 138, "e_(k+1)=(I-M^-1 A)e_k + rounding", 15, 650, cls="math")]
    out += [line(830, 170, 1145, 170, GRID, 2)]
    gates = (("converging", "BERR down + correction down", TEAL), ("stagnating", "true residual hits precision floor", RED), ("diverging", "poor factors / scaling / condition", BLUE))
    for i, (label, desc, color) in enumerate(gates):
        yy = 220 + i * 78
        out += [text(830, yy, label, 16, 700, fill=color), text(945, yy, desc, 15, 650)]
    out += [line(830, 430, 1145, 430, GRID, 2), text(830, 462, "fallback: GMRES-IR -> refactor -> raise precision", 15, 650, fill=RED), text(830, 493, "kappa(A) u_f < 1 is useful intuition, not full theorem。", 15, fill=MUTED)]
    return finish(out, "迭代改进的可信度来自高精度观测、可用近似逆和明确回退，而不是“多迭代几次”。")


def householder_givens():
    out = begin(
        "Householder 反射、Givens 旋转与稳定 QR",
        "Householder 用一次反射消去整列尾部并通过安全符号避免消去；Givens 用安全缩放的二维旋转消去单个元素；正交变换保持二范数，但实现仍要验收重构残差、正交性和局部参数生成。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Householder 把 x 反射到坐标轴", BLUE)
    out += [line(55, 380, 365, 380, GRID, 2), line(205, 420, 205, 95, GRID, 2)]
    x = (315, 170)
    target = (205, 300)
    out += [line(205, 380, x[0], x[1], BLUE, 4, marker="a0"), line(205, 380, target[0], target[1], TEAL, 4, marker="a1"), line(90, 245, 340, 355, RED, 2.5, "7 5")]
    out += [text(320, 160, "x", 17, 700, fill=BLUE), text(215, 292, "+/-||x|| e1", 15, 700, fill=TEAL), text(80, 225, "reflecting hyperplane", 15, 650, fill=RED)]
    out += [text(45, 445, "v = x + sign(x1)||x|| e1", 16, 650, cls="math"), text(45, 480, "safe sign avoids subtracting near-equal numbers。", 15, fill=MUTED)]

    heading(out, 430, "B", "Givens 只旋转两个坐标", TEAL)
    out += [circle(600, 275, 120, GRID, "none", 2), line(600, 275, 710, 190, BLUE, 4, marker="a0"), line(600, 275, 740, 275, TEAL, 4, marker="a1"), path("M660 275A60 60 0 0 0 648 239", RED, 2.5)]
    out += [text(710, 180, "(a,b)", 16, 700, fill=BLUE), text(700, 300, "(r,0)", 16, 700, fill=TEAL), text(650, 245, "theta", 15, 650, fill=RED)]
    out += [text(430, 420, "[c s; -s c] [a;b] = [r;0]", 16, 650, cls="math"), text(430, 458, "compute r=hypot(a,b), then c=a/r, s=b/r", 15, 650), text(430, 490, "scaled hypot avoids overflow and underflow。", 15, fill=MUTED)]

    heading(out, 830, "C", "结构选择与 QR 验收", RED)
    out += [text(830, 108, "Householder", 17, 700, fill=BLUE), text(830, 140, "dense column tail · block/WY · BLAS-3", 15, 650)]
    out += [line(830, 170, 1145, 170, GRID, 2), text(830, 215, "Givens", 17, 700, fill=TEAL), text(830, 247, "sparse entry · updates · bulge chasing", 15, 650)]
    out += [line(830, 277, 1145, 277, GRID, 2), text(830, 322, "verify both", 17, 700, fill=RED), text(830, 354, "reconstruction: ||A-Q R|| / ||A||", 15, 650, cls="math"), text(830, 388, "orthogonality: ||I-Q^T Q||", 15, 650, cls="math")]
    out += [text(830, 440, "small reconstruction residual alone is insufficient", 15, 650, fill=RED), text(830, 478, "compact storage: store vectors/rotations, not full Q", 15, fill=MUTED), text(830, 506, "communication cost can dominate flops。", 15, fill=MUTED)]
    return finish(out, "正交变换提供稳定几何，但安全参数生成、结构成本和双重残差验收仍不可省略。")


FIGURES = {
    "fig-stable-reductions-matmul-v2.svg": stable_reductions,
    "fig-pivoting-linear-solve-v2.svg": stable_linear_solve,
    "fig-mixed-precision-refinement-v2.svg": iterative_refinement,
    "fig-householder-givens-qr-v2.svg": householder_givens,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
