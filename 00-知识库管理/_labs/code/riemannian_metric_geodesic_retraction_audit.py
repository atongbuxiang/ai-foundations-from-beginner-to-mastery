#!/usr/bin/env python3
"""Deterministic Riemannian metric, geodesic-energy, and retraction audits.

The script uses only Python's standard library, writes one canonical SVG, and
fails if coordinate-length, quadrature, or sphere-retraction orders disagree
with the analytic predictions.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


def loglog_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def norm3(v: tuple[float, float, float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def sub3(
    u: tuple[float, float, float], v: tuple[float, float, float]
) -> tuple[float, float, float]:
    return tuple(a - b for a, b in zip(u, v))  # type: ignore[return-value]


def escape(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class SVG:
    def __init__(self) -> None:
        self.parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="455" viewBox="0 0 1200 455" role="img" aria-labelledby="title desc">',
            '<title id="title">Riemannian metric, path energy, and sphere retraction audit</title>',
            '<desc id="desc">Three log-log panels verify second-order circle polygon length, second-order midpoint energy quadrature, and second- versus third-order sphere update errors.</desc>',
            "<style>",
            "svg{font-family:'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}",
            ".title{font:700 24px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#172033}",
            ".panel{font:700 22px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#172033}",
            ".label{font:17px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#3b465c}",
            ".small{font:15px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#59657a}",
            ".grid{stroke:#dfe4ec;stroke-width:1}.axis{stroke:#8792a6;stroke-width:1.2}",
            ".blue{stroke:#3268d8;fill:none;stroke-width:2.5}.orange{stroke:#dd7a21;fill:none;stroke-width:2.5}",
            ".green{stroke:#16866f;fill:none;stroke-width:2.5}.purple{stroke:#8a52c7;fill:none;stroke-width:2.5}",
            ".dash{stroke-dasharray:5 5;stroke-width:1.6}.dotb{fill:#3268d8}.doto{fill:#dd7a21}.dotg{fill:#16866f}.dotp{fill:#8a52c7}",
            "</style>",
            '<rect width="1200" height="455" fill="#ffffff"/>',
            '<text x="28" y="31" class="title">Riemannian audit: coordinate length, path energy, sphere updates</text>',
        ]

    def text(
        self,
        x: float,
        y: float,
        value: object,
        cls: str = "label",
        anchor: str = "start",
    ) -> None:
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str) -> None:
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>'
        )

    def circle(self, x: float, y: float, cls: str) -> None:
        self.parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.3" class="{cls}"/>'
        )

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def panel(self, x: float, title: str) -> tuple[float, float, float, float]:
        self.parts.append(
            f'<rect x="{x:.2f}" y="48" width="365" height="380" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>'
        )
        self.text(x + 16, 73, title, "panel")
        return x + 50, 105, 286, 185

    def plot(
        self,
        box: tuple[float, float, float, float],
        series: list[tuple[list[float], list[float], str, str]],
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        x_label: str,
        y_label: str,
        log_x: bool = True,
        log_y: bool = True,
    ) -> None:
        x0, y0, width, height = box
        tx = (lambda v: math.log10(v)) if log_x else (lambda v: v)
        ty = (lambda v: math.log10(v)) if log_y else (lambda v: v)
        xa, xb = tx(x_range[0]), tx(x_range[1])
        ya, yb = ty(y_range[0]), ty(y_range[1])

        def px(v: float) -> float:
            return x0 + (tx(v) - xa) / (xb - xa) * width

        def py(v: float) -> float:
            return y0 + height - (ty(v) - ya) / (yb - ya) * height

        for i in range(5):
            xx = x0 + i * width / 4
            yy = y0 + i * height / 4
            self.line(xx, y0, xx, y0 + height, "grid")
            self.line(x0, yy, x0 + width, yy, "grid")
        self.line(x0, y0 + height, x0 + width, y0 + height, "axis")
        self.line(x0, y0, x0, y0 + height, "axis")
        self.text(x0 + width / 2, y0 + height + 31, x_label, "small", "middle")
        self.text(x0, y0 - 8, y_label, "small")
        for xs, ys, line_cls, dot_cls in series:
            points = [(px(x), py(y)) for x, y in zip(xs, ys)]
            self.polyline(points, line_cls)
            for x, y in points:
                self.circle(x, y, dot_cls)

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "00-知识库管理/_assets/plots/geometry/plot-riemannian-metric-geodesic-retraction-v2.svg"
        ),
    )
    args = parser.parse_args()

    # Track A: unit-circle length in polar metric versus inscribed Cartesian polygon.
    counts = [12, 24, 48, 96, 192, 384]
    mesh = [1.0 / n for n in counts]
    exact_circle_length = 2.0 * math.pi
    polar_lengths = [
        sum(math.sqrt(1.0) * (2.0 * math.pi / n) for _ in range(n))
        for n in counts
    ]
    polygon_lengths = [2.0 * n * math.sin(math.pi / n) for n in counts]
    polygon_errors = [exact_circle_length - value for value in polygon_lengths]
    circle_order = loglog_slope(mesh[-5:], polygon_errors[-5:])
    polar_error = max(abs(value - exact_circle_length) for value in polar_lengths)
    assert polar_error < 1.0e-13
    assert 1.99 < circle_order < 2.01

    # Track B: same circle arc with constant-speed and t^2 reparameterizations.
    alpha = 1.4
    exact_constant_energy = 0.5 * alpha * alpha
    exact_reparameterized_energy = 2.0 * alpha * alpha / 3.0
    constant_energies: list[float] = []
    reparameterized_energies: list[float] = []
    reparameterized_lengths: list[float] = []
    for n in counts:
        dt = 1.0 / n
        constant_energies.append(
            0.5 * sum(alpha * alpha * dt for _ in range(n))
        )
        reparameterized_energies.append(
            0.5
            * sum(
                (2.0 * alpha * ((i + 0.5) * dt)) ** 2 * dt
                for i in range(n)
            )
        )
        reparameterized_lengths.append(
            sum(2.0 * alpha * ((i + 0.5) * dt) * dt for i in range(n))
        )
    energy_errors = [
        exact_reparameterized_energy - value
        for value in reparameterized_energies
    ]
    energy_order = loglog_slope(mesh[-5:], energy_errors[-5:])
    constant_energy_error = max(
        abs(value - exact_constant_energy) for value in constant_energies
    )
    path_length_error = max(abs(value - alpha) for value in reparameterized_lengths)
    assert constant_energy_error < 1.0e-13
    assert path_length_error < 1.0e-13
    assert 1.99 < energy_order < 2.01
    assert exact_reparameterized_energy > exact_constant_energy

    # Track C: sphere Euler feasibility O(t^2), normalization vs Exp O(t^3).
    steps = [0.8 / (2**k) for k in range(6)]
    euler_residuals: list[float] = []
    retraction_exp_errors: list[float] = []
    retraction_feasibility: list[float] = []
    for step in steps:
        euler = (1.0, step, 0.0)
        euler_residuals.append(abs(sum(x * x for x in euler) - 1.0))
        scale = math.sqrt(1.0 + step * step)
        retract = (1.0 / scale, step / scale, 0.0)
        exponential = (math.cos(step), math.sin(step), 0.0)
        retraction_exp_errors.append(norm3(sub3(retract, exponential)))
        retraction_feasibility.append(
            abs(sum(x * x for x in retract) - 1.0)
        )
    euler_order = loglog_slope(steps[-5:], euler_residuals[-5:])
    retraction_order = loglog_slope(steps[-5:], retraction_exp_errors[-5:])
    assert 1.999 < euler_order < 2.001
    assert 2.96 < retraction_order < 3.02
    assert max(retraction_feasibility) < 4.0e-16

    svg = SVG()
    box_a = svg.panel(25, "A · Coordinate length")
    svg.plot(
        box_a,
        [(mesh, polygon_errors, "blue", "dotb")],
        (mesh[-1], mesh[0]),
        (polygon_errors[-1] * 0.7, polygon_errors[0] * 1.4),
        "mesh h = 1/N (log)",
        "|2π − polygon length| (log)",
    )
    svg.text(43, 350, f"observed order = {circle_order:.6f}", "label")
    svg.text(43, 370, "polar metric integral = 2π to roundoff", "small")
    svg.text(43, 389, "blue: Cartesian chord approximation, O(h²)", "small")

    box_b = svg.panel(417, "B · Path length vs energy")
    svg.plot(
        box_b,
        [(mesh, energy_errors, "green", "dotg")],
        (mesh[-1], mesh[0]),
        (energy_errors[-1] * 0.7, energy_errors[0] * 1.4),
        "time mesh h = 1/N (log)",
        "reparameterized energy error (log)",
    )
    svg.text(435, 350, f"midpoint order = {energy_order:.6f}", "label")
    svg.text(
        435,
        370,
        f"constant speed: E = {exact_constant_energy:.6f}",
        "small",
    )
    svg.text(
        435,
        389,
        f"t² speed: same L = {alpha:.1f}, E = {exact_reparameterized_energy:.6f}",
        "small",
    )

    box_c = svg.panel(809, "C · Sphere update orders")
    y_min = min(retraction_exp_errors[-1], euler_residuals[-1]) * 0.6
    y_max = max(retraction_exp_errors[0], euler_residuals[0]) * 1.5
    svg.plot(
        box_c,
        [
            (steps, euler_residuals, "orange", "doto"),
            (steps, retraction_exp_errors, "purple", "dotp"),
        ],
        (steps[-1], steps[0]),
        (y_min, y_max),
        "tangent step t (log)",
        "error / residual (log)",
    )
    svg.text(827, 350, f"orange Euler constraint: order {euler_order:.6f}", "small")
    svg.text(
        827,
        370,
        f"purple ‖R−Exp‖: order {retraction_order:.6f}",
        "small",
    )
    svg.text(827, 389, "normalization feasibility: machine zero", "small")

    output = svg.finish()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    digest = hashlib.sha256(output.encode("utf-8")).hexdigest()

    print(f"circle_length_order          = {circle_order:.8f}")
    print(f"polar_metric_max_error       = {polar_error:.12e}")
    print(f"energy_midpoint_order        = {energy_order:.8f}")
    print(f"constant_speed_energy        = {exact_constant_energy:.12f}")
    print(f"reparameterized_energy       = {exact_reparameterized_energy:.12f}")
    print(f"reparameterized_length_error = {path_length_error:.12e}")
    print(f"euler_constraint_order       = {euler_order:.8f}")
    print(f"retraction_exp_order         = {retraction_order:.8f}")
    print(f"retraction_feasibility_max   = {max(retraction_feasibility):.12e}")
    print(f"svg_sha256                   = {digest}")
    print(f"wrote                        = {args.output}")


if __name__ == "__main__":
    main()
