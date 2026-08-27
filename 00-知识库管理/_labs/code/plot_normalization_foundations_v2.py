#!/usr/bin/env python3
"""Generate deterministic NN-33--36 normalization textbook figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def polygon(points, stroke=INK, fill="none", width=2.0, dash=None):
    pts = " ".join(f"{x},{y}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{extra}/>'


def normalization_axis_contract():
    out = begin(
        "Normalization Axis Contract：统计组、参数轴与不变性",
        "同一张量可按不同轴组成统计组；完整归一化合同还包括 affine 参数共享、状态规则和 epsilon 约定；共同平移与正尺度只在明确条件下被删除。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一张量，两种统计组", BLUE)
    out += [text(55, 92, "X [B,T,D]", 17, 700, fill=INK)]
    for row in range(4):
        for col in range(5):
            x, y = 65 + col * 48, 112 + row * 39
            color = BLUE if col == 2 else GRID
            fill = "#EFF6FF" if col == 2 else BG
            out += [rect(x, y, 35, 28, color, fill, 3, 1.7)]
    out += [rect(156, 106, 47, 158, BLUE, "none", 5, 2.3)]
    out += [text(180, 290, "fixed feature", 15, 700, "middle", BLUE),
            text(180, 313, "reduce B,T", 15, 500, "middle", MUTED)]
    for row in range(2):
        for col in range(5):
            x, y = 65 + col * 48, 352 + row * 39
            color = TEAL if row == 0 else GRID
            fill = "#ECFDF5" if row == 0 else BG
            out += [rect(x, y, 35, 28, color, fill, 3, 1.7)]
    out += [rect(59, 346, 233, 40, TEAL, "none", 5, 2.3)]
    out += [text(176, 430, "fixed token: reduce D", 15, 700, "middle", TEAL),
            text(176, 458, "same shape, different function", 15, 500, "middle", RED)]

    heading(out, 430, "B", "四元组定义一个算子", TEAL)
    stages = (
        (105, "1  select group G", BLUE),
        (178, "2  center: x - mean", TEAL),
        (251, "3  scale: / sqrt(q+eps)", TEAL),
        (324, "4  affine: gamma, beta", BLUE),
    )
    for index, (y, label, color) in enumerate(stages):
        node(out, 455, y, 230, 48, label, color, size=15)
        if index < len(stages) - 1:
            out += [line(570, y + 51, 570, stages[index + 1][0] - 4, INK, 1.8, marker="a3")]
    out += [rect(705, 118, 70, 78, RED, "#FFF5F2", 5, 2),
            text(740, 147, "state", 15, 700, "middle", RED),
            text(740, 172, "mode", 15, 600, "middle", MUTED),
            line(688, 142, 701, 142, RED, 1.8, marker="a2")]
    out += [rect(455, 415, 320, 65, RED, "#FFF5F2", 5, 2),
            text(615, 441, "axes + affine + state + epsilon", 15, 700, "middle", RED),
            text(615, 465, "module name is only a preset", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "只删除声明过的方向", RED)
    out += [line(850, 292, 1125, 292, GRID, 2),
            line(975, 105, 975, 390, GRID, 2)]
    out += [path("M865 360L1100 145", TEAL, 2.5, "none", "7 5"),
            text(1090, 132, "1-perp", 15, 700, "end", TEAL)]
    out += [circle(905, 170, 7, BLUE, BLUE, 2),
            circle(955, 220, 7, BLUE, BG, 2),
            line(905, 170, 951, 216, BLUE, 2.2, marker="a0"),
            text(882, 158, "x", 15, 700, fill=BLUE),
            text(958, 213, "center", 15, 600, fill=BLUE)]
    out += [circle(1035, 205, 7, TEAL, BG, 2),
            line(955, 220, 1031, 207, TEAL, 2.5, marker="a1"),
            text(1043, 203, "normalize radius", 15, 600, fill=TEAL)]
    out += [rect(845, 410, 285, 70, RED, "#FFF5F2", 5, 2),
            text(987, 436, "shift: exact", 15, 700, "middle", BLUE),
            text(987, 459, "scale: exact only if eps = 0", 15, 650, "middle", RED)]
    return finish(out, "先锁定统计轴、参数轴与状态，再讨论被删除的方向；normalization 不是 whitening。")


def batchnorm_forward_state():
    out = begin(
        "BatchNorm Forward：当前批统计、持久状态与推理折叠",
        "卷积 BatchNorm 对每个 channel 在 N、H、W 上归约；训练输出用当前批统计并更新 buffers；推理使用固定 buffers 时可折叠为普通 affine map。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Conv BN：每个 C 一组", BLUE)
    colors = (BLUE, TEAL, RED)
    for ch, color in enumerate(colors):
        x = 65 + ch * 92
        out += [rect(x, 112, 70, 154, color, "#F8FAFC", 5, 2),
                text(x + 35, 98, f"C{ch + 1}", 15, 700, "middle", color)]
        for row in range(4):
            for col in range(2):
                out += [rect(x + 9 + col * 27, 128 + row * 31, 21, 21, color, BG, 2, 1.3)]
    out += [text(200, 302, "reduce (N,H,W)", 17, 700, "middle", BLUE),
            text(200, 332, "m = N H W", 17, 650, "middle", TEAL),
            text(200, 374, "gamma, beta shape [C]", 15, 600, "middle", MUTED)]
    out += [rect(55, 410, 292, 68, RED, "#FFF5F2", 5, 2),
            text(201, 436, "nominal count is not IID count", 15, 700, "middle", RED),
            text(201, 460, "spatial samples may correlate", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "训练路径与推理路径", TEAL)
    node(out, 445, 105, 90, 46, "input X", BLUE, size=15)
    node(out, 565, 105, 190, 46, "batch mean / biased var", BLUE, size=15)
    out += [line(538, 128, 561, 128, BLUE, 2.2, marker="a0")]
    node(out, 565, 185, 190, 52, "normalize + affine", TEAL, size=15)
    out += [line(660, 154, 660, 181, TEAL, 2.2, marker="a1")]
    out += [rect(445, 276, 135, 70, RED, "#FFF5F2", 5, 2),
            text(512, 303, "running state", 15, 700, "middle", RED),
            text(512, 328, "EMA update", 15, 500, "middle", MUTED),
            line(608, 154, 548, 272, RED, 2, marker="a2")]
    out += [text(610, 259, "TRAIN: output uses current batch", 15, 700, "middle", BLUE)]
    node(out, 445, 390, 135, 54, "fixed buffers", RED, size=15)
    node(out, 620, 390, 135, 54, "eval output", TEAL, size=15)
    out += [line(584, 417, 616, 417, TEAL, 2.2, marker="a1"),
            text(600, 478, "EVAL: no companion dependence", 15, 700, "middle", TEAL)]

    heading(out, 830, "C", "固定统计量才能折叠", RED)
    out += [rect(845, 105, 285, 68, BLUE, BG, 5, 2),
            text(987, 133, "z = W x + b", 17, 700, "middle", BLUE, "math"),
            text(987, 157, "a = gamma / sqrt(v + eps)", 15, 600, "middle", MUTED, "math")]
    out += [line(987, 178, 987, 202, INK, 2, marker="a3")]
    out += [rect(845, 208, 285, 83, TEAL, "#ECFDF5", 5, 2),
            text(987, 237, "W' = a W", 17, 700, "middle", TEAL, "math"),
            text(987, 264, "b' = a (b - mean) + beta", 15, 650, "middle", TEAL, "math")]
    checks = (("forward var", "biased"), ("running var", "unbiased obs"), ("momentum", "new-value weight"), ("mode", "train or eval"))
    for index, (left, right) in enumerate(checks):
        y = 325 + index * 43
        out += [text(850, y, left, 15, 700, fill=BLUE),
                text(1120, y, right, 15, 500, "end", MUTED),
                line(845, y + 9, 1130, y + 9, GRID, 1)]
    return finish(out, "训练 BN 是带 batch 与 state 的算子；固定 eval statistics 后才是可折叠的 affine map。")


def batchnorm_backward_coupling():
    out = begin(
        "BatchNorm Backward：两次投影、跨样本耦合与尺度方向",
        "训练反向先乘 gain，再删除组均值与 normalized radial 分量；Jacobian 因共享统计量而非对角；正尺度不变权重的梯度位于切向并随权重尺度反比变化。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "VJP 是两次组内投影", BLUE)
    stages = (
        (105, "g", BLUE),
        (174, "u = gamma g", BLUE),
        (243, "u - mean(u)", TEAL),
        (312, "- xhat mean(u xhat)", TEAL),
        (381, "dx = result / r", RED),
    )
    for index, (y, label, color) in enumerate(stages):
        node(out, 75, y, 250, 45, label, color, size=15)
        if index < len(stages) - 1:
            out += [line(200, y + 48, 200, stages[index + 1][0] - 4, INK, 1.7, marker="a3")]
    out += [text(200, 467, "sum(dx) = 0", 16, 700, "middle", BLUE, "math"),
            text(200, 494, "eps=0: centered radial dot = 0", 15, 600, "middle", TEAL)]

    heading(out, 430, "B", "Train dense；Eval diagonal", TEAL)
    out += [text(492, 94, "TRAIN J", 16, 700, "middle", TEAL),
            text(685, 94, "EVAL J", 16, 700, "middle", BLUE)]
    cell = 31
    for row in range(5):
        for col in range(5):
            x, y = 425 + col * cell, 115 + row * cell
            color = TEAL if row == col else BLUE
            fill = "#ECFDF5" if row == col else "#EFF6FF"
            out += [rect(x, y, 25, 25, color, fill, 2, 1.3)]
            x2 = 615 + col * cell
            color2 = BLUE if row == col else GRID
            fill2 = "#EFF6FF" if row == col else BG
            out += [rect(x2, y, 25, 25, color2, fill2, 2, 1.3)]
    out += [text(497, 303, "all samples coupled", 15, 650, "middle", RED),
            text(687, 303, "fixed elementwise scale", 15, 650, "middle", BLUE)]
    out += [rect(430, 350, 320, 115, RED, "#FFF5F2", 5, 2),
            text(590, 378, "batch noise is", 16, 700, "middle", RED),
            text(590, 404, "data-dependent + correlated", 15, 650, "middle", MUTED),
            text(590, 430, "non-additive + mode-specific", 15, 650, "middle", MUTED)]

    heading(out, 830, "C", "Scale ray 与切向更新", RED)
    ox, oy = 880, 390
    out += [line(ox, oy, 1120, 145, GRID, 2, "7 5"),
            circle(950, 318, 7, BLUE, BLUE, 2),
            circle(1050, 216, 8, TEAL, TEAL, 2),
            text(938, 343, "w", 15, 700, fill=BLUE),
            text(1062, 208, "a w", 15, 700, fill=TEAL)]
    out += [line(950, 318, 907, 276, BLUE, 3, marker="a0"),
            line(1050, 216, 1026, 193, TEAL, 2, marker="a1"),
            text(850, 255, "gradient tangent", 15, 700, fill=BLUE)]
    out += [rect(845, 410, 285, 75, RED, "#FFF5F2", 5, 2),
            text(987, 437, "raw grad: 1 / a", 16, 700, "middle", RED, "math"),
            text(987, 462, "angular step: about 1 / a^2", 15, 650, "middle", MUTED, "math")]
    return finish(out, "BatchNorm backward 改变依赖图与参数几何；它不是逐元素缩放，也不是独立噪声。")


def layernorm_token_geometry():
    out = begin(
        "LayerNorm Geometry：逐 token 分组、球面与低维退化",
        "LayerNorm 对每个 token 的 feature vector 单独中心化与径向归一；统计不跨 batch 或 token，但 token 内 Jacobian 密集；D 等于 1 或 2 时自由度严重退化。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "每个 token 一组 features", BLUE)
    for row in range(5):
        y = 105 + row * 60
        color = BLUE if row % 2 == 0 else TEAL
        out += [rect(60, y - 6, 270, 44, color, "none", 5, 2)]
        for col in range(6):
            out += [circle(82 + col * 43, y + 16, 9, color, BG, 1.7)]
        out += [text(48, y + 21, f"t{row + 1}", 15, 650, "end", MUTED)]
    out += [text(195, 425, "reduce D within each row", 16, 700, "middle", BLUE),
            text(195, 454, "gamma, beta [D] shared across rows", 15, 600, "middle", TEAL),
            text(195, 482, "no running statistics", 15, 600, "middle", RED)]

    heading(out, 430, "B", "Project，再归一半径", TEAL)
    out += [line(450, 315, 750, 315, GRID, 2),
            line(600, 90, 600, 465, GRID, 2)]
    out += [path("M460 390L742 128", TEAL, 2.5, "none", "7 5"),
            text(730, 112, "1-perp", 15, 700, "end", TEAL)]
    out += [circle(600, 315, 103, GRID, "none", 1.8),
            text(700, 302, "radius sqrt(D)", 15, 600, fill=MUTED)]
    out += [circle(505, 145, 7, BLUE, BLUE, 2),
            text(489, 130, "x", 15, 700, fill=BLUE),
            circle(566, 218, 7, BLUE, BG, 2),
            line(508, 150, 562, 214, BLUE, 2.4, marker="a0"),
            text(545, 208, "c", 15, 700, fill=BLUE)]
    out += [circle(526, 249, 8, TEAL, TEAL, 2),
            line(562, 222, 531, 246, TEAL, 2.5, marker="a1"),
            text(506, 274, "xhat", 15, 700, fill=TEAL)]
    out += [rect(445, 425, 310, 58, RED, "#FFF5F2", 5, 2),
            text(600, 451, "kept local degrees = D - 2", 16, 700, "middle", RED),
            text(600, 474, "before per-feature affine", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "独立 groups，不是 diagonal J", RED)
    out += [rect(845, 105, 285, 70, BLUE, BG, 5, 2),
            text(987, 133, "other tokens do not enter stats", 15, 700, "middle", BLUE),
            text(987, 158, "same rule in train and eval", 15, 500, "middle", MUTED)]
    out += [rect(845, 205, 285, 78, TEAL, "#ECFDF5", 5, 2),
            text(987, 233, "within-token J is dense", 16, 700, "middle", TEAL),
            text(987, 258, "mean + radial coupling", 15, 500, "middle", MUTED)]
    out += [rect(845, 320, 135, 95, RED, "#FFF5F2", 5, 2),
            text(912, 350, "D = 1", 17, 700, "middle", RED),
            text(912, 378, "output beta", 15, 600, "middle", MUTED),
            text(912, 402, "J = 0", 15, 600, "middle", MUTED)]
    out += [rect(995, 320, 135, 95, RED, "#FFF5F2", 5, 2),
            text(1062, 350, "D = 2", 17, 700, "middle", RED),
            text(1062, 378, "two points", 15, 600, "middle", MUTED),
            text(1062, 402, "J = 0 if eps=0", 15, 600, "middle", MUTED)]
    out += [text(987, 470, "eps restores a small radial derivative", 15, 650, "middle", BLUE)]
    return finish(out, "LayerNorm 不跨 token，但会耦合 token 内 features；宽度与 epsilon 决定保留几何。")


FIGURES = {
    "fig-normalization-axis-contract-v2.svg": normalization_axis_contract,
    "fig-batchnorm-forward-state-v2.svg": batchnorm_forward_state,
    "fig-batchnorm-backward-coupling-v2.svg": batchnorm_backward_coupling,
    "fig-layernorm-token-geometry-v2.svg": layernorm_token_geometry,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

