#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for GEO-CUM-01."""

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
GEO = ROOT / "10-数学基础" / "10.10-几何、泛函分析、核与算子基础"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = GEO / "几何、泛函分析、核与算子基础 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 几何、泛函分析、核与算子基础（10.10）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 几何、泛函分析、核与算子基础（10.10）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 几何、泛函与算子累计复现门.md"
TEACHING_AUDIT = LABS / "code" / "geometry_functional_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "geometry_functional_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "geometry-functional"
    / "plot-geometry-functional-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "d0ff3852b11f8a82af5feff469fa3ef4e1adde7836cf292b4911dec043c59bd1"
EXPECTED_INTERVENTION_SHA256 = "7b5aac02d74e0fd90053dee51ad1d17d0911454592730b486fb23e4ec12cd9bc"

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


def active_lines(content: str) -> list[str]:
    """Remove fenced code while retaining prose, formulas, links and callouts."""
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
        require("updated: 2026-08-28" in content, f"{label}: migration date missing")

    require("time_limit_minutes: 210" in assessment, "assessment time limit changed")
    require("assessment_id: GEO-CUM-01" in assessment, "assessment ID changed")
    require("assessment_id: GEO-CUM-01" in solution, "solution ID changed")
    for index in range(1, 9):
        require(f"GEO-{index:02d}" in assessment, f"assessment scope misses GEO-{index:02d}")
    for index in range(1, 15):
        require(f"### 第{index}题：" in assessment, f"assessment misses question {index}")
        require(f"### 第{index}题解答：" in solution, f"solution misses answer {index}")

    for marker in (
        "先看完整验收时间线",
        "20 分钟卷级口试",
        "三波参数化模型族",
        "九层几何—泛函—算子对象账本",
        "答案与输出隔离协议",
        "scorer nonce",
        "连续—离散证据边界",
        "48 小时换机制重建门",
        "14 天陌生 AI 几何—算子迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses cumulative marker: {marker}")
    for marker in (
        "卷级口试参考要点",
        "九层几何—泛函—算子对象账本参考",
        "三波参数化模型族的卷级数值锚点",
        "口试判分红线",
        "实验复现门的评分说明",
        "nonce 与盲参数判分红线",
        "从 `retained` 到逐节点证据",
        "最终状态边界",
    ):
        require(marker in solution, f"solution misses oral/rubric marker: {marker}")

    forbidden_in_questions = (
        "### 第1题解答：",
        "## 七、卷级口试参考要点",
        "## 八、九层几何—泛函—算子对象账本参考",
        "## 九、口试判分红线",
    )
    leaked = [marker for marker in forbidden_in_questions if marker in assessment]
    require(not leaked, f"question/solution separation failed; leaked markers: {leaked}")
    require(
        'solution: "[[阶段测验解答 - 几何、泛函分析、核与算子基础（10.10）]]"'
        in assessment,
        "assessment lost its explicit solution pointer",
    )
    require(
        "才可打开本解答或 canonical 结果" in solution,
        "solution use-order warning is incomplete",
    )

    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)题：.*（(\d+)分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)题解答：.*（(\d+)分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 15)), "assessment point headers are incomplete")
    require(sorted(solution_points) == list(range(1, 15)), "solution point headers are incomplete")
    require(question_points == solution_points, "question/solution point allocations differ")
    require(sum(question_points.values()) == 100, "question point allocation no longer totals 100")
    print(
        "PASS assessment bundle: scope 8/8, questions/answers 14/14, "
        "points=100, isolation + nonce + delay gates"
    )


def audit_cumulative_route() -> None:
    moc = read(MOC)
    expected_row = (
        "| CUM | GEO-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 跨轨盲干预 → 订正 → 48 h / 14 d → 独立审计 | "
        "三波参数化模型族、三条证明主链与 A/B/C 累计门 | `regression-passed` | `not-attempted` |"
    )
    require(expected_row in moc, "MOC cumulative status row is not regression-passed / not-attempted")
    for marker in (
        "GEO-CUM-01：卷末综合验收闭环",
        "20 分钟口试",
        "210 分钟闭卷",
        "48 小时换例",
        "14 天迁移",
        "GEO-CUM 材料证书",
        "从零如何执行 GEO-CUM",
        "geometry_functional_cumulative_contract_audit.py",
    ):
        require(marker in moc, f"MOC misses GEO-CUM marker: {marker}")

    for path in STATE_SURFACES:
        content = read(path)
        require(
            "GEO-CUM-01" in content or "GEO-CUM" in content,
            f"state surface misses GEO-CUM: {path.relative_to(ROOT)}",
        )
        nearby = "\n".join(
            line
            for line in content.splitlines()
            if "GEO-CUM" in line
            or "10.10" in line
            or "geometry_functional_cumulative_contract_audit.py" in line
        )
        require(
            "regression-passed" in nearby,
            f"state surface does not report GEO-CUM material PASS: {path.relative_to(ROOT)}",
        )
        require(
            "not-attempted" in nearby,
            f"state surface lost personal not-attempted boundary: {path.relative_to(ROOT)}",
        )
        require(
            "geometry_functional_cumulative_contract_audit.py" in content,
            f"state surface misses independent audit: {path.relative_to(ROOT)}",
        )
    print(f"PASS state surfaces: MOC plus {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "评分者随机指定、跨轨盲参与防挑题协议",
        "防止循环认证",
        "轨道A：球面几何、retraction与rotation covariance",
        "轨道B：Hilbert projection、compact spectrum与RKHS容量",
        "轨道C：Poisson smoothing与operator cutoff盲区",
        "评分者随机指定的盲手工复核",
        "盲参数干预门",
        "盲测干预怎样才算独立",
        "审计使用的固定多参数盲测 fixture",
        "--sphere-radius",
        "--coefficient-exponent",
        "--domain-length",
        "证据状态机",
        "48 小时换例与 14 天迁移",
        EXPECTED_CUM_SHA256,
        EXPECTED_INTERVENTION_SHA256,
    ):
        require(marker in experiment, f"experiment misses contract marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(TEACHING_AUDIT.is_file() and CUM_SCRIPT.is_file(), "required audit/compute scripts missing")
    print("PASS experiment contract: analytic calibration, A/B/C tracks, blind intervention and evidence states")


def audit_exact_models() -> None:
    # Track A: tangent projection, exact sphere constraint and covariance.
    point = (1.0, 0.0, 0.0)
    parameter = (1.0, 2.0, -1.0)
    inner = sum(a * b for a, b in zip(point, parameter))
    gradient = tuple(c - inner * p for p, c in zip(point, parameter))
    require(gradient == (0.0, 2.0, -1.0), "sphere gradient changed")
    tangent = tuple(value / math.sqrt(5) for value in gradient)
    for step in (0.25, 0.125, 0.0625):
        ambient = tuple(p + step * v for p, v in zip(point, tangent))
        residual = sum(value * value for value in ambient) - 1.0
        require(math.isclose(residual, step * step, abs_tol=2e-16), "sphere constraint order changed")
    step = 2 ** -10
    ambient = tuple(p + step * v for p, v in zip(point, tangent))
    retraction = tuple(value / math.sqrt(1 + step * step) for value in ambient)
    exponential = tuple(
        math.cos(step) * p + math.sin(step) * v for p, v in zip(point, tangent)
    )
    leading_ratio = math.dist(retraction, exponential) / (step ** 3)
    require(0.332 < leading_ratio < 0.334, "retraction-to-Exp cubic coefficient changed")
    angle = 0.7
    cosine, sine = math.cos(angle), math.sin(angle)
    rotation = ((cosine, -sine, 0.0), (sine, cosine, 0.0), (0.0, 0.0, 1.0))

    def matvec(matrix: tuple[tuple[float, ...], ...], vector: tuple[float, ...]) -> tuple[float, ...]:
        return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)

    rotated_point = matvec(rotation, point)
    rotated_parameter = matvec(rotation, parameter)
    rotated_inner = sum(a * b for a, b in zip(rotated_point, rotated_parameter))
    lhs = tuple(c - rotated_inner * p for p, c in zip(rotated_point, rotated_parameter))
    rhs = matvec(rotation, gradient)
    require(math.dist(lhs, rhs) < 1e-15, "sphere covariance changed")

    # Track B: coefficient tail, compact diagonal tail and effective dimension.
    size = 131072
    cutoff = 4096
    finite_tail = math.sqrt(sum(1 / (j * j) for j in range(cutoff + 1, size + 1)))
    require(
        1 / math.sqrt(cutoff + 1) - 1 / math.sqrt(size) < finite_tail < 1 / math.sqrt(cutoff),
        "Hilbert projection tail left its analytic scale",
    )
    compact_tail = 1 / ((cutoff + 1) ** 2)
    require(compact_tail > 0 and compact_tail < 6e-8, "compact operator tail changed")
    regularization = 1e-6
    effective_dimension = sum(
        1 / (1 + regularization * j * j) for j in range(1, size + 1)
    )
    require(
        math.isclose(effective_dimension, 1562.667109, abs_tol=8e-7),
        "kernel effective dimension changed",
    )

    # Track C: exact Poisson multiplier and the four error ledgers.
    modes = list(range(9, 65))
    l2_errors = [1 / ((math.pi * mode) ** 2) for mode in modes]
    energy_errors = [1 / (math.pi * mode) for mode in modes]
    strong_residuals = [1.0 for _ in modes]

    def log_slope(xs: list[int], ys: list[float]) -> float:
        log_xs = [math.log(value) for value in xs]
        log_ys = [math.log(value) for value in ys]
        mean_x = sum(log_xs) / len(log_xs)
        mean_y = sum(log_ys) / len(log_ys)
        return sum((x - mean_x) * (y - mean_y) for x, y in zip(log_xs, log_ys)) / sum(
            (x - mean_x) ** 2 for x in log_xs
        )

    require(math.isclose(log_slope(modes, l2_errors), -2.0, abs_tol=2e-15), "Poisson L2 order changed")
    require(math.isclose(log_slope(modes, energy_errors), -1.0, abs_tol=2e-15), "Poisson energy order changed")
    require(math.isclose(log_slope(modes, strong_residuals), 0.0, abs_tol=0.0), "strong residual order changed")
    l2_error = l2_errors[-1]
    energy_error = energy_errors[-1]
    require(math.isclose(l2_error, 2.47366171e-5, abs_tol=5e-14), "Poisson L2 error changed")
    require(math.isclose(energy_error, 4.97359197e-3, abs_tol=5e-12), "Poisson energy error changed")
    require(l2_error / l2_error == 1.0, "Poisson relative error changed")

    # Fixed blind fixture: derive its mechanism-changing anchors independently.
    blind_radius = 1.5
    blind_step = 2 ** -10
    blind_parameter = (1.0, 1.4, -0.6)
    blind_point = (blind_radius, 0.0, 0.0)
    blind_inner = sum(a * b for a, b in zip(blind_point, blind_parameter))
    blind_gradient = tuple(
        c - blind_inner * p / (blind_radius * blind_radius)
        for p, c in zip(blind_point, blind_parameter)
    )
    blind_gradient_norm = math.sqrt(sum(value * value for value in blind_gradient))
    blind_tangent = tuple(value / blind_gradient_norm for value in blind_gradient)
    blind_ambient = tuple(p + blind_step * v for p, v in zip(blind_point, blind_tangent))
    require(
        math.isclose(
            sum(value * value for value in blind_ambient) - blind_radius**2,
            blind_step**2,
            abs_tol=5e-16,
        ),
        "blind sphere constraint changed",
    )
    blind_retraction = tuple(
        blind_radius * value / math.sqrt(sum(item * item for item in blind_ambient))
        for value in blind_ambient
    )
    blind_exponential = tuple(
        math.cos(blind_step / blind_radius) * p
        + blind_radius * math.sin(blind_step / blind_radius) * v
        for p, v in zip(blind_point, blind_tangent)
    )
    blind_leading_ratio = math.dist(blind_retraction, blind_exponential) / blind_step**3
    require(
        math.isclose(blind_leading_ratio, 1 / (3 * blind_radius**2), rel_tol=2e-3),
        "blind retraction coefficient changed",
    )

    blind_alpha, blind_beta = 1.25, 1.5
    require(math.isclose(0.5 - blind_alpha, -0.75, abs_tol=0.0),
            "blind projection exponent changed")
    require(math.isclose(-blind_beta, -1.5, abs_tol=0.0),
            "blind compact exponent changed")
    require(math.isclose(1 / blind_beta, 2 / 3, abs_tol=0.0),
            "blind effective-dimension exponent changed")
    blind_operator_tail = (4096 + 1) ** (-blind_beta)
    require(3.8e-6 < blind_operator_tail < 3.9e-6, "blind compact tail changed")

    blind_length, blind_mode = 1.5, 80
    blind_l2 = (blind_length / (math.pi * blind_mode)) ** 2
    blind_energy = blind_length / (math.pi * blind_mode)
    require(math.isclose(blind_l2, 3.56207286e-5, abs_tol=5e-14),
            "blind Poisson L2 anchor changed")
    require(math.isclose(blind_energy, 5.96831037e-3, abs_tol=5e-12),
            "blind Poisson energy anchor changed")
    print("PASS exact cumulative models: canonical A/B/C plus fixed blind sphere/spectrum/Poisson anchors")


def audit_markdown_integrity() -> None:
    scoped = [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
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


def normalized_output(output: str) -> str:
    return "\n".join(line for line in output.splitlines() if not line.startswith("OUTPUT "))


def audit_compute() -> None:
    teaching_output = run(TEACHING_AUDIT, "--run-figures")
    require(
        "GEO-01—08 material regression: PASS" in teaching_output,
        "chapter teaching audit did not reach its material PASS",
    )

    with tempfile.TemporaryDirectory(prefix="geo-cum-audit-") as temporary_directory:
        temporary = Path(temporary_directory)
        canonical_a = temporary / "canonical-a.svg"
        canonical_b = temporary / "canonical-b.svg"
        first_output = run(CUM_SCRIPT, "--output", str(canonical_a))
        second_output = run(CUM_SCRIPT, "--output", str(canonical_b))
        for marker in (
            "A_CONFIG sphere_radius=1 objective_y=2 objective_z=-1 rotation_angle=0.7",
            "A_GEOMETRY constraint_slope=2.000000 retraction_order=2.997004 equivariance_error=3.140e-16",
            "B_CONFIG spectral_size=131072 coefficient_exponent=1 eigen_exponent=2",
            "B_SPECTRAL projection_slope=-0.495225 compact_tail_slope=-1.951949 effective_dimension_slope=0.506725 neff_at_1e-6=1562.667109",
            "C_CONFIG domain_length=1 train_cutoff=8 max_mode=64",
            "C_OPERATOR l2_slope=-2.000000 energy_slope=-1.000000 strong_slope=0.000000 last_l2=2.47366171e-05 last_energy=4.97359197e-03",
            f"SHA256 {EXPECTED_CUM_SHA256}",
        ):
            require(marker in first_output, f"canonical output misses: {marker}")
        first_digest = hashlib.sha256(canonical_a.read_bytes()).hexdigest()
        require(first_digest == EXPECTED_CUM_SHA256, f"fresh cumulative SVG hash changed: {first_digest}")
        second_digest = hashlib.sha256(canonical_b.read_bytes()).hexdigest()
        require(normalized_output(first_output) == normalized_output(second_output),
                "canonical stdout changed across output paths")
        require(first_digest == second_digest, "canonical digest changed across output paths")
        require(canonical_a.read_bytes() == canonical_b.read_bytes() == CUM_SVG.read_bytes(),
                "canonical SVG bytes differ from stored artifact")
        root_element = ET.parse(canonical_a).getroot()
        require(
            root_element.tag.endswith("svg") and "viewBox" in root_element.attrib,
            "fresh cumulative SVG failed XML/viewBox validation",
        )

        unsafe_run = subprocess.run(
            [sys.executable, str(CUM_SCRIPT), "--sphere-radius", "1.5"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        require(unsafe_run.returncode != 0,
                "noncanonical run without --output could overwrite canonical SVG")
        require("noncanonical runs require --output" in unsafe_run.stderr,
                "noncanonical output-protection error message drifted")

        intervention = temporary / "blind.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--sphere-radius", "1.5",
            "--objective-y", "1.4",
            "--objective-z", "-0.6",
            "--rotation-angle", "1.1",
            "--spectral-size", "65536",
            "--coefficient-exponent", "1.25",
            "--eigen-exponent", "1.5",
            "--domain-length", "1.5",
            "--train-cutoff", "12",
            "--max-mode", "80",
            "--output", str(intervention),
        )
        intervention_digest = hashlib.sha256(intervention.read_bytes()).hexdigest()
        require(intervention_digest == EXPECTED_INTERVENTION_SHA256,
                f"blind intervention SVG hash changed: {intervention_digest}")
        for marker in (
            "A_CONFIG sphere_radius=1.5 objective_y=1.4 objective_z=-0.6 rotation_angle=1.1",
            "A_GEOMETRY constraint_slope=2.000000 retraction_order=2.998653 equivariance_error=3.140e-16",
            "B_CONFIG spectral_size=65536 coefficient_exponent=1.25 eigen_exponent=1.5",
            "B_SPECTRAL projection_slope=-0.740993 compact_tail_slope=-1.463961 effective_dimension_slope=0.641956 neff_at_1e-6=16483.628089",
            "C_CONFIG domain_length=1.5 train_cutoff=12 max_mode=80",
            "C_OPERATOR l2_slope=-2.000000 energy_slope=-1.000000 strong_slope=0.000000 last_l2=3.56207286e-05 last_energy=5.96831037e-03",
            f"SHA256 {EXPECTED_INTERVENTION_SHA256}",
        ):
            require(marker in intervention_output, f"blind output misses: {marker}")
        intervention_svg = intervention.read_text(encoding="utf-8")
        for marker in (
            "S² radius=1.5；c=(1,1.4,-0.6)；θ=1.1",
            "N=65536；cⱼ=j⁻1.25；μⱼ=j⁻1.5",
            "(0,L), L=1.5；train 1…12；OOD 13…80",
            "j=80: L²=3.56e-05, relative=100%",
        ):
            require(marker in intervention_svg, f"blind SVG does not self-describe: {marker}")
        ET.parse(intervention)

    print("PASS chapter compute dependency: GEO-01—08 teaching/figure regression")
    print(f"PASS canonical double-run + stored SVG: sha256={first_digest}")
    print(f"PASS blind-interface intervention: sha256={EXPECTED_INTERVENTION_SHA256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="rerun GEO-01--08 figures and the deterministic GEO-CUM three-track gate",
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
        print(f"SKIP compute rerun (pass --run-compute for the formal GEO-CUM audit); stored sha256={digest}")
    print("GEO-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
