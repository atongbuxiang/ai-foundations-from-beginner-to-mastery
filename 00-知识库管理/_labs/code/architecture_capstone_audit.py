#!/usr/bin/env python3
"""Cross-volume deterministic gate for the 64-node architecture chapter."""

from pathlib import Path
import math

from plot_calculus_operator_figures_v2 import (
    AMBER, BLUE, GRID, INK, MUTED, RED, TEAL,
    begin, finish, heading, line, node, rect, text,
)

OUT = Path(__file__).resolve().parents[2] / "_assets" / "figures" / "architecture" / "fig-architecture-capstone-gate-v1.svg"


def softmax(xs):
    m = max(xs); e = [math.exp(x-m) for x in xs]; z = sum(e)
    return [v/z for v in e]


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(x) for x in zip(*a)]


def close_matrix(a, b, tol=1e-12):
    return all(abs(x-y) < tol for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def track_a_symmetry():
    # One linear message-passing step H'=(A+I)H, then relabel by P.
    a = [[0,1,0],[1,0,1],[0,1,0]]
    h = [[1,0],[0,1],[2,1]]
    p = [[0,0,1],[1,0,0],[0,1,0]]
    abar = [[a[i][j] + (i == j) for j in range(3)] for i in range(3)]
    out = matmul(abar, h)
    ap = matmul(matmul(p, a), transpose(p)); hp = matmul(p, h)
    abarp = [[ap[i][j] + (i == j) for j in range(3)] for i in range(3)]
    outp = matmul(abarp, hp)
    assert close_matrix(outp, matmul(p, out))
    pooled = [sum(r[j] for r in out) for j in range(2)]
    pooledp = [sum(r[j] for r in outp) for j in range(2)]
    assert pooled == pooledp
    return max(abs(x-y) for ra, rb in zip(outp, matmul(p,out)) for x,y in zip(ra,rb))


def track_b_causality_cache_position():
    # Scalar causal attention: full-row computation equals incremental cache.
    q, k, v = [1.0, .5, -1.0], [.2, 1.1, -.4], [2.0, -1.0, 3.0]
    full = []
    cached_k, cached_v = [], []
    incremental = []
    for t in range(3):
        scores = [q[t]*k[j] for j in range(t+1)]
        w = softmax(scores)
        full.append(sum(w[j]*v[j] for j in range(t+1)))
        cached_k.append(k[t]); cached_v.append(v[t])
        wc = softmax([q[t]*x for x in cached_k])
        incremental.append(sum(wc[j]*cached_v[j] for j in range(t+1)))
    assert max(abs(x-y) for x,y in zip(full,incremental)) < 1e-12
    theta, m, n = .37, 7, 11
    # cos/sin dot identity for one RoPE pair.
    relative = math.cos((n-m)*theta)
    explicit = math.cos(m*theta)*math.cos(n*theta)+math.sin(m*theta)*math.sin(n*theta)
    assert abs(relative-explicit) < 1e-12
    return max(abs(x-y) for x,y in zip(full,incremental)), abs(relative-explicit)


def track_c_cost_routing():
    n, d, window = 4096, 1024, 128
    dense_pairs, sparse_pairs = n*n, n*window
    assert dense_pairs/sparse_pairs == n/window == 32
    batch, length, hkv, dh, byte = 2, 8192, 8, 128, 2
    cache = 2*batch*length*hkv*dh*byte
    gqa = 2*batch*length*2*dh*byte
    assert cache/gqa == 4
    t, k, remote = 8192, 2, .75
    moe_network = 2*remote*t*k*d*byte
    loads = [10,2,2,2]
    assert sum(loads)/len(loads) == 4 and max(loads) == 10
    return dense_pairs/sparse_pairs, cache/gqa, moe_network/2**20, max(loads)/(sum(loads)/len(loads))


def figure(a_defect, b_defects, costs):
    out = begin("表示与模型架构跨卷复现门", "对称性、因果/位置与成本/路由三轨必须同时保持对象、恒等式和证据边界。", (BLUE, TEAL, RED))
    heading(out, 42, "A", "结构与重标号", BLUE)
    node(out, 55, 100, 285, 55, "H'=(A+I)H", BLUE, "#EFF6FF", 16)
    node(out, 55, 220, 285, 62, "P H' = (PAPᵀ+I)PH", TEAL, "#ECFDF5", 15)
    node(out, 55, 350, 285, 58, "sum(PH') = sum(H')", AMBER, "#FFF7ED", 15)
    out += [line(198,160,198,212,INK,2,marker="a3"), line(198,286,198,342,INK,2,marker="a3"),
            text(55,465,f"equivariance defect = {a_defect:.1e}",15,700,fill=TEAL)]

    heading(out, 430, "B", "因果、缓存与位置", TEAL)
    node(out, 455, 100, 285, 55, "causal full row", BLUE, "#EFF6FF", 16)
    node(out, 455, 220, 285, 55, "incremental KV cache", TEAL, "#ECFDF5", 16)
    out += [line(598,160,598,212,INK,2,marker="a3"), text(455,325,f"output defect = {b_defects[0]:.1e}",15,700)]
    node(out, 455, 370, 285, 52, "R(m)ᵀR(n)=R(n−m)", AMBER, "#FFF7ED", 15)
    out += [text(455,465,f"rotation defect = {b_defects[1]:.1e}",15,700,fill=TEAL)]

    heading(out, 830, "C", "成本与尾部", RED)
    rows=((105,"dense/local pairs",f"{costs[0]:.0f}×",BLUE),(185,"MHA/GQA cache",f"{costs[1]:.0f}×",TEAL),
          (265,"MoE network",f"{costs[2]:.0f} MiB",AMBER),(345,"max/mean load",f"{costs[3]:.1f}×",RED))
    for y,l,v,c in rows:
        node(out,845,y,170,42,l,c,"#F8FAFC",15); out += [text(1040,y+27,v,16,800,fill=c)]
    out += [text(845,435,"bytes / pairs 是账本；",15,700), text(845,470,"quality / latency 仍需协议。",15,700,fill=RED)]
    return finish(out,"跨架构比较先验证不变量与 shape，再分开模型函数、执行计划、近似误差和硬件结论。")


def main():
    a = track_a_symmetry(); b = track_b_causality_cache_position(); c = track_c_cost_routing()
    OUT.write_text(figure(a,b,c), encoding="utf-8")
    print(f"PASS A graph relabel equivariance defect={a:.3e}")
    print(f"PASS B causal cache defect={b[0]:.3e}; RoPE defect={b[1]:.3e}")
    print(f"PASS C dense/local={c[0]:.1f}x; cache={c[1]:.1f}x; MoE={c[2]:.1f}MiB; tail={c[3]:.1f}x")
    print(OUT)


if __name__ == "__main__":
    main()
