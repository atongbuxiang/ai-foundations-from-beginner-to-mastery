#!/usr/bin/env python3
"""Deterministic audits for finite set laws, power-set growth, and split leakage.

Standard-library only. The script exhaustively checks finite Boolean-set laws,
records counterexample rates for plausible mutants, and writes a canonical SVG.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


def powerset_bits(size: int) -> list[int]:
    """Represent every subset of [size] as an integer bit mask."""
    return list(range(1 << size))


def complement(mask: int, full: int) -> int:
    return full ^ mask


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class SVG:
    def __init__(self, width: int = 1440, height: int = 760) -> None:
        self.width = width
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-01 finite set laws, object growth, multiplicity, and split leakage audit</title>',
            '<desc id="desc">Four proof-map panels audit finite set identities, cardinality growth, the effect of deduplication on empirical means, and entity leakage hidden by row-disjoint splits.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 19px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            ".cyan{stroke:#2672dd;fill:none;stroke-width:2.7}.purple{stroke:#783ee8;fill:none;stroke-width:2.7}",
            ".orange{stroke:#e77817;fill:none;stroke-width:2.7}.green{stroke:#07956d;fill:none;stroke-width:2.7}",
            "</style>",
            '<rect width="1440" height="760" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">Finite sets → computational contracts → leakage audit</text>',
            '<text x="36" y="62" class="sub">Exhaustive evidence checks a finite model; proofs and data-generating assumptions remain separate obligations.</text>',
        ]

    def text(self, x: float, y: float, value: object, cls: str = "label", anchor: str = "start") -> None:
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'
        )

    def rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        fill: str,
        stroke: str = "none",
        rx: float = 6,
    ) -> None:
        self.parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}"/>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str = "grid") -> None:
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>'
        )

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def circle(self, x: float, y: float, color: str) -> None:
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.4" fill="{color}"/>')

    def panel(self, x: float, y: float, width: float, height: float, title: str) -> None:
        self.rect(x, y, width, height, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def run_law_audit(size: int = 6) -> dict[str, object]:
    sets = powerset_bits(size)
    full = (1 << size) - 1
    pair_total = len(sets) ** 2
    triple_total = len(sets) ** 3

    pair_true = 0
    mutant_de_morgan = 0
    for a in sets:
        for b in sets:
            lhs = complement(a | b, full)
            rhs = complement(a, full) & complement(b, full)
            pair_true += lhs == rhs
            mutant_de_morgan += lhs == (complement(a, full) | complement(b, full))

    difference_true = 0
    distributive_true = 0
    xor_assoc_true = 0
    mutant_difference = 0
    mutant_distributive = 0
    for a in sets:
        for b in sets:
            for c in sets:
                difference_true += (a & complement(b | c, full)) == (
                    (a & complement(b, full)) & (a & complement(c, full))
                )
                distributive_true += (a & (b | c)) == ((a & b) | (a & c))
                xor_assoc_true += ((a ^ b) ^ c) == (a ^ (b ^ c))
                mutant_difference += (a & complement(b | c, full)) == (
                    (a & complement(b, full)) | (a & complement(c, full))
                )
                mutant_distributive += (a & (b | c)) == ((a & b) | c)

    assert pair_true == pair_total
    assert difference_true == triple_total
    assert distributive_true == triple_total
    assert xor_assoc_true == triple_total
    assert mutant_de_morgan < pair_total
    assert mutant_difference < triple_total
    assert mutant_distributive < triple_total

    return {
        "universe_size": size,
        "subset_count": len(sets),
        "pair_total": pair_total,
        "triple_total": triple_total,
        "true_counts": [pair_true, difference_true, distributive_true, xor_assoc_true],
        "mutant_pass_rates": [
            mutant_de_morgan / pair_total,
            mutant_difference / triple_total,
            mutant_distributive / triple_total,
        ],
    }


def run_container_audit() -> dict[str, float]:
    observations = [0.0, 0.0, 0.0, 10.0]
    deduplicated = sorted(set(observations))
    sequence_mean = sum(observations) / len(observations)
    set_mean = sum(deduplicated) / len(deduplicated)
    assert sequence_mean == 2.5
    assert set_mean == 5.0
    return {
        "sequence_count": float(len(observations)),
        "set_count": float(len(deduplicated)),
        "sequence_mean": sequence_mean,
        "set_mean": set_mean,
    }


def run_split_audit() -> dict[str, float]:
    # Thirty entities, four rows each. Alternating rows guarantees row-disjoint
    # splits while placing every entity in both splits.
    rows = list(range(120))
    entity = {row: row // 4 for row in rows}
    row_train = {row for row in rows if row % 2 == 0}
    row_test = set(rows) - row_train
    assert not (row_train & row_test)
    naive_train_entities = {entity[row] for row in row_train}
    naive_test_entities = {entity[row] for row in row_test}
    naive_overlap = naive_train_entities & naive_test_entities

    entity_train = set(range(20))
    entity_test = set(range(20, 30))
    grouped_train = {row for row in rows if entity[row] in entity_train}
    grouped_test = {row for row in rows if entity[row] in entity_test}
    grouped_train_entities = {entity[row] for row in grouped_train}
    grouped_test_entities = {entity[row] for row in grouped_test}
    grouped_overlap = grouped_train_entities & grouped_test_entities

    assert len(naive_overlap) == 30
    assert not grouped_overlap
    assert not (grouped_train & grouped_test)
    return {
        "naive_row_overlap_pct": 0.0,
        "naive_entity_overlap_pct": 100.0 * len(naive_overlap) / min(
            len(naive_train_entities), len(naive_test_entities)
        ),
        "grouped_row_overlap_pct": 0.0,
        "grouped_entity_overlap_pct": 0.0,
    }


def render(
    laws: dict[str, object],
    containers: dict[str, float],
    splits: dict[str, float],
) -> str:
    svg = SVG()
    svg.panel(24, 82, 688, 300, "A · Exhaustive laws on |U| = 6")
    svg.panel(728, 82, 688, 300, "B · Object-space growth")
    svg.panel(24, 398, 688, 330, "C · Deduplication changes the object")
    svg.panel(728, 398, 688, 330, "D · Row-disjoint ≠ entity-disjoint")

    # Panel A: verified laws and pass rates of plausible but false mutations.
    true_labels = ["De Morgan", "Difference", "Distributive", "XOR associativity"]
    true_counts = laws["true_counts"]
    totals = [laws["pair_total"], laws["triple_total"], laws["triple_total"], laws["triple_total"]]
    for i, (label, count, total) in enumerate(zip(true_labels, true_counts, totals)):
        y = 132 + i * 47
        svg.text(45, y + 14, label, "label")
        svg.rect(180, y, 300, 18, "#e8edf4", rx=4)
        svg.rect(180, y, 300, 18, "#07956d", rx=4)
        svg.text(494, y + 14, f"{count:,}/{total:,}", "small")
    mutant_labels = ["wrong De Morgan", "wrong difference", "missing A∩C"]
    mutant_rates = laws["mutant_pass_rates"]
    for i, (label, rate) in enumerate(zip(mutant_labels, mutant_rates)):
        y = 326 + i * 16
        svg.text(45, y, label, "small")
        svg.text(185, y, f"accidental pass {100.0 * rate:.2f}%", "small")
    svg.text(488, 342, "TRUE laws: 100%", "metric")
    svg.text(488, 366, "mutants: falsified", "small")

    # Panel B: log2 vertical scale makes the three growth regimes comparable.
    x0, y0, width, height = 790.0, 132.0, 570.0, 190.0
    for i in range(5):
        svg.line(x0, y0 + i * height / 4, x0 + width, y0 + i * height / 4)
        svg.line(x0 + i * width / 4, y0, x0 + i * width / 4, y0 + height)
    svg.line(x0, y0 + height, x0 + width, y0 + height, "axis")
    svg.line(x0, y0, x0, y0 + height, "axis")
    ns = list(range(1, 17))
    series = [
        ([float(n) for n in ns], "cyan", "#2672dd", "|U| = n"),
        ([float(n * n) for n in ns], "orange", "#e77817", "|U×U| = n²"),
        ([float(2**n) for n in ns], "purple", "#783ee8", "|P(U)| = 2ⁿ"),
    ]
    ymax = 16.0
    for values, line_cls, color, _ in series:
        points = []
        for n, value in zip(ns, values):
            px = x0 + (n - 1) / 15.0 * width
            py = y0 + height - math.log2(value) / ymax * height
            points.append((px, py))
        svg.polyline(points, line_cls)
        for px, py in points:
            svg.circle(px, py, color)
    svg.text(x0 + width / 2, y0 + height + 18, "base-set size n", "small", "middle")
    svg.text(x0 - 23, y0 + height / 2, "log₂ count", "small", "middle")
    for i, (_, _, color, label) in enumerate(series):
        lx = 820 + i * 175
        svg.rect(lx, 365, 16, 4, color, rx=2)
        svg.text(lx + 23, 370, label, "small")

    # Panel C: counts and means before/after discarding multiplicity.
    svg.text(48, 447, "Sequence / multiset", "label")
    svg.text(48, 475, "x = (0, 0, 0, 10)", "metric")
    svg.text(48, 509, "ordinary set", "label")
    svg.text(48, 537, "range(x) = {0, 10}", "metric")
    bar_x, bar_w = 365.0, 285.0
    items = [
        ("sample count", containers["sequence_count"], containers["set_count"], 4.0),
        ("empirical mean", containers["sequence_mean"], containers["set_mean"], 5.0),
    ]
    for i, (label, sequence_value, set_value, upper) in enumerate(items):
        y = 460 + i * 105
        svg.text(bar_x, y - 11, label, "label")
        svg.rect(bar_x, y, bar_w, 23, "#e8edf4", rx=4)
        svg.rect(bar_x, y, bar_w * sequence_value / upper, 23, "#66bce8", rx=4)
        svg.text(bar_x + 8, y + 17, f"with multiplicity: {sequence_value:g}", "small")
        svg.rect(bar_x, y + 31, bar_w, 23, "#e8edf4", rx=4)
        svg.rect(bar_x, y + 31, bar_w * set_value / upper, 23, "#f2a04b", rx=4)
        svg.text(bar_x + 8, y + 48, f"deduplicated set: {set_value:g}", "small")
    svg.text(48, 690, "Set conversion changes weights, not just notation.", "sub")

    # Panel D: normalized overlap at two identity levels.
    categories = ["naive row split", "grouped entity split"]
    row_rates = [splits["naive_row_overlap_pct"], splits["grouped_row_overlap_pct"]]
    entity_rates = [splits["naive_entity_overlap_pct"], splits["grouped_entity_overlap_pct"]]
    chart_x, chart_y, chart_w, chart_h = 790.0, 460.0, 560.0, 190.0
    for i in range(5):
        yy = chart_y + chart_h - i * chart_h / 4
        svg.line(chart_x, yy, chart_x + chart_w, yy)
        svg.text(chart_x - 12, yy + 4, f"{i * 25}%", "small", "end")
    group_centers = [chart_x + 160, chart_x + 410]
    for center, row_rate, entity_rate, label in zip(group_centers, row_rates, entity_rates, categories):
        bar_width = 72
        row_height = row_rate / 100.0 * chart_h
        entity_height = entity_rate / 100.0 * chart_h
        svg.rect(center - 82, chart_y + chart_h - row_height, bar_width, max(row_height, 1), "#2672dd", rx=3)
        svg.rect(center + 10, chart_y + chart_h - entity_height, bar_width, max(entity_height, 1), "#ed4163", rx=3)
        svg.text(center, chart_y + chart_h + 25, label, "small", "middle")
    svg.rect(1010, 690, 16, 5, "#2672dd", rx=2)
    svg.text(1033, 696, "row-ID overlap", "small")
    svg.rect(1160, 690, 16, 5, "#ed4163", rx=2)
    svg.text(1183, 696, "entity-ID overlap", "small")
    svg.text(755, 711, "30/30 entities leak under alternating-row split", "sub")
    return svg.finish()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "00-知识库管理/_assets/plots/math-foundations/plot-set-operations-split-audit-v2.svg"
        ),
    )
    args = parser.parse_args()

    laws = run_law_audit()
    containers = run_container_audit()
    splits = run_split_audit()
    svg = render(laws, containers, splits)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    mutant_rates = laws["mutant_pass_rates"]
    print(f"universe_size                 = {laws['universe_size']}")
    print(f"subset_count                  = {laws['subset_count']}")
    print(f"pair_assignments              = {laws['pair_total']}")
    print(f"triple_assignments            = {laws['triple_total']}")
    print("true_law_pass_rate            = 1.00000000")
    print(f"mutant_de_morgan_pass_rate    = {mutant_rates[0]:.8f}")
    print(f"mutant_difference_pass_rate   = {mutant_rates[1]:.8f}")
    print(f"mutant_distribute_pass_rate   = {mutant_rates[2]:.8f}")
    print(f"sequence_mean                 = {containers['sequence_mean']:.8f}")
    print(f"deduplicated_set_mean         = {containers['set_mean']:.8f}")
    print(f"naive_entity_overlap_pct      = {splits['naive_entity_overlap_pct']:.8f}")
    print(f"grouped_entity_overlap_pct    = {splits['grouped_entity_overlap_pct']:.8f}")
    print(f"svg_sha256                    = {digest}")


if __name__ == "__main__":
    main()
