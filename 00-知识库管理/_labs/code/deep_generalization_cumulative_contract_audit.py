#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for DEEP-CUM-01."""

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
CHAPTER = ROOT / "20-学习理论" / "20.10-深度泛化理论接口与开放边界"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = CHAPTER / "深度泛化理论接口与开放边界 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 深度泛化理论接口与开放边界（20.10）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 深度泛化理论接口与开放边界（20.10）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 深度泛化理论接口与开放边界累计复现门.md"
GATE = LABS / "code" / "deep_generalization_cumulative_gate.py"
PREREQUISITE_AUDIT = LABS / "code" / "online_boosting_cumulative_contract_audit.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-deep-generalization-cumulative-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "1aa9c7aa4661cf7799c06fc45d13c6e6cba67530a540e542a53dfb487bf49230"
EXPECTED_BLIND_SHA256 = "fa3fdfbb9f2c8a7a57dbf2ed8b9b76ea438191d20bd84deba107c9017aec7216"

CANONICAL_LINES = (
    "TRACK A dims=5,10,15,18,22,25,30,40,60,100 risks=0.089286,0.277778,0.937500,4.500000,5.090909,1.450000,0.888889,0.763158,0.794872,0.863291 peak_p=22 peak=5.090909 tail=0.863291 min_norm=0.333333,0.333333,0.666667 min_length=0.816497 shifted_length=2.160247 train_residual=0.000000 null_test_gap=2.000000",
    "TRACK B c=4.000000 sharp_base=2.000000 sharp_scaled=16.062500 function_product=1.000000 path=1.000000 spectral_product=1.500000 stable_rank_sum=5.250000 complexity=3.436932 certificate=0.687386 complexity_scaled=3.436932",
    "TRACK C lambdas=1.600000,0.400000 r0_norm=1.000000 rt=0.154712,-0.146482 rt_norm=0.213056 slow_fraction=0.500000 particle_prediction=0.375000->0.448730 feature_moment=0.156250->0.207031 feature_drift=0.325000 ntk=0.578125->0.627258 ntk_drift=0.084987 regime=feature-moving",
)

BLIND_ARGS = (
    "--sample-size", "24", "--dimensions", "6,12,18,22,26,30,36,48,72,120",
    "--noise-variance", "0.16", "--signal-norm-squared", "1.44",
    "--design", "2,0,1;0,1,1", "--responses", "1,2", "--null-shift", "1.5",
    "--rescale", "8", "--layer-spectral", "1.5,0.75,2",
    "--layer-frobenius", "2.1213203436,1.0606601718,2.8284271247",
    "--certificate-samples", "144", "--margin", "0.75",
    "--kernel-rho", "0.3", "--kernel-time", "2", "--initial-residual", "1,-1",
    "--particle-a", "0.8,-1.2", "--particle-w", "0.4,-0.3",
    "--particle-step", "0.1", "--particle-target", "0.8",
)

BLIND_LINES = (
    "TRACK A dims=6,12,18,22,26,30,36,48,72,120 risks=0.056471,0.174545,0.576000,3.520000,3.950769,1.056000,0.829091,0.886957,1.041702,1.192421 peak_p=26 peak=3.950769 tail=1.192421 min_norm=0.000000,1.000000,1.000000 min_length=1.414214 shifted_length=2.061553 train_residual=0.000000 null_test_gap=1.500000",
    "TRACK B c=8.000000 sharp_base=2.000000 sharp_scaled=64.015625 function_product=1.000000 path=1.000000 spectral_product=2.250000 stable_rank_sum=6.000000 complexity=5.511352 certificate=0.612372 complexity_scaled=5.511352",
    "TRACK C lambdas=1.300000,0.700000 r0_norm=1.414214 rt=0.246597,-0.246597 rt_norm=0.348741 slow_fraction=1.000000 particle_prediction=0.340000->0.366975 feature_moment=0.125000->0.141190 feature_drift=0.129521 ntk=0.582500->0.598448 ntk_drift=0.027379 regime=feature-moving",
)

EXPECTED_NODES = {
    77: "插值、双下降与经典偏差方差边界",
    78: "过参数化与 Benign Overfitting",
    79: "隐式偏置、最大间隔与优化选择",
    80: "范数、平坦性、Sharpness 与参数化不变性",
    81: "神经网络容量与 Norm-Based Bound",
    82: "NTK、Lazy Training 与 Kernel Regime",
    83: "Mean-Field、Feature Learning 与训练 Regime",
    84: "深度泛化证据地图与开放问题",
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
        read(LABS / "exercises" / f"习题 - {title}.md")
        read(LABS / "solutions" / f"解答 - {title}.md")
        figure_match = re.search(r'^figure:\s*"\[\[([^\]]+)\]\]"', content, re.M)
        require(figure_match is not None, f"LT-{node_id}: figure frontmatter missing")
        require((ROOT / figure_match.group(1)).is_file(), f"LT-{node_id}: figure asset missing")
    print("PASS LT-77--84 node bundle: 8/8 draft nodes, figures, exercises/solutions and MOC mappings")


def audit_assessment() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    require("assessment_id: DEEP-CUM-01" in assessment, "assessment id missing")
    scope_match = re.search(r"^scope:\s*\[([^\]]+)\]", assessment, re.M)
    require(scope_match is not None, "scope frontmatter missing")
    scope = tuple(item.strip() for item in scope_match.group(1).split(","))
    require(scope == tuple(f"LT-{index}" for index in range(77, 85)), "assessment scope mismatch")
    questions = re.findall(r"^### 第 (\d+) 题", assessment, re.M)
    answers = re.findall(r"^## 第 (\d+) 题解答", solution, re.M)
    require(questions == [str(index) for index in range(1, 15)], "assessment is not 14 ordered questions")
    require(answers == [str(index) for index in range(1, 15)], "solution is not 14 ordered answers")
    points = [int(value) for value in re.findall(r"^### 第 \d+ 题[^\n]*（(\d+) 分）", assessment, re.M)]
    require(len(points) == 14 and sum(points) == 100, f"point contract mismatch: {points}")
    for marker in (
        "oral_limit_minutes: 25", "time_limit_minutes: 240", "ONLINE-CUM-01-retained",
        "attempt_id", "scorer nonce", "blind", "48 小时", "14 天", "not-attempted",
    ):
        require(marker in assessment, f"assessment marker missing: {marker}")
    for marker in (
        "Canonical 回归输出", EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256,
        "reciprocal rescaling", "population generalization", "not-attempted",
    ):
        require(marker in solution, f"solution marker missing: {marker}")
    for marker in (
        "九层可靠复现账本", "Canonical 复现", "Blind 干预", "输入与覆盖保护",
        "学习证据状态机", "48 小时", "14 天", "deep_generalization_cumulative_gate.py",
    ):
        require(marker in experiment, f"experiment marker missing: {marker}")
    print("PASS DEEP-CUM-01 assessment: scope=8/8, questions/solutions=14/14, points=100, oral/isolation/blind/delay gates")


def independent_math() -> None:
    n, sigma2, beta2 = 20, 0.25, 1.0
    dimensions = (5, 10, 15, 18, 22, 25, 30, 40, 60, 100)
    risks = tuple(
        sigma2 * p / (n - p - 1) if p < n - 1
        else beta2 * (1 - n / p) + sigma2 * n / (p - n - 1)
        for p in dimensions
    )
    require(math.isclose(risks[3], 4.5, abs_tol=1e-12), "underparameterized risk mismatch")
    require(math.isclose(risks[4], 56 / 11, abs_tol=1e-12), "overparameterized peak mismatch")
    require(max(range(len(risks)), key=risks.__getitem__) == 4, "peak location mismatch")
    require(math.isclose(risks[-1], 1 - 0.2 + 5 / 79, abs_tol=1e-12), "tail risk mismatch")

    min_norm = (1 / 3, 1 / 3, 2 / 3)
    null = (-1 / math.sqrt(3), -1 / math.sqrt(3), 1 / math.sqrt(3))
    shifted = tuple(value + 2 * direction for value, direction in zip(min_norm, null))
    require(math.isclose(math.sqrt(sum(value * value for value in min_norm)), math.sqrt(2 / 3), abs_tol=1e-12), "min norm mismatch")
    require(math.isclose(math.sqrt(sum(value * value for value in shifted)), math.sqrt(14 / 3), abs_tol=1e-12), "shifted norm mismatch")
    shifted_residual = math.hypot(shifted[0] + shifted[2] - 1, shifted[1] + shifted[2] - 1)
    require(math.isclose(shifted_residual, 0.0, abs_tol=1e-12), "null shift changed fit")

    c = 4.0
    require(math.isclose(c * c + c ** -2, 16.0625, abs_tol=1e-12), "sharpness mismatch")
    stable_rank_sum = 5 / 4 + 2 + 2
    complexity = 1.5 * math.sqrt(stable_rank_sum)
    require(math.isclose(complexity, 3.43693177121688, abs_tol=1e-12), "capacity mismatch")
    require(math.isclose(complexity / 5, 0.687386354243376, abs_tol=1e-12), "certificate mismatch")

    plus = math.exp(-4.8) / math.sqrt(2)
    minus = math.exp(-1.2) / math.sqrt(2)
    final = ((plus + minus) / math.sqrt(2), (plus - minus) / math.sqrt(2))
    require(math.isclose(final[0], 0.15471197948061105, abs_tol=1e-12), "kernel mode x mismatch")
    require(math.isclose(final[1], -0.14648223243159103, abs_tol=1e-12), "kernel mode y mismatch")
    next_a = (1.03125, -1.015625)
    next_w = (0.5625, -0.3125)
    prediction = sum(a * w for a, w in zip(next_a, next_w)) / 2
    feature = sum(w * w for w in next_w) / 2
    ntk = sum(a * a + w * w for a, w in zip(next_a, next_w)) / 4
    require(math.isclose(prediction, 0.44873046875, abs_tol=1e-12), "particle prediction mismatch")
    require(math.isclose(feature, 0.20703125, abs_tol=1e-12), "feature moment mismatch")
    require(math.isclose(ntk, 0.62725830078125, abs_tol=1e-12), "particle NTK mismatch")
    print("PASS independent math: interpolation/selection + invariance/capacity + kernel/particle anchors")


def audit_compute() -> None:
    before = digest(SVG)
    require(before == EXPECTED_CANONICAL_SHA256, "stored canonical SVG hash mismatch")
    first = run(())
    first_hash = digest(SVG)
    second = run(())
    second_hash = digest(SVG)
    require(lines(first.stdout) == CANONICAL_LINES == lines(second.stdout), "canonical stdout mismatch")
    require(first_hash == EXPECTED_CANONICAL_SHA256 == second_hash, "canonical double-run/hash mismatch")
    with tempfile.TemporaryDirectory(prefix="deep-cum-blind-") as directory:
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
        ("--sample-size", "3"),
        ("--dimensions", "5,10,10,18,22"),
        ("--dimensions", "5,10,15,19,22"),
        ("--noise-variance", "-1"),
        ("--design", "1,0;0,1"),
        ("--design", "1,0,0;2,0,0"),
        ("--responses", "1"),
        ("--rescale", "0"),
        ("--layer-spectral", "2"),
        ("--layer-frobenius", "1,1,1"),
        ("--margin", "0"),
        ("--kernel-rho", "1"),
        ("--kernel-time", "-1"),
        ("--initial-residual", "0,0"),
        ("--particle-a", "1"),
        ("--particle-step", "0"),
    )
    with tempfile.TemporaryDirectory(prefix="deep-cum-guards-") as directory:
        for index, args in enumerate(invalid):
            result = run((*args, "--output", str(Path(directory) / f"invalid-{index}.svg")), check=False)
            require(result.returncode != 0, f"invalid contract accepted: {args}")
        no_output = run(("--rescale", "2"), check=False)
        require(no_output.returncode != 0, "noncanonical run without output accepted")
        overwrite = run(("--rescale", "2", "--output", str(SVG)), check=False)
        require(overwrite.returncode != 0, "noncanonical canonical overwrite accepted")
    require(digest(SVG) == before, "guard tests changed canonical SVG")
    print(f"PASS guards: invalid contracts rejected={len(invalid) + 2}, canonical asset preserved")


def audit_svg() -> None:
    root = ET.parse(SVG).getroot()
    require(root.tag.endswith("svg"), "asset is not SVG")
    texts = " ".join((element.text or "") for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "interpolation risk + selected solution", "parameterization stress test + norm certificate",
        "fixed-kernel modes + moving-feature diagnostic", "interpolation != benign overfitting",
        "raw sharpness correlation != invariant explanation", "training dynamics != population generalization",
        "object · quantifier · invariance · regime",
    ):
        require(marker in texts, f"SVG misses marker: {marker}")
    print("PASS SVG semantics: three deep-generalization panels, invariance/regime ledger and evidence-boundary footer")


def audit_prerequisite_and_state() -> None:
    result = subprocess.run(
        [sys.executable, str(PREREQUISITE_AUDIT)], cwd=ROOT,
        text=True, capture_output=True, check=True,
    )
    require("ONLINE-CUM-01 material regression: PASS" in result.stdout, "ONLINE-CUM-01 material prerequisite regressed")
    assessment = read(ASSESSMENT)
    require("ONLINE-CUM-01-retained" in assessment and "本卷只能诊断性作答" in assessment,
            "personal prerequisite boundary missing")
    for path in STATE_SURFACES:
        content = read(path)
        require("DEEP-CUM-01" in content, f"state surface misses DEEP-CUM-01: {path.relative_to(ROOT)}")
        require("10/10" in content or "10 / 10" in content, f"state surface misses 10/10: {path.relative_to(ROOT)}")
        require("0/10" in content or "0 / 10" in content, f"state surface misses learner 0/10: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner: {path.relative_to(ROOT)}")
    print("PASS prerequisite boundary: ONLINE-CUM-01 material regressed, personal prerequisite remains unmet/not-attempted")
    print("PASS state surfaces: DEEP-CUM-01 material=10/10, learner=0/10/not-attempted")


def main() -> None:
    audit_nodes()
    audit_assessment()
    independent_math()
    audit_compute()
    audit_guards()
    audit_svg()
    audit_prerequisite_and_state()
    print("DEEP-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
