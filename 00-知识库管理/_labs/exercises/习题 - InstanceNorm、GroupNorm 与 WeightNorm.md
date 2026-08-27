---
type: exercise
status: draft
area: [neural-networks/normalization, vision, parameterization]
topic: "[[InstanceNorm、GroupNorm 与 WeightNorm]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - InstanceNorm、GroupNorm 与 WeightNorm]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - InstanceNorm、GroupNorm 与 WeightNorm

## A

### NN-NGW-A01
对 $X\in\mathbb R^{N\times C\times H\times W}$，分别写出 InstanceNorm2d 与 GroupNorm$(G)$ 的固定轴、归约轴、组数、组大小和常见 affine shape。

### NN-NGW-A02
精确说明 GN 在 $G=1$ 与 $G=C$ 时分别和 LN/IN 的哪些部分等价、哪些部分不一定等价。

### NN-NGW-A03
为什么 WeightNorm 不是 activation normalization？写出它的输入对象、参数化、state、跨样本依赖和不能保证的量。

## B

### NN-NGW-B01
对四个 channels $(1,3),(5,7),(2,2),(0,4)$，令 $\gamma=1,\beta=0$，分别手算 InstanceNorm 和 $G=2$ GroupNorm；处理零方差 channel。

### NN-NGW-B02
对 $v=(3,4),g=10$，先算有效权重 $w$；若 $s=\nabla_wL=(1,2)$，手算 $dg,dv$ 并检查 $v^{\mathsf T}dv=0$。

### NN-NGW-B03
取 $N=1,C=4,H=W=1$。比较 GN 的 $G=1,2,4$ 的实际组大小与退化情况；说明仅看 group count 为什么不够。

## C

### NN-NGW-C01
从 $u=v/\|v\|$ 的 differential 推导 WeightNorm 的 $dg,dv$，并指出投影矩阵的几何意义。

### NN-NGW-C02
证明 $v\mapsto av$（$a>0$）不改变有效权重，但 $\nabla_{av}L=a^{-1}\nabla_vL$。这对固定学习率意味着什么？

### NN-NGW-C03
证明 centered group normalization 的无 affine Jacobian 在 $\varepsilon=0$、非零方差组上最多保留 $m-2$ 个局部自由方向；将结论用于 GN 小组。

## D

### NN-NGW-D01
反驳“GroupNorm(1,C) 与 LayerNorm((C,H,W)) 完全相同”，给出 affine 参数量反例。

### NN-NGW-D02
反驳“InstanceNorm train/eval 一定相同”，使用一个允许 running statistics 的实现合同说明失败。

### NN-NGW-D03
反驳“WeightNorm 固定了线性层的 Lipschitz 常数”。构造两行单位范数但谱范数大于 1 的矩阵。

## E

### NN-NGW-E01
为 batch size 2 的检测模型在 BN 与 GN 间选择，列出必须固定的训练/架构变量、要记录的统计量和不能从 Wu–He 论文直接外推的结论。

### NN-NGW-E02
医学影像标签依赖绝对强度。分析 InstanceNorm 可能删除什么信号，并提出保留/对照方案。

### NN-NGW-E03
一个 RNN/生成模型不允许 minibatch companions 影响单样本输出。比较 LN、GN、WN 三种候选的对象、形状、优化语义与选择条件。

