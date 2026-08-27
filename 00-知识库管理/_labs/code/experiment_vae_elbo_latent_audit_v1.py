#!/usr/bin/env python3
"""Deterministic numerical audit for GEN-09--16.

Uses only the Python standard library. Every Monte Carlo statement is compared
with an exact finite-model value or analytic Gaussian moment and guarded by an
assertion.
"""

from __future__ import annotations

import json
import math
import random
from typing import Iterable


SEED = 20260825


def kl_discrete(q: Iterable[float], p: Iterable[float]) -> float:
    total = 0.0
    for qi, pi in zip(q, p):
        if qi > 0.0:
            if pi <= 0.0:
                return math.inf
            total += qi * math.log(qi / pi)
    return total


def logsumexp(values: list[float]) -> float:
    m = max(values)
    return m + math.log(sum(math.exp(v - m) for v in values))


def draw_categorical(rng: random.Random, probs: list[float]) -> int:
    u = rng.random()
    cumulative = 0.0
    for i, prob in enumerate(probs):
        cumulative += prob
        if u <= cumulative:
            return i
    return len(probs) - 1


def exact_elbo_audit() -> dict[str, float]:
    prior = [0.6, 0.4]
    likelihood = [0.2, 0.8]
    q = [0.5, 0.5]
    joint = [prior[z] * likelihood[z] for z in range(2)]
    evidence = sum(joint)
    posterior = [v / evidence for v in joint]
    elbo = sum(q[z] * math.log(joint[z] / q[z]) for z in range(2))
    posterior_gap = kl_discrete(q, posterior)
    residual = math.log(evidence) - elbo - posterior_gap
    assert abs(residual) < 1e-14
    return {
        "evidence": evidence,
        "log_evidence": math.log(evidence),
        "elbo": elbo,
        "posterior_gap": posterior_gap,
        "identity_residual": residual,
    }


def gaussian_kl_audit() -> dict[str, float]:
    mu = [1.0, -1.0, 0.25]
    var = [1.0, 4.0, 0.5]
    closed = 0.5 * sum(m * m + v - math.log(v) - 1.0 for m, v in zip(mu, var))
    expected_ratio = 0.0
    for m, v in zip(mu, var):
        expected_log_q = -0.5 * math.log(2.0 * math.pi * v) - 0.5
        expected_log_p = -0.5 * math.log(2.0 * math.pi) - 0.5 * (m * m + v)
        expected_ratio += expected_log_q - expected_log_p
    residual = closed - expected_ratio
    assert closed >= 0.0 and abs(residual) < 1e-14
    return {
        "closed_form": closed,
        "expected_log_density_ratio": expected_ratio,
        "residual": residual,
    }


def reparameterization_audit() -> dict[str, float]:
    rng = random.Random(SEED)
    n = 200_000
    mu, sigma = 1.25, 1.7
    samples = [mu + sigma * rng.gauss(0.0, 1.0) for _ in range(n)]
    mean = sum(samples) / n
    variance = sum((z - mean) ** 2 for z in samples) / n
    grad_mu = sum(2.0 * z for z in samples) / n

    rng = random.Random(SEED)
    grad_sigma = 0.0
    for _ in range(n):
        epsilon = rng.gauss(0.0, 1.0)
        z = mu + sigma * epsilon
        grad_sigma += 2.0 * z * epsilon
    grad_sigma /= n

    assert abs(mean - mu) < 0.015
    assert abs(variance - sigma * sigma) < 0.025
    assert abs(grad_mu - 2.0 * mu) < 0.03
    assert abs(grad_sigma - 2.0 * sigma) < 0.04
    return {
        "sample_mean": mean,
        "target_mean": mu,
        "sample_variance": variance,
        "target_variance": sigma * sigma,
        "pathwise_grad_mu": grad_mu,
        "analytic_grad_mu": 2.0 * mu,
        "pathwise_grad_sigma": grad_sigma,
        "analytic_grad_sigma": 2.0 * sigma,
    }


def iwae_audit() -> dict[str, object]:
    q = [0.5, 0.5]
    joint = [0.12, 0.32]
    evidence = sum(joint)
    weights = [joint[z] / q[z] for z in range(2)]
    repetitions = 80_000
    estimates: dict[int, dict[str, float]] = {}

    for k in (1, 5, 50):
        rng = random.Random(SEED + k)
        logs = []
        densities = []
        for _ in range(repetitions):
            sampled = [weights[draw_categorical(rng, q)] for _ in range(k)]
            log_estimate = logsumexp([math.log(w) for w in sampled]) - math.log(k)
            logs.append(log_estimate)
            densities.append(sum(sampled) / k)
        estimates[k] = {
            "mean_density_estimate": sum(densities) / repetitions,
            "mean_log_estimate_LK": sum(logs) / repetitions,
        }

    l1 = estimates[1]["mean_log_estimate_LK"]
    l5 = estimates[5]["mean_log_estimate_LK"]
    l50 = estimates[50]["mean_log_estimate_LK"]
    assert l1 < l5 < l50 < math.log(evidence)
    for values in estimates.values():
        assert abs(values["mean_density_estimate"] - evidence) < 0.0015
    return {
        "exact_evidence": evidence,
        "exact_log_evidence": math.log(evidence),
        "weights": weights,
        "repetitions": repetitions,
        "estimates": estimates,
    }


def rate_decomposition_audit() -> dict[str, object]:
    p_x = [0.55, 0.45]
    q_z_given_x = [[0.9, 0.1], [0.2, 0.8]]
    prior = [0.5, 0.5]
    aggregate = [
        sum(p_x[x] * q_z_given_x[x][z] for x in range(2))
        for z in range(2)
    ]
    rate = sum(p_x[x] * kl_discrete(q_z_given_x[x], prior) for x in range(2))
    mutual_information = sum(
        p_x[x] * kl_discrete(q_z_given_x[x], aggregate) for x in range(2)
    )
    aggregate_kl = kl_discrete(aggregate, prior)
    residual = rate - mutual_information - aggregate_kl
    assert abs(residual) < 1e-14
    assert 0.0 <= mutual_information <= rate

    q_same = [0.8, 0.2]
    zero_mi_rate = kl_discrete(q_same, prior)
    assert zero_mi_rate > 0.0
    return {
        "aggregate_posterior": aggregate,
        "rate": rate,
        "mutual_information": mutual_information,
        "aggregate_prior_kl": aggregate_kl,
        "identity_residual": residual,
        "positive_rate_zero_information_counterexample": {
            "q_z_given_every_x": q_same,
            "mutual_information": 0.0,
            "rate": zero_mi_rate,
        },
    }


def posterior_collapse_audit() -> dict[str, float]:
    prior = [0.5, 0.5]
    likelihood = [0.7, 0.7]
    q = prior[:]
    reconstruction = sum(q[z] * math.log(likelihood[z]) for z in range(2))
    rate = kl_discrete(q, prior)
    elbo = reconstruction - rate
    log_evidence = math.log(sum(prior[z] * likelihood[z] for z in range(2)))
    assert rate == 0.0
    assert abs(elbo - log_evidence) < 1e-14
    return {
        "rate": rate,
        "elbo": elbo,
        "log_evidence": log_evidence,
        "residual": elbo - log_evidence,
    }


def main() -> None:
    report = {
        "experiment": "experiment_vae_elbo_latent_audit_v1",
        "seed": SEED,
        "exact_elbo": exact_elbo_audit(),
        "gaussian_kl": gaussian_kl_audit(),
        "reparameterization": reparameterization_audit(),
        "iwae": iwae_audit(),
        "rate_decomposition": rate_decomposition_audit(),
        "posterior_collapse": posterior_collapse_audit(),
        "all_assertions_passed": True,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

