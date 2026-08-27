#!/usr/bin/env python3
"""Generate v2 textbook figures for NUM-13--16 iterative numerical methods."""

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


def arnoldi():
    out = begin(
        "Arnoldi 长递推、Ritz 证书与重启信息保留",
        "一般矩阵的 Krylov 正交化产生上 Hessenberg 投影；Ritz residual 可由 Arnoldi 关系廉价计算，但非正规性使小 residual 不等于小特征值误差；可靠实现还需重正交、锁定与保留目标不变子空间信息的重启。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一般矩阵需要长递推", BLUE)
    out += [text(45, 100, "w=A q_j", 17, 700, cls="math")]
    for i, y in enumerate((145, 195, 245, 295)):
        out += [circle(85, y, 7, BLUE, BLUE), text(105, y + 5, f"q_{i + 1}", 15, 650, fill=BLUE), line(140, y, 255, 315, GRID, 1.6)]
    out += [circle(255, 315, 9, TEAL, TEAL), text(270, 320, "orthogonal remainder", 15, 650, fill=TEAL)]
    out += [text(45, 360, "h_ij=q_i^* w； w <- w-q_i h_ij", 15, 650, cls="math")]
    for r in range(5):
        for c in range(5):
            active = r <= c + 1
            out.append(rect(105 + c * 38, 395 + r * 24, 32, 19, GRID, TEAL if active else BG, 0, 1.1))
    out += [text(45, 515, "A Q_k=Q_k H_k+h q_(k+1)e_k^T", 14, 650, cls="math")]

    heading(out, 430, "B", "Ritz residual 廉价，解释不廉价", TEAL)
    node(out, 445, 95, 310, 56, "H_k y = theta y", BLUE)
    out += [line(600, 154, 600, 195, INK, 2.3, marker="a3")]
    node(out, 445, 207, 310, 58, "u=Q_k y", TEAL)
    out += [line(600, 268, 600, 309, INK, 2.3, marker="a3")]
    node(out, 445, 321, 310, 68, "||A u-theta u||=|h e_k^T y|", RED, size=15)
    out += [text(430, 425, "normal A: residual + spectral gap", 15, 650), text(430, 456, "nonnormal A: also condition / pseudospectrum", 15, 650, fill=RED), text(430, 495, "small residual certifies an approximate pair,", 15, fill=MUTED), text(430, 518, "not automatically a small eigenvalue error。", 15, fill=MUTED)]

    heading(out, 830, "C", "正交与重启决定可持续性", RED)
    stages = (("expand to dimension m", BLUE), ("check Q^*Q and reorth", TEAL), ("select wanted Schur/Ritz vectors", RED), ("lock / restart with retained subspace", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 95 + i * 92
        node(out, 840, yy, 300, 55, label, color, size=15)
        if i < 3:
            out.append(line(990, yy + 58, 990, yy + 85, INK, 2.2, marker="a3"))
    out += [text(830, 477, "restart saves memory but can erase filters", 15, 650, fill=RED), text(830, 506, "report true residual, orthogonality and matvecs。", 15, fill=MUTED)]
    return finish(out, "Arnoldi 的核心产品不是一串 Ritz 值，而是带 residual、正交性与重启语义的投影证书。")


def svd_algorithms():
    out = begin(
        "SVD 算法分流、双对角化与双侧验收",
        "完整稠密 SVD 先经双侧正交变换约化为双对角结构；少量奇异三元组、谱范数和低秩值域分别适合 Golub–Kahan、交替幂迭代或随机值域；所有路径都应回到原矩阵检查双侧 residual、正交性和数据遍历成本。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先按交付物选择算法", BLUE)
    tasks = (("all / economy SVD", "bidiagonal + QR/DC/Jacobi", BLUE), ("top-k triplets", "Golub-Kahan / block Krylov", TEAL), ("sigma_1 only", "alternating power / Lanczos", RED), ("range Q", "randomized finder (p,q)", TEAL))
    for i, (task, method, color) in enumerate(tasks):
        yy = 102 + i * 88
        out += [circle(58, yy, 6, color, color), text(80, yy + 4, task, 15, 700, fill=color), text(80, yy + 29, method, 15, 650)]
    out += [line(45, 445, 365, 445, GRID, 2), text(45, 477, "target, rank, accuracy, passes", 15, 650), text(45, 506, "belong to the problem contract。", 15, fill=MUTED)]

    heading(out, 430, "B", "完整稠密路线保护奇异方向", TEAL)
    for r in range(5):
        for c in range(4):
            out.append(rect(445 + c * 34, 120 + r * 31, 28, 25, GRID, BLUE, 0, 1.1))
    out += [line(595, 198, 635, 198, RED, 3, marker="a2")]
    for r in range(5):
        for c in range(4):
            active = r == c or r == c + 1
            out.append(rect(650 + c * 34, 120 + r * 31, 28, 25, GRID, TEAL if active else BG, 0, 1.1))
    out += [text(430, 325, "U0^T A V0 = B bidiagonal", 16, 700, cls="math"), text(430, 361, "two-sided orthogonal transforms", 15, 650), text(430, 397, "then solve the small structured problem", 15, 650), text(430, 450, "do not explicitly form A^T A", 16, 700, fill=RED), text(430, 486, "small singular values are weak directions。", 15, fill=MUTED)]

    heading(out, 830, "C", "任何路径都回到原矩阵验收", RED)
    node(out, 840, 98, 300, 58, "candidate (sigma, u, v)", BLUE)
    out += [line(990, 159, 990, 195, INK, 2.2, marker="a3")]
    out += [rect(840, 207, 300, 75, TEAL, BG, 10, 2), text(990, 237, "r_R=A v-sigma u", 15, 650, "middle", fill=TEAL), text(990, 263, "r_L=A^T u-sigma v", 15, 650, "middle", fill=TEAL)]
    out += [line(990, 285, 990, 321, INK, 2.2, marker="a3")]
    node(out, 840, 333, 300, 72, "orthogonality + reconstruction", RED, size=15)
    out += [text(830, 444, "also report rank tolerance / gap", 15, 650), text(830, 473, "matvecs, data passes, memory and seeds", 15, 650), text(830, 506, "independent validation for randomized Q。", 15, fill=MUTED)]
    return finish(out, "SVD 的数值问题先由交付物分流，再由正交结构计算，最后由双侧 residual 与成本证书验收。")


def stationary_iteration():
    out = begin(
        "矩阵分裂、谱半径与非正规暂态",
        "定常迭代由 A=M-K 导出固定迭代矩阵 B=M^{-1}K；谱半径小于一等价于任意初值渐近收敛，但不同误差模态的阻尼、非正规暂态放大和 residual 到 error 的条件放大仍需分别分析。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一次分裂固定全部误差动力学", BLUE)
    node(out, 45, 105, 315, 55, "A=M-K； B=M^{-1}K", BLUE)
    out += [line(202, 163, 202, 199, INK, 2.2, marker="a3")]
    node(out, 45, 211, 315, 62, "x_(k+1)=B x_k+M^{-1}b", TEAL, size=15)
    out += [line(202, 276, 202, 312, INK, 2.2, marker="a3")]
    node(out, 45, 324, 315, 62, "e_(k+1)=B e_k", RED, size=16)
    out += [text(45, 425, "Jacobi: diagonal M； GS: triangular M", 15, 650), text(45, 456, "SOR / Richardson add a relaxation parameter", 15, 650), text(45, 498, "M^{-1} means solve Mz=y, not form inverse。", 15, fill=MUTED)]

    heading(out, 430, "B", "rho(B)<1 只给渐近结论", TEAL)
    out += [line(450, 350, 770, 350, GRID, 2), line(470, 390, 470, 105, GRID, 2)]
    modes = ((515, 145, BLUE, "slow mode"), (590, 225, TEAL, "middle"), (665, 300, RED, "fast mode"))
    for x, y, color, label in modes:
        out += [line(x, 350, x, y, color, 18), text(x, y - 14, label, 14, 650, "middle", fill=color)]
    out += [text(430, 410, "mode k decays like |lambda_i(B)|^k", 15, 650), text(430, 445, "all initial errors -> 0  iff  rho(B)<1", 16, 700, cls="math"), text(430, 484, "smoothers may damp high frequency first。", 15, fill=MUTED)]

    heading(out, 830, "C", "非正规矩阵可先放大再衰减", RED)
    out += [line(850, 370, 1145, 370, GRID, 2), line(870, 405, 870, 120, GRID, 2)]
    out += [path("M870 345 C910 330 920 185 980 190 C1040 195 1070 290 1135 335", RED, 3), line(875, 190, 1130, 335, TEAL, 2.5)]
    out += [text(1085, 190, "||B^k||", 15, 700, fill=RED), text(1080, 315, "rho^k", 15, 700, fill=TEAL), text(830, 425, "rho(B)<1 does not imply monotone ||e_k||", 15, 650), text(830, 456, "true residual r_k=b-Ax_k", 15, 650), text(830, 485, "error interpretation still needs condition(A)", 15, 650), text(830, 514, "and a scale-aware stopping rule。", 15, fill=MUTED)]
    return finish(out, "谱半径回答最终是否收敛；模态、非正规性与 residual 证书回答实际怎样收敛、何时可信停止。")


def krylov_preconditioning():
    out = begin(
        "Krylov 残差多项式、预条件谱重塑与总成本",
        "Krylov 方法从初始残差生成多项式搜索空间，并用不同投影条件选择近似解；预条件通过廉价近似求解重塑谱与几何，但左、右和对称形式有不同 residual 语义，最终应最小化达到原问题真残差的总时间而非单独最小化迭代数。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Krylov 方法选择残差多项式", BLUE)
    for i, label in enumerate(("r0", "A r0", "A^2 r0", "...", "A^(k-1)r0")):
        x = 45 + i * 69
        node(out, x, 115, 60, 48, label, BLUE if i < 3 else TEAL, size=13)
        if i < 4:
            out.append(line(x + 62, 139, x + 67, 139, INK, 1.8, marker="a3"))
    out += [text(45, 205, "x_k in x0+K_k(A,r0)", 16, 700, cls="math"), text(45, 245, "r_k=p_k(A)r0,  p_k(0)=1", 16, 700, cls="math")]
    choices = (("FOM", "r perpendicular K_k"), ("GMRES", "minimize ||r||_2"), ("CG / SPD", "energy-optimal geometry"))
    for i, (name, desc) in enumerate(choices):
        yy = 300 + i * 58
        out += [text(45, yy, name, 15, 700, fill=(BLUE, TEAL, RED)[i]), text(130, yy, desc, 15, 650)]
    out += [text(45, 505, "basis + projection define the method。", 15, fill=MUTED)]

    heading(out, 430, "B", "预条件重塑谱，也重写坐标", TEAL)
    out += [text(430, 100, "before", 15, 700, fill=RED), line(485, 96, 765, 96, GRID, 2)]
    for x in (500, 522, 575, 650, 735):
        out.append(circle(x, 96, 7, RED, RED))
    out += [text(430, 170, "after", 15, 700, fill=TEAL), line(485, 166, 765, 166, GRID, 2)]
    for x in (590, 603, 612, 621, 634):
        out.append(circle(x, 166, 7, TEAL, TEAL))
    out += [text(430, 225, "left:   M^{-1} A x=M^{-1} b", 15, 650, cls="math"), text(430, 263, "right:  A M^{-1} y=b； x=M^{-1}y", 15, 650, cls="math"), text(430, 301, "SPD: use a symmetry-preserving form", 15, 650)]
    out += [line(430, 337, 765, 337, GRID, 2), text(430, 371, "cluster / condition may improve", 15, 650), text(430, 407, "but nonnormality and variable M matter", 15, 650, fill=RED), text(430, 448, "always recompute r=b-Ax", 16, 700, fill=BLUE), text(430, 486, "preconditioned residual has another scale。", 15, fill=MUTED)]

    heading(out, 830, "C", "最优目标是真残差总时间", RED)
    labels = (("none", 35, 18, BLUE), ("cheap M", 20, 38, TEAL), ("strong M", 10, 95, RED))
    for i, (label, iters, setup, color) in enumerate(labels):
        yy = 115 + i * 115
        out += [text(830, yy, label, 15, 700, fill=color), rect(915, yy - 18, iters * 2.0, 22, color, color, 0, 0), rect(915 + iters * 2.0, yy - 18, setup * 1.2, 22, color, BG, 0, 2), text(1140, yy, "iter + setup", 14, 650, "end")]
    out += [text(830, 432, "total = setup + apply + matvec +", 15, 650), text(830, 455, "orthogonalization + reductions", 15, 650), text(830, 490, "include memory, communication and reuse。", 15, fill=MUTED), text(830, 518, "fewer iterations can still cost more。", 15, 700, fill=RED)]
    return finish(out, "预条件不是抽象地让谱更好，而是在保持原方程验收语义下交换 setup、单步成本与迭代次数。")


FIGURES = {
    "fig-arnoldi-restart-nonnormal-v2.svg": arnoldi,
    "fig-svd-algorithms-certificates-v2.svg": svd_algorithms,
    "fig-stationary-spectral-radius-v2.svg": stationary_iteration,
    "fig-krylov-preconditioning-v2.svg": krylov_preconditioning,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
