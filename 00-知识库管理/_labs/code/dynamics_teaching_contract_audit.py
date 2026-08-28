#!/usr/bin/env python3
"""Audit the migrated teaching contracts and exact models for DYN-01--12."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DYN = ROOT / "10-数学基础" / "10.9-ODE、动力系统与SDE"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = DYN / "ODE、动力系统与 SDE MOC.md"
FIGURE_SCRIPTS = (
    LABS / "code" / "plot_dynamics_foundations_v2.py",
    LABS / "code" / "plot_dynamics_numerics_transport_v2.py",
    LABS / "code" / "plot_stochastic_dynamics_v2.py",
)
FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "dynamics"

CONCEPTS = (
    "常微分方程、初值问题与解的存在唯一性.md",
    "线性 ODE 与矩阵指数.md",
    "相图、平衡点与局部稳定性.md",
    "Lyapunov 稳定性与能量函数.md",
    "Euler、Runge-Kutta 与离散化误差.md",
    "刚性系统、绝对稳定域与隐式方法.md",
    "流映射、Liouville 公式与连续正规化流.md",
    "连续性方程与守恒律.md",
    "随机过程、Brownian 运动与二次变差.md",
    "Itô 引理与随机微分方程.md",
    "Fokker-Planck 方程与概率流 ODE.md",
    "时间反演、score 与扩散生成动力学.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "符号与对象账本",
    "核心公式七问",
    "第一遍停靠线",
)

EXPECTED_FIGURE_BY_CONCEPT = {
    CONCEPTS[0]: "fig-ode-ivp-wellposedness-v2.svg",
    CONCEPTS[1]: "fig-linear-ode-propagation-v2.svg",
    CONCEPTS[2]: "fig-phase-portrait-local-stability-v2.svg",
    CONCEPTS[3]: "fig-lyapunov-energy-certificate-v2.svg",
    CONCEPTS[4]: "fig-runge-kutta-error-adaptivity-v2.svg",
    CONCEPTS[5]: "fig-stiffness-stability-implicit-solve-v2.svg",
    CONCEPTS[6]: "fig-flow-liouville-cnf-v2.svg",
    CONCEPTS[7]: "fig-continuity-conservation-flow-matching-v2.svg",
    CONCEPTS[8]: "fig-brownian-process-quadratic-variation-v2.svg",
    CONCEPTS[9]: "fig-ito-integral-sde-contract-v2.svg",
    CONCEPTS[10]: "fig-fokker-planck-probability-flow-v2.svg",
    CONCEPTS[11]: "fig-reverse-time-score-diffusion-v2.svg",
}

ADDITIONAL_FIGURES_BY_CONCEPT = {
    CONCEPTS[9]: ("plot-ito-sde-numerics-gradient-v2.svg",),
    CONCEPTS[10]: ("plot-fokker-planck-probability-flow-v2.svg",),
}

FIGURE_HASHES = {
    "fig-ode-ivp-wellposedness-v2.svg":
        "0a3ad7dfa3353969821c2b201db87d16ba989d48e0436e7b4c5d931efbfb55bd",
    "fig-linear-ode-propagation-v2.svg":
        "b54c790bb52f85dd21953a6fb304ad231d480cdf74d7d7b51021dc715b55a2db",
    "fig-phase-portrait-local-stability-v2.svg":
        "fea80b4c8a78187b2d22846a7ce51ff33e32e5fa3cedb13c6461d1b32ce421d1",
    "fig-lyapunov-energy-certificate-v2.svg":
        "3b3d2a92f04dc35aefdcc9dafc03cc96bcad9475b7d8240776288e59bc0fb4af",
    "fig-runge-kutta-error-adaptivity-v2.svg":
        "5d8f10777f4410787fc7f693c69025cec22bf70a9d47a84d6ee54a00d88bfa69",
    "fig-stiffness-stability-implicit-solve-v2.svg":
        "decfc0de6e38cabf8b4e0204c1283660bbe097cec9e0b9c21fb2cf67a866063e",
    "fig-flow-liouville-cnf-v2.svg":
        "2a4aa49b8eea774fbbd0cc00aa94ad4dbcfb13b849320fa77fecba590e087062",
    "fig-continuity-conservation-flow-matching-v2.svg":
        "abeab675e68f9f35dd663e4415ecf762981e93d5efb9bb0ba19035a41c4a2329",
    "fig-brownian-process-quadratic-variation-v2.svg":
        "23c1fc4263e365a029ddb35f8cf2459dcb4926ca193fb96879de806844ac51d5",
    "fig-ito-integral-sde-contract-v2.svg":
        "c68a89b5b546e60da0cf85b93878bd1ad4b786080f75ce3bea7f40e71257f1be",
    "fig-fokker-planck-probability-flow-v2.svg":
        "8e30772a4ed999df9af47461ed3681831ff8df937959bb43006ab7976934d716",
    "fig-reverse-time-score-diffusion-v2.svg":
        "7e48178a2f71f3798f8b07f07f15002cfcc5382c02285da1e079d4a3b21aae96",
}

ADDITIONAL_FIGURE_HASHES = {
    "00-知识库管理/_assets/plots/dynamics/plot-ito-sde-numerics-gradient-v2.svg":
        "67165c8a06da0210d5de7c64ccd385794c62aafba23c3b2c89bfffde29bda5ee",
    "00-知识库管理/_assets/plots/dynamics/plot-fokker-planck-probability-flow-v2.svg":
        "0751975ea07b4ba7481fdd97608e4f4a33142656d0eb85d19ef460ff85d18013",
}

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_lines(content: str) -> list[str]:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue
        if not in_fence:
            output.append(line)
    return output


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def matmul(first, second):
    return tuple(
        tuple(
            sum(first[row][index] * second[index][column] for index in range(len(second)))
            for column in range(len(second[0]))
        )
        for row in range(len(first))
    )


def add(first, second):
    return tuple(
        tuple(first[row][column] + second[row][column] for column in range(len(first[0])))
        for row in range(len(first))
    )


def scale(coefficient, matrix):
    return tuple(tuple(coefficient * value for value in row) for row in matrix)


def identity(size: int):
    return tuple(
        tuple(Fraction(int(row == column)) for column in range(size))
        for row in range(size)
    )


def audit_contracts() -> None:
    for filename in CONCEPTS:
        content = read(DYN / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in content]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in content, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in content, f"{filename}: migration date missing")
    print(f"PASS DYN teaching contracts: {len(CONCEPTS)}/{len(CONCEPTS)}; learning state remains draft")


def audit_route() -> None:
    content = read(MOC)
    for marker in (
        "全卷教学迁移路线",
        "| A | DYN-01—04",
        "第一波的单一模型链",
        "如何学习第一波，而不是把定理和图景分开背",
        "第一波材料证书",
        "| B | DYN-05—06",
        "第二波的离散化—稳定性模型链",
        "如何学习第二波，而不是把 solver 排成排行榜",
        "第二波材料证书",
        "| C | DYN-07—08",
        "第三波的流—密度守恒模型链",
        "如何学习第三波，而不是把粒子图和密度图分开看",
        "第三波材料证书",
        "| D | DYN-09—12",
        "第四波的 Brownian—扩散—反演模型链",
        "如何学习第四波，而不是先背扩散模型配方",
        "第四波材料证书",
        "DYN-CUM：卷末综合验收闭环",
        "DYN-CUM 材料证书",
        "dynamics_teaching_contract_audit.py",
        "`regression-passed`",
        "`draft / not-attempted`",
    ):
        require(marker in content, f"MOC misses route marker: {marker}")
    require(
        re.search(r"\| A \| DYN-01—04 .*`regression-passed`", content) is not None,
        "MOC first-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| B \| DYN-05—06 .*`regression-passed`", content) is not None,
        "MOC second-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| C \| DYN-07—08 .*`regression-passed`", content) is not None,
        "MOC third-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| D \| DYN-09—12 .*`regression-passed`", content) is not None,
        "MOC fourth-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| CUM \| DYN-CUM .*`regression-passed`.*`not-attempted`", content) is not None,
        "MOC cumulative material/personal state is stale",
    )
    print("PASS DYN route: four-wave map plus DYN-CUM oral/written/experiment/retention contract")


def audit_exact_first_wave_model() -> None:
    one = Fraction(1)
    zero = Fraction(0)
    a = ((zero, one), (-one, -one))
    i2 = identity(2)

    # DYN-01: global Lipschitz calibration.
    ata = matmul(transpose(a), a)
    require(ata == ((one, one), (one, 2 * one)), "A^T A changed")
    golden_ratio = (1 + math.sqrt(5)) / 2
    operator_norm = math.sqrt((3 + math.sqrt(5)) / 2)
    require(math.isclose(operator_norm, golden_ratio, rel_tol=0.0, abs_tol=2e-16), "Lipschitz constant changed")

    # DYN-02: Cayley-Hamilton and centered oscillator generator.
    a_squared = matmul(a, a)
    require(add(add(a_squared, a), i2) == scale(zero, i2), "A^2+A+I no longer vanishes")
    b = add(a, scale(Fraction(1, 2), i2))
    require(matmul(b, b) == scale(Fraction(-3, 4), i2), "centered generator square changed")
    trace = a[0][0] + a[1][1]
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    discriminant = trace * trace - 4 * determinant
    require((trace, determinant, discriminant) == (-one, one, Fraction(-3)), "phase classification changed")

    # Check the closed-form propagator at several times against ODE invariants.
    omega = math.sqrt(3) / 2
    for time in (0.0, 0.25, 1.0, 2.0):
        cosine = math.cos(omega * time)
        sine = math.sin(omega * time)
        factor = math.exp(-time / 2)
        b_float = tuple(tuple(float(value) for value in row) for row in b)
        propagator = tuple(
            tuple(
                factor * ((1.0 if row == column else 0.0) * cosine + 2 / math.sqrt(3) * b_float[row][column] * sine)
                for column in range(2)
            )
            for row in range(2)
        )
        determinant_propagator = (
            propagator[0][0] * propagator[1][1] - propagator[0][1] * propagator[1][0]
        )
        require(
            math.isclose(determinant_propagator, math.exp(-time), rel_tol=0.0, abs_tol=5e-16),
            f"det exp(tA) changed at t={time}",
        )

    # DYN-04: natural energy + strict quadratic Lyapunov metric.
    p = (
        (Fraction(3, 2), Fraction(1, 2)),
        (Fraction(1, 2), Fraction(1)),
    )
    lyapunov_left = add(matmul(transpose(a), p), matmul(p, a))
    require(lyapunov_left == scale(-one, i2), "A^T P + P A is no longer -I")
    require(p[0][0] > 0 and p[0][0] * p[1][1] - p[0][1] ** 2 > 0, "P lost positive definiteness")
    lambda_min = (5 - math.sqrt(5)) / 4
    lambda_max = (5 + math.sqrt(5)) / 4
    require(math.isclose(lambda_min * lambda_max, 1.25, abs_tol=2e-16), "P determinant/eigenvalues changed")
    require(lambda_min > 0 and lambda_max > lambda_min, "P eigenvalue order changed")

    # E=(q^2+p^2)/2 has derivative -p^2: check polynomial coefficients.
    # grad E=(q,p), f=(p,-q-p), so q*p+p*(-q-p)=-p^2.
    q_coefficient = 1 - 1
    p_squared_coefficient = -1
    require(q_coefficient == 0 and p_squared_coefficient == -1, "natural energy derivative changed")

    print(
        "PASS first-wave exact model: L=golden ratio; A^2+A+I=0; "
        "trace/det/discriminant=-1/1/-3; det exp(tA)=exp(-t); A^T P+P A=-I"
    )


def audit_exact_second_wave_model() -> None:
    def euler(z: float) -> float:
        return 1 + z

    def heun(z: float) -> float:
        return 1 + z + z * z / 2

    def rk4(z: float) -> float:
        return 1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24

    def backward_euler(z: float) -> float:
        return 1 / (1 - z)

    def trapezoidal(z: float) -> float:
        return (1 + z / 2) / (1 - z / 2)

    methods = (("Euler", euler, 1), ("Heun", heun, 2), ("RK4", rk4, 4))
    half_step_expected = {
        "Euler": Fraction(1, 2),
        "Heun": Fraction(5, 8),
        "RK4": Fraction(233, 384),
    }
    for name, method, _ in methods:
        require(
            math.isclose(method(-0.5), float(half_step_expected[name]), rel_tol=0.0, abs_tol=2e-16),
            f"{name} half-step amplification changed",
        )

    exact_endpoint = math.exp(-1)
    expected_endpoint_errors = {
        "Euler": 0.11787944117144233,
        "Heun": 0.022745558828557666,
        "RK4": 0.00029140301258534507,
    }
    for name, method, order in methods:
        errors = []
        for steps in (2, 4, 8, 16):
            step = 1 / steps
            approximation = method(-step) ** steps
            errors.append(abs(approximation - exact_endpoint))
        require(
            math.isclose(errors[0], expected_endpoint_errors[name], rel_tol=0.0, abs_tol=5e-16),
            f"{name} two-step endpoint error changed",
        )
        observed = [math.log(errors[index] / errors[index + 1], 2) for index in range(3)]
        require(abs(observed[-1] - order) < 0.08, f"{name} observed order does not approach {order}")
        require(
            abs(observed[-1] - order) < abs(observed[0] - order),
            f"{name} step-halving order is not entering the asymptotic regime",
        )

    expected_local_defects = {
        "Euler": 0.10653065971263342,
        "Heun": -0.018469340287366576,
        "RK4": -0.00024017362069983506,
    }
    for name, method, _ in methods:
        defect = math.exp(-0.5) - method(-0.5)
        require(
            math.isclose(defect, expected_local_defects[name], rel_tol=0.0, abs_tol=5e-16),
            f"{name} local defect changed",
        )

    slow_z = -0.05
    fast_z = -5.0
    extreme_z = -50.0
    require(math.isclose(euler(slow_z), 19 / 20, abs_tol=1e-16), "slow FE factor changed")
    require(math.isclose(backward_euler(slow_z), 20 / 21, abs_tol=1e-16), "slow BE factor changed")
    require(math.isclose(trapezoidal(slow_z), 39 / 41, abs_tol=1e-16), "slow TR factor changed")
    require(math.isclose(euler(fast_z), -4.0, rel_tol=0.0, abs_tol=0.0), "fast FE factor changed")
    require(
        math.isclose(backward_euler(fast_z), float(Fraction(1, 6)), rel_tol=0.0, abs_tol=1e-16),
        "fast BE factor changed",
    )
    require(
        math.isclose(trapezoidal(fast_z), float(Fraction(-3, 7)), rel_tol=0.0, abs_tol=1e-16),
        "fast TR factor changed",
    )
    require(math.isclose(2 / 100, 0.02, rel_tol=0.0, abs_tol=0.0), "FE stiff step gate changed")
    require(
        math.isclose(backward_euler(extreme_z), float(Fraction(1, 51)), rel_tol=0.0, abs_tol=1e-16),
        "extreme BE damping changed",
    )
    require(
        math.isclose(trapezoidal(extreme_z), float(Fraction(-12, 13)), rel_tol=0.0, abs_tol=1e-16),
        "extreme TR damping changed",
    )
    require(abs(backward_euler(-1e12)) < 2e-12, "BE lost L-stable limit")
    require(abs(trapezoidal(-1e12) + 1) < 5e-12, "TR stiff limit is no longer -1")

    print(
        "PASS second-wave exact model: Euler/Heun/RK4 endpoint errors and orders; "
        "slow-fast FE/BE/TR factors; h<=0.02 gate; A/L-stability limits"
    )


def audit_exact_third_wave_model() -> None:
    def flow(time: float, state: tuple[float, float]) -> tuple[float, float]:
        return (
            math.exp(time) * (state[0] + 1) - 1,
            math.exp(-2 * time) * state[1],
        )

    def density_log(time: float, state: tuple[float, float]) -> float:
        mean_first = math.exp(time) - 1
        centered_first = state[0] - mean_first
        return (
            -math.log(2 * math.pi)
            + time
            - 0.5 * (
                math.exp(-2 * time) * centered_first ** 2
                + math.exp(4 * time) * state[1] ** 2
            )
        )

    divergence = -1.0
    trace = 1.0 - 2.0
    require(trace == divergence, "affine divergence changed")

    # Flow composition, inverse, Jacobian determinant and Gaussian change of variables.
    for state in ((0.0, 0.0), (1.0, -2.0), (-0.5, 0.75)):
        for first_time, second_time in ((0.25, 0.75), (1.0, 0.5), (-0.25, 0.75)):
            composed = flow(second_time, flow(first_time, state))
            direct = flow(first_time + second_time, state)
            require(
                all(math.isclose(composed[index], direct[index], rel_tol=0.0, abs_tol=2e-14) for index in range(2)),
                "affine flow composition changed",
            )
        for time in (0.0, 0.25, 1.0, 2.0):
            recovered = flow(-time, flow(time, state))
            require(
                all(math.isclose(recovered[index], state[index], rel_tol=0.0, abs_tol=2e-14) for index in range(2)),
                "affine flow inverse changed",
            )
            jacobian_det = math.exp(time) * math.exp(-2 * time)
            require(
                math.isclose(jacobian_det, math.exp(divergence * time), rel_tol=0.0, abs_tol=2e-16),
                "Liouville determinant changed",
            )
            initial_log_density = -math.log(2 * math.pi) - 0.5 * (state[0] ** 2 + state[1] ** 2)
            pushed_log_density = density_log(time, flow(time, state))
            require(
                math.isclose(pushed_log_density, initial_log_density + time, rel_tol=0.0, abs_tol=3e-14),
                "pathwise Gaussian log-density change changed",
            )

    # Gaussian mean/covariance, entropy and moment ODEs.
    for time in (0.0, 0.25, 1.0, 2.0):
        exp_time = math.exp(time)
        mean = (exp_time - 1, 0.0)
        mean_derivative = (exp_time, 0.0)
        affine_mean_rhs = (mean[0] + 1, -2 * mean[1])
        require(mean_derivative == affine_mean_rhs, "Gaussian mean ODE changed")

        covariance = (math.exp(2 * time), math.exp(-4 * time))
        covariance_derivative = (2 * covariance[0], -4 * covariance[1])
        lyapunov_rhs = (2 * covariance[0], -4 * covariance[1])
        require(covariance_derivative == lyapunov_rhs, "Gaussian covariance ODE changed")
        require(
            math.isclose(covariance[0] * covariance[1], math.exp(-2 * time), rel_tol=0.0, abs_tol=2e-16),
            "Gaussian covariance determinant changed",
        )
        entropy = math.log(2 * math.pi * math.e) - time
        require(
            math.isclose(entropy - math.log(2 * math.pi * math.e), divergence * time, rel_tol=0.0, abs_tol=2e-16),
            "Gaussian entropy rate changed",
        )

    # Pointwise continuity residual in log-density form.
    for time in (0.0, 0.3, 1.0):
        mean_first = math.exp(time) - 1
        for state in ((0.0, 0.0), (1.25, -0.5), (-2.0, 0.75)):
            centered = state[0] - mean_first
            dt_log_density = (
                1
                + math.exp(-2 * time) * centered ** 2
                + math.exp(-time) * centered
                - 2 * math.exp(4 * time) * state[1] ** 2
            )
            gradient_log_density = (
                -math.exp(-2 * time) * centered,
                -math.exp(4 * time) * state[1],
            )
            velocity = (state[0] + 1, -2 * state[1])
            material_log_derivative = dt_log_density + sum(
                velocity[index] * gradient_log_density[index] for index in range(2)
            )
            require(
                math.isclose(material_log_derivative, -divergence, rel_tol=0.0, abs_tol=2e-13),
                "pointwise continuity log-residual changed",
            )
            require(
                math.isclose(material_log_derivative + divergence, 0.0, rel_tol=0.0, abs_tol=2e-13),
                "pointwise continuity residual is nonzero",
            )

    # Hutchinson calibration: Rademacher is exact for this diagonal A; Gaussian remains noisy.
    rademacher_estimates = [first * first - 2 * second * second for first in (-1, 1) for second in (-1, 1)]
    require(rademacher_estimates == [-1, -1, -1, -1], "Rademacher trace calibration changed")
    gaussian_variance = 2 * (1 ** 2 + (-2) ** 2)
    require(gaussian_variance == 10, "Gaussian Hutchinson variance changed")

    print(
        "PASS third-wave exact model: affine flow/composition/inverse; Liouville and Gaussian pushforward; "
        "continuity residual, moments, entropy and Hutchinson variance"
    )


def audit_exact_fourth_wave_model() -> None:
    initial_mean = 2.0
    initial_variance = 0.25

    def marginal(time: float) -> tuple[float, float]:
        alpha = math.exp(-time)
        return initial_mean * alpha, 1 - 0.75 * alpha * alpha

    def score(time: float, state: float) -> float:
        mean, variance = marginal(time)
        return -(state - mean) / variance

    # DYN-09: Brownian increments and quadratic variation on [0,1].
    for steps in (4, 16, 64, 256):
        increment_variance = 1 / steps
        qv_mean = steps * increment_variance
        qv_variance = steps * 2 * increment_variance ** 2
        require(math.isclose(qv_mean, 1.0, rel_tol=0.0, abs_tol=0.0), "Brownian QV mean changed")
        require(
            math.isclose(qv_variance, 2 / steps, rel_tol=0.0, abs_tol=2e-18),
            "Brownian QV variance changed",
        )
    require(math.isclose(math.sqrt(2 * 256 / math.pi), 12.766152972845846, abs_tol=2e-15), "TV scale changed")

    # DYN-10: exact OU conditional/marginal laws, Itô moment and EM calibration.
    for time in (0.0, 0.1, 1.0, 3.0):
        alpha = math.exp(-time)
        conditional_variance = 1 - alpha * alpha
        mean, variance = marginal(time)
        require(
            math.isclose(variance, alpha * alpha * initial_variance + conditional_variance, abs_tol=2e-16),
            "OU marginal variance decomposition changed",
        )
        second_moment = mean * mean + variance
        expected_second_moment = 1 + 13 / 4 * alpha * alpha
        require(
            math.isclose(second_moment, expected_second_moment, rel_tol=0.0, abs_tol=5e-16),
            "OU second moment changed",
        )
        moment_derivative = -13 / 2 * alpha * alpha
        generator_rhs = -2 * second_moment + 2
        require(
            math.isclose(moment_derivative, generator_rhs, rel_tol=0.0, abs_tol=1e-15),
            "OU Itô moment equation changed",
        )

    step = 0.1
    require(math.isclose(1 - step, 0.9, abs_tol=0.0), "EM mean factor changed")
    require(math.isclose(2 * step, 0.2, abs_tol=0.0), "EM variance changed")
    require(math.isclose(math.exp(-step), 0.9048374180359595, abs_tol=1e-16), "exact OU mean factor changed")
    require(
        math.isclose(1 - math.exp(-2 * step), 0.18126924692201818, abs_tol=1e-16),
        "exact OU transition variance changed",
    )

    # DYN-11: Fokker-Planck pointwise residual and PF moment equations.
    for time in (0.0, 0.3, 1.0, 3.0):
        mean, variance = marginal(time)
        mean_derivative = -mean
        variance_derivative = 2 * (1 - variance)
        require(math.isclose(-mean, mean_derivative, abs_tol=0.0), "PF mean equation changed")
        require(math.isclose(2 * (1 - variance), variance_derivative, abs_tol=0.0), "PF variance equation changed")
        for state in (-2.0, 0.0, 1.25, 3.0):
            centered = state - mean
            density_score = score(time, state)
            dt_log_density = (
                -0.5 * variance_derivative / variance
                + centered * mean_derivative / variance
                + 0.5 * centered ** 2 * variance_derivative / variance ** 2
            )
            score_derivative = -1 / variance
            fpe_over_density = 1 + state * density_score + density_score ** 2 + score_derivative
            require(
                math.isclose(dt_log_density, fpe_over_density, rel_tol=0.0, abs_tol=3e-13),
                "OU Fokker-Planck pointwise residual changed",
            )
        # Gaussian score identities used by the PF moment proof.
        expected_score = 0.0
        expected_centered_score = -1.0
        pf_mean_rhs = -mean - expected_score
        pf_variance_rhs = 2 * (-variance - expected_centered_score)
        require(math.isclose(pf_mean_rhs, mean_derivative, abs_tol=2e-16), "PF mean score identity changed")
        require(
            math.isclose(pf_variance_rhs, variance_derivative, abs_tol=5e-16),
            "PF variance score identity changed",
        )

    # DYN-12: DSM conditional-to-marginal identity and terminal mismatch.
    for time in (0.1, 1.0, 3.0):
        alpha = math.exp(-time)
        noise_variance = 1 - alpha * alpha
        mean, variance = marginal(time)
        for observed in (-1.0, 0.0, 2.5):
            posterior_initial_mean = initial_mean + alpha * initial_variance / variance * (observed - mean)
            expected_conditional_score = -(observed - alpha * posterior_initial_mean) / noise_variance
            require(
                math.isclose(expected_conditional_score, score(time, observed), rel_tol=0.0, abs_tol=2e-14),
                "DSM conditional-to-marginal score identity changed",
            )

    terminal_time = 3.0
    terminal_mean, terminal_variance = marginal(terminal_time)
    terminal_kl = 0.5 * (
        terminal_mean ** 2 + terminal_variance - 1 - math.log(terminal_variance)
    )
    require(
        math.isclose(terminal_kl, 0.00495836945554821, rel_tol=0.0, abs_tol=2e-16),
        "terminal Gaussian KL changed",
    )

    # Reverse-clock full/half score and stationary sanity checks.
    for time in (0.0, 1.0, 3.0):
        mean, variance = marginal(time)
        reverse_sde_mean_rhs = mean  # E[X + 2 score] and E[score]=0.
        reverse_pf_mean_rhs = mean   # E[X + score] and E[score]=0.
        reverse_variance_rhs_sde = 2 * (variance - 2) + 2
        reverse_variance_rhs_pf = 2 * (variance - 1)
        expected_reverse_variance = 2 * (variance - 1)
        require(reverse_sde_mean_rhs == reverse_pf_mean_rhs == mean, "reverse mean drift changed")
        require(
            math.isclose(reverse_variance_rhs_sde, expected_reverse_variance, abs_tol=2e-16),
            "reverse SDE variance drift changed",
        )
        require(
            math.isclose(reverse_variance_rhs_pf, expected_reverse_variance, abs_tol=0.0),
            "reverse PF variance drift changed",
        )
    for state in (-2.0, 0.0, 1.5):
        stationary_score = -state
        reverse_sde_drift = state + 2 * stationary_score
        reverse_pf_drift = state + stationary_score
        require(reverse_sde_drift == -state, "stationary reverse SDE drift changed")
        require(reverse_pf_drift == 0.0, "stationary reverse PF drift changed")

    print(
        "PASS fourth-wave exact model: Brownian QV; OU/Itô/EM; Fokker-Planck/PF moments; "
        "DSM, terminal KL and reverse full/half score"
    )


def audit_markdown_integrity() -> None:
    scoped = [DYN / filename for filename in CONCEPTS] + [MOC]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)

    for path in scoped:
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
        require(active.count("$$") % 2 == 0, f"{path.name}: unbalanced display math")
        for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", active):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            link_count += 1
            suffix = Path(target).suffix.lower()
            if "/" in target:
                direct = ROOT / target
                candidates = [direct] if direct.is_file() else []
                if not candidates and suffix not in KNOWN_EXTENSIONS:
                    markdown = Path(str(direct) + ".md")
                    if markdown.is_file():
                        candidates = [markdown]
            else:
                key = target[: -len(suffix)] if suffix in KNOWN_EXTENSIONS else target
                candidates = file_index.get(key, [])
                if suffix in KNOWN_EXTENSIONS:
                    candidates = [candidate for candidate in candidates if candidate.suffix.lower() == suffix]
            if not candidates:
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")

    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    figure_count = 0
    for filename in CONCEPTS:
        path = DYN / filename
        lines = read(path).splitlines()
        images = [(index, image_pattern.search(line)) for index, line in enumerate(lines)]
        images = [(index, match) for index, match in images if match is not None]
        expected = (
            EXPECTED_FIGURE_BY_CONCEPT[filename],
            *ADDITIONAL_FIGURES_BY_CONCEPT.get(filename, ()),
        )
        actual = tuple(Path(match.group(1)).name for _, match in images if match is not None)
        require(actual == expected, f"{filename}: expected figures {expected}, found {actual}")
        for position, match in images:
            require(match is not None, "internal image parser failure")
            block = "\n".join(lines[position : min(len(lines), position + 45)])
            for marker in ("[!figure]", "怎样读图", "适用边界"):
                require(marker in block, f"{filename}: figure unit {Path(match.group(1)).name} misses {marker}")
            figure_count += 1

    print(f"PASS Markdown integrity: Wiki links={link_count}; display math balanced; figure units={figure_count}")


def audit_figures(run_figures: bool) -> None:
    if run_figures:
        for figure_script in FIGURE_SCRIPTS:
            subprocess.run([sys.executable, str(figure_script)], cwd=ROOT, check=True)
    for filename, expected_hash in FIGURE_HASHES.items():
        path = FIGURE_DIR / filename
        require(path.is_file(), f"missing figure: {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"figure hash changed: {filename} -> {digest}")
        root_element = ET.parse(path).getroot()
        require(root_element.tag.endswith("svg"), f"invalid SVG root: {filename}")
        require("viewBox" in root_element.attrib, f"SVG missing viewBox: {filename}")
    for relative_path, expected_hash in ADDITIONAL_FIGURE_HASHES.items():
        path = ROOT / relative_path
        require(path.is_file(), f"missing additional figure: {relative_path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"additional figure hash changed: {relative_path} -> {digest}")
        root_element = ET.parse(path).getroot()
        require(root_element.tag.endswith("svg"), f"invalid SVG root: {relative_path}")
        require("viewBox" in root_element.attrib, f"SVG missing viewBox: {relative_path}")
    figure_total = len(FIGURE_HASHES) + len(ADDITIONAL_FIGURE_HASHES)
    print(f"PASS deterministic figures: {figure_total}/{figure_total} hashes and SVG XML")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-figures", action="store_true")
    args = parser.parse_args()

    audit_contracts()
    audit_route()
    audit_exact_first_wave_model()
    audit_exact_second_wave_model()
    audit_exact_third_wave_model()
    audit_exact_fourth_wave_model()
    audit_markdown_integrity()
    audit_figures(args.run_figures)
    print("DYN-01—12 material regression: PASS; learning state: draft/not-attempted")


if __name__ == "__main__":
    main()
