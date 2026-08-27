#!/usr/bin/env python3
"""Deterministic standard-library audit for TRN-41--TRN-48.

The experiment separates coordinate and coherent aggregation, lazy and
feature-learning parameterizations, muP exponent bookkeeping, infshape
classification, coordinate-check slopes, entry RMS versus spectral norm,
attention initialization versus aligned training, hyperparameter transfer,
width-depth accumulation, and evidence/budget gates.

It writes one JSON, ten CSV files, and three self-contained SVG figures.
NumPy, PyTorch, plotting packages, and network access are deliberately not
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
WIDTHS = [16, 64, 256, 1024]
BLUE = "#2563EB"
TEAL = "#0F766E"
AMBER = "#B76E00"
RED = "#C0392B"
INK = "#172033"
MUTED = "#52606D"
GRID = "#D9E0E7"
BACKGROUND = "#FFFEFB"


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def log_slope(rows: Sequence[Dict], value_key: str) -> float:
    xs = [math.log(float(row["width"])) for row in rows]
    ys = [math.log(float(row[value_key])) for row in rows]
    x_bar = mean(xs)
    y_bar = mean(ys)
    numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))
    denominator = sum((x - x_bar) ** 2 for x in xs)
    return numerator / denominator


def accumulation_audit() -> List[Dict]:
    rows = []
    for width in WIDTHS:
        rows.append(
            {
                "width": width,
                "entry_scale": width ** -0.5,
                "independent_sum_rms": math.sqrt(width) * width ** -0.5,
                "coherent_sum": width * width ** -0.5,
                "mean_field_independent_sum_rms": math.sqrt(width) / width,
                "mean_field_coherent_sum": width / width,
            }
        )
    return rows


def parameterization_audit() -> List[Dict]:
    rows = []
    for width in WIDTHS:
        rows.extend(
            [
                {
                    "regime": "NTK_lazy",
                    "width": width,
                    "output_multiplier": width ** -0.5,
                    "per_neuron_feature_change": width ** -0.5,
                    "aligned_output_change": 1.0,
                    "relative_feature_change": width ** -0.5,
                },
                {
                    "regime": "mean_field_feature",
                    "width": width,
                    "output_multiplier": width ** -1.0,
                    "per_neuron_feature_change": 1.0,
                    "aligned_output_change": 1.0,
                    "relative_feature_change": 1.0,
                },
            ]
        )
    return rows


def exponent_ledger_audit() -> List[Dict]:
    rows = [
        {
            "parameter_group": "input_matrix_SGD",
            "entry_init_exponent": -0.5,
            "raw_lr_exponent": 0.0,
            "entry_update_exponent": -0.5,
            "aligned_terms_exponent": 0.5,
            "feature_update_exponent": 0.0,
        },
        {
            "parameter_group": "hidden_matrix_SGD",
            "entry_init_exponent": -0.5,
            "raw_lr_exponent": -1.0,
            "entry_update_exponent": -1.0,
            "aligned_terms_exponent": 1.0,
            "feature_update_exponent": 0.0,
        },
        {
            "parameter_group": "readout_SGD",
            "entry_init_exponent": -1.0,
            "raw_lr_exponent": -1.0,
            "entry_update_exponent": -1.0,
            "aligned_terms_exponent": 1.0,
            "feature_update_exponent": 0.0,
        },
        {
            "parameter_group": "hidden_matrix_Adam_like",
            "entry_init_exponent": -0.5,
            "raw_lr_exponent": -1.0,
            "entry_update_exponent": -1.0,
            "aligned_terms_exponent": 1.0,
            "feature_update_exponent": 0.0,
        },
    ]
    return rows


def infshape_audit() -> List[Dict]:
    specifications = [
        ("token_embedding", (32000, 128), (32000, 256), (32000, 1024), "finite,infinite", "lookup"),
        ("hidden_square", (128, 128), (256, 256), (1024, 1024), "infinite,infinite", "width_sum"),
        ("ffn_up", (128, 512), (256, 1024), (1024, 4096), "infinite,infinite", "non_square_width_sum"),
        ("readout", (128, 32000), (256, 32000), (1024, 32000), "infinite,finite", "logit_width_sum"),
        ("norm_scale", (128,), (256,), (1024,), "infinite", "coordinate_affine"),
    ]
    rows = []
    for name, base, delta, target, axes, semantics in specifications:
        base_widths = [dim for dim in base if dim not in (32000,)]
        target_widths = [dim for dim in target if dim not in (32000,)]
        rows.append(
            {
                "parameter_group": name,
                "base_shape": "x".join(str(value) for value in base),
                "delta_shape": "x".join(str(value) for value in delta),
                "target_shape": "x".join(str(value) for value in target),
                "axis_classification": axes,
                "forward_semantics": semantics,
                "base_to_target_scale": max(target_widths) / max(base_widths),
            }
        )
    return rows


def coordinate_check_audit() -> List[Dict]:
    rows = []
    for width in WIDTHS:
        rows.extend(
            [
                {
                    "signal": "stable_hidden_update",
                    "width": width,
                    "step": 1,
                    "value": 0.25,
                    "expected_slope": 0.0,
                },
                {
                    "signal": "faulty_hidden_update",
                    "width": width,
                    "step": 1,
                    "value": 0.25 * math.sqrt(width / WIDTHS[0]),
                    "expected_slope": 0.5,
                },
                {
                    "signal": "readout_transient_step1",
                    "width": width,
                    "step": 1,
                    "value": 0.5 * math.sqrt(WIDTHS[-1] / width),
                    "expected_slope": -0.5,
                },
                {
                    "signal": "readout_after_transient",
                    "width": width,
                    "step": 8,
                    "value": 0.5,
                    "expected_slope": 0.0,
                },
            ]
        )
    by_signal = {}
    for row in rows:
        by_signal.setdefault(row["signal"], []).append(row)
    slopes = {signal: log_slope(group, "value") for signal, group in by_signal.items()}
    for row in rows:
        row["measured_slope"] = slopes[row["signal"]]
    return rows


def spectral_audit() -> List[Dict]:
    rows = []
    for width in WIDTHS:
        entry_rms = 1.0 / width
        rows.extend(
            [
                {
                    "matrix": "rank_one_aligned",
                    "width": width,
                    "entry_rms": entry_rms,
                    "spectral_norm_exact": 1.0,
                    "power_iteration_estimate": 1.0,
                    "effective_rank": 1.0,
                },
                {
                    "matrix": "scaled_hadamard",
                    "width": width,
                    "entry_rms": entry_rms,
                    "spectral_norm_exact": width ** -0.5,
                    "power_iteration_estimate": width ** -0.5,
                    "effective_rank": float(width),
                },
            ]
        )
    return rows


def attention_audit() -> List[Dict]:
    rows = []
    for width in WIDTHS:
        for scaling in ("sqrt", "linear"):
            multiplier = width ** -0.5 if scaling == "sqrt" else width ** -1.0
            rows.append(
                {
                    "head_dimension": width,
                    "scaling": scaling,
                    "multiplier": multiplier,
                    "independent_initial_score_rms": math.sqrt(width) * multiplier,
                    "aligned_trained_score": width * multiplier,
                }
            )
    return rows


def transfer_curve_audit() -> List[Dict]:
    candidates = [0.5, 1.0, 2.0, 4.0]
    rows = []
    base_width = 128
    for family, drift_per_octave in (("muP", 0.03), ("standard", 0.45)):
        for width in (128, 256, 512, 1024):
            shift = drift_per_octave * math.log(width / base_width, 2)
            losses = {}
            for learning_rate in candidates:
                coordinate = math.log(learning_rate / 2.0, 2)
                loss = 1.5 + (coordinate - shift) ** 2
                losses[learning_rate] = loss
            minimum = min(losses.values())
            optimum = min(candidates, key=lambda value: (losses[value], value))
            base_choice = 2.0
            near_optimal = [value for value in candidates if losses[value] <= minimum + 0.10]
            for learning_rate in candidates:
                rows.append(
                    {
                        "family": family,
                        "width": width,
                        "learning_rate": learning_rate,
                        "validation_loss": losses[learning_rate],
                        "grid_optimum": optimum,
                        "target_minimum": minimum,
                        "base_choice_regret": losses[base_choice] - minimum,
                        "within_tau_0_10": learning_rate in near_optimal,
                    }
                )
    return rows


def width_depth_audit() -> List[Dict]:
    rows = []
    for depth in (4, 16, 64, 256):
        for correlation in ("aligned", "orthogonal"):
            raw = float(depth) if correlation == "aligned" else math.sqrt(depth)
            for multiplier_name, multiplier in (
                ("none", 1.0),
                ("inverse_sqrt_depth", depth ** -0.5),
                ("inverse_depth", depth ** -1.0),
            ):
                rows.append(
                    {
                        "width": 256,
                        "depth": depth,
                        "branch_correlation": correlation,
                        "multiplier": multiplier_name,
                        "residual_scale": multiplier,
                        "normalized_accumulation": raw * multiplier,
                    }
                )
    return rows


def evidence_ledger_audit() -> List[Dict]:
    entries = [
        ("shape", "pass", 2.0, "infshape and orientation complete"),
        ("coordinate", "pass", 4.0, "all absolute slopes <= 0.05"),
        ("spectral_depth", "fail", 6.0, "rank-one update normalized spectrum drifts"),
        ("training_safety", "pass", 10.0, "0 NaN/OOM in 8 launched runs"),
        ("transfer", "blocked", 80.0, "target confirm forbidden after spectral failure"),
        ("target_confirm", "not_spent", 8.0, "reserved budget remains unused"),
    ]
    return [
        {
            "gate": gate,
            "status": status,
            "budget_gpu_hours": cost,
            "evidence": evidence,
            "included_in_total_budget": True,
        }
        for gate, status, cost, evidence in entries
    ]


def write_csv(path: Path, rows: Sequence[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
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
        "<title id=\"title\">{}</title>".format(esc(title)),
        "<desc id=\"desc\">{}</desc>".format(esc(description)),
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


def figure_coordinate_regime(path: Path, coordinate_rows: Sequence[Dict],
                             parameter_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Coordinate slopes and feature-learning regimes",
        "Two textbook panels compare stable versus faulty coordinate slopes and NTK versus mean-field relative feature updates.",
    )
    lines.append(text_element(60, 58, "Coordinate audit: horizontal is a claim, not a decoration", 28, INK, weight="700"))
    lines.append(text_element(60, 91, "Log-width slopes isolate implementation drift; regime comparison asks whether features actually move.", 17, MUTED))
    panel(lines, 55, 125, 530, 590, "A  Multi-width coordinate check")
    panel(lines, 615, 125, 530, 590, "B  Lazy versus feature-learning update")

    x_values = WIDTHS
    x_map = {value: 105 + index * 135 for index, value in enumerate(x_values)}
    y_zero = 620
    for width in x_values:
        x = x_map[width]
        lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="1"/>'.format(x, GRID))
        lines.append(text_element(x, 650, width, 16, MUTED, anchor="middle"))
    lines.append(text_element(350, 684, "width n", 17, MUTED, anchor="middle"))
    for level, label in ((0.125, "0.125"), (0.25, "0.25"), (0.5, "0.5"), (1.0, "1.0")):
        y = y_zero - math.log(level / 0.125, 2) * 105
        lines.append('<line x1="105" y1="{0:.1f}" x2="510" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(92, y + 5, label, 15, MUTED, anchor="end"))

    stable = [row for row in coordinate_rows if row["signal"] == "stable_hidden_update"]
    faulty = [row for row in coordinate_rows if row["signal"] == "faulty_hidden_update"]
    to_y = lambda value: y_zero - math.log(value / 0.125, 2) * 105
    polyline(lines, [(x_map[row["width"]], to_y(row["value"])) for row in stable], TEAL)
    polyline(lines, [(x_map[row["width"]], to_y(row["value"])) for row in faulty], RED)
    lines.append(text_element(125, 210, "stable slope = 0", 16, TEAL, weight="700"))
    lines.append(text_element(330, 260, "faulty slope = +0.5", 16, RED, weight="700"))

    x_map_b = {value: 675 + index * 135 for index, value in enumerate(x_values)}
    for width in x_values:
        x = x_map_b[width]
        lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="1"/>'.format(x, GRID))
        lines.append(text_element(x, 650, width, 16, MUTED, anchor="middle"))
    lines.append(text_element(920, 684, "width n", 17, MUTED, anchor="middle"))
    for level, label in ((0.03125, "1/32"), (0.125, "1/8"), (0.5, "1/2"), (1.0, "1")):
        y = 580 - math.log(level / 0.03125, 2) * 72
        lines.append('<line x1="675" y1="{0:.1f}" x2="1080" y2="{0:.1f}" stroke="{1}" stroke-width="1"/>'.format(y, GRID))
        lines.append(text_element(662, y + 5, label, 15, MUTED, anchor="end"))
    ntk = [row for row in parameter_rows if row["regime"] == "NTK_lazy"]
    mf = [row for row in parameter_rows if row["regime"] == "mean_field_feature"]
    regime_y = lambda value: 580 - math.log(value / 0.03125, 2) * 72
    polyline(lines, [(x_map_b[row["width"]], regime_y(row["relative_feature_change"])) for row in ntk], BLUE)
    polyline(lines, [(x_map_b[row["width"]], regime_y(row["relative_feature_change"])) for row in mf], AMBER)
    lines.append(text_element(700, 210, "mean-field: O(1)", 16, AMBER, weight="700"))
    lines.append(text_element(850, 480, "NTK: n^-1/2", 16, BLUE, weight="700"))
    lines.append(text_element(600, 756, "Evidence boundary: analytic scaling identities; not a trained-network benchmark.", 16, MUTED, anchor="middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def figure_spectral_depth(path: Path, spectral_rows: Sequence[Dict],
                          depth_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Spectral counterexample and depth accumulation",
        "Left panel shows equal entry RMS but different spectral norms. Right panel separates aligned and orthogonal residual accumulation.",
    )
    lines.append(text_element(60, 58, "Spectral and depth audit: small coordinates can still add coherently", 28, INK, weight="700"))
    lines.append(text_element(60, 91, "The worst direction and the cross-layer correlation regime require separate telemetry.", 17, MUTED))
    panel(lines, 55, 125, 530, 590, "A  Same entry RMS, different spectrum")
    panel(lines, 615, 125, 530, 590, "B  Residual accumulation after scaling")

    x_map = {value: 105 + index * 135 for index, value in enumerate(WIDTHS)}
    spec_y = lambda value: 580 - math.log(value / (1 / 32), 2) * 72
    for width in WIDTHS:
        x = x_map[width]
        lines.append(text_element(x, 650, width, 16, MUTED, anchor="middle"))
        lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="1"/>'.format(x, GRID))
    rank_one = [row for row in spectral_rows if row["matrix"] == "rank_one_aligned"]
    hadamard = [row for row in spectral_rows if row["matrix"] == "scaled_hadamard"]
    polyline(lines, [(x_map[row["width"]], spec_y(row["spectral_norm_exact"])) for row in rank_one], RED)
    polyline(lines, [(x_map[row["width"]], spec_y(row["spectral_norm_exact"])) for row in hadamard], TEAL)
    lines.append(text_element(120, 220, "rank-one ||W||2 = 1", 16, RED, weight="700"))
    lines.append(text_element(300, 470, "Hadamard ||W||2 = n^-1/2", 16, TEAL, weight="700"))
    lines.append(text_element(350, 684, "width n; both entry RMS = 1/n", 17, MUTED, anchor="middle"))

    depths = [4, 16, 64, 256]
    x_map_b = {value: 675 + index * 135 for index, value in enumerate(depths)}
    depth_y = lambda value: 580 - math.log(value / 0.25, 2) * 62
    for depth in depths:
        x = x_map_b[depth]
        lines.append(text_element(x, 650, depth, 16, MUTED, anchor="middle"))
        lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="1"/>'.format(x, GRID))
    aligned_inv = [
        row for row in depth_rows
        if row["branch_correlation"] == "aligned" and row["multiplier"] == "inverse_depth"
    ]
    aligned_sqrt = [
        row for row in depth_rows
        if row["branch_correlation"] == "aligned" and row["multiplier"] == "inverse_sqrt_depth"
    ]
    orth_sqrt = [
        row for row in depth_rows
        if row["branch_correlation"] == "orthogonal" and row["multiplier"] == "inverse_sqrt_depth"
    ]
    polyline(lines, [(x_map_b[row["depth"]], depth_y(row["normalized_accumulation"])) for row in aligned_inv], TEAL)
    polyline(lines, [(x_map_b[row["depth"]], depth_y(row["normalized_accumulation"])) for row in orth_sqrt], BLUE, dash="10 8")
    polyline(lines, [(x_map_b[row["depth"]], depth_y(row["normalized_accumulation"])) for row in aligned_sqrt], RED)
    lines.append(text_element(700, 220, "aligned × 1/L = 1", 16, TEAL, weight="700"))
    lines.append(text_element(700, 255, "orthogonal × 1/sqrt(L) = 1", 16, BLUE, weight="700"))
    lines.append(text_element(850, 400, "aligned × 1/sqrt(L) grows", 16, RED, weight="700"))
    lines.append(text_element(920, 684, "depth L", 17, MUTED, anchor="middle"))
    lines.append(text_element(600, 756, "Evidence boundary: exact structured matrices and correlation extremes; real layers may lie between them.", 16, MUTED, anchor="middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def figure_transfer(path: Path, transfer_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Hyperparameter transfer curves",
        "Two panels compare aligned muP proxy curves with drifting standard-parameterization curves across widths.",
    )
    lines.append(text_element(60, 58, "Transfer audit: compare curves and regret, not only one selected loss", 28, INK, weight="700"))
    lines.append(text_element(60, 91, "All widths share the same candidate grid; the vertical marker is the base-width choice.", 17, MUTED))
    panel(lines, 55, 125, 530, 590, "A  muP synthetic family")
    panel(lines, 615, 125, 530, 590, "B  Drifting standard family")

    candidates = [0.5, 1.0, 2.0, 4.0]
    colors = {128: BLUE, 256: TEAL, 512: AMBER, 1024: RED}
    for panel_x, family in ((55, "muP"), (615, "standard")):
        x_map = {value: panel_x + 80 + index * 125 for index, value in enumerate(candidates)}
        y_map = lambda value: 620 - (value - 1.5) / 11.5 * 400
        for loss_tick in (1.5, 4.5, 8.5, 12.5):
            y = y_map(loss_tick)
            lines.append(
                '<line x1="{0}" y1="{1:.1f}" x2="{2}" y2="{1:.1f}" '
                'stroke="{3}" stroke-width="1"/>'.format(
                    panel_x + 80, y, panel_x + 455, GRID
                )
            )
            lines.append(
                text_element(panel_x + 68, y + 5, loss_tick, 15, MUTED, anchor="end")
            )
        for value in candidates:
            x = x_map[value]
            lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="1"/>'.format(x, GRID))
            lines.append(text_element(x, 650, value, 16, MUTED, anchor="middle"))
        marker_x = x_map[2.0]
        lines.append('<line x1="{0}" y1="185" x2="{0}" y2="620" stroke="{1}" stroke-width="2" stroke-dasharray="8 7"/>'.format(marker_x, MUTED))
        lines.append(text_element(marker_x, 680, "base choice", 15, MUTED, anchor="middle"))
        for width in (128, 256, 512, 1024):
            selected = [
                row for row in transfer_rows
                if row["family"] == family and row["width"] == width
            ]
            selected.sort(key=lambda row: row["learning_rate"])
            polyline(
                lines,
                [(x_map[row["learning_rate"]], y_map(row["validation_loss"])) for row in selected],
                colors[width],
                width=3,
            )
            for row in selected:
                x, y = x_map[row["learning_rate"]], y_map(row["validation_loss"])
                lines.append('<circle cx="{:.1f}" cy="{:.1f}" r="5" fill="{}"/>'.format(x, y, colors[width]))
        lines.append(text_element(panel_x + 265, 704, "learning rate", 17, MUTED, anchor="middle"))
    for index, width in enumerate((128, 256, 512, 1024)):
        x = 350 + index * 130
        lines.append('<line x1="{0}" y1="110" x2="{1}" y2="110" stroke="{2}" stroke-width="4"/>'.format(x, x + 28, colors[width]))
        lines.append(text_element(x + 36, 116, "n={}".format(width), 15, MUTED))
    lines.append(text_element(600, 756, "Evidence boundary: deterministic curve construction validates metrics; it does not establish empirical muTransfer.", 16, MUTED, anchor="middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate_checks(data: Dict[str, Sequence[Dict]]) -> List[Dict]:
    accumulation = data["accumulation_scaling"]
    parameters = data["parameterization_regimes"]
    ledger = data["mup_exponent_ledger"]
    infshape = data["infshape_classification"]
    coordinates = data["coordinate_checks"]
    spectra = data["spectral_geometry"]
    attention = data["attention_scaling"]
    transfer = data["transfer_curves"]
    depth = data["width_depth"]
    evidence = data["evidence_ledger"]

    stable_rows = [row for row in coordinates if row["signal"] == "stable_hidden_update"]
    faulty_rows = [row for row in coordinates if row["signal"] == "faulty_hidden_update"]
    mup_target = [
        row for row in transfer
        if row["family"] == "muP" and row["width"] == 1024 and row["learning_rate"] == 2.0
    ][0]
    standard_target = [
        row for row in transfer
        if row["family"] == "standard" and row["width"] == 1024 and row["learning_rate"] == 2.0
    ][0]
    checks = [
        ("H1_independent_sum_is_constant", all(abs(row["independent_sum_rms"] - 1.0) < 1e-12 for row in accumulation)),
        ("H1_coherent_sum_grows_sqrt_width", abs(log_slope(accumulation, "coherent_sum") - 0.5) < 1e-12),
        ("H1_mean_field_coherent_sum_is_constant", all(abs(row["mean_field_coherent_sum"] - 1.0) < 1e-12 for row in accumulation)),
        ("H2_ntk_feature_change_vanishes", abs(log_slope([row for row in parameters if row["regime"] == "NTK_lazy"], "relative_feature_change") + 0.5) < 1e-12),
        ("H2_mean_field_feature_change_is_constant", all(abs(row["relative_feature_change"] - 1.0) < 1e-12 for row in parameters if row["regime"] == "mean_field_feature")),
        ("H2_functional_output_change_matched", all(abs(row["aligned_output_change"] - 1.0) < 1e-12 for row in parameters)),
        ("H3_all_feature_exponents_zero", all(abs(row["feature_update_exponent"]) < 1e-12 for row in ledger)),
        ("H3_hidden_aligned_sum_uses_n_terms", any(row["parameter_group"] == "hidden_matrix_SGD" and row["aligned_terms_exponent"] == 1.0 for row in ledger)),
        ("H4_embedding_has_finite_vocab_axis", any(row["parameter_group"] == "token_embedding" and row["axis_classification"] == "finite,infinite" for row in infshape)),
        ("H4_readout_has_finite_output_axis", any(row["parameter_group"] == "readout" and row["axis_classification"] == "infinite,finite" for row in infshape)),
        ("H4_norm_is_coordinate_affine", any(row["parameter_group"] == "norm_scale" and row["forward_semantics"] == "coordinate_affine" for row in infshape)),
        ("H5_stable_coordinate_slope_zero", abs(stable_rows[0]["measured_slope"]) < 1e-12),
        ("H5_faulty_coordinate_slope_half", abs(faulty_rows[0]["measured_slope"] - 0.5) < 1e-12),
        ("H5_readout_transient_resolves", all(abs(row["value"] - 0.5) < 1e-12 for row in coordinates if row["signal"] == "readout_after_transient")),
        ("H6_equal_entry_rms_with_spectral_gap", all(
            abs(group[0]["entry_rms"] - group[1]["entry_rms"]) < 1e-12
            and group[0]["spectral_norm_exact"] > group[1]["spectral_norm_exact"]
            for group in ([row for row in spectra if row["width"] == width] for width in WIDTHS)
        )),
        ("H6_power_iteration_matches_structured_exact", all(abs(row["power_iteration_estimate"] - row["spectral_norm_exact"]) < 1e-12 for row in spectra)),
        ("H6_rank_and_hadamard_effective_rank_differ", all(
            any(row["matrix"] == "rank_one_aligned" and row["effective_rank"] == 1.0 for row in spectra if row["width"] == width)
            and any(row["matrix"] == "scaled_hadamard" and row["effective_rank"] == width for row in spectra if row["width"] == width)
            for width in WIDTHS
        )),
        ("H7_sqrt_attention_preserves_initial_rms", all(abs(row["independent_initial_score_rms"] - 1.0) < 1e-12 for row in attention if row["scaling"] == "sqrt")),
        ("H7_linear_attention_preserves_aligned_score", all(abs(row["aligned_trained_score"] - 1.0) < 1e-12 for row in attention if row["scaling"] == "linear")),
        ("H7_one_multiplier_does_not_preserve_both_stages", all(
            row["independent_initial_score_rms"] != row["aligned_trained_score"] for row in attention if row["head_dimension"] > 1
        )),
        ("H8_mup_base_choice_regret_small", mup_target["base_choice_regret"] <= 0.10),
        ("H8_standard_base_choice_regret_large", standard_target["base_choice_regret"] > 0.10),
        ("H8_mup_grid_optimum_stays_at_base_choice", all(row["grid_optimum"] == 2.0 for row in transfer if row["family"] == "muP")),
        ("H9_aligned_inverse_depth_is_constant", all(abs(row["normalized_accumulation"] - 1.0) < 1e-12 for row in depth if row["branch_correlation"] == "aligned" and row["multiplier"] == "inverse_depth")),
        ("H9_orthogonal_inverse_sqrt_is_constant", all(abs(row["normalized_accumulation"] - 1.0) < 1e-12 for row in depth if row["branch_correlation"] == "orthogonal" and row["multiplier"] == "inverse_sqrt_depth")),
        ("H9_aligned_inverse_sqrt_still_grows", log_slope(
            [{"width": row["depth"], "value": row["normalized_accumulation"]} for row in depth if row["branch_correlation"] == "aligned" and row["multiplier"] == "inverse_sqrt_depth"],
            "value",
        ) > 0.49),
        ("H10_spectral_failure_blocks_target", any(row["gate"] == "transfer" and row["status"] == "blocked" for row in evidence)),
        ("H10_reserved_confirm_budget_is_visible", any(row["gate"] == "target_confirm" and row["included_in_total_budget"] for row in evidence)),
        ("H10_budget_total_is_110_gpu_hours", abs(sum(row["budget_gpu_hours"] for row in evidence) - 110.0) < 1e-12),
    ]
    return [{"check": name, "passed": passed} for name, passed in checks]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root_default = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root_default / "00-知识库管理/_labs/experiments/trn60.6-mup-scale-transfer-audit-v1",
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
        "accumulation_scaling": accumulation_audit(),
        "parameterization_regimes": parameterization_audit(),
        "mup_exponent_ledger": exponent_ledger_audit(),
        "infshape_classification": infshape_audit(),
        "coordinate_checks": coordinate_check_audit(),
        "spectral_geometry": spectral_audit(),
        "attention_scaling": attention_audit(),
        "transfer_curves": transfer_curve_audit(),
        "width_depth": width_depth_audit(),
        "evidence_ledger": evidence_ledger_audit(),
    }
    csv_names = {
        "accumulation_scaling": "accumulation_scaling.csv",
        "parameterization_regimes": "parameterization_regimes.csv",
        "mup_exponent_ledger": "mup_exponent_ledger.csv",
        "infshape_classification": "infshape_classification.csv",
        "coordinate_checks": "coordinate_checks.csv",
        "spectral_geometry": "spectral_geometry.csv",
        "attention_scaling": "attention_scaling.csv",
        "transfer_curves": "transfer_curves.csv",
        "width_depth": "width_depth.csv",
        "evidence_ledger": "evidence_ledger.csv",
    }
    for key, filename in csv_names.items():
        write_csv(args.output_dir / filename, data[key])

    plot_names = [
        "plot-mup-coordinate-regime-audit-v1.svg",
        "plot-mup-spectral-width-depth-audit-v1.svg",
        "plot-mutransfer-curve-evidence-audit-v1.svg",
    ]
    figure_coordinate_regime(args.plot_dir / plot_names[0], data["coordinate_checks"], data["parameterization_regimes"])
    figure_spectral_depth(args.plot_dir / plot_names[1], data["spectral_geometry"], data["width_depth"])
    figure_transfer(args.plot_dir / plot_names[2], data["transfer_curves"])

    checks = evaluate_checks(data)
    payload = {
        "experiment_id": "EXP-TRN-606-V1",
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
            "Analytic and deterministic constructions validate definitions, scaling identities, metrics, and counterexamples.",
            "They do not establish empirical hyperparameter transfer in a trained Transformer.",
            "Structured spectral examples do not estimate the spectrum of a real optimizer trajectory.",
            "Target confirmation remains blocked in the evidence ledger after the synthetic spectral gate fails.",
        ],
    }
    (args.output_dir / "results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    passed = payload["check_summary"]["passed"]
    total = payload["check_summary"]["total"]
    print("EXP-TRN-606-V1: {}/{} checks passed".format(passed, total))
    print("output_dir={}".format(args.output_dir))
    print("plot_dir={}".format(args.plot_dir))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
