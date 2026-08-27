#!/usr/bin/env python3
"""Reproducible DYN-05 audit: order, adaptivity, and discrete gradients.

Only Python's standard library is required. The script prints machine-checkable
tables, runs assertions, and deterministically writes one SVG report.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "00-知识库管理/_assets/plots/dynamics/plot-ode-order-adaptivity-gradient-v2.svg"


def euler_step(t: float, y: float, h: float, f) -> float:
    return y + h * f(t, y)


def heun_step(t: float, y: float, h: float, f) -> float:
    k1 = f(t, y)
    k2 = f(t + h, y + h * k1)
    return y + 0.5 * h * (k1 + k2)


def rk4_step(t: float, y: float, h: float, f) -> float:
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def fixed_solve(stepper, n: int) -> float:
    h = 1.0 / n
    t, y = 0.0, 1.0
    for _ in range(n):
        y = stepper(t, y, h, lambda _t, state: state)
        t += h
    return y


def fitted_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def adaptive_euler_heun(rtol: float) -> dict:
    """Integrate y'=2t cos(t^2), y(0)=0, exact y=sin(t^2), to T=4."""

    atol = 0.01 * rtol
    t, y, h = 0.0, 0.0, 0.1
    accepted = rejected = nfe = 0
    max_error = 0.0
    history: list[tuple[float, float, float]] = []

    def f(time: float, _state: float) -> float:
        return 2.0 * time * math.cos(time * time)

    while t < 4.0:
        h = min(h, 0.5, 4.0 - t)
        if h < 1e-13:
            raise RuntimeError("adaptive step underflow")
        k1 = f(t, y)
        low = y + h * k1
        k2 = f(t + h, low)
        high = y + 0.5 * h * (k1 + k2)
        nfe += 2
        scale = atol + rtol * max(abs(y), abs(high))
        err = abs(high - low) / scale
        if err <= 1.0:
            t += h
            y = high
            accepted += 1
            node_error = abs(y - math.sin(t * t))
            max_error = max(max_error, node_error)
            history.append((t, h, node_error))
        else:
            rejected += 1

        if err == 0.0:
            factor = 5.0
        else:
            factor = 0.9 * err ** (-0.5)
            factor = min(5.0, max(0.2, factor))
        h *= factor

    return {
        "rtol": rtol,
        "atol": atol,
        "endpoint_error": abs(y - math.sin(16.0)),
        "max_error": max_error,
        "accepted": accepted,
        "rejected": rejected,
        "nfe": nfe,
        "history": history,
    }


def objective(theta: float, n: int, c: float = 1.5) -> float:
    h = 1.0 / n
    y = (1.0 + h * theta) ** n
    return 0.5 * (y - c) ** 2


def discrete_gradient(theta: float, n: int, c: float = 1.5) -> float:
    h = 1.0 / n
    q = 1.0 + h * theta
    y = q**n
    return (y - c) * q ** (n - 1)


def finite_difference_gradient(theta: float, n: int) -> float:
    # For this float64 scale, 1e-5 balances O(eps^2) truncation against
    # subtractive cancellation more reliably than an unnecessarily tiny step.
    eps = 1e-5
    return (objective(theta + eps, n) - objective(theta - eps, n)) / (2.0 * eps)


def log_map(value: float, lo: float, hi: float, a: float, b: float) -> float:
    lv, llo, lhi = math.log10(value), math.log10(lo), math.log10(hi)
    return a + (lv - llo) * (b - a) / (lhi - llo)


def linear_map(value: float, lo: float, hi: float, a: float, b: float) -> float:
    return a + (value - lo) * (b - a) / (hi - lo)


def polyline(points: list[tuple[float, float]], color: str) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    circles = "".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="{color}"/>' for x, y in points
    )
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.4"/>{circles}'


def render_svg(order_rows: dict, adaptive_rows: list[dict], gradient_rows: list[dict]) -> str:
    colors = {"Euler": "#dc6b5a", "Heun": "#3f8f83", "RK4": "#4867aa"}
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="480" viewBox="0 0 1320 480" role="img" aria-labelledby="title desc">',
        '<title id="title">ODE 阶数、自适应步长与离散梯度审计</title>',
        '<desc id="desc">三面板分别比较固定步长方法的观测阶、自适应 Euler–Heun 的误差与成本、离散梯度和连续目标梯度的差异。</desc>',
        '<rect width="1320" height="480" fill="#ffffff"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#263238}.title{font-size:22px;font-weight:700}.sub{font-size:17px;fill:#53636a}.tick{font-size:15px;fill:#62727a}.box{fill:#fffefb;stroke:#d6dee8;stroke-width:1.2}.grid{stroke:#e7e9e5;stroke-width:1}</style>',
        '<text x="35" y="33" class="title">DYN-05：阶数、自适应步长与离散梯度审计</text>',
        '<text x="35" y="53" class="sub">所有曲线由同一可重复脚本生成；线段只连接实际观测点。</text>',
    ]

    panels = [(28, 76, 402, 372), (458, 76, 402, 372), (888, 76, 404, 372)]
    for x, y, w, h in panels:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="box"/>')

    # Panel A: fixed-step order.
    parts += [
        '<text x="48" y="107" class="title">A  Fixed-step observed order</text>',
        '<text x="48" y="127" class="sub">y′=y, T=1；横轴 h，纵轴 endpoint error</text>',
    ]
    ax0, ax1, ay0, ay1 = 72.0, 404.0, 154.0, 382.0
    all_errors = [e for row in order_rows.values() for e in row["errors"]]
    elo, ehi = min(all_errors) * 0.7, max(all_errors) * 1.5
    hlo, hhi = min(order_rows["Euler"]["hs"]), max(order_rows["Euler"]["hs"])
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        yy = ay1 - frac * (ay1 - ay0)
        parts.append(f'<line x1="{ax0}" y1="{yy:.1f}" x2="{ax1}" y2="{yy:.1f}" class="grid"/>')
    for name, row in order_rows.items():
        pts = [
            (log_map(h, hlo, hhi, ax0, ax1), log_map(e, elo, ehi, ay1, ay0))
            for h, e in zip(row["hs"], row["errors"])
        ]
        parts.append(polyline(pts, colors[name]))
    legend_y = 408
    for index, name in enumerate(("Euler", "Heun", "RK4")):
        x = 75 + 108 * index
        slope = order_rows[name]["slope"]
        parts += [
            f'<line x1="{x}" y1="{legend_y}" x2="{x+19}" y2="{legend_y}" stroke="{colors[name]}" stroke-width="3"/>',
            f'<text x="{x+25}" y="{legend_y+4}" class="tick">{name}: {slope:.3f}</text>',
        ]
    parts += [
        f'<text x="{ax0}" y="397" class="tick">h={hlo:.5f}</text>',
        f'<text x="{ax1-58}" y="397" class="tick">h={hhi:.3f}</text>',
        '<text x="48" y="434" class="sub">斜率接近 1 / 2 / 4，而非由单个网格点猜测。</text>',
    ]

    # Panel B: adaptive step history and sweep table.
    parts += [
        '<text x="478" y="107" class="title">B  Adaptive Euler–Heun</text>',
        '<text x="478" y="127" class="sub">y′=2t cos(t²), exact y=sin(t²)</text>',
    ]
    chosen = adaptive_rows[1]
    hist = chosen["history"]
    bx0, bx1, by0, by1 = 492.0, 836.0, 153.0, 295.0
    hmax = max(item[1] for item in hist)
    pts = [
        (linear_map(t, 0.0, 4.0, bx0, bx1), linear_map(h, 0.0, hmax, by1, by0))
        for t, h, _ in hist
    ]
    for frac in (0.0, 0.5, 1.0):
        yy = by1 - frac * (by1 - by0)
        parts.append(f'<line x1="{bx0}" y1="{yy:.1f}" x2="{bx1}" y2="{yy:.1f}" class="grid"/>')
    parts.append(polyline(pts, "#7b5ca7"))
    parts += [
        f'<text x="{bx0}" y="310" class="tick">t=0</text>',
        f'<text x="{bx1-22}" y="310" class="tick">t=4</text>',
        f'<text x="{bx0}" y="147" class="tick">h max={hmax:.3g}</text>',
        '<text x="482" y="337" class="tick">rtol</text>',
        '<text x="552" y="337" class="tick">accepted/rejected</text>',
        '<text x="682" y="337" class="tick">NFE</text>',
        '<text x="740" y="337" class="tick">max error</text>',
    ]
    for idx, row in enumerate(adaptive_rows):
        yy = 359 + idx * 25
        parts += [
            f'<text x="482" y="{yy}" class="tick">{row["rtol"]:.0e}</text>',
            f'<text x="566" y="{yy}" class="tick">{row["accepted"]}/{row["rejected"]}</text>',
            f'<text x="682" y="{yy}" class="tick">{row["nfe"]}</text>',
            f'<text x="740" y="{yy}" class="tick">{row["max_error"]:.2e}</text>',
        ]
    parts.append('<text x="478" y="434" class="sub">容差收紧提高成本并降低观测误差，但不是先验全局证书。</text>')

    # Panel C: continuous/discrete gradient gap.
    parts += [
        '<text x="908" y="107" class="title">C  Continuous vs discrete gradient</text>',
        '<text x="908" y="127" class="sub">y′=θy, θ=0.7；finite difference检查 J_h</text>',
    ]
    cx0, cx1, cy0, cy1 = 930.0, 1262.0, 154.0, 360.0
    ns = [row["n"] for row in gradient_rows]
    hs = [1.0 / n for n in ns]
    cont = [row["continuous_gap"] for row in gradient_rows]
    fd = [max(row["fd_gap"], 1e-13) for row in gradient_rows]
    glo = min(fd + cont) * 0.6
    ghi = max(fd + cont) * 1.5
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        yy = cy1 - frac * (cy1 - cy0)
        parts.append(f'<line x1="{cx0}" y1="{yy:.1f}" x2="{cx1}" y2="{yy:.1f}" class="grid"/>')
    cont_pts = [
        (log_map(h, min(hs), max(hs), cx0, cx1), log_map(g, glo, ghi, cy1, cy0))
        for h, g in zip(hs, cont)
    ]
    fd_pts = [
        (log_map(h, min(hs), max(hs), cx0, cx1), log_map(g, glo, ghi, cy1, cy0))
        for h, g in zip(hs, fd)
    ]
    parts += [
        polyline(cont_pts, "#d2694f"),
        polyline(fd_pts, "#3d7692"),
        '<line x1="932" y1="387" x2="951" y2="387" stroke="#d2694f" stroke-width="3"/>',
        '<text x="958" y="391" class="tick">|g_h − g|：离散化差距</text>',
        '<line x1="932" y1="411" x2="951" y2="411" stroke="#3d7692" stroke-width="3"/>',
        '<text x="958" y="415" class="tick">|g_h − FD(J_h)|：实现检查</text>',
        f'<text x="908" y="438" class="sub">continuous gap slope = {fitted_slope(hs, cont):.3f}；两种“误差”回答不同问题。</text>',
    ]
    parts.append('</svg>')
    return "".join(parts)


def main() -> None:
    ns = [8, 16, 32, 64, 128]
    hs = [1.0 / n for n in ns]
    steppers = {"Euler": euler_step, "Heun": heun_step, "RK4": rk4_step}
    order_rows = {}
    print("FIXED_STEP_ORDER")
    print("method\tN\th\tendpoint_error")
    for name, stepper in steppers.items():
        errors = []
        for n, h in zip(ns, hs):
            error = abs(fixed_solve(stepper, n) - math.e)
            errors.append(error)
            print(f"{name}\t{n}\t{h:.10g}\t{error:.12e}")
        slope = fitted_slope(hs, errors)
        order_rows[name] = {"hs": hs, "errors": errors, "slope": slope}
        print(f"observed_order\t{name}\t{slope:.6f}")

    adaptive_rows = [adaptive_euler_heun(rtol) for rtol in (1e-3, 1e-5, 1e-7)]
    print("\nADAPTIVE_SWEEP")
    print("rtol\tatol\taccepted\trejected\tNFE\tendpoint_error\tmax_node_error")
    for row in adaptive_rows:
        print(
            f'{row["rtol"]:.0e}\t{row["atol"]:.0e}\t{row["accepted"]}\t'
            f'{row["rejected"]}\t{row["nfe"]}\t{row["endpoint_error"]:.12e}\t'
            f'{row["max_error"]:.12e}'
        )

    theta = 0.7
    exact_gradient = (math.exp(theta) - 1.5) * math.exp(theta)
    gradient_rows = []
    print("\nGRADIENT_AUDIT")
    print("N\th\tdiscrete\tfinite_difference\tcontinuous_gap\tFD_gap")
    for n in (4, 8, 16, 32, 64, 128):
        gd = discrete_gradient(theta, n)
        gfd = finite_difference_gradient(theta, n)
        row = {
            "n": n,
            "discrete": gd,
            "fd": gfd,
            "continuous_gap": abs(gd - exact_gradient),
            "fd_gap": abs(gd - gfd),
        }
        gradient_rows.append(row)
        print(
            f'{n}\t{1/n:.10g}\t{gd:.12e}\t{gfd:.12e}\t'
            f'{row["continuous_gap"]:.12e}\t{row["fd_gap"]:.12e}'
        )

    assert 0.90 < order_rows["Euler"]["slope"] < 1.05
    assert 1.90 < order_rows["Heun"]["slope"] < 2.05
    assert 3.85 < order_rows["RK4"]["slope"] < 4.10
    assert all(
        adaptive_rows[i + 1]["max_error"] < adaptive_rows[i]["max_error"]
        for i in range(len(adaptive_rows) - 1)
    )
    assert max(row["fd_gap"] for row in gradient_rows) < 2e-9
    gradient_order = fitted_slope(
        [1.0 / row["n"] for row in gradient_rows],
        [row["continuous_gap"] for row in gradient_rows],
    )
    assert 0.80 < gradient_order < 1.05

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_svg(order_rows, adaptive_rows, gradient_rows), encoding="utf-8")
    print(f"\nASSERTIONS_PASSED\nSVG\t{OUT}")


if __name__ == "__main__":
    main()
