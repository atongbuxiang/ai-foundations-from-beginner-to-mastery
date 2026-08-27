---
type: theorem
status: draft
area: [learning-theory/online-convex-optimization, ogd, mirror-descent]
aliases: [Projected Online Gradient Descent, Online Mirror Descent, OCO]
node_id: LT-71
prerequisites: ["[[在线学习协议、Regret 与 Comparator]]", "[[凸函数、Jensen 不等式与上图集]]", "[[投影、约束与可行方向]]", "[[镜像下降、Bregman 几何与自然梯度]]"]
related: ["[[Experts、Weighted Majority 与 Multiplicative Weights]]", "[[Online-to-Batch Conversion]]", "[[Bandit Feedback 与强化学习接口]]"]
sources: ["[[S-2003-Zinkevich-OCO]]", "[[S-2012-Shalev-Online-Learning-OCO]]", "[[S-2016-Hazan-OCO]]"]
exercises: ["[[习题 - Online Gradient Descent 与 Mirror Descent]]"]
solutions: ["[[解答 - Online Gradient Descent 与 Mirror Descent]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-ogd-omd-geometry-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Online Gradient Descent 与 Mirror Descent

> [!abstract] 本章主问题
> OGD 的 $\sqrt T$ regret 来自“凸性把 loss gap 变成梯度内积”与“投影距离势能望远镜”。Mirror descent 把 Euclidean squared distance 换成与决策域匹配的 Bregman divergence，dual norm 自然进入界。

## 一、学习目标

完成本章后，应能：

1. 写 OCO protocol 与 assumptions；
2. 推导 projected OGD update；
3. 用 projection nonexpansiveness 证明 regret；
4. 优化 learning rate；
5. 说明 convexity、diameter、gradient bound 各自用途；
6. 推导 strongly convex 的 logarithmic bound 接口；
7. 定义 Bregman divergence 与 OMD；
8. 写 geometry-aware dual-norm bound；
9. 解释 entropy OMD 如何得到 multiplicative weights；
10. 区分 theorem regret 与每轮求解/梯度 oracle 误差。

## 二、OCO Protocol

决策集 $K\subseteq\mathbb R^d$ 非空、闭、凸。第 $t$ 轮 learner 选 $w_t\in K$，随后观察 convex loss $\ell_t$ 并承受 $\ell_t(w_t)$。

基本 assumptions：

$$
\|u-v\|_2\le D,\quad \forall u,v\in K,
$$

$$
\|g_t\|_2\le G,\quad g_t\in\partial\ell_t(w_t).
$$

无 bounded diameter 或 gradients，distribution-free $\sqrt T$ 常数可能无穷。

## 三、Projected OGD

$$
\boxed{
w_{t+1}
=
\Pi_K(w_t-\eta g_t),
}
$$

其中

$$
\Pi_K(z)=\arg\min_{w\in K}\|w-z\|_2.
$$

先沿 negative subgradient 走一步，再投影回可行域。投影不是 clip 每个坐标的同义词，除非 $K$ 是 box。

## 四、凸性线性化

对任意 comparator $u\in K$：

$$
\boxed{
\ell_t(w_t)-\ell_t(u)
\le
\langle g_t,w_t-u\rangle.
}
$$

这一步把 nonlinear loss regret 上界为 online linear optimization。若 loss 非凸，该 inequality 不成立。

## 五、投影势能不等式

投影对任意 $u\in K$：

$$
\|w_{t+1}-u\|_2^2
\le
\|w_t-\eta g_t-u\|_2^2.
$$

展开：

$$
\|w_{t+1}-u\|^2
\le
\|w_t-u\|^2
-2\eta\langle g_t,w_t-u\rangle
+\eta^2\|g_t\|^2.
$$

整理：

$$
\boxed{
\langle g_t,w_t-u\rangle
\le
\frac{\|w_t-u\|^2-\|w_{t+1}-u\|^2}{2\eta}
+\frac{\eta}{2}\|g_t\|^2.
}
$$

## 六、OGD Regret

由凸性、求和与望远镜：

$$
\operatorname{Reg}_T(u)
\le
\frac{\|w_1-u\|^2}{2\eta}
+\frac{\eta}{2}\sum_t\|g_t\|^2.
$$

用 $D,G$：

$$
\boxed{
\operatorname{Reg}_T(u)
\le
\frac{D^2}{2\eta}
+\frac{\eta G^2T}{2}.
}
$$

取

$$
\eta=\frac{D}{G\sqrt T}
$$

得到

$$
\boxed{\operatorname{Reg}_T\le DG\sqrt T.}
$$

## 七、每个 Assumption 在哪里用

- convexity：loss gap ≤ gradient inner product；
- convex $K$：Euclidean projection well-defined/variational property；
- diameter $D$：初始 potential；
- gradient bound $G$：每轮 quadratic cost；
- current loss unseen：regret protocol；
- exact projection/subgradient：实现 theorem update。

列 assumptions 比背最终式更重要。

## 八、Strongly Convex 接口

若每个 $\ell_t$ 是 $\lambda$-strongly convex：

$$
\ell_t(w_t)-\ell_t(u)
\le
\langle g_t,w_t-u\rangle
-\frac\lambda2\|w_t-u\|^2.
$$

用 $\eta_t=1/(\lambda t)$ 可让 negative curvature term 与势能相消，得到量级

$$
\operatorname{Reg}_T
=O\!\left(\frac{G^2}{\lambda}\log T\right).
$$

若只是总和强凸或 regularizer 强凸，证明需重新写，不能套逐轮结论。

## 九、Bregman Divergence

令 regularizer $\psi$ 可微且相对范数 $\|\cdot\|$ 为 $\sigma$-strongly convex：

$$
D_\psi(u,v)
=
\psi(u)-\psi(v)-\langle\nabla\psi(v),u-v\rangle.
$$

它非负但一般不对称，也不满足 triangle inequality；它是势能，不必是 metric。

## 十、Online Mirror Descent

一种 OMD 写法：

$$
\boxed{
w_{t+1}
=
\arg\min_{w\in K}
\left\{
\eta\langle g_t,w\rangle
+D_\psi(w,w_t)
\right\}.
}
$$

linearized loss 在 dual space 推动，Bregman term 控制相对当前点的运动。

## 十一、OMD Regret Bound

三点恒等式与 optimality 给：

$$
\langle g_t,w_t-u\rangle
\le
\frac{D_\psi(u,w_t)-D_\psi(u,w_{t+1})}{\eta}
+\frac{\eta}{2\sigma}\|g_t\|_*^2.
$$

求和：

$$
\boxed{
\operatorname{Reg}_T(u)
\le
\frac{D_\psi(u,w_1)}{\eta}
+\frac{\eta}{2\sigma}\sum_t\|g_t\|_*^2.
}
$$

primal geometry 决定 dual norm；这是 mirror descent 与 AI 参数域匹配的核心。

## 十二、两个 Geometry

### 12.1 Euclidean Ball

取 $\psi(w)=\frac12\|w\|_2^2$，$D_\psi=\frac12\|u-v\|_2^2$，OMD 退化为 OGD。

### 12.2 Probability Simplex

取 negative entropy：

$$
\psi(p)=\sum_ip_i\log p_i.
$$

Bregman divergence 是 $D_{\rm KL}(p\Vert q)$，dual norm 对应 $\ell_\infty$；update 为

$$
p_{t+1,i}\propto p_{t,i}e^{-\eta g_{t,i}},
$$

即 exponential/multiplicative weights。

## 十三、FTRL 与 OMD

FTRL：

$$
w_t=\arg\min_{w\in K}
\left\{
\eta\sum_{s<t}\langle g_s,w\rangle+\psi(w)
\right\}.
$$

在特定 regularizer/linear losses 下与 OMD updates 等价或紧密相关；一般 constraints、time-varying regularizers 与 composite losses 下 iterates 未必相同。不要只因 regret bound 相似就称算法同一。

## 十四、Approximate Oracle

若 subgradient 有误差 $\widetilde g_t=g_t+e_t$，或 projection 只近似，regret 增加

$$
\sum_t\langle e_t,w_t-u\rangle
$$

及 projection residual terms。大模型分布式/量化/截断训练中，oracle error 必须进入预算，理论不能假设免费精确投影。

## 十五、图：Euclidean 势能与 Mirror 势能

先看图回答：在 simplex 上用 Euclidean projection 与 entropy mirror update 都有 no-regret，为何 $\log d$ 与 $\sqrt d$ 的维数依赖可能不同？

![[00-知识库管理/_assets/figures/learning-theory/fig-ogd-omd-geometry-v2.svg|900]]

> [!figure] 图 20.9-03　OGD 距离望远镜、OMD 三点势能与 geometry choice
> 左栏给 projected OGD proof；中栏把 squared distance 替换为 Bregman divergence/dual norm；右栏比较 Euclidean、simplex entropy、FTRL 与 approximate oracle。来源：依据 Zinkevich、Shalev-Shwartz 与 Hazan 独立绘制；由 [[plot_online_learning_v2.py]] 确定性生成。

**怎样读图**：convexity先线性化；geometry只改变如何控制 gradient inner product 和 potential diameter。

**图没有证明什么**：图没有证明 nonconvex neural loss 具有同一 regret，也没有证明计算上能精确解每次 mirror/projection subproblem。

## 十六、常见错误

1. loss 非凸仍用 subgradient inequality；
2. 忘记 projection；
3. diameter 与 radius 混差 2；
4. primal/dual norm不匹配；
5. Bregman divergence 当对称距离；
6. entropy 边界点/零坐标不处理；
7. $\eta$ 偷看未来 $T$；
8. approximate gradient/projection 不计误差。

## 十七、最小记忆与掌握标准

> [!summary]
> - OGD = convex linearization + projected distance telescope；
> - $D^2/\eta$ 与 $\eta G^2T$ 平衡为 $DG\sqrt T$；
> - strong convexity 可给 $\log T$；
> - OMD 用 Bregman potential 与 dual norm；
> - entropy OMD 就是 multiplicative weights；
> - oracle/geometry assumptions 必须可实现。

能推导 OGD（A/B）、证明 OMD 一步不等式（C）、比较 geometry/反例（D），并为 simplex、matrix或模型路由选择 regularizer（E）。

## 十八、练习与独立详解

- [[习题 - Online Gradient Descent 与 Mirror Descent]]
- [[解答 - Online Gradient Descent 与 Mirror Descent]]

## 参考来源

- [[S-2003-Zinkevich-OCO]]
- [[S-2012-Shalev-Online-Learning-OCO]]
- [[S-2016-Hazan-OCO]]
