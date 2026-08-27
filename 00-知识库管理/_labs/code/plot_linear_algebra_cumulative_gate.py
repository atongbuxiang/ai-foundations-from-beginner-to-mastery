#!/usr/bin/env python3
"""Deterministic linear-algebra cumulative gate using only Python stdlib.

Tracks:
A. coordinate growth in an ill-conditioned basis plus quotient/projector checks;
B. equal eigenvalues but different non-normal power behavior, plus SVD tail errors;
C. rank-2 attention scores becoming full-rank after row-softmax, plus vec identity.

The SVG contains no timestamp so a full run has a stable SHA-256 hash.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path


DEFAULT_SEED = 20260820  # Reserved for future randomized interventions.
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "linear-algebra"
    / "plot-linear-algebra-cumulative-gate-v2.svg"
)


Matrix = list[list[float]]
Vector = list[float]


def transpose(a: Matrix) -> Matrix:
    return [list(col) for col in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("incompatible matrix shapes")
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matvec(a: Matrix, x: Vector) -> Vector:
    if not a or len(a[0]) != len(x):
        raise ValueError("incompatible matrix/vector shapes")
    return [sum(row[j] * x[j] for j in range(len(x))) for row in a]


def vec_norm(x: Vector) -> float:
    return math.sqrt(sum(value * value for value in x))


def frobenius_norm(a: Matrix) -> float:
    return math.sqrt(sum(value * value for row in a for value in row))


def matrix_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def inverse_2x2(a: Matrix) -> Matrix:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if abs(det) < 1e-15:
        raise ValueError("singular 2x2 matrix")
    return [
        [a[1][1] / det, -a[0][1] / det],
        [-a[1][0] / det, a[0][0] / det],
    ]


def jacobi_eigenvalues_symmetric(a: Matrix, tolerance: float = 1e-14) -> Vector:
    """Eigenvalues of a small real symmetric matrix via cyclic max-pivot Jacobi."""
    work = [row[:] for row in a]
    n = len(work)
    if any(len(row) != n for row in work):
        raise ValueError("Jacobi input must be square")
    max_steps = 120 * n * n
    for _ in range(max_steps):
        p, q = max(
            ((i, j) for i in range(n) for j in range(i + 1, n)),
            key=lambda pair: abs(work[pair[0]][pair[1]]),
        )
        apq = work[p][q]
        if abs(apq) < tolerance:
            break
        tau = (work[q][q] - work[p][p]) / (2.0 * apq)
        sign = 1.0 if tau >= 0.0 else -1.0
        t = sign / (abs(tau) + math.sqrt(1.0 + tau * tau))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        app = work[p][p]
        aqq = work[q][q]
        work[p][p] = app - t * apq
        work[q][q] = aqq + t * apq
        work[p][q] = work[q][p] = 0.0
        for k in range(n):
            if k in (p, q):
                continue
            akp = work[k][p]
            akq = work[k][q]
            work[k][p] = work[p][k] = c * akp - s * akq
            work[k][q] = work[q][k] = s * akp + c * akq
    return sorted((max(0.0, work[i][i]) for i in range(n)), reverse=True)


def singular_values(a: Matrix) -> Vector:
    ata = matmul(transpose(a), a)
    return [math.sqrt(value) for value in jacobi_eigenvalues_symmetric(ata)]


def numerical_rank(singulars: Vector, relative_tolerance: float = 1e-6) -> int:
    if not singulars or singulars[0] == 0.0:
        return 0
    threshold = relative_tolerance * singulars[0]
    return sum(value > threshold for value in singulars)


def coordinate_and_subspace_experiment() -> tuple[list[dict[str, float]], dict[str, float]]:
    rows: list[dict[str, float]] = []
    for epsilon in (1.0, 0.3, 0.1, 0.03, 0.01, 0.003):
        basis = [[1.0, 1.0], [0.0, epsilon]]
        singulars = singular_values(basis)
        coordinates = [-1.0 / epsilon, 1.0 / epsilon]  # basis @ coords = (0, 1)
        reconstruction = matvec(basis, coordinates)
        rows.append(
            {
                "epsilon": epsilon,
                "condition": singulars[0] / singulars[-1],
                "coordinate_norm": vec_norm(coordinates),
                "residual": vec_norm([reconstruction[0], reconstruction[1] - 1.0]),
            }
        )

    # Quotient representative and orthogonal-projector invariants for Q5's matrix.
    a = [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]]
    null_vector = [-1.0, -1.0, 1.0]
    x = [0.4, -1.2, 2.0]
    shifted_x = [x[i] + 3.7 * null_vector[i] for i in range(3)]
    quotient_error = vec_norm(
        [left - right for left, right in zip(matvec(a, x), matvec(a, shifted_x))]
    )

    c = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    ct = transpose(c)
    projector = matmul(matmul(c, inverse_2x2(matmul(ct, c))), ct)
    projector_idempotence = frobenius_norm(matrix_sub(matmul(projector, projector), projector))
    projector_symmetry = frobenius_norm(matrix_sub(transpose(projector), projector))
    null_error = vec_norm(matvec(a, null_vector))
    checks = {
        "quotient_error": quotient_error,
        "projector_idempotence": projector_idempotence,
        "projector_symmetry": projector_symmetry,
        "null_error": null_error,
    }
    return rows, checks


def operator_norm_upper_triangular(a: float, b: float) -> float:
    # Matrix [[a,b],[0,a]]. Largest eigenvalue of M^T M has this closed form.
    trace = 2.0 * a * a + b * b
    determinant = a ** 4
    discriminant = max(0.0, trace * trace - 4.0 * determinant)
    return math.sqrt(0.5 * (trace + math.sqrt(discriminant)))


def spectral_experiment() -> tuple[list[dict[str, float]], dict[str, object]]:
    rho = 0.9
    powers: list[dict[str, float]] = []
    for k in range(61):
        diagonal = rho**k
        off_diagonal = 0.0 if k == 0 else k * rho ** (k - 1)
        powers.append(
            {
                "k": float(k),
                "normal": diagonal,
                "jordan": operator_norm_upper_triangular(diagonal, off_diagonal),
            }
        )
    peak = max(powers, key=lambda row: row["jordan"])

    singulars = [5.0, 2.0, 0.5, 0.1]
    low_rank = []
    for rank in range(5):
        tail = singulars[rank:]
        low_rank.append(
            {
                "rank": rank,
                "spectral_error": tail[0] if tail else 0.0,
                "frobenius_error": math.sqrt(sum(value * value for value in tail)),
            }
        )
    diagnostics: dict[str, object] = {
        "rho": rho,
        "peak_k": int(peak["k"]),
        "peak_norm": peak["jordan"],
        "one_step_jordan_norm": powers[1]["jordan"],
        "low_rank": low_rank,
    }
    return powers, diagnostics


def row_softmax(a: Matrix) -> Matrix:
    out: Matrix = []
    for row in a:
        maximum = max(row)
        exponentials = [math.exp(value - maximum) for value in row]
        total = sum(exponentials)
        out.append([value / total for value in exponentials])
    return out


def kronecker(a: Matrix, b: Matrix) -> Matrix:
    return [
        [a[i][j] * b[k][ell] for j in range(len(a[0])) for ell in range(len(b[0]))]
        for i in range(len(a))
        for k in range(len(b))
    ]


def column_vec(a: Matrix) -> Vector:
    return [a[i][j] for j in range(len(a[0])) for i in range(len(a))]


def attention_and_vec_experiment() -> dict[str, object]:
    token_count = 8
    theta = [-1.2 + i * 2.5 / (token_count - 1) for i in range(token_count)]
    phi = [-0.9 + i * 2.4 / (token_count - 1) for i in range(token_count)]
    q = [[math.cos(value), math.sin(value)] for value in theta]
    k = [[math.cos(value), math.sin(value)] for value in phi]
    score = [[2.0 * value for value in row] for row in matmul(q, transpose(k))]
    attention = row_softmax(score)
    score_singulars = singular_values(score)
    attention_singulars = singular_values(attention)

    x = [[1.0, 2.0], [3.0, 4.0]]
    left = [[1.0, 1.0], [0.0, 1.0]]
    right = [[2.0, 0.0], [1.0, 1.0]]
    direct = column_vec(matmul(matmul(left, x), right))
    structured = matvec(kronecker(transpose(right), left), column_vec(x))
    vec_error = vec_norm([u - v for u, v in zip(direct, structured)])

    return {
        "score_singulars": score_singulars,
        "attention_singulars": attention_singulars,
        "score_rank": numerical_rank(score_singulars),
        "attention_rank": numerical_rank(attention_singulars),
        "rank_tolerance": 1e-6,
        "vec_error": vec_error,
        "direct_vec": direct,
    }


def svg_text(x: float, y: float, value: str, cls: str = "small", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def make_svg(
    coordinates: list[dict[str, float]],
    subspace_checks: dict[str, float],
    powers: list[dict[str, float]],
    spectral: dict[str, object],
    attention: dict[str, object],
) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="460" viewBox="0 0 1200 460" role="img" aria-labelledby="title desc">',
        '<title id="title">线性代数累计复现门</title>',
        '<desc id="desc">三面板展示病态基中的坐标放大，非正规 Jordan 系统的幂次瞬态和低秩尾误差，以及 attention score 经 softmax 后的秩变化。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.title{font-size:24px;font-weight:700;fill:#1F2937}.head{font-size:22px;font-weight:700;fill:#334155}.small{font-size:15px;fill:#64748B}.label{font-size:17px;fill:#334155}.math{font-family:Georgia,"Times New Roman",serif;font-size:17px;fill:#1F2937}.card{fill:#FFFEFB;stroke:#D7DEE8;stroke-width:1.3}.axis{stroke:#64748B;stroke-width:1.1}.grid{stroke:#D7DEE8;stroke-width:1;stroke-dasharray:4 4}</style></defs>',
        '<rect width="1200" height="460" fill="#FFFFFF"/>',
        '<text x="40" y="38" class="title">LA-CUM-01 计算门：坐标/子空间、谱/SVD 与结构化 AI 运算</text>',
        '<rect x="28" y="58" width="368" height="372" class="card"/><rect x="416" y="58" width="368" height="372" class="card"/><rect x="804" y="58" width="368" height="372" class="card"/>',
        '<text x="50" y="88" class="head">A　同一向量：病态基放大坐标</text>',
        '<text x="438" y="88" class="head">B　同一谱：非正规瞬态与 SVD 尾部</text>',
        '<text x="826" y="88" class="head">C　低秩 score 与 softmax 增秩</text>',
    ]

    # Panel A: log-log coordinate and condition-number growth.
    ax0, ay0, aw, ah = 74.0, 126.0, 275.0, 145.0
    parts += [
        f'<line x1="{ax0}" y1="{ay0+ah}" x2="{ax0+aw}" y2="{ay0+ah}" class="axis"/>',
        f'<line x1="{ax0}" y1="{ay0}" x2="{ax0}" y2="{ay0+ah}" class="axis"/>',
        svg_text(ax0 + aw / 2, ay0 + ah + 25, "−log₁₀ ε（两根基向量趋于共线）", "small", "middle"),
        svg_text(ax0, ay0 - 10, "log₁₀ magnitude", "small"),
    ]
    max_x = max(-math.log10(row["epsilon"]) for row in coordinates)
    max_y = max(math.log10(row["condition"]) for row in coordinates) + 0.12
    condition_points = []
    coordinate_points = []
    for row in coordinates:
        x_value = -math.log10(row["epsilon"])
        x = ax0 + aw * x_value / max_x
        yc = ay0 + ah - ah * math.log10(row["condition"]) / max_y
        yx = ay0 + ah - ah * math.log10(row["coordinate_norm"]) / max_y
        condition_points.append(f"{x:.1f},{yc:.1f}")
        coordinate_points.append(f"{x:.1f},{yx:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{yc:.1f}" r="4.5" fill="#DC2626"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{yx:.1f}" r="4.5" fill="#2563EB"/>')
    parts += [
        f'<polyline points="{" ".join(condition_points)}" fill="none" stroke="#DC2626" stroke-width="2.4"/>',
        f'<polyline points="{" ".join(coordinate_points)}" fill="none" stroke="#2563EB" stroke-width="2.4"/>',
        '<line x1="78" y1="318" x2="102" y2="318" stroke="#DC2626" stroke-width="2.5"/><text x="110" y="322" class="label">κ₂(Bε)</text>',
        '<line x1="205" y1="318" x2="229" y2="318" stroke="#2563EB" stroke-width="2.5"/><text x="237" y="322" class="label">‖[v]Bε‖₂</text>',
        svg_text(50, 354, "v=(0,1) 不变；坐标约按 1/ε 增长", "label"),
        svg_text(50, 379, f'P²−P Frobenius residual = {subspace_checks["projector_idempotence"]:.1e}', "small"),
        svg_text(50, 402, f'商类代表改变，输出不变（残差 {subspace_checks["quotient_error"]:.1e}）', "small"),
    ]

    # Panel B: power norms plus a compact SVD-tail inset.
    bx0, by0, bw, bh = 458.0, 122.0, 285.0, 132.0
    ymax = max(row["jordan"] for row in powers) * 1.08
    parts += [
        f'<line x1="{bx0}" y1="{by0+bh}" x2="{bx0+bw}" y2="{by0+bh}" class="axis"/>',
        f'<line x1="{bx0}" y1="{by0}" x2="{bx0}" y2="{by0+bh}" class="axis"/>',
        svg_text(bx0, by0 - 9, "operator 2-norm", "small"),
        svg_text(bx0 + bw / 2, by0 + bh + 25, "power k", "small", "middle"),
    ]
    jordan_points = []
    normal_points = []
    for row in powers:
        x = bx0 + bw * row["k"] / powers[-1]["k"]
        yj = by0 + bh - bh * row["jordan"] / ymax
        yn = by0 + bh - bh * row["normal"] / ymax
        jordan_points.append(f"{x:.1f},{yj:.1f}")
        normal_points.append(f"{x:.1f},{yn:.1f}")
    parts += [
        f'<polyline points="{" ".join(jordan_points)}" fill="none" stroke="#7C3AED" stroke-width="2.6"/>',
        f'<polyline points="{" ".join(normal_points)}" fill="none" stroke="#16A34A" stroke-width="2.4"/>',
    ]
    peak_k = int(spectral["peak_k"])
    peak_row = powers[peak_k]
    peak_x = bx0 + bw * peak_row["k"] / powers[-1]["k"]
    peak_y = by0 + bh - bh * peak_row["jordan"] / ymax
    parts += [
        f'<circle cx="{peak_x:.1f}" cy="{peak_y:.1f}" r="5" fill="#7C3AED"/>',
        svg_text(peak_x + 8, peak_y - 7, f'peak k={peak_k}, ‖Jᵏ‖={float(spectral["peak_norm"]):.2f}', "small"),
        '<line x1="464" y1="300" x2="488" y2="300" stroke="#7C3AED" stroke-width="2.5"/><text x="496" y="304" class="label">Jρ=[[ρ,1],[0,ρ]]</text>',
        '<line x1="626" y1="300" x2="650" y2="300" stroke="#16A34A" stroke-width="2.5"/><text x="658" y="304" class="label">ρI</text>',
        svg_text(438, 330, "两者 eigenvalues 都是 ρ=0.9；power behavior 不同", "small"),
    ]
    low_rank = spectral["low_rank"]
    assert isinstance(low_rank, list)
    parts.append(svg_text(438, 356, "Eckart–Young tail（σ=5,2,0.5,0.1）", "label"))
    for rank in range(1, 5):
        item = low_rank[rank]
        assert isinstance(item, dict)
        x = 456 + (rank - 1) * 75
        height = 34.0 * float(item["frobenius_error"]) / float(low_rank[1]["frobenius_error"])
        parts.append(f'<rect x="{x}" y="{405-height:.1f}" width="45" height="{height:.1f}" rx="4" fill="#F59E0B" fill-opacity=".8"/>')
        parts.append(svg_text(x + 22.5, 421, f'r={rank}', "small", "middle"))
        parts.append(svg_text(x + 22.5, 397 - height, f'{float(item["frobenius_error"]):.2g}', "small", "middle"))

    # Panel C: singular spectra before and after softmax.
    cx0, cy0, cw, ch = 844.0, 126.0, 282.0, 172.0
    floor = 1e-7
    ceiling = 12.0
    log_floor = math.log10(floor)
    log_ceiling = math.log10(ceiling)
    parts += [
        f'<line x1="{cx0}" y1="{cy0+ch}" x2="{cx0+cw}" y2="{cy0+ch}" class="axis"/>',
        f'<line x1="{cx0}" y1="{cy0}" x2="{cx0}" y2="{cy0+ch}" class="axis"/>',
        svg_text(cx0, cy0 - 9, "singular value（log scale）", "small"),
    ]
    score_singulars = attention["score_singulars"]
    attention_singulars = attention["attention_singulars"]
    assert isinstance(score_singulars, list) and isinstance(attention_singulars, list)

    def y_singular(value: float) -> float:
        clipped = max(floor, min(ceiling, value))
        fraction = (math.log10(clipped) - log_floor) / (log_ceiling - log_floor)
        return cy0 + ch - ch * fraction

    for index in range(8):
        x = cx0 + 18 + index * 34
        score_value = float(score_singulars[index])
        attention_value = float(attention_singulars[index])
        ys = y_singular(score_value)
        yp = y_singular(attention_value)
        parts.append(f'<rect x="{x-8:.1f}" y="{ys:.1f}" width="7" height="{cy0+ch-ys:.1f}" fill="#2563EB"/>')
        parts.append(f'<rect x="{x+2:.1f}" y="{yp:.1f}" width="7" height="{cy0+ch-yp:.1f}" fill="#DB2777"/>')
        parts.append(svg_text(x, cy0 + ch + 19, str(index + 1), "small", "middle"))
    parts += [
        '<rect x="850" y="325" width="10" height="10" fill="#2563EB"/><text x="867" y="335" class="label">S=QKᵀ</text>',
        '<rect x="965" y="325" width="10" height="10" fill="#DB2777"/><text x="982" y="335" class="label">row-softmax(S)</text>',
        svg_text(826, 365, f'numerical rank: {int(attention["score_rank"])} → {int(attention["attention_rank"])}  (relative tol 10⁻⁶)', "label"),
        svg_text(826, 391, f'vec(AXB) identity residual = {float(attention["vec_error"]):.1e}', "small"),
        svg_text(826, 414, "线性 rank 上界不能无条件穿过非线性", "small"),
        '</svg>',
    ]
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    coordinates, subspace_checks = coordinate_and_subspace_experiment()
    powers, spectral = spectral_experiment()
    attention = attention_and_vec_experiment()
    if not coordinates[-1]["coordinate_norm"] > coordinates[0]["coordinate_norm"]:
        raise AssertionError("coordinates should amplify as the basis becomes nearly dependent")
    if not float(spectral["peak_norm"]) > 1.0:
        raise AssertionError("the Jordan block should exhibit transient amplification")
    if not int(attention["attention_rank"]) > int(attention["score_rank"]):
        raise AssertionError("row-wise softmax should increase numerical rank in this example")
    if float(attention["vec_error"]) > 1e-12:
        raise AssertionError("the vec/Kronecker identity failed")
    svg = make_svg(coordinates, subspace_checks, powers, spectral, attention)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print("LA-CUM-01 deterministic computation gate")
    print(f"seed(reserved)={args.seed}")
    print("A coordinate conditioning")
    for row in coordinates:
        print(
            f"  eps={row['epsilon']:.3g}  kappa2={row['condition']:.8g}  "
            f"coord_norm={row['coordinate_norm']:.8g}  residual={row['residual']:.2e}"
        )
    print(
        "  subspace checks: "
        f"A*n={subspace_checks['null_error']:.2e}, "
        f"quotient={subspace_checks['quotient_error']:.2e}, "
        f"P2-P={subspace_checks['projector_idempotence']:.2e}, "
        f"PT-P={subspace_checks['projector_symmetry']:.2e}"
    )
    print("B spectral/Jordan/SVD")
    print(
        f"  rho={spectral['rho']}, ||J||2={spectral['one_step_jordan_norm']:.8g}, "
        f"peak k={spectral['peak_k']}, peak ||J^k||2={spectral['peak_norm']:.8g}"
    )
    low_rank = spectral["low_rank"]
    assert isinstance(low_rank, list)
    for item in low_rank[1:]:
        print(
            f"  rank={item['rank']}  spectral_error={item['spectral_error']:.8g}  "
            f"frobenius_error={item['frobenius_error']:.8g}"
        )
    print("C structured AI")
    print("  score singulars=" + ", ".join(f"{x:.8g}" for x in attention["score_singulars"]))
    print("  softmax singulars=" + ", ".join(f"{x:.8g}" for x in attention["attention_singulars"]))
    print(f"  numerical ranks={attention['score_rank']} -> {attention['attention_rank']}")
    print(f"  vec identity={attention['direct_vec']}, residual={attention['vec_error']:.2e}")
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(0)
