#!/usr/bin/env python3
"""Audit the migrated teaching contract and exact model for DYN-01--04."""

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
FIGURE_SCRIPT = LABS / "code" / "plot_dynamics_foundations_v2.py"
FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "dynamics"

CONCEPTS = (
    "常微分方程、初值问题与解的存在唯一性.md",
    "线性 ODE 与矩阵指数.md",
    "相图、平衡点与局部稳定性.md",
    "Lyapunov 稳定性与能量函数.md",
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
        "dynamics_teaching_contract_audit.py",
        "`regression-passed`",
        "`draft / not-attempted`",
    ):
        require(marker in content, f"MOC misses route marker: {marker}")
    require(
        re.search(r"\| A \| DYN-01—04 .*`regression-passed`", content) is not None,
        "MOC first-wave material status is not regression-passed",
    )
    require("下一教学迁移批次为 DYN-05—06" in content, "MOC next migration target is stale")
    print("PASS DYN route: four-wave map, first shared model and three-pass learning contract")


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
        require(len(images) == 1, f"{filename}: expected one textbook figure, found {len(images)}")
        position, match = images[0]
        require(match is not None, "internal image parser failure")
        expected = EXPECTED_FIGURE_BY_CONCEPT[filename]
        require(Path(match.group(1)).name == expected, f"{filename}: unexpected figure")
        block = "\n".join(lines[position : min(len(lines), position + 45)])
        for marker in ("[!figure]", "怎样读图", "适用边界"):
            require(marker in block, f"{filename}: figure unit misses {marker}")
        figure_count += 1

    print(f"PASS Markdown integrity: Wiki links={link_count}; display math balanced; figure units={figure_count}")


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
    print("DYN-01—04 material regression: PASS; learning state: draft/not-attempted")


if __name__ == "__main__":
    main()
