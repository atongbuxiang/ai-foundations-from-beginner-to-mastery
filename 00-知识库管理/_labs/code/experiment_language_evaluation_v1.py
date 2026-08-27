#!/usr/bin/env python3
"""Deterministic numerical oracles for LM-57--LM-64."""

from __future__ import annotations

import csv
import html
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_labs" / "experiments" / "lm70.8-evaluation-v1"
W, H = 1200, 700
BG, PAPER, INK, MUTED, GRID = "#FBF8F1", "#FFFDF8", "#183044", "#667784", "#D9D5CB"
BLUE, TEAL, AMBER, RED, PURPLE, GREEN = "#245AA8", "#17766E", "#C87922", "#B7443E", "#7054A3", "#4F7B45"


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(a - b) <= tol


def check(name: str, passed: bool, observed: object, expected: object, note: str) -> dict[str, object]:
    return {"name": name, "passed": bool(passed), "observed": observed, "expected": expected, "note": note}


def svg_begin(title: str, desc: str, accent: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<line x1="50" y1="70" x2="1150" y2="70" stroke="{accent}" stroke-width="4"/>',
        f'<text x="52" y="48" font-size="24" font-weight="700" fill="{INK}">{html.escape(title)}</text>',
    ]


def svg_finish(lines: list[str], footer: str) -> str:
    lines += [f'<line x1="50" y1="650" x2="1150" y2="650" stroke="{GRID}"/>',
              f'<text x="52" y="675" font-size="13" fill="{MUTED}">{html.escape(footer)}</text>', "</svg>"]
    return "\n".join(lines)


def text(lines: list[str], x: float, y: float, value: object, color: str = MUTED,
         size: float = 13, anchor: str = "start", weight: int = 400) -> None:
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(str(value))}</text>')


def metrics_plot(summary: dict[str, float], reliability: list[dict[str, float]]) -> None:
    lines = svg_begin("实验 LM70.8-A：分母、指标与校准", "同一脚本生成 macro/micro、文本指标和 reliability 图。", BLUE)
    text(lines, 65, 110, "不同分母", INK, 15, "start", 700)
    bars = [("task-macro", summary["task_macro"], PURPLE), ("example-micro", summary["example_micro"], BLUE),
            ("user-average", summary["user_average"], TEAL), ("request-average", summary["request_average"], AMBER)]
    for i, (name, value, color) in enumerate(bars):
        y = 145 + i * 72
        text(lines, 65, y+24, name, color, 12, "start", 700)
        lines.append(f'<rect x="190" y="{y}" width="{value*380}" height="36" rx="5" fill="{color}" opacity=".88"/>')
        text(lines, 585, y+24, f"{value:.3f}", color, 12, "end", 700)
    text(lines, 65, 475, "词面指标 oracle", INK, 15, "start", 700)
    vals = [("token F1", summary["token_f1"], TEAL), ("BLEU BP", summary["bleu_bp"], AMBER),
            ("ROUGE-L F1", summary["rouge_l_f1"], GREEN)]
    for i, (name, value, color) in enumerate(vals):
        x = 65 + i*175
        lines.append(f'<rect x="{x}" y="{590-value*110}" width="125" height="{value*110}" rx="5" fill="{color}" opacity=".88"/>')
        text(lines, x+62, 615, name, color, 11, "middle", 700)
        text(lines, x+62, 570-value*110, f"{value:.3f}", color, 11, "middle", 700)
    text(lines, 700, 110, "Reliability：conf 与 acc", INK, 15, "start", 700)
    x0, y0, s = 760, 465, 300
    lines += [f'<rect x="{x0}" y="{y0-s}" width="{s}" height="{s}" fill="{PAPER}" stroke="{GRID}"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0+s}" y2="{y0-s}" stroke="{MUTED}" stroke-dasharray="6 5"/>']
    for row in reliability:
        x, y = x0+row["confidence"]*s, y0-row["accuracy"]*s
        lines.append(f'<circle cx="{x}" cy="{y}" r="{7+row["weight"]*9}" fill="{RED}" opacity=".82"/>')
        text(lines, x, y-16, f'n={int(row["n"])}', RED, 10, "middle")
    text(lines, 910, 495, "confidence", MUTED, 11, "middle")
    text(lines, 720, 320, "accuracy", MUTED, 11, "middle")
    text(lines, 760, 545, f'Brier={summary["brier"]:.3f} · ECE={summary["ece"]:.3f}', RED, 14, "start", 700)
    text(lines, 760, 580, "点估计来自教学数组；不代表真实模型已校准", MUTED, 12)
    (OUT / "plot-language-eval-metrics-v1.svg").write_text(
        svg_finish(lines, "Macro/micro、lexical metric 与 calibration 是不同测量对象；图把它们并列而非合成总分。"), encoding="utf-8")


def robustness_plot(prompt_rows: list[dict[str, object]], summary: dict[str, float]) -> None:
    lines = svg_begin("实验 LM70.8-B：Prompt 热图与污染行为探针", "item×prompt scores、均值/worst-case 与 canonical permutation 对照。", PURPLE)
    text(lines, 65, 108, "ITEM × PROMPT", INK, 15, "start", 700)
    for row in prompt_rows:
        i, j, value = int(row["item"]), int(row["prompt"]), float(row["score"])
        x, y = 145+(j-1)*90, 135+(i-1)*62
        color = GREEN if value >= .75 else AMBER if value >= .45 else RED
        lines.append(f'<rect x="{x}" y="{y}" width="74" height="48" rx="6" fill="{color}" opacity="{.35+.6*value:.2f}"/>')
        text(lines, x+37, y+30, f"{value:.1f}", INK, 11, "middle", 700)
        if j == 1:
            text(lines, 70, y+30, f"item {i}", MUTED, 11)
    for j in range(1, 5):
        text(lines, 182+(j-1)*90, 475, f"prompt {j}", MUTED, 10, "middle")
    text(lines, 65, 525, f'prompt mean={summary["prompt_mean"]:.3f} · sd={summary["prompt_sd"]:.3f} · worst={summary["prompt_worst"]:.3f}', TEAL, 13, "start", 700)
    text(lines, 650, 108, "CANONICAL-ORDER PROBE", INK, 15, "start", 700)
    probe = [("canonical", summary["canonical_accuracy"], BLUE), ("permuted", summary["permuted_accuracy"], RED)]
    for i, (name, value, color) in enumerate(probe):
        y = 170+i*130
        text(lines, 650, y+30, name, color, 13, "start", 700)
        lines.append(f'<rect x="770" y="{y}" width="{value*340}" height="48" rx="6" fill="{color}" opacity=".86"/>')
        text(lines, 1120, y+30, f"{value:.2f}", color, 12, "end", 700)
    lines.append(f'<line x1="1040" y1="145" x2="1040" y2="360" stroke="{MUTED}" stroke-dasharray="6 5"/>')
    text(lines, 650, 415, f'drop={summary["canonical_drop"]:.2f}', RED, 17, "start", 700)
    lines.append(f'<rect x="650" y="455" width="485" height="125" rx="9" fill="#FFF0ED" stroke="{RED}"/>')
    text(lines, 670, 490, "诊断边界", RED, 14, "start", 700)
    text(lines, 670, 520, "下降也可能来自位置偏差、格式敏感或 parser；", MUTED, 12)
    text(lines, 670, 545, "它与污染相容，但不是训练 exposure 的充分证明。", MUTED, 12)
    (OUT / "plot-language-eval-robustness-v1.svg").write_text(
        svg_finish(lines, "热图与探针均来自 CSV 教学数据；真实结论需独立 item、预注册模板族、数据谱系与替代解释。"), encoding="utf-8")


def decision_plot(oracle_rows: list[dict[str, object]], slice_rows: list[dict[str, object]],
                  decisions: dict[str, object]) -> None:
    lines = svg_begin("实验 LM70.8-C：Oracle gap、Slice 风险与决策门", "逐层 intervention、失败率和 superiority/non-inferiority。", GREEN)
    text(lines, 65, 108, "ORACLE LADDER", INK, 15, "start", 700)
    colors = [RED, TEAL, GREEN]
    for i, (row, color) in enumerate(zip(oracle_rows, colors)):
        y = 145+i*95
        value = float(row["success"])
        text(lines, 65, y+28, row["layer"], color, 12, "start", 700)
        lines.append(f'<rect x="225" y="{y}" width="{value*430}" height="45" rx="5" fill="{color}" opacity=".86"/>')
        text(lines, 670, y+28, f"{value:.2f}", color, 12, "end", 700)
        if i:
            text(lines, 610, y-15, f'Δ={float(row["gap"]):+.2f}', color, 11, "end", 700)
    text(lines, 65, 470, "SLICE FAILURE", INK, 15, "start", 700)
    for i, row in enumerate(slice_rows):
        x = 80+i*190
        rate = float(row["failure_rate"])
        lines.append(f'<rect x="{x}" y="{610-rate*250}" width="120" height="{rate*250}" rx="5" fill="{RED}" opacity=".82"/>')
        text(lines, x+60, 630, row["slice"], MUTED, 11, "middle")
        text(lines, x+60, 590-rate*250, f'{rate:.0%}', RED, 11, "middle", 700)
    text(lines, 760, 108, "PRE-REGISTERED GATES", INK, 15, "start", 700)
    gates = [("quality superiority", bool(decisions["quality_gate"]), "+1.8 CI [+.4,+3.2]", GREEN),
             ("latency non-inferiority", bool(decisions["latency_gate"]), "+12 CI [−3,+27] ms", RED),
             ("all hard gates", bool(decisions["all_gates"]), "不可用平均总分补偿", RED)]
    for i, (name, passed, detail, color) in enumerate(gates):
        y = 145+i*130
        lines.append(f'<rect x="760" y="{y}" width="375" height="95" rx="9" fill="{"#EEF7EA" if passed else "#FFF0ED"}" stroke="{color}" stroke-width="2"/>')
        text(lines, 785, y+33, "PASS" if passed else "FAIL", color, 14, "start", 700)
        text(lines, 865, y+33, name, INK, 13, "start", 700)
        text(lines, 785, y+65, detail, MUTED, 12)
    text(lines, 760, 565, f'micro failure={float(decisions["micro_failure"]):.3f}', RED, 13, "start", 700)
    text(lines, 760, 592, "总体通过不覆盖小样本高风险 slice。", MUTED, 12)
    (OUT / "plot-language-eval-decision-v1.svg").write_text(
        svg_finish(lines, "Oracle gap 定位当前管线的干预差；决策仍必须逐项满足预注册质量、风险、延迟、成本与 slice 门。"), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, object]] = []

    task_macro = ((20/25)+(3/15))/2
    example_micro = 23/40
    user_average = ((3/4)+0)/2
    request_average = 3/5
    estimands = {"task_macro": task_macro, "example_micro": example_micro,
                 "user_average": user_average, "request_average": request_average}
    checks.append(check("estimand_macro_micro",
                        all(close(estimands[k], v) for k, v in {"task_macro":.5,"example_micro":.575,"user_average":.375,"request_average":.6}.items()),
                        estimands, {"task_macro":.5,"example_micro":.575,"user_average":.375,"request_average":.6}, "LM57"))

    overlap, cand_n, ref_n = 2, 4, 4
    token_f1 = 2*overlap/(cand_n+ref_n)
    bleu_bp = math.exp(1-8/6)
    rouge_l_f1 = 2*3/(5+4)
    metric_values = {"exact_match":0.0,"token_f1":token_f1,"bleu_bp":bleu_bp,"rouge_l_f1":rouge_l_f1}
    checks.append(check("exact_f1_bleu_rouge",
                        close(token_f1,.5) and close(bleu_bp,math.exp(-1/3)) and close(rouge_l_f1,2/3),
                        metric_values, {"exact_match":0.0,"token_f1":.5,"bleu_bp":math.exp(-1/3),"rouge_l_f1":2/3}, "LM58"))

    pass_iid = {k:1-.8**k for k in (1,3,5)}
    pass_comb = 1-math.comb(7,2)/math.comb(10,2)
    checks.append(check("pass_at_k",
                        close(pass_iid[3],.488) and close(pass_iid[5],.67232) and close(pass_comb,24/45),
                        {"iid":pass_iid,"comb_n10_c3_k2":pass_comb}, {"iid_k3":.488,"iid_k5":.67232,"comb":24/45}, "LM59"))

    brier = (.04+.49+.04)/3
    ece = .4*.05+.6*.15
    risks = {".4":0.0,".6":1/3,"1.0":2/5}
    checks.append(check("brier_ece_risk_coverage",
                        close(brier,.19) and close(ece,.11) and close(risks[".6"],1/3),
                        {"brier":brier,"ece":ece,"risks":risks}, {"brier":.19,"ece":.11,"risks":{".4":0,".6":1/3,"1.0":.4}}, "LM60"))

    factual = {"atomic_precision":6/8,"citation_precision":4/5,"claim_coverage":6/10,
               "weighted_precision":(1+2)/(1+3+2)}
    checks.append(check("factuality_citation",
                        close(factual["atomic_precision"],.75) and close(factual["citation_precision"],.8)
                        and close(factual["claim_coverage"],.6) and close(factual["weighted_precision"],.5),
                        factual, {"atomic_precision":.75,"citation_precision":.8,"claim_coverage":.6,"weighted_precision":.5}, "LM61"))

    judge = {"content_consistency":.70,"position_flip":.20,"tie_pair":.10,
             "win_tie_half":(45+10)/100,"win_no_ties":45/80,"agreement":60/80,"chance":.5}
    checks.append(check("judge_swap_winrate",
                        close(judge["win_tie_half"],.55) and close(judge["win_no_ties"],.5625)
                        and close(judge["agreement"],.75),
                        judge, {"consistency":.7,"flip":.2,"win_tie_half":.55,"win_no_ties":.5625,"agreement":.75}, "LM62"))

    canonical, permuted = 80/100, 310/500
    checks.append(check("contamination_permutation",
                        close(canonical,.8) and close(permuted,.62) and close(canonical-permuted,.18),
                        {"canonical":canonical,"permuted":permuted,"drop":canonical-permuted},
                        {"canonical":.8,"permuted":.62,"drop":.18,"interpretation":"diagnostic_not_proof"}, "LM63"))

    prompt_means = [.8,.6,.4]
    prompt_mean = sum(prompt_means)/3
    prompt_sd = math.sqrt(sum((x-prompt_mean)**2 for x in prompt_means)/3)
    # Exact distribution of the mean under three draws with replacement from the prompt family.
    bootstrap_means = [sum(xs)/3 for xs in itertools.product(prompt_means, repeat=3)]
    bootstrap_center = sum(bootstrap_means)/len(bootstrap_means)
    checks.append(check("prompt_variance_bootstrap",
                        close(prompt_mean,.6) and close(prompt_sd,math.sqrt(.08/3)) and close(bootstrap_center,.6),
                        {"mean":prompt_mean,"population_sd":prompt_sd,"range":.4,"worst":.4,
                         "exact_bootstrap_draws":len(bootstrap_means),"bootstrap_mean_center":bootstrap_center},
                        {"mean":.6,"population_sd":math.sqrt(.08/3),"range":.4,"worst":.4,
                         "exact_bootstrap_draws":27,"bootstrap_mean_center":.6}, "LM63"))

    oracle_rows = [
        {"layer":"end-to-end","success":.50,"gap":0.0},
        {"layer":"gold retriever","success":.70,"gap":.20},
        {"layer":"gold tool output","success":.82,"gap":.12},
    ]
    slice_rows = [
        {"slice":"general","n":100,"failures":5,"failure_rate":.05},
        {"slice":"long","n":20,"failures":4,"failure_rate":.20},
        {"slice":"high-risk","n":5,"failures":2,"failure_rate":.40},
    ]
    quality_gate = .4 > 0
    latency_gate = 27 <= 20
    micro_failure = 11/125
    decisions = {"oracle_gaps":[.20,.12],"quality_gate":quality_gate,"latency_gate":latency_gate,
                 "all_gates":quality_gate and latency_gate,"micro_failure":micro_failure}
    checks.append(check("evidence_oracle_decision",
                        close(oracle_rows[1]["gap"],.2) and close(oracle_rows[2]["gap"],.12)
                        and quality_gate and not latency_gate and close(micro_failure,.088),
                        decisions, {"oracle_gaps":[.2,.12],"quality_gate":True,"latency_gate":False,
                                    "all_gates":False,"micro_failure":.088}, "LM64"))

    prompt_matrix = [[.9,.4,.7,.8],[.2,.1,.5,.3],[.8,.8,.9,.6],[.4,.7,.2,.5],[.9,.3,.3,.7]]
    prompt_rows = [{"item":i+1,"prompt":j+1,"score":v} for i,row in enumerate(prompt_matrix) for j,v in enumerate(row)]
    reliability = [{"bin":1,"confidence":.25,"accuracy":.20,"n":40,"weight":.4},
                   {"bin":2,"confidence":.80,"accuracy":.65,"n":60,"weight":.6}]

    with (OUT/"metric_trace.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.writer(handle); writer.writerow(["family","metric","value"])
        for k,v in {**estimands,**metric_values,"brier":brier,"ece":ece,**factual}.items():
            family = "estimand" if k in estimands else "text_metric" if k in metric_values else "calibration" if k in ("brier","ece") else "factuality"
            writer.writerow([family,k,v])
    with (OUT/"robustness_trace.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=["item","prompt","score"]); writer.writeheader(); writer.writerows(prompt_rows)
    with (OUT/"decision_trace.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.writer(handle); writer.writerow(["record_type","name","n","failures","value","gap"])
        for row in oracle_rows:
            writer.writerow(["oracle",row["layer"],"","",row["success"],row["gap"]])
        for row in slice_rows:
            writer.writerow(["slice",row["slice"],row["n"],row["failures"],row["failure_rate"],""])

    summary = {**estimands,**metric_values,"brier":brier,"ece":ece,
               "prompt_mean":prompt_mean,"prompt_sd":prompt_sd,"prompt_worst":min(prompt_means),
               "canonical_accuracy":canonical,"permuted_accuracy":permuted,"canonical_drop":canonical-permuted}
    results = {
        "experiment_id":"lm70.8-evaluation-v1",
        "status":"passed" if all(x["passed"] for x in checks) else "failed",
        "checks_passed":sum(bool(x["passed"]) for x in checks),
        "checks_total":len(checks),
        "checks":checks,
        "determinism":"No model/API/GPU dependency; standard-library arithmetic, exact enumeration, CSV and SVG only.",
    }
    (OUT/"results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    metrics_plot(summary,reliability)
    robustness_plot(prompt_rows,summary)
    decision_plot(oracle_rows,slice_rows,decisions)
    if results["status"] != "passed":
        raise SystemExit("one or more checks failed")
    print(json.dumps({"status":results["status"],"checks":f'{results["checks_passed"]}/{results["checks_total"]}',"output":str(OUT)},ensure_ascii=False))


if __name__ == "__main__":
    main()
