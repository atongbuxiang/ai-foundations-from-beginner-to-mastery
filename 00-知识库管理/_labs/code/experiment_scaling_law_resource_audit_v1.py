#!/usr/bin/env python3
"""Deterministic standard-library audit for TRN-49--TRN-56.

The experiment separates offset-aware slopes, finite-window extrapolation,
joint N-D identifiability, compute-optimal allocation, model/system/energy
ledgers, repeated-token value, data-mixture trade-offs, inference-aware
break-even decisions, broken scaling and metric-induced emergence, and
held-out-scale evidence accounting.

It writes one JSON, ten CSV files, and three self-contained SVG figures.
NumPy, SciPy, plotting packages, and network access are deliberately not
required.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


SEED = 20260826
BLUE = "#2563EB"
TEAL = "#0F766E"
AMBER = "#B76E00"
RED = "#C0392B"
INK = "#172033"
MUTED = "#52606D"
GRID = "#D9E0E7"
BACKGROUND = "#FFFEFB"


def offset_slope_audit() -> List[Dict]:
    rows = []
    floor, amplitude, exponent = 1.0, 4.0, 0.5
    for scale in (1, 4, 16, 64, 256, 1024):
        excess = amplitude * scale ** (-exponent)
        loss = floor + excess
        rows.append(
            {
                "scale": scale,
                "floor": floor,
                "loss": loss,
                "excess_loss": excess,
                "raw_log_slope": -exponent * (1.0 - floor / loss),
                "excess_log_slope": -exponent,
            }
        )
    return rows


def extrapolation_family_audit() -> List[Dict]:
    calibration = (100.0, 1000.0)

    def true_loss(scale: float) -> float:
        return 1.0 + scale ** -0.5

    first, second = (true_loss(scale) for scale in calibration)
    zero_exponent = -math.log(second / first) / math.log(calibration[1] / calibration[0])
    zero_amplitude = first * calibration[0] ** zero_exponent
    rows = []
    for scale, split in (
        (100.0, "calibration"),
        (1000.0, "calibration"),
        (10000.0, "validation"),
        (1_000_000.0, "heldout"),
        (100_000_000.0, "heldout"),
    ):
        truth = true_loss(scale)
        zero_prediction = zero_amplitude * scale ** (-zero_exponent)
        offset_prediction = 1.0 + scale ** -0.5
        rows.append(
            {
                "scale": scale,
                "split": split,
                "true_loss": truth,
                "zero_offset_prediction": zero_prediction,
                "offset_prediction": offset_prediction,
                "zero_offset_absolute_error": abs(zero_prediction - truth),
                "offset_absolute_error": abs(offset_prediction - truth),
                "fitted_zero_offset_exponent": zero_exponent,
            }
        )
    return rows


def joint_identifiability_audit() -> List[Dict]:
    rows = []
    for model_size in (1.0, 16.0, 256.0):
        data_size = math.sqrt(model_size)
        parameter_term = 2.0 * model_size ** -0.25
        data_term = 3.0 * data_size ** -0.5
        rows.append(
            {
                "design": "diagonal_D_equals_sqrt_N",
                "model_size": model_size,
                "data_size": data_size,
                "parameter_term": parameter_term,
                "data_term": data_term,
                "loss": 1.0 + parameter_term + data_term,
                "parameter_path_exponent": -0.25,
                "data_path_exponent": -0.25,
            }
        )
    for model_size in (1.0, 16.0, 256.0):
        for data_size in (1.0, 4.0, 16.0):
            parameter_term = 2.0 * model_size ** -0.25
            data_term = 3.0 * data_size ** -0.5
            rows.append(
                {
                    "design": "crossed_grid",
                    "model_size": model_size,
                    "data_size": data_size,
                    "parameter_term": parameter_term,
                    "data_term": data_term,
                    "loss": 1.0 + parameter_term + data_term,
                    "parameter_path_exponent": -0.25,
                    "data_path_exponent": -0.5,
                }
            )
    return rows


def compute_optimal_audit() -> List[Dict]:
    alpha, beta, amplitude_n, amplitude_d, kappa = 0.34, 0.28, 1.0, 1.0, 1.0
    rows = []
    for budget in (1.0e4, 1.0e6, 1.0e8):
        optimum_n = (
            (alpha * amplitude_n) / (beta * amplitude_d)
            * (budget / kappa) ** beta
        ) ** (1.0 / (alpha + beta))
        optimum_d = budget / (kappa * optimum_n)
        optimum_excess = amplitude_n * optimum_n ** -alpha + amplitude_d * optimum_d ** -beta
        for multiplier in (0.25, 0.5, 1.0, 2.0, 4.0):
            model_size = optimum_n * multiplier
            data_size = budget / (kappa * model_size)
            parameter_term = amplitude_n * model_size ** -alpha
            data_term = amplitude_d * data_size ** -beta
            excess = parameter_term + data_term
            rows.append(
                {
                    "compute_budget": budget,
                    "model_multiplier_from_optimum": multiplier,
                    "model_size": model_size,
                    "data_size": data_size,
                    "constraint_product": kappa * model_size * data_size,
                    "parameter_term": parameter_term,
                    "data_term": data_term,
                    "weighted_parameter_margin": alpha * parameter_term,
                    "weighted_data_margin": beta * data_term,
                    "excess_loss": excess,
                    "relative_regret": excess / optimum_excess - 1.0,
                    "analytic_N_exponent": beta / (alpha + beta),
                    "analytic_D_exponent": alpha / (alpha + beta),
                }
            )
    return rows


def compute_system_ledger_audit() -> List[Dict]:
    model_flops = 1.8e21
    specifications = (
        ("efficient", 1.05, 2.0e18, 0.45, 0.80, 1.10, 0.12),
        ("recompute", 1.35, 2.0e18, 0.38, 0.90, 1.12, 0.20),
        ("legacy", 1.10, 1.0e18, 0.30, 0.70, 1.18, 0.45),
    )
    rows = []
    for name, execution_multiplier, peak, mfu, power_mw, pue, intensity in specifications:
        seconds = model_flops / (peak * mfu)
        hours = seconds / 3600.0
        executed_flops = execution_multiplier * model_flops
        hfu = executed_flops / (peak * seconds)
        facility_energy_mwh = power_mw * hours * pue
        carbon_tonnes = facility_energy_mwh * intensity
        rows.append(
            {
                "system": name,
                "model_flops": model_flops,
                "execution_multiplier": execution_multiplier,
                "executed_flops": executed_flops,
                "peak_flops_per_second": peak,
                "mfu": mfu,
                "hfu": hfu,
                "wall_seconds": seconds,
                "wall_hours": hours,
                "average_it_power_mw": power_mw,
                "pue": pue,
                "grid_intensity_kg_per_kwh": intensity,
                "facility_energy_mwh": facility_energy_mwh,
                "carbon_tonnes": carbon_tonnes,
            }
        )
    return rows


def repeated_token_audit() -> List[Dict]:
    unique_tokens_billion, retention = 100.0, 0.6
    rows = []
    for repetitions in range(1, 11):
        effective = unique_tokens_billion * (1.0 - retention ** repetitions) / (1.0 - retention)
        rows.append(
            {
                "repetitions": repetitions,
                "unique_tokens_billion": unique_tokens_billion,
                "seen_tokens_billion": unique_tokens_billion * repetitions,
                "marginal_weight": retention ** (repetitions - 1),
                "effective_tokens_billion": effective,
                "asymptotic_effective_limit_billion": unique_tokens_billion / (1.0 - retention),
            }
        )
    return rows


def mixture_transfer_audit() -> List[Dict]:
    rows = []
    targets = (("balanced_deployment", 0.45), ("domain_A_heavy", 0.80))
    for target, target_weight_a in targets:
        for weight_a in (0.2, 0.4, 0.6, 0.8):
            loss_a = 2.5 - 1.2 * weight_a + 0.2 * weight_a ** 2
            loss_b = 1.4 + 0.9 * weight_a + 0.1 * weight_a ** 2
            aggregate = target_weight_a * loss_a + (1.0 - target_weight_a) * loss_b
            rows.append(
                {
                    "target": target,
                    "training_weight_A": weight_a,
                    "training_weight_B": 1.0 - weight_a,
                    "target_weight_A": target_weight_a,
                    "domain_A_loss": loss_a,
                    "domain_B_loss": loss_b,
                    "target_aggregate_loss": aggregate,
                }
            )
    return rows


def inference_break_even_audit() -> List[Dict]:
    strategies = (
        ("A_large_short", 1000.0, 2.0, 25.0),
        ("B_small_long", 1600.0, 0.8, 20.0),
        ("C_dominated", 1800.0, 1.2, 30.0),
    )
    rows = []
    for requests in (0, 250, 500, 1000, 10000):
        for name, train_cost, infer_cost, latency in strategies:
            rows.append(
                {
                    "strategy": name,
                    "requests": requests,
                    "training_cost": train_cost,
                    "per_request_cost": infer_cost,
                    "total_lifecycle_cost": train_cost + requests * infer_cost,
                    "quality_loss": 2.0,
                    "latency_ms": latency,
                    "analytic_A_B_break_even_requests": 500.0,
                }
            )
    return rows


def broken_emergence_audit() -> List[Dict]:
    rows = []
    break_scale = 64.0
    for scale in (1.0, 4.0, 16.0, 64.0, 256.0, 1024.0, 4096.0):
        latent_ratio = (scale / break_scale) ** 0.35
        per_step_probability = 0.55 + 0.35 * latent_ratio / (1.0 + latent_ratio)
        exact_match_probability = per_step_probability ** 10
        zero_success_probability_100 = (1.0 - exact_match_probability) ** 100
        transition_ratio = (scale / break_scale) ** 4
        smooth_broken_loss = scale ** -0.3 * (1.0 + transition_ratio) ** -0.1
        local_loss_exponent = -0.3 - 0.4 * transition_ratio / (1.0 + transition_ratio)
        rows.append(
            {
                "scale": scale,
                "per_step_probability": per_step_probability,
                "exact_match_probability_m10": exact_match_probability,
                "zero_success_probability_n100": zero_success_probability_100,
                "smooth_broken_loss": smooth_broken_loss,
                "local_loss_exponent": local_loss_exponent,
                "break_scale": break_scale,
            }
        )
    return rows


def heldout_evidence_audit() -> List[Dict]:
    rows = []
    scales = (1, 2, 4, 8, 16, 32, 64, 128)
    successes = (3, 3, 3, 3, 3, 3, 2, 2)
    for index, (scale, success_count) in enumerate(zip(scales, successes)):
        if index < 4:
            split, evidence_level = "calibration", "E2"
        elif index < 6:
            split, evidence_level = "validation", "E2"
        else:
            split, evidence_level = "heldout", "E3"
        observed = 1.0 + 2.0 * scale ** -0.4
        prediction = 1.01 + 1.98 * scale ** -0.395
        interval_half_width = 0.03
        lower, upper = prediction - interval_half_width, prediction + interval_half_width
        rows.append(
            {
                "scale": scale,
                "split": split,
                "planned_runs": 3,
                "successful_runs": success_count,
                "failed_runs": 3 - success_count,
                "observed_loss": observed,
                "locked_prediction": prediction,
                "prediction_lower": lower,
                "prediction_upper": upper,
                "absolute_error": abs(prediction - observed),
                "interval_covers_observation": lower <= observed <= upper,
                "evidence_level": evidence_level,
            }
        )
    return rows


def write_csv(path: Path, rows: Sequence[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def esc(value: object) -> str:
    return html.escape(str(value))


def text_element(x: float, y: float, value: object, size: int = 18, color: str = INK,
                 anchor: str = "start", weight: str = "400") -> str:
    return (
        '<text x="{:.1f}" y="{:.1f}" font-family="Inter, Arial, sans-serif" '
        'font-size="{}" fill="{}" text-anchor="{}" font-weight="{}">{}</text>'
    ).format(x, y, size, color, anchor, weight, esc(value))


def svg_header(title: str, description: str) -> List[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" '
        'viewBox="0 0 1200 800" role="img" aria-labelledby="title desc">',
        '<title id="title">{}</title>'.format(esc(title)),
        '<desc id="desc">{}</desc>'.format(esc(description)),
        '<rect width="1200" height="800" fill="{}"/>'.format(BACKGROUND),
    ]


def panel(lines: List[str], x: int, y: int, width: int, height: int, title: str) -> None:
    lines.append(
        '<rect x="{}" y="{}" width="{}" height="{}" rx="18" fill="#FFFFFF" '
        'stroke="{}" stroke-width="2"/>'.format(x, y, width, height, GRID)
    )
    lines.append(text_element(x + 24, y + 38, title, 20, INK, weight="700"))


def polyline(lines: List[str], points: Iterable, color: str, width: int = 4,
             dash: str = "") -> None:
    coordinates = " ".join("{:.1f},{:.1f}".format(x, y) for x, y in points)
    dash_attribute = ' stroke-dasharray="{}"'.format(dash) if dash else ""
    lines.append(
        '<polyline points="{}" fill="none" stroke="{}" stroke-width="{}" '
        'stroke-linecap="round" stroke-linejoin="round"{}/>'.format(
            coordinates, color, width, dash_attribute
        )
    )


def figure_offset_extrapolation(path: Path, slope_rows: Sequence[Dict],
                                extrapolation_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Offset-aware slopes and finite-window extrapolation",
        "Two textbook panels separate raw from excess-loss slopes and compare offset-aware with zero-offset extrapolation.",
    )
    lines.append(text_element(60, 58, "Scaling audit: the floor changes slopes and extrapolation", 28, INK, weight="700"))
    lines.append(text_element(60, 91, "A straight calibration segment can hide a structurally wrong asymptote.", 17, MUTED))
    panel(lines, 55, 125, 530, 590, "A  Local slope: raw loss versus excess")
    panel(lines, 615, 125, 530, 590, "B  Same calibration, different far-scale prediction")

    x_map = {row["scale"]: 105 + index * 82 for index, row in enumerate(slope_rows)}
    y_map = lambda magnitude: 610 - magnitude / 0.55 * 360
    for magnitude in (0.0, 0.1, 0.3, 0.5):
        y = y_map(magnitude)
        lines.append('<line x1="105" y1="{0:.1f}" x2="515" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(92, y + 5, magnitude, 15, MUTED, anchor="end"))
    for scale in x_map:
        lines.append(text_element(x_map[scale], 650, scale, 15, MUTED, anchor="middle"))
    polyline(lines, [(x_map[row["scale"]], y_map(-row["raw_log_slope"])) for row in slope_rows], BLUE)
    polyline(lines, [(x_map[row["scale"]], y_map(-row["excess_log_slope"])) for row in slope_rows], TEAL, dash="10 7")
    lines.append(text_element(130, 230, "excess slope magnitude = 0.5", 16, TEAL, weight="700"))
    lines.append(text_element(285, 465, "raw slope flattens toward 0", 16, BLUE, weight="700"))
    lines.append(text_element(310, 684, "resource scale x", 17, MUTED, anchor="middle"))

    x_map_b = {row["scale"]: 675 + index * 100 for index, row in enumerate(extrapolation_rows)}
    y_map_b = lambda loss: 620 - (loss - 0.70) / 0.45 * 390
    for loss in (0.75, 0.9, 1.0, 1.1):
        y = y_map_b(loss)
        lines.append('<line x1="675" y1="{0:.1f}" x2="1075" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(662, y + 5, loss, 15, MUTED, anchor="end"))
    for row in extrapolation_rows:
        label = "1e{}".format(int(math.log10(row["scale"])))
        lines.append(text_element(x_map_b[row["scale"]], 650, label, 15, MUTED, anchor="middle"))
    polyline(lines, [(x_map_b[row["scale"]], y_map_b(row["true_loss"])) for row in extrapolation_rows], TEAL)
    polyline(lines, [(x_map_b[row["scale"]], y_map_b(row["zero_offset_prediction"])) for row in extrapolation_rows], RED)
    lines.append(text_element(700, 220, "true / offset-aware", 16, TEAL, weight="700"))
    lines.append(text_element(875, 515, "zero-offset fit drifts", 16, RED, weight="700"))
    lines.append(text_element(875, 684, "scale (log-spaced)", 17, MUTED, anchor="middle"))
    lines.append(text_element(600, 756, "Evidence boundary: exact synthetic counterexample; it tests analysis logic, not a universal neural scaling law.", 16, MUTED, anchor="middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def figure_compute_data(path: Path, allocation_rows: Sequence[Dict],
                        repetition_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Compute-optimal allocation and repeated-token value",
        "Left panel shows normalized IsoFLOP regret around the analytic optimum; right panel separates seen from effective repeated tokens.",
    )
    lines.append(text_element(60, 58, "Allocation audit: a budget optimum and a data ledger are different objects", 28, INK, weight="700"))
    lines.append(text_element(60, 91, "The optimum is a valley; repeated exposure grows the seen ledger faster than the effective proxy.", 17, MUTED))
    panel(lines, 55, 125, 530, 590, "A  IsoFLOP regret around N*")
    panel(lines, 615, 125, 530, 590, "B  Repetition: seen versus effective tokens")

    multipliers = (0.25, 0.5, 1.0, 2.0, 4.0)
    x_map = {value: 105 + index * 100 for index, value in enumerate(multipliers)}
    max_regret = max(row["relative_regret"] for row in allocation_rows)
    y_map = lambda regret: 610 - regret / (max_regret * 1.1) * 370
    for regret in (0.0, 0.025, 0.05, 0.075, 0.10):
        y = y_map(regret)
        lines.append('<line x1="105" y1="{0:.1f}" x2="505" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(92, y + 5, regret, 15, MUTED, anchor="end"))
    for value in multipliers:
        lines.append(text_element(x_map[value], 650, value, 15, MUTED, anchor="middle"))
    selected = [row for row in allocation_rows if row["compute_budget"] == 1.0e4]
    polyline(lines, [(x_map[row["model_multiplier_from_optimum"]], y_map(row["relative_regret"])) for row in selected], AMBER, width=4)
    lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="2" stroke-dasharray="8 7"/>'.format(x_map[1.0], MUTED))
    lines.append(text_element(x_map[1.0], 210, "analytic N*", 16, TEAL, anchor="middle", weight="700"))
    lines.append(text_element(305, 684, "N / N* at fixed compute", 17, MUTED, anchor="middle"))
    lines.append(text_element(115, 250, "C=1e4, 1e6, 1e8: exact overlap", 16, MUTED))
    lines.append(text_element(115, 285, "relative regret", 15, MUTED))

    x_map_b = {row["repetitions"]: 660 + row["repetitions"] * 42 for row in repetition_rows}
    y_map_b = lambda tokens: 620 - tokens / 1050.0 * 390
    for tokens in (0, 250, 500, 750, 1000):
        y = y_map_b(tokens)
        lines.append('<line x1="700" y1="{0:.1f}" x2="1080" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(688, y + 5, tokens, 15, MUTED, anchor="end"))
    polyline(lines, [(x_map_b[row["repetitions"]], y_map_b(row["seen_tokens_billion"])) for row in repetition_rows], BLUE)
    polyline(lines, [(x_map_b[row["repetitions"]], y_map_b(row["effective_tokens_billion"])) for row in repetition_rows], AMBER)
    lines.append(text_element(730, 245, "seen = U x epochs", 16, BLUE, weight="700"))
    lines.append(text_element(820, 505, "effective proxy saturates", 16, AMBER, weight="700"))
    lines.append(text_element(890, 684, "repetitions / epochs", 17, MUTED, anchor="middle"))
    lines.append(text_element(600, 756, "Evidence boundary: analytic proxy with declared exponents and decay; real optima and token value require empirical calibration.", 16, MUTED, anchor="middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def figure_broken_heldout(path: Path, broken_rows: Sequence[Dict],
                          heldout_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Metric-induced emergence and held-out-scale evidence",
        "Left panel maps smooth per-step probability to steep exact match; right panel preserves calibration, validation, held-out splits and failures.",
    )
    lines.append(text_element(60, 58, "Evidence audit: distinguish a steep metric from a tested extrapolation", 28, INK, weight="700"))
    lines.append(text_element(60, 91, "Scale blocks enter in order; failed target runs remain in the denominator.", 17, MUTED))
    panel(lines, 55, 125, 530, 590, "A  Smooth latent skill, steep exact match")
    panel(lines, 615, 125, 530, 590, "B  Locked prediction on held-out scales")

    x_map = {row["scale"]: 95 + index * 70 for index, row in enumerate(broken_rows)}
    y_map = lambda value: 620 - value * 430
    for value in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = y_map(value)
        lines.append('<line x1="95" y1="{0:.1f}" x2="515" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(82, y + 5, value, 15, MUTED, anchor="end"))
    polyline(lines, [(x_map[row["scale"]], y_map(row["per_step_probability"])) for row in broken_rows], TEAL)
    polyline(lines, [(x_map[row["scale"]], y_map(row["exact_match_probability_m10"])) for row in broken_rows], RED)
    lines.append(text_element(120, 240, "per-step p changes smoothly", 16, TEAL, weight="700"))
    lines.append(text_element(285, 515, "exact match = p^10", 16, RED, weight="700"))
    lines.append(text_element(305, 684, "model scale (log-spaced)", 17, MUTED, anchor="middle"))

    x_map_b = {row["scale"]: 675 + index * 55 for index, row in enumerate(heldout_rows)}
    y_map_b = lambda value: 620 - (value - 1.2) / 1.9 * 400
    split_colors = {"calibration": "#EAF2FF", "validation": "#E8F6F3", "heldout": "#FFF3D6"}
    for split, start, width in (("calibration", 650, 235), ("validation", 885, 110), ("heldout", 995, 120)):
        lines.append('<rect x="{}" y="180" width="{}" height="450" fill="{}" opacity="0.65"/>'.format(start, width, split_colors[split]))
    for loss in (1.3, 1.8, 2.3, 2.8):
        y = y_map_b(loss)
        lines.append('<line x1="675" y1="{0:.1f}" x2="1060" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(663, y + 5, loss, 15, MUTED, anchor="end"))
    for row in heldout_rows:
        x = x_map_b[row["scale"]]
        low, high = y_map_b(row["prediction_lower"]), y_map_b(row["prediction_upper"])
        lines.append('<line x1="{0}" y1="{1:.1f}" x2="{0}" y2="{2:.1f}" stroke="{3}" stroke-width="5"/>'.format(x, low, high, BLUE))
        lines.append('<circle cx="{:.1f}" cy="{:.1f}" r="5" fill="{}"/>'.format(x, y_map_b(row["observed_loss"]), TEAL))
        if row["failed_runs"]:
            lines.append(text_element(x, 605, "fail={}".format(row["failed_runs"]), 15, RED, anchor="middle", weight="700"))
        lines.append(text_element(x, 650, row["scale"], 15, MUTED, anchor="middle"))
    polyline(lines, [(x_map_b[row["scale"]], y_map_b(row["locked_prediction"])) for row in heldout_rows], BLUE, width=3)
    lines.append(text_element(715, 210, "calibration", 15, BLUE, weight="700"))
    lines.append(text_element(905, 210, "validation", 15, TEAL, weight="700"))
    lines.append(text_element(1020, 210, "held-out", 15, AMBER, weight="700"))
    lines.append(text_element(895, 684, "entire scale blocks", 17, MUTED, anchor="middle"))
    lines.append(text_element(600, 756, "Evidence boundary: deterministic coverage example validates bookkeeping; E3 in simulation is not external neural-model evidence.", 16, MUTED, anchor="middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate_checks(data: Dict[str, Sequence[Dict]]) -> List[Dict]:
    slopes = data["offset_slopes"]
    extrapolation = data["extrapolation_families"]
    joint = data["joint_identifiability"]
    allocation = data["compute_optimal_allocation"]
    systems = data["compute_system_ledger"]
    repetition = data["repeated_tokens"]
    mixture = data["mixture_transfer"]
    lifecycle = data["inference_break_even"]
    broken = data["broken_emergence"]
    heldout = data["heldout_evidence"]

    diagonal = [row for row in joint if row["design"].startswith("diagonal")]
    crossed = [row for row in joint if row["design"] == "crossed_grid"]
    optimum_rows = [row for row in allocation if row["model_multiplier_from_optimum"] == 1.0]
    balanced = [row for row in mixture if row["target"] == "balanced_deployment"]
    a_heavy = [row for row in mixture if row["target"] == "domain_A_heavy"]
    lifecycle_by = {(row["strategy"], row["requests"]): row for row in lifecycle}
    checks = [
        ("H1_excess_slope_equals_minus_half", all(abs(row["excess_log_slope"] + 0.5) < 1e-12 for row in slopes)),
        ("H1_raw_slope_flattens", all(abs(slopes[index + 1]["raw_log_slope"]) < abs(slopes[index]["raw_log_slope"]) for index in range(len(slopes) - 1))),
        ("H1_raw_slope_matches_offset_identity", all(abs(row["raw_log_slope"] + 0.5 * (1.0 - row["floor"] / row["loss"])) < 1e-12 for row in slopes)),
        ("H2_zero_offset_interpolates_calibration", all(row["zero_offset_absolute_error"] < 1e-12 for row in extrapolation if row["split"] == "calibration")),
        ("H2_zero_offset_far_extrapolation_fails", extrapolation[-1]["zero_offset_absolute_error"] > 0.20),
        ("H2_offset_family_recovers_truth", all(row["offset_absolute_error"] < 1e-12 for row in extrapolation)),
        ("H3_diagonal_terms_have_same_path_exponent", all(row["parameter_path_exponent"] == row["data_path_exponent"] for row in diagonal)),
        ("H3_crossed_grid_has_nine_cells", len(crossed) == 9),
        ("H3_crossed_grid_exposes_both_bottlenecks", any(row["parameter_term"] > row["data_term"] for row in crossed) and any(row["data_term"] > row["parameter_term"] for row in crossed)),
        ("H4_allocation_respects_compute_constraint", all(abs(row["constraint_product"] / row["compute_budget"] - 1.0) < 1e-12 for row in allocation)),
        ("H4_analytic_multiplier_minimizes_each_budget", all(row["relative_regret"] < 1e-12 for row in optimum_rows)),
        ("H4_weighted_margins_balance", all(abs(row["weighted_parameter_margin"] - row["weighted_data_margin"]) < 1e-12 for row in optimum_rows)),
        ("H4_allocation_exponents_sum_to_one", all(abs(row["analytic_N_exponent"] + row["analytic_D_exponent"] - 1.0) < 1e-12 for row in allocation)),
        ("H5_same_model_flops_across_systems", len({row["model_flops"] for row in systems}) == 1),
        ("H5_wall_time_depends_on_system", len({round(row["wall_seconds"], 6) for row in systems}) == len(systems)),
        ("H5_hfu_equals_execution_multiplier_times_mfu", all(abs(row["hfu"] - row["execution_multiplier"] * row["mfu"]) < 1e-12 for row in systems)),
        ("H5_carbon_uses_energy_and_grid_intensity", all(abs(row["carbon_tonnes"] - row["facility_energy_mwh"] * row["grid_intensity_kg_per_kwh"]) < 1e-12 for row in systems)),
        ("H6_effective_tokens_increase", all(repetition[index + 1]["effective_tokens_billion"] > repetition[index]["effective_tokens_billion"] for index in range(len(repetition) - 1))),
        ("H6_marginal_repeat_value_decreases", all(repetition[index + 1]["marginal_weight"] < repetition[index]["marginal_weight"] for index in range(len(repetition) - 1))),
        ("H6_effective_tokens_stay_below_limit", all(row["effective_tokens_billion"] < row["asymptotic_effective_limit_billion"] for row in repetition)),
        ("H7_mixture_weights_stay_on_simplex", all(abs(row["training_weight_A"] + row["training_weight_B"] - 1.0) < 1e-12 for row in mixture)),
        ("H7_domain_tradeoff_is_visible", balanced[-1]["domain_A_loss"] < balanced[0]["domain_A_loss"] and balanced[-1]["domain_B_loss"] > balanced[0]["domain_B_loss"]),
        ("H7_target_changes_optimal_mixture", min(balanced, key=lambda row: row["target_aggregate_loss"])["training_weight_A"] != min(a_heavy, key=lambda row: row["target_aggregate_loss"])["training_weight_A"]),
        ("H8_break_even_ties_A_and_B", abs(lifecycle_by[("A_large_short", 500)]["total_lifecycle_cost"] - lifecycle_by[("B_small_long", 500)]["total_lifecycle_cost"]) < 1e-12),
        ("H8_A_wins_before_break_even", lifecycle_by[("A_large_short", 250)]["total_lifecycle_cost"] < lifecycle_by[("B_small_long", 250)]["total_lifecycle_cost"]),
        ("H8_B_wins_after_break_even", lifecycle_by[("B_small_long", 1000)]["total_lifecycle_cost"] < lifecycle_by[("A_large_short", 1000)]["total_lifecycle_cost"]),
        ("H8_C_is_dominated_by_B", all(lifecycle_by[("C_dominated", q)]["total_lifecycle_cost"] > lifecycle_by[("B_small_long", q)]["total_lifecycle_cost"] and lifecycle_by[("C_dominated", q)]["latency_ms"] > lifecycle_by[("B_small_long", q)]["latency_ms"] for q in (0, 250, 500, 1000, 10000))),
        ("H9_exact_match_amplifies_smooth_skill", broken[-1]["exact_match_probability_m10"] / broken[0]["exact_match_probability_m10"] > broken[-1]["per_step_probability"] / broken[0]["per_step_probability"]),
        ("H9_zero_success_probability_decreases", all(broken[index + 1]["zero_success_probability_n100"] < broken[index]["zero_success_probability_n100"] for index in range(len(broken) - 1))),
        ("H9_broken_exponent_transitions", broken[0]["local_loss_exponent"] > -0.31 and broken[-1]["local_loss_exponent"] < -0.69),
        ("H10_scale_splits_are_strictly_ordered", max(row["scale"] for row in heldout if row["split"] == "calibration") < min(row["scale"] for row in heldout if row["split"] == "validation") < min(row["scale"] for row in heldout if row["split"] == "heldout")),
        ("H10_failures_remain_in_denominator", sum(row["planned_runs"] for row in heldout) == 24 and sum(row["failed_runs"] for row in heldout) == 2),
        ("H10_locked_intervals_cover_observations", all(row["interval_covers_observation"] for row in heldout)),
        ("H10_heldout_rows_are_E3", all(row["evidence_level"] == "E3" for row in heldout if row["split"] == "heldout")),
    ]
    return [{"check": name, "passed": passed} for name, passed in checks]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root_default = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root_default / "00-知识库管理/_labs/experiments/trn60.7-scaling-resource-audit-v1",
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=root_default / "00-知识库管理/_assets/plots/training-optimization",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "offset_slopes": offset_slope_audit(),
        "extrapolation_families": extrapolation_family_audit(),
        "joint_identifiability": joint_identifiability_audit(),
        "compute_optimal_allocation": compute_optimal_audit(),
        "compute_system_ledger": compute_system_ledger_audit(),
        "repeated_tokens": repeated_token_audit(),
        "mixture_transfer": mixture_transfer_audit(),
        "inference_break_even": inference_break_even_audit(),
        "broken_emergence": broken_emergence_audit(),
        "heldout_evidence": heldout_evidence_audit(),
    }
    csv_names = {key: key + ".csv" for key in data}
    for key, filename in csv_names.items():
        write_csv(args.output_dir / filename, data[key])

    plot_names = [
        "plot-scaling-offset-extrapolation-audit-v1.svg",
        "plot-scaling-compute-data-allocation-audit-v1.svg",
        "plot-scaling-broken-heldout-evidence-audit-v1.svg",
    ]
    figure_offset_extrapolation(args.plot_dir / plot_names[0], data["offset_slopes"], data["extrapolation_families"])
    figure_compute_data(args.plot_dir / plot_names[1], data["compute_optimal_allocation"], data["repeated_tokens"])
    figure_broken_heldout(args.plot_dir / plot_names[2], data["broken_emergence"], data["heldout_evidence"])

    checks = evaluate_checks(data)
    payload = {
        "experiment_id": "EXP-TRN-607-V1",
        "seed": SEED,
        "runtime": "Python standard library",
        "tracks": list(data.keys()),
        "checks": checks,
        "check_summary": {
            "passed": sum(bool(row["passed"]) for row in checks),
            "total": len(checks),
        },
        "artifacts": {
            "json": "results.json",
            "csv": list(csv_names.values()),
            "svg": plot_names,
        },
        "evidence_boundaries": [
            "Analytic and deterministic constructions validate definitions, accounting identities, metrics, and counterexamples.",
            "A synthetic E3 split does not establish a neural scaling law or external replication.",
            "The effective-token decay and loss surfaces are declared proxies, not fitted empirical constants.",
            "Lifecycle decisions remain conditional on the request horizon, system ledger, quality constraints, and candidate set.",
        ],
    }
    (args.output_dir / "results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    passed, total = payload["check_summary"]["passed"], payload["check_summary"]["total"]
    print("EXP-TRN-607-V1: {}/{} checks passed".format(passed, total))
    print("output_dir={}".format(args.output_dir))
    print("plot_dir={}".format(args.plot_dir))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
