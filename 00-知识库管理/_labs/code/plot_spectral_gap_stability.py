"""Visualize eigenvalue and eigenvector sensitivity in a symmetric 2x2 model.

The script uses only the Python standard library. It is deterministic and writes
one self-contained SVG into the vault's assets folder.
"""

from __future__ import annotations

from math import asin, atan2, degrees, log10, sqrt
from pathlib import Path


RATIO_MIN = 0.1
RATIO_MAX = 1000.0
RATIO_STEPS = 321

WIDTH = 1200
HEIGHT = 700
TOP = 112
BOTTOM = 92
LEFT = 82
RIGHT = 42
GAP = 92
PANEL_WIDTH = (WIDTH - LEFT - RIGHT - GAP) / 2
PANEL_HEIGHT = HEIGHT - TOP - BOTTOM


def actual_angle_deg(gap_to_noise: float) -> float:
    """Principal-eigenvector rotation for [[1+δ, ε], [ε, 1]]."""
    return degrees(0.5 * atan2(2.0, gap_to_noise))


def angle_bound_deg(gap_to_noise: float) -> float:
    """A coarse sin-theta-style angle bound based on ε/δ."""
    return degrees(asin(min(1.0, 1.0 / gap_to_noise)))


def normalized_eigenvalue_shift(gap_to_noise: float) -> float:
    """Maximum eigenvalue displacement divided by perturbation norm ε."""
    return (sqrt(gap_to_noise * gap_to_noise + 4.0) - gap_to_noise) / 2.0


def ratios() -> list[float]:
    low = log10(RATIO_MIN)
    high = log10(RATIO_MAX)
    return [10 ** (low + (high - low) * index / (RATIO_STEPS - 1)) for index in range(RATIO_STEPS)]


def x_coord(value: float, panel_left: float) -> float:
    fraction = (log10(value) - log10(RATIO_MIN)) / (log10(RATIO_MAX) - log10(RATIO_MIN))
    return panel_left + fraction * PANEL_WIDTH


def y_coord(value: float, maximum: float) -> float:
    return TOP + (maximum - value) / maximum * PANEL_HEIGHT


def line_path(values_x: list[float], values_y: list[float], panel_left: float, y_max: float) -> str:
    points = [
        f"{x_coord(x_value, panel_left):.2f},{y_coord(y_value, y_max):.2f}"
        for x_value, y_value in zip(values_x, values_y)
    ]
    return "M " + " L ".join(points)


def axes(parts: list[str], panel_left: float, y_max: float, y_ticks: list[float], y_label: str) -> None:
    bottom = TOP + PANEL_HEIGHT
    for tick in y_ticks:
        y_value = y_coord(tick, y_max)
        parts.append(
            f'<line x1="{panel_left:.2f}" y1="{y_value:.2f}" x2="{panel_left + PANEL_WIDTH:.2f}" y2="{y_value:.2f}" stroke="#dbe3ec"/>'
        )
        parts.append(
            f'<text class="tick" x="{panel_left - 11:.2f}" y="{y_value + 4:.2f}" text-anchor="end">{tick:g}</text>'
        )

    for tick in (0.1, 1.0, 10.0, 100.0, 1000.0):
        x_value = x_coord(tick, panel_left)
        parts.append(
            f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#edf1f5"/>'
        )
        parts.append(
            f'<text class="tick" x="{x_value:.2f}" y="{bottom + 25}" text-anchor="middle">{tick:g}</text>'
        )

    parts.extend(
        [
            f'<line x1="{panel_left:.2f}" y1="{bottom}" x2="{panel_left + PANEL_WIDTH:.2f}" y2="{bottom}" stroke="#3f4b5f" stroke-width="1.5"/>',
            f'<line x1="{panel_left:.2f}" y1="{TOP}" x2="{panel_left:.2f}" y2="{bottom}" stroke="#3f4b5f" stroke-width="1.5"/>',
            f'<text class="axis" x="{panel_left + PANEL_WIDTH / 2:.2f}" y="{bottom + 60}" text-anchor="middle">谱间隙 / 扰动 δ/ε（对数）</text>',
            f'<text class="axis" x="{panel_left - 55:.2f}" y="{TOP + PANEL_HEIGHT / 2:.2f}" text-anchor="middle" transform="rotate(-90 {panel_left - 55:.2f} {TOP + PANEL_HEIGHT / 2:.2f})">{y_label}</text>',
        ]
    )


def build_svg(values_x: list[float]) -> str:
    left_a = LEFT
    left_b = LEFT + PANEL_WIDTH + GAP
    actual_angles = [actual_angle_deg(value) for value in values_x]
    bound_angles = [angle_bound_deg(value) for value in values_x]
    shifts = [normalized_eigenvalue_shift(value) for value in values_x]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        '<title id="title">Spectral values can be stable while eigenvectors rotate</title>',
        '<desc id="description">A two-panel plot for a symmetric two-by-two matrix. Eigenvalue displacement remains below the perturbation norm, while the leading eigenvector rotates sharply when the spectral gap is comparable to noise.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#1f2937}.title{font-size:27px;font-weight:650}.subtitle{font-size:15px;fill:#64748b}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.tick{font-size:15px}.legend{font-size:15px}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="35" text-anchor="middle">谱值受扰动范数控制，特征向量还需要谱间隙</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="62" text-anchor="middle">Aδ=diag(1+δ,1)，Eε=[[0,ε],[ε,0]]，||Eε||₂=ε</text>',
        f'<text class="panel" x="{left_a + PANEL_WIDTH / 2:.2f}" y="91" text-anchor="middle">A 主特征向量旋转</text>',
        f'<text class="panel" x="{left_b + PANEL_WIDTH / 2:.2f}" y="91" text-anchor="middle">B 最大特征值位移</text>',
    ]

    axes(parts, left_a, 90.0, [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0], "旋转角 θ（度）")
    axes(parts, left_b, 1.05, [0.0, 0.25, 0.5, 0.75, 1.0], "位移 / ε")

    parts.extend(
        [
            f'<path d="{line_path(values_x, actual_angles, left_a, 90.0)}" fill="none" stroke="#2563eb" stroke-width="3.2" stroke-linecap="round"/>',
            f'<path d="{line_path(values_x, bound_angles, left_a, 90.0)}" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="8 6"/>',
            f'<path d="{line_path(values_x, shifts, left_b, 1.05)}" fill="none" stroke="#059669" stroke-width="3.2" stroke-linecap="round"/>',
            f'<line x1="{left_b:.2f}" y1="{y_coord(1.0, 1.05):.2f}" x2="{left_b + PANEL_WIDTH:.2f}" y2="{y_coord(1.0, 1.05):.2f}" stroke="#7c3aed" stroke-width="2.5" stroke-dasharray="8 6"/>',
        ]
    )

    marker_x = x_coord(1.0, left_a)
    parts.extend(
        [
            f'<line x1="{marker_x:.2f}" y1="{TOP}" x2="{marker_x:.2f}" y2="{TOP + PANEL_HEIGHT}" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="3 5"/>',
            f'<text class="legend" x="{marker_x + 7:.2f}" y="{TOP + 22}" fill="#9a6700">间隙 = 扰动</text>',
            f'<rect x="{left_a + 194:.2f}" y="{TOP + 18:.2f}" width="210" height="62" rx="7" fill="#ffffff" fill-opacity="0.94" stroke="#ccd6e0"/>',
            f'<line x1="{left_a + 210:.2f}" y1="{TOP + 39:.2f}" x2="{left_a + 239:.2f}" y2="{TOP + 39:.2f}" stroke="#2563eb" stroke-width="3.2"/>',
            f'<text class="legend" x="{left_a + 248:.2f}" y="{TOP + 44:.2f}">精确旋转角 θ</text>',
            f'<line x1="{left_a + 210:.2f}" y1="{TOP + 64:.2f}" x2="{left_a + 239:.2f}" y2="{TOP + 64:.2f}" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="8 6"/>',
            f'<text class="legend" x="{left_a + 248:.2f}" y="{TOP + 69:.2f}">sin-θ 型上界</text>',
            f'<rect x="{left_b + 184:.2f}" y="{TOP + 18:.2f}" width="220" height="62" rx="7" fill="#ffffff" fill-opacity="0.94" stroke="#ccd6e0"/>',
            f'<line x1="{left_b + 200:.2f}" y1="{TOP + 39:.2f}" x2="{left_b + 229:.2f}" y2="{TOP + 39:.2f}" stroke="#059669" stroke-width="3.2"/>',
            f'<text class="legend" x="{left_b + 238:.2f}" y="{TOP + 44:.2f}">精确位移 / ε</text>',
            f'<line x1="{left_b + 200:.2f}" y1="{TOP + 64:.2f}" x2="{left_b + 229:.2f}" y2="{TOP + 64:.2f}" stroke="#7c3aed" stroke-width="2.5" stroke-dasharray="8 6"/>',
            f'<text class="legend" x="{left_b + 238:.2f}" y="{TOP + 69:.2f}">Weyl 上界 = 1</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    values_x = ratios()
    assert max(normalized_eigenvalue_shift(value) for value in values_x) <= 1.0 + 1e-12
    assert actual_angle_deg(0.1) > 40.0 and actual_angle_deg(1000.0) < 0.1
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "perturbation"
        / "plot-spectral-gap-eigenvector-stability-v2.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(values_x), encoding="utf-8")

    print(f"saved={output}")
    print("gap_to_noise,angle_deg,sin_theta_bound_deg,max_eigenvalue_shift_over_epsilon")
    for ratio in (0.1, 1.0, 10.0, 100.0, 1000.0):
        print(
            f"{ratio:.1f},{actual_angle_deg(ratio):.4f},"
            f"{angle_bound_deg(ratio):.4f},{normalized_eigenvalue_shift(ratio):.4f}"
        )


if __name__ == "__main__":
    main()
