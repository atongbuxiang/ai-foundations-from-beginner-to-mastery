#!/usr/bin/env python3
"""Deterministic audit for hyperbolic linearization and nonhyperbolic failure.

Only the Python standard library is used.  The script prints numerical
acceptance values and generates one SVG figure used by the Obsidian note.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path
from typing import Callable, Iterable, Sequence


State = tuple[float, float]


def add(a: State, b: State, scale: float = 1.0) -> State:
    return (a[0] + scale * b[0], a[1] + scale * b[1])


def rk4_step(field: Callable[[State], State], state: State, dt: float) -> State:
    k1 = field(state)
    k2 = field(add(state, k1, 0.5 * dt))
    k3 = field(add(state, k2, 0.5 * dt))
    k4 = field(add(state, k3, dt))
    return (
        state[0] + dt * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0,
        state[1] + dt * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]) / 6.0,
    )


def integrate(
    field: Callable[[State], State], state0: State, dt: float, horizon: float
) -> list[tuple[float, State]]:
    steps = int(round(horizon / dt))
    if not math.isclose(steps * dt, horizon, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("horizon must be an integer multiple of dt")
    state = state0
    out = [(0.0, state)]
    for step in range(1, steps + 1):
        state = rk4_step(field, state, dt)
        out.append((step * dt, state))
    return out


def norm2(state: State) -> float:
    return math.hypot(state[0], state[1])


def hyperbolic_field(state: State) -> State:
    """A C-infinity nonlinear sink with J(0)=diag(-1,-2)."""
    x, y = state
    return (-x + x * x, -2.0 * y + x * x)


def hyperbolic_linear_exact(state0: State, time: float) -> State:
    return (state0[0] * math.exp(-time), state0[1] * math.exp(-2.0 * time))


def radial_field(sign: int) -> Callable[[State], State]:
    def field(state: State) -> State:
        x, y = state
        radius_sq = x * x + y * y
        return (-y + sign * x * radius_sq, x + sign * y * radius_sq)

    return field


def radial_exact(radius0: float, time: float, sign: int) -> float:
    if sign == 0:
        return radius0
    denominator = 1.0 - 2.0 * sign * radius0 * radius0 * time
    if denominator <= 0.0:
        return math.inf
    return radius0 / math.sqrt(denominator)


def regression_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = sum((x - mean_x) ** 2 for x in xs)
    return numerator / denominator


def polyline(points: Iterable[tuple[float, float]], color: str, width: float = 2.5) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_svg(
    path: Path,
    epsilons: Sequence[float],
    errors: Sequence[float],
    slope: float,
    radial_runs: dict[int, list[tuple[float, State]]],
    radius0: float,
    horizon: float,
) -> None:
    width, height = 1200, 430
    panels = [(20, 20, 370, 390), (415, 20, 370, 390), (810, 20, 370, 390)]
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">双曲线性化与非双曲失效的确定性数值审计</title>',
        '<desc id="desc">第一面板验证双曲非线性系统相对线性轨道的固定时窗误差随初值尺度二次下降；第二面板比较相同纯虚雅可比矩阵下向内、中心、向外系统的半径；第三面板显示三种系统的相平面轨道。</desc>',
        '<defs><style>',
        'text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.panel{fill:#fffefb;stroke:#d6dee8;stroke-width:1.5}.title{font:700 22px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#0f172a}.sub{font:17px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#475569}.body{font:17px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#334155}.small{font:15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#64748b}.tiny{font:15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#64748b}.axis{stroke:#94a3b8;stroke-width:1.2}.grid{stroke:#e2e8f0;stroke-width:1;stroke-dasharray:4 4}</style></defs>',
        '<rect width="1200" height="430" fill="#ffffff"/>',
    ]
    for x, y, w, h in panels:
        lines.append(f'<rect class="panel" x="{x}" y="{y}" width="{w}" height="{h}"/>')

    # Panel A: log-log error scaling.
    lines.extend(
        [
            '<text class="title" x="40" y="53">A · 双曲点：线性误差的局部阶</text>',
            '<text class="sub" x="40" y="78">固定 T=2，缩小初值尺度 ε</text>',
        ]
    )
    ax0, ay0, ax1, ay1 = 70.0, 105.0, 355.0, 330.0
    log_eps = [math.log10(v) for v in epsilons]
    log_err = [math.log10(v) for v in errors]
    xmin, xmax = min(log_eps) - 0.08, max(log_eps) + 0.08
    ymin, ymax = min(log_err) - 0.18, max(log_err) + 0.18

    def map_a(x: float, y: float) -> tuple[float, float]:
        px = ax0 + (x - xmin) / (xmax - xmin) * (ax1 - ax0)
        py = ay1 - (y - ymin) / (ymax - ymin) * (ay1 - ay0)
        return px, py

    for i in range(5):
        gx = ax0 + i * (ax1 - ax0) / 4.0
        gy = ay0 + i * (ay1 - ay0) / 4.0
        lines.append(f'<line class="grid" x1="{gx:.1f}" y1="{ay0}" x2="{gx:.1f}" y2="{ay1}"/>')
        lines.append(f'<line class="grid" x1="{ax0}" y1="{gy:.1f}" x2="{ax1}" y2="{gy:.1f}"/>')
    lines.append(f'<line class="axis" x1="{ax0}" y1="{ay1}" x2="{ax1}" y2="{ay1}"/>')
    lines.append(f'<line class="axis" x1="{ax0}" y1="{ay0}" x2="{ax0}" y2="{ay1}"/>')
    points_a = [map_a(x, y) for x, y in zip(log_eps, log_err)]
    lines.append(polyline(points_a, "#2563eb", 2.8))
    for px, py in points_a:
        lines.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4.3" fill="#2563eb" stroke="#fff" stroke-width="1.5"/>')
    lines.append('<text class="small" x="212" y="354" text-anchor="middle">log10 initial scale ε</text>')
    lines.append('<text class="small" transform="translate(48 220) rotate(-90)" text-anchor="middle">log10 max trajectory error</text>')
    lines.append(f'<rect x="83" y="116" width="155" height="42" rx="7" fill="#eff6ff" stroke="#93c5fd"/><text class="body" x="160" y="142" text-anchor="middle">fitted slope = {slope:.4f}</text>')
    lines.append('<text class="tiny" x="212" y="382" text-anchor="middle">二阶余项 ⇒ fixed-window error ∝ ε²</text>')

    # Panel B: radial curves.
    lines.extend(
        [
            '<text class="title" x="435" y="53">B · 非双曲点：同一 J，不同半径</text>',
            '<text class="sub" x="435" y="78">J* has eigenvalues ±i; nonlinear cubic decides</text>',
        ]
    )
    bx0, by0, bx1, by1 = 455.0, 105.0, 760.0, 330.0
    all_radii = [norm2(state) for run in radial_runs.values() for _, state in run]
    rmax = max(all_radii) * 1.08

    def map_b(time: float, radius: float) -> tuple[float, float]:
        return (
            bx0 + time / horizon * (bx1 - bx0),
            by1 - radius / rmax * (by1 - by0),
        )

    for i in range(5):
        gx = bx0 + i * (bx1 - bx0) / 4.0
        gy = by0 + i * (by1 - by0) / 4.0
        lines.append(f'<line class="grid" x1="{gx:.1f}" y1="{by0}" x2="{gx:.1f}" y2="{by1}"/>')
        lines.append(f'<line class="grid" x1="{bx0}" y1="{gy:.1f}" x2="{bx1}" y2="{gy:.1f}"/>')
    lines.append(f'<line class="axis" x1="{bx0}" y1="{by1}" x2="{bx1}" y2="{by1}"/>')
    lines.append(f'<line class="axis" x1="{bx0}" y1="{by0}" x2="{bx0}" y2="{by1}"/>')
    colors = {-1: "#059669", 0: "#2563eb", 1: "#dc2626"}
    names = {-1: "ṙ = −r³", 0: "ṙ = 0", 1: "ṙ = +r³"}
    for sign in (-1, 0, 1):
        sampled = radial_runs[sign][::20]
        lines.append(polyline((map_b(t, norm2(s)) for t, s in sampled), colors[sign], 2.7))
    for index, sign in enumerate((-1, 0, 1)):
        x = 475 + 94 * index
        lines.append(f'<line x1="{x}" y1="350" x2="{x+19}" y2="350" stroke="{colors[sign]}" stroke-width="3"/><text class="tiny" x="{x+24}" y="354">{escape(names[sign])}</text>')
    lines.append('<text class="small" x="608" y="382" text-anchor="middle">time t · same r(0)=0.25</text>')

    # Panel C: trajectories in phase space.
    lines.extend(
        [
            '<text class="title" x="830" y="53">C · 相平面：中心、慢吸引与逃离</text>',
            '<text class="sub" x="830" y="78">轨道共享相同瞬时线性旋转</text>',
        ]
    )
    cx0, cy0, cx1, cy1 = 848.0, 98.0, 1145.0, 348.0
    extent = max(abs(coord) for run in radial_runs.values() for _, state in run for coord in state) * 1.10

    def map_c(state: State) -> tuple[float, float]:
        x, y = state
        return (
            (cx0 + cx1) / 2.0 + x / extent * (cx1 - cx0) / 2.0,
            (cy0 + cy1) / 2.0 - y / extent * (cy1 - cy0) / 2.0,
        )

    center_x, center_y = map_c((0.0, 0.0))
    for i in range(-2, 3):
        gx = center_x + i * (cx1 - cx0) / 4.5
        gy = center_y + i * (cy1 - cy0) / 4.5
        lines.append(f'<line class="grid" x1="{gx:.1f}" y1="{cy0}" x2="{gx:.1f}" y2="{cy1}"/>')
        lines.append(f'<line class="grid" x1="{cx0}" y1="{gy:.1f}" x2="{cx1}" y2="{gy:.1f}"/>')
    lines.append(f'<line class="axis" x1="{cx0}" y1="{center_y:.1f}" x2="{cx1}" y2="{center_y:.1f}"/>')
    lines.append(f'<line class="axis" x1="{center_x:.1f}" y1="{cy0}" x2="{center_x:.1f}" y2="{cy1}"/>')
    for sign in (-1, 0, 1):
        sampled = radial_runs[sign][::10]
        lines.append(polyline((map_c(state) for _, state in sampled), colors[sign], 2.5))
        end_x, end_y = map_c(radial_runs[sign][-1][1])
        lines.append(f'<circle cx="{end_x:.2f}" cy="{end_y:.2f}" r="4" fill="{colors[sign]}" stroke="#fff" stroke-width="1.2"/>')
    start_x, start_y = map_c((radius0, 0.0))
    lines.append(f'<circle cx="{start_x:.2f}" cy="{start_y:.2f}" r="5" fill="#0f172a" stroke="#fff" stroke-width="1.5"/>')
    lines.append('<text class="tiny" x="995" y="371" text-anchor="middle">black = shared start · colored dots = T endpoints</text>')
    lines.append('<rect x="840" y="383" width="308" height="20" rx="6" fill="#fff7ed" stroke="#fdba74"/><text class="tiny" x="994" y="397" text-anchor="middle">zero real part: first-order evidence is inconclusive</text>')

    lines.append('</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/dynamics/plot-linearization-hyperbolic-nonhyperbolic-v2.svg"),
    )
    args = parser.parse_args()

    dt = 0.001
    hyper_horizon = 2.0
    direction = (0.8, -0.6)
    epsilons = [0.2, 0.1, 0.05, 0.025]
    errors: list[float] = []
    endpoint_errors: list[float] = []
    for epsilon in epsilons:
        initial = (epsilon * direction[0], epsilon * direction[1])
        run = integrate(hyperbolic_field, initial, dt, hyper_horizon)
        distances = [
            norm2((state[0] - exact[0], state[1] - exact[1]))
            for time, state in run
            for exact in [hyperbolic_linear_exact(initial, time)]
        ]
        errors.append(max(distances))
        endpoint_errors.append(distances[-1])

    slope = regression_slope(
        [math.log(value) for value in epsilons],
        [math.log(value) for value in errors],
    )

    radius0 = 0.25
    radial_horizon = 6.5
    radial_runs = {
        sign: integrate(radial_field(sign), (radius0, 0.0), dt, radial_horizon)
        for sign in (-1, 0, 1)
    }
    radial_errors: dict[int, float] = {}
    for sign, run in radial_runs.items():
        radial_errors[sign] = max(
            abs(norm2(state) - radial_exact(radius0, time, sign))
            for time, state in run
        )

    generate_svg(args.output, epsilons, errors, slope, radial_runs, radius0, radial_horizon)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()

    print("CONFIG dt=0.001 hyperbolic_T=2.0 radial_T=6.5 radial_r0=0.25")
    print("HYPERBOLIC system=(-x+x^2,-2y+x^2) jacobian=diag(-1,-2)")
    for epsilon, maximum, endpoint in zip(epsilons, errors, endpoint_errors):
        print(
            f"HYP epsilon={epsilon:.6f} max_error={maximum:.12e} "
            f"max_error_over_eps2={maximum/(epsilon*epsilon):.12e} "
            f"endpoint_error={endpoint:.12e}"
        )
    print(f"HYP fitted_loglog_slope={slope:.8f}")
    print("NONHYP jacobian_all=[[0,-1],[1,0]] eigenvalues=+i,-i")
    for sign, label in [(-1, "inward"), (0, "center"), (1, "outward")]:
        final_radius = norm2(radial_runs[sign][-1][1])
        exact_radius = radial_exact(radius0, radial_horizon, sign)
        print(
            f"RADIAL kind={label} final_radius={final_radius:.12e} "
            f"exact_final_radius={exact_radius:.12e} "
            f"max_radius_error={radial_errors[sign]:.12e}"
        )
    print(f"SVG path={args.output} sha256={digest}")

    assert 1.90 < slope < 2.10, "fixed-window linearization error should be second order"
    assert radial_errors[-1] < 1e-10 and radial_errors[0] < 1e-10 and radial_errors[1] < 1e-9
    final_radii = [norm2(radial_runs[sign][-1][1]) for sign in (-1, 0, 1)]
    assert final_radii[0] < final_radii[1] < final_radii[2]
    print("ACCEPT all_assertions_passed=true")


if __name__ == "__main__":
    main()
