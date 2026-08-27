#!/usr/bin/env python3
"""Generate eight instructional SVGs for LM-17--LM-24."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "figures" / "language-models"
W, H = 1200, 700
BG = "#FFFEFB"
INK = "#17324D"
MUTED = "#64748B"
BLUE = "#2563EB"
TEAL = "#0F766E"
AMBER = "#B7791F"
RED = "#C24135"
PURPLE = "#7C3AED"
GRID = "#D7DEE8"


def e(x: object) -> str:
    return html.escape(str(x))


def begin(title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#64748B"/></marker><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#17324D" flood-opacity="0.12"/></filter></defs>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>',
        f'<text x="55" y="55" font-size="25" font-weight="700" fill="{BLUE}">{e(title)}</text>',
    ]


def end(lines: list[str], footer: str) -> None:
    lines += [f'<text x="55" y="670" font-size="14" fill="{MUTED}">{e(footer)}</text>', '</svg>']


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str, body: str = "", fill: str = "#FFFFFF", stroke: str = GRID, title_color: str = INK) -> None:
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
    lines.append(f'<text x="{x+18}" y="{y+31}" font-size="17" font-weight="700" fill="{title_color}">{e(title)}</text>')
    if body:
        for i, row in enumerate(body.split("\n")):
            lines.append(f'<text x="{x+18}" y="{y+58+i*23}" font-size="14" fill="{MUTED}">{e(row)}</text>')


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float, color: str = MUTED, dash: str = "") -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" marker-end="url(#arrow)"{extra}/>' )


def write(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines), encoding="utf-8")


def fig_source_rights() -> None:
    lines = begin("从网页资产到训练样本：对象链与权利链不能压成一个字段", "左侧是可追溯的数据变换，右侧是分层治理判断；公开可下载不等于内容统一许可。")
    lines.append(f'<text x="55" y="92" font-size="15" fill="{MUTED}">上方追踪实体/变换，下方逐层审计访问、内容权利、隐私与用途</text>')
    items = [
        ("网页/仓库资产", "URI · timestamp\ncontent owner ?", "#EFF6FF", BLUE),
        ("WARC capture", "record id · HTTP\npayload digest", "#ECFDF5", TEAL),
        ("解析后 document", "main text · metadata\nparser version", "#FFF7E8", AMBER),
        ("训练 sample", "token IDs · boundary\nloss eligibility", "#F5F3FF", PURPLE),
    ]
    for i, (t, b, fill, color) in enumerate(items):
        x = 55 + i * 282
        box(lines, x, 130, 225, 120, t, b, fill, color, color)
        if i < len(items)-1:
            arrow(lines, x+225, 190, x+272, 190)
    rights = [
        ("访问/抓取层", "crawler / robots / service terms", BLUE),
        ("内容权利层", "copyright · license · attribution", AMBER),
        ("主体与隐私层", "PII · sensitive data · deletion", RED),
        ("用途与法域层", "research/commercial · jurisdiction", PURPLE),
    ]
    for i, (t, b, c) in enumerate(rights):
        y = 325 + i * 70
        lines += [
            f'<rect x="85" y="{y}" width="880" height="50" rx="9" fill="#FFFFFF" stroke="{c}" stroke-width="2"/>',
            f'<text x="105" y="{y+31}" font-size="16" font-weight="700" fill="{c}">{e(t)}</text>',
            f'<text x="310" y="{y+31}" font-size="15" fill="{INK}">{e(b)}</text>',
            f'<rect x="990" y="{y+6}" width="145" height="38" rx="19" fill="#F2F5F8"/><text x="1062" y="{y+30}" text-anchor="middle" font-size="14" fill="{MUTED}">evidence + owner</text>',
        ]
    lines += [
        f'<rect x="765" y="270" width="365" height="38" rx="19" fill="#FEE2E2" stroke="{RED}"/>',
        f'<text x="947" y="295" text-anchor="middle" font-size="15" font-weight="700" fill="{RED}">服务访问条款 ≠ 抓取内容的统一许可</text>',
    ]
    end(lines, "格式/provenance 是审计基础，不是授权结论；不确定项必须保留并升级审批。")
    write(OUT / "fig-lm-data-source-rights-unit-v1.svg", lines)


def fig_filter_bias() -> None:
    lines = begin("解析与过滤是选择机制：保留集和拒绝集必须同时可见", "展示网页到文本的漏斗、过滤器串联、拒绝原因以及两个群体不同的保留率。")
    steps = [("HTML", 420, BLUE), ("主文本", 330, TEAL), ("语言=zh", 265, PURPLE), ("质量规则", 195, AMBER), ("最终文档", 145, RED)]
    cx = 315
    for i, (name, width, color) in enumerate(steps):
        y = 125 + i * 82
        x = cx-width/2
        lines += [
            f'<polygon points="{x},{y} {x+width},{y} {x+width-25},{y+52} {x+25},{y+52}" fill="{color}" opacity="0.88"/>',
            f'<text x="{cx}" y="{y+32}" text-anchor="middle" font-size="17" font-weight="700" fill="#FFFFFF">{e(name)}</text>',
        ]
        if i < len(steps)-1:
            arrow(lines, cx, y+55, cx, y+76)
    lines += [
        f'<text x="55" y="110" font-size="18" font-weight="700" fill="{INK}">retained path</text>',
        f'<text x="565" y="110" font-size="18" font-weight="700" fill="{INK}">rejected ledger</text>',
    ]
    rejects = [("parser empty", "layout / JS / boilerplate", 18, BLUE), ("LID reject", "code-switch / short text", 12, PURPLE), ("quality reject", "blocklist / score / length", 26, AMBER), ("duplicate", "exact / near / cluster policy", 15, RED)]
    for i, (t,b,p,c) in enumerate(rejects):
        y=145+i*82
        lines += [
            f'<rect x="565" y="{y}" width="360" height="58" rx="9" fill="#FFFFFF" stroke="{c}" stroke-width="2"/>',
            f'<text x="585" y="{y+24}" font-size="16" font-weight="700" fill="{c}">{e(t)}</text>',
            f'<text x="585" y="{y+46}" font-size="13" fill="{MUTED}">{e(b)}</text>',
            f'<text x="895" y="{y+36}" text-anchor="end" font-size="19" font-weight="700" fill="{c}">{p}%</text>',
        ]
    # Group retention bars
    lines += [f'<text x="565" y="510" font-size="18" font-weight="700" fill="{INK}">slice retention ≠ overall retention</text>']
    groups=[("Group A",0.74,TEAL),("Group B",0.41,RED)]
    for i,(name,val,c) in enumerate(groups):
        y=545+i*48
        lines += [f'<text x="570" y="{y+22}" font-size="15" fill="{INK}">{name}</text>',f'<rect x="665" y="{y}" width="{390*val}" height="30" rx="5" fill="{c}"/><text x="{680+390*val}" y="{y+21}" font-size="14" fill="{c}">{val:.0%}</text>']
    lines += [f'<rect x="960" y="145" width="175" height="360" rx="12" fill="#F2F5F8"/>',f'<text x="1047" y="180" text-anchor="middle" font-size="16" font-weight="700" fill="{INK}">每步必须保存</text>']
    for i,t in enumerate(["input hash","rule + version","score / threshold","reason code","group slices","counterfactual sample"]):
        lines.append(f'<text x="985" y="{220+i*42}" font-size="14" fill="{MUTED}">• {e(t)}</text>')
    end(lines, "“质量”不是无方向的清洁度；过滤器定义谁被看见、谁被重复、谁被排除。")
    write(OUT / "fig-lm-data-parse-filter-bias-v1.svg", lines)


def fig_minhash() -> None:
    lines = begin("近重复检测：从 shingles 与 Jaccard 到 MinHash 和 LSH 候选", "展示两个文档的 shingle 集、签名相等率、band collision 和最终 exact verification。")
    # Sets
    box(lines, 55, 120, 245, 190, "1 · shingle sets", "A={ab,bc,cd,de}\nB={ab,bc,cd,xy}\n|∩|=3, |∪|=5\nJ(A,B)=3/5", "#EFF6FF", BLUE, BLUE)
    arrow(lines, 305, 215, 360, 215)
    box(lines, 375, 120, 250, 190, "2 · MinHash signature", "k hashes / permutations\nmatch: [✓ ✓ ✗ ✓ ✗]\nestimator = 3/5\nvariance remains", "#ECFDF5", TEAL, TEAL)
    arrow(lines, 630, 215, 685, 215)
    box(lines, 700, 120, 225, 190, "3 · LSH bands", "b=2 bands, r=2 rows\nany band match → candidate\nP(candidate)=1-(1-sʳ)ᵇ", "#FFF7E8", AMBER, AMBER)
    arrow(lines, 930, 215, 985, 215)
    box(lines, 995, 120, 150, 190, "4 · verify", "exact Jaccard\nthreshold τ\ncluster + keep\nrepresentative", "#FEE2E2", RED, RED)
    lines += [
        f'<text x="55" y="365" font-size="18" font-weight="700" fill="{INK}">候选概率曲线（b=8, r=4）：阈值不是硬台阶</text>',
        f'<line x1="90" y1="595" x2="560" y2="595" stroke="{INK}" stroke-width="2"/><line x1="90" y1="595" x2="90" y2="400" stroke="{INK}" stroke-width="2"/>',
        f'<text x="530" y="625" font-size="14" fill="{MUTED}">similarity s</text><text x="30" y="410" font-size="14" fill="{MUTED}">P(candidate)</text>',
        f'<path d="M90 595 C 260 594, 330 575, 390 500 C 450 425, 500 405, 560 400" fill="none" stroke="{PURPLE}" stroke-width="4"/>',
        f'<line x1="390" y1="595" x2="390" y2="500" stroke="{RED}" stroke-dasharray="7 5"/><text x="398" y="580" font-size="13" fill="{RED}">operating point</text>',
    ]
    box(lines, 650, 365, 495, 245, "审计四问", "① shingle/normalization 是否改变对象？\n② signature length 给多大 estimator variance？\n③ LSH 的 false negative / candidate load？\n④ cluster 留最早、最长还是最高质量？", "#FFFFFF", GRID, INK)
    end(lines, "MinHash 估计 similarity；LSH 产生候选；最终删除仍需要阈值、验证与代表策略。")
    write(OUT / "fig-lm-data-minhash-lsh-v1.svg", lines)


def fig_contamination() -> None:
    lines = begin("Benchmark 污染：时间、字符串重叠与模型利用是三条证据链", "时间轴区分 benchmark release、crawl 和训练；检测层区分 exact、n-gram、semantic；结果层区分 exposure 与 exploitation。")
    lines += [f'<text x="55" y="105" font-size="18" font-weight="700" fill="{INK}">1 · 时间轴</text>',f'<line x1="90" y1="175" x2="1110" y2="175" stroke="{GRID}" stroke-width="5"/>']
    events=[(160,"benchmark draft",BLUE),(390,"public release",RED),(635,"crawl snapshot",AMBER),(850,"train cutoff",PURPLE),(1040,"evaluation",TEAL)]
    for x,t,c in events:
        lines += [f'<circle cx="{x}" cy="175" r="11" fill="{c}"/>',f'<text x="{x}" y="145" text-anchor="middle" font-size="14" font-weight="700" fill="{c}">{e(t)}</text>']
    lines += [f'<rect x="390" y="190" width="460" height="28" rx="6" fill="#FEE2E2" opacity="0.8"/><text x="620" y="210" text-anchor="middle" font-size="13" fill="{RED}">public benchmark can enter crawl / mirrors / tutorials / answers</text>']
    lines += [f'<text x="55" y="275" font-size="18" font-weight="700" fill="{INK}">2 · Detector family 与盲点</text>']
    detectors=[("exact hash","低假阳 / 漏格式变体",BLUE),("n-gram overlap","局部复制 / common phrase",TEAL),("semantic / paraphrase","覆盖改写 / 阈值不稳定",PURPLE),("black-box probe","无语料访问 / 因果归因弱",AMBER)]
    for i,(t,b,c) in enumerate(detectors):
        x=55+(i%2)*320;y=300+(i//2)*100
        box(lines,x,y,285,75,t,b,"#FFFFFF",c,c)
    lines += [f'<text x="710" y="275" font-size="18" font-weight="700" fill="{INK}">3 · exposure 与 score gain 不是同一事件</text>']
    cells=[("未暴露 / 未利用","clean",TEAL),("暴露 / 未利用","overlap only",AMBER),("未证暴露 / 异常高分","investigate",PURPLE),("暴露 / 可利用","contaminated gain",RED)]
    for i,(t,b,c) in enumerate(cells):
        x=710+(i%2)*215;y=310+(i//2)*125
        lines += [f'<rect x="{x}" y="{y}" width="195" height="100" rx="10" fill="#FFFFFF" stroke="{c}" stroke-width="2"/>',f'<text x="{x+15}" y="{y+33}" font-size="15" font-weight="700" fill="{c}">{e(t)}</text>',f'<text x="{x+15}" y="{y+65}" font-size="13" fill="{MUTED}">{e(b)}</text>']
    lines += [f'<rect x="55" y="555" width="1090" height="72" rx="10" fill="#FFF7E8" stroke="{AMBER}"/>',f'<text x="75" y="583" font-size="15" font-weight="700" fill="{AMBER}">报告：cutoff + detector operating point + clean/dirty split + confidence interval + removed examples</text>',f'<text x="75" y="610" font-size="14" fill="{MUTED}">未命中 detector 只表示“在该检测器与阈值下未发现”，不是无污染证明。</text>']
    end(lines, "污染审计是 measurement problem：先定义 exposure 单位，再谈模型是否记忆或利用。")
    write(OUT / "fig-lm-data-contamination-time-v1.svg", lines)


def fig_mixture() -> None:
    lines = begin("数据混合在 simplex 上：raw share、sample share 与 loss share 分开", "三域 mixture triangle 展示幂次采样移动，右侧给文档、token、loss 和梯度四份权重账。")
    # Triangle
    A=(120,545);B=(520,545);C=(320,175)
    lines += [f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#F8FAFC" stroke="{INK}" stroke-width="2"/>',f'<text x="90" y="575" font-size="16" font-weight="700" fill="{BLUE}">web</text>',f'<text x="515" y="575" font-size="16" font-weight="700" fill="{TEAL}">books</text>',f'<text x="320" y="150" text-anchor="middle" font-size="16" font-weight="700" fill="{PURPLE}">code</text>']
    points=[(365,485,"raw",RED),(320,400,"α<1",AMBER),(285,315,"optimized",TEAL)]
    for x,y,t,c in points:
        lines += [f'<circle cx="{x}" cy="{y}" r="10" fill="{c}"/>',f'<text x="{x+14}" y="{y-5}" font-size="14" font-weight="700" fill="{c}">{e(t)}</text>']
    arrow(lines,365,473,323,411,AMBER)
    arrow(lines,315,388,289,326,TEAL)
    lines += [f'<text x="55" y="105" font-size="18" font-weight="700" fill="{INK}">mixture vector π∈Δ²</text>',f'<text x="55" y="625" font-size="14" fill="{MUTED}">温度/幂次采样：q_d ∝ n_d^α；α=1 按规模，α→0 近域均匀</text>']
    # ledgers
    lines += [f'<text x="625" y="105" font-size="18" font-weight="700" fill="{INK}">一次配置需要四份 share</text>']
    ledgers=[("document draw","π = [0.60,0.25,0.15]",BLUE),("model tokens","长文/ fertility 后 ≠ π",TEAL),("effective loss","packing / ignore 后再变",AMBER),("gradient / utility","norm + direction + eval weights",RED)]
    for i,(t,b,c) in enumerate(ledgers):
        y=135+i*100
        lines += [f'<rect x="630" y="{y}" width="500" height="72" rx="10" fill="#FFFFFF" stroke="{c}" stroke-width="2"/>',f'<text x="650" y="{y+29}" font-size="16" font-weight="700" fill="{c}">{e(t)}</text>',f'<text x="820" y="{y+29}" font-size="15" fill="{INK}">{e(b)}</text>',f'<rect x="650" y="{y+44}" width="{110+i*60}" height="12" rx="6" fill="{c}" opacity="0.75"/>']
        if i<3: arrow(lines,880,y+75,880,y+94)
    box(lines, 630, 555, 500, 80, "评价聚合也有权重", "R(π)=Σₑ ρₑ Lₑ(π)；训练 mixture π 与评测权重 ρ 不要混名", "#F5F3FF", PURPLE, PURPLE)
    end(lines, "Mixture 优化依赖 domain taxonomy、proxy scale、预算和 evaluation weights；没有唯一脱离任务的最优 π。")
    write(OUT / "fig-lm-data-mixture-simplex-v1.svg", lines)


def fig_packing() -> None:
    lines = begin("Packing 的三重合同：装箱、块因果 relation 与边界标签", "展示三文档装入定长序列、正确块因果矩阵、position id 与跨文档 next-token label 处理。")
    colors=[BLUE,TEAL,AMBER]
    lines += [f'<text x="55" y="105" font-size="18" font-weight="700" fill="{INK}">1 · bin packing（长度 12）</text>']
    x0=55
    lengths=[4,3,5]
    pos=0
    for i,(length,c) in enumerate(zip(lengths,colors)):
        for k in range(length):
            x=x0+(pos+k)*39
            lines += [f'<rect x="{x}" y="135" width="35" height="48" rx="5" fill="{c}"/>',f'<text x="{x+17}" y="165" text-anchor="middle" font-size="13" fill="#FFFFFF">{i+1}.{k}</text>']
        pos+=length
    lines += [f'<text x="55" y="215" font-size="14" fill="{MUTED}">doc_id: 1111 | 222 | 33333</text>',f'<text x="55" y="240" font-size="14" fill="{MUTED}">position: reset 0… 或 continuous；必须与训练/部署合同一致</text>']
    # Matrix 12x12 compact
    lines += [f'<text x="55" y="305" font-size="18" font-weight="700" fill="{INK}">2 · relation = causal ∧ same_document</text>']
    cell=21;mx=70;my=330
    ids=[1]*4+[2]*3+[3]*5
    for i in range(12):
        for j in range(12):
            visible=int(j<=i and ids[i]==ids[j])
            fill=colors[ids[i]-1] if visible else "#F2F5F8"
            lines.append(f'<rect x="{mx+j*cell}" y="{my+i*cell}" width="19" height="19" fill="{fill}" stroke="#FFFFFF"/>')
    # wrong matrix visual
    lines += [f'<text x="380" y="305" font-size="18" font-weight="700" fill="{RED}">错误：只用全局下三角</text>']
    mx2=400
    for i in range(12):
        for j in range(12):
            visible=int(j<=i)
            fill=RED if visible and ids[i]!=ids[j] else ("#CBD5E1" if visible else "#F8FAFC")
            lines.append(f'<rect x="{mx2+j*cell}" y="{my+i*cell}" width="19" height="19" fill="{fill}" stroke="#FFFFFF"/>')
    lines += [f'<text x="400" y="605" font-size="14" fill="{RED}">红格 = 后文档读取前文档</text>']
    # right target table
    box(lines, 720, 105, 425, 505, "3 · 边界 label / loss", "", "#FFFFFF", GRID, INK)
    table=[("position","d1.2","d1.EOS","d2.0","d2.1"),("input","B","EOS","C","D"),("next label","EOS","? C","D","EOS"),("score?","✓","policy","✓","✓")]
    tx=745;ty=165;cw=[100,75,85,75,75]
    for r,row in enumerate(table):
        xx=tx
        for c,val in enumerate(row):
            fill="#F2F5F8" if r==0 or c==0 else "#FFFFFF"
            lines += [f'<rect x="{xx}" y="{ty+r*48}" width="{cw[c]}" height="44" fill="{fill}" stroke="{GRID}"/>',f'<text x="{xx+cw[c]/2}" y="{ty+r*48+28}" text-anchor="middle" font-size="13" font-weight="{700 if r==0 or c==0 else 400}" fill="{RED if val=="? C" else INK}">{e(val)}</text>']
            xx+=cw[c]
    lines += [f'<text x="745" y="390" font-size="15" font-weight="700" fill="{RED}">跨文档 next-token 二选一：</text>',f'<text x="765" y="425" font-size="14" fill="{MUTED}">A. 用显式 EOS 作为 d1 末目标，再 block；</text>',f'<text x="765" y="455" font-size="14" fill="{MUTED}">B. ignore 边界 logit，不预测 d2 首 token。</text>',f'<text x="765" y="495" font-size="14" fill="{MUTED}">不可静默训练 EOS→下篇首 token，除非</text>',f'<text x="765" y="520" font-size="14" fill="{MUTED}">你明确要建模拼接流且部署也同合同。</text>']
    end(lines, "Packing efficiency 是系统指标；与未 packed 语义等价需要 relation、position 与 labels 三者一起测试。")
    write(OUT / "fig-lm-data-packing-mask-position-v1.svg", lines)


def fig_curriculum() -> None:
    lines = begin("数据顺序会改写训练路径：Curriculum、DAPT/TAPT 与遗忘账", "上方显示 checkpoint 路径与可变 mixture schedule；下方画新域改善和旧域退化的双风险轨迹。")
    stages=[("base θ₀","general mix",BLUE),("DAPT θ₁","domain corpus",PURPLE),("TAPT θ₂","task text",AMBER),("supervised θ₃","labeled data",TEAL)]
    for i,(t,b,c) in enumerate(stages):
        x=55+i*285
        box(lines,x,125,220,90,t,b,"#FFFFFF",c,c)
        if i<3: arrow(lines,x+220,170,x+275,170)
    lines += [f'<text x="55" y="100" font-size="18" font-weight="700" fill="{INK}">checkpoint lineage：每段 optimizer / data / token budget 单独版本化</text>']
    # schedule bands
    lines += [f'<text x="55" y="280" font-size="18" font-weight="700" fill="{INK}">mixture schedule π(t)</text>']
    sx=55;sy=305
    segments=[(180,BLUE,"general 100%"),(170,PURPLE,"domain ↑"),(170,AMBER,"task ↑"),(180,TEAL,"replay mix")]
    for w,c,t in segments:
        lines += [f'<rect x="{sx}" y="{sy}" width="{w}" height="42" fill="{c}" opacity="0.85"/>',f'<text x="{sx+w/2}" y="{sy+27}" text-anchor="middle" font-size="13" fill="#FFFFFF">{e(t)}</text>']
        sx+=w
    lines += [f'<line x1="55" y1="365" x2="755" y2="365" stroke="{INK}"/><text x="730" y="388" font-size="13" fill="{MUTED}">training time</text>']
    # risk chart
    lines += [f'<text x="55" y="445" font-size="18" font-weight="700" fill="{INK}">双验证集：只看新域会隐藏遗忘</text>',f'<line x1="90" y1="615" x2="735" y2="615" stroke="{INK}"/><line x1="90" y1="615" x2="90" y2="470" stroke="{INK}"/>',f'<path d="M95 520 C 220 545, 330 575, 450 590 C 560 600, 650 604, 730 605" fill="none" stroke="{PURPLE}" stroke-width="4"/>',f'<path d="M95 560 C 240 555, 330 520, 450 495 C 570 480, 650 475, 730 472" fill="none" stroke="{RED}" stroke-width="4"/>',f'<text x="580" y="595" font-size="14" fill="{PURPLE}">new-domain loss ↓</text>',f'<text x="580" y="465" font-size="14" fill="{RED}">old-domain loss ↑</text>']
    box(lines, 810, 285, 335, 335, "路径审计", "顺序：what came first?\n预算：unique / repeated tokens?\n状态：optimizer 是否重置？\n回放：旧域比例与采样？\n评价：新/旧/安全切片？\n选择：报告所有 tried orders？", "#FFF7E8", AMBER, AMBER)
    end(lines, "相同最终数据 multiset、不同顺序仍可到不同参数；curriculum 结论必须包含 path 和 selection budget。")
    write(OUT / "fig-lm-data-curriculum-continual-v1.svg", lines)


def fig_provenance() -> None:
    lines = begin("Provenance graph 与有效 Token 瀑布：规模必须可逆追溯", "左侧用实体/活动图追踪 WARC 到训练 shard；右侧把 raw tokens 逐步扣除为有效 loss targets。")
    lines += [f'<text x="55" y="105" font-size="18" font-weight="700" fill="{INK}">1 · content-addressed lineage（Entity — Activity — Entity）</text>']
    entities=[(55,140,"WARC E0","sha256:…",BLUE),(340,140,"text E1","parser:v3",TEAL),(625,140,"kept E2","filter:f7",AMBER),(910,140,"tokens E3","tok:hash",PURPLE),(625,300,"pack E4","packer:p2",RED),(910,300,"shard E5","manifest",TEAL)]
    for x,y,t,b,c in entities: box(lines,x,y,220,78,t,b,"#FFFFFF",c,c)
    for x1,y1,x2,y2,label in [(275,179,335,179,"parse"),(560,179,620,179,"filter"),(845,179,905,179,"tokenize"),(735,220,700,295,"pack"),(845,339,905,339,"write")]:
        arrow(lines,x1,y1,x2,y2)
        lines.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-8}" text-anchor="middle" font-size="12" fill="{MUTED}">{e(label)}</text>')
    lines += [f'<path d="M165 220 C165 340,390 400,625 340" fill="none" stroke="{GRID}" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#arrow)"/>',f'<text x="325" y="365" font-size="13" fill="{MUTED}">rejection/cluster manifests preserve removed ancestors</text>']
    # waterfall
    lines += [f'<text x="55" y="445" font-size="18" font-weight="700" fill="{INK}">2 · 规模瀑布：每一步的单位与 hash</text>']
    vals=[("raw bytes",100,BLUE),("parsed text",82,TEAL),("after filter",61,AMBER),("unique tokens",48,PURPLE),("packed tokens",46,RED),("loss targets",42,TEAL)]
    x=55
    for i,(name,val,c) in enumerate(vals):
        h=val*1.35;y=625-h
        lines += [f'<rect x="{x}" y="{y}" width="120" height="{h}" rx="6" fill="{c}" opacity="0.85"/>',f'<text x="{x+60}" y="{y-8}" text-anchor="middle" font-size="14" font-weight="700" fill="{c}">{val}M</text>',f'<text x="{x+60}" y="648" text-anchor="middle" font-size="12" fill="{MUTED}">{e(name)}</text>']
        if i<len(vals)-1: arrow(lines,x+122,590,x+145,590)
        x+=150
    lines += [f'<rect x="970" y="435" width="175" height="190" rx="10" fill="#F2F5F8"/>',f'<text x="1057" y="468" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">manifest minimum</text>']
    for i,t in enumerate(["parent hashes","activity config","code/container","agent/approval","counts by slice","failure + deletion"]): lines.append(f'<text x="990" y="{505+i*24}" font-size="13" fill="{MUTED}">• {e(t)}</text>')
    end(lines, "“训练了 42M tokens”只有在能回溯到原始实体、变换和被排除对象时才是可审计事实。")
    write(OUT / "fig-lm-data-provenance-effective-token-v1.svg", lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_source_rights()
    fig_filter_bias()
    fig_minhash()
    fig_contamination()
    fig_mixture()
    fig_packing()
    fig_curriculum()
    fig_provenance()
    print("generated 8 figures in", OUT)


if __name__ == "__main__":
    main()
