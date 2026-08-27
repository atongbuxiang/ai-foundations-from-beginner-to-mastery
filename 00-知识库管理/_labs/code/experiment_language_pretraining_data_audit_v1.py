#!/usr/bin/env python3
"""Deterministic standard-library audit for LM-17--LM-24.

The experiment turns selection, similarity, contamination, mixture, packing,
curriculum and provenance contracts into finite oracles. It intentionally
avoids a deep-learning framework: every output can be checked by hand.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "_labs" / "experiments" / "lm70.3-pretraining-data-audit-v1"
DEFAULT_PLOTS = ROOT / "_assets" / "plots" / "language-models"
STYLE = '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>'


def audit_selection() -> dict:
    rows = [
        {"group": "A", "source_share": 0.60, "retention": 0.75},
        {"group": "B", "source_share": 0.40, "retention": 0.30},
    ]
    total_kept = sum(row["source_share"] * row["retention"] for row in rows)
    for row in rows:
        row["kept_mass"] = row["source_share"] * row["retention"]
        row["selected_share"] = row["kept_mass"] / total_kept
    return {"rows": rows, "total_retention": total_kept}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right)


def minhash_equal(left: set[str], right: set[str], permutation: tuple[str, ...]) -> bool:
    rank = {item: index for index, item in enumerate(permutation)}
    return min(left, key=rank.get) == min(right, key=rank.get)


def audit_minhash_lsh() -> dict:
    universe = ("a", "b", "c")
    left = {"a", "b"}
    right = {"b", "c"}
    permutations = list(itertools.permutations(universe))
    equal_count = sum(minhash_equal(left, right, perm) for perm in permutations)
    exact_jaccard = jaccard(left, right)
    empirical_probability = equal_count / len(permutations)
    similarity = 0.8
    bands = 10
    rows_per_band = 4
    candidate_probability = 1.0 - (1.0 - similarity**rows_per_band) ** bands
    return {
        "universe": universe,
        "left": sorted(left),
        "right": sorted(right),
        "permutations": len(permutations),
        "equal_count": equal_count,
        "exact_jaccard": exact_jaccard,
        "enumerated_minhash_probability": empirical_probability,
        "lsh": {
            "similarity": similarity,
            "bands": bands,
            "rows_per_band": rows_per_band,
            "candidate_probability": candidate_probability,
        },
    }


def audit_clustering() -> dict:
    sets = {
        "A": {1, 2},
        "B": {1, 2, 3},
        "C": {2, 3},
    }
    pairs = {}
    for left, right in (("A", "B"), ("B", "C"), ("A", "C")):
        pairs[f"{left}-{right}"] = len(sets[left] & sets[right]) / len(sets[left] | sets[right])
    threshold = 0.5
    edges = [pair for pair, value in pairs.items() if value >= threshold]
    return {
        "sets": {name: sorted(value) for name, value in sets.items()},
        "pair_jaccard": pairs,
        "threshold": threshold,
        "edges": edges,
        "connected_component": ["A", "B", "C"],
    }


def contamination_posterior(prevalence: float, recall: float, false_positive_rate: float) -> float:
    numerator = recall * prevalence
    return numerator / (numerator + false_positive_rate * (1.0 - prevalence))


def audit_contamination() -> dict:
    prevalence = 0.02
    recall = 0.90
    false_positive_rate = 0.01
    posterior = contamination_posterior(prevalence, recall, false_positive_rate)
    return {
        "prevalence": prevalence,
        "recall": recall,
        "false_positive_rate": false_positive_rate,
        "positive_posterior": posterior,
    }


def audit_mixture() -> dict:
    rows = [
        {"domain": "A", "document_share": 0.5, "mean_tokens": 100, "loss_fraction": 1.0},
        {"domain": "B", "document_share": 0.5, "mean_tokens": 400, "loss_fraction": 0.5},
    ]
    token_mass = sum(row["document_share"] * row["mean_tokens"] for row in rows)
    target_mass = sum(
        row["document_share"] * row["mean_tokens"] * row["loss_fraction"] for row in rows
    )
    for row in rows:
        row["token_share"] = row["document_share"] * row["mean_tokens"] / token_mass
        row["target_share"] = (
            row["document_share"] * row["mean_tokens"] * row["loss_fraction"] / target_mass
        )
    power_counts = [10_000, 100, 1]
    power = {}
    for alpha in (1.0, 0.5, 0.0):
        mass = [count**alpha for count in power_counts]
        power[str(alpha)] = [value / sum(mass) for value in mass]
    return {"rows": rows, "power_counts": power_counts, "power_sampling": power}


def first_fit_decreasing(lengths: list[int], capacity: int) -> list[list[int]]:
    bins: list[list[int]] = []
    for length in sorted(lengths, reverse=True):
        for bin_items in bins:
            if sum(bin_items) + length <= capacity:
                bin_items.append(length)
                break
        else:
            bins.append([length])
    return bins


def block_causal(document_ids: list[str]) -> list[list[int]]:
    return [
        [int(key <= query and document_ids[key] == document_ids[query]) for key in range(len(document_ids))]
        for query in range(len(document_ids))
    ]


def audit_packing() -> dict:
    lengths = [6, 5, 4, 3, 2]
    capacity = 10
    bins = first_fit_decreasing(lengths, capacity)
    document_ids = ["A", "A", "B", "B", "B"]
    relation = block_causal(document_ids)
    full = ["a", "EOS", "b", "c", "EOS"]
    inputs = full[:-1]
    labels = full[1:]
    loss_mask = [1, 0, 1, 1]
    utilization = sum(lengths) / (len(bins) * capacity)
    return {
        "lengths": lengths,
        "capacity": capacity,
        "bins": bins,
        "utilization": utilization,
        "document_ids": document_ids,
        "relation": relation,
        "inputs": inputs,
        "labels": labels,
        "loss_mask": loss_mask,
        "effective_targets": sum(loss_mask),
    }


def audit_curriculum() -> dict:
    eta = 0.1

    def grad_a(theta: float) -> float:
        return theta - 1.0

    def grad_b(theta: float) -> float:
        return 2.0 * (theta + 1.0)

    def update(theta: float, gradient) -> float:
        return theta - eta * gradient(theta)

    ab_a = update(0.0, grad_a)
    ab = update(ab_a, grad_b)
    ba_b = update(0.0, grad_b)
    ba = update(ba_b, grad_a)
    return {
        "eta": eta,
        "AB": {"after_A": ab_a, "final": ab},
        "BA": {"after_B": ba_b, "final": ba},
        "absolute_path_gap": abs(ab - ba),
        "loss_changes": {"new": 1.2 - 2.0, "old": 1.4 - 1.0},
    }


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def audit_provenance() -> dict:
    stages = [
        {"name": "raw_bytes", "count": 100},
        {"name": "parsed", "count": 80},
        {"name": "filtered", "count": 60},
        {"name": "unique", "count": 45},
        {"name": "draws", "count": 50},
        {"name": "targets", "count": 42},
    ]
    adjacent = []
    for before, after in zip(stages, stages[1:]):
        adjacent.append(
            {
                "edge": f'{before["name"]}->{after["name"]}',
                "ratio": after["count"] / before["count"],
                "kind": "exposure" if before["name"] == "unique" else "fraction",
            }
        )
    masks = [[1, 1, 0, 1], [1, 0, 0, 0]]
    effective_targets = sum(sum(mask) for mask in masks)
    manifest_a = {"schema": 1, "shards": [{"id": "s1", "sha256": "abc"}], "tokenizer": "tok-v1"}
    manifest_b = {"tokenizer": "tok-v1", "shards": [{"sha256": "abc", "id": "s1"}], "schema": 1}
    return {
        "stages": stages,
        "adjacent_ratios": adjacent,
        "loss_masks": masks,
        "effective_targets": effective_targets,
        "nll_sum": 6.0,
        "mean_nll": 6.0 / effective_targets,
        "manifest_hash_a": canonical_hash(manifest_a),
        "manifest_hash_b": canonical_hash(manifest_b),
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


def write_selection_svg(path: Path, selection: dict) -> None:
    lines = svg_begin(
        "Selection changes the empirical distribution",
        "Source shares, group-specific retention and selected shares are shown as separate ledgers.",
    )
    lines += [
        '<text x="55" y="55" font-size="26" font-weight="700" fill="#17324D">Selection is a distributional operator, not neutral cleanup</text>',
        '<text x="55" y="88" font-size="15" fill="#64748B">P(group) × retention(group) → kept mass → Q(group)</text>',
    ]
    columns = [("SOURCE SHARE", "source_share", 90), ("RETENTION", "retention", 440), ("SELECTED SHARE", "selected_share", 790)]
    colors = {"A": "#2563EB", "B": "#D97706"}
    for label, key, x in columns:
        lines.append(f'<text x="{x}" y="145" font-size="17" font-weight="700" fill="#17324D">{label}</text>')
        for index, row in enumerate(selection["rows"]):
            y = 195 + index * 145
            width = 260 * row[key]
            lines += [
                f'<text x="{x}" y="{y}" font-size="18" font-weight="700" fill="{colors[row["group"]]}">Group {row["group"]}</text>',
                f'<rect x="{x}" y="{y+18}" width="260" height="44" rx="7" fill="#EEF2F7"/>',
                f'<rect x="{x}" y="{y+18}" width="{width:.2f}" height="44" rx="7" fill="{colors[row["group"]]}"/>',
                f'<text x="{x+275}" y="{y+48}" font-size="17" fill="#17324D">{row[key]:.2%}</text>',
            ]
    lines += [
        '<path d="M365 300 L415 300" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>',
        '<path d="M715 300 L765 300" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#94A3B8"/></marker></defs>',
        '<rect x="70" y="525" width="1060" height="105" rx="13" fill="#F8FAFC" stroke="#CBD5E1"/>',
        f'<text x="95" y="565" font-size="18" fill="#17324D">Overall retention = {selection["total_retention"]:.0%}</text>',
        '<text x="95" y="600" font-size="18" fill="#C24135">A moves 60% → 78.95%; B moves 40% → 21.05%.</text>',
        '<text x="605" y="565" font-size="15" fill="#64748B">The rejected set contains both noise and selection errors.</text>',
        '<text x="605" y="600" font-size="15" fill="#64748B">Audit rates by language, domain, length and rights status.</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def polyline(points: list[tuple[float, float]], x: int, y: int, width: int, height: int) -> str:
    coords = [f"{x + px * width:.1f},{y + (1.0 - py) * height:.1f}" for px, py in points]
    return " ".join(coords)


def write_similarity_svg(path: Path, minhash: dict, clustering: dict, contamination: dict) -> None:
    lines = svg_begin(
        "Similarity retrieval and contamination detection",
        "LSH candidate probability, non-transitive threshold graph and contamination posterior are shown separately.",
    )
    lines += [
        '<text x="55" y="55" font-size="26" font-weight="700" fill="#17324D">Candidate, verified pair, cluster and causal exposure are different claims</text>',
        '<line x1="400" y1="120" x2="400" y2="610" stroke="#D7DEE8"/><line x1="800" y1="120" x2="800" y2="610" stroke="#D7DEE8"/>',
        '<text x="60" y="135" font-size="18" font-weight="700" fill="#17324D">1 · LSH candidate probability</text>',
    ]
    lsh_points = [(i / 100, 1.0 - (1.0 - (i / 100) ** 4) ** 10) for i in range(101)]
    lines += [
        '<line x1="80" y1="510" x2="360" y2="510" stroke="#64748B"/><line x1="80" y1="510" x2="80" y2="190" stroke="#64748B"/>',
        f'<polyline points="{polyline(lsh_points, 80, 190, 280, 320)}" fill="none" stroke="#2563EB" stroke-width="4"/>',
        '<text x="210" y="548" font-size="14" fill="#64748B">true similarity s</text>',
        '<text x="65" y="180" font-size="13" fill="#64748B">1</text><text x="65" y="525" font-size="13" fill="#64748B">0</text>',
        f'<circle cx="{80+.8*280:.1f}" cy="{190+(1-minhash["lsh"]["candidate_probability"])*320:.1f}" r="7" fill="#C24135"/>',
        f'<text x="95" y="585" font-size="14" fill="#17324D">s=.8, b=10, r=4 → {minhash["lsh"]["candidate_probability"]:.4%}</text>',
        '<text x="425" y="135" font-size="18" font-weight="700" fill="#17324D">2 · Threshold graph is not transitive</text>',
    ]
    node_pos = {"A": (465, 330), "B": (600, 230), "C": (735, 330)}
    for pair, value in clustering["pair_jaccard"].items():
        left, right = pair.split("-")
        x1, y1 = node_pos[left]
        x2, y2 = node_pos[right]
        kept = value >= clustering["threshold"]
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{"#0F766E" if kept else "#C24135"}" stroke-width="{4 if kept else 3}" stroke-dasharray="{"" if kept else "7 6"}"/>'
        )
        lines.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-8}" text-anchor="middle" font-size="14" fill="#17324D">J={value:.2f}</text>')
    for name, (cx, cy) in node_pos.items():
        lines += [
            f'<circle cx="{cx}" cy="{cy}" r="34" fill="#EFF6FF" stroke="#2563EB" stroke-width="3"/>',
            f'<text x="{cx}" y="{cy+7}" text-anchor="middle" font-size="21" font-weight="700">{name}</text>',
        ]
    lines += [
        '<text x="430" y="435" font-size="15" fill="#0F766E">A—B and B—C pass τ=.5</text>',
        '<text x="430" y="470" font-size="15" fill="#C24135">A—C fails, yet connected components merge all 3</text>',
        '<text x="825" y="135" font-size="18" font-weight="700" fill="#17324D">3 · A positive is not certainty</text>',
    ]
    posterior_points = [
        (i / 100, contamination_posterior(i / 100, 0.90, 0.01)) if i else (0.0, 0.0)
        for i in range(101)
    ]
    lines += [
        '<line x1="845" y1="510" x2="1125" y2="510" stroke="#64748B"/><line x1="845" y1="510" x2="845" y2="190" stroke="#64748B"/>',
        f'<polyline points="{polyline(posterior_points, 845, 190, 280, 320)}" fill="none" stroke="#D97706" stroke-width="4"/>',
        '<text x="950" y="548" font-size="14" fill="#64748B">contamination base rate π</text>',
        f'<circle cx="{845+.02*280:.1f}" cy="{190+(1-contamination["positive_posterior"])*320:.1f}" r="7" fill="#C24135"/>',
        f'<text x="835" y="585" font-size="14" fill="#17324D">π=2%, recall=90%, FPR=1% → posterior {contamination["positive_posterior"]:.2%}</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def draw_matrix(lines: list[str], matrix: list[list[int]], x: int, y: int, cell: int) -> None:
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            lines.append(
                f'<rect x="{x+col_index*cell}" y="{y+row_index*cell}" width="{cell-2}" height="{cell-2}" rx="3" fill="{"#2563EB" if value else "#EEF2F7"}"/>'
            )


def write_training_svg(path: Path, mixture: dict, packing: dict, curriculum: dict, provenance: dict) -> None:
    lines = svg_begin(
        "Training accounting contracts",
        "Mixture shares, block-causal packing, curriculum path dependence and data-count provenance are shown in four panels.",
        height=760,
    )
    lines += [
        '<text x="55" y="55" font-size="26" font-weight="700" fill="#17324D">One run needs four ledgers: mixture, relation, path and provenance</text>',
        '<line x1="600" y1="105" x2="600" y2="710" stroke="#D7DEE8"/><line x1="55" y1="405" x2="1145" y2="405" stroke="#D7DEE8"/>',
        '<text x="70" y="130" font-size="18" font-weight="700" fill="#17324D">1 · Document → token → effective target</text>',
    ]
    for index, row in enumerate(mixture["rows"]):
        y = 175 + index * 90
        color = "#2563EB" if row["domain"] == "A" else "#D97706"
        lines.append(f'<text x="75" y="{y+18}" font-size="16" font-weight="700" fill="{color}">Domain {row["domain"]}</text>')
        for offset, key in enumerate(("document_share", "token_share", "target_share")):
            x = 170 + offset * 135
            lines += [
                f'<rect x="{x}" y="{y}" width="105" height="28" rx="5" fill="#EEF2F7"/>',
                f'<rect x="{x}" y="{y}" width="{105*row[key]:.1f}" height="28" rx="5" fill="{color}"/>',
                f'<text x="{x}" y="{y+52}" font-size="12" fill="#64748B">{key.replace("_share","")}: {row[key]:.0%}</text>',
            ]
    lines += [
        '<text x="630" y="130" font-size="18" font-weight="700" fill="#17324D">2 · Packed physically, isolated logically</text>',
    ]
    draw_matrix(lines, packing["relation"], 675, 175, 38)
    lines += [
        '<text x="885" y="195" font-size="14" fill="#17324D">doc IDs: A A | B B B</text>',
        '<text x="885" y="235" font-size="14" fill="#17324D">loss mask: 1 0 | 1 1</text>',
        '<text x="885" y="275" font-size="14" fill="#17324D">bins: [6,4] [5,3,2]</text>',
        '<text x="885" y="315" font-size="14" fill="#0F766E">utilization = 100%</text>',
        '<text x="70" y="445" font-size="18" font-weight="700" fill="#17324D">3 · Same counts, different order</text>',
        '<line x1="105" y1="545" x2="500" y2="545" stroke="#94A3B8" stroke-width="3"/>',
        '<circle cx="145" cy="545" r="24" fill="#EFF6FF" stroke="#2563EB"/><text x="145" y="552" text-anchor="middle" font-size="15">0</text>',
        f'<circle cx="310" cy="510" r="24" fill="#DBEAFE" stroke="#2563EB"/><text x="310" y="517" text-anchor="middle" font-size="14">A: {curriculum["AB"]["after_A"]:.1f}</text>',
        f'<circle cx="485" cy="485" r="27" fill="#FEE2E2" stroke="#C24135"/><text x="485" y="492" text-anchor="middle" font-size="14">AB: {curriculum["AB"]["final"]:.2f}</text>',
        f'<circle cx="310" cy="590" r="24" fill="#FEF3C7" stroke="#D97706"/><text x="310" y="597" text-anchor="middle" font-size="14">B: {curriculum["BA"]["after_B"]:.1f}</text>',
        f'<circle cx="485" cy="620" r="27" fill="#ECFDF5" stroke="#0F766E"/><text x="485" y="627" text-anchor="middle" font-size="14">BA: {curriculum["BA"]["final"]:.2f}</text>',
        '<path d="M170 535 C220 510 250 505 284 508" fill="none" stroke="#2563EB" stroke-width="3"/><path d="M335 505 C390 500 425 490 458 487" fill="none" stroke="#C24135" stroke-width="3"/>',
        '<path d="M170 555 C220 580 250 588 284 590" fill="none" stroke="#D97706" stroke-width="3"/><path d="M335 595 C390 605 425 615 458 618" fill="none" stroke="#0F766E" stroke-width="3"/>',
        '<text x="630" y="445" font-size="18" font-weight="700" fill="#17324D">4 · Count the object, then name the ratio</text>',
    ]
    stages = provenance["stages"]
    for index, stage in enumerate(stages):
        x = 635 + index * 88
        height = stage["count"] * 1.65
        y = 650 - height
        color = "#2563EB" if stage["name"] not in ("draws", "targets") else ("#D97706" if stage["name"] == "draws" else "#0F766E")
        lines += [
            f'<rect x="{x}" y="{y}" width="58" height="{height}" rx="5" fill="{color}"/>',
            f'<text x="{x+29}" y="{y-8}" text-anchor="middle" font-size="13" fill="#17324D">{stage["count"]}</text>',
            f'<text x="{x+29}" y="675" text-anchor="middle" font-size="11" fill="#64748B">{stage["name"]}</text>',
        ]
    lines += [
        f'<text x="635" y="715" font-size="14" fill="#17324D">loss masks → T_eff={provenance["effective_targets"]}; mean NLL=6/4={provenance["mean_nll"]:.1f}</text>',
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

    selection = audit_selection()
    minhash = audit_minhash_lsh()
    clustering = audit_clustering()
    contamination = audit_contamination()
    mixture = audit_mixture()
    packing = audit_packing()
    curriculum = audit_curriculum()
    provenance = audit_provenance()

    expected_relation = [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1],
    ]
    checks = {
        "selection_distribution_shift": abs(selection["rows"][0]["selected_share"] - 0.45 / 0.57) < 1e-12,
        "minhash_enumeration_equals_jaccard": abs(minhash["enumerated_minhash_probability"] - minhash["exact_jaccard"]) < 1e-12,
        "lsh_candidate_probability": abs(minhash["lsh"]["candidate_probability"] - (1 - (1 - 0.8**4) ** 10)) < 1e-12,
        "threshold_clustering_nontransitive": clustering["edges"] == ["A-B", "B-C"] and clustering["pair_jaccard"]["A-C"] < 0.5,
        "contamination_bayes_base_rate": abs(contamination["positive_posterior"] - 0.018 / 0.0278) < 1e-12,
        "mixture_document_token_target_separation": [row["target_share"] for row in mixture["rows"]] == [1 / 3, 2 / 3],
        "packing_relation_boundary_loss_contract": packing["bins"] == [[6, 4], [5, 3, 2]] and packing["relation"] == expected_relation and packing["loss_mask"] == [1, 0, 1, 1],
        "curriculum_update_order_noncommutes": abs(curriculum["AB"]["final"] + 0.12) < 1e-12 and abs(curriculum["BA"]["final"] + 0.08) < 1e-12,
        "provenance_effective_target_and_hash_stability": provenance["effective_targets"] == 4 and provenance["mean_nll"] == 1.5 and provenance["manifest_hash_a"] == provenance["manifest_hash_b"],
    }

    payload = {
        "experiment_id": "EXP-LM-703-V1",
        "checks": checks,
        "selection": selection,
        "minhash_lsh": minhash,
        "threshold_clustering": clustering,
        "contamination": contamination,
        "mixture": mixture,
        "packing": packing,
        "curriculum": curriculum,
        "provenance": provenance,
    }
    (args.out / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    write_csv(
        args.out / "selection_ledger.csv",
        ["group", "source_share", "retention", "kept_mass", "selected_share"],
        selection["rows"],
    )
    similarity_rows = [
        {"object": "minhash", "parameter": "J(A,B)", "value": minhash["exact_jaccard"], "meaning": "exact_oracle"},
        {"object": "lsh", "parameter": "candidate_probability", "value": minhash["lsh"]["candidate_probability"], "meaning": "retrieval_not_truth"},
    ]
    similarity_rows.extend(
        {"object": "cluster", "parameter": pair, "value": value, "meaning": "verified_pair_jaccard"}
        for pair, value in clustering["pair_jaccard"].items()
    )
    similarity_rows.append(
        {"object": "contamination", "parameter": "positive_posterior", "value": contamination["positive_posterior"], "meaning": "depends_on_base_rate"}
    )
    write_csv(
        args.out / "similarity_contamination_ledger.csv",
        ["object", "parameter", "value", "meaning"],
        similarity_rows,
    )
    training_rows = []
    for row in mixture["rows"]:
        training_rows.extend(
            [
                {"object": f'domain_{row["domain"]}', "measure": "document_share", "value": row["document_share"], "unit": "fraction"},
                {"object": f'domain_{row["domain"]}', "measure": "token_share", "value": row["token_share"], "unit": "fraction"},
                {"object": f'domain_{row["domain"]}', "measure": "target_share", "value": row["target_share"], "unit": "fraction"},
            ]
        )
    training_rows.extend(
        [
            {"object": "packing", "measure": "utilization", "value": packing["utilization"], "unit": "fraction"},
            {"object": "curriculum", "measure": "AB_final", "value": curriculum["AB"]["final"], "unit": "theta"},
            {"object": "curriculum", "measure": "BA_final", "value": curriculum["BA"]["final"], "unit": "theta"},
            {"object": "provenance", "measure": "effective_targets", "value": provenance["effective_targets"], "unit": "targets"},
            {"object": "provenance", "measure": "mean_nll", "value": provenance["mean_nll"], "unit": "nats_per_target"},
        ]
    )
    write_csv(
        args.out / "training_accounting_ledger.csv",
        ["object", "measure", "value", "unit"],
        training_rows,
    )

    write_selection_svg(args.plots / "plot-language-pretraining-selection-v1.svg", selection)
    write_similarity_svg(
        args.plots / "plot-language-pretraining-similarity-contamination-v1.svg",
        minhash,
        clustering,
        contamination,
    )
    write_training_svg(
        args.plots / "plot-language-pretraining-training-contracts-v1.svg",
        mixture,
        packing,
        curriculum,
        provenance,
    )

    print(json.dumps({"checks": checks, "out": str(args.out), "plots": str(args.plots)}, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
