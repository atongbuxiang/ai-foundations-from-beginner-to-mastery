#!/usr/bin/env python3
"""Generate LT-09--16 textbook figures for PAC learning and finite classes."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def concentration_interface():
    out = begin(
        "从固定预测器的浓缩到数据依赖选择",
        "Hoeffding 直接控制看数据前固定的 h；若 h 由同一训练集选出，必须改用同时控制、稳定性或独立测试集。置信半径只在有界、独立和目标分布不变的合同下成立。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "固定 h：经验均值围绕总体均值", BLUE)
    out += [line(60, 320, 350, 320, GRID, 2), line(60, 120, 60, 320, GRID, 2)]
    out += [line(75, 220, 335, 220, TEAL, 2.5), text(342, 226, "R_P(h)", 15, 700, fill=TEAL)]
    for i, (x, y) in enumerate(((85, 250), (125, 185), (165, 235), (205, 205), (245, 255), (285, 195), (325, 225))):
        out += [circle(x, y, 7, BLUE, BLUE), line(x, 320, x, y, GRID, 1.5)]
    out += [text(45, 385, "R_S(h)=m^{-1} sum_i ell(h,Z_i)", 15, 650, cls="math"), text(45, 425, "Pr(|R_S-R_P| > eps) <= 2 exp(-2m eps^2)", 15, 650, fill=BLUE, cls="math"), text(45, 475, "requires iid and loss in [0,1]", 15, 650, fill=RED), text(45, 510, "pointwise statement: h was fixed before S。", 15, fill=MUTED)]

    heading(out, 430, "B", "学习器看过 S：选择引入偏差", TEAL)
    for i, y in enumerate((112, 190, 268, 346)):
        out += [rect(445, y, 185, 48, BLUE if i < 3 else TEAL, BG, 7, 2), text(537, y + 30, f"candidate h{i+1}", 15, 650, "middle")]
        out += [text(655, y + 30, f"R_S={0.31 - 0.07*i:.2f}", 15, 650, fill=TEAL if i == 3 else INK)]
    out += [path("M725 105C780 165 780 330 725 400", RED, 2.5, "none", "7 5"), text(665, 435, "A selects the smallest", 15, 700, fill=RED), text(430, 480, "E R_S(h_S) need not equal E R_P(h_S)", 15, 650, fill=RED), text(430, 510, "the minimum is optimistically selected。", 15, fill=MUTED)]

    heading(out, 830, "C", "三条合法的修桥路线", RED)
    rows = (("uniform control", "one event covers every h", BLUE), ("algorithmic stability", "bound sensitivity to one sample", TEAL), ("fresh evaluation", "condition on frozen h_S", RED))
    for i, (name, desc, col) in enumerate(rows):
        y = 100 + i * 112
        out += [rect(840, y, 300, 78, col, BG, 8, 2), text(860, y + 29, name, 15, 700, fill=col), text(860, y + 58, desc, 15, 600)]
    out += [text(830, 455, "dependence / heavy tails need new tools", 15, 650, fill=RED), text(830, 490, "distribution shift is not sampling noise", 15, 650), text(830, 520, "name the randomness before using a tail bound。", 15, fill=MUTED)]
    return finish(out, "浓缩不等式先回答固定查询；学习理论的核心工作，是把它升级为对数据依赖输出仍然有效的风险证书。")


def pac_contract():
    out = begin(
        "PAC 学习的量词合同与样本复杂度",
        "PAC 把 accuracy eps、confidence delta、允许的分布族、比较器和样本量写成统一的高概率合同；realizable 与 agnostic 的差别在 comparator，不在口号。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "量词顺序决定承诺强度", BLUE)
    stages = (("exists learner A", BLUE), ("for every eps, delta", TEAL), ("for every allowed P", RED), ("m >= m_H(eps,delta)", BLUE))
    for i, (lab, col) in enumerate(stages):
        y = 85 + i * 90
        node(out, 55, y, 290, 52, lab, col, size=15)
        if i < 3:
            out += [line(200, y + 55, 200, y + 82, INK, 2, marker="a3")]
    out += [text(45, 478, "A cannot depend on the unknown P", 15, 650, fill=RED), text(45, 510, "eps and delta are requested before sampling。", 15, fill=MUTED)]

    heading(out, 430, "B", "成功事件：风险好，而非训练损失低", TEAL)
    node(out, 445, 95, 310, 58, "S ~ P^m,  U ~ learner randomness", BLUE, size=15)
    out += [line(600, 156, 600, 193, INK, 2, marker="a3")]
    node(out, 445, 205, 310, 58, "h_{S,U} = A(S,U)", TEAL, size=15)
    out += [line(600, 266, 600, 303, INK, 2, marker="a3")]
    out += [rect(445, 315, 310, 82, RED, BG, 8, 2), text(600, 346, "Pr[R_P(h_{S,U}) <= comparator + eps]", 15, 650, "middle", fill=RED), text(600, 378, ">= 1-delta", 17, 700, "middle", fill=RED)]
    out += [text(430, 455, "eps: quality tolerance", 15, 650, fill=BLUE), text(620, 455, "delta: failure budget", 15, 650, fill=TEAL), text(430, 510, "probability is over S and U。", 15, fill=MUTED)]

    heading(out, 830, "C", "两种 comparator 与三种复杂度", RED)
    out += [rect(840, 88, 300, 72, BLUE, BG, 8, 2), text(860, 117, "realizable", 15, 700, fill=BLUE), text(860, 145, "comparator = 0", 15, 650)]
    out += [rect(840, 185, 300, 72, TEAL, BG, 8, 2), text(860, 214, "agnostic", 15, 700, fill=TEAL), text(860, 242, "comparator = inf_{h in H} R_P(h)", 15, 650)]
    out += [text(830, 315, "statistical: how large must m be?", 15, 650), text(830, 355, "computational: can A run efficiently?", 15, 650), text(830, 395, "representational: how large is approximation error?", 15, 650), text(830, 455, "distribution-free != assumption-free", 15, 650, fill=RED), text(830, 490, "expectation guarantee != PAC confidence", 15, 650), text(830, 520, "sample complexity is a function, not a slogan。", 15, fill=MUTED)]
    return finish(out, "PAC 是可审计的有限样本合同：先写全对象和量词，再讨论具体算法给出的 m_H(eps,delta)。")


def finite_union():
    out = begin(
        "有限假设类：从逐点坏事件到一致收敛",
        "对 M 个预先固定假设的 Hoeffding 坏事件做 Union Bound，可构造覆盖所有 h 的共同好事件；代价是 log M，而事件之间不需要独立。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "每个固定 h 都有一个坏事件", BLUE)
    for i in range(5):
        y = 90 + i * 75
        col = RED if i in (1, 4) else BLUE
        out += [circle(85, y + 18, 15, col, BG, 2), text(85, y + 24, f"h{i+1}", 14, 700, "middle", fill=col), text(125, y + 24, "B_h: |R_S(h)-R_P(h)| > eps", 15, 650)]
    out += [text(45, 485, "Pr(B_h) <= 2 exp(-2m eps^2)", 15, 650, fill=BLUE), text(45, 515, "all B_h use the same sample S。", 15, fill=MUTED)]

    heading(out, 430, "B", "Supremum 事件就是并集", TEAL)
    out += [path("M455 115C505 70 700 70 755 120C790 165 760 240 685 248C620 290 495 265 455 215C430 180 430 145 455 115Z", RED, 2.5, "#FFF7ED")]
    for x, y, lab in ((500, 145, "B1"), (610, 120, "B2"), (700, 168, "B3"), (545, 215, "B4"), (660, 220, "B5")):
        out += [circle(x, y, 26, RED, BG, 2), text(x, y + 6, lab, 15, 700, "middle", fill=RED)]
    out += [text(430, 330, "{sup_h gap(h) > eps} = union_h B_h", 15, 700, fill=TEAL, cls="math"), text(430, 385, "Pr(union_h B_h) <= sum_h Pr(B_h)", 15, 650, cls="math"), text(430, 440, "independence is not required", 15, 700, fill=RED), text(430, 485, "indicator inequality proves the union bound", 15, 650), text(430, 515, "dependence may only make the bound loose。", 15, fill=MUTED)]

    heading(out, 830, "C", "反解后：类大小只付 log M", RED)
    out += [rect(840, 95, 300, 88, TEAL, BG, 8, 2), text(990, 128, "with probability >= 1-delta", 15, 650, "middle", fill=TEAL), text(990, 162, "sup_h |R_S-R_P| <= sqrt(log(2M/delta)/(2m))", 14, 650, "middle", fill=TEAL)]
    out += [text(830, 240, "M = number of distinct prediction functions", 15, 650), text(830, 282, "not parameter files or training runs", 15, 650, fill=RED), text(830, 332, "simultaneous event covers data-chosen h_S", 15, 650), text(830, 382, "candidate set must be fixed independently", 15, 650), text(830, 432, "infinite classes need growth / covers / complexity", 15, 650), text(830, 482, "log M is a selection price", 15, 700, fill=BLUE), text(830, 515, "it is not a claim that large classes are harmless。", 15, fill=MUTED)]
    return finish(out, "Union Bound 的作用不是制造独立性，而是把 M 个逐点证书合成一个可用于数据依赖选择的共同事件。")


def realizable_erm():
    out = begin(
        "可实现情形：坏假设在版本空间中的生存概率",
        "若存在零风险真规则且学习器返回零训练误差假设，风险大于 eps 的固定坏假设必须连续 m 次避开自身错误区域；其生存概率至多 exp(-m eps)，故得到 1/eps 率。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "版本空间随样本逐步收缩", BLUE)
    for i, (x, y, w, h, col) in enumerate(((55, 95, 300, 310, BLUE), (90, 135, 235, 235, TEAL), (130, 175, 155, 155, RED))):
        out += [rect(x, y, w, h, col, "none", 10, 2.5)]
    out += [circle(205, 245, 9, BLUE, BLUE), text(222, 251, "h* remains", 15, 700, fill=BLUE), text(45, 445, "V(S)={h: R_S(h)=0}", 16, 700, fill=TEAL), text(45, 485, "realizability guarantees V(S) is nonempty", 15, 650), text(45, 515, "any consistent learner outputs inside V(S)。", 15, fill=MUTED)]

    heading(out, 430, "B", "一个坏 h 怎样幸存", TEAL)
    out += [rect(445, 95, 310, 82, RED, BG, 8, 2), text(600, 127, "error region E_h", 16, 700, "middle", fill=RED), text(600, 158, "P_X(E_h)=R_P(h) > eps", 15, 650, "middle")]
    for i, x in enumerate((465, 520, 575, 630, 685, 740)):
        out += [circle(x, 255, 9, TEAL, TEAL), text(x, 290, f"Z{i+1}", 13, 650, "middle")]
    out += [path("M450 315C505 355 700 355 755 315", BLUE, 2.5), text(600, 382, "all m draws miss E_h", 15, 700, "middle", fill=BLUE), text(430, 430, "Pr(h survives)=(1-R_P(h))^m", 15, 650, cls="math"), text(430, 468, "<= (1-eps)^m <= exp(-m eps)", 15, 700, fill=TEAL, cls="math"), text(430, 515, "one-sided survival event—not mean estimation。", 15, fill=MUTED)]

    heading(out, 830, "C", "对所有坏假设求并集", RED)
    out += [rect(840, 95, 300, 76, RED, BG, 8, 2), text(990, 128, "Pr(R_P(h_S)>eps)", 16, 700, "middle", fill=RED), text(990, 157, "<= M exp(-m eps)", 16, 700, "middle", fill=RED)]
    out += [line(990, 175, 990, 210, INK, 2, marker="a3")]
    out += [rect(840, 222, 300, 72, TEAL, BG, 8, 2), text(990, 251, "m >= (log M + log(1/delta))/eps", 14, 650, "middle", fill=TEAL), text(990, 278, "is sufficient", 15, 700, "middle", fill=TEAL)]
    out += [text(830, 350, "1/eps comes from excluding error regions", 15, 650), text(830, 393, "not from a sharper Hoeffding constant", 15, 650, fill=RED), text(830, 440, "label noise breaks exact consistency", 15, 650), text(830, 480, "M=infinity cannot enter this union bound", 15, 650), text(830, 515, "interpolation alone does not prove realizability。", 15, fill=MUTED)]
    return finish(out, "可实现快率来自零错生存这一特殊事件；一旦有噪声或近似拟合，就必须重新建立比较桥。")


def agnostic_erm():
    out = begin(
        "不可知有限类 ERM：双侧一致收敛的比较桥",
        "噪声下没有零风险版本空间；在覆盖所有 h 的 uniform event 上，把 ERM 输出和类内 oracle 各跨越一次经验—总体间隙，得到 2 alpha 的 class excess 与 1/eps^2 样本尺度。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一共同事件控制所有候选", BLUE)
    out += [rect(55, 95, 290, 92, TEAL, BG, 8, 2), text(200, 128, "E_alpha", 17, 700, "middle", fill=TEAL), text(200, 162, "forall h: |R_S(h)-R_P(h)| <= alpha", 14, 650, "middle")]
    out += [text(45, 250, "contains both", 15, 700, fill=BLUE), text(65, 292, "data-dependent ERM h_hat", 15, 650), text(65, 332, "population oracle h_H*", 15, 650), text(45, 395, "alpha=sqrt(log(2M/delta)/(2m))", 15, 650, cls="math"), text(45, 450, "the event is built before h_hat is selected", 15, 650, fill=RED), text(45, 510, "pointwise control would not cover both objects。", 15, fill=MUTED)]

    heading(out, 430, "B", "逐行走过两次泛化间隙", TEAL)
    steps = (("R_P(h_hat)", RED), ("<= R_S(h_hat)+alpha", BLUE), ("<= R_S(h_H*)+alpha", TEAL), ("<= R_P(h_H*)+2alpha", RED))
    for i, (lab, col) in enumerate(steps):
        y = 80 + i * 100
        node(out, 445, y, 310, 54, lab, col, size=15)
        if i < 3:
            out += [line(600, y + 57, 600, y + 92, INK, 2, marker="a3")]
    out += [text(430, 475, "middle step is the ERM inequality", 15, 650, fill=TEAL), text(430, 510, "first and last steps spend alpha each。", 15, fill=MUTED)]

    heading(out, 830, "C", "风险率与适用边界", RED)
    out += [rect(840, 90, 300, 74, RED, BG, 8, 2), text(990, 120, "R_P(h_hat)-R_H* <= 2 alpha", 16, 700, "middle", fill=RED), text(990, 149, "with probability >= 1-delta", 15, 650, "middle")]
    out += [rect(840, 200, 300, 72, TEAL, BG, 8, 2), text(990, 230, "m >= 2 log(2M/delta) / eps^2", 14, 650, "middle", fill=TEAL), text(990, 257, "suffices for excess <= eps", 15, 700, "middle", fill=TEAL)]
    out += [text(830, 332, "approximate ERM adds optimization rho", 15, 650), text(830, 375, "unbounded loss needs other concentration", 15, 650, fill=RED), text(830, 418, "class excess excludes approximation error", 15, 650), text(830, 461, "1/eps^2 reflects noisy mean comparison", 15, 700, fill=BLUE), text(830, 515, "it is a general scale, not every problem's fate。", 15, fill=MUTED)]
    return finish(out, "不可知 ERM 的证明是一座三步桥：总体输出到经验输出、ERM 比较、经验 oracle 回到总体 oracle。")


def occam_weighted():
    out = begin(
        "Occam 界：用先验权重分配失败预算",
        "可数假设类中给 h 预先分配权重 pi(h)，再令其坏事件预算为 delta pi(h)；prefix-free 编码经 Kraft 不等式给出 pi(h)=2^{-L(h)}，短描述因占用更少 simultaneous-testing 预算而获得较小 penalty。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "非均匀地切分总失败预算", BLUE)
    bars = (("h1", 230, BLUE), ("h2", 150, TEAL), ("h3", 95, RED), ("h4", 60, BLUE))
    for i, (lab, w, col) in enumerate(bars):
        y = 95 + i * 82
        out += [text(45, y + 26, lab, 15, 700), text(82, y + 27, "delta*pi(h)", 13, 650, fill=col), rect(180, y, w * 0.72, 42, col, "#F8FAFC", 5, 2)]
    out += [text(45, 455, "sum_h delta*pi(h) <= delta", 15, 700, fill=BLUE, cls="math"), text(45, 490, "weights must be fixed before evaluation", 15, 650, fill=RED), text(45, 520, "pi is a budget—not posterior truth。", 15, fill=MUTED)]

    heading(out, 430, "B", "编码长度变成复杂度罚项", TEAL)
    codes = (("0", "h1", 1), ("10", "h2", 2), ("110", "h3", 3), ("111", "h4", 3))
    for i, (code, hyp, length) in enumerate(codes):
        y = 95 + i * 78
        out += [rect(445, y, 88, 44, BLUE, BG, 5, 2), text(489, y + 29, code, 16, 700, "middle", fill=BLUE), text(555, y + 29, f"{hyp}: L={length}", 15, 650), text(690, y + 29, f"pi=2^-{length}", 15, 650, fill=TEAL)]
    out += [text(430, 430, "prefix-free -> sum_h 2^{-L(h)} <= 1", 15, 700, fill=TEAL, cls="math"), text(430, 475, "penalty ~ sqrt((L(h) ln2 + ln(1/delta))/m)", 14, 650, fill=RED, cls="math"), text(430, 515, "shorter code receives a tighter certificate。", 15, fill=MUTED)]

    heading(out, 830, "C", "正确解释与常见越界", RED)
    out += [text(830, 105, "valid", 16, 700, fill=TEAL), text(850, 145, "predeclared code / prior", 15, 650), text(850, 182, "countable hypotheses", 15, 650), text(850, 219, "weighted union of bad events", 15, 650)]
    out += [line(830, 250, 1140, 250, GRID, 2), text(830, 295, "invalid shortcut", 16, 700, fill=RED), text(850, 335, "design code after seeing test errors", 15, 650), text(850, 372, "equate compression with causality", 15, 650), text(850, 409, "ignore decoder / metadata / precision", 15, 650), text(830, 465, "MDL, Bayes and PAC-Bayes are related", 15, 650), text(830, 495, "but they are not the same theorem", 15, 700, fill=RED), text(830, 520, "the coding language is part of the contract。", 15, fill=MUTED)]
    return finish(out, "Occam 界奖励的是预先固定语言中的短描述；它是概率预算定理，不是“简单模型必然真实”的哲学捷径。")


def no_free_lunch():
    out = begin(
        "No-Free-Lunch：两个不可区分世界与归纳偏置",
        "训练样本只约束已见点；若允许任意 target labeling，就能构造在样本上完全相同、却在未见点给出相反标签的世界。任何外推规则都必须偏爱某些结构，这就是归纳偏置。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "样本只照亮输入域的一部分", BLUE)
    for i in range(12):
        x = 70 + (i % 4) * 75
        y = 120 + (i // 4) * 90
        seen = i in (0, 2, 5, 7, 8, 10)
        out += [circle(x, y, 18, BLUE if seen else GRID, BLUE if seen else BG, 2.5), text(x, y + 6, "seen" if seen else "?", 12, 700, "middle", fill=BG if seen else MUTED)]
    out += [text(45, 420, "at most m distinct points are observed", 15, 650), text(45, 462, "at least m of 2m points can remain unseen", 15, 650, fill=RED), text(45, 510, "zero training error says nothing there。", 15, fill=MUTED)]

    heading(out, 430, "B", "两个世界在训练集上完全一致", TEAL)
    out += [rect(445, 95, 310, 75, BLUE, BG, 8, 2), text(600, 127, "world f0", 16, 700, "middle", fill=BLUE), text(600, 155, "seen labels: 0 1 1 0 | unseen: 0 0 1", 14, 650, "middle")]
    out += [rect(445, 210, 310, 75, RED, BG, 8, 2), text(600, 242, "world f1", 16, 700, "middle", fill=RED), text(600, 270, "seen labels: 0 1 1 0 | unseen: 1 1 0", 14, 650, "middle")]
    out += [line(600, 289, 600, 330, INK, 2, marker="a3"), rect(485, 342, 230, 62, TEAL, BG, 8, 2), text(600, 379, "same learner output law", 15, 700, "middle", fill=TEAL)]
    out += [text(430, 455, "one prediction must fail in one world", 15, 650, fill=RED), text(430, 490, "averaging finds a fixed hard target", 15, 650), text(430, 520, "the hard distribution remains realizable。", 15, fill=MUTED)]

    heading(out, 830, "C", "学习靠什么打破对称性", RED)
    biases = (("hypothesis class", "exclude arbitrary labels", BLUE), ("representation", "nearby inputs share features", TEAL), ("architecture", "equivariance / locality", RED), ("optimization", "prefer some interpolants", BLUE), ("data protocol", "encode invariance", TEAL))
    for i, (name, desc, col) in enumerate(biases):
        y = 90 + i * 78
        out += [text(830, y, name, 15, 700, fill=col), text(955, y, desc, 13, 600)]
    out += [text(830, 485, "NFL does not say all algorithms tie on reality", 15, 650, fill=RED), text(830, 520, "it says reality must be restricted or biased。", 15, fill=MUTED)]
    return finish(out, "没有无条件外推：模型成功意味着其归纳偏置与现实结构、任务损失和数据机制之间存在可利用的匹配。")


def minimax_lower():
    out = begin(
        "样本复杂度下界：从难分辨世界到 Minimax 风险",
        "上界构造一个可行算法；下界必须让任意算法都失败。Le Cam 用两个统计上接近而最优决策不同的世界，Fano 扩展到多世界 packing，Assouad 把多个二元坐标的困难相加。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先交换正确的量词", BLUE)
    out += [rect(55, 95, 290, 72, TEAL, BG, 8, 2), text(200, 125, "upper bound", 16, 700, "middle", fill=TEAL), text(200, 153, "exists A, for every P: risk is small", 14, 650, "middle")]
    out += [rect(55, 215, 290, 88, RED, BG, 8, 2), text(200, 247, "lower bound", 16, 700, "middle", fill=RED), text(200, 275, "for every A, exists hard P", 14, 650, "middle"), text(200, 296, "such that risk stays large", 14, 650, "middle")]
    out += [text(45, 370, "minimax: inf_A sup_{P in P} E_P loss(A,S)", 14, 700, fill=BLUE, cls="math"), text(45, 430, "hard distribution may depend on A", 15, 650), text(45, 470, "the whole family is fixed by the theorem", 15, 650, fill=RED), text(45, 515, "one bad algorithm proves no lower bound。", 15, fill=MUTED)]

    heading(out, 430, "B", "Le Cam：近分布、远决策", TEAL)
    node(out, 445, 95, 125, 58, "P0^m", BLUE, size=15)
    node(out, 650, 95, 105, 58, "P1^m", RED, size=15)
    out += [path("M575 125C595 105 625 105 645 125", TEAL, 2.5, "none", "7 5"), text(610, 92, "small TV / KL", 14, 700, "middle", fill=TEAL)]
    out += [line(507, 156, 535, 220, GRID, 2, marker="a3"), line(703, 156, 670, 220, GRID, 2, marker="a3")]
    node(out, 455, 232, 135, 58, "action a0", BLUE, size=15)
    node(out, 625, 232, 135, 58, "action a1", RED, size=15)
    out += [text(430, 350, "samples cannot reliably identify the world", 15, 650), text(430, 392, "but optimal actions must be separated", 15, 650, fill=RED), text(430, 445, "testing error -> estimation / excess lower bound", 15, 700, fill=TEAL), text(430, 485, "product closeness dictates useful perturbation", 15, 650), text(430, 515, "indistinguishability is the information bottleneck。", 15, fill=MUTED)]

    heading(out, 830, "C", "从二点到多点与多坐标", RED)
    methods = (("Le Cam", "2 worlds", "binary testing"), ("Fano", "M-world packing", "log M information"), ("Assouad", "hypercube", "sum coordinate errors"))
    for i, (name, worlds, mech) in enumerate(methods):
        y = 90 + i * 115
        out += [rect(840, y, 300, 82, (BLUE, TEAL, RED)[i], BG, 8, 2), text(860, y + 30, name, 16, 700, fill=(BLUE, TEAL, RED)[i]), text(950, y + 30, worlds, 15, 650), text(860, y + 62, mech, 15, 600)]
    out += [text(830, 455, "match lower and upper rates, not constants only", 15, 650), text(830, 490, "state expectation / probability conversion", 15, 650, fill=RED), text(830, 520, "a lower bound belongs to a specified problem class。", 15, fill=MUTED)]
    return finish(out, "下界证明的核心不是展示算法失败，而是构造统计上难分辨、决策上必须分开的世界族，使任何算法都支付不可避免的误差。")


FIGURES = {
    "fig-generalization-concentration-interface-v2.svg": concentration_interface,
    "fig-pac-quantifier-sample-complexity-v2.svg": pac_contract,
    "fig-finite-class-union-uniform-convergence-v2.svg": finite_union,
    "fig-realizable-version-space-survival-v2.svg": realizable_erm,
    "fig-agnostic-erm-two-gap-bridge-v2.svg": agnostic_erm,
    "fig-occam-code-prior-weight-v2.svg": occam_weighted,
    "fig-no-free-lunch-inductive-bias-v2.svg": no_free_lunch,
    "fig-minimax-lower-bound-information-v2.svg": minimax_lower,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
