#!/usr/bin/env python3
"""Deterministic three-track evidence gate for DEEP-CUM-01 (LT-77--84)."""

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
    / "plot-deep-generalization-cumulative-gate-v2.svg"
)

CANONICAL = {
    "sample_size": 20,
    "dimensions": "5,10,15,18,22,25,30,40,60,100",
    "noise_variance": 0.25,
    "signal_norm_squared": 1.0,
    "design": "1,0,1;0,1,1",
    "responses": "1,1",
    "null_shift": 2.0,
    "rescale": 4.0,
    "layer_spectral": "2,0.5,1.5",
    "layer_frobenius": "2.2360679775,0.7071067812,2.1213203436",
    "certificate_samples": 100,
    "margin": 0.5,
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
    dimensions: tuple[int, ...]
    risks: tuple[float, ...]
    peak_dimension: int
    peak_risk: float
    tail_risk: float
    min_norm: tuple[float, float, float]
    min_norm_length: float
    shifted_length: float
    train_residual: float
    null_test_gap: float


@dataclass(frozen=True)
class TrackB:
    rescale: float
    baseline_sharpness: float
    rescaled_sharpness: float
    function_product: float
    path_quantity: float
    spectral_product: float
    stable_rank_sum: float
    complexity: float
    certificate: float
    rescaled_complexity: float


@dataclass(frozen=True)
class TrackC:
    lambda_plus: float
    lambda_minus: float
    residual_initial_norm: float
    residual_final: tuple[float, float]
    residual_final_norm: float
    slow_mode_fraction: float
    particle_prediction_before: float
    particle_prediction_after: float
    feature_moment_before: float
    feature_moment_after: float
    relative_feature_drift: float
    ntk_before: float
    ntk_after: float
    relative_ntk_drift: float
    regime: str


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
        fail(f"{label} must contain rows")
    width = len(rows[0])
    if width == 0 or any(len(row) != width for row in rows):
        fail(f"{label} must be rectangular")
    return rows


def solve_2x2(matrix_: tuple[tuple[float, float], tuple[float, float]], rhs: tuple[float, float]) -> tuple[float, float]:
    (a, b), (c, d) = matrix_
    determinant = a * d - b * c
    if abs(determinant) <= 1e-12:
        fail("design must have full row rank")
    return ((d * rhs[0] - b * rhs[1]) / determinant, (-c * rhs[0] + a * rhs[1]) / determinant)


def compute_track_a(args: argparse.Namespace) -> TrackA:
    if args.sample_size < 4:
        fail("sample-size must be at least 4")
    dimensions = ints(args.dimensions, "dimensions")
    if len(dimensions) < 5 or any(value <= 0 for value in dimensions):
        fail("dimensions needs at least five positive integers")
    if len(set(dimensions)) != len(dimensions) or tuple(sorted(dimensions)) != dimensions:
        fail("dimensions must be strictly increasing")
    if args.noise_variance < 0.0 or args.signal_norm_squared < 0.0:
        fail("noise-variance and signal-norm-squared must be nonnegative")
    if any(value in (args.sample_size - 1, args.sample_size, args.sample_size + 1) for value in dimensions):
        fail("dimensions cannot use the singular interpolation window n-1,n,n+1")

    risks: list[float] = []
    for dimension in dimensions:
        if dimension < args.sample_size - 1:
            risk = args.noise_variance * dimension / (args.sample_size - dimension - 1)
        elif dimension > args.sample_size + 1:
            bias = args.signal_norm_squared * (1.0 - args.sample_size / dimension)
            variance = args.noise_variance * args.sample_size / (dimension - args.sample_size - 1)
            risk = bias + variance
        else:  # protected above; keeps the formula total under future edits.
            fail("risk is undefined in the finite-expectation interpolation window")
        risks.append(risk)

    design = matrix(args.design, "design")
    responses = floats(args.responses, "responses")
    if len(design) != 2 or len(design[0]) != 3 or len(responses) != 2:
        fail("design must be 2x3 and responses must have length 2")
    gram = (
        (sum(design[0][j] * design[0][j] for j in range(3)), sum(design[0][j] * design[1][j] for j in range(3))),
        (sum(design[1][j] * design[0][j] for j in range(3)), sum(design[1][j] * design[1][j] for j in range(3))),
    )
    alpha = solve_2x2(gram, (responses[0], responses[1]))
    min_norm = tuple(sum(design[i][j] * alpha[i] for i in range(2)) for j in range(3))
    cross = (
        design[0][1] * design[1][2] - design[0][2] * design[1][1],
        design[0][2] * design[1][0] - design[0][0] * design[1][2],
        design[0][0] * design[1][1] - design[0][1] * design[1][0],
    )
    cross_norm = math.sqrt(sum(value * value for value in cross))
    if cross_norm <= 1e-12:
        fail("design rows must be independent")
    null = tuple(value / cross_norm for value in cross)
    shifted = tuple(value + args.null_shift * direction for value, direction in zip(min_norm, null))
    train_residual = math.sqrt(sum(
        (sum(design[i][j] * min_norm[j] for j in range(3)) - responses[i]) ** 2
        for i in range(2)
    ))

    peak_index = max(range(len(risks)), key=risks.__getitem__)
    return TrackA(
        dimensions=dimensions, risks=tuple(risks), peak_dimension=dimensions[peak_index],
        peak_risk=risks[peak_index], tail_risk=risks[-1],
        min_norm=(min_norm[0], min_norm[1], min_norm[2]),
        min_norm_length=math.sqrt(sum(value * value for value in min_norm)),
        shifted_length=math.sqrt(sum(value * value for value in shifted)),
        train_residual=train_residual, null_test_gap=abs(args.null_shift),
    )


def compute_track_b(args: argparse.Namespace) -> TrackB:
    if args.rescale <= 0.0 or args.margin <= 0.0 or args.certificate_samples <= 0:
        fail("rescale, margin and certificate-samples must be positive")
    spectral = floats(args.layer_spectral, "layer-spectral")
    frobenius = floats(args.layer_frobenius, "layer-frobenius")
    if len(spectral) < 2 or len(spectral) != len(frobenius):
        fail("layer norm lists must have equal length at least two")
    if any(s <= 0.0 or f < s for s, f in zip(spectral, frobenius)):
        fail("each spectral norm must be positive and no larger than its Frobenius norm")

    stable_rank_sum = sum((f / s) ** 2 for s, f in zip(spectral, frobenius))
    spectral_product = math.prod(spectral)
    complexity = spectral_product * math.sqrt(stable_rank_sum)
    scaled_spectral = (spectral[0] * args.rescale, spectral[1] / args.rescale, *spectral[2:])
    scaled_frobenius = (frobenius[0] * args.rescale, frobenius[1] / args.rescale, *frobenius[2:])
    rescaled_complexity = math.prod(scaled_spectral) * math.sqrt(sum(
        (f / s) ** 2 for s, f in zip(scaled_spectral, scaled_frobenius)
    ))
    return TrackB(
        rescale=args.rescale, baseline_sharpness=2.0,
        rescaled_sharpness=args.rescale ** 2 + args.rescale ** -2,
        function_product=1.0, path_quantity=1.0,
        spectral_product=spectral_product, stable_rank_sum=stable_rank_sum,
        complexity=complexity,
        certificate=complexity / (args.margin * math.sqrt(args.certificate_samples)),
        rescaled_complexity=rescaled_complexity,
    )


def compute_track_c(args: argparse.Namespace) -> TrackC:
    if not -1.0 < args.kernel_rho < 1.0 or args.kernel_time < 0.0:
        fail("kernel-rho must lie in (-1,1) and kernel-time must be nonnegative")
    residual = floats(args.initial_residual, "initial-residual")
    if len(residual) != 2 or math.hypot(*residual) <= 0.0:
        fail("initial-residual must be a nonzero two-vector")
    lambda_plus = 1.0 + args.kernel_rho
    lambda_minus = 1.0 - args.kernel_rho
    plus = (residual[0] + residual[1]) / math.sqrt(2.0)
    minus = (residual[0] - residual[1]) / math.sqrt(2.0)
    plus_t = plus * math.exp(-lambda_plus * args.kernel_time)
    minus_t = minus * math.exp(-lambda_minus * args.kernel_time)
    final = ((plus_t + minus_t) / math.sqrt(2.0), (plus_t - minus_t) / math.sqrt(2.0))
    final_norm = math.hypot(*final)

    particle_a = floats(args.particle_a, "particle-a")
    particle_w = floats(args.particle_w, "particle-w")
    if len(particle_a) < 2 or len(particle_a) != len(particle_w):
        fail("particle lists must have equal length at least two")
    if args.particle_step <= 0.0:
        fail("particle-step must be positive")
    count = len(particle_a)
    prediction_before = sum(a * w for a, w in zip(particle_a, particle_w)) / count
    residual_scalar = prediction_before - args.particle_target
    next_a = tuple(a - args.particle_step * residual_scalar * w / count for a, w in zip(particle_a, particle_w))
    next_w = tuple(w - args.particle_step * residual_scalar * a / count for a, w in zip(particle_a, particle_w))
    prediction_after = sum(a * w for a, w in zip(next_a, next_w)) / count
    feature_before = sum(w * w for w in particle_w) / count
    feature_after = sum(w * w for w in next_w) / count
    ntk_before = sum(a * a + w * w for a, w in zip(particle_a, particle_w)) / (count * count)
    ntk_after = sum(a * a + w * w for a, w in zip(next_a, next_w)) / (count * count)
    feature_drift = abs(feature_after - feature_before) / max(feature_before, 1e-12)
    ntk_drift = abs(ntk_after - ntk_before) / max(ntk_before, 1e-12)
    regime = "feature-moving" if max(feature_drift, ntk_drift) >= 0.1 else "near-lazy"
    slow_energy = minus * minus
    total_energy = plus * plus + minus * minus
    return TrackC(
        lambda_plus=lambda_plus, lambda_minus=lambda_minus,
        residual_initial_norm=math.hypot(*residual), residual_final=(final[0], final[1]),
        residual_final_norm=final_norm, slow_mode_fraction=slow_energy / total_energy,
        particle_prediction_before=prediction_before, particle_prediction_after=prediction_after,
        feature_moment_before=feature_before, feature_moment_after=feature_after,
        relative_feature_drift=feature_drift, ntk_before=ntk_before, ntk_after=ntk_after,
        relative_ntk_drift=ntk_drift, regime=regime,
    )


def fmt(values: tuple[float, ...]) -> str:
    return ",".join(f"{value:.6f}" for value in values)


def stdout_lines(a: TrackA, b: TrackB, c: TrackC) -> tuple[str, str, str]:
    return (
        f"TRACK A dims={','.join(map(str, a.dimensions))} risks={fmt(a.risks)} peak_p={a.peak_dimension} "
        f"peak={a.peak_risk:.6f} tail={a.tail_risk:.6f} min_norm={fmt(a.min_norm)} "
        f"min_length={a.min_norm_length:.6f} shifted_length={a.shifted_length:.6f} "
        f"train_residual={a.train_residual:.6f} null_test_gap={a.null_test_gap:.6f}",
        f"TRACK B c={b.rescale:.6f} sharp_base={b.baseline_sharpness:.6f} "
        f"sharp_scaled={b.rescaled_sharpness:.6f} function_product={b.function_product:.6f} "
        f"path={b.path_quantity:.6f} spectral_product={b.spectral_product:.6f} "
        f"stable_rank_sum={b.stable_rank_sum:.6f} complexity={b.complexity:.6f} "
        f"certificate={b.certificate:.6f} complexity_scaled={b.rescaled_complexity:.6f}",
        f"TRACK C lambdas={c.lambda_plus:.6f},{c.lambda_minus:.6f} r0_norm={c.residual_initial_norm:.6f} "
        f"rt={fmt(c.residual_final)} rt_norm={c.residual_final_norm:.6f} slow_fraction={c.slow_mode_fraction:.6f} "
        f"particle_prediction={c.particle_prediction_before:.6f}->{c.particle_prediction_after:.6f} "
        f"feature_moment={c.feature_moment_before:.6f}->{c.feature_moment_after:.6f} "
        f"feature_drift={c.relative_feature_drift:.6f} ntk={c.ntk_before:.6f}->{c.ntk_after:.6f} "
        f"ntk_drift={c.relative_ntk_drift:.6f} regime={c.regime}",
    )


def svg_text(x: float, y: float, value: str, *, size: int = 18, fill: str = "#172033", weight: int = 500, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Arial,sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{html.escape(value)}</text>'
    )


def render_svg(a: TrackA, b: TrackB, c: TrackC, output: Path) -> None:
    width, height = 1500, 1040
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1500" height="1040" fill="#F7F4EE"/>',
        '<rect x="54" y="44" width="1392" height="84" rx="20" fill="#172033"/>',
        svg_text(82, 82, "DEEP-CUM-01 · three regimes, no universal slogan", size=27, fill="#FFFFFF", weight=700),
        svg_text(82, 110, "interpolation/selection · invariance/capacity · kernel/feature dynamics", size=17, fill="#CBD5E1"),
    ]
    panels = ((54, 154, "A", "interpolation risk + selected solution", "#2563EB"),
              (54, 424, "B", "parameterization stress test + norm certificate", "#7C3AED"),
              (54, 694, "C", "fixed-kernel modes + moving-feature diagnostic", "#059669"))
    for x, y, label, title, color in panels:
        parts.extend([
            f'<rect x="{x}" y="{y}" width="1392" height="242" rx="20" fill="#FFFFFF" stroke="#D7DCE5" stroke-width="2"/>',
            f'<circle cx="{x + 38}" cy="{y + 38}" r="22" fill="{color}"/>',
            svg_text(x + 38, y + 45, label, size=19, fill="#FFFFFF", weight=700, anchor="middle"),
            svg_text(x + 76, y + 45, title, size=22, weight=700),
        ])

    # Track A: log-scaled, clipped risk curve to preserve the threshold peak.
    chart_x, chart_y, chart_w, chart_h = 92, 226, 620, 126
    parts.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="12" fill="#EFF6FF"/>')
    log_x = [math.log(value) for value in a.dimensions]
    min_x, max_x = min(log_x), max(log_x)
    max_risk = max(a.risks)
    points = []
    for lx, risk in zip(log_x, a.risks):
        px = chart_x + 24 + (lx - min_x) / (max_x - min_x) * (chart_w - 48)
        py = chart_y + chart_h - 20 - risk / max_risk * (chart_h - 40)
        points.append((px, py))
    parts.append('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in points) + '" fill="none" stroke="#2563EB" stroke-width="4"/>')
    for (px, py), dimension in zip(points, a.dimensions):
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#2563EB"/>')
        if dimension in (a.dimensions[0], a.peak_dimension, a.dimensions[-1]):
            parts.append(svg_text(px, py - 11, f"p={dimension}", size=13, fill="#1D4ED8", anchor="middle"))
    parts.extend([
        svg_text(754, 233, f"peak risk = {a.peak_risk:.3f} at p={a.peak_dimension}", size=19, fill="#1D4ED8", weight=700),
        svg_text(754, 264, f"tail risk = {a.tail_risk:.3f}  (second descent != zero)", size=17),
        svg_text(754, 300, f"min-norm w = ({fmt(a.min_norm)})", size=17),
        svg_text(754, 330, f"same training fit, null test gap = {a.null_test_gap:.2f}", size=17),
        svg_text(754, 360, "interpolation != benign overfitting != algorithm choice", size=16, fill="#9A3412", weight=700),
    ])

    # Track B: reparameterization curve.
    chart_x, chart_y, chart_w, chart_h = 92, 496, 620, 126
    parts.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="12" fill="#F5F3FF"/>')
    scales = (0.25, 0.5, 1.0, 2.0, 4.0)
    sharp = tuple(scale * scale + scale ** -2 for scale in scales)
    points = []
    for index, value in enumerate(sharp):
        px = chart_x + 30 + index * (chart_w - 60) / (len(scales) - 1)
        py = chart_y + chart_h - 20 - value / max(sharp) * (chart_h - 38)
        points.append((px, py))
    parts.append('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in points) + '" fill="none" stroke="#7C3AED" stroke-width="4"/>')
    for (px, py), scale in zip(points, scales):
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#7C3AED"/>')
        parts.append(svg_text(px, chart_y + chart_h - 4, f"c={scale:g}", size=12, fill="#5B21B6", anchor="middle"))
    parts.extend([
        svg_text(754, 503, f"same f: ab=1; sharpness 2.000 -> {b.rescaled_sharpness:.3f}", size=19, fill="#6D28D9", weight=700),
        svg_text(754, 537, f"path quantity = {b.path_quantity:.3f} under reciprocal rescaling", size=17),
        svg_text(754, 571, f"spectral complexity = {b.complexity:.3f}", size=17),
        svg_text(754, 601, f"margin/sqrt(n) certificate scale = {b.certificate:.3f}", size=17),
        svg_text(754, 631, "raw sharpness correlation != invariant explanation", size=16, fill="#9A3412", weight=700),
    ])

    # Track C: kernel modal decay and particle movement summary.
    chart_x, chart_y, chart_w, chart_h = 92, 766, 620, 126
    parts.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="12" fill="#ECFDF5"/>')
    times = tuple(i * args_t for i, args_t in enumerate([0.5] * 7))
    for eigenvalue, color, label in ((c.lambda_plus, "#059669", "fast λ+"), (c.lambda_minus, "#D97706", "slow λ−")):
        points = []
        for index, time in enumerate(times):
            px = chart_x + 26 + index * (chart_w - 52) / (len(times) - 1)
            py = chart_y + 18 + (1.0 - math.exp(-eigenvalue * time)) * (chart_h - 42)
            points.append((px, py))
        parts.append('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in points) + f'" fill="none" stroke="{color}" stroke-width="4"/>')
        parts.append(svg_text(points[-1][0] - 4, points[-1][1] - 8, label, size=13, fill=color, anchor="end"))
    parts.extend([
        svg_text(754, 773, f"K eigenvalues = ({c.lambda_plus:.2f}, {c.lambda_minus:.2f})", size=19, fill="#047857", weight=700),
        svg_text(754, 807, f"||r(0)||={c.residual_initial_norm:.3f} -> ||r(t)||={c.residual_final_norm:.3f}", size=17),
        svg_text(754, 841, f"particle prediction {c.particle_prediction_before:.3f} -> {c.particle_prediction_after:.3f}", size=17),
        svg_text(754, 871, f"feature drift={c.relative_feature_drift:.3f}; NTK drift={c.relative_ntk_drift:.3f}; {c.regime}", size=17),
        svg_text(754, 901, "training dynamics != population generalization", size=16, fill="#9A3412", weight=700),
    ])

    parts.extend([
        '<rect x="54" y="956" width="1392" height="54" rx="16" fill="#172033"/>',
        svg_text(750, 980, "object · quantifier · invariance · regime · theorem · proxy · counterexample · open boundary", size=16, fill="#E2E8F0", weight=600, anchor="middle"),
        svg_text(750, 1001, "A curve is evidence about its fixture—not a universal law of deep learning.", size=14, fill="#94A3B8", anchor="middle"),
        '</svg>',
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--sample-size", type=int, default=CANONICAL["sample_size"])
    result.add_argument("--dimensions", default=CANONICAL["dimensions"])
    result.add_argument("--noise-variance", type=float, default=CANONICAL["noise_variance"])
    result.add_argument("--signal-norm-squared", type=float, default=CANONICAL["signal_norm_squared"])
    result.add_argument("--design", default=CANONICAL["design"])
    result.add_argument("--responses", default=CANONICAL["responses"])
    result.add_argument("--null-shift", type=float, default=CANONICAL["null_shift"])
    result.add_argument("--rescale", type=float, default=CANONICAL["rescale"])
    result.add_argument("--layer-spectral", default=CANONICAL["layer_spectral"])
    result.add_argument("--layer-frobenius", default=CANONICAL["layer_frobenius"])
    result.add_argument("--certificate-samples", type=int, default=CANONICAL["certificate_samples"])
    result.add_argument("--margin", type=float, default=CANONICAL["margin"])
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
        fail("noncanonical runs cannot overwrite the canonical SVG")
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
