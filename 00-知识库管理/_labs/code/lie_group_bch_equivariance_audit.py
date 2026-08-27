#!/usr/bin/env python3
"""Deterministic Lie exponential, BCH, and group-averaging audit.

Standard library only. The canonical artifact is a standalone SVG with three
tracks and embedded numerical summaries. Assertions turn the figure generator
into a small executable verification gate.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "00-知识库管理/_assets/plots/geometry/plot-lie-group-bch-equivariance-v2.svg"


def mat_add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def mat_scale(c, a):
    return [[c * x for x in row] for row in a]


def mat_mul(a, b):
    rows, inner, cols = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def fro(a):
    return math.sqrt(sum(x * x for row in a for x in row))


def mat_sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def rot2(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]


def hat(v):
    x, y, z = v
    return [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]]


def rot3(v):
    """exp(hat(v)) by Rodrigues, stable at zero."""
    theta = math.sqrt(sum(x * x for x in v))
    k = hat(v)
    k2 = mat_mul(k, k)
    if theta < 1.0e-8:
        a = 1.0 - theta * theta / 6.0 + theta**4 / 120.0
        b = 0.5 - theta * theta / 24.0 + theta**4 / 720.0
    else:
        a = math.sin(theta) / theta
        b = (1.0 - math.cos(theta)) / (theta * theta)
    return mat_add(mat_add(eye(3), mat_scale(a, k)), mat_scale(b, k2))


def observed_order(xs, errors):
    slopes = []
    for i in range(len(xs) - 1):
        slopes.append(math.log(errors[i] / errors[i + 1]) / math.log(xs[i] / xs[i + 1]))
    return sum(slopes[-3:]) / min(3, len(slopes))


def track_a():
    hs = [0.4 / (2**k) for k in range(7)]
    j = [[0.0, -1.0], [1.0, 0.0]]
    errors = []
    group_law = []
    orth = []
    det_res = []
    for h in hs:
        central = mat_scale(1.0 / (2.0 * h), mat_sub(rot2(h), rot2(-h)))
        errors.append(fro(mat_sub(central, j)))
        lhs = mat_mul(rot2(0.71), rot2(-0.33))
        group_law.append(fro(mat_sub(lhs, rot2(0.38))))
        r = rot2(h)
        orth.append(fro(mat_sub(mat_mul(transpose(r), r), eye(2))))
        det_res.append(abs(det2(r) - 1.0))
    order = observed_order(hs, errors)
    assert 1.995 < order < 2.005, order
    assert max(group_law) < 5.0e-16
    assert max(orth) < 4.0e-16
    assert max(det_res) < 3.0e-16
    return {"x": hs, "error": errors, "order": order, "group": max(group_law), "orth": max(orth), "det": max(det_res)}


def track_b():
    scales = [0.4 / (2**k) for k in range(7)]
    naive, bch2 = [], []
    for a in scales:
        target = mat_mul(rot3((a, 0.0, 0.0)), rot3((0.0, a, 0.0)))
        naive.append(fro(mat_sub(target, rot3((a, a, 0.0)))))
        bch2.append(fro(mat_sub(target, rot3((a, a, 0.5 * a * a)))))
    p2 = observed_order(scales, naive)
    p3 = observed_order(scales, bch2)
    assert 1.99 < p2 < 2.01, p2
    assert 2.98 < p3 < 3.02, p3
    assert bch2[-1] < naive[-1] / 100.0
    return {"x": scales, "naive": naive, "bch2": bch2, "p2": p2, "p3": p3}


def shift_matrix(n, k=1):
    s = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        s[(i + k) % n][i] = 1.0
    return s


def dense_seed_matrix(n):
    return [[
        math.sin(0.37 * (i + 1) * (j + 2))
        + 0.23 * math.cos(0.61 * (2 * i - j + 1))
        + (0.17 if i == j else 0.0)
        for j in range(n)
    ] for i in range(n)]


def conjugate_average(a, count):
    n = len(a)
    out = [[0.0 for _ in range(n)] for _ in range(n)]
    for k in range(count):
        sk = shift_matrix(n, k)
        smk = transpose(sk)
        term = mat_mul(mat_mul(smk, a), sk)
        out = mat_add(out, term)
    return mat_scale(1.0 / count, out)


def equivariance_defect(a, s):
    return fro(mat_sub(mat_mul(a, s), mat_mul(s, a))) / max(fro(a), 1.0e-300)


def circulant_from_first_column(c):
    n = len(c)
    return [[c[(i - j) % n] for j in range(n)] for i in range(n)]


def track_c():
    n = 12
    a = dense_seed_matrix(n)
    s = shift_matrix(n)
    counts = list(range(1, n + 1))
    defects = [equivariance_defect(conjugate_average(a, m), s) for m in counts]
    full = conjugate_average(a, n)
    circular = circulant_from_first_column([math.sin(0.4 * i) + 0.1 * i for i in range(n)])
    circular_defect = equivariance_defect(circular, s)
    column_residual = 0.0
    c0 = [full[i][0] for i in range(n)]
    for j in range(n):
        expected = [c0[(i - j) % n] for i in range(n)]
        column_residual = max(column_residual, math.sqrt(sum((full[i][j] - expected[i]) ** 2 for i in range(n))))
    assert defects[0] > 0.25
    assert defects[-1] < 2.0e-15
    assert circular_defect < 2.0e-16
    assert column_residual < 2.0e-15
    return {"count": counts, "defect": defects, "raw": defects[0], "full": defects[-1], "conv": circular_defect, "column": column_residual}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def log_map(v, lo, hi, y0, y1):
    floor = 1.0e-17
    z = math.log10(max(v, floor))
    return y1 - (z - lo) / (hi - lo) * (y1 - y0)


def polyline(points, color, width=2.5, dash=""):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>'


def circles(points, color):
    return "".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.6" fill="{color}"/>' for x, y in points)


def panel_axes(x, y, w, h, title, subtitle, ylabels):
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="panel"/>',
        f'<text x="{x+18}" y="{y+28}" class="title">{esc(title)}</text>',
        f'<text x="{x+18}" y="{y+48}" class="sub">{esc(subtitle)}</text>',
    ]
    ax_l, ax_r = x + 58, x + w - 18
    ax_t, ax_b = y + 72, y + h - 58
    parts.append(f'<path d="M{ax_l},{ax_t} V{ax_b} H{ax_r}" class="axis"/>')
    for label, frac in ylabels:
        yy = ax_b - frac * (ax_b - ax_t)
        parts.append(f'<path d="M{ax_l},{yy:.2f} H{ax_r}" class="grid"/>')
        parts.append(f'<text x="{ax_l-8}" y="{yy+4:.2f}" text-anchor="end" class="tick">{esc(label)}</text>')
    return parts, (ax_l, ax_r, ax_t, ax_b)


def build_svg(a, b, c):
    W, H = 1200, 560
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">']
    out.append('<title id="title">Lie exponential, BCH, and group-averaging equivariance audit</title>')
    out.append('<desc id="desc">Three panels verify the SO(2) generator, the second- and third-order errors of a naive sum and BCH correction in SO(3), and Reynolds averaging onto a cyclic-equivariant linear map.</desc>')
    out.append("""<style>
    svg{font-family:'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
    .bg{fill:#fff}.panel{fill:#fff;stroke:#cbd5e1;stroke-width:1.4}.title{font:700 22px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#0f172a}.sub{font:500 15px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#475569}.axis{fill:none;stroke:#334155;stroke-width:1.3}.grid{stroke:#e2e8f0;stroke-width:1}.tick{font:500 15px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#64748b}.label{font:600 17px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#334155}.head{font:700 24px 'Inter','Noto Sans CJK SC','Source Han Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#0f172a}.foot{font:500 15px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#334155}
    </style>""")
    out.append(f'<rect width="{W}" height="{H}" class="bg"/>')
    out.append('<text x="30" y="34" class="head">Lie 指数、BCH 与群平均等变审计</text>')
    out.append('<text x="1170" y="32" text-anchor="end" class="sub">deterministic · Python standard library · 2026-08-19</text>')

    # Track A
    parts, box = panel_axes(20, 52, 370, 400, "A  SO(2) generator", "central difference: order 2", [("1e-1", 0.8), ("1e-3", 0.6), ("1e-5", 0.4), ("1e-7", 0.2), ("1e-9", 0.0)])
    out += parts
    l, r, t, bot = box
    pts = []
    for i, e in enumerate(a["error"]):
        xx = l + i / (len(a["error"]) - 1) * (r - l)
        yy = log_map(e, -9, -1, t, bot)
        pts.append((xx, yy))
    out.append(polyline(pts, "#2563eb")); out.append(circles(pts, "#2563eb"))
    out.append(f'<text x="{l+8}" y="{bot+22}" class="label">h: 0.4 → 0.00625</text>')
    out.append(f'<text x="{l+8}" y="{t+18}" class="label" fill="#2563eb">observed p = {a["order"]:.8f}</text>')
    out.append(f'<text x="{l+8}" y="{t+36}" class="tick">group law max = {a["group"]:.2e}</text>')
    out.append(f'<text x="{l+8}" y="{t+51}" class="tick">orthogonality max = {a["orth"]:.2e}</text>')

    # Track B
    parts, box = panel_axes(415, 52, 370, 400, "B  SO(3) and BCH", "naive O(a²); BCH O(a³)", [("1e-1", 1.0), ("1e-4", 0.75), ("1e-7", 0.5), ("1e-10", 0.25), ("1e-13", 0.0)])
    out += parts
    l, r, t, bot = box
    p_naive, p_bch = [], []
    for i, (e1, e2) in enumerate(zip(b["naive"], b["bch2"])):
        xx = l + i / (len(b["naive"]) - 1) * (r - l)
        p_naive.append((xx, log_map(e1, -13, -1, t, bot)))
        p_bch.append((xx, log_map(e2, -13, -1, t, bot)))
    out.append(polyline(p_naive, "#e11d48")); out.append(circles(p_naive, "#e11d48"))
    out.append(polyline(p_bch, "#0f766e")); out.append(circles(p_bch, "#0f766e"))
    out.append(f'<text x="{l+8}" y="{t+18}" class="label" fill="#e11d48">exp(X+Y): p = {b["p2"]:.8f}</text>')
    out.append(f'<text x="{l+8}" y="{t+36}" class="label" fill="#0f766e">BCH₂: p = {b["p3"]:.8f}</text>')
    out.append(f'<text x="{l+8}" y="{bot+22}" class="label">a: 0.4 → 0.00625</text>')

    # Track C
    parts, box = panel_axes(810, 52, 370, 400, "C  C₁₂ Reynolds projection", "group average → circulant equivariance", [("1e0", 1.0), ("1e-4", 0.75), ("1e-8", 0.5), ("1e-12", 0.25), ("1e-16", 0.0)])
    out += parts
    l, r, t, bot = box
    pts = []
    for i, e in enumerate(c["defect"]):
        xx = l + i / (len(c["defect"]) - 1) * (r - l)
        pts.append((xx, log_map(e, -16, 0, t, bot)))
    out.append(polyline(pts, "#7c3aed")); out.append(circles(pts, "#7c3aed"))
    out.append(f'<text x="{l+8}" y="{t+18}" class="tick">raw defect = {c["raw"]:.3e}</text>')
    out.append(f'<text x="{l+8}" y="{t+35}" class="tick">full-group defect = {c["full"]:.3e}</text>')
    out.append(f'<text x="{l+8}" y="{t+52}" class="tick">circular-conv defect = {c["conv"]:.3e}</text>')
    out.append(f'<text x="{l+8}" y="{bot+22}" class="label">number of averaged elements: 1 → 12</text>')

    out.append('<text x="30" y="486" class="foot">Assertions: p(SO2)=2 · p(naive)=2 · p(BCH₂)=3.</text>')
    out.append('<text x="30" y="508" class="foot">Also: full C₁₂ averaging and circulant convolution commute with the shift.</text>')
    out.append('<text x="30" y="530" class="foot">Boundary: finite matrices only; no claim for learned accuracy or continuous-group discretization.</text>')
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
    print(f"so2_derivative_order={a['order']:.8f}")
    print(f"so3_naive_order={b['p2']:.8f}")
    print(f"so3_bch2_order={b['p3']:.8f}")
    print(f"raw_equivariance_defect={c['raw']:.12e}")
    print(f"full_group_defect={c['full']:.12e}")
    print(f"circular_convolution_defect={c['conv']:.12e}")
    print(f"output={args.output}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
