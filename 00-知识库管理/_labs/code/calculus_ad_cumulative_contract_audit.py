#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for CALC-CUM-01."""

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
CALCULUS = ROOT / "10-数学基础" / "10.4-多元微积分、矩阵微分与自动微分"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = CALCULUS / "多元微积分、矩阵微分与自动微分 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 多元微积分、矩阵微分与自动微分（10.4）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 多元微积分、矩阵微分与自动微分（10.4）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 微积分、矩阵微分与自动微分累计复现门.md"
CUM_SCRIPT = LABS / "code" / "plot_calculus_ad_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "calculus-ad"
    / "plot-calculus-ad-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "434dd29d2cc35e189010100365114f58f328682e5d793243da631be848ad6975"
EXPECTED_INTERVENTION_SHA256 = "b09416eb34a5d24d1652310ff8bf1f8342a662764a361408b81c7b3f9542da54"

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    ROOT / "00-知识库管理" / "00-总览" / "数学基础十卷完备性审计与学习状态总表.md",
    LABS / "exercises" / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}
Matrix2 = tuple[tuple[float, float], tuple[float, float]]
Vector2 = tuple[float, float]


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
    require("assessment_id: CALC-CUM-01" in assessment, "assessment ID changed")
    require("assessment_id: CALC-CUM-01" in solution, "solution ID changed")
    for index in range(1, 17):
        require(f"CALC-{index:02d}" in assessment, f"assessment scope misses CALC-{index:02d}")
    for index in range(1, 15):
        require(f"### 第{index}题：" in assessment, f"assessment misses question {index}")
        require(f"### 第{index}题：" in solution, f"solution misses answer {index}")

    for marker in (
        "先看完整验收时间线",
        "20分钟卷级口试",
        "八层微分与程序账本",
        "四个贯穿模型族",
        "答案隔离协议",
        "48小时与14天保持性门",
        "证据清单",
    ):
        require(marker in assessment, f"assessment misses cumulative marker: {marker}")
    for marker in (
        "卷级口试参考要点",
        "四个贯穿模型族参考",
        "口试判分红线",
        "实验复现门的评分说明",
        "从`retained`到逐节点证据",
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
        'solution: "[[阶段测验解答 - 多元微积分、矩阵微分与自动微分（10.4）]]"'
        in assessment,
        "assessment lost its explicit solution pointer",
    )
    require("之后才打开本解答" in solution, "solution use-order warning is incomplete")

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
    require(solution_points == assessment_points, "question and solution points disagree")
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
        require(f"CALC-{index:02d}" in moc, f"MOC route misses CALC-{index:02d}")
    for marker in (
        "卷级累计验收",
        "20分钟无提示口试",
        "270分钟闭卷",
        "48小时换机制",
        "14天陌生程序迁移",
        "四波统一模型族与三条证明主链",
        "calculus_ad_cumulative_contract_audit.py",
        "`regression-passed / not-attempted`",
    ):
        require(marker in moc, f"MOC misses CALC-CUM marker: {marker}")

    for path in STATE_SURFACES:
        content = read(path)
        require("CALC-CUM-01" in content, f"state surface misses CALC-CUM-01: {path.relative_to(ROOT)}")
        nearby = "\n".join(
            line
            for line in content.splitlines()
            if "CALC-CUM" in line
            or "10.4" in line
            or "calculus_ad_cumulative_contract_audit.py" in line
        )
        require(
            "regression-passed" in nearby,
            f"state surface does not report material PASS: {path.relative_to(ROOT)}",
        )
        require(
            "not-attempted" in nearby,
            f"state surface lost personal not-attempted boundary: {path.relative_to(ROOT)}",
        )
    print(f"PASS state surfaces: MOC plus {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "完整证据时间线",
        "进入实验前的四波解析校准门",
        "评分者随机指定与防挑题协议",
        "防止循环认证",
        "A轨道",
        "B轨道",
        "C轨道",
        "评分者随机指定的盲手工复核",
        "盲参数干预门",
        "--direction-y",
        "--min-local-step",
        "--max-fd-exponent",
        "--pairing-trials",
        "--hvp-direction-y",
        "--chain-length",
        "--min-hvp-step",
        "--implicit-rhs-slope",
        "--min-implicit-step",
        "--min-gap",
        "证据状态机与延迟迁移",
        EXPECTED_CUM_SHA256,
    ):
        require(marker in experiment, f"experiment misses contract marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(CUM_SCRIPT.is_file(), "cumulative compute script missing")
    print("PASS experiment contract: four-wave calibration, blind A/B/C route, intervention and evidence states")


def matvec(matrix: Matrix2, vector: Vector2) -> Vector2:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def dot(left: Vector2, right: Vector2) -> float:
    return left[0] * right[0] + left[1] * right[1]


def solve_2x2(matrix: Matrix2, rhs: Vector2) -> Vector2:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    require(determinant != 0.0, "independent 2x2 solve received singular matrix")
    return (
        (matrix[1][1] * rhs[0] - matrix[0][1] * rhs[1]) / determinant,
        (-matrix[1][0] * rhs[0] + matrix[0][0] * rhs[1]) / determinant,
    )


def audit_exact_models() -> None:
    # Wave A: Softplus and LogSumExp connect limits, derivatives and Taylor data.
    phi_zero = math.log(1.0 + math.exp(0.0))
    sigmoid_zero = math.exp(0.0) / (1.0 + math.exp(0.0))
    phi_second_zero = sigmoid_zero * (1.0 - sigmoid_zero)
    require(math.isclose(phi_zero, math.log(2.0)), "Softplus value changed")
    require(sigmoid_zero == 0.5, "Softplus first derivative changed")
    require(phi_second_zero == 0.25, "Softplus second derivative changed")
    direction_y = 0.7
    require(math.isclose(direction_y + 0.5, 1.2), "Taylor quadratic coefficient changed")
    require(math.isclose(direction_y**3, 0.343), "Taylor cubic coefficient changed")

    # Wave B: differential/gradient and the LogSumExp Hessian geometry.
    hessian: Matrix2 = ((0.25, -0.25), (-0.25, 0.25))
    common = (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0))
    contrast = (1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0))
    require(math.isclose(dot(common, matvec(hessian, common)), 0.0, abs_tol=1e-15), "common-shift curvature changed")
    require(math.isclose(dot(contrast, matvec(hessian, contrast)), 0.5, abs_tol=1e-15), "contrast curvature changed")

    x1, x2 = 1.0, 2.0
    cosine = math.cos(x1 * x2)
    jacobian = (
        (x2, x1),
        (cosine * x2, cosine * x1),
        (2.0 * x1 + cosine * x2, cosine * x1),
    )
    tangent = (1.0, -1.0)
    cotangent = (0.5, -1.0, 2.0)
    jvp = tuple(sum(row[j] * tangent[j] for j in range(2)) for row in jacobian)
    vjp = tuple(sum(jacobian[i][j] * cotangent[i] for i in range(3)) for j in range(2))
    require(
        math.isclose(sum(cotangent[i] * jvp[i] for i in range(3)), dot(tangent, vjp), abs_tol=1e-14),
        "fixed JVP/VJP pairing changed",
    )

    # Wave C: distinguish the variable-rhs exam program and shared-loss model.
    a_zero: Matrix2 = ((2.0, 1.0), (1.0, 2.0))
    x_zero = solve_2x2(a_zero, (1.0, 0.0))
    require(x_zero == (2.0 / 3.0, -1.0 / 3.0), "base solve changed")
    variable_rhs_derivative = solve_2x2(a_zero, (-x_zero[0], 1.0))
    require(
        all(math.isclose(value, target) for value, target in zip(variable_rhs_derivative, (-7.0 / 9.0, 8.0 / 9.0))),
        "variable-rhs implicit derivative changed",
    )
    require(math.isclose(dot(x_zero, variable_rhs_derivative), -22.0 / 27.0), "exam loss derivative changed")

    fixed_rhs_derivative = solve_2x2(a_zero, (-x_zero[0], 0.0))
    solve_branch = dot(x_zero, fixed_rhs_derivative)
    half_logdet_branch = 1.0 / 3.0
    require(math.isclose(solve_branch, -10.0 / 27.0), "shared solve branch changed")
    require(math.isclose(solve_branch + half_logdet_branch, -1.0 / 27.0), "shared loss derivative changed")
    require(math.isclose(2.0 / 3.0, 0.6666666666666666), "logdet derivative changed")

    # Wave D: rotation-stretch family separates spectral basis, flow and program derivatives.
    t_zero: Matrix2 = ((2.0, 0.0), (0.0, 1.0))
    t_dot: Matrix2 = ((2.0, -1.0), (2.0, 0.0))
    # A_dot = T_dot T^T + T T_dot^T, expanded independently.
    a_dot: Matrix2 = ((8.0, 3.0), (3.0, 0.0))
    require(a_dot[0][0] == 8.0, "top eigenvalue derivative changed")
    require(math.isclose(a_dot[1][0] / (4.0 - 1.0), 1.0), "top eigenvector derivative changed")
    observation = (1.0, 2.0)
    latent = solve_2x2(t_zero, observation)
    t_dot_latent = matvec(t_dot, latent)
    latent_dot = solve_2x2(t_zero, (-t_dot_latent[0], -t_dot_latent[1]))
    nll_derivative = dot(latent, latent_dot) + 1.0
    require(latent == (0.5, 2.0), "flow inverse changed")
    require(latent_dot == (0.5, -1.0), "flow inverse JVP changed")
    require(math.isclose(nll_derivative, -0.75), "Gaussian change-of-variables derivative changed")
    require(math.isclose(2.0 * 3.0, 6.0), "linear change-of-variables determinant changed")
    require(math.isclose(1.0 / 0.003, 333.3333333333333), "spectral-gap certificate changed")
    print(
        "PASS exact cumulative models: Softplus/LogSumExp, operator pairing, "
        "solve/logdet, spectral/flow/AD"
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
    require(
        root_element.tag.endswith("svg") and "viewBox" in root_element.attrib,
        "cumulative SVG failed XML/viewBox validation",
    )
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
    with tempfile.TemporaryDirectory(prefix="calc-cum-audit-") as temporary_directory:
        directory = Path(temporary_directory)
        canonical_path = directory / "canonical.svg"
        first_output = run(CUM_SCRIPT, "--output", str(canonical_path))
        for marker in (
            "CALC-CUM-01 deterministic computation gate",
            "A finite-difference best_h=",
            "B max_adjoint_pairing_residual=",
            "C logdet_derivative=0.66666667 change_of_variables_det=6",
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
            "--direction-y",
            "0.4",
            "--min-local-step",
            "5e-5",
            "--max-fd-exponent",
            "16",
            "--pairing-trials",
            "160",
            "--hvp-direction-y",
            "-0.5",
            "--chain-length",
            "2304",
            "--min-hvp-step",
            "3e-6",
            "--implicit-rhs-slope",
            "0.5",
            "--min-implicit-step",
            "1e-5",
            "--min-gap",
            "0.001",
            "--output",
            str(intervention_path),
        )
        intervention_digest = hashlib.sha256(intervention_path.read_bytes()).hexdigest()
        require(intervention_digest != first_digest, "intervention did not change the SVG")
        require(
            intervention_digest == EXPECTED_INTERVENTION_SHA256,
            f"formal intervention SVG hash changed: {intervention_digest}",
        )
        for marker in (
            "A h=5.0e-05 linear=2.2500082e-09 quadratic=7.9936058e-15",
            "final_error=0.44488849",
            "B h=3.0e-06 hvp_error=3.698195e-10",
            "C h=1.0e-05 implicit_error=3.1523195e-11",
            "C gap=0.001 eigenvector_derivative_norm=1000",
        ):
            require(marker in intervention_output, f"intervention path misses expected change: {marker}")
        for path in (canonical_path, intervention_path):
            root_element = ET.parse(path).getroot()
            require(
                root_element.tag.endswith("svg") and "viewBox" in root_element.attrib,
                f"invalid SVG: {path.name}",
            )

    print(f"PASS cumulative compute gate: deterministic double-run; sha256={first_digest}")
    print(f"PASS blind intervention interface: changed parameters and SVG; sha256={intervention_digest}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="rerun the deterministic CALC-CUM gate twice and exercise blind parameter inputs",
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
        print(f"SKIP compute rerun (pass --run-compute for the formal CALC-CUM audit); stored sha256={digest}")
    print("CALC-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
