#!/usr/bin/env python3
"""Deterministic MATH-08 audits for asymptotics and AI complexity.

Standard-library only. The script generates a four-panel SVG: classical growth
families, exact loop counters with log-log fits, finite-window local slopes, and
dense-attention projection/pairwise/memory regimes.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


def esc(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, width: int = 1440, height: int = 820) -> None:
        self.width = width
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-08 asymptotics, finite-window slopes, and attention cost audit</title>',
            '<desc id="desc">Four scientific panels compare growth families, exact linear and triangular operation counters, local slopes caused by lower-order terms and loss floors, and dense attention projection versus pairwise regimes.</desc>',
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
            ".red{stroke:#cb445a;fill:none;stroke-width:2.4}.gray{stroke:#7e8b9f;fill:none;stroke-width:2}",
            ".dash{stroke-dasharray:7 5}.dot{stroke-dasharray:3 4}",
            "</style>",
            '<rect width="1440" height="820" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-08 audit · asymptotic hierarchy, exact counts, finite slopes, and attention regimes</text>',
            '<text x="36" y="62" class="sub">Finite curves diagnose constants and crossovers; only the quantified proof establishes an infinite-tail asymptotic relation.</text>',
        ]

    def text(self, x: float, y: float, value: object, cls: str = "label", anchor: str = "start") -> None:
        self.parts.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>')

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str = "none", rx: float = 6) -> None:
        self.parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}"/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str = "grid") -> None:
        self.parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>')

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def circle(self, x: float, y: float, r: float, fill: str) -> None:
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}"/>')

    def panel(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def map_linear(value: float, lo: float, hi: float, px0: float, px1: float) -> float:
    return px0 + (value - lo) * (px1 - px0) / (hi - lo)


def map_log(value: float, lo: float, hi: float, px0: float, px1: float) -> float:
    return map_linear(math.log10(value), math.log10(lo), math.log10(hi), px0, px1)


def map_y_log(value: float, lo: float, hi: float, top: float, bottom: float) -> float:
    return bottom - (math.log10(value) - math.log10(lo)) * (bottom - top) / (math.log10(hi) - math.log10(lo))


def axes(
    svg: SVG,
    left: float,
    top: float,
    width: float,
    height: float,
    x_ticks: list[tuple[float, str]],
    y_ticks: list[tuple[float, str]],
    x_map,
    y_map,
) -> None:
    for value, label in x_ticks:
        px = x_map(value)
        svg.line(px, top, px, top + height, "grid")
        svg.text(px, top + height + 18, label, "small", "middle")
    for value, label in y_ticks:
        py = y_map(value)
        svg.line(left, py, left + width, py, "grid")
        svg.text(left - 8, py + 4, label, "small", "end")
    svg.line(left, top + height, left + width, top + height, "axis")
    svg.line(left, top, left, top + height, "axis")


def ols_slope(xs: list[float], ys: list[float]) -> float:
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    numerator = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    denominator = sum((x - xbar) ** 2 for x in xs)
    return numerator / denominator


def growth_data() -> dict[str, object]:
    ns = list(range(2, 33))
    curves = {
        "log2 n": [math.log2(n) for n in ns],
        "n": [float(n) for n in ns],
        "n log2 n": [n * math.log2(n) for n in ns],
        "n^2": [float(n * n) for n in ns],
        "2^n": [2.0**n for n in ns],
    }
    assert curves["2^n"][-1] == 2.0**32
    return {"ns": ns, "curves": curves}


def counter_data() -> dict[str, object]:
    ns = [2**k for k in range(2, 11)]
    linear = [n for n in ns]
    triangular = [n * (n + 1) // 2 for n in ns]
    logn = [math.log(n) for n in ns]
    slope_linear = ols_slope(logn, [math.log(v) for v in linear])
    slope_triangular = ols_slope(logn, [math.log(v) for v in triangular])
    assert abs(slope_linear - 1.0) < 1e-12
    assert 1.95 < slope_triangular < 2.0
    for n, value in zip(ns, triangular):
        counted = sum(1 for i in range(1, n + 1) for _ in range(1, i + 1))
        assert counted == value
    return {
        "ns": ns,
        "linear": linear,
        "triangular": triangular,
        "slope_linear": slope_linear,
        "slope_triangular": slope_triangular,
    }


def slope_data() -> dict[str, object]:
    ns = [10 ** (1 + 5 * i / 100) for i in range(101)]
    mixed = [(2 * n + 1000) / (n + 1000) for n in ns]
    raw_loss = [-0.6 * (3 * n**-0.6) / (2 + 3 * n**-0.6) for n in ns]
    corrected = [-0.6 for _ in ns]
    assert mixed[0] < 1.02 and mixed[-1] > 1.99
    assert abs(raw_loss[-1]) < abs(raw_loss[0])
    return {"ns": ns, "mixed": mixed, "raw_loss": raw_loss, "corrected": corrected}


def attention_data() -> dict[str, object]:
    d, h = 512, 8
    ts = [2**k for k in range(5, 14)]
    projection = [4 * t * d * d for t in ts]
    pairwise = [2 * t * t * d for t in ts]
    score_elements = [h * t * t for t in ts]
    crossover = 2 * d
    idx = ts.index(crossover)
    assert projection[idx] == pairwise[idx]
    return {
        "d": d,
        "h": h,
        "ts": ts,
        "projection": projection,
        "pairwise": pairwise,
        "score_elements": score_elements,
        "crossover": crossover,
    }


def draw_growth(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "A · Growth hierarchy")
    left, top, pw, ph = x + 62, y + 55, w - 92, h - 120
    x_map = lambda v: map_linear(v, 2, 32, left, left + pw)
    y_map = lambda v: map_y_log(v, 1, 1e10, top, top + ph)
    axes(svg, left, top, pw, ph, [(2, "2"), (8, "8"), (16, "16"), (24, "24"), (32, "32")], [(1, "10^0"), (1e2, "10^2"), (1e4, "10^4"), (1e6, "10^6"), (1e8, "10^8"), (1e10, "10^10")], x_map, y_map)
    styles = {"log2 n": "gray", "n": "blue", "n log2 n": "green", "n^2": "orange", "2^n": "red"}
    for name, values in data["curves"].items():
        svg.polyline([(x_map(n), y_map(v)) for n, v in zip(data["ns"], values)], styles[name])
    legend = [("log2 n", "#7e8b9f"), ("n", "#2672dd"), ("n log2 n", "#169873"), ("n^2", "#e77817"), ("2^n", "#cb445a")]
    for index, (name, color) in enumerate(legend):
        lx = left + 10 + (index % 3) * 105
        ly = top + 17 + (index // 3) * 20
        svg.circle(lx, ly - 4, 3.5, color)
        svg.text(lx + 8, ly, name, "small")
    svg.text(left + pw / 2, top + ph + 40, "n", "label", "middle")


def draw_counter(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "B · Exact counters and finite slopes")
    left, top, pw, ph = x + 62, y + 55, w - 92, h - 120
    x_map = lambda v: map_log(v, 4, 1024, left, left + pw)
    y_map = lambda v: map_y_log(v, 1, 1e6, top, top + ph)
    axes(svg, left, top, pw, ph, [(4, "4"), (16, "16"), (64, "64"), (256, "256"), (1024, "1024")], [(1, "10^0"), (1e2, "10^2"), (1e4, "10^4"), (1e6, "10^6")], x_map, y_map)
    linear_points = [(x_map(n), y_map(v)) for n, v in zip(data["ns"], data["linear"])]
    triangle_points = [(x_map(n), y_map(v)) for n, v in zip(data["ns"], data["triangular"])]
    svg.polyline(linear_points, "blue")
    svg.polyline(triangle_points, "orange")
    for px, py in linear_points:
        svg.circle(px, py, 3, "#2672dd")
    for px, py in triangle_points:
        svg.circle(px, py, 3, "#e77817")
    svg.text(left + 10, top + 18, f"linear count: slope = {data['slope_linear']:.3f}", "small")
    svg.text(left + 10, top + 38, f"n(n+1)/2: slope = {data['slope_triangular']:.3f}", "small")
    svg.text(left + pw / 2, top + ph + 40, "n (log scale)", "label", "middle")


def draw_slopes(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "C · Local slope diagnoses regimes")
    left, top, pw, ph = x + 62, y + 55, w - 92, h - 120
    x_map = lambda v: map_log(v, 10, 1e6, left, left + pw)
    y_map = lambda v: map_linear(v, -0.8, 2.2, top + ph, top)
    axes(svg, left, top, pw, ph, [(10, "10"), (100, "10^2"), (1e3, "10^3"), (1e4, "10^4"), (1e6, "10^6")], [(-0.6, "-.6"), (0, "0"), (1, "1"), (2, "2")], x_map, y_map)
    svg.polyline([(x_map(n), y_map(v)) for n, v in zip(data["ns"], data["mixed"])], "orange")
    svg.polyline([(x_map(n), y_map(v)) for n, v in zip(data["ns"], data["raw_loss"])], "purple")
    svg.polyline([(x_map(n), y_map(v)) for n, v in zip(data["ns"], data["corrected"])], "green dash")
    svg.text(left + 10, top + 18, "n^2 + 1000n: local slope 1 → 2", "small")
    svg.text(left + 10, top + 38, "raw log loss: slope → 0; floor-corrected: -0.6", "small")
    svg.text(left + pw / 2, top + ph + 40, "scale (log)", "label", "middle")


def draw_attention(svg: SVG, data: dict[str, object], x: float, y: float, w: float, h: float) -> None:
    svg.panel(x, y, w, h, "D · Attention arithmetic vs memory")
    left, top, pw, ph = x + 62, y + 55, w - 92, h - 120
    x_map = lambda v: map_log(v, 32, 8192, left, left + pw)
    y_map = lambda v: map_y_log(v, 1e6, 1e12, top, top + ph)
    axes(svg, left, top, pw, ph, [(32, "32"), (128, "128"), (512, "512"), (2048, "2048"), (8192, "8192")], [(1e6, "10^6"), (1e8, "10^8"), (1e10, "10^10"), (1e12, "10^12")], x_map, y_map)
    svg.polyline([(x_map(t), y_map(v)) for t, v in zip(data["ts"], data["projection"])], "blue")
    svg.polyline([(x_map(t), y_map(v)) for t, v in zip(data["ts"], data["pairwise"])], "red")
    # Values below the displayed 1e6 lower bound sit on the plotting floor;
    # clipping them here keeps the research curve inside the panel contract.
    svg.polyline([(x_map(t), y_map(max(v, 1e6))) for t, v in zip(data["ts"], data["score_elements"])], "purple dash")
    cx = x_map(data["crossover"])
    svg.line(cx, top, cx, top + ph, "green dash")
    svg.text(cx + 5, top + 17, f"proxy crossover T=2d={data['crossover']}", "small")
    svg.text(left + 10, top + 38, "blue: 4Td^2 projection · red: 2T^2d pairwise", "small")
    svg.text(left + 10, top + 57, "purple: hT^2 score elements (different unit)", "small")
    svg.text(left + pw / 2, top + ph + 40, "sequence length T (log)", "label", "middle")


def build_svg() -> tuple[str, dict[str, object]]:
    growth = growth_data()
    counter = counter_data()
    slopes = slope_data()
    attention = attention_data()
    svg = SVG()
    draw_growth(svg, growth, 28, 86, 678, 338)
    draw_counter(svg, counter, 734, 86, 678, 338)
    draw_slopes(svg, slopes, 28, 448, 678, 338)
    draw_attention(svg, attention, 734, 448, 678, 338)
    metrics = {
        "linear_slope": counter["slope_linear"],
        "triangular_slope": counter["slope_triangular"],
        "mixed_slope_start": slopes["mixed"][0],
        "mixed_slope_end": slopes["mixed"][-1],
        "attention_crossover": attention["crossover"],
    }
    return svg.finish(), metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/math-foundations/plot-asymptotics-complexity-audit-v2.svg"),
    )
    args = parser.parse_args()
    content, metrics = build_svg()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    print(f"wrote {args.output}")
    print(f"sha256 {digest}")
    for key, value in metrics.items():
        print(f"{key} {value}")


if __name__ == "__main__":
    main()
