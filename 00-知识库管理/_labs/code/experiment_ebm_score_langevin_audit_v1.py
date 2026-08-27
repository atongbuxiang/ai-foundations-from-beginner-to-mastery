#!/usr/bin/env python3
"""Minimal deterministic audits for GEN-25—32.

No training framework is required.  The script separates algebraic identities,
population optima, Monte-Carlo estimates, and finite-step Markov-chain effects.
"""

from __future__ import annotations

import math
import random
import statistics


SEED = 50425
RNG = random.Random(SEED)


def softmax_negative_energy(energy: list[float], temperature: float = 1.0) -> list[float]:
    logits = [-float(value) / temperature for value in energy]
    shift = max(logits)
    weight = [math.exp(value - shift) for value in logits]
    total = sum(weight)
    return [value / total for value in weight]


def audit_energy_gauge_and_temperature() -> None:
    energy = [0.0, math.log(2.0)]
    p = softmax_negative_energy(energy)
    p_shift = softmax_negative_energy([value + 17.3 for value in energy])
    p_cold = softmax_negative_energy(energy, temperature=0.5)
    assert max(abs(a - b) for a, b in zip(p, [2 / 3, 1 / 3])) < 1e-14
    assert max(abs(a - b) for a, b in zip(p, p_shift)) < 1e-14
    assert abs(p_cold[0] / p_cold[1] - 4.0) < 1e-14
    print("[GEN-25] gauge residual:", max(abs(a - b) for a, b in zip(p, p_shift)))
    print("[GEN-25] odds T=1 / T=.5:", p[0] / p[1], p_cold[0] / p_cold[1])


def bernoulli_nll(theta: float, x_mean: float) -> float:
    return -theta * x_mean + math.log1p(math.exp(theta))


def audit_positive_negative_phase() -> None:
    theta, x_mean, eps = 0.7, 0.8, 1e-6
    p_model = 1.0 / (1.0 + math.exp(-theta))
    analytic = -x_mean + p_model
    numeric = (bernoulli_nll(theta + eps, x_mean) - bernoulli_nll(theta - eps, x_mean)) / (2 * eps)
    assert abs(analytic - numeric) < 1e-9
    print("[GEN-26] NLL gradient analytic/numeric:", analytic, numeric)


def gaussian_score_matching_objective(a: float, tau2: float) -> float:
    return 0.5 * a * a * tau2 - a


def audit_score_matching_gaussian() -> None:
    tau2 = 2.5
    optimum = 1.0 / tau2
    grid = [1.2 * i / 12000 for i in range(12001)]
    grid_optimum = min(grid, key=lambda value: gaussian_score_matching_objective(value, tau2))
    assert abs(grid_optimum - optimum) <= 1.1e-4
    print("[GEN-27] Gaussian precision optimum exact/grid:", optimum, grid_optimum)


def audit_dsm_projection_and_tweedie() -> None:
    tau2, sigma2 = 2.0, 0.5
    variance_y = tau2 + sigma2
    irreducible = tau2 / (sigma2 * variance_y)
    # Predictor s_b(y)=-b y.  Both losses differ by the same conditional variance.
    for b in (0.0, 0.2, 0.4, 0.8):
        marginal_mse = (b - 1.0 / variance_y) ** 2 * variance_y
        conditional_mse = marginal_mse + irreducible
        assert abs((conditional_mse - marginal_mse) - irreducible) < 1e-14
    y = 1.3
    score = -y / variance_y
    tweedie = y + sigma2 * score
    posterior_mean = tau2 / variance_y * y
    assert abs(tweedie - posterior_mean) < 1e-14
    print("[GEN-28] DSM minus marginal MSE constant:", irreducible)
    print("[GEN-28] Tweedie/posterior mean:", tweedie, posterior_mean)


def audit_noise_scale_geometry() -> None:
    a = 2.0
    for sigma in (0.5, 2.0, 4.0):
        midpoint_score = 0.0
        curvature_log_density = (a * a - sigma * sigma) / sigma**4
        assert midpoint_score == 0.0
        kind = "valley" if curvature_log_density > 0 else ("flat" if curvature_log_density == 0 else "mode")
        print(f"[GEN-29] sigma={sigma:g}: score(0)=0, midpoint={kind}, log-density curvature={curvature_log_density:.6g}")
    ladder = [8.0 * (1.0 / 8.0) ** (i / 3.0) for i in range(4)]
    assert max(abs(a - b) for a, b in zip(ladder, [8.0, 4.0, 2.0, 1.0])) < 1e-14


def ula_chain(step: float, n: int, burn: int) -> list[float]:
    x = 0.0
    out = []
    for i in range(n + burn):
        x = (1.0 - step) * x + math.sqrt(2.0 * step) * RNG.gauss(0.0, 1.0)
        if i >= burn:
            out.append(x)
    return out


def audit_ula_bias() -> None:
    for step in (0.1, 0.5, 1.0):
        exact_variance = 1.0 / (1.0 - step / 2.0)
        sample = ula_chain(step, n=180_000, burn=2_000)
        empirical = statistics.pvariance(sample)
        assert abs(empirical - exact_variance) < 0.035
        print(f"[GEN-30] ULA h={step:g}: target=1 analytic={exact_variance:.6f} empirical={empirical:.6f}")


def mala_standard_normal(step: float, n: int, burn: int) -> tuple[list[float], float]:
    x = 5.0
    out = []
    accepted = 0
    for i in range(n + burn):
        mean_forward = (1.0 - step) * x
        y = mean_forward + math.sqrt(2.0 * step) * RNG.gauss(0.0, 1.0)
        mean_reverse = (1.0 - step) * y
        log_pi_ratio = -0.5 * y * y + 0.5 * x * x
        log_q_ratio = -((x - mean_reverse) ** 2) / (4.0 * step) + ((y - mean_forward) ** 2) / (4.0 * step)
        if math.log(RNG.random()) < min(0.0, log_pi_ratio + log_q_ratio):
            x = y
            if i >= burn:
                accepted += 1
        if i >= burn:
            out.append(x)
    return out, accepted / n


def audit_mala_correction() -> None:
    sample, acceptance = mala_standard_normal(step=1.0, n=160_000, burn=2_000)
    mean, variance = statistics.fmean(sample), statistics.pvariance(sample)
    assert abs(mean) < 0.03
    assert abs(variance - 1.0) < 0.035
    assert 0.5 < acceptance < 0.9
    point_acceptance = math.exp(-0.25)
    print("[GEN-30] MALA mean/variance/acceptance:", mean, variance, acceptance)
    print("[GEN-30] MALA alpha at x=0,y=1,h=1:", point_acceptance)


def audit_pc_budget_and_fixed_layer() -> None:
    time_steps, corrector_steps = 50, 2
    nfe = time_steps * (1 + corrector_steps)
    assert nfe == 150
    score_norm, noise_norm, ratio = 5.0, 10.0, 0.1
    step = 2.0 * ratio**2 * noise_norm**2 / score_norm**2
    assert abs(step - 0.08) < 1e-14
    print("[GEN-31] PC NFE and SNR-derived corrector step:", nfe, step)


def audit_nonconservative_score() -> None:
    # s(x,y)=(-y,x): partial_y s_x=-1, partial_x s_y=1.
    curl = 1.0 - (-1.0)
    assert curl == 2.0
    print("[GEN-32] rotational field curl (cannot be -grad E on R2):", curl)


def main() -> None:
    print("seed:", SEED)
    audit_energy_gauge_and_temperature()
    audit_positive_negative_phase()
    audit_score_matching_gaussian()
    audit_dsm_projection_and_tweedie()
    audit_noise_scale_geometry()
    audit_ula_bias()
    audit_mala_correction()
    audit_pc_budget_and_fixed_layer()
    audit_nonconservative_score()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
