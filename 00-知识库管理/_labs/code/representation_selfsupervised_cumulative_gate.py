#!/usr/bin/env python3
"""Deterministic three-track evidence gate for REPR-CUM-01 (LT-53--60).

Track A separates task-indexed representation risk, linear accessibility,
retrieval metrics and dependent augmented views. Track B computes the exact
Bayes candidate-index InfoNCE experiment together with a finite batch gradient
and latent-class collision probability. Track C separates covariance-based
non-collapse, VICReg penalties, EMA targets and masked-prediction Bayes risks.

The script proves no universal representation-learning theorem. It only makes
the finite fixtures, estimands and protocol changes reproducible.
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
    / "plot-representation-selfsupervised-cumulative-gate-v2.svg"
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

REPRESENTATIONS = ("identity", "invariant-S", "nuisance-N", "product", "enriched")
TASK_RISKS = {
    "identity": (0.0, 0.0, 0.25),
    "invariant-S": (0.0, 0.5, 0.5),
    "nuisance-N": (0.5, 0.0, 0.5),
    "product": (0.5, 0.5, 0.0),
    "enriched": (0.0, 0.0, 0.0),
}


@dataclass(frozen=True)
class RepresentationSummary:
    task_weights: tuple[float, float, float]
    weighted_risks: tuple[float, ...]
    best_representation: str
    triplet_loss: float
    average_precision: float
    recall_at_two: float
    effective_views: float
    nominal_views: int


@dataclass(frozen=True)
class ContrastiveSummary:
    match_probability: float
    candidates: int
    true_mutual_information: float
    bayes_loss: float
    infonce_bound: float
    bound_gap: float
    logits: tuple[float, ...]
    probabilities: tuple[float, ...]
    batch_loss: float
    similarity_gradients: tuple[float, ...]
    collision_probability: float


@dataclass(frozen=True)
class TargetSummary:
    covariance_eigenvalues: tuple[float, float, float]
    stable_rank: float
    participation_ratio: float
    entropy_effective_rank: float
    spectral_variance_penalty: float
    constant_variance_penalty: float
    ema_final: float
    conditional_log_risk: float
    conditional_square_risk: float
    nuisance_downstream_risk: float


def parse_csv(text: str, name: str) -> tuple[float, ...]:
    try:
        values = tuple(float(piece.strip()) for piece in text.split(","))
    except ValueError as exc:
        raise SystemExit(f"{name} must be a comma-separated numeric list") from exc
    if not values or any(not math.isfinite(value) for value in values):
        raise SystemExit(f"{name} must contain finite numbers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-weights", default="0.5,0.3,0.2")
    parser.add_argument("--positive-distance", type=float, default=0.8)
    parser.add_argument("--negative-distance", type=float, default=1.3)
    parser.add_argument("--triplet-margin", type=float, default=0.7)
    parser.add_argument("--source-units", type=int, default=12)
    parser.add_argument("--views-per-source", type=int, default=4)
    parser.add_argument("--view-correlation", type=float, default=0.6)
    parser.add_argument("--match-probability", type=float, default=0.8)
    parser.add_argument("--candidates", type=int, default=4)
    parser.add_argument("--similarities", default="1,0.5,-0.25")
    parser.add_argument("--temperature", type=float, default=0.5)
    parser.add_argument("--class-prior", default="0.5,0.3,0.2")
    parser.add_argument("--negatives", type=int, default=7)
    parser.add_argument("--ema-decay", type=float, default=0.75)
    parser.add_argument("--teacher-start", type=float, default=0.0)
    parser.add_argument("--student-sequence", default="1,3,-1,2")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def validate(args: argparse.Namespace) -> tuple[
    tuple[float, float, float], tuple[float, ...], tuple[float, ...], tuple[float, ...]
]:
    weights = parse_csv(args.task_weights, "task-weights")
    similarities = parse_csv(args.similarities, "similarities")
    prior = parse_csv(args.class_prior, "class-prior")
    sequence = parse_csv(args.student_sequence, "student-sequence")
    if len(weights) != 3 or any(value < 0 for value in weights) or not math.isclose(sum(weights), 1.0, abs_tol=1e-12):
        raise SystemExit("task-weights must contain three nonnegative values summing to one")
    if len(similarities) < 2:
        raise SystemExit("similarities must contain a positive followed by at least one negative")
    if any(value <= 0 for value in prior) or not math.isclose(sum(prior), 1.0, abs_tol=1e-12):
        raise SystemExit("class-prior must be strictly positive and sum to one")
    if not sequence:
        raise SystemExit("student-sequence may not be empty")
    finite_scalars = (
        args.positive_distance, args.negative_distance, args.triplet_margin,
        args.view_correlation, args.match_probability, args.temperature,
        args.ema_decay, args.teacher_start,
    )
    if any(not math.isfinite(value) for value in finite_scalars):
        raise SystemExit("all scalar parameters must be finite")
    if args.positive_distance < 0 or args.negative_distance < 0 or args.triplet_margin < 0:
        raise SystemExit("distances and triplet-margin must be nonnegative")
    if args.source_units <= 0 or args.views_per_source <= 0:
        raise SystemExit("source-units and views-per-source must be positive")
    if not 0 <= args.view_correlation <= 1:
        raise SystemExit("view-correlation must lie in [0,1]")
    if not 0.5 < args.match_probability < 1:
        raise SystemExit("match-probability must lie strictly between 0.5 and 1")
    if args.candidates < 2:
        raise SystemExit("candidates must be at least two")
    if args.temperature <= 0:
        raise SystemExit("temperature must be positive")
    if args.negatives < 1:
        raise SystemExit("negatives must be positive")
    if not 0 < args.ema_decay < 1:
        raise SystemExit("ema-decay must lie strictly between zero and one")
    return (weights[0], weights[1], weights[2]), similarities, prior, sequence


def is_canonical(
    args: argparse.Namespace,
    weights: tuple[float, float, float],
    similarities: tuple[float, ...],
    prior: tuple[float, ...],
    sequence: tuple[float, ...],
) -> bool:
    return (
        weights == (0.5, 0.3, 0.2)
        and similarities == (1.0, 0.5, -0.25)
        and prior == (0.5, 0.3, 0.2)
        and sequence == (1.0, 3.0, -1.0, 2.0)
        and args.positive_distance == 0.8
        and args.negative_distance == 1.3
        and args.triplet_margin == 0.7
        and args.source_units == 12
        and args.views_per_source == 4
        and args.view_correlation == 0.6
        and args.match_probability == 0.8
        and args.candidates == 4
        and args.temperature == 0.5
        and args.negatives == 7
        and args.ema_decay == 0.75
        and args.teacher_start == 0.0
    )


def representation_summary(
    weights: tuple[float, float, float],
    positive_distance: float,
    negative_distance: float,
    margin: float,
    source_units: int,
    views_per_source: int,
    view_correlation: float,
) -> RepresentationSummary:
    weighted = tuple(
        sum(weight * risk for weight, risk in zip(weights, TASK_RISKS[name]))
        for name in REPRESENTATIONS
    )
    best = min(range(len(weighted)), key=lambda index: (weighted[index], index))
    triplet = max(0.0, positive_distance - negative_distance + margin)
    relevance = (1, 0, 1, 0)
    relevant = sum(relevance)
    average_precision = sum(
        sum(relevance[: index + 1]) / (index + 1)
        for index, value in enumerate(relevance) if value
    ) / relevant
    recall_at_two = sum(relevance[:2]) / relevant
    nominal = source_units * views_per_source
    effective = nominal / (1 + (views_per_source - 1) * view_correlation)
    return RepresentationSummary(
        weights, weighted, REPRESENTATIONS[best], triplet,
        average_precision, recall_at_two, effective, nominal,
    )


def exact_candidate_loss(match_probability: float, candidates: int) -> float:
    """Exact H(I|X,Y_1:K) for a binary symmetric positive channel."""
    total = 0.0
    mass = 0.0
    for index in range(candidates):
        for anchor in (0, 1):
            for ys in itertools.product((0, 1), repeat=candidates):
                probability = 0.5 / candidates
                for candidate_index, value in enumerate(ys):
                    if candidate_index == index:
                        probability *= match_probability if value == anchor else 1 - match_probability
                    else:
                        probability *= 0.5
                ratios = tuple(
                    2 * (match_probability if value == anchor else 1 - match_probability)
                    for value in ys
                )
                posterior = ratios[index] / sum(ratios)
                total += probability * -math.log(posterior)
                mass += probability
    if not math.isclose(mass, 1.0, abs_tol=1e-12):
        raise AssertionError(f"candidate experiment mass is {mass}")
    return total


def contrastive_summary(
    match_probability: float,
    candidates: int,
    similarities: tuple[float, ...],
    temperature: float,
    prior: tuple[float, ...],
    negatives: int,
) -> ContrastiveSummary:
    binary_entropy = -(
        match_probability * math.log(match_probability)
        + (1 - match_probability) * math.log(1 - match_probability)
    )
    mutual_information = math.log(2) - binary_entropy
    bayes_loss = exact_candidate_loss(match_probability, candidates)
    bound = math.log(candidates) - bayes_loss
    logits = tuple(value / temperature for value in similarities)
    maximum = max(logits)
    exponentials = tuple(math.exp(value - maximum) for value in logits)
    probabilities = tuple(value / sum(exponentials) for value in exponentials)
    batch_loss = -math.log(probabilities[0])
    gradients = tuple(
        (probability - (1.0 if index == 0 else 0.0)) / temperature
        for index, probability in enumerate(probabilities)
    )
    collision = sum(
        class_probability * (1 - (1 - class_probability) ** negatives)
        for class_probability in prior
    )
    return ContrastiveSummary(
        match_probability, candidates, mutual_information, bayes_loss, bound,
        mutual_information - bound, logits, probabilities, batch_loss,
        gradients, collision,
    )


def target_summary(
    match_probability: float,
    ema_decay: float,
    teacher_start: float,
    sequence: tuple[float, ...],
) -> TargetSummary:
    eigenvalues = (9.0, 1.0, 0.0)
    trace = sum(eigenvalues)
    stable_rank = trace / max(eigenvalues)
    participation_ratio = trace * trace / sum(value * value for value in eigenvalues)
    positive_spectrum = tuple(value / trace for value in eigenvalues if value > 0)
    effective_rank = math.exp(-sum(value * math.log(value) for value in positive_spectrum))
    # Population-batch std=(3,1,0), gamma=1, eps=0; average over d, both views.
    spectral_penalty = 2 * sum(max(0.0, 1 - value) for value in (3.0, 1.0, 0.0)) / 3
    constant_penalty = 2.0
    teacher = teacher_start
    for student in sequence:
        teacher = ema_decay * teacher + (1 - ema_decay) * student
    conditional_log_risk = -(
        match_probability * math.log(match_probability)
        + (1 - match_probability) * math.log(1 - match_probability)
    )
    conditional_square_risk = match_probability * (1 - match_probability)
    return TargetSummary(
        eigenvalues, stable_rank, participation_ratio, effective_rank,
        spectral_penalty, constant_penalty, teacher,
        conditional_log_risk, conditional_square_risk, 0.5,
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


def build_svg(a: RepresentationSummary, b: ContrastiveSummary, c: TargetSummary) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1540" height="1000" viewBox="0 0 1540 1000">',
        f'<rect width="1540" height="1000" fill="{BG}"/>',
        text(70, 60, "Representation learning | task risk, candidate experiment, target dynamics", 27, INK, 650),
        text(70, 91, "task-indexed accessibility  ->  contrastive batch law  ->  non-collapse / self-generated targets", 15, MUTED, 500),
    ]
    panel_y, panel_h, panel_w = 130, 600, 450
    panel_xs = (70, 545, 1020)
    colors = (BLUE, AMBER, TEAL)
    for x, color in zip(panel_xs, colors):
        parts.extend((box(x, panel_y, panel_w, panel_h), line(x, panel_y + 2, x + panel_w, panel_y + 2, color, 7)))

    # Track A
    x = panel_xs[0]
    parts.extend((
        text(x + 24, 177, "A | task-indexed representation", 21, INK, 650),
        text(x + 24, 202, "affine accessibility + retrieval + view dependence", 13, MUTED, 500),
        text(x + 24, 240, f"task weights S/N/XOR = {a.task_weights}", 13),
    ))
    baseline_y = 490
    parts.append(line(x + 45, baseline_y, x + 416, baseline_y))
    maximum_risk = max(a.weighted_risks) or 1.0
    bar_width = 53
    for index, (name, risk) in enumerate(zip(REPRESENTATIONS, a.weighted_risks)):
        bar_x = x + 48 + index * 73
        height = 180 * risk / maximum_risk
        color = TEAL if name == a.best_representation else BLUE
        parts.append(f'<rect x="{bar_x}" y="{baseline_y - height}" width="{bar_width}" height="{height}" rx="3" fill="{color}"/>')
        parts.append(text(bar_x + 5, baseline_y - height - 8, f"{risk:.3f}", 12, color, 600))
        parts.append(text(bar_x - 2, baseline_y + 23, ("id", "inv-S", "nuis-N", "prod", "enrich")[index], 11, MUTED, 500))
    parts.extend((
        text(x + 24, 545, f"best task-family risk: {a.best_representation} = {min(a.weighted_risks):.3f}", 14, TEAL, 650),
        box(x + 24, 572, 402, 112, BLUE, "#F7FAFF"),
        text(x + 40, 600, f"triplet hinge = {a.triplet_loss:.3f}; AP = {a.average_precision:.3f}; Recall@2 = {a.recall_at_two:.3f}", 12, BLUE, 600),
        text(x + 40, 628, f"augmented views: nominal {a.nominal_views}, effective {a.effective_views:.3f}", 12),
        text(x + 40, 656, "invariance is valid only relative to a declared task", 12, RED, 500),
        text(x + 24, 714, "Same encoder; different task/head/protocol -> different estimand.", 11, MUTED),
    ))

    # Track B
    x = panel_xs[1]
    parts.extend((
        text(x + 24, 177, "B | candidate law and batch", 21, INK, 650),
        text(x + 24, 202, "exact binary InfoNCE + finite softmax gradient", 13, MUTED, 500),
        box(x + 24, 228, 402, 92, AMBER, "#FFF9EF"),
        text(x + 40, 257, f"q(match)={b.match_probability:.2f}; K={b.candidates}; true MI={b.true_mutual_information:.4f}", 13, AMBER, 650),
        text(x + 40, 285, f"Bayes loss={b.bayes_loss:.4f}; bound={b.infonce_bound:.4f}", 13),
        text(x + 40, 307, f"unclosed MI gap={b.bound_gap:.4f}", 12, RED, 500),
        text(x + 24, 353, "one anchor: raw similarities -> softmax probabilities", 13, INK, 600),
    ))
    for index, (logit, probability, gradient) in enumerate(zip(b.logits, b.probabilities, b.similarity_gradients)):
        y = 382 + index * 66
        role = "positive" if index == 0 else f"negative {index}"
        parts.extend((
            box(x + 24, y - 22, 402, 52, GRID, "#FAFCFF"),
            text(x + 40, y, role, 12, PURPLE if index == 0 else INK, 600),
            text(x + 150, y, f"u={logit:.3f}", 12),
            text(x + 235, y, f"p={probability:.4f}", 12),
            text(x + 330, y, f"dL/ds={gradient:.4f}", 12, RED if index == 0 else TEAL),
        ))
    parts.extend((
        text(x + 24, 596, f"batch loss={b.batch_loss:.4f}", 13, AMBER, 650),
        text(x + 24, 624, f"latent-class collision with declared negatives={b.collision_probability:.4f}", 12, RED, 500),
        box(x + 24, 650, 402, 47, GRID, "#FAFCFF"),
        text(x + 40, 680, "Changing K/batch changes the objective—not only variance.", 12, MUTED, 500),
        text(x + 24, 714, "A lower contrastive loss is not a task-free quality certificate.", 11, MUTED),
    ))

    # Track C
    x = panel_xs[2]
    parts.extend((
        text(x + 24, 177, "C | non-collapse and targets", 21, INK, 650),
        text(x + 24, 202, "covariance spectrum + VICReg + EMA + Bayes target", 13, MUTED, 500),
        box(x + 24, 228, 402, 104, TEAL, "#F1FBF8"),
        text(x + 40, 257, f"spectrum={c.covariance_eigenvalues}; stable rank={c.stable_rank:.3f}", 13, TEAL, 650),
        text(x + 40, 285, f"participation ratio={c.participation_ratio:.3f}", 13),
        text(x + 40, 309, f"entropy effective rank={c.entropy_effective_rank:.3f}", 12),
        box(x + 24, 352, 402, 82, PURPLE, "#F8F6FF"),
        text(x + 40, 381, f"VICReg variance penalty: spectral={c.spectral_variance_penalty:.3f}", 13, PURPLE, 600),
        text(x + 40, 409, f"constant={c.constant_variance_penalty:.3f}; agreement=0 for both", 12),
        box(x + 24, 454, 402, 90, AMBER, "#FFF9EF"),
        text(x + 40, 483, f"EMA teacher final={c.ema_final:.4f}", 13, AMBER, 650),
        text(x + 40, 511, f"masked Bayes log risk={c.conditional_log_risk:.4f}", 12),
        text(x + 40, 533, f"masked Bayes square risk={c.conditional_square_risk:.4f}", 12),
        box(x + 24, 566, 402, 118, GRID, "#FAFCFF"),
        text(x + 40, 596, "high-rank nuisance representation", 13, RED, 650),
        text(x + 40, 624, f"downstream 0-1 risk={c.nuisance_downstream_risk:.3f}", 12),
        text(x + 40, 652, "non-collapse != task sufficiency != transfer", 12, RED, 500),
        text(x + 24, 714, "Stop-gradient and EMA define optimization, not semantic truth.", 11, MUTED),
    ))

    # Joint audit footer
    parts.extend((
        box(70, 760, 1400, 177, GRID, PAPER, 16),
        text(94, 803, "The seven-layer representation audit", 20, INK, 650),
        text(94, 840, "source unit", 13, BLUE, 650),
        text(245, 840, "->", 18, MUTED, 600),
        text(285, 840, "view / target law", 13, AMBER, 650),
        text(480, 840, "->", 18, MUTED, 600),
        text(520, 840, "encoder + head", 13, PURPLE, 650),
        text(700, 840, "->", 18, MUTED, 600),
        text(740, 840, "selection", 13, RED, 650),
        text(860, 840, "->", 18, MUTED, 600),
        text(900, 840, "downstream protocol", 13, TEAL, 650),
        text(1110, 840, "->", 18, MUTED, 600),
        text(1150, 840, "deployment task/shift", 13, INK, 650),
        line(94, 872, 1445, 872),
        text(94, 911, "Evidence rule: low pretext loss != semantic recovery; non-collapse != usefulness; best probe score != unbiased deployment risk.", 13, RED, 500),
        text(1235, 979, "REPR-CUM-01 | deterministic finite fixtures", 11, MUTED, 500),
        "</svg>",
    ))
    return "\n".join(parts) + "\n"


def print_summary(output: Path, a: RepresentationSummary, b: ContrastiveSummary, c: TargetSummary) -> None:
    risks = ",".join(f"{name}:{risk:.6f}" for name, risk in zip(REPRESENTATIONS, a.weighted_risks))
    probabilities = ",".join(f"{value:.6f}" for value in b.probabilities)
    gradients = ",".join(f"{value:.6f}" for value in b.similarity_gradients)
    print(
        "TRACK A "
        f"weights={','.join(f'{value:g}' for value in a.task_weights)} risks={risks} "
        f"best={a.best_representation} triplet={a.triplet_loss:.6f} ap={a.average_precision:.6f} "
        f"recall2={a.recall_at_two:.6f} nominal_views={a.nominal_views} effective_views={a.effective_views:.6f}"
    )
    print(
        "TRACK B "
        f"q={b.match_probability:.6f} K={b.candidates} mi={b.true_mutual_information:.6f} "
        f"bayes_loss={b.bayes_loss:.6f} bound={b.infonce_bound:.6f} gap={b.bound_gap:.6f} "
        f"batch_loss={b.batch_loss:.6f} probs={probabilities} gradients={gradients} "
        f"collision={b.collision_probability:.6f}"
    )
    print(
        "TRACK C "
        f"spectrum={','.join(f'{value:g}' for value in c.covariance_eigenvalues)} "
        f"stable_rank={c.stable_rank:.6f} pr={c.participation_ratio:.6f} effective_rank={c.entropy_effective_rank:.6f} "
        f"vicreg_spectral={c.spectral_variance_penalty:.6f} vicreg_constant={c.constant_variance_penalty:.6f} "
        f"ema_final={c.ema_final:.6f} log_risk={c.conditional_log_risk:.6f} "
        f"square_risk={c.conditional_square_risk:.6f} nuisance_risk={c.nuisance_downstream_risk:.6f}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    weights, similarities, prior, sequence = validate(args)
    canonical = is_canonical(args, weights, similarities, prior, sequence)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")
    a = representation_summary(
        weights, args.positive_distance, args.negative_distance, args.triplet_margin,
        args.source_units, args.views_per_source, args.view_correlation,
    )
    b = contrastive_summary(
        args.match_probability, args.candidates, similarities, args.temperature,
        prior, args.negatives,
    )
    c = target_summary(args.match_probability, args.ema_decay, args.teacher_start, sequence)
    if b.infonce_bound > b.true_mutual_information + 1e-12:
        raise AssertionError("InfoNCE lower bound exceeded true mutual information")
    if c.constant_variance_penalty <= c.spectral_variance_penalty:
        raise AssertionError("canonical non-collapse penalty ordering failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(a, b, c), encoding="utf-8")
    print_summary(output, a, b, c)


if __name__ == "__main__":
    main()
