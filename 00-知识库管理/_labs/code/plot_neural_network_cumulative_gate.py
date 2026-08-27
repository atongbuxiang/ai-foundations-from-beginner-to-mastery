#!/usr/bin/env python3
"""Generate the deterministic neural-network-foundations cumulative gate.

The three panels audit different contracts instead of reporting a model score:
1. forward/reverse consistency for a small ReLU MLP;
2. depth scaling and a LayerNorm invariance check;
3. tied-embedding gradient paths plus stochastic/target identities.
"""

from __future__ import annotations

import math
from pathlib import Path

from plot_calculus_operator_figures_v2 import (
    AMBER,
    BG,
    BLUE,
    GRID,
    INK,
    MUTED,
    RED,
    TEAL,
    begin,
    circle,
    finish,
    heading,
    line,
    path,
    rect,
    text,
)


OUT = (
    Path(__file__).resolve().parents[2]
    / "_assets"
    / "plots"
    / "neural-networks"
    / "plot-neural-network-cumulative-gate-v2.svg"
)


def softmax(z: list[float]) -> list[float]:
    shift = max(z)
    exp_z = [math.exp(value - shift) for value in z]
    total = sum(exp_z)
    return [value / total for value in exp_z]


def mlp_loss(params: list[float]) -> float:
    x = [1.0, -2.0]
    target = 2
    w1 = [params[0:2], params[2:4]]
    b1 = params[4:6]
    w2 = [params[6:8], params[8:10], params[10:12]]
    b2 = params[12:15]
    a = [sum(w1[i][j] * x[j] for j in range(2)) + b1[i] for i in range(2)]
    h = [max(0.0, value) for value in a]
    z = [sum(w2[k][j] * h[j] for j in range(2)) + b2[k] for k in range(3)]
    shift = max(z)
    return -z[target] + shift + math.log(sum(math.exp(value - shift) for value in z))


def mlp_gradient(params: list[float]) -> list[float]:
    x = [1.0, -2.0]
    target = 2
    w1 = [params[0:2], params[2:4]]
    b1 = params[4:6]
    w2 = [params[6:8], params[8:10], params[10:12]]
    b2 = params[12:15]
    a = [sum(w1[i][j] * x[j] for j in range(2)) + b1[i] for i in range(2)]
    h = [max(0.0, value) for value in a]
    z = [sum(w2[k][j] * h[j] for j in range(2)) + b2[k] for k in range(3)]
    p = softmax(z)
    dz = [p[k] - float(k == target) for k in range(3)]
    dw2 = [dz[k] * h[j] for k in range(3) for j in range(2)]
    db2 = dz
    dh = [sum(w2[k][j] * dz[k] for k in range(3)) for j in range(2)]
    da = [dh[j] if a[j] > 0.0 else 0.0 for j in range(2)]
    dw1 = [da[i] * x[j] for i in range(2) for j in range(2)]
    db1 = da
    return dw1 + db1 + dw2 + db2


def central_difference_errors() -> tuple[list[float], list[float]]:
    params = [
        1.0,
        -1.0,
        0.5,
        0.5,
        0.0,
        1.0,
        1.0,
        0.0,
        -1.0,
        2.0,
        0.5,
        -1.0,
        0.0,
        0.5,
        -0.5,
    ]
    analytic = mlp_gradient(params)
    epsilons = [10.0 ** (-k) for k in range(1, 9)]
    errors: list[float] = []
    for epsilon in epsilons:
        numeric = []
        for index in range(len(params)):
            plus = params.copy()
            minus = params.copy()
            plus[index] += epsilon
            minus[index] -= epsilon
            numeric.append((mlp_loss(plus) - mlp_loss(minus)) / (2.0 * epsilon))
        errors.append(max(abs(a - b) for a, b in zip(analytic, numeric)))
    return epsilons, errors


def depth_gains(depth: int = 64) -> dict[str, list[float]]:
    weights = [0.15 + 0.05 * math.sin(0.7 * (index + 1)) for index in range(depth)]
    curves: dict[str, list[float]] = {}
    for name, alpha, plain in (
        ("plain", 1.0, True),
        ("residual alpha=1", 1.0, False),
        ("residual alpha=1/sqrt(L)", 1.0 / math.sqrt(depth), False),
    ):
        gain = 1.0
        values = []
        for weight in weights:
            gain *= weight if plain else 1.0 + alpha * weight
            values.append(abs(gain))
        curves[name] = values
    return curves


def layernorm_invariance_error() -> float:
    x = [1.0, 2.0, 3.0]

    def normalize(values: list[float]) -> list[float]:
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        return [(value - mean) / math.sqrt(variance) for value in values]

    lhs = normalize([2.0 * value + 5.0 for value in x])
    rhs = normalize(x)
    return max(abs(a - b) for a, b in zip(lhs, rhs))


def tied_loss(flat_e: list[float], target: list[float]) -> float:
    embedding = [flat_e[2 * i : 2 * i + 2] for i in range(4)]
    ids = [2, 1, 2]
    hidden = [sum(embedding[index][j] for index in ids) / len(ids) for j in range(2)]
    logits = [sum(embedding[k][j] * hidden[j] for j in range(2)) for k in range(4)]
    shift = max(logits)
    return -sum(target[k] * (logits[k] - shift) for k in range(4)) + math.log(
        sum(math.exp(value - shift) for value in logits)
    )


def tied_gradients(flat_e: list[float], target: list[float]) -> tuple[list[float], list[float]]:
    embedding = [flat_e[2 * i : 2 * i + 2] for i in range(4)]
    ids = [2, 1, 2]
    hidden = [sum(embedding[index][j] for index in ids) / len(ids) for j in range(2)]
    logits = [sum(embedding[k][j] * hidden[j] for j in range(2)) for k in range(4)]
    p = softmax(logits)
    dz = [p[k] - target[k] for k in range(4)]
    output_path = [[dz[k] * hidden[j] for j in range(2)] for k in range(4)]
    dh = [sum(embedding[k][j] * dz[k] for k in range(4)) for j in range(2)]
    lookup_path = [[0.0, 0.0] for _ in range(4)]
    for index in ids:
        for j in range(2):
            lookup_path[index][j] += dh[j] / len(ids)
    combined = [
        output_path[k][j] + lookup_path[k][j]
        for k in range(4)
        for j in range(2)
    ]
    output_only = [value for row in output_path for value in row]
    return combined, output_only


def tied_gradient_errors() -> tuple[float, float, float]:
    embedding = [1.0, 0.0, 0.0, 2.0, 1.0, 1.0, 0.0, 0.0]
    lam, epsilon = 0.3, 0.2
    mixed = [lam, 0.0, 1.0 - lam, 0.0]
    target = [(1.0 - epsilon) * value + epsilon / 4.0 for value in mixed]
    combined, output_only = tied_gradients(embedding, target)
    step = 1e-5
    numeric = []
    for index in range(len(embedding)):
        plus = embedding.copy()
        minus = embedding.copy()
        plus[index] += step
        minus[index] -= step
        numeric.append((tied_loss(plus, target) - tied_loss(minus, target)) / (2.0 * step))
    combined_error = max(abs(a - b) for a, b in zip(combined, numeric))
    output_only_error = max(abs(a - b) for a, b in zip(output_only, numeric))

    prior = [0.25] * 4
    y0 = [1.0, 0.0, 0.0, 0.0]
    y2 = [0.0, 0.0, 1.0, 0.0]
    smooth_after_mix = [
        (1.0 - epsilon) * (lam * y0[k] + (1.0 - lam) * y2[k])
        + epsilon * prior[k]
        for k in range(4)
    ]
    mix_after_smooth = [
        lam * ((1.0 - epsilon) * y0[k] + epsilon * prior[k])
        + (1.0 - lam) * ((1.0 - epsilon) * y2[k] + epsilon * prior[k])
        for k in range(4)
    ]
    commutation_error = max(abs(a - b) for a, b in zip(smooth_after_mix, mix_after_smooth))
    return combined_error, output_only_error, commutation_error


def dropout_moments() -> tuple[list[float], list[float]]:
    x = [2.0, -1.0]
    q = 0.75
    mean = x.copy()
    variance = [(1.0 - q) / q * value * value for value in x]
    return mean, variance


def build_svg() -> tuple[str, dict[str, float]]:
    epsilons, errors = central_difference_errors()
    curves = depth_gains()
    ln_error = layernorm_invariance_error()
    tied_error, missing_path_error, commutation_error = tied_gradient_errors()
    _, dropout_variance = dropout_moments()
    interaction = (0.20 - 0.26) - (0.27 - 0.30)

    out = begin(
        "神经网络基础累计复现门：梯度、深度尺度与共享随机合同",
        "同一张图分别检查数值梯度、深层 Jacobian 尺度和共享参数/随机目标；每个面板都只支持相应的实现恒等式与有限构造，不替代真实任务泛化证据。",
        (BLUE, TEAL, RED),
    )

    # A: central-difference gradient check.
    heading(out, 42, "A", "Forward / Reverse 数值对账", BLUE)
    ax_l, ax_r, ax_t, ax_b = 75.0, 355.0, 120.0, 382.0
    out += [
        line(ax_l, ax_b, ax_r, ax_b, INK, 2),
        line(ax_l, ax_t, ax_l, ax_b, INK, 2),
        text(214, 431, "finite-difference step exponent", 13, 600, "middle", MUTED),
        text(57, 226, "log10", 13, 600, "middle", MUTED),
        text(57, 244, "error", 13, 600, "middle", MUTED),
    ]
    points = []
    for index, (epsilon, error) in enumerate(zip(epsilons, errors)):
        exponent = -math.log10(epsilon)
        log_error = math.log10(error)
        x = ax_l + (exponent - 1.0) / 7.0 * (ax_r - ax_l)
        y = ax_b - (log_error + 11.0) / 9.0 * (ax_b - ax_t)
        points.append((x, y))
        out += [circle(x, y, 4.5, BLUE, BLUE, 1)]
        if index in (0, 3, 7):
            out += [text(x, ax_b + 22, f"1e-{int(exponent)}", 13, 600, "middle", MUTED)]
    out += [
        path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points), BLUE, 3),
        text(ax_l - 10, ax_t + 5, "-2", 13, 600, "end", MUTED),
        text(ax_l - 10, ax_b + 5, "-11", 13, 600, "end", MUTED),
        rect(52, 447, 310, 38, TEAL, "#ECFDF5", 5, 2),
        text(207, 472, f"best max error = {min(errors):.2e}", 15, 700, "middle", TEAL),
    ]

    # B: deep products and normalization invariant.
    heading(out, 430, "B", "深度尺度不是单层方差", TEAL)
    bx_l, bx_r, bx_t, bx_b = 470.0, 750.0, 120.0, 382.0
    out += [
        line(bx_l, bx_b, bx_r, bx_b, INK, 2),
        line(bx_l, bx_t, bx_l, bx_b, INK, 2),
        line(bx_l, bx_b - (55.0 / 59.0) * (bx_b - bx_t), bx_r, bx_b - (55.0 / 59.0) * (bx_b - bx_t), GRID, 1.5, "6 5"),
        text(610, 414, "depth", 14, 600, "middle", MUTED),
        text(452, 226, "log10", 13, 600, "middle", MUTED),
        text(452, 244, "|J gain|", 13, 600, "middle", MUTED),
    ]
    colors = {"plain": RED, "residual alpha=1": AMBER, "residual alpha=1/sqrt(L)": TEAL}
    for name, values in curves.items():
        points = []
        for index, value in enumerate(values, start=1):
            x = bx_l + (index - 1) / 63.0 * (bx_r - bx_l)
            log_gain = max(-55.0, min(4.0, math.log10(value)))
            y = bx_b - (log_gain + 55.0) / 59.0 * (bx_b - bx_t)
            points.append((x, y))
        out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points), colors[name], 3)]
    out += [
        text(480, 96, "plain", 12, 700, fill=RED),
        text(545, 96, "res alpha=1", 12, 700, fill=AMBER),
        text(650, 96, "res alpha=1/sqrt(L)", 12, 700, fill=TEAL),
        text(479, 110, "gain=1", 13, 600, fill=MUTED),
        text(600, 433, "end gains: plain 3.82e-54 · res 7.70e3 · scaled 3.30", 12, 650, "middle", MUTED),
        rect(445, 451, 310, 34, BLUE, "#EFF6FF", 5, 2),
        text(600, 474, f"LN(2x+5) vs LN(x): error {ln_error:.1e}", 14, 700, "middle", BLUE),
    ]

    # C: tied gradient paths and stochastic/target contracts.
    heading(out, 830, "C", "共享参数与随机目标必须合账", RED)
    cards = (
        ("tied E：两路梯度", f"combined error {tied_error:.2e}", TEAL),
        ("漏 lookup path", f"max error {missing_path_error:.3f}", RED),
        ("Mixup × smoothing", f"target difference {commutation_error:.1e}", BLUE),
        ("inverted dropout", f"Cov diag = ({dropout_variance[0]:.3f}, {dropout_variance[1]:.3f})", AMBER),
        ("2×2 interaction", f"Delta_AB = {interaction:.2f}", TEAL),
    )
    for index, (title_value, subtitle, color) in enumerate(cards):
        y = 82 + index * 82
        out += [
            rect(845, y, 286, 58, color, BG, 4, 1.8),
            text(861, y + 23, title_value, 15, 700, fill=color),
            text(1115, y + 47, subtitle, 14, 600, "end", MUTED),
        ]
    svg = finish(out, "累计门检查的是合同能否重建与复现；通过脚本不等于通过闭卷、迁移或真实任务实验。")
    metrics = {
        "mlp_loss": mlp_loss([
            1.0, -1.0, 0.5, 0.5, 0.0, 1.0,
            1.0, 0.0, -1.0, 2.0, 0.5, -1.0,
            0.0, 0.5, -0.5,
        ]),
        "best_gradient_error": min(errors),
        "plain_gain": curves["plain"][-1],
        "residual_gain": curves["residual alpha=1"][-1],
        "scaled_gain": curves["residual alpha=1/sqrt(L)"][-1],
        "layernorm_error": ln_error,
        "tied_gradient_error": tied_error,
        "missing_path_error": missing_path_error,
        "commutation_error": commutation_error,
        "dropout_var_0": dropout_variance[0],
        "dropout_var_1": dropout_variance[1],
        "interaction": interaction,
    }
    return svg, metrics


def main() -> None:
    svg, metrics = build_svg()
    assert metrics["best_gradient_error"] < 1e-8
    assert metrics["plain_gain"] < 1e-40
    assert metrics["residual_gain"] > 1e3
    assert 2.0 < metrics["scaled_gain"] < 4.0
    assert metrics["layernorm_error"] < 1e-12
    assert metrics["tied_gradient_error"] < 1e-8
    assert metrics["missing_path_error"] > 0.5
    assert metrics["commutation_error"] < 1e-12
    assert math.isclose(metrics["dropout_var_0"], 4.0 / 3.0)
    assert math.isclose(metrics["dropout_var_1"], 1.0 / 3.0)
    assert math.isclose(metrics["interaction"], -0.03)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(OUT)
    print(
        "mlp_loss={mlp_loss:.8f} best_grad_error={best_gradient_error:.3e} "
        "plain_gain={plain_gain:.3e} residual_gain={residual_gain:.5f} "
        "scaled_gain={scaled_gain:.5f}".format(**metrics)
    )
    print(
        "tied_error={tied_gradient_error:.3e} missing_path_error={missing_path_error:.6f} "
        "commutation_error={commutation_error:.1e} interaction={interaction:.2f}".format(**metrics)
    )


if __name__ == "__main__":
    main()
