#!/usr/bin/env python3
"""Incremental teaching-contract audit for ARCH-01--64.

The audit keeps three claims separate:
1. the 64-node architecture inventory exists;
2. only the declared migration wave satisfies the current beginner-first contract;
3. personal learning evidence remains not-attempted.

Waves A--C (ARCH-01--12) are recomputed here without importing the figure generators.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "40-表示与模型架构"
LABS = ROOT / "00-知识库管理" / "_labs"
EXERCISES = LABS / "exercises"
SOLUTIONS = LABS / "solutions"
CODE = LABS / "code"
ASSETS = ROOT / "00-知识库管理" / "_assets" / "figures" / "architecture"
MIGRATED_IDS = tuple(range(1, 13))

EXPECTED_FIGURES = {
    "fig-architecture-comparison-contract-v1.svg": "28f2e18521dc3e2c885b98bf528740b7010aad60b610e83990ab9cd6f234139e",
    "fig-discrete-convolution-workbench-v1.svg": "40541302e5981e9de43f7481309442623013350f81ff3087df53d633ade9694a",
    "fig-translation-equivariance-commutation-v1.svg": "7865a6d6eb5253f098bb3d5e178c13807acd57e5dcaa2d8da248137d424e33bd",
    "fig-convolution-shape-ledger-v1.svg": "600e99b8703e3230df93642b8cc419236809afce57196cf56253d855b1041318",
    "fig-pooling-sampling-aliasing-v1.svg": "3337ef790025679f998e8605f0918c21e006813d32878f00ed3421fc3fdd6647",
    "fig-receptive-field-theoretical-effective-v1.svg": "e6222846a62b793743a015d5c934f6e75f234fdc739077bb9e556ff806579c9b",
    "fig-cnn-stage-block-budget-v1.svg": "f4f0a434aac7305c168c96ea3a1c6078a4e36ae9268ab0042425189853e80f09",
    "fig-group-equivariance-evidence-v1.svg": "d6842a9364d871a04f3266d3c62dfc4eb4328250dbe5482b14373f19cacfe2db",
    "fig-sequence-state-causality-contract-v1.svg": "0b4edaf7140a9db9847ba9c92f2e9dc72b1b95294c36e114230c92aebdcfd73e",
    "fig-rnn-bptt-jacobian-product-v1.svg": "23153b6004d623a0a4c135c9325a51df888971d581600ab703c09353d04ca5b1",
    "fig-lstm-cell-gradient-highway-v1.svg": "6ee8c40bce570091442668677a74f98f508aced9796c91904425bd45a58bd759",
    "fig-gru-gate-conventions-v1.svg": "903d535cf953eafd8db57aa7592a1fadc5dd7e860e0f208973ba0aa17749abb8",
}

STATE_SURFACES = (
    CHAPTER / "表示与模型架构 MOC.md",
    CHAPTER / "表示与模型架构完整课程地图与掌握标准.md",
    CHAPTER / "40.1-卷积、空间结构与等变性" / "卷积、空间结构与等变性 MOC.md",
    CHAPTER / "40.2-循环网络、记忆与状态空间模型" / "循环网络、记忆与状态空间模型 MOC.md",
    EXERCISES / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
)

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}
IMAGE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def frontmatter_line(content: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.M)
    return match.group(1).strip() if match else ""


def active_text(content: str) -> str:
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
    return "\n".join(output)


def wiki_targets(content: str, embeds: bool | None = None) -> list[str]:
    text = active_text(content)
    if embeds is True:
        matches = re.findall(r"!\[\[([^\]\n]+)\]\]", text)
    elif embeds is False:
        matches = re.findall(r"(?<!!)\[\[([^\]\n]+)\]\]", text)
    else:
        matches = re.findall(r"\[\[([^\]\n]+)\]\]", text)
    targets: list[str] = []
    for raw in matches:
        target = raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip().rstrip("\\")
        if target:
            targets.append(target)
    return targets


def frontmatter_targets(content: str, key: str) -> list[str]:
    return wiki_targets(frontmatter_line(content, key))


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


def collect_nodes() -> list[tuple[int, Path, str]]:
    nodes: list[tuple[int, Path, str]] = []
    for path in CHAPTER.rglob("*.md"):
        content = read(path)
        match = re.search(r"^node_id:\s*ARCH-(\d{2})$", content, re.M)
        if match:
            nodes.append((int(match.group(1)), path, content))
    return sorted(nodes)


def audit_scope(nodes: list[tuple[int, Path, str]]) -> None:
    ids = [node_id for node_id, _, _ in nodes]
    require(ids == list(range(1, 65)), f"ARCH IDs are not exactly 01--64: {ids}")
    require(len({path for _, path, _ in nodes}) == 64, "ARCH node paths are not unique")
    rows: list[str] = []
    for volume in range(1, 9):
        volume_ids = [node_id for node_id, path, _ in nodes if path.parent.name.startswith(f"40.{volume}-")]
        expected = list(range(8 * volume - 7, 8 * volume + 1))
        require(volume_ids == expected, f"40.{volume} node contract changed: {volume_ids}")
        rows.append(f"40.{volume}=8")
    for node_id, path, content in nodes:
        relative = path.relative_to(ROOT)
        require(frontmatter_line(content, "status") == "draft", f"{relative}: node state must remain draft")
        require(frontmatter_line(content, "node_id") == f"ARCH-{node_id:02d}", f"{relative}: node ID mismatch")
        require(frontmatter_targets(content, "sources"), f"{relative}: sources missing")
        require(len(frontmatter_targets(content, "exercises")) == 1, f"{relative}: exercise link missing")
        require(len(frontmatter_targets(content, "solutions")) == 1, f"{relative}: solution link missing")
        require(len(frontmatter_targets(content, "figure")) == 1, f"{relative}: figure link missing")
        require("[!abstract]" in content, f"{relative}: abstract missing")
        require("怎样读图" in content and "图没有证明什么" in content, f"{relative}: figure unit incomplete")
        require(content.count("$$") % 2 == 0, f"{relative}: display math unbalanced")
    print("PASS ARCH static scope: 64/64 unique nodes; " + ", ".join(rows))


def audit_migrated_contract(nodes: list[tuple[int, Path, str]]) -> None:
    markers = (
        "课程位置与两遍学习路线",
        "问题链",
        "第一遍停靠线",
        "符号与对象账本",
        "贯穿算例",
        "核心公式七问",
    )
    migrated = [(node_id, path, content) for node_id, path, content in nodes if node_id in MIGRATED_IDS]
    require([node_id for node_id, _, _ in migrated] == list(MIGRATED_IDS), "migrated ARCH wave changed")
    for node_id, path, content in migrated:
        relative = path.relative_to(ROOT)
        for marker in markers:
            require(marker in content, f"{relative}: teaching marker missing: {marker}")
        fixture = "\\mathcal C_\\square" if node_id <= 8 else "\\mathcal S_\\square"
        require(fixture in content, f"{relative}: shared fixture missing: {fixture}")
        require("AI" in content, f"{relative}: AI object mapping missing")
        require(frontmatter_line(content, "updated") == "2026-08-29", f"{relative}: migration date mismatch")
        require(len(content.splitlines()) >= 230, f"{relative}: derivation depth unexpectedly short")
    print("PASS ARCH waves A--C: ARCH-01--12 course/two-pass/problem/object/formula contracts=12/12")


def audit_exercises(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    total_ids = 0
    for node_id, path, content in nodes:
        ex_target = frontmatter_targets(content, "exercises")[0]
        sol_target = frontmatter_targets(content, "solutions")[0]
        ex_paths = resolve(ex_target, index)
        sol_paths = resolve(sol_target, index)
        require(len(ex_paths) == 1, f"{path.relative_to(ROOT)}: exercise target unresolved")
        require(len(sol_paths) == 1, f"{path.relative_to(ROOT)}: solution target unresolved")
        exercise = read(ex_paths[0])
        solution = read(sol_paths[0])
        ex_ids = re.findall(r"^###\s+([A-Z0-9]+(?:-[A-Z0-9]+)*-[ABCDE]\d{2})\s*$", exercise, re.M)
        sol_ids = re.findall(r"^###\s+([A-Z0-9]+(?:-[A-Z0-9]+)*-[ABCDE]\d{2})\s*$", solution, re.M)
        require(len(ex_ids) == 15 and len(set(ex_ids)) == 15, f"{ex_paths[0].relative_to(ROOT)}: expected 15 unique IDs")
        require(sol_ids == ex_ids, f"{sol_paths[0].relative_to(ROOT)}: solution IDs/order mismatch")
        total_ids += len(ex_ids)
    require(total_ids == 960, f"exercise total changed: {total_ids}")
    print("PASS ARCH exercises/solutions: 64/64 bijections; 960/960 A--E IDs")


def audit_links_and_figures(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    link_count = 0
    for node_id, path, content in nodes:
        if node_id not in MIGRATED_IDS:
            continue
        for target in wiki_targets(content):
            matches = resolve(target, index)
            require(len(matches) == 1, f"{path.relative_to(ROOT)}: unresolved/ambiguous link {target!r}: {matches}")
            link_count += 1
        embeds = [target for target in wiki_targets(content, embeds=True) if Path(target).suffix.lower() in IMAGE_EXTENSIONS]
        require(len(embeds) == 1, f"{path.relative_to(ROOT)}: expected one formal image embed")
        figure_target = frontmatter_targets(content, "figure")[0]
        require(embeds[0] == figure_target, f"{path.relative_to(ROOT)}: frontmatter/embed figure mismatch")
        require("[!figure]" in content, f"{path.relative_to(ROOT)}: figure caption missing")
    for filename, expected_hash in EXPECTED_FIGURES.items():
        asset = ASSETS / filename
        require(asset.is_file(), f"missing figure: {asset.relative_to(ROOT)}")
        ET.parse(asset)
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()
        require(digest == expected_hash, f"{filename}: hash changed: {digest}")
    print(f"PASS ARCH waves A--C links/figures: Wiki links={link_count}; SVG/XML/hash=12/12")


def correlation_valid(x: list[float], w: list[float]) -> list[float]:
    return [sum(w[j] * x[i + j] for j in range(len(w))) for i in range(len(x) - len(w) + 1)]


def correlation_circular(x: list[float], w: list[float]) -> list[float]:
    n = len(x)
    return [sum(w[j] * x[(i + j) % n] for j in range(len(w))) for i in range(n)]


def shift(x: list[float], amount: int) -> list[float]:
    n = len(x)
    return [x[(i - amount) % n] for i in range(n)]


def rotate_ccw(matrix: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*matrix)][::-1]


def frobenius(a: list[list[float]], b: list[list[float]]) -> float:
    return sum(x * y for row_a, row_b in zip(a, b) for x, y in zip(row_a, row_b))


def audit_migrated_math(nodes: list[tuple[int, Path, str]]) -> None:
    x = [2.0, -1.0, 3.0, 0.0, 1.0]
    w = [1.0, 0.0, -1.0]
    valid = correlation_valid(x, w)
    reversed_valid = correlation_valid(x, list(reversed(w)))
    circular = correlation_circular(x, w)
    commuted = correlation_circular(shift(x, 1), w)
    shifted_output = shift(circular, 1)
    require(valid == [-1.0, -1.0, 2.0], f"valid correlation mismatch: {valid}")
    require(reversed_valid == [1.0, 1.0, -2.0], f"reversed kernel mismatch: {reversed_valid}")
    require(circular == [-1.0, -1.0, 2.0, -2.0, 2.0], f"circular output mismatch: {circular}")
    require(commuted == shifted_output, f"translation commutator nonzero: {commuted} vs {shifted_output}")

    x1 = [1.0, 1.0, 0.0, -1.0, 2.0]
    k00, k01 = [1.0, 0.0, -1.0], [0.0, 1.0, 1.0]
    k10, k11 = [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]
    y0 = [a + b for a, b in zip(correlation_valid(x, k00), correlation_valid(x1, k01))]
    y1 = [a + b + 0.5 for a, b in zip(correlation_valid(x, k10), correlation_valid(x1, k11))]
    require(y0 == [0.0, -2.0, 3.0], f"channel-0 contraction mismatch: {y0}")
    require(y1 == [-1.5, 6.5, -4.5], f"channel-1 contraction mismatch: {y1}")
    parameters = 2 * (2 * 3 + 1)
    macs = 1 * 3 * 2 * 2 * 3
    require(parameters == 14 and macs == 36, "parameter/MAC ledger mismatch")

    alternating = [1.0, -1.0] * 4
    constant = [1.0] * 8
    decimate = lambda values: values[::2]
    box = lambda values: [(values[i] + values[(i + 1) % len(values)]) / 2.0 for i in range(len(values))]
    require(decimate(alternating) == decimate(constant) == [1.0] * 4, "aliasing collision mismatch")
    require(decimate(box(alternating)) == [0.0] * 4, "anti-alias high-frequency probe mismatch")
    require(decimate(box(constant)) == [1.0] * 4, "anti-alias DC probe mismatch")

    receptive_field, jump = 1, 1
    rf_trace: list[tuple[int, int]] = []
    for kernel, stride, dilation in ((3, 1, 1), (3, 2, 1), (3, 1, 2)):
        effective_kernel = dilation * (kernel - 1) + 1
        receptive_field += (effective_kernel - 1) * jump
        jump *= stride
        rf_trace.append((receptive_field, jump))
    require(rf_trace == [(3, 1), (5, 2), (13, 2)], f"RF/jump trace mismatch: {rf_trace}")

    standard_parameters = 32 * 32 * 3 * 3
    separable_parameters = 32 * 3 * 3 + 32 * 32
    standard_macs = 28 * 28 * standard_parameters
    separable_macs = 28 * 28 * separable_parameters
    require(
        (standard_parameters, standard_macs, separable_parameters, separable_macs)
        == (9216, 7_225_344, 1312, 1_028_608),
        "CNN standard/separable ledger mismatch",
    )
    require(math.isclose(separable_parameters / standard_parameters, 41 / 288), "separable ratio mismatch")
    require(64 * 32 * 3 * 3 == 18_432 and 64 * 32 == 2_048, "stage projection ledger mismatch")

    image = [[2.0, -1.0], [0.0, 3.0]]
    template = [[2.0, 0.0], [0.0, -1.0]]
    templates: list[list[list[float]]] = []
    current = template
    for _ in range(4):
        templates.append(current)
        current = rotate_ccw(current)
    group_feature = [frobenius(image, item) for item in templates]
    rotated_image = rotate_ccw(image)
    rotated_feature = [frobenius(rotated_image, item) for item in templates]
    require(group_feature == [1.0, 1.0, 4.0, -2.0], f"C4 lift mismatch: {group_feature}")
    require(rotated_feature == [-2.0, 1.0, 1.0, 4.0], f"C4 transformed lift mismatch: {rotated_feature}")
    require(rotated_feature == [group_feature[-1], *group_feature[:-1]], "C4 output action mismatch")
    require(sum(group_feature) == sum(rotated_feature) == 4.0, "group pooling invariance mismatch")

    inputs = [1.0, 2.0, -1.0]
    recurrent_weight = 0.5
    states = [0.0]
    for value in inputs:
        states.append(recurrent_weight * states[-1] + value)
    require(states == [0.0, 1.0, 2.5, 0.25], f"sequence recurrence mismatch: {states}")
    collision_a = recurrent_weight * (recurrent_weight * 0.0 + 1.0) + 0.0
    collision_b = recurrent_weight * (recurrent_weight * 0.0 + 0.0) + 0.5
    require(collision_a == collision_b == 0.5, "state-compression collision mismatch")

    adjoints = [0.0] * 4
    adjoints[3] = states[3]
    for step in range(2, -1, -1):
        adjoints[step] = recurrent_weight * adjoints[step + 1]
    require(adjoints == [0.03125, 0.0625, 0.125, 0.25], f"BPTT adjoint mismatch: {adjoints}")
    recurrent_gradient = sum(adjoints[step] * states[step - 1] for step in range(1, 4))
    require(math.isclose(recurrent_gradient, 0.75), f"shared recurrent gradient mismatch: {recurrent_gradient}")

    def recurrent_loss(weight: float) -> float:
        state = 0.0
        for value in inputs:
            state = weight * state + value
        return 0.5 * state * state

    epsilon = 1e-6
    finite_difference = (
        recurrent_loss(recurrent_weight + epsilon) - recurrent_loss(recurrent_weight - epsilon)
    ) / (2.0 * epsilon)
    require(math.isclose(finite_difference, recurrent_gradient, rel_tol=1e-9, abs_tol=1e-9), "BPTT finite difference mismatch")

    forget = [0.75, 0.5, 0.8]
    write = [0.5, 0.25, 0.5]
    candidate = [0.5, -1.0, 0.5]
    cell = 1.0
    cell_trace: list[float] = []
    for f_value, i_value, candidate_value in zip(forget, write, candidate):
        cell = f_value * cell + i_value * candidate_value
        cell_trace.append(cell)
    require(cell_trace == [1.0, 0.25, 0.45], f"LSTM cell trace mismatch: {cell_trace}")
    require(math.isclose(math.prod(forget), 0.3), "LSTM direct retention mismatch")
    require(math.isclose(0.8 * math.tanh(cell_trace[-1]), 0.33751918, rel_tol=1e-7), "LSTM readout mismatch")
    lstm_parameters = 4 * 4 * (3 + 4) + 4 * 4
    require(lstm_parameters == 128 and 2 * 4 == 8, "LSTM parameter/state ledger mismatch")

    old_hidden = [1.0, -2.0]
    new_hidden = [-1.0, 2.0]
    update = [0.25, 0.75]
    gru_hidden = [
        (1.0 - gate) * old + gate * new
        for gate, old, new in zip(update, old_hidden, new_hidden)
    ]
    require(gru_hidden == [0.5, 1.0], f"GRU interpolation mismatch: {gru_hidden}")
    matrix = [[1.0, 1.0], [0.0, 1.0]]
    reset = [1.0, 0.0]
    probe = [1.0, 1.0]
    gated_probe = [gate * value for gate, value in zip(reset, probe)]
    reset_before = [sum(row[j] * gated_probe[j] for j in range(2)) for row in matrix]
    mixed_probe = [sum(row[j] * probe[j] for j in range(2)) for row in matrix]
    reset_after = [gate * value for gate, value in zip(reset, mixed_probe)]
    require(reset_before == [1.0, 0.0] and reset_after == [2.0, 0.0], "GRU reset placement mismatch")
    gru_parameters = 3 * 4 * (3 + 4) + 3 * 4
    require(gru_parameters == 96 and 4 == 4, "GRU parameter/state ledger mismatch")

    migrated_text = "\n".join(content for node_id, _, content in nodes if node_id in MIGRATED_IDS)
    for anchor in (
        "(-1,-1,2)", "(-1,-1,2,-2,2)", "14", "36",
        "(3,5,13)", "9,216", "7,225,344", "(1,1,4,-2)",
        "(1,5/2,1/4)", "1/32", "3/4", "(1,1/4,9/20)", "3/10", "(1/2,1)", "128", "96",
    ):
        require(anchor in migrated_text, f"wave-A teaching anchor missing: {anchor}")
    print(
        "PASS ARCH waves A--C independent math: convolution/equivariance, aliasing, RF, "
        "CNN budget, C4 lifting, recurrence/BPTT and LSTM/GRU gates exact"
    )


def audit_state_surfaces() -> None:
    for path in STATE_SURFACES:
        content = read(path)
        relative = path.relative_to(ROOT)
        require("ARCH-01—12" in content, f"{relative}: migrated range missing")
        require("12/64" in content, f"{relative}: migrated count missing")
        require("1/8" in content, f"{relative}: material-gate count missing")
        require("not-attempted" in content, f"{relative}: personal state missing")
    print(
        f"PASS ARCH state surfaces: {len(STATE_SURFACES)} views agree on "
        "migrated=12/64, material gates=1/8, personal=not-attempted"
    )


def audit_compute() -> None:
    before = {name: hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() for name in EXPECTED_FIGURES}
    scripts = (
        (CODE / "plot_architecture_convolution_foundations_v1.py", 4),
        (CODE / "plot_architecture_convolution_advanced_v1.py", 4),
        (CODE / "plot_architecture_sequence_ssm_v1.py", 8),
    )
    for _ in range(2):
        for script, expected_count in scripts:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            require(result.stdout.count("fig-") == expected_count, f"unexpected generator stdout: {result.stdout}")
    after = {name: hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() for name in EXPECTED_FIGURES}
    require(before == after == EXPECTED_FIGURES, f"deterministic figure replay changed assets: {after}")
    print("PASS ARCH waves A--C deterministic figure replay: 12 migrated SVGs, two runs, byte-identical")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-compute", action="store_true")
    args = parser.parse_args()
    nodes = collect_nodes()
    index = build_index()
    audit_scope(nodes)
    audit_migrated_contract(nodes)
    audit_exercises(nodes, index)
    audit_links_and_figures(nodes, index)
    audit_migrated_math(nodes)
    audit_state_surfaces()
    if args.run_compute:
        audit_compute()
    print("ARCH-01--12 teaching migration regression: PASS; chapter material gates=1/8")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
