#!/usr/bin/env python3
"""Deterministic completeness, projection, and L2 conditional-mean audit."""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "00-知识库管理/_assets/plots/functional-analysis/plot-banach-hilbert-projection-v2.svg"


def observed_power(xs, errors):
    values = []
    for i in range(len(xs) - 1):
        values.append(math.log(errors[i] / errors[i + 1]) / math.log(xs[i + 1] / xs[i]))
    return sum(values[-3:]) / 3.0


def track_a():
    ns = [16 * (2**k) for k in range(7)]
    partial = 0.0
    errors = []
    blocks = []
    for n in ns:
        partial = sum(1.0 / (k * k) for k in range(1, n + 1))
        errors.append(math.sqrt(max(math.pi * math.pi / 6.0 - partial, 0.0)))
        blocks.append(sum(1.0 / k for k in range(n + 1, 2 * n + 1)))
    power = observed_power(ns, errors)
    assert 0.499 < power < 0.501, power
    assert blocks[-1] > 0.692 and abs(blocks[-1] - math.log(2.0)) < 8.0e-4
    return {"n": ns, "l2": errors, "l1_block": blocks, "power": power}


def track_b():
    ts = [-0.5 + 0.025 * i for i in range(81)]
    l1 = [abs(1.0 - t) + abs(t) for t in ts]
    l2 = [math.hypot(1.0 - t, t) for t in ts]
    plateau = [d for t, d in zip(ts, l1) if 0.0 <= t <= 1.0]
    min_l2 = min(l2)
    minimizers = [t for t, d in zip(ts, l2) if abs(d - min_l2) < 1.0e-14]
    pyth = max(abs(((1 - t) ** 2 + t * t) - (0.5 + 2.0 * (t - 0.5) ** 2)) for t in ts)
    assert max(abs(x - 1.0) for x in plateau) < 1.0e-15
    assert len(minimizers) == 1 and abs(minimizers[0] - 0.5) < 1.0e-15
    assert pyth < 5.0e-16
    return {"t": ts, "l1": l1, "l2": l2, "l2_min": min_l2, "pyth": pyth}


def integral_power(a, b, p):
    return (b ** (p + 1) - a ** (p + 1)) / (p + 1)


def track_c():
    ms = [4 * (2**k) for k in range(7)]
    projection_errors = []
    left_errors = []
    orth_residuals = []
    for m in ms:
        h = 1.0 / m
        ep2 = 0.0
        el2 = 0.0
        orth = 0.0
        for j in range(m):
            a, b = j * h, (j + 1) * h
            int_f = integral_power(a, b, 2)
            int_f2 = integral_power(a, b, 4)
            mean = int_f / h
            left = a * a
            ep2 += int_f2 - 2.0 * mean * int_f + mean * mean * h
            el2 += int_f2 - 2.0 * left * int_f + left * left * h
            orth = max(orth, abs(int_f - mean * h))
        projection_errors.append(math.sqrt(max(ep2, 0.0)))
        left_errors.append(math.sqrt(max(el2, 0.0)))
        orth_residuals.append(orth)
    p_proj = observed_power(ms, projection_errors)
    p_left = observed_power(ms, left_errors)
    ratio = left_errors[-1] / projection_errors[-1]
    assert 0.999 < p_proj < 1.001, p_proj
    assert 0.997 < p_left < 1.003, p_left
    assert 1.99 < ratio < 2.01, ratio
    assert max(orth_residuals) < 2.0e-17
    assert all(a < b for a, b in zip(projection_errors, left_errors))
    return {"m": ms, "projection": projection_errors, "left": left_errors, "p_proj": p_proj, "p_left": p_left, "ratio": ratio, "orth": max(orth_residuals)}


def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def polyline(points, color, width=2.5, dash=""):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>'


def dots(points, color):
    return "".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{color}"/>' for x, y in points)


def log_y(value, log_lo, log_hi, top, bottom):
    z = math.log10(max(value, 1.0e-18))
    return bottom - (z - log_lo) / (log_hi - log_lo) * (bottom - top)


def axes(x, y, w, h, title, subtitle, labels):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="panel"/>',
           f'<text x="{x+18}" y="{y+28}" class="title">{esc(title)}</text>',
           f'<text x="{x+18}" y="{y+48}" class="sub">{esc(subtitle)}</text>']
    left, right, top, bottom = x + 58, x + w - 18, y + 72, y + h - 58
    out.append(f'<path d="M{left},{top} V{bottom} H{right}" class="axis"/>')
    for label, frac in labels:
        yy = bottom - frac * (bottom - top)
        out.append(f'<path d="M{left},{yy:.2f} H{right}" class="grid"/>')
        out.append(f'<text x="{left-8}" y="{yy+4:.2f}" text-anchor="end" class="tick">{esc(label)}</text>')
    return out, (left, right, top, bottom)


def build_svg(a, b, c):
    width, height = 1200, 560
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">']
    out.append('<title id="title">Completeness, best approximation, and conditional-expectation projection audit</title>')
    out.append('<desc id="desc">Three panels compare one truncation sequence in l2 and l1, uniqueness of Hilbert projection with an l1 minimizer plateau, and cell-mean projection against endpoint sampling.</desc>')
    out.append("""<style>
    svg{font-family:'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
    .bg{fill:#fff}.panel{fill:#fff;stroke:#cbd5e1;stroke-width:1.4}.title{font:700 22px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#0f172a}.sub{font:500 15px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#475569}.axis{fill:none;stroke:#334155;stroke-width:1.3}.grid{stroke:#e2e8f0;stroke-width:1}.tick{font:500 15px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#64748b}.label{font:600 17px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#334155}.head{font:700 24px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#0f172a}.foot{font:500 15px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#334155}
    </style>""")
    out.append(f'<rect width="{width}" height="{height}" class="bg"/>')
    out.append('<text x="30" y="34" class="head">完备化、最佳逼近与条件期望投影审计</text>')
    out.append('<text x="1170" y="32" text-anchor="end" class="sub">deterministic · Python standard library · 2026-08-19</text>')

    parts, box = axes(20, 52, 370, 400, "A  Cauchy depends on norm", "c₀₀: ℓ² Cauchy; ℓ¹ not Cauchy", [("1e0", 1.0), ("1e-1", 0.67), ("1e-2", 0.33), ("1e-3", 0.0)])
    out += parts; l, r, t, bot = box
    p_l2, p_l1 = [], []
    for i, (e, q) in enumerate(zip(a["l2"], a["l1_block"])):
        xx = l + i / 6 * (r - l)
        p_l2.append((xx, log_y(e, -3, 0, t, bot)))
        p_l1.append((xx, log_y(q, -3, 0, t, bot)))
    out += [polyline(p_l2, "#2563eb"), dots(p_l2, "#2563eb"), polyline(p_l1, "#e11d48"), dots(p_l1, "#e11d48")]
    out.append(f'<text x="{l+8}" y="{t+18}" class="label" fill="#2563eb">ℓ² tail: N^(-{a["power"]:.6f})</text>')
    out.append(f'<text x="{l+8}" y="{t+37}" class="label" fill="#e11d48">ℓ¹ block → {a["l1_block"][-1]:.6f} ≈ log 2</text>')
    out.append(f'<text x="{l+8}" y="{bot+22}" class="label">N: 16 → 1024</text>')

    parts, box = axes(415, 52, 370, 400, "B  Projection uniqueness", "distance from (1,0) to t(1,1)", [("2.0", 1.0), ("1.5", 0.67), ("1.0", 0.33), ("0.5", 0.0)])
    out += parts; l, r, t, bot = box
    def lin_y(v): return bot - (v - 0.5) / 1.5 * (bot - t)
    p1, p2 = [], []
    for i, (d1, d2) in enumerate(zip(b["l1"], b["l2"])):
        xx = l + i / 80 * (r - l)
        p1.append((xx, lin_y(d1))); p2.append((xx, lin_y(d2)))
    out += [polyline(p1, "#e11d48"), polyline(p2, "#0f766e")]
    out.append(f'<text x="{l+8}" y="{t+18}" class="label" fill="#e11d48">ℓ¹: every t∈[0,1] minimizes</text>')
    out.append(f'<text x="{l+8}" y="{t+37}" class="label" fill="#0f766e">ℓ²: unique t=0.5, d={b["l2_min"]:.6f}</text>')
    out.append(f'<text x="{l+8}" y="{bot+22}" class="label">parameter t: −0.5 → 1.5</text>')

    parts, box = axes(810, 52, 370, 400, "C  Conditional-mean projection", "cell mean vs left sampling", [("1e-1", 1.0), ("1e-2", 0.67), ("1e-3", 0.33), ("1e-4", 0.0)])
    out += parts; l, r, t, bot = box
    pp, pl = [], []
    for i, (ep, el) in enumerate(zip(c["projection"], c["left"])):
        xx = l + i / 6 * (r - l)
        pp.append((xx, log_y(ep, -4, -1, t, bot))); pl.append((xx, log_y(el, -4, -1, t, bot)))
    out += [polyline(pp, "#2563eb"), dots(pp, "#2563eb"), polyline(pl, "#d97706"), dots(pl, "#d97706")]
    out.append(f'<text x="{l+8}" y="{t+18}" class="label" fill="#2563eb">cell mean: p={c["p_proj"]:.6f}</text>')
    out.append(f'<text x="{l+8}" y="{t+37}" class="label" fill="#d97706">left sample: p={c["p_left"]:.6f}</text>')
    out.append(f'<text x="{l+8}" y="{t+56}" class="tick">ratio={c["ratio"]:.3f}; orth &lt; 2e−17</text>')
    out.append(f'<text x="{l+8}" y="{bot+22}" class="label">number of bins: 4 → 256</text>')

    out.append('<text x="30" y="486" class="foot">Assertions: ℓ² tail order=1/2 · ℓ¹ block→log 2 · Hilbert projection is unique.</text>')
    out.append('<text x="30" y="508" class="foot">Also: ℓ¹ minimizers form a segment · cell means leave orthogonal residuals.</text>')
    out.append('<text x="30" y="530" class="foot">Boundary: analytic examples only; no claim for arbitrary Banach projections or learned operators.</text>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    a, b, c = track_a(), track_b(), track_c()
    svg = build_svg(a, b, c)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    print(f"l2_tail_power={a['power']:.8f}")
    print(f"l1_doubling_block={a['l1_block'][-1]:.12f}")
    print(f"hilbert_unique_minimum={b['l2_min']:.12f}")
    print(f"piecewise_projection_order={c['p_proj']:.8f}")
    print(f"left_sample_order={c['p_left']:.8f}")
    print(f"left_to_projection_error_ratio={c['ratio']:.8f}")
    print(f"max_orthogonality_residual={c['orth']:.12e}")
    print(f"output={args.output}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
