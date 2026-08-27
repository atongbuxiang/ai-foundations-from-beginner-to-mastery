#!/usr/bin/env python3
"""Deterministic Arnoldi experiment: Ritz residuals, orthogonality and restart."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "arnoldi" / "plot-arnoldi-restart-nonnormal-v2.svg"


def dot(x, y): return sum(a*b for a, b in zip(x, y))
def norm(x): return math.sqrt(dot(x, x))
def normalize(x):
    n = norm(x)
    return [v/n for v in x]


def matvec(a, x): return [dot(row, x) for row in a]


def quant(x, digits): return [round(v, digits) for v in x] if digits is not None else x


def make_nonnormal(n):
    a = [[0.0]*n for _ in range(n)]
    for i in range(n):
        if i == 0:
            a[i][i] = 5.0
        elif i == 1:
            a[i][i] = 3.0
        else:
            a[i][i] = 2.5 - 2.0*(i-2)/(n-3)
        if i+1 < n: a[i][i+1] = 0.90
        if i+2 < n: a[i][i+2] = 0.20
    return a


def arnoldi(a, v1, steps, passes=2, digits=None):
    n = len(a)
    v = [normalize(v1)]
    h = [[0.0]*steps for _ in range(steps+1)]
    for j in range(steps):
        w = matvec(a, v[j])
        for _ in range(passes):
            for i in range(j+1):
                c = dot(v[i], w)
                h[i][j] += c
                w = [x-c*y for x, y in zip(w, v[i])]
                w = quant(w, digits)
        h[j+1][j] = norm(w)
        if h[j+1][j] < 1e-14:
            return v, h, j+1
        q = normalize(w)
        if digits is not None: q = normalize(quant(q, digits))
        v.append(q)
    return v, h, steps


def h_square(h, k): return [[h[i][j] for j in range(k)] for i in range(k)]


def dominant_pair(h, iterations=1200):
    n = len(h)
    y = normalize([1.0+0.1*i for i in range(n)])
    for _ in range(iterations):
        z = matvec(h, y)
        nz = norm(z)
        if nz == 0: break
        yn = [v/nz for v in z]
        if norm([a-b for a,b in zip(yn,y)]) < 1e-15 or norm([a+b for a,b in zip(yn,y)]) < 1e-15:
            y = yn; break
        y = yn
    hy = matvec(h, y)
    theta = dot(y, hy)/dot(y, y)
    return theta, y


def ritz(a, start, k, passes=2, digits=None):
    v, h, actual = arnoldi(a, start, k, passes=passes, digits=digits)
    k = actual
    theta, y = dominant_pair(h_square(h, k))
    x = [sum(v[j][i]*y[j] for j in range(k)) for i in range(len(a))]
    direct = norm([p-theta*q for p,q in zip(matvec(a,x),x)])
    cheap = abs(h[k][k-1]*y[-1]) if len(v) > k else direct
    return theta, x, direct, cheap, v, h, k


def orth_defect(v, k):
    q = v[:k]
    return max(abs(dot(q[i],q[j])-(1.0 if i==j else 0.0)) for i in range(k) for j in range(k))


def restart_curve(a, start, width, cycles):
    q = normalize(start)
    rows=[]
    for c in range(1,cycles+1):
        theta,x,direct,_,_,_,_ = ritz(a,q,width,passes=2)
        q=normalize(x)
        rows.append((c*width,max(direct,1e-16),theta))
    return rows


def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def logmap(v,lo,hi,a,b):
    v=max(lo,min(hi,v)); return a+(math.log10(v)-math.log10(lo))/(math.log10(hi)-math.log10(lo))*(b-a)


def axes(x0,y0,w,h,xticks,yticks,xlabel,ylabel,ylog=True):
    out=[f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo,xhi=xticks[0][0],xticks[-1][0]; ylo,yhi=yticks[0][0],yticks[-1][0]
    for val,label in xticks:
        x=x0+(val-xlo)/(xhi-xlo)*w
        out += [f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>',f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>']
    for val,label in yticks:
        frac=logmap(val,ylo,yhi,0,h) if ylog else (val-ylo)/(yhi-ylo)*h; y=y0+h-frac
        out += [f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>',f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>']
    out += [f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>',f'<text x="{x0-55}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-55} {y0+h/2})">{esc(ylabel)}</text>']
    return out


def poly(pts,color,dash=''):
    ds=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'


def mark(x,y,color,shape='circle'):
    if shape=='square': return f'<rect x="{x-3:.2f}" y="{y-3:.2f}" width="6" height="6" fill="{color}"/>'
    if shape=='diamond': return f'<path d="M{x:.2f},{y-4:.2f} L{x+4:.2f},{y:.2f} L{x:.2f},{y+4:.2f} L{x-4:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="{color}"/>'


def main():
    n=32; a=make_nonnormal(n); start=[math.sin(.43*(i+1))+.4*math.cos(.19*(i+1)) for i in range(n)]
    conv=[]
    for k in range(2,25):
        theta,_,direct,cheap,_,_,_=ritz(a,start,k,passes=2)
        conv.append((k,max(abs(theta-5.0),1e-16),max(direct,1e-16),max(cheap,1e-16)))

    orth=[]
    for k in range(2,25):
        v1,_,a1=arnoldi(a,start,k,passes=1,digits=9)
        v2,_,a2=arnoldi(a,start,k,passes=2,digits=9)
        orth.append((k,max(orth_defect(v1,a1),1e-16),max(orth_defect(v2,a2),1e-16)))

    full=[]
    for k in range(2,31):
        _,_,res,_,_,_,_=ritz(a,start,k,passes=2)
        full.append((k,max(res,1e-16)))
    restarted=restart_curve(a,start,6,5)

    W,H=1440,610
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
         '<title id="title">Arnoldi projection, orthogonality and restart tradeoff</title>',
         '<desc id="desc">The panels show Ritz error and residual, one-pass versus two-pass Arnoldi orthogonality, and full versus restarted Arnoldi convergence.</desc>',
         '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="720" y="34" text-anchor="middle" class="title">Arnoldi：一般矩阵需要长正交化，重启则用信息换内存</text>']
    for x,t in [(75,'A  Ritz 值误差与残差不是同一量'),(555,'B  两遍正交化控制基缺陷'),(1035,'C  重启限制内存，也会丢掉多项式历史')]: svg.append(f'<text x="{x}" y="67" class="panel">{t}</text>')
    colors=['#2f6fbd','#c36a14','#248a57','#8a4fb8','#c43d3d']
    y0,w,h=88,330,330
    x0=75
    svg += axes(x0,y0,w,h,[(2,'2'),(7,'7'),(13,'13'),(19,'19'),(24,'24')],[(1e-16,'10⁻¹⁶'),(1e-12,'10⁻¹²'),(1e-8,'10⁻⁸'),(1e-4,'10⁻⁴'),(1,'1')],'Arnoldi 维数 k','误差 / 残差')
    for idx,color,shape in [(1,colors[0],'circle'),(2,colors[1],'square'),(3,colors[2],'diamond')]:
        pts=[]
        for row in conv:
            x=x0+(row[0]-2)/22*w; y=y0+h-logmap(row[idx],1e-16,1,0,h); pts.append((x,y))
        svg.append(poly(pts,color,'6 4' if idx==3 else ''))
        for x,y in pts[::4]: svg.append(mark(x,y,color,shape))
    svg.append('<text x="90" y="112" class="note">A 为实上三角非正规矩阵；目标 λ=5</text>')

    x1=555
    svg += axes(x1,y0,w,h,[(2,'2'),(7,'7'),(13,'13'),(19,'19'),(24,'24')],[(1e-16,'10⁻¹⁶'),(1e-12,'10⁻¹²'),(1e-8,'10⁻⁸'),(1e-4,'10⁻⁴'),(1,'1')],'Arnoldi 维数 k','max |vᵢᵀvⱼ−δᵢⱼ|')
    for idx,color,shape in [(1,colors[4],'square'),(2,colors[2],'diamond')]:
        pts=[]
        for row in orth:
            x=x1+(row[0]-2)/22*w; y=y0+h-logmap(row[idx],1e-16,1,0,h); pts.append((x,y))
        svg.append(poly(pts,color))
        for x,y in pts[::4]: svg.append(mark(x,y,color,shape))
    svg.append('<text x="570" y="112" class="note">模拟 9 位运算；第二遍 MGS 清除回流分量</text>')

    x2=1035
    svg += axes(x2,y0,w,h,[(2,'2'),(9,'9'),(16,'16'),(23,'23'),(30,'30')],[(1e-16,'10⁻¹⁶'),(1e-12,'10⁻¹²'),(1e-8,'10⁻⁸'),(1e-4,'10⁻⁴'),(1,'1')],'累计矩阵—向量乘','主 Ritz 对残差')
    pts=[]
    for k,res in full:
        x=x2+(k-2)/28*w; y=y0+h-logmap(res,1e-16,1,0,h); pts.append((x,y))
    svg.append(poly(pts,colors[0]));
    for x,y in pts[::4]: svg.append(mark(x,y,colors[0],'circle'))
    pts=[]
    for k,res,_ in restarted:
        x=x2+(k-2)/28*w; y=y0+h-logmap(res,1e-16,1,0,h); pts.append((x,y))
    svg.append(poly(pts,colors[3],'7 4'))
    for x,y in pts: svg.append(mark(x,y,colors[3],'square'))
    svg.append('<text x="1050" y="112" class="note">重启宽度 m=6；每轮只保留一个 Ritz 向量</text>')

    legends=[(90,colors[0],'circle','|θ−5|'),(195,colors[1],'square','直接残差'),(315,colors[2],'diamond','廉价残差'),
             (575,colors[4],'square','一遍 MGS'),(715,colors[2],'diamond','两遍 MGS'),(1055,colors[0],'circle','不重启'),(1190,colors[3],'square','每 6 步重启')]
    for x,c,s,l in legends: svg.append(mark(x,500,c,s)); svg.append(f'<text x="{x+10}" y="504" class="legend">{l}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">矩阵特征值虽为实对角元，严格上三角耦合使其非正规；小残差仍需结合谱条件性解释前向误差。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_arnoldi_restart_nonnormal.py · Python 标准库 · 无随机性</text>')
    svg.append('</svg>')
    if conv[-1][1] >= 1e-10 or abs(conv[-1][2] - conv[-1][3]) >= 1e-12:
        raise RuntimeError("Arnoldi Ritz/residual identity audit failed")
    if orth[-1][1] <= 10.0 * orth[-1][2]:
        raise RuntimeError("one-pass/two-pass orthogonalization separation audit failed")
    if restarted[-1][1] >= 1e-8:
        raise RuntimeError("restarted Arnoldi convergence audit failed")
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text('\n'.join(svg),encoding='utf-8')
    print(f'saved={OUT}')
    for k in (5,10,15,20,24):
        row=conv[k-2]; print(f'ritz:k={k},eigerr={row[1]:.3e},direct={row[2]:.3e},cheap={row[3]:.3e}')
    for k in (5,10,15,20,24):
        row=orth[k-2]; print(f'orth:k={k},one={row[1]:.3e},two={row[2]:.3e}')
    for row in restarted: print(f'restart:matvec={row[0]},res={row[1]:.3e},theta={row[2]:.8f}')


if __name__=='__main__': main()
