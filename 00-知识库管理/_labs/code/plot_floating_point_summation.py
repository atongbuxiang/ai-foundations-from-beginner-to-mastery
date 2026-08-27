"""Demonstrate floating-point absorption, order dependence, and cancellation.

The script uses only the Python standard library. It emulates IEEE binary32
rounding after every arithmetic operation with struct.pack/unpack, uses
Decimal as the high-precision reference for the cancellation panel, and writes
one self-contained SVG into the vault.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from math import log10, sqrt
from pathlib import Path
from struct import pack, unpack


WIDTH = 1240
HEIGHT = 720
TOP = 126
BOTTOM = 108
LEFT_A = 88
LEFT_B = 682
PANEL_WIDTH = 480
PANEL_HEIGHT = HEIGHT - TOP - BOTTOM
SMALL = 2.0 ** -24
ERROR_FLOOR_A = 1e-12
ERROR_FLOOR_B = 1e-18


def f32(value: float) -> float:
    """Round a Python float to IEEE binary32, returning it as a Python float."""
    return unpack(">f", pack(">f", value))[0]


def add32(left: float, right: float) -> float:
    return f32(f32(left) + f32(right))


def sub32(left: float, right: float) -> float:
    return f32(f32(left) - f32(right))


def naive32(values: list[float]) -> float:
    total = f32(0.0)
    for value in values:
        total = add32(total, value)
    return total


def pairwise32(values: list[float]) -> float:
    work = [f32(value) for value in values]
    while len(work) > 1:
        next_level: list[float] = []
        index = 0
        while index + 1 < len(work):
            next_level.append(add32(work[index], work[index + 1]))
            index += 2
        if index < len(work):
            next_level.append(work[index])
        work = next_level
    return work[0] if work else f32(0.0)


def kahan32(values: list[float]) -> float:
    total = f32(0.0)
    compensation = f32(0.0)
    for value in values:
        adjusted = sub32(value, compensation)
        updated = add32(total, adjusted)
        compensation = sub32(sub32(updated, total), adjusted)
        total = updated
    return total


def summation_data() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for exponent in range(0, 19):
        count = 2**exponent
        exact = 1.0 + count * SMALL
        big_first = [1.0] + [SMALL] * count
        small_first = [SMALL] * count + [1.0]
        rows.append(
            {
                "exponent": float(exponent),
                "count": float(count),
                "big_first": abs(naive32(big_first) - exact),
                "small_first": abs(naive32(small_first) - exact),
                "pairwise": abs(pairwise32(big_first) - exact),
                "kahan": abs(kahan32(big_first) - exact),
            }
        )
    return rows


def cancellation_data() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with localcontext() as context:
        context.prec = 90
        for exponent in range(0, 19):
            x_integer = 10**exponent
            x_float = float(x_integer)
            x_decimal = Decimal(x_integer)
            reference = (x_decimal + Decimal(1)).sqrt() - x_decimal.sqrt()
            naive = sqrt(x_float + 1.0) - sqrt(x_float)
            stable = 1.0 / (sqrt(x_float + 1.0) + sqrt(x_float))
            reference_float = float(reference)
            rows.append(
                {
                    "exponent": float(exponent),
                    "x": x_float,
                    "naive": naive,
                    "stable": stable,
                    "reference": reference_float,
                    "naive_error": abs(naive - reference_float) / reference_float,
                    "stable_error": abs(stable - reference_float) / reference_float,
                }
            )
    return rows


def x_a(exponent: float) -> float:
    return LEFT_A + exponent / 18.0 * PANEL_WIDTH


def y_a(error: float) -> float:
    low, high = -12.0, -1.0
    clipped = max(ERROR_FLOOR_A, min(10.0**high, error))
    fraction = (log10(clipped) - low) / (high - low)
    return TOP + (1.0 - fraction) * PANEL_HEIGHT


def x_b(exponent: float) -> float:
    return LEFT_B + exponent / 18.0 * PANEL_WIDTH


def y_b(error: float) -> float:
    low, high = -18.0, 0.0
    clipped = max(ERROR_FLOOR_B, min(1.0, error))
    fraction = (log10(clipped) - low) / (high - low)
    return TOP + (1.0 - fraction) * PANEL_HEIGHT


def path(rows: list[dict[str, float]], x_key: str, y_key: str, panel: str) -> str:
    x_fn = x_a if panel == "a" else x_b
    y_fn = y_a if panel == "a" else y_b
    points = [f"{x_fn(row[x_key]):.2f},{y_fn(row[y_key]):.2f}" for row in rows]
    return "M " + " L ".join(points)


def build_svg(sum_rows: list[dict[str, float]], cancel_rows: list[dict[str, float]]) -> str:
    bottom = TOP + PANEL_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Floating-point summation order and catastrophic cancellation</title>',
        '<desc id="desc">The left panel compares binary32 summation orders and algorithms for one plus repeated half-ulp increments. The right panel compares direct and rationalized evaluation of square root of x plus one minus square root of x.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;fill:#1F2937}.title{font-size:26px;font-weight:700}.subtitle{font-size:16px;fill:#64748B}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.tick{font-size:15px;fill:#64748B}.legend{font-size:15px}.callout{font-size:15px;font-weight:600}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="34" text-anchor="middle">Small local roundings, large structural differences</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="58" text-anchor="middle">Left: IEEE binary32 emulation after every operation · Right: binary64 versus a 90-digit Decimal reference</text>',
        f'<text class="panel" x="{LEFT_A + PANEL_WIDTH / 2}" y="94" text-anchor="middle">A. Summation order and absorption</text>',
        f'<text class="panel" x="{LEFT_B + PANEL_WIDTH / 2}" y="94" text-anchor="middle">B. Catastrophic cancellation and reformulation</text>',
    ]

    for exponent in (-12, -10, -8, -6, -4, -2):
        y_value = y_a(10.0**exponent)
        parts.append(f'<line x1="{LEFT_A}" y1="{y_value:.2f}" x2="{LEFT_A + PANEL_WIDTH}" y2="{y_value:.2f}" stroke="#e5eaf0"/>')
        parts.append(f'<text class="tick" x="{LEFT_A - 12}" y="{y_value + 4:.2f}" text-anchor="end">10^{exponent}</text>')

    for exponent in (-18, -15, -12, -9, -6, -3, 0):
        y_value = y_b(10.0**exponent)
        parts.append(f'<line x1="{LEFT_B}" y1="{y_value:.2f}" x2="{LEFT_B + PANEL_WIDTH}" y2="{y_value:.2f}" stroke="#e5eaf0"/>')
        parts.append(f'<text class="tick" x="{LEFT_B - 12}" y="{y_value + 4:.2f}" text-anchor="end">10^{exponent}</text>')

    for exponent in (0, 3, 6, 9, 12, 15, 18):
        xa = x_a(float(exponent))
        xb = x_b(float(exponent))
        parts.append(f'<line x1="{xa:.2f}" y1="{TOP}" x2="{xa:.2f}" y2="{bottom}" stroke="#f0f3f6"/>')
        parts.append(f'<line x1="{xb:.2f}" y1="{TOP}" x2="{xb:.2f}" y2="{bottom}" stroke="#f0f3f6"/>')
        parts.append(f'<text class="tick" x="{xa:.2f}" y="{bottom + 24}" text-anchor="middle">{exponent}</text>')
        parts.append(f'<text class="tick" x="{xb:.2f}" y="{bottom + 24}" text-anchor="middle">{exponent}</text>')

    parts.extend(
        [
            f'<line x1="{LEFT_A}" y1="{bottom}" x2="{LEFT_A + PANEL_WIDTH}" y2="{bottom}" stroke="#334155" stroke-width="1.5"/>',
            f'<line x1="{LEFT_A}" y1="{TOP}" x2="{LEFT_A}" y2="{bottom}" stroke="#334155" stroke-width="1.5"/>',
            f'<line x1="{LEFT_B}" y1="{bottom}" x2="{LEFT_B + PANEL_WIDTH}" y2="{bottom}" stroke="#334155" stroke-width="1.5"/>',
            f'<line x1="{LEFT_B}" y1="{TOP}" x2="{LEFT_B}" y2="{bottom}" stroke="#334155" stroke-width="1.5"/>',
            f'<text class="axis" x="{LEFT_A + PANEL_WIDTH / 2}" y="{bottom + 56}" text-anchor="middle">k in N = 2ᵏ</text>',
            f'<text class="axis" x="{LEFT_B + PANEL_WIDTH / 2}" y="{bottom + 56}" text-anchor="middle">k in x = 10ᵏ</text>',
            f'<text class="axis" x="{LEFT_A - 62}" y="{TOP + PANEL_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 {LEFT_A - 62} {TOP + PANEL_HEIGHT / 2})">absolute summation error</text>',
            f'<text class="axis" x="{LEFT_B - 62}" y="{TOP + PANEL_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 {LEFT_B - 62} {TOP + PANEL_HEIGHT / 2})">relative evaluation error</text>',
            f'<path d="{path(sum_rows, "exponent", "big_first", "a")}" fill="none" stroke="#dc2626" stroke-width="3.1"/>',
            f'<path d="{path(sum_rows, "exponent", "small_first", "a")}" fill="none" stroke="#2563eb" stroke-width="2.7"/>',
            f'<path d="{path(sum_rows, "exponent", "pairwise", "a")}" fill="none" stroke="#7c3aed" stroke-width="2.7" stroke-dasharray="8 5"/>',
            f'<path d="{path(sum_rows, "exponent", "kahan", "a")}" fill="none" stroke="#059669" stroke-width="2.7" stroke-dasharray="3 4"/>',
            f'<path d="{path(cancel_rows, "exponent", "naive_error", "b")}" fill="none" stroke="#dc2626" stroke-width="3.1"/>',
            f'<path d="{path(cancel_rows, "exponent", "stable_error", "b")}" fill="none" stroke="#059669" stroke-width="3.1"/>',
        ]
    )

    for row in sum_rows:
        parts.append(f'<circle cx="{x_a(row["exponent"]):.2f}" cy="{y_a(row["big_first"]):.2f}" r="2.8" fill="#dc2626"/>')
    for row in cancel_rows:
        parts.append(f'<circle cx="{x_b(row["exponent"]):.2f}" cy="{y_b(row["naive_error"]):.2f}" r="2.8" fill="#dc2626"/>')
        parts.append(f'<circle cx="{x_b(row["exponent"]):.2f}" cy="{y_b(row["stable_error"]):.2f}" r="2.8" fill="#059669"/>')

    parts.extend(
        [
            f'<rect x="{LEFT_A + 16}" y="{TOP + 15}" width="245" height="104" rx="8" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1"/>',
            f'<line x1="{LEFT_A + 30}" y1="{TOP + 36}" x2="{LEFT_A + 62}" y2="{TOP + 36}" stroke="#dc2626" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_A + 72}" y="{TOP + 41}">naive: 1 first</text>',
            f'<line x1="{LEFT_A + 30}" y1="{TOP + 58}" x2="{LEFT_A + 62}" y2="{TOP + 58}" stroke="#2563eb" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_A + 72}" y="{TOP + 63}">naive: small terms first</text>',
            f'<line x1="{LEFT_A + 30}" y1="{TOP + 80}" x2="{LEFT_A + 62}" y2="{TOP + 80}" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 5"/>',
            f'<text class="legend" x="{LEFT_A + 72}" y="{TOP + 85}">pairwise</text>',
            f'<line x1="{LEFT_A + 30}" y1="{TOP + 102}" x2="{LEFT_A + 62}" y2="{TOP + 102}" stroke="#059669" stroke-width="3" stroke-dasharray="3 4"/>',
            f'<text class="legend" x="{LEFT_A + 72}" y="{TOP + 107}">Kahan compensation</text>',
            f'<rect x="{LEFT_B + 16}" y="{TOP + 15}" width="237" height="61" rx="8" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1"/>',
            f'<line x1="{LEFT_B + 30}" y1="{TOP + 36}" x2="{LEFT_B + 62}" y2="{TOP + 36}" stroke="#dc2626" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_B + 72}" y="{TOP + 41}">sqrt(x+1) − sqrt(x)</text>',
            f'<line x1="{LEFT_B + 30}" y1="{TOP + 58}" x2="{LEFT_B + 62}" y2="{TOP + 58}" stroke="#059669" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_B + 72}" y="{TOP + 63}">1 / (sqrt(x+1) + sqrt(x))</text>',
            f'<rect x="{LEFT_A + 274}" y="{TOP + 16}" width="190" height="75" rx="8" fill="#fff7ed" stroke="#f59e0b"/>',
            f'<text class="callout" x="{LEFT_A + 369}" y="{TOP + 40}" text-anchor="middle">increment = 2⁻²⁴</text>',
            f'<text class="tick" x="{LEFT_A + 369}" y="{TOP + 61}" text-anchor="middle">half an ulp at 1 in FP32</text>',
            f'<text class="tick" x="{LEFT_A + 369}" y="{TOP + 80}" text-anchor="middle">repeated additions vanish</text>',
            f'<rect x="{LEFT_B + 276}" y="{TOP + 16}" width="188" height="75" rx="8" fill="#ecfdf5" stroke="#10b981"/>',
            f'<text class="callout" x="{LEFT_B + 370}" y="{TOP + 40}" text-anchor="middle">same mathematical f(x)</text>',
            f'<text class="tick" x="{LEFT_B + 370}" y="{TOP + 61}" text-anchor="middle">different intermediate scale</text>',
            f'<text class="tick" x="{LEFT_B + 370}" y="{TOP + 80}" text-anchor="middle">reformulation is stable</text>',
            f'<text class="subtitle" x="{WIDTH / 2}" y="{HEIGHT - 22}" text-anchor="middle">Zero errors are drawn at the panel floor for visibility; inspect the printed CSV for exact zeros.</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    sum_rows = summation_data()
    cancel_rows = cancellation_data()
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "floating-point"
        / "plot-summation-cancellation-v2.svg"
    )
    if sum_rows[-1]["big_first"] <= 1e-2:
        raise RuntimeError("half-ulp absorption stress test no longer separates summation order")
    if any(row[key] != 0.0 for row in sum_rows[2:] for key in ("small_first", "pairwise", "kahan")):
        raise RuntimeError("stable summation branches changed on the exact-recovery construction")
    cancellation_at_1e16 = next(row for row in cancel_rows if int(row["exponent"]) == 16)
    if cancellation_at_1e16["naive_error"] != 1.0 or cancellation_at_1e16["stable_error"] >= 1e-14:
        raise RuntimeError("catastrophic-cancellation threshold or rationalized branch changed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(sum_rows, cancel_rows), encoding="utf-8")

    print(f"saved={output}")
    print("summation: k,N,big_first_error,small_first_error,pairwise_error,kahan_error")
    for row in sum_rows:
        if int(row["exponent"]) in (0, 4, 8, 12, 16, 18):
            print(
                f'{int(row["exponent"])},{int(row["count"])},'
                f'{row["big_first"]:.9e},{row["small_first"]:.9e},'
                f'{row["pairwise"]:.9e},{row["kahan"]:.9e}'
            )

    print("cancellation: k,x,naive,stable,reference,naive_relative_error,stable_relative_error")
    for row in cancel_rows:
        if int(row["exponent"]) in (0, 4, 8, 12, 15, 16, 18):
            print(
                f'{int(row["exponent"])},{row["x"]:.1e},'
                f'{row["naive"]:.17e},{row["stable"]:.17e},'
                f'{row["reference"]:.17e},{row["naive_error"]:.9e},'
                f'{row["stable_error"]:.9e}'
            )


if __name__ == "__main__":
    main()
