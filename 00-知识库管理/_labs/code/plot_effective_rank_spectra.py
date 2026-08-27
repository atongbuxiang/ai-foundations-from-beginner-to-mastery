"""Compare effective-rank definitions on an exponential singular spectrum.

Only the Python standard library is required. The script is deterministic and writes
one self-contained SVG into the vault assets folder.
"""

from __future__ import annotations

from math import exp, log
from pathlib import Path


DIMENSION = 64
ALPHA_MIN = 0.0
ALPHA_MAX = 0.18
ALPHA_STEPS = 181
ENERGY_TARGET = 0.99

WIDTH = 1200
HEIGHT = 620
LEFT = 92
RIGHT = 45
TOP = 98
BOTTOM = 82
PLOT_WIDTH = WIDTH - LEFT - RIGHT
PLOT_HEIGHT = HEIGHT - TOP - BOTTOM
Y_MAX = 66.0


def effective_ranks(alpha: float) -> tuple[float, float, float, int]:
    """Return stable, entropy, participation, and 99%-energy ranks."""
    singular_values = [exp(-alpha * index) for index in range(DIMENSION)]
    squared = [value * value for value in singular_values]

    stable_rank = sum(squared) / max(squared)

    total = sum(singular_values)
    probabilities = [value / total for value in singular_values]
    entropy_rank = exp(-sum(probability * log(probability) for probability in probabilities))

    participation_rank = total * total / sum(squared)

    total_energy = sum(squared)
    cumulative = 0.0
    threshold_rank = DIMENSION
    for index, value in enumerate(squared, start=1):
        cumulative += value
        if cumulative / total_energy >= ENERGY_TARGET:
            threshold_rank = index
            break

    return stable_rank, entropy_rank, participation_rank, threshold_rank


def x_coord(alpha: float) -> float:
    return LEFT + (alpha - ALPHA_MIN) / (ALPHA_MAX - ALPHA_MIN) * PLOT_WIDTH


def y_coord(value: float) -> float:
    return TOP + (Y_MAX - value) / Y_MAX * PLOT_HEIGHT


def line_path(alphas: list[float], values: list[float]) -> str:
    points = [f"{x_coord(alpha):.2f},{y_coord(value):.2f}" for alpha, value in zip(alphas, values)]
    return "M " + " L ".join(points)


def step_path(alphas: list[float], values: list[float]) -> str:
    commands = [f"M {x_coord(alphas[0]):.2f},{y_coord(values[0]):.2f}"]
    for index in range(1, len(alphas)):
        x_value = x_coord(alphas[index])
        commands.append(f"L {x_value:.2f},{y_coord(values[index - 1]):.2f}")
        commands.append(f"L {x_value:.2f},{y_coord(values[index]):.2f}")
    return " ".join(commands)


def build_svg(alphas: list[float], series: list[tuple[str, str, list[float], bool]]) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img"',
        ' aria-labelledby="title description">',
        '<title id="title">Effective-rank metrics under exponential spectral decay</title>',
        '<desc id="description">Four effective-rank definitions decrease at different rates as a 64-dimensional singular-value spectrum becomes more concentrated.</desc>',
        '<rect width="100%" height="100%" fill="#fffefb"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#1f2937}.title{font-size:27px;font-weight:650}.tick{font-size:15px}.label{font-size:18px}.legend{font-size:16px}.note{font-size:15px;fill:#64748b}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="35" text-anchor="middle">有效秩不是唯一数字：定义决定你在测什么</text>',
        f'<text class="note" x="{WIDTH / 2}" y="66" text-anchor="middle">σᵢ=exp(−α(i−1))，维数 64；横轴增大表示奇异谱更集中</text>',
    ]

    for tick in range(0, 61, 10):
        y_value = y_coord(float(tick))
        parts.append(
            f'<line x1="{LEFT}" y1="{y_value:.2f}" x2="{WIDTH - RIGHT}" y2="{y_value:.2f}" stroke="#dbe2ea" stroke-width="1"/>'
        )
        parts.append(
            f'<text class="tick" x="{LEFT - 12}" y="{y_value + 4:.2f}" text-anchor="end">{tick}</text>'
        )

    for tick_index in range(7):
        alpha = ALPHA_MIN + tick_index * 0.03
        x_value = x_coord(alpha)
        parts.append(
            f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{HEIGHT - BOTTOM}" stroke="#eef2f6" stroke-width="1"/>'
        )
        parts.append(
            f'<text class="tick" x="{x_value:.2f}" y="{HEIGHT - BOTTOM + 25}" text-anchor="middle">{alpha:.2f}</text>'
        )

    parts.extend(
        [
            f'<line x1="{LEFT}" y1="{HEIGHT - BOTTOM}" x2="{WIDTH - RIGHT}" y2="{HEIGHT - BOTTOM}" stroke="#445064" stroke-width="1.5"/>',
            f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{HEIGHT - BOTTOM}" stroke="#445064" stroke-width="1.5"/>',
        ]
    )

    for label, color, values, is_step in series:
        path = step_path(alphas, values) if is_step else line_path(alphas, values)
        parts.append(
            f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
        )

    parts.append(
        f'<text class="label" x="{WIDTH / 2}" y="{HEIGHT - 20}" text-anchor="middle">谱衰减率 α</text>'
    )
    parts.append(
        f'<text class="label" x="22" y="{TOP + PLOT_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 22 {TOP + PLOT_HEIGHT / 2})">有效秩</text>'
    )

    legend_x = LEFT + 690
    legend_y = TOP + 22
    parts.append(
        f'<rect x="{legend_x - 14}" y="{legend_y - 24}" width="352" height="104" rx="8" fill="#ffffff" fill-opacity="0.94" stroke="#cfd8e3"/>'
    )
    for index, (label, color, _, _) in enumerate(series):
        x_offset = 0 if index % 2 == 0 else 176
        y_offset = (index // 2) * 42
        x_value = legend_x + x_offset
        y_value = legend_y + y_offset
        parts.append(
            f'<line x1="{x_value}" y1="{y_value}" x2="{x_value + 28}" y2="{y_value}" stroke="{color}" stroke-width="3"/>'
        )
        parts.append(
            f'<text class="legend" x="{x_value + 36}" y="{y_value + 5}">{label}</text>'
        )

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    alphas = [
        ALPHA_MIN + index * (ALPHA_MAX - ALPHA_MIN) / (ALPHA_STEPS - 1)
        for index in range(ALPHA_STEPS)
    ]
    values = [effective_ranks(alpha) for alpha in alphas]

    stable = [value[0] for value in values]
    entropy = [value[1] for value in values]
    participation = [value[2] for value in values]
    threshold = [float(value[3]) for value in values]
    assert all(series_values[i] >= series_values[i+1] for series_values in (stable, entropy, participation, threshold) for i in range(len(series_values)-1))
    flat = effective_ranks(0.0)
    assert all(abs(value - 64.0) < 1e-12 for value in flat[:3]) and flat[3] == 64
    assert effective_ranks(0.18)[0] < 4.0 and effective_ranks(0.18)[3] <= 13

    series = [
        ("Stable rank", "#2563eb", stable, False),
        ("熵有效秩", "#0f766e", entropy, False),
        ("Participation ratio", "#b7791f", participation, False),
        ("99% 能量秩", "#64748b", threshold, True),
    ]

    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "effective-rank"
        / "plot-effective-rank-exponential-spectrum-v2.svg"
    )
    output.write_text(build_svg(alphas, series), encoding="utf-8")

    print(f"saved={output}")
    print("alpha,stable_rank,entropy_rank,participation_rank,rank_99pct_energy")
    for alpha in (0.00, 0.02, 0.05, 0.10, 0.18):
        stable_rank, entropy_rank, participation_rank, threshold_rank = effective_ranks(alpha)
        print(
            f"{alpha:.2f},{stable_rank:.4f},{entropy_rank:.4f},"
            f"{participation_rank:.4f},{threshold_rank}"
        )


if __name__ == "__main__":
    main()
