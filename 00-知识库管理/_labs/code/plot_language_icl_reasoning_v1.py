#!/usr/bin/env python3
"""Generate eight textbook-style SVGs for LM-33--LM-40."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "figures" / "language-models"
W, H = 1200, 700
BG, INK, MUTED, GRID = "#FFFEFB", "#17324D", "#64748B", "#D7DEE8"
BLUE, TEAL, AMBER, RED, PURPLE = "#2563EB", "#0F766E", "#D97706", "#C24135", "#7C3AED"


def esc(x: object) -> str:
    return html.escape(str(x))


def begin(title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#64748B"/></marker><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#17324D" flood-opacity="0.10"/></filter></defs>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>',
        f'<text x="55" y="55" font-size="25" font-weight="700" fill="{BLUE}">{esc(title)}</text>',
    ]


def finish(lines: list[str], footer: str) -> None:
    lines += [f'<text x="55" y="670" font-size="14" fill="{MUTED}">{esc(footer)}</text>', '</svg>']


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str, body: str = "", color: str = BLUE, fill: str = "#FFFFFF") -> None:
    lines += [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="2" filter="url(#shadow)"/>',
        f'<text x="{x+16}" y="{y+29}" font-size="16" font-weight="700" fill="{color}">{esc(title)}</text>',
    ]
    for i, row in enumerate(body.split("\n")):
        lines.append(f'<text x="{x+16}" y="{y+56+i*22}" font-size="13" fill="{MUTED}">{esc(row)}</text>')


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float, color: str = MUTED, dash: str = "") -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" marker-end="url(#arrow)"{extra}/>')


def write(name: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")


def prompt_event() -> None:
    lines = begin("Prompt 是精确条件事件，不是肉眼语义标签", "同一意图经不同模板、tokenizer 和答案边界形成不同 token 前缀与条件分布。")
    box(lines, 55, 120, 235, 110, "语义任务", "判断评论情感\n输出 positive / negative", BLUE, "#EFF6FF")
    arrow(lines, 300, 175, 365, 175)
    variants = [
        (380, 95, "序列 A", "Review: ...\nSentiment:", TEAL),
        (380, 245, "序列 B", "文本：...\n标签：", PURPLE),
        (380, 395, "序列 C", "<user>...<assistant>\nleading space + marker", AMBER),
    ]
    for x, y, title, body, color in variants:
        box(lines, x, y, 260, 105, title, body, color)
        arrow(lines, 650, y+52, 730, y+52, color)
    outputs = [
        (745, 95, "IDs [11, 93, 7, ...]", "P(pos)=.72", TEAL),
        (745, 245, "IDs [51, 18, 4, ...]", "P(pos)=.41", PURPLE),
        (745, 395, "IDs [1, 320, 9, ...]", "P(pos)=.63", AMBER),
    ]
    for x, y, title, body, color in outputs:
        box(lines, x, y, 285, 105, title, body, color, "#FFFFFF")
    box(lines, 55, 525, 975, 90, "可比较性合同", "固定 bytes → normalization → template → token IDs → label token set → generation boundary → sampler；逐因子做 counterfactual sweep。", RED, "#FEE2E2")
    finish(lines, "语义相近不推出条件概率相同；prompt sensitivity 是实验对象，不是需要藏掉的噪声。")
    write("fig-lm-icl-prompt-conditional-event-v1.svg", lines)


def icl_design() -> None:
    lines = begin("ICL 不是一个开关：用因子设计拆开示例内容、顺序与标签映射", "左侧列出干预因子，右侧以同一示例集合的排列热图和正确率分布展示敏感性。")
    factors = [
        ("instruction", "present / absent / paraphrase", BLUE),
        ("demo inputs", "correct / shuffled / retrieved", TEAL),
        ("demo labels", "correct / random / permuted", PURPLE),
        ("order", "all K! or preregistered sample", AMBER),
        ("verbalizer", "A/B vs positive/negative", RED),
    ]
    for i, (name, body, color) in enumerate(factors):
        box(lines, 55, 105+i*96, 360, 75, name, body, color)
    lines += [f'<text x="485" y="105" font-size="18" font-weight="700" fill="{INK}">同一四个 demos 的 24 种排列</text>']
    vals = [0.83,0.70,0.55,0.48,0.76,0.42,0.88,0.62,0.51,0.36,0.79,0.67,0.46,0.73,0.59,0.40,0.81,0.65,0.57,0.33,0.69,0.52,0.75,0.44]
    for i, v in enumerate(vals):
        r, c = divmod(i, 6); x, y = 490+c*88, 135+r*76
        color = TEAL if v >= .7 else AMBER if v >= .5 else RED
        opacity = .35 + .65*v
        lines += [f'<rect x="{x}" y="{y}" width="72" height="58" rx="7" fill="{color}" fill-opacity="{opacity:.2f}"/>', f'<text x="{x+36}" y="{y+35}" text-anchor="middle" font-size="13" fill="#FFFFFF">{v:.2f}</text>']
    box(lines, 490, 465, 510, 135, "报告分布，不只报告最好 prompt", "mean / median / min / max / quantiles\nselection rule + tuning set + number of tried prompts\npaired prediction flips + bootstrap interval", RED, "#FEE2E2")
    finish(lines, "若用测试集挑模板、示例或顺序，few-shot 结果已包含隐藏监督；label mapping 与答案解析器必须固定。")
    write("fig-lm-icl-factorial-sensitivity-v1.svg", lines)


def theory_lenses() -> None:
    lines = begin("三种 ICL 解释是带假设的模型，不是互斥口号", "Bayesian latent concept、线性回归 estimator 与 forward-pass optimizer 由不同假设到达 query prediction。")
    lenses = [
        (55, 105, "Bayesian lens", "latent task z\nposterior p(z | D)\nposterior predictive", PURPLE),
        (55, 285, "Estimator lens", "y = xᵀw + ε\nleast squares / ridge\ncompare risk curve", BLUE),
        (55, 465, "Optimizer lens", "w₁ = w₀ − η∇L_D\nlayer ≈ update step\nmechanistic construction", TEAL),
    ]
    for x, y, title, body, color in lenses:
        box(lines, x, y, 285, 130, title, body, color)
        arrow(lines, 350, y+65, 455, 350, color)
    box(lines, 475, 255, 265, 190, "Prompt D + query x*", "D={(xᵢ,yᵢ)}\nno deployment weight update\nproduce ŷ* or p(y* | D,x*)", AMBER, "#FFF7E8")
    arrow(lines, 750, 350, 835, 350)
    box(lines, 850, 255, 295, 190, "Discriminating tests", "prior shift\nnoise / condition number\nOOD coefficients\nlayerwise state probe\nalgorithmic precision", RED, "#FEE2E2")
    lines += [f'<text x="405" y="595" font-size="14" fill="{MUTED}">同一输入—输出行为可有多个解释；要用干预与失败域区分，而非只拟合一条平均曲线。</text>']
    finish(lines, "Toy theorem 的量词必须保留：模型族、训练分布、任务类、prompt 格式、深度和误差度量缺一不可。")
    write("fig-lm-icl-theory-lenses-v1.svg", lines)


def induction_circuit() -> None:
    lines = begin("Induction Head：从重复 token 模式到机制证据梯子", "上方展示 AB…A→B 的两头回路，下方区分注意力图、logit effect、ablation 与精确权重构造。")
    toks = ["A", "B", "C", "·", "·", "A", "?"]
    for i, t in enumerate(toks):
        x=70+i*105
        lines += [f'<rect x="{x}" y="115" width="70" height="52" rx="8" fill="{BLUE if t in ["A","B"] else "#EEF2F7"}"/>', f'<text x="{x+35}" y="148" text-anchor="middle" font-size="19" font-weight="700" fill="{"#FFFFFF" if t in ["A","B"] else INK}">{t}</text>']
    lines += [f'<path d="M610 110 C500 50,210 50,105 110" fill="none" stroke="{PURPLE}" stroke-width="3" marker-end="url(#arrow)"/>', f'<text x="360" y="85" text-anchor="middle" font-size="14" fill="{PURPLE}">prefix match: current A finds earlier A</text>']
    lines += [f'<path d="M210 175 C300 240,655 240,735 175" fill="none" stroke="{TEAL}" stroke-width="3" marker-end="url(#arrow)"/>', f'<text x="480" y="225" text-anchor="middle" font-size="14" fill="{TEAL}">copy: token B after earlier A raises final B logit</text>']
    evidence = [
        ("attention pattern", "where a head looks", AMBER),
        ("direct logit effect", "what token it promotes", BLUE),
        ("activation patch / ablation", "causal necessity in this run", RED),
        ("weight-level construction", "sufficiency in specified model", TEAL),
    ]
    for i, (title, body, color) in enumerate(evidence):
        x=55+i*280
        box(lines, x, 330, 245, 110, title, body, color)
        if i<3: arrow(lines,x+245,385,x+275,385)
    box(lines, 55, 500, 1085, 105, "外推边界", "两层 attention-only 的精确回路 ≠ 含 MLP 大模型的全部 ICL；单头消融也可能被冗余回路、分布外干预和 downstream nonlinearities 混淆。", PURPLE, "#F5F3FF")
    finish(lines, "机制结论应同时报告行为任务、head criterion、干预对象、替代回路和模型族。")
    write("fig-lm-icl-induction-head-evidence-v1.svg", lines)


def cot_faithfulness() -> None:
    lines = begin("可见 Chain-of-Thought 既是计算工作区，也可能是事后叙述", "结构图分离问题、隐藏状态、可见 trace 与答案，并列出四类反事实干预。")
    box(lines, 55, 150, 205, 105, "Question X", "facts + wording\npossible bias cue H", BLUE, "#EFF6FF")
    arrow(lines, 270, 202, 355, 202)
    box(lines, 370, 120, 235, 165, "Model state U", "distributed activations\nparametric knowledge\nattention + MLP computation", PURPLE, "#F5F3FF")
    arrow(lines, 615, 165, 710, 165)
    box(lines, 725, 105, 205, 110, "Visible trace R", "step 1, step 2, ...\neditable text channel", AMBER, "#FFF7E8")
    arrow(lines, 940, 160, 1015, 202)
    box(lines, 1025, 150, 120, 105, "Answer Y", "parsed\nscored", TEAL, "#ECFDF5")
    arrow(lines, 605, 245, 1015, 230, RED, "7 5")
    lines += [f'<text x="755" y="275" font-size="13" fill="{RED}">direct hidden path may bypass stated rationale</text>']
    interventions = [
        (55, 355, "truncate", "remove late steps", BLUE),
        (325, 355, "paraphrase", "same claimed content", TEAL),
        (595, 355, "inject error", "flip one premise/step", RED),
        (865, 355, "bias cue", "affects answer; is it mentioned?", PURPLE),
    ]
    for x,y,title,body,color in interventions: box(lines,x,y,245,100,title,body,color)
    box(lines, 190, 515, 820, 95, "Faithfulness 不是单一分数", "causal dependence · sufficiency · completeness · executable validity · counterfactual stability；先选定义，再选干预和指标。", RED, "#FEE2E2")
    finish(lines, "答案正确、步骤可读、步骤局部正确、解释忠实是四个不同事件；任何两者都不能自动推出另一个。")
    write("fig-lm-icl-cot-faithfulness-v1.svg", lines)


def sampling_estimators() -> None:
    lines = begin("多样本推理要分覆盖率、聚合器与选择器", "左侧是同一问题的采样路径；右侧对比 self-consistency、oracle pass-at-k 与 verifier best-of-N。")
    box(lines, 55, 115, 190, 80, "Prompt x", "fixed sampler contract", BLUE, "#EFF6FF")
    paths=[("r₁ → A",True,TEAL),("r₂ → B",False,RED),("r₃ → A",True,TEAL),("r₄ → C",False,AMBER),("r₅ → A",True,TEAL)]
    for i,(lab,ok,color) in enumerate(paths):
        y=90+i*92
        arrow(lines,245,155,345,y+38,color)
        box(lines,360,y,190,70,lab,"correct" if ok else "wrong",color)
    box(lines, 650, 95, 470, 105, "Self-consistency", "normalize final answers; A has 3/5 votes\nmajority estimates modal answer, not truth", PURPLE, "#F5F3FF")
    box(lines, 650, 245, 470, 105, "Pass-at-k", "oracle event: at least one success among k\n1 − C(n−c,k) / C(n,k)", BLUE, "#EFF6FF")
    box(lines, 650, 395, 470, 105, "Best-of-N", "verifier ranks N candidates; report oracle coverage\nand selection regret separately", TEAL, "#ECFDF5")
    box(lines, 650, 545, 470, 72, "Shared budget", "samples × tokens + verifier calls + parser failures + latency", RED, "#FEE2E2")
    finish(lines, "更多样本只有在增加有效多样性且聚合/选择规则利用这些候选时才改善 top-1；相关性会降低有效 N。")
    write("fig-lm-icl-sampling-selection-v1.svg", lines)


def test_time_search() -> None:
    lines = begin("Test-time Compute：把生成、搜索、验证与停止写成同一算法", "搜索树标出 proposal、value、branching、pruning 和 early stop；下方给出多维预算账。")
    coords=[(590,105,"s₀",BLUE),(350,225,"s₁",TEAL),(590,225,"s₂",AMBER),(830,225,"s₃",RED),(230,360,"s₁₁",TEAL),(400,360,"s₁₂",RED),(520,360,"s₂₁",AMBER),(690,360,"s₂₂",TEAL),(800,360,"s₃₁",RED),(970,360,"s₃₂",RED)]
    for x,y,label,color in coords:
        lines += [f'<circle cx="{x}" cy="{y}" r="28" fill="{color}"/>', f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">{label}</text>']
    edges=[(590,133,350,197),(590,133,590,197),(590,133,830,197),(350,253,230,332),(350,253,400,332),(590,253,520,332),(590,253,690,332),(830,253,800,332),(830,253,970,332)]
    for a,b,c,d in edges: arrow(lines,a,b,c,d)
    lines += [f'<text x="55" y="465" font-size="16" font-weight="700" fill="{INK}">Algorithm = proposal π + state parser + value V + queue rule + pruning + stopping</text>']
    budget=[("generated tokens",.82,BLUE),("model FLOPs",.70,PURPLE),("verifier calls",.48,TEAL),("serial latency",.61,AMBER),("peak memory",.37,RED)]
    for i,(name,val,color) in enumerate(budget):
        x=55+i*220
        lines += [f'<text x="{x}" y="520" font-size="12" fill="{INK}">{esc(name)}</text>', f'<rect x="{x}" y="540" width="175" height="25" rx="5" fill="#EEF2F7"/>', f'<rect x="{x}" y="540" width="{175*val}" height="25" rx="5" fill="{color}"/>']
    box(lines, 55, 585, 1065, 46, "公平比较", "同题集、同 policy、同最大输出、同总预算；报告 difficulty-stratified curve 与 anytime performance。", RED, "#FEE2E2")
    finish(lines, "Token budget、FLOPs、调用数和 wall-clock 不可互换；搜索质量由 proposal coverage 与 verifier calibration 共同限制。")
    write("fig-lm-icl-test-time-search-v1.svg", lines)


def long_context() -> None:
    lines = begin("声明窗口不等于有效上下文：长度、证据位置与任务复杂度必须联合扫描", "左侧绘制位置效应曲线，右侧展示 length × task 矩阵以及声明窗口与有效窗口的区别。")
    x0,y0,w,h=70,375,465,240
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="{INK}" stroke-width="2"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-h}" stroke="{INK}" stroke-width="2"/>']
    pts=[(75,175),(145,215),(215,285),(300,330),(385,275),(465,205),(530,165)]
    path="M"+" L".join(f"{x},{y}" for x,y in pts)
    lines += [f'<path d="{path}" fill="none" stroke="{RED}" stroke-width="4"/>']
    for x,y in pts: lines.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{RED}"/>')
    lines += [f'<text x="80" y="120" font-size="15" font-weight="700" fill="{INK}">evidence-position accuracy</text>', f'<text x="75" y="410" font-size="12" fill="{MUTED}">start</text>', f'<text x="285" y="410" font-size="12" fill="{MUTED}">middle</text>', f'<text x="500" y="410" font-size="12" fill="{MUTED}">end</text>']
    tasks=["single needle","multi-needle","multi-hop","aggregation"]
    lengths=["8K","16K","32K","64K"]
    vals=[[.98,.92,.82,.64],[.91,.80,.61,.40],[.85,.67,.44,.25],[.79,.58,.36,.18]]
    for j,t in enumerate(tasks): lines.append(f'<text x="{675+j*112}" y="128" text-anchor="middle" font-size="12" fill="{INK}">{t}</text>')
    for i,l in enumerate(lengths):
        lines.append(f'<text x="600" y="{165+i*72}" font-size="13" fill="{INK}">{l}</text>')
        for j,v in enumerate(vals[i]):
            x,y=635+j*112,140+i*72; color=TEAL if v>=.8 else AMBER if v>=.5 else RED
            lines += [f'<rect x="{x}" y="{y}" width="88" height="52" rx="6" fill="{color}" fill-opacity="{.35+.65*v:.2f}"/>', f'<text x="{x+44}" y="{y+32}" text-anchor="middle" font-size="13" fill="#FFFFFF">{v:.0%}</text>']
    box(lines, 625, 470, 500, 130, "两个窗口", "declared context: API accepts T tokens\neffective context: task accuracy remains above preregistered threshold\n必须绑定 task × position × distractor × output contract", PURPLE, "#F5F3FF")
    finish(lines, "Lost-in-the-middle 是经验诊断而非结构定理；RULER 的 synthetic success 也不能替代真实文档理解。")
    write("fig-lm-icl-long-context-evidence-v1.svg", lines)


def main() -> None:
    prompt_event(); icl_design(); theory_lenses(); induction_circuit()
    cot_faithfulness(); sampling_estimators(); test_time_search(); long_context()


if __name__ == "__main__":
    main()
