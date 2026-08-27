#!/usr/bin/env python3
"""Generate v2 textbook figures for OPT-09--12 metric and constraints."""

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


def adaptive_geometry():
    out = begin(
        "自适应优化的 variable metric、状态流与正则边界",
        "对角自适应方法用历史梯度统计改变各坐标移动代价；AdaGrad、RMSProp 与 Adam 的状态递推不同；coupled L2、AdamW 和 AMSGrad 分别改变梯度、参数更新和二阶状态上界。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "metric 改变最陡方向", BLUE)
    cx, cy = 205, 275
    out += [circle(cx, cy, 112, GRID, "none", 2), f'<ellipse cx="{cx}" cy="{cy}" rx="145" ry="62" fill="none" stroke="{TEAL}" stroke-width="2.5"/>']
    out += [circle(cx, cy, 6, INK, INK), line(cx, cy, 305, 165, RED, 3, marker="a2"), line(cx, cy, 315, 275, BLUE, 3, marker="a0"), line(cx, cy, 270, 350, TEAL, 3, marker="a1")]
    out += [text(308, 158, "gradient g", 15, 700, fill=RED), text(290, 260, "Euclidean -g", 15, 700, fill=BLUE), text(250, 376, "-H_t^-1 g", 15, 700, fill=TEAL)]
    out += [text(45, 425, "step = argmin_d {g^T d + d^T H_t d/(2 alpha)}", 15, 650, cls="math"), text(45, 463, "diagonal H_t rescales axes；dense H_t also rotates。", 15, fill=MUTED), text(45, 496, "gradient squares do not reveal Hessian signs or eigenvectors。", 15, fill=MUTED)]

    heading(out, 430, "B", "三种状态递推不能混写", TEAL)
    node(out, 455, 98, 105, 50, "g_t", BLUE)
    out += [line(560, 123, 600, 123, INK, 2.4, marker="a3")]
    node(out, 605, 98, 135, 50, "g_t squared", TEAL, size=16)
    rows = (("AdaGrad", "s_t=s_(t-1)+g_t^2", 188, BLUE), ("RMSProp", "v_t=beta v_(t-1)+(1-beta)g_t^2", 282, TEAL), ("Adam", "m_t / v_t EMA + bias correction", 376, RED))
    for label, eq, y, color in rows:
        out += [text(435, y, label, 17, 700, fill=color), line(520, y - 6, 550, y - 6, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(562, y, eq, 15, 650)]
    out += [text(430, 440, "update: -alpha * m_hat/(sqrt(v_hat)+epsilon)", 15, 650, cls="math"), text(430, 477, "epsilon location、initialization、dtype 都属于算法定义。", 15, fill=MUTED)]

    heading(out, 830, "C", "三种机制各改一层", RED)
    out += [text(830, 112, "coupled L2", 17, 700, fill=RED), text(830, 145, "P_t (g_t + lambda x_t)", 16, 650, cls="math"), text(830, 176, "penalty gradient is adaptively rescaled", 15, fill=MUTED)]
    out += [line(830, 202, 1145, 202, GRID, 2), text(830, 245, "AdamW", 17, 700, fill=BLUE), text(830, 278, "P_t g_t  +  lambda x_t", 16, 650, cls="math"), text(830, 309, "decay is outside adaptive preconditioner", 15, fill=MUTED)]
    out += [line(830, 335, 1145, 335, GRID, 2), text(830, 378, "AMSGrad", 17, 700, fill=TEAL), text(830, 411, "vbar_t = max(vbar_(t-1), v_t)", 16, 650, cls="math"), text(830, 442, "prevents denominator from decreasing", 15, fill=MUTED), text(830, 485, "safeguard != universal convergence", 15, 650, fill=RED)]
    return finish(out, "自适应优化首先是一种历史依赖的坐标几何；曲率解释、正则解释与收敛解释都需要额外证据。")


def newton_family():
    out = begin(
        "Newton、Gauss-Newton 与拟 Newton 的曲率对象和验收层",
        "Newton 用目标 Hessian 的局部二次模型；Gauss-Newton 保留最小二乘 Jacobian Gram 项；BFGS 通过 secant pairs 学习正定曲率近似；线性子问题残差与外层接受规则必须分别验收。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Newton 最小化局部二次模型", BLUE)
    out += [line(50, 410, 365, 410, GRID, 2), line(80, 435, 80, 95, GRID, 2)]
    curve, quad = [], []
    xk = 145
    for i in range(121):
        x = 80 + i * 2.3
        z = (x - 230) / 105
        curve.append((x, 350 - 120 * z * z + 18 * z**3))
        q = (x - 225) / 105
        quad.append((x, 348 - 105 * q * q))
    out += [polyline(curve, BLUE, 3.5), polyline(quad, RED, 2.5, "7 5")]
    xnew = 225
    out += [circle(xk, 245, 7, BLUE, BLUE), circle(xnew, 348, 7, TEAL, TEAL), line(xk, 425, xnew, 425, TEAL, 3, marker="a1")]
    out += [text(xk, 225, "x_k", 16, 700, "middle", fill=BLUE), text(xnew, 375, "x_k+p_N", 15, 700, "middle", fill=TEAL), text(265, 145, "m_k(p)", 16, 700, fill=RED)]
    out += [text(45, 465, "solve H_k p = -g_k；do not form H_k^-1", 16, 650, cls="math"), text(45, 498, "indefinite / singular H requires modification or trust region。", 15, fill=MUTED)]

    heading(out, 430, "B", "三类方法使用不同曲率对象", TEAL)
    y = 102
    out += [text(430, y, "exact Newton", 17, 700, fill=BLUE), text(430, y + 36, "H = J^T J + sum_i r_i Hessian(r_i)", 15, 650, cls="math"), text(430, y + 67, "retains residual-weighted second derivatives", 15, fill=MUTED)]
    y = 235
    out += [text(430, y, "Gauss-Newton", 17, 700, fill=TEAL), text(430, y + 36, "G = J^T J  >= 0", 16, 650, cls="math"), text(430, y + 67, "exact for affine residual；good near small residual", 15, fill=MUTED)]
    y = 368
    out += [text(430, y, "BFGS / L-BFGS", 17, 700, fill=RED), text(430, y + 36, "B_(k+1) s_k = y_k", 16, 650, cls="math"), text(430, y + 67, "s^T y > 0 protects positive definiteness", 15, fill=MUTED), text(430, 485, "GGN、Fisher、empirical Fisher 也不是同一矩阵。", 15, 650)]

    heading(out, 830, "C", "模型、求解、全局化三层验收", RED)
    stages = (("1  model", "choose H / GN / BFGS", BLUE), ("2  inner solve", "||B p + g|| <= tolerance", TEAL), ("3  accept step", "line search or trust ratio", RED))
    for i, (label, desc, color) in enumerate(stages):
        yy = 105 + i * 125
        node(out, 840, yy, 130, 58, label, color, size=16)
        out += [line(975, yy + 29, 1005, yy + 29, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(1015, yy + 23, desc, 15, 650)]
        if i < 2:
            out.append(line(905, yy + 62, 905, yy + 116, GRID, 2, "5 5"))
    out += [text(830, 465, "inner residual small != outer step accepted", 15, 650, fill=RED), text(830, 497, "local fast rate needs an attraction region。", 15, fill=MUTED)]
    return finish(out, "二阶法的名称不够：必须同时声明曲率矩阵、线性求解精度和接受规则。")


def projection_geometry():
    out = begin(
        "切锥、法锥、投影梯度与常见投影算子",
        "边界最优性由切锥中没有下降方向或负梯度属于法锥表达；投影将不可行 raw step 拉回闭凸集；gradient mapping 连接原点与投影点；不同约束集具有不同投影算法。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "边界最优性是 polar 几何", BLUE)
    out += [path("M55 390C120 330 170 250 205 125C260 185 315 300 360 390Z", BLUE, 3, "#EFF6FF")]
    x, y = 205, 125
    out += [circle(x, y, 7, BLUE, BLUE), path(f"M{x} {y}L80 365L345 365Z", TEAL, 2.5, "none", "7 5"), line(x, y, x, 55, RED, 3, marker="a2")]
    out += [text(95, 330, "tangent cone T_C(x)", 16, 700, fill=TEAL), text(218, 72, "normal cone N_C(x)", 15, 700, fill=RED), text(45, 430, "<n,d> <= 0 for all d in T_C(x)", 16, 650, cls="math"), text(45, 467, "-grad f(x*) in N_C(x*)", 17, 700, cls="math"), text(45, 498, "gradient need not vanish at a constrained optimum。", 15, fill=MUTED)]

    heading(out, 430, "B", "raw step 越界，projection 拉回", TEAL)
    out += [path("M450 165C500 105 620 105 690 155C770 215 735 370 620 405C510 440 420 340 450 165Z", BLUE, 3, "#EFF6FF")]
    xk, raw, proj = (535, 250), (725, 95), (680, 170)
    out += [circle(*xk, 7, BLUE, BLUE), circle(*raw, 7, RED, RED), circle(*proj, 7, TEAL, TEAL), line(xk[0], xk[1], raw[0], raw[1], RED, 3, "7 5", "a2"), line(raw[0], raw[1], proj[0], proj[1], TEAL, 3, marker="a1"), line(xk[0], xk[1], proj[0], proj[1], BLUE, 3, marker="a0")]
    out += [text(515, 278, "x_k", 15, 700, fill=BLUE), text(700, 82, "raw", 15, 700, fill=RED), text(685, 190, "Pi_C(raw)", 15, 700, fill=TEAL)]
    out += [text(430, 450, "G_eta(x) = (x-Pi_C(x-eta grad f))/eta", 15, 650, cls="math"), text(430, 486, "G_eta=0 is the projected stationarity certificate。", 15, fill=MUTED)]

    heading(out, 830, "C", "集合不同，projection 算法不同", RED)
    # simplex
    out += [path("M850 190L900 105L950 190Z", BLUE, 2.5), circle(900, 145, 5, BLUE, BLUE), text(900, 220, "simplex: sort + threshold", 15, 650, "middle")]
    # ball
    out += [circle(1070, 150, 48, TEAL, "none", 2.5), line(1070, 150, 1132, 110, RED, 2.5, "6 4"), line(1070, 150, 1110, 124, TEAL, 3), text(1070, 220, "ball: radial clipping", 15, 650, "middle")]
    # affine / PSD
    out += [line(850, 330, 955, 275, BLUE, 3), line(885, 395, 990, 340, BLUE, 3), line(930, 290, 930, 365, TEAL, 3, "6 4"), text(900, 425, "affine: linear solve", 15, 650, "middle")]
    out += [path("M1030 285L1135 285L1110 395L1055 395Z", RED, 2.5), text(1082, 345, "X >= 0", 16, 700, "middle", RED), text(1090, 425, "PSD: eigenvalue clipping", 15, 650, "middle")]
    out += [text(825, 486, "nonconvex set may have multiple projections。", 15, fill=MUTED)]
    return finish(out, "投影不是一个抽象按钮：最优性依赖锥几何，算法与误差预算依赖具体集合结构。")


def kkt_certificate():
    out = begin(
        "KKT 的法向平衡、四组证书与逻辑层级",
        "活跃约束的法向量以非负乘子平衡目标梯度；KKT 包含 primal feasibility、dual feasibility、stationarity 与 complementary slackness；CQ 给必要性，凸性给充分性，二阶条件负责非凸分类。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "活跃法向量平衡目标梯度", BLUE)
    out += [path("M55 400L55 210C130 195 205 160 275 105L355 105L355 400Z", BLUE, 3, "#EFF6FF")]
    x, y = 205, 160
    out += [circle(x, y, 7, INK, INK), line(x, y, 120, 260, RED, 3, marker="a2"), line(x, y, 280, 88, TEAL, 3, marker="a1"), line(x, y, 315, 145, BLUE, 3, marker="a0")]
    out += [text(88, 280, "grad f", 15, 700, fill=RED), text(280, 80, "lambda_1 grad g_1", 15, 700, fill=TEAL), text(275, 172, "lambda_2 grad g_2", 15, 700, fill=BLUE)]
    out += [text(45, 435, "grad f + sum_i lambda_i grad g_i + J_h^T nu = 0", 15, 650, cls="math"), text(45, 470, "inactive constraint -> lambda_i=0", 16, 650), text(45, 498, "multiplier signs follow the declared inequality convention。", 15, fill=MUTED)]

    heading(out, 430, "B", "四组条件共同组成证书", TEAL)
    items = (("primal feasible", "g(x)<=0, h(x)=0", BLUE), ("dual feasible", "lambda>=0", TEAL), ("stationarity", "grad_x L=0", RED), ("complementarity", "lambda_i g_i(x)=0", BLUE))
    for i, (label, eq, color) in enumerate(items):
        yy = 105 + i * 92
        out += [circle(455, yy, 7, color, color), line(465, yy, 500, yy, color, 2.5), text(510, yy - 7, label, 16, 700, fill=color), text(510, yy + 24, eq, 15, 650, cls="math")]
    out += [line(455, 115, 455, 375, GRID, 2, "5 5"), text(430, 470, "scale and report all four residuals separately。", 15, fill=MUTED)]

    heading(out, 830, "C", "必要、充分与分类不可混写", RED)
    stages = (("local optimum + CQ", "KKT is necessary", RED), ("convex problem + KKT", "global optimum", TEAL), ("nonconvex KKT point", "check critical-cone Hessian", BLUE))
    for i, (assumption, result, color) in enumerate(stages):
        yy = 105 + i * 125
        out += [text(835, yy, assumption, 16, 700, fill=color), line(835, yy + 18, 960, yy + 18, color, 2.5, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2"), text(978, yy + 24, result, 15, 650)]
    out += [text(830, 465, "CQ failure: optimum may have no multiplier", 15, 650, fill=RED), text(830, 497, "KKT alone gives neither strong duality nor SOSC。", 15, fill=MUTED)]
    return finish(out, "KKT 是带假设方向的证书系统：先检查符号与可行性，再检查 CQ、凸性和二阶曲率。")


FIGURES = {
    "fig-adaptive-optimizers-geometry-v2.svg": adaptive_geometry,
    "fig-newton-gn-quasinewton-v2.svg": newton_family,
    "fig-projection-feasible-directions-v2.svg": projection_geometry,
    "fig-lagrange-kkt-v2.svg": kkt_certificate,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
