---
type: solution
status: draft
area: [architecture, moe, load-balancing]
topic: "[[MoE 负载均衡辅助损失与偏置]]"
exercise: "[[习题 - MoE 负载均衡辅助损失与偏置]]"
sources: ["[[S-2021-Fedus-Switch-Transformer]]", "[[S-2025-Su-10735-MoE辅助损失]]", "[[S-2026-Su-11760-MoE序列均衡]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - MoE 负载均衡辅助损失与偏置

## A. 识别与复述

### ARCH-AUX-A01
$f_i=T^{-1}\sum_tA_{ti}$ 是 hard selection 频率；$P_i=T^{-1}\sum_tp_{ti}$ 是 soft Router probability 均值。前者接近真实负载，后者连续可导。

### ARCH-AUX-A02
Capacity 关心离散 $n_i\le C_i$ 与 overflow；$E\sum f_iP_i$ 用 soft $P$ 为 hard $f$ 提供梯度。它未直接强制每个 batch 的容量，也依 stop-gradient 和统计粒度。

### ARCH-AUX-A03
Balancing loss 调整专家使用分布；z-loss 控制 $\log\sum_i e^{z_i}$ 的尺度，主要改善 Router 数值稳定。一个均衡负载，一个约束 logits，不能互换。

## B. 手算与建模

### ARCH-AUX-B01
$2(0.75\cdot0.7+0.25\cdot0.3)=2(0.525+0.075)=1.2$。

### ARCH-AUX-B02
均匀时 $f_i=P_i=1/E$，结果为 $E\cdot E/E^2=1$。全部集中到一个专家时，一项为 1，其余为 0，结果为 $E$。

### ARCH-AUX-B03
直接系数为 $\lambda E f_i/T$。expert 1 为 $.01\cdot2\cdot.75/4=.00375$；expert 2 为 $.00125$。softmax 之后 logits 梯度还会发生交叉耦合。

## C. 推导与证明

### ARCH-AUX-C01
把 $f$ stop-grad：
$$\frac{\partial L}{\partial z_{tj}}=\frac{\lambda E}{T}\sum_i f_i p_{ti}(\delta_{ij}-p_{tj})
=\frac{\lambda E}{T}p_{tj}\left(f_j-\sum_i f_ip_{ti}\right).$$
热门专家相对 batch 加权平均有正系数，梯度下降会压低其 logit。

### ARCH-AUX-C02
Cauchy 给 $(\sum_iP_i)^2\le E\sum_iP_i^2$，故 $E\sum_iP_i^2\ge1$；等号当且仅当所有 $P_i=1/E$。这只在 $f=P$ 的理想化条件下成立。

### ARCH-AUX-C03
可写 $\min_\theta L_{task}(\theta)$，约束 $n_i(\theta)-C_i\le0$；拉格朗日式 $L_{task}+\sum_i\mu_i(n_i-C_i)$。辅助损失用可微统计替代离散 $n_i$ 并固定/学习类似乘子，但一般不等于精确约束解。

## D. 边界、反例与纠错

### ARCH-AUX-D01
若某类 token 确实只由少数专家处理得好，强制均匀会把它送给较差专家并提高 task loss。均衡是同构设备利用目标，需与质量画 Pareto。

### ARCH-AUX-D02
主 loss 可按 token mean/sum，aux 可按 layer/group 聚合，padding 和 Top-k 计数也不同；这些缩放改变相对梯度。同一 $\lambda$ 只有在完整 reduction 合同相同时可比。

### ARCH-AUX-D03
设序列 A 全为代码、B 全为诗歌，且两个专家分别擅长二者。逐序列强制 50/50 会让每条序列一半 token 去不适合专家；全 batch 恰好可 50/50 且保留专业化。

## E. AI 迁移

### ARCH-AUX-E01
取 $\lambda=0$ 与对数尺度多个正值，多 seed；固定 capacity/Router/预算。报告 task/aux loss、quality、hard/soft load、drop、Router entropy/logit、tokens/s 与 p95 step time，画 quality–balance–speed Pareto。

### ARCH-AUX-E02
保持总 batch 与目标不变，只改变统计聚合范围；同步控制通信实现。比较估计方差、load tail、专业化、质量、同步时间和对分布突变的响应，尤其检查短序列被过约束。

### ARCH-AUX-E03
每层记录 expert hard counts、$P_i$、max/mean、CV、entropy、drop、dead-expert 连续步数、Router logit/gradient norm、capacity utilization 与 p95 step time；按 token 类型/语言/位置切片，并设持续阈值告警。

