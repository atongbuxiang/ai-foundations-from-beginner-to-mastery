#!/usr/bin/env python3
"""Deterministic preconditioning experiment: spectra, PCG histories and cost-quality tradeoff."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "preconditioning" / "plot-krylov-preconditioning-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(dot(x, x))


def matvec(a, x):
    return [dot(row, x) for row in a]


def cholesky(a):
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not SPD")
                l[i][j] = math.sqrt(s)
            else:
                l[i][j] = s / l[j][j]
    return l


def solve_lower(l, b):
    x = [0.0] * len(b)
    for i in range(len(b)):
        x[i] = (b[i] - sum(l[i][j] * x[j] for j in range(i))) / l[i][i]
    return x


def solve_upper_from_lower(l, b):
    n = len(b)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(l[j][i] * x[j] for j in range(i + 1, n))) / l[i][i]
    return x


def factor_preconditioner(a, block):
    n = len(a)
    if block == 0:
        return []
    factors = []
    for start in range(0, n, block):
        stop = min(start + block, n)
        sub = [[a[i][j] for j in range(start, stop)] for i in range(start, stop)]
        factors.append((start, stop, cholesky(sub)))
    return factors


def apply_pc(factors, r):
    if not factors:
        return r[:]
    z = [0.0] * len(r)
    for start, stop, l in factors:
        y = solve_lower(l, r[start:stop])
        z[start:stop] = solve_upper_from_lower(l, y)
    return z


def full_l_from_blocks(n, factors):
    if not factors:
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    out = [[0.0] * n for _ in range(n)]
    for start, stop, l in factors:
        for i in range(stop - start):
            for j in range(i + 1):
                out[start + i][start + j] = l[i][j]
    return out


def symmetric_preconditioned(a, factors):
    n = len(a)
    l = full_l_from_blocks(n, factors)
    # B=L^{-1}A, column by column.
    b = [[0.0] * n for _ in range(n)]
    for j in range(n):
        col = solve_lower(l, [a[i][j] for i in range(n)])
        for i in range(n):
            b[i][j] = col[i]
    # C=B L^{-T}; equivalently C^T=L^{-1}B^T.
    ct = [[0.0] * n for _ in range(n)]
    for j in range(n):
        col = solve_lower(l, b[j][:])
        for i in range(n):
            ct[i][j] = col[i]
    c = [[0.5 * (ct[j][i] + ct[i][j]) for j in range(n)] for i in range(n)]
    return c


def jacobi_eigvals(a0, sweeps=100):
    a = [row[:] for row in a0]
    n = len(a)
    for _ in range(sweeps * n * n):
        p, q, largest = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest < 1e-12:
            break
        tau = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau)) if tau else 1.0
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p], a[q][q], a[p][q], a[q][p] = app - t * apq, aqq + t * apq, 0.0, 0.0
        for r in range(n):
            if r in (p, q):
                continue
            arp, arq = a[r][p], a[r][q]
            a[r][p] = a[p][r] = c * arp - s * arq
            a[r][q] = a[q][r] = s * arp + c * arq
    return sorted(a[i][i] for i in range(n))


def pcg(a, b, factors, maxit=100, tol=1e-10):
    n = len(b)
    x = [0.0] * n
    r = b[:]
    z = apply_pc(factors, r)
    p = z[:]
    rz = dot(r, z)
    base = norm(b)
    hist = [(0, 1.0)]
    for k in range(1, maxit + 1):
        ap = matvec(a, p)
        denom = dot(p, ap)
        if denom <= 0.0:
            break
        alpha = rz / denom
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r = [ri - alpha * api for ri, api in zip(r, ap)]
        rel = norm([bi - ai for bi, ai in zip(b, matvec(a, x))]) / base
        hist.append((k, max(rel, 1e-16)))
        if rel <= tol:
            break
        z = apply_pc(factors, r)
        rz_new = dot(r, z)
        beta = rz_new / rz
        p = [zi + beta * pi for zi, pi in zip(z, p)]
        rz = rz_new
    return hist


def build_problem(n=32):
    scale = [10.0 ** (4.0 * i / (n - 1)) * (1.0 + 0.18 * math.sin(0.73 * (i + 1))) for i in range(n)]
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = 2.0 * scale[i]
        if i + 1 < n:
            off = -math.sqrt(scale[i] * scale[i + 1])
            a[i][i + 1] = a[i + 1][i] = off
    xtrue = [math.sin(0.41 * (i + 1)) + 0.2 * math.cos(1.17 * (i + 1)) for i in range(n)]
    return a, matvec(a, xtrue)


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
        out += [f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>', f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>']
    for val, label in yticks:
        frac = logmap(val, ylo, yhi, 0, h) if ylog else (val - ylo) / (yhi - ylo) * h
        y = y0 + h - frac
        out += [f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>', f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>']
    out += [f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>', f'<text x="{x0-55}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-55} {y0+h/2})">{esc(ylabel)}</text>']
    return out


def poly(points, color, dash=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x, y, color, shape="circle", r=3.2):
    if shape == "square": return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond": return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    n = 32
    a, b = build_problem(n)
    blocks = [0, 1, 2, 4, 8, 16, 32]
    factors = {bs: factor_preconditioner(a, bs) for bs in blocks}
    eigsets = {}
    for bs in (0, 1, 8):
        eigsets[bs] = jacobi_eigvals(symmetric_preconditioned(a, factors[bs]))
    kappas = {bs: eigsets[bs][-1] / eigsets[bs][0] for bs in eigsets}
    histories = {bs: pcg(a, b, factors[bs], maxit=80, tol=1e-10) for bs in blocks}
    iterations = {bs: next((k for k, v in histories[bs] if v <= 1e-8), histories[bs][-1][0]) for bs in blocks}
    # Proxy includes sparse tridiagonal matvec, block setup, and triangular solves.
    work = {}
    for bs in blocks:
        effective = 1 if bs == 0 else bs
        setup = 0.0 if bs == 0 else n * effective * effective / 3.0
        apply = 0.0 if bs == 0 else 2.0 * n * effective
        work[bs] = setup + iterations[bs] * (3.0 * n + apply)

    W, H = 1440, 610
    c = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Preconditioning changes the spectrum seen by Krylov methods</title>',
           '<desc id="desc">Three panels compare eigenvalue distributions, PCG residual histories, and iteration versus work tradeoffs for block Jacobi preconditioners.</desc>',
           '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">预条件不是求逆：它用廉价近似重塑 Krylov 方法看到的谱</text>']
    for x, title in [(75, "A  对称预条件后的特征值分布"), (555, "B  同一系统的 PCG 真残差"), (1035, "C  预条件强度的工作—迭代取舍")]:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    x0, y0, w, h = 75, 88, 330, 330
    allvals = [v for vals in eigsets.values() for v in vals]
    elo, ehi = min(allvals) * 0.8, max(allvals) * 1.25
    svg += axes(x0, y0, w, h, [(1e-3, "10⁻³"), (1e-1, "10⁻¹"), (1e1, "10"), (1e3, "10³"), (1e5, "10⁵")],
                [(0, ""), (1, "none"), (2, "Jacobi"), (3, "block-8"), (4, "")], "特征值 λ（log）", "预条件", True, False)
    rowmap = {0: 1, 1: 2, 8: 3}
    colors = {0: c["red"], 1: c["blue"], 8: c["green"]}
    shapes = {0: "square", 1: "circle", 8: "diamond"}
    for bs in (0, 1, 8):
        y = y0 + h - rowmap[bs] / 4 * h
        for value in eigsets[bs]:
            x = x0 + logmap(value, 1e-3, 1e5, 0, w)
            svg.append(mark(x, y, colors[bs], shapes[bs], 2.5))
    svg.append(f'<text x="90" y="112" class="note">κ: {kappas[0]:.1e} → {kappas[1]:.1f} → {kappas[8]:.1f}</text>')

    x1 = 555
    svg += axes(x1, y0, w, h, [(0, "0"), (15, "15"), (30, "30"), (45, "45"), (60, "60")],
                [(1e-12, "10⁻¹²"), (1e-9, "10⁻⁹"), (1e-6, "10⁻⁶"), (1e-3, "10⁻³"), (1, "1")], "PCG 迭代次数", "真残差 / ‖b‖₂", False, True)
    for bs, color, shape, dash in [(0, c["red"], "square", ""), (1, c["blue"], "circle", ""), (4, c["orange"], "square", "6 4"), (8, c["green"], "diamond", "")]:
        pts = [(x1 + min(k, 60) / 60 * w, y0 + h - logmap(v, 1e-12, 1, 0, h)) for k, v in histories[bs] if k <= 60]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::8]: svg.append(mark(px, py, color, shape))
    svg.append('<text x="570" y="112" class="note">对角缩放先修复单位失衡；更大块继续捕获局部耦合</text>')

    x2 = 1035
    xmin, xmax = min(work.values()) * 0.75, max(work.values()) * 1.3
    svg += axes(x2, y0, w, h, [(1e3, "10³"), (3e3, "3×10³"), (1e4, "10⁴"), (3e4, "3×10⁴"), (1e5, "10⁵")],
                [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40")], "总工作代理（log）", "达到 10⁻⁸ 的迭代数", True, False)
    for bs in blocks:
        x = x2 + logmap(work[bs], 1e3, 1e5, 0, w)
        y = y0 + h - min(iterations[bs], 40) / 40 * h
        color = c["red"] if bs == 0 else c["green"]
        svg.append(mark(x, y, color, "diamond" if bs else "square", 4))
        label = "none" if bs == 0 else ("exact" if bs == n else f"b{bs}")
        svg.append(f'<text x="{x+7:.2f}" y="{y-7:.2f}" class="note">{label}</text>')
    svg.append('<text x="1050" y="112" class="note">代理含 setup、三对角 matvec 与 block solve；只比较本矩阵族</text>')

    legends = [(95, c["red"], "square", "none"), (180, c["blue"], "circle", "Jacobi"), (285, c["green"], "diamond", "block-8"),
               (575, c["red"], "square", "none"), (650, c["blue"], "circle", "Jacobi"), (745, c["orange"], "square", "block-4"), (845, c["green"], "diamond", "block-8")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 显示谱重塑；B 用原系统真残差验收；C 表明更强预条件通常减少迭代，却可能增加 setup、内存与每步成本。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_krylov_preconditioning.py · Python 标准库 · n=32 变尺度 SPD 三对角矩阵</text>')
    svg.append('</svg>')
    if kappas[8] >= kappas[0] / 1000.0 or iterations[8] >= iterations[0] / 5.0:
        raise RuntimeError("preconditioned spectrum/iteration audit failed")
    if work[8] >= work[0]:
        raise RuntimeError("block-8 work proxy no longer improves on the unpreconditioned solve")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"saved={OUT}")
    for bs in (0, 1, 8): print(f"spectrum:block={bs},min={eigsets[bs][0]:.6e},max={eigsets[bs][-1]:.6e},kappa={kappas[bs]:.6e}")
    for bs in blocks: print(f"pcg:block={bs},iter1e-8={iterations[bs]},final={histories[bs][-1][1]:.3e},work={work[bs]:.3e}")


if __name__ == "__main__":
    main()
