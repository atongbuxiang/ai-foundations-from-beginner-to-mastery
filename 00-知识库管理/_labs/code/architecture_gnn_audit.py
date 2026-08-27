#!/usr/bin/env python3
"""Deterministic numerical/combinatorial checks for ARCH-17--24."""

from __future__ import annotations

import math


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(x) for x in zip(*a)]


def close(a, b, tol=1e-10):
    if isinstance(a, list):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    return abs(a - b) <= tol


def relabeling():
    a = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    p = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    x = [[1], [2], [4]]
    lhs = matmul(matmul(matmul(p, a), transpose(p)), matmul(p, x))
    rhs = matmul(p, matmul(a, x))
    assert close(lhs, rhs)


def mpnn_handcheck():
    h = [1, 2, 4]
    n = [[1], [0, 2], [1]]
    h1 = [h[i] + sum(h[j] for j in n[i]) for i in range(3)]
    h2 = [h1[i] + sum(h1[j] for j in n[i]) for i in range(3)]
    assert h1 == [3, 7, 6] and h2 == [10, 16, 13]


def gcn_normalization():
    root6 = math.sqrt(6)
    s = [[0.5, 1 / root6, 0], [1 / root6, 1 / 3, 1 / root6], [0, 1 / root6, 0.5]]
    out = matmul(s, [[1], [2], [4]])
    expected = [[0.5 + 2 / root6], [1 / root6 + 2 / 3 + 4 / root6], [2 / root6 + 2]]
    assert close(out, expected)


def aggregator_collisions():
    mean = lambda xs: sum(xs) / len(xs)
    assert mean([1, 3]) == mean([1, 1, 3, 3])
    assert max([1, 3]) == max([2, 3, 3])
    assert sum([1, 3]) == sum([2, 2])
    # Base-(M+1) count encoding for labels 0,1,2 and M=3.
    enc = lambda xs: sum(4 ** x for x in xs)
    assert enc([0, 0, 2]) != enc([0, 1, 1])


def spectral_smoothing():
    coeff = [1.0, 2.0, 3.0]
    eig = [1.0, 0.6, 0.2]
    k3 = [c * lam ** 3 for c, lam in zip(coeff, eig)]
    assert close(k3, [1.0, 0.432, 0.024])
    assert abs(k3[2]) < abs(k3[1]) < abs(k3[0])


def gat_softmax():
    logits = [0.0, math.log(2), math.log(3)]
    weights = [math.exp(x) / sum(math.exp(y) for y in logits) for x in logits]
    assert close(weights, [1 / 6, 1 / 3, 1 / 2])
    value = sum(w * v for w, v in zip(weights, [1, 4, -2]))
    assert close(value, 0.5)
    shifted = [math.exp(x + 7) / sum(math.exp(y + 7) for y in logits) for x in logits]
    assert close(weights, shifted)


def invariant_readout():
    h = [[1, 0], [2, 1], [3, -1]]
    p = [h[2], h[0], h[1]]
    reduce_sum = lambda rows: [sum(r[j] for r in rows) for j in range(2)]
    reduce_max = lambda rows: [max(r[j] for r in rows) for j in range(2)]
    assert reduce_sum(h) == reduce_sum(p) == [6, 0]
    assert reduce_max(h) == reduce_max(p) == [3, 1]


def wl_signature(adj, rounds=3):
    colors = [0] * len(adj)
    for _ in range(rounds):
        signatures = [(colors[i], tuple(sorted(colors[j] for j in adj[i]))) for i in range(len(adj))]
        dictionary = {sig: k for k, sig in enumerate(sorted(set(signatures)))}
        colors = [dictionary[sig] for sig in signatures]
    return sorted(colors)


def component_count(adj):
    seen = set()
    count = 0
    for start in range(len(adj)):
        if start in seen:
            continue
        count += 1
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for neighbor in adj[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return count


def wl_counterexample():
    cycle = [[1, 5], [0, 2], [1, 3], [2, 4], [3, 5], [4, 0]]
    triangles = [[1, 2], [0, 2], [0, 1], [4, 5], [3, 5], [3, 4]]
    assert wl_signature(cycle) == wl_signature(triangles)
    # But connected-component counts differ.
    assert component_count(cycle) == 1
    assert component_count(triangles) == 2


CHECKS = [
    relabeling,
    mpnn_handcheck,
    gcn_normalization,
    aggregator_collisions,
    spectral_smoothing,
    gat_softmax,
    invariant_readout,
    wl_counterexample,
]


if __name__ == "__main__":
    for check in CHECKS:
        check()
        print(f"PASS  {check.__name__}")
    print(f"PASS  total={len(CHECKS)}")
