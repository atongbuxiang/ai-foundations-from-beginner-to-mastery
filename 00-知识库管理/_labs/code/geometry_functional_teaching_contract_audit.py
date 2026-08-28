#!/usr/bin/env python3
"""Audit the migrated teaching contracts and exact models for GEO-01--04."""

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
FIGURE_SCRIPT = LABS / "code" / "plot_geometry_foundations_v2.py"
FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "geometry"

CONCEPTS = (
    "度量空间、拓扑与连续映射.md",
    "光滑流形、切空间与余切空间.md",
    "Riemann 几何、测地线与流形优化.md",
    "Lie 群、Lie 代数与对称性.md",
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
    CONCEPTS[0]: "fig-metric-topology-continuity-v2.svg",
    CONCEPTS[1]: "fig-smooth-manifold-tangent-cotangent-v2.svg",
    CONCEPTS[2]: "fig-riemannian-geodesic-optimization-v2.svg",
    CONCEPTS[3]: "fig-lie-group-algebra-equivariance-v2.svg",
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
        "下一教学施工点是 GEO-05—06",
    ):
        require(marker in content, f"MOC misses route marker: {marker}")
    require(
        re.search(r"\| A \| GEO-01—04 .*`regression-passed`", content) is not None,
        "MOC first-wave material status is not regression-passed",
    )
    print("PASS GEO route: three-wave map, migrated S1/SO2 chain and learning-state boundary")


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
        expected = (EXPECTED_FIGURE_BY_CONCEPT[filename],)
        require(actual == expected, f"{filename}: expected figures {expected}, found {actual}")
        for position, match in images:
            require(match is not None, "internal image parser failure")
            block = "\n".join(lines[position : min(len(lines), position + 45)])
            for marker in ("[!figure]", "怎样读图", "适用边界"):
                require(marker in block, f"{filename}: figure unit {Path(match.group(1)).name} misses {marker}")
            figure_count += 1
    print(f"PASS GEO Markdown integrity: Wiki links={link_count}; display math balanced; figure units={figure_count}")


def audit_figures(run_figures: bool) -> None:
    if run_figures:
        subprocess.run([sys.executable, str(FIGURE_SCRIPT)], cwd=ROOT, check=True)
    for filename, expected_hash in FIGURE_HASHES.items():
        path = FIGURE_DIR / filename
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
    audit_markdown_integrity()
    audit_figures(args.run_figures)
    print("GEO-01—04 material regression: PASS; learning state: draft/not-attempted")


if __name__ == "__main__":
    main()
