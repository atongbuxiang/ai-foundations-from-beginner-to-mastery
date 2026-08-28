#!/usr/bin/env python3
"""Deterministic three-track gate for LT-CUM-01.

The program uses only the Python standard library.  It separates three claims:

1. finite-sample ERM selection in an exactly enumerable binary problem;
2. conditional Bayes actions under an explicit cost/reject contract;
3. holdout selection optimism across a finite candidate family.

All displayed quantities are analytic or exhaustively enumerated.  The SVG is
therefore byte-for-byte reproducible for a fixed command line.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-learning-problem-decision-cumulative-gate-v2.svg"
)

BG = "#f7f8fb"
PANEL = "#ffffff"
INK = "#172033"
MUTED = "#64748b"
GRID = "#d8dee9"
BLUE = "#2f6fed"
GREEN = "#19866f"
ORANGE = "#d97706"
RED = "#d84a4a"
PURPLE = "#7c5ce5"


DEFAULTS = {
    "px": 0.40,
    "eta0": 0.20,
    "eta1": 0.75,
    "sample_size": 6,
    "class_mode": "constant",
    "eta_grid": "0.12,0.38,0.62,0.88",
    "fp_cost": 1.0,
    "fn_cost": 2.0,
    "reject_cost": 0.24,
    "candidate_count": 32,
    "validation_size": 30,
    "base_error": 0.20,
    "delta": 0.05,
}


@dataclass(frozen=True)
class ERMSummary:
    bayes_risk: float
    oracle_risk: float
    approximation: float
    expected_train_risk: float
    expected_population_risk: float
    expected_generalization_gap: float
    expected_class_excess: float
    probability_mass: float
    hypotheses: tuple[tuple[int, int], ...]
    true_risks: tuple[float, ...]


@dataclass(frozen=True)
class DecisionRow:
    eta: float
    risk_zero: float
    risk_reject: float
    risk_one: float
    action: str
    action_risk: float
    zero_one_action: str
    zero_one_deployed_risk: float


@dataclass(frozen=True)
class HoldoutSummary:
    expected_selected_validation: float
    expected_fresh_test: float
    optimism: float
    simultaneous_radius: float
    perfect_selection_probability: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--px", type=float, default=DEFAULTS["px"])
    parser.add_argument("--eta0", type=float, default=DEFAULTS["eta0"])
    parser.add_argument("--eta1", type=float, default=DEFAULTS["eta1"])
    parser.add_argument("--sample-size", type=int, default=DEFAULTS["sample_size"])
    parser.add_argument("--class-mode", choices=("constant", "full"), default=DEFAULTS["class_mode"])
    parser.add_argument("--eta-grid", default=DEFAULTS["eta_grid"])
    parser.add_argument("--fp-cost", type=float, default=DEFAULTS["fp_cost"])
    parser.add_argument("--fn-cost", type=float, default=DEFAULTS["fn_cost"])
    parser.add_argument("--reject-cost", type=float, default=DEFAULTS["reject_cost"])
    parser.add_argument("--candidate-count", type=int, default=DEFAULTS["candidate_count"])
    parser.add_argument("--validation-size", type=int, default=DEFAULTS["validation_size"])
    parser.add_argument("--base-error", type=float, default=DEFAULTS["base_error"])
    parser.add_argument("--delta", type=float, default=DEFAULTS["delta"])
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def validate(args: argparse.Namespace) -> list[float]:
    for name in ("px", "eta0", "eta1", "base_error", "delta"):
        value = getattr(args, name)
        if not 0.0 < value < 1.0:
            raise ValueError(f"--{name.replace('_', '-')} must lie strictly in (0, 1)")
    if not 1 <= args.sample_size <= 24:
        raise ValueError("--sample-size must be in 1..24")
    if args.candidate_count < 1:
        raise ValueError("--candidate-count must be positive")
    if args.validation_size < 1:
        raise ValueError("--validation-size must be positive")
    if args.fp_cost <= 0 or args.fn_cost <= 0 or args.reject_cost < 0:
        raise ValueError("decision costs must be positive, with nonnegative reject cost")
    eta_grid = [float(token.strip()) for token in args.eta_grid.split(",") if token.strip()]
    if len(eta_grid) < 3 or any(not 0.0 < value < 1.0 for value in eta_grid):
        raise ValueError("--eta-grid requires at least three comma-separated probabilities in (0, 1)")
    return eta_grid


def is_canonical(args: argparse.Namespace) -> bool:
    return all(getattr(args, key) == value for key, value in DEFAULTS.items())


def outcome_probabilities(px: float, eta0: float, eta1: float) -> tuple[float, ...]:
    return (
        (1.0 - px) * (1.0 - eta0),
        (1.0 - px) * eta0,
        px * (1.0 - eta1),
        px * eta1,
    )


def hypothesis_risk(hypothesis: tuple[int, int], probabilities: tuple[float, ...]) -> float:
    total = 0.0
    for index, probability in enumerate(probabilities):
        x = index // 2
        y = index % 2
        total += probability * int(hypothesis[x] != y)
    return total


def compositions(total: int, parts: int = 4):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def multinomial_probability(counts: tuple[int, ...], probabilities: tuple[float, ...]) -> float:
    coefficient = math.factorial(sum(counts))
    for count in counts:
        coefficient //= math.factorial(count)
    value = float(coefficient)
    for count, probability in zip(counts, probabilities):
        value *= probability**count
    return value


def empirical_risk(hypothesis: tuple[int, int], counts: tuple[int, ...]) -> float:
    errors = 0
    for index, count in enumerate(counts):
        x = index // 2
        y = index % 2
        errors += count * int(hypothesis[x] != y)
    return errors / sum(counts)


def exact_erm_summary(
    px: float,
    eta0: float,
    eta1: float,
    sample_size: int,
    class_mode: str,
) -> ERMSummary:
    probabilities = outcome_probabilities(px, eta0, eta1)
    bayes = (int(eta0 >= 0.5), int(eta1 >= 0.5))
    bayes_risk = hypothesis_risk(bayes, probabilities)
    hypotheses = ((0, 0), (1, 1)) if class_mode == "constant" else ((0, 0), (0, 1), (1, 0), (1, 1))
    true_risks = tuple(hypothesis_risk(hypothesis, probabilities) for hypothesis in hypotheses)
    oracle_risk = min(true_risks)

    probability_mass = 0.0
    expected_train = 0.0
    expected_population = 0.0
    for counts in compositions(sample_size):
        weight = multinomial_probability(counts, probabilities)
        empirical = tuple(empirical_risk(hypothesis, counts) for hypothesis in hypotheses)
        selected = min(range(len(hypotheses)), key=lambda index: (empirical[index], index))
        probability_mass += weight
        expected_train += weight * empirical[selected]
        expected_population += weight * true_risks[selected]

    if abs(probability_mass - 1.0) > 2e-12:
        raise AssertionError("enumerated sample probability does not sum to one")
    gap = expected_population - expected_train
    class_excess = expected_population - oracle_risk
    if gap < -1e-12 or class_excess < -1e-12:
        raise AssertionError("expected ERM ledger violated")
    return ERMSummary(
        bayes_risk=bayes_risk,
        oracle_risk=oracle_risk,
        approximation=oracle_risk - bayes_risk,
        expected_train_risk=expected_train,
        expected_population_risk=expected_population,
        expected_generalization_gap=gap,
        expected_class_excess=class_excess,
        probability_mass=probability_mass,
        hypotheses=hypotheses,
        true_risks=true_risks,
    )


def decision_rows(
    eta_grid: list[float], fp_cost: float, fn_cost: float, reject_cost: float
) -> list[DecisionRow]:
    rows: list[DecisionRow] = []
    for eta in eta_grid:
        candidates = (
            ("0", fn_cost * eta),
            ("reject", reject_cost),
            ("1", fp_cost * (1.0 - eta)),
        )
        action, action_risk = min(candidates, key=lambda item: (item[1], item[0]))
        zero_one_action = "1" if eta >= 0.5 else "0"
        deployed_risk = fp_cost * (1.0 - eta) if zero_one_action == "1" else fn_cost * eta
        rows.append(
            DecisionRow(
                eta=eta,
                risk_zero=fn_cost * eta,
                risk_reject=reject_cost,
                risk_one=fp_cost * (1.0 - eta),
                action=action,
                action_risk=action_risk,
                zero_one_action=zero_one_action,
                zero_one_deployed_risk=deployed_risk,
            )
        )
    return rows


def binomial_tail(n: int, q: float, threshold: int) -> float:
    return sum(
        math.comb(n, k) * q**k * (1.0 - q) ** (n - k)
        for k in range(threshold, n + 1)
    )


def holdout_summary(k: int, n: int, q: float, delta: float) -> HoldoutSummary:
    expected_min_count = sum(binomial_tail(n, q, threshold) ** k for threshold in range(1, n + 1))
    selected_validation = expected_min_count / n
    radius = math.sqrt(math.log(2.0 * k / delta) / (2.0 * n))
    probability_perfect_one = (1.0 - q) ** n
    probability_perfect_any = 1.0 - (1.0 - probability_perfect_one) ** k
    return HoldoutSummary(
        expected_selected_validation=selected_validation,
        expected_fresh_test=q,
        optimism=q - selected_validation,
        simultaneous_radius=radius,
        perfect_selection_probability=probability_perfect_any,
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_text(x: float, y: float, value: object, size: int = 15, color: str = INK,
             weight: int = 400, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-size="{max(size, 15)}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">'
        f'{esc(value)}</text>'
    )


def rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "none",
         radius: float = 0.0, opacity: float = 1.0) -> str:
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
        f'rx="{radius:.2f}" fill="{fill}" stroke="{stroke}" opacity="{opacity:.3f}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID,
         width: float = 1.0, dash: str | None = None) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width:.2f}"{extra}/>'
    )


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.5) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width:.2f}"/>'


def panel(parts: list[str], x: float, title: str, subtitle: str) -> None:
    parts.append(rect(x, 92, 438, 448, PANEL, GRID, 16))
    parts.append(svg_text(x + 20, 124, title, 18, INK, 700))
    parts.append(svg_text(x + 20, 149, subtitle, 15, MUTED))


def draw_track_a(parts: list[str], x: float, summary: ERMSummary, args: argparse.Namespace) -> None:
    panel(parts, x, "A  对象—风险—选择账本", f"exact enumeration, m={args.sample_size}, H={args.class_mode}")
    labels = ["Bayes", "class", "E pop", "E train"]
    values = [summary.bayes_risk, summary.oracle_risk, summary.expected_population_risk, summary.expected_train_risk]
    colors = [GREEN, BLUE, ORANGE, PURPLE]
    chart_x, chart_y, chart_w, chart_h = x + 52, 184, 330, 190
    top = max(0.5, max(values) * 1.18)
    for tick in range(6):
        value = top * tick / 5
        yy = chart_y + chart_h * (1 - tick / 5)
        parts.append(line(chart_x, yy, chart_x + chart_w, yy))
        parts.append(svg_text(chart_x - 8, yy + 5, f"{value:.2f}", 14, MUTED, 400, "end"))
    bar_w = 54
    for index, (label, value, color) in enumerate(zip(labels, values, colors)):
        bx = chart_x + 25 + index * 78
        bh = chart_h * value / top
        by = chart_y + chart_h - bh
        parts.append(rect(bx, by, bar_w, bh, color, radius=6, opacity=0.9))
        parts.append(svg_text(bx + bar_w / 2, by - 7, f"{value:.3f}", 14, color, 700, "middle"))
        parts.append(svg_text(bx + bar_w / 2, chart_y + chart_h + 23, label, 14, INK, 600, "middle"))
    parts.append(rect(x + 22, 423, 394, 88, "#f3f7ff", radius=10))
    parts.append(svg_text(x + 38, 449, f"approximation = {summary.approximation:.4f}", 15, BLUE, 700))
    parts.append(svg_text(x + 38, 474, f"finite-sample class excess = {summary.expected_class_excess:.4f}", 15, ORANGE, 700))
    parts.append(svg_text(x + 38, 499, f"selection gap = {summary.expected_generalization_gap:.4f}", 15, PURPLE, 700))


def draw_track_b(parts: list[str], x: float, rows: list[DecisionRow], args: argparse.Namespace) -> None:
    panel(parts, x, "B  条件风险与 Bayes 动作", f"cFP={args.fp_cost:g}, cFN={args.fn_cost:g}, reject={args.reject_cost:g}")
    left, top, width, height = x + 58, 180, 320, 150
    maximum = max(max(row.risk_zero, row.risk_one, row.risk_reject) for row in rows) * 1.1
    for tick in range(5):
        value = maximum * tick / 4
        yy = top + height * (1 - tick / 4)
        parts.append(line(left, yy, left + width, yy))
        parts.append(svg_text(left - 8, yy + 5, f"{value:.2f}", 14, MUTED, 400, "end"))
    for color, getter in ((BLUE, lambda row: row.risk_zero), (PURPLE, lambda row: row.risk_reject), (RED, lambda row: row.risk_one)):
        points = []
        for index, row in enumerate(rows):
            xx = left + width * index / (len(rows) - 1)
            yy = top + height * (1 - getter(row) / maximum)
            points.append((xx, yy))
        parts.append(polyline(points, color, 3))
    for index, row in enumerate(rows):
        xx = left + width * index / (len(rows) - 1)
        parts.append(svg_text(xx, top + height + 23, f"η={row.eta:.2f}", 14, INK, 600, "middle"))
        parts.append(svg_text(xx, top + height + 47, row.action, 14, GREEN, 700, "middle"))
    parts.append(svg_text(left, 405, "risk(action 0)", 15, BLUE, 700))
    parts.append(svg_text(left + 120, 405, "reject", 15, PURPLE, 700))
    parts.append(svg_text(left + 210, 405, "risk(action 1)", 15, RED, 700))
    threshold = args.fp_cost / (args.fp_cost + args.fn_cost)
    reject_lo = args.reject_cost / args.fn_cost
    reject_hi = 1.0 - args.reject_cost / args.fp_cost
    parts.append(rect(x + 22, 430, 394, 81, "#f4fbf8", radius=10))
    parts.append(svg_text(x + 38, 459, f"binary cost threshold = {threshold:.3f}", 15, GREEN, 700))
    parts.append(svg_text(x + 38, 488, f"reject interval = ({reject_lo:.3f}, {reject_hi:.3f})", 15, MUTED, 600))


def draw_track_c(parts: list[str], x: float, summary: HoldoutSummary, args: argparse.Namespace) -> None:
    panel(parts, x, "C  验证选择与反馈代价", f"K={args.candidate_count}, nval={args.validation_size}, true error={args.base_error:g}")
    ks = sorted({1, 2, 4, 8, 16, args.candidate_count})
    ks = [value for value in ks if value <= max(args.candidate_count, 16)]
    left, top, width, height = x + 58, 180, 320, 150
    maximum = min(1.0, args.base_error + 0.18)
    for tick in range(5):
        value = maximum * tick / 4
        yy = top + height * (1 - tick / 4)
        parts.append(line(left, yy, left + width, yy))
        parts.append(svg_text(left - 8, yy + 5, f"{value:.2f}", 14, MUTED, 400, "end"))
    selected_points = []
    true_points = []
    for index, k in enumerate(ks):
        local = holdout_summary(k, args.validation_size, args.base_error, args.delta)
        xx = left + width * index / (len(ks) - 1)
        selected_points.append((xx, top + height * (1 - local.expected_selected_validation / maximum)))
        true_points.append((xx, top + height * (1 - args.base_error / maximum)))
        parts.append(svg_text(xx, top + height + 23, str(k), 14, INK, 600, "middle"))
    parts.append(polyline(selected_points, ORANGE, 3))
    parts.append(polyline(true_points, GREEN, 3))
    parts.append(svg_text(left, top - 12, "expected selected validation", 15, ORANGE, 700))
    parts.append(svg_text(left + 224, top - 12, "fresh risk", 15, GREEN, 700))
    parts.append(svg_text(left + width / 2, top + height + 49, "number of inspected candidates K", 14, MUTED, 600, "middle"))
    parts.append(rect(x + 22, 430, 394, 81, "#fff8ef", radius=10))
    parts.append(svg_text(x + 38, 459, f"selection optimism = {summary.optimism:.4f}", 15, ORANGE, 700))
    parts.append(svg_text(x + 38, 488, f"simultaneous radius = {summary.simultaneous_radius:.4f}", 15, RED, 700))


def build_svg(args: argparse.Namespace, erm: ERMSummary, rows: list[DecisionRow], holdout: HoldoutSummary) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="600" viewBox="0 0 1440 600">',
        rect(0, 0, 1440, 600, BG),
        svg_text(38, 42, "学习问题、Bayes 决策与评价反馈：三条不可互换的证据链", 25, INK, 700),
        svg_text(38, 70, "先声明对象与目标风险，再解释选择偏差；改变 loss 或反馈箭头就改变问题合同。", 16, MUTED),
    ]
    draw_track_a(parts, 22, erm, args)
    draw_track_b(parts, 501, rows, args)
    draw_track_c(parts, 980, holdout, args)
    parts.append(svg_text(720, 576, "材料校准图：解析/穷举结果，不是个人学习证据，也不是任意分布上的泛化定理。", 15, MUTED, 500, "middle"))
    parts.append("</svg>\n")
    return "".join(parts)


def print_summary(args: argparse.Namespace, erm: ERMSummary, rows: list[DecisionRow], holdout: HoldoutSummary, output: Path) -> None:
    print("LT-CUM-01 deterministic three-track gate")
    print(
        "TRACK A "
        f"bayes={erm.bayes_risk:.6f} oracle={erm.oracle_risk:.6f} "
        f"approximation={erm.approximation:.6f} expected_population={erm.expected_population_risk:.6f} "
        f"expected_train={erm.expected_train_risk:.6f} selection_gap={erm.expected_generalization_gap:.6f} "
        f"class_excess={erm.expected_class_excess:.6f} mass={erm.probability_mass:.12f}"
    )
    print("TRACK B " + "; ".join(f"eta={row.eta:.3f}:action={row.action}:risk={row.action_risk:.6f}:zero_one={row.zero_one_action}" for row in rows))
    print(
        "TRACK C "
        f"selected_validation={holdout.expected_selected_validation:.6f} fresh={holdout.expected_fresh_test:.6f} "
        f"optimism={holdout.optimism:.6f} radius={holdout.simultaneous_radius:.6f} "
        f"perfect_any={holdout.perfect_selection_probability:.6f}"
    )
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"SVG {output}")
    print(f"SHA256 {digest}")


def main() -> None:
    args = parse_args()
    eta_grid = validate(args)
    canonical = is_canonical(args)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; canonical asset will not be overwritten")
    output = args.output if args.output is not None else DEFAULT_OUTPUT
    erm = exact_erm_summary(args.px, args.eta0, args.eta1, args.sample_size, args.class_mode)
    rows = decision_rows(eta_grid, args.fp_cost, args.fn_cost, args.reject_cost)
    holdout = holdout_summary(args.candidate_count, args.validation_size, args.base_error, args.delta)
    svg = build_svg(args, erm, rows, holdout)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print_summary(args, erm, rows, holdout, output)


if __name__ == "__main__":
    main()
