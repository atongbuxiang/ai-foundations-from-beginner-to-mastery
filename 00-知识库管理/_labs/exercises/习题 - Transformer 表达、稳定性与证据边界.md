---
type: exercise
status: draft
area: [architecture, transformer, expressivity, stability, evidence]
topic: "[[Transformer 表达、稳定性与证据边界]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Transformer 表达、稳定性与证据边界]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Transformer 表达、稳定性与证据边界

## A. 识别与复述

### ARCH-STAB-A01
说明 attention、FFN、residual 与 position 在表达中的不同作用。

### ARCH-STAB-A02
区分 universal approximation 的存在性、optimization、generalization 与 efficiency。

### ARCH-STAB-A03
定义 I/T/E/H/O 五级证据。

## B. 手算与建模

### ARCH-STAB-B01
对标量 $F(x)=ax,N(x)=cx$，计算 Pre/Post-Norm 单层 Jacobian，并给出 $a,c$ 使一者放大、一者收缩。

### ARCH-STAB-B02
独立零均值层增量方差为 $\sigma^2$，计算 residual scale 为 $1/L$ 与 $1/\sqrt L$ 时总增量方差。

### ARCH-STAB-B03
给定 centered token matrix 奇异值 $(10,1,0.1,0.01)$，计算 stable rank，并说明它与代数秩的区别。

## C. 推导与证明

### ARCH-STAB-C01
写出通用逼近结论的完整量词骨架，并指出它不包含的学习算法保证。

### ARCH-STAB-C02
推导 Pre/Post Jacobian 与 $L$ 层 Pre-Norm residual exact expansion。

### ARCH-STAB-C03
说明 pure-attention rank collapse 结论迁移到完整 Transformer 前必须逐项检查哪些结构假设。

## D. 边界、反例与纠错

### ARCH-STAB-D01
构造“函数类能表示目标，但给定数据/优化不能可靠学到”的例子。

### ARCH-STAB-D02
反驳：“DeepNorm 训练了千层模型，所以层数越多最终性能必越好。”

### ARCH-STAB-D03
反驳：“Attention Residuals 的 depth weights 就是各层的因果贡献。”

## E. AI 迁移

### ARCH-STAB-E01
为 Pre-Norm、Post-Norm、DeepNorm 写稳定性—效果分账实验。

### ARCH-STAB-E02
设计检查 rank collapse/深度稀释的逐层诊断，并给出不能只看哪一个指标。

### ARCH-STAB-E03
为一个“新 residual 路由优于标准 residual”的声明写 I/T/E/H/O evidence card。

## 解答入口

[[解答 - Transformer 表达、稳定性与证据边界]]
