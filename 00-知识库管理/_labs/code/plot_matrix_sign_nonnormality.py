"""Plot Newton convergence and nonnormal sensitivity of the matrix sign.

The analytic family is A_q = [[1, q], [0, -1]].  It satisfies A_q**2 = I,
so sign(A_q) = A_q although its eigenvalues remain exactly +1 and -1.
After Frobenius scaling, the matrix Newton iteration reduces to the scalar
recurrence x <- (x + 1/x)/2 with x_0 = 1/sqrt(2+q^2).

For E=e_21, the exact Frechet derivative has Frobenius norm
sqrt(1 + q^2/2 + q^4/4).  The script uses only the Python standard library
and writes one deterministic, self-contained SVG.
"""

from __future__ import annotations

from math import log10, sqrt
from pathlib import Path


WIDTH = 1200
HEIGHT = 790
TOP = 142
BOTTOM = 146
LEFT_A = 86
RIGHT_A = 558
LEFT_B = 680
RIGHT_B = 1152
PLOT_HEIGHT = HEIGHT - TOP - BOTTOM

Q_MIN_LOG = -2.0
Q_MAX_LOG = 8.0
SAMPLES = 241
TARGET = 1e-12
MAX_STEPS = 100


def q_values() -> list[float]:
    return [10.0 ** (Q_MIN_LOG + index / (SAMPLES - 1) * (Q_MAX_LOG - Q_MIN_LOG)) for index in range(SAMPLES)]


def newton_steps(q_value: float) -> int:
    """Steps until |x_k^2-1| < TARGET for X_0=A_q/||A_q||_F."""
    x_value = 1.0 / sqrt(2.0 + q_value * q_value)
    for step in range(MAX_STEPS + 1):
        if abs(x_value * x_value - 1.0) < TARGET:
            return step
        x_value = 0.5 * (x_value + 1.0 / x_value)
    return MAX_STEPS


def sign_spectral_norm(q_value: float) -> float:
    """Exact 2-norm of [[1,q],[0,-1]]."""
    trace = 2.0 + q_value * q_value
    largest_eigenvalue = 0.5 * (trace + sqrt(trace * trace - 4.0))
    return sqrt(largest_eigenvalue)


def derivative_frobenius_norm(q_value: float) -> float:
    """Exact ||L_sign(A_q,e_21)||_F for delta=1."""
    return sqrt(1.0 + 0.5 * q_value * q_value + 0.25 * q_value**4)


def x_coord(q_value: float, left: float, right: float) -> float:
    fraction = (log10(q_value) - Q_MIN_LOG) / (Q_MAX_LOG - Q_MIN_LOG)
    return left + fraction * (right - left)


def y_steps(step: int) -> float:
    maximum = 40.0
    return TOP + (1.0 - min(step, maximum) / maximum) * PLOT_HEIGHT


def y_log(value: float) -> float:
    low_log = 0.0
    high_log = 16.0
    clipped = min(10.0**high_log, max(10.0**low_log, value))
    fraction = (log10(clipped) - low_log) / (high_log - low_log)
    return TOP + (1.0 - fraction) * PLOT_HEIGHT


def path(values: list[tuple[float, float]], left: float, right: float, y_function) -> str:
    points = [f"{x_coord(q_value, left, right):.2f},{y_function(value):.2f}" for q_value, value in values]
    return "M " + " L ".join(points)


def build_svg() -> str:
    q_grid = q_values()
    steps = [(q_value, float(newton_steps(q_value))) for q_value in q_grid]
    sign_norms = [(q_value, sign_spectral_norm(q_value)) for q_value in q_grid]
    derivative_norms = [(q_value, derivative_frobenius_norm(q_value)) for q_value in q_grid]
    bottom = TOP + PLOT_HEIGHT

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        '<title id="title">Nonnormality slows scaled Newton and amplifies the matrix sign derivative</title>',
        '<desc id="description">For A_q equal to the upper triangular matrix with diagonal one and minus one and off-diagonal q, the eigenvalues stay fixed. The left panel shows that Frobenius scaling makes Newton need more iterations as q grows. The right panel shows unbounded sign norm and quadratic derivative amplification.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;fill:#1f2937}.title{font-size:27px;font-weight:650}.subtitle{font-size:15px;fill:#64748b}.panel{font-size:19px;font-weight:650}.axis{font-size:16px;font-weight:600}.tick{font-size:15px;fill:#64748b}.legend{font-size:15px;font-weight:600}.note{font-size:15px;fill:#64748b}.math{font-family:Georgia,"Times New Roman",serif;font-size:16px;font-weight:600}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="38" text-anchor="middle">固定特征值不代表 matrix sign 温和：非正规性同时影响算法与导数</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="66" text-anchor="middle">A_q = [[1,q],[0,−1]]，Λ(A_q)={{−1,+1}}，且 sign(A_q)=A_q；横轴 q=t/δ 采用对数刻度</text>',
        f'<text class="panel" x="{(LEFT_A + RIGHT_A) / 2}" y="105" text-anchor="middle">A　Frobenius 缩放后的 Newton 步数</text>',
        f'<text class="panel" x="{(LEFT_B + RIGHT_B) / 2}" y="105" text-anchor="middle">B　sign 范数与一个精确方向导数</text>',
        f'<rect x="{LEFT_A}" y="{TOP}" width="{RIGHT_A - LEFT_A}" height="{PLOT_HEIGHT}" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
        f'<rect x="{LEFT_B}" y="{TOP}" width="{RIGHT_B - LEFT_B}" height="{PLOT_HEIGHT}" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
    ]

    for exponent in (-2, 0, 2, 4, 6, 8):
        q_value = 10.0**exponent
        for left, right in ((LEFT_A, RIGHT_A), (LEFT_B, RIGHT_B)):
            x_value = x_coord(q_value, left, right)
            parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#f1f5f9"/>')
            parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom + 23}" text-anchor="middle">10^{exponent}</text>')

    for step in (0, 10, 20, 30, 40):
        y_value = y_steps(step)
        parts.append(f'<line x1="{LEFT_A}" y1="{y_value:.2f}" x2="{RIGHT_A}" y2="{y_value:.2f}" stroke="#e2e8f0"/>')
        parts.append(f'<text class="tick" x="{LEFT_A - 11}" y="{y_value + 4:.2f}" text-anchor="end">{step}</text>')

    for exponent in (0, 4, 8, 12, 16):
        value = 10.0**exponent
        y_value = y_log(value)
        parts.append(f'<line x1="{LEFT_B}" y1="{y_value:.2f}" x2="{RIGHT_B}" y2="{y_value:.2f}" stroke="#e2e8f0"/>')
        parts.append(f'<text class="tick" x="{LEFT_B - 11}" y="{y_value + 4:.2f}" text-anchor="end">10^{exponent}</text>')

    parts.extend(
        [
            f'<path d="{path(steps, LEFT_A, RIGHT_A, y_steps)}" fill="none" stroke="#2563eb" stroke-width="3.2" stroke-linejoin="round"/>',
            f'<path d="{path(sign_norms, LEFT_B, RIGHT_B, y_log)}" fill="none" stroke="#10b981" stroke-width="3.2" stroke-linejoin="round"/>',
            f'<path d="{path(derivative_norms, LEFT_B, RIGHT_B, y_log)}" fill="none" stroke="#dc2626" stroke-width="3.2" stroke-linejoin="round"/>',
            f'<text class="axis" x="{(LEFT_A + RIGHT_A) / 2}" y="{bottom + 58}" text-anchor="middle">非正规比值 q</text>',
            f'<text class="axis" x="{(LEFT_B + RIGHT_B) / 2}" y="{bottom + 58}" text-anchor="middle">非正规比值 q</text>',
            f'<text class="axis" x="24" y="{TOP + PLOT_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 24 {TOP + PLOT_HEIGHT / 2})">达到 |x(k)^2−1| &lt; 10⁻¹² 的步数</text>',
            f'<text class="axis" x="615" y="{TOP + PLOT_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 615 {TOP + PLOT_HEIGHT / 2})">范数（对数刻度）</text>',
            f'<line x1="{LEFT_A + 24}" y1="{TOP + 30}" x2="{LEFT_A + 58}" y2="{TOP + 30}" stroke="#2563eb" stroke-width="3.2"/>',
            f'<text class="legend" x="{LEFT_A + 69}" y="{TOP + 34}">scaled Newton 步数</text>',
            f'<rect x="{LEFT_B + 22}" y="{TOP + 18}" width="263" height="73" rx="9" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1"/>',
            f'<line x1="{LEFT_B + 38}" y1="{TOP + 42}" x2="{LEFT_B + 72}" y2="{TOP + 42}" stroke="#10b981" stroke-width="3.2"/>',
            f'<text class="legend" x="{LEFT_B + 83}" y="{TOP + 46}">‖sign(A_q)‖₂</text>',
            f'<line x1="{LEFT_B + 38}" y1="{TOP + 70}" x2="{LEFT_B + 72}" y2="{TOP + 70}" stroke="#dc2626" stroke-width="3.2"/>',
            f'<text class="legend" x="{LEFT_B + 83}" y="{TOP + 74}">‖L_sign(A_q,e₂₁)‖F</text>',
            f'<text class="note" x="{LEFT_A}" y="{HEIGHT - 56}">左图：X₀=A_q/‖A_q‖F 后，特征值初值 x₀=1/√(2+q²)；q 越大，先从极小尺度恢复所需的步数越多。</text>',
            f'<text class="note" x="{LEFT_A}" y="{HEIGHT - 30}">右图：绿色约按 q 增长，红色约按 q²/2 增长；点谱始终固定为 ±1，因此增长完全来自非正规不变子空间几何。</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    assert newton_steps(1.0e8) > newton_steps(1.0e2) > newton_steps(1.0)
    assert abs(sign_spectral_norm(1.0e8) / 1.0e8 - 1.0) < 1e-12
    assert abs(derivative_frobenius_norm(1.0e4) / (0.5e8) - 1.0) < 1e-6
    vault_root = Path(__file__).resolve().parents[3]
    output = vault_root / "00-知识库管理" / "_assets" / "plots" / "matrix-sign" / "plot-matrix-sign-nonnormality-v2.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")

    print(f"saved={output}")
    print("q,newton_steps,sign_2_norm,frechet_F_norm")
    for q_value in (1e-2, 1.0, 1e2, 1e4, 1e8):
        print(
            f"{q_value:.0e},{newton_steps(q_value)},"
            f"{sign_spectral_norm(q_value):.12e},"
            f"{derivative_frobenius_norm(q_value):.12e}"
        )


if __name__ == "__main__":
    main()
