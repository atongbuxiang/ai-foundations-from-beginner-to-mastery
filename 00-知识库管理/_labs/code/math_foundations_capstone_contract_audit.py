#!/usr/bin/env python3
"""Independent material and compute audit for MATH-FND-CAP-01."""

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
ASSESSMENT = LABS / "assessments" / "数学基础十卷总验收 - 跨卷理论与 AI 迁移.md"
SOLUTION = LABS / "assessments" / "数学基础十卷总验收解答 - 跨卷理论与 AI 迁移.md"
EXPERIMENT = LABS / "experiments" / "实验 - 数学基础十卷跨章累计复现门.md"
CAP_SCRIPT = LABS / "code" / "plot_math_foundations_capstone_gate.py"
CAP_SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "math-foundations"
    / "plot-math-foundations-capstone-gate-v2.svg"
)
EXPECTED_CAP_SHA256 = "d5e79545ee9820bcbf18e1444890e8e462bd186b1720f2d0fd262508404ac18c"
EXPECTED_BLIND_SHA256 = "697c860c0b94fbb7660199ffc1503b862d47ce14b04ea317d39235abc8223e53"

PREREQUISITE_AUDITS = (
    ("math_foundations_cumulative_contract_audit.py", "MATH-CUM-01 material regression: PASS"),
    ("linear_algebra_cumulative_contract_audit.py", "LA-CUM-01 material regression: PASS"),
    ("matrix_analysis_cumulative_contract_audit.py", "MA-CUM-01 material regression: PASS"),
    ("calculus_ad_cumulative_contract_audit.py", "CALC-CUM-01 material regression: PASS"),
    ("probability_cumulative_contract_audit.py", "PROB-CUM-01 material regression: PASS"),
    ("information_cumulative_contract_audit.py", "INFO-CUM-01 material regression: PASS"),
    ("optimization_cumulative_contract_audit.py", "OPT-CUM-01 material regression: PASS"),
    ("numerical_cumulative_contract_audit.py", "NLA-CUM-01 material regression: PASS"),
    ("dynamics_cumulative_contract_audit.py", "DYN-CUM-01 material regression: PASS"),
    ("geometry_functional_cumulative_contract_audit.py", "GEO-CUM-01 material regression: PASS"),
)

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    ROOT / "00-知识库管理" / "00-总览" / "数学基础十卷完备性审计与学习状态总表.md",
    LABS / "exercises" / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(script: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(
        result.returncode == 0,
        f"subprocess failed: {script.relative_to(ROOT)} {' '.join(args)}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )
    return result.stdout.strip()


def active_lines(content: str) -> list[str]:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence = True, marker
            elif marker == fence:
                in_fence, fence = False, ""
            continue
        if not in_fence:
            output.append(line)
    return output


def audit_assessment_bundle() -> None:
    assessment, solution, experiment = read(ASSESSMENT), read(SOLUTION), read(EXPERIMENT)
    for content, label in (
        (assessment, "assessment"),
        (solution, "solution"),
        (experiment, "experiment"),
    ):
        require("status: draft" in content, f"{label}: document writing state changed")
        require("material_status: regression-passed" in content, f"{label}: material state changed")
        require("learning_status: not-attempted" in content, f"{label}: personal state changed")
        require("updated: 2026-08-28" in content, f"{label}: migration date missing")

    for content, label in ((assessment, "assessment"), (solution, "solution")):
        require("assessment_id: MATH-FND-CAP-01" in content, f"{label}: capstone ID changed")
    require("time_limit_minutes: 360" in assessment and "sessions: 2" in assessment,
            "two-session time contract changed")
    for scope in (
        "MATH-01—08", "LA-01—24", "MA-01—16", "CALC-01—16", "PROB-01—20",
        "INFO-01—10", "OPT-01—16", "NUM-01—20", "DYN-01—12", "GEO-01—08",
    ):
        require(scope in assessment, f"assessment scope misses {scope}")
    for index in range(1, 12):
        require(re.search(rf"^### 第\s*{index}\s*题：", assessment, re.M) is not None,
                f"assessment misses question {index}")
        require(re.search(rf"^### 第\s*{index}\s*题解答：", solution, re.M) is not None,
                f"solution misses answer {index}")

    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题：.*（(\d+)\s*分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题解答：.*（(\d+)\s*分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 12)), "assessment point headers incomplete")
    require(question_points == solution_points, "question/solution point allocations differ")
    require(sum(question_points.values()) == 100, "capstone no longer totals 100 points")

    for marker in (
        "先看完整验收时间线",
        "十卷前置证据矩阵",
        "三波参数化系统族",
        "十二层跨卷对象—证据账本",
        "答案与输出隔离协议",
        "30 分钟跨卷口试",
        "scorer nonce",
        "48 小时换系统重建门",
        "14 天陌生 AI 综合迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses capstone marker: {marker}")
    for marker in (
        "十卷前置证据判分",
        "跨卷口试参考要点",
        "十二层跨卷对象—证据账本参考",
        "三波参数化系统族的数值锚点",
        "实验复现门与 nonce 判分红线",
        "从总卷 `retained` 到课程证据",
        "最终状态边界",
    ):
        require(marker in solution, f"solution misses capstone rubric: {marker}")
    require("第 1 题解答" not in assessment, "answer content leaked into question sheet")
    require("才可打开本解答或canonical结果" in solution, "solution use-order warning incomplete")
    print("PASS capstone assessment: ten-volume scope, questions/answers 11/11, points=100, oral + isolation + delay gates")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "评分者随机指定、跨轨盲参与防挑题协议",
        "防止循环认证",
        "评分者随机指定的盲手工复核",
        "盲参数干预门",
        "盲测干预怎样才算独立",
        "审计使用的固定三轨盲测 fixture",
        "--variance-x",
        "--lambda-min",
        "--circle-radius",
        "证据状态机",
        "48 小时换系统与 14 天迁移",
        EXPECTED_CAP_SHA256,
        EXPECTED_BLIND_SHA256,
    ):
        require(marker in experiment, f"experiment misses capstone marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    print("PASS capstone experiment: parameterized A/B/C systems, scorer nonce, blind fixture and state machine")


def gaussian_anchor(
    variance_x: float,
    variance_y: float,
    observation_x: float,
    observation_y: float,
    noise: float,
) -> tuple[float, float, float, float]:
    signal = variance_x * observation_x**2 + variance_y * observation_y**2
    sigma_c_norm_sq = (
        (variance_x * observation_x) ** 2 + (variance_y * observation_y) ** 2
    )
    total = signal + noise
    mi = 0.5 * math.log(total / noise)
    trace = variance_x + variance_y - sigma_c_norm_sq / total
    determinant = variance_x * variance_y * noise / total
    return signal, mi, trace, determinant


def solve_linear(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    augmented = [row[:] + [rhs] for row, rhs in zip(matrix, vector)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        require(abs(augmented[pivot][column]) > 1e-14, "independent KRR solve became singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        for row in range(column + 1, size):
            factor = augmented[row][column] / augmented[column][column]
            for item in range(column, size + 1):
                augmented[row][item] -= factor * augmented[column][item]
    solution = [0.0] * size
    for row in range(size - 1, -1, -1):
        solution[row] = (
            augmented[row][size]
            - sum(augmented[row][column] * solution[column] for column in range(row + 1, size))
        ) / augmented[row][row]
    return solution


def krr_anchor(
    radius: float,
    lengthscale: float,
    ridge: float,
    cos_frequency: int,
    sin_frequency: int,
    amplitude: float,
) -> tuple[float, float, float]:
    size = 48
    points = [2 * math.pi * index / size for index in range(size)]

    def kernel(left: float, right: float) -> float:
        chord_sq = 2 * radius**2 * (1 - math.cos(left - right))
        return math.exp(-chord_sq / (2 * lengthscale**2))

    def target(theta: float) -> float:
        return math.cos(cos_frequency * theta) + amplitude * math.sin(sin_frequency * theta)

    gram = [[kernel(left, right) for right in points] for left in points]
    system = [[gram[i][j] + (ridge if i == j else 0.0) for j in range(size)] for i in range(size)]
    coefficients = solve_linear(system, [target(theta) for theta in points])
    squared_error = 0.0
    for index in range(360):
        theta = 2 * math.pi * (index + 0.5) / 360
        prediction = sum(coefficients[i] * kernel(theta, points[i]) for i in range(size))
        squared_error += (prediction - target(theta)) ** 2
    first = gram[0]
    eigenvalues = [
        sum(first[j] * math.cos(2 * math.pi * mode * j / size) for j in range(size))
        for mode in range(size)
    ]
    shifted = [max(value + ridge, ridge) for value in eigenvalues]
    condition = max(shifted) / min(shifted)
    rotation = 0.61
    defect = max(
        abs(kernel(left, right) - kernel(left + rotation, right + rotation))
        for left in points[::4]
        for right in points[::4]
    )
    return math.sqrt(squared_error / 360), condition, defect


def audit_exact_models() -> None:
    canonical_a = gaussian_anchor(4.0, 1.0, 1.0, 1.0, 1.0)
    blind_a = gaussian_anchor(3.0, 1.5, 1.0, 0.5, 3.0)
    for actual, expected, label in (
        (canonical_a, (5.0, 0.8958797346, 13 / 6, 2 / 3), "canonical Gaussian"),
        (blind_a, (3.375, 0.3768859012, 3.0, 2.117647059), "blind Gaussian"),
    ):
        require(all(math.isclose(a, b, rel_tol=2e-10, abs_tol=2e-10) for a, b in zip(actual, expected)),
                f"{label} anchor changed: {actual}")

    for mu, maximum, stable_eta, unstable_eta, expected_stable in (
        (1.0, 9.0, 0.20, 0.24, 0.005342747781),
        (2.0, 12.0, 0.14, 0.18, 0.0002788878486),
    ):
        threshold = 2 / maximum
        optimal_eta = 2 / (mu + maximum)
        optimal_rho = (maximum - mu) / (maximum + mu)
        require(stable_eta < threshold < unstable_eta, "Euler blind/canonical stability ordering changed")
        error = math.hypot((1 - mu * stable_eta) ** 25, (1 - maximum * stable_eta) ** 25)
        require(math.isclose(error, expected_stable, rel_tol=2e-10), "stable k=25 error changed")
        require(0 < optimal_eta < threshold and 0 < optimal_rho < 1, "optimal GD anchor invalid")

    canonical_c = krr_anchor(1.0, 0.65, 0.001, 2, 3, 0.3)
    blind_c = krr_anchor(1.5, 0.8, 0.005, 1, 4, 0.25)
    for actual, expected, label in (
        (canonical_c, (0.0001884871635, 13388.5707, 4.996003611e-16), "canonical circle KRR"),
        (blind_c, (0.0009451668782, 2134.613179, 7.21644966e-16), "blind circle KRR"),
    ):
        require(math.isclose(actual[0], expected[0], rel_tol=3e-10), f"{label} RMSE changed")
        require(math.isclose(actual[1], expected[1], rel_tol=3e-9), f"{label} condition changed")
        require(actual[2] < 2e-15, f"{label} rotation defect changed")
    print("PASS exact capstone models: canonical and blind Gaussian, Euler and circle-KRR anchors")


def audit_prerequisite_materials() -> None:
    for name, marker in PREREQUISITE_AUDITS:
        output = run(LABS / "code" / name)
        require(marker in output, f"prerequisite material audit did not pass: {name}")
    print("PASS prerequisite material audits: all ten volume gates remain regression-passed")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        nearby = "\n".join(
            line for line in content.splitlines()
            if "MATH-FND-CAP" in line or "十卷总出口" in line or audit_name in line
        )
        require("MATH-FND-CAP-01" in nearby, f"state surface misses capstone ID: {path.relative_to(ROOT)}")
        require("regression-passed" in nearby, f"state surface misses material PASS: {path.relative_to(ROOT)}")
        require("not-attempted" in nearby, f"state surface misses personal state: {path.relative_to(ROOT)}")
        require(audit_name in content, f"state surface misses independent audit: {path.relative_to(ROOT)}")
    print(f"PASS capstone state surfaces: {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_markdown() -> None:
    scoped = [ASSESSMENT, SOLUTION, EXPERIMENT]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.stem if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)
    missing: list[str] = []
    ambiguous: list[str] = []
    link_count = 0
    for path in scoped:
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in active_lines(read(path)))
        require(active.count("$$") % 2 == 0, f"{path.name}: unbalanced display math")
        for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", active):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            link_count += 1
            suffix = Path(target).suffix.lower()
            if "/" in target:
                direct = ROOT / target
                candidates = [direct] if direct.is_file() else []
                if not candidates and suffix not in KNOWN_EXTENSIONS:
                    markdown = Path(str(direct) + ".md")
                    if markdown.is_file():
                        candidates = [markdown]
            else:
                key = target[: -len(suffix)] if suffix in KNOWN_EXTENSIONS else target
                candidates = file_index.get(key, [])
                if suffix in KNOWN_EXTENSIONS:
                    candidates = [candidate for candidate in candidates if candidate.suffix.lower() == suffix]
            if not candidates:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing, f"missing Wiki links: {missing}")
    require(not ambiguous, f"ambiguous Wiki links: {ambiguous}")
    lines = read(EXPERIMENT).splitlines()
    positions = [index for index, line in enumerate(lines) if "![[" in line and ".svg" in line]
    require(len(positions) == 1, f"expected one capstone formal figure, found {len(positions)}")
    block = "\n".join(lines[positions[0]:positions[0] + 45])
    for marker in ("[!figure]", "怎样读图", "适用边界"):
        require(marker in block, f"capstone figure unit misses {marker}")
    print(f"PASS capstone Markdown: Wiki links={link_count}, display math balanced, figure unit complete")


def normalized_output(output: str) -> str:
    return "\n".join(line for line in output.splitlines() if not line.startswith("OUTPUT "))


def audit_compute() -> None:
    require(hashlib.sha256(CAP_SVG.read_bytes()).hexdigest() == EXPECTED_CAP_SHA256,
            "stored capstone SVG hash changed")
    root = ET.parse(CAP_SVG).getroot()
    require(root.tag.endswith("svg") and "viewBox" in root.attrib, "stored capstone SVG invalid")
    with tempfile.TemporaryDirectory(prefix="math-capstone-audit-") as directory:
        temporary = Path(directory)
        first_path, second_path = temporary / "canonical-a.svg", temporary / "canonical-b.svg"
        first = run(CAP_SCRIPT, "--output", str(first_path))
        second = run(CAP_SCRIPT, "--output", str(second_path))
        for marker in (
            "A_CONFIG variance_x=4 variance_y=1 observation_x=1 observation_y=1 signal_variance=5 reference_noise=1",
            "A_REFERENCE noise=1 mi=0.8958797346 posterior_trace=2.166666667 posterior_det=0.6666666667",
            "B_CONFIG lambda_min=1 lambda_max=9 stability_threshold=0.2222222222 optimal_eta=0.2 optimal_rho=0.8 flow_dt=0.2",
            "B_LEDGER eta=0.24 multiplier=(0.76,-1.16) error_k25=40.87424378",
            "C_CONFIG circle_radius=1 lengthscale=0.65 ridge=0.001 target_cos_frequency=2 target_sin_frequency=3 target_sin_amplitude=0.3 rotation=0.37",
            "C_LEDGER n=48 rmse=0.0001884871635 min_gram_eigenvalue=-1.576516695e-14 condition=13388.5707",
            f"SHA256 {EXPECTED_CAP_SHA256}",
        ):
            require(marker in first, f"canonical stdout misses {marker}")
        require(normalized_output(first) == normalized_output(second), "canonical stdout is not deterministic")
        require(first_path.read_bytes() == second_path.read_bytes() == CAP_SVG.read_bytes(),
                "canonical capstone SVG bytes differ across runs or stored artifact")

        unsafe = subprocess.run(
            [sys.executable, str(CAP_SCRIPT), "--variance-x", "3"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(unsafe.returncode != 0, "noncanonical capstone run could overwrite canonical SVG")
        require("noncanonical runs require --output" in unsafe.stderr, "overwrite protection message changed")

        blind = temporary / "blind.svg"
        blind_output = run(
            CAP_SCRIPT,
            "--variance-x", "3", "--variance-y", "1.5",
            "--observation-x", "1", "--observation-y", "0.5", "--reference-noise", "3",
            "--lambda-min", "2", "--lambda-max", "12",
            "--eta-conservative", "0.06", "--eta-stable", "0.14", "--eta-unstable", "0.18",
            "--flow-dt", "0.14", "--circle-radius", "1.5", "--lengthscale", "0.8",
            "--ridge", "0.005", "--target-cos-frequency", "1",
            "--target-sin-frequency", "4", "--target-sin-amplitude", "0.25",
            "--rotation", "0.61", "--output", str(blind),
        )
        for marker in (
            "A_CONFIG variance_x=3 variance_y=1.5 observation_x=1 observation_y=0.5 signal_variance=3.375 reference_noise=3",
            "A_REFERENCE noise=3 mi=0.3768859012 posterior_trace=3 posterior_det=2.117647059",
            "B_CONFIG lambda_min=2 lambda_max=12 stability_threshold=0.1666666667 optimal_eta=0.1428571429 optimal_rho=0.7142857143 flow_dt=0.14",
            "B_LEDGER eta=0.18 multiplier=(0.64,-1.16) error_k25=40.87424377",
            "C_CONFIG circle_radius=1.5 lengthscale=0.8 ridge=0.005 target_cos_frequency=1 target_sin_frequency=4 target_sin_amplitude=0.25 rotation=0.61",
            "C_LEDGER n=48 rmse=0.0009451668782 min_gram_eigenvalue=-1.054711873e-14 condition=2134.613179",
            f"SHA256 {EXPECTED_BLIND_SHA256}",
        ):
            require(marker in blind_output, f"blind stdout misses {marker}")
        require(hashlib.sha256(blind.read_bytes()).hexdigest() == EXPECTED_BLIND_SHA256,
                "blind capstone SVG hash changed")
        blind_svg = blind.read_text(encoding="utf-8")
        for marker in (
            "Σ=diag(3,1.5), c=(1,0.5)",
            "μ=2, L=12; η&lt;0.1667",
            "ρ=1.5, ℓ=0.8, λ=0.005, n=48",
            "target cos(1θ)+0.25sin(4θ)",
        ):
            require(marker in blind_svg, f"blind capstone SVG is not self-describing: {marker}")
        ET.parse(blind)
    print("PASS capstone compute: canonical double-run + overwrite protection + blind stdout/SVG/hash")


def main() -> None:
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_exact_models()
    audit_prerequisite_materials()
    audit_state_surfaces()
    audit_markdown()
    audit_compute()
    print("MATH-FND-CAP-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
