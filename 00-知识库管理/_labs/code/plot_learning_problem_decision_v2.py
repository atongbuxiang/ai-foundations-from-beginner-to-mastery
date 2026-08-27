#!/usr/bin/env python3
"""Generate LT-01--08 v2 textbook figures for learning problems and risk."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def learning_contract():
    out = begin("统计学习问题的七对象合同", "观测空间、未知分布、采样机制、假设空间、学习算法、损失和目标风险组成可检验的学习问题；计算张量和经验指标不能替代其中任何一层。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "世界与观测先于模型", BLUE)
    node(out, 55, 95, 290, 58, "population law P on Z=X×Y", BLUE, size=14)
    out += [line(200, 156, 200, 194, INK, 2, marker="a3")]
    node(out, 55, 205, 290, 66, "sampling protocol -> S=(Z1,...,Zm)", TEAL, size=14)
    out += [line(200, 274, 200, 312, INK, 2, marker="a3")]
    node(out, 55, 324, 290, 62, "observed dataset s", RED, size=15)
    out += [text(45, 440, "random sample S != realized dataset s", 14, 650), text(45, 475, "raw object -> observation -> encoding", 14, 650, fill=RED), text(45, 505, "each arrow can discard task-relevant information。", 14, fill=MUTED)]

    heading(out, 430, "B", "算法从样本选择预测器", TEAL)
    node(out, 445, 95, 140, 58, "sample S", BLUE)
    node(out, 650, 95, 115, 58, "h_S in H", TEAL)
    out += [line(588, 124, 645, 124, INK, 2.3, marker="a3"), text(616, 109, "learner A", 14, 650, "middle")]
    out += [line(705, 156, 705, 203, INK, 2, marker="a3")]
    node(out, 445, 216, 320, 62, "prediction action h_S(x) in A", RED, size=14)
    out += [text(430, 340, "parameter theta is a representation", 14, 650), text(430, 375, "hypothesis class H is a function set", 14, 650), text(430, 410, "algorithm A includes randomness / stopping", 14, 650, fill=RED), text(430, 472, "same H, different A -> different output law", 14, 650), text(430, 505, "proper / improper must be stated。", 14, fill=MUTED)]

    heading(out, 830, "C", "损失定义目标，风险定义验收", RED)
    node(out, 840, 90, 300, 58, "loss ell(action, outcome)", RED, size=14)
    out += [line(990, 151, 990, 188, INK, 2, marker="a3")]
    node(out, 840, 200, 300, 66, "R_P(h)=E_P ell(h(X),Y)", TEAL, size=14)
    out += [line(990, 269, 990, 306, INK, 2, marker="a3")]
    node(out, 840, 318, 300, 66, "claim: excess / gap / utility", BLUE, size=14)
    out += [text(830, 438, "target population and loss fix what 'best' means", 14, 650), text(830, 473, "confidence probability needs its random source", 14, 650, fill=RED), text(830, 505, "training success is not a complete claim。", 14, fill=MUTED)]
    return finish(out, "先固定对象、随机性与目标，再讨论模型和算法；合同不完整时，所谓泛化保证没有统一语义。")


def sampling_contract():
    out = begin("边缘同分布、i.i.d. 联合律与有效样本单位", "相同边缘分布不推出独立；i.i.d. 要求联合律分解为 P 的乘积。增强 views、同一用户记录与时间序列共享潜变量，浓缩与切分必须以真正独立的 sampling unit 为准。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "同边缘不等于独立联合律", BLUE)
    for x in (85, 155, 225, 295):
        out += [circle(x, 160, 20, BLUE, BG, 2), text(x, 166, "P", 15, 700, "middle", fill=BLUE)]
    out += [text(45, 220, "each Z_i ~ P", 16, 700), text(45, 258, "but coupling may be arbitrary", 15, 650, fill=RED)]
    out += [circle(200, 330, 25, RED, BG, 2), text(200, 336, "U", 15, 700, "middle", fill=RED)]
    for x in (90, 165, 235, 310):
        out += [line(200, 355, x, 410, GRID, 2), circle(x, 420, 8, TEAL, TEAL)]
    out += [text(45, 485, "shared latent U creates dependence", 14, 650), text(45, 512, "identical marginals can be perfectly correlated。", 14, fill=MUTED)]

    heading(out, 430, "B", "i.i.d. 是整个 joint law", TEAL)
    node(out, 445, 92, 310, 62, "S=(Z1,...,Zm) ~ P^m", TEAL, size=15)
    out += [text(430, 210, "P(Z1 in B1,...,Zm in Bm)", 15, 650, cls="math"), text(430, 246, "= product_i P(Z_i in B_i)", 15, 700, fill=TEAL, cls="math")]
    for i, x in enumerate((475, 555, 635, 715)):
        out += [circle(x, 330, 18, BLUE, BG, 2), text(x, 336, f"Z{i+1}", 14, 650, "middle", fill=BLUE)]
    out += [text(430, 410, "fresh draw for every sampling unit", 14, 650), text(430, 448, "exchangeable / without replacement / mixing", 14, 650, fill=RED), text(430, 480, "need different concentration tools", 14, 650), text(430, 510, "independence is an assumption, not a file format。", 14, fill=MUTED)]

    heading(out, 830, "C", "增强与切分按父样本分组", RED)
    for x in (875, 990, 1105):
        out += [circle(x, 135, 16, BLUE, BLUE), line(x, 153, x-25, 220, GRID, 2), line(x, 153, x+25, 220, GRID, 2), circle(x-25, 230, 8, TEAL, TEAL), circle(x+25, 230, 8, TEAL, TEAL)]
    out += [text(830, 290, "two views share the same parent", 14, 650, fill=RED), text(830, 328, "split parents / users / time blocks first", 14, 650), text(830, 372, "duplicates do not multiply independent n", 14, 650), text(830, 420, "variance includes covariance terms", 14, 650, fill=RED), text(830, 462, "report nominal m and effective sample size", 14, 650), text(830, 505, "leakage invalidates the target experiment。", 14, fill=MUTED)]
    return finish(out, "泛化定理作用于联合采样合同；增强数量、文件行数与真正独立样本量是三种不同计数。")


def predictor_class_learner():
    out = begin("参数表示、函数类与学习算法三层地图", "参数经表示映射产生预测函数且常多对一；假设空间是允许输出的函数集合；学习算法从随机样本和随机种子选择函数。同一函数类上的不同算法可以有不同输出分布和泛化。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "参数空间到函数空间常多对一", BLUE)
    for x, lab in ((80, "theta1"), (170, "theta2"), (260, "theta3")):
        node(out, x, 110, 78, 48, lab, BLUE, size=14)
    node(out, 120, 250, 180, 66, "same predictor h", TEAL, size=15)
    out += [line(119, 161, 170, 245, GRID, 2, marker="a3"), line(209, 161, 210, 245, GRID, 2, marker="a3"), line(299, 161, 250, 245, GRID, 2, marker="a3")]
    out += [text(45, 380, "Phi: Theta -> H need not be injective", 14, 650), text(45, 420, "permutation / scaling symmetries", 14, 650, fill=RED), text(45, 468, "parameter count != number of functions", 14, 650), text(45, 508, "parameter distance != prediction distance。", 14, fill=MUTED)]

    heading(out, 430, "B", "假设空间是函数集合", TEAL)
    out += [path("M455 350C480 110 725 90 760 350Z", TEAL, 2.5, "#ECFDF5")]
    for x, y in ((505, 180), (600, 150), (690, 205), (550, 285), (660, 300)):
        out += [path(f"M{x-25} {y+12}Q{x} {y-25} {x+25} {y+8}", BLUE, 2)]
    out += [text(605, 385, "H subset of A^X", 16, 700, "middle", fill=TEAL), text(430, 430, "architecture / constraints define candidates", 14, 650), text(430, 465, "data-dependent H changes the proof object", 14, 650, fill=RED), text(430, 505, "capacity belongs to functions, not filenames。", 14, fill=MUTED)]

    heading(out, 830, "C", "Learner 选择函数并带随机性", RED)
    node(out, 840, 90, 120, 54, "sample S", BLUE)
    node(out, 1020, 90, 120, 54, "seed U", RED)
    node(out, 900, 220, 180, 62, "algorithm A", TEAL)
    out += [line(900, 147, 950, 215, GRID, 2, marker="a3"), line(1080, 147, 1030, 215, GRID, 2, marker="a3"), line(990, 285, 990, 325, INK, 2, marker="a3")]
    node(out, 870, 338, 240, 62, "random output h_{S,U}", BLUE, size=14)
    out += [text(830, 450, "optimizer / early stop / regularizer are in A", 14, 650), text(830, 480, "same H, different A -> different stability", 14, 650, fill=RED), text(830, 510, "learnability and computability remain separate。", 14, fill=MUTED)]
    return finish(out, "参数是表示，H 是候选函数集合，A 是数据依赖选择规则；三层必须分别声明与分析。")


def risk_ledger():
    out = begin("Loss、population risk、empirical risk 与 data dependence", "Loss 编码单次行动代价；population risk 是目标分布期望，empirical risk 是有限样本平均。固定预测器时经验风险可无偏，但用同一数据选择 h_S 后，选择偏差需要统一控制或独立评价。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "Loss 把动作与结果变成代价", BLUE)
    node(out, 55, 95, 130, 56, "action a", BLUE)
    node(out, 245, 95, 120, 56, "outcome y", TEAL)
    node(out, 105, 220, 210, 68, "ell(a,y)", RED)
    out += [line(120, 154, 170, 215, GRID, 2, marker="a3"), line(305, 154, 250, 215, GRID, 2, marker="a3"), text(45, 350, "0-1 -> posterior mode", 14, 650), text(45, 385, "square -> conditional mean", 14, 650), text(45, 420, "absolute -> conditional median", 14, 650), text(45, 460, "log loss -> full conditional law", 14, 650, fill=RED), text(45, 505, "changing loss changes the optimal decision。", 14, fill=MUTED)]

    heading(out, 430, "B", "总体风险与经验风险分账", TEAL)
    node(out, 445, 92, 310, 66, "R_P(h)=E_P ell(h(X),Y)", TEAL, size=14)
    node(out, 445, 235, 310, 66, "R_S(h)=m^{-1} sum_i ell(h(X_i),Y_i)", BLUE, size=14)
    out += [line(600, 162, 600, 228, INK, 2, "7 5"), text(620, 202, "generalization gap", 14, 650, fill=RED), text(430, 365, "P: target population, usually unknown", 14, 650), text(430, 402, "S: realized training sample", 14, 650), text(430, 448, "test estimate is a third random object", 14, 650, fill=RED), text(430, 505, "mean / sum / weights change the estimand。", 14, fill=MUTED)]

    heading(out, 830, "C", "固定 h 与 h_S 的量词不同", RED)
    node(out, 840, 88, 300, 60, "fixed h before seeing S", BLUE, size=14)
    out += [line(990, 151, 990, 188, INK, 2, marker="a3")]
    node(out, 840, 200, 300, 60, "E_S R_S(h) = R_P(h)", TEAL, size=14)
    out += [line(990, 263, 990, 300, INK, 2, marker="a3")]
    node(out, 840, 312, 300, 64, "learner picks h_S using same S", RED, size=14)
    out += [text(830, 425, "pointwise unbiasedness does not survive selection", 14, 650, fill=RED), text(830, 460, "need uniform control / stability / fresh test", 14, 650), text(830, 505, "zero train risk alone says nothing about R_P。", 14, fill=MUTED)]
    return finish(out, "风险理论的裂缝不在期望公式本身，而在预测器是否依赖用于估计它的同一份数据。")


def erm_decomposition():
    out = begin("ERM、类内最优与超额风险分解", "Bayes optimum、class optimum、empirical ERM 与 computed output 是四个对象；超额风险需分为 target mismatch、approximation、estimation/selection 与 optimization，而 approximate ERM 的类内风险由两侧泛化间隙和优化容差控制。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "四个最优对象不能合并", BLUE)
    levels = (("Bayes h* in F", BLUE), ("class oracle h_H*", TEAL), ("empirical ERM h_hat", RED), ("computed output h_tilde", BLUE))
    for i, (lab, col) in enumerate(levels):
        y = 82 + i * 92
        node(out, 55, y, 290, 54, lab, col, size=14)
        if i < 3: out.append(line(200, y+57, 200, y+84, INK, 2, marker="a3"))
    out += [text(45, 478, "each argmin may fail to exist", 14, 650, fill=RED), text(45, 507, "infimum and returned iterate are different。", 14, fill=MUTED)]

    heading(out, 430, "B", "风险预算按来源相加", TEAL)
    out += [text(430, 110, "R_target(h_tilde)-R_target*", 15, 700, cls="math"), line(430, 132, 760, 132, GRID, 2)]
    budgets = (("target mismatch", "deployment P != training target", RED), ("approximation", "R_P(h_H*) - R_P*", BLUE), ("selection", "R_P(h_hat) - R_P(h_H*)", TEAL), ("optimization", "R_S(h_tilde)-inf_H R_S", RED))
    for i, (name, desc, col) in enumerate(budgets):
        y = 175 + i * 78
        out += [text(430, y, name, 15, 700, fill=col), text(575, y, desc, 14, 600)]
    out += [text(430, 505, "regularization can move several ledgers at once。", 14, fill=MUTED)]

    heading(out, 830, "C", "Approximate ERM 的桥", RED)
    node(out, 840, 88, 300, 58, "R_S(h_tilde) <= inf_H R_S + rho", RED, size=14)
    out += [line(990, 149, 990, 190, INK, 2, marker="a3")]
    out += [rect(840, 202, 300, 80, TEAL, BG, 8, 2), text(990, 234, "class excess <=", 14, 650, "middle", fill=TEAL), text(990, 264, "2 sup_h |R_P(h)-R_S(h)| + rho", 14, 650, "middle", fill=TEAL)]
    out += [text(830, 340, "two gaps: output and class comparator", 14, 650), text(830, 375, "uniform convergence is sufficient, not necessary", 14, 650, fill=RED), text(830, 420, "optimization tolerance rho is empirical", 14, 650), text(830, 462, "population difference may have either sign", 14, 650), text(830, 505, "train loss descent closes only one ledger。", 14, fill=MUTED)]
    return finish(out, "ERM 连接可计算目标与总体目标，但风险结论必须同时交付比较器、泛化控制和优化容差。")


def bayes_decision():
    out = begin("Conditional law、loss 与 Bayes action", "Bayes predictor 在每个 x 上最小化 conditional risk；不同 loss 从同一条件分布读取不同最优 action。Bayes risk 依赖 observation、action space 和 loss，不是脱离任务的永恒噪声下界。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "先条件化，再逐点决策", BLUE)
    node(out, 55, 90, 290, 56, "joint law P(X,Y)", BLUE, size=14)
    out += [line(200, 149, 200, 184, INK, 2, marker="a3")]
    node(out, 55, 196, 290, 60, "conditional law P(Y|X=x)", TEAL, size=14)
    out += [line(200, 259, 200, 294, INK, 2, marker="a3")]
    node(out, 55, 306, 290, 64, "r(a|x)=E[ell(a,Y)|X=x]", RED, size=14)
    out += [line(200, 373, 200, 408, INK, 2, marker="a3")]
    node(out, 55, 420, 290, 62, "h*(x) in argmin_a r(a|x)", BLUE, size=14)
    out += [text(45, 514, "measurability / existence need conditions。", 14, fill=MUTED)]

    heading(out, 430, "B", "同一条件律，不同 loss", TEAL)
    rows = (("0-1 / cost", "mode / shifted threshold", BLUE), ("square", "conditional mean", TEAL), ("absolute", "conditional median", RED), ("log loss", "full conditional distribution", BLUE))
    for i, (loss, action, col) in enumerate(rows):
        y = 102 + i * 92
        out += [text(430, y, loss, 15, 700, fill=col), line(540, y-5, 585, y-5, GRID, 2, marker="a3"), text(600, y, action, 14, 650)]
    out += [text(430, 475, "posterior estimation and decision are separate", 14, 650, fill=RED), text(430, 510, "calibration matters through downstream loss。", 14, fill=MUTED)]

    heading(out, 830, "C", "Bayes risk 是任务相对下界", RED)
    node(out, 840, 90, 300, 62, "R* = inf_h R_P(h)", RED, size=15)
    out += [text(830, 215, "change observation X -> change information", 14, 650), text(830, 255, "change action A -> change feasible decisions", 14, 650), text(830, 295, "change loss ell -> change what counts as error", 14, 650), text(830, 345, "label ambiguity != irreducible causal uncertainty", 14, 650, fill=RED), text(830, 390, "Bayes predictor != Bayesian parameter prior", 14, 650), text(830, 435, "oracle rule still requires unknown P", 14, 650), text(830, 505, "estimated Bayes risk is not automatically exact。", 14, fill=MUTED)]
    return finish(out, "Bayes 决策是已知 P 时的 oracle；真正决定最优动作的是条件分布与损失的组合。")


def realizable_learnable():
    out = begin("Realizable、agnostic、consistency 与 PAC 的量词轴", "Realizable/agnostic 是世界与比较器假设；empirical/statistical consistency 是拟合或渐近性质；PAC 是统一有限样本高概率保证。它们与 computational efficiency 处在不同轴上。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "世界假设轴", BLUE)
    out += [rect(55, 110, 290, 72, BLUE, BG, 8, 2), text(200, 139, "realizable", 14, 700, "middle", fill=BLUE), text(200, 166, "exists h* in H with R_P(h*)=0", 14, 650, "middle", fill=BLUE)]
    out += [rect(55, 260, 290, 72, TEAL, BG, 8, 2), text(200, 289, "agnostic", 14, 700, "middle", fill=TEAL), text(200, 316, "compare to inf_{h in H} R_P(h)", 14, 650, "middle", fill=TEAL)]
    out += [text(45, 390, "realizable is a distribution-class relation", 14, 650), text(45, 430, "interpolation on S is only empirical", 14, 650, fill=RED), text(45, 475, "well specified != optimizer success", 14, 650), text(45, 510, "label leakage can fake realizability。", 14, fill=MUTED)]

    heading(out, 430, "B", "保证时间轴", TEAL)
    out += [line(470, 390, 745, 390, GRID, 2), line(470, 390, 470, 105, GRID, 2), text(610, 430, "sample size m", 15, 650, "middle"), text(445, 120, "risk", 15, 650, "middle")]
    out += [path("M480 145C540 230 610 295 745 330", TEAL, 3), path("M480 170C565 250 650 275 745 285", BLUE, 2.5, "none", "7 5")]
    out += [text(500, 150, "finite PAC envelope", 14, 650, fill=BLUE), text(600, 350, "asymptotic consistency", 14, 650, fill=TEAL), text(430, 475, "pointwise rate need not be distribution-uniform", 14, 650, fill=RED), text(430, 510, "convergence mode and comparator must be named。", 14, fill=MUTED)]

    heading(out, 830, "C", "PAC 与 computation 分开", RED)
    out += [rect(840, 88, 300, 72, RED, BG, 8, 2), text(990, 117, "for all P, eps, delta", 14, 650, "middle", fill=RED), text(990, 144, "m >= m_H(eps,delta)", 14, 650, "middle", fill=RED)]
    out += [line(990, 163, 990, 198, INK, 2, marker="a3")]
    out += [rect(840, 210, 300, 72, TEAL, BG, 8, 2), text(990, 239, "Pr_S[R_P(A(S))-comp <= eps]", 14, 650, "middle", fill=TEAL), text(990, 266, ">= 1-delta", 14, 650, "middle", fill=TEAL)]
    out += [text(830, 340, "existence of learner", 15, 700, fill=BLUE), text(830, 375, "polynomial sample complexity", 15, 700, fill=TEAL), text(830, 410, "polynomial-time implementation", 15, 700, fill=RED), text(830, 455, "optimizer reaches required solution", 14, 650), text(830, 505, "four claims do not imply each other automatically。", 14, fill=MUTED)]
    return finish(out, "先定位世界假设与时间量词，再谈 learner 和 computation；零训练误差、相合与 PAC 不是同义词。")


def evaluation_feedback():
    out = begin("Train、validation、test 与自适应反馈", "数据集角色由信息流决定：train 拟合候选，validation 选择 pipeline，独立 final test 只在冻结后评价。结果若反馈进开发，holdout 就进入 learner，必须支付选择复杂度或重置独立测试。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "三份数据是三种信息角色", BLUE)
    node(out, 55, 88, 120, 54, "train", BLUE)
    node(out, 225, 88, 140, 54, "candidate models", TEAL, size=14)
    node(out, 55, 220, 120, 54, "validation", TEAL)
    node(out, 225, 220, 140, 54, "selected pipeline", RED, size=14)
    out += [line(178, 115, 220, 115, INK, 2, marker="a3"), line(178, 247, 220, 247, INK, 2, marker="a3"), line(295, 145, 295, 213, GRID, 2, marker="a3"), text(45, 350, "validation belongs to the meta-learner", 14, 650), text(45, 390, "preprocessing and checkpoint rules count", 14, 650, fill=RED), text(45, 435, "retraining changes the final fitted object", 14, 650), text(45, 505, "names of folders do not define independence。", 14, fill=MUTED)]

    heading(out, 430, "B", "冻结后，final test 才评价", TEAL)
    node(out, 445, 100, 150, 60, "frozen pipeline", BLUE, size=14)
    node(out, 645, 100, 110, 60, "final test", TEAL, size=14)
    out += [line(598, 130, 640, 130, INK, 2, marker="a3")]
    node(out, 510, 245, 190, 66, "reported estimate", RED, size=14)
    out += [line(700, 163, 630, 240, GRID, 2, marker="a3"), text(430, 370, "conditional on the frozen model", 14, 650), text(430, 405, "fresh test average can be unbiased", 14, 650, fill=TEAL), text(430, 448, "distribution shift remains a separate threat", 14, 650, fill=RED), text(430, 505, "one test set answers one target protocol。", 14, fill=MUTED)]

    heading(out, 830, "C", "反馈回路把 test 变成训练信号", RED)
    node(out, 840, 90, 140, 56, "developer", BLUE)
    node(out, 1020, 90, 120, 56, "leaderboard", RED, size=14)
    out += [line(983, 118, 1015, 118, INK, 2, marker="a3"), path("M1080 150C1090 260 915 270 905 150", RED, 2.5, "none", "7 5", "a2")]
    out += [text(830, 300, "adaptive queries make final h depend on test", 14, 650, fill=RED), text(830, 345, "fixed K candidates -> pay log K", 14, 650), text(830, 382, "adaptive reuse -> control information / privacy", 14, 650), text(830, 425, "or collect a new untouched test set", 14, 650), text(830, 470, "group/time leakage changes the sampling unit", 14, 650), text(830, 505, "benchmark saturation is a statistical event。", 14, fill=MUTED)]
    return finish(out, "评估可信度来自信息隔离与目标分布合同；一旦结果反馈，holdout 就成为学习算法的输入。")


FIGURES = {
    "fig-learning-problem-object-contract-v2.svg": learning_contract,
    "fig-sampling-joint-law-dependence-v2.svg": sampling_contract,
    "fig-predictor-class-learner-v2.svg": predictor_class_learner,
    "fig-loss-population-empirical-risk-v2.svg": risk_ledger,
    "fig-erm-excess-risk-ledger-v2.svg": erm_decomposition,
    "fig-bayes-conditional-risk-action-v2.svg": bayes_decision,
    "fig-realizable-consistency-learnability-v2.svg": realizable_learnable,
    "fig-train-validation-test-feedback-v2.svg": evaluation_feedback,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
