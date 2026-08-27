#!/usr/bin/env python3
"""Generate LT-69--72 textbook-style online-learning figures deterministically."""
from pathlib import Path
from plot_calculus_operator_figures_v2 import (
    BLUE, TEAL, AMBER, RED, INK, MUTED, GRID, BG,
    begin, finish, heading, line, path, node, text, circle, rect,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def online_protocol():
    out = begin(
        "Online Protocol：时序先于 Regret",
        "逐轮可见信息决定可实现算法；累计损失必须与预先声明的 comparator class 比较。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一轮中的信息时序", BLUE)
    stages = ((55, "history H(t-1)", BLUE), (155, "choose w(t)", TEAL),
              (255, "reveal loss(t)", RED), (355, "feedback", BLUE))
    for i, (y, lab, col) in enumerate(stages):
        node(out, 65, y + 35, 270, 48, lab, col, size=16)
        if i < len(stages) - 1:
            out.append(line(200, y + 86, 200, y + 126, INK, 2.3, marker="a3"))
    out.append(text(55, 500, "关键：选择当前 action 时看不到当前 loss。", 15, fill=MUTED))

    heading(out, 430, "B", "两条累计损失轨道", TEAL)
    out.append(text(445, 112, "learner", 17, 700, fill=BLUE))
    learner = (0.18, 0.62, 0.34, 0.82, 0.47, 0.69)
    expert = (0.32, 0.38, 0.42, 0.48, 0.53, 0.59)
    x0, dx, base, scale = 455, 48, 340, 215
    pts_l, pts_e = [], []
    for i, (a, b) in enumerate(zip(learner, expert)):
        x = x0 + i * dx
        pts_l.append((x, base - a * scale)); pts_e.append((x, base - b * scale))
    out.append(path("M" + "L".join(f"{x} {y}" for x, y in pts_l), BLUE, 3))
    out.append(path("M" + "L".join(f"{x} {y}" for x, y in pts_e), TEAL, 3, dash="7 5"))
    for x, y in pts_l: out.append(circle(x, y, 4, BLUE, BLUE))
    for x, y in pts_e: out.append(circle(x, y, 4, TEAL, TEAL))
    out += [line(445, 355, 755, 355, GRID, 1.5),
            text(445, 390, "R(T) = learner cumulative loss", 16, 650),
            text(445, 420, "        - best fixed hindsight loss", 16, 650),
            text(445, 458, "best fixed ≠ best action at every round", 15, fill=RED),
            text(445, 492, "regret may be negative", 15, fill=MUTED)]

    heading(out, 830, "C", "先声明 Feedback 与 Benchmark", RED)
    pairs = (("full information", "all losses", BLUE),
             ("gradient", "local first order", TEAL),
             ("bandit", "chosen loss only", RED),
             ("delayed", "arrives later", AMBER))
    for i, (a, b, col) in enumerate(pairs):
        y = 95 + 78 * i
        node(out, 840, y, 135, 48, a, col, size=15)
        out.append(line(980, y + 24, 1010, y + 24, INK, 2, marker="a3"))
        out.append(text(1022, y + 30, b, 15, fill=INK))
    node(out, 840, 420, 300, 55, "static / dynamic / policy regret", RED, size=15)
    out.append(text(840, 508, "协议改变，定理对象随之改变。", 15, fill=MUTED))
    return finish(out, "先画信息时序，再写 comparator 与概率量词，最后才选择算法和 regret bound。")


def hedge_potential():
    out = begin(
        "Hedge：指数权重与势能夹逼",
        "每轮指数惩罚累积损失；同一总权重的专家下界与 learner 上界夹出 regret。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "loss 进入指数权重", BLUE)
    names = ("expert 1", "expert 2", "expert 3")
    losses = ("0", "1", "1/2")
    widths = (245, 120, 174)
    for i, (name, loss, width) in enumerate(zip(names, losses, widths)):
        y = 100 + 105 * i
        out.append(text(55, y, name, 15, 650))
        out.append(rect(55, y + 15, width, 34, BLUE if i == 0 else TEAL, "#EFF6FF" if i == 0 else "#ECFDF5", 5, 1.8))
        out.append(text(320, y + 40, f"loss={loss}", 15, fill=MUTED))
    out += [text(55, 445, "w(t+1,i) = w(t,i) exp(-eta loss(t,i))", 16, 650),
            text(55, 483, "normalize weights → p(t)", 16, fill=TEAL)]

    heading(out, 430, "B", "log-potential 的上下夹逼", TEAL)
    node(out, 445, 105, 310, 62, "lower: log pi(i) - eta L(T,i)", BLUE, size=15)
    out.append(line(600, 172, 600, 210, INK, 2.2, marker="a3"))
    node(out, 445, 222, 310, 72, "log W(T+1)", TEAL, size=18)
    out.append(line(600, 298, 600, 336, INK, 2.2, marker="a3"))
    node(out, 445, 348, 310, 68, "upper: -eta L_hat + eta^2 T / 8", RED, size=15)
    out += [text(445, 460, "Hoeffding lemma requires loss in [0,1]", 15, fill=MUTED),
            text(445, 492, "same potential, two viewpoints", 15, 650, fill=TEAL)]

    heading(out, 830, "C", "复杂度—学习率平衡", RED)
    out += [line(860, 410, 1135, 410, GRID, 1.5), line(880, 435, 880, 105, GRID, 1.5),
            path("M900 125C930 180 955 270 1010 330C1050 375 1090 395 1130 402", BLUE, 3),
            path("M900 402C960 385 1020 330 1070 250C1100 205 1120 160 1130 125", RED, 3),
            path("M900 170C960 250 1010 286 1050 292C1090 298 1110 280 1130 245", TEAL, 3),
            text(900, 100, "log N / eta", 15, 650, fill=BLUE),
            text(1045, 100, "eta T / 8", 15, 650, fill=RED),
            text(955, 320, "sum", 15, 650, fill=TEAL),
            text(1015, 455, "eta* = sqrt(8 log N / T)", 15, 650, "middle"),
            text(1015, 490, "regret = O(sqrt(T log N))", 15, fill=MUTED, anchor="middle")]
    return finish(out, "Multiplicative update 是算法表面；log-potential 夹逼才是可迁移的证明骨架。")


def ogd_omd_geometry():
    out = begin(
        "OGD 与 OMD：势能下降和几何选择",
        "Euclidean projection 产生平方距离 telescope；mirror map 把同一证明搬到 Bregman 与 dual-norm 几何。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "OGD：先走一步，再投影", BLUE)
    out += [path("M70 390C90 150 290 110 345 355Z", TEAL, 3, "#ECFDF5"),
            circle(145, 285, 7, BLUE, BLUE), circle(310, 190, 7, RED, RED), circle(265, 245, 7, TEAL, TEAL),
            line(145, 285, 310, 190, RED, 3, marker="a2"),
            line(310, 190, 265, 245, TEAL, 3, marker="a1"),
            text(122, 315, "w(t)", 15, fill=BLUE),
            text(280, 175, "w(t)-eta g(t)", 15, fill=RED),
            text(245, 274, "w(t+1)", 15, fill=TEAL),
            text(55, 450, "projection: feasible + nonexpansive", 15, fill=MUTED),
            text(55, 488, "potential: ||w(t)-u||^2", 16, 650)]

    heading(out, 430, "B", "单步式到 Telescope", TEAL)
    node(out, 445, 102, 310, 65, "convexity: loss gap <= <g,w-u>", BLUE, size=15)
    out.append(line(600, 172, 600, 204, INK, 2.2, marker="a3"))
    node(out, 430, 216, 340, 84, "potential drop / eta + eta ||g||^2 / 2", TEAL, size=15)
    out.append(line(600, 304, 600, 337, INK, 2.2, marker="a3"))
    node(out, 445, 350, 310, 65, "R(T) <= D^2/(2 eta) + eta G^2 T/2", RED, size=15)
    out += [text(445, 460, "eta = D/(G sqrt T)", 16, 650),
            text(445, 492, "R(T) <= D G sqrt T", 16, 700, fill=TEAL)]

    heading(out, 830, "C", "Mirror Map 选择坐标系", RED)
    node(out, 840, 105, 300, 55, "primal w --gradient--> dual", BLUE, size=15)
    out.append(line(990, 165, 990, 202, INK, 2.2, marker="a3"))
    node(out, 840, 214, 300, 58, "dual step: grad psi(w)-eta g", TEAL, size=15)
    out.append(line(990, 277, 990, 314, INK, 2.2, marker="a3"))
    node(out, 840, 326, 300, 58, "map back / Bregman projection", RED, size=15)
    out += [text(840, 430, "Euclidean: l2 / l2", 15, fill=BLUE),
            text(840, 463, "simplex entropy: l1 / l-infinity", 15, fill=TEAL),
            text(840, 500, "geometry changes dimension dependence", 15, fill=MUTED)]
    return finish(out, "OGD 与 OMD 共享势能证明；mirror map 决定什么距离、什么 gradient bound 最自然。")


def adversary_filtration():
    out = begin(
        "随机、Oblivious 与 Adaptive Sequence",
        "filtration 精确标记谁在何时看到 learner 的历史、fresh coin 与当前 action。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "四种数据生成合同", BLUE)
    rows = (("iid", "fresh sample ⟂ history", BLUE),
            ("random order", "without replacement", TEAL),
            ("oblivious", "whole sequence pre-fixed", AMBER),
            ("adaptive", "depends on past history", RED))
    for i, (a, b, col) in enumerate(rows):
        y = 100 + i * 88
        node(out, 55, y, 145, 48, a, col, size=15)
        out.append(line(205, y + 24, 235, y + 24, INK, 2, marker="a3"))
        out.append(text(247, y + 30, b, 15))
    out.append(text(55, 478, "random ≠ independent; adversarial ≠ deterministic", 15, fill=MUTED))

    heading(out, 430, "B", "Filtration 与 Fresh Coin", TEAL)
    xs = (450, 535, 620, 705)
    labs = ("F(t-1)", "p(t)", "U(t)", "I(t)")
    cols = (BLUE, TEAL, AMBER, RED)
    for i, (x, lab, col) in enumerate(zip(xs, labs, cols)):
        node(out, x, 130, 68, 48, lab, col, size=15)
        if i < 3: out.append(line(x + 69, 154, xs[i + 1] - 5, 154, INK, 2, marker="a3"))
    out += [text(445, 220, "non-anticipating loss(t)", 16, 650, fill=TEAL),
            line(445, 238, 755, 238, TEAL, 3),
            text(445, 278, "may use F(t-1)", 15),
            text(445, 313, "must not use current U(t) or I(t)", 15, fill=RED)]
    node(out, 445, 355, 310, 65, "if loss sees I(t): standard proof can fail", RED, size=15)
    out.append(text(445, 466, "measurability is the theorem boundary", 15, fill=MUTED))

    heading(out, 830, "C", "Expectation 到 Realized Path", RED)
    node(out, 840, 105, 300, 58, "mixture loss <p(t), loss(t)>", BLUE, size=15)
    out.append(line(990, 168, 990, 205, INK, 2.2, marker="a3"))
    node(out, 840, 217, 300, 68, "D(t)=sampled loss - mixture loss", TEAL, size=15)
    out.append(line(990, 290, 990, 327, INK, 2.2, marker="a3"))
    node(out, 840, 339, 300, 58, "E[D(t)|F(t-1)] = 0", BLUE, size=15)
    out += [text(840, 438, "Azuma: bounded increments", 15, fill=TEAL),
            text(840, 470, "Freedman: conditional variance", 15, fill=TEAL),
            text(840, 505, "then obtain high-probability regret", 15, fill=MUTED)]
    return finish(out, "概率结论不是装饰：fresh randomness、可见性和条件期望共同决定证明是否成立。")


FIGURES = {
    "fig-online-protocol-regret-v2.svg": online_protocol,
    "fig-hedge-potential-v2.svg": hedge_potential,
    "fig-ogd-omd-geometry-v2.svg": ogd_omd_geometry,
    "fig-adversary-filtration-v2.svg": adversary_filtration,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, factory in FIGURES.items():
        target = OUT / name
        target.write_text(factory(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
