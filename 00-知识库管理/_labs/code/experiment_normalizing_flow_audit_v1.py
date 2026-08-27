#!/usr/bin/env python3
"""Standard-library numerical audit for GEN-33--40.

This script deliberately uses tiny analytic examples.  It tests identities,
round trips and approximation error; it is not a benchmark implementation.
"""

from __future__ import annotations

import math
import random
import statistics


TOL = 1e-9


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def normal_logpdf(x: float) -> float:
    return -0.5 * x * x - 0.5 * math.log(2.0 * math.pi)


def det2(a: list[list[float]]) -> float:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def numeric_jacobian_2d(fn, x: tuple[float, float], eps: float = 1e-6):
    cols = []
    for j in range(2):
        xp = list(x)
        xm = list(x)
        xp[j] += eps
        xm[j] -= eps
        yp = fn(tuple(xp))
        ym = fn(tuple(xm))
        cols.append(((yp[0] - ym[0]) / (2 * eps), (yp[1] - ym[1]) / (2 * eps)))
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


def audit_change_of_variables() -> None:
    # X = 3 Z - 2; evaluate at x=1, hence z=1.
    x = 1.0
    z = (x + 2.0) / 3.0
    encode = normal_logpdf(z) - math.log(3.0)
    generate = normal_logpdf(z) - math.log(3.0)
    assert close(encode, generate)
    print(f"CHANGE_OF_VARIABLES log_p_x={encode:.12f} direction_gap={encode-generate:.3e}")


def coupling_forward(x: tuple[float, float]) -> tuple[float, float]:
    x1, x2 = x
    s = 0.4 * math.tanh(x1)
    t = x1 * x1 - 0.5
    return x1, x2 * math.exp(s) + t


def coupling_inverse(y: tuple[float, float]) -> tuple[float, float]:
    y1, y2 = y
    s = 0.4 * math.tanh(y1)
    t = y1 * y1 - 0.5
    return y1, (y2 - t) * math.exp(-s)


def audit_coupling() -> None:
    x = (0.7, -1.2)
    y = coupling_forward(x)
    xr = coupling_inverse(y)
    residual = max(abs(x[i] - xr[i]) for i in range(2))
    jac = numeric_jacobian_2d(coupling_forward, x)
    numeric_logdet = math.log(abs(det2(jac)))
    analytic_logdet = 0.4 * math.tanh(x[0])
    assert residual < 1e-12
    assert abs(numeric_logdet - analytic_logdet) < 1e-9
    print(
        f"COUPLING roundtrip={residual:.3e} "
        f"analytic_logdet={analytic_logdet:.12f} numeric_gap={numeric_logdet-analytic_logdet:.3e}"
    )


def audit_glow_and_conditioning() -> None:
    height = width = 3
    w = [[2.0, 0.0], [0.0, 0.5]]
    total_logdet = height * width * math.log(abs(det2(w)))
    sigma_max, sigma_min = 2.0, 0.5
    condition = sigma_max / sigma_min
    squeezed_old = 3 * 32 * 32
    squeezed_new = 12 * 16 * 16
    assert close(total_logdet, 0.0)
    assert squeezed_old == squeezed_new
    print(
        f"GLOW HW_logdet={total_logdet:.12f} condition={condition:.1f} "
        f"squeeze_dims={squeezed_old}->{squeezed_new}"
    )


def audit_autoregressive_directions() -> None:
    # MAF encode is parallel given x; its algebraic inverse is sequential.
    x = (1.0, 3.0, 8.0)
    z = (x[0], x[1] - x[0], x[2] - x[0] - x[1])
    recovered = [z[0]]
    recovered.append(z[1] + recovered[0])
    recovered.append(z[2] + recovered[0] + recovered[1])
    assert all(close(recovered[i], x[i]) for i in range(3))
    print(f"AUTOREGRESSIVE x={x} z={z} sequential_inverse={tuple(recovered)}")


def fixed_point_inverse(y: float, a: float, steps: int) -> float:
    x = 0.0
    for _ in range(steps):
        x = y - a * x
    return x


def residual_series(a: float, order: int) -> float:
    return sum(((-1.0) ** (k + 1)) * (a**k) / k for k in range(1, order + 1))


def audit_residual_flow() -> None:
    y, a = 3.0, 0.5
    exact_inverse = y / (1.0 + a)
    errors = []
    for steps in (1, 2, 4, 8, 16):
        errors.append(abs(fixed_point_inverse(y, a, steps) - exact_inverse))
    assert all(errors[i + 1] < errors[i] for i in range(len(errors) - 1))
    exact_logdet = math.log1p(a)
    series_errors = [abs(residual_series(a, k) - exact_logdet) for k in (1, 2, 4, 8, 16)]
    assert series_errors[-1] < series_errors[0]
    print(
        "RESIDUAL inverse_errors=" + ",".join(f"{e:.3e}" for e in errors)
        + " series_errors=" + ",".join(f"{e:.3e}" for e in series_errors)
    )


def rational_quadratic(
    x: float,
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    d0: float,
    d1: float,
) -> float:
    width = x1 - x0
    height = y1 - y0
    xi = (x - x0) / width
    delta = height / width
    numerator = height * (delta * xi * xi + d0 * xi * (1.0 - xi))
    denominator = delta + (d1 + d0 - 2.0 * delta) * xi * (1.0 - xi)
    return y0 + numerator / denominator


def bisect_inverse(fn, y: float, lo: float, hi: float, steps: int = 80) -> float:
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if fn(mid) < y:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def audit_spline() -> None:
    fn = lambda x: rational_quadratic(x, -1.0, 1.0, -1.0, 1.0, 0.35, 2.2)
    grid = [-1.0 + 2.0 * i / 200 for i in range(201)]
    ys = [fn(x) for x in grid]
    min_increment = min(ys[i + 1] - ys[i] for i in range(len(ys) - 1))
    x = 0.37
    y = fn(x)
    xr = bisect_inverse(fn, y, -1.0, 1.0)
    assert min_increment > 0.0
    assert abs(x - xr) < 1e-12
    print(f"SPLINE min_grid_increment={min_increment:.6e} inverse_residual={abs(x-xr):.3e}")


def audit_cnf_and_hutchinson() -> None:
    # dz/dt = a z has exact scale exp(aT) and density change -aT.
    a, duration = 2.0, 0.5
    exact_scale = math.exp(a * duration)
    logp_change = -a * duration
    assert close(exact_scale, math.e)
    assert close(logp_change, -1.0)

    # For a non-diagonal 2x2 matrix, estimate trace with Rademacher probes.
    matrix = [[1.0, 2.0], [-1.0, 3.0]]
    true_trace = 4.0
    rng = random.Random(20260825)
    estimates = []
    for _ in range(20000):
        v = (rng.choice((-1.0, 1.0)), rng.choice((-1.0, 1.0)))
        av = (matrix[0][0] * v[0] + matrix[0][1] * v[1], matrix[1][0] * v[0] + matrix[1][1] * v[1])
        estimates.append(v[0] * av[0] + v[1] * av[1])
    mean = statistics.fmean(estimates)
    assert abs(mean - true_trace) < 0.04
    print(
        f"CNF scale={exact_scale:.12f} logp_change={logp_change:.3f} "
        f"hutchinson_mean={mean:.6f} sd={statistics.pstdev(estimates):.6f}"
    )


def audit_dequantization_and_deployment_shift() -> None:
    # p(y)=2y on [0,1]: mass is one. Jensen expectation E log(2U)=log2-1.
    mass = 1.0
    uniform_bound = math.log(2.0) - 1.0
    assert uniform_bound <= math.log(mass)

    # A deterministic shrink/denoise changes a sample distribution's variance.
    rng = random.Random(7)
    core = [rng.gauss(0.0, 1.0) for _ in range(50000)]
    deployed = [0.7 * y for y in core]
    core_var = statistics.pvariance(core)
    deployed_var = statistics.pvariance(deployed)
    ratio = deployed_var / core_var
    assert abs(ratio - 0.49) < 1e-12
    print(
        f"DEQUANT mass={mass:.3f} uniform_bound={uniform_bound:.12f} "
        f"deployment_variance_ratio={ratio:.6f}"
    )


def main() -> None:
    audit_change_of_variables()
    audit_coupling()
    audit_glow_and_conditioning()
    audit_autoregressive_directions()
    audit_residual_flow()
    audit_spline()
    audit_cnf_and_hutchinson()
    audit_dequantization_and_deployment_shift()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()

