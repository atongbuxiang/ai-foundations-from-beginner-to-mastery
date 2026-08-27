#!/usr/bin/env python3
"""Deterministic experiment for propagation, condition estimation, and stopping."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "error-propagation" / "plot-condition-estimation-stopping-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def matvec(a, x):
    return [dot(row, x) for row in a]


def transpose(a):
    return [list(col) for col in zip(*a)]


def lu_factor(a0):
    a = [row[:] for row in a0]
    n = len(a)
    piv = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if abs(a[p][k]) < 1e-30:
            raise ValueError("singular")
        if p != k:
            a[k], a[p] = a[p], a[k]
            piv[k], piv[p] = piv[p], piv[k]
        for i in range(k + 1, n):
            a[i][k] /= a[k][k]
            for j in range(k + 1, n):
                a[i][j] -= a[i][k] * a[k][j]
    return a, piv


def lu_solve(fact, b):
    lu, piv = fact
    n = len(lu)
    x = [b[piv[i]] for i in range(n)]
    for i in range(n):
        x[i] -= sum(lu[i][j] * x[j] for j in range(i))
    for i in range(n - 1, -1, -1):
        x[i] = (x[i] - sum(lu[i][j] * x[j] for j in range(i + 1, n))) / lu[i][i]
    return x


def norm1_matrix(a):
    return max(sum(abs(a[i][j]) for i in range(len(a))) for j in range(len(a[0])))


def inverse_norm1_exact(a):
    fact = lu_factor(a)
    n = len(a)
    col_sums = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        col_sums.append(sum(abs(v) for v in lu_solve(fact, e)))
    return max(col_sums)


def hager_higham_inverse_norm1(a, maxit=12):
    """Compact Hager/Higham-style estimator using A and A^T solves."""
    n = len(a)
    fa = lu_factor(a)
    fat = lu_factor(transpose(a))
    x = [1.0 / n] * n
    est = 0.0
    old_j = -1
    for _ in range(maxit):
        y = lu_solve(fa, x)
        est_new = sum(abs(v) for v in y)
        s = [1.0 if v >= 0.0 else -1.0 for v in y]
        z = lu_solve(fat, s)
        j = max(range(n), key=lambda i: abs(z[i]))
        if est_new <= est or j == old_j or abs(z[j]) <= dot(z, x):
            est = max(est, est_new)
            break
        est = est_new
        x = [0.0] * n
        x[j] = 1.0
        old_j = j
    # Higham-style alternating safeguard.
    alt = [((-1.0) ** i) * (1.0 + i / max(n - 1, 1)) for i in range(n)]
    na = sum(abs(v) for v in alt)
    y = lu_solve(fa, [v / na for v in alt])
    return max(est, sum(abs(v) for v in y))


def hilbert(n):
    return [[1.0 / (i + j + 1.0) for j in range(n)] for i in range(n)]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def log_y(v, lo, hi, y0, h):
    v = max(lo, min(hi, v))
    return y0 + h - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * h


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo, xhi = xticks[0][0], xticks[-1][0]
    for value, label in xticks:
        x = x0 + (value - xlo) / (xhi - xlo) * w
        out += [
            f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>',
            f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>',
        ]
    ylo, yhi = yticks[0][0], yticks[-1][0]
    for value, label in yticks:
        y = log_y(value, ylo, yhi, y0, h)
        out += [
            f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>',
            f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>',
        ]
    out += [
        f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>',
        f'<text x="{x0-58}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-58} {y0+h/2})">{esc(ylabel)}</text>',
    ]
    return out


def poly(points, color, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.6"{d}/>'


def mark(x, y, color, shape="circle", r=3.5):
    if shape == "square":
        return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    layers = list(range(31))
    gains = [0.85, 1.0, 1.15]
    prop = {g: [g**k for k in layers] for g in gains}

    estimates = []
    for n in range(2, 10):
        a = hilbert(n)
        norm_a = norm1_matrix(a)
        true = norm_a * inverse_norm1_exact(a)
        estimate = norm_a * hager_higham_inverse_norm1(a)
        estimates.append((n, true, estimate))

    eps = 1e-6
    rho = 0.9
    stop = []
    for k in range(181):
        weak_error = rho**k
        forward = weak_error / math.sqrt(2.0)
        residual = eps * weak_error / math.sqrt(1.0 + eps * eps)
        stop.append((k, residual, forward, residual / eps))

    W, H = 1440, 610
    y0, h, w = 88, 330, 330
    xs = [75, 555, 1035]
    colors = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">Error propagation, condition estimation, and stopping rules</title>',
        '<desc id="desc">Three panels show products of local sensitivities, true and estimated Hilbert matrix condition numbers, and premature residual-only stopping on an ill-conditioned system.</desc>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        '<text x="720" y="34" text-anchor="middle" class="title">误差传播、条件估计与停止：小残差必须经过敏感度解释</text>',
        '<text x="75" y="67" class="panel">A  局部 Jacobian 的连乘：衰减、保持与放大</text>',
        '<text x="555" y="67" class="panel">B  不显式求逆的 1-范数条件估计</text>',
        '<text x="1035" y="67" class="panel">C  病态方向中 residual-only 会过早停止</text>',
    ]

    # Panel A
    svg += axes(xs[0], y0, w, h, [(0, "0"), (10, "10"), (20, "20"), (30, "30")],
                [(1e-3, "1e−3"), (1e-2, "1e−2"), (1e-1, "1e−1"), (1, "1"), (10, "10"), (100, "1e2")],
                "层数 L", "|∂y_L/∂y_0|")
    for gain, color, shape in [(0.85, colors["blue"], "circle"), (1.0, colors["green"], "square"), (1.15, colors["red"], "diamond")]:
        pts = []
        for k, value in zip(layers, prop[gain]):
            x = xs[0] + k / 30 * w
            y = log_y(value, 1e-3, 100, y0, h)
            pts.append((x, y))
        svg.append(poly(pts, color))
        for k in (0, 10, 20, 30):
            svg.append(mark(pts[k][0], pts[k][1], color, shape))
    svg += [
        f'<text x="{xs[0]+18}" y="{y0+25}" class="note">每层局部增益只有 ±15%，30 层后却相差约 8700 倍</text>',
        f'<text x="{xs[0]+20}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">● g=0.85</text>',
        f'<text x="{xs[0]+115}" y="{y0+h+78}" class="legend" fill="{colors["green"]}">■ g=1</text>',
        f'<text x="{xs[0]+205}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">◆ g=1.15</text>',
    ]

    # Panel B
    svg += axes(xs[1], y0, w, h, [(2, "2"), (4, "4"), (6, "6"), (8, "8"), (9, "9")],
                [(1e1, "10¹"), (1e4, "10⁴"), (1e7, "10⁷"), (1e10, "10¹⁰"), (1e13, "10¹³"), (1e16, "10¹⁶")],
                "Hilbert 阶数 n", "κ₁(Hₙ)")
    true_pts, est_pts = [], []
    for n, true, est in estimates:
        x = xs[1] + (n - 2) / 7 * w
        true_pts.append((x, log_y(true, 1e1, 1e16, y0, h)))
        est_pts.append((x, log_y(est, 1e1, 1e16, y0, h)))
    svg.append(poly(true_pts, colors["red"]))
    svg.append(poly(est_pts, colors["purple"], "6 4"))
    for p in true_pts:
        svg.append(mark(p[0], p[1], colors["red"], "circle"))
    for p in est_pts:
        svg.append(mark(p[0], p[1], colors["purple"], "diamond"))
    svg += [
        f'<text x="{xs[1]+18}" y="{y0+25}" class="note">反向通信只要求 solve(A,·) 与 solve(Aᵀ,·)</text>',
        f'<text x="{xs[1]+35}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">● 显式参考 κ₁</text>',
        f'<text x="{xs[1]+180}" y="{y0+h+78}" class="legend" fill="{colors["purple"]}">◆ Hager–Higham 估计</text>',
    ]

    # Panel C
    svg += axes(xs[2], y0, w, h, [(0, "0"), (60, "60"), (120, "120"), (180, "180")],
                [(1e-16, "1e−16"), (1e-12, "1e−12"), (1e-8, "1e−8"), (1e-4, "1e−4"), (1, "1")],
                "迭代步 k", "相对量")
    keys = [(1, colors["blue"], "circle"), (2, colors["red"], "square"), (3, colors["purple"], "diamond")]
    all_pts = []
    for idx, color, shape in keys:
        pts = []
        for k, residual, forward, conditioned in stop:
            value = (residual, forward, conditioned)[idx - 1]
            x = xs[2] + k / 180 * w
            pts.append((x, log_y(value, 1e-16, 1, y0, h)))
        all_pts.append(pts)
        svg.append(poly(pts, color, "6 4" if idx == 3 else ""))
        for k in (0, 60, 120, 180):
            svg.append(mark(pts[k][0], pts[k][1], color, shape))
    tol_y = log_y(1e-8, 1e-16, 1, y0, h)
    svg += [
        f'<line x1="{xs[2]}" y1="{tol_y:.2f}" x2="{xs[2]+w}" y2="{tol_y:.2f}" stroke="{colors["green"]}" stroke-width="1.7" stroke-dasharray="3 4"/>',
        f'<text x="{xs[2]+w-8}" y="{tol_y-7:.2f}" text-anchor="end" class="note">residual tol = 1e−8</text>',
        f'<text x="{xs[2]+18}" y="{y0+25}" class="note">A=diag(1,1e−6)，误差位于弱方向</text>',
        f'<text x="{xs[2]+18}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">● residual</text>',
        f'<text x="{xs[2]+125}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">■ forward</text>',
        f'<text x="{xs[2]+225}" y="{y0+h+78}" class="legend" fill="{colors["purple"]}">◆ κr</text>',
    ]

    svg += [
        '<text x="720" y="568" text-anchor="middle" class="note">A：链式法则累积局部敏感度；B：条件估计只求逆的作用量；C：停止阈值必须结合条件性、真残差与任务尺度。</text>',
        '<text x="720" y="590" text-anchor="middle" class="note">生成：plot_condition_estimation_stopping.py · Python 标准库 · 确定性实验</text>',
        '</svg>',
    ]
    propagation_ratio = prop[1.15][-1] / prop[0.85][-1]
    if propagation_ratio <= 1e3:
        raise RuntimeError("depth sensitivity separation audit failed")
    if not all(0.9 <= estimate / true <= 1.1 for _, true, estimate in estimates):
        raise RuntimeError("condition-estimator calibration audit failed")
    naive = next(k for k, residual, _, _ in stop if residual <= 1e-8)
    forward_at_naive = stop[naive][2]
    if forward_at_naive <= 1e-3:
        raise RuntimeError("residual-only early-stop counterexample disappeared")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"saved={OUT}")
    for n, true, estimate in estimates:
        print(f"condition:n={n},true={true:.6e},estimate={estimate:.6e},ratio={estimate/true:.6e}")
    print(f"stopping:residual_tol=1e-8,naive_k={naive},forward_at_stop={forward_at_naive:.6e}")
    print(f"propagation:g085={prop[0.85][-1]:.6e},g115={prop[1.15][-1]:.6e},ratio={prop[1.15][-1]/prop[0.85][-1]:.6e}")


if __name__ == "__main__":
    main()
