#!/usr/bin/env python3
"""Generate v2 textbook figures for DYN-05--08 numerics and transport."""

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


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "dynamics"


def runge_kutta():
    out = begin(
        "一步法的 local-to-global 误差、RK stages 与自适应控制",
        "一步 exact-start defect 经约一除以 h 个步和离散稳定性放大形成 global error；Runge–Kutta 在单步内组合多个 stage slopes 满足阶条件；embedded estimator 只控制缩放局部误差，接受轨迹、全局误差与训练梯度仍需分别验收。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "局部阶还要经过稳定累积", BLUE)
    node(out, 45, 95, 315, 60, "one-step defect O(h^(p+1))", BLUE, size=15)
    out += [line(202, 158, 202, 195, INK, 2.2, marker="a3")]
    node(out, 45, 207, 315, 65, "N ~= (T-t0)/h steps", TEAL, size=15)
    out += [line(202, 275, 202, 312, INK, 2.2, marker="a3")]
    node(out, 45, 324, 315, 70, "global error O(h^p)", RED, size=16)
    out += [text(45, 430, "e_(n+1) <= (1+Lh)e_n + C h^(p+1)", 14, 650, cls="math"), text(45, 466, "discrete Gronwall supplies exp(LT)", 15, 650), text(45, 500, "consistency without stability is insufficient。", 15, fill=MUTED)]

    heading(out, 430, "B", "RK 在同一步内组合 stage slopes", TEAL)
    out += [text(430, 100, "t_n", 15, 700, fill=BLUE), line(475, 96, 755, 96, GRID, 2), text(748, 122, "t_n+h", 15, 700, "end", fill=BLUE)]
    stages = ((505, 165, "k1=f(t_n,y_n)", BLUE), (585, 240, "k2", TEAL), (665, 300, "k3", TEAL), (735, 360, "ks", RED))
    for x, y, label, color in stages:
        out += [circle(x, y, 8, color, color), text(x, y - 18, label, 14, 650, "middle", fill=color)]
    out += [path("M470 400 C540 350 625 420 755 315", INK, 2.5), text(430, 438, "y_(n+1)=y_n+h sum b_i k_i", 16, 700, cls="math"), text(430, 472, "order conditions match the flow expansion", 15, 650), text(430, 502, "more stages trade NFE for accuracy/stability。", 15, fill=MUTED)]

    heading(out, 830, "C", "embedded pair 控制一张局部账", RED)
    node(out, 840, 92, 300, 58, "shared stages -> high / low updates", BLUE, size=14)
    out += [line(990, 153, 990, 190, INK, 2.2, marker="a3")]
    node(out, 840, 202, 300, 65, "scaled error norm E", TEAL, size=15)
    out += [line(990, 270, 990, 307, INK, 2.2, marker="a3")]
    node(out, 840, 319, 300, 70, "accept/reject； h_new~h E^(-1/(p+1))", RED, size=13)
    out += [text(830, 429, "atol/rtol define component scales", 15, 650), text(830, 460, "rejected steps and dense output count", 15, 650), text(830, 490, "global state / events / gradient are separate", 15, 650, fill=RED), text(830, 516, "tolerance is not a theorem of task accuracy。", 15, fill=MUTED)]
    return finish(out, "ODE 求解可信度由 local defect、传播稳定性和自适应账本共同组成；高阶与小 tolerance 都不是全局任务保证。")


def stiffness():
    out = begin(
        "刚性时间尺度、绝对稳定与隐式代数合同",
        "刚性系统的快衰减模态会约束显式稳定步长，即使目标轨迹变化缓慢；绝对稳定用 R(z) 判断 test equation 的数值放大，A 稳定与 L 稳定有不同 stiff damping；隐式步还需 nonlinear 和 linear solve 证书。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "快误差模态绑住慢目标的步长", BLUE)
    out += [line(55, 370, 365, 370, GRID, 2), line(75, 405, 75, 95, GRID, 2)]
    out += [path("M75 175 C140 185 210 205 360 240", BLUE, 3), path("M75 115 C90 320 110 260 130 238 C160 220 230 225 360 240", RED, 2.5)]
    out += [text(250, 205, "slow solution", 15, 700, fill=BLUE), text(100, 120, "fast decaying error", 15, 700, fill=RED), text(45, 420, "e'=lambda_fast e,  Re lambda_fast <<0", 15, 650, cls="math"), text(45, 455, "Forward Euler needs |1+h lambda|<=1", 15, 650), text(45, 489, "step chosen for stability, not visible motion。", 15, fill=MUTED)]

    heading(out, 430, "B", "R(z) 分开稳定与刚性阻尼", TEAL)
    out += [line(450, 270, 770, 270, GRID, 2), line(610, 405, 610, 105, GRID, 2), text(748, 295, "Re z", 14, 650), text(620, 120, "Im z", 14, 650)]
    out.append(f'<circle cx="530" cy="270" r="80" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    out += [text(470, 180, "FE disk", 15, 700, fill=BLUE), text(625, 165, "A-stable:", 15, 700, fill=TEAL), text(625, 193, "entire left half-plane", 14, 650), text(625, 235, "L-stable:", 15, 700, fill=RED), text(625, 263, "R(z)->0 as z->-infinity", 14, 650)]
    out += [line(430, 430, 765, 430, GRID, 2), text(430, 461, "stable large h can still be inaccurate", 15, 700, fill=RED), text(430, 492, "trapezoidal is A-, not L-stable。", 15, fill=MUTED)]

    heading(out, 830, "C", "隐式一步引入嵌套求解", RED)
    node(out, 840, 90, 300, 58, "F(y_(n+1))=0", BLUE, size=15)
    out += [line(990, 151, 990, 187, INK, 2.2, marker="a3")]
    node(out, 840, 199, 300, 65, "Newton: (I-hJ) delta=-F", TEAL, size=14)
    out += [line(990, 267, 990, 303, INK, 2.2, marker="a3")]
    node(out, 840, 315, 300, 70, "linear solve + preconditioner", RED, size=15)
    out += [text(830, 425, "separate time, nonlinear and linear tolerances", 14, 650), text(830, 455, "check residual, step error and Jacobian reuse", 14, 650), text(830, 485, "reverse sensitivity solves a transpose system", 14, 650), text(830, 513, "A-stability does not certify these layers。", 15, fill=MUTED)]
    return finish(out, "刚性首先是稳定成本问题；隐式方法扩大稳定域，却把一次时间步变成需要多层残差与线性代数验收的任务。")


def flow_liouville_cnf():
    out = begin(
        "流映射、Jacobian 体积演化与 CNF 增广状态",
        "唯一可微 ODE 流将整片初值搬运到新时间切片；初值 Jacobian 满足变分方程，Jacobi 公式将 log determinant 导数化为 divergence；CNF 同时积分状态和负 divergence 的 log density，并承担 trace 与 solver 误差。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "唯一流把整片状态一致搬运", BLUE)
    for y in (140, 220, 300, 380):
        out += [circle(75, y, 6, BLUE, BLUE), circle(330, y - 25 + (y % 70), 6, TEAL, TEAL), path(f"M82 {y} C155 {y-35} 245 {y+25} 323 {y-25+(y%70)}", GRID, 2)]
    out += [text(45, 100, "time s", 15, 700, fill=BLUE), text(315, 100, "time t", 15, 700, fill=TEAL), text(45, 430, "phi_(s,s)=I", 15, 650, cls="math"), text(45, 458, "phi_(r,t) o phi_(s,r)=phi_(s,t)", 15, 650, cls="math"), text(45, 491, "uniqueness => no crossing / injectivity", 15, 650), text(45, 516, "surjectivity needs backward completeness。", 14, fill=MUTED)]

    heading(out, 430, "B", "变分方程把局部形变压成 divergence", TEAL)
    node(out, 445, 92, 310, 58, "Jdot=(D_x f) J； J(s)=I", BLUE, size=14)
    out += [line(600, 153, 600, 190, INK, 2.2, marker="a3")]
    node(out, 445, 202, 310, 68, "d/dt log det J = tr(D_x f)", TEAL, size=14)
    out += [line(600, 273, 600, 310, INK, 2.2, marker="a3")]
    node(out, 445, 322, 310, 68, "det J=exp integral div f >0", RED, size=14)
    out += [text(430, 430, "divergence controls infinitesimal volume", 15, 650), text(430, 462, "not trajectory norm or asymptotic stability", 15, 650, fill=RED), text(430, 500, "shape distortion also depends on full J。", 15, fill=MUTED)]

    heading(out, 830, "C", "CNF 同时积分状态与 log density", RED)
    node(out, 840, 92, 300, 62, "xdot=f_theta(t,x)", BLUE, size=15)
    out += [line(990, 157, 990, 194, INK, 2.2, marker="a3")]
    node(out, 840, 206, 300, 72, "d log p_t(x_t)/dt = -div f_theta", TEAL, size=13)
    out += [line(990, 281, 990, 318, INK, 2.2, marker="a3")]
    node(out, 840, 330, 300, 65, "trace: exact or Hutchinson JVP/VJP", RED, size=13)
    out += [text(830, 435, "audit solver + trace + likelihood", 15, 650), text(830, 466, "fix probe reuse/stop-gradient semantics", 14, 650), text(830, 496, "finite-step map need not preserve exact flow", 14, 650, fill=RED), text(830, 520, "support/topology limits remain。", 14, fill=MUTED)]
    return finish(out, "CNF 密度公式来自可微流的 Jacobian 体积演化；trace 估计、数值积分和训练梯度是额外误差层。")


def continuity_equation():
    out = begin(
        "控制体守恒、三种运输语言与离散/生成边界",
        "固定控制体的质量变化等于负净外流加 source；散度定理给局部 continuity PDE，characteristics、pushforward 与 weak form 是同一守恒的不同语言；边界通量、finite-volume flux 与 Flow Matching 边缘速度各有独立合同。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "局部 PDE 来自任意控制体账本", BLUE)
    out += [rect(105, 150, 190, 190, BLUE, BG, 8, 2.5), text(200, 245, "K", 28, 700, "middle", fill=BLUE)]
    for x1, y1, x2, y2 in ((65, 190, 105, 190), (295, 220, 345, 220), (180, 105, 180, 150), (235, 340, 235, 390)):
        out.append(line(x1, y1, x2, y2, RED, 3, marker="a2"))
    out += [text(45, 420, "d/dt integral_K rho", 16, 700, cls="math"), text(45, 450, "= - integral_boundaryK j dot n + integral_K s", 14, 650, cls="math"), text(45, 486, "j=rho v -> partial_t rho+div(rho v)=s", 14, 650), text(45, 514, "outward flux carries a minus sign。", 15, fill=MUTED)]

    heading(out, 430, "B", "三种语言互相校验", TEAL)
    node(out, 445, 90, 310, 55, "particles: Xdot_t=v_t(X_t)", BLUE, size=14)
    out += [line(600, 148, 600, 181, INK, 2.1, marker="a3")]
    node(out, 445, 193, 310, 62, "measures: mu_t=(X_t)_# mu_0", TEAL, size=14)
    out += [line(600, 258, 600, 291, INK, 2.1, marker="a3")]
    node(out, 445, 303, 310, 65, "PDE: partial_t rho+div(rho v)=0", RED, size=13)
    out += [text(430, 405, "weak: d/dt integral psi dmu", 15, 650), text(430, 434, "= integral grad psi dot v dmu", 15, 650), text(430, 472, "weak form includes Dirac measures", 15, 650), text(430, 501, "density formula needs extra regularity。", 15, fill=MUTED)]

    heading(out, 830, "C", "边界、离散与生成语义", RED)
    certs = (("boundary", "periodic / no-flux / inflow-outflow", BLUE), ("finite volume", "shared face flux => conservation", TEAL), ("Flow Matching", "conditional fields -> marginal velocity", RED))
    for i, (name, claim, color) in enumerate(certs):
        yy = 103 + i * 104
        out += [text(830, yy, name, 16, 700, fill=color), text(830, yy + 31, claim, 14, 650)]
        if i < 2:
            out.append(line(830, yy + 56, 1145, yy + 56, GRID, 2))
    out += [text(830, 426, "pointwise residual != global conservation", 15, 700, fill=RED), text(830, 457, "same density path may admit many velocities", 14, 650), text(830, 488, "OT adds a kinetic-energy selection", 14, 650), text(830, 516, "shocks/entropy need conservation-law theory。", 14, fill=MUTED)]
    return finish(out, "连续性方程是控制体守恒的局部语言；粒子、测度、弱 PDE 与数值通量必须在各自假设下对齐。")


FIGURES = {
    "fig-runge-kutta-error-adaptivity-v2.svg": runge_kutta,
    "fig-stiffness-stability-implicit-solve-v2.svg": stiffness,
    "fig-flow-liouville-cnf-v2.svg": flow_liouville_cnf,
    "fig-continuity-conservation-flow-matching-v2.svg": continuity_equation,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
