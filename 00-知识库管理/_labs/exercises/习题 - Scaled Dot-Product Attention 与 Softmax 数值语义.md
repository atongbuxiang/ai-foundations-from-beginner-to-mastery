---
type: exercise
status: draft
area: [architecture, attention, numerical-stability]
topic: "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Scaled Dot-Product Attention 与 Softmax 数值语义]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Scaled Dot-Product Attention 与 Softmax 数值语义

## A. 识别与复述

### ARCH-SDP-A01
写出含 additive mask 的 scaled dot-product attention，并说明 softmax 轴。

### ARCH-SDP-A02
列出推出 $\operatorname{Var}(q^\top k)=d_k$ 的至少三条假设。

### ARCH-SDP-A03
说明减行最大值与除以 $\sqrt{d_k}$ 哪个保持精确 softmax 分布、哪个一般会改变它。

## B. 手算与建模

### ARCH-SDP-B01
用稳定方法计算 $\operatorname{softmax}(1000,1001,999)$，保留三位小数。

### ARCH-SDP-B02
计算 $\operatorname{softmax}(0,0,0)$ 与 $\operatorname{softmax}(0,0,0)/$“后乘 mask $(1,1,0)$”的行和，并给出正确 masked 结果。

### ARCH-SDP-B03
若 $d_k=64$ 且未缩放 dot-product 的方差为 64，分别给出除以 $\sqrt{64}$ 与除以 64 后的方差。

## C. 推导与证明

### ARCH-SDP-C01
从独立、中心化、单位方差坐标推导 $\operatorname{Var}(q^\top k)=d_k$。

### ARCH-SDP-C02
证明 softmax 平移不变，并推出 Jacobian $J=\operatorname{Diag}(a)-aa^\top$ 满足 $J\mathbf1=0$。

### ARCH-SDP-C03
证明当最大 logit 唯一时，$\operatorname{softmax}(z/\tau)$ 在 $\tau\to0^+$ 时趋向对应 one-hot。

## D. 边界、反例与纠错

### ARCH-SDP-D01
构造坐标完全相关的 q/k 情形，使 dot-product 方差不按 $d_k$ 的独立求和公式增长。

### ARCH-SDP-D02
解释为什么用同一个有限大负数填满整行不会得到全零权重。

### ARCH-SDP-D03
反驳：“一阶 Taylor softmax 近似天然保持非负、行和 1 和全域稳定。”

## E. AI 迁移

### ARCH-SDP-E01
设计逐层/逐头 logit 数值审计，至少给出六个统计量和两个失败阈值策略。

### ARCH-SDP-E02
为 fp16/bfloat16 attention 写 mask sentinel 与 all-masked row 的兼容性测试。

### ARCH-SDP-E03
设计 temperature/key normalization 的长度扫描实验，区分代数事实、实验观察和规模外推。

## 解答入口

[[解答 - Scaled Dot-Product Attention 与 Softmax 数值语义]]
