"""Compare loss of orthogonality in classical and modified Gram-Schmidt.

The script uses only the Python standard library. It is deterministic and
writes one self-contained SVG into the vault assets directory.
"""

from __future__ import annotations

from math import log10, sqrt
from pathlib import Path


ORDER = 12
EPSILON_MIN = 1e-8
EPSILON_MAX = 1e-1
STEPS = 141

WIDTH = 1200
HEIGHT = 700
TOP = 120
BOTTOM = 92
LEFT = 86
CURVE_WIDTH = 590
PANEL_HEIGHT = HEIGHT - TOP - BOTTOM
HEAT_SIZE = 190
HEAT_GAP = 28
HEAT_LEFT = 750


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def norm(vector: list[float]) -> float:
    return sqrt(dot(vector, vector))


def matrix_columns(epsilon: float) -> list[list[float]]:
    """Columns of A = 11^T + epsilon I."""
    return [
        [1.0 + (epsilon if row == column else 0.0) for row in range(ORDER)]
        for column in range(ORDER)
    ]


def gram_schmidt(columns: list[list[float]], modified: bool) -> tuple[list[list[float]], list[list[float]]]:
    count = len(columns)
    q_columns: list[list[float]] = []
    upper = [[0.0] * count for _ in range(count)]

    for column_index, source in enumerate(columns):
        residual = source[:]

        if modified:
            for basis_index, basis in enumerate(q_columns):
                coefficient = dot(basis, residual)
                upper[basis_index][column_index] = coefficient
                residual = [
                    value - coefficient * basis[row]
                    for row, value in enumerate(residual)
                ]
        else:
            for basis_index, basis in enumerate(q_columns):
                upper[basis_index][column_index] = dot(basis, source)
            residual = [
                source[row]
                - sum(
                    upper[basis_index][column_index] * q_columns[basis_index][row]
                    for basis_index in range(column_index)
                )
                for row in range(len(source))
            ]

        diagonal = norm(residual)
        if diagonal == 0.0:
            raise ArithmeticError("computed zero residual before the exact rank boundary")
        upper[column_index][column_index] = diagonal
        q_columns.append([value / diagonal for value in residual])

    return q_columns, upper


def orthogonality_error(q_columns: list[list[float]]) -> float:
    count = len(q_columns)
    return sqrt(
        sum(
            (
                dot(q_columns[row], q_columns[column])
                - (1.0 if row == column else 0.0)
            )
            ** 2
            for row in range(count)
            for column in range(count)
        )
    )


def relative_residual(
    columns: list[list[float]],
    q_columns: list[list[float]],
    upper: list[list[float]],
) -> float:
    count = len(columns)
    rows = len(columns[0])
    residual_squared = 0.0
    matrix_squared = 0.0
    for column in range(count):
        for row in range(rows):
            reconstructed = sum(
                q_columns[index][row] * upper[index][column]
                for index in range(count)
            )
            residual_squared += (columns[column][row] - reconstructed) ** 2
            matrix_squared += columns[column][row] ** 2
    return sqrt(residual_squared / matrix_squared)


def condition_number(epsilon: float) -> float:
    """Exact 2-norm condition number of 11^T + epsilon I."""
    return (ORDER + epsilon) / epsilon


def epsilons() -> list[float]:
    high = log10(EPSILON_MAX)
    low = log10(EPSILON_MIN)
    return [10 ** (high + (low - high) * index / (STEPS - 1)) for index in range(STEPS)]


def x_coord(condition: float) -> float:
    lower = log10(condition_number(EPSILON_MAX))
    upper = log10(condition_number(EPSILON_MIN))
    fraction = (log10(condition) - lower) / (upper - lower)
    return LEFT + fraction * CURVE_WIDTH


def y_coord(error: float) -> float:
    lower = -16.0
    upper = 1.0
    clipped = min(10.0, max(1e-16, error))
    fraction = (log10(clipped) - lower) / (upper - lower)
    return TOP + (1.0 - fraction) * PANEL_HEIGHT


def line_path(conditions: list[float], errors: list[float]) -> str:
    points = [
        f"{x_coord(condition):.2f},{y_coord(error):.2f}"
        for condition, error in zip(conditions, errors)
    ]
    return "M " + " L ".join(points)


def error_matrix(q_columns: list[list[float]]) -> list[list[float]]:
    return [
        [
            abs(
                dot(q_columns[row], q_columns[column])
                - (1.0 if row == column else 0.0)
            )
            for column in range(ORDER)
        ]
        for row in range(ORDER)
    ]


def color(error: float) -> str:
    fraction = (log10(max(1e-16, min(1.0, error))) + 16.0) / 16.0
    start = (239, 246, 255)
    end = (190, 24, 93)
    values = [round(start[index] + fraction * (end[index] - start[index])) for index in range(3)]
    return "#" + "".join(f"{value:02x}" for value in values)


def add_heatmap(parts: list[str], matrix: list[list[float]], left: float, title: str) -> None:
    cell = HEAT_SIZE / ORDER
    parts.append(f'<text class="heat-title" x="{left + HEAT_SIZE / 2:.2f}" y="{TOP + 31}" text-anchor="middle">{title}</text>')
    grid_top = TOP + 55
    for row in range(ORDER):
        for column in range(ORDER):
            parts.append(
                f'<rect x="{left + column * cell:.2f}" y="{grid_top + row * cell:.2f}" '
                f'width="{cell + 0.2:.2f}" height="{cell + 0.2:.2f}" fill="{color(matrix[row][column])}"/>'
            )
    parts.append(
        f'<rect x="{left:.2f}" y="{grid_top:.2f}" width="{HEAT_SIZE}" height="{HEAT_SIZE}" fill="none" stroke="#526073"/>'
    )
    parts.append(f'<text class="small" x="{left + HEAT_SIZE / 2:.2f}" y="{grid_top + HEAT_SIZE + 25:.2f}" text-anchor="middle">column index j</text>')
    parts.append(
        f'<text class="small" x="{left - 18:.2f}" y="{grid_top + HEAT_SIZE / 2:.2f}" text-anchor="middle" '
        f'transform="rotate(-90 {left - 18:.2f} {grid_top + HEAT_SIZE / 2:.2f})">column index i</text>'
    )


def build_svg(values: list[float]) -> str:
    conditions: list[float] = []
    classical_errors: list[float] = []
    modified_errors: list[float] = []

    for epsilon in values:
        columns = matrix_columns(epsilon)
        classical_q, _ = gram_schmidt(columns, modified=False)
        modified_q, _ = gram_schmidt(columns, modified=True)
        conditions.append(condition_number(epsilon))
        classical_errors.append(orthogonality_error(classical_q))
        modified_errors.append(orthogonality_error(modified_q))

    selected_epsilon = 1e-7
    selected_columns = matrix_columns(selected_epsilon)
    selected_classical, _ = gram_schmidt(selected_columns, modified=False)
    selected_modified, _ = gram_schmidt(selected_columns, modified=True)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        '<title id="title">Modified Gram-Schmidt preserves orthogonality better on nearly dependent columns</title>',
        '<desc id="description">The left panel shows orthogonality defects as the condition number grows. The right panel compares Gram matrix error heatmaps at epsilon ten to the minus seven.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;fill:#1F2937}.title{font-size:26px;font-weight:650}.subtitle{font-size:16px;fill:#64748B}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.tick{font-size:15px}.legend{font-size:15px}.heat-title{font-size:17px;font-weight:650}.small{font-size:15px;fill:#64748B}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="35" text-anchor="middle">Same QR identity, very different numerical orthogonality</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="59" text-anchor="middle">Aε = 11ᵀ + εI, n = {ORDER}; exact κ₂(Aε) = (n + ε) / ε</text>',
        f'<text class="panel" x="{LEFT + CURVE_WIDTH / 2}" y="92" text-anchor="middle">A. Loss of orthogonality as columns become dependent</text>',
        f'<text class="panel" x="{HEAT_LEFT + HEAT_SIZE + HEAT_GAP / 2}" y="92" text-anchor="middle">B. |QᵀQ − I| at ε = 10⁻⁷</text>',
    ]

    bottom = TOP + PANEL_HEIGHT
    for exponent in (-16, -12, -8, -4, 0):
        y_value = y_coord(10.0**exponent)
        parts.append(f'<line x1="{LEFT}" y1="{y_value:.2f}" x2="{LEFT + CURVE_WIDTH}" y2="{y_value:.2f}" stroke="#dbe3ec"/>')
        parts.append(f'<text class="tick" x="{LEFT - 12}" y="{y_value + 4:.2f}" text-anchor="end">10^{exponent}</text>')

    x_ticks = (1e2, 1e4, 1e6, 1e8)
    for tick in x_ticks:
        x_value = x_coord(tick)
        parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#edf1f5"/>')
        parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom + 25}" text-anchor="middle">10^{round(log10(tick))}</text>')

    parts.extend(
        [
            f'<line x1="{LEFT}" y1="{bottom}" x2="{LEFT + CURVE_WIDTH}" y2="{bottom}" stroke="#3f4b5f" stroke-width="1.5"/>',
            f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{bottom}" stroke="#3f4b5f" stroke-width="1.5"/>',
            f'<text class="axis" x="{LEFT + CURVE_WIDTH / 2}" y="{bottom + 60}" text-anchor="middle">Exact condition number κ₂(Aε), log scale</text>',
            f'<text class="axis" x="{LEFT - 61}" y="{TOP + PANEL_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 {LEFT - 61} {TOP + PANEL_HEIGHT / 2})">Orthogonality defect ||QᵀQ − I||F</text>',
            f'<path d="{line_path(conditions, classical_errors)}" fill="none" stroke="#dc2626" stroke-width="3.2"/>',
            f'<path d="{line_path(conditions, modified_errors)}" fill="none" stroke="#2563eb" stroke-width="3.2"/>',
            f'<rect x="{LEFT + 24}" y="{TOP + 20}" width="224" height="64" rx="7" fill="#ffffff" fill-opacity="0.94" stroke="#ccd6e0"/>',
            f'<line x1="{LEFT + 42}" y1="{TOP + 42}" x2="{LEFT + 74}" y2="{TOP + 42}" stroke="#dc2626" stroke-width="3.2"/>',
            f'<text class="legend" x="{LEFT + 84}" y="{TOP + 47}">Classical Gram–Schmidt</text>',
            f'<line x1="{LEFT + 42}" y1="{TOP + 67}" x2="{LEFT + 74}" y2="{TOP + 67}" stroke="#2563eb" stroke-width="3.2"/>',
            f'<text class="legend" x="{LEFT + 84}" y="{TOP + 72}">Modified Gram–Schmidt</text>',
        ]
    )

    add_heatmap(parts, error_matrix(selected_classical), HEAT_LEFT, "Classical GS")
    add_heatmap(parts, error_matrix(selected_modified), HEAT_LEFT + HEAT_SIZE + HEAT_GAP, "Modified GS")

    legend_left = HEAT_LEFT
    legend_top = TOP + 335
    legend_width = HEAT_SIZE * 2 + HEAT_GAP
    blocks = 64
    for index in range(blocks):
        exponent = -16.0 + 16.0 * index / (blocks - 1)
        parts.append(
            f'<rect x="{legend_left + index * legend_width / blocks:.2f}" y="{legend_top}" '
            f'width="{legend_width / blocks + 0.3:.2f}" height="18" fill="{color(10**exponent)}"/>'
        )
    parts.extend(
        [
            f'<text class="small" x="{legend_left}" y="{legend_top + 39}">10⁻¹⁶</text>',
            f'<text class="small" x="{legend_left + legend_width / 2}" y="{legend_top + 39}" text-anchor="middle">absolute entry error, log color</text>',
            f'<text class="small" x="{legend_left + legend_width}" y="{legend_top + 39}" text-anchor="end">1</text>',
            f'<rect x="{legend_left}" y="{legend_top + 70}" width="{legend_width}" height="74" rx="7" fill="#f8fafc" stroke="#d7e0ea"/>',
            f'<text class="legend" x="{legend_left + 14}" y="{legend_top + 94}">At κ₂ ≈ {condition_number(selected_epsilon):.2e}:</text>',
            f'<text class="legend" x="{legend_left + 14}" y="{legend_top + 117}" fill="#9f1239">CGS defect = {orthogonality_error(selected_classical):.2e}</text>',
            f'<text class="legend" x="{legend_left + 14}" y="{legend_top + 138}" fill="#1d4ed8">MGS defect = {orthogonality_error(selected_modified):.2e}</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    values = epsilons()
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "qr"
        / "plot-gram-schmidt-orthogonality-v2.svg"
    )
    audit_columns = matrix_columns(1e-7)
    audit_classical, audit_classical_r = gram_schmidt(audit_columns, modified=False)
    audit_modified, audit_modified_r = gram_schmidt(audit_columns, modified=True)
    if orthogonality_error(audit_classical) <= 1e-1 or orthogonality_error(audit_modified) >= 1e-6:
        raise RuntimeError("CGS/MGS orthogonality separation audit failed")
    if max(relative_residual(audit_columns, audit_classical, audit_classical_r), relative_residual(audit_columns, audit_modified, audit_modified_r)) >= 1e-12:
        raise RuntimeError("QR reconstruction audit failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(values), encoding="utf-8")

    print(f"saved={output}")
    print("epsilon,condition,cgs_orthogonality,mgs_orthogonality,cgs_residual,mgs_residual")
    for epsilon in (1e-1, 1e-3, 1e-5, 1e-7, 1e-8):
        columns = matrix_columns(epsilon)
        classical_q, classical_r = gram_schmidt(columns, modified=False)
        modified_q, modified_r = gram_schmidt(columns, modified=True)
        print(
            f"{epsilon:.0e},{condition_number(epsilon):.6e},"
            f"{orthogonality_error(classical_q):.6e},"
            f"{orthogonality_error(modified_q):.6e},"
            f"{relative_residual(columns, classical_q, classical_r):.6e},"
            f"{relative_residual(columns, modified_q, modified_r):.6e}"
        )


if __name__ == "__main__":
    main()
