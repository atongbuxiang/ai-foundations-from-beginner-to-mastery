#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for OPT-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OPT = ROOT / "10-数学基础" / "10.7-优化与凸分析"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = OPT / "优化与凸分析 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 优化与凸分析（10.7）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 优化与凸分析（10.7）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 优化与凸分析累计复现门.md"
TEACHING_AUDIT = LABS / "code" / "optimization_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "plot_optimization_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "optimization"
    / "plot-optimization-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "6df184dc5a75e125d1cf2f1595574007538cdd1321efa8690dcf14cf0e6230b6"
EXPECTED_INTERVENTION_SHA256 = "e991ef5318f95ba6422c0b72d2c9b9e9e04ec91cbe6c82c4eb9d310a0fec21aa"

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    ROOT / "00-知识库管理" / "00-总览" / "数学基础十卷完备性审计与学习状态总表.md",
    ROOT / "00-知识库管理" / "_labs" / "exercises" / "练习与测验 MOC.md",
    ROOT / "00-知识库管理" / "_labs" / "推导与实验 MOC.md",
)

CONCEPTS = (
    "优化问题、可行域与局部最优.md",
    "凸集、凸组合与分离超平面.md",
    "凸函数、Jensen 不等式与上图集.md",
    "次梯度、共轭函数与 Fenchel 对偶.md",
    "光滑性、强凸性与条件数.md",
    "一阶最优性条件与梯度下降.md",
    "加速梯度、动量与下界.md",
    "随机梯度与小批量估计.md",
    "自适应优化方法.md",
    "Newton 法、Gauss-Newton 与拟 Newton 法.md",
    "投影、约束与可行方向.md",
    "Lagrange 乘子与 KKT 条件.md",
    "弱对偶、强对偶与 Slater 条件.md",
    "近端算子、复合优化与稀疏正则.md",
    "镜像下降、Bregman 几何与自然梯度.md",
    "非凸优化、鞍点与深度网络损失地形.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "核心公式七问",
    "第一遍停靠线",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def close(actual: float, expected: float, label: str, tolerance: float = 5e-9) -> None:
    require(
        math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance),
        f"{label}: expected {expected:.10f}, got {actual:.10f}",
    )


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_lines(text: str) -> list[str]:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in text.splitlines():
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


def audit_concepts() -> None:
    for filename in CONCEPTS:
        text = read(OPT / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in text, f"{filename}: migration date missing")
    print(f"PASS concept contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    for path, text in ((ASSESSMENT, assessment), (SOLUTION, solution), (EXPERIMENT, experiment)):
        require("material_status: regression-passed" in text, f"{path.name}: material status drift")
        require("learning_status: not-attempted" in text, f"{path.name}: learning status drift")
        require("updated: 2026-08-28" in text, f"{path.name}: update date drift")
    for index in range(1, 17):
        require(f"OPT-{index:02d}" in assessment, f"assessment scope misses OPT-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")
    for marker in ("15 分钟卷级口试", "四波模型链", "AI claim ladder"):
        require(marker in assessment, f"assessment misses oral-gate marker: {marker}")
    for marker in ("卷级口试参考要点", "四波模型链参考", "口试判分红线"):
        require(marker in solution, f"solution misses oral-rubric marker: {marker}")
    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第 (\d+) 题：.*（(\d+) 分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第 (\d+) 题解答：.*（(\d+) 分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 15)), "assessment point headers are incomplete")
    require(sorted(solution_points) == list(range(1, 15)), "solution point headers are incomplete")
    require(question_points == solution_points, "question/solution point allocations differ")
    require(sum(question_points.values()) == 100, "assessment points do not total 100")
    for marker in (
        "答案与输出隔离协议",
        "attempt_id",
        "scorer nonce",
        "48 小时换机制重建门",
        "14 天陌生 AI 优化迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses evidence marker: {marker}")
    for marker in ("四波统一模型的卷级数值锚点", "口试与盲干预判分红线", "最终状态边界"):
        require(marker in solution, f"solution misses evidence marker: {marker}")
    print("PASS assessment bundle: scope 16/16, questions/answers 14/14, points=100, isolation + delay gates")


def audit_analytic_calibration() -> None:
    # Wave A: Euclidean projection/Fenchel calibration.
    anchor = (Fraction(1), Fraction(1))
    x_star = (Fraction(1, 2), Fraction(1, 2))
    projection_residual = tuple(first - second for first, second in zip(anchor, x_star))
    primal_value = Fraction(1, 2) * sum(value * value for value in projection_residual)
    vertices = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    projection_inner_products = tuple(
        sum(residual * (coordinate - optimum) for residual, coordinate, optimum in zip(projection_residual, vertex, x_star))
        for vertex in vertices
    )
    endpoint_value = Fraction(1, 2) * sum(
        (coordinate - target) ** 2 for coordinate, target in zip(vertices[1], anchor)
    )
    jensen_gap = Fraction(1, 2) * (endpoint_value + endpoint_value) - primal_value
    require(primal_value == Fraction(1, 4), "Wave A projection value drift")
    require(jensen_gap == primal_value, "Wave A Jensen anchor drift")
    require(projection_inner_products == (Fraction(-1, 2), Fraction(0), Fraction(0)), "Wave A variational inequality drift")
    require(sum(x_star, Fraction(0, 1)) == 1, "Wave A boundary point drift")

    # Wave B: spectral GD and stationary covariance under isotropic noise.
    eigenvalues = (Fraction(1, 1), Fraction(4, 1))
    eta_quarter = Fraction(1, 4)
    eta_two_fifths = Fraction(2, 5)
    factors_quarter = tuple(1 - eta_quarter * value for value in eigenvalues)
    factors_two_fifths = tuple(1 - eta_two_fifths * value for value in eigenvalues)
    injection = Fraction(1, 2) * eta_quarter**2 * sum(eigenvalues)
    floor = sum(
        Fraction(1, 2) * value * eta_quarter**2 / (1 - (1 - eta_quarter * value) ** 2)
        for value in eigenvalues
    )
    require(factors_quarter == (Fraction(3, 4), Fraction(0, 1)), "Wave B eta=1/4 factors drift")
    require(factors_two_fifths == (Fraction(3, 5), Fraction(-3, 5)), "Wave B eta=2/5 factors drift")
    require(injection == Fraction(5, 32), "Wave B noise injection drift")
    require(floor == Fraction(11, 56), "Wave B noise floor drift")
    # Optimal heavy-ball parameters for mu=1, L=4 give alpha=4/9, beta=1/9.
    alpha, beta = Fraction(4, 9), Fraction(1, 9)
    for eigenvalue, expected_root in ((Fraction(1), Fraction(1, 3)), (Fraction(4), Fraction(-1, 3))):
        coefficient = 1 + beta - alpha * eigenvalue
        require(coefficient == 2 * expected_root, "Wave B HB repeated-root coefficient drift")
        require(beta == expected_root**2, "Wave B HB repeated-root product drift")

    # Wave C: unconstrained point, Euclidean/H-metric projections and KKT.
    unconstrained = (Fraction(1), Fraction(5, 8))
    euclidean_projection = (Fraction(11, 16), Fraction(5, 16))
    h_projection = x_star
    multiplier = Fraction(1, 2)
    objective = Fraction(1, 2) * (h_projection[0] ** 2 + 4 * h_projection[1] ** 2) - h_projection[0] - Fraction(5, 2) * h_projection[1]
    require(sum(euclidean_projection, Fraction(0)) == 1, "Wave C Euclidean projection drift")
    require(unconstrained == (Fraction(1), Fraction(5, 8)), "Wave C unconstrained point drift")
    require(multiplier == Fraction(1, 2), "Wave C multiplier drift")
    require(objective == Fraction(-9, 8), "Wave C objective drift")

    # Wave D: dual/prox/Fisher and scale-symmetry anchors.
    b = (Fraction(1), Fraction(5, 2))
    h_inverse = (Fraction(1), Fraction(1, 4))

    def dual_value(lagrange_multiplier: Fraction) -> Fraction:
        shifted = tuple(value - lagrange_multiplier for value in b)
        quadratic = sum(weight * value**2 for weight, value in zip(h_inverse, shifted))
        return -Fraction(1, 2) * quadratic - lagrange_multiplier

    dual_at_zero = dual_value(Fraction(0))
    dual_at_optimum = dual_value(multiplier)
    require(dual_at_zero == Fraction(-41, 32), "Wave D initial dual value drift")
    require(objective - dual_at_zero == Fraction(5, 32), "Wave D initial dual gap drift")
    require(dual_at_optimum == objective, "Wave D zero dual gap drift")

    regularization = Fraction(1, 2)
    prox_eta = Fraction(1, 4)
    forward_point = tuple(prox_eta * value for value in b)
    threshold = prox_eta * regularization
    prox_iterate = tuple(max(Fraction(0), value - threshold) for value in forward_point)

    def composite_value(point: tuple[Fraction, Fraction]) -> Fraction:
        smooth = Fraction(1, 2) * (point[0] ** 2 + 4 * point[1] ** 2) - b[0] * point[0] - b[1] * point[1]
        return smooth + regularization * sum(abs(value) for value in point)

    prox_gap = composite_value(prox_iterate) - composite_value(x_star)
    require(forward_point == (Fraction(1, 4), Fraction(5, 8)), "Wave D forward point drift")
    require(prox_iterate == (Fraction(1, 8), Fraction(1, 2)), "Wave D proximal iterate drift")
    require(prox_gap == Fraction(9, 128), "Wave D proximal gap drift")
    fisher = Fraction(16, 3)
    local_gradient = Fraction(5, 4)
    natural_direction = local_gradient / fisher
    require(natural_direction == Fraction(15, 64), "Wave D Fisher direction drift")
    factor_hessian = ((0, -1), (-1, 0))
    require(factor_hessian[0][1] == factor_hessian[1][0] == -1, "Wave D saddle Hessian drift")
    require(
        tuple(factor_hessian[0][index] + factor_hessian[1][index] for index in range(2)) == (-1, -1),
        "Wave D negative-eigenvector drift",
    )
    close(1.0**2 + 1.0**-2, 2.0, "balanced factor sharpness")
    close(10.0**2 + 10.0**-2, 100.01, "rescaled factor sharpness")
    print("PASS four-wave analytic calibration: projection/Fenchel, spectral/noise, KKT/metric, dual/prox/Fisher/symmetry")


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)
    require(
        "| CUM | OPT-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 盲干预 → 订正 → 48 h / 14 d → 独立审计 | `regression-passed / not-attempted` |"
        in moc,
        "MOC cumulative material status is not regression-passed",
    )
    for marker in (
        "怎样从零真正学完本卷",
        "三遍学习",
        "五层证据",
        "卷级总图",
        "optimization_cumulative_contract_audit.py",
    ):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "A 轨：严格鞍点",
        "B 轨：非凸而满足 PL",
        "C 轨：尺度对称",
        "盲参数干预门",
        "--stable-y0",
        "--pl-x-max",
        "--scale-span",
        "证据状态机与延迟迁移",
    ):
        require(marker in experiment, f"experiment misses track marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(TEACHING_AUDIT.is_file() and CUM_SCRIPT.is_file(), "required compute scripts missing")
    for path in STATE_SURFACES:
        state_text = read(path)
        require("optimization_cumulative_contract_audit.py" in state_text, f"state surface misses audit: {path.name}")
        require("regression-passed" in state_text, f"state surface misses material pass: {path.name}")
        require("not-attempted" in state_text, f"state surface misses personal boundary: {path.name}")
    print("PASS cumulative artifacts: oral/closed/nonce/blind/delay route + 6 synchronized state surfaces")


def audit_markdown_integrity() -> None:
    scoped = [OPT / filename for filename in CONCEPTS] + [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    math_findings: list[str] = []
    for path in scoped:
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
        if active.count("$$") % 2:
            math_findings.append(str(path.relative_to(ROOT)))
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
                    candidates = [
                        candidate
                        for candidate in candidates
                        if candidate.suffix.lower() == suffix
                    ]
            if not candidates:
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")

    require(not math_findings, f"unbalanced display math: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    figure_count = 0
    figure_findings: list[str] = []
    image_pattern = re.compile(
        r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]",
        re.I,
    )
    for path in [OPT / filename for filename in CONCEPTS] + [MOC, EXPERIMENT]:
        lines = read(path).splitlines()
        positions = [index for index, line in enumerate(lines) if image_pattern.search(line)]
        for order, position in enumerate(positions):
            figure_count += 1
            stop = positions[order + 1] if order + 1 < len(positions) else min(
                len(lines), position + 45
            )
            block = "\n".join(lines[position : min(stop, position + 45)])
            missing = [
                marker
                for marker in ("[!figure]", "怎样读图", "适用边界")
                if marker not in block
            ]
            if missing:
                figure_findings.append(
                    f"{path.relative_to(ROOT)}:{position + 1} missing {missing}"
                )
            match = image_pattern.search(lines[position])
            require(match is not None, "internal image parser failure")
            image_path = ROOT / match.group(1)
            require(image_path.is_file(), f"missing embedded image: {match.group(1)}")
            if image_path.suffix.lower() == ".svg":
                root_element = ET.parse(image_path).getroot()
                require(root_element.tag.endswith("svg"), f"invalid SVG root: {match.group(1)}")
                require("viewBox" in root_element.attrib, f"SVG missing viewBox: {match.group(1)}")

    require(not figure_findings, f"incomplete figure units: {figure_findings}")
    print(
        f"PASS Markdown integrity: Wiki links={link_count}, display math balanced; "
        f"figure units/SVG XML={figure_count}"
    )


def run(script: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    require(
        result.returncode == 0,
        f"compute failed ({script.name} {' '.join(args)}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
    )
    return result.stdout.strip()


def normalized_output(output: str) -> str:
    return "\n".join(line for line in output.splitlines() if not line.startswith("OUTPUT "))


def audit_compute() -> None:
    teaching_output = run(TEACHING_AUDIT, "--run-figures")
    require(
        "OPT-01—16 material regression: PASS" in teaching_output,
        "chapter teaching audit did not pass",
    )
    require(CUM_SVG.is_file(), "stored cumulative SVG is missing")
    stored_digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(stored_digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {stored_digest}")
    with tempfile.TemporaryDirectory(prefix="opt-cum-audit-") as temp_dir:
        temp = Path(temp_dir)
        canonical_a = temp / "canonical-a.svg"
        canonical_b = temp / "canonical-b.svg"
        output_a = run(CUM_SCRIPT, "--output", str(canonical_a))
        output_b = run(CUM_SCRIPT, "--output", str(canonical_b))
        require(normalized_output(output_a) == normalized_output(output_b), "canonical stdout is not deterministic")
        require(canonical_a.read_bytes() == canonical_b.read_bytes(), "canonical SVG double-run differs")
        digest = hashlib.sha256(canonical_a.read_bytes()).hexdigest()
        require(digest == EXPECTED_CUM_SHA256, f"canonical SVG hash changed: {digest}")
        for marker in (
            "A_CONFIG perturbation=0.001 stable_y0=0 eta=0.1 steps=160",
            "A_SADDLE exact_f=0.25000000 perturbed_f=2.80041313e-18 final_x=1.00000000",
            "B_CONFIG a=0.5 x_max=8",
            "B_PL mu=0.25000000 sampled_min_ratio=0.25000063 sampled_min_hessian=-3.34234789 at_x=-8.00000",
            "C_CONFIG scale_span=1",
            "C_SHARPNESS balanced=2.00000 extreme=100.01000",
        ):
            require(marker in output_a, f"canonical output misses: {marker}")
        ET.parse(canonical_a)

        intervention = temp / "intervention.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--perturbation", "0.005",
            "--stable-y0", "0.8",
            "--eta", "0.08",
            "--steps", "220",
            "--pl-a", "0.3",
            "--pl-x-max", "10",
            "--scale-span", "1.25",
            "--output", str(intervention),
        )
        intervention_digest = hashlib.sha256(intervention.read_bytes()).hexdigest()
        require(intervention_digest == EXPECTED_INTERVENTION_SHA256, f"intervention SVG hash changed: {intervention_digest}")
        for marker in (
            "A_CONFIG perturbation=0.005 stable_y0=0.8 eta=0.08 steps=220",
            "A_SADDLE exact_f=0.25000000 perturbed_f=3.73073197e-17 final_x=1.00000000",
            "B_CONFIG a=0.3 x_max=10",
            "B_PL mu=0.49000000 sampled_min_ratio=0.49000001 sampled_min_hessian=-1.58861185 at_x=-8.17500",
            "C_CONFIG scale_span=1.25",
            "C_SHARPNESS balanced=2.00000 extreme=316.23093",
        ):
            require(marker in intervention_output, f"intervention output misses: {marker}")
        ET.parse(intervention)

    print(f"PASS canonical double-run + stored SVG: sha256={stored_digest}")
    print(f"PASS blind-interface intervention: sha256={EXPECTED_INTERVENTION_SHA256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="also rerun all teaching figures and the deterministic cumulative compute gate",
    )
    args = parser.parse_args()
    audit_concepts()
    audit_assessment_bundle()
    audit_analytic_calibration()
    audit_cumulative_artifacts()
    audit_markdown_integrity()
    if args.run_compute:
        audit_compute()
    else:
        print("SKIP compute gates (pass --run-compute for the formal OPT-CUM audit)")
    print("OPT-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
