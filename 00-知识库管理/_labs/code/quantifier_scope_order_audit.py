#!/usr/bin/env python3
"""Deterministic audits for logical equivalence, quantifier order, and uniformity.

Standard-library only. Exhaustively checks propositional valuations and all 3x3
Boolean predicate tables, then writes a canonical light-theme SVG.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
from pathlib import Path


def esc(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, width: int = 1440, height: int = 760) -> None:
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-02 truth tables, witness order, and uniform guarantees audit</title>',
            '<desc id="desc">Four proof-map panels audit propositional identities, quantifier-order countermodels, fixed-event versus uniform success, and pointwise thresholds near a domain boundary.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 18px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            ".blue{stroke:#2672dd;fill:none;stroke-width:2.7}.purple{stroke:#783ee8;fill:none;stroke-width:2.7}",
            ".orange{stroke:#e77817;fill:none;stroke-width:2.7}.green{stroke:#07956d;fill:none;stroke-width:2.7}",
            "</style>",
            '<rect width="1440" height="760" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-02 audit · truth tables, witness order, and uniform guarantees</text>',
            '<text x="36" y="62" class="sub">Finite exhaustive semantics can expose countermodels; infinite-domain and probabilistic claims still require theorem-level arguments.</text>',
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
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.4" fill="{color}"/>')

    def panel(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def propositional_audit() -> dict[str, object]:
    pair_values = list(itertools.product([False, True], repeat=2))
    triple_values = list(itertools.product([False, True], repeat=3))

    implication = lambda p, q: (not p) or q
    true_checks = {
        "implication elimination": sum(implication(p, q) == ((not p) or q) for p, q in pair_values),
        "contraposition": sum(implication(p, q) == implication(not q, not p) for p, q in pair_values),
        "De Morgan": sum((not (p and q)) == ((not p) or (not q)) for p, q in pair_values),
        "implication transitivity": sum(
            implication(implication(p, q) and implication(q, r), implication(p, r))
            for p, q, r in triple_values
        ),
    }
    assert list(true_checks.values()) == [4, 4, 4, 8]

    mutants = {
        "converse as equivalent": sum(implication(p, q) == implication(q, p) for p, q in pair_values) / 4,
        "wrong De Morgan": sum((not (p and q)) == ((not p) and (not q)) for p, q in pair_values) / 4,
        "affirm consequent": sum(implication(implication(p, q) and q, p) for p, q in pair_values) / 4,
    }
    assert mutants == {
        "converse as equivalent": 0.5,
        "wrong De Morgan": 0.5,
        "affirm consequent": 0.75,
    }
    return {"true_checks": true_checks, "mutants": mutants}


def quantifier_matrix_audit(size: int = 3) -> dict[str, int]:
    total = 1 << (size * size)
    row_cover = 0
    global_column = 0
    both = 0
    row_only = 0
    for mask in range(total):
        value = lambda i, j: bool(mask & (1 << (i * size + j)))
        forall_exists = all(any(value(i, j) for j in range(size)) for i in range(size))
        exists_forall = any(all(value(i, j) for i in range(size)) for j in range(size))
        row_cover += forall_exists
        global_column += exists_forall
        both += forall_exists and exists_forall
        row_only += forall_exists and not exists_forall
        assert not exists_forall or forall_exists
    assert row_cover == (2**size - 1) ** size
    return {
        "size": size,
        "total": total,
        "forall_exists": row_cover,
        "exists_forall": global_column,
        "both": both,
        "row_only_countermodels": row_only,
    }


def fixed_uniform_audit() -> dict[str, list[float]]:
    class_sizes = list(range(2, 13))
    fixed_success = [1.0 - 1.0 / m for m in class_sizes]
    uniform_success = [0.0 for _ in class_sizes]
    assert fixed_success[-1] > 0.9
    assert all(value == 0.0 for value in uniform_success)
    return {"class_sizes": class_sizes, "fixed": fixed_success, "uniform": uniform_success}


def pointwise_uniform_audit(epsilon: float = 0.1) -> dict[str, list[float]]:
    xs = [0.5, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99, 0.995, 0.999]
    thresholds = [math.floor(math.log(epsilon) / math.log(x)) + 1 for x in xs]
    boundary_resolution = [1.0 / (1.0 - x) for x in xs]
    for x, n in zip(xs, thresholds):
        assert x**n < epsilon
        assert n == 1 or x ** (n - 1) >= epsilon
    assert all(b > a for a, b in zip(thresholds, thresholds[1:]))
    return {
        "xs": xs,
        "thresholds": thresholds,
        "resolution": boundary_resolution,
        "epsilon": [epsilon],
    }


def render(
    prop: dict[str, object],
    matrices: dict[str, int],
    uniformity: dict[str, list[float]],
    pointwise: dict[str, list[float]],
) -> str:
    svg = SVG()
    svg.panel(24, 82, 688, 300, "A · Propositional semantics")
    svg.panel(728, 82, 688, 300, "B · Boolean predicates on 3×3")
    svg.panel(24, 398, 688, 330, "C · Fixed-event vs uniform success")
    svg.panel(728, 398, 688, 330, "D · Pointwise threshold divergence")

    true_checks = prop["true_checks"]
    totals = [4, 4, 4, 8]
    for i, ((label, count), total) in enumerate(zip(true_checks.items(), totals)):
        y = 132 + i * 47
        svg.text(45, y + 14, label, "label")
        svg.rect(205, y, 275, 18, "#e8edf4", rx=4)
        svg.rect(205, y, 275, 18, "#07956d", rx=4)
        svg.text(494, y + 14, f"{count}/{total}", "small")
    for i, (label, rate) in enumerate(prop["mutants"].items()):
        y = 326 + i * 16
        svg.text(45, y, label, "small")
        svg.text(205, y, f"accidental pass {100 * rate:.0f}%", "small")
    svg.text(485, 342, "valid: 100%", "metric")
    svg.text(485, 365, "mutants need one counterrow", "small")

    labels = ["∀x∃y", "∃y∀x", "both", "row-only\ncountermodels"]
    values = [
        matrices["forall_exists"],
        matrices["exists_forall"],
        matrices["both"],
        matrices["row_only_countermodels"],
    ]
    colors = ["#2672dd", "#783ee8", "#07956d", "#e77817"]
    chart_x, chart_y, chart_w, chart_h = 790.0, 142.0, 555.0, 170.0
    for i in range(5):
        yy = chart_y + chart_h - i * chart_h / 4
        svg.line(chart_x, yy, chart_x + chart_w, yy)
        svg.text(chart_x - 10, yy + 4, f"{i * 25}%", "small", "end")
    centers = [850, 990, 1130, 1270]
    for center, label, value, color in zip(centers, labels, values, colors):
        pct = value / matrices["total"]
        height = pct * chart_h
        svg.rect(center - 35, chart_y + chart_h - height, 70, height, color, rx=4)
        first, *rest = label.split("\n")
        svg.text(center, 334, first, "small", "middle")
        if rest:
            svg.text(center, 349, rest[0], "small", "middle")
        svg.text(center, chart_y + chart_h - height - 7, f"{value} ({100*pct:.1f}%)", "small", "middle")
    svg.text(755, 371, "Global witness ⇒ row-wise witnesses; the converse has many finite countermodels.", "sub")

    x0, y0, width, height = 78.0, 456.0, 570.0, 190.0
    for i in range(5):
        svg.line(x0, y0 + i * height / 4, x0 + width, y0 + i * height / 4)
        svg.text(x0 - 10, y0 + height - i * height / 4 + 4, f"{i*25}%", "small", "end")
    svg.line(x0, y0 + height, x0 + width, y0 + height, "axis")
    sizes = uniformity["class_sizes"]
    fixed = uniformity["fixed"]
    shared = uniformity["uniform"]
    map_x = lambda m: x0 + (m - sizes[0]) / (sizes[-1] - sizes[0]) * width
    map_y = lambda v: y0 + height - v * height
    fixed_points = [(map_x(m), map_y(v)) for m, v in zip(sizes, fixed)]
    shared_points = [(map_x(m), map_y(v)) for m, v in zip(sizes, shared)]
    svg.polyline(fixed_points, "blue")
    svg.polyline(shared_points, "orange")
    for x, y in fixed_points:
        svg.circle(x, y, "#2672dd")
    for x, y in shared_points:
        svg.circle(x, y, "#e77817")
    svg.text(x0 + width / 2, 672, "number of hypotheses M", "small", "middle")
    svg.rect(178, 695, 16, 4, "#2672dd", rx=2)
    svg.text(201, 700, "each fixed event: 1−1/M", "small")
    svg.rect(409, 695, 16, 4, "#e77817", rx=2)
    svg.text(432, 700, "shared intersection: 0", "small")

    x0, y0, width, height = 790.0, 456.0, 560.0, 190.0
    resolutions = pointwise["resolution"]
    thresholds = pointwise["thresholds"]
    lx = [math.log10(v) for v in resolutions]
    ly = [math.log10(v) for v in thresholds]
    xmin, xmax = min(lx), max(lx)
    ymin, ymax = 0.0, math.ceil(max(ly))
    for i in range(5):
        svg.line(x0, y0 + i * height / 4, x0 + width, y0 + i * height / 4)
        svg.line(x0 + i * width / 4, y0, x0 + i * width / 4, y0 + height)
    svg.line(x0, y0 + height, x0 + width, y0 + height, "axis")
    svg.line(x0, y0, x0, y0 + height, "axis")
    points = [
        (
            x0 + (x - xmin) / (xmax - xmin) * width,
            y0 + height - (y - ymin) / (ymax - ymin) * height,
        )
        for x, y in zip(lx, ly)
    ]
    svg.polyline(points, "purple")
    for x, y in points:
        svg.circle(x, y, "#783ee8")
    svg.text(x0 + width / 2, 672, "boundary resolution 1/(1−x), log scale", "small", "middle")
    svg.text(x0 - 15, y0 + height / 2, "log N", "small", "middle")
    svg.text(755, 700, f"ε=0.1 · N(0.999)={thresholds[-1]} · sup_[0,1) xⁿ=1 ⇒ no uniform N", "sub")
    return svg.finish()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("00-知识库管理/_assets/plots/math-foundations/plot-quantifiers-negation-order-audit-v2.svg"),
    )
    args = parser.parse_args()

    prop = propositional_audit()
    matrices = quantifier_matrix_audit()
    uniformity = fixed_uniform_audit()
    pointwise = pointwise_uniform_audit()
    svg = render(prop, matrices, uniformity, pointwise)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print(f"propositional_true_laws      = {len(prop['true_checks'])}")
    print(f"matrix_domain_size           = {matrices['size']}x{matrices['size']}")
    print(f"matrix_predicates_total      = {matrices['total']}")
    print(f"forall_exists_count          = {matrices['forall_exists']}")
    print(f"exists_forall_count          = {matrices['exists_forall']}")
    print(f"row_only_countermodels       = {matrices['row_only_countermodels']}")
    print(f"fixed_success_M12            = {uniformity['fixed'][-1]:.8f}")
    print(f"uniform_success_M12          = {uniformity['uniform'][-1]:.8f}")
    print(f"pointwise_N_x0.999_eps0.1    = {pointwise['thresholds'][-1]}")
    print(f"svg_sha256                   = {digest}")


if __name__ == "__main__":
    main()
