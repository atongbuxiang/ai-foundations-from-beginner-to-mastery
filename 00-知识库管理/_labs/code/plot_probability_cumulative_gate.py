#!/usr/bin/env python3
"""Reproducible probability/statistics cumulative gate using only stdlib.

The script deliberately contrasts:
1. repeated-sampling coverage (not posterior probability),
2. importance-sampling error/ESS and an infinite-second-moment proposal,
3. a multi-chain R-hat blind spot when every chain starts in one mode.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import random
import statistics
import sys
from pathlib import Path


DEFAULT_SEED = 20260819
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = (
    ROOT
    / "00-知识库管理"
    / "_assets"
    / "figures"
    / "probability"
    / "plot-probability-cumulative-gate-v2.svg"
)


def quantile(values: list[float], p: float) -> float:
    xs = sorted(values)
    if not xs:
        raise ValueError("empty data")
    h = (len(xs) - 1) * p
    lo = int(math.floor(h))
    hi = int(math.ceil(h))
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - h) + xs[hi] * (h - lo)


def coverage_experiment(seed: int, reps: int, probability: float = 0.30) -> list[dict[str, float]]:
    rng = random.Random(seed)
    p = probability
    out: list[dict[str, float]] = []
    for n in (20, 50, 100, 500):
        estimates: list[float] = []
        covered = 0
        for _ in range(reps):
            successes = sum(rng.random() < p for _ in range(n))
            phat = successes / n
            se_hat = math.sqrt(phat * (1.0 - phat) / n)
            lo = phat - 1.96 * se_hat
            hi = phat + 1.96 * se_hat
            covered += lo <= p <= hi
            estimates.append(phat)
        bias = statistics.fmean(estimates) - p
        rmse = math.sqrt(statistics.fmean((x - p) ** 2 for x in estimates))
        out.append(
            {
                "n": float(n),
                "bias": bias,
                "rmse": rmse,
                "coverage": covered / reps,
            }
        )
    return out


def normal_tail(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def importance_experiment(
    seed: int,
    repeats: int,
    draws: int,
    threshold: float = 3.0,
    proposal_sigmas: tuple[float, float, float] = (0.70, 1.00, 2.00),
) -> tuple[float, list[dict[str, float]]]:
    truth = normal_tail(threshold)
    out: list[dict[str, float]] = []
    for j, sigma in enumerate(proposal_sigmas):
        rng = random.Random(seed + 1000 + 97 * j)
        estimates: list[float] = []
        ess_fractions: list[float] = []
        max_shares: list[float] = []
        zero_tail_runs = 0
        for _ in range(repeats):
            sum_w = 0.0
            sum_w2 = 0.0
            sum_wh = 0.0
            max_w = 0.0
            tail_hits = 0
            for _ in range(draws):
                x = rng.gauss(0.0, sigma)
                log_w = math.log(sigma) + 0.5 * x * x * (1.0 / (sigma * sigma) - 1.0)
                w = math.exp(log_w)
                sum_w += w
                sum_w2 += w * w
                max_w = max(max_w, w)
                if x > threshold:
                    sum_wh += w
                    tail_hits += 1
            estimates.append(sum_wh / draws)  # ordinary IS; target is normalized
            ess_fractions.append((sum_w * sum_w / sum_w2) / draws)
            max_shares.append(max_w / sum_w)
            zero_tail_runs += tail_hits == 0
        rmse = math.sqrt(statistics.fmean((x - truth) ** 2 for x in estimates))
        out.append(
            {
                "sigma": sigma,
                "median": quantile(estimates, 0.5),
                "rmse": rmse,
                "relative_rmse": rmse / truth,
                "ess_fraction": quantile(ess_fractions, 0.5),
                "max_share": quantile(max_shares, 0.5),
                "zero_runs": float(zero_tail_runs),
            }
        )
    return truth, out


def log_mix_target(x: float, mode_location: float = 6.0) -> float:
    # Equal mixture of N(-mode,1) and N(mode,1); common normal constant is irrelevant.
    a = -0.5 * (x + mode_location) ** 2
    b = -0.5 * (x - mode_location) ** 2
    m = max(a, b)
    return m + math.log(math.exp(a - m) + math.exp(b - m)) - math.log(2.0)


def mh_chain(
    seed: int,
    initial: float,
    warmup: int,
    draws: int,
    step: float,
    mode_location: float = 6.0,
) -> tuple[list[float], float]:
    rng = random.Random(seed)
    x = initial
    log_px = log_mix_target(x, mode_location)
    kept: list[float] = []
    accepted = 0
    total = warmup + draws
    for i in range(total):
        y = x + rng.gauss(0.0, step)
        log_py = log_mix_target(y, mode_location)
        if math.log(rng.random()) < min(0.0, log_py - log_px):
            x = y
            log_px = log_py
            accepted += 1
        if i >= warmup:
            kept.append(x)
    return kept, accepted / total


def classic_rhat(chains: list[list[float]]) -> float:
    m = len(chains)
    n = min(len(c) for c in chains)
    trimmed = [c[:n] for c in chains]
    means = [statistics.fmean(c) for c in trimmed]
    variances = [statistics.variance(c) for c in trimmed]
    w = statistics.fmean(variances)
    b = n * statistics.variance(means)
    var_hat = ((n - 1.0) / n) * w + b / n
    return math.sqrt(var_hat / w)


def split_rhat(chains: list[list[float]]) -> float:
    halves: list[list[float]] = []
    for c in chains:
        half = len(c) // 2
        halves.extend((c[:half], c[-half:]))
    return classic_rhat(halves)


def mcmc_experiment(
    seed: int,
    warmup: int,
    draws: int,
    mode_location: float = 6.0,
    proposal_step: float = 1.5,
) -> list[dict[str, object]]:
    mode = mode_location
    scenarios = [
        ("all-left", (-mode, -mode - 0.3, -mode + 0.3, -mode - 0.1)),
        ("dispersed", (-mode, -mode + 0.3, mode - 0.3, mode)),
    ]
    out: list[dict[str, object]] = []
    for j, (name, initials) in enumerate(scenarios):
        chains: list[list[float]] = []
        accepts: list[float] = []
        for i, initial in enumerate(initials):
            chain, accept = mh_chain(
                seed + 5000 + 101 * j + i,
                initial,
                warmup,
                draws,
                proposal_step,
                mode_location,
            )
            chains.append(chain)
            accepts.append(accept)
        means = [statistics.fmean(c) for c in chains]
        positive_fraction = statistics.fmean(
            statistics.fmean(1.0 if x > 0 else 0.0 for x in c) for c in chains
        )
        out.append(
            {
                "name": name,
                "means": means,
                "pooled_mean": statistics.fmean(means),
                "rhat": split_rhat(chains),
                "positive_fraction": positive_fraction,
                "acceptance": statistics.fmean(accepts),
            }
        )
    return out


def svg_text(x: float, y: float, value: str, cls: str = "small", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def make_svg(
    coverage: list[dict[str, float]],
    truth: float,
    importance: list[dict[str, float]],
    mcmc: list[dict[str, object]],
    coverage_reps: int,
    coverage_probability: float,
    tail_threshold: float,
    mode_location: float,
) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430" role="img" aria-labelledby="title desc">',
        '<title id="title">概率统计累计复现门</title>',
        '<desc id="desc">三面板展示置信区间重复抽样覆盖、重要性采样尾概率与权重退化、以及双峰目标中多链初始化导致的 R-hat 盲区。</desc>',
        '<defs><style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif}.title{font-size:24px;font-weight:700;fill:#1F2937}.head{font-size:22px;font-weight:700;fill:#334155}.small{font-size:15px;fill:#64748B}.label{font-size:17px;fill:#334155}.math{font-family:Georgia,"Times New Roman",serif;font-size:17px;fill:#1F2937}.card{fill:#FFFEFB;stroke:#D7DEE8;stroke-width:1.3}.axis{stroke:#64748B;stroke-width:1.1}.grid{stroke:#D7DEE8;stroke-width:1;stroke-dasharray:4 4}</style></defs>',
        '<rect width="1200" height="430" fill="#FFFFFF"/>',
        '<text x="40" y="38" class="title">PROB-CUM-01 计算门：coverage、importance weights 与多链诊断</text>',
        '<rect x="28" y="58" width="368" height="342" class="card"/><rect x="416" y="58" width="368" height="342" class="card"/><rect x="804" y="58" width="368" height="342" class="card"/>',
        '<text x="50" y="88" class="head">A　Wald CI 覆盖率</text>',
        '<text x="438" y="88" class="head">B　rare-event IS 与 ESS</text>',
        '<text x="826" y="88" class="head">C　双链 MCMC 与 R-hat</text>',
    ]

    # Panel A: coverage as a function of n.
    ax0, ay0, aw, ah = 70.0, 125.0, 280.0, 155.0
    parts += [
        f'<line x1="{ax0}" y1="{ay0+ah}" x2="{ax0+aw}" y2="{ay0+ah}" class="axis"/>',
        f'<line x1="{ax0}" y1="{ay0}" x2="{ax0}" y2="{ay0+ah}" class="axis"/>',
    ]
    minimum_coverage = min(float(row["coverage"]) for row in coverage)
    coverage_floor = min(0.75, math.floor((minimum_coverage - 0.05) * 20) / 20)
    def y_cov(v: float) -> float:
        return ay0 + ah - (v - coverage_floor) / (1.0 - coverage_floor) * ah
    y95 = y_cov(0.95)
    parts.append(f'<line x1="{ax0}" y1="{y95:.1f}" x2="{ax0+aw}" y2="{y95:.1f}" stroke="#16A34A" stroke-width="1.5" stroke-dasharray="6 4"/>')
    parts.append(svg_text(ax0 + aw - 4, y95 - 5, "nominal 0.95", "small", "end"))
    points = []
    for i, row in enumerate(coverage):
        x = ax0 + i * aw / 3
        y = y_cov(row["coverage"])
        points.append(f"{x:.1f},{y:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#2563EB"/>')
        parts.append(svg_text(x, ay0 + ah + 20, f'n={int(row["n"])}', "small", "middle"))
        parts.append(svg_text(x, y - 10, f'{row["coverage"]:.3f}', "label", "middle"))
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#2563EB" stroke-width="2.5"/>')
    parts.append(svg_text(70, 323, f'p={coverage_probability:.2f}；每个 n 重复 {coverage_reps} 次；Wald 区间', "small"))
    parts.append(svg_text(70, 348, "coverage 偏离 0.95 不等于 posterior 概率改变", "label"))
    parts.append(svg_text(70, 375, "小样本/边界概率需换更可靠 interval", "small"))

    # Panel B: relative RMSE bars and ESS labels.
    bx0, by0, bw, bh = 460.0, 130.0, 280.0, 145.0
    max_rr = max(float(r["relative_rmse"]) for r in importance)
    parts.append(f'<line x1="{bx0}" y1="{by0+bh}" x2="{bx0+bw}" y2="{by0+bh}" class="axis"/>')
    for i, row in enumerate(importance):
        x = bx0 + 25 + i * 92
        rr = float(row["relative_rmse"])
        h = max(3.0, rr / max_rr * 115.0)
        color = ("#DC2626", "#F59E0B", "#16A34A")[i]
        parts.append(f'<rect x="{x:.1f}" y="{by0+bh-h:.1f}" width="48" height="{h:.1f}" rx="5" fill="{color}" fill-opacity=".82"/>')
        parts.append(svg_text(x + 24, by0 + bh + 20, f'σq={float(row["sigma"]):.1f}', "small", "middle"))
        parts.append(svg_text(x + 24, by0 + bh - h - 8, f'{rr:.2f}×', "label", "middle"))
        parts.append(svg_text(x + 24, 318, f'ESS/N={float(row["ess_fraction"]):.2f}', "small", "middle"))
    parts.append(svg_text(438, 112, f'truth P(Z&gt;{tail_threshold:g})={truth:.6f}; bar=relative RMSE', "small"))
    narrow_sigma = float(importance[0]["sigma"])
    if narrow_sigma == 0.7:
        narrow_diagnostic = "σq=0.7 有 support，却有无限 weight 二阶矩"
    elif narrow_sigma * narrow_sigma <= 0.5:
        narrow_diagnostic = f"σq={narrow_sigma:.1f} 有 support，weight 二阶矩仍发散"
    else:
        narrow_diagnostic = f"σq={narrow_sigma:.1f} 二阶矩有限，仍须检查尾命中"
    parts.append(svg_text(438, 347, narrow_diagnostic, "label"))
    parts.append(svg_text(438, 374, "ESS 只诊断已见 weights；不能证明未漏 mode", "small"))

    # Panel C: chain means for same-mode vs dispersed starts.
    cx0, cy0, cw, ch = 850.0, 125.0, 270.0, 165.0
    mean_limit = mode_location + 2.0
    def y_mean(v: float) -> float:
        return cy0 + ch - (v + mean_limit) / (2.0 * mean_limit) * ch
    yzero = y_mean(0.0)
    parts += [
        f'<line x1="{cx0}" y1="{cy0+ch}" x2="{cx0+cw}" y2="{cy0+ch}" class="axis"/>',
        f'<line x1="{cx0}" y1="{yzero:.1f}" x2="{cx0+cw}" y2="{yzero:.1f}" stroke="#16A34A" stroke-width="1.5" stroke-dasharray="6 4"/>',
        svg_text(cx0 + cw, yzero - 5, "true mean = 0", "small", "end"),
    ]
    group_x = (905.0, 1065.0)
    colors = ("#7C3AED", "#DB2777", "#2563EB", "#EA580C")
    for j, row in enumerate(mcmc):
        means = row["means"]
        for i, value in enumerate(means):
            x = group_x[j] + (i - 1.5) * 14
            y = y_mean(float(value))
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{colors[i]}"/>')
        label = "同为左峰" if j == 0 else "分散两峰"
        parts.append(svg_text(group_x[j], cy0 + ch + 20, label, "label", "middle"))
        parts.append(svg_text(group_x[j], 326, f'R-hat={float(row["rhat"]):.3f}', "label", "middle"))
        parts.append(svg_text(group_x[j], 346, f'mean={float(row["pooled_mean"]):.2f}', "small", "middle"))
    parts.append(svg_text(826, 374, "低 R-hat 是必要预警工具，不是全局探索证书", "small"))
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--quick", action="store_true", help="smaller run for smoke tests")
    parser.add_argument("--coverage-p", type=float, default=0.30)
    parser.add_argument("--coverage-reps", type=int)
    parser.add_argument("--tail-threshold", type=float, default=3.0)
    parser.add_argument("--narrow-sigma", type=float, default=0.70)
    parser.add_argument("--wide-sigma", type=float, default=2.00)
    parser.add_argument("--is-repeats", type=int)
    parser.add_argument("--is-draws", type=int)
    parser.add_argument("--mode-location", type=float, default=6.0)
    parser.add_argument("--proposal-step", type=float, default=1.5)
    parser.add_argument("--warmup", type=int)
    parser.add_argument("--mcmc-draws", type=int)
    args = parser.parse_args()

    if not 0.01 <= args.coverage_p <= 0.99:
        raise ValueError("--coverage-p must lie in [0.01, 0.99]")
    if not 2.0 <= args.tail_threshold <= 5.0:
        raise ValueError("--tail-threshold must lie in [2, 5]")
    if not 0.3 <= args.narrow_sigma < 1.0:
        raise ValueError("--narrow-sigma must lie in [0.3, 1)")
    if not 1.0 < args.wide_sigma <= 4.0:
        raise ValueError("--wide-sigma must lie in (1, 4]")
    if not 3.0 <= args.mode_location <= 7.0:
        raise ValueError("--mode-location must lie in [3, 7]")
    if not 0.3 <= args.proposal_step <= 4.0:
        raise ValueError("--proposal-step must lie in [0.3, 4]")

    reps = args.coverage_reps if args.coverage_reps is not None else (800 if args.quick else 4000)
    is_repeats = args.is_repeats if args.is_repeats is not None else (12 if args.quick else 40)
    is_draws = args.is_draws if args.is_draws is not None else (5000 if args.quick else 20000)
    mcmc_draws = args.mcmc_draws if args.mcmc_draws is not None else (1200 if args.quick else 4000)
    warmup = args.warmup if args.warmup is not None else (300 if args.quick else 1000)
    for value, label, minimum in (
        (reps, "--coverage-reps", 500),
        (is_repeats, "--is-repeats", 10),
        (is_draws, "--is-draws", 2000),
        (mcmc_draws, "--mcmc-draws", 500),
        (warmup, "--warmup", 100),
    ):
        if value < minimum:
            raise ValueError(f"{label} must be at least {minimum}")

    proposal_sigmas = (args.narrow_sigma, 1.0, args.wide_sigma)
    coverage = coverage_experiment(args.seed, reps, args.coverage_p)
    truth, importance = importance_experiment(
        args.seed,
        is_repeats,
        is_draws,
        args.tail_threshold,
        proposal_sigmas,
    )
    mcmc = mcmc_experiment(
        args.seed,
        warmup,
        mcmc_draws,
        args.mode_location,
        args.proposal_step,
    )
    mcmc_by_name = {str(row["name"]): row for row in mcmc}
    canonical_configuration = (
        not args.quick
        and args.coverage_p == 0.30
        and reps == 4000
        and args.tail_threshold == 3.0
        and args.narrow_sigma == 0.70
        and args.wide_sigma == 2.00
        and is_repeats == 40
        and is_draws == 20000
        and args.mode_location == 6.0
        and args.proposal_step == 1.5
        and warmup == 1000
        and mcmc_draws == 4000
    )
    if canonical_configuration:
        if abs(float(coverage[-1]["coverage"]) - 0.95) > 0.03:
            raise AssertionError("canonical large-n Wald coverage moved outside its regression band")
        if float(min(importance, key=lambda row: row["rmse"])["sigma"]) != args.wide_sigma:
            raise AssertionError("canonical wider proposal should minimize rare-event RMSE")
        if not float(mcmc_by_name["dispersed"]["rhat"]) > float(mcmc_by_name["all-left"]["rhat"]):
            raise AssertionError("canonical dispersed initialization should expose the missed mode")
    svg = make_svg(
        coverage,
        truth,
        importance,
        mcmc,
        reps,
        args.coverage_p,
        args.tail_threshold,
        args.mode_location,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    print(f"A_CONFIG p={args.coverage_p:.6g} reps={reps}")
    print("A_COVERAGE n bias rmse wald95_coverage")
    for row in coverage:
        print(
            f'{int(row["n"]):4d} {row["bias"]:+.6f} '
            f'{row["rmse"]:.6f} {row["coverage"]:.4f}'
        )
    print(
        f"B_CONFIG threshold={args.tail_threshold:g} repeats={is_repeats} draws={is_draws} "
        f"sigmas={args.narrow_sigma:g},1,{args.wide_sigma:g}"
    )
    print(f"B_IMPORTANCE truth_tail={truth:.8f}")
    print("sigma median_est rmse relative_rmse median_ess_fraction median_max_share zero_tail_runs")
    for row in importance:
        print(
            f'{row["sigma"]:.2f} {row["median"]:.8f} {row["rmse"]:.8f} '
            f'{row["relative_rmse"]:.4f} {row["ess_fraction"]:.4f} '
            f'{row["max_share"]:.4f} {int(row["zero_runs"])}'
        )
    print(
        f"C_CONFIG mode={args.mode_location:g} step={args.proposal_step:g} "
        f"warmup={warmup} draws={mcmc_draws}"
    )
    print("C_MCMC scenario split_rhat pooled_mean positive_fraction acceptance chain_means")
    for row in mcmc:
        means = ",".join(f"{float(x):+.3f}" for x in row["means"])
        print(
            f'{row["name"]:9s} {row["rhat"]:.4f} {row["pooled_mean"]:+.4f} '
            f'{row["positive_fraction"]:.4f} {row["acceptance"]:.4f} {means}'
        )
    print(f"OUTPUT {args.output}")
    print(f"SHA256 {digest}")
    print(f"PYTHON {sys.version.split()[0]}")
    print(f"SEED {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
