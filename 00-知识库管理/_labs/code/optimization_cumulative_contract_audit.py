#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for OPT-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OPT = ROOT / "10-数学基础" / "10.7-优化与凸分析"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = OPT / "优化与凸分析 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 优化与凸分析（10.7）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 优化与凸分析（10.7）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 优化与凸分析累计复现门.md"
TEACHING_AUDIT = LABS / "code" / "optimization_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "plot_optimization_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "optimization"
    / "plot-optimization-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "6df184dc5a75e125d1cf2f1595574007538cdd1321efa8690dcf14cf0e6230b6"

CONCEPTS = (
    "优化问题、可行域与局部最优.md",
    "凸集、凸组合与分离超平面.md",
    "凸函数、Jensen 不等式与上图集.md",
    "次梯度、共轭函数与 Fenchel 对偶.md",
    "光滑性、强凸性与条件数.md",
    "一阶最优性条件与梯度下降.md",
    "加速梯度、动量与下界.md",
    "随机梯度与小批量估计.md",
    "自适应优化方法.md",
    "Newton 法、Gauss-Newton 与拟 Newton 法.md",
    "投影、约束与可行方向.md",
    "Lagrange 乘子与 KKT 条件.md",
    "弱对偶、强对偶与 Slater 条件.md",
    "近端算子、复合优化与稀疏正则.md",
    "镜像下降、Bregman 几何与自然梯度.md",
    "非凸优化、鞍点与深度网络损失地形.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "核心公式七问",
    "第一遍停靠线",
)

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


def audit_concepts() -> None:
    for filename in CONCEPTS:
        text = read(OPT / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in text, f"{filename}: migration date missing")
    print(f"PASS concept contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    for index in range(1, 17):
        require(f"OPT-{index:02d}" in assessment, f"assessment scope misses OPT-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")
    for marker in ("15 分钟卷级口试", "四波模型链", "AI claim ladder"):
        require(marker in assessment, f"assessment misses oral-gate marker: {marker}")
    for marker in ("卷级口试参考要点", "四波模型链参考", "口试判分红线"):
        require(marker in solution, f"solution misses oral-rubric marker: {marker}")
    print("PASS assessment bundle: scope 16/16, questions 14/14, oral gate present")


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)
    require(
        "| CUM | OPT-CUM | 卷级路线—口试—题解—实验—回归 | `regression-passed` |"
        in moc,
        "MOC cumulative material status is not regression-passed",
    )
    for marker in (
        "怎样从零真正学完本卷",
        "三遍学习",
        "五层证据",
        "卷级总图",
        "optimization_cumulative_contract_audit.py",
    ):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")
    for marker in (
        "进入实验前的解析校准门",
        "A 轨：严格鞍点",
        "B 轨：非凸而满足 PL",
        "C 轨：尺度对称",
    ):
        require(marker in experiment, f"experiment misses track marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(TEACHING_AUDIT.is_file() and CUM_SCRIPT.is_file(), "required compute scripts missing")
    print("PASS cumulative artifacts: route, evidence ladder, oral gate, analytic + A/B/C tracks")


def audit_markdown_integrity() -> None:
    scoped = [OPT / filename for filename in CONCEPTS] + [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
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
                    candidates = [
                        candidate
                        for candidate in candidates
                        if candidate.suffix.lower() == suffix
                    ]
            if not candidates:
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")

    require(not math_findings, f"unbalanced display math: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    figure_count = 0
    figure_findings: list[str] = []
    image_pattern = re.compile(
        r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]",
        re.I,
    )
    for path in [OPT / filename for filename in CONCEPTS] + [MOC, EXPERIMENT]:
        lines = read(path).splitlines()
        positions = [index for index, line in enumerate(lines) if image_pattern.search(line)]
        for order, position in enumerate(positions):
            figure_count += 1
            stop = positions[order + 1] if order + 1 < len(positions) else min(
                len(lines), position + 45
            )
            block = "\n".join(lines[position : min(stop, position + 45)])
            missing = [
                marker
                for marker in ("[!figure]", "怎样读图", "适用边界")
                if marker not in block
            ]
            if missing:
                figure_findings.append(
                    f"{path.relative_to(ROOT)}:{position + 1} missing {missing}"
                )
            match = image_pattern.search(lines[position])
            require(match is not None, "internal image parser failure")
            image_path = ROOT / match.group(1)
            require(image_path.is_file(), f"missing embedded image: {match.group(1)}")
            if image_path.suffix.lower() == ".svg":
                root_element = ET.parse(image_path).getroot()
                require(root_element.tag.endswith("svg"), f"invalid SVG root: {match.group(1)}")
                require("viewBox" in root_element.attrib, f"SVG missing viewBox: {match.group(1)}")

    require(not figure_findings, f"incomplete figure units: {figure_findings}")
    print(
        f"PASS Markdown integrity: Wiki links={link_count}, display math balanced; "
        f"figure units/SVG XML={figure_count}"
    )


def run(script: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def audit_compute() -> None:
    teaching_output = run(TEACHING_AUDIT, "--run-figures")
    require(
        "OPT-01—16 material regression: PASS" in teaching_output,
        "chapter teaching audit did not pass",
    )
    cumulative_output = run(CUM_SCRIPT)
    require(CUM_SVG.is_file(), "cumulative SVG was not generated")
    digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(digest == EXPECTED_CUM_SHA256, f"cumulative SVG hash changed: {digest}")
    for marker in ("saddle exact_f=", "pl mu=", "sharpness balanced="):
        require(marker in cumulative_output, f"cumulative output misses calibration: {marker}")
    print("PASS four-wave analytic teaching calibration")
    print(f"PASS cumulative compute gate: sha256={digest}")
    if cumulative_output:
        print(cumulative_output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="also rerun all teaching figures and the deterministic cumulative compute gate",
    )
    args = parser.parse_args()
    audit_concepts()
    audit_assessment_bundle()
    audit_cumulative_artifacts()
    audit_markdown_integrity()
    if args.run_compute:
        audit_compute()
    else:
        print("SKIP compute gates (pass --run-compute for the formal OPT-CUM audit)")
    print("OPT-CUM-01 material regression: PASS")


if __name__ == "__main__":
    main()
