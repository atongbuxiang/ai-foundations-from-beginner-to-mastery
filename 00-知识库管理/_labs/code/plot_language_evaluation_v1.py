#!/usr/bin/env python3
"""Generate eight varied textbook-style SVGs for LM-57--LM-64."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "figures" / "language-models"
W, H = 1200, 700
BG, PAPER, INK, MUTED, GRID = "#FBF8F1", "#FFFDF8", "#183044", "#667784", "#D9D5CB"
BLUE, TEAL, AMBER, RED, PURPLE, GREEN = "#245AA8", "#17766E", "#C87922", "#B7443E", "#7054A3", "#4F7B45"


def esc(x: object) -> str:
    return html.escape(str(x))


def begin(title: str, desc: str, accent: str) -> list[str]:
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
    lines += [f'<line x1="48" y1="650" x2="1152" y2="650" stroke="{GRID}"/>',
              f'<text x="52" y="674" font-size="13" fill="{MUTED}">{esc(footer)}</text>', '</svg>']


def text(lines: list[str], x: float, y: float, value: str, color: str = MUTED,
         size: float = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(value)}</text>')


def multi(lines: list[str], x: float, y: float, value: str, color: str = MUTED,
          size: float = 13, leading: float = 20, anchor: str = "start", weight: int = 400) -> None:
    for i, row in enumerate(value.split("\n")):
        text(lines, x, y + i * leading, row, color, size, anchor, weight)


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str,
        body: str = "", color: str = BLUE, fill: str = PAPER, radius: float = 10) -> None:
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{color}" stroke-width="1.8" filter="url(#shadow)"/>')
    text(lines, x + 15, y + 28, title, color, 15, "start", 700)
    multi(lines, x + 15, y + 53, body, MUTED, 12.3, 20)


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float,
          color: str = MUTED, dash: str = "", width: float = 2.1) -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"{extra}/>')


def write(name: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")


def estimand_pipeline() -> None:
    lines = begin("一个分数的谱系：从目标总体到决策", "总体、cluster 抽样、运行配置、评分与不确定性流水线。", BLUE)
    stages = [
        (58, 120, 170, "目标总体 P*", "用户 / 题目 / 时间\nestimand θ(c)", BLUE, "#EEF4FC"),
        (260, 120, 170, "抽样单位 U", "user → request\nstrata + cluster", TEAL, "#EAF7F4"),
        (462, 120, 170, "配置 c", "model + prompt\ndecoder + tools", PURPLE, "#F3EFFA"),
        (664, 120, 170, "输出与失败", "Y / timeout / refusal\ntrace + finish reason", AMBER, "#FFF5E7"),
        (866, 120, 170, "评分算子", "parser + reference\nmetric / judge", GREEN, "#EEF7EA"),
    ]
    for x, y, w, title, body, color, fill in stages:
        box(lines, x, y, w, 118, title, body, color, fill)
    for x in (228, 430, 632, 834):
        arrow(lines, x, 179, x + 30, 179)
    text(lines, 52, 292, "同一原始结果，换分母就换问题", INK, 16, "start", 700)
    groups = [(90, 345, "用户 A", 5, 4, BLUE), (90, 455, "用户 B", 1, 0, RED)]
    for x, y, name, n, ok, color in groups:
        text(lines, x, y, name, color, 13, "start", 700)
        for i in range(n):
            lines.append(f'<circle cx="{x+105+i*43}" cy="{y-5}" r="14" fill="{GREEN if i < ok else RED}" opacity=".88"/>')
            text(lines, x+105+i*43, y, "✓" if i < ok else "×", "#FFFFFF", 12, "middle", 700)
    box(lines, 420, 322, 280, 128, "request-micro", "4 / 6 = 0.667\n随机请求的平均表现\n用户 A 权重是 B 的 5 倍", TEAL, "#EAF7F4")
    box(lines, 420, 475, 280, 128, "user-macro", "[(4/5) + (0/1)] / 2 = 0.400\n随机用户的平均表现\n按 user cluster 重采样", PURPLE, "#F3EFFA")
    box(lines, 750, 322, 380, 281, "决策端必须看到的东西", "点估计  θ̂\ncluster-aware interval\n预注册 slices 与 multiplicity\n失败分母和 missingness\n版本差异与预算\n\n结论：0.667 与 0.400 都可算对，\n但它们不回答同一个 estimand。", RED, "#FFF0ED")
    finish(lines, "Benchmark 名称不是 estimand；总体、对象、随机性、独立单位、失败规则和版本共同定义可解释的分数。")
    write("fig-lm-eval-estimand-pipeline-v1.svg", lines)


def metric_anatomy() -> None:
    lines = begin("五把尺测同一答案：匹配单位决定盲区", "EM、token F1、BLEU、ROUGE-L 与 contextual similarity 的对照注解图。", TEAL)
    text(lines, 66, 112, "REFERENCE", MUTED, 11, "start", 700)
    text(lines, 155, 112, "the red fox jumps over the fence", INK, 17, "start", 700)
    text(lines, 66, 154, "CANDIDATE", MUTED, 11, "start", 700)
    text(lines, 155, 154, "a crimson fox leaped over the fence", PURPLE, 17, "start", 700)
    lines.append(f'<line x1="155" y1="169" x2="1090" y2="169" stroke="{GRID}"/>')
    rows = [
        (205, "Exact Match", "整串规范化后完全相同？", "0", RED),
        (280, "Token F1", "多重集合 overlap；同义词仍算错", "P=4/7 · R=4/7", AMBER),
        (355, "BLEU", "modified n-gram precision + BP；偏 precision", "短语重合 / 长度惩罚", BLUE),
        (430, "ROUGE-L", "最长公共子序列；偏 recall 的摘要视角", "LCS = fox over the fence", GREEN),
        (505, "Contextual", "embedding 对齐；允许相似词，但依赖编码器", "red↔crimson · jumps↔leaped", PURPLE),
    ]
    for y, metric, unit, result, color in rows:
        lines.append(f'<rect x="66" y="{y-27}" width="1068" height="58" rx="8" fill="{PAPER}" stroke="{GRID}"/>')
        lines.append(f'<rect x="66" y="{y-27}" width="12" height="58" rx="6" fill="{color}"/>')
        text(lines, 98, y+7, metric, color, 14, "start", 700)
        text(lines, 285, y+7, unit, MUTED, 12.5)
        text(lines, 1096, y+7, result, color, 12.5, "end", 700)
    box(lines, 66, 580, 515, 52, "语料级 ≠ 句级", "BLEU 聚合计数后再取几何平均；不可随意平均句级 BLEU。", BLUE, "#EEF4FC")
    box(lines, 610, 580, 524, 52, "相似 ≠ 正确", "语义指标也可能奖励流畅但事实错误的改写。", RED, "#FFF0ED")
    finish(lines, "先固定 normalization、tokenizer、reference 与聚合层；再把多个指标当诊断向量，而不是挑最高的一把尺。")
    write("fig-lm-eval-metric-anatomy-v1.svg", lines)


def passk_selection() -> None:
    lines = begin("生成覆盖与选择成功：两道门、两个 estimand", "candidate pool、oracle pass@k、selector 与 winner's curse。", PURPLE)
    text(lines, 65, 110, "N = 8 个候选；绿色通过隐藏测试", INK, 15, "start", 700)
    states = [0, 1, 0, 0, 1, 0, 1, 0]
    scores = [.91, .62, .87, .38, .58, .81, .55, .32]
    for i, ok in enumerate(states):
        x = 75 + i * 92
        c = GREEN if ok else RED
        lines.append(f'<rect x="{x}" y="145" width="66" height="72" rx="8" fill="{c}" opacity=".88"/>')
        text(lines, x+33, 175, f"y{i+1}", "#FFFFFF", 12, "middle", 700)
        text(lines, x+33, 199, "PASS" if ok else "FAIL", "#FFFFFF", 10, "middle", 700)
        text(lines, x+33, 240, f"ŝ={scores[i]:.2f}", c, 11, "middle", 700)
    arrow(lines, 820, 182, 885, 182, MUTED)
    box(lines, 900, 125, 235, 130, "selector 取最高 ŝ", "选择 y1：ŝ=.91\n隐藏测试：FAIL\n高噪声分数的极值被放大", RED, "#FFF0ED")
    box(lines, 65, 305, 310, 132, "Oracle coverage", "8 个样本有 c=3 个正确\npass@k = 1 − C(n−c,k)/C(n,k)\n回答：k 个里至少一个正确？", GREEN, "#EEF7EA")
    box(lines, 445, 305, 310, 132, "Selected success", "selector 只返回一个候选\n回答：用户实际拿到正确答案？\n依赖 verifier 的外部验证", PURPLE, "#F3EFFA")
    box(lines, 825, 305, 310, 132, "Budget-matched utility", "质量 − λ·tokens − μ·latency\nN 增大既改覆盖，也改成本\n并可能放大选择偏差", AMBER, "#FFF5E7")
    text(lines, 65, 492, "独立单样本成功率 p=.2 时的理论覆盖", INK, 14, "start", 700)
    x0, y0, ww, hh = 480, 610, 610, 105
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}"/>']
    pts = []
    for k in range(1, 9):
        v = 1 - .8 ** k
        x, y = x0 + (k-1)*ww/7, y0-v*hh
        pts.append((x, y)); lines.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{BLUE}"/>')
        text(lines, x, y0+20, str(k), MUTED, 10, "middle")
    lines.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    text(lines, 282, 552, "1−(1−p)^k", BLUE, 22, "middle", 700)
    text(lines, 282, 581, "只在 iid Bernoulli 理想化下成立", MUTED, 12, "middle")
    finish(lines, "pass@k 是候选池覆盖率，不是部署成功率；若看过测试、judge 或 verifier 后选最佳，还必须审计选择偏差。")
    write("fig-lm-eval-passk-selection-v1.svg", lines)


def calibration_risk() -> None:
    lines = begin("置信度的三次审问：事件、proper loss、选择风险", "reliability diagram、Brier/log loss 与 risk–coverage 曲线。", AMBER)
    # Reliability panel
    text(lines, 80, 110, "A · RELIABILITY", BLUE, 13, "start", 700)
    x0, y0, s = 90, 385, 260
    lines += [f'<rect x="{x0}" y="{y0-s}" width="{s}" height="{s}" fill="{PAPER}" stroke="{GRID}"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0+s}" y2="{y0-s}" stroke="{MUTED}" stroke-dasharray="6 5"/>']
    pts = [(.1,.07),(.3,.18),(.5,.44),(.7,.57),(.9,.76)]
    for conf, acc in pts:
        x, y = x0+conf*s, y0-acc*s
        lines.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{BLUE}"/>')
    text(lines, 220, 410, "mean confidence", MUTED, 11, "middle")
    text(lines, 66, 258, "accuracy", MUTED, 11, "middle")
    text(lines, 220, 445, "点在对角线下：over-confidence", RED, 12, "middle", 700)
    # Proper loss panel
    text(lines, 455, 110, "B · PROPER SCORES", PURPLE, 13, "start", 700)
    box(lines, 445, 125, 300, 122, "Brier", "(p − y)²\n有限且对误差平方惩罚\n多类：Σc(pc−1[y=c])²", TEAL, "#EAF7F4")
    box(lines, 445, 270, 300, 122, "Log loss", "−y log p − (1−y)log(1−p)\n对确信但错误的预测重罚\np=0 且 y=1 → ∞", PURPLE, "#F3EFFA")
    box(lines, 445, 415, 300, 72, "ECE", "描述性分箱摘要；一般不是 proper score，也不唯一。", RED, "#FFF0ED")
    # Risk coverage panel
    text(lines, 825, 110, "C · SELECTIVE GENERATION", GREEN, 13, "start", 700)
    x1, y1, ww, hh = 825, 385, 300, 260
    lines += [f'<rect x="{x1}" y="{y1-hh}" width="{ww}" height="{hh}" fill="{PAPER}" stroke="{GRID}"/>']
    curves = [([(.2,.05),(.4,.08),(.6,.14),(.8,.23),(1,.34)], GREEN),
              ([.2,.4,.6,.8,1], RED)]
    p1 = [(x1+c*ww, y1-r*hh) for c,r in curves[0][0]]
    p2 = [(x1+c*ww, y1-r*hh) for c,r in zip(curves[1][0],[.10,.16,.24,.33,.40])]
    lines.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in p1)}" fill="none" stroke="{GREEN}" stroke-width="4"/>')
    lines.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in p2)}" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="7 5"/>')
    text(lines, 975, 410, "coverage", MUTED, 11, "middle")
    text(lines, 795, 260, "risk", MUTED, 11, "middle")
    text(lines, 978, 446, "排序更好 → 同 coverage 风险更低", GREEN, 12, "middle", 700)
    box(lines, 80, 520, 1045, 100, "先定义概率事件", "“答案正确”“每个 atomic claim 有证据”“调用工具会成功”是不同 Bernoulli 事件；token probability、verbal confidence 与 judge score 不能自动互换。\n校准是相对总体与事件的条件性质；分布、prompt、decoding 或拒答策略改变后必须重新验证。", RED, "#FFF0ED")
    finish(lines, "好 ECE 不推出好决策；同时报告 proper loss、reliability、coverage–risk、分箱规则、失败分母与置信区间。")
    write("fig-lm-eval-calibration-risk-v1.svg", lines)


def factuality_lattice() -> None:
    lines = begin("一个命题的五轴审计：真、知、据、引、推出", "factuality、grounding、citation correctness 与 attribution 的事件晶格。", GREEN)
    box(lines, 55, 105, 290, 118, "回答中的 atomic claim", "c：药物 X 在 2024 年获批用于 Y\n时间切片：as-of t\n断言边界：X / 获批 / Y", BLUE, "#EEF4FC")
    axes = [
        (420, 105, "Truth", "世界在 t 时刻是否使 c 为真？", GREEN),
        (730, 105, "Task knowledge", "reference 是否把 c 设为目标事实？", TEAL),
        (420, 250, "Grounding", "提供的 context 是否支持 c？", BLUE),
        (730, 250, "Citation correctness", "被引片段真的 entail c？", PURPLE),
        (575, 395, "Attribution completeness", "需要证据的 claims 有多少被支持？", AMBER),
    ]
    for x, y, title, body, color in axes:
        box(lines, x, y, 285, 105, title, body, color)
    arrow(lines, 345, 164, 410, 164)
    arrow(lines, 345, 164, 410, 300)
    arrow(lines, 345, 164, 720, 164, MUTED, "6 5")
    arrow(lines, 345, 164, 720, 300, MUTED, "6 5")
    arrow(lines, 562, 355, 655, 392, AMBER)
    arrow(lines, 872, 355, 755, 392, AMBER)
    box(lines, 55, 270, 290, 202, "四个反例足以拆开概念", "① true but uncited\n② false but supported by a bad source\n③ citation relevant but does not entail\n④ all citations correct, yet many claims uncited\n\n所以“有引用”不是事实性证明。", RED, "#FFF0ED")
    text(lines, 55, 525, "两个常被混淆的分母", INK, 15, "start", 700)
    box(lines, 55, 545, 505, 78, "Citation precision", "被检查的 citations 中，有多少真正支持对应 claim？", PURPLE, "#F3EFFA")
    box(lines, 590, 545, 545, 78, "Claim coverage / completeness", "所有需支持 claims 中，有多少至少有一条充分证据？", AMBER, "#FFF5E7")
    finish(lines, "自动 factuality 评估本身也是检索—切分—蕴含判断管线；要保存命题、检索结果、证据 span、判决与不确定性。")
    write("fig-lm-eval-factuality-lattice-v1.svg", lines)


def judge_bias() -> None:
    lines = begin("LLM 裁判审计：交换位置、控制长度、锚定人类", "A/B 与 B/A 交换矩阵、长度 mediator 及人类校验。", RED)
    text(lines, 65, 108, "A · POSITION-SWAP MATRIX", RED, 13, "start", 700)
    text(lines, 110, 165, "presented as", MUTED, 11, "middle")
    text(lines, 205, 165, "judge: A wins", GREEN, 11, "middle", 700)
    text(lines, 325, 165, "judge: B wins", PURPLE, 11, "middle", 700)
    cells = [(150,185,110,70,"AB", "A", GREEN), (270,185,110,70,"AB", "B", RED),
             (150,265,110,70,"BA", "A", RED), (270,265,110,70,"BA", "B", PURPLE)]
    for x,y,w,h,row,out,c in cells:
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" opacity=".86"/>')
        text(lines, x+w/2, y+28, row, "#FFFFFF", 11, "middle", 700)
        text(lines, x+w/2, y+51, f"→ {out}", "#FFFFFF", 13, "middle", 700)
    multi(lines, 65, 385, "一致对：AB 与 BA 都选同一内容\n翻转对：交换位置就换赢家\n位置偏差率要与 tie / parse failure 同报", MUTED, 12.5, 21)
    text(lines, 490, 108, "B · LENGTH AS MEDIATOR", AMBER, 13, "start", 700)
    nodes = [(525,205,"system",BLUE),(700,155,"length",AMBER),(700,285,"quality",GREEN),(920,220,"judge",PURPLE)]
    for x,y,name,c in nodes:
        lines.append(f'<circle cx="{x}" cy="{y}" r="42" fill="{PAPER}" stroke="{c}" stroke-width="3"/>')
        text(lines, x, y+5, name, c, 12, "middle", 700)
    arrow(lines, 567,195,654,165,AMBER); arrow(lines, 567,218,657,274,GREEN)
    arrow(lines, 742,168,878,211,AMBER); arrow(lines, 742,278,878,231,GREEN)
    arrow(lines, 567,205,876,220,MUTED,"6 5")
    multi(lines, 490, 365, "长度可能既承载真实质量，也触发无关偏好。\n简单“扣除长度”可能删掉 treatment effect；\n应报告原始比较、长度匹配/控制比较与假设。", MUTED, 12.5, 21)
    box(lines, 65, 500, 310, 110, "人类锚点", "盲评、随机位置、明确 rubric\n多标注者；保存 disagreement\n分 slice 验证 judge-human agreement", GREEN, "#EEF7EA")
    box(lines, 445, 500, 310, 110, "裁判复现合同", "judge model/date + prompt + order\ntemperature/seed + parser\ntie/refusal/failure rule", BLUE, "#EEF4FC")
    box(lines, 825, 500, 310, 110, "不能泄漏给裁判", "系统名、风格水印、答案顺序\n不可见 reference 选择线索\n用于调 prompt 的 test labels", RED, "#FFF0ED")
    finish(lines, "LLM-as-a-Judge 是带误差和偏差的测量仪器，不是 ground truth；位置、长度、自偏好和样式都需实验审计。")
    write("fig-lm-eval-judge-bias-v1.svg", lines)


def contamination_robustness() -> None:
    lines = begin("污染路径 × Prompt 方差 × 独立单位", "训练暴露、记忆利用、item–prompt 热图与 cluster 区间。", PURPLE)
    text(lines, 60, 108, "A · CONTAMINATION PATH", RED, 13, "start", 700)
    chain = [(60,"公开题库",BLUE),(235,"训练语料",AMBER),(410,"参数记忆",PURPLE),(585,"测试行为",GREEN)]
    for x, title, c in chain:
        box(lines, x, 125, 135, 75, title, "", c)
    for x in (195,370,545): arrow(lines,x,162,x+38,162)
    text(lines, 410, 230, "exposure ≠ memorization ≠ exploitation", RED, 12, "middle", 700)
    text(lines, 60, 290, "B · ITEM × PROMPT SCORE", TEAL, 13, "start", 700)
    vals = [[.9,.4,.7,.8],[.2,.1,.5,.3],[.8,.8,.9,.6],[.4,.7,.2,.5],[.9,.3,.3,.7]]
    for i,row in enumerate(vals):
        text(lines, 65, 340+i*48, f"item {i+1}", MUTED, 11)
        for j,v in enumerate(row):
            c = GREEN if v>=.75 else AMBER if v>=.45 else RED
            x,y = 135+j*75,315+i*48
            lines.append(f'<rect x="{x}" y="{y}" width="62" height="38" rx="5" fill="{c}" opacity="{.35+.6*v:.2f}"/>')
            text(lines,x+31,y+25,f"{v:.1f}",INK,11,"middle",700)
    for j in range(4): text(lines,166+j*75,590,f"p{j+1}",MUTED,11,"middle")
    box(lines, 490, 290, 280, 140, "三种 robustness estimand", "mean over prompt distribution\nworst-case over allowed set\nvariance / quantile across formats\n\n“挑最好模板”是选择过程，不是稳健性。", TEAL, "#EAF7F4")
    box(lines, 490, 455, 280, 140, "不确定性的独立层", "item sampling\nprompt sampling\ngeneration seed\nrun / judge / retriever\n同一 item 的多 prompt 不是独立题。", PURPLE, "#F3EFFA")
    box(lines, 820, 125, 315, 185, "黑箱 canonical-order 信号", "若打乱选择题选项后显著掉分，\n可能提示记住了规范答案位置/字符串；\n但也可能来自位置偏差或格式敏感。\n\n它是诊断信号，不是污染证明。", RED, "#FFF0ED")
    box(lines, 820, 340, 315, 255, "最小稳健性报告", "dataset hash + time cutoff\ndedup / overlap 方法与阈值\n预注册 prompt family\nitem×prompt×seed 原始表\nhierarchical / cluster bootstrap\nmean + worst-case + interval\n失败、污染可疑项与版本变化\n\n外推只覆盖被抽到的模板族与总体。", BLUE, "#EEF4FC")
    finish(lines, "污染检测没有单一完美 oracle；把数据谱系、近似重叠、行为探针和受控重跑作为证据组合，并保留替代解释。")
    write("fig-lm-eval-contamination-robustness-v1.svg", lines)


def evidence_protocol() -> None:
    lines = begin("能力—行为—系统：用 intervention 建证据地图", "四层对象、oracle ladder、metric tree 与上线门。", BLUE)
    text(lines, 58, 108, "A · FOUR LAYERS", BLUE, 13, "start", 700)
    layers = [(58,130,225,"条件模型","NLL / logits / representation",BLUE),(58,225,225,"生成行为","prompt + decoder + seed",PURPLE),
              (58,320,225,"工具系统","retriever / tools / judge",TEAL),(58,415,225,"在线产品","user / load / policy / SLO",RED)]
    for x,y,w,title,body,c in layers: box(lines,x,y,w,70,title,body,c)
    for y in (200,295,390): arrow(lines,170,y,170,y+23)
    text(lines, 340, 108, "B · ORACLE LADDER", GREEN, 13, "start", 700)
    ladder = [(345,440,250,"end-to-end",RED),(385,385,210,"perfect parser",AMBER),(425,330,170,"gold evidence",TEAL),
              (465,275,130,"gold tool",GREEN),(505,220,90,"gold answer",BLUE),(535,165,60,"model",PURPLE)]
    for x,y,w,label,c in ladder:
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="43" rx="5" fill="{c}" opacity=".86"/>')
        text(lines,x+w/2,y+27,label,"#FFFFFF",11,"middle",700)
    multi(lines, 335, 510, "每次只替换一层为 oracle，观察 Δmetric。\n这定位瓶颈，但不假设各层误差可线性相加。", MUTED, 12.5, 21)
    text(lines, 660, 108, "C · METRIC TREE", PURPLE, 13, "start", 700)
    box(lines, 820, 125, 180, 62, "上线决策", "多目标约束", PURPLE, "#F3EFFA")
    branches = [(685,255,"质量","EM / factuality",GREEN),(865,255,"风险","harm / refusal",RED),(1045,255,"系统","latency / cost",BLUE)]
    for x,y,title,body,c in branches:
        arrow(lines,910,187,x,y-12,c); box(lines,x-70,y,140,88,title,body,c)
    leaves = [(640,395,"总体+slice"),(760,395,"CI+effect"),(850,395,"coverage"),(955,395,"severity"),(1040,395,"TTFT/TPOT"),(1120,395,"goodput")]
    for x,y,label in leaves:
        lines.append(f'<circle cx="{x}" cy="{y}" r="35" fill="{PAPER}" stroke="{GRID}" stroke-width="2"/>')
        multi(lines,x,y-3,label,MUTED,10.5,14,"middle",700)
    box(lines, 650, 485, 485, 125, "Decision gate", "先写 non-inferiority / superiority margin 与 SLO；\n再看 paired effect、cluster interval、slice regressions、成本。\n若一个总分掩盖硬约束，保留 metric vector 而不是加权洗平。", RED, "#FFF0ED")
    finish(lines, "证据地图把“测了什么、哪层变了、oracle 是谁、区间多宽、如何决策”连接起来；它不把 benchmark 分数神化为能力本体。")
    write("fig-lm-eval-evidence-protocol-v1.svg", lines)


def main() -> None:
    estimand_pipeline(); metric_anatomy(); passk_selection(); calibration_risk()
    factuality_lattice(); judge_bias(); contamination_robustness(); evidence_protocol()
    print(f"wrote 8 SVGs to {OUT}")


if __name__ == "__main__":
    main()
