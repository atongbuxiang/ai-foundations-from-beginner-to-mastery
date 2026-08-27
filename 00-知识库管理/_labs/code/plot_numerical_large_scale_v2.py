#!/usr/bin/env python3
"""Generate v2 textbook figures for NUM-17--20 large-scale methods."""

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


def conjugate_gradient():
    out = begin(
        "共轭梯度的能量几何、谱收敛与有限精度契约",
        "SPD 线性系统等价于严格凸二次优化；CG 在 Krylov 空间中最小化 A 能量误差并生成 A 共轭方向，速度受预条件谱分布控制；有限精度会使递推 residual 漂移，因此必须周期性重算真 residual 并监测曲率。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "SPD 把线性方程变成能量最小化", BLUE)
    for rx, ry in ((145, 52), (112, 40), (78, 28)):
        out.append(f'<ellipse cx="205" cy="270" rx="{rx}" ry="{ry}" transform="rotate(-28 205 270)" fill="none" stroke="{GRID}" stroke-width="2"/>')
    pts_sd = ((70, 380), (230, 335), (155, 260), (225, 278), (205, 270))
    for i in range(len(pts_sd) - 1):
        out.append(line(*pts_sd[i], *pts_sd[i + 1], RED, 2.2, marker="a2"))
    pts_cg = ((70, 380), (275, 330), (205, 270))
    for i in range(len(pts_cg) - 1):
        out.append(line(*pts_cg[i], *pts_cg[i + 1], BLUE, 3, marker="a1"))
    out += [circle(205, 270, 7, TEAL, TEAL), text(217, 260, "x*", 16, 700, fill=TEAL), text(45, 445, "phi(x)=1/2 x^T A x-b^T x", 16, 700, cls="math"), text(45, 478, "CG: minimize ||x-x*||_A in x0+K_k", 15, 650), text(45, 507, "steepest descent ignores accumulated geometry。", 15, fill=MUTED)]

    heading(out, 430, "B", "四个不变量连接同一算法", TEAL)
    invariants = (("r_i^T r_j=0", "residual orthogonality", BLUE), ("p_i^T A p_j=0", "A-conjugate directions", TEAL), ("x_k in x0+K_k", "Krylov containment", RED), ("min ||x-x*||_A", "energy optimality", BLUE))
    for i, (eq, desc, color) in enumerate(invariants):
        yy = 102 + i * 83
        out += [text(430, yy, eq, 16, 700, fill=color, cls="math"), text(430, yy + 27, desc, 15, 650)]
    out += [line(430, 430, 765, 430, GRID, 2), text(430, 461, "worst-case bound uses kappa", 15, 650), text(430, 487, "actual speed also uses spectral clusters。", 15, fill=MUTED)]

    heading(out, 830, "C", "PCG 与浮点实现必须验收", RED)
    stages = (("verify A=A^T and positive curvature", BLUE), ("solve M z_k=r_k； require SPD M", TEAL), ("update x,r,p by short recurrences", RED), ("recompute true r=b-Ax periodically", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 92 + i * 91
        node(out, 840, yy, 300, 56, label, color, size=14)
        if i < 3:
            out.append(line(990, yy + 59, 990, yy + 84, INK, 2.1, marker="a3"))
    out += [text(830, 474, "recursive residual can reach a false floor", 15, 650, fill=RED), text(830, 503, "report true residual, curvature and matvecs。", 15, fill=MUTED)]
    return finish(out, "CG 的短递推来自 SPD 能量几何；速度由预条件谱决定，可信停止由原方程真 residual 决定。")


def gmres_minres():
    out = begin(
        "GMRES、MINRES 的结构选择、残差最小化与重启",
        "一般方阵的 GMRES 用 Arnoldi 将原残差最小化压缩为小型 Hessenberg 最小二乘；对称不定矩阵的 MINRES 用 Lanczos 保持短递推；重启与预条件会改变搜索空间或 residual 语义，因此最终必须回到原方程验收。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先由可信结构选择方法", BLUE)
    rows = (("SPD", "CG / PCG", BLUE), ("symmetric indefinite", "MINRES / MINRES-QLP", TEAL), ("general square", "GMRES / FGMRES", RED), ("rectangular LS", "LSQR / LSMR", TEAL))
    for i, (structure, method, color) in enumerate(rows):
        yy = 105 + i * 85
        out += [circle(58, yy, 6, color, color), text(80, yy + 4, structure, 15, 700, fill=color), text(80, yy + 29, method, 15, 650)]
    out += [line(45, 445, 365, 445, GRID, 2), text(45, 475, "symmetry and definiteness are contracts,", 15, 650), text(45, 500, "not guesses from the application name。", 15, fill=MUTED)]

    heading(out, 430, "B", "GMRES 压缩为小最小二乘", TEAL)
    node(out, 445, 92, 310, 58, "Arnoldi: A V_k=V_(k+1) Hbar_k", BLUE, size=14)
    out += [line(600, 153, 600, 190, INK, 2.2, marker="a3")]
    node(out, 445, 202, 310, 70, "min_y ||beta e1-Hbar_k y||_2", TEAL, size=15)
    out += [line(600, 275, 600, 312, INK, 2.2, marker="a3")]
    node(out, 445, 324, 310, 62, "x_k=x0+V_k y_k", RED, size=15)
    out += [text(430, 425, "Givens updates residual norm online", 15, 650), text(430, 456, "full GMRES residual is nonincreasing", 15, 650), text(430, 487, "GMRES(m) discards part of the polynomial。", 15, fill=MUTED)]

    heading(out, 830, "C", "MINRES、重启与 residual 语义", RED)
    out += [text(830, 100, "symmetric indefinite", 16, 700, fill=TEAL), text(830, 130, "Lanczos tridiagonal + residual LS", 15, 650), text(830, 170, "CG curvature may fail；MINRES remains legal", 15, 650, fill=RED)]
    out += [line(830, 200, 1145, 200, GRID, 2)]
    stages = (("expand m steps", BLUE), ("retain useful spectral information", TEAL), ("restart / flexible update", RED))
    for i, (label, color) in enumerate(stages):
        yy = 225 + i * 76
        node(out, 840, yy, 300, 48, label, color, size=14)
        if i < 2:
            out.append(line(990, yy + 51, 990, yy + 70, INK, 2, marker="a3"))
    out += [text(830, 457, "left/right preconditioning changes norms", 15, 650), text(830, 486, "recompute true r=b-Ax and orthogonality。", 15, fill=MUTED)]
    return finish(out, "最小残差只在当前搜索空间与当前坐标中成立；结构合法性、重启信息与真 residual 决定生产可靠性。")


def sparse_computing():
    out = begin(
        "稀疏格式、访存主导计算与填充负载",
        "稀疏矩阵需要把数值、索引和指针共同编码；SpMV 等内核通常受访存和非零分布主导；直接分解的填充及并行负载又取决于图排序与划分，因此 nnz 只是成本模型的起点。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "格式编码结构，也规定遍历", BLUE)
    pattern = ((0, 0), (0, 3), (1, 1), (2, 0), (2, 2), (3, 1), (3, 3))
    for r in range(4):
        for c in range(4):
            fill = BLUE if (r, c) in pattern else BG
            out.append(rect(48 + c * 42, 105 + r * 42, 34, 34, GRID, fill, 0, 1.2))
    out += [text(235, 118, "COO", 16, 700, fill=BLUE), text(235, 148, "(row,col,val) stream", 15, 650), text(235, 202, "CSR", 16, 700, fill=TEAL), text(235, 232, "rowptr + colind + val", 15, 650), text(235, 286, "CSC", 16, 700, fill=RED), text(235, 316, "colptr + rowind + val", 15, 650)]
    out += [line(45, 365, 365, 365, GRID, 2), text(45, 399, "canonicalize: sort + merge duplicates", 15, 650), text(45, 431, "explicit zero still costs storage/work", 15, 650), text(45, 476, "missing entry != numerical zero", 16, 700, fill=RED), text(45, 505, "choose format from operations, not fashion。", 15, fill=MUTED)]

    heading(out, 430, "B", "算术少，数据移动仍昂贵", TEAL)
    out += [text(430, 105, "SpMV: y=A x", 17, 700, fill=TEAL), text(430, 142, "~ 2 nnz flops", 16, 650), text(430, 176, "values + indices + irregular x gathers", 15, 650)]
    out += [rect(450, 220, 275, 30, BLUE, BG, 0, 2), rect(450, 220, 58, 30, BLUE, BLUE, 0, 0), text(735, 242, "compute / memory traffic", 14, 650, "end")]
    out += [text(430, 292, "SpMM can reuse rows and amortize indices", 15, 650), text(430, 329, "SpGEMM output pattern is data-dependent", 15, 650), text(430, 366, "block formats help only with real block density", 15, 650)]
    out += [line(430, 404, 765, 404, GRID, 2), text(430, 438, "report bytes, bandwidth, padding,", 15, 650), text(430, 461, "kernel launch and synchronization", 15, 650), text(430, 500, "not only arithmetic complexity。", 15, fill=MUTED)]

    heading(out, 830, "C", "排序决定填充，划分决定尾部", RED)
    for k, x0 in enumerate((840, 975)):
        for r in range(5):
            for c in range(5):
                if k == 0:
                    active = r == c or abs(r - c) == 1
                else:
                    active = r == c or abs(r - c) <= 2
                color = RED if k == 1 and abs(r - c) == 2 else TEAL if active else BG
                out.append(rect(x0 + c * 24, 115 + r * 24, 20, 20, GRID, color, 0, 1))
    out += [text(840, 265, "original pattern", 14, 650), text(975, 265, "factor fill", 14, 650), text(830, 310, "ordering changes elimination tree + fill", 15, 650), text(830, 346, "pivoting may alter the symbolic forecast", 15, 650, fill=RED)]
    loads = (55, 105, 38, 92)
    for i, width in enumerate(loads):
        yy = 390 + i * 29
        out += [text(830, yy + 14, f"worker {i + 1}", 13, 650), rect(900, yy, width * 1.8, 17, BLUE if i != 1 else RED, BLUE if i != 1 else RED, 0, 0)]
    out += [text(830, 520, "same nnz can have different load balance。", 15, fill=MUTED)]
    return finish(out, "稀疏成本由格式语义、访存、输出结构、填充与负载共同决定；nnz 从来不是完整性能证书。")


def randomized_svd():
    out = begin(
        "随机值域、过采样幂步与独立概率证书",
        "随机 SVD 先用独立随机探针捕获近似值域，再在小空间中执行确定性 SVD；过采样降低漏方向尾部风险，幂步用额外数据遍历放大谱隙；另一组独立探针可对投影 residual 建立带失败概率的后验证书。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "两阶段把大问题压到小空间", BLUE)
    stages = (("Omega", BLUE), ("Y=A Omega", TEAL), ("Q=orth(Y)", BLUE), ("B=Q^T A", TEAL), ("small SVD", RED))
    for i, (label, color) in enumerate(stages):
        yy = 92 + i * 73
        node(out, 65, yy, 270, 45, label, color, size=15)
        if i < 4:
            out.append(line(200, yy + 48, 200, yy + 67, INK, 2, marker="a3"))
    out += [text(45, 478, "A_k ~= (Q U_tilde_k) Sigma_k V_k^T", 14, 650, cls="math"), text(45, 506, "range error and truncation error are distinct。", 15, fill=MUTED)]

    heading(out, 430, "B", "p 降尾险，q 放大谱隙", TEAL)
    out += [text(430, 105, "sketch width l=k+p", 17, 700, fill=BLUE), text(430, 140, "oversampling p adds insurance directions", 15, 650)]
    out += [line(450, 245, 765, 245, GRID, 2)]
    for i, h in enumerate((135, 105, 78, 55, 38)):
        x = 485 + i * 58
        out += [line(x, 245, x, 245 - h, BLUE, 14), line(x + 17, 245, x + 17, 245 - h * 0.55, TEAL, 14)]
    out += [text(430, 280, "q=0", 14, 650, fill=BLUE), text(510, 280, "q>0: sigma_i^(2q+1)", 14, 650, fill=TEAL)]
    out += [text(430, 330, "power steps sharpen slow spectral decay", 15, 650), text(430, 365, "but add A/A^T passes + rounding risk", 15, 650, fill=RED), text(430, 414, "reorthogonalize between applications", 15, 650), text(430, 451, "record p, q, seed and pass budget", 15, 650), text(430, 493, "expectation != a single-run guarantee。", 15, fill=MUTED)]

    heading(out, 830, "C", "独立探针把经验变成证书", RED)
    node(out, 840, 95, 300, 56, "fresh Gaussian omega_j", BLUE, size=15)
    out += [line(990, 154, 990, 193, INK, 2.2, marker="a3")]
    node(out, 840, 205, 300, 72, "z_j=(I-Q Q^T) A omega_j", TEAL, size=14)
    out += [line(990, 280, 990, 319, INK, 2.2, marker="a3")]
    node(out, 840, 331, 300, 66, "max_j ||z_j|| -> probabilistic bound", RED, size=14)
    out += [text(830, 438, "validation probes must not train Q", 15, 700, fill=RED), text(830, 470, "state norm, probe count and failure delta", 15, 650), text(830, 502, "also evaluate downstream task loss。", 15, fill=MUTED)]
    return finish(out, "随机低秩算法用 p、q 与数据遍历换取近似质量，并用独立后验探针把单次运行升级为概率证书。")


FIGURES = {
    "fig-conjugate-gradient-contract-v2.svg": conjugate_gradient,
    "fig-gmres-minres-restart-v2.svg": gmres_minres,
    "fig-sparse-computing-contract-v2.svg": sparse_computing,
    "fig-randomized-svd-certificate-v2.svg": randomized_svd,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
