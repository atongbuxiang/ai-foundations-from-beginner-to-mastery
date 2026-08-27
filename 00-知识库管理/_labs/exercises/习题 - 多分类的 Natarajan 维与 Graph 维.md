---
type: exercise
status: draft
area: [learning-theory/vc, learning-theory/multiclass]
topic: "[[多分类的 Natarajan 维与 Graph 维]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[二分类统计学习基本定理]]", "[[打散、增长与 VC 维]]"]
related: ["[[解答 - 多分类的 Natarajan 维与 Graph 维]]", "[[实值函数类、伪维与阈值化]]"]
solution: "[[解答 - 多分类的 Natarajan 维与 Graph 维]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 多分类的 Natarajan 维与 Graph 维

> [!abstract] 训练目标
> 能用见证函数逐点检验 multiclass shattering，证明 Natarajan/Graph/VC 的关系，把 Graph 维映射到扩展域 error class，并判断多分类 ERM 与 surrogate 声明的边界。

## A. 识别与复述

### LT-MC-A01

写出 Natarajan shattering 的完整量词和两个见证函数。哪些对象可依赖 desired subset $T$，哪些不可？

### LT-MC-A02

写出 Graph shattering 定义，并解释“补集上不等于 reference”为什么弱于“补集上等于预先固定的第二标签”。

### LT-MC-A03

分别解释 class PAC learnable、存在 good ERM、指定 ERM learnable、任意 ERM learnable 四个命题。

## B. 手算与数值判断

### LT-MC-B01

设 $\mathcal X=\{a,b\}$、$\mathcal Y=\{0,1,2\}$，$\mathcal H$ 含全部从 $\mathcal X$ 到 $\mathcal Y$ 的函数。计算 $d_N,d_G$，并写出打散两个点的一组 Natarajan 见证。

### LT-MC-B02

设 $\mathcal H=\{h_y:h_y(x)\equiv y,\ y\in\mathcal Y\}$ 且 $|\mathcal Y|=1000$。计算 $d_N,d_G$，说明为何不是 $\log_2 1000$。

### LT-MC-B03

已知有限标签类 $d_N=20,K=100$，只按 $d_G=O(d_N\log_2K)$ 估计其量级。计算 $d_N\log_2K$，并说明该数不是无常数的精确 $d_G$。

## C. 推导与证明

### LT-MC-C01

从 Natarajan 见证 $f_0,f_1$ 构造 Graph reference，证明 $d_N\le d_G$。

### LT-MC-C02

证明当 $|\mathcal Y|=2$ 时 $d_N=d_G=\operatorname{VCdim}$。

### LT-MC-C03

定义 $G_h=\{(x,y):h(x)=y\}$。证明 Graph shattering 等价于 set class $\{G_h\}$ 在扩展域上的 VC shattering，并说明 error set 取补为何不改变维数。

## D. 边界、反例与纠错

### LT-MC-D01

给出一个点集上“每点各能取两个标签”但无法联合实现全部 $2^m$ 模式的 class，说明逐点丰富不等于 Natarajan shattering。

### LT-MC-D02

有人把 $d_N$ 直接代入 binary 0–1 VC bound 来证明无界 cross-entropy uniform convergence。指出至少三个断点。

### LT-MC-D03

说明 infinite/open label space 下为什么不能无条件使用 $d_G=O(d_N\log K)$，并提出两个可能的替代结构假设。

## E. AI 迁移

### LT-MC-E01

对一个 50,000-token softmax 模型，分别写出 label space、score class、argmax class、loss class。指出 Natarajan/Graph 维直接对应哪一个。

### LT-MC-E02

一个分类器在多个训练误差相同的标签外推规则间 tie。设计实验检查 tie-breaking 是否改变 unseen-class/rare-class 风险，并说明理论上它属于 class 还是 learner。

### LT-MC-E03

把层级标签分类或序列 exact-match 任务改写成完整对象合同，解释为什么 flat multiclass 0–1 theorem 可能过粗。
