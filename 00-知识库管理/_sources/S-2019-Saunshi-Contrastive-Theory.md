---
type: source
status: active
area: [sources, contrastive-learning, latent-classes, downstream-risk]
source_type: paper
title: "A Theoretical Analysis of Contrastive Unsupervised Representation Learning"
author: [Nikunj Saunshi, Orestis Plevrakis, Sanjeev Arora, Mikhail Khodak, Hrishikesh Khandeparkar]
year: 2019
url: "https://proceedings.mlr.press/v97/saunshi19a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "ICML 2019"
scope_role: primary
temporal_role: modern-theory
related: ["[[正负样本、Batch 依赖与梯度估计]]", "[[表示学习的任务、表示与下游风险]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Theoretical Analysis of Contrastive Unsupervised Representation Learning

> [!abstract] 来源定位
> 在 latent-class sampling model 下把 contrastive objective 连接到 average downstream classification task，并显式出现 class collision。本库用它展示 pretext-to-downstream 定理必须写出生成模型与 task restriction。

## 本库调用

1. positive-pair law 假设 same latent class；
2. negatives 来自 class mixture 并可能 collision；
3. guarantee 覆盖特定 average downstream tasks；
4. representation class complexity 进入 generalization；
5. latent-class theorem 不能直接证明任意 augmentation 或 task 有效；
