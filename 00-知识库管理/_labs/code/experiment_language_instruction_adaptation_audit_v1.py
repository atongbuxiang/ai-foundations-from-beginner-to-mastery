#!/usr/bin/env python3
"""Deterministic standard-library audit for LM-25--LM-32."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "_labs" / "experiments" / "lm70.4-instruction-adaptation-audit-v1"
DEFAULT_PLOTS = ROOT / "_assets" / "plots" / "language-models"
STYLE = '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>'


def compile_chat(include_answer: bool) -> list[str]:
    prefix = ["BOS", "SYSTEM", "s", "EOT", "USER", "q", "EOT", "ASSISTANT"]
    return prefix + (["a", "EOS"] if include_answer else [])


def audit_template() -> dict:
    train = compile_chat(True)
    infer = compile_chat(False)
    return {
        "train": train,
        "infer": infer,
        "answer_start": len(infer),
        "train_prefix": train[: len(infer)],
    }


def audit_sft() -> dict:
    full = ["U", "q", "A", "a", "b", "EOS"]
    inputs, labels = full[:-1], full[1:]
    response_mask = [0, 0, 1, 1, 1]
    devices = [{"N": 12, "D": 6}, {"N": 9, "D": 3}]
    global_mean = sum(row["N"] for row in devices) / sum(row["D"] for row in devices)
    device_mean = sum(row["N"] / row["D"] for row in devices) / len(devices)
    turns = [{"N": 4, "D": 4}, {"N": 6, "D": 2}]
    token_mean = sum(row["N"] for row in turns) / sum(row["D"] for row in turns)
    turn_mean = sum(row["N"] / row["D"] for row in turns) / len(turns)
    return {
        "full": full,
        "inputs": inputs,
        "labels": labels,
        "response_mask": response_mask,
        "effective_targets": sum(response_mask),
        "global_mean": global_mean,
        "equal_device_mean": device_mean,
        "per_token_mean": token_mean,
        "per_turn_mean": turn_mean,
    }


def audit_instruction_distribution() -> dict:
    task_rows = [
        {"task": "A", "draw_share": 0.5, "mean_targets": 20},
        {"task": "B", "draw_share": 0.5, "mean_targets": 80},
    ]
    target_mass = sum(row["draw_share"] * row["mean_targets"] for row in task_rows)
    for row in task_rows:
        row["target_share"] = row["draw_share"] * row["mean_targets"] / target_mass
    select_rows = [
        {"group": "A", "candidate_share": 0.6, "retention": 0.8},
        {"group": "B", "candidate_share": 0.4, "retention": 0.2},
    ]
    kept = sum(row["candidate_share"] * row["retention"] for row in select_rows)
    for row in select_rows:
        row["selected_share"] = row["candidate_share"] * row["retention"] / kept
    return {"tasks": task_rows, "selection": select_rows, "total_retention": kept}


def audit_low_margin() -> dict:
    epsilon = 1e-3
    base_bias = epsilon
    tuned_bias = -epsilon
    margins_before = [base_bias] * 100
    margins_after = [tuned_bias] * 100
    flips = sum((before >= 0) != (after >= 0) for before, after in zip(margins_before, margins_after))
    return {
        "epsilon": epsilon,
        "parameter_change": abs(tuned_bias - base_bias),
        "samples": 100,
        "prediction_flips": flips,
    }


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*matrix)]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def add_matrix(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def scale_matrix(value: float, matrix: list[list[float]]) -> list[list[float]]:
    return [[value * cell for cell in row] for row in matrix]


def audit_lora() -> dict:
    base = [[1.0, 0.0], [0.0, 1.0]]
    a = [[1.0, 0.0], [0.0, 1.0]]
    b = [[2.0, 0.0], [0.0, 3.0]]
    scale = 0.5
    delta = scale_matrix(scale, matmul(b, a))
    x = [1.0, 2.0]
    unmerged = [
        left + right
        for left, right in zip(matvec(base, x), matvec(delta, x))
    ]
    merged = matvec(add_matrix(base, delta), x)
    zero_b = [[0.0, 0.0], [0.0, 0.0]]
    g = [[1.0, 2.0], [3.0, 4.0]]
    grad_b = scale_matrix(scale, matmul(g, transpose(a)))
    grad_a = scale_matrix(scale, matmul(transpose(zero_b), g))
    return {
        "base": base,
        "A": a,
        "B": b,
        "scale": scale,
        "delta": delta,
        "x": x,
        "unmerged_output": unmerged,
        "merged_output": merged,
        "grad_B_when_B_zero": grad_b,
        "grad_A_when_B_zero": grad_a,
    }


def audit_qlora_memory() -> dict:
    rows = [
        {"item": "4bit_codes", "gb": 0.50},
        {"item": "quant_metadata", "gb": 0.10},
        {"item": "adapter_states", "gb": 0.12},
        {"item": "activations", "gb": 1.40},
        {"item": "temporary", "gb": 0.50},
    ]
    return {"rows": rows, "accounted_sum_gb": sum(row["gb"] for row in rows)}


def audit_peft_counts() -> dict:
    d, layers, prompt, rank = 100, 4, 5, 2
    return {
        "d": d,
        "layers": layers,
        "prompt_length": prompt,
        "rank": rank,
        "prompt_parameters": prompt * d,
        "prefix_kv_parameters": 2 * layers * prompt * d,
        "adapter_parameters": 2 * layers * d * rank,
    }


def audit_merging() -> dict:
    theta0 = [1.0, 1.0]
    theta1 = [2.0, 0.0]
    theta2 = [1.0, 3.0]
    soup = [(left + right) / 2 for left, right in zip(theta1, theta2)]
    tau1 = [value - base for value, base in zip(theta1, theta0)]
    tau2 = [value - base for value, base in zip(theta2, theta0)]
    task_sum = [base + left + right for base, left, right in zip(theta0, tau1, tau2)]

    def ties(values: list[float], threshold: float) -> dict:
        trimmed = [value if abs(value) >= threshold else 0.0 for value in values]
        elected = 1 if sum(trimmed) > 0 else (-1 if sum(trimmed) < 0 else 0)
        aligned = [value for value in trimmed if value != 0 and int(math.copysign(1, value)) == elected]
        merged = sum(aligned) / len(aligned) if aligned else 0.0
        return {"raw": values, "trimmed": trimmed, "elected_sign": elected, "aligned": aligned, "merged": merged}

    ties_positive = ties([0.8, 0.6, -0.1], 0.2)
    ties_negative = ties([-0.7, 0.5, -0.6], 0.2)

    # Two hidden linear units, one model is a permutation of the other.
    w_a, v_a = [1.0, -1.0], [1.0, -1.0]
    w_b, v_b = [-1.0, 1.0], [-1.0, 1.0]
    x = 3.0
    f_a = sum(v * w * x for v, w in zip(v_a, w_a))
    f_b = sum(v * w * x for v, w in zip(v_b, w_b))
    w_avg = [(left + right) / 2 for left, right in zip(w_a, w_b)]
    v_avg = [(left + right) / 2 for left, right in zip(v_a, v_b)]
    f_avg = sum(v * w * x for v, w in zip(v_avg, w_avg))
    return {
        "theta0": theta0,
        "theta1": theta1,
        "theta2": theta2,
        "uniform_soup": soup,
        "tau1": tau1,
        "tau2": tau2,
        "task_vector_sum": task_sum,
        "ties_positive": ties_positive,
        "ties_negative": ties_negative,
        "permutation_counterexample": {"f_a": f_a, "f_b": f_b, "f_average": f_avg},
    }


def esc(value: object) -> str:
    return html.escape(str(value))


def svg_begin(title: str, desc: str, height: int = 700) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
        f'<rect width="1200" height="{height}" fill="#FFFEFB"/>',
        STYLE,
    ]


def write_contract_svg(path: Path, template: dict, sft: dict) -> None:
    colors = {"BOS": "#7C3AED", "SYSTEM": "#7C3AED", "s": "#7C3AED", "EOT": "#94A3B8", "USER": "#2563EB", "q": "#2563EB", "ASSISTANT": "#0F766E", "a": "#0F766E", "EOS": "#0F766E"}
    lines = svg_begin("Template prefix and SFT loss are one executable contract", "Train and inference prefixes are aligned above; shifted labels and response mask are aligned below.")
    lines += [
        '<text x="55" y="55" font-size="25" font-weight="700" fill="#17324D">Template prefix and SFT target must agree token by token</text>',
        '<text x="55" y="105" font-size="18" font-weight="700" fill="#17324D">1 · train sequence; red divider = generation / answer start</text>',
    ]
    x0, cell = 55, 105
    for i, token in enumerate(template["train"]):
        x = x0 + i * cell
        lines += [
            f'<rect x="{x}" y="135" width="94" height="46" rx="6" fill="{colors[token]}"/>',
            f'<text x="{x+47}" y="164" text-anchor="middle" font-size="12" fill="#FFFFFF">{esc(token)}</text>',
        ]
    divider = x0 + template["answer_start"] * cell - 6
    lines += [
        f'<line x1="{divider}" y1="120" x2="{divider}" y2="215" stroke="#C24135" stroke-width="4" stroke-dasharray="7 5"/>',
        '<text x="55" y="225" font-size="14" fill="#0F766E">inference sequence is exactly the prefix left of the divider</text>',
        '<text x="55" y="295" font-size="18" font-weight="700" fill="#17324D">2 · one shift, then choose the response targets</text>',
    ]
    labels = ["q", "A", "a", "b", "EOS"]
    inputs = ["U", "q", "A", "a", "b"]
    mask = sft["response_mask"]
    for i, (inp, label, score) in enumerate(zip(inputs, labels, mask)):
        x = 180 + i * 170
        lines += [
            f'<rect x="{x}" y="335" width="125" height="42" rx="6" fill="#DBEAFE"/><text x="{x+62}" y="362" text-anchor="middle" font-size="14">input {inp}</text>',
            f'<rect x="{x}" y="392" width="125" height="42" rx="6" fill="#FEF3C7"/><text x="{x+62}" y="419" text-anchor="middle" font-size="14">label {label}</text>',
            f'<rect x="{x}" y="449" width="125" height="42" rx="6" fill="{"#0F766E" if score else "#EEF2F7"}"/><text x="{x+62}" y="476" text-anchor="middle" font-size="14" fill="{"#FFFFFF" if score else "#17324D"}">mask {score}</text>',
        ]
    lines += [
        '<rect x="55" y="545" width="1090" height="82" rx="11" fill="#F8FAFC" stroke="#CBD5E1"/>',
        f'<text x="80" y="578" font-size="16" fill="#17324D">global target mean = 21/9 = {sft["global_mean"]:.4f}</text>',
        f'<text x="445" y="578" font-size="16" fill="#C24135">equal-device mean = {sft["equal_device_mean"]:.4f}</text>',
        f'<text x="780" y="578" font-size="16" fill="#17324D">per-token / per-turn = {sft["per_token_mean"]:.4f} / {sft["per_turn_mean"]:.4f}</text>',
        '<text x="80" y="610" font-size="14" fill="#64748B">Same tokens can define different estimands when the mask or denominator changes.</text>',
        "</svg>",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_lora_memory_svg(path: Path, lora: dict, memory: dict) -> None:
    lines = svg_begin("LoRA gradient flow and QLoRA memory ledger", "Left: delta matrix and zero-factor gradients. Right: additive memory accounting.")
    lines += [
        '<text x="55" y="55" font-size="25" font-weight="700" fill="#17324D">Low-rank parameter count and end-to-end memory are different ledgers</text>',
        '<line x1="600" y1="105" x2="600" y2="625" stroke="#D7DEE8"/>',
        '<text x="65" y="120" font-size="18" font-weight="700" fill="#17324D">1 · LoRA finite oracle</text>',
        f'<text x="90" y="175" font-size="17" fill="#17324D">ΔW = {esc(lora["delta"])}</text>',
        f'<text x="90" y="220" font-size="17" fill="#17324D">x = {esc(lora["x"])} → adapter output [1, 3]</text>',
        f'<text x="90" y="265" font-size="17" fill="#0F766E">merged output = {esc(lora["merged_output"])}</text>',
        '<rect x="80" y="315" width="455" height="175" rx="12" fill="#F5F3FF" stroke="#7C3AED"/>',
        '<text x="105" y="350" font-size="16" font-weight="700" fill="#7C3AED">A=I, B=0 at initialization</text>',
        f'<text x="105" y="395" font-size="14" fill="#17324D">grad B = {esc(lora["grad_B_when_B_zero"])}</text>',
        f'<text x="105" y="440" font-size="14" fill="#17324D">grad A = {esc(lora["grad_A_when_B_zero"])}</text>',
        '<text x="105" y="475" font-size="14" fill="#C24135">both A=B=0 would make both gradients zero</text>',
        '<text x="640" y="120" font-size="18" font-weight="700" fill="#17324D">2 · QLoRA accounted memory</text>',
    ]
    colors = ["#7C3AED", "#A78BFA", "#0F766E", "#2563EB", "#D97706"]
    max_value = max(row["gb"] for row in memory["rows"])
    for i, (row, color) in enumerate(zip(memory["rows"], colors)):
        y = 160 + i * 78
        width = 250 * row["gb"] / max_value
        lines += [
            f'<text x="650" y="{y+20}" font-size="14" fill="#17324D">{esc(row["item"])}</text>',
            f'<rect x="820" y="{y}" width="{width}" height="32" rx="6" fill="{color}"/>',
            f'<text x="{835+width}" y="{y+22}" font-size="14" fill="{color}">{row["gb"]:.2f} GB</text>',
        ]
    lines += [
        '<rect x="640" y="555" width="500" height="72" rx="10" fill="#FFF7E8" stroke="#D97706"/>',
        f'<text x="665" y="585" font-size="17" font-weight="700" fill="#D97706">accounted sum = {memory["accounted_sum_gb"]:.2f} GB</text>',
        '<text x="665" y="612" font-size="13" fill="#64748B">Peak still depends on lifetimes, allocator, kernel, batch and sequence.</text>',
        "</svg>",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_merging_svg(path: Path, distribution: dict, peft: dict, merging: dict) -> None:
    lines = svg_begin("Data weights, PEFT states and parameter merging", "Three panels compare instruction target shares, PEFT state counts and merging outputs.")
    lines += [
        '<text x="55" y="55" font-size="25" font-weight="700" fill="#17324D">Adaptation claims move through data, state and coordinate contracts</text>',
        '<line x1="400" y1="110" x2="400" y2="620" stroke="#D7DEE8"/><line x1="800" y1="110" x2="800" y2="620" stroke="#D7DEE8"/>',
        '<text x="55" y="130" font-size="18" font-weight="700" fill="#17324D">1 · task draw ≠ target share</text>',
    ]
    for i, row in enumerate(distribution["tasks"]):
        y = 180 + i * 120
        color = "#2563EB" if row["task"] == "A" else "#D97706"
        lines += [
            f'<text x="65" y="{y}" font-size="16" font-weight="700" fill="{color}">Task {row["task"]}</text>',
            f'<rect x="135" y="{y-24}" width="{200*row["draw_share"]}" height="28" rx="5" fill="#93C5FD"/><text x="250" y="{y-5}" font-size="13">draw {row["draw_share"]:.0%}</text>',
            f'<rect x="135" y="{y+20}" width="{200*row["target_share"]}" height="28" rx="5" fill="{color}"/><text x="250" y="{y+40}" font-size="13">target {row["target_share"]:.0%}</text>',
        ]
    lines += [
        '<text x="430" y="130" font-size="18" font-weight="700" fill="#17324D">2 · same frozen base, different state</text>',
    ]
    counts = [
        ("prompt", peft["prompt_parameters"], "#2563EB"),
        ("prefix KV", peft["prefix_kv_parameters"], "#7C3AED"),
        ("adapter", peft["adapter_parameters"], "#D97706"),
    ]
    for i, (label, value, color) in enumerate(counts):
        y = 185 + i * 105
        width = 260 * value / max(v for _, v, _ in counts)
        lines += [
            f'<text x="440" y="{y}" font-size="15" fill="#17324D">{esc(label)}</text>',
            f'<rect x="530" y="{y-25}" width="{width}" height="34" rx="6" fill="{color}"/>',
            f'<text x="{545+width}" y="{y-2}" font-size="14" fill="{color}">{value}</text>',
        ]
    lines += [
        '<text x="830" y="130" font-size="18" font-weight="700" fill="#17324D">3 · coordinates do not guarantee function</text>',
        f'<text x="845" y="190" font-size="15">uniform soup = {esc(merging["uniform_soup"])}</text>',
        f'<text x="845" y="235" font-size="15">task-vector sum = {esc(merging["task_vector_sum"])}</text>',
        f'<text x="845" y="300" font-size="15" fill="#0F766E">TIES + coordinate = {merging["ties_positive"]["merged"]:.2f}</text>',
        f'<text x="845" y="345" font-size="15" fill="#C24135">TIES − coordinate = {merging["ties_negative"]["merged"]:.2f}</text>',
        '<rect x="835" y="415" width="300" height="145" rx="11" fill="#FEE2E2" stroke="#C24135"/>',
        f'<text x="855" y="452" font-size="15" font-weight="700" fill="#C24135">Permutation counterexample</text>',
        f'<text x="855" y="492" font-size="14">fA = fB = {merging["permutation_counterexample"]["f_a"]:.1f}</text>',
        f'<text x="855" y="530" font-size="14">f(parameter average) = {merging["permutation_counterexample"]["f_average"]:.1f}</text>',
        '<text x="55" y="650" font-size="14" fill="#64748B">Every bar is tied to a unit; every merged tensor still needs independent task, OOD and safety evaluation.</text>',
        "</svg>",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--plots", type=Path, default=DEFAULT_PLOTS)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.plots.mkdir(parents=True, exist_ok=True)

    template = audit_template()
    sft = audit_sft()
    distribution = audit_instruction_distribution()
    low_margin = audit_low_margin()
    lora = audit_lora()
    memory = audit_qlora_memory()
    peft = audit_peft_counts()
    merging = audit_merging()

    checks = {
        "chat_train_inference_prefix": template["train_prefix"] == template["infer"] and template["answer_start"] == 8,
        "sft_shift_mask_and_global_denominator": sft["labels"] == ["q", "A", "a", "b", "EOS"] and sft["response_mask"] == [0, 0, 1, 1, 1] and abs(sft["global_mean"] - 7 / 3) < 1e-12,
        "instruction_draw_target_selection_shares": [row["target_share"] for row in distribution["tasks"]] == [0.2, 0.8] and abs(distribution["selection"][0]["selected_share"] - 6 / 7) < 1e-12,
        "small_parameter_large_function_flip": low_margin["parameter_change"] == 0.002 and low_margin["prediction_flips"] == 100,
        "lora_gradient_and_merge_oracle": lora["grad_A_when_B_zero"] == [[0.0, 0.0], [0.0, 0.0]] and lora["grad_B_when_B_zero"] != lora["grad_A_when_B_zero"] and lora["merged_output"] == lora["unmerged_output"] == [2.0, 5.0],
        "qlora_memory_accounting": abs(memory["accounted_sum_gb"] - 2.62) < 1e-12,
        "peft_parameter_counts": peft["prompt_parameters"] == 500 and peft["prefix_kv_parameters"] == 4000 and peft["adapter_parameters"] == 1600,
        "soup_task_arithmetic_and_ties": merging["uniform_soup"] == [1.5, 1.5] and merging["task_vector_sum"] == [2.0, 2.0] and abs(merging["ties_positive"]["merged"] - 0.7) < 1e-12 and abs(merging["ties_negative"]["merged"] + 0.65) < 1e-12,
        "permutation_breaks_naive_average": merging["permutation_counterexample"] == {"f_a": 6.0, "f_b": 6.0, "f_average": 0.0},
    }

    payload = {
        "experiment_id": "EXP-LM-704-V1",
        "checks": checks,
        "template": template,
        "sft": sft,
        "instruction_distribution": distribution,
        "low_margin": low_margin,
        "lora": lora,
        "qlora_memory": memory,
        "peft_counts": peft,
        "merging": merging,
    }
    (args.out / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    token_rows = [
        {"position": i, "input": inp, "label": label, "response_mask": mask}
        for i, (inp, label, mask) in enumerate(zip(sft["inputs"], sft["labels"], sft["response_mask"]))
    ]
    write_csv(args.out / "token_contract.csv", ["position", "input", "label", "response_mask"], token_rows)
    write_csv(args.out / "adaptation_memory.csv", ["item", "gb"], memory["rows"])
    merge_rows = [
        {"object": "uniform_soup", "coordinate_0": merging["uniform_soup"][0], "coordinate_1": merging["uniform_soup"][1], "meaning": "checkpoint_average"},
        {"object": "task_vector_sum", "coordinate_0": merging["task_vector_sum"][0], "coordinate_1": merging["task_vector_sum"][1], "meaning": "base_plus_deltas"},
        {"object": "ties_positive", "coordinate_0": merging["ties_positive"]["merged"], "coordinate_1": "", "meaning": "trim_elect_aligned_mean"},
        {"object": "ties_negative", "coordinate_0": merging["ties_negative"]["merged"], "coordinate_1": "", "meaning": "trim_elect_aligned_mean"},
    ]
    write_csv(args.out / "merge_ledger.csv", ["object", "coordinate_0", "coordinate_1", "meaning"], merge_rows)

    write_contract_svg(args.plots / "plot-language-adaptation-template-loss-v1.svg", template, sft)
    write_lora_memory_svg(args.plots / "plot-language-adaptation-lora-memory-v1.svg", lora, memory)
    write_merging_svg(args.plots / "plot-language-adaptation-peft-merging-v1.svg", distribution, peft, merging)

    print(json.dumps({"checks": checks, "out": str(args.out), "plots": str(args.plots)}, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
