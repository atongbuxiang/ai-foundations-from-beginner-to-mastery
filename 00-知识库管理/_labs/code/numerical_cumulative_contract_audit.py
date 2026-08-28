#!/usr/bin/env python3
"""Audit the static and reproducible teaching contract for NLA-CUM-01."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NUM = ROOT / "10-数学基础" / "10.8-数值计算"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = NUM / "数值线性代数 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 数值计算与数值线性代数（10.8）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 数值计算与数值线性代数（10.8）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 数值线性代数累计复现门.md"
TEACHING_AUDIT = LABS / "code" / "numerical_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "plot_numerical_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "numerical-analysis"
    / "fig-numerical-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "895af1e191506d2ada074b104eea71820af2063bc5abc522e6dce17d9b506682"
EXPECTED_INTERVENTION_SHA256 = "5b7757faa73347b469647a0fae5970e356fad39567f241e414c2ef5fbd50c706"

STATE_SURFACES = (
    ROOT / "10-数学基础" / "数学基础完整课程地图与掌握标准.md",
    ROOT / "10-数学基础" / "数学基础 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    ROOT / "00-知识库管理" / "00-总览" / "数学基础十卷完备性审计与学习状态总表.md",
    ROOT / "00-知识库管理" / "_labs" / "exercises" / "练习与测验 MOC.md",
    ROOT / "00-知识库管理" / "_labs" / "推导与实验 MOC.md",
)

CONCEPTS = (
    "浮点数与舍入误差.md",
    "前向误差与后向误差.md",
    "数值稳定性.md",
    "误差传播、条件估计与停止准则.md",
    "稳定求和、点积与矩阵乘法.md",
    "稳定求解线性方程组.md",
    "迭代改进、混合精度与残差校正.md",
    "Householder 与 Givens 变换.md",
    "稳定最小二乘与正规方程的风险.md",
    "幂法、反幂法与 Rayleigh 商迭代.md",
    "Hessenberg 化与 QR 特征值算法.md",
    "Lanczos 方法.md",
    "Arnoldi 方法.md",
    "SVD 算法与谱范数估计.md",
    "定常迭代法与谱半径.md",
    "Krylov 子空间与预条件.md",
    "共轭梯度法.md",
    "GMRES、MINRES 与残差最小化.md",
    "稀疏矩阵计算与存储复杂度.md",
    "随机化低秩近似与随机 SVD.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "符号与对象账本",
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


def active_lines(content: str) -> list[str]:
    """Drop fenced code while retaining prose, formulas, links and callouts."""
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


def audit_concepts() -> None:
    for filename in CONCEPTS:
        content = read(NUM / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in content]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in content, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in content, f"{filename}: migration date missing")
    print(f"PASS concept contracts: {len(CONCEPTS)}/{len(CONCEPTS)}; learning state remains draft")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)

    for path, content in ((ASSESSMENT, assessment), (SOLUTION, solution), (EXPERIMENT, experiment)):
        require("material_status: regression-passed" in content, f"{path.name}: material status drift")
        require("learning_status: not-attempted" in content, f"{path.name}: learning status drift")
        require("updated: 2026-08-28" in content, f"{path.name}: update date drift")

    for index in range(1, 21):
        require(f"NUM-{index:02d}" in assessment, f"assessment scope misses NUM-{index:02d}")
    for index in range(1, 15):
        require(f"### 第 {index} 题：" in assessment, f"assessment misses question {index}")
        require(f"### 第 {index} 题解答：" in solution, f"solution misses answer {index}")

    for marker in ("15 分钟卷级口试", "五波模型链", "五种不能混写的量", "AI 数值研究合同"):
        require(marker in assessment, f"assessment misses oral-gate marker: {marker}")
    for marker in ("卷级口试参考要点", "五波模型链参考", "口试判分红线", "AI 数值研究合同参考"):
        require(marker in solution, f"solution misses oral-rubric marker: {marker}")

    # The question file may link to the solution, but it must not contain answer headings or oral rubrics.
    forbidden_in_questions = (
        "### 第 1 题解答：",
        "#### 14.1 算子与形状",
        "## 六、卷级口试参考要点",
        "口试判分红线与记录",
    )
    leaked = [marker for marker in forbidden_in_questions if marker in assessment]
    require(not leaked, f"question/solution separation failed; leaked markers: {leaked}")
    require('solution: "[[阶段测验解答 - 数值计算与数值线性代数（10.8）]]"' in assessment,
            "assessment frontmatter lost the explicit solution pointer")
    require("正式作答前" not in solution or "冻结" in solution,
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
    require(sum(question_points.values()) == 100, "assessment points do not total 100")
    for marker in (
        "答案与输出隔离协议",
        "attempt_id",
        "scorer nonce",
        "48 小时换机制重建门",
        "14 天陌生 AI 数值迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses evidence marker: {marker}")
    for marker in ("五波统一模型的卷级数值锚点", "口试与盲干预判分红线", "最终状态边界"):
        require(marker in solution, f"solution misses evidence marker: {marker}")

    print("PASS assessment bundle: scope 20/20, questions/answers 14/14, points=100, isolation + delay gates")


def audit_analytic_calibration() -> None:
    # Track A: finite precision, residual, conditioning and task tolerance.
    tau = Fraction(1, 10_000)
    with localcontext(Context(prec=4, rounding=ROUND_HALF_EVEN, Emin=-999, Emax=999)):
        rounded = +(Decimal(1) + Decimal("0.0001"))
        lost_sum = +(+(Decimal("1e8") + Decimal(1)) - Decimal("1e8"))
        reordered_sum = +(+(Decimal("1e8") - Decimal("1e8")) + Decimal(1))
    require(str(rounded) == "1.000", "Track A decimal absorption drift")
    require(lost_sum == 0 and reordered_sum == 1, "Track A summation path drift")
    close(1.0 / math.sqrt(2.0), 0.7071067811865476, "Track A forward error")
    residual = float(tau) / math.sqrt(1.0 + float(tau) ** 2)
    condition = float(1 / tau)
    close(residual, 0.0000999999995, "Track A residual", tolerance=1e-12)
    close(condition * residual, 0.999999995, "Track A condition-amplified risk")
    close(0.01 / condition, 1e-6, "Track A task gate", tolerance=1e-15)

    # Track B: exact CG, GMRES, nonnormal Richardson and preconditioning.
    h = ((Fraction(1), Fraction(2)), (Fraction(2), Fraction(5)))
    r0 = (Fraction(-1), Fraction(-3))
    hp0 = tuple(sum(h[row][column] * r0[column] for column in range(2)) for row in range(2))
    alpha0 = sum(value * value for value in r0) / sum(r0[index] * hp0[index] for index in range(2))
    r1 = tuple(r0[index] - alpha0 * hp0[index] for index in range(2))
    relative_residual = math.sqrt(float(sum(value * value for value in r1) / sum(value * value for value in r0)))
    error1 = (Fraction(34, 29), Fraction(-14, 29))
    h_error1 = tuple(sum(h[row][column] * error1[column] for column in range(2)) for row in range(2))
    energy1 = sum(error1[index] * h_error1[index] for index in range(2))
    require(alpha0 == Fraction(5, 29), "Track B CG alpha drift")
    close(relative_residual, 2.0 / 29.0, "Track B CG relative residual")
    require(energy1 == Fraction(8, 29), "Track B CG energy error drift")
    close(math.sqrt(2.0 / 5.0), 0.6324555320336759, "Track B GMRES one-step residual")
    richardson_step = Fraction(1, 2)
    richardson_factors = (1 - richardson_step, 1 - 3 * richardson_step)
    require(richardson_factors == (Fraction(1, 2), Fraction(-1, 2)), "Track B Richardson spectrum drift")
    close(math.sqrt(5.0 / 4.0), 1.118033988749895, "Track B transient peak")
    close(27.0 + 18.0 * math.sqrt(2.0), 52.45584412271571, "Track B Gram condition")
    close(9.0 + 4.0 * math.sqrt(5.0), 17.94427190999916, "Track B scaled condition")

    # Track C: exact byte ledger and range/truncation/power separation.
    n, nnz_a, nnz_gram = 3, 4, 5
    value_bytes, index_bytes = 8, 4
    csr_a = nnz_a * (value_bytes + index_bytes) + (n + 1) * index_bytes
    dense_a = n * n * value_bytes
    csr_gram = nnz_gram * (value_bytes + index_bytes) + (n + 1) * index_bytes
    require((csr_a, dense_a, csr_gram) == (64, 72, 76), "Track C byte ledger drift")
    range_error = 3.0 / math.sqrt(23.0)
    best_rank2 = math.sqrt(2.0) - 1.0
    power_tail = (3.0 - 2.0 * math.sqrt(2.0)) ** 3
    close(range_error, 0.6255432421712244, "Track C range error")
    close(best_rank2, 0.41421356237309515, "Track C rank-2 error")
    close(power_tail, 0.005050633883346584, "Track C power-tail ratio")
    require(range_error > best_rank2 > power_tail > 0.0, "Track C error ordering drift")
    print("PASS analytic calibration: finite precision/condition, CG/GMRES/nonnormal solve, sparse/randomized ledger")


def audit_cumulative_artifacts() -> None:
    moc = read(MOC)
    experiment = read(EXPERIMENT)

    require(
        "| CUM | NLA-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 盲干预 → 订正 → 48 h / 14 d → 独立审计 | 五波回链与 A/B/C 累计三轨 | `regression-passed` | `not-attempted` |"
        in moc,
        "MOC cumulative status row is not regression-passed / not-attempted",
    )
    for marker in (
        "怎样从零真正学完本卷",
        "三遍学习",
        "五层证据",
        "卷级总图",
        "口试—闭卷—实验组合门",
        "numerical_cumulative_contract_audit.py",
    ):
        require(marker in moc, f"MOC misses cumulative marker: {marker}")

    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "A 轨：有限精度—误差—稳定—停止",
        "B 轨：结构—投影—预条件—真 residual",
        "C 轨：稀疏成本—随机值域—独立证书",
        "盲参数干预门",
        "--task-budget",
        "--richardson-step",
        "--value-bytes",
        "--power-iterations",
        "证据状态机与延迟迁移",
        EXPECTED_CUM_SHA256,
    ):
        require(marker in experiment, f"experiment misses cumulative marker: {marker}")

    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    require(TEACHING_AUDIT.is_file() and CUM_SCRIPT.is_file(), "required audit/compute scripts missing")
    for path in STATE_SURFACES:
        state_content = read(path)
        require("numerical_cumulative_contract_audit.py" in state_content, f"state surface misses audit: {path.name}")
        require("regression-passed" in state_content, f"state surface misses material pass: {path.name}")
        require("not-attempted" in state_content, f"state surface misses personal boundary: {path.name}")
    print("PASS cumulative artifacts: oral/closed/nonce/blind/delay route + 6 synchronized state surfaces")


def audit_markdown_integrity() -> None:
    scoped = [NUM / filename for filename in CONCEPTS] + [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
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
                    candidates = [candidate for candidate in candidates if candidate.suffix.lower() == suffix]
            if not candidates:
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")

    require(not math_findings, f"unbalanced display-math delimiters: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    figure_count = 0
    figure_findings: list[str] = []
    for path in [NUM / filename for filename in CONCEPTS] + [MOC, EXPERIMENT]:
        lines = read(path).splitlines()
        positions = [index for index, line in enumerate(lines) if image_pattern.search(line)]
        for order, position in enumerate(positions):
            figure_count += 1
            stop = positions[order + 1] if order + 1 < len(positions) else min(len(lines), position + 45)
            block = "\n".join(lines[position : min(stop, position + 45)])
            missing = [marker for marker in ("[!figure]", "怎样读图", "适用边界") if marker not in block]
            if missing:
                figure_findings.append(f"{path.relative_to(ROOT)}:{position + 1} missing {missing}")
            match = image_pattern.search(lines[position])
            require(match is not None, "internal image parser failure")
            target = match.group(1)
            image_path = ROOT / target
            require(image_path.is_file(), f"missing embedded image: {target}")
            if image_path.suffix.lower() == ".svg":
                root_element = ET.parse(image_path).getroot()
                require(root_element.tag.endswith("svg"), f"invalid SVG root: {target}")
                require("viewBox" in root_element.attrib, f"SVG missing viewBox: {target}")
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
    require("NUM-01—20 material regression: PASS" in teaching_output,
            "chapter teaching audit did not reach its material PASS")

    require(CUM_SVG.is_file(), "stored cumulative SVG is missing")
    stored_digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(stored_digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {stored_digest}")
    with tempfile.TemporaryDirectory(prefix="nla-cum-audit-") as temp_dir:
        temp = Path(temp_dir)
        canonical_a = temp / "canonical-a.svg"
        canonical_b = temp / "canonical-b.svg"
        output_a = run(CUM_SCRIPT, "--output", str(canonical_a))
        output_b = run(CUM_SCRIPT, "--output", str(canonical_b))
        require(normalized_output(output_a) == normalized_output(output_b), "canonical stdout is not deterministic")
        require(canonical_a.read_bytes() == canonical_b.read_bytes(), "canonical SVG double-run differs")
        canonical_digest = hashlib.sha256(canonical_a.read_bytes()).hexdigest()
        require(canonical_digest == EXPECTED_CUM_SHA256, f"canonical SVG hash changed: {canonical_digest}")
        for marker in (
            "A_CONFIG tau=0.0001 task_budget=0.01",
            "A_RELIABILITY fl(1+tau)=1.000 forward=0.707107 rho=0.00010000 kappa=10000.0 kappa*rho=1.00000000 task_gate=1.00e-06",
            "B_CONFIG richardson_step=0.5",
            "B_SOLVER CG_rel_r1=0.06896552 GMRES=1.41421356->0.63245553->0.0 Richardson_rho=0.5000 kappa=52.45584->17.94427",
            "C_CONFIG index_bytes=4 value_bytes=8 power_iterations=1",
            "C_SCALE index=4B CSR(A)=64B dense=72B CSR(AtA)=76B range=0.62554324 best_rank2=0.41421356 power_tail=0.00505063",
        ):
            require(marker in output_a, f"canonical output misses: {marker}")
        ET.parse(canonical_a)

        intervention = temp / "intervention.svg"
        intervention_output = run(
            CUM_SCRIPT,
            "--tau", "0.002",
            "--task-budget", "0.005",
            "--richardson-step", "0.7",
            "--index-bytes", "8",
            "--value-bytes", "4",
            "--power-iterations", "2",
            "--output", str(intervention),
        )
        intervention_digest = hashlib.sha256(intervention.read_bytes()).hexdigest()
        require(intervention_digest == EXPECTED_INTERVENTION_SHA256, f"intervention SVG hash changed: {intervention_digest}")
        for marker in (
            "A_CONFIG tau=0.002 task_budget=0.005",
            "A_RELIABILITY fl(1+tau)=1.002 forward=0.707107 rho=0.00200000 kappa=500.0 kappa*rho=0.99999800 task_gate=1.00e-05",
            "B_CONFIG richardson_step=0.7",
            "B_SOLVER CG_rel_r1=0.06896552 GMRES=1.41421356->0.63245553->0.0 Richardson_rho=1.1000 kappa=52.45584->17.94427",
            "C_CONFIG index_bytes=8 value_bytes=4 power_iterations=2",
            "C_SCALE index=8B CSR(A)=80B dense=36B CSR(AtA)=92B range=0.62554324 best_rank2=0.41421356 power_tail=0.00014868",
        ):
            require(marker in intervention_output, f"intervention output misses: {marker}")
        intervention_svg = intervention.read_text(encoding="utf-8")
        for marker in (
            "F10,4: fl(1+0.002)=1.002",
            "rho ~= 2.00e-03",
            "kappa=500",
            "0.5% task gate requires rho &lt;= 1e-05",
            "rho=1.10, transient=1.43",
            "q=2: tail ratio=0.0001487",
            "protocol: index=8B, value=4B; 另记 p/q/seed。",
        ):
            require(marker in intervention_svg, f"intervention SVG does not self-describe: {marker}")
        ET.parse(intervention)

    print("PASS chapter compute dependency: NUM-01—20 teaching/figure regression")
    print(f"PASS canonical double-run + stored SVG: sha256={stored_digest}")
    print(f"PASS blind-interface intervention: sha256={EXPECTED_INTERVENTION_SHA256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="rerun all 20 chapter figures and the deterministic NLA-CUM-01 three-track gate",
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
        digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest() if CUM_SVG.is_file() else "missing"
        require(digest == EXPECTED_CUM_SHA256, f"stored cumulative SVG hash changed: {digest}")
        print("SKIP compute rerun (pass --run-compute for the formal NLA-CUM audit)")
    print("NLA-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
