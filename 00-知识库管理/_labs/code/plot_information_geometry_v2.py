#!/usr/bin/env python3
"""Generate v2 textbook figures for DPI, MaxEnt, and divergence geometry."""

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
    text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "information-theory"


def polyline(points, color, width=2.5, dash=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, color, width, "none", dash)


def dpi_sufficiency():
    out = begin(
        "数据处理不等式、信息损失与充分性",
        "Markov 条件禁止后处理额外访问原变量；MI chain rule 给出精确损失与等号条件；统计充分性和任务充分性都要求给定表示后目标与原数据条件独立。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "后处理不能凭空增加信息", BLUE)
    node(out, 55, 125, 75, 52, "X", BLUE)
    node(out, 170, 125, 75, 52, "Y", TEAL)
    node(out, 285, 125, 75, 52, "Z", RED)
    out += [line(133, 151, 165, 151, INK, 2.5, marker="a3"), line(248, 151, 280, 151, INK, 2.5, marker="a3")]
    out += [
        path("M92 205C155 260 270 260 322 205", RED, 2.5, "none", "7 5"),
        line(196, 232, 216, 252, RED, 3),
        line(216, 232, 196, 252, RED, 3),
        text(205, 282, "无 skip / shared side information", 15, 650, "middle", RED),
        text(45, 345, "X -> Y -> Z  iff  X independent Z | Y", 16, 650, cls="math"),
        text(45, 392, "I(X;Z) <= I(X;Y)", 19, 700, cls="math"),
        text(45, 440, "deterministic 与 randomized channel 都适用。", 15, fill=MUTED),
        text(45, 478, "箭头是 factorization，不是自动因果声明。", 15, fill=RED),
    ]

    heading(out, 430, "B", "Chain rule 给出精确损失", TEAL)
    node(out, 445, 100, 310, 52, "I(X;Y,Z)", BLUE, size=18)
    out += [line(600, 155, 600, 190, INK, 2.4, marker="a3")]
    node(out, 445, 202, 310, 64, "I(X;Y) + I(X;Z|Y)", TEAL, size=16)
    out += [text(600, 294, "Markov: second term = 0", 15, 650, "middle", TEAL)]
    out += [line(600, 310, 600, 338, INK, 2.4, marker="a3")]
    node(out, 445, 348, 310, 64, "I(X;Z) + I(X;Y|Z)", RED, size=16)
    out += [
        text(430, 455, "I(X;Y)-I(X;Z) = I(X;Y|Z)", 16, 700, cls="math"),
        text(430, 492, "等号 iff Z 丢失的条件信息为 0。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "充分性必须声明保留谁的信息", RED)
    node(out, 840, 100, 65, 48, "theta", BLUE, size=15)
    node(out, 955, 100, 65, 48, "X", TEAL, size=15)
    node(out, 1070, 100, 80, 48, "T(X)", RED, size=15)
    out += [line(908, 124, 950, 124, INK, 2.3, marker="a3"), line(1023, 124, 1065, 124, INK, 2.3, marker="a3")]
    out += [
        text(830, 195, "parameter sufficiency", 16, 700, fill=BLUE),
        text(830, 230, "theta independent X | T(X)", 16, 650, cls="math"),
        text(830, 272, "p_theta(x)=g_theta(T(x)) h(x)", 16, 650, cls="math"),
        line(840, 305, 1135, 305, GRID, 2),
        text(830, 350, "task sufficiency", 16, 700, fill=TEAL),
        text(830, 387, "Y_task independent X | Z", 16, 650, cls="math"),
        text(830, 430, "保留 task 信息 != 最大化 I(X;Z)。", 16, 650),
        text(830, 472, "minimal / complete / efficient 是不同性质。", 15, fill=MUTED),
    ]
    return finish(out, "DPI 的前提是条件独立；等号、参数充分性与任务充分性都必须相对明确目标陈述。")


def maxent_duality():
    out = begin(
        "最大熵约束、指数族与凸对偶",
        "MaxEnt 在指定 support、reference measure 与 moment constraints 的可行集上优化；Lagrange 条件产生指数族；log-partition 的梯度与 Hessian 给出 moment matching 和 covariance curvature。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先在可行集里最大化 entropy", BLUE)
    out += [path("M70 390L205 100L345 390Z", BLUE, 3)]
    out += [line(105, 330, 300, 185, RED, 3), text(238, 185, "E_p[T]=tau", 15, 700, fill=RED)]
    out += [path("M125 345C165 260 245 220 300 205", TEAL, 2, "none", "7 5"), path("M145 360C185 300 240 270 280 250", TEAL, 2, "none", "7 5")]
    out += [circle(235, 234, 7, TEAL, TEAL), text(245, 224, "p*", 16, 700, fill=TEAL)]
    out += [
        text(45, 430, "maximize H(p)", 17, 700, cls="math"),
        text(45, 465, "s.t. p>=0, sum p=1, E_p[T]=tau", 15, 650, cls="math"),
        text(45, 500, "support / base measure 改变，可行集与答案也变。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "Lagrange 条件产生指数族", TEAL)
    node(out, 445, 102, 310, 58, "entropy + normalization + moments", BLUE, size=15)
    out += [line(600, 164, 600, 202, INK, 2.4, marker="a3")]
    node(out, 445, 214, 310, 68, "log p(x) = log h(x) + eta^T T(x) - A(eta)", TEAL, size=15)
    out += [line(600, 286, 600, 324, INK, 2.4, marker="a3")]
    node(out, 445, 336, 310, 58, "p_eta(x)=h(x) exp[eta^T T(x)-A]", RED, size=15)
    out += [
        text(430, 438, "A(eta)=log integral h exp(eta^T T)", 16, 650, cls="math"),
        text(430, 478, "A 不是装饰常数：它负责归一化。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "Dual 梯度 = moment mismatch", RED)
    out += [
        text(830, 118, "dual: A(eta) - eta^T tau", 17, 700, cls="math"),
        line(840, 150, 1135, 150, GRID, 2),
        text(830, 200, "gradient A(eta) = E_eta[T]", 17, 650, cls="math"),
        text(830, 242, "gradient dual = E_eta[T] - tau", 17, 650, cls="math"),
        text(830, 284, "Hessian A(eta) = Cov_eta[T]", 17, 650, cls="math"),
        line(840, 320, 1135, 320, GRID, 2),
    ]
    node(out, 845, 345, 125, 52, "empirical tau", BLUE, size=15)
    node(out, 1030, 345, 110, 52, "model moment", TEAL, size=15)
    out += [line(973, 371, 1025, 371, INK, 2.3, marker="a3")]
    out += [
        text(830, 435, "moment matching 连接 MaxEnt dual 与 MLE。", 15, 650),
        text(830, 475, "边界 tau 可能令 eta 发散或 optimizer 不存在。", 15, fill=RED),
    ]
    return finish(out, "MaxEnt、指数族与 moment matching 是同一凸对偶结构，但前提是可行性、存在性与参数最小性。")


def divergence_geometry():
    out = begin(
        "散度家族的 density ratio、凸几何与样本空间几何",
        "f-divergence 依赖 density ratio；Bregman divergence 是 convex tangent gap 并依赖坐标；IPM 与 optimal transport 通过 test functions 或 ground cost 感知样本空间。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "f-divergence：看 density ratio", BLUE)
    node(out, 55, 105, 110, 52, "P", BLUE, size=18)
    node(out, 240, 105, 110, 52, "Q", TEAL, size=18)
    out += [line(168, 131, 235, 131, INK, 2.5, marker="a3"), text(201, 112, "dP/dQ", 15, 650, "middle")]
    out += [
        text(45, 220, "D_f(P||Q)=E_Q f(dP/dQ)", 17, 650, cls="math"),
        text(45, 265, "结构：共同测度 / Radon-Nikodym ratio", 15, 650),
        text(45, 315, "优点：Markov data processing", 16, 650, fill=BLUE),
        text(45, 360, "代价：常忽略样本空间 ground geometry", 15, fill=MUTED),
        text(45, 410, "support singularity 可令 KL 无穷。", 16, fill=RED),
        text(45, 458, "TV 也同时属于 IPM；家族不是互斥标签。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "Bregman：凸函数切线缺口", TEAL)
    out += [line(445, 375, 770, 375, GRID, 2), line(470, 405, 470, 95, GRID, 2)]
    curve = []
    for i in range(121):
        x = 470 + 2.3 * i
        u = (x - 585) / 85
        y = 345 - 62 * u * u
        curve.append((x, y))
    out.append(polyline(curve, TEAL, 3))
    qx = 550
    qy = 345 - 62 * ((qx - 585) / 85) ** 2
    px = 690
    py = 345 - 62 * ((px - 585) / 85) ** 2
    slope = -124 * ((qx - 585) / 85) / 85
    tangent_y_at_p = qy + slope * (px - qx)
    out += [line(500, qy + slope * (500 - qx), 735, qy + slope * (735 - qx), BLUE, 2.5, "7 5")]
    out += [circle(qx, qy, 6, BLUE, BLUE), circle(px, py, 6, RED, RED), line(px, py, px, tangent_y_at_p, RED, 3)]
    out += [
        text(qx, qy - 16, "q", 15, 700, "middle", BLUE),
        text(px, py - 16, "p", 15, 700, "middle", RED),
        text(704, (py + tangent_y_at_p) / 2, "gap", 15, 700, fill=RED),
        text(430, 420, "D_phi(p,q)=phi(p)-phi(q)", 15, 650, cls="math"),
        text(430, 452, "             - <grad phi(q),p-q>", 15, 650, cls="math"),
        text(430, 490, "一般不对称；依赖所选坐标与 potential。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "IPM / OT：函数类与 ground cost", RED)
    ppts = ((850, 150), (885, 210), (920, 170))
    qpts = ((1045, 135), (1090, 205), (1125, 160))
    for x, y in ppts:
        out.append(circle(x, y, 7, BLUE, BLUE))
    for x, y in qpts:
        out.append(circle(x, y, 7, RED, RED))
    for (x1, y1), (x2, y2) in zip(ppts, qpts):
        out.append(line(x1 + 8, y1, x2 - 8, y2, TEAL, 2, "7 5"))
    out += [
        text(875, 112, "P samples", 15, 700, "middle", BLUE),
        text(1090, 112, "Q samples", 15, 700, "middle", RED),
        text(830, 285, "IPM = sup_g |E_P g - E_Q g|", 16, 650, cls="math"),
        text(830, 328, "OT = inf_coupling E[c(X,Y)]", 16, 650, cls="math"),
        text(830, 375, "Wasserstein: ground metric；MMD: RKHS kernel", 15, 650),
        text(830, 420, "metric 还需 symmetry + triangle inequality。", 15, fill=RED),
        text(830, 465, "population quantity != sample estimator != train loss", 15, fill=MUTED),
    ]
    return finish(out, "选择差异量时先问它依赖哪种结构，再审计拓扑、支持、可估性与训练 surrogate。")


FIGURES = {
    "fig-data-processing-sufficiency-v2.svg": dpi_sufficiency,
    "fig-maxent-exponential-duality-v2.svg": maxent_duality,
    "fig-divergence-metric-topology-v2.svg": divergence_geometry,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
