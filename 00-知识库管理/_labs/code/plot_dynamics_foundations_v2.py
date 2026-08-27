#!/usr/bin/env python3
"""Generate v2 textbook figures for DYN-01--04 ODE foundations."""

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


def ode_ivp():
    out = begin(
        "ODE 初值问题的适定性阶梯与三层对象",
        "初值问题先改写为函数空间积分算子的固定点；连续性、局部 Lipschitz 与增长或先验界分别支持存在、唯一连续依赖和全局延拓；精确流、数值轨迹与 Neural ODE 训练声明是不同层级。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "把轨迹变成函数空间固定点", BLUE)
    node(out, 45, 95, 315, 58, "candidate path y(t)", BLUE)
    out += [line(202, 156, 202, 193, INK, 2.2, marker="a3")]
    node(out, 45, 205, 315, 78, "T[y](t)=y0+integral f(s,y(s)) ds", TEAL, size=14)
    out += [line(202, 286, 202, 323, INK, 2.2, marker="a3")]
    node(out, 45, 335, 315, 62, "fixed point y=T[y]", RED, size=16)
    out += [text(45, 435, "choose a closed ball in C([t0,t0+h])", 15, 650), text(45, 468, "self-map + contraction => unique local path", 15, 650), text(45, 501, "h depends on bounds and Lipschitz scale。", 15, fill=MUTED)]

    heading(out, 430, "B", "四级结论需要不同资源", TEAL)
    ladder = (("existence", "continuity / compactness", BLUE), ("uniqueness", "state-local Lipschitz", TEAL), ("continuous dependence", "Gronwall estimate", RED), ("global continuation", "no-blow-up criterion", BLUE))
    for i, (claim, resource, color) in enumerate(ladder):
        yy = 92 + i * 95
        node(out, 445, yy, 165, 55, claim, color, size=13 if i == 2 else 14)
        out += [line(613, yy + 28, 635, yy + 28, INK, 2, marker="a3"), text(648, yy + 34, resource, 13, 650)]
    out += [text(430, 486, "continuity alone may allow many solutions", 15, 650, fill=RED), text(430, 514, "local uniqueness does not forbid blow-up。", 15, fill=MUTED)]

    heading(out, 830, "C", "模型、精确流与求解器不可混同", RED)
    stages = (("vector field f_theta", BLUE), ("exact flow Phi_(t,s)", TEAL), ("numerical trajectory y_h", RED), ("training / empirical claim", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 90 + i * 92
        node(out, 840, yy, 300, 56, label, color, size=15)
        if i < 3:
            out.append(line(990, yy + 59, 990, yy + 85, INK, 2.2, marker="a3"))
    out += [text(830, 472, "well-posedness precedes discretization", 15, 650), text(830, 501, "solver success != model/generalization proof。", 15, fill=MUTED)]
    return finish(out, "ODE 符号只是起点：固定点给局部解，Gronwall 给稳定依赖，延拓条件给时间范围，数值与学习声明另行验收。")


def linear_ode():
    out = begin(
        "线性 ODE 的传播算子、时间模态与精确采样",
        "状态转移矩阵用恒等、复合与逆组织齐次传播，variation of constants 叠加输入响应；特征值、Jordan 与非正规几何分别控制渐近、 polynomial factor 与 transient；零阶保持把连续系统精确映为离散递推但不消除 aliasing。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "状态转移组织初值与输入", BLUE)
    node(out, 45, 92, 315, 56, "x(s)", BLUE)
    out += [line(202, 151, 202, 188, INK, 2.2, marker="a3")]
    node(out, 45, 200, 315, 65, "Phi(t,s) x(s)", TEAL)
    out += [text(45, 302, "Phi(t,r) Phi(r,s)=Phi(t,s)", 15, 700, cls="math"), text(45, 338, "Phi(s,t)=Phi(t,s)^{-1}", 15, 650, cls="math"), line(45, 370, 360, 370, GRID, 2), text(45, 402, "x(t)=Phi(t,s)x(s)+", 15, 650, cls="math"), text(45, 427, "integral Phi(t,tau) B u(tau) d tau", 15, 650, cls="math"), text(45, 482, "constant A: Phi=e^{(t-s)A}。", 15, fill=MUTED)]

    heading(out, 430, "B", "三个谱对象控制不同时间行为", TEAL)
    modes = (("Re lambda", "exponential tail", BLUE), ("Jordan chain", "t^j e^{lambda t}", TEAL), ("nonnormal basis", "finite-time amplification", RED))
    for i, (obj, effect, color) in enumerate(modes):
        yy = 100 + i * 112
        out += [circle(450, yy, 7, color, color), text(474, yy + 5, obj, 16, 700, fill=color), text(474, yy + 34, effect, 15, 650)]
    out += [line(430, 417, 765, 417, GRID, 2), text(430, 450, "spectral abscissa: asymptotic rate", 15, 650), text(430, 479, "numerical abscissa / resolvent: transient", 15, 650, fill=RED), text(430, 508, "stable eigenvalues need not mean monotone norm。", 15, fill=MUTED)]

    heading(out, 830, "C", "ZOH 精确采样仍有语义边界", RED)
    node(out, 840, 92, 300, 62, "continuous: xdot=A x+B u", BLUE, size=15)
    out += [line(990, 157, 990, 194, INK, 2.2, marker="a3")]
    out += [rect(840, 206, 300, 82, TEAL, BG, 10, 2), text(990, 239, "Abar=e^(Delta A)", 14, 650, "middle", fill=TEAL), text(990, 265, "Bbar=integral e^(tau A)B d tau", 14, 650, "middle", fill=TEAL)]
    out += [line(990, 291, 990, 328, INK, 2.2, marker="a3")]
    node(out, 840, 340, 300, 62, "x_(k+1)=Abar x_k+Bbar u_k", RED, size=14)
    out += [text(830, 444, "recurrence <-> causal convolution", 15, 650), text(830, 473, "exact only under the hold assumption", 15, 650, fill=RED), text(830, 502, "sampling can alias continuous frequencies。", 15, fill=MUTED)]
    return finish(out, "线性动力学由传播算子统一；谱解释、输入卷积与采样递推各有独立假设和验收边界。")


def phase_portrait():
    out = begin(
        "相图对象、二维分类与非线性线性化边界",
        "相图必须区分 vector field、nullcline 和 orbit；二维线性平衡点可由 trace、determinant 与 discriminant 分类；非线性 Jacobian 在线性化双曲时给局部结论，零实部时同一 Jacobian 可对应吸引或排斥。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "箭头、零流线与轨道是三种对象", BLUE)
    out += [line(55, 320, 360, 320, GRID, 2), line(200, 420, 200, 95, GRID, 2)]
    for x, y, dx, dy in ((85, 150, 42, 25), (100, 350, 38, -30), (255, 140, -35, 32), (300, 365, -45, -20)):
        out.append(line(x, y, x + dx, y + dy, BLUE, 2.3, marker="a1"))
    out += [path("M75 390 C120 250 160 180 225 205 C290 230 315 285 345 120", TEAL, 3), path("M65 245 C150 250 250 270 350 285", RED, 2, "7 5"), path("M235 100 C225 200 220 300 215 410", RED, 2, "7 5")]
    out += [text(65, 455, "blue: vector field", 15, 650, fill=BLUE), text(65, 480, "red dashed: nullclines", 15, 650, fill=RED), text(65, 505, "green: one oriented orbit。", 15, fill=TEAL)]

    heading(out, 430, "B", "trace–determinant 先定线性类型", TEAL)
    out += [line(455, 330, 765, 330, GRID, 2), line(600, 440, 600, 90, GRID, 2), text(745, 353, "trace", 14, 650), text(608, 105, "det", 14, 650)]
    out += [text(455, 380, "det<0: saddle", 15, 700, fill=RED), text(465, 165, "trace<0", 15, 700, fill=TEAL), text(465, 190, "stable node/focus", 15, 650), text(635, 165, "trace>0", 15, 700, fill=RED), text(635, 190, "unstable node/focus", 15, 650), text(610, 295, "Delta=tr^2-4 det", 14, 650), text(610, 318, "node vs focus", 14, fill=MUTED)]
    out += [text(430, 470, "center / repeated boundary needs care", 15, 650), text(430, 500, "classification assumes an isolated equilibrium。", 15, fill=MUTED)]

    heading(out, 830, "C", "Jacobian 只在双曲情形作判决", RED)
    node(out, 840, 92, 300, 55, "J*=Df(x*)", BLUE)
    out += [line(990, 150, 990, 187, INK, 2.2, marker="a3")]
    node(out, 840, 199, 300, 65, "all Re lambda<0 -> local exponential", TEAL, size=14)
    out += [line(990, 267, 990, 304, INK, 2.2, marker="a3")]
    node(out, 840, 316, 300, 65, "some Re lambda>0 -> unstable", RED, size=14)
    out += [text(830, 420, "zero real part: linearization inconclusive", 15, 700, fill=RED), text(830, 452, "xdot=-x^3 attracts； xdot=+x^3 repels", 15, 650), text(830, 484, "same J*=0, opposite nonlinear behavior", 15, 650), text(830, 512, "local type != basin or global portrait。", 15, fill=MUTED)]
    return finish(out, "相图先分对象，再按线性谱分类；非线性结论只有在定理假设内成立，非双曲边界必须回到高阶项。")


def lyapunov():
    out = begin(
        "Lyapunov 子水平集、LaSalle 与多种证书语义",
        "正定标量函数的子水平集把轨道约束在嵌套区域；导数符号依次支持稳定、渐近或指数结论，半负定时 LaSalle 还需寻找零导数集中的最大不变子集；连续、离散与学习证书验证的是不同不等式。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一个标量约束所有未来轨道", BLUE)
    for rx, ry, color in ((145, 105, GRID), (110, 78, GRID), (72, 48, TEAL)):
        out.append(f'<ellipse cx="205" cy="270" rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-width="2"/>')
    out += [path("M335 180 C290 205 290 335 235 300 C195 276 230 235 205 270", BLUE, 3, marker="a1"), circle(205, 270, 7, RED, RED), text(218, 260, "x*", 15, 700, fill=RED)]
    out += [text(45, 410, "Omega_c={x: V(x)<=c}", 16, 700, cls="math"), text(45, 445, "V>0 and Vdot<=0 => forward invariance", 15, 650), text(45, 479, "bounded sublevel set can certify a region", 15, 650), text(45, 507, "if solutions remain forward complete。", 15, fill=MUTED)]

    heading(out, 430, "B", "导数强度决定结论强度", TEAL)
    ladder = (("V>0, Vdot<=0", "stable", BLUE), ("Vdot<0", "asymptotic stability", TEAL), ("Vdot<=-alpha V", "exponential rate", RED))
    for i, (condition, claim, color) in enumerate(ladder):
        yy = 98 + i * 90
        node(out, 445, yy, 190, 55, condition, color, size=14)
        out += [line(638, yy + 28, 662, yy + 28, INK, 2, marker="a3"), text(675, yy + 34, claim, 13, 650)]
    out += [line(430, 380, 765, 380, GRID, 2), text(430, 414, "if Vdot<=0 only:", 15, 700, fill=RED), text(430, 444, "find largest invariant set in {Vdot=0}", 15, 650), text(430, 476, "LaSalle can prove attraction beyond strict decay", 15, 650), text(430, 506, "but compactness/invariance are hypotheses。", 15, fill=MUTED)]

    heading(out, 830, "C", "三种证书验证不同对象", RED)
    certs = (("continuous ODE", "L_f V(x)<=0 on D", BLUE), ("discrete map", "V(F_h(x))-V(x)<=0", TEAL), ("learned V_theta", "verify domain + counterexamples", RED))
    for i, (name, test, color) in enumerate(certs):
        yy = 105 + i * 115
        out += [text(830, yy, name, 16, 700, fill=color), text(830, yy + 32, test, 15, 650)]
        if i < 2:
            out.append(line(830, yy + 58, 1145, yy + 58, GRID, 2))
    out += [text(830, 456, "sampled training loss is not a proof", 15, 700, fill=RED), text(830, 486, "state local/regional/global and robustness", 15, 650), text(830, 514, "continuous decay need not survive a stepper。", 15, fill=MUTED)]
    return finish(out, "Lyapunov 证书的力量来自量词与不变集，而不来自一条下降曲线；连续、离散和学习验证必须分层。")


FIGURES = {
    "fig-ode-ivp-wellposedness-v2.svg": ode_ivp,
    "fig-linear-ode-propagation-v2.svg": linear_ode,
    "fig-phase-portrait-local-stability-v2.svg": phase_portrait,
    "fig-lyapunov-energy-certificate-v2.svg": lyapunov,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
