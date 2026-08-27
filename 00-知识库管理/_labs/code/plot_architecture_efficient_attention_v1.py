#!/usr/bin/env python3
"""Generate the eight original ARCH-49--56 efficient-attention figures."""

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def cost_ledger():
    out = begin(
        "Attention 成本不是一个 O(n²)：阶段、张量与瓶颈总账",
        "Projection、pairwise arithmetic、score storage、HBM traffic 与 decode cache 分属不同账本。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "Prefill：一次处理 n 个 Token", RED)
    rows = ((110, "QKV/O projections", "≈ 4 n d²", BLUE), (205, "QKᵀ + AV", "≈ 2 n² d", RED),
            (300, "naive scores", "≈ h n² elements", AMBER), (395, "FFN", "≈ 2 n d d_ff", TEAL))
    for y, name, value, color in rows:
        out += [text(55, y, name, 13, 700, fill=color), text(250, y, value, 13, 800)]
        out += [rect(55, y + 18, min(285, 65 + (y - 95) // 2), 11, color, color, 4, 1)]
    out += [text(55, 468, "crossover 取决于 n/d、kernel 与 hardware。", 12, fill=MUTED)]

    heading(out, 430, "B", "Decode：每步只有一个 Query", BLUE)
    node(out, 455, 105, 285, 54, "read historical K/V cache", BLUE, "#EFF6FF", 14)
    out += [line(598, 162, 598, 205, INK, 2, marker="a3")]
    node(out, 455, 218, 285, 64, "per layer: O(t d_kv) bytes + MACs", AMBER, "#FFF7ED", 13)
    out += [line(598, 285, 598, 328, INK, 2, marker="a3")]
    node(out, 455, 342, 285, 64, "often bandwidth / latency bound", RED, "#FEF2F2", 14)
    out += [text(455, 454, "batch 与 context 越大，cache bytes 越关键。", 12, fill=MUTED)]

    heading(out, 830, "C", "四个不同优化靶点", TEAL)
    items = ((110, "Sparse / low-rank", "改变边或模型近似", RED),
             (200, "Kernel feature", "改变相似度或作随机近似", AMBER),
             (290, "FlashAttention", "不改模型，降低 HBM IO", TEAL),
             (380, "MQA / GQA / MLA", "压缩 decode cache", BLUE))
    for y, title, desc, color in items:
        node(out, 845, y, 125, 42, title, color, "#F8FAFC", 12)
        out += [text(985, y + 26, desc, 12, 650)]
    return finish(out, "先写阶段与张量，再谈复杂度；同为‘高效’的方法可能根本不在优化同一瓶颈。")


def sparse_patterns():
    out = begin(
        "稀疏 Attention：边数、图直径、感受野与 Kernel 可实现性",
        "Mask 定义信息图；真正省时还要求数据布局与 block-sparse kernel 能跳过被删边。",
        (BLUE, AMBER, RED),
    )
    heading(out, 42, "A", "四种 Relation Pattern", BLUE)
    labels = (("dense", RED), ("local w", BLUE), ("dilated", AMBER), ("global+local", TEAL))
    for k, (label, color) in enumerate(labels):
        x0 = 55 + k * 75
        out += [text(x0 + 26, 105, label, 11, 700, "middle", color)]
        for i in range(6):
            for j in range(6):
                keep = (k == 0 or (k == 1 and abs(i-j) <= 1) or
                        (k == 2 and (i == j or abs(i-j) in (2, 4))) or
                        (k == 3 and (i == 0 or j == 0 or abs(i-j) <= 1)))
                out += [rect(x0 + j * 9, 130 + i * 9, 7, 7, color if keep else GRID,
                             color if keep else "#F8FAFC", 1, 1)]
    out += [text(55, 250, "pairs: n² / nw / sparse strides / nw+ng", 13, 700),
            text(55, 288, "但单层最远路径与多层传播不同。", 13, fill=MUTED),
            text(55, 440, "结构先验必须和任务的远程依赖位置匹配。", 13, 700, fill=RED)]

    heading(out, 430, "B", "Layer-by-Layer Receptive Field", AMBER)
    for i in range(7):
        circle_x = 465 + i * 43
        out += [circle(circle_x, 150, 9, BLUE, "#EFF6FF", 2)]
        if i: out += [line(circle_x - 34, 150, circle_x - 10, 150, BLUE, 2)]
    out += [text(455, 205, "local w=1：每层最多扩一跳", 13, 700, fill=BLUE)]
    for i in range(7):
        circle_x = 465 + i * 43
        out += [circle(circle_x, 300, 9, TEAL if i == 0 else AMBER, "#F8FAFC", 2)]
        if i: out += [line(465, 300, circle_x - 10, 300, TEAL, 1.5, "4 3")]
    out += [text(455, 355, "global token：短路径，但形成 bottleneck", 13, 700, fill=TEAL),
            text(455, 430, "随机边可降图直径；结果依抽样与层数。", 12, fill=MUTED)]

    heading(out, 830, "C", "功能稀疏 ≠ 系统稀疏", RED)
    node(out, 845, 110, 275, 52, "dense scores + mask", RED, "#FEF2F2", 14)
    out += [text(845, 190, "✓ 语义正确", 13, 700, fill=TEAL), text(985, 190, "× 仍物化 n²", 13, 700, fill=RED)]
    node(out, 845, 255, 275, 52, "block indices + sparse kernel", TEAL, "#ECFDF5", 13)
    out += [text(845, 335, "✓ 跳过 blocks", 13, 700, fill=TEAL), text(985, 335, "? occupancy / padding", 13, 700, fill=AMBER),
            text(845, 410, "不规则 sparsity 可能被索引和 load imbalance 吞掉。", 12, fill=MUTED)]
    return finish(out, "稀疏 Attention 要同时提交 relation graph、路径证书、edge ledger 和可执行 kernel，而不只是一张 mask。")


def low_rank():
    out = begin(
        "低秩/序列压缩 Attention：压哪条轴，误差在哪里进入",
        "Linformer 类方法先把 K/V 的长度轴 n 投影为 k；复杂度下降以 k≪n 和可迁移投影为前提。",
        (TEAL, BLUE, RED),
    )
    heading(out, 42, "A", "沿 Sequence Axis 压缩", TEAL)
    node(out, 55, 105, 115, 230, "K,V : n × d", BLUE, "#EFF6FF", 14)
    node(out, 230, 165, 105, 110, "E,F : k × n", AMBER, "#FFF7ED", 13)
    out += [line(173, 220, 225, 220, INK, 2.5, marker="a3")]
    node(out, 55, 390, 280, 62, "K'=EK, V'=FV : k × d", TEAL, "#ECFDF5", 15)
    out += [line(282, 278, 195, 385, INK, 2.5, marker="a3"),
            text(55, 486, "score 从 n×n 变 n×k。", 13, 800, fill=TEAL)]

    heading(out, 430, "B", "Spectral Tail 只是第一道误差", BLUE)
    heights = [165, 120, 85, 58, 38, 26, 18, 12]
    for i, h in enumerate(heights):
        out += [rect(465 + i * 31, 330 - h, 21, h, BLUE if i < 3 else GRID,
                     BLUE if i < 3 else "#F8FAFC", 2, 1)]
    out += [line(455, 330, 735, 330, INK, 1.5), text(455, 370, "keep k", 12, 700, fill=BLUE),
            text(610, 370, "discarded tail", 12, 700, fill=RED),
            text(455, 420, "K/V projection → logits → softmax → output", 13, 700),
            text(455, 452, "每一步可放大或重塑误差。", 13, fill=MUTED)]

    heading(out, 830, "C", "实现与外推合同", RED)
    items = ((110, "k fixed / grows?"), (185, "E/F shared by heads/layers?"),
             (260, "causal leakage avoided?"), (335, "new n: resize or new parameters?"),
             (410, "projection MAC + memory counted?"))
    for y, item in items:
        out += [circle(855, y, 7, RED, "#F8FAFC", 2), text(875, y + 5, item, 12, 650)]
    return finish(out, "‘Attention 近似低秩’必须变成明确的轴、rank、norm、长度和输出误差合同，才能支持工程结论。")


def kernel_linear():
    out = begin(
        "Kernel Linear Attention：结合律、归一化与 Causal State",
        "当 sim(q,k)=φ(q)ᵀφ(k) 时，可先聚合 feature–value state；这可能是新 kernel，也可能是近似。",
        (AMBER, TEAL, BLUE),
    )
    heading(out, 42, "A", "Dense Left Association", AMBER)
    node(out, 55, 105, 90, 50, "Φ(Q): n×r", BLUE, "#EFF6FF", 12)
    node(out, 185, 105, 90, 50, "Φ(K)ᵀ: r×n", TEAL, "#ECFDF5", 12)
    node(out, 55, 235, 220, 58, "A = Φ(Q)Φ(K)ᵀ : n×n", RED, "#FEF2F2", 13)
    node(out, 125, 370, 90, 50, "V: n×d_v", AMBER, "#FFF7ED", 12)
    out += [line(145, 160, 165, 225, INK, 2, marker="a3"), line(230, 160, 205, 225, INK, 2, marker="a3"),
            line(165, 298, 165, 362, INK, 2, marker="a3"), text(55, 468, "work/storage includes n²", 13, 800, fill=RED)]

    heading(out, 430, "B", "Right Association + Denominator", TEAL)
    node(out, 455, 105, 125, 52, "S=Φ(K)ᵀV: r×d_v", TEAL, "#ECFDF5", 11)
    node(out, 620, 105, 120, 52, "z=Φ(K)ᵀ1: r", AMBER, "#FFF7ED", 11)
    node(out, 475, 245, 245, 75, "o_i = φ(q_i)ᵀS / φ(q_i)ᵀz", BLUE, "#EFF6FF", 14)
    out += [line(520, 160, 570, 235, INK, 2, marker="a3"), line(680, 160, 625, 235, INK, 2, marker="a3"),
            text(455, 375, "work ≈ O(n r d_v)", 13, 800, fill=TEAL),
            text(455, 415, "denominator sign / near-zero is part of semantics。", 12, fill=MUTED)]

    heading(out, 830, "C", "Causal = Recurrent State", BLUE)
    node(out, 845, 105, 275, 58, "S_t=S_{t-1}+φ(k_t)v_tᵀ", TEAL, "#ECFDF5", 13)
    node(out, 845, 210, 275, 58, "z_t=z_{t-1}+φ(k_t)", AMBER, "#FFF7ED", 13)
    node(out, 845, 315, 275, 65, "o_t=φ(q_t)ᵀS_t / φ(q_t)ᵀz_t", BLUE, "#EFF6FF", 13)
    out += [text(845, 425, "固定 state 压缩历史：快，但存在容量/遗忘边界。", 12, 700, fill=RED)]
    return finish(out, "结合律只对可分解 kernel 生效；是否等于 Softmax、是否稳定、是否保留远程信息必须分别回答。")


def performer():
    out = begin(
        "Performer：正随机特征怎样近似 Softmax Kernel",
        "先估计 exp(qᵀk)，再把随机误差传播到归一化 attention；feature 数 m 控制成本与方差。",
        (BLUE, RED, AMBER),
    )
    heading(out, 42, "A", "Gaussian Moment Identity", BLUE)
    node(out, 55, 105, 285, 66, "e^{qᵀk} = E_ω[ψ_ω(q) ψ_ω(k)]", BLUE, "#EFF6FF", 15)
    out += [text(55, 220, "ψ_ω(x)=exp(ωᵀx-‖x‖²/2)", 14, 700),
            text(55, 275, "m samples → positive feature vector", 13, fill=MUTED)]
    for i in range(5):
        out += [circle(75 + i * 58, 355 + (i % 2) * 22, 12, AMBER, "#FFF7ED", 2)]
    out += [text(55, 445, "orthogonal features target lower variance。", 13, 700, fill=AMBER)]

    heading(out, 430, "B", "两层误差不能混写", RED)
    node(out, 455, 105, 285, 52, "kernel:  K̂_ij − K_ij", AMBER, "#FFF7ED", 13)
    node(out, 455, 215, 285, 60, "ratio: N̂_i/D̂_i − N_i/D_i", RED, "#FEF2F2", 13)
    node(out, 455, 335, 285, 58, "output: ô_i − o_i", BLUE, "#EFF6FF", 13)
    out += [line(598, 160, 598, 205, INK, 2, marker="a3"), line(598, 278, 598, 325, INK, 2, marker="a3"),
            text(455, 447, "小 denominator 会放大比值误差。", 13, 800, fill=RED)]

    heading(out, 830, "C", "m 的三方账本", AMBER)
    items = ((115, "↑ m", "↓ random error", TEAL), (215, "↑ m", "↑ feature MAC/state", RED),
             (315, "fixed seed", "可复现 ≠ 无偏消失", BLUE), (415, "new draw", "增加 estimator variance", AMBER))
    for y, a, b, color in items:
        node(out, 845, y, 80, 38, a, color, "#F8FAFC", 12)
        out += [text(945, y + 24, b, 12, 650)]
    return finish(out, "Performer 的理论对象是随机 kernel 估计；真实速度与质量还取决于 m、数值稳定和实现 crossover。")


def flash():
    out = begin(
        "FlashAttention：不物化 n×n，怎样仍计算 Exact Attention",
        "Q/K/V 分块进入 SRAM；online softmax 保存每行 max、normalizer 与输出 accumulator，并在新块到来时重标度。",
        (TEAL, RED, BLUE),
    )
    heading(out, 42, "A", "Memory Hierarchy", TEAL)
    node(out, 55, 105, 285, 72, "HBM: Q, K, V, O", BLUE, "#EFF6FF", 16)
    node(out, 95, 245, 205, 68, "SRAM: Q_i × K_j tile", TEAL, "#ECFDF5", 14)
    out += [line(200, 180, 200, 235, INK, 2.5, "5 4", "a3"),
            text(55, 365, "never write full S or P to HBM", 13, 800, fill=RED),
            text(55, 420, "arithmetic still visits all dense pairs。", 13, fill=MUTED)]

    heading(out, 430, "B", "Online Softmax Merge", RED)
    node(out, 455, 95, 285, 56, "old state: (m, ℓ, o)", BLUE, "#EFF6FF", 14)
    node(out, 455, 195, 285, 56, "new tile max: m_b", AMBER, "#FFF7ED", 14)
    node(out, 455, 295, 285, 84, "m'=max(m,m_b); rescale ℓ and o", RED, "#FEF2F2", 13)
    out += [line(598, 154, 598, 185, INK, 2, marker="a3"), line(598, 254, 598, 285, INK, 2, marker="a3"),
            text(455, 430, "o accumulator 用同一 scale 合并。", 13, 700, fill=TEAL)]

    heading(out, 830, "C", "Exact 的精确含义", BLUE)
    items = ((105, "✓ same mathematical attention"), (185, "✓ no low-rank/sparse approximation"),
             (265, "≠ bitwise same reduction order"), (345, "≠ linear arithmetic complexity"),
             (425, "≠ every shape/hardware faster"))
    for y, label in items:
        color = TEAL if label.startswith("✓") else RED
        out += [text(845, y, label[:1], 16, 800, fill=color), text(875, y, label[2:], 12, 650)]
    return finish(out, "FlashAttention 优化的是数据搬运与中间存储；‘exact’和‘quadratic arithmetic’可以同时成立。")


def kv_cache():
    out = begin(
        "KV Cache、MHA、GQA、MQA：Head 自由度怎样换成 Bytes",
        "Query heads 决定并行读取视角；KV heads 决定每层每 token 缓存多少 K/V 通道。",
        (BLUE, TEAL, AMBER),
    )
    heading(out, 42, "A", "Head Mapping", BLUE)
    configs = ((110, "MHA", 8, RED), (230, "GQA", 4, AMBER), (350, "MQA", 1, TEAL))
    for y, name, groups, color in configs:
        out += [text(55, y + 16, name, 13, 800, fill=color)]
        for h in range(8):
            out += [circle(115 + h * 28, y, 8, BLUE, "#EFF6FF", 1.5)]
            group = h if groups == 8 else (h * groups // 8)
            gx = 115 + group * (196 / max(1, groups - 1)) if groups > 1 else 213
            out += [line(115 + h * 28, y + 10, gx, y + 43, color, 1)]
        for g in range(groups):
            gx = 115 + g * (196 / max(1, groups - 1)) if groups > 1 else 213
            out += [rect(gx - 9, y + 48, 18, 18, color, "#F8FAFC", 2, 1.5)]
    out += [text(55, 470, "h_q fixed；h_kv: h → g → 1", 13, 800, fill=BLUE)]

    heading(out, 430, "B", "Cache Scalars / Layer", TEAL)
    node(out, 455, 105, 285, 68, "2 · B · T · h_kv · d_h", TEAL, "#ECFDF5", 16)
    rows = ((225, "MHA", "h_kv=h", RED), (300, "GQA", "h_kv=g", AMBER), (375, "MQA", "h_kv=1", TEAL))
    for y, name, value, color in rows:
        out += [text(455, y, name, 13, 800, fill=color), text(555, y, value, 13, 700)]
    out += [text(455, 445, "bytes 再乘 layers × dtype bytes。", 12, fill=MUTED)]

    heading(out, 830, "C", "Cache 少不等于一定快", AMBER)
    items = ((110, "memory bandwidth", "通常下降", TEAL), (190, "K/V projection params", "下降", BLUE),
             (270, "quality / training", "需 uptraining/消融", RED), (350, "TP communication", "依 group mapping", AMBER),
             (430, "latency/throughput", "依 batch、kernel、quant", RED))
    for y, a, b, color in items:
        out += [text(845, y, a, 12, 800, fill=color), text(990, y, b, 11, 650)]
    return finish(out, "MHA→GQA→MQA 是 KV-head 数的连续设计轴；缓存公式是恒等式，质量和速度是协议结论。")


def mla():
    out = begin(
        "MLA：联合 KV Latent、投影吸收与 Partial RoPE",
        "训练可展开为多头 K/V；解码缓存低维 content latent 加不可任意吸收的位置 key 分支。",
        (RED, TEAL, BLUE),
    )
    heading(out, 42, "A", "Encode Once into Cache", RED)
    node(out, 55, 105, 285, 52, "x_t : d", BLUE, "#EFF6FF", 15)
    node(out, 55, 215, 285, 62, "c_t^{KV}=W_D x_t : d_c", TEAL, "#ECFDF5", 14)
    node(out, 55, 340, 285, 62, "cache [c_t^{KV}, k_t^R]", RED, "#FEF2F2", 14)
    out += [line(198, 160, 198, 205, INK, 2, marker="a3"), line(198, 280, 198, 330, INK, 2, marker="a3"),
            text(55, 455, "cache/token ≈ d_c + d_R, not h(d_k+d_v)", 12, 800, fill=RED)]

    heading(out, 430, "B", "Two Algebraic Forms", TEAL)
    node(out, 455, 95, 285, 70, "training: K_h=W^K_h c, V_h=W^V_h c", BLUE, "#EFF6FF", 12)
    node(out, 455, 240, 285, 76, "decode: absorb W^K; aggregate c", TEAL, "#ECFDF5", 12)
    out += [line(598, 168, 598, 230, INK, 2.5, "5 4", "a3"),
            text(455, 370, "exact in real algebra for absorbable branch", 12, 700, fill=TEAL),
            text(455, 410, "BF16 order and RoPE branch need separate audit。", 12, fill=MUTED)]

    heading(out, 830, "C", "Evidence Ledger", BLUE)
    items = ((105, "I", "shape/cache/reparameterization", TEAL), (185, "E", "DeepSeek-V2 system comparison", BLUE),
             (265, "E", "10907 controlled ablations", AMBER), (345, "H", "11111 limited-family optimality", RED),
             (425, "O", "MTP、quant、kernel Pareto frontier", RED))
    for y, tag, claim, color in items:
        node(out, 845, y, 38, 34, tag, color, "#F8FAFC", 12)
        out += [text(900, y + 22, claim, 11, 650)]
    return finish(out, "MLA 的强点要拆成 cache bytes、可吸收代数、head/position 设计和系统实测；整模型胜负不能替代消融。")


FIGURES = {
    "fig-attention-phase-cost-ledger-v1.svg": cost_ledger,
    "fig-sparse-attention-pattern-path-kernel-v1.svg": sparse_patterns,
    "fig-low-rank-sequence-compression-v1.svg": low_rank,
    "fig-kernel-linear-attention-state-v1.svg": kernel_linear,
    "fig-performer-random-feature-error-v1.svg": performer,
    "fig-flashattention-io-online-softmax-v1.svg": flash,
    "fig-kv-cache-mha-gqa-mqa-v1.svg": kv_cache,
    "fig-mla-latent-cache-reparameterization-v1.svg": mla,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, factory in FIGURES.items():
        path = OUT / filename
        path.write_text(factory(), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
