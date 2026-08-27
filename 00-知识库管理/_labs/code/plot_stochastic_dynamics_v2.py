#!/usr/bin/env python3
"""Generate v2 textbook figures for DYN-09--12 stochastic dynamics."""

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


def brownian():
    out = begin(
        "Brownian 时间耦合、粗糙尺度与二次变差",
        "Brownian motion 是具有平稳独立增量和连续路径的整条随机函数，不是逐时独立 Gaussian；增量按平方根时间缩放使普通导数爆炸，而平方增量和收敛到时间长度，产生 Itô 微积分的二阶项。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "marginals 不决定 process", BLUE)
    out += [line(55, 360, 365, 360, GRID, 2), line(75, 400, 75, 95, GRID, 2)]
    out += [path("M75 320 C120 260 150 305 190 225 C240 135 300 245 360 145", BLUE, 2.8), path("M75 255 C130 330 170 190 220 270 C275 350 310 115 360 205", TEAL, 2.4)]
    for x in (130, 210, 290, 350):
        out.append(line(x, 110, x, 365, GRID, 1, "4 5"))
    out += [text(45, 410, "W_t-W_s ~ N(0,t-s)", 16, 700, cls="math"), text(45, 444, "disjoint increments are independent", 15, 650), text(45, 475, "Cov(W_s,W_t)=min(s,t)", 15, 650), text(45, 506, "pointwise histograms miss temporal coupling。", 15, fill=MUTED)]

    heading(out, 430, "B", "sqrt(dt) 尺度摧毁普通导数", TEAL)
    out += [line(450, 350, 770, 350, GRID, 2), line(470, 390, 470, 100, GRID, 2)]
    hs = ((520, 125, BLUE, "dt"), (610, 215, TEAL, "dt/4"), (700, 280, RED, "dt/16"))
    for x, y, color, label in hs:
        out += [line(x, 350, x, y, color, 18), text(x, y - 14, label, 14, 650, "middle", fill=color)]
    out += [text(430, 410, "Delta W=O_P(sqrt(Delta t))", 16, 700, cls="math"), text(430, 444, "Delta W/Delta t=O_P(Delta t^(-1/2))", 15, 650, cls="math"), text(430, 478, "paths are continuous but a.s. nowhere smooth", 15, 650), text(430, 508, "white noise is a generalized derivative。", 15, fill=MUTED)]

    heading(out, 830, "C", "平方增量和留下有限极限", RED)
    node(out, 840, 92, 300, 60, "partition Pi: 0=t0<...<tn=T", BLUE, size=14)
    out += [line(990, 155, 990, 192, INK, 2.2, marker="a3")]
    node(out, 840, 204, 300, 70, "QV_Pi=sum (Delta W_i)^2", TEAL, size=14)
    out += [line(990, 277, 990, 314, INK, 2.2, marker="a3")]
    node(out, 840, 326, 300, 65, "mesh ->0: QV_Pi -> T", RED, size=15)
    out += [text(830, 430, "finite-variation continuous paths: QV=0", 14, 650), text(830, 460, "Brownian total variation diverges", 14, 650, fill=RED), text(830, 490, "(dW)^2=dt is asymptotic bookkeeping", 14, 650), text(830, 517, "not ordinary differential algebra。", 15, fill=MUTED)]
    return finish(out, "Brownian 的核心是整条路径 law：平方根增量尺度使导数失效，二次变差则保存为 Itô 二阶修正。")


def ito_sde():
    out = begin(
        "Itô 积分构造、二阶链式法则与 SDE 数值合同",
        "Itô integral 由适应左端点随机和与 L2 等距闭包定义；Brownian 二次变差使 Taylor 二阶项保留并形成 Itô formula；SDE 必须解释为积分方程，数值方法还要区分 strong、weak 与离散梯度目标。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "适应左端点和定义随机积分", BLUE)
    out += [line(55, 320, 365, 320, GRID, 2)]
    for i, h in enumerate((70, 125, 90, 155, 110)):
        x = 65 + i * 58
        out += [rect(x, 320 - h, 48, h, BLUE, BG, 0, 2), line(x + 48, 320 - h, x + 58, 320 - h, GRID, 1)]
    out += [text(45, 105, "H_{t_i} known before Delta W_i", 15, 700, fill=BLUE), text(45, 365, "sum H_(t_i)(W_(t_i+1)-W_(t_i))", 14, 650, cls="math"), text(45, 405, "E integral H dW =0", 15, 650), text(45, 438, "E|integral H dW|^2=E integral |H|^2 dt", 14, 650), text(45, 478, "isometry extends simple processes in L2", 15, 650), text(45, 508, "anticipating integrands need other theories。", 15, fill=MUTED)]

    heading(out, 430, "B", "二次变差保留 Taylor 二阶项", TEAL)
    node(out, 445, 92, 310, 58, "Delta X=a dt+b dW", BLUE, size=15)
    out += [line(600, 153, 600, 190, INK, 2.2, marker="a3")]
    node(out, 445, 202, 310, 70, "(Delta X)^2=b^2 dt + smaller terms", TEAL, size=14)
    out += [line(600, 275, 600, 312, INK, 2.2, marker="a3")]
    out += [rect(445, 324, 310, 75, RED, BG, 10, 2), text(600, 354, "df=(f_t+a f_x+1/2 b^2 f_xx)dt", 12.5, 650, "middle", fill=RED), text(600, 380, "+ b f_x dW", 13, 650, "middle", fill=RED)]
    out += [text(430, 440, "the 1/2 b^2 f_xx term is structural", 15, 700, fill=RED), text(430, 473, "Ito vs Stratonovich changes the drift", 15, 650), text(430, 505, "do not use an ordinary chain rule。", 15, fill=MUTED)]

    heading(out, 830, "C", "SDE 结果要按对象分层验收", RED)
    stages = (("integral equation + filtration", BLUE), ("existence / pathwise uniqueness", TEAL), ("coupled-path EM / Milstein", RED), ("strong / weak / gradient diagnostics", BLUE))
    for i, (label, color) in enumerate(stages):
        yy = 88 + i * 92
        node(out, 840, yy, 300, 56, label, color, size=14)
        if i < 3:
            out.append(line(990, yy + 59, 990, yy + 85, INK, 2.1, marker="a3"))
    out += [text(830, 470, "Delta W~N(0,h), not fixed-variance noise", 14, 650, fill=RED), text(830, 500, "finite difference validates the same J_h。", 15, fill=MUTED)]
    return finish(out, "Itô calculus由 adapted random sums 与 quadratic variation 建立；SDE 求解器的路径、分布与梯度误差必须分账。")


def fokker_planck():
    out = begin(
        "Generator–adjoint、概率通量与同边缘概率流",
        "Itô generator 作用在 test functions 上，分部积分把其导数转移到 density 得到 Fokker–Planck；将二阶扩散项写进 probability current 可构造 deterministic probability-flow velocity；同一时刻 marginals 相同不代表 path law 相同。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "从 test functions 转到 density", BLUE)
    node(out, 45, 92, 315, 58, "Ito formula -> generator L_t", BLUE, size=15)
    out += [line(202, 153, 202, 190, INK, 2.2, marker="a3")]
    node(out, 45, 202, 315, 70, "d/dt E phi(X_t)=E[L_t phi(X_t)]", TEAL, size=13)
    out += [line(202, 275, 202, 312, INK, 2.2, marker="a3")]
    node(out, 45, 324, 315, 72, "partial_t p=L_t^* p", RED, size=15)
    out += [text(45, 432, "L phi=a dot grad phi+1/2 D:Hess phi", 13, 650), text(45, 462, "L* p=-div(ap)+1/2 partial_ij(D_ij p)", 13, 650), text(45, 495, "boundary terms define the PDE contract。", 15, fill=MUTED)]

    heading(out, 430, "B", "扩散通量可改写为确定性速度", TEAL)
    node(out, 445, 92, 310, 62, "partial_t p=-div J", BLUE, size=15)
    out += [line(600, 157, 600, 194, INK, 2.2, marker="a3")]
    node(out, 445, 206, 310, 75, "J=a p-1/2 div(D p)", TEAL, size=14)
    out += [line(600, 284, 600, 321, INK, 2.2, marker="a3")]
    node(out, 445, 333, 310, 72, "v=J/p=a-[div(Dp)]/(2p)", RED, size=13)
    out += [text(430, 445, "if D=g(t)^2 I: v=a-1/2 g^2 score", 14, 650), text(430, 478, "state-dependent D needs div D correction", 14, 650, fill=RED), text(430, 507, "velocity is defined where p>0。", 15, fill=MUTED)]

    heading(out, 830, "C", "同 marginal，不同路径律", RED)
    out += [text(830, 100, "SDE particles", 16, 700, fill=BLUE), path("M835 145 C900 90 920 235 985 170 C1040 110 1085 245 1140 150", BLUE, 2.5), text(830, 210, "nonzero quadratic variation", 14, 650)]
    out += [line(830, 240, 1145, 240, GRID, 2), text(830, 278, "probability-flow ODE", 16, 700, fill=TEAL), path("M835 330 C920 295 1030 305 1140 345", TEAL, 2.5), text(830, 378, "deterministic given x0；zero QV", 14, 650)]
    out += [text(830, 430, "same p_t under exact score/regularity", 14, 700, fill=RED), text(830, 461, "different transitions, coupling and paths", 14, 650), text(830, 491, "separate density, score and solver errors", 14, 650), text(830, 517, "boundary/current conditions still matter。", 14, fill=MUTED)]
    return finish(out, "Fokker–Planck 由 generator 的 adjoint 得到；概率流复现 one-time marginals，却不复现随机路径 law。")


def reverse_diffusion():
    out = begin(
        "Forward noising、反向 score 漂移与生成误差链",
        "前向扩散把数据分布搬向简单先验；时间反演使用各时刻 score 修正反向漂移，reverse SDE 与 probability-flow ODE 的 score 系数不同；精确理论、网络 score、终端先验和有限步求解器是四个误差层。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先定义已知 forward noising", BLUE)
    out += [circle(85, 260, 32, BLUE, BG, 2.5), circle(200, 230, 48, TEAL, BG, 2.5), circle(330, 260, 72, RED, BG, 2.5), line(120, 260, 155, 245, INK, 2.2, marker="a3"), line(250, 242, 275, 252, INK, 2.2, marker="a3")]
    out += [text(55, 345, "p0=data", 16, 700, fill=BLUE), text(160, 345, "p_t", 16, 700, fill=TEAL), text(295, 345, "p_T ~= prior", 16, 700, fill=RED), text(45, 405, "dX=f(t,X)dt+g(t)dW", 15, 650), text(45, 443, "forward conditional law is designed", 15, 650), text(45, 478, "terminal approximation is an error source", 15, 650, fill=RED), text(45, 507, "time index and units must stay explicit。", 15, fill=MUTED)]

    heading(out, 430, "B", "score 决定反向 drift correction", TEAL)
    node(out, 445, 92, 310, 58, "score s_t(x)=grad log p_t(x)", BLUE, size=14)
    out += [line(600, 153, 600, 190, INK, 2.2, marker="a3")]
    node(out, 445, 202, 310, 78, "reverse SDE: -f + g^2 s_t", TEAL, size=14)
    out += [line(600, 283, 600, 320, INK, 2.2, marker="a3")]
    node(out, 445, 332, 310, 72, "PF ODE reverse clock: -f + 1/2 g^2 s_t", RED, size=13)
    out += [text(430, 444, "general D also needs div D", 15, 650, fill=RED), text(430, 475, "reverse filtration is not 'set dt<0'", 15, 650), text(430, 505, "positivity/regularity support the theorem。", 15, fill=MUTED)]

    heading(out, 830, "C", "理论到样本有五道误差门", RED)
    gates = (("terminal prior", BLUE), ("score model", TEAL), ("guidance / parameterization", RED), ("finite-step sampler", BLUE), ("Monte Carlo + evaluation", TEAL))
    for i, (label, color) in enumerate(gates):
        yy = 82 + i * 73
        node(out, 840, yy, 300, 45, label, color, size=14)
        if i < 4:
            out.append(line(990, yy + 48, 990, yy + 67, INK, 1.9, marker="a3"))
    out += [text(830, 469, "exact reverse dynamics assumes exact score", 14, 700, fill=RED), text(830, 497, "smaller step cannot remove score bias", 14, 650), text(830, 520, "sample quality is not likelihood proof。", 14, fill=MUTED)]
    return finish(out, "扩散生成不是把时间符号反过来；score 修正、反向时钟与多层误差合同共同决定最终样本。")


FIGURES = {
    "fig-brownian-process-quadratic-variation-v2.svg": brownian,
    "fig-ito-integral-sde-contract-v2.svg": ito_sde,
    "fig-fokker-planck-probability-flow-v2.svg": fokker_planck,
    "fig-reverse-time-score-diffusion-v2.svg": reverse_diffusion,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
