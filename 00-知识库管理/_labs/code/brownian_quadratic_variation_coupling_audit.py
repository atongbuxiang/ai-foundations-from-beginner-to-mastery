#!/usr/bin/env python3
"""Deterministic Brownian increment, variation, and temporal-coupling audit."""

from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path


SEED = 20260819
T = 1.0
N_MAX = 4096
PATHS = 768
RESOLUTIONS = [32, 64, 128, 256, 512, 1024, 2048, 4096]
TIMES = [0.25, 0.50, 0.75, 1.00]
ROOT = Path(__file__).resolve().parents[3]
PLOT = ROOT / "00-知识库管理/_assets/plots/dynamics/plot-brownian-quadratic-variation-coupling-v2.svg"


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def variance(xs: list[float]) -> float:
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def covariance(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)


def slope(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.0) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def circles(points: list[tuple[float, float]], color: str) -> str:
    return "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.4" fill="{color}"/>' for x, y in points
    )


def track_ab() -> dict[str, object]:
    rng = random.Random(SEED)
    dt = T / N_MAX
    sqrt_dt = math.sqrt(dt)
    time_indices = [round(t * N_MAX / T) for t in TIMES]
    values = [[] for _ in TIMES]
    qv = {n: [] for n in RESOLUTIONS}
    tv = {n: [] for n in RESOLUTIONS}
    first_path: list[float] = []

    for path_id in range(PATHS):
        increments = [sqrt_dt * rng.gauss(0.0, 1.0) for _ in range(N_MAX)]
        if path_id == 0:
            running = 0.0
            first_path = [0.0]
            for inc in increments:
                running += inc
                first_path.append(running)

        running = 0.0
        next_slot = 0
        for k, inc in enumerate(increments, start=1):
            running += inc
            if next_slot < len(time_indices) and k == time_indices[next_slot]:
                values[next_slot].append(running)
                next_slot += 1

        for n in RESOLUTIONS:
            block = N_MAX // n
            coarse = [
                sum(increments[start : start + block])
                for start in range(0, N_MAX, block)
            ]
            qv[n].append(sum(x * x for x in coarse))
            tv[n].append(sum(abs(x) for x in coarse))

    means = [mean(xs) for xs in values]
    variances = [variance(xs) for xs in values]
    covariance_matrix = [
        [covariance(values[i], values[j]) for j in range(len(TIMES))]
        for i in range(len(TIMES))
    ]
    inc_a = values[0]
    inc_b = [values[1][i] - values[0][i] for i in range(PATHS)]
    disjoint_cov = covariance(inc_a, inc_b)
    fourth_w1 = mean([x**4 for x in values[-1]])

    qv_mean = [mean(qv[n]) for n in RESOLUTIONS]
    qv_rmse = [math.sqrt(mean([(x - T) ** 2 for x in qv[n]])) for n in RESOLUTIONS]
    qv_theory_rmse = [T * math.sqrt(2.0 / n) for n in RESOLUTIONS]
    tv_mean = [mean(tv[n]) for n in RESOLUTIONS]
    tv_theory = [math.sqrt(2.0 * n * T / math.pi) for n in RESOLUTIONS]
    tv_log_slope = slope(
        [math.log(n) for n in RESOLUTIONS],
        [math.log(x) for x in tv_mean],
    )
    qv_rmse_slope = slope(
        [math.log(n) for n in RESOLUTIONS],
        [math.log(x) for x in qv_rmse],
    )

    return {
        "means": means,
        "variances": variances,
        "covariance_matrix": covariance_matrix,
        "disjoint_cov": disjoint_cov,
        "fourth_w1": fourth_w1,
        "qv_mean": qv_mean,
        "qv_rmse": qv_rmse,
        "qv_theory_rmse": qv_theory_rmse,
        "tv_mean": tv_mean,
        "tv_theory": tv_theory,
        "tv_log_slope": tv_log_slope,
        "qv_rmse_slope": qv_rmse_slope,
        "first_path": first_path,
    }


def track_c() -> dict[str, object]:
    rng = random.Random(SEED + 1)
    t0 = 0.5
    hs = [2.0 ** (-k) for k in range(3, 9)]
    samples = 40000
    brownian_mse: list[float] = []
    shared_mse: list[float] = []
    independent_mse: list[float] = []

    for h in hs:
        b_sum = 0.0
        s_sum = 0.0
        i_sum = 0.0
        shared_scale = math.sqrt(t0 + h) - math.sqrt(t0)
        for _ in range(samples):
            z_b = rng.gauss(0.0, 1.0)
            z_s = rng.gauss(0.0, 1.0)
            z_0 = rng.gauss(0.0, 1.0)
            z_1 = rng.gauss(0.0, 1.0)
            d_b = math.sqrt(h) * z_b
            d_s = shared_scale * z_s
            d_i = math.sqrt(t0 + h) * z_1 - math.sqrt(t0) * z_0
            b_sum += d_b * d_b
            s_sum += d_s * d_s
            i_sum += d_i * d_i
        brownian_mse.append(b_sum / samples)
        shared_mse.append(s_sum / samples)
        independent_mse.append(i_sum / samples)

    log_h = [math.log(h) for h in hs]
    orders = {
        "brownian": slope(log_h, [math.log(x) for x in brownian_mse]),
        "shared": slope(log_h, [math.log(x) for x in shared_mse]),
        "independent": slope(log_h, [math.log(x) for x in independent_mse]),
    }
    return {
        "t0": t0,
        "hs": hs,
        "brownian_mse": brownian_mse,
        "shared_mse": shared_mse,
        "independent_mse": independent_mse,
        "orders": orders,
    }


def make_svg(ab: dict[str, object], c: dict[str, object]) -> str:
    width, height = 1200, 430
    navy = "#0f172a"
    slate = "#475569"
    axis = "#94a3b8"
    blue = "#2563eb"
    green = "#059669"
    orange = "#ea580c"
    violet = "#7c3aed"

    path = ab["first_path"]
    assert isinstance(path, list)
    sample_ids = list(range(0, len(path), 16))
    if sample_ids[-1] != len(path) - 1:
        sample_ids.append(len(path) - 1)
    sample_values = [path[i] for i in sample_ids]
    lo, hi = min(sample_values), max(sample_values)
    span = max(hi - lo, 1e-12)
    path_points = [
        (70 + 285 * i / N_MAX, 310 - 175 * (path[i] - lo) / span)
        for i in sample_ids
    ]

    qv_mean = ab["qv_mean"]
    tv_mean = ab["tv_mean"]
    assert isinstance(qv_mean, list) and isinstance(tv_mean, list)
    log_ns = [math.log2(n) for n in RESOLUTIONS]
    x0, x1 = min(log_ns), max(log_ns)

    def bx(x: float) -> float:
        return 465 + 275 * (x - x0) / (x1 - x0)

    def by(y: float) -> float:
        return 315 - 180 * (y - 0.70) / (1.08 - 0.70)

    qv_points = [(bx(x), by(y)) for x, y in zip(log_ns, qv_mean)]
    tv_norm = [v / math.sqrt(n) for v, n in zip(tv_mean, RESOLUTIONS)]
    tv_points = [(bx(x), by(y)) for x, y in zip(log_ns, tv_norm)]

    hs = c["hs"]
    b_mse = c["brownian_mse"]
    s_mse = c["shared_mse"]
    i_mse = c["independent_mse"]
    assert isinstance(hs, list)
    assert isinstance(b_mse, list) and isinstance(s_mse, list) and isinstance(i_mse, list)
    log_hs = [math.log2(h) for h in hs]
    all_logs = [math.log10(y) for y in b_mse + s_mse + i_mse]
    lx0, lx1 = min(log_hs), max(log_hs)
    ly0, ly1 = min(all_logs) - 0.15, max(all_logs) + 0.15

    def cx(x: float) -> float:
        return 850 + 285 * (x - lx0) / (lx1 - lx0)

    def cy(y: float) -> float:
        return 315 - 180 * (y - ly0) / (ly1 - ly0)

    b_points = [(cx(x), cy(math.log10(y))) for x, y in zip(log_hs, b_mse)]
    s_points = [(cx(x), cy(math.log10(y))) for x, y in zip(log_hs, s_mse)]
    i_points = [(cx(x), cy(math.log10(y))) for x, y in zip(log_hs, i_mse)]

    means = ab["means"]
    variances = ab["variances"]
    assert isinstance(means, list) and isinstance(variances, list)
    orders = c["orders"]
    assert isinstance(orders, dict)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">DYN-09 Brownian 增量、路径粗糙性与时间耦合审计</title>
<desc id="desc">三面板显示Brownian路径与联合矩、quadratic variation和total variation的不同缩放，以及三种相同边缘分布时间耦合的增量均方差。</desc>
<style>text{{font-family:Inter,'PingFang SC','Noto Sans CJK SC',Arial,sans-serif;font-variant-numeric:tabular-nums lining-nums}}</style>
<rect width="1200" height="430" fill="#ffffff"/>
<text x="20" y="32" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="24" font-weight="700" fill="{navy}">DYN-09 · joint law → variation → temporal coupling</text>

<rect x="20" y="55" width="370" height="355" fill="#fffefb" stroke="#d6dee8" stroke-width="1.5"/>
<text x="42" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="22" font-weight="700" fill="{navy}">A　路径与跨时间联合矩</text>
<line x1="70" y1="315" x2="355" y2="315" stroke="{axis}" stroke-width="1.3"/>
<line x1="70" y1="125" x2="70" y2="315" stroke="{axis}" stroke-width="1.3"/>
{polyline(path_points, blue, 1.6)}
<text x="78" y="116" font-family="Georgia,'Times New Roman',serif" font-size="15" font-weight="600" fill="{navy}">one nested Brownian path</text>
<text x="79" y="343" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{slate}">t</text>
<text x="46" y="210" transform="rotate(-90 46 210)" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{slate}">W_t</text>
<text x="78" y="367" font-family="Georgia,'Times New Roman',serif" font-size="15" font-weight="600" fill="{navy}">Var(W_1)={variances[-1]:.4f}; E[W_1]={means[-1]:+.4f}</text>
<text x="78" y="389" font-family="Georgia,'Times New Roman',serif" font-size="15" fill="{slate}">disjoint increment cov={ab["disjoint_cov"]:+.3e}</text>

<rect x="415" y="55" width="370" height="355" fill="#fffefb" stroke="#d6dee8" stroke-width="1.5"/>
<text x="437" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="22" font-weight="700" fill="{navy}">B　平方变差与绝对变差</text>
<line x1="465" y1="315" x2="740" y2="315" stroke="{axis}" stroke-width="1.3"/>
<line x1="465" y1="125" x2="465" y2="315" stroke="{axis}" stroke-width="1.3"/>
{polyline(qv_points, violet, 2.2)}
{circles(qv_points, violet)}
{polyline(tv_points, green, 2.2)}
{circles(tv_points, green)}
<text x="478" y="116" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{violet}">QV / limit 1</text>
<text x="617" y="116" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{green}">TV / √N</text>
<text x="676" y="338" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{slate}">log₂ N</text>
<text x="461" y="367" font-family="Georgia,'Times New Roman',serif" font-size="15" font-weight="600" fill="{navy}">TV slope={ab["tv_log_slope"]:.4f} (theory 0.5)</text>
<text x="461" y="389" font-family="Georgia,'Times New Roman',serif" font-size="15" fill="{slate}">QV RMSE slope={ab["qv_rmse_slope"]:.4f} (theory -0.5)</text>

<rect x="810" y="55" width="370" height="355" fill="#fffefb" stroke="#d6dee8" stroke-width="1.5"/>
<text x="832" y="88" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="22" font-weight="700" fill="{navy}">C　同边缘，不同增量阶</text>
<line x1="850" y1="315" x2="1135" y2="315" stroke="{axis}" stroke-width="1.3"/>
<line x1="850" y1="125" x2="850" y2="315" stroke="{axis}" stroke-width="1.3"/>
{polyline(b_points, blue, 2.2)}
{circles(b_points, blue)}
{polyline(s_points, green, 2.2)}
{circles(s_points, green)}
{polyline(i_points, orange, 2.2)}
{circles(i_points, orange)}
<text x="858" y="116" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{blue}">Brownian</text>
<text x="944" y="116" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{green}">shared</text>
<text x="1016" y="116" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{orange}">independent</text>
<text x="1070" y="338" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{slate}">log₂ h</text>
<text x="826" y="235" transform="rotate(-90 826 235)" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{slate}">log₁₀ increment MSE</text>
<text x="848" y="367" font-family="Georgia,'Times New Roman',serif" font-size="15" font-weight="600" fill="{navy}">orders = {orders["brownian"]:.3f} / {orders["shared"]:.3f} / {orders["independent"]:.3f}</text>
<text x="848" y="389" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="{slate}">theory 1 / 2 / 0；marginals N(0,t)</text>

<rect x="960" y="407" width="200" height="22" rx="11" fill="#ecfdf5" stroke="#10b981"/>
<text x="980" y="424" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif" font-size="15" fill="#047857">all assertions passed</text>
</svg>"""


def assert_results(ab: dict[str, object], c: dict[str, object]) -> None:
    means = ab["means"]
    variances = ab["variances"]
    cov = ab["covariance_matrix"]
    qv_mean = ab["qv_mean"]
    qv_rmse = ab["qv_rmse"]
    qv_theory = ab["qv_theory_rmse"]
    tv_mean = ab["tv_mean"]
    tv_theory = ab["tv_theory"]
    assert isinstance(means, list) and isinstance(variances, list)
    assert isinstance(cov, list) and isinstance(qv_mean, list)
    assert isinstance(qv_rmse, list) and isinstance(qv_theory, list)
    assert isinstance(tv_mean, list) and isinstance(tv_theory, list)

    assert max(abs(x) for x in means) < 0.12
    assert max(abs(v - t) for v, t in zip(variances, TIMES)) < 0.09
    cov_error = max(
        abs(cov[i][j] - min(TIMES[i], TIMES[j]))
        for i in range(len(TIMES))
        for j in range(len(TIMES))
    )
    assert cov_error < 0.09
    assert abs(float(ab["disjoint_cov"])) < 0.05
    assert abs(float(ab["fourth_w1"]) - 3.0) < 0.45
    assert max(abs(x - 1.0) for x in qv_mean) < 0.035
    assert all(0.82 < x / y < 1.18 for x, y in zip(qv_rmse, qv_theory))
    assert all(0.97 < x / y < 1.03 for x, y in zip(tv_mean, tv_theory))
    assert 0.485 < float(ab["tv_log_slope"]) < 0.515
    assert -0.54 < float(ab["qv_rmse_slope"]) < -0.46

    hs = c["hs"]
    b_mse = c["brownian_mse"]
    s_mse = c["shared_mse"]
    i_mse = c["independent_mse"]
    orders = c["orders"]
    assert isinstance(hs, list) and isinstance(b_mse, list)
    assert isinstance(s_mse, list) and isinstance(i_mse, list)
    assert isinstance(orders, dict)
    t0 = float(c["t0"])
    assert all(abs(x / h - 1.0) < 0.04 for x, h in zip(b_mse, hs))
    shared_exact = [(math.sqrt(t0 + h) - math.sqrt(t0)) ** 2 for h in hs]
    independent_exact = [2.0 * t0 + h for h in hs]
    assert all(abs(x / y - 1.0) < 0.04 for x, y in zip(s_mse, shared_exact))
    assert all(abs(x / y - 1.0) < 0.04 for x, y in zip(i_mse, independent_exact))
    assert 0.96 < float(orders["brownian"]) < 1.04
    assert 1.94 < float(orders["shared"]) < 2.04
    assert -0.04 < float(orders["independent"]) < 0.04


def main() -> None:
    ab = track_ab()
    c = track_c()
    assert_results(ab, c)
    PLOT.parent.mkdir(parents=True, exist_ok=True)
    PLOT.write_text(make_svg(ab, c), encoding="utf-8")
    digest = hashlib.sha256(PLOT.read_bytes()).hexdigest()

    print("TRACK A — BROWNIAN JOINT-LAW AUDIT")
    print("times=" + ",".join(f"{t:.2f}" for t in TIMES))
    print("means=" + ",".join(f"{x:+.8f}" for x in ab["means"]))
    print("variances=" + ",".join(f"{x:.8f}" for x in ab["variances"]))
    cov = ab["covariance_matrix"]
    cov_error = max(
        abs(cov[i][j] - min(TIMES[i], TIMES[j]))
        for i in range(len(TIMES))
        for j in range(len(TIMES))
    )
    print(f"covariance_kernel_max_error={cov_error:.12e}")
    print(f"disjoint_increment_cov={ab['disjoint_cov']:+.12e}")
    print(f"E_W1_fourth={ab['fourth_w1']:.8f}")

    print("TRACK B — NESTED VARIATION AUDIT")
    for n, qm, qr, tm in zip(
        RESOLUTIONS, ab["qv_mean"], ab["qv_rmse"], ab["tv_mean"]
    ):
        print(f"N={n:4d} qv_mean={qm:.8f} qv_rmse={qr:.8f} tv_mean={tm:.8f}")
    print(f"tv_log_slope={ab['tv_log_slope']:.8f}")
    print(f"qv_rmse_log_slope={ab['qv_rmse_slope']:.8f}")

    print("TRACK C — SAME MARGINALS, DIFFERENT COUPLINGS")
    print(
        "orders="
        f"{c['orders']['brownian']:.8f},"
        f"{c['orders']['shared']:.8f},"
        f"{c['orders']['independent']:.8f}"
    )
    print(
        "smallest_h_mse="
        f"{c['brownian_mse'][-1]:.12e},"
        f"{c['shared_mse'][-1]:.12e},"
        f"{c['independent_mse'][-1]:.12e}"
    )
    print(f"SVG={PLOT}")
    print(f"SHA256={digest}")
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
