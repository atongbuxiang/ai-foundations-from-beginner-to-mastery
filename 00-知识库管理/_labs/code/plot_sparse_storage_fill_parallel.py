#!/usr/bin/env python3
"""Deterministic sparse-matrix experiment: storage, fill-in, and parallel load balance."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "sparse-computing" / "plot-sparse-storage-fill-parallel-v2.svg"


def grid_graph(m):
    n = m * m
    adj = [set() for _ in range(n)]
    for i in range(m):
        for j in range(m):
            v = i * m + j
            if i + 1 < m:
                w = (i + 1) * m + j
                adj[v].add(w)
                adj[w].add(v)
            if j + 1 < m:
                w = i * m + j + 1
                adj[v].add(w)
                adj[w].add(v)
    return adj


def symbolic_cholesky_nnz(adj0, ordering):
    adj = [set(s) for s in adj0]
    active = set(range(len(adj)))
    total = 0
    for v in ordering:
        nbr = list(adj[v] & active)
        total += 1 + len(nbr)
        for i, a in enumerate(nbr):
            for b in nbr[i + 1:]:
                adj[a].add(b)
                adj[b].add(a)
        active.remove(v)
    return total


def greedy_min_degree_order(adj0):
    adj = [set(s) for s in adj0]
    active = set(range(len(adj)))
    order = []
    while active:
        v = min(active, key=lambda x: (len(adj[x] & active), x))
        nbr = list(adj[v] & active)
        for i, a in enumerate(nbr):
            for b in nbr[i + 1:]:
                adj[a].add(b)
                adj[b].add(a)
        active.remove(v)
        order.append(v)
    return order


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
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x, y, color, shape="circle", r=3.2):
    if shape == "square":
        return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    # Panel A: theoretical bytes for an n x n float64 matrix with int32 indices.
    n = 10_000
    densities = [10.0 ** (-5 + 5 * i / 60) for i in range(61)]
    storage = []
    for d in densities:
        nnz = max(1, int(d * n * n))
        dense_mb = 8 * n * n / 1e6
        csr_mb = (8 * nnz + 4 * nnz + 4 * (n + 1)) / 1e6
        coo_mb = (8 * nnz + 4 * nnz + 4 * nnz) / 1e6
        storage.append((d, dense_mb, csr_mb, coo_mb))

    # Panel B: symbolic fill for 2-D grid Laplacians.
    fill = []
    for m in range(4, 17):
        adj = grid_graph(m)
        base_lower = len(adj) + sum(len(s) for s in adj) // 2
        natural = symbolic_cholesky_nnz(adj, list(range(len(adj))))
        md_order = greedy_min_degree_order(adj)
        mindeg = symbolic_cholesky_nnz(adj, md_order)
        fill.append((m, natural / base_lower, mindeg / base_lower, natural, mindeg))

    # Panel C: irregular row lengths and worker assignment.
    workers = 8
    nrows = 128
    row_nnz = [max(2, int(500 / ((i + 1) ** 0.72) + 3 * (1 + math.sin(0.61 * i)))) for i in range(nrows)]
    chunk = nrows // workers
    equal_rows = [sum(row_nnz[w * chunk:(w + 1) * chunk]) for w in range(workers)]
    balanced = [0] * workers
    for cost in sorted(row_nnz, reverse=True):
        w = min(range(workers), key=lambda j: (balanced[j], j))
        balanced[w] += cost
    avg = sum(row_nnz) / workers
    equal_norm = [v / avg for v in equal_rows]
    balanced_norm = [v / avg for v in balanced]
    crossover = (8 - 4 / n) / 12
    assert 0.66 < crossover < 0.67
    assert all(mindeg < natural for _, natural, mindeg, _, _ in fill)
    assert max(balanced_norm) < 1.05 and max(equal_norm) > 3.0

    W, H = 1440, 610
    c = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Sparse storage, factorization fill, and parallel imbalance</title>',
           '<desc id="desc">Three panels compare dense, CSR, and COO memory; symbolic Cholesky fill under natural and minimum-degree orderings; and equal-row versus nonzero-balanced parallel assignments.</desc>',
           '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;font-size:15px;fill:#1f2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#fffefb;stroke:#d7dee8}.grid{stroke:#e2e8f0}.note{font-size:15px;fill:#64748b}.legend{font-size:15px}</style>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<text x="720" y="34" text-anchor="middle" class="title">稀疏不是一个百分比：格式、消元图与负载共同决定真实成本</text>']
    for x, title in [(75, "A  n=10⁴：索引开销与稠密交叉点"), (555, "B  二维网格 Cholesky 的排序 fill-in"), (1035, "C  同 nnz，不同并行行分配")]:
        svg.append(f'<text x="{x}" y="67" class="panel">{title}</text>')

    x0, y0, w, h = 75, 88, 330, 330
    svg += axes(x0, y0, w, h, [(1e-5, "10⁻⁵"), (1e-4, "10⁻⁴"), (1e-3, "10⁻³"), (1e-2, "10⁻²"), (1e-1, "10⁻¹"), (1, "1")],
                [(0.01, ".01"), (0.1, ".1"), (1, "1"), (10, "10"), (100, "100"), (1000, "1000")],
                "密度 nnz/n²", "存储 MB（值 float64，索引 int32）", True, True)
    for idx, color, shape, dash in [(1, c["red"], "square", ""), (2, c["blue"], "circle", ""), (3, c["orange"], "diamond", "6 4")]:
        pts = [(x0 + logmap(row[0], 1e-5, 1, 0, w), y0 + h - logmap(row[idx], .01, 1000, 0, h)) for row in storage]
        svg.append(poly(pts, color, dash))
        for px, py in pts[::12]:
            svg.append(mark(px, py, color, shape))
    svg.append(f'<text x="90" y="112" class="note">CSR 约在密度 {crossover:.2f} 后不再比纯 dense 值数组省内存</text>')

    x1 = 555
    svg += axes(x1, y0, w, h, [(4, "4"), (7, "7"), (10, "10"), (13, "13"), (16, "16")],
                [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")],
                "网格边长 m（n=m²）", "nnz(L) / 原下三角 nnz", False, False)
    for idx, color, shape in [(1, c["red"], "square"), (2, c["green"], "diamond")]:
        pts = [(x1 + (row[0] - 4) / 12 * w, y0 + h - (row[idx] - 1) / 5 * h) for row in fill]
        svg.append(poly(pts, color))
        for px, py in pts[::3]:
            svg.append(mark(px, py, color, shape))
    svg.append('<text x="570" y="112" class="note">同一 SPD 系统只做对称置换；因子非零数却显著改变</text>')

    x2 = 1035
    svg += axes(x2, y0, w, h, [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8")],
                [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")],
                "worker", "本地 nnz / 平均 nnz", False, False)
    barw = 13
    for i in range(workers):
        cx = x2 + i / 7 * w
        h1 = equal_norm[i] / 4 * h
        h2 = balanced_norm[i] / 4 * h
        svg.append(f'<rect x="{cx-barw-2:.2f}" y="{y0+h-h1:.2f}" width="{barw}" height="{h1:.2f}" fill="{c["orange"]}"/>')
        svg.append(f'<rect x="{cx+2:.2f}" y="{y0+h-h2:.2f}" width="{barw}" height="{h2:.2f}" fill="{c["blue"]}"/>')
    yavg = y0 + h - h / 4
    svg.append(f'<line x1="{x2}" y1="{yavg:.2f}" x2="{x2+w}" y2="{yavg:.2f}" stroke="{c["green"]}" stroke-dasharray="5 4"/>')
    svg.append(f'<text x="1050" y="112" class="note">等行数最大负载={max(equal_norm):.2f}×平均；按 nnz 分配={max(balanced_norm):.2f}×</text>')

    legends = [(90, c["red"], "square", "dense"), (190, c["blue"], "circle", "CSR"), (270, c["orange"], "diamond", "COO"),
               (575, c["red"], "square", "natural"), (690, c["green"], "diamond", "greedy min-degree"),
               (1060, c["orange"], "square", "equal rows"), (1180, c["blue"], "square", "nnz-balanced")]
    for x, color, shape, label in legends:
        svg.append(mark(x, 500, color, shape))
        svg.append(f'<text x="{x+11}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A 说明索引不是免费；B 说明 fill 由消元顺序决定；C 说明平均 nnz 不能预测并行关键路径。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_sparse_storage_fill_parallel.py · Python 标准库 · 确定性结构实验</text>')
    svg.append('</svg>')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"saved={OUT}")
    print(f"storage:n={n},csr_dense_crossover={crossover:.6f}")
    for m, natural, mindeg, nn, mn in fill[::4]:
        print(f"fill:m={m},natural_ratio={natural:.6f},mindeg_ratio={mindeg:.6f},natural_nnz={nn},mindeg_nnz={mn}")
    print(f"balance:equal_max={max(equal_norm):.6f},balanced_max={max(balanced_norm):.6f},equal_eff={1/max(equal_norm):.6f},balanced_eff={1/max(balanced_norm):.6f}")


if __name__ == "__main__":
    main()
