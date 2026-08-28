#!/usr/bin/env python3
"""Generate the deterministic three-panel information-theory cumulative gate.

Only the Python standard library is used.  The panels separate:
1. the analytic Bernoulli-Hamming rate-distortion function;
2. a binary task with a nuisance bit, illustrating the IB plane;
3. fixed-model versus KT prequential codelength on a seeded sequence.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import random
import sys
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
DEFAULT_SEED = 20260819
DEFAULT_N = 400
DEFAULT_TRUE_P = 0.8


def h2(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def rd(d: float, source_probability: float = 0.5) -> float:
    maximum_distortion = min(source_probability, 1.0 - source_probability)
    return max(0.0, h2(source_probability) - h2(d)) if d <= maximum_distortion else 0.0


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


def seeded_sequence(seed: int, length: int, probability: float) -> list[int]:
    rng = random.Random(seed)
    return [1 if rng.random() < probability else 0 for _ in range(length)]


def prequential_lengths(
    xs: list[int],
    fixed_probability: float = 0.5,
    kt_alpha: float = 0.5,
) -> tuple[list[float], list[float], int | None]:
    fixed: list[float] = []
    kt: list[float] = []
    fixed_total = 0.0
    kt_total = 0.0
    successes = 0
    crossing: int | None = None
    for i, x in enumerate(xs, start=1):
        fixed_mass = fixed_probability if x == 1 else 1.0 - fixed_probability
        fixed_total += -math.log2(fixed_mass)
        previous = i - 1
        prob_one = (successes + kt_alpha) / (previous + 2.0 * kt_alpha)
        probability = prob_one if x == 1 else 1.0 - prob_one
        kt_total += -math.log2(probability)
        successes += x
        fixed.append(fixed_total)
        kt.append(kt_total)
        if crossing is None and i >= 2 and kt_total <= fixed_total:
            crossing = i
    return fixed, kt, crossing


def build_svg(
    source_probability: float = 0.5,
    rd_probe: float = 0.1,
    ib_noise: float = 0.1,
    nuisance_probability: float = 0.5,
    ib_beta: float = 2.0,
    sequence_probability: float = DEFAULT_TRUE_P,
    sequence_length: int = DEFAULT_N,
    fixed_probability: float = 0.5,
    kt_alpha: float = 0.5,
    seed: int = DEFAULT_SEED,
) -> tuple[str, dict[str, float | int | None]]:
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
    source_label = "1/2" if source_probability == 0.5 else f"{source_probability:g}"
    parts += [
        text(40, 53, "A · Bernoulli–Hamming 的理论 R(D)", "title"),
        text(40, 78, f"X~Ber({source_label})；蓝线是 information-theoretic frontier", "sub"),
    ]
    ax_l, ax_r, ax_t, ax_b = 73.0, 360.0, 112.0, 330.0
    parts += [line(ax_l, ax_b, ax_r, ax_b, stroke="#64748b", stroke_width="1.5"), line(ax_l, ax_t, ax_l, ax_b, stroke="#64748b", stroke_width="1.5")]
    rd_points = []
    maximum_distortion = min(source_probability, 1.0 - source_probability)
    source_entropy = h2(source_probability)
    for k in range(101):
        d = maximum_distortion * k / 100.0
        x = ax_l + (d / maximum_distortion) * (ax_r - ax_l)
        y = ax_b - rd(d, source_probability) / source_entropy * (ax_b - ax_t)
        rd_points.append((x, y))
    parts.append(path(rd_points, "#2563eb", 4.0))
    marker_distortions = [0.0, rd_probe, maximum_distortion / 2.0, maximum_distortion]
    for d in marker_distortions:
        x = ax_l + (d / maximum_distortion) * (ax_r - ax_l)
        y = ax_b - rd(d, source_probability) / source_entropy * (ax_b - ax_t)
        parts.append(circle(x, y, 5.0, "#7c3aed" if d < maximum_distortion else "#059669"))
        parts.append(text(x, ax_b + 20, f"{d:g}", "tiny", "middle"))
    rate_probe = rd(rd_probe, source_probability)
    parts += [text(54, 118, f"{source_entropy:g}", "tiny"), text(215, 373, "distortion D", "small", "middle"), text(47, 220, "rate", "small", "middle"), text(47, 235, "bits", "small", "middle")]
    if source_probability == 0.5 and rd_probe == 0.1:
        rd_summary = "D=0.1: R=0.5310 bits；D=0.5: R=0"
    else:
        rd_summary = f"D={rd_probe:g}: R={rate_probe:.4f} bits；D={maximum_distortion:g}: R=0"
    parts.append(text(40, 398, rd_summary, "small"))

    # Panel B: information bottleneck candidates.
    parts += [
        text(435, 53, "B · task bit Y 与 nuisance bit N", "title"),
        text(435, 78, "X=(Y,N)；理想表示保留 relevance、删除 nuisance", "sub"),
    ]
    bx_l, bx_r, bx_t, bx_b = 468.0, 755.0, 112.0, 330.0
    parts += [line(bx_l, bx_b, bx_r, bx_b, stroke="#64748b", stroke_width="1.5"), line(bx_l, bx_t, bx_l, bx_b, stroke="#64748b", stroke_width="1.5")]
    parts.append(line(bx_l, bx_t, bx_r, bx_t, stroke="#cbd5e1", stroke_width="1.2", stroke_dasharray="5 5"))

    nuisance_entropy = h2(nuisance_probability)
    full_rate = 1.0 + nuisance_entropy
    rate_axis_max = max(2.0, full_rate)

    def ib_xy(rate: float, relevance: float) -> tuple[float, float]:
        return bx_l + rate / rate_axis_max * (bx_r - bx_l), bx_b - relevance * (bx_b - bx_t)

    noise_curve = []
    for k in range(101):
        error = 0.5 * k / 100.0
        information = 1.0 - h2(error)
        noise_curve.append(ib_xy(information, information))
    parts.append(path(noise_curve, "#059669", 3.5))
    candidates = [
        (full_rate, 1.0, "keep X", "#dc2626"),
        (1.0, 1.0, "keep Y", "#2563eb"),
        (1.0 - h2(ib_noise), 1.0 - h2(ib_noise), "noisy Y", "#d97706"),
        (0.0, 0.0, "constant", "#7c3aed"),
    ]
    for rate, relevance, label, color in candidates:
        x, y = ib_xy(rate, relevance)
        parts.append(circle(x, y, 6.0, color))
        dx = -8 if label == "keep X" else 8
        anchor = "end" if label == "keep X" else "start"
        parts.append(text(x + dx, y - 10, label, "tiny", anchor))
    nuisance_summary = (
        "keep X 多花 1 bit 记 N，却不增加 I(Z;Y)"
        if nuisance_probability == 0.5
        else f"keep X 多花 {nuisance_entropy:.3f} bit 记 N，不增加 relevance"
    )
    parts += [text(610, 354, "I(X;Z) bits", "small", "middle"), text(444, 220, "I(Z;Y)", "small", "middle"), text(444, 235, "bits", "small", "middle"), text(435, 385, nuisance_summary, "small")]

    # Panel C: prequential MDL.
    xs = seeded_sequence(seed, sequence_length, sequence_probability)
    fixed, kt, crossing = prequential_lengths(xs, fixed_probability, kt_alpha)
    parts += [
        text(830, 53, "C · prequential code 会为学习速度付费", "title"),
        text(830, 78, f"seeded Ber({sequence_probability:g}) sequence；fixed p={fixed_probability:g} vs KT", "sub"),
    ]
    cx_l, cx_r, cx_t, cx_b = 850.0, 1150.0, 112.0, 330.0
    y_max = max(fixed[-1], kt[-1]) * 1.03
    parts += [line(cx_l, cx_b, cx_r, cx_b, stroke="#64748b", stroke_width="1.5"), line(cx_l, cx_t, cx_l, cx_b, stroke="#64748b", stroke_width="1.5")]

    def code_points(values: list[float]) -> list[tuple[float, float]]:
        return [
            (
                cx_l + i / (sequence_length - 1) * (cx_r - cx_l),
                cx_b - value / y_max * (cx_b - cx_t),
            )
            for i, value in enumerate(values)
        ]

    parts.append(path(code_points(fixed), "#dc2626", 3.0))
    parts.append(path(code_points(kt), "#2563eb", 3.5))
    parts += [text(1040, 134, "fixed p=0.5", "tiny"), text(1040, 184, "KT adaptive", "tiny"), text(1000, 354, "observations", "small", "middle"), text(824, 220, "bits", "small", "middle")]
    if crossing is not None:
        x_cross = cx_l + (crossing - 1) / (sequence_length - 1) * (cx_r - cx_l)
        parts.append(line(x_cross, cx_t, x_cross, cx_b, stroke="#d97706", stroke_width="1.2", stroke_dasharray="4 4"))
        parts.append(text(x_cross + 5, 312, f"cross n={crossing}", "tiny"))
    empirical_p = sum(xs) / sequence_length
    saving = fixed[-1] - kt[-1]
    parts.append(text(830, 385, f"p-hat={empirical_p:.3f}；KT 节省 {saving:.2f} bits（含学习开销）", "small"))

    parts.append("</svg>")
    metrics: dict[str, float | int | None] = {
        "rd_probe": rate_probe,
        "ib_noisy": 1.0 - h2(ib_noise),
        "ib_keep_x": full_rate - ib_beta,
        "ib_keep_y": 1.0 - ib_beta,
        "ib_noisy_objective": (1.0 - ib_beta) * (1.0 - h2(ib_noise)),
        "ib_constant": 0.0,
        "empirical_p": empirical_p,
        "fixed_bits": fixed[-1],
        "kt_bits": kt[-1],
        "saving_bits": saving,
        "crossing": crossing,
    }
    return "\n".join(parts) + "\n", metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--source-p", type=float, default=0.5)
    parser.add_argument("--rd-probe", type=float, default=0.1)
    parser.add_argument("--ib-noise", type=float, default=0.1)
    parser.add_argument("--nuisance-p", type=float, default=0.5)
    parser.add_argument("--ib-beta", type=float, default=2.0)
    parser.add_argument("--sequence-p", type=float, default=DEFAULT_TRUE_P)
    parser.add_argument("--sequence-length", type=int, default=DEFAULT_N)
    parser.add_argument("--fixed-p", type=float, default=0.5)
    parser.add_argument("--kt-alpha", type=float, default=0.5)
    args = parser.parse_args()

    for value, label in (
        (args.source_p, "--source-p"),
        (args.ib_noise, "--ib-noise"),
        (args.nuisance_p, "--nuisance-p"),
        (args.sequence_p, "--sequence-p"),
        (args.fixed_p, "--fixed-p"),
    ):
        if not 0.01 <= value <= 0.99:
            raise ValueError(f"{label} must lie in [0.01, 0.99]")
    maximum_distortion = min(args.source_p, 1.0 - args.source_p)
    if not 0.0 < args.rd_probe < maximum_distortion:
        raise ValueError("--rd-probe must lie strictly between 0 and min(source-p, 1-source-p)")
    if not 0.05 <= args.kt_alpha <= 5.0:
        raise ValueError("--kt-alpha must lie in [0.05, 5]")
    if not 0.1 <= args.ib_beta <= 10.0:
        raise ValueError("--ib-beta must lie in [0.1, 10]")
    if args.sequence_length < 20:
        raise ValueError("--sequence-length must be at least 20")

    svg, metrics = build_svg(
        source_probability=args.source_p,
        rd_probe=args.rd_probe,
        ib_noise=args.ib_noise,
        nuisance_probability=args.nuisance_p,
        ib_beta=args.ib_beta,
        sequence_probability=args.sequence_p,
        sequence_length=args.sequence_length,
        fixed_probability=args.fixed_p,
        kt_alpha=args.kt_alpha,
        seed=args.seed,
    )
    canonical_configuration = (
        args.seed == DEFAULT_SEED
        and args.source_p == 0.5
        and args.rd_probe == 0.1
        and args.ib_noise == 0.1
        and args.nuisance_p == 0.5
        and args.ib_beta == 2.0
        and args.sequence_p == DEFAULT_TRUE_P
        and args.sequence_length == DEFAULT_N
        and args.fixed_p == 0.5
        and args.kt_alpha == 0.5
    )
    if canonical_configuration:
        if abs(float(metrics["rd_probe"]) - float(metrics["ib_noisy"])) > 1e-12:
            raise AssertionError("the canonical binary examples should meet at 1-h2(0.1)")
        if not float(metrics["saving_bits"]) > 0.0:
            raise AssertionError("canonical KT coding should beat the mismatched fixed code")
        if metrics["crossing"] != 2:
            raise AssertionError("the canonical deterministic crossover audit changed")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    print(
        f"A_CONFIG source_p={args.source_p:g} probe_D={args.rd_probe:g} "
        f"max_D={maximum_distortion:g}"
    )
    print(f"A_RD probe_rate={metrics['rd_probe']:.8f} source_entropy={h2(args.source_p):.8f}")
    print(
        f"B_CONFIG noise={args.ib_noise:g} nuisance_p={args.nuisance_p:g} beta={args.ib_beta:g}"
    )
    print(
        "B_IB keep_x={ib_keep_x:.8f} keep_y={ib_keep_y:.8f} "
        "noisy_y={ib_noisy_objective:.8f} constant={ib_constant:.8f} "
        "noisy_information={ib_noisy:.8f}".format(**metrics)
    )
    print(
        f"C_CONFIG true_p={args.sequence_p:g} length={args.sequence_length} "
        f"fixed_p={args.fixed_p:g} kt_alpha={args.kt_alpha:g}"
    )
    print(
        "C_CODE empirical_p={empirical_p:.5f} fixed_bits={fixed_bits:.5f} "
        "kt_bits={kt_bits:.5f} saving_bits={saving_bits:.5f} crossing={crossing}".format(**metrics)
    )
    print(f"OUTPUT {args.output}")
    print(f"SHA256 {digest}")
    print(f"PYTHON {sys.version.split()[0]}")
    print(f"SEED {args.seed}")


if __name__ == "__main__":
    main()
