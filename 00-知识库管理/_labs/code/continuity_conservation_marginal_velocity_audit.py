#!/usr/bin/env python3
"""Three deterministic audits for continuity equations and flow matching.

Track A: conservative periodic upwind transport.
Track B: analytic Gaussian compression, quadrature mass/moment/entropy checks.
Track C: conditional Gaussian interpolation and posterior-average velocity.

Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import random
from pathlib import Path


def initial_periodic_density(x: float) -> float:
    """Smooth, positive, one-periodic profile; normalization is handled discretely."""
    bump1 = math.exp(2.5 * math.cos(2.0 * math.pi * (x - 0.22)))
    bump2 = 0.45 * math.exp(4.0 * math.cos(2.0 * math.pi * (x - 0.68)))
    return 0.08 + bump1 + bump2


def normalized_cell_values(n: int) -> list[float]:
    dx = 1.0 / n
    values = [initial_periodic_density((i + 0.5) * dx) for i in range(n)]
    mass = dx * sum(values)
    return [value / mass for value in values]


def upwind_period(values: list[float], cfl: float) -> tuple[list[float], int]:
    n = len(values)
    # For the selected N and CFL=0.8, n/cfl is an integer and T=1 exactly.
    steps = round(n / cfl)
    assert abs(steps * cfl / n - 1.0) < 1e-14
    state = values[:]
    for _ in range(steps):
        state = [
            (1.0 - cfl) * state[i] + cfl * state[(i - 1) % n]
            for i in range(n)
        ]
    return state, steps


def l1_grid(a: list[float], b: list[float], dx: float) -> float:
    return dx * sum(abs(x - y) for x, y in zip(a, b))


def observed_orders(errors: list[float]) -> list[float]:
    return [math.log(errors[i] / errors[i + 1], 2.0) for i in range(len(errors) - 1)]


def gaussian_pdf(x: float, mean: float, variance: float) -> float:
    return math.exp(-0.5 * (x - mean) ** 2 / variance) / math.sqrt(2.0 * math.pi * variance)


def trapezoid(xs: list[float], ys: list[float]) -> float:
    return sum(0.5 * (ys[i] + ys[i + 1]) * (xs[i + 1] - xs[i]) for i in range(len(xs) - 1))


def compression_audit(kappa: float, times: list[float]) -> dict[str, object]:
    count = 8001
    left, right = -8.0, 8.0
    dx = (right - left) / (count - 1)
    xs = [left + i * dx for i in range(count)]
    profiles: list[list[float]] = []
    masses: list[float] = []
    variances: list[float] = []
    entropies: list[float] = []
    for t in times:
        variance = math.exp(-2.0 * kappa * t)
        rho = [gaussian_pdf(x, 0.0, variance) for x in xs]
        profiles.append(rho)
        masses.append(trapezoid(xs, rho))
        variances.append(trapezoid(xs, [x * x * p for x, p in zip(xs, rho)]))
        entropies.append(trapezoid(xs, [-p * math.log(p) if p > 0.0 else 0.0 for p in rho]))
    exact_variances = [math.exp(-2.0 * kappa * t) for t in times]
    h0 = 0.5 * math.log(2.0 * math.pi * math.e)
    exact_entropies = [h0 - kappa * t for t in times]
    assert max(abs(m - 1.0) for m in masses) < 2e-13
    assert max(abs(a - b) for a, b in zip(variances, exact_variances)) < 2e-12
    assert max(abs(a - b) for a, b in zip(entropies, exact_entropies)) < 2e-12
    return {
        "xs": xs,
        "profiles": profiles,
        "times": times,
        "masses": masses,
        "variances": variances,
        "exact_variances": exact_variances,
        "entropies": entropies,
        "exact_entropies": exact_entropies,
    }


def exact_marginal_velocity_parameters(
    t: float, sigma0: float, sigma1: float, mean1: float
) -> tuple[float, float, float, float, float]:
    mean_t = t * mean1
    variance_t = (1.0 - t) ** 2 * sigma0**2 + t * t * sigma1**2
    covariance = t * sigma1**2 - (1.0 - t) * sigma0**2
    slope = covariance / variance_t
    intercept = mean1 - slope * mean_t
    return mean_t, variance_t, covariance, intercept, slope


def cumulative_ols(
    counts: list[int], seed: int, t: float, sigma0: float, sigma1: float, mean1: float
) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    sx = su = sxx = sxu = 0.0
    results: list[tuple[float, float]] = []
    wanted = set(counts)
    for n in range(1, max(counts) + 1):
        x0 = rng.gauss(0.0, sigma0)
        x1 = rng.gauss(mean1, sigma1)
        x = (1.0 - t) * x0 + t * x1
        u = x1 - x0
        sx += x
        su += u
        sxx += x * x
        sxu += x * u
        if n in wanted:
            denom = sxx - sx * sx / n
            slope = (sxu - sx * su / n) / denom
            intercept = su / n - slope * sx / n
            results.append((intercept, slope))
    return results


def continuity_normalized_residual(
    x: float, t: float, sigma0: float, sigma1: float, mean1: float
) -> float:
    mean, variance, _cov, intercept, slope = exact_marginal_velocity_parameters(
        t, sigma0, sigma1, mean1
    )
    y = x - mean
    variance_prime = -2.0 * (1.0 - t) * sigma0**2 + 2.0 * t * sigma1**2
    mean_prime = mean1
    dt_logp = (
        -0.5 * variance_prime / variance
        + y * mean_prime / variance
        + 0.5 * y * y * variance_prime / (variance * variance)
    )
    velocity = intercept + slope * x
    dx_logp = -y / variance
    # (p_t + (pv)_x)/p = d_t log p + v d_x log p + d_x v.
    return dt_logp + velocity * dx_logp + slope


def svg_polyline(points: list[tuple[float, float]], css: str) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline class="{css}" points="{coords}"/>'


def build_svg(track_a: dict[str, object], track_b: dict[str, object], track_c: dict[str, object]) -> str:
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470" role="img" aria-labelledby="title desc">',
        '<title id="title">守恒通量、压缩密度与边缘速度三轨审计</title>',
        '<desc id="desc">周期迎风有限体积的质量守恒和一阶误差，线性压缩下高斯密度的峰值与熵变化，以及条件高斯插值的后验平均边缘速度。</desc>',
        '<defs><style>',
        'text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.panel{fill:#fffefb;stroke:#d6dee8;stroke-width:1.5}.title{font:700 22px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#0f172a}.label{font:500 17px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#475569}.small{font:500 15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#64748b}.math{font:600 17px Georgia,"Times New Roman",serif;fill:#1e293b}.axis{stroke:#64748b;stroke-width:1.2}.grid{stroke:#e2e8f0;stroke-width:1}.blue{fill:none;stroke:#2563eb;stroke-width:2.6}.orange{fill:none;stroke:#ea580c;stroke-width:2.6}.green{fill:none;stroke:#059669;stroke-width:2.6}.violet{fill:none;stroke:#7c3aed;stroke-width:2.3;stroke-dasharray:6 4}.dotb{fill:#2563eb}.doto{fill:#ea580c}.dotg{fill:#059669}.badge{fill:#ecfdf5;stroke:#10b981;stroke-width:1.2}',
        '</style></defs>',
        '<rect width="1200" height="470" fill="#fff"/>',
        '<text class="title" x="20" y="32">DYN-08 可复现实验：flux conservation → compression → marginal velocity</text>',
    ]
    panels = [(20, 55, 370, 385), (415, 55, 370, 385), (810, 55, 370, 385)]
    for x, y, w, h in panels:
        lines.append(f'<rect class="panel" x="{x}" y="{y}" width="{w}" height="{h}"/>')

    # A: error convergence and mass identity.
    lines += [
        '<text class="title" x="42" y="88">A　有限体积守恒阶</text>',
        '<line class="axis" x1="70" y1="350" x2="355" y2="350"/>',
        '<line class="axis" x1="70" y1="350" x2="70" y2="125"/>',
        '<text class="small" x="276" y="374">grid N (log2)</text>',
        '<text class="small" transform="translate(48 275) rotate(-90)">one-period L1 error (log10)</text>',
    ]
    ns = track_a["ns"]
    errors = track_a["errors"]
    logs = [math.log10(e) for e in errors]
    lo, hi = min(logs) - 0.2, max(logs) + 0.2
    pts = []
    for n, e in zip(ns, errors):
        px = 84 + (math.log(n, 2) - math.log(ns[0], 2)) / (math.log(ns[-1], 2) - math.log(ns[0], 2)) * 250
        py = 335 - (math.log10(e) - lo) / (hi - lo) * 190
        pts.append((px, py))
    lines.append(svg_polyline(pts, "blue"))
    for x, y in pts:
        lines.append(f'<circle class="dotb" cx="{x:.2f}" cy="{y:.2f}" r="4"/>')
    lines += [
        f'<text class="math" x="80" y="112">mass drift max = {track_a["mass_drift"]:.2e}</text>',
        f'<text class="math" x="80" y="400">last observed order = {track_a["orders"][-1]:.3f}</text>',
        f'<text class="label" x="80" y="423">min rho={track_a["minimum"]:.4f}; peak ratio={track_a["peak_ratio"]:.3f}</text>',
    ]

    # B: Gaussian compression profiles.
    lines += [
        '<text class="title" x="437" y="88">B　压缩流的质量与熵</text>',
        '<line class="axis" x1="455" y1="350" x2="760" y2="350"/>',
        '<line class="axis" x1="607" y1="350" x2="607" y2="120"/>',
        '<text class="small" x="735" y="373">x</text>',
        '<text class="small" transform="translate(440 235) rotate(-90)">density</text>',
    ]
    colors = ["blue", "green", "orange"]
    labels = []
    xs_full = track_b["xs"]
    for idx, (t, profile, css) in enumerate(zip(track_b["times"], track_b["profiles"], colors)):
        pts_b = []
        for j in range(0, len(xs_full), 20):
            x = xs_full[j]
            if -3.5 <= x <= 3.5:
                px = 607 + x / 3.5 * 145
                py = 350 - profile[j] / max(track_b["profiles"][-1]) * 205
                pts_b.append((px, py))
        lines.append(svg_polyline(pts_b, css))
        labels.append(f't={t:g}')
    lines += [
        '<text class="label" x="465" y="111">蓝 t=0　绿 t=0.5　橙 t=1</text>',
        f'<text class="math" x="462" y="399">mass max error={track_b["mass_error"]:.2e}</text>',
        f'<text class="label" x="462" y="423">var(t=1)={track_b["variances"][-1]:.5f}; h drop={track_b["entropy_drop"]:.3f}</text>',
    ]

    # C: exact vs estimated marginal velocity.
    lines += [
        '<text class="title" x="832" y="88">C　条件均值恢复边缘速度</text>',
        '<line class="axis" x1="850" y1="330" x2="1150" y2="330"/>',
        '<line class="axis" x1="980" y1="365" x2="980" y2="125"/>',
        '<text class="small" x="1135" y="353">x</text>',
        '<text class="small" transform="translate(830 235) rotate(-90)">velocity</text>',
    ]
    intercept = track_c["intercept"]
    slope = track_c["slope"]
    fit_intercept, fit_slope = track_c["fits"][-1]

    def velocity_points(b: float, a: float) -> list[tuple[float, float]]:
        result = []
        for k in range(81):
            x = -3.0 + 7.0 * k / 80.0
            v = b + a * x
            px = 980 + x / 4.0 * 150
            py = 330 - v / 4.5 * 155
            result.append((px, py))
        return result

    lines.append(svg_polyline(velocity_points(intercept, slope), "violet"))
    lines.append(svg_polyline(velocity_points(fit_intercept, fit_slope), "green"))
    lines += [
        '<text class="label" x="850" y="111">紫虚线：exact　绿：20k samples OLS</text>',
        f'<text class="math" x="848" y="386">exact v(x)={intercept:.4f} + ({slope:.4f}) x</text>',
        f'<text class="label" x="848" y="410">fit={fit_intercept:.4f} + ({fit_slope:.4f})x</text>',
        f'<text class="label" x="848" y="429">normalized PDE residual max={track_c["pde_residual"]:.2e}</text>',
        '<rect class="badge" x="970" y="445" width="180" height="18" rx="9"/>',
        '<text class="small" x="998" y="458">all assertions passed</text>',
        '</svg>',
    ]
    return "\n".join(lines) + "\n"


def run(output: Path) -> None:
    # Track A.
    ns = [40, 80, 160, 320]
    cfl = 0.8
    errors: list[float] = []
    drifts: list[float] = []
    minima: list[float] = []
    peak_ratios: list[float] = []
    for n in ns:
        initial = normalized_cell_values(n)
        final, _steps = upwind_period(initial, cfl)
        dx = 1.0 / n
        errors.append(l1_grid(final, initial, dx))
        drifts.append(abs(dx * sum(final) - dx * sum(initial)))
        minima.append(min(final))
        peak_ratios.append(max(final) / max(initial))
    orders = observed_orders(errors)
    assert max(drifts) < 2e-14
    assert min(minima) > 0.0
    assert min(orders[-2:]) > 0.85
    # Failure injection: CFL>1 can create a negative cell in one step.
    spike = [0.0, 1.0, 0.0, 0.0]
    bad_cfl = 1.2
    bad = [(1.0 - bad_cfl) * spike[i] + bad_cfl * spike[(i - 1) % 4] for i in range(4)]
    assert min(bad) < 0.0
    track_a: dict[str, object] = {
        "ns": ns,
        "errors": errors,
        "orders": orders,
        "mass_drift": max(drifts),
        "minimum": min(minima),
        "peak_ratio": peak_ratios[-1],
        "bad_minimum": min(bad),
    }

    # Track B.
    kappa = 0.8
    times = [0.0, 0.5, 1.0]
    track_b = compression_audit(kappa, times)
    track_b["mass_error"] = max(abs(m - 1.0) for m in track_b["masses"])
    track_b["entropy_drop"] = track_b["entropies"][0] - track_b["entropies"][-1]

    # Track C.
    t = 0.35
    sigma0, sigma1, mean1 = 1.0, 0.7, 2.0
    mean_t, variance_t, covariance, intercept, slope = exact_marginal_velocity_parameters(
        t, sigma0, sigma1, mean1
    )
    counts = [200, 1000, 5000, 20000]
    fits = cumulative_ols(counts, 20260819, t, sigma0, sigma1, mean1)
    final_intercept, final_slope = fits[-1]
    parameter_error = math.hypot(final_intercept - intercept, final_slope - slope)
    residuals = [
        abs(continuity_normalized_residual(-4.0 + 8.0 * i / 200.0, t, sigma0, sigma1, mean1))
        for i in range(201)
    ]
    pde_residual = max(residuals)
    assert parameter_error < 0.03
    assert pde_residual < 2e-14
    # Equal-variance midpoint cancellation from the analytic example.
    _m, _q, c_mid, b_mid, a_mid = exact_marginal_velocity_parameters(0.5, 1.0, 1.0, 2.0)
    assert abs(c_mid) < 1e-15 and abs(a_mid) < 1e-15 and abs(b_mid - 2.0) < 1e-15
    track_c: dict[str, object] = {
        "t": t,
        "mean": mean_t,
        "variance": variance_t,
        "covariance": covariance,
        "intercept": intercept,
        "slope": slope,
        "counts": counts,
        "fits": fits,
        "parameter_error": parameter_error,
        "pde_residual": pde_residual,
    }

    svg = build_svg(track_a, track_b, track_c)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print("TRACK A — PERIODIC CONSERVATIVE UPWIND")
    for n, error in zip(ns, errors):
        print(f"N={n:4d}  L1_error={error:.12e}")
    print("orders=" + ",".join(f"{value:.8f}" for value in orders))
    print(f"mass_drift_max={max(drifts):.3e}  min_rho={min(minima):.8f}  peak_ratio_N320={peak_ratios[-1]:.8f}")
    print(f"failure_injection_CFL1.2_min={min(bad):.8f}")
    print("TRACK B — GAUSSIAN COMPRESSION")
    for t_value, mass, variance, entropy in zip(times, track_b["masses"], track_b["variances"], track_b["entropies"]):
        print(f"t={t_value:.1f}  mass={mass:.12f}  variance={variance:.12f}  entropy={entropy:.12f}")
    print("TRACK C — CONDITIONAL TO MARGINAL VELOCITY")
    print(f"mean_t={mean_t:.8f} variance_t={variance_t:.8f} covariance={covariance:.8f}")
    print(f"exact_intercept={intercept:.8f} exact_slope={slope:.8f}")
    for count, (b_fit, a_fit) in zip(counts, fits):
        print(f"samples={count:5d}  fit_intercept={b_fit:.8f}  fit_slope={a_fit:.8f}")
    print(f"final_parameter_error={parameter_error:.8e}  normalized_PDE_residual_max={pde_residual:.3e}")
    print(f"SVG={output}")
    print(f"SHA256={digest}")
    print("ALL ASSERTIONS PASSED")


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    default = root / "00-知识库管理/_assets/plots/dynamics/plot-continuity-conservation-marginal-velocity-v2.svg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=default)
    args = parser.parse_args()
    run(args.output.resolve())


if __name__ == "__main__":
    main()
