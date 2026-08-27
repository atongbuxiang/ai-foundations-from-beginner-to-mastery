#!/usr/bin/env python3
"""Deterministic audits for metric scale, compactness, and finite-sample topology.

Standard-library only. The script writes a canonical SVG and exits non-zero when
an analytic identity or an expected asymptotic diagnostic fails.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def loglog_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    num = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    den = sum((x - mx) ** 2 for x in lx)
    return num / den


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class SVG:
    def __init__(self, width: int = 1200, height: int = 455) -> None:
        self.width = width
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">Metric, compactness, and continuity audit</title>',
            '<desc id="desc">Three panels distinguish topological equivalence from completeness, total boundedness from compactness, and continuous finite-sample warps from a jump discontinuity.</desc>',
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
            '<text x="28" y="31" class="title">Metric–topology audit: scale, compactness, finite samples</text>',
        ]

    def text(self, x: float, y: float, value: object, cls: str = "label", anchor: str = "start") -> None:
        self.parts.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>')

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str) -> None:
        self.parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>')

    def circle(self, x: float, y: float, cls: str) -> None:
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" class="{cls}"/>')

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def panel(self, x: float, title: str) -> tuple[float, float, float, float]:
        self.parts.append(f'<rect x="{x:.2f}" y="48" width="365" height="380" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>')
        self.text(x + 16, 73, title, "panel")
        return x + 47, 100, 292, 205

    def plot(
        self,
        box: tuple[float, float, float, float],
        series: list[tuple[list[float], list[float], str, str, str]],
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        x_label: str,
        y_label: str,
        log_x: bool = False,
        log_y: bool = False,
    ) -> None:
        x0, y0, w, h = box
        tx = (lambda v: math.log10(v)) if log_x else (lambda v: v)
        ty = (lambda v: math.log10(v)) if log_y else (lambda v: v)
        xa, xb = tx(x_range[0]), tx(x_range[1])
        ya, yb = ty(y_range[0]), ty(y_range[1])

        def px(v: float) -> float:
            return x0 + (tx(v) - xa) / (xb - xa) * w

        def py(v: float) -> float:
            return y0 + h - (ty(v) - ya) / (yb - ya) * h

        for i in range(5):
            xx = x0 + i * w / 4
            yy = y0 + i * h / 4
            self.line(xx, y0, xx, y0 + h, "grid")
            self.line(x0, yy, x0 + w, yy, "grid")
        self.line(x0, y0 + h, x0 + w, y0 + h, "axis")
        self.line(x0, y0, x0, y0 + h, "axis")
        self.text(x0 + w / 2, y0 + h + 31, x_label, "small", "middle")
        self.text(x0, y0 - 8, y_label, "small", "start")
        for xs, ys, line_cls, dot_cls, _ in series:
            pts = [(px(x), py(y)) for x, y in zip(xs, ys)]
            self.polyline(pts, line_cls)
            for x, y in pts:
                self.circle(x, y, dot_cls)

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/geometry/plot-metric-topology-continuity-v2.svg"),
    )
    args = parser.parse_args()

    # Track A: same topology, different Cauchy/completeness behavior.
    tails = [2.0**k for k in range(1, 11)]
    d2_tail_diameter = [math.pi / 2.0 - math.atan(n) for n in tails]
    d1_pair_gap = tails[:]  # d_1(N, 2N) = N, so (N) is not d_1-Cauchy.
    tail_order = loglog_slope(tails[-6:], d2_tail_diameter[-6:])
    assert -1.02 < tail_order < -0.97
    assert all(b < a for a, b in zip(d2_tail_diameter, d2_tail_diameter[1:]))
    assert d2_tail_diameter[-1] < 1.0 / tails[-1]

    # Track B: total boundedness is not completeness; infinite Hilbert ball is not totally bounded.
    epsilons = [0.5, 0.25, 0.125, 0.0625, 0.03125]
    # Closed-ball epsilon-net convention; open balls need an endpoint perturbation.
    interval_cover_upper = [math.ceil(1.0 / (2.0 * eps)) for eps in epsilons]
    dimensions = [2, 4, 8, 16, 32, 64, 128, 256]
    basis_packing = dimensions[:]
    basis_min_separation = math.sqrt(2.0)
    packing_radius = 0.6
    assert 2.0 * packing_radius < basis_min_separation
    assert interval_cover_upper[-1] == 16

    # Track C: a homeomorphism has shrinking finite-sample gaps; a jump does not.
    grid_sizes = [8, 16, 32, 64, 128, 256, 512]
    warp_gaps: list[float] = []
    jump_gaps: list[float] = []
    component_counts: list[int] = []
    graph_radius = 0.05
    for count in grid_sizes:
        xs = [-1.0 + 2.0 * i / (count - 1) for i in range(count)]
        warped = [x + 0.3 * math.tanh(3.0 * x) for x in xs]
        jumped = [-1.0 if x < 0.0 else 1.0 for x in xs]
        gaps = [b - a for a, b in zip(warped, warped[1:])]
        jump_steps = [b - a for a, b in zip(jumped, jumped[1:])]
        warp_gaps.append(max(gaps))
        jump_gaps.append(max(jump_steps))
        component_counts.append(1 + sum(gap > graph_radius for gap in gaps))
        input_gap = 2.0 / (count - 1)
        assert max(gaps) <= 1.9 * input_gap + 1e-12
    warp_order = loglog_slope([float(n) for n in grid_sizes[-5:]], warp_gaps[-5:])
    assert -1.05 < warp_order < -0.95
    assert all(abs(gap - 2.0) < 1e-12 for gap in jump_gaps)
    assert component_counts[-1] == 1

    svg = SVG()
    box_a = svg.panel(22, "A · Topology vs completeness")
    svg.plot(
        box_a,
        [
            (tails, d2_tail_diameter, "blue", "dotb", "d₂ tail diameter"),
            (tails, d1_pair_gap, "orange", "doto", "d₁(N,2N)"),
        ],
        (tails[0], tails[-1]),
        (min(d2_tail_diameter) * 0.75, max(d1_pair_gap) * 1.25),
        "tail index N (log)",
        "distance (log)",
        log_x=True,
        log_y=True,
    )
    svg.text(80, 374, f"d₂ tail slope = {tail_order:.4f}; d₂-Cauchy", "small")
    svg.text(80, 393, "d₁(N,2N)=N; not d₁-Cauchy", "small")
    svg.text(80, 412, "both induce the usual topology on ℝ", "small")

    box_b = svg.panel(417, "B · Compactness ledger")
    svg.plot(
        box_b,
        [
            ([1.0 / e for e in epsilons], [float(v) for v in interval_cover_upper], "green", "dotg", "interval cover"),
            ([float(v) for v in dimensions], [float(v) for v in basis_packing], "purple", "dotp", "basis packing"),
        ],
        (2.0, 256.0),
        (1.5, 300.0),
        "1/ε or truncated dimension D (log)",
        "cover / packing count (log)",
        log_x=True,
        log_y=True,
    )
    svg.text(475, 374, "(0,1): finite ε-nets, but incomplete", "small")
    svg.text(475, 393, "ℓ² basis: distance √2; packing ≥ D", "small")
    svg.text(475, 412, "D↑: no finite 0.6-net for the full ball", "small")

    box_c = svg.panel(812, "C · Graph scale and continuity")
    svg.plot(
        box_c,
        [
            ([float(n) for n in grid_sizes], warp_gaps, "blue", "dotb", "homeomorphism"),
            ([float(n) for n in grid_sizes], jump_gaps, "orange", "doto", "jump"),
        ],
        (float(grid_sizes[0]), float(grid_sizes[-1])),
        (min(warp_gaps) * 0.7, 2.5),
        "sample count N (log)",
        "largest output gap (log)",
        log_x=True,
        log_y=True,
    )
    svg.text(870, 374, f"smooth gap slope = {warp_order:.4f} ≈ −1", "small")
    svg.text(870, 393, "jump gap=2; fixed-r graph stays split", "small")
    svg.text(870, 412, f"smooth graph connected by N=512 (r={graph_radius:g})", "small")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg.finish(), encoding="utf-8")

    print("TRACK A — same topology, different completeness")
    print(f"d2_tail_order={tail_order:.8f}")
    print(f"d2_tail_diameter_N1024={d2_tail_diameter[-1]:.12e}")
    print(f"d1_pair_gap_N1024={d1_pair_gap[-1]:.1f}")
    print("TRACK B — compactness ledger")
    print(f"interval_cover_eps_0.03125={interval_cover_upper[-1]}")
    print(f"basis_min_separation={basis_min_separation:.12f}")
    print(f"basis_packing_D256={basis_packing[-1]}")
    print("TRACK C — finite-sample scale")
    print(f"smooth_gap_order={warp_order:.8f}")
    print(f"smooth_gap_N512={warp_gaps[-1]:.12e}")
    print(f"jump_gap_N512={jump_gaps[-1]:.12e}")
    print(f"smooth_components_r0.05_N512={component_counts[-1]}")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
