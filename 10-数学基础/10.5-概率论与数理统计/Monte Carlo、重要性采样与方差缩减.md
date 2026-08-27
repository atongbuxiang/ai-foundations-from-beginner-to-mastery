---
type: concept
status: draft
area: [math/probability, math/statistics, ai/probabilistic-computation]
aliases: [Monte Carlo, importance sampling, IS, SNIS, 方差缩减, 有效样本量]
prerequisites: ["[[期望、方差与矩]]", "[[随机变量的收敛与大数定律]]", "[[中心极限定理与 Delta 方法]]", "[[浓缩不等式]]"]
related: ["[[随机变量变换与密度换元]]", "[[Bayesian 推断与后验预测]]", "[[MCMC 与随机模拟诊断]]", "[[概率论与数理统计 MOC]]"]
sources: ["Owen-2013-Monte-Carlo-Theory-Methods-Examples", "Glynn-1994-Efficiency-Improvement-Techniques", "Su-2020-7521-采样看优化", "Su-2021-8062-搜索采样", "Su-2021-8791-VAE密度估计", "Robert-Casella-Monte-Carlo-Statistical-Methods"]
created: 2026-08-19
updated: 2026-08-27
---

# Monte Carlo、重要性采样与方差缩减

> [!abstract] 本章主问题
> Monte Carlo 把难算的积分改写为随机样本平均，iid 且二阶矩有限时具有 $n^{-1/2}$ 标准误；重要性采样通过改变采样分布并用似然比纠偏，成败取决于支持覆盖和权重二阶矩，而不是“样本数看起来很大”。可信报告至少包含估计值、标准误/重复试验、ESS 与权重退化诊断、随机种子和失败条件。

## 学习目标

完成本节后，你应当能够：

1. 把积分、概率与离散求和统一写成期望；
2. 推导简单 Monte Carlo 估计器的无偏性、方差、LLN 与 CLT；
3. 正确估计 standard error，并区分随机误差、偏差和数值误差；
4. 推导普通重要性采样与自归一化重要性采样（SNIS）；
5. 检查绝对连续、支持覆盖、有限二阶矩和权重退化；
6. 理解 ESS 是权重集中度诊断，不是普适误差证书；
7. 推导 control variate、antithetic、stratification 与 Rao–Blackwell 的方差变化；
8. 在 log 域稳定计算权重，并审计 VAE/IWAE、离线策略评估和稀有事件估计。

> [!question] 初学者读完必须能回答
> 1. 积分、概率与离散求和怎样统一写成期望并用样本平均估计？
> 2. 无偏性、方差、LLN、CLT 与 standard error 分别说明估计器的哪一层性质？
> 3. 为什么 Monte Carlo 误差减半通常要约四倍独立样本？
> 4. 重要性采样公式如何由换测度得到，支持不覆盖为什么是不可修复的错误？
> 5. 普通 IS 与 SNIS 的偏差、方差和归一化条件有何不同？
> 6. ESS 为什么只能诊断权重集中，不能单独证明目标函数估计准确？
> 7. control variate、分层、对偶变量和 Rao–Blackwell 分别利用什么结构降低方差？

## 进入正文前：同一个样本平均，先分清是“算积分”还是“估参数”

> [!info] 课程位置
> 上一章给有限样本失败概率，本章把期望本身当作计算目标：分布或未归一化密度可以评价，但积分难以解析，于是由算法主动采样近似。后两章则切换到统计推断：数据由外部世界产生、分布参数未知。两种任务都使用样本平均，却有不同的信息与误差来源。

> [!tip] 建议两遍阅读
> - 第一遍比较直接采样、一个良好 proposal 和一个糟糕 proposal，逐项计算无偏性与方差。
> - 第二遍再学习 SNIS、ESS、log-weight、control variate、antithetic、stratification 和 Rao–Blackwell。不要只看样本量；必须同时检查支持、权重尾部、被积函数与样本相关性。

> [!question] 本章的推导问题链
> 1. 难算积分怎样改写成某个可采样分布下的期望？
> 2. 简单 Monte Carlo 的无偏性、方差与 $n^{-1/2}$ 误差从哪里来？
> 3. 改变采样分布后，likelihood ratio 为什么能恢复目标期望？
> 4. proposal 的支持不覆盖目标时，为什么增加样本数也无法修复？
> 5. 权重方差、被积函数和 ESS 为什么必须联合诊断？
> 6. 利用已知期望、对称性或条件结构怎样降低方差？

### 贯穿例：主动多采成功事件，方差可以降低七倍

本节暂时采用**概率计算合同**：目标分布 $p$ 已知，可以计算概率比，但假设目标期望因状态空间巨大而难以直接求和。为保持手算透明，使用它的二点缩影：

$$
Y\sim p=\operatorname{Bernoulli}(q_\star),
\qquad
q_\star=\frac3{10},
\qquad
\mu=\mathbb E_p[Y]=\frac3{10}.
$$

这里写出 $\mu$ 的解析值只是为了验证算法；真实 Monte Carlo 问题中往往能评价 $p(y)$，却不能直接算完整积分。

#### 直接 Monte Carlo

若 $Y_j\overset{\mathrm{iid}}{\sim}p$，

$$
\widehat\mu_{\mathrm{dir}}
=\frac1n\sum_{j=1}^nY_j
$$

无偏，单个被平均量的方差为

$$
\operatorname{Var}_p(Y)
=q_\star(1-q_\star)
=\frac{21}{100}.
$$

因此

$$
\operatorname{Var}(\widehat\mu_{\mathrm{dir}})
=\frac{21}{100n}.
$$

#### 良好 proposal：主动多采成功

改从

$$
Z_j\sim r=\operatorname{Bernoulli}(3/4)
$$

采样，并使用权重

$$
w(z)=\frac{p(z)}{r(z)}.
$$

两个权重分别是

$$
w(1)=\frac{3/10}{3/4}=\frac25,
\qquad
w(0)=\frac{7/10}{1/4}=\frac{14}{5}.
$$

普通重要性采样估计器为

$$
\widehat\mu_{\mathrm{IS}}
=\frac1n\sum_{j=1}^nw(Z_j)Z_j.
$$

因为 $Z=0$ 时被积函数也为零，虽然 $w(0)$ 很大，该样本对当前积分的贡献仍为零。无偏性直接核对：

$$
\mathbb E_r[w(Z)Z]
=\frac34\cdot\frac25
=\frac3{10}.
$$

单样本方差为

$$
\begin{aligned}
\operatorname{Var}_r(w(Z)Z)
&=\frac34\left(\frac25\right)^2-\left(\frac3{10}\right)^2\\
&=\frac3{100}.
\end{aligned}
$$

与直接采样的 $21/100$ 相比恰好缩小七倍，所以估计器方差变为 $3/(100n)$。

#### 糟糕 proposal：成功区域几乎采不到

若改用 $r_{\mathrm{bad}}=\operatorname{Bernoulli}(1/20)$，成功权重为

$$
w_{\mathrm{bad}}(1)=\frac{3/10}{1/20}=6.
$$

单样本方差变成

$$
\frac1{20}\cdot6^2-\left(\frac3{10}\right)^2
=\frac{171}{100},
$$

比直接采样大得多。若 proposal 令 $r(1)=0$，目标却有 $p(1)>0$，则支持根本不覆盖；成功事件永远不会出现，任何有限或无限样本量都无法纠偏。

#### 为什么 ESS 不能独立判断当前积分

对良好 proposal，

$$
\mathbb E_r[w^2]
=\frac34\left(\frac25\right)^2
+\frac14\left(\frac{14}{5}\right)^2
=\frac{52}{25}.
$$

权重型总体 ESS fraction 近似为 $1/\mathbb E_r[w^2]=25/52$，看起来不到一半；但当前被积函数在大权重的 $Z=0$ 处恰好为零，实际方差反而缩小七倍。这说明 ESS 是 integrand-blind 的权重集中诊断，不是任意目标函数的误差证书。

> [!warning] 本节知道 $q_\star$，下一节不知道 $q$
> 重要性权重使用目标概率 $p(z)$，所以它适合“目标分布可评价、积分难算”的计算问题。若 $q$ 本身就是待估未知参数，就不能偷偷用真 $q$ 构造权重；那是统计推断问题，需要 likelihood、risk 或 posterior。

> [!note] 本轮符号账本
> | 符号 | 类型 | 解释 |
> |---|---|---|
> | $p$ | 目标概率分布 | 定义希望计算的期望 |
> | $r$ | proposal 分布 | 算法实际采样的分布 |
> | $w=p/r$ | likelihood ratio | 把 proposal 下的平均纠偏回目标 |
> | $\mu$ | 固定积分值 | $\mathbb E_p[f(Y)]$ |
> | $\widehat\mu_{\mathrm{dir}}$ | 随机估计量 | 从目标直接采样的平均 |
> | $\widehat\mu_{\mathrm{IS}}$ | 随机估计量 | 加权 proposal 样本平均 |
> | ESS | 诊断量 | 权重集中程度，不是普适误差界 |

> [!analysis] 普通重要性采样公式的公式七问
> 1. **为什么引入？** 目标分布难采样或目标事件稀少时，改用更方便的 proposal 并保持期望不变。
> 2. **对象是什么？** $p$ 定义目标积分，$r$ 定义采样机制，$f$ 是被积函数，$w=p/r$ 是 Radon–Nikodym 比率的密度形式。
> 3. **条件是什么？** 在 $p(x)|f(x)|>0$ 的区域必须有 $r(x)>0$；无偏均值需一阶可积，有限方差还需 $\mathbb E_r[(wf)^2]<\infty$。
> 4. **怎样推出？** 将 $\int f(x)p(x)dx$ 乘除 $r(x)$，得到 $\mathbb E_r[w(X)f(X)]$。
> 5. **方差由什么决定？** 由 $wf$ 的二阶矩决定，不是只由权重、proposal 或样本数中的任何一个单独决定。
> 6. **边界在哪里？** 支持缺失不可修复；尾部不匹配会产生无限或极大方差；SNIS 虽免去正规化常数，却通常引入有限样本偏差。
> 7. **AI 中对应什么？** IWAE、离线策略评估、稀有事件测试和后验预测会使用权重；必须报告 log-weight 稳定性、ESS、最大权重占比和重复运行误差。

> [!success] 第一遍停靠线
> 应能复算直接采样单样本方差 $21/100$、良好 proposal 的 $3/100$ 和糟糕 proposal 的 $171/100$；能写出 $w(1)=2/5,w(0)=14/5$ 并验证无偏性；还能解释为什么 ESS fraction $25/52$ 并没有阻止当前积分获得七倍方差缩减。

## 阅读前检查

- [[期望、方差与矩]]：期望、协方差、样本方差；
- [[随机变量的收敛与大数定律]]：样本均值的一致性；
- [[中心极限定理与 Delta 方法]]：standard error 与渐近区间；
- [[浓缩不等式]]：有限样本上界和渐近误差不是同一对象；
- [[随机变量变换与密度换元]]：从 uniform 随机数构造目标分布。

## 零、Monte Carlo 解决的究竟是什么问题

很多计算可统一成

$$
\mu=\mathbb E_p[f(X)]
=\int_{\mathcal X}f(x)p(x)\,dx.
$$

它可能代表：

- 后验预测平均；
- 生成模型的边缘似然积分；
- 风险 $R(\theta)=\mathbb E[\ell_\theta(X,Y)]$；
- 稀有事件概率 $P(X\in A)=\mathbb E[\mathbf1_A(X)]$；
- 离散空间的巨大求和；
- 某个不可解析的梯度期望。

若可以生成 $X_i\overset{iid}{\sim}p$，定义

$$
\widehat\mu_n=\frac1n\sum_{i=1}^nf(X_i).
$$

核心思想非常朴素：用经验平均替代总体期望。真正困难的是误差、尾部、相关性、计算预算和错误采样分布。

## 一、简单 Monte Carlo 的四层性质

令 $Y_i=f(X_i)$，假设 $X_i$ iid $\sim p$。

### 1. 无偏性

若 $\mathbb E|Y|<\infty$，

$$
\mathbb E[\widehat\mu_n]
=\frac1n\sum_i\mathbb E[Y_i]
=\mu.
$$

无偏只说明跨无限次重复实验的平均，不保证当前一次估计接近真值。

### 2. 方差

若 $\operatorname{Var}(Y)=\sigma_f^2<\infty$，独立性给

$$
\operatorname{Var}(\widehat\mu_n)
=\frac{\sigma_f^2}{n}.
$$

root mean square error 在无偏时为

$$
\operatorname{RMSE}(\widehat\mu_n)
=\frac{\sigma_f}{\sqrt n}.
$$

误差减半通常需要约四倍样本；这就是平方根法则。

### 3. 一致性

若 $\mathbb E|Y|<\infty$，SLLN 给

$$
\widehat\mu_n\xrightarrow{a.s.}\mu.
$$

### 4. 渐近分布

若 $0<\sigma_f^2<\infty$，CLT 给

$$
\sqrt n(\widehat\mu_n-\mu)
\xrightarrow d\mathcal N(0,\sigma_f^2).
$$

因此大样本下

$$
\widehat\mu_n\approx
\mathcal N\left(\mu,\frac{\sigma_f^2}{n}\right).
$$

这不是任意 $n$ 下的等式，也不覆盖无限方差、相关样本或极端稀有事件的坏近似。

## 二、standard error 怎样估

用样本方差

$$
s_n^2=\frac1{n-1}\sum_{i=1}^n(Y_i-\bar Y)^2
$$

估计 $\sigma_f^2$，Monte Carlo standard error（MCSE）为

$$
\widehat{\operatorname{SE}}(\widehat\mu_n)
=\frac{s_n}{\sqrt n}.
$$

近似 $1-\alpha$ 区间为

$$
\widehat\mu_n
\pm z_{1-\alpha/2}\frac{s_n}{\sqrt n}.
$$

### 这个误差条不包含什么

- 模型 $p$ 本身错误；
- $f$ 的离散化/截断/近似偏差；
- 伪随机数生成器或实现 bug；
- 自归一化、clipping、adaptive proposal 引入的偏差；
- 数据集有限导致的统计不确定性，若 Monte Carlo 只是在拟合模型内部采样；
- 多次试验后挑最好结果的选择偏差。

> [!important] 两层随机性要分开
> 例如测试集 bootstrap 或 posterior predictive simulation 中，数据抽样误差和内部 Monte Carlo 误差是不同层。增加内部 sample count 只能缩小后者。

## 三、概率估计与稀有事件为什么会失败

令 $f(X)=\mathbf1_{\{X\in A\}}$，$\mu=P_p(A)=\pi$。简单 MC 为命中比例：

$$
\widehat\pi=\frac1n\sum_i\mathbf1_A(X_i),
\qquad
\operatorname{Var}(\widehat\pi)=\frac{\pi(1-\pi)}n.
$$

相对标准误约为

$$
\frac{\operatorname{SE}(\widehat\pi)}\pi
=\sqrt{\frac{1-\pi}{n\pi}}
\approx\frac1{\sqrt{n\pi}}.
$$

若 $\pi=10^{-6}$，即使 $n=10^6$，期望命中数也只有 1，相对误差约为 100%。零命中不代表事件概率为零，只表示采样分布几乎没访问目标区域。

## 四、重要性采样：换分布，但必须纠偏

目标为

$$
\mu=\int f(x)p(x)\,dx.
$$

若从另一个易采样分布 $q$ 生成样本，并且在 $fp\ne0$ 的区域有 $q>0$，则

$$
\begin{aligned}
\mu
&=\int f(x)\frac{p(x)}{q(x)}q(x)\,dx\\
&=\mathbb E_q[w(X)f(X)],
\end{aligned}
$$

其中

$$
w(x)=\frac{p(x)}{q(x)}
$$

是 importance weight / Radon–Nikodym derivative。

采样 $X_i\overset{iid}{\sim}q$：

$$
\widehat\mu_{\rm IS}
=\frac1n\sum_{i=1}^nw_i f_i.
$$

### 1. 无偏性和方差

若 $\mathbb E_q|wf|<\infty$，则

$$
\mathbb E_q[\widehat\mu_{\rm IS}]=\mu.
$$

若 $\mathbb E_q[w^2f^2]<\infty$，则

$$
\operatorname{Var}_q(\widehat\mu_{\rm IS})
=\frac1n\left[
\int\frac{f(x)^2p(x)^2}{q(x)}dx-\mu^2
\right].
$$

所以 proposal 的质量由 $f^2p^2/q$ 决定，不只是“$q$ 看起来像 $p$”。估计某个尾部函数时，proposal 应覆盖 $|f|p$ 大的区域。

### 2. 支持条件

若存在集合 $A$ 满足

$$
\int_A|f(x)|p(x)dx>0,
\qquad q(A)=0,
$$

则 proposal 永远采不到 $A$，权重比无法补救。得到的估计可能稳定地收敛到错误值。

测度语言是：在积分相关部分，$fp$ 对 $q$ 必须绝对连续。

> [!warning] 重尾方向
> proposal 尾通常不能比目标的相关加权尾轻得太多。否则少数样本的 $p/q$ 会爆炸，二阶矩甚至不存在。

## 五、最优 proposal：理论标杆与循环性

要最小化 IS 二阶矩

$$
\int\frac{f(x)^2p(x)^2}{q(x)}dx
$$

且 $\int q=1$。由 Cauchy–Schwarz 或变分法，形式最优解为

$$
q^*(x)=
\frac{|f(x)|p(x)}{\int|f(u)|p(u)du}.
$$

若 $f\ge0$，则 $q^*=fp/\mu$，且

$$
w^*(x)f(x)=\mu
$$

恒定，理论方差为零。

但 $q^*$ 的归一化常数正是未知积分 $\mu$，通常也难直接采样，所以它是设计方向，不是免费算法。实际 proposal 会用 Laplace 近似、exponential tilting、mixture、flow 或自适应方法逼近该形状。

## 六、自归一化重要性采样（SNIS）

常见情形只知道未归一化目标

$$
\widetilde p(x)=Zp(x),
$$

而 $Z$ 未知。定义 raw weight

$$
r_i=\frac{\widetilde p(X_i)}{q(X_i)},
\qquad
\widetilde w_i=\frac{r_i}{\sum_jr_j}.
$$

SNIS 估计为

$$
\widehat\mu_{\rm SNIS}
=\sum_{i=1}^n\widetilde w_i f(X_i)
=\frac{n^{-1}\sum_i r_if_i}{n^{-1}\sum_i r_i}.
$$

### 1. 为什么归一化常数消失

分子和分母同时含 $Z$：

$$
\frac{\mathbb E_q[rf]}{\mathbb E_q[r]}
=\frac{Z\mathbb E_p[f]}Z=\mu.
$$

### 2. 有限样本通常有偏

随机变量之比的期望通常不等于期望之比：

$$
\mathbb E\left[\frac{A_n}{B_n}\right]
\ne\frac{\mathbb E A_n}{\mathbb E B_n}.
$$

因此 SNIS 一般不是有限样本无偏估计器，但在适当一阶矩与支持条件下由 LLN 一致。

### 3. 渐近方差

把 SNIS 写为二维样本均值的比值并用多元 CLT + Delta，可得

$$
\sqrt n(\widehat\mu_{\rm SNIS}-\mu)
\xrightarrow d
\mathcal N(0,\tau^2),
$$

其中若 $r=\widetilde p/q$，

$$
\tau^2
=\frac{\operatorname{Var}_q(r(X)[f(X)-\mu])}
{(\mathbb E_q r)^2}.
$$

这再次说明只看权重而不看 $f$ 不能完全决定估计误差。

## 七、ESS：有用的警报器，不是万能证书

对非负 raw weights，常用 heuristic ESS 为

$$
\operatorname{ESS}_{w}
=\frac{(\sum_iw_i)^2}{\sum_iw_i^2}
=\frac1{\sum_i\widetilde w_i^2}.
$$

性质：

$$
1\le\operatorname{ESS}_w\le n.
$$

- 权重全相等时 ESS $=n$；
- 一个权重占全部质量时 ESS $\approx1$。

它与归一化权重的 Herfindahl concentration 相同，可视为“权重分散度”。但它不是：

- 任意 $f$ 下精确等价的 iid 样本数；
- bias 或 RMSE 的严格上界；
- proposal 支持覆盖的证明；
- 多模态遗漏的可靠检测器；
- MCMC autocorrelation ESS 的同一概念。

### 应同时报告的诊断

1. `ESS_w / n`；
2. 最大归一化权重 $\max_i\widetilde w_i$；
3. log-weight 的范围、分位数与直方图；
4. 多个独立 seed 的估计分散；
5. 随 $n$ 增加的 running estimate 与 running ESS；
6. proposal 是否覆盖目标各模态/尾部的结构检查；
7. 对关键函数 $f$ 的贡献 $\widetilde w_i f_i$，而不仅是 $w_i$。

## 八、图示：从样本平均到权重退化与方差设计

先用下图回答一个视觉问题：**简单平均的平方根误差、重要性权重退化和 control variate 的残差削减怎样组成同一套误差设计？**

![[00-知识库管理/_assets/figures/probability/fig-monte-carlo-importance-v2.svg|880]]

> [!figure] 图 10.5.14｜Monte Carlo 平均、重要性覆盖与 control variate
> A 从 $f(X_i)$ 的样本平均读出 standard error 的 $n^{-1/2}$ 尺度；B 对比目标 $p$ 与 proposal $q$，指出 $q$ 很小处会产生极端权重；C 把 control variate 画成对 $f$ 中可由已知均值辅助量 $h$ 预测部分的扣除。来源：独立绘制；生成脚本：[[plot_statistical_estimation_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先核对被平均对象 $f(X)$ 的方差，而不是只数样本；B 从两条曲线的覆盖关系读权重，再把 ESS 当作权重集中诊断；C 将回归线外的残差视为新估计器需要承担的随机波动，相关越强，理想系数下可削减的方差越多。

**适用边界（图没有证明什么）。** A 的 $n^{-1/2}$ standard error 需要独立或可有效处理相关性且二阶矩有限；B 的曲线不证明具体 proposal 可用，必须检查绝对连续、尾部与 $wf$ 的矩；C 假定 $\mathbb E[h]$ 已知，若系数和辅助均值也由同一小样本估计，需把额外误差计入。

## 九、log 域实现：高维权重不能直接相除

计算

$$
\ell_i=\log\widetilde p(X_i)-\log q(X_i).
$$

归一化时令 $m=\max_i\ell_i$：

$$
\widetilde w_i
=\frac{e^{\ell_i-m}}{\sum_je^{\ell_j-m}}.
$$

等价于

$$
\log\sum_je^{\ell_j}
=m+\log\sum_je^{\ell_j-m}.
$$

### 稳定并不等于统计健康

log-sum-exp 防止 overflow/underflow，却不能修复 proposal 很差。若最大 log-weight 比第二大高数百，数值上仍可得到一个看似精确的权重 1，但统计上已退化为单样本决定。

### 有正有负的被积函数

普通 IS 的 $w_i\ge0$，但 $w_if_i$ 可有正负。直接对贡献取 log 不合法。可分别累计正负部分，或使用 signed log-sum-exp，并警惕严重 cancellation。

## 十、方差缩减的统一原则

对无偏估计器，MSE 等于方差。方差缩减并不是让随机性“消失”，而是利用已知结构构造同一目标、较低方差的估计器，并把额外计算成本计入效率。

一个实用效率指标是

$$
\text{efficiency}
\propto\frac1{\operatorname{Var}(\widehat\mu)\times\text{cost}}.
$$

单样本方差减半但成本增加十倍，未必值得。

## 十一、Control variates

设希望估 $\mu=\mathbb E[f(X)]$，另有 $h(X)$ 的已知期望 $\eta=\mathbb E[h(X)]$。对常数 $\beta$，定义

$$
Y_\beta=f(X)-\beta(h(X)-\eta).
$$

因为 $\mathbb E[h-\eta]=0$：

$$
\mathbb E[Y_\beta]=\mu.
$$

方差为

$$
\operatorname{Var}(Y_\beta)
=\operatorname{Var}(f)
+\beta^2\operatorname{Var}(h)
-2\beta\operatorname{Cov}(f,h).
$$

对 $\beta$ 求导，最优系数

$$
\beta^*=
\frac{\operatorname{Cov}(f,h)}{\operatorname{Var}(h)}.
$$

最小方差

$$
\operatorname{Var}(Y_{\beta^*})
=\operatorname{Var}(f)(1-\rho_{fh}^2).
$$

相关越强，收益越大。若用同一数据估计 $\beta$，严格有限样本无偏性与 standard error 需要重新分析；可用 pilot sample、cross-fitting 或回归型误差估计。

### AI 接口：REINFORCE baseline

score-function 梯度

$$
\nabla_\theta\mathbb E_{Y\sim p_\theta}[R(Y)]
=\mathbb E[R(Y)\nabla_\theta\log p_\theta(Y)]
$$

可减去与动作适当独立的 baseline $b$，因为

$$
\mathbb E[b\nabla_\theta\log p_\theta(Y)]=0.
$$

baseline 是 control variate 思想；合法条件与最优系数必须按条件期望结构核对。

## 十二、Antithetic sampling 与 common random numbers

若 $U\sim U(0,1)$，则 $1-U$ 同分布。用成对估计

$$
\widehat\mu_{\rm anti}
=\frac1{2m}\sum_{i=1}^m[f(U_i)+f(1-U_i)].
$$

一对平均的方差是

$$
\frac14[2\operatorname{Var}(f(U))
+2\operatorname{Cov}(f(U),f(1-U))].
$$

只有 covariance 为负才减方差；对单调 $f$ 常有效，对振荡/非单调 $f$ 未必。

比较两个系统差异 $\Delta=\mathbb E[f_A(U)-f_B(U)]$ 时，用同一 $U$ 叫 common random numbers：

$$
\operatorname{Var}(f_A-f_B)
=\operatorname{Var}(f_A)+\operatorname{Var}(f_B)
-2\operatorname{Cov}(f_A,f_B).
$$

若输出正相关，差值方差降低。独立运行 A、B 会丢掉这个抵消。

## 十三、Stratification

把空间分成互斥 strata $A_1,\dots,A_K$，$P(A_k)=p_k$，则

$$
\mu=\sum_{k=1}^Kp_k\mu_k,
\qquad
\mu_k=\mathbb E[f(X)\mid X\in A_k].
$$

从第 $k$ 层采 $n_k$ 个，估计

$$
\widehat\mu_{\rm strat}
=\sum_kp_k\widehat\mu_k.
$$

独立层样本下

$$
\operatorname{Var}(\widehat\mu_{\rm strat})
=\sum_k\frac{p_k^2\sigma_k^2}{n_k}.
$$

固定总预算 $\sum_kn_k=n$ 且单位成本相同，连续放松后的 Neyman allocation 是

$$
n_k\propto p_k\sigma_k.
$$

层内越同质，方差越小。若某层被漏采或层权 $p_k$ 错误，偏差不会被“大总样本数”修复。

## 十四、Rao–Blackwell / conditional Monte Carlo

若 $Y$ 是无偏估计量，令

$$
Y^*=\mathbb E[Y\mid Z].
$$

则

$$
\mathbb E[Y^*]=\mathbb E[Y],
$$

且由 total variance：

$$
\operatorname{Var}(Y)
=\mathbb E[\operatorname{Var}(Y\mid Z)]
+\operatorname{Var}(\mathbb E[Y\mid Z])
\ge\operatorname{Var}(Y^*).
$$

直觉是：能解析积分掉的随机性就不要再采样。生成模型中对某些离散 latent state 精确求和、对条件 Gaussian 解析取期望，都是这一原则。

## 十五、重参数与 score-function：两个梯度估计接口

目标

$$
L(\theta)=\mathbb E_{X\sim p_\theta}[f_\theta(X)].
$$

### 1. Score-function

在可交换微分与积分等条件下：

$$
\nabla_\theta L
=\mathbb E_{p_\theta}
[f_\theta(X)\nabla_\theta\log p_\theta(X)
+\nabla_\theta f_\theta(X)].
$$

适用于离散样本，但常高方差。

### 2. Pathwise / reparameterization

若 $X=T_\theta(\varepsilon)$、$\varepsilon\sim r$ 与 $\theta$ 无关：

$$
L(\theta)=\mathbb E_{\varepsilon\sim r}
[f_\theta(T_\theta(\varepsilon))],
$$

可沿确定性计算图求导。它常有更低方差，但需要可微变换、交换条件和可处理的 base noise。

两者都是 Monte Carlo 梯度估计器；“可自动微分”不自动证明无偏、有限方差或数值稳定。

## 十六、三个 AI 场景的完整推导

### 1. VAE 边缘似然与 IWAE

生成模型

$$
p_\theta(x)=\int p_\theta(x,z)dz.
$$

引入 $q_\phi(z\mid x)$：

$$
p_\theta(x)
=\mathbb E_{q_\phi(z\mid x)}
\left[
\frac{p_\theta(x,z)}{q_\phi(z\mid x)}
\right].
$$

用 $K$ 个样本：

$$
\widehat p_K(x)=\frac1K\sum_{k=1}^K
\frac{p_\theta(x,z_k)}{q_\phi(z_k\mid x)}.
$$

$\widehat p_K$ 对 $p_\theta(x)$ 无偏（矩存在时），但

$$
\mathbb E[\log\widehat p_K(x)]
\le\log p_\theta(x)
$$

来自 Jensen；“先平均再取 log”会改变目标。$K$ 增大常收紧 bound，但 encoder gradient signal、权重退化和算力仍需诊断。

### 2. 离线策略评估

行为策略 $q(a\mid s)$ 采数据，目标策略 $\pi(a\mid s)$。单步 contextual bandit 的 IS：

$$
\widehat V_{\rm IS}
=\frac1n\sum_i
\frac{\pi(A_i\mid S_i)}{q(A_i\mid S_i)}R_i.
$$

必须满足 positivity：若 $\pi(a\mid s)>0$，则 $q(a\mid s)>0$。长序列 trajectory ratio 是多步概率比的乘积，方差可随 horizon 爆炸；常需 per-decision IS、doubly robust、clipping 或模型辅助，但每种修改都有新的偏差/条件。

### 3. 稀有失败概率

目标 $\pi=P_p(X\in A)$。从偏向失败区域的 $q$ 采样：

$$
\widehat\pi_{\rm IS}
=\frac1n\sum_i
\mathbf1_A(X_i)\frac{p(X_i)}{q(X_i)}.
$$

proposal 应让 $A$ 更常出现，同时保持权重二阶矩有限。只增加命中率却在 $A$ 内产生巨大权重差异，仍可能比简单 MC 更差。

## 十七、相关样本：不能再除以 $\sqrt n$

若 $Y_i$ 平稳相关，

$$
\operatorname{Var}(\bar Y_n)
=\frac{\sigma^2}{n}
\left[1+2\sum_{k=1}^{n-1}
\left(1-\frac kn\right)\rho_k\right].
$$

若自相关可和，大样本积分自相关时间

$$
\tau_{\rm int}=1+2\sum_{k=1}^\infty\rho_k
$$

给出近似

$$
\operatorname{Var}(\bar Y_n)
\approx\frac{\sigma^2\tau_{\rm int}}n,
\qquad
n_{\rm eff}\approx\frac n{\tau_{\rm int}}.
$$

这属于 MCMC ESS，与权重 ESS 公式来源不同。相关序列可用 batch means、谱方差或多链诊断，详见后续 [[MCMC 与随机模拟诊断]]。

## 十八、QMC/RQMC 的边界

Quasi-Monte Carlo 用低 discrepancy 点覆盖 $[0,1]^d$，不是 iid 随机点。对有界 Hardy–Krause variation 的函数，Koksma–Hlawka 给确定性误差

$$
|\widehat\mu_n-\mu|
\le V_{HK}(f)D_n^*.
$$

但 $V_{HK}(f)$ 常不可计算或无穷，普通 iid sample variance 也不适用于确定性 QMC。Randomized QMC 保留低 discrepancy 结构并注入随机性，可通过独立 randomizations 估计误差。QMC 不是“永远比 MC 快”的替代品；有效维数、光滑性、奇异点和变换方式都关键。

## 十九、实验报告的最低标准

每次 Monte Carlo 结果至少记录：

| 字段 | 内容 |
|---|---|
| target | 明确写出 $\mathbb E_p[f]$ 或积分 |
| estimator | simple MC / IS / SNIS / control variate 等公式 |
| samples | $n$、独立重复数、是否相关 |
| uncertainty | MCSE、独立重复的 dispersion 或有效有限样本界 |
| proposal | $q$、支持关系、是否 adaptive |
| weights | ESS ratio、max weight、log-weight 分位数 |
| numerics | dtype、logsumexp、clipping/truncation |
| reproducibility | seed、PRNG、代码版本、硬件/并行策略 |
| failures | zero hits、mode missing、infinite/NaN、seed sensitivity |

单独给一条平滑的 running curve 不足以证明收敛。

## 二十、常见误区与反例

### 误区 1：无偏意味着可靠

可构造无偏但无限方差的 IS 估计器；绝大多数运行很小，极少数运行巨大，样本均值看似稳定却没有可靠 MCSE。

### 误区 2：proposal 越接近 target 越好

目标是积分 $fp$；最优形状与 $|f|p$ 有关。估计尾概率时 $q=p$ 往往正是低效基线。

### 误区 3：SNIS 权重和为 1，所以结果无偏

权重和为 1 只保证估计是样本 $f_i$ 的凸组合；随机分母使有限样本一般有偏。

### 误区 4：ESS=100 就等价于 100 个 iid target samples

权重 ESS 不包含 $f$ 的结构，也不发现未覆盖模态。它只能作为退化诊断之一。

### 误区 5：logsumexp 后权重问题已经解决

只解决浮点表示。统计方差、support mismatch 和单点支配仍然存在。

### 误区 6：同一个 seed 下两个方法误差更接近，说明更稳定

common random numbers 会让差值更精确，这是设计优点；但单 seed 不能揭示总体 seed sensitivity。应报告 paired differences 与多独立 streams。

### 误区 7：GPU 上生成 $10^8$ 个数就是 $10^8$ 个独立样本

需核对 PRNG streams、并行子序列、重复 seed、采样算法和分布变换；程序数组长度不是独立性的证明。

## 二十一、选择方法的决策树

1. **能直接从 $p$ 独立采样，且 $f$ 方差可控？** 先用 simple MC + MCSE；
2. **目标是稀有区域或 $p$ 难采？** 设计 IS，并先审 support 与二阶矩；
3. **只知道未归一化 target？** 使用 SNIS，同时承认有限样本偏差；
4. **有已知期望的强相关辅助量？** control variate；
5. **可把空间分成层内同质区域？** stratification；
6. **有部分随机性可解析积分？** Rao–Blackwell；
7. **比较两个系统？** common random numbers / paired design；
8. **样本来自 Markov chain？** 使用相关样本 MCSE 与多链诊断；
9. **积分在低有效维且光滑？** 考虑 RQMC，但用独立 randomizations 评估误差。

## 二十二、推导审计模板

1. 目标积分/期望是什么，关于哪个 measure？
2. 样本究竟来自 $p$、$q$，还是相关链？
3. estimator 是普通平均、ratio、clipped 还是 adaptive？
4. 无偏性、一致性、CLT 各需要什么矩与支持条件？
5. standard error 是否匹配相关结构？
6. proposal 是否覆盖 $|f|p$ 的所有区域？
7. 是否存在权重二阶矩、单点支配或 mode missing？
8. 方差缩减是否引入额外成本/偏差？
9. log-domain 稳定与统计稳定是否分别检查？
10. 是否保存 seed、独立重复和失败案例？

## 二十三、最小稳定伪代码

```python
def self_normalized_is(log_target, log_proposal, value):
    logw = log_target - log_proposal
    a = max(logw)
    raw = exp(logw - a)
    weight = raw / sum(raw)
    estimate = sum(weight * value)
    ess_weight = 1.0 / sum(weight * weight)
    max_weight = max(weight)
    return estimate, ess_weight, max_weight
```

生产实现还要处理 all `-inf`、NaN、signed values、batch shape、dtype 和独立重复；不能把这段伪代码当完整诊断器。

## 二十四、与科学空间文章的关系

- [[S-2020-Su-7521-从采样看优化]]：提供 importance reweighting、未知归一化常数与不可导优化的 AI 入口；课程补充 support、矩条件、SNIS 偏差与 ESS；
- [[S-2021-Su-8062-从文本生成到搜索采样]]：把重要性采样、拒绝采样用于受限文本生成；课程严格区分“估积分”与“产生目标分布样本”；
- [[S-2021-Su-8791-VAE估计样本概率密度]]：展示 latent proposal 与 IWAE 形式；课程补上 log-of-average、权重退化和 proposal 质量诊断。

## 本章自检

- [ ] 能推导 simple MC 的无偏、方差、LLN 和 CLT；
- [ ] 能解释为什么 $n^{-1/2}$ 不是任意问题的确定性误差率；
- [ ] 能从换 measure 推导 IS，并写出 support 和二阶矩条件；
- [ ] 能证明 SNIS 一致但一般有限样本有偏；
- [ ] 能解释权重 ESS 与 MCMC ESS 的区别；
- [ ] 能在 log 域算归一化权重并识别统计退化；
- [ ] 能推导 control variate 最优系数、stratified variance 与 Rao–Blackwell；
- [ ] 能为 VAE、离线评估或稀有事件写出目标、proposal、诊断与失败边界；
- [ ] 能提交包含 MCSE、ESS、seed 和重复试验的完整报告。

## 练习与解答

- [[习题 - Monte Carlo、重要性采样与方差缩减]]
- [[解答 - Monte Carlo、重要性采样与方差缩减]]

## 参考文献与延伸

- Art B. Owen, *Monte Carlo theory, methods and examples*，第 2、8、9 章；
- Glynn, *Efficiency Improvement Techniques*：control variates、common random numbers、importance sampling、conditioning 与 stratification；
- Robert & Casella, *Monte Carlo Statistical Methods*；
- 科学空间：2020 年文章 7521、2021 年文章 8062 与 8791。
