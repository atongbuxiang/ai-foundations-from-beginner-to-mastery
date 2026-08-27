---
type: solution
status: verified
area: [training, optimization, muon, systems, reproducibility]
topic: "[[Muon 的扩展证据、系统成本与迁移边界]]"
exercise: "[[习题 - Muon 的扩展证据、系统成本与迁移边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Muon 的扩展证据、系统成本与迁移边界

> [!warning] 使用边界
> “更快”不是单一数字。每次同时写 quality target、成本分母、调参预算、失败运行与外推范围。

## A. 识别与复述

### TRN32-A01
- L0 数学身份：支持 norm duality/polar/RMS 定理，不支持训练优势；
- L1 原始算法/小规模原型：支持该实现于指定任务的可运行性和观测，不支持跨域普遍性；
- L2 大规模单组织主证据：支持论文模型/数据/预算内的规模化结果，不自动构成独立复现；
- L3 框架产品化：支持 API 可用和实现合同，不支持 empirical superiority；
- L4 跨组织长期复现：在多模型/硬件/预算及失败结果下支持更强稳健外推，仍需明确覆盖范围。

### TRN32-A02
tokens 测样本/优化效率；model FLOPs 只计模型前后向；optimizer-inclusive FLOPs 再含 NS/state；wall-clock 含 kernel/communication/tail；energy 与 dollar 还含硬件功耗、价格、利用率和失败重启。同一方法可在这些横轴上排序不同。

### TRN32-A03
state：Adam 的 $(m,v)$ 无 lossless map 到 Muon buffer，复制/清零会有 transient；LR meaning：Adam 经 $v^{-1/2}$，Muon 经 polar/shape scale，同数字步幅不同；ownership：tied embedding/head 若被两个 optimizers 持有会双更新或 state 冲突。三者都必须进 migration manifest。

## B. 手算与构造

### TRN32-B01
baseline 总时长 $100000$ s；Muon 为
$$
80000\times1.08=86400\text{ s}.
$$
wall-clock speedup ratio 为
$$
100000/86400\approx1.1574,
$$
即 throughput-to-target 提升约 15.7%，或用“耗时减少”口径是 13.6%。达标 steps 比率为 $100/80=1.25$，可说 25% step-efficiency ratio / 20% fewer steps；单步 systems overhead 是 8%。三者分母不同，不能都写“快 25%”。

### TRN32-B02
Muon state：
$$
8\text{B}\times4\text{ bytes}=32\text{ GB}.
$$
fallback AdamW：
$$
4\text{B}\times2\times4=32\text{ GB}.
$$
合计 64 GB（十进制）。真实 peak 还含 BF16 parameters 约 24 GB、gradients、master weights（若有）、optimizer temporaries/NS Gram、activation/checkpoint、allocator fragmentation、communication buckets、replication/sharding 与 framework metadata。

### TRN32-B03
AdamW mean/median 都为 100 小时。Muon sum 为 477，mean 为 95.4 小时，median 为 82 小时，但有一个 150 小时长尾，可能是 divergence/restart 或硬件异常。只报 best=80 或 median=82 会把 20% run 的严重风险隐藏；应报告每个 run、failure definition、mean/quantiles 或 survival/time-to-target 分析。

## C. 推导与证明

### TRN32-C01
总达标时间 $T=N\,t_{step}$，所以
$$
\frac{T_{base}}{T_{new}}
=\frac{N_{base}}{N_{new}}
\cdot
\frac{t_{step,base}}{t_{step,new}}.
$$
第一因子测 steps-to-quality 的 optimization effect，第二因子测单步 systems effect；一个可大于 1、另一个小于 1。tokens per step 若不同，还需再拆 batch/tokens factor。

### TRN32-C02
框架收录支持存在一个通过维护/接口门槛的软件实现，即命题“用户可调用某 transition”。效果命题则是某数据分布、模型、预算和调参协议下 empirical risk/time 的差异。前者没有包含后者的随机变量、baseline 或估计量，逻辑上不能蕴含后者；最多提高复现实验的可行性。

### TRN32-C03
把总搜索 compute $C$ 预先等分，或按对称规则给两方法相同 trial-equivalent budget。使用相同 fidelity ladder、early-stop metric/patience 和搜索器；保留独立的 final-confirmation seeds，不参与选超参数。报告全部 trials 与搜索成本，并用 nested selection/held-out confirmation 避免只在搜索噪声中挑赢家。若某方法单 trial 更贵，应按 compute 而非 trial count 分配。

## D. 边界、反例与纠错

### TRN32-D01
准确表述：[[S-2025-Liu-Muon-Scalable-LLM]] 在其 Moonlight 3B/16B MoE、数据与 compute-optimal scaling 协议中报告 Muon 配方相对所设 baseline 约 2 倍的 compute-efficiency 结果，并公开相关资源。该数字受模型族、token/quality 口径、baseline 调参和系统实现限制，不等价于所有 LLM 的 wall-clock 减半。

### TRN32-D02
若 Muon 只需 baseline 的 80% steps，但每步因 kernel/communication 需 1.5 倍时间，则总 wall-clock ratio为 $0.8\times1.5=1.2$，反而慢 20%。tokens-to-quality 更好只控制第一个因子。

### TRN32-D03
Adam $m$ 的 EMA convention/bias correction/scale 未必等于 Muon buffer；$v$ 携带的 coordinate scale 被丢弃；两者 parameter groups不同；step clocks和 skipped gradients可能不同；复制后 polar normalization 会非线性改变其意义。切换还会产生 warmup/transient。该做法只能叫 heuristic initialization，并需与 reset/overlap baseline 比较。

## E. AI 迁移

### TRN32-E01
- offline replay：输入 checkpoint 与固定 gradient traces；测 direction/scale/NS residual/kernel/state；gate 是无 shape/NaN/scale 异常；保存旧 checkpoint、manifest 和 replay outputs；
- controlled small run：固定 data/seeds，总搜索预算对称；测多横轴 quality、ablation、failure distribution；gate 是预注册质量/数值容忍；保留每 trial config/log；
- shadow-scale：真实 shard/network 上短 horizon；测 P50/P95、network bytes、peak/OOM、save/load；通过运维 gate 才扩展。任一失败即回滚到完整 AdamW state，而非只恢复 weights。

### TRN32-E02
每个 run 一行：optimizer version/config、trial role、seed、status/failure reason、tokens、model/total FLOPs、wall/energy、quality curve、time-to-target、step P50/P95/P99、optimizer kernel time、communication bytes/time、persistent/peak memory、checkpoint save/load checksum。报告搜索总成本和所有 runs，再给 matched-target tables，而非只展示最佳曲线。

### TRN32-E03
判定表：

1. 日期/版本：是否为近期、是否有正式论文；
2. 数学：定义对象、假设、不变量、反例；
3. 实现：公开代码、commit、tests、checkpoint；
4. 数值：reference residual、dtype/condition/failure；
5. 系统：FLOPs、workspace、communication、tail；
6. 经验：同预算 baseline、ablation、seeds、失败；
7. 外部性：独立团队、跨模型/硬件；
8. 结论：分别标为 identity、derived-under-assumptions、primary evidence、replicated evidence 或 open hypothesis。

## 无提示重做

- [ ] 48 小时后用一个乘法式拆开 step efficiency 与 systems overhead。
- [ ] 一周后从空白写出带 rollback 的三阶段迁移协议。
