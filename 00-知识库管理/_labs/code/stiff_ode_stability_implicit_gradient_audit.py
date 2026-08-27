#!/usr/bin/env python3
"""DYN-06 reproducible audit: stability, stiff tracking, implicit gradient."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "00-知识库管理/_assets/plots/dynamics/plot-stiff-stability-implicit-gradient-v2.svg"


def r_euler(z: float) -> float:
    return 1.0 + z


def r_rk4(z: float) -> float:
    return 1.0 + z + z * z / 2.0 + z**3 / 6.0 + z**4 / 24.0


def r_be(z: float) -> float:
    return 1.0 / (1.0 - z)


def r_trap(z: float) -> float:
    return (1.0 + z / 2.0) / (1.0 - z / 2.0)


def bisect_rk4_boundary() -> float:
    """Positive a solving R_RK4(-a)=1 away from a=0."""
    lo, hi = 2.0, 3.5
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if r_rk4(-mid) < 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


KAPPA = 1000.0


def rhs(t: float, y: float) -> float:
    return -KAPPA * (y - math.cos(t)) - math.sin(t)


def tracking_step(method: str, t: float, y: float, h: float) -> float:
    if method == "Euler":
        return y + h * rhs(t, y)
    if method == "RK4":
        k1 = rhs(t, y)
        k2 = rhs(t + h / 2.0, y + h * k1 / 2.0)
        k3 = rhs(t + h / 2.0, y + h * k2 / 2.0)
        k4 = rhs(t + h, y + h * k3)
        return y + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    if method == "BE":
        return (
            y + h * KAPPA * math.cos(t + h) - h * math.sin(t + h)
        ) / (1.0 + h * KAPPA)
    if method == "Trap":
        return (
            (1.0 - h * KAPPA / 2.0) * y
            + h * KAPPA * (math.cos(t) + math.cos(t + h)) / 2.0
            - h * (math.sin(t) + math.sin(t + h)) / 2.0
        ) / (1.0 + h * KAPPA / 2.0)
    raise ValueError(method)


def tracking_solve(method: str, n: int, perturbation: float = 0.0) -> dict:
    h = 1.0 / n
    t, y = 0.0, 1.0 + perturbation
    max_error = 0.0
    for _ in range(n):
        y = tracking_step(method, t, y, h)
        t += h
        exact = math.cos(t) + perturbation * math.exp(-KAPPA * t)
        error = abs(y - exact)
        max_error = max(max_error, error)
        if not math.isfinite(y) or abs(y) > 1e200:
            return {"endpoint_error": math.inf, "max_error": math.inf, "y": y}
    exact_final = math.cos(1.0) + perturbation * math.exp(-KAPPA)
    return {"endpoint_error": abs(y - exact_final), "max_error": max_error, "y": y}


def first_n_for_tolerance(method: str, tolerance: float) -> tuple[int, dict]:
    # Multiples of ten put every method on a shared t=0.1 audit grid.
    for n in range(10, 2001, 10):
        result = tracking_solve(method, n)
        if result["max_error"] <= tolerance:
            return n, result
    raise RuntimeError(f"no qualifying N for {method}")


def implicit_objective(theta: float, n: int, total_time: float = 0.1) -> float:
    h = total_time / n
    q = 1.0 / (1.0 - h * theta)
    return q**n


def implicit_gradient(theta: float, n: int, total_time: float = 0.1) -> float:
    h = total_time / n
    q = 1.0 / (1.0 - h * theta)
    return total_time * q ** (n + 1)


def finite_difference_gradient(theta: float, n: int) -> float:
    eps = 1e-4
    return (implicit_objective(theta + eps, n) - implicit_objective(theta - eps, n)) / (
        2.0 * eps
    )


def fitted_slope(xs: list[float], ys: list[float]) -> float:
    lx, ly = [math.log(x) for x in xs], [math.log(y) for y in ys]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def linear_map(v: float, lo: float, hi: float, a: float, b: float) -> float:
    return a + (v - lo) * (b - a) / (hi - lo)


def log_map(v: float, lo: float, hi: float, a: float, b: float) -> float:
    lv, llo, lhi = math.log10(v), math.log10(lo), math.log10(hi)
    return a + (lv - llo) * (b - a) / (lhi - llo)


def line(points: list[tuple[float, float]], color: str, width: float = 2.2) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def render_svg(boundary: float, equal_error: dict, gradient_rows: list[dict]) -> str:
    colors = {"Euler": "#dc6255", "RK4": "#9a5ab5", "BE": "#27856f", "Trap": "#356fa3"}
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="480" viewBox="0 0 1320 480" role="img" aria-labelledby="title desc">',
        '<title id="title">刚性稳定域、隐式追踪与梯度对象审计</title>',
        '<desc id="desc">三面板分别扫描负实轴绝对稳定域、比较同节点误差下的刚性追踪成本、核对 backward Euler 离散梯度与连续梯度差异。</desc>',
        '<rect width="1320" height="480" fill="#ffffff"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#263238}.title{font-size:22px;font-weight:700}.sub{font-size:17px;fill:#56666e}.tick{font-size:15px;fill:#63737b}.box{fill:#fffefb;stroke:#d6dee8;stroke-width:1.2}.grid{stroke:#e7e9e5;stroke-width:1}.threshold{stroke:#89969b;stroke-width:1.3;stroke-dasharray:5 4}</style>',
        '<text x="35" y="33" class="title">DYN-06：刚性稳定、隐式追踪与梯度对象审计</text>',
        '<text x="35" y="53" class="sub">解析解与解析放大因子作reference；NFE不替代隐式代数成本。</text>',
    ]
    for x in (28, 458, 888):
        parts.append(f'<rect x="{x}" y="76" width="402" height="372" class="box"/>')

    # A: negative-real stability scan.
    parts += [
        '<text x="48" y="107" class="title">A  Negative-real stability scan</text>',
        '<text x="48" y="127" class="sub">横轴 a=−z；纵轴 |R(−a)|（log，曲线截于 10³）</text>',
    ]
    x0, x1, y0, y1 = 70.0, 405.0, 151.0, 356.0
    ymin, ymax = 1e-3, 1e3
    threshold_y = log_map(1.0, ymin, ymax, y1, y0)
    parts.append(f'<line x1="{x0}" y1="{threshold_y:.2f}" x2="{x1}" y2="{threshold_y:.2f}" class="threshold"/>')
    parts.append(f'<text x="{x0+4}" y="{threshold_y-6:.2f}" class="tick">|R|=1 stability boundary</text>')
    functions = {"Euler": r_euler, "RK4": r_rk4, "BE": r_be, "Trap": r_trap}
    for name, fn in functions.items():
        pts = []
        for i in range(201):
            a = 10.0 * i / 200.0
            mag = min(ymax, max(ymin, abs(fn(-a))))
            pts.append((linear_map(a, 0.0, 10.0, x0, x1), log_map(mag, ymin, ymax, y1, y0)))
        parts.append(line(pts, colors[name]))
    parts += [
        f'<text x="{x0}" y="373" class="tick">a=0</text>',
        f'<text x="{x1-27}" y="373" class="tick">a=10</text>',
        f'<text x="48" y="397" class="sub">RK4 截点 a≈{boundary:.4f}；BE随a增大→0，Trap→1。</text>',
    ]
    for i, name in enumerate(("Euler", "RK4", "BE", "Trap")):
        lx = 62 + i * 84
        parts += [
            f'<line x1="{lx}" y1="418" x2="{lx+17}" y2="418" stroke="{colors[name]}" stroke-width="3"/>',
            f'<text x="{lx+22}" y="422" class="tick">{name}</text>',
        ]

    # B: equal-error shared-grid steps and contamination.
    parts += [
        '<text x="478" y="107" class="title">B  Stiff tracking at equal node error</text>',
        '<text x="478" y="127" class="sub">κ=1000，max node error ≤10⁻³；候选N为10的倍数</text>',
    ]
    bx0, bybase, barmax = 500.0, 318.0, 175.0
    names = ("Euler", "RK4", "BE", "Trap")
    for i, name in enumerate(names):
        n = equal_error[name]["n"]
        height = barmax * n / 500.0
        x = bx0 + i * 78
        parts += [
            f'<rect x="{x}" y="{bybase-height:.2f}" width="45" height="{height:.2f}" rx="4" fill="{colors[name]}" opacity="0.86"/>',
            f'<text x="{x+7}" y="{bybase-height-7:.2f}" class="tick">N={n}</text>',
            f'<text x="{x+4}" y="337" class="tick">{name}</text>',
        ]
    parts += [
        '<line x1="488" y1="318" x2="830" y2="318" class="grid"/>',
        '<text x="478" y="364" class="sub">加入初始fast contamination 10⁻³，N=10：</text>',
        f'<text x="478" y="385" class="tick">BE final fast error ≈ {equal_error["contam_be"]:.2e}</text>',
        f'<text x="478" y="405" class="tick">Trap final fast error ≈ {equal_error["contam_trap"]:.2e}</text>',
        '<text x="478" y="430" class="sub">大步稳定与fast-mode damping仍是两项不同能力。</text>',
    ]

    # C: implicit gradient.
    parts += [
        '<text x="908" y="107" class="title">C  Backward-Euler implicit gradient</text>',
        '<text x="908" y="127" class="sub">y′=θy, θ=−50, T=0.1；J_h=y_N</text>',
    ]
    cx0, cx1, cy0, cy1 = 930.0, 1263.0, 153.0, 348.0
    hs = [row["h"] for row in gradient_rows]
    cont = [row["continuous_gap"] for row in gradient_rows]
    fd = [max(row["fd_gap"], 1e-14) for row in gradient_rows]
    lo, hi = min(cont + fd) * 0.5, max(cont + fd) * 2.0
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        yy = cy1 - frac * (cy1 - cy0)
        parts.append(f'<line x1="{cx0}" y1="{yy:.2f}" x2="{cx1}" y2="{yy:.2f}" class="grid"/>')
    cont_pts = [(log_map(h, min(hs), max(hs), cx0, cx1), log_map(g, lo, hi, cy1, cy0)) for h, g in zip(hs, cont)]
    fd_pts = [(log_map(h, min(hs), max(hs), cx0, cx1), log_map(g, lo, hi, cy1, cy0)) for h, g in zip(hs, fd)]
    parts += [
        line(cont_pts, "#d2694f"),
        line(fd_pts, "#397997"),
        '<line x1="932" y1="376" x2="951" y2="376" stroke="#d2694f" stroke-width="3"/>',
        '<text x="958" y="380" class="tick">|g_h−g|：time discretization</text>',
        '<line x1="932" y1="400" x2="951" y2="400" stroke="#397997" stroke-width="3"/>',
        '<text x="958" y="404" class="tick">|g_h−FD(J_h)|：implementation</text>',
        f'<text x="908" y="430" class="sub">continuous gap slope={fitted_slope(hs, cont):.3f}；FD验证的是J_h。</text>',
    ]
    parts.append('</svg>')
    return "".join(parts)


def main() -> None:
    boundary = bisect_rk4_boundary()
    print("STABILITY_AUDIT")
    print(f"rk4_negative_real_boundary\t{boundary:.12f}")
    print("method\tR(-10)\tabs_R(-10)\tR(-100)")
    functions = {"Euler": r_euler, "RK4": r_rk4, "BE": r_be, "Trap": r_trap}
    for name, fn in functions.items():
        print(f"{name}\t{fn(-10):.12e}\t{abs(fn(-10)):.12e}\t{fn(-100):.12e}")

    equal_error = {}
    print("\nTRACKING_EQUAL_ERROR")
    print("method\tN\tendpoint_error\tmax_node_error")
    for name in ("Euler", "RK4", "BE", "Trap"):
        n, result = first_n_for_tolerance(name, 1e-3)
        equal_error[name] = {"n": n, **result}
        print(f'{name}\t{n}\t{result["endpoint_error"]:.12e}\t{result["max_error"]:.12e}')

    # Propagate the linear fast-error recurrence analytically. Direct subtraction of
    # two O(1) trajectories would hide the BE value below float64 resolution.
    h_contam = 0.1
    equal_error["contam_be"] = 1e-3 * abs(r_be(-KAPPA * h_contam)) ** 10
    equal_error["contam_trap"] = 1e-3 * abs(r_trap(-KAPPA * h_contam)) ** 10
    print("\nFAST_CONTAMINATION")
    print("method\tN\tisolated_final_contamination")
    print(f'BE\t10\t{equal_error["contam_be"]:.12e}')
    print(f'Trap\t10\t{equal_error["contam_trap"]:.12e}')

    theta, total_time = -50.0, 0.1
    exact_gradient = total_time * math.exp(theta * total_time)
    gradient_rows = []
    print("\nIMPLICIT_GRADIENT")
    print("N\th\tdiscrete\tfinite_difference\tcontinuous_gap\tFD_gap")
    for n in (5, 10, 20, 40, 80, 160):
        gd = implicit_gradient(theta, n, total_time)
        gfd = finite_difference_gradient(theta, n)
        row = {
            "n": n,
            "h": total_time / n,
            "discrete": gd,
            "fd": gfd,
            "continuous_gap": abs(gd - exact_gradient),
            "fd_gap": abs(gd - gfd),
        }
        gradient_rows.append(row)
        print(f'{n}\t{row["h"]:.10g}\t{gd:.12e}\t{gfd:.12e}\t{row["continuous_gap"]:.12e}\t{row["fd_gap"]:.12e}')

    assert abs(boundary - 2.7852935634) < 1e-9
    assert abs(r_euler(-2.0)) == 1.0 and abs(r_euler(-2.01)) > 1.0
    assert abs(r_be(-100.0)) < 0.01
    assert abs(r_trap(-100.0)) > 0.96 and r_trap(-100.0) < 0.0
    assert equal_error["Euler"]["n"] == 500
    assert equal_error["RK4"]["n"] == 360
    assert equal_error["BE"]["n"] == 10
    assert equal_error["Trap"]["n"] == 10
    assert equal_error["contam_be"] < 1e-20
    assert equal_error["contam_trap"] > 6e-4
    assert max(row["fd_gap"] for row in gradient_rows) < 1e-11
    gradient_order = fitted_slope(
        [row["h"] for row in gradient_rows],
        [row["continuous_gap"] for row in gradient_rows],
    )
    assert 0.85 < gradient_order < 1.05

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_svg(boundary, equal_error, gradient_rows), encoding="utf-8")
    print(f"\nASSERTIONS_PASSED\nSVG\t{OUT}")


if __name__ == "__main__":
    main()
