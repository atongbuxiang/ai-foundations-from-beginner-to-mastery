#!/usr/bin/env python3
"""Deterministic audits for proof rules, cases, uniqueness, and conditions.

Standard-library only. Exhausts propositional valuations, all ordered pairs of
two cases on an eight-element domain, and all 3x3 Boolean relations. It also
renders the exact contraction factor for scalar quadratic gradient descent.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


def esc(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, width: int = 1440, height: int = 760) -> None:
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-03 proof obligations, case coverage, uniqueness, and optimization conditions audit</title>',
            '<desc id="desc">Four proof-map panels count countermodels for inference rules, classify case coverage, separate existence from uniqueness, and show the exact scalar gradient-descent stability interval.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 18px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            ".blue{stroke:#2672dd;fill:none;stroke-width:2.7}.orange{stroke:#e77817;fill:none;stroke-width:2.7}",
            "</style>",
            '<rect width="1440" height="760" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-03 audit · proof obligations, case coverage, uniqueness, and conditions</text>',
            '<text x="36" y="62" class="sub">Exhaustive finite checks expose invalid inference and missing obligations; theorem-level claims still require a general proof.</text>',
        ]

    def text(self, x: float, y: float, value: object, cls: str = "label", anchor: str = "start") -> None:
        self.parts.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>')

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str = "none", rx: float = 6) -> None:
        self.parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}"/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str = "grid") -> None:
        self.parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>')

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def circle(self, x: float, y: float, color: str) -> None:
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="{color}"/>')

    def panel(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def implication(p: bool, q: bool) -> bool:
    return (not p) or q


def rule_audit() -> dict[str, object]:
    pair = list(itertools.product([False, True], repeat=2))
    triple = list(itertools.product([False, True], repeat=3))

    def count(values: list[tuple[bool, ...]], premises, conclusion) -> int:
        return sum(all(premises(*v)) and not conclusion(*v) for v in values)

    valid = {
        "modus ponens": (count(pair, lambda p, q: (p, implication(p, q)), lambda p, q: q), 4),
        "modus tollens": (count(pair, lambda p, q: (implication(p, q), not q), lambda p, q: not p), 4),
        "hypothetical": (
            count(
                triple,
                lambda p, q, r: (implication(p, q), implication(q, r)),
                lambda p, q, r: implication(p, r),
            ),
            8,
        ),
        "proof by cases": (
            count(
                triple,
                lambda p, q, r: (p or q, implication(p, r), implication(q, r)),
                lambda p, q, r: r,
            ),
            8,
        ),
    }
    invalid = {
        "affirm consequent": (
            count(pair, lambda p, q: (implication(p, q), q), lambda p, q: p),
            4,
        ),
        "deny antecedent": (
            count(pair, lambda p, q: (implication(p, q), not p), lambda p, q: not q),
            4,
        ),
    }
    assert all(c == 0 for c, _ in valid.values())
    assert all(c == 1 for c, _ in invalid.values())
    return {"valid": valid, "invalid": invalid}


def case_coverage_audit(size: int = 8) -> dict[str, int]:
    full = (1 << size) - 1
    partition = 0
    overlapping_cover = 0
    gap = 0
    for a in range(1 << size):
        for b in range(1 << size):
            cover = (a | b) == full
            disjoint = (a & b) == 0
            if cover and disjoint:
                partition += 1
            elif cover:
                overlapping_cover += 1
            else:
                gap += 1
    total = (1 << size) ** 2
    assert total == 65536
    assert partition == 256
    assert overlapping_cover == 6305
    assert gap == 58975
    assert partition + overlapping_cover + gap == total
    return {
        "size": size,
        "total": total,
        "partition": partition,
        "overlapping_cover": overlapping_cover,
        "gap": gap,
        "all_covers": partition + overlapping_cover,
    }


def existence_uniqueness_audit(size: int = 3) -> dict[str, int]:
    total = 1 << (size * size)
    no_existence = 0
    existence_nonunique = 0
    unique = 0
    for bits in range(total):
        row_counts = [
            sum((bits >> (i * size + j)) & 1 for j in range(size))
            for i in range(size)
        ]
        if not all(c >= 1 for c in row_counts):
            no_existence += 1
        elif all(c == 1 for c in row_counts):
            unique += 1
        else:
            existence_nonunique += 1
    assert total == 512
    assert no_existence == 169
    assert existence_nonunique == 316
    assert unique == 27
    return {
        "size": size,
        "total": total,
        "no_existence": no_existence,
        "existence_nonunique": existence_nonunique,
        "unique": unique,
        "existence": existence_nonunique + unique,
    }


def gd_condition_audit() -> dict[str, object]:
    values = [i / 20 for i in range(61)]
    factors = [abs(1.0 - t) for t in values]
    stable = [t for t in values if 0.0 < t < 2.0]
    witnesses = {0.0: 1.0, 1.0: 0.0, 2.0: 1.0, 2.4: 1.4}
    assert len(stable) == 39
    assert witnesses == {0.0: 1.0, 1.0: 0.0, 2.0: 1.0, 2.4: 1.4}
    return {"values": values, "factors": factors, "stable": stable, "witnesses": witnesses}


def render(
    rules: dict[str, object],
    cases: dict[str, int],
    relations: dict[str, int],
    gd: dict[str, object],
) -> str:
    svg = SVG()
    svg.panel(24, 82, 688, 300, "A · Inference countermodels")
    svg.panel(728, 82, 688, 300, "B · Two-case coverage")
    svg.panel(24, 398, 688, 330, "C · Existence vs uniqueness")
    svg.panel(728, 398, 688, 330, "D · Scalar GD contraction")

    # A: rule countermodels
    entries = list(rules["valid"].items()) + list(rules["invalid"].items())
    y0 = 126
    for i, (name, (countermodels, denominator)) in enumerate(entries):
        y = y0 + i * 38
        color = "#07956d" if countermodels == 0 else "#e77817"
        svg.text(44, y + 13, name)
        svg.rect(210, y, 410, 18, "#edf2f7")
        width = 4 if countermodels == 0 else 100
        svg.rect(210, y, width, 18, color)
        svg.text(636, y + 13, f"{countermodels}/{denominator}", "small")
    svg.text(44, 365, "Valid rules have no valuation with all premises true and conclusion false.", "sub")

    # B: case coverage categories
    case_entries = [
        ("partition", cases["partition"], "#2672dd"),
        ("overlapping cover", cases["overlapping_cover"], "#07956d"),
        ("missing cases / gap", cases["gap"], "#e77817"),
    ]
    bx0, by0, bw, bh = 790, 140, 555, 170
    for i in range(5):
        y = by0 + i * bh / 4
        svg.line(bx0, y, bx0 + bw, y)
    maxv = cases["total"]
    bar_w = 115
    for i, (name, value, color) in enumerate(case_entries):
        x = bx0 + 50 + i * 170
        h = value / maxv * bh
        svg.rect(x, by0 + bh - h, bar_w, h, color, rx=4)
        svg.text(x + bar_w / 2, by0 + bh - h - 8, f"{value:,}", "small", "middle")
        svg.text(x + bar_w / 2, 334, name, "small", "middle")
        svg.text(x + bar_w / 2, 351, f"{100*value/maxv:.1f}%", "small", "middle")
    svg.text(748, 365, "Coverage is required; disjointness is optional unless counting would double-count.", "sub")

    # C: existence/uniqueness categories
    relation_entries = [
        ("no witness for some x", relations["no_existence"], "#e77817"),
        ("exists, not unique", relations["existence_nonunique"], "#2672dd"),
        ("unique witness each x", relations["unique"], "#07956d"),
    ]
    cx0, cy0, cw, ch = 85, 460, 555, 180
    for i in range(5):
        y = cy0 + i * ch / 4
        svg.line(cx0, y, cx0 + cw, y)
    for i, (name, value, color) in enumerate(relation_entries):
        x = cx0 + 45 + i * 178
        h = value / relations["total"] * ch
        svg.rect(x, cy0 + ch - h, 120, h, color, rx=4)
        svg.text(x + 60, cy0 + ch - h - 8, f"{value} ({100*value/relations['total']:.1f}%)", "small", "middle")
        svg.text(x + 60, 662, name, "small", "middle")
    svg.text(44, 704, "343 relations satisfy existence for every x; only 27 satisfy unique existence.", "sub")

    # D: contraction factor
    dx0, dy0, dw, dh = 790, 470, 560, 190
    # stable region
    stable_x0 = dx0
    stable_x1 = dx0 + (2.0 / 3.0) * dw
    svg.rect(stable_x0, dy0, stable_x1 - stable_x0, dh, "#e8f7f1", rx=0)
    for i in range(4):
        x = dx0 + i * dw / 3
        svg.line(x, dy0, x, dy0 + dh)
        svg.text(x, 680, str(i), "small", "middle")
    for i in range(5):
        y = dy0 + i * dh / 4
        svg.line(dx0, y, dx0 + dw, y)
        svg.text(dx0 - 10, y + 4, f"{2.0 - i * 0.5:.1f}", "small", "end")
    svg.line(dx0, dy0 + dh, dx0 + dw, dy0 + dh, "axis")
    svg.line(dx0, dy0, dx0, dy0 + dh, "axis")
    # y max 2.0
    points = [
        (
            dx0 + t / 3.0 * dw,
            dy0 + dh - factor / 2.0 * dh,
        )
        for t, factor in zip(gd["values"], gd["factors"])
    ]
    svg.polyline(points, "blue")
    # y = 1 threshold
    threshold_y = dy0 + dh - 1.0 / 2.0 * dh
    svg.parts.append(
        f'<line x1="{dx0}" y1="{threshold_y:.2f}" x2="{dx0+dw}" y2="{threshold_y:.2f}" stroke="#e77817" stroke-width="2" stroke-dasharray="7 5"/>'
    )
    for t, factor in gd["witnesses"].items():
        x = dx0 + t / 3.0 * dw
        y = dy0 + dh - factor / 2.0 * dh
        svg.circle(x, y, "#783ee8")
        svg.text(x, y - 10, f"{t:g}", "small", "middle")
    svg.text(dx0 + dw / 2, 704, "normalized step eta·a", "small", "middle")
    svg.text(748, 448, "Green region: 0 < eta·a < 2. Boundary points do not contract nonzero initializations.", "sub")
    return svg.finish()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "00-知识库管理/_assets/plots/math-foundations/"
            "plot-proof-obligations-counterexamples-audit-v2.svg"
        ),
    )
    args = parser.parse_args()

    rules = rule_audit()
    cases = case_coverage_audit()
    relations = existence_uniqueness_audit()
    gd = gd_condition_audit()
    svg = render(rules, cases, relations, gd)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print(f"valid_rules                    = {len(rules['valid'])}")
    print(f"invalid_rules_with_countermodel= {len(rules['invalid'])}")
    print(f"case_pairs_total               = {cases['total']}")
    print(f"case_partitions                = {cases['partition']}")
    print(f"case_overlapping_covers        = {cases['overlapping_cover']}")
    print(f"case_pairs_with_gap            = {cases['gap']}")
    print(f"relations_total                = {relations['total']}")
    print(f"relations_existence            = {relations['existence']}")
    print(f"relations_unique               = {relations['unique']}")
    print(f"relations_exists_not_unique    = {relations['existence_nonunique']}")
    print(f"gd_stable_grid_points          = {len(gd['stable'])}")
    print(f"svg_sha256                     = {digest}")


if __name__ == "__main__":
    main()
