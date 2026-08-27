#!/usr/bin/env python3
"""Generate eight varied textbook-style SVGs for LM-65--LM-72."""

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


def text(lines: list[str], x: float, y: float, value: str, color: str = MUTED,
         size: float = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{esc(value)}</text>'
    )


def multi(lines: list[str], x: float, y: float, value: str, color: str = MUTED,
          size: float = 13, leading: float = 20, anchor: str = "start",
          weight: int = 400) -> None:
    for i, row in enumerate(value.split("\n")):
        text(lines, x, y + i * leading, row, color, size, anchor, weight)


def box(lines: list[str], x: float, y: float, w: float, h: float, title: str,
        body: str = "", color: str = BLUE, fill: str = PAPER,
        radius: float = 10) -> None:
    lines.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" stroke="{color}" stroke-width="1.8" filter="url(#shadow)"/>'
    )
    text(lines, x + 15, y + 28, title, color, 15, "start", 700)
    multi(lines, x + 15, y + 52, body, MUTED, 12.2, 19)


def arrow(lines: list[str], x1: float, y1: float, x2: float, y2: float,
          color: str = MUTED, dash: str = "", width: float = 2.1) -> None:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    lines.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"{extra}/>'
    )


def write(name: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")


def memorization_exposure() -> None:
    lines = begin("从 Canary 排名到隐私伤害：Exposure 不是终点",
                  "合成候选排序、Exposure bits 与部署风险漏斗。", AMBER)
    text(lines, 55, 108, "A · 候选空间中的损失排序", BLUE, 13, "start", 700)
    losses = [1.3, 1.8, 2.0, 2.4, 2.6, 2.9, 3.2, 3.4, 3.8, 4.1]
    for i, loss in enumerate(losses):
        y = 140 + i * 37
        c = RED if i == 2 else BLUE
        label = "canary r★" if i == 2 else f"candidate {i+1}"
        text(lines, 55, y + 14, label, c, 11, "start", 700 if i == 2 else 400)
        width = 245 * loss / max(losses)
        lines.append(f'<rect x="155" y="{y}" width="{width:.1f}" height="19" rx="4" fill="{c}" opacity=".82"/>')
        text(lines, 415, y + 14, f"loss {loss:.1f}", MUTED, 10, "end")
    box(lines, 455, 130, 285, 150, "Exposure", "|R| = 2²⁰\nrank(r★) = 2¹⁰\nexposure = log₂|R| − log₂rank\n         = 10 bits", PURPLE, "#F3EFFA")
    box(lines, 455, 310, 285, 120, "Control 必不可少", "同分布未插入字符串\n重复 × prefix × tokenizer 切片\n事前固定候选空间与 tie 规则", TEAL, "#EAF7F4")
    text(lines, 790, 108, "B · 风险漏斗", RED, 13, "start", 700)
    funnels = [
        (790, 135, 330, "训练包含 / 行为影响", BLUE),
        (820, 210, 270, "接口可观察", PURPLE),
        (850, 285, 210, "预算内抽取", AMBER),
        (880, 360, 150, "来源核验", TEAL),
        (910, 435, 90, "实际伤害", RED),
    ]
    for x, y, w, label, c in funnels:
        points = f"{x},{y} {x+w},{y} {x+w-25},{y+56} {x+25},{y+56}"
        lines.append(f'<polygon points="{points}" fill="{c}" opacity=".82"/>')
        text(lines, x + w / 2, y + 34, label, "#FFFFFF", 12, "middle", 700)
    box(lines, 455, 475, 285, 135, "报告合同", "黑/白盒访问 · prefix 知识\nquery/token/人工预算 · 匹配规则\n去重/公开来源核验 · 主体影响\n成功与未成功样本都保留", GREEN, "#EEF7EA")
    finish(lines, "只用合成 canary；高 exposure 说明排序异常，不自动证明黑盒可抽取、来自训练或造成真实隐私伤害。")
    write("fig-lm-safety-memorization-exposure-v1.svg", lines)


def membership_unlearning() -> None:
    lines = begin("成员推断的尾部与 Unlearning 的重训参照",
                  "低 FPR 检验、似然比与删除后分布比较。", PURPLE)
    text(lines, 58, 108, "A · 固定极低 FPR，再读 TPR", PURPLE, 13, "start", 700)
    x0, y0, ww, hh = 70, 400, 480, 235
    lines += [
        f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}"/>',
    ]
    for i in range(101):
        x = x0 + i * ww / 100
        z = (i - 46) / 15
        out = math.exp(-0.5 * z * z)
        zin = (i - 66) / 16
        inside = .9 * math.exp(-0.5 * zin * zin)
        yo = y0 - out * hh * .85
        yi = y0 - inside * hh * .85
        if i == 0:
            po, pi = [f"M{x:.1f},{yo:.1f}"], [f"M{x:.1f},{yi:.1f}"]
        else:
            po.append(f"L{x:.1f},{yo:.1f}")
            pi.append(f"L{x:.1f},{yi:.1f}")
    lines.append(f'<path d="{" ".join(po)}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    lines.append(f'<path d="{" ".join(pi)}" fill="none" stroke="{RED}" stroke-width="3"/>')
    tx = x0 + 78 * ww / 100
    lines.append(f'<line x1="{tx}" y1="{y0}" x2="{tx}" y2="{y0-hh}" stroke="{AMBER}" stroke-width="3" stroke-dasharray="7 5"/>')
    text(lines, tx + 8, y0 - hh + 18, "τ at FPR=α", AMBER, 11, "start", 700)
    text(lines, 160, 155, "non-member score", BLUE, 11, "start", 700)
    text(lines, 365, 155, "member score", RED, 11, "start", 700)
    text(lines, 310, 430, "attack score →", MUTED, 11, "middle")
    box(lines, 70, 470, 480, 135, "基率提醒", "PPV = π·TPR / [π·TPR + (1−π)·FPR]\n成员极罕见时，即使 ROC-AUC 尚可，阳性告警仍可能几乎全是假阳。\n低 FPR 区域需要很大的 non-member 分母。", AMBER, "#FFF5E7")
    text(lines, 610, 108, "B · 删除目标是接近“从未见过”", GREEN, 13, "start", 700)
    centers = [(715, 235, "原模型\nA(D)", RED), (955, 235, "重训参照\nA(D∖R)", GREEN), (835, 430, "unlearned\nU(A(D),R)", PURPLE)]
    for x, y, label, c in centers:
        lines.append(f'<ellipse cx="{x}" cy="{y}" rx="100" ry="65" fill="{c}" opacity=".14" stroke="{c}" stroke-width="3"/>')
        multi(lines, x, y - 5, label, c, 13, 19, "middle", 700)
    arrow(lines, 785, 280, 815, 382, PURPLE)
    arrow(lines, 900, 386, 936, 292, GREEN, "7 5")
    text(lines, 1048, 350, "d(L(U), L(retrain)) ≤ ε", INK, 13, "middle", 700)
    box(lines, 610, 515, 515, 90, "删除 lineage", "raw record → dedup cluster → token shard → checkpoint/adapter → embedding index/cache → served versions；旧副本可访问则删除闭环未完成。", BLUE, "#EEF4FC")
    finish(lines, "一个攻击失效或 benchmark 效用不变都不是删除证明；声明参考重训分布、距离、观察族、失败概率和所有派生副本。")
    write("fig-lm-safety-membership-unlearning-v1.svg", lines)


def injection_boundary() -> None:
    lines = begin("Indirect Prompt Injection：把权限边界放回系统",
                  "Tool-RAG 数据流、信任区与确定性参考监视器。", RED)
    zones = [(45, 100, 310, 520, "不可信区", "#FFF0ED", RED),
             (385, 100, 360, 520, "模型编排区", "#F3EFFA", PURPLE),
             (775, 100, 380, 520, "授权执行区", "#EEF7EA", GREEN)]
    for x, y, w, h, title, fill, c in zones:
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{c}" stroke-width="2"/>')
        text(lines, x + 18, y + 30, title, c, 14, "start", 700)
    box(lines, 75, 155, 245, 80, "用户输入", "可直接控制；身份与会话另验证", RED)
    box(lines, 75, 285, 245, 105, "网页 / 邮件 / RAG 文档", "内容可能含祈使语句\n必须保留 source、trust、timestamp", AMBER)
    box(lines, 75, 450, 245, 80, "工具返回", "数据可再次进入上下文", RED)
    box(lines, 420, 155, 290, 95, "结构化序列化", "role 与 data 标记增强可分性\n不是操作系统式隔离", PURPLE)
    box(lines, 420, 305, 290, 110, "LLM planner", "读取数据并提出 typed action\n模型没有最终 execution authority", BLUE)
    box(lines, 420, 485, 290, 80, "输出/调用提案", "不携带长期凭据", TEAL)
    box(lines, 810, 145, 310, 105, "Reference monitor", "identity · schema · scope · policy\nrate limit · confirmation", GREEN)
    box(lines, 810, 315, 310, 85, "Least-privilege tools", "read/write 分离；短期凭据；sandbox", BLUE)
    box(lines, 810, 465, 310, 105, "审计与回滚", "request/source/bundle/policy IDs\n执行/拒绝都留痕；限制 blast radius", AMBER)
    arrow(lines, 320, 200, 410, 200, MUTED)
    arrow(lines, 320, 335, 410, 335, MUTED)
    arrow(lines, 565, 250, 565, 295, MUTED)
    arrow(lines, 565, 415, 565, 475, MUTED)
    arrow(lines, 710, 525, 800, 210, GREEN)
    arrow(lines, 965, 250, 965, 305, GREEN)
    arrow(lines, 965, 400, 965, 455, GREEN)
    arrow(lines, 810, 355, 720, 355, RED, "7 5")
    text(lines, 760, 340, "结果仍是不可信数据", RED, 10, "middle", 700)
    finish(lines, "Structured prompt 只是一层；真正的安全边界由身份、schema、最小权限、用户确认、沙箱、速率限制和审计共同实现。")
    write("fig-lm-safety-injection-trust-boundary-v1.svg", lines)


def redteam_matrix() -> None:
    lines = begin("安全评估不是一个总分：覆盖 × 判定 × 后果",
                  "红队覆盖矩阵、拒答混淆矩阵与系统严重度。", TEAL)
    text(lines, 55, 105, "A · 红队覆盖矩阵", TEAL, 13, "start", 700)
    cols = ["direct", "obfuscated", "multi-turn", "indirect", "tool"]
    rows = ["privacy", "fraud", "toxicity", "bias", "safety"]
    vals = [
        [1, 1, 0, 1, 0], [1, 1, 1, 0, 1], [1, 1, 1, 0, 0],
        [1, 0, 1, 0, 0], [1, 1, 1, 1, 1],
    ]
    for j, c in enumerate(cols):
        text(lines, 170 + j * 83, 142, c, MUTED, 10, "middle", 700)
    for i, r in enumerate(rows):
        text(lines, 55, 184 + i * 55, r, INK, 11, "start", 700)
        for j, v in enumerate(vals[i]):
            c = TEAL if v else GRID
            lines.append(f'<rect x="{139+j*83}" y="{160+i*55}" width="62" height="40" rx="5" fill="{c}" opacity="{.85 if v else .55}"/>')
            text(lines, 170+j*83, 185+i*55, "tested" if v else "gap", "#FFFFFF" if v else MUTED, 9, "middle", 700)
    box(lines, 55, 465, 500, 135, "覆盖格 ≠ 风险归零", "每格还要写模型/模板/policy、攻击者知识、查询与人工预算、judge/人评、prompt-family cluster、正常效用。\n固定集合通过只支持该版本和该攻击分布。", RED, "#FFF0ED")
    text(lines, 635, 105, "B · Harmful / Benign 两个分母", PURPLE, 13, "start", 700)
    cells = [
        (670, 180, "harmful + refuse", "安全命中", GREEN),
        (885, 180, "harmful + answer", "漏放", RED),
        (670, 300, "benign + refuse", "过度拒答", AMBER),
        (885, 300, "benign + answer", "正常完成", BLUE),
    ]
    for x, y, title, result, c in cells:
        lines.append(f'<rect x="{x}" y="{y}" width="190" height="88" rx="9" fill="{c}" opacity=".84"/>')
        text(lines, x + 95, y + 33, title, "#FFFFFF", 11, "middle", 700)
        text(lines, x + 95, y + 61, result, "#FFFFFF", 16, "middle", 700)
    box(lines, 635, 445, 440, 155, "再接到系统后果", "content property → policy decision → tool/action → impact\n\n毒性低不等于无害；关键词出现不等于攻击成功；模型文字拒答也不保证工具尚未执行。\n同时报告 severity、群体切片和残余风险。", PURPLE, "#F3EFFA")
    finish(lines, "Jailbreak 是攻击过程，toxicity/bias 是行为属性，harm 是情境化后果；测量对象、分母和判定器必须分开。")
    write("fig-lm-safety-redteam-risk-matrix-v1.svg", lines)


def refusal_risk() -> None:
    lines = begin("双阈值拒答：正确性与安全风险不是同一坐标",
                  "五种动作决策面、risk–coverage 与组别 over-refusal。", GREEN)
    text(lines, 55, 105, "A · 决策面", GREEN, 13, "start", 700)
    x0, y0, ww, hh = 70, 430, 450, 290
    lines.append(f'<rect x="{x0}" y="{y0-hh}" width="{ww}" height="{hh}" fill="#EEF4FC" stroke="{GRID}"/>')
    sx, cy = x0 + .62 * ww, y0 - .45 * hh
    lines.append(f'<rect x="{sx}" y="{y0-hh}" width="{x0+ww-sx}" height="{hh*.55}" fill="#EEF7EA" opacity=".95"/>')
    lines.append(f'<rect x="{x0}" y="{y0-hh}" width="{ww}" height="{hh*.28}" fill="#FFF0ED" opacity=".93"/>')
    lines.append(f'<line x1="{sx}" y1="{y0}" x2="{sx}" y2="{y0-hh}" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="7 5"/>')
    lines.append(f'<line x1="{x0}" y1="{cy}" x2="{x0+ww}" y2="{cy}" stroke="{RED}" stroke-width="3" stroke-dasharray="7 5"/>')
    text(lines, 180, 195, "REFUSE / SAFE-COMPLETE", RED, 12, "middle", 700)
    text(lines, 190, 350, "ABSTAIN / ESCALATE", PURPLE, 12, "middle", 700)
    text(lines, 430, 310, "ANSWER", GREEN, 15, "middle", 700)
    text(lines, 295, 458, "correctness confidence →", MUTED, 11, "middle")
    text(lines, 42, 285, "safety risk ↑", MUTED, 11, "middle")
    box(lines, 70, 475, 450, 125, "动作来自代价矩阵", "answer · abstain · refuse · safe-complete · escalate\n知识不足与政策禁止分开；高风险领域需更低容忍、更多人工容量。\n阈值只在 validation 选，test 冻结。", AMBER, "#FFF5E7")
    text(lines, 600, 105, "B · Risk–Coverage 与群体代价", BLUE, 13, "start", 700)
    bx, by, bw, bh = 620, 335, 500, 185
    lines += [f'<line x1="{bx}" y1="{by}" x2="{bx+bw}" y2="{by}" stroke="{INK}"/>',
              f'<line x1="{bx}" y1="{by}" x2="{bx}" y2="{by-bh}" stroke="{INK}"/>']
    curves = [
        ([(.15,.05),(.35,.08),(.55,.13),(.75,.22),(.95,.35)], GREEN, "group A"),
        ([(.10,.09),(.25,.15),(.45,.23),(.65,.32),(.82,.44)], RED, "group B"),
    ]
    for pts, c, label in curves:
        pp = [(bx+x*bw, by-y*bh) for x, y in pts]
        lines.append(f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in pp)}" fill="none" stroke="{c}" stroke-width="4"/>')
        text(lines, pp[-1][0]-5, pp[-1][1]-10, label, c, 11, "end", 700)
    text(lines, 870, 360, "coverage", MUTED, 11, "middle")
    text(lines, 590, 240, "risk", MUTED, 11, "middle")
    box(lines, 620, 390, 500, 210, "同一总体 risk 会隐藏什么", "unsafe answer rate = P(answer | harmful)\nover-refusal = P(refuse | benign)\ncoverage_g、risk_g 与升级延迟必须逐组报告。\n\n低 risk 若靠极低 coverage、对某语言集中拒答或无限人工升级获得，不能描述为“模型更可靠”。", RED, "#FFF0ED")
    finish(lines, "分别校准 correctness 与 safety 事件；同时报告 risk、coverage、over-refusal、群体切片、人工容量和置信上界。")
    write("fig-lm-safety-refusal-risk-coverage-v1.svg", lines)


def version_contract() -> None:
    lines = begin("一次回答的版本 DAG：模型名远远不够",
                  "消息序列化、运行 bundle、内容指纹与四级复现。", BLUE)
    nodes = [
        (55, 120, 180, "messages", "role/content\nraw bytes", BLUE),
        (270, 120, 180, "template", "Jinja + params\nrendered text", PURPLE),
        (485, 120, 180, "tokenizer", "vocab + normalizer\ntoken IDs", TEAL),
        (700, 120, 180, "model + sampler", "weights/adapter/quant\ndecoder + seed", AMBER),
        (915, 120, 220, "system bundle", "retriever/tools/policy\nAPI/time/region", RED),
    ]
    for x, y, w, title, body, c in nodes:
        box(lines, x, y, w, 105, title, body, c)
    for x1, x2 in [(235, 260), (450, 475), (665, 690), (880, 905)]:
        arrow(lines, x1, 172, x2, 172)
    text(lines, 55, 280, "每一层保存实体、版本与输出", INK, 15, "start", 700)
    manifests = [
        (55, 305, "hP", "prompt bytes"),
        (215, 305, "hC", "template"),
        (375, 305, "hT", "token IDs"),
        (535, 305, "hW", "weights"),
        (695, 305, "hD", "decoder"),
        (855, 305, "hG", "tools/policy"),
    ]
    for x, y, hsh, label in manifests:
        lines.append(f'<circle cx="{x+50}" cy="{y+35}" r="34" fill="{PAPER}" stroke="{BLUE}" stroke-width="2"/>')
        text(lines, x+50, y+31, hsh, BLUE, 13, "middle", 700)
        text(lines, x+50, y+50, label, MUTED, 9, "middle")
    arrow(lines, 960, 340, 1060, 340, BLUE)
    box(lines, 1055, 292, 80, 95, "h_run", "bundle\nfingerprint", BLUE, "#EEF4FC")
    text(lines, 55, 430, "四级复现阶梯", INK, 15, "start", 700)
    stages = [
        (55, 470, 230, "R0 · 工件复算", "raw outputs → metrics", GREEN),
        (335, 470, 230, "R1 · 同栈重放", "same bundle + tolerance", TEAL),
        (615, 470, 230, "R2 · 独立重实现", "same protocol, new code", PURPLE),
        (895, 470, 240, "R3 · 外部复验", "new environment/time", RED),
    ]
    for x, y, w, title, body, c in stages:
        box(lines, x, y, w, 105, title, body, c)
    for x in (285, 565, 845):
        arrow(lines, x, 523, x + 40, 523)
    finish(lines, "哈希证明字节身份，不证明正确或安全；API 无法冻结时，记录可观察合同、时间窗口和重复 probe 的分布。")
    write("fig-lm-safety-version-contract-v1.svg", lines)


def monitoring_incident() -> None:
    lines = begin("从线上 SLI 到 Incident：监控必须能触发行动",
                  "五层监控、反馈选择与告警—回滚—复盘时间线。", AMBER)
    text(lines, 55, 105, "A · 五层 SLI 与反馈环", BLUE, 13, "start", 700)
    layers = [
        (55, 140, "Traffic", "language/domain/length", BLUE),
        (245, 140, "RAG / Tools", "freshness/error/denial", TEAL),
        (435, 140, "Behavior", "answer/refuse/policy", PURPLE),
        (625, 140, "Outcome", "completion/escalation", GREEN),
        (815, 140, "Impact", "harm/cost/SLO", RED),
    ]
    for x, y, title, body, c in layers:
        box(lines, x, y, 160, 90, title, body, c)
    for x in (215, 405, 595, 785):
        arrow(lines, x, 185, x + 20, 185)
    arrow(lines, 895, 235, 530, 310, RED, "7 5")
    arrow(lines, 530, 310, 135, 235, RED, "7 5")
    text(lines, 510, 338, "策略改变谁继续使用、谁被标注：observed labels ≠ target population", RED, 11, "middle", 700)
    box(lines, 1010, 135, 125, 105, "SLO", "window + slice\n分母 + CI\nowner + runbook", AMBER, "#FFF5E7")
    text(lines, 55, 385, "B · 一次事故的证据时间线", RED, 13, "start", 700)
    y = 470
    lines.append(f'<line x1="75" y1="{y}" x2="1120" y2="{y}" stroke="{INK}" stroke-width="3"/>')
    events = [
        (120, "deploy", BLUE, "bundle v17"),
        (310, "first bad", RED, "首个受影响请求"),
        (500, "detect", AMBER, "SLI 上界越线"),
        (690, "mitigate", PURPLE, "禁用高权工具"),
        (865, "recover", GREEN, "rollback + verify"),
        (1050, "learn", TEAL, "行动项验收"),
    ]
    for x, title, c, body in events:
        lines.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{c}"/>')
        text(lines, x, y - 25, title, c, 11, "middle", 700)
        text(lines, x, y + 35, body, MUTED, 10, "middle")
    box(lines, 75, 550, 1045, 65, "Postmortem 必须连接证据与责任", "impact · detection gap · timeline · trigger/contributors · logs/replay · mitigation/rollback · owner/deadline · 验收测试；blameless 不等于无责任或无可证伪性。", RED, "#FFF0ED")
    finish(lines, "Drift 指标是告警线索，不是根因；时间线相关也不自动识别因果。回滚优先止损，复盘再用日志、重放和干预更新证据。")
    write("fig-lm-safety-monitoring-incident-v1.svg", lines)


def evidence_card() -> None:
    lines = begin("Claim 不是卡片上的一句话：它是一张可追溯证据图",
                  "Model–Data–System Cards、PROV 血缘与治理闭环。", TEAL)
    cx, cy = 600, 330
    lines.append(f'<circle cx="{cx}" cy="{cy}" r="90" fill="#EEF4FC" stroke="{BLUE}" stroke-width="3"/>')
    text(lines, cx, cy - 18, "CLAIM", BLUE, 18, "middle", 700)
    multi(lines, cx, cy + 8, "对象 · 总体 · 比较\n效应/阈值 · CI · 版本", INK, 11, 17, "middle", 700)
    cards = [
        (80, 115, 260, "MODEL CARD", "weights/tokenizer/template\nintended use · slices · limits", BLUE),
        (470, 95, 260, "DATA CARD", "source/license/subjects\nfilters/dedup/delete/lineage", GREEN),
        (860, 115, 260, "SYSTEM CARD", "RAG/tools/permissions/policy\nSLO/threat/incident", PURPLE),
    ]
    for x, y, w, title, body, c in cards:
        box(lines, x, y, w, 115, title, body, c)
        arrow(lines, x+w/2, y+115, cx, cy-82, c)
    artifacts = [
        (70, 470, 220, "raw traces", "per request / token / tool", TEAL),
        (345, 500, 220, "scores + CI", "parser/judge/version/failures", AMBER),
        (635, 500, 220, "owner + decision", "gate/review/expiry", RED),
        (910, 470, 220, "online evidence", "SLO/drift/incident/rollback", PURPLE),
    ]
    for x, y, w, title, body, c in artifacts:
        box(lines, x, y, w, 100, title, body, c)
        arrow(lines, x+w/2, y, cx, cy+82, c, "7 5")
    text(lines, 600, 455, "PROV: Entity ← Activity ← Agent", INK, 13, "middle", 700)
    lines.append(f'<path d="M1030,465 C1160,365 1120,250 1030,230" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="7 5" marker-end="url(#arrow)"/>')
    text(lines, 1110, 350, "incident 使旧 claim 失效\n并触发下一版协议", RED, 10, "middle", 700)
    finish(lines, "Card 是描述、证据索引与治理接口，不是安全认证；每个主张都应回链原始工件、适用域、版本、负责人和失效条件。")
    write("fig-lm-safety-evidence-card-v1.svg", lines)


def main() -> None:
    memorization_exposure()
    membership_unlearning()
    injection_boundary()
    redteam_matrix()
    refusal_risk()
    version_contract()
    monitoring_incident()
    evidence_card()
    print(f"wrote 8 SVGs to {OUT}")


if __name__ == "__main__":
    main()
