#!/usr/bin/env python3
"""Generate deterministic NN-13--16 textbook figures.

The four plates share the repository palette and typography, but intentionally
use different visual grammars: adjoint operator board, stable-loss pipeline,
dual execution ledger, and verification/memory dashboard.  Only the Python
standard library is required.
"""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def activation_branch_broadcast():
    out = begin(
        "激活、分支与广播：反向是局部伴随的累加",
        "激活函数以局部斜率门控；fan-out 的各路径贡献在共享父节点相加；broadcast 与 gather 的伴随分别是 sum-to-shape 与 scatter-add。",
        (BLUE, TEAL, RED),
    )

    heading(out, 42, "A", "激活：上游乘局部斜率", BLUE)
    out += [line(58, 315, 352, 315, GRID, 2), line(205, 105, 205, 425, GRID, 2)]
    out += [path("M70 315L205 315L335 145", BLUE, 4), text(328, 132, "ReLU", 16, 700, "middle", BLUE)]
    samples = ((105, 315, "x<0", "slope 0", RED), (205, 315, "x=0", "rule", AMBER), (300, 190, "x>0", "slope 1", TEAL))
    for x, y, top, bottom, color in samples:
        out += [circle(x, y, 7, color, color), text(x, 362, top, 15, 650, "middle", color), text(x, 389, bottom, 15, 500, "middle", MUTED)]
    out += [rect(62, 432, 282, 55, TEAL, "#ECFDF5", 7, 2), text(203, 456, "z_bar = h_bar * phi'(z)", 17, 700, "middle", TEAL, "math"), text(203, 477, "mask controls one local path", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "分支：贡献必须相加", TEAL)
    pts = {"x": (465, 275), "id": (575, 155), "F": (575, 380), "+": (690, 275), "L": (760, 275)}
    for label, (x, y) in pts.items():
        color = BLUE if label == "x" else TEAL if label in ("id", "F") else RED
        out += [circle(x, y, 23, color, BG, 2.5), text(x, y + 6, label, 15, 700, "middle", color)]
    for a, b in (("x", "id"), ("x", "F"), ("id", "+"), ("F", "+"), ("+", "L")):
        x1, y1 = pts[a]; x2, y2 = pts[b]
        out += [line(x1 + 23, y1, x2 - 25, y2, INK, 2.2, marker="a3")]
    out += [path("M737 251C675 205 565 205 488 258", RED, 2.5, "none", "7 5", "a2")]
    out += [path("M737 299C675 345 565 345 488 292", RED, 2.5, "none", "7 5", "a2")]
    out += [rect(445, 430, 310, 58, RED, "#FFF5F2", 7, 2), text(600, 455, "x_bar = y_bar + J_F^T y_bar", 16, 700, "middle", RED, "math"), text(600, 477, "assignment would erase one path", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "复制的伴随是聚合", RED)
    out += [text(842, 105, "broadcast", 16, 700, fill=BLUE), rect(844, 125, 70, 54, BLUE, "#EFF6FF", 7, 2), text(879, 158, "b:[d]", 16, 700, "middle", BLUE)]
    for i in range(3):
        y = 112 + i * 55
        out += [line(917, 152, 985, y + 22, BLUE, 2.2, marker="a0"), rect(990, y, 130, 44, BLUE, BG, 6, 2), text(1055, y + 28, f"row {i+1}:[d]", 15, 650, "middle", BLUE)]
    out += [path("M1122 132C1160 168 1160 250 1122 286", RED, 2.5, "none", "6 5")]
    out += [text(1055, 315, "reverse: sum rows", 16, 700, "middle", RED)]
    out += [line(845, 345, 1135, 345, GRID, 2)]
    out += [text(842, 377, "gather: indices [2,2,1]", 16, 700, fill=TEAL)]
    out += [rect(844, 400, 290, 72, TEAL, "#ECFDF5", 7, 2), text(989, 427, "y_bar = [a,b,c]", 16, 650, "middle", TEAL, "math"), text(989, 454, "scatter-add -> x_bar=[c,a+b,0]", 15, 650, "middle", INK, "math")]
    return finish(out, "统一原则：每个 primitive 提供局部 VJP；共享路径求和，复制操作用其转置聚合。")


def softmax_cross_entropy_fused():
    out = begin(
        "Softmax–Cross-Entropy：稳定前向与融合反向",
        "先以最大值平移 logits，再用 log-sum-exp 直接形成 log-probability；归一化 target 下，融合梯度为 p-y，同时必须记录温度与 reduction 尺度。",
        (BLUE, TEAL, RED),
    )

    heading(out, 42, "A", "max-shift 改写，不改概率", BLUE)
    vals = ((105, 1000, 180, BLUE), (195, 999, 120, TEAL), (285, 998, 70, AMBER))
    out += [line(65, 335, 350, 335, GRID, 2)]
    for x, raw, height, color in vals:
        out += [rect(x - 27, 335 - height, 54, height, color, "#EFF6FF" if color == BLUE else "#ECFDF5", 4, 2), text(x, 360, str(raw), 15, 650, "middle", color)]
    out += [text(205, 405, "subtract m=max(z)=1000", 16, 700, "middle", RED), line(205, 418, 205, 444, RED, 2.5, marker="a2")]
    out += [rect(65, 455, 285, 42, TEAL, "#ECFDF5", 6, 2), text(207, 482, "shifted logits = [0,-1,-2]", 16, 700, "middle", TEAL, "math")]

    heading(out, 430, "B", "一条恒等式给出 p-y", TEAL)
    steps = (
        (108, "loss = LSE(z) - y^T z", BLUE),
        (218, "d LSE = p^T dz", TEAL),
        (328, "d loss = (p-y)^T dz", RED),
        (438, "z_bar = p-y", RED),
    )
    for i, (y, label, color) in enumerate(steps):
        out += [rect(445, y, 310, 58, color, BG if i < 3 else "#FFF5F2", 7, 2.3), text(600, y + 36, label, 17, 700, "middle", color, "math")]
        if i < len(steps) - 1:
            out += [line(600, y + 61, 600, y + 101, INK, 2.2, marker="a3")]

    heading(out, 830, "C", "尺度合同与曲率检查", RED)
    out += [text(845, 108, "per row gradient", 15, 700, fill=RED)]
    out += [rect(845, 126, 285, 54, RED, "#FFF5F2", 7, 2), text(987, 159, "(p-y) / tau", 18, 700, "middle", RED, "math")]
    contracts = (
        (215, "target sum", "1  (else alpha*p-y)", BLUE),
        (275, "temperature", "forward and backward", TEAL),
        (335, "reduction", "sum / valid-count mean", AMBER),
        (395, "mask", "padding contributes zero", BLUE),
    )
    for y, key, val, color in contracts:
        out += [text(845, y + 18, key, 15, 700, fill=color), text(965, y + 18, val, 15, 500, fill=INK), line(845, y + 29, 1130, y + 29, GRID, 1.3)]
    out += [rect(845, 462, 285, 42, TEAL, "#ECFDF5", 6, 2), text(987, 488, "H = diag(p) - p p^T  is PSD", 15, 650, "middle", TEAL, "math")]
    return finish(out, "稳定融合不是删掉数学步骤，而是把同一恒等式变成更安全、更少中间量的程序。")


def forward_reverse_ad_tape():
    out = begin(
        "Forward/Reverse AD：两种线性信息流与一份执行记录",
        "forward mode 让每个 primal 携带 tangent；reverse mode 先记录 tape，再从输出 seed 逆序回拉 cotangent；模式选择取决于输入与输出方向数。",
        (BLUE, TEAL, RED),
    )

    heading(out, 42, "A", "Forward：双轨前推", BLUE)
    labels = ((60, "x", "xdot"), (170, "u=f(x)", "J_f xdot"), (290, "y=g(u)", "J_g J_f xdot"))
    for i, (x, primal, tangent) in enumerate(labels):
        out += [rect(x, 120, 92 if i == 0 else 100, 50, BLUE, "#EFF6FF", 7, 2), text(x + (46 if i == 0 else 50), 151, primal, 15, 700, "middle", BLUE)]
        out += [rect(x, 245, 92 if i == 0 else 100, 55, TEAL, "#ECFDF5", 7, 2), text(x + (46 if i == 0 else 50), 278, tangent, 15, 650, "middle", TEAL, "math")]
        if i < 2:
            nx = labels[i + 1][0]
            out += [line(x + (94 if i == 0 else 102), 145, nx - 5, 145, BLUE, 2.7, marker="a0"), line(x + (94 if i == 0 else 102), 272, nx - 5, 272, TEAL, 2.7, marker="a1")]
    out += [rect(62, 370, 285, 92, BLUE, BG, 7, 2), text(204, 401, "one input seed -> one Jv", 17, 700, "middle", BLUE), text(204, 431, "no reverse tape required", 15, 500, "middle", MUTED), text(204, 454, "best when input directions are few", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "Reverse：tape 逆序回拉", TEAL)
    out += [text(445, 105, "forward tape", 15, 700, fill=BLUE)]
    tape = ((445, "x"), (535, "u, cache"), (650, "L"))
    for i, (x, label) in enumerate(tape):
        w = 78 if i != 1 else 100
        out += [rect(x, 125, w, 50, BLUE, "#EFF6FF", 7, 2), text(x + w / 2, 156, label, 15, 700, "middle", BLUE)]
        if i < 2:
            out += [line(x + w + 4, 150, tape[i + 1][0] - 5, 150, BLUE, 2.5, marker="a0")]
    out += [text(445, 235, "reverse cotangents", 15, 700, fill=RED)]
    back = ((650, "Lbar=1"), (535, "ubar"), (445, "xbar"))
    for i, (x, label) in enumerate(back):
        w = 78 if i != 1 else 100
        out += [rect(x, 255, w, 52, RED, "#FFF5F2", 7, 2), text(x + w / 2, 287, label, 15, 700, "middle", RED, "math")]
        if i < 2:
            next_x, _ = back[i + 1]
            out += [line(x - 5, 281, next_x + (105 if i == 0 else 83), 281, RED, 2.7, marker="a2")]
    out += [rect(445, 370, 310, 92, TEAL, BG, 7, 2), text(600, 401, "one output seed -> one u^T J", 17, 700, "middle", TEAL), text(600, 431, "stores or recomputes residuals", 15, 500, "middle", MUTED), text(600, 454, "best when output directions are few", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "模式选择看方向数", RED)
    out += [text(845, 105, "full Jacobian  J:[m,n]", 16, 700, fill=INK)]
    out += [rect(845, 130, 285, 174, GRID, "#F8FAFC", 4, 1.5)]
    out += [line(987, 130, 987, 304, GRID, 1.5), line(845, 190, 1130, 190, GRID, 1.5), line(845, 248, 1130, 248, GRID, 1.5)]
    out += [text(916, 168, "method", 15, 700, "middle", MUTED), text(1058, 168, "sweeps", 15, 700, "middle", MUTED)]
    out += [text(916, 227, "forward", 16, 700, "middle", BLUE), text(1058, 227, "n seeds", 16, 700, "middle", BLUE)]
    out += [text(916, 285, "reverse", 16, 700, "middle", TEAL), text(1058, 285, "m seeds", 16, 700, "middle", TEAL)]
    node(out, 845, 330, 285, 60, "scalar loss: m=1 -> reverse", TEAL, "#ECFDF5", 16)
    node(out, 845, 415, 285, 60, "few directions: use JVP/VJP actions", RED, "#FFF5F2", 15)
    return finish(out, "AD 精确传播程序 primitive 的导数规则；它既不是符号展开，也不是有限差分。")


def gradient_checkpoint_higher_order():
    out = begin(
        "梯度验证、Checkpointing 与高阶微分边界",
        "有限差分误差随步长呈 U 形；checkpoint 以重算换存储；Hessian-vector product 通过一阶算子组合获得，但状态、随机性和不可微点必须单独审计。",
        (BLUE, TEAL, RED),
    )

    heading(out, 42, "A", "gradient check：找 U 形窗口", BLUE)
    out += [line(70, 430, 350, 430, GRID, 2), line(70, 430, 70, 105, GRID, 2)]
    out += [text(210, 470, "log step size", 15, 650, "middle", MUTED), text(48, 260, "error", 15, 650, "middle", MUTED)]
    out += [path("M82 125C135 150 155 260 208 340C250 402 295 320 340 145", RED, 4)]
    out += [line(208, 342, 208, 430, TEAL, 2, "6 5"), circle(208, 342, 7, TEAL, TEAL)]
    out += [text(125, 175, "truncation", 15, 700, "middle", BLUE), text(298, 178, "roundoff", 15, 700, "middle", RED)]
    out += [rect(75, 500 - 58, 270, 58, TEAL, "#ECFDF5", 7, 2), text(210, 465, "central FD: O(h^2) + O(u/h)", 15, 700, "middle", TEAL, "math"), text(210, 488, "scan h; do not trust one step", 15, 500, "middle", MUTED)]

    heading(out, 430, "B", "checkpoint：存锚点，重放区间", TEAL)
    y = 210
    for i in range(9):
        x = 438 + i * 38
        color = TEAL if i in (0, 3, 6, 8) else GRID
        fill = "#ECFDF5" if color == TEAL else BG
        out += [rect(x, y, 27, 48, color, fill, 4, 2), text(x + 13.5, y + 30, str(i), 15, 650, "middle", color if color != GRID else MUTED)]
        if i < 8:
            out += [line(x + 29, y + 24, x + 36, y + 24, INK, 1.8, marker="a3")]
    out += [text(438, 125, "forward: retain only selected states", 16, 700, fill=TEAL)]
    out += [path("M555 285C575 340 690 340 751 285", RED, 2.5, "none", "7 5", "a2"), text(650, 365, "reverse: recompute 6 -> 7 -> 8", 15, 700, "middle", RED)]
    out += [rect(445, 405, 310, 78, BLUE, "#EFF6FF", 7, 2), text(600, 432, "uniform segmentation: memory ~ n/k + k", 15, 700, "middle", BLUE, "math"), text(600, 458, "choose k near sqrt(n); schedule matters", 15, 500, "middle", MUTED)]

    heading(out, 830, "C", "HVP 与语义边界", RED)
    node(out, 845, 110, 120, 56, "v", BLUE, "#EFF6FF", 18)
    node(out, 1005, 110, 125, 56, "H v", TEAL, "#ECFDF5", 18)
    out += [line(970, 138, 1000, 138, TEAL, 3, marker="a1"), text(986, 96, "JVP(grad)", 15, 650, "middle", TEAL)]
    out += [text(845, 210, "No full Hessian needed", 16, 700, fill=TEAL)]
    checks = (
        (250, "RNG/state replay", "same executed function", BLUE),
        (315, "kinks/branches", "program derivative convention", AMBER),
        (380, "create graph", "retain derivative operations", TEAL),
        (445, "memory claim", "include tape + workspace", RED),
    )
    for y0, key, val, color in checks:
        out += [rect(845, y0, 285, 48, color, BG, 6, 2), text(857, y0 + 20, key, 15, 700, fill=color), text(857, y0 + 40, val, 15, 500, fill=INK)]
    return finish(out, "可信梯度需要三类证据同时成立：数值一致、可回放的程序语义、明确的时间—内存预算。")


FIGURES = {
    "fig-activation-branch-broadcast-v2.svg": activation_branch_broadcast,
    "fig-softmax-cross-entropy-fused-v2.svg": softmax_cross_entropy_fused,
    "fig-forward-reverse-ad-tape-v2.svg": forward_reverse_ad_tape,
    "fig-gradient-checkpoint-higher-order-v2.svg": gradient_checkpoint_higher_order,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
