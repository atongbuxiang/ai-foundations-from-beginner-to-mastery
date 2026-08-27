#!/usr/bin/env python3
"""Audit NUM-01--20 teaching contracts and their shared exact models."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NUM = ROOT / "10-数学基础" / "10.8-数值计算"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = NUM / "数值线性代数 MOC.md"
FIGURE_SCRIPTS = (
    LABS / "code" / "plot_numerical_error_foundations_v2.py",
    LABS / "code" / "plot_numerical_direct_methods_v2.py",
    LABS / "code" / "plot_numerical_spectral_methods_v2.py",
    LABS / "code" / "plot_numerical_iterative_methods_v2.py",
    LABS / "code" / "plot_numerical_large_scale_v2.py",
)
FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "numerical-analysis"

CONCEPTS = (
    "浮点数与舍入误差.md",
    "前向误差与后向误差.md",
    "数值稳定性.md",
    "误差传播、条件估计与停止准则.md",
    "稳定求和、点积与矩阵乘法.md",
    "稳定求解线性方程组.md",
    "迭代改进、混合精度与残差校正.md",
    "Householder 与 Givens 变换.md",
    "稳定最小二乘与正规方程的风险.md",
    "幂法、反幂法与 Rayleigh 商迭代.md",
    "Hessenberg 化与 QR 特征值算法.md",
    "Lanczos 方法.md",
    "Arnoldi 方法.md",
    "SVD 算法与谱范数估计.md",
    "定常迭代法与谱半径.md",
    "Krylov 子空间与预条件.md",
    "共轭梯度法.md",
    "GMRES、MINRES 与残差最小化.md",
    "稀疏矩阵计算与存储复杂度.md",
    "随机化低秩近似与随机 SVD.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "符号与对象账本",
    "核心公式七问",
    "第一遍停靠线",
)

FIGURE_HASHES = {
    "fig-floating-point-system-v2.svg":
        "6661ec2e7b0e29c247e523d3cd45baf0acf4b03cdb5d18575c2f32ea5eee5496",
    "fig-error-analysis-pipeline-v2.svg":
        "f1216c5f9fe64649dd89e73626344cdd4d0f1dc9035d931763a374c7a97c58f8",
    "fig-numerical-stability-formulas-v2.svg":
        "07fbfaa757a0da24a9e64ddce55363befa00256f7c082c0ee2b30c473a2076ad",
    "fig-condition-estimation-stopping-v2.svg":
        "093aab40c145748496067227590ec447d1b51c696a98223d4a96fe0ded98e692",
    "fig-stable-reductions-matmul-v2.svg":
        "477695f5f42dd5c192d7fed82061f74e49d87bd99aa9cc373dd99819f00c0190",
    "fig-pivoting-linear-solve-v2.svg":
        "bb80e8861932835aae21c7cb5e4f438160acce225176f0a7ed85c0db6a9196fa",
    "fig-mixed-precision-refinement-v2.svg":
        "722547f7da7a0d8b9b64fed9e89310eff94462272c4a94a328d3278f6fbfffe9",
    "fig-householder-givens-qr-v2.svg":
        "4615fa61a36cfbb3850b57162c329f792e289d1b77102d94354dae22b6ab1763",
    "fig-least-squares-stability-v2.svg":
        "5a002005fa09e4c644aec0887f2187c8dd197240beb6a1c004655fcfdc67ce8f",
    "fig-power-inverse-rqi-v2.svg":
        "48eba2f05d344f48ad9ed3b3e2b201731a9fbae5f243684dddf7df5b0cf31c83",
    "fig-hessenberg-qr-v2.svg":
        "7293cca54668a0fc602850b3cc14d3c82d75cd844bba06f3a7c0cf0278a847ed",
    "fig-lanczos-ritz-orthogonality-v2.svg":
        "e9acfc1589089c3247f741fd8e4ac03d228bd0e8cd569ba7041f662e571f8aa1",
    "fig-arnoldi-restart-nonnormal-v2.svg":
        "91450824d66739919426790c4e49b7243d5e717446e8ea4222f27618f47325ee",
    "fig-svd-algorithms-certificates-v2.svg":
        "15a3f7673e074e185c22b6cb36dc543e5a8f0a5861d024edc4122b5165e9cc25",
    "fig-stationary-spectral-radius-v2.svg":
        "d6367268a954abbe1fd6e5826b81b3c9c8604a1832c7b370d056034ed0e27e60",
    "fig-krylov-preconditioning-v2.svg":
        "5be8d00a01ffafbe66554d11139e85d5eec644e00ee03f9fd2a5f1c87bacf025",
    "fig-conjugate-gradient-contract-v2.svg":
        "ff6b1e1ac447e3851b037b8f78a6040eef7c49fb644dcbdc15e221e31fe9a902",
    "fig-gmres-minres-restart-v2.svg":
        "66f4214a36c53eca304a8130687a612cf0a22cac8c0eba56660dc86fb76d116e",
    "fig-sparse-computing-contract-v2.svg":
        "9a17925a06039f1d1a3bbe1020c3d83479d2a237aaa32aa61d408474876e0e76",
    "fig-randomized-svd-certificate-v2.svg":
        "87eddd707fe2fc11cf44c77146937908a4fe420241fccc5f3667648c959cac5c",
}

EXPECTED_FIGURE_BY_CONCEPT = {
    CONCEPTS[0]: "fig-floating-point-system-v2.svg",
    CONCEPTS[1]: "fig-error-analysis-pipeline-v2.svg",
    CONCEPTS[2]: "fig-numerical-stability-formulas-v2.svg",
    CONCEPTS[3]: "fig-condition-estimation-stopping-v2.svg",
    CONCEPTS[4]: "fig-stable-reductions-matmul-v2.svg",
    CONCEPTS[5]: "fig-pivoting-linear-solve-v2.svg",
    CONCEPTS[6]: "fig-mixed-precision-refinement-v2.svg",
    CONCEPTS[7]: "fig-householder-givens-qr-v2.svg",
    CONCEPTS[8]: "fig-least-squares-stability-v2.svg",
    CONCEPTS[9]: "fig-power-inverse-rqi-v2.svg",
    CONCEPTS[10]: "fig-hessenberg-qr-v2.svg",
    CONCEPTS[11]: "fig-lanczos-ritz-orthogonality-v2.svg",
    CONCEPTS[12]: "fig-arnoldi-restart-nonnormal-v2.svg",
    CONCEPTS[13]: "fig-svd-algorithms-certificates-v2.svg",
    CONCEPTS[14]: "fig-stationary-spectral-radius-v2.svg",
    CONCEPTS[15]: "fig-krylov-preconditioning-v2.svg",
    CONCEPTS[16]: "fig-conjugate-gradient-contract-v2.svg",
    CONCEPTS[17]: "fig-gmres-minres-restart-v2.svg",
    CONCEPTS[18]: "fig-sparse-computing-contract-v2.svg",
    CONCEPTS[19]: "fig-randomized-svd-certificate-v2.svg",
}

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_lines(text: str) -> list[str]:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in text.splitlines():
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


def audit_contracts() -> None:
    for filename in CONCEPTS:
        text = read(NUM / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in text, f"{filename}: migration date missing")
    print(f"PASS NUM teaching contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_route() -> None:
    text = read(MOC)
    for marker in (
        "全卷教学迁移路线",
        "| A | NUM-01—04",
        "| B | NUM-05—08",
        "| C | NUM-09—12",
        "| D | NUM-13—16",
        "| E | NUM-17—20",
        "第一波的单一模型链",
        "如何学习第一波，而不是只把它读完",
        "第二波的单一模型链",
        "如何学习第二波，而不是背算法名",
        "第二波材料证书",
        "第三波的单一模型链",
        "如何学习第三波，而不是把谱算法混成一类",
        "第三波材料证书",
        "第四波的单一模型链",
        "如何学习第四波，而不是把所有迭代都叫“幂法”",
        "第四波材料证书",
        "第五波的单一模型链",
        "如何学习第五波，而不是只比较算法名称",
        "第五波材料证书",
        "全卷静态迁移结论",
        "numerical_teaching_contract_audit.py",
        "`regression-passed`",
        "`draft / not-attempted`",
    ):
        require(marker in text, f"MOC misses route marker: {marker}")
    require(
        re.search(r"\| B \| NUM-05—08 .*`regression-passed`", text) is not None,
        "MOC second-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| C \| NUM-09—12 .*`regression-passed`", text) is not None,
        "MOC third-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| D \| NUM-13—16 .*`regression-passed`", text) is not None,
        "MOC fourth-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| E \| NUM-17—20 .*`regression-passed`", text) is not None,
        "MOC fifth-wave material status is not regression-passed",
    )
    require("Gram-Schmidt 的数值稳定性" not in text, "MOC retains missing placeholder link")
    print("PASS NUM route: five waves, five migrated model chains, three-pass learning contracts")


def audit_exact_scalar_model() -> None:
    tau = Fraction(1, 10_000)
    gap_at_one = Fraction(1, 1_000)
    unit_roundoff = Fraction(1, 2_000)
    half_gap = gap_at_one / 2

    require(tau < half_gap, "tau should be absorbed when added to 1 in F_{10,4}")
    require(gap_at_one == 2 * unit_roundoff, "gap/unit-roundoff convention changed")

    naive = Fraction(0)
    stable = Fraction(1, 20_000)
    exact = math.sqrt(1.0 + float(tau)) - 1.0
    stable_forward = abs(float(stable) - exact) / exact
    require(naive == 0, "naive cancellation output changed")
    require(2.49e-5 < stable_forward < 2.51e-5, "stable forward error changed")
    require(stable_forward < float(unit_roundoff), "stable formula is no longer O(u)-accurate")

    stable_neighbor = 2 * stable + stable**2
    stable_backward = abs(stable_neighbor - tau) / tau
    naive_neighbor = Fraction(0)
    naive_backward = abs(naive_neighbor - tau) / tau
    require(stable_neighbor == Fraction(40_001, 400_000_000), "stable neighbor input changed")
    require(stable_backward == Fraction(1, 40_000), "stable backward error changed")
    require(naive_backward == 1, "naive backward error changed")

    condition = (math.sqrt(1.0 + float(tau)) + 1.0) / (
        2.0 * math.sqrt(1.0 + float(tau))
    )
    require(0.9999 < condition <= 1.0, "scalar relative condition calibration changed")
    print(
        "PASS scalar model: gap=1e-3, u=5e-4, naive backward=1, "
        "stable backward=2.5e-5, kappa_rel≈1"
    )


def audit_exact_linear_model() -> None:
    tau = Fraction(1, 10_000)

    # A=diag(1,tau), x*=(1,1), xhat=(1,0), b=(1,tau), r=(0,tau).
    forward_error_squared = Fraction(1, 2)
    residual_ratio_squared = tau**2 / (1 + tau**2)
    condition_number = 1 / tau
    amplified_risk_squared = condition_number**2 * residual_ratio_squared

    require(forward_error_squared == Fraction(1, 2), "relative forward error changed")
    require(condition_number == 10_000, "diagonal condition number changed")
    require(
        amplified_risk_squared == Fraction(1, 1) / (1 + tau**2),
        "condition-amplified residual identity changed",
    )

    rho = float(tau) / math.sqrt(1.0 + float(tau**2))
    joint = float(tau) / (1.0 + math.sqrt(1.0 + float(tau**2)))
    componentwise = Fraction(1)
    require(rho < 1e-4, "naive residual gate should strictly pass")
    require(4.999e-5 < joint < 5.001e-5, "joint backward error changed")
    require(componentwise == 1, "componentwise backward error changed")

    task_budget = Fraction(1, 100)
    required_rho = task_budget / condition_number
    require(required_rho == Fraction(1, 1_000_000), "condition-aware tolerance changed")
    require(rho > float(required_rho), "candidate should fail the task-aware gate")
    print(
        "PASS linear model: forward=1/sqrt(2), rho<1e-4, kappa=1e4, "
        "kappa*rho≈1, eta_joint≈5e-5, eta_comp=1, required rho=1e-6"
    )


def decimal4_context() -> Context:
    return Context(
        prec=4,
        rounding=ROUND_HALF_EVEN,
        Emin=-999,
        Emax=999,
    )


def neumaier_decimal4(values: tuple[Decimal, ...]) -> Decimal:
    with localcontext(decimal4_context()):
        total = Decimal(0)
        correction = Decimal(0)
        for value in values:
            updated = total + value
            if abs(total) >= abs(value):
                correction += (total - updated) + value
            else:
                correction += (value - updated) + total
            total = updated
        return +(total + correction)


def audit_exact_direct_model() -> None:
    eps = Fraction(1, 100_000_000)
    one = Fraction(1)

    # Reduction conditioning and exact sum.
    reduction = (1 / eps, one, -1 / eps)
    require(sum(reduction) == 1, "second-wave exact reduction changed")
    require(sum(abs(value) for value in reduction) == 200_000_001, "sum condition changed")

    with localcontext(decimal4_context()):
        huge = Decimal("1e8")
        left = +(+(huge + Decimal(1)) - huge)
        cancel_first = +(+(huge - huge) + Decimal(1))
        require(left == 0, "left-associated F_{10,4} sum should lose the unit")
        require(cancel_first == 1, "cancel-first F_{10,4} sum should recover the unit")
    compensated = neumaier_decimal4((Decimal("1e8"), Decimal(1), Decimal("-1e8")))
    require(compensated == 1, "Neumaier teaching reduction no longer recovers the tail")

    # Exact system A=[[eps,1],[1,1]], b=(1,2).
    denominator = 1 - eps
    x_star = (1 / denominator, (1 - 2 * eps) / denominator)
    kappa_inf = 4 / denominator
    require(kappa_inf == Fraction(400_000_000, 99_999_999), "kappa_inf changed")

    with localcontext(decimal4_context()):
        eps4 = Decimal("1e-8")
        multiplier = Decimal(1) / eps4
        u22 = Decimal(1) - multiplier
        rhs2 = Decimal(2) - multiplier
        x2_no_pivot = rhs2 / u22
        x1_no_pivot = (Decimal(1) - x2_no_pivot) / eps4
        require(multiplier == Decimal("1e8"), "unpivoted multiplier changed")
        require(u22 == rhs2 == Decimal("-1.000e8"), "distinct elimination values should collapse")
        require((x1_no_pivot, x2_no_pivot) == (Decimal(0), Decimal(1)), "unpivoted output changed")

        pivot_multiplier = eps4
        pivot_u22 = Decimal(1) - pivot_multiplier
        pivot_rhs2 = Decimal(1) - Decimal(2) * pivot_multiplier
        x2_pivot = pivot_rhs2 / pivot_u22
        x1_pivot = Decimal(2) - x2_pivot
        require((x1_pivot, x2_pivot) == (Decimal(1), Decimal(1)), "pivoted output changed")

    no_pivot = (Fraction(0), Fraction(1))
    pivoted = (Fraction(1), Fraction(1))
    no_pivot_error = max(abs(a - b) for a, b in zip(x_star, no_pivot)) / max(
        abs(value) for value in x_star
    )
    pivot_error = max(abs(a - b) for a, b in zip(x_star, pivoted)) / max(
        abs(value) for value in x_star
    )
    require(no_pivot_error == 1, "unpivoted relative forward error changed")
    require(pivot_error == eps, "pivoted relative forward error changed")

    pivot_residual = (-eps, Fraction(0))
    pivot_berr = abs(pivot_residual[0]) / (2 + eps)
    require(pivot_berr == eps / (2 + eps), "pivoted BERR changed")
    print(
        "PASS direct model: sum 1 -> left 0 / reordered+Neumaier 1; "
        "kappa_inf≈4, multiplier 1e8 -> 1e-8, forward 1 -> 1e-8"
    )


def audit_exact_refinement_model() -> None:
    q = Fraction(1, 4)
    relative_errors = [q ** (index + 1) for index in range(4)]
    iterate_ratios = [1 - error for error in relative_errors]
    require(
        relative_errors == [Fraction(1, 4), Fraction(1, 16), Fraction(1, 64), Fraction(1, 256)],
        "refinement error sequence changed",
    )
    require(
        iterate_ratios == [Fraction(3, 4), Fraction(15, 16), Fraction(63, 64), Fraction(255, 256)],
        "refinement iterate sequence changed",
    )
    initial_residual_ratio = q
    first_correction_ratio = (1 - q) * initial_residual_ratio
    require(first_correction_ratio == Fraction(3, 16), "first correction changed")
    require(q == 1 - (1 - q), "error-map scalar identity changed")
    print("PASS refinement model: exact error ratios 1/4, 1/16, 1/64, 1/256")


def audit_exact_qr_model() -> None:
    eps = 1e-8
    r = math.hypot(1.0, eps)
    c = 1.0 / r
    s = eps / r
    require(math.isclose(c * c + s * s, 1.0, rel_tol=0.0, abs_tol=2e-16), "Givens norm changed")

    a_tilde = ((1.0, 1.0), (eps, 1.0))
    givens = ((c, s), (-s, c))

    def matmul(first, second):
        return tuple(
            tuple(sum(first[i][k] * second[k][j] for k in range(2)) for j in range(2))
            for i in range(2)
        )

    r_factor = matmul(givens, a_tilde)
    require(abs(r_factor[1][0]) < 1e-24, "Givens failed to annihilate the lower entry")
    require(math.isclose(r_factor[0][0], r, rel_tol=0.0, abs_tol=2e-16), "R11 changed")
    require(
        math.isclose(r_factor[0][1], (1 + eps) / r, rel_tol=0.0, abs_tol=2e-16),
        "R12 changed",
    )
    require(
        math.isclose(r_factor[1][1], (1 - eps) / r, rel_tol=0.0, abs_tol=2e-16),
        "R22 changed",
    )
    require(
        math.isclose(r_factor[0][0] * r_factor[1][1], 1 - eps, rel_tol=0.0, abs_tol=2e-16),
        "QR determinant certificate changed",
    )

    safe_v = (1 + r, eps)
    safe_norm_squared = safe_v[0] ** 2 + safe_v[1] ** 2
    householder = (
        (1 - 2 * safe_v[0] ** 2 / safe_norm_squared, -2 * safe_v[0] * safe_v[1] / safe_norm_squared),
        (-2 * safe_v[1] * safe_v[0] / safe_norm_squared, 1 - 2 * safe_v[1] ** 2 / safe_norm_squared),
    )
    reflected = (
        householder[0][0] + householder[0][1] * eps,
        householder[1][0] + householder[1][1] * eps,
    )
    require(math.isclose(reflected[0], -r, rel_tol=0.0, abs_tol=3e-16), "safe reflector target changed")
    require(abs(reflected[1]) < 1e-23, "safe reflector failed to annihilate tail")

    with localcontext(decimal4_context()):
        toy_r = (Decimal(1) + Decimal("1e-16")).sqrt()
        bad_first = Decimal(1) - toy_r
        safe_first = Decimal(1) + toy_r
        require(toy_r == 1 and bad_first == 0, "unsafe Householder cancellation changed")
        require(safe_first == 2, "safe Householder leading component changed")
    print("PASS QR model: exact Givens R/determinant, safe Householder, unsafe sign cancels in F_{10,4}")


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


def matvec(matrix, vector):
    return tuple(sum(row[index] * vector[index] for index in range(len(vector))) for row in matrix)


def vector_norm(vector) -> float:
    return math.sqrt(sum(float(value) ** 2 for value in vector))


def audit_exact_spectral_model() -> None:
    q = tuple(
        tuple(Fraction(value, 3) for value in row)
        for row in ((1, 2, 2), (2, 1, -2), (-2, 2, -1))
    )
    identity = tuple(
        tuple(Fraction(int(row == column)) for column in range(3))
        for row in range(3)
    )
    require(matmul(transpose(q), q) == identity, "spectral Q is no longer orthogonal")

    sigma = (Fraction(1), Fraction(1, 2), Fraction(1, 4))
    lambdas = tuple(value**2 for value in sigma)
    a_top = tuple(
        tuple(sigma[row] * q[column][row] for column in range(3))
        for row in range(3)
    )
    a = a_top + ((Fraction(0), Fraction(0), Fraction(0)),)
    gram = matmul(transpose(a), a)
    spectral_gram = matmul(
        matmul(q, tuple(tuple(lambdas[row] if row == column else 0 for column in range(3)) for row in range(3))),
        transpose(q),
    )
    require(gram == spectral_gram, "A^T A spectral factorization changed")

    x_star = (Fraction(1), Fraction(-1), Fraction(2))
    fitted = matvec(a, x_star)
    b = fitted[:3] + (fitted[3] + 1,)
    residual = tuple(b[index] - fitted[index] for index in range(4))
    require(residual == (0, 0, 0, 1), "least-squares residual changed")
    require(matvec(transpose(a), residual) == (0, 0, 0), "least-squares stationarity changed")
    require(max(sigma) / min(sigma) == 4, "design condition number changed")
    require(max(lambdas) / min(lambdas) == 16, "normal-equation condition number changed")

    eigenvectors = tuple(tuple(q[row][column] for row in range(3)) for column in range(3))
    for eigenvalue, eigenvector in zip(lambdas, eigenvectors):
        require(
            matvec(gram, eigenvector) == tuple(eigenvalue * value for value in eigenvector),
            "Gram eigenpair changed",
        )

    # Power and shift-invert filters in exact spectral coordinates.
    require((lambdas[1] / lambdas[0]) ** 2 == Fraction(1, 16), "power second-mode ratio changed")
    require((lambdas[2] / lambdas[0]) ** 2 == Fraction(1, 256), "power third-mode ratio changed")
    shift = Fraction(5, 16)
    mapped = tuple(1 / (value - shift) for value in lambdas)
    require(mapped == (Fraction(16, 11), Fraction(-16), Fraction(-4)), "shift-invert map changed")

    tangent = Fraction(1, 3)
    cos_squared = 1 / (1 + tangent**2)
    sin_squared = tangent**2 / (1 + tangent**2)
    rho = lambdas[0] * cos_squared + lambdas[1] * sin_squared
    next_tangent = tangent * (lambdas[0] - rho) / (lambdas[1] - rho)
    require(next_tangent == -(tangent**3), "RQI cubic tangent identity changed")

    # The exact symmetric tridiagonal shared by Hessenberg and Lanczos.
    q_float = tuple(tuple(float(value) for value in row) for row in q)
    coefficient_basis = (
        (1 / math.sqrt(3), 3 / math.sqrt(14), 1 / math.sqrt(42)),
        (1 / math.sqrt(3), -1 / math.sqrt(14), -5 / math.sqrt(42)),
        (1 / math.sqrt(3), -2 / math.sqrt(14), 4 / math.sqrt(42)),
    )
    v = matmul(q_float, coefficient_basis)
    gram_float = tuple(tuple(float(value) for value in row) for row in gram)
    tridiagonal = matmul(matmul(transpose(v), gram_float), v)
    expected = (
        (7 / 16, math.sqrt(42) / 16, 0.0),
        (math.sqrt(42) / 16, 19 / 28, 5 * math.sqrt(3) / 56),
        (0.0, 5 * math.sqrt(3) / 56, 11 / 56),
    )
    for row in range(3):
        for column in range(3):
            require(
                math.isclose(tridiagonal[row][column], expected[row][column], rel_tol=0.0, abs_tol=4e-16),
                f"tridiagonal entry changed at {(row, column)}",
            )
    require(math.isclose(sum(tridiagonal[i][i] for i in range(3)), 21 / 16, abs_tol=3e-16), "T trace changed")

    # One exact-shift QR step on the invariant two-dimensional block.
    active = ((5 / 8, 3 / 8), (3 / 8, 5 / 8))
    z = ((1 / math.sqrt(2), -1 / math.sqrt(2)), (1 / math.sqrt(2), 1 / math.sqrt(2)))
    r_shift = ((3 * math.sqrt(2) / 8, 3 * math.sqrt(2) / 8), (0.0, 0.0))
    shifted = tuple(
        tuple(active[row][column] - (1 / 4 if row == column else 0) for column in range(2))
        for row in range(2)
    )
    reconstructed_shift = matmul(z, r_shift)
    shifted_next = matmul(r_shift, z)
    shifted_next = tuple(
        tuple(shifted_next[row][column] + (1 / 4 if row == column else 0) for column in range(2))
        for row in range(2)
    )
    for row in range(2):
        for column in range(2):
            require(math.isclose(reconstructed_shift[row][column], shifted[row][column], abs_tol=2e-16), "shifted QR factor changed")
    require(math.isclose(shifted_next[0][0], 1.0, abs_tol=2e-16), "shifted QR dominant value changed")
    require(math.isclose(shifted_next[1][1], 0.25, abs_tol=2e-16), "shifted QR deflated value changed")
    require(abs(shifted_next[1][0]) < 2e-16 and abs(shifted_next[0][1]) < 2e-16, "shifted QR did not deflate")

    # Two-step Ritz values and the inexpensive residual identity.
    alpha1 = expected[0][0]
    beta1 = expected[0][1]
    alpha2 = expected[1][1]
    beta2 = expected[1][2]
    trace2 = alpha1 + alpha2
    determinant2 = alpha1 * alpha2 - beta1**2
    discriminant2 = math.sqrt(trace2**2 - 4 * determinant2)
    theta_plus = (trace2 + discriminant2) / 2
    theta_minus = (trace2 - discriminant2) / 2
    require(math.isclose(theta_plus, (125 + math.sqrt(8961)) / 224, abs_tol=3e-16), "upper Ritz value changed")
    require(math.isclose(theta_minus, (125 - math.sqrt(8961)) / 224, abs_tol=3e-16), "lower Ritz value changed")

    y_raw = (beta1, theta_plus - alpha1)
    y_norm = vector_norm(y_raw)
    y = tuple(value / y_norm for value in y_raw)
    v2 = tuple(tuple(v[row][column] for column in range(2)) for row in range(3))
    ritz_vector = matvec(v2, y)
    direct_residual = tuple(
        value - theta_plus * ritz_vector[index]
        for index, value in enumerate(matvec(gram_float, ritz_vector))
    )
    cheap_residual = beta2 * abs(y[1])
    require(math.isclose(vector_norm(direct_residual), cheap_residual, abs_tol=4e-16), "Ritz residual identity changed")
    require(math.isclose(cheap_residual, 0.12397010250529546, abs_tol=4e-16), "upper Ritz residual changed")
    print(
        "PASS spectral model: kappa 4 -> 16, power/shift/RQI filters, exact T3, "
        "one-step shifted deflation and two-step Ritz residual"
    )


def audit_exact_iterative_model() -> None:
    """Check the shared nonnormal A -> SVD -> stationary -> preconditioned SPD chain."""

    def dot(first, second):
        return sum(first[index] * second[index] for index in range(len(first)))

    def close(first, second, *, atol=2e-14):
        return math.isclose(float(first), float(second), rel_tol=0.0, abs_tol=atol)

    a_exact = (
        (Fraction(1), Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(3)),
    )
    a = tuple(tuple(float(value) for value in row) for row in a_exact)
    gram_exact = matmul(transpose(a_exact), a_exact)
    expected_gram = (
        (Fraction(1), Fraction(2), Fraction(0)),
        (Fraction(2), Fraction(5), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(9)),
    )
    require(gram_exact == expected_gram, "iterative-wave Gram matrix changed")

    # NUM-13: two Arnoldi steps from q1=(1,1,1)/sqrt(3).
    q1 = tuple(1 / math.sqrt(3) for _ in range(3))
    aq1 = matvec(a, q1)
    h11 = dot(q1, aq1)
    w1 = tuple(aq1[index] - h11 * q1[index] for index in range(3))
    h21 = vector_norm(w1)
    q2 = tuple(value / h21 for value in w1)
    expected_q2 = (1 / math.sqrt(6), -2 / math.sqrt(6), 1 / math.sqrt(6))
    require(close(h11, Fraction(7, 3)), "Arnoldi h11 changed")
    require(close(h21, 2 * math.sqrt(2) / 3), "Arnoldi h21 changed")
    require(all(close(q2[index], expected_q2[index]) for index in range(3)), "Arnoldi q2 changed")

    aq2 = matvec(a, q2)
    h12 = dot(q1, aq2)
    after_q1 = tuple(aq2[index] - h12 * q1[index] for index in range(3))
    h22 = dot(q2, after_q1)
    w2 = tuple(after_q1[index] - h22 * q2[index] for index in range(3))
    h32 = vector_norm(w2)
    q3 = tuple(value / h32 for value in w2)
    expected_q3 = (-1 / math.sqrt(2), 0.0, 1 / math.sqrt(2))
    require(close(h12, -math.sqrt(2) / 3), "Arnoldi h12 changed")
    require(close(h22, Fraction(2, 3)), "Arnoldi h22 changed")
    require(close(h32, math.sqrt(3)), "Arnoldi h32 changed")
    require(all(close(q3[index], expected_q3[index]) for index in range(3)), "Arnoldi q3 changed")

    trace_h2 = h11 + h22
    determinant_h2 = h11 * h22 - h12 * h21
    require(close(trace_h2, 3), "Arnoldi H2 trace changed")
    require(close(determinant_h2, 2), "Arnoldi H2 determinant changed")
    require(close(h32 * (2 * math.sqrt(2) / 3), 2 * math.sqrt(6) / 3), "Ritz residual at theta=1 changed")
    require(close(h32 / math.sqrt(3), 1), "Ritz residual at theta=2 changed")

    q_matrix = tuple(tuple(column[row] for column in (q1, q2, q3)) for row in range(3))
    identity = matmul(transpose(q_matrix), q_matrix)
    require(
        all(close(identity[row][column], 1 if row == column else 0) for row in range(3) for column in range(3)),
        "Arnoldi Q3 lost orthogonality",
    )
    projected = matmul(matmul(transpose(q_matrix), a), q_matrix)
    expected_projected = (
        (7 / 3, -math.sqrt(2) / 3, math.sqrt(6) / 3),
        (2 * math.sqrt(2) / 3, 2 / 3, math.sqrt(3) / 3),
        (0.0, math.sqrt(3), 2.0),
    )
    require(
        all(close(projected[row][column], expected_projected[row][column]) for row in range(3) for column in range(3)),
        "full Arnoldi Hessenberg projection changed",
    )

    # NUM-14: exact singular triplets and alternating-power filter ratios.
    root_two = math.sqrt(2)
    singular_values = (3.0, 1 + root_two, root_two - 1)
    sine = math.sqrt(2 - root_two) / 2
    cosine = math.sqrt(2 + root_two) / 2
    right_vectors = ((0.0, 0.0, 1.0), (sine, cosine, 0.0), (-cosine, sine, 0.0))
    left_vectors = ((0.0, 0.0, 1.0), (cosine, sine, 0.0), (-sine, cosine, 0.0))
    for sigma, right, left in zip(singular_values, right_vectors, left_vectors):
        right_residual = tuple(matvec(a, right)[index] - sigma * left[index] for index in range(3))
        left_residual = tuple(matvec(transpose(a), left)[index] - sigma * right[index] for index in range(3))
        require(vector_norm(right_residual) < 2e-15, "right singular residual changed")
        require(vector_norm(left_residual) < 2e-15, "left singular residual changed")
    kappa_a = singular_values[0] / singular_values[-1]
    require(close(kappa_a, 3 * (1 + root_two)), "nonnormal A condition number changed")
    power_ratio = singular_values[1] ** 2 / singular_values[0] ** 2
    weak_ratio = singular_values[2] ** 2 / singular_values[0] ** 2
    require(close(power_ratio, (3 + 2 * root_two) / 9), "alternating-power second-mode ratio changed")
    require(close(weak_ratio, (3 - 2 * root_two) / 9), "alternating-power weak-mode ratio changed")

    # NUM-15: rho(B)=1/2, while a Jordan-coupled initial error grows twice.
    half = Fraction(1, 2)
    b_iteration = tuple(
        tuple((Fraction(1) if row == column else Fraction(0)) - half * a_exact[row][column] for column in range(3))
        for row in range(3)
    )
    error = (Fraction(0), Fraction(1), Fraction(0))
    expected_errors = (
        (Fraction(-1), Fraction(1, 2), Fraction(0)),
        (Fraction(-1), Fraction(1, 4), Fraction(0)),
        (Fraction(-3, 4), Fraction(1, 8), Fraction(0)),
    )
    norms = []
    for expected_error in expected_errors:
        error = matvec(b_iteration, error)
        require(error == expected_error, "stationary transient sequence changed")
        norms.append(vector_norm(error))
    require(norms[0] > 1 and norms[1] > 1 and norms[2] < 1, "stationary transient-growth boundary changed")
    require(close((1 + root_two) / 2, math.sqrt((3 + 2 * root_two) / 4)), "stationary operator norm identity changed")

    x_star = (Fraction(1), Fraction(-1), Fraction(1))
    rhs = matvec(a_exact, x_star)
    normal_rhs = matvec(transpose(a_exact), rhs)
    require(rhs == (Fraction(-1), Fraction(-1), Fraction(3)), "shared linear-system rhs changed")
    require(normal_rhs == (Fraction(-1), Fraction(-3), Fraction(9)), "shared normal rhs changed")
    require(matvec(gram_exact, x_star) == normal_rhs, "shared SPD solve no longer closes")

    # NUM-16: symmetric Jacobi scaling and residual-polynomial edge case.
    kappa_gram = 27 + 18 * root_two
    require(close(kappa_gram, kappa_a**2, atol=5e-14), "Gram condition-square identity changed")
    root_five = math.sqrt(5)
    lambda_minus = 1 - 2 / root_five
    lambda_middle = 1.0
    lambda_plus = 1 + 2 / root_five
    kappa_scaled = lambda_plus / lambda_minus
    require(close(kappa_scaled, 9 + 4 * root_five), "Jacobi-scaled condition number changed")
    endpoint_polynomial_at_middle = (1 - lambda_middle / lambda_minus) * (1 - lambda_middle / lambda_plus)
    require(close(endpoint_polynomial_at_middle, -4), "endpoint-root polynomial no longer amplifies the middle mode by four")
    for eigenvalue in (lambda_minus, lambda_middle, lambda_plus):
        annihilator = (
            (1 - eigenvalue)
            * (1 - eigenvalue / lambda_minus)
            * (1 - eigenvalue / lambda_plus)
        )
        require(close(annihilator, 0), "three-root Krylov annihilator changed")

    print(
        "PASS iterative model: exact Arnoldi H2/H3, singular triplets, rho=1/2 transient, "
        "kappa 52.46 -> 17.94 and degree-three annihilation"
    )


def audit_exact_large_scale_model() -> None:
    """Check the final shared CG -> GMRES -> sparse -> randomized-range chain."""

    def dot(first, second):
        return sum(first[index] * second[index] for index in range(len(first)))

    def add(first, second):
        return tuple(first[index] + second[index] for index in range(len(first)))

    def subtract(first, second):
        return tuple(first[index] - second[index] for index in range(len(first)))

    def scale(coefficient, vector):
        return tuple(coefficient * value for value in vector)

    def close(first, second, *, atol=3e-14):
        return math.isclose(float(first), float(second), rel_tol=0.0, abs_tol=atol)

    a = (
        (Fraction(1), Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(3)),
    )
    gram = matmul(transpose(a), a)
    x_target = (Fraction(1), Fraction(-1), Fraction(0))
    system_rhs = matvec(a, x_target)
    gram_rhs = matvec(gram, x_target)
    require(system_rhs == (Fraction(-1), Fraction(-1), Fraction(0)), "final-wave GMRES rhs changed")
    require(gram_rhs == (Fraction(-1), Fraction(-3), Fraction(0)), "final-wave CG rhs changed")

    # NUM-17: exact two-step CG on the active two-dimensional invariant subspace.
    x = (Fraction(0), Fraction(0), Fraction(0))
    residual = gram_rhs
    direction = residual
    gram_direction = matvec(gram, direction)
    alpha0 = dot(residual, residual) / dot(direction, gram_direction)
    x1 = add(x, scale(alpha0, direction))
    residual1 = subtract(residual, scale(alpha0, gram_direction))
    beta1 = dot(residual1, residual1) / dot(residual, residual)
    direction1 = add(residual1, scale(beta1, direction))
    require(alpha0 == Fraction(5, 29), "CG alpha0 changed")
    require(x1 == (Fraction(-5, 29), Fraction(-15, 29), Fraction(0)), "CG x1 changed")
    require(residual1 == (Fraction(6, 29), Fraction(-2, 29), Fraction(0)), "CG r1 changed")
    require(beta1 == Fraction(4, 841), "CG beta1 changed")
    require(direction1 == (Fraction(170, 841), Fraction(-70, 841), Fraction(0)), "CG p1 changed")
    require(dot(residual, residual1) == 0, "CG residual orthogonality changed")
    require(dot(direction, matvec(gram, direction1)) == 0, "CG conjugacy changed")
    alpha1 = dot(residual1, residual1) / dot(direction1, matvec(gram, direction1))
    x2 = add(x1, scale(alpha1, direction1))
    residual2 = subtract(residual1, scale(alpha1, matvec(gram, direction1)))
    require(alpha1 == Fraction(29, 5), "CG alpha1 changed")
    require(x2 == x_target and residual2 == (Fraction(0),) * 3, "CG two-step closure changed")
    error0 = subtract(x, x_target)
    error1 = subtract(x1, x_target)
    energy0 = dot(error0, matvec(gram, error0))
    energy1 = dot(error1, matvec(gram, error1))
    require((energy0, energy1) == (Fraction(2), Fraction(8, 29)), "CG energy sequence changed")

    # NUM-18: two-step GMRES and the squared Jordan residual polynomial.
    root_two = math.sqrt(2)
    q1 = tuple(float(value) / root_two for value in system_rhs)
    aq1 = matvec(a, q1)
    h11 = dot(q1, aq1)
    arnoldi_residual = subtract(aq1, scale(h11, q1))
    h21 = vector_norm(arnoldi_residual)
    q2 = tuple(value / h21 for value in arnoldi_residual)
    require(close(h11, 2) and close(h21, 1), "GMRES first Arnoldi column changed")
    y1 = root_two * h11 / (h11**2 + h21**2)
    gmres_x1 = scale(y1, q1)
    gmres_r1 = subtract(tuple(float(value) for value in system_rhs), matvec(a, gmres_x1))
    require(all(close(gmres_x1[index], (-2 / 5, -2 / 5, 0)[index]) for index in range(3)), "GMRES x1 changed")
    require(all(close(gmres_r1[index], (1 / 5, -3 / 5, 0)[index]) for index in range(3)), "GMRES r1 changed")
    require(close(vector_norm(gmres_r1) ** 2, Fraction(2, 5)), "GMRES first residual norm changed")
    aq2 = matvec(a, q2)
    h12 = dot(q1, aq2)
    after_q1 = subtract(aq2, scale(h12, q1))
    h22 = dot(q2, after_q1)
    final_arnoldi_residual = subtract(after_q1, scale(h22, q2))
    require(close(h12, -1) and close(h22, 0), "GMRES second Hessenberg column changed")
    require(vector_norm(final_arnoldi_residual) < 2e-15, "GMRES happy breakdown changed")
    identity_minus_a = tuple(
        tuple((Fraction(1) if row == column else Fraction(0)) - a[row][column] for column in range(3))
        for row in range(3)
    )
    polynomial_residual = matvec(matmul(identity_minus_a, identity_minus_a), system_rhs)
    require(polynomial_residual == (Fraction(0),) * 3, "GMRES Jordan polynomial no longer annihilates r0")

    # NUM-19: exact CSR representation, SpMV, and metadata-aware byte counts.
    nonzeros = tuple(
        (row, column, a[row][column])
        for row in range(3)
        for column in range(3)
        if a[row][column] != 0
    )
    require(nonzeros == ((0, 0, Fraction(1)), (0, 1, Fraction(2)), (1, 1, Fraction(1)), (2, 2, Fraction(3))), "sparse COO changed")
    indptr = [0]
    indices = []
    data = []
    for row in range(3):
        for current_row, column, value in nonzeros:
            if current_row == row:
                indices.append(column)
                data.append(value)
        indptr.append(len(indices))
    require(indptr == [0, 2, 3, 4], "CSR indptr changed")
    require(indices == [0, 1, 1, 2] and data == [Fraction(1), Fraction(2), Fraction(1), Fraction(3)], "CSR payload changed")
    require(matvec(a, x_target) == system_rhs, "CSR SpMV teaching output changed")
    csr_bytes = (8 + 4) * len(data) + 4 * (3 + 1)
    dense_bytes = 8 * 3 * 3
    gram_nonzeros = sum(value != 0 for row in gram for value in row)
    gram_csr_bytes = (8 + 4) * gram_nonzeros + 4 * (3 + 1)
    require((csr_bytes, dense_bytes, gram_nonzeros, gram_csr_bytes) == (64, 72, 5, 76), "sparse byte model changed")

    # NUM-20: fixed Rademacher realization, exact complement, and oversampling split.
    omega0 = (
        (Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(-1)),
        (Fraction(1), Fraction(1)),
    )
    sample0 = matmul(a, omega0)
    expected_sample0 = (
        (Fraction(3), Fraction(-1)),
        (Fraction(1), Fraction(-1)),
        (Fraction(3), Fraction(3)),
    )
    require(sample0 == expected_sample0, "randomized range sample changed")
    normal = (3 / math.sqrt(46), -6 / math.sqrt(46), -1 / math.sqrt(46))
    require(all(close(dot(normal, tuple(float(value) for value in column)), 0) for column in transpose(sample0)), "range complement changed")
    transpose_action = matvec(transpose(tuple(tuple(float(value) for value in row) for row in a)), normal)
    range_error = vector_norm(transpose_action)
    require(close(range_error, 3 / math.sqrt(23)), "randomized range residual changed")
    optimal_rank2_error = math.sqrt(2) - 1
    require(range_error > optimal_rank2_error, "fixed p=0 sketch unexpectedly beats the optimal rank-2 bound")
    omega1 = (
        (Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(-1), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(-1)),
    )
    determinant_omega1 = (
        omega1[0][0] * (omega1[1][1] * omega1[2][2] - omega1[1][2] * omega1[2][1])
        - omega1[0][1] * (omega1[1][0] * omega1[2][2] - omega1[1][2] * omega1[2][0])
        + omega1[0][2] * (omega1[1][0] * omega1[2][1] - omega1[1][1] * omega1[2][0])
    )
    require(determinant_omega1 == 4, "oversampled Rademacher realization lost full rank")
    tail_ratio = 3 - 2 * math.sqrt(2)
    require(close(tail_ratio**3, 0.005050633883346584, atol=2e-16), "randomized power-step ratio changed")

    print(
        "PASS large-scale model: two-step CG/GMRES, CSR 64 vs dense 72 vs Gram CSR 76 bytes, "
        "range error 3/sqrt(23) and oversampled full capture"
    )


def audit_markdown_integrity() -> None:
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    image_pattern = re.compile(
        r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]",
        re.I,
    )

    for filename in CONCEPTS:
        path = NUM / filename
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
        require(active.count("$$") % 2 == 0, f"{filename}: unbalanced display math")

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
                missing_links.append(f"{filename} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{filename} -> {target}")

        images = [(index, image_pattern.search(line)) for index, line in enumerate(lines)]
        images = [(index, match) for index, match in images if match is not None]
        require(len(images) == 1, f"{filename}: expected one textbook figure, found {len(images)}")
        position, match = images[0]
        require(match is not None, "internal image parser failure")
        expected = EXPECTED_FIGURE_BY_CONCEPT[filename]
        require(Path(match.group(1)).name == expected, f"{filename}: unexpected figure")
        block = "\n".join(lines[position : min(len(lines), position + 45)])
        for marker in ("[!figure]", "怎样读图", "适用边界"):
            require(marker in block, f"{filename}: figure unit misses {marker}")

    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")
    print(
        f"PASS Markdown integrity: Wiki links={link_count}, display math balanced, "
        f"figures={len(CONCEPTS)}/{len(CONCEPTS)}"
    )


def audit_figures(run_figures: bool) -> None:
    if run_figures:
        for script in FIGURE_SCRIPTS:
            subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)
    for filename, expected_hash in FIGURE_HASHES.items():
        path = FIGURE_DIR / filename
        require(path.is_file(), f"missing figure: {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"figure hash changed: {filename} -> {digest}")
        root = ET.parse(path).getroot()
        require(root.tag.endswith("svg"), f"invalid SVG root: {filename}")
        require("viewBox" in root.attrib, f"SVG missing viewBox: {filename}")
    print(f"PASS deterministic figures: {len(FIGURE_HASHES)}/{len(FIGURE_HASHES)} hashes and SVG XML")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-figures", action="store_true")
    args = parser.parse_args()
    audit_contracts()
    audit_route()
    audit_exact_scalar_model()
    audit_exact_linear_model()
    audit_exact_direct_model()
    audit_exact_refinement_model()
    audit_exact_qr_model()
    audit_exact_spectral_model()
    audit_exact_iterative_model()
    audit_exact_large_scale_model()
    audit_markdown_integrity()
    audit_figures(args.run_figures)
    print("NUM-01—20 material regression: PASS; learning state: draft/not-attempted")


if __name__ == "__main__":
    main()
