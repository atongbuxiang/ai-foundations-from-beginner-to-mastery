---
type: solution
status: draft
area: [architecture, graph-neural-networks, expressivity]
topic: "[[聚合器、可辨识性与 Graph Isomorphism Network]]"
exercise: "[[习题 - 聚合器、可辨识性与 Graph Isomorphism Network]]"
sources: ["[[S-2019-Xu-GIN]]", "[[S-2017-Zaheer-Deep-Sets]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 聚合器、可辨识性与 Graph Isomorphism Network

## A. 识别与复述

### ARCH-GIN-A01
在定义域 $\mathcal M$ 上，$a$ injective 指 $X\ne Y\Rightarrow a(X)\ne a(Y)$。若 $a(X)=a(Y)$，任何后续确定函数 $f$ 都给 $f(a(X))=f(a(Y))$，所以 MLP 无法知道输入原来是哪一个多重集。

### ARCH-GIN-A02
Mean 保留平均/比例但丢整体重复倍数；max 保留各坐标极值但丢计数、次大和未胜出元素；sum 保留 count scale，但裸 sum 仍有加和碰撞，需配合合适 $\phi$ 才可能 injective。

### ARCH-GIN-A03
$h_i^{(k)}=\mathrm{MLP}^{(k)}((1+\epsilon^{(k)})h_i^{(k-1)}+\sum_{j\in N(i)}h_j^{(k-1)})$。$1+\epsilon$ 使中心角色与邻居 sum 组合时可区分；$\epsilon$ 可固定或学习，不是概率权重。

## B. 手算与建模

### ARCH-GIN-B01
例如 $X=\{(0,0),(2,2)\}$ 与 $Y=\{(0,0),(0,0),(2,2),(2,2)\}$，两者 mean 都是 $(1,1)$，cardinality 分别 2、4。

### ARCH-GIN-B02
例如 $X=\{(1,3),(3,1)\}$，$Y=\{(3,3),(0,0)\}$，逐坐标 max 都是 $(3,3)$，但支持元素完全不同。

### ARCH-GIN-B03
中心项 $(1+0.5)\cdot2=3$，邻居 sum $1+1+3=5$，MLP 输入 8；恒等 MLP 输出 8。

## C. 推导与证明

### ARCH-GIN-C01
若 $X$ 有 $m$ 个元素，复制 $k$ 次后的 sum 为 $k\sum_{x\in X}x$，元素数为 $km$，mean 为 $k\sum x/(km)=\sum x/m$。

### ARCH-GIN-C02
标签编号 $r\in\{0,\ldots,q-1\}$，最大 multiplicity $M$。取基数 $B=M+1$，令 $\phi(r)=B^r$。Sum 的 $B$ 进制各位就是每个标签的计数 $0\ldots M$，无进位，故唯一编码该多重集。数值会随 $q$ 指数增长，此为存在性构造而非实际推荐。

### ARCH-GIN-C03
把第 $t$ 轮 WL color 映为表示。Injective aggregation 唯一编码邻居 color multiset，中心项保留自身 color；injective update 唯一编码二者 pair，因此新表示相等当且仅当 WL 新颜色相等。Graph-level injective multiset readout 再唯一编码最终颜色 histogram。

## D. 边界、反例与纠错

### ARCH-GIN-D01
$\{1,3\}$ 与 $\{2,2\}$ 裸 sum 都为 4，却是不同多重集。因此能力来自 $\sum\phi(x)$ 在受限域上的构造，不是加号本身。

### ARCH-GIN-D02
GIN 上界仍是 1-WL。统一初始标签下，六环与两个不相连三角形每个节点永远看到两个同色邻居，1-WL 和相应 GIN 都不能区分。名字不是一般同构保证。

### ARCH-GIN-D03
普通 LSTM 对输入顺序敏感；同一多重集的两个随机排列在一次 forward 中可给不同值。训练时随机化可能学到近似平均鲁棒性，但不提供逐次 $f(\pi X)=f(X)$ 的结构保证。

## E. AI 迁移

### ARCH-GIN-E01
生成成对多重集：复制倍数、相同 max 不同支持、相同裸 sum、相同 cardinality 不同分布；训练各 aggregator 预测 count/histogram/parity。对齐 width/MLP/steps，报告训练可拟合率与未见 cardinality 泛化，并直接统计 collision。

### ARCH-GIN-E02
构造 sum 极近但不同的连续向量、大小差异巨大的正负抵消、多邻居累加；以 float64/reference 比 float32/bfloat16，测试邻居排列、不同 scatter order、gradient finite difference、MLP saturation；报告 absolute/relative tolerance 与输出 margin。

### ARCH-GIN-E03
固定 encoder depth/total hidden budget/readout/optimizer/split/seeds；若 aggregator 参数量不同，用 matched-parameter 版本并同时报告原生版本；记录 FLOPs/memory；加入 synthetic collision probes、size-stratified test 和多次重复，避免只在一个数据集按最高 validation 选不同搜索预算。

