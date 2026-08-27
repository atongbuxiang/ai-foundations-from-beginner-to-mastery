---
type: exercise
status: verified
area: [training, scaling-laws, compute-optimal]
topic: "[[Chinchilla、Compute-optimal 参数与数据分配]]"
solution: "[[解答 - Chinchilla、Compute-optimal 参数与数据分配]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Chinchilla、Compute-optimal 参数与数据分配

> [!abstract] 训练目标
> 从联合损失面与算力约束独立推导 compute-optimal allocation，理解最优比例依赖指数、系数、可行域与成本口径。

## A. 识别与复述

### TRN51-A01
解释“固定训练算力下最优”“固定 token 下最优”和“固定部署需求下最优”的区别。

### TRN51-A02
对 $L=E+AN^{-\alpha}+BD^{-\beta}$ 与 $C=\kappa ND$，写出最优点的边际平衡条件，并用语言解释。

### TRN51-A03
什么是 IsoFLOP 曲线？它与在一个固定 $C$ 上只比较两个模型有什么证据差异？

## B. 手算与构造

### TRN51-B01
设 $\alpha=\beta=1/2$、$A=B=1$、$\kappa=1$、$C=10^4$。求连续最优 $N^*,D^*$ 与 excess loss。

### TRN51-B02
设 $\alpha=0.34,\beta=0.28$。计算 $N^*$、$D^*$ 对 $C$ 的幂指数，以及 tokens-per-parameter 比 $D^*/N^*$ 对 $C$ 的幂指数。

### TRN51-B03
在 $C=10^4$、$L-E=N^{-1/2}+D^{-1/2}$ 下，比较 $(N,D)=(100,100),(25,400),(400,25)$，说明最优附近偏离的代价。

## C. 推导与证明

### TRN51-C01
用代入法从 $D=C/(\kappa N)$ 完整推导
$$
N^*\propto C^{\beta/(\alpha+\beta)},\qquad
D^*\propto C^{\alpha/(\alpha+\beta)}.
$$

### TRN51-C02
证明最优 excess loss 随算力满足
$$
L^*(C)-E\propto C^{-\alpha\beta/(\alpha+\beta)}.
$$

### TRN51-C03
由一阶条件推导最优点处两项损失的比例，并说明为什么一般不是 $AN^{-\alpha}=BD^{-\beta}$。

## D. 边界、反例与纠错

### TRN51-D01
反驳：“Chinchilla 证明了所有模型都应训练 20 tokens/parameter。”至少列出四个改变最优比率的因素。

### TRN51-D02
为什么连续最优解不能直接成为可执行配置？从可用数据、硬件并行、整数 shape 和训练稳定性说明。

### TRN51-D03
某 IsoFLOP 曲线很平。为什么报告单个 argmin 会制造虚假精度？应报告什么替代对象？

## E. AI 迁移

### TRN51-E01
为三个算力预算设计 IsoFLOP 扫描，每个预算至少五个 $N$–$D$ 配置；说明怎样避免把超参失配当成资源失配。

### TRN51-E02
给定拟合参数的 bootstrap 样本，说明如何把不确定性传播到 $N^*(C),D^*(C)$ 与近优集合。

### TRN51-E03
写一段研究结论，同时区分连续模型的数学最优、实验网格的观测最优和工程可行的最终选择。

## 作答与复盘

不得背诵“等比例增长”；必须从拉格朗日或代入法重推，再查看 [[解答 - Chinchilla、Compute-optimal 参数与数据分配]]。
