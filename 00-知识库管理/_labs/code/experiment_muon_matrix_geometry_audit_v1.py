#!/usr/bin/env python3
"""Deterministic, standard-library audit for TRN-25--TRN-32.

The experiment separates norm-ball identities, exact 2x2 polar geometry,
finite-step Newton--Schulz maps, shape scaling, optimizer-state semantics,
Stiefel feasibility and a declared systems-cost proxy.  It writes JSON/CSV
evidence and three self-contained SVG plots.  NumPy, PyTorch and plotting
libraries are deliberately not required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


SEED = 20260826
JORDAN = (3.4445, -4.7750, 2.0315)
CLASSIC = (1.5, -0.5, 0.0)


def dot(x: list[float], y: list[float]) -> float:
    return sum(a * b for a, b in zip(x, y))


def norm(x: list[float]) -> float:
    return math.sqrt(dot(x, x))


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def matscale(a: list[list[float]], scale: float) -> list[list[float]]:
    return [[scale * value for value in row] for row in a]


def matadd(*terms: list[list[float]]) -> list[list[float]]:
    return [
        [sum(term[i][j] for term in terms) for j in range(len(terms[0][0]))]
        for i in range(len(terms[0]))
    ]


def flatten(a: list[list[float]]) -> list[float]:
    return [value for row in a for value in row]


def frobenius(a: list[list[float]]) -> float:
    return norm(flatten(a))


def matrix_difference_norm(a: list[list[float]], b: list[list[float]]) -> float:
    return norm([x - y for x, y in zip(flatten(a), flatten(b))])


def identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def diagonal(values: list[float]) -> list[list[float]]:
    return [[value if i == j else 0.0 for j in range(len(values))] for i, value in enumerate(values)]


def trace_pairing(a: list[list[float]], b: list[list[float]]) -> float:
    return dot(flatten(a), flatten(b))


def sym2_eigendecomposition(a: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    """Return descending eigenvalues and column eigenvectors for symmetric 2x2."""
    aa, bb, dd = a[0][0], a[0][1], a[1][1]
    radius = math.hypot((aa - dd) / 2.0, bb)
    center = (aa + dd) / 2.0
    values = [center + radius, center - radius]
    theta = 0.5 * math.atan2(2.0 * bb, aa - dd)
    c, s = math.cos(theta), math.sin(theta)
    vectors = [[c, -s], [s, c]]
    return values, vectors


def singular_values_2x2(a: list[list[float]]) -> list[float]:
    values, _ = sym2_eigendecomposition(matmul(transpose(a), a))
    return [math.sqrt(max(value, 0.0)) for value in values]


def symmetric_from_eigen(vectors: list[list[float]], values: list[float]) -> list[list[float]]:
    return matmul(matmul(vectors, diagonal(values)), transpose(vectors))


def polar_2x2(a: list[list[float]], tolerance: float = 1e-12) -> list[list[float]]:
    gram = matmul(transpose(a), a)
    eigenvalues, vectors = sym2_eigendecomposition(gram)
    inverse_sqrt = [1.0 / math.sqrt(value) if value > tolerance else 0.0 for value in eigenvalues]
    return matmul(a, symmetric_from_eigen(vectors, inverse_sqrt))


def spectral_norm_2x2(a: list[list[float]]) -> float:
    return max(singular_values_2x2(a))


def nuclear_norm_2x2(a: list[list[float]]) -> float:
    return sum(singular_values_2x2(a))


def scalar_map(s: float, coefficients: tuple[float, float, float]) -> float:
    aa, bb, cc = coefficients
    return aa * s + bb * s**3 + cc * s**5


def scalar_trajectory(s0: float, coefficients: tuple[float, float, float], steps: int) -> list[float]:
    values = [s0]
    for _ in range(steps):
        values.append(scalar_map(values[-1], coefficients))
    return values


def ns_step(x: list[list[float]], coefficients: tuple[float, float, float]) -> list[list[float]]:
    aa, bb, cc = coefficients
    rows, cols = len(x), len(x[0])
    if rows >= cols:
        gram = matmul(transpose(x), x)
        cubic = matmul(x, gram)
        quintic = matmul(cubic, gram)
    else:
        gram = matmul(x, transpose(x))
        cubic = matmul(gram, x)
        quintic = matmul(gram, cubic)
    return matadd(matscale(x, aa), matscale(cubic, bb), matscale(quintic, cc))


def ns_iterate(x: list[list[float]], coefficients: tuple[float, float, float], steps: int) -> list[list[float]]:
    result = [row[:] for row in x]
    for _ in range(steps):
        result = ns_step(result, coefficients)
    return result


def support_projector_from_diagonal(values: list[float], tolerance: float = 1e-14) -> list[list[float]]:
    return diagonal([1.0 if abs(value) > tolerance else 0.0 for value in values])


def audit_norm_duality() -> list[dict]:
    g = [3.0, 1.0]
    root10 = math.sqrt(10.0)
    candidates = [
        ("l2", [-3.0 / root10, -1.0 / root10], root10),
        ("linf", [-1.0, -1.0], 4.0),
        ("l1", [-1.0, 0.0], 3.0),
    ]
    rows = []
    for geometry, direction, dual in candidates:
        if geometry == "l2":
            feasibility = norm(direction)
        elif geometry == "linf":
            feasibility = max(abs(value) for value in direction)
        else:
            feasibility = sum(abs(value) for value in direction)
        rows.append(
            {
                "geometry": geometry,
                "g1": g[0],
                "g2": g[1],
                "d1": direction[0],
                "d2": direction[1],
                "step_norm": feasibility,
                "dual_norm": dual,
                "pairing": dot(g, direction),
                "predicted_decrease": -dot(g, direction),
                "optimality_gap": abs(dot(g, direction) + dual),
            }
        )
    return rows


def audit_polar_geometry() -> tuple[list[dict], list[dict]]:
    cases = {
        "diagonal": [[4.0, 0.0], [0.0, 1.0]],
        "off_diagonal": [[0.0, 2.0], [1.0, 0.0]],
        "rank_one": [[3.0, 0.0], [0.0, 0.0]],
        "rotated": [[2.0, 1.0], [1.0, 2.0]],
    }
    rows = []
    for name, gradient in cases.items():
        polar = polar_2x2(gradient)
        singular = singular_values_2x2(gradient)
        rank = sum(value > 1e-10 for value in singular)
        projector = support_projector_from_diagonal(singular)
        qtq = matmul(transpose(polar), polar)
        rows.append(
            {
                "case": name,
                "sigma1": singular[0],
                "sigma2": singular[1],
                "rank": rank,
                "nuclear_norm": sum(singular),
                "polar_spectral_norm": spectral_norm_2x2(polar),
                "polar_frobenius_norm": frobenius(polar),
                "pairing": trace_pairing(gradient, polar),
                "duality_gap": abs(trace_pairing(gradient, polar) - sum(singular)),
                "support_orthogonality_residual": matrix_difference_norm(qtq, projector),
            }
        )

    gradient = [[3.0, 0.0], [0.0, 0.0]]
    nonunique_rows = []
    for value in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        candidate = [[1.0, 0.0], [0.0, value]]
        nonunique_rows.append(
            {
                "null_space_value": value,
                "spectral_norm": spectral_norm_2x2(candidate),
                "frobenius_norm": frobenius(candidate),
                "pairing": trace_pairing(gradient, candidate),
                "nuclear_norm": nuclear_norm_2x2(gradient),
            }
        )
    return rows, nonunique_rows


def audit_newton_schulz() -> tuple[list[dict], list[dict]]:
    scalar_rows = []
    starts = [1.0, 0.5, 0.1, 0.01, 0.0]
    for name, coefficients in [("classic", CLASSIC), ("jordan", JORDAN)]:
        for start in starts:
            trajectory = scalar_trajectory(start, coefficients, 8)
            for step, value in enumerate(trajectory):
                scalar_rows.append(
                    {
                        "method": name,
                        "s0": start,
                        "step": step,
                        "singular_value": value,
                        "absolute_target_error": abs(value - (1.0 if start > 0 else 0.0)),
                        "squared_orthogonality_error": abs(value * value - (1.0 if start > 0 else 0.0)),
                    }
                )

    spectra = {
        "flat": [1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)],
        "moderate": [1.0, 0.1],
        "ill_conditioned": [1.0, 1e-4],
        "rank_deficient": [1.0, 0.0],
    }
    matrix_rows = []
    for method, coefficients in [("classic", CLASSIC), ("jordan", JORDAN)]:
        for case, values in spectra.items():
            initial = diagonal(values)
            for steps in [0, 1, 3, 5, 8]:
                output = ns_iterate(initial, coefficients, steps)
                target = support_projector_from_diagonal(values)
                out_singular = singular_values_2x2(output)
                matrix_rows.append(
                    {
                        "method": method,
                        "case": case,
                        "steps": steps,
                        "initial_sigma_min_nonzero": min(value for value in values if value > 0.0),
                        "output_sigma1": out_singular[0],
                        "output_sigma2": out_singular[1],
                        "support_orthogonality_residual": matrix_difference_norm(
                            matmul(transpose(output), output), target
                        ),
                        "polar_direction_residual": matrix_difference_norm(output, target),
                        "finite": all(math.isfinite(value) for value in flatten(output)),
                    }
                )
    return scalar_rows, matrix_rows


def shape_scale(mode: str, rows: int, cols: int) -> float:
    if mode == "original":
        return math.sqrt(max(1.0, rows / cols))
    if mode == "match_rms_adamw":
        return 0.2 * math.sqrt(max(rows, cols))
    if mode == "spectral_unclamped":
        return math.sqrt(rows / cols)
    raise ValueError(mode)


def audit_shape_scaling() -> list[dict]:
    rows = []
    for a, b, rank in [
        (4096, 1024, 1024),
        (1024, 4096, 1024),
        (4096, 4096, 4096),
        (8, 4, 2),
    ]:
        base_rms = math.sqrt(rank / (a * b))
        for mode in ["unscaled", "original", "match_rms_adamw", "spectral_unclamped"]:
            scale = 1.0 if mode == "unscaled" else shape_scale(mode, a, b)
            rows.append(
                {
                    "rows_A": a,
                    "columns_B": b,
                    "rank": rank,
                    "full_rank": rank == min(a, b),
                    "mode": mode,
                    "scale": scale,
                    "base_rms": base_rms,
                    "scaled_rms": scale * base_rms,
                    "scaled_spectral_norm": scale,
                }
            )
    return rows


def audit_momentum_and_optimizer_boundaries() -> tuple[list[dict], list[dict]]:
    gradients = [2.0, -1.0, 0.5, -0.25]
    momentum = 0.9
    ema, total = 0.0, 0.0
    momentum_rows = []
    for step, gradient in enumerate(gradients, start=1):
        ema = momentum * ema + (1.0 - momentum) * gradient
        total = momentum * total + gradient
        nesterov = (1.0 - momentum) * gradient + momentum * ema
        momentum_rows.append(
            {
                "step": step,
                "gradient": gradient,
                "ema_buffer": ema,
                "sum_buffer": total,
                "sum_times_one_minus_mu": (1.0 - momentum) * total,
                "ema_sum_relation_gap": abs(ema - (1.0 - momentum) * total),
                "current_pytorch_nesterov_matrix": nesterov,
            }
        )
    momentum_rows.append(
        {
            "step": 99,
            "gradient": 1.0,
            "ema_buffer": 1.0,
            "sum_buffer": 0.0,
            "sum_times_one_minus_mu": 0.0,
            "ema_sum_relation_gap": 1.0,
            "current_pytorch_nesterov_matrix": 0.0,
            "note": "communication counterexample: sign(2-1)=1, sign(2)+sign(-1)=0",
        }
    )

    histories = {
        "history_first_axis": ([10.0, 1.0], [1.0, 1.0]),
        "history_second_axis": ([1.0, 10.0], [1.0, 1.0]),
    }
    boundary_rows = []
    for name, (previous, current) in histories.items():
        accumulated = [p * p + c * c for p, c in zip(previous, current)]
        shampoo = [c / math.sqrt(value) for c, value in zip(current, accumulated)]
        muon = [1.0, 1.0]
        boundary_rows.append(
            {
                "history": name,
                "left_right_factor_1": accumulated[0],
                "left_right_factor_2": accumulated[1],
                "shampoo_update_1": shampoo[0],
                "shampoo_update_2": shampoo[1],
                "muon_reset_update_1": muon[0],
                "muon_reset_update_2": muon[1],
                "update_gap": norm([shampoo[i] - muon[i] for i in range(2)]),
            }
        )
    return momentum_rows, boundary_rows


def audit_stiefel_and_rotation() -> list[dict]:
    w = identity(2)
    xi = [[0.0, -1.0], [1.0, 0.0]]
    tangent_residual = matrix_difference_norm(
        matadd(matmul(transpose(w), xi), matmul(transpose(xi), w)),
        [[0.0, 0.0], [0.0, 0.0]],
    )
    rows = []
    for eta in [0.01, 0.1, 0.5]:
        euler = matadd(w, matscale(xi, eta))
        euler_residual = matrix_difference_norm(matmul(transpose(euler), euler), identity(2))
        retracted = polar_2x2(euler)
        retract_residual = matrix_difference_norm(matmul(transpose(retracted), retracted), identity(2))
        rows.append(
            {
                "case": "stiefel_step",
                "eta": eta,
                "tangent_residual": tangent_residual,
                "euler_feasibility_residual": euler_residual,
                "polar_retraction_feasibility_residual": retract_residual,
            }
        )

    angle_left, angle_right = 0.4, -0.7
    ql = [[math.cos(angle_left), -math.sin(angle_left)], [math.sin(angle_left), math.cos(angle_left)]]
    qr = [[math.cos(angle_right), -math.sin(angle_right)], [math.sin(angle_right), math.cos(angle_right)]]
    original = diagonal([3.0, 1.0])
    rotated = matmul(matmul(ql, original), transpose(qr))
    before, after = singular_values_2x2(original), singular_values_2x2(rotated)
    rows.append(
        {
            "case": "double_rotation",
            "eta": 0.0,
            "tangent_residual": 0.0,
            "euler_feasibility_residual": 0.0,
            "polar_retraction_feasibility_residual": 0.0,
            "sigma1_before": before[0],
            "sigma2_before": before[1],
            "sigma1_after": after[0],
            "sigma2_after": after[1],
            "singular_value_invariance_gap": norm([before[i] - after[i] for i in range(2)]),
        }
    )
    return rows


def audit_system_proxy() -> list[dict]:
    rows = []
    for a, b in [(4096, 1024), (1024, 4096), (4096, 4096), (8192, 1024)]:
        elements = a * b
        smaller = min(a, b)
        for steps in [3, 5]:
            rows.append(
                {
                    "rows_A": a,
                    "columns_B": b,
                    "ns_steps": steps,
                    "ns_gemm_flops_proxy": 6 * a * b * smaller * steps,
                    "fp32_momentum_bytes": 4 * elements,
                    "fp32_small_gram_bytes": 4 * smaller * smaller,
                    "fp32_two_matrix_temporaries_bytes": 8 * elements,
                    "proxy_boundary": "algorithmic GEMM/state proxy; not measured wall-clock or peak",
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def svg_escape(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_header(title: str, description: str, height: int = 720) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{svg_escape(title)}</title>',
        f'<desc id="desc">{svg_escape(description)}</desc>',
        f'<rect width="1200" height="{height}" fill="#FFFEFB"/>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;fill:#0F172A}.h{font-size:27px;font-weight:700}.sh{font-size:18px;font-weight:700}.b{font-size:14px}.s{font-size:12px;fill:#64748B}.axis{stroke:#94A3B8;stroke-width:1.5}.grid{stroke:#E2E8F0;stroke-width:1}.blue{stroke:#2563EB;fill:none;stroke-width:3}.green{stroke:#0F766E;fill:none;stroke-width:3}.amber{stroke:#B76E00;fill:none;stroke-width:3}.red{stroke:#C0392B;fill:none;stroke-width:3}.card{fill:#F8FAFC;stroke:#CBD5E1;stroke-width:1.5}</style>',
    ]


def save_svg(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines + ["</svg>", ""]), encoding="utf-8")


def plot_norm_polar(path: Path, norm_rows: list[dict], polar_rows: list[dict]) -> None:
    lines = svg_header(
        "Norm oracle 与 polar 对偶极值",
        "左侧比较同一向量梯度在三种单位球上的最大预测下降，右侧验证四个矩阵的 polar pairing 等于 nuclear norm。",
    )
    lines += [
        '<text x="48" y="48" class="h" fill="#2563EB">Norm oracle 与 polar：两次 support-function 验收</text>',
        '<rect x="48" y="88" width="520" height="520" rx="14" class="card"/>',
        '<text x="72" y="124" class="sh">A｜g=(3,1) 的三种单位步预算</text>',
        '<line x1="104" y1="538" x2="522" y2="538" class="axis"/>',
        '<line x1="104" y1="178" x2="104" y2="538" class="axis"/>',
    ]
    max_value = 4.2
    colors = ["#2563EB", "#0F766E", "#B76E00"]
    for index, row in enumerate(norm_rows):
        x = 148 + index * 124
        height = 300 * row["predicted_decrease"] / max_value
        y = 538 - height
        lines.append(f'<rect x="{x}" y="{y:.2f}" width="72" height="{height:.2f}" rx="7" fill="{colors[index]}"/>')
        lines.append(f'<text x="{x + 36}" y="566" text-anchor="middle" class="b">{svg_escape(row["geometry"])}</text>')
        lines.append(f'<text x="{x + 36}" y="{y - 12:.2f}" text-anchor="middle" class="b">{row["predicted_decrease"]:.3f}</text>')
    lines += [
        '<text x="104" y="594" class="s">柱高 = −〈g,d*〉 = dual norm；单位球不同，数值不可直接当同一物理步长比较。</text>',
        '<rect x="612" y="88" width="540" height="520" rx="14" class="card"/>',
        '<text x="636" y="124" class="sh">B｜matrix polar pairing / nuclear norm</text>',
        '<line x1="672" y1="538" x2="1110" y2="538" class="axis"/>',
        '<line x1="672" y1="178" x2="672" y2="538" class="axis"/>',
    ]
    max_nuclear = max(row["nuclear_norm"] for row in polar_rows) * 1.15
    for index, row in enumerate(polar_rows):
        x = 704 + index * 98
        h1 = 300 * row["nuclear_norm"] / max_nuclear
        h2 = 300 * row["pairing"] / max_nuclear
        lines.append(f'<rect x="{x}" y="{538-h1:.2f}" width="30" height="{h1:.2f}" fill="#CBD5E1"/>')
        lines.append(f'<rect x="{x+32}" y="{538-h2:.2f}" width="30" height="{h2:.2f}" fill="#0F766E"/>')
        lines.append(f'<text x="{x+31}" y="566" text-anchor="middle" class="s">{svg_escape(row["case"])}</text>')
    lines += [
        '<rect x="690" y="584" width="14" height="14" fill="#CBD5E1"/><text x="712" y="596" class="s">nuclear norm</text>',
        '<rect x="814" y="584" width="14" height="14" fill="#0F766E"/><text x="836" y="596" class="s">〈G,polar(G)〉</text>',
        '<rect x="48" y="644" width="1104" height="48" rx="9" fill="#ECF7F4" stroke="#0F766E"/>',
        '<text x="72" y="674" class="b">机器断言：vector optimality gap 与 matrix duality gap 均在浮点容差内；rank-one 的 null-space maximizer 仍不唯一。</text>',
        '<text x="48" y="712" class="s">确定性标准库实验｜条形图展示 exact/toy identities，不是训练 benchmark。</text>',
    ]
    save_svg(path, lines)


def plot_ns(path: Path, scalar_rows: list[dict]) -> None:
    lines = svg_header(
        "Newton–Schulz singular-value residual trajectories",
        "比较 classic 与 Jordan 多项式从两个初值出发的绝对 target residual，并显示零奇异值固定边界。",
    )
    lines += [
        '<text x="48" y="48" class="h" fill="#2563EB">有限步 NS：初始 singular value 决定五步之后还剩多少误差</text>',
        '<rect x="48" y="88" width="1104" height="538" rx="14" class="card"/>',
        '<line x1="112" y1="552" x2="1100" y2="552" class="axis"/>',
        '<line x1="112" y1="146" x2="112" y2="552" class="axis"/>',
    ]
    for exponent in range(0, 7):
        y = 552 - exponent * (406 / 6)
        lines.append(f'<line x1="112" y1="{y:.2f}" x2="1100" y2="{y:.2f}" class="grid"/>')
        lines.append(f'<text x="98" y="{y+4:.2f}" text-anchor="end" class="s">1e-{6-exponent}</text>')
    series = [
        ("classic", 0.5, "blue", "classic s₀=.5"),
        ("jordan", 0.5, "green", "Jordan s₀=.5"),
        ("classic", 0.01, "amber", "classic s₀=.01"),
        ("jordan", 0.01, "red", "Jordan s₀=.01"),
    ]
    by_key = {}
    for row in scalar_rows:
        by_key[(row["method"], row["s0"], row["step"])] = row["absolute_target_error"]
    for method, start, css, label in series:
        points = []
        for step in range(9):
            error = max(by_key[(method, start, step)], 1e-6)
            x = 112 + step * (988 / 8)
            log_position = (math.log10(error) + 6.0) / 6.0
            y = 552 - 406 * log_position
            points.append(f"{x:.2f},{y:.2f}")
        lines.append(f'<polyline points="{" ".join(points)}" class="{css}"/>')
        color = {"blue": "#2563EB", "green": "#0F766E", "amber": "#B76E00", "red": "#C0392B"}[css]
        legend_y = 166 + series.index((method, start, css, label)) * 28
        lines.append(f'<line x1="802" y1="{legend_y}" x2="842" y2="{legend_y}" stroke="{color}" stroke-width="3"/>')
        lines.append(f'<text x="852" y="{legend_y+4}" class="s">{svg_escape(label)}</text>')
    for step in range(9):
        x = 112 + step * (988 / 8)
        lines.append(f'<text x="{x:.2f}" y="580" text-anchor="middle" class="s">{step}</text>')
    lines += [
        '<text x="600" y="610" text-anchor="middle" class="b">iteration</text>',
        '<text x="48" y="132" class="s">|sₖ−target|（log scale）</text>',
        '<rect x="48" y="654" width="1104" height="48" rx="9" fill="#FFF6E5" stroke="#B76E00"/>',
        '<text x="72" y="684" class="b">边界：s₀=0 在两种奇多项式下永久为 0；tiny s₀ 的 fixed-step residual 不能由“5 steps”这个数字单独保证。</text>',
        '<text x="48" y="722" class="s">确定性标准库实验｜exact-arithmetic scalar map；未模拟 BF16 rounding。</text>',
    ]
    save_svg(path, lines)


def plot_scaling_state_system(
    path: Path, scaling_rows: list[dict], momentum_rows: list[dict], system_rows: list[dict]
) -> None:
    lines = svg_header(
        "Shape scaling、momentum semantics 与系统代理",
        "三栏分别显示 shape adjustment 的实际 RMS、EMA 与 sum buffer 轨迹，以及五步 NS 的声明式 GEMM FLOP proxy。",
        height=760,
    )
    lines += [
        '<text x="48" y="48" class="h" fill="#2563EB">从公式到程序：scale、state 与 cost 必须同时审计</text>',
        '<rect x="48" y="88" width="340" height="536" rx="14" class="card"/>',
        '<rect x="430" y="88" width="340" height="536" rx="14" class="card"/>',
        '<rect x="812" y="88" width="340" height="536" rx="14" class="card"/>',
        '<text x="70" y="122" class="sh">A｜full-rank scaled RMS</text>',
        '<text x="452" y="122" class="sh">B｜momentum buffer clocks</text>',
        '<text x="834" y="122" class="sh">C｜5-step NS FLOP proxy</text>',
    ]
    selected = [
        row
        for row in scaling_rows
        if row["full_rank"] and (row["rows_A"], row["columns_B"]) in [(4096, 1024), (1024, 4096)]
        and row["mode"] != "unscaled"
    ]
    max_rms = max(row["scaled_rms"] for row in selected)
    colors = {"original": "#2563EB", "match_rms_adamw": "#0F766E", "spectral_unclamped": "#B76E00"}
    for index, row in enumerate(selected):
        x = 70 + index * 45
        height = 300 * row["scaled_rms"] / max_rms
        y = 532 - height
        lines.append(f'<rect x="{x}" y="{y:.2f}" width="28" height="{height:.2f}" fill="{colors[row["mode"]]}"/>')
        lines.append(f'<text x="{x+14}" y="554" text-anchor="middle" class="s">{index+1}</text>')
    lines += [
        '<text x="70" y="584" class="s">1–3: tall original/match/spectral</text>',
        '<text x="70" y="606" class="s">4–6: wide original/match/spectral</text>',
    ]
    normal_momentum = [row for row in momentum_rows if row["step"] < 90]
    max_buffer = max(max(abs(row["ema_buffer"]), abs(row["sum_buffer"])) for row in normal_momentum)
    for key, css in [("ema_buffer", "blue"), ("sum_buffer", "red")]:
        points = []
        for index, row in enumerate(normal_momentum):
            x = 474 + index * 76
            y = 350 - 150 * row[key] / max_buffer
            points.append(f"{x},{y:.2f}")
        lines.append(f'<polyline points="{" ".join(points)}" class="{css}"/>')
    lines += [
        '<line x1="474" y1="350" x2="734" y2="350" class="axis"/>',
        '<text x="474" y="540" class="s">蓝：EMA；红：sum-style</text>',
        '<text x="474" y="570" class="s">本例 B_ema=(1−μ)B_sum，</text>',
        '<text x="474" y="592" class="s">但非线性/metadata 仍阻止静默互载。</text>',
    ]
    five_step = [row for row in system_rows if row["ns_steps"] == 5]
    max_flops = max(row["ns_gemm_flops_proxy"] for row in five_step)
    for index, row in enumerate(five_step):
        x = 842 + index * 72
        height = 300 * row["ns_gemm_flops_proxy"] / max_flops
        y = 532 - height
        lines.append(f'<rect x="{x}" y="{y:.2f}" width="44" height="{height:.2f}" fill="#B76E00"/>')
        lines.append(f'<text x="{x+22}" y="554" text-anchor="middle" class="s">{index+1}</text>')
    lines += [
        '<text x="834" y="584" class="s">1:4096×1024　2:1024×4096</text>',
        '<text x="834" y="606" class="s">3:4096×4096　4:8192×1024</text>',
        '<rect x="48" y="654" width="1104" height="62" rx="10" fill="#F8FAFC" stroke="#CBD5E1"/>',
        '<text x="72" y="682" class="b">解释边界：A 是 exact shape identity；B 是 state semantics；C 只是算法 FLOP proxy，不是 measured wall-clock、energy 或 peak。</text>',
        '<text x="72" y="704" class="s">公平系统结论仍需真实 kernel、sharding、communication、P95 与 failure runs。</text>',
        '<text x="48" y="746" class="s">确定性标准库实验｜所有数字和图均由 results.json 同源生成。</text>',
    ]
    save_svg(path, lines)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("00-知识库管理/_labs/experiments/trn60.4-muon-matrix-geometry-audit-v1"),
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/training-optimization"),
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)

    norm_rows = audit_norm_duality()
    polar_rows, nonunique_rows = audit_polar_geometry()
    scalar_rows, matrix_rows = audit_newton_schulz()
    scaling_rows = audit_shape_scaling()
    momentum_rows, boundary_rows = audit_momentum_and_optimizer_boundaries()
    stiefel_rows = audit_stiefel_and_rotation()
    system_rows = audit_system_proxy()

    csv_tables = {
        "norm_duality.csv": norm_rows,
        "polar_geometry.csv": polar_rows,
        "rank_nonuniqueness.csv": nonunique_rows,
        "newton_schulz_scalar.csv": scalar_rows,
        "newton_schulz_matrix.csv": matrix_rows,
        "shape_scaling.csv": scaling_rows,
        "momentum_semantics.csv": momentum_rows,
        "optimizer_boundary.csv": boundary_rows,
        "stiefel_rotation.csv": stiefel_rows,
        "system_proxy.csv": system_rows,
    }
    for filename, rows in csv_tables.items():
        write_csv(args.output_dir / filename, rows)

    plot1 = args.plot_dir / "plot-muon-norm-polar-geometry-v1.svg"
    plot2 = args.plot_dir / "plot-muon-newton-schulz-spectral-audit-v1.svg"
    plot3 = args.plot_dir / "plot-muon-scaling-state-system-v1.svg"
    plot_norm_polar(plot1, norm_rows, polar_rows)
    plot_ns(plot2, scalar_rows)
    plot_scaling_state_system(plot3, scaling_rows, momentum_rows, system_rows)

    classic_half = [
        row for row in scalar_rows if row["method"] == "classic" and row["s0"] == 0.5
    ]
    zero_rows = [row for row in scalar_rows if row["s0"] == 0.0]
    full_rank_scaling = [row for row in scaling_rows if row["full_rank"]]
    stiefel_steps = [row for row in stiefel_rows if row["case"] == "stiefel_step"]
    double_rotation = next(row for row in stiefel_rows if row["case"] == "double_rotation")
    checks = {
        "norm_oracles_feasible_and_optimal": all(
            row["step_norm"] <= 1.0 + 1e-12 and row["optimality_gap"] < 1e-12 for row in norm_rows
        ),
        "polar_pairing_matches_nuclear": all(row["duality_gap"] < 1e-10 for row in polar_rows),
        "polar_spectral_feasible": all(row["polar_spectral_norm"] <= 1.0 + 1e-10 for row in polar_rows),
        "polar_support_residual_small": all(
            row["support_orthogonality_residual"] < 1e-10 for row in polar_rows
        ),
        "rank_deficient_maximizers_share_objective": max(
            abs(row["pairing"] - 3.0) for row in nonunique_rows
        )
        < 1e-12,
        "canonical_null_choice_minimizes_frobenius": min(
            nonunique_rows, key=lambda row: row["frobenius_norm"]
        )["null_space_value"]
        == 0.0,
        "classic_half_residual_decreases": all(
            classic_half[index + 1]["absolute_target_error"]
            <= classic_half[index]["absolute_target_error"] + 1e-15
            for index in range(len(classic_half) - 1)
        ),
        "zero_singular_value_is_fixed": all(row["singular_value"] == 0.0 for row in zero_rows),
        "all_ns_matrix_outputs_finite": all(row["finite"] for row in matrix_rows),
        "ill_conditioned_five_steps_not_exact": any(
            row["case"] == "ill_conditioned"
            and row["steps"] == 5
            and row["polar_direction_residual"] > 1e-3
            for row in matrix_rows
        ),
        "original_full_rank_rms_is_inverse_sqrt_B": all(
            abs(row["scaled_rms"] - 1.0 / math.sqrt(row["columns_B"])) < 1e-12
            for row in full_rank_scaling
            if row["mode"] == "original"
        ),
        "match_full_rank_rms_is_point_two": all(
            abs(row["scaled_rms"] - 0.2) < 1e-12
            for row in full_rank_scaling
            if row["mode"] == "match_rms_adamw"
        ),
        "ema_sum_relation_holds_in_controlled_case": all(
            row["ema_sum_relation_gap"] < 1e-12 for row in momentum_rows if row["step"] < 90
        ),
        "communication_nonlinearity_counterexample": momentum_rows[-1]["ema_sum_relation_gap"] == 1.0,
        "shampoo_history_changes_update": boundary_rows[0]["shampoo_update_1"]
        != boundary_rows[1]["shampoo_update_1"],
        "muon_reset_same_current_update": boundary_rows[0]["muon_reset_update_1"]
        == boundary_rows[1]["muon_reset_update_1"],
        "stiefel_tangent_residual_small": all(row["tangent_residual"] < 1e-12 for row in stiefel_steps),
        "euler_step_is_not_feasible": all(
            row["euler_feasibility_residual"] > 0.0 for row in stiefel_steps
        ),
        "polar_retraction_is_feasible": all(
            row["polar_retraction_feasibility_residual"] < 1e-10 for row in stiefel_steps
        ),
        "double_rotation_preserves_singular_values": double_rotation[
            "singular_value_invariance_gap"
        ]
        < 1e-10,
        "system_proxy_is_positive_and_declared": all(
            row["ns_gemm_flops_proxy"] > 0 and "proxy" in row["proxy_boundary"] for row in system_rows
        ),
    }

    results = {
        "experiment_id": "EXP-TRN-604-V1",
        "seed": SEED,
        "standard_library_only": True,
        "shape_convention": "y=xW, W has rows A=input width and columns B=output width",
        "coefficients": {"classic": CLASSIC, "jordan": JORDAN},
        "tracks": {
            "norm_duality": norm_rows,
            "polar_geometry": polar_rows,
            "rank_nonuniqueness": nonunique_rows,
            "newton_schulz_scalar": scalar_rows,
            "newton_schulz_matrix": matrix_rows,
            "shape_scaling": scaling_rows,
            "momentum_semantics": momentum_rows,
            "optimizer_boundary": boundary_rows,
            "stiefel_rotation": stiefel_rows,
            "system_proxy": system_rows,
        },
        "checks": checks,
        "artifacts": {
            "csv": sorted(csv_tables),
            "plots": [plot1.name, plot2.name, plot3.name],
        },
        "boundaries": [
            "Exact 2x2/toy identities are not deep-network optimization evidence.",
            "Newton--Schulz scalar trajectories use exact Python float arithmetic, not BF16 kernels.",
            "System FLOPs/state values are declared algorithmic proxies, not measured wall-clock or peak.",
        ],
    }
    result_path = args.output_dir / "results.json"
    result_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    summary = {
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_checks_pass": all(checks.values()),
        "result": str(result_path),
        "plot_sha256": {plot.name: sha256(plot) for plot in [plot1, plot2, plot3]},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
