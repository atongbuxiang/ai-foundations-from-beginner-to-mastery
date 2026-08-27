#!/usr/bin/env python3
"""Standard-library audit for LM-33--LM-40."""

from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_labs" / "experiments" / "lm70.5-icl-reasoning-audit-v1"
PLOTS = ROOT / "_assets" / "plots" / "language-models"
OUT.mkdir(parents=True, exist_ok=True)
PLOTS.mkdir(parents=True, exist_ok=True)
COLORS = {"blue": "#2563EB", "teal": "#0F766E", "amber": "#D97706", "red": "#C24135", "purple": "#7C3AED", "ink": "#17324D", "muted": "#64748B", "grid": "#D7DEE8"}


def byte_ids(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def full_label_score(parts: list[float]) -> float:
    return sum(math.log(p) for p in parts)


def recency_score(order: tuple[int, ...], labels: list[int]) -> int:
    weights = [1, 2, 4, 8]
    return sum(weights[pos] * (1 if labels[item] else -1) for pos, item in enumerate(order))


def bayes_two_tasks(correct_likelihood: float = 0.9) -> tuple[float, float]:
    a = 0.5 * correct_likelihood
    b = 0.5 * (1.0 - correct_likelihood)
    z = a + b
    return a / z, b / z


def induction_next(tokens: list[str], current_index: int) -> str | None:
    current = tokens[current_index]
    for i in range(current_index - 1, -1, -1):
        if tokens[i] == current and i + 1 < current_index:
            return tokens[i + 1]
    return None


def pass_at_k(n: int, c: int, k: int) -> float:
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def svg_begin(title: str, desc: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="0 0 1200 700" role="img" aria-labelledby="title desc">',
        f'<title id="title">{title}</title><desc id="desc">{desc}</desc>',
        '<rect width="1200" height="700" fill="#FFFEFB"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}</style>',
        f'<text x="55" y="55" font-size="25" font-weight="700" fill="{COLORS["blue"]}">{title}</text>',
    ]


def write_svg(name: str, lines: list[str], footer: str) -> None:
    lines += [f'<text x="55" y="670" font-size="14" fill="{COLORS["muted"]}">{footer}</text>', '</svg>']
    (PLOTS / name).write_text("\n".join(lines), encoding="utf-8")


def plot_prompt_order(order_rows: list[dict[str, object]], ids_a: list[int], ids_b: list[int]) -> None:
    lines = svg_begin("LM70.5 实验一：序列差异与顺序敏感性", "两种 prompt 的 byte IDs 与 24 个 demonstration 排列的 recency score。")
    lines += [
        f'<rect x="55" y="95" width="1090" height="120" rx="12" fill="#EFF6FF" stroke="{COLORS["blue"]}"/>',
        f'<text x="75" y="130" font-size="16" font-weight="700" fill="{COLORS["ink"]}">语义近似的两个 prompt</text>',
        f'<text x="75" y="165" font-size="14" fill="{COLORS["teal"]}">A IDs: {ids_a}</text>',
        f'<text x="75" y="195" font-size="14" fill="{COLORS["purple"]}">B IDs: {ids_b}</text>',
        f'<text x="55" y="265" font-size="17" font-weight="700" fill="{COLORS["ink"]}">24 个排列的 recency-weighted label score</text>',
    ]
    scores = [int(r["score"]) for r in order_rows]
    lo, hi = min(scores), max(scores)
    for i, score in enumerate(scores):
        r, c = divmod(i, 8); x, y = 55 + c * 132, 295 + r * 92
        color = COLORS["teal"] if score > 0 else COLORS["red"] if score < 0 else COLORS["amber"]
        width = 35 + 70 * (abs(score) / max(abs(lo), abs(hi)))
        lines += [f'<rect x="{x}" y="{y}" width="110" height="58" rx="7" fill="#F8FAFC" stroke="{COLORS["grid"]}"/>', f'<rect x="{x+5}" y="{y+34}" width="{width:.1f}" height="12" rx="4" fill="{color}"/>', f'<text x="{x+55}" y="{y+24}" text-anchor="middle" font-size="13" fill="{COLORS["ink"]}">π{i+1}: {score:+d}</text>']
    lines += [f'<text x="55" y="610" font-size="14" fill="{COLORS["muted"]}">range = {lo} … {hi}; same demonstrations, different causal sequence</text>']
    write_svg("plot-language-icl-prompt-order-v1.svg", lines, "Toy recency rule is a counterexample to permutation invariance, not a model accuracy claim.")


def plot_theory_mechanism(posterior: tuple[float, float], w_ols: float, w_gd: float, clean: str, corrupt: str) -> None:
    lines = svg_begin("LM70.5 实验二：理论透镜与 induction oracle", "Bayesian posterior、OLS、一步 GD 与重复 token pattern 的可计算结果。")
    panels = [
        (55, "Bayesian posterior", f"p(z=+|D)={posterior[0]:.2f}\np(z=-|D)={posterior[1]:.2f}", COLORS["purple"]),
        (410, "Linear estimator", f"w_OLS={w_ols:.2f}\ny*(x=3)={3*w_ols:.2f}", COLORS["blue"]),
        (765, "One GD step", f"w_1={w_gd:.2f}\ny*(x=3)={3*w_gd:.2f}", COLORS["teal"]),
    ]
    for x,title,body,color in panels:
        lines += [f'<rect x="{x}" y="105" width="320" height="165" rx="12" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>', f'<text x="{x+20}" y="145" font-size="17" font-weight="700" fill="{color}">{title}</text>']
        for i,row in enumerate(body.split("\n")): lines.append(f'<text x="{x+20}" y="{185+i*35}" font-size="16" fill="{COLORS["ink"]}">{row}</text>')
    lines += [f'<text x="55" y="335" font-size="18" font-weight="700" fill="{COLORS["ink"]}">Induction counterfactual</text>']
    cases=[("clean: A B C A →",clean,COLORS["teal"]),("corrupt: A X C A →",corrupt,COLORS["red"])]
    for i,(label,out,color) in enumerate(cases):
        y=380+i*110
        lines += [f'<rect x="85" y="{y}" width="760" height="72" rx="10" fill="#F8FAFC" stroke="{color}" stroke-width="2"/>', f'<text x="115" y="{y+44}" font-size="18" fill="{COLORS["ink"]}">{label}</text>', f'<rect x="865" y="{y}" width="120" height="72" rx="10" fill="{color}"/>', f'<text x="925" y="{y+45}" text-anchor="middle" font-size="22" font-weight="700" fill="#FFFFFF">{out}</text>']
    write_svg("plot-language-icl-theory-mechanism-v1.svg", lines, "Matching toy outputs do not identify a unique mechanism; counterfactuals expose which input relation the rule uses.")


def plot_compute_context(pass_values: list[float], tree_nodes: list[int], context_rows: list[dict[str, object]]) -> None:
    lines = svg_begin("LM70.5 实验三：采样覆盖、搜索规模与有效上下文", "Pass-at-k、完整二叉树节点和最坏位置准确率的三条预算曲线。")
    sections=[(55,115,"pass@k",pass_values,COLORS["teal"]),(425,115,"binary tree nodes",tree_nodes,COLORS["purple"]),(795,115,"worst-position accuracy",[float(r["worst_accuracy"]) for r in context_rows],COLORS["red"])]
    for x,y,title,vals,color in sections:
        lines += [f'<text x="{x}" y="{y}" font-size="17" font-weight="700" fill="{color}">{title}</text>', f'<line x1="{x}" y1="520" x2="{x+300}" y2="520" stroke="{COLORS["ink"]}"/>', f'<line x1="{x}" y1="520" x2="{x}" y2="160" stroke="{COLORS["ink"]}"/>']
        vmax=max(vals); pts=[]
        for i,v in enumerate(vals):
            px=x+30+i*(240/max(1,len(vals)-1)); py=500-310*(v/vmax); pts.append((px,py))
            lines += [f'<circle cx="{px}" cy="{py}" r="6" fill="{color}"/>', f'<text x="{px}" y="{py-12}" text-anchor="middle" font-size="12" fill="{COLORS["muted"]}">{v:.2f}</text>']
        lines.append(f'<path d="M'+' L'.join(f'{a},{b}' for a,b in pts)+'" fill="none" stroke="'+color+'" stroke-width="3"/>')
    lines += [f'<text x="55" y="590" font-size="14" fill="{COLORS["muted"]}">Coverage rises with samples; exhaustive search grows exponentially; effective context can fall with length.</text>']
    write_svg("plot-language-icl-compute-context-v1.svg", lines, "All three x-axes are different resources; they must not be collapsed into one unnamed compute number.")


def main() -> None:
    checks: dict[str, bool] = {}

    prompt_a = "Review: good\nSentiment:"
    prompt_b = "Review: good\nSentiment: "
    ids_a, ids_b = byte_ids(prompt_a), byte_ids(prompt_b)
    fox = full_label_score([0.6, 0.7])
    panda = full_label_score([0.6, 0.2])
    checks["prompt_bytes_ids_and_full_label_score"] = ids_a != ids_b and fox > panda

    labels = [1, 0, 1, 0]
    order_rows = []
    for order in itertools.permutations(range(4)):
        score = recency_score(order, labels)
        order_rows.append({"order": "-".join(map(str, order)), "score": score, "prediction": int(score > 0)})
    checks["demonstration_order_changes_prediction"] = len(order_rows) == 24 and len({r["prediction"] for r in order_rows}) == 2

    base_map = {"positive": "A", "negative": "B"}
    swapped = {"positive": "B", "negative": "A"}
    checks["label_permutation_equivariance_contract"] = base_map["positive"] == "A" and swapped["positive"] == "B" and base_map != swapped

    posterior = bayes_two_tasks(0.9)
    xtx, xty = 5.0, 10.0
    w_ols = xty / xtx
    eta, n = 0.4, 2
    w_gd = eta * xty / n
    checks["bayes_ols_and_one_step_gd_oracles"] = abs(posterior[0] - 0.9) < 1e-12 and w_ols == 2.0 and w_gd == 2.0

    clean = induction_next(["A", "B", "C", "A"], 3)
    corrupt = induction_next(["A", "X", "C", "A"], 3)
    checks["induction_counterfactual"] = clean == "B" and corrupt == "X"

    trace_a = "The first option is supported by the facts."
    trace_b = "The first option is supported by the facts."
    answer_with_cue_a = "A"
    answer_with_cue_b = "B"
    checks["faithfulness_bias_intervention"] = answer_with_cue_a != answer_with_cue_b and trace_a == trace_b and "cue" not in trace_a.lower()

    answers = ["A", "B", "A", "C", "A"]
    majority = max(set(answers), key=lambda a: (answers.count(a), a))
    p53 = pass_at_k(5, 2, 3)
    oracle_coverage = 1
    chosen_success = 0
    regret = oracle_coverage - chosen_success
    checks["sampling_coverage_selection_decomposition"] = majority == "A" and abs(p53 - 0.9) < 1e-12 and regret == 1

    tree_nodes = [2 ** (d + 1) - 1 for d in range(5)]
    cost = {"generated_tokens": 1000, "policy_calls": 15, "verifier_calls": 14, "serial_depth": 3, "peak_states": 8}
    checks["search_tree_and_budget_ledger"] = tree_nodes[3] == 15 and len(cost) == 5

    context_rows = [
        {"length": 8000, "start": 0.93, "middle": 0.90, "end": 0.94, "worst_accuracy": 0.90},
        {"length": 16000, "start": 0.88, "middle": 0.82, "end": 0.90, "worst_accuracy": 0.82},
        {"length": 32000, "start": 0.80, "middle": 0.68, "end": 0.84, "worst_accuracy": 0.68},
    ]
    tau = 0.8
    teff = max(r["length"] for r in context_rows if r["worst_accuracy"] >= tau)
    checks["effective_context_threshold"] = teff == 16000

    with (OUT / "prompt_order.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["order", "score", "prediction"]); w.writeheader(); w.writerows(order_rows)
    with (OUT / "context_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(context_rows[0])); w.writeheader(); w.writerows(context_rows)
    result = {
        "checks": checks,
        "prompt_ids": {"without_trailing_space": ids_a, "with_trailing_space": ids_b},
        "full_label_log_scores": {"red_fox": fox, "red_panda": panda},
        "order_score_range": [min(r["score"] for r in order_rows), max(r["score"] for r in order_rows)],
        "bayesian_posterior": posterior,
        "linear_oracles": {"w_ols": w_ols, "w_one_step_gd": w_gd},
        "induction": {"clean": clean, "corrupt": corrupt},
        "sampling": {"majority": majority, "pass_at_3": p53, "selection_regret": regret},
        "tree_nodes_by_depth": tree_nodes,
        "cost_ledger": cost,
        "effective_context": {"threshold": tau, "tokens": teff},
    }
    (OUT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    plot_prompt_order(order_rows, ids_a, ids_b)
    plot_theory_mechanism(posterior, w_ols, w_gd, clean or "—", corrupt or "—")
    pass_values = [1 - (1 - 0.2) ** k for k in [1, 2, 4, 8, 16]]
    plot_compute_context(pass_values, tree_nodes, context_rows)

    print(json.dumps({"checks": checks, "out": str(OUT), "plots": str(PLOTS)}, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
