#!/usr/bin/env python3
"""Generate deterministic NN-53--56 embedding/output advanced textbook figures."""

from __future__ import annotations

from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER, BG, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, circle, finish, heading, line, node, path, rect, text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "neural-networks"


def softmax_bottleneck_rank():
    out = begin(
        "Softmax Bottleneck：跨 context 的 centered log-ratio rank",
        "单个 context 的自由 logits 可覆盖单纯形内部；瓶颈来自多个 contexts 共用低维 hidden-to-vocabulary 线性 head。先消去 row-shift gauge，再比较目标秩与模型秩。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "目标矩阵可能是高秩", BLUE)
    out += [text(60, 100, "P*: diag=.7, off-diag=.1", 16, 700, fill=INK)]
    colors = ((RED, "#FFF5F2"), (BLUE, "#EFF6FF"))
    x0, y0, cell = 92, 142, 52
    for i in range(4):
        out += [text(76, y0 + i * cell + 32, f"c{i+1}", 15, 700, "end", MUTED),
                text(x0 + i * cell + 26, 128, f"w{i+1}", 15, 700, "middle", MUTED)]
        for j in range(4):
            color, fill = colors[0] if i == j else colors[1]
            out += [rect(x0 + j * cell, y0 + i * cell, 46, 42, color, fill, 3, 1.5),
                    text(x0 + j * cell + 23, y0 + i * cell + 27,
                         ".7" if i == j else ".1", 15, 700, "middle", color)]
    out += [rect(52, 382, 310, 92, TEAL, "#ECFDF5", 5, 2),
            text(207, 412, "L*C = log(7) C", 17, 700, "middle", TEAL),
            text(207, 442, "rank = V - 1 = 3", 17, 700, "middle", RED),
            text(207, 466, "row shifts already removed", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "线性 head 的可辨识秩界", TEAL)
    out += [rect(445, 100, 102, 70, BLUE, "#EFF6FF", 5, 2),
            text(496, 128, "H", 19, 700, "middle", BLUE),
            text(496, 154, "N x d", 15, 600, "middle", MUTED),
            rect(592, 100, 102, 70, TEAL, "#ECFDF5", 5, 2),
            text(643, 128, "W^T", 19, 700, "middle", TEAL),
            text(643, 154, "d x V", 15, 600, "middle", MUTED),
            line(552, 135, 585, 135, INK, 2.1, marker="a3"),
            rect(445, 218, 249, 72, AMBER, "#FFFBEB", 5, 2),
            text(569, 248, "Z = H W^T + 1 b^T", 16, 700, "middle", AMBER),
            text(569, 276, "shared across contexts", 15, 600, "middle", MUTED),
            line(569, 297, 569, 335, INK, 2.1, marker="a3"),
            rect(445, 344, 315, 118, TEAL, "#ECFDF5", 5, 2),
            text(602, 374, "L C = Z C", 18, 700, "middle", TEAL),
            text(602, 406, "rank(L C) <= d + 1", 18, 700, "middle", RED),
            text(602, 436, "C removes common logit shift", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "突破方式与证据边界", RED)
    routes = (
        ("increase d", "raise linear rank budget", BLUE),
        ("nonlinear decoder", "change output family", TEAL),
        ("Mixture of Softmaxes", "sum_k pi_k p_k", RED),
    )
    for i, (name, desc, color) in enumerate(routes):
        y = 98 + i * 104
        out += [rect(845, y, 285, 76, color, BG, 5, 2),
                text(987, y + 29, name, 16, 700, "middle", color),
                text(987, y + 57, desc, 15, 600, "middle", MUTED)]
    out += [rect(845, 420, 285, 66, AMBER, "#FFFBEB", 5, 2),
            text(987, 447, "rank diagnostic is necessary", 15, 700, "middle", AMBER),
            text(987, 474, "not a quality guarantee", 15, 600, "middle", MUTED)]
    return finish(out, "瓶颈不是单点 Softmax，而是跨 contexts 的共享低维参数化；先 quotient 掉 row-shift gauge，再比较目标与模型的 centered log-ratio rank。")


def large_vocabulary_methods():
    out = begin(
        "Large-Vocabulary Output：四类计算合同不能混称",
        "Full softmax 保留 flat model 的精确归一化；sampling 近似训练目标或梯度；hierarchy/adaptive 改写概率分解。标量决策数、矩阵维度与 GPU wall time必须分账。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "每个 target 触碰多少候选？", BLUE)
    bars = (
        ("full", 10000, 286, BLUE),
        ("sample K=1000", 1001, 132, AMBER),
        ("balanced tree", 14, 58, TEAL),
    )
    for i, (label, value, width, color) in enumerate(bars):
        y = 112 + i * 104
        out += [text(58, y, label, 16, 700, fill=color),
                rect(58, y + 22, width, 34, color, color, 3, 1),
                text(352, y + 47, str(value), 15, 700, "end", INK)]
    out += [rect(52, 428, 310, 58, RED, "#FFF5F2", 5, 2),
            text(207, 453, "counts are not comparable FLOPs", 15, 700, "middle", RED),
            text(207, 478, "tree branching can underuse GPU", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "hierarchical probability is exact", TEAL)
    coords = {"r": (602, 112), "l": (515, 218), "q": (689, 218),
              "w1": (470, 346), "w2": (560, 346), "w3": (650, 346), "w4": (740, 346)}
    for a, b in (("r", "l"), ("r", "q"), ("l", "w1"), ("l", "w2"), ("q", "w3"), ("q", "w4")):
        x1, y1 = coords[a]; x2, y2 = coords[b]
        out += [line(x1, y1 + 18, x2, y2 - 20, GRID, 2)]
    for key in ("r", "l", "q"):
        x, y = coords[key]
        out += [circle(x, y, 24, TEAL, "#ECFDF5", 2), text(x, y + 6, "σ", 16, 700, "middle", TEAL)]
    for key in ("w1", "w2", "w3", "w4"):
        x, y = coords[key]
        out += [rect(x - 28, y - 20, 56, 40, BLUE, "#EFF6FF", 4, 1.7),
                text(x, y + 6, key, 15, 700, "middle", BLUE)]
    out += [rect(445, 414, 315, 72, TEAL, "#ECFDF5", 5, 2),
            text(602, 443, "P(w3|h) = P(right|h)", 15, 700, "middle", TEAL),
            text(602, 470, "x P(left at child|h)", 15, 650, "middle", INK)]

    heading(out, 830, "C", "adaptive expected-cost ledger", RED)
    out += [rect(845, 94, 285, 78, BLUE, "#EFF6FF", 5, 2),
            text(987, 122, "head: 1000 words + 3 clusters", 15, 700, "middle", BLUE),
            text(987, 151, "always evaluated = 1003", 15, 600, "middle", MUTED)]
    tails = (("tail A", ".08", TEAL), ("tail B", ".02", AMBER))
    for i, (name, prob, color) in enumerate(tails):
        y = 214 + i * 78
        out += [rect(845, y, 285, 54, color, BG, 4, 1.8),
                text(862, y + 33, name, 15, 700, fill=color),
                text(1112, y + 33, f"mass {prob}", 15, 650, "end", MUTED)]
    out += [rect(845, 386, 285, 96, RED, "#FFF5F2", 5, 2),
            text(987, 416, "toy expected labels", 16, 700, "middle", RED),
            text(987, 446, "1003 + .10 x 3000 = 1303", 15, 700, "middle", INK),
            text(987, 470, "tail dimensions may also shrink", 15, 600, "middle", MUTED)]
    return finish(out, "问清楚：近似的是原 flat model、训练 estimator，还是概率模型本身？训练速度、精确 NLL 与部署 top-k 必须分别验收。")


def padding_mask_special_tokens():
    out = begin(
        "Padding、Mask 与 Special Tokens：同一 ID 的四份合同",
        "PAD row、attention edge、loss target 与 decoding stop 属于不同算子；special token 只是离散角色登记，不会自动生成全部 masks。词表变更还必须同步参数、optimizer 与 checkpoint。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "teacher forcing 的错位与有效位", BLUE)
    toks = (("BOS", BLUE), ("a", TEAL), ("EOS", RED), ("PAD", MUTED))
    for i, (tok, color) in enumerate(toks):
        x = 52 + i * 78
        out += [rect(x, 104, 66, 42, color, BG, 4, 1.8), text(x + 33, 131, tok, 15, 700, "middle", color)]
    out += [text(52, 174, "input", 15, 700, fill=MUTED),
            path("M84 155V208", BLUE, 2, "none", None, "a0")]
    targets = (("a", TEAL), ("EOS", RED), ("PAD", MUTED), ("PAD", MUTED))
    for i, (tok, color) in enumerate(targets):
        x = 52 + i * 78
        out += [rect(x, 222, 66, 42, color, BG, 4, 1.8), text(x + 33, 249, tok, 15, 700, "middle", color)]
    out += [text(52, 293, "target", 15, 700, fill=MUTED),
            rect(52, 330, 310, 66, TEAL, "#ECFDF5", 5, 2),
            text(207, 358, "loss mask = [1, 1, 0, 0]", 16, 700, "middle", TEAL),
            text(207, 384, "mean denominator = 2", 15, 600, "middle", MUTED),
            rect(52, 428, 310, 58, AMBER, "#FFFBEB", 5, 2),
            text(207, 453, "EOS is supervised; PAD is not", 15, 700, "middle", AMBER),
            text(207, 478, "unless the task says otherwise", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "attention mask acts on edges", TEAL)
    x0, y0, cell = 470, 126, 58
    allowed = {(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2)}
    for i in range(4):
        out += [text(458, y0 + i * cell + 31, f"q{i}", 15, 700, "end", MUTED),
                text(x0 + i * cell + 25, 112, f"k{i}", 15, 700, "middle", MUTED)]
        for j in range(4):
            ok = (i, j) in allowed
            color = TEAL if ok else RED
            fill = "#ECFDF5" if ok else "#FFF5F2"
            out += [rect(x0 + j * cell, y0 + i * cell, 50, 44, color, fill, 3, 1.4),
                    text(x0 + j * cell + 25, y0 + i * cell + 29, "1" if ok else "x", 15, 700, "middle", color)]
    out += [rect(445, 394, 315, 92, RED, "#FFF5F2", 5, 2),
            text(602, 423, "causal + padding compose", 16, 700, "middle", RED),
            text(602, 451, "all-masked row needs a contract", 15, 650, "middle", INK),
            text(602, 476, "otherwise softmax can be NaN", 15, 600, "middle", MUTED)]

    heading(out, 830, "C", "词表生命周期必须原子更新", RED)
    stages = (("tokenizer", BLUE), ("E / output", TEAL), ("optimizer", AMBER), ("decode", RED))
    for i, (name, color) in enumerate(stages):
        y = 94 + i * 84
        out += [rect(845, y, 285, 54, color, BG, 4, 1.8),
                text(987, y + 33, name, 16, 700, "middle", color)]
        if i < len(stages) - 1:
            out += [line(987, y + 58, 987, y + 80, INK, 1.8, marker="a3")]
    out += [rect(845, 438, 285, 48, AMBER, "#FFFBEB", 4, 1.8),
            text(987, 468, "same integer ID != same role", 15, 700, "middle", AMBER)]
    return finish(out, "PAD row、attention edge、loss ignore 与 generation stop 必须逐一声明；复用 PAD/EOS 要做部署测试。")


def embedding_scale_compression():
    out = begin(
        "Embedding Scale 与 Compression：容量、误差和系统成本三本账",
        "初始化决定 row norm 与 tied logit variance；低秩/自适应维度改变函数类；量化引入可界的重构误差。参数更少不自动等于更低 latency 或更小训练状态。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "初始化先校准两个二阶矩", BLUE)
    out += [rect(52, 98, 310, 86, BLUE, "#EFF6FF", 5, 2),
            text(207, 129, "E ||e_i||^2 = d sigma_E^2", 16, 700, "middle", BLUE),
            text(207, 158, "lookup row scale", 15, 600, "middle", MUTED),
            rect(52, 224, 310, 96, TEAL, "#ECFDF5", 5, 2),
            text(207, 254, "Var(e_i^T h) = d sigma_E^2 q_h", 15, 700, "middle", TEAL),
            text(207, 284, "tied output logit scale", 15, 600, "middle", MUTED),
            rect(52, 362, 310, 108, RED, "#FFF5F2", 5, 2),
            text(207, 392, "one init cannot be judged alone", 16, 700, "middle", RED),
            text(207, 421, "check norm | logit RMS | entropy", 15, 650, "middle", INK),
            text(207, 451, "and padding / positional scaling", 15, 600, "middle", MUTED)]

    heading(out, 430, "B", "low-rank factorization", TEAL)
    out += [rect(445, 104, 90, 250, BLUE, "#EFF6FF", 4, 2),
            text(490, 135, "A", 20, 700, "middle", BLUE),
            text(490, 165, "V x r", 15, 600, "middle", MUTED),
            rect(590, 174, 150, 86, TEAL, "#ECFDF5", 4, 2),
            text(665, 207, "B", 20, 700, "middle", TEAL),
            text(665, 237, "r x d", 15, 600, "middle", MUTED),
            line(540, 218, 583, 218, INK, 2.1, marker="a3"),
            text(602, 389, "E = A B, rank(E) <= r", 17, 700, "middle", RED),
            rect(445, 414, 315, 72, TEAL, "#ECFDF5", 5, 2),
            text(602, 442, "V=50k, d=1024, r=128", 15, 700, "middle", TEAL),
            text(602, 470, "51.2m -> 6.531m parameters", 15, 700, "middle", INK)]

    heading(out, 830, "C", "quantization error", RED)
    out += [rect(845, 96, 285, 80, AMBER, "#FFFBEB", 5, 2),
            text(987, 126, "e_hat = s (q - z0)", 16, 700, "middle", AMBER),
            text(987, 154, "scale and zero-point are metadata", 15, 600, "middle", MUTED),
            rect(845, 216, 285, 88, RED, "#FFF5F2", 5, 2),
            text(987, 246, "||e_hat-e|| <= sqrt(d) s/2", 15, 700, "middle", RED),
            text(987, 276, "|delta logit| <= ||h|| ||error||", 15, 650, "middle", INK),
            rect(845, 344, 285, 84, BLUE, "#EFF6FF", 5, 2),
            text(987, 374, "FP16 table = 102.4 MB", 15, 700, "middle", BLUE),
            text(987, 404, "INT4 raw codes = 25.6 MB", 15, 700, "middle", TEAL),
            text(987, 476, "+ metadata, kernel, master state", 15, 700, "middle", AMBER)]
    return finish(out, "压缩要同时报告秩、重构/logit 误差、训练状态、kernel 与端到端质量；raw code bytes 不是完整收益。")


FIGURES = {
    "fig-softmax-bottleneck-rank-v2.svg": softmax_bottleneck_rank,
    "fig-large-vocabulary-output-methods-v2.svg": large_vocabulary_methods,
    "fig-padding-mask-special-token-contracts-v2.svg": padding_mask_special_tokens,
    "fig-embedding-scale-compression-v2.svg": embedding_scale_compression,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in FIGURES.items():
        target = OUT / filename
        target.write_text(builder(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
