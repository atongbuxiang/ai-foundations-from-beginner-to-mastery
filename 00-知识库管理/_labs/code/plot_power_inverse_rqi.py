#!/usr/bin/env python3
"""Deterministic convergence experiment for power, inverse, and RQI methods."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "power-iteration" / "plot-power-inverse-rqi-v2.svg"


def norm(x):
    return math.hypot(*x)


def normalize(x):
    n = norm(x)
    return [v / n for v in x]


def rayleigh(diag, x):
    return sum(lam * z * z for lam, z in zip(diag, x)) / sum(z * z for z in x)


def eig_residual(diag, x):
    mu = rayleigh(diag, x)
    return norm([(lam - mu) * z for lam, z in zip(diag, x)])


def power_curve(ratio, steps=40):
    diag = [1.0, ratio]
    x = normalize([1.0, 1.0])
    out = []
    for k in range(steps + 1):
        out.append((k, abs(x[1])))
        x = normalize([diag[i] * x[i] for i in range(2)])
    return out


def inverse_curve(shift, steps=12):
    diag = [5.0, 2.0, 1.0]
    x = normalize([0.2, 1.0, 0.4])
    out = []
    for k in range(steps + 1):
        out.append((k, max(eig_residual(diag, x), 1e-18)))
        y = [x[i] / (diag[i] - shift) for i in range(3)]
        x = normalize(y)
    return out


def rqi_step_2d(theta):
    # A=diag(1,3), target q=e2.  theta is the angle away from e2.
    x = [math.sin(theta), math.cos(theta)]
    mu = rayleigh([1.0, 3.0], x)
    y = [x[0] / (1.0 - mu), x[1] / (3.0 - mu)]
    z = normalize(y)
    return math.asin(min(1.0, abs(z[0])))


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def logmap(v, lo, hi, a, b):
    v = max(lo, min(hi, v))
    return a + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (b - a)


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel, xlog=False, ylog=True):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo, xhi = xticks[0][0], xticks[-1][0]
    ylo, yhi = yticks[0][0], yticks[-1][0]
    for val, lab in xticks:
        x = logmap(val, xlo, xhi, x0, x0+w) if xlog else x0 + (val-xlo)/(xhi-xlo)*w
        out.append(f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>')
        out.append(f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(lab)}</text>')
    for val, lab in yticks:
        y = y0+h-(logmap(val,ylo,yhi,0,h) if ylog else (val-ylo)/(yhi-ylo)*h)
        out.append(f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>')
        out.append(f'<text x="{x0-10}" y="{y+4:.2f}" text-anchor="end">{esc(lab)}</text>')
    out.append(f'<text x="{x0+w/2}" y="{y0+h+46}" text-anchor="middle" class="axis">{esc(xlabel)}</text>')
    out.append(f'<text x="{x0-55}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-55} {y0+h/2})">{esc(ylabel)}</text>')
    return out


def poly(points, color, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ps = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{ps}" fill="none" stroke="{color}" stroke-width="2.5"{d}/>'


def mark(x, y, color, shape="circle"):
    if shape == "square":
        return f'<rect x="{x-3:.2f}" y="{y-3:.2f}" width="6" height="6" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-4:.2f} L{x+4:.2f},{y:.2f} L{x:.2f},{y+4:.2f} L{x-4:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.3" fill="{color}"/>'


def main():
    power = {r: power_curve(r) for r in (0.2, 0.8, 0.98)}
    inverse = {s: inverse_curve(s) for s in (1.5, 1.9, 1.99)}
    angles = [10.0 ** (-z / 4) for z in range(1, 17)]
    cubic = [(theta, rqi_step_2d(theta)) for theta in angles]

    assert power[0.2][10][1] < power[0.8][10][1] < power[0.98][10][1]
    assert inverse[1.99][5][1] < inverse[1.9][5][1] < inverse[1.5][5][1]
    cubic_ratios = [next_angle / angle**3 for angle, next_angle in cubic if angle <= 0.1]
    assert max(abs(ratio - 1.0) for ratio in cubic_ratios) < 0.02

    W, H = 1440, 610
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">Power, inverse, and Rayleigh quotient iteration convergence</title>',
        '<desc id="desc">Power convergence slows as the spectral ratio approaches one, inverse iteration accelerates as the shift approaches the target eigenvalue, and symmetric Rayleigh quotient iteration follows a cubic local error law.</desc>',
        '<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;font-size:15px;fill:#1f2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#fffefb;stroke:#d7dee8;stroke-width:1}.grid{stroke:#e2e8f0;stroke-width:1}.note{font-size:15px;fill:#64748b}.legend{font-size:15px}</style>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        '<text x="720" y="34" text-anchor="middle" class="title">谱间隙与移位决定收敛速度</text>',
    ]

    colors = ["#2f6fbd", "#e08a28", "#248a57"]
    shapes = ["circle", "square", "diamond"]

    # A: power
    x0,y0,w,h=78,88,365,330
    svg.append('<text x="78" y="67" class="panel">A  幂法：谱比接近 1 时变慢</text>')
    svg += axes(x0,y0,w,h,[(0,"0"),(10,"10"),(20,"20"),(30,"30"),(40,"40")],
                [(1e-16,"10⁻¹⁶"),(1e-12,"10⁻¹²"),(1e-8,"10⁻⁸"),(1e-4,"10⁻⁴"),(1.0,"1")],
                "迭代次数 k", "sin∠(xₖ,q₁)")
    for idx,(ratio,curve) in enumerate(power.items()):
        pts=[]
        for k,e in curve:
            x=x0+k/40*w; y=y0+h-logmap(max(e,1e-16),1e-16,1,0,h); pts.append((x,y))
        svg.append(poly(pts,colors[idx],"7 4" if idx==2 else ""))
        for x,y in pts[::5]: svg.append(mark(x,y,colors[idx],shapes[idx]))
    svg.append('<text x="93" y="112" class="note">理论斜率由 |λ₂/λ₁|ᵏ 控制</text>')

    # B: inverse
    x1,y1,w1,h1=555,88,330,330
    svg.append('<text x="555" y="67" class="panel">B  反幂法：移位越接近目标越快</text>')
    svg += axes(x1,y1,w1,h1,[(0,"0"),(3,"3"),(6,"6"),(9,"9"),(12,"12")],
                [(1e-16,"10⁻¹⁶"),(1e-12,"10⁻¹²"),(1e-8,"10⁻⁸"),(1e-4,"10⁻⁴"),(1.0,"1")],
                "迭代次数 k", "||Axₖ−ρₖxₖ||₂")
    for idx,(shift,curve) in enumerate(inverse.items()):
        pts=[]
        for k,e in curve:
            x=x1+k/12*w1; y=y1+h1-logmap(max(e,1e-16),1e-16,1,0,h1); pts.append((x,y))
        svg.append(poly(pts,colors[idx]))
        for x,y in pts: svg.append(mark(x,y,colors[idx],shapes[idx]))
    svg.append('<text x="570" y="112" class="note">目标 λ=2；每步求解 (A−σI)y=x，不形成逆矩阵</text>')

    # C: cubic local law
    x2,y2,w2,h2=1010,88,350,330
    svg.append('<text x="1010" y="67" class="panel">C  对称 RQI：局部三次收敛</text>')
    svg += axes(x2,y2,w2,h2,[(1e-4,"10⁻⁴"),(1e-3,"10⁻³"),(1e-2,"10⁻²"),(1e-1,"10⁻¹"),(1.0,"1")],
                [(1e-12,"10⁻¹²"),(1e-9,"10⁻⁹"),(1e-6,"10⁻⁶"),(1e-3,"10⁻³"),(1.0,"1")],
                "当前角误差 e_k", "下一步角误差 e_next",xlog=True,ylog=True)
    pts=[]
    for e,enext in cubic:
        x=logmap(e,1e-4,1,x2,x2+w2); y=y2+h2-logmap(max(enext,1e-12),1e-12,1,0,h2)
        pts.append((x,y)); svg.append(mark(x,y,"#6a55a3","diamond"))
    svg.append(poly(pts,"#6a55a3"))
    ref=[]
    for e in [1e-4,1e-3,1e-2,1e-1,1.0]:
        x=logmap(e,1e-4,1,x2,x2+w2); y=y2+h2-logmap(max(e**3,1e-12),1e-12,1,0,h2); ref.append((x,y))
    svg.append(poly(ref,"#555f70","6 5"))
    svg.append('<text x="1025" y="112" class="note">A=diag(1,3)；虚线为 e_next=(e_k)^3</text>')

    # Legends
    for i,(ratio,color,shape) in enumerate(zip((0.2,0.8,0.98),colors,shapes)):
        x=92+i*125; svg.append(mark(x,500,color,shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">|λ₂/λ₁|={ratio}</text>')
    for i,(shift,color,shape) in enumerate(zip((1.5,1.9,1.99),colors,shapes)):
        x=570+i*105; svg.append(mark(x,500,color,shape)); svg.append(f'<text x="{x+10}" y="504" class="legend">σ={shift}</text>')
    svg.append(mark(1030,500,"#6a55a3","diamond")); svg.append('<text x="1040" y="504" class="legend">实际 RQI</text>')
    svg.append('<line x1="1145" y1="500" x2="1180" y2="500" stroke="#555f70" stroke-width="2" stroke-dasharray="6 5"/><text x="1188" y="504" class="legend">三次参考线</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">对角矩阵用于隔离收敛因子；一般非正规矩阵还会受特征向量条件数与瞬态放大影响。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_power_inverse_rqi.py · Python 标准库 · seed=无随机性</text>')
    svg.append('</svg>')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text("\n".join(svg),encoding="utf-8")
    print(f"saved={OUT}")
    print("power:ratio,error_k10,error_k20,error_k40")
    for ratio,curve in power.items():
        d=dict(curve); print(f"{ratio},{d[10]:.3e},{d[20]:.3e},{d[40]:.3e}")
    print("inverse:shift,residual_k2,residual_k5,residual_k10")
    for shift,curve in inverse.items():
        d=dict(curve); print(f"{shift},{d[2]:.3e},{d[5]:.3e},{d[10]:.3e}")
    print("rqi:angle,next_angle,next_over_cube")
    for e,enext in cubic[::4]:
        print(f"{e:.3e},{enext:.3e},{enext/e**3:.3e}")


if __name__ == "__main__":
    main()
