#!/usr/bin/env python3
"""Audit the migrated OPT teaching contracts and their exact teaching models."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OPT = ROOT / "10-数学基础" / "10.7-优化与凸分析"
LABS = ROOT / "00-知识库管理" / "_labs"
FIGURE_SCRIPTS = (
    LABS / "code" / "plot_convex_foundations_v2.py",
    LABS / "code" / "plot_first_order_optimization_v2.py",
    LABS / "code" / "plot_metric_constrained_optimization_v2.py",
)

CONCEPTS = (
    "优化问题、可行域与局部最优.md",
    "凸集、凸组合与分离超平面.md",
    "凸函数、Jensen 不等式与上图集.md",
    "次梯度、共轭函数与 Fenchel 对偶.md",
    "光滑性、强凸性与条件数.md",
    "一阶最优性条件与梯度下降.md",
    "加速梯度、动量与下界.md",
    "随机梯度与小批量估计.md",
    "自适应优化方法.md",
    "Newton 法、Gauss-Newton 与拟 Newton 法.md",
    "投影、约束与可行方向.md",
    "Lagrange 乘子与 KKT 条件.md",
)

CONTRACT_MARKERS = (
    "课程位置",
    "建议两遍阅读",
    "本章的推导问题链",
    "符号与对象账本",
    "核心公式七问",
    "第一遍停靠线",
)

FIGURE_HASHES = {
    "fig-optimization-problem-solution-concepts-v2.svg":
        "01b11f6ac5f8adcdffad5a4a0a42bcb207d64143361c1864540a8c73870e689b",
    "fig-convex-sets-separation-v2.svg":
        "14c5dd54a595360f7132c5f945aee9bde48acce5189b7451c008b94c13d84e7c",
    "fig-convex-functions-jensen-epigraph-v2.svg":
        "e388c5488a2db17c96aa92826f66b463a32051d1d20852430c289617eca621c2",
    "fig-subgradient-conjugate-fenchel-v2.svg":
        "17dc468cd01e44c5b673b7606d774e8a3cba1646f082cac10aeb8a4ca95208fa",
    "fig-smooth-strong-convex-condition-v2.svg":
        "0cb0a46ff744303cab3565efa2f73bdf7c4a43a4c4f172e450cddb27cf47048b",
    "fig-gradient-descent-rates-v2.svg":
        "9d3ac4346896f708d7068bbd9e23792a6299dd6512c668ce42eb97114a7bff10",
    "fig-acceleration-momentum-lower-bound-v2.svg":
        "3c27f3f79ccdb9965da1f4041f326e0fcfd13169482d4f3f7b0f3876da623a31",
    "fig-sgd-minibatch-noise-v2.svg":
        "da3a41142507540659f64eb8253d3cdb045cf93388b4781e69eb12515363f80a",
    "fig-adaptive-optimizers-geometry-v2.svg":
        "65703f1caf647ab7058c5faaaa0cd350f0fc6cbb886ec0fc647f751de6aae973",
    "fig-newton-gn-quasinewton-v2.svg":
        "36f334323e3269e38f6c28c1180dcd070d63e4b8fe9bf921f259573e7dbdccd2",
    "fig-projection-feasible-directions-v2.svg":
        "2f2f162a489999c94667905f7fe5ccbdb1449d286ce8bf078f7826b5d92482d6",
    "fig-lagrange-kkt-v2.svg":
        "044f9e3ed47598775205cb36d022db9408f0abd0d58983f4c894516d0b777aca",
}

FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "optimization"
KNOWN_EXTENSIONS = {".md", ".py", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def active_lines(text: str) -> list[str]:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue
        if not in_fence:
            output.append(line)
    return output


def add(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]):
    return first[0] + second[0], first[1] + second[1]


def sub(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]):
    return first[0] - second[0], first[1] - second[1]


def scale(value: Fraction, vector: tuple[Fraction, Fraction]):
    return value * vector[0], value * vector[1]


def dot(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]) -> Fraction:
    return first[0] * second[0] + first[1] * second[1]


def squared_norm(vector: tuple[Fraction, Fraction]) -> Fraction:
    return dot(vector, vector)


def q(point: tuple[Fraction, Fraction], target: tuple[Fraction, Fraction]) -> Fraction:
    return Fraction(1, 2) * squared_norm(sub(point, target))


def audit_contracts() -> None:
    for filename in CONCEPTS:
        text = read(OPT / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in text, f"{filename}: migration date not recorded")
    print(f"PASS OPT teaching contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_exact_model() -> None:
    zero = (Fraction(0), Fraction(0))
    e1 = (Fraction(1), Fraction(0))
    e2 = (Fraction(0), Fraction(1))
    vertices = (zero, e1, e2)
    target = (Fraction(1), Fraction(1))
    optimizer = (Fraction(1, 2), Fraction(1, 2))
    residual = sub(target, optimizer)

    require(q(optimizer, target) == Fraction(1, 4), "primal optimum changed")
    require(residual == (Fraction(1, 2), Fraction(1, 2)), "projection residual changed")

    for vertex in vertices:
        require(
            dot(residual, sub(vertex, optimizer)) <= 0,
            f"projection variational inequality fails at vertex {vertex}",
        )
        require(q(vertex, target) >= q(optimizer, target), f"vertex beats optimizer: {vertex}")

    midpoint = scale(Fraction(1, 2), add(e1, e2))
    jensen_gap = (
        Fraction(1, 2) * q(e1, target)
        + Fraction(1, 2) * q(e2, target)
        - q(midpoint, target)
    )
    require(midpoint == optimizer, "Jensen midpoint no longer matches optimizer")
    require(jensen_gap == Fraction(1, 4), "exact Jensen gap changed")

    support_at_residual = max(dot(residual, vertex) for vertex in vertices)
    require(support_at_residual == Fraction(1, 2), "triangle support function changed")
    require(
        support_at_residual == dot(residual, optimizer),
        "indicator Fenchel-Young equality does not close",
    )

    negative_residual = scale(Fraction(-1), residual)
    q_star_negative_residual = dot(target, negative_residual) + Fraction(1, 2) * squared_norm(
        negative_residual
    )
    dual_value = -q_star_negative_residual - support_at_residual
    require(q_star_negative_residual == Fraction(-3, 4), "quadratic conjugate value changed")
    require(dual_value == Fraction(1, 4), "dual optimum certificate changed")
    require(dual_value == q(optimizer, target), "primal-dual gap is not zero")

    print(
        "PASS exact model: x*=(1/2,1/2), p*=1/4, projection VI, "
        "Jensen gap=1/4, Fenchel dual gap=0"
    )


def audit_exact_spectral_model() -> None:
    hessian = (Fraction(1), Fraction(4))
    initial = (Fraction(1), Fraction(1))

    def spectral_q(point: tuple[Fraction, Fraction]) -> Fraction:
        return Fraction(1, 2) * (
            hessian[0] * point[0] ** 2 + hessian[1] * point[1] ** 2
        )

    gradient = (hessian[0] * initial[0], hessian[1] * initial[1])
    require(spectral_q(initial) == Fraction(5, 2), "spectral initial objective changed")
    require(squared_norm(gradient) == Fraction(17), "spectral initial gradient changed")
    require(min(hessian) == 1 and max(hessian) == 4, "mu/L calibration changed")

    safe_step = Fraction(1, 4)
    safe_factors = tuple(Fraction(1) - safe_step * value for value in hessian)
    safe_iterate = (safe_factors[0] * initial[0], safe_factors[1] * initial[1])
    require(safe_factors == (Fraction(3, 4), Fraction(0)), "1/L factors changed")
    require(safe_iterate == (Fraction(3, 4), Fraction(0)), "1/L iterate changed")
    require(spectral_q(safe_iterate) == Fraction(9, 32), "1/L objective changed")
    require(
        spectral_q(safe_iterate) / spectral_q(initial) == Fraction(9, 80),
        "1/L objective ratio changed",
    )

    balanced_step = Fraction(2, 5)
    balanced_factors = tuple(Fraction(1) - balanced_step * value for value in hessian)
    balanced_iterate = (
        balanced_factors[0] * initial[0],
        balanced_factors[1] * initial[1],
    )
    require(balanced_factors == (Fraction(3, 5), Fraction(-3, 5)), "balanced factors changed")
    require(spectral_q(balanced_iterate) == Fraction(9, 10), "balanced objective changed")
    require(
        spectral_q(balanced_iterate) / spectral_q(initial) == Fraction(9, 25),
        "balanced objective ratio changed",
    )

    hb_step = Fraction(4, 9)
    hb_momentum = Fraction(1, 9)
    hb_coefficients = tuple(Fraction(1) + hb_momentum - hb_step * value for value in hessian)
    hb_roots = tuple(coefficient / 2 for coefficient in hb_coefficients)
    for coefficient in hb_coefficients:
        require(coefficient**2 - 4 * hb_momentum == 0, "heavy-ball endpoint is not a double root")
    require(hb_coefficients == (Fraction(2, 3), Fraction(-2, 3)), "HB coefficients changed")
    require(hb_roots == (Fraction(1, 3), Fraction(-1, 3)), "HB roots changed")

    trace_h = sum(hessian)
    noise_injection = safe_step**2 * trace_h / 2
    stationary_variances = tuple(
        safe_step / (value * (2 - safe_step * value)) for value in hessian
    )
    stationary_objective = Fraction(1, 2) * sum(
        value * variance for value, variance in zip(hessian, stationary_variances)
    )
    require(noise_injection == Fraction(5, 32), "SGD injection coefficient changed")
    require(
        stationary_variances == (Fraction(1, 7), Fraction(1, 16)),
        "SGD stationary variances changed",
    )
    require(stationary_objective == Fraction(11, 56), "SGD objective floor changed")

    print(
        "PASS exact spectral model: mu=1, L=4, GD factors, HB roots=±1/3, "
        "SGD injection=5/32 and floor=11/56 (times sigma^2/B)"
    )


def audit_exact_constrained_model() -> None:
    hessian = (Fraction(1), Fraction(4))
    linear = (Fraction(1), Fraction(5, 2))
    zero = (Fraction(0), Fraction(0))
    unconstrained = (linear[0] / hessian[0], linear[1] / hessian[1])
    optimizer = (Fraction(1, 2), Fraction(1, 2))

    def objective(point: tuple[Fraction, Fraction]) -> Fraction:
        quadratic = hessian[0] * point[0] ** 2 + hessian[1] * point[1] ** 2
        return Fraction(1, 2) * quadratic - dot(linear, point)

    def gradient(point: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return hessian[0] * point[0] - linear[0], hessian[1] * point[1] - linear[1]

    require(unconstrained == (Fraction(1), Fraction(5, 8)), "unconstrained Newton point changed")
    require(sum(unconstrained) == Fraction(13, 8), "unconstrained feasibility audit changed")
    require(objective(unconstrained) == Fraction(-41, 32), "unconstrained objective changed")
    require(objective(optimizer) == Fraction(-9, 8), "constrained objective changed")
    require(gradient(optimizer) == (Fraction(-1, 2), Fraction(-1, 2)), "boundary gradient changed")

    euclidean_step = sub(zero, gradient(zero))
    exact_metric_step = (
        -gradient(zero)[0] / hessian[0],
        -gradient(zero)[1] / hessian[1],
    )
    normalized_step = (
        -gradient(zero)[0] / abs(gradient(zero)[0]),
        -gradient(zero)[1] / abs(gradient(zero)[1]),
    )
    require(euclidean_step == linear, "Euclidean metric step changed")
    require(exact_metric_step == unconstrained, "exact-H metric step changed")
    require(normalized_step == (Fraction(1), Fraction(1)), "gradient normalization changed")

    newton_decrement_sq = dot(linear, unconstrained)
    require(newton_decrement_sq == Fraction(41, 16), "Newton decrement changed")
    require(
        Fraction(1, 2) * newton_decrement_sq == objective(zero) - objective(unconstrained),
        "Newton predicted/actual reduction no longer matches",
    )

    least_squares_a = (Fraction(1), Fraction(2))
    least_squares_c = (Fraction(1), Fraction(5, 4))
    require(
        (least_squares_a[0] ** 2, least_squares_a[1] ** 2) == hessian,
        "Gauss-Newton matrix changed",
    )
    require(
        (least_squares_a[0] * least_squares_c[0], least_squares_a[1] * least_squares_c[1])
        == linear,
        "least-squares linear term changed",
    )
    secant = (Fraction(1), Fraction(1))
    secant_gradient = (hessian[0] * secant[0], hessian[1] * secant[1])
    require(secant_gradient == (Fraction(1), Fraction(4)), "secant curvature changed")
    require(dot(secant, secant_gradient) == Fraction(5), "BFGS curvature product changed")

    euclidean_projection = (Fraction(11, 16), Fraction(5, 16))
    require(sum(euclidean_projection) == 1, "Euclidean projection is not on active face")
    metric_residual = sub(optimizer, unconstrained)
    metric_normal = (
        hessian[0] * metric_residual[0],
        hessian[1] * metric_residual[1],
    )
    require(metric_normal == (Fraction(-1, 2), Fraction(-1, 2)), "H-projection normal changed")

    step = Fraction(1, 4)
    raw = sub(optimizer, scale(step, gradient(optimizer)))
    require(raw == (Fraction(5, 8), Fraction(5, 8)), "projected-gradient raw point changed")
    require(
        sub(raw, optimizer) == (Fraction(1, 8), Fraction(1, 8)),
        "projected-gradient normal offset changed",
    )

    constraints = (
        optimizer[0] + optimizer[1] - 1,
        -optimizer[0],
        -optimizer[1],
    )
    multipliers = (Fraction(1, 2), Fraction(0), Fraction(0))
    stationarity = add(gradient(optimizer), scale(multipliers[0], (Fraction(1), Fraction(1))))
    complementarity = tuple(value * constraint for value, constraint in zip(multipliers, constraints))
    require(constraints == (Fraction(0), Fraction(-1, 2), Fraction(-1, 2)), "KKT primal values changed")
    require(stationarity == zero, "KKT stationarity changed")
    require(complementarity == (0, 0, 0), "KKT complementarity changed")
    slater = (Fraction(1, 4), Fraction(1, 4))
    require(slater[0] + slater[1] < 1 and min(slater) > 0, "Slater point changed")
    require(Fraction(1, 4) * 2 == multipliers[0], "scaled multiplier audit changed")

    print(
        "PASS exact constrained model: variable metrics, Newton/GN/secant, "
        "I/H projections, projected stationarity, KKT lambda=(1/2,0,0)"
    )


def audit_markdown_integrity() -> None:
    scoped = [OPT / filename for filename in CONCEPTS]
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    math_findings: list[str] = []
    for path in scoped:
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
        if active.count("$$") % 2:
            math_findings.append(str(path.relative_to(ROOT)))
        for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", active):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            link_count += 1
            suffix = Path(target).suffix.lower()
            if "/" in target:
                direct = ROOT / target
                candidates = [direct] if direct.is_file() else []
                if not candidates and suffix not in KNOWN_EXTENSIONS:
                    markdown = Path(str(direct) + ".md")
                    if markdown.is_file():
                        candidates = [markdown]
            else:
                key = target[: -len(suffix)] if suffix in KNOWN_EXTENSIONS else target
                candidates = file_index.get(key, [])
                if suffix in KNOWN_EXTENSIONS:
                    candidates = [candidate for candidate in candidates if candidate.suffix.lower() == suffix]
            if not candidates:
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{path.relative_to(ROOT)} -> {target}")

    require(not math_findings, f"unbalanced display math: {math_findings}")
    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")

    figure_count = 0
    image_pattern = re.compile(r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
    for path in scoped:
        lines = read(path).splitlines()
        positions = [index for index, line in enumerate(lines) if image_pattern.search(line)]
        require(len(positions) == 1, f"{path.name}: expected exactly one teaching figure")
        for position in positions:
            figure_count += 1
            block = "\n".join(lines[position : min(len(lines), position + 45)])
            for marker in ("[!figure]", "怎样读图", "适用边界"):
                require(marker in block, f"{path.name}:{position + 1} misses figure marker {marker}")
            match = image_pattern.search(lines[position])
            require(match is not None, "internal image parser failure")
            image_path = ROOT / match.group(1)
            require(image_path.is_file(), f"missing embedded image: {match.group(1)}")
            if image_path.suffix.lower() == ".svg":
                root_element = ET.parse(image_path).getroot()
                require(root_element.tag.endswith("svg"), f"invalid SVG root: {match.group(1)}")
                require("viewBox" in root_element.attrib, f"SVG missing viewBox: {match.group(1)}")

    print(
        f"PASS scoped Markdown: Wiki links={link_count}, display math balanced, "
        f"figure units/SVG XML={figure_count}"
    )


def audit_figures() -> None:
    outputs: list[str] = []
    for script in FIGURE_SCRIPTS:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        if result.stdout.strip():
            outputs.append(result.stdout.strip())
    for filename, expected in FIGURE_HASHES.items():
        path = FIGURE_DIR / filename
        require(path.is_file(), f"figure script did not generate {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"figure hash changed for {filename}: {digest}")
    print(f"PASS deterministic figures: {len(FIGURE_HASHES)}/{len(FIGURE_HASHES)} hashes stable")
    if outputs:
        print("\n".join(outputs))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-figures",
        action="store_true",
        help="regenerate the migrated OPT SVGs and verify their SHA-256 hashes",
    )
    args = parser.parse_args()
    audit_contracts()
    audit_exact_model()
    audit_exact_spectral_model()
    audit_exact_constrained_model()
    audit_markdown_integrity()
    if args.run_figures:
        audit_figures()
    else:
        print("SKIP figure regeneration (pass --run-figures for the formal first-wave audit)")
    print(f"OPT-01—{len(CONCEPTS):02d} material regression: PASS")


if __name__ == "__main__":
    main()
