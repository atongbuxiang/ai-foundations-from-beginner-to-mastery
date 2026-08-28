#!/usr/bin/env python3
"""Deterministic three-track gate for GEO-CUM-01.

Track A audits sphere geometry and orthogonal covariance.  Track B separates
Hilbert projection, compact spectral tails, and kernel effective dimension.
Track C shows how one Poisson cutoff model has radically different errors in
L2, energy/H^-1, relative, and strong-residual topologies.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理/_assets/plots/geometry-functional/"
    / "plot-geometry-functional-cumulative-gate-v2.svg"
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
    parser.add_argument("--sphere-radius", type=float, default=1.0)
    parser.add_argument("--objective-y", type=float, default=2.0)
    parser.add_argument("--objective-z", type=float, default=-1.0)
    parser.add_argument("--rotation-angle", type=float, default=0.7)
    parser.add_argument("--spectral-size", type=int, default=131072)
    parser.add_argument("--coefficient-exponent", type=float, default=1.0)
    parser.add_argument("--eigen-exponent", type=float, default=2.0)
    parser.add_argument("--domain-length", type=float, default=1.0)
    parser.add_argument("--train-cutoff", type=int, default=8)
    parser.add_argument("--max-mode", type=int, default=64)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, size: int = 15, color: str = INK,
         weight: int = 400, anchor: str = "start") -> str:
    # Enforce the course minimum for auxiliary text on a standalone SVG.
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


def circle(x: float, y: float, radius: float, fill: str) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{fill}"/>'


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.5,
             dash: str | None = None) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width:.2f}" stroke-linejoin="round" '
        f'stroke-linecap="round"{extra}/>'
    )


def dot(x: list[float], y: list[float]) -> float:
    return sum(a * b for a, b in zip(x, y))


def norm(x: list[float]) -> float:
    return math.sqrt(dot(x, x))


def scale(a: float, x: list[float]) -> list[float]:
    return [a * value for value in x]


def add(x: list[float], y: list[float]) -> list[float]:
    return [a + b for a, b in zip(x, y)]


def sub(x: list[float], y: list[float]) -> list[float]:
    return [a - b for a, b in zip(x, y)]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [dot(row, vector) for row in matrix]


def sphere_gradient(point: list[float], parameter: list[float]) -> list[float]:
    radius_squared = dot(point, point)
    if radius_squared <= 0.0:
        raise ValueError("sphere point must be nonzero")
    return sub(parameter, scale(dot(point, parameter) / radius_squared, point))


def ols_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    denominator = sum((x - mx) ** 2 for x in lx)
    if denominator == 0.0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / denominator


def map_linear(value: float, lo: float, hi: float, out_lo: float, out_hi: float) -> float:
    return out_lo + (value - lo) * (out_hi - out_lo) / (hi - lo)


def geometry_track(
    radius: float,
    parameter_y: float,
    parameter_z: float,
    angle: float,
) -> dict[str, object]:
    if radius <= 0.0:
        raise ValueError("--sphere-radius must be positive")
    point = [radius, 0.0, 0.0]
    parameter = [1.0, parameter_y, parameter_z]
    gradient = sphere_gradient(point, parameter)
    gradient_norm = norm(gradient)
    if gradient_norm == 0.0:
        raise ValueError("--objective-y and --objective-z cannot both be zero")
    tangent = scale(1.0 / gradient_norm, gradient)
    hs = [2.0 ** (-k) for k in range(12, 1, -1)]
    ambient_residuals = []
    retraction_errors = []
    for h in hs:
        ambient = add(point, scale(h, tangent))
        ambient_residuals.append(abs(dot(ambient, ambient) - radius * radius))
        exponential = add(
            scale(math.cos(h / radius), point),
            scale(radius * math.sin(h / radius), tangent),
        )
        retraction = scale(radius / norm(ambient), ambient)
        retraction_errors.append(norm(sub(retraction, exponential)))
        if abs(norm(retraction) - radius) > 5e-16 * max(1.0, radius):
            raise AssertionError("normalization retraction left the sphere")

    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotation = [[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]]
    rotated_point = matvec(rotation, point)
    rotated_parameter = matvec(rotation, parameter)
    lhs = sphere_gradient(rotated_point, rotated_parameter)
    rhs = matvec(rotation, gradient)
    equivariance_error = norm(sub(lhs, rhs))
    if equivariance_error > 2e-15:
        raise AssertionError("sphere gradient covariance failed")

    return {
        "hs": hs,
        "ambient": ambient_residuals,
        "retraction": retraction_errors,
        "constraint_slope": ols_slope(hs, ambient_residuals),
        "retraction_slope": ols_slope(hs, retraction_errors),
        "equivariance_error": equivariance_error,
        "radius": radius,
        "parameter_y": parameter_y,
        "parameter_z": parameter_z,
        "angle": angle,
    }


def functional_track(
    size: int,
    coefficient_exponent: float,
    eigen_exponent: float,
) -> dict[str, object]:
    if size < 8192:
        raise ValueError("--spectral-size must be at least 8192")
    if coefficient_exponent <= 0.5:
        raise ValueError("--coefficient-exponent must exceed 0.5 for an l2 target")
    if eigen_exponent <= 0.0:
        raise ValueError("--eigen-exponent must be positive")
    ms = [2 ** k for k in range(2, 13)]
    prefix = [0.0]
    for j in range(1, size + 1):
        coefficient_square = (
            1.0 / (j * j)
            if coefficient_exponent == 1.0
            else j ** (-2.0 * coefficient_exponent)
        )
        prefix.append(prefix[-1] + coefficient_square)
    total = prefix[-1]
    projection_errors = [math.sqrt(total - prefix[m]) for m in ms]
    compact_tails = [
        1.0 / ((m + 1) ** 2)
        if eigen_exponent == 2.0
        else (m + 1) ** (-eigen_exponent)
        for m in ms
    ]

    lambdas = [10.0 ** (-exponent / 2.0) for exponent in range(2, 13)]
    effective_dimensions = []
    for regularization in lambdas:
        effective_dimensions.append(
            sum(
                1.0 / (
                    1.0
                    + (
                        regularization * j * j
                        if eigen_exponent == 2.0
                        else regularization * j ** eigen_exponent
                    )
                )
                for j in range(1, size + 1)
            )
        )
    effective_slope = ols_slope([1.0 / value for value in lambdas], effective_dimensions)
    return {
        "ms": ms,
        "projection": projection_errors,
        "compact": compact_tails,
        "projection_slope": ols_slope(ms, projection_errors),
        "compact_slope": ols_slope(ms, compact_tails),
        "lambdas": lambdas,
        "effective": effective_dimensions,
        "effective_slope": effective_slope,
        "effective_last": effective_dimensions[-1],
        "coefficient_exponent": coefficient_exponent,
        "eigen_exponent": eigen_exponent,
        "size": size,
    }


def pde_track(domain_length: float, train_cutoff: int, max_mode: int) -> dict[str, object]:
    if domain_length <= 0.0:
        raise ValueError("--domain-length must be positive")
    if train_cutoff < 1 or max_mode <= train_cutoff + 4:
        raise ValueError("require 1 <= train-cutoff < max-mode-4")
    modes = list(range(train_cutoff + 1, max_mode + 1))
    if domain_length == 1.0:
        l2_errors = [1.0 / ((math.pi * mode) ** 2) for mode in modes]
        energy_errors = [1.0 / (math.pi * mode) for mode in modes]
    else:
        l2_errors = [(domain_length / (math.pi * mode)) ** 2 for mode in modes]
        energy_errors = [domain_length / (math.pi * mode) for mode in modes]
    strong_residuals = [1.0 for _ in modes]
    return {
        "modes": modes,
        "l2": l2_errors,
        "energy": energy_errors,
        "strong": strong_residuals,
        "l2_slope": ols_slope(modes, l2_errors),
        "energy_slope": ols_slope(modes, energy_errors),
        "strong_slope": ols_slope(modes, strong_residuals),
        "last_l2": l2_errors[-1],
        "last_energy": energy_errors[-1],
        "domain_length": domain_length,
    }


def panel_shell(parts: list[str], x: float, title_label: str, subtitle: str) -> None:
    parts.append(rect(x, 86, 440, 470, PANEL, GRID, 14))
    parts.append(text(x + 18, 116, title_label, 22, INK, 700))
    parts.append(text(x + 18, 142, subtitle, 15, MUTED))


def draw_loglog(parts: list[str], xs: list[float], series: list[tuple[str, list[float], str]],
                x0: float, x1: float, y0: float, y1: float,
                lx0: float, lx1: float, ly0: float, ly1: float) -> None:
    for exponent in range(math.ceil(ly0), math.floor(ly1) + 1, 2):
        yy = map_linear(exponent, ly0, ly1, y1, y0)
        parts.append(line(x0, yy, x1, yy, GRID, 1))
        parts.append(text(x0 - 7, yy + 4, f"10^{exponent}", 9, MUTED, 400, "end"))
    for label, ys, color in series:
        points = []
        for x_value, y_value in zip(xs, ys):
            xx = map_linear(math.log10(x_value), lx0, lx1, x0, x1)
            yy = map_linear(math.log10(y_value), ly0, ly1, y1, y0)
            points.append((xx, yy))
        parts.append(polyline(points, color, 2.6))
        for xx, yy in points:
            parts.append(circle(xx, yy, 2.5, color))


def draw_panel_a(parts: list[str], x: float, data: dict[str, object]) -> None:
    canonical = (
        data["radius"] == 1.0
        and data["parameter_y"] == 2.0
        and data["parameter_z"] == -1.0
        and data["angle"] == 0.7
    )
    subtitle = (
        "ambient step、retraction、Exp 与 SO(3) covariance"
        if canonical
        else (
            f"S² radius={data['radius']:g}；c=(1,{data['parameter_y']:g},{data['parameter_z']:g})；"
            f"θ={data['angle']:g}"
        )
    )
    panel_shell(parts, x, "A  球面几何与对称", subtitle)
    xs = data["hs"]
    x0, x1, y0, y1 = x + 62, x + 412, 170, 315
    lx0, lx1 = math.log10(min(xs)), math.log10(max(xs))
    draw_loglog(
        parts, xs,
        [("constraint", data["ambient"], ORANGE), ("R−Exp", data["retraction"], BLUE)],
        x0, x1, y0, y1, lx0, lx1, -12.0, -1.0,
    )
    for exponent in [-3, -2, -1]:
        value = 10.0 ** exponent
        if min(xs) <= value <= max(xs):
            xx = map_linear(exponent, lx0, lx1, x0, x1)
            parts.append(line(xx, y0, xx, y1, GRID, 1))
            parts.append(text(xx, y1 + 18, f"10^{exponent}", 9, MUTED, 400, "middle"))
    parts.append(line(x + 78, 354, x + 103, 354, ORANGE, 2.6))
    parts.append(text(x + 111, 359, f"ambient constraint: p={data['constraint_slope']:.3f}", 10, INK))
    parts.append(line(x + 78, 379, x + 103, 379, BLUE, 2.6))
    parts.append(text(x + 111, 384, f"R−Exp: p={data['retraction_slope']:.3f}", 10, INK))
    parts.append(rect(x + 24, 410, 392, 113, "#f2f6ff", radius=8))
    parts.append(text(x + 38, 437, "解析对象", 10, BLUE, 700))
    parts.append(text(x + 112, 437, "constraint = h²；R−Exp = O(h³)", 10, INK))
    parts.append(text(x + 38, 465, "对称门", 10, GREEN, 700))
    parts.append(text(x + 112, 465, f"grad(Qp,Qc)−Qgrad(p,c) = {data['equivariance_error']:.1e}", 10, INK))
    parts.append(text(x + 38, 496, "边界：只验局部阶与协变，不证明全局坐标或最优性", 10, MUTED))


def draw_panel_b(parts: list[str], x: float, data: dict[str, object]) -> None:
    canonical = (
        data["size"] == 131072
        and data["coefficient_exponent"] == 1.0
        and data["eigen_exponent"] == 2.0
    )
    subtitle = (
        "同一谱中分离approximation tail与regularization capacity"
        if canonical
        else (
            f"N={data['size']}；cⱼ=j⁻{data['coefficient_exponent']:g}；"
            f"μⱼ=j⁻{data['eigen_exponent']:g}"
        )
    )
    panel_shell(parts, x, "B  Hilbert投影、紧谱与RKHS", subtitle)
    xs = data["ms"]
    x0, x1, y0, y1 = x + 62, x + 412, 170, 315
    lx0, lx1 = math.log10(min(xs)), math.log10(max(xs))
    draw_loglog(
        parts, xs,
        [("projection", data["projection"], GREEN), ("operator tail", data["compact"], PURPLE)],
        x0, x1, y0, y1, lx0, lx1, -8.0, 0.0,
    )
    for exponent in [1, 2, 3]:
        value = 10.0 ** exponent
        if min(xs) <= value <= max(xs):
            xx = map_linear(exponent, lx0, lx1, x0, x1)
            parts.append(line(xx, y0, xx, y1, GRID, 1))
            parts.append(text(xx, y1 + 18, f"10^{exponent}", 9, MUTED, 400, "middle"))
    parts.append(line(x + 78, 354, x + 103, 354, GREEN, 2.6))
    parts.append(text(x + 111, 359, f"∥c−Pₘc∥: p={data['projection_slope']:.3f}", 10, INK))
    parts.append(line(x + 78, 379, x + 103, 379, PURPLE, 2.6))
    parts.append(text(x + 111, 384, f"∥K−Kₘ∥: p={data['compact_slope']:.3f}", 10, INK))
    parts.append(rect(x + 24, 410, 392, 113, "#f0fbf7", radius=8))
    parts.append(text(x + 38, 437, "Kernel谱", 10, GREEN, 700))
    kernel_label = (
        "μⱼ=j⁻²；N_eff(λ)=Σ μ/(μ+λ)"
        if data["eigen_exponent"] == 2.0
        else f"μⱼ=j⁻{data['eigen_exponent']:g}；N_eff(λ)=Σ μ/(μ+λ)"
    )
    parts.append(text(x + 111, 437, kernel_label, 10, INK))
    parts.append(text(x + 38, 465, "容量斜率", 10, ORANGE, 700))
    parts.append(text(x + 111, 465, f"log N_eff vs log(1/λ): {data['effective_slope']:.3f}", 10, INK))
    parts.append(text(x + 38, 496, "边界：有限谱尾不是连续紧性的解析证明", 10, MUTED))


def draw_panel_c(parts: list[str], x: float, data: dict[str, object], cutoff: int, max_mode: int) -> None:
    canonical = data["domain_length"] == 1.0 and cutoff == 8 and max_mode == 64
    subtitle = (
        "cutoff model在不同function-space norms下并非同一误差"
        if canonical
        else f"(0,L), L={data['domain_length']:g}；train 1…{cutoff}；OOD {cutoff + 1}…{max_mode}"
    )
    panel_shell(parts, x, "C  弱PDE与算子泛化", subtitle)
    xs = data["modes"]
    x0, x1, y0, y1 = x + 62, x + 412, 170, 315
    lx0, lx1 = math.log10(min(xs)), math.log10(max(xs))
    draw_loglog(
        parts, xs,
        [("strong", data["strong"], RED), ("energy", data["energy"], ORANGE), ("L2", data["l2"], BLUE)],
        x0, x1, y0, y1, lx0, lx1, -5.0, 0.5,
    )
    for mode in [10, 20, 40, 60]:
        if min(xs) <= mode <= max(xs):
            xx = map_linear(math.log10(mode), lx0, lx1, x0, x1)
            parts.append(line(xx, y0, xx, y1, GRID, 1))
            parts.append(text(xx, y1 + 18, mode, 9, MUTED, 400, "middle"))
    legend = [
        (RED, f"strong residual: p={data['strong_slope']:.1f}"),
        (ORANGE, f"H¹/H⁻¹: p={data['energy_slope']:.1f}"),
        (BLUE, f"L² absolute: p={data['l2_slope']:.1f}"),
    ]
    for idx, (color, label) in enumerate(legend):
        yy = 350 + idx * 23
        parts.append(line(x + 38, yy, x + 60, yy, color, 2.6))
        parts.append(text(x + 68, yy + 5, label, 9, INK))
    parts.append(rect(x + 24, 424, 392, 99, "#fff3f2", radius=8))
    parts.append(text(x + 38, 450, "训练子空间", 10, GREEN, 700))
    parts.append(text(x + 123, 450, f"modes 1…{cutoff}；OOD {cutoff + 1}…{max_mode}", 10, INK))
    parts.append(text(x + 38, 477, "高频陷阱", 10, RED, 700))
    parts.append(text(x + 123, 477, f"j={max_mode}: L²={data['last_l2']:.2e}, relative=100%", 10, INK))
    parts.append(text(x + 38, 505, "边界：小绝对误差不保证小相对误差或小强残差", 10, MUTED))


def build_svg(geometry: dict[str, object], functional: dict[str, object],
              pde: dict[str, object], cutoff: int, max_mode: int) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="580" viewBox="0 0 1440 580" role="img" aria-labelledby="title desc">',
        '<title id="title">几何、泛函与算子累计复现门</title>',
        '<desc id="desc">三面板展示流形约束与等变性、Hilbert 投影与紧算子谱尾，以及弱 PDE 不同范数残差。</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}</style>',
        rect(0, 0, 1440, 580, BG),
        text(40, 38, "GEO-CUM-01 · 几何—泛函—弱PDE三轨复现门", 24, INK, 750),
        text(40, 66, "局部几何要过对称门，有限谱要过紧性门，离散残差要回到声明的函数空间范数", 15, MUTED),
    ]
    draw_panel_a(parts, 30, geometry)
    draw_panel_b(parts, 500, functional)
    draw_panel_c(parts, 970, pde, cutoff, max_mode)
    parts.append(text(720, 573, "Generated deterministically with Python standard library · composed ≠ mastered", 10, MUTED, 400, "middle"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    args = parse_args()
    canonical = (
        args.sphere_radius == 1.0
        and args.objective_y == 2.0
        and args.objective_z == -1.0
        and args.rotation_angle == 0.7
        and args.spectral_size == 131072
        and args.coefficient_exponent == 1.0
        and args.eigen_exponent == 2.0
        and args.domain_length == 1.0
        and args.train_cutoff == 8
        and args.max_mode == 64
    )
    if not canonical and args.output is None:
        raise SystemExit("noncanonical runs require --output so the canonical SVG is not overwritten")
    geometry = geometry_track(
        args.sphere_radius,
        args.objective_y,
        args.objective_z,
        args.rotation_angle,
    )
    functional = functional_track(
        args.spectral_size,
        args.coefficient_exponent,
        args.eigen_exponent,
    )
    pde = pde_track(args.domain_length, args.train_cutoff, args.max_mode)

    if abs(geometry["constraint_slope"] - 2.0) > 1e-12:
        raise AssertionError("ambient sphere residual should be exactly second order")
    if not (2.98 < geometry["retraction_slope"] < 3.01):
        raise AssertionError("normalization retraction should differ from Exp at third order")
    expected_projection_order = 0.5 - args.coefficient_exponent
    if abs(functional["projection_slope"] - expected_projection_order) > 0.08:
        raise AssertionError("Hilbert projection tail left its analytic finite-window order")
    if abs(functional["compact_slope"] + args.eigen_exponent) > 0.10:
        raise AssertionError("compact tail left its analytic finite-window order")
    if abs(pde["l2_slope"] + 2.0) > 1e-12 or abs(pde["energy_slope"] + 1.0) > 1e-12:
        raise AssertionError("Poisson modal norms have incorrect orders")

    svg = build_svg(geometry, functional, pde, args.train_cutoff, args.max_mode)
    output = (args.output or DEFAULT_OUTPUT).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print(
        f"A_CONFIG sphere_radius={args.sphere_radius:g} objective_y={args.objective_y:g} "
        f"objective_z={args.objective_z:g} rotation_angle={args.rotation_angle:g}"
    )
    print(
        "A_GEOMETRY "
        f"constraint_slope={geometry['constraint_slope']:.6f} "
        f"retraction_order={geometry['retraction_slope']:.6f} "
        f"equivariance_error={geometry['equivariance_error']:.3e}"
    )
    print(
        f"B_CONFIG spectral_size={args.spectral_size} "
        f"coefficient_exponent={args.coefficient_exponent:g} eigen_exponent={args.eigen_exponent:g}"
    )
    print(
        "B_SPECTRAL "
        f"projection_slope={functional['projection_slope']:.6f} "
        f"compact_tail_slope={functional['compact_slope']:.6f} "
        f"effective_dimension_slope={functional['effective_slope']:.6f} "
        f"neff_at_1e-6={functional['effective_last']:.6f}"
    )
    print(
        f"C_CONFIG domain_length={args.domain_length:g} train_cutoff={args.train_cutoff} "
        f"max_mode={args.max_mode}"
    )
    print(
        "C_OPERATOR "
        f"l2_slope={pde['l2_slope']:.6f} energy_slope={pde['energy_slope']:.6f} "
        f"strong_slope={pde['strong_slope']:.6f} "
        f"last_l2={pde['last_l2']:.8e} last_energy={pde['last_energy']:.8e}"
    )
    print(f"OUTPUT {output}")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()
