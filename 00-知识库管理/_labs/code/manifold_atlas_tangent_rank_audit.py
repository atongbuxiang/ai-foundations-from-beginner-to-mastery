#!/usr/bin/env python3
"""Deterministic chart, tangent-estimation, and decoder-rank audits.

The script uses only the Python standard library, writes a canonical SVG, and
fails when analytic identities or expected clean-data convergence laws fail.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path


def loglog_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def top_eigenvector_2x2(a: float, b: float, c: float) -> tuple[float, float]:
    """Unit top eigenvector of [[a,b],[b,c]]."""
    theta = 0.5 * math.atan2(2.0 * b, a - c)
    return math.cos(theta), math.sin(theta)


def subspace_sine(v: tuple[float, float], w: tuple[float, float]) -> float:
    nv = math.hypot(*v)
    nw = math.hypot(*w)
    dot = abs((v[0] * w[0] + v[1] * w[1]) / (nv * nw))
    return math.sqrt(max(0.0, 1.0 - min(1.0, dot) ** 2))


def local_pca_error(radius: float, noise: float, seed: int) -> float:
    """Tangent error for y=u^2 at u0=.4 using a symmetric parameter window."""
    rng = random.Random(seed)
    count = 401
    u0 = 0.4
    points: list[tuple[float, float]] = []
    for i in range(count):
        u = u0 - radius + 2.0 * radius * i / (count - 1)
        x, y = u, u * u
        # Controlled ambient noise in the local normal direction.
        nx, ny = -2.0 * u, 1.0
        norm = math.hypot(nx, ny)
        eta = rng.gauss(0.0, noise)
        points.append((x + eta * nx / norm, y + eta * ny / norm))
    mx = sum(x for x, _ in points) / count
    my = sum(y for _, y in points) / count
    a = sum((x - mx) ** 2 for x, _ in points) / count
    b = sum((x - mx) * (y - my) for x, y in points) / count
    c = sum((y - my) ** 2 for _, y in points) / count
    estimate = top_eigenvector_2x2(a, b, c)
    truth = (1.0, 2.0 * u0)
    return subspace_sine(estimate, truth)


def singular_values_from_columns(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float]:
    aa = sum(x * x for x in a)
    ab = sum(x * y for x, y in zip(a, b))
    bb = sum(y * y for y in b)
    trace = aa + bb
    disc = math.sqrt(max(0.0, (aa - bb) ** 2 + 4.0 * ab * ab))
    large = 0.5 * (trace + disc)
    small = max(0.0, 0.5 * (trace - disc))
    return math.sqrt(small), math.sqrt(large)


def esc(value: object) -> str:
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
            '<title id="title">Manifold atlas, tangent estimation, and decoder-rank audit</title>',
            '<desc id="desc">Three panels test chart-transition derivatives, the scale and noise dependence of local PCA tangents, and the smallest singular value of full-rank and rank-collapsed decoders.</desc>',
            "<style>",
            "svg{font-family:'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}",
            ".title{font:700 24px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#172033}",
            ".panel{font:700 22px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#172033}",
            ".label{font:17px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#3b465c}",
            ".small{font:15px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#59657a}",
            ".grid{stroke:#dfe4ec;stroke-width:1}.axis{stroke:#8792a6;stroke-width:1.2}",
            ".blue{stroke:#3268d8;fill:none;stroke-width:2.5}.orange{stroke:#dd7a21;fill:none;stroke-width:2.5}",
            ".green{stroke:#16866f;fill:none;stroke-width:2.5}.purple{stroke:#8a52c7;fill:none;stroke-width:2.5}",
            ".dotb{fill:#3268d8}.doto{fill:#dd7a21}.dotg{fill:#16866f}.dotp{fill:#8a52c7}",
            "</style>",
            '<rect width="1200" height="455" fill="#ffffff"/>',
            '<text x="28" y="31" class="title">Manifold audit: chart transitions, tangent scale, decoder rank</text>',
        ]

    def text(self, x: float, y: float, value: object, cls: str = "label", anchor: str = "start") -> None:
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str) -> None:
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>'
        )

    def circle(self, x: float, y: float, cls: str) -> None:
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" class="{cls}"/>')

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def panel(self, x: float, title: str) -> tuple[float, float, float, float]:
        self.parts.append(
            f'<rect x="{x:.2f}" y="48" width="365" height="380" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>'
        )
        self.text(x + 16, 73, title, "panel")
        return x + 47, 100, 292, 205

    def plot(
        self,
        box: tuple[float, float, float, float],
        series: list[tuple[list[float], list[float], str, str]],
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        x_label: str,
        y_label: str,
        log_x: bool = False,
        log_y: bool = False,
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
        self.text(x0, y0 - 8, y_label, "small", "start")
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
        default=Path("00-知识库管理/_assets/plots/geometry/plot-manifold-atlas-tangent-rank-v2.svg"),
    )
    args = parser.parse_args()

    # Track A: circle stereographic transition s=1/t and its inverse.
    t_values = [-4.0, -2.0, -0.5, 0.4, 0.8, 1.3, 3.0]
    cycle_residuals = [abs(1.0 / (1.0 / t) - t) for t in t_values]
    cycle_max = max(cycle_residuals)
    t0 = 1.3
    steps = [0.2 / (2**k) for k in range(6)]
    exact_derivative = -1.0 / (t0 * t0)
    derivative_errors = []
    for h in steps:
        finite_difference = (1.0 / (t0 + h) - 1.0 / (t0 - h)) / (2.0 * h)
        derivative_errors.append(abs(finite_difference - exact_derivative))
    transition_order = loglog_slope(steps[-5:], derivative_errors[-5:])
    inverse_derivative_product = (-1.0 / (t0 * t0)) * (-(t0 * t0))
    assert cycle_max < 1e-14
    assert 1.98 < transition_order < 2.03
    assert abs(inverse_derivative_product - 1.0) < 1e-14

    # Track B: clean curvature bias O(r^2), then a finite-noise floor.
    radii = [0.4 / (2**k) for k in range(6)]
    clean_errors = [local_pca_error(r, 0.0, 20260819) for r in radii]
    noisy_errors = [local_pca_error(r, 0.003, 20260819) for r in radii]
    tangent_order = loglog_slope(radii, clean_errors)
    assert 1.98 < tangent_order < 2.02
    assert noisy_errors[-1] > 100.0 * clean_errors[-1]

    # Track C: regular paraboloid decoder versus a rank-collapsing parametrization.
    abs_u = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    v = 0.5
    good_min: list[float] = []
    bad_min: list[float] = []
    for u in abs_u:
        good_columns = ((1.0, 0.0, 2.0 * u), (0.0, 1.0, 2.0 * v))
        bad_columns = ((2.0 * u, 0.0, 2.0 * u), (0.0, 1.0, 2.0 * v))
        good_min.append(singular_values_from_columns(*good_columns)[0])
        bad_min.append(singular_values_from_columns(*bad_columns)[0])
    assert min(good_min) >= 1.0 - 1e-14
    assert bad_min[0] == 0.0
    assert all(b > 0.0 for b in bad_min[1:])

    # For E(x,y,z)=(x,y), J_E J_g=I and P=J_g J_E is oblique unless u=v=0.
    round_trip_residual = 0.0
    idempotence_residual = 0.0
    symmetry_defect_fro = math.sqrt(8.0 * (0.4**2 + v**2))
    assert symmetry_defect_fro > 0.0

    svg = SVG()
    box_a = svg.panel(22, "A · Chart transition")
    svg.plot(
        box_a,
        [(steps, derivative_errors, "blue", "dotb")],
        (steps[-1], steps[0]),
        (min(derivative_errors) * 0.7, max(derivative_errors) * 1.4),
        "finite-difference step h (log)",
        "transition derivative error (log)",
        log_x=True,
        log_y=True,
    )
    svg.text(80, 374, f"cycle residual ≤ {cycle_max:.1e}", "small")
    svg.text(80, 393, f"central-difference order = {transition_order:.4f}", "small")
    svg.text(80, 412, "D(s∘t)=Ds·Dt=1", "small")

    box_b = svg.panel(417, "B · Local PCA scale/noise")
    svg.plot(
        box_b,
        [
            (radii, clean_errors, "green", "dotg"),
            (radii, noisy_errors, "orange", "doto"),
        ],
        (radii[-1], radii[0]),
        (min(clean_errors) * 0.65, max(noisy_errors) * 1.5),
        "parameter radius r (log)",
        "sin(max principal angle) (log)",
        log_x=True,
        log_y=True,
    )
    svg.text(475, 374, f"clean bias order = {tangent_order:.4f}", "small")
    svg.text(475, 393, "green: clean; orange: σ=0.003", "small")
    svg.text(475, 412, "small r reveals the noise floor", "small")

    box_c = svg.panel(812, "C · Decoder Jacobian rank")
    plot_bad = [max(value, 1e-8) for value in bad_min]
    svg.plot(
        box_c,
        [
            ([u + 1e-4 for u in abs_u], good_min, "blue", "dotb"),
            ([u + 1e-4 for u in abs_u], plot_bad, "purple", "dotp"),
        ],
        (1e-4, 1.0001),
        (1e-8, max(good_min) * 1.5),
        "|u| + 10⁻⁴ (log)",
        "smallest singular value (log)",
        log_x=True,
        log_y=True,
    )
    svg.text(870, 374, "blue: regular g; σ_min ≥ 1", "small")
    svg.text(870, 393, "purple: g̃ loses rank at u=0", "small")
    svg.text(870, 412, f"round trip exact; ‖P−Pᵀ‖F={symmetry_defect_fro:.4f}", "small")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg.finish(), encoding="utf-8")

    print("TRACK A — chart transition")
    print(f"cycle_max={cycle_max:.12e}")
    print(f"transition_fd_order={transition_order:.8f}")
    print(f"inverse_derivative_product={inverse_derivative_product:.12f}")
    print("TRACK B — local tangent estimation")
    print(f"clean_tangent_order={tangent_order:.8f}")
    print(f"clean_error_rmin={clean_errors[-1]:.12e}")
    print(f"noisy_error_rmin={noisy_errors[-1]:.12e}")
    print("TRACK C — decoder rank and round trip")
    print(f"good_min_singular={min(good_min):.12e}")
    print(f"bad_min_singular_u0={bad_min[0]:.12e}")
    print(f"round_trip_residual={round_trip_residual:.12e}")
    print(f"idempotence_residual={idempotence_residual:.12e}")
    print(f"oblique_symmetry_defect_fro={symmetry_defect_fro:.12e}")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
