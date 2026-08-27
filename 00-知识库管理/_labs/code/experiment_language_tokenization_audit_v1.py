#!/usr/bin/env python3
"""Deterministic standard-library audit for LM-01--LM-08.

The script checks Unicode normalization, BPE tie/rank semantics, WordPiece
greedy dead ends, Unigram marginal/Viterbi/sampling, and byte round trips. It
emits JSON, CSV and three self-contained SVG plots.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import random
import unicodedata
from collections import Counter
from pathlib import Path


SEED = 20260826
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "_labs" / "experiments" / "lm70.1-tokenization-audit-v1"
DEFAULT_PLOTS = ROOT / "_assets" / "plots" / "language-models"


def cps(s: str) -> list[str]:
    return [f"U+{ord(ch):04X}" for ch in s]


def audit_unicode() -> dict:
    samples = {
        "precomposed_e_acute": "é",
        "decomposed_e_acute": "e\u0301",
        "circled_one": "①",
        "fullwidth_A": "Ａ",
    }
    rows = []
    for name, value in samples.items():
        for form in ("identity", "NFC", "NFD", "NFKC", "NFKD"):
            normalized = value if form == "identity" else unicodedata.normalize(form, value)
            rows.append({
                "sample": name,
                "form": form,
                "text": normalized,
                "codepoints": cps(normalized),
                "codepoint_count": len(normalized),
                "utf8_bytes": len(normalized.encode("utf-8")),
            })
    return {
        "python_unicodedata_version": unicodedata.unidata_version,
        "rows": rows,
        "nfc_equivalent": unicodedata.normalize("NFC", samples["precomposed_e_acute"]) == unicodedata.normalize("NFC", samples["decomposed_e_acute"]),
        "nfkc_circled_one": unicodedata.normalize("NFKC", samples["circled_one"]),
        "nfkc_fullwidth_A": unicodedata.normalize("NFKC", samples["fullwidth_A"]),
        "idempotent": all(
            unicodedata.normalize(form, unicodedata.normalize(form, value)) == unicodedata.normalize(form, value)
            for form in ("NFC", "NFD", "NFKC", "NFKD")
            for value in samples.values()
        ),
    }


def nonoverlap_merge(seq: tuple[str, ...], pair: tuple[str, str]) -> tuple[str, ...]:
    out: list[str] = []
    i = 0
    while i < len(seq):
        if i + 1 < len(seq) and (seq[i], seq[i + 1]) == pair:
            out.append(seq[i] + seq[i + 1])
            i += 2
        else:
            out.append(seq[i])
            i += 1
    return tuple(out)


def pair_counts(corpus: dict[tuple[str, ...], int]) -> Counter:
    counts: Counter = Counter()
    for seq, frequency in corpus.items():
        for i in range(len(seq) - 1):
            counts[(seq[i], seq[i + 1])] += frequency
    return counts


def train_bpe(corpus: dict[tuple[str, ...], int], steps: int) -> tuple[list[tuple[str, str]], list[dict]]:
    state = dict(corpus)
    merges: list[tuple[str, str]] = []
    history = []
    for rank in range(steps):
        counts = pair_counts(state)
        if not counts:
            break
        maximum = max(counts.values())
        ties = sorted(pair for pair, count in counts.items() if count == maximum)
        chosen = ties[0]  # explicit lexical tie break
        history.append({
            "rank": rank,
            "chosen": list(chosen),
            "frequency": maximum,
            "ties": [list(pair) for pair in ties],
        })
        merges.append(chosen)
        new_state: dict[tuple[str, ...], int] = {}
        for seq, frequency in state.items():
            merged = nonoverlap_merge(seq, chosen)
            new_state[merged] = new_state.get(merged, 0) + frequency
        state = new_state
    return merges, history


def encode_bpe(text: str, merges: list[tuple[str, str]]) -> list[str]:
    seq = tuple(text)
    for pair in merges:
        seq = nonoverlap_merge(seq, pair)
    return list(seq)


def audit_bpe() -> dict:
    corpus = {
        tuple("low_"): 5,
        tuple("lower_"): 2,
        tuple("newest_"): 6,
    }
    merges, history = train_bpe(corpus, 8)
    rank_bc_first = encode_bpe("abc", [("b", "c"), ("a", "b")])
    rank_ab_first = encode_bpe("abc", [("a", "b"), ("b", "c")])
    overlap = list(nonoverlap_merge(tuple("aaaa"), ("a", "a")))
    return {
        "tie_break": "lexicographically smallest pair",
        "merges": [list(pair) for pair in merges],
        "history": history,
        "rank_counterexample": {
            "bc_first": rank_bc_first,
            "ab_first": rank_ab_first,
        },
        "overlap_aaaa": overlap,
    }


def wp_piece(text: str, start: int, end: int) -> str:
    raw = text[start:end]
    return raw if start == 0 else "##" + raw


def wordpiece_greedy(text: str, vocab: set[str]) -> list[str] | None:
    i = 0
    pieces: list[str] = []
    while i < len(text):
        found = None
        for j in range(len(text), i, -1):
            candidate = wp_piece(text, i, j)
            if candidate in vocab:
                found = (j, candidate)
                break
        if found is None:
            return None
        i, candidate = found
        pieces.append(candidate)
    return pieces


def wordpiece_dp(text: str, vocab: set[str]) -> list[str] | None:
    best: list[list[str] | None] = [None] * (len(text) + 1)
    best[0] = []
    for i in range(len(text)):
        if best[i] is None:
            continue
        for j in range(i + 1, len(text) + 1):
            candidate = wp_piece(text, i, j)
            if candidate not in vocab:
                continue
            proposal = best[i] + [candidate]
            if best[j] is None or len(proposal) < len(best[j]):
                best[j] = proposal
    return best[-1]


def audit_wordpiece() -> dict:
    vocab = {"a", "ab", "##bc"}
    return {
        "text": "abc",
        "vocab": sorted(vocab),
        "greedy": wordpiece_greedy("abc", vocab),
        "global_min_piece_path": wordpiece_dp("abc", vocab),
        "playing": wordpiece_greedy("playing", {"play", "player", "##er", "##ing"}),
        "player": wordpiece_greedy("player", {"play", "player", "##er", "##ing"}),
    }


def segmentations(text: str, probs: dict[str, float]) -> list[list[str]]:
    out: list[list[str]] = []

    def visit(index: int, path: list[str]) -> None:
        if index == len(text):
            out.append(list(path))
            return
        for token in sorted(probs):
            if text.startswith(token, index):
                path.append(token)
                visit(index + len(token), path)
                path.pop()

    visit(0, [])
    return out


def path_probability(path: list[str], probs: dict[str, float]) -> float:
    value = 1.0
    for token in path:
        value *= probs[token]
    return value


def audit_unigram(rng: random.Random, draws: int) -> dict:
    probs = {"a": 0.4, "b": 0.3, "ab": 0.2, "x": 0.1}
    paths = segmentations("ab", probs)
    raw = [path_probability(path, probs) for path in paths]
    marginal = sum(raw)
    posterior = [value / marginal for value in raw]
    alpha = 0.5
    weights = [value ** alpha for value in raw]
    total = sum(weights)
    sampling_probs = [weight / total for weight in weights]
    counts = [0] * len(paths)
    for _ in range(draws):
        u = rng.random()
        cumulative = 0.0
        for index, probability in enumerate(sampling_probs):
            cumulative += probability
            if u <= cumulative:
                counts[index] += 1
                break
    rows = []
    for path, value, post, target, count in zip(paths, raw, posterior, sampling_probs, counts):
        rows.append({
            "path": path,
            "path_probability": value,
            "posterior_alpha_1": post,
            "target_alpha_0_5": target,
            "empirical_alpha_0_5": count / draws,
            "absolute_error": abs(count / draws - target),
        })
    return {
        "piece_probs": probs,
        "marginal": marginal,
        "map_path": paths[max(range(len(paths)), key=lambda i: raw[i])],
        "alpha": alpha,
        "draws": draws,
        "rows": rows,
    }


def audit_byte_roundtrip(rng: random.Random, trials: int = 1000) -> dict:
    for _ in range(trials):
        value = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 65)))
        tokens = list(value)
        decoded = bytes(tokens)
        if decoded != value:
            return {"trials": trials, "passed": False}
    return {"trials": trials, "passed": True}


STYLE = '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",sans-serif}.mono{font-family:"SFMono-Regular",Menlo,monospace}</style>'


def esc(value: object) -> str:
    return html.escape(str(value))


def svg_begin(title: str, desc: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
        '<rect width="1200" height="620" fill="#FFFEFB"/>', STYLE,
    ]


def write_unicode_svg(path: Path, data: dict) -> None:
    selected = [row for row in data["rows"] if row["sample"] in {"decomposed_e_acute", "circled_one"}]
    lines = svg_begin("Unicode normalization 改变码点与字节长度", "比较分解 e acute 与圈号一在 identity、NFC、NFD、NFKC、NFKD 下的码点和 UTF-8 字节数。")
    lines += ['<text x="55" y="55" font-size="24" font-weight="700" fill="#2563EB">Unicode normalization：同一视觉与不同信息合同</text>']
    forms = ["identity", "NFC", "NFD", "NFKC", "NFKD"]
    for panel, sample in enumerate(("decomposed_e_acute", "circled_one")):
        x0 = 70 + panel * 570
        lines.append(f'<text x="{x0}" y="105" font-size="20" font-weight="700" fill="#{"0F766E" if panel == 0 else "C24135"}">{esc(sample)}</text>')
        rows = {r["form"]: r for r in selected if r["sample"] == sample}
        for i, form in enumerate(forms):
            row = rows[form]; y = 155 + i * 75
            cpw = row["codepoint_count"] * 70
            byw = row["utf8_bytes"] * 45
            lines += [
                f'<text x="{x0}" y="{y}" font-size="16" font-weight="700">{form}</text>',
                f'<rect x="{x0+95}" y="{y-20}" width="{cpw}" height="22" fill="#2563EB"/><text x="{x0+105+cpw}" y="{y-3}" font-size="14">{row["codepoint_count"]} cp</text>',
                f'<rect x="{x0+95}" y="{y+10}" width="{byw}" height="22" fill="#B7791F"/><text x="{x0+105+byw}" y="{y+27}" font-size="14">{row["utf8_bytes"]} bytes</text>',
                f'<text x="{x0+310}" y="{y+2}" font-size="13" fill="#64748B">{" ".join(row["codepoints"])}</text>',
            ]
    lines += ['<text x="55" y="585" font-size="15" fill="#64748B">蓝条=码点数，琥珀条=UTF-8 bytes；Python unicodedata 版本写入 results.json，不代替 Unicode 官方 conformance tests。</text>', '</svg>']
    path.write_text("\n".join(lines), encoding="utf-8")


def write_path_svg(path: Path, bpe: dict, wp: dict) -> None:
    lines = svg_begin("BPE rank 与 WordPiece greedy 的路径反例", "左侧展示同一 abc 因 BPE merge rank 不同而分叉；右侧展示 WordPiece greedy 失败但全局路径存在。")
    lines += ['<text x="55" y="55" font-size="24" font-weight="700" fill="#2563EB">局部规则决定路径：rank 分叉与 greedy dead end</text>',
              '<line x1="600" y1="85" x2="600" y2="540" stroke="#D7DEE8" stroke-width="2"/>',
              '<text x="75" y="110" font-size="20" font-weight="700" fill="#2563EB">BPE：相同词表、不同 rank</text>',
              '<rect x="210" y="150" width="180" height="55" rx="8" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/><text x="300" y="185" text-anchor="middle" font-size="20">a b c</text>',
              '<line x1="270" y1="210" x2="165" y2="300" stroke="#2563EB" stroke-width="3"/><line x1="330" y1="210" x2="435" y2="300" stroke="#C24135" stroke-width="3"/>',
              f'<rect x="75" y="315" width="210" height="58" rx="8" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/><text x="180" y="350" text-anchor="middle" font-size="18">{esc(" ".join(bpe["rank_counterexample"]["ab_first"]))}</text>',
              f'<rect x="315" y="315" width="210" height="58" rx="8" fill="#FEE2E2" stroke="#C24135" stroke-width="2"/><text x="420" y="350" text-anchor="middle" font-size="18">{esc(" ".join(bpe["rank_counterexample"]["bc_first"]))}</text>',
              '<text x="180" y="410" text-anchor="middle" font-size="14" fill="#2563EB">(a,b) first</text><text x="420" y="410" text-anchor="middle" font-size="14" fill="#C24135">(b,c) first</text>',
              '<text x="645" y="110" font-size="20" font-weight="700" fill="#0F766E">WordPiece：最长局部匹配可死路</text>',
              '<text x="665" y="170" font-size="18">vocab = {a, ab, ##bc}</text>',
              '<rect x="665" y="215" width="150" height="55" rx="8" fill="#FEE2E2" stroke="#C24135" stroke-width="2"/><text x="740" y="250" text-anchor="middle" font-size="18">ab + ?c</text>',
              '<text x="835" y="250" font-size="16" font-weight="700" fill="#C24135">greedy → failure</text>',
              '<rect x="665" y="330" width="130" height="55" rx="8" fill="#ECFDF5" stroke="#0F766E" stroke-width="2"/><text x="730" y="365" text-anchor="middle" font-size="18">a</text>',
              '<rect x="815" y="330" width="150" height="55" rx="8" fill="#ECFDF5" stroke="#0F766E" stroke-width="2"/><text x="890" y="365" text-anchor="middle" font-size="18">##bc</text>',
              '<text x="985" y="365" font-size="16" font-weight="700" fill="#0F766E">global path exists</text>',
              '<text x="55" y="585" font-size="15" fill="#64748B">两例都是算法语义 oracle：不用于宣称 BPE 或 WordPiece 哪个下游更优。</text>', '</svg>']
    path.write_text("\n".join(lines), encoding="utf-8")


def write_unigram_svg(path: Path, data: dict) -> None:
    lines = svg_begin("Unigram 路径目标概率与抽样频率", "对字符串 ab 的两条路径，在 alpha 0.5 下比较精确温度化概率与固定 seed 经验频率。")
    lines += ['<text x="55" y="55" font-size="24" font-weight="700" fill="#2563EB">Unigram sampling oracle：exact target vs empirical frequency</text>']
    base_x = 190
    for i, row in enumerate(data["rows"]):
        x = base_x + i * 430
        target_h = row["target_alpha_0_5"] * 650
        emp_h = row["empirical_alpha_0_5"] * 650
        lines += [
            f'<text x="{x+120}" y="125" text-anchor="middle" font-size="20" font-weight="700">{esc(" + ".join(row["path"]))}</text>',
            f'<rect x="{x}" y="{500-target_h}" width="95" height="{target_h}" fill="#0F766E"/><text x="{x+47}" y="530" text-anchor="middle" font-size="14">target</text>',
            f'<rect x="{x+145}" y="{500-emp_h}" width="95" height="{emp_h}" fill="#2563EB"/><text x="{x+192}" y="530" text-anchor="middle" font-size="14">empirical</text>',
            f'<text x="{x+120}" y="565" text-anchor="middle" font-size="14" fill="#64748B">abs err={row["absolute_error"]:.4f}</text>',
        ]
    lines += [f'<text x="55" y="595" font-size="15" fill="#64748B">alpha={data["alpha"]}, draws={data["draws"]}, seed={SEED}；先枚举归一化，再检查采样器。</text>', '</svg>']
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--plots", type=Path, default=DEFAULT_PLOTS)
    parser.add_argument("--draws", type=int, default=20000)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.plots.mkdir(parents=True, exist_ok=True)

    rng = random.Random(SEED)
    unicode_data = audit_unicode()
    bpe_data = audit_bpe()
    wp_data = audit_wordpiece()
    unigram_data = audit_unigram(rng, args.draws)
    byte_data = audit_byte_roundtrip(rng)

    checks = {
        "unicode_nfc_equivalence": unicode_data["nfc_equivalent"],
        "unicode_nfkc_compatibility_change": unicode_data["nfkc_circled_one"] == "1" and unicode_data["nfkc_fullwidth_A"] == "A",
        "unicode_normalization_idempotent": unicode_data["idempotent"],
        "bpe_rank_counterexample": bpe_data["rank_counterexample"]["bc_first"] != bpe_data["rank_counterexample"]["ab_first"],
        "bpe_overlap_nonoverlap": bpe_data["overlap_aaaa"] == ["aa", "aa"],
        "wordpiece_greedy_dead_end": wp_data["greedy"] is None and wp_data["global_min_piece_path"] == ["a", "##bc"],
        "unigram_marginal": abs(unigram_data["marginal"] - 0.32) < 1e-12,
        "unigram_sampling": max(row["absolute_error"] for row in unigram_data["rows"]) < 0.015,
        "byte_roundtrip": byte_data["passed"],
    }
    payload = {
        "experiment_id": "EXP-LM-701-V1",
        "seed": SEED,
        "checks": checks,
        "unicode": unicode_data,
        "bpe": bpe_data,
        "wordpiece": wp_data,
        "unigram": unigram_data,
        "byte_roundtrip": byte_data,
    }
    (args.out / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(args.out / "unicode_normalization.csv", ["sample", "form", "text", "codepoints", "codepoint_count", "utf8_bytes"], [dict(row, codepoints=" ".join(row["codepoints"])) for row in unicode_data["rows"]])
    write_csv(args.out / "bpe_history.csv", ["rank", "chosen", "frequency", "ties"], [dict(row, chosen="+".join(row["chosen"]), ties="|".join("+".join(pair) for pair in row["ties"])) for row in bpe_data["history"]])
    write_csv(args.out / "unigram_paths.csv", ["path", "path_probability", "posterior_alpha_1", "target_alpha_0_5", "empirical_alpha_0_5", "absolute_error"], [dict(row, path="+".join(row["path"])) for row in unigram_data["rows"]])

    write_unicode_svg(args.plots / "plot-tokenization-unicode-normalization-v1.svg", unicode_data)
    write_path_svg(args.plots / "plot-tokenization-path-algorithms-v1.svg", bpe_data, wp_data)
    write_unigram_svg(args.plots / "plot-tokenization-unigram-sampling-v1.svg", unigram_data)

    print(json.dumps({"checks": checks, "out": str(args.out), "plots": str(args.plots)}, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
