#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for INFO-CUM-01."""

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
INFO = ROOT / "10-数学基础" / "10.6-信息论与统计学习接口"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = INFO / "信息论与统计学习接口 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 信息论与统计学习接口（10.6）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 信息论与统计学习接口（10.6）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 信息论累计复现门.md"
CUM_SCRIPT = LABS / "code" / "plot_information_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "information-theory"
    / "plot-information-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "29fce27e85639837d2e8265f2f8fa9a3c6412680b39559a9e3c0f4db8fcdde47"
EXPECTED_INTERVENTION_SHA256 = "f0fe492a143fa7c6b7d59f1266332ca7b1061283afdbeb92407a45e6af829192"

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    ROOT / "00-知识库管理" / "00-总览" / "数学基础十卷完备性审计与学习状态总表.md",
    ROOT / "00-知识库管理" / "_labs" / "exercises" / "练习与测验 MOC.md",
    ROOT / "00-知识库管理" / "_labs" / "推导与实验 MOC.md",
)

CONCEPTS = (
    "自信息、熵与编码长度.md",
    "联合熵、条件熵与链式法则.md",
    "交叉熵与 KL 散度.md",
    "互信息与依赖性.md",
    "数据处理不等式与充分统计量.md",
    "无损编码、典型集与渐近等分性.md",
    "最大熵原理与指数族.md",
    "变分推断、ELBO 与证据分解.md",
    "f-散度、Bregman 散度与概率度量.md",
    "率失真、信息瓶颈与最小描述长度.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "符号与对象账本",
    "公式七问",
    "第一遍停靠线",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def close(actual: float, expected: float, label: str, tolerance: float = 5e-7) -> None:
    require(
        math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance),
        f"{label}: expected {expected:.9f}, got {actual:.9f}",
    )


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


def h2(probability: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -probability * math.log2(probability) - (1.0 - probability) * math.log2(
        1.0 - probability
    )


def bernoulli_kl(first: float, second: float) -> float:
    return first * math.log(first / second) + (1.0 - first) * math.log(
        (1.0 - first) / (1.0 - second)
    )


def audit_concepts() -> None:
    for filename in CONCEPTS:
        text = read(INFO / filename)
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
    for index in range(1, 11):
        require(f"INFO-{index:02d}" in assessment, f"assessment scope misses INFO-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")
    for marker in ("15 分钟卷级口试", "三波模型链", "证据等级", "计算复现门"):
        require(marker in assessment, f"assessment misses oral/compute marker: {marker}")
    for marker in ("卷级口试参考要点", "三波模型链", "同值异义", "证据链"):
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
        "答案隔离与防挑轨协议",
        "attempt_id",
        "scorer nonce",
        "48 小时换协议重建门",
        "14 天陌生 AI 信息目标迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses evidence marker: {marker}")
    for marker in ("三波统一模型的卷级数值锚点", "口试与盲干预的判分红线", "最终状态边界"):
        require(marker in solution, f"solution misses evidence marker: {marker}")
    print("PASS assessment bundle: scope 10/10, questions/answers 14/14, points=100, isolation + delay gates")


def audit_analytic_calibration() -> None:
    noisy_joint = (Fraction(3, 8), Fraction(1, 8), Fraction(1, 8), Fraction(3, 8))
    require(sum(noisy_joint, Fraction(0, 1)) == 1, "noisy-bit joint normalization drift")
    require(noisy_joint[0] + noisy_joint[3] == Fraction(3, 4), "noisy-bit match mass drift")
    quarter_entropy = h2(0.25)
    cascade_error = 0.25 * 0.75 + 0.75 * 0.25
    first_channel_information = 1.0 - quarter_entropy
    endpoint_information = 1.0 - h2(cascade_error)
    processing_loss = first_channel_information - endpoint_information

    close(quarter_entropy, 0.811278124, "h2(1/4)")
    close(cascade_error, 0.375, "BSC cascade error")
    close(first_channel_information, 0.188721876, "first BSC mutual information")
    close(endpoint_information, 0.045565998, "cascade endpoint mutual information")
    close(processing_loss, 0.143155878, "DPI processing loss")
    require(Fraction(1, 4) * Fraction(3, 4) * 2 == Fraction(3, 8), "BSC cascade fraction drift")

    eta = math.log(0.25 / 0.75)
    maxent_joint = (9.0 / 16.0, 3.0 / 16.0, 3.0 / 16.0, 1.0 / 16.0)
    close(eta, -math.log(3.0), "MaxEnt natural parameter")
    close(sum(maxent_joint), 1.0, "MaxEnt normalization")
    close(maxent_joint[1] + maxent_joint[3], 0.25, "MaxEnt first moment")
    close(maxent_joint[2] + maxent_joint[3], 0.25, "MaxEnt second moment")
    require(tuple(Fraction(round(value * 16), 16) for value in maxent_joint) == (
        Fraction(9, 16), Fraction(3, 16), Fraction(3, 16), Fraction(1, 16)
    ), "MaxEnt exact joint drift")

    prior_one = 0.25
    noise = 0.25
    evidence_one = (1.0 - prior_one) * noise + prior_one * (1.0 - noise)
    posterior_one = prior_one * (1.0 - noise) / evidence_one
    elbo_prior_q = (1.0 - prior_one) * math.log(noise) + prior_one * math.log(1.0 - noise)
    log_evidence = math.log(evidence_one)
    reverse_gap = bernoulli_kl(prior_one, posterior_one)
    forward_kl = bernoulli_kl(posterior_one, prior_one)

    close(evidence_one, 0.375, "latent evidence")
    close(posterior_one, 0.5, "latent posterior")
    close(log_evidence, -0.980829253, "log evidence")
    close(elbo_prior_q, -1.111641289, "ELBO with q=prior")
    close(log_evidence - elbo_prior_q, 0.130812036, "evidence-ELBO gap")
    close(reverse_gap, 0.130812036, "reverse KL gap")
    close(forward_kl, 0.143841036, "forward KL")
    close(abs(posterior_one - prior_one), 0.25, "Bernoulli TV and unit-cost W1")
    require(Fraction(3, 8) == Fraction(1, 4) * Fraction(3, 4) + Fraction(3, 4) * Fraction(1, 4), "latent evidence fraction drift")
    require(Fraction(1, 4) * Fraction(3, 4) / Fraction(3, 8) == Fraction(1, 2), "latent posterior fraction drift")

    biased_rd = quarter_entropy - h2(0.125)
    latent_information = h2(evidence_one) - h2(noise)
    naive_latent_code = h2(prior_one) + h2(noise)
    evidence_code = h2(evidence_one)
    mdl_gap = naive_latent_code - evidence_code

    close(biased_rd, 0.267713681, "biased Bernoulli R(1/8)")
    close(latent_information, 0.143155878, "latent mutual information")
    close(naive_latent_code, 1.622556249, "naive latent/evidence code")
    close(evidence_code, 0.954434003, "marginal evidence code")
    close(mdl_gap, 0.668122246, "MDL/bits-back gap")
    print(
        "PASS analytic calibration: noisy-bit/DPI, MaxEnt, evidence/ELBO, "
        "divergence, RD/IB/MDL"
    )


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)
    require(
        "| CUM | INFO-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 盲干预 → 订正 → 48 h / 14 d → 独立审计 | `regression-passed / not-attempted` |" in moc,
        "MOC cumulative material status is not regression-passed",
    )
    for marker in ("三遍学习", "五层证据", "卷级总图", "information_cumulative_contract_audit.py"):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "A. Bernoulli–Hamming",
        "B. task bit",
        "C. prequential code",
        "盲参数干预门",
        "--source-p",
        "--ib-noise",
        "--sequence-p",
        "证据状态机与延迟迁移",
    ):
        require(marker in experiment, f"experiment misses track marker: {marker}")
    for path in (MOC, ASSESSMENT, SOLUTION, EXPERIMENT):
        headings = [line.strip() for line in read(path).splitlines() if line.startswith("#")]
        duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
        require(not duplicates, f"{path.name}: duplicate headings {duplicates}")
    require(CUM_SCRIPT.is_file(), "cumulative compute script missing")
    for path in STATE_SURFACES:
        state_text = read(path)
        require("information_cumulative_contract_audit.py" in state_text, f"state surface misses audit: {path.name}")
        require("regression-passed" in state_text, f"state surface misses material pass: {path.name}")
        require("not-attempted" in state_text, f"state surface misses personal boundary: {path.name}")
    print("PASS cumulative artifacts: oral/closed/nonce/blind/delay route + 6 synchronized state surfaces")


def audit_markdown_integrity() -> None:
    scoped = [INFO / filename for filename in CONCEPTS] + [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
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

    figure_count = 0
    figure_findings: list[str] = []
    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    for path in [INFO / filename for filename in CONCEPTS] + [MOC, EXPERIMENT]:
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
    require(CUM_SVG.is_file(), "stored cumulative SVG is missing")
    stored_digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(stored_digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {stored_digest}")

    with tempfile.TemporaryDirectory(prefix="info-cum-audit-") as temp_dir:
        temp = Path(temp_dir)
        canonical_a = temp / "canonical-a.svg"
        canonical_b = temp / "canonical-b.svg"
        output_a = run(CUM_SCRIPT, "--output", str(canonical_a))
        output_b = run(CUM_SCRIPT, "--output", str(canonical_b))
        require(normalized_output(output_a) == normalized_output(output_b), "canonical stdout is not deterministic")
        require(canonical_a.read_bytes() == canonical_b.read_bytes(), "canonical SVG double-run differs")
        canonical_digest = hashlib.sha256(canonical_a.read_bytes()).hexdigest()
        require(canonical_digest == EXPECTED_CUM_SHA256, f"canonical SVG hash changed: {canonical_digest}")
        for marker in (
            "A_CONFIG source_p=0.5 probe_D=0.1 max_D=0.5",
            "A_RD probe_rate=0.53100441 source_entropy=1.00000000",
            "B_IB keep_x=0.00000000 keep_y=-1.00000000 noisy_y=-0.53100441",
            "C_CODE empirical_p=0.80250 fixed_bits=400.00000 kt_bits=291.40886 saving_bits=108.59114 crossing=2",
        ):
            require(marker in output_a, f"canonical output misses: {marker}")
        ET.parse(canonical_a)

        intervention = temp / "intervention.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--source-p", "0.3",
            "--rd-probe", "0.08",
            "--ib-noise", "0.2",
            "--nuisance-p", "0.2",
            "--ib-beta", "1.5",
            "--sequence-p", "0.65",
            "--sequence-length", "600",
            "--fixed-p", "0.5",
            "--kt-alpha", "1",
            "--output", str(intervention),
        )
        intervention_digest = hashlib.sha256(intervention.read_bytes()).hexdigest()
        require(intervention_digest == EXPECTED_INTERVENTION_SHA256, f"intervention SVG hash changed: {intervention_digest}")
        for marker in (
            "A_CONFIG source_p=0.3 probe_D=0.08 max_D=0.3",
            "A_RD probe_rate=0.47911171 source_entropy=0.88129090",
            "B_CONFIG noise=0.2 nuisance_p=0.2 beta=1.5",
            "B_IB keep_x=0.22192809 keep_y=-0.50000000 noisy_y=-0.13903595",
            "C_CONFIG true_p=0.65 length=600 fixed_p=0.5 kt_alpha=1",
            "C_CODE empirical_p=0.65833 fixed_bits=600.00000 kt_bits=560.20940 saving_bits=39.79060 crossing=2",
        ):
            require(marker in intervention_output, f"intervention output misses: {marker}")
        ET.parse(intervention)

    print(f"PASS canonical double-run + stored SVG: sha256={stored_digest}")
    print(f"PASS blind-interface intervention: sha256={EXPECTED_INTERVENTION_SHA256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="also rerun the deterministic INFO-CUM compute gate and verify its SVG hash",
    )
    args = parser.parse_args()
    audit_concepts()
    audit_assessment_bundle()
    audit_analytic_calibration()
    audit_cumulative_artifacts()
    audit_markdown_integrity()
    if args.run_compute:
        audit_compute()
    else:
        print("SKIP compute gate (pass --run-compute for the formal INFO-CUM audit)")
    print("INFO-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
