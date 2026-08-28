#!/usr/bin/env python3
"""Deterministic cross-volume evidence gate for LT-QUAL-01.

The shared model is realizable threshold learning on a finite ordered domain.
Track A enumerates every training sample and checks Bayes/class/ERM risks,
ghost replacement, direct replace-one stability and the exact output channel.
Track B evaluates finite-class, sample-compression and PAC-Bayes certificates
on a larger balanced certificate sample. Track C audits statement types and
selection budgets. No Monte Carlo or third-party dependency is used.
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
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-learning-theory-qualification-01-gate-v2.svg"
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

DEFAULT_PRIOR = "0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666"
DEFAULT_POSTERIOR = "0.02,0.03,0.1,0.7,0.1,0.05"


@dataclass(frozen=True)
class ExactSummary:
    domain_size: int
    target: int
    sample_size: int
    hypothesis_count: int
    vc_dimension: int
    growth_on_domain: int
    bayes_risk: float
    class_risk: float
    expected_empirical_risk: float
    expected_population_risk: float
    ghost_replacement: float
    direct_stability: float
    output_probabilities: tuple[float, ...]
    output_entropy: float
    information_radius: float


@dataclass(frozen=True)
class CertificateSummary:
    sample_size: int
    empirical_risks: tuple[float, ...]
    empirical_gibbs_risk: float
    true_gibbs_risk: float
    finite_radius: float
    finite_bound: float
    compression_bound: float
    posterior_kl: float
    pac_budget: float
    pac_bound: float
    joint_pac_bound: float
    route_count: int
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
    parser.add_argument("--domain-size", type=int, default=5)
    parser.add_argument("--target-threshold", type=int, default=3)
    parser.add_argument("--enumeration-size", type=int, default=6)
    parser.add_argument("--certificate-size", type=int, default=200)
    parser.add_argument("--delta", type=float, default=0.05)
    parser.add_argument("--prior", default=DEFAULT_PRIOR)
    parser.add_argument("--posterior", default=DEFAULT_POSTERIOR)
    parser.add_argument("--compression-bits", type=int, default=1)
    parser.add_argument("--route-count", type=int, default=5)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def validate(args: argparse.Namespace) -> tuple[tuple[float, ...], tuple[float, ...]]:
    prior = parse_float_csv(args.prior, "prior")
    posterior = parse_float_csv(args.posterior, "posterior")
    if not 2 <= args.domain_size <= 7:
        raise SystemExit("domain-size must lie in 2..7")
    if not 0 <= args.target_threshold <= args.domain_size:
        raise SystemExit("target-threshold must lie in 0..domain-size")
    if args.enumeration_size < 1:
        raise SystemExit("enumeration-size must be positive")
    if args.domain_size**args.enumeration_size > 500_000:
        raise SystemExit("exact enumeration exceeds 500000 samples")
    if args.certificate_size < 2 or args.certificate_size % args.domain_size != 0:
        raise SystemExit("certificate-size must be at least 2 and divisible by domain-size")
    if not 0 < args.delta < 1:
        raise SystemExit("delta must lie in (0,1)")
    if args.compression_bits < 0:
        raise SystemExit("compression-bits must be nonnegative")
    if args.route_count < 1:
        raise SystemExit("route-count must be positive")
    expected_length = args.domain_size + 1
    if len(prior) != expected_length or len(posterior) != expected_length:
        raise SystemExit("prior and posterior must have domain-size + 1 masses")
    if any(value < 0 for value in prior + posterior):
        raise SystemExit("prior and posterior masses must be nonnegative")
    if not math.isclose(sum(prior), 1.0, rel_tol=0, abs_tol=1e-12):
        raise SystemExit("prior masses must sum to one")
    if not math.isclose(sum(posterior), 1.0, rel_tol=0, abs_tol=1e-12):
        raise SystemExit("posterior masses must sum to one")
    if any(q > 0 and p == 0 for p, q in zip(prior, posterior)):
        raise SystemExit("posterior must be absolutely continuous with respect to prior")
    return prior, posterior


def is_canonical(args: argparse.Namespace) -> bool:
    return (
        args.domain_size == 5
        and args.target_threshold == 3
        and args.enumeration_size == 6
        and args.certificate_size == 200
        and args.delta == 0.05
        and args.prior == DEFAULT_PRIOR
        and args.posterior == DEFAULT_POSTERIOR
        and args.compression_bits == 1
        and args.route_count == 5
    )


def prediction(threshold: int, point: int) -> int:
    return int(point >= threshold)


def label(target: int, point: int) -> int:
    return prediction(target, point)


def empirical_errors(
    sample: tuple[int, ...], domain_size: int, target: int
) -> tuple[int, ...]:
    return tuple(
        sum(prediction(threshold, point) != label(target, point) for point in sample)
        for threshold in range(domain_size + 1)
    )


def lexicographic_erm(sample: tuple[int, ...], domain_size: int, target: int) -> int:
    errors = empirical_errors(sample, domain_size, target)
    return min(range(domain_size + 1), key=lambda threshold: (errors[threshold], threshold))


def population_risk(threshold: int, target: int, domain_size: int) -> float:
    return abs(threshold - target) / domain_size


def exact_summary(domain_size: int, target: int, sample_size: int) -> ExactSummary:
    samples = tuple(itertools.product(range(domain_size), repeat=sample_size))
    outputs = {sample: lexicographic_erm(sample, domain_size, target) for sample in samples}
    output_counts = [0] * (domain_size + 1)
    population_total = 0.0
    empirical_total = 0.0
    ghost_total = 0.0
    direct_stability = 0.0

    for sample in samples:
        output = outputs[sample]
        output_counts[output] += 1
        population_total += population_risk(output, target, domain_size)
        empirical_total += empirical_errors(sample, domain_size, target)[output] / sample_size
        for index in range(sample_size):
            for replacement in range(domain_size):
                replaced = list(sample)
                replaced[index] = replacement
                replaced_tuple = tuple(replaced)
                replaced_output = outputs[replaced_tuple]
                original_point = sample[index]
                ghost_total += (
                    int(prediction(replaced_output, original_point) != label(target, original_point))
                    - int(prediction(output, original_point) != label(target, original_point))
                )
                if replaced_output != output:
                    for test_point in range(domain_size):
                        loss_difference = abs(
                            int(prediction(replaced_output, test_point) != label(target, test_point))
                            - int(prediction(output, test_point) != label(target, test_point))
                        )
                        direct_stability = max(direct_stability, float(loss_difference))

    sample_count = len(samples)
    output_probabilities = tuple(count / sample_count for count in output_counts)
    output_entropy = -sum(
        probability * math.log(probability)
        for probability in output_probabilities
        if probability > 0
    )
    expected_population = population_total / sample_count
    expected_empirical = empirical_total / sample_count
    ghost_replacement = ghost_total / (sample_count * sample_size * domain_size)
    information_radius = math.sqrt(output_entropy / (2 * sample_size))
    return ExactSummary(
        domain_size,
        target,
        sample_size,
        domain_size + 1,
        1,
        domain_size + 1,
        0.0,
        0.0,
        expected_empirical,
        expected_population,
        ghost_replacement,
        direct_stability,
        output_probabilities,
        output_entropy,
        information_radius,
    )


def bernoulli_kl(left: float, right: float) -> float:
    if left == 0:
        return -math.log(1 - right)
    if left == 1:
        return -math.log(right)
    return left * math.log(left / right) + (1 - left) * math.log((1 - left) / (1 - right))


def inverse_bernoulli_kl_upper(empirical: float, budget: float) -> float:
    if empirical == 1:
        return 1.0
    low, high = empirical, 1 - 1e-15
    for _ in range(130):
        middle = (low + high) / 2
        if bernoulli_kl(empirical, middle) <= budget:
            low = middle
        else:
            high = middle
    return low


def certificate_summary(
    domain_size: int,
    target: int,
    sample_size: int,
    delta: float,
    prior: tuple[float, ...],
    posterior: tuple[float, ...],
    compression_bits: int,
    route_count: int,
) -> CertificateSummary:
    empirical_risks = tuple(
        population_risk(threshold, target, domain_size)
        for threshold in range(domain_size + 1)
    )
    empirical_gibbs = sum(q * risk for q, risk in zip(posterior, empirical_risks))
    true_gibbs = empirical_gibbs
    hypothesis_count = domain_size + 1
    finite_radius = math.sqrt(math.log(2 * hypothesis_count / delta) / (2 * sample_size))
    finite_bound = empirical_gibbs + finite_radius
    compression_bound = (
        math.log(math.comb(sample_size, 1))
        + compression_bits * math.log(2)
        + math.log(1 / delta)
    ) / (sample_size - 1)
    posterior_kl = sum(q * math.log(q / p) for p, q in zip(prior, posterior) if q > 0)
    pac_budget = (posterior_kl + math.log((sample_size + 1) / delta)) / sample_size
    pac_bound = inverse_bernoulli_kl_upper(empirical_gibbs, pac_budget)
    joint_budget = (
        posterior_kl + math.log((sample_size + 1) * route_count / delta)
    ) / sample_size
    joint_pac_bound = inverse_bernoulli_kl_upper(empirical_gibbs, joint_budget)
    return CertificateSummary(
        sample_size,
        empirical_risks,
        empirical_gibbs,
        true_gibbs,
        finite_radius,
        finite_bound,
        compression_bound,
        posterior_kl,
        pac_budget,
        pac_bound,
        joint_pac_bound,
        route_count,
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


def build_svg(exact: ExactSummary, certificates: CertificateSummary) -> str:
    width, height = 1540, 1010
    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG, BG, 0, 0),
        text(70, 62, "Learning theory qualification I | one model, five proof routes", 27, INK, 750),
        text(70, 93, "risk/object  ->  PAC/VC  ->  data-dependent complexity  ->  algorithm/output-dependent generalization", 16, MUTED, 500),
    ]
    panel_y, panel_h, panel_w, gap = 132, 590, 450, 25
    xs = (70, 545, 1020)
    panel_data = (
        ("A | exact learning process", "all samples, all replacements, no Monte Carlo", BLUE),
        ("B | larger-sample certificates", "same threshold family; predictor identities separated", AMBER),
        ("C | route before number", "validity, statement type, selection budget", TEAL),
    )
    for x, (title, subtitle, color) in zip(xs, panel_data):
        items.append(rect(x, panel_y, panel_w, panel_h, PAPER, GRID, 16, 1.5))
        items.append(rect(x, panel_y, panel_w, 7, color, color, 4, 0))
        items.append(text(x + 24, panel_y + 48, title, 20, INK, 740))
        items.append(text(x + 24, panel_y + 73, subtitle, 13, MUTED, 500))

    # Panel A: exact output channel.
    ax = xs[0]
    items.append(text(ax + 24, panel_y + 112, f"X={{0,...,{exact.domain_size - 1}}}, target threshold={exact.target}", 14, INK, 650))
    items.append(text(ax + 24, panel_y + 137, f"lexicographic consistent ERM, m={exact.sample_size}", 13, MUTED, 500))
    chart_left, chart_top, chart_width, chart_height = ax + 42, panel_y + 180, 370, 205
    items.append(line(chart_left, chart_top + chart_height, chart_left + chart_width, chart_top + chart_height, GRID, 1.5))
    max_probability = max(exact.output_probabilities) or 1
    slot = chart_width / len(exact.output_probabilities)
    for threshold, probability in enumerate(exact.output_probabilities):
        bar_height = chart_height * probability / max_probability
        color = TEAL if threshold == exact.target else BLUE
        items.append(rect(chart_left + threshold * slot + 8, chart_top + chart_height - bar_height, slot - 16, bar_height, color, color, 3, 0))
        items.append(text(chart_left + (threshold + 0.5) * slot, chart_top + chart_height + 22, f"t={threshold}", 12, MUTED, 600, "middle"))
        if probability > 0:
            items.append(text(chart_left + (threshold + 0.5) * slot, chart_top + chart_height - bar_height - 7, f"{probability:.3f}", 11, color, 700, "middle"))
    items.append(text(ax + 24, panel_y + 442, f"E empirical risk = {exact.expected_empirical_risk:.6f}", 14, INK, 600))
    items.append(text(ax + 24, panel_y + 470, f"E population gap = {exact.expected_population_risk:.6f}", 14, BLUE, 730))
    items.append(text(ax + 24, panel_y + 498, f"ghost replacement = {exact.ghost_replacement:.6f}", 14, TEAL, 730))
    items.append(text(ax + 24, panel_y + 526, f"direct stability beta = {exact.direct_stability:.1f}", 14, RED, 730))
    items.append(text(ax + 24, panel_y + 558, "Exact gap = ghost identity; worst-case beta can be vacuous.", 12, RED, 650))

    # Panel B: certificate values.
    bx = xs[1]
    items.append(text(bx + 24, panel_y + 112, f"balanced certificate sample m={certificates.sample_size}", 14, INK, 650))
    rows = (
        ("true Gibbs risk Q", certificates.true_gibbs_risk, TEAL),
        ("finite-class bound Q", certificates.finite_bound, BLUE),
        ("PAC-Bayes-kl Q", certificates.pac_bound, PURPLE),
        ("joint-budget PAC Q", certificates.joint_pac_bound, RED),
        ("compression ERM", certificates.compression_bound, AMBER),
    )
    maximum = max(value for _, value, _ in rows) * 1.12
    y = panel_y + 164
    for label_value, value, color in rows:
        items.append(text(bx + 24, y, label_value, 13, MUTED, 620))
        items.append(rect(bx + 205, y - 15, 165 * value / maximum, 17, color, color, 3, 0))
        items.append(text(bx + 424, y, f"{value:.4f}", 13, color, 730, "end"))
        y += 48
    items.append(rect(bx + 24, panel_y + 420, panel_w - 48, 112, "#FFF9EE", "#E8C98E", 10, 1.2))
    items.append(text(bx + 42, panel_y + 451, "certificate ledger", 14, AMBER, 740))
    items.append(text(bx + 42, panel_y + 480, f"Rhat(Q)={certificates.empirical_gibbs_risk:.4f}   KL(Q||P)={certificates.posterior_kl:.4f}", 13, INK, 600))
    items.append(text(bx + 42, panel_y + 508, f"finite radius={certificates.finite_radius:.4f}   delta/J={certificates.joint_delta:.3f}", 13, INK, 600))
    items.append(text(bx + 24, panel_y + 558, "Compression controls reconstructed ERM, not Gibbs Q.", 12, RED, 650))

    # Panel C: statement route ledger.
    cx = xs[2]
    items.append(text(cx + 24, panel_y + 112, "Five routes on the shared threshold model", 14, INK, 650))
    ledger = (
        ("capacity", "Gibbs Q", "high probability", f"{certificates.finite_bound:.3f}", BLUE),
        ("stability", "small-m ERM", "expected", f"{exact.direct_stability:.1f}", RED),
        ("compression", "large-m ERM", "high probability", f"{certificates.compression_bound:.3f}", AMBER),
        ("PAC-Bayes", "Gibbs Q", "high probability", f"{certificates.pac_bound:.3f}", PURPLE),
        ("information", "small-m ERM", "expected gap", f"{exact.information_radius:.3f}", TEAL),
    )
    y = panel_y + 158
    for route, predictor_name, statement_type, value, color in ledger:
        items.append(rect(cx + 24, y - 20, panel_w - 48, 64, "#F8FAFD", GRID, 8, 1))
        items.append(text(cx + 40, y + 3, route, 14, color, 740))
        items.append(text(cx + 150, y + 3, predictor_name, 12, INK, 620))
        items.append(text(cx + 150, y + 27, statement_type, 11, MUTED, 500))
        items.append(text(cx + 402, y + 15, value, 14, color, 740, "end"))
        y += 78
    items.append(text(cx + 24, panel_y + 558, "Filter by object/event first; compare numbers second.", 12, RED, 680))

    # Bottom cross-volume contract.
    items.append(rect(70, 752, 1400, 188, PAPER, GRID, 16, 1.5))
    items.append(text(94, 792, "The cross-volume proof spine", 19, INK, 740))
    stages = (
        ("object / risk", "D, loss, Bayes, class, algorithm"),
        ("capacity", "|H|, VC=1, growth=d+1"),
        ("data-dependent", "empirical restriction / margin / local"),
        ("algorithm/output", "beta, compression, KL, I(S;W)"),
    )
    for index, (stage, detail) in enumerate(stages):
        x = 94 + index * 340
        items.append(text(x, 833, stage, 14, (BLUE, AMBER, PURPLE, TEAL)[index], 740))
        items.append(text(x, 861, detail, 12, INK, 600))
        if index < 3:
            items.append(text(x + 310, 848, "->", 18, MUTED, 700, "middle"))
    items.append(line(94, 885, 1445, 885, GRID, 1))
    items.append(text(94, 913, "Qualification rule: a valid bound may be vacuous; a small number may be invalid; material pass is not learner pass.", 13, RED, 700))
    items.append(text(1470, 982, "LT-QUAL-01 | deterministic exact-enumeration fixture", 12, MUTED, 500, "end"))
    items.append("</svg>")
    return "\n".join(items) + "\n"


def distribution_text(probabilities: tuple[float, ...]) -> str:
    return ",".join(f"{index}:{probability:.6f}" for index, probability in enumerate(probabilities))


def print_summary(output: Path, exact: ExactSummary, certificates: CertificateSummary) -> None:
    print(
        "TRACK A "
        f"d={exact.domain_size} target={exact.target} enum_m={exact.sample_size} "
        f"hypotheses={exact.hypothesis_count} vc={exact.vc_dimension} growth={exact.growth_on_domain} "
        f"bayes={exact.bayes_risk:.6f} class={exact.class_risk:.6f} "
        f"expected_emp={exact.expected_empirical_risk:.6f} "
        f"expected_pop={exact.expected_population_risk:.6f} "
        f"ghost={exact.ghost_replacement:.6f} stability={exact.direct_stability:.6f}"
    )
    print(
        "TRACK B "
        f"cert_m={certificates.sample_size} gibbs_emp={certificates.empirical_gibbs_risk:.6f} "
        f"gibbs_true={certificates.true_gibbs_risk:.6f} finite={certificates.finite_bound:.6f} "
        f"compression={certificates.compression_bound:.6f} kl={certificates.posterior_kl:.6f} "
        f"pac={certificates.pac_bound:.6f} joint_pac={certificates.joint_pac_bound:.6f}"
    )
    print(
        "TRACK C "
        f"output_entropy={exact.output_entropy:.6f} info_radius={exact.information_radius:.6f} "
        f"output={distribution_text(exact.output_probabilities)} "
        f"routes={certificates.route_count} joint_delta={certificates.joint_delta:.6f}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    prior, posterior = validate(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")

    exact = exact_summary(args.domain_size, args.target_threshold, args.enumeration_size)
    certificates = certificate_summary(
        args.domain_size,
        args.target_threshold,
        args.certificate_size,
        args.delta,
        prior,
        posterior,
        args.compression_bits,
        args.route_count,
    )
    if not math.isclose(
        exact.expected_population_risk,
        exact.ghost_replacement,
        rel_tol=0,
        abs_tol=1e-12,
    ):
        raise AssertionError("ghost replacement identity failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(exact, certificates), encoding="utf-8")
    print_summary(output, exact, certificates)


if __name__ == "__main__":
    main()
