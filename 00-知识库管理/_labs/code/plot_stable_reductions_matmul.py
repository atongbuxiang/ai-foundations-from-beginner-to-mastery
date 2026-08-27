#!/usr/bin/env python3
"""Deterministic reductions and mixed-precision dot/GEMM accuracy experiment."""

from __future__ import annotations

import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_assets" / "plots" / "stable-kernels" / "plot-stable-reductions-matmul-v2.svg"


def f32(x):
    return struct.unpack(">f", struct.pack(">f", float(x)))[0]


def f16(x):
    return struct.unpack(">e", struct.pack(">e", float(x)))[0]


def add32(a, b):
    return f32(f32(a) + f32(b))


def mul32(a, b):
    return f32(f32(a) * f32(b))


def sequential32(values):
    s = 0.0
    for x in values:
        s = add32(s, x)
    return s


def pairwise32(values):
    level = [f32(x) for x in values]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            nxt.append(add32(level[i], level[i + 1]))
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0] if level else 0.0


def kahan32(values):
    s = 0.0
    c = 0.0
    for x in values:
        y = add32(x, -c)
        t = add32(s, y)
        c = add32(add32(t, -s), -y)
        s = t
    return s


def neumaier32(values):
    s = 0.0
    c = 0.0
    for x in values:
        t = add32(s, x)
        if abs(s) >= abs(x):
            c = add32(c, add32(add32(s, -t), x))
        else:
            c = add32(c, add32(add32(x, -t), s))
        s = t
    return add32(s, c)


def relerr(value, ref):
    return abs(value - ref) / max(abs(ref), 1e-300)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def log_y(v, lo, hi, y0, h):
    v = max(lo, min(hi, v))
    return y0 + h - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * h


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="frame"/>']
    xlo, xhi = xticks[0][0], xticks[-1][0]
    for value, label in xticks:
        x = x0 + (math.log2(value) - math.log2(xlo)) / (math.log2(xhi) - math.log2(xlo)) * w
        out += [
            f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0+h}" class="grid"/>',
            f'<text x="{x:.2f}" y="{y0+h+20}" text-anchor="middle">{esc(label)}</text>',
        ]
    ylo, yhi = yticks[0][0], yticks[-1][0]
    for value, label in yticks:
        y = log_y(value, ylo, yhi, y0, h)
        out += [
            f'<line x1="{x0}" y1="{y:.2f}" x2="{x0+w}" y2="{y:.2f}" class="grid"/>',
            f'<text x="{x0-9}" y="{y+4:.2f}" text-anchor="end">{esc(label)}</text>',
        ]
    out += [
        f'<text x="{x0+w/2}" y="{y0+h+45}" text-anchor="middle" class="axis">{esc(xlabel)}</text>',
        f'<text x="{x0-58}" y="{y0+h/2}" text-anchor="middle" class="axis" transform="rotate(-90 {x0-58} {y0+h/2})">{esc(ylabel)}</text>',
    ]
    return out


def xlog(value, lo, hi, x0, w):
    return x0 + (math.log2(value) - math.log2(lo)) / (math.log2(hi) - math.log2(lo)) * w


def poly(points, color, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.6"{d}/>'


def mark(x, y, color, shape="circle", r=3.5):
    if shape == "square":
        return f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{2*r}" height="{2*r}" fill="{color}"/>'
    if shape == "diamond":
        return f'<path d="M{x:.2f},{y-r-1:.2f} L{x+r+1:.2f},{y:.2f} L{x:.2f},{y+r+1:.2f} L{x-r-1:.2f},{y:.2f}Z" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def main():
    ns = [2**k for k in range(0, 17)]
    delta = 2.0**-24
    sums = []
    for n in ns:
        values = [1.0] + [delta] * n
        ref = 1.0 + n * delta
        sums.append((n, relerr(sequential32(values), ref), relerr(pairwise32(values), ref), relerr(kahan32(values), ref)))

    amplitudes = [2.0**k for k in range(0, 33, 2)]
    cancellation = []
    for a in amplitudes:
        bad = [a, 1.0, -a]
        good = [a, -a, 1.0]
        cancellation.append((a, relerr(sequential32(bad), 1.0), relerr(sequential32(good), 1.0), relerr(neumaier32(bad), 1.0)))

    inner = [2**k for k in range(4, 14)]
    accum = []
    for n in inner:
        products = []
        for i in range(n):
            a = f16(math.sin(0.17 * (i + 1)) + 0.21 * math.cos(0.037 * (i + 1)))
            b = f16(math.cos(0.11 * (i + 1)) - 0.13 * math.sin(0.071 * (i + 1)))
            products.append(float(a) * float(b))
        scale = math.fsum(abs(v) for v in products)
        ref = math.fsum(products)
        acc16 = 0.0
        for value in products:
            acc16 = f16(f16(acc16) + f16(value))
        acc32 = sequential32(products)
        acc32_pair = pairwise32(products)
        accum.append((n, abs(acc16 - ref) / scale, abs(acc32 - ref) / scale, abs(acc32_pair - ref) / scale))

    W, H = 1440, 610
    y0, h, w = 88, 330, 330
    xs = [75, 555, 1035]
    colors = {"blue": "#2f6fbd", "orange": "#c36a14", "green": "#248a57", "purple": "#8a4fb8", "red": "#c43d3d"}
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">Stable summation, cancellation, and mixed precision accumulation</title>',
        '<desc id="desc">Three panels compare sequential, pairwise, and compensated summation; nonassociative cancellation orders; and FP16 versus FP32 accumulation of FP16 products.</desc>',
        '<style>text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Noto Sans CJK SC",sans-serif;font-size:15px;fill:#1F2937}.title{font-size:27px;font-weight:650}.panel{font-size:19px;font-weight:650}.axis{font-size:16px}.frame{fill:#FFFEFB;stroke:#64748B}.grid{stroke:#D7DEE8}.note{font-size:15px;fill:#64748B}.legend{font-size:15px}</style>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        '<text x="720" y="34" text-anchor="middle" class="title">稳定求和、点积与矩阵乘法：乘加顺序和累加精度属于算法</text>',
        '<text x="75" y="67" class="panel">A  1 后累加半 ulp：顺序、树归约与补偿</text>',
        '<text x="555" y="67" class="panel">B  同一三项点积：浮点加法不结合</text>',
        '<text x="1035" y="67" class="panel">C  FP16 输入：累加精度控制 GEMM 内核误差</text>',
    ]

    ticks_a = [(1, "1"), (16, "16"), (256, "256"), (4096, "4k"), (65536, "65k")]
    yticks = [(1e-10, "1e−10"), (1e-8, "1e−8"), (1e-6, "1e−6"), (1e-4, "1e−4"), (1e-2, "1e−2"), (1, "1")]
    svg += axes(xs[0], y0, w, h, ticks_a, yticks, "小项个数 n", "relative error")
    for idx, color, shape in [(1, colors["red"], "circle"), (2, colors["blue"], "square"), (3, colors["green"], "diamond")]:
        pts = [(xlog(row[0], 1, 65536, xs[0], w), log_y(max(row[idx], 1e-10), 1e-10, 1, y0, h)) for row in sums]
        svg.append(poly(pts, color, "6 4" if idx == 2 else ""))
        for j in (0, 4, 8, 12, 16):
            svg.append(mark(pts[j][0], pts[j][1], color, shape))
    svg += [
        f'<text x="{xs[0]+18}" y="{y0+25}" class="note">精确值：1+n·2⁻²⁴；逐项加法不断吸收小项</text>',
        f'<text x="{xs[0]+22}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">● sequential</text>',
        f'<text x="{xs[0]+137}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">■ pairwise</text>',
        f'<text x="{xs[0]+245}" y="{y0+h+78}" class="legend" fill="{colors["green"]}">◆ Kahan</text>',
    ]

    ticks_b = [(1, "1"), (256, "2⁸"), (65536, "2¹⁶"), (16777216, "2²⁴"), (4294967296, "2³²")]
    svg += axes(xs[1], y0, w, h, ticks_b, yticks, "消去尺度 a", "|computed−1|")
    for idx, color, shape in [(1, colors["red"], "circle"), (2, colors["blue"], "square"), (3, colors["green"], "diamond")]:
        pts = [(xlog(row[0], 1, 2**32, xs[1], w), log_y(max(row[idx], 1e-10), 1e-10, 1, y0, h)) for row in cancellation]
        svg.append(poly(pts, color, "6 4" if idx == 2 else ""))
        for j in (0, 4, 8, 12, 16):
            svg.append(mark(pts[j][0], pts[j][1], color, shape))
    svg += [
        f'<text x="{xs[1]+18}" y="{y0+25}" class="note">数学上 (a+1)−a = (a−a)+1 = 1；FP32 并非如此</text>',
        f'<text x="{xs[1]+8}" y="{y0+h+78}" class="legend" fill="{colors["red"]}">● (a+1)−a</text>',
        f'<text x="{xs[1]+115}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">■ (a−a)+1</text>',
        f'<text x="{xs[1]+220}" y="{y0+h+78}" class="legend" fill="{colors["green"]}">◆ Neumaier</text>',
    ]

    ticks_c = [(16, "16"), (64, "64"), (256, "256"), (1024, "1k"), (8192, "8k")]
    yticks_c = [(1e-10, "1e−10"), (1e-8, "1e−8"), (1e-6, "1e−6"), (1e-4, "1e−4"), (1e-2, "1e−2")]
    svg += axes(xs[2], y0, w, h, ticks_c, yticks_c, "inner dimension k", "|error| / Σ|aᵢbᵢ|")
    for idx, color, shape in [(1, colors["orange"], "circle"), (2, colors["blue"], "square"), (3, colors["purple"], "diamond")]:
        pts = [(xlog(row[0], 16, 8192, xs[2], w), log_y(max(row[idx], 1e-10), 1e-10, 1e-2, y0, h)) for row in accum]
        svg.append(poly(pts, color, "6 4" if idx == 3 else ""))
        for j in (0, 2, 4, 6, 9):
            svg.append(mark(pts[j][0], pts[j][1], color, shape))
    svg += [
        f'<text x="{xs[2]+18}" y="{y0+25}" class="note">输入先量化为 FP16；参考对乘积用 math.fsum</text>',
        f'<text x="{xs[2]+20}" y="{y0+h+78}" class="legend" fill="{colors["orange"]}">● FP16</text>',
        f'<text x="{xs[2]+120}" y="{y0+h+78}" class="legend" fill="{colors["blue"]}">■ FP32</text>',
        f'<text x="{xs[2]+220}" y="{y0+h+78}" class="legend" fill="{colors["purple"]}">◆ pairwise32</text>',
    ]

    svg += [
        '<text x="720" y="568" text-anchor="middle" class="note">A：树归约把线性误差深度降为对数；B：消去条件性决定顺序敏感；C：storage、multiply 与 accumulate precision 必须分开报告。</text>',
        '<text x="720" y="590" text-anchor="middle" class="note">生成：plot_stable_reductions_matmul.py · Python 标准库 · binary16/binary32 软件舍入</text>',
        '</svg>',
    ]
    if sums[-1][1] <= 1e-3 or sums[-1][2:] != (0.0, 0.0):
        raise RuntimeError("sequential/pairwise/Kahan summation separation audit failed")
    if not any(bad == 1.0 and good == 0.0 and compensated == 0.0 for _, bad, good, compensated in cancellation):
        raise RuntimeError("nonassociative cancellation witness disappeared")
    if max(row[1] for row in accum) <= 1e-4 or max(row[2] for row in accum) >= 1e-6:
        raise RuntimeError("FP16/FP32 accumulation separation audit failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"saved={OUT}")
    for row in sums[::4]:
        print(f"sum:n={row[0]},sequential={row[1]:.6e},pairwise={row[2]:.6e},kahan={row[3]:.6e}")
    for row in cancellation[::4]:
        print(f"cancel:a={row[0]:.1e},bad={row[1]:.6e},good={row[2]:.6e},neumaier={row[3]:.6e}")
    for row in accum:
        print(f"accum:k={row[0]},fp16={row[1]:.6e},fp32={row[2]:.6e},pair32={row[3]:.6e}")


if __name__ == "__main__":
    main()
