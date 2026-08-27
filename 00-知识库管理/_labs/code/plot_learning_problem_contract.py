#!/usr/bin/env python3
"""Generate the canonical four-panel contract for LT-01—LT-04.

The file uses only the Python standard library so the figure remains easy to
rebuild.  Text is deliberately short; the notes carry the formal derivations.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "00-知识库管理/_assets/figures/learning-theory/fig-learning-problem-contract-v1.svg"


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x: int, y: int, content: str, size: int = 22, color: str = "#1f2937",
         weight: int = 500, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Inter, PingFang SC, '
        f'Noto Sans CJK SC, sans-serif" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{esc(content)}</text>'
    )


def rounded(x: int, y: int, w: int, h: int, fill: str = "#ffffff",
            stroke: str = "#dbe4f0", radius: int = 22, sw: int = 2) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = "#6366f1") -> str:
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="3" '
        f'fill="none" marker-end="url(#arrow)"/>'
    )


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="720" viewBox="0 0 1400 720">',
    '<defs>',
    '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8faff"/><stop offset="1" stop-color="#eef7f4"/></linearGradient>',
    '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#26324d" flood-opacity="0.10"/></filter>',
    '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#6366f1"/></marker>',
    '</defs>',
    '<rect width="1400" height="720" fill="url(#bg)"/>',
    text(70, 70, "统计学习的四层对象合同", 34, "#172554", 750),
    text(70, 108, "先固定世界、数据、算法与评价，再讨论‘学得好’。", 20, "#53627a", 450),
]

cards = [
    ("01", "世界与样本", "P 产生未来对象，也产生训练样本", "#eef2ff", "#4f46e5"),
    ("02", "采样合同", "i.i.d. 是 P^m，不是数据的天然属性", "#ecfeff", "#0891b2"),
    ("03", "学习器与函数", "A 读入 S，输出 h_S ∈ H", "#f0fdf4", "#16a34a"),
    ("04", "损失与风险", "训练量 R_S 不等于目标量 R_P", "#fff7ed", "#ea580c"),
]

for i, (num, title_s, subtitle, tint, accent) in enumerate(cards):
    x = 70 + i * 330
    parts += [
        f'<g filter="url(#shadow)">{rounded(x, 155, 300, 455)}</g>',
        rounded(x + 22, 180, 58, 42, tint, accent, 12, 2),
        text(x + 51, 209, num, 19, accent, 750, "middle"),
        text(x + 96, 211, title_s, 24, "#172554", 700),
        text(x + 24, 252, subtitle, 16, "#64748b", 450),
    ]

# Card 1: P -> S and Z.
parts += [
    rounded(102, 312, 96, 70, "#eef2ff", "#a5b4fc", 16), text(150, 354, "未知 P", 21, "#4338ca", 700, "middle"),
    rounded(238, 288, 96, 60, "#ffffff", "#cbd5e1", 14), text(286, 325, "样本 S", 18, "#334155", 650, "middle"),
    rounded(238, 398, 96, 60, "#ffffff", "#cbd5e1", 14), text(286, 435, "未来 Z", 18, "#334155", 650, "middle"),
    arrow(198, 337, 236, 319), arrow(198, 358, 236, 425),
    text(95, 506, "同一 P：训练与目标相连", 17, "#475569", 550),
    text(95, 540, "若部署变为 Q，问题已改变", 17, "#b45309", 550),
]

# Card 2: independent draws vs duplicates.
for j in range(4):
    cx = 438 + j * 55
    parts += [f'<circle cx="{cx}" cy="326" r="19" fill="#ecfeff" stroke="#22d3ee" stroke-width="2"/>', text(cx, 333, f"Z{j+1}", 13, "#0e7490", 700, "middle")]
parts += [
    text(425, 375, "i.i.d.: 每个箭头重新抽样", 16, "#475569", 550),
    rounded(432, 410, 88, 50, "#fef2f2", "#fca5a5", 12), text(476, 442, "原样本", 16, "#b91c1c", 650, "middle"),
    arrow(520, 422, 570, 402, "#6366f1"), arrow(520, 448, 570, 478, "#6366f1"),
    rounded(572, 380, 95, 46, "#ffffff", "#fecaca", 12), text(620, 409, "增强 1", 15, "#b91c1c", 600, "middle"),
    rounded(572, 460, 95, 46, "#ffffff", "#fecaca", 12), text(620, 489, "增强 2", 15, "#b91c1c", 600, "middle"),
    text(425, 545, "共同来源 ⇒ 条件相关", 17, "#b45309", 650),
]

# Card 3: data -> algorithm -> predictor.
parts += [
    rounded(752, 300, 78, 62, "#ffffff", "#bbf7d0", 14), text(791, 338, "S", 24, "#15803d", 750, "middle"),
    rounded(861, 292, 92, 78, "#f0fdf4", "#86efac", 16), text(907, 327, "算法 A", 18, "#15803d", 700, "middle"), text(907, 351, "+ 随机 U", 13, "#64748b", 500, "middle"),
    rounded(985, 300, 90, 62, "#ffffff", "#bbf7d0", 14), text(1030, 338, "h_S", 22, "#15803d", 750, "middle"),
    arrow(830, 331, 859, 331), arrow(953, 331, 983, 331),
    rounded(785, 414, 250, 70, "#f8fafc", "#cbd5e1", 16), text(910, 444, "参数 θ  ──表示──▶  函数 h", 17, "#334155", 650, "middle"), text(910, 469, "多组 θ 可以是同一个 h", 14, "#64748b", 500, "middle"),
    text(755, 540, "H 限制可输出的函数；A 决定如何选", 16, "#475569", 550),
]

# Card 4: empirical vs population risk.
parts += [
    rounded(1088, 292, 112, 72, "#fff7ed", "#fdba74", 16), text(1144, 323, "训练量", 16, "#c2410c", 650, "middle"), text(1144, 349, "R_S(h)", 21, "#9a3412", 750, "middle"),
    rounded(1240, 292, 112, 72, "#ffffff", "#fdba74", 16), text(1296, 323, "目标量", 16, "#c2410c", 650, "middle"), text(1296, 349, "R_P(h)", 21, "#9a3412", 750, "middle"),
    arrow(1202, 329, 1238, 329),
    text(1090, 405, "gap = R_P(h_S) − R_S(h_S)", 17, "#7c2d12", 650),
    rounded(1090, 446, 258, 78, "#fffaf5", "#fed7aa", 14),
    text(1219, 476, "固定 h：经验均值可无偏", 16, "#475569", 550, "middle"),
    text(1219, 502, "数据选出的 h_S：需泛化理论", 16, "#b45309", 650, "middle"),
    text(1090, 560, "metric、loss、reduction 都要写清", 16, "#475569", 550),
]

parts += [
    '<line x1="70" y1="650" x2="1330" y2="650" stroke="#dbe4f0" stroke-width="2"/>',
    text(70, 687, "对象未固定 → 概率、误差与‘泛化’的量词都无法解释", 18, "#334155", 650),
    text(1330, 687, "LT-01—04 · v1", 15, "#64748b", 500, "end"),
    '</svg>',
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(parts), encoding="utf-8")
print(OUTPUT)
