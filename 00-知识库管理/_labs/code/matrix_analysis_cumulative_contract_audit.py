#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for MA-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "10-数学基础" / "10.3-矩阵分析"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = MATRIX / "矩阵分析 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 矩阵分析（10.3）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 矩阵分析（10.3）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 矩阵分析累计复现门.md"
CUM_SCRIPT = LABS / "code" / "plot_matrix_analysis_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "matrix-analysis"
    / "plot-matrix-analysis-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "3985e488b31217a6f2fffa2fda864a9b7a545a28bb7f4a0275d3575f78601ec6"

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "10-数学基础" / "线性代数完整学习路线与掌握标准.md",
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


def active_lines(content: str) -> list[str]:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue
        if not in_fence:
            output.append(line)
    return output


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)

    for content, label in (
        (assessment, "assessment"),
        (solution, "solution"),
        (experiment, "experiment"),
    ):
        require("status: draft" in content, f"{label}: learning document must remain draft")
        require(
            "material_status: regression-passed" in content,
            f"{label}: material state is not regression-passed",
        )
        require(
            "learning_status: not-attempted" in content,
            f"{label}: personal state is not not-attempted",
        )
        require("updated: 2026-08-27" in content, f"{label}: migration date missing")

    require("time_limit_minutes: 270" in assessment, "assessment time limit changed")
    require("assessment_id: MA-CUM-01" in assessment, "assessment ID changed")
    require("assessment_id: MA-CUM-01" in solution, "solution ID changed")
    for index in range(1, 17):
        require(f"MA-{index:02d}" in assessment, f"assessment scope misses MA-{index:02d}")
    for index in range(1, 15):
        require(f"### 第{index}题：" in assessment, f"assessment misses question {index}")
        require(f"### 第{index}题：" in solution, f"solution misses answer {index}")

    for marker in (
        "先看完整验收时间线",
        "20 分钟卷级口试",
        "八层矩阵分析账本",
        "四个贯穿模型族",
        "答案隔离协议",
        "48 小时与 14 天保持性门",
        "证据清单",
    ):
        require(marker in assessment, f"assessment misses cumulative marker: {marker}")
    for marker in (
        "卷级口试参考要点",
        "四个贯穿模型族参考",
        "口试判分红线",
        "实验复现门的评分说明",
        "从 `retained` 到逐节点证据",
    ):
        require(marker in solution, f"solution misses oral/rubric marker: {marker}")

    forbidden_in_questions = (
        "## 8. 卷级口试参考要点",
        "## 9. 四个贯穿模型族参考",
        "## 10. 口试判分红线",
        "## 11. 实验复现门的评分说明",
    )
    leaked = [marker for marker in forbidden_in_questions if marker in assessment]
    require(not leaked, f"question/solution separation failed; leaked markers: {leaked}")
    require(
        'solution: "[[阶段测验解答 - 矩阵分析（10.3）]]"' in assessment,
        "assessment lost its explicit solution pointer",
    )
    require("冻结全部原始记录后再打开本解答" in solution, "solution use-order warning is incomplete")

    question_pattern = re.compile(r"^### 第(\d+)题：.*（(\d+)分）$", re.MULTILINE)
    assessment_points = [
        (int(index), int(points)) for index, points in question_pattern.findall(assessment)
    ]
    solution_points = [
        (int(index), int(points)) for index, points in question_pattern.findall(solution)
    ]
    require(
        [index for index, _ in assessment_points] == list(range(1, 15)),
        "assessment question numbering is no longer exactly 1--14",
    )
    require(
        solution_points == assessment_points,
        "question and solution point allocations disagree",
    )
    require(
        sum(points for _, points in assessment_points) == 100,
        "question point allocation no longer totals 100",
    )
    print(
        "PASS assessment bundle: scope 16/16, questions 14/14, "
        "oral/written/retention gates, answer isolation"
    )


def audit_cumulative_route() -> None:
    moc = read(MOC)
    for index in range(1, 17):
        require(f"MA-{index:02d}" in moc, f"MOC route misses MA-{index:02d}")
    for marker in (
        "卷级累计验收",
        "20 分钟无提示口试",
        "270 分钟闭卷",
        "48 小时换机制空白重建",
        "14 天陌生 AI 算子报告迁移",
        "四波统一模型族与三条证明主链",
        "matrix_analysis_cumulative_contract_audit.py",
        "`regression-passed / not-attempted`",
    ):
        require(marker in moc, f"MOC misses MA-CUM marker: {marker}")

    for path in STATE_SURFACES:
        content = read(path)
        require(
            "MA-CUM-01" in content or "MA-CUM" in content,
            f"state surface misses MA-CUM: {path.relative_to(ROOT)}",
        )
        nearby = "\n".join(
            line
            for line in content.splitlines()
            if "MA-CUM" in line
            or "10.3" in line
            or "matrix_analysis_cumulative_contract_audit.py" in line
        )
        require(
            "regression-passed" in nearby,
            f"state surface does not report MA-CUM material PASS: {path.relative_to(ROOT)}",
        )
        require(
            "not-attempted" in nearby,
            f"state surface lost personal not-attempted boundary: {path.relative_to(ROOT)}",
        )
    print(f"PASS state surfaces: MOC plus {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "进入实验前的四波解析校准门",
        "评分者随机指定与防挑题协议",
        "防止循环认证",
        "A轨道：至少两项",
        "B轨道：至少两项",
        "C轨道：至少两项",
        "评分者随机指定的盲手工复核",
        "盲参数干预门",
        "--min-delta",
        "--eta",
        "--min-gap",
        "--pseudospectral-epsilon",
        "--max-pseudo-coupling",
        "--max-sign-coupling",
        "--min-step",
        "证据状态机",
        "48 小时换机制与 14 天迁移",
        EXPECTED_CUM_SHA256,
    ):
        require(marker in experiment, f"experiment misses contract marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(CUM_SCRIPT.is_file(), "cumulative compute script missing")
    print("PASS experiment contract: four-wave calibration, blind A/B/C route, intervention and evidence states")


def operator_norm_upper_triangular(a: float, b: float, d: float) -> float:
    trace = a * a + b * b + d * d
    determinant_squared = (a * d) ** 2
    discriminant = max(0.0, trace * trace - 4.0 * determinant_squared)
    return math.sqrt(0.5 * (trace + math.sqrt(discriminant)))


def matmul_2x2(
    left: tuple[tuple[float, float], tuple[float, float]],
    right: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Multiply two real 2-by-2 matrices without depending on the plot implementation."""
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def transpose_2x2(
    matrix: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def audit_exact_models() -> None:
    # Wave A: near-singular map, inverse amplification and distance to singularity.
    epsilon = 0.003
    singulars = (1.0, epsilon)
    condition = singulars[0] / singulars[1]
    distance_to_singular = singulars[1]
    require(math.isclose(condition, 333.3333333333333), "A_epsilon condition changed")
    require(distance_to_singular == epsilon, "distance-to-singularity certificate changed")

    # Wave B: rank-deficient endpoint, EYM tail, effective rank and polar boundary.
    endpoint = ((1.0, 0.0), (0.0, 0.0))
    pseudoinverse = ((1.0, 0.0), (0.0, 0.0))
    endpoint_pinv = matmul_2x2(endpoint, pseudoinverse)
    pinv_endpoint = matmul_2x2(pseudoinverse, endpoint)
    require(
        matmul_2x2(endpoint_pinv, endpoint) == endpoint,
        "A_0 pseudoinverse fails A A+ A = A",
    )
    require(
        matmul_2x2(pinv_endpoint, pseudoinverse) == pseudoinverse,
        "A_0 pseudoinverse fails A+ A A+ = A+",
    )
    require(
        transpose_2x2(endpoint_pinv) == endpoint_pinv,
        "A_0 pseudoinverse fails symmetry of A A+",
    )
    require(
        transpose_2x2(pinv_endpoint) == pinv_endpoint,
        "A_0 pseudoinverse fails symmetry of A+ A",
    )
    stable_rank = (1.0 + epsilon * epsilon) / 1.0
    require(math.isclose(stable_rank, 1.000009, abs_tol=1e-15), "stable rank changed")
    spectral_tail = epsilon
    frobenius_tail = math.sqrt(epsilon * epsilon)
    require(spectral_tail == frobenius_tail == epsilon, "EYM rank-one tail changed")

    # Wave C: positive margin/Cholesky and closing-gap direction rotation.
    delta = 0.003
    minimum = delta
    maximum = 2.0 - delta
    cholesky_pivot = math.sqrt(2.0 * delta - delta * delta)
    require(math.isclose(maximum / minimum, 665.6666666667, abs_tol=5e-10), "SPD condition changed")
    require(math.isclose(cholesky_pivot, 0.07740155037, abs_tol=5e-11), "Cholesky pivot changed")
    eta = 0.02
    gap = 0.003
    angle = 0.5 * math.atan2(2.0 * eta, gap)
    eigen_shift = math.sqrt((gap / 2.0) ** 2 + eta * eta) - gap / 2.0
    require(math.isclose(angle * 180.0 / math.pi, 42.855423, abs_tol=5e-7), "gap-angle model changed")
    require(eigen_shift < eta, "Weyl-scale shift bound changed")

    # Wave D: resolvent certificate, nonunitary sign, Frechet divided differences and structure.
    pseudo_radius = math.sqrt(1e-3 * 100.0)
    require(math.isclose(pseudo_radius, 0.3162277660, abs_tol=5e-11), "pseudospectral certificate changed")
    sign_norm = operator_norm_upper_triangular(1.0, 10.0, -1.0)
    require(math.isclose(sign_norm, 10.09901951, abs_tol=5e-9), "matrix-sign norm changed")
    sign_matrix = ((1.0, 10.0), (0.0, -1.0))
    sign_square = matmul_2x2(sign_matrix, sign_matrix)
    require(sign_square == ((1.0, 0.0), (0.0, 1.0)), "sign involution changed")
    divided_difference = 3.0 / math.log(4.0)
    derivative = ((1.0, 2.0 * divided_difference), (-divided_difference, 0.0))
    require(math.isclose(derivative[0][1], 6.0 / math.log(4.0)), "Frechet divided difference changed")
    require(math.isclose(math.sqrt(2.0), 1.41421356237, abs_tol=5e-12), "ambient condition changed")
    symmetric_restriction = 1.0 - 1.0
    require(symmetric_restriction == 0.0, "symmetric structured condition changed")
    print(
        "PASS exact cumulative models: near-singular/low-rank, SPD/gap, "
        "resolvent/sign/Frechet/structure"
    )


def audit_markdown_integrity() -> None:
    scoped = [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        suffix = path.suffix.lower()
        key = path.name[: -len(path.suffix)] if suffix in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    for path in scoped:
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
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
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    experiment_lines = read(EXPERIMENT).splitlines()
    positions = [index for index, line in enumerate(experiment_lines) if image_pattern.search(line)]
    require(len(positions) == 1, f"cumulative experiment expected one formal figure, found {len(positions)}")
    block = "\n".join(experiment_lines[positions[0] : min(len(experiment_lines), positions[0] + 45)])
    for marker in ("[!figure]", "怎样读图", "适用边界"):
        require(marker in block, f"cumulative figure unit misses {marker}")
    print(f"PASS cumulative Markdown: Wiki links={link_count}, display math balanced, figure unit complete")


def stored_artifact_digest() -> str:
    require(CUM_SVG.is_file(), "cumulative SVG is missing")
    digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {digest}")
    root_element = ET.parse(CUM_SVG).getroot()
    require(root_element.tag.endswith("svg") and "viewBox" in root_element.attrib, "cumulative SVG failed XML/viewBox validation")
    return digest


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


def audit_compute() -> None:
    with tempfile.TemporaryDirectory(prefix="ma-cum-audit-") as temporary_directory:
        directory = Path(temporary_directory)
        canonical_path = directory / "canonical.svg"
        first_output = run(CUM_SCRIPT, "--output", str(canonical_path))
        for marker in (
            "A positive-definite margin / Cholesky / condition",
            "B perturbation gap and non-normal pseudospectrum",
            "C matrix function and structure",
        ):
            require(marker in first_output, f"cumulative script misses track report: {marker}")
        first_digest = hashlib.sha256(canonical_path.read_bytes()).hexdigest()
        require(first_digest == EXPECTED_CUM_SHA256, f"fresh cumulative SVG hash changed: {first_digest}")
        first_bytes = canonical_path.read_bytes()
        second_output = run(CUM_SCRIPT, "--output", str(canonical_path))
        second_digest = hashlib.sha256(canonical_path.read_bytes()).hexdigest()
        require(first_output == second_output and first_digest == second_digest, "cumulative gate is not deterministic")
        require(first_bytes == canonical_path.read_bytes(), "cumulative SVG bytes changed across two runs")

        intervention_path = directory / "intervention.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--min-delta",
            "0.001",
            "--eta",
            "0.01",
            "--min-gap",
            "0.001",
            "--pseudospectral-epsilon",
            "0.0004",
            "--max-pseudo-coupling",
            "400",
            "--max-sign-coupling",
            "20",
            "--min-step",
            "0.0001",
            "--output",
            str(intervention_path),
        )
        intervention_digest = hashlib.sha256(intervention_path.read_bytes()).hexdigest()
        require(intervention_digest != first_digest, "intervention did not change the SVG")
        for marker in (
            "delta=0.001",
            "kappa2=1999",
            "gap=0.001",
            "K=400  eps=4e-04",
            "K=20  sign_norm=20.049876",
            "h=1.0e-04",
        ):
            require(marker in intervention_output, f"intervention path misses expected change: {marker}")
        for path in (canonical_path, intervention_path):
            root_element = ET.parse(path).getroot()
            require(root_element.tag.endswith("svg") and "viewBox" in root_element.attrib, f"invalid SVG: {path.name}")

    print(f"PASS cumulative compute gate: deterministic double-run; sha256={first_digest}")
    print(f"PASS blind intervention interface: changed parameters and SVG; sha256={intervention_digest}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="rerun the deterministic MA-CUM gate twice and exercise blind parameter inputs",
    )
    args = parser.parse_args()

    audit_assessment_bundle()
    audit_cumulative_route()
    audit_experiment_contract()
    audit_exact_models()
    audit_markdown_integrity()
    digest = stored_artifact_digest()
    if args.run_compute:
        audit_compute()
    else:
        print(f"SKIP compute rerun (pass --run-compute for the formal MA-CUM audit); stored sha256={digest}")
    print("MA-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
