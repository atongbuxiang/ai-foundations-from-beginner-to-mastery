#!/usr/bin/env python3
"""Deterministic numerical checks for GEN-01--08.

Standard-library only.  The script checks identities and counterexamples; it is
not a benchmark and does not claim to reproduce a neural generative model.
"""

from __future__ import annotations

import json
import math


def kl(p: list[float], q: list[float]) -> float:
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q) if pi > 0.0)


def entropy(p: list[float]) -> float:
    return -sum(pi * math.log(pi) for pi in p if pi > 0.0)


def cross_entropy(p: list[float], q: list[float]) -> float:
    return -sum(pi * math.log(qi) for pi, qi in zip(p, q) if pi > 0.0)


def normalize(values: list[float]) -> list[float]:
    total = sum(values)
    if total <= 0.0:
        raise ValueError("normalization mass must be positive")
    return [value / total for value in values]


def temperature(p: list[float], tau: float) -> list[float]:
    if tau <= 0.0:
        raise ValueError("temperature must be positive")
    return normalize([value ** (1.0 / tau) for value in p])


def top_k(p: list[float], k: int) -> list[float]:
    keep = set(sorted(range(len(p)), key=lambda i: (-p[i], i))[:k])
    return normalize([value if i in keep else 0.0 for i, value in enumerate(p)])


def top_p(p: list[float], threshold: float) -> list[float]:
    order = sorted(range(len(p)), key=lambda i: (-p[i], i))
    keep: set[int] = set()
    cumulative = 0.0
    for i in order:
        keep.add(i)
        cumulative += p[i]
        if cumulative >= threshold:
            break
    return normalize([value if i in keep else 0.0 for i, value in enumerate(p)])


def dequantization_check(bin_index: int, grid_size: int = 200_000) -> dict[str, float]:
    # A normalized density on [0, 2): integral 0.3 in bin 0 and 0.7 in bin 1.
    def density(y: float) -> float:
        if 0.0 <= y < 1.0:
            return 0.2 + 0.2 * y
        if 1.0 <= y < 2.0:
            return 0.6 + 0.2 * (y - 1.0)
        return 0.0

    exact_mass = 0.3 if bin_index == 0 else 0.7
    log_values = []
    for j in range(grid_size):
        u = (j + 0.5) / grid_size
        log_values.append(math.log(density(bin_index + u)))
    uniform_bound = sum(log_values) / grid_size
    return {
        "exact_log_mass": math.log(exact_mass),
        "uniform_dequant_bound": uniform_bound,
        "jensen_gap": math.log(exact_mass) - uniform_bound,
    }


def main() -> None:
    p_star = [0.5, 0.3, 0.2]
    p_model = [0.45, 0.4, 0.15]
    h = entropy(p_star)
    ce = cross_entropy(p_star, p_model)
    divergence = kl(p_star, p_model)

    # AR example from GEN-04.
    ar_joint = {
        "00": 0.4 * 0.8,
        "01": 0.4 * 0.2,
        "10": 0.6 * 0.1,
        "11": 0.6 * 0.9,
    }
    p_x2_1 = ar_joint["01"] + ar_joint["11"]
    reverse_x1_1_given_x2_1 = ar_joint["11"] / p_x2_1

    # The true two-step process has X2=X1 with uniform marginals.  Under full
    # independent-prefix replacement, the training pair is the product law.
    true_pair = [0.5, 0.0, 0.0, 0.5]  # 00, 01, 10, 11
    replaced_pair = [0.25, 0.25, 0.25, 0.25]

    base = [0.5, 0.3, 0.15, 0.05]
    result = {
        "mle_kl_identity": {
            "entropy": h,
            "cross_entropy": ce,
            "forward_kl": divergence,
            "identity_residual": ce - h - divergence,
        },
        "autoregressive_joint": {
            "table": ar_joint,
            "normalization_residual": sum(ar_joint.values()) - 1.0,
            "p_x2_equals_1": p_x2_1,
            "p_x1_equals_1_given_x2_equals_1": reverse_x1_1_given_x2_1,
        },
        "scheduled_sampling_counterexample": {
            "true_pair": true_pair,
            "independent_replacement_pair": replaced_pair,
            "true_mutual_information_nats": math.log(2.0),
            "replacement_mutual_information_nats": 0.0,
            "optimal_second_step_probability_given_either_prefix": 0.5,
        },
        "dequantization": {
            "bin_0": dequantization_check(0),
            "bin_1": dequantization_check(1),
        },
        "decoding_kernels": {
            "base": base,
            "temperature_0.5": temperature(base, 0.5),
            "top_2": top_k(base, 2),
            "top_p_0.8": top_p(base, 0.8),
            "removed_mass_top_2": sum(base[2:]),
        },
    }

    # Deterministic gates: fail loudly if the teaching identities drift.
    assert abs(result["mle_kl_identity"]["identity_residual"]) < 1e-12
    assert abs(result["autoregressive_joint"]["normalization_residual"]) < 1e-12
    assert result["dequantization"]["bin_0"]["jensen_gap"] > 0.0
    assert result["dequantization"]["bin_1"]["jensen_gap"] > 0.0
    assert abs(sum(result["decoding_kernels"]["temperature_0.5"]) - 1.0) < 1e-12
    assert abs(sum(result["decoding_kernels"]["top_2"]) - 1.0) < 1e-12
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

