#!/usr/bin/env python3
"""Independent material and reproducibility audit for RAD-CUM-01."""

from __future__ import annotations

import hashlib
import itertools
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LABS = ROOT / "00-知识库管理" / "_labs"
CHAPTER = ROOT / "20-学习理论" / "20.4-数据依赖复杂度、间隔与快率"
MOC = CHAPTER / "数据依赖复杂度、间隔与快率 MOC.md"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 数据依赖复杂度、间隔与快率（20.4）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 数据依赖复杂度、间隔与快率（20.4）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 数据依赖复杂度、间隔与快率累计复现门.md"
GATE_SCRIPT = LABS / "code" / "rademacher_margin_local_cumulative_gate.py"
CANONICAL_SVG = (
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-rademacher-margin-local-cumulative-gate-v2.svg"
)

CANONICAL_SHA256 = "0927973a4f96cc973ad5729358c41c681296485dee651ffbbd9ab86cebf72ed0"
BLIND_SHA256 = "3e7d928f4d83629cae72e9c6a3c58403a78a50c9beca4f93e48f095843358781"

BLIND_ARGS = (
    "--linear-norm", "1.2",
    "--ramp-gamma", "1.0",
    "--margin-levels=-0.3,0.1,0.3,0.6,1.1",
    "--margin-counts", "30,70,150,350,600",
    "--gamma-grid", "0.25,0.5,0.75,1.0",
    "--margin-norm", "1.25",
    "--data-radius", "0.9",
    "--delta", "0.08",
    "--cover-dim", "3",
    "--local-dim", "6",
    "--local-size", "600",
    "--local-a", "1.1",
    "--local-b", "0.7",
    "--fat-ambient", "6",
    "--fat-norm", "1.2",
    "--fat-radius", "0.8",
    "--fat-gammas", "0.3,0.4,0.6,0.9",
)

EXPECTED_BLIND_LINES = (
    "TRACK A l2_exact=0.686474 energy_bound=0.734847 finite_score=0.600000 finite_margin=0.600000 ramp=0.296875 contraction_bound=1.200000",
    "TRACK B m=1200 selected_gamma=0.5 selected_raw=0.599554 confidence=0.131413 rad_bound=0.032476 bounds=0.25:0.734362,0.5:0.599554,0.75:0.804618,1:0.761317",
    "TRACK C cover=0:8,1:2,2:2,3:1 fixed=0.024064 slow=0.117000 improvement=4.862087 fat=0.3:6,0.4:5,0.6:2,0.9:1",
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
        require(result.returncode != 0, "gate unexpectedly accepted an invalid contract")
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


def independent_finite_rademacher(vectors: tuple[tuple[float, ...], ...]) -> float:
    sample_size = len(vectors[0])
    values = []
    for signs in itertools.product((-1.0, 1.0), repeat=sample_size):
        values.append(max(sum(sign * value for sign, value in zip(signs, vector)) for vector in vectors) / sample_size)
    return sum(values) / len(values)


def independent_sign_anchors(linear_norm: float, ramp_gamma: float) -> tuple[float, float, float, float, float]:
    sample = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, -1.0))
    labels = (1.0, 1.0, -1.0, 1.0)
    norms = []
    for signs in itertools.product((-1.0, 1.0), repeat=4):
        first = sum(sign * point[0] for sign, point in zip(signs, sample))
        second = sum(sign * point[1] for sign, point in zip(signs, sample))
        norms.append(math.sqrt(first * first + second * second))
    exact = linear_norm * sum(norms) / len(norms) / 4
    energy = linear_norm * math.sqrt(sum(x * x + y * y for x, y in sample)) / 4
    weights = ((0.0, 0.0), (linear_norm, 0.0), (-linear_norm, 0.0), (0.0, linear_norm), (0.0, -linear_norm))
    scores = tuple(tuple(w[0] * x[0] + w[1] * x[1] for x in sample) for w in weights)
    margins = tuple(tuple(label * value for label, value in zip(labels, vector)) for vector in scores)

    def centered(value: float) -> float:
        if value <= 0:
            loss = 1.0
        elif value >= ramp_gamma:
            loss = 0.0
        else:
            loss = 1.0 - value / ramp_gamma
        return loss - 1.0

    ramps = tuple(tuple(centered(value) for value in vector) for vector in margins)
    return (
        exact,
        energy,
        independent_finite_rademacher(scores),
        independent_finite_rademacher(margins),
        independent_finite_rademacher(ramps),
    )


def independent_margin_anchors(
    levels: tuple[float, ...], counts: tuple[int, ...], gammas: tuple[float, ...],
    norm_bound: float, data_radius: float, delta: float,
) -> tuple[float, float, tuple[float, ...], int]:
    sample_size = sum(counts)
    radius = norm_bound * data_radius / math.sqrt(sample_size)
    confidence = 3 * math.sqrt(math.log(2 * len(gammas) / delta) / (2 * sample_size))
    raw = []
    for gamma in gammas:
        empirical = sum(count for level, count in zip(levels, counts) if level <= gamma) / sample_size
        raw.append(empirical + 4 * radius / gamma + confidence)
    selected = min(range(len(gammas)), key=lambda index: (raw[index], index))
    return radius, confidence, tuple(raw), selected


def hamming(left: int, right: int) -> int:
    return bin(left ^ right).count("1")


def independent_cover(cube_dim: int, radius: int) -> int:
    points = tuple(range(2**cube_dim))
    for size in range(1, len(points) + 1):
        for centers in itertools.combinations(points, size):
            if all(any(hamming(point, center) <= radius for center in centers) for point in points):
                return size
    raise AssertionError("finite cube must be coverable")


def audit_node_bundle() -> None:
    files = sorted(path for path in CHAPTER.glob("*.md") if path != MOC)
    require(len(files) == 8, f"expected 8 LT-25--32 nodes, found {len(files)}")
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
    require(sorted(found) == list(range(25, 33)), f"scope changed: {sorted(found)}")
    moc = read(MOC)
    for node_id in range(25, 33):
        require(re.search(rf"^\| LT-{node_id:02d} \|", moc, re.M) is not None, f"MOC misses LT-{node_id:02d}")
    print("PASS LT-25--32 node bundle: 8/8 unique draft nodes, visuals and MOC mappings")


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    for content, label in ((assessment, "assessment"), (solution, "solution"), (experiment, "experiment")):
        frontmatter = parse_frontmatter(content)
        require(frontmatter.get("status") == "draft", f"{label}: status must remain draft")
        require(frontmatter.get("material_status") == "regression-passed", f"{label}: material status changed")
        require(frontmatter.get("learning_status") == "not-attempted", f"{label}: personal status changed")
        require(frontmatter.get("assessment_id") == "RAD-CUM-01", f"{label}: assessment ID changed")
        require(frontmatter.get("updated") == "2026-08-28", f"{label}: date changed")
    require("time_limit_minutes: 210" in assessment, "assessment duration changed")
    for node_id in range(25, 33):
        require(f"LT-{node_id:02d}" in assessment, f"assessment scope misses LT-{node_id:02d}")
    for question in range(1, 15):
        require(re.search(rf"^### 第\s*{question}\s*题：.*（(\d+)\s*分）$", assessment, re.M) is not None,
                f"question sheet misses question {question}")
        require(re.search(rf"^### 第\s*{question}\s*题解答：.*（(\d+)\s*分）$", solution, re.M) is not None,
                f"solution misses answer {question}")
    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题：.*（(\d+)\s*分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第\s*(\d+)\s*题解答：.*（(\d+)\s*分）$", solution, re.M)
    }
    require(question_points == solution_points, "question/solution points differ")
    require(sum(question_points.values()) == 100, "assessment does not total 100 points")
    for marker in (
        "20 分钟卷级口试", "210 分钟闭卷", "三轨参数化模型族", "八层数据依赖复杂度证明账本",
        "答案与输出隔离协议", "scorer nonce", "48 小时与 14 天复测", "提交证据清单",
    ):
        require(marker in assessment, f"assessment misses marker: {marker}")
    for marker in ("口试评分参考", "实验复现与延迟门参考", "状态边界"):
        require(marker in solution, f"solution misses marker: {marker}")
    require("第 1 题解答" not in assessment, "answer leaked into question sheet")
    require("才可打开本页或 canonical stdout" in solution, "solution isolation warning missing")
    print("PASS assessment bundle: scope=8/8, questions/solutions=14/14, points=100, isolation + delay gates")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "三轨统一对象合同",
        "轨道 A：精确 signs、双范数与收缩",
        "轨道 B：预注册 margin 选择",
        "轨道 C：cover、local 与 fat 的责任边界",
        "评分者随机指定、跨轨盲参与防挑题协议",
        "独立审计固定 fixture",
        "盲参数干预怎样才算独立",
        "证据状态机",
        CANONICAL_SHA256,
        BLIND_SHA256,
    ):
        require(marker in experiment, f"experiment contract misses: {marker}")
    headings = [line.strip() for line in experiment.splitlines() if line.startswith("#")]
    duplicate = sorted({heading for heading in headings if headings.count(heading) > 1})
    require(not duplicate, f"experiment duplicate headings: {duplicate}")
    print("PASS experiment contract: analytic calibration, three tracks, selection/localization boundaries")


def audit_analytic_anchors() -> None:
    exact, energy, score, margin, ramp = independent_sign_anchors(1.0, 0.75)
    require(abs(exact - 0.5720614028176844) < 1e-14, "Track A exact dual-norm value changed")
    require(abs(energy - 0.6123724356957945) < 1e-14, "Track A energy bound changed")
    require(abs(score - 0.5) < 1e-15 and abs(margin - 0.5) < 1e-15, "label invariance changed")
    require(abs(ramp - 0.296875) < 1e-15, "centered ramp complexity changed")

    radius, confidence, raw, selected = independent_margin_anchors(
        (-0.2, 0.15, 0.35, 0.7, 1.2), (40, 80, 160, 440, 880), (0.2, 0.4, 0.8, 1.0),
        1.25, 1.0, 0.05,
    )
    require(abs(radius - 0.03125) < 1e-15, "Track B linear radius changed")
    require(abs(confidence - 0.11947353830595767) < 1e-14, "Track B confidence changed")
    expected_raw = (0.8194735383059577, 0.6069735383059577, 0.7257235383059577, 0.6944735383059576)
    require(all(abs(left - right) < 1e-14 for left, right in zip(raw, expected_raw)), "Track B raw bounds changed")
    require(selected == 1, "Track B selected gamma changed")

    covers = tuple(independent_cover(4, radius_value) for radius_value in (0, 1, 2, 4))
    require(covers == (16, 4, 2, 1), "Track C exact covers changed")
    coefficient = 1.2 * math.sqrt(8 / 800)
    offset = 0.5 * 8 / 800
    root_t = (coefficient + math.sqrt(coefficient**2 + 4 * offset)) / 2
    fixed = root_t**2
    require(abs(fixed - 0.02332834219459485) < 1e-14, "Track C fixed point changed")
    require(tuple(min(8, int(math.floor((1 / gamma) ** 2 + 1e-12))) for gamma in (0.25, 0.35, 0.5, 0.75)) == (8, 8, 4, 1),
            "Track C fat profile changed")
    print("PASS analytic anchors: exact signs, margin budget, internal covers, fixed point and fat profile")


def audit_svg(path: Path, expected_hash: str, required_text: tuple[str, ...]) -> None:
    require(path.is_file(), f"missing SVG: {path}")
    require(sha256(path) == expected_hash, f"SVG hash changed: {path.name}")
    root = ET.parse(path).getroot()
    require(root.tag.endswith("svg"), f"not an SVG root: {path.name}")
    require(root.attrib.get("viewBox") == "0 0 1440 700", f"SVG viewBox changed: {path.name}")
    text_content = " ".join("".join(element.itertext()) for element in root.iter() if element.tag.endswith("text"))
    for marker in required_text:
        require(marker in text_content, f"SVG is not self-describing; misses {marker!r}")
    require(sum(1 for element in root.iter() if element.tag.endswith("text")) >= 50,
            f"SVG text density too low: {path.name}")


def audit_reproducibility() -> None:
    stored_before = CANONICAL_SVG.read_bytes()
    first = run()
    first_bytes = CANONICAL_SVG.read_bytes()
    second = run()
    second_bytes = CANONICAL_SVG.read_bytes()
    require(stored_before == first_bytes == second_bytes, "canonical output is not byte deterministic")
    require("l2_exact=0.572061" in first.stdout, "canonical Track A anchor missing")
    require("selected_gamma=0.4" in first.stdout, "canonical Track B anchor missing")
    require("cover=0:16,1:4,2:2,4:1" in first.stdout, "canonical Track C anchor missing")
    audit_svg(
        CANONICAL_SVG,
        CANONICAL_SHA256,
        ("精确 signs × 收缩", "预注册 margin 选择", "尺度梯 × 局部 fixed point"),
    )

    with tempfile.TemporaryDirectory() as temporary:
        first_path = Path(temporary) / "blind-first.svg"
        second_path = Path(temporary) / "blind-second.svg"
        first_blind = run(*BLIND_ARGS, "--output", str(first_path))
        second_blind = run(*BLIND_ARGS, "--output", str(second_path))
        require(first_path.read_bytes() == second_path.read_bytes(), "blind output is not byte deterministic")
        for line_value in EXPECTED_BLIND_LINES:
            require(line_value in first_blind.stdout and line_value in second_blind.stdout,
                    f"blind stdout changed: {line_value}")
        audit_svg(first_path, BLIND_SHA256, ("m=1200", "Hamming cube q=3", "γ=0.3 → 6"))

    unsafe = run(*BLIND_ARGS, expect_success=False)
    require("require --output" in (unsafe.stdout + unsafe.stderr), "unsafe refusal changed")
    explicit = run(*BLIND_ARGS, "--output", str(CANONICAL_SVG), expect_success=False)
    require("may not target" in (explicit.stdout + explicit.stderr), "explicit canonical overwrite was accepted")
    require(CANONICAL_SVG.read_bytes() == stored_before, "overwrite tests changed canonical asset")

    with tempfile.TemporaryDirectory() as temporary:
        invalid_path = Path(temporary) / "invalid.svg"
        invalid = run("--cover-dim", "5", "--output", str(invalid_path), expect_success=False)
        require("must lie in 1..4" in (invalid.stdout + invalid.stderr), "invalid cover dimension was accepted")
        require(not invalid_path.exists(), "invalid input created output")
        mismatch = run("--margin-counts", "1,2", "--output", str(invalid_path), expect_success=False)
        require("equal lengths" in (mismatch.stdout + mismatch.stderr), "mismatched margin contract was accepted")
        require(not invalid_path.exists(), "mismatched input created output")
    print("PASS deterministic compute: canonical + blind double-run, XML/hash and overwrite/input protection")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require("RAD-CUM-01" in content, f"state surface misses volume ID: {path.relative_to(ROOT)}")
        require(audit_name in content, f"state surface misses audit link: {path.relative_to(ROOT)}")
        require("regression-passed" in content, f"state surface misses material state: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface misses learner state: {path.relative_to(ROOT)}")
    root_moc = read(ROOT / "20-学习理论" / "学习理论 MOC.md")
    curriculum = read(ROOT / "20-学习理论" / "学习理论完整课程地图与掌握标准.md")
    for content, label in ((root_moc, "root MOC"), (curriculum, "curriculum map")):
        require(re.search(r"7\s*/\s*10", content) is not None, f"{label}: volume-gate count not synchronized")
        require(re.search(r"0\s*/\s*10", content) is not None, f"{label}: personal count changed")
    print(f"PASS state surfaces: {len(STATE_SURFACES)} views agree on 7/10 material gates and 0/10 personal passes")


def main() -> None:
    audit_node_bundle()
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_analytic_anchors()
    audit_reproducibility()
    audit_state_surfaces()
    print("RAD-CUM-01 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
