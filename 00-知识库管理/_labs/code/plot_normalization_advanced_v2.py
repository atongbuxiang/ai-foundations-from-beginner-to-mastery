#!/usr/bin/env python3
"""Generate deterministic NN-37--40 normalization textbook figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def rmsnorm_geometry():
    out = begin(
        "RMSNorm Geometry：少一个中心化投影",
        "LayerNorm 先删除共同平移再归一半径；RMSNorm 直接按原点半径归一，因此保留均值方向，并在 VJP 中少一个 mean-removal 项。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一输入，两条几何路径", BLUE)
    node(out, 52, 105, 78, 48, "x", BLUE)
    node(out, 170, 88, 174, 52, "LN: subtract mean", TEAL, size=15)
    node(out, 170, 185, 174, 52, "RMS: keep mean", BLUE, size=15)
    out += [line(134, 125, 165, 113, TEAL, 2.3, marker="a1"),
            line(134, 135, 165, 210, BLUE, 2.3, marker="a0")]
    node(out, 90, 295, 255, 54, "normalize radius", RED, size=16)
    out += [line(257, 144, 217, 290, TEAL, 2.2, marker="a1"),
            line(257, 241, 242, 290, BLUE, 2.2, marker="a0")]
    out += [text(50, 405, "LN removes: shift + radial", 16, 700, fill=TEAL),
            text(50, 438, "RMS removes: radial only", 16, 700, fill=BLUE),
            text(50, 476, "kept degrees: D-2  vs  D-1", 16, 650, fill=RED)]

    heading(out, 430, "B", "超平面交球面 vs 整个球面", TEAL)
    cx, cy, rad = 600, 286, 132
    out += [circle(cx, cy, rad, GRID, "none", 2),
            line(455, 430, 748, 150, TEAL, 2.5, "8 6"),
            text(735, 138, "1-perp", 15, 700, "end", TEAL)]
    out += [path("M507 380C548 421 653 419 696 377", BLUE, 4),
            text(600, 455, "RMS: whole sphere", 16, 700, "middle", BLUE)]
    out += [circle(521, 370, 8, TEAL, TEAL, 2),
            circle(678, 187, 8, TEAL, TEAL, 2),
            text(600, 112, "LN: intersection with 1-perp", 15, 700, "middle", TEAL)]
    out += [line(cx, cy, 690, 380, BLUE, 2.5, marker="a0"),
            text(697, 397, "mean kept", 15, 650, fill=BLUE)]

    heading(out, 830, "C", "VJP 的一个缺项", RED)
    node(out, 845, 102, 285, 56, "u = gamma * g", BLUE, size=16)
    node(out, 845, 202, 285, 70, "LN: u - mean(u) - h mean(uh)", TEAL, size=15)
    node(out, 845, 318, 285, 70, "RMS: u - h mean(uh)", BLUE, size=15)
    out += [line(987, 162, 987, 197, INK, 2, marker="a3"),
            line(987, 277, 987, 313, INK, 2, marker="a3")]
    out += [text(987, 432, "LN: sum(dx)=0", 16, 700, "middle", TEAL),
            text(987, 464, "RMS: x dot dx=0 if eps=0", 15, 700, "middle", BLUE)]
    return finish(out, "RMSNorm 保留共同均值方向；少一次 centering，就是少删除一个自由度。")


def normalization_family_lattice():
    out = begin(
        "Normalization Family：统计轴与参数对象",
        "InstanceNorm 与 GroupNorm 在卷积张量上改变统计集合；GroupNorm 的两个极端只保证统计核心对应；WeightNorm 则作用于权重方向而非 activation。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "N C H W 上的统计组", BLUE)
    rows = (
        ("BN", "fix C", "reduce N,H,W", BLUE),
        ("IN", "fix N,C", "reduce H,W", TEAL),
        ("GN", "fix N,G", "reduce C/G,H,W", RED),
    )
    for idx, (name, fixed, reduced, color) in enumerate(rows):
        y = 105 + idx * 112
        out += [text(52, y + 31, name, 20, 700, fill=color),
                rect(98, y, 92, 48, color, BG, 5, 2),
                text(144, y + 30, fixed, 15, 650, "middle", color),
                line(196, y + 24, 224, y + 24, INK, 2, marker="a3"),
                rect(230, y, 138, 48, color, "#F8FAFC", 5, 2),
                text(299, y + 30, reduced, 15, 650, "middle", color)]
    out += [text(52, 455, "same formula shell", 15, 650, fill=MUTED),
            text(52, 482, "different dependency graph", 16, 700, fill=RED)]

    heading(out, 430, "B", "GN 极端：统计同，合同未必同", TEAL)
    node(out, 445, 115, 90, 62, "G = 1", TEAL)
    node(out, 575, 115, 90, 62, "...", BLUE)
    node(out, 705, 115, 70, 62, "G = C", RED)
    out += [line(539, 146, 570, 146, INK, 2, marker="a3"),
            line(669, 146, 700, 146, INK, 2, marker="a3")]
    out += [text(490, 223, "stats like LN(C,H,W)", 15, 650, "middle", TEAL),
            text(738, 223, "stats like IN", 15, 650, "middle", RED)]
    checks = (("GN affine", "per channel"), ("LN affine", "per element"),
              ("IN state", "optional"), ("GN state", "none"))
    for idx, (left, right) in enumerate(checks):
        y = 292 + idx * 48
        out += [text(445, y, left, 15, 700, fill=BLUE),
                text(765, y, right, 15, 600, "end", MUTED),
                line(442, y + 10, 770, y + 10, GRID, 1)]

    heading(out, 830, "C", "WeightNorm：对象换成参数", RED)
    cx, cy, rad = 990, 265, 118
    out += [circle(cx, cy, rad, GRID, "none", 2),
            line(cx, cy, 1065, 180, BLUE, 3, marker="a0"),
            circle(1065, 180, 7, BLUE, BLUE, 2),
            text(1080, 174, "v direction", 15, 700, fill=BLUE)]
    out += [line(cx, cy, 1115, 123, TEAL, 3, marker="a1"),
            text(1122, 118, "w = g v / ||v||", 15, 700, "end", TEAL)]
    out += [rect(845, 405, 285, 72, RED, "#FFF5F2", 5, 2),
            text(987, 433, "no activation statistics", 16, 700, "middle", RED),
            text(987, 459, "no minibatch companions", 15, 600, "middle", MUTED)]
    return finish(out, "先问被归一的是 activation group 还是 weight direction；名称相近不代表对象相同。")


def pre_post_jacobian():
    out = begin(
        "Pre-Norm vs Post-Norm：恒等铁路与归一化闸门",
        "Pre-Norm 把归一化放入残差分支，Jacobian 显式含 identity rail；Post-Norm 对残差和整体归一，使 identity 与 branch 一起经过 normalization Jacobian。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "前向：Norm 在分叉前还是合流后", BLUE)
    node(out, 50, 105, 72, 46, "x", BLUE)
    node(out, 165, 90, 74, 46, "N", TEAL)
    node(out, 280, 90, 74, 46, "F", RED)
    out += [line(126, 126, 160, 113, TEAL, 2.3, marker="a1"),
            line(243, 113, 275, 113, RED, 2.3, marker="a2"),
            path("M86 154V235H318", BLUE, 2.8, "none", None, "a0"),
            line(318, 140, 318, 230, RED, 2.3, marker="a2"),
            circle(318, 235, 7, INK, BG, 2),
            text(200, 278, "Pre: x + F(N(x))", 16, 700, "middle", BLUE)]
    node(out, 50, 335, 72, 46, "x", BLUE)
    node(out, 165, 322, 74, 46, "F", RED)
    out += [path("M86 384V432H250", BLUE, 2.8, "none", None, "a0"),
            line(126, 358, 160, 345, RED, 2.3, marker="a2"),
            line(202, 372, 202, 427, RED, 2.3, marker="a2"),
            circle(250, 432, 7, INK, BG, 2)]
    node(out, 280, 407, 74, 50, "N", TEAL)
    out += [line(258, 432, 275, 432, TEAL, 2.3, marker="a1"),
            text(202, 488, "Post: N(x + F(x))", 16, 700, "middle", RED)]

    heading(out, 430, "B", "反向：rail 与 gate", TEAL)
    out += [line(445, 150, 755, 150, BLUE, 5, marker="a0"),
            text(600, 126, "identity rail I", 16, 700, "middle", BLUE)]
    node(out, 485, 225, 96, 50, "J_N", TEAL)
    node(out, 625, 225, 96, 50, "J_F", RED)
    out += [path("M455 150V250H480", TEAL, 2.5, "none", None, "a1"),
            line(585, 250, 620, 250, RED, 2.3, marker="a2"),
            path("M725 250H755V155", RED, 2.3, "none", None, "a2"),
            text(600, 315, "Pre: I + J_F J_N", 17, 700, "middle", BLUE)]
    node(out, 455, 380, 112, 52, "I + J_F", BLUE)
    node(out, 630, 380, 112, 52, "J_N", TEAL)
    out += [line(571, 406, 625, 406, TEAL, 2.5, marker="a1"),
            text(600, 476, "Post: J_N (I + J_F)", 17, 700, "middle", RED)]

    heading(out, 830, "C", "结论必须停在证据层", RED)
    levels = (
        ("1  exact", "Jacobian identities", BLUE),
        ("2  theorem", "mean-field + assumptions", TEAL),
        ("3  explanation", "relative residual growth", AMBER),
        ("4  experiment", "task / tuning / seed", RED),
    )
    for idx, (level, desc, color) in enumerate(levels):
        y = 100 + idx * 98
        out += [rect(845, y, 285, 68, color, BG, 5, 2),
                text(862, y + 28, level, 15, 700, fill=color),
                text(1115, y + 52, desc, 15, 600, "end", MUTED)]
        if idx < len(levels) - 1:
            out += [line(987, y + 72, 987, y + 92, INK, 1.7, marker="a3")]
    return finish(out, "恒等 rail 是严格结构；训练稳定与最终效果还需要尺度、相关性、优化和实验。")


def normalization_systems():
    out = begin(
        "Normalization Systems：组、通信、精度与因果",
        "优化批量不等于统计组；分布式统计必须按 count 合并；低精度 reduction 可能溢出或消去；跨时间归约会让未来 suffix 改变过去输出。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "三个 batch，不是一件事", BLUE)
    for row in range(2):
        for col in range(4):
            x, y = 60 + col * 68, 105 + row * 58
            color = BLUE if col < 2 else TEAL
            out += [rect(x, y, 52, 42, color, "#F8FAFC", 4, 1.7)]
    out += [rect(52, 96, 128, 110, BLUE, "none", 6, 2.5),
            rect(188, 96, 128, 110, TEAL, "none", 6, 2.5)]
    out += [text(116, 240, "microbatch 1", 15, 700, "middle", BLUE),
            text(252, 240, "microbatch 2", 15, 700, "middle", TEAL),
            text(184, 283, "one optimizer update", 16, 700, "middle", INK)]
    out += [line(80, 320, 320, 320, GRID, 3),
            line(80, 310, 80, 330, BLUE, 3),
            line(320, 310, 320, 330, RED, 3),
            text(200, 355, "nominal m", 15, 650, "middle", MUTED),
            line(80, 395, 215, 395, BLUE, 5),
            text(200, 430, "effective m shrinks with correlation", 15, 700, "middle", RED),
            text(200, 465, "gradient accumulation does not merge BN stats", 15, 650, "middle", MUTED)]

    heading(out, 430, "B", "Sync：合并 n, mean, M2", TEAL)
    node(out, 445, 105, 132, 58, "rank A", BLUE)
    node(out, 445, 245, 132, 58, "rank B", RED)
    out += [text(511, 193, "(n_A, mu_A, M2_A)", 15, 650, "middle", BLUE),
            text(511, 333, "(n_B, mu_B, M2_B)", 15, 650, "middle", RED)]
    node(out, 630, 175, 125, 78, "weighted merge", TEAL, size=15)
    out += [line(581, 135, 625, 195, BLUE, 2.4, marker="a0"),
            line(581, 274, 625, 230, RED, 2.4, marker="a2")]
    out += [text(670, 333, "not average(rank means)", 15, 700, "middle", RED),
            rect(438, 375, 320, 86, TEAL, "#ECFDF5", 5, 2),
            text(598, 405, "collective changes forward + backward", 15, 700, "middle", TEAL),
            text(598, 435, "process group and dtype are semantics", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "精度门 + 时间门", RED)
    stages = (("x", BLUE), ("square", RED), ("reduce", TEAL), ("rsqrt", BLUE))
    for idx, (lab, color) in enumerate(stages):
        x = 835 + idx * 80
        node(out, x, 100, 66, 44, lab, color, size=15)
        if idx < len(stages) - 1:
            out += [line(x + 68, 122, x + 76, 122, INK, 1.8, marker="a3")]
    out += [text(835, 178, "loss scaling does not repair this path", 15, 700, fill=RED)]
    y = 280
    for idx, val in enumerate(("x1", "x2", "x3", "future")):
        x = 850 + idx * 82
        color = BLUE if idx < 2 else RED
        out += [circle(x, y, 12, color, BG, 2),
                text(x, y + 45, val, 15, 650, "middle", color)]
        if idx < 3:
            out += [line(x + 15, y, x + 65, y, GRID, 2)]
    out += [path("M1108 263C1075 205 900 208 855 263", RED, 2.6, "none", "7 5", "a2"),
            text(980, 222, "full-time stats leak suffix", 15, 700, "middle", RED)]
    out += [rect(845, 385, 285, 82, TEAL, "#ECFDF5", 5, 2),
            text(987, 415, "prefix test", 16, 700, "middle", TEAL),
            text(987, 444, "change suffix; prefix output must stay", 15, 600, "middle", MUTED)]
    return finish(out, "先锁定统计组，再审计 collective、accumulator 与 prefix；四道门彼此不能替代。")


FIGURES = {
    "fig-rmsnorm-centering-invariance-v2.svg": rmsnorm_geometry,
    "fig-normalization-family-axis-lattice-v2.svg": normalization_family_lattice,
    "fig-pre-post-norm-jacobian-v2.svg": pre_post_jacobian,
    "fig-normalization-systems-causality-v2.svg": normalization_systems,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
