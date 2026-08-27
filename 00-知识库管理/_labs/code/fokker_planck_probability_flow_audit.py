#!/usr/bin/env python3
"""Deterministic Fokker–Planck, probability-flow, and score-error audit."""

from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path


SEED = 20260819
KAPPA = 0.8
SIGMA_OU = 0.7
V0_OU = 0.4
T_OU = 0.6
DOMAIN = 6.0
FPE_GRIDS = [80, 160, 320]

V0 = 0.4
SIGMA = 0.9
T = 1.0
PATHS = 5000
N_MAX = 512
RESOLUTIONS = [16, 32, 64, 128, 256, 512]
SCORE_EPSILONS = [-0.20, -0.10, -0.05, 0.0, 0.05, 0.10, 0.20]
ODE_RESOLUTIONS = [8, 16, 32, 64, 128, 256, 512]

ROOT = Path(__file__).resolve().parents[3]
PLOT = ROOT / "00-知识库管理/_assets/plots/dynamics/plot-fokker-planck-probability-flow-v1.svg"


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def variance(xs: list[float]) -> float:
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def covariance(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)


def slope(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )


def normal_pdf(x: float, var: float) -> float:
    return math.exp(-0.5 * x * x / var) / math.sqrt(2.0 * math.pi * var)


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.3) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def circles(points: list[tuple[float, float]], color: str, radius: float = 3.5) -> str:
    return "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}"/>'
        for x, y in points
    )


def solve_ou_fpe(n: int) -> dict[str, float]:
    dx = 2.0 * DOMAIN / n
    centers = [-DOMAIN + (i + 0.5) * dx for i in range(n)]
    p = [normal_pdf(x, V0_OU) for x in centers]
    mass0 = sum(p) * dx
    p = [x / mass0 for x in p]
    diffusion = 0.5 * SIGMA_OU * SIGMA_OU
    max_speed = KAPPA * DOMAIN
    dt_limit = 0.42 / (max_speed / dx + 2.0 * diffusion / (dx * dx))
    steps = math.ceil(T_OU / dt_limit)
    dt = T_OU / steps

    min_density = min(p)
    for _ in range(steps):
        flux = [0.0] * (n + 1)
        for i in range(1, n):
            x_face = -DOMAIN + i * dx
            drift = -KAPPA * x_face
            p_up = p[i - 1] if drift >= 0.0 else p[i]
            flux[i] = drift * p_up - diffusion * (p[i] - p[i - 1]) / dx
        p = [
            p[i] - (dt / dx) * (flux[i + 1] - flux[i])
            for i in range(n)
        ]
        min_density = min(min_density, min(p))

    exact_var = (
        V0_OU * math.exp(-2.0 * KAPPA * T_OU)
        + SIGMA_OU * SIGMA_OU / (2.0 * KAPPA)
        * (1.0 - math.exp(-2.0 * KAPPA * T_OU))
    )
    exact = [normal_pdf(x, exact_var) for x in centers]
    mass = sum(p) * dx
    numeric_mean = sum(x * q for x, q in zip(centers, p)) * dx
    numeric_var = sum((x - numeric_mean) ** 2 * q for x, q in zip(centers, p)) * dx
    l1_error = sum(abs(q - e) for q, e in zip(p, exact)) * dx
    return {
        "n": float(n),
        "dx": dx,
        "steps": float(steps),
        "mass_error": abs(mass - 1.0),
        "min_density": min_density,
        "mean": numeric_mean,
        "variance": numeric_var,
        "exact_variance": exact_var,
        "l1_error": l1_error,
    }


def probability_flow_coupling() -> dict[str, object]:
    rng = random.Random(SEED)
    fine_h = T / N_MAX
    sqrt_h = math.sqrt(fine_h)
    qv_sde = {n: [] for n in RESOLUTIONS}
    qv_pf = {n: [] for n in RESOLUTIONS}
    sde_half: list[float] = []
    sde_final: list[float] = []
    pf_half: list[float] = []
    pf_final: list[float] = []

    for _ in range(PATHS):
        x0 = math.sqrt(V0) * rng.gauss(0.0, 1.0)
        fine = [sqrt_h * rng.gauss(0.0, 1.0) for _ in range(N_MAX)]
        w_half = sum(fine[: N_MAX // 2])
        w_final = w_half + sum(fine[N_MAX // 2 :])
        v_half = V0 + SIGMA * SIGMA * 0.5
        v_final = V0 + SIGMA * SIGMA * T
        sde_half.append(x0 + SIGMA * w_half)
        sde_final.append(x0 + SIGMA * w_final)
        pf_half.append(x0 * math.sqrt(v_half / V0))
        pf_final.append(x0 * math.sqrt(v_final / V0))

        for n in RESOLUTIONS:
            block = N_MAX // n
            coarse = [
                sum(fine[start : start + block])
                for start in range(0, N_MAX, block)
            ]
            qv_sde[n].append(sum((SIGMA * dw) ** 2 for dw in coarse))
            pf_values = [
                x0 * math.sqrt((V0 + SIGMA * SIGMA * (i / n)) / V0)
                for i in range(n + 1)
            ]
            qv_pf[n].append(
                sum((pf_values[i + 1] - pf_values[i]) ** 2 for i in range(n))
            )

    sde_qv_mean = [mean(qv_sde[n]) for n in RESOLUTIONS]
    pf_qv_mean = [mean(qv_pf[n]) for n in RESOLUTIONS]
    log_h = [math.log(T / n) for n in RESOLUTIONS]
    return {
        "sde_qv_mean": sde_qv_mean,
        "pf_qv_mean": pf_qv_mean,
        "sde_qv_order": slope(log_h, [math.log(x) for x in sde_qv_mean]),
        "pf_qv_order": slope(log_h, [math.log(x) for x in pf_qv_mean]),
        "sde_var_half": variance(sde_half),
        "sde_var_final": variance(sde_final),
        "pf_var_half": variance(pf_half),
        "pf_var_final": variance(pf_final),
        "sde_cross_cov": covariance(sde_half, sde_final),
        "pf_cross_cov": covariance(pf_half, pf_final),
        "theory_var_half": V0 + SIGMA * SIGMA * 0.5,
        "theory_var_final": V0 + SIGMA * SIGMA * T,
        "theory_sde_cross": V0 + SIGMA * SIGMA * 0.5,
        "theory_pf_cross": math.sqrt(
            (V0 + SIGMA * SIGMA * 0.5) * (V0 + SIGMA * SIGMA * T)
        ),
    }


def score_and_solver_errors() -> dict[str, object]:
    v_final = V0 + SIGMA * SIGMA * T
    ratio = v_final / V0
    score_relative_errors = [
        ratio**epsilon - 1.0 for epsilon in SCORE_EPSILONS
    ]
    solver_relative_errors: list[float] = []
    for n in ODE_RESOLUTIONS:
        h = T / n
        factor = 1.0
        for k in range(n):
            t = k * h
            velocity_rate = (
                SIGMA * SIGMA / (2.0 * (V0 + SIGMA * SIGMA * t))
            )
            factor *= 1.0 + h * velocity_rate
        variance_n = V0 * factor * factor
        solver_relative_errors.append(abs(variance_n / v_final - 1.0))
    solver_order = slope(
        [math.log(T / n) for n in ODE_RESOLUTIONS],
        [math.log(x) for x in solver_relative_errors],
    )
    return {
        "score_relative_errors": score_relative_errors,
        "solver_relative_errors": solver_relative_errors,
        "solver_order": solver_order,
        "v_final": v_final,
    }


def make_svg(
    fpe: list[dict[str, float]],
    coupling: dict[str, object],
    score: dict[str, object],
) -> str:
    navy = "#0f172a"
    slate = "#475569"
    axis = "#94a3b8"
    blue = "#2563eb"
    green = "#059669"
    orange = "#ea580c"
    violet = "#7c3aed"

    fpe_x = [math.log10(x["dx"]) for x in fpe]
    fpe_y = [math.log10(x["l1_error"]) for x in fpe]
    fx0, fx1 = min(fpe_x), max(fpe_x)
    fy0, fy1 = min(fpe_y) - 0.25, max(fpe_y) + 0.25
    fpe_points = [
        (
            75 + 275 * (x - fx0) / (fx1 - fx0),
            300 - 160 * (y - fy0) / (fy1 - fy0),
        )
        for x, y in zip(fpe_x, fpe_y)
    ]

    qv_sde = coupling["sde_qv_mean"]
    qv_pf = coupling["pf_qv_mean"]
    assert isinstance(qv_sde, list) and isinstance(qv_pf, list)
    qx = [math.log2(n) for n in RESOLUTIONS]
    qy_all = [math.log10(x) for x in qv_sde + qv_pf]
    qx0, qx1 = min(qx), max(qx)
    qy0, qy1 = min(qy_all) - 0.25, max(qy_all) + 0.25

    def qpoints(values: list[float]) -> list[tuple[float, float]]:
        return [
            (
                465 + 275 * (x - qx0) / (qx1 - qx0),
                300 - 160 * (math.log10(y) - qy0) / (qy1 - qy0),
            )
            for x, y in zip(qx, values)
        ]

    sde_points = qpoints(qv_sde)
    pf_points = qpoints(qv_pf)

    rel = score["score_relative_errors"]
    assert isinstance(rel, list)
    ex0, ex1 = min(SCORE_EPSILONS), max(SCORE_EPSILONS)
    ey0, ey1 = min(rel) - 0.04, max(rel) + 0.04
    score_points = [
        (
            855 + 275 * (e - ex0) / (ex1 - ex0),
            265 - 120 * (r - ey0) / (ey1 - ey0),
        )
        for e, r in zip(SCORE_EPSILONS, rel)
    ]
    zero_y = 265 - 120 * (0.0 - ey0) / (ey1 - ey0)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430" role="img" aria-labelledby="title desc">
<title id="title">DYN-11 Fokker–Planck 与概率流 ODE 审计</title>
<desc id="desc">三面板展示守恒有限体积求解OU Fokker–Planck的收敛、同边缘SDE与概率流ODE的不同二次变差，以及score误差和有限步ODE误差的分账。</desc>
<rect width="1200" height="430" fill="#ffffff"/>
<text x="20" y="32" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="20" font-weight="700" fill="{navy}">DYN-11 可复现实验：密度守恒 → 同边缘不同路径 → score/solver 分账</text>

<rect x="20" y="55" width="370" height="355" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="42" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="18.5" font-weight="700" fill="{navy}">A　守恒通量推进 OU 密度</text>
<line x1="75" y1="300" x2="350" y2="300" stroke="{axis}" stroke-width="1.2"/>
<line x1="75" y1="130" x2="75" y2="300" stroke="{axis}" stroke-width="1.2"/>
{polyline(fpe_points, blue)}
{circles(fpe_points, blue)}
<text x="92" y="119" font-family="Georgia,'Times New Roman',serif" font-size="13" font-weight="600" fill="{blue}">L1 density error vs cell width</text>
<text x="92" y="327" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">cell width dx (coarser →)</text>
<text x="47" y="230" transform="rotate(-90 47 230)" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">log error</text>
<text x="74" y="355" font-family="Georgia,'Times New Roman',serif" font-size="13" font-weight="600" fill="{navy}">observed order = {slope(fpe_x, fpe_y):.3f}</text>
<text x="74" y="379" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{green}">max mass drift={max(x['mass_error'] for x in fpe):.1e}; min p={min(x['min_density'] for x in fpe):.1e}</text>

<rect x="410" y="55" width="370" height="355" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="432" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="18.5" font-weight="700" fill="{navy}">B　相同 marginals，不同 path law</text>
<line x1="465" y1="300" x2="740" y2="300" stroke="{axis}" stroke-width="1.2"/>
<line x1="465" y1="130" x2="465" y2="300" stroke="{axis}" stroke-width="1.2"/>
{polyline(sde_points, orange)}
{circles(sde_points, orange)}
{polyline(pf_points, green)}
{circles(pf_points, green)}
<text x="482" y="118" font-family="Georgia,'Times New Roman',serif" font-size="12.8" font-weight="600" fill="{orange}">SDE QV order={coupling['sde_qv_order']:.3f} (constant)</text>
<text x="482" y="140" font-family="Georgia,'Times New Roman',serif" font-size="12.8" font-weight="600" fill="{green}">probability-flow QV order={coupling['pf_qv_order']:.3f}</text>
<text x="482" y="327" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">partition count N (finer →)</text>
<text x="438" y="230" transform="rotate(-90 438 230)" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">log realized QV</text>
<text x="464" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="12.3" fill="{navy}">两者 Var(X_T) 都接近 {coupling['theory_var_final']:.3f}</text>
<text x="464" y="382" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="12.3" fill="{navy}">但 cross-time covariance 与二次变差不同</text>

<rect x="800" y="55" width="380" height="355" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="822" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="18.5" font-weight="700" fill="{navy}">C　score 误差不是 ODE 步长误差</text>
<line x1="855" y1="{zero_y:.2f}" x2="1130" y2="{zero_y:.2f}" stroke="{axis}" stroke-width="1.2" stroke-dasharray="5 4"/>
<line x1="855" y1="130" x2="855" y2="270" stroke="{axis}" stroke-width="1.2"/>
{polyline(score_points, violet)}
{circles(score_points, violet)}
<text x="872" y="119" font-family="Georgia,'Times New Roman',serif" font-size="12.8" font-weight="600" fill="{violet}">final variance error vs score scale error</text>
<text x="872" y="294" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">score multiplicative error epsilon</text>
<text x="828" y="225" transform="rotate(-90 828 225)" font-family="Georgia,'Times New Roman',serif" font-size="12.5" fill="{slate}">relative variance error</text>
<rect x="842" y="316" width="306" height="67" rx="10" fill="#ffffff" stroke="#ddd6fe"/>
<text x="995" y="340" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-size="13" font-weight="600" fill="{blue}">exact-score Euler ODE order = {score['solver_order']:.3f}</text>
<text x="995" y="362" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="12.2" fill="{navy}">h → 0 只能消除 solver bias</text>
<text x="995" y="378" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="12.2" fill="{navy}">错误 score 的连续流仍到达错误密度</text>
</svg>
"""


def validate(
    fpe: list[dict[str, float]],
    coupling: dict[str, object],
    score: dict[str, object],
    svg: str,
) -> None:
    fpe_order = slope(
        [math.log(x["dx"]) for x in fpe],
        [math.log(x["l1_error"]) for x in fpe],
    )
    assert 0.75 < fpe_order < 1.20
    assert max(x["mass_error"] for x in fpe) < 2.0e-13
    assert min(x["min_density"] for x in fpe) > -2.0e-14
    assert -0.08 < float(coupling["sde_qv_order"]) < 0.08
    assert 0.90 < float(coupling["pf_qv_order"]) < 1.10
    assert abs(float(coupling["sde_var_final"]) - float(coupling["theory_var_final"])) < 0.05
    assert abs(float(coupling["pf_var_final"]) - float(coupling["theory_var_final"])) < 0.05
    assert 0.90 < float(score["solver_order"]) < 1.08
    rel = score["score_relative_errors"]
    assert isinstance(rel, list) and abs(rel[3]) < 1.0e-15
    assert svg.count("<rect") >= 5 and svg.count("<polyline") >= 4


def print_results(
    fpe: list[dict[str, float]],
    coupling: dict[str, object],
    score: dict[str, object],
    digest: str,
) -> None:
    fpe_order = slope(
        [math.log(x["dx"]) for x in fpe],
        [math.log(x["l1_error"]) for x in fpe],
    )
    print("DYN-11 Fokker-Planck / probability-flow audit")
    print("FPE grid  steps  L1_error  mass_error  min_density  variance")
    for x in fpe:
        print(
            f"{int(x['n']):3d} {int(x['steps']):5d} {x['l1_error']:.8e} "
            f"{x['mass_error']:.3e} {x['min_density']:.3e} {x['variance']:.8f}"
        )
    print(f"FPE L1 order             = {fpe_order:.8f}")
    print("N   SDE_QV_mean   PF_QV_mean")
    for i, n in enumerate(RESOLUTIONS):
        print(
            f"{n:3d} {coupling['sde_qv_mean'][i]:.8e} "
            f"{coupling['pf_qv_mean'][i]:.8e}"
        )
    print(f"SDE QV order             = {coupling['sde_qv_order']:.8f}")
    print(f"PF ODE QV order          = {coupling['pf_qv_order']:.8f}")
    print(
        "final variances SDE/PF/theory = "
        f"{coupling['sde_var_final']:.8f}/"
        f"{coupling['pf_var_final']:.8f}/"
        f"{coupling['theory_var_final']:.8f}"
    )
    print(
        "cross covariances SDE/PF/theory = "
        f"{coupling['sde_cross_cov']:.8f}/"
        f"{coupling['pf_cross_cov']:.8f}/"
        f"{coupling['theory_sde_cross']:.8f},"
        f"{coupling['theory_pf_cross']:.8f}"
    )
    print("score epsilon -> final variance relative error")
    for e, r in zip(SCORE_EPSILONS, score["score_relative_errors"]):
        print(f"{e:+.2f} -> {r:+.8f}")
    print(f"exact-score Euler order  = {score['solver_order']:.8f}")
    print(f"svg_sha256={digest}")


def main() -> None:
    fpe = [solve_ou_fpe(n) for n in FPE_GRIDS]
    coupling = probability_flow_coupling()
    score = score_and_solver_errors()
    svg = make_svg(fpe, coupling, score)
    validate(fpe, coupling, score, svg)
    PLOT.parent.mkdir(parents=True, exist_ok=True)
    PLOT.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(PLOT.read_bytes()).hexdigest()
    print_results(fpe, coupling, score, digest)


if __name__ == "__main__":
    main()
