#!/usr/bin/env python3
"""Independent material and deterministic-compute audit for MODEL-CUM-01."""

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
CHAPTER = ROOT / "20-学习理论" / "20.6-经典模型与模型选择"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = CHAPTER / "经典模型与模型选择 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 经典模型与模型选择（20.6）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 经典模型与模型选择（20.6）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 经典模型与模型选择累计复现门.md"
GATE = LABS / "code" / "classical_models_cumulative_gate.py"
SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory"
    / "plot-classical-models-cumulative-gate-v2.svg"
)

EXPECTED_CANONICAL_SHA256 = "52ef4fd81480840c81a20949b5e2e8445e9961d8d334cae9d9ce35c99d8be903"
EXPECTED_BLIND_SHA256 = "52fc707c402d51c5d40050b535f397dc4ed4607face58eac1df5c36843175f6f"

CANONICAL_LINES = (
    "TRACK A dim=3 sigma=0.500000 ols_expected=4.265625 best_lambda=1.000000 best_expected=0.395372 df=1.500000 selection=0:0.000000,0.25:0.250000,1:0.375000,4:0.375000 selected_true=0.407059 selected_val=0.298943 optimism=0.108117",
    "TRACK B tree_threshold=-1.500000 gini_gain=0.444444 svm_w=2.000000 svm_b=3.000000 margin=0.500000 logistic_c1=0.113810 logistic_c4=0.006051 bootstrap=46656 query=-2.250000 bag_prob=0.334898 member_var=0.222741 independent_var=0.008910 correlated_var=0.051676 boost_error=0.166667 alpha=0.804719 boost_z=0.745356 hard_weight=0.500000",
    "TRACK C pca_top=5.546470 pca_second=0.120197 eigengap=5.426274 top_vector=0.915348,0.402663 kmeans=0.666667 em_one=1.891605 em_final=1.987221 em_iterations=9 em_gain=2.742353 single_aic=30.269933 mix_aic=25.270108 single_bic=29.853452 mix_bic=25.061868 label_swap=0.000000",
)

BLIND_ARGS = (
    "--singular-values", "3,1,0.5",
    "--beta", "1.2,0.6,0.3",
    "--train-signs", "1,-1,1",
    "--lambdas", "0,0.2,0.8,3",
    "--sigma", "0.4",
    "--query", "-2.75",
    "--ensemble-members", "40",
    "--member-correlation", "0.1",
    "--em-initial-mean", "0.7",
)

BLIND_LINES = (
    "TRACK A dim=3 sigma=0.400000 ols_expected=0.817778 best_lambda=0.800000 best_expected=0.233610 df=1.712018 selection=0:0.000000,0.2:0.500000,0.8:0.250000,3:0.250000 selected_true=0.261739 selected_val=0.188393 optimism=0.073346",
    "TRACK B tree_threshold=-1.500000 gini_gain=0.444444 svm_w=2.000000 svm_b=3.000000 margin=0.500000 logistic_c1=0.113810 logistic_c4=0.006051 bootstrap=46656 query=-2.750000 bag_prob=0.087791 member_var=0.080084 independent_var=0.002002 correlated_var=0.009810 boost_error=0.166667 alpha=0.804719 boost_z=0.745356 hard_weight=0.500000",
    "TRACK C pca_top=5.546470 pca_second=0.120197 eigengap=5.426274 top_vector=0.915348,0.402663 kmeans=0.666667 em_one=1.762142 em_final=1.987221 em_iterations=10 em_gain=4.518791 single_aic=30.269933 mix_aic=25.270108 single_bic=29.853452 mix_bic=25.061868 label_swap=0.000000",
)

EXPECTED_NODES = {
    41: "偏差—方差—噪声分解",
    42: "正则化、交叉验证与模型选择",
    43: "线性回归的统计学习理论",
    44: "逻辑回归、复合损失与概率分类",
    45: "支持向量机、最大间隔与核方法",
    46: "核岭回归与 Gaussian Process 接口",
    47: "决策树、分裂准则与剪枝",
    48: "Bagging、Random Forest 与 Boosting",
    49: "PCA 的统计估计与主子空间风险",
    50: "K-Means、聚类风险与不可辨识性",
    51: "潜变量模型、混合模型与 EM",
    52: "模型可辨识性、选择与 Misspecification",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_gate(*args: str, success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(GATE), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if success:
        require(result.returncode == 0,
                f"gate failed: {' '.join(args)}\n{result.stdout}\n{result.stderr}")
    else:
        require(result.returncode != 0, f"invalid contract accepted: {' '.join(args)}")
        require(result.stderr.strip(), "invalid contract has no stderr diagnostic")
    return result


def ridge_ledger(
    singular: tuple[float, ...], beta: tuple[float, ...], sigma: float,
    lambdas: tuple[float, ...],
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    bias, variance, total, degrees = [], [], [], []
    for ridge in lambdas:
        current_bias = sum(
            ridge**2 * coefficient**2 / (value**2 + ridge) ** 2
            for value, coefficient in zip(singular, beta)
        )
        current_variance = sum(
            sigma**2 * value**2 / (value**2 + ridge) ** 2 for value in singular
        )
        bias.append(current_bias)
        variance.append(current_variance)
        total.append(current_bias + current_variance)
        degrees.append(sum(value**2 / (value**2 + ridge) for value in singular))
    return tuple(bias), tuple(variance), tuple(total), tuple(degrees)


def exact_selection(
    singular: tuple[float, ...], beta: tuple[float, ...], signs: tuple[int, ...],
    sigma: float, lambdas: tuple[float, ...],
) -> tuple[tuple[float, ...], float, float]:
    statistic = tuple(coefficient + sigma * sign / value
                      for coefficient, sign, value in zip(beta, signs, singular))
    candidates = tuple(tuple(
        value**2 * z / (value**2 + ridge) for value, z in zip(singular, statistic)
    ) for ridge in lambdas)
    dimension = len(beta)
    fresh = tuple(
        sum((prediction - coefficient) ** 2
            for prediction, coefficient in zip(candidate, beta)) / dimension + sigma**2
        for candidate in candidates
    )
    counts = [0] * len(lambdas)
    true_sum = validation_sum = 0.0
    for sign_vector in itertools.product((-1, 1), repeat=dimension):
        response = tuple(coefficient + sigma * sign
                         for coefficient, sign in zip(beta, sign_vector))
        losses = tuple(sum((prediction - target) ** 2
                           for prediction, target in zip(candidate, response)) / dimension
                       for candidate in candidates)
        chosen = min(range(len(lambdas)), key=lambda index: (losses[index], index))
        counts[chosen] += 1
        true_sum += fresh[chosen]
        validation_sum += losses[chosen]
    count = 2**dimension
    return tuple(value / count for value in counts), true_sum / count, validation_sum / count


def tree_and_bootstrap(query: float) -> tuple[float, float, float]:
    points = (-3.0, -2.0, -1.0, 1.0, 2.0, 3.0)
    labels = (0, 0, 1, 1, 1, 1)
    thresholds = (-4.0, -2.5, -1.5, 0.0, 1.5, 2.5, 4.0)

    def impurity(values: tuple[int, ...]) -> float:
        if not values:
            return 0.0
        probability = sum(values) / len(values)
        return 2 * probability * (1 - probability)

    parent = impurity(labels)
    gains = []
    for threshold in thresholds:
        left = tuple(label for point, label in zip(points, labels) if point < threshold)
        right = tuple(label for point, label in zip(points, labels) if point >= threshold)
        gains.append(parent - (len(left) * impurity(left) + len(right) * impurity(right)) / 6)
    best = max(range(len(thresholds)), key=lambda index: (gains[index], -index))
    positives = 0
    for sample in itertools.product(range(6), repeat=6):
        errors = [sum(int(points[index] >= threshold) != labels[index] for index in sample)
                  for threshold in thresholds]
        chosen = min(range(len(thresholds)), key=lambda index: (errors[index], index))
        positives += int(query >= thresholds[chosen])
    return thresholds[best], gains[best], positives / 6**6


def log_mixture(observations: tuple[float, ...], mean: float) -> float:
    return sum(math.log(
        (math.exp(-0.5 * (value - mean) ** 2)
         + math.exp(-0.5 * (value + mean) ** 2))
        / (2 * math.sqrt(2 * math.pi))
    ) for value in observations)


def em_independent(initial: float, tolerance: float = 1e-12) -> tuple[float, float, int, float]:
    observations = (-3.0, -2.0, -1.0, 1.0, 2.0, 3.0)

    def update(mean: float) -> float:
        weights = [math.exp(-0.5 * (value - mean) ** 2) for value in observations]
        alternatives = [math.exp(-0.5 * (value + mean) ** 2) for value in observations]
        responsibilities = [right / (right + left)
                            for right, left in zip(weights, alternatives)]
        return sum(weight * value for weight, value in zip(responsibilities, observations)) / sum(responsibilities)

    first = update(initial)
    mean = initial
    for iteration in range(1, 101):
        new = update(mean)
        if abs(new - mean) <= tolerance:
            mean = new
            break
        mean = new
    else:
        raise AssertionError("independent EM did not converge")
    return first, mean, iteration, log_mixture(observations, mean) - log_mixture(observations, initial)


def audit_node_bundle() -> None:
    discovered: dict[int, tuple[Path, str]] = {}
    for path in CHAPTER.glob("*.md"):
        content = read(path)
        match = re.search(r"^node_id:\s*LT-(\d{2})$", content, re.M)
        if match:
            discovered[int(match.group(1))] = (path, content)
    require(sorted(discovered) == list(range(41, 53)), "20.6 node IDs are not exactly LT-41--52")
    moc = read(MOC)
    for node_id, title in EXPECTED_NODES.items():
        path, content = discovered[node_id]
        require(path.stem == title, f"LT-{node_id}: path/title mismatch")
        require(f"# {title}" in content, f"LT-{node_id}: H1 mismatch")
        require("status: draft" in content, f"LT-{node_id}: writing state changed")
        require("figure:" in content and "-v2.svg" in content, f"LT-{node_id}: figure contract missing")
        require(f"| LT-{node_id} | [[{title}]]" in moc, f"LT-{node_id}: MOC row missing")
        exercise = LABS / "exercises" / f"习题 - {title}.md"
        solution = LABS / "solutions" / f"解答 - {title}.md"
        require(exercise.is_file(), f"LT-{node_id}: exercise missing")
        require(solution.is_file(), f"LT-{node_id}: solution missing")
    print("PASS LT-41--52 node bundle: 12/12 draft nodes, figures, exercises/solutions and MOC mappings")


def audit_assessment_bundle() -> None:
    assessment, solution, experiment = read(ASSESSMENT), read(SOLUTION), read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        require("status: draft" in content, f"{label}: writing state changed")
        require("material_status: regression-passed" in content, f"{label}: material state changed")
        require("learning_status: not-attempted" in content, f"{label}: learner state changed")
        require("MODEL-CUM-01" in content, f"{label}: ID missing")
        require("updated: 2026-08-28" in content, f"{label}: update date missing")
    require("formal_prerequisite: LT-QUAL-01-retained" in assessment, "formal prerequisite missing")
    require("time_limit_minutes: 240" in assessment and "oral_limit_minutes: 25" in assessment,
            "time contract changed")
    for node_id in range(41, 53):
        require(f"LT-{node_id}" in assessment, f"assessment scope misses LT-{node_id}")
    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题：.*（(\d+)\s*分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题解答：.*（(\d+)\s*分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 15)), "assessment questions are not exactly 1--14")
    require(question_points == solution_points, "question/solution point ledgers differ")
    require(sum(question_points.values()) == 100, "assessment no longer totals 100 points")
    require("第 1 题解答" not in assessment, "answer leaked into question sheet")
    for marker in (
        "答案与输出隔离协议", "25 分钟卷级口试", "240 分钟闭卷", "十层经典模型账本",
        "三轨参数化模型族", "scorer nonce", "评分门槛", "48 小时", "14 天", "提交证据清单",
    ):
        require(marker in assessment, f"assessment marker missing: {marker}")
    for marker in (
        "口试参考要点", "谱 ridge", "验证选择与 KRR–GP", "边界、树与集成",
        "PCA、K-Means、EM", "proper loss、margin 与 kernel", "十条声明",
        EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256, "不会推进该状态",
    ):
        require(marker in solution, f"solution marker missing: {marker}")
    for marker in (
        "执行顺序与防循环认证", "六层共同合同", "谱正则化与 validation selection",
        "边界、partition 与 ensemble", "PCA、K-Means、EM 与可辨识性",
        "固定三轨 blind fixture", "非法合同注入", "个人 blind artifact",
        EXPECTED_CANONICAL_SHA256, EXPECTED_BLIND_SHA256,
    ):
        require(marker in experiment, f"experiment marker missing: {marker}")
    print("PASS MODEL-CUM-01 assessment: scope=12/12, questions/solutions=14/14, points=100, oral/isolation/blind/delay gates")


def audit_independent_math() -> None:
    bias, variance, total, degrees = ridge_ledger(
        (4.0, 1.0, 0.25), (1.0, 0.8, 0.4), 0.5, (0.0, 0.25, 1.0, 4.0)
    )
    require(math.isclose(total[0], 4.265625, abs_tol=1e-12), "canonical OLS risk mismatch")
    require(math.isclose(bias[1], 0.1282366863905326, abs_tol=1e-12), "ridge bias mismatch")
    require(math.isclose(variance[2], 0.090181660899654, abs_tol=1e-12), "ridge variance mismatch")
    require(math.isclose(total[2], 0.3953719723183391, abs_tol=1e-12), "best ridge risk mismatch")
    require(math.isclose(degrees[2], 1.5, abs_tol=1e-12), "ridge df mismatch")
    require(all(left >= right for left, right in zip(degrees, degrees[1:])), "ridge df is not monotone")

    frequencies, selected_true, selected_validation = exact_selection(
        (4.0, 1.0, 0.25), (1.0, 0.8, 0.4), (-1, 1, -1), 0.5,
        (0.0, 0.25, 1.0, 4.0),
    )
    require(frequencies == (0.0, 0.25, 0.375, 0.375), "selection frequencies mismatch")
    require(math.isclose(selected_true, 0.407059175948486, abs_tol=1e-12), "selected true risk mismatch")
    require(math.isclose(selected_validation, 0.2989426601113819, abs_tol=1e-12), "selected validation mismatch")

    threshold, gain, probability = tree_and_bootstrap(-2.25)
    require(threshold == -1.5 and math.isclose(gain, 4 / 9, abs_tol=1e-12), "tree split mismatch")
    require(math.isclose(probability, 15625 / 46656, abs_tol=1e-12), "bootstrap probability mismatch")
    margins = (3, 1, 1, 5, 7, 9)
    logistic_one = sum(math.log1p(math.exp(-value)) for value in margins) / 6
    logistic_four = sum(math.log1p(math.exp(-4 * value)) for value in margins) / 6
    require(math.isclose(logistic_one, 0.11381015729046723, abs_tol=1e-12), "logistic c1 mismatch")
    require(math.isclose(logistic_four, 0.006051000348490417, abs_tol=1e-12), "logistic c4 mismatch")
    member_variance = probability * (1 - probability)
    require(math.isclose(member_variance / 25, 0.00890965287583076, abs_tol=1e-12), "independent ensemble mismatch")
    require(math.isclose(member_variance * (0.2 + 0.8 / 25), 0.0516759866798184, abs_tol=1e-12), "correlated ensemble mismatch")
    require(math.isclose(0.5 * math.log(5), 0.8047189562170503, abs_tol=1e-12), "boost alpha mismatch")

    trace, determinant = 17 / 3, 2 / 3
    discriminant = math.sqrt(trace**2 - 4 * determinant)
    pca_top, pca_second = (trace + discriminant) / 2, (trace - discriminant) / 2
    require(math.isclose(pca_top, 5.546470099349952, abs_tol=1e-12), "PCA top eigenvalue mismatch")
    require(math.isclose(pca_second, 0.1201965673167158, abs_tol=1e-12), "PCA second eigenvalue mismatch")
    first, final, iterations, gain_ll = em_independent(1.0)
    require(math.isclose(first, 1.8916045257225302, abs_tol=1e-12), "EM one-step mismatch")
    require(math.isclose(final, 1.9872206557397558, abs_tol=1e-12), "EM fixed point mismatch")
    require(iterations == 9, "EM iteration count mismatch")
    require(math.isclose(gain_ll, 2.742352969961732, abs_tol=1e-12), "EM gain mismatch")
    observations = (-3.0, -2.0, -1.0, 1.0, 2.0, 3.0)
    variance_single = sum(value**2 for value in observations) / 6
    single_ll = sum(-0.5 * (math.log(2 * math.pi * variance_single) + value**2 / variance_single)
                    for value in observations)
    require(math.isclose(-2 * single_ll + 4, 30.269932644138965, abs_tol=1e-12), "single AIC mismatch")
    require(math.isclose(-2 * log_mixture(observations, final) + 2, 25.2701081288579, abs_tol=1e-12), "mixture AIC mismatch")
    print("PASS independent math: ridge/selection + margin/tree/bootstrap/boost + PCA/KMeans/EM/AIC canonical anchors")


def audit_gate_runs() -> None:
    require(sha256(SVG) == EXPECTED_CANONICAL_SHA256, "stored canonical SVG hash changed")
    ET.parse(SVG)
    with tempfile.TemporaryDirectory(prefix="model-cum-audit-") as temporary:
        directory = Path(temporary)
        first_path, second_path = directory / "canonical-a.svg", directory / "canonical-b.svg"
        first = run_gate("--output", str(first_path))
        second = run_gate("--output", str(second_path))
        require(sha256(first_path) == EXPECTED_CANONICAL_SHA256, "generated canonical hash mismatch")
        require(sha256(second_path) == EXPECTED_CANONICAL_SHA256, "canonical double-run nondeterministic")
        for line in CANONICAL_LINES:
            require(line in first.stdout, f"canonical stdout missing: {line}")
        normalized_second = second.stdout.replace(str(second_path), str(first_path))
        require(first.stdout == normalized_second, "canonical stdout changes across output path")
        ET.parse(first_path)

        blind_path = directory / "blind.svg"
        blind = run_gate(*BLIND_ARGS, "--output", str(blind_path))
        require(sha256(blind_path) == EXPECTED_BLIND_SHA256, "blind hash mismatch")
        for line in BLIND_LINES:
            require(line in blind.stdout, f"blind stdout missing: {line}")
        ET.parse(blind_path)
    print("PASS deterministic compute: canonical double-run + cross-track blind stdout/SVG/XML/hash")


def audit_guards() -> None:
    before = sha256(SVG)
    with tempfile.TemporaryDirectory(prefix="model-cum-guard-") as temporary:
        directory = Path(temporary)
        eleven = ",".join("1" for _ in range(11))
        signs = ",".join("1" for _ in range(11))
        cases = (
            ("noncanonical-no-output", ("--query", "-2.75")),
            ("dimension-mismatch", ("--singular-values", "4,1", "--output", str(directory / "dim.svg"))),
            ("zero-singular", ("--singular-values", "4,1,0", "--output", str(directory / "zero.svg"))),
            ("negative-lambda", ("--lambdas", "0,-1", "--output", str(directory / "neg.svg"))),
            ("duplicate-lambda", ("--lambdas", "0,1,1", "--output", str(directory / "dup.svg"))),
            ("correlation", ("--member-correlation", "1.2", "--output", str(directory / "rho.svg"))),
            ("enumeration-budget", ("--singular-values", eleven, "--beta", eleven,
                                     "--train-signs", signs, "--output", str(directory / "large.svg"))),
            ("em-nonconvergence", ("--em-max-iterations", "1", "--em-tolerance", "1e-15",
                                   "--output", str(directory / "em.svg"))),
            ("canonical-overwrite", ("--query", "-2.75", "--output", str(SVG))),
        )
        for label, args in cases:
            result = run_gate(*args, success=False)
            if label not in ("noncanonical-no-output", "canonical-overwrite"):
                output_values = [Path(args[index + 1]) for index, value in enumerate(args[:-1]) if value == "--output"]
                require(not any(path.exists() for path in output_values), f"{label}: rejected run created artifact")
    require(sha256(SVG) == before, "guard suite changed canonical SVG")
    print(f"PASS guards: invalid contracts rejected={len(cases)}, canonical asset preserved")


def audit_svg_semantics() -> None:
    root = ET.parse(SVG).getroot()
    all_text = " ".join(element.text or "" for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "A | spectral procedure", "B | boundary and ensemble", "C | latent geometry",
        "exact validation-selection ledger", "hard-margin SVM", "AdaBoost round 1",
        "EM fixed point", "The six-layer classical-model audit", "optimization descent != population validity",
    ):
        require(marker in all_text, f"SVG semantic marker missing: {marker}")
    print("PASS SVG semantics: three estimand panels, selection ledger and evidence-boundary footer")


def audit_prerequisite_and_state() -> None:
    prerequisite = LABS / "code" / "learning_theory_qualification_01_contract_audit.py"
    result = subprocess.run([sys.executable, str(prerequisite)], cwd=ROOT, text=True, capture_output=True)
    require(result.returncode == 0, f"LT-QUAL-01 material prerequisite failed\n{result.stdout}\n{result.stderr}")
    require("LT-QUAL-01 material regression: PASS" in result.stdout, "qualification prerequisite marker missing")
    require("PERSONAL LEARNING STATUS: not-attempted" in result.stdout,
            "qualification audit unexpectedly claims personal retained")
    print("PASS prerequisite boundary: LT-QUAL-01 material regressed, personal prerequisite remains unmet/not-attempted")

    for path in STATE_SURFACES:
        content = read(path)
        require("MODEL-CUM-01" in content, f"state surface misses MODEL-CUM-01: {path.relative_to(ROOT)}")
        require(re.search(r"8\s*/\s*10", content) is not None or path == MOC,
                f"state surface misses 8/10 material count: {path.relative_to(ROOT)}")
        require(re.search(r"0\s*/\s*10", content) is not None,
                f"state surface misses 0/10 learner count: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims learner status: {path.relative_to(ROOT)}")
    print("PASS state surfaces: MODEL-CUM-01 retained as prerequisite, current material=8/10, learner=0/10/not-attempted")


def main() -> None:
    audit_node_bundle()
    audit_assessment_bundle()
    audit_independent_math()
    audit_gate_runs()
    audit_guards()
    audit_svg_semantics()
    audit_prerequisite_and_state()
    print("MODEL-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
