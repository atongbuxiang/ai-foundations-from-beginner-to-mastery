---
type: solution
status: verified
area: [training, distributed-systems, reproducibility]
topic: "[[通信 Roofline、非确定性与分布式训练证据地图]]"
exercise: "[[习题 - 通信 Roofline、非确定性与分布式训练证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 通信 Roofline、非确定性与分布式训练证据地图

> [!warning] 使用边界
> Roofline 是上界模型，profiler 是观测，matched learning curve 是算法证据；三者不能相互替代。

## A. 识别与复述

### TRN64-A01
$I=W/Q$ 是每 byte 数据移动对应的 work；compute ceiling 为 $C$，bandwidth ceiling 为 $BI$，ridge $I^*=C/B$。HBM、NVLink/PCIe、跨节点网络和 NVMe 各有不同 $B$、latency 与可 overlap 范围，所以同一 job 有多个分层 ridge。

### TRN64-A02
bitwise 要求位串相同；numerical 允许声明容差；trajectory 比较 learning curves/状态路径；decision 要求最终模型选择或工程结论在预定风险下稳定。同 seed 只是控制 RNG 输入的一部分，连 bitwise 都不保证，更不能单独证明后三级。

### TRN64-A03
浮点归约：ring/tree 加法顺序；并发/原子：atomic update 到达顺序；kernel：autotuner 选择不同 convolution；RNG：dropout/rounding stream 错位；数据/故障：sampler 顺序或 elastic restart；软件硬件：driver/compiler/firmware 变化。需要分别锁定或纳入变异分布。

## B. 手算与构造

### TRN64-B01
$I^*=300/3=100$ FLOP/byte（TFLOP/TB 单位相消）。$I=40$ 时 $BI=120$ TFLOP/s，受带宽限制；$I=200$ 时 $BI=600$，由 compute ceiling 截为 300 TFLOP/s。

### TRN64-B02
latency 为 $14\times4\mu s=56\mu s$；bandwidth 项 $1.75/350$ s $=5$ ms；总约 $5.056$ ms。遮蔽 80% 后暴露约 $1.011$ ms。真实 overlap 需由时间线而非固定百分比确认。

### TRN64-B03
$$
E_{64}=\frac{800}{64\times18}\approx0.6944=69.4\%.
$$
峰值 FLOPs 不是单卡执行同一 workload 的实测 $T_1$；用它作分母会混入 kernel 利用率与算法差异，失去 strong-scaling 的含义。

## C. 推导与证明

### TRN64-C01
运行时间至少为 $\max(W/C,Q/B)$，故 rate
$$
\frac{W}{T}\le\min\left(C,\frac{W}{Q/B}\right)=\min(C,BI).
$$
两条上界相交于 $C=BI^*$，所以 $I^*=C/B$。

### TRN64-C02
设 buckets 在 backward 的 3、6、9 ms ready，各通信 4 ms 且串行：通信区间为 $[3,7],[7,11],[11,15]$。若 compute 到 12 ms，总通信和是 12 ms，但 step 仅被最后尾巴延长到 15 ms，即暴露 3 ms。overlap overhead 应从依赖 DAG 的 critical path/区间并集求，不可简单相加 profiler kernel durations。

### TRN64-C03
在有限精度取 $a=10^{20},b=-10^{20},c=3.14$：$(a+b)+c=3.14$，而 $a+(b+c)$ 中 $b+c$ 舍入回 $-10^{20}$，结果约 0。collective order 能改变末位并经非线性放大；但若多 seed 的质量区间、失败率和模型选择均稳定，仍可达到 decision reproducibility，而无需强求 bitwise。

## D. 边界、反例与纠错

### TRN64-D01
tokens/s 可因 tokenizer 口径、padding、短序列、skip update 或更大 global batch 上升；达到同 loss 可能需要更多 tokens/steps，失败 run 也可能被剔除。成本结论必须用相同有效 token/quality 口径和全部失败分母，最好报告 time-to-quality 与能耗/费用。

### TRN64-D02
一次相同可能是偶然；还未锁定 driver、library、deterministic flags、data snapshot、kernel/autotune 和 distributed topology。至少要做预定重复、扰动环境或 seed 的分层实验，并按目标报告 bitwise hash、数值容差、trajectory band 或 decision stability。

### TRN64-D03
NCCL 下降可能同时发生于 GPU clock 提升、输入 pipeline 变快导致 bucket ready 改变、bucket size/顺序改变、warmup/cache 状态不同，或只选择最好 trace。需 configuration manifest、交错/配对运行、完整 critical path 和单因素干预，才能支持因果归因。

## E. AI 迁移

### TRN64-E01
E0：配置、代码/软件/硬件/data manifest；E1：吞吐、显存、链路 counters；E2：profiler DAG 与 exposed tail；E3：compute/data-matched learning curve 和 failure denominator，首次直接检验训练质量；E4：paired repeats、CI/尾部；E5：只改目标机制的干预、negative control 与 mediator timing，开始支持特定因果判断。

### TRN64-E02
compute-matched 固定有效 tokens/FLOPs/update contract，在同预算比较 quality；wall-clock-matched 固定时间/设备预算比较可达 quality。预注册 checkpoint rule，不在 target 上挑 checkpoint；init/data seeds 配对，系统 repeats 分层；报告 paired difference CI、全部 planned failures、fixed-horizon 或预定 sequential stopping，禁止看到优势后临时停。

### TRN64-E03
DAG 可写：collective dtype→gradient reduction error→attention score/probability bias→entropy/concentration→collapse，同时 hardware/kernel、scale、data order、loss scale 是共同原因。negative controls：不经过该 collective 的层/张量；保持 dtype 但在 reduction 前后做 FP32 oracle。测量 mediator 必须在 collapse 前逐 step 保存，并用只升 reduction precision 的干预检验中介先变、hazard 后变。

## 无提示重做

- [ ] 48 小时后重算 ridge 与 exposed tail。
- [ ] 一周后把一条 speedup 声明完整映射到 E0—E5。
