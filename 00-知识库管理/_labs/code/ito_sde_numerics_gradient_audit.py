#!/usr/bin/env python3
"""Deterministic Itô-sum, SDE-discretization, and gradient audit.

The script intentionally uses only the Python standard library.  Every coarse
grid is formed by summing one finest Brownian increment array, so strong errors
compare approximations driven by the same Brownian path.
"""

from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path


SEED = 20260819
T = 1.0
X0 = 1.0
MU = 0.35
SIGMA = 0.80
TARGET = 1.40
PATHS = 6000
N_MAX = 512
RESOLUTIONS = [8, 16, 32, 64, 128, 256, 512]
FD_EPS = 1.0e-5
ROOT = Path(__file__).resolve().parents[3]
PLOT = ROOT / "00-知识库管理/_assets/plots/dynamics/plot-ito-sde-numerics-gradient-v1.svg"


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def slope(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.3) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def circles(points: list[tuple[float, float]], color: str) -> str:
    return "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{color}"/>'
        for x, y in points
    )


def coarse_increments(fine: list[float], n: int) -> list[float]:
    block = N_MAX // n
    return [sum(fine[start : start + block]) for start in range(0, N_MAX, block)]


def em_terminal(increments: list[float], sigma: float = SIGMA) -> float:
    h = T / len(increments)
    x = X0
    for dw in increments:
        x *= 1.0 + MU * h + sigma * dw
    return x


def em_terminal_and_sigma_sensitivity(increments: list[float]) -> tuple[float, float]:
    h = T / len(increments)
    x = X0
    sensitivity = 0.0
    for dw in increments:
        factor = 1.0 + MU * h + SIGMA * dw
        sensitivity = sensitivity * factor + x * dw
        x *= factor
    return x, sensitivity


def run_audit() -> dict[str, object]:
    rng = random.Random(SEED)
    sqrt_h_fine = math.sqrt(T / N_MAX)

    ito_sq_error = {n: 0.0 for n in RESOLUTIONS}
    strat_sq_error = {n: 0.0 for n in RESOLUTIONS}
    correction_sum = {n: 0.0 for n in RESOLUTIONS}
    strong_sq_error = {n: 0.0 for n in RESOLUTIONS}
    gradient_gap_sq = {n: 0.0 for n in RESOLUTIONS}
    gradient_sum = {n: 0.0 for n in RESOLUTIONS}
    objective_sum = {n: 0.0 for n in RESOLUTIONS}
    objective_plus_sum = {n: 0.0 for n in RESOLUTIONS}
    objective_minus_sum = {n: 0.0 for n in RESOLUTIONS}

    for _ in range(PATHS):
        fine = [sqrt_h_fine * rng.gauss(0.0, 1.0) for _ in range(N_MAX)]
        w_t = sum(fine)
        exact_x = X0 * math.exp((MU - 0.5 * SIGMA * SIGMA) * T + SIGMA * w_t)
        exact_s = exact_x * (w_t - SIGMA * T)
        exact_grad_sample = (exact_x - TARGET) * exact_s

        for n in RESOLUTIONS:
            increments = coarse_increments(fine, n)
            qv = sum(dw * dw for dw in increments)
            left = 0.5 * (w_t * w_t - qv)
            trapezoid = 0.5 * w_t * w_t
            ito_target = 0.5 * (w_t * w_t - T)
            strat_target = 0.5 * w_t * w_t
            ito_sq_error[n] += (left - ito_target) ** 2
            strat_sq_error[n] += (trapezoid - strat_target) ** 2
            correction_sum[n] += trapezoid - left

            x, sensitivity = em_terminal_and_sigma_sensitivity(increments)
            strong_sq_error[n] += (x - exact_x) ** 2
            grad_sample = (x - TARGET) * sensitivity
            gradient_gap_sq[n] += (grad_sample - exact_grad_sample) ** 2
            gradient_sum[n] += grad_sample
            objective_sum[n] += 0.5 * (x - TARGET) ** 2

            x_plus = em_terminal(increments, SIGMA + FD_EPS)
            x_minus = em_terminal(increments, SIGMA - FD_EPS)
            objective_plus_sum[n] += 0.5 * (x_plus - TARGET) ** 2
            objective_minus_sum[n] += 0.5 * (x_minus - TARGET) ** 2

    ito_rmse = [math.sqrt(ito_sq_error[n] / PATHS) for n in RESOLUTIONS]
    strat_rmse = [math.sqrt(strat_sq_error[n] / PATHS) for n in RESOLUTIONS]
    correction_mean = [correction_sum[n] / PATHS for n in RESOLUTIONS]
    strong_rmse = [math.sqrt(strong_sq_error[n] / PATHS) for n in RESOLUTIONS]
    weak_bias = [
        abs(X0 * (1.0 + MU * T / n) ** n - X0 * math.exp(MU * T))
        for n in RESOLUTIONS
    ]
    gradient_gap_rmse = [
        math.sqrt(gradient_gap_sq[n] / PATHS) for n in RESOLUTIONS
    ]
    gradients = [gradient_sum[n] / PATHS for n in RESOLUTIONS]
    objectives = [objective_sum[n] / PATHS for n in RESOLUTIONS]
    finite_difference = [
        (objective_plus_sum[n] - objective_minus_sum[n]) / (2.0 * FD_EPS * PATHS)
        for n in RESOLUTIONS
    ]
    fd_abs_error = [abs(g - fd) for g, fd in zip(gradients, finite_difference)]

    log_h = [math.log(T / n) for n in RESOLUTIONS]
    results: dict[str, object] = {
        "ito_rmse": ito_rmse,
        "strat_rmse": strat_rmse,
        "correction_mean": correction_mean,
        "strong_rmse": strong_rmse,
        "weak_bias": weak_bias,
        "gradient_gap_rmse": gradient_gap_rmse,
        "gradients": gradients,
        "objectives": objectives,
        "finite_difference": finite_difference,
        "fd_abs_error": fd_abs_error,
        "ito_order": slope(log_h, [math.log(x) for x in ito_rmse]),
        "strong_order": slope(log_h, [math.log(x) for x in strong_rmse]),
        "weak_order": slope(log_h, [math.log(x) for x in weak_bias]),
        "gradient_gap_order": slope(
            log_h, [math.log(x) for x in gradient_gap_rmse]
        ),
    }
    return results


def make_svg(r: dict[str, object]) -> str:
    width, height = 1200, 430
    navy = "#0f172a"
    slate = "#475569"
    axis = "#94a3b8"
    blue = "#2563eb"
    green = "#059669"
    orange = "#ea580c"
    violet = "#7c3aed"

    hs = [T / n for n in RESOLUTIONS]
    xlogs = [math.log2(h) for h in hs]
    xlo, xhi = min(xlogs), max(xlogs)

    def points(values: list[float], left: float, ymin: float, ymax: float) -> list[tuple[float, float]]:
        return [
            (
                left + 275.0 * (x - xlo) / (xhi - xlo),
                315.0 - 178.0 * (math.log10(y) - ymin) / (ymax - ymin),
            )
            for x, y in zip(xlogs, values)
        ]

    ito = r["ito_rmse"]
    strong = r["strong_rmse"]
    weak = r["weak_bias"]
    grad_gap = r["gradient_gap_rmse"]
    fd_err = r["fd_abs_error"]
    corrections = r["correction_mean"]
    assert all(isinstance(x, list) for x in [ito, strong, weak, grad_gap, fd_err, corrections])

    a_logs = [math.log10(y) for y in ito]
    a_lo, a_hi = min(a_logs) - 0.25, max(a_logs) + 0.25
    a_points = points(ito, 75.0, a_lo, a_hi)

    b_all = [math.log10(y) for y in strong + weak]
    b_lo, b_hi = min(b_all) - 0.25, max(b_all) + 0.25
    b_strong = points(strong, 465.0, b_lo, b_hi)
    b_weak = points(weak, 465.0, b_lo, b_hi)

    c_all = [math.log10(y) for y in grad_gap + fd_err]
    c_lo, c_hi = min(c_all) - 0.35, max(c_all) + 0.35
    c_gap = points(grad_gap, 855.0, c_lo, c_hi)
    c_fd = points(fd_err, 855.0, c_lo, c_hi)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">DYN-10 Itô、SDE 数值与离散梯度审计</title>
<desc id="desc">三面板展示左端点与梯形随机和的二次变差修正、Euler–Maruyama 对几何 Brownian 运动的强弱误差，以及离散灵敏度、有限差分和连续目标之间的误差。</desc>
<rect width="1200" height="430" fill="#ffffff"/>
<text x="20" y="32" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="20" font-weight="700" fill="{navy}">DYN-10 可复现实验：积分解释 → 强/弱误差 → 离散梯度</text>

<rect x="20" y="55" width="370" height="355" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="42" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="18.5" font-weight="700" fill="{navy}">A　左端点记住二次变差</text>
<line x1="75" y1="315" x2="350" y2="315" stroke="{axis}" stroke-width="1.2"/>
<line x1="75" y1="130" x2="75" y2="315" stroke="{axis}" stroke-width="1.2"/>
{polyline(a_points, blue)}
{circles(a_points, blue)}
<text x="92" y="119" font-family="Georgia,'Times New Roman',serif" font-size="13" font-weight="600" fill="{blue}">RMSE of Ito left sum</text>
<text x="92" y="342" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">step h (coarser →)</text>
<text x="48" y="232" transform="rotate(-90 48 232)" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">log error</text>
<text x="74" y="365" font-family="Georgia,'Times New Roman',serif" font-size="13" font-weight="600" fill="{navy}">observed order = {r['ito_order']:.3f}</text>
<text x="74" y="387" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{green}">mean(trap − left) → 0.5; finest={corrections[-1]:.4f}</text>

<rect x="410" y="55" width="370" height="355" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="432" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="18.5" font-weight="700" fill="{navy}">B　同一 Brownian path 下验收 EM</text>
<line x1="465" y1="315" x2="740" y2="315" stroke="{axis}" stroke-width="1.2"/>
<line x1="465" y1="130" x2="465" y2="315" stroke="{axis}" stroke-width="1.2"/>
{polyline(b_strong, orange)}
{circles(b_strong, orange)}
{polyline(b_weak, green)}
{circles(b_weak, green)}
<text x="482" y="118" font-family="Georgia,'Times New Roman',serif" font-size="12.8" font-weight="600" fill="{orange}">strong endpoint RMSE: p={r['strong_order']:.3f}</text>
<text x="482" y="140" font-family="Georgia,'Times New Roman',serif" font-size="12.8" font-weight="600" fill="{green}">weak mean bias: p={r['weak_order']:.3f}</text>
<text x="482" y="342" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">step h (coarser →)</text>
<text x="438" y="232" transform="rotate(-90 438 232)" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">log error</text>
<text x="464" y="375" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="12.5" fill="{navy}">强误差追踪同一路径；弱误差只比较期望</text>

<rect x="800" y="55" width="380" height="355" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="822" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="18.5" font-weight="700" fill="{navy}">C　先验收离散目标，再谈连续极限</text>
<line x1="855" y1="315" x2="1130" y2="315" stroke="{axis}" stroke-width="1.2"/>
<line x1="855" y1="130" x2="855" y2="315" stroke="{axis}" stroke-width="1.2"/>
{polyline(c_gap, violet)}
{circles(c_gap, violet)}
{polyline(c_fd, blue)}
{circles(c_fd, blue)}
<text x="872" y="118" font-family="Georgia,'Times New Roman',serif" font-size="12.7" font-weight="600" fill="{violet}">pathwise gradient gap: p={r['gradient_gap_order']:.3f}</text>
<text x="872" y="140" font-family="Georgia,'Times New Roman',serif" font-size="12.7" font-weight="600" fill="{blue}">discrete tangent vs finite difference</text>
<text x="872" y="342" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">step h (coarser →)</text>
<text x="828" y="232" transform="rotate(-90 828 232)" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">log error</text>
<text x="855" y="375" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="12.4" fill="{navy}">FD 只验证同一个 J_h；它不证明 J_h = J</text>
</svg>
"""


def validate(r: dict[str, object], svg: str) -> None:
    assert 0.42 < float(r["ito_order"]) < 0.58
    assert 0.42 < float(r["strong_order"]) < 0.65
    assert 0.90 < float(r["weak_order"]) < 1.08
    assert 0.35 < float(r["gradient_gap_order"]) < 0.70
    corrections = r["correction_mean"]
    strat_rmse = r["strat_rmse"]
    fd_error = r["fd_abs_error"]
    assert isinstance(corrections, list) and abs(corrections[-1] - 0.5) < 0.015
    assert isinstance(strat_rmse, list) and max(strat_rmse) < 1.0e-12
    assert isinstance(fd_error, list) and max(fd_error) < 5.0e-8
    assert svg.count("<rect") >= 4 and svg.count("<polyline") >= 5
    assert "DYN-10" in svg and "finite difference" in svg


def print_results(r: dict[str, object], digest: str) -> None:
    print("DYN-10 Itô/SDE numerical audit")
    print(f"seed={SEED} paths={PATHS} N_max={N_MAX}")
    print("N   Ito_RMSE   correction   EM_strong   weak_mean_bias   grad_gap   FD_error")
    for i, n in enumerate(RESOLUTIONS):
        print(
            f"{n:3d} "
            f"{r['ito_rmse'][i]:.8e} "
            f"{r['correction_mean'][i]:.8f} "
            f"{r['strong_rmse'][i]:.8e} "
            f"{r['weak_bias'][i]:.8e} "
            f"{r['gradient_gap_rmse'][i]:.8e} "
            f"{r['fd_abs_error'][i]:.8e}"
        )
    print(f"Ito left-sum order      = {r['ito_order']:.8f}")
    print(f"EM strong order         = {r['strong_order']:.8f}")
    print(f"EM weak mean order      = {r['weak_order']:.8f}")
    print(f"gradient gap order      = {r['gradient_gap_order']:.8f}")
    print(f"max trapezoid identity  = {max(r['strat_rmse']):.8e}")
    print(f"max tangent-vs-FD error = {max(r['fd_abs_error']):.8e}")
    print(f"svg_sha256={digest}")


def main() -> None:
    results = run_audit()
    svg = make_svg(results)
    validate(results, svg)
    PLOT.parent.mkdir(parents=True, exist_ok=True)
    PLOT.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(PLOT.read_bytes()).hexdigest()
    print_results(results, digest)


if __name__ == "__main__":
    main()
