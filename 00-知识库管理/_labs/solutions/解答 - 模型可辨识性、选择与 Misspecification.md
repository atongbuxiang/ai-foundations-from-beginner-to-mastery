---
type: solution
status: draft
area: [learning-theory/identifiability, misspecification, model-selection]
topic: "[[习题 - 模型可辨识性、选择与 Misspecification]]"
prerequisites: ["[[模型可辨识性、选择与 Misspecification]]"]
related: ["[[正则化、交叉验证与模型选择]]", "[[潜变量模型、混合模型与 EM]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 模型可辨识性、选择与 Misspecification

> [!warning] 解题原则
> 先写可观测law (P_\theta)，再问映射是否单射；先写deployment/scientific target，再选择criterion。一个唯一optimizer、较小AIC或漂亮validation score都不能单独证明parameter真实、模型正确或机制唯一。

## A. 识别与复述

### LT-IDM-A01

- **global identifiability**：
  $$
  P_\theta=P_{\theta'}\Rightarrow\theta=\theta'
  $$
  对整个 (\Theta) 成立；
- **local identifiability**：上述implication只需在目标parameter的某邻域成立；远处仍可有等价points；
- **generic identifiability**：除去lower-dimensional/measure-zero exceptional set后成立，例如distinct mixture components且weights非零时只差permutation；
- **practical identifiability**：finite sample/design下likelihood有足够curvature、uncertainty足够小，可稳定区分邻近laws。

前三者主要是population model map的结构属性；practical identifiability还依赖sample size、design、noise与algorithm/numerics。structurally identifiable也可能因为information eigenvalue极小而难估。

### LT-IDM-A02

- correct specification：存在 (\theta_0) 使 (P_0=P_{\theta_0})；
- pseudo-true parameter：错设时使 (E_0\log p_\theta(X)) 最大、等价地forward KL最小的parameter或set；
- parameter consistency：(\widehat\theta_n) 接近明确parameter target，通常还需identifiability；
- prediction consistency：预测risk接近所定义的oracle/Bayes/model-class optimum，不必恢复unique parameter；
- mechanism recovery：parameter/latent structure确实对应data-generating causal/computational mechanism，需要比observational prediction更强的assumptions或interventions。

它们不可逐级自动推出。错设模型也可预测良好；预测一致也可能沿parameter symmetry有无穷representatives。

### LT-IDM-A03

- AIC：在regular fixed-dimensional likelihood setting中近似expected future log-loss/KL optimism correction；常见误读是“必然选择真实模型”。
- BIC：在regular identifiable models与适当prior下近似log marginal evidence；含真fixed candidate时有model-selection consistency语义；常见误读是“penalty更大所以普遍更正确”。
- CV：模拟指定split下整个learning procedure的held-out task loss；常见误读是“选择后最小CV score仍是无偏最终性能”。

它们的loss、asymptotic target与regularity不同；应按问题选，而不是多数投票。

## B. 手算与数值判断

### LT-IDM-B01

对任意 (c)：

$$
\frac{e^{a_k+c}}{\sum_je^{a_j+c}}
=\frac{e^ce^{a_k}}{e^c\sum_je^{a_j}}
=\frac{e^{a_k}}{\sum_je^{a_j}}.
$$

所以fiber为 (a+\operatorname{span}\{\mathbf1\})。对 (a=(1,2,3))，mean为2，sum-to-zero representative：

$$
\boxed{(-1,0,1)}.
$$

减去last logit 3，last-logit-zero representative：

$$
\boxed{(-2,-1,0)}.
$$

两者logits不同，但softmax probabilities完全相同；它们只是不同gauge。

### LT-IDM-B02

Gaussian negative expected log-likelihood（去常数）是

$$
L(\mu,\sigma^2)
=\frac12\log\sigma^2
+\frac{E_0[(X-\mu)^2]}{2\sigma^2}.
$$

由于

$$
E_0[(X-\mu)^2]=4+(\mu-1)^2,
$$

先对 (\mu) 最小得 (\mu^\star=1)，再对variance得

$$
\boxed{(\mu^\star,(\sigma^2)^\star)=(1,4)}.
$$

这只说明forward-KL Gaussian projection匹配前两moments；不保证density shape、skewness、tail probability、quantiles、rare-event risk或shift下性能正确。

### LT-IDM-B03

$$
\operatorname{AIC}_1=-2(-100)+2(2)=\boxed{204},
$$

$$
\operatorname{AIC}_2=-2(-96)+2(5)=\boxed{202}.
$$

AIC选model 2。

因 (\log100\approx4.60517)：

$$
\operatorname{BIC}_1
=200+2\log100
\approx\boxed{209.21},
$$

$$
\operatorname{BIC}_2
=192+5\log100
\approx\boxed{215.03}.
$$

BIC选model 1。结果不同不矛盾：AIC经典目标偏predictive KL；BIC penalty来自regular marginal-evidence expansion，并在含真候选的特定setting追求model identification。

## C. 推导与证明

### LT-IDM-C01

定义 (\theta\sim\theta'\iff P_\theta=P_{\theta'})。

- reflexive：(P_\theta=P_\theta)，故 (\theta\sim\theta)；
- symmetric：若 (P_\theta=P_{\theta'})，则 (P_{\theta'}=P_\theta)；
- transitive：若 (P_\theta=P_{\theta'}) 且 (P_{\theta'}=P_{\theta''})，则 (P_\theta=P_{\theta''})。

所以它是equivalence relation。class

$$
[\theta]=\{\theta':P_{\theta'}=P_\theta\}
$$

中的每个point对任意sample size都给同一data distribution，因此no observation-only procedure能确定其中哪个coordinate representation“真的发生”。quotient (\Theta/\!\sim) 把整个fiber视为一个observable model point，因而parameter loss、confidence set与mechanistic claim应尽量定义在quotient或invariant functional上。

### LT-IDM-C02

在 (P_0) 与 (P_\theta) 对共同dominating measure有densities (p_0,p_\theta)，且相关expectations有限时：

$$
\begin{aligned}
D_{\rm KL}(P_0\|P_\theta)
&=E_0\log\frac{p_0(X)}{p_\theta(X)}\\
&=E_0\log p_0(X)-E_0\log p_\theta(X).
\end{aligned}
$$

第一项与 (\theta) 无关，故

$$
\boxed{
\arg\max_\theta E_0\log p_\theta(X)
=
\arg\min_\theta D_{\rm KL}(P_0\|P_\theta).
}
$$

若某 (p_\theta=0) 在 (P_0)-positive set上，则KL为 (+\infty)、expected log likelihood为 (-\infty)；support必须正确处理。若 entropy项不有限，可用expected log-likelihood ordering或extended-real formulation，不能随意做 (\infty-\infty)。argmin还可能不取得或不唯一，故一般先定义pseudo-true set。

### LT-IDM-C03

设

$$
s_\theta(X)=\nabla_\theta\log p_\theta(X),
$$

且 (E_0s_{\theta^\star}=0)。interior QMLE满足sample score equation

$$
0=\frac1n\sum_{i=1}^ns_{\widehat\theta}(X_i).
$$

在 (\theta^\star) 作Taylor expansion：

$$
0
=\frac1n\sum_i s_{\theta^\star}(X_i)
+\left[
\frac1n\sum_i\nabla_\theta s_{\widetilde\theta_i}(X_i)
\right](\widehat\theta-\theta^\star).
$$

若sample Hessian uniform趋于 (-H)，(H) nonsingular，则

$$
\sqrt n(\widehat\theta-\theta^\star)
=H^{-1}\frac1{\sqrt n}\sum_i s_{\theta^\star}(X_i)+o_p(1).
$$

令

$$
J=E_0[s_{\theta^\star}s_{\theta^\star}^\top].
$$

multivariate CLT与Slutsky给出

$$
\boxed{
\sqrt n(\widehat\theta-\theta^\star)
\Rightarrow N(0,H^{-1}JH^{-1}).
}
$$

在correctly specified、smooth、interior、identifiable regular model且可交换积分微分时，information equality (H=J=I(\theta_0))，sandwich化简为

$$
I(\theta_0)^{-1}.
$$

dependence、boundary、singularity、nonunique target或high dimension需要不同理论。

## D. 边界、反例与纠错

### LT-IDM-D01

two-component Gaussian mixture 中令 means 为 $(-\delta/2,+\delta/2)$，weights 与 variance 已知。对任何 $\delta\ne0$（modulo label/order constraint）模型可 structurally identifiable；但 $\delta$ 很小时 components 几乎重合，laws 对 $\delta$ 的变化极不敏感，information 很小，likelihood 形成平坦 ridge，finite-sample confidence region 巨大。

这是真实statistical information不足。更多optimizer iterations只能更精确地找到同一平坦objective上的某点，不能让data提供没有的信息。改善需要更大/更有信息量的sample、experimental design、external labels或明确prior；prior会改变inferential target，不能伪装为data identification。

### LT-IDM-D02

令

$$
X=\begin{pmatrix}1&1\\2&2\end{pmatrix}.
$$

其null space包含 (v=(1,-1)^\top)。因此

$$
X(\beta+tv)=X\beta
$$

对任意 (t) 成立，training mean vector可辨识而coefficients不唯一。

若test input (x_\star=(3,3))，则 (x_\star^\top v=0)，prediction对所有representatives相同。若 (x_\star=(1,0))，则

$$
x_\star^\top(\beta+tv)=x_\star^\top\beta+t,
$$

prediction随arbitrary (t) 改变，所以这种off-row-space extrapolation不可由training observations辨识。

### LT-IDM-D03

对每个fixed candidate，validation score可能估计其risk；但选择

$$
\widehat j=\arg\min_j\widehat R_{\rm val}(j)
$$

会偏向那些validation noise恰好有利的candidates。若根据scores继续设计architectures，candidate generation也适配了validation，最小score具有selection optimism。

修复协议：

1. 外层按deployment-relevant user/time groups切分；
2. 只在outer-train中做architecture/checkpoint/hyperparameter adaptive search；
3. inner validation负责选择和early stopping；
4. 锁定完整procedure后在outer-test只评价一次；
5. 若需稳定estimate，使用nested CV汇总outer scores；
6. 若看outer结果后继续修改，保留全新confirmatory test或明确其已成为development set。

最终fit可用全部development data重训，但reported outer performance评价的是selection procedure，而不是已见outer data后继续调优的新procedure。

## E. AI 迁移

### LT-IDM-E01

LLM selection protocol：

- 预注册target vector：task success、proper probabilistic score、safety、latency/cost与group constraints；
- observation unit按conversation/user/source/time切分，避免prompt variants跨fold；
- outer split模拟future deployment；
- outer-train内记录所有checkpoints、decoding、prompt/reranker与人工反馈的adaptive search transcript；
- inner loop选择一次，并固定aggregation/tie-breaking；
- outer evaluation报告uncertainty、per-group calibration、failure taxonomy与cost，而非只报winner；
- final test之前锁定model card和threshold；
- shift suite覆盖新domain、time、language与adversarial inputs；
- 选择后若要做参数/差异显著性推断，使用outer folds或独立confirmatory data。

### LT-IDM-E02

错设是常态，因此 uncertainty report应分层：

1. **sampling uncertainty conditional on procedure**：对well-defined estimator可用bootstrap、cluster/HAC或适当sandwich；
2. **model uncertainty**：alternative likelihoods/architectures/ensembles与sensitivity，不由单一sandwich覆盖；
3. **optimization/Monte Carlo uncertainty**：seeds、decoding samples、finite ensemble；
4. **selection uncertainty**：搜索多个candidates后的optimism与winner instability；
5. **distribution shift**：scenario/stress tests、importance assumptions、online calibration；iid standard errors不包含未知shift bias；
6. **target uncertainty**：human labels/preferences本身的 disagreement与temporal drift。

报告预测interval/score时要写其conditioning set、coverage population、groups与validation regime，不能只给一个“95% confidence”。

### LT-IDM-E03

若同层hidden units可permutation，交换所谓“事实核验neuron”与另一个unit并同步交换相邻weights，end-to-end function不变。ReLU等positive-homogeneous network还可作

$$
(a_j,w_j)\mapsto(a_j/c,cw_j),
$$

激活幅值与weights改变但function不变。因此单一index或magnitude不是gauge-invariant evidence。

更可信审计需要：

- 明确claim在parameter、activation还是function/intervention层；
- 跨seeds/checkpoints做permutation/rotation alignment；
- 使用causal intervention/ablation并控制downstream compensations；
- 检查specificity：干预是否只影响fact verification而非广泛能力；
- 用counterfactual datasets与held-out facts复现；
- 测试distributed representation与multiple sufficient pathways；
- 把结论限制为equivalence-invariant functional或稳定subspace，而非任意neuron编号。

observational correlation或linear probe成功只说明information可读出，不证明该neuron是唯一、必要或因果模块。
