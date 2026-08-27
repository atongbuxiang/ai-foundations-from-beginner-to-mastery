#!/usr/bin/env python3
"""Deterministic finite audits for functions, relations, and quotients.

Standard-library only. The script exhausts all functions 3→3, all subset
pairs for image/preimage laws, all binary relations on four elements, and all
Boolean-valued rules on a parity quotient. It emits a deterministic SVG.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
            '<title id="title">MATH-04 finite functions, set laws, equivalence relations, and quotient rules audit</title>',
            '<desc id="desc">Four proof-map panels exhaust finite functions, distinguish image and preimage laws, count equivalence relations, and test whether representative-dependent rules descend to a quotient.</desc>',
            "<style>",
            ".title{font-weight:700;font-size:24px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".sub{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#53627a}",
            ".paneltitle{font-weight:700;font-size:22px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#182236}",
            ".label{font-size:17px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#35445c}",
            ".small{font-size:15px;font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;fill:#5e6d84}",
            ".metric{font:700 18px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#182236}",
            ".grid{stroke:#dce4ef;stroke-width:1}.axis{stroke:#8292aa;stroke-width:1.2}",
            "</style>",
            '<rect width="1440" height="760" fill="#ffffff"/>',
            '<text x="36" y="38" class="title">MATH-04 audit · finite functions, set laws, equivalence relations, and quotient rules</text>',
            '<text x="36" y="62" class="sub">Exhaustive enumeration turns definitions into certificates; general infinite-domain claims still require proofs.</text>',
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

    def panel(
        self, x: float, y: float, w: float, h: float, title: str
    ) -> None:
        self.rect(x, y, w, h, "#fffefb", "#d6dee8", 0)
        self.text(x + 18, y + 27, title, "paneltitle")

    def finish(self) -> str:
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"


def powerset(size: int) -> list[frozenset[int]]:
    return [
        frozenset(i for i in range(size) if mask & (1 << i))
        for mask in range(1 << size)
    ]


def image(function: tuple[int, ...], subset: frozenset[int]) -> frozenset[int]:
    return frozenset(function[x] for x in subset)


def preimage(
    function: tuple[int, ...], subset: frozenset[int]
) -> frozenset[int]:
    return frozenset(x for x, y in enumerate(function) if y in subset)


def function_audit(size: int = 3) -> dict[str, int]:
    functions = list(itertools.product(range(size), repeat=size))
    injective = sum(len(set(f)) == size for f in functions)
    surjective = sum(set(f) == set(range(size)) for f in functions)
    bijective = sum(
        len(set(f)) == size and set(f) == set(range(size)) for f in functions
    )
    assert len(functions) == 27
    assert injective == surjective == bijective == 6
    return {
        "total": len(functions),
        "injective": injective,
        "surjective": surjective,
        "bijective": bijective,
        "neither": len(functions) - len(
            {f for f in functions if len(set(f)) == size or set(f) == set(range(size))}
        ),
    }


def set_law_audit(size: int = 3) -> dict[str, int]:
    universe = frozenset(range(size))
    subsets = powerset(size)
    functions = list(itertools.product(range(size), repeat=size))
    pair_checks = len(functions) * len(subsets) ** 2
    pre_union = pre_intersection = pre_complement = 0
    image_union = image_intersection_subset = image_intersection_equal = 0

    for f in functions:
        for a in subsets:
            for b in subsets:
                if preimage(f, a | b) == preimage(f, a) | preimage(f, b):
                    pre_union += 1
                if preimage(f, a & b) == preimage(f, a) & preimage(f, b):
                    pre_intersection += 1
                if preimage(f, universe - a) == universe - preimage(f, a):
                    pre_complement += 1
                if image(f, a | b) == image(f, a) | image(f, b):
                    image_union += 1
                lhs = image(f, a & b)
                rhs = image(f, a) & image(f, b)
                if lhs <= rhs:
                    image_intersection_subset += 1
                if lhs == rhs:
                    image_intersection_equal += 1

    assert pair_checks == 1728
    assert pre_union == pre_intersection == pre_complement == pair_checks
    assert image_union == image_intersection_subset == pair_checks
    assert image_intersection_equal < pair_checks

    roundtrip_checks = len(functions) * len(subsets)
    input_inclusion = input_equality = 0
    output_identity = output_equality = 0
    for f in functions:
        im = image(f, universe)
        for a in subsets:
            round_in = preimage(f, image(f, a))
            if a <= round_in:
                input_inclusion += 1
            if a == round_in:
                input_equality += 1

            round_out = image(f, preimage(f, a))
            if round_out == a & im:
                output_identity += 1
            if round_out == a:
                output_equality += 1

    assert roundtrip_checks == 216
    assert input_inclusion == output_identity == roundtrip_checks
    return {
        "pair_checks": pair_checks,
        "pre_union": pre_union,
        "pre_intersection": pre_intersection,
        "pre_complement": pre_complement,
        "image_union": image_union,
        "image_intersection_subset": image_intersection_subset,
        "image_intersection_equal": image_intersection_equal,
        "image_intersection_fail": pair_checks - image_intersection_equal,
        "roundtrip_checks": roundtrip_checks,
        "input_inclusion": input_inclusion,
        "input_equality": input_equality,
        "output_identity": output_identity,
        "output_equality": output_equality,
    }


def relation_properties(bits: int, size: int) -> tuple[bool, bool, bool]:
    def has(a: int, b: int) -> bool:
        return bool(bits & (1 << (a * size + b)))

    reflexive = all(has(a, a) for a in range(size))
    symmetric = all(
        has(a, b) == has(b, a)
        for a in range(size)
        for b in range(size)
    )
    transitive = all(
        not (has(a, b) and has(b, c)) or has(a, c)
        for a in range(size)
        for b in range(size)
        for c in range(size)
    )
    return reflexive, symmetric, transitive


def relation_audit(size: int = 4) -> dict[str, int]:
    total = 1 << (size * size)
    reflexive = symmetric = transitive = equivalence = 0
    for bits in range(total):
        r, s, t = relation_properties(bits, size)
        reflexive += r
        symmetric += s
        transitive += t
        equivalence += r and s and t
    assert total == 65536
    assert equivalence == 15
    return {
        "total": total,
        "reflexive": reflexive,
        "symmetric": symmetric,
        "transitive": transitive,
        "equivalence": equivalence,
    }


def quotient_audit() -> dict[str, object]:
    domain = range(4)
    rules = list(itertools.product([0, 1], repeat=4))
    well_defined = [
        rule
        for rule in rules
        if rule[0] == rule[2] and rule[1] == rule[3]
    ]
    witness = (0, 0, 1, 1)
    assert len(rules) == 16
    assert len(well_defined) == 4
    assert witness not in well_defined
    assert 0 % 2 == 2 % 2 and witness[0] != witness[2]
    return {
        "total": len(rules),
        "well_defined": len(well_defined),
        "representative_dependent": len(rules) - len(well_defined),
        "witness": witness,
        "classes": [[x for x in domain if x % 2 == parity] for parity in (0, 1)],
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
    # Reserve a wider label gutter now that proof-map body text is 14 px.
    svg.rect(x + 200, y, width, 18, "#edf2f7")
    fill = max(2.0, width * value / maximum)
    svg.rect(x + 200, y, fill, 18, color)
    svg.text(x + 210 + width, y + 13, f"{value:,}", "small", "end")


def render(
    funcs: dict[str, int],
    laws: dict[str, int],
    relations: dict[str, int],
    quotient: dict[str, object],
) -> str:
    svg = SVG()
    svg.panel(24, 82, 688, 300, "A · Functions X→Y, |X|=|Y|=3")
    svg.panel(728, 82, 688, 300, "B · Set-law exhaustive audit")
    svg.panel(24, 398, 688, 330, "C · Binary relations on four points")
    svg.panel(728, 398, 688, 330, "D · Parity quotient representatives")

    # A
    entries_a = [
        ("all functions", funcs["total"], "#2672dd"),
        ("injective", funcs["injective"], "#07956d"),
        ("surjective", funcs["surjective"], "#6f56c5"),
        ("bijective", funcs["bijective"], "#e77817"),
    ]
    for i, (label, value, color) in enumerate(entries_a):
        draw_bar(svg, 44, 128 + i * 48, 350, value, funcs["total"], label, color)
    svg.text(44, 337, "Finite equal-size certificate: injective ⇔ surjective ⇔ bijective.", "sub")
    svg.text(44, 360, "Counts: 3³=27 total; 3!=6 permutations.", "sub")

    # B
    entries_b = [
        ("preimage ∪ / ∩ / complement", laws["pair_checks"], "#07956d"),
        ("image union", laws["image_union"], "#2672dd"),
        ("image intersection subset", laws["image_intersection_subset"], "#6f56c5"),
        ("image intersection equality", laws["image_intersection_equal"], "#e77817"),
    ]
    for i, (label, value, color) in enumerate(entries_b):
        draw_bar(svg, 748, 128 + i * 48, 335, value, laws["pair_checks"], label, color)
    svg.text(748, 337, f"Strict failures of image(A∩C)=image(A)∩image(C): {laws['image_intersection_fail']:,}.", "sub")
    svg.text(748, 360, "Preimage Boolean laws and image-union law pass every finite case.", "sub")

    # C
    entries_c = [
        ("all relations", relations["total"], "#2672dd"),
        ("reflexive", relations["reflexive"], "#07956d"),
        ("symmetric", relations["symmetric"], "#6f56c5"),
        ("transitive", relations["transitive"], "#e77817"),
        ("equivalence", relations["equivalence"], "#d1495b"),
    ]
    for i, (label, value, color) in enumerate(entries_c):
        draw_bar(svg, 44, 448 + i * 43, 350, value, relations["total"], label, color)
    svg.text(44, 681, "Exactly 15 equivalence relations = Bell number B₄ = 15 partitions.", "sub")
    svg.text(44, 705, "Each property is audited independently before their conjunction.", "sub")

    # D
    q_total = int(quotient["total"])
    q_good = int(quotient["well_defined"])
    q_bad = int(quotient["representative_dependent"])
    svg.text(748, 450, "Parity classes", "small")
    svg.rect(748, 466, 278, 66, "#edf8f5", "#9ccfc1", 10)
    svg.text(887, 492, "[0] = {0,2}        [1] = {1,3}", "metric", "middle")
    svg.text(887, 518, "constant on each class ⇒ well-defined", "small", "middle")
    draw_bar(svg, 748, 557, 335, q_good, q_total, "well-defined rules", "#07956d")
    draw_bar(svg, 748, 605, 335, q_bad, q_total, "representative-dependent", "#e77817")
    svg.text(748, 669, "Failure witness g=(0,0,1,1): 0~2 but g(0)≠g(2).", "sub")
    svg.text(748, 695, "Only 2²=4 rules descend from four points to two classes.", "sub")

    return svg.finish()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "00-知识库管理/_assets/plots/math-foundations/"
            "plot-function-relation-quotient-audit-v2.svg"
        ),
    )
    args = parser.parse_args()

    funcs = function_audit()
    laws = set_law_audit()
    relations = relation_audit()
    quotient = quotient_audit()
    document = render(funcs, laws, relations, quotient)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    digest = hashlib.sha256(document.encode("utf-8")).hexdigest()

    print("FUNCTIONS", funcs)
    print("SET_LAWS", laws)
    print("RELATIONS", relations)
    print("QUOTIENT", quotient)
    print("OUTPUT", args.output)
    print("SHA256", digest)


if __name__ == "__main__":
    main()
