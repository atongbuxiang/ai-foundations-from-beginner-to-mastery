#!/usr/bin/env python3
"""Deterministic CG experiment: geometry, spectral clustering and residual drift."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "conjugate-gradient" / "plot-conjugate-gradient-geometry-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(dot(x, x))


def matvec(a, x):
    return [dot(row, x) for row in a]


def axpy(a, x, y):
    return [a * xi + yi for xi, yi in zip(x, y)]


def cg(a, b, xtrue, maxit, x0=None):
    n = len(b)
    x = [0.0] * n if x0 is None else x0[:]
    r = [bi - ai for bi, ai in zip(b, matvec(a, x))]
    p = r[:]
    rr = dot(r, r)
    e0 = [xi - ti for xi, ti in zip(x, xtrue)]
    base = math.sqrt(dot(e0, matvec(a, e0)))
    hist = [(0, 1.0)]
    path = [x[:]]
    for k in range(1, maxit + 1):
        ap = matvec(a, p)
        alpha = rr / dot(p, ap)
        x = axpy(alpha, p, x)
        r = axpy(-alpha, ap, r)
        rr_new = dot(r, r)
        err = [xi - ti for xi, ti in zip(x, xtrue)]
        hist.append((k, max(math.sqrt(max(dot(err, matvec(a, err)), 0.0)) / base, 1e-16)))
        path.append(x[:])
        if math.sqrt(rr_new) < 1e-14 * max(norm(b), 1.0):
            break
        beta = rr_new / rr
        p = axpy(beta, p, r)
        rr = rr_new
    return hist, path


def steepest(a, b, xtrue, steps, x0):
    x = x0[:]
    path = [x[:]]
    for _ in range(steps):
        r = [bi - ai for bi, ai in zip(b, matvec(a, x))]
        ar = matvec(a, r)
        alpha = dot(r, r) / dot(r, ar)
        x = axpy(alpha, r, x)
        path.append(x[:])
    return path


def orthogonal_basis(n):
    cols = []
    for j in range(n):
        v = [math.sin((i + 1) * (j + 1) * 0.37) + math.cos((i + 1) * (j + 2) * 0.19) for i in range(n)]
        for _ in range(2):
            for q in cols:
                c = dot(q, v)
                v = [vi - c * qi for vi, qi in zip(v, q)]
        nv = norm(v)
        if nv < 1e-10:
            v = [1.0 if i == j else 0.0 for i in range(n)]
            for _ in range(2):
                for q in cols:
                    c = dot(q, v)
                    v = [vi - c * qi for vi, qi in zip(v, q)]
            nv = norm(v)
        cols.append([vi / nv for vi in v])
    return cols


def matrix_from_spectrum(lam, qcols):
    n = len(lam)
    return [[sum(lam[k] * qcols[k][i] * qcols[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def qsig(v, digits):
    if v == 0.0:
        return 0.0
    return float(f"{v:.{digits}g}")


def qvec(x, digits):
    return [qsig(v, digits) for v in x]


def cg_quantized(a, b, maxit=120, digits=8, replacement=None):
    n = len(b)
    x = [0.0] * n
    r = qvec(b, digits)
    p = r[:]
    rr = qsig(dot(r, r), digits)
    base = norm(b)
    hist = [(0, 1.0, 1.0)]
    for k in range(1, maxit + 1):
        ap = qvec(matvec(a, p), digits)
        denom = qsig(dot(p, ap), digits)
        if denom <= 0.0 or rr <= 0.0:
            break
        alpha = qsig(rr / denom, digits)
        x = qvec([xi + alpha * pi for xi, pi in zip(x, p)], digits)
        r = qvec([ri - alpha * api for ri, api in zip(r, ap)], digits)
        if replacement and k % replacement == 0:
            r = qvec([bi - ai for bi, ai in zip(b, matvec(a, x))], digits)
            p = r[:]
            rr = qsig(dot(r, r), digits)
        else:
            rr_new = qsig(dot(r, r), digits)
            beta = qsig(rr_new / rr, digits)
            p = qvec([ri + beta * pi for ri, pi in zip(r, p)], digits)
            rr = rr_new
        rec = norm(r) / base
        true = norm([bi - ai for bi, ai in zip(b, matvec(a, x))]) / base
        hist.append((k, max(rec, 1e-18), max(true, 1e-18)))
    return hist


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def logmap(v, lo, hi, a, b):
    v = max(lo, min(hi, v))
    return a + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (b - a)


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel, ylog=False):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo, xhi = xticks[0][0], xticks[-1][0]
    ylo, yhi = yticks[0][0], yticks[-1][0]
    for val, label in xticks:
        x = x0 + (val - xlo) / (xhi - xlo) * w
        out += [f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>', f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>']
    for val, label in yticks:
        frac = logmap(val, ylo, yhi, 0, h) if ylog else (val - ylo) / (yhi - ylo) * h
        y = y0 + h - frac
        out += [f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>', f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>']
    out += [f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>', f'<text x="{x0-55}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-55} {y0+h/2})">{esc(ylabel)}</text>']
    return out


def poly(points, color, dash="", width=2.5):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="{width}"{ds}/>'


def mark(x, y, color, shape="circle", r=3.2):
    if shape == "square": return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond": return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    # Panel A: two-dimensional energy geometry.
    a2 = [[1.0, 0.0], [0.0, 20.0]]
    xstar2 = [1.0, 1.0]
    b2 = matvec(a2, xstar2)
    x0 = [-1.3, 2.2]
    sd_path = steepest(a2, b2, xstar2, 9, x0)
    _, cg_path = cg(a2, b2, xstar2, 3, x0)

    # Panel B: same condition number, different spectral distributions.
    n = 40
    spread = [1000.0 ** (i / (n - 1)) for i in range(n)]
    clustered = [1.0] * 10 + [2.0] * 10 + [50.0] * 10 + [1000.0] * 10
    xtrue = [math.sin(0.53 * (i + 1)) + 0.3 * math.cos(0.17 * (i + 1)) for i in range(n)]
    aspread = [[spread[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
    acluster = [[clustered[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
    hspread, _ = cg(aspread, matvec(aspread, xtrue), xtrue, 40)
    hcluster, _ = cg(acluster, matvec(acluster, xtrue), xtrue, 40)
    q = (math.sqrt(1000.0) - 1.0) / (math.sqrt(1000.0) + 1.0)
    bound = [(k, max(min(2.0 * q**k, 1.0), 1e-16)) for k in range(41)]

    # Panel C: recursive residual can drift from the true residual in reduced precision.
    nfp = 35
    qcols = orthogonal_basis(nfp)
    lam = [10.0 ** (4.0 * i / (nfp - 1)) for i in range(nfp)]
    afp = matrix_from_spectrum(lam, qcols)
    coeff = [math.sin(0.71 * (i + 1)) + 0.1 * math.cos(1.31 * (i + 1)) for i in range(nfp)]
    bfp = [sum(qcols[j][i] * coeff[j] for j in range(nfp)) for i in range(nfp)]
    drift = cg_quantized(afp, bfp, 400, digits=7, replacement=None)
    replaced = cg_quantized(afp, bfp, 400, digits=7, replacement=30)

    W, H = 1440, 610
    c = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Conjugate gradient geometry, spectral clustering and finite precision</title>',
           '<desc id="desc">Three panels compare steepest descent and CG paths, CG convergence for spread and clustered spectra, and recursive versus true residuals in simulated reduced precision.</desc>',
           '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}.contour{fill:none;stroke:#D7DEE8;stroke-width:1.5}</style>',
           '<defs><clipPath id="cg-panel-a"><rect x="75" y="88" width="330" height="330"/></clipPath></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">共轭梯度：在 A-几何中一次消去一个方向，但谱与舍入决定真实速度</text>']
    for x, title in [(75, "A  最速下降的锯齿与 CG 的共轭方向"), (555, "B  相同 κ，不同谱分布"), (1035, "C  递推残差不总等于真残差")]:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    x0p, y0p, wp, hp = 75, 88, 330, 330
    svg += axes(x0p, y0p, wp, hp, [(-1.5, "−1.5"), (-0.25, "−.25"), (1, "1"), (2.25, "2.25"), (3.5, "3.5")],
                [(-0.5, "−.5"), (0.25, ".25"), (1, "1"), (1.75, "1.75"), (2.5, "2.5")], "x₁", "x₂", False)
    def world(v):
        return (x0p + (v[0] + 1.5) / 5.0 * wp, y0p + hp - (v[1] + 0.5) / 3.0 * hp)
    for level in (0.4, 1.5, 5.0, 15.0, 35.0):
        pts = []
        for j in range(101):
            t = 2 * math.pi * j / 100
            p = [1.0 + math.sqrt(level) * math.cos(t), 1.0 + math.sqrt(level / 20.0) * math.sin(t)]
            pts.append(world(p))
        svg.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" class="contour" clip-path="url(#cg-panel-a)"/>')
    for path, color, shape in [(sd_path, c["orange"], "square"), (cg_path, c["blue"], "diamond")]:
        pts = [world(p) for p in path]
        svg.append(poly(pts, color))
        for px, py in pts: svg.append(mark(px, py, color, shape))
    sx, sy = world(xstar2); svg.append(mark(sx, sy, c["green"], "circle", 5)); svg.append(f'<text x="{sx+8:.2f}" y="{sy-8:.2f}" class="note">x*</text>')

    x1 = 555
    svg += axes(x1, 88, 330, 330, [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40")],
                [(1e-16, "10⁻¹⁶"), (1e-12, "10⁻¹²"), (1e-8, "10⁻⁸"), (1e-4, "10⁻⁴"), (1, "1")], "CG 迭代次数 k", "‖eₖ‖A / ‖e₀‖A", True)
    for hist, color, shape, dash in [(hspread, c["orange"], "square", ""), (hcluster, c["green"], "diamond", ""), (bound, c["purple"], "circle", "6 4")]:
        pts = [(x1 + k / 40 * 330, 88 + 330 - logmap(v, 1e-16, 1, 0, 330)) for k, v in hist]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::5]: svg.append(mark(px, py, color, shape))
    svg.append('<text x="570" y="112" class="note">两者 κ=1000；四点聚簇在精确算术中至多 4 步终止</text>')

    x2 = 1035
    svg += axes(x2, 88, 330, 330, [(0, "0"), (100, "100"), (200, "200"), (300, "300"), (400, "400")],
                [(1e-16, "10⁻¹⁶"), (1e-12, "10⁻¹²"), (1e-8, "10⁻⁸"), (1e-4, "10⁻⁴"), (1, "1")], "迭代次数 k", "相对残差", True)
    series = [([(k, rec) for k, rec, _ in drift], c["blue"], "circle", "", "递推残差"),
              ([(k, true) for k, _, true in drift], c["red"], "square", "", "真残差"),
              ([(k, true) for k, _, true in replaced], c["green"], "diamond", "6 4", "每 30 步重算并重启")]
    for hist, color, shape, dash, _ in series:
        pts = [(x2 + k / 400 * 330, 88 + 330 - logmap(v, 1e-16, 1, 0, 330)) for k, v in hist]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::40]: svg.append(mark(px, py, color, shape))
    svg.append('<text x="1050" y="112" class="note">35 阶 κ=10⁴；显式 7 位有效数字模拟</text>')

    legends = [(95, c["orange"], "square", "最速下降"), (230, c["blue"], "diamond", "CG"), (310, c["green"], "circle", "精确解"),
               (575, c["orange"], "square", "spread"), (680, c["green"], "diamond", "4 clusters"), (800, c["purple"], "circle", "κ-bound"),
               (1055, c["blue"], "circle", "递推"), (1130, c["red"], "square", "真实"), (1205, c["green"], "diamond", "30 步重算+重启")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 展示能量几何；B 说明条件数界忽略聚簇；C 说明停止时应抽查 b−Ax，而不能永远只信递推 rₖ。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_conjugate_gradient_geometry.py · Python 标准库 · 确定性矩阵</text>')
    svg.append('</svg>')
    spread_by_k = dict(hspread)
    clustered_by_k = dict(hcluster)
    peak_gap = max((true / rec, k, rec, true) for k, rec, true in drift if rec > 0)
    if spread_by_k[4] <= 1e-2 or clustered_by_k[4] >= 1e-8:
        raise RuntimeError("spectral-clustering CG separation audit failed")
    if peak_gap[0] <= 1e10 or replaced[-1][2] >= 1e-3:
        raise RuntimeError("recursive/true residual drift audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"saved={OUT}")
    for name, hist in (("spread", hspread), ("clustered", hcluster)):
        vals = dict(hist); print(f"spectrum:{name},k4={vals.get(4, hist[-1][1]):.3e},k10={vals.get(10, hist[-1][1]):.3e},final_k={hist[-1][0]},final={hist[-1][1]:.3e}")
    print(f"drift:max_true_over_recursive={peak_gap[0]:.3e},k={peak_gap[1]},rec={peak_gap[2]:.3e},true={peak_gap[3]:.3e}")
    print(f"replacement:final_k={replaced[-1][0]},rec={replaced[-1][1]:.3e},true={replaced[-1][2]:.3e}")


if __name__ == "__main__":
    main()
