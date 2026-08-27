#!/usr/bin/env python3
"""Generate eight textbook-style SVGs for LM-41--LM-48."""

from __future__ import annotations

import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "figures" / "language-models"
W, H = 1200, 700
BG, PAPER, INK, MUTED, GRID = "#FBF8F1", "#FFFDF8", "#183044", "#667784", "#D9D5CB"
BLUE, TEAL, AMBER, RED, PURPLE, GREEN = "#245AA8", "#17766E", "#C87922", "#B7443E", "#7054A3", "#4F7B45"


def esc(x: object) -> str:
    return html.escape(str(x))


def begin(title: str, desc: str, accent: str = BLUE) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7.5" refY="3.5" orient="auto"><path d="M0,0 L0,7 L8,3.5 z" fill="#667784"/></marker><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#183044" flood-opacity="0.10"/></filter></defs>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>',
        f'<line x1="48" y1="70" x2="1152" y2="70" stroke="{accent}" stroke-width="4"/>',
        f'<text x="52" y="49" font-size="24" font-weight="700" fill="{INK}">{esc(title)}</text>',
    ]


def finish(lines: list[str], footer: str) -> None:
    lines += [
        f'<line x1="48" y1="650" x2="1152" y2="650" stroke="{GRID}" stroke-width="1"/>',
        f'<text x="52" y="674" font-size="13" fill="{MUTED}">{esc(footer)}</text>',
        '</svg>',
    ]


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str, body: str = "",
        color: str = BLUE, fill: str = PAPER, radius: float = 10) -> None:
    lines += [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{color}" stroke-width="1.8" filter="url(#shadow)"/>',
        f'<text x="{x+15}" y="{y+28}" font-size="15" font-weight="700" fill="{color}">{esc(title)}</text>',
    ]
    for i, row in enumerate(body.split("\n")):
        lines.append(f'<text x="{x+15}" y="{y+52+i*20}" font-size="12.5" fill="{MUTED}">{esc(row)}</text>')


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float,
          color: str = MUTED, dash: str = "", width: float = 2.2) -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"{extra}/>')


def label(lines: list[str], x: float, y: float, text: str, color: str = MUTED,
          size: int = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>')


def write(name: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")


def latent_document() -> None:
    lines = begin("RAG：把文档写成潜变量，再逐层审计近似", "语料、检索分布、top-K 截断与条件生成器的概率图。", PURPLE)
    box(lines, 55, 120, 205, 92, "输入 x", "question + time\n+ permissions", BLUE, "#EEF4FC")
    box(lines, 55, 286, 205, 105, "语料快照 C", "documents + versions\n+ ACL + valid time", GREEN, "#EFF6EA")
    box(lines, 355, 170, 250, 180, "检索分布 pη(z|x,C)", "z₁  0.48\nz₂  0.31\nz₃  0.14\nother  0.07", PURPLE, "#F3EFFA")
    arrow(lines, 260, 166, 355, 215, BLUE)
    arrow(lines, 260, 338, 355, 300, GREEN)
    box(lines, 700, 110, 190, 88, "z₁ · 0.48", "policy page · v7", TEAL)
    box(lines, 700, 235, 190, 88, "z₂ · 0.31", "release note · v3", AMBER)
    box(lines, 700, 360, 190, 88, "z₃ · 0.14", "FAQ · old", RED)
    arrow(lines, 605, 220, 700, 154, PURPLE)
    arrow(lines, 605, 255, 700, 279, PURPLE)
    arrow(lines, 605, 290, 700, 404, PURPLE)
    lines += [f'<path d="M610 325 C650 500,760 510,890 485" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="7 5"/>']
    label(lines, 655, 505, "top-K 截断：other 被丢弃并重新归一化", RED, 12)
    box(lines, 965, 200, 180, 170, "生成器 pθ(y|x,z)", "evidence-conditioned\n+ parametric prior\n→ answer y", TEAL, "#EAF7F4")
    for y in (154, 279, 404):
        arrow(lines, 890, y, 965, 260, MUTED)
    lines += [f'<path d="M160 120 C380 75,820 65,1040 190" fill="none" stroke="{AMBER}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#arrow)"/>']
    label(lines, 590, 95, "虚线：参数记忆可绕过当前证据 → 答对不证明检索正确", AMBER, 13, "middle", 600)
    box(lines, 85, 515, 1030, 96, "四个条件事件", "corpus answerable  →  retrieved  →  retained in context  →  generated + attributed correctly", RED, "#FFF0ED")
    finish(lines, "候选内 softmax 只是截断近似；retriever score 未经校准时不能称为真实相关概率。")
    write("fig-lm-rag-latent-document-v1.svg", lines)


def data_lineage() -> None:
    lines = begin("从原始字节到向量条目：正向构建、反向追溯", "文档解析、span、chunk、embedding 和 index 的可逆数据血缘。", GREEN)
    stages = [
        (65, 115, 185, 105, "原始文件", "doc-id D17\nhash · license · ACL", GREEN, "#EFF6EA"),
        (285, 115, 185, 105, "规范文本", "parser v4\nUTF-8 · pages · tables", BLUE, "#EEF4FC"),
        (505, 115, 185, 105, "可引用 span", "[a,b) offsets\nsection · page · time", AMBER, "#FFF5E7"),
        (725, 115, 185, 105, "检索 chunk", "C17-04\nparent · overlap · ACL", PURPLE, "#F3EFFA"),
        (945, 115, 185, 105, "向量与索引", "encoder hash · dim\ndistance · index build", TEAL, "#EAF7F4"),
    ]
    for item in stages:
        box(lines, *item)
    for x in (250, 470, 690, 910):
        arrow(lines, x, 167, x+35, 167)
    label(lines, 65, 273, "反向追溯：citation → vector-id → chunk-id → span → original bytes", INK, 15, "start", 700)
    for x1, x2 in ((1037, 817), (817, 597), (597, 377), (377, 157)):
        arrow(lines, x1, 300, x2, 300, RED, "6 4")
    tests = [
        ("边界覆盖", "gold span 是否被任一 chunk 完整覆盖？", BLUE),
        ("距离合同", "normalized? cosine / dot / L2 是否一致？", PURPLE),
        ("权限传播", "pre-filter / post-filter；cache 是否二次验证？", RED),
        ("删除传播", "doc → chunks → vectors → replicas → cache", GREEN),
    ]
    for i, (t, b, c) in enumerate(tests):
        x = 65 + i * 270
        box(lines, x, 350, 240, 105, t, b, c)
    box(lines, 65, 500, 1055, 108, "版本闭包", "index-version  ↦  corpus snapshot + parser + chunker + metadata schema + encoder/tokenizer + dtype/quantization + ANN parameters", RED, "#FFF0ED")
    finish(lines, "完整 manifest 不保证检索有效；它保证对象可识别、更新可传播、引用可定位、错误可复现。")
    write("fig-lm-rag-data-lineage-v1.svg", lines)


def ranking_fusion() -> None:
    lines = begin("BM25、Dense 与 RRF：先理解分数，再做融合", "词频饱和曲线、双编码器相似度与名次融合算例。", AMBER)
    x0, y0, ww, hh = 70, 345, 330, 220
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}" stroke-width="1.7"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}" stroke-width="1.7"/>']
    pts = []
    for i in range(11):
        tf = i
        val = 2.2 * tf / (tf + 1.6) if tf else 0
        pts.append((x0 + i * ww / 10, y0 - val / 2.2 * hh))
    lines.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{AMBER}" stroke-width="4"/>')
    for x, y in pts[::2]:
        lines.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{AMBER}"/>')
    label(lines, 72, 105, "① BM25：词频收益递减", INK, 17, "start", 700)
    label(lines, 205, 376, "term frequency", MUTED, 12, "middle")
    label(lines, 47, 215, "weight", MUTED, 12, "middle")
    box(lines, 455, 115, 265, 225, "② Dense dual encoder", "query q → [0.8, 0.1]\n\nD₁ → [0.7, 0.2]  dot .58\nD₂ → [0.2, 0.9]  dot .25\n\n向量可预计算；分数非概率", BLUE, "#EEF4FC")
    box(lines, 775, 105, 355, 252, "③ RRF 只融合名次", "             BM25   dense\nDoc A          1       10\nDoc B          3        3\n\nA: 1/61 + 1/70 = .03068\nB: 1/63 + 1/63 = .03175\n\n→ B 稳定靠前，融合后排第一", PURPLE, "#F3EFFA")
    box(lines, 455, 405, 675, 150, "候选集合先决定上界", "BM25 top-K = B    Dense top-K = D\nUnion oracle = gold ∈ (B ∪ D) ?\n再比较 raw-score calibration / learned fusion / RRF；验证集选参数，测试集只评一次。", RED, "#FFF0ED")
    finish(lines, "BM25 与 dense 使用不同归纳偏置；hybrid 的互补性是待测假设，不是系统名称带来的保证。")
    write("fig-lm-rag-ranking-fusion-v1.svg", lines)


def ann_funnel() -> None:
    lines = begin("两阶段检索是一条不可逆漏斗", "exact oracle、ANN、candidate set、reranker 与 context 的保真和延迟。", TEAL)
    funnels = [
        (85, 115, 970, 82, "Exact vector ranking · N = 1,000,000", "gold rank = 37", BLUE),
        (155, 220, 830, 82, "ANN candidates · K₁ = 200", "ANN recall@200 = .96 · gold kept", TEAL),
        (245, 325, 650, 82, "Cross / late-interaction rerank · K₂ = 20", "gold rank → 4", PURPLE),
        (355, 430, 430, 82, "Context selection · 6 passages", "gold retained", AMBER),
    ]
    for x, y, w, h, t, b, c in funnels:
        lines += [f'<path d="M{x},{y} L{x+w},{y} L{x+w-38},{y+h} L{x+38},{y+h} Z" fill="{PAPER}" stroke="{c}" stroke-width="2" filter="url(#shadow)"/>']
        label(lines, x+w/2, y+31, t, c, 15, "middle", 700)
        label(lines, x+w/2, y+57, b, MUTED, 12.5, "middle")
    label(lines, 1085, 138, "不可恢复点", RED, 14, "middle", 700)
    lines += [f'<path d="M1080 160 L1080 485" stroke="{RED}" stroke-width="2" stroke-dasharray="5 5"/>']
    label(lines, 1085, 520, "一旦 gold 被丢弃，\n重排器无法创造证据", RED, 12, "middle")
    parts = [("encode", .15, BLUE), ("ANN", .20, TEAL), ("fetch", .10, GREEN), ("rerank", .32, PURPLE), ("generate", .23, AMBER)]
    x = 85
    label(lines, 85, 570, "端到端 p95 延迟分解", INK, 14, "start", 700)
    for name, frac, color in parts:
        width = 900 * frac
        lines += [f'<rect x="{x}" y="588" width="{width}" height="34" fill="{color}"/>']
        label(lines, x + width/2, 611, name, "#FFFFFF", 11, "middle", 700)
        x += width
    finish(lines, "分开报告 ANN 对 exact top-K 的保真、任务 evidence recall、rerank 增益与 p50/p95/p99。")
    write("fig-lm-rag-ann-rerank-funnel-v1.svg", lines)


def negative_geometry() -> None:
    lines = begin("困难负样本：梯度更强，也更接近标注边界", "InfoNCE 下不同负样本与 false negative 的二维教学投影。", RED)
    cx, cy = 410, 335
    for r in (85, 165, 245):
        lines.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="1.3" stroke-dasharray="4 5"/>')
    lines += [f'<circle cx="{cx}" cy="{cy}" r="15" fill="{BLUE}"/>']
    label(lines, cx+22, cy+5, "query q", BLUE, 14, "start", 700)
    points = [
        (350, 275, GREEN, "positive d⁺", "plus"),
        (610, 500, MUTED, "random negative", "dot"),
        (265, 485, AMBER, "BM25 hard negative", "triangle"),
        (520, 245, RED, "model-mined negative", "triangle"),
        (455, 380, PURPLE, "unlabeled alternative evidence", "ring"),
    ]
    for x, y, c, txt, shape in points:
        if shape == "triangle":
            lines.append(f'<path d="M{x},{y-10} L{x-10},{y+9} L{x+10},{y+9} Z" fill="{c}"/>')
        elif shape == "ring":
            lines += [f'<circle cx="{x}" cy="{y}" r="13" fill="{PAPER}" stroke="{c}" stroke-width="4"/>',
                      f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>']
        else:
            lines.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}"/>')
        label(lines, x+16, y+5, txt, c, 12)
    box(lines, 755, 115, 365, 160, "Softmax 梯度", "∂L/∂s(d) = [π(d|q) − 1{d=d⁺}] / τ\n\n高分负例 π 大 → 下推更强\n温度小 → 梯度更尖锐", BLUE, "#EEF4FC")
    box(lines, 755, 315, 365, 125, "False-negative audit", "相关但不支持？替代证据？\n时间/权限错位？parent/chunk 粒度错？", RED, "#FFF0ED")
    box(lines, 755, 480, 365, 125, "Index lag", "miner uses encoder η(t−Δ)\nΔ 过大：负样本分布陈旧\n刷新更快：计算与通信成本上升", PURPLE, "#F3EFFA")
    finish(lines, "二维距离仅用于解释采样；是否蕴含答案必须回到原文、时点、权限和标注协议。")
    write("fig-lm-rag-negative-geometry-v1.svg", lines)


def claim_citation() -> None:
    lines = begin("Context 不是一堆卡片：每个命题都要落到支持 span", "候选去重、预算编排、冲突呈现与 claim-level citation。", BLUE)
    label(lines, 70, 108, "SOURCE CARDS", MUTED, 11, "start", 700)
    cards = [
        (70, 130, "A · policy v7", "effective 2026-08\n… rate is 4.2% …", GREEN),
        (70, 245, "B · old FAQ", "effective 2024-01\n… rate is 3.8% …", RED),
        (70, 360, "C · news copy", "copies B; no new evidence", AMBER),
    ]
    for x, y, t, b, c in cards:
        box(lines, x, y, 260, 90, t, b, c)
    arrow(lines, 340, 175, 445, 175, GREEN)
    arrow(lines, 340, 290, 445, 290, RED)
    arrow(lines, 340, 405, 445, 405, AMBER)
    label(lines, 465, 108, "CONTEXT LAYOUT · 420 tokens", MUTED, 11, "start", 700)
    lines += [f'<rect x="445" y="130" width="320" height="365" rx="5" fill="{PAPER}" stroke="{GRID}" stroke-width="1.5"/>']
    label(lines, 465, 163, "[A §2 · current]", GREEN, 12, "start", 700)
    label(lines, 465, 190, "The current official rate is 4.2%.", INK, 13)
    lines += [f'<rect x="462" y="202" width="278" height="4" fill="{GREEN}"/>']
    label(lines, 465, 250, "[B §1 · historical]", RED, 12, "start", 700)
    label(lines, 465, 277, "The earlier FAQ reported 3.8%.", INK, 13)
    lines += [f'<rect x="462" y="289" width="265" height="4" fill="{RED}"/>']
    label(lines, 465, 345, "C removed: duplicate of B", AMBER, 12)
    label(lines, 465, 405, "Budget ledger", MUTED, 12, "start", 700)
    label(lines, 465, 432, "A 160 · B 140 · instructions 70 · answer 50", INK, 12)
    label(lines, 850, 108, "ANSWER + CITATIONS", MUTED, 11, "start", 700)
    box(lines, 830, 135, 315, 100, "Claim 1 · current value", "The rate is 4.2%.  [A §2]\n✓ precise span entails claim", GREEN, "#EFF6EA")
    box(lines, 830, 265, 315, 115, "Claim 2 · historical contrast", "It was previously 3.8%.  [B §1]\n✓ time-scoped; conflict preserved", BLUE, "#EEF4FC")
    box(lines, 830, 410, 315, 100, "Bad citation pattern", "The policy is universally best. [A]\n✗ related page does not entail claim", RED, "#FFF0ED")
    lines += [f'<path d="M740 202 C790 190,790 185,830 185" fill="none" stroke="{GREEN}" stroke-width="2.5" marker-end="url(#arrow)"/>',
              f'<path d="M727 289 C790 300,790 320,830 320" fill="none" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#arrow)"/>']
    box(lines, 70, 540, 1075, 75, "四问审计", "citation exists?  ·  cited span relevant?  ·  span entails exact claim?  ·  source valid and authoritative at query time?", PURPLE, "#F3EFFA")
    finish(lines, "相关性、支持性、世界事实、正确归因与因果 faithfulness 是五个不同事件。")
    write("fig-lm-rag-claim-citation-layout-v1.svg", lines)


def iterative_machine() -> None:
    lines = begin("多跳检索：状态—动作—观察—验证—停止", "带预算、循环检测与 provenance 的序贯决策。", PURPLE)
    nodes = [
        (190, 175, "S₀", "question\nbudget 3", BLUE),
        (480, 130, "A₀", "retrieve\nLost Gravity", PURPLE),
        (770, 175, "O₁", "Mack Rides\nsource span", GREEN),
        (850, 405, "S₁", "new entity\nbudget 2", BLUE),
        (575, 535, "A₁", "retrieve\nMack Rides country", PURPLE),
        (285, 470, "O₂", "Germany\nsource span", GREEN),
    ]
    for x, y, title, body, color in nodes:
        lines += [f'<circle cx="{x}" cy="{y}" r="58" fill="{PAPER}" stroke="{color}" stroke-width="3" filter="url(#shadow)"/>']
        label(lines, x, y-8, title, color, 17, "middle", 700)
        for j, row in enumerate(body.split("\n")):
            label(lines, x, y+15+j*17, row, MUTED, 11, "middle")
    curved = [
        "M248 160 C320 110,390 105,422 125",
        "M538 135 C620 115,695 130,714 158",
        "M805 225 C860 270,880 320,865 347",
        "M800 443 C730 505,660 530,633 533",
        "M517 537 C430 545,350 520,329 505",
        "M255 420 C190 360,160 270,177 232",
    ]
    colors = [PURPLE, GREEN, BLUE, PURPLE, GREEN, AMBER]
    for d, c in zip(curved, colors):
        lines.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3" marker-end="url(#arrow)"/>')
    box(lines, 470, 275, 265, 135, "Verifier / stop", "both supporting spans found?\ncontradiction checked?\nbudget left?\n→ answer / retrieve / abstain", RED, "#FFF0ED")
    arrow(lines, 735, 335, 790, 365, RED)
    lines += [f'<path d="M470 335 C390 335,350 320,300 260" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arrow)"/>']
    label(lines, 338, 315, "duplicate/query drift → rollback", RED, 11, "middle")
    box(lines, 885, 525, 255, 95, "Call ledger", "query · filters · IDs · scores\nlatency · state before/after", TEAL, "#EAF7F4")
    finish(lines, "可见 reasoning 可生成下一查询，但不能替代 evidence graph；每次工具调用都必须有状态与来源日志。")
    write("fig-lm-rag-iterative-state-machine-v1.svg", lines)


def evaluation_cube() -> None:
    lines = begin("RAG 评估立方体：取回、答对、归因必须联合观察", "三轴事件、故障树投影与成本向量。", RED)
    ox, oy, s, dx, dy = 160, 455, 170, 75, -65
    cubes = []
    for r in (0, 1):
        for g in (0, 1):
            for a in (0, 1):
                x = ox + g*s + a*dx
                y = oy - r*s + a*dy
                good = r and g and a
                color = GREEN if good else BLUE if (r+g+a)==2 else AMBER if (r+g+a)==1 else RED
                opacity = .85 if good else .22 + .12*(r+g+a)
                cubes.append((x,y,r,g,a,color,opacity))
    for x,y,r,g,a,color,opacity in cubes:
        lines += [f'<rect x="{x}" y="{y}" width="58" height="58" fill="{color}" fill-opacity="{opacity}" stroke="{color}" stroke-width="1.2"/>']
        label(lines, x+29, y+35, f"{r}{g}{a}", "#FFFFFF" if opacity>.55 else INK, 12, "middle", 700)
    arrow(lines, ox-25, oy+70, ox+s+70, oy+70, BLUE)
    label(lines, ox+s/2+20, oy+96, "Generation G", BLUE, 13, "middle", 700)
    arrow(lines, ox-25, oy+60, ox-25, oy-s-25, TEAL)
    label(lines, ox-50, oy-s/2, "Retrieval R", TEAL, 13, "middle", 700)
    arrow(lines, ox+s+80, oy+50, ox+s+80+dx, oy+50+dy, PURPLE)
    label(lines, ox+s+135, oy-10, "Attribution A", PURPLE, 13, "middle", 700)
    label(lines, 155, 120, "cell 111 = joint success; 011/101/110 reveal different compensations", INK, 13, "start", 700)
    box(lines, 610, 105, 505, 300, "最早失败层", "1  corpus answerable?\n2  chunk covers evidence?\n3  exact retriever ranks it?\n4  ANN preserves exact candidate?\n5  fusion / reranker keeps it?\n6  context retains + positions it?\n7  generator uses / abstains?\n8  citation links claim → span?", RED, "#FFF0ED")
    bars = [("index", .65, BLUE), ("p95 latency", .82, TEAL), ("retrieved tokens", .48, AMBER), ("generator cost", .72, PURPLE)]
    label(lines, 610, 450, "成本向量：质量曲线必须在同预算比较", INK, 14, "start", 700)
    for i,(name,val,color) in enumerate(bars):
        y=480+i*38
        label(lines, 610, y+15, name, MUTED, 11)
        lines += [f'<rect x="735" y="{y}" width="340" height="20" rx="4" fill="#EAE6DD"/>',
                  f'<rect x="735" y="{y}" width="{340*val}" height="20" rx="4" fill="{color}"/>']
    finish(lines, "三个边缘平均数不能决定联合成功率；oracle 干预与配对分析比单一端到端分数更可诊断。")
    write("fig-lm-rag-evaluation-cube-v1.svg", lines)


def main() -> None:
    latent_document()
    data_lineage()
    ranking_fusion()
    ann_funnel()
    negative_geometry()
    claim_citation()
    iterative_machine()
    evaluation_cube()


if __name__ == "__main__":
    main()
