#!/usr/bin/env python3
"""Re-render DYN-10/11 deterministic audits in the v2 research-plot style."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import fokker_planck_probability_flow_audit as fp
import ito_sde_numerics_gradient_audit as ito


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "00-知识库管理/_assets/plots/dynamics"
ITO_OUT = OUT / "plot-ito-sde-numerics-gradient-v2.svg"
FP_OUT = OUT / "plot-fokker-planck-probability-flow-v2.svg"

BG = "#fbfaf7"
INK = "#25313d"
MUTED = "#66778c"
GRID = "#d5dee8"
BLUE = "#2f6fec"
TEAL = "#0f7f75"
RED = "#c94134"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif"
MATH = "Georgia,'Times New Roman',serif"


def esc(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tx(x: float, y: float, value: object, size: float = 15, weight: int = 500, color: str = INK, anchor: str = "start", family: str = FONT) -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{esc(value)}</text>'


def ln(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 1.5, dash: str | None = None) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"{extra}/>'


def poly(points: list[tuple[float, float]], color: str, width: float = 2.6) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dots = "".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.2" fill="{BG}" stroke="{color}" stroke-width="2.2"/>' for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>{dots}'


def log_points(xs: list[float], ys: list[float], left: float, top: float, width: float, height: float) -> list[tuple[float, float]]:
    lx = [math.log10(x) for x in xs]
    ly = [math.log10(max(y, 1.0e-18)) for y in ys]
    x0, x1 = min(lx), max(lx)
    y0, y1 = min(ly), max(ly)
    pad = max(0.12, 0.12 * (y1 - y0 or 1.0))
    y0, y1 = y0 - pad, y1 + pad
    return [(left + width * (x - x0) / (x1 - x0 or 1.0), top + height * (y1 - y) / (y1 - y0 or 1.0)) for x, y in zip(lx, ly)]


def log_points_shared(xs: list[float], series: list[list[float]], left: float, top: float, width: float, height: float) -> list[list[tuple[float, float]]]:
    lx = [math.log10(x) for x in xs]
    all_y = [math.log10(max(y, 1.0e-18)) for values in series for y in values]
    x0, x1 = min(lx), max(lx)
    y0, y1 = min(all_y), max(all_y)
    pad = max(0.12, 0.12 * (y1 - y0 or 1.0))
    y0, y1 = y0 - pad, y1 + pad
    return [[(left + width * (x - x0) / (x1 - x0 or 1.0), top + height * (y1 - math.log10(max(y, 1.0e-18))) / (y1 - y0 or 1.0)) for x, y in zip(lx, values)] for values in series]


def axes(left: float, top: float, width: float, height: float, x_left: str, x_right: str, y_label: str) -> list[str]:
    return [
        ln(left, top + height, left + width, top + height, INK, 1.6),
        ln(left, top, left, top + height, INK, 1.6),
        ln(left, top + height * 0.5, left + width, top + height * 0.5, GRID, 1, "4 5"),
        tx(left, top + height + 27, x_left, 15, 500, MUTED),
        tx(left + width, top + height + 27, x_right, 15, 500, MUTED, "end"),
        tx(left - 33, top + height * 0.55, y_label, 15, 500, MUTED, "middle", MATH),
    ]


def shell(title: str, desc: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(desc)}</desc>',
        f'<rect width="1200" height="600" fill="{BG}"/>',
        ln(400, 35, 400, 525, GRID, 2),
        ln(800, 35, 800, 525, GRID, 2),
        f'<style>text{{font-family:{FONT};font-variant-numeric:tabular-nums lining-nums}}</style>',
    ]


def finish(out: list[str], footer: str) -> str:
    out += [ln(60, 535, 1140, 535, GRID, 2), tx(600, 572, footer, 18, 700, INK, "middle"), "</svg>"]
    return "\n".join(out)


def ito_svg(r: dict[str, object]) -> str:
    hs = [ito.T / n for n in ito.RESOLUTIONS]
    ito_rmse = list(r["ito_rmse"])
    corr = [abs(x - 0.5) for x in r["correction_mean"]]
    strong = list(r["strong_rmse"])
    weak = list(r["weak_bias"])
    gap = list(r["gradient_gap_rmse"])
    fd = list(r["fd_abs_error"])
    out = shell("Itô 和、SDE 强弱误差与离散梯度审计", "固定 seed 与 nested Brownian increments 下，三面板分别报告 Itô 左端点和的收敛及二次变差修正、Euler–Maruyama 对 GBM 的强弱误差、离散梯度与有限差分和连续目标之间的误差。")
    out += [tx(42, 60, "A", 24, 750, BLUE), tx(80, 60, "Itô 左和与 1/2 修正", 21, 700), tx(430, 60, "B", 24, 750, TEAL), tx(468, 60, "同路径 strong / weak 误差", 21, 700), tx(830, 60, "C", 24, 750, RED), tx(868, 60, "离散梯度与连续极限", 21, 700)]
    lefts = (75.0, 465.0, 855.0)
    top, pw, ph = 115.0, 280.0, 260.0
    for left in lefts:
        out += axes(left, top, pw, ph, "fine h", "coarse h", "log10 error")
    a1, a2 = log_points_shared(hs, [ito_rmse, corr], lefts[0], top, pw, ph)
    b1, b2 = log_points_shared(hs, [strong, weak], lefts[1], top, pw, ph)
    c1, c2 = log_points_shared(hs, [gap, fd], lefts[2], top, pw, ph)
    out += [poly(a1, BLUE), poly(a2, TEAL), tx(82, 101, f"left-sum RMSE  p={r['ito_order']:.3f}", 15, 650, BLUE), tx(82, 425, "teal: |mean correction - 0.5|", 15, 600, TEAL), tx(82, 454, f"finest correction={r['correction_mean'][-1]:.4f}", 15, 600)]
    out += [poly(b1, RED), poly(b2, TEAL), tx(472, 101, f"strong endpoint  p={r['strong_order']:.3f}", 15, 650, RED), tx(472, 425, f"weak mean bias  p={r['weak_order']:.3f}", 15, 650, TEAL), tx(472, 454, "same nested Brownian paths for strong error", 15, 600)]
    out += [poly(c1, RED), poly(c2, BLUE), tx(862, 101, f"pathwise gradient gap  p={r['gradient_gap_order']:.3f}", 15, 650, RED), tx(862, 425, "blue: discrete tangent vs finite difference", 15, 600, BLUE), tx(862, 454, "FD validates J_h, not J_h=J", 15, 650)]
    out += [tx(75, 495, f"seed={ito.SEED}; paths={ito.PATHS}; Nmax={ito.N_MAX}; GBM mu={ito.MU}, sigma={ito.SIGMA}", 15, 500, MUTED), tx(855, 495, f"max tangent–FD gap={max(fd):.2e}", 15, 500, MUTED)]
    return finish(out, "同路径耦合定义 strong error；期望定义 weak error；离散梯度一致性不能替代连续目标收敛。")


def fp_svg(fpe_data: list[dict[str, float]], coupling: dict[str, object], score: dict[str, object]) -> str:
    out = shell("Fokker–Planck、概率流与 score/solver 误差审计", "三面板分别报告 OU Fokker–Planck 守恒有限体积的网格收敛、相同 one-time marginals 下 SDE 与 probability-flow ODE 的不同 quadratic variation，以及 score multiplicative error 对终端方差的偏差。")
    out += [tx(42, 60, "A", 24, 750, BLUE), tx(80, 60, "守恒 FPE 的网格收敛", 21, 700), tx(430, 60, "B", 24, 750, TEAL), tx(468, 60, "同 marginals、不同 QV", 21, 700), tx(830, 60, "C", 24, 750, RED), tx(868, 60, "score 偏差与 solver 偏差", 21, 700)]
    lefts = (75.0, 465.0, 855.0)
    top, pw, ph = 115.0, 280.0, 260.0
    out += axes(lefts[0], top, pw, ph, "fine dx", "coarse dx", "log10 L1 error")
    dx = [x["dx"] for x in fpe_data]
    err = [x["l1_error"] for x in fpe_data]
    a = log_points(dx, err, lefts[0], top, pw, ph)
    fpe_order = fp.slope([math.log(x) for x in dx], [math.log(x) for x in err])
    out += [poly(a, BLUE), tx(82, 101, f"OU finite volume  p={fpe_order:.3f}", 15, 650, BLUE), tx(82, 425, f"max mass drift={max(x['mass_error'] for x in fpe_data):.2e}", 15, 600, TEAL), tx(82, 454, f"min density={min(x['min_density'] for x in fpe_data):.2e}", 15, 600)]
    ns = list(fp.RESOLUTIONS)
    qv_sde = list(coupling["sde_qv_mean"])
    qv_pf = list(coupling["pf_qv_mean"])
    out += axes(lefts[1], top, pw, ph, "coarse N", "fine N", "log10 realized QV")
    b1, b2 = log_points_shared(ns, [qv_sde, qv_pf], lefts[1], top, pw, ph)
    out += [poly(b1, RED), poly(b2, TEAL), tx(472, 101, f"SDE QV order={coupling['sde_qv_order']:.3f}", 15, 650, RED), tx(472, 425, f"PF ODE QV order={coupling['pf_qv_order']:.3f}", 15, 650, TEAL), tx(472, 454, f"both terminal variance ~= {coupling['theory_var_final']:.3f}", 15, 600)]
    eps = list(fp.SCORE_EPSILONS)
    rel = list(score["score_relative_errors"])
    ex0, ex1 = min(eps), max(eps)
    ey0, ey1 = min(rel), max(rel)
    ey_pad = 0.08 * (ey1 - ey0)
    ey0, ey1 = ey0 - ey_pad, ey1 + ey_pad
    c = [(lefts[2] + pw * (x - ex0) / (ex1 - ex0), top + ph * (ey1 - y) / (ey1 - ey0)) for x, y in zip(eps, rel)]
    zero_y = top + ph * (ey1 - 0.0) / (ey1 - ey0)
    out += [ln(lefts[2], top + ph, lefts[2] + pw, top + ph, INK, 1.6), ln(lefts[2], top, lefts[2], top + ph, INK, 1.6), ln(lefts[2], zero_y, lefts[2] + pw, zero_y, GRID, 1.4, "5 5"), poly(c, RED), tx(862, 101, "terminal variance error vs score scale", 15, 650, RED), tx(lefts[2], 402, "epsilon=-0.20", 15, 500, MUTED), tx(lefts[2] + pw, 402, "epsilon=+0.20", 15, 500, MUTED, "end"), tx(862, 425, f"exact-score Euler order={score['solver_order']:.3f}", 15, 650, BLUE), tx(862, 454, "h->0 removes solver bias, not score bias", 15, 600)]
    out += [tx(75, 495, f"seed={fp.SEED}; paths={fp.PATHS}; OU grids=80/160/320", 15, 500, MUTED), tx(855, 495, "score epsilon range=-0.20..+0.20", 15, 500, MUTED)]
    return finish(out, "守恒、路径 law 与 score/solver 误差是三道独立验收门；相同终端 histogram 不能合并它们。")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ito_results = ito.run_audit()
    ito_text = ito_svg(ito_results)
    ito.validate(ito_results, ito.make_svg(ito_results))
    ITO_OUT.write_text(ito_text, encoding="utf-8")

    fpe_data = [fp.solve_ou_fpe(n) for n in fp.FPE_GRIDS]
    coupling = fp.probability_flow_coupling()
    score = fp.score_and_solver_errors()
    old_svg = fp.make_svg(fpe_data, coupling, score)
    fp.validate(fpe_data, coupling, score, old_svg)
    FP_OUT.write_text(fp_svg(fpe_data, coupling, score), encoding="utf-8")

    print(f"{ITO_OUT} sha256={hashlib.sha256(ITO_OUT.read_bytes()).hexdigest()}")
    print(f"{FP_OUT} sha256={hashlib.sha256(FP_OUT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
