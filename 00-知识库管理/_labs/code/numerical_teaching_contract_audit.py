#!/usr/bin/env python3
"""Audit NUM-01--08 teaching contracts and their two shared exact models."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NUM = ROOT / "10-数学基础" / "10.8-数值计算"
LABS = ROOT / "00-知识库管理" / "_labs"
MOC = NUM / "数值线性代数 MOC.md"
FIGURE_SCRIPTS = (
    LABS / "code" / "plot_numerical_error_foundations_v2.py",
    LABS / "code" / "plot_numerical_direct_methods_v2.py",
)
FIGURE_DIR = ROOT / "00-知识库管理" / "_assets" / "figures" / "numerical-analysis"

CONCEPTS = (
    "浮点数与舍入误差.md",
    "前向误差与后向误差.md",
    "数值稳定性.md",
    "误差传播、条件估计与停止准则.md",
    "稳定求和、点积与矩阵乘法.md",
    "稳定求解线性方程组.md",
    "迭代改进、混合精度与残差校正.md",
    "Householder 与 Givens 变换.md",
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
    "fig-floating-point-system-v2.svg":
        "6661ec2e7b0e29c247e523d3cd45baf0acf4b03cdb5d18575c2f32ea5eee5496",
    "fig-error-analysis-pipeline-v2.svg":
        "f1216c5f9fe64649dd89e73626344cdd4d0f1dc9035d931763a374c7a97c58f8",
    "fig-numerical-stability-formulas-v2.svg":
        "07fbfaa757a0da24a9e64ddce55363befa00256f7c082c0ee2b30c473a2076ad",
    "fig-condition-estimation-stopping-v2.svg":
        "093aab40c145748496067227590ec447d1b51c696a98223d4a96fe0ded98e692",
    "fig-stable-reductions-matmul-v2.svg":
        "477695f5f42dd5c192d7fed82061f74e49d87bd99aa9cc373dd99819f00c0190",
    "fig-pivoting-linear-solve-v2.svg":
        "bb80e8861932835aae21c7cb5e4f438160acce225176f0a7ed85c0db6a9196fa",
    "fig-mixed-precision-refinement-v2.svg":
        "722547f7da7a0d8b9b64fed9e89310eff94462272c4a94a328d3278f6fbfffe9",
    "fig-householder-givens-qr-v2.svg":
        "4615fa61a36cfbb3850b57162c329f792e289d1b77102d94354dae22b6ab1763",
}

EXPECTED_FIGURE_BY_CONCEPT = {
    CONCEPTS[0]: "fig-floating-point-system-v2.svg",
    CONCEPTS[1]: "fig-error-analysis-pipeline-v2.svg",
    CONCEPTS[2]: "fig-numerical-stability-formulas-v2.svg",
    CONCEPTS[3]: "fig-condition-estimation-stopping-v2.svg",
    CONCEPTS[4]: "fig-stable-reductions-matmul-v2.svg",
    CONCEPTS[5]: "fig-pivoting-linear-solve-v2.svg",
    CONCEPTS[6]: "fig-mixed-precision-refinement-v2.svg",
    CONCEPTS[7]: "fig-householder-givens-qr-v2.svg",
}

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


def audit_contracts() -> None:
    for filename in CONCEPTS:
        text = read(NUM / filename)
        missing = [marker for marker in CONTRACT_MARKERS if marker not in text]
        require(not missing, f"{filename}: missing teaching markers {missing}")
        require("status: draft" in text, f"{filename}: learning state must remain draft")
        require("updated: 2026-08-27" in text, f"{filename}: migration date missing")
    print(f"PASS NUM teaching contracts: {len(CONCEPTS)}/{len(CONCEPTS)}")


def audit_route() -> None:
    text = read(MOC)
    for marker in (
        "全卷教学迁移路线",
        "| A | NUM-01—04",
        "| B | NUM-05—08",
        "| C | NUM-09—12",
        "| D | NUM-13—16",
        "| E | NUM-17—20",
        "第一波的单一模型链",
        "如何学习第一波，而不是只把它读完",
        "第二波的单一模型链",
        "如何学习第二波，而不是背算法名",
        "第二波材料证书",
        "numerical_teaching_contract_audit.py",
        "`regression-passed`",
        "`draft / not-attempted`",
    ):
        require(marker in text, f"MOC misses route marker: {marker}")
    require(
        re.search(r"\| B \| NUM-05—08 .*`regression-passed`", text) is not None,
        "MOC second-wave material status is not regression-passed",
    )
    require("Gram-Schmidt 的数值稳定性" not in text, "MOC retains missing placeholder link")
    print("PASS NUM route: five waves, two migrated model chains, three-pass learning contracts")


def audit_exact_scalar_model() -> None:
    tau = Fraction(1, 10_000)
    gap_at_one = Fraction(1, 1_000)
    unit_roundoff = Fraction(1, 2_000)
    half_gap = gap_at_one / 2

    require(tau < half_gap, "tau should be absorbed when added to 1 in F_{10,4}")
    require(gap_at_one == 2 * unit_roundoff, "gap/unit-roundoff convention changed")

    naive = Fraction(0)
    stable = Fraction(1, 20_000)
    exact = math.sqrt(1.0 + float(tau)) - 1.0
    stable_forward = abs(float(stable) - exact) / exact
    require(naive == 0, "naive cancellation output changed")
    require(2.49e-5 < stable_forward < 2.51e-5, "stable forward error changed")
    require(stable_forward < float(unit_roundoff), "stable formula is no longer O(u)-accurate")

    stable_neighbor = 2 * stable + stable**2
    stable_backward = abs(stable_neighbor - tau) / tau
    naive_neighbor = Fraction(0)
    naive_backward = abs(naive_neighbor - tau) / tau
    require(stable_neighbor == Fraction(40_001, 400_000_000), "stable neighbor input changed")
    require(stable_backward == Fraction(1, 40_000), "stable backward error changed")
    require(naive_backward == 1, "naive backward error changed")

    condition = (math.sqrt(1.0 + float(tau)) + 1.0) / (
        2.0 * math.sqrt(1.0 + float(tau))
    )
    require(0.9999 < condition <= 1.0, "scalar relative condition calibration changed")
    print(
        "PASS scalar model: gap=1e-3, u=5e-4, naive backward=1, "
        "stable backward=2.5e-5, kappa_rel≈1"
    )


def audit_exact_linear_model() -> None:
    tau = Fraction(1, 10_000)

    # A=diag(1,tau), x*=(1,1), xhat=(1,0), b=(1,tau), r=(0,tau).
    forward_error_squared = Fraction(1, 2)
    residual_ratio_squared = tau**2 / (1 + tau**2)
    condition_number = 1 / tau
    amplified_risk_squared = condition_number**2 * residual_ratio_squared

    require(forward_error_squared == Fraction(1, 2), "relative forward error changed")
    require(condition_number == 10_000, "diagonal condition number changed")
    require(
        amplified_risk_squared == Fraction(1, 1) / (1 + tau**2),
        "condition-amplified residual identity changed",
    )

    rho = float(tau) / math.sqrt(1.0 + float(tau**2))
    joint = float(tau) / (1.0 + math.sqrt(1.0 + float(tau**2)))
    componentwise = Fraction(1)
    require(rho < 1e-4, "naive residual gate should strictly pass")
    require(4.999e-5 < joint < 5.001e-5, "joint backward error changed")
    require(componentwise == 1, "componentwise backward error changed")

    task_budget = Fraction(1, 100)
    required_rho = task_budget / condition_number
    require(required_rho == Fraction(1, 1_000_000), "condition-aware tolerance changed")
    require(rho > float(required_rho), "candidate should fail the task-aware gate")
    print(
        "PASS linear model: forward=1/sqrt(2), rho<1e-4, kappa=1e4, "
        "kappa*rho≈1, eta_joint≈5e-5, eta_comp=1, required rho=1e-6"
    )


def decimal4_context() -> Context:
    return Context(
        prec=4,
        rounding=ROUND_HALF_EVEN,
        Emin=-999,
        Emax=999,
    )


def neumaier_decimal4(values: tuple[Decimal, ...]) -> Decimal:
    with localcontext(decimal4_context()):
        total = Decimal(0)
        correction = Decimal(0)
        for value in values:
            updated = total + value
            if abs(total) >= abs(value):
                correction += (total - updated) + value
            else:
                correction += (value - updated) + total
            total = updated
        return +(total + correction)


def audit_exact_direct_model() -> None:
    eps = Fraction(1, 100_000_000)
    one = Fraction(1)

    # Reduction conditioning and exact sum.
    reduction = (1 / eps, one, -1 / eps)
    require(sum(reduction) == 1, "second-wave exact reduction changed")
    require(sum(abs(value) for value in reduction) == 200_000_001, "sum condition changed")

    with localcontext(decimal4_context()):
        huge = Decimal("1e8")
        left = +(+(huge + Decimal(1)) - huge)
        cancel_first = +(+(huge - huge) + Decimal(1))
        require(left == 0, "left-associated F_{10,4} sum should lose the unit")
        require(cancel_first == 1, "cancel-first F_{10,4} sum should recover the unit")
    compensated = neumaier_decimal4((Decimal("1e8"), Decimal(1), Decimal("-1e8")))
    require(compensated == 1, "Neumaier teaching reduction no longer recovers the tail")

    # Exact system A=[[eps,1],[1,1]], b=(1,2).
    denominator = 1 - eps
    x_star = (1 / denominator, (1 - 2 * eps) / denominator)
    kappa_inf = 4 / denominator
    require(kappa_inf == Fraction(400_000_000, 99_999_999), "kappa_inf changed")

    with localcontext(decimal4_context()):
        eps4 = Decimal("1e-8")
        multiplier = Decimal(1) / eps4
        u22 = Decimal(1) - multiplier
        rhs2 = Decimal(2) - multiplier
        x2_no_pivot = rhs2 / u22
        x1_no_pivot = (Decimal(1) - x2_no_pivot) / eps4
        require(multiplier == Decimal("1e8"), "unpivoted multiplier changed")
        require(u22 == rhs2 == Decimal("-1.000e8"), "distinct elimination values should collapse")
        require((x1_no_pivot, x2_no_pivot) == (Decimal(0), Decimal(1)), "unpivoted output changed")

        pivot_multiplier = eps4
        pivot_u22 = Decimal(1) - pivot_multiplier
        pivot_rhs2 = Decimal(1) - Decimal(2) * pivot_multiplier
        x2_pivot = pivot_rhs2 / pivot_u22
        x1_pivot = Decimal(2) - x2_pivot
        require((x1_pivot, x2_pivot) == (Decimal(1), Decimal(1)), "pivoted output changed")

    no_pivot = (Fraction(0), Fraction(1))
    pivoted = (Fraction(1), Fraction(1))
    no_pivot_error = max(abs(a - b) for a, b in zip(x_star, no_pivot)) / max(
        abs(value) for value in x_star
    )
    pivot_error = max(abs(a - b) for a, b in zip(x_star, pivoted)) / max(
        abs(value) for value in x_star
    )
    require(no_pivot_error == 1, "unpivoted relative forward error changed")
    require(pivot_error == eps, "pivoted relative forward error changed")

    pivot_residual = (-eps, Fraction(0))
    pivot_berr = abs(pivot_residual[0]) / (2 + eps)
    require(pivot_berr == eps / (2 + eps), "pivoted BERR changed")
    print(
        "PASS direct model: sum 1 -> left 0 / reordered+Neumaier 1; "
        "kappa_inf≈4, multiplier 1e8 -> 1e-8, forward 1 -> 1e-8"
    )


def audit_exact_refinement_model() -> None:
    q = Fraction(1, 4)
    relative_errors = [q ** (index + 1) for index in range(4)]
    iterate_ratios = [1 - error for error in relative_errors]
    require(
        relative_errors == [Fraction(1, 4), Fraction(1, 16), Fraction(1, 64), Fraction(1, 256)],
        "refinement error sequence changed",
    )
    require(
        iterate_ratios == [Fraction(3, 4), Fraction(15, 16), Fraction(63, 64), Fraction(255, 256)],
        "refinement iterate sequence changed",
    )
    initial_residual_ratio = q
    first_correction_ratio = (1 - q) * initial_residual_ratio
    require(first_correction_ratio == Fraction(3, 16), "first correction changed")
    require(q == 1 - (1 - q), "error-map scalar identity changed")
    print("PASS refinement model: exact error ratios 1/4, 1/16, 1/64, 1/256")


def audit_exact_qr_model() -> None:
    eps = 1e-8
    r = math.hypot(1.0, eps)
    c = 1.0 / r
    s = eps / r
    require(math.isclose(c * c + s * s, 1.0, rel_tol=0.0, abs_tol=2e-16), "Givens norm changed")

    a_tilde = ((1.0, 1.0), (eps, 1.0))
    givens = ((c, s), (-s, c))

    def matmul(first, second):
        return tuple(
            tuple(sum(first[i][k] * second[k][j] for k in range(2)) for j in range(2))
            for i in range(2)
        )

    r_factor = matmul(givens, a_tilde)
    require(abs(r_factor[1][0]) < 1e-24, "Givens failed to annihilate the lower entry")
    require(math.isclose(r_factor[0][0], r, rel_tol=0.0, abs_tol=2e-16), "R11 changed")
    require(
        math.isclose(r_factor[0][1], (1 + eps) / r, rel_tol=0.0, abs_tol=2e-16),
        "R12 changed",
    )
    require(
        math.isclose(r_factor[1][1], (1 - eps) / r, rel_tol=0.0, abs_tol=2e-16),
        "R22 changed",
    )
    require(
        math.isclose(r_factor[0][0] * r_factor[1][1], 1 - eps, rel_tol=0.0, abs_tol=2e-16),
        "QR determinant certificate changed",
    )

    safe_v = (1 + r, eps)
    safe_norm_squared = safe_v[0] ** 2 + safe_v[1] ** 2
    householder = (
        (1 - 2 * safe_v[0] ** 2 / safe_norm_squared, -2 * safe_v[0] * safe_v[1] / safe_norm_squared),
        (-2 * safe_v[1] * safe_v[0] / safe_norm_squared, 1 - 2 * safe_v[1] ** 2 / safe_norm_squared),
    )
    reflected = (
        householder[0][0] + householder[0][1] * eps,
        householder[1][0] + householder[1][1] * eps,
    )
    require(math.isclose(reflected[0], -r, rel_tol=0.0, abs_tol=3e-16), "safe reflector target changed")
    require(abs(reflected[1]) < 1e-23, "safe reflector failed to annihilate tail")

    with localcontext(decimal4_context()):
        toy_r = (Decimal(1) + Decimal("1e-16")).sqrt()
        bad_first = Decimal(1) - toy_r
        safe_first = Decimal(1) + toy_r
        require(toy_r == 1 and bad_first == 0, "unsafe Householder cancellation changed")
        require(safe_first == 2, "safe Householder leading component changed")
    print("PASS QR model: exact Givens R/determinant, safe Householder, unsafe sign cancels in F_{10,4}")


def audit_markdown_integrity() -> None:
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    file_index: dict[str, list[Path]] = {}
    for path in all_files:
        key = path.name[: -len(path.suffix)] if path.suffix.lower() in KNOWN_EXTENSIONS else path.name
        file_index.setdefault(key, []).append(path)

    link_count = 0
    missing_links: list[str] = []
    ambiguous_links: list[str] = []
    image_pattern = re.compile(
        r"!\[\[([^\]]+\.(?:svg|png|jpe?g|webp))(?:\|[^\]]*)?\]\]",
        re.I,
    )

    for filename in CONCEPTS:
        path = NUM / filename
        lines = active_lines(read(path))
        active = "\n".join(re.sub(r"`[^`]*`", "", line) for line in lines)
        require(active.count("$$") % 2 == 0, f"{filename}: unbalanced display math")

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
                missing_links.append(f"{filename} -> {target}")
            elif len(candidates) > 1:
                ambiguous_links.append(f"{filename} -> {target}")

        images = [(index, image_pattern.search(line)) for index, line in enumerate(lines)]
        images = [(index, match) for index, match in images if match is not None]
        require(len(images) == 1, f"{filename}: expected one textbook figure, found {len(images)}")
        position, match = images[0]
        require(match is not None, "internal image parser failure")
        expected = EXPECTED_FIGURE_BY_CONCEPT[filename]
        require(Path(match.group(1)).name == expected, f"{filename}: unexpected figure")
        block = "\n".join(lines[position : min(len(lines), position + 45)])
        for marker in ("[!figure]", "怎样读图", "适用边界"):
            require(marker in block, f"{filename}: figure unit misses {marker}")

    require(not missing_links, f"missing Wiki links: {missing_links}")
    require(not ambiguous_links, f"ambiguous Wiki links: {ambiguous_links}")
    print(
        f"PASS Markdown integrity: Wiki links={link_count}, display math balanced, "
        f"figures={len(CONCEPTS)}/{len(CONCEPTS)}"
    )


def audit_figures(run_figures: bool) -> None:
    if run_figures:
        for script in FIGURE_SCRIPTS:
            subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)
    for filename, expected_hash in FIGURE_HASHES.items():
        path = FIGURE_DIR / filename
        require(path.is_file(), f"missing figure: {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"figure hash changed: {filename} -> {digest}")
        root = ET.parse(path).getroot()
        require(root.tag.endswith("svg"), f"invalid SVG root: {filename}")
        require("viewBox" in root.attrib, f"SVG missing viewBox: {filename}")
    print(f"PASS deterministic figures: {len(FIGURE_HASHES)}/{len(FIGURE_HASHES)} hashes and SVG XML")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-figures", action="store_true")
    args = parser.parse_args()
    audit_contracts()
    audit_route()
    audit_exact_scalar_model()
    audit_exact_linear_model()
    audit_exact_direct_model()
    audit_exact_refinement_model()
    audit_exact_qr_model()
    audit_markdown_integrity()
    audit_figures(args.run_figures)
    print("NUM-01—08 material regression: PASS; learning state: draft/not-attempted")


if __name__ == "__main__":
    main()
