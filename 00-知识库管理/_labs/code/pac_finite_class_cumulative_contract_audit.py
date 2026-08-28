#!/usr/bin/env python3
"""Independent material and reproducibility audit for PAC-CUM-01."""

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
CHAPTER = ROOT / "20-学习理论" / "20.2-PAC学习与有限假设类"
MOC = CHAPTER / "PAC 学习与有限假设类 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - PAC 学习与有限假设类（20.2）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - PAC 学习与有限假设类（20.2）.md"
EXPERIMENT = LABS / "experiments" / "实验 - PAC 学习与有限假设类累计复现门.md"
GATE_SCRIPT = LABS / "code" / "pac_finite_class_cumulative_gate.py"
CANONICAL_SVG = (
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-pac-finite-class-cumulative-gate-v2.svg"
)

CANONICAL_SHA256 = "7dda45017be1cf60331afeebc506c727be597c4d40b8ea4bebbcee7d0099ab80"
BLIND_SHA256 = "f5bdaabff75caafbd2ebfefe3505fc5ec003caa6fd9331236dd9d81c9c0b9536"

BLIND_ARGS = (
    "--bad-count", "17",
    "--bad-risk", "0.23",
    "--realizable-size", "19",
    "--risk-grid", "0.15,0.21,0.28,0.41",
    "--agnostic-size", "31",
    "--code-lengths", "2,2,3,3",
    "--occam-size", "70",
    "--testing-size", "33",
    "--gamma", "0.055",
    "--delta", "0.08",
)

EXPECTED_BLIND_LINES = (
    "TRACK A bad=17 survival=0.006971 exact_failure=0.112130 union=0.118515 exponential=0.215071 exact_m=21 sufficient_m=24",
    "TRACK B radius=0.272538 exact_uniform_failure=0.002593 expected_population=0.168544 expected_train=0.131799 selection_gap=0.036745 class_excess=0.018544 mass=1.000000000000",
    "TRACK C kraft=0.750000 radii=0.181367,0.181367,0.194538,0.194538 tv=0.476949 testing_error=0.261525 pinsker_lower=0.183408",
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
        require(result.returncode != 0, "gate unexpectedly accepted unsafe output contract")
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


def binomial_pmf(n: int, q: float, count: int) -> float:
    return math.comb(n, count) * q**count * (1 - q) ** (n - count)


def binomial_cdf(n: int, q: float, count: int) -> float:
    if count < 0:
        return 0.0
    if count >= n:
        return 1.0
    return sum(binomial_pmf(n, q, k) for k in range(count + 1))


def independent_agnostic_anchor(risks: tuple[float, ...], m: int, delta: float) -> tuple[float, ...]:
    radius = math.sqrt(math.log(2 * len(risks) / delta) / (2 * m))
    uniform_success = 1.0
    for risk in risks:
        uniform_success *= sum(
            binomial_pmf(m, risk, count)
            for count in range(m + 1)
            if abs(count / m - risk) <= radius + 1e-15
        )
    expected_population = expected_train = mass = 0.0
    for index, risk in enumerate(risks):
        for count in range(m + 1):
            probability = binomial_pmf(m, risk, count)
            for earlier in risks[:index]:
                probability *= 1 - binomial_cdf(m, earlier, count)
            for later in risks[index + 1 :]:
                probability *= 1 - binomial_cdf(m, later, count - 1)
            mass += probability
            expected_population += probability * risk
            expected_train += probability * count / m
    return radius, 1 - uniform_success, expected_population, expected_train, mass


def audit_node_bundle() -> None:
    files = sorted(path for path in CHAPTER.glob("*.md") if path != MOC)
    require(len(files) == 8, f"expected 8 LT-09--16 nodes, found {len(files)}")
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
        require("![[" in content, f"embedded figure contract missing: {path.name}")
    require(sorted(found) == list(range(9, 17)), f"scope changed: {sorted(found)}")
    moc = read(MOC)
    for node_id in range(9, 17):
        require(re.search(rf"^\| LT-{node_id:02d} \|", moc, re.M) is not None, f"MOC misses LT-{node_id:02d}")
    print("PASS LT-09--16 node bundle: 8/8 unique draft nodes, figures and MOC mappings")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        frontmatter = parse_frontmatter(content)
        require(frontmatter.get("status") == "draft", f"{label}: status must remain draft")
        require(frontmatter.get("material_status") == "regression-passed", f"{label}: material status changed")
        require(frontmatter.get("learning_status") == "not-attempted", f"{label}: personal status changed")
        require(frontmatter.get("assessment_id") == "PAC-CUM-01", f"{label}: assessment ID changed")
        require(frontmatter.get("updated") == "2026-08-28", f"{label}: date changed")

    require("time_limit_minutes: 210" in assessment, "assessment duration changed")
    for node_id in range(9, 17):
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
        "20 分钟卷级口试",
        "210 分钟闭卷",
        "三轨参数化模型族",
        "八层 PAC 证明账本",
        "答案与输出隔离协议",
        "scorer nonce",
        "48 小时与 14 天复测",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses cumulative marker: {marker}")
    for marker in (
        "卷级口试参考要点",
        "实验复现门的评分说明",
        "Nonce 与盲参数判分红线",
        "48 小时与 14 天复测说明",
        "从 `retained` 到逐节点证据",
        "最终状态边界",
    ):
        require(marker in solution, f"solution misses rubric marker: {marker}")
    require("第 1 题解答" not in assessment, "answer leaked into question sheet")
    require("才可打开本页或 canonical stdout" in solution, "solution isolation warning missing")
    print("PASS assessment bundle: scope=8/8, questions/solutions=14/14, points=100, isolation + delay gates")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "三轨统一对象合同",
        "轨道 A：可实现版本空间的生存证书",
        "轨道 B：不可知 ERM、双侧共同事件与选择偏差",
        "轨道 C：Occam 失败预算与 Le Cam 难分辨性",
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
    print("PASS experiment contract: analytic calibration, three tracks, blind fixture and evidence state machine")


def audit_analytic_anchors() -> None:
    survival = 0.82**28
    exact_failure = 1 - (1 - survival) ** 31
    require(abs(survival - 0.0038617830030521247) < 1e-15, "track A survival anchor changed")
    require(abs(exact_failure - 0.11303257933192612) < 1e-14, "track A exact failure changed")
    require(math.ceil(math.log(31 / 0.05) / 0.18) == 36, "track A sufficient m changed")

    radius, uniform_failure, expected_population, expected_train, mass = independent_agnostic_anchor(
        (0.18, 0.22, 0.29, 0.36), 40, 0.05
    )
    require(abs(radius - 0.25187233411080073) < 1e-14, "track B radius changed")
    require(abs(uniform_failure - 0.0017069197836533379) < 1e-14, "track B uniform event changed")
    require(abs(expected_population - 0.19729831883873342) < 1e-14, "track B selected risk changed")
    require(abs(expected_train - 0.15829838200021823) < 1e-14, "track B selected train risk changed")
    require(abs(mass - 1.0) < 1e-12, "track B selection probabilities do not sum to one")

    lengths = (1, 2, 4, 4, 5)
    kraft = sum(2.0 ** (-length) for length in lengths)
    require(abs(kraft - 0.90625) < 1e-15, "track C Kraft sum changed")
    gamma, n = 0.04, 40
    p_minus, p_plus = 0.5 - gamma, 0.5 + gamma
    tv = 0.5 * sum(abs(binomial_pmf(n, p_minus, k) - binomial_pmf(n, p_plus, k)) for k in range(n + 1))
    require(abs(tv - 0.38547250790429427) < 1e-14, "track C exact TV changed")
    require(abs((1 - tv) / 2 - 0.3072637460478529) < 1e-14, "track C testing error changed")
    print("PASS analytic anchors: realizable survival, agnostic exact selection, Kraft and two-point testing")


def audit_svg(path: Path, expected_hash: str, required_text: tuple[str, ...]) -> None:
    require(path.is_file(), f"missing SVG: {path}")
    require(sha256(path) == expected_hash, f"SVG hash changed: {path.name}")
    root = ET.parse(path).getroot()
    require(root.tag.endswith("svg"), f"not an SVG root: {path.name}")
    require(root.attrib.get("viewBox") == "0 0 1440 680", f"SVG viewBox changed: {path.name}")
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
    require("exact_failure=0.113033" in first.stdout, "canonical track A anchor missing")
    require("class_excess=0.017298" in first.stdout, "canonical track B anchor missing")
    require("testing_error=0.307264" in first.stdout, "canonical track C anchor missing")
    audit_svg(
        CANONICAL_SVG,
        CANONICAL_SHA256,
        ("可实现：坏假设生存", "不可知：共同事件覆盖 ERM", "编码上界 × 测试下界"),
    )

    with tempfile.TemporaryDirectory() as temporary:
        first_path = Path(temporary) / "blind-first.svg"
        second_path = Path(temporary) / "blind-second.svg"
        first_blind = run(*BLIND_ARGS, "--output", str(first_path))
        second_blind = run(*BLIND_ARGS, "--output", str(second_path))
        require(first_path.read_bytes() == second_path.read_bytes(), "blind output is not byte deterministic")
        for line in EXPECTED_BLIND_LINES:
            require(line in first_blind.stdout and line in second_blind.stdout, f"blind stdout changed: {line}")
        audit_svg(first_path, BLIND_SHA256, ("|H|-1=17", "K=4, m=31", "Kraft=0.75000"))

    unsafe = run(*BLIND_ARGS, expect_success=False)
    require("require --output" in (unsafe.stdout + unsafe.stderr), "unsafe refusal message changed")
    require(CANONICAL_SVG.read_bytes() == stored_before, "noncanonical failure changed canonical asset")

    explicit_overwrite = run(*BLIND_ARGS, "--output", str(CANONICAL_SVG), expect_success=False)
    require("may not target" in (explicit_overwrite.stdout + explicit_overwrite.stderr),
            "explicit canonical overwrite was not rejected")
    require(CANONICAL_SVG.read_bytes() == stored_before, "explicit overwrite refusal changed canonical asset")

    invalid = run("--code-lengths", "1,1,1", "--output", str(ROOT / ".pac-invalid.svg"), expect_success=False)
    require("Kraft" in (invalid.stdout + invalid.stderr), "Kraft violation was not rejected")
    require(not (ROOT / ".pac-invalid.svg").exists(), "invalid input created an output")
    print("PASS deterministic compute: canonical + blind double-run, XML/hash and overwrite/Kraft protection")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require("PAC-CUM-01" in content, f"state surface misses volume ID: {path.relative_to(ROOT)}")
        require(audit_name in content, f"state surface misses audit link: {path.relative_to(ROOT)}")
        require("regression-passed" in content, f"state surface misses material state: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface misses personal state: {path.relative_to(ROOT)}")
    root_moc = read(ROOT / "20-学习理论" / "学习理论 MOC.md")
    curriculum = read(ROOT / "20-学习理论" / "学习理论完整课程地图与掌握标准.md")
    for content, label in ((root_moc, "root MOC"), (curriculum, "curriculum map")):
        require(re.search(r"5\s*/\s*10", content) is not None, f"{label}: volume-gate count not synchronized")
        require(re.search(r"0\s*/\s*10", content) is not None, f"{label}: personal volume count changed")
    print(f"PASS state surfaces: {len(STATE_SURFACES)} views preserve PAC-CUM-01 and agree on 5/10 material gates, 0/10 personal passes")


def main() -> None:
    audit_node_bundle()
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_analytic_anchors()
    audit_reproducibility()
    audit_state_surfaces()
    print("PAC-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
