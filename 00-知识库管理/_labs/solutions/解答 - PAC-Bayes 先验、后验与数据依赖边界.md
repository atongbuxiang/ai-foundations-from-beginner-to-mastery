---
type: solution
status: draft
area: [learning-theory/pac-bayes, data-dependent-priors]
topic: "[[PAC-Bayes 先验、后验与数据依赖边界]]"
exercise: "[[习题 - PAC-Bayes 先验、后验与数据依赖边界]]"
prerequisites: ["[[PAC-Bayes 先验、后验与数据依赖边界]]"]
related: ["[[PAC-Bayes Bound 的测度变换主线]]", "[[训练集、验证集、测试集与自适应复用]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - PAC-Bayes 先验、后验与数据依赖边界

> [!warning] 核心判据
> prior independence 必须相对真正承担 high-probability certificate 的样本解释；文件路径、时间戳或“预训练”名称不能替代数据 lineage 证据。

## A. 识别与复述

### LT-PBPP-A01

\(P\) 可以依赖：

1. architecture；
2. public/domain knowledge；
3. 与 certificate sample 独立的 pretraining data；
4. 训练前固定 hyperparameters；
5. 独立 randomness。

不能无修正依赖：

1. certificate sample labels；
2. 该 sample 上训练出的 weights；
3. 看过 bound 后选出的 scale；
4. 与 certificate sample 重叠的 data；
5. 在该 sample 上选出的 architecture/prior family member。

“独立”相对 bound 外层随机抽取的 certificate sample。若 split 后只在 \(S_1\) 证书，prior 可依赖独立 \(S_0\)。

### LT-PBPP-A02

good event 的形式是

$$
\mathbb P_S[\forall Q,\mathcal B(S,P,Q)]\ge1-\delta.
$$

因此 posterior mean、variance 等都可用 \(S\) 优化。\(P\) 位于 event 外，若也用 \(S\) 选择，原 prior-averaged exponential moment 不成立。prior hyperparameter selection 应通过 independent data、predeclared grid + union/mixture cost、hierarchical prior 或 specialized theorem 处理。

### LT-PBPP-A03

- independent pretraining：条件于独立 pretraining data，\(P\) 对 certificate sample 固定；代价是数据独立/重叠审计；
- sample split：\(S_0\) 训练 prior、\(S_1\) 证书；代价是 denominator 只剩 \(m_1\)；
- fixed mixture：训练前固定 \((P_j,\pi_j)\)，训练后选 \(j\) 支付 \(\log(1/\pi_j)\)；
- DP prior：允许受控 sample dependence，但必须用专门 theorem 支付 privacy/confidence correction。

## B. 手算与数值判断

### LT-PBPP-B01

\(d=2,\Sigma_P=4I,\Sigma_Q=I,\mu_Q=(1,-1)\)。一般公式给

$$
\operatorname{tr}(\Sigma_P^{-1}\Sigma_Q)
=\operatorname{tr}\left(\frac14I_2\right)
=\frac12,
$$

$$
\mu_Q^\top\Sigma_P^{-1}\mu_Q
=\frac14(1^2+(-1)^2)
=\frac12,
$$

$$
\log\frac{\det\Sigma_P}{\det\Sigma_Q}
=\log\frac{16}{1}
=\log16.
$$

故

$$
\operatorname{KL}(Q\|P)
=\frac12\left[\frac12+\frac12-2+\log16\right]
=\frac12(\log16-1)
\approx\boxed{0.88629}.
$$

### LT-PBPP-B02

$$
\operatorname{KL}(Q_\sigma\|P)
=\frac12\left[
d\sigma^2+\|\mu\|^2-d-d\log\sigma^2
\right].
$$

令 \(v=\sigma^2\)，则

$$
\frac{d}{dv}\operatorname{KL}
=\frac d2\left(1-\frac1v\right).
$$

唯一 stationary point 为 \(v=1\)，二阶导

$$
\frac d{2v^2}>0,
$$

所以

$$
\boxed{\sigma^2=1}.
$$

固定 mean 时，covariance 与 prior covariance 匹配最小化 covariance KL；mean cost \(\|\mu\|^2/2\) 仍保留。

### LT-PBPP-B03

第三个 prior 的代价：

$$
\log\frac1{\pi_3}
=\log6
\approx\boxed{1.79176\text{ nats}}.
$$

除以 \(m=1000\)：

$$
\boxed{0.00179176}.
$$

它进入 PAC-Bayes numerator，而不是直接加到 risk 上；最终还需 binary-kl inverse。

## C. 推导与证明

### LT-PBPP-C01

Gaussian log density 差为

$$
\log q(w)-\log p(w)
=\frac12\log\frac{\det\Sigma_P}{\det\Sigma_Q}
-\frac12(w-\mu_Q)^\top\Sigma_Q^{-1}(w-\mu_Q)
+\frac12(w-\mu_P)^\top\Sigma_P^{-1}(w-\mu_P).
$$

在 \(Q\) 下第一 quadratic expectation 是 \(d\)。写

$$
W-\mu_P=(W-\mu_Q)+(\mu_Q-\mu_P).
$$

cross term expectation 为零，并有

$$
\mathbb E_Q
(W-\mu_Q)^\top\Sigma_P^{-1}(W-\mu_Q)
=\operatorname{tr}(\Sigma_P^{-1}\Sigma_Q).
$$

所以第二 quadratic expectation 为

$$
\operatorname{tr}(\Sigma_P^{-1}\Sigma_Q)
+(\mu_Q-\mu_P)^\top\Sigma_P^{-1}(\mu_Q-\mu_P).
$$

合并得

$$
\frac12\left[
\operatorname{tr}(\Sigma_P^{-1}\Sigma_Q)
+(\mu_Q-\mu_P)^\top\Sigma_P^{-1}(\mu_Q-\mu_P)
-d+\log\frac{\det\Sigma_P}{\det\Sigma_Q}
\right].
$$

### LT-PBPP-C02

对每个固定 \(s_0\)，\(P_{s_0}\) 是关于随机 \(S_1\) 的 fixed prior。标准 theorem 给

$$
\mathbb P_{S_1\mid S_0=s_0}(E_{s_0})\ge1-\delta,
$$

其中 \(E_{s_0}\) 是同时对所有 \(Q\) 的 \(S_1\)-risk certificate。

利用 tower property：

$$
\begin{aligned}
\mathbb P_{S_0,S_1}(E)
&=
\mathbb E_{S_0}
\mathbb P(E\mid S_0)\\
&\ge
\mathbb E_{S_0}(1-\delta)
=1-\delta.
\end{aligned}
$$

关键是 \(S_1\perp S_0\)，且 empirical risk/denominator 只使用 \(S_1\)。

### LT-PBPP-C03

因为

$$
P_{\rm mix}
=\sum_k\pi_kP_k
\ge\pi_jP_j
$$

作为 measures/densities，若 \(Q\ll P_j\)，则 \(Q\)-a.s.

$$
\frac{dQ}{dP_{\rm mix}}
\le
\frac1{\pi_j}\frac{dQ}{dP_j}.
$$

取 log 并在 \(Q\) 下积分：

$$
\begin{aligned}
\operatorname{KL}(Q\|P_{\rm mix})
&=
\mathbb E_Q\log\frac{dQ}{dP_{\rm mix}}\\
&\le
\mathbb E_Q\log\frac{dQ}{dP_j}
+\log\frac1{\pi_j}\\
&=
\operatorname{KL}(Q\|P_j)
+\log\frac1{\pi_j}.
\end{aligned}
$$

## D. 边界、反例与纠错

### LT-PBPP-D01

可能 leakage：

1. exact duplicates；
2. near-duplicate passages/images；
3. 同一 user/document 被切到两边；
4. label/answer 可从预训练文本恢复；
5. certificate examples 曾用于 checkpoint selection；
6. tokenizer/vocabulary 用 certificate corpus 拟合；
7. synthetic data 由 certificate records 生成；
8. human feedback 观察过 certificate errors。

因此需要 sample-level lineage 与 de-duplication，而非文件名判断。

### LT-PBPP-D02

条件于 \(S_0\)，\(P_{S_0}\) 对 \(S_1\) 固定；proof 只为

$$
\widehat R_{S_1}(Q)
$$

建立 exponential moment。把 \(S_0\) loss 加回 empirical average 时，hypothesis distribution/prior 已依赖这些 observations，fixed-\(h\)/fixed-prior concentration 不能覆盖它们。denominator 必须是 \(m_1\)，除非使用另一个明确允许 reuse 的 theorem。

### LT-PBPP-D03

离散例子：

$$
P(h_1)=1,\quad P(h_2)=0,
\qquad
Q(h_2)=1.
$$

则 \(Q\not\ll P\)，KL infinite。

degenerate Gaussian 例子：\(P\) 在 \(\mathbb R^2\) 上只支持直线 \(w_2=0\)，而 \(Q\) 对 \(w_2\) 有正 variance 或 mean 非零。\(Q\) 把质量放在 \(P\)-null set 外，KL infinite。

## E. AI 迁移

### LT-PBPP-E01

至少记录：

1. pretraining dataset identity/hash；
2. fine-tuning/certificate dataset identity/hash；
3. sample unit；
4. overlap/de-duplication report；
5. pretraining checkpoint 与选择规则；
6. architecture/tokenizer lineage；
7. prior mean/covariance/hyperparameters；
8. prior hyperparameter tuning history；
9. posterior mean/covariance/support；
10. fine-tuning algorithm/seeds；
11. empirical Gibbs sampling protocol；
12. KL implementation与 units；
13. confidence splits；
14. Monte Carlo correction；
15. deployment predictor；
16. final bound 与 trivial baseline。

### LT-PBPP-E02

例如取

$$
\tau_j=2^j,\qquad j\in\mathbb Z
$$

并给可归一化 weights

$$
\pi_j=\frac{c}{(1+|j|)^2},
\qquad
c^{-1}=\sum_{j\in\mathbb Z}(1+|j|)^{-2}.
$$

训练前固定 family \(P_j=\mathcal N(0,\tau_j^2I)\)。训练后选 \(j\) 时可用

$$
\operatorname{KL}(Q\|P_j)
+\log\frac1{\pi_j}
+\log\frac{m+1}{\delta}
$$

作为 numerator。也可直接用 mixture \(P_{\rm mix}=\sum_j\pi_jP_j\) 计算/上界 KL。

### LT-PBPP-E03

采

$$
W_1,\ldots,W_K\overset{\rm iid}{\sim}Q
$$

并计算 \([0,1]\)-valued

$$
L_k=\widehat R_S(h_{W_k}).
$$

Hoeffding 给：以至少 \(1-\eta\) 的 sampling probability，

$$
\widehat R_S(Q)
\le
\frac1K\sum_kL_k
+\sqrt{\frac{\log(1/\eta)}{2K}}.
$$

把这个 upper confidence value 代入 PAC-Bayes inverse-kl，并用 union bound 分配

$$
\delta_{\rm total}
=\delta_{\rm PAC}+\eta_{\rm MC}.
$$

若还调多个 posteriors/priors，应继续加入相应 simultaneous/union budget。
