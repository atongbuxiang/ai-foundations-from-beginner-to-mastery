#!/usr/bin/env python3
"""Deterministic audit for flow maps, Liouville, CNF integration and Hutchinson trace.

Only Python's standard library is required.  The script writes an SVG with three
tracks and exits non-zero if any analytic/numerical contract fails.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import random
from pathlib import Path


def matmul2(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def det2(a: list[list[float]]) -> float:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def nonnormal_exp(t: float) -> list[list[float]]:
    e1 = math.exp(-t)
    e2 = math.exp(-2.0 * t)
    return [[e1, 8.0 * (e1 - e2)], [0.0, e2]]


def singular_values_2x2(a: list[list[float]]) -> tuple[float, float]:
    ata = matmul2(
        [[a[0][0], a[1][0]], [a[0][1], a[1][1]]],
        a,
    )
    tr = ata[0][0] + ata[1][1]
    disc = max(0.0, tr * tr - 4.0 * det2(ata))
    lmax = 0.5 * (tr + math.sqrt(disc))
    lmin = 0.5 * (tr - math.sqrt(disc))
    return math.sqrt(max(lmax, 0.0)), math.sqrt(max(lmin, 0.0))


def polygon_area(points: list[tuple[float, float]]) -> float:
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]):
        acc += x0 * y1 - x1 * y0
    return abs(acc) / 2.0


def rhs_augmented(state: tuple[float, float]) -> tuple[float, float]:
    x, _logp = state
    return -x**3, 3.0 * x * x


def rk4_step(state: tuple[float, float], h: float) -> tuple[float, float]:
    def add(y: tuple[float, float], k: tuple[float, float], scale: float) -> tuple[float, float]:
        return y[0] + scale * k[0], y[1] + scale * k[1]

    k1 = rhs_augmented(state)
    k2 = rhs_augmented(add(state, k1, h / 2.0))
    k3 = rhs_augmented(add(state, k2, h / 2.0))
    k4 = rhs_augmented(add(state, k3, h))
    return (
        state[0] + h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0,
        state[1] + h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0,
    )


def integrate_rk4(x0: float, logp0: float, t1: float, steps: int) -> tuple[float, float]:
    h = t1 / steps
    state = (x0, logp0)
    for _ in range(steps):
        state = rk4_step(state, h)
    return state


def exact_augmented(x0: float, logp0: float, t: float) -> tuple[float, float, float]:
    scale = 1.0 + 2.0 * t * x0 * x0
    x = x0 / math.sqrt(scale)
    jac = scale ** (-1.5)
    logp = logp0 - math.log(jac)
    return x, logp, jac


def observed_orders(errors: list[float]) -> list[float]:
    return [math.log(errors[i] / errors[i + 1], 2.0) for i in range(len(errors) - 1)]


TRACE_MATRIX = [
    [1.0, 2.0, -1.0, 0.5],
    [0.0, -2.0, 3.0, 1.0],
    [4.0, -1.0, 0.5, 2.0],
    [0.0, 2.0, -3.0, 3.0],
]


def quadratic(a: list[list[float]], eps: tuple[int, ...]) -> float:
    return sum(eps[i] * a[i][j] * eps[j] for i in range(len(a)) for j in range(len(a)))


def symmetric_part(a: list[list[float]]) -> list[list[float]]:
    n = len(a)
    return [[0.5 * (a[i][j] + a[j][i]) for j in range(n)] for i in range(n)]


def population_variance(values: list[float]) -> float:
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)


def cumulative_probe_means(a: list[list[float]], counts: list[int], seed: int) -> list[float]:
    rng = random.Random(seed)
    total = 0.0
    result: list[float] = []
    wanted = set(counts)
    for k in range(1, max(counts) + 1):
        eps = tuple(1 if rng.random() < 0.5 else -1 for _ in range(len(a)))
        total += quadratic(a, eps)
        if k in wanted:
            result.append(total / k)
    return result


def svg_polyline(points: list[tuple[float, float]], css_class: str) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline class="{css_class}" points="{coords}"/>'


def build_svg(
    linear: dict[str, float],
    nonlinear: dict[str, object],
    trace: dict[str, object],
) -> str:
    width, height = 1200, 470
    panels = [(20, 55, 370, 385), (415, 55, 370, 385), (810, 55, 370, 385)]
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">流映射、Liouville 与 Hutchinson 三轨审计</title>',
        '<desc id="desc">非正规线性流的剪切与面积收缩、非线性连续正规化流的四阶数值收敛、随机迹估计的精确方差和标准误差。</desc>',
        '<defs><style>',
        'text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.panel{fill:#fffefb;stroke:#d6dee8;stroke-width:1.5}.title{font:700 22px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#0f172a}.label{font:500 17px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#475569}.math{font:600 17px Georgia,"Times New Roman",serif;fill:#1e293b}.axis{stroke:#64748b;stroke-width:1.2}.grid{stroke:#e2e8f0;stroke-width:1}.blue{fill:none;stroke:#2563eb;stroke-width:2.6}.orange{fill:none;stroke:#ea580c;stroke-width:2.6}.green{fill:none;stroke:#059669;stroke-width:2.6}.violet{fill:none;stroke:#7c3aed;stroke-width:2.2;stroke-dasharray:6 4}.dotb{fill:#2563eb}.doto{fill:#ea580c}.dotg{fill:#059669}.square0{fill:#dbeafe;fill-opacity:.55;stroke:#2563eb;stroke-width:2}.square1{fill:#ffedd5;fill-opacity:.60;stroke:#ea580c;stroke-width:2}.badge{fill:#ecfdf5;stroke:#10b981;stroke-width:1.2}.small{font:500 15px Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#475569}',
        '</style></defs>',
        '<rect width="1200" height="470" fill="#ffffff"/>',
        '<text class="title" x="20" y="32">DYN-07 可复现实验：geometry → log-density → stochastic trace</text>',
    ]
    for x, y, w, h in panels:
        lines.append(f'<rect class="panel" x="{x}" y="{y}" width="{w}" height="{h}"/>')

    # Panel A: transformed unit square.
    lines += [
        '<text class="title" x="42" y="88">A　非正规形变与面积收缩</text>',
        '<line class="axis" x1="65" y1="350" x2="350" y2="350"/>',
        '<line class="axis" x1="105" y1="375" x2="105" y2="120"/>',
    ]
    scale = 82.0
    ox, oy = 105.0, 350.0
    unit = [(ox, oy), (ox + scale, oy), (ox + scale, oy - scale), (ox, oy - scale)]
    m = nonnormal_exp(0.5)
    transformed_xy = [(0.0, 0.0), (m[0][0], m[1][0]), (m[0][0] + m[0][1], m[1][0] + m[1][1]), (m[0][1], m[1][1])]
    transformed = [(ox + scale * x, oy - scale * y) for x, y in transformed_xy]
    unit_s = " ".join(f"{x:.2f},{y:.2f}" for x, y in unit)
    trans_s = " ".join(f"{x:.2f},{y:.2f}" for x, y in transformed)
    lines += [
        f'<polygon class="square0" points="{unit_s}"/>',
        f'<polygon class="square1" points="{trans_s}"/>',
        '<text class="label" x="70" y="398">蓝：t=0　橙：t=0.5</text>',
        f'<text class="math" x="45" y="112">det exp(tA)=exp(-3t)={linear["det"]:.6f}</text>',
        f'<text class="label" x="45" y="420">polygon area={linear["area"]:.6f}; σmax={linear["smax"]:.3f}</text>',
    ]

    # Panel B: log-log errors.
    lines += [
        '<text class="title" x="437" y="88">B　RK4 增广系统同步阶</text>',
        '<line class="axis" x1="470" y1="365" x2="755" y2="365"/>',
        '<line class="axis" x1="470" y1="365" x2="470" y2="125"/>',
        '<text class="small" x="676" y="386">steps N (log₂)</text>',
        '<text class="small" transform="translate(446 245) rotate(-90)">endpoint error (log₁₀)</text>',
    ]
    ns = nonlinear["steps"]
    xerrs = nonlinear["x_errors"]
    lerrs = nonlinear["logp_errors"]
    all_logs = [math.log10(e) for e in xerrs + lerrs]
    ymin, ymax = min(all_logs) - 0.3, max(all_logs) + 0.3

    def plot_points(vals: list[float]) -> list[tuple[float, float]]:
        pts = []
        for n, value in zip(ns, vals):
            px = 480 + (math.log(n, 2) - math.log(ns[0], 2)) / (math.log(ns[-1], 2) - math.log(ns[0], 2)) * 260
            ly = math.log10(value)
            py = 350 - (ly - ymin) / (ymax - ymin) * 205
            pts.append((px, py))
        return pts

    xpts = plot_points(xerrs)
    lpts = plot_points(lerrs)
    lines.append(svg_polyline(xpts, "blue"))
    lines.append(svg_polyline(lpts, "orange"))
    for x, y in xpts:
        lines.append(f'<circle class="dotb" cx="{x:.2f}" cy="{y:.2f}" r="4"/>')
    for x, y in lpts:
        lines.append(f'<circle class="doto" cx="{x:.2f}" cy="{y:.2f}" r="4"/>')
    lines += [
        '<text class="label" x="490" y="113" fill="#2563eb">● state error</text>',
        '<text class="label" x="600" y="113" fill="#ea580c">● logp error</text>',
        f'<text class="math" x="482" y="409">last observed order: x={nonlinear["x_order"]:.3f}, logp={nonlinear["logp_order"]:.3f}</text>',
        f'<text class="label" x="482" y="429">Liouville residual={nonlinear["liouville_residual"]:.2e}</text>',
    ]

    # Panel C: standard error and actual cumulative errors.
    lines += [
        '<text class="title" x="832" y="88">C　Hutchinson 无偏、方差与 SE</text>',
        '<line class="axis" x1="855" y1="350" x2="1145" y2="350"/>',
        '<line class="axis" x1="855" y1="350" x2="855" y2="130"/>',
        '<text class="small" x="1070" y="374">probes m (log₂)</text>',
        '<text class="small" transform="translate(833 274) rotate(-90)">absolute error / theoretical SE</text>',
    ]
    counts = trace["counts"]
    actual = trace["actual_errors"]
    ses = trace["standard_errors"]
    positive = [v for v in actual + ses if v > 0]
    cmin, cmax = math.log10(min(positive)) - 0.3, math.log10(max(positive)) + 0.3

    def trace_points(vals: list[float]) -> list[tuple[float, float]]:
        pts = []
        for count, value in zip(counts, vals):
            px = 865 + math.log(count, 2) / math.log(counts[-1], 2) * 265
            safe = max(value, min(positive) * 0.5)
            py = 335 - (math.log10(safe) - cmin) / (cmax - cmin) * 185
            pts.append((px, py))
        return pts

    septs = trace_points(ses)
    actpts = trace_points(actual)
    lines.append(svg_polyline(septs, "green"))
    lines.append(svg_polyline(actpts, "violet"))
    for x, y in septs:
        lines.append(f'<circle class="dotg" cx="{x:.2f}" cy="{y:.2f}" r="4"/>')
    lines += [
        '<text class="label" x="868" y="113">绿：理论 SE ∝ m⁻¹ᐟ²　紫虚线：单条累计均值误差</text>',
        f'<text class="math" x="868" y="396">trace={trace["true_trace"]:.2f}; exact-enum mean={trace["enum_mean"]:.2f}</text>',
        f'<text class="label" x="868" y="420">enum variance={trace["enum_variance"]:.2f} = theory {trace["theory_variance"]:.2f}</text>',
    ]
    lines += [
        '<rect class="badge" x="970" y="445" width="180" height="18" rx="9"/>',
        '<text class="small" x="998" y="458">all assertions passed</text>',
        '</svg>',
    ]
    return "\n".join(lines) + "\n"


def run(output: Path) -> None:
    # Track A: nonnormal linear flow.
    t = 0.5
    m = nonnormal_exp(t)
    det = det2(m)
    exact_det = math.exp(-3.0 * t)
    mapped = [
        (0.0, 0.0),
        (m[0][0], m[1][0]),
        (m[0][0] + m[0][1], m[1][0] + m[1][1]),
        (m[0][1], m[1][1]),
    ]
    area = polygon_area(mapped)
    smax, smin = singular_values_2x2(m)
    assert abs(det - exact_det) < 1e-14
    assert abs(area - exact_det) < 1e-14
    assert smax > 1.0 and smin > 0.0
    linear = {"det": det, "area": area, "smax": smax, "smin": smin}

    # Track B: nonlinear exact flow and augmented RK4.
    x0 = 1.2
    t1 = 1.0
    logp0 = -0.5 * x0 * x0 - 0.5 * math.log(2.0 * math.pi)
    x_exact, logp_exact, jac = exact_augmented(x0, logp0, t1)
    steps = [10, 20, 40, 80, 160]
    x_errors: list[float] = []
    logp_errors: list[float] = []
    for n in steps:
        x_num, logp_num = integrate_rk4(x0, logp0, t1, n)
        x_errors.append(abs(x_num - x_exact))
        logp_errors.append(abs(logp_num - logp_exact))
    x_orders = observed_orders(x_errors)
    logp_orders = observed_orders(logp_errors)
    liouville_residual = abs((logp_exact - logp0) + math.log(jac))
    assert all(b < a for a, b in zip(x_errors, x_errors[1:]))
    assert all(b < a for a, b in zip(logp_errors, logp_errors[1:]))
    # The state error has a short pre-asymptotic cancellation at N=20→40;
    # the finest refinement must nevertheless recover fourth order.
    assert x_orders[-1] > 3.8
    assert min(logp_orders[-2:]) > 3.8
    assert liouville_residual < 1e-14
    nonlinear: dict[str, object] = {
        "x0": x0,
        "steps": steps,
        "x_exact": x_exact,
        "logp_exact": logp_exact,
        "jac": jac,
        "x_errors": x_errors,
        "logp_errors": logp_errors,
        "x_orders": x_orders,
        "logp_orders": logp_orders,
        "x_order": x_orders[-1],
        "logp_order": logp_orders[-1],
        "liouville_residual": liouville_residual,
    }

    # Track C: exact enumeration of all Rademacher probes in d=4.
    n = len(TRACE_MATRIX)
    probes = list(itertools.product((-1, 1), repeat=n))
    values = [quadratic(TRACE_MATRIX, eps) for eps in probes]
    true_trace = sum(TRACE_MATRIX[i][i] for i in range(n))
    enum_mean = sum(values) / len(values)
    enum_variance = population_variance(values)
    sym = symmetric_part(TRACE_MATRIX)
    theory_variance = 4.0 * sum(sym[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
    gaussian_variance = 2.0 * sum(sym[i][j] ** 2 for i in range(n) for j in range(n))
    counts = [1, 4, 16, 64, 256, 1024]
    means = cumulative_probe_means(TRACE_MATRIX, counts, 20260819)
    actual_errors = [abs(value - true_trace) for value in means]
    standard_errors = [math.sqrt(theory_variance / count) for count in counts]
    assert abs(enum_mean - true_trace) < 1e-14
    assert abs(enum_variance - theory_variance) < 1e-14
    assert abs(theory_variance - 27.25) < 1e-14
    assert abs(gaussian_variance - 55.75) < 1e-14
    trace: dict[str, object] = {
        "true_trace": true_trace,
        "enum_mean": enum_mean,
        "enum_variance": enum_variance,
        "theory_variance": theory_variance,
        "gaussian_variance": gaussian_variance,
        "counts": counts,
        "means": means,
        "actual_errors": actual_errors,
        "standard_errors": standard_errors,
    }

    svg = build_svg(linear, nonlinear, trace)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print("TRACK A — NONNORMAL FLOW")
    print(f"det(exp(tA))={det:.12e}  polygon_area={area:.12e}  sigma_max={smax:.8f}  sigma_min={smin:.8f}")
    print("TRACK B — NONLINEAR CNF RK4")
    print(f"exact_x={x_exact:.12e}  exact_logp={logp_exact:.12e}  jac={jac:.12e}")
    for nstep, xe, le in zip(steps, x_errors, logp_errors):
        print(f"N={nstep:4d}  state_error={xe:.12e}  logp_error={le:.12e}")
    print("state_orders=" + ",".join(f"{p:.8f}" for p in x_orders))
    print("logp_orders=" + ",".join(f"{p:.8f}" for p in logp_orders))
    print(f"liouville_residual={liouville_residual:.3e}")
    print("TRACK C — HUTCHINSON")
    print(f"trace={true_trace:.8f}  enum_mean={enum_mean:.8f}  enum_var={enum_variance:.8f}  rad_theory={theory_variance:.8f}  gaussian_theory={gaussian_variance:.8f}")
    for count, mean, err, se in zip(counts, means, actual_errors, standard_errors):
        print(f"m={count:4d}  cumulative_mean={mean:.8f}  abs_error={err:.8f}  theory_se={se:.8f}")
    print(f"SVG={output}")
    print(f"SHA256={digest}")
    print("ALL ASSERTIONS PASSED")


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    default = root / "00-知识库管理/_assets/plots/dynamics/plot-cnf-liouville-hutchinson-v2.svg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=default)
    args = parser.parse_args()
    run(args.output.resolve())


if __name__ == "__main__":
    main()
