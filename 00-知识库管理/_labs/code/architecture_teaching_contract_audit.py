#!/usr/bin/env python3
"""Incremental teaching-contract audit for ARCH-01--64.

The audit keeps three claims separate:
1. the 64-node architecture inventory exists;
2. only the declared migration wave satisfies the current beginner-first contract;
3. personal learning evidence remains not-attempted.

Wave A (ARCH-01--04) is recomputed here without importing the figure generator.
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
MIGRATED_IDS = tuple(range(1, 5))

EXPECTED_FIGURES = {
    "fig-architecture-comparison-contract-v1.svg": "28f2e18521dc3e2c885b98bf528740b7010aad60b610e83990ab9cd6f234139e",
    "fig-discrete-convolution-workbench-v1.svg": "40541302e5981e9de43f7481309442623013350f81ff3087df53d633ade9694a",
    "fig-translation-equivariance-commutation-v1.svg": "7865a6d6eb5253f098bb3d5e178c13807acd57e5dcaa2d8da248137d424e33bd",
    "fig-convolution-shape-ledger-v1.svg": "600e99b8703e3230df93642b8cc419236809afce57196cf56253d855b1041318",
}

STATE_SURFACES = (
    CHAPTER / "表示与模型架构 MOC.md",
    CHAPTER / "表示与模型架构完整课程地图与掌握标准.md",
    CHAPTER / "40.1-卷积、空间结构与等变性" / "卷积、空间结构与等变性 MOC.md",
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
        require("\\mathcal C_\\square" in content, f"{relative}: shared fixture missing")
        require("AI" in content, f"{relative}: AI object mapping missing")
        require(frontmatter_line(content, "updated") == "2026-08-29", f"{relative}: migration date mismatch")
        require(len(content.splitlines()) >= 230, f"{relative}: derivation depth unexpectedly short")
    print("PASS ARCH wave A: ARCH-01--04 course/two-pass/problem/object/formula contracts=4/4")


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
    print(f"PASS ARCH wave-A links/figures: Wiki links={link_count}; SVG/XML/hash=4/4")


def correlation_valid(x: list[float], w: list[float]) -> list[float]:
    return [sum(w[j] * x[i + j] for j in range(len(w))) for i in range(len(x) - len(w) + 1)]


def correlation_circular(x: list[float], w: list[float]) -> list[float]:
    n = len(x)
    return [sum(w[j] * x[(i + j) % n] for j in range(len(w))) for i in range(n)]


def shift(x: list[float], amount: int) -> list[float]:
    n = len(x)
    return [x[(i - amount) % n] for i in range(n)]


def audit_wave_a_math(nodes: list[tuple[int, Path, str]]) -> None:
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

    migrated_text = "\n".join(content for node_id, _, content in nodes if node_id in MIGRATED_IDS)
    for anchor in ("(-1,-1,2)", "(-1,-1,2,-2,2)", "14", "36"):
        require(anchor in migrated_text, f"wave-A teaching anchor missing: {anchor}")
    print("PASS ARCH wave-A independent math: valid/reversed/circular correlation, equivariance and multi-channel ledger exact")


def audit_state_surfaces() -> None:
    for path in STATE_SURFACES:
        content = read(path)
        relative = path.relative_to(ROOT)
        require("ARCH-01—04" in content, f"{relative}: migrated range missing")
        require("4/64" in content, f"{relative}: migrated count missing")
        require("not-attempted" in content, f"{relative}: personal state missing")
    print(f"PASS ARCH state surfaces: {len(STATE_SURFACES)} views agree on migrated=4/64, personal=not-attempted")


def audit_compute() -> None:
    script = CODE / "plot_architecture_convolution_foundations_v1.py"
    before = {name: hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() for name in EXPECTED_FIGURES}
    for _ in range(2):
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        require(result.stdout.count("fig-") == 4, f"unexpected generator stdout: {result.stdout}")
    after = {name: hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() for name in EXPECTED_FIGURES}
    require(before == after == EXPECTED_FIGURES, f"deterministic figure replay changed assets: {after}")
    print("PASS ARCH wave-A deterministic figure replay: 4 SVGs, two runs, byte-identical")


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
    audit_wave_a_math(nodes)
    audit_state_surfaces()
    if args.run_compute:
        audit_compute()
    print("ARCH-01--04 teaching migration regression: PASS; chapter material gates=0/8")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
