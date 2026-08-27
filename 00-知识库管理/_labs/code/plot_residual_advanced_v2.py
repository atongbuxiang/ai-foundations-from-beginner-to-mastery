#!/usr/bin/env python3
"""Generate deterministic NN-45--48 residual-network textbook figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def residual_placement_contract():
    out = begin(
        "Residual Placement：合并前后谁过滤恒等轨",
        "原始 post-activation、full pre-activation、Transformer Pre-Norm 与 Post-Norm 的差别可由前向算子和 Jacobian 的乘法顺序精确定位。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "四种放置合同", BLUE)
    rows = (
        ("CNN post-act", "phi(x + F(x))", "J_phi (I + J_F)", RED),
        ("CNN full pre-act", "x + F(P(x))", "I + J_F J_P", TEAL),
        ("Transformer Pre-Norm", "x + F(N(x))", "I + J_F J_N", BLUE),
        ("Transformer Post-Norm", "N(x + F(x))", "J_N (I + J_F)", AMBER),
    )
    for idx, (name, forward, jac, color) in enumerate(rows):
        y = 92 + idx * 98
        out += [rect(52, y, 310, 76, color, BG, 5, 2),
                text(68, y + 25, name, 15, 700, fill=color),
                text(345, y + 48, forward, 15, 650, "end", INK),
                text(345, y + 68, jac, 15, 600, "end", MUTED)]

    heading(out, 430, "B", "同形外壳，不同内部对象", TEAL)
    out += [rect(445, 98, 315, 126, BLUE, "#EFF6FF", 5, 2),
            text(602, 126, "CNN full pre-activation", 16, 700, "middle", BLUE),
            text(602, 159, "P = BN / ReLU stack", 15, 650, "middle", INK),
            text(602, 189, "axes + train/eval state matter", 15, 600, "middle", MUTED),
            rect(445, 270, 315, 126, TEAL, "#ECFDF5", 5, 2),
            text(602, 298, "Transformer Pre-Norm", 16, 700, "middle", TEAL),
            text(602, 331, "N = token-wise norm", 15, 650, "middle", INK),
            text(602, 361, "attention / FFN semantics matter", 15, 600, "middle", MUTED),
            text(602, 458, "same Jacobian shell != same architecture", 15, 700, "middle", RED)]

    heading(out, 830, "C", "二维局部反例：rail 是否被门控", RED)
    out += [rect(845, 96, 285, 104, TEAL, "#ECFDF5", 5, 2),
            text(987, 125, "pre-activation", 16, 700, "middle", TEAL),
            text(987, 157, "J = [[1,0],[2,1]]", 16, 650, "middle", INK),
            text(987, 184, "rank 2; det = 1", 15, 600, "middle", MUTED),
            rect(845, 250, 285, 104, RED, "#FFF5F2", 5, 2),
            text(987, 279, "post-activation", 16, 700, "middle", RED),
            text(987, 311, "J = [[1,1],[0,0]]", 16, 650, "middle", INK),
            text(987, 338, "rank 1; a direction is deleted", 15, 600, "middle", MUTED),
            text(987, 421, "activation mask is local", 15, 700, "middle", AMBER),
            text(987, 451, "boundary points need subgradients", 15, 600, "middle", MUTED)]
    return finish(out, "先写前向式，再按计算顺序写 Jacobian；名称相似不能替代轴、状态与求值点合同。")


def skip_fusion_taxonomy():
    out = begin(
        "Skip Taxonomy：加法、门控、拼接与跨尺度",
        "四类 skip 的差别不只是连线形状：融合算子决定状态维度、Jacobian、信息身份和系统成本；连接数也不等于独立路径数。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "融合算子先于网络名称", BLUE)
    kinds = (
        ("add", "P(x) + F(x)", "fixed width", BLUE),
        ("gate", "T H + (1-T)x", "data dependent", TEAL),
        ("concat", "[x, z1, ..., zl]", "width grows", AMBER),
        ("long skip", "enc -> align -> dec", "cross scale", RED),
    )
    for idx, (kind, formula, effect, color) in enumerate(kinds):
        y = 92 + idx * 96
        out += [rect(52, y, 310, 72, color, BG, 5, 2),
                text(68, y + 26, kind, 16, 700, fill=color),
                text(345, y + 46, formula, 15, 650, "end", INK),
                text(345, y + 66, effect, 15, 600, "end", MUTED)]

    heading(out, 430, "B", "Highway：别漏 gate 导数", TEAL)
    node(out, 450, 104, 80, 48, "x", BLUE)
    node(out, 580, 96, 105, 54, "H(x)", TEAL)
    out += [path("M493 153V233H575", BLUE, 2.4, "none", None, "a0"),
            line(535, 128, 575, 123, TEAL, 2.4, marker="a1"),
            path("M633 153V205H615V222", TEAL, 2.4, "none", None, "a1"),
            circle(615, 235, 8, INK, BG, 2),
            text(602, 290, "y = T H + (1-T)x", 16, 700, "middle", INK),
            rect(445, 330, 315, 112, RED, "#FFF5F2", 5, 2),
            text(602, 360, "J includes Diag(H-x) J_T", 15, 700, "middle", RED),
            text(602, 394, "gate can amplify or cancel carry", 15, 600, "middle", MUTED),
            text(602, 420, "T near 0 is only an initialization bias", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "Dense block：宽度增长", RED)
    widths = (("x0", 64, BLUE), ("z1", 96, TEAL), ("z2", 128, TEAL),
              ("z3", 160, AMBER), ("z4", 192, RED))
    for idx, (lab, width, color) in enumerate(widths):
        y = 90 + idx * 72
        bar = 85 + int((width - 64) * 0.78)
        out += [rect(845, y, bar, 44, color, "#F8FAFC", 4, 1.8),
                text(856, y + 28, f"{lab}: C={width}", 15, 700, fill=color)]
    out += [text(987, 466, "C0=64, k=32, L=4 -> C=192", 15, 700, "middle", INK),
            text(987, 492, "input-channel work: 64+96+128+160", 15, 600, "middle", MUTED)]
    return finish(out, "统一比较 skip 时，逐项登记 source、transform、fusion、shape、Jacobian 与 memory traffic。")


def ultradeep_scaling_methods():
    out = begin(
        "Ultra-Deep Scaling：ReZero、Fixup 与 DeepNorm",
        "三种方法都控制极深训练，却作用在不同位置：可学习 residual gate、无归一化分支初始化、Post-LN shortcut 与指定权重缩放。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "ReZero：零 gate 起步", BLUE)
    out += [rect(52, 100, 310, 84, BLUE, "#EFF6FF", 5, 2),
            text(207, 132, "x+ = x + alpha F(x)", 17, 700, "middle", BLUE),
            text(207, 162, "alpha(0)=0  =>  J_x=I", 15, 650, "middle", INK),
            rect(52, 226, 310, 104, TEAL, "#ECFDF5", 5, 2),
            text(207, 257, "dL/dalpha = g^T F(x)", 15, 700, "middle", TEAL),
            text(207, 289, "usually nonzero", 15, 600, "middle", MUTED),
            text(207, 316, "dL/dtheta = 0 at first step", 15, 600, "middle", MUTED),
            text(207, 401, "if F(x)=0 too: gate deadlock", 15, 700, "middle", RED),
            text(207, 448, "identity is a state-Jacobian claim", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "Fixup：深度缩放初始化", TEAL)
    out += [rect(445, 98, 315, 90, TEAL, "#ECFDF5", 5, 2),
            text(602, 129, "non-last weights", 16, 700, "middle", TEAL),
            text(602, 161, "scale by L^[-1/(2m-2)]", 15, 650, "middle", INK),
            rect(445, 230, 315, 92, BLUE, "#EFF6FF", 5, 2),
            text(602, 261, "last branch layer = 0", 16, 700, "middle", BLUE),
            text(602, 292, "plus scalar biases / multiplier", 15, 600, "middle", MUTED),
            text(602, 373, "m=2, L=100  =>  scale=0.1", 15, 700, "middle", RED),
            text(602, 422, "not whole-network zero initialization", 15, 600, "middle", MUTED),
            text(602, 452, "no normalization in original method", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "DeepNorm：双尺度", RED)
    out += [rect(845, 96, 285, 92, RED, "#FFF5F2", 5, 2),
            text(987, 127, "LN(alpha x + G(x))", 16, 700, "middle", RED),
            text(987, 159, "alpha stays at runtime", 15, 600, "middle", MUTED),
            rect(845, 226, 285, 104, AMBER, "#FFFBEB", 5, 2),
            text(987, 257, "encoder-only N", 16, 700, "middle", AMBER),
            text(987, 287, "alpha=(2N)^1/4", 15, 650, "middle", INK),
            text(987, 312, "beta=(8N)^-1/4", 15, 650, "middle", INK),
            text(987, 389, "N=100: alpha=3.761", 15, 700, "middle", BLUE),
            text(987, 417, "beta=0.188", 15, 700, "middle", TEAL),
            text(987, 463, "update bound != universal stability", 15, 600, "middle", MUTED)]
    return finish(out, "方法名相近不等于可混搭：先标注 scale 作用对象、是否运行时存在、零梯度层级与理论假设。")


def depth_evidence_map():
    out = begin(
        "Depth Evidence Map：六种深度，五级断言，六本稳定账",
        "名义层数、路径长度、ODE 时间和系统串行深度不是同一个变量；结构恒等式、条件定理、机制、实验与系统证据也不能互相代替。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先声明 depth 坐标", BLUE)
    depths = (
        "nominal blocks", "nonlinear path length", "shortest graph distance",
        "effective gradient path", "ODE horizon / step", "sequential latency",
    )
    for idx, label in enumerate(depths):
        y = 88 + idx * 64
        color = (BLUE, TEAL, AMBER, RED, BLUE, TEAL)[idx]
        out += [rect(52, y, 310, 46, color, BG, 4, 1.8),
                text(68, y + 29, f"{idx+1}  {label}", 15, 700, fill=color)]
    out += [text(207, 489, "same L can imply different depth", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "toy path，不是独立集成", TEAL)
    out += [rect(445, 94, 315, 78, TEAL, "#ECFDF5", 5, 2),
            text(602, 124, "(1+a)^L = sum C(L,k) a^k", 15, 700, "middle", TEAL),
            text(602, 151, "scalar / homogeneous calibration", 15, 600, "middle", MUTED)]
    for k, height in enumerate((20, 52, 94, 112, 82, 42, 16)):
        x = 462 + k * 41
        out += [rect(x, 360 - height, 25, height, BLUE if k < 4 else AMBER, "#EFF6FF", 3, 1.5),
                text(x + 12, 383, str(k), 15, 650, "middle", MUTED)]
    out += [line(455, 361, 747, 361, GRID, 1.8),
            text(602, 414, "p=a/(1+a),  E[K]=Lp", 15, 700, "middle", INK),
            text(602, 444, "a=c/L  =>  E[K] approaches c", 15, 700, "middle", RED),
            text(602, 474, "matrices / nonlinear gates", 15, 600, "middle", MUTED),
            text(602, 496, "break this probability reading", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "证据层与稳定仪表", RED)
    levels = (("exact structure", BLUE), ("conditional theorem", TEAL),
              ("mechanism", AMBER), ("controlled experiment", RED),
              ("system evidence", BLUE))
    for idx, (lab, color) in enumerate(levels):
        y = 88 + idx * 57
        out += [rect(845, y, 285, 40, color, BG, 4, 1.6),
                text(860, y + 26, f"{idx+1}  {lab}", 15, 700, fill=color)]
    out += [text(845, 407, "audit together:", 16, 700, fill=INK),
            text(845, 438, "forward | backward | update", 15, 650, fill=TEAL),
            text(845, 466, "numerical | statistical | system", 15, 650, fill=RED),
            text(1128, 495, "correlation != norm", 15, 600, "end", MUTED)]
    return finish(out, "先固定 depth 与 stability 的对象，再把每条结论放回它真正拥有的证据层。")


FIGURES = {
    "fig-residual-placement-contract-v2.svg": residual_placement_contract,
    "fig-skip-fusion-taxonomy-v2.svg": skip_fusion_taxonomy,
    "fig-ultradeep-scaling-methods-v2.svg": ultradeep_scaling_methods,
    "fig-depth-evidence-map-v2.svg": depth_evidence_map,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
