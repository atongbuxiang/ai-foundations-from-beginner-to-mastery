#!/usr/bin/env python3
"""Generate ARCH-01--04 figures for architecture/convolution foundations.

The plates deliberately use four different textbook grammars: comparison
matrix, discrete signal workbench, commutative proof map, and tensor ledger.
They remain visually consistent with the course paper-and-ink system.
"""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def architecture_comparison():
    out = begin(
        "架构比较：结构、信息混合与成本合同",
        "同一输入向量可由全连接、局部共享、递推状态或内容寻址处理；设计差异必须沿对称性、交互图和资源成本分账。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "先声明输入结构", BLUE)
    for i, lab in enumerate(("x₁", "x₂", "x₃", "x₄", "x₅")):
        x = 68 + i * 63
        out += [circle(x, 150, 18, BLUE, "#EFF6FF", 2.5), text(x, 156, lab, 15, 700, "middle", BLUE)]
        if i < 4:
            out += [line(x + 19, 150, x + 44, 150, GRID, 2)]
    out += [text(45, 215, "序列：有顺序与位移", 16, 700), text(45, 252, "图像：二维网格与局部邻域", 16, 700), text(45, 289, "图：邻接而非固定索引", 16, 700)]
    out += [rect(55, 340, 300, 95, RED, "#FFF5F2", 6, 2), text(205, 372, "若先 flatten", 17, 700, "middle", RED), text(205, 405, "结构不会自动保留", 16, 650, "middle", RED)]
    out += [text(45, 485, "归纳偏置 = 先限制可表示/易学习的函数。", 15, fill=MUTED)]

    heading(out, 430, "B", "四种信息混合图", TEAL)
    rows = ((125, "Dense", "all-to-all", BLUE), (220, "Conv", "local + shared", TEAL), (315, "RNN", "state chain", RED), (410, "Attention", "data-dependent", BLUE))
    for y, name, rule, color in rows:
        out += [text(438, y, name, 16, 700, fill=color), text(540, y, rule, 15, 650, fill=MUTED)]
        for i in range(4):
            out += [circle(660 + i * 30, y - 6, 5, color, color, 1)]
        if name == "Dense":
            for i in range(4):
                out += [line(660 + i * 30, y - 6, 770, y - 6, color, 1)]
        elif name == "Conv":
            for i in range(3):
                out += [line(660 + i * 30, y - 6, 690 + i * 30, y - 6, color, 3)]
        elif name == "RNN":
            for i in range(3):
                out += [line(665 + i * 30, y - 6, 685 + i * 30, y - 6, color, 2.5, marker="a2")]
        else:
            out += [path("M660 %s Q705 %s 750 %s" % (y - 6, y - 60, y - 6), color, 2.5), path("M690 %s Q720 %s 750 %s" % (y - 6, y + 45, y - 6), color, 2.5)]
    out += [text(438, 490, "交互图决定一步能看多远，也决定并行和缓存。", 15, fill=MUTED)]

    heading(out, 830, "C", "比较时至少六本账", RED)
    items = ((110, "symmetry", "不变 / 等变"), (175, "range", "局部 / 全局 / 状态"), (240, "parameters", "是否随位置增长"), (305, "arithmetic", "MACs / FLOPs"), (370, "memory & IO", "激活 / cache / 搬运"), (435, "evidence", "I / T / E / H / O"))
    for y, left, right in items:
        out += [text(845, y, left, 16, 700, fill=BLUE if y < 300 else TEAL), text(1000, y, right, 15, 650), line(842, y + 16, 1138, y + 16, GRID, 1)]
    out += [text(842, 493, "没有脱离数据、任务和硬件的唯一最佳架构。", 15, 700, fill=RED)]
    return finish(out, "架构选择不是名称偏好，而是结构假设、信息路径和资源约束的联合合同。")


def discrete_convolution_workbench():
    out = begin(
        "离散卷积工作台：翻转、滑动与边界",
        "一维离散互相关直接滑动核，数学卷积先翻转核；valid、same 与 circular 边界给出不同的输出对象。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "一个可完整手算的窗口", BLUE)
    vals = (2, -1, 3, 0, 1)
    for i, v in enumerate(vals):
        x = 55 + i * 60
        out += [rect(x, 130, 48, 48, BLUE, "#EFF6FF", 4, 2), text(x + 24, 161, v, 17, 700, "middle", BLUE)]
    out += [text(45, 110, "input x", 16, 700, fill=BLUE)]
    for i, v in enumerate((1, 0, -1)):
        x = 115 + i * 60
        out += [rect(x, 235, 48, 48, TEAL, "#ECFDF5", 4, 2), text(x + 24, 266, v, 17, 700, "middle", TEAL)]
    out += [text(45, 215, "kernel w", 16, 700, fill=TEAL), line(139, 290, 139, 332, INK, 2, marker="a3")]
    out += [text(45, 365, "cross-correlation: 2·1 + (−1)·0 + 3·(−1) = −1", 16, 650, cls="math")]
    out += [text(45, 410, "convolution uses reversed kernel: [−1,0,1]", 16, 650, fill=RED)]
    out += [text(45, 470, "深度学习 API 通常实现互相关，但把参数学习后仍称 conv。", 15, fill=MUTED)]

    heading(out, 430, "B", "三种边界不是同一问题", TEAL)
    schemes = ((120, "valid", "只保留完整窗口", "L−K+1"), (260, "same", "zero pad 后近似同长", "ceil(L/S)"), (400, "circular", "首尾相接", "周期信号"))
    for y, name, meaning, length in schemes:
        out += [text(440, y, name, 17, 700, fill=TEAL), text(535, y, meaning, 15, 650), rect(438, y + 18, 300, 42, TEAL, "#ECFDF5", 4, 1.8), text(588, y + 46, length, 16, 700, "middle", TEAL, cls="math")]
    out += [text(438, 495, "边界会进入数值值域，也会影响严格等变性。", 15, fill=MUTED)]

    heading(out, 830, "C", "线性算子与成本账", RED)
    out += [text(845, 112, "y[i] = Σ_j w[j] x[i+j]", 18, 700, cls="math", fill=BLUE)]
    out += [text(845, 160, "固定 w 时：x ↦ y 是线性的", 16, 650), text(845, 205, "固定 x 时：w ↦ y 也是线性的", 16, 650)]
    out += [rect(842, 250, 300, 115, BLUE, "#EFF6FF", 6, 2), text(992, 282, "direct 1D valid", 16, 700, "middle", BLUE), text(992, 318, "(L−K+1)K MACs", 18, 700, "middle", BLUE, cls="math"), text(992, 348, "K parameters", 16, 650, "middle", BLUE)]
    out += [text(842, 411, "FFT 可降低长核渐近成本，", 15, fill=MUTED), text(842, 443, "但小核 CNN 常由 direct kernel 更合适。", 15, fill=MUTED), text(842, 487, "算法最优取决于 L、K、batch 与硬件。", 15, 700, fill=RED)]
    return finish(out, "先固定翻转、索引和边界约定，才存在唯一可复算的“卷积输出”。")


def equivariance_commutation():
    out = begin(
        "平移等变性：交换图、共享核与失效边界",
        "单位步幅、恰当定义域上的共享卷积与平移算子可交换；位置依赖权重、边界裁切和下采样会破坏或限制该性质。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "等变 = 先移再算，先算再移", BLUE)
    node(out, 55, 120, 110, 55, "x", BLUE, "#EFF6FF")
    node(out, 260, 120, 110, 55, "Tτ x", TEAL, "#ECFDF5")
    node(out, 55, 340, 110, 55, "Cw x", TEAL, "#ECFDF5")
    node(out, 260, 340, 110, 55, "Tτ Cw x", BLUE, "#EFF6FF")
    out += [line(166, 148, 254, 148, BLUE, 3, marker="a0"), text(210, 132, "shift Tτ", 15, 650, "middle", fill=BLUE)]
    out += [line(110, 176, 110, 332, TEAL, 3, marker="a1"), text(120, 255, "Cw", 16, 700, fill=TEAL)]
    out += [line(315, 176, 315, 332, TEAL, 3, marker="a1"), text(325, 255, "Cw", 16, 700, fill=TEAL)]
    out += [line(166, 368, 254, 368, BLUE, 3, marker="a0"), text(210, 352, "shift Tτ", 15, 650, "middle", fill=BLUE)]
    out += [text(45, 455, "Cw Tτ = Tτ Cw", 20, 700, cls="math", fill=RED), text(45, 493, "输出移动，不是输出保持不变。", 15, fill=MUTED)]

    heading(out, 430, "B", "为何共享核是关键", TEAL)
    for i in range(4):
        out += [circle(465 + i * 80, 155, 8, BLUE, BLUE, 1), text(465 + i * 80, 190, "i+%s" % i, 15, 650, "middle")]
    out += [path("M455 235 Q585 175 715 235", TEAL, 3), text(585, 225, "same w at every i", 16, 700, "middle", fill=TEAL)]
    out += [text(438, 300, "(Cw Tτx)[i]", 17, 650, cls="math"), text(620, 300, "= Σj w[j] x[i+j−τ]", 15, 650, cls="math")]
    out += [text(438, 350, "(Tτ Cwx)[i]", 17, 650, cls="math"), text(620, 350, "= (Cwx)[i−τ]", 15, 650, cls="math")]
    out += [text(438, 402, "同一 w 与相对位移 j 让两式相等。", 16, 700, fill=TEAL), text(438, 465, "若 w=w_i 随位置变，换元后不再匹配。", 15, fill=MUTED)]

    heading(out, 830, "C", "三个常见失效点", RED)
    failures = ((115, "finite boundary", "zero/crop 产生特殊边缘"), (245, "stride > 1", "只对 stride 的整数倍平移对齐"), (375, "pool / nonlinear", "需逐个检查所需群作用"))
    for y, title, detail in failures:
        out += [circle(855, y - 7, 11, RED, BG, 3), line(848, y - 14, 862, y, RED, 2.5), line(862, y - 14, 848, y, RED, 2.5), text(885, y, title, 16, 700, fill=RED), text(885, y + 32, detail, 15, 650, fill=MUTED)]
    out += [text(842, 475, "等变性是算子恒等式；", 15, 700, fill=BLUE), text(842, 505, "鲁棒性与泛化仍是任务和数据上的经验问题。", 15, 650)]
    return finish(out, "共享局部核给出平移等变的结构理由，但边界、采样和任务读出决定实际保留程度。")


def convolution_shape_ledger():
    out = begin(
        "多通道卷积：张量形状、超参数与资源总账",
        "二维卷积把 Cin 个输入通道的局部窗口与 Cout 组核缩并；stride、padding 与 dilation 决定输出空间尺寸，group 决定通道连接。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "四维输入与四维权重", BLUE)
    out += [rect(55, 125, 115, 230, BLUE, "#EFF6FF", 5, 2.5), rect(78, 105, 115, 230, BLUE, "none", 5, 1.5), text(125, 385, "X [N,Cin,H,W]", 16, 700, "middle", BLUE)]
    out += [text(208, 240, "×", 25, 700, "middle")]
    out += [rect(240, 155, 115, 160, TEAL, "#ECFDF5", 5, 2.5), rect(258, 138, 115, 160, TEAL, "none", 5, 1.5), text(305, 345, "K [Cout,Cin/G,Kh,Kw]", 15, 700, "middle", TEAL)]
    out += [text(45, 438, "每个 output channel 对输入组内通道求和。", 15, fill=MUTED), text(45, 478, "bias [Cout] 广播到 N,Hout,Wout。", 15, 650)]

    heading(out, 430, "B", "空间输出尺寸逐轴计算", TEAL)
    out += [text(438, 120, "effective kernel", 15, 700, fill=TEAL), text(620, 120, "Ke = D(K−1)+1", 17, 700, cls="math")]
    out += [text(438, 190, "output height", 15, 700, fill=TEAL), text(555, 190, "Hout = floor((H+2P−Ke)/S)+1", 15, 700, cls="math")]
    out += [text(438, 260, "output width", 15, 700, fill=TEAL), text(555, 260, "Wout = floor((W+2P−Ke)/S)+1", 15, 700, cls="math")]
    out += [rect(438, 315, 310, 120, RED, "#FFF5F2", 6, 2), text(593, 347, "Example", 16, 700, "middle", RED), text(593, 382, "H=7,K=3,P=1,S=2,D=1", 15, 650, "middle", cls="math"), text(593, 416, "Hout=floor(6/2)+1=4", 17, 700, "middle", RED, cls="math")]
    out += [text(438, 488, "‘same’ 的具体左右补法仍需查框架约定。", 15, fill=MUTED)]

    heading(out, 830, "C", "参数与 MACs 分账", RED)
    out += [text(842, 112, "parameters", 16, 700, fill=BLUE), text(842, 145, "Cout(Cin/G · KhKw + 1)", 17, 700, cls="math")]
    out += [text(842, 205, "forward MACs", 16, 700, fill=TEAL), text(842, 238, "N Hout Wout Cout Cin/G KhKw", 16, 700, cls="math")]
    out += [line(842, 270, 1140, 270, GRID, 2)]
    comparisons = ((310, "standard", "G=1"), (365, "grouped", "1<G<Cin"), (420, "depthwise", "G=Cin"), (475, "pointwise", "Kh=Kw=1"))
    for y, name, rule in comparisons:
        out += [text(845, y, name, 15, 700, fill=RED if name == "depthwise" else BLUE), text(990, y, rule, 15, 650, cls="math")]
    return finish(out, "任何卷积层先写 X、K、Y 的完整形状，再计算空间尺寸、参数和动态工作量。")


FIGURES = {
    "fig-architecture-comparison-contract-v1.svg": architecture_comparison,
    "fig-discrete-convolution-workbench-v1.svg": discrete_convolution_workbench,
    "fig-translation-equivariance-commutation-v1.svg": equivariance_commutation,
    "fig-convolution-shape-ledger-v1.svg": convolution_shape_ledger,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
