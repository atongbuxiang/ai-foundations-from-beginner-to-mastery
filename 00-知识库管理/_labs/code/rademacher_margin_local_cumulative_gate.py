#!/usr/bin/env python3
"""Deterministic three-track evidence gate for RAD-CUM-01.

Track A enumerates every Rademacher sign vector on a fixed two-dimensional
sample, checks the exact dual-norm formula, and measures a centered ramp
composition on a finite score class.  Track B audits a preregistered margin
grid with a simultaneous confidence budget.  Track C computes exact internal
covers of a small Hamming cube, a sub-root fixed point, and an orthogonal
linear-ball fat-shattering profile.  No Monte Carlo is used.
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
    / "plot-rademacher-margin-local-cumulative-gate-v2.svg"
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

DEFAULT_MARGIN_LEVELS = "-0.2,0.15,0.35,0.7,1.2"
DEFAULT_MARGIN_COUNTS = "40,80,160,440,880"
DEFAULT_GAMMA_GRID = "0.2,0.4,0.8,1.0"
DEFAULT_FAT_GAMMAS = "0.25,0.35,0.5,0.75"


@dataclass(frozen=True)
class SignSummary:
    l2_exact: float
    energy_bound: float
    finite_score: float
    finite_margin: float
    ramp_complexity: float
    contraction_bound: float
    sign_count: int
    restriction_count: int


@dataclass(frozen=True)
class MarginSummary:
    sample_size: int
    gammas: tuple[float, ...]
    low_margin_rates: tuple[float, ...]
    penalties: tuple[float, ...]
    confidence: float
    raw_bounds: tuple[float, ...]
    selected: int
    linear_radius: float


@dataclass(frozen=True)
class ScaleSummary:
    hamming_radii: tuple[int, ...]
    cover_numbers: tuple[int, ...]
    fixed_point: float
    slow_radius: float
    improvement: float
    fat_gammas: tuple[float, ...]
    fat_dimensions: tuple[int, ...]


def parse_float_csv(raw: str, label: str) -> tuple[float, ...]:
    try:
        values = tuple(float(piece.strip()) for piece in raw.split(",") if piece.strip())
    except ValueError as exc:
        raise SystemExit(f"{label} must be a comma-separated numeric list") from exc
    if not values or any(not math.isfinite(value) for value in values):
        raise SystemExit(f"{label} must contain finite values")
    return values


def parse_int_csv(raw: str, label: str) -> tuple[int, ...]:
    try:
        values = tuple(int(piece.strip()) for piece in raw.split(",") if piece.strip())
    except ValueError as exc:
        raise SystemExit(f"{label} must be a comma-separated integer list") from exc
    if not values:
        raise SystemExit(f"{label} may not be empty")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--linear-norm", type=float, default=1.0)
    parser.add_argument("--ramp-gamma", type=float, default=0.75)
    parser.add_argument("--margin-levels", default=DEFAULT_MARGIN_LEVELS)
    parser.add_argument("--margin-counts", default=DEFAULT_MARGIN_COUNTS)
    parser.add_argument("--gamma-grid", default=DEFAULT_GAMMA_GRID)
    parser.add_argument("--margin-norm", type=float, default=1.25)
    parser.add_argument("--data-radius", type=float, default=1.0)
    parser.add_argument("--delta", type=float, default=0.05)
    parser.add_argument("--cover-dim", type=int, default=4)
    parser.add_argument("--local-dim", type=int, default=8)
    parser.add_argument("--local-size", type=int, default=800)
    parser.add_argument("--local-a", type=float, default=1.2)
    parser.add_argument("--local-b", type=float, default=0.5)
    parser.add_argument("--fat-ambient", type=int, default=8)
    parser.add_argument("--fat-norm", type=float, default=1.0)
    parser.add_argument("--fat-radius", type=float, default=1.0)
    parser.add_argument("--fat-gammas", default=DEFAULT_FAT_GAMMAS)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def validate(args: argparse.Namespace) -> tuple[tuple[float, ...], tuple[int, ...], tuple[float, ...], tuple[float, ...]]:
    levels = parse_float_csv(args.margin_levels, "margin-levels")
    counts = parse_int_csv(args.margin_counts, "margin-counts")
    gammas = parse_float_csv(args.gamma_grid, "gamma-grid")
    fat_gammas = parse_float_csv(args.fat_gammas, "fat-gammas")
    if len(levels) != len(counts):
        raise SystemExit("margin-levels and margin-counts must have equal lengths")
    if any(count <= 0 for count in counts):
        raise SystemExit("margin-counts must be positive")
    if tuple(sorted(levels)) != levels:
        raise SystemExit("margin-levels must be increasing")
    if tuple(sorted(gammas)) != gammas or any(gamma <= 0 for gamma in gammas):
        raise SystemExit("gamma-grid must be positive and increasing")
    if tuple(sorted(fat_gammas)) != fat_gammas or any(gamma <= 0 for gamma in fat_gammas):
        raise SystemExit("fat-gammas must be positive and increasing")
    if not (0 < args.delta < 1):
        raise SystemExit("delta must lie in (0,1)")
    for label in ("linear_norm", "ramp_gamma", "margin_norm", "data_radius", "local_a", "local_b",
                  "fat_norm", "fat_radius"):
        if getattr(args, label) <= 0:
            raise SystemExit(f"{label.replace('_', '-')} must be positive")
    if not (1 <= args.cover_dim <= 4):
        raise SystemExit("cover-dim must lie in 1..4 for exact internal-cover enumeration")
    if args.local_dim <= 0 or args.local_size <= 0 or args.local_dim > args.local_size:
        raise SystemExit("local dimensions require 0 < local-dim <= local-size")
    if args.fat_ambient <= 0:
        raise SystemExit("fat-ambient must be positive")
    return levels, counts, gammas, fat_gammas


def is_canonical(args: argparse.Namespace) -> bool:
    return (
        args.linear_norm == 1.0
        and args.ramp_gamma == 0.75
        and args.margin_levels == DEFAULT_MARGIN_LEVELS
        and args.margin_counts == DEFAULT_MARGIN_COUNTS
        and args.gamma_grid == DEFAULT_GAMMA_GRID
        and args.margin_norm == 1.25
        and args.data_radius == 1.0
        and args.delta == 0.05
        and args.cover_dim == 4
        and args.local_dim == 8
        and args.local_size == 800
        and args.local_a == 1.2
        and args.local_b == 0.5
        and args.fat_ambient == 8
        and args.fat_norm == 1.0
        and args.fat_radius == 1.0
        and args.fat_gammas == DEFAULT_FAT_GAMMAS
    )


def dot(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right))


def exact_finite_rademacher(vectors: tuple[tuple[float, ...], ...]) -> float:
    sample_size = len(vectors[0])
    total = 0.0
    for signs in itertools.product((-1.0, 1.0), repeat=sample_size):
        total += max(dot(signs, vector) for vector in vectors) / sample_size
    return total / (2**sample_size)


def ramp(value: float, gamma: float) -> float:
    if value <= 0:
        return 1.0
    if value >= gamma:
        return 0.0
    return 1.0 - value / gamma


def sign_summary(linear_norm: float, ramp_gamma: float) -> SignSummary:
    sample = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, -1.0))
    labels = (1.0, 1.0, -1.0, 1.0)
    sample_size = len(sample)
    norm_total = 0.0
    for signs in itertools.product((-1.0, 1.0), repeat=sample_size):
        vector = tuple(sum(sign * point[j] for sign, point in zip(signs, sample)) for j in range(2))
        norm_total += math.sqrt(dot(vector, vector))
    l2_exact = linear_norm * norm_total / (2**sample_size) / sample_size
    energy_bound = linear_norm / sample_size * math.sqrt(sum(dot(point, point) for point in sample))

    base_weights = ((0.0, 0.0), (1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0))
    weights = tuple(tuple(linear_norm * value for value in weight) for weight in base_weights)
    scores = tuple(tuple(dot(weight, point) for point in sample) for weight in weights)
    margins = tuple(tuple(label * value for label, value in zip(labels, score)) for score in scores)
    centered_ramps = tuple(
        tuple(ramp(value, ramp_gamma) - ramp(0.0, ramp_gamma) for value in margin)
        for margin in margins
    )
    finite_score = exact_finite_rademacher(scores)
    finite_margin = exact_finite_rademacher(margins)
    ramp_complexity = exact_finite_rademacher(centered_ramps)
    contraction_bound = 2.0 / ramp_gamma * finite_score
    return SignSummary(
        l2_exact,
        energy_bound,
        finite_score,
        finite_margin,
        ramp_complexity,
        contraction_bound,
        2**sample_size,
        len(scores),
    )


def margin_summary(
    levels: tuple[float, ...], counts: tuple[int, ...], gammas: tuple[float, ...],
    norm_bound: float, data_radius: float, delta: float,
) -> MarginSummary:
    sample_size = sum(counts)
    linear_radius = norm_bound * data_radius / math.sqrt(sample_size)
    confidence = 3.0 * math.sqrt(math.log(2 * len(gammas) / delta) / (2 * sample_size))
    low_margin_rates = tuple(
        sum(count for level, count in zip(levels, counts) if level <= gamma) / sample_size
        for gamma in gammas
    )
    penalties = tuple(4.0 * linear_radius / gamma for gamma in gammas)
    raw_bounds = tuple(rate + penalty + confidence for rate, penalty in zip(low_margin_rates, penalties))
    selected = min(range(len(gammas)), key=lambda index: (raw_bounds[index], index))
    return MarginSummary(
        sample_size, gammas, low_margin_rates, penalties, confidence, raw_bounds, selected, linear_radius
    )


def hamming(left: int, right: int) -> int:
    return bin(left ^ right).count("1")


def exact_internal_cover(cube_dim: int, hamming_radius: int) -> int:
    points = tuple(range(2**cube_dim))
    balls = []
    for center in points:
        mask = 0
        for point in points:
            if hamming(center, point) <= hamming_radius:
                mask |= 1 << point
        balls.append(mask)
    full = (1 << len(points)) - 1
    for size in range(1, len(points) + 1):
        for centers in itertools.combinations(points, size):
            union = 0
            for center in centers:
                union |= balls[center]
            if union == full:
                return size
    raise AssertionError("finite cube must admit a cover")


def scale_summary(
    cover_dim: int, local_dim: int, local_size: int, local_a: float, local_b: float,
    fat_ambient: int, fat_norm: float, fat_radius: float, fat_gammas: tuple[float, ...],
) -> ScaleSummary:
    radii = tuple(sorted({0, 1, math.ceil(cover_dim / 2), cover_dim}))
    cover_numbers = tuple(exact_internal_cover(cover_dim, radius) for radius in radii)
    root_coefficient = local_a * math.sqrt(local_dim / local_size)
    offset = local_b * local_dim / local_size
    root_t = (root_coefficient + math.sqrt(root_coefficient**2 + 4 * offset)) / 2
    fixed_point = root_t**2
    slow_radius = root_coefficient + offset
    improvement = slow_radius / fixed_point
    fat_dimensions = tuple(
        min(fat_ambient, int(math.floor((fat_norm * fat_radius / gamma) ** 2 + 1e-12)))
        for gamma in fat_gammas
    )
    return ScaleSummary(
        radii, cover_numbers, fixed_point, slow_radius, improvement, fat_gammas, fat_dimensions
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


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 2,
         dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}"{dash_attr}/>'
    )


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.5, dash: str = "") -> str:
    serial = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{serial}" fill="none" stroke="{color}" stroke-width="{width:.1f}"{dash_attr}/>'


def circle(x: float, y: float, radius: float, fill: str, stroke: str = PAPER) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def panel(parts: list[str], x: float, label: str, title: str, subtitle: str, color: str) -> None:
    parts += [
        rect(x, 112, 420, 525),
        text(x + 22, 148, label, 14, color, 750),
        text(x + 60, 148, title, 19, INK, 750),
        text(x + 22, 177, subtitle, 13, MUTED, 500),
    ]


def build_svg(args: argparse.Namespace, signs: SignSummary, margins: MarginSummary, scales: ScaleSummary) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 700" role="img" aria-labelledby="title desc">',
        '<title id="title">数据依赖复杂度、间隔与快率累计证据门</title>',
        '<desc id="desc">精确 Rademacher 枚举、预注册间隔证书与覆盖数、局部固定点、fat profile 的三轨解析总图。</desc>',
        rect(0, 0, 1440, 700, BG, BG, 0, 0),
        text(40, 48, "Rademacher → margin → local/fat：复杂度怎样贴近数据与尺度", 26, INK, 800),
        text(40, 78, "先固定随机对象，再传递函数几何；最后才把局部或尺度信息写进风险证书。", 15, MUTED, 500),
    ]

    panel(parts, 35, "A", "精确 signs × 收缩", "fixed sample; all sign vectors, no Monte Carlo", BLUE)
    parts += [
        text(60, 210, f"m=4, signs={signs.sign_count}, finite restrictions={signs.restriction_count}", 14, INK, 700),
        text(60, 242, "infinite ℓ2 ball:  B/m · E‖Σσᵢxᵢ‖₂", 13, MUTED, 600),
    ]
    rows = (
        ("exact dual-norm R̂", signs.l2_exact, BLUE),
        ("energy upper bound", signs.energy_bound, AMBER),
        ("finite score R̂", signs.finite_score, TEAL),
        ("centered ramp R̂", signs.ramp_complexity, RED),
    )
    max_bar = max(value for _, value, _ in rows)
    for index, (label, value, color) in enumerate(rows):
        y = 278 + index * 57
        parts += [
            text(60, y, label, 13, MUTED, 600),
            rect(60, y + 10, 260, 17, "#EEF2F7", "#EEF2F7", 4, 0),
            rect(60, y + 10, 260 * value / max_bar, 17, color, color, 4, 0),
            text(410, y + 25, f"{value:.6f}", 13, color, 700, "end"),
        ]
    parts += [
        line(60, 520, 430, 520),
        text(60, 552, f"label multiplication: {signs.finite_score:.6f} = {signs.finite_margin:.6f}", 13, TEAL, 700),
        text(60, 582, f"safe contraction 2/γ · R̂ = {signs.contraction_bound:.6f}", 13, RED, 700),
        text(60, 612, "exact composed complexity can be much smaller than its certificate", 11, MUTED, 600),
    ]

    panel(parts, 510, "B", "预注册 margin 选择", "empirical curve + complexity + simultaneous confidence", TEAL)
    parts += [
        text(535, 210, f"m={margins.sample_size}, δ={args.delta:.3f}, |Γ|={len(margins.gammas)}", 14, INK, 700),
        text(535, 235, f"linear R̂ upper bound={margins.linear_radius:.6f}", 12, MUTED, 600),
    ]
    x0, y0, width, height = 555, 480, 300, 210
    parts += [line(x0, y0 - height, x0, y0, INK, 1.5), line(x0, y0, x0 + width, y0, INK, 1.5)]
    max_bound = max(1.0, max(margins.raw_bounds))
    empirical_points: list[tuple[float, float]] = []
    bound_points: list[tuple[float, float]] = []
    for index, (gamma, rate, bound) in enumerate(zip(margins.gammas, margins.low_margin_rates, margins.raw_bounds)):
        x = x0 + index * width / max(1, len(margins.gammas) - 1)
        empirical_y = y0 - rate / max_bound * height
        bound_y = y0 - bound / max_bound * height
        empirical_points.append((x, empirical_y))
        bound_points.append((x, bound_y))
        parts += [
            text(x, y0 + 22, f"{gamma:g}", 11, MUTED, 600, "middle"),
            circle(x, empirical_y, 4, BLUE),
            circle(x, bound_y, 5 if index == margins.selected else 4, TEAL if index == margins.selected else RED),
        ]
    parts += [
        polyline(empirical_points, BLUE),
        polyline(bound_points, RED),
        text(705, 520, "margin threshold γ", 11, MUTED, 600, "middle"),
        line(535, 548, 557, 548, BLUE, 3), text(565, 553, "empirical low-margin rate", 12, BLUE, 650),
        line(535, 574, 557, 574, RED, 3), text(565, 579, "raw simultaneous certificate", 12, RED, 650),
        text(535, 608, f"selected γ={margins.gammas[margins.selected]:g}; raw={margins.raw_bounds[margins.selected]:.6f}", 13, TEAL, 750),
        text(880, 608, f"confidence={margins.confidence:.6f}", 11, MUTED, 600, "end"),
    ]

    panel(parts, 985, "C", "尺度梯 × 局部 fixed point", "exact cover, sub-root mechanism and fat profile", RED)
    parts += [
        text(1010, 210, f"Hamming cube q={args.cover_dim}: exact internal covers", 14, INK, 700),
        text(1010, 238, "radius h", 12, MUTED, 650),
        text(1120, 238, "ε=√(h/q)", 12, MUTED, 650),
        text(1260, 238, "N(ε)", 12, MUTED, 650),
    ]
    for index, (radius, number) in enumerate(zip(scales.hamming_radii, scales.cover_numbers)):
        y = 268 + index * 31
        parts += [
            text(1010, y, str(radius), 13, INK, 650),
            text(1120, y, f"{math.sqrt(radius / args.cover_dim):.3f}", 13, BLUE, 650),
            text(1260, y, str(number), 13, TEAL, 750),
        ]
    local_top = 392
    parts += [line(1010, local_top, 1380, local_top), text(1010, local_top + 30, "sub-root ψ(r)=a√(rd/m)+b·d/m", 13, INK, 700)]
    plot_x, plot_y, plot_w, plot_h = 1020, 535, 170, 100
    r_max = max(0.08, scales.slow_radius * 1.1)
    fixed_points: list[tuple[float, float]] = []
    diagonal: list[tuple[float, float]] = []
    for index in range(51):
        radius = r_max * index / 50
        psi = args.local_a * math.sqrt(radius * args.local_dim / args.local_size) + args.local_b * args.local_dim / args.local_size
        x = plot_x + plot_w * radius / r_max
        fixed_points.append((x, plot_y - plot_h * min(psi, r_max) / r_max))
        diagonal.append((x, plot_y - plot_h * radius / r_max))
    parts += [
        line(plot_x, plot_y - plot_h, plot_x, plot_y, INK, 1.2),
        line(plot_x, plot_y, plot_x + plot_w, plot_y, INK, 1.2),
        polyline(diagonal, MUTED, 1.5, "5 4"),
        polyline(fixed_points, RED, 2.5),
    ]
    fixed_x = plot_x + plot_w * scales.fixed_point / r_max
    fixed_y = plot_y - plot_h * scales.fixed_point / r_max
    parts += [
        circle(fixed_x, fixed_y, 5, TEAL),
        text(1205, 455, f"r*={scales.fixed_point:.6f}", 13, TEAL, 750),
        text(1205, 481, f"global proxy={scales.slow_radius:.6f}", 12, MUTED, 650),
        text(1205, 507, f"ratio={scales.improvement:.3f}×", 12, RED, 700),
        text(1205, 545, "orthogonal ℓ2-ball fat profile", 12, INK, 700),
    ]
    for index, (gamma, dimension) in enumerate(zip(scales.fat_gammas, scales.fat_dimensions)):
        x = 1205 + (index % 2) * 95
        y = 571 + (index // 2) * 27
        parts.append(text(x, y, f"γ={gamma:g} → {dimension}", 12, BLUE if index % 2 == 0 else AMBER, 650))
    parts += [text(1010, 620, "fast rate needs Bernstein/curvature; fat witness keeps its scale", 10, RED, 650)]

    parts += [
        text(720, 675, "读图顺序：固定 signs 与 class → 为 γ 选择付预算 → 用尺度/局部结构改善证书，而非改写数据。", 13, MUTED, 650, "middle"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def print_summary(output: Path, signs: SignSummary, margins: MarginSummary, scales: ScaleSummary) -> None:
    margin_bits = ",".join(f"{gamma:g}:{bound:.6f}" for gamma, bound in zip(margins.gammas, margins.raw_bounds))
    cover_bits = ",".join(f"{radius}:{number}" for radius, number in zip(scales.hamming_radii, scales.cover_numbers))
    fat_bits = ",".join(f"{gamma:g}:{dimension}" for gamma, dimension in zip(scales.fat_gammas, scales.fat_dimensions))
    print("RAD-CUM-01 deterministic three-track gate")
    print(
        "TRACK A "
        f"l2_exact={signs.l2_exact:.6f} energy_bound={signs.energy_bound:.6f} "
        f"finite_score={signs.finite_score:.6f} finite_margin={signs.finite_margin:.6f} "
        f"ramp={signs.ramp_complexity:.6f} contraction_bound={signs.contraction_bound:.6f}"
    )
    print(
        "TRACK B "
        f"m={margins.sample_size} selected_gamma={margins.gammas[margins.selected]:g} "
        f"selected_raw={margins.raw_bounds[margins.selected]:.6f} "
        f"confidence={margins.confidence:.6f} rad_bound={margins.linear_radius:.6f} bounds={margin_bits}"
    )
    print(
        "TRACK C "
        f"cover={cover_bits} fixed={scales.fixed_point:.6f} slow={scales.slow_radius:.6f} "
        f"improvement={scales.improvement:.6f} fat={fat_bits}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    levels, counts, gammas, fat_gammas = validate(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")
    output.parent.mkdir(parents=True, exist_ok=True)

    signs = sign_summary(args.linear_norm, args.ramp_gamma)
    margins = margin_summary(levels, counts, gammas, args.margin_norm, args.data_radius, args.delta)
    scales = scale_summary(
        args.cover_dim, args.local_dim, args.local_size, args.local_a, args.local_b,
        args.fat_ambient, args.fat_norm, args.fat_radius, fat_gammas,
    )
    output.write_text(build_svg(args, signs, margins, scales), encoding="utf-8")
    print_summary(output, signs, margins, scales)


if __name__ == "__main__":
    main()
