"""Plot pivoting and mixed-precision iterative refinement effects.

The script uses only Python's standard library and writes a self-contained SVG.
Panels A/B solve a well-conditioned 2x2 family with and without partial
pivoting. Panel C factors a rotated SPD matrix in simulated float32, computes
residuals/updates in float64, and performs five refinement steps.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from math import cos, log10, sin, sqrt
from pathlib import Path
from struct import pack, unpack


WIDTH = 1440
HEIGHT = 800
TOP = 160
BOTTOM = 126
LEFTS = (86, 545, 1004)
PANEL_WIDTH = 360
PANEL_HEIGHT = HEIGHT - TOP - BOTTOM
Y_MIN = -18.0
Y_MAX = 0.2

RED = "#dc2626"
BLUE = "#2563eb"
GREEN = "#059669"
PURPLE = "#7c3aed"
GRID = "#e5eaf0"
AXIS = "#334155"


def f32(value: float) -> float:
    """Round a Python float to IEEE-like binary32."""
    return unpack("!f", pack("!f", float(value)))[0]


def identity(value: float) -> float:
    return float(value)


def factor_2x2(
    matrix: list[list[float]], rounder, pivot: bool
) -> tuple[float, float, float, float, bool]:
    """Return u00, u01, l10, u11, swapped for a rounded 2x2 LU."""
    a00 = rounder(matrix[0][0])
    a01 = rounder(matrix[0][1])
    a10 = rounder(matrix[1][0])
    a11 = rounder(matrix[1][1])
    swapped = False
    if pivot and abs(a10) > abs(a00):
        a00, a10 = a10, a00
        a01, a11 = a11, a01
        swapped = True
    if a00 == 0.0:
        raise ZeroDivisionError("zero first pivot")
    multiplier = rounder(a10 / a00)
    product = rounder(multiplier * a01)
    u11 = rounder(a11 - product)
    if u11 == 0.0:
        raise ZeroDivisionError("zero second pivot")
    return a00, a01, multiplier, u11, swapped


def solve_factored_2x2(
    factors: tuple[float, float, float, float, bool],
    rhs: list[float],
    rounder,
) -> list[float]:
    u00, u01, multiplier, u11, swapped = factors
    b0, b1 = rhs
    if swapped:
        b0, b1 = b1, b0
    y0 = rounder(b0)
    y1 = rounder(rounder(b1) - rounder(multiplier * y0))
    x1 = rounder(y1 / u11)
    x0 = rounder((y0 - rounder(u01 * x1)) / u00)
    return [x0, x1]


def norm2(vector: list[float]) -> float:
    return sqrt(sum(value * value for value in vector))


def forward_error(computed: list[float], reference: list[float]) -> float:
    difference = [a - b for a, b in zip(computed, reference)]
    return norm2(difference) / norm2(reference)


def componentwise_berr(
    matrix: list[list[float]], rhs: list[float], solution: list[float]
) -> float:
    values: list[float] = []
    for row, b_value in zip(matrix, rhs):
        residual = b_value - sum(a * x for a, x in zip(row, solution))
        scale = abs(b_value) + sum(abs(a) * abs(x) for a, x in zip(row, solution))
        values.append(abs(residual) / scale if scale else (0.0 if residual == 0.0 else 1.0))
    return max(values)


def pivot_family_rows() -> list[dict[str, float]]:
    """Solve [[eps,1],[1,1]] x = [1,2] for eps=10^-k."""
    rows: list[dict[str, float]] = []
    with localcontext() as ctx:
        ctx.prec = 90
        one = Decimal(1)
        two = Decimal(2)
        ten = Decimal(10)
        for exponent in range(1, 19):
            eps_decimal = ten ** (-exponent)
            reference_decimal = [
                one / (one - eps_decimal),
                (one - two * eps_decimal) / (one - eps_decimal),
            ]
            reference = [float(value) for value in reference_decimal]
            eps = 10.0 ** (-exponent)
            matrix = [[eps, 1.0], [1.0, 1.0]]
            rhs = [1.0, 2.0]

            try:
                no_pivot_factors = factor_2x2(matrix, identity, False)
                no_pivot = solve_factored_2x2(no_pivot_factors, rhs, identity)
                no_pivot_forward = forward_error(no_pivot, reference)
                no_pivot_berr = componentwise_berr(matrix, rhs, no_pivot)
            except (ZeroDivisionError, OverflowError):
                no_pivot = [float("nan"), float("nan")]
                no_pivot_forward = 1.0
                no_pivot_berr = 1.0

            pivot_factors = factor_2x2(matrix, identity, True)
            partial = solve_factored_2x2(pivot_factors, rhs, identity)
            rows.append(
                {
                    "x": float(exponent),
                    "eps": eps,
                    "reference0": reference[0],
                    "no_pivot0": no_pivot[0],
                    "partial0": partial[0],
                    "forward_no_pivot": no_pivot_forward,
                    "forward_partial": forward_error(partial, reference),
                    "berr_no_pivot": no_pivot_berr,
                    "berr_partial": componentwise_berr(matrix, rhs, partial),
                }
            )
    return rows


def rotated_spd(condition: float) -> list[list[float]]:
    angle = 0.37
    c = cos(angle)
    s = sin(angle)
    small = 1.0 / condition
    return [
        [c * c + small * s * s, (1.0 - small) * c * s],
        [(1.0 - small) * c * s, s * s + small * c * c],
    ]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(a * x for a, x in zip(row, vector)) for row in matrix]


def refinement_rows() -> list[dict[str, float]]:
    """Factor in f32; compute residual/update in f64 for five steps."""
    rows: list[dict[str, float]] = []
    reference = [1.0, -2.0]
    for exponent in range(1, 11):
        condition = 10.0**exponent
        matrix = rotated_spd(condition)
        rhs = matvec(matrix, reference)
        try:
            factors = factor_2x2(matrix, f32, True)
            initial = solve_factored_2x2(factors, rhs, f32)
            refined = [float(initial[0]), float(initial[1])]
            for _ in range(5):
                ax = matvec(matrix, refined)
                residual = [b - value for b, value in zip(rhs, ax)]
                correction = solve_factored_2x2(factors, residual, f32)
                refined = [x + d for x, d in zip(refined, correction)]
            rows.append(
                {
                    "x": float(exponent),
                    "condition": condition,
                    "initial_forward": forward_error(initial, reference),
                    "refined_forward": forward_error(refined, reference),
                    "initial_berr": componentwise_berr(matrix, rhs, initial),
                    "refined_berr": componentwise_berr(matrix, rhs, refined),
                    "failed": 0.0,
                }
            )
        except (ZeroDivisionError, OverflowError):
            rows.append(
                {
                    "x": float(exponent),
                    "condition": condition,
                    "initial_forward": 1.0,
                    "refined_forward": 1.0,
                    "initial_berr": 1.0,
                    "refined_berr": 1.0,
                    "failed": 1.0,
                }
            )
    return rows


def x_pivot(value: float, panel: int) -> float:
    return LEFTS[panel] + (value - 1.0) / 17.0 * PANEL_WIDTH


def x_refine(value: float) -> float:
    return LEFTS[2] + (value - 1.0) / 9.0 * PANEL_WIDTH


def y(value: float) -> float:
    clipped = max(10.0**Y_MIN, min(10.0**Y_MAX, value))
    ratio = (log10(clipped) - Y_MIN) / (Y_MAX - Y_MIN)
    return TOP + (1.0 - ratio) * PANEL_HEIGHT


def path(rows: list[dict[str, float]], key: str, panel: int) -> str:
    x_fn = (lambda row: x_refine(row["x"])) if panel == 2 else (
        lambda row: x_pivot(row["x"], panel)
    )
    points = [f'{x_fn(row):.2f},{y(row[key]):.2f}' for row in rows]
    return "M " + " L ".join(points)


def markers(rows: list[dict[str, float]], key: str, panel: int, color: str) -> list[str]:
    x_fn = (lambda row: x_refine(row["x"])) if panel == 2 else (
        lambda row: x_pivot(row["x"], panel)
    )
    return [
        f'<circle cx="{x_fn(row):.2f}" cy="{y(row[key]):.2f}" r="3.1" fill="{color}"/>'
        for row in rows
    ]


def build_svg(pivot_rows: list[dict[str, float]], refine_rows: list[dict[str, float]]) -> str:
    bottom = TOP + PANEL_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Partial pivoting and mixed-precision iterative refinement</title>',
        '<desc id="desc">Panels A and B compare forward and componentwise backward errors for a well-conditioned two by two system with and without partial pivoting. Panel C compares a float32 LU initial solution with five float64-residual refinement steps as condition number grows.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;fill:#1F2937}.title{font-size:27px;font-weight:760}.subtitle{font-size:17px;fill:#64748B}.panel{font-size:19px;font-weight:700}.axis{font-size:16px}.tick{font-size:15px;fill:#64748B}.legend{font-size:15px}.callout{font-size:15px;font-weight:650}</style>',
        f'<text class="title" x="{WIDTH/2}" y="38" text-anchor="middle">选主元修复算法失稳；高精度残差在条件允许时修复低精度初解</text>',
        f'<text class="subtitle" x="{WIDTH/2}" y="66" text-anchor="middle">左/中：κ∞→4 的 2×2 家族 · 右：旋转 SPD、float32 LU + 5 次 float64 residual refinement</text>',
        f'<text class="panel" x="{LEFTS[0]+PANEL_WIDTH/2}" y="110" text-anchor="middle">A. 相对前向误差</text>',
        f'<text class="panel" x="{LEFTS[1]+PANEL_WIDTH/2}" y="110" text-anchor="middle">B. componentwise BERR</text>',
        f'<text class="panel" x="{LEFTS[2]+PANEL_WIDTH/2}" y="110" text-anchor="middle">C. 低精度初解与迭代改进</text>',
    ]

    for exponent in (-18, -15, -12, -9, -6, -3, 0):
        y_value = y(10.0**exponent)
        for left in LEFTS:
            parts.append(
                f'<line x1="{left}" y1="{y_value:.2f}" x2="{left+PANEL_WIDTH}" y2="{y_value:.2f}" stroke="{GRID}"/>'
            )
            parts.append(
                f'<text class="tick" x="{left-10}" y="{y_value+4:.2f}" text-anchor="end">10^{exponent}</text>'
            )

    for panel in (0, 1):
        for exponent in (1, 4, 7, 10, 13, 16, 18):
            x_value = x_pivot(float(exponent), panel)
            parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#f1f5f9"/>')
            parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom+23}" text-anchor="middle">{exponent}</text>')

    for exponent in range(1, 11):
        x_value = x_refine(float(exponent))
        parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#f1f5f9"/>')
        parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom+23}" text-anchor="middle">{exponent}</text>')

    for left in LEFTS:
        parts.extend([
            f'<line x1="{left}" y1="{bottom}" x2="{left+PANEL_WIDTH}" y2="{bottom}" stroke="{AXIS}" stroke-width="1.4"/>',
            f'<line x1="{left}" y1="{TOP}" x2="{left}" y2="{bottom}" stroke="{AXIS}" stroke-width="1.4"/>',
        ])

    parts.extend([
        f'<text class="axis" x="{LEFTS[0]+PANEL_WIDTH/2}" y="{bottom+53}" text-anchor="middle">k in ε = 10⁻ᵏ</text>',
        f'<text class="axis" x="{LEFTS[1]+PANEL_WIDTH/2}" y="{bottom+53}" text-anchor="middle">k in ε = 10⁻ᵏ</text>',
        f'<text class="axis" x="{LEFTS[2]+PANEL_WIDTH/2}" y="{bottom+53}" text-anchor="middle">k in κ₂(A) = 10ᵏ</text>',
        f'<path d="{path(pivot_rows, "forward_no_pivot", 0)}" fill="none" stroke="{RED}" stroke-width="3.2"/>',
        f'<path d="{path(pivot_rows, "forward_partial", 0)}" fill="none" stroke="{BLUE}" stroke-width="3.2"/>',
        f'<path d="{path(pivot_rows, "berr_no_pivot", 1)}" fill="none" stroke="{RED}" stroke-width="3.2"/>',
        f'<path d="{path(pivot_rows, "berr_partial", 1)}" fill="none" stroke="{BLUE}" stroke-width="3.2"/>',
        f'<path d="{path(refine_rows, "initial_forward", 2)}" fill="none" stroke="{PURPLE}" stroke-width="3.2"/>',
        f'<path d="{path(refine_rows, "refined_forward", 2)}" fill="none" stroke="{GREEN}" stroke-width="3.2"/>',
    ])
    parts.extend(markers(pivot_rows, "forward_no_pivot", 0, RED))
    parts.extend(markers(pivot_rows, "forward_partial", 0, BLUE))
    parts.extend(markers(pivot_rows, "berr_no_pivot", 1, RED))
    parts.extend(markers(pivot_rows, "berr_partial", 1, BLUE))
    parts.extend(markers(refine_rows, "initial_forward", 2, PURPLE))
    parts.extend(markers(refine_rows, "refined_forward", 2, GREEN))

    legends = (
        (LEFTS[0], ((RED, "无主元"), (BLUE, "部分选主元"))),
        (LEFTS[1], ((RED, "无主元"), (BLUE, "部分选主元"))),
        (LEFTS[2], ((PURPLE, "float32 LU 初解"), (GREEN, "5 次迭代改进"))),
    )
    for left, entries in legends:
        parts.append(f'<rect x="{left+15}" y="{TOP+16}" width="185" height="62" rx="8" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1"/>')
        for index, (color, label) in enumerate(entries):
            yy = TOP + 38 + index * 24
            parts.append(f'<line x1="{left+29}" y1="{yy}" x2="{left+59}" y2="{yy}" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<text class="legend" x="{left+69}" y="{yy+4}">{label}</text>')

    first_bad = next(row for row in pivot_rows if row["forward_no_pivot"] > 0.1)
    first_refine_fail = next((row for row in refine_rows if row["failed"] == 1.0), refine_rows[-1])
    parts.extend([
        f'<rect x="{LEFTS[0]+214}" y="{TOP+18}" width="130" height="58" rx="8" fill="#fff7ed" stroke="#f59e0b"/>',
        f'<text class="callout" x="{LEFTS[0]+279}" y="{TOP+42}" text-anchor="middle">ε=10^-{int(first_bad["x"])} 后失真</text>',
        f'<text class="tick" x="{LEFTS[0]+279}" y="{TOP+62}" text-anchor="middle">但 κ∞ 始终约 4</text>',
        f'<rect x="{LEFTS[2]+214}" y="{TOP+18}" width="130" height="58" rx="8" fill="#ecfdf5" stroke="#10b981"/>',
        f'<text class="callout" x="{LEFTS[2]+279}" y="{TOP+42}" text-anchor="middle">κu₃₂ 接近 1</text>',
        f'<text class="tick" x="{LEFTS[2]+279}" y="{TOP+62}" text-anchor="middle">refinement 开始失效</text>',
        f'<text class="subtitle" x="{WIDTH/2}" y="{HEIGHT-26}" text-anchor="middle">读图：pivoting 处理算法制造的误差；refinement 处理低精度初解，但不能越过低精度因子丢失敏感方向的边界。</text>',
        '</svg>',
    ])
    return "\n".join(parts)


def main() -> None:
    pivot_rows = pivot_family_rows()
    refine_rows = refinement_rows()
    vault_root = Path(__file__).resolve().parents[3]
    output = vault_root / "00-知识库管理" / "_assets" / "plots" / "error-analysis" / "plot-pivoting-refinement-v2.svg"
    if max(row["forward_partial"] for row in pivot_rows) >= 1e-12 or not any(row["forward_no_pivot"] > 0.1 for row in pivot_rows):
        raise RuntimeError("partial-pivoting separation audit failed")
    if refine_rows[5]["refined_forward"] >= refine_rows[5]["initial_forward"] * 1e-6:
        raise RuntimeError("iterative refinement no longer repairs the moderate-condition case")
    if refine_rows[-1]["failed"] != 1.0:
        raise RuntimeError("low-precision factorization failure boundary changed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(pivot_rows, refine_rows), encoding="utf-8")

    print(f"saved={output}")
    print("pivot:k,eps,reference_x1,no_pivot_x1,partial_x1,forward_no_pivot,forward_partial,berr_no_pivot,berr_partial")
    for row in pivot_rows:
        if int(row["x"]) in (1, 4, 7, 8, 10, 13, 16, 18):
            print(
                f'{int(row["x"])},{row["eps"]:.1e},{row["reference0"]:.9e},'
                f'{row["no_pivot0"]:.9e},{row["partial0"]:.9e},'
                f'{row["forward_no_pivot"]:.9e},{row["forward_partial"]:.9e},'
                f'{row["berr_no_pivot"]:.9e},{row["berr_partial"]:.9e}'
            )

    print("refinement:k,condition,initial_forward,refined_forward,initial_berr,refined_berr,failed")
    for row in refine_rows:
        print(
            f'{int(row["x"])},{row["condition"]:.1e},'
            f'{row["initial_forward"]:.9e},{row["refined_forward"]:.9e},'
            f'{row["initial_berr"]:.9e},{row["refined_berr"]:.9e},'
            f'{int(row["failed"])}'
        )


if __name__ == "__main__":
    main()
