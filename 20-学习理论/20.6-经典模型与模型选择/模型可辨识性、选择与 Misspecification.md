---
type: theorem
status: draft
area: [learning-theory/identifiability, misspecification, quasi-mle, model-selection]
aliases: [Identifiability and Misspecification, Pseudo-true Parameter, Sandwich Covariance, AIC BIC and CV]
node_id: LT-52
prerequisites: ["[[统计模型、估计量与偏差方差]]", "[[最大似然估计与 MAP]]", "[[Fisher 信息、Cramér–Rao 界与渐近正态性]]", "[[正则化、交叉验证与模型选择]]", "[[潜变量模型、混合模型与 EM]]"]
related: ["[[K-Means、聚类风险与不可辨识性]]", "[[线性回归的统计学习理论]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
sources: ["[[S-1982-White-Misspecified-MLE]]", "[[S-1974-Akaike-Statistical-Model-Identification]]", "[[S-1978-Schwarz-Model-Dimension]]", "[[S-1963-Teicher-Finite-Mixture-Identifiability]]", "[[S-2009-Hastie-Tibshirani-Friedman-ESL]]"]
exercises: ["[[习题 - 模型可辨识性、选择与 Misspecification]]"]
solutions: ["[[解答 - 模型可辨识性、选择与 Misspecification]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-identifiability-selection-misspecification-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 模型可辨识性、选择与 Misspecification

> [!abstract] 本章主问题
> 参数模型不是一个公式集合，而是一张从 parameter space 到 probability laws 的映射：
>
> $$
> T:\Theta\to\mathcal P,
> \qquad
> T(\theta)=P_\theta.
> $$
>
> 若不同参数给出同一个 law，data 即使无限多也不能区分它们；若 true law (P_0) 根本不在 model family 中，MLE 通常收敛到 KL 意义下最接近的 **pseudo-true parameter**，而不是真实机制。AIC、BIC 与 cross-validation 又分别近似不同的 selection target，不能被当成同一把“模型好坏尺”。
>
> 本章把四个层次严格分开：
>
> 1. **structural identifiability**：population law是否唯一确定parameter；
> 2. **estimability / practical identifiability**：finite data中能否稳定估计；
> 3. **correct specification**：true law是否属于 model family；
> 4. **selection target**：想要预测、evidence、结构恢复，还是可解释参数。

> [!question] 初学者读完必须能回答
> 1. 参数不可辨识与“样本太少”有什么根本区别？
> 2. 为什么线性回归参数不可唯一时，某些预测仍可以唯一？
> 3. misspecified MLE 的 population target 是什么？
> 4. information equality 为什么在错设下失效，sandwich covariance 从何而来？
> 5. AIC、BIC 与 CV 各自近似什么目标？
> 6. 为什么 mixture 与 neural network 中不能机械使用 parameter count？

## 一、学习目标

1. 把 statistical model写成 (\theta\mapsto P_\theta)；
2. 定义 global、local、generic 与 practical identifiability；
3. 用 equivalence class 与 quotient parameter描述模型对称性；
4. 区分 parameter identifiability 与 prediction/functional identifiability；
5. 推导 misspecified MLE 的 KL projection；
6. 推导 (H^{-1}JH^{-1}) sandwich asymptotic covariance；
7. 比较 AIC、BIC 与 cross-validation 的目标及regularity条件；
8. 审计 mixture、softmax 与 neural network 中的 symmetry；
9. 识别 weak information、boundary、singularity与post-selection bias；
10. 为 AI 模型写出可复核的 model-card contract。

## 二、先固定对象：模型是一张映射

令样本空间为 (\mathcal X)，probability laws 集合为 (\mathcal P(\mathcal X))，parameter space 为 (\Theta)。parametric family写成

$$
\mathcal M
=
\{P_\theta:\theta\in\Theta\}.
$$

真正负责 identifiability 的对象不是符号 (\theta)，而是映射

$$
T:\Theta\to\mathcal M,
\qquad
\theta\mapsto P_\theta.
$$

> [!warning] 三个层次不可混写
> - (\theta)：parameter representation；
> - (P_\theta)：由参数诱导的 observable law；
> - (P_0)：实际 data-generating law。
>
> 参数优化器返回一个 (\widehat\theta)，不等于它恢复了唯一的真实参数；(P_0\notin\mathcal M) 时甚至不存在“生成 (P_0) 的模型参数”。

## 三、Global Identifiability

模型全局可辨识，当且仅当

$$
\boxed{
P_{\theta_1}=P_{\theta_2}
\Longrightarrow
\theta_1=\theta_2.
}
$$

也就是 (T) 是 injective。

若存在 (\theta_1\ne\theta_2) 但 (P_{\theta_1}=P_{\theta_2})，则任何只由观测 data 计算的统计量都不可能区分二者，因为它们诱导完全相同的 sample law：

$$
P_{\theta_1}^{\otimes n}
=
P_{\theta_2}^{\otimes n}
\qquad
\text{for every }n.
$$

这不是“需要更多 data”的问题；即使 (n\to\infty)，observable distribution仍相同。

### 3.1 Equivalence Class 与 Quotient Parameter

定义

$$
\theta\sim\theta'
\iff
P_\theta=P_{\theta'}.
$$

参数 (\theta) 的 equivalence class（也称 fiber）是

$$
[\theta]
=
\{\theta'\in\Theta:P_{\theta'}=P_\theta\}.
$$

data至多识别这个 class。真正由 observable law 索引的对象是 quotient space

$$
\Theta/\!\sim.
$$

处理不可辨识性有三条合法路线：

1. 加约束选择 class 中一个 representative；
2. 直接报告 invariant functional (g([\theta]))；
3. 承认多个等价解，而不赋予任意 coordinate 机制意义。

## 四、四个例子：同样是“不唯一”，含义不同

### 4.1 Softmax 的 Additive Symmetry

对 logits (a=(a_1,\ldots,a_K))，

$$
p_k(a)
=
\frac{e^{a_k}}{\sum_j e^{a_j}}.
$$

对任何常数 (c)，

$$
p_k(a+c\mathbf 1)=p_k(a).
$$

所以 unconstrained logits只识别到

$$
[a]=\{a+c\mathbf 1:c\in\mathbb R\}.
$$

可设 (a_K=0) 或 (\sum_ka_k=0) 选定 gauge；概率本身无需这种任意选择。

### 4.2 Rank-deficient Linear Regression

fixed design regression中，若 (Xv=0)，则

$$
X(\beta+v)=X\beta.
$$

因此 training-design 上的 mean vector (X\beta) 可唯一，而 (\beta) 不唯一。对新输入 (x_\star)：

- 若 (x_\star^\top v=0) 对所有 (v\in\ker X)，预测 (x_\star^\top\beta) 可辨识；
- 否则 extrapolation 会依赖任意 representative。

这说明 **prediction identifiability 可以弱于 parameter identifiability**。

### 4.3 Mixture Label Switching

对 two-component mixture，交换

$$
(\pi_1,\eta_1),(\pi_2,\eta_2)
$$

不改变 marginal density。若 components distinct，finite mixture 可能只在 permutation 意义下可辨识：应该识别 unordered set，而不是第 1 个/第 2 个 component 的名字。

### 4.4 Neural Network Symmetry

单 hidden layer网络

$$
f(x)
=
\sum_{j=1}^m a_j\sigma(w_j^\top x)
$$

对 hidden units 的 permutation保持函数不变。若 (\sigma) positive homogeneous（如 ReLU），对 (c>0)：

$$
a_j\sigma(w_j^\top x)
=
\frac{a_j}{c}\sigma((cw_j)^\top x).
$$

因此 parameter-space distance、单个 neuron identity 与 Hessian zero directions都可能受 symmetry影响；function-space behavior通常更接近可观测对象。

## 五、Local、Generic 与 Practical Identifiability

### 5.1 Local Identifiability

在 (\theta_0) 的某邻域内，若

$$
P_\theta=P_{\theta_0}
\Longrightarrow
\theta=\theta_0,
$$

则称 (\theta_0) locally identifiable。local不保证 global：远处仍可能有等价参数。

### 5.2 Generic Identifiability

若除去 lower-dimensional exceptional set 后可辨识，称 generically identifiable。mixture components重合、mixing weight为零或parameter落在boundary时，常进入 exceptional set。

### 5.3 Fisher Information 的局部诊断

score为

$$
s_\theta(X)=\nabla_\theta\log p_\theta(X),
$$

Fisher information为

$$
I(\theta)
=
E_\theta[s_\theta(X)s_\theta(X)^\top].
$$

若存在 smooth curve (\theta(t)) 满足 (P_{\theta(t)}) 在 (t=0) 附近不变，令 (v=\dot\theta(0))，则通常

$$
v^\top s_{\theta_0}(X)=0
\quad\text{a.s.},
\qquad
I(\theta_0)v=0.
$$

所以 exact continuous symmetry常造成 singular information。

> [!warning] 反向推理需要regularity
> singular Fisher information 可能来自 boundary、non-smooth parameterization 或higher-order identification；nonsingular information也只支持局部regular结论，不自动证明global identifiability。

### 5.4 Practical Identifiability

即使 structural identifiability成立，finite sample中仍可能非常难估：

- Fisher information 的最小 eigenvalue 很小；
- mixture components几乎重合；
- features高度collinear；
- likelihood有长而平的 ridge；
- signal-to-noise ratio过低。

这是 **weak identification**：不是完全相同的 laws，而是许多 laws 在当前 sample size 下太接近。更多有效 data、better design 或合理prior可能改善它；它不能通过给 optimizer 跑更多步根治。

## 六、Correct Specification 与 Misspecification

### 6.1 Correctly Specified Model

若存在 (\theta_0\in\Theta) 使

$$
P_0=P_{\theta_0},
$$

称模型 correctly specified。若模型还 identifiable，才可以把 (\theta_0) 视为唯一 true parameter。

### 6.2 Misspecified Model

若

$$
P_0\notin\mathcal M,
$$

模型错设。现实中常见来源包括：

- conditional mean形式错误；
- noise distribution或variance错误；
- independence assumption错误；
- omitted variables / latent dependence；
- label noise或selection bias；
- train与deployment distributions不同。

错设不意味着模型毫无用途；它意味着必须重新说明 estimator 的 target 与 uncertainty。

## 七、Misspecified MLE 收敛到什么？

设 dominated model有density (p_\theta)，数据 iid 来自 (P_0)，MLE/QMLE为

$$
\widehat\theta_n
\in
\arg\max_{\theta\in\Theta}
\frac1n\sum_{i=1}^n\log p_\theta(X_i).
$$

在 uniform law of large numbers、compactness/identification 等适当条件下，empirical criterion趋近

$$
M(\theta)
=
E_0[\log p_\theta(X)].
$$

定义 pseudo-true set

$$
\Theta^\star
=
\arg\max_{\theta\in\Theta}M(\theta).
$$

因为

$$
\begin{aligned}
D_{\mathrm{KL}}(P_0\|P_\theta)
&=
E_0\left[
\log\frac{p_0(X)}{p_\theta(X)}
\right]\\
&=
E_0[\log p_0(X)]-E_0[\log p_\theta(X)],
\end{aligned}
$$

第一项与 (\theta) 无关，故

$$
\boxed{
\Theta^\star
=
\arg\min_{\theta\in\Theta}
D_{\mathrm{KL}}(P_0\|P_\theta).
}
$$

若 minimizer唯一，记为 (\theta^\star)，则在合适条件下

$$
\widehat\theta_n\xrightarrow{p}\theta^\star.
$$

> [!important] 一致性必须带目标
> “MLE consistent”在错设下通常是对 (\theta^\star) 的一致，而不是对某个真实机制参数的一致。KL projection还依赖选用的 likelihood、observed variables 与 sampling law。

## 八、Worked Example：用 Gaussian 拟合非 Gaussian Data

假设 (P_0) 具有有限 mean (m_0) 与variance (v_0>0)，但不必是 Gaussian。用

$$
q_{\mu,\sigma^2}(x)
=
\frac1{\sqrt{2\pi\sigma^2}}
\exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

拟合。population negative log-likelihood（忽略常数）为

$$
L(\mu,\sigma^2)
=
\frac12\log\sigma^2
+
\frac{E_0[(X-\mu)^2]}{2\sigma^2}.
$$

而

$$
E_0[(X-\mu)^2]
=
v_0+(\mu-m_0)^2.
$$

所以先对 (\mu) 最小化得到 (\mu^\star=m_0)，再对 (\sigma^2) 最小化得到

$$
\boxed{
\mu^\star=m_0,
\qquad
(\sigma^2)^\star=v_0.
}
$$

Gaussian family虽然错设，pseudo-true parameters仍匹配前两阶 moments。但这不保证 Gaussian tail probabilities、quantiles 或 rare-event risk正确。

## 九、Sandwich Covariance：为什么不是 (I^{-1})

令单样本 criterion

$$
m_\theta(X)=\log p_\theta(X),
$$

score

$$
s_\theta(X)=\nabla_\theta m_\theta(X).
$$

在 interior pseudo-true parameter处，一阶条件为

$$
E_0[s_{\theta^\star}(X)]=0.
$$

定义

$$
H
=
-E_0[\nabla_\theta^2m_{\theta^\star}(X)],
\qquad
J
=
E_0[s_{\theta^\star}(X)s_{\theta^\star}(X)^\top].
$$

sample first-order condition是

$$
0
=
\frac1n\sum_{i=1}^ns_{\widehat\theta_n}(X_i).
$$

在 (\theta^\star) 展开：

$$
0
\approx
\frac1n\sum_{i=1}^ns_{\theta^\star}(X_i)
-H(\widehat\theta_n-\theta^\star).
$$

乘 (\sqrt n)：

$$
\sqrt n(\widehat\theta_n-\theta^\star)
\approx
H^{-1}
\frac1{\sqrt n}
\sum_{i=1}^ns_{\theta^\star}(X_i).
$$

由 multivariate CLT，

$$
\boxed{
\sqrt n(\widehat\theta_n-\theta^\star)
\Rightarrow
N\left(0,H^{-1}JH^{-1}\right).
}
$$

这个 bread–meat–bread 结构称 sandwich covariance。

### 9.1 Correct Specification 是特殊情形

在 correctly specified、interior、smooth 且可交换 differentiation/integration 的regular model中，information equality给出

$$
H=J=I(\theta_0),
$$

于是 covariance退化为 (I(\theta_0)^{-1})。错设下一般

$$
H\ne J,
$$

只用 inverse Hessian会漏掉 score variability。

> [!warning] Sandwich 也不是万能修复
> clustering/dependence需要相应 cluster/HAC meat；boundary、singular model、nonunique pseudo-true set、heavy tails或 high-dimensional (d/n\not\to0) 时，standard root-(n) sandwich theory可能不成立。

## 十、参数风险与预测风险不是一回事

parameter loss可能是

$$
\|\widehat\theta-\theta_0\|^2,
$$

但在有 symmetry 时这个 loss 依赖 arbitrary representative。合法 alternatives包括

$$
\inf_{g\in G}
\|\widehat\theta-g\theta_0\|,
$$

或 function/distribution distance

$$
E_X[(f_{\widehat\theta}(X)-f_{\theta_0}(X))^2],
\qquad
D(P_{\widehat\theta},P_{\theta_0}).
$$

反过来，良好的 average prediction也不保证：

- causal parameters正确；
- tail risk正确；
- subgroup calibration正确；
- out-of-distribution predictions稳定；
- latent variables对应人类语义。

## 十一、为什么 Model Selection 需要惩罚？

若候选 (\mathcal M_1\subset\mathcal M_2)，larger model的 maximized training likelihood不会更差：

$$
\ell_n(\widehat\theta_2)
\ge
\ell_n(\widehat\theta_1).
$$

但同一 data 同时用于 fitting 与 scoring，training fit有 optimism。selection criterion必须回答：是在估计 future predictive loss、integrated evidence，还是希望恢复一个固定的true candidate？

## 十二、AIC：Regular Parametric Predictive KL

对 dimension (d) 的regular likelihood model，Akaike information criterion为

$$
\boxed{
\operatorname{AIC}
=
-2\ell_n(\widehat\theta)+2d.
}
$$

选择数值更小者。其经典推导目标是修正 in-sample maximized log-likelihood对 expected out-of-sample log-loss/KL risk 的 optimism。

AIC的语义不是：

- posterior model probability；
- 对所有任务都一致恢复 true model；
- 可以无视 adaptive candidate search；
- 在 singular model中仍可直接把 raw parameter count 当 (d)。

有限样本、Gaussian linear model常使用 AICc修正；effective degrees of freedom也可能不同于 nominal count。

## 十三、BIC：Regular Laplace Evidence Approximation

Schwarz criterion常写为

$$
\boxed{
\operatorname{BIC}
=
-2\ell_n(\widehat\theta)+d\log n.
}
$$

在 fixed-dimensional、regular、identifiable models与适当prior下，它对应 marginal likelihood 的 large-(n) Laplace approximation。若 finite candidate list中含true regular model，BIC有 model-identification consistency 的经典语义。

当 $P_0$ 不在 candidates、dimension 随 $n$ 增长、prior 在关键处退化或 model singular 时，机械套用 $d\log n$ 失去原推导保证。

## 十四、Cross-Validation：直接模拟 Held-out Pipeline

Cross-validation估计的是指定 split mechanism 下，整个 learning procedure 的 held-out loss：

$$
\widehat R_{\rm CV}(A_j)
=
\frac1K
\sum_{k=1}^K
\frac1{|V_k|}
\sum_{i\in V_k}
\ell\left(
A_j(S\setminus V_k),Z_i
\right).
$$

CV可使用与部署任务一致的 loss，也能包含 preprocessing、regularization与early stopping；代价是 split variance、training-size bias与selection reuse。若还要估计 selected procedure 的性能，需要 nested CV或独立test。

## 十五、AIC、BIC、CV 不是同一把尺

| 方法 | 主要 target | 经典条件 | 常见误读 |
|---|---|---|---|
| AIC | expected predictive log-loss / KL | regular parametric, fixed dimension, MLE asymptotics | “选择真实模型” |
| BIC | marginal evidence近似；含真候选时结构识别 | regular identifiable model, fixed dimension, suitable prior | “总比AIC更保守所以更正确” |
| CV | 指定 split/pipeline 的 held-out task loss | split匹配exchangeability/dependence，pipeline无leakage | “一个CV数值就是无偏最终性能” |

### 15.1 数值例子

设 model 1 有 (d_1=2)、(\ell_1=-100)；model 2 有 (d_2=5)、(\ell_2=-96)。则

$$
\operatorname{AIC}_1=204,
\qquad
\operatorname{AIC}_2=202,
$$

AIC选 model 2。若 (n=100)，

$$
\operatorname{BIC}_1
=200+2\log100
\approx209.21,
$$

$$
\operatorname{BIC}_2
=192+5\log100
\approx215.03,
$$

BIC选 model 1。两者没有矛盾：它们的 asymptotic targets不同。

## 十六、图解：从 Parameter Fibers 到 Selection Target

先看图回答：一个 model selection criterion 数值更小，为什么既不能证明 parameter 可辨识，也不能证明 model correctly specified？

![[00-知识库管理/_assets/figures/learning-theory/fig-identifiability-selection-misspecification-v2.svg|900]]

> [!figure] 图 20.6-12　可辨识对象、错设投影与选择目标
> 左栏显示多个 parameter points可以落到同一个 observable law；中栏把 true law投影到 misspecified model family，并区分 curvature \(H\) 与 score variability \(J\)；右栏再问 selection criterion对准 predictive KL、regular Bayesian evidence还是 held-out task loss。来源：依据 Teicher、White、Akaike、Schwarz与ESL独立绘制；确定性 SVG，由 [[plot_classical_models_unsupervised_v2.py]] 生成。

**怎样读图**：顺序不能倒置。先决定 data 能识别 parameter、equivalence class 还是prediction；再说明 \(P_0\in\mathcal M\) 或 KL projection；最后才根据部署或科学目标选择 AIC、BIC、CV 或独立验证。

**图没有证明什么**：它没有证明 sandwich covariance 对 singular/high-dimensional/dependent data 自动有效，也没有证明 AIC、BIC 或 CV 中存在无条件最优者；每条路线仍需要各自的regularity、数据切分与target合同。

## 十七、Singular Models：Mixture 与 Neural Network 的特殊危险

regular likelihood theory通常假设：

- parameter interior；
- locally identifiable；
- Fisher information nonsingular；
- likelihood可作quadratic approximation；
- effective dimension固定。

mixtures与neural networks常违反这些条件：

- label/permutation symmetry；
- redundant components/units；
- zero mixing weights或boundary；
- merging components；
- scaling symmetry；
- non-isolated optima与singular Hessian。

因此 raw parameter count不一定等于 effective complexity；regular AIC/BIC penalty与chi-square likelihood-ratio calibration不能自动搬用。

## 十八、Model Checking 不等于 Model Proof

合法检查包括：

- residual pattern与heteroskedasticity；
- calibration by subgroup/time；
- posterior/predictive checks；
- tail与extreme-event error；
- sensitivity to alternative likelihoods；
- influence与outlier diagnostics；
- train/deployment shift；
- negative controls或simulation-based calibration。

检查不拒绝模型只表示“当前诊断未发现足够证据”，不是模型为真。反过来，大样本下极小、无关紧要的deviation也可能显著；需要同时报告 practical effect。

## 十九、Selection 后的 Inference

若同一 data 被用于：

1. 构造 candidates；
2. 选择最优candidate；
3. 报告 selected model 的 coefficient confidence interval；

则 conventional fixed-model interval通常忽略selection event，coverage可能失真。可采用：

- independent confirmatory sample；
- sample splitting / cross-fitting；
- selective inference；
- model averaging与stability analysis；
- 清楚标注 exploratory 而非 confirmatory claim。

candidate search越adaptive，越不能只把最后保留的几个models当作全部 multiplicity。

## 二十、Distribution Shift 下的边界

KL projection

$$
\theta^\star
\in
\argmin_\theta
D_{\rm KL}(P_0\|P_\theta)
$$

只针对训练 law (P_0)。deployment law变成 (Q) 后，目标可能变为

$$
\argmin_\theta
E_Q[-\log p_\theta(X)],

$$

未必仍由同一 (\theta^\star) 最优。in-distribution sandwich covariance也不包含未知shift造成的 systematic bias。

## 二十一、AI 接口

### 21.1 Checkpoint 与 Architecture Selection

validation perplexity、human preference、safety rate与latency是不同targets。先写 deployment utility，再定 selection rule；不能用一个aggregate score替所有维度。

### 21.2 Representation 的 Gauge Freedom

hidden representation常可经可逆rotation、permutation或scaling而保持 end-to-end function。逐coordinate解释前必须建立 alignment/invariant，否则“第 (j) 个神经元的意义”可能依赖任意 basis。

### 21.3 Mechanistic Claim

预测相同不表示内部机制唯一。parameter intervention若沿不可辨识fiber改变，observable fit不能决定哪个内部叙事为真；需要额外 interventions、architectural constraints或 causal assumptions。

### 21.4 Uncertainty under Misspecification

大型模型几乎总是错设。reported uncertainty至少要问：

- aleatoric还是epistemic？
- conditional on fixed model还是包含selection？
- iid sampling还是cluster/time dependence？
- in-distribution还是shift-aware？
- average calibration还是tail/subgroup calibration？

## 二十二、完整审计清单

### 22.1 Identifiability

- [ ] 写清 observable law (P_\theta)；
- [ ] 列出 known symmetries/equivalence group；
- [ ] 区分 global、local、generic、practical；
- [ ] 选择 invariant loss或声明 gauge；
- [ ] 检查 boundary与singular information。

### 22.2 Misspecification

- [ ] 写明 (P_0\in\mathcal M) 是假设还是证据；
- [ ] 定义 pseudo-true target；
- [ ] 检查 independence/variance/link assumptions；
- [ ] 使用与dependence匹配的robust covariance；
- [ ] 做 residual、tail、subgroup 与shift diagnostics。

### 22.3 Selection

- [ ] 先写 selection target；
- [ ] 记录所有 searched candidates与human/agent feedback；
- [ ] preprocessing完全置于 folds 内；
- [ ] 区分 inner selection与outer evaluation；
- [ ] selected-model inference不假装model预先固定。

## 二十三、常见错误

1. 把 optimizer返回唯一数组当作 model identifiable；
2. 用 Hessian nonsingular 宣称 global identifiability；
3. 在 misspecified model中仍把 (I^{-1}) 当标准误；
4. 把 pseudo-true parameter叫作真实机制；
5. 把 AIC、BIC 与 CV 看成只差 penalty strength；
6. 对 mixture/NN直接套 regular parameter count；
7. 用 training/selection data再次报告无修正confidence；
8. average prediction好就声称 subgroup、tail 与 shift 都可靠；
9. 把 latent component编号赋予固定人类语义；
10. diagnostics没拒绝就宣布模型正确。

## 二十四、最小记忆

1. **可辨识性是映射 (\theta\mapsto P_\theta) 是否单射，不是优化器是否给出一个答案。**
2. **有 symmetry 时，data识别的是 equivalence class；loss也应尊重这个 symmetry。**
3. **错设 MLE 的 target 是 (\arg\min_\theta D_{\rm KL}(P_0\|P_\theta))。**
4. **错设下 asymptotic covariance通常是 (H^{-1}JH^{-1})，不是单纯 inverse Hessian。**
5. **AIC偏 predictive KL，BIC偏regular evidence/true-model recovery，CV偏指定pipeline的held-out task loss。**
6. **预测表现、参数解释、机制恢复与 shift robustness 是四种不同claim。**

## 二十五、掌握标准

- [ ] 能从 model map判断 global identifiability；
- [ ] 能写出 softmax、mixture与NN的 equivalence classes；
- [ ] 能解释 parameter不可辨识但prediction可辨识的例子；
- [ ] 能独立推导 KL projection；
- [ ] 能从 score expansion推导 sandwich covariance；
- [ ] 能根据科学目标选择 AIC、BIC、CV或承认它们都不充分；
- [ ] 能指出 regular criteria 在 singular model中的失效条件；
- [ ] 能设计 model checking、selection与confirmatory evaluation协议；
- [ ] 能把 AI representation/机制claim写成 invariant、可检验陈述。

## 二十六、练习与独立详解

- 练习：[[习题 - 模型可辨识性、选择与 Misspecification]]
- 独立详解：[[解答 - 模型可辨识性、选择与 Misspecification]]

## 参考来源

- [[S-1982-White-Misspecified-MLE]]
- [[S-1974-Akaike-Statistical-Model-Identification]]
- [[S-1978-Schwarz-Model-Dimension]]
- [[S-1963-Teicher-Finite-Mixture-Identifiability]]
- [[S-2009-Hastie-Tibshirani-Friedman-ESL]]

## 相关链接

- [[最大似然估计与 MAP]]
- [[Fisher 信息、Cramér–Rao 界与渐近正态性]]
- [[正则化、交叉验证与模型选择]]
- [[潜变量模型、混合模型与 EM]]
- [[K-Means、聚类风险与不可辨识性]]
