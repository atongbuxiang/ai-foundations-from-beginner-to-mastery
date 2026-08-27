"""Plot how conditioning and scaling separate residual from forward error.

The script uses only the Python standard library and writes a self-contained
SVG into the Obsidian vault. Panel A uses a nearly singular symmetric 2x2
family. Panel B uses a diagonally scaled family to compare normwise and
componentwise right-hand-side backward errors.
"""

from __future__ import annotations

from math import log10, sqrt
from pathlib import Path


WIDTH = 1280
HEIGHT = 760
TOP = 142
BOTTOM = 118
LEFT_A = 96
LEFT_B = 698
PANEL_WIDTH = 488
PANEL_HEIGHT = HEIGHT - TOP - BOTTOM
Y_MIN = -14.0
Y_MAX = 0.2
T = 0.5


def near_singular_data() -> list[dict[str, float]]:
    """Return exact metrics for A_eps=[[1,1],[1,1+eps]]."""
    rows: list[dict[str, float]] = []
    for exponent in range(1, 13):
        eps = 10.0 ** (-exponent)
        # A_eps is SPD. Compute lambda_min via det/lambda_max to avoid
        # cancellation in (trace - sqrt(trace**2 - 4*det))/2.
        trace = 2.0 + eps
        discriminant = sqrt(4.0 + eps * eps)
        lambda_max = 0.5 * (trace + discriminant)
        lambda_min = eps / lambda_max
        condition = lambda_max / lambda_min
        b_norm = sqrt(2.0**2 + (2.0 + eps) ** 2)
        relative_residual = abs(T * eps) / b_norm
        forward_error = abs(T)
        rows.append(
            {
                "exponent": float(exponent),
                "epsilon": eps,
                "condition": condition,
                "forward": forward_error,
                "residual": relative_residual,
                "conditioned": condition * relative_residual,
            }
        )
    return rows


def scaled_component_data() -> list[dict[str, float]]:
    """Return metrics for diag(1,alpha), x=(1,1), xhat=(1,2)."""
    rows: list[dict[str, float]] = []
    for exponent in range(0, 13):
        alpha = 10.0 ** (-exponent)
        relative_residual = alpha / sqrt(1.0 + alpha * alpha)
        condition = 1.0 / alpha
        rows.append(
            {
                "exponent": float(exponent),
                "alpha": alpha,
                "condition": condition,
                "forward": 1.0 / sqrt(2.0),
                "normwise_rhs": relative_residual,
                "componentwise_rhs": 1.0,
                "conditioned": condition * relative_residual,
            }
        )
    return rows


def x_a(exponent: float) -> float:
    return LEFT_A + (exponent - 1.0) / 11.0 * PANEL_WIDTH


def x_b(exponent: float) -> float:
    return LEFT_B + exponent / 12.0 * PANEL_WIDTH


def y(value: float) -> float:
    clipped = max(10.0**Y_MIN, min(10.0**Y_MAX, value))
    fraction = (log10(clipped) - Y_MIN) / (Y_MAX - Y_MIN)
    return TOP + (1.0 - fraction) * PANEL_HEIGHT


def path(
    rows: list[dict[str, float]], y_key: str, panel: str
) -> str:
    x_fn = x_a if panel == "a" else x_b
    points = [f'{x_fn(row["exponent"]):.2f},{y(row[y_key]):.2f}' for row in rows]
    return "M " + " L ".join(points)


def circles(
    rows: list[dict[str, float]], y_key: str, panel: str, color: str
) -> list[str]:
    x_fn = x_a if panel == "a" else x_b
    return [
        f'<circle cx="{x_fn(row["exponent"]):.2f}" '
        f'cy="{y(row[y_key]):.2f}" r="3.2" fill="{color}"/>'
        for row in rows
    ]


def build_svg(
    near_rows: list[dict[str, float]], scale_rows: list[dict[str, float]]
) -> str:
    bottom = TOP + PANEL_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Small residual, large forward error, and hidden componentwise error</title>',
        '<desc id="desc">Panel A shows a fixed forward error with a vanishing relative residual in a nearly singular two by two system. Panel B shows that normwise residual can vanish while one small right-hand-side component has one hundred percent relative backward error.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;fill:#1F2937}.title{font-size:26px;font-weight:760}.subtitle{font-size:16px;fill:#64748B}.panel{font-size:19px;font-weight:700}.axis{font-size:16px}.tick{font-size:15px;fill:#64748B}.legend{font-size:15px}.callout{font-size:15px;font-weight:650}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="38" text-anchor="middle">残差小，不等于答案近；范数小，不等于每个分量都好</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="65" text-anchor="middle">两个解析 2×2 家族 · 所有曲线由闭式公式生成，无随机数</text>',
        f'<text class="panel" x="{LEFT_A + PANEL_WIDTH / 2}" y="104" text-anchor="middle">A. 病态方向：相对残差趋零，前向误差保持 50%</text>',
        f'<text class="panel" x="{LEFT_B + PANEL_WIDTH / 2}" y="104" text-anchor="middle">B. 尺度失衡：范数型趋零，第二分量仍错 100%</text>',
    ]

    for exponent in (-14, -12, -10, -8, -6, -4, -2, 0):
        y_value = y(10.0**exponent)
        for left in (LEFT_A, LEFT_B):
            parts.append(
                f'<line x1="{left}" y1="{y_value:.2f}" '
                f'x2="{left + PANEL_WIDTH}" y2="{y_value:.2f}" stroke="#e5eaf0"/>'
            )
        parts.append(
            f'<text class="tick" x="{LEFT_A - 12}" y="{y_value + 4:.2f}" '
            f'text-anchor="end">10^{exponent}</text>'
        )
        parts.append(
            f'<text class="tick" x="{LEFT_B - 12}" y="{y_value + 4:.2f}" '
            f'text-anchor="end">10^{exponent}</text>'
        )

    for exponent in (1, 3, 5, 7, 9, 11, 12):
        x_value = x_a(float(exponent))
        parts.append(
            f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" '
            f'y2="{bottom}" stroke="#f1f5f9"/>'
        )
        parts.append(
            f'<text class="tick" x="{x_value:.2f}" y="{bottom + 24}" '
            f'text-anchor="middle">{exponent}</text>'
        )

    for exponent in (0, 2, 4, 6, 8, 10, 12):
        x_value = x_b(float(exponent))
        parts.append(
            f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" '
            f'y2="{bottom}" stroke="#f1f5f9"/>'
        )
        parts.append(
            f'<text class="tick" x="{x_value:.2f}" y="{bottom + 24}" '
            f'text-anchor="middle">{exponent}</text>'
        )

    for left in (LEFT_A, LEFT_B):
        parts.extend(
            [
                f'<line x1="{left}" y1="{bottom}" x2="{left + PANEL_WIDTH}" y2="{bottom}" stroke="#334155" stroke-width="1.5"/>',
                f'<line x1="{left}" y1="{TOP}" x2="{left}" y2="{bottom}" stroke="#334155" stroke-width="1.5"/>',
            ]
        )

    parts.extend(
        [
            f'<text class="axis" x="{LEFT_A + PANEL_WIDTH / 2}" y="{bottom + 56}" text-anchor="middle">k in ε = 10⁻ᵏ</text>',
            f'<text class="axis" x="{LEFT_B + PANEL_WIDTH / 2}" y="{bottom + 56}" text-anchor="middle">k in α = 10⁻ᵏ</text>',
            f'<text class="axis" x="{LEFT_A - 66}" y="{TOP + PANEL_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 {LEFT_A - 66} {TOP + PANEL_HEIGHT / 2})">relative quantity</text>',
            f'<text class="axis" x="{LEFT_B - 66}" y="{TOP + PANEL_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 {LEFT_B - 66} {TOP + PANEL_HEIGHT / 2})">relative quantity</text>',
            f'<path d="{path(near_rows, "forward", "a")}" fill="none" stroke="#dc2626" stroke-width="3.2"/>',
            f'<path d="{path(near_rows, "residual", "a")}" fill="none" stroke="#2563eb" stroke-width="3.2"/>',
            f'<path d="{path(near_rows, "conditioned", "a")}" fill="none" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 5"/>',
            f'<path d="{path(scale_rows, "forward", "b")}" fill="none" stroke="#dc2626" stroke-width="3.2"/>',
            f'<path d="{path(scale_rows, "normwise_rhs", "b")}" fill="none" stroke="#2563eb" stroke-width="3.2"/>',
            f'<path d="{path(scale_rows, "componentwise_rhs", "b")}" fill="none" stroke="#059669" stroke-width="3" stroke-dasharray="3 4"/>',
            f'<path d="{path(scale_rows, "conditioned", "b")}" fill="none" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 5"/>',
        ]
    )

    parts.extend(circles(near_rows, "residual", "a", "#2563eb"))
    parts.extend(circles(scale_rows, "normwise_rhs", "b", "#2563eb"))

    parts.extend(
        [
            f'<rect x="{LEFT_A + 18}" y="{TOP + 17}" width="228" height="82" rx="9" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1"/>',
            f'<line x1="{LEFT_A + 32}" y1="{TOP + 39}" x2="{LEFT_A + 64}" y2="{TOP + 39}" stroke="#dc2626" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_A + 74}" y="{TOP + 44}">forward error</text>',
            f'<line x1="{LEFT_A + 32}" y1="{TOP + 61}" x2="{LEFT_A + 64}" y2="{TOP + 61}" stroke="#2563eb" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_A + 74}" y="{TOP + 66}">relative residual = η_b</text>',
            f'<line x1="{LEFT_A + 32}" y1="{TOP + 83}" x2="{LEFT_A + 64}" y2="{TOP + 83}" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 5"/>',
            f'<text class="legend" x="{LEFT_A + 74}" y="{TOP + 88}">κ₂(A) × relative residual</text>',
            f'<rect x="{LEFT_B + 18}" y="{TOP + 17}" width="252" height="104" rx="9" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1"/>',
            f'<line x1="{LEFT_B + 32}" y1="{TOP + 39}" x2="{LEFT_B + 64}" y2="{TOP + 39}" stroke="#dc2626" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_B + 74}" y="{TOP + 44}">forward error</text>',
            f'<line x1="{LEFT_B + 32}" y1="{TOP + 61}" x2="{LEFT_B + 64}" y2="{TOP + 61}" stroke="#2563eb" stroke-width="3"/>',
            f'<text class="legend" x="{LEFT_B + 74}" y="{TOP + 66}">normwise RHS η_b</text>',
            f'<line x1="{LEFT_B + 32}" y1="{TOP + 83}" x2="{LEFT_B + 64}" y2="{TOP + 83}" stroke="#059669" stroke-width="3" stroke-dasharray="3 4"/>',
            f'<text class="legend" x="{LEFT_B + 74}" y="{TOP + 88}">componentwise RHS η_b,comp</text>',
            f'<line x1="{LEFT_B + 32}" y1="{TOP + 105}" x2="{LEFT_B + 64}" y2="{TOP + 105}" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 5"/>',
            f'<text class="legend" x="{LEFT_B + 74}" y="{TOP + 110}">κ₂(A) × normwise η_b</text>',
            f'<rect x="{LEFT_A + 277}" y="{TOP + 19}" width="192" height="76" rx="9" fill="#fff7ed" stroke="#f59e0b"/>',
            f'<text class="callout" x="{LEFT_A + 373}" y="{TOP + 43}" text-anchor="middle">误差沿近零空间方向</text>',
            f'<text class="tick" x="{LEFT_A + 373}" y="{TOP + 65}" text-anchor="middle">A 把大解误差压成小残差</text>',
            f'<text class="tick" x="{LEFT_A + 373}" y="{TOP + 85}" text-anchor="middle">κ 恢复了被隐藏的放大</text>',
            f'<rect x="{LEFT_B + 292}" y="{TOP + 19}" width="177" height="98" rx="9" fill="#ecfdf5" stroke="#10b981"/>',
            f'<text class="callout" x="{LEFT_B + 380}" y="{TOP + 43}" text-anchor="middle">小分量仍有独立意义</text>',
            f'<text class="tick" x="{LEFT_B + 380}" y="{TOP + 65}" text-anchor="middle">总体范数由第 1 分量主导</text>',
            f'<text class="tick" x="{LEFT_B + 380}" y="{TOP + 85}" text-anchor="middle">第 2 个 RHS 却改变 100%</text>',
            f'<text class="tick" x="{LEFT_B + 380}" y="{TOP + 105}" text-anchor="middle">需补充分量型指标</text>',
            f'<text class="subtitle" x="{WIDTH / 2}" y="{HEIGHT - 24}" text-anchor="middle">结论：残差必须尺度化；后向误差必须匹配扰动模型；前向解释必须乘上条件性。</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    near_rows = near_singular_data()
    scale_rows = scaled_component_data()
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "error-analysis"
        / "plot-forward-backward-conditioning-v2.svg"
    )
    if not all(abs(row["forward"] - 0.5) < 1e-12 for row in near_rows):
        raise RuntimeError("near-singular family no longer preserves the fixed 50% forward error")
    if near_rows[-1]["residual"] >= 1e-12 or near_rows[-1]["conditioned"] <= 0.5:
        raise RuntimeError("conditioned-residual scale audit failed")
    if scale_rows[-1]["normwise_rhs"] >= 1e-10 or abs(scale_rows[-1]["componentwise_rhs"] - 1.0) > 1e-12:
        raise RuntimeError("normwise/componentwise separation audit failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(near_rows, scale_rows), encoding="utf-8")

    print(f"saved={output}")
    print("near-singular: eps,kappa2,forward,relative_residual,kappa_times_residual")
    for row in near_rows:
        if int(row["exponent"]) in (1, 3, 6, 9, 12):
            print(
                f'{row["epsilon"]:.1e},{row["condition"]:.9e},'
                f'{row["forward"]:.9e},{row["residual"]:.9e},'
                f'{row["conditioned"]:.9e}'
            )

    print("scaled: alpha,kappa2,forward,normwise_rhs,componentwise_rhs,kappa_times_normwise")
    for row in scale_rows:
        if int(row["exponent"]) in (0, 3, 6, 9, 12):
            print(
                f'{row["alpha"]:.1e},{row["condition"]:.9e},'
                f'{row["forward"]:.9e},{row["normwise_rhs"]:.9e},'
                f'{row["componentwise_rhs"]:.9e},{row["conditioned"]:.9e}'
            )


if __name__ == "__main__":
    main()
