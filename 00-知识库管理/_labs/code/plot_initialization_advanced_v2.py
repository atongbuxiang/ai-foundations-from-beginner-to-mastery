#!/usr/bin/env python3
"""Generate deterministic NN-29--32 initialization textbook figures."""

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


def correlation_edge_of_chaos():
    out = begin(
        "Correlation Propagation：从二维 Gaussian 到 Edge of Chaos",
        "两输入 covariance map 控制表示的相对几何；c=1 处斜率区分 ordered、critical 与 chaotic 局部制度，但不控制完整 Jacobian spectrum。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一随机网络的两条输入路径", BLUE)
    node(out, 55, 105, 82, 48, "input x", BLUE, size=15)
    node(out, 55, 205, 82, 48, "input x'", TEAL, size=15)
    node(out, 170, 145, 82, 68, "same W,b", RED, size=15)
    node(out, 282, 105, 65, 48, "U", BLUE, size=17)
    node(out, 282, 205, 65, 48, "V", TEAL, size=17)
    out += [line(139, 129, 166, 167, BLUE, 2.4, marker="a0"), line(139, 229, 166, 191, TEAL, 2.4, marker="a1")]
    out += [line(255, 167, 279, 129, BLUE, 2.4, marker="a0"), line(255, 191, 279, 229, TEAL, 2.4, marker="a1")]
    out += [rect(55, 300, 292, 64, BLUE, BG, 6, 2), text(201, 327, "Cov(U,V) = q c", 17, 700, "middle", BLUE, "math"), text(201, 351, "shared bias contributes + sb^2", 15, 500, "middle", MUTED)]
    out += [rect(55, 395, 292, 84, TEAL, "#ECFDF5", 6, 2), text(201, 422, "V = sqrt(q) [c Z1 + sqrt(1-c^2) Z2]", 15, 650, "middle", TEAL, "math"), text(201, 449, "two independent normals", 15, 500, "middle", MUTED), text(201, 470, "one correlated pair", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "Correlation map 与对角线的相交", TEAL)
    x0, x1, y0, y1 = 455, 752, 105, 380
    out += [line(x0, y1, x1, y1, GRID, 2), line(x0, y0, x0, y1, GRID, 2)]
    diag = []
    ordered = []
    critical = []
    chaotic = []
    for i in range(101):
        c = i / 100
        x = x0 + c * (x1 - x0)
        def yy(v):
            return y1 - v * (y1 - y0)
        relu = (math.sqrt(max(0.0, 1 - c * c)) + (math.pi - math.acos(c)) * c) / math.pi
        diag.append((x, yy(c)))
        ordered.append((x, yy(0.72 * c + 0.28)))
        critical.append((x, yy(relu)))
        chaotic.append((x, yy(0.75 * c + 0.25 * c * c)))
    out += [polyline(diag, GRID, 2, "6 5"), polyline(ordered, BLUE, 3), polyline(critical, TEAL, 3), polyline(chaotic, RED, 3)]
    out += [text(465, 126, "ordered: slope < 1", 15, 700, fill=BLUE), text(465, 151, "critical: slope = 1", 15, 700, fill=TEAL), text(465, 176, "chaotic: slope > 1", 15, 700, fill=RED)]
    out += [text(x1, y1 + 29, "c_l", 15, 600, "end", MUTED, "math")]
    out += [rect(455, 418, 297, 67, RED, "#FFF5F2", 6, 2), text(603, 445, "chi_1 = C'(1)", 17, 700, "middle", RED, "math"), text(603, 470, "local slope, not global geometry", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "Depth scale 与证据边界", RED)
    x0, x1, y0, y1 = 845, 1130, 105, 305
    out += [line(x0, y1, x1, y1, GRID, 2), line(x0, y0, x0, y1, GRID, 2)]
    decay, edge, grow = [], [], []
    for i in range(81):
        depth = i / 80 * 40
        x = x0 + i / 80 * (x1 - x0)
        vals = (0.72 ** depth, 1 / (1 + 0.12 * depth), min(1.0, 0.02 * (1.12 ** depth)))
        decay.append((x, y1 - vals[0] * (y1 - y0)))
        edge.append((x, y1 - vals[1] * (y1 - y0)))
        grow.append((x, y1 - vals[2] * (y1 - y0)))
    out += [polyline(decay, BLUE, 3), polyline(edge, TEAL, 3), polyline(grow, RED, 3)]
    out += [text(858, 126, "ordered delta", 15, 700, fill=BLUE), text(858, 151, "critical higher order", 15, 700, fill=TEAL), text(858, 176, "chaotic delta", 15, 700, fill=RED)]
    out += [text(1128, 331, "depth", 15, 600, "end", MUTED)]
    out += [rect(845, 365, 285, 42, BLUE, BG, 5, 2), text(987, 391, "pairwise correlation", 15, 650, "middle", BLUE)]
    out += [line(987, 410, 987, 428, INK, 1.8, marker="a3")]
    out += [rect(845, 433, 285, 42, TEAL, BG, 5, 2), text(987, 459, "random-direction JVP / VJP", 15, 650, "middle", TEAL)]
    out += [line(987, 478, 987, 492, INK, 1.8, marker="a3")]
    out += [text(987, 513, "full spectrum still separate", 15, 700, "middle", RED)]
    return finish(out, "Edge of Chaos 是 correlation map 的局部临界条件；从 pairwise geometry 到全谱和训练仍有明确证据缺口。")


def orthogonal_dynamical_isometry():
    out = begin(
        "Orthogonal Initialization 与 Dynamical Isometry 的谱层级",
        "Square 与 semi-orthogonal matrices 只在相应子空间保长；nonlinear derivative masks 改变深层 Jacobian；平均平方谱不能替代极端奇异值。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Square / Semi-Orthogonal Maps", BLUE)
    specs = ((70, 125, 62, 62, "square", "all dirs", BLUE), (166, 105, 52, 102, "tall", "input dirs", TEAL), (252, 137, 94, 44, "wide", "row space", RED))
    for x, y, w, h, title, detail, color in specs:
        out += [rect(x, y, w, h, color, "#F8FAFC", 3, 2), text(x + w / 2, y + h + 28, title, 15, 700, "middle", color), text(x + w / 2, y + h + 51, detail, 15, 500, "middle", MUTED)]
        for k in range(3):
            yy = y + 14 + k * min(22, (h - 20) / 2)
            out += [line(x + 10, yy, x + w - 10, yy, color, 1.8)]
    out += [rect(55, 295, 292, 66, BLUE, BG, 6, 2), text(201, 322, "Q^T Q = I: input norm preserved", 15, 650, "middle", BLUE, "math"), text(201, 348, "requires rows >= columns", 15, 500, "middle", MUTED)]
    out += [rect(55, 390, 292, 82, RED, "#FFF5F2", 6, 2), text(201, 418, "Q Q^T = I", 15, 650, "middle", RED, "math"), text(201, 444, "kernel remains when input wider", 15, 500, "middle", MUTED), text(201, 466, "state the protected subspace", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "Nonlinearity reshapes Jacobian", TEAL)
    chain = ((445, "W1", BLUE), (520, "D1", RED), (595, "W2", BLUE), (670, "D2", RED))
    for i, (x, lab, color) in enumerate(chain):
        node(out, x, 112, 55, 48, lab, color, size=16)
        if i < len(chain) - 1:
            out += [line(x + 58, 136, chain[i + 1][0] - 4, 136, INK, 2, marker="a3")]
    out += [text(600, 205, "J = D2 W2 D1 W1", 17, 700, "middle", TEAL, "math")]
    bars = ((475, 0.94, BLUE), (520, 0.64, TEAL), (565, 0.16, RED), (610, 0.78, TEAL), (655, 0.05, RED), (700, 0.52, BLUE))
    out += [line(455, 385, 748, 385, GRID, 2)]
    for x, val, color in bars:
        h = val * 140
        out += [rect(x, 385 - h, 24, h, color, color, 1, 1), text(x + 12, 409, f"{val:.2f}", 15, 600, "middle", MUTED)]
    out += [text(600, 445, "orthogonal W does not flatten D", 16, 700, "middle", RED), text(600, 474, "ReLU zeros can remove directions", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "谱主张不可混用", RED)
    out += [rect(845, 105, 285, 70, BLUE, BG, 6, 2), text(862, 133, "1  mean squared singular value", 15, 700, fill=BLUE), text(862, 158, "average random direction", 15, 500, fill=MUTED)]
    out += [rect(845, 205, 285, 70, TEAL, BG, 6, 2), text(862, 233, "2  condition number", 15, 700, fill=TEAL), text(862, 258, "extreme directions", 15, 500, fill=MUTED)]
    out += [rect(845, 305, 285, 70, RED, "#FFF5F2", 6, 2), text(862, 333, "3  dynamical isometry", 15, 700, fill=RED), text(862, 358, "all relevant s_i near 1", 15, 500, fill=MUTED)]
    out += [line(987, 178, 987, 198, INK, 1.8, marker="a3"), line(987, 278, 987, 298, INK, 1.8, marker="a3")]
    out += [rect(845, 410, 285, 78, RED, "#FFF5F2", 6, 2), text(987, 438, "mean = 1 can hide", 16, 700, "middle", RED), text(987, 463, "one near-zero singular direction", 15, 500, "middle", MUTED)]
    return finish(out, "单层正交是谱校准基线；全网 dynamical isometry 还需处理 derivative、shape、operator 与训练漂移。")


def zero_init_symmetry_boundaries():
    out = begin(
        "Zero Initialization：对称不变子空间与结构化例外",
        "完整 hidden-unit bundles 若相同，会被等变的 deterministic update 保持；bias、single layer、zero head 与 residual zero-last 各有不同第一步梯度。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Identical units 沿对称对角线更新", BLUE)
    for k, x in enumerate((75, 180, 285)):
        out += [circle(x, 145, 24, BLUE, BG, 2), circle(x, 225, 24, TEAL, BG, 2)]
        out += [text(x, 151, "u1", 15, 700, "middle", BLUE), text(x, 231, "u2", 15, 700, "middle", TEAL)]
        if k < 2:
            out += [line(x + 27, 145, x + 74, 145, BLUE, 2.3, marker="a0"), line(x + 27, 225, x + 74, 225, TEAL, 2.3, marker="a1")]
    out += [line(75, 185, 309, 185, RED, 1.8, "6 5"), text(192, 178, "theta1 = theta2", 15, 700, "middle", RED, "math")]
    out += [rect(55, 305, 292, 64, BLUE, BG, 6, 2), text(201, 333, "Delta theta remains zero", 17, 700, "middle", BLUE, "math"), text(201, 357, "same gradient + same optimizer state", 15, 500, "middle", MUTED)]
    out += [rect(55, 402, 292, 74, RED, "#FFF5F2", 6, 2), text(201, 430, "bundle = incoming + bias + outgoing", 15, 650, "middle", RED), text(201, 456, "one matrix alone is not the orbit", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "第一步梯度路径决定能否离开零", TEAL)
    rows = ((105, "all-zero MLP", "W2 blocks W1; h may be zero", RED), (228, "zero output head", "head learns; encoder waits", BLUE), (351, "residual zero-last", "identity path stays open", TEAL))
    for y, title, detail, color in rows:
        out += [rect(445, y, 310, 86, color, BG if color != RED else "#FFF5F2", 6, 2), text(462, y + 29, title, 16, 700, fill=color), text(462, y + 56, detail, 15, 500, fill=MUTED)]
        out += [circle(715, y + 43, 13, color, BG, 2), line(682, y + 43, 699, y + 43, color, 2, marker="a0" if color == BLUE else "a1" if color == TEAL else "a2")]
    out += [text(600, 476, "trace the loss-to-parameter chain", 15, 700, "middle", MUTED)]

    heading(out, 830, "C", "逐对象判断，而不是一句口诀", RED)
    items = ((105, "hidden weights", "usually random", RED), (171, "hidden bias", "zero often fine", TEAL), (237, "linear / logistic", "zero can move", BLUE), (303, "zero head", "encoder waits", TEAL), (369, "residual last", "skip protected", BLUE), (435, "padding row", "intentional fixed zero", RED))
    for y, left, right, color in items:
        out += [rect(845, y, 285, 48, color, BG, 4, 1.8), text(862, y + 30, left, 15, 700, fill=color), text(1115, y + 30, right, 15, 500, "end", MUTED)]
    return finish(out, "零初始化的判据是完整 symmetry orbit 与第一步计算图；结构化例外必须逐参数说明。")


def lsuv_fixup_diagnostic_loop():
    out = begin(
        "LSUV、Fixup 与现代初始化诊断闭环",
        "LSUV 用 calibration data 逐层校准输出 variance；Fixup 用 residual depth 缩放 branch update；可靠流程还要测相关、反向、谱与更新系统。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "LSUV：逐层测量与反馈重缩放", BLUE)
    node(out, 55, 105, 130, 50, "orthogonal W", BLUE, size=15)
    node(out, 215, 105, 132, 50, "forward batch", TEAL, size=15)
    out += [line(188, 130, 211, 130, INK, 2, marker="a3")]
    node(out, 215, 208, 132, 50, "measure Var", TEAL, size=15)
    out += [line(281, 159, 281, 204, TEAL, 2.4, marker="a1")]
    node(out, 55, 208, 130, 50, "W / sqrt(v)", RED, size=15)
    out += [line(211, 233, 189, 233, RED, 2.4, marker="a2"), path("M120 205C120 170 220 176 242 201", BLUE, 2.0, "none", "6 5", "a0")]
    out += [rect(55, 305, 292, 70, BLUE, BG, 6, 2), text(201, 333, "stop when |v - 1| < tol", 16, 700, "middle", BLUE, "math"), text(201, 358, "or trials reach Tmax", 15, 500, "middle", MUTED)]
    out += [rect(55, 402, 292, 74, RED, "#FFF5F2", 6, 2), text(201, 430, "declare axes / mode / batch", 15, 700, "middle", RED), text(201, 456, "one-time calibration, not BatchNorm", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "Fixup：Depth-aware Branch", TEAL)
    node(out, 445, 108, 70, 48, "x", BLUE, size=17)
    node(out, 690, 108, 70, 48, "x + F", TEAL, size=15)
    out += [line(518, 132, 686, 132, BLUE, 3, marker="a0")]
    node(out, 495, 225, 68, 45, "W1*a", TEAL, size=15)
    node(out, 585, 225, 68, 45, "...", TEAL, size=15)
    node(out, 675, 225, 68, 45, "Wm=0", RED, size=15)
    out += [line(480, 157, 515, 220, INK, 2, marker="a3"), line(566, 247, 581, 247, INK, 2, marker="a3"), line(656, 247, 671, 247, INK, 2, marker="a3"), line(709, 220, 722, 160, RED, 2, marker="a2")]
    out += [rect(445, 320, 310, 58, TEAL, "#ECFDF5", 6, 2), text(600, 346, "a = L^(-1/(2m-2))", 16, 700, "middle", TEAL, "math"), text(600, 369, "a^(m-1) = L^(-1/2)", 15, 600, "middle", MUTED, "math")]
    out += [rect(445, 410, 310, 65, RED, "#FFF5F2", 6, 2), text(600, 437, "zero last + scalar multiplier / bias", 15, 700, "middle", RED), text(600, 461, "the complete recipe matters", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "定位第一处失效", RED)
    stages = ((105, "1 parameter / fan / dtype", BLUE), (164, "2 forward moments", TEAL), (223, "3 input correlation", BLUE), (282, "4 backward JVP / VJP", TEAL), (341, "5 spectrum / rank / extremes", RED), (400, "6 update / AMP / distributed", RED))
    for i, (y, label, color) in enumerate(stages):
        out += [rect(845, y, 285, 40, color, BG, 4, 1.8), text(987, y + 26, label, 15, 650, "middle", color)]
        if i < len(stages) - 1:
            out += [line(987, y + 42, 987, stages[i + 1][0] - 3, INK, 1.5, marker="a3")]
    out += [text(987, 478, "modify the first failing mechanism", 15, 700, "middle", RED), text(987, 505, "then rerun every downstream check", 15, 500, "middle", MUTED)]
    return finish(out, "初始化是可证伪流程：解析先验、仪表化 dry run、局部修正与多 seed 训练证据缺一不可。")


FIGURES = {
    "fig-correlation-edge-of-chaos-v2.svg": correlation_edge_of_chaos,
    "fig-orthogonal-dynamical-isometry-v2.svg": orthogonal_dynamical_isometry,
    "fig-zero-init-symmetry-boundaries-v2.svg": zero_init_symmetry_boundaries,
    "fig-lsuv-fixup-diagnostic-loop-v2.svg": lsuv_fixup_diagnostic_loop,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
