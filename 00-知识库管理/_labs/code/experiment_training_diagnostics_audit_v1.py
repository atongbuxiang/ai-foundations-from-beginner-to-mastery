#!/usr/bin/env python3
"""Deterministic standard-library audit for TRN-65--TRN-72.

Ten tracks cover clock alignment, first-bad-event localization, UWR/spectrum,
confounding, factorial interactions, paired variance, finite-horizon sequential
boundaries, checkpoint-selection optimism, compute matching, and research-ledger
completeness. The script writes one JSON, ten CSV files, and three SVG figures.

No external numerical, plotting, ML, GPU, distributed, or network dependency is
required. The examples are exact/finite teaching oracles, not model benchmarks.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Sequence


SEED = 20260826
BLUE, TEAL, AMBER, RED = "#2563EB", "#0F766E", "#B7791F", "#C24135"
INK, MUTED, GRID, BG = "#1F2937", "#64748B", "#D7DEE8", "#FFFEFB"
FONT = "Inter, PingFang SC, Noto Sans CJK SC, sans-serif"


def clock_alignment_audit() -> List[Dict]:
    batches = ((1000, 990), (980, 1020), (1005, 995), (970, 1030))
    outcomes = ("success", "overflow", "success", "success")
    rows, micro, update, token = [], 0, 0, 0
    for attempt, (counts, outcome) in enumerate(zip(batches, outcomes), start=1):
        before = update
        micro += len(counts)
        token += sum(counts)
        if outcome == "success":
            update += 1
        rows.append({
            "attempt": attempt, "outcome": outcome,
            "microstep_clock": micro, "optimizer_step_before": before,
            "optimizer_step_after": update, "effective_token_clock": token,
            "scheduler_by_update": update, "scheduler_by_attempt": attempt,
            "skipped_update": int(outcome == "overflow"),
        })
    return rows


def first_bad_event_audit() -> List[Dict]:
    lo, hi, true_first = 12000, 12512, 12341
    rows, round_id = [], 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        bad = mid >= true_first
        rows.append({
            "round": round_id, "normal_lower": lo, "bad_upper": hi,
            "midpoint": mid, "midpoint_bad": int(bad),
            "interval_width_before": hi - lo,
        })
        if bad:
            hi = mid
        else:
            lo = mid
        round_id += 1
    rows.append({
        "round": round_id, "normal_lower": lo, "bad_upper": hi,
        "midpoint": hi, "midpoint_bad": 1,
        "interval_width_before": hi - lo,
    })
    return rows


def uwr_spectrum_audit() -> List[Dict]:
    d = 100
    cases = (
        ("rank_one", 1.0, 1.0, 1.0),
        ("rank_25_equal", 1.0, 0.2, 25.0),
        ("rank_100_equal", 1.0, 0.1, 100.0),
    )
    rows = []
    for name, frob, spectral, stable_rank in cases:
        rows.append({
            "case": name, "dimension": d,
            "frobenius_norm": frob, "entry_rms": frob / d,
            "spectral_norm": spectral, "stable_rank": stable_rank,
            "weight_frobenius_norm": 20.0, "weight_spectral_norm": 8.0,
            "frobenius_uwr": frob / 20.0,
            "spectral_uwr": spectral / 8.0,
        })
    return rows


def confounding_simpson_audit() -> List[Dict]:
    groups = (
        ("short", 0.90, 0.92, 0.80, 0.20),
        ("long", 0.60, 0.65, 0.20, 0.80),
    )
    old_total = sum(old * w_old for _, old, _, w_old, _ in groups)
    new_total = sum(new * w_new for _, _, new, _, w_new in groups)
    new_standardized = sum(new * w_old for _, _, new, w_old, _ in groups)
    return [{
        "group": group, "old_success": old, "new_success": new,
        "within_group_effect": new - old,
        "old_group_weight": w_old, "new_group_weight": w_new,
        "old_crude_success": old_total, "new_crude_success": new_total,
        "new_standardized_to_old_mix": new_standardized,
        "standardized_effect": new_standardized - old_total,
    } for group, old, new, w_old, w_new in groups]


def factorial_interaction_audit() -> List[Dict]:
    cells = ((-1, -1, 10.0), (1, -1, 14.0), (-1, 1, 12.0), (1, 1, 22.0))
    beta0 = sum(y for _, _, y in cells) / 4.0
    beta_a = sum(a * y for a, _, y in cells) / 4.0
    beta_b = sum(b * y for _, b, y in cells) / 4.0
    beta_ab = sum(a * b * y for a, b, y in cells) / 4.0
    return [{
        "A": a, "B": b, "response": y,
        "beta0": beta0, "beta_A": beta_a, "beta_B": beta_b,
        "beta_AB": beta_ab, "A_effect": 2 * beta_a,
        "B_effect": 2 * beta_b, "difference_in_differences": 4 * beta_ab,
    } for a, b, y in cells]


def paired_variance_audit() -> List[Dict]:
    a = (10.0, 12.0, 9.0, 13.0, 11.0, 14.0)
    b = (9.3, 11.4, 8.5, 12.2, 10.6, 13.1)
    diffs = tuple(x - y for x, y in zip(a, b))
    ma, mb = mean(a), mean(b)
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (len(a) - 1)
    var_a, var_b = stdev(a) ** 2, stdev(b) ** 2
    var_d = stdev(diffs) ** 2
    return [{
        "pair": i + 1, "A": x, "B": y, "difference": d,
        "mean_difference": mean(diffs), "paired_difference_variance": var_d,
        "unpaired_sum_variance": var_a + var_b,
        "sample_covariance": cov,
        "variance_identity_rhs": var_a + var_b - 2 * cov,
    } for i, (x, y, d) in enumerate(zip(a, b, diffs))]


def sequential_boundary_audit() -> List[Dict]:
    # Bounded observations in [-1, 1]. Union-bound Hoeffding is simultaneous
    # over the finite, predeclared horizon T; it is a teaching proxy, not the
    # tighter confidence-sequence constructions in Howard et al.
    observations = (0.2, -0.1, 0.4, 0.3, -0.2, 0.5, 0.1, 0.4, 0.2, 0.3,
                    0.6, -0.1, 0.3, 0.2, 0.4, 0.5, 0.0, 0.4, 0.3, 0.2)
    alpha, horizon = 0.05, len(observations)
    rows, total = [], 0.0
    for t, x in enumerate(observations, start=1):
        total += x
        mu = total / t
        fixed = math.sqrt(2.0 * math.log(2.0 / alpha) / t)
        uniform = math.sqrt(2.0 * math.log(2.0 * horizon / alpha) / t)
        rows.append({
            "t": t, "observation": x, "running_mean": mu,
            "fixed_time_hoeffding_halfwidth": fixed,
            "finite_horizon_uniform_halfwidth": uniform,
            "fixed_lower": mu - fixed, "fixed_upper": mu + fixed,
            "uniform_lower": mu - uniform, "uniform_upper": mu + uniform,
            "alpha": alpha, "declared_horizon": horizon,
        })
    return rows


def checkpoint_selection_audit() -> List[Dict]:
    true_risk = 1.0
    runs = (
        (0.10, -0.04, 0.03, -0.08, 0.02, 0.05),
        (0.02, -0.11, 0.07, 0.04, -0.03, 0.01),
        (-0.05, 0.03, -0.02, 0.06, -0.09, 0.04),
    )
    rows = []
    for replicate, noises in enumerate(runs, start=1):
        observed = tuple(true_risk + e for e in noises)
        idx = min(range(len(observed)), key=observed.__getitem__)
        for k, (noise, risk) in enumerate(zip(noises, observed), start=1):
            rows.append({
                "replicate": replicate, "checkpoint": k, "true_risk": true_risk,
                "validation_noise": noise, "observed_validation_risk": risk,
                "selected": int(k - 1 == idx), "selected_observed_risk": observed[idx],
                "selection_optimism": true_risk - observed[idx],
            })
    return rows


def compute_matching_audit() -> List[Dict]:
    methods = (
        ("A", 120_000.0, 30e9, 40, 5, 0.04),
        ("B", 100_000.0, 20e9, 10, 1, 0.02),
    )
    return [{
        "method": m, "throughput_tokens_per_second": rate,
        "tokens_to_quality": tokens, "time_to_quality_seconds": tokens / rate,
        "tuning_trials": trials, "failed_runs": failures,
        "locked_test_loss_improvement": quality,
        "throughput_rank": 1 if m == "A" else 2,
        "time_to_quality_rank": 2 if m == "A" else 1,
        "total_trial_plus_failure_count": trials + failures,
    } for m, rate, tokens, trials, failures, quality in methods]


def research_ledger_audit() -> List[Dict]:
    records = (
        ("claim", 8, 8, "E0"),
        ("protocol", 10, 10, "E0"),
        ("manifest", 9, 9, "E1"),
        ("telemetry", 8, 7, "E2"),
        ("incident", 9, 9, "E2"),
        ("randomized_study", 8, 8, "E3"),
        ("mechanism_intervention", 7, 5, "E4"),
        ("external_replication", 6, 2, "E5"),
    )
    return [{
        "record": name, "required_fields": required,
        "present_fields": present, "missing_fields": required - present,
        "completeness_fraction": present / required,
        "evidence_target": level,
        "claim_language_allowed": {
            "E0": "defined", "E1": "local_oracle", "E2": "compatible_timeline",
            "E3": "protocol_effect", "E4": "mechanism_discrimination",
            "E5": "bounded_external_robustness",
        }[level],
    } for name, required, present, level in records]


def write_csv(path: Path, rows: Sequence[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def svg_text(x: float, y: float, text: str, size: int = 17, color: str = INK,
             weight: int = 400, anchor: str = "start") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{color}">'
            f'{html.escape(str(text))}</text>')


def svg_start(title: str, desc: str, height: int = 700) -> List[str]:
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title>',
        f'<desc id="desc">{html.escape(desc)}</desc>',
        f'<style>text{{font-family:{FONT};}}</style>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#1F2937"/></marker></defs>',
        f'<rect width="1200" height="{height}" fill="{BG}"/>',
    ]


def write_telemetry_first_bad_svg(path: Path, clocks: Sequence[Dict], binary: Sequence[Dict]) -> None:
    s = svg_start("Telemetry clocks and first-bad-event audit", "Clock divergence after a skipped update and deterministic binary localization of the first bad training step.")
    s.append(svg_text(60, 54, "A  Skipped update makes clocks diverge", 24, INK, 700))
    x0, x1 = 90, 550
    for i, row in enumerate(clocks):
        y = 110 + i * 82
        s.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GRID}" stroke-width="2"/>')
        s.append(svg_text(65, y + 6, f"attempt {row['attempt']}", 16, MUTED))
        color = RED if row["skipped_update"] else TEAL
        s.append(f'<circle cx="210" cy="{y}" r="8" fill="{color}"/>')
        s.append(svg_text(235, y + 6, row["outcome"], 17, color, 700))
        s.append(svg_text(360, y + 6, f"micro={row['microstep_clock']}  update={row['optimizer_step_after']}  token={row['effective_token_clock']}", 16, INK))
    s.append(svg_text(80, 475, "attempt clock", 17, AMBER, 700))
    s.append(svg_text(250, 475, "!=", 18, RED, 700))
    s.append(svg_text(300, 475, "optimizer clock after overflow", 17, TEAL, 700))
    s.append(f'<line x1="620" y1="80" x2="620" y2="620" stroke="{GRID}" stroke-dasharray="6 6"/>')
    s.append(svg_text(670, 54, "B  Checkpoint bisection", 24, INK, 700))
    base_y = 130
    s.append(f'<line x1="680" y1="{base_y}" x2="1120" y2="{base_y}" stroke="{INK}" stroke-width="3"/>')
    s.append(svg_text(680, 166, "12000 normal", 16, TEAL, 700, "middle"))
    s.append(svg_text(1120, 166, "12512 bad", 16, RED, 700, "middle"))
    for i, row in enumerate(binary[:-1]):
        y = 220 + i * 35
        width = row["interval_width_before"]
        color = RED if row["midpoint_bad"] else TEAL
        s.append(svg_text(680, y, f"r{i}", 15, MUTED))
        s.append(f'<line x1="730" y1="{y-6}" x2="{730 + min(360, width * .7)}" y2="{y-6}" stroke="{GRID}" stroke-width="7"/>')
        s.append(f'<circle cx="{730 + min(360, width * .35)}" cy="{y-6}" r="6" fill="{color}"/>')
        s.append(svg_text(1110, y, f"mid={row['midpoint']}  {'bad' if row['midpoint_bad'] else 'normal'}", 15, color, 700, "end"))
    final = binary[-1]
    s.append(svg_text(670, 605, f"first bad = {final['bad_upper']} ; last normal = {final['normal_lower']}", 18, RED, 700))
    s.append(svg_text(60, 660, "These clocks and boundaries are exact teaching oracles; real replay may require tolerance and repeated localization.", 16, MUTED))
    s.append('</svg>\n')
    path.write_text("".join(s), encoding="utf-8")


def write_causal_factorial_paired_svg(path: Path, conf: Sequence[Dict], fac: Sequence[Dict], paired: Sequence[Dict]) -> None:
    s = svg_start("Confounding, factorial interaction and pairing audit", "A Simpson reversal, a two-factor contrast decomposition, and paired variance reduction appear in three scientific panels.")
    s.append(svg_text(60, 54, "A  Simpson reversal after a composition shift", 22, INK, 700))
    old, new = conf[0]["old_crude_success"], conf[0]["new_crude_success"]
    std = conf[0]["new_standardized_to_old_mix"]
    for i, (label, value, color) in enumerate((("old crude", old, BLUE), ("new crude", new, RED), ("new standardized", std, TEAL))):
        y = 115 + i * 58
        s.append(svg_text(70, y + 6, label, 16, color, 700))
        s.append(f'<line x1="225" y1="{y}" x2="{225 + value * 300}" y2="{y}" stroke="{color}" stroke-width="12"/>')
        s.append(svg_text(540, y + 6, f"{value:.3f}", 16, INK, 700, "end"))
    s.append(svg_text(70, 310, "Within each length group, new > old.", 16, MUTED))
    s.append(svg_text(70, 338, "The crude reversal comes only from mixture weights.", 16, MUTED))
    s.append(f'<line x1="590" y1="75" x2="590" y2="640" stroke="{GRID}" stroke-dasharray="6 6"/>')
    s.append(svg_text(630, 54, "B  2 x 2 contrast", 22, INK, 700))
    cells = {(r["A"], r["B"]): r["response"] for r in fac}
    for j, b in enumerate((-1, 1)):
        for i, a in enumerate((-1, 1)):
            x, y = 650 + i * 150, 100 + j * 150
            color = TEAL if (a, b) == (1, 1) else GRID
            s.append(f'<rect x="{x}" y="{y}" width="120" height="105" fill="none" stroke="{color}" stroke-width="3"/>')
            s.append(svg_text(x + 60, y + 42, f"A={a:+d}, B={b:+d}", 15, MUTED, 400, "middle"))
            s.append(svg_text(x + 60, y + 78, f"Y={cells[(a,b)]:.0f}", 22, TEAL if color == TEAL else INK, 700, "middle"))
    s.append(svg_text(955, 115, f"A effect = {fac[0]['A_effect']:.1f}", 17, BLUE, 700))
    s.append(svg_text(955, 155, f"B effect = {fac[0]['B_effect']:.1f}", 17, TEAL, 700))
    s.append(svg_text(955, 195, f"interaction DiD = {fac[0]['difference_in_differences']:.1f}", 17, RED, 700))
    s.append(svg_text(955, 240, "Main effects do not replace", 16, MUTED))
    s.append(svg_text(955, 268, "conditional effects.", 16, MUTED))
    s.append(f'<line x1="620" y1="370" x2="1135" y2="370" stroke="{GRID}" stroke-dasharray="6 6"/>')
    s.append(svg_text(630, 420, "C  Pair shared difficulty before estimating the effect", 22, INK, 700))
    for i, row in enumerate(paired):
        y1 = 470 + (row["A"] - 9) * 24
        y2 = 470 + (row["B"] - 9) * 24
        s.append(f'<line x1="720" y1="{y1}" x2="930" y2="{y2}" stroke="{GRID}" stroke-width="2"/>')
        s.append(f'<circle cx="720" cy="{y1}" r="6" fill="{BLUE}"/><circle cx="930" cy="{y2}" r="6" fill="{TEAL}"/>')
    s.append(svg_text(720, 455, "A", 18, BLUE, 700, "middle"))
    s.append(svg_text(930, 455, "B", 18, TEAL, 700, "middle"))
    s.append(svg_text(995, 500, f"Var paired = {paired[0]['paired_difference_variance']:.3f}", 16, TEAL, 700))
    s.append(svg_text(995, 535, f"Var unpaired = {paired[0]['unpaired_sum_variance']:.3f}", 16, RED, 700))
    s.append(svg_text(60, 665, "Finite examples identify estimators and counterexamples; they do not supply a universal effect size or seed count.", 16, MUTED))
    s.append('</svg>\n')
    path.write_text("".join(s), encoding="utf-8")


def write_selection_sequential_ledger_svg(path: Path, seq: Sequence[Dict], ckpt: Sequence[Dict], ledger: Sequence[Dict]) -> None:
    s = svg_start("Selection, sequential boundaries and evidence ledger audit", "Checkpoint selection optimism, fixed-time versus finite-horizon uniform bounds, and evidence completeness are separated.")
    s.append(svg_text(60, 54, "A  Minimum selection captures negative noise", 22, INK, 700))
    rep = [r for r in ckpt if r["replicate"] == 1]
    for i, row in enumerate(rep):
        x = 85 + i * 78
        y = 250 - (row["observed_validation_risk"] - 0.9) * 650
        color = RED if row["selected"] else BLUE
        s.append(f'<circle cx="{x}" cy="{y}" r="{9 if row["selected"] else 6}" fill="{color}"/>')
        if i:
            prev = rep[i-1]
            px = 85 + (i-1) * 78
            py = 250 - (prev["observed_validation_risk"] - 0.9) * 650
            s.append(f'<line x1="{px}" y1="{py}" x2="{x}" y2="{y}" stroke="{GRID}" stroke-width="2"/>')
        s.append(svg_text(x, 310, f"c{i+1}", 15, MUTED, 400, "middle"))
    s.append(f'<line x1="75" y1="185" x2="500" y2="185" stroke="{TEAL}" stroke-dasharray="7 5" stroke-width="2"/>')
    s.append(svg_text(500, 175, "true risk", 16, TEAL, 700, "end"))
    selected = next(r for r in rep if r["selected"])
    s.append(svg_text(75, 350, f"selected optimism = {selected['selection_optimism']:.2f}", 17, RED, 700))
    s.append(f'<line x1="560" y1="75" x2="560" y2="400" stroke="{GRID}" stroke-dasharray="6 6"/>')
    s.append(svg_text(600, 54, "B  Repeated looks need a wider bound", 22, INK, 700))
    x0, y0, w, h = 620, 320, 500, 220
    s.append(f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="{INK}"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-h}" stroke="{INK}"/>')
    def points(key: str, sign: float = 1.0) -> str:
        vals = []
        visible = seq[1:]
        for row in visible:
            x = x0 + (row["t"] - 2) * w / (len(visible) - 1)
            y = 215 - (row["running_mean"] + sign * row[key]) * 38
            vals.append(f"{x:.1f},{y:.1f}")
        return " ".join(vals)
    s.append(f'<polyline points="{points("finite_horizon_uniform_halfwidth")}" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    s.append(f'<polyline points="{points("finite_horizon_uniform_halfwidth", -1)}" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    mean_points = []
    visible = seq[1:]
    for row in visible:
        x = x0 + (row["t"] - 2) * w / (len(visible) - 1)
        y = 215 - row["running_mean"] * 38
        mean_points.append(f"{x:.1f},{y:.1f}")
    s.append(f'<polyline points="{" ".join(mean_points)}" fill="none" stroke="{BLUE}" stroke-width="4"/>')
    s.append(svg_text(870, 365, "finite-horizon simultaneous bound", 16, RED, 700, "middle"))
    s.append(f'<line x1="60" y1="415" x2="1140" y2="415" stroke="{GRID}"/>')
    s.append(svg_text(60, 458, "C  Ledger completeness is not evidence level", 22, INK, 700))
    for i, row in enumerate(ledger):
        x, y = 70 + (i % 4) * 275, 495 + (i // 4) * 80
        color = TEAL if row["missing_fields"] == 0 else (AMBER if row["completeness_fraction"] >= .7 else RED)
        s.append(svg_text(x, y, f"{row['record']} · {row['evidence_target']}", 16, color, 700))
        s.append(f'<line x1="{x}" y1="{y+24}" x2="{x+220}" y2="{y+24}" stroke="{GRID}" stroke-width="8"/><line x1="{x}" y1="{y+24}" x2="{x+220*row["completeness_fraction"]}" y2="{y+24}" stroke="{color}" stroke-width="8"/>')
        s.append(svg_text(x, y + 52, f"missing {row['missing_fields']} fields", 15, MUTED))
    s.append(svg_text(60, 680, "A complete E2 timeline is still not an E3 randomized intervention; scope and evidence language remain explicit.", 16, MUTED))
    s.append('</svg>\n')
    path.write_text("".join(s), encoding="utf-8")


def add_check(checks: List[Dict], check_id: str, condition: bool, expected, observed) -> None:
    checks.append({"id": check_id, "passed": bool(condition), "expected": expected, "observed": observed})


def main() -> None:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[3]
    parser.add_argument("--output-dir", type=Path, default=root / "00-知识库管理/_labs/experiments/trn60.9-training-diagnostics-audit-v1")
    parser.add_argument("--plot-dir", type=Path, default=root / "00-知识库管理/_assets/plots/training-optimization")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)

    tracks = {
        "clock_alignment": clock_alignment_audit(),
        "first_bad_event": first_bad_event_audit(),
        "uwr_spectrum": uwr_spectrum_audit(),
        "confounding_simpson": confounding_simpson_audit(),
        "factorial_interaction": factorial_interaction_audit(),
        "paired_variance": paired_variance_audit(),
        "sequential_boundary": sequential_boundary_audit(),
        "checkpoint_selection": checkpoint_selection_audit(),
        "compute_matching": compute_matching_audit(),
        "research_ledger": research_ledger_audit(),
    }
    csv_paths = []
    for name, rows in tracks.items():
        target = args.output_dir / f"{name}.csv"
        write_csv(target, rows)
        csv_paths.append(target)

    plot_paths = [
        args.plot_dir / "plot-telemetry-first-bad-audit-v1.svg",
        args.plot_dir / "plot-causal-factorial-paired-audit-v1.svg",
        args.plot_dir / "plot-selection-sequential-ledger-audit-v1.svg",
    ]
    write_telemetry_first_bad_svg(plot_paths[0], tracks["clock_alignment"], tracks["first_bad_event"])
    write_causal_factorial_paired_svg(plot_paths[1], tracks["confounding_simpson"], tracks["factorial_interaction"], tracks["paired_variance"])
    write_selection_sequential_ledger_svg(plot_paths[2], tracks["sequential_boundary"], tracks["checkpoint_selection"], tracks["research_ledger"])

    checks: List[Dict] = []
    c, f, u, conf, fac = (tracks[k] for k in ("clock_alignment", "first_bad_event", "uwr_spectrum", "confounding_simpson", "factorial_interaction"))
    pair, seq, ck, comp, led = (tracks[k] for k in ("paired_variance", "sequential_boundary", "checkpoint_selection", "compute_matching", "research_ledger"))
    add_check(checks, "CLK-01", c[-1]["microstep_clock"] == 8, 8, c[-1]["microstep_clock"])
    add_check(checks, "CLK-02", c[-1]["optimizer_step_after"] == 3, 3, c[-1]["optimizer_step_after"])
    add_check(checks, "CLK-03", c[-1]["effective_token_clock"] == 7990, 7990, c[-1]["effective_token_clock"])
    add_check(checks, "CLK-04", c[1]["scheduler_by_attempt"] != c[1]["scheduler_by_update"], "diverge", [c[1]["scheduler_by_attempt"], c[1]["scheduler_by_update"]])
    add_check(checks, "BAD-01", f[-1]["bad_upper"] == 12341, 12341, f[-1]["bad_upper"])
    add_check(checks, "BAD-02", f[-1]["normal_lower"] == 12340, 12340, f[-1]["normal_lower"])
    add_check(checks, "BAD-03", len(f) <= 10, "<=10", len(f))
    add_check(checks, "BAD-04", f[-1]["interval_width_before"] == 1, 1, f[-1]["interval_width_before"])
    add_check(checks, "UWR-01", math.isclose(u[0]["entry_rms"], .01), .01, u[0]["entry_rms"])
    add_check(checks, "UWR-02", u[0]["stable_rank"] == 1, 1, u[0]["stable_rank"])
    add_check(checks, "UWR-03", u[2]["stable_rank"] == 100, 100, u[2]["stable_rank"])
    add_check(checks, "UWR-04", u[0]["spectral_uwr"] > u[2]["spectral_uwr"], "rank-one larger", [u[0]["spectral_uwr"], u[2]["spectral_uwr"]])
    add_check(checks, "CFD-01", all(r["within_group_effect"] > 0 for r in conf), "both positive", [r["within_group_effect"] for r in conf])
    add_check(checks, "CFD-02", conf[0]["new_crude_success"] < conf[0]["old_crude_success"], "crude reversal", [conf[0]["old_crude_success"], conf[0]["new_crude_success"]])
    add_check(checks, "CFD-03", conf[0]["standardized_effect"] > 0, "positive standardized", conf[0]["standardized_effect"])
    add_check(checks, "CFD-04", math.isclose(conf[0]["new_standardized_to_old_mix"], .866), .866, conf[0]["new_standardized_to_old_mix"])
    add_check(checks, "FAC-01", fac[0]["beta_A"] == 3.5, 3.5, fac[0]["beta_A"])
    add_check(checks, "FAC-02", fac[0]["beta_B"] == 2.5, 2.5, fac[0]["beta_B"])
    add_check(checks, "FAC-03", fac[0]["beta_AB"] == 1.5, 1.5, fac[0]["beta_AB"])
    add_check(checks, "FAC-04", fac[0]["difference_in_differences"] == 6, 6, fac[0]["difference_in_differences"])
    add_check(checks, "PAIR-01", math.isclose(pair[0]["paired_difference_variance"], pair[0]["variance_identity_rhs"]), "variance identity", [pair[0]["paired_difference_variance"], pair[0]["variance_identity_rhs"]])
    add_check(checks, "PAIR-02", pair[0]["paired_difference_variance"] < pair[0]["unpaired_sum_variance"], "paired smaller", [pair[0]["paired_difference_variance"], pair[0]["unpaired_sum_variance"]])
    add_check(checks, "PAIR-03", pair[0]["sample_covariance"] > 0, "positive covariance", pair[0]["sample_covariance"])
    add_check(checks, "PAIR-04", len(pair) == 6, 6, len(pair))
    add_check(checks, "SEQ-01", all(r["finite_horizon_uniform_halfwidth"] > r["fixed_time_hoeffding_halfwidth"] for r in seq), "uniform wider", "all")
    add_check(checks, "SEQ-02", seq[-1]["declared_horizon"] == 20, 20, seq[-1]["declared_horizon"])
    add_check(checks, "SEQ-03", seq[-1]["uniform_lower"] < seq[-1]["running_mean"] < seq[-1]["uniform_upper"], "mean inside", [seq[-1]["uniform_lower"], seq[-1]["running_mean"], seq[-1]["uniform_upper"]])
    add_check(checks, "SEQ-04", seq[-1]["finite_horizon_uniform_halfwidth"] < seq[0]["finite_horizon_uniform_halfwidth"], "shrinks", [seq[0]["finite_horizon_uniform_halfwidth"], seq[-1]["finite_horizon_uniform_halfwidth"]])
    add_check(checks, "CKPT-01", sum(r["selected"] for r in ck) == 3, 3, sum(r["selected"] for r in ck))
    add_check(checks, "CKPT-02", all(r["selection_optimism"] > 0 for r in ck if r["selected"]), "positive optimism", [r["selection_optimism"] for r in ck if r["selected"]])
    add_check(checks, "CKPT-03", len({r["checkpoint"] for r in ck if r["selected"]}) >= 2, ">=2 selected indices", sorted({r["checkpoint"] for r in ck if r["selected"]}))
    add_check(checks, "CKPT-04", len(ck) == 18, 18, len(ck))
    add_check(checks, "CMP-01", comp[0]["throughput_tokens_per_second"] > comp[1]["throughput_tokens_per_second"], "A throughput higher", [comp[0]["throughput_tokens_per_second"], comp[1]["throughput_tokens_per_second"]])
    add_check(checks, "CMP-02", comp[0]["time_to_quality_seconds"] > comp[1]["time_to_quality_seconds"], "A time worse", [comp[0]["time_to_quality_seconds"], comp[1]["time_to_quality_seconds"]])
    add_check(checks, "CMP-03", comp[0]["total_trial_plus_failure_count"] == 45, 45, comp[0]["total_trial_plus_failure_count"])
    add_check(checks, "CMP-04", comp[1]["time_to_quality_seconds"] == 200000, 200000, comp[1]["time_to_quality_seconds"])
    add_check(checks, "LED-01", sum(r["missing_fields"] for r in led) == 7, 7, sum(r["missing_fields"] for r in led))
    add_check(checks, "LED-02", next(r for r in led if r["record"] == "incident")["missing_fields"] == 0, 0, next(r for r in led if r["record"] == "incident")["missing_fields"])
    add_check(checks, "LED-03", next(r for r in led if r["record"] == "external_replication")["evidence_target"] == "E5", "E5", next(r for r in led if r["record"] == "external_replication")["evidence_target"])
    add_check(checks, "LED-04", len(led) == 8, 8, len(led))

    if not all(item["passed"] for item in checks):
        failed = [item for item in checks if not item["passed"]]
        raise AssertionError(json.dumps(failed, ensure_ascii=False, indent=2))

    artifacts = csv_paths + plot_paths
    summary = {
        "experiment_id": "EXP-TRN-609-V1",
        "seed": SEED,
        "track_count": len(tracks),
        "check_count": len(checks),
        "checks_passed": sum(item["passed"] for item in checks),
        "checks": checks,
        "key_results": {
            "clock_final": c[-1], "first_bad_boundary": f[-1],
            "simpson": {k: conf[0][k] for k in ("old_crude_success", "new_crude_success", "new_standardized_to_old_mix", "standardized_effect")},
            "factorial": {k: fac[0][k] for k in ("beta_A", "beta_B", "beta_AB", "difference_in_differences")},
            "paired_variance_ratio": pair[0]["paired_difference_variance"] / pair[0]["unpaired_sum_variance"],
            "time_to_quality": {r["method"]: r["time_to_quality_seconds"] for r in comp},
            "ledger_missing_fields": {r["record"]: r["missing_fields"] for r in led},
        },
        "boundaries": [
            "Synthetic deterministic or finite analytical oracles are not a real training benchmark.",
            "The finite-horizon union-bound interval is a valid teaching construction under bounded observations, not a substitute for a chosen production confidence-sequence method.",
            "Telemetry ordering and a complete ledger do not by themselves identify causality.",
            "Compute and checkpoint results are protocol examples, not universal model rankings.",
        ],
        "artifact_sha256": {p.name: sha256(p) for p in artifacts},
    }
    result_path = args.output_dir / "results.json"
    result_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(checks)}/{len(checks)} checks passed")
    print(f"wrote {1 + len(artifacts)} files including results.json")


if __name__ == "__main__":
    main()
