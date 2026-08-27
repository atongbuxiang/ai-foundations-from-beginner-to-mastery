#!/usr/bin/env python3
"""Deterministic randomized-SVD experiment: oversampling, power passes, and certificates."""

from __future__ import annotations

import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "randomized-low-rank" / "plot-randomized-svd-probability-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(max(dot(x, x), 0.0))


def orthonormalize(cols, tol=1e-13):
    q = []
    for col in cols:
        v = col[:]
        for _ in range(2):
            for qi in q:
                h = dot(qi, v)
                v = [vi - h * qij for vi, qij in zip(v, qi)]
        nv = norm(v)
        if nv > tol:
            q.append([vi / nv for vi in v])
    return q


def sym_eigh(a0):
    """Small symmetric Jacobi eigensolver returning descending eigenpairs."""
    a = [row[:] for row in a0]
    n = len(a)
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(80 * n * n):
        p, q, largest = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest < 1e-13:
            break
        tau = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau)) if tau else 1.0
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = a[q][p] = 0.0
        for r in range(n):
            if r in (p, q):
                continue
            arp, arq = a[r][p], a[r][q]
            a[r][p] = a[p][r] = c * arp - s * arq
            a[r][q] = a[q][r] = s * arp + c * arq
        for r in range(n):
            vrp, vrq = v[r][p], v[r][q]
            v[r][p] = c * vrp - s * vrq
            v[r][q] = s * vrp + c * vrq
    pairs = sorted(((a[i][i], [v[r][i] for r in range(n)]) for i in range(n)), key=lambda z: z[0], reverse=True)
    return pairs


def apply_residual(sigma, ucols, x):
    ax = [s * xi for s, xi in zip(sigma, x)]
    coeff = [dot(u, ax) for u in ucols]
    return [axi - sum(coeff[j] * ucols[j][i] for j in range(len(ucols))) for i, axi in enumerate(ax)]


def apply_residual_t(sigma, ucols, y):
    coeff = [dot(u, y) for u in ucols]
    py = [yi - sum(coeff[j] * ucols[j][i] for j in range(len(ucols))) for i, yi in enumerate(y)]
    return [s * yi for s, yi in zip(sigma, py)]


def spectral_residual(sigma, ucols):
    n = len(sigma)
    best = 0.0
    for start in range(2):
        x = [math.sin((start + 1.3) * (i + 1)) + 0.2 * math.cos((start + 2.1) * (i + 1)) for i in range(n)]
        nx = norm(x)
        x = [xi / nx for xi in x]
        for _ in range(80):
            y = apply_residual(sigma, ucols, x)
            z = apply_residual_t(sigma, ucols, y)
            nz = norm(z)
            if nz == 0.0:
                break
            x = [zi / nz for zi in z]
        best = max(best, norm(apply_residual(sigma, ucols, x)))
    return best


def randomized_rank_k(sigma, k, p, qpower, seed):
    rng = random.Random(seed)
    n = len(sigma)
    ell = min(n, k + p)
    omega = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(ell)]
    y = [[sigma[i] * col[i] for i in range(n)] for col in omega]
    for _ in range(qpower):
        qcols = orthonormalize(y)
        z = [[sigma[i] * col[i] for i in range(n)] for col in qcols]
        y = [[sigma[i] * col[i] for i in range(n)] for col in z]
    qcols = orthonormalize(y)
    ell = len(qcols)
    csmall = [[sum((sigma[t] ** 2) * qcols[i][t] * qcols[j][t] for t in range(n)) for j in range(ell)] for i in range(ell)]
    eig = sym_eigh(csmall)
    ucols = []
    for _, w in eig[:k]:
        u = [sum(qcols[j][i] * w[j] for j in range(ell)) for i in range(n)]
        nu = norm(u)
        ucols.append([ui / nu for ui in u])
    spec = spectral_residual(sigma, ucols)
    captured = sum(max(val, 0.0) for val, _ in eig[:k])
    frob = math.sqrt(max(sum(s * s for s in sigma) - captured, 0.0))
    return spec, frob, ucols


def quantile(values, frac):
    s = sorted(values)
    pos = frac * (len(s) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return s[lo]
    return s[lo] * (hi - pos) + s[hi] * (pos - lo)


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
        out += [f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>',
                f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>']
    for val, label in yticks:
        frac = logmap(val, ylo, yhi, 0, h) if ylog else (val - ylo) / (yhi - ylo) * h
        y = y0 + h - frac
        out += [f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>',
                f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>']
    out += [f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>',
            f'<text x="{x0-55}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-55} {y0+h/2})">{esc(ylabel)}</text>']
    return out


def poly(points, color, dash=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x, y, color, shape="circle", r=3.2):
    if shape == "square":
        return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    n = 60
    k = 8
    slow = [10.0 ** (-2.0 * i / (n - 1)) for i in range(n)]
    fast = [10.0 ** (-6.0 * i / (n - 1)) for i in range(n)]

    # Panel A: oversampling distribution for the slow spectrum.
    pvals = [0, 2, 5, 10]
    over = []
    for p in pvals:
        ratios = []
        for s in range(30):
            spec, _, _ = randomized_rank_k(slow, k, p, 0, 20260815 + 97 * s + p)
            ratios.append(spec / slow[k])
        over.append((p, quantile(ratios, .1), quantile(ratios, .5), quantile(ratios, .9), max(ratios)))

    # Panel B: power iterations and data passes, comparing slow and fast spectra.
    power = []
    for qpower in range(4):
        row = [qpower]
        for sigma in (slow, fast):
            ratios = []
            for s in range(16):
                spec, _, _ = randomized_rank_k(sigma, k, 5, qpower, 20261815 + 131 * s + 17 * qpower)
                ratios.append(spec / sigma[k])
            row.append(quantile(ratios, .5))
        power.append(tuple(row))

    # Panel C: independent Gaussian probes give a probabilistic upper certificate.
    cert = []
    alpha = 10.0
    probes = 5
    factor = alpha * math.sqrt(2.0 / math.pi)
    for s in range(1, 17):
        spec, _, ucols = randomized_rank_k(slow, k, 5, 1, 20262815 + 211 * s)
        rng = random.Random(20263815 + s)
        responses = []
        for _ in range(probes):
            omega = [rng.gauss(0.0, 1.0) for _ in range(n)]
            responses.append(norm(apply_residual(slow, ucols, omega)))
        cert.append((s, spec, factor * max(responses)))

    assert over[0][2] > over[-1][2] and over[0][4] > over[-1][4]
    assert all(power[i][1] > power[i+1][1] for i in range(len(power)-1))
    assert all(bound >= actual for _, actual, bound in cert)

    W, H = 1440, 610
    c = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Randomized SVD probability, power iteration, and certification</title>',
           '<desc id="desc">Three panels show oversampling quantiles, power iteration versus data passes for two spectra, and independent Gaussian a posteriori residual certificates.</desc>',
           '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;font-size:15px;fill:#1f2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#fffefb;stroke:#d7dee8}.grid{stroke:#e2e8f0}.note{font-size:15px;fill:#64748b}.legend{font-size:15px}</style>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">随机低秩近似：用概率换取少量数据访问，但必须记录尾部与证书</text>']
    for x, title in [(75, "A  oversampling 降低坏 seed 的尾部"), (555, "B  power iteration：精度换数据 passes"), (1035, "C  独立 Gaussian 探针的后验上界")]:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    x0, y0, w, h = 75, 88, 330, 330
    svg += axes(x0, y0, w, h, [(0, "0"), (2, "2"), (5, "5"), (10, "10")],
                [(1, "1"), (1.2, "1.2"), (1.4, "1.4"), (1.6, "1.6"), (2, "2")],
                "oversampling p（ℓ=k+p）", "谱误差 / 最优 σₖ₊₁", True)
    medpts = []
    for p, q10, q50, q90, worst in over:
        px = x0 + p / 10 * w
        y10 = y0 + h - logmap(q10, 1, 2, 0, h)
        y50 = y0 + h - logmap(q50, 1, 2, 0, h)
        y90 = y0 + h - logmap(q90, 1, 2, 0, h)
        yw = y0 + h - logmap(worst, 1, 2, 0, h)
        svg.append(f'<line x1="{px:.2f}" y1="{y10:.2f}" x2="{px:.2f}" y2="{y90:.2f}" stroke="{c["blue"]}" stroke-width="5" opacity=".45"/>')
        svg.append(f'<line x1="{px:.2f}" y1="{y90:.2f}" x2="{px:.2f}" y2="{yw:.2f}" stroke="{c["red"]}" stroke-dasharray="3 3"/>')
        svg.append(mark(px, y50, c["blue"], "circle", 4))
        svg.append(mark(px, yw, c["red"], "diamond", 3))
        medpts.append((px, y50))
    svg.append(poly(medpts, c["blue"]))
    svg.append('<text x="90" y="112" class="note">粗线为 10%–90%；红菱形为 30 个 seed 中最坏值</text>')

    x1 = 555
    svg += axes(x1, y0, w, h, [(0, "q=0"), (1, "q=1"), (2, "q=2"), (3, "q=3")],
                [(1, "1"), (1.2, "1.2"), (1.4, "1.4"), (1.6, "1.6"), (2, "2")],
                "power steps q（range passes=2q+1）", "中位谱误差 / σₖ₊₁", True)
    for idx, color, shape in [(1, c["orange"], "square"), (2, c["green"], "diamond")]:
        pts = [(x1 + row[0] / 3 * w, y0 + h - logmap(row[idx], 1, 2, 0, h)) for row in power]
        svg.append(poly(pts, color))
        for px, py in pts:
            svg.append(mark(px, py, color, shape, 4))
    svg.append('<text x="570" y="112" class="note">另做 B=QᵀA 还需一次 pass；每次幂步必须重正交</text>')

    x2 = 1035
    svg += axes(x2, y0, w, h, [(1, "1"), (4, "4"), (8, "8"), (12, "12"), (16, "16")],
                [(0.01, ".01"), (0.1, ".1"), (1, "1"), (10, "10"), (100, "100")],
                "近似 seed", "残差谱范数 / 概率上界", True)
    truepts = [(x2 + (s - 1) / 15 * w, y0 + h - logmap(v, .01, 100, 0, h)) for s, v, _ in cert]
    boundpts = [(x2 + (s - 1) / 15 * w, y0 + h - logmap(v, .01, 100, 0, h)) for s, _, v in cert]
    svg.append(poly(truepts, c["blue"]))
    svg.append(poly(boundpts, c["purple"], "6 4"))
    for px, py in truepts:
        svg.append(mark(px, py, c["blue"], "circle"))
    for px, py in boundpts:
        svg.append(mark(px, py, c["purple"], "diamond"))
    svg.append('<text x="1050" y="112" class="note">α=10、r=5：失败概率上界 α⁻ʳ=10⁻⁵；证书保守但可审计</text>')

    legends = [(90, c["blue"], "circle", "median / 10–90%"), (265, c["red"], "diamond", "worst seed"),
               (575, c["orange"], "square", "slow spectrum"), (720, c["green"], "diamond", "fast spectrum"),
               (1060, c["blue"], "circle", "true ‖R‖₂"), (1190, c["purple"], "diamond", "prob. certificate")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape))
        svg.append(f'<text x="{x+11}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 看分布而非单 seed；B 把精度改善换算为数据访问；C 用独立探针把随机结果升级为可检查输出。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_randomized_svd_probability.py · Python 标准库 · n=60，目标秩 k=8</text>')
    svg.append('</svg>')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"saved={OUT}")
    for row in over:
        print(f"oversampling:p={row[0]},q10={row[1]:.6e},median={row[2]:.6e},q90={row[3]:.6e},worst={row[4]:.6e}")
    for row in power:
        print(f"power:q={row[0]},slow_median={row[1]:.6e},fast_median={row[2]:.6e},range_passes={2*row[0]+1}")
    ratios = [bound / actual for _, actual, bound in cert]
    print(f"certificate:min_ratio={min(ratios):.6e},median_ratio={quantile(ratios,.5):.6e},max_ratio={max(ratios):.6e},failure_bound={alpha**(-probes):.1e}")


if __name__ == "__main__":
    main()
