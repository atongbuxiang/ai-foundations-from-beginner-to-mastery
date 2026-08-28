#!/usr/bin/env python3
"""Deterministic three-track evidence gate for PAC learning and finite classes.

The script deliberately uses exactly enumerable finite models.  It is a teaching
instrument, not a Monte-Carlo illustration: every reported probability is an
analytic finite sum and every SVG is byte deterministic.
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
    / "plot-pac-finite-class-cumulative-gate-v2.svg"
)

DEFAULTS = {
    "bad_count": 31,
    "bad_risk": 0.18,
    "realizable_size": 28,
    "risk_grid": "0.18,0.22,0.29,0.36",
    "agnostic_size": 40,
    "code_lengths": "1,2,4,4,5",
    "occam_size": 80,
    "testing_size": 40,
    "gamma": 0.04,
    "delta": 0.05,
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
class RealizableSummary:
    bad_count: int
    survival_one: float
    exact_failure: float
    union_failure: float
    exponential_failure: float
    sufficient_m: int
    exact_m: int


@dataclass(frozen=True)
class AgnosticSummary:
    risks: tuple[float, ...]
    radius: float
    exact_uniform_failure: float
    expected_population: float
    expected_train: float
    selection_gap: float
    class_excess: float
    selection_mass: float


@dataclass(frozen=True)
class CodingTestingSummary:
    lengths: tuple[int, ...]
    kraft_sum: float
    radii: tuple[float, ...]
    p_minus: float
    p_plus: float
    exact_tv: float
    exact_testing_error: float
    pinsker_testing_lower: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bad-count", type=int, default=DEFAULTS["bad_count"])
    parser.add_argument("--bad-risk", type=float, default=DEFAULTS["bad_risk"])
    parser.add_argument("--realizable-size", type=int, default=DEFAULTS["realizable_size"])
    parser.add_argument("--risk-grid", default=DEFAULTS["risk_grid"])
    parser.add_argument("--agnostic-size", type=int, default=DEFAULTS["agnostic_size"])
    parser.add_argument("--code-lengths", default=DEFAULTS["code_lengths"])
    parser.add_argument("--occam-size", type=int, default=DEFAULTS["occam_size"])
    parser.add_argument("--testing-size", type=int, default=DEFAULTS["testing_size"])
    parser.add_argument("--gamma", type=float, default=DEFAULTS["gamma"])
    parser.add_argument("--delta", type=float, default=DEFAULTS["delta"])
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def parse_float_list(raw: str) -> tuple[float, ...]:
    try:
        values = tuple(float(item.strip()) for item in raw.split(",") if item.strip())
    except ValueError as exc:
        raise SystemExit(f"invalid float list: {raw!r}") from exc
    if not values:
        raise SystemExit("risk grid must not be empty")
    return values


def parse_int_list(raw: str) -> tuple[int, ...]:
    try:
        values = tuple(int(item.strip()) for item in raw.split(",") if item.strip())
    except ValueError as exc:
        raise SystemExit(f"invalid integer list: {raw!r}") from exc
    if not values:
        raise SystemExit("code lengths must not be empty")
    return values


def validate(args: argparse.Namespace) -> tuple[tuple[float, ...], tuple[int, ...]]:
    risks = parse_float_list(args.risk_grid)
    lengths = parse_int_list(args.code_lengths)
    if args.bad_count < 1:
        raise SystemExit("bad-count must be positive")
    if not 0 < args.bad_risk < 1:
        raise SystemExit("bad-risk must lie in (0,1)")
    if args.realizable_size < 1 or args.agnostic_size < 1 or args.occam_size < 1 or args.testing_size < 1:
        raise SystemExit("all sample sizes must be positive")
    if any(not 0 < risk < 1 for risk in risks):
        raise SystemExit("all risk-grid entries must lie in (0,1)")
    if len(risks) < 2:
        raise SystemExit("risk-grid needs at least two hypotheses")
    if any(length < 1 for length in lengths):
        raise SystemExit("all code lengths must be positive integers")
    if sum(2.0 ** (-length) for length in lengths) > 1 + 1e-12:
        raise SystemExit("code lengths violate the Kraft inequality")
    if not 0 < args.gamma < 0.5:
        raise SystemExit("gamma must lie in (0,0.5)")
    if not 0 < args.delta < 1:
        raise SystemExit("delta must lie in (0,1)")
    return risks, lengths


def is_canonical(args: argparse.Namespace) -> bool:
    return all(getattr(args, key) == value for key, value in DEFAULTS.items())


def binomial_pmf(n: int, q: float, count: int) -> float:
    return math.comb(n, count) * q**count * (1 - q) ** (n - count)


def binomial_cdf(n: int, q: float, count: int) -> float:
    if count < 0:
        return 0.0
    if count >= n:
        return 1.0
    return sum(binomial_pmf(n, q, k) for k in range(count + 1))


def realizable_summary(bad_count: int, risk: float, m: int, delta: float) -> RealizableSummary:
    survival = (1 - risk) ** m
    exact_failure = 1 - (1 - survival) ** bad_count
    union_failure = min(1.0, bad_count * survival)
    exponential_failure = min(1.0, bad_count * math.exp(-m * risk))
    sufficient_m = math.ceil(math.log(bad_count / delta) / risk)
    exact_m = 1
    while 1 - (1 - (1 - risk) ** exact_m) ** bad_count > delta:
        exact_m += 1
    return RealizableSummary(
        bad_count,
        survival,
        exact_failure,
        union_failure,
        exponential_failure,
        sufficient_m,
        exact_m,
    )


def agnostic_summary(risks: tuple[float, ...], m: int, delta: float) -> AgnosticSummary:
    k_hypotheses = len(risks)
    radius = math.sqrt(math.log(2 * k_hypotheses / delta) / (2 * m))

    uniform_success = 1.0
    for risk in risks:
        allowed = sum(
            binomial_pmf(m, risk, count)
            for count in range(m + 1)
            if abs(count / m - risk) <= radius + 1e-15
        )
        uniform_success *= allowed

    expected_population = 0.0
    expected_train = 0.0
    selection_mass = 0.0
    # Lexicographic ERM: earlier hypotheses win empirical-risk ties.
    for index, risk in enumerate(risks):
        for count in range(m + 1):
            probability = binomial_pmf(m, risk, count)
            for earlier in risks[:index]:
                probability *= 1 - binomial_cdf(m, earlier, count)
            for later in risks[index + 1 :]:
                probability *= 1 - binomial_cdf(m, later, count - 1)
            selection_mass += probability
            expected_population += probability * risk
            expected_train += probability * count / m

    return AgnosticSummary(
        risks,
        radius,
        1 - uniform_success,
        expected_population,
        expected_train,
        expected_population - expected_train,
        expected_population - min(risks),
        selection_mass,
    )


def coding_testing_summary(
    lengths: tuple[int, ...], occam_m: int, testing_m: int, gamma: float, delta: float
) -> CodingTestingSummary:
    kraft = sum(2.0 ** (-length) for length in lengths)
    radii = tuple(
        math.sqrt((math.log(2 / delta) + length * math.log(2)) / (2 * occam_m))
        for length in lengths
    )
    p_minus, p_plus = 0.5 - gamma, 0.5 + gamma
    tv = 0.5 * sum(
        abs(binomial_pmf(testing_m, p_minus, count) - binomial_pmf(testing_m, p_plus, count))
        for count in range(testing_m + 1)
    )
    exact_error = (1 - tv) / 2
    kl_one = 2 * gamma * math.log(p_plus / p_minus)
    pinsker_tv = min(1.0, math.sqrt(testing_m * kl_one / 2))
    pinsker_lower = (1 - pinsker_tv) / 2
    return CodingTestingSummary(
        lengths,
        kraft,
        radii,
        p_minus,
        p_plus,
        tv,
        exact_error,
        pinsker_lower,
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


def panel(parts: list[str], x: float, label: str, title: str, subtitle: str, color: str) -> None:
    parts += [rect(x, 112, 420, 505), text(x + 22, 148, label, 14, color, 750),
              text(x + 60, 148, title, 19, INK, 750), text(x + 22, 177, subtitle, 13, MUTED, 500)]


def build_svg(args: argparse.Namespace, real: RealizableSummary, agn: AgnosticSummary,
              coding: CodingTestingSummary) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 680" role="img" aria-labelledby="title desc">',
        '<title id="title">PAC 与有限假设类累计证据门</title>',
        '<desc id="desc">可实现生存概率、不可知 ERM 选择和 Occam 编码与 Le Cam 下界的三轨解析总图。</desc>',
        rect(0, 0, 1440, 680, BG, BG, 0, 0),
        text(40, 48, "PAC 与有限假设类：上界、选择与下界", 27, INK, 800),
        text(40, 78, "同一张图分清：零错排除、双侧均值比较、非均匀预算和统计不可区分性。", 15, MUTED, 500),
    ]

    panel(parts, 35, "A", "可实现：坏假设生存", "exact model → union bound → exp certificate", BLUE)
    sx, sy, sw = 70, 220, 340
    parts += [text(60, 211, f"|H|-1={args.bad_count}, r={args.bad_risk:.3f}, m={args.realizable_size}", 14, INK, 650)]
    rows = (
        ("one bad h survives", real.survival_one, TEAL),
        ("exact any-bad failure", real.exact_failure, BLUE),
        ("union bound", real.union_failure, AMBER),
        ("M exp(-mr)", real.exponential_failure, RED),
    )
    for idx, (label, value, color) in enumerate(rows):
        y = sy + idx * 64
        width = max(2.0, sw * min(1.0, value))
        parts += [text(60, y, label, 13, MUTED, 600), rect(sx, y + 10, sw, 18, "#EEF2F7", "#EEF2F7", 4, 0),
                  rect(sx, y + 10, width, 18, color, color, 4, 0), text(420, y + 25, f"{value:.6f}", 13, color, 700, "end")]
    parts += [line(60, 490, 430, 490), text(60, 520, f"exact minimal m for δ: {real.exact_m}", 15, TEAL, 700),
              text(60, 548, f"exp sufficient m: {real.sufficient_m}", 15, RED, 700),
              text(60, 580, "mechanism: every sample must miss E_h", 13, MUTED, 500)]

    panel(parts, 510, "B", "不可知：共同事件覆盖 ERM", "exact binomial sums + lexicographic selection", TEAL)
    parts += [text(535, 211, f"K={len(agn.risks)}, m={args.agnostic_size}, δ={args.delta:.3f}", 14, INK, 650),
              text(535, 241, "true risks q_j", 13, MUTED, 600)]
    for idx, risk in enumerate(agn.risks):
        x = 545 + idx * (320 / max(1, len(agn.risks) - 1))
        y = 340 - risk * 260
        parts += [line(x, 350, x, y, GRID, 1.5), f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{TEAL}"/>',
                  text(x, 372, f"h{idx+1}", 12, MUTED, 600, "middle"), text(x, y - 12, f"{risk:.2f}", 12, TEAL, 700, "middle")]
    parts += [line(540, 350, 880, 350, INK, 1.5), text(535, 412, f"Hoeffding radius α = {agn.radius:.6f}", 14, BLUE, 700),
              text(535, 442, f"exact P(uniform event fails) = {agn.exact_uniform_failure:.6f}", 14, RED, 700),
              text(535, 482, f"E[R_P(h_ERM)] = {agn.expected_population:.6f}", 14, INK, 650),
              text(535, 510, f"E[R_S(h_ERM)] = {agn.expected_train:.6f}", 14, INK, 650),
              text(535, 538, f"selection gap = {agn.selection_gap:.6f}", 14, RED, 700),
              text(535, 566, f"class excess = {agn.class_excess:.6f}", 14, TEAL, 700),
              text(535, 594, "proof bridge spends α twice: excess ≤ 2α", 13, MUTED, 500)]

    panel(parts, 985, "C", "编码上界 × 测试下界", "Kraft-weighted confidence + exact Le Cam TV", RED)
    parts += [text(1010, 211, f"code L={','.join(map(str, coding.lengths))}; Kraft={coding.kraft_sum:.5f}", 14, INK, 650),
              text(1010, 241, f"Occam m={args.occam_size}, δ={args.delta:.3f}", 13, MUTED, 600)]
    max_radius = max(coding.radii)
    for idx, (length, radius) in enumerate(zip(coding.lengths, coding.radii)):
        y = 262 + idx * 38
        width = 245 * radius / max_radius
        parts += [text(1010, y + 16, f"L={length}", 12, MUTED, 650), rect(1055, y, 245, 18, "#EEF2F7", "#EEF2F7", 4, 0),
                  rect(1055, y, width, 18, BLUE, BLUE, 4, 0), text(1325, y + 15, f"α={radius:.4f}", 12, BLUE, 700, "end")]
    separator = 455
    parts += [line(1010, separator, 1380, separator),
              text(1010, separator + 32, f"P−=Bern({coding.p_minus:.2f}), P+=Bern({coding.p_plus:.2f}), m={args.testing_size}", 13, INK, 650),
              text(1010, separator + 62, f"exact TV(P−^m,P+^m) = {coding.exact_tv:.6f}", 14, TEAL, 700),
              text(1010, separator + 91, f"min testing error = (1-TV)/2 = {coding.exact_testing_error:.6f}", 14, RED, 700),
              text(1010, separator + 120, f"Pinsker-certified lower bound = {coding.pinsker_testing_lower:.6f}", 13, AMBER, 700),
              text(1010, 603, "upper: exists success · lower: every algorithm can face failure", 11, MUTED, 500)]

    parts += [text(720, 657, "教材式读图顺序：先核事件和量词，再比较数值；图像不替代证明。", 14, MUTED, 600, "middle"), "</svg>"]
    return "\n".join(parts) + "\n"


def print_summary(args: argparse.Namespace, real: RealizableSummary, agn: AgnosticSummary,
                  coding: CodingTestingSummary, output: Path) -> None:
    print("PAC-CUM-01 deterministic three-track gate")
    print(
        "TRACK A "
        f"bad={real.bad_count} survival={real.survival_one:.6f} exact_failure={real.exact_failure:.6f} "
        f"union={real.union_failure:.6f} exponential={real.exponential_failure:.6f} "
        f"exact_m={real.exact_m} sufficient_m={real.sufficient_m}"
    )
    print(
        "TRACK B "
        f"radius={agn.radius:.6f} exact_uniform_failure={agn.exact_uniform_failure:.6f} "
        f"expected_population={agn.expected_population:.6f} expected_train={agn.expected_train:.6f} "
        f"selection_gap={agn.selection_gap:.6f} class_excess={agn.class_excess:.6f} "
        f"mass={agn.selection_mass:.12f}"
    )
    print(
        "TRACK C "
        f"kraft={coding.kraft_sum:.6f} radii={','.join(f'{value:.6f}' for value in coding.radii)} "
        f"tv={coding.exact_tv:.6f} testing_error={coding.exact_testing_error:.6f} "
        f"pinsker_lower={coding.pinsker_testing_lower:.6f}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    risks, lengths = validate(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = args.output if args.output is not None else CANONICAL_OUTPUT
    output = output.resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")
    output.parent.mkdir(parents=True, exist_ok=True)

    real = realizable_summary(args.bad_count, args.bad_risk, args.realizable_size, args.delta)
    agn = agnostic_summary(risks, args.agnostic_size, args.delta)
    coding = coding_testing_summary(lengths, args.occam_size, args.testing_size, args.gamma, args.delta)
    output.write_text(build_svg(args, real, agn, coding), encoding="utf-8")
    print_summary(args, real, agn, coding, output)


if __name__ == "__main__":
    main()
