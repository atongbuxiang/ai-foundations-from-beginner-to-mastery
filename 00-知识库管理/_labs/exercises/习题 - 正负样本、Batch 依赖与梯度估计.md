---
type: exercise
status: draft
area: [learning-theory/contrastive-learning, batch-dependence, gradients]
topic: "[[正负样本、Batch 依赖与梯度估计]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[正负样本、Batch 依赖与梯度估计]]"]
related: ["[[解答 - 正负样本、Batch 依赖与梯度估计]]", "[[数据增强、不变性、等变性与任务充分性]]"]
solution: "[[解答 - 正负样本、Batch 依赖与梯度估计]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 正负样本、Batch 依赖与梯度估计

> [!abstract] 训练目标
> 能写two-view NT-Xent、推导softmax与embedding梯度，计算false-negative collision，区分objective/bias/variance，并审计hard sampler、queue与distributed all-gather。

## A. 识别与复述

### LT-BAT-A01

写出B个source units、2B views、positive index、eligible denominator与symmetric NT-Xent。

### LT-BAT-A02

区分false negative、dependent negative与stale negative。

### LT-BAT-A03

为什么batch size在contrastive learning中不只是Monte Carlo variance参数？

## B. 手算与数值判断

### LT-BAT-B01

anchor logits为$(2,1,0)$，第一项positive。计算probabilities、loss与每个logit gradient。

### LT-BAT-B02

balanced 10-class latent model中有63个iid negatives。求anchor至少遇到一个same-class negative的概率。

### LT-BAT-B03

two-class prior为$(0.8,0.2)$。求single-negative average collision $\sum\pi_c^2$，以及class-1 anchor在7 negatives中至少一次collision概率。

## C. 推导与证明

### LT-BAT-C01

推导$\partial\ell/\partial u_k=p_k-1\{k=+\}$以及dot-product下对anchor embedding的gradient。

### LT-BAT-C02

推导unit normalization $z=v/\|v\|$ 的Jacobian，并解释gradient为何落在sphere tangent。

### LT-BAT-C03

若negative proposal改为$q_\beta(y\mid x)$，写出importance weight；说明unknown normalizer/self-normalization如何引入问题。

## D. 边界、反例与纠错

### LT-BAT-D01

反驳“更多negatives一定更好”；从ceiling、hardness、collision、compute与dependence讨论。

### LT-BAT-D02

说明memory bank的encoder staleness为何不是iid current-negative sampling。

### LT-BAT-D03

同一用户多条记录随机分散到batch和test会造成什么objective/evaluation问题？

## E. AI 迁移

### LT-BAT-E01

为distributed SimCLR写sampler、all-gather、mask、gradient、loss-scale、seed与last-batch合同。

### LT-BAT-E02

为sentence embedding设计group-aware negative sampler，处理same-document、translation与near-duplicate false negatives。

### LT-BAT-E03

设计ablation矩阵：batch、temperature、hardness、debias prior、queue age；规定outer downstream与collision diagnostics。

