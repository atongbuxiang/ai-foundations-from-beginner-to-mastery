#!/usr/bin/env python3
"""Static and deterministic material audit for learning theory LT-01--84."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "20-学习理论"
LABS = ROOT / "00-知识库管理" / "_labs"
EXERCISES = LABS / "exercises"
SOLUTIONS = LABS / "solutions"
CODE = LABS / "code"
FIGURE_AUDITOR = CODE / "audit-markdown-figure-units.mjs"
ASSET_DIRS = (
    ROOT / "00-知识库管理" / "_assets" / "figures" / "learning-theory",
    ROOT / "00-知识库管理" / "_assets" / "plots" / "learning-theory",
)
STATE_SURFACES = (
    CHAPTER / "学习理论 MOC.md",
    CHAPTER / "学习理论完整课程地图与掌握标准.md",
    EXERCISES / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
)

VOLUME_CONTRACT = {
    1: (1, 8),
    2: (9, 16),
    3: (17, 24),
    4: (25, 32),
    5: (33, 40),
    6: (41, 52),
    7: (53, 60),
    8: (61, 68),
    9: (69, 76),
    10: (77, 84),
}

EXPECTED_FIGURE_SCRIPTS = {
    "plot_calibration_uncertainty_v2.py",
    "plot_classical_models_core_v2.py",
    "plot_classical_models_ensemble_v2.py",
    "plot_classical_models_unsupervised_v2.py",
    "plot_deep_generalization_part1_v2.py",
    "plot_deep_generalization_part2_v2.py",
    "plot_distribution_shift_v2.py",
    "plot_learning_problem_decision_v2.py",
    "plot_online_learning_part2_v2.py",
    "plot_online_learning_v2.py",
    "plot_pac_bayes_information_v2.py",
    "plot_pac_finite_class_v2.py",
    "plot_rademacher_advanced_v2.py",
    "plot_rademacher_core_v2.py",
    "plot_representation_contrastive_v2.py",
    "plot_selfsupervised_transfer_v2.py",
    "plot_stability_compression_v2.py",
    "plot_vc_extensions_v2.py",
}

KNOWN_EXTENSIONS = {
    ".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf",
}
IMAGE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


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


def frontmatter_line(content: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.M)
    return match.group(1).strip() if match else ""


def wiki_targets(content: str, embeds: bool | None = None) -> list[str]:
    lines = active_lines(content)
    joined = "\n".join(lines)
    if embeds is True:
        matches = re.findall(r"!\[\[([^\]\n]+)\]\]", joined)
    elif embeds is False:
        matches = re.findall(r"(?<!!)\[\[([^\]\n]+)\]\]", joined)
    else:
        matches = re.findall(r"\[\[([^\]\n]+)\]\]", joined)
    targets: list[str] = []
    for raw in matches:
        normalized = raw.replace("\\|", "|")
        target = normalized.split("|", 1)[0].split("#", 1)[0].strip().rstrip("\\")
        if target:
            targets.append(target)
    return targets


def frontmatter_targets(content: str, key: str) -> list[str]:
    value = frontmatter_line(content, key)
    return wiki_targets(value)


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
        candidates = [candidate for candidate in candidates if candidate.suffix.lower() == suffix]
    return candidates


def collect_nodes() -> list[tuple[int, Path, str]]:
    nodes: list[tuple[int, Path, str]] = []
    for path in CHAPTER.rglob("*.md"):
        content = read(path)
        match = re.search(r"^node_id:\s*LT-(\d{2})$", content, re.M)
        if match:
            nodes.append((int(match.group(1)), path, content))
    nodes.sort()
    return nodes


def audit_scope_and_node_contracts(nodes: list[tuple[int, Path, str]]) -> None:
    ids = [node_id for node_id, _, _ in nodes]
    require(ids == list(range(1, 85)), f"LT IDs are not exactly 01--84: {ids}")
    require(len({path for _, path, _ in nodes}) == 84, "LT node paths are not unique")

    volume_rows: list[str] = []
    for volume, (first, last) in VOLUME_CONTRACT.items():
        volume_nodes = [
            node_id for node_id, path, _ in nodes
            if re.match(rf"20\.{volume}(?:-|$)", path.parent.name)
        ]
        expected = list(range(first, last + 1))
        require(volume_nodes == expected, f"20.{volume} node contract changed: {volume_nodes}")
        volume_path = next(
            path for node_id, path, _content in nodes if first <= node_id <= last
        ).parent
        mocs = list(volume_path.glob("*MOC.md"))
        require(len(mocs) == 1, f"20.{volume} must have exactly one volume MOC")
        volume_rows.append(f"20.{volume}={len(volume_nodes)}")

    type_counts: Counter[str] = Counter()
    allowed_types = {"concept", "theorem", "comparison", "synthesis"}
    for node_id, path, content in nodes:
        relative = path.relative_to(ROOT)
        node_type = frontmatter_line(content, "type")
        require(node_type in allowed_types, f"{relative}: unsupported teaching type {node_type!r}")
        type_counts[node_type] += 1
        require(frontmatter_line(content, "status") == "draft", f"{relative}: learning state must remain draft")
        require(frontmatter_line(content, "node_id") == f"LT-{node_id:02d}", f"{relative}: node ID mismatch")
        require(frontmatter_line(content, "created"), f"{relative}: created date missing")
        require(frontmatter_line(content, "updated"), f"{relative}: updated date missing")
        require(frontmatter_targets(content, "sources"), f"{relative}: sources missing")
        require(len(frontmatter_targets(content, "exercises")) == 1, f"{relative}: exercise link must be singular")
        require(len(frontmatter_targets(content, "solutions")) == 1, f"{relative}: solution link must be singular")
        require("[!abstract]" in content, f"{relative}: main-problem abstract missing")
        require(
            "学习目标" in content or "学完本章应能做什么" in content,
            f"{relative}: beginner learning goals missing",
        )
        require("怎样读图" in content, f"{relative}: read-the-figure guidance missing")
        require(
            "适用边界" in content or "图没有证明什么" in content,
            f"{relative}: figure boundary missing",
        )
        require(content.count("$$") % 2 == 0, f"{relative}: unbalanced display math")
    print(
        "PASS LT scope and node contracts: 84/84 unique nodes; "
        + ", ".join(volume_rows)
        + f"; types={dict(sorted(type_counts.items()))}"
    )


def question_ids(content: str) -> list[str]:
    return re.findall(r"^###\s+([^\s]+-[A-E]\d{2})\s*$", content, re.M)


def audit_exercise_solution_bijection(
    nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]
) -> None:
    all_exercise_ids: list[str] = []
    all_solution_ids: list[str] = []
    seen_exercises: set[Path] = set()
    seen_solutions: set[Path] = set()

    for node_id, node_path, node in nodes:
        exercise_target = frontmatter_targets(node, "exercises")[0]
        solution_target = frontmatter_targets(node, "solutions")[0]
        exercise_paths = resolve(exercise_target, index)
        solution_paths = resolve(solution_target, index)
        require(len(exercise_paths) == 1, f"LT-{node_id:02d}: exercise target is missing/ambiguous")
        require(len(solution_paths) == 1, f"LT-{node_id:02d}: solution target is missing/ambiguous")
        exercise_path, solution_path = exercise_paths[0], solution_paths[0]
        require(exercise_path.parent == EXERCISES, f"LT-{node_id:02d}: exercise stored outside exercise lab")
        require(solution_path.parent == SOLUTIONS, f"LT-{node_id:02d}: solution stored outside solution lab")
        require(exercise_path not in seen_exercises, f"exercise reused by multiple nodes: {exercise_path.name}")
        require(solution_path not in seen_solutions, f"solution reused by multiple nodes: {solution_path.name}")
        seen_exercises.add(exercise_path)
        seen_solutions.add(solution_path)

        exercise, solution = read(exercise_path), read(solution_path)
        require(frontmatter_line(exercise, "type") == "exercise", f"{exercise_path.name}: type changed")
        require(frontmatter_line(solution, "type") == "solution", f"{solution_path.name}: type changed")
        require(frontmatter_line(exercise, "status") == "draft", f"{exercise_path.name}: personal state changed")
        require(frontmatter_line(solution, "status") == "draft", f"{solution_path.name}: personal state changed")
        require(node_path.stem in frontmatter_targets(exercise, "topic"), f"{exercise_path.name}: topic backlink changed")
        require(node_path.stem in frontmatter_targets(solution, "topic"), f"{solution_path.name}: topic backlink changed")
        require(solution_path.stem in frontmatter_targets(exercise, "solution"), f"{exercise_path.name}: solution backlink changed")
        require(exercise_path.stem in frontmatter_targets(solution, "exercise"), f"{solution_path.name}: exercise backlink changed")

        exercise_ids = question_ids(exercise)
        solution_ids = question_ids(solution)
        require(len(exercise_ids) == len(set(exercise_ids)) == 15, f"{exercise_path.name}: expected 15 unique questions")
        require(exercise_ids == solution_ids, f"LT-{node_id:02d}: question/solution IDs or order differ")
        levels = Counter(identifier.rsplit("-", 1)[-1][0] for identifier in exercise_ids)
        require(levels == Counter({level: 3 for level in "ABCDE"}), f"{exercise_path.name}: A--E distribution changed")
        all_exercise_ids.extend(exercise_ids)
        all_solution_ids.extend(solution_ids)

    require(len(seen_exercises) == len(seen_solutions) == 84, "LT support-file count changed")
    require(len(all_exercise_ids) == len(all_solution_ids) == 1260, "LT question total changed")
    require(len(set(all_exercise_ids)) == 1260, "LT question IDs are not globally unique")
    require(all_exercise_ids == all_solution_ids, "LT chapter question/solution sequence changed")
    print("PASS LT exercises and solutions: 84/84 bijections; 1260/1260 A--E IDs")


def audit_sources_and_links(
    nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]
) -> None:
    source_targets = sorted({
        target
        for _, _, content in nodes
        for target in frontmatter_targets(content, "sources")
    })
    status_counts: Counter[str] = Counter()
    for target in source_targets:
        paths = resolve(target, index)
        require(len(paths) == 1, f"source target is missing/ambiguous: {target}")
        source = read(paths[0])
        require(paths[0].parent.name == "_sources", f"source target is not a source card: {target}")
        status = frontmatter_line(source, "status")
        require(status in {"active", "verified", "draft"}, f"unsupported source status: {target} -> {status}")
        status_counts[status] += 1
        for key in (
            "source_type", "title", "author", "year", "url", "accessed",
            "source_tier", "scope_role", "temporal_role",
        ):
            require(frontmatter_line(source, key), f"source metadata misses {key}: {target}")
        if status == "draft":
            require(frontmatter_line(source, "source_type") == "blog", f"draft formal source is not allowed: {target}")
            require(frontmatter_line(source, "source_tier") == "C", f"draft source must be tier C: {target}")
            require("核心断言" in source and "边界" in source, f"draft bridge lacks assertion/boundary audit: {target}")

    scoped = sorted(CHAPTER.rglob("*.md"))
    missing: list[str] = []
    ambiguous: list[str] = []
    link_count = 0
    for path in scoped:
        for target in wiki_targets(read(path), embeds=False):
            link_count += 1
            candidates = resolve(target, index)
            if not candidates:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing, f"missing LT Wiki links: {missing[:20]}")
    require(not ambiguous, f"ambiguous LT Wiki links: {ambiguous[:20]}")
    print(
        f"PASS LT sources and links: source cards={len(source_targets)} "
        f"{dict(sorted(status_counts.items()))}; scoped Wiki links={link_count}"
    )


def audit_figures(
    nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]
) -> set[Path]:
    assets: set[Path] = set()
    figure_scripts: set[str] = set()
    node_files_with_figures: set[Path] = set()
    embed_count = 0

    for _, path, content in nodes:
        embeds = wiki_targets(content, embeds=True)
        require(embeds, f"{path.relative_to(ROOT)}: no formal visual")
        node_files_with_figures.add(path)
        for target in embeds:
            embed_count += 1
            require(target.startswith("00-知识库管理/"), f"relative/non-rooted LT image target: {target}")
            candidates = resolve(target, index)
            require(len(candidates) == 1, f"LT image is missing/ambiguous: {target}")
            asset = candidates[0]
            require(asset.suffix.lower() in IMAGE_EXTENSIONS, f"non-image embed in LT node: {target}")
            assets.add(asset)
            if asset.suffix.lower() == ".svg":
                root = ET.parse(asset).getroot()
                require(root.tag.endswith("svg") and "viewBox" in root.attrib, f"invalid SVG contract: {target}")
        for target in wiki_targets(content, embeds=False):
            if target.startswith("plot_") and target.endswith(".py"):
                figure_scripts.add(target)

    require(len(node_files_with_figures) == 84, "not every LT node has a formal visual")
    require(embed_count == 96, f"LT node figure count changed: {embed_count}")
    require(figure_scripts == EXPECTED_FIGURE_SCRIPTS, f"LT figure-script set changed: {sorted(figure_scripts)}")
    for script in figure_scripts:
        require((CODE / script).is_file(), f"missing LT figure script: {script}")

    result = subprocess.run(
        ["node", str(FIGURE_AUDITOR), str(ROOT), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"figure-unit auditor failed:\n{result.stderr}")
    payload = json.loads(result.stdout)
    records = [
        record for record in payload["records"]
        if record["file"].startswith("20-学习理论/")
    ]
    failed = [record for record in records if not record["pass"]]
    require(len(records) == 97, f"LT scoped figure-unit count changed: {len(records)}")
    require(not failed, f"LT figure units failed: {failed[:10]}")
    print(
        f"PASS LT figures: node embeds={embed_count}; chapter figure units=97/97; "
        f"SVG/XML assets={sum(path.suffix.lower() == '.svg' for path in assets)}; scripts=18"
    )
    return assets


def snapshot_assets() -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for directory in ASSET_DIRS:
        require(directory.is_dir(), f"missing LT asset directory: {directory.relative_to(ROOT)}")
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                snapshot[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def run_figure_scripts() -> None:
    for name in sorted(EXPECTED_FIGURE_SCRIPTS):
        script = CODE / name
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(
            result.returncode == 0,
            f"LT figure script failed: {name}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


def audit_deterministic_figures() -> None:
    before = snapshot_assets()
    run_figure_scripts()
    first = snapshot_assets()
    run_figure_scripts()
    second = snapshot_assets()
    require(before == first, "stored LT assets differ from one deterministic regeneration")
    require(first == second, "LT figure regeneration is not byte deterministic")
    print(f"PASS LT deterministic figures: scripts=18; stored assets={len(before)}; double-run byte identity")


def audit_curriculum_map(nodes: list[tuple[int, Path, str]]) -> None:
    curriculum = read(CHAPTER / "学习理论完整课程地图与掌握标准.md")
    root_moc = read(CHAPTER / "学习理论 MOC.md")
    mapped = {
        int(node_id): title
        for node_id, title in re.findall(r"^\| LT-(\d{2}) \| \[\[([^\]|]+)", curriculum, re.M)
    }
    require(sorted(mapped) == list(range(1, 85)), "curriculum map does not contain LT-01--84 exactly once")
    for node_id, path, _ in nodes:
        require(mapped[node_id] == path.stem, f"curriculum map/path mismatch for LT-{node_id:02d}")
    for content, label in ((curriculum, "curriculum"), (root_moc, "root MOC")):
        require("84" in content and "10" in content, f"{label}: fixed scope markers missing")
        require("not-attempted" in content, f"{label}: personal state boundary missing")
    print("PASS LT curriculum map: 84/84 ID-title-path mappings; ten-volume scope fixed")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require(audit_name in content, f"state surface misses LT audit: {path.relative_to(ROOT)}")
        require("regression-passed" in content, f"state surface misses material state: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface misses personal state: {path.relative_to(ROOT)}")
        require(re.search(r"0\s*/\s*10", content) is not None, f"state surface misses zero volume gates: {path.relative_to(ROOT)}")
    print(f"PASS LT state surfaces: {len(STATE_SURFACES)} curriculum/lab/ledger views agree")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-compute",
        action="store_true",
        help="Regenerate all 18 LT figure families twice and require byte identity.",
    )
    args = parser.parse_args()

    nodes = collect_nodes()
    index = build_index()
    audit_scope_and_node_contracts(nodes)
    audit_exercise_solution_bijection(nodes, index)
    audit_sources_and_links(nodes, index)
    audit_figures(nodes, index)
    audit_curriculum_map(nodes)
    audit_state_surfaces()
    if args.run_compute:
        audit_deterministic_figures()
    print("LT-01--84 material regression: PASS")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
