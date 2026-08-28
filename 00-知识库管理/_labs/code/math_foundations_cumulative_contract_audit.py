#!/usr/bin/env python3
"""Independent material and reproducibility audit for MATH-CUM-01."""

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
CHAPTER = ROOT / "10-数学基础" / "10.1-数学语言、逻辑与证明"
MOC = CHAPTER / "数学语言、逻辑与证明 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 数学语言、逻辑与证明（10.1）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 数学语言、逻辑与证明（10.1）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 数学语言、逻辑与证明累计复现门.md"
CUM_SCRIPT = LABS / "code" / "math_foundations_cumulative_gate.py"
CUM_SVG = (
    ROOT / "00-知识库管理" / "_assets" / "plots" / "math-foundations"
    / "plot-math-foundations-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "c635f3c63df194b79e53cd7ccf99f7c523b52158a66dd64df8d0896456960f25"
EXPECTED_BLIND_SHA256 = "132a8211dfdbcce391c94f4a2e0ba5b8b8abc318c1eefc5cd030d38ac2d7da03"

NODE_AUDITS = (
    "set_operations_split_audit.py",
    "quantifier_scope_order_audit.py",
    "proof_obligation_counterexample_audit.py",
    "function_relation_quotient_audit.py",
    "induction_recursion_counting_audit.py",
    "inequality_bound_audit.py",
    "sequence_limit_completeness_audit.py",
    "asymptotics_complexity_audit.py",
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


def audit_node_bundle() -> None:
    markdown = [path for path in CHAPTER.glob("*.md") if path != MOC]
    require(len(markdown) == 8, f"expected eight chapter bodies, found {len(markdown)}")
    moc = read(MOC)
    for index in range(1, 9):
        node_id = f"MATH-{index:02d}"
        require(re.search(rf"^\| {node_id} \|", moc, re.M) is not None,
                f"{node_id}: missing from MOC curriculum tables")
    for name in NODE_AUDITS:
        run(LABS / "code" / name)
    print("PASS node bundle: MATH-01—08 unique and all eight deterministic node audits execute")


def audit_assessment_bundle() -> None:
    assessment, solution, experiment = read(ASSESSMENT), read(SOLUTION), read(EXPERIMENT)
    for content, label in (
        (assessment, "assessment"),
        (solution, "solution"),
        (experiment, "experiment"),
    ):
        require("status: draft" in content, f"{label}: learning document must remain draft")
        require("material_status: regression-passed" in content, f"{label}: material state changed")
        require("learning_status: not-attempted" in content, f"{label}: personal state changed")
        require("updated: 2026-08-28" in content, f"{label}: migration date missing")

    require("assessment_id: MATH-CUM-01" in assessment, "assessment ID changed")
    require("assessment_id: MATH-CUM-01" in solution, "solution ID changed")
    require("time_limit_minutes: 180" in assessment, "assessment time limit changed")
    for index in range(1, 9):
        require(f"MATH-{index:02d}" in assessment, f"assessment scope misses MATH-{index:02d}")
    for index in range(1, 15):
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
    require(sorted(question_points) == list(range(1, 15)), "assessment point headers incomplete")
    require(question_points == solution_points, "question/solution point allocations differ")
    require(sum(question_points.values()) == 100, "assessment no longer totals 100 points")

    for marker in (
        "先看完整验收时间线",
        "15 分钟卷级口试",
        "三波参数化模型族",
        "九层数学语言—证明对象账本",
        "答案与输出隔离协议",
        "scorer nonce",
        "48 小时换机制重建门",
        "14 天陌生 AI theorem-audit 迁移门",
        "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses cumulative marker: {marker}")
    for marker in (
        "卷级口试参考要点",
        "九层数学语言—证明对象账本参考",
        "三波参数化模型族的卷级数值锚点",
        "口试判分红线",
        "实验复现门的评分说明",
        "nonce 与盲参数判分红线",
        "从 `retained` 到逐节点证据",
        "最终状态边界",
    ):
        require(marker in solution, f"solution misses rubric marker: {marker}")
    require("第 1 题解答" not in assessment, "answer content leaked into question sheet")
    require("才可打开本解答或 canonical 结果" in solution, "solution use-order warning incomplete")
    print("PASS assessment bundle: scope 8/8, questions/answers 14/14, points=100, isolation + nonce + delay gates")


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
        "审计使用的固定多参数盲测 fixture",
        "--adaptive-rank-exponent",
        "证据状态机",
        "48 小时换例与 14 天迁移",
        EXPECTED_CUM_SHA256,
        EXPECTED_BLIND_SHA256,
    ):
        require(marker in experiment, f"experiment misses contract marker: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicates, f"experiment has duplicate headings: {duplicates}")
    print("PASS experiment contract: analytic calibration, A/B/C families, blind fixture and evidence states")


def relation_counts(m: int) -> tuple[int, int, int, int]:
    total = 2 ** (m * m)
    pointwise = (2**m - 1) ** m
    uniform = sum(
        (-1) ** (j + 1) * math.comb(m, j) * 2 ** (m * (m - j))
        for j in range(1, m + 1)
    )
    return total, pointwise, uniform, pointwise - uniform


def certificate(epsilon: float, q: float, coefficient: float) -> int:
    return max(0, math.floor(math.log(coefficient / epsilon) / math.log(1 / q)) + 1)


def slope(xs: list[float], ys: list[float]) -> float:
    lx, ly = [math.log(x) for x in xs], [math.log(y) for y in ys]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum((x - mx) ** 2 for x in lx)


def audit_exact_models() -> None:
    require(relation_counts(4) == (65536, 50625, 14911, 35714), "canonical relation counts changed")
    require(relation_counts(3) == (512, 343, 169, 174), "blind relation counts changed")

    for q, r, forcing, expected_c, expected_certificates in (
        (0.8, 0.6, 0.5, 3.5, [27, 47, 68, 89]),
        (0.75, 0.5, 0.4, 2.6, [20, 36, 52, 68]),
    ):
        coefficient = 1 + forcing / (q - r)
        require(math.isclose(coefficient, expected_c), "recurrence envelope coefficient changed")
        actual = [certificate(eps, q, coefficient) for eps in (1e-2, 1e-4, 1e-6, 1e-8)]
        require(actual == expected_certificates, "recurrence certificates changed")
        values = [1.0]
        for k in range(100):
            values.append(q * values[-1] + forcing * r**k)
        closed = [coefficient * q**k - (coefficient - 1) * r**k for k in range(101)]
        require(max(abs(a - b) for a, b in zip(values, closed)) < 3e-15,
                "recurrence closed form changed")

    lengths = [float(32 * 2**i) for i in range(9)]
    for dimension, exponent, expected_dense in ((512, 1.0, 1.378561), (384, 0.5, 1.428261)):
        dense = [4 * t * dimension**2 + 2 * t**2 * dimension for t in lengths]
        adaptive = [4 * t * dimension * t**exponent / (4 if exponent == 1 else 2) for t in lengths]
        require(math.isclose(slope(lengths, dense), expected_dense, abs_tol=6e-7),
                "dense finite-window slope changed")
        require(math.isclose(slope(lengths, adaptive), 1 + exponent, abs_tol=2e-15),
                "adaptive-rank slope changed")
    print("PASS exact models: canonical and fixed blind relation/recurrence/complexity anchors")


def audit_state_surfaces() -> None:
    expected_row = (
        "| CUM | MATH-CUM-01 | 口试 → 闭卷 → nonce 随机轨 → 跨轨盲干预 → 订正 → 48 h / 14 d → 独立审计 | "
        "量词关系、受迫递推与 rank 增长制度三轨门 | `regression-passed` | `not-attempted` |"
    )
    require(expected_row in read(MOC), "chapter MOC cumulative status row missing")
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        nearby = "\n".join(
            line for line in content.splitlines()
            if "MATH-CUM" in line or "10.1" in line or audit_name in line
        )
        require("MATH-CUM" in nearby, f"state surface misses MATH-CUM: {path.relative_to(ROOT)}")
        require("regression-passed" in nearby, f"state surface misses material PASS: {path.relative_to(ROOT)}")
        require("not-attempted" in nearby, f"state surface misses personal state: {path.relative_to(ROOT)}")
        require(audit_name in content, f"state surface misses independent audit: {path.relative_to(ROOT)}")
    print(f"PASS state surfaces: chapter MOC plus {len(STATE_SURFACES)} curriculum/ledger views agree")


def audit_markdown() -> None:
    scoped = [MOC, ASSESSMENT, SOLUTION, EXPERIMENT]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.stem if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        index.setdefault(key, []).append(path)
    missing: list[str] = []
    links = 0
    for path in scoped:
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in active_lines(read(path)))
        require(active.count("$$") % 2 == 0, f"{path.name}: unbalanced display math")
        for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", active):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            links += 1
            if "/" in target:
                direct = ROOT / target
                found = direct.is_file() or (not direct.suffix and Path(str(direct) + ".md").is_file())
            else:
                suffix = Path(target).suffix.lower()
                key = target[: -len(suffix)] if suffix in KNOWN_EXTENSIONS else target
                found = bool(index.get(key))
            if not found:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing, f"missing Wiki links: {missing}")
    lines = read(EXPERIMENT).splitlines()
    positions = [i for i, line in enumerate(lines) if "![[" in line and ".svg" in line]
    require(len(positions) == 1, f"expected one cumulative formal figure, found {len(positions)}")
    block = "\n".join(lines[positions[0]:positions[0] + 45])
    for marker in ("[!figure]", "怎样读图", "适用边界"):
        require(marker in block, f"figure unit misses {marker}")
    print(f"PASS cumulative Markdown: Wiki links={links}, display math balanced, figure unit complete")


def normalized_output(output: str) -> str:
    return "\n".join(line for line in output.splitlines() if not line.startswith("OUTPUT "))


def audit_compute() -> None:
    require(hashlib.sha256(CUM_SVG.read_bytes()).hexdigest() == EXPECTED_CUM_SHA256,
            "stored canonical SVG hash changed")
    root = ET.parse(CUM_SVG).getroot()
    require(root.tag.endswith("svg") and "viewBox" in root.attrib, "stored SVG XML/viewBox invalid")
    with tempfile.TemporaryDirectory(prefix="math-cum-audit-") as directory:
        temporary = Path(directory)
        canonical_a, canonical_b = temporary / "canonical-a.svg", temporary / "canonical-b.svg"
        first = run(CUM_SCRIPT, "--output", str(canonical_a))
        second = run(CUM_SCRIPT, "--output", str(canonical_b))
        for marker in (
            "A_COUNTS total=65536 pointwise=50625 uniform=14911 swap_gap=35714",
            "B_CONFIG contraction=0.8 forcing_rate=0.6 forcing=0.5 envelope_coefficient=3.5",
            "certificates=1e-02:27/27,1e-04:47/47,1e-06:68/68,1e-08:89/89",
            "C_COMPLEXITY dense_slope=1.378561 fixed_rank_slope=1.000000 adaptive_rank_slope=2.000000 score_slope=2.000000",
            f"SHA256 {EXPECTED_CUM_SHA256}",
        ):
            require(marker in first, f"canonical stdout misses {marker}")
        require(normalized_output(first) == normalized_output(second), "canonical stdout is not deterministic")
        require(canonical_a.read_bytes() == canonical_b.read_bytes() == CUM_SVG.read_bytes(),
                "canonical SVG bytes differ across runs or stored artifact")

        unsafe = subprocess.run(
            [sys.executable, str(CUM_SCRIPT), "--domain-size", "3"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(unsafe.returncode != 0, "noncanonical run could overwrite canonical artifact")
        require("noncanonical runs require --output" in unsafe.stderr, "protection message changed")

        blind = temporary / "blind.svg"
        blind_output = run(
            CUM_SCRIPT,
            "--domain-size", "3",
            "--contraction", "0.75",
            "--forcing-rate", "0.5",
            "--forcing", "0.4",
            "--dimension", "384",
            "--feature-rank", "96",
            "--adaptive-rank-exponent", "0.5",
            "--adaptive-rank-divisor", "2",
            "--output", str(blind),
        )
        for marker in (
            "A_COUNTS total=512 pointwise=343 uniform=169 swap_gap=174",
            "B_CONFIG contraction=0.75 forcing_rate=0.5 forcing=0.4 envelope_coefficient=2.6",
            "certificates=1e-02:20/20,1e-04:36/36,1e-06:52/52,1e-08:68/68",
            "C_COMPLEXITY dense_slope=1.428261 fixed_rank_slope=1.000000 adaptive_rank_slope=1.500000 score_slope=2.000000",
            f"SHA256 {EXPECTED_BLIND_SHA256}",
        ):
            require(marker in blind_output, f"blind stdout misses {marker}")
        require(hashlib.sha256(blind.read_bytes()).hexdigest() == EXPECTED_BLIND_SHA256,
                "blind SVG hash changed")
        blind_svg = blind.read_text(encoding="utf-8")
        for marker in (
            "|X|=|Y|=3；枚举 512 个 Boolean relations",
            "eₖ₊₁=0.75eₖ+0.4·0.5ᵏ；envelope C=2.6",
            "d=384, fixed r=96；adaptive r=T^0.5/2",
            "adaptive-r: p=1.500",
        ):
            require(marker in blind_svg, f"blind SVG is not self-describing: {marker}")
        ET.parse(blind)
    print("PASS compute: canonical double-run + overwrite protection + blind stdout/SVG/hash contract")


def main() -> None:
    audit_node_bundle()
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_exact_models()
    audit_state_surfaces()
    audit_markdown()
    audit_compute()
    print("MATH-01—08 material regression: PASS")
    print("MATH-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
