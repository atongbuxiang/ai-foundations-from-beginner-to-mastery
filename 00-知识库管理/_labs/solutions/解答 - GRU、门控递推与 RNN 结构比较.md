---
type: solution
status: draft
area: [architecture, rnn, gru]
topic: "[[GRU、门控递推与 RNN 结构比较]]"
exercise: "[[习题 - GRU、门控递推与 RNN 结构比较]]"
sources: ["[[S-2014-Cho-GRU]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - GRU、门控递推与 RNN 结构比较

## A. 识别与复述

### ARCH-GRU-A01
$r=\sigma(W_rx+U_rh+b_r)$，$z=\sigma(W_zx+U_zh+b_z)$，$\tilde h=\tanh(W_hx+U_h(r\odot h)+b_h)$，$h'= (1-z)\odot h+z\odot\tilde h$。这里 $z=1$ 偏向写新候选。

### ARCH-GRU-A02
Update 对每一维在旧 hidden 与候选间连续插值；reset 在候选生成阶段调节旧 hidden 的可见程度。二者都是数据依赖向量，不是整个 cell 的单一硬开关。

### ARCH-GRU-A03
GRU 只传 $h$，常见两门；LSTM 传 $(h,c)$，常见三门加候选。相同 hidden 宽度下 GRU 常为三组 affine、state $d_h$，LSTM 四组 affine、state $2d_h$。

## B. 手算与建模

### ARCH-GRU-B01
$(1-z)\odot h=(0.75,0.2)\odot(2,-1)=(1.5,-0.2)$；$z\odot\tilde h=(0,2.4)$；和为 $(1.5,2.2)$。若得到 1.65，则是算术错误。

### ARCH-GRU-B02
$h_t=0.8h_{t-1}+0.2(4)$。$h_1=0.8$，$h_2=1.44$；固定点满足 $h=0.8h+0.8$，故极限 4。

### ARCH-GRU-B03
$3d_h(d_x+d_h)+3d_h=3(32)(52)+96=5088$。单层单样本只需 32 个 recurrent state scalars。

## C. 推导与证明

### ARCH-GRU-C01
把 $z,\tilde h$ 固定，$h_t=(1-z_t)\odot h_{t-1}+\text{constant}$，直接 Jacobian 为 $\operatorname{diag}(1-z_t)$；跨步为逐维 $\prod_k(1-z_k)$。完整导数另含 gate/candidate 路径。

### ARCH-GRU-C02
$U\operatorname{diag}(r)h$ 与 $\operatorname{diag}(r)Uh$ 对所有 $h$ 相等需矩阵交换。若 $U$ 与 $\operatorname{diag}(r)$ 可交换，例如 $U$ 为对角矩阵，或 $r$ 所有分量相同为标量倍 identity，则相等；一般稠密 $U$ 不满足。

### ARCH-GRU-C03
$h_t=(1-z)^th_0+z\sum_{k=1}^t(1-z)^{t-k}\tilde h_k$。旧状态 half-life 满足 $(1-z)^\tau=1/2$，故 $\tau=\log(1/2)/\log(1-z)$。

## D. 边界、反例与纠错

### ARCH-GRU-D01
可能差在 update 语义互补、gate packing 顺序、reset-before/after、input/recurrent bias 拆分、权重转置、候选激活和初态轴。必须比较显式计算图。

### ARCH-GRU-D02
参数数只是一项。GPU fused LSTM kernel 可能优于未优化 GRU；accuracy 依赖任务和优化；更少参数可能欠拟合，也可能正则化更好。应测 latency/throughput/memory/quality，而非演绎绝对排序。

### ARCH-GRU-D03
写入约定：$h'=(1-z)h+z\tilde h$；保留约定令 $z'=1-z$，写 $h'=z'h+(1-z')\tilde h$。只要门 logits/参数相应变换，语义相同。

## E. AI 迁移

### ARCH-GRU-E01
选 $d_x=d_h=2$ 的非对称小权重和输入，分别导出 preactivation、$r,z,\tilde h,h'$；逐段重排 gate、转置权重并处理 bias，直到所有中间量对齐。用非标量 $r$ 和非对角 $U_h$ 暴露 reset 位置差异。

### ARCH-GRU-E02
至少测目标准确率/校准、训练稳定与收敛步数、batch=1 p50/p95 latency、吞吐、峰值 RAM/flash、每会话 state bytes、能耗、量化误差和 reset 可靠性；固定参数预算或延迟预算做公平比较。

### ARCH-GRU-E03
相似处：都有输入依赖的保留/写入系数和固定维流式 state。区别：GRU candidate 是一般非线性 hidden recurrence；经典 SSM 有结构化线性 state dynamics，Mamba 的选择性参数化和 scan/hardware 合同特定。直觉可桥接，方程与复杂度不能等同。

