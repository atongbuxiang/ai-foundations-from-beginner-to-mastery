#!/usr/bin/env python3
"""Generate the deterministic neural-network-foundations cumulative gate.

The three panels audit different contracts instead of reporting a model score:
1. forward/reverse consistency for a small ReLU MLP;
2. depth scaling and a LayerNorm invariance check;
3. tied-embedding gradient paths plus stochastic/target identities.
"""

from __future__ import annotations

import argparse
import hashlib
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


DEFAULT_OUTPUT = (
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


def mlp_loss(params: list[float], x: list[float], target: int) -> float:
    w1 = [params[0:2], params[2:4]]
    b1 = params[4:6]
    w2 = [params[6:8], params[8:10], params[10:12]]
    b2 = params[12:15]
    a = [sum(w1[i][j] * x[j] for j in range(2)) + b1[i] for i in range(2)]
    h = [max(0.0, value) for value in a]
    z = [sum(w2[k][j] * h[j] for j in range(2)) + b2[k] for k in range(3)]
    shift = max(z)
    return -z[target] + shift + math.log(sum(math.exp(value - shift) for value in z))


def mlp_gradient(params: list[float], x: list[float], target: int) -> list[float]:
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


def central_difference_errors(x: list[float], target: int) -> tuple[list[float], list[float]]:
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
    analytic = mlp_gradient(params, x, target)
    epsilons = [10.0 ** (-k) for k in range(1, 9)]
    errors: list[float] = []
    for epsilon in epsilons:
        numeric = []
        for index in range(len(params)):
            plus = params.copy()
            minus = params.copy()
            plus[index] += epsilon
            minus[index] -= epsilon
            numeric.append(
                (mlp_loss(plus, x, target) - mlp_loss(minus, x, target))
                / (2.0 * epsilon)
            )
        errors.append(max(abs(a - b) for a, b in zip(analytic, numeric)))
    return epsilons, errors


def depth_gains(
    depth: int,
    weight_base: float,
    weight_amplitude: float,
    weight_frequency: float,
) -> dict[str, list[float]]:
    weights = [
        weight_base + weight_amplitude * math.sin(weight_frequency * (index + 1))
        for index in range(depth)
    ]
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


def layernorm_invariance_error(scale: float, shift: float) -> float:
    x = [1.0, 2.0, 3.0]

    def normalize(values: list[float]) -> list[float]:
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        return [(value - mean) / math.sqrt(variance) for value in values]

    lhs = normalize([scale * value + shift for value in x])
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


def tied_gradient_errors(
    lam: float,
    epsilon: float,
    step: float,
) -> tuple[float, float, float]:
    embedding = [1.0, 0.0, 0.0, 2.0, 1.0, 1.0, 0.0, 0.0]
    mixed = [lam, 0.0, 1.0 - lam, 0.0]
    target = [(1.0 - epsilon) * value + epsilon / 4.0 for value in mixed]
    combined, output_only = tied_gradients(embedding, target)
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


def dropout_moments(q: float) -> tuple[list[float], list[float]]:
    x = [2.0, -1.0]
    mean = x.copy()
    variance = [(1.0 - q) / q * value * value for value in x]
    return mean, variance


def build_svg(args: argparse.Namespace) -> tuple[str, dict[str, float]]:
    mlp_input = [args.x0, args.x1]
    epsilons, errors = central_difference_errors(mlp_input, args.target)
    curves = depth_gains(
        args.depth,
        args.weight_base,
        args.weight_amplitude,
        args.weight_frequency,
    )
    ln_error = layernorm_invariance_error(args.ln_scale, args.ln_shift)
    tied_error, missing_path_error, commutation_error = tied_gradient_errors(
        args.mix_lambda,
        args.label_epsilon,
        args.tied_step,
    )
    _, dropout_variance = dropout_moments(args.dropout_q)
    interaction = (
        (args.risk11 - args.risk10)
        - (args.risk01 - args.risk00)
    )
    mixed = [args.mix_lambda, 0.0, 1.0 - args.mix_lambda, 0.0]
    target = [
        (1.0 - args.label_epsilon) * value + args.label_epsilon / 4.0
        for value in mixed
    ]

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
        text(7, 236, "log10 error", 11, 600, fill=MUTED),
        text(215, 108, f"x=({args.x0:g},{args.x1:g}) · target={args.target + 1}", 12, 650, "middle", MUTED),
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
    heading(out, 430, "B", f"深度尺度：L={args.depth}", TEAL)
    bx_l, bx_r, bx_t, bx_b = 470.0, 750.0, 120.0, 382.0
    out += [
        line(bx_l, bx_b, bx_r, bx_b, INK, 2),
        line(bx_l, bx_t, bx_l, bx_b, INK, 2),
        line(bx_l, bx_b - (55.0 / 59.0) * (bx_b - bx_t), bx_r, bx_b - (55.0 / 59.0) * (bx_b - bx_t), GRID, 1.5, "6 5"),
        text(610, 414, "depth", 14, 600, "middle", MUTED),
        text(407, 236, "log10 |J|", 12, 600, fill=MUTED),
    ]
    colors = {"plain": RED, "residual alpha=1": AMBER, "residual alpha=1/sqrt(L)": TEAL}
    for name, values in curves.items():
        points = []
        for index, value in enumerate(values, start=1):
            x = bx_l + (index - 1) / max(1.0, args.depth - 1.0) * (bx_r - bx_l)
            log_gain = max(-55.0, min(4.0, math.log10(value)))
            y = bx_b - (log_gain + 55.0) / 59.0 * (bx_b - bx_t)
            points.append((x, y))
        out += [path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points), colors[name], 3)]
    out += [
        text(480, 96, "plain", 12, 700, fill=RED),
        text(545, 96, "res alpha=1", 12, 700, fill=AMBER),
        text(650, 96, "res alpha=1/sqrt(L)", 12, 700, fill=TEAL),
        text(479, 110, "gain=1", 13, 600, fill=MUTED),
        text(445, 433, f"plain {curves['plain'][-1]:.2e}", 11, 650, fill=RED),
        text(
            610,
            433,
            f"res {curves['residual alpha=1'][-1]:.2e}",
            11,
            650,
            "middle",
            AMBER,
        ),
        text(
            755,
            433,
            f"scaled {curves['residual alpha=1/sqrt(L)'][-1]:.2f}",
            11,
            650,
            "end",
            TEAL,
        ),
        rect(445, 451, 310, 34, BLUE, "#EFF6FF", 5, 2),
        text(
            600,
            474,
            f"LN({args.ln_scale:g}x{args.ln_shift:+g}) vs LN(x): error {ln_error:.1e}",
            14,
            700,
            "middle",
            BLUE,
        ),
    ]

    # C: tied gradient paths and stochastic/target contracts.
    heading(
        out,
        830,
        "C",
        f"共享目标：λ={args.mix_lambda:g}, ε={args.label_epsilon:g}, q={args.dropout_q:g}",
        RED,
    )
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
        "mlp_loss": mlp_loss(
            [
                1.0, -1.0, 0.5, 0.5, 0.0, 1.0,
                1.0, 0.0, -1.0, 2.0, 0.5, -1.0,
                0.0, 0.5, -0.5,
            ],
            mlp_input,
            args.target,
        ),
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
        "target_0": target[0],
        "target_1": target[1],
        "target_2": target[2],
        "target_3": target[3],
    }
    return svg, metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--x0", type=float, default=1.0)
    parser.add_argument("--x1", type=float, default=-2.0)
    parser.add_argument("--target", type=int, default=2, choices=range(3))
    parser.add_argument("--depth", type=int, default=64)
    parser.add_argument("--weight-base", type=float, default=0.15)
    parser.add_argument("--weight-amplitude", type=float, default=0.05)
    parser.add_argument("--weight-frequency", type=float, default=0.7)
    parser.add_argument("--ln-scale", type=float, default=2.0)
    parser.add_argument("--ln-shift", type=float, default=5.0)
    parser.add_argument("--mix-lambda", type=float, default=0.3)
    parser.add_argument("--label-epsilon", type=float, default=0.2)
    parser.add_argument("--dropout-q", type=float, default=0.75)
    parser.add_argument("--tied-step", type=float, default=1e-5)
    parser.add_argument("--risk00", type=float, default=0.30)
    parser.add_argument("--risk10", type=float, default=0.26)
    parser.add_argument("--risk01", type=float, default=0.27)
    parser.add_argument("--risk11", type=float, default=0.20)
    return parser.parse_args()


def is_canonical(args: argparse.Namespace) -> bool:
    defaults = {
        "x0": 1.0,
        "x1": -2.0,
        "target": 2,
        "depth": 64,
        "weight_base": 0.15,
        "weight_amplitude": 0.05,
        "weight_frequency": 0.7,
        "ln_scale": 2.0,
        "ln_shift": 5.0,
        "mix_lambda": 0.3,
        "label_epsilon": 0.2,
        "dropout_q": 0.75,
        "tied_step": 1e-5,
        "risk00": 0.30,
        "risk10": 0.26,
        "risk01": 0.27,
        "risk11": 0.20,
    }
    return all(getattr(args, key) == value for key, value in defaults.items())


def validate_args(args: argparse.Namespace) -> None:
    if args.depth < 2:
        raise SystemExit("--depth must be at least 2")
    if args.weight_base <= abs(args.weight_amplitude):
        raise SystemExit("--weight-base must exceed abs(--weight-amplitude)")
    if args.ln_scale <= 0.0:
        raise SystemExit("--ln-scale must be positive")
    if not 0.0 <= args.mix_lambda <= 1.0:
        raise SystemExit("--mix-lambda must lie in [0, 1]")
    if not 0.0 <= args.label_epsilon <= 1.0:
        raise SystemExit("--label-epsilon must lie in [0, 1]")
    if not 0.0 < args.dropout_q <= 1.0:
        raise SystemExit("--dropout-q must lie in (0, 1]")
    if args.tied_step <= 0.0:
        raise SystemExit("--tied-step must be positive")
    # Keep the whole finite-difference sweep inside one ReLU activation region.
    preactivations = (
        args.x0 - args.x1,
        0.5 * args.x0 + 0.5 * args.x1 + 1.0,
    )
    if min(preactivations) <= 0.2:
        raise SystemExit("chosen input is too close to a ReLU kink for the canonical finite-difference sweep")


def main() -> None:
    args = parse_args()
    validate_args(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical runs require --output so the canonical SVG is not overwritten")
    output = (args.output or DEFAULT_OUTPUT).expanduser().resolve()
    svg, metrics = build_svg(args)
    assert metrics["best_gradient_error"] < 1e-7
    assert metrics["layernorm_error"] < 1e-12
    assert metrics["tied_gradient_error"] < 1e-7
    assert metrics["missing_path_error"] > 0.1
    assert metrics["commutation_error"] < 1e-12
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(
        f"A_CONFIG x0={args.x0:g} x1={args.x1:g} target={args.target + 1} "
        "fd_exponents=1:8"
    )
    print(
        "A_GRADIENT mlp_loss={mlp_loss:.8f} best_grad_error={best_gradient_error:.3e}".format(
            **metrics
        )
    )
    print(
        f"B_CONFIG depth={args.depth} weight_base={args.weight_base:g} "
        f"weight_amplitude={args.weight_amplitude:g} weight_frequency={args.weight_frequency:g}"
    )
    print(
        "B_GAINS plain={plain_gain:.8e} residual={residual_gain:.8f} "
        "scaled={scaled_gain:.8f}".format(**metrics)
    )
    print(
        f"B_LAYERNORM scale={args.ln_scale:g} shift={args.ln_shift:g} "
        f"error={metrics['layernorm_error']:.3e}"
    )
    print(
        f"C_CONFIG mix_lambda={args.mix_lambda:g} label_epsilon={args.label_epsilon:g} "
        f"dropout_q={args.dropout_q:g} tied_step={args.tied_step:g}"
    )
    print(
        "C_TARGET values={target_0:.8f},{target_1:.8f},{target_2:.8f},{target_3:.8f}".format(
            **metrics
        )
    )
    print(
        "C_REGULARIZATION tied_error={tied_gradient_error:.3e} "
        "missing_path_error={missing_path_error:.6f} "
        "commutation_error={commutation_error:.1e} "
        "dropout_var={dropout_var_0:.8f},{dropout_var_1:.8f} "
        "interaction={interaction:.8f}".format(**metrics)
    )
    print(f"OUTPUT {output}")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()
