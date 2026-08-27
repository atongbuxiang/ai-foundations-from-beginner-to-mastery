#!/usr/bin/env python3
"""Standard-library numerical audit for GEN-41--48.

The examples are deliberately scalar or two-state.  They test the algebra,
conditioning and indexing contracts behind DDPM/DDIM; they do not train a
denoiser and are not a generative-quality benchmark.
"""

from __future__ import annotations

import math
import random
import statistics


TOL = 1e-10


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def make_schedule(betas: list[float]) -> tuple[list[float], list[float]]:
    """Return alpha and alpha_bar arrays with a dummy index zero."""
    alphas = [1.0] + [1.0 - beta for beta in betas]
    alpha_bar = [1.0]
    for alpha in alphas[1:]:
        alpha_bar.append(alpha_bar[-1] * alpha)
    return alphas, alpha_bar


def audit_forward_marginal() -> None:
    alphas, alpha_bar = make_schedule([0.1, 0.2, 0.3])
    assert close(alpha_bar[3], 0.9 * 0.8 * 0.7)
    assert all(close(alpha_bar[t] / alpha_bar[t - 1], alphas[t]) for t in range(1, 4))

    x0 = 1.7
    target_mean = math.sqrt(alpha_bar[3]) * x0
    target_var = 1.0 - alpha_bar[3]
    rng = random.Random(20260825)
    samples = [target_mean + math.sqrt(target_var) * rng.gauss(0.0, 1.0) for _ in range(100_000)]
    sample_mean = statistics.fmean(samples)
    sample_var = statistics.pvariance(samples)
    assert abs(sample_mean - target_mean) < 0.01
    assert abs(sample_var - target_var) < 0.01
    print(
        f"FORWARD alpha_bar_3={alpha_bar[3]:.12f} "
        f"mean_gap={sample_mean-target_mean:.3e} variance_gap={sample_var-target_var:.3e}"
    )


def audit_posterior_and_elbo_kernel() -> None:
    alphas, alpha_bar = make_schedule([0.1, 0.2])
    t = 2
    beta = 1.0 - alphas[t]
    posterior_var = beta * (1.0 - alpha_bar[t - 1]) / (1.0 - alpha_bar[t])
    c0 = math.sqrt(alpha_bar[t - 1]) * beta / (1.0 - alpha_bar[t])
    ct = math.sqrt(alphas[t]) * (1.0 - alpha_bar[t - 1]) / (1.0 - alpha_bar[t])

    x0, eps = 1.2, -0.7
    xt = math.sqrt(alpha_bar[t]) * x0 + math.sqrt(1.0 - alpha_bar[t]) * eps
    posterior_mean_two_state = c0 * x0 + ct * xt
    posterior_mean_noise = (xt - beta * eps / math.sqrt(1.0 - alpha_bar[t])) / math.sqrt(alphas[t])
    assert close(posterior_var, 1.0 / 14.0)
    assert close(posterior_mean_two_state, posterior_mean_noise)
    print(
        f"POSTERIOR beta_tilde={posterior_var:.12f} "
        f"mean_form_gap={posterior_mean_two_state-posterior_mean_noise:.3e}"
    )


def audit_parameterizations() -> None:
    a, sigma = 0.6, 0.8
    x0, eps = 1.3, -0.4
    xt = a * x0 + sigma * eps
    v = a * eps - sigma * x0
    recovered_x0 = a * xt - sigma * v
    recovered_eps = sigma * xt + a * v
    marginal_score = -eps / sigma
    assert close(a * a + sigma * sigma, 1.0)
    assert close(recovered_x0, x0)
    assert close(recovered_eps, eps)
    print(
        f"PARAMETERIZATION x0_gap={recovered_x0-x0:.3e} eps_gap={recovered_eps-eps:.3e} "
        f"single_pair_score_target={marginal_score:.6f}"
    )


def weighted_scalar_optimum(targets: tuple[float, float], weights: tuple[float, float]) -> float:
    return sum(w * y for w, y in zip(weights, targets)) / sum(weights)


def audit_loss_snr_and_timestep_estimator() -> None:
    unweighted = weighted_scalar_optimum((0.0, 10.0), (1.0, 1.0))
    reweighted = weighted_scalar_optimum((0.0, 10.0), (9.0, 1.0))
    assert close(unweighted, 5.0)
    assert close(reweighted, 1.0)

    objective = (0.8, 0.2)
    proposal = (0.5, 0.5)
    losses = (2.0, 6.0)
    exact = sum(p * loss for p, loss in zip(objective, losses))
    corrected = sum(r * (p / r) * loss for p, r, loss in zip(objective, proposal, losses))
    uncorrected = sum(r * loss for r, loss in zip(proposal, losses))
    assert close(exact, corrected)
    assert not close(exact, uncorrected)
    snr_pair = (0.8 / 0.2, 0.2 / 0.8)
    print(
        f"LOSS shared_optimum={unweighted:.3f}->{reweighted:.3f} "
        f"corrected={corrected:.3f} uncorrected={uncorrected:.3f} snr={snr_pair}"
    )


def gaussian_nll_without_constant(y: float, mean: float, variance: float) -> float:
    return 0.5 * math.log(variance) + 0.5 * (y - mean) ** 2 / variance


def audit_reverse_variance() -> None:
    ys = (1.0, 3.0)
    true_mean = statistics.fmean(ys)
    true_variance = statistics.pvariance(ys)
    model_mean = 1.5
    residual_second_moment = statistics.fmean((y - model_mean) ** 2 for y in ys)
    decomposition = true_variance + (true_mean - model_mean) ** 2
    assert close(residual_second_moment, 1.25)
    assert close(residual_second_moment, decomposition)
    risk_at_optimum = statistics.fmean(
        gaussian_nll_without_constant(y, model_mean, residual_second_moment) for y in ys
    )
    for trial in (0.5, 0.9, 1.8, 3.0):
        trial_risk = statistics.fmean(gaussian_nll_without_constant(y, model_mean, trial) for y in ys)
        assert risk_at_optimum <= trial_risk + 1e-12
    print(
        f"REVERSE_VARIANCE conditional={true_variance:.6f} mean_error={(true_mean-model_mean)**2:.6f} "
        f"optimal={residual_second_moment:.6f}"
    )


def ddim_sigma(alpha_bar_s: float, alpha_bar_t: float, eta: float) -> float:
    return eta * math.sqrt((1.0 - alpha_bar_s) / (1.0 - alpha_bar_t)) * math.sqrt(
        1.0 - alpha_bar_t / alpha_bar_s
    )


def ddim_step(
    xt: float,
    eps_hat: float,
    alpha_bar_s: float,
    alpha_bar_t: float,
    eta: float,
    z: float,
) -> float:
    a_s, a_t = math.sqrt(alpha_bar_s), math.sqrt(alpha_bar_t)
    sigma_t = math.sqrt(1.0 - alpha_bar_t)
    x0_hat = (xt - sigma_t * eps_hat) / a_t
    sigma_skip = ddim_sigma(alpha_bar_s, alpha_bar_t, eta)
    direction_sq = 1.0 - alpha_bar_s - sigma_skip * sigma_skip
    assert direction_sq >= -1e-14
    return a_s * x0_hat + math.sqrt(max(0.0, direction_sq)) * eps_hat + sigma_skip * z


def audit_ddim() -> None:
    alpha_bar_s, alpha_bar_t = 0.8, 0.5
    first = ddim_step(0.4, -0.3, alpha_bar_s, alpha_bar_t, eta=0.0, z=-10.0)
    second = ddim_step(0.4, -0.3, alpha_bar_s, alpha_bar_t, eta=0.0, z=10.0)
    assert close(first, second)

    alphas, alpha_bar = make_schedule([0.1, 0.2])
    posterior_var = (1.0 - alphas[2]) * (1.0 - alpha_bar[1]) / (1.0 - alpha_bar[2])
    adjacent_ddim_var = ddim_sigma(alpha_bar[1], alpha_bar[2], eta=1.0) ** 2
    assert close(adjacent_ddim_var, posterior_var)
    print(
        f"DDIM eta0_z_gap={first-second:.3e} "
        f"adjacent_variance_gap={adjacent_ddim_var-posterior_var:.3e}"
    )


def matvec(matrix: list[list[float]], vector: tuple[float, float]) -> tuple[float, float]:
    return tuple(sum(row[j] * vector[j] for j in range(2)) for row in matrix)  # type: ignore[return-value]


def audit_kernel_consistency() -> None:
    q_t = (0.5, 0.5)
    correlated = [[0.8, 0.7], [0.2, 0.3]]
    independent = [[0.75, 0.75], [0.25, 0.25]]
    target = (0.75, 0.25)
    correlated_out = matvec(correlated, q_t)
    independent_out = matvec(independent, q_t)
    assert all(close(correlated_out[i], target[i]) for i in range(2))
    assert all(close(independent_out[i], target[i]) for i in range(2))
    assert correlated != independent
    print(
        f"KERNEL correlated_out={correlated_out} independent_out={independent_out} "
        f"same_marginal={correlated_out == independent_out}"
    )


def audit_index_and_last_step_mask() -> None:
    _, alpha_bar = make_schedule([0.1, 0.2])
    correct_t2 = alpha_bar[2]
    wrong_off_by_one = alpha_bar[1]
    assert close(correct_t2, 0.72)
    assert not close(correct_t2, wrong_off_by_one)

    means = (2.0, 3.0)
    sigmas = (0.1, 0.2)
    timesteps = (1, 2)
    noises = (5.0, 5.0)
    outputs = tuple(
        mean + (1.0 if t > 1 else 0.0) * sigma * noise
        for mean, sigma, t, noise in zip(means, sigmas, timesteps, noises)
    )
    assert outputs == (2.0, 4.0)
    print(
        f"IMPLEMENTATION alpha_bar_t2={correct_t2:.3f} off_by_one={wrong_off_by_one:.3f} "
        f"last_step_outputs={outputs}"
    )


def main() -> None:
    audit_forward_marginal()
    audit_posterior_and_elbo_kernel()
    audit_parameterizations()
    audit_loss_snr_and_timestep_estimator()
    audit_reverse_variance()
    audit_ddim()
    audit_kernel_consistency()
    audit_index_and_last_step_mask()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
