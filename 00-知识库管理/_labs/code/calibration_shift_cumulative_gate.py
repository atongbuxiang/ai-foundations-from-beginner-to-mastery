#!/usr/bin/env python3
"""Deterministic three-track evidence gate for REL-CUM-01 (LT-61--68).

Track A separates calibration, proper scoring and predictive-mixture variance.
Track B separates exchangeable conformal ranks from covariate-shift importance
weighting and overlap. Track C separates domain-adaptation discrepancy, joint
ideal error, OOD ranking and average/worst-group risk. The finite fixtures do
not certify universal robustness, causal invariance or personal mastery.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import itertools
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CANONICAL_OUTPUT = (
    ROOT / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-calibration-shift-cumulative-gate-v2.svg"
)

INK = "#172033"
MUTED = "#5E6B82"
GRID = "#CBD7E6"
BG = "#F5F8FC"
PAPER = "#FFFFFF"
BLUE = "#2F63E9"
TEAL = "#0A9D88"
AMBER = "#BE7812"
RED = "#C84032"
PURPLE = "#7656C7"


@dataclass(frozen=True)
class CalibrationSummary:
    probabilities: tuple[float, ...]
    event_rates: tuple[float, ...]
    accuracy: float
    ece: float
    brier: float
    log_loss: float
    uncertainty: float
    resolution: float
    reliability: float
    mixture_mean: float
    aleatoric_variance: float
    epistemic_variance: float
    total_variance: float


@dataclass(frozen=True)
class CoverageShiftSummary:
    calibration_size: int
    alpha: float
    rank_index: int
    quantile: float
    finite_rank_coverage: float
    interval_low: float
    interval_high: float
    weights: tuple[float, ...]
    source_risk: float
    target_risk: float
    weighted_risk: float
    second_weight_moment: float
    effective_sample_size: float
    clipped_unnormalized_risk: float
    clipped_self_normalized_risk: float


@dataclass(frozen=True)
class RobustnessSummary:
    divergence: float
    source_risk: float
    target_risk: float
    joint_ideal_error: float
    adaptation_bound: float
    auroc: float
    id_acceptance: float
    ood_false_acceptance: float
    average_group_risk: float
    worst_group_risk: float


def parse_csv(text: str, name: str) -> tuple[float, ...]:
    try:
        values = tuple(float(piece.strip()) for piece in text.split(","))
    except ValueError as exc:
        raise SystemExit(f"{name} must be a comma-separated numeric list") from exc
    if not values or any(not math.isfinite(value) for value in values):
        raise SystemExit(f"{name} must contain finite values")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forecast-probabilities", default="0.1,0.4,0.7,0.9")
    parser.add_argument("--event-rates", default="0.2,0.4,0.6,0.8")
    parser.add_argument("--bin-size", type=int, default=5)
    parser.add_argument("--mixture-weights", default="0.4,0.6")
    parser.add_argument("--mixture-means", default="-1,2")
    parser.add_argument("--mixture-variances", default="0.5,1.5")
    parser.add_argument("--conformal-scores", default="0.1,0.2,0.25,0.4,0.55,0.7,0.9")
    parser.add_argument("--alpha", type=float, default=0.25)
    parser.add_argument("--prediction", type=float, default=3.2)
    parser.add_argument("--source-probabilities", default="0.5,0.4,0.1")
    parser.add_argument("--target-probabilities", default="0.2,0.3,0.5")
    parser.add_argument("--losses", default="0.1,0.3,0.8")
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--weight-clip", type=float, default=2.0)
    parser.add_argument("--source-label-threshold", type=int, default=1)
    parser.add_argument("--target-label-threshold", type=int, default=2)
    parser.add_argument("--id-scores", default="0.9,0.8,0.6")
    parser.add_argument("--ood-scores", default="0.7,0.4,0.2")
    parser.add_argument("--ood-threshold", type=float, default=0.65)
    parser.add_argument("--group-weights", default="0.7,0.2,0.1")
    parser.add_argument("--group-risks", default="0.1,0.2,0.5")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def normalized(values: tuple[float, ...], name: str, *, strictly_positive: bool = True) -> None:
    if strictly_positive and any(value <= 0 for value in values):
        raise SystemExit(f"{name} must be strictly positive")
    if not strictly_positive and any(value < 0 for value in values):
        raise SystemExit(f"{name} must be nonnegative")
    if not math.isclose(sum(values), 1.0, abs_tol=1e-12):
        raise SystemExit(f"{name} must sum to one")


def validate(args: argparse.Namespace) -> tuple[tuple[float, ...], ...]:
    forecast = parse_csv(args.forecast_probabilities, "forecast-probabilities")
    event = parse_csv(args.event_rates, "event-rates")
    mix_w = parse_csv(args.mixture_weights, "mixture-weights")
    mix_m = parse_csv(args.mixture_means, "mixture-means")
    mix_v = parse_csv(args.mixture_variances, "mixture-variances")
    scores = parse_csv(args.conformal_scores, "conformal-scores")
    source = parse_csv(args.source_probabilities, "source-probabilities")
    target = parse_csv(args.target_probabilities, "target-probabilities")
    losses = parse_csv(args.losses, "losses")
    id_scores = parse_csv(args.id_scores, "id-scores")
    ood_scores = parse_csv(args.ood_scores, "ood-scores")
    group_w = parse_csv(args.group_weights, "group-weights")
    group_r = parse_csv(args.group_risks, "group-risks")
    if len(forecast) != len(event) or len(forecast) < 2:
        raise SystemExit("forecast-probabilities and event-rates must have the same length >=2")
    if any(not 0 < value < 1 for value in forecast):
        raise SystemExit("forecast probabilities must lie strictly between zero and one")
    if any(not 0 <= value <= 1 for value in event):
        raise SystemExit("event rates must lie in [0,1]")
    if args.bin_size <= 0 or any(not math.isclose(value * args.bin_size, round(value * args.bin_size), abs_tol=1e-12) for value in event):
        raise SystemExit("bin-size must be positive and make every event count integral")
    if not (len(mix_w) == len(mix_m) == len(mix_v)) or len(mix_w) < 2:
        raise SystemExit("mixture lists must have the same length >=2")
    normalized(mix_w, "mixture-weights")
    if any(value <= 0 for value in mix_v):
        raise SystemExit("mixture variances must be positive")
    if tuple(sorted(scores)) != scores or any(value < 0 for value in scores):
        raise SystemExit("conformal-scores must be sorted and nonnegative")
    if not 0 < args.alpha < 1:
        raise SystemExit("alpha must lie in (0,1)")
    rank_index = math.ceil((len(scores) + 1) * (1 - args.alpha))
    if rank_index > len(scores):
        raise SystemExit("alpha is too small for a finite calibration quantile")
    if not math.isfinite(args.prediction):
        raise SystemExit("prediction must be finite")
    if not (len(source) == len(target) == len(losses) == 3):
        raise SystemExit("source, target and losses must each contain three values")
    normalized(source, "source-probabilities")
    normalized(target, "target-probabilities")
    if any(value < 0 for value in losses):
        raise SystemExit("losses must be nonnegative")
    if args.sample_size <= 0 or args.weight_clip <= 0:
        raise SystemExit("sample-size and weight-clip must be positive")
    if args.source_label_threshold not in range(4) or args.target_label_threshold not in range(4):
        raise SystemExit("label thresholds must lie in {0,1,2,3}")
    if not id_scores or not ood_scores:
        raise SystemExit("ID and OOD score lists may not be empty")
    if not math.isfinite(args.ood_threshold):
        raise SystemExit("ood-threshold must be finite")
    if len(group_w) != len(group_r) or len(group_w) < 2:
        raise SystemExit("group lists must have the same length >=2")
    normalized(group_w, "group-weights")
    if any(value < 0 for value in group_r):
        raise SystemExit("group-risks must be nonnegative")
    return (
        forecast, event, mix_w, mix_m, mix_v, scores, source, target,
        losses, id_scores, ood_scores, group_w, group_r,
    )


def is_canonical(args: argparse.Namespace, values: tuple[tuple[float, ...], ...]) -> bool:
    return values == (
        (0.1, 0.4, 0.7, 0.9), (0.2, 0.4, 0.6, 0.8),
        (0.4, 0.6), (-1.0, 2.0), (0.5, 1.5),
        (0.1, 0.2, 0.25, 0.4, 0.55, 0.7, 0.9),
        (0.5, 0.4, 0.1), (0.2, 0.3, 0.5), (0.1, 0.3, 0.8),
        (0.9, 0.8, 0.6), (0.7, 0.4, 0.2),
        (0.7, 0.2, 0.1), (0.1, 0.2, 0.5),
    ) and (
        args.bin_size == 5 and args.alpha == 0.25 and args.prediction == 3.2
        and args.sample_size == 100 and args.weight_clip == 2.0
        and args.source_label_threshold == 1 and args.target_label_threshold == 2
        and args.ood_threshold == 0.65
    )


def calibration_summary(
    forecast: tuple[float, ...],
    event: tuple[float, ...],
    mix_w: tuple[float, ...],
    mix_m: tuple[float, ...],
    mix_v: tuple[float, ...],
) -> CalibrationSummary:
    bins = len(forecast)
    overall_rate = sum(event) / bins
    accuracy = sum(rate if probability >= 0.5 else 1 - rate for probability, rate in zip(forecast, event)) / bins
    ece = sum(abs(probability - rate) for probability, rate in zip(forecast, event)) / bins
    brier = sum((probability - rate) ** 2 + rate * (1 - rate) for probability, rate in zip(forecast, event)) / bins
    log_loss = sum(
        -(rate * math.log(probability) + (1 - rate) * math.log(1 - probability))
        for probability, rate in zip(forecast, event)
    ) / bins
    uncertainty = overall_rate * (1 - overall_rate)
    resolution = sum((rate - overall_rate) ** 2 for rate in event) / bins
    reliability = sum((probability - rate) ** 2 for probability, rate in zip(forecast, event)) / bins
    require_close = uncertainty - resolution + reliability
    if not math.isclose(brier, require_close, abs_tol=1e-12):
        raise AssertionError("Brier decomposition failed")
    mixture_mean = sum(weight * mean for weight, mean in zip(mix_w, mix_m))
    aleatoric = sum(weight * variance for weight, variance in zip(mix_w, mix_v))
    epistemic = sum(weight * (mean - mixture_mean) ** 2 for weight, mean in zip(mix_w, mix_m))
    return CalibrationSummary(
        forecast, event, accuracy, ece, brier, log_loss,
        uncertainty, resolution, reliability, mixture_mean,
        aleatoric, epistemic, aleatoric + epistemic,
    )


def coverage_shift_summary(
    scores: tuple[float, ...],
    alpha: float,
    prediction: float,
    source: tuple[float, ...],
    target: tuple[float, ...],
    losses: tuple[float, ...],
    sample_size: int,
    clip: float,
) -> CoverageShiftSummary:
    rank_index = math.ceil((len(scores) + 1) * (1 - alpha))
    quantile = scores[rank_index - 1]
    weights = tuple(target_value / source_value for source_value, target_value in zip(source, target))
    source_risk = sum(probability * loss for probability, loss in zip(source, losses))
    target_risk = sum(probability * loss for probability, loss in zip(target, losses))
    weighted_risk = sum(probability * weight * loss for probability, weight, loss in zip(source, weights, losses))
    second_moment = sum(probability * weight * weight for probability, weight in zip(source, weights))
    effective_size = sample_size / second_moment
    clipped = tuple(min(weight, clip) for weight in weights)
    numerator = sum(probability * weight * loss for probability, weight, loss in zip(source, clipped, losses))
    denominator = sum(probability * weight for probability, weight in zip(source, clipped))
    if not math.isclose(target_risk, weighted_risk, abs_tol=1e-12):
        raise AssertionError("importance-weight identity failed")
    return CoverageShiftSummary(
        len(scores), alpha, rank_index, quantile, rank_index / (len(scores) + 1),
        prediction - quantile, prediction + quantile, weights,
        source_risk, target_risk, weighted_risk, second_moment,
        effective_size, numerator, numerator / denominator,
    )


def threshold_hypotheses() -> tuple[tuple[int, int, int], ...]:
    return tuple(tuple(int(value >= threshold) for value in range(3)) for threshold in range(4))


def classification_risk(distribution: tuple[float, ...], prediction: tuple[int, ...], truth: tuple[int, ...]) -> float:
    return sum(probability for probability, guess, label in zip(distribution, prediction, truth) if guess != label)


def robustness_summary(
    source: tuple[float, ...],
    target: tuple[float, ...],
    source_label_threshold: int,
    target_label_threshold: int,
    id_scores: tuple[float, ...],
    ood_scores: tuple[float, ...],
    ood_threshold: float,
    group_w: tuple[float, ...],
    group_r: tuple[float, ...],
) -> RobustnessSummary:
    hypotheses = threshold_hypotheses()
    divergence = 0.0
    for first, second in itertools.combinations(hypotheses, 2):
        source_disagreement = sum(p for p, a, b in zip(source, first, second) if a != b)
        target_disagreement = sum(p for p, a, b in zip(target, first, second) if a != b)
        divergence = max(divergence, 2 * abs(source_disagreement - target_disagreement))
    source_truth = tuple(int(value >= source_label_threshold) for value in range(3))
    target_truth = tuple(int(value >= target_label_threshold) for value in range(3))
    risks = tuple(
        (
            classification_risk(source, hypothesis, source_truth),
            classification_risk(target, hypothesis, target_truth),
        )
        for hypothesis in hypotheses
    )
    selected_index = source_label_threshold
    source_risk, target_risk = risks[selected_index]
    joint_ideal = min(source_value + target_value for source_value, target_value in risks)
    bound = source_risk + 0.5 * divergence + joint_ideal
    pair_score = sum(
        1.0 if id_score > ood_score else 0.5 if id_score == ood_score else 0.0
        for id_score in id_scores for ood_score in ood_scores
    )
    auroc = pair_score / (len(id_scores) * len(ood_scores))
    id_acceptance = sum(score >= ood_threshold for score in id_scores) / len(id_scores)
    ood_false_acceptance = sum(score >= ood_threshold for score in ood_scores) / len(ood_scores)
    average_group = sum(weight * risk for weight, risk in zip(group_w, group_r))
    return RobustnessSummary(
        divergence, source_risk, target_risk, joint_ideal, bound,
        auroc, id_acceptance, ood_false_acceptance,
        average_group, max(group_r),
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, size: int = 14, color: str = INK, weight: int = 400) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" fill="{color}" font-weight="{weight}">{esc(value)}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 1.0) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def box(x: float, y: float, width: float, height: float, stroke: str = GRID, fill: str = PAPER, radius: int = 10) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
    )


def build_svg(a: CalibrationSummary, b: CoverageShiftSummary, c: RobustnessSummary) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1540" height="1000" viewBox="0 0 1540 1000">',
        f'<rect width="1540" height="1000" fill="{BG}"/>',
        text(70, 60, "Reliable prediction | probability, coverage, shift and robustness ledgers", 27, INK, 650),
        text(70, 91, "proper probability quality  ->  finite-rank coverage / overlap  ->  adaptation / OOD / group utility", 15, MUTED, 500),
    ]
    panel_y, panel_h, panel_w = 130, 600, 450
    panel_xs = (70, 545, 1020)
    for x, color in zip(panel_xs, (BLUE, AMBER, TEAL)):
        parts.extend((box(x, panel_y, panel_w, panel_h), line(x, panel_y + 2, x + panel_w, panel_y + 2, color, 7)))

    # A
    x = panel_xs[0]
    parts.extend((
        text(x + 24, 177, "A | calibration and uncertainty", 21, INK, 650),
        text(x + 24, 202, "equal-mass reliability bins + predictive mixture", 13, MUTED, 500),
        text(x + 24, 238, "forecast p  ->  empirical event rate", 13, INK, 600),
    ))
    for index, (probability, rate) in enumerate(zip(a.probabilities, a.event_rates)):
        y = 270 + index * 55
        parts.extend((
            box(x + 24, y - 24, 402, 43, GRID, "#FAFCFF"),
            text(x + 42, y + 2, f"bin {index + 1}", 12, MUTED, 600),
            text(x + 130, y + 2, f"p={probability:.2f}", 12, BLUE, 600),
            text(x + 225, y + 2, f"freq={rate:.2f}", 12, TEAL, 600),
            text(x + 334, y + 2, f"gap={probability - rate:+.2f}", 12, RED),
        ))
    parts.extend((
        box(x + 24, 490, 402, 92, BLUE, "#F7FAFF"),
        text(x + 40, 519, f"accuracy={a.accuracy:.3f}; ECE={a.ece:.3f}", 13, BLUE, 650),
        text(x + 40, 547, f"Brier={a.brier:.4f}; log loss={a.log_loss:.4f}", 13),
        text(x + 40, 571, f"U-R+Rel={a.uncertainty:.3f}-{a.resolution:.3f}+{a.reliability:.4f}", 12, MUTED),
        box(x + 24, 602, 402, 82, PURPLE, "#F8F6FF"),
        text(x + 40, 631, f"mixture mean={a.mixture_mean:.3f}", 13, PURPLE, 650),
        text(x + 40, 659, f"aleatoric={a.aleatoric_variance:.3f}; epistemic={a.epistemic_variance:.3f}; total={a.total_variance:.3f}", 12),
        text(x + 24, 714, "Accuracy, calibration and uncertainty answer different questions.", 11, MUTED),
    ))

    # B
    x = panel_xs[1]
    parts.extend((
        text(x + 24, 177, "B | coverage and overlap", 21, INK, 650),
        text(x + 24, 202, "split-conformal rank + exact covariate reweighting", 13, MUTED, 500),
        box(x + 24, 228, 402, 122, AMBER, "#FFF9EF"),
        text(x + 40, 257, f"m={b.calibration_size}; alpha={b.alpha:.2f}; k={b.rank_index}", 13, AMBER, 650),
        text(x + 40, 285, f"qhat={b.quantile:.3f}; finite rank coverage={b.finite_rank_coverage:.3f}", 13),
        text(x + 40, 313, f"prediction interval=[{b.interval_low:.3f}, {b.interval_high:.3f}]", 13, TEAL, 600),
        text(x + 40, 337, "guarantee: exchangeable marginal coverage", 12, RED, 500),
        text(x + 24, 390, f"importance weights={tuple(round(value, 3) for value in b.weights)}", 13, INK, 600),
        box(x + 24, 410, 402, 124, TEAL, "#F1FBF8"),
        text(x + 40, 439, f"source risk={b.source_risk:.3f}", 13),
        text(x + 40, 467, f"target = weighted risk={b.target_risk:.3f}", 13, TEAL, 650),
        text(x + 40, 495, f"E_s[w^2]={b.second_weight_moment:.3f}; ESS={b.effective_sample_size:.3f}", 13),
        text(x + 40, 521, "large weights expose weak overlap", 12, RED, 500),
        box(x + 24, 560, 402, 110, GRID, "#FAFCFF"),
        text(x + 40, 590, f"clipped unnormalized risk={b.clipped_unnormalized_risk:.3f}", 13, RED, 600),
        text(x + 40, 618, f"clipped self-normalized={b.clipped_self_normalized_risk:.3f}", 13),
        text(x + 40, 646, "clipping trades variance for estimand bias", 12, MUTED),
        text(x + 24, 714, "Exchangeability and overlap are different, non-interchangeable gates.", 11, MUTED),
    ))

    # C
    x = panel_xs[2]
    parts.extend((
        text(x + 24, 177, "C | adaptation, OOD and groups", 21, INK, 650),
        text(x + 24, 202, "finite HΔH audit + ranking/threshold + group risk", 13, MUTED, 500),
        box(x + 24, 228, 402, 142, TEAL, "#F1FBF8"),
        text(x + 40, 257, f"HΔH divergence={c.divergence:.3f}", 13, TEAL, 650),
        text(x + 40, 285, f"source risk={c.source_risk:.3f}; target risk={c.target_risk:.3f}", 13),
        text(x + 40, 313, f"joint ideal error lambda={c.joint_ideal_error:.3f}", 13, RED, 600),
        text(x + 40, 341, f"bound RHS={c.adaptation_bound:.3f}", 13, AMBER, 650),
        text(x + 40, 362, "small discrepancy cannot delete lambda", 12, MUTED),
        box(x + 24, 398, 402, 116, BLUE, "#F7FAFF"),
        text(x + 40, 427, f"OOD AUROC={c.auroc:.3f}", 13, BLUE, 650),
        text(x + 40, 455, f"ID acceptance={c.id_acceptance:.3f}", 13),
        text(x + 40, 483, f"OOD false acceptance={c.ood_false_acceptance:.3f}", 13, RED, 600),
        box(x + 24, 548, 402, 112, PURPLE, "#F8F6FF"),
        text(x + 40, 578, f"average group risk={c.average_group_risk:.3f}", 13, PURPLE, 650),
        text(x + 40, 606, f"worst-group risk={c.worst_group_risk:.3f}", 13, RED, 650),
        text(x + 40, 634, "robustness needs a declared denominator/set", 12, MUTED),
        text(x + 24, 714, "OOD ranking, threshold utility and causal invariance are not synonyms.", 11, MUTED),
    ))

    parts.extend((
        box(70, 760, 1400, 177, GRID, PAPER, 16),
        text(94, 803, "The eight-layer reliability audit", 20, INK, 650),
        text(94, 840, "joint law", 13, BLUE, 650),
        text(215, 840, "->", 18, MUTED, 600),
        text(255, 840, "predictive object", 13, PURPLE, 650),
        text(435, 840, "->", 18, MUTED, 600),
        text(475, 840, "assumption", 13, AMBER, 650),
        text(605, 840, "->", 18, MUTED, 600),
        text(645, 840, "certificate", 13, TEAL, 650),
        text(775, 840, "->", 18, MUTED, 600),
        text(815, 840, "selection", 13, RED, 650),
        text(930, 840, "->", 18, MUTED, 600),
        text(970, 840, "decision utility / shift set", 13, INK, 650),
        line(94, 872, 1445, 872),
        text(94, 911, "Evidence rule: calibrated != accurate; marginal coverage != conditional coverage; OOD score != robustness or causality.", 13, RED, 500),
        text(1245, 979, "REL-CUM-01 | deterministic finite fixtures", 11, MUTED, 500),
        "</svg>",
    ))
    return "\n".join(parts) + "\n"


def print_summary(output: Path, a: CalibrationSummary, b: CoverageShiftSummary, c: RobustnessSummary) -> None:
    print(
        "TRACK A "
        f"accuracy={a.accuracy:.6f} ece={a.ece:.6f} brier={a.brier:.6f} log_loss={a.log_loss:.6f} "
        f"uncertainty={a.uncertainty:.6f} resolution={a.resolution:.6f} reliability={a.reliability:.6f} "
        f"mixture_mean={a.mixture_mean:.6f} aleatoric={a.aleatoric_variance:.6f} "
        f"epistemic={a.epistemic_variance:.6f} total_variance={a.total_variance:.6f}"
    )
    print(
        "TRACK B "
        f"m={b.calibration_size} alpha={b.alpha:.6f} k={b.rank_index} quantile={b.quantile:.6f} "
        f"rank_coverage={b.finite_rank_coverage:.6f} interval={b.interval_low:.6f},{b.interval_high:.6f} "
        f"weights={','.join(f'{value:.6f}' for value in b.weights)} source_risk={b.source_risk:.6f} "
        f"target_risk={b.target_risk:.6f} weighted_risk={b.weighted_risk:.6f} "
        f"weight_second={b.second_weight_moment:.6f} ess={b.effective_sample_size:.6f} "
        f"clipped={b.clipped_unnormalized_risk:.6f} self_normalized={b.clipped_self_normalized_risk:.6f}"
    )
    print(
        "TRACK C "
        f"divergence={c.divergence:.6f} source_risk={c.source_risk:.6f} target_risk={c.target_risk:.6f} "
        f"joint_ideal={c.joint_ideal_error:.6f} bound={c.adaptation_bound:.6f} "
        f"auroc={c.auroc:.6f} id_accept={c.id_acceptance:.6f} ood_false_accept={c.ood_false_acceptance:.6f} "
        f"average_group={c.average_group_risk:.6f} worst_group={c.worst_group_risk:.6f}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    values = validate(args)
    canonical = is_canonical(args, values)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")
    (
        forecast, event, mix_w, mix_m, mix_v, scores, source, target,
        losses, id_scores, ood_scores, group_w, group_r,
    ) = values
    a = calibration_summary(forecast, event, mix_w, mix_m, mix_v)
    b = coverage_shift_summary(
        scores, args.alpha, args.prediction, source, target, losses,
        args.sample_size, args.weight_clip,
    )
    c = robustness_summary(
        source, target, args.source_label_threshold, args.target_label_threshold,
        id_scores, ood_scores, args.ood_threshold, group_w, group_r,
    )
    if c.target_risk > c.adaptation_bound + 1e-12:
        raise AssertionError("adaptation bound failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(a, b, c), encoding="utf-8")
    print_summary(output, a, b, c)


if __name__ == "__main__":
    main()
