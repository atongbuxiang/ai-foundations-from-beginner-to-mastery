#!/usr/bin/env python3
"""Generate v2 figures for OPT-01--04 convex-analysis foundations."""

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


def polyline(points, color, width=2.5, dash=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, color, width, "none", dash)


def optimization_contract():
    out = begin(
        "优化问题契约、解的存在状态与三层误差",
        "一个优化问题必须同时声明变量、domain、目标、约束和解概念；infimum、minimum 与 unbounded 不同；optimization、statistical 与 deployment error 也不能互换。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先写完整 problem contract", BLUE)
    items = (("decision x", BLUE), ("domain dom f", TEAL), ("objective f0", RED), ("constraints", BLUE), ("solution concept", TEAL))
    for i, (label, color) in enumerate(items):
        y = 95 + i * 78
        node(out, 55, y, 285, 50, label, color, size=16)
        if i < len(items) - 1:
            out.append(line(198, y + 52, 198, y + 72, INK, 2, marker="a3"))
    out += [text(45, 492, "data / hyperparameters / randomness 也属于 instance。", 15, fill=MUTED)]

    heading(out, 430, "B", "最优值状态不能只看曲线下降", TEAL)
    out += [line(440, 400, 770, 400, GRID, 2)]
    # attained minimum
    pts = []
    for i in range(61):
        x = 445 + 1.7 * i
        y = 190 + 0.035 * (x - 495) ** 2
        pts.append((x, min(y, 390)))
    out.append(polyline(pts, BLUE, 3))
    out.append(circle(495, 190, 6, BLUE, BLUE))
    # unattained infimum
    pts = []
    for i in range(61):
        x = 555 + 1.65 * i
        y = 335 - 130 * math.exp(-0.04 * (x - 555))
        pts.append((x, y))
    out.append(polyline(pts, TEAL, 3))
    out.append(line(555, 335, 655, 335, TEAL, 1.5, "5 4"))
    # unbounded
    out += [line(675, 175, 755, 365, RED, 3, marker="a2")]
    out += [
        text(495, 435, "minimum attained", 15, 700, "middle", BLUE),
        text(610, 470, "infimum not attained", 15, 700, "middle", TEAL),
        text(720, 435, "unbounded", 15, 700, "middle", RED),
        text(430, 115, "existence = finite value + attainment", 16, 650),
    ]

    heading(out, 830, "C", "算法成功不等于模型成功", RED)
    layers = (
        ("optimization", "objective / residual", BLUE),
        ("statistics", "generalization gap", TEAL),
        ("deployment", "utility / shift", RED),
    )
    for i, (label, desc, color) in enumerate(layers):
        y = 105 + i * 120
        node(out, 840, y, 130, 54, label, color, size=16)
        out += [line(973, y + 27, 1008, y + 27, INK, 2.2, marker="a3"), text(1018, y + 33, desc, 15, 650)]
    out += [
        text(830, 455, "objective gap != solution distance", 15, 650),
        text(830, 488, "换算需要 convexity / error bound 等结构。", 15, fill=MUTED),
    ]
    return finish(out, "先定义问题和证书，再解释算法输出；下降曲线不能替代存在性、统计性与部署证据。")


def convex_sets():
    out = begin(
        "凸集线段判据、投影分离与三类锥几何",
        "凸集包含任意两点间整条线段；闭凸集最近点给出分离超平面；simplex、second-order cone 与 PSD cone 是不同结构的凸集合。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "线段是否始终留在集合内", BLUE)
    out += [path("M55 120C105 82 180 105 190 170C200 245 115 275 60 230C30 205 30 150 55 120Z", BLUE, 3)]
    out += [circle(75, 205, 6, BLUE, BLUE), circle(165, 135, 6, BLUE, BLUE), line(80, 201, 160, 139, TEAL, 3)]
    out += [text(110, 295, "convex", 16, 700, "middle", BLUE)]
    out += [path("M230 130C255 95 305 100 315 140C325 180 290 205 260 190C235 178 215 160 230 130Z", RED, 3), path("M250 250C275 210 330 215 345 255C360 295 315 325 280 310C248 296 230 275 250 250Z", RED, 3)]
    out += [circle(270, 155, 6, RED, RED), circle(300, 275, 6, RED, RED), line(274, 160, 296, 270, RED, 3, "7 5")]
    out += [text(290, 350, "nonconvex: segment leaves set", 15, 700, "middle", RED), text(45, 455, "convex combinations preserve feasibility。", 16, 650), text(45, 490, "rank constraint / union 通常破坏凸性。", 15, fill=MUTED)]

    heading(out, 430, "B", "最近点产生分离超平面", TEAL)
    out += [path("M455 145C505 105 600 110 640 165C685 230 615 320 525 300C450 283 420 200 455 145Z", BLUE, 3)]
    p = (720, 170)
    proj = (635, 175)
    out += [circle(*p, 7, RED, RED), circle(*proj, 7, TEAL, TEAL), line(proj[0], proj[1], p[0], p[1], RED, 3)]
    out += [line(655, 85, 665, 330, TEAL, 3), text(720, 155, "y", 16, 700, "middle", RED), text(623, 165, "Pi_C(y)", 15, 700, "end", TEAL)]
    out += [
        text(430, 375, "normal = y - Pi_C(y)", 16, 650, cls="math"),
        text(430, 415, "<y-p, x-p> <= 0 for all x in C", 15, 650, cls="math"),
        text(430, 465, "closed + convex 给 existence 与 uniqueness。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "Simplex、SOC 与 PSD cone", RED)
    out += [path("M845 225L915 105L985 225Z", BLUE, 3), text(915, 255, "simplex", 15, 700, "middle", BLUE)]
    out += [path("M1000 225L1050 105L1100 225Z", TEAL, 3), path("M1000 225C1020 245 1080 245 1100 225", TEAL, 3), text(1050, 270, "SOC", 15, 700, "middle", TEAL)]
    out += [path("M865 345L975 345L945 465L895 465Z", RED, 3), text(920, 410, "X >= 0", 17, 700, "middle", RED), text(1060, 375, "PSD cone", 16, 700, "middle", RED)]
    out += [
        text(830, 495, "三者都凸，但 projection / barrier / dual cone 不同。", 15, fill=MUTED),
    ]
    return finish(out, "凸性是一条线段闭包性质；投影和分离把它转成证书，不同凸锥仍需不同计算结构。")


def convex_functions():
    out = begin(
        "凸函数的 chord、Jensen gap 与 logsumexp 曲率",
        "凸函数图像在 chord 下、在所有切线之上且 epigraph 为凸集；Jensen 比较先平均与先过函数；logsumexp 的 gradient 与 Hessian 分别是 softmax 与 covariance。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Chord 在上，切线在下", BLUE)
    out += [line(50, 390, 360, 390, GRID, 2), line(70, 415, 70, 95, GRID, 2)]
    curve = []
    for i in range(121):
        x = 70 + 2.25 * i
        y = 350 - 0.006 * (x - 205) ** 2
        curve.append((x, y))
    out.append(polyline(curve, BLUE, 3))
    x1, x2 = 115, 300
    y1 = 350 - 0.006 * (x1 - 205) ** 2
    y2 = 350 - 0.006 * (x2 - 205) ** 2
    out += [line(x1, y1, x2, y2, RED, 3), circle(x1, y1, 5, RED, RED), circle(x2, y2, 5, RED, RED)]
    tx = 175
    ty = 350 - 0.006 * (tx - 205) ** 2
    slope = -0.012 * (tx - 205)
    out += [line(90, ty + slope * (90 - tx), 320, ty + slope * (320 - tx), TEAL, 2.5, "7 5"), text(255, 125, "chord", 15, 700, fill=RED), text(95, 300, "supporting tangent", 15, 700, fill=TEAL)]
    out += [text(45, 455, "f(theta x+(1-theta)y) <= theta f(x)+(1-theta)f(y)", 15, 650, cls="math"), text(45, 490, "epi f convex；domain 也必须凸。", 15, fill=MUTED)]

    heading(out, 430, "B", "Jensen 比较两条平均路径", TEAL)
    node(out, 445, 105, 100, 50, "x_i", BLUE, size=17)
    node(out, 650, 105, 105, 50, "f(x_i)", RED, size=17)
    node(out, 445, 280, 135, 52, "E[X]", TEAL, size=17)
    node(out, 635, 280, 120, 52, "f(E[X])", TEAL, size=16)
    out += [line(548, 130, 645, 130, INK, 2.4, marker="a3"), line(495, 158, 510, 273, BLUE, 2.4, marker="a0"), line(583, 306, 630, 306, INK, 2.4, marker="a3")]
    out += [line(702, 158, 702, 273, RED, 2.4, marker="a2"), text(710, 220, "E", 15, 700, fill=RED)]
    out += [
        text(430, 385, "f(E[X]) <= E[f(X)]", 19, 700, cls="math"),
        text(430, 430, "gap depends on spread + curvature", 16, 650),
        text(430, 475, "等号需检查 affine region / a.s. constancy。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "LogSumExp 的 AI 曲率接口", RED)
    node(out, 840, 105, 300, 58, "LSE(z)=log sum_i exp(z_i)", BLUE, size=16)
    out += [line(990, 166, 990, 205, INK, 2.4, marker="a3")]
    node(out, 840, 218, 300, 58, "gradient = softmax(z)", TEAL, size=17)
    out += [line(990, 279, 990, 318, INK, 2.4, marker="a3")]
    node(out, 840, 330, 300, 66, "Hessian = Diag(p)-p p^T >= 0", RED, size=15)
    out += [
        text(830, 442, "Hessian 是 categorical covariance。", 16, 650),
        text(830, 480, "对 logits 凸，不代表对 deep weights 凸。", 15, fill=MUTED),
    ]
    return finish(out, "Chord、epigraph、一阶支撑、Hessian 与 Jensen 是同一凸性的不同接口；变量与 domain 不能省略。")


def subgradient_fenchel():
    out = begin(
        "次梯度、凸共轭与 Fenchel–Young 证书",
        "不可微凸点有一族全局支撑斜率；共轭为每个 dual slope 选择最佳截距；Fenchel–Young gap 非负并在 primal-dual 次梯度匹配时为零。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Kink 处是一束合法支撑线", BLUE)
    out += [line(55, 385, 355, 385, GRID, 2), line(205, 410, 205, 95, GRID, 2)]
    out += [path("M70 150L205 350L340 150", BLUE, 3)]
    for slope, color in ((-0.75, RED), (0.0, TEAL), (0.7, RED)):
        out.append(line(85, 350 + slope * (85 - 205), 325, 350 + slope * (325 - 205), color, 2, "7 5"))
    out += [circle(205, 350, 6, BLUE, BLUE), text(205, 82, "f(x)=|x|", 17, 700, "middle")]
    out += [
        text(45, 435, "partial |x|(0) = [-1,1]", 18, 700, cls="math"),
        text(45, 475, "每条线都是全局 affine lower bound。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "共轭选择每个 slope 的最佳截距", TEAL)
    out += [line(440, 385, 770, 385, GRID, 2), line(470, 410, 470, 95, GRID, 2)]
    curve = []
    for i in range(121):
        x = 470 + 2.35 * i
        y = 350 - 0.005 * (x - 600) ** 2
        curve.append((x, y))
    out.append(polyline(curve, TEAL, 3))
    for offset, color in ((40, GRID), (5, BLUE), (-30, GRID)):
        out.append(line(480, 355 + offset, 750, 160 + offset, color, 2, "6 4"))
    out += [circle(615, 260, 6, BLUE, BLUE), text(430, 430, "f*(y)=sup_x { y^T x - f(x) }", 17, 650, cls="math"), text(430, 472, "固定 slope y，向上移动直线直到接触。", 15, fill=MUTED)]

    heading(out, 830, "C", "Fenchel–Young：gap 即证书", RED)
    node(out, 840, 105, 130, 54, "primal x", BLUE, size=17)
    node(out, 1010, 105, 130, 54, "dual y", TEAL, size=17)
    out += [line(973, 132, 1005, 132, INK, 2.3, marker="a3")]
    out += [
        text(830, 225, "gap = f(x)+f*(y)-<x,y> >= 0", 17, 700, cls="math"),
        line(840, 260, 1135, 260, GRID, 2),
        text(830, 315, "gap=0", 18, 700, fill=RED),
        text(930, 315, "iff y in partial f(x)", 17, 650, cls="math"),
        text(930, 355, "iff x in partial f*(y)", 17, 650, cls="math"),
        text(830, 420, "0 in partial f(x*)  <=>  global optimum", 16, 650, cls="math"),
        text(830, 468, "写出 dual 不自动给 zero gap 或 attainment。", 15, fill=MUTED),
    ]
    return finish(out, "次梯度给全局支撑，共轭交换变量与斜率，Fenchel–Young 等号把二者闭合为证书。")


FIGURES = {
    "fig-optimization-problem-solution-concepts-v2.svg": optimization_contract,
    "fig-convex-sets-separation-v2.svg": convex_sets,
    "fig-convex-functions-jensen-epigraph-v2.svg": convex_functions,
    "fig-subgradient-conjugate-fenchel-v2.svg": subgradient_fenchel,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
