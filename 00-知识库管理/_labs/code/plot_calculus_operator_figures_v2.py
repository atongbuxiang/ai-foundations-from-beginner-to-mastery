#!/usr/bin/env python3
"""Generate the operator-oriented v2 figures for calculus chapter 10.4.

The figures share a restrained textbook visual language but keep topic-specific
geometry.  They use only the Python standard library and deterministic data.
"""

from __future__ import annotations

import html
from fractions import Fraction
from pathlib import Path


W, H = 1200, 600
BG = "#FFFEFB"
INK = "#1F2937"
MUTED = "#64748B"
GRID = "#D7DEE8"
BLUE = "#2563EB"
TEAL = "#0F766E"
AMBER = "#B7791F"
RED = "#C24135"


def esc(value: object) -> str:
    return html.escape(str(value))


def text(x, y, value, size=17, weight=400, anchor="start", fill=INK, cls=""):
    klass = f' class="{cls}"' if cls else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{max(15, size)}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}"{klass}>{esc(value)}</text>'
    )


def line(x1, y1, x2, y2, color=GRID, width=2, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}{m}/>'


def path(d, color=INK, width=2.5, fill="none", dash=None, marker=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    ma = f' marker-end="url(#{marker})"' if marker else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"{da}{ma}/>'


def rect(x, y, w, h, stroke=INK, fill="none", radius=8, width=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def circle(x, y, r, stroke=INK, fill=BG, width=2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def arrow_defs(colors=(BLUE, TEAL, AMBER, RED, INK)):
    out = ["<defs>"]
    for i, color in enumerate(colors):
        out.append(
            f'<marker id="a{i}" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
            f'<path d="M0 0L9 4.5L0 9Z" fill="{color}"/></marker>'
        )
    out.append('<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.math{font-family:STIX Two Text,"Times New Roman",serif}</style>')
    out.append("</defs>")
    return "".join(out)


def begin(title, desc, colors=(BLUE, TEAL, AMBER)):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(desc)}</desc>',
        arrow_defs(colors + (INK,)),
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        line(400, 36, 400, 520, GRID, 2),
        line(800, 36, 800, 520, GRID, 2),
    ]


def heading(out, x, label, title, color):
    out.append(text(x, 58, label, 24, 700, fill=color))
    out.append(text(x + 38, 58, title, 22, 700))


def finish(out, conclusion):
    out.append(line(60, 535, 1140, 535, GRID, 2))
    out.append(text(600, 570, conclusion, 18, 650, "middle"))
    out.append("</svg>")
    return "\n".join(out)


def node(out, x, y, w, h, label, color=BLUE, fill=BG, size=17):
    out.append(rect(x, y, w, h, color, fill, 8, 2))
    out.append(text(x + w / 2, y + h / 2 + 6, label, size, 650, "middle", color))


def chain_rule():
    out = begin("链式法则、计算图与深层 Jacobian", "函数复合对应导数算子复合；JVP 前推、VJP 回拉并在分支处累加；深层乘积与残差支路有不同传播结构。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "复合 = 局部算子依次作用", BLUE)
    for x, lab in ((55, "X"), (165, "Y"), (275, "Z")):
        node(out, x, 105, 72, 50, lab, BLUE if lab == "X" else TEAL)
    out += [line(128, 130, 160, 130, INK, 2.5, marker="a3"), line(238, 130, 270, 130, INK, 2.5, marker="a3")]
    out += [text(144, 112, "f", 17, 650, "middle"), text(254, 112, "g", 17, 650, "middle")]
    for x, lab in ((55, "v"), (165, "Df(x)v"), (275, "Dg(y)Df(x)v")):
        node(out, x, 220, 72 if x < 200 else 100, 54, lab, TEAL, size=15)
    out += [line(128, 247, 160, 247, TEAL, 3, marker="a1"), line(238, 247, 270, 247, TEAL, 3, marker="a1")]
    out += [text(45, 335, "D(g o f)(x) = Dg(f(x)) o Df(x)", 18, 650, cls="math"), text(45, 371, "坐标：J_(gof) = J_g J_f；右侧先作用", 16, fill=MUTED)]

    heading(out, 430, "B", "分支：前推，回拉时相加", TEAL)
    pts = {"x": (470, 245), "a": (575, 155), "b": (575, 335), "c": (690, 245), "L": (755, 245)}
    for k, (x, y) in pts.items():
        out.append(circle(x, y, 24, BLUE if k == "x" else TEAL if k in "ab" else RED, BG, 2.5)); out.append(text(x, y + 6, k, 17, 700, "middle"))
    for a, b in (("x", "a"), ("x", "b"), ("a", "c"), ("b", "c"), ("c", "L")):
        x1,y1=pts[a]; x2,y2=pts[b]; out.append(line(x1+22,y1,x2-25,y2,INK,2.4,marker="a3"))
    out += [path("M550 177L493 230", RED, 2.5, "none", "7 5", "a2"), path("M550 313L493 260", RED, 2.5, "none", "7 5", "a2")]
    out += [text(435, 410, "fan-out 后：x_bar = x_bar^(a) + x_bar^(b)", 17, 650), text(435, 444, "反向箭头表示对偶回拉，不表示求逆。", 16, fill=MUTED)]

    heading(out, 830, "C", "深层乘积与残差通道", RED)
    for i, lab in enumerate(("J1", "J2", "J3", "...", "JL")):
        x=830+i*66; node(out,x,112,48,44,lab,BLUE,size=15)
        if i<4: out.append(line(x+49,134,x+63,134,INK,2,marker="a3"))
    out += [text(830, 205, "||JL ... J1|| <= product ||Jl||", 17, 650, cls="math"), text(830, 240, "连续收缩 -> 可能消失", 17, fill=TEAL), text(830, 272, "连续放大 -> 可能爆炸", 17, fill=RED)]
    node(out, 830, 330, 132, 55, "x + F(x)", TEAL)
    out += [line(968,357,1020,357,TEAL,3,marker="a1"), text(1035, 363, "J = I + JF", 18, 700), text(830, 430, "恒等支路提供直接通道；仍不保证全局稳定。", 16, fill=MUTED)]
    return finish(out, "链式法则决定局部算子如何复合；计算图只是在复用这些作用与累加。")


def matrix_calculus():
    out=begin("矩阵微分、迹技巧与布局", "从矩阵方向上的线性泛函，经 Frobenius 配对得到梯度；迹循环只用于隔离 dX；矩阵输出优先保留为 JVP/VJP 算子。", (BLUE, TEAL, AMBER))
    heading(out,42,"A","微分先于梯度",BLUE)
    node(out,55,105,290,62,"Df(X): E -> scalar",BLUE)
    out += [line(200,170,200,205,BLUE,3,marker="a0")]
    node(out,55,215,290,78,"df = <G,dX>_F = tr(G^T dX)",TEAL,size=16)
    out += [line(200,297,200,330,TEAL,3,marker="a1")]
    node(out,55,342,290,62,"gradient_X f = G",BLUE)
    out += [text(55,455,"形状：G 与 X 相同；内积固定坐标表示。",16,fill=MUTED)]

    heading(out,430,"B","迹循环只为隔离 dX",TEAL)
    for y,lab,col in ((112,"df = tr(A dX B)",AMBER),(225,"= tr(B A dX)",TEAL),(338,"gradient_X f = (BA)^T",BLUE)):
        node(out,445,y,310,64,lab,col,size=17)
    out += [line(600,180,600,218,INK,2.5,marker="a3"),line(600,293,600,331,INK,2.5,marker="a3")]
    out += [text(440,447,"允许 tr(ABC)=tr(BCA)；禁止任意交换 B、C。",16,fill=MUTED)]

    heading(out,830,"C","矩阵输出保留为算子",AMBER)
    node(out,850,105,280,56,"F(X)=A X B",BLUE)
    out += [line(990,165,990,200,INK,2.5,marker="a3")]
    node(out,830,215,145,76,"JVP: A dX B",TEAL,size=16); node(out,1000,215,145,76,"VJP: A^T Ybar B^T",AMBER,size=15)
    out += [text(830,345,"完整 Jacobian 依赖 vec 布局，可能是四阶数组。",16,fill=MUTED),text(830,385,"实际计算优先请求作用，而不是物化坐标表。",17,650)]
    return finish(out,"矩阵求导的可靠顺序：先写线性微分，再用内积读梯度，最后选择 JVP 或 VJP。")


def implicit_diff():
    out=begin("线性求解与隐式微分", "隐式方程先线性化，再通过切向或伴随线性求解得到导数；可信度同时受存在唯一、残差、条件数与反向残差控制。", (BLUE, TEAL, RED))
    heading(out,42,"A","由方程定义输出",TEAL)
    node(out,60,105,280,58,"F(z(theta), theta)=0",TEAL)
    out += [line(200,168,200,205,INK,2.5,marker="a3")]
    node(out,48,218,304,76,"DzF zdot + DthetaF thetadot = 0",BLUE,size=16)
    out += [line(200,298,200,335,INK,2.5,marker="a3")]
    node(out,48,348,304,70,"solve DzF zdot = -DthetaF thetadot",TEAL,size=16)
    out += [text(48,460,"可逆性保证局部唯一分支，也控制敏感性。",16,fill=MUTED)]

    heading(out,430,"B","Ax=b 的三次求解",BLUE)
    for y,lab,col in ((108,"forward: solve A x = b",TEAL),(225,"JVP: solve A xdot = bdot - Adot x",BLUE),(342,"VJP: solve A^T lambda = xbar",RED)):
        node(out,438,y,324,68,lab,col,size=16)
    out += [line(600,180,600,218,INK,2.5,marker="a3"),line(600,297,600,335,INK,2.5,marker="a3"),text(438,454,"返回 bbar=lambda, Abar=-lambda x^T；不形成 inverse。",16,fill=MUTED)]

    heading(out,830,"C","梯度可信度是一条链",RED)
    items=(("1  局部解存在且唯一",TEAL),("2  前向残差足够小",BLUE),("3  Jacobian 条件性可接受",RED),("4  伴随残差进入误差预算",TEAL))
    for i,(lab,col) in enumerate(items):
        y=105+i*92; node(out,840,y,300,55,lab,col,size=16)
        if i<3: out.append(line(990,y+58,990,y+85,INK,2,marker="a3"))
    return finish(out,"隐式梯度不是一个公式开关：前向问题、线性化与伴随求解必须一起验收。")


def logdet():
    out=begin("行列式、log-det 与迹的导数", "行列式描述局部体积；trace 给出 log-det 的一阶相对变化；数值上通过分解计算并在 Gaussian 与 flow 中调用。", (BLUE, TEAL, RED))
    heading(out,42,"A","体积与 Jacobi 公式",BLUE)
    out += [path("M75 165L225 125L325 175L175 220Z",BLUE,3,"#EFF6FF"),path("M75 165V305L175 355V220M175 355L325 310V175",BLUE,3)]
    out += [text(200,395,"volume scale = |det A|",18,650,"middle"),text(45,448,"d log|det A| = tr(A^-1 dA)",17,650,cls="math")]

    heading(out,430,"B","稳定计算来自分解",TEAL)
    node(out,445,108,310,64,"SPD: A=L L^T; logdet=2 sum log Lii",TEAL,size=16)
    out += [line(600,176,600,213,INK,2.5,marker="a3")]
    node(out,445,225,310,64,"general: P A=L U; sign + sum log|Uii|",BLUE,size=15)
    out += [line(600,293,600,330,INK,2.5,marker="a3")]
    node(out,445,342,310,64,"Do not form det and then take log",RED,size=16)
    out += [text(445,451,"inverse action也通过 solve 获得。",16,fill=MUTED)]

    heading(out,830,"C","概率模型中的两类调用",RED)
    out += [text(835,125,"Gaussian",19,700,fill=BLUE),text(835,160,"1/2 log det Sigma + 1/2 r^T Sigma^-1 r",16,cls="math"),text(835,205,"Normalizing flow",19,700,fill=TEAL),text(835,240,"log p_X = log p_Z + log|det J_f|",16,cls="math")]
    node(out,835,300,310,70,"sigma_min -> 0: logdet -> -infinity; gradient grows",RED,size=15)
    out += [text(835,410,"结构化三角 Jacobian 降低计算成本。",16,fill=MUTED)]
    return finish(out,"先分清体积、符号与可逆性，再在对数域计算；接近奇异时必须报告条件性。")


def solve_logdet_bridge():
    out = begin(
        "求解—log-det 计算图的三种一致导数",
        "同一个二维 SPD 算例中，primal 计算、JVP 前推与 VJP 回拉都给出 dL/dtheta=-1/27；求解与 log-det 两条分支在共享矩阵处累加。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一张图，两条分支", BLUE)
    node(out, 58, 95, 72, 48, "theta", BLUE, size=16)
    node(out, 185, 95, 150, 48, "A(theta)", BLUE, size=16)
    out.append(line(132, 119, 180, 119, BLUE, 3, marker="a0"))
    node(out, 48, 215, 145, 58, "solve A x=b", TEAL, size=15)
    node(out, 220, 215, 145, 58, "1/2 logdet A", RED, size=15)
    out += [
        path("M235 145C205 165 165 180 125 210", TEAL, 2.5, marker="a1"),
        path("M285 145C305 165 315 180 300 210", RED, 2.5, marker="a2"),
    ]
    node(out, 48, 325, 145, 54, "q=1/2 ||x||^2", TEAL, size=15)
    node(out, 220, 325, 145, 54, "r", RED, size=16)
    out += [
        line(120, 275, 120, 320, TEAL, 2.5, marker="a1"),
        line(292, 275, 292, 320, RED, 2.5, marker="a2"),
        path("M120 382C145 410 168 420 198 438", TEAL, 2.5, marker="a1"),
        path("M292 382C270 410 245 420 215 438", RED, 2.5, marker="a2"),
    ]
    node(out, 165, 440, 90, 48, "L=q+r", BLUE, size=16)

    heading(out, 430, "B", "JVP：切向量前推", TEAL)
    node(out, 445, 98, 310, 58, "A0=[[2,1],[1,2]],  x0=(2/3,-1/3)", BLUE, size=15)
    node(out, 445, 210, 310, 64, "xdot=(-4/9, 2/9)", TEAL, size=17)
    node(out, 445, 330, 145, 64, "qdot=-10/27", TEAL, size=16)
    node(out, 610, 330, 145, 64, "rdot=+9/27", RED, size=16)
    out += [
        line(600, 160, 600, 204, INK, 2.5, marker="a3"),
        path("M600 278C560 298 535 310 520 324", TEAL, 2.5, marker="a1"),
        path("M600 278C640 298 665 310 680 324", RED, 2.5, marker="a2"),
        text(600, 460, "Ldot = -10/27 + 9/27 = -1/27", 18, 700, "middle"),
    ]

    heading(out, 830, "C", "VJP：贡献回拉并相加", RED)
    node(out, 845, 100, 285, 58, "solve A0^T lambda = x0", TEAL, size=16)
    node(out, 845, 210, 285, 62, "Abar_solve = -lambda x0^T", TEAL, size=15)
    node(out, 845, 320, 285, 62, "Abar_logdet = 1/2 A0^-T", RED, size=15)
    out += [
        line(988, 162, 988, 204, TEAL, 2.5, marker="a1"),
        path("M900 386C900 420 930 432 970 448", TEAL, 2.5, marker="a1"),
        path("M1070 386C1070 420 1040 432 1000 448", RED, 2.5, marker="a2"),
        text(990, 482, "<Abar,E11> = -1/27", 18, 700, "middle"),
    ]
    return finish(
        out,
        "直接求导 = JVP = VJP 配对；三条证据一致后，局部公式才算闭合。",
    )


def spectral_flow_ad_bridge():
    out = begin(
        "谱坐标、可逆换元与自动微分的对象边界",
        "旋转伸缩族在谱碰撞时失去唯一特征基，但底层线性映射仍可逆，Gaussian 换元与直接程序的前反向导数保持良好。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "谱坐标：先声明对象", BLUE)
    node(out, 48, 96, 305, 56, "T_t = R_t diag(2 exp(t), 1)", BLUE, size=15)
    node(out, 48, 205, 305, 60, "A_t = T_t T_t^T", TEAL, size=17)
    out.append(line(200, 156, 200, 199, INK, 2.5, marker="a3"))
    node(out, 48, 322, 145, 72, "gap=3; l1'=8", TEAL, size=15)
    node(out, 213, 322, 140, 72, "t*=-log2; A*=I", RED, size=15)
    out += [
        path("M165 269C135 286 120 300 118 316", TEAL, 2.5, marker="a1"),
        path("M235 269C265 286 280 300 282 316", RED, 2.5, marker="a2"),
        text(48, 455, "重谱：basis 不唯一；T_t* 仍为正交矩阵。", 16, 650),
    ]

    heading(out, 430, "B", "可逆换元：质量守恒", TEAL)
    node(out, 445, 98, 130, 54, "z ~ N(0,I)", BLUE, size=16)
    node(out, 625, 98, 130, 54, "x = T_t z", TEAL, size=16)
    out.append(line(578, 125, 620, 125, TEAL, 3, marker="a1"))
    node(out, 445, 210, 310, 64, "det T_t = 2 exp(t) > 0", TEAL, size=17)
    node(out, 445, 328, 310, 68, "p_X = p_Z(T_t^-1 x) / |det T_t|", BLUE, size=15)
    out += [
        line(600, 158, 600, 204, INK, 2.5, marker="a3"),
        line(600, 278, 600, 322, INK, 2.5, marker="a3"),
        text(600, 458, "x*=(1,2):  NLL'(0) = -3/4", 17, 700, "middle"),
    ]

    heading(out, 830, "C", "AD：对程序而非意图求导", RED)
    node(out, 842, 96, 292, 58, "sin, cos, exp, arithmetic", BLUE, size=16)
    node(out, 842, 210, 135, 64, "JVP = -3/4", TEAL, size=16)
    node(out, 999, 210, 135, 64, "VJP = -3/4", TEAL, size=16)
    out += [
        path("M988 158C930 178 915 190 910 204", TEAL, 2.5, marker="a1"),
        path("M988 158C1045 178 1060 190 1065 204", TEAL, 2.5, marker="a1"),
    ]
    out.append(rect(842, 332, 292, 72, RED, BG, 8, 2))
    out.append(text(988, 361, "repeated-spectrum eigenbasis", 15, 650, "middle", RED))
    out.append(text(988, 386, "gradient rule may fail", 15, 650, "middle", RED))
    out += [
        text(842, 456, "函数可微，不保证任意中间表示可微。", 16, 650, fill=MUTED),
    ]
    return finish(
        out,
        "先定位失效对象：谱基退化、Jacobian 奇异与程序规则错误是三类不同问题。",
    )


def validate_solve_logdet_example():
    """Exact arithmetic gate for the shared CALC-09—12 example."""
    x = (Fraction(2, 3), Fraction(-1, 3))
    x_dot = (Fraction(-4, 9), Fraction(2, 9))
    q_dot = x[0] * x_dot[0] + x[1] * x_dot[1]
    r_dot = Fraction(1, 3)
    total = q_dot + r_dot

    lam = (Fraction(5, 9), Fraction(-4, 9))
    solve_e11 = -lam[0] * x[0]
    logdet_e11 = Fraction(1, 3)
    reverse_total = solve_e11 + logdet_e11

    assert q_dot == Fraction(-10, 27)
    assert total == Fraction(-1, 27)
    assert reverse_total == total
    assert Fraction(-10, 27) + Fraction(1, 3) == total
    print("CALC-09—12 exact gate: direct = JVP = VJP = -1/27")


def validate_spectral_flow_ad_example():
    """Exact arithmetic gate for the shared CALC-13—16 example at tau=0."""
    a_dot = (
        (Fraction(8), Fraction(3)),
        (Fraction(3), Fraction(0)),
    )
    lambda1_dot = a_dot[0][0]
    u1_dot_coefficient = a_dot[1][0] / Fraction(4 - 1)

    z = (Fraction(1, 2), Fraction(2))
    z_dot = (Fraction(1, 2), Fraction(-1))
    nll_dot = z[0] * z_dot[0] + z[1] * z_dot[1] + Fraction(1)

    bar_a = Fraction(1, 4)
    bar_c = Fraction(17, 4)
    bar_s = Fraction(-3, 2)
    reverse_dot = Fraction(1) - bar_a + bar_c * Fraction(0) + bar_s

    assert lambda1_dot == Fraction(8)
    assert u1_dot_coefficient == Fraction(1)
    assert nll_dot == Fraction(-3, 4)
    assert reverse_dot == nll_dot
    print("CALC-13—16 exact gate: spectral + change-of-variables + JVP/VJP passed")


def spectral():
    out=begin("特征值、特征向量与 SVD 的导数", "简单谱下标量导数稳定；向量导数含谱间隙分母；重谱时基不唯一，应改比较投影和子空间。", (BLUE, TEAL, RED))
    heading(out,42,"A","简单特征值与 gap",BLUE)
    node(out,52,105,300,58,"A u_i = lambda_i u_i",BLUE)
    out += [text(55,205,"d lambda_i = u_i^T (dA) u_i",17,650,cls="math"),text(55,250,"du_i contains 1/(lambda_i-lambda_j)",17,650,fill=RED,cls="math")]
    out += [line(90,335,310,335,GRID,2),circle(135,335,8,BLUE,BLUE),circle(255,335,8,TEAL,TEAL),line(135,310,135,360,BLUE,2),line(255,310,255,360,TEAL,2),text(195,300,"gap",18,700,"middle")]
    out += [text(52,418,"gap 小：方向敏感；标量谱值仍可能较稳定。",16,fill=MUTED)]

    heading(out,430,"B","重复谱：改用子空间",TEAL)
    out += [circle(535,245,95,TEAL,"#ECFDF5",2.5),line(535,245,475,170,TEAL,3),line(535,245,610,190,TEAL,3),text(535,372,"同一子空间内，基可任意旋转",16,650,"middle")]
    out += [line(645,245,695,245,INK,2.5,marker="a3"),node(out,710,190,60,110,"P=UU^T",BLUE,size=16) if False else ""]
    node(out,685,190,85,110,"P = U U^T",BLUE,size=15)
    out += [text(430,430,"比较投影距离或主角，不逐列比较向量。",16,fill=MUTED)]

    heading(out,830,"C","SVD 的两类退化",RED)
    node(out,845,105,285,56,"A = U Sigma V^T",BLUE)
    out += [text(845,205,"d sigma_i = u_i^T (dA) v_i",17,650,cls="math"),text(845,255,"方向分母: sigma_i^2 - sigma_j^2",17,650,fill=RED),text(845,300,"补空间分母: sigma_i",17,650,fill=RED)]
    out += [text(845,365,"碰撞、零值、秩变化必须分层处理。",17,700),text(845,410,"符号、排列与内部旋转也要纳入审计。",16,fill=MUTED)]
    return finish(out,"谱值、单个方向与不变子空间是不同输出对象；先声明对象，再选择可微结论。")


def inverse_implicit():
    out=begin("逆函数定理与隐函数定理", "可逆线性化生成局部逆或唯一隐式分支；定量稳定、全局可逆与数值求解仍是不同层次。", (BLUE, TEAL, RED))
    heading(out,42,"A","局部逆来自可逆线性化",TEAL)
    out += [circle(120,220,78,TEAL,"#ECFDF5",2.5),circle(300,220,68,BLUE,"#EFF6FF",2.5),path("M100 250C125 190 145 270 175 175",TEAL,3),line(200,220,230,220,INK,2.5,marker="a3")]
    out += [text(120,330,"a 附近",16,650,"middle"),text(300,310,"f(a) 附近",16,650,"middle"),text(45,405,"D(f^-1)(f(a)) = Df(a)^-1",17,650,cls="math")]

    heading(out,430,"B","零水平集成为函数图像",BLUE)
    out += [line(450,390,750,390,GRID,2),line(480,420,480,115,GRID,2),path("M480 345C540 325 570 210 650 240C700 260 720 185 755 150",TEAL,4),circle(650,240,7,TEAL,TEAL)]
    out += [text(660,226,"(x,g(x))",15,fill=MUTED),text(445,445,"DyF 可逆 => Dg = -(DyF)^-1 DxF",16,650,cls="math")]

    heading(out,830,"C","四个层次必须分开",RED)
    items=(("局部存在唯一：Jacobian 可逆",TEAL),("定量稳定：sigma_min 不太小",BLUE),("全局可逆：需要额外结构",RED),("数值求解：分支、残差与吸引域",TEAL))
    for i,(lab,col) in enumerate(items): node(out,840,105+i*88,300,56,lab,col,size=16)
    return finish(out,"逆/隐函数定理给出精确的局部结构；它不自动提供全局双射或数值算法保证。")


def change_variables():
    out=begin("多重积分与换元公式", "多重积分是局部体积加权和；Jacobian determinant 负责局部体积换算；概率密度按同一质量守恒重新计价。", (BLUE, TEAL, RED))
    heading(out,42,"A","积分是小体积加权和",BLUE)
    for i in range(8): out.append(line(65+i*38,115,65+i*38,365,GRID,1.5))
    for j in range(7): out.append(line(65,115+j*38,331,115+j*38,GRID,1.5))
    out += [path("M66 315C105 250 160 275 205 205C245 145 290 170 331 220L331 365L66 365Z",BLUE,3,"#EFF6FF"),text(198,425,"integral ≈ sum f(xi_k) Delta V_k",16,650,"middle",cls="math")]

    heading(out,430,"B","Jacobian 负责局部体积",TEAL)
    out += [path("M455 145H565V285H455Z",BLUE,3,"#EFF6FF"),line(585,220,645,220,INK,2.5,marker="a3"),path("M675 135L765 165L735 315L645 285Z",TEAL,3,"#ECFDF5")]
    out += [text(510,335,"du",16,650,"middle"),text(705,335,"dx",16,650,"middle"),text(600,392,"dx = |det DT(u)| du",17,650,"middle",cls="math"),text(430,440,"det=0 表示局部体积塌缩。",16,fill=MUTED)]

    heading(out,830,"C","概率密度与非单射",RED)
    out += [text(835,130,"生成方向 y=T(x):",17,700,fill=TEAL),text(835,170,"p_Y(y)=p_X(x)/|det DT(x)|",16,cls="math"),text(835,230,"编码方向 z=f(x):",17,700,fill=BLUE),text(835,270,"log p_X=log p_Z+log|det J_f|",16,cls="math")]
    node(out,835,330,310,70,"non-injective: sum over all preimages",RED,size=15)
    return finish(out,"换元公式是质量守恒的局部计价规则；双射、支持集、维数与可积性缺一不可。")


def autodiff():
    out=begin("自动微分的前向、反向与高阶模式", "前向模式推送 tangent，反向模式回拉 cotangent；高阶组合和 checkpoint 在计算与内存之间权衡。", (BLUE, TEAL, AMBER))
    heading(out,42,"A","Forward：tangent 前推",BLUE)
    for x,lab in ((70,"x"),(190,"v=f(x)"),(310,"y=g(v)")): node(out,x,120,72,50,lab,BLUE,size=15)
    out += [line(143,145,185,145,BLUE,3,marker="a0"),line(263,145,305,145,BLUE,3,marker="a0")]
    for x,lab in ((70,"xdot"),(190,"vdot=Jf xdot"),(310,"ydot=Jg vdot")): node(out,x,250,72 if x==70 else 100,52,lab,TEAL,size=15)
    out += [line(143,276,185,276,TEAL,3,marker="a1"),line(291,276,305,276,TEAL,3,marker="a1"),text(45,380,"一次输入 seed -> 一个 Jv",18,700),text(45,420,"适合输入方向少、输出方向多。",16,fill=MUTED)]

    heading(out,430,"B","Reverse：cotangent 回拉",TEAL)
    for x,lab in ((450,"x"),(570,"v"),(690,"L")): node(out,x,120,70,50,lab,BLUE,size=16)
    out += [line(521,145,565,145,BLUE,3,marker="a0"),line(641,145,685,145,BLUE,3,marker="a0"),line(685,275,642,275,TEAL,3,marker="a1"),line(565,275,522,275,TEAL,3,marker="a1")]
    out += [text(690,260,"seed Lbar=1",16,650,"middle"),text(570,310,"xbar = Jf^T Jg^T",16,650,"middle"),text(430,380,"一个输出 seed -> 一个 J^T u",18,700),text(430,420,"适合标量损失对海量参数求梯度。",16,fill=MUTED)]

    heading(out,830,"C","高阶组合与内存权衡",AMBER)
    node(out,840,105,300,70,"forward-over-reverse: H v",TEAL,size=16)
    node(out,840,215,300,70,"checkpoint: memory down; FLOPs up",AMBER,size=15)
    node(out,840,325,300,70,"custom VJP / implicit: audit high order",BLUE,size=15)
    out += [text(840,445,"AD 求程序导数；控制流、状态和随机性必须先定义。",16,fill=MUTED)]
    return finish(out,"模式选择由输入/输出方向数、内存和所需导数作用决定，而不是由 API 名称决定。")


BUILDERS = {
    "chain-rule/fig-chain-rule-computational-graph-v2.svg": chain_rule,
    "matrix-calculus/fig-matrix-differential-trace-layout-v2.svg": matrix_calculus,
    "implicit-differentiation/fig-linear-solve-implicit-differentiation-v2.svg": implicit_diff,
    "logdet/fig-determinant-logdet-trace-derivative-v2.svg": logdet,
    "calculus-ad/fig-solve-logdet-chain-v2.svg": solve_logdet_bridge,
    "calculus-ad/fig-spectral-flow-ad-chain-v2.svg": spectral_flow_ad_bridge,
    "spectral-derivatives/fig-eigen-svd-derivatives-v2.svg": spectral,
    "inverse-implicit-theorems/fig-inverse-implicit-function-theorems-v2.svg": inverse_implicit,
    "change-of-variables/fig-multiple-integrals-change-variables-v2.svg": change_variables,
    "autodiff/fig-forward-reverse-higher-order-ad-v2.svg": autodiff,
}


def main():
    validate_solve_logdet_example()
    validate_spectral_flow_ad_example()
    root = Path(__file__).resolve().parents[2] / "_assets" / "figures"
    for relative, builder in BUILDERS.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
