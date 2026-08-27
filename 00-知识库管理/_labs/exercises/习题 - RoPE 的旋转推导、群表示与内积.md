---
type: exercise
status: draft
area: [architecture, positional-encoding, rope, group-representation]
topic: "[[RoPE 的旋转推导、群表示与内积]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - RoPE 的旋转推导、群表示与内积]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - RoPE 的旋转推导、群表示与内积

## A. 识别与复述

### ARCH-ROPE-A01
写出二维旋转块 $R_\theta$、RoPE 的 query/key 变换与相对内积恒等式。

### ARCH-ROPE-A02
为什么 RoPE 通常只旋转 Q/K 而不要求旋转 V？说明两者在 attention 中的角色。

### ARCH-ROPE-A03
列出 RoPE 实现必须固定的 pairing、频率表、position offset、rotary dimension 与 dtype 合同。

## B. 手算与建模

### ARCH-ROPE-B01
令 $q=(1,0),k=(0,1),\theta=\pi/4,m=1,n=3$，分别计算 $(R_mq)^\top(R_nk)$ 与 $q^\top R_{n-m}k$。

### ARCH-ROPE-B02
对四维向量 $(x_0,x_1,x_2,x_3)$，分别写出 adjacent pairing 与 half-split pairing 的通道配对。

### ARCH-ROPE-B03
缓存中已有 5 个 token，新输入 3 个 token。写出正确 position IDs；若错误从 0 重启，列出被改变的相对位移。

## C. 推导与证明

### ARCH-ROPE-C01
证明二维旋转矩阵正交，且 $R_a^\top R_b=R_{b-a}$。

### ARCH-ROPE-C02
把多频 RoPE 写成 block-diagonal 表示，证明范数保持与完整相对内积恒等式。

### ARCH-ROPE-C03
设离散位置表示满足 $R_{m+n}=R_mR_n$ 且每个 $R_n$ 正交，证明 $R_n=R_1^n$；说明这给出什么、没给出什么。

## D. 边界、反例与纠错

### ARCH-ROPE-D01
反驳：“RoPE 内积只依相对位移，所以 attention 权重只依相对位移。”

### ARCH-ROPE-D02
构造 pairing 不一致使训练与推理输出改变、但 shape 和 norm 测试都通过的例子。

### ARCH-ROPE-D03
解释为何旋转范数保持不能推出远距离注意力自然衰减，也不能推出长度外推。

## E. AI 迁移

### ARCH-ROPE-E01
写一个跨 full forward 与 KV-cache decoding 的 RoPE 等价性测试方案。

### ARCH-ROPE-E02
设计一个检查不同 head 频率/尺度配置的实验，避免把代数正确性与性能结论混为一谈。

### ARCH-ROPE-E03
给一个 RoPE 实现审查清单，覆盖数学恒等式、张量布局、数值精度和 serving offset。

## 解答入口

[[解答 - RoPE 的旋转推导、群表示与内积]]
