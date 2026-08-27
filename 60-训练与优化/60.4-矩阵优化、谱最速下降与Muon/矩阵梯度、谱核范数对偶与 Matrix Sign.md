---
type: derivation
status: verified
area: [training, optimization, matrix-analysis, muon]
node_id: TRN-26
aliases: [谱最速下降与矩阵符号, Spectral Nuclear Duality]
prerequisites: ["[[最速下降、范数选择与对偶范数]]", "[[奇异值分解]]", "[[矩阵范数]]", "[[极分解]]"]
related: ["[[Newton–Schulz Matrix Sign 的收敛与有限精度]]", "[[Muon 的动量、正交化与参数分组合同]]", "[[矩阵符号函数]]"]
sources: ["[[S-2024-Bernstein-Newhouse-Old-Optimizer-New-Norm]]", "[[S-1986-Higham-Polar-Decomposition]]", "[[S-2008-Higham-矩阵符号函数]]", "[[S-2024-Su-10592-Muon优化器赏析]]", "[[S-2025-Su-10739-Muon续集]]"]
exercises: ["[[习题 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]"]
solutions: ["[[解答 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-spectral-nuclear-msign-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 矩阵梯度、谱核范数对偶与 Matrix Sign

> [!abstract] 一句话结论
> 对矩阵梯度 $G=U\Sigma V^T$，若用 spectral norm 限制一步更新，则线性模型的最大下降量是 nuclear norm $\lVert G\rVert_*$，一个 canonical 最速方向是 $-UV^T$。它是极分解的 partial isometry；rank-deficient 时最优解并不唯一。

## 一、矩阵梯度使用什么 pairing

设 $W\in\mathbb R^{m\times n}$，目标 $L(W)$。矩阵梯度 $G=\nabla_WL$ 由 Frobenius pairing 定义：

$$
DL(W)[\Delta]
=\langle G,\Delta\rangle_F
=\operatorname{tr}(G^T\Delta).
\tag{1}
$$

这只是把线性泛函写成矩阵坐标，并不表示步长一定使用 Frobenius norm。我们可以解

$$
\min_{\lVert\Delta\rVert_2\le1}\langle G,\Delta\rangle_F,
\tag{2}
$$

其中 $\lVert\cdot\rVert_2$ 是矩阵诱导二范数，也就是最大奇异值。

## 二、谱范数与核范数为什么互为对偶

令 compact SVD 为

$$
G=U_r\Sigma_rV_r^T,\qquad
\Sigma_r=\operatorname{diag}(\sigma_1,\ldots,\sigma_r),\quad \sigma_i>0.
$$

对任意 $\lVert\Delta\rVert_2\le1$，von Neumann trace inequality 给出

$$
\langle G,\Delta\rangle_F
\le\sum_{i=1}^{\min(m,n)}\sigma_i(G)\sigma_i(\Delta)
\le\sum_{i=1}^r\sigma_i(G).
\tag{3}
$$

右端就是 nuclear norm

$$
\lVert G\rVert_*=\sum_{i=1}^r\sigma_i(G).
$$

取

$$
\Delta=U_rV_r^T
\tag{4}
$$

有 $\lVert\Delta\rVert_2=1$ 且

$$
\langle G,U_rV_r^T\rangle_F
=\operatorname{tr}(\Sigma_r)
=\lVert G\rVert_*.
$$

因此

$$
\sup_{\lVert\Delta\rVert_2\le1}
\langle G,\Delta\rangle_F
=\lVert G\rVert_*,
\tag{5}
$$

谱范数与核范数互为对偶，式 (2) 的一个解为

$$
\Delta_\star=-U_rV_r^T.
\tag{6}
$$

## 三、为什么只保留奇异向量、把非零奇异值压成 1

普通 Frobenius geometry 的单位最速方向是

$$
-\frac{G}{\lVert G\rVert_F}
=-U_r\frac{\Sigma_r}{\lVert\Sigma_r\rVert_F}V_r^T.
$$

大奇异值方向仍获得更大幅度。spectral geometry 的 canonical direction 则是

$$
-U_rI_rV_r^T,
$$

所有 rank-support 上的奇异方向幅度相同。这不是声称“小奇异方向更重要”，而是 spectral step budget 的精确线性 oracle。

### 3.1 二维手算

令

$$
G=\begin{bmatrix}4&0\\0&1\end{bmatrix}.
$$

则 $\lVert G\rVert_*=5$，$U=V=I$，spectral-unit 最速方向是

$$
\Delta_\star=-I,\qquad
\langle G,\Delta_\star\rangle_F=-5.
$$

若误用 $-G/\lVert G\rVert_F$，预测下降为

$$
-\lVert G\rVert_F=-\sqrt{17}>-5,
$$

在 spectral budget 下它不是最优；它没有用满第二个奇异方向的允许幅度。

## 四、rank-deficient 时为什么不唯一

若 $r<\min(m,n)$，式 (6) 只规定了 $G$ 的 row/column support 上的动作。补全正交基

$$
U=[U_r,U_0],\qquad V=[V_r,V_0].
$$

则

$$
\Delta=U_rV_r^T+U_0KV_0^T,\qquad \lVert K\rVert_2\le1
\tag{7}
$$

仍满足 $\lVert\Delta\rVert_2\le1$，且第二项与 $G$ Frobenius-orthogonal，所以也达到同样极值。canonical partial isometry 取 $K=0$，因为它：

- 在 null-space 上不凭空添加动作；
- 具有最小 Frobenius norm $\sqrt r$；
- 与极分解中的 canonical polar factor 对齐。

> [!warning] “最速方向唯一”需要额外条件
> spectral norm 单位球不严格凸。即使 $G$ 非零，只要存在未被 $G$ 看见的奇异子空间，最优点就可以是一整个面。

## 五、polar factor、SVD-type msign 与 classical matrix sign

对矩形矩阵 $G=U_r\Sigma_rV_r^T$，本卷定义

$$
\operatorname{msign}(G):=U_rV_r^T.
\tag{8}
$$

它也是 canonical polar factor。若 $G$ 列满秩且 $m\ge n$，

$$
\operatorname{msign}(G)
=G(G^TG)^{-1/2}.
\tag{9}
$$

若行满秩且 $m\le n$，

$$
\operatorname{msign}(G)
=(GG^T)^{-1/2}G.
\tag{10}
$$

但经典 square-matrix sign 通常按无虚轴特征值的方阵定义：

$$
\operatorname{sign}(A)
=A(A^2)^{-1/2},
\tag{11}
$$

它是 eigenvalue function；非对称、非正规矩阵上不等于把 singular values 替换为 1。为避免概念偷换，本卷始终写：

- polar/msign：式 (8) 的 SVD-type partial isometry；
- classical sign：式 (11) 的方阵函数；
- finite-step NS output：某个多项式近似，既不默认为前两者的精确值。

## 六、极分解唯一性边界

极分解写作

$$
G=QH,\qquad H=(G^TG)^{1/2}\succeq0.
$$

当 $G$ 列满秩时，$Q$ 唯一且 $Q^TQ=I$；rank-deficient 时，作为 partial isometry 的 canonical $Q=U_rV_r^T$ 在 support 上唯一，但扩展成方形正交矩阵或在 null-space 上的动作并不唯一。

它还解决最近正交/partial-isometry 问题的一类版本：

$$
\min_{Q^TQ=I}\lVert G-Q\rVert_F.
$$

不过“最近正交矩阵”与“spectral-unit 最速方向”是两个不同优化问题，只是恰好共享 polar factor，不能把证明互相替代。

## 七、从精确 oracle 到实际优化器还有四个缺口

式 (6) 只给出单步线性 oracle。实际 Muon 还必须决定：

1. 对 raw gradient 还是 momentum matrix 做 msign；
2. 精确 SVD/polar 还是有限步 Newton–Schulz；
3. unit spectral step 如何做 shape scaling；
4. 哪些参数属于二维 hidden matrices，其他参数由谁更新。

所以“Muon = matrix sign gradient descent”只是一层数学骨架，不是完整可执行合同。

## 八、图：从 SVD 到对偶极值、极分解与三种 sign 对象

先看图回答：四条路径究竟在变换 singular values、eigenvalues，还是只计算有限步多项式近似？

![[00-知识库管理/_assets/figures/training-optimization/fig-spectral-nuclear-msign-ledger-v1.svg|900]]

> [!figure] 图 TRN-26　谱/核范数对偶与 msign 对象总账
> 图把 $G=U\Sigma V^T$ 分别送入对偶极值、canonical polar factor、classical matrix sign 和 finite-step polynomial 四条路径，并标出 rank-deficient non-uniqueness。来源：依据 [[S-1986-Higham-Polar-Decomposition]]、[[S-2008-Higham-矩阵符号函数]] 与 [[S-2024-Bernstein-Newhouse-Old-Optimizer-New-Norm]] 独立绘制。

**怎样读图**：先问算法究竟变换的是 singular values 还是 eigenvalues；再问输出是精确函数值还是有限步近似。

**图没有证明什么**：图没有证明有限步低精度 Newton–Schulz 一定接近 polar factor，也没有证明 spectral geometry 在所有网络上优于 Frobenius geometry。

## 九、AI 应用中的函数空间解释

若线性层写作 $y=xW$，参数扰动产生

$$
\delta y=x\Delta W.
$$

于是

$$
\lVert\delta y\rVert_2
\le\lVert x\rVert_2\lVert\Delta W\rVert_2.
$$

spectral norm 直接控制最坏输入方向上的 output change。这提供了选择 spectral step budget 的合理动机。但真实网络还有输入分布、activation、normalization、residual 和层间耦合；最坏方向 bound 不是平均训练效果的完整模型。

## 十、本节出口

你应能独立证明式 (5)，手算小矩阵的 polar/msign，解释 rank-deficient non-uniqueness，并拒绝把 classical sign、SVD-type msign 与 finite-step Newton–Schulz 输出混为一谈。

## 练习与独立解答

- [[习题 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]
- [[解答 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]
