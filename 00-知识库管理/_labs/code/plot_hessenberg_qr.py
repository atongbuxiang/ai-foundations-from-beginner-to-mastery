#!/usr/bin/env python3
"""Deterministic Hessenberg reduction and shifted-QR experiment (stdlib only)."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "hessenberg-qr" / "plot-hessenberg-qr-v2.svg"


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def frob(a):
    return math.sqrt(sum(x * x for row in a for x in row))


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def norm(x):
    return math.hypot(*x)


def householder_qr(a0):
    a = [row[:] for row in a0]
    m, n = len(a), len(a[0])
    q = eye(m)
    for k in range(min(m, n)):
        x = [a[i][k] for i in range(k, m)]
        nx = norm(x)
        if nx == 0.0:
            continue
        alpha = -math.copysign(nx, x[0] if x[0] else 1.0)
        v = x[:]
        v[0] -= alpha
        beta = 2.0 / sum(z * z for z in v)
        for j in range(k, n):
            tau = beta * sum(v[i-k] * a[i][j] for i in range(k, m))
            for i in range(k, m):
                a[i][j] -= tau * v[i-k]
        # Q <- Q H
        for i in range(m):
            tau = beta * sum(q[i][j] * v[j-k] for j in range(k, m))
            for j in range(k, m):
                q[i][j] -= tau * v[j-k]
    return q, a


def hessenberg(a0):
    a = [row[:] for row in a0]
    n = len(a)
    q = eye(n)
    for k in range(n - 2):
        x = [a[i][k] for i in range(k + 1, n)]
        nx = norm(x)
        if nx == 0.0:
            continue
        alpha = -math.copysign(nx, x[0] if x[0] else 1.0)
        v = x[:]
        v[0] -= alpha
        beta = 2.0 / sum(z * z for z in v)
        # A <- H A: rows k+1:n, all columns.
        for j in range(k, n):
            tau = beta * sum(v[i-k-1] * a[i][j] for i in range(k+1, n))
            for i in range(k+1, n):
                a[i][j] -= tau * v[i-k-1]
        # A <- A H: all rows, columns k+1:n.
        for i in range(n):
            tau = beta * sum(a[i][j] * v[j-k-1] for j in range(k+1, n))
            for j in range(k+1, n):
                a[i][j] -= tau * v[j-k-1]
        # Q <- Q H.
        for i in range(n):
            tau = beta * sum(q[i][j] * v[j-k-1] for j in range(k+1, n))
            for j in range(k+1, n):
                q[i][j] -= tau * v[j-k-1]
        for i in range(k+2, n):
            a[i][k] = 0.0
    return q, a


def shifted_qr_curve(a0, mode, steps=80):
    a = [row[:] for row in a0]
    n = len(a)
    out = []
    for k in range(steps + 1):
        out.append((k, max(abs(a[n-1][n-2]), 1e-18)))
        if abs(a[n-1][n-2]) < 1e-15:
            # Retain the floor for visual comparison after deflation.
            continue
        if mode == "unshifted":
            mu = 0.0
        elif mode == "rayleigh":
            mu = a[n-1][n-1]
        else:
            aa, bb, dd = a[n-2][n-2], a[n-2][n-1], a[n-1][n-1]
            delta = (aa - dd) / 2.0
            sign = 1.0 if delta >= 0.0 else -1.0
            mu = dd - sign * bb * bb / (abs(delta) + math.hypot(delta, bb))
        shifted = [[a[i][j] - (mu if i == j else 0.0) for j in range(n)] for i in range(n)]
        q, r = householder_qr(shifted)
        a = matmul(r, q)
        for i in range(n):
            a[i][i] += mu
        # The input is symmetric tridiagonal; enforce its invariant structure
        # only at roundoff level so the experiment studies convergence, not fill.
        for i in range(n):
            for j in range(i+1, n):
                v = 0.5 * (a[i][j] + a[j][i])
                a[i][j] = a[j][i] = v
        for i in range(n):
            for j in range(n):
                if abs(i-j) > 1 and abs(a[i][j]) < 1e-12:
                    a[i][j] = 0.0
        if abs(a[n-1][n-2]) <= 1e-14 * (abs(a[n-2][n-2]) + abs(a[n-1][n-1])):
            a[n-1][n-2] = a[n-2][n-1] = 0.0
    return out


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def logmap(v, lo, hi, a, b):
    v = max(lo, min(hi, v))
    return a + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (b - a)


def axes(x0,y0,w,h,xticks,yticks,xlabel,ylabel,xlog=False,ylog=True):
    out=[f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo,xhi=xticks[0][0],xticks[-1][0]; ylo,yhi=yticks[0][0],yticks[-1][0]
    for v,lab in xticks:
        x=logmap(v,xlo,xhi,x0,x0+w) if xlog else x0+(v-xlo)/(xhi-xlo)*w
        out += [f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>',f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(lab)}</text>']
    for v,lab in yticks:
        y=y0+h-(logmap(v,ylo,yhi,0,h) if ylog else (v-ylo)/(yhi-ylo)*h)
        out += [f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>',f'<text x="{x0-10}" y="{y+4:.2f}" text-anchor="end">{esc(lab)}</text>']
    out += [f'<text x="{x0+w/2}" y="{y0+h+46}" text-anchor="middle" class="axis">{esc(xlabel)}</text>',f'<text x="{x0-54}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-54} {y0+h/2})">{esc(ylabel)}</text>']
    return out


def poly(points,color,dash=""):
    ds=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x,y,color,shape="circle"):
    if shape=="square": return f'<rect x="{x-3:.2f}" y="{y-3:.2f}" width="6" height="6" fill="{color}"/>'
    if shape=="diamond": return f'<path d="M{x:.2f},{y-4:.2f} L{x+4:.2f},{y:.2f} L{x:.2f},{y+4:.2f} L{x-4:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.3" fill="{color}"/>'


def heatmap(svg,a,x0,y0,size,title):
    n=len(a); cell=size/n; scale=max(abs(v) for row in a for v in row)
    svg.append(f'<text x="{x0+size/2}" y="{y0-10}" text-anchor="middle" class="note">{title}</text>')
    for i in range(n):
        for j in range(n):
            mag=abs(a[i][j])/scale if scale else 0.0
            opacity=0.08+0.86*math.sqrt(mag) if mag>1e-15 else 0.0
            fill="#2f6fbd" if mag>1e-15 else "#ffffff"
            svg.append(f'<rect x="{x0+j*cell:.2f}" y="{y0+i*cell:.2f}" width="{cell:.2f}" height="{cell:.2f}" fill="{fill}" fill-opacity="{opacity:.3f}" stroke="#dbe1e8" stroke-width="0.8"/>')


def main():
    n=6
    dense=[[math.sin((i+1)*(j+2))+0.17*(i-j)+0.3*(1 if i==j else 0) for j in range(n)] for i in range(n)]
    q,hess=hessenberg(dense)
    sim=matmul(transpose(q),matmul(dense,q))
    simerr=frob(sub(sim,hess))/frob(dense)
    orth=frob(sub(matmul(transpose(q),q),eye(n)))

    tri=[[0.0]*4 for _ in range(4)]
    diag=[4.0,3.0,2.0,1.0]; off=[0.8,0.6,0.4]
    for i,v in enumerate(diag): tri[i][i]=v
    for i,v in enumerate(off): tri[i][i+1]=tri[i+1][i]=v
    curves={m:shifted_qr_curve(tri,m) for m in ("unshifted","rayleigh","wilkinson")}

    sizes=[16,32,64,128,256,512]
    costs=[(n,float(n**3),float(6*n*n)) for n in sizes]

    below_band=max(abs(hess[i][j]) for i in range(n) for j in range(n) if i>j+1)
    deflation_1e8={mode:next(k for k,e in curve if e<1e-8) for mode,curve in curves.items()}
    assert simerr < 1e-12 and orth < 1e-12 and below_band < 1e-12
    assert deflation_1e8["wilkinson"] <= deflation_1e8["rayleigh"] < deflation_1e8["unshifted"]
    assert costs[-1][1] / costs[-1][2] > 50.0

    W,H=1440,610
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
         '<title id="title">Hessenberg reduction and shifted QR convergence</title>',
         '<desc id="desc">The first panel shows dense-to-Hessenberg structure preservation, the second compares unshifted, Rayleigh, and Wilkinson-shifted QR deflation, and the third contrasts cubic and quadratic work scaling.</desc>',
         '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;font-size:15px;fill:#1f2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#fffefb;stroke:#d7dee8;stroke-width:1}.grid{stroke:#e2e8f0;stroke-width:1}.note{font-size:15px;fill:#64748b}.legend{font-size:15px}</style>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="720" y="34" text-anchor="middle" class="title">Hessenberg 先约化，移位 QR 再迭代</text>']
    # A heatmaps
    svg.append('<text x="70" y="67" class="panel">A  正交相似保持谱，只压缩带宽</text>')
    heatmap(svg,dense,105,130,145,"原始稠密 A")
    svg.append('<text x="285" y="205" text-anchor="middle" class="panel">→</text>')
    heatmap(svg,hess,325,130,145,"H=QᵀAQ")
    svg.append(f'<text x="90" y="315" class="note">相似残差：{simerr:.2e}</text>')
    svg.append(f'<text x="90" y="340" class="note">正交缺陷：{orth:.2e}</text>')
    svg.append('<text x="90" y="380" class="note">蓝色深浅表示 |aᵢⱼ|；第二条次对角线以下为零。</text>')
    svg.append('<text x="90" y="405" class="note">对称矩阵会进一步约化成三对角矩阵。</text>')

    # B convergence
    x1,y1,w1,h1=570,88,330,330
    svg.append('<text x="570" y="67" class="panel">B  移位控制 deflation 速度</text>')
    svg += axes(x1,y1,w1,h1,[(0,"0"),(20,"20"),(40,"40"),(60,"60"),(80,"80")],[(1e-16,"10⁻¹⁶"),(1e-12,"10⁻¹²"),(1e-8,"10⁻⁸"),(1e-4,"10⁻⁴"),(1.0,"1")],"QR 步数 k","末端次对角元 |hₙ,ₙ₋₁|")
    colors={"unshifted":"#c43d3d","rayleigh":"#2f6fbd","wilkinson":"#248a57"}; shapes={"unshifted":"square","rayleigh":"circle","wilkinson":"diamond"}
    for mode,curve in curves.items():
        pts=[]
        for k,e in curve:
            x=x1+k/80*w1; y=y1+h1-logmap(max(e,1e-16),1e-16,1,0,h1); pts.append((x,y))
        svg.append(poly(pts,colors[mode],"7 4" if mode=="unshifted" else ""))
        for x,y in pts[::5]: svg.append(mark(x,y,colors[mode],shapes[mode]))
    svg.append('<text x="585" y="112" class="note">Wilkinson shift 选尾部 2×2 特征值中更近者</text>')

    # C cost
    x2,y2,w2,h2=1030,88,330,330
    svg.append('<text x="1030" y="67" class="panel">C  结构把每步从 O(n³) 降到 O(n²)</text>')
    svg += axes(x2,y2,w2,h2,[(16,"16"),(32,"32"),(64,"64"),(128,"128"),(256,"256"),(512,"512")],[(1e3,"10³"),(1e5,"10⁵"),(1e7,"10⁷"),(1e9,"10⁹")],"矩阵阶数 n（对数）","工作量代理（对数）",xlog=True,ylog=True)
    densepts=[]; hpts=[]
    for n,dc,hc in costs:
        x=logmap(n,16,512,x2,x2+w2); yd=y2+h2-logmap(dc,1e3,1e9,0,h2); yh=y2+h2-logmap(hc,1e3,1e9,0,h2)
        densepts.append((x,yd)); hpts.append((x,yh)); svg.append(mark(x,yd,"#c43d3d","square")); svg.append(mark(x,yh,"#248a57","diamond"))
    svg.append(poly(densepts,"#c43d3d")); svg.append(poly(hpts,"#248a57"))
    svg.append('<text x="1045" y="112" class="note">代理：稠密 n³；Hessenberg 隐式 QR 约 6n²</text>')

    # legends/footer
    legends=[("unshifted","无移位"),("rayleigh","Rayleigh shift"),("wilkinson","Wilkinson shift")]
    for i,(m,label) in enumerate(legends):
        x=575+i*120; svg.append(mark(x,500,colors[m],shapes[m])); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append(mark(1050,500,"#c43d3d","square")); svg.append('<text x="1060" y="504" class="legend">稠密 QR 步</text>')
    svg.append(mark(1175,500,"#248a57","diamond")); svg.append('<text x="1185" y="504" class="legend">Hessenberg 隐式步</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">显式教学实现用于展示不变量与收敛；生产 eigensolver 还需要平衡、多重移位、aggressive early deflation 与异常退出处理。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_hessenberg_qr.py · Python 标准库 · seed=无随机性</text>')
    svg.append('</svg>')
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text("\n".join(svg),encoding="utf-8")
    print(f"saved={OUT}")
    print(f"hessenberg:similarity_residual={simerr:.3e},orthogonality={orth:.3e}")
    print("qr:mode,step_to_1e-8,step_to_deflation,final_subdiag")
    for mode,curve in curves.items():
        k8=next((k for k,e in curve if e<1e-8),None); kd=next((k for k,e in curve if e<=1e-15),None)
        print(f"{mode},{k8},{kd},{curve[-1][1]:.3e}")
    print("cost:n,dense_proxy,hessenberg_proxy")
    for row in costs: print(f"{row[0]},{row[1]:.0f},{row[2]:.0f}")


if __name__=="__main__":
    main()
