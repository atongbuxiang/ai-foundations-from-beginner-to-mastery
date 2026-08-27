#!/usr/bin/env python3
"""Generate the eight original ARCH-25--32 Attention teaching figures."""

from __future__ import annotations

from pathlib import Path
from math import exp, log

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture"


def qkv_contract():
    out = begin(
        "Q/K/V 不是三份副本：它们承担三种角色",
        "query 提出检索需求，key 提供可匹配地址，value 是真正被加权返回的内容。",
        (BLUE, TEAL, AMBER),
    )
    heading(out, 42, "A", "图书馆式内容寻址", BLUE)
    node(out, 55, 105, 270, 70, "query：我现在需要什么？", BLUE, "#EFF6FF", 16)
    out += [line(190, 178, 190, 220, BLUE, 3, marker="a0")]
    node(out, 55, 235, 270, 70, "与每个 key 计算匹配分数", TEAL, "#ECFDF5", 16)
    out += [line(190, 308, 190, 350, TEAL, 3, marker="a1")]
    node(out, 55, 365, 270, 70, "按权重汇总对应 value", AMBER, "#FFF7ED", 16)
    out += [text(55, 480, "地址相似不等于内容相同。", 15, 700, fill=RED)]

    heading(out, 430, "B", "一个 query 的逐项读取", TEAL)
    out += [circle(490, 270, 30, BLUE, "#EFF6FF", 2.5), text(490, 277, "q_i", 17, 700, "middle", BLUE)]
    for j, (y, score, val, col) in enumerate(
        ((120, ".70", "v₁", TEAL), (260, ".20", "v₂", AMBER), (400, ".10", "v₃", RED)), 1
    ):
        out += [rect(610, y-30, 92, 52, col, "#F8FAFC", 7, 2), text(656, y+3, f"k{j}", 15, 700, "middle", col),
                line(522, 270, 607, y, col, 1.5 + 4*float(score), marker="a1"),
                rect(720, y-30, 70, 52, col, "#F8FAFC", 7, 2), text(755, y+3, val, 15, 700, "middle", col),
                text(570, (270+y)/2 - 6, score, 14, 700, "middle", col)]
    out += [text(455, 480, "o_i = .70 v₁ + .20 v₂ + .10 v₃", 17, 700, cls="math")]

    heading(out, 830, "C", "对象与 shape 合同", AMBER)
    rows = ((105, "Q", "T_q × d_k", "提出 T_q 次读取"), (205, "K", "T_k × d_k", "提供 T_k 个地址"),
            (305, "V", "T_k × d_v", "提供 T_k 份内容"), (405, "O", "T_q × d_v", "每个 query 得一份返回"))
    for y, tag, shape, role in rows:
        out += [rect(845, y-25, 46, 38, BLUE if tag in "QO" else TEAL, "#F8FAFC", 6, 2),
                text(868, y+1, tag, 16, 800, "middle", BLUE if tag in "QO" else TEAL),
                text(910, y, shape, 16, 700), text(910, y+29, role, 14, fill=MUTED)]
    return finish(out, "先分清检索请求、匹配地址和返回内容，再写分数、归一化与矩阵乘法。")


def scaled_softmax():
    out = begin(
        "Scaled Dot-Product Attention：从 logit 到稳定的行分布",
        "缩放控制典型 logit 尺度；减去行最大值保持精确 softmax，却避免指数溢出。",
        (AMBER, BLUE, RED),
    )
    heading(out, 42, "A", "为什么除以 sqrt(d_k)", AMBER)
    out += [text(55, 115, "qᵀk = Σ q_r k_r", 19, 750, cls="math"),
            text(55, 170, "若坐标独立、中心化、Var=1：", 15, fill=MUTED),
            text(55, 220, "Var(qᵀk) = d_k", 22, 800, fill=RED, cls="math"),
            line(70, 265, 320, 265, GRID, 2),
            text(55, 315, "Var(qᵀk / sqrt(d_k)) = 1", 18, 750, fill=TEAL, cls="math"),
            text(55, 385, "这是条件化方差推导；", 15, fill=MUTED),
            text(55, 418, "相关、非中心或重尾坐标需实测。", 15, fill=MUTED)]

    heading(out, 430, "B", "一行 logits 的数值账", BLUE)
    logits = (1000.0, 1001.0, 999.0)
    shifted = tuple(z-max(logits) for z in logits)
    weights = tuple(exp(z)/sum(exp(t) for t in shifted) for z in shifted)
    labels = ((120, "raw z", "[1000, 1001, 999]", RED), (225, "z − max(z)", "[−1, 0, −2]", BLUE),
              (330, "exp", "[0.368, 1, 0.135]", AMBER), (435, "normalize", f"[{weights[0]:.3f}, {weights[1]:.3f}, {weights[2]:.3f}]", TEAL))
    for y, lab, val, col in labels:
        out += [text(450, y, lab, 15, 700, fill=col), rect(565, y-30, 220, 48, col, "#F8FAFC", 6, 2),
                text(675, y+1, val, 15, 700, "middle", col)]

    heading(out, 830, "C", "Softmax 的四条语义", RED)
    facts = ((110, "平移不变", "softmax(z+c1)=softmax(z)"), (205, "行归一", "a_j>0, Σa_j=1"),
             (300, "温度敏感", "scale changes entropy"), (395, "全遮蔽例外", "undefined unless contract says how"))
    for y, title, formula in facts:
        out += [circle(860, y-5, 12, TEAL if y < 300 else RED, "#F8FAFC", 2), text(860, y, str((y-15)//95), 12, 700, "middle"),
                text(890, y-7, title, 15, 750), text(890, y+22, formula, 14, fill=MUTED)]
    return finish(out, "缩放是统计尺度控制，减最大值是等价数值变换；两者的理由不能混写。")


def masks_visibility():
    out = begin(
        "Attention Mask 是可见性合同，不是事后把权重涂黑",
        "padding、causal 与结构 mask 规定哪些 query-key pair 存在；必须在 softmax 前进入 logits。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "Inclusive causal 可见性矩阵", RED)
    x0, y0, s = 80, 115, 55
    for i in range(6):
        out += [text(x0-25, y0+i*s+35, f"q{i+1}", 13, 700, "middle", RED), text(x0+i*s+27, y0-18, f"k{i+1}", 13, 700, "middle", BLUE)]
        for j in range(6):
            vis = j <= i
            out += [rect(x0+j*s, y0+i*s, 48, 48, TEAL if vis else GRID, "#D1FAE5" if vis else "#F1F5F9", 3, 1.5),
                    text(x0+j*s+24, y0+i*s+30, "✓" if vis else "×", 16, 700, "middle", TEAL if vis else MUTED)]
    out += [text(55, 480, "第 i 行只看 1…i；关系本身编码顺序。", 15, 700, fill=RED)]

    heading(out, 430, "B", "三种 mask 不要混用", BLUE)
    rows = ((115, "key padding", "某些列对所有有效 query 不可见", BLUE),
            (230, "query padding", "通常用 loss/output mask 处理", AMBER),
            (345, "structural / causal", "逐 pair 的允许关系", RED))
    for y, title, desc, col in rows:
        out += [rect(455, y-35, 300, 72, col, "#F8FAFC", 8, 2), text(475, y-7, title, 16, 750, fill=col),
                text(475, y+22, desc, 14, fill=MUTED)]

    heading(out, 830, "C", "错误顺序与安全顺序", TEAL)
    node(out, 845, 100, 280, 54, "S = QKᵀ / sqrt(d)", BLUE, "#EFF6FF", 15)
    out += [line(985, 157, 985, 188, INK, 2, marker="a3")]
    node(out, 845, 200, 280, 54, "S + M  (0 or −∞)", RED, "#FEE2E2", 15)
    out += [line(985, 257, 985, 288, INK, 2, marker="a3")]
    node(out, 845, 300, 280, 54, "row-wise stable softmax", TEAL, "#ECFDF5", 15)
    out += [text(845, 402, "softmax 后乘 0 会破坏行和；", 15, 700, fill=RED),
            text(845, 434, "全遮蔽行须显式定义。", 15, 700, fill=RED)]
    return finish(out, "先定义可见关系，再归一化；mask convention、dtype 与全遮蔽行为必须写进实现合同。")


def self_cross_shapes():
    out = begin(
        "Self-Attention 与 Cross-Attention：来源不同，矩阵合同相同",
        "score 的行数来自 query，列数来自 key/value；cross-attention 允许 T_q 与 T_k 不同。",
        (BLUE, TEAL, AMBER),
    )
    heading(out, 42, "A", "Self：Q/K/V 来自同一序列", BLUE)
    node(out, 55, 105, 285, 58, "X : T × d_model", BLUE, "#EFF6FF", 16)
    for x, lab, col in ((55, "XW_Q", BLUE), (150, "XW_K", TEAL), (245, "XW_V", AMBER)):
        out += [line(x+47, 166, x+47, 220, col, 2, marker="a1"), rect(x, 230, 86, 48, col, "#F8FAFC", 6, 2), text(x+43, 260, lab, 14, 700, "middle", col)]
    out += [text(55, 335, "共享来源 ≠ 共享投影", 16, 750, fill=RED),
            text(55, 390, "score: T × T", 18, 750, cls="math"), text(55, 435, "output: T × d_v", 18, 750, cls="math")]

    heading(out, 430, "B", "Cross：query 与 memory 分源", TEAL)
    node(out, 450, 90, 300, 55, "X_q : T_q × d_model", BLUE, "#EFF6FF", 15)
    node(out, 450, 190, 300, 55, "X_m : T_k × d_model", TEAL, "#ECFDF5", 15)
    out += [line(525, 148, 525, 305, BLUE, 2.5, marker="a0"), line(600, 248, 600, 305, TEAL, 2.5, marker="a1"), line(675, 248, 675, 305, AMBER, 2.5, marker="a2")]
    for x, lab, col in ((480, "Q", BLUE), (555, "K", TEAL), (630, "V", AMBER)):
        out += [rect(x, 315, 62, 45, col, "#F8FAFC", 5, 2), text(x+31, 343, lab, 15, 800, "middle", col)]
    out += [text(455, 405, "score: T_q × T_k", 18, 750, cls="math"), text(455, 450, "output: T_q × d_v", 18, 750, cls="math")]

    heading(out, 830, "C", "shape ledger", AMBER)
    rows = ((105, "QKᵀ", "(T_q×d_k)(d_k×T_k)"), (205, "A", "T_q × T_k"),
            (305, "AV", "(T_q×T_k)(T_k×d_v)"), (405, "O", "T_q × d_v"))
    for y, name, shape in rows:
        out += [text(845, y, name, 17, 800, fill=BLUE if name in "QO" else TEAL), text(905, y, shape, 15, 650)]
    return finish(out, "只要守住 inner dimensions，self/cross 的统一公式自然成立；长度来源由任务接口决定。")


def multihead_budget():
    out = begin(
        "Multi-Head Attention：多个投影子空间与一张完整预算表",
        "固定总宽时，增加 head 数通常缩小每头维度；标准四投影主阶参数量并不随 head 数增加。",
        (TEAL, BLUE, RED),
    )
    heading(out, 42, "A", "分头—独立寻址—拼接", TEAL)
    node(out, 55, 90, 290, 55, "X : T × d_model", BLUE, "#EFF6FF", 16)
    for i, col in enumerate((BLUE, TEAL, AMBER, RED)):
        x = 55 + i*76
        out += [line(x+34, 148, x+34, 205, col, 2, marker="a1"), rect(x, 215, 68, 100, col, "#F8FAFC", 6, 2),
                text(x+34, 245, f"head {i+1}", 13, 750, "middle", col), text(x+34, 280, "T×d_h", 13, 650, "middle")]
    out += [line(89, 318, 190, 370, BLUE, 2), line(165, 318, 190, 370, TEAL, 2), line(241, 318, 190, 370, AMBER, 2), line(317, 318, 190, 370, RED, 2),
            rect(80, 380, 220, 48, TEAL, "#ECFDF5", 6, 2), text(190, 410, "Concat → W_O", 16, 750, "middle", TEAL)]

    heading(out, 430, "B", "标准参数量：h 消去", BLUE)
    out += [text(450, 115, "h d_h = d_model", 20, 800, fill=BLUE, cls="math"),
            text(450, 180, "W_Q, W_K, W_V : 3 d_model²", 17, 700, cls="math"),
            text(450, 235, "W_O : d_model²", 17, 700, cls="math"),
            line(455, 270, 750, 270, GRID, 2), text(450, 320, "total ≈ 4 d_model²", 22, 850, fill=TEAL, cls="math"),
            text(450, 390, "偏置另计；GQA/MQA/unequal dims 需重算。", 14, fill=MUTED),
            text(450, 430, "score 元素仍为 B·h·T_q·T_k。", 15, 700, fill=RED)]

    heading(out, 830, "C", "更多头会改变什么", RED)
    rows = ((105, "per-head width", "d_h = d_model / h ↓"), (195, "score storage", "B h T_q T_k ↑"),
            (285, "kernel scheduling", "small GEMMs / fusion change"), (375, "functional use", "must test ablation/pruning"))
    for y, title, value in rows:
        out += [text(845, y, title, 15, 750, fill=RED), text(845, y+30, value, 14, fill=MUTED)]
    return finish(out, "多头不是免费表达力：参数、每头宽度、score 存储、kernel 和训练后利用率必须分开审计。")


def geometry_kernel_probability():
    out = begin(
        "Attention 的三种数学视角：几何、核与条件分布",
        "同一组权重可同时由向量匹配、指数核和可见位置上的 categorical distribution 来理解。",
        (BLUE, AMBER, TEAL),
    )
    heading(out, 42, "A", "几何：dot product 混合角度与范数", BLUE)
    out += [line(165, 340, 165, 120, GRID, 2), line(65, 340, 345, 340, GRID, 2),
            line(165, 340, 305, 170, BLUE, 4, marker="a0"), line(165, 340, 300, 275, TEAL, 4, marker="a1"),
            path("M220 340A55 55 0 0 0 207 298", AMBER, 3), text(310, 165, "q", 17, 800, fill=BLUE),
            text(305, 280, "k", 17, 800, fill=TEAL), text(215, 315, "θ", 16, 750, fill=AMBER),
            text(55, 420, "qᵀk = ||q|| ||k|| cos θ", 18, 750, cls="math"),
            text(55, 465, "cosine normalization removes norm channel.", 14, fill=MUTED)]

    heading(out, 430, "B", "核：指数 affinity 的 feature 展开", AMBER)
    out += [text(450, 110, "K(q,k)=exp(qᵀk)", 20, 800, fill=AMBER, cls="math"),
            text(450, 175, "= Σₙ (qᵀk)ⁿ / n!", 18, 700, cls="math"),
            text(450, 235, "= <φ(q), φ(k)>", 19, 800, fill=TEAL, cls="math"),
            line(465, 275, 740, 275, GRID, 2), text(450, 325, "finite/random features", 16, 750, fill=BLUE),
            text(450, 360, "approximate numerator + denominator", 14, fill=MUTED),
            text(450, 415, "small denominator can amplify error", 15, 750, fill=RED)]

    heading(out, 830, "C", "概率：每行是位置分布", TEAL)
    weights = (.56, .25, .13, .06)
    for i, w in enumerate(weights):
        x = 850 + i*72
        h = 150*w/.56
        out += [rect(x, 380-h, 44, h, TEAL, "#A7F3D0", 3, 2), text(x+22, 405, f"k{i+1}", 13, 700, "middle"),
                text(x+22, 360-h, f"{w:.2f}", 13, 700, "middle", TEAL)]
    out += [line(840, 381, 1145, 381, GRID, 2), text(845, 115, "a_ij = p(J=j | q_i, visible keys)", 15, 700, cls="math"),
            text(845, 165, "o_i lies in convex hull{v_j}", 15, 700, fill=BLUE),
            text(845, 445, "这不是‘位置 j 为真’的概率。", 15, 750, fill=RED)]
    return finish(out, "三种视角互补：几何解释 logit，核解释 factorization，概率解释行归一；都不自动给因果解释。")


def rank_effective_rank():
    out = begin(
        "Attention 的秩：logit、权重、输出与有效秩是四本账",
        "低秩 logits 经 row-softmax 后可变成满秩；严格满秩也可能谱高度集中、数值上近似低维。",
        (RED, BLUE, TEAL),
    )
    heading(out, 42, "A", "三处 rank 不可串用", RED)
    boxes = ((90, "L = QKᵀ", "rank(L) ≤ d_k", BLUE), (225, "A = row-softmax(L+M)", "nonlinear: rank can increase", AMBER),
             (360, "O = AV", "rank(O) ≤ min(rank A, rank V)", TEAL))
    for y, title, claim, col in boxes:
        node(out, 55, y, 300, 62, title, col, "#F8FAFC", 16)
        out += [text(55, y+93, claim, 14, 700, fill=col)]
        if y < 360:
            out += [line(205, y+105, 205, y+132, INK, 2, marker="a3")]

    heading(out, 430, "B", "因果矩阵：满秩不等于健康", BLUE)
    x0, y0, s = 470, 110, 46
    for i in range(6):
        for j in range(6):
            if j > i:
                fill, val, col = "#F1F5F9", "0", GRID
            elif j == i:
                fill, val, col = "#FEE2E2", "+", RED
            else:
                fill, val, col = "#EFF6FF", "·", BLUE
            out += [rect(x0+j*s, y0+i*s, 40, 40, col, fill, 2, 1.5), text(x0+j*s+20, y0+i*s+25, val, 14, 700, "middle", col)]
    out += [text(455, 425, "lower triangular + positive diagonal", 15, 700),
            text(455, 458, "⇒ det(A)>0 ⇒ strict full rank", 17, 800, fill=RED, cls="math")]

    heading(out, 830, "C", "同样 rank=6，不同有效维数", TEAL)
    spectra = ((145, (1,.95,.9,.85,.8,.75), BLUE, "flat spectrum"),
               (330, (1,.18,.07,.025,.01,.004), RED, "concentrated spectrum"))
    for base, vals, col, lab in spectra:
        out += [text(845, base-65, lab, 15, 750, fill=col), line(845, base+5, 1145, base+5, GRID, 2)]
        for i, v in enumerate(vals):
            out += [rect(855+i*45, base-50*v, 25, 50*v, col, "#F8FAFC", 2, 2)]
    out += [text(845, 440, "state definition: stable rank? entropy rank? threshold?", 13, fill=MUTED)]
    return finish(out, "先写计算对象和 rank 定义，再谈瓶颈；full rank、good conditioning 与高 effective rank 互不等价。")


def failure_evidence():
    out = begin(
        "Attention 失效模式：从症状到干预，再到证据等级",
        "熵低、头可剪、长度外推失败或热力图漂亮都只是观测；机制结论需要对应反例与干预。",
        (RED, AMBER, TEAL),
    )
    heading(out, 42, "A", "五类常见症状", RED)
    symptoms = ((100, "scale", "logits saturate / vanish"), (180, "mask", "leakage / all-masked NaN"),
                (260, "rank", "token uniformity / bottleneck"), (340, "length", "entropy & norm drift"),
                (420, "explain", "weights ≠ faithful attribution"))
    for y, tag, desc in symptoms:
        out += [rect(55, y-28, 86, 38, RED, "#FEE2E2", 6, 2), text(98, y-2, tag, 14, 800, "middle", RED),
                text(155, y-2, desc, 14, 650)]

    heading(out, 430, "B", "诊断—干预成对", AMBER)
    pairs = ((110, "logit std / row entropy", "temp / norm ablation"),
             (210, "head pruning curve", "single + joint pruning"),
             (310, "singular spectrum by layer", "residual / MLP ablation"),
             (410, "counterfactual output", "replace / permute weights"))
    for y, measure, intervention in pairs:
        out += [text(445, y, measure, 13, 750, fill=BLUE), line(610, y-5, 642, y-5, AMBER, 2.5, marker="a2"),
                text(655, y, intervention, 12, 650)]

    heading(out, 830, "C", "I / T / E / H / O 证据阶梯", TEAL)
    levels = ((120, "I", "shape / mask / determinant"), (200, "T", "model + stated assumptions"),
              (280, "E", "versioned experiment"), (360, "H", "mechanism explanation"), (440, "O", "scale / OOD extrapolation"))
    for y, tag, desc in levels:
        col = TEAL if tag in "IT" else AMBER if tag == "E" else RED
        out += [rect(845, y-28, 46, 40, col, "#F8FAFC", 5, 2),
                text(868, y-2, tag, 15, 850, "middle", col), text(910, y-2, desc, 13, 650)]
    return finish(out, "先把症状转成测量，再用最小干预检验机制；不能让实验、猜想或开放外推冒充定理。")


FIGURES = {
    "fig-attention-qkv-content-addressing-v1.svg": qkv_contract,
    "fig-attention-scaled-softmax-ledger-v1.svg": scaled_softmax,
    "fig-attention-mask-visibility-contract-v1.svg": masks_visibility,
    "fig-attention-self-cross-shapes-v1.svg": self_cross_shapes,
    "fig-attention-multihead-budget-v1.svg": multihead_budget,
    "fig-attention-geometry-kernel-probability-v1.svg": geometry_kernel_probability,
    "fig-attention-rank-effective-rank-v1.svg": rank_effective_rank,
    "fig-attention-failure-evidence-v1.svg": failure_evidence,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
