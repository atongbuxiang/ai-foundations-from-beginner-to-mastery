#!/usr/bin/env python3
"""Standard-library numerical audit for TRN-01--TRN-08.

Checks reduction scaling, gradient accumulation boundaries, momentum convention
translation, heavy-ball roots, mini-batch covariance scaling, and the empirical
critical-batch tradeoff. It also emits three self-contained SVG plots.
"""

from __future__ import annotations

import argparse
import cmath
import csv
import json
import math
import random
from pathlib import Path


SEED = 20260826


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def sample_variance(xs: list[float]) -> float:
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def clip_scalar(x: float, threshold: float) -> float:
    return max(-threshold, min(threshold, x))


def audit_reduction_and_accumulation() -> dict:
    theta = 1.0
    gradients = [2.0, 4.0]
    eta_mean = 0.1
    eta_sum = eta_mean / len(gradients)
    theta_mean = theta - eta_mean * mean(gradients)
    theta_sum_matched = theta - eta_sum * sum(gradients)
    theta_sum_unmatched = theta - eta_mean * sum(gradients)

    # Frozen-parameter accumulation versus sequential parameter updates.
    ys = [1.0, 3.0]
    theta0 = 0.0
    eta = 0.1
    frozen_grads = [theta0 - y for y in ys]
    batch_grad = mean(frozen_grads)
    accumulated_grad = sum(g / len(ys) for g in frozen_grads)
    theta_batch = theta0 - eta * batch_grad
    theta_sequential = theta0
    for y in ys:
        theta_sequential -= eta * (theta_sequential - y)

    per_micro_clip = clip_scalar(2.0, 1.0) + clip_scalar(-1.0, 1.0)
    post_sum_clip = clip_scalar(2.0 - 1.0, 1.0)

    return {
        "mean_sum": {
            "theta_mean": theta_mean,
            "theta_sum_matched": theta_sum_matched,
            "theta_sum_unmatched": theta_sum_unmatched,
            "matched_abs_error": abs(theta_mean - theta_sum_matched),
        },
        "accumulation": {
            "batch_grad": batch_grad,
            "accumulated_grad": accumulated_grad,
            "gradient_abs_error": abs(batch_grad - accumulated_grad),
            "theta_one_batch_step": theta_batch,
            "theta_two_sequential_steps": theta_sequential,
        },
        "clipping_counterexample": {
            "sum_of_micro_clips": per_micro_clip,
            "clip_after_sum": post_sum_clip,
        },
    }


def audit_momentum_conventions() -> dict:
    gradients = [2.0, -1.0, 0.5]
    mu = 0.9
    eta = 0.1
    buffer = 0.0
    velocity = 0.0
    rows = []
    for step, gradient in enumerate(gradients):
        buffer = mu * buffer + gradient
        velocity = mu * velocity - eta * gradient
        rows.append(
            {
                "step": step,
                "gradient": gradient,
                "buffer": buffer,
                "velocity": velocity,
                "translation_error": abs(velocity + eta * buffer),
            }
        )

    # Variable LR breaks the naive velocity recurrence.
    lrs = [0.1, 0.01]
    variable_buffer = 0.0
    naive_velocity = 0.0
    variable_rows = []
    for step, (gradient, lr) in enumerate(zip([1.0, 1.0], lrs)):
        variable_buffer = mu * variable_buffer + gradient
        buffer_update = -lr * variable_buffer
        naive_velocity = mu * naive_velocity - lr * gradient
        variable_rows.append(
            {
                "step": step,
                "lr": lr,
                "buffer_parameter_update": buffer_update,
                "naive_velocity_update": naive_velocity,
            }
        )

    # PyTorch-style first-buffer exception when dampening is nonzero.
    dampening = 0.1
    pt_buffer = None
    pt_rows = []
    for step, gradient in enumerate([1.0, 2.0, 3.0]):
        if pt_buffer is None:
            pt_buffer = gradient
        else:
            pt_buffer = mu * pt_buffer + (1.0 - dampening) * gradient
        pt_rows.append({"step": step, "gradient": gradient, "buffer": pt_buffer})

    return {
        "constant_lr_translation": rows,
        "max_translation_error": max(row["translation_error"] for row in rows),
        "variable_lr_counterexample": variable_rows,
        "pytorch_dampening_first_step": pt_rows,
    }


def heavy_ball_roots(mu: float, normalized_step: float) -> tuple[complex, complex]:
    a = 1.0 + mu - normalized_step
    discriminant = complex(a * a - 4.0 * mu, 0.0)
    root = cmath.sqrt(discriminant)
    return (0.5 * (a + root), 0.5 * (a - root))


def root_class(r1: complex, r2: complex, tol: float = 1e-10) -> str:
    rho = max(abs(r1), abs(r2))
    if rho >= 1.0 - tol:
        return "unstable"
    if abs(r1.imag) > tol or abs(r2.imag) > tol:
        return "complex_damped"
    if r1.real >= 0.0 and r2.real >= 0.0:
        return "positive_real"
    return "negative_real"


def audit_heavy_ball() -> dict:
    mu = 0.9
    rows = []
    for index in range(0, 421):
        x = index / 100.0
        r1, r2 = heavy_ball_roots(mu, x)
        rows.append(
            {
                "eta_lambda": x,
                "rho": max(abs(r1), abs(r2)),
                "class": root_class(r1, r2),
            }
        )
    boundaries = {
        "positive_to_complex": (1.0 - math.sqrt(mu)) ** 2,
        "complex_to_negative": (1.0 + math.sqrt(mu)) ** 2,
        "stability_upper": 2.0 * (1.0 + mu),
    }
    return {"mu": mu, "boundaries": boundaries, "rows": rows}


def audit_covariance(rng: random.Random, repeats: int) -> dict:
    population = [-1.0, 1.0, 3.0, 5.0]
    population_mean = mean(population)
    covariance_n = mean([(x - population_mean) ** 2 for x in population])
    rows = []
    for batch_size in [1, 2, 4, 8, 16, 32, 64]:
        estimates = [
            mean([rng.choice(population) for _ in range(batch_size)])
            for _ in range(repeats)
        ]
        empirical = sample_variance(estimates)
        theory = covariance_n / batch_size
        rows.append(
            {
                "batch_size": batch_size,
                "empirical_variance": empirical,
                "theory_variance": theory,
                "relative_error": abs(empirical - theory) / theory,
            }
        )

    without_replacement = []
    n = len(population)
    for batch_size in [1, 2, 3, 4]:
        estimates = [mean(rng.sample(population, batch_size)) for _ in range(repeats)]
        empirical = sample_variance(estimates)
        theory = (n - batch_size) * covariance_n / (batch_size * (n - 1))
        without_replacement.append(
            {
                "batch_size": batch_size,
                "empirical_variance": empirical,
                "theory_variance": theory,
                "absolute_error": abs(empirical - theory),
            }
        )
    return {
        "population": population,
        "population_mean": population_mean,
        "covariance_denominator_n": covariance_n,
        "with_replacement": rows,
        "without_replacement": without_replacement,
    }


def audit_critical_batch() -> dict:
    noise_batch = 256.0
    batch_sizes = [2 ** k for k in range(0, 13)]
    rows = []
    for batch_size in batch_sizes:
        rows.append(
            {
                "batch_size": batch_size,
                "steps_over_min": 1.0 + noise_batch / batch_size,
                "examples_over_min": 1.0 + batch_size / noise_batch,
            }
        )
    return {"noise_batch": noise_batch, "rows": rows}


SVG_STYLE = """<style>
.sans{font-family:Inter,\"PingFang SC\",\"Noto Sans CJK SC\",sans-serif}.mono{font-family:\"SFMono-Regular\",Menlo,monospace}
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


def write_covariance_svg(path: Path, data: dict) -> None:
    rows = data["with_replacement"]
    lines = svg_header(
        "Mini-batch 方差按一除以 B 缩放的 Monte Carlo 审计",
        "对固定四点梯度总体重复有放回抽样，比较批量均值经验方差与理论 C 除以 B，并在下方给出相对误差。",
    )
    x0, y0, width, height = 110.0, 500.0, 960.0, 360.0
    lines += [
        '<text x="62" y="58" class="sans blue" font-size="23" font-weight="700">Monte Carlo：batch mean variance</text>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0+width}" y2="{y0}" stroke="#1F2937" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-height}" stroke="#1F2937" stroke-width="2"/>',
    ]
    max_variance = max(row["theory_variance"] for row in rows)
    for index, row in enumerate(rows):
        x = x0 + index * width / (len(rows) - 1)
        y_theory = y0 - row["theory_variance"] / max_variance * height
        y_emp = y0 - row["empirical_variance"] / max_variance * height
        lines.append(f'<circle cx="{x:.2f}" cy="{y_emp:.2f}" r="7" fill="#2563EB"/>')
        if index:
            previous = rows[index - 1]
            px = x0 + (index - 1) * width / (len(rows) - 1)
            py = y0 - previous["theory_variance"] / max_variance * height
            lines.append(f'<line x1="{px:.2f}" y1="{py:.2f}" x2="{x:.2f}" y2="{y_theory:.2f}" stroke="#0F766E" stroke-width="3"/>')
        lines.append(f'<text x="{x:.2f}" y="530" class="mono ink" font-size="16" text-anchor="middle">{row["batch_size"]}</text>')
    lines += [
        '<text x="590" y="574" class="sans ink" font-size="17" text-anchor="middle">batch size B（横轴为倍增序列）</text>',
        '<text x="34" y="320" class="sans ink" font-size="17" text-anchor="middle" transform="rotate(-90 34 320)">variance</text>',
        '<circle cx="852" cy="76" r="7" fill="#2563EB"/><text x="870" y="82" class="sans ink" font-size="17">empirical</text>',
        '<line x1="982" y1="76" x2="1024" y2="76" stroke="#0F766E" stroke-width="3"/><text x="1036" y="82" class="sans ink" font-size="17">C/B</text>',
        '<text x="62" y="614" class="sans muted" font-size="16">seed=20260826；误差来自有限 Monte Carlo，不代表真实深网 gradient 为 Gaussian。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_stability_svg(path: Path, data: dict) -> None:
    rows = data["rows"]
    boundaries = data["boundaries"]
    lines = svg_header(
        "Heavy-ball 特征根谱半径与解析稳定边界",
        "固定 momentum 为零点九，扫描 eta lambda，绘制最大根模并标出复根区域和解析稳定上界。",
    )
    x0, y0, width, height = 100.0, 500.0, 1000.0, 360.0
    lines += [
        '<text x="62" y="58" class="sans blue" font-size="23" font-weight="700">Heavy-ball roots：mu=0.9</text>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0+width}" y2="{y0}" stroke="#1F2937" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-height}" stroke="#1F2937" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0-height/1.3:.2f}" x2="{x0+width}" y2="{y0-height/1.3:.2f}" stroke="#C24135" stroke-width="2" stroke-dasharray="8 7"/>',
    ]
    points = []
    for row in rows:
        x = x0 + row["eta_lambda"] / 4.2 * width
        y = y0 - min(row["rho"], 1.3) / 1.3 * height
        points.append(f"{x:.2f},{y:.2f}")
    lines.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#2563EB" stroke-width="3"/>')
    for label, value in boundaries.items():
        x = x0 + value / 4.2 * width
        color = "#C24135" if label == "stability_upper" else "#B7791F"
        lines.append(f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0-height}" stroke="{color}" stroke-width="2" stroke-dasharray="7 6"/>')
        if label == "positive_to_complex":
            label_x, label_y, anchor = x + 8.0, 530, "start"
        elif label == "complex_to_negative":
            label_x, label_y, anchor = x - 8.0, 530, "end"
        else:
            label_x, label_y, anchor = x + 8.0, 552, "start"
        lines.append(f'<text x="{label_x:.2f}" y="{label_y}" class="mono ink" font-size="15" text-anchor="{anchor}">{value:.3f}</text>')
    lines += [
        '<text x="600" y="574" class="sans ink" font-size="17" text-anchor="middle">normalized step eta × lambda</text>',
        '<text x="34" y="320" class="sans ink" font-size="17" text-anchor="middle" transform="rotate(-90 34 320)">spectral radius</text>',
        '<text x="760" y="92" class="sans amber" font-size="17">amber：根类型边界</text>',
        '<text x="950" y="92" class="sans red" font-size="17">red：rho=1 / stability</text>',
        '<text x="62" y="614" class="sans muted" font-size="16">解析对象是固定 quadratic eigenmode；不直接覆盖时变非凸训练。</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_critical_svg(path: Path, data: dict) -> None:
    rows = data["rows"]
    lines = svg_header(
        "Critical batch 经验模型中的 step 与 example 代价",
        "以 B noise 为二百五十六，绘制归一化 optimizer steps 随 batch 下降、归一化 examples 随 batch 上升，并标出两者为二的交点。",
    )
    x0, y0, width, height = 100.0, 500.0, 1000.0, 360.0
    lines += [
        '<text x="62" y="58" class="sans blue" font-size="23" font-weight="700">Empirical tradeoff model：B_noise=256</text>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0+width}" y2="{y0}" stroke="#1F2937" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-height}" stroke="#1F2937" stroke-width="2"/>',
    ]
    step_points, example_points = [], []
    max_cost = 10.0
    for index, row in enumerate(rows):
        x = x0 + index * width / (len(rows) - 1)
        sy = y0 - min(row["steps_over_min"], max_cost) / max_cost * height
        ey = y0 - min(row["examples_over_min"], max_cost) / max_cost * height
        step_points.append(f"{x:.2f},{sy:.2f}")
        example_points.append(f"{x:.2f},{ey:.2f}")
        if row["batch_size"] in [1, 16, 256, 4096]:
            lines.append(f'<text x="{x:.2f}" y="530" class="mono ink" font-size="15" text-anchor="middle">{row["batch_size"]}</text>')
    critical_index = [row["batch_size"] for row in rows].index(256)
    critical_x = x0 + critical_index * width / (len(rows) - 1)
    critical_y = y0 - 2.0 / max_cost * height
    lines += [
        f'<polyline points="{" ".join(step_points)}" fill="none" stroke="#2563EB" stroke-width="4"/>',
        f'<polyline points="{" ".join(example_points)}" fill="none" stroke="#B7791F" stroke-width="4"/>',
        f'<line x1="{critical_x:.2f}" y1="{y0}" x2="{critical_x:.2f}" y2="{y0-height}" stroke="#0F766E" stroke-width="2" stroke-dasharray="8 7"/>',
        f'<circle cx="{critical_x:.2f}" cy="{critical_y:.2f}" r="8" fill="#0F766E"/>',
        '<text x="600" y="574" class="sans ink" font-size="17" text-anchor="middle">batch size B（倍增序列）</text>',
        '<text x="34" y="320" class="sans ink" font-size="17" text-anchor="middle" transform="rotate(-90 34 320)">normalized cost（上端截断为 10）</text>',
        '<line x1="800" y1="82" x2="842" y2="82" stroke="#2563EB" stroke-width="4"/><text x="854" y="88" class="sans ink" font-size="17">steps / min</text>',
        '<line x1="980" y1="82" x2="1022" y2="82" stroke="#B7791F" stroke-width="4"/><text x="1034" y="88" class="sans ink" font-size="17">examples / min</text>',
        '<text x="62" y="614" class="sans muted" font-size="16">这是 McCandlish 风格经验拟合，不含硬件 step time，也不是普遍定理。</text>',
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
    parser.add_argument("--repeats", type=int, default=30000)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("00-知识库管理/_labs/experiments/trn60.1-sgd-momentum-noise-audit-v1"),
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/training-optimization"),
    )
    args = parser.parse_args()

    rng = random.Random(SEED)
    reduction = audit_reduction_and_accumulation()
    momentum = audit_momentum_conventions()
    heavy_ball = audit_heavy_ball()
    covariance = audit_covariance(rng, args.repeats)
    critical = audit_critical_batch()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "seed": SEED,
        "repeats": args.repeats,
        "reduction_and_accumulation": reduction,
        "momentum": momentum,
        "heavy_ball": {"mu": heavy_ball["mu"], "boundaries": heavy_ball["boundaries"]},
        "covariance": covariance,
        "critical_batch": critical,
    }
    (args.output_dir / "results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_csv(args.output_dir / "covariance_with_replacement.csv", covariance["with_replacement"])
    write_csv(args.output_dir / "covariance_without_replacement.csv", covariance["without_replacement"])
    write_csv(args.output_dir / "heavy_ball_scan.csv", heavy_ball["rows"])
    write_csv(args.output_dir / "critical_batch_tradeoff.csv", critical["rows"])

    write_covariance_svg(args.plot_dir / "plot-batch-covariance-scaling-v1.svg", covariance)
    write_stability_svg(args.plot_dir / "plot-heavy-ball-stability-audit-v1.svg", heavy_ball)
    write_critical_svg(args.plot_dir / "plot-critical-batch-tradeoff-v1.svg", critical)

    checks = {
        "mean_sum_match": reduction["mean_sum"]["matched_abs_error"] < 1e-12,
        "accumulation_match": reduction["accumulation"]["gradient_abs_error"] < 1e-12,
        "clipping_counterexample": reduction["clipping_counterexample"]["sum_of_micro_clips"]
        != reduction["clipping_counterexample"]["clip_after_sum"],
        "momentum_constant_lr_translation": momentum["max_translation_error"] < 1e-12,
        "covariance_relative_error_below_5pct": max(
            row["relative_error"] for row in covariance["with_replacement"]
        )
        < 0.05,
        "analytic_stability_upper_is_3p8": abs(
            heavy_ball["boundaries"]["stability_upper"] - 3.8
        )
        < 1e-12,
    }
    print(json.dumps({"checks": checks, "output_dir": str(args.output_dir)}, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
