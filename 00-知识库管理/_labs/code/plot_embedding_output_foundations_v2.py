#!/usr/bin/env python3
"""Generate deterministic NN-49--52 embedding/output textbook figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def embedding_lookup_sparse_gradient():
    out = begin(
        "Embedding Lookup：选择矩阵、重复索引与稀疏更新",
        "查表等于 one-hot 选择矩阵乘法；反向把每个位置的上游梯度散射并按重复 token 求和；稀疏梯度表示不等于整条优化链都稀疏。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "lookup = row selection", BLUE)
    out += [rect(52, 92, 128, 292, BLUE, "#EFF6FF", 5, 2),
            text(116, 120, "E [4 x 2]", 16, 700, "middle", BLUE)]
    rows = (("e0", "[ 1, 0 ]"), ("e1", "[ 0, 1 ]"),
            ("e2", "[ 2,-1 ]"), ("e3", "[-1, 3 ]"))
    for i, (lab, val) in enumerate(rows):
        y = 150 + i * 54
        out += [text(68, y, lab, 15, 700, fill=TEAL if i in (1, 2) else MUTED),
                text(164, y, val, 15, 650, "end", INK)]
    out += [text(265, 120, "ids", 16, 700, "middle", RED),
            text(265, 160, "2", 17, 700, "middle", RED),
            text(265, 216, "1", 17, 700, "middle", RED),
            text(265, 272, "2", 17, 700, "middle", RED),
            line(287, 156, 297, 156, TEAL, 2.2, marker="a1"),
            line(287, 212, 297, 212, TEAL, 2.2, marker="a1"),
            line(287, 268, 297, 268, TEAL, 2.2, marker="a1"),
            text(305, 160, "[ 2,-1 ]", 15, 650, fill=INK),
            text(305, 216, "[ 0, 1 ]", 15, 650, fill=INK),
            text(305, 272, "[ 2,-1 ]", 15, 650, fill=INK),
            rect(52, 420, 310, 62, TEAL, "#ECFDF5", 5, 2),
            text(207, 447, "X = S E = E[ids]", 17, 700, "middle", TEAL),
            text(207, 471, "gather avoids one-hot storage", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "backward = scatter-add", TEAL)
    out += [text(445, 104, "upstream rows", 16, 700, fill=INK)]
    gs = (("g0", "[ 1, 2 ]", BLUE), ("g1", "[-1,.5]", AMBER), ("g2", "[ 3,-1]", BLUE))
    for i, (lab, val, color) in enumerate(gs):
        y = 136 + i * 66
        out += [rect(445, y, 136, 44, color, BG, 4, 1.8),
                text(457, y + 28, f"{lab} {val}", 15, 700, fill=color)]
    out += [line(587, 158, 700, 158, BLUE, 2.2, marker="a0"),
            line(587, 224, 700, 224, AMBER, 2.2, marker="a3"),
            line(587, 290, 700, 290, BLUE, 2.2, marker="a0"),
            text(748, 162, "row 2", 15, 700, "end", BLUE),
            text(748, 228, "row 1", 15, 700, "end", AMBER),
            text(748, 294, "row 2", 15, 700, "end", BLUE),
            rect(445, 356, 315, 106, RED, "#FFF5F2", 5, 2),
            text(602, 386, "dE[2] = g0 + g2 = [4,1]", 15, 700, "middle", RED),
            text(602, 417, "dE[1] = g1 = [-1,.5]", 15, 650, "middle", INK),
            text(602, 446, "untouched rows are zero in lookup VJP", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "V x d cost ledger", RED)
    out += [rect(845, 96, 285, 78, BLUE, "#EFF6FF", 5, 2),
            text(987, 125, "parameters = V d", 17, 700, "middle", BLUE),
            text(987, 154, "lookup compute touches selected rows", 15, 600, "middle", MUTED),
            rect(845, 216, 285, 96, TEAL, "#ECFDF5", 5, 2),
            text(987, 246, "sparse gradient", 16, 700, "middle", TEAL),
            text(987, 276, "stores touched row updates", 15, 600, "middle", INK),
            text(987, 298, "optimizer support is restricted", 15, 600, "middle", MUTED),
            rect(845, 354, 285, 96, RED, "#FFF5F2", 5, 2),
            text(987, 384, "dense output use", 16, 700, "middle", RED),
            text(987, 414, "usually gradients all V rows", 15, 600, "middle", INK),
            text(987, 438, "tying can destroy input-only sparsity", 15, 600, "middle", MUTED)]
    return finish(out, "查表省去 one-hot 物化；重复 token 必须 scatter-add；稀疏收益要沿 optimizer、decay、通信整链验证。")


def embedding_geometry_anisotropy():
    out = begin(
        "Embedding Geometry：norm、angle、centering 与各向异性",
        "内积同时混合长度与夹角，cosine 删除正尺度但不平移不变；共同均值可抬高 pairwise cosine，centering 后仍要看 covariance spectrum 与任务。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "三种相似度不是同一问题", BLUE)
    out += [text(60, 105, "a=(3,4), b=(4,3)", 17, 700, fill=INK),
            rect(52, 142, 310, 74, BLUE, "#EFF6FF", 5, 2),
            text(207, 172, "dot = 24", 17, 700, "middle", BLUE),
            text(207, 198, "uses norm and angle", 15, 600, "middle", MUTED),
            rect(52, 244, 310, 74, TEAL, "#ECFDF5", 5, 2),
            text(207, 274, "cos = 24 / 25 = .96", 17, 700, "middle", TEAL),
            text(207, 300, "positive-scale invariant", 15, 600, "middle", MUTED),
            rect(52, 346, 310, 74, RED, "#FFF5F2", 5, 2),
            text(207, 376, "distance = sqrt(2)", 17, 700, "middle", RED),
            text(207, 402, "translation invariant", 15, 600, "middle", MUTED),
            text(207, 470, "metric choice changes nearest neighbors", 15, 700, "middle", AMBER)]

    heading(out, 430, "B", "共同均值形成窄锥", TEAL)
    ox, oy = 470, 390
    out += [line(ox, oy, 748, oy, GRID, 1.8), line(ox, oy, ox, 100, GRID, 1.8)]
    ends = ((720, 180, BLUE), (730, 245, TEAL), (710, 305, AMBER), (735, 350, RED))
    for x, y, color in ends:
        out += [line(ox, oy, x, y, color, 2.5, marker="a0")]
    out += [text(610, 125, "uncentered vectors", 16, 700, "middle", INK),
            text(610, 420, "large common mean -> high cosine", 15, 700, "middle", RED),
            rect(445, 448, 315, 46, TEAL, "#ECFDF5", 4, 1.8),
            text(602, 477, "center first; then inspect covariance spectrum", 15, 700, "middle", TEAL)]

    heading(out, 830, "C", "变换不变性与诊断", RED)
    transforms = (
        ("orthogonal Q", "dot / cos / dist", BLUE),
        ("positive scale", "cos only", TEAL),
        ("common shift", "distance only", AMBER),
        ("general invertible", "none guaranteed", RED),
    )
    for i, (name, keep, color) in enumerate(transforms):
        y = 94 + i * 80
        out += [rect(845, y, 285, 58, color, BG, 4, 1.8),
                text(860, y + 24, name, 15, 700, fill=color),
                text(1115, y + 43, keep, 15, 600, "end", MUTED)]
    out += [text(845, 434, "anisotropy is a family of tests:", 15, 700, fill=INK),
            text(845, 462, "mean | pairwise cosine | spectrum", 15, 650, fill=TEAL),
            text(845, 488, "effective rank | local clusters | task", 15, 650, fill=RED)]
    return finish(out, "几何结论必须声明对象、是否 centering、metric 与允许的重参数化；单个 cosine 不能代表全部表示质量。")


def weight_tying_shared_gradient():
    out = begin(
        "Weight Tying：同一矩阵，两种角色，一次梯度求和",
        "输入端用 E 的一行编码 token，输出端用 E 的全部行作为类别 prototypes；共享减少参数但加入约束，反向梯度是 lookup 与 classifier 两条 VJP 的和。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "共享矩阵的两条前向路径", BLUE)
    node(out, 52, 104, 86, 48, "token i", BLUE)
    node(out, 170, 96, 112, 56, "E^T e_i", TEAL, size=15)
    out += [line(143, 128, 165, 125, BLUE, 2.2, marker="a0"),
            text(220, 184, "input row", 15, 650, "middle", MUTED)]
    node(out, 52, 280, 86, 48, "hidden h", RED)
    node(out, 170, 272, 112, 56, "E h + b", AMBER, size=15)
    out += [line(143, 304, 165, 301, RED, 2.2, marker="a2"),
            text(220, 360, "all output rows", 15, 650, "middle", MUTED),
            rect(52, 414, 310, 68, BLUE, "#EFF6FF", 5, 2),
            text(207, 442, "E [V x d]", 17, 700, "middle", BLUE),
            text(207, 469, "direct tie requires hidden dimension d", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "shared Parameter 的 VJP 相加", TEAL)
    out += [rect(445, 98, 315, 88, BLUE, "#EFF6FF", 5, 2),
            text(602, 128, "lookup contribution", 16, 700, "middle", BLUE),
            text(602, 158, "e_i g_x^T  (row sparse)", 15, 650, "middle", INK),
            rect(445, 226, 315, 88, RED, "#FFF5F2", 5, 2),
            text(602, 256, "output contribution", 16, 700, "middle", RED),
            text(602, 286, "(p-y) h^T  (usually dense)", 15, 650, "middle", INK),
            line(602, 321, 602, 365, INK, 2.2, marker="a3"),
            rect(445, 374, 315, 82, TEAL, "#ECFDF5", 5, 2),
            text(602, 405, "dE = dE_input + dE_output", 16, 700, "middle", TEAL),
            text(602, 435, "plus every other shared use", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "参数节省与函数约束", RED)
    out += [rect(845, 96, 285, 84, BLUE, "#EFF6FF", 5, 2),
            text(987, 126, "untied: E [Vxd] + U [Vxd]", 15, 700, "middle", BLUE),
            text(987, 156, "two vocabulary matrices", 15, 600, "middle", MUTED),
            rect(845, 218, 285, 84, TEAL, "#ECFDF5", 5, 2),
            text(987, 248, "tied: U = E", 16, 700, "middle", TEAL),
            text(987, 278, "save Vd parameters", 15, 650, "middle", INK),
            rect(845, 340, 285, 104, RED, "#FFF5F2", 5, 2),
            text(987, 370, "if d_h != d", 16, 700, "middle", RED),
            text(987, 400, "z = E P h + b", 15, 650, "middle", INK),
            text(987, 428, "projection changes count and geometry", 15, 600, "middle", MUTED),
            text(987, 482, "fewer parameters != free equivalence", 15, 700, "middle", AMBER)]
    return finish(out, "共享参数既节省一个词表矩阵，也把输入表示和输出分类器耦合；必须同时审计两条梯度、维度与尺度。")


def softmax_output_parameterization():
    out = begin(
        "Softmax Output：logit 差、温度与概率单纯形",
        "线性 head 产生未归一化 logits；Softmax 只依赖两两差并映到单纯形内部；正尺度保持 argmax 却改变熵、梯度和校准，大词表仍需全量归一化。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "从 hidden 到 categorical law", BLUE)
    node(out, 52, 105, 80, 48, "h", BLUE)
    node(out, 170, 96, 108, 56, "W h + b", TEAL, size=15)
    node(out, 52, 240, 108, 52, "logits z", TEAL, size=15)
    node(out, 220, 232, 112, 56, "softmax", RED, size=15)
    out += [line(137, 129, 165, 125, BLUE, 2.2, marker="a0"),
            path("M224 157V205H106V235", TEAL, 2.2, "none", None, "a1"),
            line(165, 266, 215, 260, RED, 2.2, marker="a2"),
            rect(52, 342, 310, 82, BLUE, "#EFF6FF", 5, 2),
            text(207, 372, "log p_i / p_j = z_i - z_j", 16, 700, "middle", BLUE),
            text(207, 402, "only pairwise differences are identifiable", 15, 600, "middle", MUTED),
            text(207, 476, "finite logits -> interior probabilities", 15, 700, "middle", RED)]

    heading(out, 430, "B", "shift gauge 与 temperature", TEAL)
    out += [rect(445, 96, 315, 82, TEAL, "#ECFDF5", 5, 2),
            text(602, 126, "softmax(z + c1) = softmax(z)", 15, 700, "middle", TEAL),
            text(602, 154, "fix gauge: max=0 or sum z=0", 15, 600, "middle", MUTED)]
    temps = (("tau < 1", "sharper", RED), ("tau = 1", "baseline", BLUE), ("tau > 1", "flatter", TEAL))
    for i, (tau, desc, color) in enumerate(temps):
        y = 222 + i * 68
        out += [rect(445, y, 315, 46, color, BG, 4, 1.7),
                text(462, y + 29, tau, 15, 700, fill=color),
                text(742, y + 29, desc, 15, 650, "end", MUTED)]
    out += [text(602, 454, "dH/dtau = Var_p(z) / tau^3 >= 0", 15, 700, "middle", AMBER),
            text(602, 484, "argmax stays; probabilities and gradients change", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "边界、数值与大词表", RED)
    out += [rect(845, 94, 285, 76, BLUE, "#EFF6FF", 5, 2),
            text(987, 123, "stable value", 16, 700, "middle", BLUE),
            text(987, 151, "subtract max + logsumexp", 15, 650, "middle", INK),
            rect(845, 208, 285, 76, TEAL, "#ECFDF5", 5, 2),
            text(987, 237, "probability boundary", 16, 700, "middle", TEAL),
            text(987, 265, "p_i=0 needs infinite logit gap", 15, 600, "middle", MUTED),
            rect(845, 322, 285, 92, RED, "#FFF5F2", 5, 2),
            text(987, 351, "full vocabulary", 16, 700, "middle", RED),
            text(987, 380, "logits / normalize over V", 15, 650, "middle", INK),
            text(987, 402, "compute, memory and communication", 15, 600, "middle", MUTED),
            text(987, 468, "confidence != calibration", 15, 700, "middle", AMBER)]
    return finish(out, "Softmax 定义的是 logit 差的概率参数化；scale、bias、mask、数值实现与词表成本都属于同一个输出合同。")


FIGURES = {
    "fig-embedding-lookup-sparse-gradient-v2.svg": embedding_lookup_sparse_gradient,
    "fig-embedding-geometry-anisotropy-v2.svg": embedding_geometry_anisotropy,
    "fig-weight-tying-shared-gradient-v2.svg": weight_tying_shared_gradient,
    "fig-softmax-output-parameterization-v2.svg": softmax_output_parameterization,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
