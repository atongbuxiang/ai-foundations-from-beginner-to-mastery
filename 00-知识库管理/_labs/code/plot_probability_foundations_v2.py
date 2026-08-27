#!/usr/bin/env python3
"""Generate the first eight probability-foundations figures in textbook style."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, H, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


def probability_space():
    out=begin("样本空间、事件与概率公理","概率模型由结果空间、可判定事件族和满足三公理的概率测度共同组成。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","样本空间：互斥且穷尽",BLUE)
    for i,lab in enumerate(("HH","HT","TH","TT")):
        x=62+(i%2)*130; y=120+(i//2)*105; node(out,x,y,92,58,lab,BLUE if i<2 else TEAL)
    out += [text(45,355,"一次实验恰落入一个 outcome omega。",17,650),text(45,395,"outcome 是元素；event 是元素集合。",16,fill=MUTED),text(45,435,"记录粒度不同，可以得到不同但合法的 Omega。",16,fill=MUTED)]

    heading(out,430,"B","事件族：观察者拥有的信息",TEAL)
    node(out,445,115,135,66,"C_H={HH,HT}",BLUE,size=15); node(out,620,115,135,66,"C_T={TH,TT}",TEAL,size=15)
    out += [line(512,185,512,235,INK,2.5),line(687,185,687,235,INK,2.5),text(600,270,"F={empty, Omega, C_H, C_T}",17,650,"middle"),text(430,330,"若只观察第一次抛掷，HH 与 HT 不可区分。",16),text(430,375,"sigma-algebra 对补集和可数并封闭。",17,650),text(430,415,"它也可以理解为可提出并判定的问题集合。",16,fill=MUTED)]

    heading(out,830,"C","概率测度：三条一致性",AMBER)
    items=(("nonnegative: P(A)>=0",BLUE),("normalized: P(Omega)=1",TEAL),("countably additive on disjoint events",AMBER))
    for i,(lab,col) in enumerate(items): node(out,840,112+i*102,300,62,lab,col,size=15)
    out += [text(840,440,"推出补集、容斥、连续性与 union bound。",16,fill=MUTED)]
    return finish(out,"完整概率模型是 (Omega, F, P)：先定义结果与可问事件，再进行一致赋值。")


def conditioning():
    out=begin("条件概率、全概率与 Bayes 公式","条件化是在事件 B 内重新归一；全概率汇总互斥原因；Bayes 用似然比更新先验 odds。",(BLUE,TEAL,RED))
    heading(out,42,"A","限制到 B，再归一化",BLUE)
    out += [circle(160,235,115,BLUE,"#EFF6FF",2.5),circle(245,235,95,TEAL,"#ECFDF5",2.5),text(112,230,"B",22,700,fill=BLUE),text(215,230,"A∩B",18,700,fill=TEAL)]
    out += [text(45,385,"P(A|B)=P(A∩B)/P(B)",19,700,cls="math"),text(45,425,"B 外质量被排除；B 内总质量缩放为 1。",16,fill=MUTED)]

    heading(out,430,"B","分割原因，汇总证据",TEAL)
    for i,lab in enumerate(("H1","H2","H3")):
        node(out,445,130+i*105,72,52,lab,TEAL,size=16); out.append(line(520,156+i*105,675,235,INK,2,marker="a3"))
    node(out,690,205,70,62,"E",BLUE,size=19)
    out += [text(430,455,"P(E)=sum_i P(E|Hi)P(Hi)",17,650,cls="math"),text(430,490,"原因必须互斥且穷尽；遗漏原因会漏掉证据。",15,fill=MUTED)]

    heading(out,830,"C","Bayes：odds 乘似然比",RED)
    node(out,845,115,120,66,"prior odds\n1:99",BLUE,size=16); node(out,1020,115,120,66,"LR=0.99/0.05",TEAL,size=15)
    out += [line(968,148,1015,148,INK,2.5,marker="a3"),text(990,130,"×",22,700,"middle")]
    node(out,885,235,220,72,"posterior odds ≈ 1:5",RED,size=17)
    out += [text(995,345,"P≈1/6",22,700,"middle",RED),text(830,405,"低 base rate 仍可主导后验。",17,650),text(830,445,"恒等式正确不等于模型与因果假设正确。",16,fill=MUTED)]
    return finish(out,"条件化改变信息集合并重新归一；Bayes 反转的是概率方向，不自动反转因果方向。")


def random_variable():
    out=begin("随机变量、分布与分位数","随机变量把样本结果映到数值；分布是概率的推前；CDF 统一离散、连续与混合情形，广义分位数反转累计概率。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","X: Omega -> R",BLUE)
    for i,lab in enumerate(("HH","HT","TH","TT")):
        x=50+(i%2)*85; y=120+(i//2)*90; node(out,x,y,62,45,lab,BLUE,size=15)
    for val,y in (("2",125),("1",215),("0",305)): node(out,290,y,55,45,val,TEAL,size=17)
    out += [line(115,142,285,147,INK,2,marker="a3"),line(200,142,285,237,INK,2,marker="a3"),line(115,232,285,237,INK,2,marker="a3"),line(200,232,285,327,INK,2,marker="a3"),text(45,405,"X = 正面个数；P_X = P o X^-1",17,650),text(45,442,"多个 outcomes 可以被同一数值分组。",16,fill=MUTED)]

    heading(out,430,"B","PMF、PDF 与 CDF",TEAL)
    rows=(("PMF","point mass; sum=1",BLUE),("PDF","interval probability = area",TEAL),("CDF","F(x)=P(X<=x); always exists",AMBER))
    for i,(a,b,c) in enumerate(rows):
        y=112+i*105; out += [text(440,y+28,a,19,700,fill=c),line(515,y+21,755,y+21,GRID,2),text(530,y+28,b,16,fill=MUTED)]
    out += [text(430,450,"混合分布可同时具有 CDF 跳跃与连续部分。",16,650)]

    heading(out,830,"C","广义分位数与逆变换",AMBER)
    out += [line(850,390,1140,390,GRID,2),line(870,420,870,105,GRID,2),path("M870 370L930 350V300H990L1045 225V160H1125",BLUE,3),line(915,320,1040,320,AMBER,2,"6 5"),line(1040,390,1040,320,AMBER,2,"6 5")]
    out += [text(910,310,"u",17,700,fill=AMBER),text(1040,415,"Q(u)",17,700,"middle",AMBER),text(830,470,"Q(u)=inf{x:F(x)>=u}; U~Unif => Q(U)~F",15,650,cls="math")]
    return finish(out,"先区分随机变量、分布、密度和累计函数；分位数是 CDF 的广义逆，不要求严格单调。")


def discrete():
    out=begin("常用离散分布的生成机制","同一随机试验序列因记录对象不同产生 Bernoulli、Binomial、Geometric 等分布；无放回与稀有事件极限有不同依赖结构。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","重复二元试验：记录什么",BLUE)
    node(out,55,110,130,55,"Bernoulli(p)",BLUE)
    out += [line(120,168,120,220,INK,2.5),line(120,220,290,220,INK,2.5)]
    for y,lab,col in ((245,"total successes -> Bin(n,p)",TEAL),(330,"first success -> Geom(p)",AMBER),(415,"rth success -> NegBin(r,p)",BLUE)):
        node(out,55,y,290,55,lab,col,size=15)
    out += [text(45,500,"固定次数与等待时间是不同随机变量。",15,fill=MUTED)]

    heading(out,430,"B","多类别与有限总体",TEAL)
    node(out,445,110,135,58,"Categorical(pi)",TEAL,size=15); node(out,620,110,135,58,"Multinomial(n,pi)",BLUE,size=15)
    out += [line(583,139,615,139,INK,2.5,marker="a3"),text(600,105,"n iid",15,650,"middle")]
    node(out,445,260,135,58,"population N,K",AMBER,size=15); node(out,620,260,135,58,"Hypergeom",TEAL,size=16)
    out += [line(583,289,615,289,INK,2.5,marker="a3"),text(600,255,"without replacement",15,650,"middle"),text(430,405,"无放回制造负相关，不能假装每次独立。",17,650),text(430,445,"类别计数向量之和固定为 n。",16,fill=MUTED)]

    heading(out,830,"C","Poisson 稀有事件极限",AMBER)
    node(out,845,110,290,58,"X_n ~ Bin(n,p_n)",BLUE)
    out += [line(990,172,990,215,INK,2.5,marker="a3"),text(990,250,"n->∞, p_n->0, n p_n->lambda",17,650,"middle")]
    node(out,845,285,290,60,"X ~ Poisson(lambda)",TEAL)
    out += [text(990,385,"E[X]=Var(X)=lambda",18,700,"middle"),text(830,440,"“n 大”不够；总均值必须保持有限。",16,fill=MUTED)]
    return finish(out,"分布名不是关键词匹配：先写随机机制、支持集、依赖与记录对象。")


def continuous():
    out=begin("常用连续分布与指数族","连续密度先匹配支持集和尾部；指数族以配分函数统一归一化、矩与曲率。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","density 高度不是点概率",BLUE)
    out += [line(55,385,355,385,GRID,2),line(70,410,70,100,GRID,2)]
    pts=[]
    for i in range(121):
        x=-3+6*i/120; y=math.exp(-x*x/2); pts.append((70+45*(x+3),385-210*y))
    out.append(path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts),BLUE,3))
    out += [line(95,315,160,315,TEAL,8),path("M220 385C225 245 265 215 345 360",AMBER,3),text(105,300,"Uniform",15,650,fill=TEAL),text(200,180,"Gaussian",16,650,fill=BLUE),text(285,245,"Exp",16,650,fill=AMBER),text(45,455,"probability = area; point probability is usually 0",15,fill=MUTED)]

    heading(out,430,"B","支持集先于形状参数",TEAL)
    out += [text(445,125,"Gamma: x>0",18,700,fill=AMBER),text(445,170,"shape controls zero-boundary and skew",16,fill=MUTED),text(445,245,"Beta: 0<x<1",18,700,fill=TEAL),text(445,290,"can be left/right skewed or U-shaped",16,fill=MUTED)]
    node(out,445,350,310,64,"support mismatch = model error",BLUE,size=16)

    heading(out,830,"C","指数族：A(eta) 编码矩",AMBER)
    node(out,835,105,310,72,"p_eta(x)=h(x) exp(eta^T T(x)-A(eta))",BLUE,size=15)
    out += [line(990,182,990,220,INK,2.5,marker="a3")]
    node(out,835,230,310,58,"grad A = E_eta[T(X)]",TEAL,size=16)
    out += [line(990,292,990,330,INK,2.5,marker="a3")]
    node(out,835,340,310,58,"Hess A = Cov_eta(T) >= 0",AMBER,size=16)
    out += [text(835,455,"微分移入积分需要共同支持与可积控制。",16,fill=MUTED)]
    return finish(out,"连续模型先审计支持集、尾部和面积；指数族公式的导数仍需交换微分与积分的条件。")


def joint():
    out=begin("联合分布、边缘分布与独立性","联合分布保留变量配对；边缘化沿轴求和会丢失 coupling；独立要求整个联合测度分解。",(BLUE,TEAL,RED))
    heading(out,42,"A","联合表沿轴边缘化",BLUE)
    vals=[[".30",".20",".50"],[".10",".40",".50"],[".40",".60","1.00"]]
    for i in range(3):
        for j in range(3):
            x=65+j*88;y=125+i*70; out.append(rect(x,y,88,70,GRID,"#EFF6FF" if i<2 and j<2 else "#ECFDF5",0,1.5));out.append(text(x+44,y+43,vals[i][j],16,650,"middle"))
    out += [text(200,365,"p_X(x)=sum_y p(x,y)",17,650,"middle"),text(200,405,"p_Y(y)=sum_x p(x,y)",17,650,"middle"),text(45,450,"边缘化丢掉 X、Y 如何配对。",16,fill=MUTED)]

    heading(out,430,"B","相同边缘，不同 coupling",TEAL)
    for offset,rev,label in ((0,False,"same"),(165,True,"opposite")):
        x=450+offset
        for i in range(2):
            for j in range(2):
                fill=TEAL if (i==j) != rev else BG; out.append(rect(x+j*55,145+i*55,55,55,GRID,fill,0,1.5))
        out.append(text(x+55,285,label,16,650,"middle"))
    out += [text(600,345,"P_X=P_Y=Bernoulli(1/2)",17,650,"middle"),text(430,390,"但 P(X=Y) 可以是 1 或 0。",17,700),text(430,430,"边缘不能恢复依赖。",16,fill=MUTED)]

    heading(out,830,"C","独立是强分解合同",RED)
    node(out,840,115,105,58,"P_X",BLUE); node(out,1035,115,105,58,"P_Y",TEAL)
    out += [text(990,152,"×",25,700,"middle"),line(990,180,990,235,INK,2.5,marker="a3")]
    node(out,845,250,290,72,"P_(X,Y) = P_X tensor P_Y",RED,size=16)
    out += [text(830,375,"p(x,y)=p_X(x)p_Y(y) for all measurable sets",15,650),text(830,420,"检查一个事件或零相关远远不够。",16,fill=MUTED)]
    return finish(out,"边缘描述各变量，联合描述它们如何配对；独立必须对整个联合分布成立。")


def expectation():
    out=begin("期望、方差与矩","期望是对分布的线性积分；方差是中心化平方矩；矩的存在与交叉协方差决定尺度传播是否有效。",(BLUE,TEAL,AMBER))
    heading(out,42,"A","期望是加权汇总",BLUE)
    xs=(90,190,290); ps=(0.15,0.30,0.55)
    out += [line(65,355,345,355,GRID,2)]
    for x,p,lab in zip(xs,ps,("0","1","2")):
        out += [line(x,355,x,355-260*p,BLUE,10),text(x,385,lab,17,650,"middle"),text(x,345-260*p,f"p={p}",15,650,"middle",BLUE)]
    out += [text(200,445,"E[X]=sum x p(x)=1.4",19,700,"middle"),text(45,480,"均值不必位于支持集，也不等于众数。",15,fill=MUTED)]

    heading(out,430,"B","方差围绕均值测量平方波动",TEAL)
    out += [line(450,275,750,275,GRID,2),line(600,180,600,350,TEAL,2,"6 5"),text(600,165,"mu",17,700,"middle",TEAL)]
    for x in (485,535,650,720): out.append(circle(x,275,8,BLUE,BLUE))
    out += [text(600,390,"Var(X)=E[(X-mu)^2]",18,700,"middle",cls="math"),text(600,430,"=E[X^2]-E[X]^2 >= 0",17,650,"middle",cls="math"),text(430,470,"单位平方；重尾时可能不存在。",16,fill=MUTED)]

    heading(out,830,"C","线性与尺度传播",AMBER)
    out += [text(835,135,"indicator I_A: E[I_A]=P(A)",17,650),text(835,195,"E[sum I_i]=sum P(A_i)",17,650),text(835,255,"linearity does not require independence",16,fill=TEAL)]
    node(out,835,315,310,68,"Var(q dot k)=d  -> scale by 1/sqrt(d)",AMBER,size=15)
    out += [text(835,430,"方差相加必须检查协方差交叉项。",16,fill=MUTED)]
    return finish(out,"期望的线性最可靠；方差与高阶矩需要存在性、中心化和依赖结构审计。")


def covariance():
    out=begin("协方差、相关性与条件期望","协方差只测线性共变；零协方差不等于独立；条件期望是给定信息下的 L2 正交投影。",(BLUE,TEAL,RED))
    heading(out,42,"A","中心化乘积的平均",BLUE)
    out += [line(75,280,350,280,GRID,2),line(210,410,210,105,GRID,2)]
    pts=((110,350),(140,320),(275,190),(310,150),(120,170),(295,340))
    for x,y in pts: out.append(circle(x,y,7,BLUE if (x-210)*(280-y)>0 else RED,BLUE if (x-210)*(280-y)>0 else RED))
    out += [text(45,445,"Cov(X,Y)=E[(X-mu_X)(Y-mu_Y)]",16,650,cls="math"),text(45,480,"同侧偏差为正，异侧偏差为负。",15,fill=MUTED)]

    heading(out,430,"B","零协方差仍可强依赖",RED)
    out += [line(450,390,760,390,GRID,2),line(605,420,605,100,GRID,2),path("M470 150Q605 390 740 150",RED,3)]
    for x in (490,540,605,670,720):
        y=390-0.013*(x-605)**2; out.append(circle(x,y,6,RED,RED))
    out += [text(600,440,"Y=X^2; X symmetric => Cov(X,Y)=0",16,650,"middle",cls="math"),text(430,480,"Y 完全由 X 决定；不相关不等于独立。",15,fill=MUTED)]

    heading(out,830,"C","条件期望是 L2 投影",TEAL)
    out += [line(865,380,1125,380,GRID,3),circle(930,190,8,BLUE,BLUE),line(930,198,995,380,BLUE,3),line(930,190,1060,310,RED,2,"7 5"),circle(995,380,7,TEAL,TEAL)]
    out += [text(925,165,"X",18,700,"middle",BLUE),text(995,410,"E[X|G]",16,700,"middle",TEAL),text(835,455,"E[(X-E[X|G])Z]=0 for every Z in L2(G)",15,650,cls="math"),text(835,490,"因此它最小化给定信息下的 MSE。",15,fill=MUTED)]
    return finish(out,"相关性只回答线性问题；条件期望回答在给定信息下的最佳平方预测问题。")


def hidden_coin_bridge():
    out=begin(
        "隐藏硬币模型：从概率空间到联合依赖",
        "八原子概率空间经条件化得到来源后验，经随机变量推前得到正面数分布，经边缘化得到条件独立但边缘相关的两次抛掷。",
        (BLUE,TEAL,RED),
    )
    heading(out,42,"A","八原子概率合同",BLUE)
    node(out,50,100,125,56,"Z=F: 2/3",BLUE,size=16)
    node(out,225,100,125,56,"Z=B: 1/3",RED,size=16)
    out += [
        text(50,210,"F row: 1/6, 1/6, 1/6, 1/6",15,650),
        text(50,255,"B row: 1/48, 1/16, 1/16, 3/16",15,650),
        line(50,290,350,290,GRID,2),
        text(200,335,"8 atoms; total mass = 1",18,700,"middle"),
        text(50,395,"Omega={F,B} x {0,1} x {0,1}",16,650),
        text(50,440,"outcome 是元素；event 是元素集合。",16,fill=MUTED),
    ]

    heading(out,430,"B","条件更新与推前分布",TEAL)
    node(out,445,98,310,58,"P(X1=1) = 7/12",BLUE,size=17)
    node(out,445,205,145,62,"P(B|H) = 3/7",TEAL,size=16)
    node(out,610,205,145,62,"P(B|HH) = 9/17",TEAL,size=16)
    out.append(line(600,160,600,198,INK,2.5,marker="a3"))
    node(out,445,330,310,70,"S=X1+X2: 3/16, 11/24, 17/48",BLUE,size=15)
    out += [
        text(600,445,"Q(0.5)=1; Q(0.9)=2",17,650,"middle"),
        text(430,482,"条件化重加权；随机变量合并原子。",15,fill=MUTED),
    ]

    heading(out,830,"C","条件独立不等于边缘独立",RED)
    node(out,842,98,292,58,"P(X1=1)=P(X2=1)=7/12",BLUE,size=15)
    node(out,842,205,292,64,"P(1,1)=17/48",TEAL,size=17)
    node(out,842,320,292,68,"17/48 != (7/12)^2",RED,size=17)
    out += [
        line(988,160,988,198,INK,2.5,marker="a3"),
        line(988,273,988,313,INK,2.5,marker="a3"),
        text(842,445,"X1 independent X2 | Z",16,700,fill=TEAL),
        text(842,480,"潜变量混合后产生边缘依赖。",15,fill=MUTED),
    ]
    return finish(
        out,
        "同一份联合模型依次支持事件概率、Bayes 更新、推前分布与独立性审计。",
    )


def beta_bernoulli_bridge():
    out=begin(
        "Beta–Bernoulli：从连续隐变量到矩、依赖与分布族",
        "随机成功率 Θ 把连续密度、条件 Bernoulli、边缘相关和过度离散连接成同一份可复算模型。",
        (TEAL,BLUE,AMBER),
    )

    heading(out,42,"A","连续隐变量与矩",TEAL)
    out += [line(62,345,350,345,GRID,2),line(62,345,62,125,GRID,2)]
    pts=[]
    for i in range(101):
        theta=i/100
        density=6*theta*(1-theta)
        pts.append((62+288*theta,345-125*density))
    out.append(path("M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts),TEAL,3))
    out += [
        line(206,345,206,155,AMBER,2,"6 5"),
        text(206,372,"1/2",15,650,"middle",AMBER),
        text(205,112,"f(theta)=6 theta(1-theta)",17,700,"middle",TEAL,cls="math"),
        text(48,416,"E[Theta]=1/2; E[Theta^2]=3/10",16,650,cls="math"),
        text(48,458,"Var(Theta)=1/20",18,700,fill=BLUE,cls="math"),
        text(48,493,"参数本身随样本变化。",15,fill=MUTED),
    ]

    heading(out,430,"B","条件独立，边缘正相关",BLUE)
    node(out,535,103,120,58,"Theta",TEAL,size=18)
    node(out,450,220,115,58,"X1 | Theta",BLUE,size=15)
    node(out,625,220,115,58,"X2 | Theta",BLUE,size=15)
    out += [
        line(565,163,510,213,INK,2.5,marker="a3"),
        line(625,163,682,213,INK,2.5,marker="a3"),
        text(600,325,"X1 independent X2 | Theta",16,700,"middle",TEAL),
        text(440,376,"P(1,1)=3/10; Cov=1/20; rho=1/5",15,650,cls="math"),
        text(440,422,"E[X2|X1=1]=3/5",16,650,cls="math"),
        text(440,458,"E[X2|X1=0]=2/5",16,650,cls="math"),
        text(440,493,"共享原因被边缘化后留下依赖。",15,fill=MUTED),
    ]

    heading(out,830,"C","同均值，不同计数波动",AMBER)
    base_y=260
    for x,p in zip((862,912,962),(0.25,0.50,0.25)):
        out += [line(x,base_y,x,base_y-125*p,BLUE,13)]
    for x,p in zip((1030,1080,1130),(0.30,0.40,0.30)):
        out += [line(x,base_y,x,base_y-125*p,TEAL,13)]
    out += [
        line(845,base_y,1145,base_y,GRID,2),
        text(912,130,"Bin(2,1/2)",15,700,"middle",BLUE),
        text(1080,130,"Beta-Binomial",15,700,"middle",TEAL),
        text(912,294,"(1/4, 1/2, 1/4)",14,650,"middle",BLUE),
        text(1080,294,"(3/10, 2/5, 3/10)",14,650,"middle",TEAL),
        text(845,346,"same E[S]=1",17,700,fill=INK,cls="math"),
        text(845,384,"Var: 1/2  ->  3/5",18,700,fill=AMBER,cls="math"),
        text(845,430,"Bernoulli exponential family:",15,650),
        text(845,462,"A'(eta)=theta; A''(eta)=theta(1-theta)",14,650,cls="math"),
        text(845,493,"随机参数使计数出现额外离散。",15,fill=MUTED),
    ]
    return finish(
        out,
        "先读连续参数，再读条件结构，最后比较边缘计数；均值相同并不意味着不确定性结构相同。",
    )


def validate_hidden_coin_example():
    """Exact arithmetic gate for the shared PROB-01—04 example."""
    fair = (Fraction(1, 6),) * 4
    biased = (
        Fraction(1, 48),
        Fraction(1, 16),
        Fraction(1, 16),
        Fraction(3, 16),
    )
    assert sum(fair + biased) == 1

    head = Fraction(7, 12)
    posterior_one = Fraction(1, 4) / head
    posterior_two = Fraction(3, 16) / Fraction(17, 48)
    assert posterior_one == Fraction(3, 7)
    assert posterior_two == Fraction(9, 17)

    s_pmf = (
        Fraction(3, 16),
        Fraction(11, 24),
        Fraction(17, 48),
    )
    assert sum(s_pmf) == 1

    marginal_head = Fraction(7, 12)
    joint_heads = Fraction(17, 48)
    assert joint_heads != marginal_head * marginal_head
    assert joint_heads - marginal_head * marginal_head == Fraction(1, 72)
    print("PROB-01—04 exact gate: atoms + Bayes + pushforward + dependence passed")


def validate_beta_bernoulli_example():
    """Exact arithmetic gate for the shared PROB-05—08 example."""
    def beta_integer(a: int, b: int) -> Fraction:
        return Fraction(
            math.factorial(a - 1) * math.factorial(b - 1),
            math.factorial(a + b - 1),
        )

    normalization = 6 * beta_integer(2, 2)
    mean_theta = 6 * beta_integer(3, 2)
    second_theta = 6 * beta_integer(4, 2)
    variance_theta = second_theta - mean_theta * mean_theta
    assert normalization == 1
    assert mean_theta == Fraction(1, 2)
    assert second_theta == Fraction(3, 10)
    assert variance_theta == Fraction(1, 20)

    beta_binomial = (
        6 * beta_integer(2, 4),
        12 * beta_integer(3, 3),
        6 * beta_integer(4, 2),
    )
    assert beta_binomial == (
        Fraction(3, 10),
        Fraction(2, 5),
        Fraction(3, 10),
    )
    assert sum(beta_binomial) == 1
    mean_s = sum(Fraction(k) * p for k, p in enumerate(beta_binomial))
    second_s = sum(Fraction(k * k) * p for k, p in enumerate(beta_binomial))
    assert mean_s == 1
    assert second_s == Fraction(8, 5)
    assert second_s - mean_s * mean_s == Fraction(3, 5)

    covariance = second_theta - mean_theta * mean_theta
    correlation = covariance / Fraction(1, 4)
    conditional_one = second_theta / mean_theta
    conditional_zero = (mean_theta - second_theta) / (1 - mean_theta)
    assert covariance == Fraction(1, 20)
    assert correlation == Fraction(1, 5)
    assert conditional_one == Fraction(3, 5)
    assert conditional_zero == Fraction(2, 5)
    print("PROB-05—08 exact gate: Beta moments + covariance + mixture PMF passed")


BUILDERS={
    "fig-probability-space-axioms-v2.svg":probability_space,
    "fig-conditioning-bayes-odds-v2.svg":conditioning,
    "fig-random-variable-cdf-quantile-v2.svg":random_variable,
    "fig-discrete-distribution-mechanisms-v2.svg":discrete,
    "fig-continuous-exponential-family-v2.svg":continuous,
    "fig-joint-marginal-independence-v2.svg":joint,
    "fig-expectation-variance-moments-v2.svg":expectation,
    "fig-covariance-conditional-expectation-v2.svg":covariance,
    "fig-hidden-coin-probability-language-v2.svg":hidden_coin_bridge,
    "fig-beta-bernoulli-moments-families-v2.svg":beta_bernoulli_bridge,
}


def main():
    validate_hidden_coin_example()
    validate_beta_bernoulli_example()
    root=Path(__file__).resolve().parents[2]/"_assets"/"figures"/"probability"
    root.mkdir(parents=True,exist_ok=True)
    for name,builder in BUILDERS.items():
        target=root/name;target.write_text(builder(),encoding="utf-8");print(target)


if __name__=="__main__":
    main()
