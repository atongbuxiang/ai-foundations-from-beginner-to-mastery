#!/usr/bin/env python3
"""Exact and deterministic audits for GEN-17--24."""

import json
import math


def kl(p, q):
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q) if pi > 0)


def optimal_discriminator_js():
    p, q = [0.8, 0.2], [0.4, 0.6]
    d_star = [pi / (pi + qi) for pi, qi in zip(p, q)]
    value = sum(pi * math.log(di) + qi * math.log(1 - di)
                for pi, qi, di in zip(p, q, d_star))
    m = [(pi + qi) / 2 for pi, qi in zip(p, q)]
    js = 0.5 * (kl(p, m) + kl(q, m))
    residual = value - (-math.log(4) + 2 * js)
    assert abs(residual) < 1e-14
    return {"d_star": d_star, "js": js, "value": value, "residual": residual}


def generator_gradients():
    rows = {}
    for d in (0.01, 0.5, 0.8):
        rows[str(d)] = {
            "saturating_logit_slope": -d,
            "non_saturating_logit_slope": -(1 - d),
        }
    assert abs(rows["0.01"]["non_saturating_logit_slope"]) > 50 * abs(
        rows["0.01"]["saturating_logit_slope"]
    )
    return rows


def pointmass_topology():
    rows = []
    for theta in (1.0, 0.1, 0.001, 0.0):
        js = math.log(2) if theta != 0 else 0.0
        w1 = abs(theta)
        rows.append({"theta": theta, "js": js, "w1": w1})
    assert rows[-2]["js"] == math.log(2) and rows[-2]["w1"] == 0.001
    return rows


def sampled_gradient_counterexample():
    # f(x)=x+A*x^2*(1-x)^2 has f'(0)=f'(1)=1 but a large interior slope.
    a = 50.0

    def derivative(x):
        return 1 + a * 2 * x * (1 - x) * (1 - 2 * x)

    sampled = [derivative(0.0), derivative(1.0)]
    hidden = derivative(0.25)
    assert sampled == [1.0, 1.0] and hidden > 10.0
    return {"sampled_gradients": sampled, "hidden_gradient_at_0.25": hidden}


def bilinear_dynamics():
    rows = []
    for eta in (0.01, 0.1, 0.5):
        eigen_modulus = math.sqrt(1 + eta * eta)
        radius_squared_factor = 1 + eta * eta
        assert eigen_modulus > 1
        rows.append({
            "eta": eta,
            "simultaneous_gda_eigen_modulus": eigen_modulus,
            "radius_squared_factor_per_step": radius_squared_factor,
        })
    return rows


def mode_coverage():
    real_modes, generated_modes = 8, 2
    result = {
        "real_entropy": math.log(real_modes),
        "generated_entropy": math.log(generated_modes),
        "precision_if_both_generated_modes_are_valid": 1.0,
        "mode_recall": generated_modes / real_modes,
    }
    assert result["mode_recall"] == 0.25
    return result


def main():
    report = {
        "experiment": "experiment_gan_objectives_dynamics_audit_v1",
        "optimal_discriminator_js": optimal_discriminator_js(),
        "generator_gradients": generator_gradients(),
        "pointmass_topology": pointmass_topology(),
        "sampled_gradient_counterexample": sampled_gradient_counterexample(),
        "bilinear_dynamics": bilinear_dynamics(),
        "mode_coverage": mode_coverage(),
        "all_assertions_passed": True,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

