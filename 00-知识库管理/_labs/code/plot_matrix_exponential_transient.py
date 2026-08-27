"""Plot finite-time amplification for a stable nonnormal matrix family.

For A_K = [[-1, K], [0, -2]], the matrix exponential is known exactly.
This deterministic script uses only the Python standard library and writes a
self-contained SVG into the vault assets folder.
"""

from __future__ import annotations

from math import exp, log, sqrt
from pathlib import Path


WIDTH = 1080
HEIGHT = 680
LEFT = 90
RIGHT = 44
TOP = 112
BOTTOM = 92
PLOT_WIDTH = WIDTH - LEFT - RIGHT
PLOT_HEIGHT = HEIGHT - TOP - BOTTOM
T_MIN = 0.0
T_MAX = 5.0
Y_MIN = 0.0
Y_MAX = 5.4
STEPS = 501
K_VALUES = (0.0, 5.0, 20.0)
COLORS = {0.0: "#2563eb", 5.0: "#16a34a", 20.0: "#dc2626"}


def entries(t_value: float, coupling: float) -> tuple[float, float, float]:
    """Return a, b, d for exp(t A_K) = [[a, b], [0, d]]."""
    a = exp(-t_value)
    d = exp(-2.0 * t_value)
    b = coupling * (a - d)
    return a, b, d


def spectral_norm(t_value: float, coupling: float) -> float:
    """Largest singular value of the exact two-by-two exponential."""
    a, b, d = entries(t_value, coupling)
    trace_gram = a * a + b * b + d * d
    determinant_gram = (a * d) ** 2
    discriminant = max(0.0, trace_gram * trace_gram - 4.0 * determinant_gram)
    largest_eigenvalue = 0.5 * (trace_gram + sqrt(discriminant))
    return sqrt(largest_eigenvalue)


def x_coord(t_value: float) -> float:
    return LEFT + (t_value - T_MIN) / (T_MAX - T_MIN) * PLOT_WIDTH


def y_coord(value: float) -> float:
    return TOP + (1.0 - (value - Y_MIN) / (Y_MAX - Y_MIN)) * PLOT_HEIGHT


def curve_path(coupling: float) -> str:
    points: list[str] = []
    for index in range(STEPS):
        t_value = T_MIN + (T_MAX - T_MIN) * index / (STEPS - 1)
        points.append(f"{x_coord(t_value):.2f},{y_coord(spectral_norm(t_value, coupling)):.2f}")
    return "M " + " L ".join(points)


def peak(coupling: float) -> tuple[float, float]:
    samples = [
        (T_MIN + (T_MAX - T_MIN) * index / (20 * (STEPS - 1)))
        for index in range(20 * (STEPS - 1) + 1)
    ]
    return max(((spectral_norm(t_value, coupling), t_value) for t_value in samples))


def build_svg() -> str:
    bottom = TOP + PLOT_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Stable eigenvalues do not preclude transient amplification</title>',
        '<desc id="desc">The spectral norm of exp(t A K) is plotted for upper triangular stable matrices with couplings zero, five and twenty. Larger nonnormal coupling produces a higher finite-time peak although both eigenvalues remain negative.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#172033}.title{font-size:23px;font-weight:700}.subtitle{font-size:14px;fill:#536176}.axis{font-size:14px;font-weight:600}.tick{font-size:12px;fill:#64748b}.legend{font-size:14px;font-weight:600}.note{font-size:13px;fill:#475569}</style>',
        f'<text class="title" x="{WIDTH / 2}" y="37" text-anchor="middle">Stable eigenvalues can hide finite-time amplification</text>',
        f'<text class="subtitle" x="{WIDTH / 2}" y="63" text-anchor="middle">A_K = [[−1, K], [0, −2]] has α(A_K) = −1 for every K, but ||exp(tA_K)||₂ depends strongly on K</text>',
    ]

    for y_tick in (0, 1, 2, 3, 4, 5):
        y_value = y_coord(float(y_tick))
        parts.append(f'<line x1="{LEFT}" y1="{y_value:.2f}" x2="{WIDTH - RIGHT}" y2="{y_value:.2f}" stroke="#e2e8f0"/>')
        parts.append(f'<text class="tick" x="{LEFT - 13}" y="{y_value + 4:.2f}" text-anchor="end">{y_tick}</text>')

    for x_tick in range(0, 6):
        x_value = x_coord(float(x_tick))
        parts.append(f'<line x1="{x_value:.2f}" y1="{TOP}" x2="{x_value:.2f}" y2="{bottom}" stroke="#f1f5f9"/>')
        parts.append(f'<text class="tick" x="{x_value:.2f}" y="{bottom + 25}" text-anchor="middle">{x_tick}</text>')

    parts.extend(
        [
            f'<line x1="{LEFT}" y1="{bottom}" x2="{WIDTH - RIGHT}" y2="{bottom}" stroke="#334155" stroke-width="1.6"/>',
            f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{bottom}" stroke="#334155" stroke-width="1.6"/>',
            f'<text class="axis" x="{LEFT + PLOT_WIDTH / 2}" y="{bottom + 60}" text-anchor="middle">time t</text>',
            f'<text class="axis" x="28" y="{TOP + PLOT_HEIGHT / 2}" text-anchor="middle" transform="rotate(-90 28 {TOP + PLOT_HEIGHT / 2})">spectral norm ||exp(tA_K)||₂</text>',
            f'<line x1="{x_coord(log(2.0)):.2f}" y1="{TOP}" x2="{x_coord(log(2.0)):.2f}" y2="{bottom}" stroke="#7c3aed" stroke-width="1.7" stroke-dasharray="7 6"/>',
            f'<text class="note" x="{x_coord(log(2.0)) + 8:.2f}" y="{TOP + 20}">t = ln 2: off-diagonal term K/4</text>',
        ]
    )

    for coupling in K_VALUES:
        color = COLORS[coupling]
        parts.append(f'<path d="{curve_path(coupling)}" fill="none" stroke="{color}" stroke-width="3.2"/>')

    legend_x = WIDTH - RIGHT - 190
    legend_y = TOP + 42
    parts.append(f'<rect x="{legend_x - 18}" y="{legend_y - 28}" width="194" height="102" rx="9" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1"/>')
    for index, coupling in enumerate(K_VALUES):
        y_value = legend_y + index * 28
        parts.append(f'<line x1="{legend_x}" y1="{y_value}" x2="{legend_x + 34}" y2="{y_value}" stroke="{COLORS[coupling]}" stroke-width="3.5"/>')
        parts.append(f'<text class="legend" x="{legend_x + 45}" y="{y_value + 5}">K = {int(coupling)}</text>')

    peak_value, peak_time = peak(20.0)
    peak_x = x_coord(peak_time)
    peak_y = y_coord(peak_value)
    parts.extend(
        [
            f'<circle cx="{peak_x:.2f}" cy="{peak_y:.2f}" r="5.2" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>',
            f'<path d="M {peak_x + 7:.2f},{peak_y - 4:.2f} L {peak_x + 80:.2f},{peak_y - 49:.2f}" fill="none" stroke="#991b1b" stroke-width="1.5"/>',
            f'<rect x="{peak_x + 74:.2f}" y="{peak_y - 76:.2f}" width="176" height="50" rx="7" fill="#fff7ed" stroke="#fdba74"/>',
            f'<text class="note" x="{peak_x + 86:.2f}" y="{peak_y - 56:.2f}">K = 20 peak ≈ {peak_value:.3f}</text>',
            f'<text class="note" x="{peak_x + 86:.2f}" y="{peak_y - 38:.2f}">at t ≈ {peak_time:.3f}</text>',
            f'<text class="note" x="{LEFT}" y="{HEIGHT - 20}">All curves decay to zero as t → ∞. The peak is a finite-time, direction-dependent effect caused by nonnormal coupling—not unstable eigenvalues.</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts)


def main() -> None:
    vault_root = Path(__file__).resolve().parents[3]
    output = (
        vault_root
        / "00-知识库管理"
        / "_assets"
        / "plots"
        / "matrix-functions"
        / "plot-matrix-exponential-transient-v1.svg"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")

    print(f"saved={output}")
    print("K,norm_at_t0,norm_at_ln2,peak_norm,peak_time")
    for coupling in K_VALUES:
        peak_value, peak_time = peak(coupling)
        print(
            f"{coupling:.0f},{spectral_norm(0.0, coupling):.6f},"
            f"{spectral_norm(log(2.0), coupling):.6f},"
            f"{peak_value:.6f},{peak_time:.6f}"
        )


if __name__ == "__main__":
    main()
