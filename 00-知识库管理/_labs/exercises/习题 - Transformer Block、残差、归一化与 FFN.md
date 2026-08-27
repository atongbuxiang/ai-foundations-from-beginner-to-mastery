---
type: exercise
status: draft
area: [architecture, transformer, residual, normalization, feed-forward]
topic: "[[Transformer Block、残差、归一化与 FFN]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Transformer Block、残差、归一化与 FFN]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Transformer Block、残差、归一化与 FFN

## A. 识别与复述

### ARCH-BLOCK-A01
写出一个 Pre-Norm self-attention + FFN block 的两步方程，并标注每一步 shape。

### ARCH-BLOCK-A02
说明 attention 与 position-wise FFN 分别沿哪条轴混合信息。

### ARCH-BLOCK-A03
区分 attention dropout、residual dropout 与 DropPath 的作用位置和随机单位。

## B. 手算与建模

### ARCH-BLOCK-B01
给定 $d=512,d_{ff}=2048$，计算普通 FFN 与同宽三矩阵门控 FFN 的主权重数。

### ARCH-BLOCK-B02
对标量 $F(x)=ax$、$N(x)=cx$，分别求 Pre-Norm $y=x+F(N(x))$ 与 Post-Norm $y=N(x+F(x))$ 的导数。

### ARCH-BLOCK-B03
一个 block 输入为 $(B,T,d)=(8,128,768)$，attention 分支输出 $(8,128,512)$。它能否直接 residual addition？给出最小修正。

## C. 推导与证明

### ARCH-BLOCK-C01
推导 Pre/Post-Norm 抽象子层的精确 Jacobian，并指出恒等项的位置差异。

### ARCH-BLOCK-C02
把 $L$ 层 Pre-Norm residual recurrence 展开成初值与分支增量之和；说明展开本身没有证明什么。

### ARCH-BLOCK-C03
在独立零均值分支增量、方差相同的简化假设下，推导 residual scale 为 $1/\sqrt L$ 时总增量方差的阶；再与确定性最坏界比较。

## D. 边界、反例与纠错

### ARCH-BLOCK-D01
反驳：“Pre-Norm 有恒等 Jacobian 项，所以任意深度下梯度范数必定稳定。”

### ARCH-BLOCK-D02
构造一个 FFN 对 token 独立、但输出仍依赖其他 token 的两步例子。

### ARCH-BLOCK-D03
指出“DeepNorm 成功训练千层模型，因此任意任务都应使用千层 Post-Norm”的至少四个逻辑缺口。

## E. AI 迁移

### ARCH-BLOCK-E01
设计一个 Pre/Post-Norm 公平比较实验，列出必须固定、扫描和报告的变量。

### ARCH-BLOCK-E02
为 residual/dropout 接线写一个最小单元测试组，覆盖 train/eval 与 checkpoint recomputation。

### ARCH-BLOCK-E03
为 Attention Residuals 写一张版本化 evidence card，区分标准 residual、full AttnRes 与 block AttnRes。

## 解答入口

[[解答 - Transformer Block、残差、归一化与 FFN]]
