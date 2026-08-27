#!/usr/bin/env python3
"""Deterministic audit for reverse-time diffusion, score identities, and sampler errors.

Standard-library only.  The script writes one canonical SVG and exits non-zero
when any mathematical or numerical acceptance gate fails.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SVG_PATH = ROOT / "_assets/plots/dynamics/plot-reverse-time-score-diffusion-v2.svg"

BETA = 2.0
T_FINAL = 2.0
M0 = 1.2
V0 = 0.3


def forward_moments(t: float) -> tuple[float, float]:
    decay = math.exp(-BETA * t)
    return M0 * math.sqrt(decay), 1.0 + (V0 - 1.0) * decay


def score_gaussian(t: float, x: float) -> float:
    mean, var = forward_moments(t)
    return -(x - mean) / var


def reverse_drift(t: float, x: float, score_scale: float = 1.0) -> float:
    # Forward-s reverse clock Y_s=X_{T-s}: -f + D score.
    return 0.5 * BETA * x + BETA * score_scale * score_gaussian(t, x)


def backward_conditional_mean(t: float, h: float, x: float) -> float:
    prev_mean, prev_var = forward_moments(t - h)
    now_mean, now_var = forward_moments(t)
    transition = math.exp(-0.5 * BETA * h)
    covariance = transition * prev_var
    return prev_mean + covariance / now_var * (x - now_mean)


def rms(values: list[float]) -> float:
    return math.sqrt(sum(v * v for v in values) / len(values))


def fit_order(step_sizes: list[float], errors: list[float]) -> float:
    xs = [math.log(h) for h in step_sizes]
    ys = [math.log(e) for e in errors]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / sum(
        (x - xbar) ** 2 for x in xs
    )


def reverse_drift_gate() -> tuple[list[float], list[float], float]:
    t = 1.2
    hs = [0.2, 0.1, 0.05, 0.025, 0.0125]
    xs = [-2.0 + 0.25 * i for i in range(21)]
    errors = []
    for h in hs:
        local_errors = []
        for x in xs:
            finite_h = (backward_conditional_mean(t, h, x) - x) / h
            local_errors.append(finite_h - reverse_drift(t, x))
        errors.append(rms(local_errors))
    return hs, errors, fit_order(hs, errors)


MIX_MEAN = 2.0
MIX_VAR = 0.16
ALPHA = 0.75
SIGMA = 0.8
NOISY_COMPONENT_VAR = ALPHA * ALPHA * MIX_VAR + SIGMA * SIGMA


def gaussian_pdf(x: float, mean: float, var: float) -> float:
    return math.exp(-0.5 * (x - mean) ** 2 / var) / math.sqrt(2.0 * math.pi * var)


def mixture_quantities(x: float) -> tuple[float, float, float, float]:
    component_means = (-MIX_MEAN, MIX_MEAN)
    likelihoods = [
        0.5 * gaussian_pdf(x, ALPHA * mean, NOISY_COMPONENT_VAR)
        for mean in component_means
    ]
    total = sum(likelihoods)
    weights = [value / total for value in likelihoods]

    component_scores = [
        -(x - ALPHA * mean) / NOISY_COMPONENT_VAR for mean in component_means
    ]
    marginal_score = sum(w * s for w, s in zip(weights, component_scores))

    covariance = ALPHA * MIX_VAR
    posterior_component_means = [
        mean
        + covariance / NOISY_COMPONENT_VAR * (x - ALPHA * mean)
        for mean in component_means
    ]
    posterior_mean = sum(
        w * mean for w, mean in zip(weights, posterior_component_means)
    )
    conditional_target_average = -(x - ALPHA * posterior_mean) / (SIGMA * SIGMA)
    tweedie_mean = (x + SIGMA * SIGMA * marginal_score) / ALPHA
    return marginal_score, conditional_target_average, posterior_mean, tweedie_mean


def score_identity_gate() -> tuple[list[float], list[float], list[float], float, float]:
    xs = [-4.5 + 0.05 * i for i in range(181)]
    scores = []
    denoisers = []
    score_errors = []
    tweedie_errors = []
    for x in xs:
        score, conditional_average, posterior_mean, tweedie_mean = mixture_quantities(x)
        scores.append(score)
        denoisers.append(posterior_mean)
        score_errors.append(abs(score - conditional_average))
        tweedie_errors.append(abs(posterior_mean - tweedie_mean))
    return xs, scores, denoisers, max(score_errors), max(tweedie_errors)


def reverse_moment_euler(
    steps: int,
    *,
    score_scale: float = 1.0,
    terminal_mean: float | None = None,
    terminal_var: float | None = None,
    score_coefficient: float = 1.0,
) -> tuple[float, float]:
    mean_t, var_t = forward_moments(T_FINAL)
    mean = mean_t if terminal_mean is None else terminal_mean
    var = var_t if terminal_var is None else terminal_var
    h = T_FINAL / steps
    for n in range(steps):
        s = n * h
        t = T_FINAL - s
        target_mean, target_var = forward_moments(t)
        # -f + coefficient * D * estimated score.
        a = BETA * (0.5 - score_coefficient * score_scale / target_var)
        c = BETA * score_coefficient * score_scale * target_mean / target_var
        multiplier = 1.0 + a * h
        mean = multiplier * mean + c * h
        var = multiplier * multiplier * var + BETA * h
    return mean, var


def probability_flow_moment_euler(steps: int) -> tuple[float, float]:
    mean, var = forward_moments(T_FINAL)
    h = T_FINAL / steps
    for n in range(steps):
        t = T_FINAL - n * h
        target_mean, target_var = forward_moments(t)
        # Reverse-s probability flow: -f + (D/2) score, no diffusion.
        a = 0.5 * BETA * (1.0 - 1.0 / target_var)
        c = 0.5 * BETA * target_mean / target_var
        multiplier = 1.0 + a * h
        mean = multiplier * mean + c * h
        var = multiplier * multiplier * var
    return mean, var


def moment_error(mean: float, var: float) -> float:
    return math.sqrt((mean - M0) ** 2 + (var - V0) ** 2)


def sampler_gate() -> dict[str, object]:
    steps = [16, 32, 64, 128, 256, 512]
    hs = [T_FINAL / n for n in steps]
    sde_errors = []
    pf_errors = []
    sde_moments = []
    pf_moments = []
    for n in steps:
        sde = reverse_moment_euler(n)
        pf = probability_flow_moment_euler(n)
        sde_moments.append(sde)
        pf_moments.append(pf)
        sde_errors.append(moment_error(*sde))
        pf_errors.append(moment_error(*pf))

    fine_steps = 4096
    exact_fine = moment_error(*reverse_moment_euler(fine_steps))
    score_bias = moment_error(
        *reverse_moment_euler(fine_steps, score_scale=1.10)
    )
    prior_bias = moment_error(
        *reverse_moment_euler(fine_steps, terminal_mean=0.0, terminal_var=1.0)
    )
    half_coefficient_bias = moment_error(
        *reverse_moment_euler(fine_steps, score_coefficient=0.5)
    )
    return {
        "steps": steps,
        "hs": hs,
        "sde_errors": sde_errors,
        "pf_errors": pf_errors,
        "sde_moments": sde_moments,
        "pf_moments": pf_moments,
        "sde_order": fit_order(hs, sde_errors),
        "pf_order": fit_order(hs, pf_errors),
        "exact_fine": exact_fine,
        "score_bias": score_bias,
        "prior_bias": prior_bias,
        "half_coefficient_bias": half_coefficient_bias,
    }


def polyline(
    points: list[tuple[float, float]],
    *,
    color: str,
    width: float = 2.2,
    dash: str | None = None,
) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{dash_attr}/>'
    )


def map_points(
    xs: list[float],
    ys: list[float],
    left: float,
    top: float,
    width: float,
    height: float,
    *,
    log_x: bool = False,
    log_y: bool = False,
    y_min: float | None = None,
    y_max: float | None = None,
) -> list[tuple[float, float]]:
    tx = [math.log10(x) if log_x else x for x in xs]
    ty = [math.log10(y) if log_y else y for y in ys]
    xmin, xmax = min(tx), max(tx)
    ymin = min(ty) if y_min is None else y_min
    ymax = max(ty) if y_max is None else y_max
    return [
        (
            left + (x - xmin) / (xmax - xmin) * width,
            top + (ymax - y) / (ymax - ymin) * height,
        )
        for x, y in zip(tx, ty)
    ]


def write_svg(
    drift_hs: list[float],
    drift_errors: list[float],
    drift_order: float,
    mix_xs: list[float],
    mix_scores: list[float],
    mix_denoisers: list[float],
    score_identity_error: float,
    tweedie_error: float,
    sampler: dict[str, object],
) -> str:
    width, height = 1200, 430
    panel_w = 370
    panels = [20, 410, 800]

    drift_points = map_points(
        drift_hs,
        drift_errors,
        75,
        145,
        270,
        145,
        log_x=True,
        log_y=True,
    )
    score_points = map_points(
        mix_xs,
        mix_scores,
        465,
        145,
        270,
        145,
        y_min=-3.2,
        y_max=3.2,
    )
    denoiser_points = map_points(
        mix_xs,
        mix_denoisers,
        465,
        145,
        270,
        145,
        y_min=-3.2,
        y_max=3.2,
    )
    hs = sampler["hs"]
    sde_errors = sampler["sde_errors"]
    pf_errors = sampler["pf_errors"]
    all_errors = list(sde_errors) + list(pf_errors) + [
        sampler["score_bias"],
        sampler["prior_bias"],
        sampler["half_coefficient_bias"],
    ]
    y_min = math.log10(min(all_errors)) - 0.08
    y_max = math.log10(max(all_errors)) + 0.08
    sde_points = map_points(
        hs,
        sde_errors,
        855,
        145,
        270,
        145,
        log_x=True,
        log_y=True,
        y_min=y_min,
        y_max=y_max,
    )
    pf_points = map_points(
        hs,
        pf_errors,
        855,
        145,
        270,
        145,
        log_x=True,
        log_y=True,
        y_min=y_min,
        y_max=y_max,
    )

    def horizontal(value: float, color: str, dash: str) -> str:
        y = 145 + (y_max - math.log10(value)) / (y_max - y_min) * 145
        return f'<line x1="855" y1="{y:.2f}" x2="1125" y2="{y:.2f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>'

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">DYN-12 reverse-time score diffusion audit</title>',
        '<desc id="desc">Three panels audit the finite-h reverse drift limit, denoising score and Tweedie identities on a Gaussian mixture, and separate exact-score solver convergence from score, terminal-prior, and coefficient errors.</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;font-variant-numeric:tabular-nums lining-nums}</style>',
        '<rect width="1200" height="430" fill="#ffffff"/>',
        '<text x="20" y="32" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="24" font-weight="700" fill="#0f172a">DYN-12 · 反向漂移 → score 恒等式 → 误差分账</text>',
    ]
    for x in panels:
        svg.append(f'<rect x="{x}" y="55" width="{panel_w}" height="355" fill="#fffefb" stroke="#d6dee8" stroke-width="1.5"/>')

    svg.extend(
        [
            '<text x="42" y="88" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="22" font-weight="700" fill="#0f172a">A　Bayes → 反向漂移</text>',
            '<text x="75" y="122" font-family="Georgia,serif" font-size="15" font-weight="600" fill="#2563eb">backward-drift RMSE / h</text>',
            '<line x1="75" y1="145" x2="75" y2="290" stroke="#94a3b8"/><line x1="75" y1="290" x2="345" y2="290" stroke="#94a3b8"/>',
            polyline(drift_points, color="#2563eb"),
            '<text x="75" y="318" font-family="Georgia,serif" font-size="15" fill="#475569">h (coarser →)</text>',
            f'<text x="75" y="348" font-family="Georgia,serif" font-size="17" font-weight="700" fill="#0f172a">observed order = {drift_order:.4f}</text>',
            '<text x="75" y="378" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="15" fill="#047857">极限含 D score；不是 dt 取负</text>',
            '<text x="432" y="88" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="22" font-weight="700" fill="#0f172a">B　DSM / Tweedie</text>',
            '<text x="465" y="122" font-family="Georgia,serif" font-size="15" font-weight="600" fill="#7c3aed">score · posterior denoiser</text>',
            '<line x1="465" y1="145" x2="465" y2="290" stroke="#94a3b8"/><line x1="465" y1="217.5" x2="735" y2="217.5" stroke="#cbd5e1" stroke-dasharray="5 4"/><line x1="465" y1="290" x2="735" y2="290" stroke="#94a3b8"/>',
            polyline(score_points, color="#7c3aed"),
            polyline(denoiser_points, color="#059669"),
            '<text x="465" y="318" font-family="Georgia,serif" font-size="15" fill="#475569">noisy observation x_t</text>',
            f'<text x="465" y="348" font-family="Georgia,serif" font-size="15" font-weight="700" fill="#0f172a">DSM max err = {score_identity_error:.1e}</text>',
            f'<text x="465" y="375" font-family="Georgia,serif" font-size="15" fill="#047857">Tweedie max err = {tweedie_error:.1e}</text>',
            '<text x="822" y="88" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="22" font-weight="700" fill="#0f172a">C　solver 与误差地板</text>',
            '<text x="855" y="122" font-family="Georgia,serif" font-size="15" font-weight="600" fill="#0f172a">terminal moment error (log-log)</text>',
            '<line x1="855" y1="145" x2="855" y2="290" stroke="#94a3b8"/><line x1="855" y1="290" x2="1125" y2="290" stroke="#94a3b8"/>',
            horizontal(float(sampler["score_bias"]), "#dc2626", "6 4"),
            horizontal(float(sampler["prior_bias"]), "#d97706", "3 3"),
            horizontal(float(sampler["half_coefficient_bias"]), "#64748b", "9 4"),
            polyline(sde_points, color="#2563eb"),
            polyline(pf_points, color="#059669"),
            '<text x="855" y="318" font-family="Georgia,serif" font-size="15" fill="#475569">h (coarser →)</text>',
            f'<text x="855" y="345" font-family="Georgia,serif" font-size="15" font-weight="700" fill="#2563eb">SDE p={float(sampler["sde_order"]):.3f}</text>',
            f'<text x="1025" y="345" font-family="Georgia,serif" font-size="15" font-weight="700" fill="#059669">PF p={float(sampler["pf_order"]):.3f}</text>',
            '<text x="855" y="372" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="15" fill="#dc2626">score+10%</text><text x="956" y="372" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="15" fill="#d97706">prior</text><text x="1063" y="372" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="15" fill="#64748b">half drift</text>',
            '<text x="855" y="397" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif" font-size="15" fill="#0f172a">h 只消除 solver error</text>',
            '</svg>',
        ]
    )
    content = "\n".join(svg) + "\n"
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(content, encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def main() -> None:
    drift_hs, drift_errors, drift_order = reverse_drift_gate()
    mix_xs, mix_scores, mix_denoisers, score_error, tweedie_error = score_identity_gate()
    sampler = sampler_gate()

    assert 0.85 < drift_order < 1.15
    assert score_error < 2.0e-14
    assert tweedie_error < 2.0e-14
    assert 0.85 < float(sampler["sde_order"]) < 1.20
    assert 0.85 < float(sampler["pf_order"]) < 1.20
    assert float(sampler["exact_fine"]) < 2.0e-3
    assert float(sampler["score_bias"]) > 2.0e-2
    assert float(sampler["prior_bias"]) > 5.0e-3
    assert float(sampler["half_coefficient_bias"]) > 2.0e-1

    digest = write_svg(
        drift_hs,
        drift_errors,
        drift_order,
        mix_xs,
        mix_scores,
        mix_denoisers,
        score_error,
        tweedie_error,
        sampler,
    )

    print("reverse drift finite-h gate")
    for h, error in zip(drift_hs, drift_errors):
        print(f"h={h:.6f} rmse={error:.10e}")
    print(f"reverse drift order={drift_order:.8f}")
    print(f"DSM identity max error={score_error:.10e}")
    print(f"Tweedie identity max error={tweedie_error:.10e}")
    print("reverse sampler moment gate")
    for n, sde, pf, se, pe in zip(
        sampler["steps"],
        sampler["sde_moments"],
        sampler["pf_moments"],
        sampler["sde_errors"],
        sampler["pf_errors"],
    ):
        print(
            f"N={n:4d} SDE mean/var={sde[0]:.9f}/{sde[1]:.9f} err={se:.9e} "
            f"PF mean/var={pf[0]:.9f}/{pf[1]:.9f} err={pe:.9e}"
        )
    print(f"reverse SDE order={float(sampler['sde_order']):.8f}")
    print(f"probability-flow order={float(sampler['pf_order']):.8f}")
    print(f"fine exact-score error={float(sampler['exact_fine']):.9e}")
    print(f"score +10% bias floor={float(sampler['score_bias']):.9e}")
    print(f"terminal prior mismatch floor={float(sampler['prior_bias']):.9e}")
    print(f"half-score reverse-SDE floor={float(sampler['half_coefficient_bias']):.9e}")
    print(f"svg_sha256={digest}")


if __name__ == "__main__":
    main()
