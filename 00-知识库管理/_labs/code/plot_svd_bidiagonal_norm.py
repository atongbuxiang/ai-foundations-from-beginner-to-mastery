#!/usr/bin/env python3
"""Deterministic SVD experiment: bidiagonalization, norm estimation and randomized range."""

from __future__ import annotations

import math
import random
from pathlib import Path


ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_assets'/'plots'/'svd-algorithms'/'plot-svd-bidiagonal-norm-v2.svg'


def dot(x,y): return sum(a*b for a,b in zip(x,y))
def norm(x): return math.sqrt(dot(x,x))
def normalize(x):
    n=norm(x); return [v/n for v in x]
def eye(n): return [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
def transpose(a): return [list(row) for row in zip(*a)]
def matmul(a,b):
    bt=transpose(b); return [[dot(row,col) for col in bt] for row in a]
def frob(a): return math.sqrt(sum(v*v for row in a for v in row))
def sub(a,b): return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def reflector(x):
    nx=norm(x)
    if nx==0.0: return [0.0]*len(x),0.0
    alpha=-math.copysign(nx,x[0] if x[0] else 1.0)
    v=x[:]; v[0]-=alpha
    return v,2.0/dot(v,v)


def bidiagonalize(a0):
    a=[row[:] for row in a0]; m,n=len(a),len(a[0]); u=eye(m); vmat=eye(n)
    for k in range(min(m,n)):
        vl,beta=reflector([a[i][k] for i in range(k,m)])
        if beta:
            for j in range(k,n):
                tau=beta*sum(vl[i-k]*a[i][j] for i in range(k,m))
                for i in range(k,m): a[i][j]-=tau*vl[i-k]
            for i in range(m):
                tau=beta*sum(u[i][j]*vl[j-k] for j in range(k,m))
                for j in range(k,m): u[i][j]-=tau*vl[j-k]
        if k+1<n:
            vr,beta=reflector([a[k][j] for j in range(k+1,n)])
            if beta:
                for i in range(m):
                    tau=beta*sum(a[i][j]*vr[j-k-1] for j in range(k+1,n))
                    for j in range(k+1,n): a[i][j]-=tau*vr[j-k-1]
                for i in range(n):
                    tau=beta*sum(vmat[i][j]*vr[j-k-1] for j in range(k+1,n))
                    for j in range(k+1,n): vmat[i][j]-=tau*vr[j-k-1]
        for i in range(m):
            for j in range(n):
                if i>j or j>i+1:
                    if abs(a[i][j])<1e-12: a[i][j]=0.0
    return u,a,vmat


def qr_columns(cols):
    q=[]
    for col in cols:
        z=col[:]
        for _ in range(2):
            for qi in q:
                c=dot(qi,z); z=[a-c*b for a,b in zip(z,qi)]
        nz=norm(z)
        if nz>1e-13: q.append([v/nz for v in z])
    return q


def projection(cols,x):
    y=[0.0]*len(x)
    for q in cols:
        c=dot(q,x)
        y=[a+c*b for a,b in zip(y,q)]
    return y


def residual_spectral_norm(s,qcols,iters=100):
    n=len(s); x=normalize([math.sin(.61*(i+1))+.2 for i in range(n)])
    est=0.0
    for _ in range(iters):
        ax=[s[i]*x[i] for i in range(n)]
        p=projection(qcols,ax); y=[a-b for a,b in zip(ax,p)]
        z=[s[i]*y[i] for i in range(n)]
        nz=norm(z)
        if nz==0: return 0.0
        x=[v/nz for v in z]
        est=math.sqrt(max(dot(x,z),0.0))
    ax=[s[i]*x[i] for i in range(n)]; p=projection(qcols,ax)
    return norm([a-b for a,b in zip(ax,p)])


def randomized_range_errors(s,k,ps,qs,seed=20260815):
    n=len(s); max_l=k+max(ps); rng=random.Random(seed)
    omega=[[rng.gauss(0,1) for _ in range(max_l)] for _ in range(n)]
    rows=[]
    for power in qs:
        for p in ps:
            l=k+p
            cols=[[s[i]*omega[i][j] for i in range(n)] for j in range(l)]
            qcols=qr_columns(cols)
            for _ in range(power):
                cols=[[s[i]*q[i] for i in range(n)] for q in qcols]
                qcols=qr_columns(cols)
                cols=[[s[i]*q[i] for i in range(n)] for q in qcols]
                qcols=qr_columns(cols)
            err=residual_spectral_norm(s,qcols)
            # Q has l=k+p columns here, so compare its range residual with
            # the optimal rank-l spectral error sigma_{l+1}.
            rows.append((power,p,err,err/s[k+p]))
    return rows


def power_norm_curve(r,steps=30):
    s=[1.0,r,0.5*r,0.2*r]
    x=normalize([.4,.7,.2,.55]); out=[]
    for k in range(1,steps+1):
        ata=[s[i]*s[i]*x[i] for i in range(len(s))]
        x=normalize(ata)
        est=math.sqrt(sum((s[i]*x[i])**2 for i in range(len(s))))
        out.append((k,max(1.0-est,1e-16)))
    return out


def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def logmap(v,lo,hi,a,b):
    v=max(lo,min(hi,v)); return a+(math.log10(v)-math.log10(lo))/(math.log10(hi)-math.log10(lo))*(b-a)
def axes(x0,y0,w,h,xticks,yticks,xlabel,ylabel,ylog=True):
    out=[f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']; xlo,xhi=xticks[0][0],xticks[-1][0]; ylo,yhi=yticks[0][0],yticks[-1][0]
    for val,label in xticks:
        x=x0+(val-xlo)/(xhi-xlo)*w; out += [f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>',f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>']
    for val,label in yticks:
        frac=logmap(val,ylo,yhi,0,h) if ylog else (val-ylo)/(yhi-ylo)*h; y=y0+h-frac; out += [f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>',f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>']
    out += [f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>',f'<text x="{x0-55}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-55} {y0+h/2})">{esc(ylabel)}</text>']; return out
def poly(pts,color,dash=''):
    ds=f' stroke-dasharray="{dash}"' if dash else ''; return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="2.5"{ds}/>'
def mark(x,y,color,shape='circle'):
    if shape=='square': return f'<rect x="{x-3:.2f}" y="{y-3:.2f}" width="6" height="6" fill="{color}"/>'
    if shape=='diamond': return f'<path d="M{x:.2f},{y-4:.2f} L{x+4:.2f},{y:.2f} L{x:.2f},{y+4:.2f} L{x-4:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="{color}"/>'


def heatmap(svg,a,x0,y0,w,h,title):
    m,n=len(a),len(a[0]); cw,ch=w/n,h/m; scale=max(abs(v) for row in a for v in row)
    svg.append(f'<text x="{x0+w/2}" y="{y0-10}" text-anchor="middle" class="note">{title}</text>')
    for i in range(m):
        for j in range(n):
            mag=abs(a[i][j])/scale if scale else 0; opacity=0.08+0.86*math.sqrt(mag) if mag>1e-15 else 0; fill='#2f6fbd' if mag>1e-15 else '#ffffff'
            svg.append(f'<rect x="{x0+j*cw:.2f}" y="{y0+i*ch:.2f}" width="{cw:.2f}" height="{ch:.2f}" fill="{fill}" fill-opacity="{opacity:.3f}" stroke="#dbe1e8" stroke-width="0.8"/>')


def main():
    m,n=7,5
    a=[[math.sin((i+1)*(j+2))+.13*(i-j)+(.4 if i==j else 0) for j in range(n)] for i in range(m)]
    u,b,v=bidiagonalize(a); check=matmul(transpose(u),matmul(a,v)); sim=frob(sub(check,b))/frob(a); ou=frob(sub(matmul(transpose(u),u),eye(m))); ov=frob(sub(matmul(transpose(v),v),eye(n)))
    curves={r:power_norm_curve(r) for r in (.2,.8,.98)}
    s=[math.exp(-i/5.0) for i in range(30)]; randrows=randomized_range_errors(s,5,list(range(0,9)),(0,1))
    assert sim < 1e-12 and ou < 1e-12 and ov < 1e-12
    assert curves[.2][-1][1] < curves[.8][-1][1] < curves[.98][-1][1]
    range_by_qp={(q,p):error for q,p,error,_ in randrows}
    assert all(range_by_qp[(1,p)] < range_by_qp[(0,p)] for p in range(9))

    W,H=1440,610
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">','<title id="title">SVD bidiagonal reduction, norm iteration and randomized range approximation</title>','<desc id="desc">Panels show orthogonal bidiagonal reduction, convergence of spectral norm power estimates, and effects of oversampling and power iteration on randomized range approximation.</desc>','<style>text{font-family:Inter,"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;font-size:15px;fill:#1f2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#fffefb;stroke:#d7dee8}.grid{stroke:#e2e8f0}.note{font-size:15px;fill:#64748b}.legend{font-size:15px}</style>',f'<rect width="{W}" height="{H}" fill="#ffffff"/>','<text x="720" y="34" text-anchor="middle" class="title">SVD 计算：先压缩结构，再按所需精度与规模选路线</text>']
    for x,t in [(70,'A  左右正交变换把矩形矩阵压到双对角'),(570,'B  谱间隙决定谱范数估计速度'),(1030,'C  oversampling 与 power steps 改善随机范围')]: svg.append(f'<text x="{x}" y="67" class="panel">{t}</text>')
    heatmap(svg,a,100,125,150,180,'原始 A（7×5）'); svg.append('<text x="285" y="220" class="panel">→</text>'); heatmap(svg,b,330,125,150,180,'B=UᵀAV')
    svg.append(f'<text x="95" y="342" class="note">归一化约化残差：{sim:.2e}</text>'); svg.append(f'<text x="95" y="367" class="note">U / V 正交缺陷：{ou:.2e} / {ov:.2e}</text>'); svg.append('<text x="95" y="405" class="note">蓝色表示非零幅度；B 只保留主对角与第一超对角。</text>')

    colors={.2:'#2f6fbd',.8:'#c36a14',.98:'#248a57'}; shapes={.2:'circle',.8:'square',.98:'diamond'}; x1,y0,w,h=570,88,330,330
    svg += axes(x1,y0,w,h,[(1,'1'),(8,'8'),(15,'15'),(22,'22'),(30,'30')],[(1e-16,'10⁻¹⁶'),(1e-12,'10⁻¹²'),(1e-8,'10⁻⁸'),(1e-4,'10⁻⁴'),(1,'1')],'AᵀA 幂迭代次数','1 − σ̂₁/σ₁')
    for r,curve in curves.items():
        pts=[]
        for k,e in curve:
            x=x1+(k-1)/29*w; y=y0+h-logmap(e,1e-16,1,0,h); pts.append((x,y))
        svg.append(poly(pts,colors[r]));
        for x,y in pts[::5]: svg.append(mark(x,y,colors[r],shapes[r]))
    svg.append('<text x="585" y="112" class="note">有效收敛比约为 (σ₂/σ₁)²；0.98 最慢</text>')

    x2=1030
    svg += axes(x2,y0,w,h,[(0,'0'),(2,'2'),(4,'4'),(6,'6'),(8,'8')],[(1,'1'),(1.5,'1.5'),(2,'2'),(3,'3'),(5,'5')],'oversampling p','‖(I−QQᵀ)A‖₂ / σₖ₊ₚ₊₁',ylog=False)
    for power,color,shape in [(0,'#c43d3d','square'),(1,'#248a57','diamond')]:
        rows=[r for r in randrows if r[0]==power]; pts=[]
        for _,p,_,ratio in rows:
            x=x2+p/8*w; y=y0+h-(max(1,min(5,ratio))-1)/4*h; pts.append((x,y))
        svg.append(poly(pts,color));
        for x,y in pts: svg.append(mark(x,y,color,shape))
    svg.append('<text x="1045" y="112" class="note">目标秩 k=5；固定 Gaussian sketch seed=20260815</text>')

    legends=[(580,colors[.2],'circle','σ₂/σ₁=0.2'),(700,colors[.8],'square','0.8'),(795,colors[.98],'diamond','0.98'),(1050,'#c43d3d','square','q=0'),(1160,'#248a57','diamond','q=1')]
    for x,c,sym,label in legends: svg.append(mark(x,500,c,sym)); svg.append(f'<text x="{x+10}" y="504" class="legend">{label}</text>')
    svg.append('<text x="720" y="555" text-anchor="middle" class="note">B 面板只估计最大奇异值；C 面板是有限维单种子实验，概率保证、单遍算法与 structured sketch 留给随机低秩专章。</text>')
    svg.append('<text x="720" y="580" text-anchor="middle" class="note">生成：plot_svd_bidiagonal_norm.py · Python 标准库 · seed=20260815</text>'); svg.append('</svg>')
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text('\n'.join(svg),encoding='utf-8')
    print(f'saved={OUT}'); print(f'bidiagonal:residual={sim:.3e},orth_u={ou:.3e},orth_v={ov:.3e}')
    for r in (.2,.8,.98):
        c=curves[r]; print(f'norm:ratio={r},k5={c[4][1]:.3e},k15={c[14][1]:.3e},k30={c[29][1]:.3e}')
    for row in randrows:
        if row[1] in (0,2,5,8): print(f'range:q={row[0]},p={row[1]},error={row[2]:.3e},over_opt={row[3]:.3f}')


if __name__=='__main__': main()
