#!/usr/bin/env python3
"""Standard-library numerical audit for GEN-49--56.

The examples are scalar or two-point by design.  They verify continuous-time
diffusion, score projection, flow matching and finite-step contracts; they do
not train a neural network and are not a generative-quality benchmark.
"""

from __future__ import annotations

import math
import random
import statistics


TOL = 1e-10


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def mean_and_var(values: list[float]) -> tuple[float, float]:
    return statistics.fmean(values), statistics.pvariance(values)


def audit_vp_ve_subvp() -> None:
    beta, t = 2.0, 0.5
    B = beta * t
    mean_coefficient = math.exp(-0.5 * B)
    vp_var = 1.0 - math.exp(-B)
    subvp_var = (1.0 - math.exp(-B)) ** 2
    ve_var = 2.0 * t

    assert close(mean_coefficient, math.exp(-0.5))
    assert subvp_var < vp_var < ve_var + 1e-12
    vp_rhs = -beta * vp_var + beta
    vp_derivative = beta * math.exp(-B)
    subvp_rhs = -beta * subvp_var + beta * (1.0 - math.exp(-2.0 * B))
    subvp_derivative = 2.0 * beta * math.exp(-B) * (1.0 - math.exp(-B))
    assert close(vp_rhs, vp_derivative)
    assert close(subvp_rhs, subvp_derivative)

    x0 = 1.5
    rng = random.Random(4901)
    samples = [mean_coefficient * x0 + math.sqrt(vp_var) * rng.gauss(0.0, 1.0) for _ in range(80_000)]
    sample_mean, sample_var = mean_and_var(samples)
    assert abs(sample_mean - mean_coefficient * x0) < 0.012
    assert abs(sample_var - vp_var) < 0.012
    print(
        f"GEN49 m={mean_coefficient:.6f} vp_var={vp_var:.6f} "
        f"subvp_var={subvp_var:.6f} ve_var={ve_var:.6f} "
        f"mc_mean_gap={sample_mean-mean_coefficient*x0:.3e} mc_var_gap={sample_var-vp_var:.3e}"
    )


def audit_reverse_time_sign() -> None:
    beta, x = 1.7, 0.8
    forward_drift = -0.5 * beta * x
    score = -x  # stationary N(0,1)
    g2 = beta
    decreasing_t_bracket = forward_drift - g2 * score
    increasing_tau_drift = -forward_drift + g2 * score
    assert close(increasing_tau_drift, -0.5 * beta * x)
    assert close(decreasing_t_bracket, -increasing_tau_drift)

    dt = -0.01
    d_tau = 0.01
    assert close(decreasing_t_bracket * dt, increasing_tau_drift * d_tau)

    t = 0.6
    brownian_score = -x / (4.0 + t)
    brownian_reverse_drift = brownian_score
    assert brownian_reverse_drift < 0.0
    print(
        f"GEN50 t_bracket={decreasing_t_bracket:.6f} tau_drift={increasing_tau_drift:.6f} "
        f"actual_step_gap={decreasing_t_bracket*dt-increasing_tau_drift*d_tau:.3e} "
        f"brownian_reverse={brownian_reverse_drift:.6f}"
    )


def audit_probability_flow() -> None:
    rng_sde = random.Random(5101)
    rng_ode = random.Random(5102)
    t = 1.0
    n = 80_000
    sde_endpoints = [rng_sde.gauss(0.0, 1.0) + rng_sde.gauss(0.0, math.sqrt(t)) for _ in range(n)]
    ode_endpoints = [math.sqrt(1.0 + t) * rng_ode.gauss(0.0, 1.0) for _ in range(n)]
    sde_mean, sde_var = mean_and_var(sde_endpoints)
    ode_mean, ode_var = mean_and_var(ode_endpoints)
    assert abs(sde_mean) < 0.02 and abs(ode_mean) < 0.02
    assert abs(sde_var - 2.0) < 0.035 and abs(ode_var - 2.0) < 0.035
    assert abs(sde_var - ode_var) < 0.045

    # One Brownian path has O(1) quadratic variation; a smooth PF path has O(h).
    steps = 10_000
    h = 1.0 / steps
    rng_path = random.Random(5103)
    brownian_qv = sum((math.sqrt(h) * rng_path.gauss(0.0, 1.0)) ** 2 for _ in range(steps))
    x0 = 1.0
    ode_points = [x0 * math.sqrt(1.0 + k * h) for k in range(steps + 1)]
    ode_qv = sum((ode_points[k + 1] - ode_points[k]) ** 2 for k in range(steps))
    assert 0.94 < brownian_qv < 1.06
    assert ode_qv < 1e-3
    print(
        f"GEN51 sde_var={sde_var:.6f} ode_var={ode_var:.6f} "
        f"brownian_qv={brownian_qv:.6f} ode_qv={ode_qv:.3e}"
    )


def audit_score_projection() -> None:
    tau0, a, sigma = 2.0, 2.0, 3.0
    marginal_var = a * a * tau0 * tau0 + sigma * sigma
    constant_gap = a * a * tau0 * tau0 / (sigma * sigma * marginal_var)
    rng = random.Random(5201)
    triples: list[tuple[float, float, float]] = []
    for _ in range(120_000):
        x0 = rng.gauss(0.0, tau0)
        eps = rng.gauss(0.0, 1.0)
        xt = a * x0 + sigma * eps
        conditional_score = -eps / sigma
        marginal_score = -xt / marginal_var
        triples.append((xt, conditional_score, marginal_score))

    gaps = []
    for coefficient in (-0.09, 0.04):
        conditional_loss = statistics.fmean((u - coefficient * x) ** 2 for x, u, _ in triples)
        marginal_loss = statistics.fmean((m - coefficient * x) ** 2 for x, _, m in triples)
        gaps.append(conditional_loss - marginal_loss)
    assert abs(gaps[0] - constant_gap) < 0.003
    assert abs(gaps[1] - constant_gap) < 0.003
    assert abs(gaps[0] - gaps[1]) < 0.003
    print(
        f"GEN52 analytic_gap={constant_gap:.8f} observed_gaps=({gaps[0]:.8f},{gaps[1]:.8f}) "
        f"gap_difference={gaps[0]-gaps[1]:.3e}"
    )


def audit_flow_matching_weak_form() -> None:
    t = 0.3
    alpha, sigma = math.sqrt(1.0 - t), math.sqrt(t)
    alpha_dot = -0.5 / math.sqrt(1.0 - t)
    sigma_dot = 0.5 / math.sqrt(t)
    rng = random.Random(5301)
    x_values: list[float] = []
    u_values: list[float] = []
    for _ in range(120_000):
        x0 = rng.gauss(0.0, 1.0)
        eps = rng.gauss(0.0, 1.0)
        x_values.append(alpha * x0 + sigma * eps)
        u_values.append(alpha_dot * x0 + sigma_dot * eps)

    # For the stationary N(0,1) marginal path, the best linear marginal field is zero.
    cov_xu = statistics.fmean(x * u for x, u in zip(x_values, u_values))
    weak_x2_residual = 2.0 * cov_xu  # d/dt E[X^2] = E[2 X U] = 0.
    x_var = statistics.pvariance(x_values)
    assert abs(x_var - 1.0) < 0.015
    assert abs(cov_xu) < 0.015
    assert abs(weak_x2_residual) < 0.03
    assert statistics.pvariance(u_values) > 0.5  # conditional targets move although v=0.
    print(
        f"GEN53 marginal_var={x_var:.6f} cov_XU={cov_xu:.3e} "
        f"weak_x2_residual={weak_x2_residual:.3e} conditional_U_var={statistics.pvariance(u_values):.6f}"
    )


def audit_coupling_and_ot() -> None:
    identity_velocities = (0.0, 0.0)
    swap_velocities = (2.0, -2.0)
    assert close(statistics.fmean(identity_velocities), 0.0)
    assert close(statistics.pvariance(identity_velocities), 0.0)
    assert close(statistics.fmean(swap_velocities), 0.0)
    assert close(statistics.pvariance(swap_velocities), 4.0)

    same_order_cost = (1.0 - 0.0) ** 2 + (4.0 - 3.0) ** 2
    crossing_cost = (4.0 - 0.0) ** 2 + (1.0 - 3.0) ** 2
    assert close(same_order_cost, 2.0)
    assert close(crossing_cost, 20.0)

    batch_diagonal = 1.0 + 0.0
    batch_off_diagonal = 9.0 + 4.0
    assert batch_diagonal < batch_off_diagonal
    print(
        f"GEN54 identity_var=0.000000 swap_var={statistics.pvariance(swap_velocities):.6f} "
        f"same_order_cost={same_order_cost:.1f} crossing_cost={crossing_cost:.1f} "
        f"batch_assignment={batch_diagonal:.1f}<{batch_off_diagonal:.1f}"
    )


def reverse_euler_tx(z1: float, steps: int) -> float:
    z = z1
    h = -1.0 / steps
    t = 1.0
    for _ in range(steps):
        z += (t * z) * h
        t += h
    return z


def audit_rectified_flow_and_finite_steps() -> None:
    z1 = 1.0
    exact = math.exp(-0.5) * z1
    estimates = [reverse_euler_tx(z1, steps) for steps in (1, 2, 4, 8, 32)]
    errors = [abs(value - exact) for value in estimates]
    assert close(estimates[0], 0.0)
    assert all(errors[k + 1] < errors[k] for k in range(len(errors) - 1))

    path_length_ratio = (3.0 + 4.0) / 5.0
    assert close(path_length_ratio, 1.4)
    x, t = 1.2, 0.7
    material_acceleration = x + t * (t * x)  # partial_t(t*x) + J_x(t*x)*(t*x)
    assert close(material_acceleration, x * (1.0 + t * t))
    print(
        f"GEN55 exact={exact:.8f} estimates={[round(v, 8) for v in estimates]} "
        f"errors={[round(v, 8) for v in errors]} length_ratio={path_length_ratio:.3f} "
        f"material_accel={material_acceleration:.6f}"
    )


def audit_unified_parameterizations() -> None:
    phi, x0, eps = 0.7, 1.3, -0.4
    alpha, sigma = math.cos(phi), math.sin(phi)
    angle_velocity = -sigma * x0 + alpha * eps
    diffusion_v = alpha * eps - sigma * x0
    assert close(angle_velocity, diffusion_v)

    t = 0.5
    general_velocity = -x0 + 2.0 * t * eps
    mislabeled_diffusion_v = (1.0 - t) * eps - t * t * x0
    assert not close(general_velocity, mislabeled_diffusion_v)

    v, score, epsilon_rate = -1.0, -2.0, 0.3  # coefficients multiplying x
    sde_drift = v + epsilon_rate * score
    diffusion = math.sqrt(2.0 * epsilon_rate)
    assert close(sde_drift, -1.6)
    assert close(diffusion * diffusion, 0.6)

    # Invertible target scaling changes an unweighted squared-error metric.
    residuals = (1.0, 1.0)
    scales = (1.0, 3.0)
    original_mse = statistics.fmean(r * r for r in residuals)
    transformed_mse = statistics.fmean((a * r) ** 2 for a, r in zip(scales, residuals))
    assert close(original_mse, 1.0)
    assert close(transformed_mse, 5.0)
    print(
        f"GEN56 angle_v_gap={angle_velocity-diffusion_v:.3e} "
        f"general_v_gap={general_velocity-mislabeled_diffusion_v:.6f} "
        f"same_density_sde_drift={sde_drift:.3f} diffusion={diffusion:.6f} "
        f"mse_metric={original_mse:.1f}->{transformed_mse:.1f}"
    )


def main() -> None:
    audit_vp_ve_subvp()
    audit_reverse_time_sign()
    audit_probability_flow()
    audit_score_projection()
    audit_flow_matching_weak_form()
    audit_coupling_and_ot()
    audit_rectified_flow_and_finite_steps()
    audit_unified_parameterizations()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
