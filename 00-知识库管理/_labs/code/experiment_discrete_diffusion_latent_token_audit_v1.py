#!/usr/bin/env python3
"""Minimal standard-library audit for GEN-57--64.

Checks categorical matrix marginals/posteriors, absorbing-mask Bayes,
two-state CTMC reversal, VQ/FSQ bookkeeping, and DDCM finite-code weights.
No training framework is required.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from typing import Iterable, Sequence


Vector = list[float]
Matrix = list[list[float]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    assert len(a[0]) == len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def row_times(v: Vector, q: Matrix) -> Vector:
    return [sum(v[i] * q[i][j] for i in range(len(v))) for j in range(len(q[0]))]


def assert_stochastic(q: Matrix, tol: float = 1e-12) -> None:
    assert q and all(len(row) == len(q[0]) for row in q)
    for row in q:
        assert all(math.isfinite(x) and x >= -tol for x in row)
        assert abs(sum(row) - 1.0) <= tol


def categorical(rng: random.Random, probs: Sequence[float]) -> int:
    u = rng.random()
    total = 0.0
    for i, p in enumerate(probs):
        total += p
        if u <= total:
            return i
    return len(probs) - 1


def categorical_posterior(
    x0: int, xt: int, q_bar_prev: Matrix, q_step: Matrix
) -> Vector:
    arrival = q_bar_prev[x0]
    weights = [arrival[i] * q_step[i][xt] for i in range(len(arrival))]
    denom = sum(weights)
    assert denom > 0.0
    return [w / denom for w in weights]


def monte_carlo_chain(
    rng: random.Random, x0: int, kernels: Sequence[Matrix], samples: int
) -> Vector:
    counts = [0] * len(kernels[0])
    for _ in range(samples):
        x = x0
        for q in kernels:
            x = categorical(rng, q[x])
        counts[x] += 1
    return [c / samples for c in counts]


def entropy(probs: Iterable[float]) -> float:
    return -sum(p * math.log(p) for p in probs if p > 0.0)


def squared_distance(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def softmax(logits: Sequence[float]) -> Vector:
    m = max(logits)
    weights = [math.exp(x - m) for x in logits]
    z = sum(weights)
    return [w / z for w in weights]


def run(seed: int, samples: int) -> dict[str, object]:
    rng = random.Random(seed)

    # GEN-57: closed marginal and posterior.
    q = [[0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8]]
    assert_stochastic(q)
    q2 = matmul(q, q)
    assert_stochastic(q2)
    closed = q2[0]
    empirical = monte_carlo_chain(rng, 0, [q, q], samples)
    posterior = categorical_posterior(0, 1, q, q)
    assert max(abs(a - b) for a, b in zip(closed, [0.66, 0.17, 0.17])) < 1e-12
    assert max(abs(a - b) for a, b in zip(posterior, [8 / 17, 8 / 17, 1 / 17])) < 1e-12
    assert max(abs(a - b) for a, b in zip(closed, empirical)) < 0.02

    # GEN-58: absorbing mask posterior.
    alphas = [0.9, 0.8, 0.5]
    bar2 = alphas[0] * alphas[1]
    bar3 = bar2 * alphas[2]
    clean_prev = bar2 * (1.0 - alphas[2]) / (1.0 - bar3)
    mask_prev = (1.0 - bar2) / (1.0 - bar3)
    assert abs(clean_prev - 0.5625) < 1e-12
    assert abs(clean_prev + mask_prev - 1.0) < 1e-12

    # GEN-59: two-state reverse rates and one Euler probability step.
    rate = [[-2.0, 2.0], [1.0, -1.0]]
    p = [0.75, 0.25]
    reverse_2_to_1 = rate[0][1] * p[0] / p[1]
    reverse_1_to_2 = rate[1][0] * p[1] / p[0]
    assert abs(reverse_2_to_1 - 6.0) < 1e-12
    assert abs(reverse_1_to_2 - 1.0 / 3.0) < 1e-12
    h = 0.05
    q_h = [
        [(1.0 if i == j else 0.0) + h * rate[i][j] for j in range(2)]
        for i in range(2)
    ]
    assert_stochastic(q_h)

    # GEN-60/61: nearest VQ, assignment entropy, and FSQ cardinality.
    codes = [(0.0, 0.0), (2.0, 0.0), (0.0, 2.0)]
    z = (1.4, 0.3)
    distances = [squared_distance(z, code) for code in codes]
    nearest = min(range(len(codes)), key=distances.__getitem__)
    assert nearest == 1 and abs(distances[1] - 0.45) < 1e-12
    assignments = [0, 0, 0, 0, 1, 1, 2, 3]
    count = Counter(assignments)
    assignment_probs = [count[i] / len(assignments) for i in range(4)]
    ppl = math.exp(entropy(assignment_probs))
    assert abs(ppl - math.exp(1.2130075659799042)) < 1e-12
    fsq_levels = [8, 8, 8, 5, 5]
    fsq_cardinality = math.prod(fsq_levels)
    assert fsq_cardinality == 12800

    # GEN-64: DDCM max-inner-product vs density-weighted sampling.
    noise_codes = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]
    residual = (2.0, -1.0)
    dot_logits = [sum(x * y for x, y in zip(code, residual)) for code in noise_codes]
    greedy_code = max(range(len(noise_codes)), key=dot_logits.__getitem__)
    assert greedy_code == 0
    target_mean = (1.0, 0.5)
    density_logits = [-0.5 * squared_distance(code, target_mean) for code in noise_codes]
    density_probs = softmax(density_logits)
    assert abs(sum(density_probs) - 1.0) < 1e-12
    assert max(range(len(density_probs)), key=density_probs.__getitem__) == 0

    return {
        "seed": seed,
        "samples": samples,
        "categorical": {
            "closed_x2_given_x0_1": closed,
            "monte_carlo": empirical,
            "max_abs_error": max(abs(a - b) for a, b in zip(closed, empirical)),
            "posterior_x1_given_x2_2_x0_1": posterior,
        },
        "absorbing": {
            "bar_alpha_3": bar3,
            "p_x2_clean_given_x3_mask": clean_prev,
            "p_x2_mask_given_x3_mask": mask_prev,
        },
        "ctmc": {
            "reverse_2_to_1": reverse_2_to_1,
            "reverse_1_to_2": reverse_1_to_2,
            "valid_small_step_kernel": q_h,
        },
        "quantization": {
            "vq_squared_distances": distances,
            "vq_nearest_index_zero_based": nearest,
            "assignment_perplexity": ppl,
            "fsq_cardinality": fsq_cardinality,
        },
        "ddcm": {
            "greedy_dot_logits": dot_logits,
            "greedy_code_zero_based": greedy_code,
            "density_probs": density_probs,
        },
        "all_assertions_passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260825)
    parser.add_argument("--samples", type=int, default=100_000)
    args = parser.parse_args()
    print(json.dumps(run(args.seed, args.samples), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
