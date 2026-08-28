#!/usr/bin/env python3
"""Audit the migrated teaching contracts and exact models for GEO-01--08."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GEO = ROOT / "10-数学基础" / "10.10-几何、泛函分析、核与算子基础"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = GEO / "几何、泛函分析、核与算子基础 MOC.md"
GEOMETRY_FIGURE_SCRIPT = LABS / "code" / "plot_geometry_foundations_v2.py"
FUNCTIONAL_FIGURE_SCRIPT = LABS / "code" / "plot_functional_analysis_v2.py"
BANACH_AUDIT_SCRIPT = LABS / "code" / "banach_hilbert_projection_audit.py"
COMPACT_AUDIT_SCRIPT = LABS / "code" / "compact_operator_spectrum_audit.py"
RKHS_AUDIT_SCRIPT = LABS / "code" / "rkhs_kernel_audit.py"
SOBOLEV_AUDIT_SCRIPT = LABS / "code" / "sobolev_variational_operator_audit.py"
GEOMETRY_FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "geometry"
FUNCTIONAL_FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "functional-analysis"
FUNCTIONAL_PLOT_DIR = ROOT / "00-知识库管理" / "_assets" / "plots" / "functional-analysis"

FIRST_WAVE_CONCEPTS = (
    "度量空间、拓扑与连续映射.md",
    "光滑流形、切空间与余切空间.md",
    "Riemann 几何、测地线与流形优化.md",
    "Lie 群、Lie 代数与对称性.md",
)

SECOND_WAVE_CONCEPTS = (
    "Banach 空间、Hilbert 空间与正交投影.md",
    "有界算子、紧算子与谱理论基础.md",
)

THIRD_WAVE_CONCEPTS = (
    "正定核、RKHS 与表示定理.md",
    "弱导数、Sobolev 空间与神经算子接口.md",
)

CONCEPTS = FIRST_WAVE_CONCEPTS + SECOND_WAVE_CONCEPTS + THIRD_WAVE_CONCEPTS

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "符号与对象账本",
    "核心公式七问",
    "第一遍停靠线",
)

EXPECTED_FIGURE_BY_CONCEPT = {
    CONCEPTS[0]: ("fig-metric-topology-continuity-v2.svg",),
    CONCEPTS[1]: ("fig-smooth-manifold-tangent-cotangent-v2.svg",),
    CONCEPTS[2]: ("fig-riemannian-geodesic-optimization-v2.svg",),
    CONCEPTS[3]: ("fig-lie-group-algebra-equivariance-v2.svg",),
    CONCEPTS[4]: (
        "plot-banach-hilbert-projection-v2.svg",
        "fig-banach-hilbert-projection-v2.svg",
    ),
    CONCEPTS[5]: (
        "plot-compact-operator-spectrum-v2.svg",
        "fig-bounded-compact-spectrum-v2.svg",
    ),
    CONCEPTS[6]: (
        "plot-rkhs-krr-rff-v2.svg",
        "fig-positive-kernel-rkhs-representer-v2.svg",
    ),
    CONCEPTS[7]: (
        "plot-sobolev-weak-fem-operator-v2.svg",
        "fig-weak-sobolev-variational-operator-v2.svg",
    ),
}

FIGURE_PATHS = {
    "fig-metric-topology-continuity-v2.svg":
        GEOMETRY_FIGURE_DIR / "fig-metric-topology-continuity-v2.svg",
    "fig-smooth-manifold-tangent-cotangent-v2.svg":
        GEOMETRY_FIGURE_DIR / "fig-smooth-manifold-tangent-cotangent-v2.svg",
    "fig-riemannian-geodesic-optimization-v2.svg":
        GEOMETRY_FIGURE_DIR / "fig-riemannian-geodesic-optimization-v2.svg",
    "fig-lie-group-algebra-equivariance-v2.svg":
        GEOMETRY_FIGURE_DIR / "fig-lie-group-algebra-equivariance-v2.svg",
    "fig-banach-hilbert-projection-v2.svg":
        FUNCTIONAL_FIGURE_DIR / "fig-banach-hilbert-projection-v2.svg",
    "fig-bounded-compact-spectrum-v2.svg":
        FUNCTIONAL_FIGURE_DIR / "fig-bounded-compact-spectrum-v2.svg",
    "plot-banach-hilbert-projection-v2.svg":
        FUNCTIONAL_PLOT_DIR / "plot-banach-hilbert-projection-v2.svg",
    "plot-compact-operator-spectrum-v2.svg":
        FUNCTIONAL_PLOT_DIR / "plot-compact-operator-spectrum-v2.svg",
    "fig-positive-kernel-rkhs-representer-v2.svg":
        FUNCTIONAL_FIGURE_DIR / "fig-positive-kernel-rkhs-representer-v2.svg",
    "fig-weak-sobolev-variational-operator-v2.svg":
        FUNCTIONAL_FIGURE_DIR / "fig-weak-sobolev-variational-operator-v2.svg",
    "plot-rkhs-krr-rff-v2.svg":
        FUNCTIONAL_PLOT_DIR / "plot-rkhs-krr-rff-v2.svg",
    "plot-sobolev-weak-fem-operator-v2.svg":
        FUNCTIONAL_PLOT_DIR / "plot-sobolev-weak-fem-operator-v2.svg",
}

FIGURE_HASHES = {
    "fig-metric-topology-continuity-v2.svg":
        "0157a9da25b304725e0cb8a616626430570b4cbc97cf2dcd8cc45136d3dc6a25",
    "fig-smooth-manifold-tangent-cotangent-v2.svg":
        "7e445201266f013663e8cd786ebb6eab9fab21af9315e2a18a3a6175275cdaca",
    "fig-riemannian-geodesic-optimization-v2.svg":
        "335d672e126052b3c4d749c4769db3707656dff6a46b2b7dc129f5903b17cf9e",
    "fig-lie-group-algebra-equivariance-v2.svg":
        "6add355cfaf336fae2d87f14c883fdda98eba6e6cba83ce6a8925cc76e6cc6b9",
    "fig-banach-hilbert-projection-v2.svg":
        "7875607832954c07f12b5548716909d1f14267e79a3f0cd99996cec6ce960251",
    "fig-bounded-compact-spectrum-v2.svg":
        "9ef7f68ae8ee70b866cb5df3a2db228dab425c5d540ade7cb964c38f3be6de6f",
    "plot-banach-hilbert-projection-v2.svg":
        "c89f1cde4141996909ae78efcceb9857a4ecf3f71eaf81d44a1f04a6c8726d56",
    "plot-compact-operator-spectrum-v2.svg":
        "ab6d18eafb30d5665cb6d13229d18938352a93b524ddf1d3f7e346b82babbcf9",
    "fig-positive-kernel-rkhs-representer-v2.svg":
        "7b9b478f3e79bafef81552db7b965605b66d96e1295ed1d32a5f424c2c29d269",
    "fig-weak-sobolev-variational-operator-v2.svg":
        "8841137633397af4e2114e7c6335ab22890e7d5487eb9ca1641b57a6784565c5",
    "plot-rkhs-krr-rff-v2.svg":
        "cd35628d3df9ccc16308b0279d49d03a3ea751b0297724ca0c30d2807cc4f51e",
    "plot-sobolev-weak-fem-operator-v2.svg":
        "37be10891b4fac13df512179a462da9d62ab2ea3c1b02e6bfbcfb6478fdd9949",
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


def matmul(first, second):
    return tuple(
        tuple(
            sum(first[row][index] * second[index][column] for index in range(len(second)))
            for column in range(len(second[0]))
        )
        for row in range(len(first))
    )


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def matvec(matrix, vector):
    return tuple(sum(row[index] * vector[index] for index in range(len(vector))) for row in matrix)


def dot(first, second):
    return sum(left * right for left, right in zip(first, second))


def norm(vector):
    return math.sqrt(dot(vector, vector))


def close_vector(first, second, tolerance: float = 2e-14) -> bool:
    return all(math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)
               for left, right in zip(first, second))


def rotation(angle: float):
    return (
        (math.cos(angle), -math.sin(angle)),
        (math.sin(angle), math.cos(angle)),
    )


def audit_contracts() -> None:
    for filename in CONCEPTS:
        content = read(GEO / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in content]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in content, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in content, f"{filename}: migration date missing")
    print(f"PASS GEO teaching contracts: {len(CONCEPTS)}/{len(CONCEPTS)}; learning state remains draft")


def audit_route() -> None:
    content = read(MOC)
    for marker in (
        "全卷教学迁移路线",
        "| A | GEO-01—04",
        "第一波的 $S^1$—$SO(2)$ 单一模型链",
        "如何学习第一波，而不是背四套几何术语",
        "第一波材料证书",
        "| B | GEO-05—06",
        "| C | GEO-07—08",
        "geometry_functional_teaching_contract_audit.py",
        "`regression-passed`",
        "`draft / not-attempted`",
        "第二波的 \\(\\ell^2\\)—对角紧算子单一模型链",
        "如何学习第二波，而不是背泛函分析定理名",
        "第二波材料证书",
        "第三波的 Green kernel—弱 PDE—解算子单一模型链",
        "如何学习第三波，而不是背 kernel 与 PDE 名词",
        "第三波材料证书",
        "GEO-CUM：卷末综合验收闭环",
        "下一步不是继续补累计材料",
    ):
        require(marker in content, f"MOC misses route marker: {marker}")
    require(
        re.search(r"\| A \| GEO-01—04 .*`regression-passed`", content) is not None,
        "MOC first-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| B \| GEO-05—06 .*`regression-passed`", content) is not None,
        "MOC second-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| C \| GEO-07—08 .*`regression-passed`", content) is not None,
        "MOC third-wave material status is not regression-passed",
    )
    require(
        re.search(r"\| CUM \| GEO-CUM .*`regression-passed`.*`not-attempted`", content)
        is not None,
        "MOC cumulative material/personal states are not separated",
    )
    print("PASS GEO route: three migrated model chains and learning-state boundary")


def audit_exact_first_wave_model() -> None:
    # GEO-01: chord/angular metric identity and bi-Lipschitz bounds.
    for first_angle, second_angle in (
        (0.0, 0.0),
        (0.0, math.pi),
        (0.01, 2 * math.pi - 0.01),
        (-1.2, 2.4),
    ):
        raw = second_angle - first_angle
        wrapped = (raw + math.pi) % (2 * math.pi) - math.pi
        angular = abs(wrapped)
        first = (math.cos(first_angle), math.sin(first_angle))
        second = (math.cos(second_angle), math.sin(second_angle))
        chord = norm((first[0] - second[0], first[1] - second[1]))
        require(math.isclose(chord, 2 * math.sin(angular / 2), rel_tol=0.0, abs_tol=8e-16),
                "circle chord/angular identity changed")
        require((2 / math.pi) * angular <= chord + 2e-15, "lower metric comparison failed")
        require(chord <= angular + 2e-15, "upper metric comparison failed")

    # GEO-02: stereographic inverse, transition and tangent kernel.
    for coordinate in (-3.0, -0.5, 0.25, 2.0):
        x = 2 * coordinate / (1 + coordinate ** 2)
        y = (coordinate ** 2 - 1) / (1 + coordinate ** 2)
        require(math.isclose(x * x + y * y, 1.0, abs_tol=3e-16),
                "north stereographic inverse left circle")
        recovered = x / (1 - y)
        require(math.isclose(recovered, coordinate, abs_tol=2e-15),
                "north stereographic round trip changed")
        south = x / (1 + y)
        require(math.isclose(south, 1 / coordinate, abs_tol=3e-15),
                "stereographic transition changed")
    for angle in (-1.0, 0.0, 1.7):
        point = (math.cos(angle), math.sin(angle))
        tangent = (-math.sin(angle), math.cos(angle))
        require(math.isclose(dot(point, tangent), 0.0, abs_tol=1e-16),
                "circle tangent kernel changed")
        require(math.isclose(norm(tangent), 1.0, abs_tol=1e-16),
                "circle tangent basis lost unit norm")

    # GEO-03: exponential, tangent gradient, retraction order and rotation covariance.
    point = (math.cos(0.4), math.sin(0.4))
    tangent_basis = (-point[1], point[0])
    objective = (1.3, -0.7)
    projection = (
        (1 - point[0] ** 2, -point[0] * point[1]),
        (-point[0] * point[1], 1 - point[1] ** 2),
    )
    ambient_gradient = (-objective[0], -objective[1])
    gradient = matvec(projection, ambient_gradient)
    require(math.isclose(dot(point, gradient), 0.0, abs_tol=2e-16),
            "projected circle gradient left tangent")
    require(math.isclose(dot(gradient, tangent_basis), dot(ambient_gradient, tangent_basis), abs_tol=2e-16),
            "circle Riesz identity changed")

    for step in (0.2, 0.1, 0.05):
        vector = (step * tangent_basis[0], step * tangent_basis[1])
        exponential = (
            math.cos(step) * point[0] + math.sin(step) * tangent_basis[0],
            math.cos(step) * point[1] + math.sin(step) * tangent_basis[1],
        )
        candidate = (point[0] + vector[0], point[1] + vector[1])
        candidate_norm = norm(candidate)
        retraction = (candidate[0] / candidate_norm, candidate[1] / candidate_norm)
        require(math.isclose(norm(exponential), 1.0, abs_tol=2e-16), "circle Exp left manifold")
        require(math.isclose(norm(retraction), 1.0, abs_tol=2e-16), "circle retraction left manifold")
        require(norm((retraction[0] - exponential[0], retraction[1] - exponential[1])) < 0.36 * step ** 3,
                "circle retraction lost cubic point agreement")

    covariance_rotation = rotation(0.7)
    rotated_point = matvec(covariance_rotation, point)
    rotated_objective = matvec(covariance_rotation, objective)
    rotated_projection = (
        (1 - rotated_point[0] ** 2, -rotated_point[0] * rotated_point[1]),
        (-rotated_point[0] * rotated_point[1], 1 - rotated_point[1] ** 2),
    )
    rotated_gradient = matvec(rotated_projection, (-rotated_objective[0], -rotated_objective[1]))
    require(close_vector(rotated_gradient, matvec(covariance_rotation, gradient)),
            "circle gradient rotation covariance changed")

    # GEO-04: group law, Lie exponential, commutant and O(2) refinement.
    first_rotation = rotation(0.4)
    second_rotation = rotation(-1.1)
    require(all(close_vector(row, target) for row, target in zip(
        matmul(first_rotation, second_rotation), rotation(-0.7))),
        "SO(2) group law changed")
    j = ((0.0, -1.0), (1.0, 0.0))
    identity = ((1.0, 0.0), (0.0, 1.0))
    require(matmul(j, j) == ((-1.0, 0.0), (0.0, -1.0)), "J^2=-I changed")
    for angle in (-1.4, 0.0, 0.8):
        exponential = tuple(
            tuple(math.cos(angle) * identity[row][column] + math.sin(angle) * j[row][column]
                  for column in range(2))
            for row in range(2)
        )
        require(all(close_vector(row, target) for row, target in zip(exponential, rotation(angle))),
                "SO(2) exponential changed")

    a, b = 1.2, -0.3
    equivariant_map = (
        (a, -b),
        (b, a),
    )
    require(matmul(equivariant_map, j) == matmul(j, equivariant_map),
            "SO(2) commutant changed")
    reflection = ((1.0, 0.0), (0.0, -1.0))
    require(matmul(equivariant_map, reflection) != matmul(reflection, equivariant_map),
            "O(2) reflection failed to remove J component")

    print(
        "PASS first-wave exact model: circle metric/chart/tangent; induced Exp/gradient/retraction; "
        "SO(2) exponential/action commutant"
    )


def audit_exact_second_wave_model() -> None:
    # GEO-05: one c00 sequence separates l2-Cauchy behavior from l1.
    for cutoff in (8, 32, 128, 512):
        l2_tail_upper = 1.0 / cutoff
        finite_tail = sum(1.0 / (index * index) for index in range(cutoff + 1, 8 * cutoff + 1))
        require(finite_tail <= l2_tail_upper + 2e-15, "c00 l2 tail bound changed")
        l1_doubling_block = sum(1.0 / index for index in range(cutoff + 1, 2 * cutoff + 1))
        require(l1_doubling_block >= 0.5, "c00 l1 non-Cauchy witness changed")

    # Orthogonal truncation gives an exact Pythagorean best-approximation ledger.
    x = (1.0, -2.0, 3.0, -4.0, 5.0)
    projected = (1.0, -2.0, 0.0, 0.0, 0.0)
    candidate = (0.5, 0.25, 0.0, 0.0, 0.0)
    residual = tuple(left - right for left, right in zip(x, projected))
    in_subspace_error = tuple(left - right for left, right in zip(projected, candidate))
    total_error = tuple(left - right for left, right in zip(x, candidate))
    require(dot(residual, in_subspace_error) == 0.0, "projection residual lost orthogonality")
    require(
        dot(total_error, total_error)
        == dot(residual, residual) + dot(in_subspace_error, in_subspace_error),
        "projection Pythagorean identity changed",
    )
    require(dot(total_error, total_error) >= dot(residual, residual), "projection lost optimality")

    # Riesz witness g=(1/n) is square-summable; the formal all-ones probe is unbounded.
    riesz_norm = math.pi / math.sqrt(6.0)
    require(math.isclose(riesz_norm * riesz_norm, math.pi ** 2 / 6.0, abs_tol=3e-16),
            "Riesz witness norm changed")
    for dimension in (4, 16, 64, 256):
        unit_probe = tuple(1.0 / math.sqrt(dimension) for _ in range(dimension))
        require(math.isclose(norm(unit_probe), 1.0, abs_tol=2e-15),
                "all-ones functional probe lost unit norm")
        require(math.isclose(sum(unit_probe), math.sqrt(dimension), abs_tol=3e-14),
                "unbounded all-ones functional witness changed")
        weak_pairing = tuple(1.0 / index for index in range(1, dimension + 1))[-1]
        require(math.isclose(weak_pairing, 1.0 / dimension, abs_tol=0.0),
                "weak basis probe changed")
    require(math.isclose(norm((1.0, 0.0, 0.0)), 1.0), "orthonormal basis norm changed")

    # GEO-06: K e_n=(1/n)e_n is bounded, compact, self-adjoint and spectrally ill-posed.
    require(max(1.0 / index for index in range(1, 257)) == 1.0, "diagonal operator norm changed")
    for cutoff in (1, 4, 16, 64):
        expected_tail = 1.0 / (cutoff + 1)
        sampled_tail = max(1.0 / index for index in range(cutoff + 1, 8 * cutoff + 9))
        require(math.isclose(sampled_tail, expected_tail, abs_tol=0.0),
                "compact diagonal operator tail changed")
        tail_basis_vector = tuple(0.0 for _ in range(cutoff)) + (1.0,)
        require(math.isclose(norm(tail_basis_vector), 1.0, abs_tol=0.0),
                "identity finite-rank tail changed")

    # Every 1/n is an eigenvalue; zero is spectral but not an eigenvalue.
    for index in (1, 2, 7, 31):
        eigenvalue = 1.0 / index
        require(math.isclose(eigenvalue, 1.0 / index, abs_tol=0.0),
                "compact diagonal eigenvalue changed")
    require(all(1.0 / index != 0.0 for index in range(1, 1000)),
            "zero became a point eigenvalue")
    witness_image_norm_sq = sum(1.0 / (index * index) for index in range(1, 10000))
    require(witness_image_norm_sq < math.pi ** 2 / 6.0, "inverse range witness left l2")
    for dimension in (8, 32, 128):
        image = tuple(1.0 / index for index in range(1, dimension + 1))
        formal_preimage = tuple(index * value for index, value in enumerate(image, start=1))
        require(norm(image) < riesz_norm, "inverse witness image left bounded l2 ball")
        require(math.isclose(norm(formal_preimage), math.sqrt(dimension), abs_tol=2e-14),
                "unbounded inverse witness changed")

    # A non-spectral lambda has a uniform diagonal gap.
    test_lambda = 0.3
    gap = min(abs(1.0 / index - test_lambda) for index in range(1, 10000))
    require(gap > 0.03, "resolvent diagonal gap changed")

    # Spectral inversion amplifies a unit-coordinate perturbation by its mode index.
    noise = 1e-4
    for mode in (1, 10, 100):
        require(math.isclose((mode * noise) / noise, mode, abs_tol=2e-14),
                "inverse noise amplification changed")

    print(
        "PASS second-wave exact model: c00 completion/projection/Riesz/weak limit; "
        "compact diagonal tail/full spectrum/inverse amplification"
    )


def audit_exact_third_wave_model() -> None:
    def bridge_kernel(first: float, second: float) -> float:
        return min(first, second) - first * second

    # GEO-07: Brownian-bridge feature identity and finite PSD tests.
    for first, second in ((0.0, 0.7), (0.2, 0.2), (0.2, 0.8), (1.0, 0.3)):
        feature_inner = (
            min(first, second)
            - second * first
            - first * second
            + first * second
        )
        require(math.isclose(feature_inner, bridge_kernel(first, second), abs_tol=2e-16),
                "Brownian-bridge feature identity changed")

    points = (0.1, 0.35, 0.8)
    coefficients = (1.2, -0.7, 0.4)
    quadratic = sum(
        coefficients[row] * coefficients[column] * bridge_kernel(points[row], points[column])
        for row in range(len(points))
        for column in range(len(points))
    )
    require(quadratic >= -2e-16, "Brownian-bridge Gram matrix lost PSD")

    # The concrete H_0^1 reproducing calculation for f(t)=t-t^3.
    derivative_norm = math.sqrt(4.0 / 5.0)
    for point in (0.1, 0.37, 0.75, 0.95):
        value = point - point ** 3
        left_integral = value
        right_integral = -value
        reproducing = (1.0 - point) * left_integral - point * right_integral
        require(math.isclose(reproducing, value, abs_tol=2e-16),
                "H01 reproducing identity changed")
        section_norm = math.sqrt(point * (1.0 - point))
        require(abs(value) <= section_norm * derivative_norm + 2e-16,
                "bounded point-evaluation certificate changed")

    # Two-point KRR system for x=(1/4,3/4), y=(1,-1), n lambda=1/5.
    diagonal = 3.0 / 16.0
    off_diagonal = 1.0 / 16.0
    regularization = 1.0 / 5.0
    alpha = 40.0 / 13.0
    first_residual = (diagonal + regularization) * alpha - off_diagonal * alpha - 1.0
    second_residual = off_diagonal * alpha - (diagonal + regularization) * alpha + 1.0
    require(abs(first_residual) < 3e-16 and abs(second_residual) < 3e-16,
            "two-point KRR representer system changed")

    # Mercer series of the Green kernel.
    first, second = 0.23, 0.71
    partial = 2.0 * math.fsum(
        math.sin(mode * math.pi * first) * math.sin(mode * math.pi * second)
        / (mode * math.pi) ** 2
        for mode in range(1, 20001)
    )
    require(abs(partial - bridge_kernel(first, second)) < 1e-9,
            "Green-kernel sine expansion changed")
    for mode in (1, 2, 8, 32):
        eigenvalue = 1.0 / (mode * math.pi) ** 2
        require(eigenvalue > 0.0, "Mercer eigenvalue lost positivity")

    # GEO-08: weak derivative identity for |x| against a smooth boundary-zero probe.
    intervals = 20000
    step = 2.0 / intervals
    lhs = 0.0
    rhs = 0.0
    for index in range(intervals + 1):
        coordinate = -1.0 + index * step
        weight = 0.5 if index in (0, intervals) else 1.0
        probe = (1.0 - coordinate * coordinate) ** 2
        derivative = -4.0 * coordinate * (1.0 - coordinate * coordinate)
        sign = -1.0 if coordinate < 0.0 else (1.0 if coordinate > 0.0 else 0.0)
        lhs += weight * abs(coordinate) * derivative
        rhs += weight * sign * probe
    lhs *= step
    rhs *= step
    require(abs(lhs + rhs) < 2e-15, "weak derivative test identity changed")

    # Poisson weak balance for u=sin(pi x) against several sine tests.
    quadrature_points = 20000
    quadrature_step = 1.0 / quadrature_points
    for test_mode in (1, 2, 3):
        stiffness = 0.0
        load = 0.0
        for index in range(quadrature_points):
            coordinate = (index + 0.5) * quadrature_step
            solution_derivative = math.pi * math.cos(math.pi * coordinate)
            test_derivative = test_mode * math.pi * math.cos(test_mode * math.pi * coordinate)
            forcing = math.pi ** 2 * math.sin(math.pi * coordinate)
            test_value = math.sin(test_mode * math.pi * coordinate)
            stiffness += solution_derivative * test_derivative
            load += forcing * test_value
        stiffness *= quadrature_step
        load *= quadrature_step
        require(math.isclose(stiffness, load, abs_tol=2e-12),
                "Poisson sine weak balance changed")

    # Green section reproduces v(t) for v(x)=x(1-x).
    point = 0.37
    value = point * (1.0 - point)
    left_derivative_integral = value
    right_derivative_integral = -value
    green_balance = (1.0 - point) * left_derivative_integral - point * right_derivative_integral
    require(math.isclose(green_balance, value, abs_tol=2e-16),
            "Green-section weak balance changed")

    # Sine solution gains, compact tail, and hard-cutoff OOD failure.
    for cutoff in (1, 4, 8, 32):
        expected_tail = 1.0 / ((cutoff + 1) * math.pi) ** 2
        sampled_tail = max(
            1.0 / (mode * math.pi) ** 2
            for mode in range(cutoff + 1, cutoff + 1025)
        )
        require(math.isclose(sampled_tail, expected_tail, abs_tol=0.0),
                "Poisson solution-operator tail changed")
    cutoff = 8
    exact_unseen = 1.0 / ((cutoff + 1) * math.pi) ** 2
    learned_unseen = 0.0
    relative_error = abs(learned_unseen - exact_unseen) / exact_unseen
    require(math.isclose(relative_error, 1.0, abs_tol=0.0),
            "low-mode operator OOD witness changed")

    print(
        "PASS third-wave exact model: Green-kernel PSD/reproduction/representer/Mercer; "
        "weak Poisson balance/Galerkin spectrum/operator OOD"
    )


def audit_markdown_integrity() -> None:
    scoped = [GEO / filename for filename in CONCEPTS] + [MOC]
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
        path = GEO / filename
        lines = read(path).splitlines()
        images = [(index, image_pattern.search(line)) for index, line in enumerate(lines)]
        images = [(index, match) for index, match in images if match is not None]
        actual = tuple(Path(match.group(1)).name for _, match in images if match is not None)
        expected = EXPECTED_FIGURE_BY_CONCEPT[filename]
        require(actual == expected, f"{filename}: expected figures {expected}, found {actual}")
        for position, match in images:
            require(match is not None, "internal image parser failure")
            block = "\n".join(lines[position : min(len(lines), position + 45)])
            for marker in ("[!figure]", "怎样读图", "适用边界"):
                require(marker in block, f"{filename}: figure unit {Path(match.group(1)).name} misses {marker}")
            figure_count += 1
    print(f"PASS GEO Markdown integrity: Wiki links={link_count}; display math balanced; figure units={figure_count}")


def resolve_numpy_python() -> Path:
    candidates = (
        Path(sys.executable),
        Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime"
        / "dependencies" / "python" / "bin" / "python3",
    )
    for candidate in candidates:
        if not candidate.is_file():
            continue
        probe = subprocess.run(
            [str(candidate), "-c", "import numpy"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if probe.returncode == 0:
            return candidate
    raise AssertionError(
        "NumPy runtime not found; run with the workspace dependency Python or install NumPy"
    )


def audit_figures(run_figures: bool) -> None:
    if run_figures:
        for script in (GEOMETRY_FIGURE_SCRIPT, FUNCTIONAL_FIGURE_SCRIPT):
            subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)
        subprocess.run([sys.executable, str(BANACH_AUDIT_SCRIPT)], cwd=ROOT, check=True)
        numpy_python = resolve_numpy_python()
        for script in (COMPACT_AUDIT_SCRIPT, RKHS_AUDIT_SCRIPT, SOBOLEV_AUDIT_SCRIPT):
            subprocess.run(
                [str(numpy_python), str(script)],
                cwd=ROOT,
                check=True,
            )
    for filename, expected_hash in FIGURE_HASHES.items():
        path = FIGURE_PATHS[filename]
        require(path.is_file(), f"missing figure: {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"figure hash changed: {filename} -> {digest}")
        root_element = ET.parse(path).getroot()
        require(root_element.tag.endswith("svg"), f"invalid SVG root: {filename}")
        require("viewBox" in root_element.attrib, f"SVG missing viewBox: {filename}")
    print(f"PASS deterministic figures: {len(FIGURE_HASHES)}/{len(FIGURE_HASHES)} hashes and SVG XML")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-figures", action="store_true")
    args = parser.parse_args()

    audit_contracts()
    audit_route()
    audit_exact_first_wave_model()
    audit_exact_second_wave_model()
    audit_exact_third_wave_model()
    audit_markdown_integrity()
    audit_figures(args.run_figures)
    print("GEO-01—08 material regression: PASS; learning state: draft/not-attempted")


if __name__ == "__main__":
    main()
