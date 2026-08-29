#!/usr/bin/env python3
"""Audit the static and reproducible contract for NN-CUM-01."""

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
CHAPTER = ROOT / "30-神经网络基础"
LABS = ROOT / "00-知识库管理" / "_labs"
ASSESSMENT = LABS / "assessments" / "阶段测验 - 神经网络基础（第三章）.md"
SOLUTION = LABS / "assessments" / "阶段测验解答 - 神经网络基础（第三章）.md"
EXPERIMENT = LABS / "experiments" / "实验 - 神经网络基础累计复现门.md"
MOC = CHAPTER / "神经网络基础 MOC.md"
TEACHING_AUDIT = LABS / "code" / "neural_network_foundations_teaching_contract_audit.py"
CUM_SCRIPT = LABS / "code" / "plot_neural_network_cumulative_gate.py"
CUM_SVG = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "neural-networks"
    / "plot-neural-network-cumulative-gate-v2.svg"
)
EXPECTED_CUM_SHA256 = "aac6c5167ac56ff94b1f7b374d4fdc22deda5cb336b5fb6bdc94059dfdc8bb0e"
EXPECTED_BLIND_SHA256 = "a36bc4dfb6dda830b0b4e5bd82f0962c2224f1e0e6b9f18dbc3ae6b5260d8c4f"

STATE_SURFACES = (
    MOC,
    CHAPTER / "神经网络基础完整课程地图与掌握标准.md",
    LABS / "exercises" / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    CHAPTER / "30.1-前馈网络、感知机与表达能力" / "前馈网络、感知机与表达能力 MOC.md",
    CHAPTER / "30.2-计算图、反向传播与自动微分" / "计算图、反向传播与自动微分 MOC.md",
    CHAPTER / "30.3-激活函数、门控与非线性" / "激活函数、门控与非线性 MOC.md",
    CHAPTER / "30.4-初始化与信号传播" / "初始化与信号传播 MOC.md",
    CHAPTER / "30.5-归一化、尺度与统计量" / "归一化、尺度与统计量 MOC.md",
    CHAPTER / "30.6-残差连接、深度与稳定性" / "残差连接、深度与稳定性 MOC.md",
    CHAPTER / "30.7-Embedding、权重共享与输出参数化" / "Embedding、权重共享与输出参数化 MOC.md",
    CHAPTER / "30.8-随机正则化与网络级泛化接口" / "随机正则化与网络级泛化接口 MOC.md",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_text(content: str) -> str:
    output: list[str] = []
    in_fence = False
    fence = ""
    fence_token = chr(96) * 3
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(fence_token) or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence = True, marker
            elif marker == fence:
                in_fence, fence = False, ""
            continue
        if not in_fence:
            output.append(re.sub(r"\x60[^\x60]*\x60", "", line))
    return "\n".join(output)


def frontmatter_line(content: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.M)
    return match.group(1).strip() if match else ""


def audit_assessment_bundle() -> None:
    assessment = read(ASSESSMENT)
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    for content, label in (
        (assessment, "assessment"),
        (solution, "solution"),
        (experiment, "experiment"),
    ):
        require(frontmatter_line(content, "status") == "draft", f"{label}: learning document must remain draft")
        require(frontmatter_line(content, "material_status") == "regression-passed", f"{label}: material state is not regression-passed")
        require(frontmatter_line(content, "learning_status") == "not-attempted", f"{label}: personal state is not not-attempted")
        require(frontmatter_line(content, "updated") == "2026-08-29", f"{label}: cumulative migration date missing")

    require(frontmatter_line(assessment, "assessment_id") == "NN-CUM-01", "assessment ID changed")
    require(frontmatter_line(solution, "assessment_id") == "NN-CUM-01", "solution ID changed")
    require(frontmatter_line(assessment, "time_limit_minutes") == "240", "assessment time limit changed")
    scope = re.findall(r"NN-\d{2}", frontmatter_line(assessment, "scope"))
    solution_scope = re.findall(r"NN-\d{2}", frontmatter_line(solution, "scope"))
    expected_scope = [f"NN-{index:02d}" for index in range(1, 65)]
    require(scope == solution_scope == expected_scope, "assessment/solution scope is not exactly NN-01--64")

    question_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第 (\d+) 题：.*（(\d+) 分）$", assessment, re.M)
    }
    solution_points = {
        int(index): int(points)
        for index, points in re.findall(r"^### 第 (\d+) 题解答：.*（(\d+) 分）$", solution, re.M)
    }
    require(sorted(question_points) == list(range(1, 15)), "assessment question headers are incomplete")
    require(question_points == solution_points, "question/solution point allocations differ")
    require(sum(question_points.values()) == 100, "assessment points no longer total 100")

    for marker in (
        "完整验收时间线",
        "答案与输出隔离协议",
        "十二层神经网络对象账本",
        "20 分钟卷级口试",
        "scorer nonce 与盲参数计算复现门",
        "48 小时换机制重建门",
        "14 天陌生 AI 模型审计迁移门",
        "提交证据清单与状态机",
    ):
        require(marker in assessment, f"assessment misses evidence marker: {marker}")
    retained_marker = "从 " + chr(96) + "retained" + chr(96) + " 到逐节点证据"
    for marker in (
        "卷级口试参考要点",
        "十二层神经网络对象账本参考",
        "实验复现门的评分说明",
        "nonce 与盲参数判分红线",
        "最终状态边界",
        retained_marker,
    ):
        require(marker in solution, f"solution misses rubric marker: {marker}")
    require("才可打开本解答或 canonical 结果" in solution, "solution answer-isolation warning is incomplete")
    for leaked in ("### 第 1 题解答：", "Canonical 三轨数值锚点", "2.90642844"):
        require(leaked not in assessment, f"answer leaked into assessment: {leaked}")
    print("PASS NN-CUM assessment bundle: scope=64/64, questions/answers=14/14, points=100, oral/isolation/nonce/delay gates")


def audit_experiment_contract() -> None:
    experiment = read(EXPERIMENT)
    for marker in (
        "执行顺序、答案隔离与 scorer nonce",
        "进入实验前的解析校准门",
        "禁止循环认证",
        "固定盲参 CLI 回归示例",
        "参数接口与非法合同",
        "证据状态机与延迟门",
        EXPECTED_CUM_SHA256,
        EXPECTED_BLIND_SHA256,
        "--x0",
        "--depth",
        "--mix-lambda",
        "--output",
    ):
        require(marker in experiment, f"experiment misses cumulative marker: {marker}")
    for track in ("A 轨", "B 轨", "C 轨"):
        require(track in experiment, f"experiment misses track: {track}")
    require("not-attempted → attempted → passed → retained" in read(ASSESSMENT), "assessment state route missing")
    print("PASS NN-CUM experiment contract: three tracks, analytic calibration, output protection, blind CLI and state machine")


def mlp_loss(x: tuple[float, float], target: int) -> float:
    weight_1 = ((1.0, -1.0), (0.5, 0.5))
    bias_1 = (0.0, 1.0)
    weight_2 = ((1.0, 0.0), (-1.0, 2.0), (0.5, -1.0))
    bias_2 = (0.0, 0.5, -0.5)
    preactivation = tuple(sum(weight_1[i][j] * x[j] for j in range(2)) + bias_1[i] for i in range(2))
    hidden = tuple(max(0.0, value) for value in preactivation)
    logits = tuple(sum(weight_2[k][j] * hidden[j] for j in range(2)) + bias_2[k] for k in range(3))
    shift = max(logits)
    return -logits[target] + shift + math.log(sum(math.exp(value - shift) for value in logits))


def depth_end_gains(depth: int, base: float, amplitude: float, frequency: float) -> tuple[float, float, float]:
    weights = tuple(base + amplitude * math.sin(frequency * (index + 1)) for index in range(depth))
    plain = math.prod(weights)
    residual = math.prod(1.0 + value for value in weights)
    scaled = math.prod(1.0 + value / math.sqrt(depth) for value in weights)
    return plain, residual, scaled


def smoothed_mix_target(lam: float, epsilon: float) -> tuple[float, ...]:
    mixed = (lam, 0.0, 1.0 - lam, 0.0)
    return tuple((1.0 - epsilon) * value + epsilon / 4.0 for value in mixed)


def audit_exact_models() -> None:
    solution = read(SOLUTION)
    experiment = read(EXPERIMENT)
    canonical_loss = mlp_loss((1.0, -2.0), 2)
    blind_loss = mlp_loss((0.75, -1.5), 1)
    require(math.isclose(canonical_loss, 2.58910368, rel_tol=0.0, abs_tol=5e-9), "canonical MLP loss drifted")
    require(math.isclose(blind_loss, 2.90642844, rel_tol=0.0, abs_tol=5e-9), "blind MLP loss drifted")

    canonical_gains = depth_end_gains(64, 0.15, 0.05, 0.7)
    blind_gains = depth_end_gains(48, 0.12, 0.03, 0.5)
    expected_canonical = (3.82008431e-54, 7701.89764140, 3.29755522)
    expected_blind = (3.38964774e-45, 232.51781404, 2.28625295)
    for actual, expected in zip(canonical_gains, expected_canonical):
        require(math.isclose(actual, expected, rel_tol=5e-9, abs_tol=1e-60), "canonical depth gain drifted")
    for actual, expected in zip(blind_gains, expected_blind):
        require(math.isclose(actual, expected, rel_tol=5e-9, abs_tol=1e-50), "blind depth gain drifted")

    canonical_target = smoothed_mix_target(0.3, 0.2)
    require(all(math.isclose(a, b, abs_tol=1e-15) for a, b in zip(canonical_target, (0.29, 0.05, 0.61, 0.05))), "canonical target drifted")
    blind_target = smoothed_mix_target(0.4, 0.15)
    expected_blind_target = (0.3775, 0.0375, 0.5475, 0.0375)
    require(all(math.isclose(a, b, abs_tol=1e-15) for a, b in zip(blind_target, expected_blind_target)), "blind target drifted")
    canonical_dropout = tuple((1.0 - 0.75) / 0.75 * value * value for value in (2.0, -1.0))
    blind_dropout = tuple((1.0 - 0.6) / 0.6 * value * value for value in (2.0, -1.0))
    require(all(math.isclose(a, b) for a, b in zip(canonical_dropout, (4.0 / 3.0, 1.0 / 3.0))), "canonical Dropout variance drifted")
    require(all(math.isclose(a, b) for a, b in zip(blind_dropout, (8.0 / 3.0, 2.0 / 3.0))), "blind Dropout variance drifted")
    canonical_interaction = (0.20 - 0.26) - (0.27 - 0.30)
    blind_interaction = (0.24 - 0.29) - (0.31 - 0.34)
    require(math.isclose(canonical_interaction, -0.03, abs_tol=1e-15), "canonical interaction drifted")
    require(math.isclose(blind_interaction, -0.02, abs_tol=1e-15), "blind interaction drifted")

    for marker in ("2.58910368", "3.82008431", "0.29000000", "-0.03000000"):
        require(marker in experiment, f"experiment loses canonical anchor: {marker}")
    for marker in ("2.90642844", "3.38964774", "0.3775", "-0.02"):
        require(marker in solution and marker in experiment, f"written blind anchor missing: {marker}")
    print("PASS NN-CUM exact models: canonical/blind MLP, depth products, affine targets, Dropout moments and interactions")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require("NN-CUM-01" in content, f"state surface misses NN-CUM-01: {path.relative_to(ROOT)}")
        require(audit_name in content, f"state surface misses cumulative audit: {path.relative_to(ROOT)}")
        require("regression-passed" in content, f"state surface misses cumulative material pass: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims personal learning: {path.relative_to(ROOT)}")
    print(f"PASS NN-CUM state surfaces: {len(STATE_SURFACES)} views agree on material=regression-passed, personal=not-attempted")


def build_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        key = path.stem if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        index.setdefault(key, []).append(path)
    return index


def resolve(target: str, index: dict[str, list[Path]]) -> list[Path]:
    suffix = Path(target).suffix.lower()
    if "/" in target:
        direct = ROOT / target
        candidates = [direct] if direct.is_file() else []
        if not candidates and suffix not in KNOWN_EXTENSIONS:
            markdown = Path(str(direct) + ".md")
            if markdown.is_file():
                candidates = [markdown]
        return candidates
    key = target[: -len(suffix)] if suffix in KNOWN_EXTENSIONS else target
    candidates = index.get(key, [])
    if suffix in KNOWN_EXTENSIONS:
        candidates = [path for path in candidates if path.suffix.lower() == suffix]
    return candidates


def audit_markdown_integrity() -> None:
    scoped = (MOC, ASSESSMENT, SOLUTION, EXPERIMENT)
    index = build_index()
    links = 0
    missing: list[str] = []
    ambiguous: list[str] = []
    for path in scoped:
        active = active_text(read(path))
        require(active.count("$$") % 2 == 0, f"{path.name}: unbalanced display math")
        for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", active):
            target = raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            links += 1
            candidates = resolve(target, index)
            if not candidates:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing, f"NN-CUM missing Wiki links: {missing}")
    require(not ambiguous, f"NN-CUM ambiguous Wiki links: {ambiguous}")

    experiment_lines = read(EXPERIMENT).splitlines()
    positions = [
        index
        for index, line in enumerate(experiment_lines)
        if re.search(r"!\[\[[^\]]+\.svg(?:\|[^\]]*)?\]\]", line)
    ]
    require(len(positions) == 1, f"NN-CUM experiment expected one formal figure, found {len(positions)}")
    block = "\n".join(experiment_lines[positions[0] : positions[0] + 45])
    for marker in ("[!figure]", "怎样读图", "图没有证明什么"):
        require(marker in block, f"NN-CUM figure unit misses: {marker}")
    print(f"PASS NN-CUM Markdown: scoped Wiki links={links}, display math balanced, figure unit complete")


def stored_artifact_digest() -> str:
    require(CUM_SVG.is_file(), "NN-CUM canonical SVG is missing")
    digest = hashlib.sha256(CUM_SVG.read_bytes()).hexdigest()
    require(digest == EXPECTED_CUM_SHA256, f"stored NN-CUM SVG hash changed: {digest}")
    root_element = ET.parse(CUM_SVG).getroot()
    require(root_element.tag.endswith("svg") and "viewBox" in root_element.attrib, "NN-CUM SVG failed XML/viewBox validation")
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
        f"subprocess failed: {script.relative_to(ROOT)} {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )
    return result.stdout.strip()


def normalized_output(output: str) -> str:
    return "\n".join(line for line in output.splitlines() if not line.startswith("OUTPUT "))


def audit_compute() -> None:
    teaching = run(TEACHING_AUDIT)
    require("NN-01--64 teaching migration regression: PASS" in teaching, "NN teaching prerequisite did not pass")
    stored_before = CUM_SVG.read_bytes()
    with tempfile.TemporaryDirectory(prefix="nn-cum-audit-") as temporary_directory:
        temporary = Path(temporary_directory)
        first_svg = temporary / "canonical-a.svg"
        second_svg = temporary / "canonical-b.svg"
        first_output = run(CUM_SCRIPT, "--output", str(first_svg))
        second_output = run(CUM_SCRIPT, "--output", str(second_svg))
        require(normalized_output(first_output) == normalized_output(second_output), "canonical stdout changed across runs")
        require(first_svg.read_bytes() == second_svg.read_bytes(), "canonical SVG changed across runs")
        require(first_svg.read_bytes() == stored_before, "fresh canonical SVG differs from stored artifact")
        canonical_digest = hashlib.sha256(first_svg.read_bytes()).hexdigest()
        require(canonical_digest == EXPECTED_CUM_SHA256, f"fresh canonical hash changed: {canonical_digest}")
        for marker in (
            "A_CONFIG x0=1 x1=-2 target=3 fd_exponents=1:8",
            "A_GRADIENT mlp_loss=2.58910368 best_grad_error=3.949e-11",
            "B_CONFIG depth=64 weight_base=0.15 weight_amplitude=0.05 weight_frequency=0.7",
            "B_GAINS plain=3.82008431e-54 residual=7701.89764140 scaled=3.29755522",
            "C_TARGET values=0.29000000,0.05000000,0.61000000,0.05000000",
            "dropout_var=1.33333333,0.33333333 interaction=-0.03000000",
            f"SHA256 {EXPECTED_CUM_SHA256}",
        ):
            require(marker in first_output, f"canonical stdout misses: {marker}")
        ET.parse(first_svg)

        unsafe = subprocess.run(
            [sys.executable, str(CUM_SCRIPT), "--depth", "48"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        require(unsafe.returncode != 0, "noncanonical run without --output could overwrite canonical SVG")
        require("noncanonical runs require --output" in unsafe.stderr, "output-protection error message drifted")

        blind_svg = temporary / "blind.svg"
        blind_output = run(
            CUM_SCRIPT,
            "--x0", "0.75",
            "--x1", "-1.5",
            "--target", "1",
            "--depth", "48",
            "--weight-base", "0.12",
            "--weight-amplitude", "0.03",
            "--weight-frequency", "0.5",
            "--ln-scale", "1.5",
            "--ln-shift", "-2",
            "--mix-lambda", "0.4",
            "--label-epsilon", "0.15",
            "--dropout-q", "0.6",
            "--tied-step", "2e-5",
            "--risk00", "0.34",
            "--risk10", "0.29",
            "--risk01", "0.31",
            "--risk11", "0.24",
            "--output", str(blind_svg),
        )
        blind_digest = hashlib.sha256(blind_svg.read_bytes()).hexdigest()
        require(blind_digest == EXPECTED_BLIND_SHA256, f"fixed blind hash changed: {blind_digest}")
        for marker in (
            "A_GRADIENT mlp_loss=2.90642844 best_grad_error=3.837e-11",
            "B_GAINS plain=3.38964774e-45 residual=232.51781404 scaled=2.28625295",
            "B_LAYERNORM scale=1.5 shift=-2 error=2.220e-16",
            "C_TARGET values=0.37750000,0.03750000,0.54750000,0.03750000",
            "dropout_var=2.66666667,0.66666667 interaction=-0.02000000",
            f"SHA256 {EXPECTED_BLIND_SHA256}",
        ):
            require(marker in blind_output, f"blind stdout misses: {marker}")
        blind_text = blind_svg.read_text(encoding="utf-8")
        for marker in (
            "x=(0.75,-1.5) · target=2",
            "深度尺度：L=48",
            "共享目标：λ=0.4, ε=0.15, q=0.6",
            "LN(1.5x-2) vs LN(x)",
        ):
            require(marker in blind_text, f"blind SVG does not self-describe: {marker}")
        ET.parse(blind_svg)

        invalid_cases = (
            (("--depth", "1"), "--depth must be at least 2"),
            (("--dropout-q", "0"), "--dropout-q must lie in (0, 1]"),
            (("--weight-base", "0.05", "--weight-amplitude", "0.05"), "--weight-base must exceed"),
            (("--x0", "0", "--x1", "0"), "too close to a ReLU kink"),
        )
        for arguments, expected_error in invalid_cases:
            result = subprocess.run(
                [sys.executable, str(CUM_SCRIPT), *arguments, "--output", str(temporary / "invalid.svg")],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            require(result.returncode != 0 and expected_error in result.stderr, f"invalid contract was not rejected: {arguments}")

    require(CUM_SVG.read_bytes() == stored_before, "compute audit mutated canonical SVG")
    print("PASS NN-CUM compute prerequisite: NN-01--64 teaching audit")
    print(f"PASS NN-CUM canonical double-run + stored SVG: sha256={EXPECTED_CUM_SHA256}")
    print(f"PASS NN-CUM fixed blind intervention + output/invalid guards: sha256={EXPECTED_BLIND_SHA256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-compute", action="store_true", help="rerun NN-01--64 prerequisite plus NN-CUM canonical/blind gates")
    args = parser.parse_args()
    audit_assessment_bundle()
    audit_experiment_contract()
    audit_exact_models()
    audit_state_surfaces()
    audit_markdown_integrity()
    digest = stored_artifact_digest()
    if args.run_compute:
        audit_compute()
    else:
        print(f"SKIP compute rerun (pass --run-compute for the formal NN-CUM-01 audit); stored sha256={digest}")
    print("NN-CUM-01 material regression: PASS; personal learning: not-attempted")


if __name__ == "__main__":
    main()
