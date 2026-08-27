#!/usr/bin/env python3
"""Deterministic stationary-iteration experiment: modes, convergence and transient growth."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "stationary-iterations" / "plot-stationary-spectral-radius-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(dot(x, x))


def poisson_mv(x):
    n = len(x)
    return [2.0 * x[i] - (x[i - 1] if i else 0.0) - (x[i + 1] if i + 1 < n else 0.0) for i in range(n)]


def residual_norm(x, b):
    return norm([bi - ai for bi, ai in zip(b, poisson_mv(x))])


def iterate(method, b, sweeps, omega=1.0):
    n = len(b)
    x = [0.0] * n
    base = norm(b)
    hist = [(0, residual_norm(x, b) / base)]
    for k in range(1, sweeps + 1):
        old = x[:]
        if method == "jacobi":
            x = [(b[i] + (old[i - 1] if i else 0.0) + (old[i + 1] if i + 1 < n else 0.0)) / 2.0 for i in range(n)]
        else:
            for i in range(n):
                gs = (b[i] + (x[i - 1] if i else 0.0) + (old[i + 1] if i + 1 < n else 0.0)) / 2.0
                x[i] = (1.0 - omega) * old[i] + omega * gs
        hist.append((k, max(residual_norm(x, b) / base, 1e-16)))
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
    # Panel A: exact Fourier-mode factors for the 1-D Poisson Jacobi smoother.
    nmode = 64
    modes = []
    for j in range(1, nmode + 1):
        theta = j * math.pi / (nmode + 1)
        standard = abs(math.cos(theta))
        weighted = abs(1.0 - (2.0 / 3.0) * (1.0 - math.cos(theta)))
        modes.append((j / (nmode + 1), standard, weighted))

    # Panel B: same Poisson problem, different stationary splittings.
    n = 31
    xtrue = [1.0 + 0.25 * math.sin(3 * math.pi * (i + 1) / (n + 1)) + 0.1 * math.sin(11 * math.pi * (i + 1) / (n + 1)) for i in range(n)]
    b = poisson_mv(xtrue)
    rho_j = math.cos(math.pi / (n + 1))
    omega_opt = 2.0 / (1.0 + math.sqrt(1.0 - rho_j * rho_j))
    histories = {
        "Jacobi": iterate("jacobi", b, 120),
        "Gauss–Seidel": iterate("gs", b, 120),
        "SOR optimal": iterate("sor", b, 120, omega_opt),
        "SOR 1.95": iterate("sor", b, 120, 1.95),
    }

    # Panel C: rho(B)<1 is asymptotic; a nonnormal B may grow first.
    e = [0.0, 1.0]
    transient = []
    rho = 0.82
    for k in range(61):
        transient.append((k, max(norm(e), 1e-16), max(rho**k, 1e-16)))
        e = [0.82 * e[0] + 4.0 * e[1], 0.68 * e[1]]

    W, H = 1440, 610
    c = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Stationary iterations, spectral radius and nonnormal transient</title>',
           '<desc id="desc">Three panels show Jacobi mode damping, convergence histories of Jacobi Gauss-Seidel and SOR, and transient growth despite spectral radius below one.</desc>',
           '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">定常迭代：谱半径决定终局，分裂、频率与非正规性决定过程</text>']
    for x, title in [(75, "A  Jacobi 对不同误差频率的阻尼"), (555, "B  同一 Poisson 系统的收敛速度"), (1035, "C  ρ(B)&lt;1 仍可先暂态放大")]:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    x0, y0, w, h = 75, 88, 330, 330
    svg += axes(x0, y0, w, h, [(0, "0"), (0.25, "¼"), (0.5, "½"), (0.75, "¾"), (1, "1")],
                [(0, "0"), (0.25, ".25"), (0.5, ".5"), (0.75, ".75"), (1, "1")], "归一化频率 j/(n+1)", "单步放大因子", False)
    for idx, color, shape in [(1, c["blue"], "circle"), (2, c["orange"], "square")]:
        pts = [(x0 + row[0] * w, y0 + h - row[idx] * h) for row in modes]
        svg.append(poly(pts, color))
        for px, py in pts[::10]: svg.append(mark(px, py, color, shape))
    svg.append('<line x1="240" y1="88" x2="240" y2="418" stroke="#7b879a" stroke-dasharray="4 4"/>')
    svg.append('<text x="250" y="112" class="note">右半区是高频；ω=2/3 抑制高频</text>')

    x1 = 555
    svg += axes(x1, y0, w, h, [(0, "0"), (30, "30"), (60, "60"), (90, "90"), (120, "120")],
                [(1e-12, "10⁻¹²"), (1e-9, "10⁻⁹"), (1e-6, "10⁻⁶"), (1e-3, "10⁻³"), (1, "1")], "sweeps", "‖b−Axₖ‖₂ / ‖b‖₂", True)
    styles = [("Jacobi", c["blue"], "circle", ""), ("Gauss–Seidel", c["orange"], "square", ""),
              ("SOR optimal", c["green"], "diamond", ""), ("SOR 1.95", c["purple"], "square", "6 4")]
    for name, color, shape, dash in styles:
        pts = [(x1 + k / 120 * w, y0 + h - logmap(v, 1e-12, 1, 0, h)) for k, v in histories[name]]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::20]: svg.append(mark(px, py, color, shape))
    svg.append(f'<text x="570" y="112" class="note">n=31；理论 ω*={omega_opt:.3f}，接近 2 并不等于更快</text>')

    x2 = 1035
    svg += axes(x2, y0, w, h, [(0, "0"), (15, "15"), (30, "30"), (45, "45"), (60, "60")],
                [(1e-3, "10⁻³"), (1e-2, "10⁻²"), (1e-1, "10⁻¹"), (1, "1"), (10, "10"), (100, "100")], "迭代次数 k", "误差范数", True)
    for idx, color, shape, dash in [(1, c["red"], "square", ""), (2, c["green"], "diamond", "6 4")]:
        pts = [(x2 + k / 60 * w, y0 + h - logmap(v, 1e-3, 100, 0, h)) for k, *vals in transient for v in [vals[idx - 1]]]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::10]: svg.append(mark(px, py, color, shape))
    svg.append('<text x="1050" y="112" class="note">B=[[.82,4],[0,.68]]；谱半径 .82，但 ‖Bᵏe₂‖ 先增</text>')

    legends = [(95, c["blue"], "circle", "Jacobi ω=1"), (250, c["orange"], "square", "weighted Jacobi ω=2/3"),
               (570, c["blue"], "circle", "Jacobi"), (650, c["orange"], "square", "GS"), (710, c["green"], "diamond", "SOR ω*"), (810, c["purple"], "square", "SOR 1.95"),
               (1055, c["red"], "square", "实际 ‖Bᵏe₂‖"), (1200, c["green"], "diamond", "ρ(B)ᵏ")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 分离平滑与全局求解；B 比较分裂与松弛参数；C 提醒 ρ(B)&lt;1 是渐近判据，不承诺单调收缩。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_stationary_spectral_radius.py · Python 标准库 · 确定性数据</text>')
    svg.append('</svg>')
    peak = max(transient, key=lambda row: row[1])
    if histories["SOR optimal"][-1][1] >= 1e-8 or histories["Jacobi"][-1][1] <= 1e-2:
        raise RuntimeError("stationary-splitting convergence separation audit failed")
    if peak[1] <= 5.0 or transient[-1][1] <= 10.0 * transient[-1][2]:
        raise RuntimeError("nonnormal transient-growth audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"saved={OUT}")
    print(f"poisson:n={n},rho_j={rho_j:.8f},omega_opt={omega_opt:.8f}")
    for name in histories:
        vals = dict(histories[name])
        print(f"history:{name},k30={vals[30]:.3e},k60={vals[60]:.3e},k120={vals[120]:.3e}")
    print(f"transient:peak_k={peak[0]},peak={peak[1]:.6e},rho60={rho**60:.6e},actual60={transient[-1][1]:.6e}")


if __name__ == "__main__":
    main()
