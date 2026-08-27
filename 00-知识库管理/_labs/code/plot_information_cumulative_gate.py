#!/usr/bin/env python3
"""Generate the deterministic three-panel information-theory cumulative gate.

Only the Python standard library is used.  The panels separate:
1. the analytic Bernoulli-Hamming rate-distortion function;
2. a binary task with a nuisance bit, illustrating the IB plane;
3. fixed-model versus KT prequential codelength on a seeded sequence.
"""

from __future__ import annotations

import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "information-theory"
    / "plot-information-cumulative-gate-v2.svg"
)
SEED = 20260819
N = 400
TRUE_P = 0.8


def h2(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def rd(d: float) -> float:
    return max(0.0, 1.0 - h2(d)) if d <= 0.5 else 0.0


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def line(x1: float, y1: float, x2: float, y2: float, **attrs: object) -> str:
    extra = " ".join(f'{key.replace("_", "-")}="{esc(value)}"' for key, value in attrs.items())
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {extra}/>'


def text(x: float, y: float, value: object, cls: str = "small", anchor: str = "start") -> str:
    return f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}">{esc(value)}</text>'


def path(points: list[tuple[float, float]], color: str, width: float = 3.0, dash: str | None = None) -> str:
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attr}/>'


def circle(x: float, y: float, radius: float, color: str) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}"/>'


def seeded_sequence() -> list[int]:
    rng = random.Random(SEED)
    return [1 if rng.random() < TRUE_P else 0 for _ in range(N)]


def prequential_lengths(xs: list[int]) -> tuple[list[float], list[float], int | None]:
    fixed: list[float] = []
    kt: list[float] = []
    fixed_total = 0.0
    kt_total = 0.0
    successes = 0
    crossing: int | None = None
    for i, x in enumerate(xs, start=1):
        fixed_total += 1.0  # -log2 0.5
        previous = i - 1
        prob_one = (successes + 0.5) / (previous + 1.0)
        probability = prob_one if x == 1 else 1.0 - prob_one
        kt_total += -math.log2(probability)
        successes += x
        fixed.append(fixed_total)
        kt.append(kt_total)
        if crossing is None and i >= 2 and kt_total <= fixed_total:
            crossing = i
    return fixed, kt, crossing


def build_svg() -> tuple[str, dict[str, float | int | None]]:
    width, height = 1200, 430
    panel_x = [20, 415, 810]
    panel_w = 370
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">信息论累计复现门</title>',
        '<desc id="desc">三面板展示 Bernoulli 率失真、信息瓶颈边界与有限样本通用编码账本。</desc>',
        '<rect width="1200" height="430" fill="#ffffff"/>',
        """<style>
        text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.panel{fill:#fffefb;stroke:#d7dee8;stroke-width:1.5}.title{font-size:19px;font-weight:700;fill:#1f2937}.sub,.body,.small,.tiny{font-size:15px}.sub{fill:#475569}.body{fill:#334155}.small,.tiny{fill:#64748b}
        </style>""",
    ]
    for x in panel_x:
        parts.append(f'<rect class="panel" x="{x}" y="20" width="{panel_w}" height="390"/>')

    # Panel A: Bernoulli-Hamming R(D).
    parts += [
        text(40, 53, "A · Bernoulli–Hamming 的理论 R(D)", "title"),
        text(40, 78, "X~Ber(1/2)；蓝线是 information-theoretic frontier", "sub"),
    ]
    ax_l, ax_r, ax_t, ax_b = 73.0, 360.0, 112.0, 330.0
    parts += [line(ax_l, ax_b, ax_r, ax_b, stroke="#64748b", stroke_width="1.5"), line(ax_l, ax_t, ax_l, ax_b, stroke="#64748b", stroke_width="1.5")]
    rd_points = []
    for k in range(101):
        d = 0.5 * k / 100.0
        x = ax_l + (d / 0.5) * (ax_r - ax_l)
        y = ax_b - rd(d) * (ax_b - ax_t)
        rd_points.append((x, y))
    parts.append(path(rd_points, "#2563eb", 4.0))
    for d in [0.0, 0.1, 0.25, 0.5]:
        x = ax_l + (d / 0.5) * (ax_r - ax_l)
        y = ax_b - rd(d) * (ax_b - ax_t)
        parts.append(circle(x, y, 5.0, "#7c3aed" if d < 0.5 else "#059669"))
        parts.append(text(x, ax_b + 20, f"{d:g}", "tiny", "middle"))
    parts += [text(54, 118, "1", "tiny"), text(205, 354, "distortion D", "small", "middle"), text(47, 220, "rate", "small", "middle"), text(47, 235, "bits", "small", "middle")]
    parts.append(text(40, 385, "D=0.1: R=0.5310 bits；D=0.5: R=0", "small"))

    # Panel B: information bottleneck candidates.
    parts += [
        text(435, 53, "B · task bit Y 与 nuisance bit N", "title"),
        text(435, 78, "X=(Y,N)；理想表示保留 relevance、删除 nuisance", "sub"),
    ]
    bx_l, bx_r, bx_t, bx_b = 468.0, 755.0, 112.0, 330.0
    parts += [line(bx_l, bx_b, bx_r, bx_b, stroke="#64748b", stroke_width="1.5"), line(bx_l, bx_t, bx_l, bx_b, stroke="#64748b", stroke_width="1.5")]
    parts.append(line(bx_l, bx_t, bx_r, bx_t, stroke="#cbd5e1", stroke_width="1.2", stroke_dasharray="5 5"))

    def ib_xy(rate: float, relevance: float) -> tuple[float, float]:
        return bx_l + rate / 2.0 * (bx_r - bx_l), bx_b - relevance * (bx_b - bx_t)

    noise_curve = []
    for k in range(101):
        error = 0.5 * k / 100.0
        information = 1.0 - h2(error)
        noise_curve.append(ib_xy(information, information))
    parts.append(path(noise_curve, "#059669", 3.5))
    candidates = [
        (2.0, 1.0, "keep X", "#dc2626"),
        (1.0, 1.0, "keep Y", "#2563eb"),
        (1.0 - h2(0.1), 1.0 - h2(0.1), "noisy Y", "#d97706"),
        (0.0, 0.0, "constant", "#7c3aed"),
    ]
    for rate, relevance, label, color in candidates:
        x, y = ib_xy(rate, relevance)
        parts.append(circle(x, y, 6.0, color))
        dx = -8 if label == "keep X" else 8
        anchor = "end" if label == "keep X" else "start"
        parts.append(text(x + dx, y - 10, label, "tiny", anchor))
    parts += [text(610, 354, "I(X;Z) bits", "small", "middle"), text(444, 220, "I(Z;Y)", "small", "middle"), text(444, 235, "bits", "small", "middle"), text(435, 385, "keep X 多花 1 bit 记 N，却不增加 I(Z;Y)", "small")]

    # Panel C: prequential MDL.
    xs = seeded_sequence()
    fixed, kt, crossing = prequential_lengths(xs)
    parts += [
        text(830, 53, "C · prequential code 会为学习速度付费", "title"),
        text(830, 78, "seeded Ber(0.8) sequence；fixed p=0.5 vs KT", "sub"),
    ]
    cx_l, cx_r, cx_t, cx_b = 850.0, 1150.0, 112.0, 330.0
    y_max = max(fixed[-1], kt[-1]) * 1.03
    parts += [line(cx_l, cx_b, cx_r, cx_b, stroke="#64748b", stroke_width="1.5"), line(cx_l, cx_t, cx_l, cx_b, stroke="#64748b", stroke_width="1.5")]

    def code_points(values: list[float]) -> list[tuple[float, float]]:
        return [
            (
                cx_l + i / (N - 1) * (cx_r - cx_l),
                cx_b - value / y_max * (cx_b - cx_t),
            )
            for i, value in enumerate(values)
        ]

    parts.append(path(code_points(fixed), "#dc2626", 3.0))
    parts.append(path(code_points(kt), "#2563eb", 3.5))
    parts += [text(1040, 134, "fixed p=0.5", "tiny"), text(1040, 184, "KT adaptive", "tiny"), text(1000, 354, "observations", "small", "middle"), text(824, 220, "bits", "small", "middle")]
    if crossing is not None:
        x_cross = cx_l + (crossing - 1) / (N - 1) * (cx_r - cx_l)
        parts.append(line(x_cross, cx_t, x_cross, cx_b, stroke="#d97706", stroke_width="1.2", stroke_dasharray="4 4"))
        parts.append(text(x_cross + 5, 312, f"cross n={crossing}", "tiny"))
    empirical_p = sum(xs) / N
    saving = fixed[-1] - kt[-1]
    parts.append(text(830, 385, f"p-hat={empirical_p:.3f}；KT 节省 {saving:.2f} bits（含学习开销）", "small"))

    parts.append("</svg>")
    metrics: dict[str, float | int | None] = {
        "rd_d01": rd(0.1),
        "ib_noisy": 1.0 - h2(0.1),
        "empirical_p": empirical_p,
        "fixed_bits": fixed[-1],
        "kt_bits": kt[-1],
        "saving_bits": saving,
        "crossing": crossing,
    }
    return "\n".join(parts) + "\n", metrics


def main() -> None:
    svg, metrics = build_svg()
    if abs(float(metrics["rd_d01"]) - float(metrics["ib_noisy"])) > 1e-12:
        raise AssertionError("the matched binary examples should meet at 1-h2(0.1)")
    if not float(metrics["saving_bits"]) > 0.0:
        raise AssertionError("KT coding should beat the mismatched fixed code on this sequence")
    if metrics["crossing"] != 2:
        raise AssertionError("the deterministic crossover audit changed unexpectedly")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT}")
    print(f"rd_D0.1={metrics['rd_d01']:.8f} ib_noisy={metrics['ib_noisy']:.8f}")
    print(
        "empirical_p={empirical_p:.5f} fixed_bits={fixed_bits:.5f} "
        "kt_bits={kt_bits:.5f} saving_bits={saving_bits:.5f} crossing={crossing}".format(**metrics)
    )


if __name__ == "__main__":
    main()
