#!/usr/bin/env python3
"""Generate v2 textbook figures for OPT-05--08 first-order optimization."""

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


def smooth_strong_condition():
    out = begin(
        "光滑性、强凸性与条件数的曲率夹逼",
        "L 光滑性给切平面的二次上模型，mu 强凸性给二次下模型；在二次型上二者成为 Hessian 谱端点，条件数刻画各向异性的时间尺度；点、区域和全局曲率声明具有不同量词。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一点的二次上、下模型", BLUE)
    out += [line(52, 410, 365, 410, GRID, 2), line(82, 435, 82, 95, GRID, 2)]
    x0 = 205
    actual = []
    upper = []
    lower = []
    for i in range(121):
        x = 78 + i * 2.25
        dx = (x - x0) / 105
        actual.append((x, 335 - 92 * dx - 70 * dx * dx))
        upper.append((x, 335 - 92 * dx - 85 * dx * dx))
        lower.append((x, 335 - 92 * dx - 45 * dx * dx))
    out += [polyline(upper, RED, 2.4, "7 5"), polyline(actual, BLUE, 3.5), polyline(lower, TEAL, 2.4, "7 5")]
    out += [circle(x0, 335, 6, BLUE, BLUE), text(292, 128, "L upper model", 15, 700, fill=RED), text(274, 330, "f", 17, 700, fill=BLUE), text(280, 382, "mu lower model", 15, 700, fill=TEAL)]
    out += [text(45, 462, "same value + same gradient at x", 16, 650), text(45, 496, "lower <= f(y) <= upper", 16, fill=MUTED, cls="math")]

    heading(out, 430, "B", "谱端点决定各向异性", TEAL)
    out += [line(445, 405, 765, 405, GRID, 2), line(605, 92, 605, 440, GRID, 2)]
    for rx, ry in ((145, 92), (106, 65), (66, 39)):
        out.append(f'<ellipse cx="605" cy="260" rx="{rx}" ry="{ry}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    out += [circle(605, 260, 6, TEAL, TEAL), line(605, 260, 740, 260, RED, 3, marker="a2"), line(605, 260, 605, 170, TEAL, 3, marker="a1")]
    out += [text(625, 292, "lambda=mu (slow)", 15, 650, fill=RED), text(615, 160, "lambda=L (fast)", 15, 650, fill=TEAL)]
    out += [text(435, 446, "mu I <= Hessian <= L I", 17, 650, cls="math"), text(435, 482, "kappa=L/mu；坐标或 metric 改变它。", 16, fill=MUTED)]

    heading(out, 830, "C", "曲率结论的量词逐层增强", RED)
    out += [circle(980, 185, 35, RED, "#FFF7F5", 2.5), circle(980, 245, 105, TEAL, "none", 2.5), circle(980, 300, 170, BLUE, "none", 2.5)]
    out += [text(980, 190, "point", 16, 700, "middle", RED), text(1095, 215, "region", 16, 700, fill=TEAL), text(1095, 345, "global", 16, 700, fill=BLUE)]
    out += [text(825, 400, "H(x0) snapshot", 15, 650, fill=RED), text(825, 432, "all x on trajectory / sublevel set", 15, 650, fill=TEAL), text(825, 464, "all x in declared domain", 15, 650, fill=BLUE), text(825, 497, "还必须固定 norm 与 parameterization。", 15, fill=MUTED)]
    return finish(out, "L 与 mu 是带 domain、norm 和量词的曲率证书；kappa 只在这些对象固定后才有算法含义。")


def gradient_descent_rates():
    out = begin(
        "梯度下降的有限步证书、病态轨迹与收敛终点",
        "负梯度只给无穷小方向，descent lemma 给有限步下降；病态二次型中统一步长产生之字轨迹；非凸、凸和强凸假设导向不同的误差对象与速率。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "L 把下降方向升级为有限步", BLUE)
    out += [line(50, 405, 370, 405, GRID, 2), line(78, 430, 78, 95, GRID, 2)]
    xk, yk = 142, 205
    curve = []
    model = []
    for i in range(121):
        x = 80 + i * 2.35
        dx = (x - 225) / 120
        curve.append((x, 350 - 165 * dx * dx + 22 * dx**3))
        d0 = (x - xk) / 120
        model.append((x, yk + 150 * d0 - 120 * d0 * d0))
    out += [polyline(curve, BLUE, 3.5), polyline(model, RED, 2.4, "7 5")]
    xnext = 232
    ynext = 350 - 165 * ((xnext - 225) / 120) ** 2 + 22 * ((xnext - 225) / 120) ** 3
    out += [circle(xk, yk, 6, RED, RED), circle(xnext, ynext, 6, TEAL, TEAL), line(xk, 420, xnext, 420, TEAL, 3, marker="a1")]
    out += [text(xk, 187, "x_k", 16, 700, "middle", RED), text(xnext, ynext + 28, "x_k - eta grad f", 15, 650, "middle", TEAL), text(275, 145, "quadratic upper model", 15, 650, fill=RED)]
    out += [text(45, 468, "Delta f <= -eta(1-L eta/2)||grad f||^2", 15, 650, cls="math"), text(45, 499, "0 < eta < 2/L gives descent；eta=1/L 便于证明。", 15, fill=MUTED)]

    heading(out, 430, "B", "病态二次型产生 zig-zag", TEAL)
    for rx, ry in ((145, 92), (107, 66), (70, 41), (36, 20)):
        out.append(f'<ellipse cx="605" cy="270" rx="{rx}" ry="{ry}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    pts = [(470, 172), (500, 366), (528, 190), (552, 342), (570, 212), (586, 318), (596, 239), (605, 286), (605, 270)]
    out += [polyline(pts, RED, 3), circle(470, 172, 6, RED, RED), circle(605, 270, 6, TEAL, TEAL)]
    out += [text(460, 152, "x_0", 15, 700, fill=RED), text(615, 265, "x*", 15, 700, fill=TEAL), text(430, 405, "stable step controlled by L", 16, 650), text(430, 438, "progress along slow axis controlled by mu", 16, 650), text(430, 477, "eta*=2/(L+mu), rho*=(kappa-1)/(kappa+1)", 15, fill=MUTED, cls="math")]

    heading(out, 830, "C", "假设改变，终点也改变", RED)
    yrows = (122, 245, 368)
    labels = (("smooth + lower bounded", "min ||grad f||^2 = O(1/T)", RED), ("+ convex", "function gap = O(1/T)", BLUE), ("+ mu-strongly convex", "gap shrinks geometrically", TEAL))
    for i, (assumption, result, color) in enumerate(labels):
        y = yrows[i]
        out += [circle(850, y, 7, color, color), line(860, y, 895, y, color, 2.5), text(905, y - 8, assumption, 16, 700, fill=color), text(905, y + 25, result, 16, 650)]
        if i < 2:
            out.append(line(850, y + 14, 850, yrows[i + 1] - 14, GRID, 2, "5 5"))
    out += [text(825, 468, "stationarity != global optimum != generalization", 15, 650, fill=MUTED)]
    return finish(out, "先用 L 证明有限步安全，再按函数类读取相应误差对象；收敛率不能跨假设改写。")


def acceleration_momentum():
    out = begin(
        "动量、特征根与一阶 oracle 加速",
        "Heavy-ball 在当前位置求梯度，Nesterov 在外推点求梯度；二次型的每个特征模态服从二阶递推并由单位圆内的根控制；一般光滑凸函数上的加速率必须与同一 oracle 类的下界配对。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "HB 与 NAG 的梯度位置不同", BLUE)
    for rx, ry in ((145, 92), (100, 62), (55, 32)):
        out.append(f'<ellipse cx="205" cy="270" rx="{rx}" ry="{ry}" fill="none" stroke="{GRID}" stroke-width="2"/>')
    prev, cur, look, hb, nag = (92, 168), (145, 350), (205, 405), (220, 280), (240, 270)
    out += [circle(*prev, 6, INK, INK), circle(*cur, 7, BLUE, BLUE), circle(205, 270, 6, TEAL, TEAL)]
    out += [line(prev[0], prev[1], cur[0], cur[1], INK, 2.5, marker="a3"), line(cur[0], cur[1], look[0], look[1], RED, 2.5, "7 5", "a2"), line(cur[0], cur[1], hb[0], hb[1], BLUE, 3, marker="a0"), line(look[0], look[1], nag[0], nag[1], RED, 3, marker="a2")]
    out += [text(78, 150, "x_(k-1)", 15, 650), text(120, 375, "x_k", 16, 700, fill=BLUE), text(212, 430, "look-ahead y_k", 15, 650, fill=RED), text(235, 248, "x*", 15, 700, fill=TEAL)]
    out += [text(45, 468, "HB: grad f(x_k)", 16, 650, fill=BLUE), text(220, 468, "NAG: grad f(y_k)", 16, 650, fill=RED), text(45, 499, "名称相近，不代表递推或定理相同。", 15, fill=MUTED)]

    heading(out, 430, "B", "每个特征值对应两个根", TEAL)
    out += [text(430, 110, "z_(k+1)=(1+beta-eta lambda)z_k-beta z_(k-1)", 15, 650, cls="math")]
    cx, cy, radius = 600, 300, 112
    out += [line(452, cy, 760, cy, GRID, 2), line(cx, 170, cx, 430, GRID, 2), circle(cx, cy, radius, TEAL, "none", 2.5)]
    stable = ((642, 255), (558, 345))
    for p in stable:
        out.append(circle(*p, 7, BLUE, BLUE))
    out += [circle(735, 260, 7, RED, RED), text(665, 225, "|r|<1", 16, 700, fill=BLUE), text(710, 242, "unstable", 15, 700, fill=RED)]
    out += [text(430, 455, "r^2-(1+beta-eta lambda)r+beta=0", 15, 650, cls="math"), text(430, 488, "所有 lambda in [mu,L] 的根都须在单位圆内。", 15, fill=MUTED)]

    heading(out, 830, "C", "函数类上的最坏情形阶", RED)
    out += [line(850, 420, 1150, 420, GRID, 2), line(870, 438, 870, 100, GRID, 2), text(1145, 448, "iterations k", 15, 650, "end"), text(835, 110, "gap", 15, 650)]
    gd, nag, lower = [], [], []
    for i in range(1, 91):
        x = 875 + i * 2.9
        gd.append((x, 120 + 47 * math.log1p(i)))
        nag.append((x, 120 + 61 * math.log1p(i)))
        lower.append((x, 126 + 58 * math.log1p(i)))
    out += [polyline(gd, RED, 3), polyline(nag, BLUE, 3.5), polyline(lower, TEAL, 2, "7 5")]
    out += [text(1020, 245, "GD  O(1/k)", 15, 700, fill=RED), text(1010, 350, "NAG  O(1/k^2)", 15, 700, fill=BLUE), text(925, 400, "lower bound: same order", 15, 650, fill=TEAL)]
    out += [text(825, 488, "必须固定函数类、oracle、维度与误差准则。", 15, fill=MUTED)]
    return finish(out, "加速是受函数类与信息模型约束的复杂度结论；动量轨迹、谱半径和 wall-clock 是不同证据。")


def sgd_minibatch_noise():
    out = begin(
        "随机梯度、批量方差与固定步长噪声平台",
        "随机梯度在给定历史后应围绕目标梯度取条件均值；独立小批量的方差按一除以 B 缩减，相关与无放回抽样改变规律；固定步长在强凸局部通常先快速收敛再停在噪声平台。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "条件均值才是 oracle 支点", BLUE)
    origin = (115, 360)
    samples = ((238, 145), (305, 205), (325, 285), (270, 365), (205, 315), (285, 125), (345, 235))
    for i, p in enumerate(samples):
        out.append(line(origin[0], origin[1], p[0], p[1], RED, 1.8, "5 4", "a2" if i in (0, 3, 6) else None))
    mean = (286, 235)
    out += [circle(*origin, 6, INK, INK), line(origin[0], origin[1], mean[0], mean[1], TEAL, 4, marker="a1"), circle(*mean, 6, TEAL, TEAL)]
    out += [text(238, 216, "E[g_k | F_k]", 16, 700, fill=TEAL), text(47, 430, "g_k = grad F(theta_k) + xi_k", 16, 650, cls="math"), text(47, 465, "E[xi_k | F_k]=0", 16, 650, cls="math"), text(47, 498, "先声明 estimand、history 与 sampling law。", 15, fill=MUTED)]

    heading(out, 430, "B", "batch 方差律依赖抽样结构", TEAL)
    out += [line(455, 420, 765, 420, GRID, 2), line(475, 440, 475, 105, GRID, 2), text(760, 448, "batch B", 15, 650, "end"), text(435, 112, "variance", 15, 650)]
    iid, corr, wor = [], [], []
    for i in range(1, 101):
        x = 478 + i * 2.72
        iid.append((x, 400 - 275 / math.sqrt(i)))
        corr.append((x, 300 - 175 / math.sqrt(i)))
        wor.append((x, 410 - 300 * math.sqrt(max(0.0, (101 - i) / (101 * i)))))
    out += [polyline(iid, BLUE, 3), polyline(corr, RED, 3), polyline(wor, TEAL, 2.5, "7 5")]
    out += [text(630, 348, "iid: sigma^2/B", 15, 700, fill=BLUE), text(590, 270, "positive correlation: plateau", 15, 700, fill=RED), text(505, 380, "without replacement (zero at N)", 15, 650, fill=TEAL)]
    out += [text(430, 486, "standard deviation scales as 1/sqrt(B), not 1/B。", 15, fill=MUTED)]

    heading(out, 830, "C", "固定步长的 transient 与平台", RED)
    out += [line(845, 420, 1155, 420, GRID, 2), line(865, 440, 865, 105, GRID, 2), text(1150, 448, "iterations", 15, 650, "end"), text(820, 112, "error", 15, 650)]
    high, low = [], []
    for i in range(101):
        x = 870 + i * 2.7
        high.append((x, 140 + 205 * (1 - math.exp(-i / 17))))
        low.append((x, 140 + 265 * (1 - math.exp(-i / 34))))
    out += [polyline(high, RED, 3.5), polyline(low, TEAL, 3), line(870, 345, 1145, 345, RED, 1.8, "7 5")]
    out += [text(1000, 320, "large eta / small B", 15, 700, fill=RED), text(990, 400, "small eta / large B", 15, 700, fill=TEAL), text(825, 470, "typical floor scale: eta sigma^2/(mu B)", 15, 650, cls="math"), text(825, 499, "优化误差平台不自动说明泛化好坏。", 15, fill=MUTED)]
    return finish(out, "SGD 定理从条件 oracle 与方差预算出发；batch、步长、样本预算和部署指标必须分层报告。")


FIGURES = {
    "fig-smooth-strong-convex-condition-v2.svg": smooth_strong_condition,
    "fig-gradient-descent-rates-v2.svg": gradient_descent_rates,
    "fig-acceleration-momentum-lower-bound-v2.svg": acceleration_momentum,
    "fig-sgd-minibatch-noise-v2.svg": sgd_minibatch_noise,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
