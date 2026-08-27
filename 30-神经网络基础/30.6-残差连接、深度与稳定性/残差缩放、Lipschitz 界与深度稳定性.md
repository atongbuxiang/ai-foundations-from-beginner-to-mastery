---
type: derivation
status: draft
area: [neural-networks/residual-stability, lipschitz, perturbation-analysis]
aliases: [Residual Scaling and Depth Stability, Residual Lipschitz Bounds]
node_id: NN-44
prerequisites: ["[[残差块 Jacobian 与梯度直通]]", "[[ResNet 的 ODE 与离散动力系统视角]]", "[[矩阵范数]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[正交初始化与 Dynamical Isometry]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[浮点数与舍入误差]]", "[[深度、有效路径与稳定性证据地图]]"]
sources: ["[[S-2018-Haber-Ruthotto-Stable-Architectures]]", "[[S-2022-Su-8994-Why-Residual]]", "[[S-2018-Su-6051-Lipschitz约束]]", "[[S-2018-Lu-Numerical-ODE-Networks]]"]
exercises: ["[[习题 - 残差缩放、Lipschitz 界与深度稳定性]]"]
solutions: ["[[解答 - 残差缩放、Lipschitz 界与深度稳定性]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-residual-scaling-lipschitz-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 残差缩放、Lipschitz 界与深度稳定性

> [!abstract] 本章主问题
> residual scale $\alpha_\ell$ 同时控制单层状态扰动、branch Jacobian、参数梯度和数值增量。确定性 worst-case 稳定的核心账本是 $\sum_\ell |\alpha_\ell|L_\ell$，而不是只看每层“很小”；$1/N$ 与 $1/\sqrt N$ 分别服务最坏乘积与随机二阶矩，不能互换。更重要的是，$F$ 小 Lipschitz 并不让 $I+\alpha F$ 自动收缩，收缩还需要方向性的耗散条件。

## 一、学习目标

读完本节，你应能：

1. 写出带 scale residual chain 的 two-trajectory recurrence；
2. 推导 product bound、指数界和带 forcing 的离散 Gronwall；
3. 给出 residual block 的 bi-Lipschitz 充分条件；
4. 解释为什么 $\operatorname{Lip}(F)<1$ 不代表 $I+F$ contraction；
5. 用 one-sided Lipschitz 推导真正的收缩条件；
6. 区分 $1/N$ worst-case scaling 与 $1/\sqrt N$ variance scaling；
7. 审计 projection、local/global bound、roundoff 与 mixed precision；
8. 区分 sensitivity、robustness、optimization 与 generalization。

## 二、带 scale 的 residual chain

设

$$
x_{\ell+1}
=x_\ell+\alpha_\ell F_\ell(x_\ell),
\qquad
\ell=0,\dots,N-1.
$$

其中

$$
F_\ell:\mathbb R^D\to\mathbb R^D,
\qquad
\alpha_\ell\in\mathbb R.
$$

$\alpha_\ell$ 可能是固定常数、$1/N$、$1/\sqrt N$、可学习 gate、初始化 scale 或 stochastic-depth mask 的一部分。

## 三、两条 trajectory 的单步扰动

取两个输入 $x_\ell,\widetilde x_\ell$，定义

$$
\delta_\ell=x_\ell-\widetilde x_\ell.
$$

若 $F_\ell$ 在所考虑 domain 上是 $L_\ell$-Lipschitz，则

$$
\begin{aligned}
\delta_{\ell+1}
&=\delta_\ell
+\alpha_\ell\left[F_\ell(x_\ell)-F_\ell(\widetilde x_\ell)\right],\\
\|\delta_{\ell+1}\|
&\le
\left(1+|\alpha_\ell|L_\ell\right)\|\delta_\ell\|.
\end{aligned}
$$

记

$$
q_\ell=1+|\alpha_\ell|L_\ell.
$$

## 四、跨层 product 与指数界

迭代得到

$$
\boxed{
\|\delta_N\|
\le
\prod_{\ell=0}^{N-1}q_\ell\,\|\delta_0\|
}.
$$

由 $1+z\le e^z$，

$$
\boxed{
\|\delta_N\|
\le
\exp\left(\sum_{\ell=0}^{N-1}|\alpha_\ell|L_\ell\right)
\|\delta_0\|
}.
$$

因此一个自然的 depth-uniform 充分条件是

$$
\sup_N\sum_{\ell=0}^{N-1}|\alpha_\ell|L_\ell<\infty.
$$

这只是上界充分条件，不是必要条件；方向相消、耗散和结构对称可比它更稳定。

## 五、带每层误差的离散 Gronwall

若受扰执行为

$$
\widetilde x_{\ell+1}
=\widetilde x_\ell
+\alpha_\ell F_\ell(\widetilde x_\ell)
+\xi_\ell,
$$

其中 $\xi_\ell$ 可表示 rounding、量化、通信、近似 branch 或 solver defect，则

$$
\|\delta_{\ell+1}\|
\le q_\ell\|\delta_\ell\|+\|\xi_\ell\|.
$$

展开为

$$
\boxed{
\|\delta_N\|
\le
\left(\prod_{j=0}^{N-1}q_j\right)\|\delta_0\|
+\sum_{k=0}^{N-1}
\left(\prod_{j=k+1}^{N-1}q_j\right)\|\xi_k\|
}.
$$

早期误差要穿过更多后续 block，因此通常具有更长 amplification tail。

## 六、单块 upper/lower bound 与可逆性

令

$$
G(x)=x+\alpha F(x),
\qquad
\operatorname{Lip}(F)\le L.
$$

上界：

$$
\|G(x)-G(y)\|
\le(1+|\alpha|L)\|x-y\|.
$$

下界：

$$
\|G(x)-G(y)\|
\ge(1-|\alpha|L)\|x-y\|.
$$

若

$$
|\alpha|L<1,
$$

则 $G$ 是 injective，并且逆映射在其像上满足

$$
\operatorname{Lip}(G^{-1})
\le\frac1{1-|\alpha|L}.
$$

这给出 residual flow 可逆方法的基础充分条件，但它可能保守，并且 projection、dimension change 和非确定操作会破坏前提。

## 七、关键陷阱：branch 小不等于 block 收缩

由上界只能得到

$$
\operatorname{Lip}(I+\alpha F)
\le1+|\alpha|L,
$$

右边通常大于 1。即使 $L<1$，也不能推出 block contraction。

最简单反例是

$$
F(x)=\beta x,
\qquad
0<\beta<1.
$$

虽然 $F$ 是 $\beta$-Lipschitz，

$$
G(x)=(1+\alpha\beta)x
$$

在 $\alpha>0$ 时反而放大。

## 八、one-sided Lipschitz 与真正的方向条件

假设对所有 $x,y$，

$$
\langle x-y,F(x)-F(y)\rangle
\le\mu\|x-y\|^2,
$$

并且 $F$ 是 $L$-Lipschitz。对 $\alpha\ge0$，

$$
\begin{aligned}
\|G(x)-G(y)\|^2
&=\|\delta+\alpha\Delta F\|^2\\
&=\|\delta\|^2
+2\alpha\langle\delta,\Delta F\rangle
+\alpha^2\|\Delta F\|^2\\
&\le
\left(1+2\alpha\mu+\alpha^2L^2\right)\|\delta\|^2.
\end{aligned}
$$

若 $\mu<0$ 且

$$
0<\alpha<\frac{-2\mu}{L^2},
$$

则括号小于 1，block 才有 contraction certificate。$\mu$ 描述方向性耗散，不能由非负的普通 Lipschitz 常数替代。

## 九、标量 dissipative 例子

令

$$
F(x)=-\beta x,
\qquad
\beta>0.
$$

则

$$
x^+=(1-\alpha\beta)x.
$$

收缩当且仅当

$$
|1-\alpha\beta|<1
\iff
0<\alpha\beta<2.
$$

其中：

- $0<\alpha\beta<1$：同号单调衰减；
- $1<\alpha\beta<2$：变号振荡但 norm 衰减；
- $\alpha\beta=2$：norm 不变；
- $\alpha\beta>2$：离散不稳定。

这正是连续耗散与 Euler step-size 条件的结合。

## 十、$1/N$ 与 $1/\sqrt N$ 解决不同账本

假设 $L_\ell\le C$。

### 10.1 worst-case 同向累积

若

$$
\alpha_\ell=\frac1N,
$$

则

$$
\sum_{\ell=0}^{N-1}\alpha_\ell L_\ell\le C,
$$

所以 deterministic bound 不超过 $e^C$。

### 10.2 随机不相关二阶矩

若 branch increments 近似零均值、不相关且方差 $O(1)$，则

$$
\operatorname{Var}\left(\sum_{\ell=0}^{N-1}\alpha F_\ell\right)
\approx N\alpha^2O(1).
$$

取

$$
\alpha=\frac1{\sqrt N}
$$

可让方差保持 $O(1)$。

但 deterministic worst-case 指数账本变为

$$
\exp(C\sqrt N),
$$

并不 uniform bounded。$1/\sqrt N$ 需要随机方向、相关性或更具体 mean-field 假设，不能冒充 worst-case theorem。

## 十一、参数梯度也被 scale 改写

对

$$
x_{\ell+1}=x_\ell+\alpha_\ell F_\ell(x_\ell;\theta_\ell),
$$

有

$$
\nabla_{\theta_\ell}\mathcal L
=\alpha_\ell
J_{\theta_\ell}F_\ell^\mathsf T
g_{\ell+1}.
$$

所以减小 $\alpha_\ell$ 也减小 branch 参数的第一步梯度。它可能防止 update explosion，也可能让学习过慢；学习率、optimizer preconditioner、weight decay 和 warm-up 必须一起登记。

科学空间的“为什么需要残差”提供了这个尺度入口，但训练期结论仍需区分初始化量级、全程动态与任务实验。

## 十二、projection shortcut 的修正

若

$$
x_{\ell+1}=P_\ell x_\ell+\alpha_\ell F_\ell(x_\ell),
$$

则

$$
\operatorname{Lip}(G_\ell)
\le
\|P_\ell\|+|\alpha_\ell|L_\ell.
$$

若 $P_\ell$ 降维，则不存在正的全空间 lower Lipschitz bound；信息已可能在 shortcut 中丢失。若 $P_\ell$ 是 orthogonal/isometry，才可保留 identity-like norm 基线。

## 十三、local、empirical 与 global Lipschitz

必须区分：

- **global**：domain 所有 $x,y$ 的统一常数；
- **restricted-domain**：只在指定集合；
- **local Jacobian**：某一点的 $\|J(x)\|$；
- **empirical**：有限样本/方向上的估计；
- **expected**：对数据或随机参数取期望。

乘积上界使用 global 或沿 tube 有效的 uniform 常数。几批数据上的 JVP gain 小，不能直接证明全空间 certificate。

## 十四、合法上界也可能极松

对 composition，layerwise spectral-norm product 是合法 upper bound，却可能：

1. 每层最坏方向彼此不对齐；
2. residual branch 与 identity 相消；
3. activation mask 限制 reachable directions；
4. data manifold 远小于 ambient space；
5. non-normal transient 让局部现象不能由 eigenvalue 概括。

所以应同时报告 theorem bound、power-iteration estimate、随机 JVP 分布与真实扰动实验，而不只给一个数字。

## 十五、有限精度 forcing

浮点 residual update 可抽象为

$$
\widetilde x_{\ell+1}
=\widetilde x_\ell
+\alpha_\ell F_\ell(\widetilde x_\ell)
+\xi_\ell.
$$

$\xi_\ell$ 包括：

- branch compute rounding；
- cast 到 residual dtype；
- addition rounding；
- all-reduce/communication reduction order；
- quantization/dequantization；
- checkpoint recomputation mismatch。

若 $\alpha F$ 太小，它可能被大 residual stream 的 ulp 吞没；若刻意放大后再相消，又可能引入 cancellation。稳定缩放必须与 accumulator dtype 一起设计。

## 十六、敏感性不等于鲁棒性或泛化

小 Lipschitz 上界可限制输入扰动放大，但以下结论仍需额外条件：

- adversarial robustness 需要 margin 与威胁模型；
- generalization 需要数据分布、容量和学习算法；
- optimization 需要参数 Jacobian/Hessian 与 trajectory；
- calibration 和 OOD 不是 input Lipschitz 的直接推论。

因此“不敏感”不能自动翻译成“更准、更稳健、更泛化”。

## 十七、图：尺度账本、收缩门与误差累积

先看图回答：为什么 $1/N$ 能控制 worst-case exponent，而 $1/\sqrt N$ 只自然控制不相关方差？为什么 $\operatorname{Lip}(F)<1$ 仍不足以让 $I+F$ 收缩？早期误差怎样穿过后续乘积？

![[00-知识库管理/_assets/figures/neural-networks/fig-residual-scaling-lipschitz-v2.svg|900]]

> [!figure] 图 30.6-04　残差深度稳定性的三本账：乘积、方向与 forcing
> 左栏把 $\prod(1+\alpha L)$ 压成 $\exp(\sum\alpha L)$ 并对比 $1/N$、$1/\sqrt N$；中栏用 expanding 与 dissipative scalar branch 区分“小 Lipschitz”与 contraction；右栏展示每层误差 $\xi_k$ 被后续 gain 加权的离散 Gronwall。来源：依据 Haber–Ruthotto 2018、苏剑林 2022 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_residual_foundations_v2.py]] 确定性生成。

**怎样读图**：先锁定是 deterministic worst-case 还是 stochastic second moment，再检查 branch 与差向量的夹角，最后沿右栏看每个误差发生位置后的剩余 amplification tail。

**图没有证明什么**：图没有证明 $1/N$ 是所有任务的最优缩放，也没有把 layerwise Lipschitz upper bound 当作真实增益或泛化误差。

## 十八、最小验收

1. 推导 two-trajectory 单步界；
2. 推导 product 与 exponential bound；
3. 展开带 forcing 的离散 Gronwall；
4. 证明 $1-|\alpha|L$ lower bound；
5. 给出“小 branch 不等于 contraction”的反例；
6. 推导 one-sided Lipschitz contraction 条件；
7. 复算 scalar dissipative 四个区间；
8. 区分 $1/N$ 与 $1/\sqrt N$；
9. 把 projection norm 加入单层界；
10. 设计 local/global/empirical 与 dtype 联合审计。

> [!summary]
> residual scale 的可靠分析必须同时有三本账：确定性乘积由 $\sum|\alpha_\ell|L_\ell$ 控制，收缩需要 one-sided dissipativity，随机二阶矩还依赖相关性；每层数值或近似误差则按剩余 gain 累积。把这些对象分开，才能从“小 residual”走到可审计的深度稳定性。

- [[残差连接、深度与稳定性 MOC]]
- [[习题 - 残差缩放、Lipschitz 界与深度稳定性]]
- [[解答 - 残差缩放、Lipschitz 界与深度稳定性]]
