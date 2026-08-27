#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for NLA-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NUM = ROOT / "10-数学基础" / "10.8-数值计算"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = NUM / "数值线性代数 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 数值计算与数值线性代数（10.8）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 数值计算与数值线性代数（10.8）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 数值线性代数累计复现门.md"
TEACHING_AUDIT = LABS / "code" / "numerical_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "plot_numerical_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "numerical-analysis"
    / "fig-numerical-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "895af1e191506d2ada074b104eea71820af2063bc5abc522e6dce17d9b506682"

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

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_lines(content: str) -> list[str]:
    """Drop fenced code while retaining prose, formulas, links and callouts."""
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


def audit_concepts() -> None:
    for filename in CONCEPTS:
        content = read(NUM / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in content]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in content, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in content, f"{filename}: migration date missing")
    print(f"PASS concept contracts: {len(CONCEPTS)}/{len(CONCEPTS)}; learning state remains draft")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)

    for index in range(1, 21):
        require(f"NUM-{index:02d}" in assessment, f"assessment scope misses NUM-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")

    for marker in ("15 分钟卷级口试", "五波模型链", "五种不能混写的量", "AI 数值研究合同"):
        require(marker in assessment, f"assessment misses oral-gate marker: {marker}")
    for marker in ("卷级口试参考要点", "五波模型链参考", "口试判分红线", "AI 数值研究合同参考"):
        require(marker in solution, f"solution misses oral-rubric marker: {marker}")

    # The question file may link to the solution, but it must not contain answer headings or oral rubrics.
    forbidden_in_questions = (
        "### 第 1 题解答：",
        "#### 14.1 算子与形状",
        "## 六、卷级口试参考要点",
        "口试判分红线与记录",
    )
    leaked = [marker for marker in forbidden_in_questions if marker in assessment]
    require(not leaked, f"question/solution separation failed; leaked markers: {leaked}")
    require('solution: "[[阶段测验解答 - 数值计算与数值线性代数（10.8）]]"' in assessment,
            "assessment frontmatter lost the explicit solution pointer")
    require("正式作答前" not in solution or "冻结" in solution,
            "solution use-order warning is incomplete")

    print("PASS assessment bundle: scope 20/20, questions 14/14, oral gate present, answer markers isolated")


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)

    require(
        "| CUM | NUM-CUM | 卷级路线—口试—题解—实验—回归 | 五波随机回链与 A/B/C 累计三轨 | `regression-passed` | `not-attempted` |"
        in moc,
        "MOC cumulative status row is not regression-passed / not-attempted",
    )
    for marker in (
        "怎样从零真正学完本卷",
        "三遍学习",
        "五层证据",
        "卷级总图",
        "口试—闭卷—实验组合门",
        "numerical_cumulative_contract_audit.py",
    ):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")

    for marker in (
        "进入实验前的解析校准门",
        "A 轨：有限精度—误差—稳定—停止",
        "B 轨：结构—投影—预条件—真 residual",
        "C 轨：稀疏成本—随机值域—独立证书",
        "随机指定轨道的复核协议",
        EXPECTED_CUM_SHA256,
    ):
        require(marker in experiment, f"experiment misses cumulative marker: {marker}")

    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(TEACHING_AUDIT.is_file() and CUM_SCRIPT.is_file(), "required audit/compute scripts missing")
    print("PASS cumulative artifacts: zero-entry route, oral/written gate, evidence ladder and A/B/C experiment")


def audit_markdown_integrity() -> None:
    scoped = [NUM / filename for filename in CONCEPTS] + [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
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

    require(not math_findings, f"unbalanced display-math delimiters: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    figure_count = 0
    figure_findings: list[str] = []
    for path in [NUM / filename for filename in CONCEPTS] + [MOC, EXPERIMENT]:
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
    require("NUM-01—20 material regression: PASS" in teaching_output,
            "chapter teaching audit did not reach its material PASS")

    first_output = run(CUM_SCRIPT)
    require("A reliability:" in first_output and "B solver:" in first_output and "C scale:" in first_output,
            "cumulative script did not report all three tracks")
    require(CUM_SVG.is_file(), "cumulative SVG was not generated")
    first_digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(first_digest == EXPECTED_CUM_SHA256, f"cumulative SVG hash changed: {first_digest}")

    second_output = run(CUM_SCRIPT)
    second_digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(first_output == second_output and first_digest == second_digest,
            "cumulative compute gate is not deterministic across two runs")
    root_element = ET.parse(CUM_SVG).getroot()
    require(root_element.tag.endswith("svg") and "viewBox" in root_element.attrib,
            "cumulative SVG failed XML/viewBox validation")

    print("PASS chapter compute dependency: NUM-01—20 teaching/figure regression")
    print(f"PASS cumulative compute gate: deterministic double-run; sha256={first_digest}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="rerun all 20 chapter figures and the deterministic NUM-CUM three-track gate",
    )
    args = parser.parse_args()

    audit_concepts()
    audit_assessment_bundle()
    audit_cumulative_artifacts()
    audit_markdown_integrity()
    if args.run_compute:
        audit_compute()
    else:
        digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest() if CUM_SVG.is_file() else "missing"
        require(digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {digest}")
        print("SKIP compute rerun (pass --run-compute for the formal NLA-CUM audit)")
    print("NLA-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
