#!/usr/bin/env python3
"""Deterministic cross-volume evidence gate for LT-QUAL-02 (LT-41--84)."""

from __future__ import annotations

import argparse
import hashlib
import html
import math
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-learning-theory-qualification-02-gate-v2.svg"
)

CANONICAL = {
    "source_probabilities": "0.4,0.3,0.2,0.1",
    "target_probabilities": "0.1,0.2,0.3,0.4",
    "labels": "0,0,1,1",
    "model_probabilities": "0.1,0.3,0.7,0.55;0.25,0.45,0.85,0.9;0.05,0.6,0.6,0.95",
    "representation_spectra": "4,1,0.1;2,1,0.5;3,0.05,0.01",
    "online_contexts": "0,3,1,2,3,3,1,2",
    "hedge_eta": 0.8,
    "logging_policy": "0.7,0.2,0.1;0.6,0.3,0.1;0.4,0.4,0.2;0.2,0.5,0.3",
    "target_policy": "0.1,0.7,0.2;0.1,0.7,0.2;0.1,0.8,0.1;0.1,0.8,0.1",
    "logged_contexts": "0,3,1,2,3,0",
    "logged_actions": "0,1,0,1,2,1",
    "design": "1,0,1;0,1,1",
    "responses": "1,1",
    "null_shift": 2.0,
    "rescale": 4.0,
    "kernel_rho": 0.6,
    "kernel_time": 3.0,
    "initial_residual": "1,0",
    "particle_a": "1,-1",
    "particle_w": "0.5,-0.25",
    "particle_step": 0.2,
    "particle_target": 1.0,
}


@dataclass(frozen=True)
class TrackA:
    source_risks: tuple[float, ...]
    target_risks: tuple[float, ...]
    target_calibration_gaps: tuple[float, ...]
    importance_weights: tuple[float, ...]
    ess_fraction: float
    source_winner: int
    target_winner: int
    effective_ranks: tuple[float, ...]


@dataclass(frozen=True)
class TrackB:
    horizon: int
    hedge_loss: float
    best_loss: float
    regret: float
    final_probabilities: tuple[float, ...]
    target_policy_risk: float
    observed_ips: float
    maximum_joint_ratio: float
    observed_ess: float
    observed_ratios: tuple[float, ...]


@dataclass(frozen=True)
class TrackC:
    min_norm: tuple[float, float, float]
    min_norm_length: float
    shifted_length: float
    train_residual: float
    null_test_gap: float
    sharpness_base: float
    sharpness_scaled: float
    path_quantity: float
    kernel_eigenvalues: tuple[float, float]
    residual_final_norm: float
    relative_feature_drift: float
    relative_ntk_drift: float
    regime: str


def fail(message: str) -> None:
    raise ValueError(message)


def floats(raw: str, label: str) -> tuple[float, ...]:
    try:
        values = tuple(float(piece.strip()) for piece in raw.split(",") if piece.strip())
    except ValueError as error:
        raise ValueError(f"{label} must be a comma-separated numeric list") from error
    if not values or any(not math.isfinite(value) for value in values):
        fail(f"{label} must contain finite values")
    return values


def ints(raw: str, label: str) -> tuple[int, ...]:
    values = floats(raw, label)
    if any(value != int(value) for value in values):
        fail(f"{label} must contain integers")
    return tuple(int(value) for value in values)


def matrix(raw: str, label: str) -> tuple[tuple[float, ...], ...]:
    rows = tuple(floats(row, label) for row in raw.split(";") if row.strip())
    if not rows:
        fail(f"{label} must contain rows")
    width = len(rows[0])
    if width == 0 or any(len(row) != width for row in rows):
        fail(f"{label} must be rectangular")
    return rows


def probability_vector(raw: str, label: str, *, positive: bool = False) -> tuple[float, ...]:
    values = floats(raw, label)
    if any(value < 0.0 or value > 1.0 for value in values):
        fail(f"{label} entries must lie in [0,1]")
    if positive and any(value <= 0.0 for value in values):
        fail(f"{label} entries must be positive")
    if not math.isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=1e-10):
        fail(f"{label} must sum to one")
    return values


def policy_matrix(raw: str, label: str, contexts: int, actions: int, *, positive: bool = False) -> tuple[tuple[float, ...], ...]:
    rows = matrix(raw, label)
    if len(rows) != contexts or any(len(row) != actions for row in rows):
        fail(f"{label} must be contexts x actions")
    for index, row in enumerate(rows):
        if any(value < 0.0 or value > 1.0 for value in row):
            fail(f"{label} row {index} entries must lie in [0,1]")
        if positive and any(value <= 0.0 for value in row):
            fail(f"{label} row {index} entries must be positive")
        if not math.isclose(sum(row), 1.0, rel_tol=0.0, abs_tol=1e-10):
            fail(f"{label} row {index} must sum to one")
    return rows


def parse_shared(args: argparse.Namespace) -> tuple[
    tuple[float, ...], tuple[float, ...], tuple[int, ...],
    tuple[tuple[float, ...], ...], tuple[tuple[float, ...], ...]
]:
    source = probability_vector(args.source_probabilities, "source-probabilities", positive=True)
    target = probability_vector(args.target_probabilities, "target-probabilities")
    labels = ints(args.labels, "labels")
    models = matrix(args.model_probabilities, "model-probabilities")
    spectra = matrix(args.representation_spectra, "representation-spectra")
    contexts = len(source)
    if len(target) != contexts or len(labels) != contexts:
        fail("source, target and labels must have equal context length")
    if any(label not in (0, 1) for label in labels):
        fail("labels must be binary")
    if len(models) < 2 or any(len(row) != contexts for row in models):
        fail("model-probabilities needs at least two models over every context")
    if any(value < 0.0 or value > 1.0 for row in models for value in row):
        fail("model probabilities must lie in [0,1]")
    if len(spectra) != len(models) or any(len(row) < 2 for row in spectra):
        fail("representation-spectra needs one row of length at least two per model")
    if any(value <= 0.0 for row in spectra for value in row):
        fail("representation eigenvalues must be positive")
    return source, target, labels, models, spectra


def losses(models: tuple[tuple[float, ...], ...], labels: tuple[int, ...]) -> tuple[tuple[float, ...], ...]:
    return tuple(tuple((model[x] - labels[x]) ** 2 for model in models) for x in range(len(labels)))


def compute_track_a(args: argparse.Namespace) -> TrackA:
    source, target, labels, models, spectra = parse_shared(args)
    source_risks = tuple(sum(q * (score - y) ** 2 for q, score, y in zip(source, model, labels)) for model in models)
    target_risks = tuple(sum(p * (score - y) ** 2 for p, score, y in zip(target, model, labels)) for model in models)
    calibration = tuple(sum(p * abs(score - y) for p, score, y in zip(target, model, labels)) for model in models)
    weights = tuple(p / q for p, q in zip(target, source))
    second_moment = sum(q * weight * weight for q, weight in zip(source, weights))
    effective_ranks = tuple(sum(row) / max(row) for row in spectra)
    return TrackA(
        source_risks=source_risks,
        target_risks=target_risks,
        target_calibration_gaps=calibration,
        importance_weights=weights,
        ess_fraction=1.0 / second_moment,
        source_winner=min(range(len(models)), key=source_risks.__getitem__),
        target_winner=min(range(len(models)), key=target_risks.__getitem__),
        effective_ranks=effective_ranks,
    )


def compute_track_b(args: argparse.Namespace) -> TrackB:
    source, target, labels, models, _ = parse_shared(args)
    loss_table = losses(models, labels)
    contexts = ints(args.online_contexts, "online-contexts")
    if not contexts or any(context < 0 or context >= len(source) for context in contexts):
        fail("online-contexts contains an invalid context")
    if args.hedge_eta <= 0.0:
        fail("hedge-eta must be positive")
    cumulative = [0.0] * len(models)
    hedge_loss = 0.0
    for context in contexts:
        unnormalized = [math.exp(-args.hedge_eta * value) for value in cumulative]
        total = sum(unnormalized)
        probabilities = [value / total for value in unnormalized]
        row = loss_table[context]
        hedge_loss += sum(probability * loss for probability, loss in zip(probabilities, row))
        cumulative = [old + loss for old, loss in zip(cumulative, row)]
    final_weights = [math.exp(-args.hedge_eta * value) for value in cumulative]
    final_total = sum(final_weights)

    logging = policy_matrix(args.logging_policy, "logging-policy", len(source), len(models), positive=True)
    policy = policy_matrix(args.target_policy, "target-policy", len(source), len(models))
    logged_contexts = ints(args.logged_contexts, "logged-contexts")
    logged_actions = ints(args.logged_actions, "logged-actions")
    if len(logged_contexts) != len(logged_actions) or not logged_contexts:
        fail("logged contexts/actions must have equal nonzero length")
    if any(context < 0 or context >= len(source) for context in logged_contexts):
        fail("logged-contexts contains an invalid context")
    if any(action < 0 or action >= len(models) for action in logged_actions):
        fail("logged-actions contains an invalid action")

    true_risk = sum(
        target[x] * sum(policy[x][action] * loss_table[x][action] for action in range(len(models)))
        for x in range(len(source))
    )
    ratios: list[float] = []
    contributions: list[float] = []
    for context, action in zip(logged_contexts, logged_actions):
        ratio = (target[context] / source[context]) * (policy[context][action] / logging[context][action])
        ratios.append(ratio)
        contributions.append(ratio * loss_table[context][action])
    maximum_joint_ratio = max(
        (target[x] / source[x]) * (policy[x][action] / logging[x][action])
        for x in range(len(source)) for action in range(len(models))
    )
    ratio_sum = sum(ratios)
    observed_ess = ratio_sum * ratio_sum / sum(value * value for value in ratios) if ratio_sum > 0 else 0.0
    return TrackB(
        horizon=len(contexts), hedge_loss=hedge_loss, best_loss=min(cumulative),
        regret=hedge_loss - min(cumulative),
        final_probabilities=tuple(value / final_total for value in final_weights),
        target_policy_risk=true_risk, observed_ips=sum(contributions) / len(contributions),
        maximum_joint_ratio=maximum_joint_ratio, observed_ess=observed_ess,
        observed_ratios=tuple(ratios),
    )


def solve_2x2(matrix_: tuple[tuple[float, float], tuple[float, float]], rhs: tuple[float, float]) -> tuple[float, float]:
    (a, b), (c, d) = matrix_
    determinant = a * d - b * c
    if abs(determinant) <= 1e-12:
        fail("design must have full row rank")
    return ((d * rhs[0] - b * rhs[1]) / determinant, (-c * rhs[0] + a * rhs[1]) / determinant)


def compute_track_c(args: argparse.Namespace) -> TrackC:
    design = matrix(args.design, "design")
    responses = floats(args.responses, "responses")
    if len(design) != 2 or len(design[0]) != 3 or len(responses) != 2:
        fail("design must be 2x3 and responses length 2")
    gram = (
        (sum(design[0][j] ** 2 for j in range(3)), sum(design[0][j] * design[1][j] for j in range(3))),
        (sum(design[1][j] * design[0][j] for j in range(3)), sum(design[1][j] ** 2 for j in range(3))),
    )
    alpha = solve_2x2(gram, (responses[0], responses[1]))
    minimum = tuple(sum(design[i][j] * alpha[i] for i in range(2)) for j in range(3))
    cross = (
        design[0][1] * design[1][2] - design[0][2] * design[1][1],
        design[0][2] * design[1][0] - design[0][0] * design[1][2],
        design[0][0] * design[1][1] - design[0][1] * design[1][0],
    )
    cross_length = math.sqrt(sum(value * value for value in cross))
    if cross_length <= 1e-12:
        fail("design rows must be independent")
    null = tuple(value / cross_length for value in cross)
    shifted = tuple(value + args.null_shift * direction for value, direction in zip(minimum, null))
    residual = math.sqrt(sum(
        (sum(design[i][j] * minimum[j] for j in range(3)) - responses[i]) ** 2 for i in range(2)
    ))
    if args.rescale <= 0.0:
        fail("rescale must be positive")
    if not -1.0 < args.kernel_rho < 1.0 or args.kernel_time < 0.0:
        fail("kernel-rho must lie in (-1,1) and kernel-time be nonnegative")
    initial = floats(args.initial_residual, "initial-residual")
    if len(initial) != 2 or math.hypot(*initial) <= 0.0:
        fail("initial-residual must be a nonzero two-vector")
    plus_lambda, minus_lambda = 1 + args.kernel_rho, 1 - args.kernel_rho
    plus = (initial[0] + initial[1]) / math.sqrt(2)
    minus = (initial[0] - initial[1]) / math.sqrt(2)
    plus_t = plus * math.exp(-plus_lambda * args.kernel_time)
    minus_t = minus * math.exp(-minus_lambda * args.kernel_time)
    final = ((plus_t + minus_t) / math.sqrt(2), (plus_t - minus_t) / math.sqrt(2))

    particle_a = floats(args.particle_a, "particle-a")
    particle_w = floats(args.particle_w, "particle-w")
    if len(particle_a) < 2 or len(particle_a) != len(particle_w):
        fail("particle lists must have equal length at least two")
    if args.particle_step <= 0.0:
        fail("particle-step must be positive")
    count = len(particle_a)
    prediction = sum(a * w for a, w in zip(particle_a, particle_w)) / count
    scalar_residual = prediction - args.particle_target
    next_a = tuple(a - args.particle_step * scalar_residual * w / count for a, w in zip(particle_a, particle_w))
    next_w = tuple(w - args.particle_step * scalar_residual * a / count for a, w in zip(particle_a, particle_w))
    feature_before = sum(w * w for w in particle_w) / count
    feature_after = sum(w * w for w in next_w) / count
    ntk_before = sum(a * a + w * w for a, w in zip(particle_a, particle_w)) / (count * count)
    ntk_after = sum(a * a + w * w for a, w in zip(next_a, next_w)) / (count * count)
    feature_drift = abs(feature_after - feature_before) / max(feature_before, 1e-12)
    ntk_drift = abs(ntk_after - ntk_before) / max(ntk_before, 1e-12)
    return TrackC(
        min_norm=(minimum[0], minimum[1], minimum[2]),
        min_norm_length=math.sqrt(sum(value * value for value in minimum)),
        shifted_length=math.sqrt(sum(value * value for value in shifted)),
        train_residual=residual, null_test_gap=abs(args.null_shift),
        sharpness_base=2.0, sharpness_scaled=args.rescale ** 2 + args.rescale ** -2,
        path_quantity=1.0, kernel_eigenvalues=(plus_lambda, minus_lambda),
        residual_final_norm=math.hypot(*final), relative_feature_drift=feature_drift,
        relative_ntk_drift=ntk_drift,
        regime="feature-moving" if max(feature_drift, ntk_drift) >= 0.1 else "near-lazy",
    )


def fmt(values: tuple[float, ...]) -> str:
    return ",".join(f"{value:.6f}" for value in values)


def stdout_lines(a: TrackA, b: TrackB, c: TrackC) -> tuple[str, str, str]:
    return (
        f"TRACK A source_brier={fmt(a.source_risks)} target_brier={fmt(a.target_risks)} "
        f"target_cal_gap={fmt(a.target_calibration_gaps)} weights={fmt(a.importance_weights)} "
        f"ess_fraction={a.ess_fraction:.6f} source_winner={a.source_winner} "
        f"target_winner={a.target_winner} effective_rank={fmt(a.effective_ranks)}",
        f"TRACK B T={b.horizon} hedge_loss={b.hedge_loss:.6f} best={b.best_loss:.6f} "
        f"regret={b.regret:.6f} final_probs={fmt(b.final_probabilities)} "
        f"target_policy_risk={b.target_policy_risk:.6f} observed_ips={b.observed_ips:.6f} "
        f"max_joint_ratio={b.maximum_joint_ratio:.6f} observed_ess={b.observed_ess:.6f} "
        f"observed_ratios={fmt(b.observed_ratios)}",
        f"TRACK C min_norm={fmt(c.min_norm)} min_length={c.min_norm_length:.6f} "
        f"shifted_length={c.shifted_length:.6f} train_residual={c.train_residual:.6f} "
        f"null_test_gap={c.null_test_gap:.6f} sharpness={c.sharpness_base:.6f}->{c.sharpness_scaled:.6f} "
        f"path={c.path_quantity:.6f} kernel_eigenvalues={fmt(c.kernel_eigenvalues)} "
        f"residual_final_norm={c.residual_final_norm:.6f} feature_drift={c.relative_feature_drift:.6f} "
        f"ntk_drift={c.relative_ntk_drift:.6f} regime={c.regime}",
    )


def text(x: float, y: float, value: str, *, size: int = 18, fill: str = "#172033", weight: int = 500, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Arial,sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{html.escape(value)}</text>'
    )


def render_svg(a: TrackA, b: TrackB, c: TrackC, output: Path) -> None:
    width, height = 1500, 1080
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1500" height="1080" fill="#F7F4EE"/>',
        '<rect x="54" y="40" width="1392" height="90" rx="22" fill="#172033"/>',
        text(82, 79, "LT-QUAL-02 · one service, three ledgers, five theory interfaces", size=27, fill="#FFFFFF", weight=700),
        text(82, 111, "model/representation selection · reliable interactive deployment · deep-mechanism audit", size=17, fill="#CBD5E1"),
    ]
    panels = ((54, 154, "A", "source selection -> target risk and representation audit", "#2563EB"),
              (54, 432, "B", "online routing -> off-policy deployment evidence", "#7C3AED"),
              (54, 710, "C", "training fit -> invariant mechanism and regime boundary", "#059669"))
    for x, y, label, title, color in panels:
        parts.extend([
            f'<rect x="{x}" y="{y}" width="1392" height="250" rx="20" fill="#FFFFFF" stroke="#D7DCE5" stroke-width="2"/>',
            f'<circle cx="{x + 38}" cy="{y + 38}" r="22" fill="{color}"/>',
            text(x + 38, y + 45, label, size=19, fill="#FFFFFF", weight=700, anchor="middle"),
            text(x + 76, y + 45, title, size=22, weight=700),
        ])

    # A: paired source/target Brier bars.
    base_x, base_y = 105, 360
    scale = 1150
    colors = ("#2563EB", "#7C3AED", "#D97706")
    for index, (source_risk, target_risk, color) in enumerate(zip(a.source_risks, a.target_risks, colors)):
        x = base_x + index * 190
        parts.extend([
            f'<rect x="{x}" y="{base_y - source_risk * scale:.1f}" width="56" height="{source_risk * scale:.1f}" rx="7" fill="{color}" opacity="0.38"/>',
            f'<rect x="{x + 66}" y="{base_y - target_risk * scale:.1f}" width="56" height="{target_risk * scale:.1f}" rx="7" fill="{color}"/>',
            text(x + 61, 384, f"M{index}: S / T", size=13, fill=color, weight=650, anchor="middle"),
        ])
    parts.extend([
        text(744, 226, f"source winner M{a.source_winner}; target winner M{a.target_winner}", size=20, fill="#1D4ED8", weight=700),
        text(744, 262, f"density ratios = ({fmt(a.importance_weights)})", size=17),
        text(744, 294, f"population ESS fraction = {a.ess_fraction:.3f}", size=17),
        text(744, 326, f"representation effective ranks = ({fmt(a.effective_ranks)})", size=17),
        text(744, 358, "source winner != target winner; non-collapse != transfer", size=16, fill="#9A3412", weight=700),
    ])

    # B: Hedge cumulative result and OPE ratio bars.
    parts.extend([
        '<rect x="92" y="507" width="620" height="140" rx="14" fill="#F5F3FF"/>',
        text(118, 540, f"Hedge loss {b.hedge_loss:.3f}", size=20, fill="#6D28D9", weight=700),
        text(118, 576, f"best fixed {b.best_loss:.3f}  -> regret {b.regret:.3f}", size=18),
        text(118, 612, f"final mixture ({fmt(b.final_probabilities)})", size=17),
    ])
    max_ratio = max(b.observed_ratios) if b.observed_ratios else 1.0
    for index, ratio in enumerate(b.observed_ratios):
        x = 430 + index * 42
        height_ = 92 * ratio / max(max_ratio, 1e-12)
        parts.append(f'<rect x="{x}" y="{630 - height_:.1f}" width="24" height="{height_:.1f}" rx="4" fill="#7C3AED" opacity="0.72"/>')
    parts.extend([
        text(744, 504, f"target policy risk = {b.target_policy_risk:.3f}", size=20, fill="#6D28D9", weight=700),
        text(744, 540, f"one observed IPS mean = {b.observed_ips:.3f}", size=17),
        text(744, 574, f"max context-action ratio = {b.maximum_joint_ratio:.3f}", size=17),
        text(744, 608, f"observed weight ESS = {b.observed_ess:.3f} / {len(b.observed_ratios)}", size=17),
        text(744, 642, "regret != target risk; unbiasedness != safe deployment", size=16, fill="#9A3412", weight=700),
    ])

    # C: four mechanism cards.
    cards = (
        (92, "same fit", f"||w_min|| {c.min_norm_length:.3f} -> shifted {c.shifted_length:.3f}"),
        (390, "same function", f"sharpness {c.sharpness_base:.1f} -> {c.sharpness_scaled:.3f}"),
        (688, "fixed kernel", f"lambda ({fmt(c.kernel_eigenvalues)}), ||r_t|| {c.residual_final_norm:.3f}"),
        (986, "finite particles", f"feature {c.relative_feature_drift:.3f}; NTK {c.relative_ntk_drift:.3f}"),
    )
    for x, title_, body in cards:
        parts.extend([
            f'<rect x="{x}" y="792" width="262" height="105" rx="14" fill="#ECFDF5" stroke="#A7F3D0"/>',
            text(x + 18, 827, title_, size=17, fill="#047857", weight=700),
            text(x + 18, 864, body, size=14),
        ])
    parts.extend([
        text(92, 928, f"null test gap={c.null_test_gap:.2f}; path={c.path_quantity:.2f}; regime={c.regime}", size=17, fill="#047857", weight=700),
        text(820, 928, "fit/dynamics/proxy != population explanation", size=16, fill="#9A3412", weight=700),
    ])

    parts.extend([
        '<rect x="54" y="996" width="1392" height="56" rx="17" fill="#172033"/>',
        text(750, 1020, "task · data · representation · model · selection · calibration · shift · protocol · feedback · comparator · invariance · regime · deployment", size=15, fill="#E2E8F0", weight=600, anchor="middle"),
        text(750, 1043, "A valid cross-volume claim preserves predictor, sample, event and quantifier across every arrow.", size=14, fill="#94A3B8", anchor="middle"),
        '</svg>',
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--source-probabilities", default=CANONICAL["source_probabilities"])
    result.add_argument("--target-probabilities", default=CANONICAL["target_probabilities"])
    result.add_argument("--labels", default=CANONICAL["labels"])
    result.add_argument("--model-probabilities", default=CANONICAL["model_probabilities"])
    result.add_argument("--representation-spectra", default=CANONICAL["representation_spectra"])
    result.add_argument("--online-contexts", default=CANONICAL["online_contexts"])
    result.add_argument("--hedge-eta", type=float, default=CANONICAL["hedge_eta"])
    result.add_argument("--logging-policy", default=CANONICAL["logging_policy"])
    result.add_argument("--target-policy", default=CANONICAL["target_policy"])
    result.add_argument("--logged-contexts", default=CANONICAL["logged_contexts"])
    result.add_argument("--logged-actions", default=CANONICAL["logged_actions"])
    result.add_argument("--design", default=CANONICAL["design"])
    result.add_argument("--responses", default=CANONICAL["responses"])
    result.add_argument("--null-shift", type=float, default=CANONICAL["null_shift"])
    result.add_argument("--rescale", type=float, default=CANONICAL["rescale"])
    result.add_argument("--kernel-rho", type=float, default=CANONICAL["kernel_rho"])
    result.add_argument("--kernel-time", type=float, default=CANONICAL["kernel_time"])
    result.add_argument("--initial-residual", default=CANONICAL["initial_residual"])
    result.add_argument("--particle-a", default=CANONICAL["particle_a"])
    result.add_argument("--particle-w", default=CANONICAL["particle_w"])
    result.add_argument("--particle-step", type=float, default=CANONICAL["particle_step"])
    result.add_argument("--particle-target", type=float, default=CANONICAL["particle_target"])
    result.add_argument("--output", type=Path)
    return result


def is_canonical(args: argparse.Namespace) -> bool:
    return all(getattr(args, key) == value for key, value in CANONICAL.items())


def main() -> None:
    args = parser().parse_args()
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        fail("noncanonical runs require --output")
    output = args.output.resolve() if args.output else DEFAULT_SVG
    if not canonical and output == DEFAULT_SVG.resolve():
        fail("noncanonical runs cannot overwrite canonical SVG")
    a = compute_track_a(args)
    b = compute_track_b(args)
    c = compute_track_c(args)
    render_svg(a, b, c, output)
    for line in stdout_lines(a, b, c):
        print(line)
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
