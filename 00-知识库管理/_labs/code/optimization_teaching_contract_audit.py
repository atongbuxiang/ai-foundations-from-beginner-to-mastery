#!/usr/bin/env python3
"""Audit the OPT-01—04 teaching contract and its exact projection model."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OPT = ROOT / "10-数学基础" / "10.7-优化与凸分析"
LABS = ROOT / "00-知识库管理" / "_labs"
FIGURE_SCRIPT = LABS / "code" / "plot_convex_foundations_v2.py"

CONCEPTS = (
    "优化问题、可行域与局部最优.md",
    "凸集、凸组合与分离超平面.md",
    "凸函数、Jensen 不等式与上图集.md",
    "次梯度、共轭函数与 Fenchel 对偶.md",
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
    "fig-optimization-problem-solution-concepts-v2.svg":
        "01b11f6ac5f8adcdffad5a4a0a42bcb207d64143361c1864540a8c73870e689b",
    "fig-convex-sets-separation-v2.svg":
        "14c5dd54a595360f7132c5f945aee9bde48acce5189b7451c008b94c13d84e7c",
    "fig-convex-functions-jensen-epigraph-v2.svg":
        "e388c5488a2db17c96aa92826f66b463a32051d1d20852430c289617eca621c2",
    "fig-subgradient-conjugate-fenchel-v2.svg":
        "17dc468cd01e44c5b673b7606d774e8a3cba1646f082cac10aeb8a4ca95208fa",
}

FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "optimization"
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


def add(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]):
    return first[0] + second[0], first[1] + second[1]


def sub(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]):
    return first[0] - second[0], first[1] - second[1]


def scale(value: Fraction, vector: tuple[Fraction, Fraction]):
    return value * vector[0], value * vector[1]


def dot(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]) -> Fraction:
    return first[0] * second[0] + first[1] * second[1]


def squared_norm(vector: tuple[Fraction, Fraction]) -> Fraction:
    return dot(vector, vector)


def q(point: tuple[Fraction, Fraction], target: tuple[Fraction, Fraction]) -> Fraction:
    return Fraction(1, 2) * squared_norm(sub(point, target))


def audit_contracts() -> None:
    for filename in CONCEPTS:
        text = read(OPT / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in text, f"{filename}: migration date not recorded")
    print(f"PASS OPT teaching contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_exact_model() -> None:
    zero = (Fraction(0), Fraction(0))
    e1 = (Fraction(1), Fraction(0))
    e2 = (Fraction(0), Fraction(1))
    vertices = (zero, e1, e2)
    target = (Fraction(1), Fraction(1))
    optimizer = (Fraction(1, 2), Fraction(1, 2))
    residual = sub(target, optimizer)

    require(q(optimizer, target) == Fraction(1, 4), "primal optimum changed")
    require(residual == (Fraction(1, 2), Fraction(1, 2)), "projection residual changed")

    for vertex in vertices:
        require(
            dot(residual, sub(vertex, optimizer)) <= 0,
            f"projection variational inequality fails at vertex {vertex}",
        )
        require(q(vertex, target) >= q(optimizer, target), f"vertex beats optimizer: {vertex}")

    midpoint = scale(Fraction(1, 2), add(e1, e2))
    jensen_gap = (
        Fraction(1, 2) * q(e1, target)
        + Fraction(1, 2) * q(e2, target)
        - q(midpoint, target)
    )
    require(midpoint == optimizer, "Jensen midpoint no longer matches optimizer")
    require(jensen_gap == Fraction(1, 4), "exact Jensen gap changed")

    support_at_residual = max(dot(residual, vertex) for vertex in vertices)
    require(support_at_residual == Fraction(1, 2), "triangle support function changed")
    require(
        support_at_residual == dot(residual, optimizer),
        "indicator Fenchel-Young equality does not close",
    )

    negative_residual = scale(Fraction(-1), residual)
    q_star_negative_residual = dot(target, negative_residual) + Fraction(1, 2) * squared_norm(
        negative_residual
    )
    dual_value = -q_star_negative_residual - support_at_residual
    require(q_star_negative_residual == Fraction(-3, 4), "quadratic conjugate value changed")
    require(dual_value == Fraction(1, 4), "dual optimum certificate changed")
    require(dual_value == q(optimizer, target), "primal-dual gap is not zero")

    print(
        "PASS exact model: x*=(1/2,1/2), p*=1/4, projection VI, "
        "Jensen gap=1/4, Fenchel dual gap=0"
    )


def audit_markdown_integrity() -> None:
    scoped = [OPT / filename for filename in CONCEPTS]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    math_findings: list[str] = []
    for path in scoped:
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
        if active.count("$$") % 2:
            math_findings.append(str(path.relative_to(ROOT)))
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

    require(not math_findings, f"unbalanced display math: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    figure_count = 0
    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    for path in scoped:
        lines = read(path).splitlines()
        positions = [index for index, line in enumerate(lines) if image_pattern.search(line)]
        require(len(positions) == 1, f"{path.name}: expected exactly one teaching figure")
        for position in positions:
            figure_count += 1
            block = "\n".join(lines[position : min(len(lines), position + 45)])
            for marker in ("[!figure]", "怎样读图", "适用边界"):
                require(marker in block, f"{path.name}:{position + 1} misses figure marker {marker}")
            match = image_pattern.search(lines[position])
            require(match is not None, "internal image parser failure")
            image_path = ROOT / match.group(1)
            require(image_path.is_file(), f"missing embedded image: {match.group(1)}")
            if image_path.suffix.lower() == ".svg":
                root_element = ET.parse(image_path).getroot()
                require(root_element.tag.endswith("svg"), f"invalid SVG root: {match.group(1)}")
                require("viewBox" in root_element.attrib, f"SVG missing viewBox: {match.group(1)}")

    print(
        f"PASS scoped Markdown: Wiki links={link_count}, display math balanced, "
        f"figure units/SVG XML={figure_count}"
    )


def audit_figures() -> None:
    result = subprocess.run(
        [sys.executable, str(FIGURE_SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    for filename, expected in FIGURE_HASHES.items():
        path = FIGURE_DIR / filename
        require(path.is_file(), f"figure script did not generate {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"figure hash changed for {filename}: {digest}")
    print(f"PASS deterministic figures: {len(FIGURE_HASHES)}/{len(FIGURE_HASHES)} hashes stable")
    if result.stdout.strip():
        print(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-figures",
        action="store_true",
        help="regenerate the four OPT-01—04 SVGs and verify their SHA-256 hashes",
    )
    args = parser.parse_args()
    audit_contracts()
    audit_exact_model()
    audit_markdown_integrity()
    if args.run_figures:
        audit_figures()
    else:
        print("SKIP figure regeneration (pass --run-figures for the formal first-wave audit)")
    print("OPT-01—04 material regression: PASS")


if __name__ == "__main__":
    main()
