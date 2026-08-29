#!/usr/bin/env python3
"""Generate ARCH-05--08 figures with distinct textbook visual grammars."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def sampling_aliasing():
    out = begin("下采样：池化、混叠与不变性边界", "高频信号直接抽取会折叠为错误低频；低通再采样减少混叠但丢失细节；pooling 的局部稳定不等于严格全局不变。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "直接 decimate：高频折叠", BLUE)
    pts = []
    for i in range(17):
        x = 50 + i * 20
        y = 250 - 80 * math.sin(i * 0.78 * math.pi)
        pts.append((x, y))
    out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts), BLUE, 2.5)]
    for i, (x, y) in enumerate(pts):
        if i % 2 == 0:
            out += [circle(x, y, 5, RED, RED, 1)]
    out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts) if i % 2 == 0), RED, 3, dash="7 5")]
    out += [text(45, 365, "red samples suggest a false lower frequency", 15, 700, fill=RED), text(45, 420, "stride S reduces the Nyquist limit by S", 16, 650, cls="math"), text(45, 475, "抽样前仍含高频 → aliasing。", 15, fill=MUTED)]

    heading(out, 430, "B", "low-pass → downsample", TEAL)
    pts2 = []
    for i in range(17):
        x = 450 + i * 20
        y = 250 - 48 * math.sin(i * 0.22 * math.pi)
        pts2.append((x, y))
    out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts2), TEAL, 3)]
    for i, (x, y) in enumerate(pts2):
        if i % 2 == 0:
            out += [circle(x, y, 5, BLUE, BLUE, 1)]
    out += [text(438, 350, "blur suppresses frequencies above new Nyquist", 15, 700, fill=TEAL), text(438, 405, "benefit: less shift-sensitive sampling", 15, 650), text(438, 448, "cost: fine detail and sharpness may be lost", 15, 650, fill=RED), text(438, 488, "filter, padding and task must be audited", 15, fill=MUTED)]

    heading(out, 830, "C", "pooling 不是免费不变", RED)
    out += [rect(842, 105, 300, 72, BLUE, "#EFF6FF", 6, 2), text(992, 135, "local max / average", 17, 700, "middle", BLUE), text(992, 162, "window summary", 15, 650, "middle")]
    out += [line(992, 180, 992, 220, INK, 2.5, marker="a3")]
    out += [rect(842, 232, 300, 72, TEAL, "#ECFDF5", 6, 2), text(992, 262, "stride / decimation", 17, 700, "middle", TEAL), text(992, 289, "changes sampling lattice", 15, 650, "middle")]
    out += [text(842, 360, "small local perturbation", 15, 700, fill=BLUE), text(1040, 360, "≠", 20, 700, fill=RED), text(1075, 360, "global invariance", 15, 700, fill=RED)]
    out += [text(842, 415, "anti-aliasing is a signal-processing fix;", 15, fill=MUTED), text(842, 448, "accuracy gain is an empirical claim.", 15, fill=MUTED), text(842, 493, "report consistency and task metric separately", 15, 700, fill=RED)]
    return finish(out, "下采样先改变可表示频率，再改变等变关系；不变性必须由读出与任务共同定义。")


def receptive_fields():
    out = begin("感受野：理论支持集、路径计数与有效影响", "kernel、stride 与 dilation 精确决定理论感受野；到中心的路径更多产生集中贡献；训练后的 effective receptive field 依参数、输入和测量定义。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "jump 与 receptive field 递推", BLUE)
    layers = ((100, "input", "r=1, j=1"), (210, "3×3,s1", "r=3, j=1"), (320, "3×3,s2", "r=5, j=2"))
    for y, lab, vals in layers:
        out += [rect(60, y, 290, 58, BLUE if y == 100 else TEAL, "#EFF6FF" if y == 100 else "#ECFDF5", 5, 2), text(95, y + 35, lab, 16, 700, fill=BLUE if y == 100 else TEAL), text(235, y + 35, vals, 15, 650, cls="math")]
        if y < 300:
            out += [line(205, y + 60, 205, y + 98, INK, 2.5, marker="a3")]
    out += [text(45, 430, "j_l = j_(l−1) s_l", 16, 700, cls="math"), text(45, 467, "r_l = r_(l−1) + (k_eff,l − 1) j_(l−1)", 15, 700, cls="math"), text(45, 505, "support: can influence, not equal influence", 15, fill=MUTED)]

    heading(out, 430, "B", "路径数在中心更密集", TEAL)
    coeff = (1, 6, 15, 20, 15, 6, 1)
    for i, v in enumerate(coeff):
        x = 448 + i * 43
        h = v * 12
        out += [rect(x, 400 - h, 28, h, TEAL, "#ECFDF5", 2, 1.5), text(x + 14, 425, str(i - 3), 15, 650, "middle")]
    out += [text(438, 115, "six repeated local steps", 16, 700, fill=TEAL), text(438, 155, "path counts ∝ binomial coefficients", 15, 650), text(438, 458, "simplified path analysis", 15, fill=MUTED), text(438, 486, "→ Gaussian-like center under assumptions", 15, fill=MUTED), text(438, 514, "learned weights can reshape it", 15, 700, fill=RED)]

    heading(out, 830, "C", "effective RF 是测量对象", RED)
    size = 9
    for i in range(size):
        for j in range(size):
            dist2 = (i - 4) ** 2 + (j - 4) ** 2
            alpha = max(0.08, math.exp(-dist2 / 7.0))
            shade = int(255 - 100 * alpha)
            fill = f"rgb({shade},{shade+5},{255})"
            out += [rect(850 + j * 29, 110 + i * 29, 25, 25, BLUE, fill, 1, 0.8)]
    out += [text(980, 400, "gradient / perturbation map", 15, 700, "middle", fill=BLUE), text(842, 447, "depends on output scalar, input, weights,", 15, fill=MUTED), text(842, 478, "activation state and threshold", 15, fill=MUTED), text(842, 512, "ERF ≠ causal explanation", 15, 700, fill=RED)]
    return finish(out, "先精确计算理论支持集，再把有效影响当作带定义、带协议的敏感度测量。")


def cnn_stage_budget():
    out = begin("CNN stage：分辨率金字塔、残差块与可分离成本", "CNN 以 stage 交替降低空间分辨率、提高通道宽度；残差连接管理深度；depthwise+pointwise 分离空间和通道混合，但理论 MACs 不等于设备 latency。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "stage pyramid 分配预算", BLUE)
    stages = ((60, 110, 300, 80, "56×56 × 64"), (95, 225, 235, 80, "28×28 × 128"), (130, 340, 170, 80, "14×14 × 256"))
    for i, (x, y, w, h, lab) in enumerate(stages):
        color = BLUE if i == 0 else TEAL
        out += [rect(x, y, w, h, color, "#EFF6FF" if i == 0 else "#ECFDF5", 5, 2), text(x + w / 2, y + 48, lab, 17, 700, "middle", color)]
        if i < 2:
            out += [line(x + w / 2, y + h + 2, stages[i + 1][0] + stages[i + 1][2] / 2, stages[i + 1][1] - 5, INK, 2.5, marker="a3")]
    out += [text(45, 470, "halve H,W; often double C", 16, 700, fill=BLUE), text(45, 505, "standard 3×3 MACs remain roughly level", 15, fill=MUTED)]

    heading(out, 430, "B", "block 组合而非层名清单", TEAL)
    node(out, 445, 125, 85, 50, "x", BLUE, "#EFF6FF")
    node(out, 575, 125, 120, 50, "spatial mix", TEAL, "#ECFDF5")
    node(out, 575, 245, 120, 50, "channel mix", TEAL, "#ECFDF5")
    node(out, 575, 365, 120, 50, "+ shortcut", RED, "#FFF5F2")
    out += [line(531, 150, 568, 150, INK, 2.5, marker="a3"), line(635, 178, 635, 237, INK, 2.5, marker="a3"), line(635, 298, 635, 357, INK, 2.5, marker="a3"), path("M487 177L487 390L568 390", BLUE, 2.5, marker="a0")]
    out += [text(438, 465, "stride/channel mismatch needs projection", 15, fill=MUTED), text(438, 500, "norm placement is part of block contract", 15, 700, fill=RED)]

    heading(out, 830, "C", "standard vs separable", RED)
    out += [rect(845, 105, 290, 72, BLUE, "#EFF6FF", 5, 2), text(990, 135, "standard K×K", 17, 700, "middle", BLUE), text(990, 162, "Cin Cout K²", 16, 650, "middle", cls="math")]
    out += [line(990, 180, 990, 220, INK, 2.5, marker="a3")]
    out += [rect(845, 232, 130, 72, TEAL, "#ECFDF5", 5, 2), text(910, 262, "depthwise", 16, 700, "middle", TEAL), text(910, 289, "Cin K²", 15, 650, "middle", cls="math")]
    out += [text(991, 274, "+", 21, 700, "middle"), rect(1008, 232, 130, 72, TEAL, "#ECFDF5", 5, 2), text(1073, 262, "pointwise", 16, 700, "middle", TEAL), text(1073, 289, "Cin Cout", 15, 650, "middle", cls="math")]
    out += [text(842, 360, "ratio ≈ 1/Cout + 1/K²", 17, 700, fill=RED, cls="math"), text(842, 410, "but depthwise may be memory-bound", 15, fill=MUTED), text(842, 450, "benchmark target device and batch", 15, fill=MUTED), text(842, 495, "FLOPs, latency, energy are distinct", 15, 700, fill=RED)]
    return finish(out, "现代 CNN 的核心是 stage、block 与资源协同设计，而不是按年代背诵架构名字。")


def group_equivariance():
    out = begin("群卷积：轨道共享、feature action 与证据边界", "群作用把输入变换组织成轨道；G-convolution 在群元素上共享滤波器并保持可预测变换；结构等变不自动等于任务不变或经验最优。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "从一个 pattern 到群轨道", BLUE)
    cx, cy = 205, 255
    for angle, lab in ((0, "0°"), (90, "90°"), (180, "180°"), (270, "270°")):
        rad = math.radians(angle)
        x, y = cx + 120 * math.cos(rad), cy + 120 * math.sin(rad)
        out += [rect(x - 28, y - 28, 56, 56, BLUE, "#EFF6FF", 4, 2), line(x, y, x + 18 * math.cos(rad), y + 18 * math.sin(rad), RED, 4), text(x, y + 50, lab, 15, 650, "middle")]
    out += [circle(cx, cy, 25, TEAL, "#ECFDF5", 2.5), text(cx, cy + 6, "G", 18, 700, "middle", TEAL), text(45, 455, "orbit(x) = {T_g x : g∈G}", 17, 700, cls="math"), text(45, 492, "需要先说明任务真正拥有哪个 symmetry。", 15, fill=MUTED)]

    heading(out, 430, "B", "feature map 也随群变换", TEAL)
    node(out, 445, 120, 115, 55, "x", BLUE, "#EFF6FF")
    node(out, 645, 120, 115, 55, "Tg x", BLUE, "#EFF6FF")
    node(out, 445, 350, 115, 55, "f(x)", TEAL, "#ECFDF5")
    node(out, 645, 350, 115, 55, "Sg f(x)", TEAL, "#ECFDF5")
    out += [line(561, 148, 638, 148, BLUE, 3, marker="a0"), line(502, 178, 502, 342, TEAL, 3, marker="a1"), line(702, 178, 702, 342, TEAL, 3, marker="a1"), line(561, 378, 638, 378, BLUE, 3, marker="a0")]
    out += [text(438, 455, "f(Tg x)=Sg f(x)", 19, 700, cls="math", fill=RED), text(438, 493, "output action Sg is part of the definition", 15, fill=MUTED)]

    heading(out, 830, "C", "四层证据不要越级", RED)
    levels = ((105, "I", "equivariance identity", BLUE), (195, "T", "function / sample bounds", TEAL), (285, "E", "dataset & scale experiments", RED), (375, "H/O", "why it helps / when it fails", BLUE))
    for y, tag, label, color in levels:
        out += [circle(860, y - 5, 18, color, BG, 2.5), text(860, y + 1, tag, 15, 700, "middle", color), text(895, y, label, 16, 650), line(842, y + 30, 1138, y + 30, GRID, 1)]
    out += [text(842, 455, "wrong symmetry can increase bias", 15, 700, fill=RED), text(842, 492, "augmentation and equivariance are complementary", 15, fill=MUTED)]
    return finish(out, "群等变网络把正确对称性写入参数共享；保证的强弱取决于群、边界、读出和证据层级。")


FIGURES = {
    "fig-pooling-sampling-aliasing-v1.svg": sampling_aliasing,
    "fig-receptive-field-theoretical-effective-v1.svg": receptive_fields,
    "fig-cnn-stage-block-budget-v1.svg": cnn_stage_budget,
    "fig-group-equivariance-evidence-v1.svg": group_equivariance,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
