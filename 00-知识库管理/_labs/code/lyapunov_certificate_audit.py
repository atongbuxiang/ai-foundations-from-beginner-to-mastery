#!/usr/bin/env python3
"""Deterministic audit for Lyapunov metrics, LaSalle, and Euler stability.

Only the Python standard library is required.  The script writes one SVG and
prints machine-checkable metrics used by the accompanying Obsidian lab note.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "dynamics"
    / "plot-lyapunov-metric-lasalle-discrete-v2.svg"
)


def linspace(start: float, stop: float, count: int) -> list[float]:
    if count < 2:
        return [start]
    step = (stop - start) / (count - 1)
    return [start + i * step for i in range(count)]


def nonnormal_state(t: float) -> tuple[float, float]:
    """Exact state for A=[[-1,6],[0,-2]], x0=(1,1)/sqrt(2)."""
    a = 1.0 / math.sqrt(2.0)
    e1 = math.exp(-t)
    e2 = math.exp(-2.0 * t)
    return a * (7.0 * e1 - 6.0 * e2), a * e2


def p_energy(x: tuple[float, float]) -> float:
    x1, x2 = x
    return 0.5 * x1 * x1 + 2.0 * x1 * x2 + 3.25 * x2 * x2


def norm_sq(x: tuple[float, float]) -> float:
    return x[0] * x[0] + x[1] * x[1]


def oscillator_rhs(state: tuple[float, float], gamma: float) -> tuple[float, float]:
    q, p = state
    return p, -q - gamma * p


def rk4_step(
    state: tuple[float, float],
    dt: float,
    rhs: Callable[[tuple[float, float]], tuple[float, float]],
) -> tuple[float, float]:
    k1 = rhs(state)
    k2 = rhs((state[0] + 0.5 * dt * k1[0], state[1] + 0.5 * dt * k1[1]))
    k3 = rhs((state[0] + 0.5 * dt * k2[0], state[1] + 0.5 * dt * k2[1]))
    k4 = rhs((state[0] + dt * k3[0], state[1] + dt * k3[1]))
    return (
        state[0] + dt * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0,
        state[1] + dt * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]) / 6.0,
    )


def polyline(
    points: Sequence[tuple[float, float]],
    stroke: str,
    width: float = 2.4,
    dash: str | None = None,
) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{coords}" fill="none" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linejoin="round" '
        f'stroke-linecap="round"{dash_attr}/>'
    )


def map_points(
    xs: Iterable[float],
    ys: Iterable[float],
    x0: float,
    y0: float,
    width: float,
    height: float,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> list[tuple[float, float]]:
    result = []
    for x, y in zip(xs, ys):
        px = x0 + width * (x - xmin) / (xmax - xmin)
        py = y0 + height * (ymax - y) / (ymax - ymin)
        result.append((px, py))
    return result


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def axis_panel(
    title: str,
    subtitle: str,
    x: float,
    y: float,
    width: float,
    height: float,
    xlabel: str,
    ylabel: str,
    x_ticks: Sequence[tuple[float, str]],
    y_ticks: Sequence[tuple[float, str]],
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> tuple[list[str], tuple[float, float, float, float]]:
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        'fill="#fffefb" stroke="#d6dee8" stroke-width="1.5"/>',
        f'<text x="{x + 18}" y="{y + 29}" class="title">{esc(title)}</text>',
        f'<text x="{x + 18}" y="{y + 49}" class="sub">{esc(subtitle)}</text>',
    ]
    left = x + 52
    top = y + 70
    plot_w = width - 72
    # Reserve a footer band for the acceptance note and x-axis label.
    plot_h = height - 148
    bottom = top + plot_h
    right = left + plot_w

    for value, label in y_ticks:
        py = top + plot_h * (ymax - value) / (ymax - ymin)
        parts.append(
            f'<line x1="{left}" y1="{py:.2f}" x2="{right}" y2="{py:.2f}" '
            'stroke="#e2e8f0" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{left - 8}" y="{py + 4:.2f}" class="tick" '
            f'text-anchor="end">{esc(label)}</text>'
        )
    for value, label in x_ticks:
        px = left + plot_w * (value - xmin) / (xmax - xmin)
        parts.append(
            f'<line x1="{px:.2f}" y1="{top}" x2="{px:.2f}" y2="{bottom}" '
            'stroke="#f1f5f9" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{px:.2f}" y="{bottom + 18}" class="tick" '
            f'text-anchor="middle">{esc(label)}</text>'
        )
    parts.extend(
        [
            f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" '
            'stroke="#64748b" stroke-width="1.2"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" '
            'stroke="#64748b" stroke-width="1.2"/>',
            f'<text x="{(left + right) / 2}" y="{y + height - 12}" '
            f'class="axis" text-anchor="middle">{esc(xlabel)}</text>',
            f'<text x="{x + 15}" y="{(top + bottom) / 2}" class="axis" '
            f'text-anchor="middle" transform="rotate(-90 {x + 15} {(top + bottom) / 2})">'
            f'{esc(ylabel)}</text>',
        ]
    )
    return parts, (left, top, plot_w, plot_h)


def build_svg(metrics: dict[str, float], output: Path) -> None:
    width, height = 1320, 470
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Lyapunov certificate audit</title>',
        '<desc id="desc">Three panels compare a tailored Lyapunov metric with '
        'Euclidean transient growth, show LaSalle energy decay for a damped '
        'oscillator, and locate the explicit Euler stability boundary.</desc>',
        """<style>
        text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}
        .title{font:700 22px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#0f172a}
        .sub{font:17px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#475569}
        .axis{font:15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#475569}
        .tick{font:15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#64748b}
        .legend{font:15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#334155}
        .note{font:15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#0f172a}
        </style>""",
        '<rect width="1320" height="470" fill="#ffffff"/>',
    ]

    # Panel A
    panel_a, box_a = axis_panel(
        "A · 非正规系统与 P-能量",
        "A=[[-1,6],[0,-2]],  AᵀP+PA=-I",
        18,
        18,
        412,
        434,
        "time t",
        "normalized quantity",
        [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5"), (2, "2")],
        0,
        5,
        0,
        2.25,
    )
    parts.extend(panel_a)
    times_a = linspace(0.0, 5.0, 501)
    states_a = [nonnormal_state(t) for t in times_a]
    n0 = norm_sq(states_a[0])
    v0 = p_energy(states_a[0])
    norm_rel = [norm_sq(x) / n0 for x in states_a]
    vp_rel = [p_energy(x) / v0 for x in states_a]
    left, top, pw, ph = box_a
    parts.append(polyline(map_points(times_a, norm_rel, left, top, pw, ph, 0, 5, 0, 2.25), "#ef4444"))
    parts.append(polyline(map_points(times_a, vp_rel, left, top, pw, ph, 0, 5, 0, 2.25), "#2563eb"))
    parts.extend(
        [
            '<line x1="84" y1="92" x2="106" y2="92" stroke="#ef4444" stroke-width="3"/>',
            '<text x="112" y="96" class="legend">‖x‖² / ‖x₀‖²</text>',
            '<line x1="220" y1="92" x2="242" y2="92" stroke="#2563eb" stroke-width="3"/>',
            '<text x="248" y="96" class="legend">V_P / V_P(x₀)</text>',
            f'<text x="84" y="415" class="note">peak Euclidean ratio = '
            f'{metrics["nonnormal_peak_norm_sq_ratio"]:.4f};  V̇_P = −‖x‖²</text>',
        ]
    )

    # Panel B
    panel_b, box_b = axis_panel(
        "B · LaSalle：Ė=0 不等于停",
        "q̇=p, ṗ=−q−0.4p,  Ė=−0.4p²",
        454,
        18,
        412,
        434,
        "time t",
        "normalized value",
        [(0, "0"), (5, "5"), (10, "10"), (15, "15"), (20, "20")],
        [(0, "0"), (0.5, "0.5"), (1, "1")],
        0,
        20,
        0,
        1.05,
    )
    parts.extend(panel_b)
    gamma = 0.4
    dt = 0.002
    steps = int(20.0 / dt)
    state = (1.5, 0.0)
    times_b: list[float] = []
    energy_rel: list[float] = []
    diss_rel: list[float] = []
    e0 = 0.5 * (state[0] ** 2 + state[1] ** 2)
    for k in range(steps + 1):
        if k % 10 == 0:
            times_b.append(k * dt)
            e = 0.5 * (state[0] ** 2 + state[1] ** 2)
            energy_rel.append(e / e0)
            diss_rel.append(gamma * state[1] ** 2 / e0)
        if k < steps:
            state = rk4_step(state, dt, lambda z: oscillator_rhs(z, gamma))
    left, top, pw, ph = box_b
    parts.append(polyline(map_points(times_b, energy_rel, left, top, pw, ph, 0, 20, 0, 1.05), "#2563eb"))
    parts.append(polyline(map_points(times_b, diss_rel, left, top, pw, ph, 0, 20, 0, 1.05), "#f97316", 2.0, "5 4"))
    parts.extend(
        [
            '<line x1="520" y1="92" x2="542" y2="92" stroke="#2563eb" stroke-width="3"/>',
            '<text x="548" y="96" class="legend">E(t) / E(0)</text>',
            '<line x1="658" y1="92" x2="680" y2="92" stroke="#f97316" stroke-width="3" stroke-dasharray="5 4"/>',
            '<text x="686" y="96" class="legend">0.4p² / E(0)</text>',
            '<circle cx="506" cy="112" r="4.5" fill="#ef4444"/>',
            '<text x="516" y="116" class="note">t=0: p=0 ⇒ Ė=0, but ṗ=−1.5</text>',
            f'<text x="520" y="415" class="note">final norm={metrics["oscillator_final_norm"]:.5f}; '
            f'invariant subset=(0,0)</text>',
        ]
    )

    # Panel C
    panel_c, box_c = axis_panel(
        "C · 离散步长与相反结论",
        "ẋ=−x; Euler: xₖ₊₁=(1−h)xₖ",
        890,
        18,
        412,
        434,
        "step k",
        "log₁₀(Vₖ / V₀)",
        [(0, "0"), (5, "5"), (10, "10"), (15, "15"), (20, "20")],
        [(-12, "−12"), (-8, "−8"), (-4, "−4"), (0, "0"), (3, "3")],
        0,
        20,
        -12.5,
        3.5,
    )
    parts.extend(panel_c)
    left, top, pw, ph = box_c
    colors = {0.5: "#059669", 1.8: "#2563eb", 2.2: "#ef4444"}
    for h in (0.5, 1.8, 2.2):
        ks = list(range(21))
        values = []
        for k in ks:
            ratio = abs(1.0 - h) ** (2 * k)
            values.append(max(-12.5, math.log10(ratio) if ratio > 0 else -12.5))
        parts.append(
            polyline(
                map_points(ks, values, left, top, pw, ph, 0, 20, -12.5, 3.5),
                colors[h],
            )
        )
    y_zero = top + ph * (3.5 - 0.0) / 16.0
    parts.append(
        f'<line x1="{left}" y1="{y_zero:.2f}" x2="{left + pw}" y2="{y_zero:.2f}" '
        'stroke="#0f172a" stroke-width="1.2" stroke-dasharray="4 4"/>'
    )
    parts.extend(
        [
            '<line x1="956" y1="92" x2="976" y2="92" stroke="#059669" stroke-width="3"/>',
            '<text x="982" y="96" class="legend">h=0.5</text>',
            '<line x1="1038" y1="92" x2="1058" y2="92" stroke="#2563eb" stroke-width="3"/>',
            '<text x="1064" y="96" class="legend">h=1.8</text>',
            '<line x1="1120" y1="92" x2="1140" y2="92" stroke="#ef4444" stroke-width="3"/>',
            '<text x="1146" y="96" class="legend">h=2.2</text>',
            '<text x="956" y="415" class="note">ΔV = ½h(h−2)x²; strict decay iff 0 &lt; h &lt; 2</text>',
        ]
    )

    parts.append("</svg>")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts), encoding="utf-8")


def audit() -> dict[str, float]:
    # Track A exact samples.
    times = linspace(0.0, 5.0, 5001)
    states = [nonnormal_state(t) for t in times]
    norm_values = [norm_sq(x) for x in states]
    p_values = [p_energy(x) for x in states]
    initial_norm_sq = norm_values[0]
    initial_p = p_values[0]
    max_p_increase = max(p_values[i + 1] - p_values[i] for i in range(len(p_values) - 1))

    # Exact matrix identity residual for P.
    # A^T P + P A + I, expanded using tiny 2x2 arithmetic.
    a = ((-1.0, 6.0), (0.0, -2.0))
    p = ((0.5, 1.0), (1.0, 3.25))
    residual = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        for j in range(2):
            atp = sum(a[k][i] * p[k][j] for k in range(2))
            pa = sum(p[i][k] * a[k][j] for k in range(2))
            residual[i][j] = atp + pa + (1.0 if i == j else 0.0)
    identity_residual = max(abs(value) for row in residual for value in row)

    # Track B RK4.
    gamma = 0.4
    dt = 0.002
    steps = int(20.0 / dt)
    state = (1.5, 0.0)
    energies = [0.5 * (state[0] ** 2 + state[1] ** 2)]
    for _ in range(steps):
        state = rk4_step(state, dt, lambda z: oscillator_rhs(z, gamma))
        energies.append(0.5 * (state[0] ** 2 + state[1] ** 2))
    max_energy_increase = max(
        energies[i + 1] - energies[i] for i in range(len(energies) - 1)
    )

    # Track C exact Euler ratios.
    euler_ratios = {
        h: abs(1.0 - h) ** 40
        for h in (0.5, 1.8, 2.2)
    }

    metrics = {
        "nonnormal_initial_norm_sq_derivative": 3.0,
        "nonnormal_peak_norm_sq_ratio": max(norm_values) / initial_norm_sq,
        "nonnormal_final_norm_sq_ratio": norm_values[-1] / initial_norm_sq,
        "p_energy_final_ratio": p_values[-1] / initial_p,
        "p_energy_max_step_increase": max_p_increase,
        "lyapunov_equation_max_residual": identity_residual,
        "oscillator_initial_energy_derivative": 0.0,
        "oscillator_initial_p_derivative": -1.5,
        "oscillator_final_norm": math.sqrt(norm_sq(state)),
        "oscillator_final_energy_ratio": energies[-1] / energies[0],
        "oscillator_max_step_energy_increase": max_energy_increase,
        "euler_h_0_5_energy_ratio_k20": euler_ratios[0.5],
        "euler_h_1_8_energy_ratio_k20": euler_ratios[1.8],
        "euler_h_2_2_energy_ratio_k20": euler_ratios[2.2],
    }

    assert metrics["nonnormal_initial_norm_sq_derivative"] > 0.0
    assert metrics["nonnormal_peak_norm_sq_ratio"] > 1.5
    assert metrics["p_energy_max_step_increase"] < 0.0
    assert metrics["lyapunov_equation_max_residual"] < 1e-14
    assert metrics["oscillator_initial_energy_derivative"] == 0.0
    assert metrics["oscillator_initial_p_derivative"] != 0.0
    assert metrics["oscillator_max_step_energy_increase"] <= 1e-12
    assert metrics["oscillator_final_norm"] < 0.05
    assert metrics["euler_h_0_5_energy_ratio_k20"] < 1.0
    assert metrics["euler_h_1_8_energy_ratio_k20"] < 1.0
    assert metrics["euler_h_2_2_energy_ratio_k20"] > 1.0
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    metrics = audit()
    build_svg(metrics, args.output)
    svg_hash = hashlib.sha256(args.output.read_bytes()).hexdigest()
    report = {
        "output": str(args.output),
        "sha256": svg_hash,
        **metrics,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
