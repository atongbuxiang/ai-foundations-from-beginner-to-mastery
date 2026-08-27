#!/usr/bin/env python3
"""Generate LT-21--24 textbook figures for VC-theory extensions.

The figures are deterministic proof maps.  They use the shared paper-ink
renderer so typography, palette, spacing, metadata and accessibility match
the rest of the learning-theory volume.
"""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "learning-theory"


def fundamental_theorem():
    out = begin(
        "二分类统计学习基本定理：四种性质的等价地图",
        "对预先固定、满足常规可测性条件的二分类假设类，有限 VC 维、分布无关一致收敛、ERM 可学习与 PAC 可学习在定性上等价；具体样本率取决于 realizable 或 agnostic 设定以及采用的证明路线。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "四个命题不是同一句话", BLUE)
    items = (
        ("finite VC dimension", 55, 95, BLUE),
        ("uniform convergence", 55, 205, TEAL),
        ("ERM PAC learnable", 55, 315, RED),
        ("PAC learnable", 55, 425, BLUE),
    )
    for i, (lab, x, y, col) in enumerate(items):
        node(out, x, y, 290, 58, lab, col, size=15)
        if i < len(items) - 1:
            out += [line(200, y + 61, 200, y + 99, INK, 2, marker="a3")]

    heading(out, 430, "B", "每条箭头有自己的证明任务", TEAL)
    routes = (
        ("VC -> UC", "growth + symmetrization", BLUE),
        ("UC -> ERM", "two-gap comparison", TEAL),
        ("ERM -> PAC", "existence is immediate", RED),
        ("PAC -> finite VC", "shattered-set lower bound", BLUE),
    )
    for i, (name, why, col) in enumerate(routes):
        y = 92 + i * 102
        out += [rect(445, y, 310, 72, col, BG, 8, 2)]
        out += [text(462, y + 29, name, 15, 700, fill=col), text(462, y + 57, why, 15, 600)]
    out += [text(430, 510, "rates and constants are route-specific。", 15, fill=MUTED)]

    heading(out, 830, "C", "率、量词与边界必须另记", RED)
    out += [text(830, 105, "realizable optimal scale", 15, 700, fill=BLUE)]
    out += [text(850, 142, "(d + log(1/delta)) / eps", 15, 650, cls="math")]
    out += [text(830, 195, "agnostic optimal scale", 15, 700, fill=TEAL)]
    out += [text(850, 232, "(d + log(1/delta)) / eps^2", 15, 650, cls="math")]
    out += [line(830, 265, 1140, 265, GRID, 2)]
    out += [text(830, 310, "requires binary 0-1 prediction", 15, 650)]
    out += [text(830, 350, "sample is iid from the target law", 15, 650)]
    out += [text(830, 390, "class is fixed before seeing S", 15, 650)]
    out += [text(830, 430, "measurability is not automatic", 15, 650, fill=RED)]
    out += [text(830, 475, "computation may still be intractable", 15, 650)]
    out += [text(830, 510, "deep nets need additional mechanisms。", 15, fill=MUTED)]
    return finish(out, "基本定理连接容量、估计与可学习性；它不把所有证明路线、数值常数或计算复杂度压成同一件事。")


def structural_risk_minimization():
    out = begin(
        "结构风险最小化：嵌套模型、置信预算与惩罚",
        "把可能具有无限 VC 维的总类写成有限 VC 子类的可数并，为第 k 层分配置信预算 delta pi_k；在共同好事件上比较经验风险加复杂度惩罚，得到 oracle-style 风险账本。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "总类由可控层级组成", BLUE)
    boxes = ((80, 120, 250, 330, "H4", RED), (105, 155, 200, 255, "H3", TEAL), (130, 190, 150, 180, "H2", BLUE), (155, 225, 100, 105, "H1", TEAL))
    for x, y, w, h, lab, col in boxes:
        out += [rect(x, y, w, h, col, "none", 10, 2.5), text(x + 12, y + 25, lab, 15, 700, fill=col)]
    out += [text(45, 485, "H = union_k H_k", 15, 650, cls="math")]
    out += [text(45, 515, "each d_k is finite; union VC may be infinite。", 15, fill=MUTED)]

    heading(out, 430, "B", "为每层预先切分失败预算", TEAL)
    rows = (("H1", "delta*pi_1", 240, BLUE), ("H2", "delta*pi_2", 170, TEAL), ("H3", "delta*pi_3", 105, RED), ("...", "sum pi_k <= 1", 55, BLUE))
    for i, (lab, budget, width, col) in enumerate(rows):
        y = 98 + i * 92
        out += [text(440, y + 27, lab, 15, 700), rect(485, y, width, 42, col, "#F8FAFC", 5, 2), text(740, y + 27, budget, 13, 650, "end", fill=col)]
    out += [text(430, 485, "pen_k uses d_k and log(1/(delta*pi_k))", 14, 650, cls="math")]
    out += [text(430, 515, "weights precede validation。", 15, fill=MUTED)]

    heading(out, 830, "C", "SRM 比较拟合与选择代价", RED)
    out += [rect(840, 92, 300, 78, BLUE, BG, 8, 2)]
    out += [text(990, 122, "score(k,h)", 16, 700, "middle", fill=BLUE), text(990, 153, "= R_S(h) + pen_k", 16, 650, "middle")]
    out += [line(990, 174, 990, 213, INK, 2, marker="a3")]
    out += [rect(840, 225, 300, 92, TEAL, BG, 8, 2)]
    out += [text(990, 257, "choose layer and hypothesis", 15, 700, "middle", fill=TEAL), text(990, 287, "on one simultaneous event", 15, 650, "middle")]
    out += [text(830, 370, "small layer: larger approximation error", 15, 650)]
    out += [text(830, 410, "large layer: larger estimation penalty", 15, 650)]
    out += [text(830, 450, "optimization error must be added", 15, 650, fill=RED)]
    out += [text(830, 485, "nonuniform learnability is h-dependent", 15, 650)]
    out += [text(830, 515, "weaker than one global PAC bound。", 15, fill=MUTED)]
    return finish(out, "SRM 的核心是同一高概率事件上的跨层比较；惩罚是选择账本，不是对复杂模型的道德偏好。")


def multiclass_dimensions():
    out = begin(
        "多分类容量：Natarajan 见证与 Graph 见证",
        "Natarajan 打散要求每个点有两个不同候选标签并实现全部二选一模式；Graph 打散固定一个基准标签函数，只要求任意子集上的标签等于基准、补集上偏离基准。二者在二分类时退化为 VC 维。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Natarajan：逐点二选一", BLUE)
    for i, (x, a, b) in enumerate(((90, "cat", "dog"), (200, "red", "blue"), (310, "A", "B"))):
        out += [circle(x, 145, 12, BLUE, BG, 2), text(x, 115, f"x{i+1}", 15, 700, "middle")]
        out += [rect(x - 42, 185, 84, 42, TEAL, BG, 5, 2), text(x, 212, a, 13, 650, "middle", fill=TEAL)]
        out += [rect(x - 42, 250, 84, 42, RED, BG, 5, 2), text(x, 277, b, 13, 650, "middle", fill=RED)]
    out += [text(45, 350, "for every T: first labels on T", 14, 650)]
    out += [text(45, 385, "second labels outside T", 14, 650)]
    out += [text(45, 445, "two witnesses may vary with the point", 15, 700, fill=BLUE)]
    out += [text(45, 485, "all 2^m binary choices must occur", 14, 650)]
    out += [text(45, 515, "many labels do not prove shattering。", 15, fill=MUTED)]

    heading(out, 430, "B", "Graph：匹配或偏离一个基准", TEAL)
    out += [rect(445, 92, 310, 65, BLUE, BG, 8, 2), text(600, 120, "reference labeling f(x)", 15, 700, "middle", fill=BLUE), text(600, 148, "one fixed label at every x", 14, 650, "middle")]
    for i, x in enumerate((480, 560, 640, 720)):
        col = TEAL if i in (0, 2) else RED
        out += [circle(x, 240, 16, col, BG, 2.5), text(x, 246, "=" if col == TEAL else "!=", 13, 700, "middle", fill=col)]
    out += [text(430, 305, "T: h(x)=f(x)", 15, 650, fill=TEAL)]
    out += [text(430, 342, "outside T: h(x)!=f(x)", 15, 650, fill=RED)]
    out += [text(430, 405, "the alternative label may depend on h and x", 14, 650)]
    out += [text(430, 455, "Natarajan shattering implies Graph shattering", 14, 700, fill=BLUE)]
    out += [text(430, 490, "therefore d_N <= d_G", 16, 700, fill=TEAL, cls="math")]
    out += [text(430, 515, "the reverse needs a label-dependent argument。", 15, fill=MUTED)]

    heading(out, 830, "C", "学习结论不能只换符号", RED)
    out += [text(830, 105, "binary labels", 15, 700, fill=BLUE)]
    out += [text(850, 142, "d_N = d_G = VCdim", 15, 650, cls="math")]
    out += [text(830, 198, "finite label set of size K", 15, 700, fill=TEAL)]
    out += [text(850, 235, "d_N <= d_G = O(d_N log K)", 14, 650, cls="math")]
    out += [line(830, 268, 1140, 268, GRID, 2)]
    out += [text(830, 315, "finite d_N characterizes PAC learnability", 14, 650)]
    out += [text(830, 355, "generic ERM bounds may depend on d_G", 14, 650)]
    out += [text(830, 395, "different ERM tie-breaking can matter", 14, 650, fill=RED)]
    out += [text(830, 435, "structured or huge label spaces need care", 14, 650)]
    out += [text(830, 475, "surrogate loss adds a calibration bridge", 14, 650)]
    out += [text(830, 515, "multiclass is not binary VC with K pasted on。", 15, fill=MUTED)]
    return finish(out, "Natarajan 维刻画逐点的两标签自由度；Graph 维更贴近一致 ERM 的误差图，两者承担不同证明角色。")


def pseudodimension():
    out = begin(
        "伪维：用逐点阈值把实值函数变成二分模式",
        "实值函数类在点 x_i 上配备各自阈值 r_i；若能实现全部高于或低于阈值的模式，则该点集被 pseudo-shatter。等价地，伪维是 subgraph indicator class 在扩展空间 X 乘 R 上的 VC 维。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "每个点有自己的阈值", BLUE)
    xs = (90, 195, 300)
    rs = (230, 175, 275)
    for i, (x, y) in enumerate(zip(xs, rs)):
        out += [line(x, 105, x, 390, GRID, 2), line(x - 32, y, x + 32, y, RED, 3)]
        out += [text(x, 420, f"x{i+1}", 15, 700, "middle"), text(x + 38, y + 6, f"r{i+1}", 13, 650, fill=RED)]
        out += [circle(x, y - 65 if i != 1 else y + 75, 8, BLUE if i != 1 else TEAL, BLUE if i != 1 else TEAL)]
    out += [text(45, 470, "bit_i = 1{f(x_i) > r_i}", 16, 700, fill=BLUE, cls="math")]
    out += [text(45, 515, "one shared threshold is weaker。", 15, fill=MUTED)]

    heading(out, 430, "B", "等价的 subgraph 分类类", TEAL)
    out += [line(465, 405, 745, 405, GRID, 2), line(465, 90, 465, 405, GRID, 2)]
    out += [path("M470 350C520 315 555 330 600 255C645 180 690 205 745 125", BLUE, 3)]
    out += [path("M470 405L470 350C520 315 555 330 600 255C645 180 690 205 745 125L745 405Z", "none", 0, "#EFF6FF")]
    for x, y, col in ((500, 335, TEAL), (550, 280, RED), (620, 305, TEAL), (700, 160, RED)):
        out += [circle(x, y, 7, col, col)]
    out += [text(430, 455, "G_f(x,r)=1{r < f(x)}", 16, 700, fill=TEAL, cls="math")]
    out += [text(430, 490, "Pdim(F)=VCdim({G_f:f in F})", 15, 650, cls="math")]
    out += [text(430, 515, "domain expands to X times R。", 15, fill=MUTED)]

    heading(out, 830, "C", "从容量到风险还需损失合同", RED)
    out += [rect(840, 92, 300, 70, BLUE, BG, 8, 2), text(990, 122, "finite Pdim(F)", 16, 700, "middle", fill=BLUE), text(990, 150, "controls threshold patterns", 14, 650, "middle")]
    out += [line(990, 166, 990, 202, INK, 2, marker="a3")]
    out += [rect(840, 214, 300, 78, TEAL, BG, 8, 2), text(990, 244, "bounded range / bounded loss", 15, 700, "middle", fill=TEAL), text(990, 273, "+ concentration or covering", 14, 650, "middle")]
    out += [line(990, 296, 990, 332, INK, 2, marker="a3")]
    out += [rect(840, 344, 300, 72, RED, BG, 8, 2), text(990, 374, "uniform risk guarantee", 15, 700, "middle", fill=RED), text(990, 403, "with an explicit scale", 14, 650, "middle")]
    out += [text(830, 462, "unbounded squared or log loss needs tails", 14, 650, fill=RED)]
    out += [text(830, 490, "fat-shattering keeps the accuracy scale", 14, 650)]
    out += [text(830, 515, "finite Pdim is not a tail bound。", 15, fill=MUTED)]
    return finish(out, "伪维只把实值自由度转成组合容量；要控制真实损失，还必须说明范围、尾部、尺度与复合步骤。")


FIGURES = {
    "fig-binary-learning-fundamental-theorem-v2.svg": fundamental_theorem,
    "fig-srm-nested-classes-penalty-v2.svg": structural_risk_minimization,
    "fig-multiclass-natarajan-graph-v2.svg": multiclass_dimensions,
    "fig-pseudodimension-threshold-subgraph-v2.svg": pseudodimension,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
