---
type: theorem
status: draft
area: [learning-theory/pac-bayes, measure-change, randomized-predictors]
aliases: [PAC-Bayes-kl Bound, PAC Bayesian Bound, Change-of-Measure Generalization]
node_id: LT-37
prerequisites: ["[[交叉熵与 KL 散度]]", "[[浓缩不等式]]", "[[泛化间隙与浓缩不等式接口]]", "[[Occam 界、编码长度与先验权重]]"]
related: ["[[PAC-Bayes 先验、后验与数据依赖边界]]", "[[互信息与信息论泛化界]]", "[[容量界、稳定性界与 PAC-Bayes 的比较]]", "[[样本压缩方案与泛化]]"]
sources: ["[[S-1999-McAllester-PAC-Bayesian-Theorems]]", "[[S-2002-Seeger-PAC-Bayesian-Generalization]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - PAC-Bayes Bound 的测度变换主线]]"]
solutions: ["[[解答 - PAC-Bayes Bound 的测度变换主线]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-pac-bayes-measure-change-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# PAC-Bayes Bound 的测度变换主线

> [!abstract] 本章主问题
> 设 \(P\) 是看见当前训练样本前固定的 prior，训练后我们选择任意 posterior \(Q\)。PAC-Bayes-kl 定理说明：在 i.i.d. binary 0–1 loss 下，以至少 \(1-\delta\) 的概率，同时对所有 \(Q\)，
> $$
> \operatorname{kl}\!\left(\widehat R_S(Q)\middle\|R(Q)\right)
> \le
> \frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}{m}.
> $$
> 证明不是“Bayes 公式加 concentration”，而是四个精确齿轮：fixed-h 二项指数矩、prior averaging、KL 测度变换、Bernoulli-KL 联合凸性。真正被证书控制的是从 \(Q\) 抽取 hypothesis 的 **Gibbs predictor**。

> [!question] 初学者读完必须能回答
> 1. PAC-Bayes 中的 prior、posterior 为什么不一定是 Bayesian prior/posterior？
> 2. posterior 为什么可以看见训练样本，prior 为什么不可以直接用同一数据拟合？
> 3. Donsker–Varadhan change-of-measure inequality 从哪里来？
> 4. \(\operatorname{KL}(Q\|P)\) 为什么是“换测度的通行费”？
> 5. theorem 控制 Gibbs risk、majority vote、posterior mean 还是 MAP risk？
> 6. binary-kl inverse 为什么通常比平方根 corollary 更值得保留？

## 一、学习目标

1. 把 hypothesis space、prior、posterior、loss 与两种 Gibbs risk 写成完整概率对象；
2. 证明 KL 测度变换引理；
3. 用 binomial types 推出 fixed-h 指数矩上界；
4. 完整拼接 PAC-Bayes-kl theorem；
5. 推出 Pinsker 平方根 corollary，并说明其松弛位置；
6. 解释 simultaneous-over-\(Q\) 量词；
7. 从 point posterior 恢复 weighted Occam intuition；
8. 审计 continuous parameter、deterministic predictor 与 majority vote 的边界；
9. 把 theorem 转成可计算的 inverse-kl certificate。

## 二、对象合同：随机的是哪三层

令

$$
S=(Z_1,\ldots,Z_m)\sim\mathcal D^m
$$

是 i.i.d. 训练样本，hypothesis space 为可测空间 \((\mathcal H,\mathcal A)\)，loss 为

$$
\ell:\mathcal H\times\mathcal Z\to\{0,1\}.
$$

定义单个 hypothesis 的 empirical 与 population risks：

$$
\widehat R_S(h)
=\frac1m\sum_{i=1}^m\ell(h,Z_i),
\qquad
R(h)=\mathbb E_{Z\sim\mathcal D}\ell(h,Z).
$$

在 \(\mathcal H\) 上给定两个 probability measures：

- \(P\)：prior，在当前证书样本 \(S\) 被观察之前固定；
- \(Q=Q_S\)：posterior，可以在观察 \(S\) 后任意选择。

对 \(Q\) 取平均得到 Gibbs risks：

$$
\widehat R_S(Q)
=\mathbb E_{h\sim Q}\widehat R_S(h),
\qquad
R(Q)
=\mathbb E_{h\sim Q}R(h).
$$

因此概率结构有三层：

1. \(S\sim\mathcal D^m\)：theorem 的 high-probability 外层；
2. \(h\sim Q_S\)：Gibbs predictor 的随机化；
3. fresh \(Z\sim\mathcal D\)：population risk 中的测试点。

漏掉任意一层都会把 theorem 读错。

### 2.1 Gibbs Predictor

Gibbs predictor 对每次预测重新采样 \(h\sim Q\)，再输出 \(h(x)\)。其 0–1 risk 正好是

$$
R(Q)=\mathbb E_{h\sim Q}R(h).
$$

它不是以下对象：

- posterior mean parameters；
- MAP hypothesis；
- 对 posterior predictive probabilities 取 argmax；
- 多数投票 classifier。

这些 deterministic predictors 可能与 Gibbs predictor 有关系，但需要额外 inequality。

## 三、Binary Relative Entropy

对 \(q,p\in[0,1]\)，定义 Bernoulli relative entropy

$$
\operatorname{kl}(q\|p)
=q\log\frac qp
+(1-q)\log\frac{1-q}{1-p}.
$$

边界按连续延拓解释，例如

$$
\operatorname{kl}(0\|p)=-\log(1-p).
$$

不要混淆：

$$
\operatorname{kl}(q\|p)
\quad\text{是两个 Bernoulli 参数之间的 scalar divergence，}
$$

$$
\operatorname{KL}(Q\|P)
\quad\text{是 hypothesis-space measures 之间的 divergence。}
$$

两者在 PAC-Bayes theorem 中扮演完全不同的角色。

## 四、图解：三步证明管线

先回答：**为什么图中必须先对 prior 平均指数矩，再把测度换成 posterior？**

![[00-知识库管理/_assets/figures/learning-theory/fig-pac-bayes-measure-change-v2.svg|900]]

> [!figure] 图 20.5.5｜prior 矩控制、KL 测度变换与 binary-kl 风险证书
> 左栏先在样本随机性下控制不依赖样本的 prior 平均指数矩；中栏用 \(\operatorname{KL}(Q\|P)\) 支付从 \(P\) 到 data-dependent \(Q\) 的测度变化；右栏把平均 pointwise binary KL 聚合为 Gibbs risks 并反演。来源：依据 McAllester–Seeger 主线独立绘制；确定性 SVG，由 [[plot_pac_bayes_information_v2.py]] 生成。

**怎样读图。** good event 只需要对 prior integral 建立一次。进入这个 event 后，change-of-measure inequality 对所有 \(Q\) 都是确定性真命题，所以训练后优化 \(Q\) 不再需要重新 union bound。

**图没有证明什么。** 它没有允许 prior 偷看同一 \(S\)，没有把 Gibbs certificate 自动转成单个 neural network 的证书，也没有覆盖无界 loss、dependent data 或任意 data-dependent prior。

## 五、齿轮一：KL 测度变换引理

> [!theorem] Change-of-measure inequality
> 若 \(Q\ll P\)，且相关期望存在，则对任意 measurable \(f:\mathcal H\to\mathbb R\)，
> $$
> \boxed{
> \mathbb E_Q f
> \le
> \operatorname{KL}(Q\|P)
> +\log\mathbb E_P e^f.}
> $$

令 Radon–Nikodym density 为

$$
r(h)=\frac{dQ}{dP}(h).
$$

在 \(Q\)-almost surely 意义下 \(r(h)>0\)。于是

$$
\begin{aligned}
\mathbb E_Q f-\operatorname{KL}(Q\|P)
&=
\mathbb E_Q\left[
f-\log\frac{dQ}{dP}
\right]\\
&=
\mathbb E_Q\log\left(
\frac{e^f}{r}
\right).
\end{aligned}
$$

因为 \(\log\) 是 concave，Jensen inequality 给出

$$
\mathbb E_Q\log\left(
\frac{e^f}{r}
\right)
\le
\log\mathbb E_Q\left[
\frac{e^f}{r}
\right].
$$

利用 \(dQ=r\,dP\)：

$$
\mathbb E_Q\left[
\frac{e^f}{r}
\right]
=
\int_{\{r>0\}}e^f\,dP
\le
\mathbb E_Pe^f.
$$

这里保留最后一个不等号很重要：\(Q\ll P\) 不要求反向的 \(P\ll Q\)；若 \(P\) 还在 \(\{r=0\}\) 上有质量，那部分只会把 \(\mathbb E_Pe^f\) 增大。所以

$$
\mathbb E_Q f
\le
\operatorname{KL}(Q\|P)
+\log\mathbb E_Pe^f.
$$

证明完成。

### 5.1 KL 为什么是换测度的通行费

若 \(Q=P\)，则 KL 为零，无需支付测度变化。若 \(Q\) 把质量集中到 \(P\) 认为罕见的区域，density ratio \(dQ/dP\) 变大，KL 增加。

若 \(Q\not\ll P\)，存在集合 \(A\) 满足

$$
P(A)=0,\qquad Q(A)>0.
$$

此时 \(Q\) 把正质量放到 prior 完全排除的区域，约定

$$
\operatorname{KL}(Q\|P)=+\infty,
$$

证书变为空。

## 六、齿轮二：Fixed-\(h\) 的二项指数矩

固定 \(h\)，记

$$
p=R(h),
\qquad
\widehat p=\widehat R_S(h).
$$

因为 loss 是 Bernoulli，令

$$
K=m\widehat p
=\sum_{i=1}^m\ell(h,Z_i)
\sim\operatorname{Binomial}(m,p).
$$

我们要证明

$$
\boxed{
\mathbb E_S
\exp\left[
m\,\operatorname{kl}(\widehat p\|p)
\right]
\le m+1.}
$$

按 \(K=k\) 求和：

$$
\sum_{k=0}^m
{m\choose k}p^k(1-p)^{m-k}
\exp\left[
m\operatorname{kl}\left(\frac km\middle\|p\right)
\right].
$$

展开 exponential：

$$
\exp\left[
m\operatorname{kl}\left(\frac km\middle\|p\right)
\right]
=
\left(\frac{k/m}{p}\right)^k
\left(\frac{1-k/m}{1-p}\right)^{m-k}.
$$

与 binomial probability 相乘后，\(p\) 消失：

$$
{m\choose k}
\left(\frac km\right)^k
\left(1-\frac km\right)^{m-k}.
$$

这个量正是 parameter \(k/m\) 的 binomial distribution 在 \(k\) 处的 probability，因此不超过 \(1\)。总共有 \(m+1\) 个 types，于是总和不超过 \(m+1\)。

> [!info] \(m+1\) 从哪里来
> 不是 hypothesis 数量，也不是 labels 数量；它来自 empirical error count \(K\in\{0,\ldots,m\}\) 的 \(m+1\) 个可能 binomial types。

## 七、齿轮三：先对 Prior 平均，再用 Markov

定义非负随机变量

$$
M(S)
=
\mathbb E_{h\sim P}
\exp\left[
m\operatorname{kl}(\widehat R_S(h)\|R(h))
\right].
$$

因为 \(P\) 不依赖 \(S\)，Tonelli theorem 允许交换积分：

$$
\begin{aligned}
\mathbb E_S M(S)
&=
\mathbb E_{h\sim P}
\mathbb E_S
\exp\left[
m\operatorname{kl}(\widehat R_S(h)\|R(h))
\right]\\
&\le m+1.
\end{aligned}
$$

Markov inequality 因此给出

$$
\mathbb P_S\left(
M(S)>\frac{m+1}{\delta}
\right)
\le\delta.
$$

也就是说，以至少 \(1-\delta\) 的概率，

$$
\boxed{
\log M(S)
\le
\log\frac{m+1}{\delta}.}
$$

这一步正是 prior independence 的使用点。若 \(P=P_S\) 在看见当前 \(S\) 后被选择，就不能把它无条件移到 \(\mathbb E_S\) 外面。

## 八、齿轮四：在 Good Event 内换成任意 Posterior

固定一个满足上一节 good event 的样本 \(S\)。取

$$
f_S(h)
=m\operatorname{kl}(\widehat R_S(h)\|R(h)).
$$

change-of-measure inequality 给出：对每个 \(Q\ll P\)，

$$
\mathbb E_Q f_S(h)
\le
\operatorname{KL}(Q\|P)
+\log M(S).
$$

因此

$$
\mathbb E_Q
\operatorname{kl}(\widehat R_S(h)\|R(h))
\le
\frac{
\operatorname{KL}(Q\|P)+\log((m+1)/\delta)
}{m}.
$$

现在使用 binary relative entropy 的 joint convexity：

$$
\operatorname{kl}\left(
\mathbb E_Q\widehat R_S(h)
\middle\|
\mathbb E_QR(h)
\right)
\le
\mathbb E_Q
\operatorname{kl}(\widehat R_S(h)\|R(h)).
$$

左侧正是

$$
\operatorname{kl}(\widehat R_S(Q)\|R(Q)).
$$

于是得到主定理。

## 九、PAC-Bayes-kl 主定理

> [!theorem] PAC-Bayes-kl
> 在第二节合同下，任取与 \(S\) 独立的 prior \(P\)。对任意 \(\delta\in(0,1)\)，以至少 \(1-\delta\) 的 \(S\sim\mathcal D^m\) 概率，同时对所有 probability measures \(Q\)：
> $$
> \boxed{
> \operatorname{kl}\!\left(
> \widehat R_S(Q)\middle\|R(Q)
> \right)
> \le
> \frac{
> \operatorname{KL}(Q\|P)+\log((m+1)/\delta)
> }{m}.}
> $$
> 对 \(Q\not\ll P\)，右侧解释为 \(+\infty\)。

### 9.1 量词顺序

完整逻辑是

$$
\forall P\text{ independent of }S,\ \forall\delta\in(0,1):
$$

$$
\mathbb P_S\left[
\forall Q,\ 
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le
\frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}m
\right]\ge1-\delta.
$$

“\(\forall Q\)”在 good event 内部，所以 \(Q\) 可以是 \(S\) 的复杂函数，可以由训练、验证或 bound optimization 得到。

## 十、从 Binary-KL 解出 Risk

定义 upper inverse

$$
\operatorname{kl}^{-1}_+(q,c)
=
\sup\{p\in[q,1]:\operatorname{kl}(q\|p)\le c\}.
$$

令

$$
c(Q)
=
\frac{
\operatorname{KL}(Q\|P)+\log((m+1)/\delta)
}{m},
$$

则

$$
\boxed{
R(Q)
\le
\operatorname{kl}^{-1}_+
\left(\widehat R_S(Q),c(Q)\right).}
$$

一维 binary search 就能稳定计算这个 inverse；没有必要一开始就把它放松成平方根。

### 10.1 零经验风险的精确反演

若 \(\widehat R_S(Q)=0\)，则

$$
\operatorname{kl}(0\|R(Q))
=-\log(1-R(Q))
\le c.
$$

所以

$$
\boxed{
R(Q)\le1-e^{-c}.}
$$

当 \(c\) 很小时，这近似 \(c\)，而平方根 bound 只有 \(O(\sqrt c)\)，可能松得多。

## 十一、Pinsker 平方根 Corollary

Pinsker inequality 在 Bernoulli 情形给出

$$
\operatorname{kl}(q\|p)
\ge2(q-p)^2.
$$

因此

$$
|R(Q)-\widehat R_S(Q)|
\le
\sqrt{\frac{c(Q)}2}.
$$

特别地，

$$
\boxed{
R(Q)
\le
\widehat R_S(Q)
+\sqrt{
\frac{
\operatorname{KL}(Q\|P)+\log((m+1)/\delta)
}{2m}
}.}
$$

它容易阅读，却经过了额外松弛；做数值 certificate 时优先保留 inverse-kl。

## 十二、从 PAC-Bayes 读出 Occam Bound

设 \(\mathcal H\) 可数，\(P(h)>0\)。对 point posterior

$$
Q=\delta_h,
$$

有

$$
\operatorname{KL}(\delta_h\|P)
=\log\frac1{P(h)}.
$$

于是 PAC-Bayes complexity 退化为 weighted description penalty：

$$
\log\frac1{P(h)}.
$$

这解释了 Occam 与 PAC-Bayes 的关系：在离散空间中，point posterior 是 posterior family 的特例。

### 12.1 Continuous Prior 下 Point Mass 的陷阱

若 \(P\) 是 \(\mathbb R^d\) 上有密度的 Gaussian，而 \(Q=\delta_w\)，则

$$
P(\{w\})=0,\qquad Q(\{w\})=1,
$$

所以 \(Q\not\ll P\) 且

$$
\operatorname{KL}(Q\|P)=+\infty.
$$

因此连续参数 neural network 不能把训练权重 point mass 直接塞进这个 theorem；通常要选择有密度的 noisy posterior。

## 十三、Gibbs Risk 与 Majority Vote

对 binary classification，设 posterior vote 为

$$
B_Q(x)
=
\mathbf 1\left\{
\mathbb P_{h\sim Q}(h(x)=1)\ge\frac12
\right\}.
$$

若 majority vote 在 \((x,y)\) 上犯错，至少一半的 posterior hypotheses 也犯错，所以

$$
\mathbf 1\{B_Q(x)\ne y\}
\le
2\mathbb E_{h\sim Q}
\mathbf 1\{h(x)\ne y\}.
$$

取期望：

$$
\boxed{
R(B_Q)\le2R(Q).}
$$

这是一个额外、可能很松的 conversion，不应把两者写成相等。更精细的 vote bounds 需要 margin/disagreement information。

## 十四、PAC-Bayes Optimization

定理同时对所有 \(Q\) 成立，因此可以在训练后解

$$
\min_Q
\operatorname{kl}^{-1}_+\left(
\widehat R_S(Q),
\frac{\operatorname{KL}(Q\|P)+c_\delta}{m}
\right).
$$

也常优化 surrogate：

$$
\min_Q
\widehat R_S(Q)
+\lambda\operatorname{KL}(Q\|P).
$$

但 surrogate minimizer 不一定最小化最终 inverse-kl certificate。可信实现应分别记录：

1. posterior family；
2. prior；
3. stochastic empirical Gibbs risk estimator；
4. KL 的解析式或 certified estimate；
5. confidence budget；
6. binary-kl numerical inversion。

## 十五、一个离散数值例子

设 \(m=1000\)、\(\delta=0.05\)，某 posterior 满足

$$
\widehat R_S(Q)=0.04,
\qquad
\operatorname{KL}(Q\|P)=12.
$$

则

$$
c
=
\frac{12+\log(1001/0.05)}{1000}
\approx0.02190.
$$

Pinsker corollary 给

$$
R(Q)
\le0.04+\sqrt{0.02190/2}
\approx0.1447.
$$

inverse-kl 会给更紧数值，应通过单调 binary search 求解。这个例子也显示：只报告 KL=12 没有意义，必须同时报告 \(m\)、empirical Gibbs risk 与 \(\delta\)。

## 十六、AI 接口：随机化权重分布

令 prior 与 posterior 是 parameter-space distributions：

$$
P=\mathcal N(\mu_P,\Sigma_P),
\qquad
Q=\mathcal N(\mu_Q,\Sigma_Q).
$$

每次从 \(Q\) 采样权重 \(w\)，得到 network \(h_w\)。PAC-Bayes certificate 控制

$$
\mathbb E_{w\sim Q}R(h_w),
$$

不是只控制中心网络 \(h_{\mu_Q}\)。

posterior noise 增大会有两面：

- \(Q\) 可能更接近 broad prior，降低 KL；
- perturbed networks 可能更常犯错，提高 empirical Gibbs risk。

有效 certificate 来自两者的真实平衡，不来自把 variance 人为调到极端。

## 十七、适用边界

本章 theorem 明确假设：

- i.i.d. samples；
- binary 0–1 loss；
- prior independent of current sample；
- measurable hypothesis/loss；
- posterior absolutely continuous relative to prior；
- Gibbs predictor。

以下变化需要其他 theorem：

- unbounded cross-entropy；
- dependent/time-series data；
- distribution shift；
- data-dependent prior；
- deterministic posterior mean；
- posterior chosen after repeated use of a separate test set；
- Monte Carlo estimate 自身带来的数值不确定性。

## 十八、常见误区

> [!warning] 误区 1：posterior 就是 Bayes rule 算出来的
> 错。PAC-Bayes 的 \(Q\) 是任意 certificate distribution。

> [!warning] 误区 2：先验越接近训练解越好，所以训练后设 \(P=Q\)
> 这会让 KL 形式上归零，却破坏 prior-independence 的概率步骤。

> [!warning] 误区 3：有了高概率 theorem，单个网络也自动被控制
> theorem 的直接对象是 Gibbs risk；point mass 在 continuous prior 下通常有 infinite KL。

> [!warning] 误区 4：PAC-Bayes 是 Bayesian posterior consistency
> 它是 frequentist high-probability generalization statement；名字相似不等于推断目标相同。

> [!warning] 误区 5：把右侧压到小于 1 就说明模型性能好
> nonvacuity 只表示 certificate 有信息；风险是否足够低仍依应用阈值决定。

## 十九、证书验收清单

1. 当前 certificate sample 是什么，大小 \(m\) 是多少？
2. loss 是否真在 theorem 的范围内？
3. prior 是否在看见这批 sample 前确定？
4. posterior 是否满足 \(Q\ll P\)？
5. empirical quantity 是否是 Gibbs average？
6. KL 是否以 nats 计算？
7. confidence budget 是否包含所有调参/多次报告？
8. 使用的是 inverse-kl 还是额外松弛？
9. Monte Carlo estimation error 是否另行控制？
10. 最终部署对象是否与 certified randomized predictor 相同？

## 二十、小结

PAC-Bayes 的核心不是一句“经验风险加 KL”：

1. fixed-\(h\) binary loss 提供指数矩；
2. data-independent prior 让矩界可平均；
3. Markov 产生一个与 posterior 无关的 good event；
4. change of measure 用 \(\operatorname{KL}(Q\|P)\) 把 prior 换成任意 posterior；
5. joint convexity 把 pointwise divergence 聚合成 Gibbs risk divergence；
6. inverse binary KL 给出最终 population-risk certificate。

真正的难点不在记公式，而在量词：**prior 在 event 外固定，posterior 在 event 内任意。**

## 来源与延伸

- [[S-1999-McAllester-PAC-Bayesian-Theorems]]：PAC-Bayesian guarantee 的经典起点；
- [[S-2002-Seeger-PAC-Bayesian-Generalization]]：本章 PAC-Bayes-kl 形式与 Gibbs-risk 口径；
- [[PAC-Bayes 先验、后验与数据依赖边界]]：下一章处理合法 prior、Gaussian KL 与 data dependence；
- [[互信息与信息论泛化界]]：另一种 KL 测度比较如何控制 sample–output dependence；
- [[容量界、稳定性界与 PAC-Bayes 的比较]]：不同 certificate 的量词与选型。
