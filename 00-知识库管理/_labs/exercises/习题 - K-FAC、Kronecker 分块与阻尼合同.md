---
type: exercise
status: verified
area: [training, optimization, curvature]
topic: "[[K-FAC、Kronecker 分块与阻尼合同]]"
solution: "[[解答 - K-FAC、Kronecker 分块与阻尼合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - K-FAC、Kronecker 分块与阻尼合同

> [!abstract] 训练目标
> 从线性层的 exact sample outer product 推到 K-FAC moment factorization；能核对 vec convention、inverse apply、factor damping 的额外交叉项与生产系统的三只时钟。

## A. 识别与复述

### TRN22-A01
对 $s=Wa$、$\delta=\partial\ell/\partial s$，写出样本 gradient、column-major vectorization 和其 exact outer product。近似从哪一步才开始？

### TRN22-A02
K-FAC 删除了哪两类结构：同一 layer 内的 factor dependence 与 layer 之间的 blocks？为什么“activation 与 gradient 独立”只能作简写？

### TRN22-A03
列出 factor-statistics update、inverse/eigen refresh、preconditioner apply 三只时钟及其主要 state；解释 stale preconditioner 从何而来。

## B. 手算与构造

### TRN22-B01
取 $a=(1,2)^\top$、$\delta=(3,-1)^\top$。计算 $\nabla_W\ell=\delta a^T$、column-major `vec`，并验证它等于 $a\otimes\delta$。

### TRN22-B02
令 $A=\operatorname{diag}(4,1)$、$S=\operatorname{diag}(9,1)$、$G=\begin{bmatrix}6&2\\3&1\end{bmatrix}$。计算 $S^{-1}GA^{-1}$，并解释左右 factor 各校正哪个空间。

### TRN22-B03
在一维 factor toy 中，两样本的 $(a^2,\delta^2)$ 分别为 $(1,1)$ 与 $(4,4)$。计算 $\mathbb E[a^2\delta^2]$ 和 $\mathbb E[a^2]\mathbb E[\delta^2]$，量化 K-FAC moment factorization error。

## C. 推导与证明

### TRN22-C01
证明 $(a\otimes\delta)(a\otimes\delta)^T=(aa^T)\otimes(\delta\delta^T)$，并核对左右矩阵 shape。

### TRN22-C02
在 column-major convention 下证明
$$ (A^{-1}\otimes S^{-1})\operatorname{vec}(G)=\operatorname{vec}(S^{-1}GA^{-T}). $$

### TRN22-C03
展开 $(A+\alpha I)\otimes(S+\beta I)$，证明即使 $\alpha\beta=\lambda$ 也一般不等于 $A\otimes S+\lambda I$；指出 exact eigenbasis damping 如何处理 eigenvalue。

## D. 边界、反例与纠错

### TRN22-D01
构造 activation 与 backprop factor 强相关的样本分布，使 K-FAC factorization 有非零偏差；说明更多样本会收敛到哪个对象。

### TRN22-D02
反驳：“K-FAC state 一定是 $O(P)$。”用方形 $d\times d$ layer 比较参数量、factor 元素、inverse cache 与 block splitting。

### TRN22-D03
解释卷积/attention 中把 token 或空间位置当额外样本、先聚合再 outer product、保留 cross-location terms 三种 convention 会怎样改变尺度与 rank。

## E. AI 迁移

### TRN22-E01
设计 K-FAC layer card，覆盖 vec convention、bias、factor reduction、EMA、damping、inverse residual、refresh period、weight sharing 与 distributed layout。

### TRN22-E02
设计一个 numerical unit test，同时验证 exact sample Kronecker identity、moment factorization error 与 exact/factored damping mismatch。

### TRN22-E03
如何公平比较 K-FAC 与 AdamW？除质量外，列出 factor 计算、通信、peak memory、refresh tail latency、失败运行与调参预算字段。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。所有矩阵式都必须标 shape 与 vec convention，完成后打开 [[解答 - K-FAC、Kronecker 分块与阻尼合同]]。
