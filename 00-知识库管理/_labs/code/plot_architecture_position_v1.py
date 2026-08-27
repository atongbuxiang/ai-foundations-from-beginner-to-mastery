#!/usr/bin/env python3
"""Generate the eight original ARCH-41--48 positional-encoding teaching figures."""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def symmetry():
    out = begin(
        "没有位置时：Self-Attention 保留 Token 置换对称",
        "共享投影与逐行运算使无位置 encoder 对 token permutation 等变；pooling 后进一步变为不变。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "同一集合，两种排列", BLUE)
    for y, labels in ((112, ("A", "B", "C")), (262, ("C", "A", "B"))):
        for i, label in enumerate(labels):
            node(out, 55 + i * 95, y, 70, 48, label, BLUE if y == 112 else TEAL, "#F8FAFC", 15)
        out += [text(55, y + 82, "共享 Q/K/V；全可见 relation 同步置换", 13, fill=MUTED)]
    out += [line(90, 165, 90, 250, INK, 2, "6 5", "a3")]
    out += [text(55, 430, "输出只会按同一 permutation 重排。", 14, 700, fill=BLUE)]

    heading(out, 430, "B", "等变证明链", TEAL)
    for y, label, color in (
        (100, "Q(PX)=P Q(X)", BLUE),
        (195, "S(PX)=P S(X) Pᵀ", TEAL),
        (290, "A(PX)=P A(X) Pᵀ", AMBER),
        (385, "F(PX)=P F(X)", RED),
    ):
        node(out, 455, y, 290, 54, label, color, "#F8FAFC", 15)
        if y < 385:
            out.append(line(600, y + 57, 600, y + 91, INK, 2, marker="a3"))

    heading(out, 830, "C", "怎样打破或利用对称", RED)
    items = (
        ("absolute / relative position", BLUE),
        ("causal / structural mask", RED),
        ("special token / boundary", AMBER),
        ("graph, grid, segment coordinates", TEAL),
    )
    for i, (label, color) in enumerate(items):
        y = 105 + i * 88
        out += [circle(858, y, 9, color, "#F8FAFC", 2), text(880, y + 5, label, 14, 650)]
    out += [text(845, 458, "Causal mask 提供顺序非对称，", 13, fill=MUTED),
            text(845, 484, "但不保证高分辨率计数或外推。", 13, 700, fill=RED)]
    return finish(out, "位置编码不是装饰：先问模型还保留什么对称，再决定需要注入哪种坐标。")


def absolute_position():
    out = begin(
        "可学习绝对位置：相加、索引、尺度与分辨率合同",
        "Token 与 position 可相加的前提是 shape 对齐；padding、packing、offset 与 resize 都会改变坐标语义。",
        (BLUE, AMBER, TEAL),
    )
    heading(out, 42, "A", "相加前先核对 Shape", BLUE)
    node(out, 55, 105, 290, 52, "token E[x] : B × T × d", BLUE, "#EFF6FF", 14)
    node(out, 55, 205, 290, 52, "position P[id] : B × T × d", AMBER, "#FFF7ED", 14)
    out += [line(200, 160, 200, 195, INK, 2, marker="a3"),
            line(200, 260, 200, 295, INK, 2, marker="a3")]
    node(out, 55, 305, 290, 58, "X₀ = E[x] + α P[id]", TEAL, "#ECFDF5", 15)
    out += [text(55, 420, "相同 d 不保证相同 norm；", 13, fill=MUTED),
            text(55, 447, "α、初始化与 input norm 要登记。", 13, 700, fill=BLUE)]

    heading(out, 430, "B", "Position ID 生命周期", AMBER)
    rows = (
        (105, "padding", "是否占 ID？"),
        (190, "packing", "样本边界 reset / isolate"),
        (275, "decode cache", "offset = cached length"),
        (360, "crop / segment", "局部 ID 还是全局 ID"),
        (445, "max table", "越界报错 / 扩表 / 插值"),
    )
    for y, name, desc in rows:
        out += [text(450, y, name, 13, 800, fill=AMBER), text(610, y, desc, 12, 650)]

    heading(out, 830, "C", "训练表格 ≠ 连续函数", TEAL)
    for i, label in enumerate(("0", "1", "2", "…", "L₀−1")):
        node(out, 840 + i * 61, 112, 48, 40, label, TEAL, "#ECFDF5", 13)
    out += [text(845, 205, "测试 L₁ > L₀：", 15, 800, fill=RED),
            text(845, 242, "• 新行随机/复制：未训练参数", 13),
            text(845, 278, "• 1D 插值：改变邻距与谱", 13),
            text(845, 314, "• 2D 插值：需先恢复网格", 13),
            text(845, 380, "输入可运行，不代表坐标语义", 14, 700, fill=RED),
            text(845, 410, "或长程利用保持不变。", 14, 700, fill=RED)]
    return finish(out, "绝对位置表的真正接口是 ID 生成、相加尺度、最大范围与分辨率变更，而不只是一个参数矩阵。")


def sinusoidal():
    out = begin(
        "Sinusoidal 位置编码：频率阶梯、平移旋转与混叠",
        "每对通道是一只不同转速的相位钟；平移在二维通道内对应固定旋转，内积只依相对位移。",
        (TEAL, BLUE, AMBER),
    )
    heading(out, 42, "A", "多尺度相位钟", TEAL)
    for i, (y, label, turns, color) in enumerate((
        (120, "high ω", "快：局部分辨率高", RED),
        (230, "mid ω", "中等尺度", AMBER),
        (340, "low ω", "慢：覆盖范围长", BLUE),
    )):
        out += [circle(105, y, 35, color, "#F8FAFC", 2),
                line(105, y, 105 + 27, y - 12 + i * 6, color, 3),
                text(165, y - 5, label, 15, 800, fill=color),
                text(165, y + 25, turns, 13, fill=MUTED)]
    out += [text(55, 455, "ωᵢ = base^(−2i/d)", 18, 750, fill=TEAL)]

    heading(out, 430, "B", "平移 = 通道内旋转", BLUE)
    node(out, 455, 105, 290, 56, "pω(n) = [cos ωn, sin ωn]", BLUE, "#EFF6FF", 14)
    out += [line(600, 164, 600, 205, INK, 2, marker="a3")]
    node(out, 455, 218, 290, 62, "pω(n+Δ) = R(ωΔ) pω(n)", TEAL, "#ECFDF5", 14)
    out += [line(600, 283, 600, 324, INK, 2, marker="a3")]
    node(out, 455, 338, 290, 62, "pω(m)ᵀpω(n)=cos ω(m−n)", AMBER, "#FFF7ED", 14)
    out += [text(455, 450, "这是精确恒等式，不是性能定理。", 13, 700, fill=RED)]

    heading(out, 830, "C", "分辨率与混叠", AMBER)
    out += [text(845, 110, "短周期", 14, 800, fill=RED),
            text(940, 110, "邻位易区分，远处重复", 13),
            text(845, 190, "长周期", 14, 800, fill=BLUE),
            text(940, 190, "远程不重复，邻位变化小", 13),
            text(845, 270, "组合频率", 14, 800, fill=TEAL),
            text(940, 270, "用多尺度缓解单频歧义", 13),
            text(845, 355, "base / dtype / length", 14, 800, fill=AMBER),
            text(845, 390, "共同决定相位分辨率；", 13, fill=MUTED),
            text(845, 418, "有限精度下近似相同也会混淆。", 13, fill=MUTED)]
    return finish(out, "Sinusoidal 的强项是可解析平移结构；频率表、有限精度与任务训练仍决定能否真正利用这种结构。")


def relative_position():
    out = begin(
        "相对位置编码：注入点、距离压缩与常量输入反例",
        "相对信息可进入 logits、relative keys 或 relative values；只改 row-stochastic 权重存在明确的常量输入盲区。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "三种注入位置", RED)
    rows = (
        (105, "logit bias", "qᵢᵀkⱼ + b(i−j)", RED),
        (210, "relative key", "qᵢᵀ[kⱼ+aᴷ(i−j)]", BLUE),
        (315, "relative value", "Σ αᵢⱼ[vⱼ+aⱽ(i−j)]", TEAL),
    )
    for y, name, formula, color in rows:
        out += [text(55, y, name, 14, 800, fill=color),
                rect(55, y + 18, 285, 48, color, "#F8FAFC", 6, 2),
                text(197, y + 48, formula, 13, 650, "middle", color)]
    out += [text(55, 455, "注入点不同，表达与缓存成本也不同。", 13, fill=MUTED)]

    heading(out, 430, "B", "距离函数就是先验", BLUE)
    for y, label, desc, color in (
        (105, "clip", "远于 K 的距离同一桶", RED),
        (195, "log buckets", "越远分辨率越粗", AMBER),
        (285, "linear bias", "显式 recency slope", BLUE),
        (375, "2D / graph", "距离不再只是一维差", TEAL),
    ):
        node(out, 455, y, 115, 44, label, color, "#F8FAFC", 13)
        out += [text(585, y + 28, desc, 13, 650)]

    heading(out, 830, "C", "全同 Values 探针", TEAL)
    node(out, 845, 105, 280, 52, "v₁ = v₂ = … = v", TEAL, "#ECFDF5", 14)
    out += [line(985, 160, 985, 202, INK, 2, marker="a3")]
    node(out, 845, 215, 280, 66, "oᵢ = Σⱼ αᵢⱼ v = v", BLUE, "#EFF6FF", 15)
    out += [text(845, 335, "即使 α 的每行不同，", 14, 700, fill=RED),
            text(845, 365, "row sum = 1 仍使输出相同。", 14, 700, fill=RED),
            text(845, 425, "特殊 token / V 位置项 / 非归一化", 12, fill=MUTED),
            text(845, 450, "可打破前提，因此这是条件反例。", 12, fill=MUTED)]
    return finish(out, "相对位置不是一个单一公式：先记录注入点和距离压缩，再用常量输入探针检查表达边界。")


def rope():
    out = begin(
        "RoPE：绝对旋转怎样在 QK 内积中变成相对位移",
        "位置 m、n 分别旋转 Q、K；正交表示合同把两次绝对变换合并成只依 n−m 的相对旋转。",
        (BLUE, TEAL, AMBER),
    )
    heading(out, 42, "A", "Q/K 各自按位置旋转", BLUE)
    node(out, 55, 105, 110, 52, "qₘ", BLUE, "#EFF6FF", 16)
    node(out, 235, 105, 110, 52, "Rₘ qₘ", TEAL, "#ECFDF5", 15)
    out += [line(168, 131, 230, 131, BLUE, 3, marker="a0"), text(199, 113, "Rₘ", 13, 700, "middle")]
    node(out, 55, 265, 110, 52, "kₙ", BLUE, "#EFF6FF", 16)
    node(out, 235, 265, 110, 52, "Rₙ kₙ", TEAL, "#ECFDF5", 15)
    out += [line(168, 291, 230, 291, BLUE, 3, marker="a0"), text(199, 273, "Rₙ", 13, 700, "middle")]
    out += [line(290, 160, 290, 250, AMBER, 2.5, "6 5", "a2"),
            text(55, 405, "Rotation 只作用成对通道；", 13, fill=MUTED),
            text(55, 432, "head_dim、pairing、offset 是实现合同。", 13, 700, fill=BLUE)]

    heading(out, 430, "B", "相对位移恒等式", TEAL)
    node(out, 455, 105, 290, 58, "RₘᵀRₙ = Rₙ₋ₘ", TEAL, "#ECFDF5", 17)
    out += [line(600, 166, 600, 210, INK, 2, marker="a3")]
    node(out, 435, 225, 330, 72, "(Rₘqₘ)ᵀ(Rₙkₙ) = qₘᵀRₙ₋ₘkₙ", BLUE, "#EFF6FF", 15)
    out += [line(600, 300, 600, 344, INK, 2, marker="a3")]
    node(out, 455, 358, 290, 58, "‖Rₙx‖ = ‖x‖", AMBER, "#FFF7ED", 16)
    out += [text(455, 460, "离散位置：Rₙ = R₁ⁿ。", 13, fill=MUTED)]

    heading(out, 830, "C", "恒等式没有承诺", AMBER)
    items = (
        "注意力随距离单调下降",
        "训练外相位仍可正确解释",
        "所有 head 都使用同一尺度",
        "长上下文检索与推理可靠",
    )
    for i, label in enumerate(items):
        y = 115 + i * 78
        out += [text(845, y, "×", 18, 800, fill=RED), text(875, y, label, 13, 650)]
    out += [text(845, 445, "代数结构 = I；性能与外推 = E/H。", 13, 700, fill=AMBER)]
    return finish(out, "RoPE 的证明核心只有正交表示与相对内积；频率、训练覆盖和任务利用必须另建证据。")


def multiaxis():
    out = begin(
        "二维、多轴与多模态位置：坐标域、轴组合与冲突",
        "图像、视频与图文混排同时具有多个坐标轴；编码前必须声明每轴含义、通道分配和跨模态共同坐标。",
        (AMBER, TEAL, BLUE),
    )
    heading(out, 42, "A", "不同对象，不同坐标", AMBER)
    rows = (
        (105, "text", "(sequence)", BLUE),
        (195, "image", "(row, column)", AMBER),
        (285, "video", "(time, row, column)", RED),
        (375, "document", "(page, block, line, x/y)", TEAL),
    )
    for y, name, coord, color in rows:
        node(out, 55, y, 100, 42, name, color, "#F8FAFC", 13)
        out += [text(175, y + 28, coord, 13, 650)]

    heading(out, 430, "B", "轴怎样进入表示", TEAL)
    for y, title, desc, color in (
        (105, "add", "p = pᵣ + p𝚌", BLUE),
        (205, "concat/split", "channels 分给各轴", TEAL),
        (305, "relative bias", "b(Δr, Δc, …)", AMBER),
        (405, "commuting rotations", "R(x,y)=Rₓ(x)Rᵧ(y)", RED),
    ):
        node(out, 445, y, 150, 46, title, color, "#F8FAFC", 13)
        out += [text(610, y + 29, desc, 13, 650)]

    heading(out, 830, "C", "图文混排的三层坐标", BLUE)
    out += [rect(845, 105, 280, 58, BLUE, "#EFF6FF", 6, 2),
            text(985, 140, "global reading order", 14, 750, "middle", BLUE),
            rect(845, 205, 280, 58, TEAL, "#ECFDF5", 6, 2),
            text(985, 240, "modality / segment identity", 14, 750, "middle", TEAL),
            rect(845, 305, 280, 74, AMBER, "#FFF7ED", 6, 2),
            text(985, 340, "image row / column", 14, 750, "middle", AMBER),
            text(985, 363, "or text line / within-line", 12, 650, "middle", AMBER),
            text(845, 430, "轴共享会碰撞；轴完全分离会削弱", 12, fill=MUTED),
            text(845, 454, "跨模态距离。必须用任务验证。", 12, fill=MUTED)]
    return finish(out, "多轴位置编码首先是坐标建模问题；任何旋转或 bias 公式都必须服从明确的布局与模态语义。")


def extrapolation():
    out = begin(
        "长度扩展方法：相位变换、训练覆盖与成本边界",
        "直接外推、位置插值、逐频率缩放与 ReRoPE 处理不同失配；没有一种公式自动解决远程依赖。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "四种位置变换", RED)
    rows = (
        (100, "Direct", "ρ(Δ)=Δ", RED),
        (190, "PI", "ρ(Δ)=Δ/k", BLUE),
        (280, "NTK / mixed", "ωᵢ→ωᵢ/sᵢ", TEAL),
        (370, "ReRoPE", "ρ(Δ)=min(Δ,w)", AMBER),
    )
    for y, name, formula, color in rows:
        node(out, 55, y, 120, 44, name, color, "#F8FAFC", 13)
        out += [text(195, y + 28, formula, 14, 700, fill=color)]
    out += [text(55, 455, "所有映射都要注明 causal 符号、", 12, fill=MUTED),
            text(55, 478, "训练长度 L₀ 与目标长度 L₁。", 12, fill=MUTED)]

    heading(out, 430, "B", "它们交换了什么风险", BLUE)
    rows2 = (
        (105, "Direct", "未见相位 / 相对距离"),
        (185, "PI", "邻位拥挤；通常需微调"),
        (265, "per-frequency", "不同通道分担外推"),
        (345, "rectified", "窗口外距离被截断"),
        (425, "local mask", "远程边直接删除"),
    )
    for y, name, desc in rows2:
        out += [text(450, y, name, 13, 800, fill=BLUE), text(555, y, desc, 12, 650)]

    heading(out, 830, "C", "三张账必须同时过关", TEAL)
    cards = (
        (110, "position coverage", "训练见过哪些相位/距离", BLUE),
        (235, "attention regime", "候选数、熵与远程路径", TEAL),
        (360, "system contract", "cache、kernel、额外 score", AMBER),
    )
    for y, title, desc, color in cards:
        out += [rect(845, y - 30, 280, 70, color, "#F8FAFC", 7, 2),
                text(985, y - 3, title, 14, 800, "middle", color),
                text(985, y + 23, desc, 12, 650, "middle", MUTED)]
    out += [text(845, 460, "“无限外推”必须保留问号与测试范围。", 13, 700, fill=RED)]
    return finish(out, "位置变换只解决外推问题的一部分；训练覆盖、attention 候选制度、远程任务与系统成本要一起验收。")


def evaluation():
    out = begin(
        "长上下文评测：可接受长度、可利用长度与任务证据",
        "支持 N tokens 只说明接口上限；真正评测要同时扫描长度、证据位置、依赖跨度、干扰和任务类型。",
        (TEAL, RED, BLUE),
    )
    heading(out, 42, "A", "四级 Context 能力", TEAL)
    for y, title, color in (
        (95, "1  accepts input", BLUE),
        (180, "2  numerically stable", TEAL),
        (265, "3  retrieves / tracks", AMBER),
        (350, "4  reasons / improves", RED),
    ):
        node(out, 55, y, 290, 50, title, color, "#F8FAFC", 14)
    out += [text(55, 440, "前一级不是后一级的充分条件。", 14, 700, fill=RED)]

    heading(out, 430, "B", "评测矩阵而非单点", RED)
    x0, y0, cw, ch = 455, 110, 68, 58
    cols = ("4K", "8K", "16K", "32K")
    rows = ("start", "middle", "end", "multi-hop")
    for j, label in enumerate(cols):
        out += [text(x0 + j * cw + 27, 95, label, 12, 700, "middle", RED)]
    for i, label in enumerate(rows):
        out += [text(448, y0 + i * ch + 34, label, 11, 650, "end")]
        for j in range(len(cols)):
            color = TEAL if (i + j) % 3 else AMBER
            out += [rect(x0 + j * cw, y0 + i * ch, 54, 44, color, "#F8FAFC", 4, 1.5)]
    out += [text(455, 385, "再扫描 distractors、needle 数、", 12, fill=MUTED),
            text(455, 410, "dependency span、language 与 seed。", 12, fill=MUTED)]

    heading(out, 830, "C", "指标各自会漏什么", BLUE)
    rows3 = (
        (100, "PPL", "局部 token 可掩盖远程失效"),
        (185, "needle", "单事实检索不等于推理"),
        (270, "LongBench", "任务平均掩盖长度/位置"),
        (355, "RULER", "synthetic 成功不等于真实文档"),
        (440, "latency", "可用但成本可能不可部署"),
    )
    for y, name, caveat in rows3:
        out += [text(845, y, name, 13, 800, fill=BLUE), text(930, y, caveat, 11, 650)]
    return finish(out, "有效上下文不是模型卡上的单一数字，而是任务、位置、依赖跨度、质量阈值和系统预算共同定义的曲线。")


FIGURES = {
    "fig-position-permutation-symmetry-v1.svg": symmetry,
    "fig-learned-absolute-position-contract-v1.svg": absolute_position,
    "fig-sinusoidal-frequency-shift-v1.svg": sinusoidal,
    "fig-relative-position-injection-probe-v1.svg": relative_position,
    "fig-rope-rotation-relative-inner-product-v1.svg": rope,
    "fig-multiaxis-multimodal-position-v1.svg": multiaxis,
    "fig-context-extension-methods-v1.svg": extrapolation,
    "fig-long-context-evaluation-matrix-v1.svg": evaluation,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, render in FIGURES.items():
        target = OUT / filename
        target.write_text(render(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
