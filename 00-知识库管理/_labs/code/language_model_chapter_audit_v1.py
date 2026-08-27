#!/usr/bin/env python3
"""Static and reproducibility audit for chapter 7 (LM-01--LM-72)."""

from __future__ import annotations

from xml.etree import ElementTree as ET
import json
from pathlib import Path
import re
import shutil
import subprocess


VAULT = Path(__file__).resolve().parents[3]
CHAPTER = VAULT / "70-语言模型"
SOURCE_DIR = VAULT / "00-知识库管理" / "_sources"
EXERCISE_DIR = VAULT / "00-知识库管理" / "_labs" / "exercises"
SOLUTION_DIR = VAULT / "00-知识库管理" / "_labs" / "solutions"
OUT = VAULT / "00-知识库管理" / "_labs" / "experiments" / "lm70-chapter-audit-v1"
FIGURE_AUDITOR = VAULT / "00-知识库管理" / "_labs" / "code" / "audit-markdown-figure-units.mjs"

EXPERIMENT_DIRS = [
    "lm70.1-tokenization-audit-v1",
    "lm70.2-language-objectives-audit-v1",
    "lm70.3-pretraining-data-audit-v1",
    "lm70.4-instruction-adaptation-audit-v1",
    "lm70.5-icl-reasoning-audit-v1",
    "lm70.6-rag-audit-v1",
    "lm70.7-decoding-serving-v1",
    "lm70.8-evaluation-v1",
    "lm70.9-safety-deployment-v1",
]


def check(name: str, passed: bool, observed: object, expected: object, note: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "observed": observed,
        "expected": expected,
        "note": note,
    }


def frontmatter_status(text: str) -> str:
    match = re.search(r"^status:\s*(\S+)", text, re.M)
    return match.group(1) if match else ""


def source_calls(node_text: str) -> set[str]:
    match = re.search(r"^sources:\s*\[(.*?)\]$", node_text, re.M)
    return set(re.findall(r"\[\[([^\]]+)\]\]", match.group(1))) if match else set()


def wiki_targets(text: str) -> list[str]:
    targets = []
    for inner in re.findall(r"\[\[([^\]\n]+)\]\]", text):
        if "\\|" in inner:
            inner = inner.split("\\|", 1)[0]
        else:
            inner = inner.split("|", 1)[0]
        target = inner.split("#", 1)[0].strip().rstrip("\\")
        if target:
            targets.append(target)
    return targets


def experiment_ok(path: Path) -> tuple[bool, int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    checks = data.get("checks")
    if isinstance(checks, dict):
        values = [bool(value) for value in checks.values()]
        return all(values), sum(values), len(values)
    if isinstance(checks, list):
        values = [bool(row.get("passed")) for row in checks]
        status = data.get("status", "passed") == "passed"
        return status and all(values), sum(values), len(values)
    if "passed" in data and "total" in data:
        return data["passed"] == data["total"], int(data["passed"]), int(data["total"])
    return False, 0, 0


def node_runtime() -> str:
    found = shutil.which("node")
    if found:
        return found
    fallback = Path("/Users/tong/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node")
    if fallback.exists():
        return str(fallback)
    raise RuntimeError("node runtime not found")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, object]] = []
    markdown = sorted(CHAPTER.rglob("*.md"))
    nodes: list[tuple[int, Path, str]] = []
    all_sources: set[str] = set()

    for path in markdown:
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^node_id:\s*LM-(\d+)", text, re.M)
        if match:
            node_id = int(match.group(1))
            nodes.append((node_id, path, text))
            all_sources.update(source_calls(text))

    ids = sorted(node_id for node_id, _, _ in nodes)
    node_status_bad = [
        str(path.relative_to(VAULT))
        for _, path, text in nodes
        if frontmatter_status(text) != "verified"
    ]
    checks.append(check(
        "node_ids_and_status",
        ids == list(range(1, 73)) and len(nodes) == 72 and not node_status_bad,
        {"nodes": len(nodes), "ids": [min(ids), max(ids)], "unique": len(set(ids)), "status_bad": node_status_bad},
        {"nodes": 72, "ids": [1, 72], "unique": 72, "status_bad": []},
        "LM-01--LM-72 must be unique, contiguous and verified.",
    ))

    volume_rows = []
    volume_ok = True
    volume_dirs = sorted(
        path for path in CHAPTER.iterdir()
        if path.is_dir() and re.fullmatch(r"70\.\d-.*", path.name)
    )
    for directory in volume_dirs:
        texts = [(path, path.read_text(encoding="utf-8")) for path in directory.glob("*.md")]
        row = {
            "volume": directory.name,
            "markdown": len(texts),
            "nodes": sum("node_id: LM-" in text for _, text in texts),
            "moc": sum(re.search(r"^type:\s*moc$", text, re.M) is not None for _, text in texts),
        }
        expected = {
            "volume": directory.name, "markdown": 9, "nodes": 8, "moc": 1,
        }
        volume_ok = volume_ok and row == expected
        volume_rows.append(row)
    checks.append(check(
        "nine_volume_core_contract",
        len(volume_rows) == 9 and volume_ok,
        volume_rows,
        "Each of 9 volumes keeps 8 core nodes + 1 MOC at the learning-path level.",
        "Experiments, assessments and maintenance audits are checked in dedicated support folders.",
    ))

    support_specs = {
        "实验与复现": ("experiment", 9),
        "测验与解答": ("assessment", 10),
        "课程维护": ("audit", 10),
    }
    support_rows = []
    support_ok = True
    for directory_name, (expected_type, expected_count) in support_specs.items():
        directory = CHAPTER / directory_name
        files = sorted(directory.glob("*.md")) if directory.is_dir() else []
        typed = [
            path for path in files
            if re.search(
                rf"^type:\s*{re.escape(expected_type)}$",
                path.read_text(encoding="utf-8"),
                re.M,
            )
        ]
        row = {
            "directory": directory_name,
            "type": expected_type,
            "markdown": len(files),
            "typed": len(typed),
            "expected": expected_count,
        }
        support_ok = support_ok and len(files) == len(typed) == expected_count
        support_rows.append(row)
    checks.append(check(
        "chapter_support_material_contract",
        support_ok,
        support_rows,
        support_specs,
        "Support materials remain complete but no longer compete visually with the core learning path.",
    ))

    exercise_ids: list[str] = []
    solution_ids: list[str] = []
    pattern = re.compile(r"^### (LM\d{2}-[A-E]\d{2})$", re.M)
    for path in EXERCISE_DIR.glob("习题 - *.md"):
        exercise_ids.extend(pattern.findall(path.read_text(encoding="utf-8")))
    for path in SOLUTION_DIR.glob("解答 - *.md"):
        solution_ids.extend(pattern.findall(path.read_text(encoding="utf-8")))
    expected_ids = {
        f"LM{node:02d}-{level}{number:02d}"
        for node in range(1, 73)
        for level in "ABCDE"
        for number in range(1, 4)
    }
    qa_ok = (
        len(exercise_ids) == len(set(exercise_ids)) == 1080
        and len(solution_ids) == len(set(solution_ids)) == 1080
        and set(exercise_ids) == set(solution_ids) == expected_ids
    )
    checks.append(check(
        "exercise_solution_bijection",
        qa_ok,
        {
            "exercise": len(exercise_ids), "exercise_unique": len(set(exercise_ids)),
            "solution": len(solution_ids), "solution_unique": len(set(solution_ids)),
            "bijection": set(exercise_ids) == set(solution_ids),
        },
        {"exercise": 1080, "solution": 1080, "unique": True, "bijection": True},
        "Every node has A--E x 3 questions and a same-ID solution.",
    ))

    source_bad = []
    for stem in sorted(all_sources):
        path = SOURCE_DIR / f"{stem}.md"
        if not path.exists():
            source_bad.append({"source": stem, "status": "missing"})
            continue
        status = frontmatter_status(path.read_text(encoding="utf-8"))
        if status != "verified":
            source_bad.append({"source": stem, "status": status or "missing-status"})
    checks.append(check(
        "source_cards_verified",
        len(all_sources) > 0 and not source_bad,
        {"unique_sources": len(all_sources), "bad": source_bad},
        {"unique_sources": len(all_sources), "bad": []},
        "Only actually called node sources are counted.",
    ))

    embeds = []
    for path in markdown:
        for target, width in re.findall(
            r"!\[\[([^\]|]+)(?:\|(\d+))?\]\]",
            path.read_text(encoding="utf-8"),
        ):
            embeds.append((path, target, width))
    image_bad = []
    for source, target, width in embeds:
        asset = VAULT / target
        if not asset.exists():
            image_bad.append({"file": str(source.relative_to(VAULT)), "target": target, "error": "missing"})
            continue
        if not width:
            image_bad.append({"file": str(source.relative_to(VAULT)), "target": target, "error": "width"})
        if asset.suffix.lower() == ".svg":
            try:
                ET.parse(asset)
            except Exception as exc:
                image_bad.append({"file": str(source.relative_to(VAULT)), "target": target, "error": str(exc)})
    checks.append(check(
        "image_embeds_and_svg",
        len(embeds) >= 99 and not image_bad,
        {"embeds": len(embeds), "unique_targets": len({target for _, target, _ in embeds}), "bad": image_bad},
        {"minimum_embeds": 99, "bad": []},
        "All chapter figures use rooted paths, numeric widths and parseable SVG/XML.",
    ))

    audit_result = subprocess.run(
        [node_runtime(), str(FIGURE_AUDITOR), str(VAULT), "--json"],
        check=True, capture_output=True, text=True,
    )
    figure_records = [
        row for row in json.loads(audit_result.stdout)["records"]
        if str(row["file"]).startswith("70-语言模型/")
    ]
    figure_bad = [
        {
            "file": row["file"], "line": row["line"], "target": row["target"],
            "missing": [name for name, passed in row["checks"].items() if not passed],
        }
        for row in figure_records if not row["pass"]
    ]
    checks.append(check(
        "strict_figure_units",
        len(figure_records) == len(embeds) and not figure_bad,
        {"records": len(figure_records), "bad": figure_bad},
        {"records": len(embeds), "bad": []},
        "Question to image to provenance to read-back to explicit boundary.",
    ))

    all_files = [path for path in VAULT.rglob("*") if path.is_file()]
    names = {path.name for path in all_files}
    stems = {path.stem for path in all_files}
    relatives = {str(path.relative_to(VAULT)) for path in all_files}
    relative_without_md = {value[:-3] if value.endswith(".md") else value for value in relatives}
    unresolved = []
    wiki_count = 0
    for path in markdown:
        for target in wiki_targets(path.read_text(encoding="utf-8")):
            wiki_count += 1
            ok = (
                target in relatives or target in relative_without_md
                if "/" in target else target in names or target in stems
            )
            if not ok:
                unresolved.append({"file": str(path.relative_to(VAULT)), "target": target})
    checks.append(check(
        "internal_links_resolved",
        not unresolved,
        {"wiki_links": wiki_count, "unresolved": unresolved},
        {"unresolved": []},
        "Bare links resolve by filename/stem; rooted links resolve from the vault root.",
    ))

    experiment_rows = []
    experiments_ok = True
    for directory in EXPERIMENT_DIRS:
        path = VAULT / "00-知识库管理" / "_labs" / "experiments" / directory / "results.json"
        if not path.exists():
            row = {"experiment": directory, "passed": False, "checks": "missing"}
            experiments_ok = False
        else:
            passed, count, total = experiment_ok(path)
            row = {"experiment": directory, "passed": passed, "checks": f"{count}/{total}"}
            experiments_ok = experiments_ok and passed and total == 9
        experiment_rows.append(row)
    checks.append(check(
        "nine_experiments_passed",
        len(experiment_rows) == 9 and experiments_ok,
        experiment_rows,
        "Nine deterministic experiments, each with 9/9 checks.",
        "The audit reads results produced by scripts rerun in the same handoff.",
    ))

    delimiter_bad = []
    control_bad = []
    fence_pattern = re.compile(f"^\\s*({chr(96)}{{3,}}|~{{3,}})")
    for path in markdown:
        text_value = path.read_text(encoding="utf-8")
        if text_value.count("$$") % 2:
            delimiter_bad.append({"file": str(path.relative_to(VAULT)), "delimiter": "$$"})
        fence = None
        for line_number, line in enumerate(text_value.splitlines(), start=1):
            match = fence_pattern.match(line)
            if match:
                char = match.group(1)[0]
                if fence is None:
                    fence = char
                elif fence == char:
                    fence = None
            for character in line:
                if ord(character) < 32 and character != "\t":
                    control_bad.append({"file": str(path.relative_to(VAULT)), "line": line_number, "code": ord(character)})
        if fence is not None:
            delimiter_bad.append({"file": str(path.relative_to(VAULT)), "delimiter": "fence"})
    checks.append(check(
        "markdown_delimiters_and_controls",
        not delimiter_bad and not control_bad,
        {"delimiter_bad": delimiter_bad, "control_bad": control_bad},
        {"delimiter_bad": [], "control_bad": []},
        "Block math and Markdown fences are balanced; no embedded control bytes.",
    ))

    results = {
        "audit_id": "lm70-chapter-audit-v1",
        "status": "passed" if all(row["passed"] for row in checks) else "failed",
        "checks_passed": sum(bool(row["passed"]) for row in checks),
        "checks_total": len(checks),
        "summary": {
            "chapter_markdown": len(markdown),
            "nodes": len(nodes),
            "questions": len(exercise_ids),
            "solutions": len(solution_ids),
            "unique_sources": len(all_sources),
            "image_embeds": len(embeds),
            "strict_figure_units": len(figure_records),
            "experiments": len(experiment_rows),
        },
        "checks": checks,
    }
    (OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(
        {
            "status": results["status"],
            "checks": f'{results["checks_passed"]}/{results["checks_total"]}',
            "summary": results["summary"],
            "output": str(OUT),
        },
        ensure_ascii=False,
    ))
    if results["status"] != "passed":
        raise SystemExit("chapter audit failed; inspect results.json")


if __name__ == "__main__":
    main()
