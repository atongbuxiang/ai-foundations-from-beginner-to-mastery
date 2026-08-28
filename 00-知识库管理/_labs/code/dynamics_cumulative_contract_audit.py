#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for DYN-CUM-01."""

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
DYN = ROOT / "10-数学基础" / "10.9-ODE、动力系统与SDE"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = DYN / "ODE、动力系统与 SDE MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - ODE、动力系统与 SDE（10.9）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - ODE、动力系统与 SDE（10.9）.md"
EXPERIMENT = LABS / "experiments" / "实验 - ODE、动力系统与 SDE 累计复现门.md"
TEACHING_AUDIT = LABS / "code" / "dynamics_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "dynamics_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "dynamics"
    / "plot-dynamics-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "b03decf286243fdfd16051a04ec70e1afb7b35c3369c24bd0a5e2856b90957cc"
EXPECTED_INTERVENTION_SHA256 = "65c1d45c002169e354facffb355c483560288af8633c0c263943cefabc4636b2"

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
        require("material_status: regression-passed" in content,
                f"{label}: material state is not regression-passed")
        require("learning_status: not-attempted" in content,
                f"{label}: personal state is not not-attempted")
        require("updated: 2026-08-28" in content, f"{label}: migration date missing")

    require("time_limit_minutes: 240" in assessment, "assessment time limit changed")
    require("assessment_id: DYN-CUM-01" in assessment, "assessment ID changed")
    require("assessment_id: DYN-CUM-01" in solution, "solution ID changed")
    for index in range(1, 13):
        require(f"DYN-{index:02d}" in assessment, f"assessment scope misses DYN-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")

    for marker in (
        "先看完整验收时间线",
        "20 分钟卷级口试",
        "四波模型链",
        "九层连续动力学对象账本",
        "时钟与 full/half-score 系数",
        "连续生成模型研究合同",
        "48 小时换机制重建门",
        "14 天陌生 AI 连续动力学迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses cumulative marker: {marker}")
    for marker in (
        "卷级口试参考要点",
        "四波模型链参考",
        "九层连续动力学对象账本参考",
        "时钟与 full/half-score 参考",
        "口试判分红线",
        "实验复现门的评分说明",
        "从 `retained` 到逐节点证据",
    ):
        require(marker in solution, f"solution misses oral/rubric marker: {marker}")

    forbidden_in_questions = (
        "### 第 1 题解答：",
        "## 七、卷级口试参考要点",
        "四波模型链参考",
        "口试判分红线",
    )
    leaked = [marker for marker in forbidden_in_questions if marker in assessment]
    require(not leaked, f"question/solution separation failed; leaked markers: {leaked}")
    require(
        'solution: "[[阶段测验解答 - ODE、动力系统与 SDE（10.9）]]"' in assessment,
        "assessment lost its explicit solution pointer",
    )
    require("才可打开本解答或 canonical 结果" in solution,
            "solution use-order warning is incomplete")

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
    require(sum(question_points.values()) == 100, "question point allocation no longer totals 100")
    for marker in (
        "答案与输出隔离协议",
        "九层连续动力学对象账本",
        "scorer nonce",
        "48 小时换机制重建门",
        "14 天陌生 AI 连续动力学迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses evidence marker: {marker}")
    for marker in (
        "四波统一模型的卷级数值锚点",
        "nonce 与盲参数判分红线",
        "最终状态边界",
    ):
        require(marker in solution, f"solution misses evidence marker: {marker}")
    print("PASS assessment bundle: scope 12/12, questions/answers 14/14, points=100, isolation + nonce + delay gates")


def audit_cumulative_route() -> None:
    moc = read(MOC)
    expected_row = (
        "| CUM | DYN-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 盲干预 → 订正 → 48 h / 14 d → 独立审计 | "
        "四波回链、三条主推导与 A/B/C 累计门 | `regression-passed` | `not-attempted` |"
    )
    require(expected_row in moc, "MOC cumulative status row is not regression-passed / not-attempted")
    for marker in (
        "DYN-CUM-01：卷末综合验收闭环",
        "20 分钟口试",
        "240 分钟闭卷",
        "48 小时换机制",
        "14 天陌生 AI 迁移",
        "DYN-CUM-01 材料证书",
        "从零如何执行 DYN-CUM-01",
        "dynamics_cumulative_contract_audit.py",
    ):
        require(marker in moc, f"MOC misses DYN-CUM marker: {marker}")

    for path in STATE_SURFACES:
        content = read(path)
        require("DYN-CUM-01" in content or "DYN-CUM" in content,
                f"state surface misses DYN-CUM: {path.relative_to(ROOT)}")
        require("dynamics_cumulative_contract_audit.py" in content,
                f"state surface misses independent audit: {path.relative_to(ROOT)}")
        require("regression-passed" in content,
                f"state surface does not report DYN-CUM material PASS: {path.relative_to(ROOT)}")
        require("not-attempted" in content,
                f"state surface lost personal not-attempted boundary: {path.relative_to(ROOT)}")
    print(f"PASS state surfaces: MOC plus {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "防止循环认证",
        "A 轨：连续稳定与离散稳定不是同一证书",
        "B 轨：解析密度、probability current 与 PF characteristics",
        "C 轨：Brownian path、Itô 与 reverse score 系数",
        "评分者随机指定的手工复核",
        "盲参数干预门",
        "盲测干预怎样才算独立",
        "审计使用的固定多参数盲测 fixture",
        "--density-sigma",
        "--brownian-steps",
        "证据状态机",
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
    # Written Q5: nonnormal flow at t = log(3)/2.
    time = 0.5 * math.log(3)
    exp_slow = math.exp(-time)
    exp_fast = math.exp(-3 * time)
    state = (5 * (exp_slow - exp_fast), exp_fast)
    norm = math.hypot(*state)
    require(math.isclose(state[0], 10 / (3 * math.sqrt(3)), abs_tol=3e-15),
            "nonnormal-flow first coordinate changed")
    require(math.isclose(state[1], 1 / (3 * math.sqrt(3)), abs_tol=3e-16),
            "nonnormal-flow second coordinate changed")
    require(math.isclose(norm, math.sqrt(101 / 27), abs_tol=4e-16),
            "nonnormal transient norm changed")
    require(math.isclose(math.exp(-4 * time), 1 / 9, abs_tol=2e-16),
            "nonnormal determinant changed")

    # Written Q7 and Q8: stability and OU score/current/reverse clock.
    require(math.isclose(2 / 40, 0.05, abs_tol=0.0), "Euler stability boundary changed")
    require(math.isclose(2.7853 / 40, 0.0696325, abs_tol=1e-15), "RK4 boundary changed")
    require(math.isclose(1 / (1 + 4), 0.2, abs_tol=0.0), "BE factor changed")
    require(math.isclose((1 - 2) / (1 + 2), -1 / 3, abs_tol=0.0), "trapezoidal factor changed")
    mean = 2 * math.exp(-math.log(2))
    variance = 1 + 3 * math.exp(-2 * math.log(2))
    require(mean == 1.0 and variance == 1.75, "written OU marginal changed")
    score_slope = -1 / variance
    require(math.isclose(score_slope, -4 / 7, abs_tol=0.0), "written OU score changed")
    score_at_mean = score_slope * (mean - mean)
    pf_at_mean = -mean - score_at_mean
    reverse_at_mean = mean + 2 * score_at_mean
    require((score_at_mean, pf_at_mean, reverse_at_mean) == (0.0, -1.0, 1.0),
            "OU current/reverse sanity check changed")

    # Cumulative A track canonical stability factors.
    z = -80 / 25
    euler = 1 + z
    rk4 = 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24
    backward_euler = 1 / (1 - z)
    trapezoidal = (1 + z / 2) / (1 - z / 2)
    expected = (-2.2, 1.827733333333334, 0.23809523809523808, -0.23076923076923078)
    for value, target in zip((euler, rk4, backward_euler, trapezoidal), expected):
        require(math.isclose(value, target, abs_tol=2e-15), "cumulative A stability factor changed")

    # Cumulative B analytic Fourier density and continuity residual.
    amplitude0 = 0.65
    sigma = 1.1
    for current_time in (0.0, 0.3, 0.8):
        amplitude = amplitude0 * math.exp(-0.5 * sigma ** 2 * current_time)
        for state_value in (-2.0, 0.0, 1.25):
            density = (1 + amplitude * math.cos(state_value)) / (2 * math.pi)
            dt_density = -(sigma ** 2 * amplitude * math.cos(state_value)) / (4 * math.pi)
            flux_derivative = sigma ** 2 * amplitude * math.cos(state_value) / (4 * math.pi)
            require(density > 0, "cumulative B density lost positivity")
            require(math.isclose(dt_density + flux_derivative, 0.0, abs_tol=0.0),
                    "cumulative B continuity residual changed")

    # Cumulative C full/half score and stationary sanity checks.
    beta = 2.0
    final_time = 0.6
    require(math.isclose(beta * final_time, 1.2, abs_tol=0.0), "cumulative C QV target changed")
    require(math.isclose(1 + beta * final_time, 2.2, abs_tol=0.0),
            "cumulative C wrong-half-score moment changed")
    for state_value in (-2.0, 0.0, 1.5):
        score = -state_value
        pf_velocity = -0.5 * beta * state_value - 0.5 * beta * score
        reverse_sde = 0.5 * beta * state_value + beta * score
        reverse_pf = 0.5 * beta * state_value + 0.5 * beta * score
        require(pf_velocity == 0.0 and reverse_pf == 0.0,
                "stationary probability-flow coefficient changed")
        require(reverse_sde == -0.5 * beta * state_value,
                "stationary reverse-SDE full-score coefficient changed")

    # Fixed blind fixture: independently derive all mechanism-changing targets.
    blind_z = -50.0 / 30.0
    blind_euler = 1.0 + blind_z
    blind_rk4 = 1.0 + blind_z + blind_z**2 / 2.0 + blind_z**3 / 6.0 + blind_z**4 / 24.0
    blind_be = 1.0 / (1.0 - blind_z)
    blind_trap = (1.0 + blind_z / 2.0) / (1.0 - blind_z / 2.0)
    for value, target in zip(
        (blind_euler, blind_rk4, blind_be, blind_trap),
        (-2.0 / 3.0, 0.2721193415637861, 3.0 / 8.0, 1.0 / 11.0),
    ):
        require(math.isclose(value, target, abs_tol=2e-15), "blind A stability factor changed")
    require(all(abs(value) < 1.0 for value in (blind_euler, blind_rk4, blind_be, blind_trap)),
            "blind A stability classification changed")

    blind_a0, blind_sigma, blind_time = 0.8, 0.9, 1.0
    blind_amplitude = blind_a0 * math.exp(-0.5 * blind_sigma**2 * blind_time)
    require(math.isclose(1.0 - blind_a0, 0.2, abs_tol=0.0), "blind B positivity margin changed")
    require(math.isclose(blind_amplitude, 0.5335814486867795, abs_tol=2e-16),
            "blind B terminal Fourier amplitude changed")
    for state_value in (-2.0, 0.0, 1.25):
        dt_density = -(blind_sigma**2 * blind_amplitude * math.cos(state_value)) / (4.0 * math.pi)
        flux_divergence = -dt_density
        require(math.isclose(dt_density + flux_divergence, 0.0, abs_tol=0.0),
                "blind B continuity residual changed")

    blind_beta, blind_stochastic_time = 1.5, 0.75
    require(math.isclose(blind_beta * blind_stochastic_time, 1.125, abs_tol=0.0),
            "blind C QV target changed")
    require(math.isclose(1.0 + blind_beta * blind_stochastic_time, 2.125, abs_tol=0.0),
            "blind C half-score moment target changed")

    print("PASS exact cumulative models: written anchors, canonical A/B/C and fixed blind mechanisms")


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
    position = positions[0]
    block = "\n".join(experiment_lines[position : min(len(experiment_lines), position + 45)])
    for marker in ("[!figure]", "怎样读图", "适用边界"):
        require(marker in block, f"cumulative figure unit misses {marker}")
    print(f"PASS cumulative Markdown: Wiki links={link_count}, display math balanced, figure unit complete")


def stored_artifact_digest() -> str:
    require(CUM_SVG.is_file(), "cumulative SVG is missing")
    digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {digest}")
    root_element = ET.parse(CUM_SVG).getroot()
    require(root_element.tag.endswith("svg") and "viewBox" in root_element.attrib,
            "cumulative SVG failed XML/viewBox validation")
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
    require("DYN-01—12 material regression: PASS" in teaching_output,
            "chapter teaching audit did not reach its material PASS")

    with tempfile.TemporaryDirectory(prefix="dyn-cum-audit-") as temporary_directory:
        temporary = Path(temporary_directory)
        canonical_a = temporary / "canonical-a.svg"
        canonical_b = temporary / "canonical-b.svg"
        first_output = run(CUM_SCRIPT, "--output", str(canonical_a))
        second_output = run(CUM_SCRIPT, "--output", str(canonical_b))
        require(normalized_output(first_output) == normalized_output(second_output),
                "canonical stdout changed across two runs")
        require(canonical_a.read_bytes() == canonical_b.read_bytes(),
                "canonical SVG bytes changed across two runs")
        first_digest = hashlib.sha256(canonical_a.read_bytes()).hexdigest()
        require(first_digest == EXPECTED_CUM_SHA256, f"fresh canonical SVG hash changed: {first_digest}")
        for marker in (
            "A_CONFIG stiffness=80 plot_steps=25",
            "A_DYNAMICS z_fast=-3.200000 factors EE=-2.20000000 RK4=1.82773333 BE=0.23809524 Trap=-0.23076923",
            "A_ORDERS EE=1.00216894 RK4=3.92818205 BE=0.99784827 Trap=2.00000782",
            "B_CONFIG density_a=0.65 density_sigma=1.1 density_time=0.8",
            "B_TRANSPORT state_order=4.03145834 logp_order=4.04224788 mass_drift=4.441e-16 pde_residual=0.000e+00",
            "C_CONFIG beta=2 stochastic_time=0.6 paths=2048 brownian_steps=512 seed=20260819",
            "C_STOCHASTIC qv=1.19888410 target=1.20000000 ito_order=0.49850219 full_m2=0.97673218 half_m2=2.14844674 half_target=2.20000000",
            f"SHA256 {EXPECTED_CUM_SHA256}",
        ):
            require(marker in first_output, f"canonical output misses: {marker}")
        root_element = ET.parse(canonical_a).getroot()
        require(root_element.tag.endswith("svg") and "viewBox" in root_element.attrib,
                "fresh cumulative SVG failed XML/viewBox validation")

        unsafe_run = subprocess.run(
            [sys.executable, str(CUM_SCRIPT), "--stiffness", "50"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        require(unsafe_run.returncode != 0, "noncanonical run without --output could overwrite canonical SVG")
        require("noncanonical runs require --output" in unsafe_run.stderr,
                "noncanonical output-protection error message drifted")

        intervention = temporary / "blind.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--stiffness", "50",
            "--plot-steps", "30",
            "--density-a", "0.8",
            "--density-sigma", "0.9",
            "--density-time", "1.0",
            "--beta", "1.5",
            "--stochastic-time", "0.75",
            "--paths", "1536",
            "--brownian-steps", "384",
            "--seed", "20260828",
            "--output", str(intervention),
        )
        intervention_digest = hashlib.sha256(intervention.read_bytes()).hexdigest()
        require(intervention_digest == EXPECTED_INTERVENTION_SHA256,
                f"blind intervention SVG hash changed: {intervention_digest}")
        for marker in (
            "A_CONFIG stiffness=50 plot_steps=30",
            "A_DYNAMICS z_fast=-1.666667 factors EE=-0.66666667 RK4=0.27211934 BE=0.37500000 Trap=0.09090909",
            "A_ORDERS EE=1.00216894 RK4=3.92818205 BE=0.99784827 Trap=2.00000782",
            "B_CONFIG density_a=0.8 density_sigma=0.9 density_time=1",
            "B_TRANSPORT state_order=4.05597835 logp_order=4.05653516 mass_drift=4.441e-16 pde_residual=0.000e+00",
            "C_CONFIG beta=1.5 stochastic_time=0.75 paths=1536 brownian_steps=384 seed=20260828",
            "C_STOCHASTIC qv=1.12838453 target=1.12500000 ito_order=0.49776175 full_m2=0.99961395 half_m2=2.13623152 half_target=2.12500000",
            f"SHA256 {EXPECTED_INTERVENTION_SHA256}",
        ):
            require(marker in intervention_output, f"blind output misses: {marker}")
        intervention_svg = intervention.read_text(encoding="utf-8")
        for marker in (
            "x′=−x, y′=−50y；V′≤−2V；h=0.033",
            "a₀=0.8, σ=0.9, T=1；p=(1+a(t) cos x)/(2π)",
            "OU；β=1.5, T=0.75, paths=1536, N=384",
            "analytic half-score target=1+βT=2.1250",
        ):
            require(marker in intervention_svg, f"blind SVG does not self-describe: {marker}")
        ET.parse(intervention)

    print("PASS chapter compute dependency: DYN-01—12 teaching/figure regression")
    print(f"PASS canonical double-run + stored SVG: sha256={first_digest}")
    print(f"PASS blind-interface intervention: sha256={EXPECTED_INTERVENTION_SHA256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="rerun DYN-01--12 figures and the deterministic DYN-CUM-01 three-track gate",
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
        print(f"SKIP compute rerun (pass --run-compute for the formal DYN-CUM-01 audit); stored sha256={digest}")
    print("DYN-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
