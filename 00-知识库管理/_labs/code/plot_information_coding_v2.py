#!/usr/bin/env python3
"""Generate v2 textbook figures for coding, ELBO, and rate/IB/MDL notes."""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG,
    BLUE,
    GRID,
    INK,
    MUTED,
    RED,
    TEAL,
    begin,
    circle,
    finish,
    heading,
    line,
    node,
    path,
    rect,
    text,
)


OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "information-theory"


def polyline(points, color, width=2.5, dash=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, color, width, "none", dash)


def lossless_aep():
    out = begin(
        "前缀编码、典型集与无损压缩阈值",
        "前缀树保证即时可译；AEP 使每符号 surprise 集中在 entropy 附近；典型集大小约为 2^(nH)，从而形成 fixed-length almost-lossless coding 的 H 阈值。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Prefix-free：叶子即时可译", BLUE)
    out += [circle(190, 105, 9, INK, INK), line(185, 115, 120, 205, BLUE, 2.5), line(195, 115, 270, 205, BLUE, 2.5)]
    out += [circle(120, 215, 9, RED, BG, 2.5), circle(270, 215, 9, INK, INK, 2.5)]
    out += [line(265, 225, 225, 315, TEAL, 2.5), line(275, 225, 325, 315, TEAL, 2.5)]
    out += [circle(225, 325, 9, TEAL, BG, 2.5), circle(325, 325, 9, TEAL, BG, 2.5)]
    out += [
        text(145, 155, "0", 15, 700, "middle", BLUE),
        text(235, 155, "1", 15, 700, "middle", BLUE),
        text(238, 270, "0", 15, 700, "middle", TEAL),
        text(305, 270, "1", 15, 700, "middle", TEAL),
        text(120, 247, "a: 0", 15, 700, "middle"),
        text(225, 357, "b: 10", 15, 700, "middle"),
        text(325, 357, "c: 11", 15, 700, "middle"),
        text(45, 420, "prefix-free => uniquely decodable", 16, 650),
        text(45, 458, "Kraft / McMillan 控制可用叶子容量。", 15, fill=MUTED),
        text(45, 492, "nonsingular 不自动保证 concatenation 唯一。", 15, fill=RED),
    ]

    heading(out, 430, "B", "AEP：每符号 surprise 集中", TEAL)
    out += [line(440, 385, 770, 385, GRID, 2), line(460, 410, 460, 95, GRID, 2)]
    curves = ((70, 115, BLUE), (38, 190, TEAL), (20, 245, RED))
    for scale, height, color in curves:
        pts = []
        for i in range(121):
            x = 460 + 2.45 * i
            y = 385 - height * math.exp(-0.5 * ((x - 620) / scale) ** 2)
            pts.append((x, y))
        out.append(polyline(pts, color, 2.5))
    out += [line(620, 100, 620, 385, INK, 2, "7 5"), text(620, 88, "H(X)", 16, 700, "middle")]
    out += [
        text(705, 190, "n grows", 15, 700, fill=RED),
        text(430, 430, "-(1/n) log p(X^n) -> H(X)", 17, 650, cls="math"),
        text(430, 470, "约 2^(nH) 个序列，各自概率约 2^(-nH)。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "Rate H 是 fixed-length 一阶阈值", RED)
    out += [line(850, 300, 1140, 300, GRID, 3), line(990, 240, 990, 350, RED, 3), text(990, 222, "H", 18, 700, "middle", RED)]
    out += [
        text(900, 280, "R < H", 17, 700, "middle", BLUE),
        text(1070, 280, "R > H", 17, 700, "middle", TEAL),
        text(830, 380, "codewords: 2^(nR)", 17, 650, cls="math"),
        text(830, 417, "typical sequences: about 2^(nH)", 16, 650, cls="math"),
        text(830, 455, "R>H：可覆盖典型集，error -> 0", 15, fill=TEAL),
        text(830, 490, "R<H：容量指数级不足（converse）。", 15, fill=RED),
    ]
    return finish(out, "单符号前缀码解决可译性；AEP 与典型集才给出长 block almost-lossless 压缩的 entropy 阈值。")


def elbo_identity():
    out = begin(
        "变分对象、ELBO 证据分解与误差来源",
        "生成模型定义 joint、evidence 与 model posterior；q 是人为选择的近似；log evidence 精确分解为 ELBO 加 reverse-KL gap，训练误差还需区分 family、amortization、optimization 与 Monte Carlo。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Posterior 与 q 是不同对象", BLUE)
    node(out, 55, 100, 110, 52, "prior p(z)", BLUE, size=16)
    node(out, 240, 100, 120, 52, "p(x|z)", TEAL, size=16)
    out += [line(168, 126, 235, 126, INK, 2.5, marker="a3")]
    node(out, 55, 220, 305, 58, "joint p(x,z) = p(z)p(x|z)", TEAL, size=16)
    out += [line(205, 156, 205, 214, INK, 2.3, marker="a3")]
    node(out, 55, 340, 138, 56, "posterior p(z|x)", RED, size=15)
    node(out, 222, 340, 138, 56, "approx q_phi(z|x)", BLUE, size=15)
    out += [
        text(45, 440, "evidence p(x)=integral p(x,z) dz", 16, 650, cls="math"),
        text(45, 480, "q 由 inference design 定义，不是 posterior 别名。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "Evidence = ELBO + KL gap", TEAL)
    out += [rect(450, 145, 190, 78, TEAL, BG, 5, 2), rect(640, 145, 115, 78, RED, BG, 5, 2)]
    out += [
        text(545, 190, "ELBO(q)", 20, 700, "middle", TEAL),
        text(698, 181, "KL(q ||", 16, 700, "middle", RED),
        text(698, 207, "p(z|x))", 16, 700, "middle", RED),
        text(600, 275, "log p_theta(x) = ELBO + KL gap", 17, 700, "middle", cls="math"),
        text(430, 330, "ELBO = E_q[log p(x,z) - log q(z)]", 16, 650, cls="math"),
        text(430, 375, "= E_q log p(x|z) - KL(q||p(z))", 16, 650, cls="math"),
        text(430, 425, "gap=0 iff q = model posterior a.e.", 15, fill=TEAL),
        text(430, 470, "support failure 可让 ELBO/KL 失去有限值。", 15, fill=RED),
    ]

    heading(out, 830, "C", "“Gap”要按来源拆开", RED)
    items = (
        ("family gap", "近似族表示不了 posterior", BLUE),
        ("amortization gap", "shared encoder 不达 per-x optimum", TEAL),
        ("optimization gap", "参数化目标尚未优化到位", RED),
        ("Monte Carlo error", "objective / gradient 随机估计", BLUE),
    )
    for i, (label, desc, color) in enumerate(items):
        y = 100 + i * 84
        text_y = y + 18
        out += [circle(842, text_y - 5, 5, color, color), text(857, text_y, label, 16, 700, fill=color), text(857, text_y + 30, desc, 15, 650)]
    out += [
        line(835, 445, 1135, 445, GRID, 2),
        text(830, 480, "另有 model misspecification 与 evaluation gap。", 15, fill=MUTED),
    ]
    return finish(out, "ELBO 是精确证据分解中的下界项；近似、摊销、优化与随机估计误差必须分别诊断。")


def rate_ib_mdl():
    out = begin(
        "率失真、信息瓶颈与最小描述长度的对象分层",
        "Rate-distortion 优化重建率与 distortion；information bottleneck 压缩输入信息并保留任务信息；MDL 比较可译码协议下模型与数据的总描述长度。",
        (BLUE, TEAL, RED),
    )
    heading(out, 42, "A", "Rate-distortion：重建保真率", BLUE)
    node(out, 45, 105, 70, 50, "X^n", BLUE)
    node(out, 155, 105, 70, 50, "M", TEAL)
    node(out, 265, 105, 90, 50, "Xhat^n", RED)
    out += [line(118, 130, 150, 130, INK, 2.4, marker="a3"), line(228, 130, 260, 130, INK, 2.4, marker="a3")]
    out += [text(190, 190, "rate R", 15, 700, "middle", TEAL), text(310, 190, "distortion D", 15, 700, "middle", RED)]
    out += [line(55, 390, 355, 390, GRID, 2), line(75, 415, 75, 235, GRID, 2)]
    pts = []
    for i in range(121):
        d = i / 120
        x = 75 + 260 * d
        y = 390 - 145 * max(0.0, 1 - math.sqrt(d))
        pts.append((x, y))
    out.append(polyline(pts, BLUE, 3))
    out += [text(70, 225, "R(D)", 16, 700, fill=BLUE), text(330, 420, "D", 15, 650), text(45, 470, "distortion function 是问题定义，不是自然常数。", 15, fill=MUTED)]

    heading(out, 430, "B", "IB：任务相关压缩", TEAL)
    node(out, 445, 105, 70, 50, "X", BLUE)
    node(out, 590, 105, 70, 50, "Z", TEAL)
    node(out, 700, 235, 70, 50, "Y", RED)
    out += [line(518, 130, 585, 130, INK, 2.4, marker="a3"), line(735, 230, 660, 157, RED, 2.4, marker="a2")]
    out += [
        text(550, 100, "compress", 15, 650, "middle", BLUE),
        text(690, 180, "relevance", 15, 650, "middle", RED),
        text(430, 330, "min I(X;Z) - beta I(Z;Y)", 17, 700, cls="math"),
        text(430, 375, "Markov structure: Y - X - Z", 16, 650, cls="math"),
        text(430, 420, "保留 task 信息 != 保留全部输入。", 16, 650),
        text(430, 465, "variational bounds 改变可优化 surrogate。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "MDL：完整可译码协议", RED)
    out += [rect(850, 110, 270, 62, BLUE, BG, 4, 2), rect(850, 172, 270, 76, TEAL, BG, 4, 2), rect(850, 248, 270, 92, RED, BG, 4, 2)]
    out += [
        text(985, 147, "protocol / model class", 16, 700, "middle", BLUE),
        text(985, 216, "model / parameter description", 16, 700, "middle", TEAL),
        text(985, 298, "data given model", 17, 700, "middle", RED),
        text(830, 390, "L_total = L(protocol,model) + L(data|model)", 15, 650, cls="math"),
        text(830, 430, "two-part / mixture / NML / prequential 不同。", 15, 650),
        text(830, 470, "短描述不自动证明 causal truth 或泛化。", 15, fill=MUTED),
    ]
    return finish(out, "三种目标都出现 rate/complexity 权衡，但随机对象、保真目标与可译码协议完全不同。")


FIGURES = {
    "fig-lossless-coding-aep-v2.svg": lossless_aep,
    "fig-elbo-evidence-gap-v2.svg": elbo_identity,
    "fig-rate-distortion-ib-mdl-v2.svg": rate_ib_mdl,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        target = OUT / name
        target.write_text(build(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
