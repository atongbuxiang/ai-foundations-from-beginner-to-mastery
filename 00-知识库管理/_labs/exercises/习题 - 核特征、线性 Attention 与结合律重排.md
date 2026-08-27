---
type: exercise
status: draft
area: [architecture, efficient-attention, kernel, linear-attention]
topic: "[[核特征、线性 Attention 与结合律重排]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 核特征、线性 Attention 与结合律重排]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 核特征、线性 Attention 与结合律重排

## A. 识别与复述

### ARCH-KERNEL-A01
写出一般归一化 kernel attention，并指出分子、分母和可见邻域各自的语义。

### ARCH-KERNEL-A02
若 $\kappa(q,k)=\phi(q)^\top\phi(k)$，写出 full bidirectional attention 的状态 $S,z$ 与输出公式。

### ARCH-KERNEL-A03
区分“对同一有限维 kernel 做结合律重排”与“选择 ELU+1 等 feature map 改变 softmax kernel”。

## B. 手算与建模

### ARCH-KERNEL-B01
给定 $\phi(q)=(2,1)$，两个 $\phi(k)$ 分别为 $(1,0),(1,2)$，value 为 $3,5$。手算 normalized output，并用 $S,z$ 重算验证。

### ARCH-KERNEL-B02
令 $n=4096,r=64,d_v=128$。比较 materialize $n\times n$ kernel matrix 与先算 $S=\Phi(K)^\top V$ 的主要中间标量数。

### ARCH-KERNEL-B03
对 causal 三步 scalar value，给定 feature 序列，逐步更新 $S_t,z_t$ 并计算每步输出。

## C. 推导与证明

### ARCH-KERNEL-C01
从求和交换顺序推导 $\Phi(Q)(\Phi(K)^\top V)$ 与 $(\Phi(Q)\Phi(K)^\top)V$ 的等价性，并写明 shape 条件。

### ARCH-KERNEL-C02
证明 causal prefix state 递推与对每个 $t$ 显式求和完全等价。

### ARCH-KERNEL-C03
推导固定 local window 的 rolling add/subtract 状态；说明任意 query-dependent mask 为什么通常不能共用一个全局状态。

## D. 边界、反例与纠错

### ARCH-KERNEL-D01
构造分母接近零导致输出极不稳定的例子，说明“线性复杂度”与数值稳定性是不同命题。

### ARCH-KERNEL-D02
反驳：“只要写成 $\phi(q)^\top\phi(k)$，就得到了精确 softmax attention。”

### ARCH-KERNEL-D03
说明固定维 recurrent state 不能仅凭结合律就保证保留任意长历史的全部可查询信息。

## E. AI 迁移

### ARCH-KERNEL-E01
写一个 dense kernel reference 与 full/causal linearized implementation 的等价测试，包含 denominator 检查。

### ARCH-KERNEL-E02
设计一个比较不同 feature map 的实验，把 kernel approximation、最终 output、训练质量和 wall-clock 四层证据分开。

### ARCH-KERNEL-E03
给出 linear attention 实现审查清单，覆盖 mask、normalization、scan、dtype、state reset 与 padding。

## 解答入口

[[解答 - 核特征、线性 Attention 与结合律重排]]
