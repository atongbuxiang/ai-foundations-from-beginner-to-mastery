#!/usr/bin/env python3
"""Generate probability geometry, transforms, limits, CLT and concentration v2 figures."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


def ellipse_path(cx, cy, rx, ry, angle=0.0, n=100):
    ca,sa=math.cos(angle),math.sin(angle); pts=[]
    for i in range(n+1):
        t=2*math.pi*i/n; x=rx*math.cos(t);y=ry*math.sin(t)
        pts.append((cx+ca*x-sa*y,cy+sa*x+ca*y))
    return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+"Z"


def gaussian():
    out=begin("多元高斯的协方差几何、条件化与重参数","协方差决定 Mahalanobis 椭球；条件分布由 Schur 补给出；Cholesky 同时支持采样与稳定 log-density。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","等 Mahalanobis 距离椭圆",BLUE)
    out += [line(65,290,350,290,GRID,2),line(205,430,205,105,GRID,2),path(ellipse_path(205,270,125,65,-0.45),BLUE,3),path(ellipse_path(205,270,80,42,-0.45),TEAL,2),circle(205,270,6,INK,INK)]
    out += [line(205,270,300,225,BLUE,3),line(205,270,235,330,TEAL,3),text(205,255,"mu",16,700,"middle"),text(45,415,"(x-mu)^T Sigma^-1 (x-mu)=c",16,650,cls="math"),text(45,455,"主轴是 eigenvectors；尺度是 sqrt(eigenvalues)。",15,fill=MUTED)]

    heading(out,430,"B","条件化移动均值并缩小协方差",TEAL)
    out += [path(ellipse_path(595,260,145,95,-0.35),BLUE,2.5),line(440,240,760,240,AMBER,2,"7 5"),circle(620,240,7,TEAL,TEAL),text(660,225,"X_b=b",16,700,fill=AMBER)]
    out += [text(430,380,"mu_a|b = mu_a + Sigma_ab Sigma_bb^-1(b-mu_b)",15,650,cls="math"),text(430,420,"Sigma_a|b = Sigma_aa - Sigma_ab Sigma_bb^-1 Sigma_ba",15,650,cls="math"),text(430,460,"Schur complement <= marginal covariance",15,fill=MUTED)]

    heading(out,830,"C","Cholesky：采样与稳定计算",AMBER)
    out += [circle(875,205,60,BLUE,"#EFF6FF",2.5),text(875,212,"Z~N(0,I)",16,700,"middle",BLUE),line(940,205,1010,205,INK,2.5,marker="a3"),path(ellipse_path(1090,205,75,43,-0.45),TEAL,3,"#ECFDF5"),text(975,185,"L",20,700,"middle")]
    out += [text(835,325,"X = mu + L Z,   Sigma = L L^T",17,650,cls="math"),text(835,370,"solve L y = x-mu; quadratic = ||y||^2",16,650,cls="math"),text(835,415,"log det Sigma = 2 sum_i log L_ii",16,650,cls="math"),text(835,455,"不显式形成 Sigma^-1 或 determinant。",15,fill=MUTED)]
    return finish(out,"多元高斯的椭球、条件截面与重参数是同一协方差结构的三种接口。")


def transform():
    out=begin("随机变量变换与密度换元","推前概率通过原像守恒；非单射变换需要汇总所有逆分支；Jacobian 体积放大与密度缩小互为倒数。",(BLUE,TEAL,RED))
    heading(out,42,"A","推前：输出事件取原像",BLUE)
    node(out,55,120,125,68,"T^-1(B)",TEAL); node(out,270,120,75,68,"B",BLUE)
    out += [line(185,154,265,154,INK,2.5,marker="a3"),text(225,135,"T",18,700,"middle"),text(45,250,"P_Y(B)=P_X(T^-1(B))",18,700,cls="math"),text(45,300,"T 不必可逆；原像始终是合法集合。",16),text(45,350,"离散情形：把原像中所有点质量相加。",16,650),text(45,405,"先写集合守恒，再选择 PMF/CDF/PDF 表示。",15,fill=MUTED)]

    heading(out,430,"B","非单射：Y=X^2 的两分支",TEAL)
    out += [line(455,360,760,360,GRID,2),line(605,410,605,105,GRID,2),path("M480 120Q605 360 730 120",TEAL,3),circle(530,250,7,BLUE,BLUE),circle(680,250,7,BLUE,BLUE),line(530,250,605,250,RED,2,"6 5"),line(680,250,605,250,RED,2,"6 5")]
    out += [text(530,230,"-sqrt(y)",15,650,"middle"),text(680,230,"+sqrt(y)",15,650,"middle"),text(430,425,"f_Y(y) = [f_X(sqrt y)+f_X(-sqrt y)]/(2 sqrt y)",14,650,cls="math"),text(430,465,"漏掉任一分支都会丢失质量；T'(0)=0 单独审计。",15,fill=MUTED)]

    heading(out,830,"C","Jacobian：体积与密度互逆",RED)
    out += [path("M850 145H955V270H850Z",BLUE,3,"#EFF6FF"),line(975,210,1030,210,INK,2.5,marker="a3"),path("M1060 130L1140 160L1120 300L1040 270Z",TEAL,3,"#ECFDF5")]
    out += [text(902,315,"dx",16,700,"middle"),text(1090,335,"dy",16,700,"middle"),text(830,385,"dy ≈ |det J_T(x)| dx",17,650,cls="math"),text(830,425,"f_Y(y)=f_X(x)/|det J_T(x)|",17,650,cls="math"),text(830,465,"绝对值去除定向翻转；det=0 表示密度奇异。",15,fill=MUTED)]
    return finish(out,"变换分布的统一原则是质量守恒：原像求和与 Jacobian 换元只是不同坐标表达。")


def convergence_lln():
    out=begin("随机变量收敛模式与大数定律","Lp 与几乎处处收敛都推出依概率收敛，依概率推出依分布；WLLN 用方差缩减和 Chebyshev 建立平均的一致性。",(BLUE,TEAL,RED))
    heading(out,42,"A","四种收敛不是同义词",BLUE)
    node(out,55,105,130,58,"L^p",BLUE); node(out,220,105,130,58,"a.s.",TEAL); node(out,135,235,140,62,"in probability",BLUE); node(out,135,365,140,62,"in distribution",TEAL)
    out += [line(120,166,175,228,BLUE,2.5,marker="a0"),line(285,166,235,228,TEAL,2.5,marker="a1"),line(205,300,205,358,INK,2.5,marker="a3")]
    out += [text(45,475,"逆箭头一般失败；需要反例或额外条件。",16,fill=RED)]

    heading(out,430,"B","有限方差 WLLN 的证明链",TEAL)
    stages=(("Xbar_n=(1/n) sum Xi",BLUE),("E[Xbar_n]=mu",TEAL),("Var(Xbar_n)=sigma^2/n",BLUE),("P(|Xbar_n-mu|>=eps) <= sigma^2/(n eps^2)",TEAL))
    for i,(lab,col) in enumerate(stages):
        y=92+i*95; node(out,438,y,325,55,lab,col,size=15)
        if i<3: out.append(line(600,y+58,600,y+88,INK,2,marker="a3"))
    out += [text(600,482,"Xbar_n ->P mu",19,700,"middle",TEAL)]

    heading(out,830,"C","LLN 给一致性，不给全部保证",RED)
    items=("finite n speed needs concentration","Gaussian shape needs CLT","dependence changes effective sample size","nonstationarity changes the target")
    for i,lab in enumerate(items): out += [text(840,125+i*82,"• "+lab,16,650,fill=RED if i>1 else INK)]
    out += [text(840,465,"强大数定律还需要明确可积性与依赖条件。",15,fill=MUTED)]
    return finish(out,"先声明收敛模式与共同概率空间；大数定律只在明确假设下保证样本平均稳定。")


def clt_delta():
    out=begin("中心极限定理与 Delta 方法","CLT 描述 sqrt(n) 放大的平均误差之分布极限；Berry–Esseen量化 CDF 误差；Delta 方法用局部导数传播渐近分布。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","中心化与 sqrt(n) 标准化",BLUE)
    out += [line(55,385,355,385,GRID,2),line(70,415,70,105,GRID,2)]
    skew=[];gauss=[]
    for i in range(121):
        x=i/120*5; skew.append((70+52*x,385-210*x*math.exp(-x)))
        z=-3+6*i/120;gauss.append((70+45*(z+3),385-210*math.exp(-z*z/2)))
    out += [path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in skew),AMBER,3),path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in gauss),BLUE,3),text(120,180,"single: skewed",15,650,fill=AMBER),text(245,225,"standardized sum",15,650,fill=BLUE),text(45,455,"Z_n=(sum Xi-n mu)/(sigma sqrt n) ->d N(0,1)",15,650,cls="math")]

    heading(out,430,"B","有限 n：近似不是等号",TEAL)
    out += [line(450,390,760,390,GRID,2),line(475,420,475,105,GRID,2)]
    pts1=[];pts2=[]
    for i in range(121):
        x=-3+6*i/120; phi=1/(1+math.exp(-1.7*x)); fn=min(1,max(0,phi+0.035*math.sin(4*x)*math.exp(-x*x/3)))
        pts1.append((475+45*(x+3),390-250*phi));pts2.append((475+45*(x+3),390-250*fn))
    out += [path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts1),BLUE,3),path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts2),TEAL,2,"none","7 5"),text(430,450,"sup_x |F_n(x)-Phi(x)| <= C rho/(sigma^3 sqrt n)",14,650,cls="math"),text(430,485,"CDF 绝对误差不等于极端尾部相对误差。",15,fill=MUTED)]

    heading(out,830,"C","Delta：局部切线传播",AMBER)
    out += [line(845,390,1145,390,GRID,2),line(870,420,870,105,GRID,2),path("M870 360C950 350 1000 300 1060 170C1090 120 1120 105 1140 100",BLUE,3),line(905,350,1120,150,AMBER,3,"7 5"),circle(990,290,7,TEAL,TEAL)]
    out += [text(990,320,"theta",16,700,"middle",TEAL),text(830,450,"sqrt n[g(T_n)-g(theta)] ->d g'(theta) Z",15,650,cls="math"),text(830,485,"若 g'(theta)=0，需要二阶展开与新尺度。",15,fill=MUTED)]
    return finish(out,"CLT 是渐近分布结论，Delta 是局部传播规则；二者都不是有限样本尾界。")


def paired_observation_limit_bridge():
    out=begin(
        "从四原子观测到 Gaussian 极限",
        "同一 Beta–Bernoulli 观测对先定义矩匹配 Gaussian 与白化坐标，再由独立样本平均进入 LLN、CLT 和 Delta 传播。",
        (BLUE,TEAL,AMBER),
    )

    heading(out,42,"A","相同矩，不同分布",BLUE)
    for x,y,p,col in (
        (80,155,"3/10",BLUE),
        (80,275,"1/5",TEAL),
        (180,155,"1/5",TEAL),
        (180,275,"3/10",BLUE),
    ):
        out += [circle(x,y,8,col,col),text(x,y-18,p,14,650,"middle",col)]
    out += [
        line(55,310,205,310,GRID,2),
        line(55,310,55,115,GRID,2),
        text(130,345,"W: four atoms",16,700,"middle",BLUE),
        line(215,215,245,215,INK,2.5,marker="a3"),
        path(ellipse_path(300,215,65,42,-0.35),TEAL,3),
        circle(300,215,5,INK,INK),
        text(300,345,"G ~ N(mu,Sigma)",16,700,"middle",TEAL),
        text(45,405,"mu=(1/2,1/2)",16,650,cls="math"),
        text(45,442,"Sigma: diag 1/4; off-diag 1/20",15,650,cls="math"),
        text(45,480,"eigenvalues: 3/10 and 1/5",16,700,fill=AMBER,cls="math"),
    ]

    heading(out,430,"B","变换与 LLN 的依赖边界",TEAL)
    node(out,440,100,88,54,"G-mu",BLUE,size=15)
    node(out,555,100,88,54,"U",TEAL,size=17)
    node(out,670,100,88,54,"Z",AMBER,size=17)
    out += [
        line(530,127,550,127,INK,2.2,marker="a3"),
        line(645,127,665,127,INK,2.2,marker="a3"),
        text(540,98,"Q^T",14,650,"middle"),
        text(655,98,"D^-1/2",14,650,"middle"),
        text(430,200,"Cov(U)=diag(3/10,1/5); Cov(Z)=I",14,650,cls="math"),
    ]
    node(out,440,250,315,62,"fresh Theta_i:  Wbar_n -> mu",TEAL,size=16)
    node(out,440,365,315,68,"shared Theta:  Wbar_n -> (Theta,Theta)",RED,size=15)
    out += [
        text(440,338,"independent complete samples",15,650,fill=TEAL),
        text(440,468,"共享环境不会被增加样本数平均掉。",15,fill=MUTED),
    ]

    heading(out,830,"C","CLT 与 Delta 局部传播",AMBER)
    node(out,840,98,300,64,"sqrt(n)(Wbar_n-mu) -> N(0,Sigma)",BLUE,size=15)
    out += [line(990,165,990,208,INK,2.5,marker="a3")]
    node(out,840,218,300,65,"g(a,b)=a b;  grad g=(1/2,1/2)",TEAL,size=15)
    out += [line(990,286,990,330,INK,2.5,marker="a3")]
    node(out,840,340,300,66,"asymptotic variance = 3/20",AMBER,size=17)
    out += [
        text(840,440,"gradient zero? use n-scale + quadratic limit",15,650,fill=RED),
        text(840,478,"1/4 是边缘均值乘积；joint success 是 3/10。",15,fill=MUTED),
    ]
    return finish(
        out,
        "先区分有限分布与矩匹配参照，再检查跨样本独立，最后才把 Gaussian 极限通过局部导数传播。",
    )


def concentration():
    out=begin("浓缩不等式的假设、Chernoff 优化与有限类代价","尾部假设决定可控制的 MGF；Chernoff 对倾斜参数优化；同时控制有限类需用 union bound 支付 log M。",(BLUE,TEAL,RED))
    heading(out,42,"A","假设越强，尾界越锐利",BLUE)
    out += [line(55,390,355,390,GRID,2),line(70,420,70,105,GRID,2)]
    p1=[];p2=[];p3=[]
    for i in range(1,121):
        t=0.05+4.95*i/120;x=70+55*t
        p1.append((x,390-250/(1+t*t)));p2.append((x,390-250*math.exp(-0.55*t*t)));p3.append((x,390-250*math.exp(-0.55*min(t*t,2.2*t))))
    out += [path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in p1),RED,2.5),path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in p2),BLUE,3),path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in p3),TEAL,2.5,"none","7 5"),text(110,185,"Chebyshev ~1/t^2",15,fill=RED),text(200,265,"Hoeffding exp(-c t^2)",15,fill=BLUE),text(165,320,"Bernstein variance+range",15,fill=TEAL),text(45,455,"界的曲线不是任意真实分布的尾概率。",15,fill=MUTED)]

    heading(out,430,"B","Chernoff：优化指数倾斜",TEAL)
    out += [text(435,125,"P(S>=t) <= exp[-lambda t + psi(lambda)]",15,650,cls="math"),line(455,390,755,390,GRID,2),line(480,420,480,165,GRID,2)]
    pts=[]
    for i in range(121):
        lam=3*i/120; val=(lam-1.35)**2+0.35;pts.append((480+88*lam,390-75*val))
    out += [path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts),TEAL,3),circle(480+88*1.35,390-75*0.35,7,RED,RED),text(599,350,"lambda*",16,700,"middle",RED),text(430,455,"独立性把和的 MGF 化为乘积；最优 lambda 给最强指数。",15,fill=MUTED)]

    heading(out,830,"C","固定对象到有限类同时成立",RED)
    for i,lab in enumerate(("h1","h2","...","hM")): node(out,840+i*72,125,52,48,lab,BLUE,size=15)
    out += [line(840,210,1130,210,INK,2),text(985,245,"select after seeing data",16,700,"middle",RED),text(830,310,"fixed h: 2 exp(-2 n eps^2)",16,650,cls="math"),text(830,355,"all M: union bound -> log M in radius",16,650),text(830,400,"eps = sqrt(log(2M/delta)/(2n))",16,650,cls="math"),text(830,455,"选择后不能继续冒充“预先固定”。",15,fill=MUTED)]
    return finish(out,"高概率界必须同时声明随机对象、尾部假设、置信水平与是否经过数据依赖选择。")


def validate_paired_observation_limit_example():
    """Exact arithmetic gate for the shared PROB-09—12 example."""
    atoms = (
        ((0, 0), Fraction(3, 10)),
        ((1, 0), Fraction(1, 5)),
        ((0, 1), Fraction(1, 5)),
        ((1, 1), Fraction(3, 10)),
    )
    assert sum(p for _, p in atoms) == 1

    mean = tuple(sum(Fraction(x[j]) * p for x, p in atoms) for j in range(2))
    assert mean == (Fraction(1, 2), Fraction(1, 2))
    covariance = tuple(
        tuple(
            sum(
                (Fraction(x[j]) - mean[j]) * (Fraction(x[k]) - mean[k]) * p
                for x, p in atoms
            )
            for k in range(2)
        )
        for j in range(2)
    )
    assert covariance == (
        (Fraction(1, 4), Fraction(1, 20)),
        (Fraction(1, 20), Fraction(1, 4)),
    )

    a, b = covariance[0]
    eigenvalues = (a + b, a - b)
    determinant = a * a - b * b
    assert eigenvalues == (Fraction(3, 10), Fraction(1, 5))
    assert determinant == Fraction(3, 50)

    l11 = Fraction(1, 2)
    l21 = Fraction(1, 10)
    l22_squared = Fraction(6, 25)
    assert l11 * l11 == covariance[0][0]
    assert l11 * l21 == covariance[1][0]
    assert l21 * l21 + l22_squared == covariance[1][1]

    conditional_slope = covariance[1][0] / covariance[0][0]
    conditional_variance = covariance[1][1] - covariance[1][0] ** 2 / covariance[0][0]
    assert conditional_slope == Fraction(1, 5)
    assert conditional_variance == Fraction(6, 25)

    trace = covariance[0][0] + covariance[1][1]
    assert trace == Fraction(1, 2)
    for n in (1, 2, 5, 25):
        assert trace / n == Fraction(1, 2 * n)

    grad = (Fraction(1, 2), Fraction(1, 2))
    delta_variance = sum(
        grad[j] * covariance[j][k] * grad[k]
        for j in range(2)
        for k in range(2)
    )
    assert delta_variance == Fraction(3, 20)
    assert mean[0] * mean[1] == Fraction(1, 4)
    assert atoms[-1][1] == Fraction(3, 10)
    print("PROB-09—12 exact gate: moments + geometry + LLN + Delta passed")


BUILDERS={
    "fig-multivariate-gaussian-geometry-v2.svg":gaussian,
    "fig-random-variable-transform-jacobian-v2.svg":transform,
    "fig-random-convergence-lln-v2.svg":convergence_lln,
    "fig-clt-delta-method-v2.svg":clt_delta,
    "fig-concentration-inequalities-v2.svg":concentration,
    "fig-paired-observation-gaussian-limit-v2.svg":paired_observation_limit_bridge,
}


def main():
    validate_paired_observation_limit_example()
    root=Path(__file__).resolve().parents[2]/"_assets"/"figures"/"probability"
    for name,builder in BUILDERS.items():
        target=root/name;target.write_text(builder(),encoding="utf-8");print(target)


if __name__=="__main__":main()
