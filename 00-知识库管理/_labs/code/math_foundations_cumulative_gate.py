#!/usr/bin/env python3
"""Deterministic three-track gate for MATH-CUM-01.

Only the Python standard library is used.  The SVG is deliberately generated
from analytic/enumerated quantities so a second run is byte-for-byte identical.
"""

from __future__ import annotations

import argparse
import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理/_assets/plots/math-foundations/"
    / "plot-math-foundations-cumulative-gate-v2.svg"
)

BG = "#ffffff"
PANEL = "#fffefb"
INK = "#1f2937"
MUTED = "#64748b"
GRID = "#d7dee8"
BLUE = "#2563eb"
RED = "#dc4545"
GREEN = "#16836b"
ORANGE = "#d97706"
PURPLE = "#7c3aed"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain-size", type=int, default=4)
    parser.add_argument("--contraction", type=float, default=0.8)
    parser.add_argument("--forcing-rate", type=float, default=0.6)
    parser.add_argument("--forcing", type=float, default=0.5)
    parser.add_argument("--dimension", type=int, default=512)
    parser.add_argument("--feature-rank", type=int, default=64)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, size: int = 14, color: str = INK,
         weight: int = 400, anchor: str = "start") -> str:
    size = max(size, 15)
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">'
        f'{esc(value)}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID,
         width: float = 1.0, dash: str | None = None) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width:.2f}"{extra}/>'
    )


def rect(x: float, y: float, w: float, h: float, fill: str,
         stroke: str = "none", radius: float = 0.0, opacity: float = 1.0) -> str:
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
        f'rx="{radius:.2f}" fill="{fill}" stroke="{stroke}" opacity="{opacity:.3f}"/>'
    )


def circle(x: float, y: float, r: float, fill: str, stroke: str = "none") -> str:
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" '
        f'fill="{fill}" stroke="{stroke}"/>'
    )


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.5,
             dash: str | None = None) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width:.2f}" stroke-linejoin="round" '
        f'stroke-linecap="round"{extra}/>'
    )


def enumerate_relations(m: int) -> tuple[int, int, int, int]:
    if m <= 0 or m > 4:
        raise ValueError("--domain-size must be in 1..4 for full enumeration")
    total = 1 << (m * m)
    pointwise = 0
    uniform = 0
    for bits in range(total):
        every_row_has_witness = True
        for row in range(m):
            row_mask = ((1 << m) - 1) << (row * m)
            if bits & row_mask == 0:
                every_row_has_witness = False
                break
        some_column_is_universal = False
        for col in range(m):
            if all(bits & (1 << (row * m + col)) for row in range(m)):
                some_column_is_universal = True
                break
        pointwise += int(every_row_has_witness)
        uniform += int(some_column_is_universal)
        if some_column_is_universal and not every_row_has_witness:
            raise AssertionError("uniform witness must imply row-wise witnesses")
    return total, pointwise, uniform, pointwise - uniform


def recurrence_values(q: float, r: float, forcing: float, steps: int = 100) -> tuple[list[float], list[float], float]:
    if not (0.0 < r < q < 1.0):
        raise ValueError("require 0 < forcing-rate < contraction < 1")
    if forcing <= 0.0:
        raise ValueError("--forcing must be positive")
    values = [1.0]
    for k in range(steps):
        values.append(q * values[-1] + forcing * (r ** k))
    coefficient = forcing / (q - r)
    closed = [(1.0 + coefficient) * q ** k - coefficient * r ** k for k in range(steps + 1)]
    maximum_error = max(abs(a - b) for a, b in zip(values, closed))
    if maximum_error > 2e-14:
        raise AssertionError("recurrence and closed form disagree")
    envelope = [(1.0 + coefficient) * q ** k for k in range(steps + 1)]
    if any(v < -1e-15 or v > u + 2e-14 for v, u in zip(values, envelope)):
        raise AssertionError("recurrence escaped its proof envelope")
    return values, envelope, maximum_error


def strict_certificate(epsilon: float, q: float, coefficient: float) -> int:
    raw = math.log(coefficient / epsilon) / math.log(1.0 / q)
    return max(0, math.floor(raw) + 1)


def exact_first_below(values: list[float], epsilon: float) -> int:
    for k, value in enumerate(values):
        if value < epsilon:
            return k
    raise ValueError("increase recurrence steps")


def ols_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum((x - mx) ** 2 for x in lx)


def map_linear(value: float, lo: float, hi: float, out_lo: float, out_hi: float) -> float:
    return out_lo + (value - lo) * (out_hi - out_lo) / (hi - lo)


def panel_shell(parts: list[str], x: float, title_label: str, subtitle: str) -> None:
    parts.append(rect(x, 86, 440, 430, PANEL, GRID, 14))
    parts.append(text(x + 18, 116, title_label, 17, INK, 700))
    parts.append(text(x + 18, 138, subtitle, 12, MUTED))


def draw_panel_a(parts: list[str], x: float, total: int, pointwise: int,
                 uniform: int, gap: int, m: int) -> None:
    panel_shell(parts, x, "A  量词换序的有限反模型", "枚举全部 Boolean relations；计数是有限定理")
    chart_x = x + 30
    chart_y = 170
    chart_w = 250
    chart_h = 185
    labels = ["∀x∃y", "∃y∀x", "换序缺口"]
    values = [pointwise, uniform, gap]
    colors = [BLUE, GREEN, RED]
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        yy = chart_y + chart_h * (1.0 - tick)
        parts.append(line(chart_x, yy, chart_x + chart_w, yy, GRID, 1))
        parts.append(text(chart_x - 7, yy + 4, f"{int(total * tick / 1000)}k", 10, MUTED, 400, "end"))
    bar_w = 52
    for idx, (label, value, color) in enumerate(zip(labels, values, colors)):
        bx = chart_x + 28 + idx * 75
        bh = chart_h * value / total
        by = chart_y + chart_h - bh
        parts.append(rect(bx, by, bar_w, bh, color, radius=5, opacity=0.9))
        parts.append(text(bx + bar_w / 2, by - 8, f"{value:,}", 11, color, 700, "middle"))
        parts.append(text(bx + bar_w / 2, chart_y + chart_h + 20, label, 11, INK, 600, "middle"))

    mx = x + 310
    my = 182
    cell = 24
    parts.append(text(mx + cell * 2, my - 13, "反例 R(x,y) ⇔ x=y", 11, PURPLE, 700, "middle"))
    for row in range(m):
        parts.append(text(mx - 8, my + row * cell + 17, f"x{row}", 9, MUTED, 400, "end"))
        for col in range(m):
            fill = PURPLE if row == col else "#eef1f6"
            parts.append(rect(mx + col * cell, my + row * cell, cell - 2, cell - 2, fill, radius=3))
            parts.append(text(mx + col * cell + 11, my + row * cell + 16,
                              "1" if row == col else "0", 10,
                              "#ffffff" if row == col else MUTED, 700, "middle"))
    parts.append(text(mx + cell * 2, my + m * cell + 19, "每行有 1；没有全 1 列", 10, MUTED, 400, "middle"))
    parts.append(rect(x + 24, 397, 392, 88, "#f2f6ff", radius=8))
    parts.append(text(x + 38, 422, "能推出", 11, BLUE, 700))
    parts.append(text(x + 103, 422, "在 4×4 有限域中，uniform ⇒ pointwise", 11, INK))
    parts.append(text(x + 38, 450, "不能推出", 11, RED, 700))
    parts.append(text(x + 103, 450, "任意无穷域上的量词定理；真实模型的性质", 11, INK))
    parts.append(text(x + 38, 477, f"全部关系 {total:,}；换序反例 {gap:,}", 11, MUTED))


def draw_panel_b(parts: list[str], x: float, values: list[float], envelope: list[float],
                 certificates: list[tuple[float, int, int]]) -> None:
    panel_shell(parts, x, "B  递推 → 界 → 极限 → 步数", "同一 proof certificate 串联 MATH-05—08")
    px0, px1 = x + 54, x + 410
    py0, py1 = 170, 360
    k_max = 95
    log_lo, log_hi = -9.5, 1.0
    for exponent in [-8, -6, -4, -2, 0]:
        yy = map_linear(exponent, log_lo, log_hi, py1, py0)
        parts.append(line(px0, yy, px1, yy, GRID, 1))
        parts.append(text(px0 - 8, yy + 4, f"10^{exponent}", 10, MUTED, 400, "end"))
    for kval in [0, 20, 40, 60, 80]:
        xx = map_linear(kval, 0, k_max, px0, px1)
        parts.append(line(xx, py0, xx, py1, GRID, 1))
        parts.append(text(xx, py1 + 19, kval, 10, MUTED, 400, "middle"))
    exact_points = []
    bound_points = []
    for k in range(k_max + 1):
        xx = map_linear(k, 0, k_max, px0, px1)
        exact_points.append((xx, map_linear(math.log10(values[k]), log_lo, log_hi, py1, py0)))
        bound_points.append((xx, map_linear(math.log10(envelope[k]), log_lo, log_hi, py1, py0)))
    parts.append(polyline(bound_points, ORANGE, 2.2, "7 5"))
    parts.append(polyline(exact_points, BLUE, 2.8))
    parts.append(line(x + 72, 382, x + 100, 382, BLUE, 2.8))
    parts.append(text(x + 108, 386, "exact eₖ", 11, INK))
    parts.append(line(x + 201, 382, x + 229, 382, ORANGE, 2.2, "7 5"))
    parts.append(text(x + 237, 386, "3.5·0.8ᵏ envelope", 11, INK))
    parts.append(rect(x + 24, 404, 392, 82, "#fff8ec", radius=8))
    parts.append(text(x + 38, 426, "ε", 10, MUTED, 700))
    parts.append(text(x + 110, 426, "证书 N", 10, MUTED, 700))
    parts.append(text(x + 200, 426, "真实首达", 10, MUTED, 700))
    for idx, (eps, cert, exact) in enumerate(certificates):
        yy = 446 + idx * 13
        parts.append(text(x + 38, yy, f"{eps:.0e}", 10, INK))
        parts.append(text(x + 123, yy, cert, 10, ORANGE, 700, "middle"))
        parts.append(text(x + 224, yy, exact, 10, BLUE, 700, "middle"))
    parts.append(text(x + 300, 453, "固定 q=0.8", 10, MUTED))
    parts.append(text(x + 300, 470, "N(ε)=Θ(log 1/ε)", 10, GREEN, 700))


def draw_panel_c(parts: list[str], x: float, lengths: list[float], curves: list[tuple[str, list[float], str]],
                 slopes: dict[str, float], d: int, rank: int) -> None:
    panel_shell(parts, x, "C  Attention 复杂度制度", "解析 operation proxy；不是 GPU wall-time")
    px0, px1 = x + 58, x + 414
    py0, py1 = 170, 365
    lx0, lx1 = math.log2(min(lengths)), math.log2(max(lengths))
    all_logs = [math.log10(v) for _, ys, _ in curves for v in ys]
    ly0 = math.floor(min(all_logs))
    ly1 = math.ceil(max(all_logs))
    for exponent in range(ly0, ly1 + 1, 2):
        yy = map_linear(exponent, ly0, ly1, py1, py0)
        parts.append(line(px0, yy, px1, yy, GRID, 1))
        parts.append(text(px0 - 8, yy + 4, f"10^{exponent}", 10, MUTED, 400, "end"))
    for exponent in [5, 7, 9, 11, 13]:
        if lx0 <= exponent <= lx1:
            xx = map_linear(exponent, lx0, lx1, px0, px1)
            parts.append(line(xx, py0, xx, py1, GRID, 1))
            parts.append(text(xx, py1 + 19, f"2^{exponent}", 10, MUTED, 400, "middle"))
    for label, ys, color in curves:
        points = []
        for length, value in zip(lengths, ys):
            xx = map_linear(math.log2(length), lx0, lx1, px0, px1)
            yy = map_linear(math.log10(value), ly0, ly1, py1, py0)
            points.append((xx, yy))
        parts.append(polyline(points, color, 2.6))
        for xx, yy in points:
            parts.append(circle(xx, yy, 2.6, color))
    legend_y = 392
    for idx, (label, _, color) in enumerate(curves):
        xx = x + 34 + (idx % 2) * 205
        yy = legend_y + (idx // 2) * 20
        parts.append(line(xx, yy, xx + 24, yy, color, 2.6))
        parts.append(text(xx + 31, yy + 4, f"{label}: p={slopes[label]:.3f}", 10, INK))
    parts.append(rect(x + 24, 440, 392, 47, "#f0fbf7", radius=8))
    parts.append(text(x + 38, 461, f"d={d}, fixed r={rank}: linear；r=T/4: quadratic", 10, GREEN, 700))
    parts.append(text(x + 38, 478, "改变 r(T) 就改变 theorem；memory 与 work 分账", 10, MUTED))


def build_svg(total: int, pointwise: int, uniform: int, gap: int, m: int,
              values: list[float], envelope: list[float], certificates: list[tuple[float, int, int]],
              lengths: list[float], curves: list[tuple[str, list[float], str]], slopes: dict[str, float],
              d: int, rank: int) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="540" viewBox="0 0 1440 540" role="img" aria-labelledby="title desc">',
        '<title id="title">数学语言、逻辑与证明累计复现门</title>',
        '<desc id="desc">三面板展示有限量词换序反例、递推误差证书与不同增长制度下的复杂度曲线。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}</style>',
        rect(0, 0, 1440, 540, BG),
        text(40, 38, "MATH-CUM-01 · 量词—证明—复杂度三轨复现门", 24, INK, 750),
        text(40, 66, "有限枚举负责找反例，解析界负责无限结论，复杂度曲线必须绑定增长制度", 13, MUTED),
    ]
    draw_panel_a(parts, 30, total, pointwise, uniform, gap, m)
    draw_panel_b(parts, 500, values, envelope, certificates)
    draw_panel_c(parts, 970, lengths, curves, slopes, d, rank)
    parts.append(text(720, 531, "Generated deterministically with Python standard library · composed ≠ mastered", 10, MUTED, 400, "middle"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    args = parse_args()
    total, pointwise, uniform, gap = enumerate_relations(args.domain_size)
    expected_pointwise = ((1 << args.domain_size) - 1) ** args.domain_size
    if pointwise != expected_pointwise:
        raise AssertionError("row-wise count disagrees with product rule")

    values, envelope, maximum_error = recurrence_values(
        args.contraction, args.forcing_rate, args.forcing, steps=120
    )
    coefficient = 1.0 + args.forcing / (args.contraction - args.forcing_rate)
    epsilons = [1e-2, 1e-4, 1e-6, 1e-8]
    certificates = [
        (eps, strict_certificate(eps, args.contraction, coefficient), exact_first_below(values, eps))
        for eps in epsilons
    ]

    lengths = [float(32 * (2 ** i)) for i in range(9)]
    dense = [4.0 * t * args.dimension ** 2 + 2.0 * t ** 2 * args.dimension for t in lengths]
    fixed = [4.0 * t * args.dimension * args.feature_rank for t in lengths]
    adaptive = [4.0 * t * args.dimension * (t / 4.0) for t in lengths]
    memory = [t ** 2 for t in lengths]
    curves = [
        ("dense work", dense, BLUE),
        ("fixed-r work", fixed, GREEN),
        ("r=T/4 work", adaptive, RED),
        ("score elements", memory, PURPLE),
    ]
    slopes = {label: ols_slope(lengths, ys) for label, ys, _ in curves}
    if abs(slopes["fixed-r work"] - 1.0) > 1e-12:
        raise AssertionError("fixed-r work should be exactly linear")
    if abs(slopes["r=T/4 work"] - 2.0) > 1e-12:
        raise AssertionError("adaptive rank should be exactly quadratic")
    if abs(slopes["score elements"] - 2.0) > 1e-12:
        raise AssertionError("dense score elements should be quadratic")

    svg = build_svg(
        total, pointwise, uniform, gap, args.domain_size,
        values, envelope, certificates,
        lengths, curves, slopes, args.dimension, args.feature_rank,
    )
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")

    cert_summary = ",".join(f"{eps:.0e}:{cert}/{exact}" for eps, cert, exact in certificates)
    print(
        f"relations total={total} pointwise={pointwise} uniform={uniform} swap_gap={gap}"
    )
    print(
        f"recurrence max_closed_form_error={maximum_error:.3e} certificates={cert_summary}"
    )
    print(
        "complexity "
        f"dense_slope={slopes['dense work']:.6f} "
        f"fixed_rank_slope={slopes['fixed-r work']:.6f} "
        f"adaptive_rank_slope={slopes['r=T/4 work']:.6f} "
        f"score_slope={slopes['score elements']:.6f}"
    )
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
