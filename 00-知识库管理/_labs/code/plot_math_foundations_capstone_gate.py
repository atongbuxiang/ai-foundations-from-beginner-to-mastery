#!/usr/bin/env python3
"""Deterministic three-track computation gate for MATH-FND-CAP-01.

Only the Python standard library is used.  The script intentionally keeps the
three evidence layers separate: an analytic Gaussian ledger, exact quadratic
dynamics, and a finite circle-kernel discretization.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "00-知识库管理" / "_assets" / "plots" / "math-foundations" / "plot-math-foundations-capstone-gate-v2.svg"
DEFAULT_SEED = 20260820


def gaussian_track(
    variance_x: float,
    variance_y: float,
    observation_x: float,
    observation_y: float,
) -> list[dict[str, float]]:
    """Analytic linear-Gaussian information and posterior ledger."""
    rows = []
    signal_variance = (
        variance_x * observation_x**2 + variance_y * observation_y**2
    )
    sigma_c_norm_sq = (
        (variance_x * observation_x) ** 2
        + (variance_y * observation_y) ** 2
    )
    prior_trace = variance_x + variance_y
    prior_det = variance_x * variance_y
    for noise_variance in (0.1, 0.3, 1.0, 3.0, 10.0):
        total_variance = signal_variance + noise_variance
        rows.append(
            {
                "noise": noise_variance,
                "mi": 0.5 * math.log(total_variance / noise_variance),
                "posterior_trace": prior_trace - sigma_c_norm_sq / total_variance,
                "posterior_det": prior_det * noise_variance / total_variance,
            }
        )
    return rows


def quadratic_track(
    lambda_min: float,
    lambda_max: float,
    eta_values: tuple[float, float, float],
    flow_dt: float,
) -> tuple[dict[float, list[float]], list[float]]:
    """Gradient-descent error and matched gradient-flow error."""
    discrete: dict[float, list[float]] = {}
    for eta in eta_values:
        e1 = e2 = 1.0
        norms = []
        for _ in range(26):
            norms.append(math.hypot(e1, e2))
            e1 *= 1.0 - lambda_min * eta
            e2 *= 1.0 - lambda_max * eta
        discrete[eta] = norms
    flow = [
        math.hypot(
            math.exp(-lambda_min * flow_dt * k),
            math.exp(-lambda_max * flow_dt * k),
        )
        for k in range(26)
    ]
    return discrete, flow


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Small dense solve by partial-pivoted Gaussian elimination."""
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(aug[i][k]))
        if abs(aug[pivot][k]) < 1e-14:
            raise ArithmeticError("singular kernel system")
        aug[k], aug[pivot] = aug[pivot], aug[k]
        for i in range(k + 1, n):
            factor = aug[i][k] / aug[k][k]
            aug[i][k] = 0.0
            for j in range(k + 1, n + 1):
                aug[i][j] -= factor * aug[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))) / aug[i][i]
    return x


def target(
    theta: float,
    cos_frequency: int,
    sin_frequency: int,
    sin_amplitude: float,
) -> float:
    return (
        math.cos(float(cos_frequency) * theta)
        + sin_amplitude * math.sin(float(sin_frequency) * theta)
    )


def circle_kernel(theta: float, phi: float, lengthscale: float, radius: float) -> float:
    if radius == 1.0:
        chord_sq = 2.0 - 2.0 * math.cos(theta - phi)
    else:
        chord_sq = 2.0 * radius**2 * (1.0 - math.cos(theta - phi))
    return math.exp(-chord_sq / (2.0 * lengthscale * lengthscale))


def circle_kernel_track(
    radius: float,
    lengthscale: float,
    ridge: float,
    cos_frequency: int,
    sin_frequency: int,
    sin_amplitude: float,
    rotation: float,
) -> tuple[list[dict[str, float]], float, list[dict[str, float]]]:
    """Finite KRR on S1 plus rotation and retraction audits."""
    rows = []
    for n in (8, 12, 24, 48):
        theta = [2.0 * math.pi * i / n for i in range(n)]
        gram = [
            [circle_kernel(ti, tj, lengthscale, radius) for tj in theta]
            for ti in theta
        ]
        system = [[gram[i][j] + (ridge if i == j else 0.0) for j in range(n)] for i in range(n)]
        alpha = solve_linear(
            system,
            [target(ti, cos_frequency, sin_frequency, sin_amplitude) for ti in theta],
        )
        squared = 0.0
        for j in range(360):
            t = 2.0 * math.pi * (j + 0.5) / 360.0
            pred = sum(
                alpha[i] * circle_kernel(t, theta[i], lengthscale, radius)
                for i in range(n)
            )
            truth = target(t, cos_frequency, sin_frequency, sin_amplitude)
            squared += (pred - truth) ** 2
        # The Gram matrix is circulant on an equispaced circle, so its
        # eigenvalues are the real DFT of the first row.
        first = gram[0]
        eig = [
            sum(first[j] * math.cos(2.0 * math.pi * ell * j / n) for j in range(n))
            for ell in range(n)
        ]
        shifted = [max(value + ridge, ridge) for value in eig]
        rows.append(
            {
                "n": float(n),
                "rmse": math.sqrt(squared / 360.0),
                "min_gram_eigenvalue": min(eig),
                "condition": max(shifted) / min(shifted),
            }
        )

    theta = [2.0 * math.pi * i / 24 for i in range(24)]
    rotation_defect = max(
        abs(
            circle_kernel(a, b, lengthscale, radius)
            - circle_kernel(a + rotation, b + rotation, lengthscale, radius)
        )
        for a in theta
        for b in theta
    )

    retraction_rows = []
    for h in (0.3, 0.1, 0.03, 0.01):
        norm = math.sqrt(radius * radius + h * h)
        retract = (radius * radius / norm, radius * h / norm)
        exact_exp = (
            radius * math.cos(h / radius),
            radius * math.sin(h / radius),
        )
        error = math.hypot(retract[0] - exact_exp[0], retract[1] - exact_exp[1])
        retraction_rows.append({"h": h, "error": error})
    return rows, rotation_defect, retraction_rows


def svg_text(x: float, y: float, value: str, cls: str = "small", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def polyline(values: list[float], x0: float, y0: float, width: float, height: float,
             color: str, ymin: float | None = None, ymax: float | None = None) -> list[str]:
    lo = min(values) if ymin is None else ymin
    hi = max(values) if ymax is None else ymax
    span = max(hi - lo, 1e-15)
    points = []
    circles = []
    for i, value in enumerate(values):
        x = x0 + width * i / max(len(values) - 1, 1)
        y = y0 + height - height * (value - lo) / span
        points.append(f"{x:.1f},{y:.1f}")
        circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{color}"/>')
    return [f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.5"/>', *circles]


def make_svg(
    gaussian,
    discrete,
    flow,
    kernel_rows,
    rotation_defect,
    retraction_rows,
    config: dict[str, float | int],
) -> str:
    eta_values = (
        float(config["eta_conservative"]),
        float(config["eta_stable"]),
        float(config["eta_unstable"]),
    )
    canonical = (
        config["variance_x"] == 4.0
        and config["variance_y"] == 1.0
        and config["observation_x"] == 1.0
        and config["observation_y"] == 1.0
        and config["reference_noise"] == 1.0
        and config["lambda_min"] == 1.0
        and config["lambda_max"] == 9.0
        and eta_values == (0.10, 0.20, 0.24)
        and config["flow_dt"] == 0.2
        and config["circle_radius"] == 1.0
        and config["lengthscale"] == 0.65
        and config["ridge"] == 1e-3
        and config["target_cos_frequency"] == 2
        and config["target_sin_frequency"] == 3
        and config["target_sin_amplitude"] == 0.3
        and config["rotation"] == 0.37
    )
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480" role="img" aria-labelledby="title desc">',
        '<title id="title">数学基础十卷跨章累计复现门</title>',
        '<desc id="desc">三面板分别展示线性高斯信息账本、二次优化的连续与离散稳定，以及圆周上的核回归、旋转不变性和retraction误差。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.title{font-size:24px;font-weight:700;fill:#1F2937}.head{font-size:22px;font-weight:700;fill:#334155}.small{font-size:15px;fill:#64748B}.label{font-size:17px;fill:#334155}.card{fill:#FFFEFB;stroke:#D7DEE8;stroke-width:1.3}.axis{stroke:#64748B;stroke-width:1.1}.dash{stroke-dasharray:5 5}</style></defs>',
        '<rect width="1200" height="480" fill="#FFFFFF"/>',
        '<text x="40" y="39" class="title">MATH-FND-CAP-01：信息、优化动力与几何核方法的跨卷证据账</text>',
        '<rect x="28" y="59" width="368" height="390" class="card"/><rect x="416" y="59" width="368" height="390" class="card"/><rect x="804" y="59" width="368" height="390" class="card"/>',
        '<text x="50" y="89" class="head">A　Gaussian information</text>',
        '<text x="438" y="89" class="head">B　Discrete stability</text>',
        '<text x="826" y="89" class="head">C　Circle-kernel geometry</text>',
    ]

    # Track A: use separate fixed scales and label the two analytic quantities.
    x0, y0, width, height = 72.0, 124.0, 280.0, 145.0
    parts += [f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" class="axis"/>']
    mi_hi = 2.0 if canonical else max(row["mi"] for row in gaussian) * 1.05
    trace_hi = 5.0 if canonical else max(
        float(config["variance_x"]) + float(config["variance_y"]),
        max(row["posterior_trace"] for row in gaussian),
    ) * 1.05
    parts += polyline([row["mi"] for row in gaussian], x0, y0, width, height, "#7C3AED", 0.0, mi_hi)
    parts += polyline([row["posterior_trace"] for row in gaussian], x0, y0, width, height, "#16A34A", 0.0, trace_hi)
    mi_label = "purple: I(X;Z) [0,2] nats" if canonical else f"purple: I(X;Z) [0,{mi_hi:.2g}] nats"
    trace_label = "green: tr Cov(X|Z) [0,5]" if canonical else f"green: tr Cov(X|Z) [0,{trace_hi:.2g}]"
    parts += [svg_text(72, 294, mi_label, "label"), svg_text(72, 316, trace_label, "label")]
    reference_noise = float(config["reference_noise"])
    reference = next(row for row in gaussian if row["noise"] == reference_noise)
    reference_line = (
        f'R=1: I={reference["mi"]:.4f}, posterior trace={reference["posterior_trace"]:.4f}'
        if canonical
        else f'R={reference_noise:g}: I={reference["mi"]:.4f}, post tr={reference["posterior_trace"]:.4f}'
    )
    determinant_line = (
        f'posterior det={reference["posterior_det"]:.4f}; noise ↑ ⇒ information ↓'
        if canonical
        else f'Σ=diag({config["variance_x"]:g},{config["variance_y"]:g}), c=({config["observation_x"]:g},{config["observation_y"]:g})'
    )
    parts += [svg_text(50, 350, reference_line, "small"), svg_text(50, 375, determinant_line, "small"), svg_text(50, 402, "定理值 ≠ estimator；先验/噪声/方向必须分账", "small"), svg_text(50, 428, "x-axis noise variance: 0.1, 0.3, 1, 3, 10", "small")]

    # Track B: log error curves, with the Euler stability boundary made explicit.
    x0, y0, width, height = 458.0, 124.0, 280.0, 170.0
    all_logs = [math.log10(max(v, 1e-12)) for values in discrete.values() for v in values]
    all_logs += [math.log10(max(v, 1e-12)) for v in flow]
    ymin, ymax = min(all_logs), max(all_logs)
    colors = {
        eta_values[0]: "#2563EB",
        eta_values[1]: "#16A34A",
        eta_values[2]: "#DC2626",
    }
    for eta, values in discrete.items():
        parts += polyline([math.log10(max(v, 1e-12)) for v in values], x0, y0, width, height, colors[eta], ymin, ymax)
    parts += polyline([math.log10(max(v, 1e-12)) for v in flow], x0, y0, width, height, "#7C3AED", ymin, ymax)
    parts += [f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" class="axis"/>']
    legend = (
        "blue η=.10　green η=.20　red η=.24"
        if canonical
        else f"blue η={eta_values[0]:g}　green η={eta_values[1]:g}　red η={eta_values[2]:g}"
    )
    flow_label = (
        "purple: exact flow sampled at t=0.2k"
        if canonical
        else f"purple: exact flow at t={config['flow_dt']:g}k"
    )
    stability_label = (
        "stability: 0 &lt; η &lt; 2/9 ≈ .2222"
        if canonical
        else f"μ={config['lambda_min']:g}, L={config['lambda_max']:g}; η&lt;{2/float(config['lambda_max']):.4g}"
    )
    stable_line = (
        f'k=25: η=.20 error={discrete[eta_values[1]][-1]:.3g}'
        if canonical
        else f'k=25: stable η={eta_values[1]:g}, error={discrete[eta_values[1]][-1]:.3g}'
    )
    unstable_line = (
        f'k=25: η=.24 error={discrete[eta_values[2]][-1]:.3g} (diverges)'
        if canonical
        else f'k=25: probe η={eta_values[2]:g}, error={discrete[eta_values[2]][-1]:.3g}'
    )
    parts += [svg_text(458, 319, legend, "label"), svg_text(458, 342, flow_label, "small"), svg_text(438, 372, stability_label, "small"), svg_text(438, 398, stable_line, "small"), svg_text(438, 421, unstable_line, "small")]

    # Track C: KRR refinement plus invariant/geometric checks.
    x0, y0, width, height = 846.0, 124.0, 270.0, 145.0
    rmse_logs = [math.log10(max(row["rmse"], 1e-14)) for row in kernel_rows]
    parts += [f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" class="axis"/>']
    parts += polyline(rmse_logs, x0, y0, width, height, "#DB2777")
    parts += [svg_text(846, 294, "log10 test RMSE; n = 8, 12, 24, 48", "label")]
    last = kernel_rows[-1]
    h0, h1 = retraction_rows[0], retraction_rows[-1]
    first_c_line = (
        f'n=48: RMSE={last["rmse"]:.3g}, cond(K+λI)≈{last["condition"]:.3g}'
        if canonical
        else f'ρ={config["circle_radius"]:g}, ℓ={config["lengthscale"]:g}, λ={config["ridge"]:g}, n=48'
    )
    second_c_line = (
        f'finite Gram min eigenvalue={last["min_gram_eigenvalue"]:.2g}'
        if canonical
        else f'RMSE={last["rmse"]:.3g}, cond≈{last["condition"]:.3g}, min eig={last["min_gram_eigenvalue"]:.2g}'
    )
    rotation_line = (
        f'rotation-kernel defect={rotation_defect:.1e}'
        if canonical
        else f'target cos({config["target_cos_frequency"]:g}θ)+{config["target_sin_amplitude"]:g}sin({config["target_sin_frequency"]:g}θ); rot defect={rotation_defect:.1e}'
    )
    parts += [svg_text(826, 328, first_c_line, "small"), svg_text(826, 352, second_c_line, "small"), svg_text(826, 376, rotation_line, "small"), svg_text(826, 400, f'retraction−Exp: h={h0["h"]:.1f} → {h0["error"]:.2g}', "small"), svg_text(826, 422, f'h={h1["h"]:.2f} → {h1["error"]:.2g}; finite mesh ≠ operator theorem', "small"), '</svg>']
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variance-x", type=float, default=4.0)
    parser.add_argument("--variance-y", type=float, default=1.0)
    parser.add_argument("--observation-x", type=float, default=1.0)
    parser.add_argument("--observation-y", type=float, default=1.0)
    parser.add_argument("--reference-noise", type=float, default=1.0)
    parser.add_argument("--lambda-min", type=float, default=1.0)
    parser.add_argument("--lambda-max", type=float, default=9.0)
    parser.add_argument("--eta-conservative", type=float, default=0.10)
    parser.add_argument("--eta-stable", type=float, default=0.20)
    parser.add_argument("--eta-unstable", type=float, default=0.24)
    parser.add_argument("--flow-dt", type=float, default=0.20)
    parser.add_argument("--circle-radius", type=float, default=1.0)
    parser.add_argument("--lengthscale", type=float, default=0.65)
    parser.add_argument("--ridge", type=float, default=1e-3)
    parser.add_argument("--target-cos-frequency", type=int, default=2)
    parser.add_argument("--target-sin-frequency", type=int, default=3)
    parser.add_argument("--target-sin-amplitude", type=float, default=0.3)
    parser.add_argument("--rotation", type=float, default=0.37)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Reserved in the artifact contract; tracks are analytic/deterministic.")
    args = parser.parse_args()

    if args.variance_x <= 0.0 or args.variance_y <= 0.0:
        raise ValueError("Gaussian marginal variances must be positive")
    if args.observation_x == 0.0 and args.observation_y == 0.0:
        raise ValueError("the observation direction must be nonzero")
    if args.reference_noise not in (0.1, 0.3, 1.0, 3.0, 10.0):
        raise ValueError("--reference-noise must be one of 0.1, 0.3, 1, 3, 10")
    if not (0.0 < args.lambda_min < args.lambda_max):
        raise ValueError("require 0 < lambda-min < lambda-max")
    stability_threshold = 2.0 / args.lambda_max
    if not (
        0.0 < args.eta_conservative < stability_threshold
        and 0.0 < args.eta_stable < stability_threshold
        and args.eta_unstable > stability_threshold
    ):
        raise ValueError("require conservative/stable eta below 2/lambda-max and unstable eta above it")
    eta_values = (args.eta_conservative, args.eta_stable, args.eta_unstable)
    if len(set(eta_values)) != 3:
        raise ValueError("the three eta probes must be distinct")
    if args.flow_dt <= 0.0:
        raise ValueError("--flow-dt must be positive")
    if args.circle_radius <= 0.0 or args.lengthscale <= 0.0 or args.ridge <= 0.0:
        raise ValueError("circle radius, lengthscale and ridge must be positive")
    if args.target_cos_frequency < 0 or args.target_sin_frequency < 0:
        raise ValueError("target frequencies must be nonnegative integers")

    config: dict[str, float | int] = {
        "variance_x": args.variance_x,
        "variance_y": args.variance_y,
        "observation_x": args.observation_x,
        "observation_y": args.observation_y,
        "reference_noise": args.reference_noise,
        "lambda_min": args.lambda_min,
        "lambda_max": args.lambda_max,
        "eta_conservative": args.eta_conservative,
        "eta_stable": args.eta_stable,
        "eta_unstable": args.eta_unstable,
        "flow_dt": args.flow_dt,
        "circle_radius": args.circle_radius,
        "lengthscale": args.lengthscale,
        "ridge": args.ridge,
        "target_cos_frequency": args.target_cos_frequency,
        "target_sin_frequency": args.target_sin_frequency,
        "target_sin_amplitude": args.target_sin_amplitude,
        "rotation": args.rotation,
    }
    canonical = (
        args.seed == DEFAULT_SEED
        and args.variance_x == 4.0
        and args.variance_y == 1.0
        and args.observation_x == 1.0
        and args.observation_y == 1.0
        and args.reference_noise == 1.0
        and args.lambda_min == 1.0
        and args.lambda_max == 9.0
        and eta_values == (0.10, 0.20, 0.24)
        and args.flow_dt == 0.20
        and args.circle_radius == 1.0
        and args.lengthscale == 0.65
        and args.ridge == 1e-3
        and args.target_cos_frequency == 2
        and args.target_sin_frequency == 3
        and args.target_sin_amplitude == 0.3
        and args.rotation == 0.37
    )
    if not canonical and args.output is None:
        raise SystemExit(
            "noncanonical runs require --output so the canonical SVG is not overwritten"
        )

    gaussian = gaussian_track(
        args.variance_x,
        args.variance_y,
        args.observation_x,
        args.observation_y,
    )
    discrete, flow = quadratic_track(
        args.lambda_min,
        args.lambda_max,
        eta_values,
        args.flow_dt,
    )
    kernel_rows, rotation_defect, retraction_rows = circle_kernel_track(
        args.circle_radius,
        args.lengthscale,
        args.ridge,
        args.target_cos_frequency,
        args.target_sin_frequency,
        args.target_sin_amplitude,
        args.rotation,
    )
    if not all(gaussian[i]["mi"] > gaussian[i + 1]["mi"] for i in range(len(gaussian) - 1)):
        raise AssertionError("Gaussian mutual information should decrease with noise")
    if not discrete[args.eta_unstable][-1] > discrete[args.eta_stable][-1]:
        raise AssertionError("the step beyond the Euler stability threshold should diverge")
    if rotation_defect > 1e-12:
        raise AssertionError("the circle kernel must be rotation invariant")
    if not all(retraction_rows[i]["error"] > retraction_rows[i + 1]["error"] for i in range(len(retraction_rows) - 1)):
        raise AssertionError("retraction error should shrink with the tangent step")
    svg = make_svg(
        gaussian,
        discrete,
        flow,
        kernel_rows,
        rotation_defect,
        retraction_rows,
        config,
    )
    output = (args.output or DEFAULT_OUTPUT).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()

    signal_variance = (
        args.variance_x * args.observation_x**2
        + args.variance_y * args.observation_y**2
    )
    reference = next(row for row in gaussian if row["noise"] == args.reference_noise)
    print(
        f"A_CONFIG variance_x={args.variance_x:g} variance_y={args.variance_y:g} "
        f"observation_x={args.observation_x:g} observation_y={args.observation_y:g} "
        f"signal_variance={signal_variance:g} reference_noise={args.reference_noise:g}"
    )
    for row in gaussian:
        print(f"A_LEDGER noise={row['noise']:.3g} mi={row['mi']:.10g} posterior_trace={row['posterior_trace']:.10g} posterior_det={row['posterior_det']:.10g}")
    print(
        f"A_REFERENCE noise={args.reference_noise:g} mi={reference['mi']:.10g} "
        f"posterior_trace={reference['posterior_trace']:.10g} "
        f"posterior_det={reference['posterior_det']:.10g}"
    )
    print(
        f"B_CONFIG lambda_min={args.lambda_min:g} lambda_max={args.lambda_max:g} "
        f"stability_threshold={stability_threshold:.10g} "
        f"optimal_eta={2/(args.lambda_min + args.lambda_max):.10g} "
        f"optimal_rho={(args.lambda_max - args.lambda_min)/(args.lambda_max + args.lambda_min):.10g} "
        f"flow_dt={args.flow_dt:g}"
    )
    for eta, values in discrete.items():
        print(f"B_LEDGER eta={eta:g} multiplier=({1-args.lambda_min*eta:.6g},{1-args.lambda_max*eta:.6g}) error_k25={values[-1]:.10g}")
    print(f"B_FLOW error_k25={flow[-1]:.10g}")
    print(
        f"C_CONFIG circle_radius={args.circle_radius:g} lengthscale={args.lengthscale:g} "
        f"ridge={args.ridge:g} target_cos_frequency={args.target_cos_frequency} "
        f"target_sin_frequency={args.target_sin_frequency} "
        f"target_sin_amplitude={args.target_sin_amplitude:g} rotation={args.rotation:g}"
    )
    for row in kernel_rows:
        print(f"C_LEDGER n={int(row['n'])} rmse={row['rmse']:.10g} min_gram_eigenvalue={row['min_gram_eigenvalue']:.10g} condition={row['condition']:.10g}")
    print(f"C_ROTATION defect={rotation_defect:.10g}")
    for row in retraction_rows:
        print(f"C_RETRACTION h={row['h']:.3g} retraction_exp_error={row['error']:.10g}")
    print(f"SEED {args.seed} (reserved; no stochastic estimates in v2)")
    print(f"OUTPUT {output}")
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(0)
