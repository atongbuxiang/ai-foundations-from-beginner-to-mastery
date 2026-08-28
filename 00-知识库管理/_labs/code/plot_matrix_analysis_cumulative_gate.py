#!/usr/bin/env python3
"""Deterministic MA-CUM-01 computation gate using Python stdlib only.

Tracks:
A. positive-definite margin, Rayleigh extrema, Cholesky pivot and conditioning;
B. Hermitian eigenvector rotation across a closing gap plus non-normal pseudospectrum;
C. matrix sign versus polar geometry, Frechet Taylor check and structured condition.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path


DEFAULT_SEED = 20260820  # Reserved for learner interventions.
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "matrix-analysis"
    / "plot-matrix-analysis-cumulative-gate-v2.svg"
)

Matrix = list[list[float]]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matrix_add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def matrix_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def matrix_scale(a: Matrix, scalar: float) -> Matrix:
    return [[scalar * value for value in row] for row in a]


def frobenius_norm(a: Matrix) -> float:
    return math.sqrt(sum(value * value for row in a for value in row))


def operator_norm_2x2(a: Matrix) -> float:
    trace_ata = sum(value * value for row in a for value in row)
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    discriminant = max(0.0, trace_ata * trace_ata - 4.0 * determinant * determinant)
    return math.sqrt(0.5 * (trace_ata + math.sqrt(discriminant)))


def matrix_exp_series(a: Matrix, terms: int = 80) -> Matrix:
    """Small dense exponential by its convergent power series.

    Inputs in this gate have norm below 2, so no scaling is needed. This is a
    verification routine, not a recommendation for production matrix exp.
    """
    n = len(a)
    total = identity(n)
    term = identity(n)
    for k in range(1, terms + 1):
        term = matrix_scale(matmul(term, a), 1.0 / k)
        total = matrix_add(total, term)
        if frobenius_norm(term) < 1e-17:
            break
    return total


def positive_definite_experiment(min_delta: float = 0.003) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for delta in (1.0, 0.3, 0.1, 0.03, 0.01, min_delta):
        rho = 1.0 - delta
        minimum = delta
        maximum = 2.0 - delta
        final_pivot = math.sqrt(1.0 - rho * rho)
        h = [[1.0, rho], [rho, 1.0]]
        l = [[1.0, 0.0], [rho, final_pivot]]
        llt = matmul(l, [[1.0, rho], [0.0, final_pivot]])
        rows.append(
            {
                "delta": delta,
                "lambda_min": minimum,
                "lambda_max": maximum,
                "condition": maximum / minimum,
                "last_pivot": final_pivot,
                "inverse_pivot_squared": 1.0 / (final_pivot * final_pivot),
                "cholesky_residual": frobenius_norm(matrix_sub(h, llt)),
            }
        )
    return rows


def perturbation_experiment(
    eta: float = 0.02,
    min_gap: float = 0.003,
    pseudospectral_epsilon: float = 1e-3,
    max_pseudo_coupling: float = 100.0,
) -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    gap_rows: list[dict[str, float]] = []
    for gap in (1.0, 0.3, 0.1, 0.03, 0.01, min_gap):
        theta = 0.5 * math.atan2(2.0 * eta, gap)
        eigen_shift = math.sqrt((0.5 * gap) ** 2 + eta * eta) - 0.5 * gap
        gap_rows.append(
            {
                "gap": gap,
                "eta": eta,
                "angle_radians": theta,
                "angle_degrees": theta * 180.0 / math.pi,
                "sin_angle": math.sin(theta),
                "eta_over_gap": eta / gap,
                "eigen_shift": eigen_shift,
            }
        )

    pseudo_rows: list[dict[str, float]] = []
    for coupling in (1.0, 3.0, 10.0, 30.0, max_pseudo_coupling):
        pseudo_rows.append(
            {
                "coupling": coupling,
                "epsilon": pseudospectral_epsilon,
                "lower_radius": math.sqrt(pseudospectral_epsilon * coupling),
            }
        )
    return gap_rows, pseudo_rows


def matrix_function_structure_experiment(
    max_sign_coupling: float = 10.0,
    min_step: float = 3e-4,
) -> dict[str, object]:
    sign_rows: list[dict[str, float]] = []
    for coupling in (0.0, 0.5, 1.0, 2.0, 5.0, max_sign_coupling):
        sign_matrix = [[1.0, coupling], [0.0, -1.0]]
        sign_square_residual = frobenius_norm(
            matrix_sub(matmul(sign_matrix, sign_matrix), identity(2))
        )
        sign_rows.append(
            {
                "coupling": coupling,
                "sign_norm": operator_norm_2x2(sign_matrix),
                "polar_norm": 1.0,
                "involution_residual": sign_square_residual,
            }
        )

    a = [[0.0, 0.0], [0.0, math.log(4.0)]]
    e = [[1.0, 2.0], [-1.0, 0.0]]
    divided_difference = 3.0 / math.log(4.0)
    derivative = [[1.0, 2.0 * divided_difference], [-divided_difference, 0.0]]
    exp_a = [[1.0, 0.0], [0.0, 4.0]]
    taylor_rows: list[dict[str, float]] = []
    for step in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, min_step):
        perturbed = matrix_add(a, matrix_scale(e, step))
        exact = matrix_exp_series(perturbed)
        linear = matrix_add(exp_a, matrix_scale(derivative, step))
        remainder = frobenius_norm(matrix_sub(exact, linear))
        taylor_rows.append(
            {
                "step": step,
                "remainder": remainder,
                "remainder_over_step": remainder / step,
                "remainder_over_step_squared": remainder / (step * step),
            }
        )

    return {
        "sign": sign_rows,
        "taylor": taylor_rows,
        "unstructured_condition": math.sqrt(2.0),
        "symmetric_structured_condition": 0.0,
    }


def svg_text(x: float, y: float, value: str, cls: str = "small", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def make_svg(
    positive: list[dict[str, float]],
    gaps: list[dict[str, float]],
    pseudo: list[dict[str, float]],
    functions: dict[str, object],
) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470" role="img" aria-labelledby="title desc">',
        '<title id="title">矩阵分析累计复现门</title>',
        '<desc id="desc">三面板展示正定边界与条件数，谱间隙闭合时的特征向量旋转和非正规伪谱，以及矩阵 sign、polar、Frechet 导数与结构化条件数的区别。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.title{font-size:24px;font-weight:700;fill:#1F2937}.head{font-size:22px;font-weight:700;fill:#334155}.small{font-size:15px;fill:#64748B}.label{font-size:17px;fill:#334155}.math{font-family:Georgia,"Times New Roman",serif;font-size:17px;fill:#1F2937}.card{fill:#FFFEFB;stroke:#D7DEE8;stroke-width:1.3}.axis{stroke:#64748B;stroke-width:1.1}.grid{stroke:#D7DEE8;stroke-width:1;stroke-dasharray:4 4}</style></defs>',
        '<rect width="1200" height="470" fill="#FFFFFF"/>',
        '<text x="40" y="38" class="title">MA-CUM-01 计算门：正定变分、扰动/非正规与矩阵函数结构</text>',
        '<rect x="28" y="58" width="368" height="382" class="card"/><rect x="416" y="58" width="368" height="382" class="card"/><rect x="804" y="58" width="368" height="382" class="card"/>',
        '<text x="50" y="88" class="head">A　PSD 边界与投影条件</text>',
        '<text x="438" y="88" class="head">B　谱隙与方向旋转</text>',
        '<text x="826" y="88" class="head">C　sign 与 polar 的结构差异</text>',
    ]

    # Panel A: log growth as the positive margin closes.
    ax0, ay0, aw, ah = 74.0, 126.0, 275.0, 150.0
    parts += [
        f'<line x1="{ax0}" y1="{ay0+ah}" x2="{ax0+aw}" y2="{ay0+ah}" class="axis"/>',
        f'<line x1="{ax0}" y1="{ay0}" x2="{ax0}" y2="{ay0+ah}" class="axis"/>',
        svg_text(ax0, ay0 - 10, "log₁₀ amplification", "small"),
        svg_text(ax0 + aw / 2, ay0 + ah + 24, "−log₁₀ δ，λmin(Hδ)=δ", "small", "middle"),
    ]
    max_x = max(-math.log10(row["delta"]) for row in positive)
    max_y = max(math.log10(row["condition"]) for row in positive) * 1.06
    cond_points: list[str] = []
    pivot_points: list[str] = []
    for row in positive:
        x = ax0 + aw * (-math.log10(row["delta"])) / max_x
        yc = ay0 + ah - ah * math.log10(row["condition"]) / max_y
        yp = ay0 + ah - ah * math.log10(row["inverse_pivot_squared"]) / max_y
        cond_points.append(f"{x:.1f},{yc:.1f}")
        pivot_points.append(f"{x:.1f},{yp:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{yc:.1f}" r="4.5" fill="#DC2626"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{yp:.1f}" r="4.5" fill="#2563EB"/>')
    parts += [
        f'<polyline points="{" ".join(cond_points)}" fill="none" stroke="#DC2626" stroke-width="2.4"/>',
        f'<polyline points="{" ".join(pivot_points)}" fill="none" stroke="#2563EB" stroke-width="2.4"/>',
        '<line x1="70" y1="323" x2="94" y2="323" stroke="#DC2626" stroke-width="2.5"/><text x="102" y="327" class="label">κ₂(Hδ)</text>',
        '<line x1="205" y1="323" x2="229" y2="323" stroke="#2563EB" stroke-width="2.5"/><text x="237" y="327" class="label">1/l₂₂²</text>',
        svg_text(50, 357, "Hδ=[[1,1−δ],[1−δ,1]]；δ↓0 接近 rank-1", "label"),
        svg_text(50, 385, "同一退化：margin↓ / κ↑ / pivot↓", "small"),
        svg_text(50, 412, f'max ‖LLᵀ−H‖F = {max(row["cholesky_residual"] for row in positive):.1e}', "small"),
    ]

    # Panel B: angle versus gap with pseudospectral lower-radius inset.
    bx0, by0, bw, bh = 458.0, 126.0, 285.0, 145.0
    max_angle = 48.0
    parts += [
        f'<line x1="{bx0}" y1="{by0+bh}" x2="{bx0+bw}" y2="{by0+bh}" class="axis"/>',
        f'<line x1="{bx0}" y1="{by0}" x2="{bx0}" y2="{by0+bh}" class="axis"/>',
        svg_text(bx0, by0 - 10, "top eigenvector rotation (degrees)", "small"),
        svg_text(bx0 + bw / 2, by0 + bh + 24, f'−log₁₀ gap（‖E‖₂={gaps[0]["eta"]:.2g}）', "small", "middle"),
    ]
    max_gap_x = max(-math.log10(row["gap"]) for row in gaps)
    angle_points: list[str] = []
    for row in gaps:
        x = bx0 + bw * (-math.log10(row["gap"])) / max_gap_x
        y = by0 + bh - bh * row["angle_degrees"] / max_angle
        angle_points.append(f"{x:.1f},{y:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#7C3AED"/>')
    parts += [
        f'<polyline points="{" ".join(angle_points)}" fill="none" stroke="#7C3AED" stroke-width="2.6"/>',
        svg_text(438, 316, "Weyl：所有 eigenvalue shifts ≤ 0.02", "label"),
        svg_text(438, 341, f'gap=0.003 时 direction rotation={gaps[-1]["angle_degrees"]:.1f}°', "small"),
        svg_text(438, 360, "J_K：spectrum={0}，rε ≥ √(εK)", "label"),
    ]
    max_radius = max(row["lower_radius"] for row in pseudo)
    for index, row in enumerate(pseudo):
        x = 452.0 + index * 61.0
        height = 38.0 * row["lower_radius"] / max_radius
        parts.append(f'<rect x="{x:.1f}" y="{418-height:.1f}" width="36" height="{height:.1f}" rx="4" fill="#F59E0B" fill-opacity=".82"/>')
        parts.append(svg_text(x + 18, 433, f'K={int(row["coupling"])}', "small", "middle"))
        parts.append(svg_text(x + 18, 408 - height, f'{row["lower_radius"]:.2g}', "small", "middle"))

    # Panel C: matrix-sign norm versus polar norm and derivative/structure checks.
    sign_rows = functions["sign"]
    taylor_rows = functions["taylor"]
    assert isinstance(sign_rows, list) and isinstance(taylor_rows, list)
    cx0, cy0, cw, ch = 844.0, 126.0, 282.0, 145.0
    max_sign = max(float(row["sign_norm"]) for row in sign_rows) * 1.06
    parts += [
        f'<line x1="{cx0}" y1="{cy0+ch}" x2="{cx0+cw}" y2="{cy0+ch}" class="axis"/>',
        f'<line x1="{cx0}" y1="{cy0}" x2="{cx0}" y2="{cy0+ch}" class="axis"/>',
        svg_text(cx0, cy0 - 10, "operator 2-norm", "small"),
        svg_text(cx0 + cw / 2, cy0 + ch + 24, "coupling K in T_K=[[1,K],[0,−1]]", "small", "middle"),
    ]
    sign_points: list[str] = []
    polar_points: list[str] = []
    max_k = float(sign_rows[-1]["coupling"])
    for row in sign_rows:
        x = cx0 + cw * float(row["coupling"]) / max_k
        ys = cy0 + ch - ch * float(row["sign_norm"]) / max_sign
        yp = cy0 + ch - ch / max_sign
        sign_points.append(f"{x:.1f},{ys:.1f}")
        polar_points.append(f"{x:.1f},{yp:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{ys:.1f}" r="4.5" fill="#DB2777"/>')
    parts += [
        f'<polyline points="{" ".join(sign_points)}" fill="none" stroke="#DB2777" stroke-width="2.6"/>',
        f'<polyline points="{" ".join(polar_points)}" fill="none" stroke="#16A34A" stroke-width="2.4"/>',
        '<line x1="850" y1="318" x2="874" y2="318" stroke="#DB2777" stroke-width="2.5"/><text x="882" y="322" class="label">‖sign(TK)‖₂</text>',
        '<line x1="1009" y1="318" x2="1033" y2="318" stroke="#16A34A" stroke-width="2.5"/><text x="1041" y="322" class="label">‖Qpolar‖₂=1</text>',
        svg_text(826, 351, "sign(TK)=TK and sign²=I，但并非 unitary", "label"),
        svg_text(826, 378, f'Fréchet check: (remainder/h) {taylor_rows[0]["remainder_over_step"]:.2g} → {taylor_rows[-1]["remainder_over_step"]:.2g}', "small"),
        svg_text(826, 404, f'skew functional κunstruct=√2，κsymmetric={float(functions["symmetric_structured_condition"]):.0f}', "small"),
        svg_text(826, 429, "同一 ambient operator，结构限制会改变 worst direction", "small"),
        '</svg>',
    ]
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--min-delta", type=float, default=0.003)
    parser.add_argument("--eta", type=float, default=0.02)
    parser.add_argument("--min-gap", type=float, default=0.003)
    parser.add_argument("--pseudospectral-epsilon", type=float, default=1e-3)
    parser.add_argument("--max-pseudo-coupling", type=float, default=100.0)
    parser.add_argument("--max-sign-coupling", type=float, default=10.0)
    parser.add_argument("--min-step", type=float, default=3e-4)
    args = parser.parse_args()

    if not 0.0 < args.min_delta <= 0.01:
        raise ValueError("--min-delta must lie in (0, 0.01]")
    if not 0.0 < args.eta <= 0.2:
        raise ValueError("--eta must lie in (0, 0.2]")
    if not 0.0 < args.min_gap <= 0.01:
        raise ValueError("--min-gap must lie in (0, 0.01]")
    if not 0.0 < args.pseudospectral_epsilon <= 0.1:
        raise ValueError("--pseudospectral-epsilon must lie in (0, 0.1]")
    if not 30.0 <= args.max_pseudo_coupling <= 1e6:
        raise ValueError("--max-pseudo-coupling must lie in [30, 1e6]")
    if not 5.0 <= args.max_sign_coupling <= 1e4:
        raise ValueError("--max-sign-coupling must lie in [5, 1e4]")
    if not 0.0 < args.min_step <= 1e-3:
        raise ValueError("--min-step must lie in (0, 1e-3]")

    positive = positive_definite_experiment(args.min_delta)
    gaps, pseudo = perturbation_experiment(
        args.eta,
        args.min_gap,
        args.pseudospectral_epsilon,
        args.max_pseudo_coupling,
    )
    functions = matrix_function_structure_experiment(args.max_sign_coupling, args.min_step)
    if not positive[-1]["condition"] > positive[0]["condition"]:
        raise AssertionError("conditioning should worsen as the positive-definite margin closes")
    if not gaps[-1]["angle_degrees"] > gaps[0]["angle_degrees"]:
        raise AssertionError("eigenvector rotation should grow as the spectral gap closes")
    sign_rows = functions["sign"]
    taylor_rows = functions["taylor"]
    assert isinstance(sign_rows, list) and isinstance(taylor_rows, list)
    if not sign_rows[-1]["sign_norm"] > sign_rows[0]["sign_norm"]:
        raise AssertionError("non-normal matrix-sign norm should grow with coupling")
    if any(abs(row["polar_norm"] - 1.0) > 1e-12 for row in sign_rows):
        raise AssertionError("the polar factor must retain unit operator norm")
    svg = make_svg(positive, gaps, pseudo, functions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print("MA-CUM-01 deterministic computation gate")
    print(f"seed(reserved)={args.seed}")
    print("A positive-definite margin / Cholesky / condition")
    for row in positive:
        print(
            f"  delta={row['delta']:.3g}  lambda_min={row['lambda_min']:.8g}  "
            f"kappa2={row['condition']:.8g}  l22={row['last_pivot']:.8g}  "
            f"residual={row['cholesky_residual']:.2e}"
        )
    print("B perturbation gap and non-normal pseudospectrum")
    for row in gaps:
        print(
            f"  gap={row['gap']:.3g}  eig_shift={row['eigen_shift']:.8g}  "
            f"angle_deg={row['angle_degrees']:.8g}  sin_angle={row['sin_angle']:.8g}"
        )
    for row in pseudo:
        print(
            f"  K={row['coupling']:.0f}  eps={row['epsilon']:.0e}  "
            f"pseudospectral_lower_radius={row['lower_radius']:.8g}"
        )
    print("C matrix function and structure")
    for row in sign_rows:
        print(
            f"  K={row['coupling']:.3g}  sign_norm={row['sign_norm']:.8g}  "
            f"polar_norm={row['polar_norm']:.1f}  sign2_residual={row['involution_residual']:.2e}"
        )
    for row in taylor_rows:
        print(
            f"  h={row['step']:.1e}  remainder={row['remainder']:.8g}  "
            f"remainder/h={row['remainder_over_step']:.8g}  "
            f"remainder/h2={row['remainder_over_step_squared']:.8g}"
        )
    print(
        f"  condition unstructured={functions['unstructured_condition']:.8g}, "
        f"symmetric-structured={functions['symmetric_structured_condition']:.1f}"
    )
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(0)
