#!/usr/bin/env python3
"""Reproduce the GEO-07 positive-kernel, representer, KRR/GP, and RFF audit.

Requires NumPy only. A fixed root seed makes all stochastic tracks reproducible.
The script writes one dependency-free SVG and prints the canonical metrics/hash.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np


VAULT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    VAULT_ROOT
    / "00-知识库管理"
    / "_assets"
    / "plots"
    / "functional-analysis"
    / "plot-rkhs-krr-rff-v2.svg"
)
ROOT_SEED = 20260819


def rbf_kernel(x: np.ndarray, z: np.ndarray, ell: float) -> np.ndarray:
    """RBF Gram/cross-Gram for row-wise observations."""
    x = np.atleast_2d(x)
    z = np.atleast_2d(z)
    sq = np.sum(x * x, axis=1)[:, None] + np.sum(z * z, axis=1)[None, :] - 2.0 * x @ z.T
    return np.exp(-np.maximum(sq, 0.0) / (2.0 * ell * ell))


def track_gram_spectra() -> dict[str, np.ndarray | float]:
    x = np.linspace(-1.5, 1.5, 24)[:, None]
    k_rbf = rbf_kernel(x, x, ell=0.42)
    d2 = (x - x.T) ** 2
    k_bad = -d2
    eig_rbf = np.linalg.eigvalsh((k_rbf + k_rbf.T) / 2.0)
    eig_bad = np.linalg.eigvalsh((k_bad + k_bad.T) / 2.0)
    c = np.ones(len(x))
    c[1::2] = -1.0
    # This coefficient is not chosen as a negative witness; minimum eigenvalue is.
    return {
        "eig_rbf": eig_rbf,
        "eig_bad": eig_bad,
        "rbf_min": float(eig_rbf[0]),
        "bad_min": float(eig_bad[0]),
        "bad_max": float(eig_bad[-1]),
        "symmetry_residual": float(np.linalg.norm(k_rbf - k_rbf.T, ord="fro")),
    }


def track_representer_projection() -> dict[str, np.ndarray | float]:
    rng = np.random.default_rng(ROOT_SEED + 1)
    n, d, p = 18, 3, 80
    x = rng.normal(size=(n, d))
    omega = rng.normal(scale=1.0 / 0.9, size=(p, d))
    phase = rng.uniform(0.0, 2.0 * math.pi, size=p)
    phi = math.sqrt(2.0 / p) * np.cos(x @ omega.T + phase)
    weight = rng.normal(size=p)

    _, singular, vt = np.linalg.svd(phi, full_matrices=True)
    rank = int(np.sum(singular > singular[0] * 1e-12))
    row_basis = vt[:rank].T
    weight_parallel = row_basis @ (row_basis.T @ weight)
    weight_perp = weight - weight_parallel

    pred_full = phi @ weight
    pred_parallel = phi @ weight_parallel
    pred_gap = float(np.max(np.abs(pred_full - pred_parallel)))
    orth_residual = float(np.linalg.norm(phi @ weight_perp))
    norm_full = float(np.linalg.norm(weight))
    norm_parallel = float(np.linalg.norm(weight_parallel))
    norm_perp = float(np.linalg.norm(weight_perp))
    pythagoras_residual = abs(norm_full**2 - norm_parallel**2 - norm_perp**2)

    return {
        "rank": rank,
        "singular": singular,
        "pred_gap": pred_gap,
        "orth_residual": orth_residual,
        "norm_full": norm_full,
        "norm_parallel": norm_parallel,
        "norm_perp": norm_perp,
        "pythagoras_residual": pythagoras_residual,
    }


def track_krr_gp() -> dict[str, np.ndarray | float]:
    rng = np.random.default_rng(ROOT_SEED + 2)
    x_train = np.linspace(-2.8, 2.8, 14)[:, None]
    truth_train = np.sin(1.35 * x_train[:, 0]) + 0.18 * x_train[:, 0]
    sigma = 0.18
    y = truth_train + rng.normal(scale=sigma, size=len(x_train))
    ell = 0.72
    k_train = rbf_kernel(x_train, x_train, ell)
    sigma2 = sigma * sigma
    lam = sigma2 / len(x_train)

    system = k_train + sigma2 * np.eye(len(x_train))
    alpha_gp = np.linalg.solve(system, y)
    alpha_krr = np.linalg.solve(k_train + len(x_train) * lam * np.eye(len(x_train)), y)

    x_test = np.linspace(-3.3, 3.3, 360)[:, None]
    k_cross = rbf_kernel(x_test, x_train, ell)
    mean_gp = k_cross @ alpha_gp
    mean_krr = k_cross @ alpha_krr
    solve_cross = np.linalg.solve(system, k_cross.T)
    latent_var = 1.0 - np.sum(k_cross * solve_cross.T, axis=1)
    latent_var = np.maximum(latent_var, 0.0)
    truth_test = np.sin(1.35 * x_test[:, 0]) + 0.18 * x_test[:, 0]

    return {
        "x_train": x_train[:, 0],
        "y": y,
        "x_test": x_test[:, 0],
        "truth_test": truth_test,
        "mean_gp": mean_gp,
        "mean_krr": mean_krr,
        "std_gp": np.sqrt(latent_var),
        "mean_gap": float(np.max(np.abs(mean_gp - mean_krr))),
        "lambda": lam,
        "sigma2": sigma2,
        "condition": float(np.linalg.cond(system)),
        "solve_residual": float(np.linalg.norm(system @ alpha_gp - y) / np.linalg.norm(y)),
    }


def track_rff() -> dict[str, np.ndarray | float]:
    rng_points = np.random.default_rng(ROOT_SEED + 3)
    x = rng_points.uniform(-2.0, 2.0, size=(72, 2))
    ell = 0.85
    exact = rbf_kernel(x, x, ell)
    exact_norm = np.linalg.norm(exact, ord="fro")
    dimensions = np.array([8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    repetitions = 48
    errors = np.empty((repetitions, len(dimensions)))

    # Independent features at each D avoid implying pathwise monotonicity.
    for rep in range(repetitions):
        for j, dim in enumerate(dimensions):
            rng = np.random.default_rng(ROOT_SEED + 1000 + 97 * rep + int(dim))
            omega = rng.normal(scale=1.0 / ell, size=(dim, x.shape[1]))
            phase = rng.uniform(0.0, 2.0 * math.pi, size=dim)
            z = math.sqrt(2.0 / dim) * np.cos(x @ omega.T + phase)
            approx = z @ z.T
            errors[rep, j] = np.linalg.norm(approx - exact, ord="fro") / exact_norm

    mean = errors.mean(axis=0)
    q10, q90 = np.quantile(errors, [0.1, 0.9], axis=0)
    slope = float(np.polyfit(np.log(dimensions), np.log(mean), deg=1)[0])
    nonmonotone_fraction = float(np.mean(np.any(np.diff(errors, axis=1) > 0.0, axis=1)))
    return {
        "dimensions": dimensions,
        "errors": errors,
        "mean": mean,
        "q10": q10,
        "q90": q90,
        "slope": slope,
        "nonmonotone_fraction": nonmonotone_fraction,
        "repetitions": repetitions,
    }


def _lin(values: np.ndarray, lo: float, hi: float, out_lo: float, out_hi: float) -> np.ndarray:
    return out_lo + (values - lo) * (out_hi - out_lo) / (hi - lo)


def _log(values: np.ndarray, lo: float, hi: float, out_lo: float, out_hi: float) -> np.ndarray:
    logs = np.log10(np.clip(values, 1e-300, None))
    return _lin(logs, math.log10(lo), math.log10(hi), out_lo, out_hi)


def _symlog(values: np.ndarray, scale: float = 1e-9) -> np.ndarray:
    return np.sign(values) * np.log10(1.0 + np.abs(values) / scale)


def _polyline(x: np.ndarray, y: np.ndarray, cls: str) -> str:
    points = " ".join(f"{a:.2f},{b:.2f}" for a, b in zip(x, y))
    return f'<polyline class="{cls}" points="{points}"/>'


def make_plot(
    gram: dict[str, np.ndarray | float],
    projection: dict[str, np.ndarray | float],
    regression: dict[str, np.ndarray | float],
    rff: dict[str, np.ndarray | float],
) -> None:
    width, height = 1200, 710
    panels = {
        "a": (65.0, 120.0, 470.0, 190.0),
        "b": (665.0, 120.0, 470.0, 190.0),
        "c": (65.0, 440.0, 470.0, 190.0),
        "d": (665.0, 440.0, 470.0, 190.0),
    }
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">GEO-07 正定核、表示定理、KRR-GP 与随机特征四轨审计</title>',
        '<desc id="desc">比较合法与非法 Gram 谱，展示样本张成空间投影保持预测并降低范数，验证 KRR 与 GP 后验均值一致，并显示随机傅里叶特征误差的分布收敛。</desc>',
        '<defs><style>',
        'svg{font-family:"Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
        '.bg{fill:#fff}.panel{fill:#fff;stroke:#cbd5e1;stroke-width:1.4}.ttl{font:700 22px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#0f172a}.sub{font:500 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#475569}.axis{stroke:#64748b;stroke-width:1.2}.grid{stroke:#e2e8f0;stroke-width:1}.tick{font:500 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#64748b}.blue{fill:none;stroke:#2563eb;stroke-width:2.4}.rose{fill:none;stroke:#e11d48;stroke-width:2.2}.green{fill:none;stroke:#059669;stroke-width:2.5}.amber{fill:none;stroke:#d97706;stroke-width:1.8;stroke-dasharray:6 4}.gray{fill:none;stroke:#64748b;stroke-width:1.6;stroke-dasharray:5 4}.bandb{fill:#bfdbfe;fill-opacity:.58;stroke:none}.bandg{fill:#bbf7d0;fill-opacity:.62;stroke:none}.dotb{fill:#2563eb}.dotr{fill:#e11d48}.dotg{fill:#059669}.legend{font:600 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#334155}.bartext{font:600 15px "Inter","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#334155}',
        '</style></defs>',
        f'<rect class="bg" width="{width}" height="{height}"/>',
        '<text class="ttl" x="30" y="31">GEO-07 reproducibility audit · from finite PSD tests to finite kernel computation</text>',
        '<text class="sub" x="30" y="51">Root seed 20260819 · NumPy only · approximation trends are reported across 48 independent feature draws.</text>',
        '<rect class="panel" x="25" y="68" width="550" height="276"/>',
        '<rect class="panel" x="625" y="68" width="550" height="276"/>',
        '<rect class="panel" x="25" y="388" width="550" height="276"/>',
        '<rect class="panel" x="625" y="388" width="550" height="276"/>',
        '<text class="ttl" x="45" y="91">A  Symmetry ≠ PSD</text>',
        '<text class="sub" x="45" y="107">RBF Gram vs symmetric negative squared-distance matrix · symlog spectrum</text>',
        '<text class="ttl" x="645" y="91">B  Representer projection</text>',
        '<text class="sub" x="645" y="107">finite feature analogue of the representer projection proof</text>',
        '<text class="ttl" x="45" y="411">C  KRR mean = GP mean</text>',
        '<text class="sub" x="45" y="427">zero-mean GP with sigma² = n lambda compared to KRR</text>',
        '<text class="ttl" x="645" y="411">D  RFF: distribution, not pathwise</text>',
        '<text class="sub" x="645" y="427">relative Gram Frobenius error · mean and 10–90% over seeds</text>',
    ]
    for x, y, w, h in panels.values():
        svg.extend(
            [
                f'<line class="axis" x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}"/>',
                f'<line class="axis" x1="{x}" y1="{y}" x2="{x}" y2="{y+h}"/>',
            ]
        )

    # A: signed-log Gram spectra.
    ax, ay, aw, ah = panels["a"]
    idx = np.arange(1, len(gram["eig_rbf"]) + 1, dtype=float)
    sx = _lin(idx, idx.min(), idx.max(), ax, ax + aw)
    both = np.concatenate([gram["eig_rbf"], gram["eig_bad"]])
    transformed = _symlog(both)
    lo, hi = float(transformed.min()), float(transformed.max())
    y_rbf = _lin(_symlog(gram["eig_rbf"]), lo, hi, ay + ah, ay)
    y_bad = _lin(_symlog(gram["eig_bad"]), lo, hi, ay + ah, ay)
    y_zero = float(_lin(np.array([0.0]), lo, hi, ay + ah, ay)[0])
    svg.append(f'<line class="grid" x1="{ax}" y1="{y_zero:.2f}" x2="{ax+aw}" y2="{y_zero:.2f}"/>')
    svg.append(_polyline(sx, y_rbf, "blue"))
    svg.append(_polyline(sx, y_bad, "rose"))
    for xx, yy in zip(sx, y_rbf):
        svg.append(f'<circle class="dotb" cx="{xx:.2f}" cy="{yy:.2f}" r="2.5"/>')
    for xx, yy in zip(sx, y_bad):
        svg.append(f'<circle class="dotr" cx="{xx:.2f}" cy="{yy:.2f}" r="2.5"/>')
    svg.extend(
        [
            f'<text class="legend" x="{ax+12}" y="{ay+18}">RBF PSD · min {gram["rbf_min"]:.1e}</text>',
            f'<text class="legend" x="{ax+12}" y="{ay+34}">-|x-z|² · min {gram["bad_min"]:.2f}</text>',
            f'<text class="tick" x="{ax+aw/2}" y="{ay+ah+20}" text-anchor="middle">ordered eigenvalue index</text>',
            f'<text class="tick" x="{ax-8}" y="{y_zero+3:.2f}" text-anchor="end">0</text>',
        ]
    )

    # B: norm bars.
    bx, by, bw, bh = panels["b"]
    norms = np.array([projection["norm_full"], projection["norm_parallel"], projection["norm_perp"]], dtype=float)
    labels = ["full w", "sample span w∥", "orthogonal w⊥"]
    colors = ["#64748b", "#7c3aed", "#f59e0b"]
    xpos = np.array([bx + 95.0, bx + 235.0, bx + 375.0])
    # Reserve a clean evidence strip above the bars for the two audit statistics.
    tops = _lin(norms, 0.0, float(norms.max()) * 1.45, by + bh, by)
    for xx, top, val, label, color in zip(xpos, tops, norms, labels, colors):
        svg.append(f'<rect x="{xx-36:.2f}" y="{top:.2f}" width="72" height="{by+bh-top:.2f}" rx="6" fill="{color}" fill-opacity=".88"/>')
        svg.append(f'<text class="bartext" x="{xx:.2f}" y="{top-7:.2f}" text-anchor="middle">{val:.2f}</text>')
        svg.append(f'<text class="tick" x="{xx:.2f}" y="{by+bh+20:.2f}" text-anchor="middle">{label}</text>')
    svg.extend(
        [
            f'<text class="legend" x="{bx+bw-10}" y="{by+18}" text-anchor="end">max prediction gap = {projection["pred_gap"]:.1e}</text>',
            f'<text class="legend" x="{bx+bw-10}" y="{by+34}" text-anchor="end">sample feature rank = {projection["rank"]} of 80</text>',
        ]
    )

    # C: regression, posterior band, and observations.
    cx, cy, cw, ch = panels["c"]
    xt = regression["x_test"]
    mean = regression["mean_gp"]
    std = regression["std_gp"]
    lower, upper = mean - 1.96 * std, mean + 1.96 * std
    all_y = np.concatenate([lower, upper, regression["truth_test"], regression["y"]])
    ylo, yhi = float(all_y.min() - 0.1), float(all_y.max() + 0.1)
    px = _lin(xt, float(xt.min()), float(xt.max()), cx, cx + cw)
    py_lower = _lin(lower, ylo, yhi, cy + ch, cy)
    py_upper = _lin(upper, ylo, yhi, cy + ch, cy)
    polygon = " ".join(f"{x:.2f},{y:.2f}" for x, y in zip(px, py_upper)) + " " + " ".join(
        f"{x:.2f},{y:.2f}" for x, y in zip(px[::-1], py_lower[::-1])
    )
    svg.append(f'<polygon class="bandb" points="{polygon}"/>')
    svg.append(_polyline(px, _lin(regression["truth_test"], ylo, yhi, cy + ch, cy), "gray"))
    svg.append(_polyline(px, _lin(mean, ylo, yhi, cy + ch, cy), "blue"))
    train_x = _lin(regression["x_train"], float(xt.min()), float(xt.max()), cx, cx + cw)
    train_y = _lin(regression["y"], ylo, yhi, cy + ch, cy)
    for xx, yy in zip(train_x, train_y):
        svg.append(f'<circle class="dotr" cx="{xx:.2f}" cy="{yy:.2f}" r="3.3" stroke="white" stroke-width=".7"/>')
    svg.extend(
        [
            f'<text class="legend" x="{cx+12}" y="{cy+18}">blue: GP mean = KRR · band: latent 95%</text>',
            f'<text class="legend" x="{cx+12}" y="{cy+34}">max mean gap {regression["mean_gap"]:.1e} · sigma²=n lambda={regression["sigma2"]:.4f}</text>',
            f'<text class="tick" x="{cx+cw/2}" y="{cy+ch+20}" text-anchor="middle">input x</text>',
        ]
    )

    # D: RFF log-log mean, quantile band, reference.
    dx, dy, dw, dh = panels["d"]
    dims = rff["dimensions"].astype(float)
    mean_error = rff["mean"]
    ref = mean_error[0] * np.sqrt(dims[0] / dims)
    error_lo = float(min(np.min(rff["q10"]), np.min(ref)) * 0.8)
    error_hi = float(max(np.max(rff["q90"]), np.max(ref)) * 1.2)
    qx = _log(dims, float(dims.min()), float(dims.max()), dx, dx + dw)
    q10y = _log(rff["q10"], error_lo, error_hi, dy + dh, dy)
    q90y = _log(rff["q90"], error_lo, error_hi, dy + dh, dy)
    polygon = " ".join(f"{x:.2f},{y:.2f}" for x, y in zip(qx, q90y)) + " " + " ".join(
        f"{x:.2f},{y:.2f}" for x, y in zip(qx[::-1], q10y[::-1])
    )
    svg.append(f'<polygon class="bandg" points="{polygon}"/>')
    svg.append(_polyline(qx, _log(mean_error, error_lo, error_hi, dy + dh, dy), "green"))
    svg.append(_polyline(qx, _log(ref, error_lo, error_hi, dy + dh, dy), "amber"))
    for xx, yy in zip(qx, _log(mean_error, error_lo, error_hi, dy + dh, dy)):
        svg.append(f'<circle class="dotg" cx="{xx:.2f}" cy="{yy:.2f}" r="3"/>')
    for dim, xx in zip(dims, qx):
        svg.append(f'<text class="tick" x="{xx:.2f}" y="{dy+dh+20}" text-anchor="middle">{int(dim)}</text>')
    svg.extend(
        [
            f'<text class="legend" x="{dx+12}" y="{dy+18}">mean slope = {rff["slope"]:.3f} · dashed D^-1/2</text>',
            f'<text class="legend" x="{dx+12}" y="{dy+34}">nonmonotone seed paths = {100*rff["nonmonotone_fraction"]:.0f}%</text>',
        ]
    )
    svg.extend(
        [
            '<text class="sub" x="600" y="697" text-anchor="middle">Generated by rkhs_kernel_audit.py · exact Gram/KRR calculations and fixed-seed RFF Monte Carlo · no plotting dependency</text>',
            '</svg>',
        ]
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg) + "\n", encoding="utf-8")


def main() -> None:
    gram = track_gram_spectra()
    projection = track_representer_projection()
    regression = track_krr_gp()
    rff = track_rff()

    assert gram["rbf_min"] > -1e-10
    assert gram["bad_min"] < -1.0 and gram["bad_max"] > 1.0
    assert projection["pred_gap"] < 1e-12
    assert projection["pythagoras_residual"] < 1e-10
    assert projection["norm_parallel"] < projection["norm_full"]
    assert regression["mean_gap"] < 1e-13
    assert regression["solve_residual"] < 1e-12
    assert -0.60 < rff["slope"] < -0.40
    assert rff["nonmonotone_fraction"] > 0.25

    make_plot(gram, projection, regression, rff)
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()

    print(f"root_seed={ROOT_SEED}")
    print(f"rbf_gram_min_eigenvalue={gram['rbf_min']:.12e}")
    print(f"invalid_distance_min_eigenvalue={gram['bad_min']:.12e}")
    print(f"invalid_distance_max_eigenvalue={gram['bad_max']:.12e}")
    print(f"representer_sample_rank={projection['rank']}")
    print(f"representer_prediction_gap={projection['pred_gap']:.12e}")
    print(f"representer_norm_full={projection['norm_full']:.12e}")
    print(f"representer_norm_parallel={projection['norm_parallel']:.12e}")
    print(f"representer_norm_perp={projection['norm_perp']:.12e}")
    print(f"representer_pythagoras_residual={projection['pythagoras_residual']:.12e}")
    print(f"krr_gp_max_mean_gap={regression['mean_gap']:.12e}")
    print(f"krr_gp_sigma2={regression['sigma2']:.12e}")
    print(f"krr_gp_lambda={regression['lambda']:.12e}")
    print(f"krr_system_condition={regression['condition']:.12e}")
    print(f"krr_solve_relative_residual={regression['solve_residual']:.12e}")
    print(f"rff_repetitions={rff['repetitions']}")
    print(f"rff_mean_log_slope={rff['slope']:.12f}")
    print(f"rff_nonmonotone_path_fraction={rff['nonmonotone_fraction']:.12f}")
    print(f"rff_D8_mean_error={rff['mean'][0]:.12e}")
    print(f"rff_D2048_mean_error={rff['mean'][-1]:.12e}")
    print(f"output={OUTPUT}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
