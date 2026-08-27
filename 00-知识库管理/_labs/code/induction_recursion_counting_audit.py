#!/usr/bin/env python3
"""Deterministic audits for induction coverage, recursion, and counting.

Standard-library only. The script computes finite reachability certificates for
induction strides, exact naive-Fibonacci call counts versus memoized states,
enumerates all 12-bit strings to verify binomial counts and inclusion-exclusion,
and compares a complete autoregressive tree with fixed-width beam expansion.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
from pathlib import Path


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class SVG:
    def __init__(self, width: int = 1440, height: int = 760) -> None:
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">MATH-05 induction reachability, recursion calls, exact counting, and beam pruning audit</title>',
            '<desc id="desc">Four proof-map panels show induction reachability under different bases and strides, recursive versus memoized Fibonacci cost, exact binary-string counts, and full-tree versus beam-search expansions.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 18px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            ".blue{stroke:#2672dd;fill:none;stroke-width:2.8}.orange{stroke:#e77817;fill:none;stroke-width:2.8}",
            "</style>",
            '<rect width="1440" height="760" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-05 audit · induction reachability, recursion calls, exact counting, and beam pruning</text>',
            '<text x="36" y="62" class="sub">Finite certificates expose missing bases and repeated states; general claims still require induction and representation proofs.</text>',
        ]

    def text(
        self,
        x: float,
        y: float,
        value: object,
        cls: str = "label",
        anchor: str = "start",
    ) -> None:
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'
        )

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str,
        stroke: str = "none",
        rx: float = 6,
    ) -> None:
        self.parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" fill="{fill}" stroke="{stroke}"/>'
        )

    def line(
        self, x1: float, y1: float, x2: float, y2: float, cls: str = "grid"
    ) -> None:
        self.parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" class="{cls}"/>'
        )

    def polyline(self, points: list[tuple[float, float]], cls: str) -> None:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" class="{cls}"/>')

    def circle(self, x: float, y: float, r: float, fill: str) -> None:
        self.parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}"/>'
        )

    def panel(
        self, x: float, y: float, w: float, h: float, title: str
    ) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def reachable_indices(
    bases: set[int], stride: int, maximum: int
) -> set[int]:
    reached = {b for b in bases if 0 <= b <= maximum}
    changed = True
    while changed:
        changed = False
        for n in sorted(reached):
            target = n + stride
            if target <= maximum and target not in reached:
                reached.add(target)
                changed = True
    return reached


def induction_audit(maximum: int = 15) -> dict[str, object]:
    scenarios = [
        ("base {0}, step +1", {0}, 1),
        ("base {0}, step +2", {0}, 2),
        ("bases {0,1}, step +2", {0, 1}, 2),
        ("base {5}, step +1", {5}, 1),
    ]
    results = []
    for name, bases, stride in scenarios:
        reached = reachable_indices(bases, stride, maximum)
        results.append(
            {
                "name": name,
                "bases": sorted(bases),
                "stride": stride,
                "reached": sorted(reached),
                "count": len(reached),
            }
        )
    assert results[0]["count"] == 16
    assert results[1]["reached"] == list(range(0, 16, 2))
    assert results[2]["count"] == 16
    assert results[3]["reached"] == list(range(5, 16))
    return {"maximum": maximum, "scenarios": results}


def fibonacci_values(maximum: int) -> list[int]:
    values = [0, 1]
    for _ in range(2, maximum + 1):
        values.append(values[-1] + values[-2])
    return values[: maximum + 1]


def recursion_audit(maximum: int = 20) -> dict[str, object]:
    calls = [1, 1]
    for _ in range(2, maximum + 1):
        calls.append(1 + calls[-1] + calls[-2])
    fib = fibonacci_values(maximum + 1)
    expected = [2 * fib[n + 1] - 1 for n in range(maximum + 1)]
    memo_states = [n + 1 for n in range(maximum + 1)]
    additions = [0 if n < 2 else n - 1 for n in range(maximum + 1)]
    assert calls == expected
    assert calls[10] == 177
    assert calls[20] == 21891
    return {
        "maximum": maximum,
        "calls": calls,
        "memo_states": memo_states,
        "additions": additions,
    }


def counting_audit(length: int = 12) -> dict[str, object]:
    counts = [0] * (length + 1)
    starts_one = 0
    ends_one = 0
    both = 0
    total = 0
    for bits in itertools.product((0, 1), repeat=length):
        total += 1
        counts[sum(bits)] += 1
        starts_one += bits[0] == 1
        ends_one += bits[-1] == 1
        both += bits[0] == 1 and bits[-1] == 1
    expected = [math.comb(length, k) for k in range(length + 1)]
    union = starts_one + ends_one - both
    direct_union = sum(
        bits[0] == 1 or bits[-1] == 1
        for bits in itertools.product((0, 1), repeat=length)
    )
    assert counts == expected
    assert total == 4096
    assert sum(counts) == 2**length
    assert (starts_one, ends_one, both, union) == (2048, 2048, 1024, 3072)
    assert union == direct_union
    return {
        "length": length,
        "total": total,
        "counts": counts,
        "expected": expected,
        "starts_one": starts_one,
        "ends_one": ends_one,
        "both": both,
        "union": union,
        "naive_sum": starts_one + ends_one,
    }


def search_audit(
    vocabulary: int = 4, beam: int = 3, maximum_depth: int = 8
) -> dict[str, object]:
    depths = list(range(1, maximum_depth + 1))
    full_cumulative = [
        sum(vocabulary**t for t in range(1, depth + 1))
        for depth in depths
    ]
    beam_cumulative = [
        vocabulary + (depth - 1) * beam * vocabulary
        for depth in depths
    ]
    terminal_paths = [vocabulary**depth for depth in depths]
    assert full_cumulative[5] == 5460
    assert full_cumulative[-1] == 87380
    assert beam_cumulative[5] == 64
    assert beam_cumulative[-1] == 88
    return {
        "vocabulary": vocabulary,
        "beam": beam,
        "depths": depths,
        "full_cumulative": full_cumulative,
        "beam_cumulative": beam_cumulative,
        "terminal_paths": terminal_paths,
    }


def draw_bar(
    svg: SVG,
    x: float,
    y: float,
    width: float,
    value: int,
    maximum: int,
    label: str,
    color: str,
) -> None:
    svg.text(x, y + 13, label)
    svg.rect(x + 190, y, width, 18, "#edf2f7")
    fill = max(2.0, width * value / maximum)
    svg.rect(x + 190, y, fill, 18, color)
    svg.text(x + 202 + width, y + 13, f"{value:,}", "small", "end")


def render(
    induction: dict[str, object],
    recursion: dict[str, object],
    counting: dict[str, object],
    search: dict[str, object],
) -> str:
    svg = SVG()
    svg.panel(24, 82, 688, 300, "A · Induction coverage")
    svg.panel(728, 82, 688, 300, "B · Fibonacci recursion states")
    svg.panel(24, 398, 688, 330, "C · 4,096 binary strings")
    svg.panel(728, 398, 688, 330, "D · Full tree vs beam search")

    # A: reachable indices as 4 rows of cells
    colors = ["#07956d", "#e77817", "#2672dd", "#6f56c5"]
    for row, scenario in enumerate(induction["scenarios"]):
        y = 132 + row * 55
        svg.text(44, y + 12, scenario["name"], "small")
        reached = set(scenario["reached"])
        for n in range(16):
            x = 218 + n * 27
            fill = colors[row] if n in reached else "#e8edf4"
            svg.rect(x, y, 20, 20, fill, rx=3)
            if row == 3:
                svg.text(x + 10, y + 39, n, "small", "middle")
        svg.text(673, y + 14, f"{scenario['count']}/16", "small", "end")
    svg.text(44, 352, "Stride +2 needs bases in both residue classes; base 5 correctly proves only n≥5.", "sub")

    # B: log-scale lines
    x0, y0, w, h = 780, 132, 560, 182
    max_log = math.log10(max(recursion["calls"]))
    for i in range(5):
        y = y0 + i * h / 4
        svg.line(x0, y, x0 + w, y)
    call_points = []
    memo_points = []
    for n, (calls, states) in enumerate(
        zip(recursion["calls"], recursion["memo_states"])
    ):
        x = x0 + n / recursion["maximum"] * w
        call_y = y0 + h - math.log10(calls) / max_log * h
        memo_y = y0 + h - math.log10(states) / max_log * h
        call_points.append((x, call_y))
        memo_points.append((x, memo_y))
    svg.polyline(call_points, "orange")
    svg.polyline(memo_points, "blue")
    svg.text(780, 336, "orange: recursive calls  C₂₀=21,891", "sub")
    svg.text(1065, 336, "blue: memo states  n+1=21", "sub")
    svg.text(780, 360, "Same value recurrence, different computation graph and cost.", "sub")

    # C: Hamming weight counts
    counts = counting["counts"]
    max_count = max(counts)
    cx0, cy0, cw, ch = 72, 461, 590, 157
    for i in range(5):
        y = cy0 + i * ch / 4
        svg.line(cx0, y, cx0 + cw, y)
    bar_w = cw / len(counts) * 0.72
    for k, value in enumerate(counts):
        x = cx0 + (k + 0.14) * cw / len(counts)
        height = value / max_count * ch
        svg.rect(x, cy0 + ch - height, bar_w, height, "#2672dd", rx=2)
        svg.text(x + bar_w / 2, cy0 + ch + 18, k, "small", "middle")
    svg.text(44, 655, "Enumerated weight counts exactly match C(12,k); their sum is 2¹²=4,096.", "sub")
    svg.text(44, 681, "starts-1 + ends-1 = 4,096; subtract overlap 1,024 ⇒ union 3,072.", "sub")
    svg.text(44, 705, "Naive addition overcounts the intersection by exactly 1,024 strings.", "sub")

    # D: log-scale tree versus beam
    dx0, dy0, dw, dh = 780, 461, 560, 166
    max_log_d = math.log10(max(search["full_cumulative"]))
    for i in range(5):
        y = dy0 + i * dh / 4
        svg.line(dx0, y, dx0 + dw, y)
    full_points = []
    beam_points = []
    for depth, full, beam in zip(
        search["depths"],
        search["full_cumulative"],
        search["beam_cumulative"],
    ):
        x = dx0 + (depth - 1) / (len(search["depths"]) - 1) * dw
        full_y = dy0 + dh - math.log10(full) / max_log_d * dh
        beam_y = dy0 + dh - math.log10(beam) / max_log_d * dh
        full_points.append((x, full_y))
        beam_points.append((x, beam_y))
        svg.circle(x, full_y, 2.8, "#e77817")
        svg.circle(x, beam_y, 2.8, "#2672dd")
        svg.text(x, dy0 + dh + 18, depth, "small", "middle")
    svg.polyline(full_points, "orange")
    svg.polyline(beam_points, "blue")
    svg.text(748, 655, "depth 8: full 87,380 cumulative nodes; beam upper bound 88 expansions.", "sub")
    svg.text(748, 681, "Pruning controls visited states but does not certify global optimality.", "sub")
    svg.text(748, 705, "Both panels use log-scaled y coordinates; labels report exact counts.", "sub")

    return svg.finish()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "00-知识库管理/_assets/plots/math-foundations/"
            "plot-induction-recursion-counting-audit-v2.svg"
        ),
    )
    args = parser.parse_args()

    induction = induction_audit()
    recursion = recursion_audit()
    counting = counting_audit()
    search = search_audit()
    document = render(induction, recursion, counting, search)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    digest = hashlib.sha256(document.encode("utf-8")).hexdigest()

    print("INDUCTION", induction)
    print(
        "RECURSION",
        {
            "C10": recursion["calls"][10],
            "C20": recursion["calls"][20],
            "memo20": recursion["memo_states"][20],
        },
    )
    print("COUNTING", counting)
    print("SEARCH", search)
    print("OUTPUT", args.output)
    print("SHA256", digest)


if __name__ == "__main__":
    main()
