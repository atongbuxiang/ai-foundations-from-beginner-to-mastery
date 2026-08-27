#!/usr/bin/env python3
"""Generate v2 textbook figures for the four foundational information notes."""

from __future__ import annotations

import math
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


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "information-theory"


def polyline(points, color, width=2.5, dash=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, color, width, "none", dash)


def self_information():
    out = begin(
        "自信息、熵与前缀码长度",
        "小概率结果有更大负对数惊讶度；entropy 是按真实概率加权的平均自信息；Kraft 条件把概率长度与可译码二进制前缀码连接起来。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "结果越罕见，自信息越大", BLUE)
    out += [line(55, 390, 355, 390, GRID, 2), line(70, 420, 70, 95, GRID, 2)]
    pts = []
    for i in range(1, 121):
        p = 0.02 + 0.98 * i / 120
        x = 70 + 275 * p
        y = 390 - 75 * (-math.log(p, 2))
        pts.append((x, max(110, y)))
    out.append(polyline(pts, BLUE, 3))
    out += [
        text(205, 125, "i(x) = -log_2 p(x)", 17, 700, "middle", cls="math"),
        text(335, 420, "p", 15, 650),
        text(52, 112, "bits", 15, 650),
        circle(97, 245, 6, RED, RED),
        circle(318, 378, 6, TEAL, TEAL),
        text(45, 455, "同一结果的 surprise 取决于所用模型。", 15, fill=MUTED),
        text(45, 488, "独立概率相乘 -> 信息相加。", 15, fill=RED),
    ]

    heading(out, 430, "B", "熵是分布上的加权平均", TEAL)
    probs = (0.50, 0.25, 0.125, 0.125)
    for i, p in enumerate(probs):
        x = 455 + i * 72
        h = 210 * p / 0.5
        out += [rect(x, 350 - h, 42, h, TEAL, BG, 2, 2), text(x + 21, 380, f"x{i+1}", 15, 650, "middle")]
        surprise = -math.log(p, 2)
        out.append(circle(x + 21, 125 + surprise * 42, 5, BLUE, BLUE))
    out += [
        text(430, 105, "点：-log p_i", 15, 650, fill=BLUE),
        text(430, 420, "H(X) = sum_i p_i[-log p_i]", 17, 650, cls="math"),
        text(430, 460, "realization 有不同 surprise；entropy 只有一个平均值。", 15, fill=MUTED),
        text(430, 493, "均匀分布在固定有限 support 上达到最大熵。", 15, fill=RED),
    ]

    heading(out, 830, "C", "前缀树把码长变成可译码约束", RED)
    root = (900, 120)
    out.append(circle(*root, 10, INK, INK))
    out += [line(895, 130, 850, 215, BLUE, 2.5), line(905, 130, 1020, 215, BLUE, 2.5)]
    out += [line(1015, 235, 970, 325, TEAL, 2.5), line(1025, 235, 1080, 325, TEAL, 2.5)]
    out += [
        circle(850, 225, 9, RED, BG, 2.5),
        circle(1020, 225, 9, INK, INK, 2.5),
        circle(970, 335, 9, TEAL, BG, 2.5),
        circle(1080, 335, 9, TEAL, BG, 2.5),
        text(872, 170, "0", 15, 700, "middle", BLUE),
        text(960, 170, "1", 15, 700, "middle", BLUE),
        text(980, 282, "0", 15, 700, "middle", TEAL),
        text(1058, 282, "1", 15, 700, "middle", TEAL),
        text(850, 255, "x1: 0", 15, 700, "middle"),
        text(970, 367, "x2: 10", 15, 700, "middle"),
        text(1080, 367, "x3: 11", 15, 700, "middle"),
    ]
    out += [
        text(830, 400, "Kraft: sum_i 2^(-l_i) <= 1", 17, 650, cls="math"),
        text(830, 440, "H_2(X) <= L < H_2(X)+1", 17, 650, cls="math"),
        text(830, 480, "ideal length 可为实数；单符号码长必须为整数。", 15, fill=MUTED),
    ]
    return finish(out, "负对数连接概率乘法与长度加法；entropy 是平均理想长度，前缀码再加入可译码约束。")


def entropy_chain():
    out = begin(
        "联合熵、条件熵与链式编码",
        "描述一对变量可以一次联合编码，也可以先编码 X 再按 X 选择 Y 的条件码；序列重复这一分解，得到 autoregressive likelihood 与 token NLL。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一次描述联合结果", BLUE)
    labels = (("x1,y1", 0.42), ("x1,y2", 0.08), ("x2,y1", 0.12), ("x2,y2", 0.38))
    for i, (lab, p) in enumerate(labels):
        x = 55 + (i % 2) * 145
        y = 110 + (i // 2) * 110
        out += [rect(x, y, 125, 80, BLUE, BG, 6, 2), text(x + 62, y + 31, lab, 15, 650, "middle"), text(x + 62, y + 60, f"p={p:.2f}", 15, 650, "middle", TEAL)]
    out += [
        text(45, 365, "i(x,y) = -log p(x,y)", 17, 650, cls="math"),
        text(45, 407, "H(X,Y) = E[i(X,Y)]", 17, 650, cls="math"),
        text(45, 458, "两个变量不代表两份独立信息。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "分阶段描述完全等价", TEAL)
    node(out, 450, 110, 120, 52, "encode X", BLUE, size=16)
    node(out, 630, 110, 130, 52, "encode Y | X", TEAL, size=16)
    out += [line(573, 136, 625, 136, INK, 2.5, marker="a3")]
    out += [
        text(430, 220, "p(x,y)=p(x)p(y|x)", 17, 650, cls="math"),
        text(430, 266, "-log p(x,y)", 17, 650, cls="math"),
        text(430, 302, "= -log p(x) - log p(y|x)", 17, 650, cls="math"),
        line(440, 340, 760, 340, GRID, 2),
        text(430, 390, "H(X,Y) = H(X) + H(Y|X)", 18, 700, cls="math"),
        text(430, 438, "H(Y|X) 是对 X 的加权平均，不是固定 x 的单值。", 15, fill=MUTED),
        text(430, 477, "离散情形：H(Y|X) <= H(Y)。", 15, fill=RED),
    ]

    heading(out, 830, "C", "序列链式法则就是逐 token 预测", RED)
    xs = (840, 910, 980, 1050, 1120)
    for i, x in enumerate(xs):
        node(out, x, 115, 48, 46, f"X{i+1}" if i < 4 else "XT", BLUE if i == 0 else TEAL, size=15)
        if i < len(xs) - 1:
            out.append(line(x + 49, 138, xs[i + 1] - 5, 138, INK, 2, marker="a3"))
    out += [
        text(830, 225, "p(x_1:T)=product_t p(x_t|x_<t)", 16, 650, cls="math"),
        text(830, 275, "H(X_1:T)=sum_t H(X_t|X_<t)", 16, 650, cls="math"),
        text(830, 330, "token NLL 要声明 mask、EOS 与 reduction。", 15, fill=MUTED),
        text(830, 380, "条件箭头描述 factorization，", 16, 650),
        text(830, 415, "本身不是因果方向。", 16, 650, fill=RED),
    ]
    return finish(out, "概率链式分解经负对数与期望，精确变成联合、条件与序列 entropy 的加法。")


def cross_entropy_kl():
    out = begin(
        "交叉熵、KL 方向与支持失配",
        "数据由 P 加权而用 Q 的码长评分，得到 cross-entropy；它分解为不可约 entropy 与失配 KL；KL 的方向和支持关系决定惩罚形态与是否有限。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "P 产生数据，Q 提供码长", BLUE)
    pvals = (0.48, 0.30, 0.16, 0.06)
    qvals = (0.22, 0.28, 0.31, 0.19)
    for i, (p, q) in enumerate(zip(pvals, qvals)):
        x = 55 + i * 72
        out += [rect(x, 345 - 210 * p / 0.5, 25, 210 * p / 0.5, BLUE, BG, 1, 2), rect(x + 29, 345 - 210 * q / 0.5, 25, 210 * q / 0.5, TEAL, BG, 1, 2)]
        out.append(text(x + 27, 378, f"x{i+1}", 15, 650, "middle"))
    out += [
        text(45, 105, "P weight", 15, 700, fill=BLUE),
        text(135, 105, "Q score", 15, 700, fill=TEAL),
        text(45, 420, "H(P,Q)=E_P[-log q(X)]", 17, 650, cls="math"),
        text(45, 460, "外层 expectation 在 P；log 内评价 Q。", 15, fill=MUTED),
        text(45, 492, "q(x)=0 且 p(x)>0 -> infinite cost", 15, fill=RED),
    ]

    heading(out, 430, "B", "交叉熵 = 不可约项 + 失配项", TEAL)
    out += [rect(450, 155, 165, 70, BLUE, BG, 5, 2), rect(615, 155, 130, 70, RED, BG, 5, 2)]
    out += [
        text(532, 195, "H(P)", 20, 700, "middle", BLUE),
        text(680, 195, "KL(P||Q)", 17, 700, "middle", RED),
        text(600, 275, "H(P,Q) = H(P) + D_KL(P||Q)", 17, 700, "middle", cls="math"),
        text(430, 335, "固定 P 时：min_Q cross-entropy", 16, 650),
        text(430, 372, "等价于 min_Q KL(P||Q)。", 16, 650),
        text(430, 425, "经验 NLL 是样本平均；总体结论还需泛化。", 15, fill=MUTED),
        text(430, 468, "KL>=0，但不是距离 metric。", 15, fill=RED),
    ]

    heading(out, 830, "C", "方向改变“漏模态”与“追模态”", RED)
    out += [line(840, 320, 1140, 320, GRID, 2), line(855, 345, 855, 95, GRID, 2)]
    p1 = []
    q1 = []
    for i in range(121):
        x = 855 + 2.3 * i
        p = math.exp(-0.5 * ((x - 925) / 28) ** 2) + 0.85 * math.exp(-0.5 * ((x - 1060) / 34) ** 2)
        q = 1.15 * math.exp(-0.5 * ((x - 1040) / 48) ** 2)
        p1.append((x, 320 - 135 * p))
        q1.append((x, 320 - 135 * q))
    out += [polyline(p1, BLUE, 3), polyline(q1, TEAL, 3, "8 5")]
    out += [
        text(870, 118, "P: two modes", 15, 700, fill=BLUE),
        text(1060, 155, "Q", 15, 700, fill=TEAL),
        text(830, 380, "KL(P||Q): P-weighted; missing P support is severe", 15, 650),
        text(830, 420, "KL(Q||P): Q-weighted; can prefer one mode", 15, 650),
        text(830, 465, "图示是优化倾向，不是普遍有限样本定理。", 15, fill=MUTED),
    ]
    return finish(out, "交叉熵的 expectation 方向、KL 的参数顺序与支持覆盖必须在每次应用中显式核对。")


def mutual_information():
    out = begin(
        "互信息、PMI 与独立基线",
        "互信息比较真实 joint 与保持 marginals 的 product baseline；PMI 是单个格子的有符号 log-ratio，MI 是 joint 加权平均；entropy reduction 给出同一量的预测解释。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Joint 与 product baseline 比较", BLUE)
    joint = ((0.34, 0.06, 0.02), (0.05, 0.28, 0.05), (0.01, 0.07, 0.12))
    for r, row in enumerate(joint):
        for c, val in enumerate(row):
            x, y = 60 + c * 82, 105 + r * 82
            color = BLUE if r == c else TEAL
            out += [rect(x, y, 66, 66, color, BG, 3, 2), text(x + 33, y + 39, f"{val:.2f}", 15, 650, "middle")]
    out += [
        text(45, 390, "baseline = P_X P_Y", 17, 650, cls="math"),
        text(45, 430, "I(X;Y)=KL(P_XY || P_X P_Y)", 16, 650, cls="math"),
        text(45, 475, "baseline 保留 marginals，只移除依赖。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "PMI 可正可负，MI 是平均", TEAL)
    node(out, 445, 110, 135, 58, "PMI > 0", BLUE, size=17)
    node(out, 625, 110, 135, 58, "PMI < 0", RED, size=17)
    out += [
        text(512, 205, "joint 比独立更常见", 15, 650, "middle", BLUE),
        text(692, 205, "joint 比独立更少见", 15, 650, "middle", RED),
        line(470, 285, 740, 285, GRID, 2),
        circle(500, 285, 7, RED, RED),
        circle(555, 285, 7, BLUE, BLUE),
        circle(610, 285, 7, RED, RED),
        circle(665, 285, 7, BLUE, BLUE),
        circle(720, 285, 7, BLUE, BLUE),
        text(600, 330, "joint-weighted average", 15, 650, "middle"),
        text(430, 385, "PMI(x;y)=log p(x,y)/[p(x)p(y)]", 16, 650, cls="math"),
        text(430, 425, "I(X;Y)=E_XY[PMI(X;Y)] >= 0", 16, 650, cls="math"),
        text(430, 468, "平均非负不表示每个局部证据非负。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "等价于观察后减少的 entropy", RED)
    out += [rect(845, 125, 270, 58, BLUE, BG, 4, 2), rect(845, 230, 165, 58, TEAL, BG, 4, 2)]
    out += [
        text(980, 161, "H(X)", 18, 700, "middle", BLUE),
        text(928, 266, "H(X|Y)", 18, 700, "middle", TEAL),
        line(1015, 210, 1115, 210, RED, 3),
        text(1065, 201, "I(X;Y)", 16, 700, "middle", RED),
        text(830, 345, "I = H(X)-H(X|Y) = H(Y)-H(Y|X)", 16, 650, cls="math"),
        text(830, 390, "I=0 iff independent（离散/良好情形）。", 15, 650),
        text(830, 432, "能检测非线性统计依赖；", 16, 650),
        text(830, 468, "不提供因果方向，也不保证易估计。", 16, 650, fill=RED),
    ]
    return finish(out, "互信息同时是 joint-to-product KL、平均 PMI 与 entropy reduction；三种表示共享同一 joint。")


FIGURES = {
    "fig-self-information-entropy-code-length-v2.svg": self_information,
    "fig-joint-conditional-entropy-chain-rule-v2.svg": entropy_chain,
    "fig-cross-entropy-kl-v2.svg": cross_entropy_kl,
    "fig-mutual-information-dependence-v2.svg": mutual_information,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
