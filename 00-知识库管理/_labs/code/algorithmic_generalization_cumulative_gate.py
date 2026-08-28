#!/usr/bin/env python3
"""Deterministic three-track evidence gate for ALG-CUM-01.

Track A computes exact replace-one stability and expected generalization for a
Bernoulli sample-mean learner, then records the standard RERM and synchronous-
coupling SGD certificates. Track B evaluates an exact sample-compression bound
and a finite two-hypothesis PAC-Bayes-kl certificate. Track C computes the
mutual information of a binary randomized channel and the resulting expected
generalization radius. No Monte Carlo or third-party package is used.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CANONICAL_OUTPUT = (
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-algorithmic-generalization-cumulative-gate-v2.svg"
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

DEFAULT_STEPS = "0.2,0.15,0.1,0.05"
DEFAULT_PRIOR = "0.7,0.3"
DEFAULT_POSTERIOR = "0.9,0.1"
DEFAULT_EMPIRICAL_RISKS = "0.02,0.25"


@dataclass(frozen=True)
class StabilitySummary:
    sample_size: int
    bernoulli_p: float
    exact_beta: float
    expected_gap: float
    rerm_beta: float
    sgd_beta: float
    step_sum: float


@dataclass(frozen=True)
class DescriptionSummary:
    sample_size: int
    compression_k: int
    message_bits: int
    compression_bound: float
    empirical_gibbs_risk: float
    posterior_kl: float
    pac_kl_budget: float
    inverse_kl_bound: float
    pinsker_bound: float
    joint_inverse_kl_bound: float


@dataclass(frozen=True)
class InformationSummary:
    sample_size: int
    channel_accuracy: float
    exact_mi: float
    bit_budget: float
    exact_radius: float
    bit_radius: float
    route_count: int
    route_log_cost: float
    joint_delta: float


def parse_float_csv(raw: str, label: str) -> tuple[float, ...]:
    try:
        values = tuple(float(piece.strip()) for piece in raw.split(",") if piece.strip())
    except ValueError as exc:
        raise SystemExit(f"{label} must be a comma-separated numeric list") from exc
    if not values or any(not math.isfinite(value) for value in values):
        raise SystemExit(f"{label} must contain finite values")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stability-size", type=int, default=20)
    parser.add_argument("--bernoulli-p", type=float, default=0.5)
    parser.add_argument("--lipschitz", type=float, default=1.0)
    parser.add_argument("--regularization", type=float, default=2.0)
    parser.add_argument("--step-sizes", default=DEFAULT_STEPS)
    parser.add_argument("--certificate-size", type=int, default=200)
    parser.add_argument("--compression-k", type=int, default=5)
    parser.add_argument("--message-bits", type=int, default=3)
    parser.add_argument("--delta", type=float, default=0.05)
    parser.add_argument("--prior", default=DEFAULT_PRIOR)
    parser.add_argument("--posterior", default=DEFAULT_POSTERIOR)
    parser.add_argument("--empirical-risks", default=DEFAULT_EMPIRICAL_RISKS)
    parser.add_argument("--information-size", type=int, default=200)
    parser.add_argument("--channel-accuracy", type=float, default=0.8)
    parser.add_argument("--route-count", type=int, default=5)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def validate(
    args: argparse.Namespace,
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    steps = parse_float_csv(args.step_sizes, "step-sizes")
    prior = parse_float_csv(args.prior, "prior")
    posterior = parse_float_csv(args.posterior, "posterior")
    empirical_risks = parse_float_csv(args.empirical_risks, "empirical-risks")
    if args.stability_size < 2:
        raise SystemExit("stability-size must be at least 2")
    if args.certificate_size < 2 or args.information_size < 1:
        raise SystemExit("certificate-size must be at least 2 and information-size positive")
    if not (0 <= args.bernoulli_p <= 1):
        raise SystemExit("bernoulli-p must lie in [0,1]")
    if args.lipschitz <= 0 or args.regularization <= 0:
        raise SystemExit("lipschitz and regularization must be positive")
    if any(step <= 0 for step in steps):
        raise SystemExit("step-sizes must be positive")
    if not (0 <= args.compression_k < args.certificate_size):
        raise SystemExit("compression-k must satisfy 0 <= k < certificate-size")
    if args.message_bits < 0:
        raise SystemExit("message-bits must be nonnegative")
    if not (0 < args.delta < 1):
        raise SystemExit("delta must lie in (0,1)")
    if not (0.5 <= args.channel_accuracy <= 1):
        raise SystemExit("channel-accuracy must lie in [0.5,1]")
    if args.route_count < 1:
        raise SystemExit("route-count must be positive")
    if not (len(prior) == len(posterior) == len(empirical_risks)):
        raise SystemExit("prior, posterior and empirical-risks must have equal lengths")
    if len(prior) < 2:
        raise SystemExit("PAC-Bayes fixture requires at least two hypotheses")
    if any(value < 0 for value in prior + posterior):
        raise SystemExit("prior and posterior masses must be nonnegative")
    if not math.isclose(sum(prior), 1.0, rel_tol=0, abs_tol=1e-12):
        raise SystemExit("prior masses must sum to one")
    if not math.isclose(sum(posterior), 1.0, rel_tol=0, abs_tol=1e-12):
        raise SystemExit("posterior masses must sum to one")
    if any(not 0 <= risk <= 1 for risk in empirical_risks):
        raise SystemExit("empirical-risks must lie in [0,1]")
    if any(q > 0 and p == 0 for p, q in zip(prior, posterior)):
        raise SystemExit("posterior must be absolutely continuous with respect to prior")
    return steps, prior, posterior, empirical_risks


def is_canonical(args: argparse.Namespace) -> bool:
    return (
        args.stability_size == 20
        and args.bernoulli_p == 0.5
        and args.lipschitz == 1.0
        and args.regularization == 2.0
        and args.step_sizes == DEFAULT_STEPS
        and args.certificate_size == 200
        and args.compression_k == 5
        and args.message_bits == 3
        and args.delta == 0.05
        and args.prior == DEFAULT_PRIOR
        and args.posterior == DEFAULT_POSTERIOR
        and args.empirical_risks == DEFAULT_EMPIRICAL_RISKS
        and args.information_size == 200
        and args.channel_accuracy == 0.8
        and args.route_count == 5
    )


def binomial_probability(size: int, successes: int, probability: float) -> float:
    return math.comb(size, successes) * probability**successes * (1 - probability) ** (size - successes)


def squared_population_risk(weight: float, probability: float) -> float:
    return probability * (1 - weight) ** 2 + (1 - probability) * weight**2


def squared_empirical_risk(weight: float, successes: int, size: int) -> float:
    frequency = successes / size
    return frequency * (1 - weight) ** 2 + (1 - frequency) * weight**2


def stability_summary(
    sample_size: int,
    probability: float,
    lipschitz: float,
    regularization: float,
    steps: tuple[float, ...],
) -> StabilitySummary:
    exact_beta = 0.0
    for successes in range(sample_size):
        left = successes / sample_size
        right = (successes + 1) / sample_size
        for test_value in (0.0, 1.0):
            difference = abs((left - test_value) ** 2 - (right - test_value) ** 2)
            exact_beta = max(exact_beta, difference)

    expected_gap = 0.0
    for successes in range(sample_size + 1):
        weight = successes / sample_size
        gap = squared_population_risk(weight, probability) - squared_empirical_risk(
            weight, successes, sample_size
        )
        expected_gap += binomial_probability(sample_size, successes, probability) * gap

    rerm_beta = 2 * lipschitz**2 / (regularization * sample_size)
    step_sum = sum(steps)
    sgd_beta = 2 * lipschitz**2 * step_sum / sample_size
    return StabilitySummary(
        sample_size, probability, exact_beta, expected_gap, rerm_beta, sgd_beta, step_sum
    )


def bernoulli_kl(left: float, right: float) -> float:
    if not 0 <= left <= 1 or not 0 < right < 1:
        raise ValueError("Bernoulli KL requires left in [0,1] and right in (0,1)")
    if left == 0:
        return -math.log(1 - right)
    if left == 1:
        return -math.log(right)
    return left * math.log(left / right) + (1 - left) * math.log((1 - left) / (1 - right))


def inverse_bernoulli_kl_upper(empirical: float, budget: float) -> float:
    if empirical == 1:
        return 1.0
    low = empirical
    high = 1 - 1e-15
    for _ in range(120):
        midpoint = (low + high) / 2
        if bernoulli_kl(empirical, midpoint) <= budget:
            low = midpoint
        else:
            high = midpoint
    return low


def description_summary(
    sample_size: int,
    compression_k: int,
    message_bits: int,
    delta: float,
    prior: tuple[float, ...],
    posterior: tuple[float, ...],
    empirical_risks: tuple[float, ...],
    route_count: int,
) -> DescriptionSummary:
    compression_bound = (
        math.log(math.comb(sample_size, compression_k))
        + message_bits * math.log(2)
        + math.log(1 / delta)
    ) / (sample_size - compression_k)
    empirical_gibbs_risk = sum(q * risk for q, risk in zip(posterior, empirical_risks))
    posterior_kl = sum(q * math.log(q / p) for p, q in zip(prior, posterior) if q > 0)
    pac_kl_budget = (posterior_kl + math.log((sample_size + 1) / delta)) / sample_size
    inverse_kl_bound = inverse_bernoulli_kl_upper(empirical_gibbs_risk, pac_kl_budget)
    pinsker_bound = min(1.0, empirical_gibbs_risk + math.sqrt(pac_kl_budget / 2))
    joint_budget = (
        posterior_kl + math.log((sample_size + 1) * route_count / delta)
    ) / sample_size
    joint_inverse = inverse_bernoulli_kl_upper(empirical_gibbs_risk, joint_budget)
    return DescriptionSummary(
        sample_size,
        compression_k,
        message_bits,
        compression_bound,
        empirical_gibbs_risk,
        posterior_kl,
        pac_kl_budget,
        inverse_kl_bound,
        pinsker_bound,
        joint_inverse,
    )


def binary_entropy(probability: float) -> float:
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * math.log(probability) - (1 - probability) * math.log(1 - probability)


def information_summary(
    sample_size: int, channel_accuracy: float, route_count: int, delta: float
) -> InformationSummary:
    exact_mi = math.log(2) - binary_entropy(channel_accuracy)
    bit_budget = math.log(2)
    exact_radius = math.sqrt(exact_mi / (2 * sample_size))
    bit_radius = math.sqrt(bit_budget / (2 * sample_size))
    return InformationSummary(
        sample_size,
        channel_accuracy,
        exact_mi,
        bit_budget,
        exact_radius,
        bit_radius,
        route_count,
        math.log(route_count),
        delta / route_count,
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(
    x: float,
    y: float,
    value: object,
    size: int = 15,
    color: str = INK,
    weight: int = 500,
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">'
        f"{esc(value)}</text>"
    )


def rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str = PAPER,
    stroke: str = GRID,
    radius: float = 12,
    stroke_width: float = 1.5,
) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
    )


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = GRID,
    width: float = 2,
    dash: str = "",
) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}"{dash_attr}/>'
    )


def bar(
    items: list[str], x: float, baseline: float, width: float, value: float, maximum: float, color: str, label: str
) -> None:
    height = 190 * value / maximum if maximum else 0
    items.append(rect(x, baseline - height, width, height, color, color, 3, 0))
    items.append(text(x + width / 2, baseline - height - 8, f"{value:.4f}", 13, color, 700, "middle"))
    items.append(text(x + width / 2, baseline + 24, label, 13, MUTED, 600, "middle"))


def build_svg(
    stability: StabilitySummary, description: DescriptionSummary, information: InformationSummary
) -> str:
    width, height = 1540, 990
    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG, BG, 0, 0),
        text(70, 64, "Algorithm-dependent generalization | three-track evidence gate", 27, INK, 750),
        text(70, 94, "replace-one stability  →  compressed/randomized description  →  information leakage", 16, MUTED, 500),
    ]

    panel_y, panel_h, panel_w, gap = 132, 570, 450, 25
    xs = (70, 70 + panel_w + gap, 70 + 2 * (panel_w + gap))
    titles = (
        "A | one sample changes",
        "B | short / nearby description",
        "C | how much sample information",
    )
    subtitles = (
        "expected guarantee; exact finite audit",
        "high-probability compression + PAC-Bayes-kl",
        "expected signed gap; binary learning channel",
    )
    colors = (BLUE, AMBER, TEAL)
    for x, title, subtitle, color in zip(xs, titles, subtitles, colors):
        items.append(rect(x, panel_y, panel_w, panel_h, PAPER, GRID, 16, 1.5))
        items.append(rect(x, panel_y, panel_w, 7, color, color, 4, 0))
        items.append(text(x + 24, panel_y + 48, title, 20, INK, 740))
        items.append(text(x + 24, panel_y + 73, subtitle, 13, MUTED, 500))

    # Track A bars.
    ax = xs[0]
    base = panel_y + 335
    items.append(text(ax + 24, panel_y + 114, f"Bernoulli mean learner: m={stability.sample_size}, p={stability.bernoulli_p:g}", 14, INK, 650))
    items.append(text(ax + 24, panel_y + 140, "loss=(w-z)²; all adjacent counts + z∈{0,1}", 13, MUTED, 500))
    items.append(line(ax + 28, base, ax + panel_w - 24, base, GRID, 1.5))
    values_a = (
        (stability.exact_beta, RED, "exact β"),
        (stability.expected_gap, BLUE, "E gen"),
        (stability.rerm_beta, PURPLE, "RERM"),
        (stability.sgd_beta, TEAL, "SGD"),
    )
    max_a = max(value for value, _, _ in values_a) * 1.15
    for index, (value, color, label) in enumerate(values_a):
        bar(items, ax + 48 + index * 96, base, 52, value, max_a, color, label)
    items.append(text(ax + 24, panel_y + 400, "interfaces", 13, MUTED, 700))
    items.append(text(ax + 24, panel_y + 426, "RERM: 2L²/(λm)", 14, INK, 600))
    items.append(text(ax + 235, panel_y + 426, f"={stability.rerm_beta:.4f}", 14, PURPLE, 720))
    items.append(text(ax + 24, panel_y + 452, "SGD: 2 L^2 sum(eta_t) / m", 14, INK, 600))
    items.append(text(ax + 235, panel_y + 452, f"={stability.sgd_beta:.4f}", 14, TEAL, 720))
    items.append(text(ax + 24, panel_y + 500, "β controls sensitivity; it need not equal E gen.", 13, RED, 650))
    items.append(text(ax + 24, panel_y + 525, "SGD certificate is convex/smooth synchronous coupling.", 12, MUTED, 500))

    # Track B certificate table and bars.
    bx = xs[1]
    items.append(text(bx + 24, panel_y + 114, f"m={description.sample_size}, δ=0.05", 14, INK, 650))
    rows = (
        ("compression k=5, b=3", description.compression_bound, BLUE),
        ("PAC-Bayes inverse-kl", description.inverse_kl_bound, TEAL),
        ("PAC-Bayes Pinsker", description.pinsker_bound, RED),
        ("δ/5 inverse-kl", description.joint_inverse_kl_bound, PURPLE),
    )
    y = panel_y + 157
    for label, value, color in rows:
        items.append(text(bx + 24, y, label, 13, MUTED, 600))
        items.append(rect(bx + 210, y - 15, 185 * value / 0.22, 17, color, color, 3, 0))
        items.append(text(bx + 425, y, f"{value:.4f}", 13, color, 720, "end"))
        y += 45
    items.append(rect(bx + 24, panel_y + 350, panel_w - 48, 130, "#FFF9EE", "#E8C98E", 10, 1.2))
    items.append(text(bx + 42, panel_y + 380, "PAC-Bayes ledger", 14, AMBER, 740))
    items.append(text(bx + 42, panel_y + 408, f"R̂(Q) = {description.empirical_gibbs_risk:.4f}", 14, INK, 600))
    items.append(text(bx + 220, panel_y + 408, f"KL(Q||P) = {description.posterior_kl:.4f}", 14, INK, 600))
    items.append(text(bx + 42, panel_y + 438, f"kl budget = {description.pac_kl_budget:.4f}", 14, INK, 600))
    items.append(text(bx + 42, panel_y + 466, "P fixed before certificate data; Q may depend on it.", 12, MUTED, 520))
    items.append(text(bx + 24, panel_y + 518, "Object: reconstructed h vs Gibbs predictor are different.", 12, RED, 650))

    # Track C channel diagram and values.
    cx = xs[2]
    items.append(text(cx + 24, panel_y + 114, "X~Bernoulli(1/2)  →  randomized response W", 14, INK, 650))
    items.append(rect(cx + 36, panel_y + 154, 90, 58, "#EEF3FF", BLUE, 12, 1.5))
    items.append(text(cx + 81, panel_y + 190, "sample bit X", 13, BLUE, 700, "middle"))
    items.append(line(cx + 128, panel_y + 183, cx + 298, panel_y + 183, TEAL, 3))
    items.append(text(cx + 213, panel_y + 165, f"correct with q={information.channel_accuracy:g}", 12, TEAL, 650, "middle"))
    items.append(rect(cx + 302, panel_y + 154, 105, 58, "#ECFBF7", TEAL, 12, 1.5))
    items.append(text(cx + 354, panel_y + 190, "output W", 13, TEAL, 700, "middle"))
    items.append(rect(cx + 24, panel_y + 252, panel_w - 48, 174, "#F4FBF9", "#A8D9CE", 10, 1.2))
    items.append(text(cx + 42, panel_y + 285, f"exact I(X;W) = {information.exact_mi:.6f} nats", 15, TEAL, 740))
    items.append(text(cx + 42, panel_y + 319, f"one-bit ceiling = ln 2 = {information.bit_budget:.6f}", 14, INK, 600))
    items.append(text(cx + 42, panel_y + 355, f"exact radius = {information.exact_radius:.6f}", 14, BLUE, 720))
    items.append(text(cx + 42, panel_y + 385, f"bit-budget radius = {information.bit_radius:.6f}", 14, PURPLE, 720))
    items.append(text(cx + 24, panel_y + 468, "The theorem bounds |E gen|, not E|gen| or a tail.", 13, RED, 650))
    items.append(text(cx + 24, panel_y + 500, f"Selecting {information.route_count} certificates: pay ln {information.route_count}={information.route_log_cost:.4f}", 13, INK, 650))
    items.append(text(cx + 24, panel_y + 525, f"A simple union ledger uses δ/{information.route_count}={information.joint_delta:.3f} per route.", 12, MUTED, 500))

    # Cross-track reading contract.
    items.append(rect(70, 732, 1400, 190, PAPER, GRID, 16, 1.5))
    items.append(text(94, 773, "Read across the tracks only after matching the contract", 19, INK, 740))
    columns = (
        ("stability", "algorithm + adjacent samples", "expected / bounded-loss tail"),
        ("compression", "fixed encoder/message/decoder", "high probability; realizable"),
        ("PAC-Bayes", "fixed prior P + data posterior Q", "high probability; Gibbs risk"),
        ("information", "joint law P(S,W)", "expected signed gap"),
    )
    for index, (name, obj, conclusion) in enumerate(columns):
        x = 94 + index * 343
        items.append(text(x, 813, name, 14, colors[index % 3], 740))
        items.append(text(x, 840, obj, 12, INK, 600))
        items.append(text(x, 866, conclusion, 12, MUTED, 500))
    items.append(line(94, 886, 1445, 886, GRID, 1))
    items.append(text(94, 910, "Do not take a post-hoc minimum: align predictor, loss, sample, randomness and confidence event first.", 13, RED, 700))
    items.append(text(1470, 964, "ALG-CUM-01 | deterministic finite/analytic fixture", 12, MUTED, 500, "end"))
    items.append("</svg>")
    return "\n".join(items) + "\n"


def print_summary(
    output: Path,
    stability: StabilitySummary,
    description: DescriptionSummary,
    information: InformationSummary,
) -> None:
    print(
        "TRACK A "
        f"m={stability.sample_size} exact_beta={stability.exact_beta:.6f} "
        f"expected_gap={stability.expected_gap:.6f} rerm_beta={stability.rerm_beta:.6f} "
        f"sgd_beta={stability.sgd_beta:.6f} step_sum={stability.step_sum:.6f}"
    )
    print(
        "TRACK B "
        f"m={description.sample_size} compression={description.compression_bound:.6f} "
        f"empirical_gibbs={description.empirical_gibbs_risk:.6f} posterior_kl={description.posterior_kl:.6f} "
        f"kl_budget={description.pac_kl_budget:.6f} inverse_kl={description.inverse_kl_bound:.6f} "
        f"pinsker={description.pinsker_bound:.6f} joint_inverse_kl={description.joint_inverse_kl_bound:.6f}"
    )
    print(
        "TRACK C "
        f"m={information.sample_size} accuracy={information.channel_accuracy:.6f} "
        f"exact_mi={information.exact_mi:.6f} bit_budget={information.bit_budget:.6f} "
        f"exact_radius={information.exact_radius:.6f} bit_radius={information.bit_radius:.6f} "
        f"routes={information.route_count} joint_delta={information.joint_delta:.6f}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    steps, prior, posterior, empirical_risks = validate(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")

    stability = stability_summary(
        args.stability_size, args.bernoulli_p, args.lipschitz, args.regularization, steps
    )
    description = description_summary(
        args.certificate_size,
        args.compression_k,
        args.message_bits,
        args.delta,
        prior,
        posterior,
        empirical_risks,
        args.route_count,
    )
    information = information_summary(
        args.information_size, args.channel_accuracy, args.route_count, args.delta
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(stability, description, information), encoding="utf-8")
    print_summary(output, stability, description, information)


if __name__ == "__main__":
    main()
