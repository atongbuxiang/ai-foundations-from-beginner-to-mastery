#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for ONLINE-CUM-01."""

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
CHAPTER = ROOT / "20-学习理论" / "20.9-在线学习、Boosting与序列预测"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = CHAPTER / "在线学习、Boosting 与序列预测 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 在线学习、Boosting 与序列预测（20.9）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 在线学习、Boosting 与序列预测（20.9）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 在线学习、Boosting 与序列预测累计复现门.md"
GATE = LABS / "code" / "online_boosting_cumulative_gate.py"
PREREQUISITE_AUDIT = LABS / "code" / "calibration_shift_cumulative_contract_audit.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-online-boosting-cumulative-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "2c61d35ce6dc1acedec1e6e62dea4ca62797ece325edc4787ca06eb055c45181"
EXPECTED_BLIND_SHA256 = "2f54d14536bf71f86c76a57011d33456c91173d5d808b6f97b8eb3d92ff24960"

CANONICAL_LINES = (
    "TRACK A T=4 eta=0.693147 hedge_loss=2.566667 best=2.000000 regret=0.566667 bound=1.931536 final_probs=0.400000,0.200000,0.400000 ogd_T=5 ogd_eta=0.500000 ogd_loss=2.500000 comparator=-1.000000 ogd_regret=3.500000 ogd_bound=3.750000 adaptive_T=6 adaptive_regret=3.000000",
    "TRACK B mistakes=2 final_w=1.000000,1.000000 R=1.414214 gamma=0.707107 mistake_bound=4.000000 progress=1.414214 norm=1.414214 boost_errors=0.250000,0.333333 alphas=0.549306,0.346574 Z=0.866025,0.942809 product=0.816497 training_error=0.250000 min_margin=-0.202733",
    "TRACK C T=4 random_risk=0.250000 comparator=0.100000 online_regret=0.600000 excess=0.150000 radius=0.611937 ucb=1.183198,1.324766 ucb_choice=2 ips=0.000000,0.000000,4.500000 target_risk=0.700000 observed_estimate=2.700000 ips_variance=1.019200 max_ratio=3.000000",
)

BLIND_ARGS = (
    "--hedge-losses", "0,1,0;1,0,1;1,1,0;0,0,1;1,0,0",
    "--hedge-eta", "1.0986122886681098",
    "--ogd-gradients", "2,-1,-1,2,-2,1", "--ogd-eta", "0.25",
    "--adaptive-actions", "1,1,2,2,1",
    "--perceptron-examples", "2,0,1;0,1,1;-1,-2,-1", "--separator", "1,1",
    "--boost-margins", "1,1,1,-1,-1;-1,-1,1,1,1",
    "--online-risks", "0.15,0.35,0.25,0.05,0.2", "--comparator-risk", "0.05", "--delta", "0.1",
    "--ucb-counts", "12,18", "--ucb-means", "0.55,0.48",
    "--logging-probabilities", "0.4,0.4,0.2",
    "--target-probabilities", "0.1,0.3,0.6",
    "--bandit-losses", "0.3,0.5,0.8", "--chosen-action", "2",
)

BLIND_LINES = (
    "TRACK A T=5 eta=1.098612 hedge_loss=2.790476 best=2.000000 regret=0.790476 bound=1.686633 final_probs=0.142857,0.428571,0.428571 ogd_T=6 ogd_eta=0.250000 ogd_loss=1.750000 comparator=-1.000000 ogd_regret=2.750000 ogd_bound=3.875000 adaptive_T=5 adaptive_regret=3.000000",
    "TRACK B mistakes=2 final_w=2.000000,1.000000 R=2.236068 gamma=0.707107 mistake_bound=10.000000 progress=2.121320 norm=2.236068 boost_errors=0.400000,0.333333 alphas=0.202733,0.346574 Z=0.979796,0.942809 product=0.923760 training_error=0.400000 min_margin=-0.143841",
    "TRACK C T=5 random_risk=0.200000 comparator=0.050000 online_regret=0.750000 excess=0.150000 radius=0.479853 ucb=1.302905,1.094745 ucb_choice=1 ips=0.000000,1.250000,0.000000 target_risk=0.660000 observed_estimate=0.375000 ips_variance=0.774900 max_ratio=3.000000",
)

EXPECTED_NODES = {
    69: "在线学习协议、Regret 与 Comparator",
    70: "Experts、Weighted Majority 与 Multiplicative Weights",
    71: "Online Gradient Descent 与 Mirror Descent",
    72: "随机、对抗与自适应序列的区别",
    73: "Perceptron Mistake Bound 与 Margin",
    74: "Boosting、弱学习与指数损失",
    75: "Online-to-Batch Conversion",
    76: "Bandit Feedback 与强化学习接口",
}

STATE_SURFACES = (
    MOC,
    ROOT / "20-学习理论" / "学习理论 MOC.md",
    ROOT / "20-学习理论" / "学习理论完整课程地图与掌握标准.md",
    LABS / "exercises" / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: tuple[str, ...] | list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GATE), *args], cwd=ROOT,
        text=True, capture_output=True, check=check,
    )


def lines(stdout: str) -> tuple[str, ...]:
    return tuple(line for line in stdout.splitlines() if line.startswith("TRACK "))


def audit_nodes() -> None:
    moc = read(MOC)
    for node_id, title in EXPECTED_NODES.items():
        path = CHAPTER / f"{title}.md"
        content = read(path)
        require(f"node_id: LT-{node_id}" in content, f"LT-{node_id}: node id mismatch")
        require("status: draft" in content, f"LT-{node_id}: draft boundary missing")
        require(f"# {title}" in content, f"LT-{node_id}: title mismatch")
        require(f"[[习题 - {title}]]" in content, f"LT-{node_id}: exercise link missing")
        require(f"[[解答 - {title}]]" in content, f"LT-{node_id}: solution link missing")
        require(f"| LT-{node_id} | [[{title}]]" in moc, f"LT-{node_id}: MOC row missing")
        exercise = LABS / "exercises" / f"习题 - {title}.md"
        solution = LABS / "solutions" / f"解答 - {title}.md"
        read(exercise)
        read(solution)
        figure_match = re.search(r'^figure:\s*"\[\[([^\]]+)\]\]"', content, re.M)
        require(figure_match is not None, f"LT-{node_id}: figure frontmatter missing")
        require((ROOT / figure_match.group(1)).is_file(), f"LT-{node_id}: figure asset missing")
    print("PASS LT-69--76 node bundle: 8/8 draft nodes, figures, exercises/solutions and MOC mappings")


def audit_assessment() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    require("assessment_id: ONLINE-CUM-01" in assessment, "assessment id missing")
    scope_match = re.search(r"^scope:\s*\[([^\]]+)\]", assessment, re.M)
    require(scope_match is not None, "scope frontmatter missing")
    scope = tuple(item.strip() for item in scope_match.group(1).split(","))
    require(scope == tuple(f"LT-{index}" for index in range(69, 77)), "assessment scope mismatch")
    questions = re.findall(r"^### 第 (\d+) 题", assessment, re.M)
    answers = re.findall(r"^## 第 (\d+) 题解答", solution, re.M)
    require(questions == [str(index) for index in range(1, 15)], "assessment is not 14 ordered questions")
    require(answers == [str(index) for index in range(1, 15)], "solution is not 14 ordered answers")
    points = [int(value) for value in re.findall(r"^### 第 \d+ 题[^\n]*（(\d+) 分）", assessment, re.M)]
    require(len(points) == 14 and sum(points) == 100, f"point contract mismatch: {points}")
    for marker in (
        "oral_limit_minutes: 25", "time_limit_minutes: 240", "REL-CUM-01-retained",
        "attempt_id", "scorer nonce", "blind", "48 小时", "14 天", "not-attempted",
    ):
        require(marker in assessment, f"assessment marker missing: {marker}")
    for marker in (
        "Canonical 回归输出", EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256,
        "past-measurability", "current-action-aware", "IPS", "not-attempted",
    ):
        require(marker in solution, f"solution marker missing: {marker}")
    for marker in (
        "八层可靠复现账本", "Canonical 复现", "Blind 干预", "输入与覆盖保护",
        "学习证据状态机", "48 小时", "14 天", "online_boosting_cumulative_gate.py",
    ):
        require(marker in experiment, f"experiment marker missing: {marker}")
    print("PASS ONLINE-CUM-01 assessment: scope=8/8, questions/solutions=14/14, points=100, oral/isolation/blind/delay gates")


def independent_math() -> None:
    # Hedge exact finite recursion.
    losses = ((0, 1, 1), (1, 0, 1), (0, 1, 0), (1, 1, 0))
    eta = math.log(2.0)
    cumulative = [0.0, 0.0, 0.0]
    algorithm_loss = 0.0
    for row in losses:
        weights = [math.exp(-eta * value) for value in cumulative]
        total = sum(weights)
        algorithm_loss += sum(weight * loss / total for weight, loss in zip(weights, row))
        cumulative = [old + value for old, value in zip(cumulative, row)]
    require(math.isclose(algorithm_loss, 77 / 30, abs_tol=1e-12), "Hedge loss mismatch")
    require(cumulative == [2.0, 3.0, 2.0], "expert ledger mismatch")
    require(math.isclose(algorithm_loss - min(cumulative), 17 / 30, abs_tol=1e-12), "Hedge regret mismatch")

    # Scalar OGD and current-action-aware counterexample.
    decision = 0.0
    ogd_loss = 0.0
    gradients = (1.0, -2.0, 1.0, 2.0, -1.0)
    for gradient in gradients:
        ogd_loss += gradient * decision
        decision = max(-1.0, min(1.0, decision - 0.5 * gradient))
    require(math.isclose(ogd_loss, 2.5, abs_tol=1e-12), "OGD loss mismatch")
    require(math.isclose(ogd_loss - (-1.0), 3.5, abs_tol=1e-12), "OGD regret mismatch")
    require(6 - min(3, 3) == 3, "adaptive counterexample mismatch")

    # Perceptron and AdaBoost are independently reconstructed.
    examples = ((1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (-1.0, -1.0, -1.0))
    weight = [0.0, 0.0]
    mistakes = 0
    for x1, x2, label in examples:
        if label * (weight[0] * x1 + weight[1] * x2) <= 0.0:
            weight = [weight[0] + label * x1, weight[1] + label * x2]
            mistakes += 1
    require(mistakes == 2 and weight == [1.0, 1.0], "Perceptron recursion mismatch")
    require(math.isclose((math.sqrt(2) / (1 / math.sqrt(2))) ** 2, 4.0, abs_tol=1e-12), "mistake bound mismatch")
    boost_rows = ((1, 1, 1, -1), (-1, -1, 1, 1))
    distribution = [0.25] * 4
    alphas: list[float] = []
    normalizers: list[float] = []
    for row in boost_rows:
        error = sum(value for value, signed in zip(distribution, row) if signed < 0)
        alpha = 0.5 * math.log((1 - error) / error)
        normalizer = 2 * math.sqrt(error * (1 - error))
        distribution = [value * math.exp(-alpha * signed) / normalizer for value, signed in zip(distribution, row)]
        alphas.append(alpha)
        normalizers.append(normalizer)
    margins = [sum(alphas[t] * boost_rows[t][i] for t in range(2)) for i in range(4)]
    require(math.isclose(math.prod(normalizers), math.sqrt(6) / 3, abs_tol=1e-12), "boost product mismatch")
    require(sum(value <= 0 for value in margins) == 1, "boost training error mismatch")

    # Risk conversion, UCB and scalar IPS variance.
    risks = (0.2, 0.4, 0.1, 0.3)
    require(math.isclose(sum(risks) / 4, 0.25, abs_tol=1e-12), "random iterate mismatch")
    require(math.isclose(sum(value - 0.1 for value in risks), 0.6, abs_tol=1e-12), "online regret mismatch")
    ucb = (0.6 + math.sqrt(2 * math.log(30) / 20), 0.5 + math.sqrt(2 * math.log(30) / 10))
    require(ucb[1] > ucb[0], "UCB choice mismatch")
    logging = (0.5, 0.3, 0.2)
    target = (0.2, 0.2, 0.6)
    bandit_losses = (0.2, 0.6, 0.9)
    risk = sum(pi * loss for pi, loss in zip(target, bandit_losses))
    variance = sum(pi * pi * loss * loss / p for pi, loss, p in zip(target, bandit_losses, logging)) - risk * risk
    require(math.isclose(risk, 0.7, abs_tol=1e-12), "target risk mismatch")
    require(math.isclose(variance, 1.0192, abs_tol=1e-12), "IPS variance mismatch")
    print("PASS independent math: Hedge/OGD/visibility + Perceptron/AdaBoost + online-to-batch/UCB/IPS anchors")


def audit_compute() -> None:
    before = digest(SVG)
    require(before == EXPECTED_CANONICAL_SHA256, "stored canonical SVG hash mismatch")
    first = run(())
    first_hash = digest(SVG)
    second = run(())
    second_hash = digest(SVG)
    require(lines(first.stdout) == CANONICAL_LINES == lines(second.stdout), "canonical stdout mismatch")
    require(first_hash == EXPECTED_CANONICAL_SHA256 == second_hash, "canonical double-run/hash mismatch")
    with tempfile.TemporaryDirectory(prefix="online-cum-blind-") as directory:
        first_path = Path(directory) / "blind-1.svg"
        second_path = Path(directory) / "blind-2.svg"
        blind_first = run((*BLIND_ARGS, "--output", str(first_path)))
        blind_second = run((*BLIND_ARGS, "--output", str(second_path)))
        require(lines(blind_first.stdout) == BLIND_LINES == lines(blind_second.stdout), "blind stdout mismatch")
        require(digest(first_path) == EXPECTED_BLIND_SHA256 == digest(second_path), "blind double-run/hash mismatch")
        ET.parse(first_path)
    require(digest(SVG) == before, "blind run changed canonical SVG")
    print("PASS deterministic compute: canonical double-run + cross-track blind stdout/SVG/XML/hash")


def audit_guards() -> None:
    before = digest(SVG)
    invalid = (
        ("--hedge-losses", "0,1;1"),
        ("--hedge-losses", "0;1"),
        ("--hedge-losses", "0,2;1,0"),
        ("--hedge-eta", "0"),
        ("--ogd-eta", "0"),
        ("--adaptive-actions", "1,3"),
        ("--perceptron-examples", "1,0,0"),
        ("--separator", "0,0"),
        ("--separator=-1,-1",),
        ("--boost-margins", "1,-1"),
        ("--online-risks", "0.2,1.2"),
        ("--delta", "1"),
        ("--ucb-counts", "0,2"),
        ("--logging-probabilities", "0.5,0.5,0.1"),
        ("--logging-probabilities", "0.5,0.5,0"),
        ("--chosen-action", "0"),
    )
    with tempfile.TemporaryDirectory(prefix="online-cum-guards-") as directory:
        for index, args in enumerate(invalid):
            result = run((*args, "--output", str(Path(directory) / f"invalid-{index}.svg")), check=False)
            require(result.returncode != 0, f"invalid contract accepted: {args}")
        no_output = run(("--hedge-eta", "0.5"), check=False)
        require(no_output.returncode != 0, "noncanonical run without output accepted")
        overwrite = run(("--hedge-eta", "0.5", "--output", str(SVG)), check=False)
        require(overwrite.returncode != 0, "noncanonical canonical overwrite accepted")
    require(digest(SVG) == before, "guard tests changed canonical SVG")
    print(f"PASS guards: invalid contracts rejected={len(invalid) + 2}, canonical asset preserved")


def audit_svg() -> None:
    root = ET.parse(SVG).getroot()
    require(root.tag.endswith("svg"), "asset is not SVG")
    texts = " ".join((element.text or "") for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "full-information sequence", "margin to exponential potential", "risk bridge and partial feedback",
        "eight-layer sequential audit", "No-regret != iid generalization", "bandit != RL",
    ):
        require(marker in texts, f"SVG misses marker: {marker}")
    print("PASS SVG semantics: three sequential-learning panels, eight-layer ledger and evidence-boundary footer")


def audit_prerequisite_and_state() -> None:
    result = subprocess.run(
        [sys.executable, str(PREREQUISITE_AUDIT)], cwd=ROOT,
        text=True, capture_output=True, check=True,
    )
    require("REL-CUM-01 material regression: PASS" in result.stdout, "REL-CUM-01 material prerequisite regressed")
    assessment = read(ASSESSMENT)
    require("REL-CUM-01-retained" in assessment and "本卷只能诊断性作答" in assessment,
            "personal prerequisite boundary missing")
    for path in STATE_SURFACES:
        content = read(path)
        require("ONLINE-CUM-01" in content, f"state surface misses ONLINE-CUM-01: {path.relative_to(ROOT)}")
        require("9/10" in content or "9 / 10" in content, f"state surface misses 9/10: {path.relative_to(ROOT)}")
        require("0/10" in content or "0 / 10" in content, f"state surface misses learner 0/10: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner: {path.relative_to(ROOT)}")
    print("PASS prerequisite boundary: REL-CUM-01 material regressed, personal prerequisite remains unmet/not-attempted")
    print("PASS state surfaces: ONLINE-CUM-01 material=9/10, learner=0/10/not-attempted")


def main() -> None:
    audit_nodes()
    audit_assessment()
    independent_math()
    audit_compute()
    audit_guards()
    audit_svg()
    audit_prerequisite_and_state()
    print("ONLINE-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
