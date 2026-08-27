---
type: derivation
status: verified
area: [generative-models, likelihood, information-theory]
aliases: [生成模型最大似然, NLL与前向KL]
node_id: GEN-03
prerequisites: ["[[生成建模的对象、样本空间与数据分布]]", "[[最大似然估计与 MAP]]", "[[交叉熵与 KL 散度]]"]
related: ["[[生成建模对象、似然与自回归 MOC]]", "[[概率链式分解、顺序选择与自回归生成]]", "[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]"]
sources: ["[[S-2018-Su-6016-fGAN与变分散度]]"]
exercises: ["[[习题 - 最大似然、交叉熵与前向 KL]]"]
solutions: ["[[解答 - 最大似然、交叉熵与前向 KL]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gen-mle-kl-ledgers-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 最大似然、交叉熵与前向 KL

> [!abstract] 本节主问题
> 对来自 $P_*$ 的数据，最大化模型似然等价于最小化经验 NLL；其总体版本是最小化 cross-entropy，并在 $P_*$ 固定且相关熵有限时等价于最小化 $D_{\mathrm{KL}}(P_*\Vert P_\theta)$。这个等价不消除有限样本、模型错设、优化误差，也不能把 density 数值直接当样本质量。

## 一、从数据集到经验目标

给 iid 数据 $x^{(1)},\ldots,x^{(n)}\sim P_*$，似然是

$$
L_n(\theta)=\prod_{i=1}^n p_\theta(x^{(i)}).
$$

因为对数严格递增，最大化 $L_n$ 等价于最大化 log-likelihood：

$$
\ell_n(\theta)=\sum_{i=1}^n\log p_\theta(x^{(i)}).
$$

再乘 $-1/n$ 得经验负对数似然

$$
\widehat R_n(\theta)
=-\frac1n\sum_{i=1}^n\log p_\theta(x^{(i)})
=\mathbb E_{X\sim\widehat P_n}[-\log p_\theta(X)].
$$

乘正数与加模型无关常数不改变 argmin，但会改变报告数值、梯度缩放和超参数解释，不能随意省略归约口径。

## 二、总体风险是 cross-entropy

理想总体目标为

$$
R(\theta)=\mathbb E_{X\sim P_*}[-\log p_\theta(X)].
$$

离散情形这就是

$$
H(P_*,P_\theta)=-\sum_x p_*(x)\log p_\theta(x).
$$

连续情形把和换为相对同一参考测度的积分；此时 cross-entropy/differential entropy 会随坐标尺度变化，但 KL 在适当变换下保持不变。

## 三、逐步推导 forward KL

假设 $P_*\ll P_\theta$ 且相关期望有限：

$$
\begin{aligned}
D_{\mathrm{KL}}(P_*\Vert P_\theta)
&=\mathbb E_{P_*}\left[\log\frac{p_*(X)}{p_\theta(X)}\right]\\
&=\mathbb E_{P_*}[\log p_*(X)]
 -\mathbb E_{P_*}[\log p_\theta(X)]\\
&=-H(P_*)+R(\theta).
\end{aligned}
$$

于是

$$
R(\theta)=H(P_*)+D_{\mathrm{KL}}(P_*\Vert P_\theta).
$$

$H(P_*)$ 对 $\theta$ 不变，所以 population MLE 与 forward KL 有相同 argmin。注意：训练时不需要知道 $p_*$ 或 $H(P_*)$；样本平均直接估计 $R(\theta)$。

> [!warning] 等价的准确含义
> 这里是“总体目标相差与 $\theta$ 无关的常数，因而 argmin 相同”。经验 NLL 不是经验分布与连续模型 KL 的无条件等式；连续经验分布是原子测度，往往不对 Lebesgue-density 模型绝对连续。

## 四、forward KL 为何惩罚漏模式

若存在 $A$ 使 $P_*(A)>0$ 但 $P_\theta(A)=0$，则 forward KL 为 $+\infty$。因此在模型可表达、目标准确估计并优化良好时，它强烈反对漏掉数据支持。

但“forward KL 必然产生模糊样本”不是定理。若模型族受限，例如用单个 Gaussian 拟合双峰数据，最优解可能扩大方差覆盖两个峰；模糊是模型族与目标互动的结果，而非 KL 方向的唯一后果。

## 五、最小手算：Bernoulli

设真实 $P_*(1)=0.75$，模型 $P_q(1)=q$。总体 NLL

$$
R(q)=-0.75\log q-0.25\log(1-q).
$$

求导：

$$
R'(q)=-\frac{0.75}{q}+\frac{0.25}{1-q}.
$$

令其为零，

$$
0.25q=0.75(1-q)\Longrightarrow q=0.75.
$$

二阶导

$$
R''(q)=\frac{0.75}{q^2}+\frac{0.25}{(1-q)^2}>0,
$$

所以是唯一全局最小。若十个样本中有 8 个 1，经验 MLE 是 $\hat q=0.8$；总体最优与有限样本最优不同，差异由 sampling error 解释。

## 六、条件最大似然

条件生成用联合数据 $(C,X)\sim P_*$：

$$
R_{\mathrm{cond}}(\theta)
=\mathbb E_{P_*(C,X)}[-\log p_\theta(X\mid C)].
$$

按条件分解，

$$
R_{\mathrm{cond}}(\theta)
=H_{P_*}(X\mid C)
+\mathbb E_{C\sim P_*}
D_{\mathrm{KL}}\left(P_*(X\mid C)\Vert P_\theta(X\mid C)\right).
$$

因此它按训练条件分布 $P_*(C)$ 加权。部署条件分布改变时，平均表现也会改变；罕见条件可能因训练权重小而学得差。

## 七、四类误差不能由 KL 恒等式消失

设 $\hat\theta$ 是实际训练结果，$\theta^\star_\mathcal M$ 是模型族总体最优：

| 误差 | 问题 |
|---|---|
| approximation | 模型族中是否存在接近 $P_*$ 的分布？ |
| estimation | $\widehat R_n$ 与 $R$ 相差多少？ |
| optimization | 算法是否找到经验/总体近优点？ |
| protocol | dequantization、tokenization、mask/reduction 是否定义了同一目标？ |

再加生成时 sampler/decoder error，才是完整系统账。

## 八、likelihood 不是唯一评价器

平均 NLL 是 proper scoring rule，适合评价概率分布；但有限数据上的样本质量、语义、条件忠实、隐私和成本并不被单一标量完全概括。模型还可能利用低层背景统计提高 image likelihood，却不改善人类感知语义。正确结论不是“likelihood 无用”，而是“likelihood 回答一个明确但不完备的问题”。

## 九、科学空间研读框

[[S-2018-Su-6016-fGAN与变分散度]]展示不同 divergence 可通过变分形式进入生成训练，适合作为“目标不只有 forward KL”的入口。本节保留 MLE 的独立地位：forward KL 等价是直接恒等式，不依赖 discriminator；f-GAN 的 critic optimum、有限函数类和交替优化属于另一估计/训练账。不能因二者都出现 KL 就把训练程序称为等价。

## 十、图：从数据平均到总体 KL 的三层账

先看图回答：训练代码实际计算哪一栏，理论上希望逼近哪一栏，哪一项因为与 $\theta$ 无关而可从优化中省略？

![[00-知识库管理/_assets/figures/generative-models/fig-gen-mle-kl-ledgers-v1.svg|900]]

> [!figure] 图 50.1-03　经验 NLL、population cross-entropy 与 forward KL
> 图把有限样本估计、总体风险和 KL 恒等分解分为三阶段，并在底部列出 approximation/estimation/optimization/protocol 四类误差。来源：依据 MLE 与 KL 定义独立绘制。

**怎样读图**：从左到右追踪同一个 integrand $-\log p_\theta(x)$：先在样本上平均，再在 $P_*$ 下取期望，最后加减 $\log p_*$ 得到熵常数与 KL。

**图没有证明什么**：图不提供有限样本一致性速率，也不保证非凸优化达到全局最优，更不说明 likelihood 足以预测感知质量。

## 十一、本节回顾

- empirical MLE 最小化样本 NLL；population NLL 是 cross-entropy；
- 在绝对连续与可积条件下，它等于数据熵加 forward KL；
- 数据熵对参数不变，只能从 argmin 中省略，不能从报告口径中随意抹去；
- support 漏失会使 forward KL 发散；
- approximation、estimation、optimization、protocol 和 sampling error 必须分账。

## 十二、练习与独立详解

- [[习题 - 最大似然、交叉熵与前向 KL]]
- [[解答 - 最大似然、交叉熵与前向 KL]]
