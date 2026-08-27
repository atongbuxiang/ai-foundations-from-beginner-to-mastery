#!/usr/bin/env python3
"""Generate LT-73--76 textbook-style online/boosting/bandit figures."""
from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    BLUE, TEAL, AMBER, RED, INK, MUTED, GRID, BG,
    begin, finish, heading, line, path, node, text, circle, rect,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def perceptron():
    out = begin("Perceptron：Margin 与 Mistake 双账本",
                "错误更新既沿 separator 取得线性进展，又只让权重范数平方根增长。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "错误样本触发几何更新", BLUE)
    out += [line(70, 380, 350, 125, TEAL, 3),
            line(70, 350, 350, 350, GRID, 1.5), line(180, 440, 180, 95, GRID, 1.5),
            circle(130, 295, 7, BLUE, BLUE), circle(245, 205, 7, RED, RED),
            line(130, 295, 245, 205, RED, 3, marker="a2"),
            text(92, 320, "w(k)", 15, fill=BLUE), text(245, 190, "w(k)+y x", 15, fill=RED),
            text(255, 135, "separator u", 15, fill=TEAL),
            text(55, 432, "update only if y<w,x> <= 0", 15, 650),
            text(55, 470, "each mistake adds >= gamma progress", 15, fill=MUTED)]

    heading(out, 430, "B", "线性下界撞上平方根上界", TEAL)
    out += [line(455, 410, 760, 410, GRID, 1.5), line(475, 435, 475, 105, GRID, 1.5),
            path("M480 400L745 130", TEAL, 3),
            path("M480 400C525 300 610 235 745 190", BLUE, 3),
            circle(650, 226, 7, RED, RED),
            text(675, 205, "intersection", 15, fill=RED),
            text(625, 135, "M gamma", 16, 700, fill=TEAL),
            text(630, 280, "R sqrt(M)", 16, 700, fill=BLUE),
            text(445, 455, "M gamma <= <w,u> <= ||w|| <= R sqrt(M)", 15, 650),
            text(445, 492, "therefore M <= (R/gamma)^2", 16, 700, fill=RED)]

    heading(out, 830, "C", "结论与边界必须分账", RED)
    rows = (("separable + margin", "finite mistakes", TEAL),
            ("noise / contradiction", "violation term", RED),
            ("kernel feature space", "same proof", BLUE),
            ("population risk", "needs conversion", AMBER))
    for i, (a, b, col) in enumerate(rows):
        y = 100 + i * 84
        node(out, 840, y, 160, 48, a, col, size=15)
        out.append(line(1005, y + 24, 1030, y + 24, INK, 2, marker="a3"))
        out.append(text(1040, y + 30, b, 15))
    out += [text(840, 458, "scale invariant: R/gamma", 15, 650),
            text(840, 492, "finite mistakes ≠ max margin", 15, fill=MUTED)]
    return finish(out, "证明只有三步：margin progress、norm growth、Cauchy；每一步都对应一个不可省略的假设。")


def boosting():
    out = begin("AdaBoost：弱边、重加权与指数势能",
                "样本分布驱动弱规则；归一化常数同时记录指数损失和训练错误上界。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "一轮重加权回路", BLUE)
    pts = ((195, 110, "D(t)", BLUE), (305, 220, "h(t)", TEAL),
           (195, 340, "alpha(t)", AMBER), (82, 220, "D(t+1)", RED))
    for x, y, lab, col in pts:
        out.append(circle(x, y, 38, col, BG, 2.5)); out.append(text(x, y + 6, lab, 15, 700, "middle", col))
    out += [path("M225 135C265 150 285 175 295 195", INK, 2.3, marker="a3"),
            path("M295 248C280 285 250 315 225 325", INK, 2.3, marker="a3"),
            path("M165 325C125 305 105 270 98 250", INK, 2.3, marker="a3"),
            path("M98 190C110 150 145 125 165 115", INK, 2.3, marker="a3"),
            text(55, 420, "wrong samples multiply by exp(+alpha)", 15, fill=RED),
            text(55, 454, "correct samples multiply by exp(-alpha)", 15, fill=TEAL),
            text(55, 490, "weak learner must win on every D(t)", 15, 650)]

    heading(out, 430, "B", "Z(t) 是势能收缩率", TEAL)
    node(out, 445, 100, 310, 58, "epsilon(t) = 1/2 - gamma(t)", BLUE, size=15)
    out.append(line(600, 163, 600, 198, INK, 2.2, marker="a3"))
    node(out, 445, 210, 310, 62, "Z(t)=2 sqrt(epsilon(1-epsilon))", TEAL, size=15)
    out.append(line(600, 277, 600, 312, INK, 2.2, marker="a3"))
    node(out, 430, 324, 340, 72, "mean exp(-y F(T,x)) = product Z(t)", BLUE, size=15)
    out += [text(445, 444, "training error <= exp(-2 sum gamma(t)^2)", 15, 700, fill=RED),
            text(445, 482, "zero edge -> no contraction", 15, fill=MUTED)]

    heading(out, 830, "C", "证据阶梯与失效模式", RED)
    rows = (("1", "positive edge", BLUE), ("2", "training exp loss", TEAL),
            ("3", "margin distribution", AMBER), ("4", "test generalization", RED))
    for i, (k, lab, col) in enumerate(rows):
        y = 100 + i * 80
        out.append(circle(865, y + 22, 20, col, BG, 2)); out.append(text(865, y + 28, k, 15, 700, "middle", col))
        out.append(line(890, y + 22, 920, y + 22, INK, 2, marker="a3")); out.append(text(932, y + 28, lab, 16, 650))
    node(out, 840, 430, 300, 55, "label noise attracts exponential weight", RED, size=15)
    out.append(text(840, 512, "training theorem is not a test theorem", 15, fill=MUTED))
    return finish(out, "AdaBoost 的可验证主线是 D(t) → edge → Z(t) → exponential loss；泛化与噪声另开账户。")


def online_batch():
    out = begin("Online-to-Batch：从 Fresh Example 到 Population Risk",
                "history-measurable predictor 与当前 iid 样本的条件独立，把 online loss 变成 risk observation。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "Test-then-Train 时序", BLUE)
    stages = ((75, "past Z(1:t-1)", BLUE), (180, "build h(t)", TEAL),
              (285, "fresh Z(t)", AMBER), (390, "score, then update", RED))
    for i, (y, lab, col) in enumerate(stages):
        node(out, 60, y, 290, 50, lab, col, size=15)
        if i < 3: out.append(line(205, y + 54, 205, y + 98, INK, 2.2, marker="a3"))
    out += [text(55, 478, "E[loss(h(t),Z(t)) | F(t-1)] = L(h(t))", 15, 650),
            text(55, 510, "train-then-test on Z(t) breaks freshness", 15, fill=RED)]

    heading(out, 430, "B", "平均保证对应什么输出？", TEAL)
    rows = (("random iterate", "always valid in expectation", BLUE),
            ("prediction average", "needs convexity + Jensen", TEAL),
            ("last iterate", "needs extra structure", RED))
    for i, (a, b, col) in enumerate(rows):
        y = 105 + i * 105
        node(out, 445, y, 145, 52, a, col, size=15)
        out.append(line(595, y + 26, 625, y + 26, INK, 2, marker="a3"))
        out.append(text(637, y + 32, b, 15))
    out += [text(445, 448, "B(T)/T turns regret scale into risk scale", 15, 650),
            text(445, 484, "existence of a good iterate is not selection", 15, fill=MUTED)]

    heading(out, 830, "C", "概率与 Comparator 双桥", RED)
    node(out, 840, 105, 300, 55, "online loss -> average risk", BLUE, size=15)
    out.append(line(990, 165, 990, 198, INK, 2.2, marker="a3"))
    node(out, 840, 210, 300, 55, "regret -> fixed comparator loss", TEAL, size=15)
    out.append(line(990, 270, 990, 303, INK, 2.2, marker="a3"))
    node(out, 840, 315, 300, 55, "comparator empirical -> population", AMBER, size=15)
    out += [text(840, 412, "martingale + fixed-function concentration", 15, 650),
            text(840, 450, "data-selected comparator needs more", 15, fill=RED),
            text(840, 486, "dependence / drift changes the target", 15, fill=MUTED)]
    return finish(out, "Regret 除以 T 只是数值步骤；freshness、输出规则和 concentration 才完成统计对象的转换。")


def bandit_rl():
    out = begin("Bandit Feedback 与 RL：可见性、估计和状态",
                "未选 action 的 loss 缺失导致探索和 inverse propensity；state transition 则把问题推进到 RL。",
                (BLUE, TEAL, RED))
    heading(out, 42, "A", "Feedback Ladder", BLUE)
    rows = (("experts", "all action losses", BLUE),
            ("bandit", "chosen loss only", RED),
            ("contextual", "context + chosen loss", TEAL))
    for i, (a, b, col) in enumerate(rows):
        y = 105 + i * 105
        node(out, 55, y, 130, 52, a, col, size=15)
        out.append(line(190, y + 26, 220, y + 26, INK, 2, marker="a3"))
        out.append(text(232, y + 32, b, 15))
    out += [text(55, 447, "less feedback -> active exploration", 15, 650),
            text(55, 483, "unselected outcomes are counterfactual", 15, fill=MUTED)]

    heading(out, 430, "B", "IPS：无偏与方差同源", TEAL)
    node(out, 445, 105, 310, 55, "sample I(t) from p(t)", BLUE, size=15)
    out.append(line(600, 165, 600, 198, INK, 2.2, marker="a3"))
    node(out, 445, 210, 310, 65, "loss_hat(i)=1{I=i} loss(i) / p(i)", TEAL, size=15)
    out.append(line(600, 280, 600, 313, INK, 2.2, marker="a3"))
    node(out, 445, 325, 310, 55, "E loss_hat(i) = loss(i)", BLUE, size=15)
    out += [text(445, 423, "second moment = loss(i)^2 / p(i)", 15, 650, fill=RED),
            text(445, 459, "small p: large variance", 15, fill=RED),
            text(445, 493, "p=0: no identification", 15, fill=MUTED)]

    heading(out, 830, "C", "Horizon 1 到 Stateful RL", RED)
    node(out, 840, 95, 300, 48, "bandit: action -> immediate reward", BLUE, size=15)
    out.append(line(990, 148, 990, 183, INK, 2.2, marker="a3"))
    node(out, 840, 195, 300, 58, "MDP: state, action, reward, next state", TEAL, size=15)
    out.append(line(990, 258, 990, 293, INK, 2.2, marker="a3"))
    node(out, 840, 305, 300, 58, "return + credit + occupancy", RED, size=15)
    out += [text(840, 408, "offline: propensity + overlap", 15, 650),
            text(840, 444, "deployment: safety constraints", 15, 650, fill=RED),
            text(840, 483, "low regret ≠ safe exploration", 15, fill=MUTED)]
    return finish(out, "先按反馈可见性选择 estimator，再按 action 是否改变未来 state 决定 bandit 还是 RL。")


FIGURES = {
    "fig-perceptron-margin-mistakes-v2.svg": perceptron,
    "fig-boosting-weak-strong-exp-loss-v2.svg": boosting,
    "fig-online-to-batch-conversion-v2.svg": online_batch,
    "fig-bandit-rl-interface-v2.svg": bandit_rl,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, factory in FIGURES.items():
        target = OUT / name
        target.write_text(factory(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
