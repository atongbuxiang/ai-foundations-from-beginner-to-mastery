#!/usr/bin/env python3
"""Deterministic least-squares stability experiment using only stdlib."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "least-squares" / "plot-least-squares-stability-v2.svg"


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.hypot(*x)


def matvec(a, x):
    return [dot(row, x) for row in a]


def tmatvec(a, x):
    return [sum(a[i][j] * x[i] for i in range(len(a))) for j in range(len(a[0]))]


def residual(a, x, b):
    return [u - v for u, v in zip(matvec(a, x), b)]


def normal_equations_2col(a, b):
    c1 = [row[0] for row in a]
    c2 = [row[1] for row in a]
    g11, g12, g22 = dot(c1, c1), dot(c1, c2), dot(c2, c2)
    h1, h2 = dot(c1, b), dot(c2, b)
    det = g11 * g22 - g12 * g12
    if det == 0.0 or not math.isfinite(det):
        return None
    return [(g22 * h1 - g12 * h2) / det, (g11 * h2 - g12 * h1) / det]


def householder_ls(a0, b0):
    a = [row[:] for row in a0]
    b = b0[:]
    m, n = len(a), len(a[0])
    for k in range(n):
        x = [a[i][k] for i in range(k, m)]
        nx = norm(x)
        if nx == 0.0:
            continue
        alpha = -math.copysign(nx, x[0] if x[0] != 0.0 else 1.0)
        v = x[:]
        v[0] -= alpha
        vv = dot(v, v)
        beta = 2.0 / vv
        for j in range(k, n):
            tau = beta * sum(v[i - k] * a[i][j] for i in range(k, m))
            for i in range(k, m):
                a[i][j] -= tau * v[i - k]
        tau = beta * sum(v[i - k] * b[i] for i in range(k, m))
        for i in range(k, m):
            b[i] -= tau * v[i - k]
    r11, r12, r22 = a[0][0], a[0][1], a[1][1]
    if r11 == 0.0 or r22 == 0.0:
        return None
    x2 = b[1] / r22
    x1 = (b[0] - r12 * x2) / r11
    return [x1, x2]


def structured_svd_ls(eps, b, cutoff=0.0):
    # A = [[1,1],[eps,0],[0,eps]] has exact right singular vectors
    # v+ = (1,1)/sqrt(2), v- = (1,-1)/sqrt(2).
    rt2 = math.sqrt(2.0)
    vecs = [[1.0 / rt2, 1.0 / rt2], [1.0 / rt2, -1.0 / rt2]]
    sigmas = [math.sqrt(2.0 + eps * eps), abs(eps)]
    a = [[1.0, 1.0], [eps, 0.0], [0.0, eps]]
    threshold = cutoff * sigmas[0]
    ans = [0.0, 0.0]
    for v, sigma in zip(vecs, sigmas):
        if sigma <= threshold:
            continue
        av = matvec(a, v)
        u = [z / sigma for z in av]
        coeff = dot(u, b) / sigma
        ans[0] += coeff * v[0]
        ans[1] += coeff * v[1]
    return ans


def relerr(x, ref):
    if x is None or any(not math.isfinite(v) for v in x):
        return 1.0
    return min(1.0, norm([x[i] - ref[i] for i in range(len(ref))]) / norm(ref))


def fmt(v):
    if v == 0:
        return "0"
    if v >= 1e3 or v < 1e-2:
        return f"{v:.1e}"
    return f"{v:.3g}"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def logmap(value, lo, hi, start, end):
    value = max(lo, min(hi, value))
    return start + (math.log10(value) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (end - start)


def line(points, color, dash=""):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5"{d}/>'


def circle(x, y, color, shape="circle"):
    if shape == "square":
        return f'<rect x="{x-3:.2f}" y="{y-3:.2f}" width="6" height="6" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M {x:.2f} {y-4:.2f} L {x+4:.2f} {y:.2f} L {x:.2f} {y+4:.2f} L {x-4:.2f} {y:.2f} Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{color}"/>'


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel, xlog=True, ylog=True):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    for v, lab in xticks:
        x = logmap(v, xticks[0][0], xticks[-1][0], x0, x0+w) if xlog else x0 + (v-xticks[0][0])/(xticks[-1][0]-xticks[0][0])*w
        out.append(f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>')
        out.append(f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(lab)}</text>')
    for v, lab in yticks:
        y = y0+h-(logmap(v, yticks[0][0], yticks[-1][0], 0, h) if ylog else (v-yticks[0][0])/(yticks[-1][0]-yticks[0][0])*h)
        out.append(f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>')
        out.append(f'<text x="{x0-10}" y="{y+4:.2f}" text-anchor="end">{esc(lab)}</text>')
    out.append(f'<text x="{x0+w/2}" y="{y0+h+46}" text-anchor="middle" class="axis">{esc(xlabel)}</text>')
    out.append(f'<text x="{x0-54}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-54} {y0+h/2})">{esc(ylabel)}</text>')
    return out


def main():
    eps_values = [10.0 ** (-k) for k in range(1, 13)]
    ref = [1.0, -1.0]
    rows = []
    for eps in eps_values:
        a = [[1.0, 1.0], [eps, 0.0], [0.0, eps]]
        r = [eps, -1.0, -1.0]
        # Keep the irreducible residual at a fixed fraction of ||A x|| so that
        # the diagnostic comparison is not confounded by a changing noise ratio.
        delta = 1e-8 * eps
        b0 = matvec(a, ref)
        b = [b0[i] + delta * r[i] for i in range(3)]
        kappa = math.sqrt(2.0 + eps * eps) / eps
        methods = {
            "normal": normal_equations_2col(a, b),
            "qr": householder_ls(a, b),
            "svd": structured_svd_ls(eps, b),
        }
        row = {"eps": eps, "kappa": kappa}
        for name, x in methods.items():
            row[name] = relerr(x, ref)
            if x is None:
                row[name + "_res"] = 1.0
                row[name + "_stat"] = 1.0
            else:
                rr = residual(a, x, b)
                row[name + "_res"] = norm(rr) / norm(b)
                row[name + "_stat"] = norm(tmatvec(a, rr)) / (norm(a[0]) * max(norm(rr), 1e-300))
        rows.append(row)

    # A diagonal spectral model isolates the bias--variance tradeoff of TSVD:
    # progressively weak coordinates contain progressively worse SNR.
    singulars = [1.0, 1e-2, 1e-4, 1e-6, 1e-8]
    clean = singulars[:]
    noise = [0.0, 2e-8, -3e-8, 4e-8, -5e-8]
    noisy = [clean[i] + noise[i] for i in range(len(clean))]
    cutoffs = [0.0, 1e-9, 1e-7, 1e-5, 1e-3, 1e-1]
    trade = []
    for c in cutoffs:
        threshold = c * singulars[0]
        x = [noisy[i] / singulars[i] if singulars[i] > threshold else 0.0 for i in range(len(singulars))]
        rr = [singulars[i] * x[i] - noisy[i] for i in range(len(singulars))]
        trade.append((c if c else 1e-10, norm(rr), norm(x)))

    W, H = 1440, 610
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">Least-squares stability: normal equations, QR, SVD, and truncation</title>',
        '<desc id="desc">Three panels show coefficient error versus condition number, residual and stationarity diagnostics, and the residual-solution-norm tradeoff under singular-value truncation.</desc>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B;stroke-width:1.5}.grid{stroke:#D7DEE8;stroke-width:1}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        '<text id="vis-title" x="720" y="34" text-anchor="middle" class="title">稳定最小二乘：小残差不等于参数可信</text>',
    ]
    colors = {"normal": "#c43d3d", "qr": "#2f6fbd", "svd": "#248a57"}
    shapes = {"normal": "square", "qr": "circle", "svd": "diamond"}

    # Panel A
    x0, y0, w, h = 82, 88, 365, 330
    svg.append('<text x="82" y="67" class="panel">A  参数前向误差</text>')
    svg += axes(x0, y0, w, h,
                [(1e1,"10¹"),(1e4,"10⁴"),(1e8,"10⁸"),(1e12,"10¹²")],
                [(1e-16,"10⁻¹⁶"),(1e-12,"10⁻¹²"),(1e-8,"10⁻⁸"),(1e-4,"10⁻⁴"),(1.0,"1")],
                "κ₂(A)（对数）", "||x̂−x||₂ / ||x||₂")
    for name in ["normal","qr","svd"]:
        pts=[]
        for row in rows:
            x=logmap(row["kappa"],1e1,1e12,x0,x0+w)
            y=y0+h-logmap(max(row[name],1e-16),1e-16,1.0,0,h)
            pts.append((x,y)); svg.append(circle(x,y,colors[name],shapes[name]))
        svg.append(line(pts,colors[name],"7 4" if name=="normal" else ""))
    svg.append('<text x="95" y="111" class="note">正规方程约在 κ≈u⁻¹ᐟ² 后失去弱方向</text>')

    # Panel B: at hardest nonsingular before total failure, compare residual/stationarity/error.
    x1, y1, w1, h1 = 555, 88, 330, 330
    svg.append('<text x="555" y="67" class="panel">B  三种验收量不可互换</text>')
    svg += axes(x1,y1,w1,h1,[(0,"正规方程"),(1,"Householder QR"),(2,"结构 SVD")],
                [(1e-16,"10⁻¹⁶"),(1e-12,"10⁻¹²"),(1e-8,"10⁻⁸"),(1e-4,"10⁻⁴"),(1.0,"1")],
                "方法（κ₂(A)≈1.4×10⁷）", "相对量（对数）",xlog=False,ylog=True)
    hard=min(rows,key=lambda r:abs(math.log10(r["kappa"])-7.15))
    metrics=[("参数误差","",0), ("原始残差","_res",1), ("驻点残差","_stat",2)]
    metric_colors=["#8b4bb6","#e08a28","#2b8a86"]
    names=["normal","qr","svd"]
    for mi,(label,suffix,_) in enumerate(metrics):
        pts=[]
        for j,name in enumerate(names):
            x=x1+(j/2)*w1
            val=max(hard[name+suffix],1e-16)
            y=y1+h1-logmap(val,1e-16,1.0,0,h1)
            x += (mi-1)*10
            pts.append((x,y)); svg.append(circle(x,y,metric_colors[mi],["circle","square","diamond"][mi]))
        svg.append(line(pts,metric_colors[mi]))
    svg.append('<text x="570" y="111" class="note">残差接近噪声地板时，参数仍可因病态放大而错误</text>')

    # Panel C: L-curve-like tradeoff.
    x2,y2,w2,h2=1010,88,350,330
    svg.append('<text x="1010" y="67" class="panel">C  截断 SVD 的偏差—方差取舍</text>')
    svg += axes(x2,y2,w2,h2,[(1e-8,"10⁻⁸"),(1e-6,"10⁻⁶"),(1e-4,"10⁻⁴"),(1e-2,"10⁻²")],
                [(1.0,"1"),(3.0,"3"),(10.0,"10")],
                "||Ax̂−b||₂", "||x̂||₂")
    pts=[]
    for cutoff,resn,xn in trade:
        xx=logmap(max(resn,1e-8),1e-8,1e-2,x2,x2+w2)
        yy=y2+h2-logmap(max(xn,1.0),1.0,10.0,0,h2)
        pts.append((xx,yy)); svg.append(circle(xx,yy,"#6a55a3","diamond"))
        if cutoff in (1e-10,1e-7,1e-5,1e-3):
            lab="无截断" if cutoff==1e-10 else f"rcond={cutoff:.0e}"
            svg.append(f'<text x="{xx+7:.2f}" y="{yy-7:.2f}" class="note">{lab}</text>')
    svg.append(line(pts,"#6a55a3"))
    svg.append('<text x="1025" y="111" class="note">舍弃弱方向会增加残差，但抑制解范数与噪声放大</text>')

    # Shared legend and footer.
    lx=100
    for i,(name,label) in enumerate([("normal","正规方程"),("qr","Householder QR"),("svd","结构 SVD")]):
        x=lx+i*155; svg.append(circle(x,500,colors[name],shapes[name])); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    for i,(label,color,shape) in enumerate([("参数误差","#8b4bb6","circle"),("原始残差","#e08a28","square"),("驻点残差","#2b8a86","diamond")]):
        x=610+i*145; svg.append(circle(x,500,color,shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">A/B：Aε=[[1,1],[ε,0],[0,ε]]、x=(1,−1)、固定相对正交残差；C：奇异值 1…10⁻⁸ 的对角谱加固定噪声。仅验证这些确定性构造。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_least_squares_stability.py · Python 标准库 · seed=无随机性</text>')
    svg.append('</svg>')
    if rows[-1]["normal"] != 1.0 or max(rows[-1]["qr"], rows[-1]["svd"]) >= 1e-12:
        raise RuntimeError("normal-equations versus QR/SVD separation audit failed")
    if not (trade[0][1] < trade[-1][1] and trade[0][2] > trade[-1][2]):
        raise RuntimeError("truncated-SVD residual/solution-norm tradeoff audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"saved={OUT}")
    print("least_squares:kappa,normal_err,qr_err,svd_err,normal_res,qr_res,svd_res")
    for r in rows:
        print(",".join(fmt(r[k]) for k in ["kappa","normal","qr","svd","normal_res","qr_res","svd_res"]))
    print("truncation:cutoff,residual,solution_norm")
    for row in trade:
        print(",".join(fmt(v) for v in row))


if __name__ == "__main__":
    main()
