#!/usr/bin/env python3
"""Standard-library audit for GEN-65--72.

Checks conditional Gaussian guidance, CFG scale convention, the exact versus
plug-in likelihood score in a linear Gaussian inverse problem, Euler/Heun
errors, finite-map composition, the MeanFlow identity, FID/KID arithmetic,
and a finite-difference check of the one-dimensional FD covariance gradient.
No machine-learning framework is required.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Callable, Sequence


Vector = list[float]


def add(a: Sequence[float], b: Sequence[float]) -> Vector:
    return [x + y for x, y in zip(a, b)]


def scale(c: float, a: Sequence[float]) -> Vector:
    return [c * x for x in a]


def sub(a: Sequence[float], b: Sequence[float]) -> Vector:
    return [x - y for x, y in zip(a, b)]


def l2(a: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def central_difference(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x - h)) / (2.0 * h)


def tilted_gaussian(a: float, tau2: float, w: float) -> dict[str, float]:
    return {
        "mean": w * a / (tau2 + w),
        "variance": tau2 / (tau2 + w),
    }


def cfg(r_u: Sequence[float], r_c: Sequence[float], w: float) -> Vector:
    return add(r_u, scale(w, sub(r_c, r_u)))


def linear_gaussian_inverse(
    tau0: float,
    alpha: float,
    sigma: float,
    a: float,
    sigma_y: float,
    x_t: float,
    y: float,
) -> dict[str, float]:
    tau02 = tau0 * tau0
    denom = alpha * alpha * tau02 + sigma * sigma
    k = alpha * tau02 / denom
    c = tau02 * sigma * sigma / denom
    exact_variance = sigma_y * sigma_y + a * a * c
    residual = y - a * k * x_t
    exact_score = a * k * residual / exact_variance
    plugin_score = a * k * residual / (sigma_y * sigma_y)
    return {
        "k": k,
        "conditional_variance_x0_given_xt": c,
        "variance_y_given_xt": exact_variance,
        "exact_likelihood_score": exact_score,
        "plugin_likelihood_score": plugin_score,
        "plugin_to_exact_ratio": plugin_score / exact_score,
    }


def euler_heun_exp(h: float) -> dict[str, float]:
    x0 = 1.0
    exact = math.exp(h)
    euler = x0 + h * x0
    predictor = euler
    heun = x0 + 0.5 * h * (x0 + predictor)
    return {
        "exact": exact,
        "euler": euler,
        "euler_abs_error": abs(euler - exact),
        "heun": heun,
        "heun_abs_error": abs(heun - exact),
    }


def affine_map(x: float, a: float, b: float) -> float:
    return a * x + b


def composition_audit(x: float) -> dict[str, float]:
    # Teacher T_h(x)=0.9x+1.  The exact two-step affine student is 0.81x+1.9.
    teacher_two = affine_map(affine_map(x, 0.9, 1.0), 0.9, 1.0)
    student_one = affine_map(x, 0.81, 1.9)
    constant_direct = 7.0
    constant_composed = 7.0
    return {
        "teacher_two_step": teacher_two,
        "student_one_step": student_one,
        "affine_residual": abs(student_one - teacher_two),
        "constant_map_composition_residual": abs(
            constant_direct - constant_composed
        ),
        "constant_map_endpoint_error_for_target_zero": abs(constant_direct),
    }


def meanflow_exponential(t: float, h_fd: float) -> dict[str, float]:
    assert t > h_fd > 0.0
    r = 0.0
    z_r = 1.0

    def trajectory(s: float) -> float:
        return math.exp(s)

    def average_velocity_at(s: float) -> float:
        return (trajectory(s) - z_r) / (s - r)

    z_t = trajectory(t)
    u = average_velocity_at(t)
    v = z_t
    total_derivative_fd = central_difference(average_velocity_at, t, h_fd)
    identity_rhs = v - (t - r) * total_derivative_fd
    endpoint_recovered = z_t - (t - r) * u
    return {
        "z_t": z_t,
        "instantaneous_velocity": v,
        "average_velocity": u,
        "endpoint_velocity_arithmetic_mean": 0.5 * (1.0 + z_t),
        "total_derivative_fd": total_derivative_fd,
        "identity_rhs": identity_rhs,
        "identity_abs_error": abs(u - identity_rhs),
        "recovered_z_r": endpoint_recovered,
    }


def fid_1d(mu_r: float, var_r: float, mu_g: float, var_g: float) -> float:
    assert var_r >= 0.0 and var_g >= 0.0
    return (mu_r - mu_g) ** 2 + var_r + var_g - 2.0 * math.sqrt(var_r * var_g)


def unbiased_mmd_linear(real: Sequence[float], generated: Sequence[float]) -> float:
    m, n = len(real), len(generated)
    assert m > 1 and n > 1
    rr = sum(real[i] * real[j] for i in range(m) for j in range(m) if i != j)
    gg = sum(
        generated[i] * generated[j]
        for i in range(n)
        for j in range(n)
        if i != j
    )
    rg = sum(x * y for x in real for y in generated)
    return rr / (m * (m - 1)) + gg / (n * (n - 1)) - 2.0 * rg / (m * n)


def fd_variance_gradient_1d(var_r: float, var_g: float, h_fd: float) -> dict[str, float]:
    analytic = 1.0 - math.sqrt(var_r / var_g)
    numeric = central_difference(lambda x: fid_1d(0.0, var_r, 0.0, x), var_g, h_fd)
    return {
        "analytic": analytic,
        "finite_difference": numeric,
        "abs_error": abs(analytic - numeric),
    }


def run(step: float) -> dict[str, object]:
    tilt_w1 = tilted_gaussian(a=2.0, tau2=4.0, w=1.0)
    tilt_w3 = tilted_gaussian(a=2.0, tau2=4.0, w=3.0)
    assert abs(tilt_w1["mean"] - 0.4) < 1e-12
    assert abs(tilt_w1["variance"] - 0.8) < 1e-12
    assert abs(tilt_w3["mean"] - 6.0 / 7.0) < 1e-12

    cfg_values = {str(w): cfg([1.0, 2.0], [3.0, -1.0], w) for w in [0.0, 0.5, 1.0, 4.0]}
    assert cfg_values["0.0"] == [1.0, 2.0]
    assert cfg_values["1.0"] == [3.0, -1.0]
    assert cfg_values["4.0"] == [9.0, -10.0]

    inverse = linear_gaussian_inverse(1.0, 0.8, 0.6, 2.0, 0.5, 0.3, 1.0)
    assert abs(inverse["k"] - 0.8) < 1e-12
    assert abs(inverse["conditional_variance_x0_given_xt"] - 0.36) < 1e-12
    assert abs(inverse["variance_y_given_xt"] - 1.69) < 1e-12
    assert inverse["plugin_likelihood_score"] > inverse["exact_likelihood_score"]

    ode = euler_heun_exp(0.5)
    assert ode["heun_abs_error"] < ode["euler_abs_error"]

    composition = composition_audit(2.0)
    assert composition["affine_residual"] < 1e-12
    assert composition["constant_map_composition_residual"] == 0.0
    assert composition["constant_map_endpoint_error_for_target_zero"] > 0.0

    meanflow = meanflow_exponential(1.0, step)
    assert meanflow["identity_abs_error"] < 1e-7
    assert abs(meanflow["recovered_z_r"] - 1.0) < 1e-12
    assert abs(
        meanflow["average_velocity"]
        - meanflow["endpoint_velocity_arithmetic_mean"]
    ) > 0.1

    fid = fid_1d(0.0, 1.0, 2.0, 4.0)
    kid = unbiased_mmd_linear([0.0, 2.0], [1.0, 3.0])
    fd_grad = fd_variance_gradient_1d(4.0, 9.0, step)
    assert abs(fid - 5.0) < 1e-12
    assert abs(kid + 1.0) < 1e-12
    assert fd_grad["abs_error"] < 1e-7

    return {
        "finite_difference_step": step,
        "classifier_guidance": {"w1": tilt_w1, "w3": tilt_w3},
        "cfg": cfg_values,
        "inverse_problem": inverse,
        "solver": ode,
        "distillation_and_consistency": composition,
        "meanflow": meanflow,
        "evaluation": {
            "fid_1d": fid,
            "unbiased_mmd_linear": kid,
            "fd_variance_gradient": fd_grad,
        },
        "all_assertions_passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fd-step", type=float, default=1e-5)
    args = parser.parse_args()
    print(json.dumps(run(args.fd_step), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
