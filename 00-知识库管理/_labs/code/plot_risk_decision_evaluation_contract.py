#!/usr/bin/env python3
"""Generate the canonical four-panel visual for LT-05—LT-08."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "00-知识库管理/_assets/figures/learning-theory/fig-risk-decision-evaluation-contract-v1.svg"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=20, color="#1f2937", weight=500, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="Inter, PingFang SC, Noto Sans CJK SC, sans-serif" '
            f'font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')


def box(x, y, w, h, fill="#fff", stroke="#dbe4f0", r=18, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arr(x1, y1, x2, y2, color="#6366f1", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#arrow)"{d}/>'


p = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="720" viewBox="0 0 1400 720">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8faff"/><stop offset="1" stop-color="#eef7f4"/></linearGradient>',
    '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#26324d" flood-opacity="0.10"/></filter>',
    '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#6366f1"/></marker></defs>',
    '<rect width="1400" height="720" fill="url(#bg)"/>',
    txt(70, 70, "从经验风险到可信评价", 34, "#172554", 750),
    txt(70, 108, "分清误差来源、最优决策、学习保证与数据复用。", 20, "#53627a", 450),
]

meta = [
    ("05", "ERM 与误差分账", "优化训练量，不等于已控制目标风险", "#eef2ff", "#4f46e5"),
    ("06", "Bayes 最优决策", "先求条件风险，再对每个 x 选动作", "#ecfeff", "#0891b2"),
    ("07", "可学习性的量词", "finite-sample 与 asymptotic 不能混称", "#f0fdf4", "#16a34a"),
    ("08", "验证与测试复用", "反馈进入开发流程，holdout 就不再独立", "#fff7ed", "#ea580c"),
]

for i, (num, title, sub, tint, accent) in enumerate(meta):
    x = 70 + i * 330
    p += [f'<g filter="url(#shadow)">{box(x,155,300,455)}</g>', box(x+22,180,58,42,tint,accent,12),
          txt(x+51,209,num,19,accent,750,"middle"), txt(x+96,211,title,23,"#172554",700),
          txt(x+24,252,sub,15,"#64748b",450)]

# 05: risk ladder.
x0 = 92
levels = [("R*", "Bayes"), ("R_H*", "类内最优"), ("R_P(h_S)", "学习输出")]
for j, (main, sub) in enumerate(levels):
    y = 315 + j*92
    p += [box(x0, y, 118, 62, "#fff", "#a5b4fc", 14), txt(x0+59,y+29,main,18,"#4338ca",700,"middle"), txt(x0+59,y+50,sub,12,"#64748b",500,"middle")]
if True:
    p += [arr(212,346,264,346), txt(238,332,"近似",12,"#4f46e5",650,"middle"),
          arr(212,438,264,438), txt(238,424,"估计+算法",12,"#4f46e5",650,"middle"),
          box(266,315,80,62,"#eef2ff","#a5b4fc",14), txt(306,353,"差额",17,"#4338ca",700,"middle"),
          box(266,407,80,62,"#eef2ff","#a5b4fc",14), txt(306,445,"差额",17,"#4338ca",700,"middle"),
          txt(94,544,"generalization gap + ρ_opt",15,"#475569",600)]

# 06: posterior to actions.
p += [box(423,292,254,66,"#ecfeff","#67e8f9",16), txt(550,321,"η(x)=P(Y=1|x)",18,"#0e7490",700,"middle"), txt(550,346,"conditional law",13,"#64748b",500,"middle")]
for y,label,rule in [(397,"0–1","η ≥ 1/2"),(461,"成本敏感","η ≥ c_FP/(c_FP+c_FN)"),(525,"平方 / log","均值 / 完整分布")]:
    p += [box(430,y,104,48,"#fff","#a5f3fc",12), txt(482,y+30,label,14,"#0e7490",650,"middle"), arr(536,y+24,567,y+24), box(570,y,100,48,"#f8fafc","#cbd5e1",12), txt(620,y+30,rule,11,"#334155",600,"middle")]

# 07: 2x2 axes.
p += [txt(907,292,"有限样本",14,"#15803d",650,"middle"), txt(1025,292,"渐近",14,"#15803d",650,"middle"),
      txt(766,354,"可实现",14,"#15803d",650), txt(766,471,"不可知",14,"#15803d",650)]
for x,y,label in [(844,312,"realizable PAC"),(962,312,"相合性"),(844,429,"agnostic PAC"),(962,429,"Bayes / H-consistency")]:
    p += [box(x,y,110,82,"#f0fdf4","#86efac",14), txt(x+55,y+35,label.split(' ')[0],13,"#166534",650,"middle"), txt(x+55,y+58," ".join(label.split(' ')[1:]),11,"#64748b",500,"middle")]
p += [txt(758,544,"量词：∃ learner，∀P，∀ε,δ",15,"#475569",600)]

# 08: train/val/test flow + red feedback.
p += [box(1090,292,78,52,"#fff7ed","#fdba74",13), txt(1129,324,"Train",15,"#c2410c",700,"middle"),
      box(1200,292,72,52,"#fff7ed","#fdba74",13), txt(1236,324,"Val",15,"#c2410c",700,"middle"),
      box(1302,292,60,52,"#fff","#fdba74",13), txt(1332,324,"Test",15,"#c2410c",700,"middle"),
      arr(1168,318,1198,318), arr(1272,318,1300,318),
      box(1110,397,226,58,"#fffaf5","#fed7aa",14), txt(1223,423,"冻结 pipeline 后",14,"#7c2d12",650,"middle"), txt(1223,445,"只做最终估计",13,"#64748b",500,"middle"),
      arr(1332,346,1332,394,"#6366f1"),
      '<path d="M1330 482 C1260 550 1130 550 1110 468" stroke="#ef4444" stroke-width="3" fill="none" stroke-dasharray="8 7" marker-end="url(#arrow)"/>',
      txt(1225,523,"看结果再改模型 = feedback",14,"#b91c1c",650,"middle"), txt(1090,560,"K 次选择要付复杂度；自适应更难",13,"#475569",550)]

p += ['<line x1="70" y1="650" x2="1330" y2="650" stroke="#dbe4f0" stroke-width="2"/>',
      txt(70,687,"先对齐目标，再证明学习；先冻结算法，再使用最终测试。",18,"#334155",650),
      txt(1330,687,"LT-05—08 · v1",15,"#64748b",500,"end"), '</svg>']

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(p), encoding="utf-8")
print(OUTPUT)
