---
type: exercise
status: draft
area: [learning-theory/empirical-process, learning-theory/complexity]
topic: "[[Rademacher 复杂度与经验复杂度]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Ghost Sample、对称化与经验过程入口]]", "[[浓缩不等式]]"]
related: ["[[解答 - Rademacher 复杂度与经验复杂度]]", "[[收缩引理与 Lipschitz 损失复合]]"]
solution: "[[解答 - Rademacher 复杂度与经验复杂度]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Rademacher 复杂度与经验复杂度

> [!abstract] 训练目标
> 能计算小型 empirical complexity、证明结构性质与 Massart lemma、重建 empirical risk certificate，并把 sign Monte Carlo、optimization gap 与 statistical confidence 分账。

## A. 识别与复述

### LT-RAD-A01

写出 $\widehat{\mathfrak R}_S(\mathcal F)$ 与 $\mathfrak R_m(\mathcal F)$。两个 expectation 分别对谁取？

### LT-RAD-A02

解释 signed、absolute 与 symmetric-hull 三种 convention 的关系，为什么不能跨定义搬常数？

### LT-RAD-A03

陈述正文采用的 $[0,1]$ empirical Rademacher high-probability bound，并解释三个加项的角色。

## B. 手算与数值判断

### LT-RAD-B01

固定 $m=2$，restriction set $A=\{(0,0),(1,0),(0,1)\}$。枚举 signs，算出精确 empirical complexity。

### LT-RAD-B02

有限 restriction set 有 $M=100$ 个向量，每个 $\|a\|_2\le\sqrt{500}$，$m=500$。用 Massart lemma 计算上界。

### LT-RAD-B03

取 $m=10{,}000,\delta=0.05,\widehat{\mathfrak R}_S=0.03,P_mf=0.12$。用正文定理计算 $Pf$ 的 upper certificate。

## C. 推导与证明

### LT-RAD-C01

证明 empirical complexity 的单调性、正缩放、加固定函数不变与 convex-hull 不变。

### LT-RAD-C02

从 Rademacher MGF 完整推导 Massart finite-class lemma，优化 $\lambda$。

### LT-RAD-C03

给出 empirical Rademacher risk bound 的证明账本：symmetrization、gap concentration、empirical complexity concentration 与 Union Bound。无需追求比正文更好的常数。

## D. 边界、反例与纠错

### LT-RAD-D01

证明 singleton class 的 signed complexity 为 0，再构造一个 $[0,1]$ fixed function 使有限样本 empirical mean 仍随机。

### LT-RAD-D02

说明用 SGD 拟合 signs 得到的最大相关通常是 nominal class supremum 的下界。为什么把它直接放进 generalization upper bound 不合法？

### LT-RAD-D03

给出两个在训练 sample restrictions 完全相同、sample 外行为不同的函数。经验 complexity 能否区分它们？这是否使 theorem 错误？

## E. AI 迁移

### LT-RAD-E01

设计一个用 $B$ 组 signs 估计 linear-probe empirical complexity 的复现实验，列出 seed、optimization、Monte Carlo 与 statistical 四类记录。

### LT-RAD-E02

为什么对 neural network 用随机 labels 重新训练，得到的训练准确率不等于 Rademacher complexity？列出至少三项差异。

### LT-RAD-E03

对 architecture search 的最终赢家只计算一个 empirical complexity 是否足够？给出 simultaneous model-selection 修复方案。
