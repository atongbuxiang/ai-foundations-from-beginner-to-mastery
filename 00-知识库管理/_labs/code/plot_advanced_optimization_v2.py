#!/usr/bin/env python3
"""Generate v2 textbook figures for OPT-13--16 advanced optimization."""

from __future__ import annotations

import math
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


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "optimization"


def polyline(points, color, width=2.5, dash=None, marker=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, color, width, "none", dash, marker)


def duality_certificate():
    out = begin(
        "弱对偶、Slater 强对偶与 primal-dual 证书",
        "每个 dual feasible multiplier 给 primal optimum 的下界；Slater 在凸问题中把下界推到最优值并通常带来 dual attainment；primal feasibility、dual feasibility、residual 与 gap 共同形成可计算证书。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "dual function 是一族全局下界", BLUE)
    out += [line(65, 415, 360, 415, GRID, 2), line(85, 440, 85, 95, GRID, 2)]
    curve = []
    for i in range(121):
        x = 88 + i * 2.2
        z = (x - 225) / 115
        curve.append((x, 350 - 135 * z * z + 12 * z**3))
    out += [polyline(curve, BLUE, 3.5), line(95, 355, 345, 260, TEAL, 2.5, "7 5"), line(95, 385, 345, 325, RED, 2.5, "7 5")]
    out += [text(275, 160, "primal objective", 15, 700, fill=BLUE), text(265, 245, "L(x,lambda_1)", 15, 650, fill=TEAL), text(265, 322, "L(x,lambda_2)", 15, 650, fill=RED)]
    out += [text(45, 455, "g(lambda,nu)=inf_x L(x,lambda,nu)", 16, 650, cls="math"), text(45, 486, "dual feasible => g(lambda,nu) <= p*", 16, 650, cls="math")]

    heading(out, 430, "B", "值相等与解被取得是两件事", TEAL)
    # Weak duality: two distinct optimal values.
    out += [text(430, 108, "weak only", 16, 700, fill=RED), line(565, 140, 750, 140, GRID, 2), circle(590, 140, 7, RED, RED), circle(710, 140, 7, RED, RED), line(600, 140, 700, 140, RED, 3, marker="a2"), text(575, 170, "d*", 15, 650), text(695, 170, "p*", 15, 650)]
    # Strong duality with attained dual optimum.
    out += [text(430, 243, "strong + dual attained", 16, 700, fill=TEAL), line(565, 275, 750, 275, GRID, 2), circle(650, 275, 8, TEAL, TEAL), text(668, 281, "d*=p*", 15, 650)]
    # Same value but the maximizing multiplier is absent.
    out += [text(430, 373, "strong, dual not attained", 16, 700, fill=BLUE), line(565, 405, 750, 405, GRID, 2), circle(650, 405, 8, BLUE, BG, 2.5), text(668, 411, "sup g = p*", 15, 650)]
    out += [text(430, 458, "open point = supremum not attained", 15, 650, fill=MUTED), text(430, 490, "zero gap does not imply attainment。", 15, fill=MUTED)]

    heading(out, 830, "C", "可计算 certificate 要同时可行", RED)
    node(out, 840, 105, 138, 56, "primal x", BLUE)
    node(out, 1000, 105, 145, 56, "dual (lambda,nu)", TEAL, size=15)
    out += [line(910, 164, 910, 205, BLUE, 2.5, marker="a0"), line(1072, 164, 1072, 205, TEAL, 2.5, marker="a1")]
    out += [text(830, 242, "check constraints + multiplier signs", 16, 650), line(830, 268, 1145, 268, GRID, 2)]
    out += [text(830, 318, "gap = f0(x) - g(lambda,nu) >= 0", 16, 700, cls="math"), text(830, 358, "f0(x)-p* <= gap", 17, 700, fill=RED, cls="math")]
    out += [text(830, 410, "convex + relative-interior Slater", 16, 650, fill=TEAL), text(830, 442, "=> strong duality + typical multiplier attainment", 15, 650), text(830, 486, "numerical residuals and scaling still matter。", 15, fill=MUTED)]
    return finish(out, "对偶的核心用途是下界与证书；tightness、attainment 和数值可验证性必须分开陈述。")


def proximal_composite():
    out = begin(
        "近端梯度、软阈值与显式隐式算子",
        "复合目标先对光滑项做显式梯度步，再对结构项做隐式近端步；L1 近端产生精确 dead zone；projection、proximal point 与 forward-backward splitting 是同一 resolvent 语言的不同实例。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "forward 后用 prox 恢复结构", BLUE)
    xk, raw, prox = (90, 330), (305, 160), (265, 285)
    out += [path("M55 390C110 290 190 250 270 260C330 268 355 330 365 390Z", BLUE, 3, "#EFF6FF")]
    out += [circle(*xk, 7, BLUE, BLUE), circle(*raw, 7, RED, RED), circle(*prox, 7, TEAL, TEAL), line(xk[0], xk[1], raw[0], raw[1], RED, 3, "7 5", "a2"), line(raw[0], raw[1], prox[0], prox[1], TEAL, 3, marker="a1")]
    out += [text(65, 355, "x_k", 15, 700, fill=BLUE), text(300, 145, "v=x_k-eta grad f", 15, 650, "middle", fill=RED), text(275, 310, "prox_(eta g)(v)", 15, 700, fill=TEAL)]
    out += [text(45, 435, "x_(k+1)=prox_(eta g)(x_k-eta grad f(x_k))", 15, 650, cls="math"), text(45, 470, "gradient treats smooth f；prox solves structured g exactly。", 15, fill=MUTED), text(45, 499, "indicator prox = projection。", 15, fill=MUTED)]

    heading(out, 430, "B", "L1 prox 的 soft-threshold", TEAL)
    out += [line(445, 300, 765, 300, GRID, 2), line(605, 105, 605, 440, GRID, 2)]
    out += [line(465, 120, 555, 210, BLUE, 3), line(555, 300, 655, 300, RED, 4), line(655, 390, 745, 480, BLUE, 3)]
    out += [line(555, 285, 555, 315, RED, 2), line(655, 285, 655, 315, RED, 2), text(555, 338, "-eta lambda", 15, 650, "middle"), text(655, 338, "+eta lambda", 15, 650, "middle")]
    out += [text(470, 155, "v + eta lambda", 15, 650, fill=BLUE), text(665, 425, "v - eta lambda", 15, 650, fill=BLUE), text(605, 260, "0", 16, 700, "middle", fill=RED), text(430, 486, "exact zeros arise from the nonsmooth kink。", 15, fill=MUTED)]

    heading(out, 830, "C", "显式、隐式与 splitting", RED)
    rows = (("gradient", "x+ = x - eta grad f(x)", BLUE), ("proximal point", "x+ = (I + eta partial g)^-1 x", TEAL), ("forward-backward", "explicit grad f + implicit prox g", RED))
    for i, (label, eq, color) in enumerate(rows):
        yy = 105 + i * 125
        out += [text(830, yy, label, 17, 700, fill=color), line(830, yy + 18, 880, yy + 18, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(895, yy + 24, eq, 15, 650, cls="math")]
    out += [text(830, 450, "prox_(f+g) generally != prox_f o prox_g", 15, 650, fill=RED, cls="math"), text(830, 486, "inexact / nonconvex prox: new error budget。", 15, fill=MUTED)]
    return finish(out, "近端法把不可微结构放进可解子问题；精确零、可行性与收敛证书都来自这个算子，而非事后剪枝。")


def mirror_natural():
    out = begin(
        "镜像下降、熵几何与 Fisher 自然梯度",
        "镜像下降在由 convex potential 定义的 dual coordinates 中做梯度更新；负熵在 simplex 上产生乘法权重；自然梯度从局部 KL trust region 得到 Fisher-preconditioned direction，但近似 Fisher 与 damping 会改变算法。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先到 dual coordinate 再返回", BLUE)
    node(out, 45, 115, 125, 58, "primal x_t", BLUE)
    node(out, 235, 115, 130, 58, "z_t=grad psi(x_t)", TEAL, size=15)
    out += [line(172, 144, 230, 144, INK, 2.5, marker="a3"), text(200, 125, "grad psi", 15, 650, "middle")]
    node(out, 235, 265, 130, 58, "z_t-eta g_t", RED, size=16)
    node(out, 45, 265, 125, 58, "x_(t+1)", BLUE)
    out += [line(300, 176, 300, 258, RED, 3, marker="a2"), line(230, 294, 175, 294, TEAL, 3, marker="a1"), text(202, 280, "grad psi*", 15, 650, "middle")]
    out += [text(45, 390, "argmin_x {eta <g_t,x> + D_psi(x,x_t)}", 15, 650, cls="math"), text(45, 432, "D_psi is directional；usually not a metric。", 15, fill=MUTED), text(45, 478, "Euclidean psi recovers projected gradient。", 15, fill=MUTED)]

    heading(out, 430, "B", "负熵在 simplex 上给乘法更新", TEAL)
    out += [path("M465 385L600 105L745 385Z", BLUE, 3)]
    before = ((535, 290, 10), (600, 255, 14), (665, 320, 8))
    after = ((555, 315, 7), (615, 185, 18), (680, 340, 5))
    for x, y, r in before:
        out.append(circle(x, y, r, GRID, BG, 2))
    for x, y, r in after:
        out.append(circle(x, y, r, TEAL, TEAL, 2))
    out += [text(430, 430, "x_(t+1,i) proportional to x_(t,i) exp(-eta g_i)", 15, 650, cls="math"), text(430, 466, "positivity + normalization are built into geometry。", 15, fill=MUTED), text(430, 497, "rates depend on the chosen norm and potential。", 15, fill=MUTED)]

    heading(out, 830, "C", "KL trust region 产生 Fisher step", RED)
    out += [f'<ellipse cx="990" cy="240" rx="150" ry="78" fill="none" stroke="{TEAL}" stroke-width="2.5"/>', circle(930, 260, 7, BLUE, BLUE), line(930, 260, 1065, 210, RED, 3, marker="a2")]
    out += [text(1070, 205, "-F^-1 grad L", 15, 700, fill=RED), text(835, 345, "min_d <grad L,d>  s.t.  d^T F d <= 2 epsilon", 15, 650, cls="math")]
    out += [text(830, 395, "exact Fisher: model expectation", 15, 650, fill=TEAL), text(830, 427, "empirical Fisher / GGN / K-FAC: different objects", 15, 650, fill=BLUE), text(830, 459, "damping changes metric and invariance", 15, 650, fill=RED), text(830, 492, "singular F needs range/pseudoinverse conditions。", 15, fill=MUTED)]
    return finish(out, "几何选择决定一步的含义：Bregman、KL 与 Euclidean 距离可共享框架，但其对象和不变量不能混用。")


def nonconvex_landscape():
    out = begin(
        "非凸驻点、strict-saddle 动力学与尺度对称性",
        "零梯度点可为极小、strict saddle 或 Hessian 看不出的退化鞍点；strict saddle 有稳定与不稳定方向并可借扰动有限时间逃逸；深网尺度对称性可保持预测函数不变却改变参数 Hessian sharpness。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "小 gradient 之后仍要分类", BLUE)
    # minimum
    out += [path("M50 190Q100 300 150 190", BLUE, 3), circle(100, 245, 5, BLUE, BLUE), text(100, 325, "local min", 15, 700, "middle", fill=BLUE)]
    # strict saddle surface cross sections
    out += [path("M165 245Q215 135 265 245", RED, 3), path("M165 190Q215 300 265 190", TEAL, 3), circle(215, 215, 5, INK, INK), text(215, 325, "strict saddle", 15, 700, "middle", fill=RED)]
    # degenerate
    pts = []
    for i in range(81):
        x = 278 + i
        z = (x - 318) / 32
        pts.append((x, 245 - 18 * z**3))
    out += [polyline(pts, TEAL, 3), circle(318, 245, 5, INK, INK), text(320, 325, "degenerate", 15, 700, "middle", fill=TEAL)]
    out += [text(45, 390, "FOSP: ||grad f|| small", 16, 650), text(45, 425, "SOSP also checks lambda_min(H)", 16, 650), text(45, 470, "PSD Hessian is necessary, not generally sufficient。", 15, fill=MUTED)]

    heading(out, 430, "B", "strict saddle 有稳定与不稳定方向", TEAL)
    out += [line(455, 275, 760, 275, GRID, 2), line(605, 105, 605, 445, GRID, 2)]
    out += [path("M470 390C525 305 555 245 605 275C655 305 690 245 745 160", BLUE, 3), path("M470 160C525 245 555 305 605 275C655 245 690 305 745 390", RED, 3)]
    out += [circle(605, 275, 7, INK, INK), line(605, 275, 710, 350, RED, 3, marker="a2"), line(605, 275, 535, 225, BLUE, 2.5, "7 5")]
    out += [text(705, 375, "unstable escape", 15, 700, fill=RED), text(455, 205, "stable manifold", 15, 700, fill=BLUE), text(430, 430, "almost-sure avoidance != finite-time escape", 15, 650), text(430, 468, "finite-time proof needs Hessian-Lipschitz bounds。", 15, fill=MUTED)]

    heading(out, 830, "C", "尺度对称改变 raw sharpness", RED)
    out += [line(845, 420, 1155, 420, GRID, 2), line(900, 445, 900, 95, GRID, 2)]
    curve = []
    for i in range(1, 121):
        x = 880 + i * 2.1
        a = (x - 840) / 85
        y = 390 - 150 / max(a, 0.35)
        curve.append((x, max(110, y)))
    out += [polyline(curve, BLUE, 3.5), circle(930, 240, 7, TEAL, TEAL), circle(1085, 350, 7, RED, RED)]
    out += [text(925, 220, "(ca,b/c)", 15, 700, fill=TEAL), text(1075, 375, "(a,b)", 15, 700, fill=RED), text(835, 455, "two-layer scale symmetry: ab = constant", 15, 650, cls="math")]
    out += [text(830, 487, "same predictor；raw Hessian spectrum changes。", 15, fill=MUTED)]
    return finish(out, "非凸结论必须沿 stationary classification、escape dynamics 与 model-specific landscape 逐级增加假设。")


FIGURES = {
    "fig-duality-slater-certificate-v2.svg": duality_certificate,
    "fig-proximal-composite-sparsity-v2.svg": proximal_composite,
    "fig-mirror-natural-geometry-v2.svg": mirror_natural,
    "fig-nonconvex-saddles-landscape-v2.svg": nonconvex_landscape,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
