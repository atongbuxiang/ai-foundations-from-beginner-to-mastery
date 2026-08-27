#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for INFO-CUM-01."""

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
EXPECTED_CUM_SHA256 = "7153136c90817de71c11e407106c268c2b193098fa192b1bf66c87f359c2f540"

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
    for index in range(1, 11):
        require(f"INFO-{index:02d}" in assessment, f"assessment scope misses INFO-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")
    for marker in ("15 分钟卷级口试", "三波模型链", "证据等级", "计算复现门"):
        require(marker in assessment, f"assessment misses oral/compute marker: {marker}")
    for marker in ("卷级口试参考要点", "三波模型链", "同值异义", "证据链"):
        require(marker in solution, f"solution misses oral rubric marker: {marker}")
    print("PASS assessment bundle: scope 10/10, questions 14/14, oral gate present")


def audit_analytic_calibration() -> None:
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

    eta = math.log(0.25 / 0.75)
    maxent_joint = (9.0 / 16.0, 3.0 / 16.0, 3.0 / 16.0, 1.0 / 16.0)
    close(eta, -math.log(3.0), "MaxEnt natural parameter")
    close(sum(maxent_joint), 1.0, "MaxEnt normalization")
    close(maxent_joint[1] + maxent_joint[3], 0.25, "MaxEnt first moment")
    close(maxent_joint[2] + maxent_joint[3], 0.25, "MaxEnt second moment")

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
        "| CUM | INFO-CUM | 卷级路线—口试—题解—实验—回归 | `regression-passed` |" in moc,
        "MOC cumulative material status is not regression-passed",
    )
    for marker in ("三遍学习", "五层证据", "卷级总图", "information_cumulative_contract_audit.py"):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")
    for marker in (
        "进入实验前的解析校准门",
        "A. Bernoulli–Hamming",
        "B. task bit",
        "C. prequential code",
    ):
        require(marker in experiment, f"experiment misses track marker: {marker}")
    for path in (MOC, ASSESSMENT, SOLUTION, EXPERIMENT):
        headings = [line.strip() for line in read(path).splitlines() if line.startswith("#")]
        duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
        require(not duplicates, f"{path.name}: duplicate headings {duplicates}")
    require(CUM_SCRIPT.is_file(), "cumulative compute script missing")
    print("PASS cumulative artifacts: route, evidence ladder, oral gate, analytic + A/B/C tracks")


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
    cumulative_output = run(CUM_SCRIPT)
    require("rd_D0.1=0.53100441" in cumulative_output, "rate-distortion calibration missing")
    require("saving_bits=108.59114 crossing=2" in cumulative_output, "prequential calibration changed")
    require(CUM_SVG.is_file(), "cumulative SVG was not generated")
    digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(digest == EXPECTED_CUM_SHA256, f"cumulative SVG hash changed: {digest}")
    print(f"PASS cumulative compute gate: sha256={digest}")
    print(cumulative_output)


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
    print("INFO-CUM-01 material regression: PASS")


if __name__ == "__main__":
    main()
