---
type: concept
status: draft
area: [math/optimization, math/information-geometry, ai/training]
aliases: [镜像下降, 镜像下降、自然梯度与几何预条件, mirror descent, Bregman divergence, natural gradient, Fisher geometry, exponentiated gradient]
prerequisites: ["[[梯度、方向导数与最陡方向]]", "[[投影、约束与可行方向]]", "[[交叉熵与 KL 散度]]"]
related: ["[[优化与凸分析 MOC]]", "[[近端算子、复合优化与稀疏正则]]", "[[自适应优化方法]]", "[[Hessian、二阶微分与曲率]]"]
sources: ["Stanford-EE364B-Mirror-Descent", "MIT-6.253-Entropy-Prox", "Beck-Teboulle-2003-Mirror", "Amari-1998-Natural-Gradient", "Martens-2020-Natural-Gradient", "Su-10592-Muon", "Su-11215-Manifold-Steepest"]
created: 2026-08-19
updated: 2026-08-27
---

# 镜像下降、Bregman 几何与自然梯度

> [!abstract] 本章主问题
> “最陡下降方向”不是只由 objective 决定，还取决于我们用什么局部距离衡量一步有多大。mirror descent 用 convex potential 产生 Bregman divergence，把 gradient step 放进适合 simplex、positive cone 或其他可行域的几何；natural gradient 用 model distribution 的 local KL 二次型产生 Fisher metric。二者共享“linearized loss + geometry-controlled movement”的结构，但不应无条件等同：mirror map、parameterization、Fisher 定义、damping 和 approximation 都会改变实际算法。

## 学习目标

完成本章后，你应当能够：

1. 从 strictly convex potential 定义 Bregman divergence；
2. 证明非负性，并解释它为何一般不 symmetric、无 triangle inequality；
3. 推导 constrained mirror-descent subproblem 与 dual-coordinate update；
4. 恢复 Euclidean projected gradient；
5. 从 negative entropy 推 exponentiated-gradient update；
6. 证明 Bregman three-point identity；
7. 由 one-step inequality 推导 online regret / convex optimization rate；
8. 解释 geometry choice 怎样改变 dimension dependence；
9. 把 quadratic mirror map 与 preconditioning/AdaGrad 联系起来；
10. 从 KL trust region 的二阶展开推导 natural gradient；
11. 区分 exact Fisher、empirical Fisher 与 generalized Gauss–Newton；
12. 正确陈述 natural gradient 的 reparameterization invariance及其边界；
13. 解释 mirror descent 与 natural gradient 何时局部相合、何时不同；
14. 处理 singular Fisher、pseudoinverse、damping 与 block approximations；
15. 区分 Muon 的 spectral geometry 与 Fisher natural gradient。

> [!question] 初学者读完必须能回答
> 1. Bregman divergence 怎样由 convex potential 与 tangent gap 定义，为什么一般不是 metric？
> 2. mirror-descent 子问题怎样在 primal/dual coordinates 之间转换？
> 3. Euclidean quadratic potential 如何恢复 projected gradient？
> 4. negative entropy 为什么在 simplex 上产生 exponentiated-gradient/multiplicative update？
> 5. three-point identity 怎样进入 one-step inequality 与 regret/rate 证明？
> 6. local KL trust region 怎样二阶展开为 Fisher metric 并推出 natural-gradient direction？
> 7. exact Fisher、empirical Fisher、GGN、K-FAC、damping、pseudoinverse 与 Muon 为什么不能混作同一种 geometry？

## 阅读前检查：三个容易混淆的层次

- [[梯度、方向导数与最陡方向]]说明了 Euclidean gradient 依赖 inner product；
- [[梯度、方向导数与最陡方向]]还说明 metric tensor 如何把 differential 变成 gradient vector；
- 本章关注怎样把这种几何落实成可执行 update、proof 与 AI 审计。

> [!note] 课程位置
> OPT-09 已经说明 inverse metric 把 differential 转成 displacement；OPT-11 的 Euclidean projection 又说明 movement geometry 会改变约束解。本章把固定 quadratic metric 推广为 Bregman divergence，并在 probability simplex 上得到 entropy mirror descent；随后只在 infinitesimal/local 层面，把 KL 二阶展开连接到 Fisher natural gradient。

> [!tip] 建议两遍阅读
> **第一遍**只学习二元 simplex 上的一次 entropy mirror step：写出乘法权重、正规化，并核对它怎样从 $(1/4,3/4)$ 到达 $(1/2,1/2)$。**第二遍**再证明 three-point identity、regret bound、natural-gradient invariance，并区分 exact Fisher、empirical Fisher、GGN、K-FAC 与 damping。有限 mirror step 和 local Fisher step 绝不能在第一遍就混成同一个公式。

## 本章的推导问题链

1. 为什么 gradient 是一个线性 functional，而“走多远”还需要 geometry？
2. Bregman divergence 从 tangent gap 怎样产生，为什么非负却通常不是 metric？
3. mirror subproblem 的一阶条件为什么在 $\nabla\psi$ coordinates 中变成加法更新？
4. negative entropy 怎样把 additive dual step 变成 primal multiplicative weights？
5. KL 的二阶项怎样定义 Fisher；这个 local quadratic approximation漏掉了什么？
6. exact Fisher、empirical Fisher、GGN 和 optimizer 的 gradient-square state 分别对什么分布、残差和参数化取期望？

## 贯穿算例：同一个 quadratic，换成 probability-simplex geometry

把第四波的 quadratic 限制在二元 probability simplex：

$$
x=(p,1-p)^T,
\qquad
0<p<1,
$$

$$
f(x)=\frac12x^THx-b^Tx,
\qquad
H=\operatorname{diag}(1,4),
\qquad
b=(1,5/2)^T.
$$

代入得到一维函数

$$
\phi(p)
=f(p,1-p)
=\frac52p^2-\frac52p-\frac12.
$$

因此

$$
\phi'(p)=5p-\frac52,
\qquad
p^*=\frac12,
\qquad
x^*=(1/2,1/2)^T.
$$

这与前两章共享同一 $x^*$，但本章问的是：从一个严格正的 probability vector 出发，Euclidean、entropy 与 Fisher geometry 分别怎样解释“一步”。

### 符号与对象账本

| 对象 | 类型 | 本例/算法角色 | 不可直接称为 |
|---|---|---|---|
| $\psi(x)=\sum_i x_i\log x_i$ | mirror potential | 产生 entropy geometry | objective loss |
| $D_\psi(x,y)$ | Bregman divergence | 本例为 $D_{\mathrm{KL}}(x\|y)$ | symmetric distance |
| $g_0=\nabla f(x_0)$ | primal differential | 进入 dual-coordinate update | Fisher matrix |
| $\eta$ | mirror step scale | 控制 linear term 与 movement 的平衡 | KL radius 本身 |
| $F(p)$ | exact Bernoulli Fisher | $1/[p(1-p)]$ | empirical gradient outer product |
| $d_{\mathrm{nat}}$ | local direction | $-F^{-1}\phi'(p)$ | 有限 mirror iterate |

### 第一步：在起点计算真正进入更新的 gradient difference

取

$$
x_0=(1/4,3/4)^T.
$$

原二维 gradient 为

$$
g_0=Hx_0-b
=\left(-\frac34,\frac12\right)^T.
$$

在 simplex tangent direction $(1,-1)$ 上，真正决定 $p$ 变化的是

$$
g_{0,1}-g_{0,2}
=-\frac54
=\phi'(1/4).
$$

给 gradient 两个坐标同时加同一个常数不会改变 entropy update，因为 normalization 会把共同因子消掉；这正对应 simplex normal direction 的不可辨识性。

### 第二步：entropy mirror step 精确到达 $x^*$

negative-entropy mirror descent 给

$$
x_{+,i}
=\frac{x_{0,i}e^{-\eta g_{0,i}}}
{\sum_jx_{0,j}e^{-\eta g_{0,j}}}.
$$

先看两个分量的 ratio：

$$
\frac{x_{+,1}}{x_{+,2}}
=\frac{1/4}{3/4}
\exp\left[-\eta(g_{0,1}-g_{0,2})\right]
=\frac13\exp\left(\frac54\eta\right).
$$

选择

$$
\eta=\frac45\log3,
$$

则 ratio 恰好为 $1$；再用两分量和为 $1$，得到

$$
\boxed{
x_+=(1/2,1/2)^T=x^*.
}
$$

这一步的 Bregman movement 是

$$
\begin{aligned}
D_{\mathrm{KL}}(x^*\|x_0)
&=\frac12\log\frac{1/2}{1/4}
+\frac12\log\frac{1/2}{3/4}\\
&=\frac12\log\frac43.
\end{aligned}
$$

注意方向：mirror subproblem 使用的是 $D_\psi(x,x_0)$，这里因而是 $D_{\mathrm{KL}}(x^*\|x_0)$，反向 KL 数值不同。

### 第三步：Fisher 只给这一几何的局部二次方向

对 Bernoulli mean parameter $p$，

$$
F(p)
=\mathbb E\left[
\left(\frac{\partial}{\partial p}\log P_p(Z)\right)^2
\right]
=\frac1{p(1-p)}.
$$

在 $p_0=1/4$，

$$
F(p_0)=\frac{16}{3}.
$$

把 KL 只保留到二阶，并把 $\phi$ 只线性化，unit-scale natural direction 为

$$
\boxed{
d_{\mathrm{nat}}
=-F(p_0)^{-1}\phi'(p_0)
=-\frac3{16}\left(-\frac54\right)
=\frac{15}{64}.
}
$$

它指向 $p^*=1/2$，但不是上面有限 entropy step 的位移

$$
p^*-p_0=\frac14=\frac{16}{64}.
$$

两者相近来自 local geometry 一致；两者不等来自 finite-step KL 的高阶项、step scaling 与 normalization。Natural gradient 是局部方向，除非另有 line search/trust-region solve，不能把 $p_0+d_{\mathrm{nat}}$ 宣称为 exact mirror iterate。

### 核心公式七问：mirror-descent 子问题

对

$$
x_{t+1}
=\arg\min_{x\in\mathcal X}
\left\{
\eta\langle g_t,x\rangle+D_\psi(x,x_t)
\right\},
$$

逐项回答：

1. **目的：**在 linearized loss 与符合变量结构的 movement geometry 之间取平衡；
2. **对象：**$g_t$ 是 differential，$\psi$ 选择 geometry，$x$ 才是子问题变量；
3. **来路：**用 convex tangent gap 替换 Euclidean squared distance；
4. **步骤：**写 optimality，进入 $\nabla\psi$ dual coordinates 做 additive step，再经 conjugate/normalization 返回；
5. **读法：**同一个 differential 经不同 geometry 会变成不同 displacement；
6. **检查：**核对 divergence 方向、domain interior、strong-convexity norm、dual norm和 boundary support；
7. **去路：**entropy/multiplicative weights、variational inference、policy trust region 与 Fisher natural gradient。

> [!warning] Fisher 与实现边界
> Exact Fisher 必须声明 model distribution、输入分布和 parameterization；empirical Fisher 是 observed gradients 的 outer product，GGN 从 loss curvature 与 Jacobian 组合，K-FAC 又是结构近似。Damping 把 $F^{-1}$ 改成 $(F+\lambda I)^{-1}$，pseudoinverse 还依赖 range 与 cutoff。它们可能工程上相关，却不是同一个 theorem object。

> [!success] 第一遍停靠线
> 合上笔记后，能把 quadratic 限制成 $\phi(p)=\frac52p^2-\frac52p-\frac12$；从 $x_0=(1/4,3/4)$ 算出 $g_0=(-3/4,1/2)$；由 ratio 公式和 $\eta=\frac45\log3$ 得到 $x_+=(1/2,1/2)$；再算出 Bernoulli Fisher $16/3$ 与 local natural direction $15/64$，并解释为什么它不是有限 mirror 位移 $16/64$。

先用下图回答一个视觉问题：**选择不同 movement geometry 后，一步更新怎样在 mirror coordinates、simplex 熵几何和 Fisher–KL 局部几何中改变？**

![[00-知识库管理/_assets/figures/optimization/fig-mirror-natural-geometry-v2.svg|880]]

> [!figure] 图 10.7.15｜Mirror dual coordinates、熵更新与 Fisher trust region
> A 先用 $z_t=\nabla\psi(x_t)$ 进入 dual coordinate，在其中做 $z_t-\eta g_t$，再经 $\nabla\psi^*$ 返回 primal；B 以 negative entropy 在 simplex 上的乘法权重说明 positivity/normalization 如何内置于 geometry；C 从 local KL trust region 得到 $-F^{-1}\nabla L$，并列出 exact Fisher、empirical Fisher/GGN/K-FAC、damping 与 singularity 的边界。来源：独立绘制；生成脚本：[[plot_advanced_optimization_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 不要把 dual coordinate 当作普通坐标复制：梯度在 dual space 更新，返回要用 conjugate map；B 比较概率分量的相对变化而非 Euclidean 绝对位移；C 先声明 KL 的方向、期望分布和 Fisher 定义，再检查 inverse action、damping 与近似。只有对象一致时，才讨论 reparameterization invariance。

**适用边界（图没有证明什么）。** Bregman divergence 通常不对称且无三角不等式；strict convexity 也不自动给所需 strong-convexity rate。Entropy update 假设 simplex interior/适当边界处理。Natural-gradient 图是 local second-order KL approximation；finite step 的 actual KL 仍需检查。Empirical Fisher、GGN、K-FAC 与 exact Fisher 不是可随意互换的矩阵，damping 和 singular pseudoinverse 也会改变不变性。

## 零、为什么 Euclidean distance 不是默认真理

普通 projected gradient 可写为

$$
x_{t+1}
=\arg\min_{x\in C}
\left\{
\eta\langle g_t,x\rangle
+\frac12\|x-x_t\|_2^2
\right\}.
$$

第一项偏好下降，第二项限制移动。若 $x$ 是 probability vector，Euclidean distance：

- 不主动尊重 positivity；
- 在 boundary 附近与概率相对变化不匹配；
- 对高维 simplex 的 dimension dependence 可能不佳。

因此问题不是“怎样修改 gradient 数值”，而是：

> 用什么 geometry 衡量从 $x_t$ 到 $x$ 的一步？

## 一、Bregman divergence：由 convex potential 产生方向性距离

令 $\psi$ 在 convex set $\mathcal X$ 上 differentiable 且 strictly convex。定义

$$
D_\psi(x,y)
:=
\psi(x)-\psi(y)-\langle\nabla\psi(y),x-y\rangle.
$$

它是 $\psi(x)$ 与 $\psi$ 在 $y$ 处 tangent hyperplane 的 vertical gap。

### 1.1 非负性

convexity first-order inequality：

$$
\psi(x)\ge
\psi(y)+\langle\nabla\psi(y),x-y\rangle,
$$

所以

$$
D_\psi(x,y)\ge0.
$$

strict convexity 下 $x\ne y$ 时严格为正。

### 1.2 它通常不是 metric

一般：

$$
D_\psi(x,y)\ne D_\psi(y,x),
$$

且未必满足 triangle inequality。称其为 divergence，不应偷换为 metric distance。

若 $\psi(x)=\frac12\|x\|_2^2$：

$$
D_\psi(x,y)=\frac12\|x-y\|_2^2.
$$

若 $x,y$ 在 probability simplex interior，取 negative entropy

$$
\psi(x)=\sum_{i=1}^d x_i\log x_i,
$$

则

$$
D_\psi(x,y)
=\sum_i x_i\log\frac{x_i}{y_i}
=D_{\mathrm{KL}}(x\|y).
$$

方向由 first argument 决定；反过来不是同一个 KL。

### 1.3 local quadratic geometry

若 $\psi$ 二阶 differentiable：

$$
D_\psi(y+\Delta,y)
=\frac12\Delta^T\nabla^2\psi(y)\Delta
+o(\|\Delta\|^2).
$$

因此 Hessian $\nabla^2\psi(y)$ 是 Bregman divergence 的 local metric tensor，但 global divergence 包含更高阶与方向信息。

## 二、mirror descent：linearized loss + Bregman movement

给 convex feasible set $\mathcal X$、subgradient $g_t\in\partial f_t(x_t)$，定义

$$
\boxed{
x_{t+1}
=\arg\min_{x\in\mathcal X}
\left\{
\eta_t\langle g_t,x\rangle
+D_\psi(x,x_t)
\right\}.
}
$$

若 $\mathcal X$ 无额外边界且解在 interior，stationarity：

$$
\eta_tg_t
+\nabla\psi(x_{t+1})
-\nabla\psi(x_t)=0.
$$

所以

$$
\boxed{
\nabla\psi(x_{t+1})
=\nabla\psi(x_t)-\eta_tg_t.
}
$$

令 dual coordinate $\theta=\nabla\psi(x)$，更新是：

1. 用 mirror map 把 primal $x_t$ 映到 dual $\theta_t$；
2. 在 dual coordinate 做线性 step；
3. 用 $(\nabla\psi)^{-1}$ 映回 primal。

全局使用逆映射还需要 $\psi$ 具有 Legendre-type regularity，或至少把 inverse 限制在 $\nabla\psi$ 的像上；strict convexity只保证 gradient 在适当 convex differentiability domain 上 injective，并不自动保证其像覆盖整个 dual space。有 constraints 时还需 Bregman projection / normal cone，不能只写无约束逆映射。

## 三、两个基本特例

### 3.1 Euclidean potential 恢复 projected gradient

取

$$
\psi(x)=\frac12\|x\|_2^2.
$$

则

$$
x_{t+1}
=\arg\min_{x\in\mathcal X}
\left\{
\eta_t\langle g_t,x\rangle
+\frac12\|x-x_t\|^2
\right\}
=\Pi_{\mathcal X}(x_t-\eta_tg_t).
$$

mirror descent 不是与 gradient descent 完全无关的新算法，而是其 geometry-generalized form。

### 3.2 negative entropy 恢复 exponentiated gradient

在 simplex

$$
\Delta_d=\left\{x\ge0:\sum_i x_i=1\right\}
$$

上取 negative entropy。带 normalization multiplier $\lambda$ 的 stationarity：

$$
\eta g_{t,i}
+\log x_{t+1,i}-\log x_{t,i}
+\lambda=0.
$$

所以

$$
x_{t+1,i}
=x_{t,i}e^{-\eta g_{t,i}}e^{-\lambda}.
$$

用 $\sum_i x_{t+1,i}=1$ 得

$$
\boxed{
x_{t+1,i}
=\frac{x_{t,i}e^{-\eta g_{t,i}}}
{\sum_jx_{t,j}e^{-\eta g_{t,j}}}.
}
$$

它自动保持 positivity 与 normalization。数值实现应在 log domain 用 log-sum-exp，避免 overflow/underflow。

> [!warning] support 不能自动复活
> 若 $x_{t,i}=0$，multiplicative update 仍为零。标准 entropy mirror descent 通常从 strictly positive interior 初始化；若要允许 support expansion，要改 regularizer、加入 mixing 或处理 boundary subgradient。

## 四、three-point identity：证明的代数枢纽

展开定义可得

$$
\boxed{
\langle\nabla\psi(y)-\nabla\psi(z),x-y\rangle
=D_\psi(x,z)-D_\psi(x,y)-D_\psi(y,z).
}
$$

验证：右侧展开后，$\psi(x),\psi(y),\psi(z)$ 相消，只剩 gradient inner products。

对 mirror step 的 optimality condition（含 normal cone），任意 $x\in\mathcal X$：

$$
\left\langle
\eta_tg_t+\nabla\psi(x_{t+1})-\nabla\psi(x_t),
x-x_{t+1}
\right\rangle\ge0.
$$

代入 three-point identity：

$$
\boxed{
\eta_t\langle g_t,x_{t+1}-x\rangle
\le
D_\psi(x,x_t)
-D_\psi(x,x_{t+1})
-D_\psi(x_{t+1},x_t).
}
$$

这是 telescope 的核心。

## 五、从 one-step inequality 到 regret bound

假设 $\psi$ 关于 norm $\|\cdot\|$ 是 $\sigma$-strongly convex：

$$
D_\psi(y,x)\ge\frac\sigma2\|y-x\|^2.
$$

将

$$
\langle g_t,x_t-x\rangle
=\langle g_t,x_t-x_{t+1}\rangle
+\langle g_t,x_{t+1}-x\rangle
$$

与上一节 inequality 合并，并用 Hölder–Young：

$$
\langle g_t,x_t-x_{t+1}\rangle
-\frac{\sigma}{2\eta_t}\|x_{t+1}-x_t\|^2
\le\frac{\eta_t}{2\sigma}\|g_t\|_*^2.
$$

常数步长 $\eta$ 时：

$$
\boxed{
\sum_{t=1}^T
\langle g_t,x_t-x\rangle
\le
\frac{D_\psi(x,x_1)}{\eta}
+\frac{\eta}{2\sigma}
\sum_{t=1}^T\|g_t\|_*^2.
}
$$

若 $f_t$ convex：

$$
f_t(x_t)-f_t(x)
\le\langle g_t,x_t-x\rangle.
$$

因此得到 online regret bound。若 $\|g_t\|_*\le G$、$D_\psi(x,x_1)\le R^2$，选

$$
\eta=\frac{\sqrt{2\sigma}R}{G\sqrt T}
$$

可得 $O(RG\sqrt{T/\sigma})$ regret，平均 regret 为 $O(1/\sqrt T)$。对同一 offline convex objective，用 averaged iterate 可转成 suboptimality bound。

### 5.1 为什么 dual norm 出现

movement 用 $\|\cdot\|$ 衡量，gradient linear functional 的大小自然由 dual norm

$$
\|g\|_*=\sup_{\|x\|\le1}\langle g,x\rangle
$$

衡量。geometry choice 同时决定 diameter $D_\psi$ 与 gradient bound $\|g_t\|_*$，不能只看其中一个。

## 六、dimension dependence：simplex 为何偏爱 entropy

在 $d$-simplex 上，uniform initialization $x_1=(1/d,\ldots,1/d)$。对任意 vertex $e_i$：

$$
D_{\mathrm{KL}}(e_i\|x_1)=\log d.
$$

entropy mirror descent 若 $\|g_t\|_\infty\le G$，其 bound 依赖 $\sqrt{\log d}$。Euclidean 分析的 gradient dual norm 是 $\ell_2$，若每个 coordinate bounded，则 $\|g_t\|_2$ 可达 $G\sqrt d$。

这不是说 entropy 在所有数据上必然更快，而是 worst-case geometry 更匹配 simplex + $\ell_\infty$ gradient structure。

## 七、quadratic mirror map、preconditioning 与 AdaGrad

取固定 $H\succ0$：

$$
\psi(x)=\frac12x^THx,
\qquad
D_\psi(x,y)=\frac12\|x-y\|_H^2.
$$

无约束 mirror update：

$$
H x_{t+1}=Hx_t-\eta g_t,
$$

即

$$
x_{t+1}=x_t-\eta H^{-1}g_t.
$$

因此 preconditioned gradient 是 quadratic mirror descent。

若 $H_t$ 随 cumulative gradient statistics 改变，可得到 AdaGrad-like adaptive regularization。但 time-varying regularizer 的 proof 还会出现

$$
D_{\psi_{t+1}}(x,x_{t+1})
-D_{\psi_t}(x,x_{t+1})
$$

等 geometry-change terms。不能只把 Adam/AdaGrad 的 denominator 看成某个静态 Bregman divergence 后直接继承定理。

## 八、natural gradient：从 distributional trust region 推导

设 model distribution $p_\theta(y\mid x)$，objective $\mathcal L(\theta)$。希望线性化下降同时限制 model distribution 改变：

$$
\min_\delta
\nabla\mathcal L(\theta)^T\delta
\quad\text{s.t.}\quad
\mathbb E_x
D_{\mathrm{KL}}\big(
p_\theta(\cdot\mid x)
\|p_{\theta+\delta}(\cdot\mid x)
\big)
\le\varepsilon.
$$

KL 在 $\delta=0$ 的一阶项为零，二阶展开：

$$
\mathbb E_xD_{\mathrm{KL}}
\big(p_\theta\|p_{\theta+\delta}\big)
=\frac12\delta^TF(\theta)\delta
+O(\|\delta\|^3),
$$

其中 exact Fisher：

$$
\boxed{
F(\theta)
=
\mathbb E_{x\sim q(x)}
\mathbb E_{y\sim p_\theta(\cdot\mid x)}
\left[
s_\theta(x,y)s_\theta(x,y)^T
\right],
}
$$

$$
s_\theta(x,y)=\nabla_\theta\log p_\theta(y\mid x).
$$

$q(x)$ 是明确指定的 input/data distribution；inner label/response 必须从当前 model 抽样或求精确期望。

Lagrangian stationarity：

$$
\nabla\mathcal L+\lambda F\delta=0,
$$

所以方向

$$
\boxed{
\delta_{\mathrm{NG}}\propto-F^{-1}\nabla\mathcal L.
}
$$

若 trust-region radius 固定，比例因子由

$$
\frac12\delta^TF\delta=\varepsilon
$$

决定。若写成 penalty/Tikhonov step，则 step size/damping 承担比例。

## 九、exact Fisher、empirical Fisher 与 GGN 不能混名

### 9.1 exact/model Fisher

outer expectation 对 inputs，inner expectation 对 model-generated $y\sim p_\theta(\cdot\mid x)$。在 regular model 条件下：

$$
F
=-\mathbb E_{p_\theta}
\left[\nabla_\theta^2\log p_\theta\right].
$$

### 9.2 empirical Fisher

训练数据 label 固定时常计算

$$
\widehat F_{\mathrm{emp}}
=\frac1n\sum_{i=1}^n
\nabla\log p_\theta(y_i\mid x_i)
\nabla\log p_\theta(y_i\mid x_i)^T.
$$

它不是一般意义下 exact Fisher 的 unbiased estimator，因为 $y_i$ 来自 data distribution 而非当前 model。只有在 model well specified/near fit 等附加条件下才可能接近。

### 9.3 generalized Gauss–Newton

对 network output $z_\theta(x)$ 和 convex output loss $\ell(z,y)$：

$$
G_{\mathrm{GN}}
=\mathbb E\left[
J_\theta^T
\nabla_z^2\ell
J_\theta
\right].
$$

对 negative log-likelihood 与相应 exponential-family output，exact Fisher 和 GGN 有重要等价关系；对 arbitrary loss 则不是。三者都 PSD，但“PSD”不表示同一个 curvature object。

## 十、reparameterization invariance：正确命题与边界

令 $\theta=\phi(\alpha)$ 是同维 smooth locally invertible reparameterization，Jacobian $J=\partial\theta/\partial\alpha$ nonsingular。gradient covector 与 Fisher transform：

$$
\nabla_\alpha\mathcal L
=J^T\nabla_\theta\mathcal L,
\qquad
F_\alpha=J^TF_\theta J.
$$

在 exact invertible smooth reparameterization、exact Fisher、exact inverse 与 infinitesimal update 下，natural-gradient tangent vector 表示同一个 distribution-space direction：

$$
J F_\alpha^{-1}\nabla_\alpha\mathcal L
=F_\theta^{-1}\nabla_\theta\mathcal L.
$$

但以下会破坏 exact invariance：

- finite step 后参数映射的 higher-order terms；
- singular/noninvertible/redundant parameterization；
- damping $F+\lambda I$，因为 identity matrix 不按 tensor transformation；
- diagonal/block/K-FAC approximation；
- empirical Fisher；
- momentum、clipping、weight decay 与 optimizer state；
- stochastic estimator 和 finite batch。

因此更准确的说法是“natural gradient 具有理想化的 first-order reparameterization invariance”，而不是“任何叫 natural optimizer 的实现都参数化无关”。

## 十一、mirror descent 与 natural gradient 的关系

两者都可写成：

$$
\text{linearized objective}
+\text{geometry-controlled movement}.
$$

mirror descent 用

$$
D_\psi(\theta,\theta_t)
\approx\frac12
(\theta-\theta_t)^T
\nabla^2\psi(\theta_t)
(\theta-\theta_t),
$$

natural gradient 用 local KL：

$$
D_{\mathrm{KL}}(p_{\theta_t}\|p_\theta)
\approx\frac12
(\theta-\theta_t)^TF(\theta_t)(\theta-\theta_t).
$$

若存在 potential $\psi$ 使

$$
\nabla^2\psi(\theta)=F(\theta)
$$

在所用坐标区域成立，则二者 local metric 相同。在 regular exponential family 的 natural/expectation dual coordinates 中，这种联系尤其清楚：log-partition 的 Hessian 是 Fisher。

但一般 neural parameterization 中：

- arbitrary Fisher metric 未必在当前坐标全局等于某个 convex scalar potential 的 Hessian；
- mirror step 使用 finite Bregman divergence，natural gradient通常只用 local quadratic KL；
- constraints、orientation 与 retraction 不同；
- approximate Fisher 可能根本不对应 exact divergence。

所以“natural gradient 就是 mirror descent”只能带明确条件陈述。

## 十二、singular Fisher、damping 与 scalable approximations

### 12.1 Fisher 为什么 singular

overparameterization、symmetry、dead units、nonidentifiability 都可使某些 parameter directions 不改变 distribution：

$$
\delta^TF\delta=0.
$$

这时 $F^{-1}$ 不存在。Moore–Penrose pseudoinverse 给 minimum-Euclidean-norm representative，但仍依参数表示选 representative。

### 12.2 damping

常用

$$
(F+\lambda I)\delta=-g.
$$

它改善 conditioning，并把 step 变成 KL curvature 与 Euclidean penalty 的混合。$\lambda$ 不是纯数值细节：它改变 geometry、direction 与 invariance property。

### 12.3 matrix-free 与 approximate solves

不显式形成 $F$，用 Fisher-vector products + conjugate gradient 求

$$
(F+\lambda I)\delta=-g.
$$

必须报告：

- linear solve residual；
- CG iterations/preconditioner；
- batch used for $Fv$ 与 gradient 是否相同；
- damping/trust-region acceptance；
- negative/near-zero curvature 数值处理。

### 12.4 diagonal、block 与 K-FAC

近似把 cross-coordinate/cross-layer correlations 删除或 factorize。它们降低成本但改变 operator。评估应比较：

- approximation error（若可测）；
- predicted vs actual KL；
- objective improvement per compute；
- parameterization sensitivity；
- memory/communication cost。

## 十三、Muon 与 spectral steepest descent：相关但不是同一件事

对矩阵参数 $W$，若一步大小用 spectral norm $\|\Delta W\|_2$ 衡量，linearized objective

$$
\min_{\|\Delta W\|_2\le\varepsilon}
\langle G,\Delta W\rangle
$$

的 steepest direction 与 nuclear dual norm、matrix polar factor 有关。Muon 用矩阵正交化/迭代近似产生此类 geometry-aware update，可从“矩阵范数下的最陡方向”理解。

但：

- spectral metric 不等于 model-distribution Fisher metric；
- polar/orthogonalized gradient 不自动是 natural gradient；
- 只有构造了相应 potential/divergence 并验证更新一致时，才能称为 mirror descent；
- block size、Newton–Schulz steps、scaling 与 momentum 都改变实际 optimizer。

这正是 geometry 视角的价值：它帮助分类，而不是把所有 preconditioning 算法混为一类。

## 十四、AI 接口

### 14.1 probability simplex 与 mixture weights

entropy mirror descent 自动保持 positivity/normalization，适合 mixture weights、portfolio-like allocations、attention distributions 的受约束子问题。softmax parameterization 的 Euclidean gradient并不自动等于 simplex 上 mirror descent。

### 14.2 variational inference

exponential-family natural parameters、expectation parameters与 log-partition/negative entropy 构成 Legendre duality。natural gradient 可在 distribution manifold 上改善 coordinate conditioning，但 Monte Carlo estimator、amortization 与 constrained family 都引入额外误差。

### 14.3 reinforcement learning

TRPO-like 方法用 expected KL 近似 trust region。policy Fisher 依赖 state visitation distribution；旧 policy/new policy 的 KL orientation、sampling distribution 和 advantage estimator 都必须注明。finite-step line search 是为控制二阶近似失真，不是装饰。

### 14.4 large neural training

Fisher/K-FAC 类方法、AdaGrad/Adam、Shampoo、Muon 都在做不同意义的 geometry/preconditioning。比较时应统一：

- movement norm/divergence；
- curvature/statistics estimator；
- block/factorization；
- damping/normalization；
- compute and memory budget；
- convergence statement 是 convex regret、stationarity 还是 empirical scaling。

## 十五、数值验收合同

mirror descent 至少报告：

1. mirror potential 与 domain；
2. strong-convexity norm 及 dual norm；
3. step schedule；
4. Bregman projection accuracy；
5. boundary/support handling；
6. $D_\psi(x_{t+1},x_t)$ 与 gradient dual norm。

natural gradient 至少报告：

1. model Fisher / empirical Fisher / GGN 的精确定义；
2. input 与 output sampling distribution；
3. block/diagonal/K-FAC 等 approximation；
4. damping、CG tolerance 与 solve residual；
5. predicted quadratic KL 与 measured actual KL；
6. accepted step/line search；
7. singular directions/pseudoinverse policy；
8. parameterization、normalization 与 optimizer state；
9. batch noise 和 random seed；
10. improvement per wall-clock 与 memory，而不只 iteration count。

## 十六、常见误区

1. **Bregman divergence 是 metric**：通常不 symmetric 且无 triangle inequality；
2. **mirror descent 就是先做 Euclidean gradient再换变量**：constraints 下还含 Bregman projection；
3. **entropy update 可以从零恢复 support**：multiplicative zero 会保持零；
4. **换 geometry 只影响常数**：它会改变 dual norm 与 dimension dependence；
5. **AdaGrad 定理可由固定 quadratic mirror map 直接得到**：time-varying regularizer 需额外项；
6. **empirical Fisher 等于 Fisher**：采样分布不同；
7. **GGN 与 Fisher 对任何 loss 都相等**：只在特定 likelihood/output structure 下；
8. **natural gradient 完全参数化不变**：finite step、damping 与 approximation 会破坏；
9. **$F+\lambda I$ 只是防除零**：它改变 geometry；
10. **Muon 是 natural gradient**：spectral geometry 与 Fisher geometry 不同。

## 十七、掌握标准

### Level 1：识别

- 写出 $D_\psi$、mirror step 与 Fisher；
- 区分 exact/empirical Fisher/GGN。

### Level 2：手算

- 推 Euclidean 与 entropy updates；
- 解一个小型 KL trust-region natural step。

### Level 3：证明

- 证明 three-point identity 和 regret bound；
- 推导 reparameterization transformation law。

### Level 4：迁移

- 为 simplex/matrix/distribution problem 选择 geometry；
- 审计 Fisher approximation/damping；
- 判断某 optimizer 是否真对应 mirror/natural gradient。

## 十八、自检问题

1. Bregman divergence 的非负性用了什么？
2. 为什么 $D_\psi(x,y)$ 一般不等于 $D_\psi(y,x)$？
3. constraints 怎样改变 dual-coordinate update？
4. entropy mirror step 如何保持 simplex？
5. three-point identity 怎样产生 telescope？
6. geometry 为什么同时决定 primal norm 与 gradient dual norm？
7. exact Fisher 的 inner response 从哪个 distribution 取？
8. empirical Fisher 为什么通常不是 exact Fisher？
9. damping 怎样破坏 exact invariance？
10. Muon 的 matrix spectral geometry 与 Fisher 有什么本质差别？

## 十九、来源与证据边界

1. Stanford EE364B, [Mirror Descent slides](https://web.stanford.edu/class/ee364b/lectures/mirror_descent_slides.pdf)：Bregman divergence、mirror update、regret proof 与 exponentiated gradient；
2. MIT OCW, [6.253 Lecture Notes](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/pages/lecture-notes/) Lecture 24：entropy proximal mappings 与 related algorithms；
3. Beck & Teboulle, *Mirror Descent and Nonlinear Projected Subgradient Methods*, 2003：convex mirror-descent framework；
4. Amari, *Natural Gradient Works Efficiently in Learning*, 1998：information geometry 与 natural gradient；
5. Martens, [New Insights and Perspectives on the Natural Gradient Method](https://jmlr.org/papers/v21/17-678.html), JMLR 2020：Fisher/GGN、damping、trust region、invariance 与 approximation 边界；
6. [科学空间：Muon 优化器赏析](https://spaces.ac.cn/archives/10592) 与 [流形上的最速下降](https://spaces.ac.cn/archives/11215)：矩阵范数与 manifold steepest-direction 的中文 AI 入口。

> [!info] 证据分工
> Stanford/MIT 与 Beck–Teboulle 承担 mirror-descent theorem；Amari/Martens 承担 natural-gradient formal theory；科学空间承担 Muon/流形几何的问题入口。Muon 与 natural gradient 的区分是按 movement geometry 作出的结构判断，不将博客中的启发性解释升级为普遍等价定理。

## 二十、配套训练

- 习题：[[习题 - 镜像下降、Bregman 几何与自然梯度]]
- 详解：[[解答 - 镜像下降、Bregman 几何与自然梯度]]
- 前驱：[[梯度、方向导数与最陡方向]]、[[投影、约束与可行方向]]
- 后继：[[非凸优化、鞍点与深度网络损失地形]]
