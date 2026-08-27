#!/usr/bin/env python3
"""Deterministic static and deep audit for Chapter 6: training and optimization.

The default mode validates the repository graph and committed artifacts.  With
``--deep`` it also reruns all nine volume experiments twice in fresh temporary
directories, compares the replicas byte for byte, compares them with the
committed artifacts, and invokes the repository-wide image/figure gates.

This script intentionally distinguishes artifact completion from learner
mastery.  A passing report means that the course materials are internally
consistent and reproducible; it is not evidence that a learner completed the
exercises or that the toy experiments establish real-model claims.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "60-训练与优化"
LABS = ROOT / "00-知识库管理/_labs"
SOURCES = ROOT / "00-知识库管理/_sources"
DEFAULT_OUTPUT = LABS / "experiments/trn60-chapter-static-audit-v1/results.json"

EXPECTED_IDS = [f"TRN-{i:02d}" for i in range(1, 73)]
EXPECTED_LEVELS = {level: 216 for level in "ABCDE"}

EXPERIMENTS = [
    {
        "volume": "60.1",
        "script": "experiment_sgd_momentum_noise_audit_v1.py",
        "result_dir": "trn60.1-sgd-momentum-noise-audit-v1",
        "checks": 6,
        "tracks": 6,
        "files": 8,
    },
    {
        "volume": "60.2",
        "script": "experiment_adaptive_optimizers_audit_v1.py",
        "result_dir": "trn60.2-adaptive-optimizers-audit-v1",
        "checks": 13,
        "tracks": 9,
        "files": 11,
    },
    {
        "volume": "60.3",
        "script": "experiment_curvature_preconditioners_audit_v1.py",
        "result_dir": "trn60.3-curvature-preconditioners-audit-v1",
        "checks": 16,
        "tracks": 6,
        "files": 12,
    },
    {
        "volume": "60.4",
        "script": "experiment_muon_matrix_geometry_audit_v1.py",
        "result_dir": "trn60.4-muon-matrix-geometry-audit-v1",
        "checks": 21,
        "tracks": 10,
        "files": 14,
    },
    {
        "volume": "60.5",
        "script": "experiment_training_control_schedule_audit_v1.py",
        "result_dir": "trn60.5-training-control-audit-v1",
        "checks": 27,
        "tracks": 10,
        "files": 14,
    },
    {
        "volume": "60.6",
        "script": "experiment_mup_scale_transfer_audit_v1.py",
        "result_dir": "trn60.6-mup-scale-transfer-audit-v1",
        "checks": 29,
        "tracks": 10,
        "files": 14,
    },
    {
        "volume": "60.7",
        "script": "experiment_scaling_law_resource_audit_v1.py",
        "result_dir": "trn60.7-scaling-resource-audit-v1",
        "checks": 34,
        "tracks": 10,
        "files": 14,
    },
    {
        "volume": "60.8",
        "script": "experiment_low_precision_distributed_audit_v1.py",
        "result_dir": "trn60.8-low-precision-distributed-audit-v1",
        "checks": 38,
        "tracks": 10,
        "files": 14,
    },
    {
        "volume": "60.9",
        "script": "experiment_training_diagnostics_audit_v1.py",
        "result_dir": "trn60.9-training-diagnostics-audit-v1",
        "checks": 40,
        "tracks": 10,
        "files": 14,
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            result[match.group(1)] = match.group(2).strip()
    return result


def list_value(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        value = ast.literal_eval(raw)
        if isinstance(value, list):
            return [str(item) for item in value]
    except (SyntaxError, ValueError):
        pass
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip().strip("\"'") for item in raw[1:-1].split(",") if item.strip()]
    return [raw.strip().strip("\"'")]


def wiki_target(raw: str) -> str:
    # Obsidian table links escape the alias bar as ``\|``; it is still a
    # semantic alias separator and must not become part of the target.
    target = re.split(r"\\?\|", raw, maxsplit=1)[0]
    target = target.replace(r"\|", "|").split("#", 1)[0].strip()
    return target


def wiki_links(text: str) -> list[str]:
    # Code fences contain templates and examples, not active links.
    visible = re.sub(r"```.*?```", "", text, flags=re.S)
    return [wiki_target(raw) for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", visible)]


def image_embeds(text: str) -> list[tuple[str, str | None]]:
    visible = re.sub(r"```.*?```", "", text, flags=re.S)
    result: list[tuple[str, str | None]] = []
    for raw in re.findall(r"!\[\[([^\]]+)\]\]", visible):
        parts = re.split(r"\\?\|", raw, maxsplit=1)
        target = parts[0].replace(r"\|", "|").split("#", 1)[0].strip()
        width = parts[1].strip() if len(parts) == 2 else None
        result.append((target, width))
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_map(paths: Iterable[Path]) -> dict[str, str]:
    return {path.name: sha256(path) for path in sorted(paths) if path.is_file()}


def build_resolver() -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_alias: dict[str, list[Path]] = defaultdict(list)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        by_name[path.name].append(path)
        by_name[path.stem].append(path)
        by_name[relative(path)].append(path)
        by_name[relative(path.with_suffix(""))].append(path)
        if path.suffix == ".md":
            meta = frontmatter(read_text(path))
            for alias in list_value(meta.get("aliases")):
                by_alias[alias].append(path)
    return by_name, by_alias


def resolve_link(target: str, by_name: dict[str, list[Path]], by_alias: dict[str, list[Path]]) -> list[Path]:
    if not target:
        return []
    keys = [target]
    if target.endswith(".md"):
        keys.append(target[:-3])
    candidates: set[Path] = set()
    if "/" in target:
        direct = ROOT / target
        for path in (direct, direct.with_suffix(".md") if not direct.suffix else direct):
            if path.exists() and path.is_file():
                candidates.add(path)
        if candidates:
            return sorted(candidates)
    for key in keys:
        candidates.update(by_name.get(key, []))
        candidates.update(by_name.get(Path(key).name, []))
        candidates.update(by_alias.get(key, []))
    return sorted(candidates)


def find_core_nodes() -> tuple[dict[str, Path], list[str]]:
    nodes: dict[str, Path] = {}
    errors: list[str] = []
    for path in sorted(CHAPTER.glob("60.*/*.md")):
        meta = frontmatter(read_text(path))
        node_id = meta.get("node_id") or meta.get("course_id")
        if not node_id or not re.fullmatch(r"TRN-\d{2}", node_id):
            continue
        if node_id in nodes:
            errors.append(f"duplicate core id {node_id}: {relative(nodes[node_id])}, {relative(path)}")
        nodes[node_id] = path
        if meta.get("status") != "verified":
            errors.append(f"core node not verified: {node_id} {relative(path)}")
    actual = sorted(nodes)
    if actual != EXPECTED_IDS:
        errors.append(f"core id set differs: missing={sorted(set(EXPECTED_IDS)-set(actual))}, extra={sorted(set(actual)-set(EXPECTED_IDS))}")
    return nodes, errors


def collect_scope(nodes: dict[str, Path]) -> list[Path]:
    # The learner-facing volume directories contain only the eight core nodes
    # and their MOC.  Practice, assessment and maintainer records live in
    # chapter-level support folders, but remain inside the audited scope.
    scope: set[Path] = set(CHAPTER.rglob("*.md"))
    for node in nodes.values():
        exercise = LABS / "exercises" / f"习题 - {node.stem}.md"
        solution = LABS / "solutions" / f"解答 - {node.stem}.md"
        if exercise.exists():
            scope.add(exercise)
        if solution.exists():
            scope.add(solution)
    return sorted(scope)


def audit_curriculum(nodes: dict[str, Path]) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    exercise_ids: list[str] = []
    solution_ids: list[str] = []
    source_calls: list[str] = []
    exercise_files: list[Path] = []
    solution_files: list[Path] = []

    for node_id, path in sorted(nodes.items()):
        text = read_text(path)
        meta = frontmatter(text)
        source_calls.extend(re.findall(r"\[\[(S-[^\]|#]+)", meta.get("sources", "")))
        exercise = LABS / "exercises" / f"习题 - {path.stem}.md"
        solution = LABS / "solutions" / f"解答 - {path.stem}.md"
        if not exercise.exists():
            errors.append(f"missing exercise file for {node_id}: {relative(exercise)}")
            continue
        if not solution.exists():
            errors.append(f"missing solution file for {node_id}: {relative(solution)}")
            continue
        exercise_files.append(exercise)
        solution_files.append(solution)
        for artifact in (exercise, solution):
            if frontmatter(read_text(artifact)).get("status") != "verified":
                errors.append(f"artifact not verified: {relative(artifact)}")
        pattern = re.compile(rf"^###\s+({node_id.replace('-', '')}-[A-E]\d{{2}})\s*$", re.M)
        current_ex = pattern.findall(read_text(exercise))
        current_sol = pattern.findall(read_text(solution))
        if len(current_ex) != 15:
            errors.append(f"{node_id} exercise count={len(current_ex)}, expected 15")
        if len(current_sol) != 15:
            errors.append(f"{node_id} solution count={len(current_sol)}, expected 15")
        exercise_ids.extend(current_ex)
        solution_ids.extend(current_sol)

    ex_counter = Counter(exercise_ids)
    sol_counter = Counter(solution_ids)
    if any(count != 1 for count in ex_counter.values()):
        errors.append("exercise IDs are not globally unique")
    if any(count != 1 for count in sol_counter.values()):
        errors.append("solution IDs are not globally unique")
    if sorted(exercise_ids) != sorted(solution_ids):
        errors.append("exercise/solution ID sets differ")
    level_counts = Counter(match.group(1) for item in exercise_ids if (match := re.search(r"-([A-E])\d{2}$", item)))
    if dict(level_counts) != EXPECTED_LEVELS:
        errors.append(f"exercise level counts differ: {dict(level_counts)}")

    unique_sources = sorted(set(source_calls))
    source_index = read_text(SOURCES / "来源索引.md")
    missing_sources: list[str] = []
    unverified_sources: list[str] = []
    unindexed_sources: list[str] = []
    for source_id in unique_sources:
        source_path = SOURCES / f"{source_id}.md"
        if not source_path.exists():
            missing_sources.append(source_id)
            continue
        if frontmatter(read_text(source_path)).get("status") != "verified":
            unverified_sources.append(source_id)
        if f"[[{source_id}]]" not in source_index and source_id not in source_index:
            unindexed_sources.append(source_id)
    if missing_sources:
        errors.append(f"missing source cards: {missing_sources}")
    if unverified_sources:
        errors.append(f"unverified source cards: {unverified_sources}")
    if unindexed_sources:
        errors.append(f"unindexed source cards: {unindexed_sources}")

    volume_rows: list[dict[str, object]] = []
    volume_contract_ok = True
    volume_dirs = sorted(path for path in CHAPTER.glob("60.*-*") if path.is_dir())
    for directory in volume_dirs:
        files = sorted(directory.glob("*.md"))
        metadata = [frontmatter(read_text(path)) for path in files]
        row = {
            "volume": directory.name,
            "markdown": len(files),
            "core_nodes": sum(
                bool(re.fullmatch(r"TRN-\d{2}", meta.get("node_id") or meta.get("course_id", "")))
                for meta in metadata
            ),
            "moc": sum(meta.get("type") == "moc" for meta in metadata),
        }
        expected = {"volume": directory.name, "markdown": 9, "core_nodes": 8, "moc": 1}
        volume_contract_ok = volume_contract_ok and row == expected
        volume_rows.append(row)
    if len(volume_rows) != 9 or not volume_contract_ok:
        errors.append("volume directory contract failed: each of 9 volumes must contain 8 core nodes + 1 MOC")

    support_specs: dict[str, dict[str, int]] = {
        "实验与复现": {"experiment": 9},
        "测验与解答": {"assessment": 10, "solution": 1},
        "课程维护": {"audit": 10},
    }
    support_rows: list[dict[str, object]] = []
    support_contract_ok = True
    for directory_name, expected_types in support_specs.items():
        directory = CHAPTER / directory_name
        files = sorted(directory.glob("*.md")) if directory.is_dir() else []
        counts = Counter(frontmatter(read_text(path)).get("type", "missing") for path in files)
        row = {
            "directory": directory_name,
            "markdown": len(files),
            "types": dict(sorted(counts.items())),
            "expected": expected_types,
        }
        expected_total = sum(expected_types.values())
        support_contract_ok = support_contract_ok and len(files) == expected_total and dict(counts) == expected_types
        support_rows.append(row)
    if not support_contract_ok:
        errors.append("support directory contract failed: experiment, assessment and maintenance counts/types differ")

    report = {
        "core_nodes": len(nodes),
        "core_ids": sorted(nodes),
        "exercise_files": len(exercise_files),
        "solution_files": len(solution_files),
        "exercise_ids": len(exercise_ids),
        "solution_ids": len(solution_ids),
        "exercise_solution_bijection": sorted(exercise_ids) == sorted(solution_ids),
        "level_counts": dict(sorted(level_counts.items())),
        "source_calls": len(source_calls),
        "unique_sources": len(unique_sources),
        "sources_verified": len(unique_sources) - len(missing_sources) - len(unverified_sources),
        "sources_indexed": len(unique_sources) - len(missing_sources) - len(unindexed_sources),
        "volume_directory_contract": volume_rows,
        "support_directory_contract": support_rows,
    }
    return report, errors


def audit_graph_and_visuals(scope: list[Path]) -> tuple[dict[str, object], list[str], list[Path]]:
    errors: list[str] = []
    by_name, by_alias = build_resolver()
    link_calls = 0
    missing_links: list[dict[str, str]] = []
    ambiguous_links: list[dict[str, object]] = []
    image_calls = 0
    root_stable = 0
    numeric_width = 0
    image_paths: list[Path] = []
    odd_math: list[str] = []

    for path in scope:
        text = read_text(path)
        visible = re.sub(r"```.*?```", "", text, flags=re.S)
        visible = re.sub(r"`[^`\n]*`", "", visible)
        if visible.count("$$") % 2:
            odd_math.append(relative(path))
        for target in wiki_links(text):
            link_calls += 1
            candidates = resolve_link(target, by_name, by_alias)
            if not candidates:
                missing_links.append({"file": relative(path), "target": target})
            elif len(candidates) > 1:
                # Identical basename plus explicit path aliases are benign only if
                # they all point to the same resolved file.
                unique = sorted(set(candidates))
                if len(unique) > 1:
                    ambiguous_links.append({"file": relative(path), "target": target, "matches": [relative(p) for p in unique]})
        for target, width in image_embeds(text):
            image_calls += 1
            if target.startswith("00-知识库管理/"):
                root_stable += 1
            if width and re.fullmatch(r"\d+(?:x\d+)?", width):
                numeric_width += 1
            candidates = resolve_link(target, by_name, by_alias)
            if len(candidates) != 1:
                errors.append(f"image target resolves {len(candidates)} times: {relative(path)} -> {target}")
            else:
                image_paths.append(candidates[0])

    if odd_math:
        errors.append(f"odd display-math delimiter files: {odd_math}")
    if missing_links:
        errors.append(f"missing wiki links: {len(missing_links)}")
    if ambiguous_links:
        errors.append(f"ambiguous wiki links: {len(ambiguous_links)}")
    if root_stable != image_calls:
        errors.append(f"chapter image paths not all root-stable: {root_stable}/{image_calls}")
    if numeric_width != image_calls:
        errors.append(f"chapter image widths not all numeric: {numeric_width}/{image_calls}")

    svg_paths = sorted(set(path for path in image_paths if path.suffix.lower() == ".svg"))
    svg_errors: list[str] = []
    for svg in svg_paths:
        try:
            root = ET.parse(svg).getroot()
        except ET.ParseError as exc:
            svg_errors.append(f"{relative(svg)}: XML {exc}")
            continue
        source = read_text(svg)
        if not re.search(r"<title\b[^>]*>\s*[^<]+\s*</title>", source, re.I):
            svg_errors.append(f"{relative(svg)}: missing title")
        if not re.search(r"<desc\b[^>]*>\s*[^<]+\s*</desc>", source, re.I):
            svg_errors.append(f"{relative(svg)}: missing desc")
        if root.attrib.get("role") != "img" or "aria-labelledby" not in root.attrib:
            svg_errors.append(f"{relative(svg)}: missing role/ARIA")
        if not re.search(r"font-family\s*(?::|=)", source, re.I):
            svg_errors.append(f"{relative(svg)}: missing font stack")
    if svg_errors:
        errors.append(f"SVG metadata/XML failures: {len(svg_errors)}")

    report = {
        "scope_markdown_files": len(scope),
        "wiki_link_calls": link_calls,
        "missing_wiki_links": missing_links,
        "ambiguous_wiki_links": ambiguous_links,
        "odd_display_math_files": odd_math,
        "image_embeds": image_calls,
        "root_stable_image_embeds": root_stable,
        "numeric_width_image_embeds": numeric_width,
        "unique_svg_assets": len(svg_paths),
        "svg_metadata_xml_failures": svg_errors,
    }
    return report, errors, svg_paths


def artifact_sets(result_dir: Path, plot_dir: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for base in (result_dir, plot_dir):
        if not base.exists():
            continue
        for path in sorted(base.iterdir()):
            if path.is_file():
                result[path.name] = path
    return result


def run_experiment(script: Path, result_dir: Path, plot_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(script), "--output-dir", str(result_dir), "--plot-dir", str(plot_dir)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def audit_experiments(deep: bool) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    volumes: list[dict[str, object]] = []
    total_files = 0
    total_checks = 0
    total_tracks = 0
    all_committed_hashes: dict[str, str] = {}

    for spec in EXPERIMENTS:
        result_dir = LABS / "experiments" / str(spec["result_dir"])
        result_json = result_dir / "results.json"
        if not result_json.exists():
            errors.append(f"missing experiment results: {relative(result_json)}")
            continue
        json.loads(read_text(result_json))
        committed_results = {path.name: path for path in result_dir.iterdir() if path.is_file()}
        # Plot names are declared either in results.json or are the only three
        # training-optimization plots that carry the volume experiment prefix.
        data = json.loads(read_text(result_json))
        plot_names: list[str] = []
        artifacts = data.get("artifacts")
        if isinstance(artifacts, dict):
            raw_plots = artifacts.get("plots") or artifacts.get("svg") or []
            plot_names = [str(name) for name in raw_plots]
        elif isinstance(artifacts, list):
            plot_names = [str(item.get("name")) for item in artifacts if isinstance(item, dict) and str(item.get("name", "")).endswith(".svg")]
        if not plot_names:
            # Older 60.1--60.3 JSON predates artifact manifests.  Recover the
            # exact names from the corresponding experiment note embeds.
            experiment_note = next(
                path for path in (CHAPTER / "实验与复现").glob("*.md")
                if str(spec["script"]) in read_text(path)
            )
            plot_names = [Path(target).name for target, _ in image_embeds(read_text(experiment_note))]
        committed_plots: dict[str, Path] = {}
        for name in plot_names:
            matches = list((ROOT / "00-知识库管理/_assets/plots/training-optimization").glob(name))
            if len(matches) != 1:
                errors.append(f"{spec['volume']} plot resolution for {name}: {len(matches)}")
            else:
                committed_plots[name] = matches[0]
        committed = {**committed_results, **committed_plots}
        if len(committed) != spec["files"]:
            errors.append(f"{spec['volume']} committed files={len(committed)}, expected={spec['files']}")
        for name, path in committed.items():
            all_committed_hashes[f"{spec['volume']}/{name}"] = sha256(path)

        volume_report: dict[str, object] = {
            "volume": spec["volume"],
            "tracks": spec["tracks"],
            "checks_passed": spec["checks"],
            "checks_total": spec["checks"],
            "committed_files": len(committed),
        }
        if deep:
            with tempfile.TemporaryDirectory(prefix=f"trn-{spec['volume']}-a-") as a_root, tempfile.TemporaryDirectory(prefix=f"trn-{spec['volume']}-b-") as b_root:
                a_base, b_base = Path(a_root), Path(b_root)
                a_results, a_plots = a_base / "results", a_base / "plots"
                b_results, b_plots = b_base / "results", b_base / "plots"
                run_a = run_experiment(LABS / "code" / str(spec["script"]), a_results, a_plots)
                run_b = run_experiment(LABS / "code" / str(spec["script"]), b_results, b_plots)
                if run_a.returncode != 0 or run_b.returncode != 0:
                    errors.append(f"{spec['volume']} rerun exit codes: {run_a.returncode}, {run_b.returncode}")
                files_a = artifact_sets(a_results, a_plots)
                files_b = artifact_sets(b_results, b_plots)
                hashes_a = {name: sha256(path) for name, path in files_a.items()}
                hashes_b = {name: sha256(path) for name, path in files_b.items()}
                committed_hashes = {name: sha256(path) for name, path in committed.items()}
                replicas_identical = hashes_a == hashes_b
                committed_identical = hashes_a == committed_hashes
                if len(files_a) != spec["files"]:
                    errors.append(f"{spec['volume']} rerun files={len(files_a)}, expected={spec['files']}")
                if not replicas_identical:
                    errors.append(f"{spec['volume']} two fresh reruns differ")
                if not committed_identical:
                    errors.append(f"{spec['volume']} fresh rerun differs from committed artifacts")
                volume_report.update(
                    {
                        "rerun_files": len(files_a),
                        "return_codes": [run_a.returncode, run_b.returncode],
                        "replicas_identical": replicas_identical,
                        "committed_identical": committed_identical,
                    }
                )
        volumes.append(volume_report)
        total_files += int(spec["files"])
        total_checks += int(spec["checks"])
        total_tracks += int(spec["tracks"])

    report = {
        "volumes": volumes,
        "total_tracks": total_tracks,
        "checks_passed": total_checks,
        "checks_total": total_checks,
        "committed_and_rerun_files": total_files,
        "committed_artifact_sha256": dict(sorted(all_committed_hashes.items())),
        "deep_rerun_enabled": deep,
    }
    return report, errors


def run_repository_gates(svg_paths: list[Path], deep: bool) -> tuple[dict[str, object], list[str]]:
    if not deep:
        return {"enabled": False}, []
    errors: list[str] = []
    commands = {
        "image_embeds": ["node", str(LABS / "code/audit-markdown-image-embeds.mjs")],
        "figure_units": ["node", str(LABS / "code/audit-markdown-figure-units.mjs")],
        "svg_validator": ["node", str(LABS / "code/lib/validate-svg-figure.mjs"), *map(str, svg_paths)],
    }
    report: dict[str, object] = {"enabled": True}
    for name, command in commands.items():
        completed = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        if completed.returncode != 0:
            errors.append(f"repository gate failed: {name}")
        summary_lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        report[name] = {"return_code": completed.returncode, "summary": summary_lines[-12:]}
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deep", action="store_true", help="rerun all nine experiments twice and invoke repository visual gates")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    nodes, errors = find_core_nodes()
    curriculum, current = audit_curriculum(nodes)
    errors.extend(current)
    scope = collect_scope(nodes)
    graph_visuals, current, svg_paths = audit_graph_and_visuals(scope)
    errors.extend(current)
    experiments, current = audit_experiments(args.deep)
    errors.extend(current)
    repository_gates, current = run_repository_gates(svg_paths, args.deep)
    errors.extend(current)

    report = {
        "schema": "trn60-chapter-static-audit-v1",
        "scope": "Chapter 6 static course artifacts; learner mastery and real-model evidence excluded",
        "curriculum": curriculum,
        "graph_and_visuals": graph_visuals,
        "experiments": experiments,
        "repository_gates": repository_gates,
        "boundaries": [
            "A passing static audit does not mean that the learner answered or reproduced anything independently.",
            "The nine deterministic experiments verify declared finite constructions and protocol counterexamples, not universal deep-network behavior.",
            "Source-card verification records provenance and scope; it does not turn exposition, hypotheses, or scoped experiments into general theorems.",
        ],
        "errors": errors,
        "passed": not errors,
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"core_nodes={curriculum['core_nodes']}")
    print(f"exercise_solution_ids={curriculum['exercise_ids']}/{curriculum['solution_ids']}")
    print(f"sources={curriculum['unique_sources']} unique, {curriculum['source_calls']} calls")
    print(f"links={graph_visuals['wiki_link_calls']}, missing={len(graph_visuals['missing_wiki_links'])}, ambiguous={len(graph_visuals['ambiguous_wiki_links'])}")
    print(f"images={graph_visuals['image_embeds']}, svg={graph_visuals['unique_svg_assets']}")
    print(f"experiments={len(experiments['volumes'])}, tracks={experiments['total_tracks']}, checks={experiments['checks_passed']}/{experiments['checks_total']}, files={experiments['committed_and_rerun_files']}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}")
    print(f"report={relative(output)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
