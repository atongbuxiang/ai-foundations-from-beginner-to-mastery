---
type: exercise
status: verified
area: [training, optimization, manifold-optimization, muon]
topic: "[[Stiefel、谱球面、旋转 Muon 与约束更新]]"
solution: "[[解答 - Stiefel、谱球面、旋转 Muon 与约束更新]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Stiefel、谱球面、旋转 Muon 与约束更新

> [!abstract] 训练目标
> 能推导 Stiefel tangent condition、Euclidean projection 与 polar retraction；严格区分 orthogonalized update、orthogonal parameter、spectral ball 和 fixed-singular-value orbit。

## A. 识别与复述

### TRN31-A01
分别定义 ambient matrix、orthogonalized update、Stiefel-constrained parameter 与左右正交 orbit update。

### TRN31-A02
给出 $\operatorname{St}(m,p)$、其 tangent space 和 embedded Euclidean metric 下的 tangent projection。

### TRN31-A03
区分 tangent step、retraction、exponential map 与 exact feasible rotation；它们在局部阶数和计算成本上有何不同？

## B. 手算与构造

### TRN31-B01
令 $W=I_2$，候选方向
$$
\Xi=\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$
验证 $\Xi$ 是 tangent；计算 $(W+\eta\Xi)^T(W+\eta\Xi)$，说明直接 Euler step 的 feasibility error。

### TRN31-B02
令 $W=(1,0)^T\in\operatorname{St}(2,1)$，ambient gradient $G=(2,3)^T$。计算 $\Pi_W(G)=G-W\operatorname{sym}(W^TG)$，并验证 tangent condition。

### TRN31-B03
令 $W=\operatorname{diag}(3,1)$，$Q_L,Q_R$ 为任意 $2\times2$ rotation。计算 $W_+=Q_LWQ_R^T$ 的 singular values、Frobenius norm、spectral norm 与 determinant magnitude。

## C. 推导与证明

### TRN31-C01
从约束曲线 $W(t)^TW(t)=I$ 求导，推出 tangent condition $W^T\Xi+\Xi^TW=0$。

### TRN31-C02
证明 $\Pi_W(G)=G-W\operatorname{sym}(W^TG)$ 位于 tangent space，并证明 normal component 为 $W\operatorname{sym}(W^TG)$。

### TRN31-C03
证明 polar retraction
$$
R_W(\Xi)=(W+\Xi)[(W+\Xi)^T(W+\Xi)]^{-1/2}
$$
精确满足列正交，并验证 $R_W(0)=W$ 与一阶导为 identity on tangent space。

## D. 边界、反例与纠错

### TRN31-D01
用 $W=I,Q=I$ 反驳“若 update $Q$ 正交，则 $W-\eta Q$ 仍正交”。给出任意 $\eta\ne0,2$ 的结果。

### TRN31-D02
反驳“固定奇异值轨道不会损失表达能力”。构造目标矩阵 $W_\star=\operatorname{diag}(2,2)$ 与初值 $\operatorname{diag}(3,1)$，说明任何双旋转都无法到达。

### TRN31-D03
为什么一篇九天前发布的 Stiefel 解析推导不能直接升级为成熟工程结论？按 theorem verification、numerical stability、complexity、implementation 和 replication 分层回答。

## E. AI 迁移

### TRN31-E01
为 orthogonal linear layer 设计训练 step：ambient gradient、projection、optimizer state、retraction 与 mixed-precision feasibility correction 应如何排序？

### TRN31-E02
设计数值测试比较 Euler tangent step、QR retraction、polar retraction 与 Cayley/exponential update。写出 feasibility、distance、loss decrease、cost 与 reversibility 指标。

### TRN31-E03
为普通 Muon、Stiefel-Muon 与双旋转 Muon 设计 controlled ablation。哪些参数集合、不变量和 baseline 必须分别声明？

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。先验证 tangent 与 finite feasibility 是两道不同的门，再打开 [[解答 - Stiefel、谱球面、旋转 Muon 与约束更新]]。
