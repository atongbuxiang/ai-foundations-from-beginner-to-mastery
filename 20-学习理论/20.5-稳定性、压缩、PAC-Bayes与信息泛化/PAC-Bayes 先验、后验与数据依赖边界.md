---
type: concept
status: draft
area: [learning-theory/pac-bayes, data-dependent-priors, randomized-neural-networks]
aliases: [PAC-Bayes Prior Posterior Contract, Data-Dependent PAC-Bayes Prior]
node_id: LT-38
prerequisites: ["[[PAC-Bayes Bound 的测度变换主线]]", "[[多元高斯分布]]", "[[交叉熵与 KL 散度]]", "[[训练集、验证集、测试集与自适应复用]]"]
related: ["[[互信息与信息论泛化界]]", "[[容量界、稳定性界与 PAC-Bayes 的比较]]", "[[Linear Probe、Fine-Tuning 与迁移评估]]", "[[神经网络容量与 Norm-Based Bound]]"]
sources: ["[[S-2002-Seeger-PAC-Bayesian-Generalization]]", "[[S-2018-Dziugaite-Roy-Data-Dependent-Priors]]", "[[S-1999-McAllester-PAC-Bayesian-Theorems]]"]
exercises: ["[[习题 - PAC-Bayes 先验、后验与数据依赖边界]]"]
solutions: ["[[解答 - PAC-Bayes 先验、后验与数据依赖边界]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-pac-bayes-prior-posterior-contract-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# PAC-Bayes 先验、后验与数据依赖边界

> [!abstract] 本章主问题
> “posterior 可以依赖训练数据”不意味着“prior 也可以训练后随意选择”。标准 PAC-Bayes-kl theorem 的成功事件依赖一个相对证书样本固定的 \(P\)，却同时覆盖全部 \(Q\)。合法增加 prior expressiveness 的主要路线是：独立预训练 prior、sample-split conditional prior、预声明的有限/可数 prior mixture，或引用带附加代价的专门 data-dependent-prior theorem。对 continuous neural-network parameters，还必须让 \(Q\ll P\)，并承认直接证书控制的是 noisy Gibbs network。

> [!question] 初学者读完必须能回答
> 1. prior independence 究竟是“独立于什么”？
> 2. 为什么同一数据可以优化 \(Q\)，却不能无修正地优化 \(P\)？
> 3. sample-split prior 的条件化证明怎样写？
> 4. Gaussian posterior 与 Gaussian prior 的 KL 是什么？
> 5. 为什么 deterministic point mass 在 continuous prior 下通常失败？
> 6. independent pretraining、prior mixture 与 DP prior 分别支付什么代价？

## 一、学习目标

1. 写清标准 PAC-Bayes 的合法 prior/posterior 时间线；
2. 区分 distribution dependence、sample dependence 与 side-information dependence；
3. 推导 multivariate Gaussian KL；
4. 分析 posterior mean、variance 与 empirical Gibbs risk 的三方权衡；
5. 证明 split-sample conditional prior 的合法性；
6. 用 mixture prior/union budget 处理预声明 prior family；
7. 理解 differential-privacy prior 只在专门 theorem 下合法；
8. 审计 pretraining/fine-tuning 数据重叠；
9. 建立 neural PAC-Bayes certificate 的可复现协议。

## 二、标准合同：先 \(P\)，后 \(S\)，再 \(Q_S\)

标准 PAC-Bayes-kl statement 的量词可以写成：

$$
\forall P\text{ independent of }S,\quad
\mathbb P_S\left[
\forall Q,\ \mathcal B(S,P,Q)
\right]\ge1-\delta.
$$

其中 \(\mathcal B\) 是

$$
\operatorname{kl}\left(
\widehat R_S(Q)\middle\|R(Q)
\right)
\le
\frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}m.
$$

时间线是：

1. 声明 data law、hypothesis space、loss、confidence；
2. 在观察 certificate sample 前固定 \(P\)；
3. 采样 \(S\sim\mathcal D^m\)；
4. 用 \(S\) 训练并选择 \(Q_S\)；
5. 在同一个 simultaneous event 内计算 certificate。

### 2.1 “独立”不是“完全没有知识”

\(P\) 可以依赖：

- architecture；
- optimizer family；
- public knowledge；
- data-generating distribution 的已知结构；
- 与 \(S\) 独立的 pretraining dataset；
- 独立随机种子；
- 事先固定的 hyperparameters。

\(P\) 不可无修正地依赖：

- 当前 certificate sample 的 labels；
- 当前 sample 上训练出的 weights；
- 反复查看 certificate result 后调整的 prior scale；
- 与 certificate sample 重叠的数据；
- 当前 sample 上选择出的 architecture，而选择复杂度未计入。

重点不是 prior 是否“聪明”，而是其 randomness 是否与 theorem 外层的 \(S\) 合法分离。

## 三、图解：时间线、合法路线与 Gaussian 权衡

先回答：**为什么图中 sample split 是“换了一批证书数据”，而不是让同一数据免费服务两次？**

![[00-知识库管理/_assets/figures/learning-theory/fig-pac-bayes-prior-posterior-contract-v2.svg|900]]

> [!figure] 图 20.5.6｜PAC-Bayes prior/posterior 的时间合同与四条合法路线
> 左栏标出 standard prior、sample 与 posterior 的先后关系；中栏分开 independent pretraining、sample split、fixed mixture 与专门 DP-prior theorem；右栏显示 Gaussian posterior noise 缩小时 KL 上升、噪声增大时 empirical Gibbs risk 可能恶化。来源：依据 Seeger 与 Dziugaite–Roy 主线独立绘制；确定性 SVG，由 [[plot_pac_bayes_information_v2.py]] 生成。

**怎样读图。** prior 是 reference distribution；posterior 是训练后选择的 certificate distribution。合法性与 tightness 是两件事：固定但极差的 prior 仍合法，只是 bound 可能 vacuous。

**图没有证明什么。** 它没有声称 differential privacy 是唯一 data-dependent prior 方法，也没有给 DP theorem 的具体常数；不同专门 theorem 的 privacy、sample size 与 confidence correction 必须逐一核对。

## 四、为什么 \(Q\) 可以看数据

在 [[PAC-Bayes Bound 的测度变换主线]] 中，我们先建立一个只涉及 \(P\) 的 good event：

$$
\mathcal E_P(S)
=
\left\{
\mathbb E_{h\sim P}
e^{m\operatorname{kl}(\widehat R_S(h)\|R(h))}
\le\frac{m+1}{\delta}
\right\}.
$$

它满足

$$
\mathbb P_S(\mathcal E_P)\ge1-\delta.
$$

一旦 \(S\in\mathcal E_P\)，change-of-measure inequality 是对每个 \(Q\) 都成立的确定性 inequality。因此：

$$
S\in\mathcal E_P
\Longrightarrow
\forall Q,\ \mathcal B(S,P,Q).
$$

这就是训练后优化 \(Q\) 合法的原因。不是因为 \(Q\) “也是随机的”，而是因为 theorem 先建立了 **simultaneous-over-\(Q\)** event。

## 五、为什么 \(P_S\) 不能直接代入

若把 prior 写成 \(P_S\)，proof 中的关键交换变成

$$
\mathbb E_S
\mathbb E_{h\sim P_S}
e^{f(S,h)}.
$$

一般不能改写为

$$
\mathbb E_{h\sim P}
\mathbb E_S e^{f(S,h)}
$$

因为不存在一个与 \(S\) 独立的固定 \(P\)。极端地，可以让 \(P_S\) 把全部质量放在最过拟合当前样本的 hypothesis 上；此时 prior average 已经被数据选择偏差污染。

> [!warning] 形式上的 KL=0 不是证书
> 训练后设 \(P_S=Q_S\) 会得到 \(\operatorname{KL}(Q_S\|P_S)=0\)，但它改变了 theorem 的假设。不能用一个破坏假设的代入得到“完美复杂度”。

## 六、Posterior 不是 Bayesian Posterior

PAC-Bayes 中的 \(Q\) 可以是：

- Bayesian posterior；
- variational approximation；
- training solution 周围的 Gaussian；
- 离散 ensemble weights；
- 由 bound optimization 得到的 distribution；
- 某个 predefined family 中经验风险—KL 权衡的 minimizer。

theorem 不要求

$$
Q(dh)
\propto
P(dh)\prod_i p(Y_i\mid X_i,h).
$$

“posterior”只表示观察数据后选择的 measure。PAC-Bayes 是 frequentist high-probability certificate，不是 posterior credibility statement。

## 七、Gaussian Prior 与 Posterior 的 KL

设

$$
Q=\mathcal N(\mu_Q,\Sigma_Q),
\qquad
P=\mathcal N(\mu_P,\Sigma_P),
$$

其中 \(\Sigma_P,\Sigma_Q\) 正定，维度为 \(d\)。则

$$
\boxed{
\operatorname{KL}(Q\|P)
=\frac12\left[
\operatorname{tr}(\Sigma_P^{-1}\Sigma_Q)
+(\mu_P-\mu_Q)^\top\Sigma_P^{-1}(\mu_P-\mu_Q)
-d
+\log\frac{\det\Sigma_P}{\det\Sigma_Q}
\right].}
$$

### 7.1 推导

Gaussian log density 是

$$
\log q(w)
=-\frac d2\log(2\pi)
-\frac12\log\det\Sigma_Q
-\frac12(w-\mu_Q)^\top\Sigma_Q^{-1}(w-\mu_Q),
$$

对 \(p(w)\) 同理。因此

$$
\operatorname{KL}(Q\|P)
=\mathbb E_Q[\log q(W)-\log p(W)].
$$

在 \(Q\) 下，

$$
\mathbb E_Q
(W-\mu_Q)^\top\Sigma_Q^{-1}(W-\mu_Q)
=d.
$$

另一方面，把

$$
W-\mu_P
=(W-\mu_Q)+(\mu_Q-\mu_P)
$$

代入，并用 \(\mathbb E_Q(W-\mu_Q)=0\)，得到

$$
\begin{aligned}
&\mathbb E_Q
(W-\mu_P)^\top\Sigma_P^{-1}(W-\mu_P)\\
&=
\operatorname{tr}(\Sigma_P^{-1}\Sigma_Q)
+(\mu_Q-\mu_P)^\top
\Sigma_P^{-1}
(\mu_Q-\mu_P).
\end{aligned}
$$

合并 log-determinant 与 quadratic terms 即得公式。

### 7.2 Isotropic 情形

若

$$
P=\mathcal N(\mu_P,\sigma_P^2I),
\qquad
Q=\mathcal N(\mu_Q,\sigma_Q^2I),
$$

则

$$
\boxed{
\operatorname{KL}(Q\|P)
=\frac12\left[
d\frac{\sigma_Q^2}{\sigma_P^2}
+\frac{\|\mu_Q-\mu_P\|_2^2}{\sigma_P^2}
-d
+d\log\frac{\sigma_P^2}{\sigma_Q^2}
\right].}
$$

当 \(\sigma_Q\downarrow0\)，最后一项趋于 \(+\infty\)。这就是 posterior 逼近 point mass 时 KL 爆炸的解析表现。

## 八、Neural Posterior 的三方权衡

一个可计算的 neural PAC-Bayes certificate 同时受三项影响：

1. 中心距离：
   $$
   \|\mu_Q-\mu_P\|_{\Sigma_P^{-1}}^2;
   $$
2. covariance mismatch：
   $$
   \operatorname{tr}(\Sigma_P^{-1}\Sigma_Q)
   -\log\det\Sigma_Q;
   $$
3. perturbed empirical risk：
   $$
   \widehat R_S(Q)
   =\mathbb E_{W\sim Q}\widehat R_S(h_W).
   $$

posterior 太窄：

- empirical Gibbs risk 可能接近 center network；
- KL 通过 \(-\log\det\Sigma_Q\) 爆炸。

posterior 太宽：

- KL 的 concentration penalty 可能下降到某个范围；
- sampled networks 的 predictions 失真，empirical Gibbs risk 增大。

所以 “flatness” 不是只看 Hessian 的局部美学；它必须落实为一个 parameterization-aware distributional perturbation experiment。

## 九、路线一：独立 Pretraining Prior

设预训练数据

$$
S_{\mathrm{pre}}\sim\mathcal D_{\mathrm{pre}}^{n}
$$

与 fine-tuning/certificate sample

$$
S_{\mathrm{ft}}\sim\mathcal D_{\mathrm{ft}}^{m}
$$

独立。可以用 \(S_{\mathrm{pre}}\) 训练 prior center：

$$
\mu_P=A_{\mathrm{pre}}(S_{\mathrm{pre}}).
$$

条件于 \(S_{\mathrm{pre}}\)，\(P\) 对 \(S_{\mathrm{ft}}\) 是固定的，所以标准 PAC-Bayes theorem 可应用于 \(S_{\mathrm{ft}}\)。

### 9.1 数据重叠风险

若 pretraining corpus 与 \(S_{\mathrm{ft}}\) 有 duplicate/near-duplicate examples，或者 certificate labels 可从 pretraining data 恢复，independence 不再自动成立。

审计应记录：

- dataset lineage；
- de-duplication rule；
- sample-level overlap；
- label leakage；
- checkpoint 是否在看见 certificate metrics 后选择。

“来自不同文件夹”不是统计独立性证明。

## 十、路线二：Sample-Split Conditional Prior

把 i.i.d. sample 随机分成独立两部分：

$$
S=(S_0,S_1),
\qquad
|S_0|=m_0,\quad|S_1|=m_1.
$$

用 \(S_0\) 构造

$$
P_{S_0}.
$$

然后只在 \(S_1\) 上定义 empirical Gibbs risk：

$$
\widehat R_{S_1}(Q)
=\frac1{m_1}\sum_{z\in S_1}
\mathbb E_{h\sim Q}\ell(h,z).
$$

### 10.1 条件化证明

固定任意 \(S_0=s_0\)。由于 \(S_1\) 与 \(S_0\) 独立，条件于 \(S_0=s_0\) 时，\(P_{s_0}\) 对 \(S_1\) 是固定 prior。因此

$$
\mathbb P_{S_1\mid S_0=s_0}
\left[
\forall Q,\ 
\operatorname{kl}(\widehat R_{S_1}(Q)\|R(Q))
\le
\frac{
\operatorname{KL}(Q\|P_{s_0})
+\log((m_1+1)/\delta)
}{m_1}
\right]
\ge1-\delta.
$$

这个 lower bound 对每个 \(s_0\) 都成立。再对 \(S_0\) 积分，得到 joint probability 至少 \(1-\delta\)。

### 10.2 代价

prior 变得 data-informed，但 certificate 样本量从 \(m\) 降到 \(m_1\)。\(S_0\) 上的 low training error 不能塞进 \(\widehat R_{S_1}(Q)\) 以扩大 denominator。

## 十一、路线三：预声明 Prior Family

设训练前固定 countable family

$$
\{P_j:j\in\mathbb N\}
$$

及 weights \(\pi_j>0\)，满足

$$
\sum_j\pi_j=1.
$$

### 11.1 Union-Budget View

给第 \(j\) 个 prior 分配

$$
\delta_j=\delta\pi_j.
$$

对全部 \(j\) 做 union bound，得到同时成立的 bound：

$$
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le
\frac{
\operatorname{KL}(Q\|P_j)
+\log((m+1)/\delta)
+\log(1/\pi_j)
}{m}.
$$

训练后可以选择 \(j\)，但要支付 code length

$$
\log\frac1{\pi_j}.
$$

### 11.2 Mixture-Prior View

也可以固定

$$
P_{\mathrm{mix}}=\sum_j\pi_jP_j.
$$

在适当支撑条件下，

$$
P_{\mathrm{mix}}\ge\pi_jP_j
$$

意味着

$$
\operatorname{KL}(Q\|P_{\mathrm{mix}})
\le
\operatorname{KL}(Q\|P_j)
+\log\frac1{\pi_j}.
$$

两种视角都表达同一原则：训练后挑 prior family member 不是免费操作，必须把选择编码进去。

## 十二、路线四：专门的 Data-Dependent-Prior Theorem

[[S-2018-Dziugaite-Roy-Data-Dependent-Priors]] 说明：若 prior-generation mechanism 对 sample 是 differential private，可在专门 PAC-Bayes theorem 中允许某种 data dependence，并出现 privacy/confidence correction。

这里必须保持三个边界：

1. 不能把 standard theorem 的右侧原封不动保留；
2. 必须验证 prior mechanism 的 privacy definition 与参数；
3. 必须使用该 theorem 对应的 loss、sample 与 probability convention。

因此本库只把它写成结构：

$$
\text{empirical term}
+\frac{\operatorname{KL}(Q\|P_S)+\text{confidence}}m
+\text{privacy correction},
$$

不把某篇论文的常数脱离条件复制到所有场景。

## 十三、Prior Hyperparameters 的选择

设 prior 是

$$
P_\tau=\mathcal N(0,\tau^2I).
$$

如果 \(\tau\) 在看见同一 \(S\) 的 certificate 后连续调到最优，标准 fixed-\(P\) theorem 不支持这个过程。

合法方案包括：

- 训练前固定 \(\tau\)；
- 在 independent data 上选 \(\tau\)；
- 预声明 grid \(\{\tau_j\}\) 与 weights \(\pi_j\)，支付 \(\log(1/\pi_j)\)；
- 把 \(\tau\) 放进 hierarchical prior，并对 joint object 计算 KL；
- 使用合适的 data-dependent-prior theorem。

相反，posterior variance \(\sigma_Q\) 可以在 \(S\) 上优化，因为 \(Q\) 已在 simultaneous quantifier 内。

## 十四、Support 与 Parameterization

### 14.1 Support

若 \(P\) 的某个 coordinate variance 是零，而 \(Q\) 在该 coordinate 有不同 mean 或正 variance，则 \(Q\not\ll P\)，KL infinite。

实践上应检查：

- covariance 是否 positive definite；
- pruned coordinates 的 prior/posterior support 是否一致；
- discrete architecture switches 是否有 prior mass；
- quantized weights 是否与 continuous prior 使用了错误 measure。

### 14.2 Parameterization

functionally equivalent neural networks 可能因：

- hidden-unit permutation；
- positive homogeneity/rescaling；
- normalization symmetry；
- redundant parameterization

而有不同 parameter-space KL。一个 tight parameter-space certificate 不自动具有 representation invariance。

可能的修复方向包括：

- symmetry-aware prior；
- quotient/canonical parameterization；
- function-space distribution；
- 把 parameterization choice 作为 theorem contract 明示。

## 十五、Monte Carlo Empirical Gibbs Risk

对大型 neural posterior，通常用

$$
W_1,\ldots,W_K\overset{\mathrm{iid}}{\sim}Q
$$

估计

$$
\widehat R_S(Q)
=
\mathbb E_Q\widehat R_S(h_W).
$$

naive estimate 是

$$
\widetilde R_{S,K}
=\frac1K\sum_{k=1}^K\widehat R_S(h_{W_k}).
$$

但 theorem 需要真实的 \(Q\)-expectation，而不是未校正 Monte Carlo point estimate。若 loss bounded，可以再用 concentration 构造 upper confidence bound：

$$
\widehat R_S(Q)
\le
\widetilde R_{S,K}
+\sqrt{\frac{\log(1/\eta)}{2K}}
$$

（这里给出的是独立 \(W_k\)、\([0,1]\)-valued summary 下的一个简单 Hoeffding 口径）。总失败概率要分配为：

$$
\delta_{\mathrm{total}}
=\delta_{\mathrm{PAC}}
+\eta_{\mathrm{MC}}
+\cdots.
$$

## 十六、部署对象与证书对象一致

若证书控制 Gibbs predictor，却部署 posterior mean network，必须额外证明：

$$
R(h_{\mu_Q})
\le
\Phi(R(Q),\text{other quantities}).
$$

一般不存在这样的无条件 inequality。可选策略：

- 真正部署 stochastic ensemble/Gibbs sampling；
- 使用 majority-vote conversion；
- 直接为 deterministic object 寻找其他 bound；
- 证明 distributional perturbation 下 prediction 不变；
- 明确把 PAC-Bayes certificate 解释成局部 ensemble robustness，而非 center risk guarantee。

## 十七、一个完整审计案例

假设流程：

1. 在 public corpus 上预训练 checkpoint \(w_0\)；
2. 在 private fine-tuning sample \(S\) 上得到 \(w_S\)；
3. 设
   $$
   P=\mathcal N(w_0,\sigma_P^2I),
   \qquad
   Q=\mathcal N(w_S,\sigma_Q^2I);
   $$
4. 用同一 \(S\) 优化 \(\sigma_Q\) 和 \(Q\)；
5. 计算 empirical Gibbs risk 与 Gaussian KL。

要合法，至少验证：

- public corpus 与 \(S\) 无重叠/leakage；
- \(w_0,\sigma_P\) 没有根据 \(S\) 调整；
- architecture 与 parameterization 预先固定，或选择成本被支付；
- \(Q\ll P\)；
- empirical risk 对 sampled weights 取平均；
- Monte Carlo uncertainty 被计入；
- 部署对象与证书对象一致。

若 \(\sigma_P\) 也是看了 \(S\) 后挑的，需要 grid/mixture/split/special theorem 之一。

## 十八、常见误区

> [!warning] 误区 1：prior 不能依赖任何数据
> 它可以依赖与 certificate sample 独立的数据；真正条件是相对当前 high-probability sampling event 的合法独立性。

> [!warning] 误区 2：sample split 后，\(S_0\) 和 \(S_1\) 的 loss 都能放进 denominator \(m\)
> standard conditional proof 只把 \(S_1\) 当 certificate sample，denominator 是 \(m_1\)。

> [!warning] 误区 3：训练后从十万个 prior 中挑最小 KL 不需付费
> 若 prior family selection 不在 simultaneous event 内，就需要 mixture weights 或 union budget。

> [!warning] 误区 4：Gaussian KL 小就说明函数接近
> KL 在 parameter distribution 上计算；symmetry 与 parameterization 会改变它。

> [!warning] 误区 5：DP prior 可以直接代入任何 PAC-Bayes 公式
> 只能使用对应专门 theorem，并保留 privacy correction。

## 十九、Prior/Posterior 验收表

| 检查项 | 必须记录 |
|---|---|
| certificate sample | 样本单位、来源、大小、i.i.d. 假设 |
| prior construction | 数据、随机种子、checkpoint、hyperparameters |
| independence | overlap/de-duplication/leakage 证据 |
| posterior family | mean、covariance、support、训练方式 |
| KL | 方向 \(Q\|P\)、单位 nats、数值稳定性 |
| empirical Gibbs risk | sampling protocol 与 Monte Carlo CI |
| confidence | PAC、MC、multi-prior 等预算 |
| predictor | Gibbs、vote、mean 或 MAP |
| tuning history | 哪些量看过 certificate data |
| reproducibility | code、seed、data lineage 与 hash |

## 二十、小结

PAC-Bayes prior/posterior 的核心不是命名，而是概率时序：

- prior 是在 certificate sample 前固定的 reference；
- posterior 是 sample 后选择、由 simultaneous theorem 覆盖的 distribution；
- Gaussian KL 精确衡量 center、scale 与 covariance 的改变；
- continuous point posterior 通常导致 infinite KL；
- independent pretraining、sample split、fixed mixture 与 specialized DP theorem 是不同合法路线；
- 所有 data reuse、prior selection、Monte Carlo estimation 与 deployment conversion 都必须单独记账。

“先验更接近答案”可以让 bound 更紧，但只有在它没有偷看证书答案，或已经为这种依赖支付合法代价时才有意义。

## 来源与延伸

- [[S-2002-Seeger-PAC-Bayesian-Generalization]]：标准 prior/posterior 量词与 PAC-Bayes-kl；
- [[S-2018-Dziugaite-Roy-Data-Dependent-Priors]]：DP data-dependent prior 的专门路线；
- [[PAC-Bayes Bound 的测度变换主线]]：本章合法性规则所依赖的 proof step；
- [[互信息与信息论泛化界]]：把 algorithm dependence 改写成 sample–output information；
- [[容量界、稳定性界与 PAC-Bayes 的比较]]：证书选择的统一审计。
