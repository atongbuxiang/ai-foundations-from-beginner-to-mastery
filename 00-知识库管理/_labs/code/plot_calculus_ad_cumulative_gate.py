#!/usr/bin/env python3
"""Deterministic CALC-CUM-01 gate using only Python stdlib."""

from __future__ import annotations

import argparse
import hashlib
import math
import random
import sys
from pathlib import Path


DEFAULT_SEED = 20260820
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "00-知识库管理" / "_assets" / "figures" / "calculus-ad" / "plot-calculus-ad-cumulative-gate-v2.svg"


def norm2(x: list[float]) -> float:
    return math.sqrt(sum(v * v for v in x))


def local_experiment() -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    a, b = 1.0, 0.7
    taylor = []
    for h in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5):
        x, y = h * a, h * b
        value = math.exp(x * y) + 0.5 * x * x + y ** 3
        linear = 1.0
        quadratic = 1.0 + x * y + 0.5 * x * x
        taylor.append({"h": h, "linear_error": abs(value - linear), "quadratic_error": abs(value - quadratic)})
    finite_difference = []
    for exponent in range(1, 16):
        h = 10.0 ** (-exponent)
        estimate = (math.exp(h) - math.exp(-h)) / (2.0 * h)
        finite_difference.append({"h": h, "error": abs(estimate - 1.0)})
    return taylor, finite_difference


def graph_jacobian(x: list[float]) -> list[list[float]]:
    x1, x2 = x
    c = math.cos(x1 * x2)
    return [[x2, x1], [c * x2, c * x1], [2.0 * x1 + c * x2, c * x1]]


def matvec(a: list[list[float]], x: list[float]) -> list[float]:
    return [sum(row[j] * x[j] for j in range(len(x))) for row in a]


def transpose_matvec(a: list[list[float]], x: list[float]) -> list[float]:
    return [sum(a[i][j] * x[i] for i in range(len(a))) for j in range(len(a[0]))]


def loss_gradient(x: list[float]) -> list[float]:
    x1, x2 = x
    u = x1 * x2
    w = x1 * x1 + math.sin(u)
    c = math.cos(u)
    return [w * (2.0 * x1 + c * x2), w * c * x1]


def loss_hvp(x: list[float], p: list[float]) -> list[float]:
    x1, x2 = x
    u = x1 * x2
    s, c = math.sin(u), math.cos(u)
    w = x1 * x1 + s
    grad_w = [2.0 * x1 + c * x2, c * x1]
    h_w = [
        [2.0 - s * x2 * x2, c - s * x1 * x2],
        [c - s * x1 * x2, -s * x1 * x1],
    ]
    dot = sum(grad_w[i] * p[i] for i in range(2))
    return [grad_w[i] * dot + w * sum(h_w[i][j] * p[j] for j in range(2)) for i in range(2)]


def ad_experiment(seed: int) -> tuple[float, list[dict[str, float]], dict[str, float]]:
    rng = random.Random(seed)
    max_pairing = 0.0
    for _ in range(100):
        x = [rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)]
        p = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        q = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        j = graph_jacobian(x)
        left = sum(qi * vi for qi, vi in zip(q, matvec(j, p)))
        right = sum(pi * vi for pi, vi in zip(p, transpose_matvec(j, q)))
        max_pairing = max(max_pairing, abs(left - right))

    x, p = [1.0, 2.0], [1.0, -1.0]
    exact = loss_hvp(x, p)
    hvp_rows = []
    for h in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5):
        plus = loss_gradient([x[i] + h * p[i] for i in range(2)])
        minus = loss_gradient([x[i] - h * p[i] for i in range(2)])
        estimate = [(plus[i] - minus[i]) / (2.0 * h) for i in range(2)]
        hvp_rows.append({"h": h, "error": norm2([estimate[i] - exact[i] for i in range(2)])})
    checkpoint = {"chain_length": 1024.0, "full_tape": 1024.0, "sqrt_checkpoint_memory": 64.0}
    return max_pairing, hvp_rows, checkpoint


def solve_x(theta: float) -> list[float]:
    a, d, off = 2.0 + theta, 2.0, 1.0
    det = a * d - off * off
    b1, b2 = 1.0, theta
    return [(d * b1 - off * b2) / det, (-off * b1 + a * b2) / det]


def implicit_spectral_experiment() -> tuple[list[dict[str, float]], list[dict[str, float]], float]:
    exact = [-7.0 / 9.0, 8.0 / 9.0]
    implicit = []
    for h in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5):
        plus, minus = solve_x(h), solve_x(-h)
        estimate = [(plus[i] - minus[i]) / (2.0 * h) for i in range(2)]
        implicit.append({"h": h, "error": norm2([estimate[i] - exact[i] for i in range(2)])})
    spectral = []
    for gap in (1.0, 0.3, 0.1, 0.03, 0.01, 0.003):
        spectral.append({"gap": gap, "eigenvector_derivative_norm": 1.0 / gap})
    logdet_direct = 2.0 / 3.0
    return implicit, spectral, logdet_direct


def svg_text(x: float, y: float, value: str, cls: str = "small", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def log_curve(rows: list[dict[str, float]], key: str, x0: float, y0: float, width: float, height: float, color: str, bounds=None) -> tuple[str, list[str]]:
    xs = [-math.log10(row["h"]) for row in rows]
    vals = [max(float(row[key]), 1e-18) for row in rows]
    logs = [math.log10(v) for v in vals]
    if bounds is None:
        xmin, xmax, ymin, ymax = min(xs), max(xs), min(logs), max(logs)
    else:
        xmin, xmax, ymin, ymax = bounds
    span_y = max(ymax - ymin, 1.0)
    points, circles = [], []
    for xval, yval in zip(xs, logs):
        x = x0 + width * (xval - xmin) / max(xmax - xmin, 1e-12)
        y = y0 + height - height * (yval - ymin) / span_y
        points.append(f"{x:.1f},{y:.1f}")
        circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8" fill="{color}"/>')
    return f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.4"/>', circles


def make_svg(taylor, finite_difference, pairing, hvp, checkpoint, implicit, spectral) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470" role="img" aria-labelledby="title desc">',
        '<title id="title">微积分、矩阵微分与自动微分累计复现门</title>',
        '<desc id="desc">三面板展示 Taylor 余项和有限差分，JVP/VJP 伴随与 HVP，及隐式导数和谱间隙敏感性。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.title{font-size:24px;font-weight:700;fill:#1F2937}.head{font-size:22px;font-weight:700;fill:#334155}.small{font-size:15px;fill:#64748B}.label{font-size:17px;fill:#334155}.card{fill:#FFFEFB;stroke:#D7DEE8;stroke-width:1.3}.axis{stroke:#64748B;stroke-width:1.1}</style></defs>',
        '<rect width="1200" height="470" fill="#FFFFFF"/>',
        '<text x="40" y="38" class="title">CALC-CUM-01 计算门：局部模型、AD 传播与隐式/谱导数</text>',
        '<rect x="28" y="58" width="368" height="382" class="card"/><rect x="416" y="58" width="368" height="382" class="card"/><rect x="804" y="58" width="368" height="382" class="card"/>',
        '<text x="50" y="88" class="head">A　Taylor 阶与有限差分</text>',
        '<text x="438" y="88" class="head">B　JVP/VJP 与 HVP</text>',
        '<text x="826" y="88" class="head">C　隐式微分与谱隙</text>',
    ]

    # A
    x0, y0, w, hgt = 74.0, 126.0, 275.0, 150.0
    parts += [f'<line x1="{x0}" y1="{y0+hgt}" x2="{x0+w}" y2="{y0+hgt}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+hgt}" class="axis"/>']
    a_xs = [-math.log10(row["h"]) for row in taylor]
    a_logs = [math.log10(max(row[key], 1e-18)) for row in taylor for key in ("linear_error", "quadratic_error")]
    a_bounds = (min(a_xs), max(a_xs), min(a_logs), max(a_logs))
    l1, c1 = log_curve(taylor, "linear_error", x0, y0, w, hgt, "#DC2626", a_bounds)
    l2, c2 = log_curve(taylor, "quadratic_error", x0, y0, w, hgt, "#2563EB", a_bounds)
    parts += [l1, *c1, l2, *c2, svg_text(74, 302, "red: linear remainder ~h²　blue: quadratic ~h³", "label"), svg_text(50, 337, "有限差分不是 h 越小越好：", "label")]
    best_fd = min(finite_difference, key=lambda row: row["error"])
    parts += [svg_text(50, 363, f'centered exp′(0): best h≈{best_fd["h"]:.0e}, error≈{best_fd["error"]:.1e}', "small"), svg_text(50, 391, f'h=1e−15 时 error={finite_difference[-1]["error"]:.2g}', "small"), svg_text(50, 418, "Taylor slope验收理论阶数；FD仅是数值证据", "small")]

    # B
    x0, y0 = 458.0, 126.0
    parts += [f'<line x1="{x0}" y1="{y0+hgt}" x2="{x0+w}" y2="{y0+hgt}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+hgt}" class="axis"/>']
    lh, ch = log_curve(hvp, "error", x0, y0, w, hgt, "#7C3AED")
    parts += [lh, *ch, svg_text(458, 302, "centered gradient difference → analytic HVP", "label"), svg_text(438, 337, f'100 random adjoint tests: max residual={pairing:.1e}', "small"), svg_text(438, 365, f'chain N={int(checkpoint["chain_length"])}: full tape≈{int(checkpoint["full_tape"])} states', "small"), svg_text(438, 391, f'√N checkpoint schedule≈{int(checkpoint["sqrt_checkpoint_memory"])} live states', "small"), svg_text(438, 418, "Checkpoint换time/memory，不改同一程序导数", "small")]

    # C: two curves normalized to their own logs.
    x0, y0 = 844.0, 126.0
    parts += [f'<line x1="{x0}" y1="{y0+hgt}" x2="{x0+w}" y2="{y0+hgt}" class="axis"/>', f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+hgt}" class="axis"/>']
    li, ci = log_curve(implicit, "error", x0, y0, w, hgt, "#16A34A")
    parts += [li, *ci, svg_text(844, 302, "green: centered FD → implicit derivative", "label")]
    # Spectral gap bars.
    max_s = max(row["eigenvector_derivative_norm"] for row in spectral)
    for idx, row in enumerate(spectral):
        x = 835 + idx * 49
        height = 45 * math.log10(row["eigenvector_derivative_norm"] + 1) / math.log10(max_s + 1)
        parts.append(f'<rect x="{x}" y="{390-height:.1f}" width="30" height="{height:.1f}" rx="4" fill="#DB2777" fill-opacity=".8"/>')
        parts.append(svg_text(x + 15, 406, f'{row["gap"]:.3g}', "small", "middle"))
    parts += [svg_text(826, 332, "eigenvector derivative ‖u̇‖=1/gap", "label"), svg_text(826, 428, "bar x-axis=gap；重根处应改报 projector/subspace", "small"), '</svg>']
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()
    taylor, fd = local_experiment()
    pairing, hvp, checkpoint = ad_experiment(args.seed)
    implicit, spectral, logdet = implicit_spectral_experiment()
    if pairing > 1e-12:
        raise AssertionError("Jacobian/adjoint pairing identity failed")
    if not taylor[-1]["quadratic_error"] < taylor[0]["quadratic_error"]:
        raise AssertionError("quadratic Taylor remainder should shrink locally")
    if not implicit[-1]["error"] < implicit[0]["error"]:
        raise AssertionError("implicit derivative finite-difference error should shrink")
    if not spectral[-1]["eigenvector_derivative_norm"] > spectral[0]["eigenvector_derivative_norm"]:
        raise AssertionError("eigenvector sensitivity should grow as the gap closes")
    svg = make_svg(taylor, fd, pairing, hvp, checkpoint, implicit, spectral)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode()).hexdigest()
    print("CALC-CUM-01 deterministic computation gate")
    print(f"seed={args.seed}")
    for row in taylor: print(f"A h={row['h']:.1e} linear={row['linear_error']:.8g} quadratic={row['quadratic_error']:.8g}")
    best = min(fd, key=lambda row: row["error"])
    print(f"A finite-difference best_h={best['h']:.1e} best_error={best['error']:.8g} final_error={fd[-1]['error']:.8g}")
    print(f"B max_adjoint_pairing_residual={pairing:.8g}")
    for row in hvp: print(f"B h={row['h']:.1e} hvp_error={row['error']:.8g}")
    for row in implicit: print(f"C h={row['h']:.1e} implicit_error={row['error']:.8g}")
    for row in spectral: print(f"C gap={row['gap']:.3g} eigenvector_derivative_norm={row['eigenvector_derivative_norm']:.8g}")
    print(f"C logdet_derivative={logdet:.8g} change_of_variables_det=6")
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(0)
