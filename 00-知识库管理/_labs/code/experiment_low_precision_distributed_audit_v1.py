#!/usr/bin/env python3
"""Deterministic standard-library audit for TRN-57--TRN-64.

The ten tracks test format/ulp contracts, loss-scaling clocks, stochastic
rounding, quantization/state bytes, global-batch weighting, ring All-Reduce,
parallel tensor shapes, ZeRO/FSDP peak memory, offload/roofline bounds, and
floating-point/reproducibility evidence.

The script writes one JSON, ten CSV files, and three self-contained SVGs.
NumPy, plotting packages, accelerators, distributed runtimes, and network
access are deliberately not required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
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
BG = "#FFFEFB"


def dtype_contract_audit() -> List[Dict]:
    formats = (
        ("FP32", 8, 23, "storage_and_execution"),
        ("TF32-multiply", 8, 10, "execution_policy"),
        ("FP16", 5, 10, "storage_and_execution"),
        ("BF16", 8, 7, "storage_and_execution"),
        ("FP8-E4M3", 4, 3, "scaled_execution"),
        ("FP8-E5M2", 5, 2, "scaled_execution"),
    )
    return [
        {
            "format": name,
            "exponent_bits": exponent,
            "fraction_bits": fraction,
            "precision_bits": fraction + 1,
            "ulp_at_one": 2.0 ** (-fraction),
            "unit_roundoff_normal": 2.0 ** (-(fraction + 1)),
            "contract_role": role,
        }
        for name, exponent, fraction, role in formats
    ]


def loss_scaling_clock_audit() -> List[Dict]:
    outcomes = ("success", "success", "overflow", "success", "success")
    scale, update, streak = 1024.0, 0, 0
    rows = []
    for attempt, outcome in enumerate(outcomes, start=1):
        before = scale
        if outcome == "success":
            update += 1
            streak += 1
            optimizer_advanced = 1
            if streak == 2:
                scale *= 2.0
                streak = 0
        else:
            optimizer_advanced = 0
            scale *= 0.5
            streak = 0
        rows.append(
            {
                "attempt": attempt,
                "outcome": outcome,
                "scale_before": before,
                "scale_after": scale,
                "successful_update": update,
                "growth_streak": streak,
                "optimizer_advanced": optimizer_advanced,
                "attempt_clock": attempt,
                "safe_scale_min_proxy": 64.0,
                "safe_scale_max_proxy": 128.0,
            }
        )
    return rows


def stochastic_rounding_audit() -> List[Dict]:
    q_low, q_high, x = 0.0, 0.25, 0.10
    delta = q_high - q_low
    p_high = (x - q_low) / delta
    p_low = 1.0 - p_high
    expectation = p_low * q_low + p_high * q_high
    variance = p_low * (q_low - x) ** 2 + p_high * (q_high - x) ** 2
    rows = []
    for step in range(0, 6):
        rows.append(
            {
                "step": step,
                "q_low": q_low,
                "q_high": q_high,
                "x": x,
                "p_low": p_low,
                "p_high": p_high,
                "one_step_expectation": expectation,
                "one_step_error_variance": variance,
                "variance_upper_bound": delta ** 2 / 4.0,
                "rn_micro_update_trajectory": 1.0,
                "sr_expected_micro_update_trajectory": 1.0 - 0.02 * step,
            }
        )
    return rows


def quantization_ledger_audit() -> List[Dict]:
    values = (-1.0, 0.0, 0.6, 2.4)
    scale, zero_point = 1.0, 1
    quantized = []
    for value in values:
        clipped = min(2.0, max(-1.0, value))
        code = min(3, max(0, int(math.floor(clipped / scale + 0.5)) + zero_point))
        dequantized = scale * (code - zero_point)
        quantized.append((value, clipped, code, dequantized))
    baseline_bytes, compressed_bytes = 16.0, 10.0
    fp32_bucket_mb = 100.0
    elements = fp32_bucket_mb * 1_000_000.0 / 4.0
    compressed_bucket_mb = elements / 1_000_000.0 + math.ceil(elements / 256.0) * 4.0 / 1_000_000.0
    return [
        {
            "value": value,
            "clipped_value": clipped,
            "quantized_code": code,
            "dequantized_value": dequantized,
            "absolute_error": abs(dequantized - value),
            "scale": scale,
            "zero_point": zero_point,
            "adam_baseline_bytes_per_parameter": baseline_bytes,
            "adam_8bit_state_bytes_per_parameter": compressed_bytes,
            "state_byte_saving_fraction": 1.0 - compressed_bytes / baseline_bytes,
            "fp32_bucket_mb": fp32_bucket_mb,
            "int8_bucket_plus_scales_mb": compressed_bucket_mb,
            "payload_compression_ratio": fp32_bucket_mb / compressed_bucket_mb,
        }
        for value, clipped, code, dequantized in quantized
    ]


def global_batch_audit() -> List[Dict]:
    counts = (4, 2, 3)
    means = (1.0, 4.0, 7.0)
    sums = tuple(n * mean for n, mean in zip(counts, means))
    weighted = sum(sums) / sum(counts)
    rank_mean = sum(means) / len(means)
    return [
        {
            "rank": rank,
            "effective_sample_count": count,
            "local_gradient_mean": mean,
            "local_gradient_sum": total,
            "global_sample_count": sum(counts),
            "correct_global_sample_mean": weighted,
            "incorrect_equal_rank_mean": rank_mean,
            "rank_mean_bias": rank_mean - weighted,
        }
        for rank, (count, mean, total) in enumerate(zip(counts, means, sums))
    ]


def ring_allreduce_audit() -> List[Dict]:
    message_gib = 1.0
    rows = []
    for ranks in (2, 4, 8, 16, 64):
        rows.append(
            {
                "ranks": ranks,
                "message_gib": message_gib,
                "reduce_scatter_rounds": ranks - 1,
                "all_gather_rounds": ranks - 1,
                "chunk_gib": message_gib / ranks,
                "per_rank_volume_gib": 2.0 * (ranks - 1) * message_gib / ranks,
                "parameter_server_worker_volume_gib": 2.0 * message_gib,
                "ring_to_parameter_server_worker_ratio": (ranks - 1) / ranks,
            }
        )
    return rows


def parallelism_shape_audit() -> List[Dict]:
    batch, hidden, output, degree = 8, 4096, 8192, 4
    return [
        {
            "case": "column_parallel_linear",
            "local_weight_rows": hidden,
            "local_weight_cols": output // degree,
            "local_output_rows": batch,
            "local_output_cols": output // degree,
            "collective": "optional_all_gather",
            "pipeline_efficiency_proxy": "",
            "expert_capacity": "",
        },
        {
            "case": "row_parallel_linear",
            "local_weight_rows": hidden // degree,
            "local_weight_cols": output,
            "local_output_rows": batch,
            "local_output_cols": output,
            "collective": "all_reduce_sum",
            "pipeline_efficiency_proxy": "",
            "expert_capacity": "",
        },
        {
            "case": "pipeline_8_stages_32_microbatches",
            "local_weight_rows": "",
            "local_weight_cols": "",
            "local_output_rows": "",
            "local_output_cols": "",
            "collective": "point_to_point",
            "pipeline_efficiency_proxy": 32.0 / 39.0,
            "expert_capacity": "",
        },
        {
            "case": "expert_4096_tokens_8_experts_cf1.25",
            "local_weight_rows": "",
            "local_weight_cols": "",
            "local_output_rows": "",
            "local_output_cols": "",
            "collective": "all_to_all",
            "pipeline_efficiency_proxy": "",
            "expert_capacity": 640,
        },
    ]


def zero_memory_audit() -> List[Dict]:
    ranks, parameters = 8, 1_000_000_000
    schemes = (
        ("DDP", 16.0),
        ("ZeRO-1", 4.0 + 12.0 / ranks),
        ("ZeRO-2", 2.0 + 14.0 / ranks),
        ("ZeRO-3", 16.0 / ranks),
    )
    peak_components = (2.0, 3.0, 8.0, 1.5, 0.9)
    return [
        {
            "scheme": scheme,
            "ranks": ranks,
            "bytes_per_parameter_steady": bytes_per_parameter,
            "steady_model_state_gb_decimal": bytes_per_parameter * parameters / 1e9,
            "persistent_shard_gb": peak_components[0],
            "transient_layer_gather_gb": peak_components[1],
            "live_activation_gb": peak_components[2],
            "workspace_gb": peak_components[3],
            "other_buffer_gb": peak_components[4],
            "illustrative_live_peak_gb": sum(peak_components),
        }
        for scheme, bytes_per_parameter in schemes
    ]


def offload_roofline_audit() -> List[Dict]:
    compute_tflops, bandwidth_tbps = 300.0, 3.0
    ridge = compute_tflops / bandwidth_tbps
    rows = []
    for intensity in (40.0, 100.0, 200.0):
        rows.append(
            {
                "intensity_flop_per_byte": intensity,
                "compute_ceiling_tflops": compute_tflops,
                "bandwidth_tbps": bandwidth_tbps,
                "ridge_intensity": ridge,
                "roofline_tflops": min(compute_tflops, bandwidth_tbps * intensity),
                "bottleneck": "bandwidth" if intensity < ridge else "compute",
                "offload_total_gb": 24.0,
                "offload_bandwidth_gbps": 48.0,
                "offload_transfer_lower_bound_seconds": 0.5,
                "compute_seconds": 0.35,
            }
        )
    return rows


def reproducibility_evidence_audit() -> List[Dict]:
    a, b, c = 1.0e20, -1.0e20, 3.14
    left = (a + b) + c
    right = a + (b + c)
    labels = (
        ("E0", "configuration_manifest", 0, 0),
        ("E1", "throughput_memory_counters", 0, 0),
        ("E2", "profiler_critical_path", 0, 0),
        ("E3", "matched_learning_curve", 1, 0),
        ("E4", "paired_repeats_confidence_interval", 1, 0),
        ("E5", "causal_intervention_controls", 1, 1),
    )
    return [
        {
            "evidence_level": level,
            "evidence_object": label,
            "directly_tests_training_quality": quality,
            "supports_specific_causal_claim": causal,
            "left_association": left,
            "right_association": right,
            "association_difference": left - right,
            "strong_scaling_efficiency_64": 800.0 / (64.0 * 18.0),
            "bitwise_reproducibility_implied": 0,
            "decision_reproducibility_implied": 0,
        }
        for level, label, quality, causal in labels
    ]


def write_csv(path: Path, rows: Sequence[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_text(x: float, y: float, value: object, size: int = 16, color: str = MUTED,
             weight: int = 400, anchor: str = "start") -> str:
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}">{esc(value)}</text>')


def svg_header(title: str, subtitle: str) -> List[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(subtitle)}</desc>',
        f'<rect width="1200" height="800" fill="{BG}"/>',
        svg_text(60, 58, title, 28, INK, 700),
        svg_text(60, 91, subtitle, 17, MUTED),
    ]


def write_low_precision_svg(path: Path, dtype_rows: Sequence[Dict], sr_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Representability, control flow and estimator variance are separate contracts",
        "The audit combines ulp spacing, a safe loss-scale interval, and exact stochastic-rounding moments.",
    )
    lines += [
        f'<rect x="45" y="125" width="535" height="590" rx="18" fill="#FFFFFF" stroke="{GRID}" stroke-width="2"/>',
        f'<rect x="605" y="125" width="550" height="590" rx="18" fill="#FFFFFF" stroke="{GRID}" stroke-width="2"/>',
        svg_text(70, 166, "A  ulp at one and safe scale", 20, INK, 700),
        svg_text(630, 166, "B  Tiny updates: RN versus SR expectation", 20, INK, 700),
    ]
    selected = [row for row in dtype_rows if row["format"] in ("FP32", "FP16", "BF16", "FP8-E4M3")]
    max_log = max(math.log2(row["ulp_at_one"]) for row in selected)
    min_log = min(math.log2(row["ulp_at_one"]) for row in selected)
    for index, row in enumerate(selected):
        y = 230 + index * 82
        value = math.log2(row["ulp_at_one"])
        width = 70 + 300 * (value - min_log) / (max_log - min_log)
        color = (BLUE, TEAL, AMBER, RED)[index]
        lines += [svg_text(85, y, row["format"], 17, INK, 700),
                  f'<rect x="190" y="{y-22}" width="{width:.3f}" height="30" rx="8" fill="{color}" opacity="0.84"/>',
                  svg_text(200 + width, y, f'2^{int(value)}', 15, color, 700)]
    lines += [
        f'<rect x="95" y="575" width="420" height="85" rx="14" fill="#FFF3D6" stroke="{AMBER}" stroke-width="2"/>',
        svg_text(305, 610, "loss-scale proxy: 64 <= S <= 128", 18, AMBER, 700, "middle"),
        svg_text(305, 638, "range feasibility does not choose the final dynamic policy", 15, MUTED, 400, "middle"),
    ]
    x0, y0, x1, y1 = 675, 610, 1090, 220
    lines += [f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{MUTED}" stroke-width="2"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{MUTED}" stroke-width="2"/>']
    def px(step: int) -> float:
        return x0 + 35 + step * 70
    def py(value: float) -> float:
        return y0 - (value - 0.88) * 900
    exact_points = " ".join(f"{px(row['step']):.1f},{py(row['sr_expected_micro_update_trajectory']):.1f}" for row in sr_rows)
    rn_points = " ".join(f"{px(row['step']):.1f},{py(row['rn_micro_update_trajectory']):.1f}" for row in sr_rows)
    lines += [f'<polyline points="{exact_points}" fill="none" stroke="{TEAL}" stroke-width="4"/>',
              f'<polyline points="{rn_points}" fill="none" stroke="{RED}" stroke-width="4"/>',
              svg_text(735, 475, "RN: repeated update is swallowed", 16, RED, 700),
              svg_text(820, 575, "SR ensemble mean: -0.02 per step", 16, TEAL, 700),
              svg_text(875, 670, "update attempts", 16, MUTED, 400, "middle"),
              f'<rect x="720" y="300" width="330" height="45" rx="10" fill="#E8F6F3"/>',
              svg_text(885, 328, "E[Q]=x; Var(error)=0.015 <= 0.015625", 15, TEAL, 700, "middle"),
              svg_text(60, 760, "Deterministic analytic audit — no sampled trajectory proves final-model unbiasedness.", 15, MUTED),
              '</svg>']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_distributed_svg(path: Path, batch_rows: Sequence[Dict], zero_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "Global estimator semantics and peak memory need two-dimensional ledgers",
        "The left panel weights samples before division; the right separates sharded steady state from a live peak.",
    )
    lines += [
        f'<rect x="45" y="125" width="535" height="590" rx="18" fill="#FFFFFF" stroke="{GRID}" stroke-width="2"/>',
        f'<rect x="605" y="125" width="550" height="590" rx="18" fill="#FFFFFF" stroke="{GRID}" stroke-width="2"/>',
        svg_text(70, 166, "A  Unequal ranks: sum numerator and count", 20, INK, 700),
        svg_text(630, 166, "B  Model-state steady bytes versus live peak", 20, INK, 700),
    ]
    colors = (BLUE, TEAL, AMBER)
    for idx, row in enumerate(batch_rows):
        x = 85 + idx * 160
        lines += [f'<rect x="{x}" y="220" width="130" height="105" rx="14" fill="{colors[idx]}18" stroke="{colors[idx]}" stroke-width="2"/>',
                  svg_text(x + 65, 250, f"rank {row['rank']}", 17, colors[idx], 700, "middle"),
                  svg_text(x + 65, 278, f"n={row['effective_sample_count']}, mean={row['local_gradient_mean']}", 15, MUTED, 400, "middle"),
                  svg_text(x + 65, 304, f"sum={row['local_gradient_sum']}", 15, MUTED, 400, "middle")]
    weighted = batch_rows[0]["correct_global_sample_mean"]
    rank_mean = batch_rows[0]["incorrect_equal_rank_mean"]
    lines += [
        f'<rect x="105" y="395" width="410" height="95" rx="14" fill="#E8F6F3" stroke="{TEAL}" stroke-width="2"/>',
        svg_text(310, 430, "correct: (4 + 8 + 21) / 9", 18, TEAL, 700, "middle"),
        svg_text(310, 462, f"global sample mean = {weighted:.6f}", 17, INK, 700, "middle"),
        f'<rect x="105" y="525" width="410" height="80" rx="14" fill="#FFF7F4" stroke="{RED}" stroke-width="2"/>',
        svg_text(310, 558, "incorrect: (1 + 4 + 7) / 3", 17, RED, 700, "middle"),
        svg_text(310, 586, f"equal-rank mean = {rank_mean:.1f}", 16, MUTED, 400, "middle"),
    ]
    max_bytes = max(row["bytes_per_parameter_steady"] for row in zero_rows)
    for idx, row in enumerate(zero_rows):
        y = 225 + idx * 75
        width = 300 * row["bytes_per_parameter_steady"] / max_bytes
        color = (RED, AMBER, BLUE, TEAL)[idx]
        lines += [svg_text(630, y, row["scheme"], 16, INK, 700),
                  f'<rect x="720" y="{y-22}" width="{width:.3f}" height="30" rx="7" fill="{color}" opacity="0.82"/>',
                  svg_text(730 + width, y, f"{row['bytes_per_parameter_steady']:.2f} B/param", 15, color, 700)]
    peak = zero_rows[0]["illustrative_live_peak_gb"]
    lines += [
        f'<rect x="655" y="545" width="455" height="105" rx="14" fill="#FFF3D6" stroke="{AMBER}" stroke-width="2"/>',
        svg_text(882, 578, "ZeRO-3 steady = 2.0 GB", 17, TEAL, 700, "middle"),
        svg_text(882, 608, f"same timeline live peak = {peak:.1f} GB", 18, RED, 700, "middle"),
        svg_text(882, 634, "gather + activation + workspace + buffers", 15, MUTED, 400, "middle"),
        svg_text(60, 760, "Algebra and capacity audit — neither panel predicts backend schedule, topology or allocator behavior.", 15, MUTED),
        '</svg>',
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_roofline_svg(path: Path, roof_rows: Sequence[Dict], repro_rows: Sequence[Dict]) -> None:
    lines = svg_header(
        "A systems counter becomes a training claim only after the evidence ladder",
        "Roofline bounds attainable rate; matched curves and interventions test quality and causality.",
    )
    lines += [
        f'<rect x="45" y="125" width="600" height="590" rx="18" fill="#FFFFFF" stroke="{GRID}" stroke-width="2"/>',
        f'<rect x="670" y="125" width="485" height="590" rx="18" fill="#FFFFFF" stroke="{GRID}" stroke-width="2"/>',
        svg_text(70, 166, "A  Roofline and offload lower bound", 20, INK, 700),
        svg_text(695, 166, "B  Evidence E0 to E5", 20, INK, 700),
    ]
    x0, y0 = 115, 620
    lines += [f'<line x1="{x0}" y1="{y0}" x2="590" y2="{y0}" stroke="{MUTED}" stroke-width="2"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="220" stroke="{MUTED}" stroke-width="2"/>',
              f'<path d="M120 610 L350 285 H585" fill="none" stroke="{BLUE}" stroke-width="4"/>',
              svg_text(575, 270, "compute ceiling: 300 TFLOP/s", 16, BLUE, 700, "end"),
              f'<line x1="350" y1="285" x2="350" y2="620" stroke="{BLUE}" stroke-width="2" stroke-dasharray="8 7"/>',
              svg_text(350, 650, "ridge I*=100", 16, MUTED, 700, "middle")]
    for row, color in zip(roof_rows, (TEAL, AMBER, RED)):
        x = 120 + row["intensity_flop_per_byte"] * 2.3
        y = 620 - row["roofline_tflops"] * 1.08
        if row["intensity_flop_per_byte"] == 40.0:
            label_x, label_y, anchor = x + 13, y - 8, "start"
        elif row["intensity_flop_per_byte"] == 100.0:
            label_x, label_y, anchor = x + 14, y + 30, "start"
        else:
            label_x, label_y, anchor = x - 12, y + 30, "end"
        lines += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="10" fill="{color}"/>',
                  svg_text(label_x, label_y, f"I={row['intensity_flop_per_byte']:.0f}: {row['roofline_tflops']:.0f}", 15, color, 700, anchor)]
    lines += [
        f'<rect x="150" y="500" width="370" height="75" rx="12" fill="#FFF7F4"/>',
        svg_text(335, 531, "offload: 24 GB / 48 GB/s = 0.50 s", 17, RED, 700, "middle"),
        svg_text(335, 558, "compute = 0.35 s; no overlap => transfer dominates", 15, MUTED, 400, "middle"),
    ]
    widths = (390, 360, 330, 300, 270, 240)
    fills = ("#F1F3F5", "#EAF2FF", "#EAF2FF", "#E8F6F3", "#FFF3D6", "#FFF7F4")
    colors = (INK, BLUE, BLUE, TEAL, AMBER, RED)
    pretty = {
        "configuration_manifest": "configuration + manifest",
        "throughput_memory_counters": "throughput + memory counters",
        "profiler_critical_path": "profiler critical path",
        "matched_learning_curve": "matched learning curve",
        "paired_repeats_confidence_interval": "paired repeats + CI",
        "causal_intervention_controls": "causal intervention + controls",
    }
    for idx, (row, width, fill, color) in enumerate(zip(repro_rows, widths, fills, colors)):
        y = 590 - idx * 68
        x = 910 - width / 2
        lines += [f'<rect x="{x}" y="{y}" width="{width}" height="52" rx="10" fill="{fill}"/>',
                  svg_text(910, y + 32, f"{row['evidence_level']}  {pretty[row['evidence_object']]}", 15, color, 700, "middle")]
    lines += [
        svg_text(910, 655, "(a+b)+c = 3.14; a+(b+c) = 0.0", 15, RED, 700, "middle"),
        svg_text(910, 682, "non-associativity is not itself a failed decision", 15, MUTED, 400, "middle"),
        svg_text(60, 760, "Synthetic audit — E3 tests quality; E5 supports a scoped causal claim; no rung grants universal validity.", 15, MUTED),
        '</svg>',
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def run(output_dir: Path, plot_dir: Path) -> Dict:
    tracks = {
        "dtype_contract": dtype_contract_audit(),
        "loss_scaling_clocks": loss_scaling_clock_audit(),
        "stochastic_rounding": stochastic_rounding_audit(),
        "quantization_ledger": quantization_ledger_audit(),
        "global_batch": global_batch_audit(),
        "ring_allreduce": ring_allreduce_audit(),
        "parallelism_shapes": parallelism_shape_audit(),
        "zero_memory": zero_memory_audit(),
        "offload_roofline": offload_roofline_audit(),
        "reproducibility_evidence": reproducibility_evidence_audit(),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)
    csv_paths = []
    for name, rows in tracks.items():
        path = output_dir / f"{name}.csv"
        write_csv(path, rows)
        csv_paths.append(path)

    plot_paths = [
        plot_dir / "plot-low-precision-state-estimators-audit-v1.svg",
        plot_dir / "plot-distributed-batch-memory-audit-v1.svg",
        plot_dir / "plot-roofline-reproducibility-audit-v1.svg",
    ]
    write_low_precision_svg(plot_paths[0], tracks["dtype_contract"], tracks["stochastic_rounding"])
    write_distributed_svg(plot_paths[1], tracks["global_batch"], tracks["zero_memory"])
    write_roofline_svg(plot_paths[2], tracks["offload_roofline"], tracks["reproducibility_evidence"])

    dtypes = {row["format"]: row for row in tracks["dtype_contract"]}
    clocks = tracks["loss_scaling_clocks"]
    sr = tracks["stochastic_rounding"][0]
    quant = tracks["quantization_ledger"]
    batch = tracks["global_batch"][0]
    ring = {row["ranks"]: row for row in tracks["ring_allreduce"]}
    parallel = {row["case"]: row for row in tracks["parallelism_shapes"]}
    zero = {row["scheme"]: row for row in tracks["zero_memory"]}
    roof = {row["intensity_flop_per_byte"]: row for row in tracks["offload_roofline"]}
    repro = tracks["reproducibility_evidence"]

    checks = {
        "dtype_bf16_matches_fp32_exponent_bits": dtypes["BF16"]["exponent_bits"] == dtypes["FP32"]["exponent_bits"],
        "dtype_bf16_ulp_coarser_than_fp16": dtypes["BF16"]["ulp_at_one"] > dtypes["FP16"]["ulp_at_one"],
        "dtype_tf32_multiply_matches_fp16_precision_bits": dtypes["TF32-multiply"]["precision_bits"] == dtypes["FP16"]["precision_bits"],
        "dtype_fp32_has_finest_ulp_in_table": dtypes["FP32"]["ulp_at_one"] == min(row["ulp_at_one"] for row in tracks["dtype_contract"]),
        "loss_safe_scale_interval_nonempty": clocks[0]["safe_scale_min_proxy"] <= clocks[0]["safe_scale_max_proxy"],
        "loss_attempt_count_five": clocks[-1]["attempt_clock"] == 5,
        "loss_successful_update_count_four": clocks[-1]["successful_update"] == 4,
        "loss_overflow_does_not_advance_optimizer": clocks[2]["optimizer_advanced"] == 0,
        "loss_scale_trajectory_matches_contract": [row["scale_after"] for row in clocks] == [1024.0, 2048.0, 1024.0, 1024.0, 2048.0],
        "sr_probabilities_sum_to_one": math.isclose(sr["p_low"] + sr["p_high"], 1.0),
        "sr_one_step_conditionally_unbiased": math.isclose(sr["one_step_expectation"], sr["x"]),
        "sr_variance_below_quarter_grid_bound": sr["one_step_error_variance"] <= sr["variance_upper_bound"],
        "sr_expected_five_step_update_preserved": math.isclose(tracks["stochastic_rounding"][-1]["sr_expected_micro_update_trajectory"], 0.9),
        "quant_affine_codes_match_oracle": [row["quantized_code"] for row in quant] == [0, 1, 2, 3],
        "quant_affine_dequant_values_match_oracle": [row["dequantized_value"] for row in quant] == [-1.0, 0.0, 1.0, 2.0],
        "quant_state_ledger_saves_six_bytes_per_parameter": math.isclose(quant[0]["adam_baseline_bytes_per_parameter"] - quant[0]["adam_8bit_state_bytes_per_parameter"], 6.0),
        "quant_bucket_ratio_is_less_than_four_due_to_scales": 3.9 < quant[0]["payload_compression_ratio"] < 4.0,
        "batch_weighted_mean_equals_33_over_9": math.isclose(batch["correct_global_sample_mean"], 33.0 / 9.0),
        "batch_equal_rank_mean_is_four": math.isclose(batch["incorrect_equal_rank_mean"], 4.0),
        "batch_unequal_counts_create_bias": not math.isclose(batch["correct_global_sample_mean"], batch["incorrect_equal_rank_mean"]),
        "batch_counts_sum_to_nine": batch["global_sample_count"] == 9,
        "ring_eight_rank_volume_is_1_75_gib": math.isclose(ring[8]["per_rank_volume_gib"], 1.75),
        "ring_has_two_p_minus_one_phases": ring[16]["reduce_scatter_rounds"] + ring[16]["all_gather_rounds"] == 30,
        "ring_volume_tends_to_two_messages": ring[64]["per_rank_volume_gib"] > ring[8]["per_rank_volume_gib"],
        "parallel_column_output_is_sharded": parallel["column_parallel_linear"]["local_output_cols"] == 2048,
        "parallel_row_output_requires_sum": parallel["row_parallel_linear"]["collective"] == "all_reduce_sum",
        "parallel_pipeline_efficiency_is_32_over_39": math.isclose(parallel["pipeline_8_stages_32_microbatches"]["pipeline_efficiency_proxy"], 32.0 / 39.0),
        "zero_ddp_is_16_bytes_per_parameter": math.isclose(zero["DDP"]["bytes_per_parameter_steady"], 16.0),
        "zero_stage1_is_5_5_bytes_per_parameter": math.isclose(zero["ZeRO-1"]["bytes_per_parameter_steady"], 5.5),
        "zero_stage3_is_2_bytes_per_parameter": math.isclose(zero["ZeRO-3"]["bytes_per_parameter_steady"], 2.0),
        "zero_live_peak_exceeds_steady_shard": zero["ZeRO-3"]["illustrative_live_peak_gb"] > zero["ZeRO-3"]["steady_model_state_gb_decimal"],
        "roofline_ridge_is_100_flop_per_byte": math.isclose(roof[100.0]["ridge_intensity"], 100.0),
        "roofline_low_intensity_is_bandwidth_bound": roof[40.0]["bottleneck"] == "bandwidth" and math.isclose(roof[40.0]["roofline_tflops"], 120.0),
        "roofline_high_intensity_hits_compute_ceiling": roof[200.0]["bottleneck"] == "compute" and math.isclose(roof[200.0]["roofline_tflops"], 300.0),
        "repro_floating_addition_is_nonassociative": repro[0]["left_association"] != repro[0]["right_association"],
        "repro_quality_first_tested_at_E3": [row["evidence_level"] for row in repro if row["directly_tests_training_quality"]][0] == "E3",
        "repro_causal_support_reserved_for_E5": [row["evidence_level"] for row in repro if row["supports_specific_causal_claim"]] == ["E5"],
        "repro_strong_scaling_efficiency_is_69_percent": math.isclose(repro[0]["strong_scaling_efficiency_64"], 800.0 / 1152.0),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError("failed checks: " + ", ".join(failed))

    artifact_paths = csv_paths + plot_paths
    payload = {
        "experiment_id": "EXP-TRN-608-V1",
        "seed": SEED,
        "evidence_level": "deterministic analytic and synthetic audit; not a real distributed training run",
        "track_count": len(tracks),
        "check_count": len(checks),
        "passed_check_count": sum(bool(value) for value in checks.values()),
        "checks": checks,
        "artifacts": [
            {"name": path.name, "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in artifact_paths
        ],
        "key_results": {
            "safe_loss_scale_proxy": [64.0, 128.0],
            "sr_error_variance": sr["one_step_error_variance"],
            "correct_global_mean": batch["correct_global_sample_mean"],
            "incorrect_rank_mean": batch["incorrect_equal_rank_mean"],
            "ring_8_rank_volume_gib": ring[8]["per_rank_volume_gib"],
            "zero3_steady_gb": zero["ZeRO-3"]["steady_model_state_gb_decimal"],
            "illustrative_live_peak_gb": zero["ZeRO-3"]["illustrative_live_peak_gb"],
            "roofline_ridge": roof[100.0]["ridge_intensity"],
            "floating_left_association": repro[0]["left_association"],
            "floating_right_association": repro[0]["right_association"],
        },
        "boundaries": [
            "Format fields and analytic proxies do not identify an accelerator kernel.",
            "Synthetic collectives do not measure topology, contention, overlap, or failures.",
            "One-step stochastic-rounding unbiasedness does not prove trajectory or decision unbiasedness.",
            "Throughput and profiler evidence do not replace matched quality and causal controls.",
        ],
    }
    result_path = output_dir / "results.json"
    result_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "00-知识库管理/_labs/experiments/trn60.8-low-precision-distributed-audit-v1",
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=root / "00-知识库管理/_assets/plots/training-optimization",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run(args.output_dir, args.plot_dir)
    print(f"{payload['passed_check_count']}/{payload['check_count']} checks passed")
    print(f"wrote 1 JSON, {payload['track_count']} CSV, and 3 SVG artifacts")


if __name__ == "__main__":
    main()
