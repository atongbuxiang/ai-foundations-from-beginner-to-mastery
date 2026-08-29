#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for LT-QUAL-01.

The audit deliberately does not import the gate generator. It reconstructs the
threshold output law, ghost replacement expectation, stability witness,
finite/compression/PAC-Bayes certificates and inverse Bernoulli-KL endpoint
with separate code before comparing canonical and blind subprocess artifacts.
"""

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
LABS = ROOT / "00-知识库管理" / "_labs"
ASSESSMENT = LABS / "assessments" / "资格考 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）.md"
SOLUTION = LABS / "assessments" / "资格考解答 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 学习理论资格考 I 跨卷累计复现门.md"
GATE = LABS / "code" / "learning_theory_qualification_01_gate.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-learning-theory-qualification-01-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "e61df86632115cab0f592b07661abd9fdafa1c81f45fff9570ea51fb7274b7f6"
EXPECTED_BLIND_SHA256 = "45aa1b16b5a0f8e7ce1c5125e97414e0fc871b72af16a07c6e7bf8f9f73ab218"

CANONICAL_LINES = (
    "TRACK A d=5 target=3 enum_m=6 hypotheses=6 vc=1 growth=6 bayes=0.000000 class=0.000000 expected_emp=0.000000 expected_pop=0.062579 ghost=0.062579 stability=1.000000",
    "TRACK B cert_m=200 gibbs_emp=0.084000 gibbs_true=0.084000 finite=0.201054 compression=0.045162 kl=0.748346 pac=0.191657 joint_pac=0.202908",
    "TRACK C output_entropy=0.711929 info_radius=0.243572 output=0:0.004096,1:0.042560,2:0.215488,3:0.737856,4:0.000000,5:0.000000 routes=5 joint_delta=0.010000",
)

BLIND_ARGS = (
    "--domain-size", "6",
    "--target-threshold", "4",
    "--enumeration-size", "5",
    "--certificate-size", "240",
    "--delta", "0.08",
    "--prior", "0.1,0.1,0.1,0.15,0.2,0.15,0.2",
    "--posterior", "0.02,0.03,0.05,0.1,0.65,0.1,0.05",
    "--compression-bits", "2",
    "--route-count", "4",
)

BLIND_LINES = (
    "TRACK A d=6 target=4 enum_m=5 hypotheses=7 vc=1 growth=7 bayes=0.000000 class=0.000000 expected_emp=0.000000 expected_pop=0.094822 ghost=0.094822 stability=1.000000",
    "TRACK B cert_m=240 gibbs_emp=0.095000 gibbs_true=0.095000 finite=0.198730 compression=0.039300 kl=0.512753 pac=0.191608 joint_pac=0.200615",
    "TRACK C output_entropy=1.012295 info_radius=0.318166 output=0:0.004115,1:0.027135,2:0.100437,3:0.270190,4:0.598122,5:0.000000,6:0.000000 routes=4 joint_delta=0.020000",
)

PREREQUISITE_AUDITS = (
    ("learning_problem_decision_cumulative_contract_audit.py", "LT-CUM-01 material regression: PASS"),
    ("pac_finite_class_cumulative_contract_audit.py", "PAC-CUM-01 material regression: PASS"),
    ("vc_uniform_convergence_cumulative_contract_audit.py", "VC-CUM-01 material regression: PASS"),
    ("rademacher_margin_local_cumulative_contract_audit.py", "RAD-CUM-01 material regression: PASS"),
    ("algorithmic_generalization_cumulative_contract_audit.py", "PASS ALG-CUM-01 independent contract audit"),
)

STATE_SURFACES = (
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_ok(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(GATE), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(
        result.returncode == 0,
        f"gate failed for {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )
    return result


def run_rejected(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(GATE), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(result.returncode != 0, f"invalid contract was accepted: {' '.join(args)}")
    return result


def bernoulli_kl(left: float, right: float) -> float:
    if left == 0:
        return -math.log1p(-right)
    if left == 1:
        return -math.log(right)
    return left * math.log(left / right) + (1 - left) * math.log((1 - left) / (1 - right))


def inverse_kl(empirical: float, budget: float) -> float:
    lower, upper = empirical, 1.0 - 1e-15
    while upper - lower > 1e-14:
        midpoint = (lower + upper) / 2
        if bernoulli_kl(empirical, midpoint) <= budget:
            lower = midpoint
        else:
            upper = midpoint
    return lower


def independent_output_law(domain: int, target: int, sample_size: int) -> tuple[float, ...]:
    """Analytic maximum-negative formula, independent of sample enumeration."""
    positive_count = domain - target
    probabilities = [0.0] * (domain + 1)
    probabilities[0] = (positive_count / domain) ** sample_size
    for threshold in range(1, target + 1):
        upper = ((positive_count + threshold) / domain) ** sample_size
        lower = ((positive_count + threshold - 1) / domain) ** sample_size
        probabilities[threshold] = upper - lower
    require(math.isclose(sum(probabilities), 1.0, abs_tol=1e-14), "analytic output law does not sum to one")
    return tuple(probabilities)


def independent_erm(sample: tuple[int, ...], target: int) -> int:
    negatives = [point for point in sample if point < target]
    return 0 if not negatives else max(negatives) + 1


def independent_ghost(domain: int, target: int, sample_size: int) -> float:
    """Direct exchange table using a separately specified threshold learner."""
    total = 0
    sample_count = domain**sample_size
    for sample in itertools.product(range(domain), repeat=sample_size):
        original = independent_erm(sample, target)
        for index in range(sample_size):
            old_point = sample[index]
            original_loss = int((old_point >= original) != (old_point >= target))
            for replacement in range(domain):
                changed = sample[:index] + (replacement,) + sample[index + 1 :]
                changed_threshold = independent_erm(changed, target)
                changed_loss = int((old_point >= changed_threshold) != (old_point >= target))
                total += changed_loss - original_loss
    return total / (sample_count * sample_size * domain)


def independent_exact(domain: int, target: int, sample_size: int) -> dict[str, object]:
    probabilities = independent_output_law(domain, target, sample_size)
    population = sum(probability * abs(threshold - target) / domain
                     for threshold, probability in enumerate(probabilities))
    entropy = -sum(probability * math.log(probability)
                   for probability in probabilities if probability > 0)
    ghost = independent_ghost(domain, target, sample_size)
    # Witness: all target points versus one target-1 point. At x=0 loss flips.
    all_positive = (target,) * sample_size
    adjacent = (target - 1,) + (target,) * (sample_size - 1)
    left, right = independent_erm(all_positive, target), independent_erm(adjacent, target)
    witness_difference = abs(int((0 >= left) != (0 >= target)) - int((0 >= right) != (0 >= target)))
    require(witness_difference == 1, "independent stability witness failed")
    return {
        "probabilities": probabilities,
        "population": population,
        "ghost": ghost,
        "entropy": entropy,
        "information_radius": math.sqrt(entropy / (2 * sample_size)),
        "stability": float(witness_difference),
    }


def independent_certificates(
    domain: int,
    target: int,
    sample_size: int,
    delta: float,
    prior: tuple[float, ...],
    posterior: tuple[float, ...],
    bits: int,
    routes: int,
) -> dict[str, float]:
    risks = tuple(abs(threshold - target) / domain for threshold in range(domain + 1))
    empirical = sum(weight * risk for weight, risk in zip(posterior, risks))
    finite = empirical + math.sqrt(math.log(2 * (domain + 1) / delta) / (2 * sample_size))
    compression = (math.log(sample_size) + bits * math.log(2) + math.log(1 / delta)) / (sample_size - 1)
    divergence = sum(q * math.log(q / p) for p, q in zip(prior, posterior) if q > 0)
    budget = (divergence + math.log((sample_size + 1) / delta)) / sample_size
    joint_budget = (divergence + math.log((sample_size + 1) * routes / delta)) / sample_size
    return {
        "empirical": empirical,
        "finite": finite,
        "compression": compression,
        "kl": divergence,
        "pac": inverse_kl(empirical, budget),
        "joint_pac": inverse_kl(empirical, joint_budget),
    }


def audit_assessment_bundle() -> None:
    assessment, solution, experiment = read(ASSESSMENT), read(SOLUTION), read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        require("status: draft" in content, f"{label}: writing state changed")
        require("material_status: regression-passed" in content, f"{label}: material state changed")
        require("learning_status: not-attempted" in content, f"{label}: learner state changed")
        require("updated: 2026-08-28" in content, f"{label}: update date missing")
        require("LT-QUAL-01" in content, f"{label}: qualification ID missing")

    require("oral_limit_minutes: 30" in assessment, "oral time changed")
    require("time_limit_minutes: 300" in assessment and "sessions: 2" in assessment,
            "two-session closed-book contract changed")
    require("node_count: 40" in assessment and "LT-01—40" in assessment, "scope is not LT-01--40")
    for gate in ("LT-CUM-01", "PAC-CUM-01", "VC-CUM-01", "RAD-CUM-01", "ALG-CUM-01"):
        require(gate in assessment, f"missing prerequisite {gate}")

    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题：.*（(\d+)\s*分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题解答：.*（(\d+)\s*分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 11)), "assessment questions are not exactly 1--10")
    require(question_points == solution_points, "question and solution point ledgers differ")
    require(sum(question_points.values()) == 100, "qualification exam no longer totals 100 points")
    require("第 1 题解答" not in assessment, "answer leaked into question sheet")

    for marker in (
        "十二层跨卷证明账本", "30 分钟跨卷口试", "Session I", "Session II",
        "scorer nonce", "答案与输出隔离协议", "48 小时", "14 天", "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses marker: {marker}")
    for marker in (
        "口试参考要点", "ghost replacement identity", "finite → VC/growth → Rademacher",
        "information proof", "compression 与 PAC-Bayes", "instruction-tuned 模型协议",
        EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256, "不会推进个人学习状态",
    ):
        require(marker in solution, f"solution misses rubric marker: {marker}")
    for marker in (
        "三本互不混账", "推导必须先于 stdout", "scorer nonce", "共同模型",
        "全部样本、全部替换", "大样本证书账", "先路由，再比较", "非法合同注入",
        "个人 blind artifact", "48 小时", "14 天", EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256,
    ):
        require(marker in experiment, f"experiment misses marker: {marker}")
    print("PASS LT-QUAL-01 assessment: scope=LT-01--40, oral=30m, closed=2x150m, questions/answers=10/10, points=100")


def audit_independent_math() -> None:
    canonical = independent_exact(5, 3, 6)
    expected_probabilities = (0.004096, 0.04256, 0.215488, 0.737856, 0.0, 0.0)
    for actual, expected in zip(canonical["probabilities"], expected_probabilities):
        require(math.isclose(actual, expected, abs_tol=1e-12), "canonical output law mismatch")
    require(math.isclose(canonical["population"], 0.0625792, abs_tol=1e-12), "canonical population gap mismatch")
    require(math.isclose(canonical["ghost"], 0.0625792, abs_tol=1e-12), "canonical ghost mismatch")
    require(math.isclose(canonical["entropy"], 0.7119287491, abs_tol=1e-10), "canonical entropy mismatch")
    require(math.isclose(canonical["information_radius"], 0.2435721572, abs_tol=1e-10), "canonical information radius mismatch")

    cert = independent_certificates(
        5, 3, 200, 0.05,
        (1 / 6,) * 6,
        (0.02, 0.03, 0.10, 0.70, 0.10, 0.05),
        1, 5,
    )
    anchors = {
        "empirical": 0.084,
        "finite": 0.2010538223,
        "compression": 0.0451617931,
        "kl": 0.7483461792,
        "pac": 0.1916574890,
        "joint_pac": 0.2029084707,
    }
    for name, expected in anchors.items():
        require(math.isclose(cert[name], expected, abs_tol=1e-10), f"canonical {name} mismatch")
    require(cert["joint_pac"] >= cert["pac"], "selection budget failed monotonicity")

    blind = independent_exact(6, 4, 5)
    require(math.isclose(blind["population"], 0.0948216735, abs_tol=1e-10), "blind population mismatch")
    require(math.isclose(blind["ghost"], blind["population"], abs_tol=1e-12), "blind ghost identity mismatch")
    require(math.isclose(blind["entropy"], 1.0122954691, abs_tol=1e-10), "blind entropy mismatch")
    blind_cert = independent_certificates(
        6, 4, 240, 0.08,
        (0.1, 0.1, 0.1, 0.15, 0.2, 0.15, 0.2),
        (0.02, 0.03, 0.05, 0.1, 0.65, 0.1, 0.05),
        2, 4,
    )
    require(math.isclose(blind_cert["empirical"], 0.095, abs_tol=1e-12), "blind Gibbs risk mismatch")
    require(math.isclose(blind_cert["finite"], 0.1987302790, abs_tol=1e-10), "blind finite mismatch")
    require(math.isclose(blind_cert["compression"], 0.0392998407, abs_tol=1e-10), "blind compression mismatch")
    require(math.isclose(blind_cert["pac"], 0.1916075998, abs_tol=1e-10), "blind PAC mismatch")
    print("PASS independent math: output law + ghost + stability + entropy/MI + finite/compression/PAC-Bayes canonical/blind anchors")


def audit_generated_artifacts() -> None:
    require(sha256(SVG) == EXPECTED_CANONICAL_SHA256, "stored canonical SVG hash changed")
    ET.parse(SVG)
    with tempfile.TemporaryDirectory(prefix="lt-qual-audit-") as temporary:
        directory = Path(temporary)
        canonical_a = directory / "canonical-a.svg"
        canonical_b = directory / "canonical-b.svg"
        first = run_ok("--output", str(canonical_a))
        second = run_ok("--output", str(canonical_b))
        require(sha256(canonical_a) == EXPECTED_CANONICAL_SHA256, "generated canonical hash mismatch")
        require(sha256(canonical_b) == EXPECTED_CANONICAL_SHA256, "canonical double-run is nondeterministic")
        require(first.stdout == second.stdout.replace(str(canonical_b), str(canonical_a)), "canonical stdout changed across paths")
        for line in CANONICAL_LINES:
            require(line in first.stdout, f"canonical stdout misses: {line}")
        ET.parse(canonical_a)

        blind_path = directory / "blind.svg"
        blind = run_ok(*BLIND_ARGS, "--output", str(blind_path))
        require(sha256(blind_path) == EXPECTED_BLIND_SHA256, "blind SVG hash mismatch")
        for line in BLIND_LINES:
            require(line in blind.stdout, f"blind stdout misses: {line}")
        ET.parse(blind_path)
    print("PASS deterministic artifacts: canonical double-run + stored byte identity + cross-track blind stdout/SVG/XML/hash")


def audit_guards() -> None:
    stored_before = sha256(SVG)
    with tempfile.TemporaryDirectory(prefix="lt-qual-guard-") as temporary:
        directory = Path(temporary)
        cases = (
            ("noncanonical-no-output", ("--domain-size", "6")),
            ("enumeration-budget", ("--domain-size", "7", "--enumeration-size", "7", "--output", str(directory / "large.svg"))),
            ("certificate-divisibility", ("--certificate-size", "201", "--output", str(directory / "div.svg"))),
            ("target-range", ("--target-threshold", "8", "--output", str(directory / "target.svg"))),
            ("prior-mass", ("--prior", "0.1,0.1,0.1,0.1,0.1,0.1", "--output", str(directory / "prior.svg"))),
            ("posterior-mass", ("--posterior", "0.02,0.03,0.1,0.7,0.1,0.04", "--output", str(directory / "post.svg"))),
            ("support", ("--prior", "0,0.2,0.2,0.2,0.2,0.2", "--output", str(directory / "support.svg"))),
            ("canonical-overwrite", ("--domain-size", "6", "--prior", "0.142857142857,0.142857142857,0.142857142857,0.142857142857,0.142857142857,0.142857142857,0.142857142858", "--posterior", "0.1,0.1,0.1,0.1,0.2,0.2,0.2", "--output", str(SVG))),
        )
        for label, args in cases:
            result = run_rejected(*args)
            require(result.stderr.strip(), f"{label}: rejection has no diagnostic")
    require(sha256(SVG) == stored_before, "guard tests changed canonical SVG")
    print(f"PASS guards: invalid contracts rejected={len(cases)}, canonical asset preserved")


def audit_prerequisites_and_state() -> None:
    for script_name, marker in PREREQUISITE_AUDITS:
        script = LABS / "code" / script_name
        result = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True)
        require(result.returncode == 0, f"prerequisite audit failed: {script_name}\n{result.stdout}\n{result.stderr}")
        require(marker in result.stdout, f"prerequisite audit marker missing: {marker}")
    print("PASS prerequisites: LT/PAC/VC/RAD/ALG five material gates retained as regression prerequisites")

    for surface in STATE_SURFACES:
        content = read(surface)
        require("LT-QUAL-01" in content, f"state surface misses LT-QUAL-01: {surface.relative_to(ROOT)}")
        require("2/2" in content or "2 / 2" in content, f"state surface misses qualification material 2/2: {surface.relative_to(ROOT)}")
        require("0/2" in content or "0 / 2" in content, f"state surface misses personal qualification 0/2: {surface.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner status: {surface.relative_to(ROOT)}")
    print("PASS state surfaces: LT-QUAL-01 retained as first material prerequisite; qualification material now=2/2, personal=0/2/not-attempted")


def main() -> None:
    audit_assessment_bundle()
    audit_independent_math()
    audit_generated_artifacts()
    audit_guards()
    audit_prerequisites_and_state()
    print("LT-QUAL-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
