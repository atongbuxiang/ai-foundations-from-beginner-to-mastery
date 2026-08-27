#!/usr/bin/env python3
"""Pure-stdlib numerical audits for ARCH-57--64 MoE notes."""

from __future__ import annotations

import itertools
import math
import sys


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def softmax(xs):
    m = max(xs)
    es = [math.exp(x - m) for x in xs]
    z = sum(es)
    return [x / z for x in es]


def topk(xs, k):
    return sorted(range(len(xs)), key=lambda i: (-xs[i], i))[:k]


def check_capacity_compute_ledger():
    d, m, experts, active, me = 1024, 4096, 8, 2, 2048
    dense = 2 * d * m
    total = experts * 2 * d * me
    active_macs = active * 2 * d * me
    assert total == 4 * dense
    assert active_macs == dense
    assert experts * me / m == 4


def check_router_gate_contract():
    z = [2.0, 1.0, -1.0]
    p = softmax(z)
    idx = topk(p, 2)
    renorm = [p[i] / sum(p[j] for j in idx) for i in idx]
    selected_softmax = softmax([z[i] for i in idx])
    assert idx == [0, 1]
    assert all(close(a, b) for a, b in zip(renorm, selected_softmax))
    sig = [1 / (1 + math.exp(-x)) for x in z]
    assert topk(sig, 2) == idx
    eps = 1e-6
    gate_plus = (p[0] + eps) / (p[0] + eps)
    gate_minus = (p[0] - eps) / (p[0] - eps)
    assert close((gate_plus - gate_minus) / (2 * eps), 0.0)


def check_dispatch_capacity():
    loads, cap = [4, 2, 2], 3
    processed = sum(min(x, cap) for x in loads)
    dropped = sum(max(0, x - cap) for x in loads)
    empty = sum(max(0, cap - x) for x in loads)
    assert (processed, dropped, empty) == (7, 1, 2)
    assert close(processed / (len(loads) * cap), 7 / 9)
    matrix = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    assert [sum(r) for r in matrix] == [2, 2, 2]
    assert [sum(matrix[t][j] for t in range(3)) for j in range(3)] == [2, 2, 2]


def check_aux_loss_and_gradient():
    f = [0.75, 0.25]
    logits = [math.log(0.7), math.log(0.3)]
    lam, experts, tokens = 0.01, 2, 4

    def loss(z):
        p = softmax(z)
        return lam * experts * sum(fi * pi for fi, pi in zip(f, p))

    p = softmax(logits)
    assert close(experts * sum(fi * pi for fi, pi in zip(f, p)), 1.2)
    analytic = [
        lam * experts * p[j] * (f[j] - sum(fi * pi for fi, pi in zip(f, p)))
        for j in range(2)
    ]
    eps = 1e-6
    numerical = []
    for j in range(2):
        zp, zm = logits[:], logits[:]
        zp[j] += eps
        zm[j] -= eps
        numerical.append((loss(zp) - loss(zm)) / (2 * eps))
    assert all(close(a, n, 1e-6) for a, n in zip(analytic, numerical))
    direct = [lam * experts * fi / tokens for fi in f]
    assert all(close(x, y) for x, y in zip(direct, [0.00375, 0.00125]))


def check_feedback_assignment_quantile():
    target, load, bias, eta = [4, 4], [6, 2], [0.0, 0.0], 0.1
    updated = [b - eta * (1 if n > q else -1 if n < q else 0)
               for b, n, q in zip(bias, load, target)]
    assert updated == [-0.1, 0.1]
    assert topk([0.55 + updated[0], 0.50 + updated[1]], 1) == [1]

    score = [[9, 7, 2], [8, 6, 5], [4, 9, 7], [3, 8, 9]]
    best = (-math.inf, None)
    for assignment in itertools.product(range(3), repeat=4):
        loads = [assignment.count(j) for j in range(3)]
        if max(loads) <= 2:
            value = sum(score[t][assignment[t]] for t in range(4))
            best = max(best, (value, assignment))
    assert best[0] == 35

    scores = [0.91, 0.72, 0.48, 0.31, 0.12]
    assert sum(s > 0.4 for s in scores) == 3


def check_expert_design_axes():
    e, m, k, r = 8, 4096, 2, 4
    ep, mp, kp = r * e, m // r, r * k
    assert ep * mp == e * m
    assert kp * mp == k * m
    d, ms, routed_e, me, kt = 1024, 1024, 16, 512, 3
    params = 2 * d * ms + routed_e * 2 * d * me
    macs = 2 * d * ms + kt * 2 * d * me
    assert params == 18_874_368
    assert macs == 5_242_880


def check_expert_parallel_payload():
    t, k, d, bytes_per, remote = 8192, 2, 4096, 2, 0.75
    payload = 2 * remote * t * k * d * bytes_per
    assert payload == 201_326_592
    assert payload / 2**20 == 192
    balanced = [4, 4, 4, 4]
    skewed = [10, 2, 2, 2]
    assert sum(balanced) == sum(skewed) == 16
    assert max(skewed) / max(balanced) == 2.5


def check_normalization_and_evidence_boundaries():
    z = [1.0, 0.0]
    sm = softmax(z)
    sg = [1 / (1 + math.exp(-x)) for x in z]
    assert close(sum(sm), 1.0)
    assert close(sum(sg), 1.2310585786300048)
    assert topk(sm, 1) == topk(sg, 1) == [0]
    n, experts, frequent = 1000, 10, 180
    target = n / experts
    assert frequent > target
    assert max(frequent, target) == 180
    evidence = ["I", "T", "E", "H", "O"]
    assert len(evidence) == len(set(evidence)) == 5


CHECKS = [
    ("capacity/active-parameter/MAC ledger", check_capacity_compute_ledger),
    ("score activation/Top-k/Re-Norm contract", check_router_gate_contract),
    ("capacity/drop/pad/dropless accounting", check_dispatch_capacity),
    ("auxiliary loss and proxy gradient", check_aux_loss_and_gradient),
    ("loss-free feedback/assignment/quantile", check_feedback_assignment_quantile),
    ("shared/fine-grained/dynamic axes", check_expert_design_axes),
    ("expert-parallel payload and tail load", check_expert_parallel_payload),
    ("normalization/hash/evidence boundaries", check_normalization_and_evidence_boundaries),
]


def main():
    failures = 0
    for label, fn in CHECKS:
        try:
            fn()
        except Exception as exc:  # audit should print every failed ledger
            failures += 1
            print(f"FAIL {label}: {exc}")
        else:
            print(f"PASS {label}")
    print(f"{len(CHECKS)-failures}/{len(CHECKS)} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
