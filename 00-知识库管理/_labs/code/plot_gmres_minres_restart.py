#!/usr/bin/env python3
"""Deterministic GMRES/MINRES experiment: residual minimization, restart, and method contracts."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "residual-minimization" / "plot-gmres-minres-restart-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(max(dot(x, x), 0.0))


def matvec(a, x):
    return [dot(row, x) for row in a]


def axpy(a, x, y):
    return [yi + a * xi for xi, yi in zip(x, y)]


def grcar(n, upper=3):
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = 1.0
        if i:
            a[i][i - 1] = -1.0
        for j in range(i + 1, min(n, i + upper + 1)):
            a[i][j] = 1.0
    return a


def backsolve(r, g, k):
    y = [0.0] * k
    for i in range(k - 1, -1, -1):
        rhs = g[i] - sum(r[i][j] * y[j] for j in range(i + 1, k))
        y[i] = rhs / r[i][i]
    return y


def gmres(a, b, restart, maxit, tol=1e-13):
    """Restarted GMRES with MGS Arnoldi and incremental Givens QR; records true residual."""
    n = len(b)
    x = [0.0] * n
    base = norm(b)
    hist = [(0, 1.0)]
    matvecs = 0
    orth_dots = 0
    cycle_ends = []
    while matvecs < maxit and hist[-1][1] > tol:
        r0 = [bi - ai for bi, ai in zip(b, matvec(a, x))]
        beta = norm(r0)
        if beta == 0.0:
            break
        m = min(restart, maxit - matvecs)
        v = [[ri / beta for ri in r0]]
        h = [[0.0] * m for _ in range(m + 1)]
        cs = [0.0] * m
        sn = [0.0] * m
        g = [0.0] * (m + 1)
        g[0] = beta
        used = 0
        for j in range(m):
            w = matvec(a, v[j])
            matvecs += 1
            for i in range(j + 1):
                hij = dot(v[i], w)
                orth_dots += 1
                h[i][j] = hij
                w = axpy(-hij, v[i], w)
            h[j + 1][j] = norm(w)
            if h[j + 1][j] > 1e-15:
                v.append([wi / h[j + 1][j] for wi in w])
            else:
                v.append([0.0] * n)
            for i in range(j):
                t = cs[i] * h[i][j] + sn[i] * h[i + 1][j]
                h[i + 1][j] = -sn[i] * h[i][j] + cs[i] * h[i + 1][j]
                h[i][j] = t
            den = math.hypot(h[j][j], h[j + 1][j])
            cs[j] = h[j][j] / den if den else 1.0
            sn[j] = h[j + 1][j] / den if den else 0.0
            h[j][j] = den
            h[j + 1][j] = 0.0
            g[j + 1] = -sn[j] * g[j]
            g[j] = cs[j] * g[j]
            used = j + 1
            y = backsolve(h, g, used)
            xt = x[:]
            for q in range(used):
                xt = axpy(y[q], v[q], xt)
            tr = norm([bi - ai for bi, ai in zip(b, matvec(a, xt))]) / base
            hist.append((matvecs, max(tr, 1e-16)))
            if tr <= tol or abs(g[j + 1]) <= tol * base:
                x = xt
                break
        else:
            y = backsolve(h, g, used)
            for q in range(used):
                x = axpy(y[q], v[q], x)
        if hist[-1][1] <= tol:
            cycle_ends.append(matvecs)
            break
        if used and (not cycle_ends or cycle_ends[-1] != matvecs):
            if 'y' not in locals():
                y = backsolve(h, g, used)
            # If the cycle ended by exhausting m, x was updated in the for-else.
            cycle_ends.append(matvecs)
    return hist, matvecs, orth_dots, cycle_ends


def minres_small_demo():
    # For symmetric A=diag(1,-1), Arnoldi residual minimization is MINRES.
    a = [[1.0, 0.0], [0.0, -1.0]]
    b = [1.0, 1.0]
    hist, _, _, _ = gmres(a, b, restart=2, maxit=2, tol=1e-15)
    return hist


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def logmap(v, lo, hi, a, b):
    v = max(lo, min(hi, v))
    return a + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (b - a)


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel, xlog=False, ylog=False):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo, xhi = xticks[0][0], xticks[-1][0]
    ylo, yhi = yticks[0][0], yticks[-1][0]
    for val, label in xticks:
        frac = logmap(val, xlo, xhi, 0, w) if xlog else (val - xlo) / (xhi - xlo) * w
        x = x0 + frac
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
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x, y, color, shape="circle", r=3.2):
    if shape == "square":
        return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    n = 40
    a = grcar(n)
    xtrue = [math.sin(0.37 * (i + 1)) + 0.2 * math.cos(0.91 * (i + 1)) for i in range(n)]
    b = matvec(a, xtrue)
    full, _, full_dots, _ = gmres(a, b, restart=40, maxit=40)
    r8, _, r8_dots, ends8 = gmres(a, b, restart=8, maxit=120)
    r16, _, r16_dots, ends16 = gmres(a, b, restart=16, maxit=120)
    minres = minres_small_demo()

    restart_sizes = [4, 6, 8, 12, 16, 24, 40]
    trade = []
    for m in restart_sizes:
        hist, _, dots, _ = gmres(a, b, restart=m, maxit=120)
        trade.append((m, hist[-1][1], dots))

    W, H = 1440, 610
    c = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">GMRES, MINRES, restart and residual minimization</title>',
           '<desc id="desc">Three panels show full and restarted GMRES on a nonnormal matrix, MINRES succeeding where CG breaks down on a symmetric indefinite system, and restart memory versus residual tradeoffs.</desc>',
           '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">残差最小化：结构决定方法，重启决定记忆与停滞</text>']
    for x, title in [(75, "A  非正规 Grcar：完整与重启 GMRES"), (555, "B  对称不定：CG breakdown，MINRES 仍合法"), (1035, "C  固定 120 matvec 的重启权衡")]:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    x0, y0, w, h = 75, 88, 330, 330
    svg += axes(x0, y0, w, h, [(0, "0"), (30, "30"), (60, "60"), (90, "90"), (120, "120")],
                [(1e-14, "10⁻¹⁴"), (1e-10, "10⁻¹⁰"), (1e-6, "10⁻⁶"), (1e-2, "10⁻²"), (1, "1")],
                "matvec 次数", "真相对残差", False, True)
    series = [(full, c["green"], "diamond", ""), (r16, c["blue"], "circle", ""), (r8, c["orange"], "square", "6 4")]
    for hist, color, shape, dash in series:
        pts = [(x0 + k / 120 * w, y0 + h - logmap(v, 1e-14, 1, 0, h)) for k, v in hist]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::max(1, len(pts)//7)]:
            svg.append(mark(px, py, color, shape))
    for k in ends8[:-1]:
        x = x0 + k / 120 * w
        svg.append(f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" stroke="#c36a14" stroke-dasharray="2 5" opacity=".35"/>')
    svg.append('<text x="90" y="112" class="note">竖虚线为 GMRES(8) 重启；真残差在完整周期内单调</text>')

    x1 = 555
    svg += axes(x1, y0, w, h, [(0, "0"), (0.5, ".5"), (1, "1"), (1.5, "1.5"), (2, "2")],
                [(0, "0"), (0.25, ".25"), (0.5, ".5"), (0.75, ".75"), (1, "1")],
                "Krylov 步数", "相对残差", False, False)
    min_pts = [(x1 + k / 2 * w, y0 + h - v * h) for k, v in minres]
    svg.append(poly(min_pts, c["green"]))
    for px, py in min_pts:
        svg.append(mark(px, py, c["green"], "diamond", 4))
    svg.append(f'<line x1="{x1}" y1="{y0}" x2="{x1}" y2="{y0+h}" stroke="{c["red"]}" stroke-width="3"/>')
    svg.append(mark(x1, y0, c["red"], "square", 4))
    svg.append('<text x="570" y="112" class="note">A=diag(1,−1), b=(1,1)：p₀ᵀAp₀=0，CG 首步无定义</text>')
    svg.append('<text x="720" y="250" text-anchor="middle" class="note">MINRES 第 1 步只能保持残差；第 2 步精确求解</text>')

    x2 = 1035
    svg += axes(x2, y0, w, h, [(4, "4"), (8, "8"), (16, "16"), (24, "24"), (40, "40")],
                [(1e-14, "10⁻¹⁴"), (1e-10, "10⁻¹⁰"), (1e-6, "10⁻⁶"), (1e-2, "10⁻²"), (1, "1")],
                "重启维数 m（≈ 基向量内存）", "120 次后的真残差", False, True)
    trade_pts = []
    maxdots = max(t[2] for t in trade)
    for m, res, dots in trade:
        px = x2 + (m - 4) / 36 * w
        py = y0 + h - logmap(res, 1e-14, 1, 0, h)
        rad = 4 + 7 * math.sqrt(dots / maxdots)
        trade_pts.append((px, py))
        svg.append(mark(px, py, c["purple"], "circle", rad))
        if m in (4, 16, 24, 40):
            svg.append(f'<text x="{px:.2f}" y="{py-12:.2f}" text-anchor="middle" class="note">m={m}</text>')
    svg.append(poly(trade_pts, c["purple"], "4 4"))
    svg.append('<text x="1050" y="112" class="note">圆越大表示累计正交内积越多；内存增大不保证同预算最优</text>')

    legends = [(90, c["green"], "diamond", "full GMRES"), (200, c["blue"], "circle", "GMRES(16)"), (320, c["orange"], "square", "GMRES(8)"),
               (575, c["green"], "diamond", "MINRES"), (690, c["red"], "square", "CG breakdown"),
               (1060, c["purple"], "circle", "restart tradeoff")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape))
        svg.append(f'<text x="{x+11}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 分离完整最优与重启遗忘；B 强调对称不定不能用 CG；C 同时计入基内存与正交化工作。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_gmres_minres_restart.py · Python 标准库 · n=40 Grcar 与确定性右端</text>')
    svg.append('</svg>')
    if full[-1][1] >= 1e-12 or min(r8[-1][1], r16[-1][1]) <= 1e-9:
        raise RuntimeError("full/restarted GMRES separation audit failed")
    if minres[1][1] < 0.9 or minres[-1][1] >= 1e-12:
        raise RuntimeError("MINRES indefinite-system audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"saved={OUT}")
    for name, hist, dots in [("full", full, full_dots), ("r16", r16, r16_dots), ("r8", r8, r8_dots)]:
        print(f"gmres:{name},steps={hist[-1][0]},final={hist[-1][1]:.6e},orth_dots={dots}")
    print("minres:" + ",".join(f"k{k}={v:.6e}" for k, v in minres))
    for m, res, dots in trade:
        print(f"trade:m={m},res={res:.6e},orth_dots={dots}")


if __name__ == "__main__":
    main()
