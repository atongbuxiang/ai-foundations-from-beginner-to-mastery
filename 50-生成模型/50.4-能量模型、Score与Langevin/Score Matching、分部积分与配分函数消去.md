---
type: concept
status: verified
area: [generative-models, score-matching, statistics]
node_id: GEN-27
prerequisites: ["[[能量模型、未归一化密度与配分函数]]", "[[多重积分、换元公式与积分变换]]"]
related: ["[[去噪 Score Matching、Tweedie 公式与条件期望]]", "[[时间反演、score 与扩散生成动力学]]"]
sources: ["[[S-2005-Hyvarinen-Score-Matching]]", "[[S-2023-Su-9509-得分匹配与条件得分匹配]]"]
exercises: ["[[习题 - Score Matching、分部积分与配分函数消去]]"]
solutions: ["[[解答 - Score Matching、分部积分与配分函数消去]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-score-matching-integration-parts-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Score Matching、分部积分与配分函数消去

> [!abstract] 本节主问题
> Score matching 不比较 density 数值，而比较关于数据坐标的 log-density 梯度。$Z_\theta$ 对 $x$ 是常数，因此自动消失；未知数据 score 再通过分部积分消去。这个漂亮结论不是无条件代数：连续性、二阶导数、可积性和边界通量都是定理的一部分。

## 一、先分清两种 score

统计学里常见 parameter score：

$$
\nabla_\theta\log p_\theta(x).
$$

生成模型本卷所说的 data/Stein score 是：

$$
s_p(x):=\nabla_x\log p(x).
$$

一个对参数求导，一个对样本坐标求导。下文的 score 均指后者。

对 EBM，

$$
\log p_\theta(x)=-E_\theta(x)-\log Z_\theta,
$$

而 $Z_\theta$ 不依赖 $x$，故

$$
\boxed{s_\theta(x)=-\nabla_xE_\theta(x).}
$$

这一步消除了配分函数，却没有自动给出训练目标，因为真实 $s_*$ 仍未知。

## 二、Fisher divergence

定义

$$
J_F(\theta)
=\frac12 E_{X\sim p_*}
\|s_\theta(X)-s_*(X)\|^2.
$$

展开：

$$
J_F
=E_{p_*}\left[
\frac12\|s_\theta\|^2-s_\theta^\top s_*
\right]
+C_*,
$$

其中 $C_*=\frac12E\|s_*\|^2$ 与 $\theta$ 无关。困难项是

$$
-E_{p_*}[s_\theta^\top s_*]
=-\sum_{i=1}^d\int s_{\theta,i}(x)\partial_i p_*(x)dx.
$$

## 三、逐坐标分部积分

对每个坐标 $i$，在边界项消失时：

$$
\begin{aligned}
-\int s_{\theta,i}\partial_ip_*dx
&=-\left[ s_{\theta,i}p_*\right]_{\partial\mathcal X}
+\int p_*\partial_i s_{\theta,i}dx\\
&=E_{p_*}[\partial_i s_{\theta,i}].
\end{aligned}
$$

求和得到 Hyvärinen objective：

$$
\boxed{
J_F(\theta)
=E_{p_*}\left[
\frac12\|s_\theta(X)\|^2
+\nabla\cdot s_\theta(X)
\right]+C_* .}
$$

右侧只需数据样本与模型 score 的导数。

## 四、写成 energy 形式

由于 $s_\theta=-\nabla E_\theta$，

$$
\nabla\cdot s_\theta=-\Delta E_\theta,
$$

所以

$$
\boxed{
J_{SM}(\theta)
=E_{p_*}\left[
\frac12\|\nabla_xE_\theta(X)\|^2
-\Delta_xE_\theta(X)
\right]
}
$$

忽略与 $\theta$ 无关常数。这绕开 MCMC model phase，却引入输入 Hessian trace $\Delta E$ 的计算成本。

## 五、边界项不能凭感觉删掉

在 $\mathbb R^d$ 上通常要求 $p_*(x)s_{\theta,i}(x)$ 在无穷远足够快衰减。在有界区域 $\Omega$ 上，散度定理给表面项

$$
\int_{\partial\Omega}p_*(x)s_\theta(x)^\top n(x)dS.
$$

若它不为零，朴素 SM objective 与 Fisher divergence 不再只差常数。对非负数据、simplex、离散变量或流形数据，需要加权/广义/离散 score matching，而不能照抄欧氏公式。

## 六、Score 是否唯一确定 density

若连通区域上 $s_p=s_q$，则

$$
\nabla(\log p-\log q)=0,
$$

所以 $\log p-\log q=C$；归一化后 $p=q$。但若 support 有多个不连通分量，局部 score 看不到各分量之间的相对质量常数。这是单尺度、流形/分离模式下的重要可辨识边界。

## 七、高维计算：trace 与 sliced 近似

$\nabla\cdot s=\operatorname{tr}(\nabla_xs)$ 可用 Hutchinson identity：若 $E[vv^\top]=I$，

$$
\operatorname{tr}J_s
=E_v[v^\top J_s v].
$$

自动微分可计算 Jacobian-vector product，但有限 probe 引入 Monte Carlo variance。它省内存/算力，不改变 boundary 条件，也不自动保证 learned vector field 可积为某个全局 energy。

## 八、图：两次“消去”分别靠什么

先看图回答：$Z_\theta$ 消失和 $s_*$ 消失，分别依赖哪一个不同理由？

![[00-知识库管理/_assets/figures/generative-models/fig-score-matching-integration-parts-v1.svg|900]]

> [!figure] 图 50.4-03　Score Matching 的配分函数消去与分部积分链
> 左侧以 $x$-gradient 消去 $\log Z_\theta$；中间展开 Fisher divergence；右侧以分部积分将真实 score 转移为模型 divergence，并显式保留 boundary flux。来源：依据 Hyvärinen 2005 独立重绘。

**怎样读图**：第一道箭头是“常数对 $x$ 求导为零”，不需要分部积分；第二道箭头才需要把导数从 $p_*$ 转移到 $s_\theta$。红色边界框若不为零，最终 objective 就缺项。

**图没有证明什么**：图不证明任意 support 都满足边界条件，不证明有限神经网络能达到真实 score，也不证明 trace estimator 没有方差。

## 九、本节回顾

- 本卷 score 是 $\nabla_x\log p$，不是 parameter score；
- $x$-gradient 消去 $Z_\theta$；分部积分消去未知数据 score；
- energy 形式包含 gradient norm 与 Laplacian；
- boundary、support 连通性与二阶计算不可省略；
- score matching 避开模型相，但没有免费消除所有统计和计算困难。

## 十、练习与独立详解

- [[习题 - Score Matching、分部积分与配分函数消去]]
- [[解答 - Score Matching、分部积分与配分函数消去]]
