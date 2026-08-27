---
type: exercise
status: verified
area: [training, optimization, mup, embedding, attention]
topic: "[[Embedding、Readout、Attention 与特殊参数组缩放]]"
solution: "[[解答 - Embedding、Readout、Attention 与特殊参数组缩放]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Embedding、Readout、Attention 与特殊参数组缩放

> [!abstract] 训练目标
> 能按 lookup、sum、dot product、coordinate affine 与 factor product 的使用语义推导特殊参数组，不用 tensor rank 代替几何。

## A. 识别与复述

### TRN46-A01
为什么 embedding 与 readout 即使都关联 $V\times d$ 矩阵，也不能使用同一 hidden-matrix rule？

### TRN46-A02
解释 weight tying 的双角色冲突；forward multiplier 与 optimizer moments 分别要审计什么？

### TRN46-A03
比较 bias、norm scale、Q/K/V/O 与 LoRA A/B 的 forward 聚合语义和主要 scale axes。

## B. 手算与构造

### TRN46-B01
$W^{out}_{jv}$ update 为 $c/d$，$h_j=1$。计算 $\Delta z_v$。若 update 改为 $c/\sqrt d$，随 $d$ 怎样变化？

### TRN46-B02
$q_j,k_j$ 独立、均值 0、方差 2。计算 $q^\top k$ 的方差；分别乘 $1/\sqrt{d_h}$ 与 $1/d_h$ 后的方差。

### TRN46-B03
一个 batch 的 token IDs 为 $[1,1,1,2]$，loss 对 token embedding 输出的梯度分别为 $g_1,g_2,g_3,g_4$。在 sum reduction 与 mean reduction 下写 $E_1,E_2$ 的梯度；说明 token frequency 怎样进入 update。

## C. 推导与证明

### TRN46-C01
从 softmax cross-entropy 推导 readout gradient
$$
\partial L/\partial W_{jv}=h_j(p_v-\mathbf1[v=t]).
$$
说明为何 update 与 $h$ 对齐，从而按 $d$ 聚合。

### TRN46-C02
对 tied parameter $E$，若 readout 使用 $z=\alpha_dhE^\top$，推导总梯度是 lookup 项与 readout 项之和，并标出 $\alpha_d$。

### TRN46-C03
对 $W_{eff}=W_0+\alpha AB$ 推导一阶与二阶 update
$$
\Delta(xAB).
$$
若 $B_0=0$，第一步中 $\nabla A$ 为什么可能为零？

## D. 边界、反例与纠错

### TRN46-D01
反驳：“所有二维参数都应交给 Muon/hidden μP group。”至少用 embedding、readout、norm 与低秩因子中的三例。

### TRN46-D02
构造 $d_{model}$ 同样加倍，但 attention score scaling 不应以同样方式改变的两条 head path。

### TRN46-D03
为什么 $1/\sqrt{d_h}$ 与 $1/d_h$ 不能简单判为一个正确、一个错误？分别写出它们控制的阶段和失败观察。

## E. AI 迁移

### TRN46-E01
为 tied-embedding Transformer 写 parameter-group manifest：embedding/head、Q/K/V/O、FFN、bias、norm，包含 init、multiplier、optimizer、LR、decay 与 telemetry。

### TRN46-E02
设计一个 attention scaling 消融，隔离固定 head 数、固定 head dimension、zero-query 与 sequence length 的交互。

### TRN46-E03
审计 LoRA 差分 LR：规定 width/rank 路径、zero-init 因子、factor/combined update 和 target claim 边界。

## 作答与复盘

查看 [[解答 - Embedding、Readout、Attention 与特殊参数组缩放]] 前，先对每个参数写“选择/求和/点积/逐坐标/乘积”标签。
