#!/usr/bin/env python3
"""Deterministic Lanczos experiment: Ritz convergence, residuals and orthogonality."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "lanczos" / "plot-lanczos-ritz-orthogonality-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(dot(x, x))


def normalize(x):
    n = norm(x)
    return [v / n for v in x]


def matvec_diag(d, x):
    return [a * b for a, b in zip(d, x)]


def quantize(x, digits):
    return [round(v, digits) for v in x] if digits is not None else x


def jacobi_eigh(a0, sweeps=100):
    """Small real symmetric eigensolver; returns ascending values and eigenvectors by columns."""
    a = [row[:] for row in a0]
    n = len(a)
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps * max(1, n * n)):
        p, q, largest = 0, 1 if n > 1 else 0, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest < 1e-14:
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
    order = sorted(range(n), key=lambda i: a[i][i])
    vals = [a[i][i] for i in order]
    vecs = [[v[r][i] for i in order] for r in range(n)]
    return vals, vecs


def lanczos(d, q1, steps, reorth=False, digits=None):
    n = len(d)
    q = normalize(q1)
    qprev = [0.0] * n
    beta_prev = 0.0
    qs = [q]
    alphas, betas = [], []
    for j in range(steps):
        z = [v - beta_prev * qp for v, qp in zip(matvec_diag(d, q), qprev)]
        alpha = dot(q, z)
        z = [v - alpha * qi for v, qi in zip(z, q)]
        if reorth:
            for _ in range(2):
                for old in qs:
                    c = dot(old, z)
                    z = [v - c * oi for v, oi in zip(z, old)]
        z = quantize(z, digits)
        beta = norm(z)
        alphas.append(alpha)
        betas.append(beta)
        if beta < 1e-14 or j + 1 == steps:
            break
        qprev, q = q, normalize(z)
        if digits is not None:
            q = normalize(quantize(q, digits))
        qs.append(q)
        beta_prev = beta
    return alphas, betas, qs


def tridiag(alphas, betas):
    n = len(alphas)
    t = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(alphas):
        t[i][i] = a
    for i in range(n - 1):
        t[i][i + 1] = t[i + 1][i] = betas[i]
    return t


def orth_defect(qs):
    defect = 0.0
    for i, qi in enumerate(qs):
        for j, qj in enumerate(qs):
            target = 1.0 if i == j else 0.0
            defect = max(defect, abs(dot(qi, qj) - target))
    return defect


def ritz_data(d, q1, k):
    # Use the literal three-term recurrence here so the cheap residual identity
    # is the exact algebraic relation being tested; reorthogonalization is
    # isolated in panel C.
    alphas, betas, qs = lanczos(d, q1, k, reorth=False)
    vals, vecs = jacobi_eigh(tridiag(alphas, betas))
    theta = vals[-1]
    y = [vecs[i][-1] for i in range(len(vals))]
    x = [sum(qs[j][i] * y[j] for j in range(len(y))) for i in range(len(d))]
    direct = norm([a * b - theta * b for a, b in zip(d, x)])
    cheap = abs(betas[len(alphas) - 1] * y[-1])
    return vals[0], vals[-1], direct, cheap


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def logmap(v, lo, hi, a, b):
    v = max(lo, min(hi, v))
    return a + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (b - a)


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel, ylog=True):
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
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x, y, color, shape="circle"):
    if shape == "square":
        return f'<rect x="{x-3:.2f}" y="{y-3:.2f}" width="6" height="6" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-4:.2f} L{x+4:.2f},{y:.2f} L{x:.2f},{y+4:.2f} L{x-4:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="{color}"/>'


def main():
    n = 40
    d = [10.0, 7.0] + [6.0 - 5.5 * i / (n - 3) for i in range(n - 2)]
    q1 = [math.sin(0.71 * (i + 1)) + 0.2 * math.cos(1.13 * (i + 1)) for i in range(n)]
    ks = list(range(2, 31))
    extreme, residuals = [], []
    for k in ks:
        lo, hi, direct, cheap = ritz_data(d, q1, k)
        extreme.append((k, max(abs(hi - max(d)), 1e-16), max(abs(lo - min(d)), 1e-16)))
        residuals.append((k, max(direct, 1e-16), max(cheap, 1e-16)))

    d_cluster = [8.0, 7.999, 7.998] + [2.0 - 1.5 * i / 56 for i in range(57)]
    q_cluster = [math.sin(0.37 * (i + 1)) + 0.3 for i in range(60)]
    orth = []
    for k in range(2, 46):
        _, _, q_short = lanczos(d_cluster, q_cluster, k, reorth=False, digits=9)
        _, _, q_full = lanczos(d_cluster, q_cluster, k, reorth=True, digits=9)
        orth.append((k, max(orth_defect(q_short), 1e-16), max(orth_defect(q_full), 1e-16)))

    W, H = 1440, 610
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Lanczos Ritz convergence, residual identity and orthogonality</title>',
           '<desc id="desc">Three panels show convergence of extremal Ritz values, agreement of direct and cheap residuals, and finite-precision loss of orthogonality with and without reorthogonalization.</desc>',
           '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">Lanczos：小型三对角投影暴露极端谱，也暴露有限精度代价</text>']
    panels = [(75, "A  极端 Ritz 值先收敛"), (555, "B  残差无需形成高维 Ritz 向量"), (1035, "C  三项递推不保证浮点全局正交")]
    for x, title in panels:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    colors = {"a": "#2f6fbd", "b": "#c36a14", "c": "#248a57", "d": "#8a4fb8"}
    x0, y0, w, h = 75, 88, 330, 330
    svg += axes(x0, y0, w, h, [(2, "2"), (9, "9"), (16, "16"), (23, "23"), (30, "30")],
                [(1e-16, "10⁻¹⁶"), (1e-12, "10⁻¹²"), (1e-8, "10⁻⁸"), (1e-4, "10⁻⁴"), (1.0, "1")], "Lanczos 步数 k", "Ritz 值绝对误差")
    for idx, color, shape in [(1, colors["a"], "circle"), (2, colors["b"], "square")]:
        pts = []
        for row in extreme:
            x = x0 + (row[0] - 2) / 28 * w
            y = y0 + h - logmap(row[idx], 1e-16, 1, 0, h)
            pts.append((x, y))
        svg.append(poly(pts, color))
        for x, y in pts[::4]: svg.append(mark(x, y, color, shape))
    svg.append('<text x="90" y="112" class="note">对称投影 + 交错定理使边界 Ritz 值有结构化趋近</text>')

    x1 = 555
    svg += axes(x1, y0, w, h, [(2, "2"), (9, "9"), (16, "16"), (23, "23"), (30, "30")],
                [(1e-16, "10⁻¹⁶"), (1e-12, "10⁻¹²"), (1e-8, "10⁻⁸"), (1e-4, "10⁻⁴"), (1.0, "1")], "Lanczos 步数 k", "主 Ritz 对残差范数")
    for idx, color, shape, dash in [(1, colors["c"], "diamond", ""), (2, colors["d"], "square", "6 4")]:
        pts = []
        for row in residuals:
            x = x1 + (row[0] - 2) / 28 * w
            y = y0 + h - logmap(row[idx], 1e-16, 1, 0, h)
            pts.append((x, y))
        svg.append(poly(pts, color, dash))
        for x, y in pts[::4]: svg.append(mark(x, y, color, shape))
    svg.append('<text x="570" y="112" class="note">直接 ‖Ax−θx‖ 与 |βₖ eₖᵀy| 重合</text>')

    x2 = 1035
    svg += axes(x2, y0, w, h, [(2, "2"), (13, "13"), (24, "24"), (35, "35"), (45, "45")],
                [(1e-16, "10⁻¹⁶"), (1e-12, "10⁻¹²"), (1e-8, "10⁻⁸"), (1e-4, "10⁻⁴"), (1.0, "1")], "Lanczos 步数 k", "max |qᵢᵀqⱼ−δᵢⱼ|")
    for idx, color, shape in [(1, "#c43d3d", "square"), (2, colors["c"], "diamond")]:
        pts = []
        for row in orth:
            x = x2 + (row[0] - 2) / 43 * w
            y = y0 + h - logmap(row[idx], 1e-16, 1, 0, h)
            pts.append((x, y))
        svg.append(poly(pts, color))
        for x, y in pts[::6]: svg.append(mark(x, y, color, shape))
    svg.append('<text x="1050" y="112" class="note">模拟 9 位运算；聚簇极端谱放大正交性回流</text>')

    legends = [(95, colors["a"], "circle", "最大 Ritz 值误差"), (245, colors["b"], "square", "最小 Ritz 值误差"),
               (575, colors["c"], "diamond", "直接残差"), (720, colors["d"], "square", "廉价残差公式"),
               (1055, "#c43d3d", "square", "仅三项递推"), (1205, colors["c"], "diamond", "全重正交化")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 为 40 阶对角谱；B 验证 Ritz 残差恒等式；C 用显式降精度隔离有限精度正交性丢失，不代表特定硬件格式。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_lanczos_ritz_orthogonality.py · Python 标准库 · 无随机性</text>')
    svg.append('</svg>')
    if extreme[-1][1] >= 1e-10 or max(abs(direct - cheap) for _, direct, cheap in residuals) >= 1e-10:
        raise RuntimeError("Lanczos Ritz/residual identity audit failed")
    if orth[-1][1] <= 0.5 or orth[-1][2] >= 1e-6:
        raise RuntimeError("Lanczos reorthogonalization separation audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"saved={OUT}")
    for k in (5, 10, 20, 30):
        row = extreme[ks.index(k)]; rr = residuals[ks.index(k)]
        print(f"ritz:k={k},max_err={row[1]:.3e},min_err={row[2]:.3e},direct_res={rr[1]:.3e},cheap_res={rr[2]:.3e}")
    for k in (10, 20, 30, 40, 45):
        row = orth[k - 2]
        print(f"orth:k={k},short={row[1]:.3e},full={row[2]:.3e}")


if __name__ == "__main__":
    main()
