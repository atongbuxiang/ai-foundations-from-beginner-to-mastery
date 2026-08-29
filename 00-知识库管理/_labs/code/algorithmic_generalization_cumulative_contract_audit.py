#!/usr/bin/env python3
"""Independent material and reproducibility audit for ALG-CUM-01."""

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
CHAPTER = ROOT / "20-学习理论" / "20.5-稳定性、压缩、PAC-Bayes与信息泛化"
MOC = CHAPTER / "稳定性、压缩、PAC-Bayes 与信息泛化 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 稳定性、压缩、PAC-Bayes 与信息泛化累计复现门.md"
GATE_SCRIPT = LABS / "code" / "algorithmic_generalization_cumulative_gate.py"
CANONICAL_SVG = (
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-algorithmic-generalization-cumulative-gate-v2.svg"
)

CANONICAL_SHA256 = "ef8b95b87a1595550669fc4a1db3d623f8f4d6ad5c7ee7463eae5e06498fd6a6"
BLIND_SHA256 = "e6a4bd8767c33414445f9b7920e5ddf5cbd11f5577ff5a00ac80b44f22df7736"

BLIND_ARGS = (
    "--stability-size", "16",
    "--bernoulli-p", "0.3",
    "--lipschitz", "1.2",
    "--regularization", "3",
    "--step-sizes", "0.1,0.08,0.04",
    "--certificate-size", "160",
    "--compression-k", "4",
    "--message-bits", "5",
    "--delta", "0.08",
    "--prior", "0.6,0.4",
    "--posterior", "0.75,0.25",
    "--empirical-risks", "0.04,0.3",
    "--information-size", "160",
    "--channel-accuracy", "0.7",
    "--route-count", "4",
)

EXPECTED_CANONICAL_LINES = (
    "TRACK A m=20 exact_beta=0.097500 expected_gap=0.025000 rerm_beta=0.050000 sgd_beta=0.050000 step_sum=0.500000",
    "TRACK B m=200 compression=0.137071 empirical_gibbs=0.043000 posterior_kl=0.116322 kl_budget=0.042077 inverse_kl=0.127958 pinsker=0.188046 joint_inverse_kl=0.138265",
    "TRACK C m=200 accuracy=0.800000 exact_mi=0.192745 bit_budget=0.693147 exact_radius=0.021951 bit_radius=0.041628 routes=5 joint_delta=0.010000",
)

EXPECTED_BLIND_LINES = (
    "TRACK A m=16 exact_beta=0.121094 expected_gap=0.026250 rerm_beta=0.060000 sgd_beta=0.039600 step_sum=0.220000",
    "TRACK B m=160 compression=0.147925 empirical_gibbs=0.105000 posterior_kl=0.049857 kl_budget=0.047856 inverse_kl=0.223594 pinsker=0.259687 joint_inverse_kl=0.235887",
    "TRACK C m=160 accuracy=0.700000 exact_mi=0.082283 bit_budget=0.693147 exact_radius=0.016035 bit_radius=0.046541 routes=4 joint_delta=0.020000",
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
        require(result.returncode != 0, f"gate accepted invalid contract: {' '.join(args)}")
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


def independent_mean_anchors(sample_size: int, probability: float) -> tuple[float, float]:
    beta = 0.0
    expected_gap = 0.0
    for successes in range(sample_size):
        left = successes / sample_size
        right = (successes + 1) / sample_size
        for test_value in (0.0, 1.0):
            beta = max(
                beta,
                abs((left - test_value) ** 2 - (right - test_value) ** 2),
            )
    for successes in range(sample_size + 1):
        weight = successes / sample_size
        population = probability * (1 - weight) ** 2 + (1 - probability) * weight**2
        empirical = weight * (1 - weight) ** 2 + (1 - weight) * weight**2
        mass = (
            math.comb(sample_size, successes)
            * probability**successes
            * (1 - probability) ** (sample_size - successes)
        )
        expected_gap += mass * (population - empirical)
    return beta, expected_gap


def binary_kl(left: float, right: float) -> float:
    if left == 0:
        return -math.log(1 - right)
    if left == 1:
        return -math.log(right)
    return left * math.log(left / right) + (1 - left) * math.log((1 - left) / (1 - right))


def independent_inverse_kl(empirical: float, budget: float) -> float:
    low, high = empirical, 1 - 1e-15
    for _ in range(140):
        middle = (low + high) / 2
        if binary_kl(empirical, middle) <= budget:
            low = middle
        else:
            high = middle
    return low


def independent_description_anchors(
    sample_size: int,
    compression_k: int,
    message_bits: int,
    delta: float,
    prior: tuple[float, ...],
    posterior: tuple[float, ...],
    empirical_risks: tuple[float, ...],
    route_count: int,
) -> tuple[float, float, float, float, float, float]:
    compression = (
        math.log(math.comb(sample_size, compression_k))
        + message_bits * math.log(2)
        + math.log(1 / delta)
    ) / (sample_size - compression_k)
    empirical = sum(q * risk for q, risk in zip(posterior, empirical_risks))
    posterior_kl = sum(q * math.log(q / p) for p, q in zip(prior, posterior) if q)
    budget = (posterior_kl + math.log((sample_size + 1) / delta)) / sample_size
    inverse = independent_inverse_kl(empirical, budget)
    pinsker = min(1.0, empirical + math.sqrt(budget / 2))
    joint_budget = (
        posterior_kl + math.log((sample_size + 1) * route_count / delta)
    ) / sample_size
    joint_inverse = independent_inverse_kl(empirical, joint_budget)
    return compression, empirical, posterior_kl, budget, inverse, pinsker, joint_inverse


def independent_channel_anchors(
    accuracy: float, sample_size: int
) -> tuple[float, float, float, float]:
    joint = (
        (0.0, 0.0, 0.5 * accuracy),
        (0.0, 1.0, 0.5 * (1 - accuracy)),
        (1.0, 0.0, 0.5 * (1 - accuracy)),
        (1.0, 1.0, 0.5 * accuracy),
    )
    x_marginal = {0.0: 0.5, 1.0: 0.5}
    w_marginal = {0.0: 0.5, 1.0: 0.5}
    mutual_information = sum(
        mass * math.log(mass / (x_marginal[x] * w_marginal[w]))
        for x, w, mass in joint
        if mass > 0
    )
    bit_budget = math.log(2)
    return (
        mutual_information,
        bit_budget,
        math.sqrt(mutual_information / (2 * sample_size)),
        math.sqrt(bit_budget / (2 * sample_size)),
    )


def audit_node_bundle() -> None:
    files = sorted(path for path in CHAPTER.glob("*.md") if path != MOC)
    require(len(files) == 8, f"expected 8 LT-33--40 nodes, found {len(files)}")
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
        require("![[" in content and "> [!figure]" in content, f"visual contract missing: {path.name}")
    require(sorted(found) == list(range(33, 41)), f"scope changed: {sorted(found)}")
    moc = read(MOC)
    for node_id in range(33, 41):
        require(re.search(rf"^\| LT-{node_id:02d} \|", moc, re.M) is not None, f"MOC misses LT-{node_id:02d}")
    print("PASS LT-33--40 node bundle: 8/8 unique draft nodes, visuals and MOC mappings")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        frontmatter = parse_frontmatter(content)
        require(frontmatter.get("status") == "draft", f"{label}: status must remain draft")
        require(frontmatter.get("material_status") == "regression-passed", f"{label}: material status changed")
        require(frontmatter.get("learning_status") == "not-attempted", f"{label}: learner status changed")
        require(frontmatter.get("assessment_id") == "ALG-CUM-01", f"{label}: assessment ID changed")
        require(frontmatter.get("updated") == "2026-08-28", f"{label}: date changed")
    require("time_limit_minutes: 210" in assessment, "assessment duration changed")
    for node_id in range(33, 41):
        require(f"LT-{node_id:02d}" in assessment, f"assessment scope misses LT-{node_id:02d}")
    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题：.*（(\d+)\s*分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题解答：.*（(\d+)\s*分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 15)), "question sheet does not contain questions 1--14")
    require(question_points == solution_points, "question/solution points differ")
    require(sum(question_points.values()) == 100, "assessment does not total 100 points")
    for marker in (
        "20 分钟卷级口试",
        "210 分钟闭卷",
        "三轨参数化模型族",
        "八层算法依赖泛化证明账本",
        "答案与输出隔离协议",
        "scorer nonce",
        "48 小时与 14 天复测",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses marker: {marker}")
    for marker in ("口试评分参考", "实验复现与延迟门参考", "状态边界"):
        require(marker in solution, f"solution misses marker: {marker}")
    require("第 1 题解答" not in assessment, "answer leaked into question sheet")
    require("才可打开本页或 canonical stdout" in solution, "solution isolation warning missing")
    print("PASS assessment bundle: scope=8/8, questions/solutions=14/14, points=100, isolation + delay gates")


def audit_experiment_contract() -> None:
    content = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "三轨统一对象合同",
        "轨道 A：replace-one、RERM 与 SGD",
        "轨道 B：compression 与 PAC-Bayes",
        "轨道 C：information 与证书选择",
        "评分者随机指定、跨轨盲参与防挑题协议",
        "盲参数干预怎样才算独立",
        "独立审计固定 fixture",
        "证据状态机",
        CANONICAL_SHA256,
        BLIND_SHA256,
    ):
        require(marker in content, f"experiment misses marker: {marker}")
    require("无 Monte Carlo" in content, "experiment must state deterministic status")
    require("不能直接取 minimum" in content, "cross-certificate selection boundary missing")
    print("PASS experiment contract: deterministic three tracks, isolation, blind and state-machine markers")


def audit_independent_canonical_math() -> None:
    beta, gap = independent_mean_anchors(20, 0.5)
    require(math.isclose(beta, 0.0975, abs_tol=1e-12), "canonical exact beta changed")
    require(math.isclose(gap, 0.025, abs_tol=1e-12), "canonical expected gap changed")
    rerm = 2 * 1.0**2 / (2.0 * 20)
    sgd = 2 * 1.0**2 * sum((0.2, 0.15, 0.1, 0.05)) / 20
    require(math.isclose(rerm, 0.05, abs_tol=1e-12), "canonical RERM anchor changed")
    require(math.isclose(sgd, 0.05, abs_tol=1e-12), "canonical SGD anchor changed")
    description = independent_description_anchors(
        200, 5, 3, 0.05, (0.7, 0.3), (0.9, 0.1), (0.02, 0.25), 5
    )
    expected_description = (
        0.13707122914044795,
        0.043,
        0.1163217565860046,
        0.04207679469099535,
        0.12795813838284636,
        0.1880461903860204,
        0.13826497355984474,
    )
    for actual, expected in zip(description, expected_description):
        require(math.isclose(actual, expected, rel_tol=0, abs_tol=1e-12), "canonical description anchor changed")
    information = independent_channel_anchors(0.8, 200)
    expected_information = (
        0.19274475702175753,
        0.6931471805599453,
        0.021951352863875927,
        0.041627730557884886,
    )
    for actual, expected in zip(information, expected_information):
        require(math.isclose(actual, expected, rel_tol=0, abs_tol=1e-12), "canonical information anchor changed")
    print("PASS independent canonical math: stability, compression, PAC-Bayes and channel MI")


def audit_gate_runs() -> None:
    require(GATE_SCRIPT.is_file(), "gate script missing")
    require(CANONICAL_SVG.is_file(), "canonical SVG missing")
    require(sha256(CANONICAL_SVG) == CANONICAL_SHA256, "stored canonical SVG hash changed")
    with tempfile.TemporaryDirectory(prefix="alg-cum-audit-") as directory:
        temp = Path(directory)
        canonical_one = temp / "canonical-one.svg"
        canonical_two = temp / "canonical-two.svg"
        blind_one = temp / "blind-one.svg"
        blind_two = temp / "blind-two.svg"
        first = run("--output", str(canonical_one))
        second = run("--output", str(canonical_two))
        blind_first = run(*BLIND_ARGS, "--output", str(blind_one))
        blind_second = run(*BLIND_ARGS, "--output", str(blind_two))
        require(tuple(first.stdout.splitlines()[:3]) == EXPECTED_CANONICAL_LINES, "canonical stdout changed")
        require(tuple(second.stdout.splitlines()[:3]) == EXPECTED_CANONICAL_LINES, "canonical repeat stdout changed")
        require(tuple(blind_first.stdout.splitlines()[:3]) == EXPECTED_BLIND_LINES, "blind stdout changed")
        require(tuple(blind_second.stdout.splitlines()[:3]) == EXPECTED_BLIND_LINES, "blind repeat stdout changed")
        require(canonical_one.read_bytes() == canonical_two.read_bytes(), "canonical generation is nondeterministic")
        require(canonical_one.read_bytes() == CANONICAL_SVG.read_bytes(), "stored canonical differs from generated")
        require(blind_one.read_bytes() == blind_two.read_bytes(), "blind generation is nondeterministic")
        require(sha256(canonical_one) == CANONICAL_SHA256, "canonical generated hash changed")
        require(sha256(blind_one) == BLIND_SHA256, "blind generated hash changed")
        for path in (canonical_one, canonical_two, blind_one, blind_two):
            root = ET.parse(path).getroot()
            require(root.tag.endswith("svg"), f"not an SVG: {path.name}")
            require(root.attrib.get("viewBox") == "0 0 1540 990", f"SVG dimensions changed: {path.name}")
    print("PASS gate runs: canonical/blind double-run, stdout, SVG/XML and hashes")


def audit_input_guards() -> None:
    with tempfile.TemporaryDirectory(prefix="alg-cum-guards-") as directory:
        temp = Path(directory)
        run("--stability-size", "21", expect_success=False)
        run(
            "--certificate-size", "20", "--compression-k", "20",
            "--output", str(temp / "bad-k.svg"), expect_success=False,
        )
        run(
            "--bernoulli-p", "1.2",
            "--output", str(temp / "bad-probability.svg"), expect_success=False,
        )
        run(
            "--prior", "1,0", "--posterior", "0.9,0.1",
            "--output", str(temp / "bad-support.svg"), expect_success=False,
        )
        run(
            "--posterior", "0.8,0.3",
            "--output", str(temp / "bad-mass.svg"), expect_success=False,
        )
        before = CANONICAL_SVG.read_bytes()
        run(
            "--stability-size", "21", "--output", str(CANONICAL_SVG),
            expect_success=False,
        )
        require(CANONICAL_SVG.read_bytes() == before, "canonical SVG changed after overwrite attempt")
    script = read(GATE_SCRIPT)
    for marker in (
        "noncanonical parameters require --output",
        "noncanonical parameters may not target the canonical SVG",
        "posterior must be absolutely continuous with respect to prior",
        "compression-k must satisfy 0 <= k < certificate-size",
    ):
        require(marker in script, f"gate guard missing: {marker}")
    print("PASS input guards: output isolation, probabilities, compression and PAC-Bayes support")


def audit_svg_semantics() -> None:
    root = ET.parse(CANONICAL_SVG).getroot()
    all_text = " ".join(element.text or "" for element in root.iter() if element.tag.endswith("text"))
    for marker in (
        "A | one sample changes",
        "B | short / nearby description",
        "C | how much sample information",
        "exact β",
        "PAC-Bayes inverse-kl",
        "exact I(X;W)",
        "Do not take a post-hoc minimum",
        "expected signed gap",
    ):
        require(marker in all_text, f"SVG semantic marker missing: {marker}")
    print("PASS SVG semantics: three panels, statement types and no-post-hoc-minimum warning")


def audit_state_surfaces() -> None:
    for path in STATE_SURFACES:
        content = read(path)
        require("ALG-CUM-01" in content, f"state surface misses ALG-CUM-01: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface misses learner boundary: {path.relative_to(ROOT)}")
        require(
            "9/10" in content or "9 / 10" in content or path == MOC,
            f"state surface misses 9/10 material count: {path.relative_to(ROOT)}",
        )
    chapter_moc = read(MOC)
    require("regression-passed" in chapter_moc, "chapter MOC misses material state")
    require("0/8 经真实作答验收" in chapter_moc, "chapter learner count changed")
    print("PASS state surfaces: ALG-CUM-01 synchronized, current material=9/10 and learner=not-attempted")


def main() -> None:
    audit_node_bundle()
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_independent_canonical_math()
    audit_gate_runs()
    audit_input_guards()
    audit_svg_semantics()
    audit_state_surfaces()
    print("PASS ALG-CUM-01 independent contract audit")


if __name__ == "__main__":
    main()
