#!/usr/bin/env python3
"""Deterministic numerical oracles for LM-49--LM-56."""

from __future__ import annotations

import csv
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_labs" / "experiments" / "lm70.7-decoding-serving-v1"
W, H = 1200, 700
BG, PAPER, INK, MUTED, GRID = "#FBF8F1", "#FFFDF8", "#183044", "#667784", "#D9D5CB"
BLUE, TEAL, AMBER, RED, PURPLE, GREEN = "#245AA8", "#17766E", "#C87922", "#B7443E", "#7054A3", "#4F7B45"


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(a - b) <= tol


def softmax(z: list[float], tau: float = 1.0) -> list[float]:
    m = max(z)
    w = [math.exp((x - m) / tau) for x in z]
    s = sum(w)
    return [x / s for x in w]


def check(name: str, passed: bool, observed: object, expected: object, note: str) -> dict[str, object]:
    return {"name": name, "passed": bool(passed), "observed": observed, "expected": expected, "note": note}


def svg_begin(title: str, desc: str, accent: str) -> list[str]:
    e = html.escape
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<line x1="50" y1="70" x2="1150" y2="70" stroke="{accent}" stroke-width="4"/>',
        f'<text x="52" y="48" font-size="24" font-weight="700" fill="{INK}">{e(title)}</text>',
    ]


def svg_finish(lines: list[str], footer: str) -> str:
    lines += [
        f'<line x1="50" y1="650" x2="1150" y2="650" stroke="{GRID}"/>',
        f'<text x="52" y="675" font-size="13" fill="{MUTED}">{html.escape(footer)}</text>',
        "</svg>",
    ]
    return "\n".join(lines)


def text(lines: list[str], x: float, y: float, value: object, color: str = MUTED,
         size: float = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(str(value))}</text>')


def decoding_plot(distributions: list[dict[str, object]], supports: dict[str, list[int]]) -> None:
    lines = svg_begin("实验 LM70.7-A：温度分布与截断 support", "由脚本数值输出直接绘制的 softmax 与 support。", BLUE)
    x0, y0, ww, hh = 75, 405, 500, 250
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x0+ww}" y2="{y0}" stroke="{INK}"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hh}" stroke="{INK}"/>']
    colors = [BLUE, TEAL, AMBER]
    for token in range(3):
        pts = []
        for i, row in enumerate(distributions):
            x = x0 + i * ww / (len(distributions)-1)
            y = y0 - float(row["probabilities"][token]) * hh
            pts.append((x, y))
        lines.append(f'<path d="M{" L".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="none" stroke="{colors[token]}" stroke-width="4"/>')
        text(lines, 520, 155+27*token, f"token {token+1}", colors[token], 13, "start", 700)
    for i, row in enumerate(distributions):
        if i % 5 == 0:
            x = x0 + i * ww / (len(distributions)-1)
            text(lines, x, 430, row["temperature"], MUTED, 10, "middle")
    text(lines, 325, 465, "temperature", MUTED, 13, "middle")
    text(lines, 655, 115, "固定概率剖面 p=(.34,.23,.16,.11,.07,.04,.03,.02)", INK, 15, "start", 700)
    rows = [("top-3", supports["top3"], BLUE), ("top-p=.75", supports["top_p_075"], TEAL), ("min-p=.2", supports["min_p_02"], AMBER)]
    for j, (name, ids, color) in enumerate(rows):
        y = 175 + j*125
        text(lines, 655, y, name, color, 14, "start", 700)
        for i in range(8):
            x = 655 + i*56
            fill = color if i in ids else "#E5E2DB"
            lines.append(f'<rect x="{x}" y="{y+20}" width="42" height="42" rx="5" fill="{fill}"/>')
            text(lines, x+21, y+47, f"v{i+1}", "#FFFFFF" if i in ids else MUTED, 11, "middle", 700)
    text(lines, 655, 570, "颜色 = 保留；灰色 = 删除；随后必须重归一化", RED, 13, "start", 700)
    (OUT / "plot-language-decoding-distributions-v1.svg").write_text(
        svg_finish(lines, "曲线与集合均来自 results.json 同一组数值，不代表真实模型质量。"), encoding="utf-8")


def serving_plot(serving_rows: list[dict[str, object]], kv_bytes: int, block_rows: list[dict[str, int]]) -> None:
    lines = svg_begin("实验 LM70.7-B：请求时间线与 KV block 账", "由确定性时间戳和 block 算例生成。", TEAL)
    text(lines, 70, 105, "REQUEST TRACE · milliseconds", MUTED, 11, "start", 700)
    scale, origin = 1.85, 150
    colors = [BLUE, TEAL]
    for j, row in enumerate(serving_rows):
        y = 150 + j*100
        text(lines, 70, y+27, row["request"], colors[j], 13, "start", 700)
        segments = [
            (row["arrival_ms"], row["prefill_start_ms"], "queue", MUTED),
            (row["prefill_start_ms"], row["first_token_ms"], "prefill", BLUE),
            (row["first_token_ms"], row["complete_ms"], "decode", TEAL),
        ]
        for start, end, name, color in segments:
            x = origin + float(start)*scale
            w = (float(end)-float(start))*scale
            lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="45" rx="4" fill="{color}" opacity=".88"/>')
            if w > 70:
                text(lines, x+w/2, y+28, name, "#FFFFFF", 11, "middle", 700)
        text(lines, origin+float(row["first_token_ms"])*scale, y+65, f'TTFT {row["ttft_ms"]} ms', RED, 11, "middle", 700)
    text(lines, 70, 380, f"KV per token = {kv_bytes:,} bytes = 128 KiB", INK, 15, "start", 700)
    x = 70
    colors3 = [BLUE, TEAL, AMBER]
    for j, row in enumerate(block_rows):
        text(lines, x, 425, f'length {row["length"]}', colors3[j], 12, "start", 700)
        for b in range(row["blocks"]):
            lines.append(f'<rect x="{x+b*58}" y="445" width="48" height="65" rx="5" fill="{colors3[j]}" opacity=".88"/>')
            text(lines, x+b*58+24, 483, f"B{b}", "#FFFFFF", 11, "middle", 700)
        text(lines, x, 540, f'blocks {row["blocks"]} · waste {row["waste_tokens"]}', MUTED, 11)
        x += 330
    text(lines, 70, 590, "总 blocks=7；最后块空位=16 tokens。分页降低 max-length 预留，但仍有末块与 metadata 成本。", RED, 13, "start", 700)
    (OUT / "plot-language-serving-trace-v1.svg").write_text(
        svg_finish(lines, "这是时间戳与容量算例；真实 TTFT/TBT 必须在给定 arrival、长度、硬件和 scheduler 下测量。"), encoding="utf-8")


def speculative_plot(p: list[float], q: list[float], accepted: list[float], residual: list[float],
                     configs: list[dict[str, object]]) -> None:
    lines = svg_begin("实验 LM70.7-C：Speculative 质量守恒与 Pareto", "重叠质量、残差与三配置支配关系。", PURPLE)
    x0, width = 75, 470
    colors = [BLUE, TEAL, AMBER]
    for j, (name, vals, y) in enumerate((("target p", p, 125), ("draft q", q, 190), ("accepted mass", accepted, 285), ("residual", residual, 350))):
        pos = x0
        for i, value in enumerate(vals):
            w = width*value
            lines.append(f'<rect x="{pos}" y="{y}" width="{w}" height="42" fill="{colors[i]}" opacity="{1 if j in (0,2) else .65}"/>')
            if w > 35:
                text(lines, pos+w/2, y+27, f"{value:.2f}", "#FFFFFF", 11, "middle", 700)
            pos += w
        text(lines, x0+width+15, y+27, name, MUTED, 12)
    text(lines, 75, 430, "accepted + residual = target tokenwise", GREEN, 14, "start", 700)
    text(lines, 690, 112, "质量 ↑", INK, 14, "start", 700)
    ox, oy, ww, hh = 705, 535, 400, 350
    lines += [f'<line x1="{ox}" y1="{oy}" x2="{ox+ww}" y2="{oy}" stroke="{INK}"/>',
              f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-hh}" stroke="{INK}"/>']
    for row, color in zip(configs, [MUTED, RED, GREEN]):
        x = ox + (float(row["latency_ms"])-90)/40*ww
        y = oy - (float(row["quality"])-.79)/.04*hh
        lines.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{color}"/>')
        text(lines, x+15, y+5, row["name"], color, 12, "start", 700)
    text(lines, ox+ww/2, 575, "p99 latency →", MUTED, 12, "middle")
    text(lines, 705, 615, "C 支配 A/B：质量不低、延迟与成本均不高，至少一项更优。", GREEN, 12.5, "start", 700)
    (OUT / "plot-language-speculative-evidence-v1.svg").write_text(
        svg_finish(lines, "质量守恒是概率恒等式；右侧 Pareto 仅为可复现教学数据，不是引擎 benchmark。"), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, object]] = []

    z = [2.0, 1.0, 0.0]
    p1 = softmax(z)
    shifted = softmax([x+17 for x in z])
    checks.append(check("softmax_shift_temperature", all(close(a,b) for a,b in zip(p1,shifted)) and close(math.exp((z[0]-z[1])/.5), math.exp(2)),
                        {"softmax": p1, "shifted": shifted, "odds_tau_0_5": math.exp(2)},
                        {"shift_invariant": True, "odds_tau_0_5": math.exp(2)}, "LM49"))

    greedy = .6*.5
    global_best = .4*.9
    checks.append(check("greedy_vs_sequence_map", global_best > greedy,
                        {"greedy_Ax": greedy, "global_By": global_best}, {"global_best": "By", "probability": .36}, "LM50"))

    profile = [.34,.23,.16,.11,.07,.04,.03,.02]
    top3 = list(range(3))
    cumulative = 0.0
    top_p = []
    for i, value in enumerate(profile):
        top_p.append(i); cumulative += value
        if cumulative >= .75:
            break
    threshold = .2*max(profile)
    min_p = [i for i,value in enumerate(profile) if value >= threshold]
    supports = {"top3": top3, "top_p_075": top_p, "min_p_02": min_p}
    checks.append(check("truncation_supports", supports == {"top3":[0,1,2],"top_p_075":[0,1,2,3],"min_p_02":[0,1,2,3,4]},
                        supports, {"top3":[0,1,2],"top_p_075":[0,1,2,3],"min_p_02":[0,1,2,3,4]}, "LM51"))

    hazards = [.1,.2,.5]
    survival = [1.0]
    for h in hazards:
        survival.append(survival[-1]*(1-h))
    checks.append(check("eos_survival", all(close(a,b) for a,b in zip(survival,[1,.9,.72,.36])) and close(survival[2]*hazards[2],.36),
                        {"survival":survival,"stop_at_3":survival[2]*hazards[2]}, {"survival":[1,.9,.72,.36],"stop_at_3":.36}, "LM52"))

    raw = {"b":.4,"c":.3,"d":.2,"EOS":.1}
    valid = ["b","c"]
    grammar_z = sum(raw[x] for x in valid)
    constrained = {x:raw[x]/grammar_z for x in valid}
    checks.append(check("grammar_mask", close(grammar_z,.7) and close(constrained["b"],4/7) and close(constrained["c"],3/7),
                        {"valid":valid,"Z":grammar_z,"q":constrained}, {"valid":["b","c"],"Z":.7,"q":{"b":4/7,"c":3/7}}, "LM53"))

    kv_bytes = 32*2*8*128*2
    lengths = [17,32,47]
    block_rows = [{"length":n,"blocks":math.ceil(n/16),"waste_tokens":(16-n%16)%16} for n in lengths]
    checks.append(check("kv_bytes_and_blocks", kv_bytes == 131072 and sum(x["blocks"] for x in block_rows)==7 and sum(x["waste_tokens"] for x in block_rows)==16,
                        {"bytes_per_token":kv_bytes,"rows":block_rows}, {"bytes_per_token":131072,"blocks_total":7,"waste_total":16}, "LM54"))

    p = [.5,.3,.2]; q = [.35,.45,.2]
    accepted = [min(a,b) for a,b in zip(p,q)]
    rejection = 1-sum(accepted)
    residual_raw = [max(a-b,0) for a,b in zip(p,q)]
    residual = [x/rejection for x in residual_raw]
    recovered = [a+rejection*r for a,r in zip(accepted,residual)]
    checks.append(check("speculative_mass_conservation", all(close(a,b) for a,b in zip(recovered,p)) and close(sum(accepted),.85),
                        {"accepted_mass":accepted,"alpha":sum(accepted),"residual":residual,"recovered":recovered},
                        {"alpha":.85,"residual":[1,0,0],"recovered":p}, "LM55"))

    serving_rows = [
        {"request":"R1","arrival_ms":0,"prefill_start_ms":40,"first_token_ms":140,"complete_ms":300},
        {"request":"R2","arrival_ms":50,"prefill_start_ms":130,"first_token_ms":250,"complete_ms":500},
    ]
    for row in serving_rows:
        row["ttft_ms"] = row["first_token_ms"]-row["arrival_ms"]
        row["e2e_ms"] = row["complete_ms"]-row["arrival_ms"]
    goodput = 42/10
    checks.append(check("serving_metrics_and_goodput", serving_rows[0]["ttft_ms"]==140 and serving_rows[1]["ttft_ms"]==200 and close(goodput,4.2),
                        {"requests":serving_rows,"goodput_req_s":goodput}, {"ttft_ms":[140,200],"goodput_req_s":4.2}, "LM56"))

    configs = [
        {"name":"A","quality":.80,"latency_ms":100,"cost":2.0},
        {"name":"B","quality":.82,"latency_ms":120,"cost":2.0},
        {"name":"C","quality":.82,"latency_ms":100,"cost":1.8},
    ]
    def dominates(a: dict[str, object], b: dict[str, object]) -> bool:
        no_worse = a["quality"] >= b["quality"] and a["latency_ms"] <= b["latency_ms"] and a["cost"] <= b["cost"]
        strict = a["quality"] > b["quality"] or a["latency_ms"] < b["latency_ms"] or a["cost"] < b["cost"]
        return bool(no_worse and strict)
    speedup = 30/22
    checks.append(check("pareto_and_speed_model", dominates(configs[2],configs[0]) and dominates(configs[2],configs[1]) and close(speedup,1.3636363636363635),
                        {"C_dominates_A":dominates(configs[2],configs[0]),"C_dominates_B":dominates(configs[2],configs[1]),"speedup":speedup},
                        {"C_dominates_A":True,"C_dominates_B":True,"speedup":30/22}, "LM55-LM56"))

    temperatures = []
    for i in range(21):
        tau = .2 + i*.14
        temperatures.append({"temperature":round(tau,2),"probabilities":softmax(z,tau)})

    with (OUT/"decoding_trace.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.writer(handle); writer.writerow(["temperature","p_token_1","p_token_2","p_token_3"])
        for row in temperatures:
            writer.writerow([row["temperature"],*row["probabilities"]])
    with (OUT/"serving_trace.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(serving_rows[0].keys())); writer.writeheader(); writer.writerows(serving_rows)
    with (OUT/"speculative_trace.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.writer(handle); writer.writerow(["token","target_p","draft_q","accepted_mass","residual_probability","recovered_mass"])
        for i in range(3):
            writer.writerow([i,p[i],q[i],accepted[i],residual[i],recovered[i]])

    results = {
        "experiment_id":"lm70.7-decoding-serving-v1",
        "status":"passed" if all(x["passed"] for x in checks) else "failed",
        "checks_passed":sum(bool(x["passed"]) for x in checks),
        "checks_total":len(checks),
        "checks":checks,
        "determinism":"No model/API/GPU dependency; standard-library arithmetic and SVG only.",
    }
    (OUT/"results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    decoding_plot(temperatures,supports)
    serving_plot(serving_rows,kv_bytes,block_rows)
    speculative_plot(p,q,accepted,residual,configs)
    if results["status"] != "passed":
        raise SystemExit("one or more checks failed")
    print(json.dumps({"status":results["status"],"checks":f'{results["checks_passed"]}/{results["checks_total"]}',"output":str(OUT)},ensure_ascii=False))


if __name__ == "__main__":
    main()
