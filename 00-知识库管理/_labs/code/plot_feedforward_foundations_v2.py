#!/usr/bin/env python3
"""Generate NN-01--04 textbook figures for feedforward foundations.

The four plates share the course paper-and-ink palette, but use distinct
visual grammars: geometric construction, tensor ledger, update trajectory,
and computation flow.  All content is deterministic and self-contained.
"""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def neuron_affine_hyperplane():
    out = begin(
        "人工神经元：仿射分数、超平面与激活出口",
        "输入和权重先形成仿射分数；权重是等值超平面的法向量，偏置移动边界；激活函数再决定输出范围与语义。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "从输入坐标到一个 score", BLUE)
    for y, lab, val in ((112, "x1", "2"), (202, "x2", "−1"), (292, "x3", "3")):
        out += [circle(80, y, 22, BLUE, BG, 2.5), text(80, y + 6, lab, 16, 700, "middle", BLUE)]
        out += [text(122, y + 6, val, 16, 650), line(148, y, 245, 220, GRID, 2)]
    out += [circle(270, 220, 42, TEAL, "#ECFDF5", 3), text(270, 212, "Σ", 28, 700, "middle", TEAL), text(270, 239, "+ b", 16, 650, "middle", TEAL)]
    out += [line(313, 220, 365, 220, INK, 2.5, marker="a3"), text(340, 204, "z", 18, 700, "middle")]
    out += [text(45, 375, "x,w ∈ R^d;  b,z ∈ R", 17, 650, cls="math"), text(45, 414, "z = wᵀx + b", 21, 700, fill=BLUE, cls="math")]
    out += [text(45, 461, "先是 affine score；此时还没有概率语义。", 15, fill=MUTED)]

    heading(out, 430, "B", "法向量、平移与距离", TEAL)
    out += [line(458, 430, 758, 430, GRID, 1.5), line(475, 470, 475, 95, GRID, 1.5)]
    out += [path("M455 365L755 160", TEAL, 4), text(700, 150, "wᵀx+b=0", 16, 700, fill=TEAL)]
    out += [circle(650, 355, 8, RED, RED, 2), text(664, 376, "x", 17, 700, fill=RED)]
    out += [line(650, 355, 573, 242, RED, 3, "7 5", "a2"), text(635, 277, "signed distance", 15, 650, "middle", fill=RED)]
    out += [line(573, 242, 635, 200, BLUE, 4, marker="a0"), text(641, 203, "w", 18, 700, fill=BLUE)]
    out += [text(430, 470, "d±(x,H)= (wᵀx+b)/||w||₂", 17, 650, cls="math"), text(430, 507, "b 移动等值面；w 决定方向与 score 尺度。", 15, fill=MUTED)]

    heading(out, 830, "C", "同一 z，四种不同出口", RED)
    out += [line(855, 405, 1135, 405, GRID, 1.5), line(980, 455, 980, 95, GRID, 1.5)]
    out += [line(850, 405, 1135, 125, BLUE, 2.8), text(1095, 135, "identity", 15, 700, fill=BLUE)]
    out += [path("M850 405L980 405L980 145L1135 145", RED, 2.8), text(1085, 168, "step", 15, 700, fill=RED)]
    out += [path("M850 390C910 388 935 355 980 275C1025 195 1060 165 1135 163", TEAL, 3), text(1055, 207, "sigmoid", 15, 700, fill=TEAL)]
    out += [path("M850 405L980 405L1135 250", INK, 2.5), text(1088, 270, "ReLU", 15, 700)]
    out += [text(842, 468, "activation 决定值域；loss 与校准决定统计语义。", 15, fill=MUTED), text(842, 502, "score ≠ probability ≠ hard decision", 16, 700, fill=RED)]
    return finish(out, "一个神经元先测量输入沿 w 的位置，再由 activation 与任务合同解释这个测量。")


def dense_layer_shapes():
    out = begin(
        "Dense layer：矩阵形状、广播与资源账本",
        "多个神经元的权重列组成矩阵；batch 与 sequence 轴被保留，最后 feature 轴被映射；参数、计算、激活存储和秩需要分别计数。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "矩阵块先核对 contracted axis", BLUE)
    out += [rect(55, 125, 105, 230, BLUE, "#EFF6FF", 4, 2.5), text(107, 105, "X", 22, 700, "middle", BLUE)]
    for y in (155, 205, 255, 305):
        out += [line(65, y, 150, y, GRID, 1.2)]
    out += [text(107, 386, "[B, din]", 16, 650, "middle")]
    out += [text(181, 245, "×", 25, 700, "middle")]
    out += [rect(210, 155, 130, 170, TEAL, "#ECFDF5", 4, 2.5), text(275, 135, "W", 22, 700, "middle", TEAL)]
    for x in (242, 275, 308):
        out += [line(x, 165, x, 315, GRID, 1.2)]
    out += [text(275, 356, "[din, dout]", 16, 650, "middle")]
    out += [text(362, 245, "+ b", 20, 700, "middle", fill=RED), text(45, 440, "shared din must match", 16, 700, fill=BLUE), text(45, 478, "Z = XW + 1b  →  [B,dout]", 17, 650, cls="math")]

    heading(out, 430, "B", "保留位置轴，只替换 feature", TEAL)
    out += [rect(445, 105, 300, 82, BLUE, "#EFF6FF", 4, 2.5), text(595, 137, "B × T × din", 22, 700, "middle", BLUE), text(595, 166, "batch · token · feature", 15, 650, "middle", MUTED)]
    out += [line(595, 190, 595, 235, INK, 2.5, marker="a3")]
    out += [rect(500, 247, 190, 66, TEAL, "#ECFDF5", 4, 2.5), text(595, 276, "same W,b", 18, 700, "middle", TEAL), text(595, 301, "at every (b,t)", 15, 650, "middle", TEAL)]
    out += [line(595, 316, 595, 361, INK, 2.5, marker="a3")]
    out += [rect(445, 373, 300, 82, RED, "#FFF5F2", 4, 2.5), text(595, 405, "B × T × dout", 22, 700, "middle", RED), text(595, 434, "B,T unchanged", 15, 650, "middle", MUTED)]
    out += [text(430, 501, "bias shape [dout]；合法广播仍需轴语义审计。", 15, fill=MUTED)]

    heading(out, 830, "C", "四本账不能相互替代", RED)
    ledgers = (
        (105, "Parameters", "(din+1)dout", BLUE),
        (205, "MACs", "BT din·dout", TEAL),
        (305, "Activations", "BT dout scalars", RED),
        (405, "Rank ceiling", "≤ min(din,dout)", BLUE),
    )
    for y, title, formula, color in ledgers:
        out += [text(845, y, title, 17, 700, fill=color), line(965, y - 6, 1000, y - 6, GRID, 2), text(1012, y, formula, 16, 650, cls="math")]
    out += [text(842, 486, "latency 还取决于 layout、bandwidth 与 kernel。", 15, fill=MUTED)]
    return finish(out, "先对形状和轴，再分别计算静态参数、动态工作量、缓存与信息瓶颈。")


def perceptron_update_geometry():
    out = begin(
        "感知机：错误修正、参数轨迹与有限错误证据",
        "错误样本沿 yx 方向修正法向量；轨迹由样本顺序决定；正间隔进展和范数平方根增长共同给出有限错误上界。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "错误点触发一次几何修正", BLUE)
    out += [line(60, 430, 360, 430, GRID, 1.5), line(190, 470, 190, 95, GRID, 1.5)]
    for x, y in ((260, 155), (310, 205), (275, 285)):
        out += [circle(x, y, 7, BLUE, BLUE, 2), text(x + 10, y - 8, "+", 15, 700, fill=BLUE)]
    for x, y in ((90, 325), (125, 245), (110, 160)):
        out += [circle(x, y, 7, TEAL, BG, 2.5), text(x + 10, y - 8, "−", 15, 700, fill=TEAL)]
    out += [path("M65 120L350 365", RED, 3, "none", "8 5"), text(278, 385, "old boundary", 15, 650, fill=RED)]
    out += [path("M65 365L350 130", TEAL, 4), text(260, 120, "new boundary", 15, 700, fill=TEAL)]
    out += [line(190, 255, 260, 170, BLUE, 3.5, marker="a0"), text(220, 195, "y x", 17, 700, fill=BLUE)]
    out += [text(45, 482, "w⁺ = w + η yx", 19, 700, cls="math"), text(45, 510, "当前 margin 增加 η||x||²；其他点未必改善。", 15, fill=MUTED)]

    heading(out, 430, "B", "逐轮轨迹账", TEAL)
    headers = ((440, "k"), (492, "score"), (570, "y·score"), (670, "w after"))
    for x, label in headers:
        out += [text(x, 115, label, 15, 700, fill=TEAL)]
    out += [line(435, 130, 760, 130, TEAL, 2)]
    rows = (
        (170, "1", "0", "0", "(1,1)"),
        (225, "2", "0", "0", "(2,0)"),
        (280, "3", "−2", "+2", "(2,0)"),
        (335, "4", "+2", "+2", "(2,0)"),
    )
    for y, k, score, margin, weight in rows:
        out += [text(445, y, k, 16, 650), text(500, y, score, 16, 650), text(590, y, margin, 16, 650), text(680, y, weight, 16, 650)]
        out += [line(435, y + 18, 760, y + 18, GRID, 1)]
    out += [text(438, 410, "tie rule is part of the algorithm", 15, 650, fill=RED), text(438, 450, "顺序可改最终参数，不改 theorem 的共同上界。", 15, fill=MUTED)]

    heading(out, 830, "C", "两本账夹出 mistake bound", RED)
    out += [line(860, 430, 1135, 430, GRID, 1.5), line(860, 430, 860, 110, GRID, 1.5)]
    out += [path("M865 414L1125 145", TEAL, 4), text(1015, 185, "progress  Mγ", 16, 700, fill=TEAL)]
    out += [path("M865 414C930 320 1010 270 1125 235", BLUE, 4), text(1010, 260, "norm  R√M", 16, 700, fill=BLUE)]
    out += [circle(1085, 187, 7, RED, RED, 2), text(1095, 175, "intersection", 15, 650, fill=RED)]
    out += [text(842, 470, "Mγ ≤ uᵀw ≤ ||w|| ≤ R√M", 17, 650, cls="math"), text(842, 505, "unit u, γ>0, ||x||≤R  ⇒  M≤(R/γ)²", 16, 700, fill=RED, cls="math")]
    return finish(out, "有限错误来自共同正间隔方向；它不等于唯一解、最大间隔或总体泛化。")


def mlp_forward_shape_ledger():
    out = begin(
        "MLP：逐层前向、形状账本与输出合同",
        "多层感知机是 affine 与非线性的函数复合；形状沿 feature 轴变化，参数、计算和训练缓存分账；最后输出必须与任务和损失匹配。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "函数复合形成表示阶梯", BLUE)
    stages = ((65, 120, "x", "d₀"), (150, 190, "h¹", "d₁"), (245, 270, "h²", "d₂"), (330, 345, "ŷ", "d₃"))
    for i, (x, y, lab, dim) in enumerate(stages):
        color = BLUE if i == 0 else TEAL if i < 3 else RED
        out += [circle(x, y, 27, color, BG, 2.5), text(x, y + 6, lab, 16, 700, "middle", color), text(x, y + 50, dim, 15, 650, "middle", MUTED)]
        if i < len(stages) - 1:
            x2, y2, _, _ = stages[i + 1]
            out += [line(x + 28, y + 8, x2 - 30, y2 - 8, INK, 2.5, marker="a3")]
            out += [text((x + x2) / 2, (y + y2) / 2 - 10, "affine + φ", 15, 650, "middle", fill=BLUE)]
    out += [text(45, 430, "h(l) = phi_l(h(l−1) W(l) + b(l))", 18, 700, cls="math"), text(45, 470, "所有 phi=identity  ⇒  整体仍是一个 affine map。", 15, 650, fill=RED), text(45, 505, "hidden representation 可重排数据，但也可能丢失信息。", 15, fill=MUTED)]

    heading(out, 430, "B", "Layer ledger：每层两次命名", TEAL)
    out += [text(440, 105, "layer", 15, 700, fill=TEAL), text(510, 105, "input × weight", 15, 700, fill=TEAL), text(680, 105, "Z → H", 15, 700, fill=TEAL), line(435, 120, 760, 120, TEAL, 2)]
    rows = (
        (165, "1", "[B,d₀] × [d₀,d₁]", "[B,d₁]"),
        (235, "2", "[B,d₁] × [d₁,d₂]", "[B,d₂]"),
        (305, "3", "[B,d₂] × [d₂,d₃]", "[B,d₃]"),
    )
    for y, layer, prod, result in rows:
        out += [text(455, y, layer, 17, 700, fill=BLUE), text(505, y, prod, 15, 650, cls="math"), text(682, y, result, 15, 650, cls="math"), line(435, y + 22, 760, y + 22, GRID, 1)]
    out += [text(438, 370, "Z: pre-activation", 16, 700, fill=BLUE), text(605, 370, "H: after φ", 16, 700, fill=TEAL)]
    out += [text(438, 416, "sequence input: [B,T,d]；B,T 保留。", 15, 650), text(438, 460, "forward cache 保存 H/Z；inference 可丢弃多数中间量。", 15, fill=MUTED), text(438, 500, "参数数 = Σ_l (d(l−1)+1)d(l)", 16, 700, fill=RED, cls="math")]

    heading(out, 830, "C", "资源与输出语义分开验收", RED)
    out += [text(845, 112, "static", 15, 700, fill=BLUE), text(910, 112, "parameters", 16, 650), text(1040, 112, "Σ(din+1)dout", 15, 650, cls="math")]
    out += [text(845, 165, "work", 15, 700, fill=TEAL), text(910, 165, "MACs", 16, 650), text(1040, 165, "BΣ din·dout", 15, 650, cls="math")]
    out += [text(845, 218, "cache", 15, 700, fill=RED), text(910, 218, "H/Z/masks", 16, 650), text(1040, 218, "∝ BΣ d(l)", 15, 650, cls="math")]
    out += [line(840, 247, 1140, 247, GRID, 2)]
    heads = ((282, "regression", "identity → real value", BLUE), (342, "binary", "one logit → sigmoid/BCE", TEAL), (402, "K-class", "K logits → softmax/CE", RED), (462, "multi-label", "K independent logits", BLUE))
    for y, task, contract, color in heads:
        out += [text(845, y, task, 15, 700, fill=color), text(940, y, contract, 15, 650)]
    out += [text(842, 505, "output activation 由 action space 与 loss 决定。", 15, fill=MUTED)]
    return finish(out, "沿计算图核对 Z/H 与 shape，再分别验收资源账本和输出任务合同。")


FIGURES = {
    "fig-neuron-affine-hyperplane-v2.svg": neuron_affine_hyperplane,
    "fig-dense-layer-shapes-v2.svg": dense_layer_shapes,
    "fig-perceptron-update-geometry-v2.svg": perceptron_update_geometry,
    "fig-mlp-forward-shape-ledger-v2.svg": mlp_forward_shape_ledger,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
