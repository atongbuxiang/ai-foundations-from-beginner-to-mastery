#!/usr/bin/env python3
"""Independent material and reproducibility audit for VC-CUM-01."""

from __future__ import annotations

import hashlib
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LABS = ROOT / "00-知识库管理" / "_labs"
CHAPTER = ROOT / "20-学习理论" / "20.3-VC维与一致收敛"
MOC = CHAPTER / "VC 维与一致收敛 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - VC 维与一致收敛（20.3）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - VC 维与一致收敛（20.3）.md"
EXPERIMENT = LABS / "experiments" / "实验 - VC 维与一致收敛累计复现门.md"
GATE_SCRIPT = LABS / "code" / "vc_uniform_convergence_cumulative_gate.py"
CANONICAL_SVG = (
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-vc-uniform-convergence-cumulative-gate-v2.svg"
)

CANONICAL_SHA256 = "94a22793710901fde04a3e4e6ea89ad94e0954a2abba9041f4cf1819a76afd31"
BLIND_SHA256 = "16c35bb8c37c47fc401e6112809015cde6c721a2ac475d7522255a01658e64ad"

BLIND_ARGS = (
    "--max-size", "12",
    "--interval-runs", "3",
    "--domain-size", "5",
    "--uniform-size", "32",
    "--delta", "0.08",
    "--layer-dims", "1,3,6",
    "--layer-weights", "0.5,0.25,0.125",
    "--empirical-risks", "0.24,0.15,0.11",
    "--true-risks", "0.23,0.16,0.12",
    "--srm-size", "2500",
    "--multiclass-points", "4",
    "--label-count", "3",
)

EXPECTED_BLIND_LINES = (
    "TRACK A runs=3 vc=6 tau_d=64 tau_d1=127 tau_max=2510 sauer_max=2510",
    "TRACK B exact_radius=0.181250 exact_success=0.938561 dkw_radius=0.224265 finite_radius=0.279806 vc_radius_raw=1.421831 failure_at_finite=0.002331",
    "TRACK C selected=1 oracle_layer=1 penalties=0.212583,0.312687,0.409269 scores=0.452583,0.462687,0.519269 multiclass_functions=81 natarajan_patterns=16 graph_patterns=16 pseudo_patterns=4",
)

STATE_SURFACES = (
    MOC,
    ROOT / "20-学习理论" / "学习理论 MOC.md",
    ROOT / "20-学习理论" / "学习理论完整课程地图与掌握标准.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    LABS / "exercises" / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if expect_success:
        require(
            result.returncode == 0,
            f"gate failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    else:
        require(result.returncode != 0, "gate unexpectedly accepted an invalid contract")
    return result


def parse_frontmatter(content: str) -> dict[str, str]:
    require(content.startswith("---\n"), "document lacks YAML frontmatter")
    end = content.find("\n---\n", 4)
    require(end >= 0, "frontmatter is not closed")
    output: dict[str, str] = {}
    for line in content[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            output[key.strip()] = value.strip()
    return output


def independent_run_count(m: int, runs: int) -> int:
    return sum(math.comb(m + 1, 2 * k) for k in range(runs + 1) if 2 * k <= m + 1)


def independent_cdf_success(domain_size: int, sample_size: int, radius: float) -> float:
    inverse_factorials = tuple(1.0 / math.factorial(count) for count in range(sample_size + 1))
    states: dict[int, float] = {0: 1.0}
    for category in range(1, domain_size + 1):
        following: dict[int, float] = {}
        for allocated, weight in states.items():
            for count in range(sample_size - allocated + 1):
                total = allocated + count
                if category < domain_size and abs(total / sample_size - category / domain_size) > radius + 1e-14:
                    continue
                following[total] = following.get(total, 0.0) + weight * inverse_factorials[count]
        states = following
    return math.factorial(sample_size) * states.get(sample_size, 0.0) / domain_size**sample_size


def exact_radius(domain_size: int, sample_size: int, delta: float) -> tuple[float, float]:
    candidates = {0.0}
    for category in range(1, domain_size):
        for count in range(sample_size + 1):
            candidates.add(abs(count / sample_size - category / domain_size))
    for radius in sorted(candidates):
        success = independent_cdf_success(domain_size, sample_size, radius)
        if success >= 1 - delta - 1e-12:
            return radius, success
    raise AssertionError("no exact radius found")


def audit_node_bundle() -> None:
    files = sorted(path for path in CHAPTER.glob("*.md") if path != MOC)
    require(len(files) == 8, f"expected 8 LT-17--24 nodes, found {len(files)}")
    found: dict[int, Path] = {}
    for path in files:
        content = read(path)
        match = re.search(r"^node_id:\s*LT-(\d{2})\s*$", content, re.M)
        require(match is not None, f"node ID missing: {path.name}")
        node_id = int(match.group(1))
        require(node_id not in found, f"duplicate LT-{node_id:02d}")
        found[node_id] = path
        require("status: draft" in content, f"node state changed: {path.name}")
        require("exercises:" in content and "solutions:" in content, f"learning loop incomplete: {path.name}")
        require("![[" in content, f"embedded visual missing: {path.name}")
    require(sorted(found) == list(range(17, 25)), f"scope changed: {sorted(found)}")
    moc = read(MOC)
    for node_id in range(17, 25):
        require(re.search(rf"^\| LT-{node_id:02d} \|", moc, re.M) is not None, f"MOC misses LT-{node_id:02d}")
    print("PASS LT-17--24 node bundle: 8/8 unique draft nodes, visuals and MOC mappings")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        frontmatter = parse_frontmatter(content)
        require(frontmatter.get("status") == "draft", f"{label}: status must remain draft")
        require(frontmatter.get("material_status") == "regression-passed", f"{label}: material status changed")
        require(frontmatter.get("learning_status") == "not-attempted", f"{label}: personal status changed")
        require(frontmatter.get("assessment_id") == "VC-CUM-01", f"{label}: assessment ID changed")
        require(frontmatter.get("updated") == "2026-08-28", f"{label}: date changed")
    require("time_limit_minutes: 210" in assessment, "assessment duration changed")
    for node_id in range(17, 25):
        require(f"LT-{node_id:02d}" in assessment, f"assessment scope misses LT-{node_id:02d}")
    for question in range(1, 15):
        require(re.search(rf"^### 第\s*{question}\s*题：.*（(\d+)\s*分）$", assessment, re.M) is not None,
                f"question sheet misses question {question}")
        require(re.search(rf"^### 第\s*{question}\s*题解答：.*（(\d+)\s*分）$", solution, re.M) is not None,
                f"solution misses answer {question}")
    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题：.*（(\d+)\s*分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题解答：.*（(\d+)\s*分）$", solution, re.M)
    }
    require(question_points == solution_points, "question/solution points differ")
    require(sum(question_points.values()) == 100, "assessment does not total 100 points")
    for marker in (
        "20 分钟卷级口试", "210 分钟闭卷", "三轨参数化模型族", "八层 VC 证明账本",
        "答案与输出隔离协议", "scorer nonce", "48 小时与 14 天复测", "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses marker: {marker}")
    for marker in (
        "卷级口试参考要点", "实验复现门的评分说明", "Nonce 与盲参数判分红线",
        "48 小时与 14 天复测说明", "从 `retained` 到逐节点证据", "最终状态边界",
    ):
        require(marker in solution, f"solution misses marker: {marker}")
    require("第 1 题解答" not in assessment, "answer leaked into question sheet")
    require("才可打开本页或 canonical stdout" in solution, "solution isolation warning missing")
    print("PASS assessment bundle: scope=8/8, questions/solutions=14/14, points=100, isolation + delay gates")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "三轨统一对象合同",
        "轨道 A：从连续 1 段到 Sauer 极值类",
        "轨道 B：精确 uniform deviation 与通用证书",
        "轨道 C：SRM 与扩展见证的责任边界",
        "评分者随机指定、跨轨盲参与防挑题协议",
        "独立审计固定 fixture",
        "盲参数干预怎样才算独立",
        "证据状态机",
        CANONICAL_SHA256,
        BLIND_SHA256,
    ):
        require(marker in experiment, f"experiment contract misses: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicate = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicate, f"experiment duplicate headings: {duplicate}")
    print("PASS experiment contract: analytic calibration, three tracks, exact DP and evidence state machine")


def audit_analytic_anchors() -> None:
    require(independent_run_count(4, 2) == 16, "Track A tau(d) changed")
    require(independent_run_count(5, 2) == 31, "Track A tau(d+1) changed")
    require(independent_run_count(10, 2) == 386, "Track A maximum-class count changed")
    require(sum(math.comb(10, index) for index in range(5)) == 386, "Sauer sum changed")

    radius, success = exact_radius(6, 40, 0.05)
    require(abs(radius - 0.175) < 1e-15, "Track B exact radius changed")
    require(abs(success - 0.953254466758426) < 1e-14, "Track B exact success changed")
    dkw = math.sqrt(math.log(40) / 80)
    finite = math.sqrt(math.log(280) / 80)
    vc = math.sqrt(8 / 40 * (math.log(81) + math.log(80)))
    require(abs(dkw - 0.2147347041733688) < 1e-14, "DKW radius changed")
    require(abs(finite - 0.26539568579691647) < 1e-14, "finite-class radius changed")
    require(abs(vc - 1.3248755254246583) < 1e-14, "VC radius changed")

    dims = (1, 2, 4, 8)
    weights = (0.5, 0.25, 0.125, 0.0625)
    penalties = tuple(
        math.sqrt(8 / 3000 * (d * math.log(2 * math.e * 3000 / d) + math.log(4 / (0.05 * weight))))
        for d, weight in zip(dims, weights)
    )
    expected = (0.19849224040883154, 0.2518256334905524, 0.3254303805720047, 0.4261930736466952)
    require(all(abs(left - right) < 1e-14 for left, right in zip(penalties, expected)), "SRM penalties changed")
    scores = tuple(risk + penalty for risk, penalty in zip((0.26, 0.18, 0.115, 0.09), penalties))
    require(min(range(4), key=lambda index: scores[index]) == 1, "SRM selected layer changed")
    require(4**3 == 64 and 2**3 == 8, "multiclass witness counts changed")
    print("PASS analytic anchors: interval growth, exact CDF law, certificate radii, SRM and witnesses")


def audit_svg(path: Path, expected_hash: str, required_text: tuple[str, ...]) -> None:
    require(path.is_file(), f"missing SVG: {path}")
    require(sha256(path) == expected_hash, f"SVG hash changed: {path.name}")
    root = ET.parse(path).getroot()
    require(root.tag.endswith("svg"), f"not an SVG root: {path.name}")
    require(root.attrib.get("viewBox") == "0 0 1440 700", f"SVG viewBox changed: {path.name}")
    text_content = " ".join("".join(element.itertext()) for element in root.iter() if element.tag.endswith("text"))
    for marker in required_text:
        require(marker in text_content, f"SVG is not self-describing; misses {marker!r}")
    require(sum(1 for element in root.iter() if element.tag.endswith("text")) >= 55,
            f"SVG text density too low: {path.name}")


def audit_reproducibility() -> None:
    stored_before = CANONICAL_SVG.read_bytes()
    first = run()
    first_bytes = CANONICAL_SVG.read_bytes()
    second = run()
    second_bytes = CANONICAL_SVG.read_bytes()
    require(stored_before == first_bytes == second_bytes, "canonical output is not byte deterministic")
    require("tau_max=386" in first.stdout, "canonical Track A anchor missing")
    require("exact_radius=0.175000" in first.stdout, "canonical Track B anchor missing")
    require("selected=2 oracle_layer=1" in first.stdout, "canonical Track C anchor missing")
    audit_svg(
        CANONICAL_SVG,
        CANONICAL_SHA256,
        ("增长函数 × Sauer 包络", "阈值类的精确共同偏差", "SRM 选择 × 推广见证"),
    )

    with tempfile.TemporaryDirectory() as temporary:
        first_path = Path(temporary) / "blind-first.svg"
        second_path = Path(temporary) / "blind-second.svg"
        first_blind = run(*BLIND_ARGS, "--output", str(first_path))
        second_blind = run(*BLIND_ARGS, "--output", str(second_path))
        require(first_path.read_bytes() == second_path.read_bytes(), "blind output is not byte deterministic")
        for line in EXPECTED_BLIND_LINES:
            require(line in first_blind.stdout and line in second_blind.stdout, f"blind stdout changed: {line}")
        audit_svg(first_path, BLIND_SHA256, ("runs=3", "D=5, m=32", "|Y|^q=81"))

    unsafe = run(*BLIND_ARGS, expect_success=False)
    require("require --output" in (unsafe.stdout + unsafe.stderr), "unsafe refusal changed")
    explicit = run(*BLIND_ARGS, "--output", str(CANONICAL_SVG), expect_success=False)
    require("may not target" in (explicit.stdout + explicit.stderr), "explicit canonical overwrite was accepted")
    require(CANONICAL_SVG.read_bytes() == stored_before, "overwrite tests changed canonical asset")

    with tempfile.TemporaryDirectory() as temporary:
        invalid_path = Path(temporary) / "invalid.svg"
        invalid = run("--layer-weights", "0.7,0.4,0.1,0.1", "--output", str(invalid_path), expect_success=False)
        require("sum to at most one" in (invalid.stdout + invalid.stderr), "invalid SRM weights were not rejected")
        require(not invalid_path.exists(), "invalid input created output")
    print("PASS deterministic compute: canonical + blind double-run, XML/hash and overwrite/weight protection")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require("VC-CUM-01" in content, f"state surface misses volume ID: {path.relative_to(ROOT)}")
        require(audit_name in content, f"state surface misses audit link: {path.relative_to(ROOT)}")
        require("regression-passed" in content, f"state surface misses material state: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface misses learner state: {path.relative_to(ROOT)}")
    root_moc = read(ROOT / "20-学习理论" / "学习理论 MOC.md")
    curriculum = read(ROOT / "20-学习理论" / "学习理论完整课程地图与掌握标准.md")
    for content, label in ((root_moc, "root MOC"), (curriculum, "curriculum map")):
        require(re.search(r"3\s*/\s*10", content) is not None, f"{label}: volume-gate count not synchronized")
        require(re.search(r"0\s*/\s*10", content) is not None, f"{label}: personal count changed")
    print(f"PASS state surfaces: {len(STATE_SURFACES)} views agree on 3/10 material gates and 0/10 personal passes")


def main() -> None:
    audit_node_bundle()
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_analytic_anchors()
    audit_reproducibility()
    audit_state_surfaces()
    print("VC-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
