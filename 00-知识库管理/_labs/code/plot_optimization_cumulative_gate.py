#!/usr/bin/env python3
"""Generate the deterministic optimization cumulative-gate SVG.

The three panels deliberately separate three claims:
1. exact gradient descent can remain on a strict saddle's stable manifold,
   while a small perturbation excites the unstable direction;
2. a differentiable objective can be nonconvex and still satisfy a global
   Polyak-Lojasiewicz inequality;
3. scale-equivalent factorizations can have identical predictions and loss
   but arbitrarily different raw Hessian sharpness.

Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "optimization"
    / "plot-optimization-cumulative-gate-v2.svg"
)


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def text(x: float, y: float, value: object, cls: str = "small", anchor: str = "start") -> str:
    return f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}">{esc(value)}</text>'


def line(x1: float, y1: float, x2: float, y2: float, **attrs: object) -> str:
    extra = " ".join(
        f'{key.replace("_", "-")}="{esc(value)}"' for key, value in attrs.items()
    )
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {extra}/>'


def path(
    points: list[tuple[float, float]],
    color: str,
    width: float = 3.0,
    dash: str | None = None,
) -> str:
    commands = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="{commands}" fill="none" stroke="{color}" '
        f'stroke-width="{width}"{dash_attr}/>'
    )


def circle(x: float, y: float, radius: float, color: str) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}"/>'


def saddle_objective(x: float, y: float) -> float:
    return 0.25 * (x * x - 1.0) ** 2 + 0.5 * y * y


def saddle_gradient(x: float, y: float) -> tuple[float, float]:
    return x * (x * x - 1.0), y


def saddle_run(x0: float, y0: float, eta: float, steps: int) -> tuple[list[float], float, float]:
    x, y = x0, y0
    values = [saddle_objective(x, y)]
    for _ in range(steps):
        gx, gy = saddle_gradient(x, y)
        x -= eta * gx
        y -= eta * gy
        values.append(saddle_objective(x, y))
    return values, x, y


def pl_values(x: float, a: float) -> tuple[float, float, float]:
    h = x + a * math.sin(x)
    hp = 1.0 + a * math.cos(x)
    hpp = -a * math.sin(x)
    f = 0.5 * h * h
    gradient = h * hp
    ratio = hp * hp if f > 1e-24 else hp * hp
    hessian = hp * hp + h * hpp
    return ratio, hessian, gradient


def build_svg(
    perturbation: float,
    stable_y0: float,
    pl_a: float,
    pl_x_max: float,
    scale_span: float,
    eta: float,
    steps: int,
) -> tuple[str, dict[str, float]]:
    exact, exact_x, exact_y = saddle_run(0.0, stable_y0, eta, steps)
    perturbed, final_x, final_y = saddle_run(perturbation, stable_y0, eta, steps)

    width, height = 1200, 430
    panel_x = [20, 415, 810]
    panel_w = 370
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">优化与凸分析累计复现门</title>',
        '<desc id="desc">三面板展示鞍点稳定流形、PL 条件与非凸性分离，以及参数化缩放导致的 sharpness 变化。</desc>',
        '<rect width="1200" height="430" fill="#ffffff"/>',
        """<style>
        text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.panel{fill:#fffefb;stroke:#d7dee8;stroke-width:1.5}.title{font-size:19px;font-weight:700;fill:#1f2937}.sub,.body,.small,.tiny{font-size:15px}.sub{fill:#475569}.body{fill:#334155}.small,.tiny{fill:#64748b}
        </style>""",
    ]
    for x in panel_x:
        parts.append(f'<rect class="panel" x="{x}" y="20" width="{panel_w}" height="390"/>')

    # Panel A: exact stable manifold versus perturbed escape.
    parts += [
        text(40, 53, "A · 严格鞍点：精确卡住 vs 扰动逃逸", "title"),
        text(40, 78, "f=¼(x²−1)²+½y²；原点 Hessian=diag(−1,1)", "sub"),
    ]
    ax_l, ax_r, ax_t, ax_b = 72.0, 360.0, 112.0, 330.0
    parts += [
        line(ax_l, ax_b, ax_r, ax_b, stroke="#64748b", stroke_width="1.5"),
        line(ax_l, ax_t, ax_l, ax_b, stroke="#64748b", stroke_width="1.5"),
    ]
    max_f = max(max(exact), max(perturbed), 0.26)

    def trajectory_points(values: list[float]) -> list[tuple[float, float]]:
        return [
            (
                ax_l + i / steps * (ax_r - ax_l),
                ax_b - value / max_f * (ax_b - ax_t),
            )
            for i, value in enumerate(values)
        ]

    parts.append(path(trajectory_points(exact), "#dc2626", 3.0, "6 4"))
    parts.append(path(trajectory_points(perturbed), "#2563eb", 3.5))
    parts += [
        text(240, 128, "exact x₀=0", "tiny"),
        text(240, 293, f"perturbed x₀={perturbation:g}", "tiny"),
        text(216, 354, "GD iterations", "small", "middle"),
        text(46, 220, "objective", "small", "middle"),
        text(40, 385, f"final x={final_x:.6f}；f={perturbed[-1]:.3e}", "small"),
    ]

    # Panel B: nonconvex PL objective.
    parts += [
        text(435, 53, "B · 非凸不妨碍 PL 全局梯度支配", "title"),
        text(435, 78, f"h=x+{pl_a:g}sin x；f=½h²；PL 下界 μ=(1−a)²", "sub"),
    ]
    bx_l, bx_r, bx_t, bx_b = 468.0, 755.0, 112.0, 330.0
    parts += [
        line(bx_l, bx_b, bx_r, bx_b, stroke="#64748b", stroke_width="1.5"),
        line(bx_l, bx_t, bx_l, bx_b, stroke="#64748b", stroke_width="1.5"),
    ]
    x_min, x_max = -pl_x_max, pl_x_max
    y_min, y_max = -4.0, 3.0

    def bxy(x: float, y: float) -> tuple[float, float]:
        return (
            bx_l + (x - x_min) / (x_max - x_min) * (bx_r - bx_l),
            bx_b - (y - y_min) / (y_max - y_min) * (bx_b - bx_t),
        )

    zero_y = bxy(0.0, 0.0)[1]
    mu = (1.0 - pl_a) ** 2
    mu_y = bxy(0.0, mu)[1]
    parts += [
        line(bx_l, zero_y, bx_r, zero_y, stroke="#94a3b8", stroke_width="1.2"),
        line(bx_l, mu_y, bx_r, mu_y, stroke="#d97706", stroke_width="1.2", stroke_dasharray="5 4"),
    ]
    ratios: list[tuple[float, float]] = []
    hessians: list[tuple[float, float]] = []
    ratio_min = float("inf")
    hessian_min = float("inf")
    hessian_min_x = 0.0
    for i in range(801):
        x = x_min + (x_max - x_min) * i / 800.0
        ratio, hessian, _ = pl_values(x, pl_a)
        ratio_min = min(ratio_min, ratio)
        if hessian < hessian_min:
            hessian_min = hessian
            hessian_min_x = x
        ratios.append(bxy(x, max(y_min, min(y_max, ratio))))
        hessians.append(bxy(x, max(y_min, min(y_max, hessian))))
    parts.append(path(ratios, "#2563eb", 3.0))
    parts.append(path(hessians, "#dc2626", 2.5))
    parts += [
        text(662, 125, "PL ratio = h′²", "tiny"),
        text(662, 175, "Hessian f″", "tiny"),
        text(612, 354, f"x ∈ [−{pl_x_max:g},{pl_x_max:g}]", "small", "middle"),
        text(442, zero_y + 4, "0", "tiny", "middle"),
        text(435, 385, f"min f″={hessian_min:.3f} < 0；min ratio≈{ratio_min:.3f}", "small"),
    ]

    # Panel C: scale symmetry and raw sharpness.
    parts += [
        text(830, 53, "C · 相同 predictor，不同 raw sharpness", "title"),
        text(830, 78, "f(a,b)=½(ab−1)²；(a,b)=(s,1/s) 始终有 ab=1", "sub"),
    ]
    cx_l, cx_r, cx_t, cx_b = 850.0, 1145.0, 112.0, 315.0
    parts += [
        line(cx_l, cx_b, cx_r, cx_b, stroke="#64748b", stroke_width="1.5"),
        line(cx_l, cx_t, cx_l, cx_b, stroke="#64748b", stroke_width="1.5"),
    ]

    sharpness_extreme = 10.0 ** (2.0 * scale_span) + 10.0 ** (-2.0 * scale_span)

    def cxy(s: float, sharpness: float) -> tuple[float, float]:
        log_s = math.log10(s)
        return (
            cx_l + (log_s + scale_span) / (2.0 * scale_span) * (cx_r - cx_l),
            cx_b - (sharpness - 2.0) / (sharpness_extreme - 2.0) * (cx_b - cx_t),
        )

    curve: list[tuple[float, float]] = []
    for i in range(401):
        log_s = -scale_span + 2.0 * scale_span * i / 400.0
        s = 10.0**log_s
        sharpness = s * s + 1.0 / (s * s)
        curve.append(cxy(s, sharpness))
    parts.append(path(curve, "#2563eb", 3.5))
    scale_low = 10.0 ** (-scale_span)
    scale_high = 10.0**scale_span
    for s, color in [(scale_low, "#dc2626"), (1.0, "#059669"), (scale_high, "#dc2626")]:
        sharpness = s * s + 1.0 / (s * s)
        x, y = cxy(s, sharpness)
        parts.append(circle(x, y, 5.5, color))
        parts.append(text(x, y - 11 if s != 1.0 else y - 12, f"s={s:g}", "tiny", "middle"))
    parts += [
        text(997, 342, "log scale s", "small", "middle"),
        text(825, 210, "λmax(H)", "small", "middle"),
        text(
            830,
            372,
            f"s=1: λmax=2；s={scale_low:g} 或 {scale_high:g}: λmax={sharpness_extreme:g}",
            "small",
        ),
        text(830, 391, "训练函数与 loss 恒定；坐标曲率不是泛化不变量", "small"),
    ]

    parts.append("</svg>")
    metrics = {
        "exact_final_f": exact[-1],
        "perturbed_final_f": perturbed[-1],
        "perturbed_final_x": final_x,
        "perturbed_final_y": final_y,
        "pl_mu": mu,
        "pl_ratio_min": ratio_min,
        "pl_hessian_min": hessian_min,
        "pl_hessian_min_x": hessian_min_x,
        "sharpness_balanced": 2.0,
        "sharpness_extreme": sharpness_extreme,
    }
    return "\n".join(parts) + "\n", metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--perturbation", type=float, default=1e-3)
    parser.add_argument("--stable-y0", type=float, default=0.0)
    parser.add_argument("--pl-a", type=float, default=0.5)
    parser.add_argument("--pl-x-max", type=float, default=8.0)
    parser.add_argument("--scale-span", type=float, default=1.0)
    parser.add_argument("--eta", type=float, default=0.1)
    parser.add_argument("--steps", type=int, default=160)
    args = parser.parse_args()
    if not 0.0 < args.pl_a < 1.0:
        parser.error("--pl-a must lie in (0, 1)")
    if not 0.0 < abs(args.perturbation) <= 0.1:
        parser.error("--perturbation must be nonzero with absolute value at most 0.1")
    if not abs(args.stable_y0) <= 2.0:
        parser.error("--stable-y0 must have absolute value at most 2")
    if not 4.0 <= args.pl_x_max <= 20.0:
        parser.error("--pl-x-max must lie in [4, 20]")
    if not 0.25 <= args.scale_span <= 2.0:
        parser.error("--scale-span must lie in [0.25, 2]")
    if not 0.0 < args.eta < 1.0:
        parser.error("--eta must lie in (0, 1) for this demonstration")
    if args.steps < 2:
        parser.error("--steps must be at least 2")
    return args


def main() -> None:
    args = parse_args()
    output = args.output.expanduser().resolve()
    svg, metrics = build_svg(
        args.perturbation,
        args.stable_y0,
        args.pl_a,
        args.pl_x_max,
        args.scale_span,
        args.eta,
        args.steps,
    )
    if not all(math.isfinite(value) for value in metrics.values()):
        raise AssertionError("trajectory or calibration produced a non-finite value")
    if not metrics["perturbed_final_f"] < metrics["exact_final_f"]:
        raise AssertionError("the perturbed trajectory should escape toward a lower objective")
    if metrics["pl_ratio_min"] + 1e-10 < metrics["pl_mu"]:
        raise AssertionError("sampled PL ratios must respect the analytic constant")
    if not metrics["sharpness_extreme"] > metrics["sharpness_balanced"]:
        raise AssertionError("the rescaled coordinates should have larger coordinate sharpness")
    canonical = (
        args.perturbation == 1e-3
        and args.stable_y0 == 0.0
        and args.pl_a == 0.5
        and args.pl_x_max == 8.0
        and args.scale_span == 1.0
        and args.eta == 0.1
        and args.steps == 160
    )
    if canonical and abs(metrics["exact_final_f"] - 0.25) > 1e-12:
        raise AssertionError("the canonical saddle trajectory should stay at f=1/4")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(
        f"A_CONFIG perturbation={args.perturbation:g} stable_y0={args.stable_y0:g} "
        f"eta={args.eta:g} steps={args.steps}"
    )
    print(
        "A_SADDLE exact_f={exact_final_f:.8f} perturbed_f={perturbed_final_f:.8e} "
        "final_x={perturbed_final_x:.8f}".format(**metrics)
    )
    print(
        f"B_CONFIG a={args.pl_a:g} x_max={args.pl_x_max:g}"
    )
    print(
        "B_PL mu={pl_mu:.8f} sampled_min_ratio={pl_ratio_min:.8f} "
        "sampled_min_hessian={pl_hessian_min:.8f} at_x={pl_hessian_min_x:.5f}".format(**metrics)
    )
    print(f"C_CONFIG scale_span={args.scale_span:g}")
    print(
        "C_SHARPNESS balanced={sharpness_balanced:.5f} extreme={sharpness_extreme:.5f}".format(
            **metrics
        )
    )
    print(f"OUTPUT {output}")
    print(f"SHA256 {digest}")
    print(f"PYTHON {sys.version.split()[0]}")


if __name__ == "__main__":
    main()
