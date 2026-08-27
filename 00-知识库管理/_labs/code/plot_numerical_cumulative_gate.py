#!/usr/bin/env python3
"""Generate and calibrate the deterministic NUM-CUM-01 three-track gate."""

from __future__ import annotations

import argparse
import math
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    BG,
    BLUE,
    GRID,
    INK,
    MUTED,
    RED,
    TEAL,
    begin,
    finish,
    heading,
    line,
    node,
    rect,
    text,
)


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "numerical-analysis"
    / "fig-numerical-cumulative-gate-v2.svg"
)


def decimal4() -> Context:
    return Context(prec=4, rounding=ROUND_HALF_EVEN, Emin=-999, Emax=999)


def track_a(tau: float) -> dict[str, float | str]:
    with localcontext(decimal4()):
        rounded = +(Decimal(1) + Decimal(str(tau)))
        huge = Decimal("1e8")
        lost_sum = +(+(huge + Decimal(1)) - huge)
        reordered_sum = +(+(huge - huge) + Decimal(1))

    residual = tau / math.sqrt(1.0 + tau * tau)
    condition = 1.0 / tau
    return {
        "rounded": str(rounded),
        "lost_sum": float(lost_sum),
        "reordered_sum": float(reordered_sum),
        "forward": 1.0 / math.sqrt(2.0),
        "residual": residual,
        "condition": condition,
        "risk": condition * residual,
        "task_gate": 0.01 / condition,
    }


def track_b(step: float) -> dict[str, float]:
    # A has eigenvalues 1, 1, 3; Richardson B=I-step*A.
    spectral_radius = max(abs(1.0 - step), abs(1.0 - 3.0 * step))
    root_two = math.sqrt(2.0)
    return {
        "cg_relative_r1": 2.0 / 29.0,
        "cg_energy_e1_sq": 8.0 / 29.0,
        "gmres_r0": root_two,
        "gmres_r1": math.sqrt(2.0 / 5.0),
        "gmres_r2": 0.0,
        "richardson_step": step,
        "richardson_rho": spectral_radius,
        "richardson_peak": math.sqrt(5.0 / 4.0),
        "kappa_gram": 27.0 + 18.0 * root_two,
        "kappa_scaled": 9.0 + 4.0 * math.sqrt(5.0),
    }


def track_c(index_bytes: int) -> dict[str, float | int]:
    value_bytes = 8
    n = 3
    nnz_a = 4
    nnz_gram = 5
    csr_a = nnz_a * value_bytes + nnz_a * index_bytes + (n + 1) * index_bytes
    csr_gram = nnz_gram * value_bytes + nnz_gram * index_bytes + (n + 1) * index_bytes
    return {
        "index_bytes": index_bytes,
        "csr_a": csr_a,
        "dense_a": n * n * value_bytes,
        "csr_gram": csr_gram,
        "range_error": 3.0 / math.sqrt(23.0),
        "best_rank2": math.sqrt(2.0) - 1.0,
        "oversampled_range": 0.0,
        "power_tail_ratio": (3.0 - 2.0 * math.sqrt(2.0)) ** 3,
    }


def assert_canonical(a: dict[str, float | str], b: dict[str, float], c: dict[str, float | int]) -> None:
    assert a["rounded"] == "1.000"
    assert a["lost_sum"] == 0.0 and a["reordered_sum"] == 1.0
    assert math.isclose(float(a["forward"]), 1 / math.sqrt(2), abs_tol=1e-15)
    assert 0.99999999 < float(a["risk"]) < 1.0
    assert math.isclose(float(a["task_gate"]), 1e-6, abs_tol=1e-18)

    assert math.isclose(b["cg_relative_r1"], 2 / 29, abs_tol=1e-15)
    assert math.isclose(b["cg_energy_e1_sq"], 8 / 29, abs_tol=1e-15)
    assert math.isclose(b["gmres_r1"], math.sqrt(2 / 5), abs_tol=1e-15)
    assert b["gmres_r2"] == 0.0
    assert math.isclose(b["richardson_rho"], 0.5, abs_tol=1e-15)
    assert b["richardson_peak"] > 1.0
    assert b["kappa_scaled"] < b["kappa_gram"]

    assert c["csr_a"] == 64 and c["dense_a"] == 72 and c["csr_gram"] == 76
    assert math.isclose(float(c["range_error"]), 3 / math.sqrt(23), abs_tol=1e-15)
    assert float(c["range_error"]) > float(c["best_rank2"])
    assert c["oversampled_range"] == 0.0
    assert math.isclose(float(c["power_tail_ratio"]), 0.005050633883346584, abs_tol=2e-16)


def build_figure(a: dict[str, float | str], b: dict[str, float], c: dict[str, float | int]) -> str:
    out = begin(
        "数值线性代数累计门：误差链、求解链与规模链",
        "三条轨道把 NUM-01—20 收束为同一研究合同：先问有限精度误差能否解释，再按结构选择并认证求解器，最后同时核算稀疏成本和随机近似误差。",
        (BLUE, TEAL, RED),
    )

    heading(out, 42, "A", "可靠性链：残差不等于误差", BLUE)
    stages_a = (
        ("F10,4: fl(1+1e-4)=1", BLUE),
        ("rho ~= 1e-4", TEAL),
        ("kappa=1e4", RED),
        ("kappa*rho ~= 1", RED),
    )
    for index, (label, color) in enumerate(stages_a):
        y = 91 + 82 * index
        node(out, 55, y, 292, 48, label, color, size=15)
        if index < len(stages_a) - 1:
            out.append(line(201, y + 51, 201, y + 76, INK, 2.1, marker="a3"))
    out += [
        text(45, 445, f"forward error = {float(a['forward']):.4f}", 16, 700, fill=RED),
        text(45, 476, f"1% task gate requires rho <= {float(a['task_gate']):.0e}", 15, 650),
        text(45, 505, "证书必须同时写 condition、stability 与 task budget。", 15, fill=MUTED),
    ]

    heading(out, 430, "B", "结构链：选法与真残差", TEAL)
    rows_b = (
        ("SPD", "CG: ||r1||/||r0||=2/29", BLUE),
        ("general", "GMRES: sqrt2 -> sqrt(2/5) -> 0", TEAL),
        ("stationary", "rho=1/2, but transient peak > 1", RED),
        ("precondition", "kappa: 52.46 -> 17.94", BLUE),
    )
    for index, (structure, result, color) in enumerate(rows_b):
        y = 99 + 91 * index
        out += [
            rect(440, y, 105, 55, color, BG, 8, 2),
            text(492, y + 34, structure, 15, 700, "middle", color),
            text(565, y + 33, result, 15, 650),
        ]
    out += [
        line(430, 461, 765, 461, GRID, 2),
        text(430, 491, "递推量只用于导航；原算子真 residual 才能验收。", 15, fill=MUTED),
    ]

    heading(out, 830, "C", "规模链：成本与随机证书", RED)
    labels_c = (
        ("A dense", int(c["dense_a"]), BLUE),
        ("A CSR", int(c["csr_a"]), TEAL),
        ("A^T A CSR", int(c["csr_gram"]), RED),
    )
    for index, (label, value, color) in enumerate(labels_c):
        y = 112 + 65 * index
        out += [
            text(830, y + 17, label, 14, 650),
            rect(930, y, 2.25 * value, 24, color, color, 2, 0),
            text(1115, y + 18, f"{value} B", 14, 700, "end", color),
        ]
    out += [
        line(830, 325, 1145, 325, GRID, 2),
        text(830, 360, f"range error = {float(c['range_error']):.4f}", 16, 700, fill=RED),
        text(830, 394, f"best rank-2 = {float(c['best_rank2']):.4f}", 16, 700, fill=TEAL),
        text(830, 430, "p=1: range error=0, truncation error remains", 15, 650),
        text(830, 467, "另记 p/q、seed、passes、failure probability。", 15, fill=MUTED),
        text(830, 501, "nnz 与单次随机结果都不是完整证书。", 15, 700, fill=RED),
    ]
    return finish(
        out,
        "卷级判断顺序：对象与结构 -> 误差传播 -> 算法与成本 -> 独立证书 -> AI 任务容差。",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intervention", choices=("none", "a", "b", "c"), default="none")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    tau = 1e-3 if args.intervention == "a" else 1e-4
    step = 0.8 if args.intervention == "b" else 0.5
    index_bytes = 8 if args.intervention == "c" else 4
    a = track_a(tau)
    b = track_b(step)
    c = track_c(index_bytes)

    if args.intervention == "none":
        assert_canonical(a, b, c)
    elif args.output is None:
        raise SystemExit("intervention runs require --output so the canonical SVG is not overwritten")

    target = args.output or DEFAULT_OUTPUT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_figure(a, b, c), encoding="utf-8")

    print(
        "A reliability: "
        f"fl(1+tau)={a['rounded']} forward={float(a['forward']):.6f} "
        f"rho={float(a['residual']):.8f} kappa={float(a['condition']):.1f} "
        f"kappa*rho={float(a['risk']):.8f} task_gate={float(a['task_gate']):.2e}"
    )
    print(
        "B solver: "
        f"CG_rel_r1={b['cg_relative_r1']:.8f} GMRES={b['gmres_r0']:.8f}->"
        f"{b['gmres_r1']:.8f}->{b['gmres_r2']:.1f} Richardson_rho={b['richardson_rho']:.4f} "
        f"kappa={b['kappa_gram']:.5f}->{b['kappa_scaled']:.5f}"
    )
    print(
        "C scale: "
        f"index={c['index_bytes']}B CSR(A)={c['csr_a']}B dense={c['dense_a']}B "
        f"CSR(AtA)={c['csr_gram']}B range={float(c['range_error']):.8f} "
        f"best_rank2={float(c['best_rank2']):.8f} power_tail={float(c['power_tail_ratio']):.8f}"
    )
    print(target)


if __name__ == "__main__":
    main()
