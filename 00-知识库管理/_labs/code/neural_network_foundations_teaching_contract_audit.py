#!/usr/bin/env python3
"""Static inventory and incremental teaching-contract audit for NN-01--64."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "30-神经网络基础"
LABS = ROOT / "00-知识库管理" / "_labs"
EXERCISES = LABS / "exercises"
SOLUTIONS = LABS / "solutions"
CODE = LABS / "code"
FIGURE_AUDITOR = CODE / "audit-markdown-figure-units.mjs"
ASSET_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "neural-networks"
MIGRATED_IDS = tuple(range(1, 17))

STATE_SURFACES = (
    CHAPTER / "神经网络基础 MOC.md",
    CHAPTER / "神经网络基础完整课程地图与掌握标准.md",
    EXERCISES / "练习与测验 MOC.md",
    LABS / "推导与实验 MOC.md",
    ROOT / "00-知识库管理" / "00-总览" / "全库教学重写审计与迁移台账.md",
    CHAPTER / "30.1-前馈网络、感知机与表达能力" / "前馈网络、感知机与表达能力 MOC.md",
    CHAPTER / "30.2-计算图、反向传播与自动微分" / "计算图、反向传播与自动微分 MOC.md",
)

EXPECTED_FIGURE_SCRIPTS = {
    "plot_activation_advanced_v2.py",
    "plot_activation_foundations_v2.py",
    "plot_backprop_advanced_v2.py",
    "plot_backprop_foundations_v2.py",
    "plot_embedding_output_advanced_v2.py",
    "plot_embedding_output_foundations_v2.py",
    "plot_feedforward_expressivity_v2.py",
    "plot_feedforward_foundations_v2.py",
    "plot_initialization_advanced_v2.py",
    "plot_initialization_foundations_v2.py",
    "plot_normalization_advanced_v2.py",
    "plot_normalization_foundations_v2.py",
    "plot_random_regularization_foundations_v2.py",
    "plot_regularization_interfaces_v2.py",
    "plot_residual_advanced_v2.py",
    "plot_residual_foundations_v2.py",
}

KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}
IMAGE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
SOURCE_KEYS = (
    "source_type", "title", "author", "year", "url", "accessed",
    "source_tier", "scope_role", "temporal_role",
)


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


def frontmatter_line(content: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.M)
    return match.group(1).strip() if match else ""


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
        match = re.search(r"^node_id:\s*NN-(\d{2})$", content, re.M)
        if match:
            nodes.append((int(match.group(1)), path, content))
    return sorted(nodes)


def audit_scope(nodes: list[tuple[int, Path, str]]) -> None:
    ids = [node_id for node_id, _, _ in nodes]
    require(ids == list(range(1, 65)), f"NN IDs are not exactly 01--64: {ids}")
    require(len({path for _, path, _ in nodes}) == 64, "NN node paths are not unique")
    volume_rows: list[str] = []
    allowed_types = {"comparison", "concept", "derivation", "framework", "method", "moc", "model", "synthesis", "theorem"}
    type_counts: Counter[str] = Counter()
    for volume in range(1, 9):
        volume_ids = [node_id for node_id, path, _ in nodes if path.parent.name.startswith(f"30.{volume}-")]
        expected = list(range(8 * volume - 7, 8 * volume + 1))
        require(volume_ids == expected, f"30.{volume} node contract changed: {volume_ids}")
        volume_rows.append(f"30.{volume}=8")
    for node_id, path, content in nodes:
        relative = path.relative_to(ROOT)
        node_type = frontmatter_line(content, "type")
        require(node_type in allowed_types, f"{relative}: unsupported type {node_type!r}")
        type_counts[node_type] += 1
        require(frontmatter_line(content, "status") == "draft", f"{relative}: node state must remain draft")
        require(frontmatter_line(content, "node_id") == f"NN-{node_id:02d}", f"{relative}: node ID mismatch")
        require(frontmatter_line(content, "created") and frontmatter_line(content, "updated"), f"{relative}: dates missing")
        require(frontmatter_targets(content, "sources"), f"{relative}: sources missing")
        require(len(frontmatter_targets(content, "exercises")) == 1, f"{relative}: exercise target must be singular")
        require(len(frontmatter_targets(content, "solutions")) == 1, f"{relative}: solution target must be singular")
        require(len(frontmatter_targets(content, "figure")) == 1, f"{relative}: figure frontmatter target missing")
        require("[!abstract]" in content, f"{relative}: abstract missing")
        require("怎样读图" in content and "图没有证明什么" in content, f"{relative}: figure reading/boundary contract missing")
        require(content.count("$$") % 2 == 0, f"{relative}: unbalanced display math")
    print(
        "PASS NN static scope: 64/64 unique nodes; " + ", ".join(volume_rows)
        + f"; types={dict(sorted(type_counts.items()))}"
    )


def audit_migrated_contract(nodes: list[tuple[int, Path, str]]) -> None:
    markers = (
        "课程位置与两遍学习路线", "问题链", "第一遍停靠线",
        "符号与对象账本", "贯穿算例", "核心公式七问",
    )
    migrated = [(node_id, path, content) for node_id, path, content in nodes if node_id in MIGRATED_IDS]
    require([node_id for node_id, _, _ in migrated] == list(MIGRATED_IDS), "migrated NN wave changed")
    for node_id, path, content in migrated:
        relative = path.relative_to(ROOT)
        for marker in markers:
            require(marker in content, f"{relative}: teaching-contract marker missing: {marker}")
        fixture = "X_\\star" if node_id <= 4 else "X_\\oplus" if node_id <= 8 else "X_\\diamond"
        require(fixture in content, f"{relative}: shared teaching fixture missing: {fixture}")
        require("AI" in content, f"{relative}: AI object mapping missing")
        require(len(content.splitlines()) >= 180, f"{relative}: derivation depth unexpectedly short")
    print("PASS NN teaching migration waves A--D: NN-01--16 course position/two-pass/problem/object/formula contracts=16/16")


def audit_wave_c_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-09--12 affine-regression fixture without importing note code."""
    x = ((1.0, 2.0), (-1.0, 1.0))
    w = ((1.0, -1.0), (2.0, 1.0))
    b = (0.0, 1.0)
    y = ((4.0, 1.0), (2.0, 1.0))
    lam = 0.5

    def mm(a: tuple[tuple[float, ...], ...], c: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        return tuple(tuple(sum(a[i][k] * c[k][j] for k in range(len(c))) for j in range(len(c[0]))) for i in range(len(a)))

    def transpose(a: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        return tuple(tuple(a[i][j] for i in range(len(a))) for j in range(len(a[0])))

    z0 = mm(x, w)
    z = tuple(tuple(z0[i][j] + b[j] for j in range(2)) for i in range(2))
    residual = tuple(tuple(z[i][j] - y[i][j] for j in range(2)) for i in range(2))
    loss = 0.5 * sum(value * value for row in residual for value in row) + 0.5 * lam * sum(value * value for row in w for value in row)
    require(z == ((5.0, 2.0), (1.0, 3.0)) and residual == ((1.0, 1.0), (-1.0, 2.0)), "NN wave-C forward fixture drifted")
    require(loss == 5.25, f"NN wave-C loss drifted: {loss}")

    direction = ((1.0, 0.0), (0.0, 0.0))
    dz = mm(x, direction)
    directional = sum(residual[i][j] * dz[i][j] for i in range(2) for j in range(2)) + lam * sum(w[i][j] * direction[i][j] for i in range(2) for j in range(2))
    data_w = mm(transpose(x), residual)
    reg_w = tuple(tuple(lam * w[i][j] for j in range(2)) for i in range(2))
    total_w = tuple(tuple(data_w[i][j] + reg_w[i][j] for j in range(2)) for i in range(2))
    grad_x = mm(residual, transpose(w))
    grad_b = tuple(sum(residual[i][j] for i in range(2)) for j in range(2))
    require(dz == ((1.0, 0.0), (-1.0, 0.0)) and directional == 2.5, "NN wave-C JVP drifted")
    require(data_w == ((2.0, -1.0), (1.0, 4.0)), f"NN wave-C data gradient drifted: {data_w}")
    require(total_w == ((2.5, -1.5), (2.0, 4.5)), f"NN wave-C total gradient drifted: {total_w}")
    require(grad_x == ((0.0, 3.0), (-3.0, 0.0)) and grad_b == (0.0, 3.0), "NN wave-C affine VJP drifted")

    wave = {node_id: content for node_id, _, content in nodes if 9 <= node_id <= 12}
    expected_markers = {9: ("L=5.25",), 10: ("2.5",), 11: ("L=5.25", "2.5"), 12: ("2.5",)}
    for node_id, expected in expected_markers.items():
        require(all(marker in wave[node_id] for marker in expected), f"NN-{node_id:02d}: shared numeric closure missing")
    print("PASS NN wave-C independent math: forward loss=5.25; JVP/VJP=2.5; data/reg/affine gradients exact")


def audit_wave_d_fixture(nodes: list[tuple[int, Path, str]]) -> None:
    """Recompute the NN-13--16 residual-softmax fixture independently."""
    z = ((5.0, 2.0), (1.0, 3.0))
    c = (2.0, 2.0)
    a = tuple(tuple(z[i][j] - c[j] for j in range(2)) for i in range(2))
    h = tuple(tuple(max(0.0, a[i][j]) for j in range(2)) for i in range(2))
    q = tuple(tuple(z[i][j] + h[i][j] for j in range(2)) for i in range(2))
    require(a == ((3.0, 0.0), (-1.0, 1.0)) and h == ((3.0, 0.0), (0.0, 1.0)), "NN wave-D ReLU fixture drifted")
    require(q == ((8.0, 2.0), (1.0, 4.0)), f"NN wave-D logits drifted: {q}")

    upstream = ((1.0, -1.0), (2.0, 1.0))
    mask = tuple(tuple(1.0 if a[i][j] > 0.0 else 0.0 for j in range(2)) for i in range(2))
    grad_z = tuple(tuple(upstream[i][j] * (1.0 + mask[i][j]) for j in range(2)) for i in range(2))
    grad_c = tuple(-sum(upstream[i][j] * mask[i][j] for i in range(2)) for j in range(2))
    require(grad_z == ((2.0, -1.0), (2.0, 2.0)) and grad_c == (-1.0, -1.0), "NN wave-D branch/broadcast VJP drifted")

    probs: list[tuple[float, float]] = []
    for row in q:
        maximum = max(row)
        exps = tuple(math.exp(value - maximum) for value in row)
        total = sum(exps)
        probs.append((exps[0] / total, exps[1] / total))
    loss = (-math.log(probs[0][0]) - math.log(probs[1][1])) / 2.0
    logit_grad = (((probs[0][0] - 1.0) / 2.0, probs[0][1] / 2.0), (probs[1][0] / 2.0, (probs[1][1] - 1.0) / 2.0))
    directional = logit_grad[0][0]
    hvp_scale = probs[0][0] * probs[0][1] / 2.0
    require(abs(loss - 0.02553151835573612) < 1e-15, f"NN wave-D CE loss drifted: {loss}")
    require(abs(directional + 0.0012363115783173284) < 1e-15, f"NN wave-D JVP/VJP drifted: {directional}")
    require(abs(hvp_scale - 0.0012332546456799655) < 1e-15, f"NN wave-D HVP drifted: {hvp_scale}")
    require(all(abs(sum(row)) < 1e-15 for row in logit_grad), "NN wave-D softmax shift-null direction drifted")

    wave = {node_id: content for node_id, _, content in nodes if 13 <= node_id <= 16}
    expected = {13: ("Q=Z+H",), 14: ("0.0255315",), 15: ("-0.00123631",), 16: ("0.00123325",)}
    for node_id, markers in expected.items():
        require(all(marker in wave[node_id] for marker in markers), f"NN-{node_id:02d}: wave-D numeric closure missing")
    print("PASS NN wave-D independent math: residual/broadcast VJP; stable CE=0.0255315; JVP/VJP and HVP exact")


def question_ids(content: str) -> list[str]:
    return re.findall(r"^###\s+([^\s]+-[A-E]\d{2})\s*$", content, re.M)


def audit_exercises(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    seen_exercises: set[Path] = set()
    seen_solutions: set[Path] = set()
    all_ids: list[str] = []
    for node_id, node_path, node in nodes:
        exercise_paths = resolve(frontmatter_targets(node, "exercises")[0], index)
        solution_paths = resolve(frontmatter_targets(node, "solutions")[0], index)
        require(len(exercise_paths) == len(solution_paths) == 1, f"NN-{node_id:02d}: exercise/solution missing or ambiguous")
        exercise_path, solution_path = exercise_paths[0], solution_paths[0]
        require(exercise_path.parent == EXERCISES and solution_path.parent == SOLUTIONS, f"NN-{node_id:02d}: support file outside lab")
        require(exercise_path not in seen_exercises and solution_path not in seen_solutions, f"NN-{node_id:02d}: support file reused")
        seen_exercises.add(exercise_path)
        seen_solutions.add(solution_path)
        exercise, solution = read(exercise_path), read(solution_path)
        require(frontmatter_line(exercise, "type") == "exercise" and frontmatter_line(solution, "type") == "solution", f"NN-{node_id:02d}: support type mismatch")
        require(frontmatter_line(exercise, "status") == frontmatter_line(solution, "status") == "draft", f"NN-{node_id:02d}: learner state changed")
        require(node_path.stem in frontmatter_targets(exercise, "topic"), f"NN-{node_id:02d}: exercise topic backlink missing")
        require(node_path.stem in frontmatter_targets(solution, "topic"), f"NN-{node_id:02d}: solution topic backlink missing")
        require(solution_path.stem in frontmatter_targets(exercise, "solution"), f"NN-{node_id:02d}: exercise solution link missing")
        require(exercise_path.stem in frontmatter_targets(solution, "exercise"), f"NN-{node_id:02d}: solution exercise link missing")
        exercise_ids, solution_ids = question_ids(exercise), question_ids(solution)
        require(exercise_ids == solution_ids, f"NN-{node_id:02d}: question/solution order differs")
        require(len(exercise_ids) == len(set(exercise_ids)) == 15, f"NN-{node_id:02d}: expected 15 unique A--E questions")
        require(Counter(identifier.rsplit("-", 1)[-1][0] for identifier in exercise_ids) == Counter({level: 3 for level in "ABCDE"}), f"NN-{node_id:02d}: A--E distribution changed")
        all_ids.extend(exercise_ids)
    require(len(seen_exercises) == len(seen_solutions) == 64, "NN support-file count changed")
    require(len(all_ids) == len(set(all_ids)) == 960, "NN global question total/uniqueness changed")
    print("PASS NN exercises and solutions: 64/64 bijections; 960/960 A--E IDs")


def audit_sources_and_links(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    source_targets = sorted({target for _, _, content in nodes for target in frontmatter_targets(content, "sources")})
    migrated_source_targets = {target for node_id, _, content in nodes if node_id in MIGRATED_IDS for target in frontmatter_targets(content, "sources")}
    status_counts: Counter[str] = Counter()
    legacy_metadata_gaps: list[str] = []
    migrated_tiers: dict[str, str] = {}
    for target in source_targets:
        paths = resolve(target, index)
        require(len(paths) == 1 and paths[0].parent.name == "_sources", f"source missing/ambiguous/not a card: {target}")
        source = read(paths[0])
        status = frontmatter_line(source, "status")
        require(status in {"active", "verified", "draft"}, f"unsupported source status: {target} -> {status}")
        status_counts[status] += 1
        missing_keys = [key for key in SOURCE_KEYS if not frontmatter_line(source, key)]
        if target in migrated_source_targets:
            require(not missing_keys, f"migrated-wave source metadata incomplete: {target} -> {missing_keys}")
            tier = frontmatter_line(source, "source_tier")
            require(tier in {"A", "B", "C"}, f"migrated-wave source tier unsupported: {target} -> {tier}")
            migrated_tiers[target] = tier
            if tier in {"A", "B"}:
                require(status in {"active", "verified"}, f"migrated-wave A/B source not active/verified: {target}")
            else:
                require(status in {"draft", "active", "verified"}, f"migrated-wave C source status unsupported: {target}")
        elif missing_keys:
            legacy_metadata_gaps.extend(f"{target}:{key}" for key in missing_keys)

    for node_id, _, content in nodes:
        if node_id not in MIGRATED_IDS:
            continue
        tiers = {migrated_tiers[target] for target in frontmatter_targets(content, "sources")}
        require(tiers & {"A", "B"}, f"NN-{node_id:02d}: migrated node lacks an A/B source anchor")

    missing: list[str] = []
    ambiguous: list[str] = []
    link_count = 0
    for path in sorted(CHAPTER.rglob("*.md")):
        for target in wiki_targets(read(path), embeds=False):
            link_count += 1
            candidates = resolve(target, index)
            if not candidates:
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous.append(f"{path.relative_to(ROOT)} -> {target}")
    require(not missing, f"missing NN Wiki links: {missing[:20]}")
    require(not ambiguous, f"ambiguous NN Wiki links: {ambiguous[:20]}")
    print(
        f"PASS NN sources/links: cards={len(source_targets)} {dict(sorted(status_counts.items()))}; "
        f"migrated-wave metadata complete with per-node A/B anchors; legacy metadata fields pending={len(legacy_metadata_gaps)}; scoped Wiki links={link_count}"
    )


def audit_figures(nodes: list[tuple[int, Path, str]], index: dict[str, list[Path]]) -> None:
    assets: set[Path] = set()
    scripts: set[str] = set()
    embed_count = 0
    for _, path, content in nodes:
        embeds = wiki_targets(content, embeds=True)
        require(len(embeds) == 1, f"{path.relative_to(ROOT)}: expected exactly one formal visual")
        target = embeds[0]
        embed_count += 1
        require(target.startswith("00-知识库管理/_assets/figures/neural-networks/"), f"unstable NN image target: {target}")
        candidates = resolve(target, index)
        require(len(candidates) == 1 and candidates[0].suffix.lower() in IMAGE_EXTENSIONS, f"NN image missing/ambiguous: {target}")
        asset = candidates[0]
        assets.add(asset)
        if asset.suffix.lower() == ".svg":
            root = ET.parse(asset).getroot()
            require(root.tag.endswith("svg") and "viewBox" in root.attrib, f"invalid NN SVG: {target}")
        for link in wiki_targets(content, embeds=False):
            if link.endswith(".py") and "plot_" in link:
                scripts.add(Path(link).name)
    require(embed_count == len(assets) == 64, f"NN node figure inventory changed: embeds={embed_count}, assets={len(assets)}")
    require(scripts == EXPECTED_FIGURE_SCRIPTS, f"NN figure script set changed: {sorted(scripts)}")
    for script in scripts:
        require((CODE / script).is_file(), f"missing NN figure script: {script}")

    result = subprocess.run(["node", str(FIGURE_AUDITOR), str(ROOT), "--json"], cwd=ROOT, text=True, capture_output=True)
    require(result.returncode == 0, f"figure-unit auditor failed:\n{result.stderr}")
    payload = json.loads(result.stdout)
    records = [record for record in payload["records"] if record["file"].startswith("30-神经网络基础/")]
    require(len(records) == 64 and all(record["pass"] for record in records), f"NN figure-unit contract changed: {records}")
    print("PASS NN figures: node embeds/assets=64/64; chapter figure units=64/64; SVG/XML=64; scripts=16")


def audit_curriculum(nodes: list[tuple[int, Path, str]]) -> None:
    curriculum = read(CHAPTER / "神经网络基础完整课程地图与掌握标准.md")
    mapped = {int(node_id): title for node_id, title in re.findall(r"^\| NN-(\d{2}) \| \[\[([^\]|]+)", curriculum, re.M)}
    require(sorted(mapped) == list(range(1, 65)), "NN curriculum does not map NN-01--64 exactly once")
    for node_id, path, _ in nodes:
        require(mapped[node_id] == path.stem, f"NN curriculum/path mismatch: NN-{node_id:02d}")
    print("PASS NN curriculum: 64/64 ID-title-path mappings; eight-volume scope fixed")


def snapshot_assets() -> dict[str, str]:
    require(ASSET_DIR.is_dir(), "NN figure asset directory missing")
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(ASSET_DIR.rglob("*")) if path.is_file()
    }


def run_figure_scripts() -> None:
    for name in sorted(EXPECTED_FIGURE_SCRIPTS):
        result = subprocess.run([sys.executable, str(CODE / name)], cwd=ROOT, text=True, capture_output=True)
        require(result.returncode == 0, f"NN figure script failed: {name}\n{result.stdout}\n{result.stderr}")


def audit_deterministic_figures() -> None:
    before = snapshot_assets()
    run_figure_scripts()
    first = snapshot_assets()
    run_figure_scripts()
    second = snapshot_assets()
    require(before == first == second, "NN stored figures differ from deterministic double regeneration")
    require(len(before) == 64, f"NN stored figure count changed: {len(before)}")
    print("PASS NN deterministic figures: scripts=16; stored assets=64; double-run byte identity")


def audit_state_surfaces() -> None:
    audit_name = Path(__file__).name
    for path in STATE_SURFACES:
        content = read(path)
        require(audit_name in content, f"state surface misses NN audit: {path.relative_to(ROOT)}")
        require("16/64" in content or "16 / 64" in content, f"state surface misses NN migrated count: {path.relative_to(ROOT)}")
        require("48/64" in content or "48 / 64" in content, f"state surface misses NN pending count: {path.relative_to(ROOT)}")
        require("not-attempted" in content, f"state surface overclaims NN learner: {path.relative_to(ROOT)}")
    print("PASS NN state surfaces: 5 global + 2 volume views agree on migrated=16/64, pending=48/64, learner=not-attempted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-figures", action="store_true", help="Regenerate all 16 NN figure families twice.")
    args = parser.parse_args()
    nodes = collect_nodes()
    index = build_index()
    audit_scope(nodes)
    audit_migrated_contract(nodes)
    audit_wave_c_fixture(nodes)
    audit_wave_d_fixture(nodes)
    audit_exercises(nodes, index)
    audit_sources_and_links(nodes, index)
    audit_figures(nodes, index)
    audit_curriculum(nodes)
    audit_state_surfaces()
    if args.run_figures:
        audit_deterministic_figures()
    print("NN-01--16 teaching migration regression: PASS; 30.1--30.2 material gates=2/8")
    print("NN-17--64 teaching migration: pending (48/64)")
    print("PERSONAL LEARNING STATUS: not-attempted")


if __name__ == "__main__":
    main()
