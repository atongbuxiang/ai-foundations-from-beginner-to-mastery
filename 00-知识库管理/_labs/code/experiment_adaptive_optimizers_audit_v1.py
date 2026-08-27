#!/usr/bin/env python3
"""Standard-library numerical audit for TRN-09--TRN-16.

The script separates exact identities, controlled counterexamples and
mean-field/statistical approximations for AdaGrad, RMSProp, Adam/AMSGrad,
AdamW and Adafactor. It emits deterministic tables plus three self-contained
SVG plots. No NumPy, plotting library, ML framework or network is required.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path


SEED = 20260826


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def rms(xs: list[float]) -> float:
    return math.sqrt(mean([x * x for x in xs]))


def adagrad_directions(gradients: list[float], epsilon: float = 0.0) -> list[float]:
    accumulator = 0.0
    directions = []
    for gradient in gradients:
        accumulator += gradient * gradient
        directions.append(gradient / (math.sqrt(accumulator) + epsilon))
    return directions


def audit_adagrad_scale() -> dict:
    base = [1.0, -2.0, 0.5, 3.0]
    scale = 7.0
    base_directions = adagrad_directions(base)
    globally_scaled = adagrad_directions([scale * x for x in base])
    exact_errors = [abs(x - y) for x, y in zip(base_directions, globally_scaled)]

    baseline = adagrad_directions([1.0, 1.0, 1.0, 1.0])
    scale_switch = adagrad_directions([1.0, 1.0, 10.0, 10.0])
    globally_ten = adagrad_directions([10.0, 10.0, 10.0, 10.0])
    rows = []
    for index in range(4):
        rows.append(
            {
                "step": index + 1,
                "baseline": baseline[index],
                "global_scale_10": globally_ten[index],
                "midrun_scale_switch": scale_switch[index],
            }
        )
    return {
        "global_scale": scale,
        "base_gradients": base,
        "base_directions": base_directions,
        "globally_scaled_directions": globally_scaled,
        "max_exact_error": max(exact_errors),
        "midrun_rows": rows,
        "step3_switch_gap": abs(scale_switch[2] - baseline[2]),
    }


def audit_rmsprop_response(rho: float = 0.9, old_square: float = 1.0, new_square: float = 9.0) -> dict:
    value = old_square
    rows = []
    max_error = 0.0
    for step in range(1, 61):
        value = rho * value + (1.0 - rho) * new_square
        analytic = new_square + (rho**step) * (old_square - new_square)
        error = abs(value - analytic)
        max_error = max(max_error, error)
        rows.append(
            {
                "step_after_switch": step,
                "recursive_v": value,
                "analytic_v": analytic,
                "absolute_error": error,
                "remaining_fraction": (new_square - value) / (new_square - old_square),
            }
        )
    half_life = math.log(0.5) / math.log(rho)
    e_fold = -1.0 / math.log(rho)
    effective_n = (1.0 + rho) / (1.0 - rho)
    return {
        "rho": rho,
        "old_square": old_square,
        "new_square": new_square,
        "half_life": half_life,
        "e_fold": e_fold,
        "effective_sample_size": effective_n,
        "max_recursion_error": max_error,
        "rows": rows,
    }


def adam_states(gradients: list[float], beta1: float, beta2: float, epsilon: float = 0.0) -> list[dict]:
    first = 0.0
    second = 0.0
    rows = []
    for step, gradient in enumerate(gradients, start=1):
        first = beta1 * first + (1.0 - beta1) * gradient
        second = beta2 * second + (1.0 - beta2) * gradient * gradient
        first_hat = first / (1.0 - beta1**step)
        second_hat = second / (1.0 - beta2**step)
        direction = first_hat / (math.sqrt(second_hat) + epsilon)
        rows.append(
            {
                "step": step,
                "gradient": gradient,
                "m": first,
                "v": second,
                "m_hat": first_hat,
                "v_hat": second_hat,
                "direction": direction,
            }
        )
    return rows


def audit_adam_bias(rng: random.Random, repeats: int = 50000) -> dict:
    constant_rows = adam_states([2.0] * 12, beta1=0.9, beta2=0.999)
    constant_m_error = max(abs(row["m_hat"] - 2.0) for row in constant_rows)
    constant_v_error = max(abs(row["v_hat"] - 4.0) for row in constant_rows)
    constant_direction_error = max(abs(row["direction"] - 1.0) for row in constant_rows)

    # One-step distribution: g is -1 or +3 with equal probability.
    # m_hat=g and v_hat=g^2 are unbiased for their population moments, while
    # E[m_hat/sqrt(v_hat)] = E[sign(g)] = 0, not mu/sqrt(nu)=1/sqrt(5).
    samples = [-1.0 if rng.random() < 0.5 else 3.0 for _ in range(repeats)]
    empirical_m = mean(samples)
    empirical_v = mean([x * x for x in samples])
    empirical_ratio = mean([x / abs(x) for x in samples])
    population_mu = 1.0
    population_nu = 5.0
    ratio_of_moments = population_mu / math.sqrt(population_nu)
    return {
        "constant_gradient": {
            "rows": constant_rows,
            "max_m_hat_error": constant_m_error,
            "max_v_hat_error": constant_v_error,
            "max_direction_error": constant_direction_error,
        },
        "ratio_counterexample": {
            "repeats": repeats,
            "distribution": {"-1": 0.5, "3": 0.5},
            "population_mu": population_mu,
            "population_second_moment": population_nu,
            "empirical_m_hat_mean": empirical_m,
            "empirical_v_hat_mean": empirical_v,
            "empirical_mean_ratio": empirical_ratio,
            "ratio_of_population_moments": ratio_of_moments,
            "gap": abs(empirical_ratio - ratio_of_moments),
        },
    }


def audit_epsilon() -> dict:
    epsilon_out = 1e-8
    epsilon_in = epsilon_out * epsilon_out
    rows = []
    for exponent in range(-14, 3):
        root_v = 10.0**exponent
        v = root_v * root_v
        m = root_v
        root_out = m / (root_v + epsilon_out)
        root_in_matched = m / math.sqrt(v + epsilon_in)
        root_in_same_literal = m / math.sqrt(v + epsilon_out)
        rows.append(
            {
                "log10_sqrt_v": exponent,
                "sqrt_v": root_v,
                "root_out_eps_1e-8": root_out,
                "root_in_eps_1e-16": root_in_matched,
                "root_in_same_literal_1e-8": root_in_same_literal,
                "epsilon_over_sqrt_v": epsilon_out / root_v,
            }
        )

    m = 2e-7
    root_v = 3e-9
    c = 100.0
    original = m / (root_v + epsilon_out)
    scaled = c * m / (c * root_v + epsilon_out)
    predicted_ratio = (root_v + epsilon_out) / (root_v + epsilon_out / c)
    return {
        "epsilon_out": epsilon_out,
        "epsilon_in_zero_scale_matched": epsilon_in,
        "rows": rows,
        "scale_break": {
            "m": m,
            "sqrt_v": root_v,
            "scale": c,
            "original_direction": original,
            "scaled_direction": scaled,
            "observed_ratio": scaled / original,
            "predicted_ratio": predicted_ratio,
            "ratio_error": abs(scaled / original - predicted_ratio),
        },
    }


def project_unit_interval(x: float) -> float:
    return max(-1.0, min(1.0, x))


def audit_adam_amsgrad_counterexample(steps: int = 12000) -> dict:
    c = 4.0
    beta2 = 1.0 / (1.0 + c * c)
    alpha = 0.5
    adam_x = 0.0
    amsgrad_x = 0.0
    adam_v = 0.0
    amsgrad_raw_v = 0.0
    amsgrad_max_v = 0.0
    adam_cumulative_loss = 0.0
    amsgrad_cumulative_loss = 0.0
    best_cumulative_loss = 0.0
    rows = []
    for step in range(1, steps + 1):
        gradient = c if step % 3 == 1 else -1.0
        lr = alpha / step
        adam_cumulative_loss += gradient * adam_x
        amsgrad_cumulative_loss += gradient * amsgrad_x
        best_cumulative_loss += gradient * (-1.0)

        adam_v = beta2 * adam_v + (1.0 - beta2) * gradient * gradient
        amsgrad_raw_v = beta2 * amsgrad_raw_v + (1.0 - beta2) * gradient * gradient
        amsgrad_max_v = max(amsgrad_max_v, amsgrad_raw_v)
        adam_x = project_unit_interval(adam_x - lr * gradient / math.sqrt(adam_v))
        amsgrad_x = project_unit_interval(
            amsgrad_x - lr * gradient / math.sqrt(amsgrad_max_v)
        )
        if step <= 30 or step % 60 == 0 or step == steps:
            rows.append(
                {
                    "step": step,
                    "adam_x": adam_x,
                    "amsgrad_x": amsgrad_x,
                    "adam_v": adam_v,
                    "amsgrad_max_v": amsgrad_max_v,
                    "adam_regret": adam_cumulative_loss - best_cumulative_loss,
                    "amsgrad_regret": amsgrad_cumulative_loss - best_cumulative_loss,
                }
            )
    return {
        "C": c,
        "beta1": 0.0,
        "beta2": beta2,
        "alpha_t": "0.5/t",
        "domain": [-1.0, 1.0],
        "steps": steps,
        "best_fixed_comparator": -1.0,
        "cycle_slope": c - 2.0,
        "final_adam_x": adam_x,
        "final_amsgrad_x": amsgrad_x,
        "final_adam_regret": adam_cumulative_loss - best_cumulative_loss,
        "final_amsgrad_regret": amsgrad_cumulative_loss - best_cumulative_loss,
        "rows": rows,
    }


def audit_decay_paths() -> dict:
    theta = [1.0, 1.0]
    preconditioner = [1.0, 0.1]
    eta = 0.1
    decay = 0.2
    coupled = [
        theta[i] - eta * preconditioner[i] * decay * theta[i] for i in range(2)
    ]
    adamw = [(1.0 - eta * decay) * x for x in theta]
    lrs = [0.1, 0.05, 0.01]
    exact_multiplier = math.prod([1.0 - lr * decay for lr in lrs])
    exponential = math.exp(-decay * sum(lrs))
    return {
        "theta": theta,
        "preconditioner_diagonal": preconditioner,
        "eta": eta,
        "lambda": decay,
        "coupled_after": coupled,
        "adamw_after": adamw,
        "anisotropy_gap": abs((coupled[0] - theta[0]) - (coupled[1] - theta[1])),
        "schedule_lrs": lrs,
        "exact_cumulative_multiplier": exact_multiplier,
        "exponential_approximation": exponential,
        "approximation_error": abs(exact_multiplier - exponential),
    }


def audit_update_rms(rng: random.Random, steps: int = 140000, burn_in: int = 20000) -> dict:
    rows = []
    for beta1 in [0.0, 0.9, 0.99]:
        first = 0.0
        second = 0.0
        beta2 = 0.999
        sum_square = 0.0
        count = 0
        for step in range(1, steps + 1):
            gradient = rng.gauss(0.0, 1.0)
            first = beta1 * first + (1.0 - beta1) * gradient
            second = beta2 * second + (1.0 - beta2) * gradient * gradient
            if step > burn_in:
                direction = first / math.sqrt(second)
                sum_square += direction * direction
                count += 1
        empirical = math.sqrt(sum_square / count)
        theory = math.sqrt((1.0 - beta1) / (1.0 + beta1))
        rows.append(
            {
                "beta1": beta1,
                "beta2": beta2,
                "empirical_direction_rms": empirical,
                "mean_field_theory": theory,
                "relative_error": abs(empirical - theory) / theory,
            }
        )
    return {"steps": steps, "burn_in": burn_in, "rows": rows}


def audit_weight_rms(rng: random.Random, paths: int = 1200, steps: int = 7000) -> dict:
    eta = 0.01
    decay = 0.1
    contraction = 1.0 - eta * decay
    states = [0.0] * paths
    for _ in range(steps):
        for index in range(paths):
            noise = 1.0 if rng.random() < 0.5 else -1.0
            states[index] = contraction * states[index] - eta * noise
    empirical = rms(states)
    exact = math.sqrt(eta / (2.0 * decay - eta * decay * decay))
    approximation = math.sqrt(eta / (2.0 * decay))

    sweep = []
    for sweep_eta, sweep_decay in [
        (0.0025, 0.1),
        (0.005, 0.1),
        (0.01, 0.1),
        (0.02, 0.1),
        (0.01, 0.05),
        (0.01, 0.2),
    ]:
        sweep.append(
            {
                "eta": sweep_eta,
                "lambda": sweep_decay,
                "exact_stationary_rms": math.sqrt(
                    sweep_eta / (2.0 * sweep_decay - sweep_eta * sweep_decay * sweep_decay)
                ),
                "small_step_approximation": math.sqrt(sweep_eta / (2.0 * sweep_decay)),
            }
        )
    return {
        "monte_carlo": {
            "paths": paths,
            "steps": steps,
            "eta": eta,
            "lambda": decay,
            "empirical_rms": empirical,
            "exact_stationary_rms": exact,
            "small_step_approximation": approximation,
            "relative_error_to_exact": abs(empirical - exact) / exact,
        },
        "analytic_sweep": sweep,
    }


def factor_reconstruct(matrix: list[list[float]]) -> tuple[list[float], list[float], list[list[float]]]:
    row_sums = [sum(row) for row in matrix]
    column_sums = [sum(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))]
    total = sum(row_sums)
    reconstruction = [
        [row_sums[i] * column_sums[j] / total for j in range(len(column_sums))]
        for i in range(len(row_sums))
    ]
    return row_sums, column_sums, reconstruction


def audit_adafactor() -> dict:
    cases = {
        "rank_one": [[1.0, 3.0], [2.0, 6.0]],
        "identity": [[1.0, 0.0], [0.0, 1.0]],
        "general": [[1.0, 4.0, 2.0], [3.0, 1.0, 5.0]],
    }
    results = []
    for name, matrix in cases.items():
        row_sums, column_sums, reconstruction = factor_reconstruct(matrix)
        reconstructed_rows = [sum(row) for row in reconstruction]
        reconstructed_columns = [
            sum(reconstruction[i][j] for i in range(len(reconstruction)))
            for j in range(len(reconstruction[0]))
        ]
        element_error = math.sqrt(
            mean(
                [
                    (matrix[i][j] - reconstruction[i][j]) ** 2
                    for i in range(len(matrix))
                    for j in range(len(matrix[0]))
                ]
            )
        )
        results.append(
            {
                "case": name,
                "matrix": matrix,
                "row_sums": row_sums,
                "column_sums": column_sums,
                "reconstruction": reconstruction,
                "max_row_marginal_error": max(
                    abs(x - y) for x, y in zip(row_sums, reconstructed_rows)
                ),
                "max_column_marginal_error": max(
                    abs(x - y) for x, y in zip(column_sums, reconstructed_columns)
                ),
                "element_rms_error": element_error,
            }
        )
    n = 4096
    m = 4096
    return {
        "cases": results,
        "state_ledger": {
            "shape": [n, m],
            "elements": n * m,
            "adam_two_moments_fp32_bytes": 2 * n * m * 4,
            "adafactor_row_column_fp32_bytes": (n + m) * 4,
            "ideal_ratio": 2 * n * m / (n + m),
        },
    }


SVG_STYLE = """<style>
.sans{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}
.ink{fill:#1F2937}.muted{fill:#64748B}.blue{fill:#2563EB}.green{fill:#0F766E}.amber{fill:#B7791F}.red{fill:#C24135}
</style>"""


def svg_header(title: str, desc: str, height: int = 640) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{title}</title>',
        f'<desc id="desc">{desc}</desc>',
        f'<rect width="1200" height="{height}" fill="#FFFEFB"/>',
        SVG_STYLE,
    ]


def polyline(points: list[tuple[float, float]], color: str, width: int = 4, dash: str = "") -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attr}/>'


def write_epsilon_svg(path: Path, data: dict) -> None:
    rows = data["rows"]
    lines = svg_header(
        "Adam epsilon 位置与工作区间",
        "横轴为二阶矩平方根的十进对数，比较 root-out、零点尺度匹配的 root-in 与同字面 epsilon 的 root-in 响应。",
    )
    x0, y0, width, height = 105.0, 505.0, 980.0, 360.0
    lines += [
        '<text x="58" y="56" class="sans blue" font-size="23" font-weight="700">Epsilon response：m = sqrt(v)</text>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0+width}" y2="{y0}" stroke="#1F2937" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-height}" stroke="#1F2937" stroke-width="2"/>',
    ]
    series = [
        ("root_out_eps_1e-8", "#2563EB"),
        ("root_in_eps_1e-16", "#0F766E"),
        ("root_in_same_literal_1e-8", "#C24135"),
    ]
    lo, hi = rows[0]["log10_sqrt_v"], rows[-1]["log10_sqrt_v"]
    for key, color in series:
        points = []
        for row in rows:
            x = x0 + (row["log10_sqrt_v"] - lo) / (hi - lo) * width
            y = y0 - min(1.0, row[key]) * height
            points.append((x, y))
        lines.append(polyline(points, color))
    epsilon_x = x0 + (-8 - lo) / (hi - lo) * width
    lines += [
        f'<line x1="{epsilon_x:.2f}" y1="{y0}" x2="{epsilon_x:.2f}" y2="{y0-height}" stroke="#B7791F" stroke-width="2" stroke-dasharray="7 6"/>',
        '<line x1="670" y1="82" x2="712" y2="82" stroke="#2563EB" stroke-width="4"/><text x="722" y="88" class="sans ink" font-size="16">root-out eps=1e-8</text>',
        '<line x1="670" y1="112" x2="712" y2="112" stroke="#0F766E" stroke-width="4"/><text x="722" y="118" class="sans ink" font-size="16">root-in eps=1e-16</text>',
        '<line x1="940" y1="82" x2="982" y2="82" stroke="#C24135" stroke-width="4"/><text x="992" y="88" class="sans ink" font-size="16">root-in eps=1e-8</text>',
        '<text x="595" y="556" class="sans ink" font-size="17" text-anchor="middle">log10 sqrt(v)</text>',
        '<text x="34" y="325" class="sans ink" font-size="17" text-anchor="middle" transform="rotate(-90 34 325)">normalized direction</text>',
        '<text x="58" y="607" class="sans muted" font-size="16">绿线只匹配 v→0 的 denominator 尺度；它与蓝线在中间区仍不是同一函数。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_counterexample_svg(path: Path, data: dict) -> None:
    rows = data["rows"]
    lines = svg_header(
        "三周期凸反例中的 Adam 与 AMSGrad 轨迹",
        "在区间负一到一上使用斜率四、负一、负一的周期损失和 alpha 除以 t 步长，比较两个投影迭代。",
    )
    x0, y0, width, height = 105.0, 505.0, 980.0, 360.0
    lines += [
        '<text x="58" y="56" class="sans blue" font-size="23" font-weight="700">Reddi-style convex counterexample：C=4</text>',
        f'<rect x="{x0}" y="{y0-height}" width="{width}" height="{height}" fill="#F8FAFC" stroke="#CBD5E1"/>',
    ]
    max_log = math.log10(data["steps"])
    adam_points = []
    ams_points = []
    for row in rows:
        x = x0 + math.log10(row["step"]) / max_log * width
        adam_y = y0 - (row["adam_x"] + 1.0) / 2.0 * height
        ams_y = y0 - (row["amsgrad_x"] + 1.0) / 2.0 * height
        adam_points.append((x, adam_y))
        ams_points.append((x, ams_y))
    lines += [
        polyline(adam_points, "#C24135"),
        polyline(ams_points, "#0F766E"),
        f'<line x1="{x0}" y1="{y0}" x2="{x0+width}" y2="{y0}" stroke="#2563EB" stroke-width="2" stroke-dasharray="7 6"/>',
        '<text x="112" y="493" class="sans blue" font-size="16">best fixed comparator x* = -1</text>',
        '<line x1="720" y1="82" x2="762" y2="82" stroke="#C24135" stroke-width="4"/><text x="772" y="88" class="sans ink" font-size="17">Adam</text>',
        '<line x1="900" y1="82" x2="942" y2="82" stroke="#0F766E" stroke-width="4"/><text x="952" y="88" class="sans ink" font-size="17">AMSGrad</text>',
        '<text x="595" y="556" class="sans ink" font-size="17" text-anchor="middle">optimizer step（log10 axis）</text>',
        '<text x="34" y="325" class="sans ink" font-size="17" text-anchor="middle" transform="rotate(-90 34 325)">projected iterate x</text>',
        '<text x="58" y="607" class="sans muted" font-size="16">这是否定特定 online-convex 普遍保证的受控反例，不是深度网络 benchmark。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_rms_svg(path: Path, update_data: dict, weight_data: dict) -> None:
    lines = svg_header(
        "Adam Update RMS 与 AdamW Weight RMS 审计",
        "左侧比较不同 beta1 的 Monte Carlo direction RMS 与 mean-field 公式，右侧展示线性随机递推的 Weight RMS 平方根缩放。",
        height=680,
    )
    lines += [
        '<text x="58" y="56" class="sans blue" font-size="23" font-weight="700">A | Update RMS：low-SNR stationary audit</text>',
        '<text x="628" y="56" class="sans blue" font-size="23" font-weight="700">B | Weight RMS：linear recursion audit</text>',
    ]
    # Left: grouped point pairs.
    x_positions = [150.0, 330.0, 510.0]
    y0, height = 510.0, 360.0
    for x, row in zip(x_positions, update_data["rows"]):
        y_emp = y0 - row["empirical_direction_rms"] * height
        y_theory = y0 - row["mean_field_theory"] * height
        lines += [
            f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y_emp:.2f}" stroke="#2563EB" stroke-width="20"/>',
            f'<circle cx="{x+34}" cy="{y_theory:.2f}" r="8" fill="#0F766E"/>',
            f'<text x="{x+15}" y="548" class="mono ink" font-size="16" text-anchor="middle">b1={row["beta1"]}</text>',
        ]
    lines += [
        '<line x1="90" y1="510" x2="565" y2="510" stroke="#1F2937" stroke-width="2"/>',
        '<line x1="90" y1="150" x2="90" y2="510" stroke="#1F2937" stroke-width="2"/>',
        '<rect x="110" y="92" width="20" height="20" fill="#2563EB"/><text x="140" y="108" class="sans ink" font-size="16">empirical</text>',
        '<circle cx="260" cy="102" r="8" fill="#0F766E"/><text x="278" y="108" class="sans ink" font-size="16">mean-field</text>',
    ]
    # Right: analytic square-root scaling for eta sweep at lambda=.1.
    sweep = [row for row in weight_data["analytic_sweep"] if row["lambda"] == 0.1]
    x0, width = 655.0, 455.0
    min_eta, max_eta = min(row["eta"] for row in sweep), max(row["eta"] for row in sweep)
    max_rms = max(row["exact_stationary_rms"] for row in sweep)
    exact_points = []
    approx_points = []
    for row in sweep:
        x = x0 + (math.log(row["eta"]) - math.log(min_eta)) / (math.log(max_eta) - math.log(min_eta)) * width
        exact_y = y0 - row["exact_stationary_rms"] / max_rms * height
        approx_y = y0 - row["small_step_approximation"] / max_rms * height
        exact_points.append((x, exact_y))
        approx_points.append((x, approx_y))
        lines.append(f'<text x="{x:.2f}" y="548" class="mono ink" font-size="15" text-anchor="middle">{row["eta"]:g}</text>')
    lines += [
        f'<line x1="{x0}" y1="510" x2="{x0+width}" y2="510" stroke="#1F2937" stroke-width="2"/>',
        f'<line x1="{x0}" y1="150" x2="{x0}" y2="510" stroke="#1F2937" stroke-width="2"/>',
        polyline(exact_points, "#2563EB"),
        polyline(approx_points, "#B7791F", dash="8 7"),
        '<line x1="805" y1="102" x2="847" y2="102" stroke="#2563EB" stroke-width="4"/><text x="857" y="108" class="sans ink" font-size="16">exact stationary</text>',
        '<line x1="1000" y1="102" x2="1042" y2="102" stroke="#B7791F" stroke-width="4" stroke-dasharray="8 7"/><text x="1052" y="108" class="sans ink" font-size="16">sqrt law</text>',
        '<text x="882" y="584" class="sans ink" font-size="17" text-anchor="middle">eta（log axis）, lambda=0.1</text>',
        '<text x="58" y="637" class="sans muted" font-size="16">左：随机比值在指定 regime 接近公式；右：平方根律来自零均值独立噪声的线性稳态，不是网络层定理。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("00-知识库管理/_labs/experiments/trn60.2-adaptive-optimizers-audit-v1"),
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/training-optimization"),
    )
    parser.add_argument("--ratio-repeats", type=int, default=50000)
    args = parser.parse_args()

    rng = random.Random(SEED)
    adagrad = audit_adagrad_scale()
    rmsprop = audit_rmsprop_response()
    adam_bias = audit_adam_bias(rng, args.ratio_repeats)
    epsilon = audit_epsilon()
    counterexample = audit_adam_amsgrad_counterexample()
    decay = audit_decay_paths()
    update_rms = audit_update_rms(rng)
    weight_rms = audit_weight_rms(rng)
    adafactor = audit_adafactor()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "seed": SEED,
        "adagrad_scale": adagrad,
        "rmsprop_response": rmsprop,
        "adam_bias": adam_bias,
        "epsilon": epsilon,
        "adam_amsgrad_counterexample": counterexample,
        "decay_paths": decay,
        "update_rms": update_rms,
        "weight_rms": weight_rms,
        "adafactor": adafactor,
    }
    (args.output_dir / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_csv(args.output_dir / "adagrad_scale_switch.csv", adagrad["midrun_rows"])
    write_csv(args.output_dir / "rmsprop_step_response.csv", rmsprop["rows"])
    write_csv(args.output_dir / "epsilon_response.csv", epsilon["rows"])
    write_csv(args.output_dir / "adam_amsgrad_counterexample.csv", counterexample["rows"])
    write_csv(args.output_dir / "update_rms.csv", update_rms["rows"])
    write_csv(args.output_dir / "weight_rms_sweep.csv", weight_rms["analytic_sweep"])
    write_csv(
        args.output_dir / "adafactor_reconstruction.csv",
        [
            {
                "case": case["case"],
                "max_row_marginal_error": case["max_row_marginal_error"],
                "max_column_marginal_error": case["max_column_marginal_error"],
                "element_rms_error": case["element_rms_error"],
            }
            for case in adafactor["cases"]
        ],
    )

    write_epsilon_svg(args.plot_dir / "plot-adaptive-epsilon-response-v1.svg", epsilon)
    write_counterexample_svg(
        args.plot_dir / "plot-adam-amsgrad-counterexample-v1.svg", counterexample
    )
    write_rms_svg(
        args.plot_dir / "plot-update-weight-rms-audit-v1.svg", update_rms, weight_rms
    )

    checks = {
        "adagrad_global_scale_identity": adagrad["max_exact_error"] < 1e-12,
        "adagrad_midrun_scale_counterexample": adagrad["step3_switch_gap"] > 0.3,
        "rmsprop_exact_step_response": rmsprop["max_recursion_error"] < 1e-12,
        "adam_constant_gradient_bias_correction": max(
            adam_bias["constant_gradient"]["max_m_hat_error"],
            adam_bias["constant_gradient"]["max_v_hat_error"],
            adam_bias["constant_gradient"]["max_direction_error"],
        )
        < 1e-10,
        "adam_ratio_not_unbiased": adam_bias["ratio_counterexample"]["gap"] > 0.35,
        "epsilon_scale_ratio_identity": epsilon["scale_break"]["ratio_error"] < 1e-12,
        "adam_counterexample_wrong_endpoint": counterexample["final_adam_x"] > 0.5,
        "amsgrad_counterexample_best_endpoint": counterexample["final_amsgrad_x"] < -0.99,
        "coupled_decay_is_anisotropic": decay["anisotropy_gap"] > 0.01,
        "update_rms_mean_field_within_3pct": max(
            row["relative_error"] for row in update_rms["rows"]
        )
        < 0.03,
        "weight_rms_mc_within_6pct": weight_rms["monte_carlo"]["relative_error_to_exact"]
        < 0.06,
        "adafactor_marginals_exact": max(
            max(case["max_row_marginal_error"], case["max_column_marginal_error"])
            for case in adafactor["cases"]
        )
        < 1e-12,
        "adafactor_rank_one_exact_and_general_not": adafactor["cases"][0]["element_rms_error"]
        < 1e-12
        and adafactor["cases"][1]["element_rms_error"] > 0.4,
    }
    print(
        json.dumps(
            {"checks": checks, "output_dir": str(args.output_dir), "plot_dir": str(args.plot_dir)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
