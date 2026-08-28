#!/usr/bin/env python3
"""Deterministic three-track gate for VC dimension and uniform convergence.

Track A enumerates binary patterns.  Track B computes the exact finite-sample
distribution of the empirical-CDF supremum on a discrete uniform domain by a
multinomial dynamic program.  Track C audits SRM penalties and finite witnesses
for multiclass and pseudo-shattering extensions.  No Monte Carlo is used.
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
    / "plot-vc-uniform-convergence-cumulative-gate-v2.svg"
)

DEFAULTS = {
    "max_size": 10,
    "interval_runs": 2,
    "domain_size": 6,
    "uniform_size": 40,
    "delta": 0.05,
    "layer_dims": "1,2,4,8",
    "layer_weights": "0.5,0.25,0.125,0.0625",
    "empirical_risks": "0.26,0.18,0.115,0.09",
    "true_risks": "0.255,0.185,0.13,0.105",
    "srm_size": 3000,
    "multiclass_points": 3,
    "label_count": 4,
}

BG = "#F8FAFC"
PAPER = "#FFFFFF"
INK = "#172033"
MUTED = "#5B667A"
GRID = "#CBD5E1"
BLUE = "#2563EB"
TEAL = "#0F9D8A"
RED = "#C24135"
AMBER = "#B7791F"


@dataclass(frozen=True)
class GrowthSummary:
    m_values: tuple[int, ...]
    threshold_counts: tuple[int, ...]
    one_interval_counts: tuple[int, ...]
    run_counts: tuple[int, ...]
    sauer_counts: tuple[int, ...]
    vc_dimension: int


@dataclass(frozen=True)
class UniformSummary:
    exact_radius: float
    exact_success: float
    dkw_radius: float
    finite_radius: float
    vc_radius_raw: float
    exact_failure_at_finite: float


@dataclass(frozen=True)
class SRMSummary:
    dims: tuple[int, ...]
    weights: tuple[float, ...]
    empirical: tuple[float, ...]
    true: tuple[float, ...]
    penalties: tuple[float, ...]
    scores: tuple[float, ...]
    selected: int
    oracle_bounds: tuple[float, ...]
    oracle_layer: int
    natarajan_patterns: int
    graph_patterns: int
    multiclass_functions: int
    pseudo_patterns: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-size", type=int, default=DEFAULTS["max_size"])
    parser.add_argument("--interval-runs", type=int, default=DEFAULTS["interval_runs"])
    parser.add_argument("--domain-size", type=int, default=DEFAULTS["domain_size"])
    parser.add_argument("--uniform-size", type=int, default=DEFAULTS["uniform_size"])
    parser.add_argument("--delta", type=float, default=DEFAULTS["delta"])
    parser.add_argument("--layer-dims", default=DEFAULTS["layer_dims"])
    parser.add_argument("--layer-weights", default=DEFAULTS["layer_weights"])
    parser.add_argument("--empirical-risks", default=DEFAULTS["empirical_risks"])
    parser.add_argument("--true-risks", default=DEFAULTS["true_risks"])
    parser.add_argument("--srm-size", type=int, default=DEFAULTS["srm_size"])
    parser.add_argument("--multiclass-points", type=int, default=DEFAULTS["multiclass_points"])
    parser.add_argument("--label-count", type=int, default=DEFAULTS["label_count"])
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def parse_int_list(raw: str, name: str) -> tuple[int, ...]:
    try:
        values = tuple(int(item.strip()) for item in raw.split(",") if item.strip())
    except ValueError as exc:
        raise SystemExit(f"invalid {name}: {raw!r}") from exc
    if not values:
        raise SystemExit(f"{name} must not be empty")
    return values


def parse_float_list(raw: str, name: str) -> tuple[float, ...]:
    try:
        values = tuple(float(item.strip()) for item in raw.split(",") if item.strip())
    except ValueError as exc:
        raise SystemExit(f"invalid {name}: {raw!r}") from exc
    if not values:
        raise SystemExit(f"{name} must not be empty")
    return values


def validate(args: argparse.Namespace) -> tuple[tuple[int, ...], tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    dims = parse_int_list(args.layer_dims, "layer dimensions")
    weights = parse_float_list(args.layer_weights, "layer weights")
    empirical = parse_float_list(args.empirical_risks, "empirical risks")
    true = parse_float_list(args.true_risks, "true risks")
    if args.interval_runs < 1 or args.max_size < 2 * args.interval_runs + 1:
        raise SystemExit("max-size must exceed the claimed VC dimension 2*interval-runs")
    if args.max_size > 18:
        raise SystemExit("max-size above 18 is refused because Track A explicitly enumerates bit strings")
    if args.domain_size < 2 or args.uniform_size < 2:
        raise SystemExit("domain-size and uniform-size must be at least two")
    if args.uniform_size > 160:
        raise SystemExit("uniform-size above 160 is refused by the exact dynamic-program contract")
    if not 0 < args.delta < 1:
        raise SystemExit("delta must lie in (0,1)")
    if not (len(dims) == len(weights) == len(empirical) == len(true)):
        raise SystemExit("layer dimensions, weights, empirical risks and true risks must have equal length")
    if any(d < 1 or d > 2 * args.srm_size for d in dims):
        raise SystemExit("each layer dimension must lie in [1,2*srm-size]")
    if any(w <= 0 for w in weights) or sum(weights) > 1 + 1e-12:
        raise SystemExit("layer weights must be positive and sum to at most one")
    if any(not 0 <= risk <= 1 for risk in empirical + true):
        raise SystemExit("all risks must lie in [0,1]")
    if args.srm_size < 1:
        raise SystemExit("srm-size must be positive")
    if args.multiclass_points < 1 or args.multiclass_points > 8:
        raise SystemExit("multiclass-points must lie in [1,8]")
    if args.label_count < 2 or args.label_count > 12:
        raise SystemExit("label-count must lie in [2,12]")
    return dims, weights, empirical, true


def is_canonical(args: argparse.Namespace) -> bool:
    return all(getattr(args, key) == value for key, value in DEFAULTS.items())


def one_runs(bits: tuple[int, ...]) -> int:
    return sum(bit == 1 and (index == 0 or bits[index - 1] == 0) for index, bit in enumerate(bits))


def enumerate_run_patterns(m: int, max_runs: int) -> int:
    return sum(one_runs(bits) <= max_runs for bits in itertools.product((0, 1), repeat=m))


def sauer_sum(m: int, dimension: int) -> int:
    return sum(math.comb(m, index) for index in range(min(m, dimension) + 1))


def growth_summary(max_size: int, runs: int) -> GrowthSummary:
    m_values = tuple(range(1, max_size + 1))
    thresholds = tuple(m + 1 for m in m_values)
    intervals = tuple(enumerate_run_patterns(m, 1) for m in m_values)
    run_counts = tuple(enumerate_run_patterns(m, runs) for m in m_values)
    dimension = 2 * runs
    sauer = tuple(sauer_sum(m, dimension) for m in m_values)
    if run_counts != sauer:
        raise AssertionError("unions of ordered intervals should attain the Sauer envelope")
    inferred = max(m for m, count in zip(m_values, run_counts) if count == 2**m)
    if inferred != dimension or run_counts[dimension] >= 2 ** (dimension + 1):
        raise AssertionError("enumerated shattering transition disagrees with VC=2*runs")
    return GrowthSummary(m_values, thresholds, intervals, run_counts, sauer, inferred)


def discrete_cdf_success(domain_size: int, sample_size: int, radius: float) -> float:
    """Exact P(sup_j |F_m(j)-j/D| <= radius) for Uniform{1,...,D}."""
    inverse_factorials = tuple(1.0 / math.factorial(count) for count in range(sample_size + 1))
    states: dict[int, float] = {0: 1.0}
    for category in range(1, domain_size + 1):
        next_states: dict[int, float] = {}
        for allocated, weight in states.items():
            for count in range(sample_size - allocated + 1):
                total = allocated + count
                if category < domain_size:
                    gap = abs(total / sample_size - category / domain_size)
                    if gap > radius + 1e-14:
                        continue
                next_states[total] = next_states.get(total, 0.0) + weight * inverse_factorials[count]
        states = next_states
    coefficient = states.get(sample_size, 0.0)
    probability = math.factorial(sample_size) * coefficient / domain_size**sample_size
    return min(1.0, max(0.0, probability))


def uniform_summary(domain_size: int, sample_size: int, delta: float) -> UniformSummary:
    candidates = {0.0}
    for category in range(1, domain_size):
        truth = category / domain_size
        for count in range(sample_size + 1):
            candidates.add(abs(count / sample_size - truth))
    exact_radius = 1.0
    exact_success = 1.0
    for radius in sorted(candidates):
        success = discrete_cdf_success(domain_size, sample_size, radius)
        if success >= 1 - delta - 1e-12:
            exact_radius, exact_success = radius, success
            break

    dkw_radius = math.sqrt(math.log(2 / delta) / (2 * sample_size))
    finite_radius = math.sqrt(math.log(2 * (domain_size + 1) / delta) / (2 * sample_size))
    growth_2m = 2 * sample_size + 1  # threshold class: tau(n)=n+1
    vc_radius = math.sqrt(8 / sample_size * (math.log(growth_2m) + math.log(4 / delta)))
    failure_at_finite = 1 - discrete_cdf_success(domain_size, sample_size, finite_radius)
    return UniformSummary(
        exact_radius,
        exact_success,
        dkw_radius,
        finite_radius,
        vc_radius,
        failure_at_finite,
    )


def pseudo_witness_patterns() -> int:
    points = (-1.0, 1.0)
    thresholds = (0.0, 0.0)
    patterns = set()
    for slope in (-2.0, -1.0, 0.0, 1.0, 2.0):
        for intercept in (-2.0, -1.0, 0.0, 1.0, 2.0):
            patterns.add(tuple(int(slope * x + intercept > threshold) for x, threshold in zip(points, thresholds)))
    return len(patterns)


def srm_summary(
    dims: tuple[int, ...], weights: tuple[float, ...], empirical: tuple[float, ...],
    true: tuple[float, ...], sample_size: int, delta: float, multiclass_points: int, label_count: int,
) -> SRMSummary:
    penalties = tuple(
        min(
            1.0,
            math.sqrt(
                8 / sample_size
                * (dimension * math.log(2 * math.e * sample_size / dimension) + math.log(4 / (delta * weight)))
            ),
        )
        for dimension, weight in zip(dims, weights)
    )
    scores = tuple(risk + penalty for risk, penalty in zip(empirical, penalties))
    selected = min(range(len(scores)), key=lambda index: (scores[index], index))
    oracle_bounds = tuple(risk + 2 * penalty for risk, penalty in zip(true, penalties))
    oracle_layer = min(range(len(oracle_bounds)), key=lambda index: (oracle_bounds[index], index))

    # Full multiclass functions on q points contain both a Natarajan two-label
    # witness and every match/deviate pattern relative to a fixed graph witness.
    full_functions = label_count**multiclass_points
    binary_witness = 2**multiclass_points
    return SRMSummary(
        dims,
        weights,
        empirical,
        true,
        penalties,
        scores,
        selected,
        oracle_bounds,
        oracle_layer,
        binary_witness,
        binary_witness,
        full_functions,
        pseudo_witness_patterns(),
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, size: int = 15, color: str = INK, weight: int = 500,
         anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{esc(value)}</text>'
    )


def rect(x: float, y: float, width: float, height: float, fill: str = PAPER, stroke: str = GRID,
         radius: float = 12, stroke_width: float = 1.5) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 2) -> str:
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width:.1f}"/>'


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.5, dash: str = "") -> str:
    serial = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{serial}" fill="none" stroke="{color}" stroke-width="{width:.1f}"{dash_attr}/>'


def panel(parts: list[str], x: float, label: str, title: str, subtitle: str, color: str) -> None:
    parts += [rect(x, 112, 420, 525), text(x + 22, 148, label, 14, color, 750),
              text(x + 60, 148, title, 19, INK, 750), text(x + 22, 177, subtitle, 13, MUTED, 500)]


def build_svg(args: argparse.Namespace, growth: GrowthSummary, uniform: UniformSummary, srm: SRMSummary) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 700" role="img" aria-labelledby="title desc">',
        '<title id="title">VC 维与一致收敛累计证据门</title>',
        '<desc id="desc">增长函数、精确一致偏差和结构风险最小化与推广见证的三轨解析总图。</desc>',
        rect(0, 0, 1440, 700, BG, BG, 0, 0),
        text(40, 48, "VC 维与一致收敛：组合容量如何变成风险证书", 27, INK, 800),
        text(40, 78, "从 labeling patterns 到概率事件，再到可数模型层级；有限见证只承担它能证明的方向。", 15, MUTED, 500),
    ]

    panel(parts, 35, "A", "增长函数 × Sauer 包络", "ordered unions of intervals; exact enumeration", BLUE)
    parts += [text(60, 210, f"runs={args.interval_runs} ⇒ claimed VC d={growth.vc_dimension}", 14, INK, 700)]
    x0, y0, width, height = 72, 500, 330, 245
    parts += [line(x0, y0 - height, x0, y0, INK, 1.5), line(x0, y0, x0 + width, y0, INK, 1.5)]
    max_log = max(growth.m_values)
    series = (
        (growth.threshold_counts, TEAL, "thresholds"),
        (growth.one_interval_counts, AMBER, "one interval"),
        (growth.run_counts, BLUE, f"≤{args.interval_runs} runs"),
        (tuple(2**m for m in growth.m_values), RED, "all labelings"),
    )
    for counts, color, _ in series:
        points = []
        for index, (m, count) in enumerate(zip(growth.m_values, counts)):
            x = x0 + index * width / max(1, len(growth.m_values) - 1)
            y = y0 - math.log2(count) / max_log * height
            points.append((x, y))
        parts.append(polyline(points, color, 2.5, "7 5" if color == RED else ""))
    for index, (_, color, label) in enumerate(series):
        y = 535 + index * 23
        parts += [line(60, y - 5, 82, y - 5, color, 3), text(90, y, label, 12, color, 650)]
    parts += [text(237, 520, "x: sample size m  ·  y: log2 τ(m)", 11, MUTED, 600, "middle")]
    parts += [text(60, 625, f"τ(d)={2**growth.vc_dimension}; τ(d+1)={growth.run_counts[growth.vc_dimension]}<2^(d+1)", 12, RED, 700)]

    panel(parts, 510, "B", "阈值类的精确共同偏差", "finite-domain KS law vs general certificates", TEAL)
    parts += [text(535, 210, f"Uniform domain D={args.domain_size}, m={args.uniform_size}, δ={args.delta:.3f}", 14, INK, 700)]
    radius_rows = (
        ("exact (1−δ) radius", uniform.exact_radius, TEAL),
        ("DKW radius", uniform.dkw_radius, BLUE),
        ("finite |H|=D+1", uniform.finite_radius, AMBER),
        ("VC route (raw)", uniform.vc_radius_raw, RED),
    )
    max_radius = max(value for _, value, _ in radius_rows)
    for index, (label, value, color) in enumerate(radius_rows):
        y = 246 + index * 68
        bar_width = 270 * value / max_radius
        parts += [text(535, y, label, 13, MUTED, 600), rect(535, y + 12, 270, 18, "#EEF2F7", "#EEF2F7", 4, 0),
                  rect(535, y + 12, bar_width, 18, color, color, 4, 0), text(875, y + 27, f"{value:.6f}", 13, color, 700, "end")]
    parts += [line(535, 520, 885, 520), text(535, 552, f"exact success at exact radius = {uniform.exact_success:.6f}", 14, TEAL, 700),
              text(535, 582, f"exact failure at finite-H radius = {uniform.exact_failure_at_finite:.6f}", 14, BLUE, 700),
              text(535, 612, "VC radius > 1 is valid but vacuous for 0–1 risk", 12, RED, 650)]

    panel(parts, 985, "C", "SRM 选择 × 推广见证", "weighted layer search; witness is not a dimension proof", RED)
    parts += [text(1010, 210, f"SRM m={args.srm_size}, δ={args.delta:.3f}", 14, INK, 700),
              text(1010, 236, "layer   d    R_S    penalty    score", 12, MUTED, 650)]
    for index, (dimension, empirical, penalty, score) in enumerate(zip(srm.dims, srm.empirical, srm.penalties, srm.scores)):
        y = 267 + index * 38
        color = TEAL if index == srm.selected else INK
        marker = "★" if index == srm.selected else " "
        parts += [text(1010, y, f"{marker} H{index+1}", 13, color, 750), text(1075, y, str(dimension), 13, color, 600),
                  text(1120, y, f"{empirical:.3f}", 13, color, 600), text(1190, y, f"{penalty:.3f}", 13, color, 600),
                  text(1280, y, f"{score:.3f}", 13, color, 700)]
    bottom = 267 + len(srm.dims) * 38
    parts += [text(1010, bottom + 12, f"selected layer = H{srm.selected+1}", 13, TEAL, 700),
              text(1010, bottom + 36, f"best true-risk layer = H{min(range(len(srm.true)), key=srm.true.__getitem__)+1}", 12, MUTED, 600),
              text(1010, bottom + 60, f"best oracle-bound layer = H{srm.oracle_layer+1}", 12, RED, 650),
              line(1010, bottom + 78, 1380, bottom + 78),
              rect(1010, bottom + 94, 175, 82, "#ECFDF5", TEAL, 8, 1.5),
              text(1022, bottom + 118, "multiclass full class", 12, TEAL, 700),
              text(1022, bottom + 142, f"|Y|^q={srm.multiclass_functions}; q={args.multiclass_points}", 12, INK, 600),
              text(1022, bottom + 164, f"N/G witness patterns={srm.natarajan_patterns}", 12, INK, 600),
              rect(1200, bottom + 94, 180, 82, "#EFF6FF", BLUE, 8, 1.5),
              text(1212, bottom + 118, "affine pseudo witness", 12, BLUE, 700),
              text(1212, bottom + 142, "x=(−1,1), r=(0,0)", 12, INK, 600),
              text(1212, bottom + 164, f"realized bits={srm.pseudo_patterns}/4", 12, INK, 600),
              text(1010, 620, "witness ⇒ lower bound only; upper bound needs a separate proof", 11, RED, 650)]

    parts += [text(720, 677, "读图顺序：先数行为，再建共同事件，最后做层级选择；每次都重写对象与量词。", 14, MUTED, 600, "middle"), "</svg>"]
    return "\n".join(parts) + "\n"


def print_summary(args: argparse.Namespace, growth: GrowthSummary, uniform: UniformSummary,
                  srm: SRMSummary, output: Path) -> None:
    print("VC-CUM-01 deterministic three-track gate")
    print(
        "TRACK A "
        f"runs={args.interval_runs} vc={growth.vc_dimension} "
        f"tau_d={growth.run_counts[growth.vc_dimension-1]} "
        f"tau_d1={growth.run_counts[growth.vc_dimension]} "
        f"tau_max={growth.run_counts[-1]} sauer_max={growth.sauer_counts[-1]}"
    )
    print(
        "TRACK B "
        f"exact_radius={uniform.exact_radius:.6f} exact_success={uniform.exact_success:.6f} "
        f"dkw_radius={uniform.dkw_radius:.6f} finite_radius={uniform.finite_radius:.6f} "
        f"vc_radius_raw={uniform.vc_radius_raw:.6f} "
        f"failure_at_finite={uniform.exact_failure_at_finite:.6f}"
    )
    print(
        "TRACK C "
        f"selected={srm.selected+1} oracle_layer={srm.oracle_layer+1} "
        f"penalties={','.join(f'{value:.6f}' for value in srm.penalties)} "
        f"scores={','.join(f'{value:.6f}' for value in srm.scores)} "
        f"multiclass_functions={srm.multiclass_functions} "
        f"natarajan_patterns={srm.natarajan_patterns} graph_patterns={srm.graph_patterns} "
        f"pseudo_patterns={srm.pseudo_patterns}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    dims, weights, empirical, true = validate(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")
    output.parent.mkdir(parents=True, exist_ok=True)

    growth = growth_summary(args.max_size, args.interval_runs)
    uniform = uniform_summary(args.domain_size, args.uniform_size, args.delta)
    srm = srm_summary(
        dims, weights, empirical, true, args.srm_size, args.delta, args.multiclass_points, args.label_count
    )
    output.write_text(build_svg(args, growth, uniform, srm), encoding="utf-8")
    print_summary(args, growth, uniform, srm, output)


if __name__ == "__main__":
    main()
