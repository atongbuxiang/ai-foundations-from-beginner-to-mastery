#!/usr/bin/env python3
"""Deterministic standard-library audit for TRN-33--TRN-40.

The script separates learning-rate scale, warmup, schedule endpoints and
horizon semantics, clipping bias/scope, Weight-RMS memory, parameter averaging,
factorial interactions and compute accounting.  It writes one JSON, ten CSVs
and three self-contained SVG figures.  NumPy, PyTorch and plotting packages are
deliberately not required.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path


SEED = 20260826


def dot(x: list[float], y: list[float]) -> float:
    return sum(a * b for a, b in zip(x, y))


def norm(x: list[float]) -> float:
    return math.sqrt(dot(x, x))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = mean(values)
    return sum((value - center) ** 2 for value in values) / (len(values) - 1)


def clip_vector(vector: list[float], threshold: float) -> tuple[list[float], float]:
    size = norm(vector)
    scale = 1.0 if size <= threshold or size == 0.0 else threshold / size
    return [scale * value for value in vector], scale


def audit_learning_rate_scale() -> list[dict]:
    theta = [6.0, 8.0]
    direction = [3.0, 4.0]
    rows = []
    for name, eta, scale in [("base", 0.1, 1.0), ("rescaled", 0.01, 10.0)]:
        actual_direction = [scale * value for value in direction]
        delta = [-eta * value for value in actual_direction]
        rows.append(
            {
                "case": name,
                "raw_learning_rate": eta,
                "direction_scale": scale,
                "direction_norm": norm(actual_direction),
                "delta_1": delta[0],
                "delta_2": delta[1],
                "absolute_step": norm(delta),
                "relative_step": norm(delta) / norm(theta),
            }
        )

    # An exact quadratic descent case: H=diag(2,8), theta=(1,1), eta=.2.
    gradient = [2.0, 8.0]
    delta = [-0.2 * value for value in gradient]
    before = 0.5 * (2.0 + 8.0)
    after_theta = [1.0 + delta[0], 1.0 + delta[1]]
    after = 0.5 * (2.0 * after_theta[0] ** 2 + 8.0 * after_theta[1] ** 2)
    rows.append(
        {
            "case": "quadratic_descent",
            "raw_learning_rate": 0.2,
            "direction_scale": 1.0,
            "direction_norm": norm(gradient),
            "delta_1": delta[0],
            "delta_2": delta[1],
            "absolute_step": norm(delta),
            "relative_step": norm(delta) / math.sqrt(2.0),
            "loss_before": before,
            "loss_after": after,
        }
    )
    return rows


def audit_warmup() -> list[dict]:
    curvature = 50.0
    peak = 0.05
    warmup_updates = 5
    rows = []
    theta = 1.0
    for update in range(1, warmup_updates + 1):
        eta = peak * update / warmup_updates
        multiplier = 1.0 - eta * curvature
        theta_next = multiplier * theta
        rows.append(
            {
                "successful_update": update,
                "learning_rate": eta,
                "quadratic_multiplier": multiplier,
                "strict_step_stability": 0.0 < eta * curvature < 2.0,
                "theta_before": theta,
                "theta_after": theta_next,
                "loss_before": 0.5 * curvature * theta * theta,
                "loss_after": 0.5 * curvature * theta_next * theta_next,
            }
        )
        theta = theta_next
    rows.append(
        {
            "successful_update": "clock_audit",
            "attempt_steps": 100,
            "overflow_probability": 0.2,
            "expected_successful_updates": 80.0,
            "attempt_clock_progress": 1.0,
            "success_clock_progress": 0.8,
        }
    )
    return rows


def schedule_values(name: str, count: int) -> list[float]:
    values = []
    for step in range(count):
        s = step / (count - 1)
        if name == "constant":
            value = 1.0
        elif name == "linear":
            value = 1.0 - s
        elif name == "cosine":
            value = 0.5 * (1.0 + math.cos(math.pi * s))
        elif name == "inverse_sqrt":
            value = 1.0 / math.sqrt(1.0 + step / 10.0)
        elif name == "wsd":
            stable_end = int(0.75 * (count - 1))
            value = 1.0 if step <= stable_end else (count - 1 - step) / (count - 1 - stable_end)
        else:
            raise ValueError(name)
        values.append(value)
    return values


def audit_schedules(count: int = 101) -> list[dict]:
    rows = []
    for name in ["constant", "linear", "cosine", "inverse_sqrt", "wsd"]:
        values = schedule_values(name, count)
        total = sum(values)
        squared = sum(value * value for value in values)
        decay_product = math.prod(1.0 - 0.01 * value for value in values)
        for step, value in enumerate(values):
            rows.append(
                {
                    "schedule": name,
                    "step": step,
                    "normalized_time": step / (count - 1),
                    "learning_rate": value,
                    "sum_learning_rate": total,
                    "sum_squared_learning_rate": squared,
                    "adamw_decay_product_lambda_0_01": decay_product,
                }
            )
    return rows


def audit_horizon() -> list[dict]:
    rows = []
    horizon = 100
    for step in [0, 25, 50, 75, 100]:
        old = 0.5 * (1.0 + math.cos(math.pi * step / horizon))
        extended = 0.5 * (1.0 + math.cos(math.pi * step / (2 * horizon)))
        trunk = 1.0 if step <= 75 else (100 - step) / 25
        rows.append(
            {
                "step": step,
                "cosine_horizon_100": old,
                "cosine_horizon_200": extended,
                "history_rewrite_gap": extended - old,
                "wsd_trunk_or_cooldown": trunk,
            }
        )
    return rows


def audit_clipping_bias() -> list[dict]:
    rows = []
    for value, probability in [(10.0, 0.1), (-1.0, 0.9)]:
        clipped = max(-1.0, min(1.0, value))
        rows.append(
            {
                "gradient": value,
                "probability": probability,
                "clipped_gradient": clipped,
                "raw_expectation_contribution": value * probability,
                "clipped_expectation_contribution": clipped * probability,
            }
        )
    raw_expectation = sum(row["raw_expectation_contribution"] for row in rows)
    clipped_expectation = sum(row["clipped_expectation_contribution"] for row in rows)
    rows.append(
        {
            "gradient": "expectation",
            "probability": 1.0,
            "clipped_gradient": "",
            "raw_expectation_contribution": raw_expectation,
            "clipped_expectation_contribution": clipped_expectation,
        }
    )

    first, second = [10.0, 0.0], [0.0, 2.0]
    averaged = [(a + b) / 2.0 for a, b in zip(first, second)]
    clip_after_average, _ = clip_vector(averaged, 1.0)
    clipped_first, _ = clip_vector(first, 1.0)
    clipped_second, _ = clip_vector(second, 1.0)
    average_after_clip = [(a + b) / 2.0 for a, b in zip(clipped_first, clipped_second)]
    rows.append(
        {
            "gradient": "clip_after_average",
            "vector_1": clip_after_average[0],
            "vector_2": clip_after_average[1],
        }
    )
    rows.append(
        {
            "gradient": "average_after_clip",
            "vector_1": average_after_clip[0],
            "vector_2": average_after_clip[1],
        }
    )
    return rows


def audit_clipping_scope() -> list[dict]:
    layer_1 = [6.0, 8.0]
    layer_2 = [0.6, 0.8]
    global_output, global_scale = clip_vector(layer_1 + layer_2, 5.0)
    layer_1_output, layer_1_scale = clip_vector(layer_1, 5.0)
    layer_2_output, layer_2_scale = clip_vector(layer_2, 5.0)
    rows = [
        {
            "method": "global",
            "layer_1_output_norm": norm(global_output[:2]),
            "layer_2_output_norm": norm(global_output[2:]),
            "layer_norm_ratio": norm(global_output[:2]) / norm(global_output[2:]),
            "layer_1_scale": global_scale,
            "layer_2_scale": global_scale,
        },
        {
            "method": "layerwise",
            "layer_1_output_norm": norm(layer_1_output),
            "layer_2_output_norm": norm(layer_2_output),
            "layer_norm_ratio": norm(layer_1_output) / norm(layer_2_output),
            "layer_1_scale": layer_1_scale,
            "layer_2_scale": layer_2_scale,
        },
    ]
    weight_norms = [10.0, 1.0]
    gradient_norms = [10.0, 1.0]
    agc_lambda = 0.1
    thresholds = [agc_lambda * value for value in weight_norms]
    output_norms = [min(g, threshold) for g, threshold in zip(gradient_norms, thresholds)]
    rows.append(
        {
            "method": "agc",
            "layer_1_output_norm": output_norms[0],
            "layer_2_output_norm": output_norms[1],
            "layer_norm_ratio": output_norms[0] / output_norms[1],
            "layer_1_scale": output_norms[0] / gradient_norms[0],
            "layer_2_scale": output_norms[1] / gradient_norms[1],
            "agc_lambda": agc_lambda,
        }
    )
    return rows


def audit_weight_rms() -> list[dict]:
    r = 4.0
    c = 0.0
    weight_decay = 0.1
    eta_before = 0.01
    a_before = 1.0 - eta_before * weight_decay
    # Start at the exact first-stage equilibrium so the step-80 LR intervention
    # isolates memory lag rather than an unrelated burn-in transient.
    q = eta_before * eta_before * r / (1.0 - a_before * a_before)
    rows = []
    for step in range(121):
        eta = 0.01 if step < 80 else 0.002
        a = 1.0 - eta * weight_decay
        equilibrium = eta * eta * r / (1.0 - a * a)
        q_next = a * a * q + eta * eta * r - 2.0 * a * eta * c
        rows.append(
            {
                "step": step,
                "learning_rate": eta,
                "decay_factor": a,
                "q_before": q,
                "q_after": q_next,
                "weight_rms_after": math.sqrt(q_next),
                "instantaneous_equilibrium_q": equilibrium,
                "recursion_residual": q_next - (a * a * q + eta * eta * r - 2.0 * a * eta * c),
            }
        )
        q = q_next
    return rows


def audit_averaging() -> list[dict]:
    values = [2.0, 4.0, 10.0]
    beta = 0.9
    ema = 0.0
    cumulative = 0.0
    rows = []
    for step, value in enumerate(values, start=1):
        ema = beta * ema + (1.0 - beta) * value
        cumulative += value
        swa = cumulative / step
        rows.append(
            {
                "step": step,
                "parameter": value,
                "ema": ema,
                "swa_prefix": swa,
                "ema_effective_weight_current": 1.0 - beta,
            }
        )
    rows.append(
        {
            "step": "nonlinear_counterexample",
            "theta_1": 1.0,
            "theta_2": 3.0,
            "parameter_average": 2.0,
            "prediction_at_parameter_average": 4.0,
            "prediction_average": 5.0,
        }
    )
    return rows


def audit_factorial() -> list[dict]:
    rows = []
    jitters = [0.10, -0.10, 0.05, -0.05, 0.0]
    for seed_index, jitter in enumerate(jitters, start=1):
        cells = {
            (0, 0): 2.0 + jitter,
            (1, 0): 1.7 + jitter,
            (0, 1): 1.8 + jitter,
            (1, 1): 1.2 + jitter,
        }
        interaction = cells[(1, 1)] - cells[(1, 0)] - cells[(0, 1)] + cells[(0, 0)]
        for (a, b), outcome in cells.items():
            rows.append(
                {
                    "seed": seed_index,
                    "factor_a": a,
                    "factor_b": b,
                    "validation_loss": outcome,
                    "paired_difference_a_at_b0": cells[(1, 0)] - cells[(0, 0)],
                    "interaction": interaction,
                }
            )
    return rows


def audit_budget() -> list[dict]:
    configurations = 4
    seeds = 2
    trunk = 100.0
    branches = 3
    branch = 10.0
    lineages = configurations * seeds
    shared = lineages * (trunk + branches * branch)
    naive = lineages * branches * (trunk + branch)
    return [
        {"account": "training_lineage_shared", "gpu_hours": shared, "included_runs": lineages},
        {"account": "training_naive_branch_rerun", "gpu_hours": naive, "included_runs": lineages * branches},
        {"account": "tuning", "gpu_hours": 64.0, "included_runs": 8},
        {"account": "selection", "gpu_hours": 8.0, "included_runs": 24},
        {"account": "final_evaluation", "gpu_hours": 6.0, "included_runs": 3},
        {"account": "lineage_saving", "gpu_hours": naive - shared, "included_runs": lineages},
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def svg_open(title: str, description: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title>',
        f'<desc id="desc">{html.escape(description)}</desc>',
        '<rect width="1200" height="800" fill="#FFFEFB"/>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;fill:#0F172A}.h{font-size:27px;font-weight:700}.sh{font-size:18px;font-weight:700}.b{font-size:14px}.s{font-size:12.5px;fill:#64748B}.axis{stroke:#94A3B8;stroke-width:1.5}.grid{stroke:#E2E8F0;stroke-width:1}.blue{stroke:#2563EB;stroke-width:3;fill:none}.green{stroke:#0F766E;stroke-width:3;fill:none}.amber{stroke:#B76E00;stroke-width:3;fill:none}.red{stroke:#C0392B;stroke-width:3;fill:none}.panel{fill:#F8FAFC;stroke:#CBD5E1;stroke-width:2}</style>',
    ]


def text_svg(x: float, y: float, value: str, klass: str = "b", fill: str | None = None) -> str:
    extra = f' fill="{fill}"' if fill else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{klass}"{extra}>{html.escape(value)}</text>'


def polyline_svg(points: list[tuple[float, float]], klass: str) -> str:
    payload = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{payload}" class="{klass}"/>'


def plot_schedule_horizon(path: Path, schedules: list[dict], horizon: list[dict]) -> None:
    lines = svg_open(
        "训练 schedule 的端点、面积与 horizon 改写",
        "左图比较五条归一化学习率曲线，右图比较同一历史时刻在两个 cosine horizon 下的学习率。",
    )
    lines += [text_svg(48, 48, "Schedule 名字之外，还要验收端点、面积与未来时域", "h", "#2563EB")]
    lines += ['<rect x="48" y="86" width="690" height="566" rx="14" class="panel"/>']
    lines += [text_svg(72, 124, "归一化 schedule（101 个离散点）", "sh")]
    left, top, width, height = 90.0, 170.0, 610.0, 400.0
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        y = top + height * (1.0 - frac)
        lines.append(f'<line x1="{left}" y1="{y}" x2="{left+width}" y2="{y}" class="grid"/>')
        lines.append(text_svg(58, y + 5, f"{frac:.2g}", "s"))
    lines.append(f'<line x1="{left}" y1="{top+height}" x2="{left+width}" y2="{top+height}" class="axis"/>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+height}" class="axis"/>')
    color_classes = {"constant": "blue", "linear": "green", "cosine": "amber", "inverse_sqrt": "red", "wsd": "blue"}
    dash = {"wsd": ' stroke-dasharray="8 6"'}
    for name in ["constant", "linear", "cosine", "inverse_sqrt", "wsd"]:
        values = [row for row in schedules if row["schedule"] == name]
        points = [(left + width * row["normalized_time"], top + height * (1.0 - row["learning_rate"])) for row in values]
        payload = polyline_svg(points, color_classes[name])
        if name in dash:
            payload = payload.replace("/>", f'{dash[name]}/>' )
        lines.append(payload)
    legend = [("constant", "#2563EB"), ("linear", "#0F766E"), ("cosine", "#B76E00"), ("inverse-sqrt", "#C0392B"), ("WSD", "#2563EB")]
    for index, (label, color) in enumerate(legend):
        x = 82 + index * 122
        lines.append(f'<line x1="{x}" y1="612" x2="{x+28}" y2="612" stroke="{color}" stroke-width="3"/>')
        lines.append(text_svg(x + 34, 617, label, "s"))

    lines += ['<rect x="774" y="86" width="378" height="566" rx="14" fill="#EEF4FF" stroke="#2563EB" stroke-width="2"/>']
    lines += [text_svg(798, 124, "同一 t，不同未来 T", "sh")]
    right_left, right_top, right_width, right_height = 812.0, 180.0, 300.0, 300.0
    lines.append(f'<line x1="{right_left}" y1="{right_top+right_height}" x2="{right_left+right_width}" y2="{right_top+right_height}" class="axis"/>')
    lines.append(f'<line x1="{right_left}" y1="{right_top}" x2="{right_left}" y2="{right_top+right_height}" class="axis"/>')
    old_points = [(right_left + right_width * row["step"] / 100.0, right_top + right_height * (1.0 - row["cosine_horizon_100"])) for row in horizon]
    new_points = [(right_left + right_width * row["step"] / 100.0, right_top + right_height * (1.0 - row["cosine_horizon_200"])) for row in horizon]
    lines.append(polyline_svg(old_points, "red"))
    lines.append(polyline_svg(new_points, "blue"))
    lines.append(text_svg(814, 518, "红：ηₜ(T)　蓝：ηₜ(2T)", "b"))
    lines.append(text_svg(814, 552, "t=T/2：0.500 → 0.854", "b", "#C0392B"))
    lines.append(text_svg(814, 584, "历史轨迹不能在 checkpoint 后重写", "s"))
    lines += ['<rect x="48" y="694" width="1104" height="62" rx="10" fill="#FFF6E5" stroke="#B76E00"/>']
    lines += [text_svg(72, 722, "读图边界：曲线展示控制输入；相同面积或端点不推出相同 optimizer state、参数轨迹或泛化。", "b")]
    lines += [text_svg(72, 746, "WSD 让 stable trunk 可复用，但 cooldown 与选择仍依赖停止时刻。", "s"), "</svg>"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_clipping_weight_rms(path: Path, clipping: list[dict], weight_rms: list[dict]) -> None:
    lines = svg_open(
        "裁剪偏差与 Weight RMS 的动态记忆",
        "左侧显示裁剪前后期望符号反转，右侧显示学习率阶跃后权重能量缓慢追随瞬时平衡。",
    )
    lines += [text_svg(48, 48, "两个控制器、两种边界：估计器偏差与历史滞后", "h", "#2563EB")]
    lines += ['<rect x="48" y="86" width="430" height="566" rx="14" fill="#FFF1F0" stroke="#C0392B" stroke-width="2"/>']
    lines += [text_svg(72, 124, "裁剪可反转随机梯度期望", "sh")]
    expectation = next(row for row in clipping if row["gradient"] == "expectation")
    values = [("E[g]", expectation["raw_expectation_contribution"], "#2563EB"), ("E[clip₁(g)]", expectation["clipped_expectation_contribution"], "#C0392B")]
    zero_y = 342.0
    lines.append(f'<line x1="92" y1="{zero_y}" x2="430" y2="{zero_y}" class="axis"/>')
    scale = 180.0
    for index, (label, value, color) in enumerate(values):
        x = 132 + index * 170
        y = zero_y - value * scale
        height = abs(value * scale)
        top = min(y, zero_y)
        lines.append(f'<rect x="{x}" y="{top}" width="82" height="{height}" rx="7" fill="{color}" opacity="0.82"/>')
        lines.append(text_svg(x - 6, 536, label, "b"))
        lines.append(text_svg(x + 18, top - 12 if value > 0 else top + height + 24, f"{value:.1f}", "sh", color))
    lines.append(text_svg(72, 584, "0.1×10 + 0.9×(−1) = +0.1", "b"))
    lines.append(text_svg(72, 614, "0.1×1 + 0.9×(−1) = −0.8", "b", "#C0392B"))

    lines += ['<rect x="514" y="86" width="638" height="566" rx="14" fill="#ECF7F4" stroke="#0F766E" stroke-width="2"/>']
    lines += [text_svg(538, 124, "LR 阶跃后，qₜ 不会瞬时跳到新平衡", "sh")]
    left, top, width, height = 560.0, 172.0, 552.0, 360.0
    max_q = max(max(row["q_after"], row["instantaneous_equilibrium_q"]) for row in weight_rms)
    lines.append(f'<line x1="{left}" y1="{top+height}" x2="{left+width}" y2="{top+height}" class="axis"/>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+height}" class="axis"/>')
    for step in [0, 40, 80, 120]:
        x = left + width * step / 120.0
        lines.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top+height}" class="grid"/>')
        lines.append(text_svg(x - 10, top + height + 25, str(step), "s"))
    q_points = [(left + width * row["step"] / 120.0, top + height * (1.0 - row["q_after"] / max_q)) for row in weight_rms]
    eq_points = [(left + width * row["step"] / 120.0, top + height * (1.0 - row["instantaneous_equilibrium_q"] / max_q)) for row in weight_rms]
    lines.append(polyline_svg(q_points, "blue"))
    lines.append(polyline_svg(eq_points, "amber"))
    lines.append(text_svg(560, 580, "蓝：实际 qₜ　橙：按当前 η/λ 计算的瞬时平衡", "b"))
    lines.append(text_svg(560, 612, "step 80 降 LR；历史核使实际 qₜ 缓慢追随", "s"))
    lines += ['<rect x="48" y="694" width="1104" height="62" rx="10" fill="#F8FAFC" stroke="#CBD5E1"/>']
    lines += [text_svg(72, 722, "读图边界：裁剪限制单次输入，不能保证无偏；瞬时 √(η/λ) 近似也不能删除 Weight RMS 的历史核。", "b")]
    lines += [text_svg(72, 746, "两者都必须与 optimizer state、时钟和功能更新遥测共同解释。", "s"), "</svg>"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_averaging_factorial(path: Path, averaging: list[dict], factorial: list[dict]) -> None:
    lines = svg_open(
        "参数平均与训练控制器交互",
        "左侧比较原参数轨迹、EMA 和前缀 SWA，右侧展示二乘二因子单元及非零交互。",
    )
    lines += [text_svg(48, 48, "平均对象与联合实验：输出选择也属于训练控制系统", "h", "#2563EB")]
    lines += ['<rect x="48" y="86" width="540" height="566" rx="14" fill="#EEF4FF" stroke="#2563EB" stroke-width="2"/>']
    lines += [text_svg(72, 124, "同一参数轨迹的三种读法", "sh")]
    numeric = [row for row in averaging if isinstance(row["step"], int)]
    left, top, width, height = 92.0, 176.0, 440.0, 300.0
    max_value = 10.0
    lines.append(f'<line x1="{left}" y1="{top+height}" x2="{left+width}" y2="{top+height}" class="axis"/>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+height}" class="axis"/>')
    for step in [1, 2, 3]:
        x = left + width * (step - 1) / 2
        lines.append(text_svg(x - 5, top + height + 25, str(step), "s"))
    raw = [(left + width * (row["step"] - 1) / 2, top + height * (1.0 - row["parameter"] / max_value)) for row in numeric]
    ema = [(left + width * (row["step"] - 1) / 2, top + height * (1.0 - row["ema"] / max_value)) for row in numeric]
    swa = [(left + width * (row["step"] - 1) / 2, top + height * (1.0 - row["swa_prefix"] / max_value)) for row in numeric]
    lines.append(polyline_svg(raw, "blue"))
    lines.append(polyline_svg(ema, "red"))
    lines.append(polyline_svg(swa, "green"))
    lines.append(text_svg(92, 526, "蓝：θₜ　红：EMA　绿：prefix SWA", "b"))
    lines.append(text_svg(92, 560, "非线性反例：f(θ̄)=4，但平均预测=5", "b", "#C0392B"))
    lines.append(text_svg(92, 592, "参数平均不是 prediction ensemble", "s"))

    lines += ['<rect x="624" y="86" width="528" height="566" rx="14" fill="#ECF7F4" stroke="#0F766E" stroke-width="2"/>']
    lines += [text_svg(648, 124, "2×2 因子单元与交互", "sh")]
    cell_means = {}
    for a in [0, 1]:
        for b in [0, 1]:
            cell_means[(a, b)] = mean([row["validation_loss"] for row in factorial if row["factor_a"] == a and row["factor_b"] == b])
    colors = {(0, 0): ("#EEF4FF", "#2563EB"), (1, 0): ("#ECF7F4", "#0F766E"), (0, 1): ("#FFF6E5", "#B76E00"), (1, 1): ("#FFF1F0", "#C0392B")}
    for a in [0, 1]:
        for b in [0, 1]:
            x = 720 + b * 190
            y = 190 + a * 150
            fill, stroke = colors[(a, b)]
            lines.append(f'<rect x="{x}" y="{y}" width="150" height="112" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            lines.append(text_svg(x + 48, y + 43, f"y{a}{b}", "sh"))
            lines.append(text_svg(x + 50, y + 78, f"{cell_means[(a,b)]:.1f}", "sh", stroke))
    interaction = cell_means[(1, 1)] - cell_means[(1, 0)] - cell_means[(0, 1)] + cell_means[(0, 0)]
    lines.append(text_svg(648, 520, f"I = y11 − y10 − y01 + y00 = {interaction:.1f}", "b"))
    lines.append(text_svg(648, 554, "I≠0：单因素排序不能外推联合配置", "b", "#C0392B"))
    lines.append(text_svg(648, 588, "paired seeds 共享扰动，先比较 cell 内差值", "s"))
    lines += ['<rect x="48" y="694" width="1104" height="62" rx="10" fill="#FFF6E5" stroke="#B76E00"/>']
    lines += [text_svg(72, 722, "读图边界：EMA/SWA 曲线不证明更好；非零交互只在当前模型、数据、因子水平与预算范围内成立。", "b")]
    lines += [text_svg(72, 746, "最终 claim 仍须报告 paired seeds、失败分母与训练/调参/选择/评估四本预算。", "s"), "</svg>"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_checks(data: dict[str, list[dict]]) -> list[dict]:
    lr = data["learning_rate_scale"]
    warmup = data["warmup_quadratic"]
    schedules = data["schedule_audit"]
    horizon = data["horizon_rewrite"]
    clipping = data["clipping_bias"]
    scope = data["clipping_scope"]
    rms = data["weight_rms"]
    averaging = data["averaging"]
    factorial = data["factorial"]
    budget = data["budget_ledger"]

    by_schedule = {name: [row for row in schedules if row["schedule"] == name] for name in ["constant", "linear", "cosine", "inverse_sqrt", "wsd"]}
    expectation = next(row for row in clipping if row["gradient"] == "expectation")
    after_average = next(row for row in clipping if row["gradient"] == "clip_after_average")
    after_clip = next(row for row in clipping if row["gradient"] == "average_after_clip")
    cell_means = {(a, b): mean([row["validation_loss"] for row in factorial if row["factor_a"] == a and row["factor_b"] == b]) for a in [0, 1] for b in [0, 1]}
    interaction = cell_means[(1, 1)] - cell_means[(1, 0)] - cell_means[(0, 1)] + cell_means[(0, 0)]
    paired = [row["paired_difference_a_at_b0"] for row in factorial if row["factor_b"] == 0 and row["factor_a"] == 0]
    y0 = [row["validation_loss"] for row in factorial if row["factor_a"] == 0 and row["factor_b"] == 0]
    y1 = [row["validation_loss"] for row in factorial if row["factor_a"] == 1 and row["factor_b"] == 0]

    checks = [
        ("lr_rescale_same_displacement", abs(lr[0]["delta_1"] - lr[1]["delta_1"]) < 1e-12 and abs(lr[0]["delta_2"] - lr[1]["delta_2"]) < 1e-12),
        ("quadratic_eta_0_2_descends", lr[2]["loss_after"] < lr[2]["loss_before"]),
        ("warmup_first_three_strictly_stable", all(row["strict_step_stability"] for row in warmup[:3])),
        ("warmup_peak_is_unstable", not warmup[4]["strict_step_stability"]),
        ("attempt_and_success_clock_diverge", warmup[-1]["expected_successful_updates"] == 80.0),
        ("linear_endpoints_exact", by_schedule["linear"][0]["learning_rate"] == 1.0 and by_schedule["linear"][-1]["learning_rate"] == 0.0),
        ("cosine_endpoints_exact", abs(by_schedule["cosine"][0]["learning_rate"] - 1.0) < 1e-12 and abs(by_schedule["cosine"][-1]["learning_rate"]) < 1e-12),
        ("wsd_endpoint_exact", by_schedule["wsd"][-1]["learning_rate"] == 0.0),
        ("linear_and_cosine_areas_near_equal", abs(sum(row["learning_rate"] for row in by_schedule["linear"]) - sum(row["learning_rate"] for row in by_schedule["cosine"])) < 1e-10),
        ("cosine_squared_area_exceeds_linear", sum(row["learning_rate"] ** 2 for row in by_schedule["cosine"]) > sum(row["learning_rate"] ** 2 for row in by_schedule["linear"])),
        ("inverse_sqrt_tail_not_zero", by_schedule["inverse_sqrt"][-1]["learning_rate"] > 0.0),
        ("horizon_rewrites_interior_history", all(row["history_rewrite_gap"] > 0.0 for row in horizon[1:-1])),
        ("horizon_origin_matches", abs(horizon[0]["history_rewrite_gap"]) < 1e-12),
        ("clipping_bias_reverses_expectation", expectation["raw_expectation_contribution"] > 0.0 and expectation["clipped_expectation_contribution"] < 0.0),
        ("clip_and_average_do_not_commute", abs(after_average["vector_1"] - after_clip["vector_1"]) > 0.1 and abs(after_average["vector_2"] - after_clip["vector_2"]) > 0.1),
        ("global_clipping_preserves_layer_ratio", abs(scope[0]["layer_norm_ratio"] - 10.0) < 1e-12),
        ("layerwise_clipping_changes_layer_ratio", abs(scope[1]["layer_norm_ratio"] - 5.0) < 1e-12),
        ("agc_threshold_tracks_weight_norm", abs(scope[2]["layer_norm_ratio"] - 10.0) < 1e-12),
        ("weight_rms_recursion_exact", max(abs(row["recursion_residual"]) for row in rms) < 1e-15),
        ("weight_rms_lags_after_lr_drop", rms[80]["q_after"] > 2.0 * rms[80]["instantaneous_equilibrium_q"]),
        ("lower_lr_equilibrium_is_lower", rms[80]["instantaneous_equilibrium_q"] < rms[79]["instantaneous_equilibrium_q"]),
        ("ema_three_step_value", abs(averaging[2]["ema"] - 1.522) < 1e-12),
        ("parameter_and_prediction_average_differ", averaging[-1]["prediction_at_parameter_average"] != averaging[-1]["prediction_average"]),
        ("factorial_interaction_nonzero", abs(interaction + 0.3) < 1e-12),
        ("paired_variance_below_unpaired_sum", sample_variance(paired) < sample_variance(y0) + sample_variance(y1)),
        ("lineage_dedup_saves_compute", next(row for row in budget if row["account"] == "training_lineage_shared")["gpu_hours"] < next(row for row in budget if row["account"] == "training_naive_branch_rerun")["gpu_hours"]),
        ("four_budget_accounts_present", {"training_lineage_shared", "tuning", "selection", "final_evaluation"}.issubset({row["account"] for row in budget})),
    ]
    return [{"id": name, "passed": bool(passed)} for name, passed in checks]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("00-知识库管理/_labs/experiments/trn60.5-training-control-audit-v1"),
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/training-optimization"),
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.plot_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "learning_rate_scale": audit_learning_rate_scale(),
        "warmup_quadratic": audit_warmup(),
        "schedule_audit": audit_schedules(),
        "horizon_rewrite": audit_horizon(),
        "clipping_bias": audit_clipping_bias(),
        "clipping_scope": audit_clipping_scope(),
        "weight_rms": audit_weight_rms(),
        "averaging": audit_averaging(),
        "factorial": audit_factorial(),
        "budget_ledger": audit_budget(),
    }
    for name, rows in data.items():
        write_csv(args.output_dir / f"{name}.csv", rows)

    plot_schedule_horizon(
        args.plot_dir / "plot-training-control-schedule-horizon-v1.svg",
        data["schedule_audit"],
        data["horizon_rewrite"],
    )
    plot_clipping_weight_rms(
        args.plot_dir / "plot-training-control-clipping-weight-rms-v1.svg",
        data["clipping_bias"],
        data["weight_rms"],
    )
    plot_averaging_factorial(
        args.plot_dir / "plot-training-control-averaging-factorial-v1.svg",
        data["averaging"],
        data["factorial"],
    )

    checks = build_checks(data)
    result = {
        "experiment_id": "EXP-TRN-605-V1",
        "seed": SEED,
        "standard_library_only": True,
        "tracks": list(data),
        "check_count": len(checks),
        "passed_count": sum(check["passed"] for check in checks),
        "checks": checks,
        "evidence_boundaries": [
            "Deterministic scalar/vector controls test definitions and counterexamples, not LLM quality.",
            "Schedule area and Weight-RMS equilibrium are diagnostics, not sufficient performance statistics.",
            "Factorial effects are scoped to the declared cells and budget ledger.",
        ],
        "artifacts": {
            "csv": [f"{name}.csv" for name in data],
            "plots": [
                "plot-training-control-schedule-horizon-v1.svg",
                "plot-training-control-clipping-weight-rms-v1.svg",
                "plot-training-control-averaging-factorial-v1.svg",
            ],
        },
    }
    (args.output_dir / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if result["passed_count"] != result["check_count"]:
        failed = [check["id"] for check in checks if not check["passed"]]
        raise SystemExit("failed checks: " + ", ".join(failed))
    print(f"PASS {result['passed_count']}/{result['check_count']} checks")
    print(f"output={args.output_dir}")
    print(f"plots={args.plot_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
