#!/usr/bin/env python3
"""Deterministic three-track evidence gate for MODEL-CUM-01 (LT-41--52).

Track A joins fixed-design ridge bias/variance, spectral filtering, KRR/GP mean
language and exact holdout selection. Track B joins logistic separation, the
hard-margin SVM, tree splitting, exact bootstrap aggregation and one AdaBoost
round. Track C joins PCA, K-Means, symmetric Gaussian-mixture EM, label
switching and selection criteria. Only the finite fixtures are computed; the
associated universal statements still require proofs in the assessment.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import itertools
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CANONICAL_OUTPUT = (
    ROOT / "00-知识库管理/_assets/plots/learning-theory"
    / "plot-classical-models-cumulative-gate-v2.svg"
)

DEFAULT_SINGULAR = (4.0, 1.0, 0.25)
DEFAULT_BETA = (1.0, 0.8, 0.4)
DEFAULT_TRAIN_SIGNS = (-1, 1, -1)
DEFAULT_LAMBDAS = (0.0, 0.25, 1.0, 4.0)

INK = "#172033"
MUTED = "#5E6B82"
GRID = "#CBD7E6"
BG = "#F5F8FC"
PAPER = "#FFFFFF"
BLUE = "#2F63E9"
TEAL = "#0A9D88"
AMBER = "#BE7812"
RED = "#C84032"
PURPLE = "#7656C7"


@dataclass(frozen=True)
class SpectralSummary:
    singular_values: tuple[float, ...]
    beta: tuple[float, ...]
    sigma: float
    lambdas: tuple[float, ...]
    expected_bias: tuple[float, ...]
    expected_variance: tuple[float, ...]
    expected_excess: tuple[float, ...]
    effective_df: tuple[float, ...]
    best_index: int
    selection_frequencies: tuple[float, ...]
    selected_true_risk: float
    selected_validation_risk: float
    selection_optimism: float


@dataclass(frozen=True)
class SupervisedSummary:
    tree_threshold: float
    gini_gain: float
    svm_weight: float
    svm_intercept: float
    geometric_margin: float
    logistic_loss_c1: float
    logistic_loss_c4: float
    bootstrap_count: int
    query: float
    bag_probability: float
    member_variance: float
    independent_ensemble_variance: float
    correlated_ensemble_variance: float
    ensemble_members: int
    member_correlation: float
    boost_error: float
    boost_alpha: float
    boost_normalizer: float
    hard_example_weight: float


@dataclass(frozen=True)
class LatentSummary:
    pca_top: float
    pca_second: float
    eigengap: float
    top_vector: tuple[float, float]
    kmeans_distortion: float
    em_initial_mean: float
    em_one_step_mean: float
    em_final_mean: float
    em_iterations: int
    em_initial_log_likelihood: float
    em_final_log_likelihood: float
    single_variance: float
    single_aic: float
    single_bic: float
    mixture_aic: float
    mixture_bic: float
    label_swap_defect: float


def csv_floats(raw: str, label: str) -> tuple[float, ...]:
    try:
        values = tuple(float(piece.strip()) for piece in raw.split(",") if piece.strip())
    except ValueError as exc:
        raise SystemExit(f"{label} must be a comma-separated numeric list") from exc
    if not values or any(not math.isfinite(value) for value in values):
        raise SystemExit(f"{label} must contain finite values")
    return values


def csv_signs(raw: str) -> tuple[int, ...]:
    values = csv_floats(raw, "train-signs")
    if any(value not in (-1.0, 1.0) for value in values):
        raise SystemExit("train-signs entries must be -1 or 1")
    return tuple(int(value) for value in values)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--singular-values", default="4,1,0.25")
    parser.add_argument("--beta", default="1,0.8,0.4")
    parser.add_argument("--train-signs", default="-1,1,-1")
    parser.add_argument("--lambdas", default="0,0.25,1,4")
    parser.add_argument("--sigma", type=float, default=0.5)
    parser.add_argument("--query", type=float, default=-2.25)
    parser.add_argument("--ensemble-members", type=int, default=25)
    parser.add_argument("--member-correlation", type=float, default=0.2)
    parser.add_argument("--em-initial-mean", type=float, default=1.0)
    parser.add_argument("--em-tolerance", type=float, default=1e-12)
    parser.add_argument("--em-max-iterations", type=int, default=100)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def validate(
    args: argparse.Namespace,
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[int, ...], tuple[float, ...]]:
    singular = csv_floats(args.singular_values, "singular-values")
    beta = csv_floats(args.beta, "beta")
    signs = csv_signs(args.train_signs)
    lambdas = csv_floats(args.lambdas, "lambdas")
    if not (len(singular) == len(beta) == len(signs)):
        raise SystemExit("singular-values, beta and train-signs must have equal length")
    if not 1 <= len(singular) <= 10:
        raise SystemExit("spectral dimension must lie in 1..10")
    if any(value <= 0 for value in singular):
        raise SystemExit("singular-values must be positive")
    if not 0 < args.sigma <= 5:
        raise SystemExit("sigma must lie in (0,5]")
    if not 2 <= len(lambdas) <= 12:
        raise SystemExit("lambdas must contain 2..12 candidates")
    if any(value < 0 for value in lambdas):
        raise SystemExit("lambdas must be nonnegative")
    if len(set(lambdas)) != len(lambdas):
        raise SystemExit("lambdas must be distinct")
    if not -4 <= args.query <= 4:
        raise SystemExit("query must lie in [-4,4]")
    if not 1 <= args.ensemble_members <= 10_000:
        raise SystemExit("ensemble-members must lie in 1..10000")
    if not 0 <= args.member_correlation <= 1:
        raise SystemExit("member-correlation must lie in [0,1]")
    if not 0 < args.em_initial_mean <= 5:
        raise SystemExit("em-initial-mean must lie in (0,5]")
    if not 0 < args.em_tolerance < 1:
        raise SystemExit("em-tolerance must lie in (0,1)")
    if not 1 <= args.em_max_iterations <= 10_000:
        raise SystemExit("em-max-iterations must lie in 1..10000")
    return singular, beta, signs, lambdas


def is_canonical(
    args: argparse.Namespace,
    singular: tuple[float, ...],
    beta: tuple[float, ...],
    signs: tuple[int, ...],
    lambdas: tuple[float, ...],
) -> bool:
    return (
        singular == DEFAULT_SINGULAR
        and beta == DEFAULT_BETA
        and signs == DEFAULT_TRAIN_SIGNS
        and lambdas == DEFAULT_LAMBDAS
        and args.sigma == 0.5
        and args.query == -2.25
        and args.ensemble_members == 25
        and args.member_correlation == 0.2
        and args.em_initial_mean == 1.0
        and args.em_tolerance == 1e-12
        and args.em_max_iterations == 100
    )


def spectral_summary(
    singular: tuple[float, ...],
    beta: tuple[float, ...],
    signs: tuple[int, ...],
    lambdas: tuple[float, ...],
    sigma: float,
) -> SpectralSummary:
    biases: list[float] = []
    variances: list[float] = []
    degrees: list[float] = []
    for ridge in lambdas:
        biases.append(sum(
            (ridge / (value * value + ridge)) ** 2 * coefficient * coefficient
            for value, coefficient in zip(singular, beta)
        ))
        variances.append(sum(
            sigma * sigma * value * value / (value * value + ridge) ** 2
            for value in singular
        ))
        degrees.append(sum(
            value * value / (value * value + ridge) for value in singular
        ))
    excess = tuple(left + right for left, right in zip(biases, variances))
    best = min(range(len(lambdas)), key=lambda index: (excess[index], index))

    # A frozen training realization produces fixed candidate predictors before
    # the independent validation response is drawn.
    sufficient = tuple(
        coefficient + sigma * sign / value
        for value, coefficient, sign in zip(singular, beta, signs)
    )
    predictions = tuple(tuple(
        value * value / (value * value + ridge) * statistic
        for value, statistic in zip(singular, sufficient)
    ) for ridge in lambdas)
    dimension = len(beta)
    true_risks = tuple(
        sum((prediction - coefficient) ** 2 for prediction, coefficient in zip(candidate, beta))
        / dimension
        + sigma * sigma
        for candidate in predictions
    )
    selection_counts = [0] * len(lambdas)
    selected_true = 0.0
    selected_validation = 0.0
    for validation_signs in itertools.product((-1, 1), repeat=dimension):
        validation_response = tuple(
            coefficient + sigma * sign
            for coefficient, sign in zip(beta, validation_signs)
        )
        validation_risks = tuple(
            sum((prediction - response) ** 2
                for prediction, response in zip(candidate, validation_response)) / dimension
            for candidate in predictions
        )
        chosen = min(range(len(lambdas)), key=lambda index: (validation_risks[index], index))
        selection_counts[chosen] += 1
        selected_true += true_risks[chosen]
        selected_validation += validation_risks[chosen]
    validation_count = 2**dimension
    selected_true /= validation_count
    selected_validation /= validation_count
    return SpectralSummary(
        singular,
        beta,
        sigma,
        lambdas,
        tuple(biases),
        tuple(variances),
        excess,
        tuple(degrees),
        best,
        tuple(count / validation_count for count in selection_counts),
        selected_true,
        selected_validation,
        selected_true - selected_validation,
    )


def gini(labels: tuple[int, ...]) -> float:
    if not labels:
        return 0.0
    probability = sum(labels) / len(labels)
    return 2 * probability * (1 - probability)


def supervised_summary(
    query: float,
    ensemble_members: int,
    member_correlation: float,
) -> SupervisedSummary:
    points = (-3.0, -2.0, -1.0, 1.0, 2.0, 3.0)
    labels = (0, 0, 1, 1, 1, 1)
    thresholds = (-4.0, -2.5, -1.5, 0.0, 1.5, 2.5, 4.0)
    base_impurity = gini(labels)
    gains: list[float] = []
    for threshold in thresholds:
        left = tuple(label for point, label in zip(points, labels) if point < threshold)
        right = tuple(label for point, label in zip(points, labels) if point >= threshold)
        weighted = (len(left) * gini(left) + len(right) * gini(right)) / len(points)
        gains.append(base_impurity - weighted)
    best_tree = max(range(len(thresholds)), key=lambda index: (gains[index], -index))

    # The two closest opposite-class points are -2 and -1. In canonical
    # hard-margin normalization y(wx+b)>=1 they imply w=2,b=3.
    svm_weight, svm_intercept = 2.0, 3.0
    signed_labels = tuple(2 * label - 1 for label in labels)
    margins = tuple(
        signed * (svm_weight * point + svm_intercept)
        for point, signed in zip(points, signed_labels)
    )
    logistic_c1 = sum(math.log1p(math.exp(-margin)) for margin in margins) / len(points)
    logistic_c4 = sum(math.log1p(math.exp(-4 * margin)) for margin in margins) / len(points)

    output_positive = 0
    bootstrap_count = len(points) ** len(points)
    for indices in itertools.product(range(len(points)), repeat=len(points)):
        errors = tuple(
            sum(int(points[index] >= threshold) != labels[index] for index in indices)
            for threshold in thresholds
        )
        chosen = min(range(len(thresholds)), key=lambda index: (errors[index], index))
        output_positive += int(query >= thresholds[chosen])
    probability = output_positive / bootstrap_count
    member_variance = probability * (1 - probability)
    independent_variance = member_variance / ensemble_members
    correlated_variance = member_variance * (
        member_correlation + (1 - member_correlation) / ensemble_members
    )

    stump_predictions = tuple(int(point >= 0) for point in points)
    boost_error = sum(prediction != label for prediction, label in zip(stump_predictions, labels)) / len(points)
    boost_alpha = 0.5 * math.log((1 - boost_error) / boost_error)
    raw_weights = tuple(
        math.exp(-boost_alpha * signed * (2 * prediction - 1))
        for signed, prediction in zip(signed_labels, stump_predictions)
    )
    normalizer = sum(raw_weights) / len(points)
    normalized_weights = tuple(weight / sum(raw_weights) for weight in raw_weights)
    return SupervisedSummary(
        thresholds[best_tree],
        gains[best_tree],
        svm_weight,
        svm_intercept,
        1 / abs(svm_weight),
        logistic_c1,
        logistic_c4,
        bootstrap_count,
        query,
        probability,
        member_variance,
        independent_variance,
        correlated_variance,
        ensemble_members,
        member_correlation,
        boost_error,
        boost_alpha,
        normalizer,
        max(normalized_weights),
    )


def mixture_log_likelihood(observations: tuple[float, ...], mean: float) -> float:
    normalizer = math.sqrt(2 * math.pi)
    return sum(math.log(
        0.5 * math.exp(-0.5 * (value + mean) ** 2) / normalizer
        + 0.5 * math.exp(-0.5 * (value - mean) ** 2) / normalizer
    ) for value in observations)


def em_update(observations: tuple[float, ...], mean: float) -> float:
    responsibilities = tuple(
        1 / (1 + math.exp(-2 * mean * value)) for value in observations
    )
    return sum(weight * value for weight, value in zip(responsibilities, observations)) / sum(responsibilities)


def latent_summary(initial_mean: float, tolerance: float, max_iterations: int) -> LatentSummary:
    # Centered 2D points: covariance [[14/3,2],[2,1]].
    trace = 17 / 3
    discriminant = math.sqrt(265) / 3
    top = (trace + discriminant) / 2
    second = (trace - discriminant) / 2
    unnormalized = (1.0, (top - 14 / 3) / 2)
    norm = math.hypot(*unnormalized)
    top_vector = (unnormalized[0] / norm, unnormalized[1] / norm)
    kmeans_distortion = 2 / 3

    observations = (-3.0, -2.0, -1.0, 1.0, 2.0, 3.0)
    one_step = em_update(observations, initial_mean)
    mean = initial_mean
    iterations = 0
    for iterations in range(1, max_iterations + 1):
        updated = em_update(observations, mean)
        if abs(updated - mean) <= tolerance:
            mean = updated
            break
        mean = updated
    else:
        raise SystemExit("EM did not converge within em-max-iterations")

    initial_ll = mixture_log_likelihood(observations, initial_mean)
    final_ll = mixture_log_likelihood(observations, mean)
    single_variance = sum(value * value for value in observations) / len(observations)
    single_ll = sum(
        -0.5 * (math.log(2 * math.pi * single_variance) + value * value / single_variance)
        for value in observations
    )
    sample_size = len(observations)
    # M1 has free mean/variance (2 parameters). M2 is the deliberately
    # constrained symmetric, equal-weight, unit-variance family (1 parameter).
    single_aic = -2 * single_ll + 2 * 2
    single_bic = -2 * single_ll + 2 * math.log(sample_size)
    mixture_aic = -2 * final_ll + 2
    mixture_bic = -2 * final_ll + math.log(sample_size)
    label_swap_defect = abs(final_ll - mixture_log_likelihood(observations, -mean))
    return LatentSummary(
        top,
        second,
        discriminant,
        top_vector,
        kmeans_distortion,
        initial_mean,
        one_step,
        mean,
        iterations,
        initial_ll,
        final_ll,
        single_variance,
        single_aic,
        single_bic,
        mixture_aic,
        mixture_bic,
        label_swap_defect,
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, size: int = 14, color: str = INK,
         weight: int = 500, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">'
        f'{esc(value)}</text>'
    )


def rect(x: float, y: float, width: float, height: float, fill: str = PAPER,
         stroke: str = GRID, radius: float = 12, stroke_width: float = 1.5) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID,
         width: float = 2, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}"{dash_attr}/>'
    )


def build_svg(spectral: SpectralSummary, supervised: SupervisedSummary,
              latent: LatentSummary) -> str:
    width, height = 1540, 1010
    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG, BG, 0, 0),
        text(70, 60, "Classical models | three estimands, three algorithms, one selection ledger", 27, INK, 750),
        text(70, 91, "spectral supervised risk  ->  margins / partitions / ensembles  ->  latent geometry / identifiability", 16, MUTED, 500),
    ]
    panel_y, panel_h, panel_w = 130, 600, 450
    xs = (70, 545, 1020)
    headers = (
        ("A | spectral procedure", "ridge risk + exact validation selection", BLUE),
        ("B | boundary and ensemble", "logistic / SVM / tree / bagging / boost", AMBER),
        ("C | latent geometry", "PCA / K-Means / EM / model choice", TEAL),
    )
    for x, (title, subtitle, color) in zip(xs, headers):
        items.extend((
            rect(x, panel_y, panel_w, panel_h, PAPER, GRID, 16, 1.5),
            rect(x, panel_y, panel_w, 7, color, color, 4, 0),
            text(x + 24, panel_y + 48, title, 20, INK, 740),
            text(x + 24, panel_y + 73, subtitle, 13, MUTED, 500),
        ))

    # Track A: stacked ridge bias/variance bars and validation selection.
    ax = xs[0]
    items.append(text(ax + 24, panel_y + 111, f"s={spectral.singular_values}  sigma={spectral.sigma:g}", 13, INK, 650))
    chart_x, chart_y, chart_w, chart_h = ax + 45, panel_y + 155, 355, 210
    items.append(line(chart_x, chart_y + chart_h, chart_x + chart_w, chart_y + chart_h, GRID, 1.5))
    maximum = max(spectral.expected_excess)
    slot = chart_w / len(spectral.lambdas)
    for index, ridge in enumerate(spectral.lambdas):
        variance_height = chart_h * spectral.expected_variance[index] / maximum
        bias_height = chart_h * spectral.expected_bias[index] / maximum
        left = chart_x + index * slot + 13
        width_bar = slot - 26
        items.append(rect(left, chart_y + chart_h - variance_height, width_bar, variance_height, BLUE, BLUE, 2, 0))
        items.append(rect(left, chart_y + chart_h - variance_height - bias_height, width_bar, bias_height, AMBER, AMBER, 2, 0))
        items.append(text(left + width_bar / 2, chart_y + chart_h + 22, f"l={ridge:g}", 11, MUTED, 600, "middle"))
        items.append(text(left + width_bar / 2, chart_y + chart_h - variance_height - bias_height - 7,
                          f"{spectral.expected_excess[index]:.3f}", 11,
                          TEAL if index == spectral.best_index else INK, 700, "middle"))
    best = spectral.best_index
    items.append(text(ax + 24, panel_y + 414,
                      f"best expected excess: lambda={spectral.lambdas[best]:g}, risk={spectral.expected_excess[best]:.4f}",
                      14, TEAL, 730))
    items.append(text(ax + 24, panel_y + 443, f"effective df={spectral.effective_df[best]:.4f}", 13, INK, 620))
    freq = ", ".join(f"{ridge:g}:{value:.3f}" for ridge, value in zip(spectral.lambdas, spectral.selection_frequencies))
    items.append(rect(ax + 24, panel_y + 472, panel_w - 48, 91, "#F7FAFF", GRID, 9, 1))
    items.append(text(ax + 40, panel_y + 499, "exact validation-selection ledger", 13, BLUE, 740))
    items.append(text(ax + 40, panel_y + 525, f"selection frequency  {freq}", 11, INK, 600))
    items.append(text(ax + 40, panel_y + 550,
                      f"true={spectral.selected_true_risk:.4f}  min-val={spectral.selected_validation_risk:.4f}  optimism={spectral.selection_optimism:.4f}",
                      11, RED, 700))
    items.append(text(ax + 24, panel_y + 584, "Blue=variance, amber=bias; selection uses a separate random response.", 11, MUTED, 600))

    # Track B: object ladder plus exact ensemble values.
    bx = xs[1]
    rows = (
        ("logistic ray", f"loss c=1: {supervised.logistic_loss_c1:.4f} -> c=4: {supervised.logistic_loss_c4:.4f}", PURPLE),
        ("hard-margin SVM", f"w={supervised.svm_weight:.1f}, b={supervised.svm_intercept:.1f}, margin={supervised.geometric_margin:.2f}", BLUE),
        ("best tree split", f"t={supervised.tree_threshold:.1f}, Gini gain={supervised.gini_gain:.4f}", AMBER),
        ("exact bagging", f"P(h({supervised.query:g})=1)={supervised.bag_probability:.4f}", TEAL),
        ("AdaBoost round 1", f"err={supervised.boost_error:.4f}, alpha={supervised.boost_alpha:.4f}", RED),
    )
    y = panel_y + 115
    for label, detail, color in rows:
        items.append(rect(bx + 24, y - 20, panel_w - 48, 66, "#F8FAFD", GRID, 8, 1))
        items.append(text(bx + 40, y + 4, label, 13, color, 740))
        items.append(text(bx + 40, y + 29, detail, 12, INK, 600))
        y += 80
    items.append(rect(bx + 24, panel_y + 510, panel_w - 48, 68, "#FFF9EE", "#E8C98E", 9, 1))
    items.append(text(bx + 40, panel_y + 537,
                      f"member var={supervised.member_variance:.4f}; B={supervised.ensemble_members}", 12, INK, 650))
    items.append(text(bx + 40, panel_y + 562,
                      f"independent={supervised.independent_ensemble_variance:.4f}; rho={supervised.member_correlation:g} -> {supervised.correlated_ensemble_variance:.4f}",
                      12, RED, 700))
    items.append(text(bx + 24, panel_y + 584, "Same labels; different estimands, losses, algorithms and outputs.", 11, MUTED, 600))

    # Track C: PCA/KMeans/EM/selection values.
    cx = xs[2]
    items.append(text(cx + 24, panel_y + 111, "six symmetric points; 2D geometry and 1D latent projection", 13, INK, 650))
    latent_rows = (
        ("PCA spectrum", f"{latent.pca_top:.4f}, {latent.pca_second:.4f}; gap={latent.eigengap:.4f}", BLUE),
        ("K-Means K=2", f"distortion={latent.kmeans_distortion:.4f}; labels swap", AMBER),
        ("EM one step", f"mu {latent.em_initial_mean:g} -> {latent.em_one_step_mean:.4f}", TEAL),
        ("EM fixed point", f"mu={latent.em_final_mean:.4f}; iterations={latent.em_iterations}", PURPLE),
    )
    y = panel_y + 155
    for label, detail, color in latent_rows:
        items.append(rect(cx + 24, y - 21, panel_w - 48, 68, "#F8FAFD", GRID, 8, 1))
        items.append(text(cx + 40, y + 4, label, 13, color, 740))
        items.append(text(cx + 40, y + 30, detail, 12, INK, 600))
        y += 82
    items.append(rect(cx + 24, panel_y + 474, panel_w - 48, 112, "#F3FBF8", "#A9DACE", 9, 1))
    items.append(text(cx + 40, panel_y + 503, "selection arithmetic (declared candidate families)", 12, TEAL, 740))
    items.append(text(cx + 40, panel_y + 531,
                      f"single Gaussian AIC/BIC  {latent.single_aic:.3f} / {latent.single_bic:.3f}", 12, INK, 600))
    items.append(text(cx + 40, panel_y + 558,
                      f"symmetric mixture AIC/BIC  {latent.mixture_aic:.3f} / {latent.mixture_bic:.3f}", 12, INK, 600))
    items.append(text(cx + 24, panel_y + 584, "A score comparison is not semantic recovery or post-selection inference.", 11, RED, 650))

    # Bottom cross-model audit spine.
    items.append(rect(70, 760, 1400, 178, PAPER, GRID, 16, 1.5))
    items.append(text(94, 799, "The six-layer classical-model audit", 19, INK, 740))
    stages = (
        ("estimand", "prediction / probability / subspace / density", BLUE),
        ("procedure", "loss + regularizer + optimizer + tie-break", AMBER),
        ("selection", "candidate family + split + search transcript", PURPLE),
        ("deployment", "refit predictor + shift + utility", TEAL),
    )
    for index, (stage, detail, color) in enumerate(stages):
        x = 94 + index * 340
        items.append(text(x, 837, stage, 14, color, 740))
        items.append(text(x, 864, detail, 11, INK, 600))
        if index < 3:
            items.append(text(x + 308, 852, "->", 18, MUTED, 700, "middle"))
    items.append(line(94, 885, 1445, 885, GRID, 1))
    items.append(text(94, 914,
                      "Evidence rule: optimization descent != population validity; best validation score != unbiased final risk; parameter identity != predictive identity.",
                      13, RED, 700))
    items.append(text(1470, 982, "MODEL-CUM-01 | deterministic finite fixtures", 12, MUTED, 500, "end"))
    items.append("</svg>")
    return "\n".join(items) + "\n"


def print_summary(output: Path, spectral: SpectralSummary,
                  supervised: SupervisedSummary, latent: LatentSummary) -> None:
    best = spectral.best_index
    selection = ",".join(
        f"{ridge:g}:{frequency:.6f}"
        for ridge, frequency in zip(spectral.lambdas, spectral.selection_frequencies)
    )
    print(
        "TRACK A "
        f"dim={len(spectral.beta)} sigma={spectral.sigma:.6f} "
        f"ols_expected={spectral.expected_excess[0]:.6f} "
        f"best_lambda={spectral.lambdas[best]:.6f} best_expected={spectral.expected_excess[best]:.6f} "
        f"df={spectral.effective_df[best]:.6f} selection={selection} "
        f"selected_true={spectral.selected_true_risk:.6f} "
        f"selected_val={spectral.selected_validation_risk:.6f} optimism={spectral.selection_optimism:.6f}"
    )
    print(
        "TRACK B "
        f"tree_threshold={supervised.tree_threshold:.6f} gini_gain={supervised.gini_gain:.6f} "
        f"svm_w={supervised.svm_weight:.6f} svm_b={supervised.svm_intercept:.6f} "
        f"margin={supervised.geometric_margin:.6f} logistic_c1={supervised.logistic_loss_c1:.6f} "
        f"logistic_c4={supervised.logistic_loss_c4:.6f} bootstrap={supervised.bootstrap_count} "
        f"query={supervised.query:.6f} bag_prob={supervised.bag_probability:.6f} "
        f"member_var={supervised.member_variance:.6f} independent_var={supervised.independent_ensemble_variance:.6f} "
        f"correlated_var={supervised.correlated_ensemble_variance:.6f} "
        f"boost_error={supervised.boost_error:.6f} alpha={supervised.boost_alpha:.6f} "
        f"boost_z={supervised.boost_normalizer:.6f} "
        f"hard_weight={supervised.hard_example_weight:.6f}"
    )
    print(
        "TRACK C "
        f"pca_top={latent.pca_top:.6f} pca_second={latent.pca_second:.6f} eigengap={latent.eigengap:.6f} "
        f"top_vector={latent.top_vector[0]:.6f},{latent.top_vector[1]:.6f} "
        f"kmeans={latent.kmeans_distortion:.6f} em_one={latent.em_one_step_mean:.6f} "
        f"em_final={latent.em_final_mean:.6f} em_iterations={latent.em_iterations} "
        f"em_gain={latent.em_final_log_likelihood - latent.em_initial_log_likelihood:.6f} "
        f"single_aic={latent.single_aic:.6f} mix_aic={latent.mixture_aic:.6f} "
        f"single_bic={latent.single_bic:.6f} mix_bic={latent.mixture_bic:.6f} "
        f"label_swap={latent.label_swap_defect:.6f}"
    )
    print(f"SVG {output}")
    print(f"SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


def main() -> None:
    args = parse_args()
    singular, beta, signs, lambdas = validate(args)
    canonical = is_canonical(args, singular, beta, signs, lambdas)
    if not canonical and args.output is None:
        raise SystemExit("noncanonical parameters require --output; refusing to overwrite canonical SVG")
    output = (args.output if args.output is not None else CANONICAL_OUTPUT).resolve()
    if not canonical and output == CANONICAL_OUTPUT.resolve():
        raise SystemExit("noncanonical parameters may not target the canonical SVG")

    spectral = spectral_summary(singular, beta, signs, lambdas, args.sigma)
    supervised = supervised_summary(args.query, args.ensemble_members, args.member_correlation)
    latent = latent_summary(args.em_initial_mean, args.em_tolerance, args.em_max_iterations)
    if spectral.selection_optimism < -1e-12:
        raise AssertionError("selection optimism calibration became negative")
    if latent.em_final_log_likelihood + 1e-12 < latent.em_initial_log_likelihood:
        raise AssertionError("EM likelihood monotonicity failed")
    if latent.label_swap_defect > 1e-12:
        raise AssertionError("label-switching likelihood invariance failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(spectral, supervised, latent), encoding="utf-8")
    print_summary(output, spectral, supervised, latent)


if __name__ == "__main__":
    main()
