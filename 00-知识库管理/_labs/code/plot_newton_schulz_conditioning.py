"""Visualize how conditioning controls finite-step Newton--Schulz polar accuracy.

The matrix family is A_kappa = diag(1, 1/kappa), normalized by its Frobenius
norm.  Because the Newton--Schulz iteration preserves singular vectors, the
experiment is exact scalar arithmetic on the two singular values.  The script
uses only the Python standard library and writes one deterministic SVG.
"""

from __future__ import annotations

from math import log10, sqrt
from pathlib import Path


KAPPAS = (1, 10, 100, 1000)
COLORS = ("#2563eb", "#64748b", "#b7791f", "#c24135")
MAX_STEPS = 28
FLOOR = 1e-16
TARGET = 1e-8

WIDTH = 1200
HEIGHT = 700
LEFT = 100
RIGHT = 50
TOP = 104
BOTTOM = 100
PLOT_WIDTH = WIDTH - LEFT - RIGHT
PLOT_HEIGHT = HEIGHT - TOP - BOTTOM


def newton_schulz(value: float) -> float:
    """One scalar step corresponding to X <- 1/2 X(3I-X*X)."""
    return 0.5 * value * (3.0 - value * value)


def normalized_singular_values(kappa: float) -> tuple[float, float]:
    scale = sqrt(1.0 + 1.0 / (kappa * kappa))
    return 1.0 / scale, 1.0 / (kappa * scale)


def defects(kappa: float) -> list[float]:
    first, second = normalized_singular_values(kappa)
    values: list[float] = []
    for _ in range(MAX_STEPS + 1):
        values.append(max(abs(first * first - 1.0), abs(second * second - 1.0)))
        first = newton_schulz(first)
        second = newton_schulz(second)
    return values


def x_coord(step: int) -> float:
    return LEFT + step / MAX_STEPS * PLOT_WIDTH


def y_coord(value: float) -> float:
    clipped = min(1.0, max(FLOOR, value))
    fraction = (log10(clipped) - log10(FLOOR)) / (0.0 - log10(FLOOR))
    return TOP + (1.0 - fraction) * PLOT_HEIGHT


def curve_path(values: list[float]) -> str:
    points = [f"{x_coord(step):.2f},{y_coord(value):.2f}" for step, value in enumerate(values)]
    return "M " + " L ".join(points)


def first_step_below(values: list[float], target: float) -> str:
    for step, value in enumerate(values):
        if value < target:
            return str(step)
    return f">{MAX_STEPS}"


def build_svg(series: list[tuple[int, list[float]]]) -> str:
    bottom = TOP + PLOT_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        '<title id="title">Newton--Schulz orthogonality defect for increasingly ill-conditioned matrices</title>',
        '<desc id="description">The spectral orthogonality defect falls rapidly after the smallest singular value enters the local convergence region, but fixed-step accuracy deteriorates as the condition number grows. A rank-deficient matrix remains rank deficient.</desc>',
        '<rect width="100%" height="100%" fill="#fffefb"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#1f2937}.title{font-size:27px;font-weight:650}.subtitle{font-size:15px;fill:#64748b}.axis{font-size:16px;font-weight:600}.tick{font-size:15px;fill:#64748b}.legend{font-size:15px;font-weight:600}.note{font-size:15px;fill:#64748b}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="35" text-anchor="middle">Newton–Schulz 极分解：条件数推迟局部快速收敛</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="66" text-anchor="middle">Aκ=diag(1,1/κ)/||diag(1,1/κ)||F；误差为 ||X*X−I||₂</text>',
        f'<rect x="{LEFT}" y="{TOP}" width="{PLOT_WIDTH}" height="{PLOT_HEIGHT}" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
    ]

    for exponent in (0, -4, -8, -12, -16):
        value = 10.0**exponent
        y_value = y_coord(value)
        label = "1" if exponent == 0 else f"10^{exponent}"
        parts.append(f'<line x1="{LEFT}" y1="{y_value:.2f}" x2="{LEFT + PLOT_WIDTH}" y2="{y_value:.2f}" stroke="#e2e8f0"/>')
        parts.append(f'<text class="tick" x="{LEFT - 12}" y="{y_value + 4:.2f}" text-anchor="end">{label}</text>')

    for step in (0, 5, 10, 15, 20, 25, 28):
        x_value = x_coord(step)
        parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#f1f5f9"/>')
        parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom + 25}" text-anchor="middle">{step}</text>')

    target_y = y_coord(TARGET)
    parts.extend(
        [
            f'<line x1="{LEFT}" y1="{target_y:.2f}" x2="{LEFT + PLOT_WIDTH}" y2="{target_y:.2f}" stroke="#64748b" stroke-width="1.8" stroke-dasharray="7 6"/>',
            f'<text class="note" x="{LEFT + 10}" y="{target_y - 8:.2f}">验收线：10⁻⁸</text>',
            f'<text class="axis" x="{LEFT + PLOT_WIDTH / 2}" y="{bottom + 65}" text-anchor="middle">迭代步 k</text>',
            f'<text class="axis" x="28" y="{TOP + PLOT_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 28 {TOP + PLOT_HEIGHT / 2})">谱范数正交性缺陷（对数刻度）</text>',
        ]
    )

    for (kappa, values), color in zip(series, COLORS):
        parts.append(f'<path d="{curve_path(values)}" fill="none" stroke="{color}" stroke-width="3.2" stroke-linejoin="round"/>')

    rank_deficient = [1.0] * (MAX_STEPS + 1)
    parts.append(f'<path d="{curve_path(rank_deficient)}" fill="none" stroke="#64748b" stroke-width="2.4" stroke-dasharray="8 6"/>')

    legend_x = LEFT + 34
    legend_y = TOP + 34
    parts.append(f'<rect x="{legend_x - 18}" y="{legend_y - 24}" width="286" height="142" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1"/>')
    for index, ((kappa, values), color) in enumerate(zip(series, COLORS)):
        y_value = legend_y + index * 25
        parts.append(f'<line x1="{legend_x}" y1="{y_value}" x2="{legend_x + 32}" y2="{y_value}" stroke="{color}" stroke-width="3.2"/>')
        parts.append(f'<text class="legend" x="{legend_x + 43}" y="{y_value + 4}">κ = {kappa}；达到 10⁻⁸：{first_step_below(values, TARGET)} 步</text>')
    last_y = legend_y + 4 * 25
    parts.append(f'<line x1="{legend_x}" y1="{last_y}" x2="{legend_x + 32}" y2="{last_y}" stroke="#64748b" stroke-width="2.4" stroke-dasharray="8 6"/>')
    parts.append(f'<text class="legend" x="{legend_x + 43}" y="{last_y + 4}">秩亏：缺陷恒为 1</text>')

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    series = [(kappa, defects(float(kappa))) for kappa in KAPPAS]
    hit_steps = [int(first_step_below(values, TARGET)) for _, values in series]
    assert hit_steps == [5, 10, 16, 22]
    assert all(values[-1] < TARGET for _, values in series)
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "polar-decomposition"
        / "plot-newton-schulz-conditioning-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(series), encoding="utf-8")

    print(f"saved={output}")
    print("kappa,initial_defect,defect_after_5_steps,first_step_below_1e-8")
    for kappa, values in series:
        print(f"{kappa},{values[0]:.12e},{values[5]:.12e},{first_step_below(values, TARGET)}")
    print("rank_deficient,1.000000000000e+00,1.000000000000e+00,never")


if __name__ == "__main__":
    main()
