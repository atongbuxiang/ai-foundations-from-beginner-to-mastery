#!/usr/bin/env python3
"""Deterministic, standard-library audit for TRN-17--TRN-24.

The experiment separates exact identities, estimator mismatches, structural
approximations and numerical/system diagnostics for Hessian/GGN/Fisher,
trust regions, HVP/CG, natural gradient, K-FAC, Shampoo and SOAP.  It writes
CSV/JSON evidence and three self-contained SVG plots; NumPy and ML frameworks
are deliberately not required.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


SEED = 20260826


def dot(x: list[float], y: list[float]) -> float:
    return sum(a * b for a, b in zip(x, y))


def norm(x: list[float]) -> float:
    return math.sqrt(dot(x, x))


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def matvec(a: list[list[float]], x: list[float]) -> list[float]:
    return [dot(row, x) for row in a]


def outer(x: list[float], y: list[float]) -> list[list[float]]:
    return [[a * b for b in y] for a in x]


def kron(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[aij * bij for aij in arow for bij in brow] for arow in a for brow in b]


def vec_col(a: list[list[float]]) -> list[float]:
    return [a[i][j] for j in range(len(a[0])) for i in range(len(a))]


def flatten(a: list[list[float]]) -> list[float]:
    return [x for row in a for x in row]


def matrix_difference_norm(a: list[list[float]], b: list[list[float]]) -> float:
    return norm([x - y for x, y in zip(flatten(a), flatten(b))])


def matrix_frobenius(a: list[list[float]]) -> float:
    return norm(flatten(a))


def diagonal(values: list[float]) -> list[list[float]]:
    return [[value if i == j else 0.0 for j in range(len(values))] for i, value in enumerate(values)]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def cosine(x: list[float], y: list[float]) -> float:
    return dot(x, y) / (norm(x) * norm(y))


def audit_curvature_objects() -> dict:
    decomposition_rows = []
    max_decomposition_error = 0.0
    for theta in [0.0, 0.25, 0.5, 1.0, 1.5]:
        ggn = 4.0 * theta * theta
        residual_term = 2.0 * (theta * theta - 1.0)
        hessian = 6.0 * theta * theta - 2.0
        error = abs(hessian - (ggn + residual_term))
        max_decomposition_error = max(max_decomposition_error, error)
        decomposition_rows.append(
            {
                "theta": theta,
                "GGN": ggn,
                "model_second_order_term": residual_term,
                "Hessian": hessian,
                "decomposition_error": error,
            }
        )

    p, x = 0.8, 2.0
    common = x * x * p * (1.0 - p)
    logistic_rows = []
    for label in [0, 1]:
        empirical = (x * (p - label)) ** 2
        logistic_rows.append(
            {
                "observed_label": label,
                "Hessian": common,
                "GGN": common,
                "true_Fisher": common,
                "empirical_Fisher": empirical,
            }
        )

    gaussian = {
        "theta": 2.0,
        "observed_y": 2.0,
        "Hessian": 1.0,
        "GGN": 1.0,
        "true_Fisher": 1.0,
        "empirical_Fisher": 0.0,
    }
    gradients = [1.0, -1.0]
    per_sample_second = sum(g * g for g in gradients) / len(gradients)
    outer_batch_mean = (sum(gradients) / len(gradients)) ** 2
    return {
        "decomposition_rows": decomposition_rows,
        "max_decomposition_error": max_decomposition_error,
        "logistic_rows": logistic_rows,
        "gaussian_optimum": gaussian,
        "reduction_counterexample": {
            "gradients": gradients,
            "mean_per_sample_outer": per_sample_second,
            "outer_batch_mean": outer_batch_mean,
        },
    }


def audit_trust_region_and_damping() -> dict:
    theta = 1.0
    old_loss = 0.25 * theta**4
    rows = []
    for damping in [0.0, 0.25, 1.0, 3.0, 10.0]:
        gradient = theta**3
        hessian = 3.0 * theta * theta
        step = -gradient / (hessian + damping)
        predicted = -(gradient * step + 0.5 * hessian * step * step)
        new_loss = 0.25 * (theta + step) ** 4
        actual = old_loss - new_loss
        rows.append(
            {
                "damping": damping,
                "step": step,
                "predicted_reduction": predicted,
                "actual_reduction": actual,
                "rho": actual / predicted,
            }
        )
    eigen_rows = []
    for mu in [-1.0, 0.1, 1.0, 10.0]:
        lam = 2.0
        eigen_rows.append(
            {
                "eigenvalue": mu,
                "damping": lam,
                "inverse_gain": 1.0 / (mu + lam),
                "regularized_positive": mu + lam > 0.0,
            }
        )
    return {"quartic_rows": rows, "eigenmode_rows": eigen_rows}


def cg_diagonal(diagonal_values: list[float], b: list[float]) -> list[dict]:
    x = [0.0] * len(b)
    r = b[:]
    direction = r[:]
    exact = [bi / ai for ai, bi in zip(diagonal_values, b)]
    rows = [
        {
            "iteration": 0,
            "residual_norm": norm(r),
            "solution_error_norm": norm([u - v for u, v in zip(x, exact)]),
        }
    ]
    rr = dot(r, r)
    for iteration in range(1, len(b) + 1):
        ad = [a * d for a, d in zip(diagonal_values, direction)]
        alpha = rr / dot(direction, ad)
        x = [u + alpha * d for u, d in zip(x, direction)]
        r = [u - alpha * v for u, v in zip(r, ad)]
        rr_new = dot(r, r)
        rows.append(
            {
                "iteration": iteration,
                "residual_norm": math.sqrt(max(rr_new, 0.0)),
                "solution_error_norm": norm([u - v for u, v in zip(x, exact)]),
            }
        )
        if rr_new < 1e-28:
            break
        beta = rr_new / rr
        direction = [u + beta * d for u, d in zip(r, direction)]
        rr = rr_new
    return rows


def audit_hvp_and_cg() -> dict:
    hessian = [[2.0, 1.0], [1.0, 4.0]]
    vector = [1.0, -1.0]
    hvp = matvec(hessian, vector)
    u = [2.0, 1.0]
    symmetry_gap = abs(dot(u, hvp) - dot(vector, matvec(hessian, u)))

    theta, direction = 0.7, 1.3
    exact_scalar_hvp = -math.sin(theta) * direction
    finite_rows = []
    for exponent in range(-1, -14, -1):
        h = 10.0**exponent
        estimate = (math.cos(theta + h * direction) - math.cos(theta)) / h
        finite_rows.append(
            {
                "h": h,
                "estimate": estimate,
                "exact_Hv": exact_scalar_hvp,
                "absolute_error": abs(estimate - exact_scalar_hvp),
            }
        )
    diagonal_values = [1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
    cg_rows = cg_diagonal(diagonal_values, [1.0] * len(diagonal_values))
    preconditioned_condition = max([1.0] * 6) / min([1.0] * 6)
    negative_direction = [0.0, 1.0]
    indefinite = [[1.0, 0.0], [0.0, -1.0]]
    negative_quadratic = dot(negative_direction, matvec(indefinite, negative_direction))
    return {
        "exact_hvp": hvp,
        "symmetry_gap": symmetry_gap,
        "finite_difference_rows": finite_rows,
        "cg_rows": cg_rows,
        "unpreconditioned_condition_number": 100.0,
        "exact_diagonal_preconditioned_condition_number": preconditioned_condition,
        "steihaug_negative_curvature": negative_quadratic,
    }


def audit_natural_gradient() -> dict:
    p = 0.8
    logit = math.log(p / (1.0 - p))
    grad_logit = p - 1.0
    fisher_logit = p * (1.0 - p)
    natural_logit = -grad_logit / fisher_logit
    grad_probability = -1.0 / p
    fisher_probability = 1.0 / (p * (1.0 - p))
    natural_probability = -grad_probability / fisher_probability
    tangent_from_logit = p * (1.0 - p) * natural_logit
    rows = []
    for eta in [1.0, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001]:
        endpoint_logit = sigmoid(logit + eta * natural_logit)
        endpoint_probability = p + eta * natural_probability
        rows.append(
            {
                "eta": eta,
                "endpoint_via_logit": endpoint_logit,
                "endpoint_via_probability": endpoint_probability,
                "endpoint_gap": abs(endpoint_logit - endpoint_probability),
                "gap_over_eta_squared": abs(endpoint_logit - endpoint_probability) / (eta * eta),
            }
        )
    return {
        "p": p,
        "grad_logit": grad_logit,
        "fisher_logit": fisher_logit,
        "natural_logit": natural_logit,
        "grad_probability": grad_probability,
        "fisher_probability": fisher_probability,
        "natural_probability": natural_probability,
        "tangent_from_logit": tangent_from_logit,
        "tangent_gap": abs(tangent_from_logit - natural_probability),
        "finite_step_rows": rows,
    }


def audit_kfac() -> dict:
    activation = [1.0, 2.0]
    backprop = [3.0, -1.0]
    gradient = outer(backprop, activation)
    vectorized = vec_col(gradient)
    exact_outer = outer(vectorized, vectorized)
    kronecker_outer = kron(outer(activation, activation), outer(backprop, backprop))
    sample_identity_error = matrix_difference_norm(exact_outer, kronecker_outer)

    exact_moment = (1.0 + 16.0) / 2.0
    factorized_moment = ((1.0 + 4.0) / 2.0) ** 2

    a_eigen = [4.0, 1.0]
    s_eigen = [9.0, 1.0]
    damping = 1.0
    exact_denominators = [a * s + damping for a in a_eigen for s in s_eigen]
    factored_denominators = [(a + 1.0) * (s + 1.0) for a in a_eigen for s in s_eigen]
    exact_step = [-1.0 / value for value in exact_denominators]
    factored_step = [-1.0 / value for value in factored_denominators]
    damping_rows = [
        {
            "mode": index,
            "exact_denominator": exact,
            "factored_denominator": factored,
            "exact_step": exact_step[index - 1],
            "factored_step": factored_step[index - 1],
        }
        for index, (exact, factored) in enumerate(zip(exact_denominators, factored_denominators), start=1)
    ]
    return {
        "sample_identity_error": sample_identity_error,
        "vectorized_gradient": vectorized,
        "exact_correlated_moment": exact_moment,
        "factorized_correlated_moment": factorized_moment,
        "factorization_gap": abs(exact_moment - factorized_moment),
        "damping_rows": damping_rows,
        "damped_step_cosine": cosine(exact_step, factored_step),
        "damped_step_relative_norm_gap": abs(norm(exact_step) - norm(factored_step)) / norm(exact_step),
    }


def audit_shampoo_and_soap() -> dict:
    left_root = [[0.5, 0.0], [0.0, 1.0]]
    right_root = [[1.0, 0.0], [0.0, 1.0 / 3.0]]
    gradient = [[1.0, 1.0], [1.0, 1.0]]
    shampoo_update = matmul(matmul(left_root, gradient), right_root)
    inverse_root_residual = matrix_difference_norm(
        matmul(matmul(matmul(left_root, left_root), left_root), left_root),
        [[1.0 / 16.0, 0.0], [0.0, 1.0]],
    )
    wrong_root = [[0.25, 0.0], [0.0, 1.0]]
    wrong_power_times_a = matmul(
        matmul(matmul(matmul(wrong_root, wrong_root), wrong_root), wrong_root),
        [[16.0, 0.0], [0.0, 1.0]],
    )
    wrong_residual = matrix_difference_norm(wrong_power_times_a, [[1.0, 0.0], [0.0, 1.0]])

    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    q = [[inv_sqrt2, inv_sqrt2], [inv_sqrt2, -inv_sqrt2]]
    original = [[2.0, 0.0], [0.0, 0.0]]
    rotated = matmul(matmul(transpose(q), original), q)
    roundtrip = matmul(matmul(q, rotated), transpose(q))
    rotation_roundtrip_error = matrix_difference_norm(original, roundtrip)
    rotation_norm_gap = abs(matrix_frobenius(original) - matrix_frobenius(rotated))

    g = [1.0, 0.0]
    rotated_g = matvec(transpose(q), g)
    normalized_rotated = [value / abs(value) for value in rotated_g]
    returned = matvec(q, normalized_rotated)
    original_normalized = [1.0, 0.0]
    nonlinear_equivariance_gap = norm([a - b for a, b in zip(returned, original_normalized)])

    old_second = [[1.0, 0.0], [0.0, 9.0]]
    transported_second = matmul(matmul(transpose(q), old_second), q)
    lost_offdiag_norm = math.sqrt(2.0 * transported_second[0][1] ** 2)
    return {
        "shampoo_update": shampoo_update,
        "inverse_root_residual": inverse_root_residual,
        "wrong_root_residual": wrong_residual,
        "soap_rotated_gradient": rotated,
        "rotation_roundtrip_error": rotation_roundtrip_error,
        "rotation_norm_gap": rotation_norm_gap,
        "elementwise_returned_update": returned,
        "nonlinear_equivariance_gap": nonlinear_equivariance_gap,
        "transported_second_moment": transported_second,
        "lost_offdiagonal_norm": lost_offdiag_norm,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def svg_header(title: str, desc: str, height: int = 700) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{title}</title>',
        f'<desc id="desc">{desc}</desc>',
        f'<rect width="1200" height="{height}" fill="#FFFEFB"/>',
        '<style>.sans{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif}.mono{font-family:"SFMono-Regular",Consolas,monospace}.ink{fill:#0F172A}.muted{fill:#64748B}.white{fill:#FFFFFF}.blue{fill:#2563EB}.teal{fill:#0F766E}.red{fill:#C0392B}.amber{fill:#B76E00}</style>',
    ]


def polyline(points: list[tuple[float, float]], color: str, dash: str = "") -> str:
    data = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{data}" fill="none" stroke="{color}" stroke-width="4"{dash_attr}/>'


def write_curvature_svg(path: Path, data: dict) -> None:
    logistic = data["logistic_rows"]
    gaussian = data["gaussian_optimum"]
    reduction = data["reduction_counterexample"]
    lines = svg_header(
        "曲率对象的三个反例数值审计",
        "非线性模型二阶项、标签测度与 reduction order 三类不等价的定量对照。",
    )
    lines += [
        '<text x="48" y="54" class="sans blue" font-size="26" font-weight="700">曲率对象不是同 shape 矩阵的同义词</text>',
        '<text x="48" y="92" class="sans muted" font-size="16">每个 panel 只删除一条错误等号；数值来自可复跑 toy model。</text>',
    ]
    panels = [(48, "A | nonlinear term", "theta=0", [("GGN", 0.0, "#0F766E"), ("Hessian", -2.0, "#C0392B")]),
              (420, "B | label measure", "logistic p=0.8, x=2", [("true F", logistic[0]["true_Fisher"], "#2563EB"), ("EF y=1", logistic[1]["empirical_Fisher"], "#0F766E"), ("EF y=0", logistic[0]["empirical_Fisher"], "#B76E00")]),
              (792, "C | reduction order", "per-sample g=+1,-1", [("mean outer", reduction["mean_per_sample_outer"], "#2563EB"), ("outer mean", reduction["outer_batch_mean"], "#C0392B")])]
    for x0, heading, subtitle, bars in panels:
        lines += [f'<rect x="{x0}" y="125" width="330" height="465" rx="14" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>',
                  f'<text x="{x0+24}" y="168" class="sans ink" font-size="21" font-weight="700">{heading}</text>',
                  f'<text x="{x0+24}" y="198" class="sans muted" font-size="15">{subtitle}</text>']
        baseline = 390.0
        for index, (label, value, color) in enumerate(bars):
            bx = x0 + 35 + index * (250.0 / max(len(bars), 1))
            bh = min(200.0, abs(value) * 80.0)
            by = baseline - bh if value >= 0 else baseline
            value_y = by - 10.0 if value >= 0 else by + bh - 12.0
            value_class = "mono ink" if value >= 0 else "mono white"
            lines += [f'<rect x="{bx:.1f}" y="{by:.1f}" width="55" height="{bh:.1f}" fill="{color}" opacity="0.88"/>',
                      f'<text x="{bx+27.5:.1f}" y="565" class="sans ink" font-size="15" text-anchor="middle">{label}</text>',
                      f'<text x="{bx+27.5:.1f}" y="{value_y:.1f}" class="{value_class}" font-size="16" text-anchor="middle">{value:g}</text>']
        lines.append(f'<line x1="{x0+24}" y1="{baseline}" x2="{x0+306}" y2="{baseline}" stroke="#94A3B8" stroke-width="2"/>')
    lines += [
        f'<text x="48" y="638" class="sans red" font-size="17">Gaussian optimum: empirical Fisher={gaussian["empirical_Fisher"]:g}, true Fisher=Hessian={gaussian["true_Fisher"]:g}.</text>',
        '<text x="48" y="670" class="sans muted" font-size="15">PSD、样本更多或变量名都不能修复对象、测度与 reduction 的错配。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_hvp_cg_svg(path: Path, hvp: dict, trust: dict) -> None:
    lines = svg_header(
        "HVP、有限差分、CG 与阻尼数值审计",
        "左侧展示 finite-difference HVP 的 U 型误差，中间展示 CG residual 与 solution error，右侧展示 quartic model 的 damping 与 rho。",
    )
    lines += [
        '<text x="48" y="54" class="sans blue" font-size="25" font-weight="700">Matrix-free 二阶步仍需三类数值证书</text>',
        '<text x="48" y="92" class="sans muted" font-size="16">finite difference 只作诊断；CG residual 与 solution error 分开；rho 检验 local model。</text>',
    ]
    # Panel A: finite-difference error on log axes.
    x0, y0, w, h = 70.0, 520.0, 300.0, 310.0
    finite = hvp["finite_difference_rows"]
    finite_points = []
    logs = [math.log10(max(row["absolute_error"], 1e-18)) for row in finite]
    lo, hi = min(logs), max(logs)
    for index, (row, value) in enumerate(zip(finite, logs)):
        x = x0 + index / (len(finite) - 1) * w
        y = y0 - (value - lo) / (hi - lo) * h
        finite_points.append((x, y))
    lines += ['<text x="58" y="145" class="sans teal" font-size="21" font-weight="700">A | finite-difference U curve</text>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="#334155" stroke-width="2"/>',
              f'<line x1="{x0}" y1="{y0-h}" x2="{x0}" y2="{y0}" stroke="#334155" stroke-width="2"/>',
              polyline(finite_points, "#C0392B"),
              '<text x="220" y="557" class="sans muted" font-size="15" text-anchor="middle">h: 1e-1 → 1e-13</text>']
    # Panel B: CG curves, log1p scale to include zero.
    x1, w1 = 455.0, 300.0
    cg = hvp["cg_rows"]
    max_log = max(math.log10(1.0 + row["residual_norm"]) for row in cg)
    residual_points, error_points = [], []
    for row in cg:
        x = x1 + row["iteration"] / max(cg[-1]["iteration"], 1) * w1
        residual_points.append((x, y0 - math.log10(1.0 + row["residual_norm"]) / max_log * h))
        error_points.append((x, y0 - math.log10(1.0 + row["solution_error_norm"]) / max_log * h))
    lines += ['<text x="430" y="145" class="sans teal" font-size="21" font-weight="700">B | CG: residual vs error</text>',
              f'<line x1="{x1}" y1="{y0}" x2="{x1+w1}" y2="{y0}" stroke="#334155" stroke-width="2"/>',
              f'<line x1="{x1}" y1="{y0-h}" x2="{x1}" y2="{y0}" stroke="#334155" stroke-width="2"/>',
              polyline(residual_points, "#2563EB"), polyline(error_points, "#B76E00", "8 6"),
              '<text x="605" y="557" class="sans muted" font-size="15" text-anchor="middle">CG iteration; kappa=100</text>',
              '<line x1="490" y1="180" x2="530" y2="180" stroke="#2563EB" stroke-width="4"/><text x="540" y="186" class="sans ink" font-size="15">residual</text>',
              '<line x1="625" y1="180" x2="665" y2="180" stroke="#B76E00" stroke-width="4" stroke-dasharray="8 6"/><text x="675" y="186" class="sans ink" font-size="15">error</text>']
    # Panel C: damping table.
    lines += ['<text x="805" y="145" class="sans teal" font-size="21" font-weight="700">C | damping and model ratio</text>',
              '<rect x="800" y="170" width="350" height="350" rx="12" fill="#FFF6E5" stroke="#B76E00" stroke-width="2"/>',
              '<text x="824" y="207" class="mono ink" font-size="16">lambda    step      rho</text>']
    for index, row in enumerate(trust["quartic_rows"]):
        lines.append(f'<text x="824" y="{245+index*48}" class="mono ink" font-size="16">{row["damping"]:5.2f}   {row["step"]:8.4f}   {row["rho"]:7.4f}</text>')
    lines += ['<text x="824" y="495" class="sans red" font-size="15">damping changes step; rho tests the model.</text>',
              '<text x="48" y="638" class="sans muted" font-size="15">Steihaug negative-curvature certificate: d^T B d = -1；这不是 residual convergence。</text>',
              '</svg>']
    path.write_text("\n".join(lines), encoding="utf-8")


def write_structure_svg(path: Path, kfac: dict, shampoo: dict) -> None:
    lines = svg_header(
        "K-FAC、Shampoo 与 SOAP 结构近似审计",
        "K-FAC moment/damping bias、Shampoo inverse-root residual 与 SOAP basis-state nonlinear gap 的并列证据。",
    )
    metrics = [
        ("K-FAC moment gap", kfac["factorization_gap"], "#B76E00"),
        ("factored step norm gap", kfac["damped_step_relative_norm_gap"], "#C0392B"),
        ("correct root residual", shampoo["inverse_root_residual"], "#0F766E"),
        ("wrong root residual", shampoo["wrong_root_residual"], "#C0392B"),
        ("SOAP nonlinear gap", shampoo["nonlinear_equivariance_gap"], "#2563EB"),
        ("lost offdiag norm", shampoo["lost_offdiagonal_norm"], "#B76E00"),
    ]
    max_value = max(value for _, value, _ in metrics)
    lines += [
        '<text x="48" y="54" class="sans blue" font-size="25" font-weight="700">结构化 optimizer 的误差来自不同接口</text>',
        '<text x="48" y="92" class="sans muted" font-size="16">同一柱图尺度用于定位量级，不表示六个指标具有相同单位或可直接排名。</text>',
        '<line x1="88" y1="535" x2="1140" y2="535" stroke="#334155" stroke-width="2"/>',
    ]
    bar_width = 105.0
    for index, (label, value, color) in enumerate(metrics):
        x = 105.0 + index * 172.0
        height = 330.0 * value / max_value if max_value else 0.0
        lines += [f'<rect x="{x}" y="{535-height:.2f}" width="{bar_width}" height="{height:.2f}" fill="{color}" opacity="0.88"/>',
                  f'<text x="{x+bar_width/2}" y="{515-height:.2f}" class="mono ink" font-size="16" text-anchor="middle">{value:.4g}</text>',
                  f'<text x="{x+bar_width/2}" y="570" class="sans ink" font-size="15" text-anchor="middle">{label}</text>']
    lines += [
        '<rect x="70" y="615" width="1060" height="54" rx="10" fill="#F8FAFC" stroke="#CBD5E1"/>',
        '<text x="92" y="648" class="sans muted" font-size="15">exact sample identity = 0；correct inverse-root residual = 0；其余非零量分别来自 statistical factorization、damping 或 basis-state nonlinear operation。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("00-知识库管理/_labs/experiments/trn60.3-curvature-preconditioners-audit-v1"),
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/training-optimization"),
    )
    args = parser.parse_args()

    curvature = audit_curvature_objects()
    trust = audit_trust_region_and_damping()
    hvp = audit_hvp_and_cg()
    natural = audit_natural_gradient()
    kfac = audit_kfac()
    matrix_methods = audit_shampoo_and_soap()
    result = {
        "seed": SEED,
        "curvature_objects": curvature,
        "trust_region_and_damping": trust,
        "hvp_and_cg": hvp,
        "natural_gradient": natural,
        "kfac": kfac,
        "shampoo_and_soap": matrix_methods,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_csv(args.output_dir / "curvature_decomposition.csv", curvature["decomposition_rows"])
    write_csv(args.output_dir / "logistic_label_measure.csv", curvature["logistic_rows"])
    write_csv(args.output_dir / "trust_region_damping.csv", trust["quartic_rows"])
    write_csv(args.output_dir / "hvp_finite_difference.csv", hvp["finite_difference_rows"])
    write_csv(args.output_dir / "cg_conditioning.csv", hvp["cg_rows"])
    write_csv(args.output_dir / "natural_gradient_coordinates.csv", natural["finite_step_rows"])
    write_csv(args.output_dir / "kfac_damping.csv", kfac["damping_rows"])
    write_csv(
        args.output_dir / "matrix_root_basis.csv",
        [
            {"metric": "correct_inverse_root_residual", "value": matrix_methods["inverse_root_residual"]},
            {"metric": "wrong_inverse_root_residual", "value": matrix_methods["wrong_root_residual"]},
            {"metric": "rotation_roundtrip_error", "value": matrix_methods["rotation_roundtrip_error"]},
            {"metric": "rotation_norm_gap", "value": matrix_methods["rotation_norm_gap"]},
            {"metric": "nonlinear_equivariance_gap", "value": matrix_methods["nonlinear_equivariance_gap"]},
            {"metric": "lost_offdiagonal_norm", "value": matrix_methods["lost_offdiagonal_norm"]},
        ],
    )

    write_curvature_svg(args.plot_dir / "plot-curvature-object-counterexamples-v1.svg", curvature)
    write_hvp_cg_svg(args.plot_dir / "plot-hvp-cg-trust-region-audit-v1.svg", hvp, trust)
    write_structure_svg(args.plot_dir / "plot-kfac-shampoo-soap-approximation-v1.svg", kfac, matrix_methods)

    finite_errors = [row["absolute_error"] for row in hvp["finite_difference_rows"]]
    endpoint_rows = natural["finite_step_rows"]
    checks = {
        "hessian_decomposition_exact": curvature["max_decomposition_error"] < 1e-14,
        "ggn_misses_negative_curvature": curvature["decomposition_rows"][0]["GGN"] == 0.0 and curvature["decomposition_rows"][0]["Hessian"] < 0.0,
        "logistic_label_measure_mismatch": abs(curvature["logistic_rows"][0]["empirical_Fisher"] - curvature["logistic_rows"][1]["empirical_Fisher"]) > 2.0,
        "gaussian_empirical_fisher_collapses": curvature["gaussian_optimum"]["empirical_Fisher"] == 0.0 and curvature["gaussian_optimum"]["true_Fisher"] == 1.0,
        "reduction_order_counterexample": curvature["reduction_counterexample"]["mean_per_sample_outer"] == 1.0 and curvature["reduction_counterexample"]["outer_batch_mean"] == 0.0,
        "trust_model_ratios_positive": all(row["rho"] > 0.0 for row in trust["quartic_rows"]),
        "hvp_bilinear_symmetry": hvp["symmetry_gap"] < 1e-14,
        "finite_difference_has_interior_best_scale": 0 < finite_errors.index(min(finite_errors)) < len(finite_errors) - 1,
        "cg_reaches_small_error": hvp["cg_rows"][-1]["solution_error_norm"] < 1e-10,
        "steihaug_detects_negative_curvature": hvp["steihaug_negative_curvature"] < 0.0,
        "natural_tangent_invariant": natural["tangent_gap"] < 1e-14,
        "natural_finite_gap_shrinks": endpoint_rows[-1]["endpoint_gap"] < endpoint_rows[0]["endpoint_gap"] * 1e-4,
        "kfac_sample_identity_exact": kfac["sample_identity_error"] < 1e-14,
        "kfac_factorization_and_damping_are_approximate": kfac["factorization_gap"] > 2.0 and kfac["damped_step_relative_norm_gap"] > 0.3,
        "shampoo_correct_root_and_wrong_exponent_separated": matrix_methods["inverse_root_residual"] < 1e-14 and matrix_methods["wrong_root_residual"] > 0.9,
        "soap_rotation_exact_but_nonlinearity_not": matrix_methods["rotation_roundtrip_error"] < 1e-14 and matrix_methods["rotation_norm_gap"] < 1e-14 and matrix_methods["nonlinear_equivariance_gap"] > 0.4,
    }
    print(json.dumps({"checks": checks, "output_dir": str(args.output_dir), "plot_dir": str(args.plot_dir)}, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
