#!/usr/bin/env python3
"""Generate v2 textbook figures for NUM-09--12 least-squares and spectra."""

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


def least_squares_stability():
    out = begin(
        "最小二乘投影、正规方程条件数平方与算法选择",
        "最小二乘将 b 投影到 A 的列空间并使残差正交；形成 A 转置 A 会把奇异值平方并将条件数平方；QR、QRCP 与 SVD 在稳定性、秩诊断、最小范数和成本上承担不同职责。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "解是列空间中的正交投影", BLUE)
    out += [path("M60 400L345 210", BLUE, 3), text(285, 230, "range(A)", 16, 700, fill=BLUE)]
    p, b = (230, 287), (300, 125)
    out += [circle(*p, 7, TEAL, TEAL), circle(*b, 7, RED, RED), line(p[0], p[1], b[0], b[1], RED, 3, marker="a2"), line(85, 383, p[0], p[1], TEAL, 3, marker="a1")]
    out += [text(310, 118, "b", 16, 700, fill=RED), text(235, 310, "A x*", 16, 700, fill=TEAL), text(265, 220, "r=b-Ax*", 15, 650, fill=RED)]
    out += [path("M228 270L245 278L237 295", INK, 2), text(45, 445, "A^T r = 0", 18, 700, cls="math"), text(45, 478, "small residual != accurate parameters", 15, fill=MUTED), text(45, 501, "when weak directions amplify noise。", 15, fill=MUTED)]

    heading(out, 430, "B", "三条计算路径保留不同信息", TEAL)
    rows = (("normal equations", "A^T A x=A^T b", "kappa becomes kappa(A)^2", RED), ("Householder QR", "R x=Q^T b", "stable full-rank baseline", TEAL), ("QRCP / SVD", "rank-revealing filter", "rank + min-norm control", BLUE))
    for i, (label, eq, desc, color) in enumerate(rows):
        yy = 98 + i * 130
        out += [text(430, yy, label, 17, 700, fill=color), text(430, yy + 34, eq, 16, 650, cls="math"), text(430, yy + 67, desc, 15, 650, fill=MUTED)]
        if i < 2:
            out.append(line(430, yy + 90, 765, yy + 90, GRID, 2))
    out += [text(430, 488, "tolerance belongs to the", 15, fill=RED), text(430, 511, "numerical problem definition。", 15, fill=RED)]

    heading(out, 830, "C", "算法选择取决于秩与任务", RED)
    cases = (("full rank, dense", "Householder QR", TEAL), ("rank uncertain", "QRCP / COD", BLUE), ("min norm / weak modes", "SVD / TSVD / ridge", RED), ("streaming / sparse", "iterative or updating QR", TEAL))
    for i, (case, method, color) in enumerate(cases):
        yy = 100 + i * 83
        out += [circle(850, yy, 6, color, color), text(872, yy + 4, case, 15, 700, fill=color), text(872, yy + 29, method, 15, 650)]
    out += [line(830, 430, 1145, 430, GRID, 2), text(830, 458, "verify residual, A^T r, rank", 15, 650), text(830, 481, "and parameter sensitivity", 15, 650), text(830, 510, "regularization also changes the target。", 15, fill=MUTED)]
    return finish(out, "正规方程是正确公式但可能是错误执行路径；稳定求解要同时保护投影、秩和弱方向。")


def power_inverse_rqi():
    out = begin(
        "幂法、移位反幂法与 Rayleigh 商迭代的谱过滤",
        "幂法用多项式 lambda 的幂放大主模方向；反幂法用一除以 lambda 减 sigma 放大离移位最近的方向；对称单特征值附近的 Rayleigh 商迭代更新移位并具有局部三次角误差收敛，但每步线性求解和 residual 仍需验收。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "幂法按谱比过滤方向", BLUE)
    out += [line(55, 355, 365, 355, GRID, 2), line(85, 395, 85, 100, GRID, 2)]
    bars = ((125, 125, BLUE, "lambda1"), (205, 205, TEAL, "lambda2"), (285, 280, RED, "lambda3"))
    for x, y, color, label in bars:
        out += [line(x, 355, x, y, color, 18), text(x, y - 15, label, 15, 650, "middle", fill=color)]
    out += [text(45, 420, "coefficient ratio after k steps", 16, 650), text(45, 453, "~ |lambda2/lambda1|^k", 17, 700, cls="math"), text(45, 486, "fails if target component is zero", 15, fill=MUTED), text(45, 509, "or dominant moduli tie。", 15, fill=MUTED)]

    heading(out, 430, "B", "shift-invert 把最近特征值变成最大", TEAL)
    out += [line(450, 270, 770, 270, GRID, 2), text(455, 300, "lambda", 15, 650)]
    eigs = ((500, BLUE), (575, TEAL), (685, RED), (735, BLUE))
    for x, color in eigs:
        out += [circle(x, 270, 7, color, color), line(x, 255, x, 285, color, 2)]
    sigma = 650
    out += [line(sigma, 150, sigma, 390, RED, 2.5, "7 5"), text(sigma, 135, "shift sigma", 15, 700, "middle", fill=RED), line(650, 410, 690, 410, RED, 3, marker="a2")]
    out += [text(430, 110, "eigenvalues become 1/(lambda_i-sigma)", 16, 650, cls="math"), text(430, 436, "nearest lambda becomes dominant", 15, 650), text(430, 475, "solve (A-sigma I)y=x；", 15, fill=MUTED), text(430, 498, "never form the inverse。", 15, fill=MUTED)]

    heading(out, 830, "C", "RQI 更新 shift，但只局部超快", RED)
    stages = (("x_k", BLUE), ("rho_k=x_k^T A x_k", TEAL), ("solve (A-rho_k I)y=x_k", RED), ("normalize -> x_(k+1)", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 95 + i * 90
        node(out, 840, yy, 300, 52, label, color, size=15)
        if i < 3:
            out.append(line(990, yy + 54, 990, yy + 83, INK, 2.2, marker="a3"))
    out += [text(830, 451, "symmetric + simple + local", 15, 650, fill=RED), text(830, 474, "regime: cubic angle convergence", 15, 650, fill=RED), text(830, 503, "stop by residual；interpret with gap。", 15, fill=MUTED)]
    return finish(out, "谱迭代的速度由过滤函数与谱间隙决定；可信结果仍由 residual 和求解质量认证。")


def hessenberg_qr():
    out = begin(
        "Hessenberg 约化、隐式移位 QR 与 deflation",
        "一般稠密矩阵先经双侧 Householder 正交相似约化为上 Hessenberg，再用隐式移位和 bulge chasing 保持带宽，以尺度感知 deflation 收缩活跃块并得到 Schur 形式；后向稳定不消除非正规特征值敏感性。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一次 O(n^3) 约化保留相似性", BLUE)
    # Dense and Hessenberg patterns.
    for r in range(5):
        for c in range(5):
            out.append(rect(50 + c * 36, 115 + r * 36, 30, 30, GRID, BLUE if (r + c) % 2 else BG, 0, 1.5))
    out += [line(240, 205, 280, 205, RED, 3, marker="a2")]
    for r in range(5):
        for c in range(5):
            fill = TEAL if r <= c + 1 else BG
            out.append(rect(290 + c * 18, 135 + r * 36, 16, 30, GRID, fill, 0, 1))
    out += [text(45, 335, "Q0^T A Q0 = H", 18, 700, cls="math"), text(45, 375, "H is upper Hessenberg", 16, 650, fill=TEAL), text(45, 414, "trace, spectrum and 2-norm", 15, 650), text(45, 437, "are preserved", 15, 650), text(45, 482, "later QR steps cost O(n^2)。", 15, fill=MUTED)]

    heading(out, 430, "B", "隐式 shift 产生并追逐 bulge", TEAL)
    # Bulge snapshots.
    for k, x0 in enumerate((440, 555, 670)):
        for r in range(5):
            for c in range(5):
                active = r <= c + 1 or (r == min(4, k + 2) and c == k)
                color = RED if (r == min(4, k + 2) and c == k and r > c + 1) else TEAL if active else BG
                out.append(rect(x0 + c * 13, 150 + r * 35, 11, 28, GRID, color, 0, 1))
        if k < 2:
            out.append(line(x0 + 72, 220, x0 + 102, 220, INK, 2, marker="a3"))
    out += [text(430, 365, "Francis step: form first column", 15, 650), text(430, 388, "without explicit QR factors", 15, 650), text(430, 423, "chase the bulge back to band", 15, 650), text(430, 458, "implicit Q theorem fixes the step", 15, 650), text(430, 493, "shift: speed；orthogonality: stability。", 15, fill=MUTED)]

    heading(out, 830, "C", "deflation 收缩到 Schur blocks", RED)
    node(out, 840, 100, 300, 55, "active Hessenberg block", BLUE)
    out += [line(990, 158, 990, 198, INK, 2.4, marker="a3")]
    node(out, 840, 210, 300, 68, "test |h_(i+1,i)| against local scale", TEAL, size=15)
    out += [line(990, 281, 990, 321, INK, 2.4, marker="a3")]
    node(out, 840, 333, 300, 68, "split -> 1x1 / real 2x2 Schur blocks", RED, size=15)
    out += [text(830, 441, "verify ||A Q-Q T|| and Q^T Q-I", 15, 650, cls="math"), text(830, 472, "stable Schur form != accurate", 15, 650, fill=RED), text(830, 495, "eigenvectors for nonnormal A", 15, 650, fill=RED), text(830, 518, "report conditioning context。", 15, fill=MUTED)]
    return finish(out, "稠密 QR 特征值算法依靠 Hessenberg 结构、隐式移位和 deflation 达到 O(n^3) 总成本。")


def lanczos():
    out = begin(
        "Lanczos 三项递推、Ritz residual 与有限精度正交性",
        "对称矩阵的 Krylov 投影产生小型三对角 T_k；Ritz residual 可由最后一个递推系数廉价计算；浮点中已收敛方向会重新进入递推并产生 ghost Ritz values，因此需要重正交、锁定与重启。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "对称性把长 Arnoldi 化成三项递推", BLUE)
    for i, label in enumerate(("q_(k-1)", "q_k", "A q_k", "q_(k+1)")):
        x = 45 + i * 90
        node(out, x, 115, 72, 50, label, BLUE if i < 2 else TEAL, size=15)
        if i < 3:
            out.append(line(x + 74, 140, x + 86, 140, INK, 2, marker="a3"))
    out += [text(45, 220, "beta_(k-1) q_(k-1) + alpha_k q_k + beta_k q_(k+1)", 14, 650, cls="math")]
    # Tridiagonal sketch.
    for r in range(5):
        for c in range(5):
            active = abs(r - c) <= 1
            out.append(rect(105 + c * 38, 285 + r * 34, 32, 28, GRID, TEAL if active else BG, 0, 1.2))
    out += [text(45, 479, "T_k = Q_k^T A Q_k", 15, 650), text(45, 502, "tridiagonal；maintain Q_k^T Q_k ~= I。", 15, fill=MUTED)]

    heading(out, 430, "B", "Ritz residual 几乎免费", TEAL)
    node(out, 445, 105, 310, 56, "T_k y = theta y", BLUE)
    out += [line(600, 164, 600, 205, INK, 2.5, marker="a3")]
    node(out, 445, 218, 310, 65, "u=Q_k y", TEAL)
    out += [line(600, 286, 600, 327, INK, 2.5, marker="a3")]
    node(out, 445, 340, 310, 72, "||A u-theta u|| = |beta_k e_k^T y|", RED, size=15)
    out += [text(430, 455, "extreme Ritz values often converge first", 15, 650), text(430, 487, "vector accuracy also needs a spectral gap。", 15, fill=MUTED)]

    heading(out, 830, "C", "短递推仍需正交性管理", RED)
    out += [line(850, 250, 1140, 250, GRID, 2)]
    for i, x in enumerate((875, 930, 990, 1050, 1110)):
        color = RED if i in (1, 4) else BLUE
        out += [circle(x, 250, 8, color, color), text(x, 220 - (i % 2) * 28, "theta" if i not in (1, 4) else "ghost", 15, 650, "middle", fill=color)]
    out += [text(830, 315, "roundoff breaks Q_k^T Q_k=I", 16, 700, fill=RED), text(830, 352, "converged directions can re-enter", 15, 650), text(830, 375, "and create ghost Ritz values", 15, 650), text(830, 410, "remedies", 17, 700, fill=TEAL), text(830, 440, "full/selective reorthogonalization", 15, 650), text(830, 469, "locking + thick/implicit restart", 15, 650), text(830, 502, "distinguish lucky/numerical breakdown。", 15, fill=MUTED)]
    return finish(out, "Lanczos 的三项递推只降低每步结构成本；可靠 eigensolver 仍由 residual、gap 和正交性管理组成。")


FIGURES = {
    "fig-least-squares-stability-v2.svg": least_squares_stability,
    "fig-power-inverse-rqi-v2.svg": power_inverse_rqi,
    "fig-hessenberg-qr-v2.svg": hessenberg_qr,
    "fig-lanczos-ritz-orthogonality-v2.svg": lanczos,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
