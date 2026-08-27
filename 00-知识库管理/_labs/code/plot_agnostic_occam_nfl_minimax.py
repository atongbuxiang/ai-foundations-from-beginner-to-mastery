#!/usr/bin/env python3
"""Generate the canonical LT-13—LT-16 agnostic/Occam/NFL/minimax visual."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "00-知识库管理/_assets/figures/learning-theory/fig-agnostic-occam-nfl-minimax-v1.svg"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tx(x, y, s, size=20, color="#1f2937", weight=500, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Inter, PingFang SC, Noto Sans CJK SC, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'


def rect(x, y, w, h, fill="#fff", stroke="#dbe4f0", r=18, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1, y1, x2, y2, color="#6366f1", dash=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#arr)"{ds}/>'


p = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="720" viewBox="0 0 1400 720">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8faff"/><stop offset="1" stop-color="#eef7f4"/></linearGradient><filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#26324d" flood-opacity="0.10"/></filter><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#6366f1"/></marker></defs>',
    '<rect width="1400" height="720" fill="url(#bg)"/>',
    tx(70, 70, "从不可知上界到学习的不可能性边界", 34, "#172554", 750),
    tx(70, 108, "估计非零风险 → 按描述分配复杂度 → 暴露归纳偏置 → 用检验证明下界。", 20, "#53627a", 450),
]

meta = [
    ("13", "不可知 ERM", "双侧估计非零 risk，付出 1/ε²", "#eef2ff", "#4f46e5"),
    ("14", "Occam / 编码", "给短假设更大的先验失败预算", "#ecfeff", "#0891b2"),
    ("15", "No-Free-Lunch", "未见点的标签仍像公平硬币", "#fff7ed", "#ea580c"),
    ("16", "Minimax 下界", "把学习困难归约为统计检验困难", "#f0fdf4", "#16a34a"),
]
for i, (num, title, sub, tint, accent) in enumerate(meta):
    x = 70 + i * 330
    p += [
        f'<g filter="url(#shadow)">{rect(x,155,300,455)}</g>',
        rect(x + 22, 180, 58, 42, tint, accent, 12),
        tx(x + 51, 209, num, 19, accent, 750, "middle"),
        tx(x + 96, 211, title, 23, "#172554", 700),
        tx(x + 24, 252, sub, 15, "#64748b", 450),
    ]

# 13: empirical/population bridge with two deviations.
p += [
    rect(96, 300, 98, 58, "#eef2ff", "#a5b4fc", 13),
    tx(145, 325, "ERM 输出", 14, "#4338ca", 700, "middle"),
    tx(145, 347, "h_S", 17, "#4338ca", 750, "middle"),
    arrow(196, 329, 238, 329),
    rect(242, 300, 104, 58, "#fff", "#a5b4fc", 13),
    tx(294, 325, "类内 oracle", 13, "#4338ca", 650, "middle"),
    tx(294, 347, "h*", 17, "#4338ca", 750, "middle"),
    tx(94, 413, "excess ≤ 2 sup_h |R_S−R_P|", 14, "#475569", 650),
    tx(94, 454, "≤ 2 √[ log(2M/δ) / (2m) ]", 15, "#4338ca", 700),
    tx(94, 506, "m ≥ 2 log(2M/δ) / ε²", 15, "#312e81", 750),
    tx(94, 550, "噪声下不能要求 zero training error", 13, "#b45309", 650),
]

# 14: weighted hypotheses and Kraft budget.
weights = [("h₁", "π=.50", 303), ("h₂", "π=.25", 369), ("h₃", "π=.125", 435)]
for name, weight, y in weights:
    p += [
        rect(430, y, 72, 46, "#ecfeff", "#67e8f9", 11),
        tx(466, y + 29, name, 15, "#0e7490", 700, "middle"),
        rect(514, y, 86, 46, "#fff", "#a5f3fc", 11),
        tx(557, y + 29, weight, 13, "#0e7490", 650, "middle"),
        arrow(603, y + 23, 642, y + 23),
        tx(654, y + 29, "δπ", 14, "#0e7490", 700),
    ]
p += [
    tx(426, 516, "Σ_h π(h) ≤ 1", 15, "#0e7490", 700),
    tx(426, 548, "penalty ≈ √[log 1/π(h) / m]", 14, "#475569", 650),
    tx(426, 578, "prefix-free: π(h)=2^(−L(h))", 13, "#0f766e", 650),
]

# 15: seen/unseen points.
for j in range(8):
    cx = 762 + (j % 4) * 58
    cy = 307 + (j // 4) * 76
    seen = j < 4
    p += [
        f'<circle cx="{cx}" cy="{cy}" r="19" fill="{"#ffedd5" if seen else "#fff"}" stroke="{"#fb923c" if seen else "#cbd5e1"}" stroke-width="2"/>',
        tx(cx, cy + 6, "✓" if seen else "?", 17, "#c2410c" if seen else "#64748b", 750, "middle"),
    ]
p += [
    tx(756, 455, "m seen", 14, "#c2410c", 700),
    tx(888, 455, "≥ m unseen", 14, "#64748b", 700),
    tx(756, 501, "average unseen error ≥ 1/2", 14, "#9a3412", 650),
    tx(756, 536, "∃P:  Pr(R_P(A(S)) ≥ 1/8)", 13, "#475569", 650),
    tx(756, 565, "≥ 1/7", 18, "#c2410c", 750),
]

# 16: overlapping distributions and lower-bound output.
p += [
    '<path d="M1090 376 C1120 294 1190 294 1218 376" fill="none" stroke="#22c55e" stroke-width="4"/>',
    '<path d="M1160 376 C1190 294 1260 294 1288 376" fill="none" stroke="#6366f1" stroke-width="4"/>',
    tx(1120, 306, "P₀", 15, "#15803d", 700),
    tx(1260, 306, "P₁", 15, "#4338ca", 700),
    '<line x1="1084" y1="378" x2="1300" y2="378" stroke="#cbd5e1" stroke-width="2"/>',
    tx(1192, 410, "overlap → testing error", 13, "#475569", 650, "middle"),
    arrow(1192, 426, 1192, 462),
    rect(1090, 470, 204, 58, "#f0fdf4", "#86efac", 13),
    tx(1192, 495, "inf_A sup_P risk", 15, "#166534", 700, "middle"),
    tx(1192, 517, "≥ testing lower bound", 13, "#166534", 650, "middle"),
    tx(1090, 565, "Le Cam: 2 points · Fano: packing", 13, "#166534", 650),
]

p += [
    '<line x1="70" y1="650" x2="1330" y2="650" stroke="#dbe4f0" stroke-width="2"/>',
    tx(70, 687, "上界告诉我们某算法能做到什么；下界告诉我们所有算法都无法跨过什么。", 18, "#334155", 650),
    tx(1330, 687, "LT-13—16 · v1", 15, "#64748b", 500, "end"),
    '</svg>',
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(p), encoding="utf-8")
print(OUTPUT)
