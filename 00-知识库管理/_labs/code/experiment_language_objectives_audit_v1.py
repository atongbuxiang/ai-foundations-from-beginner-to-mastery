#!/usr/bin/env python3
"""Deterministic standard-library audit for LM-09--LM-16.

The script makes probability objects, visibility relations, loss regions and
denominators executable. It emits JSON, CSV and three self-contained SVGs.
No model framework is required: every check is a finite oracle that a real
training pipeline can be compared against.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "_labs" / "experiments" / "lm70.2-language-objectives-audit-v1"
DEFAULT_PLOTS = ROOT / "_assets" / "plots" / "language-models"


def audit_chain_tree() -> dict:
    """Finite tree: EOS now, EOS after a, or forced EOS after aa."""
    leaves = {
        "EOS": 0.2,
        "a EOS": 0.8 * 0.5,
        "a a EOS": 0.8 * 0.5 * 1.0,
    }
    sequence = "a EOS"
    product = leaves[sequence]
    nll_parts = [-math.log(0.8), -math.log(0.5)]
    return {
        "leaves": leaves,
        "leaf_sum": sum(leaves.values()),
        "sequence": sequence,
        "path_product": product,
        "nll_parts": nll_parts,
        "nll_sum": sum(nll_parts),
        "nll_direct": -math.log(product),
    }


def causal_relation(length: int) -> list[list[int]]:
    return [[int(j <= i) for j in range(length)] for i in range(length)]


def prefix_relation(prefix: int, suffix: int) -> list[list[int]]:
    length = prefix + suffix
    out: list[list[int]] = []
    for i in range(length):
        row = []
        for j in range(length):
            if i < prefix:
                row.append(int(j < prefix))
            else:
                row.append(int(j <= i))
        out.append(row)
    return out


def audit_causal_contract() -> dict:
    full = ["BOS", "a", "b", "EOS"]
    inputs = full[:-1]
    labels = full[1:]
    relation = causal_relation(len(inputs))
    loss_mask = [1, 1, 1]
    pairs = [f"{x}->{y}" for x, y in zip(inputs, labels)]
    return {
        "full": full,
        "inputs": inputs,
        "labels": labels,
        "pairs": pairs,
        "relation": relation,
        "loss_mask": loss_mask,
        "effective_targets": sum(loss_mask),
    }


def audit_reduction() -> dict:
    devices = [
        {"device": "A", "tokens": 80, "mean_nll": 1.2},
        {"device": "B", "tokens": 20, "mean_nll": 2.0},
    ]
    for row in devices:
        row["numerator"] = row["tokens"] * row["mean_nll"]
    global_mean = sum(r["numerator"] for r in devices) / sum(r["tokens"] for r in devices)
    device_mean = sum(r["mean_nll"] for r in devices) / len(devices)
    return {
        "devices": devices,
        "global_token_mean": global_mean,
        "equal_device_mean": device_mean,
        "absolute_gap": abs(global_mean - device_mean),
    }


def audit_mlm() -> dict:
    base_tokens = 10_000
    targets = int(base_tokens * 0.15)
    branches = {
        "MASK_visible": int(targets * 0.80),
        "random_visible": int(targets * 0.10),
        "unchanged_visible": int(targets * 0.10),
    }

    # Incompatible binary conditionals: the two directions imply different
    # odds ratios. Their exponentiated PLL weights also do not sum to one.
    px1_given_y = {0: 0.2, 1: 0.8}
    py1_given_x = {0: 0.3, 1: 0.6}
    odds_x = (0.8 / 0.2) / (0.2 / 0.8)
    odds_y = (0.6 / 0.4) / (0.3 / 0.7)
    pll_weights = {}
    for x in (0, 1):
        for y in (0, 1):
            px = px1_given_y[y] if x == 1 else 1.0 - px1_given_y[y]
            py = py1_given_x[x] if y == 1 else 1.0 - py1_given_x[x]
            pll_weights[f"{x}{y}"] = px * py
    return {
        "base_tokens": base_tokens,
        "targets": targets,
        "branches": branches,
        "visible_MASK_positions": branches["MASK_visible"],
        "loss_positions": targets,
        "conditional_odds_ratio_x_given_y": odds_x,
        "conditional_odds_ratio_y_given_x": odds_y,
        "pll_weights": pll_weights,
        "pll_weight_sum": sum(pll_weights.values()),
    }


def corrupt_spans(clean: list[str], spans: list[tuple[int, int]]) -> tuple[list[str], list[str]]:
    """Spans are zero-based half-open, sorted and non-overlapping."""
    source: list[str] = []
    target: list[str] = []
    cursor = 0
    for k, (start, end) in enumerate(spans):
        if not (cursor <= start < end <= len(clean)):
            raise ValueError("invalid or overlapping span")
        sentinel = f"<s{k}>"
        source.extend(clean[cursor:start])
        source.append(sentinel)
        target.append(sentinel)
        target.extend(clean[start:end])
        cursor = end
    source.extend(clean[cursor:])
    target.append(f"<s{len(spans)}>")
    return source, target


def reconstruct_spans(source: list[str], target: list[str]) -> list[str]:
    positions = {token: i for i, token in enumerate(target) if token.startswith("<s")}
    sentinels = sorted(positions, key=lambda token: positions[token])
    restored: list[str] = []
    for token in source:
        if not token.startswith("<s"):
            restored.append(token)
            continue
        start = positions[token] + 1
        index = sentinels.index(token)
        next_token = sentinels[index + 1]
        end = positions[next_token]
        restored.extend(target[start:end])
    return restored


def audit_t5() -> dict:
    clean = list("abcdefg")
    spans = [(1, 3), (5, 6)]
    source, target = corrupt_spans(clean, spans)
    restored = reconstruct_spans(source, target)
    return {
        "clean": clean,
        "spans_half_open": spans,
        "source": source,
        "target": target,
        "restored": restored,
        "source_length_formula": len(clean) - 3 + 2,
        "target_length_formula": 3 + 2 + 1,
    }


def audit_prefix() -> dict:
    relation = prefix_relation(2, 3)
    expected = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
    ]
    return {"prefix": 2, "suffix": 3, "relation": relation, "expected": expected}


def audit_mixture() -> dict:
    rows = [
        {"mode": "R", "samples": 50, "mean_targets": 20},
        {"mode": "X", "samples": 50, "mean_targets": 80},
    ]
    total_samples = sum(r["samples"] for r in rows)
    total_targets = sum(r["samples"] * r["mean_targets"] for r in rows)
    for row in rows:
        row["targets"] = row["samples"] * row["mean_targets"]
        row["sample_share"] = row["samples"] / total_samples
        row["target_share"] = row["targets"] / total_targets
    return {"rows": rows, "total_samples": total_samples, "total_targets": total_targets}


def audit_denominators() -> dict:
    string_probability = 1e-6
    raw_bytes = 12
    token_counts = {"tokenizer_A": 2, "tokenizer_B": 6}
    ppl = {name: string_probability ** (-1.0 / count) for name, count in token_counts.items()}
    bpb = -math.log(string_probability) / (raw_bytes * math.log(2.0))
    return {
        "string_probability": string_probability,
        "raw_bytes": raw_bytes,
        "token_counts": token_counts,
        "token_ppl": ppl,
        "bpb_both": bpb,
    }


STYLE = '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>'


def esc(value: object) -> str:
    return html.escape(str(value))


def svg_begin(title: str, desc: str, height: int = 650) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
        f'<rect width="1200" height="{height}" fill="#FFFEFB"/>', STYLE,
    ]


def matrix_svg(lines: list[str], matrix: list[list[int]], x0: int, y0: int, cell: int, label: str, boundary: int | None = None) -> None:
    lines.append(f'<text x="{x0}" y="{y0-24}" font-size="19" font-weight="700" fill="#17324D">{esc(label)}</text>')
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            fill = "#2563EB" if value else "#F2F5F8"
            stroke = "#D7DEE8"
            lines.append(f'<rect x="{x0+j*cell}" y="{y0+i*cell}" width="{cell-3}" height="{cell-3}" rx="4" fill="{fill}" stroke="{stroke}"/>')
    if boundary is not None:
        bx = x0 + boundary * cell - 2
        by = y0 + boundary * cell - 2
        extent = len(matrix) * cell
        lines.append(f'<line x1="{bx}" y1="{y0-7}" x2="{bx}" y2="{y0+extent}" stroke="#C24135" stroke-width="3" stroke-dasharray="7 5"/>')
        lines.append(f'<line x1="{x0-7}" y1="{by}" x2="{x0+extent}" y2="{by}" stroke="#C24135" stroke-width="3" stroke-dasharray="7 5"/>')


def write_relation_svg(path: Path, causal: dict, prefix: dict) -> None:
    lines = svg_begin("Causal 与 Prefix LM 可见性关系", "并排显示 causal 下三角和 prefix 四块 relation，行是 query、列是 key。")
    lines += [
        '<text x="55" y="55" font-size="25" font-weight="700" fill="#2563EB">可见性不是模型名称：逐格审计 query → key</text>',
        '<text x="55" y="88" font-size="15" fill="#64748B">蓝色=可读，灰色=屏蔽；两张图均以 query 为行、key 为列</text>',
    ]
    matrix_svg(lines, causal["relation"], 155, 180, 72, "Causal LM：L=3")
    matrix_svg(lines, prefix["relation"], 675, 145, 72, "Prefix LM：P=2, S=3", boundary=2)
    lines += [
        '<text x="155" y="450" font-size="16" fill="#17324D">每个位置只读自己与过去</text>',
        '<text x="675" y="540" font-size="16" fill="#17324D">左上双向；右上禁泄漏；左下读 source；右下因果</text>',
        '<rect x="55" y="575" width="1090" height="48" rx="9" fill="#FFF7E8" stroke="#E5B94E"/>',
        '<text x="75" y="605" font-size="15" fill="#6B4E16">relation 只回答“谁能看谁”；target shift、loss mask 与 denominator 必须另画。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_sampler_svg(path: Path, mlm: dict, mixture: dict) -> None:
    lines = svg_begin("MLM corruption 与 mixture 权重账本", "左侧显示 MLM targets 和输入可见分支，右侧显示同样本份额但不同 target token 份额。")
    lines += [
        '<text x="55" y="55" font-size="25" font-weight="700" fill="#2563EB">Sampler 先决定训练分布，别从名字猜 loss</text>',
        '<line x1="600" y1="105" x2="600" y2="570" stroke="#D7DEE8" stroke-width="2"/>',
        '<text x="75" y="115" font-size="20" font-weight="700" fill="#17324D">MLM：10,000 clean positions</text>',
        '<rect x="80" y="160" width="470" height="62" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>',
        f'<text x="315" y="198" text-anchor="middle" font-size="20" font-weight="700">{mlm["targets"]} loss targets (15%)</text>',
    ]
    branch_colors = ["#2563EB", "#B7791F", "#0F766E"]
    labels = [("[MASK] visible", 1200), ("random visible", 150), ("unchanged visible", 150)]
    for i, ((label, count), color) in enumerate(zip(labels, branch_colors)):
        y = 270 + i * 78
        width = 370 * count / 1200
        lines += [
            f'<rect x="105" y="{y}" width="{width}" height="34" rx="6" fill="{color}"/>',
            f'<text x="{120+width}" y="{y+23}" font-size="15" fill="#17324D">{esc(label)} = {count}</text>',
        ]
    lines += [
        '<text x="75" y="545" font-size="15" fill="#C24135">可见 [MASK] 数 1200 ≠ loss positions 1500</text>',
        '<text x="645" y="115" font-size="20" font-weight="700" fill="#17324D">Mixture：相同 sample share</text>',
    ]
    for i, row in enumerate(mixture["rows"]):
        y = 180 + i * 190
        sample_w = row["sample_share"] * 380
        token_w = row["target_share"] * 380
        color = "#0F766E" if row["mode"] == "R" else "#C24135"
        lines += [
            f'<text x="655" y="{y}" font-size="18" font-weight="700" fill="{color}">mode {row["mode"]}</text>',
            f'<rect x="750" y="{y-22}" width="{sample_w}" height="34" rx="6" fill="#93C5FD"/><text x="760" y="{y+1}" font-size="14">sample {row["sample_share"]:.0%}</text>',
            f'<rect x="750" y="{y+35}" width="{token_w}" height="34" rx="6" fill="{color}"/><text x="760" y="{y+58}" font-size="14" fill="#FFFFFF">target {row["target_share"]:.0%}</text>',
            f'<text x="750" y="{y+96}" font-size="14" fill="#64748B">{row["samples"]} samples × {row["mean_targets"]} targets</text>',
        ]
    lines += [
        '<text x="645" y="575" font-size="15" fill="#64748B">sample、token、compute、gradient 是四份不同账本</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_denominator_svg(path: Path, reduction: dict, denom: dict) -> None:
    lines = svg_begin("Reduction 与 tokenizer denominator 反例", "左侧比较全局 token mean 和设备等权 mean；右侧固定字符串概率展示 token PPL 分叉而 BPB 相同。")
    lines += [
        '<text x="55" y="55" font-size="25" font-weight="700" fill="#2563EB">相同 numerator 语义，错误 denominator 就是另一个 estimand</text>',
        '<line x1="600" y1="105" x2="600" y2="565" stroke="#D7DEE8" stroke-width="2"/>',
        '<text x="75" y="115" font-size="20" font-weight="700" fill="#17324D">分布式 reduction</text>',
        '<text x="95" y="175" font-size="17">A: 80 tokens × 1.2 = 96 nats</text>',
        '<text x="95" y="215" font-size="17">B: 20 tokens × 2.0 = 40 nats</text>',
        '<rect x="95" y="270" width="370" height="70" rx="10" fill="#ECFDF5" stroke="#0F766E" stroke-width="2"/>',
        f'<text x="280" y="312" text-anchor="middle" font-size="23" font-weight="700" fill="#0F766E">global token mean = {reduction["global_token_mean"]:.2f}</text>',
        '<rect x="95" y="380" width="370" height="70" rx="10" fill="#FEE2E2" stroke="#C24135" stroke-width="2"/>',
        f'<text x="280" y="422" text-anchor="middle" font-size="23" font-weight="700" fill="#C24135">equal-device mean = {reduction["equal_device_mean"]:.2f}</text>',
        '<text x="75" y="515" font-size="15" fill="#64748B">先 all-reduce numerator 与 denominator，再相除</text>',
        '<text x="645" y="115" font-size="20" font-weight="700" fill="#17324D">跨 tokenizer：同一字符串概率 10⁻⁶</text>',
    ]
    values = [("A · 2 tokens", denom["token_ppl"]["tokenizer_A"], "#C24135"), ("B · 6 tokens", denom["token_ppl"]["tokenizer_B"], "#2563EB")]
    for i, (label, value, color) in enumerate(values):
        y = 190 + i * 130
        bar_w = 390 * math.log10(value) / 3.0
        lines += [
            f'<text x="660" y="{y}" font-size="17" font-weight="700">{esc(label)}</text>',
            f'<rect x="660" y="{y+20}" width="{bar_w}" height="46" rx="7" fill="{color}"/>',
            f'<text x="{675+bar_w}" y="{y+51}" font-size="18" font-weight="700" fill="{color}">PPL={value:.0f}</text>',
        ]
    lines += [
        '<rect x="660" y="465" width="440" height="72" rx="10" fill="#FFF7E8" stroke="#E5B94E" stroke-width="2"/>',
        f'<text x="880" y="495" text-anchor="middle" font-size="17">共同 raw denominator = {denom["raw_bytes"]} UTF-8 bytes</text>',
        f'<text x="880" y="523" text-anchor="middle" font-size="21" font-weight="700" fill="#6B4E16">两者 BPB = {denom["bpb_both"]:.4f}</text>',
        '<text x="645" y="585" font-size="15" fill="#64748B">共同 BPB 仍要求两模型对同一 raw byte string 定义概率。</text>',
        '</svg>',
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

    chain = audit_chain_tree()
    causal = audit_causal_contract()
    reduction = audit_reduction()
    mlm = audit_mlm()
    t5 = audit_t5()
    prefix = audit_prefix()
    mixture = audit_mixture()
    denominators = audit_denominators()

    checks = {
        "chain_tree_probability_conservation": abs(chain["leaf_sum"] - 1.0) < 1e-12 and abs(chain["nll_sum"] - chain["nll_direct"]) < 1e-12,
        "causal_shift_relation_loss_alignment": causal["pairs"] == ["BOS->a", "a->b", "b->EOS"] and causal["relation"] == [[1, 0, 0], [1, 1, 0], [1, 1, 1]] and causal["effective_targets"] == 3,
        "global_numerator_denominator_reduction": abs(reduction["global_token_mean"] - 1.36) < 1e-12 and reduction["absolute_gap"] > 0.2,
        "mlm_mask_set_not_visible_MASK_set": mlm["loss_positions"] == 1500 and mlm["visible_MASK_positions"] == 1200 and sum(mlm["branches"].values()) == 1500,
        "mlm_conditionals_not_automatic_joint": abs(mlm["conditional_odds_ratio_x_given_y"] - mlm["conditional_odds_ratio_y_given_x"]) > 1.0 and abs(mlm["pll_weight_sum"] - 1.0) > 0.1,
        "t5_sentinel_roundtrip": t5["restored"] == t5["clean"] and len(t5["source"]) == t5["source_length_formula"] and len(t5["target"]) == t5["target_length_formula"],
        "prefix_relation_exact": prefix["relation"] == prefix["expected"],
        "mixture_sample_share_not_target_share": all(abs(r["sample_share"] - 0.5) < 1e-12 for r in mixture["rows"]) and [r["target_share"] for r in mixture["rows"]] == [0.2, 0.8],
        "cross_tokenizer_ppl_counterexample_bpb_common": abs(denominators["token_ppl"]["tokenizer_A"] - 1000.0) < 1e-9 and abs(denominators["token_ppl"]["tokenizer_B"] - 10.0) < 1e-9,
    }

    payload = {
        "experiment_id": "EXP-LM-702-V1",
        "checks": checks,
        "chain_tree": chain,
        "causal_contract": causal,
        "distributed_reduction": reduction,
        "mlm": mlm,
        "t5_span_corruption": t5,
        "prefix_lm": prefix,
        "mixture": mixture,
        "denominators": denominators,
    }
    (args.out / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    relation_rows = []
    for name, matrix in (("causal", causal["relation"]), ("prefix", prefix["relation"])):
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                relation_rows.append({"relation": name, "query": i, "key": j, "visible": value})
    write_csv(args.out / "relations.csv", ["relation", "query", "key", "visible"], relation_rows)
    write_csv(args.out / "mixture_ledger.csv", ["mode", "samples", "mean_targets", "targets", "sample_share", "target_share"], mixture["rows"])
    denom_rows = [
        {"object": "global_token_mean", "numerator_or_probability": 136, "denominator": 100, "result": reduction["global_token_mean"]},
        {"object": "equal_device_mean", "numerator_or_probability": "1.2+2.0", "denominator": 2, "result": reduction["equal_device_mean"]},
        {"object": "tokenizer_A_ppl", "numerator_or_probability": 1e-6, "denominator": 2, "result": denominators["token_ppl"]["tokenizer_A"]},
        {"object": "tokenizer_B_ppl", "numerator_or_probability": 1e-6, "denominator": 6, "result": denominators["token_ppl"]["tokenizer_B"]},
        {"object": "common_bpb", "numerator_or_probability": -math.log(1e-6), "denominator": 12, "result": denominators["bpb_both"]},
    ]
    write_csv(args.out / "denominator_ledger.csv", ["object", "numerator_or_probability", "denominator", "result"], denom_rows)

    write_relation_svg(args.plots / "plot-language-objectives-relations-v1.svg", causal, prefix)
    write_sampler_svg(args.plots / "plot-language-objectives-sampler-ledger-v1.svg", mlm, mixture)
    write_denominator_svg(args.plots / "plot-language-objectives-denominators-v1.svg", reduction, denominators)

    print(json.dumps({"checks": checks, "out": str(args.out), "plots": str(args.plots)}, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
