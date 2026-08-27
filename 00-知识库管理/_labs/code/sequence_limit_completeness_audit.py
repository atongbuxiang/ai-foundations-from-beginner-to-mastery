#!/usr/bin/env python3
"""Deterministic audits for sequence limits, completeness, and float stagnation.

Standard-library only. Four panels compare epsilon-N witnesses for geometric
sequences, exact rational Newton iterates approaching sqrt(2), pointwise versus
uniform behavior of x**n, and the difference between exact error and binary64
rounding near one.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class SVG:
    def __init__(self, width: int = 1440, height: int = 820) -> None:
        self.width = width
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-07 sequence limits, completeness, uniformity, and binary64 audit</title>',
            '<desc id="desc">Four scientific panels show geometric epsilon-N thresholds, exact rational Newton iterates approaching square root two, pointwise but nonuniform convergence of x to the n, and binary64 rounding of one plus two to the minus n.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 16px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            ".blue{stroke:#2672dd;fill:none;stroke-width:2.8}.orange{stroke:#e77817;fill:none;stroke-width:2.8}",
            ".green{stroke:#169873;fill:none;stroke-width:2.8}.purple{stroke:#7b61c9;fill:none;stroke-width:2.8}",
            ".red{stroke:#cb445a;fill:none;stroke-width:2.4}.gray{stroke:#7e8b9f;fill:none;stroke-width:2}",
            ".dash{stroke-dasharray:7 5}.dot{stroke-dasharray:3 4}",
            "</style>",
            '<rect width="1440" height="820" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-07 audit · tail witnesses, missing limits, moving hard points, and finite precision</text>',
            '<text x="36" y="62" class="sub">Finite computation diagnoses a proof contract; it does not replace the universal epsilon–N, completeness, or uniform-convergence theorem.</text>',
        ]

    def text(self, x: float, y: float, value: object, cls: str = "label", anchor: str = "start") -> None:
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'
        )

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str = "none", rx: float = 6) -> None:
        self.parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}"/>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str = "grid") -> None:
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>'
        )

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def circle(self, x: float, y: float, r: float, fill: str, stroke: str = "none") -> None:
        self.parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}"/>'
        )

    def panel(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def first_strict_geometric_witness(q: float, epsilon: float) -> int:
    n = 1
    while q**n >= epsilon:
        n += 1
    assert q**n < epsilon
    assert n == 1 or q ** (n - 1) >= epsilon
    return n


def geometric_audit() -> dict[str, object]:
    epsilon = 1e-6
    qs = (0.5, 0.8, 0.99)
    thresholds = {q: first_strict_geometric_witness(q, epsilon) for q in qs}
    assert thresholds == {0.5: 20, 0.8: 62, 0.99: 1375}
    steps = list(range(1, 1501))
    curves = {q: [q**n for n in steps] for q in qs}
    return {"epsilon": epsilon, "qs": qs, "thresholds": thresholds, "steps": steps, "curves": curves}


def rational_newton_audit(iterations: int = 8) -> dict[str, object]:
    values = [Fraction(1, 1)]
    for _ in range(iterations - 1):
        current = values[-1]
        values.append((current + Fraction(2, 1) / current) / 2)
    with localcontext() as context:
        context.prec = 140
        root_decimal = Decimal(2).sqrt()
        errors_decimal = [
            abs(Decimal(value.numerator) / Decimal(value.denominator) - root_decimal)
            for value in values
        ]
    root = math.sqrt(2.0)
    errors = [float(error) for error in errors_decimal]
    assert all(isinstance(value, Fraction) for value in values)
    assert all(errors[index + 1] < errors[index] for index in range(4))
    assert errors[-1] < 1e-90
    cauchy_gaps = [abs(float(values[index + 1] - values[index])) for index in range(len(values) - 1)]
    return {"values": values, "errors": errors, "cauchy_gaps": cauchy_gaps, "root": root}


def function_sequence_audit() -> dict[str, object]:
    ns = (1, 4, 16, 64)
    xs = [index / 400 for index in range(401)]
    curves = {n: [x**n for x in xs] for n in ns}
    fixed_grid = [index / 100 for index in range(100)]  # excludes one
    grid_maxima = {n: max(x**n for x in fixed_grid) for n in ns}
    moving_errors = {n: (2 ** (-1 / n)) ** n for n in ns}
    assert all(math.isclose(value, 0.5, abs_tol=2e-15) for value in moving_errors.values())
    assert all(0.0 < grid_maxima[n] < 1.0 for n in ns)
    true_supremum = 1.0
    return {
        "ns": ns,
        "xs": xs,
        "curves": curves,
        "grid_maxima": grid_maxima,
        "moving_errors": moving_errors,
        "true_supremum": true_supremum,
    }


def float_audit() -> dict[str, object]:
    ns = list(range(1, 81))
    exact_bits = ns[:]
    values = [1.0 + 2.0 ** (-n) for n in ns]
    stored_errors = [abs(value - 1.0) for value in values]
    first_equal = next(n for n, value in zip(ns, values) if value == 1.0)
    assert first_equal == 53
    assert values[51] > 1.0  # n = 52
    assert values[52] == 1.0  # n = 53
    stored_bits = [(-math.log2(error) if error > 0.0 else None) for error in stored_errors]
    return {
        "ns": ns,
        "exact_bits": exact_bits,
        "stored_errors": stored_errors,
        "stored_bits": stored_bits,
        "first_equal": first_equal,
        "ulp_one": math.ulp(1.0),
    }


def map_linear(value: float, lo: float, hi: float, px0: float, px1: float) -> float:
    return px0 + (value - lo) * (px1 - px0) / (hi - lo)


def map_log10(value: float, lo_exp: float, hi_exp: float, py0: float, py1: float) -> float:
    exponent = math.log10(max(value, 10**lo_exp))
    return py1 - (exponent - lo_exp) * (py1 - py0) / (hi_exp - lo_exp)


def axes(svg: SVG, left: float, top: float, width: float, height: float, x_ticks: list[tuple[float, str]], y_ticks: list[tuple[float, str]], x_map, y_map) -> None:
    for value, label in x_ticks:
        x = x_map(value)
        svg.line(x, top, x, top + height, "grid")
        svg.text(x, top + height + 18, label, "small", "middle")
    for value, label in y_ticks:
        y = y_map(value)
        svg.line(left, y, left + width, y, "grid")
        svg.text(left - 8, y + 4, label, "small", "end")
    svg.line(left, top + height, left + width, top + height, "axis")
    svg.line(left, top, left, top + height, "axis")


def draw_geometric(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "A · epsilon–N tail witness")
    left, top, pw, ph = x + 62, y + 55, w - 90, h - 122
    x_map = lambda value: map_linear(value, 0, 1500, left, left + pw)
    y_map = lambda value: map_log10(value, -7, 0, top, top + ph)
    axes(svg, left, top, pw, ph, [(0, "0"), (500, "500"), (1000, "1000"), (1500, "1500")], [(1, "10^0"), (1e-2, "10^-2"), (1e-4, "10^-4"), (1e-6, "10^-6")], x_map, y_map)
    colors = {0.5: "blue", 0.8: "orange", 0.99: "green"}
    for q in data["qs"]:
        points = [(x_map(n), y_map(value)) for n, value in zip(data["steps"], data["curves"][q]) if value >= 1e-7]
        svg.polyline(points, colors[q])
    threshold_y = y_map(data["epsilon"])
    svg.line(left, threshold_y, left + pw, threshold_y, "red dash")
    svg.text(left + 6, threshold_y - 7, "epsilon = 10^-6", "small")
    svg.text(left + 12, top + 18, "q=.5  N=20", "small")
    svg.text(left + 132, top + 18, "q=.8  N=62", "small")
    svg.text(left + 255, top + 18, "q=.99  N=1375", "small")
    svg.text(left + pw / 2, top + ph + 40, "iteration n", "label", "middle")


def draw_newton(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "B · Rational Cauchy, missing limit")
    left, top, pw, ph = x + 62, y + 55, w - 90, h - 122
    x_map = lambda value: map_linear(value, 1, 8, left, left + pw)
    y_map = lambda value: map_log10(max(value, 1e-100), -100, 0, top, top + ph)
    axes(svg, left, top, pw, ph, [(1, "1"), (2, "2"), (4, "4"), (6, "6"), (8, "8")], [(1, "10^0"), (1e-20, "10^-20"), (1e-40, "10^-40"), (1e-60, "10^-60"), (1e-80, "10^-80"), (1e-100, "10^-100")], x_map, y_map)
    points = [(x_map(index + 1), y_map(error)) for index, error in enumerate(data["errors"])]
    svg.polyline(points, "purple")
    for px, py in points:
        svg.circle(px, py, 3.2, "#7b61c9")
    svg.text(left + 12, top + 18, "x_(k+1) = (x_k + 2/x_k)/2; every x_k is rational", "small")
    svg.text(left + 12, top + 38, "limit in R = sqrt(2), but sqrt(2) is not in Q", "small")
    svg.text(left + pw / 2, top + ph + 40, "Newton step k", "label", "middle")


def draw_function_sequence(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "C · Pointwise x^n and moving input")
    left, top, pw, ph = x + 62, y + 55, w - 90, h - 122
    x_map = lambda value: map_linear(value, 0, 1, left, left + pw)
    y_map = lambda value: map_linear(value, 0, 1, top + ph, top)
    axes(svg, left, top, pw, ph, [(0, "0"), (0.25, ".25"), (0.5, ".5"), (0.75, ".75"), (1, "1")], [(0, "0"), (0.5, ".5"), (1, "1")], x_map, y_map)
    classes = {1: "blue", 4: "orange", 16: "green", 64: "purple"}
    for n in data["ns"]:
        svg.polyline([(x_map(xv), y_map(yv)) for xv, yv in zip(data["xs"], data["curves"][n])], classes[n])
    svg.text(left + 12, top + 18, "n = 1 / 4 / 16 / 64", "small")
    svg.text(left + 12, top + 38, "true sup error = 1 for every n; moving witness has error 1/2", "small")
    svg.text(left + pw / 2, top + ph + 40, "input x", "label", "middle")


def draw_float(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "D · Binary64 saturation")
    left, top, pw, ph = x + 62, y + 55, w - 90, h - 122
    x_map = lambda value: map_linear(value, 1, 80, left, left + pw)
    y_map = lambda value: map_linear(value, 0, 80, top + ph, top)
    axes(svg, left, top, pw, ph, [(1, "1"), (20, "20"), (40, "40"), (53, "53"), (60, "60"), (80, "80")], [(0, "0"), (20, "20"), (40, "40"), (52, "52"), (80, "80")], x_map, y_map)
    exact_points = [(x_map(n), y_map(bits)) for n, bits in zip(data["ns"], data["exact_bits"])]
    stored_points = [(x_map(n), y_map(bits)) for n, bits in zip(data["ns"], data["stored_bits"]) if bits is not None]
    svg.polyline(exact_points, "blue")
    svg.polyline(stored_points, "orange")
    stop_x = x_map(data["first_equal"])
    svg.line(stop_x, top, stop_x, top + ph, "red dash")
    svg.text(stop_x + 7, top + 18, "first stored x_n == 1 at n=53", "small")
    svg.text(left + 12, top + 38, "blue: exact -log2(error); orange: binary64 until error becomes zero", "small")
    svg.text(left + pw / 2, top + ph + 40, "n", "label", "middle")


def build_svg(output: Path) -> tuple[str, dict[str, object]]:
    geometric = geometric_audit()
    newton = rational_newton_audit()
    functions = function_sequence_audit()
    floats = float_audit()
    svg = SVG()
    draw_geometric(svg, geometric, 30, 85, 680, 345)
    draw_newton(svg, newton, 730, 85, 680, 345)
    draw_function_sequence(svg, functions, 30, 450, 680, 345)
    draw_float(svg, floats, 730, 450, 680, 345)
    content = svg.finish()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    summary = {
        "geometric_thresholds": geometric["thresholds"],
        "newton_last_fraction_digits": (len(str(newton["values"][-1].numerator)), len(str(newton["values"][-1].denominator))),
        "newton_last_float_error": newton["errors"][-1],
        "function_true_supremum": functions["true_supremum"],
        "function_n64_fixed_grid_max": functions["grid_maxima"][64],
        "binary64_first_equal": floats["first_equal"],
        "binary64_ulp_one": floats["ulp_one"],
    }
    return content, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/math-foundations/plot-sequence-limit-completeness-audit-v2.svg"),
    )
    args = parser.parse_args()
    content, summary = build_svg(args.output)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    print(f"wrote={args.output}")
    print(f"sha256={digest}")
    for key, value in summary.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
