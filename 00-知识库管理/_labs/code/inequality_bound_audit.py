#!/usr/bin/env python3
"""Deterministic audits for inequality slack, equality, and stable evaluation.

Standard-library only. The script audits the free parameter in quadratic Young,
the angular equality geometry of Cauchy-Schwarz, a two-point exponential Jensen
gap, log-sum-exp max bounds across dimension/temperature, a finite Lipschitz
grid, and naive versus shifted floating-point evaluation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
from pathlib import Path


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class SVG:
    def __init__(self, width: int = 1440, height: int = 760) -> None:
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-06 inequality slack, equality, Jensen gap, and log-sum-exp audit</title>',
            '<desc id="desc">Four scientific panels show Young bound slack versus epsilon, Cauchy normalized inner product versus angle, exponential Jensen gap versus spread, and log-sum-exp max gap versus margin for several dimensions and temperatures.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 17px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            ".blue{stroke:#2672dd;fill:none;stroke-width:2.8}.orange{stroke:#e77817;fill:none;stroke-width:2.8}",
            ".green{stroke:#169873;fill:none;stroke-width:2.8}.purple{stroke:#7b61c9;fill:none;stroke-width:2.8}",
            ".red{stroke:#cb445a;fill:none;stroke-width:2.3}.dash{stroke-dasharray:7 5}",
            "</style>",
            '<rect width="1440" height="760" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-06 audit · slack, equality geometry, Jensen curvature, and stable log-sum-exp</text>',
            '<text x="36" y="62" class="sub">Finite curves diagnose where a valid bound becomes loose; universal inequalities still require proof.</text>',
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
            f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'
        )

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str,
        stroke: str = "none",
        rx: float = 6,
    ) -> None:
        self.parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}"/>'
        )

    def line(
        self, x1: float, y1: float, x2: float, y2: float, cls: str = "grid"
    ) -> None:
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>'
        )

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def circle(self, x: float, y: float, r: float, fill: str) -> None:
        self.parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}"/>'
        )

    def panel(
        self, x: float, y: float, w: float, h: float, title: str
    ) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def stable_lse(values: tuple[float, ...] | list[float]) -> float:
    maximum = max(values)
    return maximum + math.log(sum(math.exp(value - maximum) for value in values))


def young_audit(a: float = 3.0, b: float = 1.0) -> dict[str, object]:
    epsilons = [
        10 ** (-1.3 + 2.0 * index / 200)
        for index in range(201)
    ]
    target = 2.0 * abs(a * b)
    bounds = [epsilon * a * a + b * b / epsilon for epsilon in epsilons]
    optimum = abs(b / a)
    optimum_bound = optimum * a * a + b * b / optimum
    assert all(bound + 1e-12 >= target for bound in bounds)
    assert math.isclose(optimum_bound, target, rel_tol=0.0, abs_tol=1e-12)
    return {
        "a": a,
        "b": b,
        "epsilons": epsilons,
        "target": target,
        "bounds": bounds,
        "optimum": optimum,
        "optimum_bound": optimum_bound,
        "bound_eps_1": a * a + b * b,
    }


def cauchy_audit() -> dict[str, object]:
    angles = list(range(0, 91))
    ratios = [abs(math.cos(math.radians(angle))) for angle in angles]
    slacks = [1.0 - ratio for ratio in ratios]
    assert math.isclose(ratios[0], 1.0, abs_tol=1e-12)
    assert ratios[-1] < 1e-12
    assert all(0.0 <= ratio <= 1.0 for ratio in ratios)
    checkpoints = {
        angle: abs(math.cos(math.radians(angle)))
        for angle in (0, 30, 60, 90)
    }
    return {
        "angles": angles,
        "ratios": ratios,
        "slacks": slacks,
        "checkpoints": checkpoints,
    }


def jensen_audit() -> dict[str, object]:
    spreads = [2.5 * index / 200 for index in range(201)]
    exact_gaps = [math.cosh(spread) - 1.0 for spread in spreads]
    quadratic = [0.5 * spread * spread for spread in spreads]
    assert all(gap >= -1e-14 for gap in exact_gaps)
    assert all(
        exact + 1e-12 >= approximation
        for exact, approximation in zip(exact_gaps, quadratic)
    )
    checkpoints = {
        spread: math.cosh(spread) - 1.0
        for spread in (0.0, 0.5, 1.0, 2.0)
    }
    return {
        "spreads": spreads,
        "exact_gaps": exact_gaps,
        "quadratic": quadratic,
        "checkpoints": checkpoints,
    }


def lse_gap(classes: int, temperature: float, margin: float) -> float:
    return temperature * math.log1p(
        (classes - 1) * math.exp(-margin / temperature)
    )


def lse_audit() -> dict[str, object]:
    margins = [10.0 * index / 200 for index in range(201)]
    configurations = [
        (8, 1.0, "C=8, tau=1"),
        (32, 1.0, "C=32, tau=1"),
        (8, 0.5, "C=8, tau=0.5"),
    ]
    curves: dict[str, list[float]] = {}
    for classes, temperature, label in configurations:
        values = [
            lse_gap(classes, temperature, margin)
            for margin in margins
        ]
        upper = temperature * math.log(classes)
        assert math.isclose(values[0], upper, abs_tol=1e-12)
        assert all(0.0 <= value <= upper + 1e-12 for value in values)
        assert all(
            values[index + 1] <= values[index] + 1e-15
            for index in range(len(values) - 1)
        )
        curves[label] = values

    overflow = False
    try:
        math.log(math.exp(1000.0) + math.exp(999.0) + math.exp(998.0))
    except OverflowError:
        overflow = True
    stable_value = stable_lse((1000.0, 999.0, 998.0))
    assert overflow
    assert math.isclose(stable_value, 1000.4076059644444, abs_tol=1e-12)

    grid = (-4.0, -1.0, 0.0, 2.0, 7.0)
    vectors = list(itertools.product(grid, repeat=3))
    maximum_ratio = 0.0
    checked_pairs = 0
    for x in vectors:
        lse_x = stable_lse(x)
        for y in vectors:
            delta = max(abs(left - right) for left, right in zip(x, y))
            if delta == 0.0:
                continue
            ratio = abs(lse_x - stable_lse(y)) / delta
            maximum_ratio = max(maximum_ratio, ratio)
            checked_pairs += 1
            assert ratio <= 1.0 + 2e-14

    return {
        "margins": margins,
        "curves": curves,
        "configurations": configurations,
        "overflow": overflow,
        "stable_value": stable_value,
        "checked_pairs": checked_pairs,
        "maximum_lipschitz_ratio": maximum_ratio,
        "gap_c8_tau1_margin4": lse_gap(8, 1.0, 4.0),
        "gap_c32_tau1_margin4": lse_gap(32, 1.0, 4.0),
        "gap_c8_tau05_margin4": lse_gap(8, 0.5, 4.0),
    }


def chart_box(
    x: float, y: float, w: float, h: float
) -> tuple[float, float, float, float]:
    return x + 58, y + 50, x + w - 22, y + h - 48


def draw_axes(
    svg: SVG,
    box: tuple[float, float, float, float],
    x_ticks: list[tuple[float, str]],
    y_ticks: list[tuple[float, str]],
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
) -> tuple[object, object]:
    left, top, right, bottom = box

    def sx(value: float) -> float:
        return left + (value - x_min) * (right - left) / (x_max - x_min)

    def sy(value: float) -> float:
        return bottom - (value - y_min) * (bottom - top) / (y_max - y_min)

    for value, label in y_ticks:
        py = sy(value)
        svg.line(left, py, right, py, "grid")
        svg.text(left - 8, py + 4, label, "small", "end")
    for value, label in x_ticks:
        px = sx(value)
        svg.line(px, top, px, bottom, "grid")
        svg.text(px, bottom + 17, label, "small", "middle")
    svg.line(left, bottom, right, bottom, "axis")
    svg.line(left, top, left, bottom, "axis")
    return sx, sy


def draw_legend(
    svg: SVG,
    x: float,
    y: float,
    entries: list[tuple[str, str]],
) -> None:
    offset = 0.0
    colors = {
        "blue": "#2672dd",
        "orange": "#e77817",
        "green": "#169873",
        "purple": "#7b61c9",
        "red": "#cb445a",
    }
    for label, cls in entries:
        svg.line(x + offset, y, x + offset + 20, y, cls)
        svg.text(x + offset + 26, y + 4, label, "small")
        offset += 26 + max(74, 6.6 * len(label))


def render(
    young: dict[str, object],
    cauchy: dict[str, object],
    jensen: dict[str, object],
    lse: dict[str, object],
) -> str:
    svg = SVG()

    # Panel A: Young.
    x, y, w, h = 36.0, 88.0, 670.0, 288.0
    svg.panel(x, y, w, h, "A · Young slack: a=3, b=1")
    box = chart_box(x, y, w, h)
    sx, sy = draw_axes(
        svg,
        box,
        [
            (math.log10(0.05), "0.05"),
            (math.log10(0.1), "0.1"),
            (math.log10(1 / 3), "1/3"),
            (0.0, "1"),
            (math.log10(5.0), "5"),
        ],
        [(0.0, "0"), (6.0, "6"), (12.0, "12"), (24.0, "24"), (36.0, "36")],
        math.log10(0.05),
        math.log10(5.0),
        0.0,
        36.0,
    )
    epsilons = young["epsilons"]
    bounds = young["bounds"]
    assert isinstance(epsilons, list) and isinstance(bounds, list)
    svg.polyline(
        [
            (sx(math.log10(epsilon)), sy(bound))
            for epsilon, bound in zip(epsilons, bounds)
            if bound <= 36.0
        ],
        "blue",
    )
    target = float(young["target"])
    svg.line(box[0], sy(target), box[2], sy(target), "orange dash")
    optimum = float(young["optimum"])
    svg.circle(sx(math.log10(optimum)), sy(target), 4.5, "#169873")
    draw_legend(svg, x + 405, y + 25, [("Young upper", "blue"), ("exact 2|ab|", "orange")])
    svg.text(x + 18, y + h - 14, "epsilon=1 gives 10; optimum epsilon=1/3 gives 6 exactly.", "small")

    # Panel B: Cauchy.
    x, y, w, h = 734.0, 88.0, 670.0, 288.0
    svg.panel(x, y, w, h, "B · Cauchy equality geometry")
    box = chart_box(x, y, w, h)
    sx, sy = draw_axes(
        svg,
        box,
        [(0.0, "0°"), (30.0, "30°"), (60.0, "60°"), (90.0, "90°")],
        [(0.0, "0"), (0.25, ".25"), (0.5, ".5"), (0.75, ".75"), (1.0, "1")],
        0.0,
        90.0,
        0.0,
        1.0,
    )
    angles = cauchy["angles"]
    ratios = cauchy["ratios"]
    slacks = cauchy["slacks"]
    assert isinstance(angles, list) and isinstance(ratios, list) and isinstance(slacks, list)
    svg.polyline([(sx(a), sy(r)) for a, r in zip(angles, ratios)], "blue")
    svg.polyline([(sx(a), sy(s)) for a, s in zip(angles, slacks)], "orange")
    draw_legend(svg, x + 395, y + 25, [("|cos theta|", "blue"), ("slack", "orange")])
    svg.text(x + 18, y + h - 14, "Parallel vectors are tight; orthogonal vectors have maximum normalized slack.", "small")

    # Panel C: Jensen.
    x, y, w, h = 36.0, 404.0, 670.0, 310.0
    svg.panel(x, y, w, h, "C · Jensen gap on {-r,+r}")
    box = chart_box(x, y, w, h)
    sx, sy = draw_axes(
        svg,
        box,
        [(0.0, "0"), (0.5, ".5"), (1.0, "1"), (1.5, "1.5"), (2.0, "2"), (2.5, "2.5")],
        [(0.0, "0"), (1.0, "1"), (2.0, "2"), (3.0, "3"), (4.0, "4"), (5.0, "5")],
        0.0,
        2.5,
        0.0,
        5.3,
    )
    spreads = jensen["spreads"]
    gaps = jensen["exact_gaps"]
    quadratic = jensen["quadratic"]
    assert isinstance(spreads, list) and isinstance(gaps, list) and isinstance(quadratic, list)
    svg.polyline([(sx(r), sy(g)) for r, g in zip(spreads, gaps)], "purple")
    svg.polyline([(sx(r), sy(q)) for r, q in zip(spreads, quadratic)], "green dash")
    draw_legend(svg, x + 350, y + 25, [("exact gap", "purple"), ("r^2/2 local term", "green")])
    svg.text(x + 18, y + h - 14, "Gap is zero only at r=0; curvature turns spread into a positive Jensen gap.", "small")

    # Panel D: LSE.
    x, y, w, h = 734.0, 404.0, 670.0, 310.0
    svg.panel(x, y, w, h, "D · LSE gap vs margin")
    box = chart_box(x, y, w, h)
    sx, sy = draw_axes(
        svg,
        box,
        [(0.0, "0"), (2.0, "2"), (4.0, "4"), (6.0, "6"), (8.0, "8"), (10.0, "10")],
        [(0.0, "0"), (0.7, ".7"), (1.4, "1.4"), (2.1, "2.1"), (2.8, "2.8"), (3.5, "3.5")],
        0.0,
        10.0,
        0.0,
        3.55,
    )
    margins = lse["margins"]
    curves = lse["curves"]
    assert isinstance(margins, list) and isinstance(curves, dict)
    styles = {
        "C=8, tau=1": "blue",
        "C=32, tau=1": "orange",
        "C=8, tau=0.5": "green",
    }
    for label, values in curves.items():
        assert isinstance(values, list)
        svg.polyline(
            [(sx(margin), sy(value)) for margin, value in zip(margins, values)],
            styles[label],
        )
    draw_legend(
        svg,
        x + 315,
        y + 25,
        [
            ("C=8,tau=1", "blue"),
            ("C=32,tau=1", "orange"),
            ("C=8,tau=.5", "green"),
        ],
    )
    stable_value = float(lse["stable_value"])
    svg.text(
        x + 18,
        y + h - 14,
        f"naive exp(1000) overflows; shifted LSE(1000,999,998) = {stable_value:.6f}.",
        "small",
    )

    return svg.finish()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "00-知识库管理/_assets/plots/math-foundations/"
            "plot-inequality-bound-audit-v2.svg"
        ),
    )
    args = parser.parse_args()

    young = young_audit()
    cauchy = cauchy_audit()
    jensen = jensen_audit()
    lse = lse_audit()
    document = render(young, cauchy, jensen, lse)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    digest = hashlib.sha256(document.encode("utf-8")).hexdigest()

    print(
        "YOUNG",
        {
            "target": young["target"],
            "epsilon_star": young["optimum"],
            "bound_star": young["optimum_bound"],
            "bound_epsilon_1": young["bound_eps_1"],
        },
    )
    print("CAUCHY", cauchy["checkpoints"])
    print("JENSEN", jensen["checkpoints"])
    print(
        "LSE",
        {
            "gap_C8_tau1_margin4": lse["gap_c8_tau1_margin4"],
            "gap_C32_tau1_margin4": lse["gap_c32_tau1_margin4"],
            "gap_C8_tau05_margin4": lse["gap_c8_tau05_margin4"],
            "naive_overflow": lse["overflow"],
            "stable_value": lse["stable_value"],
            "lipschitz_pairs": lse["checked_pairs"],
            "max_lipschitz_ratio": lse["maximum_lipschitz_ratio"],
        },
    )
    print("OUTPUT", args.output)
    print("SHA256", digest)


if __name__ == "__main__":
    main()
