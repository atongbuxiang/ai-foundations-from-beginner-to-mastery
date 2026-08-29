#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for REPR-CUM-01."""

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
CHAPTER = ROOT / "20-学习理论" / "20.7-表示学习、度量学习与自监督"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = CHAPTER / "表示学习、度量学习与自监督 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 表示学习、度量学习与自监督（20.7）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 表示学习、度量学习与自监督（20.7）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 表示学习、度量学习与自监督累计复现门.md"
GATE = LABS / "code" / "representation_selfsupervised_cumulative_gate.py"
MODEL_AUDIT = LABS / "code" / "classical_models_cumulative_contract_audit.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-representation-selfsupervised-cumulative-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "5ccfe7391e2205c2d225626e3c062ee45b036e72fee4182c9322e919d8e817bf"
EXPECTED_BLIND_SHA256 = "e0be10b2abce82da52fcac07c132087f18045bcb0a510eb814ffcdf471cab8a9"

CANONICAL_LINES = (
    "TRACK A weights=0.5,0.3,0.2 risks=identity:0.050000,invariant-S:0.250000,nuisance-N:0.350000,product:0.400000,enriched:0.000000 best=enriched triplet=0.200000 ap=0.833333 recall2=0.500000 nominal_views=48 effective_views=17.142857",
    "TRACK B q=0.800000 K=4 mi=0.192745 bayes_loss=1.240493 bound=0.145801 gap=0.046943 batch_loss=0.371539 probs=0.689672,0.253716,0.056612 gradients=-0.620656,0.507432,0.113223 collision=0.929444",
    "TRACK C spectrum=9,1,0 stable_rank=1.111111 pr=1.219512 effective_rank=1.384145 vicreg_spectral=0.666667 vicreg_constant=2.000000 ema_final=0.839844 log_risk=0.500402 square_risk=0.160000 nuisance_risk=0.500000",
)

BLIND_ARGS = (
    "--task-weights", "0.2,0.5,0.3",
    "--positive-distance", "0.6",
    "--negative-distance", "1.4",
    "--triplet-margin", "0.9",
    "--source-units", "10",
    "--views-per-source", "5",
    "--view-correlation", "0.4",
    "--match-probability", "0.7",
    "--candidates", "5",
    "--similarities", "0.8,0.4,-0.3",
    "--temperature", "0.4",
    "--class-prior", "0.4,0.35,0.25",
    "--negatives", "9",
    "--ema-decay", "0.6",
    "--teacher-start", "0.5",
    "--student-sequence", "2,-2,4,1",
)

BLIND_LINES = (
    "TRACK A weights=0.2,0.5,0.3 risks=identity:0.075000,invariant-S:0.400000,nuisance-N:0.250000,product:0.350000,enriched:0.000000 best=enriched triplet=0.100000 ap=0.833333 recall2=0.500000 nominal_views=50 effective_views=19.230769",
    "TRACK B q=0.700000 K=5 mi=0.082283 bayes_loss=1.543388 bound=0.066050 gap=0.016233 batch_loss=0.358937 probs=0.698418,0.256934,0.044648 gradients=-0.753955,0.642334,0.111621 collision=0.969949",
    "TRACK C spectrum=9,1,0 stable_rank=1.111111 pr=1.219512 effective_rank=1.384145 vicreg_spectral=0.666667 vicreg_constant=2.000000 ema_final=1.309600 log_risk=0.610864 square_risk=0.210000 nuisance_risk=0.500000",
)

EXPECTED_NODES = {
    53: "表示学习的任务、表示与下游风险",
    54: "度量学习、相似性与检索风险",
    55: "对比学习、InfoNCE 与密度比",
    56: "正负样本、Batch 依赖与梯度估计",
    57: "数据增强、不变性、等变性与任务充分性",
    58: "表示坍缩、非坍缩与可辨识边界",
    59: "遮蔽预测、Teacher–Student 与自监督目标",
    60: "Linear Probe、Fine-Tuning 与迁移评估",
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
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def output_lines(stdout: str) -> tuple[str, ...]:
    return tuple(line for line in stdout.splitlines() if line.startswith("TRACK "))


def audit_nodes() -> None:
    moc = read(MOC)
    for node_id, title in EXPECTED_NODES.items():
        path = CHAPTER / f"{title}.md"
        content = read(path)
        require(f"node_id: LT-{node_id}" in content, f"LT-{node_id}: node_id mismatch")
        require("status: draft" in content, f"LT-{node_id}: status must remain draft")
        require("exercises:" in content and "solutions:" in content, f"LT-{node_id}: exercise/solution metadata missing")
        figure_match = re.search(r'figure:\s*"\[\[([^\]]+)\]\]"', content)
        require(figure_match is not None, f"LT-{node_id}: figure metadata missing")
        require((ROOT / figure_match.group(1)).is_file(), f"LT-{node_id}: figure target missing")
        require(f"| LT-{node_id} | [[{title}]]" in moc, f"LT-{node_id}: MOC mapping missing")
        exercise = LABS / "exercises" / f"习题 - {title}.md"
        solution = LABS / "solutions" / f"解答 - {title}.md"
        require(exercise.is_file() and solution.is_file(), f"LT-{node_id}: A--E exercise pair missing")
    print("PASS LT-53--60 node bundle: 8/8 draft nodes, figures, exercises/solutions and MOC mappings")


def points_from_headings(content: str, solution: bool = False) -> list[int]:
    if solution:
        pattern = r"^## 第\s*(\d+)\s*题解答：.*?（(\d+) 分）\s*$"
    else:
        pattern = r"^### 第\s*(\d+)\s*题：.*?（(\d+) 分）\s*$"
    matches = re.findall(pattern, content, flags=re.MULTILINE)
    require([int(number) for number, _ in matches] == list(range(1, 15)), "question numbering must be 1--14")
    return [int(points) for _, points in matches]


def audit_assessment() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    scope = set(re.findall(r"LT-(?:5[3-9]|60)", assessment))
    require(scope == {f"LT-{number}" for number in range(53, 61)}, "assessment scope is not LT-53--60")
    question_points = points_from_headings(assessment)
    solution_points = points_from_headings(solution, solution=True)
    require(question_points == solution_points, "question/solution point ledgers differ")
    require(sum(question_points) == 100, "assessment points do not sum to 100")
    markers = (
        "oral_limit_minutes: 25", "time_limit_minutes: 240",
        "formal_prerequisite: MODEL-CUM-01-retained", "scorer nonce",
        "48 小时", "14 天", "not-attempted", "非法合同",
    )
    for marker in markers:
        require(marker in assessment, f"assessment misses gate marker: {marker}")
    for marker in (
        "seven-layer", "candidate-index", "non-collapse", "task sufficiency",
        "locked", "canonical", "blind", "SHA256",
    ):
        require(marker.lower() in experiment.lower(), f"experiment misses contract marker: {marker}")
    require("TRACK A" in solution and "TRACK B" in solution and "TRACK C" in solution, "solution misses canonical outputs")
    print("PASS REPR-CUM-01 assessment: scope=8/8, questions/solutions=14/14, points=100, oral/isolation/blind/delay gates")


def exact_candidate_loss(q: float, candidates: int) -> float:
    total = 0.0
    mass = 0.0
    for index in range(candidates):
        for anchor in (0, 1):
            for ys in itertools.product((0, 1), repeat=candidates):
                probability = 0.5 / candidates
                for candidate_index, value in enumerate(ys):
                    probability *= (
                        q if value == anchor else 1 - q
                    ) if candidate_index == index else 0.5
                ratios = [2 * (q if value == anchor else 1 - q) for value in ys]
                posterior = ratios[index] / sum(ratios)
                total += probability * -math.log(posterior)
                mass += probability
    require(math.isclose(mass, 1.0, abs_tol=1e-12), "candidate mass failed")
    return total


def independent_math() -> None:
    weights = (0.5, 0.3, 0.2)
    risks = (
        (0.0, 0.0, 0.25), (0.0, 0.5, 0.5), (0.5, 0.0, 0.5),
        (0.5, 0.5, 0.0), (0.0, 0.0, 0.0),
    )
    weighted = tuple(sum(a * b for a, b in zip(weights, row)) for row in risks)
    require(weighted == (0.05, 0.25, 0.35, 0.4, 0.0), "task risk table failed")
    require(math.isclose(max(0.0, 0.8 - 1.3 + 0.7), 0.2), "triplet failed")
    require(math.isclose(0.5 * (1 + 2 / 3), 5 / 6), "AP failed")
    require(math.isclose(48 / (1 + 3 * 0.6), 17.142857142857142), "effective views failed")

    q, candidates = 0.8, 4
    entropy = -(q * math.log(q) + (1 - q) * math.log(1 - q))
    mutual_information = math.log(2) - entropy
    bayes_loss = exact_candidate_loss(q, candidates)
    bound = math.log(candidates) - bayes_loss
    require(math.isclose(mutual_information, 0.19274475702175736, abs_tol=1e-12), "MI failed")
    require(math.isclose(bayes_loss, 1.2404929694885098, abs_tol=1e-12), "Bayes NCE failed")
    require(bound <= mutual_information + 1e-12, "InfoNCE lower-bound ordering failed")

    logits = (2.0, 1.0, -0.5)
    exps = tuple(math.exp(value) for value in logits)
    probabilities = tuple(value / sum(exps) for value in exps)
    gradients = tuple((value - (1 if index == 0 else 0)) / 0.5 for index, value in enumerate(probabilities))
    require(math.isclose(-math.log(probabilities[0]), 0.37153903185268294, abs_tol=1e-12), "batch loss failed")
    require(math.isclose(sum(gradients), 0.0, abs_tol=1e-12), "softmax gradients do not sum to zero")
    prior = (0.5, 0.3, 0.2)
    collision = sum(value * (1 - (1 - value) ** 7) for value in prior)
    require(math.isclose(collision, 0.92944442, abs_tol=1e-12), "collision failed")

    eigenvalues = (9.0, 1.0, 0.0)
    trace = sum(eigenvalues)
    stable = trace / max(eigenvalues)
    participation = trace * trace / sum(value * value for value in eigenvalues)
    effective = math.exp(-(0.9 * math.log(0.9) + 0.1 * math.log(0.1)))
    require(math.isclose(stable, 10 / 9), "stable rank failed")
    require(math.isclose(participation, 100 / 82), "participation ratio failed")
    require(math.isclose(effective, 1.384145488461686), "effective rank failed")
    teacher = 0.0
    for student in (1.0, 3.0, -1.0, 2.0):
        teacher = 0.75 * teacher + 0.25 * student
    require(math.isclose(teacher, 0.83984375), "EMA failed")
    require(math.isclose(q * (1 - q), 0.16), "square Bayes risk failed")
    print("PASS independent math: task/metric/dependence + exact InfoNCE/batch + spectrum/VICReg/EMA anchors")


def audit_compute() -> None:
    canonical_before = SVG.read_bytes()
    require(hashlib.sha256(canonical_before).hexdigest() == EXPECTED_CANONICAL_SHA256, "stored canonical hash mismatch")
    first = run(())
    bytes_first = SVG.read_bytes()
    second = run(())
    bytes_second = SVG.read_bytes()
    require(output_lines(first.stdout) == CANONICAL_LINES, "canonical stdout mismatch")
    require(output_lines(second.stdout) == CANONICAL_LINES, "canonical second stdout mismatch")
    require(bytes_first == bytes_second == canonical_before, "canonical double-run changed bytes")

    with tempfile.TemporaryDirectory(prefix="repr-cum-audit-") as directory:
        blind_path = Path(directory) / "blind.svg"
        blind_first = run((*BLIND_ARGS, "--output", str(blind_path)))
        blind_bytes_first = blind_path.read_bytes()
        blind_second = run((*BLIND_ARGS, "--output", str(blind_path)))
        blind_bytes_second = blind_path.read_bytes()
        require(output_lines(blind_first.stdout) == BLIND_LINES, "blind stdout mismatch")
        require(output_lines(blind_second.stdout) == BLIND_LINES, "blind second stdout mismatch")
        require(blind_bytes_first == blind_bytes_second, "blind double-run changed bytes")
        require(hashlib.sha256(blind_bytes_first).hexdigest() == EXPECTED_BLIND_SHA256, "blind hash mismatch")
        ET.fromstring(blind_bytes_first)
    print("PASS deterministic compute: canonical double-run + cross-track blind stdout/SVG/XML/hash")


def audit_guards() -> None:
    canonical_before = digest(SVG)
    invalid = (
        ("--task-weights", "0.5,0.5"),
        ("--task-weights", "0.5,0.5,0.5"),
        ("--view-correlation", "1.2"),
        ("--match-probability", "0.5"),
        ("--candidates", "1"),
        ("--temperature", "0"),
        ("--class-prior", "0.5,0.6"),
        ("--negatives", "0"),
        ("--ema-decay", "1"),
    )
    with tempfile.TemporaryDirectory(prefix="repr-cum-guards-") as directory:
        for index, args in enumerate(invalid):
            result = run((*args, "--output", str(Path(directory) / f"invalid-{index}.svg")), check=False)
            require(result.returncode != 0, f"invalid contract accepted: {args}")
        no_output = run(("--candidates", "3"), check=False)
        require(no_output.returncode != 0, "noncanonical run without output was accepted")
        overwrite = run(("--candidates", "3", "--output", str(SVG)), check=False)
        require(overwrite.returncode != 0, "noncanonical canonical overwrite was accepted")
    require(digest(SVG) == canonical_before, "guard tests changed canonical asset")
    print(f"PASS guards: invalid contracts rejected={len(invalid) + 2}, canonical asset preserved")


def audit_svg() -> None:
    tree = ET.parse(SVG)
    root = tree.getroot()
    require(root.tag.endswith("svg"), "canonical asset is not SVG")
    texts = " ".join((element.text or "") for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "task-indexed representation", "candidate law and batch", "non-collapse and targets",
        "seven-layer representation audit", "low pretext loss", "non-collapse != usefulness",
    ):
        require(marker in texts, f"SVG misses semantic marker: {marker}")
    print("PASS SVG semantics: three estimand panels, seven-layer ledger and evidence-boundary footer")


def audit_prerequisite_and_state() -> None:
    prerequisite = subprocess.run(
        [sys.executable, str(MODEL_AUDIT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    require("MODEL-CUM-01 material regression: PASS" in prerequisite.stdout, "MODEL-CUM-01 material prerequisite regressed")
    assessment = read(ASSESSMENT)
    require("MODEL-CUM-01-retained" in assessment, "formal personal prerequisite missing")
    require("个人前置尚未满足" in assessment, "unmet personal prerequisite boundary missing")
    for path in STATE_SURFACES:
        content = read(path)
        require("REPR-CUM-01" in content, f"state surface misses REPR-CUM-01: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner status: {path.relative_to(ROOT)}")
        require("9/10" in content or "9 / 10" in content or path == MOC, f"state surface misses 9/10 material count: {path.relative_to(ROOT)}")
        require("0/10" in content or "0 / 10" in content, f"state surface misses 0/10 learner count: {path.relative_to(ROOT)}")
    print("PASS prerequisite boundary: MODEL-CUM-01 material regressed, personal prerequisite remains unmet/not-attempted")
    print("PASS state surfaces: REPR-CUM-01 current material=9/10, learner=0/10/not-attempted")


def main() -> None:
    audit_nodes()
    audit_assessment()
    independent_math()
    audit_compute()
    audit_guards()
    audit_svg()
    audit_prerequisite_and_state()
    print("REPR-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
