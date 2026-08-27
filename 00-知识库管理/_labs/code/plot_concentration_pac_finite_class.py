#!/usr/bin/env python3
"""Generate the canonical LT-09—LT-12 concentration/PAC visual."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "00-知识库管理/_assets/figures/learning-theory/fig-concentration-pac-finite-class-v1.svg"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tx(x,y,s,size=20,color="#1f2937",weight=500,anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Inter, PingFang SC, Noto Sans CJK SC, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'


def rect(x,y,w,h,fill="#fff",stroke="#dbe4f0",r=18,sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1,y1,x2,y2,color="#6366f1",dash=""):
    ds=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#arr)"{ds}/>'


p=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="720" viewBox="0 0 1400 720">',
   '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8faff"/><stop offset="1" stop-color="#eef7f4"/></linearGradient><filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#26324d" flood-opacity="0.10"/></filter><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#6366f1"/></marker></defs>',
   '<rect width="1400" height="720" fill="url(#bg)"/>',
   tx(70,70,"从一次浓缩到有限类 PAC 保证",34,"#172554",750),
   tx(70,108,"固定一个函数 → 写全量词 → 同时控制整个类 → 利用可实现结构提速。",20,"#53627a",450)]

meta=[("09","固定 h 的浓缩","先固定预测器，再抽独立样本","#eef2ff","#4f46e5"),
      ("10","PAC 量词合同","ε 是精度，δ 是失败概率，m 是资源","#ecfeff","#0891b2"),
      ("11","有限类一致控制","Union Bound 把 M 个坏事件相加","#f0fdf4","#16a34a"),
      ("12","可实现一致 ERM","坏函数要在 m 次抽样中零失误","#fff7ed","#ea580c")]
for i,(num,title,sub,tint,accent) in enumerate(meta):
    x=70+i*330
    p += [f'<g filter="url(#shadow)">{rect(x,155,300,455)}</g>',rect(x+22,180,58,42,tint,accent,12),tx(x+51,209,num,19,accent,750,"middle"),tx(x+96,211,title,23,"#172554",700),tx(x+24,252,sub,15,"#64748b",450)]

# 09: interval around population risk.
p += [tx(94,304,"R_S(h)",17,"#4338ca",700), '<line x1="100" y1="377" x2="342" y2="377" stroke="#cbd5e1" stroke-width="3"/>',
      '<rect x="170" y="347" width="104" height="60" rx="14" fill="#eef2ff" stroke="#a5b4fc" stroke-width="2"/>', tx(222,372,"R_P(h) ± ε",16,"#4338ca",700,"middle"),tx(222,395,"置信带",12,"#64748b",500,"middle"),
      '<circle cx="122" cy="377" r="7" fill="#ef4444"/><circle cx="320" cy="377" r="7" fill="#ef4444"/>',
      tx(92,455,"P(|R_S−R_P|>ε)",15,"#475569",600),tx(92,487,"≤ 2 exp(−2mε²)",18,"#4338ca",700),tx(92,544,"h 若由同一 S 选出：不能直接代入",14,"#b45309",650)]

# 10: PAC controls.
for y,label,val,color in [(300,"精度","ε ↓","#0e7490"),(375,"置信","δ ↓","#0e7490"),(450,"样本","m ↑","#0e7490")]:
    p += [rect(430,y,104,54,"#ecfeff","#67e8f9",13),tx(482,y+33,label,15,color,650,"middle"),arrow(536,y+27,573,y+27),rect(576,y,92,54,"#fff","#a5f3fc",13),tx(622,y+33,val,18,color,700,"middle")]
p += [tx(425,535,"∀P，P_S(excess ≤ ε) ≥ 1−δ",14,"#475569",650)]

# 11: hypotheses and union.
for row in range(3):
    for col in range(3):
        cx=755+col*56; cy=320+row*64
        p += [rect(cx,cy,52,42,"#f0fdf4","#86efac",10),tx(cx+26,cy+27,f"h{row*3+col+1}",12,"#166534",650,"middle")]
p += [arrow(922,386,946,386),rect(950,350,58,72,"#fff","#86efac",12),tx(979,380,"Σ",23,"#15803d",750,"middle"),tx(979,405,"坏事件",11,"#64748b",500,"middle"),
      tx(760,516,"P(∃h bad) ≤ 2M e^(−2mε²)",14,"#166534",650),tx(760,548,"complexity = log M",15,"#475569",600)]

# 12: survival probability.
p += [rect(1090,292,114,58,"#fff7ed","#fdba74",14),tx(1147,320,"坏 h",16,"#c2410c",700,"middle"),tx(1147,342,"R_P(h)>ε",12,"#64748b",500,"middle"),arrow(1206,321,1240,321),rect(1244,292,92,58,"#fff","#fdba74",14),tx(1290,320,"零训练错",13,"#c2410c",650,"middle"),tx(1290,341,"生存",12,"#64748b",500,"middle"),
      tx(1092,402,"P(R_S(h)=0)",15,"#7c2d12",600),tx(1092,434,"= (1−R_P(h))^m",16,"#9a3412",700),tx(1092,466,"≤ exp(−mε)",18,"#c2410c",750),
      tx(1092,520,"× |H| ≤ δ",17,"#475569",650),tx(1092,552,"m ≥ log(|H|/δ) / ε",15,"#b45309",700)]

p += ['<line x1="70" y1="650" x2="1330" y2="650" stroke="#dbe4f0" stroke-width="2"/>',tx(70,687,"固定 h 的 concentration 不是终点；学习保证必须覆盖数据选出的输出。",18,"#334155",650),tx(1330,687,"LT-09—12 · v1",15,"#64748b",500,"end"),'</svg>']

OUTPUT.parent.mkdir(parents=True,exist_ok=True)
OUTPUT.write_text("\n".join(p),encoding="utf-8")
print(OUTPUT)
