#!/usr/bin/env python3
"""Generate a deterministic SVG for Householder/Givens QR stability.

Only the Python standard library is used.  The experiment isolates:
1) Householder target-sign cancellation;
2) unsafe versus scaled Givens radius generation;
3) loss of orthogonality for MGS versus Householder/Givens QR.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "qr" / "plot-householder-givens-qr-v2.svg"
FLOOR = 1.0e-18


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm2(x):
    return math.sqrt(dot(x, x))


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(col) for col in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def frobenius(a):
    return math.sqrt(sum(x * x for row in a for x in row))


def matrix_sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def orthogonality_defect(q):
    n = len(q[0])
    return frobenius(matrix_sub(matmul(transpose(q), q), identity(n)))


def reconstruction_error(a, q, r):
    denom = frobenius(a)
    return frobenius(matrix_sub(a, matmul(q, r))) / denom


def householder_apply(x, stable):
    """Return tail retention |(Hx)_2|/|x_2| for a 2-vector."""
    nrm = math.hypot(x[0], x[1])
    if stable:
        alpha = -math.copysign(nrm, x[0] if x[0] != 0.0 else 1.0)
    else:
        alpha = nrm
    v = [x[0] - alpha, x[1]]
    vv = dot(v, v)
    if vv == 0.0 or not math.isfinite(vv):
        return 1.0
    scale = 2.0 * dot(v, x) / vv
    y = [x[i] - scale * v[i] for i in range(2)]
    return abs(y[1]) / abs(x[1])


def givens_residual(f, g, safe):
    """Return normalized annihilation residual, mapping invalid outputs to one."""
    if safe:
        radius = math.hypot(f, g)
    else:
        square_sum = f * f + g * g
        radius = math.sqrt(square_sum)
    if radius == 0.0 or not math.isfinite(radius):
        return 1.0
    c = f / radius
    s = g / radius
    if not all(math.isfinite(z) for z in (c, s)):
        return 1.0
    tail = -s * f + c * g
    scale = math.hypot(f, g)
    if scale == 0.0 or not math.isfinite(scale):
        return 1.0
    return abs(tail) / scale


def mgs_qr(a):
    m = len(a)
    n = len(a[0])
    qcols = []
    r = [[0.0] * n for _ in range(n)]
    for j in range(n):
        v = [a[i][j] for i in range(m)]
        for i, qi in enumerate(qcols):
            rij = dot(qi, v)
            r[i][j] = rij
            v = [vk - rij * qik for vk, qik in zip(v, qi)]
        r[j][j] = norm2(v)
        if r[j][j] == 0.0:
            qcols.append([0.0] * m)
        else:
            qcols.append([vk / r[j][j] for vk in v])
    q = [[qcols[j][i] for j in range(n)] for i in range(m)]
    return q, r


def apply_reflector_left(a, start, v, tau, first_col=0):
    ncols = len(a[0])
    for j in range(first_col, ncols):
        w = tau * sum(v[t] * a[start + t][j] for t in range(len(v)))
        for t in range(len(v)):
            a[start + t][j] -= v[t] * w


def householder_qr(a):
    m = len(a)
    n = len(a[0])
    r = [row[:] for row in a]
    reflectors = []
    for k in range(min(m, n)):
        x = [r[i][k] for i in range(k, m)]
        nrm = norm2(x)
        if nrm == 0.0:
            reflectors.append((k, [1.0] + [0.0] * (len(x) - 1), 0.0))
            continue
        alpha = -math.copysign(nrm, x[0] if x[0] != 0.0 else 1.0)
        v = x[:]
        v[0] -= alpha
        vv = dot(v, v)
        tau = 2.0 / vv
        apply_reflector_left(r, k, v, tau, k)
        r[k][k] = alpha
        for i in range(k + 1, m):
            if abs(r[i][k]) < 64.0 * math.ulp(1.0) * max(1.0, nrm):
                r[i][k] = 0.0
        reflectors.append((k, v, tau))

    q = identity(m)
    for k, v, tau in reversed(reflectors):
        apply_reflector_left(q, k, v, tau, 0)
    qthin = [row[:n] for row in q]
    rthin = [row[:n] for row in r[:n]]
    return qthin, rthin


def apply_givens_rows(a, i, j, c, s, first_col=0):
    for k in range(first_col, len(a[0])):
        x = a[i][k]
        y = a[j][k]
        a[i][k] = c * x + s * y
        a[j][k] = -s * x + c * y


def givens_qr(a):
    m = len(a)
    n = len(a[0])
    r = [row[:] for row in a]
    qt = identity(m)
    for col in range(n):
        for row in range(m - 1, col, -1):
            f = r[row - 1][col]
            g = r[row][col]
            radius = math.hypot(f, g)
            if radius == 0.0:
                continue
            c = f / radius
            s = g / radius
            apply_givens_rows(r, row - 1, row, c, s, col)
            apply_givens_rows(qt, row - 1, row, c, s, 0)
            r[row][col] = 0.0
    q = transpose(qt)
    qthin = [row[:n] for row in q]
    rthin = [row[:n] for row in r[:n]]
    return qthin, rthin


def dct_orthogonal(n):
    q = []
    for i in range(n):
        row = []
        for j in range(n):
            scale = math.sqrt(1.0 / n) if j == 0 else math.sqrt(2.0 / n)
            row.append(scale * math.cos(math.pi * (i + 0.5) * j / n))
        q.append(row)
    return q


def structured_matrix(n, eps):
    """Deterministic dense matrix with singular values from one to eps."""
    u = dct_orthogonal(n)
    # A distinct orthogonal right factor avoids a coordinate-aligned easy case.
    v = [row[1:] + row[:1] for row in u]
    singular = [eps ** (j / (n - 1)) for j in range(n)]
    return [
        [sum(u[i][k] * singular[k] * v[j][k] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def fmt(value):
    return f"{value:.3e}"


def xmap(x, x0, x1, left, width):
    return left + (x - x0) * width / (x1 - x0)


def ymap_log(y, top, height, ymin=FLOOR, ymax=1.0):
    y = min(ymax, max(ymin, y))
    lo = math.log10(ymin)
    hi = math.log10(ymax)
    return top + (hi - math.log10(y)) * height / (hi - lo)


def path(points, x_domain, left, top, width, height):
    coords = []
    for x, y in points:
        px = xmap(x, x_domain[0], x_domain[1], left, width)
        py = ymap_log(y, top, height)
        coords.append((px, py))
    return " ".join(("M" if i == 0 else "L") + f"{x:.2f},{y:.2f}" for i, (x, y) in enumerate(coords))


def circles(points, x_domain, left, top, width, height, color):
    chunks = []
    for x, y in points:
        px = xmap(x, x_domain[0], x_domain[1], left, width)
        py = ymap_log(y, top, height)
        chunks.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="3" fill="{color}"/>')
    return "".join(chunks)


def make_svg(house_data, givens_data, qr_data):
    width, height = 1440, 800
    panel_w = 360
    plot_h = 500
    top = 160
    lefts = [86, 545, 1004]
    colors = {
        "red": "#dc2626",
        "blue": "#2563eb",
        "green": "#059669",
        "purple": "#7c3aed",
        "orange": "#ea580c",
    }
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 800" role="img" aria-labelledby="title desc">',
        '<title id="title">Stable Householder signs, safe Givens scaling, and QR orthogonality</title>',
        '<desc id="desc">Panel A compares stable and cancellation-prone Householder target signs. Panel B compares naive squared Givens radius with safe scaling across extreme magnitudes. Panel C compares orthogonality defects of modified Gram-Schmidt, Householder, and Givens QR as condition number grows.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;fill:#1F2937}.title{font-size:27px;font-weight:760}.subtitle{font-size:17px;fill:#64748B}.panel{font-size:19px;font-weight:700}.axis{font-size:16px}.tick{font-size:15px;fill:#64748B}.legend{font-size:15px}.callout{font-size:15px;font-weight:650}</style>',
        '<text class="title" x="720" y="38" text-anchor="middle">正交变换的稳定性来自两层：安全生成局部变换 + 正交序列不放大误差</text>',
        '<text class="subtitle" x="720" y="66" text-anchor="middle">左：Householder 符号 · 中：Givens 极端尺度 · 右：近相关列上的 QR 正交性</text>',
        '<text class="panel" x="266" y="110" text-anchor="middle">A. Householder 尾部分量保留比例</text>',
        '<text class="panel" x="725" y="110" text-anchor="middle">B. Givens 消零相对残差</text>',
        '<text class="panel" x="1184" y="110" text-anchor="middle">C. ||I − QᵀQ||F</text>',
    ]

    for left in lefts:
        for exponent in range(-18, 1, 3):
            y = ymap_log(10.0**exponent, top, plot_h)
            svg.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left+panel_w}" y2="{y:.2f}" stroke="#e5eaf0"/>')
            svg.append(f'<text class="tick" x="{left-10}" y="{y+4:.2f}" text-anchor="end">10^{exponent}</text>')
        svg.append(f'<rect x="{left}" y="{top}" width="{panel_w}" height="{plot_h}" fill="none" stroke="#334155"/>')

    # Panel A
    a_naive = [(row[0], max(FLOOR, row[1])) for row in house_data]
    a_stable = [(row[0], max(FLOOR, row[2])) for row in house_data]
    for points, color in ((a_naive, colors["red"]), (a_stable, colors["blue"])):
        svg.append(f'<path d="{path(points, (1,18), lefts[0],top,panel_w,plot_h)}" fill="none" stroke="{color}" stroke-width="3"/>')
        svg.append(circles(points, (1,18), lefts[0],top,panel_w,plot_h,color))
    for k in [1, 4, 7, 10, 13, 16, 18]:
        x = xmap(k, 1, 18, lefts[0], panel_w)
        svg.append(f'<text class="tick" x="{x:.2f}" y="{top+plot_h+26}" text-anchor="middle">{k}</text>')
    svg.append(f'<text class="axis" x="{lefts[0]+panel_w/2}" y="{top+plot_h+58}" text-anchor="middle">k in x = (1, 10⁻ᵏ)</text>')
    svg.append(f'<line x1="116" y1="190" x2="146" y2="190" stroke="{colors["red"]}" stroke-width="3"/><text class="legend" x="156" y="194">固定同号目标</text>')
    svg.append(f'<line x1="116" y1="216" x2="146" y2="216" stroke="{colors["blue"]}" stroke-width="3"/><text class="legend" x="156" y="220">相反符号目标</text>')
    svg.append('<rect x="285" y="176" width="145" height="58" rx="8" fill="#fff7ed" stroke="#fb923c"/><text class="callout" x="357" y="198" text-anchor="middle">k≈8 后同号相减</text><text class="tick" x="357" y="218" text-anchor="middle">尾部几乎原样保留</text>')

    # Panel B
    b_naive = [(row[0], max(FLOOR, row[1])) for row in givens_data]
    b_safe = [(row[0], max(FLOOR, row[2])) for row in givens_data]
    for points, color in ((b_naive, colors["red"]), (b_safe, colors["green"])):
        svg.append(f'<path d="{path(points, (-300,300), lefts[1],top,panel_w,plot_h)}" fill="none" stroke="{color}" stroke-width="3"/>')
        svg.append(circles(points, (-300,300), lefts[1],top,panel_w,plot_h,color))
    for exponent in [-300, -150, 0, 150, 300]:
        x = xmap(exponent, -300, 300, lefts[1], panel_w)
        svg.append(f'<text class="tick" x="{x:.2f}" y="{top+plot_h+26}" text-anchor="middle">{exponent}</text>')
    svg.append(f'<text class="axis" x="{lefts[1]+panel_w/2}" y="{top+plot_h+58}" text-anchor="middle">e in f,g = O(10ᵉ)</text>')
    svg.append(f'<line x1="575" y1="190" x2="605" y2="190" stroke="{colors["red"]}" stroke-width="3"/><text class="legend" x="615" y="194">sqrt(f²+g²)</text>')
    svg.append(f'<line x1="575" y1="216" x2="605" y2="216" stroke="{colors["green"]}" stroke-width="3"/><text class="legend" x="615" y="220">safe scaling / hypot</text>')
    svg.append('<rect x="739" y="176" width="150" height="58" rx="8" fill="#ecfdf5" stroke="#10b981"/><text class="callout" x="814" y="198" text-anchor="middle">真实半径仍可表示</text><text class="tick" x="814" y="218" text-anchor="middle">朴素平方先失败</text>')

    # Panel C
    series = [
        ([(row[0], max(FLOOR, row[1])) for row in qr_data], colors["purple"], "MGS"),
        ([(row[0], max(FLOOR, row[2])) for row in qr_data], colors["blue"], "Householder"),
        ([(row[0], max(FLOOR, row[3])) for row in qr_data], colors["green"], "Givens"),
    ]
    for points, color, _ in series:
        svg.append(f'<path d="{path(points, (1,14), lefts[2],top,panel_w,plot_h)}" fill="none" stroke="{color}" stroke-width="3"/>')
        svg.append(circles(points, (1,14), lefts[2],top,panel_w,plot_h,color))
    for exponent in [1, 4, 7, 10, 13, 14]:
        x = xmap(exponent, 1, 14, lefts[2], panel_w)
        svg.append(f'<text class="tick" x="{x:.2f}" y="{top+plot_h+26}" text-anchor="middle">{exponent}</text>')
    svg.append(f'<text class="axis" x="{lefts[2]+panel_w/2}" y="{top+plot_h+58}" text-anchor="middle">log₁₀ κ₂(A)</text>')
    ylegend = 190
    for _, color, label in series:
        svg.append(f'<line x1="1034" y1="{ylegend}" x2="1064" y2="{ylegend}" stroke="{color}" stroke-width="3"/><text class="legend" x="1074" y="{ylegend+4}">{label}</text>')
        ylegend += 26
    svg.append('<rect x="1210" y="176" width="140" height="78" rx="8" fill="#eff6ff" stroke="#60a5fa"/><text class="callout" x="1280" y="198" text-anchor="middle">反射 / 旋转</text><text class="tick" x="1280" y="218" text-anchor="middle">正交性近舍入地板</text><text class="tick" x="1280" y="238" text-anchor="middle">MGS 随 κ 上升</text>')

    svg.append('<text class="subtitle" x="720" y="760" text-anchor="middle">读图：局部参数必须安全生成；之后正交变换序列才能把误差控制在邻近输入尺度。图示结论不外推为任何特定 GPU 库的性能排序。</text>')
    svg.append('</svg>')
    return "\n".join(svg) + "\n"


def main():
    house_data = []
    for k in range(1, 19):
        x = [1.0, 10.0 ** (-k)]
        house_data.append((k, householder_apply(x, False), householder_apply(x, True)))

    exponents = [-300, -250, -200, -160, -154, -153, -100, 0, 100, 153, 154, 160, 200, 250, 300]
    givens_data = []
    for exponent in exponents:
        scale = 10.0**exponent
        f = 1.3 * scale
        g = 0.9 * scale
        givens_data.append((exponent, givens_residual(f, g, False), givens_residual(f, g, True)))

    qr_data = []
    n = 12
    for k in range(1, 15):
        eps = 10.0 ** (-k)
        a = structured_matrix(n, eps)
        condition = 1.0 / eps
        log_condition = math.log10(condition)
        qm, rm = mgs_qr(a)
        qh, rh = householder_qr(a)
        qg, rg = givens_qr(a)
        qr_data.append(
            (
                log_condition,
                orthogonality_defect(qm),
                orthogonality_defect(qh),
                orthogonality_defect(qg),
                reconstruction_error(a, qm, rm),
                reconstruction_error(a, qh, rh),
                reconstruction_error(a, qg, rg),
            )
        )

    if house_data[-1][1] != 1.0 or max(row[2] for row in house_data) >= 1e-12:
        raise RuntimeError("Householder sign-choice separation audit failed")
    if givens_data[0][1] != 1.0 or max(row[2] for row in givens_data) >= 1e-12:
        raise RuntimeError("safe-scaled Givens audit failed")
    if qr_data[-1][1] <= 1e-5 or max(qr_data[-1][2], qr_data[-1][3]) >= 1e-12:
        raise RuntimeError("orthogonal-transform QR audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(make_svg(house_data, givens_data, qr_data), encoding="utf-8")
    print(f"saved={OUT}")
    print("householder:k,tail_ratio_naive,tail_ratio_stable")
    for row in house_data:
        print(f"{row[0]},{fmt(row[1])},{fmt(row[2])}")
    print("givens:exponent,residual_naive,residual_safe")
    for row in givens_data:
        print(f"{row[0]},{fmt(row[1])},{fmt(row[2])}")
    print("qr:log10_condition,orth_mgs,orth_householder,orth_givens,rec_mgs,rec_householder,rec_givens")
    for row in qr_data:
        print(",".join(fmt(value) for value in row))


if __name__ == "__main__":
    main()
