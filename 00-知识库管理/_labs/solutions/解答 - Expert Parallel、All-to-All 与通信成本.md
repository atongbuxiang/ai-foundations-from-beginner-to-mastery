---
type: solution
status: draft
area: [architecture, moe, distributed-systems]
topic: "[[Expert Parallel、All-to-All 与通信成本]]"
exercise: "[[习题 - Expert Parallel、All-to-All 与通信成本]]"
sources: ["[[S-2022-Hwang-Tutel]]", "[[S-2022-Rajbhandari-DeepSpeed-MoE]]", "[[S-2022-Gale-MegaBlocks]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Expert Parallel、All-to-All 与通信成本

## A. 识别与复述

### ARCH-EP-A01
本地 Router；生成/pack assignment；dispatch All-to-All；expert owner 本地分组与 FFN；combine All-to-All 返回；inverse permutation、gate sum 与 residual。反向还要传相应梯度。

### ARCH-EP-A02
Logical payload 按张量 shape 数有用 bytes；physical traffic 计 collective 算法在真实链路经过的 bytes/跳数；latency 还含启动、拥塞、pack、同步与重叠。三者不能互代。

### ARCH-EP-A03
DP 切数据/复制模型；TP 切单层矩阵；PP 切层；EP 切专家集合；SP/CP 切 sequence/context。组合布局决定每种 collective 的参与组和频率。

## B. 手算与建模

### ARCH-EP-B01
$$2rTkds=2(.75)(8192)(2)(4096)(2)=201{,}326{,}592\text{ bytes}=192\text{ MiB}.$$
它不含 metadata、padding、多跳和反向。

### ARCH-EP-B02
每设备 $64/8=8$ 个专家，专家参数为 $8\times1.5=12$B。还需加 Router、dense/shared 层与并行副本。

### ARCH-EP-B03
两者 $Q/B$ 相同，但 B 的启动项为 $1024\ell$，A 仅 $8\ell$；小消息也常降低有效带宽，所以 B 可能显著更慢。若通信能合并/重叠，结论需实测。

## C. 推导与证明

### ARCH-EP-C01
有 $Tk$ 个 assignment，每个发送 $d$ 个、每个 $s$ bytes，dispatch 为 $Tkds$；只有比例 $r$ 过网。输出同宽返回再乘 2，得 $2rTkds$。

### ARCH-EP-C02
同步 barrier 只有所有 rank 完成本层才能继续，故 $T_{step}\ge T_i$ 对每个 $i$ 成立，进而 $T_{step}\ge\max_iT_i$。平均 load 相同不约束最大值。

### ARCH-EP-C03
若计算 $C$、通信 $M$，完全串行 $T=C+M$；理想完全重叠且无依赖/争用时 $T\ge\max(C,M)$，可达到该下界。真实时间位于其间并加 pack/sync 等额外项。

## D. 边界、反例与纠错

### ARCH-EP-D01
若通信仅占原端到端 10%，字节下降 20% 的理论总收益上限约 2%，且有效带宽、消息数或 overlap 可能同时变差。Amdahl、拓扑与尾部必须进入判断。

### ARCH-EP-D02
Dropless 优化本地不规则 expert GEMM 并保留 assignment；token 仍可能在远端 expert，仍需 dispatch/combine。最忙设备的变长 batch 也仍决定尾部。

### ARCH-EP-D03
四 rank 总负载 16：$[4,4,4,4]$ 与 $[10,2,2,2]$ 平均都为 4，最大值分别 4 与 10。若每 assignment 时间近似相同，第二种同步下界约为前者 2.5 倍。

## E. AI 迁移

### ARCH-EP-E01
扫 $T,k,E$、EP size、experts/device、均匀/偏斜路由、node placement、dtype、capacity 与 overlap；固定其他并行度。记录 per-rank bytes/load、collective/pack/GEMM 时间、overlap、p50/p95/p99 step、显存和 tokens/s。

### ARCH-EP-E02
固定 assignment trace，分别把常互访专家放在本节点、随机放置和跨节点最坏放置；重放并记录 remote fraction、inter-node bytes、链路利用、collective 和端到端时间。这样把 placement 与 Router 质量分离。

### ARCH-EP-E03
先看 MoE layer 占比；再分 pack、A2A、GEMM、combine。A2A 高则检查 bytes 与带宽：bytes 高查 $k$/remote/padding，带宽低查消息/拓扑；若等待高查 max-rank skew；若通信被覆盖则转查 GEMM/straggler。每步用 per-rank trace 验证，不用平均值猜测。

