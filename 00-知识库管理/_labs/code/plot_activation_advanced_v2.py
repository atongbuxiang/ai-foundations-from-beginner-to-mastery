#!/usr/bin/env python3
"""Generate deterministic NN-21--24 activation and gating textbook figures."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def polyline(points, color=INK, width=2.5, dash=None):
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>'


def curve_points(fn, x0, x1, y0, y1, xmin=-5.0, xmax=5.0, ymin=-1.2, ymax=5.0, n=180):
    points = []
    for index in range(n + 1):
        x = xmin + (xmax - xmin) * index / n
        y = max(ymin, min(ymax, fn(x)))
        px = x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
        py = y1 - (y - ymin) / (ymax - ymin) * (y1 - y0)
        points.append((px, py))
    return points


def smooth_activation_operators():
    out = begin(
        "Softplus、GELU 与 SiLU：三个不同的平滑算子",
        "Softplus 平滑 maximum；GELU 与 SiLU 以不同 CDF 自门控；函数曲线相近不代表构造、导数、曲率与实现合同相同。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先区分构造算子", BLUE)
    node(out, 55, 105, 68, 44, "0", BLUE)
    node(out, 55, 175, 68, 44, "x", BLUE)
    node(out, 170, 135, 165, 58, "log-sum-exp", BLUE)
    out += [line(125, 127, 166, 155, BLUE, 2.4, marker="a0"), line(125, 197, 166, 172, BLUE, 2.4, marker="a0")]
    out += [text(195, 221, "Softplus", 16, 700, "middle", BLUE)]

    node(out, 55, 277, 68, 44, "x", TEAL)
    node(out, 154, 252, 90, 44, "CDF", TEAL)
    node(out, 154, 326, 90, 44, "sigmoid", TEAL)
    out += [line(125, 299, 150, 274, TEAL, 2.4, marker="a1"), line(125, 299, 150, 348, TEAL, 2.4, marker="a1")]
    node(out, 276, 276, 70, 70, "x * gate", TEAL, size=15)
    out += [line(246, 274, 272, 296, TEAL, 2.4, marker="a1"), line(246, 348, 272, 326, TEAL, 2.4, marker="a1")]
    out += [text(198, 402, "GELU / SiLU: self-gating", 16, 700, "middle", TEAL)]
    out += [rect(55, 438, 290, 52, RED, "#FFF5F2", 7, 2), text(200, 461, "convolution smooths the whole graph", 15, 700, "middle", RED), text(200, 482, "E[ReLU(x+noise)] != GELU", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "值相近，斜率与曲率不同", TEAL)
    x0, x1, y0, y1 = 448, 750, 108, 390
    x_axis = y1 - (0 - (-1.2)) / (5.0 - (-1.2)) * (y1 - y0)
    y_axis = x0 + (0 - (-5.0)) / 10.0 * (x1 - x0)
    out += [line(x0, x_axis, x1, x_axis, GRID, 2), line(y_axis, y0, y_axis, y1, GRID, 2)]
    sigmoid = lambda z: 1.0 / (1.0 + math.exp(-z))
    softplus = lambda z: max(z, 0.0) + math.log1p(math.exp(-abs(z)))
    gelu = lambda z: z * 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    silu = lambda z: z * sigmoid(z)
    out += [polyline(curve_points(softplus, x0, x1, y0, y1), BLUE, 3.2)]
    out += [polyline(curve_points(gelu, x0, x1, y0, y1), TEAL, 3.0)]
    out += [polyline(curve_points(silu, x0, x1, y0, y1), RED, 2.8, "7 5")]
    out += [text(665, 139, "Softplus", 15, 700, fill=BLUE), text(665, 170, "GELU", 15, 700, fill=TEAL), text(665, 201, "SiLU", 15, 700, fill=RED)]
    out += [rect(445, 420, 310, 72, TEAL, "#ECFDF5", 7, 2), text(600, 446, "center slopes = 1/2", 16, 700, "middle", TEAL), text(600, 471, "only Softplus is globally convex", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "Exact / Approx 是版本合同", RED)
    node(out, 845, 105, 122, 54, "exact GELU", BLUE, size=15)
    node(out, 1010, 105, 120, 54, "tanh / sigmoid", TEAL, size=15)
    out += [line(970, 132, 1006, 132, RED, 2.5, "5 4", "a2")]
    rows = (
        (200, "forward max error"),
        (251, "VJP / gradgrad error"),
        (302, "dtype + input interval"),
        (353, "kernel + fusion"),
        (404, "checkpoint / export flag"),
    )
    for index, (y, label) in enumerate(rows):
        color = BLUE if index % 2 == 0 else TEAL
        out += [rect(845, y, 285, 38, color, BG, 5, 1.8), circle(863, y + 19, 6, color, color, 1), text(879, y + 25, label, 15, 650)]
    out += [rect(845, 462, 285, 38, RED, "#FFF5F2", 5, 2), text(987, 487, "same name != same executable", 15, 700, "middle", RED)]
    return finish(out, "先问平滑了什么，再看导数与曲率，最后把近似、精度和 backward 固定为可复现实验合同。")


def glu_gated_ffn():
    out = begin(
        "GLU Family：双投影、乘性汇合与三矩阵预算",
        "Value 与 gate 两条 learned projections 在逐元乘法处汇合；反向必须分流再累加；公平比较需要按真实宽度核对参数、计算、存储和融合。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "两条投影在乘法处汇合", BLUE)
    node(out, 55, 230, 62, 50, "X", BLUE)
    node(out, 160, 125, 116, 52, "V = X Wv", BLUE, size=15)
    node(out, 160, 335, 116, 52, "G = X Wg", TEAL, size=15)
    node(out, 160, 415, 116, 48, "phi(G)", TEAL, size=15)
    out += [line(120, 245, 156, 151, BLUE, 2.5, marker="a0"), line(120, 265, 156, 361, TEAL, 2.5, marker="a1"), line(218, 389, 218, 411, TEAL, 2.5, marker="a1")]
    node(out, 315, 245, 52, 52, "*", RED, size=22)
    out += [line(278, 151, 311, 258, BLUE, 2.5, marker="a0"), line(278, 439, 311, 284, TEAL, 2.5, marker="a1")]
    out += [text(340, 214, "H = V * phi(G)", 16, 700, "end", RED), text(55, 490, "GEGLU / SwiGLU gates may be negative or > 1.", 15, 600, fill=MUTED)]

    heading(out, 430, "B", "Reverse：分流、乘法、再累加", TEAL)
    node(out, 540, 100, 110, 50, "Hbar = U", RED, size=15)
    node(out, 445, 215, 135, 62, "Vbar = U phi(G)", BLUE, size=15)
    node(out, 625, 215, 130, 62, "Gbar = U V phi'(G)", TEAL, size=15)
    out += [line(570, 153, 520, 211, BLUE, 2.5, marker="a0"), line(620, 153, 690, 211, TEAL, 2.5, marker="a1")]
    node(out, 445, 355, 310, 62, "Xbar = Vbar Wv^T + Gbar Wg^T", RED, size=15)
    out += [line(515, 280, 540, 351, BLUE, 2.5, marker="a0"), line(690, 280, 660, 351, TEAL, 2.5, marker="a1")]
    out += [rect(445, 448, 310, 44, RED, "#FFF5F2", 6, 2), text(600, 476, "no uniform gradient lower bound", 15, 700, "middle", RED)]

    heading(out, 830, "C", "预算匹配不止一个比例", RED)
    out += [text(845, 117, "standard FFN", 16, 700, fill=BLUE), text(1115, 117, "2 d h", 17, 700, "end", BLUE, "math")]
    out += [line(845, 133, 1130, 133, GRID, 1.5)]
    out += [text(845, 165, "gated FFN", 16, 700, fill=TEAL), text(1115, 165, "3 d h_g", 17, 700, "end", TEAL, "math")]
    out += [line(845, 181, 1130, 181, GRID, 1.5)]
    out += [rect(845, 204, 285, 52, RED, "#FFF5F2", 6, 2), text(987, 236, "parameter match: h_g about 2h/3", 15, 700, "middle", RED)]
    for index, label in enumerate(("tile-rounded width", "logical / saved bytes", "TP communication", "fused wall-clock")):
        y = 285 + index * 48
        color = BLUE if index % 2 == 0 else TEAL
        out += [circle(858, y, 7, color, color, 1), text(876, y + 6, label, 15, 650)]
    out += [line(845, 482, 1130, 482, GRID, 1.5), text(987, 508, "measure on the target device", 15, 700, "middle", RED)]
    return finish(out, "GLU 的结构事实是双投影乘法；性能事实必须在参数、FLOP、内存、通信和目标硬件上分别验收。")


def maxout_upper_envelope():
    out = begin(
        "Maxout：Upper Envelope、Winner Region 与计算语义",
        "多个 affine candidates 的上包络形成 convex piecewise-linear unit；唯一 winner 给局部梯度，tie 给次微分；梯度稀疏不等于前向跳算。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Affine candidates 与上包络", BLUE)
    x0, x1, y0, y1 = 65, 350, 110, 420
    out += [line(x0, 330, x1, 330, GRID, 2), line(205, y0, 205, y1, GRID, 2)]
    # Candidate lines in pixel coordinates; the highlighted envelope is traced explicitly.
    out += [line(70, 385, 345, 145, BLUE, 2, "7 5"), line(70, 155, 345, 385, TEAL, 2, "7 5"), line(70, 245, 345, 245, RED, 2, "7 5")]
    out += [path("M70 155L160 230L175 245L240 245L255 230L345 145", INK, 4)]
    out += [circle(175, 245, 6, RED, BG, 2), circle(240, 245, 6, RED, BG, 2)]
    out += [text(90, 139, "candidate 2", 15, 650, fill=TEAL), text(268, 132, "candidate 1", 15, 650, fill=BLUE), text(260, 268, "candidate 3", 15, 650, fill=RED)]
    out += [text(205, 464, "bold curve = upper envelope", 16, 700, "middle", INK), text(205, 491, "ties sit on region boundaries", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "Winner 决定局部 VJP", TEAL)
    regions = ((450, 105, 92, "R2", TEAL), (542, 105, 118, "R3", RED), (660, 105, 92, "R1", BLUE))
    for x, y, w, label, color in regions:
        out += [rect(x, y, w, 58, color, color, 0, 1), text(x + w / 2, y + 36, label, 16, 700, "middle", BG)]
    out += [text(450, 205, "unique winner r*", 16, 700, fill=TEAL), text(450, 237, "gradient = winning slope", 16, 650, fill=INK)]
    out += [line(450, 263, 755, 263, GRID, 2)]
    out += [text(450, 305, "tie active set A", 16, 700, fill=RED), text(450, 337, "subgradient = convex hull of active slopes", 15, 650, fill=INK)]
    out += [text(450, 375, "directional slope = max active dot product", 15, 650, fill=INK)]
    out += [rect(450, 418, 302, 70, RED, "#FFF5F2", 6, 2), text(601, 446, "framework tie rule", 16, 700, "middle", RED), text(601, 471, "is a convention, not a derivative theorem", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "三种“稀疏”不可混用", RED)
    rows = (
        (105, "Maxout forward", "compute all k candidates", BLUE),
        (205, "Maxout backward", "route VJP to winner", TEAL),
        (305, "MoE routing", "select before expert compute", RED),
        (405, "ReLU zeros", "dense GEMM already happened", BLUE),
    )
    for index, (y, title, detail, color) in enumerate(rows):
        out += [rect(845, y, 285, 68, color, BG, 7, 2), text(862, y + 27, title, 16, 700, fill=color), text(862, y + 51, detail, 15, 500, fill=MUTED)]
        if index < len(rows) - 1:
            out += [line(987, y + 71, 987, rows[index + 1][0] - 4, GRID, 1.5)]
    return finish(out, "先计算 candidate、再选择 winner 是普通 Maxout；只有选择发生在昂贵分支之前，才构成真正条件计算。")


def activation_evidence_protocol():
    out = begin(
        "激活函数证据协议：从稳定 Primitive 到有边界结论",
        "可靠选择依次审计数值实现、深层尺度、系统预算与统计选择；任何漂亮的单点指标都不能跨越尚未通过的证据门。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "数值门：稳定 Primitive", BLUE)
    rows = (
        (105, "sigmoid", "sign branch", BLUE),
        (178, "Softplus", "max + log1p", TEAL),
        (251, "log-sigmoid", "-Softplus(-x)", BLUE),
        (324, "ELU near zero", "expm1", TEAL),
        (397, "GELU", "exact / approx flag", BLUE),
    )
    for y, name, implementation, color in rows:
        out += [rect(55, y, 292, 52, color, BG, 6, 2), text(70, y + 22, name, 15, 700, fill=color), text(70, y + 43, implementation, 15, 500, fill=MUTED)]
    out += [text(200, 490, "forward + VJP + gradgrad", 15, 700, "middle", RED)]

    heading(out, 430, "B", "传播门：不要混淆统计量", TEAL)
    metrics = (
        (105, "mean", "E[H]"),
        (172, "second moment", "E[H^2]"),
        (239, "variance", "E[H^2] - E[H]^2"),
        (306, "derivative gain", "E[phi'(Z)^2]"),
        (373, "directional spectrum", "singular values of J"),
    )
    for index, (y, label, formula) in enumerate(metrics):
        color = BLUE if index < 3 else TEAL
        out += [rect(445, y, 310, 48, color, "#F8FAFC", 6, 1.8), text(460, y + 20, label, 15, 700, fill=color), text(740, y + 34, formula, 15, 600, "end", INK, "math")]
    out += [rect(445, 454, 310, 43, RED, "#FFF5F2", 6, 2), text(600, 481, "stable moments != stable Jacobian", 15, 700, "middle", RED)]

    heading(out, 830, "C", "系统 + 统计门：结论逐级收窄", RED)
    gates = (
        (105, "1  parameters / MAC / bytes", BLUE),
        (171, "2  fused latency on target GPU", TEAL),
        (237, "3  plug-in + retuned tracks", BLUE),
        (303, "4  matched budget + all seeds", TEAL),
        (369, "5  selection correction + test", RED),
    )
    for index, (y, label, color) in enumerate(gates):
        out += [rect(845, y, 285, 45, color, BG, 6, 2), text(987, y + 28, label, 15, 650, "middle", color)]
        if index < len(gates) - 1:
            out += [line(987, y + 47, 987, gates[index + 1][0] - 3, INK, 1.8, marker="a3")]
    out += [rect(845, 447, 285, 52, RED, "#FFF5F2", 7, 2), text(987, 470, "bounded claim", 16, 700, "middle", RED), text(987, 491, "model + data + budget + hardware", 15, 500, "middle", MUTED)]
    return finish(out, "可发布结论不是“某激活最好”，而是它在已声明模型、数据、预算、精度和硬件范围内通过了哪些证据门。")


FIGURES = {
    "fig-smooth-activation-operators-v2.svg": smooth_activation_operators,
    "fig-glu-gated-ffn-v2.svg": glu_gated_ffn,
    "fig-maxout-upper-envelope-v2.svg": maxout_upper_envelope,
    "fig-activation-evidence-protocol-v2.svg": activation_evidence_protocol,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
