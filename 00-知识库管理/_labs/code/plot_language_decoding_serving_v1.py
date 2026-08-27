#!/usr/bin/env python3
"""Generate eight varied textbook-style SVGs for LM-49--LM-56."""

from __future__ import annotations

import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "figures" / "language-models"
W, H = 1200, 700
BG, PAPER, INK, MUTED, GRID = "#FBF8F1", "#FFFDF8", "#183044", "#667784", "#D9D5CB"
BLUE, TEAL, AMBER, RED, PURPLE, GREEN = "#245AA8", "#17766E", "#C87922", "#B7443E", "#7054A3", "#4F7B45"


def esc(value: object) -> str:
    return html.escape(str(value))


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
    lines += [
        f'<line x1="48" y1="650" x2="1152" y2="650" stroke="{GRID}"/>',
        f'<text x="52" y="674" font-size="13" fill="{MUTED}">{esc(footer)}</text>',
        '</svg>',
    ]


def label(lines: list[str], x: float, y: float, text: str, color: str = MUTED,
          size: float = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>')


def multiline(lines: list[str], x: float, y: float, text: str, color: str = MUTED,
              size: float = 13, leading: float = 20, anchor: str = "start", weight: int = 400) -> None:
    for i, row in enumerate(text.split("\n")):
        label(lines, x, y + i * leading, row, color, size, anchor, weight)


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str,
        body: str = "", color: str = BLUE, fill: str = PAPER, radius: float = 10) -> None:
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{color}" stroke-width="1.8" filter="url(#shadow)"/>')
    label(lines, x + 15, y + 28, title, color, 15, "start", 700)
    multiline(lines, x + 15, y + 53, body, MUTED, 12.5, 20)


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float,
          color: str = MUTED, dash: str = "", width: float = 2.2) -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"{extra}/>')


def write(name: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")


def softmax(values: list[float], tau: float) -> list[float]:
    top = max(values)
    weights = [math.exp((x - top) / tau) for x in values]
    total = sum(weights)
    return [x / total for x in weights]


def temperature_simplex() -> None:
    lines = begin("温度：排名不动，概率质量沿 simplex 移动", "三分类 softmax 随温度变化及 inverse-CDF 采样。", BLUE)
    logits = [2.0, 1.0, 0.0]
    x0, y0, ww, hh = 75, 405, 570, 275
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}" stroke-width="1.7"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}" stroke-width="1.7"/>']
    for j, (idx, color, token) in enumerate(((0, BLUE, "A"), (1, TEAL, "B"), (2, AMBER, "C"))):
        pts = []
        for i in range(81):
            tau = .2 + i * 2.8 / 80
            prob = softmax(logits, tau)[idx]
            pts.append((x0 + i * ww / 80, y0 - prob * hh))
        path = " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        lines.append(f'<path d="M{path}" fill="none" stroke="{color}" stroke-width="3.5"/>')
        label(lines, 530, 145 + 27*j, f"token {token}", color, 13, "start", 700)
    for tau in (.2, 1, 2, 3):
        x = x0 + (tau - .2) / 2.8 * ww
        lines.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+6}" stroke="{INK}"/>')
        label(lines, x, y0 + 24, str(tau), MUTED, 11, "middle")
    label(lines, x0 + ww/2, 452, "temperature τ", MUTED, 13, "middle")
    label(lines, 52, 265, "probability", MUTED, 12, "middle")
    box(lines, 705, 115, 410, 105, "Odds 的精确变化", "pτ(A)/pτ(B) = exp[(zA−zB)/τ]\n有限 τ > 0：A > B > C 的排名不变", PURPLE, "#F3EFFA")
    probs = softmax(logits, 1.0)
    label(lines, 705, 268, "τ = 1 的 categorical 区间", INK, 15, "start", 700)
    bx, by, bw = 705, 292, 410
    colors = [BLUE, TEAL, AMBER]
    pos = bx
    for p, color, token in zip(probs, colors, "ABC"):
        width = bw * p
        lines.append(f'<rect x="{pos}" y="{by}" width="{width}" height="54" fill="{color}"/>')
        label(lines, pos + width/2, by + 33, f"{token} · {p:.3f}", "#FFFFFF", 12, "middle", 700)
        pos += width
    u = .78
    ux = bx + bw * u
    lines += [f'<line x1="{ux}" y1="270" x2="{ux}" y2="365" stroke="{RED}" stroke-width="3"/>',
              f'<path d="M{ux-7},270 L{ux+7},270 L{ux},282 Z" fill="{RED}"/>']
    label(lines, ux, 390, "U=.78 → B", RED, 13, "middle", 700)
    box(lines, 705, 430, 410, 145, "复现合同", "checkpoint + tokenizer/template\nprocessors 与顺序 + sampler\nRNG algorithm/state/counter + scheduler\nstop/parser + kernel/hardware", RED, "#FFF0ED")
    finish(lines, "升温增加 token entropy，不等于增加事实性或语义创造力；seed 也不是完整复现合同。")
    write("fig-lm-decoding-temperature-simplex-v1.svg", lines)


def beam_tree() -> None:
    lines = begin("Beam Search：保留的是前缀，不是未来", "局部累计分、剪枝、完成队列与长度规则。", PURPLE)
    levels = [(120, [("〈BOS〉", 0.0, BLUE)]),
              (290, [("A", -.36, GREEN), ("B", -.51, TEAL), ("C", -1.61, MUTED)]),
              (480, [("A·x", -.87, GREEN), ("A·y", -1.05, AMBER), ("B·z", -.92, TEAL), ("B·x", -1.43, RED)])]
    coords: dict[str, tuple[float, float]] = {}
    for depth, (y, nodes) in enumerate(levels):
        span = 940 if len(nodes) > 1 else 0
        start = 130 if len(nodes) > 1 else 590
        for i, (name, score, color) in enumerate(nodes):
            x = start + (span * i / max(1, len(nodes)-1))
            coords[name] = (x, y)
            lines.append(f'<circle cx="{x}" cy="{y}" r="36" fill="{PAPER}" stroke="{color}" stroke-width="3" filter="url(#shadow)"/>')
            label(lines, x, y-3, name, color, 12.5, "middle", 700)
            label(lines, x, y+17, f"{score:.2f}", MUTED, 11, "middle")
    parent = {"A":"〈BOS〉", "B":"〈BOS〉", "C":"〈BOS〉", "A·x":"A", "A·y":"A", "B·z":"B", "B·x":"B"}
    for child, par in parent.items():
        x1, y1 = coords[par]; x2, y2 = coords[child]
        color = MUTED if child in ("C", "A·y", "B·x") else GREEN
        dash = "6 5" if child in ("C", "A·y", "B·x") else ""
        arrow(lines, x1, y1+37, x2, y2-39, color, dash, 2)
    label(lines, 75, 90, "beam width B = 2", PURPLE, 15, "start", 700)
    label(lines, coords["C"][0], 350, "step 1 剪枝", RED, 12, "middle", 700)
    label(lines, coords["A·y"][0], 545, "step 2 剪枝", RED, 12, "middle", 700)
    label(lines, coords["B·x"][0], 545, "step 2 剪枝", RED, 12, "middle", 700)
    box(lines, 70, 565, 500, 65, "搜索账", "active beams ≠ completed hypotheses；剪掉的未来不可恢复", RED, "#FFF0ED")
    box(lines, 620, 565, 510, 65, "评分账", "raw Σ log p 偏短；length normalization 会重新定义排序目标", BLUE, "#EEF4FC")
    finish(lines, "扩大 beam 改善搜索近似不保证任务质量单调；early-stop 必须有可证的完成上界或明确启发式。")
    write("fig-lm-decoding-beam-tree-v1.svg", lines)


def truncation_profile() -> None:
    lines = begin("四种截断：同一概率剖面的四把尺", "top-k、top-p、locally typical 与 min-p 的候选集合。", AMBER)
    p = [.34, .23, .16, .11, .07, .04, .03, .02]
    colors = [BLUE, TEAL, GREEN, AMBER, PURPLE, RED, MUTED, GRID]
    bx, by, gap = 75, 175, 67
    label(lines, 75, 110, "原始分布 p(v) · 按概率降序", INK, 16, "start", 700)
    for i, value in enumerate(p):
        h = value * 790
        x = bx + i * gap
        lines.append(f'<rect x="{x}" y="{by+270-h}" width="42" height="{h}" rx="4" fill="{colors[i]}"/>')
        label(lines, x+21, by+292, f"v{i+1}", MUTED, 11, "middle")
        label(lines, x+21, by+255-h, f"{value:.2f}", colors[i], 11, "middle", 700)
    panels = [
        (660, 115, "top-k · k=3", "固定保留 3 个最高概率 token", "{v1,v2,v3}", BLUE, "#EEF4FC"),
        (910, 115, "top-p · p=.75", "最小前缀累计质量 ≥ .75", "{v1,v2,v3,v4}", TEAL, "#EAF7F4"),
        (660, 300, "typical · ε", "按 |−log p(v)−H(p)| 接近熵排序", "不是概率排名前缀", PURPLE, "#F3EFFA"),
        (910, 300, "min-p · α=.2", "保留 p(v) ≥ α·max p", "threshold=.068", AMBER, "#FFF5E7"),
    ]
    for x, y, title, body, result, color, fill in panels:
        box(lines, x, y, 220, 145, title, body + "\n\n" + result, color, fill)
    box(lines, 75, 520, 1055, 105, "统一算子", "S(p; λ) → q(v) = p(v)·1[v∈S] / Σu∈S p(u)     ·     support 会随 temperature 与 processor 顺序变化\n方法定义可以精确复现；跨任务的经验优越性必须由预注册对照、足够样本和可靠统计单独支持。", RED, "#FFF0ED")
    finish(lines, "截断删除尾部并重新归一化；它改变 rollout 分布，不是“只把低概率 token 忽略掉”而已。")
    write("fig-lm-decoding-truncation-profile-v1.svg", lines)


def stopping_survival() -> None:
    lines = begin("停止是一组事件：EOS hazard、外部截断与退化循环", "生存概率、finish reason 与重复状态环。", RED)
    hazard = [.08, .12, .20, .18, .35, .60]
    surv = [1.0]
    for h in hazard:
        surv.append(surv[-1] * (1-h))
    x0, y0, ww, hh = 80, 395, 520, 250
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}" stroke-width="1.7"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}" stroke-width="1.7"/>']
    pts = [(x0+i*ww/6, y0-surv[i]*hh) for i in range(7)]
    lines.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{BLUE}" stroke-width="4"/>')
    for i, (x, y) in enumerate(pts):
        lines.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{BLUE}"/>')
        label(lines, x, y-13, f"{surv[i]:.2f}", BLUE, 10.5, "middle")
        label(lines, x, y0+22, str(i), MUTED, 11, "middle")
    label(lines, 80, 112, "S(t)=Πᵢ<t[1−hᵢ]", INK, 16, "start", 700)
    label(lines, 340, 435, "step t", MUTED, 12, "middle")
    box(lines, 675, 105, 450, 150, "五个 finish events", "EOS token · stop string · max_new_tokens\ngrammar accepting state · server cancel/timeout\n必须报告触发者、返回文本是否含标记、是否截在 token 内", RED, "#FFF0ED")
    label(lines, 760, 310, "退化循环不是 EOS 的反义词", INK, 15, "start", 700)
    circle = [(800, 405, "A"), (1010, 405, "B"), (905, 535, "A′")]
    for x, y, name in circle:
        lines.append(f'<circle cx="{x}" cy="{y}" r="44" fill="{PAPER}" stroke="{PURPLE}" stroke-width="3"/>')
        label(lines, x, y+6, name, PURPLE, 17, "middle", 700)
    arrow(lines, 844, 405, 962, 405, PURPLE)
    arrow(lines, 988, 445, 936, 503, PURPLE)
    arrow(lines, 871, 504, 822, 445, PURPLE)
    label(lines, 905, 594, "repetition penalty 改 logits → 改变采样核", AMBER, 12, "middle", 700)
    finish(lines, "训练期 exposure bias、模型概率形状、解码惩罚和服务截断要分账；同一重复现象可有不同原因。")
    write("fig-lm-decoding-stopping-survival-v1.svg", lines)


def prefix_automaton() -> None:
    lines = begin("Grammar decoding：检查可完成前缀，而非只看首字符", "parser state、完整 token 字节转移与语义安全边界。", GREEN)
    states = [(110, 205, "q₀", BLUE), (315, 150, "q₁", TEAL), (525, 205, "q₂", TEAL), (315, 325, "dead", RED)]
    for x, y, name, color in states:
        lines.append(f'<circle cx="{x}" cy="{y}" r="38" fill="{PAPER}" stroke="{color}" stroke-width="3" filter="url(#shadow)"/>')
        label(lines, x, y+6, name, color, 16, "middle", 700)
    arrow(lines, 148, 195, 275, 160, GREEN)
    label(lines, 215, 150, "token '{\"'", GREEN, 11, "middle", 700)
    arrow(lines, 353, 160, 487, 195, GREEN)
    label(lines, 420, 152, "token 'key\"'", GREEN, 11, "middle", 700)
    arrow(lines, 132, 234, 280, 310, RED)
    label(lines, 208, 282, "token '{]'", RED, 11, "middle", 700)
    lines.append(f'<circle cx="{525}" cy="{205}" r="30" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    label(lines, 70, 100, "L：目标语言    Pref(L)：仍可补全为 L 的全部前缀", INK, 15, "start", 700)
    box(lines, 635, 105, 490, 150, "Token-level valid set", "A(q)={v : δ*(q, bytes(v)) 仍可抵达接受态}\nq(v)=p(v)·1[v∈A(q)] / Z\nZ 很小：形式可行，但模型原始合法质量很低", BLUE, "#EEF4FC")
    label(lines, 70, 420, "保证必须分层", INK, 16, "start", 700)
    layers = [(70, 455, 235, "语法", "括号、逗号、枚举", GREEN), (330, 455, 235, "Schema 子集", "类型、required、范围支持", BLUE), (590, 455, 235, "语义", "跨字段关系、事实", AMBER), (850, 455, 275, "权限与副作用", "授权、金额、幂等、沙箱", RED)]
    for x, y, w, title, body, color in layers:
        box(lines, x, y, w, 115, title, body, color)
    label(lines, 187, 607, "约束器可承诺", GREEN, 12, "middle", 700)
    arrow(lines, 300, 604, 845, 604, MUTED, "6 5")
    label(lines, 990, 607, "需独立验证与治理", RED, 12, "middle", 700)
    finish(lines, "语法接受态不证明字段真实、相互一致或工具安全；tokenizer 与 grammar 版本都属于约束合同。")
    write("fig-lm-decoding-prefix-automaton-v1.svg", lines)


def kv_scheduler() -> None:
    lines = begin("LLM Serving：时间轴由调度，显存板由 KV 生命周期", "prefill/decode continuous batching 与 paged KV block table。", TEAL)
    label(lines, 65, 105, "ITERATION SCHEDULER", MUTED, 11, "start", 700)
    xs = [190, 330, 470, 610, 750, 890, 1030]
    for i, x in enumerate(xs):
        label(lines, x, 105, f"iter {i}", MUTED, 10.5, "middle")
        lines.append(f'<line x1="{x}" y1="115" x2="{x}" y2="345" stroke="{GRID}" stroke-dasharray="3 5"/>')
    rows = [(145, "request A", BLUE), (215, "request B", TEAL), (285, "request C", AMBER)]
    for y, name, color in rows:
        label(lines, 65, y+24, name, color, 12.5, "start", 700)
    tasks = [
        (190,145,270,42,"prefill · 512",BLUE),(470,145,105,42,"d1",BLUE),(610,145,105,42,"d2",BLUE),(750,145,105,42,"d3",BLUE),
        (330,215,130,42,"prefill · 64",TEAL),(470,215,105,42,"d1",TEAL),(610,215,105,42,"d2",TEAL),(750,215,105,42,"EOS",TEAL),
        (610,285,270,42,"prefill · 768",AMBER),(890,285,105,42,"d1",AMBER),(1030,285,105,42,"d2",AMBER),
    ]
    for x,y,w,h,t,c in tasks:
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}" opacity=".88"/>')
        label(lines, x+w/2, y+26, t, "#FFFFFF", 11, "middle", 700)
    label(lines, 65, 382, "PAGED KV MEMORY", MUTED, 11, "start", 700)
    colors = [BLUE, TEAL, AMBER]
    names = ["A", "B", "C"]
    positions = [0,1,4,7,2,6,3,9,10,5,8,11]
    for i, slot in enumerate(positions):
        x = 65 + slot * 87
        owner = i % 3
        lines.append(f'<rect x="{x}" y="420" width="70" height="74" rx="5" fill="{colors[owner]}" opacity=".88"/>')
        label(lines, x+35, 447, f"P{slot}", "#FFFFFF", 11, "middle", 700)
        label(lines, x+35, 475, f"{names[owner]}·L{i//3}", "#FFFFFF", 11, "middle", 700)
    box(lines, 65, 530, 320, 90, "KV / token", "L × 2 × nKV × dhead × bytes", BLUE, "#EEF4FC")
    box(lines, 420, 530, 320, 90, "分页缓解", "max-length 预留与外部碎片", TEAL, "#EAF7F4")
    box(lines, 775, 530, 360, 90, "调度权衡", "TTFT ↔ TBT ↔ throughput ↔ KV pressure", RED, "#FFF0ED")
    finish(lines, "FlashAttention 的 attention IO 优化与 persistent KV 容量是两本账；性能数字必须绑定负载与硬件。")
    write("fig-lm-serving-kv-scheduler-v1.svg", lines)


def speculative_waterfall() -> None:
    lines = begin("Speculative sampling：重叠质量被接受，缺口由 residual 补齐", "单步质量恒等式与多 token 首拒绝 waterfall。", PURPLE)
    p = [.50, .30, .20]
    q = [.35, .45, .20]
    x0, width = 80, 460
    label(lines, x0, 108, "单步质量分解", INK, 16, "start", 700)
    for row, (name, vals, y) in enumerate((("target p", p, 145), ("draft q", q, 215))):
        pos = x0
        for value, color, token in zip(vals, [BLUE, TEAL, AMBER], "ABC"):
            w = width * value
            lines.append(f'<rect x="{pos}" y="{y}" width="{w}" height="45" fill="{color}" opacity="{1 if row == 0 else .62}"/>')
            label(lines, pos+w/2, y+28, f"{token} {value:.2f}", "#FFFFFF", 11, "middle", 700)
            pos += w
        label(lines, x0+width+15, y+28, name, MUTED, 12)
    overlap = sum(min(a,b) for a,b in zip(p,q))
    box(lines, 80, 295, 500, 125, "质量恒等式", f"accepted(x)=min[p(x),q(x)]\nresidual(x)=(p(x)−q(x))+\nα=Σ min(p,q)={overlap:.2f}=1−TV(p,q)", GREEN, "#EFF6EA")
    label(lines, 665, 108, "多 token 首拒绝瀑布", INK, 16, "start", 700)
    steps = [(665,145,"x₁","accept · .92",GREEN),(785,225,"x₂","accept · .78",GREEN),(905,305,"x₃","reject · .41",RED),(1025,385,"x₄","discard",MUTED)]
    for i, (x,y,t,b,c) in enumerate(steps):
        lines.append(f'<circle cx="{x}" cy="{y}" r="40" fill="{PAPER}" stroke="{c}" stroke-width="3" filter="url(#shadow)"/>')
        label(lines, x, y-4, t, c, 16, "middle", 700)
        label(lines, x, y+17, b, MUTED, 10.5, "middle")
        if i < len(steps)-1:
            nx, ny = steps[i+1][0], steps[i+1][1]
            arrow(lines, x+34, y+24, nx-34, ny-24, c)
    box(lines, 650, 465, 475, 115, "首次拒绝后的动作", "从该位置 (p−q)+ / R 采一个 token\n丢弃后续 draft；KV 回滚/复用须记录\n若全接受，算法可再提交一个 target bonus token", RED, "#FFF0ED")
    box(lines, 80, 465, 500, 115, "exact 的边界", "保持 target 的输出分布 ≠ 固定 seed 字节一致\nprocessors/support/tokenizer/stop 必须一致\naccept rate ≠ wall-clock speedup", BLUE, "#EEF4FC")
    finish(lines, "分布精确性可由质量守恒证明；系统加速仍取决于 draft 成本、验证形状、batch 和 KV 策略。")
    write("fig-lm-speculative-acceptance-waterfall-v1.svg", lines)


def evidence_map() -> None:
    lines = begin("解码与 Serving 证据地图：对象层、时间线与 Pareto", "model—decoder—server 分层评估及质量—延迟前沿。", BLUE)
    layers = [(65,110,245,95,"RAW MODEL","logits · checkpoint",BLUE,"#EEF4FC"),(65,240,245,115,"DECODER","processors · sampler\nconstraints · RNG · stop",PURPLE,"#F3EFFA"),(65,390,245,125,"SERVER","queue · prefill/decode\nKV · scheduler · hardware",TEAL,"#EAF7F4")]
    for args in layers:
        box(lines, *args)
    arrow(lines, 187, 205, 187, 240, MUTED)
    arrow(lines, 187, 355, 187, 390, MUTED)
    label(lines, 375, 110, "REQUEST TRACE", MUTED, 11, "start", 700)
    stages = [(375,145,105,"queue",MUTED),(480,145,170,"prefill",BLUE),(650,145,90,"d1",TEAL),(740,145,90,"d2",TEAL),(830,145,90,"d3",TEAL),(920,145,125,"post",AMBER)]
    for x,y,w,t,c in stages:
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="48" fill="{c}" opacity=".88"/>')
        label(lines, x+w/2, y+30, t, "#FFFFFF", 11, "middle", 700)
    arrow(lines, 375, 220, 650, 220, RED)
    label(lines, 512, 241, "TTFT", RED, 11, "middle", 700)
    arrow(lines, 650, 260, 920, 260, PURPLE)
    label(lines, 785, 281, "per-token TBT / TPOT", PURPLE, 11, "middle", 700)
    label(lines, 375, 330, "PARETO：质量 ↑，p99 latency →", INK, 14, "start", 700)
    x0,y0,ww,hh=405,570,690,205
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}"/>',f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}"/>']
    points=[(470,520,MUTED,"A"),(560,480,RED,"B"),(650,505,MUTED,"C"),(745,430,TEAL,"D"),(870,390,BLUE,"E"),(1010,405,MUTED,"F")]
    for x,y,c,name in points:
        lines.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>')
        label(lines,x+13,y+4,name,c,11,"start",700)
    lines.append(f'<path d="M560,480 C640,455 690,450 745,430 C810,405 835,398 870,390" fill="none" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="7 5"/>')
    label(lines, 760, 600, "p50 / p95 / p99 · goodput under SLO · memory · cost", MUTED, 12, "middle")
    box(lines, 335, 105, 820, 195, "", "", GRID, "none")
    finish(lines, "同一条输出、同一分布、同 seed 字节复现和同一服务质量是四个不同主张。")
    write("fig-lm-decoding-serving-evidence-map-v1.svg", lines)


def main() -> None:
    temperature_simplex()
    beam_tree()
    truncation_profile()
    stopping_survival()
    prefix_automaton()
    kv_scheduler()
    speculative_waterfall()
    evidence_map()


if __name__ == "__main__":
    main()
