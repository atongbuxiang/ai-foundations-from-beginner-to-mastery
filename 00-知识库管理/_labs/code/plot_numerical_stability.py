"""Compare algebraically equivalent formulas with different stability.

The script uses only the Python standard library.  It writes a self-contained
SVG into the Obsidian vault and prints selected numeric rows for verification.
Panel A/B study the small root of x^2 - 2 B x + 1.  Panel C studies naive and
shifted log-sum-exp for scores (s, 0, -s).
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from math import exp, isfinite, log, log1p, sqrt
from pathlib import Path


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


def quadratic_rows() -> list[dict[str, float]]:
    """Return forward and polynomial backward errors for B=10^k."""
    rows: list[dict[str, float]] = []
    with localcontext() as ctx:
        ctx.prec = 90
        one = Decimal(1)
        for exponent in range(1, 17):
            b_decimal = Decimal(10) ** exponent
            root_decimal = one / (
                b_decimal + (b_decimal * b_decimal - one).sqrt()
            )
            reference = float(root_decimal)

            b = float(10**exponent)
            radical = sqrt(b * b - 1.0)
            naive = b - radical
            stable = 1.0 / (b + radical)

            def forward(value: float) -> float:
                return abs(value - reference) / abs(reference)

            def backward(value: float) -> float:
                residual = value * value - 2.0 * b * value + 1.0
                scale = value * value + 2.0 * b * abs(value) + 1.0
                return abs(residual) / scale

            rows.append(
                {
                    "x": float(exponent),
                    "b": b,
                    "naive": naive,
                    "stable": stable,
                    "reference": reference,
                    "forward_naive": forward(naive),
                    "forward_stable": forward(stable),
                    "backward_naive": backward(naive),
                    "backward_stable": backward(stable),
                }
            )
    return rows


def lse_reference(score: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 90
        s = Decimal(score)
        return s + (Decimal(1) + (-s).exp() + (-2 * s).exp()).ln()


def logsumexp_rows() -> list[dict[str, float]]:
    """Return relative error or a failure marker for scores (s,0,-s)."""
    scores = list(range(0, 701, 50)) + [710, 750, 800, 900, 1000]
    rows: list[dict[str, float]] = []
    for score in scores:
        reference_decimal = lse_reference(score)
        reference = float(reference_decimal)
        stable = score + log1p(exp(-score) + exp(-2 * score))

        try:
            naive = log(exp(score) + 1.0 + exp(-score))
            naive_failed = not isfinite(naive)
        except OverflowError:
            naive = float("nan")
            naive_failed = True

        scale = max(1.0, abs(reference))
        stable_error = abs(stable - reference) / scale
        naive_error = (
            1.0 if naive_failed else abs(naive - reference) / scale
        )
        rows.append(
            {
                "x": float(score),
                "reference": reference,
                "stable": stable,
                "naive": naive,
                "stable_error": stable_error,
                "naive_error": naive_error,
                "naive_failed": 1.0 if naive_failed else 0.0,
            }
        )
    return rows


def x_quadratic(value: float, panel: int) -> float:
    return LEFTS[panel] + (value - 1.0) / 15.0 * PANEL_WIDTH


def x_lse(value: float) -> float:
    return LEFTS[2] + value / 1000.0 * PANEL_WIDTH


def y(value: float) -> float:
    safe = max(10.0**Y_MIN, min(10.0**Y_MAX, value))
    ratio = (log(safe, 10) - Y_MIN) / (Y_MAX - Y_MIN)
    return TOP + (1.0 - ratio) * PANEL_HEIGHT


def path(rows: list[dict[str, float]], key: str, panel: int) -> str:
    x_fn = (lambda row: x_lse(row["x"])) if panel == 2 else (
        lambda row: x_quadratic(row["x"], panel)
    )
    points = [f'{x_fn(row):.2f},{y(row[key]):.2f}' for row in rows]
    return "M " + " L ".join(points)


def markers(
    rows: list[dict[str, float]], key: str, panel: int, color: str
) -> list[str]:
    x_fn = (lambda row: x_lse(row["x"])) if panel == 2 else (
        lambda row: x_quadratic(row["x"], panel)
    )
    return [
        f'<circle cx="{x_fn(row):.2f}" cy="{y(row[key]):.2f}" '
        f'r="3.1" fill="{color}"/>'
        for row in rows
    ]


def build_svg(
    quadratic: list[dict[str, float]], lse: list[dict[str, float]]
) -> str:
    bottom = TOP + PANEL_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Equivalent formulas can have unequal numerical stability</title>',
        '<desc id="desc">Two panels compare naive and stable formulas for a quadratic small root using forward and backward errors. A third panel compares naive and shifted log-sum-exp, marking overflow as unit failure.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;fill:#1F2937}.title{font-size:27px;font-weight:760}.subtitle{font-size:17px;fill:#64748B}.panel{font-size:19px;font-weight:700}.axis{font-size:16px}.tick{font-size:15px;fill:#64748B}.legend{font-size:15px}.callout{font-size:15px;font-weight:650}</style>',
        f'<text class="title" x="{WIDTH/2}" y="38" text-anchor="middle">同一个数学问题，不同执行路径：消去会失真，平移可避开溢出</text>',
        f'<text class="subtitle" x="{WIDTH/2}" y="66" text-anchor="middle">二次方程小根使用 90 位 Decimal 参考；LSE 溢出点按失败误差 1 标记</text>',
        f'<text class="panel" x="{LEFTS[0]+PANEL_WIDTH/2}" y="110" text-anchor="middle">A. 小根相对前向误差</text>',
        f'<text class="panel" x="{LEFTS[1]+PANEL_WIDTH/2}" y="110" text-anchor="middle">B. 归一化多项式后向误差</text>',
        f'<text class="panel" x="{LEFTS[2]+PANEL_WIDTH/2}" y="110" text-anchor="middle">C. log-sum-exp 相对误差 / 溢出</text>',
    ]

    for exponent in (-18, -15, -12, -9, -6, -3, 0):
        y_value = y(10.0**exponent)
        for left in LEFTS:
            parts.append(
                f'<line x1="{left}" y1="{y_value:.2f}" x2="{left+PANEL_WIDTH}" '
                f'y2="{y_value:.2f}" stroke="{GRID}"/>'
            )
            parts.append(
                f'<text class="tick" x="{left-10}" y="{y_value+4:.2f}" '
                f'text-anchor="end">10^{exponent}</text>'
            )

    for panel in (0, 1):
        for exponent in (1, 4, 7, 10, 13, 16):
            x_value = x_quadratic(float(exponent), panel)
            parts.append(
                f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" '
                f'y2="{bottom}" stroke="#f1f5f9"/>'
            )
            parts.append(
                f'<text class="tick" x="{x_value:.2f}" y="{bottom+23}" '
                f'text-anchor="middle">{exponent}</text>'
            )

    for score in (0, 200, 400, 600, 800, 1000):
        x_value = x_lse(float(score))
        parts.append(
            f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" '
            f'y2="{bottom}" stroke="#f1f5f9"/>'
        )
        parts.append(
            f'<text class="tick" x="{x_value:.2f}" y="{bottom+23}" '
            f'text-anchor="middle">{score}</text>'
        )

    for left in LEFTS:
        parts.extend(
            [
                f'<line x1="{left}" y1="{bottom}" x2="{left+PANEL_WIDTH}" y2="{bottom}" stroke="{AXIS}" stroke-width="1.4"/>',
                f'<line x1="{left}" y1="{TOP}" x2="{left}" y2="{bottom}" stroke="{AXIS}" stroke-width="1.4"/>',
            ]
        )

    parts.extend(
        [
            f'<text class="axis" x="{LEFTS[0]+PANEL_WIDTH/2}" y="{bottom+53}" text-anchor="middle">k in B = 10ᵏ</text>',
            f'<text class="axis" x="{LEFTS[1]+PANEL_WIDTH/2}" y="{bottom+53}" text-anchor="middle">k in B = 10ᵏ</text>',
            f'<text class="axis" x="{LEFTS[2]+PANEL_WIDTH/2}" y="{bottom+53}" text-anchor="middle">score s in (s, 0, −s)</text>',
            f'<path d="{path(quadratic, "forward_naive", 0)}" fill="none" stroke="{RED}" stroke-width="3.2"/>',
            f'<path d="{path(quadratic, "forward_stable", 0)}" fill="none" stroke="{BLUE}" stroke-width="3.2"/>',
            f'<path d="{path(quadratic, "backward_naive", 1)}" fill="none" stroke="{RED}" stroke-width="3.2"/>',
            f'<path d="{path(quadratic, "backward_stable", 1)}" fill="none" stroke="{BLUE}" stroke-width="3.2"/>',
            f'<path d="{path(lse, "naive_error", 2)}" fill="none" stroke="{PURPLE}" stroke-width="3.2"/>',
            f'<path d="{path(lse, "stable_error", 2)}" fill="none" stroke="{GREEN}" stroke-width="3.2"/>',
        ]
    )
    parts.extend(markers(quadratic, "forward_naive", 0, RED))
    parts.extend(markers(quadratic, "forward_stable", 0, BLUE))
    parts.extend(markers(quadratic, "backward_naive", 1, RED))
    parts.extend(markers(quadratic, "backward_stable", 1, BLUE))
    parts.extend(markers(lse, "naive_error", 2, PURPLE))
    parts.extend(markers(lse, "stable_error", 2, GREEN))

    legend_data = (
        (LEFTS[0], ((RED, "直接相减"), (BLUE, "根乘积改写"))),
        (LEFTS[1], ((RED, "直接相减"), (BLUE, "根乘积改写"))),
        (LEFTS[2], ((PURPLE, "直接 exponentiate"), (GREEN, "减最大值"))),
    )
    for left, entries in legend_data:
        parts.append(
            f'<rect x="{left+15}" y="{TOP+16}" width="177" height="62" rx="8" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1"/>'
        )
        for index, (color, label) in enumerate(entries):
            yy = TOP + 38 + index * 24
            parts.append(
                f'<line x1="{left+29}" y1="{yy}" x2="{left+59}" y2="{yy}" stroke="{color}" stroke-width="3"/>'
            )
            parts.append(
                f'<text class="legend" x="{left+69}" y="{yy+4}">{label}</text>'
            )

    first_zero = next(row for row in quadratic if row["naive"] == 0.0)
    first_failure = next(row for row in lse if row["naive_failed"] == 1.0)
    parts.extend(
        [
            f'<rect x="{LEFTS[0]+205}" y="{TOP+18}" width="139" height="58" rx="8" fill="#fff7ed" stroke="#f59e0b"/>',
            f'<text class="callout" x="{LEFTS[0]+274}" y="{TOP+42}" text-anchor="middle">B=10^{int(first_zero["x"])} 起直接得到 0</text>',
            f'<text class="tick" x="{LEFTS[0]+274}" y="{TOP+62}" text-anchor="middle">相对误差变为 100%</text>',
            f'<rect x="{LEFTS[2]+205}" y="{TOP+18}" width="139" height="58" rx="8" fill="#fef2f2" stroke="#ef4444"/>',
            f'<text class="callout" x="{LEFTS[2]+274}" y="{TOP+42}" text-anchor="middle">s={int(first_failure["x"])} 起朴素溢出</text>',
            f'<text class="tick" x="{LEFTS[2]+274}" y="{TOP+62}" text-anchor="middle">精确 LSE 仍可表示</text>',
            f'<text class="subtitle" x="{WIDTH/2}" y="{HEIGHT-26}" text-anchor="middle">读图：问题相同，稳定改写同时控制前向/后向误差并避免中间溢出；提高精度只会把失效点向右推。</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    quadratic = quadratic_rows()
    lse = logsumexp_rows()
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "error-analysis"
        / "plot-numerical-stability-formulas-v2.svg"
    )
    first_zero = next(row for row in quadratic if row["naive"] == 0.0)
    first_overflow = next(row for row in lse if row["naive_failed"] == 1.0)
    if int(first_zero["x"]) != 8 or max(row["forward_stable"] for row in quadratic) >= 1e-14:
        raise RuntimeError("quadratic cancellation threshold or stable branch changed")
    if int(first_overflow["x"]) != 710 or max(row["stable_error"] for row in lse) >= 1e-12:
        raise RuntimeError("log-sum-exp overflow threshold or shifted branch changed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(quadratic, lse), encoding="utf-8")

    print(f"saved={output}")
    print("quadratic:k,B,reference,naive,stable,forward_naive,forward_stable,backward_naive,backward_stable")
    for row in quadratic:
        if int(row["x"]) in (1, 4, 7, 8, 10, 13, 16):
            print(
                f'{int(row["x"])},{row["b"]:.1e},{row["reference"]:.9e},'
                f'{row["naive"]:.9e},{row["stable"]:.9e},'
                f'{row["forward_naive"]:.9e},{row["forward_stable"]:.9e},'
                f'{row["backward_naive"]:.9e},{row["backward_stable"]:.9e}'
            )

    print("logsumexp:score,reference,naive,stable,naive_error,stable_error,naive_failed")
    for row in lse:
        if int(row["x"]) in (0, 100, 500, 700, 710, 800, 1000):
            print(
                f'{int(row["x"])},{row["reference"]:.17g},'
                f'{row["naive"]:.17g},{row["stable"]:.17g},'
                f'{row["naive_error"]:.9e},{row["stable_error"]:.9e},'
                f'{int(row["naive_failed"])}'
            )


if __name__ == "__main__":
    main()
