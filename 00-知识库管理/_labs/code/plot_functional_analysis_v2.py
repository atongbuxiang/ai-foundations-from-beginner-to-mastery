#!/usr/bin/env python3
"""Generate v2 textbook figures for GEO-05--08 functional-analysis foundations."""

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


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "functional-analysis"


def banach_hilbert():
    out = begin(
        "Normed、Banach、Hilbert 与正交投影",
        "Norm 先给距离，completeness 得 Banach；inner product 还给角度和正交，完备后得 Hilbert。Hilbert 中 closed convex set 有唯一最近点，closed subspace 的 residual 与子空间正交；连续函数对象不可与有限采样向量混同。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "结构逐层增加，结论随之增加", BLUE)
    node(out, 55, 90, 290, 54, "vector space", BLUE, size=15)
    out += [line(200, 147, 200, 176, INK, 2, marker="a3")]
    node(out, 55, 185, 290, 54, "norm -> distance / Cauchy", TEAL, size=15)
    out += [line(140, 242, 140, 271, INK, 2, marker="a3"), line(260, 242, 260, 271, INK, 2, marker="a3")]
    node(out, 45, 280, 180, 60, "complete -> Banach", BLUE, size=14)
    node(out, 225, 280, 150, 60, "inner product", RED, size=14)
    out += [line(300, 343, 300, 372, INK, 2, marker="a3")]
    node(out, 225, 382, 150, 60, "complete -> Hilbert", TEAL, size=14)
    out += [text(45, 480, "Hilbert is Banach, but not conversely", 14, 650), text(45, 510, "in infinite dimension, bounded != compact。", 14, fill=MUTED)]

    heading(out, 430, "B", "Projection theorem：最近点与正交", TEAL)
    out += [path("M450 360L755 360", TEAL, 3), circle(590, 360, 7, TEAL, TEAL), circle(690, 145, 8, BLUE, BLUE), line(690, 145, 590, 360, RED, 3, marker="a2"), line(590, 360, 745, 360, BLUE, 2)]
    out += [text(690, 126, "x", 16, 700, "middle", fill=BLUE), text(590, 390, "p=P_M x", 15, 700, "middle", fill=TEAL), text(645, 245, "x-p", 15, 700, fill=RED), text(430, 430, "p in closed subspace M minimizes ||x-m||", 14, 650), text(430, 462, "x-p is orthogonal to every m in M", 14, 650), text(430, 492, "closed convex -> unique nearest point", 14, fill=MUTED), text(430, 516, "orthogonality additionally requires a subspace。", 14, fill=MUTED)]

    heading(out, 830, "C", "函数对象、采样与误差范数", RED)
    out += [path("M845 145C900 70 930 225 985 135C1030 62 1075 205 1135 112", BLUE, 3), text(840, 90, "continuum function f", 15, 700, fill=BLUE)]
    for x, y in ((860, 132), (915, 158), (970, 151), (1025, 105), (1080, 168), (1130, 118)):
        out.append(circle(x, y, 5, RED, RED))
    out += [line(990, 220, 990, 252, INK, 2, marker="a3")]
    node(out, 840, 265, 300, 62, "sample vector + quadrature weights", TEAL, size=14)
    out += [line(990, 330, 990, 362, INK, 2, marker="a3")]
    node(out, 840, 375, 300, 62, "finite representation / model", BLUE, size=14)
    out += [text(830, 475, "L2 / sup / Sobolev norms ask different questions", 14, 650, fill=RED), text(830, 505, "grid error != continuum function-space error。", 14, fill=MUTED)]
    return finish(out, "完备性保证极限不逃出空间；Hilbert 结构再给正交投影，但离散采样仍需单独误差合同。")


def bounded_compact_spectrum():
    out = begin(
        "Bounded、compact operators 与无限维 spectrum",
        "Bounded linear operator 等价于连续并由 operator norm 控制；compact operator 把 bounded sequences 送到具有收敛子列的 sequences；无限维 spectrum 由不可有界可逆性定义，不只含 eigenvalues，compact self-adjoint 情形才恢复离散正交谱展开。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "bounded = 线性作用的稳定合同", BLUE)
    out += [circle(115, 220, 80, BLUE, BG, 2.5), text(115, 225, "unit ball", 15, 700, "middle", fill=BLUE), line(205, 220, 250, 220, INK, 2.4, marker="a3")]
    out.append('<ellipse cx="315" cy="220" rx="55" ry="120" fill="none" stroke="%s" stroke-width="2.5"/>' % TEAL)
    out += [text(315, 225, "T(B_X)", 15, 700, "middle", fill=TEAL), text(45, 390, "||Tx|| <= ||T|| ||x||", 16, 700, cls="math"), text(45, 425, "linear + bounded  <=>  continuous", 15, 650), text(45, 463, "invertible algebraically is not enough", 15, 650, fill=RED), text(45, 500, "bounded inverse is a separate requirement。", 14, fill=MUTED)]

    heading(out, 430, "B", "compact：有界序列恢复收敛子列", TEAL)
    for i, (x, y) in enumerate(((455, 135), (520, 190), (475, 285), (600, 120), (690, 190), (730, 315), (570, 345))):
        out.append(circle(x, y, 5, BLUE, BLUE))
    out += [line(600, 235, 645, 235, INK, 2.4, marker="a3")]
    for i in range(7):
        out.append(circle(705 + i * 7, 235 + (-1) ** i * (18 - 2 * i), 4, TEAL, TEAL))
    out += [circle(760, 235, 7, RED, RED), text(430, 392, "bounded sequence (x_n)", 14, 650), text(430, 420, "-> some (Tx_nk) converges", 14, 650, fill=TEAL), text(430, 452, "compact does not require T(B_X) closed", 14, 650), text(430, 484, "identity on infinite-dimensional H: not compact", 14, 650, fill=RED), text(430, 514, "finite rank and norm limits are compact。", 14, fill=MUTED)]

    heading(out, 830, "C", "spectrum 不只等于 eigenvalues", RED)
    node(out, 840, 88, 300, 58, "T - lambda I has no bounded inverse", RED, size=14)
    out += [line(990, 149, 990, 184, INK, 2, marker="a3")]
    for i, label in enumerate(("point", "continuous", "residual")):
        node(out, 840 + i * 103, 195, 94, 52, label, (BLUE, TEAL, RED)[i], size=14)
    out += [line(990, 252, 990, 285, INK, 2, marker="a3")]
    out += [rect(840, 298, 300, 72, TEAL, BG, 8, 2), text(990, 326, "compact self-adjoint: orthogonal modes", 14, 650, "middle", fill=TEAL), text(990, 353, "nonzero spectrum accumulates only at 0", 14, 650, "middle", fill=TEAL)]
    out += [text(830, 420, "0 can be spectral but not an eigenvalue", 14, 650, fill=RED), text(830, 455, "finite sections may mislead", 14, 650), text(830, 495, "matrix intuition needs extra structure。", 14, fill=MUTED)]
    return finish(out, "Boundedness controls stability，compactness restores subsequences；只有附加结构才把无限维 spectrum 化成矩阵式特征展开。")


def positive_kernel_rkhs():
    out = begin(
        "Positive kernel、RKHS 与 representer theorem",
        "PSD kernel 的入口量词是任意有限 Gram matrix 半正定；canonical sections 完备化为 RKHS，点值由 inner product 再生；对经验损失加单调 Hilbert norm regularization 时，最优解落在 sample kernel sections 的有限 span。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "PSD Gram 是全称量词", BLUE)
    pts = ((75, 125), (150, 95), (235, 145), (320, 105))
    for i, (x, y) in enumerate(pts):
        out += [circle(x, y, 7, BLUE, BLUE), text(x, y - 14, f"x{i+1}", 14, 650, "middle")]
    for i in range(4):
        for j in range(4):
            color = TEAL if i == j else GRID
            out.append(rect(90 + j * 42, 210 + i * 42, 36, 36, color, BG, 2, 1.8))
    out += [text(280, 260, "K_ij=k(x_i,x_j)", 15, 700, fill=TEAL), text(45, 410, "for every n, points and coefficients c", 14, 650), text(45, 442, "c^T K c >= 0", 17, 700, fill=BLUE, cls="math"), text(45, 478, "symmetric similarity alone is insufficient", 14, 650, fill=RED), text(45, 506, "one sampled PSD matrix proves only a finite test。", 14, fill=MUTED)]

    heading(out, 430, "B", "Reproducing property：点值连续", TEAL)
    out += [path("M455 300C500 90 565 370 625 165C675 30 730 280 770 120", BLUE, 3), circle(625, 165, 7, RED, RED), line(625, 165, 625, 350, RED, 2, "6 5")]
    out += [text(625, 385, "x", 15, 700, "middle", fill=RED), text(430, 420, "k_x = k(x, .) in H_k", 16, 650, cls="math"), text(430, 455, "f(x) = <f, k_x>_H", 17, 700, fill=TEAL, cls="math"), text(430, 490, "|f(x)| <= ||f|| sqrt(k(x,x))", 14, 650), text(430, 516, "bounded point evaluation is extra structure。", 14, fill=MUTED)]

    heading(out, 830, "C", "Representer：有限样本 span", RED)
    for i, y in enumerate((105, 175, 245)):
        node(out, 840, y, 120, 48, f"(x_{i+1}, y_{i+1})", BLUE, size=14)
        out.append(line(963, y + 24, 1000, 260, GRID, 1.8))
    node(out, 985, 225, 155, 70, "f* = Σ alpha_i k_xi", TEAL, size=14)
    out += [line(1072, 298, 1072, 332, INK, 2, marker="a3")]
    node(out, 840, 345, 300, 58, "finite Gram system + conditioning", BLUE, size=14)
    out += [text(830, 450, "loss uses sample values + norm regularizer", 14, 650), text(830, 480, "monotonicity removes the orthogonal part", 14, 650, fill=RED), text(830, 510, "finite span requires explicit hypotheses。", 14, fill=MUTED)]
    return finish(out, "Kernel 先通过所有有限 PSD 测试定义几何；RKHS 再生点值，representer theorem 在明确损失与正则条件下完成有限化。")


def weak_sobolev_operator():
    out = begin(
        "Weak derivative、Sobolev spaces 与 neural operators",
        "Weak derivative 通过对所有测试函数的分部积分定义；Sobolev norm 同时控制函数和弱导数，embedding、trace 与 compactness 需要域和指数条件；弱 PDE 经变分适定性和离散误差后才连接函数到函数的 neural operator。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "弱导数：把微分移给测试函数", BLUE)
    out += [line(55, 285, 350, 285, GRID, 2), line(200, 100, 200, 355, GRID, 2), path("M70 180L200 285L335 175", BLUE, 3), text(75, 150, "u(x)=|x|", 15, 700, fill=BLUE)]
    out += [path("M75 380L195 380L205 330L335 330", RED, 3), text(75, 420, "weak u' = sign(x) a.e.", 15, 700, fill=RED), text(45, 465, "integral u D phi = - integral v phi", 15, 650, cls="math"), text(45, 500, "identity holds for every compactly supported test。", 14, fill=MUTED)]

    heading(out, 430, "B", "Sobolev：正则、边界与紧性合同", TEAL)
    node(out, 445, 90, 310, 58, "W^{k,p}: u and weak derivatives in Lp", TEAL, size=14)
    out += [line(600, 151, 600, 182, INK, 2, marker="a3")]
    node(out, 445, 195, 310, 58, "embedding: W^{k,p} -> Lq / C^alpha", BLUE, size=14)
    out += [line(600, 256, 600, 287, INK, 2, marker="a3")]
    node(out, 445, 300, 310, 58, "trace / compactness / Poincare", RED, size=14)
    out += [text(430, 410, "dimension + exponent + domain regularity matter", 14, 650, fill=RED), text(430, 445, "H_0^1 closure encodes boundary values weakly", 14, 650), text(430, 480, "weak compactness != strong compactness", 14, 650), text(430, 510, "embeddings require dimension/domain hypotheses。", 14, fill=MUTED)]

    heading(out, 830, "C", "从弱 PDE 到 neural operator", RED)
    stages = (("input coefficient a in X", BLUE), ("weak problem: find u in V", TEAL), ("well-posed solution map G:X->Y", RED), ("discretize / learn / test in norms", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 82 + i * 90
        node(out, 840, yy, 300, 54, label, color, size=14)
        if i < 3:
            out.append(line(990, yy + 57, 990, yy + 83, INK, 2, marker="a3"))
    out += [text(830, 458, "low training residual != operator approximation", 14, 650, fill=RED), text(830, 487, "mesh sharing != resolution convergence", 14, 650), text(830, 516, "report data, discretization, model and solver errors。", 14, fill=MUTED)]
    return finish(out, "弱形式扩大可解对象；Sobolev 合同控制正则与边界，neural operator 还须跨输入函数族和离散层验收。")


FIGURES = {
    "fig-banach-hilbert-projection-v2.svg": banach_hilbert,
    "fig-bounded-compact-spectrum-v2.svg": bounded_compact_spectrum,
    "fig-positive-kernel-rkhs-representer-v2.svg": positive_kernel_rkhs,
    "fig-weak-sobolev-variational-operator-v2.svg": weak_sobolev_operator,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
