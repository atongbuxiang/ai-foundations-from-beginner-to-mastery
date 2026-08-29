#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for REL-CUM-01."""

from __future__ import annotations

import hashlib
import itertools
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "20-学习理论" / "20.8-校准、不确定性与分布偏移"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = CHAPTER / "校准、不确定性与分布偏移 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 校准、不确定性与分布偏移（20.8）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 校准、不确定性与分布偏移（20.8）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 校准、不确定性与分布偏移累计复现门.md"
GATE = LABS / "code" / "calibration_shift_cumulative_gate.py"
PREREQUISITE_AUDIT = LABS / "code" / "representation_selfsupervised_cumulative_contract_audit.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-calibration-shift-cumulative-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "e98073eb6f23a596d07e1a5a1c8a0b8dcd75322284df4f27aec9d92926abeeff"
EXPECTED_BLIND_SHA256 = "72ad44b1b1cd84ddfbb12fafc5b1b16da8a0320d207dafe650354566b9cfa2f7"

CANONICAL_LINES = (
    "TRACK A accuracy=0.700000 ece=0.075000 brier=0.207500 log_loss=0.614554 uncertainty=0.250000 resolution=0.050000 reliability=0.007500 mixture_mean=0.800000 aleatoric=1.100000 epistemic=2.160000 total_variance=3.260000",
    "TRACK B m=7 alpha=0.250000 k=6 quantile=0.700000 rank_coverage=0.750000 interval=2.500000,3.900000 weights=0.400000,0.750000,5.000000 source_risk=0.250000 target_risk=0.510000 weighted_risk=0.510000 weight_second=2.805000 ess=35.650624 clipped=0.270000 self_normalized=0.385714",
    "TRACK C divergence=0.800000 source_risk=0.000000 target_risk=0.300000 joint_ideal=0.300000 bound=0.700000 auroc=0.888889 id_accept=0.666667 ood_false_accept=0.333333 average_group=0.160000 worst_group=0.500000",
)

BLIND_ARGS = (
    "--forecast-probabilities", "0.15,0.35,0.65,0.85",
    "--event-rates", "0.2,0.4,0.6,0.8",
    "--mixture-weights", "0.3,0.7",
    "--mixture-means=-0.5,1.5",
    "--mixture-variances", "0.8,1.2",
    "--conformal-scores", "0.05,0.15,0.3,0.45,0.6,0.75,0.85,0.95",
    "--alpha", "0.2",
    "--prediction", "2.5",
    "--source-probabilities", "0.4,0.4,0.2",
    "--target-probabilities", "0.2,0.2,0.6",
    "--losses", "0.2,0.4,0.7",
    "--sample-size", "120",
    "--weight-clip", "2.5",
    "--id-scores", "0.95,0.7,0.55",
    "--ood-scores", "0.8,0.5,0.1",
    "--ood-threshold", "0.6",
    "--group-weights", "0.5,0.3,0.2",
    "--group-risks", "0.12,0.25,0.45",
)

BLIND_LINES = (
    "TRACK A accuracy=0.700000 ece=0.050000 brier=0.202500 log_loss=0.593919 uncertainty=0.250000 resolution=0.050000 reliability=0.002500 mixture_mean=0.900000 aleatoric=1.080000 epistemic=0.840000 total_variance=1.920000",
    "TRACK B m=8 alpha=0.200000 k=8 quantile=0.950000 rank_coverage=0.888889 interval=1.550000,3.450000 weights=0.500000,0.500000,3.000000 source_risk=0.380000 target_risk=0.540000 weighted_risk=0.540000 weight_second=2.000000 ess=60.000000 clipped=0.470000 self_normalized=0.522222",
    "TRACK C divergence=0.800000 source_risk=0.000000 target_risk=0.200000 joint_ideal=0.200000 bound=0.600000 auroc=0.777778 id_accept=0.666667 ood_false_accept=0.333333 average_group=0.225000 worst_group=0.450000",
)

EXPECTED_NODES = {
    61: "概率校准、Proper Scoring Rule 与可靠性图",
    62: "Aleatoric、Epistemic 与模型不确定性",
    63: "Bayesian Posterior Predictive、Ensemble 与近似边界",
    64: "Conformal Prediction 与有限样本 Coverage",
    65: "Covariate、Label 与 Concept Shift",
    66: "重要性加权与 Covariate Shift 校正",
    67: "Domain Adaptation 与 Domain Generalization Bound",
    68: "OOD、鲁棒性与因果不变性的边界",
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
        [sys.executable, str(GATE), *args],
        cwd=ROOT, text=True, capture_output=True, check=check,
    )


def output_lines(stdout: str) -> tuple[str, ...]:
    return tuple(line for line in stdout.splitlines() if line.startswith("TRACK "))


def audit_nodes() -> None:
    moc = read(MOC)
    for node_id, title in EXPECTED_NODES.items():
        content = read(CHAPTER / f"{title}.md")
        require(f"node_id: LT-{node_id}" in content, f"LT-{node_id}: node_id mismatch")
        require("status: draft" in content, f"LT-{node_id}: status must remain draft")
        require("exercises:" in content and "solutions:" in content, f"LT-{node_id}: exercise/solution metadata missing")
        figure_match = re.search(r'figure:\s*"\[\[([^\]]+)\]\]"', content)
        require(figure_match is not None, f"LT-{node_id}: figure metadata missing")
        require((ROOT / figure_match.group(1)).is_file(), f"LT-{node_id}: figure target missing")
        require(f"| LT-{node_id} | [[{title}]]" in moc, f"LT-{node_id}: MOC mapping missing")
        require((LABS / "exercises" / f"习题 - {title}.md").is_file(), f"LT-{node_id}: exercise missing")
        require((LABS / "solutions" / f"解答 - {title}.md").is_file(), f"LT-{node_id}: solution missing")
    print("PASS LT-61--68 node bundle: 8/8 draft nodes, figures, exercises/solutions and MOC mappings")


def points(content: str, solution: bool) -> list[int]:
    pattern = (
        r"^## 第\s*(\d+)\s*题解答：.*?（(\d+) 分）\s*$"
        if solution else
        r"^### 第\s*(\d+)\s*题：.*?（(\d+) 分）\s*$"
    )
    matches = re.findall(pattern, content, flags=re.MULTILINE)
    require([int(number) for number, _ in matches] == list(range(1, 15)), "question numbering must be 1--14")
    return [int(value) for _, value in matches]


def audit_assessment() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    scope = set(re.findall(r"LT-(?:6[1-8])", assessment))
    require(scope == {f"LT-{number}" for number in range(61, 69)}, "scope is not LT-61--68")
    question_points = points(assessment, False)
    solution_points = points(solution, True)
    require(question_points == solution_points and sum(question_points) == 100, "question/solution point ledger failed")
    for marker in (
        "oral_limit_minutes: 25", "time_limit_minutes: 240",
        "formal_prerequisite: REPR-CUM-01-retained", "scorer nonce",
        "48 小时", "14 天", "非法合同", "not-attempted",
    ):
        require(marker in assessment, f"assessment misses marker: {marker}")
    for marker in (
        "eight-layer reliability audit", "exchangeability", "overlap",
        "canonical", "blind", "SHA256", "图没有证明什么",
    ):
        require(marker.lower() in experiment.lower(), f"experiment misses marker: {marker}")
    require(all(marker in solution for marker in ("TRACK A", "TRACK B", "TRACK C")), "solution misses canonical outputs")
    print("PASS REL-CUM-01 assessment: scope=8/8, questions/solutions=14/14, points=100, oral/isolation/blind/delay gates")


def independent_math() -> None:
    forecast = (0.1, 0.4, 0.7, 0.9)
    event = (0.2, 0.4, 0.6, 0.8)
    accuracy = sum(rate if probability >= 0.5 else 1 - rate for probability, rate in zip(forecast, event)) / 4
    ece = sum(abs(probability - rate) for probability, rate in zip(forecast, event)) / 4
    brier = sum((probability - rate) ** 2 + rate * (1 - rate) for probability, rate in zip(forecast, event)) / 4
    log_loss = sum(-(rate * math.log(probability) + (1 - rate) * math.log(1 - probability)) for probability, rate in zip(forecast, event)) / 4
    require(math.isclose(accuracy, 0.7) and math.isclose(ece, 0.075), "accuracy/ECE failed")
    require(math.isclose(brier, 0.2075) and math.isclose(log_loss, 0.6145541543382527), "proper risks failed")
    require(math.isclose(brier, 0.25 - 0.05 + 0.0075), "Brier decomposition failed")
    mean = 0.4 * -1 + 0.6 * 2
    within = 0.4 * 0.5 + 0.6 * 1.5
    between = 0.4 * (-1 - mean) ** 2 + 0.6 * (2 - mean) ** 2
    require(math.isclose(mean, 0.8) and math.isclose(within, 1.1) and math.isclose(between, 2.16), "mixture variance failed")

    scores = (0.1, 0.2, 0.25, 0.4, 0.55, 0.7, 0.9)
    k = math.ceil((len(scores) + 1) * 0.75)
    require(k == 6 and math.isclose(scores[k - 1], 0.7) and math.isclose(k / 8, 0.75), "conformal rank failed")
    source, target, losses = (0.5, 0.4, 0.1), (0.2, 0.3, 0.5), (0.1, 0.3, 0.8)
    weights = tuple(t / s for s, t in zip(source, target))
    target_risk = sum(p * loss for p, loss in zip(target, losses))
    weighted = sum(p * w * loss for p, w, loss in zip(source, weights, losses))
    second = sum(p * w * w for p, w in zip(source, weights))
    require(weights == (0.4, 0.7499999999999999, 5.0), "importance weights failed")
    require(math.isclose(target_risk, 0.51) and math.isclose(weighted, 0.51), "target identity failed")
    require(math.isclose(second, 2.805) and math.isclose(100 / second, 35.65062388591801), "ESS failed")

    hypotheses = tuple(tuple(int(value >= threshold) for value in range(3)) for threshold in range(4))
    divergence = 0.0
    for first, second_h in itertools.combinations(hypotheses, 2):
        ds = sum(p for p, a, b in zip((0.6, 0.3, 0.1), first, second_h) if a != b)
        dt = sum(p for p, a, b in zip((0.2, 0.3, 0.5), first, second_h) if a != b)
        divergence = max(divergence, 2 * abs(ds - dt))
    require(math.isclose(divergence, 0.8), "H-delta-H failed")
    require(math.isclose(8 / 9, 0.8888888888888888), "AUROC anchor failed")
    require(math.isclose(0.7 * 0.1 + 0.2 * 0.2 + 0.1 * 0.5, 0.16), "group risk failed")
    print("PASS independent math: calibration/mixture + conformal/importance + adaptation/OOD/group anchors")


def audit_compute() -> None:
    stored = SVG.read_bytes()
    require(hashlib.sha256(stored).hexdigest() == EXPECTED_CANONICAL_SHA256, "canonical hash mismatch")
    first = run(())
    bytes_first = SVG.read_bytes()
    second = run(())
    bytes_second = SVG.read_bytes()
    require(output_lines(first.stdout) == CANONICAL_LINES, "canonical stdout mismatch")
    require(output_lines(second.stdout) == CANONICAL_LINES, "canonical second stdout mismatch")
    require(stored == bytes_first == bytes_second, "canonical double-run changed bytes")
    with tempfile.TemporaryDirectory(prefix="rel-cum-audit-") as directory:
        output = Path(directory) / "blind.svg"
        blind_first = run((*BLIND_ARGS, "--output", str(output)))
        first_bytes = output.read_bytes()
        blind_second = run((*BLIND_ARGS, "--output", str(output)))
        second_bytes = output.read_bytes()
        require(output_lines(blind_first.stdout) == BLIND_LINES, "blind stdout mismatch")
        require(output_lines(blind_second.stdout) == BLIND_LINES, "blind second stdout mismatch")
        require(first_bytes == second_bytes, "blind double-run changed bytes")
        require(hashlib.sha256(first_bytes).hexdigest() == EXPECTED_BLIND_SHA256, "blind hash mismatch")
        ET.fromstring(first_bytes)
    print("PASS deterministic compute: canonical double-run + cross-track blind stdout/SVG/XML/hash")


def audit_guards() -> None:
    before = digest(SVG)
    invalid = (
        ("--forecast-probabilities", "0.1,0.4"),
        ("--forecast-probabilities", "0,0.4,0.7,0.9"),
        ("--event-rates", "0.25,0.4,0.6,0.8"),
        ("--mixture-weights", "0.3,0.3"),
        ("--mixture-variances", "0.5,-1"),
        ("--conformal-scores", "0.2,0.1"),
        ("--alpha", "0.01"),
        ("--source-probabilities", "0.5,0.5,0"),
        ("--sample-size", "0"),
        ("--source-label-threshold", "4"),
        ("--group-weights", "0.5,0.5,0.5"),
    )
    with tempfile.TemporaryDirectory(prefix="rel-cum-guards-") as directory:
        for index, args in enumerate(invalid):
            result = run((*args, "--output", str(Path(directory) / f"invalid-{index}.svg")), check=False)
            require(result.returncode != 0, f"invalid contract accepted: {args}")
        no_output = run(("--alpha", "0.2"), check=False)
        require(no_output.returncode != 0, "noncanonical run without output accepted")
        overwrite = run(("--alpha", "0.2", "--output", str(SVG)), check=False)
        require(overwrite.returncode != 0, "noncanonical overwrite accepted")
    require(digest(SVG) == before, "guard tests changed canonical asset")
    print(f"PASS guards: invalid contracts rejected={len(invalid) + 2}, canonical asset preserved")


def audit_svg() -> None:
    root = ET.parse(SVG).getroot()
    require(root.tag.endswith("svg"), "asset is not SVG")
    texts = " ".join((element.text or "") for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "calibration and uncertainty", "coverage and overlap", "adaptation, OOD and groups",
        "eight-layer reliability audit", "calibrated !=", "marginal coverage !=",
    ):
        require(marker in texts, f"SVG misses marker: {marker}")
    print("PASS SVG semantics: three reliability panels, eight-layer ledger and evidence-boundary footer")


def audit_prerequisite_and_state() -> None:
    result = subprocess.run(
        [sys.executable, str(PREREQUISITE_AUDIT)],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    require("REPR-CUM-01 material regression: PASS" in result.stdout, "REPR-CUM-01 material prerequisite regressed")
    assessment = read(ASSESSMENT)
    require("REPR-CUM-01-retained" in assessment and "本卷只能诊断性作答" in assessment, "personal prerequisite boundary missing")
    for path in STATE_SURFACES:
        content = read(path)
        require("REL-CUM-01" in content, f"state surface misses REL-CUM-01: {path.relative_to(ROOT)}")
        require("10/10" in content or "10 / 10" in content or path == MOC, f"state surface misses 10/10: {path.relative_to(ROOT)}")
        require("0/10" in content or "0 / 10" in content, f"state surface misses learner 0/10: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner: {path.relative_to(ROOT)}")
    print("PASS prerequisite boundary: REPR-CUM-01 material regressed, personal prerequisite remains unmet/not-attempted")
    print("PASS state surfaces: REL-CUM-01 current material=10/10, learner=0/10/not-attempted")


def main() -> None:
    audit_nodes()
    audit_assessment()
    independent_math()
    audit_compute()
    audit_guards()
    audit_svg()
    audit_prerequisite_and_state()
    print("REL-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
