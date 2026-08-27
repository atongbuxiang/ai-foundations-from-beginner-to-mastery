#!/usr/bin/env python3
"""Deterministic three-track computation gate for MATH-FND-CAP-01.

Only the Python standard library is used.  The script intentionally keeps the
three evidence layers separate: an analytic Gaussian ledger, exact quadratic
dynamics, and a finite circle-kernel discretization.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "00-知识库管理" / "_assets" / "plots" / "math-foundations" / "plot-math-foundations-capstone-gate-v2.svg"
DEFAULT_SEED = 20260820


def gaussian_track() -> list[dict[str, float]]:
    """Analytic linear-Gaussian information and posterior ledger."""
    rows = []
    signal_variance = 5.0
    sigma_c_norm_sq = 17.0
    for noise_variance in (0.1, 0.3, 1.0, 3.0, 10.0):
        total_variance = signal_variance + noise_variance
        rows.append(
            {
                "noise": noise_variance,
                "mi": 0.5 * math.log(total_variance / noise_variance),
                "posterior_trace": 5.0 - sigma_c_norm_sq / total_variance,
                "posterior_det": 4.0 * noise_variance / total_variance,
            }
        )
    return rows


def quadratic_track() -> tuple[dict[float, list[float]], list[float]]:
    """Gradient-descent error and matched gradient-flow error."""
    discrete: dict[float, list[float]] = {}
    for eta in (0.10, 0.20, 0.24):
        e1 = e2 = 1.0
        norms = []
        for _ in range(26):
            norms.append(math.hypot(e1, e2))
            e1 *= 1.0 - eta
            e2 *= 1.0 - 9.0 * eta
        discrete[eta] = norms
    flow = [math.hypot(math.exp(-0.2 * k), math.exp(-1.8 * k)) for k in range(26)]
    return discrete, flow


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Small dense solve by partial-pivoted Gaussian elimination."""
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(aug[i][k]))
        if abs(aug[pivot][k]) < 1e-14:
            raise ArithmeticError("singular kernel system")
        aug[k], aug[pivot] = aug[pivot], aug[k]
        for i in range(k + 1, n):
            factor = aug[i][k] / aug[k][k]
            aug[i][k] = 0.0
            for j in range(k + 1, n + 1):
                aug[i][j] -= factor * aug[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))) / aug[i][i]
    return x


def target(theta: float) -> float:
    return math.cos(2.0 * theta) + 0.3 * math.sin(3.0 * theta)


def circle_kernel(theta: float, phi: float, lengthscale: float) -> float:
    chord_sq = 2.0 - 2.0 * math.cos(theta - phi)
    return math.exp(-chord_sq / (2.0 * lengthscale * lengthscale))


def circle_kernel_track() -> tuple[list[dict[str, float]], float, list[dict[str, float]]]:
    """Finite KRR on S1 plus rotation and retraction audits."""
    lengthscale, ridge = 0.65, 1e-3
    rows = []
    for n in (8, 12, 24, 48):
        theta = [2.0 * math.pi * i / n for i in range(n)]
        gram = [[circle_kernel(ti, tj, lengthscale) for tj in theta] for ti in theta]
        system = [[gram[i][j] + (ridge if i == j else 0.0) for j in range(n)] for i in range(n)]
        alpha = solve_linear(system, [target(ti) for ti in theta])
        squared = 0.0
        for j in range(360):
            t = 2.0 * math.pi * (j + 0.5) / 360.0
            pred = sum(alpha[i] * circle_kernel(t, theta[i], lengthscale) for i in range(n))
            squared += (pred - target(t)) ** 2
        # The Gram matrix is circulant on an equispaced circle, so its
        # eigenvalues are the real DFT of the first row.
        first = gram[0]
        eig = [
            sum(first[j] * math.cos(2.0 * math.pi * ell * j / n) for j in range(n))
            for ell in range(n)
        ]
        shifted = [max(value + ridge, ridge) for value in eig]
        rows.append(
            {
                "n": float(n),
                "rmse": math.sqrt(squared / 360.0),
                "min_gram_eigenvalue": min(eig),
                "condition": max(shifted) / min(shifted),
            }
        )

    rotation = 0.37
    theta = [2.0 * math.pi * i / 24 for i in range(24)]
    rotation_defect = max(
        abs(circle_kernel(a, b, lengthscale) - circle_kernel(a + rotation, b + rotation, lengthscale))
        for a in theta
        for b in theta
    )

    retraction_rows = []
    for h in (0.3, 0.1, 0.03, 0.01):
        norm = math.sqrt(1.0 + h * h)
        retract = (1.0 / norm, h / norm)
        exact_exp = (math.cos(h), math.sin(h))
        error = math.hypot(retract[0] - exact_exp[0], retract[1] - exact_exp[1])
        retraction_rows.append({"h": h, "error": error})
    return rows, rotation_defect, retraction_rows


def svg_text(x: float, y: float, value: str, cls: str = "small", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def polyline(values: list[float], x0: float, y0: float, width: float, height: float,
             color: str, ymin: float | None = None, ymax: float | None = None) -> list[str]:
    lo = min(values) if ymin is None else ymin
    hi = max(values) if ymax is None else ymax
    span = max(hi - lo, 1e-15)
    points = []
    circles = []
    for i, value in enumerate(values):
        x = x0 + width * i / max(len(values) - 1, 1)
        y = y0 + height - height * (value - lo) / span
        points.append(f"{x:.1f},{y:.1f}")
        circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{color}"/>')
    return [f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.5"/>', *circles]


def make_svg(gaussian, discrete, flow, kernel_rows, rotation_defect, retraction_rows) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480" role="img" aria-labelledby="title desc">',
        '<title id="title">数学基础十卷跨章累计复现门</title>',
        '<desc id="desc">三面板分别展示线性高斯信息账本、二次优化的连续与离散稳定，以及圆周上的核回归、旋转不变性和retraction误差。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.title{font-size:24px;font-weight:700;fill:#1F2937}.head{font-size:22px;font-weight:700;fill:#334155}.small{font-size:15px;fill:#64748B}.label{font-size:17px;fill:#334155}.card{fill:#FFFEFB;stroke:#D7DEE8;stroke-width:1.3}.axis{stroke:#64748B;stroke-width:1.1}.dash{stroke-dasharray:5 5}</style></defs>',
        '<rect width="1200" height="480" fill="#FFFFFF"/>',
        '<text x="40" y="39" class="title">MATH-FND-CAP-01：信息、优化动力与几何核方法的跨卷证据账</text>',
        '<rect x="28" y="59" width="368" height="390" class="card"/><rect x="416" y="59" width="368" height="390" class="card"/><rect x="804" y="59" width="368" height="390" class="card"/>',
        '<text x="50" y="89" class="head">A　Gaussian information</text>',
        '<text x="438" y="89" class="head">B　Discrete stability</text>',
        '<text x="826" y="89" class="head">C　Circle-kernel geometry</text>',
    ]

    # Track A: use separate fixed scales and label the two analytic quantities.
    x0, y0, width, height = 72.0, 124.0, 280.0, 145.0
    parts += [f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" class="axis"/>']
    parts += polyline([row["mi"] for row in gaussian], x0, y0, width, height, "#7C3AED", 0.0, 2.0)
    parts += polyline([row["posterior_trace"] for row in gaussian], x0, y0, width, height, "#16A34A", 0.0, 5.0)
    parts += [svg_text(72, 294, "purple: I(X;Z) [0,2] nats", "label"), svg_text(72, 316, "green: tr Cov(X|Z) [0,5]", "label")]
    one = next(row for row in gaussian if row["noise"] == 1.0)
    parts += [svg_text(50, 350, f'R=1: I={one["mi"]:.4f}, posterior trace={one["posterior_trace"]:.4f}', "small"), svg_text(50, 375, f'posterior det={one["posterior_det"]:.4f}; noise ↑ ⇒ information ↓', "small"), svg_text(50, 402, "定理值 ≠ estimator；先验/噪声/方向必须分账", "small"), svg_text(50, 428, "x-axis noise variance: 0.1, 0.3, 1, 3, 10", "small")]

    # Track B: log error curves, with the Euler stability boundary made explicit.
    x0, y0, width, height = 458.0, 124.0, 280.0, 170.0
    all_logs = [math.log10(max(v, 1e-12)) for values in discrete.values() for v in values]
    all_logs += [math.log10(max(v, 1e-12)) for v in flow]
    ymin, ymax = min(all_logs), max(all_logs)
    colors = {0.10: "#2563EB", 0.20: "#16A34A", 0.24: "#DC2626"}
    for eta, values in discrete.items():
        parts += polyline([math.log10(max(v, 1e-12)) for v in values], x0, y0, width, height, colors[eta], ymin, ymax)
    parts += polyline([math.log10(max(v, 1e-12)) for v in flow], x0, y0, width, height, "#7C3AED", ymin, ymax)
    parts += [f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" class="axis"/>']
    parts += [svg_text(458, 319, "blue η=.10　green η=.20　red η=.24", "label"), svg_text(458, 342, "purple: exact flow sampled at t=0.2k", "small"), svg_text(438, 372, "stability: 0 &lt; η &lt; 2/9 ≈ .2222", "small"), svg_text(438, 398, f'k=25: η=.20 error={discrete[0.20][-1]:.3g}', "small"), svg_text(438, 421, f'k=25: η=.24 error={discrete[0.24][-1]:.3g} (diverges)', "small")]

    # Track C: KRR refinement plus invariant/geometric checks.
    x0, y0, width, height = 846.0, 124.0, 270.0, 145.0
    rmse_logs = [math.log10(max(row["rmse"], 1e-14)) for row in kernel_rows]
    parts += [f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" class="axis"/>']
    parts += polyline(rmse_logs, x0, y0, width, height, "#DB2777")
    parts += [svg_text(846, 294, "log10 test RMSE; n = 8, 12, 24, 48", "label")]
    last = kernel_rows[-1]
    h0, h1 = retraction_rows[0], retraction_rows[-1]
    parts += [svg_text(826, 328, f'n=48: RMSE={last["rmse"]:.3g}, cond(K+λI)≈{last["condition"]:.3g}', "small"), svg_text(826, 352, f'finite Gram min eigenvalue={last["min_gram_eigenvalue"]:.2g}', "small"), svg_text(826, 376, f'rotation-kernel defect={rotation_defect:.1e}', "small"), svg_text(826, 400, f'retraction−Exp: h={h0["h"]:.1f} → {h0["error"]:.2g}', "small"), svg_text(826, 422, f'h={h1["h"]:.2f} → {h1["error"]:.2g}; finite mesh ≠ operator theorem', "small"), '</svg>']
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Reserved in the artifact contract; tracks are analytic/deterministic.")
    args = parser.parse_args()

    gaussian = gaussian_track()
    discrete, flow = quadratic_track()
    kernel_rows, rotation_defect, retraction_rows = circle_kernel_track()
    if not all(gaussian[i]["mi"] > gaussian[i + 1]["mi"] for i in range(len(gaussian) - 1)):
        raise AssertionError("Gaussian mutual information should decrease with noise")
    if not discrete[0.24][-1] > discrete[0.20][-1]:
        raise AssertionError("the step beyond the Euler stability threshold should diverge")
    if rotation_defect > 1e-12:
        raise AssertionError("the circle kernel must be rotation invariant")
    if not all(retraction_rows[i]["error"] > retraction_rows[i + 1]["error"] for i in range(len(retraction_rows) - 1)):
        raise AssertionError("retraction error should shrink with the tangent step")
    svg = make_svg(gaussian, discrete, flow, kernel_rows, rotation_defect, retraction_rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print("MATH-FND-CAP-01 deterministic computation gate")
    print(f"seed={args.seed} (reserved; no stochastic estimates in v2)")
    for row in gaussian:
        print(f"A noise={row['noise']:.3g} mi={row['mi']:.10g} posterior_trace={row['posterior_trace']:.10g} posterior_det={row['posterior_det']:.10g}")
    print("A handcheck noise=1 mean_coefficient=(2/3,1/6) posterior_cov=((4/3,-2/3),(-2/3,5/6))")
    for eta, values in discrete.items():
        print(f"B eta={eta:.2f} multiplier=({1-eta:.6g},{1-9*eta:.6g}) error_k25={values[-1]:.10g}")
    print(f"B Euler_stability_threshold={2/9:.10g} optimal_eta={2/10:.10g} optimal_rho={8/10:.10g} flow_error_k25={flow[-1]:.10g}")
    for row in kernel_rows:
        print(f"C n={int(row['n'])} rmse={row['rmse']:.10g} min_gram_eigenvalue={row['min_gram_eigenvalue']:.10g} condition={row['condition']:.10g}")
    print(f"C rotation_defect={rotation_defect:.10g}")
    for row in retraction_rows:
        print(f"C h={row['h']:.3g} retraction_exp_error={row['error']:.10g}")
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(0)
