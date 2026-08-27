"""Visualize conditioning and Cholesky pivots near a positive-definite boundary.

The script uses exact formulas and only the Python standard library. It is
deterministic and writes one self-contained SVG into the vault assets folder.
"""

from __future__ import annotations

from math import log10, sqrt
from pathlib import Path


DISTANCE_MIN = 1e-6
DISTANCE_MAX = 1.0
STEPS = 301

WIDTH = 1200
HEIGHT = 700
TOP = 116
BOTTOM = 94
LEFT = 84
RIGHT = 42
GAP = 94
PANEL_WIDTH = (WIDTH - LEFT - RIGHT - GAP) / 2
PANEL_HEIGHT = HEIGHT - TOP - BOTTOM


def condition_number(distance: float) -> float:
    """Condition number of [[1, rho], [rho, 1]], where distance = 1-rho."""
    return (2.0 - distance) / distance


def second_pivot(distance: float) -> float:
    """Second Cholesky diagonal sqrt(1-rho^2)."""
    return sqrt(2.0 * distance - distance * distance)


def distances() -> list[float]:
    low = log10(DISTANCE_MIN)
    high = log10(DISTANCE_MAX)
    return [10 ** (low + (high - low) * index / (STEPS - 1)) for index in range(STEPS)]


def x_coord(distance: float, panel_left: float) -> float:
    fraction = (log10(distance) - log10(DISTANCE_MIN)) / (
        log10(DISTANCE_MAX) - log10(DISTANCE_MIN)
    )
    return panel_left + fraction * PANEL_WIDTH


def log_y_coord(value: float, lower: float, upper: float) -> float:
    fraction = (log10(value) - log10(lower)) / (log10(upper) - log10(lower))
    return TOP + (1.0 - fraction) * PANEL_HEIGHT


def path(values_x: list[float], values_y: list[float], panel_left: float, lower: float, upper: float) -> str:
    points = [
        f"{x_coord(x_value, panel_left):.2f},{log_y_coord(y_value, lower, upper):.2f}"
        for x_value, y_value in zip(values_x, values_y)
    ]
    return "M " + " L ".join(points)


def add_axes(
    parts: list[str],
    panel_left: float,
    lower: float,
    upper: float,
    y_ticks: tuple[float, ...],
    y_label: str,
) -> None:
    bottom = TOP + PANEL_HEIGHT
    for tick in y_ticks:
        y_value = log_y_coord(tick, lower, upper)
        exponent = round(log10(tick))
        label = "1" if exponent == 0 else f"10^{exponent}"
        parts.append(f'<line x1="{panel_left:.2f}" y1="{y_value:.2f}" x2="{panel_left + PANEL_WIDTH:.2f}" y2="{y_value:.2f}" stroke="#dbe3ec"/>')
        parts.append(f'<text class="tick" x="{panel_left - 11:.2f}" y="{y_value + 4:.2f}" text-anchor="end">{label}</text>')

    for exponent in (-6, -4, -2, 0):
        tick = 10.0**exponent
        x_value = x_coord(tick, panel_left)
        label = "1" if exponent == 0 else f"10^{exponent}"
        parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#edf1f5"/>')
        parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom + 25}" text-anchor="middle">{label}</text>')

    parts.extend(
        [
            f'<line x1="{panel_left:.2f}" y1="{bottom}" x2="{panel_left + PANEL_WIDTH:.2f}" y2="{bottom}" stroke="#3f4b5f" stroke-width="1.5"/>',
            f'<line x1="{panel_left:.2f}" y1="{TOP}" x2="{panel_left:.2f}" y2="{bottom}" stroke="#3f4b5f" stroke-width="1.5"/>',
            f'<text class="axis" x="{panel_left + PANEL_WIDTH / 2:.2f}" y="{bottom + 60}" text-anchor="middle">Distance to boundary 1 − ρ (log scale)</text>',
            f'<text class="axis" x="{panel_left - 57:.2f}" y="{TOP + PANEL_HEIGHT / 2:.2f}" text-anchor="middle" transform="rotate(-90 {panel_left - 57:.2f} {TOP + PANEL_HEIGHT / 2:.2f})">{y_label}</text>',
        ]
    )


def build_svg(values: list[float]) -> str:
    left_a = LEFT
    left_b = LEFT + PANEL_WIDTH + GAP
    conditions = [condition_number(value) for value in values]
    pivots = [second_pivot(value) for value in values]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        '<title id="title">Condition number diverges and a Cholesky pivot vanishes at the positive-definite boundary</title>',
        '<desc id="description">For a two by two correlation matrix, the condition number grows while the second Cholesky pivot shrinks as rho approaches one.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;fill:#1F2937}.title{font-size:26px;font-weight:650}.subtitle{font-size:16px;fill:#64748B}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.tick{font-size:15px}.legend{font-size:15px}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="35" text-anchor="middle">Approaching the positive-definite boundary leaves a numerical warning</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="59" text-anchor="middle">Aρ = [[1, ρ], [ρ, 1]],  λ = 1 ± ρ,  L₂₂ = √(1 − ρ²)</text>',
        f'<text class="panel" x="{left_a + PANEL_WIDTH / 2:.2f}" y="91" text-anchor="middle">A. Spectral condition number</text>',
        f'<text class="panel" x="{left_b + PANEL_WIDTH / 2:.2f}" y="91" text-anchor="middle">B. Second Cholesky diagonal</text>',
    ]

    add_axes(parts, left_a, 1.0, 2e6, (1.0, 1e2, 1e4, 1e6), "κ₂(Aρ)")
    add_axes(parts, left_b, 1e-3, 1.0, (1e-3, 1e-2, 1e-1, 1.0), "Cholesky pivot L₂₂")

    parts.extend(
        [
            f'<path d="{path(values, conditions, left_a, 1.0, 2e6)}" fill="none" stroke="#dc2626" stroke-width="3.2"/>',
            f'<path d="{path(values, pivots, left_b, 1e-3, 1.0)}" fill="none" stroke="#2563eb" stroke-width="3.2"/>',
            f'<rect x="{left_a + 164:.2f}" y="{TOP + 25:.2f}" width="220" height="56" rx="7" fill="#ffffff" fill-opacity="0.94" stroke="#ccd6e0"/>',
            f'<text class="legend" x="{left_a + 179:.2f}" y="{TOP + 48:.2f}">κ₂ = (1 + ρ) / (1 − ρ)</text>',
            f'<text class="legend" x="{left_a + 179:.2f}" y="{TOP + 69:.2f}" fill="#9f1239">diverges as ρ → 1</text>',
            f'<rect x="{left_b + 154:.2f}" y="{TOP + 300:.2f}" width="230" height="56" rx="7" fill="#ffffff" fill-opacity="0.94" stroke="#ccd6e0"/>',
            f'<text class="legend" x="{left_b + 169:.2f}" y="{TOP + 323:.2f}">L₂₂ = √[(1 − ρ)(1 + ρ)]</text>',
            f'<text class="legend" x="{left_b + 169:.2f}" y="{TOP + 344:.2f}" fill="#1d4ed8">vanishes as ρ → 1</text>',
            f'<text class="legend" x="{LEFT}" y="{HEIGHT - 19}" fill="#7c3aed">Boundary lies to the left: smaller 1 − ρ means stronger correlation and less independent information.</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    values = distances()
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "cholesky"
        / "plot-cholesky-pivot-condition-v2.svg"
    )
    if abs(condition_number(1.0) - 1.0) > 1e-12 or condition_number(DISTANCE_MIN) <= 1e6:
        raise RuntimeError("positive-definite boundary condition-number audit failed")
    if second_pivot(DISTANCE_MIN) >= 2e-3 or abs(second_pivot(1.0) - 1.0) > 1e-12:
        raise RuntimeError("Cholesky pivot boundary audit failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(values), encoding="utf-8")

    print(f"saved={output}")
    print("rho,distance_to_boundary,condition,second_cholesky_pivot")
    for rho in (0.0, 0.5, 0.9, 0.99, 0.999):
        distance = 1.0 - rho
        print(
            f"{rho:.3f},{distance:.6f},{condition_number(distance):.6f},"
            f"{second_pivot(distance):.6f}"
        )


if __name__ == "__main__":
    main()
