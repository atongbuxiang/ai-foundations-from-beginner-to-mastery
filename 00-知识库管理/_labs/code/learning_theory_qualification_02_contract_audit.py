#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for LT-QUAL-02."""

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
ASSESSMENT = LABS / "assessments" / "资格考 - 学习理论 II：从模型选择到深度泛化证据（20.6—20.10）.md"
SOLUTION = LABS / "assessments" / "资格考解答 - 学习理论 II：从模型选择到深度泛化证据（20.6—20.10）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 学习理论资格考 II 跨卷累计复现门.md"
GATE = LABS / "code" / "learning_theory_qualification_02_gate.py"
QUAL_01_AUDIT = LABS / "code" / "learning_theory_qualification_01_contract_audit.py"
DEEP_AUDIT = LABS / "code" / "deep_generalization_cumulative_contract_audit.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-learning-theory-qualification-02-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "7bfd9f947a3416dd9fbf7fb889d525128723e5702fcba343e65beba258d71563"
EXPECTED_BLIND_SHA256 = "1df68fb356beefc67fbd9bf54dbb50e77160ddbd080e8acf7c9b424e1e77d876"

CANONICAL_LINES = (
    "TRACK A source_brier=0.069250,0.091250,0.141250 target_brier=0.127000,0.057500,0.121250 target_cal_gap=0.340000,0.200000,0.265000 weights=0.250000,0.666667,1.500000,4.000000 ess_fraction=0.452830 source_winner=0 target_winner=1 effective_rank=1.275000,1.750000,1.020000",
    "TRACK B T=8 hedge_loss=0.857972 best=0.542500 regret=0.315472 final_probs=0.297629,0.421512,0.280858 target_policy_risk=0.073375 observed_ips=0.033313 max_joint_ratio=6.400000 observed_ess=2.631218 observed_ratios=0.035714,6.400000,0.111111,3.000000,1.333333,0.875000",
    "TRACK C min_norm=0.333333,0.333333,0.666667 min_length=0.816497 shifted_length=2.160247 train_residual=0.000000 null_test_gap=2.000000 sharpness=2.000000->16.062500 path=1.000000 kernel_eigenvalues=1.600000,0.400000 residual_final_norm=0.213056 feature_drift=0.325000 ntk_drift=0.084987 regime=feature-moving",
)

BLIND_ARGS = (
    "--source-probabilities", "0.5,0.2,0.2,0.1",
    "--target-probabilities", "0.1,0.1,0.3,0.5", "--labels", "0,0,1,1",
    "--model-probabilities", "0.05,0.25,0.75,0.5;0.3,0.4,0.9,0.95;0.1,0.55,0.65,0.9",
    "--representation-spectra", "5,1,0.2;2,1,0.25;3,0.1,0.02",
    "--online-contexts", "0,1,3,3,2,1,3,0,2", "--hedge-eta", "0.6",
    "--logging-policy", "0.75,0.15,0.1;0.55,0.3,0.15;0.35,0.45,0.2;0.15,0.55,0.3",
    "--target-policy", "0.1,0.75,0.15;0.1,0.75,0.15;0.1,0.8,0.1;0.05,0.85,0.1",
    "--logged-contexts", "0,3,1,2,3,0,2", "--logged-actions", "0,1,2,1,2,1,0",
    "--design", "2,0,1;0,1,1", "--responses", "1,2", "--null-shift", "1.5",
    "--rescale", "8", "--kernel-rho", "0.3", "--kernel-time", "2",
    "--initial-residual", "1,-1", "--particle-a", "0.8,-1.2",
    "--particle-w", "0.4,-0.3", "--particle-step", "0.1", "--particle-target", "0.8",
)

BLIND_LINES = (
    "TRACK A source_brier=0.051250,0.079250,0.091000 target_brier=0.150250,0.029250,0.073000 target_cal_gap=0.355000,0.125000,0.220000 weights=0.200000,0.500000,1.500000,5.000000 ess_fraction=0.331126 source_winner=0 target_winner=1 effective_rank=1.240000,1.625000,1.040000",
    "TRACK B T=9 hedge_loss=0.817734 best=0.527500 regret=0.290234 final_probs=0.294396,0.392064,0.313540 target_policy_risk=0.039850 observed_ips=0.047251 max_joint_ratio=7.727273 observed_ess=2.765490 observed_ratios=0.026667,7.727273,0.500000,2.666667,1.666667,1.000000,0.428571",
    "TRACK C min_norm=0.000000,1.000000,1.000000 min_length=1.414214 shifted_length=2.061553 train_residual=0.000000 null_test_gap=1.500000 sharpness=2.000000->64.015625 path=1.000000 kernel_eigenvalues=1.300000,0.700000 residual_final_norm=0.348741 feature_drift=0.129521 ntk_drift=0.027379 regime=feature-moving",
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: tuple[str, ...] | list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GATE), *args], cwd=ROOT,
        text=True, capture_output=True, check=check,
    )


def lines(stdout: str) -> tuple[str, ...]:
    return tuple(line for line in stdout.splitlines() if line.startswith("TRACK "))


def audit_assessment() -> None:
    assessment, solution, experiment = read(ASSESSMENT), read(SOLUTION), read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        require("status: draft" in content, f"{label}: draft boundary missing")
        require("material_status: regression-passed" in content, f"{label}: material state missing")
        require("learning_status: not-attempted" in content, f"{label}: learner boundary missing")
        require("LT-QUAL-02" in content, f"{label}: qualification id missing")
    require("scope: [LT-41—84]" in assessment and "node_count: 44" in assessment, "scope mismatch")
    require("oral_limit_minutes: 35" in assessment, "oral time mismatch")
    require("time_limit_minutes: 320" in assessment and "sessions: 2" in assessment, "session contract mismatch")
    for gate in ("MODEL-CUM-01", "REPR-CUM-01", "REL-CUM-01", "ONLINE-CUM-01", "DEEP-CUM-01"):
        require(gate in assessment, f"missing prerequisite gate: {gate}")
    questions = {int(i): int(p) for i, p in re.findall(r"^### 第 (\d+) 题：.*（(\d+) 分）$", assessment, re.M)}
    answers = {int(i): int(p) for i, p in re.findall(r"^## 第 (\d+) 题解答：.*（(\d+) 分）$", solution, re.M)}
    require(sorted(questions) == list(range(1, 11)), "assessment questions are not 1--10")
    require(questions == answers and sum(questions.values()) == 100, f"point/solution ledger mismatch: {questions} vs {answers}")
    for marker in ("attempt_id", "scorer nonce", "blind", "48 小时", "14 天", "not-attempted"):
        require(marker in assessment, f"assessment marker missing: {marker}")
    for marker in ("Canonical 回归输出", "固定 Blind 回归输出", EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256, "joint-ratio", "not-attempted"):
        require(marker in solution, f"solution marker missing: {marker}")
    for marker in ("十三层最小合同", "Canonical 复现", "固定跨卷 Blind", "输入与覆盖保护", "学习证据状态机", "48 小时", "14 天"):
        require(marker in experiment, f"experiment marker missing: {marker}")
    print("PASS LT-QUAL-02 assessment: scope=LT-41--84, oral=35m, closed=2x160m, questions/answers=10/10, points=100")


def independent_math() -> None:
    source = (0.4, 0.3, 0.2, 0.1)
    target = (0.1, 0.2, 0.3, 0.4)
    labels = (0, 0, 1, 1)
    models = (
        (0.1, 0.3, 0.7, 0.55),
        (0.25, 0.45, 0.85, 0.9),
        (0.05, 0.6, 0.6, 0.95),
    )
    source_risks = tuple(sum(q * (s - y) ** 2 for q, s, y in zip(source, model, labels)) for model in models)
    target_risks = tuple(sum(p * (s - y) ** 2 for p, s, y in zip(target, model, labels)) for model in models)
    require(all(math.isclose(x, y, abs_tol=1e-14) for x, y in zip(source_risks, (0.06925, 0.09125, 0.14125))), "source Brier mismatch")
    require(all(math.isclose(x, y, abs_tol=1e-14) for x, y in zip(target_risks, (0.127, 0.0575, 0.12125))), "target Brier mismatch")
    weights = tuple(p / q for p, q in zip(target, source))
    ess_fraction = 1 / sum(q * w * w for q, w in zip(source, weights))
    require(math.isclose(ess_fraction, 24 / 53, abs_tol=1e-14), "population ESS mismatch")
    require((5.1 / 4, 3.5 / 2, 3.06 / 3) == (1.275, 1.75, 1.02), "effective ranks mismatch")

    contexts = (0, 3, 1, 2, 3, 3, 1, 2)
    eta = 0.8
    cumulative = [0.0, 0.0, 0.0]
    hedge_loss = 0.0
    for context in contexts:
        raw = [math.exp(-eta * value) for value in cumulative]
        probabilities = [value / sum(raw) for value in raw]
        row = [(model[context] - labels[context]) ** 2 for model in models]
        hedge_loss += sum(p * loss for p, loss in zip(probabilities, row))
        cumulative = [old + loss for old, loss in zip(cumulative, row)]
    require(math.isclose(hedge_loss, 0.85797233796473, abs_tol=1e-14), "Hedge loss mismatch")
    require(all(math.isclose(x, y, abs_tol=1e-14) for x, y in zip(cumulative, (0.9775, 0.5425, 1.05))), "expert ledger mismatch")

    logging = ((.7, .2, .1), (.6, .3, .1), (.4, .4, .2), (.2, .5, .3))
    policy = ((.1, .7, .2), (.1, .7, .2), (.1, .8, .1), (.1, .8, .1))
    loss_table = tuple(tuple((model[x] - labels[x]) ** 2 for model in models) for x in range(4))
    true_risk = sum(target[x] * sum(policy[x][a] * loss_table[x][a] for a in range(3)) for x in range(4))
    require(math.isclose(true_risk, 0.073375, abs_tol=1e-14), "target policy risk mismatch")
    logged_contexts, logged_actions = (0, 3, 1, 2, 3, 0), (0, 1, 0, 1, 2, 1)
    ratios = tuple((target[x] / source[x]) * (policy[x][a] / logging[x][a]) for x, a in zip(logged_contexts, logged_actions))
    observed = sum(r * loss_table[x][a] for r, x, a in zip(ratios, logged_contexts, logged_actions)) / len(ratios)
    require(math.isclose(observed, 0.03331299603174602, abs_tol=1e-14), "observed IPS mismatch")
    require(math.isclose(max((target[x] / source[x]) * (policy[x][a] / logging[x][a]) for x in range(4) for a in range(3)), 6.4, abs_tol=1e-14), "max ratio mismatch")

    minimum = (1 / 3, 1 / 3, 2 / 3)
    require(math.isclose(math.sqrt(sum(value * value for value in minimum)), math.sqrt(2 / 3), abs_tol=1e-14), "min norm mismatch")
    require(math.isclose(math.sqrt(14 / 3), 2.160246899469287, abs_tol=1e-14), "null-shift norm mismatch")
    require(math.isclose(4 ** 2 + 4 ** -2, 16.0625, abs_tol=1e-14), "sharpness mismatch")
    plus, minus = math.exp(-4.8) / math.sqrt(2), math.exp(-1.2) / math.sqrt(2)
    final = ((plus + minus) / math.sqrt(2), (plus - minus) / math.sqrt(2))
    require(math.isclose(math.hypot(*final), 0.2130559574688107, abs_tol=1e-14), "kernel norm mismatch")
    next_a, next_w = (1.03125, -1.015625), (0.5625, -0.3125)
    feature_before = (0.5**2 + (-0.25)**2) / 2
    feature_after = sum(value * value for value in next_w) / 2
    ntk_before = (1**2 + 0.5**2 + (-1)**2 + (-0.25)**2) / 4
    ntk_after = sum(a * a + w * w for a, w in zip(next_a, next_w)) / 4
    require(math.isclose((feature_after - feature_before) / feature_before, 0.325, abs_tol=1e-14), "feature drift mismatch")
    require(math.isclose((ntk_after - ntk_before) / ntk_before, 0.08498733108108109, abs_tol=1e-14), "NTK drift mismatch")
    print("PASS independent math: source/target representation + online/OPE + interpolation/invariance/regime anchors")


def audit_compute() -> None:
    before = digest(SVG)
    require(before == EXPECTED_CANONICAL_SHA256, "stored canonical SVG hash mismatch")
    first, second = run(()), run(())
    require(lines(first.stdout) == CANONICAL_LINES == lines(second.stdout), "canonical stdout mismatch")
    require(digest(SVG) == EXPECTED_CANONICAL_SHA256 == before, "canonical double-run/hash mismatch")
    with tempfile.TemporaryDirectory(prefix="lt-qual-02-blind-") as directory:
        first_path, second_path = Path(directory) / "blind-1.svg", Path(directory) / "blind-2.svg"
        blind_first = run((*BLIND_ARGS, "--output", str(first_path)))
        blind_second = run((*BLIND_ARGS, "--output", str(second_path)))
        require(lines(blind_first.stdout) == BLIND_LINES == lines(blind_second.stdout), "blind stdout mismatch")
        require(digest(first_path) == EXPECTED_BLIND_SHA256 == digest(second_path), "blind double-run/hash mismatch")
        ET.parse(first_path)
    require(digest(SVG) == before, "blind run changed canonical SVG")
    print("PASS deterministic artifacts: canonical double-run + cross-volume blind stdout/SVG/XML/hash")


def audit_guards() -> None:
    before = digest(SVG)
    invalid = (
        ("--source-probabilities", "0.5,0.5,0,0"),
        ("--target-probabilities", "0.1,0.2,0.3"),
        ("--labels", "0,0,2,1"),
        ("--model-probabilities", "0.1,0.2,0.3,1.2;0.2,0.3,0.4,0.5"),
        ("--representation-spectra", "1,0;2,1;3,1"),
        ("--online-contexts", "0,4"),
        ("--hedge-eta", "0"),
        ("--logging-policy", "0.7,0.3,0;0.6,0.3,0.1;0.4,0.4,0.2;0.2,0.5,0.3"),
        ("--target-policy", "0.1,0.7;0.1,0.7;0.1,0.8;0.1,0.8"),
        ("--logged-actions", "0,1,3,1,2,1"),
        ("--design", "1,0;0,1"),
        ("--design", "1,0,0;2,0,0"),
        ("--rescale", "0"),
        ("--kernel-rho", "1"),
        ("--initial-residual", "0,0"),
        ("--particle-step", "0"),
    )
    with tempfile.TemporaryDirectory(prefix="lt-qual-02-guards-") as directory:
        for index, args in enumerate(invalid):
            result = run((*args, "--output", str(Path(directory) / f"invalid-{index}.svg")), check=False)
            require(result.returncode != 0, f"invalid contract accepted: {args}")
        require(run(("--hedge-eta", "0.7"), check=False).returncode != 0, "noncanonical no-output accepted")
        require(run(("--hedge-eta", "0.7", "--output", str(SVG)), check=False).returncode != 0, "canonical overwrite accepted")
    require(digest(SVG) == before, "guards changed canonical SVG")
    print(f"PASS guards: invalid contracts rejected={len(invalid) + 2}, canonical asset preserved")


def audit_svg() -> None:
    root = ET.parse(SVG).getroot()
    texts = " ".join((element.text or "") for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "source selection -> target risk and representation audit",
        "online routing -> off-policy deployment evidence",
        "training fit -> invariant mechanism and regime boundary",
        "source winner != target winner", "regret != target risk",
        "fit/dynamics/proxy != population explanation",
        "task · data · representation · model · selection",
    ):
        require(marker in texts, f"SVG marker missing: {marker}")
    print("PASS SVG semantics: three cross-volume panels and thirteen-layer evidence-boundary footer")


def audit_prerequisites_and_state() -> None:
    for script, marker in ((QUAL_01_AUDIT, "LT-QUAL-01 material regression: PASS"), (DEEP_AUDIT, "DEEP-CUM-01 material regression: PASS")):
        result = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True)
        require(result.returncode == 0, f"prerequisite audit failed: {script.name}\n{result.stdout}\n{result.stderr}")
        require(marker in result.stdout, f"prerequisite marker missing: {marker}")
    print("PASS prerequisites: LT-QUAL-01 and 20.6--20.10 material chains regressed; personal retained remains unmet")
    assessment = read(ASSESSMENT)
    require("LT-QUAL-01-and-five-volume-retained" in assessment, "personal prerequisite boundary missing")
    for surface in STATE_SURFACES:
        content = read(surface)
        require("LT-QUAL-02" in content, f"state surface misses LT-QUAL-02: {surface.relative_to(ROOT)}")
        require("2/2" in content or "2 / 2" in content, f"state surface misses qualification material 2/2: {surface.relative_to(ROOT)}")
        require("0/2" in content or "0 / 2" in content, f"state surface misses personal qualification 0/2: {surface.relative_to(ROOT)}")
        require("10/10" in content or "10 / 10" in content, f"state surface misses volume material 10/10: {surface.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner: {surface.relative_to(ROOT)}")
    print("PASS state surfaces: qualifications material=2/2, volume material=10/10, learner=0/2 and 0/10/not-attempted")


def main() -> None:
    audit_assessment()
    independent_math()
    audit_compute()
    audit_guards()
    audit_svg()
    audit_prerequisites_and_state()
    print("LT-QUAL-02 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
