---
type: exercise
status: draft
area: [neural-networks/activations, maxout]
topic: "[[Maxout、分段线性区域与条件计算]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Maxout、分段线性区域与条件计算]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Maxout、分段线性区域与条件计算
## A
### NN-MAX-A01
写出 rank-$k$ maxout 的定义与 batch tensor shapes。
### NN-MAX-A02
区分 unique winner gradient、tie subdifferential 与 framework convention。
### NN-MAX-A03
解释 gradient routing 与 forward conditional compute 的差别。
## B
### NN-MAX-B01
求 $h(x)=\max(x,-x,1)$ 的分段公式、winner regions 与 ties。
### NN-MAX-B02
给两个 tied affine candidates 和方向 $v$，计算 directional derivative。
### NN-MAX-B03
比较 dense layer 与 $k=4$ maxout layer 的参数、MAC 与 candidate storage。
## C
### NN-MAX-C01
证明 pointwise maximum of affine functions 为 convex。
### NN-MAX-C02
证明 winner region 是 polyhedron，并说明 candidate 可永不获胜。
### NN-MAX-C03
证明 ReLU 是固定 maxout 特例；构造 unit convex 但网络整体 nonconvex 的例子。
## D
### NN-MAX-D01
反驳“$k$ candidates 必产生 $k$ 个可见 pieces”。
### NN-MAX-D02
反驳“backward 只给 winner 梯度，所以 forward 节省 $k$ 倍计算”。
### NN-MAX-D03
说明 finite difference 在 tie 附近为何不稳定，并设计正确测试。
## E
### NN-MAX-E01
为 Maxout kernel 设计 permutation、tie、NaN 与 determinism 验收。
### NN-MAX-E02
设计 winner starvation 与 margin 监测。
### NN-MAX-E03
比较 Maxout、MoE top-$k$ routing 与 ReLU sparsity 的计算语义。
## 解答入口
[[解答 - Maxout、分段线性区域与条件计算]]
