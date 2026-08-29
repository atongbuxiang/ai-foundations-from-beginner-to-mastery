#!/usr/bin/env python3
"""Deterministic three-track evidence gate for ONLINE-CUM-01 (LT-69--76)."""

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
    / "plot-online-boosting-cumulative-gate-v2.svg"
)

CANONICAL = {
    "hedge_losses": "0,1,1;1,0,1;0,1,0;1,1,0",
    "hedge_eta": math.log(2.0),
    "ogd_gradients": "1,-2,1,2,-1",
    "ogd_eta": 0.5,
    "ogd_radius": 1.0,
    "adaptive_actions": "1,2,1,2,2,1",
    "perceptron_examples": "1,0,1;0,1,1;-1,-1,-1",
    "separator": "1,1",
    "boost_margins": "1,1,1,-1;-1,-1,1,1",
    "online_risks": "0.2,0.4,0.1,0.3",
    "comparator_risk": 0.1,
    "delta": 0.05,
    "ucb_counts": "20,10",
    "ucb_means": "0.6,0.5",
    "logging_probabilities": "0.5,0.3,0.2",
    "target_probabilities": "0.2,0.2,0.6",
    "bandit_losses": "0.2,0.6,0.9",
    "chosen_action": 3,
}


@dataclass(frozen=True)
class TrackA:
    horizon: int
    experts: int
    eta: float
    hedge_loss: float
    best_loss: float
    hedge_regret: float
    hedge_bound: float
    final_probabilities: tuple[float, ...]
    ogd_horizon: int
    ogd_eta: float
    ogd_path: tuple[float, ...]
    ogd_loss: float
    comparator_loss: float
    ogd_regret: float
    ogd_bound: float
    adaptive_horizon: int
    adaptive_regret: float


@dataclass(frozen=True)
class TrackB:
    mistakes: int
    final_weight: tuple[float, float]
    radius: float
    margin: float
    mistake_bound: float
    progress: float
    weight_norm: float
    boost_errors: tuple[float, ...]
    boost_alphas: tuple[float, ...]
    boost_normalizers: tuple[float, ...]
    boost_product: float
    training_error: float
    minimum_margin: float


@dataclass(frozen=True)
class TrackC:
    horizon: int
    random_iterate_risk: float
    comparator_risk: float
    online_regret: float
    excess_risk: float
    deviation_radius: float
    ucb_values: tuple[float, ...]
    ucb_choice: int
    ips_vector: tuple[float, ...]
    target_risk: float
    observed_target_estimate: float
    ips_variance: float
    maximum_ratio: float


def fail(message: str) -> None:
    raise ValueError(message)


def floats(raw: str, label: str) -> tuple[float, ...]:
    try:
        values = tuple(float(item.strip()) for item in raw.split(",") if item.strip())
    except ValueError as error:
        raise ValueError(f"{label} must be a comma-separated float list") from error
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
        fail(f"{label} must contain at least one row")
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
    if not math.isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=1e-9):
        fail(f"{label} must sum to one")
    return values


def project(value: float, radius: float) -> float:
    return max(-radius, min(radius, value))


def compute_track_a(args: argparse.Namespace) -> TrackA:
    losses = matrix(args.hedge_losses, "hedge-losses")
    if len(losses[0]) < 2 or any(value < 0.0 or value > 1.0 for row in losses for value in row):
        fail("hedge-losses needs at least two experts and losses in [0,1]")
    if args.hedge_eta <= 0.0 or not math.isfinite(args.hedge_eta):
        fail("hedge-eta must be positive")

    cumulative = [0.0] * len(losses[0])
    hedge_loss = 0.0
    for row in losses:
        weights = [math.exp(-args.hedge_eta * loss) for loss in cumulative]
        total = sum(weights)
        probabilities = [weight / total for weight in weights]
        hedge_loss += sum(probability * loss for probability, loss in zip(probabilities, row))
        cumulative = [old + loss for old, loss in zip(cumulative, row)]
    final_weights = [math.exp(-args.hedge_eta * loss) for loss in cumulative]
    final_total = sum(final_weights)
    final_probabilities = tuple(weight / final_total for weight in final_weights)
    best_loss = min(cumulative)
    hedge_bound = math.log(len(cumulative)) / args.hedge_eta + args.hedge_eta * len(losses) / 8.0

    gradients = floats(args.ogd_gradients, "ogd-gradients")
    if args.ogd_eta <= 0.0 or args.ogd_radius <= 0.0:
        fail("ogd-eta and ogd-radius must be positive")
    decision = 0.0
    path: list[float] = []
    ogd_loss = 0.0
    for gradient in gradients:
        path.append(decision)
        ogd_loss += gradient * decision
        decision = project(decision - args.ogd_eta * gradient, args.ogd_radius)
    gradient_sum = sum(gradients)
    comparator = -args.ogd_radius if gradient_sum > 0.0 else args.ogd_radius if gradient_sum < 0.0 else 0.0
    comparator_loss = comparator * gradient_sum
    ogd_bound = (
        comparator * comparator / (2.0 * args.ogd_eta)
        + args.ogd_eta * sum(gradient * gradient for gradient in gradients) / 2.0
    )

    actions = ints(args.adaptive_actions, "adaptive-actions")
    if any(action not in (1, 2) for action in actions):
        fail("adaptive-actions entries must be 1 or 2")
    counts = (actions.count(1), actions.count(2))
    adaptive_regret = float(len(actions) - min(counts))

    return TrackA(
        horizon=len(losses), experts=len(losses[0]), eta=args.hedge_eta,
        hedge_loss=hedge_loss, best_loss=best_loss, hedge_regret=hedge_loss - best_loss,
        hedge_bound=hedge_bound, final_probabilities=final_probabilities,
        ogd_horizon=len(gradients), ogd_eta=args.ogd_eta, ogd_path=tuple(path),
        ogd_loss=ogd_loss, comparator_loss=comparator_loss,
        ogd_regret=ogd_loss - comparator_loss, ogd_bound=ogd_bound,
        adaptive_horizon=len(actions), adaptive_regret=adaptive_regret,
    )


def compute_track_b(args: argparse.Namespace) -> TrackB:
    examples = matrix(args.perceptron_examples, "perceptron-examples")
    if any(len(row) != 3 or row[2] not in (-1.0, 1.0) for row in examples):
        fail("perceptron-examples rows must be x1,x2,y with y in {-1,1}")
    separator_raw = floats(args.separator, "separator")
    if len(separator_raw) != 2 or math.hypot(*separator_raw) == 0.0:
        fail("separator must be a nonzero two-vector")
    separator_norm = math.hypot(*separator_raw)
    separator = (separator_raw[0] / separator_norm, separator_raw[1] / separator_norm)
    margins = tuple(y * (separator[0] * x1 + separator[1] * x2) for x1, x2, y in examples)
    if min(margins) <= 0.0:
        fail("separator must give every perceptron example positive margin")
    radius = max(math.hypot(x1, x2) for x1, x2, _ in examples)
    margin = min(margins)
    weight = [0.0, 0.0]
    mistakes = 0
    for x1, x2, label in examples:
        if label * (weight[0] * x1 + weight[1] * x2) <= 0.0:
            weight[0] += label * x1
            weight[1] += label * x2
            mistakes += 1
    progress = weight[0] * separator[0] + weight[1] * separator[1]
    weight_norm = math.hypot(*weight)

    boost_rows = matrix(args.boost_margins, "boost-margins")
    if len(boost_rows[0]) < 2 or any(value not in (-1.0, 1.0) for row in boost_rows for value in row):
        fail("boost-margins must be a rectangular matrix of -1/+1 margins")
    distribution = [1.0 / len(boost_rows[0])] * len(boost_rows[0])
    errors: list[float] = []
    alphas: list[float] = []
    normalizers: list[float] = []
    for row in boost_rows:
        error = sum(weight_i for weight_i, signed_margin in zip(distribution, row) if signed_margin < 0.0)
        if not 0.0 < error < 0.5:
            fail("every boosting round must have weighted error strictly between 0 and 1/2")
        alpha = 0.5 * math.log((1.0 - error) / error)
        normalizer = 2.0 * math.sqrt(error * (1.0 - error))
        distribution = [
            weight_i * math.exp(-alpha * signed_margin) / normalizer
            for weight_i, signed_margin in zip(distribution, row)
        ]
        errors.append(error)
        alphas.append(alpha)
        normalizers.append(normalizer)
    ensemble_margins = tuple(
        sum(alphas[round_index] * boost_rows[round_index][sample_index] for round_index in range(len(boost_rows)))
        for sample_index in range(len(boost_rows[0]))
    )
    training_error = sum(value <= 0.0 for value in ensemble_margins) / len(ensemble_margins)

    return TrackB(
        mistakes=mistakes, final_weight=(weight[0], weight[1]), radius=radius, margin=margin,
        mistake_bound=(radius / margin) ** 2, progress=progress, weight_norm=weight_norm,
        boost_errors=tuple(errors), boost_alphas=tuple(alphas),
        boost_normalizers=tuple(normalizers), boost_product=math.prod(normalizers),
        training_error=training_error, minimum_margin=min(ensemble_margins),
    )


def compute_track_c(args: argparse.Namespace) -> TrackC:
    risks = floats(args.online_risks, "online-risks")
    if any(value < 0.0 or value > 1.0 for value in risks):
        fail("online-risks entries must lie in [0,1]")
    if not 0.0 <= args.comparator_risk <= 1.0:
        fail("comparator-risk must lie in [0,1]")
    if not 0.0 < args.delta < 1.0:
        fail("delta must lie strictly between zero and one")
    random_iterate_risk = sum(risks) / len(risks)
    online_regret = sum(value - args.comparator_risk for value in risks)
    deviation_radius = math.sqrt(math.log(1.0 / args.delta) / (2.0 * len(risks)))

    counts = ints(args.ucb_counts, "ucb-counts")
    means = floats(args.ucb_means, "ucb-means")
    if len(counts) != len(means) or len(counts) < 2 or any(count <= 0 for count in counts):
        fail("ucb-counts and ucb-means need the same length >=2 and positive counts")
    if any(mean < 0.0 or mean > 1.0 for mean in means):
        fail("ucb-means entries must lie in [0,1]")
    time = sum(counts)
    ucb_values = tuple(mean + math.sqrt(2.0 * math.log(time) / count) for mean, count in zip(means, counts))
    ucb_choice = max(range(len(ucb_values)), key=lambda index: ucb_values[index]) + 1

    logging = probability_vector(args.logging_probabilities, "logging-probabilities", positive=True)
    target = probability_vector(args.target_probabilities, "target-probabilities")
    losses = floats(args.bandit_losses, "bandit-losses")
    if len(logging) != len(target) or len(logging) != len(losses):
        fail("logging, target and bandit loss vectors must have equal length")
    if any(loss < 0.0 or loss > 1.0 for loss in losses):
        fail("bandit-losses entries must lie in [0,1]")
    if not 1 <= args.chosen_action <= len(logging):
        fail("chosen-action is outside the action set")
    chosen = args.chosen_action - 1
    ips_vector = tuple(losses[index] / logging[index] if index == chosen else 0.0 for index in range(len(logging)))
    target_risk = sum(probability * loss for probability, loss in zip(target, losses))
    observed_target_estimate = target[chosen] * losses[chosen] / logging[chosen]
    second_moment = sum(
        target_probability ** 2 * loss ** 2 / logging_probability
        for target_probability, loss, logging_probability in zip(target, losses, logging)
    )
    maximum_ratio = max(target_probability / logging_probability for target_probability, logging_probability in zip(target, logging))

    return TrackC(
        horizon=len(risks), random_iterate_risk=random_iterate_risk,
        comparator_risk=args.comparator_risk, online_regret=online_regret,
        excess_risk=random_iterate_risk - args.comparator_risk,
        deviation_radius=deviation_radius, ucb_values=ucb_values, ucb_choice=ucb_choice,
        ips_vector=ips_vector, target_risk=target_risk,
        observed_target_estimate=observed_target_estimate,
        ips_variance=second_moment - target_risk ** 2, maximum_ratio=maximum_ratio,
    )


def f6(value: float) -> str:
    return f"{value:.6f}"


def csv6(values: tuple[float, ...]) -> str:
    return ",".join(f6(value) for value in values)


def stdout_lines(a: TrackA, b: TrackB, c: TrackC) -> tuple[str, str, str]:
    return (
        f"TRACK A T={a.horizon} eta={f6(a.eta)} hedge_loss={f6(a.hedge_loss)} "
        f"best={f6(a.best_loss)} regret={f6(a.hedge_regret)} bound={f6(a.hedge_bound)} "
        f"final_probs={csv6(a.final_probabilities)} ogd_T={a.ogd_horizon} ogd_eta={f6(a.ogd_eta)} "
        f"ogd_loss={f6(a.ogd_loss)} comparator={f6(a.comparator_loss)} ogd_regret={f6(a.ogd_regret)} "
        f"ogd_bound={f6(a.ogd_bound)} adaptive_T={a.adaptive_horizon} adaptive_regret={f6(a.adaptive_regret)}",
        f"TRACK B mistakes={b.mistakes} final_w={csv6(b.final_weight)} R={f6(b.radius)} gamma={f6(b.margin)} "
        f"mistake_bound={f6(b.mistake_bound)} progress={f6(b.progress)} norm={f6(b.weight_norm)} "
        f"boost_errors={csv6(b.boost_errors)} alphas={csv6(b.boost_alphas)} Z={csv6(b.boost_normalizers)} "
        f"product={f6(b.boost_product)} training_error={f6(b.training_error)} min_margin={f6(b.minimum_margin)}",
        f"TRACK C T={c.horizon} random_risk={f6(c.random_iterate_risk)} comparator={f6(c.comparator_risk)} "
        f"online_regret={f6(c.online_regret)} excess={f6(c.excess_risk)} radius={f6(c.deviation_radius)} "
        f"ucb={csv6(c.ucb_values)} ucb_choice={c.ucb_choice} ips={csv6(c.ips_vector)} "
        f"target_risk={f6(c.target_risk)} observed_estimate={f6(c.observed_target_estimate)} "
        f"ips_variance={f6(c.ips_variance)} max_ratio={f6(c.maximum_ratio)}",
    )


INK = "#172033"
MUTED = "#5F6B7A"
GRID = "#D9E1EA"
BG = "#F7F9FC"
WHITE = "#FFFFFF"
BLUE = "#2563EB"
TEAL = "#0F8B8D"
AMBER = "#D97706"
RED = "#C2413B"
PURPLE = "#7656C9"
GREEN = "#238B57"


def text(x: float, y: float, value: str, size: int = 14, color: str = INK, weight: int = 500,
         anchor: str = "start", css_class: str = "") -> str:
    cls = f' class="{css_class}"' if css_class else ""
    return (
        f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{color}" font-weight="{weight}" '
        f'text-anchor="{anchor}"{cls}>{html.escape(value)}</text>'
    )


def rect(x: float, y: float, width: float, height: float, fill: str = WHITE, stroke: str = GRID,
         radius: float = 14, stroke_width: float = 1.5) -> str:
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" rx="{radius:g}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:g}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 2,
         dash: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="{width:g}"{d}/>'


def circle(cx: float, cy: float, radius: float, fill: str, stroke: str = WHITE, width: float = 2) -> str:
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{radius:g}" fill="{fill}" stroke="{stroke}" stroke-width="{width:g}"/>'


def bar(parts: list[str], x: float, y: float, width: float, value: float, maximum: float, color: str,
        label: str, shown: str) -> None:
    parts.append(text(x, y - 8, label, 12, MUTED, 600))
    parts.append(rect(x, y, width, 13, "#EEF2F7", "#EEF2F7", 6, 0))
    parts.append(rect(x, y, width * max(0.0, min(1.0, value / maximum)), 13, color, color, 6, 0))
    parts.append(text(x + width + 8, y + 11, shown, 12, color, 700))


def render_svg(a: TrackA, b: TrackB, c: TrackC) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1040" viewBox="0 0 1500 1040">',
        '<style>text{font-family:Inter,"Noto Sans SC","PingFang SC",Arial,sans-serif}.math{font-family:"STIX Two Math","Times New Roman",serif}</style>',
        rect(0, 0, 1500, 1040, BG, BG, 0, 0),
        text(55, 60, "20.9 cumulative evidence gate", 28, INK, 760),
        text(55, 90, "protocol and regret  ·  margin and boosting  ·  risk bridge and partial feedback", 15, MUTED, 550),
    ]
    panel_y, panel_h, panel_w = 125, 650, 440
    xs = (45, 530, 1015)
    for x in xs:
        parts.append(rect(x, panel_y, panel_w, panel_h, WHITE, GRID, 18, 1.5))

    # Track A
    ax = xs[0]
    parts += [
        text(ax + 24, 164, "A  |  full-information sequence", 18, BLUE, 750),
        text(ax + 24, 192, "Hedge potential → OGD geometry → visibility", 13, MUTED, 550),
        text(ax + 24, 230, f"Hedge: T={a.horizon}, N={a.experts}, eta={a.eta:.3f}", 14, INK, 650),
    ]
    for index, probability in enumerate(a.final_probabilities):
        y = 258 + index * 29
        parts += [text(ax + 24, y + 11, f"expert {index + 1}", 12, MUTED, 600),
                  rect(ax + 96, y, 238, 13, "#EEF2F7", "#EEF2F7", 6, 0),
                  rect(ax + 96, y, 238 * probability, 13, BLUE, BLUE, 6, 0),
                  text(ax + 344, y + 11, f"p={probability:.3f}", 12, BLUE, 700)]
    bar(parts, ax + 24, 363, 215, a.hedge_regret, a.hedge_bound, BLUE, "realized external regret", f"{a.hedge_regret:.3f}")
    parts += [text(ax + 322, 376, f"≤ {a.hedge_bound:.3f}", 12, MUTED, 650), line(ax + 24, 407, ax + 416, 407)]
    parts += [text(ax + 24, 438, "Projected OGD on [-R,R]", 14, INK, 700),
              text(ax + 24, 462, "decision before each gradient", 12, MUTED, 550)]
    x0, y0, span = ax + 36, 505, 350
    parts.append(line(x0, y0, x0 + span, y0, GRID, 3))
    for index, decision in enumerate(a.ogd_path):
        px = x0 + index * span / max(1, len(a.ogd_path) - 1)
        py = y0 - 55 * decision
        parts += [line(px, y0 - 58, px, y0 + 58, "#EEF2F7", 1), circle(px, py, 6, TEAL),
                  text(px, y0 + 80, f"t{index + 1}", 11, MUTED, 600, "middle")]
    bar(parts, ax + 24, 617, 215, a.ogd_regret, a.ogd_bound, TEAL, "OGD regret / comparator", f"{a.ogd_regret:.3f}")
    parts += [text(ax + 322, 630, f"≤ {a.ogd_bound:.3f}", 12, MUTED, 650),
              rect(ax + 24, 666, 392, 72, "#FFF5F2", "#F2C7C0", 12, 1.2),
              text(ax + 40, 692, "current-action-aware adversary", 13, RED, 700),
              text(ax + 40, 716, f"T={a.adaptive_horizon}: linear regret = {a.adaptive_regret:.1f}", 13, RED, 650)]

    # Track B
    bx = xs[1]
    parts += [
        text(bx + 24, 164, "B  |  margin to exponential potential", 18, PURPLE, 750),
        text(bx + 24, 192, "Perceptron double ledger → AdaBoost product", 13, MUTED, 550),
        text(bx + 24, 230, f"Perceptron mistakes M = {b.mistakes}", 14, INK, 700),
        rect(bx + 24, 254, 392, 126, "#F7F4FF", "#D9CEF5", 12, 1.2),
        text(bx + 42, 282, "progress", 12, MUTED, 650),
        text(bx + 42, 311, f"<w,u> = {b.progress:.3f}  >=  M gamma", 15, PURPLE, 700, css_class="math"),
        text(bx + 42, 342, "norm growth", 12, MUTED, 650),
        text(bx + 42, 369, f"||w|| = {b.weight_norm:.3f}  <=  R sqrt(M)", 15, PURPLE, 700, css_class="math"),
        text(bx + 24, 416, f"certificate: M={b.mistakes} <= (R/gamma)^2={b.mistake_bound:.3f}", 14, PURPLE, 700),
        line(bx + 24, 443, bx + 416, 443),
        text(bx + 24, 476, "AdaBoost exact two-ledger identity", 14, INK, 700),
    ]
    for index, (error, alpha, normalizer) in enumerate(zip(b.boost_errors, b.boost_alphas, b.boost_normalizers)):
        y = 509 + index * 54
        parts += [circle(bx + 42, y - 5, 15, AMBER), text(bx + 42, y, str(index + 1), 12, WHITE, 750, "middle"),
                  text(bx + 68, y - 7, f"epsilon={error:.3f}   alpha={alpha:.3f}", 13, INK, 650),
                  text(bx + 68, y + 15, f"Z={normalizer:.3f}", 12, MUTED, 650)]
    parts += [
        rect(bx + 24, 632, 392, 106, "#FFF9EC", "#F0D49A", 12, 1.2),
        text(bx + 42, 660, f"product Z_t = {b.boost_product:.6f}", 14, AMBER, 750, css_class="math"),
        text(bx + 42, 687, f"training error = {b.training_error:.3f}", 13, INK, 650),
        text(bx + 42, 714, f"minimum ensemble margin = {b.minimum_margin:.3f}", 13, RED, 650),
    ]

    # Track C
    cx = xs[2]
    parts += [
        text(cx + 24, 164, "C  |  risk bridge and partial feedback", 18, GREEN, 750),
        text(cx + 24, 192, "online-to-batch → UCB / IPS → RL boundary", 13, MUTED, 550),
        rect(cx + 24, 222, 392, 135, "#EFFAF4", "#BFE5CF", 12, 1.2),
        text(cx + 42, 252, "past-measurable predictors + fresh iid point", 13, GREEN, 700),
        text(cx + 42, 282, f"random iterate risk = {c.random_iterate_risk:.3f}", 15, INK, 700),
        text(cx + 42, 310, f"regret / T = excess = {c.excess_risk:.3f}", 14, GREEN, 700),
        text(cx + 42, 337, f"illustrative deviation radius = {c.deviation_radius:.3f}", 12, MUTED, 600),
        text(cx + 24, 398, "Stochastic UCB index", 14, INK, 700),
    ]
    max_ucb = max(c.ucb_values) * 1.12
    for index, value in enumerate(c.ucb_values):
        y = 423 + index * 37
        color = GREEN if index + 1 == c.ucb_choice else "#8CA0B3"
        parts += [text(cx + 24, y + 12, f"arm {index + 1}", 12, MUTED, 650),
                  rect(cx + 76, y, 250, 14, "#EEF2F7", "#EEF2F7", 7, 0),
                  rect(cx + 76, y, 250 * value / max_ucb, 14, color, color, 7, 0),
                  text(cx + 337, y + 12, f"{value:.3f}", 12, color, 750)]
    parts += [
        text(cx + 24, 524, f"choose arm {c.ucb_choice}", 13, GREEN, 750),
        line(cx + 24, 549, cx + 416, 549),
        text(cx + 24, 580, "Bandit IPS: unbiased, potentially explosive", 14, INK, 700),
        text(cx + 24, 608, f"one observed target estimate = {c.observed_target_estimate:.3f}", 13, RED, 650),
        text(cx + 24, 634, f"true target risk = {c.target_risk:.3f}", 13, GREEN, 700),
        text(cx + 24, 660, f"variance = {c.ips_variance:.3f}   max ratio = {c.maximum_ratio:.1f}", 13, MUTED, 650),
        rect(cx + 24, 686, 392, 52, "#FFF5F2", "#F2C7C0", 12, 1.2),
        text(cx + 42, 718, "bandit != RL: actions do not yet alter future states", 12, RED, 700),
    ]

    # Footer ledger and boundaries
    parts += [
        rect(45, 805, 1410, 172, WHITE, GRID, 18, 1.5),
        text(70, 840, "eight-layer sequential audit", 17, INK, 760),
    ]
    ledger = [
        ("1 protocol", "move order"), ("2 filtration", "who sees fresh coin"),
        ("3 feedback", "full / bandit"), ("4 comparator", "fixed / policy"),
        ("5 potential", "log-W / distance"), ("6 probability", "path / expectation"),
        ("7 conversion", "regret -> risk"), ("8 boundary", "deployment / RL"),
    ]
    for index, (title, subtitle) in enumerate(ledger):
        x = 70 + index * 170
        parts += [rect(x, 862, 154, 58, "#F7F9FC", GRID, 10, 1),
                  text(x + 12, 885, title, 12, BLUE if index < 4 else TEAL, 700),
                  text(x + 12, 907, subtitle, 11, MUTED, 550)]
    parts += [
        text(70, 949, "No-regret != iid generalization   ·   small training error != test guarantee   ·   unbiased IPS != safe deployment",
             13, RED, 700),
        text(1430, 1009, "ONLINE-CUM-01 | deterministic finite fixtures", 11, MUTED, 500, "end"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hedge-losses", default=CANONICAL["hedge_losses"])
    parser.add_argument("--hedge-eta", type=float, default=CANONICAL["hedge_eta"])
    parser.add_argument("--ogd-gradients", default=CANONICAL["ogd_gradients"])
    parser.add_argument("--ogd-eta", type=float, default=CANONICAL["ogd_eta"])
    parser.add_argument("--ogd-radius", type=float, default=CANONICAL["ogd_radius"])
    parser.add_argument("--adaptive-actions", default=CANONICAL["adaptive_actions"])
    parser.add_argument("--perceptron-examples", default=CANONICAL["perceptron_examples"])
    parser.add_argument("--separator", default=CANONICAL["separator"])
    parser.add_argument("--boost-margins", default=CANONICAL["boost_margins"])
    parser.add_argument("--online-risks", default=CANONICAL["online_risks"])
    parser.add_argument("--comparator-risk", type=float, default=CANONICAL["comparator_risk"])
    parser.add_argument("--delta", type=float, default=CANONICAL["delta"])
    parser.add_argument("--ucb-counts", default=CANONICAL["ucb_counts"])
    parser.add_argument("--ucb-means", default=CANONICAL["ucb_means"])
    parser.add_argument("--logging-probabilities", default=CANONICAL["logging_probabilities"])
    parser.add_argument("--target-probabilities", default=CANONICAL["target_probabilities"])
    parser.add_argument("--bandit-losses", default=CANONICAL["bandit_losses"])
    parser.add_argument("--chosen-action", type=int, default=CANONICAL["chosen_action"])
    parser.add_argument("--output", type=Path)
    return parser


def is_canonical(args: argparse.Namespace) -> bool:
    return all(getattr(args, key) == value for key, value in CANONICAL.items())


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        canonical = is_canonical(args)
        if args.output is None and not canonical:
            fail("noncanonical parameters require --output")
        output = DEFAULT_SVG if args.output is None else args.output.resolve()
        if not canonical and output == DEFAULT_SVG.resolve():
            fail("noncanonical parameters cannot overwrite the canonical SVG")
        track_a = compute_track_a(args)
        track_b = compute_track_b(args)
        track_c = compute_track_c(args)
        svg = render_svg(track_a, track_b, track_c)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(svg, encoding="utf-8")
        for line_value in stdout_lines(track_a, track_b, track_c):
            print(line_value)
        print(f"SHA256 {hashlib.sha256(svg.encode('utf-8')).hexdigest()}")
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
