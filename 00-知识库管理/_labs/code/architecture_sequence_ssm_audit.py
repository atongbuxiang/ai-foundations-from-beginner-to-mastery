#!/usr/bin/env python3
"""Deterministic numerical audits for ARCH-09--16.

This is not a benchmark. It checks small, exactly interpretable cases used by
the notes: recurrence unrolling, BPTT, gated updates, ZOH discretization,
recurrence/convolution agreement, affine-scan associativity, a rank-one
inverse, and selective retention.
"""

from __future__ import annotations

import math


TOL = 1e-8


def close(a: float, b: float, tol: float = TOL) -> None:
    if not math.isclose(a, b, rel_tol=tol, abs_tol=tol):
        raise AssertionError(f"{a} != {b}")


def state_recurrence() -> None:
    h = 0.0
    values = []
    for x in (1.0, 2.0, -1.0):
        h = 0.8 * h + x
        values.append(h)
    for got, expected in zip(values, (1.0, 2.8, 1.24)):
        close(got, expected)


def scalar_bptt_finite_difference() -> None:
    # h1 = w h0 + x1, h2 = w h1 + x2, loss = h2^2 / 2.
    h0, x1, x2, w = 0.3, 1.2, -0.4, 0.7

    def loss(weight: float) -> float:
        h1 = weight * h0 + x1
        h2 = weight * h1 + x2
        return 0.5 * h2 * h2

    h1 = w * h0 + x1
    h2 = w * h1 + x2
    analytic = h2 * (h1 + w * h0)
    eps = 1e-6
    numeric = (loss(w + eps) - loss(w - eps)) / (2 * eps)
    close(analytic, numeric, 1e-6)


def gated_updates() -> None:
    c1 = 0.5 * 2.0 + 0.2 * 1.0
    c2 = 0.8 * c1 + 0.5 * (-0.4)
    close(c1, 1.2)
    close(c2, 0.76)

    h_old = (2.0, -1.0)
    h_new = (0.0, 3.0)
    z = (0.25, 0.8)
    result = tuple((1 - gate) * old + gate * new for old, new, gate in zip(h_old, h_new, z))
    close(result[0], 1.5)
    close(result[1], 2.2)


def scalar_zoh_and_stability() -> None:
    # dx/dt = -2 x + 3 u, Delta = 0.5.
    abar = math.exp(-1.0)
    bbar = 1.5 * (1.0 - math.exp(-1.0))
    close(abar, 0.36787944117144233)
    close(bbar, 0.9481808382428365)
    close(bbar / (1.0 - abar), 1.5)

    exact_pole = math.exp(-10.0 * 0.3)
    euler_pole = 1.0 - 10.0 * 0.3
    assert abs(exact_pole) < 1.0
    assert abs(euler_pole) > 1.0


def recurrence_convolution_agreement() -> None:
    a, b, c = 0.5, 2.0, 1.0
    inputs = (1.0, 1.0, 0.0, -1.0)
    state = 0.0
    recurrence = []
    for u in inputs:
        state = a * state + b * u
        recurrence.append(c * state)

    kernel = [c * (a**j) * b for j in range(len(inputs))]
    convolution = []
    for t in range(len(inputs)):
        convolution.append(sum(kernel[t - j] * inputs[j] for j in range(t + 1)))
    for got, expected in zip(recurrence, convolution):
        close(got, expected)


def compose(p2: tuple[float, float], p1: tuple[float, float]) -> tuple[float, float]:
    a2, b2 = p2
    a1, b1 = p1
    return a2 * a1, a2 * b1 + b2


def scan_associativity() -> None:
    p1, p2, p3 = (2.0, 1.0), (3.0, -1.0), (0.5, 4.0)
    left = compose(p3, compose(p2, p1))
    right = compose(compose(p3, p2), p1)
    close(left[0], right[0])
    close(left[1], right[1])
    close(left[0], 3.0)
    close(left[1], 5.0)


def rank_one_inverse() -> None:
    # Inverse of diag(2,3) + [1,1]^T[1,1] is [[4,-1],[-1,3]] / 11.
    inv = ((4 / 11, -1 / 11), (-1 / 11, 3 / 11))
    matrix = ((3.0, 1.0), (1.0, 4.0))
    product = tuple(
        tuple(sum(matrix[i][k] * inv[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )
    for i in range(2):
        for j in range(2):
            close(product[i][j], 1.0 if i == j else 0.0)


def selective_retention() -> None:
    values = [math.exp(-delta) for delta in (0.1, 1.0, 3.0)]
    assert values[0] > values[1] > values[2] > 0.0
    close(values[0], 0.9048374180359595)
    close(values[2], 0.049787068367863944)


def main() -> None:
    checks = (
        state_recurrence,
        scalar_bptt_finite_difference,
        gated_updates,
        scalar_zoh_and_stability,
        recurrence_convolution_agreement,
        scan_associativity,
        rank_one_inverse,
        selective_retention,
    )
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print(f"PASS architecture_sequence_ssm_audit ({len(checks)} checks)")


if __name__ == "__main__":
    main()
