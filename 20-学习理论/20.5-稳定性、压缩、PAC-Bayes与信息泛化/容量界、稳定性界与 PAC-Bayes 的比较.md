---
type: comparison
status: draft
area: [learning-theory/generalization-certificates, bound-selection, audit]
aliases: [Generalization Bounds Comparison, Capacity Stability Compression PAC-Bayes Information]
node_id: LT-40
prerequisites: ["[[VC 一致收敛与泛化界]]", "[[Rademacher 复杂度与经验复杂度]]", "[[算法稳定性与替换一个样本]]", "[[样本压缩方案与泛化]]", "[[PAC-Bayes Bound 的测度变换主线]]", "[[互信息与信息论泛化界]]"]
related: ["[[结构风险最小化与非一致可学习性]]", "[[局部 Rademacher 复杂度与快收敛率]]", "[[神经网络容量与 Norm-Based Bound]]", "[[深度泛化证据地图与开放问题]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]", "[[S-2002-Bousquet-Elisseeff-Stability-Generalization]]", "[[S-2002-Seeger-PAC-Bayesian-Generalization]]", "[[S-2017-Xu-Raginsky-Information-Generalization]]"]
exercises: ["[[习题 - 容量界、稳定性界与 PAC-Bayes 的比较]]"]
solutions: ["[[解答 - 容量界、稳定性界与 PAC-Bayes 的比较]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-generalization-certificates-comparison-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 容量界、稳定性界与 PAC-Bayes 的比较

> [!abstract] 本章主问题
> VC/Rademacher 容量、算法稳定性、样本压缩、PAC-Bayes 与 mutual information 都能解释“为什么训练得到的对象可能泛化”，但它们不是同一公式的五种写法。它们分别控制 hypothesis class、neighboring-sample sensitivity、reconstructible description、posterior-to-prior change 与 sample–output dependence；也分别产生 uniform/high-probability、algorithm-specific、Gibbs 或 expected-signed guarantees。正确比较必须先对齐 sample、loss、risk、output、randomness、confidence 与 selection protocol，再比较数值是否 nonvacuous。

> [!question] 初学者读完必须能回答
> 1. 五类 certificate 的复杂度对象分别是什么？
> 2. 哪些是 uniform over hypotheses，哪些绑定具体 algorithm 或 randomized output？
> 3. 为什么 \(\log|\mathcal H|\)、code length、KL 与 mutual information 可能长得相似却不能直接互换？
> 4. 为什么 stability 小不等于 risk 小？
> 5. 为什么训练后从多个 bounds 中取最小值也可能需要 selection correction？
> 6. 面对一个 AI system 应怎样选择第一条可审计路线？

## 一、学习目标

1. 建立五类 generalization certificate 的共同坐标系；
2. 对齐各自的对象、量词、假设、输出与保证类型；
3. 识别 finite-class/description-length 的交叉特例；
4. 解释 stability、PAC-Bayes 与 information 不能无条件互推；
5. 区分 logical validity、nonvacuity、tightness 与 explanatory adequacy；
6. 设计 predeclared multi-certificate selection；
7. 为 convex model、compressed model、stochastic network 与 adaptive selection 选型；
8. 为 deep-learning generalization 保留理论边界与证据等级。

## 二、比较前先写共同对象合同

任何两个 bounds 比较前，先填：

$$
\boxed{
(\mathcal D,\ S,\ A,\ \mathcal H,\ \ell,\ R,\ \widehat R,\ \text{output},\ \delta).}
$$

具体问：

1. sample unit 是 token、example、document 还是 user？
2. \(S\) 是否 i.i.d.？
3. loss 是 0–1、bounded surrogate 还是 unbounded cross-entropy？
4. output 是 deterministic \(h\)、randomized \(W\)、posterior \(Q\) 还是 transcript？
5. population risk 与 empirical risk 是否针对同一 predictor？
6. probability 是 over sample、algorithm randomness 还是两者？
7. guarantee 是 expectation 还是 probability \(1-\delta\)？
8. hyperparameter/model/bound selection 是否使用了同一数据？

如果合同不同，右侧 numerical values 即使都叫“complexity”也不可直接排序。

## 三、图解：五类证书与量词

先回答：**为什么图中“先对齐量词”位于“比较 bound 数值”之前？**

![[00-知识库管理/_assets/figures/learning-theory/fig-generalization-certificates-comparison-v2.svg|900]]

> [!figure] 图 20.5.8｜容量、稳定性、压缩、PAC-Bayes 与信息证书的统一审计
> 左栏把五种 complexity 放在同一个 risk-gap 问题周围；中栏标明 class supremum、neighboring samples、decoder、posterior 与 average channel 的不同量词；右栏提醒 post-hoc 选择最小证书也要预声明或分配置信预算。来源：依据本卷 LT-33—39 与经典学习理论主线独立绘制；确定性 SVG，由 [[plot_pac_bayes_information_v2.py]] 生成。

**怎样读图。** 五类 bounds 是互补观察镜头。某个 neural network 可以同时属于大 class、由稳定 algorithm 训练、被量化、配有 noisy posterior，并作为有限 transcript 发布；每个镜头回答不同问题。

**图没有证明什么。** 它没有声称五类 bound exhaust 所有泛化理论，也没有给出一种总能选出最紧界的无偏 procedure。

## 四、五类证书总表

| 路线 | complexity 对象 | 典型量词 | 直接保证 | 主要优势 | 主要缺口 |
|---|---|---|---|---|---|
| VC/Rademacher/容量 | class \(\mathcal H\) 或 loss class | \(\sup_{h\in\mathcal H}\) | 多为 high-probability uniform gap | algorithm agnostic；可支持 ERM | 对大深网 class 可能 vacuous |
| stability | algorithm \(A\) 对 \(S\simeq S'\) 的 loss 敏感性 | neighboring samples | expected 或 high-probability gap | 绑定实际 optimizer/regularization | 需敏感性假设；不直接给 low risk |
| sample/description compression | compressed witnesses/code + fixed decoder | all legal descriptions | 多为 high-probability risk/gap | 直接连接可重构描述 | decoder、side info、lossy case 难 |
| PAC-Bayes | posterior \(Q\) 相对 prior \(P\) | simultaneous over \(Q\) | high-probability Gibbs-risk certificate | data-dependent posterior；可优化 | prior legality；stochastic predictor；KL parameterization |
| mutual information | channel \(P_{W\mid S}\) | average joint dependence | 基础式为 expected signed gap | algorithm/distribution dependent；composition | MI 难算；continuous deterministic 可 infinite；非 tail |

## 五、容量路线：控制整个函数类

典型形式：

$$
\mathbb P_S\left[
\sup_{h\in\mathcal H}
|R(h)-\widehat R_S(h)|
\le \operatorname{Comp}(\mathcal H,S,m,\delta)
\right]\ge1-\delta.
$$

复杂度可以是：

- \(\log|\mathcal H|\)；
- VC dimension；
- growth function；
- empirical Rademacher complexity；
- covering number；
- norm/margin complexity；
- localized complexity。

### 5.1 优势

因为 event 同时覆盖所有 \(h\in\mathcal H\)，任何用 \(S\) 选择的 ERM/SRM output 都可代入。它不要求知道 optimizer 的 sensitivity。

### 5.2 缺口

若 \(\mathcal H\) 是能表达大量 labelings 的 overparameterized network class，worst-case capacity 可能远大于实际 algorithm 探索的区域。

“VC bound vacuous”不等于 uniform convergence 数学错误；它表示 chosen class/scale 没有为当前 sample 提供 informative certificate。

## 六、Stability 路线：控制算法对一个样本的反应

replace-one uniform stability 典型定义：

$$
\sup_{z}
|\ell(A(S),z)-\ell(A(S'),z)|
\le\beta_m
$$

对任意只差一个 coordinate 的 \(S,S'\)。

基础 expected guarantee：

$$
\left|
\mathbb E[R(A(S))-\widehat R_S(A(S))]
\right|
\le\beta_m.
$$

bounded loss 下可进一步得到 high-probability variants。

### 6.1 优势

- 直接分析 actual algorithm；
- strong convex regularization 给 \(\beta_m=O(1/m)\)；
- iterative optimization 可显式显示 step size 与 training time；
- 不需对整个 class 取 supremum。

### 6.2 缺口

- global Lipschitz/smoothness/convexity 可能不适合深网；
- parameter distance 小不是 loss stability；
- randomized algorithm 需要 seed/coupling quantifier；
- gap 小仍可能有
  $$
  \widehat R_S(A(S))\approx R(A(S))\approx0.9.
  $$

稳定性证明“train 与 population 接近”，不单独证明“二者都低”。

## 七、Compression 路线：控制可重构描述

realizable exact-size-\(k\) sample compression 的原型：

$$
\mathbb P(R(h_S)>\varepsilon)
\le
2^b{m\choose k}(1-\varepsilon)^{m-k}.
$$

复杂度来自：

$$
\log{m\choose k}+b\log2.
$$

### 7.1 优势

- 与少量 support/prototype/witness 有直接解释；
- 无需控制整个 class；
- description counting 与 generalization proof 紧密连接。

### 7.2 缺口

- 必须有 fixed decoder；
- reconstruction 要满足 theorem 需要的 full-sample consistency/approximation；
- continuous side values 与 learned representation 必须计入；
- model-file compression 不自动是 sample compression；
- agnostic/lossy setting 需要另一套 theorem。

## 八、PAC-Bayes 路线：控制 Posterior 相对 Prior 的改变

PAC-Bayes-kl 原型：

$$
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le
\frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}m
$$

同时对所有 \(Q\) 成立。

### 8.1 优势

- posterior 可以依赖 data；
- complexity 是 local/distributional，而非整个 class；
- 可把 independent pretraining 变成 informative prior；
- bound 本身可优化；
- 离散 point posterior 恢复 weighted Occam。

### 8.2 缺口

- prior 必须合法；
- direct object 是 Gibbs predictor；
- continuous deterministic point mass 常 infinite KL；
- parameter-space KL 对 symmetry/scale 敏感；
- empirical Gibbs risk 常需 Monte Carlo confidence；
- KL 小不保证 center network risk 小。

## 九、Information 路线：控制输出携带的样本信息

sub-Gaussian loss 下：

$$
\left|
\mathbb E[R(W)-\widehat R_S(W)]
\right|
\le
\sqrt{\frac{2\sigma^2I(S;W)}m}.
$$

### 9.1 优势

- 绑定 actual randomized channel；
- distribution-dependent；
- finite output、bit transcript、post-processing 与 adaptive chain rule 有自然接口；
- 揭示 data reuse/selection bias。

### 9.2 缺口

- 基础 guarantee 只是 expected signed gap；
- \(I(S;W)\) 需要整个 training distribution，难从单次 run 估计；
- deterministic continuous output 常 infinite；
- average dependence 不控制 worst-case adjacent-sample sensitivity；
- small MI 仍需 empirical risk 足够低才能得到 low population risk。

## 十、有限类：相似数量级，不同证明对象

设 \(|\mathcal H|=K\)。

### 10.1 Capacity

union bound/Hoeffding 给 complexity

$$
\log K.
$$

event uniform over all \(h\in\mathcal H\)。

### 10.2 Occam/Compression

为每个 \(h\) 编码，uniform code length 至少约

$$
\log_2K.
$$

证明按 descriptions 计数。

### 10.3 PAC-Bayes

取 uniform prior \(P(h)=1/K\) 与 point posterior \(\delta_h\)：

$$
\operatorname{KL}(\delta_h\|P)=\log K.
$$

### 10.4 Mutual Information

若 algorithm output \(W\in\mathcal H\)，则

$$
I(S;W)\le H(W)\le\log K.
$$

四者都出现 \(\log K\)，但：

- capacity 给 high-probability uniform control；
- Occam 依赖合法 code/decoder；
- PAC-Bayes 控制 Gibbs/point posterior 且依赖 prior；
- MI 基础式控制 expected signed algorithmic gap。

相同 numerator 不等于相同 theorem。

## 十一、稳定性与容量：Algorithm vs Class

考虑同一巨大 class \(\mathcal H\) 中两个 algorithms：

- \(A_1\)：strongly regularized convex ERM；
- \(A_2\)：能用一个样本点触发完全不同 predictor 的 lookup rule。

capacity bound 对两者相同，因为 class 相同。stability 可能：

$$
\beta_m(A_1)=O(1/m),
\qquad
\beta_m(A_2)=O(1).
$$

这显示 stability 可区分 optimization rule。

反过来，一个 unstable ERM 仍可能因 small VC dimension 获得 uniform guarantee。algorithm instability 不自动否定 class learnability。

## 十二、PAC-Bayes 与 Capacity：Local Distribution vs Supremum

capacity 典型控制：

$$
\sup_{h\in\mathcal H}G_S(h).
$$

PAC-Bayes 控制：

$$
\mathbb E_{h\sim Q}G_S(h)
$$

并用 \(\operatorname{KL}(Q\|P)\) 支付 \(Q\) 集中到哪些区域。

若 \(Q\) 只覆盖 class 中一个 small, robust basin，PAC-Bayes 可能绕过远处 bad hypotheses。但代价是：

- prior 要给该 basin 足够质量；
- sampled hypotheses 都要保持 low risk；
- certificate 针对 randomized mixture。

这不是“PAC-Bayes 永远比 VC 紧”，而是 quantifier changed。

## 十三、Compression、PAC-Bayes 与 Description Length

如果 hypothesis 有 prefix code length \(L(h)\)，可以设 prior

$$
P(h)\propto e^{-L(h)}
$$

（满足 Kraft-type normalization）。point posterior complexity 约为

$$
\operatorname{KL}(\delta_h\|P)
\approx L(h).
$$

若 learned object 由 \(k\) 个 sample indices 与 \(b\) side bits 重构，description length 约

$$
\log{m\choose k}+b\log2.
$$

它们的联系是真实的，但要防止三种偷换：

1. sample point 本身可能包含无限/大量 bits；
2. decoder/architecture/codebook 也可能 data-dependent；
3. lossy model compression 不满足 realizable sample-compression consistency。

## 十四、PAC-Bayes 与 Mutual Information

identity

$$
I(S;W)
=\mathbb E_S
\operatorname{KL}(P_{W\mid S}\|P_W)
$$

显示 marginal output law \(P_W\) 是 average reference。

PAC-Bayes 则使用一个可声明的 prior \(P\)：

$$
\operatorname{KL}(Q_S\|P).
$$

可以分解：

$$
\mathbb E_S\operatorname{KL}(P_{W\mid S}\|P)
=
I(S;W)+\operatorname{KL}(P_W\|P),
$$

只要 measures 与积分合法。

### 14.1 推导

写 density log ratio：

$$
\log\frac{dP_{W\mid S}}{dP}
=
\log\frac{dP_{W\mid S}}{dP_W}
+\log\frac{dP_W}{dP}.
$$

对 joint law 取 expectation：

- 第一项是 \(I(S;W)\)；
- 第二项只依赖 \(W\)，是 \(\operatorname{KL}(P_W\|P)\)。

这个 identity 说明 ideal marginal prior 最小化 average KL，但它不自动给可实现的 high-probability prior，因为 \(P_W\) 依赖未知 \(\mathcal D\) 与完整 algorithm law。

## 十五、Stability 与 Mutual Information 不可无条件互推

### 15.1 Stable 但 Infinite Information

sample mean

$$
W=\frac1m\sum_iZ_i
$$

对一个 bounded sample replacement 的敏感性是 \(O(1/m)\)，但若 \(Z_i\) 连续且 \(W\) deterministic，\(I(S;W)\) 通常 infinite。

### 15.2 Low Average Information 但 Worst-Case Unstable

算法可以在一个 data-law 下极低概率事件发生时泄露整个 sample，平时输出常数。average \(I(S;W)\) 可很小，但在该 rare neighboring sample 上 output 可剧烈变化。

所以：

- stability 是 worst-case adjacency style；
- mutual information 是 distribution-average dependence style。

要建立桥梁需额外 tail、privacy、noise 或 channel regularity。

## 十六、逻辑有效、Nonvacuous、Tight、解释充分

四个评价维度不可混为一谈。

### 16.1 Valid

所有 theorem assumptions 与 quantifiers 成立。

### 16.2 Nonvacuous

若 risk 本来在 \([0,1]\)，upper bound 小于 \(1\) 才至少提供新信息。

### 16.3 Tight

bound 与实际 risk/gap 的差距足够小，可用于模型比较或设计。

### 16.4 Explanatory

complexity 随现实 intervention 有正确趋势。例如：

- 增强 regularization 后 stability 改善；
- 加入 irrelevant parameters 不应让 function-level explanation 任意恶化；
- data leakage 应让 certificate 失效或付费；
- more training 在 unstable regime 不应被无条件奖励。

一个 theorem 可以 valid/nonvacuous，却未解释 observed phenomenon；也可以有漂亮 correlation，却没有有效 theorem。

## 十七、不能无修正地 Post-hoc 取最小 Bound

假设对每个 \(j\)，单独有

$$
\mathbb P(R\le B_j(S,\delta))\ge1-\delta.
$$

这不推出

$$
\mathbb P\left(
R\le\min_jB_j(S,\delta)
\right)\ge1-\delta.
$$

因为不同 \(B_j\) 的 failure events 可以不同，选择最小者本身依赖 \(S\)。

### 17.1 有限族修复

预声明 \(J\) 个 bounds，分配

$$
\delta_j>0,
\qquad
\sum_{j=1}^J\delta_j\le\delta.
$$

union bound 给：

$$
\mathbb P\left[
\forall j,\ R\le B_j(S,\delta_j)
\right]\ge1-\delta.
$$

此时训练后取

$$
\min_jB_j(S,\delta_j)
$$

才合法。

### 17.2 不同 Predictor 的问题

若每个 bound 控制不同 output \(h_j\)，取最小 bound 同时也在选择 predictor。必须确保：

- 所有 predictor 的 events simultaneous；
- empirical risks 使用同一合法 data；
- deployed predictor 正是被选者；
- selection protocol 没额外看 test data。

## 十八、选型决策树

### 18.1 第一问：需要 Uniform ERM Guarantee 吗

若算法未定、要比较整个 class 或证明 learnability：

- finite class / VC / Rademacher / covering；
- 若 global class 太大，尝试 norm、margin、localization。

### 18.2 第二问：实际 Algorithm 可分析邻接敏感性吗

若是 convex regularized ERM、contractive iterations 或受控 SGD：

- stability 优先；
- 明确 replacement unit、loss range、randomness coupling。

### 18.3 第三问：输出有明确短重构描述吗

若有 support set、prototype、decision tree、quantized code：

- sample compression 或 description-length/Occam；
- 计入 decoder、side bits、architecture 与 learned representation。

### 18.4 第四问：可部署 Randomized Predictor 吗

若能构造独立 prior 与 noisy posterior，并计算 Gibbs risk/KL：

- PAC-Bayes；
- 保持 prior legality 与 Monte Carlo confidence。

### 18.5 第五问：Algorithm Channel/Transcript 可控吗

若关注 adaptive model selection、有限输出、隐私或 noisy channel：

- mutual information/related information measures；
- 明确 expectation vs high probability。

多个答案都为“是”时，可以并行构造证书，但最终选择要预声明置信预算。

## 十九、模型—证书匹配矩阵

| 场景 | 首选入口 | 原因 | 主要风险 |
|---|---|---|---|
| strongly convex regularized linear model | stability | 曲率直接控制 replacement sensitivity | loss/Lipschitz constants |
| norm-bounded linear predictor | Rademacher/margin | 可解析 class complexity | norm/data scale 选择 |
| hard-margin support-vector reconstruction | compression + margin | 少量 support 与 geometric margin | soft/noisy case、coefficients |
| stochastic neural ensemble | PAC-Bayes | posterior distribution 与 KL 可优化 | prior legality、Gibbs mismatch |
| quantized finite model release | description length / MI | bit budget 明确 | training-dependent decoder/transcript |
| adaptive hyperparameter search | MI / reusable validation | selection transcript 是核心 | expected vs tail guarantee |
| giant deterministic deep net | norm/margin、compression、stability、PAC-Bayes 均需试验 | 没有单一普适路线 | assumptions/vacuity/invariance |

## 二十、一个统一数值模板

对所有 candidate certificates，报告：

| 字段 | 值 |
|---|---|
| population target | distribution、task、sample unit |
| empirical loss | value、range、estimator |
| output object | \(h,A,Q,W\) 或 transcript |
| complexity | numerical value 与单位 |
| sample size | effective \(m\) |
| confidence | \(\delta\) 与所有预算拆分 |
| resulting bound | risk/gap、expectation/high probability |
| validity audit | assumptions pass/fail |
| nonvacuity | 与 trivial range 比较 |
| reproducibility | data/code/seed/hash |

只有在 output 与 guarantee type 一致时，才把 bounds 放到同一图表。

## 二十一、Deep Learning 的边界

现代深网可能同时表现出：

- huge worst-case capacity；
- interpolation；
- optimizer-dependent implicit bias；
- augmentation/data dependence；
- pretrained representation；
- stochastic training；
- scale/permutation symmetry；
- memorization 与 benign overfitting。

因此一个完整解释往往需要多层证据：

1. valid theorem under declared regime；
2. computed nonvacuous certificate；
3. intervention：改变 width、noise、margin、data size 后 prediction；
4. counterexample：该 metric 是否能被 reparameterization 操纵；
5. empirical reproduction；
6. open boundary：哪些现象仍未解释。

“某个 bound 与 test error correlation 很高”是实验证据，不自动是因果或 distribution-free theorem。

## 二十二、常见误区

> [!warning] 误区 1：复杂度项越小，theory 就越好
> 先检查它控制什么 predictor、什么 risk、什么 probability。

> [!warning] 误区 2：algorithm-dependent bound 必然比 class bound 紧
> 具体稳定性/KL/MI 可能很大或不可算；没有支配关系。

> [!warning] 误区 3：五个 bounds 都 valid，所以可直接报告最小者
> 若 events 未同时化，post-hoc minimum 破坏 confidence。

> [!warning] 误区 4：vacuous bound 等于 theorem 被证伪
> 它只说明当前 complexity/sample size 没给有用数值。

> [!warning] 误区 5：一个 certificate 足以解释所有深网泛化
> optimization、representation、data geometry 与 distribution shift 可能不在该 theorem 的对象内。

## 二十三、综合验收清单

1. 五元对象 \((S,A,\ell,R,\text{output})\) 是否写全？
2. complexity 控制 class、algorithm、description、posterior 还是 channel？
3. quantifier 是 supremum、neighbor、all \(Q\) 还是 expectation？
4. guarantee 是 risk 还是 generalization gap？
5. confidence over 什么 randomness？
6. empirical term 与 population term 是否对应同一 predictor？
7. data-dependent choices 是否在 event 内或已付 selection cost？
8. 数值是否 nonvacuous？
9. metric 是否受 parameterization/symmetry 操纵？
10. deployment 与 certificate object 是否一致？
11. 是否有 counterexample 与 intervention？
12. 是否诚实声明未覆盖的 regime？

## 二十四、小结

五类证书的最短记忆法：

- 容量：整个 class 能随数据变化多少；
- 稳定性：具体 algorithm 遇到一个样本替换会变化多少；
- 压缩：输出能否由短而合法的描述重构；
- PAC-Bayes：data-dependent posterior 离 data-independent prior 多远；
- mutual information：输出平均携带多少训练样本信息。

它们共享一个核心思想：自适应选择必须付复杂度。但复杂度的对象、量词与保证不同。严谨的选型顺序是：

1. 对齐概率合同；
2. 选择与机制相匹配的 certificate；
3. 验证 theorem assumptions；
4. 计算并检查 nonvacuity；
5. 为 multi-bound/model selection 分配置信预算；
6. 区分 certificate、经验相关和完整科学解释。

## 来源与延伸

- [[算法稳定性与替换一个样本]]、[[样本压缩方案与泛化]]：algorithm/description 两条主线；
- [[PAC-Bayes Bound 的测度变换主线]]、[[PAC-Bayes 先验、后验与数据依赖边界]]：posterior certificate；
- [[互信息与信息论泛化界]]：sample–output channel；
- [[VC 一致收敛与泛化界]]、[[Rademacher 复杂度与经验复杂度]]：uniform capacity；
- [[深度泛化证据地图与开放问题]]：后续 deep-learning 证据分层。
