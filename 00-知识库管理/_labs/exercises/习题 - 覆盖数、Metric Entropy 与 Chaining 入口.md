---
type: exercise
status: draft
area: [learning-theory/metric-entropy, empirical-process/chaining]
topic: "[[覆盖数、Metric Entropy 与 Chaining 入口]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]", "[[度量空间、拓扑与连续映射]]"]
related: ["[[解答 - 覆盖数、Metric Entropy 与 Chaining 入口]]", "[[局部 Rademacher 复杂度与快收敛率]]"]
solution: "[[解答 - 覆盖数、Metric Entropy 与 Chaining 入口]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 覆盖数、Metric Entropy 与 Chaining 入口

> [!abstract] 训练目标
> 能在指定 metric/resolution 下计算 cover/packing，用单尺度 net 推出 complexity bound，解释 chaining telescoping 与 Dudley cutoff，并把 parameter geometry 合法传到 function geometry。

## A. 识别与复述

### LT-ENT-A01

定义 internal $\varepsilon$-cover、covering number、$\varepsilon$-packing、packing number 与 metric entropy。

### LT-ENT-A02

定义 empirical $L_2$ pseudometric $d_S$，解释为何不同函数的距离可以为 0。

### LT-ENT-A03

区分 metric entropy 与 Shannon entropy；说明两者的对象、输入与含义。

## B. 手算与数值判断

### LT-ENT-B01

在 $T=[0,1]$、Euclidean metric 下，以 internal closed balls 计算 $N(0.25,T,|\cdot|)$；给出一个最小 cover。

### LT-ENT-B02

固定样本 $(x_1,x_2)$，三个 restriction vectors 为 $(0,0),(1,0),(0,1)$。计算所有 pairwise $d_S$，并求 $\varepsilon=0.6$ 与 $0.8$ 时的 internal covering number。

### LT-ENT-B03

若 $m=400$、$A=1$、$N(\varepsilon)=1000$、$\varepsilon=0.05$，计算单尺度 bound
$$
\varepsilon+A\sqrt{2\log N(\varepsilon)/m}.
$$

## C. 推导与证明

### LT-ENT-C01

证明 $M(2\varepsilon)\le N(\varepsilon)\le M(\varepsilon)$，指出 maximal packing 在证明中的作用。

### LT-ENT-C02

从最近 net projection、Cauchy–Schwarz 与 Massart lemma 推导单尺度 cover bound。

### LT-ENT-C03

写出 dyadic nets 的 telescoping identity，证明 increment distance 至多 $3\varepsilon_k$，并解释离散和怎样近似 entropy integral。

## D. 边界、反例与纠错

### LT-ENT-D01

构造同一集合在两种 metric 下 covering number相差巨大的例子，反驳“covering number 是集合固有大小”。

### LT-ENT-D02

对 $\log N(\varepsilon)\asymp\varepsilon^{-p}$，分析 $p<2,p=2,p>2$ 时 entropy integral 在 0 附近的行为及 cutoff 作用。

### LT-ENT-D03

说明为什么 data-dependent empirical cover 可以合法，但用 labels 训练后挑一个小子类再当 fixed class 不一定合法。

## E. AI 迁移

### LT-ENT-E01

给定 $d_S(f_\theta,f_{\theta'})\le L_S\|\theta-\theta'\|_2$，证明 parameter cover transfer，并列出深网中使该 bound 过松的三类原因。

### LT-ENT-E02

为 vector-valued diffusion score 定义一个 empirical metric；说明 output norm、time/noise sampling 与 loss contraction怎样影响 cover。

### LT-ENT-E03

设计一个两层神经网络 entropy 审计清单：列出 layer norm、activation、input radius、parameter symmetry、output metric 与 cutoff 的角色。
