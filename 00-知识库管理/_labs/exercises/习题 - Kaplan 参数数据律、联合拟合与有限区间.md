---
type: exercise
status: verified
area: [training, scaling-laws, language-models]
topic: "[[Kaplan 参数数据律、联合拟合与有限区间]]"
solution: "[[解答 - Kaplan 参数数据律、联合拟合与有限区间]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Kaplan 参数数据律、联合拟合与有限区间

> [!abstract] 训练目标
> 能区分参数律、数据律、算力律与联合曲面，识别 undertraining、参数计数和有限尺度区间造成的伪指数。

## A. 识别与复述

### TRN50-A01
分别定义 $N,D,C,T$，并说明“训练步数”“训练 token 数”和“训练 FLOPs”为什么不能互换。

### TRN50-A02
区分 marginal fit $L(N)$、$L(D)$ 与 joint fit $L(N,D)$。两条边际幂律为何不足以唯一确定一个联合曲面？

### TRN50-A03
什么是 optimization gap $G(N,D,T)$？为什么未训练充分的点不应直接解释为架构或数据的统计极限？

## B. 手算与构造

### TRN50-B01
设联合模型
$$
L(N,D)=1+3N^{-0.2}+5D^{-0.3}.
$$
计算 $(N,D)=(1,1),(32,1),(1,100),(32,100)$ 的 loss，并判断每个角落由哪一瓶颈主导。

### TRN50-B02
一个小模型含 1 亿 non-embedding 参数和 5000 万 embedding 参数，大模型含 10 亿 non-embedding 参数和同样的 5000 万 embedding 参数。若横轴分别用 total 与 non-embedding 参数，计算两模型的尺度比。

### TRN50-B03
构造一条路径 $D=N^{1/2}$。把上式限制到该路径后写成 $L(N)$，说明为什么单条对角路径会把两个瓶颈混在一个表观斜率中。

## C. 推导与证明

### TRN50-C01
对 $L=E+AN^{-\alpha}+BD^{-\beta}$ 推导关于 $\log N$ 的局部斜率，并说明它依赖数据瓶颈与 offset。

### TRN50-C02
若实际观测为 $L_{obs}=L_\infty(N,D)+G(N,D,T)$，且较大模型的 $G$ 更大，论证忽略 $G$ 时参数缩放收益为何会被低估。

### TRN50-C03
证明只观测 $D=kN^p$ 时，无法稳健地区分 $AN^{-\alpha}$ 与 $Bk^{-\beta}N^{-p\beta}$，尤其当 $\alpha\approx p\beta$。

## D. 边界、反例与纠错

### TRN50-D01
反驳：“固定训练步数比较不同 batch size 与 sequence length，就是固定数据量的参数律。”

### TRN50-D02
为什么“小尺度上 embedding 占比高”会扭曲 total-parameter 横轴的指数？指出向更大尺度外推时的风险。

### TRN50-D03
某研究对每个规模单独做无限超参搜索，却把搜索成本排除在 compute 中。说明它的科学问题与资源规划问题分别该如何报告。

## E. AI 迁移

### TRN50-E01
设计一个至少 $4\times4$ 的 $N$–$D$ crossed grid，并说明怎样加入 checkpoint 维度以估计 $G(N,D,T)$。

### TRN50-E02
给出一个 Kaplan 风格结果的复现审计表：至少覆盖参数计数、token 计数、训练充分度、超参和 loss 口径。

### TRN50-E03
面对两篇指数不一致的论文，写出调和顺序：先比较哪些对象、区间、路径和拟合选择，再讨论是否存在真实矛盾？

## 作答与复盘

先把每条 scaling claim 投影到 $(N,D,T,C)$ 四维账本，再查看 [[解答 - Kaplan 参数数据律、联合拟合与有限区间]]。
