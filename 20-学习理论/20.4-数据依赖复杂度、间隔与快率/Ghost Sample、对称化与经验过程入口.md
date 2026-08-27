---
type: theorem
status: draft
area: [learning-theory/empirical-process, probability/symmetrization]
aliases: [Ghost Sample Symmetrization, Symmetrization Lemma, 对称化引理]
node_id: LT-25
prerequisites: ["[[VC 一致收敛与泛化界]]", "[[期望、方差与矩]]", "[[协方差、相关性与条件期望]]"]
related: ["[[Rademacher 复杂度与经验复杂度]]", "[[收缩引理与 Lipschitz 损失复合]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]", "[[互信息与信息论泛化界]]"]
sources: ["[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - Ghost Sample、对称化与经验过程入口]]"]
solutions: ["[[解答 - Ghost Sample、对称化与经验过程入口]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-ghost-sample-symmetrization-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Ghost Sample、对称化与经验过程入口

> [!abstract] 本章主问题
> 对函数类 $\mathcal F$，我们想控制
> $$
> \sup_{f\in\mathcal F}(Pf-P_mf),
> \qquad
> Pf=\mathbb E f(Z),\quad P_mf=\frac1m\sum_{i=1}^mf(Z_i).
> $$
> 难点是 $Pf$ 未知且 supremum 选择的 $f$ 依赖样本。对称化分三步：用独立 ghost sample $S'$ 把 $Pf$ 写成条件期望；利用每对 $(Z_i,Z_i')$ 的 exchangeability 引入 Rademacher signs；再把双样本差拆成两个同分布的单样本随机过程。由此得到 one-sided expectation bound
> $$
> \mathbb E_S\sup_{f\in\mathcal F}(Pf-P_mf)
> \le2\mathfrak R_m(\mathcal F).
> $$
> 两侧绝对偏差需要使用 absolute Rademacher complexity 或对称化函数类；high-probability 结论还要再加 concentration。

> [!question] 初学者读完必须能回答
> 1. ghost sample 为什么能替代 $Pf$，Jensen 用在什么对象上？
> 2. Rademacher sign 表示真实 label、算法随机性，还是样本对的随机交换？
> 3. 双样本 supremum 为什么至多是两个单样本 supremum 之和？
> 4. one-sided 与 absolute symmetrization 的 convention 有何差别？
> 5. 为什么 expectation bound 不能直接写成“以概率 $1-\delta$”？

## 一、学习目标

1. 写清 $P,P_m,P_m'$ 与三层随机性的关系；
2. 从条件 Jensen 完整推出 ghost-sample inequality；
3. 证明 pairwise random swap 不改变 $(S,S')$ 联合分布；
4. 将双样本差写成 Rademacher signed process；
5. 追踪 supremum、expectation 和 absolute value 的合法交换；
6. 区分 population Rademacher complexity 与 empirical complexity；
7. 说明 bounded difference 如何把 expectation 升级为 high probability；
8. 识别 dependent data、data-dependent class 和 adaptive evaluation 下的断点。

## 二、统一记号

令 observation space 为 $\mathcal Z$，未知分布为 $P$。训练样本

$$
S=(Z_1,\ldots,Z_m)\sim P^m.
$$

函数类

$$
\mathcal F\subseteq\mathbb R^{\mathcal Z}
$$

在本节默认可测且至少可积。记

$$
Pf=\mathbb E_{Z\sim P}f(Z),
\qquad
P_mf=\frac1m\sum_{i=1}^mf(Z_i).
$$

引入独立同分布副本

$$
S'=(Z_1',\ldots,Z_m')\sim P^m,
\qquad S'\perp S,
$$

并记

$$
P_m'f=\frac1m\sum_{i=1}^mf(Z_i').
$$

Rademacher signs 为

$$
\sigma_1,\ldots,\sigma_m
\overset{\rm iid}{\sim}\operatorname{Unif}\{-1,+1\},
$$

且与 $(S,S')$ 独立。

## 三、第一步：用 Ghost Sample 替代总体期望

固定训练样本 $S$。对每个 $f$，独立同分布性给出

$$
Pf=\mathbb E_{S'}P_m'f.
$$

因此

$$
\sup_{f\in\mathcal F}(Pf-P_mf)
=
\sup_f\mathbb E_{S'}(P_m'f-P_mf).
$$

函数 $x\mapsto\sup_f x_f$ 是凸函数；也可直接使用“supremum of expectations 不超过 expectation of supremum”：

$$
\sup_f\mathbb E_{S'}X_f(S')
\le
\mathbb E_{S'}\sup_fX_f(S').
$$

令 $X_f=P_m'f-P_mf$，得到对每个固定 $S$：

$$
\sup_f(Pf-P_mf)
\le
\mathbb E_{S'}\sup_f(P_m'f-P_mf).
$$

再对 $S$ 取期望：

$$
\boxed{
\mathbb E_S\sup_f(Pf-P_mf)
\le
\mathbb E_{S,S'}\sup_f(P_m'f-P_mf).
}
$$

### 3.1 为什么方向不能反

supremum 内的最优 $f$ 可以依赖 $S'$。右侧在看到 ghost sample 后选择最有利函数，通常比先固定 $f$ 再取 $S'$ 期望更大。因此 Jensen 只给“$\le$”。

### 3.2 Ghost sample 不是验证集

$S'$ 只存在于概率空间中，算法不访问它，也不用于 model selection。真实验证集若被查看，会改变 learner/evaluation contract；proof ghost 不会。

## 四、图解三次对象变换

先回答：**图中哪一步是 inequality，哪一步是 distributional equality，哪一步使用 subadditivity？**

![[00-知识库管理/_assets/figures/learning-theory/fig-ghost-sample-symmetrization-v2.svg|900]]

> [!figure] 图 20.4.1｜总体偏差、双样本差与随机符号过程
> 左栏用 conditional Jensen 引入 ghost sample；中栏利用 sample pairs 的 exchangeability 进行随机交换；右栏把双样本 signed supremum 拆成两个单样本过程。来源：依据标准 symmetrization lemma 独立绘制；确定性 SVG，由 [[plot_rademacher_core_v2.py]] 生成。

**怎样读图。** 左栏是上界，不是等号；中栏是联合分布不变产生的等号；右栏对 supremum 使用 $\sup_f(A_f+B_f)\le\sup_fA_f+\sup_fB_f$。最终的 2 来自两个同分布单样本项。

**适用边界（图没有证明什么）。** 图没有给出 high-probability concentration、dependent sample 的替代交换、measurability 处理或 data-dependent class 的 conditional theorem；也没有把 ghost sample 当作算法所需数据。

## 五、第二步：随机交换产生 Rademacher Signs

对每个 $i$，$(Z_i,Z_i')$ 是两个 iid draws。因此

$$
(Z_i,Z_i')\overset d=(Z_i',Z_i).
$$

给定 sign $\sigma_i$，定义交换后的 pair：

$$
(\widetilde Z_i,\widetilde Z_i')
=
\begin{cases}
(Z_i,Z_i'),&\sigma_i=+1,\\
(Z_i',Z_i),&\sigma_i=-1.
\end{cases}
$$

对所有坐标独立交换后，

$$
(\widetilde S,\widetilde S')\overset d=(S,S').
$$

并且

$$
f(\widetilde Z_i')-f(\widetilde Z_i)
=\sigma_i\bigl(f(Z_i')-f(Z_i)\bigr)
$$

（若交换 convention 相反，只会把全部 $\sigma_i$ 取负，分布不变）。故

$$
\mathbb E_{S,S'}\sup_f\frac1m\sum_i(f(Z_i')-f(Z_i))
$$

$$
=
\mathbb E_{S,S',\sigma}
\sup_f\frac1m\sum_i\sigma_i(f(Z_i')-f(Z_i)).
$$

> [!important] Sign 的角色
> $\sigma_i$ 不是真实标签，不来自训练算法，也不是 bootstrap weight；它只编码第 $i$ 对 iid 样本是否交换。正因为 pair joint law 对交换不变，才可插入 signs。

## 六、第三步：把双样本过程拆开

对固定 $(S,S',\sigma)$，

$$
\begin{aligned}
&\sup_{f\in\mathcal F}
\frac1m\sum_i\sigma_i(f(Z_i')-f(Z_i))\\
&\le
\sup_f\frac1m\sum_i\sigma_if(Z_i')
+
\sup_f\frac1m\sum_i(-\sigma_i)f(Z_i).
\end{aligned}
$$

定义 signed empirical Rademacher complexity

$$
\widehat{\mathfrak R}_S(\mathcal F)
=
\mathbb E_\sigma
\left[
\sup_{f\in\mathcal F}
\frac1m\sum_{i=1}^m\sigma_if(Z_i)
\right],
$$

以及 population/expected complexity

$$
\mathfrak R_m(\mathcal F)
=\mathbb E_S\widehat{\mathfrak R}_S(\mathcal F).
$$

因为 $S,S'$ 同分布，$-\sigma\overset d=\sigma$，上面两项的期望都等于 $\mathfrak R_m(\mathcal F)$。合并前三步：

> [!theorem] One-sided expectation symmetrization
> 在可积与可测条件下，
> $$
> \boxed{
> \mathbb E_S\sup_{f\in\mathcal F}(Pf-P_mf)
> \le2\mathfrak R_m(\mathcal F).
> }
> $$

## 七、Two-Sided Gap 的 Convention

我们常需控制

$$
\sup_f|Pf-P_mf|.
$$

定义对称扩张

$$
\mathcal F_\pm=\mathcal F\cup(-\mathcal F).
$$

则

$$
\sup_{f\in\mathcal F}|Pf-P_mf|
=
\sup_{g\in\mathcal F_\pm}(Pg-P_mg).
$$

所以

$$
\mathbb E\sup_f|Pf-P_mf|
\le2\mathfrak R_m(\mathcal F_\pm).
$$

另一种做法是直接定义 absolute empirical complexity

$$
\widehat{\mathfrak R}^{\rm abs}_S(\mathcal F)
=
\mathbb E_\sigma
\sup_f\left|
\frac1m\sum_i\sigma_if(Z_i)
\right|.
$$

则可写

$$
\mathbb E\sup_f|Pf-P_mf|
\le2\mathbb E_S\widehat{\mathfrak R}^{\rm abs}_S(\mathcal F).
$$

> [!warning] 常数不能跨 convention 搬运
> 有的教材在定义中使用 $2/m$，有的把 absolute value 放进 supremum，有的默认 $\mathcal F=-\mathcal F$。引用“因子 2”前必须先对齐定义。

## 八、从 Expectation 到 High Probability

若 $f(z)\in[0,1]$，定义

$$
\Phi(S)=\sup_f(Pf-P_mf).
$$

把一个 $Z_i$ 替换为 $\widetilde Z_i$，对任意 $f$ 的经验均值至多改变 $1/m$，所以

$$
|\Phi(S)-\Phi(S^{(i)})|\le\frac1m.
$$

McDiarmid inequality 给出以至少 $1-\delta$ 的概率：

$$
\Phi(S)
\le\mathbb E\Phi(S)
+\sqrt{\frac{\log(1/\delta)}{2m}}.
$$

结合 symmetrization：

$$
\Phi(S)
\le
2\mathfrak R_m(\mathcal F)
+\sqrt{\frac{\log(1/\delta)}{2m}}.
$$

这是 population complexity 版本。若要用可从当前样本计算的 $\widehat{\mathfrak R}_S$，还要控制 empirical complexity 自身围绕 $\mathfrak R_m$ 的波动；下一节给出完整 selected bound。

## 九、一个有限函数类的最小例子

固定样本 $S=(z_1,z_2)$，假设 restrictions 为

$$
f_1(S)=(0,0),
\qquad
f_2(S)=(1,0).
$$

对四个 sign patterns：

| $(\sigma_1,\sigma_2)$ | $f_1$ score | $f_2$ score | supremum |
|---|---:|---:|---:|
| $(+,+)$ | 0 | $1/2$ | $1/2$ |
| $(+,-)$ | 0 | $1/2$ | $1/2$ |
| $(-,+)$ | 0 | $-1/2$ | 0 |
| $(-,-)$ | 0 | $-1/2$ | 0 |

因此

$$
\widehat{\mathfrak R}_S(\{f_1,f_2\})
=\frac14\left(\frac12+\frac12+0+0\right)
=\frac14.
$$

若两个函数在样本上 restrictions 相同，经验复杂度不会因为它们在样本外不同而增加。这正说明 empirical complexity 是 sample-restricted 对象。

## 十、三类常见误用

### 10.1 把 expectation inequality 当 tail bound

$$
\mathbb E\Phi\le2\mathfrak R_m
$$

没有 $\delta$，也不表示每个样本都满足。可用 Markov 得到很弱 tail，但标准高概率结果使用 bounded differences 或更精细 concentration。

### 10.2 把 Ghost sample 变成额外训练数据

证明中的 $S'$ 可无限设想而无需收集；算法若实际访问第二份数据，输出依赖关系改变，必须重新定义 learner。

### 10.3 对 dependent pairs 随意交换

若时间序列、grouped samples 或 augmentation pairs 不是 iid exchangeable，则

$$
(Z_i,Z_i')\overset d=(Z_i',Z_i)
$$

未必成立。需要 block symmetrization、mixing coefficient、martingale 或专门 dependent-process complexity。

## 十一、AI 中的对象映射

### 11.1 Batch negative 与对比学习

单个 loss term 依赖整个 batch 时，不能把它写成独立 $f(Z_i)$ 的平均再直接 symmetrize。sample unit 可能是 batch、pair graph 或 U-statistic，需要对应对称化。

### 11.2 数据增强

若同一原样本生成多个 correlated views，有效独立单位是原始 example，而不是 view 数。交换单个 view 可能破坏 joint law。

### 11.3 Foundation-model evaluation

若 prompts 由模型输出或人工反馈自适应生成，$\mathcal F$ 或 sample distribution 依赖先前 observations。应把完整 transcript 条件化，或使用 online/stability/information 工具。

### 11.4 随机训练算法

Symmetrization 控制的是 class supremum 或指定随机函数类。算法随机种子 $U$ 与 Rademacher signs $\sigma$ 是不同随机变量；若只分析 algorithm output，可条件于 $U$ 或采用 stability/PAC-Bayes 等更贴近算法的工具。

## 十二、常见错误

> [!warning] “$Pf=P_m'f$”
> 错。只有 $Pf=\mathbb E_{S'}P_m'f$；单个 ghost empirical mean 仍随机。

> [!warning] “$\sup_f\mathbb EX_f=\mathbb E\sup_fX_f$”
> 一般错，只有不等式 $\le$。右侧可让最优 $f$ 随 $S'$ 变化。

> [!warning] “Sign 是人工随机 label”
> 它在定义 Rademacher complexity 时可直观解释为随机符号，但在 symmetrization 证明中来源是 iid sample pairs 的交换。

> [!warning] “对称化已经证明泛化”
> 它只把目标归约为 complexity；若 complexity 大、loss 无界或 sampling contract 不成立，风险证书仍不可用。

## 十三、本节回顾

1. 为什么 $Pf$ 是 ghost empirical mean 的条件期望？
2. Jensen/supremum inequality 的方向是什么？
3. pairwise exchangeability 怎样产生 $\sigma_i$？
4. supremum 的 subadditivity 怎样产生两个 Rademacher 项？
5. one-sided、symmetric-hull 与 absolute complexity 怎样对应？
6. $f\in[0,1]$ 时 changing-one-sample sensitivity 为什么是 $1/m$？
7. empirical 与 population complexity 的随机对象分别是什么？
8. batch-dependent loss 会破坏哪一种 additive representation？

## 十四、来源与后继

- 原始/经典 data-dependent complexity：[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]；
- 教材交叉校准：[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]；
- 下一步：[[Rademacher 复杂度与经验复杂度]]给出结构性质、Massart lemma 与 empirical risk certificate；
- 训练闭环：[[习题 - Ghost Sample、对称化与经验过程入口]]与[[解答 - Ghost Sample、对称化与经验过程入口]]。
