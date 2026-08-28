#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for PROB-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from fractions import Fraction
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
EXPECTED_INTERVENTION_SHA256 = "31402ed50a404dcd9444353f8d3a1155d928b34f968061b3c77b1f27a0064b75"

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    ROOT / "00-知识库管理" / "00-总览" / "数学基础十卷完备性审计与学习状态总表.md",
    ROOT / "00-知识库管理" / "_labs" / "exercises" / "练习与测验 MOC.md",
    ROOT / "00-知识库管理" / "_labs" / "推导与实验 MOC.md",
)

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
    experiment = read(EXPERIMENT)
    for path, text in ((ASSESSMENT, assessment), (SOLUTION, solution), (EXPERIMENT, experiment)):
        require("material_status: regression-passed" in text, f"{path.name}: material status drift")
        require("learning_status: not-attempted" in text, f"{path.name}: learning status drift")
        require("updated: 2026-08-28" in text, f"{path.name}: update date drift")
    for index in range(1, 21):
        require(f"PROB-{index:02d}" in assessment, f"assessment scope misses PROB-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")
    for marker in ("15 分钟卷级口试", "五波模型链", "三类不确定性"):
        require(marker in assessment, f"assessment misses oral-gate marker: {marker}")
    for marker in ("卷级口试参考要点", "五波模型链", "模型错设"):
        require(marker in solution, f"solution misses oral rubric marker: {marker}")
    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第 (\d+) 题：.*（(\d+) 分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第 (\d+) 题解答：.*（(\d+) 分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 15)), "assessment point headers are incomplete")
    require(sorted(solution_points) == list(range(1, 15)), "solution point headers are incomplete")
    require(question_points == solution_points, "question/solution point allocations differ")
    require(sum(question_points.values()) == 100, "assessment points do not total 100")
    require(not re.search(r"^### 第 \d+ 题解答", assessment, re.M), "solution headers leaked into assessment")
    for marker in (
        "答案隔离与防挑题协议",
        "attempt_id",
        "scorer nonce",
        "48 小时换机制重建门",
        "14 天陌生 AI 研究迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses evidence marker: {marker}")
    for marker in ("五波统一模型的卷级数值锚点", "口试与盲干预的判分红线", "最终状态边界"):
        require(marker in solution, f"solution misses evidence marker: {marker}")
    print("PASS assessment bundle: scope 20/20, questions/answers 14/14, points=100, isolation + delay gates")


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)
    require(
        "| CUM | PROB-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 盲干预 → 订正 → 48 h / 14 d → 独立审计 | `regression-passed / not-attempted` |" in moc,
        "MOC cumulative material status is not regression-passed",
    )
    for marker in ("三遍学习", "五层证据", "卷级总图", "probability_cumulative_contract_audit.py"):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")
    for marker in (
        "执行顺序、解析校准与随机指定",
        "A. coverage",
        "B. rare-event importance sampling",
        "C. 双峰 MCMC",
        "scorer nonce：不可挑轨",
        "盲参数干预门",
        "--coverage-p",
        "--tail-threshold",
        "--mode-location",
        "证据状态机与延迟迁移",
    ):
        require(marker in experiment, f"experiment misses track marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(CUM_SCRIPT.is_file() and INFERENCE_SCRIPT.is_file(), "required compute scripts missing")
    for path in STATE_SURFACES:
        state_text = read(path)
        require("probability_cumulative_contract_audit.py" in state_text, f"state surface misses audit: {path.name}")
        require("regression-passed" in state_text, f"state surface misses material pass: {path.name}")
        require("not-attempted" in state_text, f"state surface misses personal boundary: {path.name}")
    print("PASS cumulative artifacts: oral/closed/nonce/blind/delay route + 6 synchronized state surfaces")


def audit_independent_models() -> None:
    """Recompute the five-wave anchors without importing the plotting code."""
    p_b, p_f = Fraction(1, 3), Fraction(2, 3)
    head_b, head_f = Fraction(3, 4), Fraction(1, 2)
    p_head = p_b * head_b + p_f * head_f
    p_both = p_b * head_b**2 + p_f * head_f**2
    require(p_head == Fraction(7, 12), "wave A marginal drift")
    require(p_b * head_b / p_head == Fraction(3, 7), "wave A one-head posterior drift")
    require(p_b * head_b**2 / p_both == Fraction(9, 17), "wave A two-head posterior drift")
    require(p_both == Fraction(17, 48) and p_both != p_head**2, "wave A dependence drift")

    beta_mean = Fraction(2, 4)
    beta_second = Fraction(2 * 3, 4 * 5)
    beta_var = beta_second - beta_mean**2
    require((beta_mean, beta_second, beta_var) == (Fraction(1, 2), Fraction(3, 10), Fraction(1, 20)), "wave B moments drift")
    beta_binomial = (1 - 2 * beta_mean + beta_second, 2 * (beta_mean - beta_second), beta_second)
    require(beta_binomial == (Fraction(3, 10), Fraction(2, 5), Fraction(3, 10)), "wave B predictive drift")
    require(beta_second - beta_mean**2 == Fraction(1, 20), "wave B covariance drift")

    marginal_var, covariance = Fraction(1, 4), Fraction(1, 20)
    eig_plus, eig_minus = marginal_var + covariance, marginal_var - covariance
    delta_variance = Fraction(1, 4) * (2 * marginal_var + 2 * covariance)
    require((eig_plus, eig_minus) == (Fraction(3, 10), Fraction(1, 5)), "wave C covariance geometry drift")
    require(delta_variance == Fraction(3, 20), "wave C Delta variance drift")

    q = Fraction(3, 10)
    direct_var = q * (1 - q)
    good_var = q**2 / Fraction(3, 4) - q**2
    bad_var = q**2 / Fraction(1, 20) - q**2
    require((direct_var, good_var, bad_var) == (Fraction(21, 100), Fraction(3, 100), Fraction(171, 100)), "wave D IS variance drift")
    require(2 * math.exp(-4) < 0.105, "wave D Hoeffding/Chebyshev ordering drift")

    fisher_total = Fraction(10, 1) / (q * (1 - q))
    crlb = 1 / fisher_total
    post_a, post_b = 5, 9
    post_mean = Fraction(post_a, post_a + post_b)
    post_var = Fraction(post_a * post_b, (post_a + post_b) ** 2 * (post_a + post_b + 1))
    predictive = (
        Fraction(post_b * (post_b + 1), 14 * 15),
        Fraction(2 * post_a * post_b, 14 * 15),
        Fraction(post_a * (post_a + 1), 14 * 15),
    )
    exact_p = Fraction(2 * sum(math.comb(10, k) for k in range(4)), 2**10)
    posterior_upper = Fraction(sum(math.comb(13, k) for k in range(5)), 2**13)
    require((fisher_total, crlb) == (Fraction(1000, 21), Fraction(21, 1000)), "wave E Fisher drift")
    require((post_mean, post_var) == (Fraction(5, 14), Fraction(3, 196)), "wave E posterior drift")
    require(predictive == (Fraction(3, 7), Fraction(3, 7), Fraction(1, 7)), "wave E predictive drift")
    require(exact_p == Fraction(11, 32), "wave E exact test drift")
    require(1 - posterior_upper == Fraction(7099, 8192), "wave E posterior event drift")
    require(Fraction(7, 10) ** 2 < Fraction(1, 2) < Fraction(4, 5) ** 2, "IS second-moment boundary drift")
    require(Fraction(1, 2) * (-6) + Fraction(1, 2) * 6 == 0, "symmetric-mixture mean drift")
    print("PASS independent five-wave models: exact Bayes/moments/Delta/IS/Fisher-posterior anchors")


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


def run(script: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    require(
        result.returncode == 0,
        f"compute failed ({script.name} {' '.join(args)}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
    )
    return result.stdout.strip()


def normalized_output(output: str) -> str:
    return "\n".join(line for line in output.splitlines() if not line.startswith("OUTPUT "))


def audit_compute() -> None:
    inference_output = run(INFERENCE_SCRIPT)
    require("PROB-17—20 inference gate:" in inference_output, "inference gate did not report its calibration")
    require(CUM_SVG.is_file(), "stored cumulative SVG is missing")
    stored_digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(stored_digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {stored_digest}")

    with tempfile.TemporaryDirectory(prefix="prob-cum-audit-") as temp_dir:
        temp = Path(temp_dir)
        canonical_a = temp / "canonical-a.svg"
        canonical_b = temp / "canonical-b.svg"
        output_a = run(CUM_SCRIPT, "--output", str(canonical_a))
        output_b = run(CUM_SCRIPT, "--output", str(canonical_b))
        require(normalized_output(output_a) == normalized_output(output_b), "canonical stdout is not deterministic")
        require(canonical_a.read_bytes() == canonical_b.read_bytes(), "canonical SVG double-run differs")
        canonical_digest = hashlib.sha256(canonical_a.read_bytes()).hexdigest()
        require(canonical_digest == EXPECTED_CUM_SHA256, f"canonical SVG hash changed: {canonical_digest}")
        ET.parse(canonical_a)

        intervention = temp / "intervention.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--coverage-p", "0.1",
            "--coverage-reps", "2500",
            "--tail-threshold", "3.5",
            "--narrow-sigma", "0.8",
            "--wide-sigma", "2.5",
            "--is-repeats", "30",
            "--is-draws", "15000",
            "--mode-location", "7",
            "--proposal-step", "1.2",
            "--warmup", "800",
            "--mcmc-draws", "3000",
            "--output", str(intervention),
        )
        intervention_digest = hashlib.sha256(intervention.read_bytes()).hexdigest()
        require(intervention_digest == EXPECTED_INTERVENTION_SHA256, f"intervention SVG hash changed: {intervention_digest}")
        for marker in (
            "A_CONFIG p=0.1 reps=2500",
            "  20 +0.001760 0.067127 0.8828",
            "B_CONFIG threshold=3.5 repeats=30 draws=15000 sigmas=0.8,1,2.5",
            "0.80 0.00000000 0.00023263 1.0000 0.8385 0.0010 30",
            "2.50 0.00023608 0.00000998 0.0429",
            "C_CONFIG mode=7 step=1.2 warmup=800 draws=3000",
            "all-left  1.0022 -7.0005",
            "dispersed 7.6342 +0.0205",
        ):
            require(marker in intervention_output, f"intervention output misses: {marker}")
        ET.parse(intervention)

    print("PASS analytic inference calibration")
    print(f"PASS canonical double-run + stored SVG: sha256={stored_digest}")
    print(f"PASS blind-interface intervention: sha256={EXPECTED_INTERVENTION_SHA256}")


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
    audit_independent_models()
    audit_markdown_integrity()
    if args.run_compute:
        audit_compute()
    else:
        print("SKIP compute gates (pass --run-compute for the formal PROB-CUM audit)")
    print("PROB-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
