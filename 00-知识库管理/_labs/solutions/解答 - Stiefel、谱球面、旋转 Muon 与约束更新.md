---
type: solution
status: verified
area: [training, optimization, manifold-optimization, muon]
topic: "[[Stiefel、谱球面、旋转 Muon 与约束更新]]"
exercise: "[[习题 - Stiefel、谱球面、旋转 Muon 与约束更新]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Stiefel、谱球面、旋转 Muon 与约束更新

> [!warning] 使用边界
> update 的列/行关系、direction 的 tangent feasibility 与 parameter 的 finite-step feasibility 是三件事。每次证明都先写 constraint set 和 metric。

## A. 识别与复述

### TRN31-A01
ambient matrix 是无约束 Euclidean space 中的 $W$；orthogonalized update 是某个 $\Delta$ 满足 $\Delta^T\Delta\approx I$ 或 $\Delta\Delta^T\approx I$；Stiefel parameter 要求当前及每步后 $W^TW=I$；orbit update $Q_LWQ_R^T$ 由左右正交 action 生成，固定 $W$ 的全部 singular values。四者分别是环境空间、方向性质、参数流形与群轨道。

### TRN31-A02
$$
\operatorname{St}(m,p)=\{W:W^TW=I_p\},
$$
$$
T_W\operatorname{St}(m,p)
=\{\Xi:W^T\Xi+\Xi^TW=0\}.
$$
embedded Euclidean metric 下
$$
\Pi_W(G)=G-W\operatorname{sym}(W^TG).
$$
换 canonical/其他 metric 时 Riemannian gradient 表达可能不同。

### TRN31-A03
tangent step 只是一阶可行方向；retraction 是满足 $R_W(0)=W$、一阶导为 identity 的局部回映，有限步精确落在流形；exponential map沿指定 Riemannian metric 的 geodesic，通常更贵；exact rotation 用群作用保持特定不变量，但可行集合可能比整个 Stiefel 或 ambient space更小。局部一阶相同不表示 finite path/cost 相同。

## B. 手算与构造

### TRN31-B01
$\Xi^T=-\Xi$，所以在 $W=I$：
$$
W^T\Xi+\Xi^TW=\Xi+\Xi^T=0.
$$
但
$$
(I+\eta\Xi)^T(I+\eta\Xi)
=I+\eta(\Xi+\Xi^T)+\eta^2\Xi^T\Xi
=(1+\eta^2)I.
$$
feasibility error 是二阶的，但只要 $\eta\ne0$ 就非零。

### TRN31-B02
$W^TG=2$，一维对称化仍为 2：
$$
\Pi_W(G)=(2,3)^T-(1,0)^T2=(0,3)^T.
$$
对 $p=1$，tangent condition 等价于 $W^T\Xi=0$；这里等于 0。

### TRN31-B03
左右乘正交矩阵不改变 singular values，所以仍为 $(3,1)$。因此
$$
\lVert W_+\rVert_F=\sqrt{10},\quad
\lVert W_+\rVert_2=3,\quad
|\det W_+|=|\det W|=3.
$$
determinant 的符号可由 $\det Q_L\det Q_R$ 改变，但 magnitude 保持。

## C. 推导与证明

### TRN31-C01
对 $W(t)^TW(t)=I$ 求导：
$$
\dot W(t)^TW(t)+W(t)^T\dot W(t)=0.
$$
令 $t=0$、$\Xi=\dot W(0)$，得
$$
\Xi^TW+W^T\Xi=0.
$$
它意味着 $W^T\Xi$ skew-symmetric。

### TRN31-C02
令 $S=\operatorname{sym}(W^TG)$。则
$$
W^T(G-WS)+(G-WS)^TW
=W^TG+G^TW-2S=0,
$$
所以投影结果 tangent。normal component $WS$ 的 $S$ 对称；对任意 tangent $\Xi$，
$$
\langle WS,\Xi\rangle_F
=\operatorname{tr}(S W^T\Xi)=0,
$$
因为 symmetric 与 skew-symmetric 矩阵的 Frobenius pairing 为零。

### TRN31-C03
设 $A=W+\Xi$ 且 $A^TA\succ0$：
$$
R^TR
=(A^TA)^{-1/2}A^TA(A^TA)^{-1/2}=I.
$$
$\Xi=0$ 时 $R=W(W^TW)^{-1/2}=W$。对 tangent $t\Xi$，
$$
(W+t\Xi)^T(W+t\Xi)=I+t^2\Xi^T\Xi,
$$
故 inverse square root 为 $I+O(t^2)$，于是
$$
R_W(t\Xi)=W+t\Xi+O(t^2).
$$
一阶导确为 $\Xi$。

## D. 边界、反例与纠错

### TRN31-D01
$W-\eta Q=(1-\eta)I$，所以
$$
(W-\eta Q)^T(W-\eta Q)=(1-\eta)^2I.
$$
只有 $\eta=0$ 或 $\eta=2$ 时等于 $I$；一般小 learning rate 反而明确不在 Stiefel 上。$Q$ 自身正交没有提供 $W^TQ+Q^TW=0$。

### TRN31-D02
任何 $Q_L\operatorname{diag}(3,1)Q_R^T$ 的 singular values 都是 $(3,1)$；目标 $\operatorname{diag}(2,2)$ 的 singular values 为 $(2,2)$。singular values 是左右正交轨道的完备不变量之一，故目标不在该轨道。固定谱会删掉学习 gain/condition 的能力。

### TRN31-D03
先逐式核验 norm/metric、rank、inverse/root 存在与最优性；再对病态/低精度矩阵测 residual 和稳定性；展开 SVD/root/solve 的 FLOPs、memory、communication；需要公开且版本化实现；最后才看多任务、硬件、seed 的独立复现。发布日期极近只表示尚缺积累，不表示推导错误，但工程结论必须降级。

## E. AI 迁移

### TRN31-E01
建议顺序：得到 unscaled ambient gradient并完成 distributed reduction；按所选 metric/projector 得 tangent gradient；在 tangent state 表示下更新 momentum/optimizer state，必要时 vector transport；形成 tangent step；用稳定的 polar/QR retraction回到流形；在 master precision 检查/修正 feasibility；最后同步低精度参数。weight decay 若会离开流形，必须改成流形内 regularizer，而非机械乘缩。

### TRN31-E02
固定相同 tangent $\Xi$ 和步长网格。比较：

- $r_{feas}=\lVert W_+^TW_+-I\rVert$；
- 与 exponential/reference 的 geodesic/chordal distance；
- predicted vs actual loss decrease；
- first-order direction cosine；
- FLOPs、wall-clock、peak、backward cost；
- forward/backward round-trip 或 reversibility（适用时）；
- FP64/训练 dtype residual；
- tall/wide/near-rank-loss shapes。

Euler 是非可行 baseline；QR/polar 的 sign convention 也要固定。

### TRN31-E03
普通 Muon：ambient $W$，只约束/近似 update polar；Stiefel-Muon：parameter set 为 $W^TW=I$，需 tangent/retraction；双旋转：parameter 位于固定 singular-value orbit。共享模型/data/search budget，但 capacity 不同，应另报 parameter/function constraint。baseline 至少含 unconstrained AdamW/Muon、标准 Riemannian SGD/Adam。报告 feasibility、singular spectra、quality、cost 与失败 runs。

## 无提示重做

- [ ] 48 小时后推导 tangent projection 与 polar retraction。
- [ ] 一周后用 $W=I,Q=I$ 和不匹配 singular spectra 两个反例解释两类约束错误。
