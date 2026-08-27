---
type: derivation
status: verified
area: [training, optimization, manifold-optimization, muon]
node_id: TRN-31
aliases: [Stiefel Muon, Orthogonal Parameter Updates]
prerequisites: ["[[Riemann 几何、测地线与流形优化]]", "[[极分解]]", "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]"]
related: ["[[Newton–Schulz Matrix Sign 的收敛与有限精度]]", "[[Muon 的扩展证据、系统成本与迁移边界]]", "[[极分解]]", "[[正交投影]]"]
sources: ["[[S-2008-Absil-Matrix-Manifolds]]", "[[S-2025-Su-11196-流形最速下降超球面]]", "[[S-2025-Su-11215-Muon正交]]", "[[S-2026-Su-11777-Muon双旋转]]", "[[S-2026-Su-11864-Stiefel解析解]]"]
exercises: ["[[习题 - Stiefel、谱球面、旋转 Muon 与约束更新]]"]
solutions: ["[[解答 - Stiefel、谱球面、旋转 Muon 与约束更新]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-stiefel-tangent-retraction-rotation-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Stiefel、谱球面、旋转 Muon 与约束更新

> [!abstract] 一句话结论
> “更新矩阵近似正交”与“参数被约束为正交矩阵”完全不同。Stiefel 优化必须依次处理 ambient gradient、tangent projection、局部步与 retraction；双旋转更新又把参数限制在固定奇异值轨道上。约束带来精确不变量，也可能删掉任务需要的自由度。

## 一、四个对象先分开

设 $W\in\mathbb R^{m\times p}$，$m\ge p$。

1. **ambient parameter**：$W$ 可取任意矩阵；
2. **orthogonalized update**：$\Delta W$ 的列近似正交，但 $W+\Delta W$ 未必正交；
3. **Stiefel-constrained parameter**：始终要求 $W^TW=I_p$；
4. **orthogonal orbit update**：$W$ 只做左右旋转，因而保持全部 singular values。

这四个集合/动作不能用一个“orthogonal Muon”名称代替。

## 二、Stiefel 流形与切空间

列正交 Stiefel manifold 定义为

$$
\operatorname{St}(m,p)
=\{W\in\mathbb R^{m\times p}:W^TW=I_p\}.
\tag{1}
$$

令平滑曲线 $W(t)$ 留在流形上，$W(0)=W$，$\dot W(0)=\Xi$。对约束求导：

$$
\frac d{dt}W(t)^TW(t)\Big|_{t=0}
=W^T\Xi+\Xi^TW=0.
\tag{2}
$$

因此切空间为

$$
T_W\operatorname{St}(m,p)
=\{\Xi:W^T\Xi+\Xi^TW=0\}.
\tag{3}
$$

这是**一阶可行条件**。

## 三、ambient gradient 如何投影到 tangent

设 Euclidean gradient 为 $G$。在 embedded Euclidean metric 下，切空间正交投影为

$$
\Pi_W(G)
=G-W\operatorname{sym}(W^TG),
\tag{4}
$$

其中

$$
\operatorname{sym}(A)=\frac12(A+A^T).
$$

验证：

$$
W^T\Pi_W(G)+\Pi_W(G)^TW
=W^TG+G^TW-2\operatorname{sym}(W^TG)=0.
$$

所以 Riemannian gradient 可取

$$
\operatorname{grad}L(W)=\Pi_W(G)
\tag{5}
$$

（具体表达仍依赖所选 Riemannian metric）。

## 四、tangent step 为什么仍不精确可行

取 $\Xi\in T_W\operatorname{St}(m,p)$，直接 Euler step：

$$
\widetilde W=W+\eta\Xi.
$$

则

$$
\widetilde W^T\widetilde W
=I+\eta(W^T\Xi+\Xi^TW)+\eta^2\Xi^T\Xi
=I+\eta^2\Xi^T\Xi.
\tag{6}
$$

一阶项消失，但二阶项仍使参数离开流形。因此 tangent direction 不等于 finite-step feasible update。

### 4.1 polar retraction

一种标准 retraction 是

$$
R_W(\eta\Xi)
=(W+\eta\Xi)
\left[(W+\eta\Xi)^T(W+\eta\Xi)\right]^{-1/2}.
\tag{7}
$$

只要括号内正定，它满足精确列正交。QR retraction 也常用；两者的 finite-step path 与数值成本不同。

## 五、Muon update 为什么通常不是 Stiefel tangent

普通 Muon 对 ambient gradient/momentum $M$ 取

$$
Q_M=\operatorname{polar}(M)
$$

并做 $W_+=W-\eta Q_M$。即使

$$
Q_M^TQ_M=I,
$$

它一般不满足

$$
W^TQ_M+Q_M^TW=0.
$$

所以“update 本身列正交”不能推出它在 $W$ 处是 tangent，更不能推出 $W_+^TW_+=I$。若参数要留在 Stiefel 上，必须先构造 Riemannian direction，再 retraction 或使用 exact feasible flow。

## 六、谱球、Stiefel 与 orthogonal group 的包含关系

- spectral unit ball：

$$
\mathbb B_2=\{\Delta:\lVert\Delta\rVert_2\le1\};
$$

- 满列 rank 的 polar directions 位于边界且 $Q^TQ=I$；
- $\operatorname{St}(m,p)$ 是参数集合，不是 update ball；
- 当 $m=p$ 时，$\operatorname{St}(p,p)=O(p)$，还分 determinant 为 $\pm1$ 的连通分支。

谱单位球的线性 oracle 允许 rank-deficient/nonunique boundary solutions；Stiefel constraint 要求每个 column 始终正交归一。二者只在某些矩阵上共享 $U V^T$ 形式。

## 七、双旋转：固定奇异值轨道

设

$$
W_+=Q_LWQ_R^T,
\qquad
Q_L^TQ_L=I,\quad Q_R^TQ_R=I.
\tag{8}
$$

则

$$
W_+^TW_+
=Q_R(W^TW)Q_R^T,
\tag{9}
$$

因此 $W_+^TW_+$ 与 $W^TW$ 特征值相同，亦即 $W_+$ 与 $W$ 的所有 singular values 完全相同。Frobenius norm、spectral norm、nuclear norm 与 rank 也全部保持。

这给出强约束：

- 优点：不会发生 singular-value explosion/collapse；
- 风险：如果任务需要学习新的 gain、rank profile 或 condition number，轨道内更新无法做到。

[[S-2026-Su-11777-Muon双旋转]] 提供了前沿变体入口，但“保持谱”是数学不变量，“训练更好”仍是需实验检验的命题。

## 八、Cayley/exponential flow 与 retraction

方形正交矩阵可用 skew-symmetric generator $\Omega^T=-\Omega$：

$$
W_+=W\exp(\eta\Omega)
\tag{10}
$$

精确保持正交。Cayley transform

$$
\operatorname{cay}(\eta\Omega)
=\left(I-\frac\eta2\Omega\right)^{-1}
\left(I+\frac\eta2\Omega\right)
\tag{11}
$$

也为正交矩阵（逆存在时），并近似 exponential。它们与 polar/QR retraction 都可产生 feasible point，但 path、cost、数值稳定性和可表示分支不同。

## 九、2026 解析结果如何纳入，而不提前封神

[[S-2026-Su-11864-Stiefel解析解]] 在 2026-08-17 提出指定设定下的解析最速方向。由于距本库访问日仅九天，采用三层证据：

1. Stiefel 定义、切空间与 retraction：按 [[S-2008-Absil-Matrix-Manifolds]] 的成熟框架；
2. 解析表达：逐式重推其 norm、metric、rank 与 inverse/root 存在条件；
3. 工程优势：等待公开实现、复杂度展开、finite-precision residual 和跨任务复现。

“解析”只表示不需要某类迭代求解，并不自动表示计算便宜；若表达仍含 SVD、matrix root 或 solve，必须计入实际 FLOPs 与通信。

## 十、约束训练的最小审计

每步记录：

$$
r_{feas}=\lVert W^TW-I\rVert_F,
\qquad
r_{tan}=\lVert W^T\Xi+\Xi^TW\rVert_F,
\tag{12}
$$

以及：

- retraction 前后的 loss 与 direction cosine；
- singular values 是否按设计保持或允许变化；
- exact FP64 feasibility 与训练 dtype feasibility；
- projection/retraction 的 wall-clock、peak memory、通信；
- constraint strength 与 task quality 的 trade-off。

## 十一、图：从 ambient gradient 到 tangent、retraction 与固定谱轨道

先看图回答：一个自身列正交的 update 为什么仍可能离开 Stiefel manifold，双旋转又额外冻结了哪些可学习量？

![[00-知识库管理/_assets/figures/training-optimization/fig-stiefel-tangent-retraction-rotation-v1.svg|900]]

> [!figure] 图 TRN-31　Stiefel tangent、finite-step retraction 与双旋转轨道
> 图把普通 Muon 的 orthogonalized ambient update 与真正的 Stiefel 流程分开，并展示双旋转 $Q_LWQ_R^T$ 对奇异值的精确保持。来源：依据 [[S-2008-Absil-Matrix-Manifolds]]、[[S-2025-Su-11215-Muon正交]]、[[S-2026-Su-11777-Muon双旋转]] 独立绘制。

**怎样读图**：沿蓝色路径做 constrained optimization；红色箭头说明“update 正交”不能跨过 tangent/retraction 两道门；绿色轨道表示另一类固定谱约束。

**图没有证明什么**：几何可行性不证明 loss 会下降，也不证明固定 singular values 适合所有层。

## 十二、本节出口

你应能推导式 (3)—(7)，判定一个矩阵方向是否 tangent，区分 update orthogonality 与 parameter feasibility，并证明双旋转的 singular-value invariance。

## 练习与独立解答

- [[习题 - Stiefel、谱球面、旋转 Muon 与约束更新]]
- [[解答 - Stiefel、谱球面、旋转 Muon 与约束更新]]
