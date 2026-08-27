---
type: concept
status: draft
area: [math/statistics, ai/bayesian-inference, ai/uncertainty]
aliases: [Bayesian inference, 贝叶斯推断, posterior predictive, 后验预测, credible interval]
prerequisites: ["[[条件概率、全概率与 Bayes 公式]]", "[[最大似然估计与 MAP]]", "[[统计模型、估计量与偏差方差]]", "[[Fisher 信息、Cramér–Rao 界与渐近正态性]]"]
related: ["[[MCMC 与随机模拟诊断]]", "[[假设检验、置信区间与多重比较]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[概率论与数理统计 MOC]]"]
sources: ["MIT-18.655-Lecture-3-Bayesian-Models", "MIT-18.655-Lecture-5-Prediction", "MIT-18.655-Lecture-11-Bayes-Procedures", "MIT-18.655-Lecture-18-Bayes-Asymptotics", "Gelman-et-al-Bayesian-Data-Analysis", "Gelman-Meng-Stern-1996-Posterior-Predictive", "Stan-Users-Guide-Posterior-Prediction", "Su-2018-5343-VAE-Bayesian"]
created: 2026-08-19
updated: 2026-08-27
---

# Bayesian 推断与后验预测

> [!abstract] 本章主问题
> Bayesian 推断先指定数据与未知量的联合概率模型，再用条件化把 prior 更新为 posterior；真正用于预测的对象是把参数不确定性积分掉的 posterior predictive。后验概率、credible interval 和 Bayes action 都是“给定模型与已观测数据”的条件声明，不自动拥有 frequentist coverage，也不能消除模型错设、prior sensitivity、近似推断误差或部署分布漂移。

## 学习目标

完成本节后，你应当能够：

1. 从 joint model 推导 prior、likelihood、evidence、posterior 与 posterior predictive；
2. 解释参数为何在 Bayesian model 中是随机变量，而观测后真值并非“又随机了一次”；
3. 推导 Beta–Binomial、Dirichlet–Categorical 与 Normal–Normal conjugate update；
4. 解释 posterior mean、median、MAP 分别对应哪些 loss；
5. 区分 equal-tail、HPD credible set 与 frequentist confidence interval；
6. 用 posterior predictive 分解 aleatoric 与 parameter uncertainty；
7. 区分 prior predictive check、posterior predictive check 和 held-out predictive evaluation；
8. 说明 marginal likelihood/Bayes factor 对 prior normalization 与 prior scale 的敏感性；
9. 解释 hierarchical model 的 partial pooling；
10. 审计 Bayesian neural network、VAE、Laplace、VI、deep ensemble 和 MC dropout 的真实推断对象。

> [!question] 初学者读完必须能回答
> 1. prior、sampling model、joint、evidence、posterior 与 posterior predictive 各是什么对象？
> 2. 为什么 Bayesian 推断必须先写联合模型，posterior proper 又需要检查什么？
> 3. 参数在 Bayesian 模型中“随机”表示什么，观测后的条件不确定性应怎样解释？
> 4. conjugacy 为什么便于解析更新，它没有解决哪些模型错设问题？
> 5. posterior mean、median 与 MAP 分别在哪些损失下是 Bayes action？
> 6. credible interval 与 frequentist confidence interval 的概率声明为何不同？
> 7. posterior predictive 如何传播参数不确定性，prior check、PPC 与 held-out evaluation 又分别检查什么？

## 阅读前检查

- [[条件概率、全概率与 Bayes 公式]]：条件化、evidence 与 odds；
- [[最大似然估计与 MAP]]：likelihood 不是参数概率，MAP 只是 posterior mode；
- [[统计模型、估计量与偏差方差]]：estimand、risk 与 sampling distribution；
- [[Fisher 信息、Cramér–Rao 界与渐近正态性]]：regular likelihood concentration 与 Bernstein–von Mises 的接口。

## 零、先写联合分布，不从公式口号开始

设参数 $\Theta\in\mathcal T$，观测数据 $Y$。Bayesian model 的起点是

$$
p(\theta,y)
=p(\theta)p(y\mid\theta).
$$

这里：

- $p(\theta)$ 是 prior；
- $p(y\mid\theta)$ 是 sampling model/likelihood；
- $p(\theta,y)$ 是完整 joint model。

观测 $Y=y$ 后：

$$
p(\theta\mid y)
=\frac{p(y\mid\theta)p(\theta)}
{p(y)},
$$

其中

$$
p(y)=\int p(y\mid\theta)p(\theta)d\theta
$$

称 evidence、marginal likelihood 或 prior predictive density at $y$。

先用下图回答一个视觉问题：**联合模型、条件更新、后验预测与模型检查为什么必须保持为四个不同步骤？**

![[00-知识库管理/_assets/figures/probability/fig-bayesian-posterior-predictive-v2.svg|880]]

> [!figure] 图 10.5.18｜Bayesian 联合模型、posterior predictive 与三类检查
> A 从 prior 与 sampling model 组成 joint，再以观测 $Y=y$ 条件化为 posterior；B 从 posterior 抽取参数并生成未来数据，把参数不确定性积分进 posterior predictive；C 区分 prior predictive、posterior predictive 与 held-out evaluation 的提问时点。来源：独立绘制；生成脚本：[[plot_statistical_inference_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 按生成方向读 joint，按观测后的条件方向读 posterior，并单独检查 evidence；B 不把单个 $\widehat\theta$ 的 plug-in prediction 冒充后验预测；C 依次问先验生成范围、给定数据后的模型复现能力和面对新数据的外推表现。

**适用边界（图没有证明什么）。** 图假定 joint model 可定义且 posterior proper，不保证 prior 合理或 likelihood 正确；圆点只示意 posterior predictive draws，不证明 Monte Carlo 已收敛；PPC 使用数据两次且主要检查模型—数据不协调，不能替代 held-out 泛化、因果识别或部署漂移审计。

## 进入正文前：更新参数不确定性，并把它传播到未来观测

> [!info] 课程位置
> MLE/MAP 只保留参数空间中的一个点；本章保留完整 posterior，并进一步对未来数据积分。下一章会对照 frequentist p 值与 coverage，强调两种概率声明的条件对象不同；最后一章再用 MCMC 近似无法直接积分的 posterior。

> [!tip] 建议两遍阅读
> - 第一遍只完成 Beta–Bernoulli 更新，并算出 posterior mean、variance、MAP 和一到两次未来观测的 predictive。
> - 第二遍再学习 Bayes action、credible set、hierarchical partial pooling、prior/posterior predictive check、marginal likelihood 和模型错设。解析共轭只是计算便利，不是模型正确性的证据。

> [!question] 本章的推导问题链
> 1. prior 与 sampling model 怎样组成完整 joint model？
> 2. evidence 为什么是 posterior 归一化和模型比较所需的对象？
> 3. Beta prior 与 Bernoulli likelihood 为什么保持共轭？
> 4. posterior mean、MAP 和 posterior variance分别回答什么？
> 5. posterior predictive 为什么要把参数积分掉，而不是只代入一个点？
> 6. 两个未来观测在给定参数时独立，边缘预测时为什么相关？
> 7. credible probability、frequentist coverage 与 MCMC 数值误差为什么属于不同层？

### 贯穿例：Beta$(2,2)$ prior 经十次观测更新

设 Bayesian joint model 为

$$
Q\sim\operatorname{Beta}(2,2),
$$

$$
Y_i\mid Q=q
\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(q).
$$

这里 $Q$ 是共同成功概率的 Bayesian 随机参数，不是上一轮每个样本内部的 Beta–Bernoulli 潜变量 $\Theta_i$。观测到

$$
n=10,
\qquad K=\sum_{i=1}^{10}Y_i=3.
$$

prior 与 likelihood 相乘：

$$
\begin{aligned}
p(q\mid y)
&\propto q^{2-1}(1-q)^{2-1}
q^3(1-q)^7\\
&=q^4(1-q)^8.
\end{aligned}
$$

因此

$$
Q\mid y\sim\operatorname{Beta}(5,9).
$$

若记录的是计数 $K=3$，evidence 为 Beta-Binomial 概率

$$
P(K=3)
=\binom{10}{3}\frac{B(5,9)}{B(2,2)}
=\frac{16}{143}.
$$

它是观测数据在 prior predictive 下的概率，不是 posterior 中参数的概率。

posterior 的三个常用摘要为

$$
\mathbb E[Q\mid y]=\frac5{14},
$$

$$
\operatorname{Var}(Q\mid y)
=\frac{5\cdot9}{14^2\cdot15}
=\frac3{196},
$$

$$
\operatorname{mode}(Q\mid y)
=\frac{5-1}{5+9-2}
=\frac13.
$$

mean、variance 和 mode 分别描述中心、剩余不确定性与最高密度点。MAP 不是 posterior 的替代品。

#### 一次未来观测

对新观测 $Y_{\mathrm{new}}$，

$$
\begin{aligned}
P(Y_{\mathrm{new}}=1\mid y)
&=\int_0^1P(Y_{\mathrm{new}}=1\mid q)p(q\mid y)dq\\
&=\mathbb E[Q\mid y]
=\frac5{14}.
\end{aligned}
$$

这与 plug-in posterior mean 的一次 Bernoulli 成功概率数值相同，但完整 predictive 的意义来自积分；对多个未来观测，plug-in 与 posterior predictive 不再相同。

#### 两次未来观测

令 $M=Y_{\mathrm{new},1}+Y_{\mathrm{new},2}$。给定 $Q$ 时，

$$
M\mid Q\sim\operatorname{Binomial}(2,Q).
$$

把 $Q$ 按 Beta$(5,9)$ posterior 积掉：

$$
P(M=2\mid y)=\mathbb E[Q^2\mid y]
=\frac{5\cdot6}{14\cdot15}
=\frac17,
$$

$$
P(M=1\mid y)
=2\mathbb E[Q(1-Q)\mid y]
=\frac37,
$$

$$
P(M=0\mid y)
=\mathbb E[(1-Q)^2\mid y]
=\frac37.
$$

若把 $Q$ 固定成 posterior mean $5/14$，则会得到普通 Binomial$(2,5/14)$，其中

$$
P_{\mathrm{plug\text{-}in}}(M=2)
=\left(\frac5{14}\right)^2
=\frac{25}{196}
\ne\frac17.
$$

差异来自参数不确定性。两个未来 Bernoulli 在给定 $Q$ 后独立，但积分掉共同 $Q$ 后，

$$
\operatorname{Cov}(Y_{\mathrm{new},1},Y_{\mathrm{new},2}\mid y)
=\operatorname{Var}(Q\mid y)
=\frac3{196}>0.
$$

单个未来观测的预测方差还可分解为

$$
\underbrace{\mathbb E[Q(1-Q)\mid y]}_{3/14\ \text{aleatoric}}
+
\underbrace{\operatorname{Var}(Q\mid y)}_{3/196\ \text{parameter}}
=\frac{45}{196}.
$$

> [!note] 本轮对象账本
> | 对象 | 本例 | 条件或归一化 |
> |---|---|---|
> | prior | Beta$(2,2)$ | 观测数据前对 $Q$ 的模型 |
> | likelihood | $q^3(1-q)^7$ | 固定数据后关于 $q$ 的相对支持 |
> | evidence | $16/143$ | 计数数据的 prior predictive 概率 |
> | posterior | Beta$(5,9)$ | 给定已观测数据后的参数分布 |
> | posterior predictive | $(3/7,3/7,1/7)$ | 积掉 $Q$ 后两次未来成功数分布 |
> | plug-in predictive | Binomial$(2,5/14)$ | 忽略参数分布宽度的点代入近似 |

> [!analysis] Posterior predictive 的公式七问
> 1. **为什么引入？** 决策面对的是未来观测，不只是未知参数；预测必须传播参数不确定性。
> 2. **对象是什么？** $p(y_{\rm new}\mid q)$ 是 sampling model，$p(q\mid y)$ 是 posterior，积分结果是未来数据空间上的概率分布。
> 3. **条件是什么？** joint model、prior 与 likelihood 必须给出 proper posterior，并声明未来数据与历史数据在给定参数后的条件结构。
> 4. **怎样推出？** 对 joint conditional $p(y_{\rm new},q\mid y)$ 边缘化参数 $q$。
> 5. **不确定性怎样分解？** 全方差把预测波动拆成 posterior 平均的条件噪声与条件均值随 posterior 的变化。
> 6. **边界在哪里？** posterior predictive 仍条件于模型；prior sensitivity、likelihood 错设、近似推断和部署漂移不会因积分自动消失。
> 7. **AI 中对应什么？** Bayesian classifier、ensemble predictive、语言模型后验平均和不确定性分解都调用这层思想；单个 MAP/mean checkpoint 会丢掉参数混合。

> [!success] 第一遍停靠线
> 应能从 Beta$(2,2)$ 与 $K=3,n=10$ 得到 Beta$(5,9)$；算出 posterior mean $5/14$、variance $3/196$、MAP $1/3$；再推出两次未来成功数 PMF $(3/7,3/7,1/7)$，并用 $1/7\ne25/196$ 解释 posterior predictive 与 plug-in prediction 的差别。

> [!warning] Posterior 是条件分布，不是“likelihood 归一化一下”这么简单
> 分母是否有限、prior 是否 proper、support 是否匹配都要检查。若 prior improper，posterior 有时仍可 proper，但 marginal likelihood 与 Bayes factor 通常失去定义。

## 一、Bayesian 概率究竟对什么随机

在生成叙述中：

1. $\Theta\sim p(\theta)$；
2. $Y\mid\Theta=\theta\sim p(y\mid\theta)$。

在实际数据已经出现后，posterior 表达的是：

$$
\text{在 joint model 与数据 }y\text{ 给定时，对未知 }\theta\text{ 的条件不确定性。}
$$

这不是声称物理常数在观察之后继续变化。随机变量语言把不确定量纳入同一概率演算；其解释可能是主观 belief、可交换生成模型或决策建模，但数学对象都是条件概率。

### 参数 posterior 与 latent posterior

必须区分：

- parameter posterior $p(\theta\mid y_{1:n})$：对控制整个数据分布的未知参数；
- local latent posterior $p(z_i\mid x_i,\theta)$：对每个样本的隐藏变量；
- amortized approximation $q_\phi(z\mid x)$：由网络近似 latent posterior；
- predictive distribution $p(\widetilde y\mid y)$：对未来观测。

VAE 中的 $q_\phi(z\mid x)$ 通常不是神经网络全部权重的 Bayesian posterior。

## 二、Odds 形式与序贯更新

对两个参数/模型假设 $\theta_1,\theta_0$：

$$
\frac{p(\theta_1\mid y)}{p(\theta_0\mid y)}
=\frac{p(y\mid\theta_1)}{p(y\mid\theta_0)}
\frac{p(\theta_1)}{p(\theta_0)}.
$$

即

$$
\text{posterior odds}
=\text{likelihood ratio}\times\text{prior odds}.
$$

若数据条件独立：

$$
p(\theta\mid y_{1:n})
\propto p(\theta)\prod_{i=1}^np(y_i\mid\theta).
$$

新数据 $y_{n+1}$ 到来时，

$$
p(\theta\mid y_{1:n+1})
\propto p(y_{n+1}\mid\theta)
p(\theta\mid y_{1:n}).
$$

昨日 posterior 可作今日 prior，前提是 likelihood factorization 与数据选择机制没有改变。重复使用同一数据会把证据计算两次。

## 三、Conjugacy 的意义

若 prior 与 likelihood 结合后，posterior 仍落在同一分布族，称 conjugate prior。

优势：

- 解析更新；
- 充分统计量压缩；
- 便于 sanity check 和在线更新；
- 为复杂推断算法提供可验证基准。

限制：

- conjugacy 是计算便利，不是 prior 合理性的证明；
- 参数化改变会改变“共轭族”的外观；
- 高维深度模型通常不共轭。

## 四、Beta–Binomial：从零推导

设

$$
Y_i\mid p\overset{iid}\sim\operatorname{Bernoulli}(p),
\qquad
p\sim\operatorname{Beta}(a,b).
$$

记 $S=\sum_iY_i$。likelihood kernel：

$$
p(y\mid p)\propto p^S(1-p)^{n-S}.
$$

prior density：

$$
p(p)\propto p^{a-1}(1-p)^{b-1}.
$$

相乘：

$$
p(p\mid y)
\propto
p^{a+S-1}(1-p)^{b+n-S-1}.
$$

所以

$$
\boxed{
p\mid y\sim\operatorname{Beta}(a+S,b+n-S)
}.
$$

### Posterior mean

$$
E[p\mid y]
=\frac{a+S}{a+b+n}.
$$

写成加权平均：

$$
E[p\mid y]
=\frac{a+b}{a+b+n}\frac a{a+b}
+\frac n{a+b+n}\frac Sn.
$$

$a+b$ 像 prior effective sample size，但这个解释只在该模型与所选 parameterization 下有意义。

### Posterior variance

令 $\alpha=a+S,\beta=b+n-S$：

$$
\operatorname{Var}(p\mid y)
=\frac{\alpha\beta}
{(\alpha+\beta)^2(\alpha+\beta+1)}.
$$

样本增加通常使 posterior 集中；但若数据并非 iid Bernoulli，公式中的“$n$ 条信息”会被高估。

## 五、Beta–Binomial posterior predictive

未来一次 $\widetilde Y\mid p\sim\operatorname{Bernoulli}(p)$：

$$
\begin{aligned}
P(\widetilde Y=1\mid y)
&=\int P(\widetilde Y=1\mid p)p(p\mid y)dp\\
&=\int p\,p(p\mid y)dp\\
&=E[p\mid y]\\
&=\frac{a+S}{a+b+n}.
\end{aligned}
$$

未来 $m$ 次成功数 $\widetilde S$ 的分布为 Beta–Binomial：

$$
P(\widetilde S=k\mid y)
=\binom mk
\frac{B(\alpha+k,\beta+m-k)}{B(\alpha,\beta)}.
$$

它通常比 plug-in $\operatorname{Binomial}(m,\widehat p)$ 更分散，因为还积分了 parameter uncertainty。

## 六、Dirichlet–Categorical/Multinomial

对 $K$ 类概率向量 $\pi$：

$$
\pi\sim\operatorname{Dirichlet}(\alpha_1,\ldots,\alpha_K).
$$

数据类别 counts 为 $n_k$，则

$$
\pi\mid y
\sim\operatorname{Dirichlet}(\alpha_1+n_1,\ldots,\alpha_K+n_K).
$$

posterior mean：

$$
E[\pi_k\mid y]
=\frac{\alpha_k+n_k}{\alpha_0+n},
\qquad
\alpha_0=\sum_k\alpha_k.
$$

未来类别 predictive probability 正是该 posterior mean。

> [!warning] “加一平滑”隐含一个具体 prior
> 对每类 count 加一相当于 Dirichlet$(1,\ldots,1)$ posterior predictive，但它在类别数巨大时带来总 prior mass $K$。不能只看“每类 1 很小”而忽略总尺度。

## 七、Normal–Normal：精度加权

设

$$
Y_i\mid\mu\overset{iid}\sim N(\mu,\sigma^2),
\qquad
\mu\sim N(\mu_0,\tau_0^2),
$$

$\sigma^2$ 已知。likelihood 关于 $\mu$：

$$
\exp\left[
-\frac n{2\sigma^2}(\mu-\bar y)^2
\right].
$$

与 prior 相乘并配方，posterior 为

$$
\mu\mid y\sim N(\mu_n,\tau_n^2),
$$

其中

$$
\frac1{\tau_n^2}
=\frac1{\tau_0^2}+\frac n{\sigma^2},
$$

$$
\mu_n
=\tau_n^2
\left(
\frac{\mu_0}{\tau_0^2}
+\frac{n\bar y}{\sigma^2}
\right).
$$

即 posterior precision = prior precision + data precision。

posterior mean 也是 precision-weighted average：

$$
\mu_n
=\frac{\sigma^2}{\sigma^2+n\tau_0^2}\mu_0
+\frac{n\tau_0^2}{\sigma^2+n\tau_0^2}\bar y.
$$

## 八、Normal posterior predictive 与不确定性分解

新观测

$$
\widetilde Y\mid\mu\sim N(\mu,\sigma^2).
$$

积分 $\mu$：

$$
\widetilde Y\mid y
\sim N(\mu_n,\sigma^2+\tau_n^2).
$$

由 total variance：

$$
\begin{aligned}
\operatorname{Var}(\widetilde Y\mid y)
&=E[\operatorname{Var}(\widetilde Y\mid\mu,y)\mid y]\\
&\quad+\operatorname{Var}(E[\widetilde Y\mid\mu,y]\mid y)\\
&=\sigma^2+\tau_n^2.
\end{aligned}
$$

- $\sigma^2$：在模型内即使知道参数仍存在的 observation/aleatoric uncertainty；
- $\tau_n^2$：由 parameter posterior 带来的 epistemic component。

> [!warning] Aleatoric/epistemic 不是模型外真理
> 分解依赖模型层级。漏掉 covariate、随机效应或 distribution shift 时，所谓 aleatoric 可能只是尚未建模的结构；模型错设也不会被 posterior variance 自动承认。

## 九、Posterior summary 是决策问题

给 action $a$ 与 loss $L(\theta,a)$，posterior risk：

$$
\rho(a\mid y)
=E[L(\Theta,a)\mid y].
$$

Bayes action：

$$
a^*(y)\in\arg\min_a\rho(a\mid y).
$$

### Squared loss

$$
L(\theta,a)=(a-\theta)^2
$$

由 bias–variance 型分解，posterior mean 最优：

$$
a^*=E[\Theta\mid y].
$$

### Absolute loss

$$
L(\theta,a)=|a-\theta|
$$

posterior median 最优。

### 0–1 邻域损失

在离散参数或小邻域近似下，posterior mode/MAP 可最优。但连续参数点的概率为零，严格 0–1 loss 需要邻域或离散 action 定义。

因此 mean、median、MAP 并非三个谁更“接近真值”的通用排行榜，而是三个不同 loss 下的 action。

## 十、Credible interval 与 HPD

posterior credible set $C(y)$ 满足

$$
P(\Theta\in C(y)\mid y)=1-\alpha.
$$

### Equal-tail interval

$$
C_{\rm ET}
=\left[
F^{-1}_{\Theta\mid y}(\alpha/2),
F^{-1}_{\Theta\mid y}(1-\alpha/2)
\right].
$$

### Highest posterior density

HPD region 形如

$$
C_{\rm HPD}=\{\theta:p(\theta\mid y)\ge c\},
$$

选择 $c$ 使 posterior mass 为 $1-\alpha$。在单峰分布中常是最短 density-level region；多峰时可由多个不相连区间构成。

### 与 confidence interval 的根本差别

credible：

$$
P(\Theta\in C(y)\mid y)=0.95
$$

是给定数据后的 posterior probability。

confidence procedure：

$$
P_\theta(\theta\in C(Y))\ge0.95
$$

是固定 $\theta$、重复采数据时的 coverage。

二者在某些 conjugate/regular large-sample 情形数值接近，但逻辑对象不同。

## 十一、Posterior predictive 是预测主对象

对未来数据 $\widetilde y$：

$$
\boxed{
p(\widetilde y\mid y)
=\int p(\widetilde y\mid\theta)
p(\theta\mid y)d\theta
}.
$$

plug-in prediction

$$
p(\widetilde y\mid\widehat\theta)
$$

把 parameter uncertainty 压成一个点，通常低估 spread，并可能在非线性模型中连 predictive mean 都不同：

$$
E[g(\Theta)\mid y]\ne g(E[\Theta\mid y]).
$$

Monte Carlo draws $\theta^{(s)}\sim p(\theta\mid y)$ 时：

$$
p(\widetilde y\mid y)
\approx\frac1S\sum_{s=1}^S
p(\widetilde y\mid\theta^{(s)}).
$$

predictive log-density 应稳定计算：

$$
\log\widehat p(\widetilde y\mid y)
=\operatorname{logsumexp}_s
\log p(\widetilde y\mid\theta^{(s)})
-\log S.
$$

## 十二、Prior predictive：拟合前先问模型能生成什么

prior predictive：

$$
p(y)=\int p(y\mid\theta)p(\theta)d\theta.
$$

在看真实数据前，从

$$
\theta^{(s)}\sim p(\theta),
\qquad
y^{(s)}\sim p(y\mid\theta^{(s)})
$$

模拟，可检查：

- 输出尺度是否荒谬；
- 概率是否几乎全在 0/1；
- count/rate 是否超出现实数量级；
- 网络 function prior 是否过于粗糙或饱和；
- hierarchical scale 是否导致极端 group variation。

weakly informative prior 的含义应落到 prior predictive 行为，不是只看 parameter standard deviation 数值“大不大”。

## 十三、Posterior predictive check

从 posterior draw 生成 replicated data：

$$
\theta^{(s)}\sim p(\theta\mid y),
\qquad
y_{\rm rep}^{(s)}\sim p(y\mid\theta^{(s)}).
$$

选择与任务有关的 discrepancy $T(y,\theta)$，比较 observed 与 replicated：

$$
T(y,\theta^{(s)})
\quad\text{vs}\quad
T(y_{\rm rep}^{(s)},\theta^{(s)}).
$$

适合检查：

- tail、zero inflation、overdispersion；
- residual 与 covariate 的结构；
- group extrema；
- calibration/reliability；
- sequence length、rare token、burstiness。

> [!warning] Posterior predictive check 不是“模型通过了”
> 数据既用于形成 posterior，又用于检查 replicated discrepancy，posterior predictive tail area 一般不是 uniform classical p-value。PPC 是定向模型批评工具；没有发现某个 discrepancy 的问题，不代表模型真实或预测可靠。

## 十四、Held-out predictive evaluation

模型检查与模型比较要区分。

- PPC：问模型能否复现关心的数据结构；
- held-out log predictive density：问对未见数据的概率预测如何；
- task utility：问实际 decision loss；
- calibration：问长期概率声明与频率是否匹配。

同一训练数据上 posterior predictive fit 容易乐观。模型选择应使用独立 test、cross-validation 或适当的信息准则；选择后再报告同一分数仍有 selection bias。

## 十五、Hierarchical model 与 partial pooling

设 group $j$：

$$
y_{ij}\mid\theta_j\sim N(\theta_j,\sigma_j^2),
$$

$$
\theta_j\mid\mu,\tau\sim N(\mu,\tau^2).
$$

给定 hyperparameters 时，group posterior mean 是

$$
E[\theta_j\mid y_j,\mu,\tau]
=w_j\bar y_j+(1-w_j)\mu,
$$

其中

$$
w_j
=\frac{n_j/\sigma_j^2}
{n_j/\sigma_j^2+1/\tau^2}.
$$

小样本 group 的 $w_j$ 小，更向总体均值 shrink；大样本 group 保留自身数据。

三种策略：

- no pooling：每组完全独立，small group variance 大；
- complete pooling：所有组参数相同，忽略真实异质性；
- partial pooling：从 group population 学 shrinkage strength。

若 $\mu,\tau$ 也未知，应对其 posterior 积分；把 empirical Bayes point estimate 当 full Bayes 会低估 hyperparameter uncertainty。

## 十六、Marginal likelihood 与 Bayes factor

模型 $M_k$ 的 evidence：

$$
p(y\mid M_k)
=\int p(y\mid\theta_k,M_k)
p(\theta_k\mid M_k)d\theta_k.
$$

Bayes factor：

$$
BF_{10}
=\frac{p(y\mid M_1)}{p(y\mid M_0)}.
$$

posterior model odds：

$$
\frac{P(M_1\mid y)}{P(M_0\mid y)}
=BF_{10}\frac{P(M_1)}{P(M_0)}.
$$

evidence 平均整个 prior parameter space 的 likelihood，因此包含 Occam factor；但也高度敏感于 prior scale。把 alternative prior 扩得很宽会把大量 prior mass 放到数据不支持区域，从而降低 evidence。

### Improper prior 禁区

若

$$
p(\theta)\propto c
$$

且 $c$ 未定，posterior 内的常数有时会归一化消去；但 model evidence 保留该常数，所以 Bayes factor 任意。模型比较需 proper priors 或专门的替代方法。

## 十七、Prior sensitivity 与 robustness

至少做三层：

1. prior predictive：prior 在 data/function 空间意味着什么；
2. posterior sensitivity：合理 prior family/scale 改变时关键 estimand 如何变；
3. decision sensitivity：posterior 的改变是否足以改变 action。

当 likelihood 弱、parameter 不可辨识、样本小或 OOD 外推时，prior 影响尤其大。报告“数据压倒 prior”前要展示，而不是宣称。

### Power prior/tempering

若使用

$$
p(\theta\mid y)\propto p(\theta)p(y\mid\theta)^\beta,
$$

$\beta\ne1$ 定义的是 generalized/tempered posterior。它可用于 robustness、PAC-Bayes 或计算，但不是原 joint model 的普通 Bayes posterior，必须明确 calibration target。

## 十八、Posterior consistency 与 Bernstein–von Mises

在固定维、正确指定、可辨识、真值内点、prior 在真值附近连续且为正、likelihood regular 等条件下，posterior 可集中到 $\theta_0$，并满足近似：

$$
\sqrt n(\Theta-\widehat\theta_{\rm MLE})
\mid Y_{1:n}
\approx N(0,I(\theta_0)^{-1}).
$$

于是 posterior covariance 约为

$$
\frac1nI(\theta_0)^{-1},
$$

credible interval 与 Wald confidence interval 可一阶接近。

但 BvM 不是高维深度模型的免费通行证。以下会失败或需新理论：

- parameter dimension 随 $n$ 增长；
- boundary/singular mixture；
- nonidentifiability；
- misspecification；
- prior 在真值附近为零；
- nonparametric function；
- neural-network symmetry。

## 十九、Bayesian calibration 的三种层次

### Model-based calibration

若

$$
\Theta\sim p(\theta),\quad Y\sim p(y\mid\Theta),
$$

则 posterior credible statements 在 joint prior-predictive repetition 下有 calibration 性质。

### Simulation-based calibration

重复：

1. 从 prior 抽 $\theta^{(r)}$；
2. 从 likelihood 抽 $y^{(r)}$；
3. 运行推断算法得 posterior draws；
4. 检查真 $\theta^{(r)}$ 在 draws 中的 rank。

若模型与实现正确，ranks 应近似 uniform。SBC 主要验证推断实现相对于已指定生成模型，不证明模型适合真实世界。

### Frequentist coverage

固定某个 $\theta_0$ 重复抽数据，检查 Bayesian interval coverage。这是外加的 frequentist 评估，可能依 $\theta_0$ 变化。

三者不能互相替代。

## 二十、近似推断误差必须单列

解析 posterior 常不可得。常见近似：

| 方法 | 近似对象 | 主要误差/诊断 |
|---|---|---|
| Laplace | mode 附近 Gaussian | 多峰、偏斜、boundary、Hessian 奇异 |
| Variational inference | 受限 $q_\phi$ 最小化某种 KL | mode-seeking、underdispersion、optimization gap |
| MCMC | 用相关 draws 近似 posterior expectation | warmup、mixing、MCSE、R-hat、divergence |
| Importance sampling | proposal 加权 | support、weight variance、ESS |
| SMC | sequence of targets/particles | resampling degeneracy、path design |

最终误差至少包括：

$$
\text{model error}
+\text{data uncertainty}
+\text{approximation error}
+\text{Monte Carlo/optimization error}.
$$

## 二十一、Bayesian neural networks 的对象审计

若对网络权重放 prior：

$$
p(\theta\mid D)
\propto p(D\mid\theta)p(\theta).
$$

预测：

$$
p(y_*\mid x_*,D)
=\int p(y_*\mid x_*,\theta)
p(\theta\mid D)d\theta.
$$

但需要审计：

1. weight prior 在 function space 诱导什么分布？
2. permutation/scale symmetry 是否造成多 mode 和奇异 geometry？
3. likelihood 是否描述 label noise 与 sampling mechanism？
4. 推断是 exact MCMC、Laplace、VI 还是 heuristic？
5. OOD 时 function prior 是否合理？
6. posterior predictive calibration 是 in-distribution 还是 deployment distribution？

### Deep ensemble

多个随机初始化训练出的模型平均可改善预测与经验不确定性，但通常不是从一个已声明 posterior 的校准 draws。

### MC dropout

可在特定 variational interpretation 下视为近似，但 dropout forward passes 不自动等于任意网络的 exact Bayesian posterior samples。

### Laplace

inverse curvature 提供 local Gaussian approximation；对非辨识、多 mode 和高度非线性 prediction，应把 parameter draws 传播到 function space 并验证。

## 二十二、VAE 中的 Bayesian 语言边界

生成模型：

$$
p_\theta(x,z)=p(z)p_\theta(x\mid z).
$$

真实 latent posterior：

$$
p_\theta(z\mid x)
=\frac{p(z)p_\theta(x\mid z)}
{p_\theta(x)}.
$$

因为 evidence

$$
p_\theta(x)=\int p(z)p_\theta(x\mid z)dz
$$

难算，引入

$$
q_\phi(z\mid x)
$$

近似 local posterior。ELBO identity：

$$
\log p_\theta(x)
=\mathcal L(\theta,\phi;x)
+D_{\rm KL}(q_\phi(z\mid x)\|p_\theta(z\mid x)).
$$

这不等于给 network parameters $(\theta,\phi)$ 做 full Bayesian inference。它是 latent-variable variational inference 与 parameter point estimation 的组合，除非另外对权重建 prior/posterior。

## 二十三、常见误区

### 误区 1：Posterior 是客观真理

它是 likelihood、prior、数据处理与 model class 共同条件下的结论。

### 误区 2：95% credible interval 自动有 95% frequentist coverage

只在特定 joint calibration 或正则渐近情形可能接近；有限样本 coverage 需验证。

### 误区 3：Posterior 很窄说明模型可靠

错设且数据多时 posterior 可非常窄却集中在错误 pseudo-target。

### 误区 4：Flat prior 等于没有假设

flatness 依赖参数坐标；improper prior 还会破坏 model evidence。

### 误区 5：MAP 是“完整 Bayesian”

MAP 丢掉 posterior width、skewness、multi-modality 与 prediction integration。

### 误区 6：PPC 图相似说明模型真实

只说明所选 discrepancy 未暴露问题；需要多方面检查和 held-out evaluation。

### 误区 7：更多 posterior draws 能修复错误模型

draws 只减计算误差，不能修模型错设、错误 prior 或数据泄漏。

## 二十四、Bayesian 工作流审计模板

1. joint model 与 factorization 是什么？
2. data-selection/missingness mechanism 是否建模？
3. prior 定义在哪个 parameterization，是否 proper？
4. prior predictive 是否合理？
5. parameter/latent/function 哪个对象有 posterior？
6. posterior 是否 proper、identifiable？
7. estimand 与 posterior loss/action 是什么？
8. credible region 是 equal-tail、HPD 还是其他？
9. prediction 是否积分 parameter uncertainty？
10. 推断方法是什么，approximation error 如何检查？
11. MCMC 是否通过多链、R-hat、ESS、MCSE 与 sampler diagnostics？
12. 是否执行 SBC/模拟 recovery？
13. PPC 针对哪些 discrepancy？
14. held-out predictive performance 如何评估？
15. prior/model/shift sensitivity 是否报告？

## 二十五、与后续章节的接口

- [[假设检验、置信区间与多重比较]]：区分 posterior probability 与 repeated-sampling error/coverage；
- [[MCMC 与随机模拟诊断]]：posterior 积分不可解析时，如何产生相关 draws 并量化计算误差；
- [[交叉熵与 KL 散度]]：ELBO、variational approximation 与 predictive log score；
- [[Bayes 决策、Bayes 预测器与 Bayes 风险]]与[[概率校准、Proper Scoring Rule 与可靠性图]]：从 posterior distribution 走到 action、utility 与预测校准。

## 本章自检

- [ ] 能从 joint model 写出 evidence、posterior 与 predictive；
- [ ] 能推导三组 conjugate update；
- [ ] 能从 posterior loss 推出 mean/median/MAP；
- [ ] 能区分 credible 与 confidence；
- [ ] 能推导 predictive variance 的两层分解；
- [ ] 能设计 prior predictive 与 posterior predictive check；
- [ ] 能解释 Bayes factor 的 prior sensitivity；
- [ ] 能说明 hierarchical partial pooling；
- [ ] 能限制 Bernstein–von Mises 的适用范围；
- [ ] 能区分 parameter posterior、latent posterior 与 amortized approximation；
- [ ] 能把 model/data/approximation/Monte Carlo error 分层。

## 练习与解答

- [[习题 - Bayesian 推断与后验预测]]
- [[解答 - Bayesian 推断与后验预测]]

## 参考文献与延伸

- MIT 18.655, Lectures 3, 5, 11, 18：Bayesian model、prediction、Bayes decision 与 asymptotics；
- Gelman et al., *Bayesian Data Analysis*；
- Gelman, Meng & Stern (1996), posterior predictive assessment；
- Stan User’s Guide, Posterior Predictive Sampling / Checks / SBC；
- [[S-2018-Su-5343-VAE从贝叶斯观点出发]]。
