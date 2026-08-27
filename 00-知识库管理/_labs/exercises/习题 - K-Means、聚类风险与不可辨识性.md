---
type: exercise
status: draft
area: [learning-theory/k-means, clustering, unsupervised-learning]
topic: "[[K-Means、聚类风险与不可辨识性]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[K-Means、聚类风险与不可辨识性]]"]
related: ["[[解答 - K-Means、聚类风险与不可辨识性]]", "[[潜变量模型、混合模型与 EM]]"]
solution: "[[解答 - K-Means、聚类风险与不可辨识性]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - K-Means、聚类风险与不可辨识性

> [!abstract] 训练目标
> 区分 population objective、empirical global minimizer与 Lloyd iterate；能证明 assignment/update单调性，使用 permutation-invariant loss，并为无监督表示、routing与伪标签设计不自证循环的评价。

## A. 识别与复述

### LT-KMEANS-A01

写出 population K-Means risk与 empirical distortion；区分 unordered centers、Voronoi partition、global minimizer与 Lloyd algorithm输出。

### LT-KMEANS-A02

解释 label permutation、empty cluster、duplicate centers与multiple global optima分别造成什么不唯一性。

### LT-KMEANS-A03

比较 internal metric、external metric与 downstream utility。为什么 silhouette较高不等于发现了真实语义类别？

## B. 手算与数值判断

### LT-KMEANS-B01

对一维数据 (0,2,9,11)，(K=2)，初始 centers为 (0,9)。执行一轮 assignment与update，计算更新前后 distortion；再给出global optimum及其distortion。

### LT-KMEANS-B02

证明 fixed nonempty cluster (A) 的 squared-distance center为 sample mean，并计算 (A=\{2,9,11\}) 时的最佳center与 within-cluster sum of squares。

### LT-KMEANS-B03

真实 unordered centers (C^\star=\{(0,0),(10,0)\})，估计输出按相反编号写为 (\widehat C=\{(10.5,0),(0.5,0)\})。计算 naive index-wise squared error与 permutation-matched squared error。

## C. 推导与证明

### LT-KMEANS-C01

证明 Lloyd assignment step 与 nonempty-cluster mean update step都不增加 empirical distortion。为什么这只证明objective values单调，不证明global optimality？

### LT-KMEANS-C02

证明 K-Means risk对center permutation不变，并给出 permutation-invariant center loss。若population minimizer不唯一，普通“收敛到 (C^\star)”应如何改写？

### LT-KMEANS-C03

把 empirical-risk consistency 的证明架构拆成：uniform convergence、population separation/uniqueness与argmin transfer。指出 Lloyd local search为何不能直接继承 global ERM consistency。

## D. 边界、反例与纠错

### LT-KMEANS-D01

给出一个 Lloyd 因初始化停在差local optimum的例子或几何解释。k-means++改善的是什么，不能保证什么？

### LT-KMEANS-D02

构造一个 feature rescaling会改变聚类的例子。为什么standardization也不是自动正确？

### LT-KMEANS-D03

反驳“cluster id就是潜在真实类别”。至少讨论geometry、representation、(K)、symmetry与task dependence。

## E. AI 迁移

### LT-KMEANS-E01

为 embedding vector quantization设计训练与评价协议：codebook usage、distortion、dead codes、restarts、downstream utility与distribution shift。

### LT-KMEANS-E02

为 mixture-of-experts router 的hard routing使用K-Means初始化，说明如何避免把同一 validation signal用于初始化选择与最终评价。

### LT-KMEANS-E03

写一份聚类实验报告最小字段：representation、metric、scaling、(K)、initialization、global/local gap、stability、external labels、downstream test与伦理风险。
