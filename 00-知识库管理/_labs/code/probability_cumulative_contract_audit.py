#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for PROB-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROB = ROOT / "10-数学基础" / "10.5-概率论与数理统计"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = PROB / "概率论与数理统计 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 概率论与数理统计（10.5）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 概率论与数理统计（10.5）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 概率统计累计复现门.md"
CUM_SCRIPT = LABS / "code" / "plot_probability_cumulative_gate.py"
INFERENCE_SCRIPT = LABS / "code" / "plot_statistical_inference_v2.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "probability"
    / "plot-probability-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "69ebc90f4b09cc85829b3a642840f0a0dced9d71f7f6b76a755e66b204bea896"

CONCEPTS = (
    "样本空间、事件与概率公理.md",
    "条件概率、全概率与 Bayes 公式.md",
    "随机变量、分布与分位数.md",
    "联合分布、边缘分布与独立性.md",
    "期望、方差与矩.md",
    "协方差、相关性与条件期望.md",
    "常用离散分布.md",
    "常用连续分布与指数族.md",
    "多元高斯分布.md",
    "随机变量变换与密度换元.md",
    "随机变量的收敛与大数定律.md",
    "中心极限定理与 Delta 方法.md",
    "浓缩不等式.md",
    "Monte Carlo、重要性采样与方差缩减.md",
    "统计模型、估计量与偏差方差.md",
    "最大似然估计与 MAP.md",
    "Fisher 信息、Cramér–Rao 界与渐近正态性.md",
    "Bayesian 推断与后验预测.md",
    "假设检验、置信区间与多重比较.md",
    "MCMC 与随机模拟诊断.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "公式七问",
    "第一遍停靠线",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_lines(text: str) -> list[str]:
    """Drop fenced code while retaining ordinary Markdown and callouts."""
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
        text = read(PROB / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing contract markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
    print(f"PASS concept contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    for index in range(1, 21):
        require(f"PROB-{index:02d}" in assessment, f"assessment scope misses PROB-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")
    for marker in ("15 分钟卷级口试", "五波模型链", "三类不确定性"):
        require(marker in assessment, f"assessment misses oral-gate marker: {marker}")
    for marker in ("卷级口试参考要点", "五波模型链", "模型错设"):
        require(marker in solution, f"solution misses oral rubric marker: {marker}")
    print("PASS assessment bundle: scope 20/20, questions 14/14, oral gate present")


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)
    require(
        "| CUM | PROB-CUM | 卷级路线—口试—题解—实验—回归 | `regression-passed` |" in moc,
        "MOC cumulative material status is not regression-passed",
    )
    for marker in ("三遍学习", "五层证据", "卷级总图", "probability_cumulative_contract_audit.py"):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")
    for marker in (
        "进入实验前的解析校准门",
        "A. coverage",
        "B. rare-event importance sampling",
        "C. 双峰 MCMC",
    ):
        require(marker in experiment, f"experiment misses track marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(CUM_SCRIPT.is_file() and INFERENCE_SCRIPT.is_file(), "required compute scripts missing")
    print("PASS cumulative artifacts: route, evidence ladder, oral gate, analytic + A/B/C tracks")


def audit_markdown_integrity() -> None:
    scoped = [PROB / filename for filename in CONCEPTS] + [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
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
                    candidates = [path for path in candidates if path.suffix.lower() == suffix]
            if not candidates:
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")

    require(not math_findings, f"unbalanced display-math delimiters: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    figure_count = 0
    figure_findings: list[str] = []
    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    for path in [PROB / filename for filename in CONCEPTS] + [MOC]:
        lines = read(path).splitlines()
        positions = [index for index, line in enumerate(lines) if image_pattern.search(line)]
        for order, position in enumerate(positions):
            figure_count += 1
            stop = positions[order + 1] if order + 1 < len(positions) else min(len(lines), position + 45)
            block = "\n".join(lines[position : min(stop, position + 45)])
            missing = [marker for marker in ("[!figure]", "怎样读图", "适用边界") if marker not in block]
            if missing:
                figure_findings.append(f"{path.relative_to(ROOT)}:{position + 1} missing {missing}")
            match = image_pattern.search(lines[position])
            require(match is not None, "internal image parser failure")
            target = match.group(1)
            image_path = ROOT / target
            require(image_path.is_file(), f"missing embedded image: {target}")
            if image_path.suffix.lower() == ".svg":
                root_element = ET.parse(image_path).getroot()
                require(root_element.tag.endswith("svg"), f"invalid SVG root: {target}")
                require("viewBox" in root_element.attrib, f"SVG missing viewBox: {target}")
    require(not figure_findings, f"incomplete figure units: {figure_findings}")
    print(
        f"PASS Markdown integrity: Wiki links={link_count}, display math balanced; "
        f"figure units/SVG XML={figure_count}"
    )


def run(script: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def audit_compute() -> None:
    inference_output = run(INFERENCE_SCRIPT)
    require("PROB-17—20 inference gate:" in inference_output, "inference gate did not report its calibration")
    cumulative_output = run(CUM_SCRIPT)
    require(CUM_SVG.is_file(), "cumulative SVG was not generated")
    digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(digest == EXPECTED_CUM_SHA256, f"cumulative SVG hash changed: {digest}")
    print("PASS analytic inference calibration")
    print(f"PASS cumulative compute gate: sha256={digest}")
    if cumulative_output:
        print(cumulative_output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="also rerun the deterministic inference and full cumulative compute gates",
    )
    args = parser.parse_args()
    audit_concepts()
    audit_assessment_bundle()
    audit_cumulative_artifacts()
    audit_markdown_integrity()
    if args.run_compute:
        audit_compute()
    else:
        print("SKIP compute gates (pass --run-compute for the formal PROB-CUM audit)")
    print("PROB-CUM-01 material regression: PASS")


if __name__ == "__main__":
    main()
