#!/usr/bin/env python3
"""Deterministic mixed-precision iterative-refinement and GMRES-IR experiment."""

from __future__ import annotations

import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "iterative-refinement" / "plot-mixed-precision-refinement-v2.svg"


def q16(x):
    try:
        return struct.unpack(">e", struct.pack(">e", float(x)))[0]
    except OverflowError:
        return math.copysign(math.inf, x)


def q32(x):
    return struct.unpack(">f", struct.pack(">f", float(x)))[0]


def dot(x, y):
    return math.fsum(a * b for a, b in zip(x, y))


def norm2(x):
    return math.sqrt(max(dot(x, x), 0.0))


def matvec(a, x):
    return [dot(row, x) for row in a]


def dct_basis(n):
    q = [[0.0] * n for _ in range(n)]
    for i in range(n):
        q[i][0] = 1.0 / math.sqrt(n)
        for j in range(1, n):
            q[i][j] = math.sqrt(2.0 / n) * math.cos(math.pi * (i + 0.5) * j / n)
    return q


def spd_matrix(n, condition):
    q = dct_basis(n)
    eig = [condition ** (-i / (n - 1)) for i in range(n)]
    return [[math.fsum(q[i][k] * eig[k] * q[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def low_lu_factor(a0):
    a = [[q16(v) for v in row] for row in a0]
    n = len(a)
    piv = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if not math.isfinite(a[p][k]) or abs(a[p][k]) < 2.0**-24:
            raise ValueError("low precision singular pivot")
        if p != k:
            a[k], a[p] = a[p], a[k]
            piv[k], piv[p] = piv[p], piv[k]
        for i in range(k + 1, n):
            a[i][k] = q16(a[i][k] / a[k][k])
            for j in range(k + 1, n):
                a[i][j] = q16(a[i][j] - q16(a[i][k] * a[k][j]))
    return a, piv


def low_lu_solve(fact, b):
    lu, piv = fact
    n = len(lu)
    x = [q16(b[piv[i]]) for i in range(n)]
    for i in range(n):
        for j in range(i):
            x[i] = q16(x[i] - q16(lu[i][j] * x[j]))
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            x[i] = q16(x[i] - q16(lu[i][j] * x[j]))
        x[i] = q16(x[i] / lu[i][i])
        if not math.isfinite(x[i]):
            raise ValueError("low precision solve overflow")
    return x


def residual(a, b, x, precision):
    out = []
    for i, row in enumerate(a):
        if precision == "f64":
            ax = math.fsum(row[j] * x[j] for j in range(len(x)))
            out.append(b[i] - ax)
        elif precision == "f32":
            ax = 0.0
            for j in range(len(x)):
                ax = q32(ax + q32(q32(row[j]) * q32(x[j])))
            out.append(q32(q32(b[i]) - ax))
        else:
            ax = 0.0
            for j in range(len(x)):
                ax = q16(ax + q16(q16(row[j]) * q16(x[j])))
            out.append(q16(q16(b[i]) - ax))
    return out


def forward_error(x, xtrue):
    return norm2([a - b for a, b in zip(x, xtrue)]) / norm2(xtrue)


def least_squares(h, beta):
    rows = len(h)
    cols = len(h[0]) if rows else 0
    qcols = []
    r = [[0.0] * cols for _ in range(cols)]
    for j in range(cols):
        v = [h[i][j] for i in range(rows)]
        for i, qi in enumerate(qcols):
            r[i][j] = dot(qi, v)
            v = [vk - r[i][j] * qik for vk, qik in zip(v, qi)]
        r[j][j] = norm2(v)
        if r[j][j] < 1e-30:
            return [0.0] * cols
        qcols.append([vk / r[j][j] for vk in v])
    g = [beta * qi[0] for qi in qcols]
    y = [0.0] * cols
    for i in range(cols - 1, -1, -1):
        y[i] = (g[i] - sum(r[i][j] * y[j] for j in range(i + 1, cols))) / r[i][i]
    return y


def gmres_correction(a, fact, rhs, m=5):
    beta = norm2(rhs)
    if beta == 0.0:
        return [0.0] * len(rhs)
    q = [[v / beta for v in rhs]]
    zcols = []
    h = [[0.0] * m for _ in range(m + 1)]
    steps = 0
    for j in range(m):
        z = low_lu_solve(fact, q[j])
        zcols.append(z)
        w = matvec(a, z)
        for i in range(j + 1):
            h[i][j] = dot(q[i], w)
            w = [wk - h[i][j] * qik for wk, qik in zip(w, q[i])]
        h[j + 1][j] = norm2(w)
        steps = j + 1
        if h[j + 1][j] < 1e-14:
            break
        q.append([wk / h[j + 1][j] for wk in w])
    hs = [row[:steps] for row in h[: steps + 1]]
    y = least_squares(hs, beta)
    return [math.fsum(zcols[j][i] * y[j] for j in range(steps)) for i in range(len(rhs))]


def classical_ir(a, b, xtrue, residual_precision="f64", steps=10):
    try:
        fact = low_lu_factor(a)
        x = [q32(v) for v in low_lu_solve(fact, b)]
    except ValueError:
        return [1.0] * (steps + 1)
    history = [forward_error(x, xtrue)]
    for _ in range(steps):
        try:
            r = residual(a, b, x, residual_precision)
            d = low_lu_solve(fact, r)
            x = [q32(xi + di) for xi, di in zip(x, d)]
            err = forward_error(x, xtrue)
            history.append(err if math.isfinite(err) else 1.0)
        except ValueError:
            history.append(1.0)
    return history


def gmres_ir(a, b, xtrue, steps=5, inner=5):
    try:
        fact = low_lu_factor(a)
        x = [q32(v) for v in low_lu_solve(fact, b)]
    except ValueError:
        return [1.0] * (steps + 1)
    history = [forward_error(x, xtrue)]
    for _ in range(steps):
        try:
            r = residual(a, b, x, "f64")
            d = gmres_correction(a, fact, r, inner)
            x = [q32(xi + di) for xi, di in zip(x, d)]
            err = forward_error(x, xtrue)
            history.append(err if math.isfinite(err) else 1.0)
        except ValueError:
            history.append(1.0)
    return history


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def log_y(v, lo, hi, y0, h):
    v = max(lo, min(hi, v))
    return y0 + h - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * h


def axes_linear_x(x0, y0, w, h, xticks, yticks, xlabel, ylabel):
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


def axes_log_x(x0, y0, w, h, xticks, yticks, xlabel, ylabel):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo, xhi = xticks[0][0], xticks[-1][0]
    for value, label in xticks:
        x = x0 + (math.log10(value) - math.log10(xlo)) / (math.log10(xhi) - math.log10(xlo)) * w
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


def problem(condition, n=8):
    a = spd_matrix(n, condition)
    xtrue = [math.sin(0.61 * (i + 1)) - 0.37 * math.cos(0.29 * (i + 1)) for i in range(n)]
    b = matvec(a, xtrue)
    return a, b, xtrue


def main():
    histories = {}
    for condition in (1e2, 1e3, 1e4):
        a, b, xt = problem(condition)
        histories[condition] = classical_ir(a, b, xt, "f64", 10)

    a_mid, b_mid, xt_mid = problem(1e2)
    residual_histories = {
        p: classical_ir(a_mid, b_mid, xt_mid, p, 10)
        for p in ("f16", "f32", "f64")
    }

    conditions = [10.0, 30.0, 100.0, 300.0, 1e3, 3e3, 1e4, 3e4, 1e5]
    sweep = []
    for condition in conditions:
        a, b, xt = problem(condition)
        classical = classical_ir(a, b, xt, "f64", 10)[-1]
        gmres = gmres_ir(a, b, xt, 5, 5)[-1]
        sweep.append((condition, classical, gmres))

    W, H = 1440, 610
    y0, h, w = 88, 330, 330
    xs = [75, 555, 1035]
    colors = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    yticks = [(1e-8, "1e−8"), (1e-6, "1e−6"), (1e-4, "1e−4"), (1e-2, "1e−2"), (1, "1")]
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">Mixed precision iterative refinement and GMRES-IR</title>',
        '<desc id="desc">Three panels show the condition-number convergence boundary, the impact of residual precision, and the wider success region of GMRES-based iterative refinement.</desc>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        '<text x="720" y="34" text-anchor="middle" class="title">迭代改进与混合精度：低精度负责大工作，高精度负责纠错与验收</text>',
        '<text x="75" y="67" class="panel">A  binary16 LU 的条件数收敛边界</text>',
        '<text x="555" y="67" class="panel">B  残差精度决定可达到的误差地板</text>',
        '<text x="1035" y="67" class="panel">C  GMRES-IR 扩展低精度因子的可用区间</text>',
    ]

    svg += axes_linear_x(xs[0], y0, w, h, [(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8"), (10, "10")], yticks, "refinement step", "relative forward error")
    for condition, color, shape in [(1e2, colors["green"], "circle"), (1e3, colors["blue"], "square"), (1e4, colors["red"], "diamond")]:
        hist = histories[condition]
        pts = [(xs[0] + k / 10 * w, log_y(max(v, 1e-8), 1e-8, 1, y0, h)) for k, v in enumerate(hist)]
        svg.append(poly(pts, color))
        for k in (0, 2, 4, 6, 8, 10):
            svg.append(mark(pts[k][0], pts[k][1], color, shape))
    svg += [
        f'<text x="{xs[0]+18}" y="{y0+25}" class="note">n=8 DCT 相似 SPD；LU 每个算术步骤舍入到 binary16</text>',
        f'<text x="{xs[0]+15}" y="{y0+h+78}" class="legend" fill="{colors["green"]}">● κ=10²</text>',
        f'<text x="{xs[0]+120}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">■ κ=10³</text>',
        f'<text x="{xs[0]+225}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">◆ κ=10⁴</text>',
    ]

    svg += axes_linear_x(xs[1], y0, w, h, [(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8"), (10, "10")], yticks, "refinement step", "relative forward error")
    for precision, color, shape in [("f16", colors["orange"], "circle"), ("f32", colors["blue"], "square"), ("f64", colors["purple"], "diamond")]:
        hist = residual_histories[precision]
        pts = [(xs[1] + k / 10 * w, log_y(max(v, 1e-8), 1e-8, 1, y0, h)) for k, v in enumerate(hist)]
        svg.append(poly(pts, color, "6 4" if precision == "f64" else ""))
        for k in (0, 2, 4, 6, 8, 10):
            svg.append(mark(pts[k][0], pts[k][1], color, shape))
    svg += [
        f'<text x="{xs[1]+18}" y="{y0+25}" class="note">固定 κ=10²、同一 binary16 LU，只改变 r=b−Ax 的精度</text>',
        f'<text x="{xs[1]+35}" y="{y0+h+78}" class="legend" fill="{colors["orange"]}">● FP16 r</text>',
        f'<text x="{xs[1]+145}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">■ FP32 r</text>',
        f'<text x="{xs[1]+250}" y="{y0+h+78}" class="legend" fill="{colors["purple"]}">◆ FP64 r</text>',
    ]

    xticks_c = [(10, "10"), (100, "10²"), (1000, "10³"), (10000, "10⁴"), (100000, "10⁵")]
    svg += axes_log_x(xs[2], y0, w, h, xticks_c, yticks, "κ₂(A)", "final relative forward error")
    for idx, color, shape in [(1, colors["red"], "circle"), (2, colors["green"], "diamond")]:
        pts = []
        for condition, classical, gmres in sweep:
            value = (classical, gmres)[idx - 1]
            x = xs[2] + (math.log10(condition) - 1) / 4 * w
            pts.append((x, log_y(max(value, 1e-8), 1e-8, 1, y0, h)))
        svg.append(poly(pts, color, "6 4" if idx == 2 else ""))
        for p in pts:
            svg.append(mark(p[0], p[1], color, shape))
    svg += [
        f'<text x="{xs[2]+18}" y="{y0+25}" class="note">classical：1 次低精度 solve；GMRES-IR：5 步</text>',
        f'<text x="{xs[2]+55}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">● classical IR</text>',
        f'<text x="{xs[2]+205}" y="{y0+h+78}" class="legend" fill="{colors["green"]}">◆ GMRES-IR</text>',
    ]

    svg += [
        '<text x="720" y="568" text-anchor="middle" class="note">A：κ·u_factor 接近 1 时经典校正失去收缩；B：高精度残差避免纠错信号被再次舍入；C：GMRES 近似解预条件校正方程。</text>',
        '<text x="720" y="590" text-anchor="middle" class="note">生成：plot_mixed_precision_refinement.py · Python 标准库 · binary16 LU / binary32 update / binary64 reference</text>',
        '</svg>',
    ]
    if histories[1e2][-1] >= histories[1e2][0] * 1e-3:
        raise RuntimeError("classical refinement no longer repairs the kappa=1e2 case")
    if residual_histories["f64"][-1] >= residual_histories["f16"][-1] * 1e-3:
        raise RuntimeError("residual-precision separation audit failed")
    if sweep[-2][2] >= 1e-6 or sweep[-1][1:] != (1.0, 1.0):
        raise RuntimeError("GMRES-IR success/failure boundary changed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"saved={OUT}")
    for condition, hist in histories.items():
        print(f"classical:kappa={condition:.1e},initial={hist[0]:.6e},final={hist[-1]:.6e}")
    for precision, hist in residual_histories.items():
        print(f"residual:{precision},initial={hist[0]:.6e},final={hist[-1]:.6e}")
    for condition, classical, gmres in sweep:
        print(f"sweep:kappa={condition:.1e},classical={classical:.6e},gmres_ir={gmres:.6e}")


if __name__ == "__main__":
    main()
