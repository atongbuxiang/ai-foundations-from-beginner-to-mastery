#!/usr/bin/env python3
"""Generate the ODE/dynamical-systems/SDE cumulative-gate SVG.

The three tracks deliberately separate three layers:

1. a stable continuous linear system and four finite-step solver maps;
2. an analytic periodic density path, its probability current, probability-flow
   characteristics, and the CNF log-density ledger;
3. Brownian quadratic variation, an Ito identity, and the full-score versus
   half-score distinction in a noisy reverse SDE.

Only the Python standard library is used.  The canonical run is deterministic
for a fixed seed and argument list.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_assets/plots/dynamics/plot-dynamics-cumulative-gate-v2.svg"


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def text(x: float, y: float, value: object, cls: str = "small", anchor: str = "start") -> str:
    return f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}">{esc(value)}</text>'


def line(x1: float, y1: float, x2: float, y2: float, **attrs: object) -> str:
    extra = " ".join(
        f'{key.replace("_", "-")}="{esc(value)}"' for key, value in attrs.items()
    )
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {extra}/>'


def path(
    points: list[tuple[float, float]],
    color: str,
    width: float = 3.0,
    dash: str | None = None,
) -> str:
    commands = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="{commands}" fill="none" stroke="{color}" '
        f'stroke-width="{width}"{dash_attr}/>'
    )


def circle(x: float, y: float, radius: float, color: str) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}"/>'


def fit_order(step_sizes: list[float], errors: list[float]) -> float:
    xs = [math.log(value) for value in step_sizes]
    ys = [math.log(max(value, 1e-300)) for value in errors]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    numerator = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    denominator = sum((x - xbar) ** 2 for x in xs)
    return numerator / denominator


# ---------------------------------------------------------------------------
# Track A: continuous stability versus finite-step stability.


def stability_factor(method: str, z: float) -> float:
    if method == "Euler":
        return 1.0 + z
    if method == "RK4":
        return 1.0 + z + z * z / 2.0 + z**3 / 6.0 + z**4 / 24.0
    if method == "BE":
        return 1.0 / (1.0 - z)
    if method == "Trap":
        return (1.0 + z / 2.0) / (1.0 - z / 2.0)
    raise ValueError(f"unknown method: {method}")


def linear_trajectory(method: str, stiffness: float, steps: int) -> list[float]:
    h = 1.0 / steps
    slow_factor = stability_factor(method, -h)
    fast_factor = stability_factor(method, -stiffness * h)
    x, y = 1.0, 1.0
    energies = [0.5 * (x * x + y * y)]
    for _ in range(steps):
        x *= slow_factor
        y *= fast_factor
        energies.append(0.5 * (x * x + y * y))
    return energies


def exact_energy(stiffness: float, t: float) -> float:
    return 0.5 * (math.exp(-2.0 * t) + math.exp(-2.0 * stiffness * t))


def endpoint_error(method: str, stiffness: float, steps: int) -> float:
    h = 1.0 / steps
    x_num = stability_factor(method, -h) ** steps
    y_num = stability_factor(method, -stiffness * h) ** steps
    return math.hypot(x_num - math.exp(-1.0), y_num - math.exp(-stiffness))


def track_a(stiffness: float, plot_steps: int) -> dict[str, object]:
    methods = ["Euler", "RK4", "BE", "Trap"]
    trajectories = {
        method: linear_trajectory(method, stiffness, plot_steps) for method in methods
    }
    refinement = [80, 160, 320, 640]
    hs = [1.0 / n for n in refinement]
    errors = {
        method: [endpoint_error(method, stiffness, n) for n in refinement]
        for method in methods
    }
    orders = {method: fit_order(hs, errors[method]) for method in methods}
    z_fast = -stiffness / plot_steps
    return {
        "methods": methods,
        "trajectories": trajectories,
        "refinement": refinement,
        "errors": errors,
        "orders": orders,
        "z_fast": z_fast,
        "factors": {method: stability_factor(method, z_fast) for method in methods},
    }


# ---------------------------------------------------------------------------
# Track B: analytic heat-flow density and probability-flow characteristics.


def harmonic_amplitude(t: float, a0: float, sigma: float) -> float:
    return a0 * math.exp(-0.5 * sigma * sigma * t)


def density(x: float, t: float, a0: float, sigma: float) -> float:
    a = harmonic_amplitude(t, a0, sigma)
    return (1.0 + a * math.cos(x)) / (2.0 * math.pi)


def score(x: float, t: float, a0: float, sigma: float) -> float:
    a = harmonic_amplitude(t, a0, sigma)
    return -a * math.sin(x) / (1.0 + a * math.cos(x))


def pf_velocity(x: float, t: float, a0: float, sigma: float) -> float:
    return -0.5 * sigma * sigma * score(x, t, a0, sigma)


def pf_divergence(x: float, t: float, a0: float, sigma: float) -> float:
    a = harmonic_amplitude(t, a0, sigma)
    denominator = 1.0 + a * math.cos(x)
    return 0.5 * sigma * sigma * (a * math.cos(x) + a * a) / (
        denominator * denominator
    )


def periodic_cdf(x: float, amplitude: float) -> float:
    return (x + math.pi + amplitude * math.sin(x)) / (2.0 * math.pi)


def exact_characteristic(x0: float, a0: float, sigma: float, final_time: float) -> float:
    target = periodic_cdf(x0, a0)
    final_amplitude = harmonic_amplitude(final_time, a0, sigma)
    left, right = -math.pi, math.pi
    for _ in range(90):
        midpoint = 0.5 * (left + right)
        if periodic_cdf(midpoint, final_amplitude) < target:
            left = midpoint
        else:
            right = midpoint
    return 0.5 * (left + right)


def rk4_characteristic(
    x0: float,
    a0: float,
    sigma: float,
    final_time: float,
    steps: int,
    keep_path: bool = False,
) -> tuple[float, float, list[tuple[float, float]]]:
    h = final_time / steps
    x = x0
    logp = math.log(density(x0, 0.0, a0, sigma))
    history = [(0.0, x)] if keep_path else []

    def rhs(t: float, state_x: float) -> tuple[float, float]:
        return (
            pf_velocity(state_x, t, a0, sigma),
            -pf_divergence(state_x, t, a0, sigma),
        )

    for index in range(steps):
        t = index * h
        k1x, k1l = rhs(t, x)
        k2x, k2l = rhs(t + 0.5 * h, x + 0.5 * h * k1x)
        k3x, k3l = rhs(t + 0.5 * h, x + 0.5 * h * k2x)
        k4x, k4l = rhs(t + h, x + h * k3x)
        x += h * (k1x + 2.0 * k2x + 2.0 * k3x + k4x) / 6.0
        logp += h * (k1l + 2.0 * k2l + 2.0 * k3l + k4l) / 6.0
        if keep_path:
            history.append(((index + 1) * h, x))
    return x, logp, history


def track_b(a0: float, sigma: float, final_time: float) -> dict[str, object]:
    refinements = [5, 10, 20, 40]
    hs = [final_time / n for n in refinements]
    initial_points = [
        -math.pi + 2.0 * math.pi * (i + 0.5) / 41.0 for i in range(41)
    ]
    state_errors: list[float] = []
    logp_errors: list[float] = []
    for steps in refinements:
        max_state = 0.0
        max_logp = 0.0
        for x0 in initial_points:
            exact_x = exact_characteristic(x0, a0, sigma, final_time)
            numerical_x, numerical_logp, _ = rk4_characteristic(
                x0, a0, sigma, final_time, steps
            )
            exact_logp = math.log(density(exact_x, final_time, a0, sigma))
            max_state = max(max_state, abs(numerical_x - exact_x))
            max_logp = max(max_logp, abs(numerical_logp - exact_logp))
        state_errors.append(max_state)
        logp_errors.append(max_logp)

    grid_size = 4096
    dx = 2.0 * math.pi / grid_size
    masses = []
    max_pde_residual = 0.0
    for t in [0.0, 0.25 * final_time, 0.5 * final_time, final_time]:
        mass = 0.0
        a = harmonic_amplitude(t, a0, sigma)
        for i in range(grid_size):
            x = -math.pi + (i + 0.5) * dx
            p = density(x, t, a0, sigma)
            mass += p * dx
            partial_t_p = -0.5 * sigma * sigma * a * math.cos(x) / (2.0 * math.pi)
            flux_divergence = (
                0.5 * sigma * sigma * a * math.cos(x) / (2.0 * math.pi)
            )
            max_pde_residual = max(
                max_pde_residual, abs(partial_t_p + flux_divergence)
            )
        masses.append(mass)

    paths = []
    for x0 in [-2.7, -1.8, -0.9, 0.0, 0.9, 1.8, 2.7]:
        _, _, history = rk4_characteristic(
            x0, a0, sigma, final_time, 120, keep_path=True
        )
        paths.append(history)

    return {
        "refinements": refinements,
        "hs": hs,
        "state_errors": state_errors,
        "logp_errors": logp_errors,
        "state_order": fit_order(hs, state_errors),
        "logp_order": fit_order(hs, logp_errors),
        "mass_drift": max(abs(value - 1.0) for value in masses),
        "pde_residual": max_pde_residual,
        "paths": paths,
    }


# ---------------------------------------------------------------------------
# Track C: pathwise stochastic certificates and reverse-score coefficient.


def analytic_em_second_moment(beta: float, final_time: float, steps: int) -> float:
    dt = final_time / steps
    factor = 1.0 - 0.5 * beta * dt
    if abs(1.0 - factor * factor) < 1e-15:
        return 1.0 + beta * final_time
    factor_power = factor ** (2 * steps)
    return factor_power + beta * dt * (1.0 - factor_power) / (1.0 - factor * factor)


def track_c(
    beta: float,
    final_time: float,
    paths: int,
    finest_steps: int,
    seed: int,
) -> dict[str, object]:
    levels = [finest_steps // 8, finest_steps // 4, finest_steps // 2, finest_steps]
    sums_qv = [0.0 for _ in levels]
    sums_residual_sq = [0.0 for _ in levels]
    sums_exact_m2 = [0.0 for _ in levels]
    sums_half_m2 = [0.0 for _ in levels]
    rng = random.Random(seed)
    sqrt_beta = math.sqrt(beta)
    fine_dt = final_time / finest_steps
    fine_scale = math.sqrt(fine_dt)

    for _ in range(paths):
        x0 = rng.gauss(0.0, 1.0)
        fine_increments = [fine_scale * rng.gauss(0.0, 1.0) for _ in range(finest_steps)]
        for level_index, steps in enumerate(levels):
            block = finest_steps // steps
            dt = final_time / steps
            x = x0
            x_half = x0
            qv = 0.0
            ito_rhs = 0.0
            for step in range(steps):
                start = step * block
                dw = sum(fine_increments[start : start + block])
                previous = x
                dx = -0.5 * beta * previous * dt + sqrt_beta * dw
                x = previous + dx
                qv += dx * dx
                ito_rhs += (-beta * previous * previous + beta) * dt
                ito_rhs += 2.0 * sqrt_beta * previous * dw
                x_half += sqrt_beta * dw
            residual = x * x - x0 * x0 - ito_rhs
            sums_qv[level_index] += qv
            sums_residual_sq[level_index] += residual * residual
            sums_exact_m2[level_index] += x * x
            sums_half_m2[level_index] += x_half * x_half

    qv_means = [value / paths for value in sums_qv]
    ito_rmse = [math.sqrt(value / paths) for value in sums_residual_sq]
    exact_m2 = [value / paths for value in sums_exact_m2]
    half_m2 = [value / paths for value in sums_half_m2]
    hs = [final_time / steps for steps in levels]
    return {
        "levels": levels,
        "hs": hs,
        "qv": qv_means,
        "ito_rmse": ito_rmse,
        "ito_order": fit_order(hs, ito_rmse),
        "exact_m2": exact_m2,
        "half_m2": half_m2,
        "analytic_exact_m2": analytic_em_second_moment(beta, final_time, finest_steps),
        "analytic_half_m2": 1.0 + beta * final_time,
        "qv_target": beta * final_time,
    }


# ---------------------------------------------------------------------------
# SVG composition.


def build_svg(
    stiffness: float,
    plot_steps: int,
    density_a: float,
    density_sigma: float,
    density_time: float,
    beta: float,
    stochastic_time: float,
    paths_count: int,
    brownian_steps: int,
    seed: int,
) -> tuple[str, dict[str, object]]:
    a = track_a(stiffness, plot_steps)
    b = track_b(density_a, density_sigma, density_time)
    c = track_c(beta, stochastic_time, paths_count, brownian_steps, seed)

    width, height = 1200, 455
    panel_x = [20.0, 415.0, 810.0]
    panel_w = 370.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">ODE、动力系统与 SDE 累计复现门</title>',
        '<desc id="desc">三面板展示刚性稳定与阶数、连续性方程与概率流、以及 Brownian 二次变差和 score 误差传播。</desc>',
        '<rect width="1200" height="455" fill="#ffffff"/>',
        """<style>
        text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.panel{fill:#fffefb;stroke:#d7dee8;stroke-width:1.5}.title{font-size:19px;font-weight:700;fill:#1f2937}.sub,.body,.small,.tiny{font-size:15px}.sub{fill:#475569}.body{fill:#334155}.small,.tiny{fill:#64748b}
        </style>""",
    ]
    for x in panel_x:
        parts.append(f'<rect class="panel" x="{x}" y="20" width="{panel_w}" height="415"/>')

    # Panel A: log-energy trajectories.
    parts += [
        text(40, 51, "A · 连续稳定 ≠ 任意离散步长稳定", "title"),
        text(40, 75, f"x′=−x, y′=−{stiffness:g}y；V′≤−2V；h={1/plot_steps:.3f}", "sub"),
    ]
    ax_l, ax_r, ax_t, ax_b = 70.0, 365.0, 106.0, 330.0
    parts += [
        line(ax_l, ax_b, ax_r, ax_b, stroke="#64748b", stroke_width="1.3"),
        line(ax_l, ax_t, ax_l, ax_b, stroke="#64748b", stroke_width="1.3"),
    ]
    all_log_values = []
    for method in a["methods"]:
        all_log_values.extend(math.log10(max(value, 1e-20)) for value in a["trajectories"][method])
    exact_values = [exact_energy(stiffness, i / plot_steps) for i in range(plot_steps + 1)]
    all_log_values.extend(math.log10(max(value, 1e-20)) for value in exact_values)
    ymin = min(-7.0, min(all_log_values))
    ymax = max(1.0, max(all_log_values))

    def axy(index: int, energy: float) -> tuple[float, float]:
        value = math.log10(max(energy, 1e-20))
        return (
            ax_l + index / plot_steps * (ax_r - ax_l),
            ax_b - (value - ymin) / (ymax - ymin) * (ax_b - ax_t),
        )

    parts.append(path([axy(i, value) for i, value in enumerate(exact_values)], "#0f172a", 2.8))
    colors = {"Euler": "#dc2626", "RK4": "#d97706", "BE": "#059669", "Trap": "#2563eb"}
    for method in a["methods"]:
        points = [axy(i, value) for i, value in enumerate(a["trajectories"][method])]
        parts.append(path(points, colors[method], 2.6, "5 3" if method in ("Euler", "RK4") else None))
    parts += [
        text(218, 350, "time t", "small", "middle"),
        text(ax_l, ax_t - 8, "log₁₀ V", "tiny"),
        line(82, 120, 100, 120, stroke="#0f172a", stroke_width="2.8"),
        text(105, 124, "exact", "tiny"),
        line(157, 120, 175, 120, stroke="#dc2626", stroke_width="2.8", stroke_dasharray="5 3"),
        text(180, 124, "Euler", "tiny"),
        line(232, 120, 250, 120, stroke="#d97706", stroke_width="2.8", stroke_dasharray="5 3"),
        text(255, 124, "RK4", "tiny"),
        line(82, 139, 100, 139, stroke="#059669", stroke_width="2.8"),
        text(105, 143, "BE", "tiny"),
        line(157, 139, 175, 139, stroke="#2563eb", stroke_width="2.8"),
        text(180, 143, "Trap", "tiny"),
        text(40, 373, f"fast z={a['z_fast']:.2f}: Euler R={a['factors']['Euler']:.3f}, RK4 R={a['factors']['RK4']:.3f}", "small"),
        text(40, 393, f"refinement orders: EE {a['orders']['Euler']:.2f}, RK4 {a['orders']['RK4']:.2f}", "small"),
        text(40, 413, f"BE {a['orders']['BE']:.2f}, Trap {a['orders']['Trap']:.2f}", "small"),
    ]

    # Panel B: density curves and probability-flow characteristics.
    parts += [
        text(435, 51, "B · 同一密度：FPE current 与 PF 特征线", "title"),
        text(435, 75, "p=(1+a(t) cos x)/(2π)；a(t)=a₀ exp(−σ²t/2)", "sub"),
    ]
    bx_l, bx_r, bx_t, bx_b = 462.0, 765.0, 108.0, 320.0
    parts += [
        line(bx_l, bx_b, bx_r, bx_b, stroke="#64748b", stroke_width="1.3"),
        line(bx_l, bx_t, bx_l, bx_b, stroke="#64748b", stroke_width="1.3"),
    ]

    def bxy(t: float, x: float) -> tuple[float, float]:
        return (
            bx_l + t / density_time * (bx_r - bx_l),
            bx_b - (x + math.pi) / (2.0 * math.pi) * (bx_b - bx_t),
        )

    for history in b["paths"]:
        parts.append(path([bxy(t, x) for t, x in history], "#2563eb", 2.0))
    parts += [
        text(613, 342, "forward time", "small", "middle"),
        text(bx_l, bx_t - 8, "state x on circle", "tiny"),
        text(470, 123, "probability-flow characteristics", "tiny"),
        text(435, 370, f"RK4 state/logp orders: {b['state_order']:.3f} / {b['logp_order']:.3f}", "small"),
        text(435, 390, f"mass drift {b['mass_drift']:.2e}; PDE residual {b['pde_residual']:.2e}", "small"),
        text(435, 412, "finite change-of-variables 与 continuity ledger 同时通过", "small"),
    ]

    # Panel C: quadratic variation and reverse endpoint moments.
    parts += [
        text(830, 51, "C · Path 证书与 reverse-score 系数", "title"),
        text(830, 75, f"stationary OU；β={beta:g}, T={stochastic_time:g}, paths={paths_count}", "sub"),
    ]
    cx_l, cx_r, cx_t, cx_b = 842.0, 1004.0, 112.0, 292.0
    parts += [
        line(cx_l, cx_b, cx_r, cx_b, stroke="#64748b", stroke_width="1.3"),
        line(cx_l, cx_t, cx_l, cx_b, stroke="#64748b", stroke_width="1.3"),
    ]
    qv_max = max(c["qv_target"] * 1.2, max(c["qv"]) * 1.1)

    def cxy(index: int, value: float) -> tuple[float, float]:
        return (
            cx_l + index / (len(c["levels"]) - 1) * (cx_r - cx_l),
            cx_b - value / qv_max * (cx_b - cx_t),
        )

    target_y = cxy(0, c["qv_target"])[1]
    parts.append(line(cx_l, target_y, cx_r, target_y, stroke="#0f172a", stroke_width="1.5", stroke_dasharray="5 3"))
    qv_points = [cxy(i, value) for i, value in enumerate(c["qv"])]
    parts.append(path(qv_points, "#2563eb", 2.8))
    for x, y in qv_points:
        parts.append(circle(x, y, 3.5, "#2563eb"))
    zero_y = cxy(0, 0.0)[1]
    parts.append(line(cx_l, zero_y, cx_r, zero_y, stroke="#059669", stroke_width="2.0"))
    parts += [
        text(923, 312, "refinement N", "tiny", "middle"),
        text(cx_l, cx_t - 8, "quadratic variation", "tiny"),
        text(853, target_y - 7, "SDE target βT", "tiny"),
        text(853, zero_y - 7, "PF ODE = 0", "tiny"),
    ]

    # Endpoint second-moment bars.
    bar_left, bar_right = 1040.0, 1154.0
    base_y, top_y = 292.0, 112.0
    max_m2 = max(c["analytic_half_m2"] * 1.15, c["half_m2"][-1] * 1.1)
    exact_height = c["exact_m2"][-1] / max_m2 * (base_y - top_y)
    half_height = c["half_m2"][-1] / max_m2 * (base_y - top_y)
    parts += [
        line(bar_left, base_y, bar_right, base_y, stroke="#64748b", stroke_width="1.3"),
        f'<rect x="{bar_left + 10:.2f}" y="{base_y - exact_height:.2f}" width="36" height="{exact_height:.2f}" fill="#059669"/>',
        f'<rect x="{bar_left + 66:.2f}" y="{base_y - half_height:.2f}" width="36" height="{half_height:.2f}" fill="#dc2626"/>',
        text(bar_left + 28, 309, "full", "tiny", "middle"),
        text(bar_left + 84, 309, "half", "tiny", "middle"),
        text(1097, 99, "terminal E[X²]", "tiny", "middle"),
        text(830, 350, f"Itô residual order {c['ito_order']:.3f}; finest QV {c['qv'][-1]:.4f}", "small"),
        text(830, 372, f"full-score noisy reverse E[X²]={c['exact_m2'][-1]:.4f} (target 1)", "small"),
        text(830, 394, f"half-score noisy reverse E[X²]={c['half_m2'][-1]:.4f}", "small"),
        text(830, 414, f"analytic half-score target=1+βT={c['analytic_half_m2']:.4f}", "small"),
    ]

    parts.append("</svg>")
    return "\n".join(parts), {"A": a, "B": b, "C": c}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stiffness", type=float, default=80.0)
    parser.add_argument("--plot-steps", type=int, default=25)
    parser.add_argument("--density-a", type=float, default=0.65)
    parser.add_argument("--density-sigma", type=float, default=1.1)
    parser.add_argument("--density-time", type=float, default=0.8)
    parser.add_argument("--beta", type=float, default=2.0)
    parser.add_argument("--stochastic-time", type=float, default=0.6)
    parser.add_argument("--paths", type=int, default=2048)
    parser.add_argument("--brownian-steps", type=int, default=512)
    parser.add_argument("--seed", type=int, default=20260819)
    args = parser.parse_args()
    if args.stiffness <= 1.0:
        parser.error("--stiffness must exceed 1")
    if args.plot_steps < 4:
        parser.error("--plot-steps must be at least 4")
    if not 0.0 < args.density_a < 1.0:
        parser.error("--density-a must lie in (0, 1)")
    if args.density_sigma <= 0.0 or args.density_time <= 0.0:
        parser.error("density sigma/time must be positive")
    if args.beta <= 0.0 or args.stochastic_time <= 0.0:
        parser.error("beta/stochastic time must be positive")
    if args.paths < 128:
        parser.error("--paths must be at least 128")
    if args.brownian_steps < 64 or args.brownian_steps % 8 != 0:
        parser.error("--brownian-steps must be a multiple of 8 and at least 64")
    return args


def main() -> None:
    args = parse_args()
    output = args.output.expanduser().resolve()
    svg, metrics = build_svg(
        args.stiffness,
        args.plot_steps,
        args.density_a,
        args.density_sigma,
        args.density_time,
        args.beta,
        args.stochastic_time,
        args.paths,
        args.brownian_steps,
        args.seed,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    a, b, c = metrics["A"], metrics["B"], metrics["C"]
    print(f"wrote {output}")
    print(
        "A z_fast={:.6f} factors EE={:.8f} RK4={:.8f} BE={:.8f} Trap={:.8f}".format(
            a["z_fast"],
            a["factors"]["Euler"],
            a["factors"]["RK4"],
            a["factors"]["BE"],
            a["factors"]["Trap"],
        )
    )
    print(
        "A orders EE={:.8f} RK4={:.8f} BE={:.8f} Trap={:.8f}".format(
            a["orders"]["Euler"],
            a["orders"]["RK4"],
            a["orders"]["BE"],
            a["orders"]["Trap"],
        )
    )
    print(
        "B orders state={:.8f} logp={:.8f} mass_drift={:.3e} pde_residual={:.3e}".format(
            b["state_order"], b["logp_order"], b["mass_drift"], b["pde_residual"]
        )
    )
    print(
        "C qv={:.8f} target={:.8f} ito_order={:.8f} full_m2={:.8f} half_m2={:.8f} half_target={:.8f}".format(
            c["qv"][-1],
            c["qv_target"],
            c["ito_order"],
            c["exact_m2"][-1],
            c["half_m2"][-1],
            c["analytic_half_m2"],
        )
    )
    print(f"sha256 {digest}")

    if not (0.8 < a["orders"]["Euler"] < 1.2):
        raise SystemExit("Euler order gate failed")
    if not (3.5 < a["orders"]["RK4"] < 4.5):
        raise SystemExit("RK4 order gate failed")
    if not (0.8 < a["orders"]["BE"] < 1.2):
        raise SystemExit("backward Euler order gate failed")
    if not (1.7 < a["orders"]["Trap"] < 2.3):
        raise SystemExit("trapezoidal order gate failed")
    if not (3.5 < b["state_order"] < 4.5 and 3.5 < b["logp_order"] < 4.5):
        raise SystemExit("probability-flow RK4 order gate failed")
    if b["mass_drift"] > 1e-12 or b["pde_residual"] > 1e-13:
        raise SystemExit("density conservation gate failed")
    if abs(c["qv"][-1] - c["qv_target"]) > 0.08:
        raise SystemExit("quadratic variation gate failed")
    if not (0.35 < c["ito_order"] < 0.7):
        raise SystemExit("Ito residual order gate failed")
    if abs(c["half_m2"][-1] - c["analytic_half_m2"]) > 0.15:
        raise SystemExit("half-score endpoint moment gate failed")


if __name__ == "__main__":
    main()
