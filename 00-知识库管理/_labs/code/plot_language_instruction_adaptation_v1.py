#!/usr/bin/env python3
"""Generate eight instructional SVGs for LM-25--LM-32."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "figures" / "language-models"
W, H = 1200, 700
BG, INK, MUTED, GRID = "#FFFEFB", "#17324D", "#64748B", "#D7DEE8"
BLUE, TEAL, AMBER, RED, PURPLE = "#2563EB", "#0F766E", "#D97706", "#C24135", "#7C3AED"


def e(value: object) -> str:
    return html.escape(str(value))


def begin(title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#64748B"/></marker><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#17324D" flood-opacity="0.10"/></filter></defs>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>',
        f'<text x="55" y="55" font-size="25" font-weight="700" fill="{BLUE}">{e(title)}</text>',
    ]


def finish(lines: list[str], footer: str) -> None:
    lines += [f'<text x="55" y="670" font-size="14" fill="{MUTED}">{e(footer)}</text>', "</svg>"]


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str, body: str = "", color: str = BLUE, fill: str = "#FFFFFF") -> None:
    lines += [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="2" filter="url(#shadow)"/>',
        f'<text x="{x+16}" y="{y+29}" font-size="16" font-weight="700" fill="{color}">{e(title)}</text>',
    ]
    for index, row in enumerate(body.split("\n")):
        if row:
            lines.append(f'<text x="{x+16}" y="{y+56+index*22}" font-size="13" fill="{MUTED}">{e(row)}</text>')


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float, color: str = MUTED, dash: str = "") -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" marker-end="url(#arrow)"{extra}/>')


def write(name: str, lines: list[str]) -> None:
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")


def chat_template() -> None:
    lines = begin("Chat Template 是编译器：结构化消息必须唯一落到 token 与生成边界", "消息对象经过模板和 tokenizer 形成 input ids，并由训练或生成模式决定后缀。")
    messages = [("system", "You are concise.", PURPLE), ("user", "2+3=?", BLUE), ("assistant", "5", TEAL), ("tool", '{"name":"calc"}', AMBER)]
    for i, (role, content, color) in enumerate(messages):
        y = 115 + i * 82
        lines += [
            f'<rect x="55" y="{y}" width="280" height="62" rx="10" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>',
            f'<rect x="68" y="{y+12}" width="78" height="36" rx="18" fill="{color}"/><text x="107" y="{y+35}" text-anchor="middle" font-size="13" fill="#FFFFFF">{e(role)}</text>',
            f'<text x="160" y="{y+37}" font-size="14" fill="{INK}">{e(content)}</text>',
        ]
    arrow(lines, 350, 280, 405, 280)
    box(lines, 420, 115, 300, 335, "Template source + flags", "Jinja / repository revision\nrole markers + separators\nBOS / EOS policy\nadd_generation_prompt\ncontinue_final_message\ntool schema + escaping", PURPLE, "#F5F3FF")
    arrow(lines, 735, 280, 790, 280)
    box(lines, 805, 115, 340, 150, "Rendered text", "<|system|> ... <eos>\n<|user|> ... <eos>\n<|assistant|>", AMBER, "#FFF7E8")
    box(lines, 805, 300, 340, 150, "Tokenizer output", "input_ids + special token map\nattention relation\nprompt length / generation start", BLUE, "#EFF6FF")
    lines += [
        f'<rect x="420" y="500" width="725" height="115" rx="12" fill="#FEE2E2" stroke="{RED}" stroke-width="2"/>',
        f'<text x="445" y="533" font-size="16" font-weight="700" fill="{RED}">同一消息，不同 template/flag 会成为不同条件事件</text>',
        f'<text x="445" y="566" font-size="14" fill="{INK}">训练：完整 assistant target + loss mask　　推理：只到 assistant generation prefix</text>',
        f'<text x="445" y="594" font-size="14" fill="{MUTED}">必须保存 template bytes、tokenizer hash、flags、最终 IDs 与 generation start。</text>',
    ]
    finish(lines, "消息语义不等于序列语义；可复现对象是 compiler input、compiler version 与 compiler output 的三元组。")
    write("fig-lm-adapt-chat-template-contract-v1.svg", lines)


def sft_loss() -> None:
    lines = begin("SFT 的四张量：输入、shift 后标签、relation 与 loss mask", "同一对话展示 full-sequence loss 与 response-only loss 的差别，并标出 teacher forcing 与自由生成的条件分布差异。")
    tokens = [("<sys>", PURPLE, 0), ("rules", PURPLE, 0), ("<user>", BLUE, 0), ("Q", BLUE, 0), ("<asst>", TEAL, 0), ("A1", TEAL, 1), ("A2", TEAL, 1), ("EOS", TEAL, 1)]
    x0, y0, cell = 55, 125, 118
    lines.append(f'<text x="55" y="102" font-size="17" font-weight="700" fill="{INK}">serialized tokens</text>')
    for i, (token, color, response) in enumerate(tokens):
        x = x0 + i * cell
        lines += [
            f'<rect x="{x}" y="{y0}" width="105" height="48" rx="7" fill="{color}"/>',
            f'<text x="{x+52}" y="{y0+30}" text-anchor="middle" font-size="14" fill="#FFFFFF">{e(token)}</text>',
            f'<text x="{x+52}" y="{y0+77}" text-anchor="middle" font-size="12" fill="{MUTED}">t={i}</text>',
        ]
    rows = [
        ("labels after one shift", ["rules", "<user>", "Q", "<asst>", "A1", "A2", "EOS", "—"], AMBER),
        ("full-sequence mask", ["1", "1", "1", "1", "1", "1", "1", "0"], RED),
        ("response-only mask", ["0", "0", "0", "0", "1", "1", "1", "0"], TEAL),
    ]
    for row_index, (label, values, color) in enumerate(rows):
        y = 245 + row_index * 76
        lines.append(f'<text x="55" y="{y+30}" font-size="14" font-weight="700" fill="{color}">{e(label)}</text>')
        for i, value in enumerate(values):
            x = 260 + i * 102
            fill = color if value == "1" else "#EEF2F7"
            text_color = "#FFFFFF" if value == "1" else INK
            lines += [f'<rect x="{x}" y="{y}" width="88" height="42" rx="6" fill="{fill}"/>', f'<text x="{x+44}" y="{y+27}" text-anchor="middle" font-size="13" fill="{text_color}">{e(value)}</text>']
    box(lines, 55, 500, 500, 115, "Teacher forcing · training", "predict A2 conditioned on gold A1\nparallel shifted targets; exact NLL on chosen mask", TEAL, "#ECFDF5")
    box(lines, 645, 500, 500, 115, "Free running · inference", "predict A2 conditioned on sampled Â1\nerrors alter future history; sampler/stop now matter", RED, "#FEE2E2")
    arrow(lines, 555, 558, 635, 558, RED, "7 5")
    finish(lines, "Response-only 不是自动正确：mask 边界、assistant marker、multi-turn weighting 与 global denominator 都属于目标定义。")
    write("fig-lm-adapt-sft-loss-contract-v1.svg", lines)


def instruction_data() -> None:
    lines = begin("指令数据不是一行 prompt-response：来源、模板、turn 与选择构成经验分布", "展示任务祖先、模板扩展、synthetic teacher、过滤和多轮切分如何共同决定训练份额。")
    stages = [
        (55, 120, "Task ancestors", "dataset / author / license\nbenchmark overlap", BLUE),
        (330, 120, "Templates", "instruction variants\nfew-shot / CoT / locale", PURPLE),
        (605, 120, "Instances", "human / synthetic teacher\ninput + target + metadata", AMBER),
        (880, 120, "Selected examples", "quality / safety / dedup\nturn + target masks", TEAL),
    ]
    for i, (x, y, title, body, color) in enumerate(stages):
        box(lines, x, y, 235, 118, title, body, color)
        if i < len(stages) - 1:
            arrow(lines, x + 235, y + 59, x + 265, y + 59)
    lines += [f'<text x="55" y="300" font-size="18" font-weight="700" fill="{INK}">三种不可合并的权重</text>']
    ledgers = [("task share", 0.55, BLUE), ("conversation share", 0.30, PURPLE), ("assistant target share", 0.72, TEAL)]
    for i, (label, value, color) in enumerate(ledgers):
        y = 335 + i * 62
        lines += [
            f'<text x="65" y="{y+22}" font-size="14" fill="{INK}">{e(label)}</text>',
            f'<rect x="230" y="{y}" width="310" height="30" rx="5" fill="#EEF2F7"/><rect x="230" y="{y}" width="{310*value}" height="30" rx="5" fill="{color}"/>',
            f'<text x="552" y="{y+21}" font-size="14" fill="{color}">{value:.0%}</text>',
        ]
    lines += [
        f'<path d="M930 245 C1120 300,1090 500,880 515" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#arrow)"/>',
        f'<path d="M880 515 C720 555,650 435,700 250" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#arrow)"/>',
        f'<text x="765" y="570" font-size="15" font-weight="700" fill="{RED}">teacher → filter → student → next teacher</text>',
        f'<text x="705" y="600" font-size="13" fill="{MUTED}">self-generation can amplify style, factual and safety selection biases</text>',
    ]
    box(lines, 620, 315, 240, 185, "Multi-turn unit", "turn 1: user → assistant\nturn 2: user → assistant\ndocument-uniform?\nconversation-uniform?\nassistant-target-uniform?", AMBER, "#FFF7E8")
    finish(lines, "数据质量是相对目标的测量问题；必须同时报告 kept 与 rejected pool、teacher version、mixing unit 和有效 targets。")
    write("fig-lm-adapt-instruction-data-bias-v1.svg", lines)


def full_finetune() -> None:
    lines = begin("Fine-tuning 的改变要分参数、函数与能力三层测量", "左侧显示不同可训练参数集合，右侧以新域改善和旧域遗忘的二维平面展示多目标权衡。")
    lines += [f'<text x="55" y="105" font-size="18" font-weight="700" fill="{INK}">1 · trainable-set contract</text>']
    layers = ["embed", "attn-1", "ffn-1", "attn-2", "ffn-2", "head"]
    configs = [("full", [1,1,1,1,1,1], RED), ("freeze lower", [0,0,0,1,1,1], AMBER), ("head only", [0,0,0,0,0,1], BLUE)]
    for r, (name, mask, color) in enumerate(configs):
        y = 140 + r * 88
        lines.append(f'<text x="55" y="{y+29}" font-size="14" font-weight="700" fill="{color}">{e(name)}</text>')
        for i, (layer, active) in enumerate(zip(layers, mask)):
            x = 170 + i * 72
            lines += [
                f'<rect x="{x}" y="{y}" width="62" height="42" rx="6" fill="{color if active else "#EEF2F7"}"/>',
                f'<text x="{x+31}" y="{y+65}" text-anchor="middle" font-size="10" fill="{MUTED}">{e(layer)}</text>',
            ]
    lines += [f'<text x="650" y="105" font-size="18" font-weight="700" fill="{INK}">2 · function-space audit</text>']
    x0, y0, w, h = 690, 435, 420, 285
    lines += [
        f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-h}" stroke="{INK}" stroke-width="2"/>',
        f'<text x="{x0+w-110}" y="{y0+34}" font-size="13" fill="{MUTED}">new-domain gain →</text>',
        f'<text x="{x0-25}" y="{y0-h-15}" font-size="13" fill="{MUTED}">old retention ↑</text>',
    ]
    points = [(735, 220, "base", BLUE), (935, 305, "full FT", RED), (865, 210, "replay", TEAL), (815, 250, "freeze", AMBER)]
    for x, y, label, color in points:
        lines += [f'<circle cx="{x}" cy="{y}" r="12" fill="{color}"/>', f'<text x="{x+16}" y="{y-8}" font-size="14" font-weight="700" fill="{color}">{e(label)}</text>']
    lines += [
        f'<path d="M735 220 C805 245,865 280,935 305" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="7 5"/>',
        f'<rect x="55" y="485" width="545" height="135" rx="12" fill="#F8FAFC" stroke="{GRID}"/>',
        f'<text x="75" y="520" font-size="15" font-weight="700" fill="{INK}">不要用一个数替代三层变化</text>',
        f'<text x="75" y="550" font-size="14" fill="{MUTED}">参数：norm / cosine / layerwise drift</text>',
        f'<text x="75" y="578" font-size="14" fill="{MUTED}">函数：logit KL / representation / calibration</text>',
        f'<text x="75" y="606" font-size="14" fill="{MUTED}">能力：new / old / safety / temporal slices</text>',
    ]
    finish(lines, "冻结参数限制可移动坐标，不自动限制功能变化；遗忘必须由旧能力切片和 matched checkpoint protocol 识别。")
    write("fig-lm-adapt-full-finetune-forgetting-v1.svg", lines)


def lora() -> None:
    lines = begin("LoRA：低秩的是权重增量，初始化决定首步梯度流", "展示 W0 加缩放 BA、矩阵形状、两种常见初始化的首步梯度，以及训练后 merge 等价。")
    box(lines, 55, 115, 270, 150, "Frozen base", "W₀ ∈ Rᵐˣⁿ\nxW₀ remains fixed\nno optimizer state for W₀", BLUE, "#EFF6FF")
    lines += [f'<text x="350" y="195" font-size="30" font-weight="700" fill="{INK}">+</text>']
    box(lines, 405, 115, 350, 150, "Trainable update", "A ∈ Rʳˣⁿ,  B ∈ Rᵐˣʳ\nΔW = sBA, rank(ΔW) ≤ r\nparameters = r(m+n)", PURPLE, "#F5F3FF")
    arrow(lines, 770, 190, 835, 190)
    box(lines, 850, 115, 295, 150, "Forward", "y = x(W₀+sBA)ᵀ\nunmerged: two small matmuls\nmerged: W* = W₀+sBA", TEAL, "#ECFDF5")
    lines += [f'<text x="55" y="325" font-size="18" font-weight="700" fill="{INK}">首步梯度流：零初始化哪一个因子很重要</text>']
    headers = ["initialization", "ΔW at step 0", "gradient to A", "gradient to B"]
    widths = [230, 220, 220, 220]
    tx, ty = 85, 355
    for c, header in enumerate(headers):
        x = tx + sum(widths[:c])
        lines += [f'<rect x="{x}" y="{ty}" width="{widths[c]}" height="45" fill="#EEF2F7" stroke="{GRID}"/>', f'<text x="{x+widths[c]/2}" y="{ty+28}" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}">{e(header)}</text>']
    rows = [
        (("A random, B=0", "0", "0 at first step", "nonzero"), BLUE),
        (("A=0, B random", "0", "nonzero", "0 at first step"), AMBER),
        (("A=0, B=0", "0", "0", "0 · stuck"), RED),
    ]
    for r, (row, row_color) in enumerate(rows):
        y = ty + 45 + r * 55
        for c, value in enumerate(row):
            x = tx + sum(widths[:c])
            lines += [f'<rect x="{x}" y="{y}" width="{widths[c]}" height="50" fill="#FFFFFF" stroke="{GRID}"/>', f'<text x="{x+widths[c]/2}" y="{y+31}" text-anchor="middle" font-size="13" fill="{row_color if c==0 else INK}">{e(value)}</text>']
    lines += [
        f'<rect x="85" y="585" width="890" height="42" rx="8" fill="#ECFDF5" stroke="{TEAL}"/>',
        f'<text x="105" y="611" font-size="14" fill="{TEAL}">Merge oracle: for every x, xW₀ᵀ + s(xAᵀ)Bᵀ = x(W₀+sBA)ᵀ within floating-point tolerance.</text>',
    ]
    finish(lines, "Trainable-parameter ratio 不是总内存或速度比；target modules、rank、scale、dropout、dtype 与 merge status 都要版本化。")
    write("fig-lm-adapt-lora-factorization-v1.svg", lines)


def qlora() -> None:
    lines = begin("QLoRA 显存总账：4-bit 是基座存储格式，不是全部训练状态", "权重从量化存储经反量化参与计算，梯度流向 LoRA；下方用堆叠账本区分持久与峰值内存。")
    box(lines, 55, 115, 245, 125, "4-bit base storage", "quantized blocks q\nscale / zero / metadata\nfrozen parameters", PURPLE, "#F5F3FF")
    arrow(lines, 315, 178, 375, 178)
    box(lines, 390, 115, 245, 125, "Dequantize for compute", "W̃ = dequant(q, scale)\nbf16/fp16 compute tiles\ntemporary buffers", AMBER, "#FFF7E8")
    arrow(lines, 650, 178, 710, 178)
    box(lines, 725, 115, 200, 125, "Forward / backward", "activations\ncheckpointing\nkernel workspace", BLUE, "#EFF6FF")
    arrow(lines, 940, 178, 995, 178)
    box(lines, 1010, 115, 135, 125, "LoRA", "A,B grads\noptimizer\nmaster state", TEAL, "#ECFDF5")
    lines += [f'<path d="M1075 255 C1075 295,520 300,520 255" fill="none" stroke="{TEAL}" stroke-width="3" marker-end="url(#arrow)"/>', f'<text x="780" y="285" text-anchor="middle" font-size="13" fill="{TEAL}">gradient passes through dequantized base; base q is not updated</text>']
    lines += [f'<text x="55" y="345" font-size="18" font-weight="700" fill="{INK}">memory ledger（illustrative, not to scale）</text>']
    ledger = [
        ("quantized base + metadata", 330, PURPLE),
        ("LoRA weights + grads + optimizer", 170, TEAL),
        ("activations / saved tensors", 300, BLUE),
        ("dequant / kernel / allocator peak", 180, AMBER),
    ]
    y = 390
    for label, width, color in ledger:
        lines += [
            f'<text x="55" y="{y+28}" font-size="14" fill="{INK}">{e(label)}</text>',
            f'<rect x="335" y="{y}" width="{width}" height="38" rx="6" fill="{color}"/>',
            f'<text x="{350+width}" y="{y+26}" font-size="13" fill="{color}">{width} relative units</text>',
        ]
        y += 56
    box(lines, 805, 365, 340, 235, "必须记录", "quant format + group size\nquant metadata / double quant\ncompute dtype + accumulation\nLoRA rank / target modules\nsequence / batch / checkpointing\noptimizer + page / offload\nallocated vs reserved vs peak", RED, "#FEE2E2")
    finish(lines, "显存比较必须在同 sequence、batch、checkpointing、kernel 与硬件上测峰值；4-bit 不是自动的 4× 端到端节省。")
    write("fig-lm-adapt-qlora-memory-v1.svg", lines)


def peft_interfaces() -> None:
    lines = begin("PEFT 方法的本质差异：改权重、插模块、加状态，还是缩放激活", "以 Transformer block 为中心标出 Adapter、Prompt、Prefix、IA3 与 LoRA 的注入位置和服务成本。")
    lines += [f'<text x="455" y="100" font-size="18" font-weight="700" fill="{INK}">Frozen Transformer block</text>']
    boxes = [(430, 125, "Attention", BLUE), (430, 275, "FFN", PURPLE), (430, 425, "Residual + output", TEAL)]
    for x, y, label, color in boxes:
        box(lines, x, y, 340, 85, label, "frozen base computation", color)
        if y < 425:
            arrow(lines, 600, y+85, 600, y+140)
    methods = [
        (55, 120, "Prompt tuning", "learn input embeddings\ncontext + prefill cost", BLUE, 430, 155),
        (55, 275, "Prefix tuning", "learn per-layer K/V prefix\nKV + context cost", PURPLE, 430, 190),
        (55, 455, "Adapter", "bottleneck residual module\nextra layer FLOPs", AMBER, 430, 455),
        (825, 120, "LoRA", "low-rank ΔW on chosen linear maps\nmerge may remove latency", TEAL, 770, 165),
        (825, 310, "IA3", "learn vectors that scale K/V/FFN\nchannelwise gates", RED, 770, 320),
    ]
    for x, y, title, body, color, tx, ty in methods:
        box(lines, x, y, 315, 105, title, body, color, "#FFFFFF")
        arrow(lines, x+315 if x<400 else x, y+52, tx, ty, color, "6 4")
    lines += [
        f'<rect x="385" y="560" width="430" height="72" rx="10" fill="#F8FAFC" stroke="{GRID}"/>',
        f'<text x="600" y="586" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">比较轴：trainable params · saved state · extra FLOPs</text>',
        f'<text x="600" y="611" text-anchor="middle" font-size="14" fill="{MUTED}">context/KV · mergeability · task batching · quality frontier</text>',
    ]
    finish(lines, "所有 PEFT 都冻结大部分基座，但它们修改的计算图位置不同；参数少不能直接推出训练快、推理快或效果相同。")
    write("fig-lm-adapt-peft-interface-v1.svg", lines)


def merging() -> None:
    lines = begin("参数合并：Soup、Task Arithmetic 与 TIES 使用相同坐标，却有不同假设", "上方显示共同 base 与 task vectors；下方逐坐标演示 trim、elect sign、merge。")
    box(lines, 55, 110, 220, 95, "Common base θ₀", "same architecture\nsame parameter names\nsame tokenizer", BLUE, "#EFF6FF")
    tasks = [("θ₁=θ₀+τ₁", PURPLE), ("θ₂=θ₀+τ₂", AMBER), ("θ₃=θ₀+τ₃", TEAL)]
    for i, (label, color) in enumerate(tasks):
        x = 370 + i * 260
        box(lines, x, 110, 210, 95, label, "fine-tuned checkpoint", color)
        arrow(lines, 275, 158, x-15, 158, color)
    lines += [
        f'<text x="55" y="265" font-size="16" font-weight="700" fill="{INK}">Soup: Σᵢwᵢθᵢ　　Task arithmetic: θ₀+Σᵢαᵢτᵢ　　TIES: trim → elect sign → aligned merge</text>',
        f'<text x="55" y="315" font-size="18" font-weight="700" fill="{INK}">TIES coordinate toy example</text>',
    ]
    headers = ["coordinate", "τ₁", "τ₂", "τ₃", "after trim", "elected sign", "merged"]
    widths = [120, 100, 100, 100, 180, 160, 150]
    rows = [
        ("j=1", "+.8", "+.6", "-.1", "+.8,+.6,0", "+", "+.7"),
        ("j=2", "-.7", "+.5", "-.6", "-.7,+.5,-.6", "-", "-.65"),
        ("j=3", "+.02", "-.01", "+.03", "0,0,0", "none", "0"),
    ]
    tx, ty = 70, 350
    for c, header in enumerate(headers):
        x = tx + sum(widths[:c])
        lines += [f'<rect x="{x}" y="{ty}" width="{widths[c]}" height="44" fill="#EEF2F7" stroke="{GRID}"/>', f'<text x="{x+widths[c]/2}" y="{ty+27}" text-anchor="middle" font-size="12" font-weight="700" fill="{INK}">{e(header)}</text>']
    for r, row in enumerate(rows):
        y = ty + 44 + r * 58
        for c, value in enumerate(row):
            x = tx + sum(widths[:c])
            color = TEAL if c == 6 else (RED if c == 5 and value == "-" else INK)
            lines += [f'<rect x="{x}" y="{y}" width="{widths[c]}" height="54" fill="#FFFFFF" stroke="{GRID}"/>', f'<text x="{x+widths[c]/2}" y="{y+33}" text-anchor="middle" font-size="13" fill="{color}">{e(value)}</text>']
    lines += [
        f'<rect x="70" y="585" width="1060" height="48" rx="9" fill="#FEE2E2" stroke="{RED}"/>',
        f'<text x="90" y="614" font-size="14" fill="{RED}">Parameter arithmetic is not function arithmetic: validate interpolation barriers, per-task metrics, conflicts, calibration and safety.</text>',
    ]
    finish(lines, "合并报告必须绑定共同 base hash、task-vector construction、density/sign/scale、validation selection 和全部任务切片。")
    write("fig-lm-adapt-merge-ties-v1.svg", lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chat_template()
    sft_loss()
    instruction_data()
    full_finetune()
    lora()
    qlora()
    peft_interfaces()
    merging()
    print("generated 8 figures in", OUT)


if __name__ == "__main__":
    main()
