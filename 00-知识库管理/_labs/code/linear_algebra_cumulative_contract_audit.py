#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for LA-CUM-01."""

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
LINEAR = ROOT / "10-数学基础" / "10.2-线性代数"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = LINEAR / "线性代数 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 线性代数（10.2）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 线性代数（10.2）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 线性代数累计复现门.md"
CUM_SCRIPT = LABS / "code" / "plot_linear_algebra_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "linear-algebra"
    / "plot-linear-algebra-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "35dec5ba56a5727c4cd3d08e36e77ffe5dd23aeb6092f20788b7c6a4bf54345e"

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
        require("updated: 2026-08-27" in content, f"{label}: migration date missing")

    require("time_limit_minutes: 240" in assessment, "assessment time limit changed")
    require("assessment_id: LA-CUM-01" in assessment, "assessment ID changed")
    require("assessment_id: LA-CUM-01" in solution, "solution ID changed")
    for index in range(1, 25):
        require(f"LA-{index:02d}" in assessment, f"assessment scope misses LA-{index:02d}")
    for index in range(1, 15):
        require(f"### 第{index}题：" in assessment, f"assessment misses question {index}")
        require(f"### 第{index}题：" in solution, f"solution misses answer {index}")

    for marker in (
        "先看完整验收时间线",
        "20 分钟卷级口试",
        "八层对象账本",
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
        'solution: "[[阶段测验解答 - 线性代数（10.2）]]"' in assessment,
        "assessment lost its explicit solution pointer",
    )
    require("冻结全部原始记录后再打开本解答" in solution, "solution use-order warning is incomplete")

    points = (5, 5, 5, 5, 8, 8, 7, 7, 8, 8, 9, 10, 5, 10)
    require(sum(points) == 100, "question point allocation no longer totals 100")
    print(
        "PASS assessment bundle: scope 24/24, questions 14/14, "
        "oral/written/retention gates, answer isolation"
    )


def audit_cumulative_route() -> None:
    moc = read(MOC)
    for index in range(1, 25):
        require(f"LA-{index:02d}" in moc, f"MOC route misses LA-{index:02d}")
    for marker in (
        "卷级累计验收",
        "20 分钟无提示口试",
        "240 分钟闭卷",
        "48 小时换例空白重建",
        "14 天陌生 AI 报告迁移",
        "四个贯穿模型族",
        "linear_algebra_cumulative_contract_audit.py",
        "`regression-passed / not-attempted`",
    ):
        require(marker in moc, f"MOC misses LA-CUM marker: {marker}")

    for path in STATE_SURFACES:
        content = read(path)
        require(
            "LA-CUM-01" in content or "LA-CUM" in content,
            f"state surface misses LA-CUM: {path.relative_to(ROOT)}",
        )
        nearby = "\n".join(
            line
            for line in content.splitlines()
            if "LA-CUM" in line
            or "10.2" in line
            or "linear_algebra_cumulative_contract_audit.py" in line
        )
        require(
            "regression-passed" in nearby,
            f"state surface does not report LA-CUM material PASS: {path.relative_to(ROOT)}",
        )
        require(
            "not-attempted" in nearby,
            f"state surface lost personal not-attempted boundary: {path.relative_to(ROOT)}",
        )
    print(f"PASS state surfaces: MOC plus {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "进入实验前的解析校准门",
        "评分者随机指定与防挑题协议",
        "防止循环认证",
        "A轨道：至少两项",
        "B轨道：至少两项",
        "C轨道：至少两项",
        "评分者随机指定的盲手工复核",
        "盲参数干预门",
        "--min-epsilon",
        "--rho",
        "--score-scale",
        "--rank-tolerance",
        "证据状态机",
        "48 小时换例与 14 天迁移",
        EXPECTED_CUM_SHA256,
    ):
        require(marker in experiment, f"experiment misses contract marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(CUM_SCRIPT.is_file(), "cumulative compute script missing")
    print("PASS experiment contract: analytic calibration, blind A/B/C route, intervention and evidence states")


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*a)]


def numerical_rank(a: list[list[float]], tolerance: float = 1e-10) -> int:
    """Independent Gaussian-elimination rank, not the gate's singular-value routine."""
    work = [row[:] for row in a]
    rows, columns = len(work), len(work[0])
    rank = 0
    for column in range(columns):
        pivot = max(range(rank, rows), key=lambda row: abs(work[row][column]), default=rank)
        if rank >= rows or abs(work[pivot][column]) <= tolerance:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        for row in range(rank + 1, rows):
            factor = work[row][column] / pivot_value
            for index in range(column, columns):
                work[row][index] -= factor * work[rank][index]
        rank += 1
        if rank == rows:
            break
    return rank


def operator_norm_upper_triangular(a: float, b: float) -> float:
    trace = 2.0 * a * a + b * b
    determinant = a**4
    discriminant = max(0.0, trace * trace - 4.0 * determinant)
    return math.sqrt(0.5 * (trace + math.sqrt(discriminant)))


def audit_exact_models() -> None:
    # Track A: analytic coordinates/condition plus exact integer/rational subspace checks.
    epsilon = 0.003
    coordinate_norm = math.sqrt(2.0) / epsilon
    trace = 2.0 + epsilon * epsilon
    discriminant = math.sqrt(4.0 + epsilon**4)
    lambda_max = (trace + discriminant) / 2.0
    lambda_min = (trace - discriminant) / 2.0
    condition = math.sqrt(lambda_max / lambda_min)
    require(math.isclose(coordinate_norm, 471.404520791, abs_tol=5e-10), "coordinate growth changed")
    require(math.isclose(condition, 666.66816667, abs_tol=8e-7), "basis condition changed")

    a = ((1, 0, 1), (0, 1, 1), (1, 1, 2))
    null = (-1, -1, 1)
    require(tuple(sum(row[j] * null[j] for j in range(3)) for row in a) == (0, 0, 0), "kernel changed")
    projector_numerators = ((2, -1, 1), (-1, 2, 1), (1, 1, 2))
    product = tuple(
        tuple(sum(projector_numerators[i][k] * projector_numerators[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )
    require(product == tuple(tuple(3 * value for value in row) for row in projector_numerators), "P^2=P changed")
    transposed_projector = tuple(tuple(row) for row in transpose([list(row) for row in projector_numerators]))
    require(projector_numerators == transposed_projector, "P^T=P changed")

    # Track B: independent Jordan norm scan and EYM tail ledger.
    powers: list[float] = []
    for k in range(61):
        diagonal = 0.9**k
        off_diagonal = 0.0 if k == 0 else k * 0.9 ** (k - 1)
        powers.append(operator_norm_upper_triangular(diagonal, off_diagonal))
    peak_k = max(range(len(powers)), key=powers.__getitem__)
    require(peak_k == 9, f"Jordan peak index changed: {peak_k}")
    require(math.isclose(powers[peak_k], 3.9125671, abs_tol=5e-8), "Jordan peak norm changed")
    singulars = (5.0, 2.0, 0.5, 0.1)
    spectral = [singulars[r] if r < len(singulars) else 0.0 for r in range(1, 5)]
    frobenius = [math.sqrt(sum(value * value for value in singulars[r:])) for r in range(1, 5)]
    require(spectral == [2.0, 0.5, 0.1, 0.0], "spectral SVD tails changed")
    require(math.isclose(frobenius[0], 2.063976744, abs_tol=5e-9), "Frobenius SVD tail changed")

    # Track C: factorized score rank, nonlinear softmax rank and column-vec identity.
    theta = [-1.2 + i * 2.5 / 7 for i in range(8)]
    phi = [-0.9 + i * 2.4 / 7 for i in range(8)]
    q = [[math.cos(value), math.sin(value)] for value in theta]
    k = [[math.cos(value), math.sin(value)] for value in phi]
    score = [[2.0 * value for value in row] for row in matmul(q, transpose(k))]
    attention: list[list[float]] = []
    for row in score:
        maximum = max(row)
        values = [math.exp(value - maximum) for value in row]
        total = sum(values)
        attention.append([value / total for value in values])
    require(numerical_rank(score) == 2, "factorized score rank changed")
    require(numerical_rank(attention) == 8, "softmax counterexample rank changed")

    x = [[1.0, 2.0], [3.0, 4.0]]
    left = [[1.0, 1.0], [0.0, 1.0]]
    right = [[2.0, 0.0], [1.0, 1.0]]
    direct_matrix = matmul(matmul(left, x), right)
    direct_vec = [direct_matrix[i][j] for j in range(2) for i in range(2)]
    require(direct_vec == [14.0, 10.0, 6.0, 4.0], "column-vec identity target changed")
    print(
        "PASS exact cumulative models: coordinate/quotient/projector, "
        "Jordan/SVD tails, attention rank and vec identity"
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
    with tempfile.TemporaryDirectory(prefix="la-cum-audit-") as temporary_directory:
        directory = Path(temporary_directory)
        canonical_path = directory / "canonical.svg"
        first_output = run(CUM_SCRIPT, "--output", str(canonical_path))
        for marker in ("A coordinate conditioning", "B spectral/Jordan/SVD", "C structured AI"):
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
            "--min-epsilon",
            "0.001",
            "--rho",
            "0.8",
            "--score-scale",
            "0.5",
            "--rank-tolerance",
            "1e-6",
            "--output",
            str(intervention_path),
        )
        intervention_digest = hashlib.sha256(intervention_path.read_bytes()).hexdigest()
        require(intervention_digest != first_digest, "intervention did not change the SVG")
        for marker in ("eps=0.001", "rho=0.8", "peak k=4", "numerical ranks=2 -> 7"):
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
        help="rerun the deterministic LA-CUM gate twice and exercise blind parameter inputs",
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
        print(f"SKIP compute rerun (pass --run-compute for the formal LA-CUM audit); stored sha256={digest}")
    print("LA-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
