---
type: exercise
status: verified
area: [training, distributed-systems, reproducibility]
topic: "[[通信 Roofline、非确定性与分布式训练证据地图]]"
solution: "[[解答 - 通信 Roofline、非确定性与分布式训练证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 通信 Roofline、非确定性与分布式训练证据地图

> [!abstract] 训练目标
> 能计算 roofline/ridge、latency–bandwidth 与 scaling efficiency，区分四级复现目标，并从配置到因果干预搭建性能—质量联合证据链。

## A. 识别与复述

### TRN64-A01
定义 arithmetic intensity、compute ceiling、memory/communication bandwidth ceiling 与 ridge point。为何分布式训练可能同时有多个 ridge？

### TRN64-A02
区分 bitwise、numerical、trajectory 与 decision reproducibility；“同 seed”最多是其中哪一层的输入条件？

### TRN64-A03
列出分布式非确定性来源树：浮点归约、并发/原子、kernel 选择、RNG、数据/故障、软件/硬件。每类给一个例子。

## B. 手算与构造

### TRN64-B01
设备 compute ceiling 300 TFLOP/s、HBM bandwidth 3 TB/s。求 ridge intensity；kernel intensity 为 40 与 200 FLOP/byte 时，各自的 roofline 上界。

### TRN64-B02
collective 粗模为 $T=\alpha k+M/B$。取 $\alpha=4\,\mu s$、$k=14$、$M=1.75$ GB、$B=350$ GB/s，求时间；若 80% 被 compute 遮蔽，暴露尾巴约多少？

### TRN64-B03
真实单卡 baseline step time 为 800 ms，64 卡为 18 ms。按 strong-scaling efficiency $T_1/(64T_{64})$ 计算效率；若错误用峰值 FLOPs baseline，会损失什么含义？

## C. 推导与证明

### TRN64-C01
由 work $W$、bytes $Q$、峰值算力 $C$ 与带宽 $B$ 推导 attainable rate $\min(C,BI)$，其中 $I=W/Q$，并推导 ridge $I^*=C/B$。

### TRN64-C02
构造三个 bucket 的 backward-ready 与 communication 时间线，证明总通信时间之和不等于 step overhead；真正进入关键路径的是未遮蔽并集/尾巴。

### TRN64-C03
用 $(a+b)+c\ne a+(b+c)$ 的浮点例子说明 collective tree/ring 顺序能改变结果；解释为什么这不自动推翻 decision reproducibility。

## D. 边界、反例与纠错

### TRN64-D01
反驳：“tokens/s 提升 25%，所以训练成本与最终质量都提升 25%。”指出 batch、tokenizer、skip、收敛 step 与失败率混杂。

### TRN64-D02
反驳：“同 seed 两次终点一致，就证明系统可复现。”给出确定性环境未锁定与样本量不足两个缺口。

### TRN64-D03
反驳：“profiler 显示 NCCL 时间下降，所以代码改动导致了吞吐提升。”列出 clock、input pipeline、bucket、warmup 与选择偏差竞争解释。

## E. AI 迁移

### TRN64-E01
为一次 distributed speedup claim 写 E0—E5 证据清单，并标出哪一级开始检验训练质量、哪一级支持因果判断。

### TRN64-E02
设计 compute-matched 与 wall-clock-matched 双重比较，明确 checkpoint 选择、seed pairing、置信区间、failure denominator 和停止规则。

### TRN64-E03
为“低精度 collective 引发 Attention collapse”画因果 DAG，提出至少两个 negative control 与一个 mediator-time-order 测量。

## 作答与复盘

先做单位检查和关键路径时间线，再查看 [[解答 - 通信 Roofline、非确定性与分布式训练证据地图]]。吞吐、质量、因果与复现必须分别给证据，不得相互代替。
