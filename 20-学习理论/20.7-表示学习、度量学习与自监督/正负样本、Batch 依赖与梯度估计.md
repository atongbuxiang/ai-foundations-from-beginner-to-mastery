---
type: theorem
status: draft
area: [learning-theory/contrastive-learning, batch-dependence, negative-sampling, gradient-estimation]
aliases: [Contrastive Batch Dependence, False Negatives and Gradient, In-Batch Negative Sampling]
node_id: LT-56
prerequisites: ["[[对比学习、InfoNCE 与密度比]]", "[[随机梯度与小批量估计]]", "[[训练集、验证集、测试集与自适应复用]]", "[[度量学习、相似性与检索风险]]"]
related: ["[[数据增强、不变性、等变性与任务充分性]]", "[[表示坍缩、非坍缩与可辨识边界]]", "[[随机、对抗与自适应序列的区别]]"]
sources: ["[[S-2020-Chen-SimCLR]]", "[[S-2020-Chuang-Debiased-Contrastive]]", "[[S-2019-Saunshi-Contrastive-Theory]]", "[[S-2018-Oord-Li-Vinyals-CPC]]", "[[S-2015-Schroff-Kalenichenko-Philbin-FaceNet]]"]
exercises: ["[[习题 - 正负样本、Batch 依赖与梯度估计]]"]
solutions: ["[[解答 - 正负样本、Batch 依赖与梯度估计]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-batch-negative-gradient-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 正负样本、Batch 依赖与梯度估计

> [!abstract] 本章主问题
> ordinary ERM中的mini-batch常被视为固定single-example risk的Monte Carlo estimator。in-batch contrastive learning不同：每个anchor的loss显式依赖同一batch其他items，batch定义candidate set、negative distribution、class collision与gradient weights。
>
> 对logits $u_k=s(z_i,z_k)/\tau$，
>
> $$
> \ell_i
> =
> -u_{j(i)}+\log\sum_{k\in\mathcal A(i)}e^{u_k},
> $$
>
> 梯度为
>
> $$
> \boxed{
> \frac{\partial\ell_i}{\partial u_k}
> =
> p_{ik}-\mathbf1\{k=j(i)\}.
> }
> $$
>
> 因此small temperature、hard negatives、false negatives、all-gather、memory bank与mask都直接改变学习信号，而不只是gradient variance。

> [!question] 初学者读完必须能回答
> 1. 为什么batch size在contrastive learning中可能改变objective？
> 2. softmax gradient怎样给hard candidates更大权重？
> 3. false negative collision probability怎样计算？
> 4. random、hard、debiased与importance-corrected sampling区别是什么？
> 5. memory bank staleness与distributed all-gather改变了什么？
> 6. user/time/group dependence为何既影响loss又影响evaluation？

## 一、学习目标

1. 写出two-view in-batch construction；
2. 明确eligible denominator与mask；
3. 推导logit与embedding gradient；
4. 解释temperature对gradient concentration的作用；
5. 推导latent-class false-negative概率；
6. 区分objective change、estimator bias与variance；
7. 分析hard mining与false negatives的冲突；
8. 审计memory bank、momentum encoder与distributed gather；
9. 处理group/time/sequence dependence；
10. 设计可复现sampler与outer evaluation。

## 二、Two-View Batch Contract

先抽 $B$ 个source units：

$$
U_1,\ldots,U_B.
$$

对每个unit独立或按声明coupling生成two views：

$$
X_{2b-1}=A_{b,1}(U_b),
\qquad
X_{2b}=A_{b,2}(U_b).
$$

编码并normalize：

$$
z_i
=
\frac{h_\theta(X_i)}{\|h_\theta(X_i)\|}.
$$

对anchor $i$，其paired positive index记为 $j(i)$。eligible candidates $\mathcal A(i)$ 通常包含除自己外的其他 $2B-1$ views，但实现可能排除：

- same-source extra views；
- same-user/group items；
- known positives；
- padding或duplicate；
- local-rank-only candidates。

mask是统计method definition。

## 三、NT-Xent Loss

similarity logit：

$$
u_{ik}
=
\frac{z_i^Tz_k}{\tau}.
$$

anchor loss：

$$
\boxed{
\ell_i
=
-\log
\frac{e^{u_{i,j(i)}}}
{\sum_{k\in\mathcal A(i)}e^{u_{ik}}}.
}
$$

batch loss常取

$$
\widehat L_B
=
\frac1{2B}\sum_{i=1}^{2B}\ell_i.
$$

必须声明sum/mean、是否两向对称、positive是否进入denominator、stop-gradient与cross-device aggregation。

## 四、Softmax Gradient 推导

令

$$
p_{ik}
=
\frac{e^{u_{ik}}}{\sum_{r\in\mathcal A(i)}e^{u_{ir}}}.
$$

则

$$
\ell_i
=
-u_{i,j(i)}
+
\log\sum_re^{u_{ir}}.
$$

对任意eligible $k$：

$$
\frac{\partial\ell_i}{\partial u_{ik}}
=
-\mathbf1\{k=j(i)\}+p_{ik}.
$$

所以：

- positive gradient为 $p_{i,j}-1<0$，gradient descent提高positive logit；
- negative gradient为 $p_{ik}>0$，gradient descent降低negative logit；
- 当前logit越大，$p_{ik}$越大，candidate获得更强push。

这就是softmax内部的automatic hard-negative weighting。

## 五、Embedding Gradient

忽略normalization Jacobian，若 $u_{ik}=z_i^Tz_k/\tau$，则

$$
\frac{\partial\ell_i}{\partial z_i}
=
\frac1\tau
\left(
\sum_{k\in\mathcal A(i)}p_{ik}z_k
-
z_{j(i)}
\right).
$$

它把anchor拉向positive，并推离softmax-weighted candidate average。

实际normalized embedding还需chain rule通过

$$
z=\frac{v}{\|v\|}
$$

其Jacobian把gradient投影到sphere tangent并按 $1/\|v\|$ 缩放。

## 六、Temperature 改变什么

$$
p_{ik}
=
\operatorname{softmax}(s_{ik}/\tau).
$$

- small $\tau$：probability集中到最大similarity candidates，hard items主导，gradient scale含 $1/\tau$；
- large $\tau$：weights更平，hard/easy差异减弱。

temperature不是只做post-hoc calibration；它改变training geometry、effective hardness与numerical stability。

## 七、手算一个 Batch

某anchor有一个positive与两个negatives，logits（已除temperature）为

$$
u=(2,1,0),
$$

positive是第一项。normalizer：

$$
Z=e^2+e+1\approx11.107.
$$

probabilities：

$$
p\approx(0.665,0.245,0.090).
$$

loss：

$$
\ell=-\log0.665\approx0.408.
$$

logit gradients：

$$
\nabla_u\ell
\approx
(-0.335,0.245,0.090).
$$

更相似的negative得到更大push。

## 八、Batch Size 不只改变 Variance

若每个anchor有 $K-1$ negatives，改变 $B$ 通常改变 $K$。这会同时改变：

1. candidate classification difficulty；
2. InfoNCE lower-bound ceiling $\log K$；
3. log-sum-exp denominator distribution；
4. 遇到hard/false negative的概率；
5. gradient direction与magnitude；
6. compute与communication；
7. batch normalization statistics。

因此不同batch size的loss数值通常不是同一fixed per-example objective的简单低/高variance estimate。

## 九、Latent-Class False Negatives

假设每个unit有latent class $C\in\{1,\ldots,m\}$，class prior $\pi_c$。anchor class为 $c$，一个marginal negative与anchor同class概率为

$$
P(C^-=c\mid C=c)=\pi_c.
$$

若有 $K-1$ iid negatives，至少一个same-class collision概率：

$$
\boxed{
1-(1-\pi_c)^{K-1}.
}
$$

对random anchor平均single-negative collision：

$$
P(C^-=C)
=
\sum_c\pi_c^2.
$$

### 9.1 数值例子

balanced 10 classes，$\pi_c=0.1$，63个negatives：

$$
1-0.9^{63}
\approx
0.9987.
$$

几乎必有same-class item。但same class是否真应视为positive仍由task定义；latent-class model只是一种解释。

## 十、False Negative 不是普通 Noise

若same-semantic items被push apart，population objective本身改变。其后果可能是：

- class cluster被撕裂；
- instance discrimination增强但class sufficiency下降；
- frequent classes受更多collision；
- minority class/near duplicate梯度被放大；
- hard mining进一步聚焦false negatives。

这不是简单zero-mean gradient noise。

## 十一、Debiasing 的条件

若negative marginal可写为

$$
p_Y
=
\tau^+p_Y^+
+
(1-\tau^+)p_Y^-,
$$

其中 $p_Y^+$ 是same-class、$p_Y^-$ 是true-negative，理论上可在已知/估计 $\tau^+$ 下从mixture expectation校正true-negative term。

但需要：

- latent-class mixture模型正确；
- class prior/collision rate可用；
- positive/negative conditional laws稳定；
- clipping保持numerical合法；
- correction variance可控。

debiased objective不是assumption-free repair。

## 十二、Hard Negative Sampling

若从proposal

$$
q_\beta(y\mid x)
\propto
p_Y(y)\exp(\beta s(x,y))
$$

抽negatives，$\beta$控制hardness。它能提高nontrivial gradients，但optimal score针对的新contrast distribution也改变。

若目标仍是原 $p_Y$ expectation，可尝试importance weighting：

$$
w(x,y)=\frac{p_Y(y)}{q_\beta(y\mid x)}.
$$

但self-normalization、unknown normalizer与large weights引入bias/variance。production中常选择直接承认新training objective并用outer task评价。

## 十三、Dependent Batch

iid unit assumption会被以下情况破坏：

- 同一user多条records；
- 同一document的chunks；
- 相邻video/audio frames；
- repeated patient/site；
- distributed sampler重复样本；
- curriculum按difficulty成组。

依赖会同时改变：

- effective negative law；
- collision/duplicate probability；
- variance与effective sample size；
- train/test leakage。

先按independent group/time unit抽sample，再在unit内生成views，通常比先随机row shuffle更合法。

## 十四、Memory Bank 与 Momentum Encoder

memory bank扩展candidate set，但stored embedding由旧parameters产生：

$$
z_k^{\rm bank}
=
h_{\theta_{t-\Delta_k}}(x_k).
$$

当前anchor用 $\theta_t$，所以score混合不同encoders。staleness可能提供large dictionary，也引入moving-target bias。

momentum encoder用

$$
\bar\theta_t
=
m\bar\theta_{t-1}+(1-m)\theta_t
$$

平滑key encoder。它改变computational graph：keys是否stop-gradient、queue何时更新都需声明。

## 十五、Distributed All-Gather

若每张device local batch为 $B_{\rm local}$，$R$ 个replicas all-gather后candidate数约乘 $R$。必须审计：

- gradients是否穿过remote embeddings；
- duplicate sampler seeds；
- cross-replica positive index；
- global loss是sum还是mean；
- communication failure/uneven last batch；
- BatchNorm是否local或synchronized。

相同learning rate在不同global denominator下未必保持相同effective update。

## 十六、图：Batch 同时定义目标与梯度

先看图回答：为什么“更多negative通常有用”与“更多negative增加false-negative exposure”可以同时为真？

![[00-知识库管理/_assets/figures/learning-theory/fig-batch-negative-gradient-v2.svg|900]]

> [!figure] 图 20.7-04　in-batch候选、softmax梯度与negative failure modes
> 左栏把source-unit sampling、positive pairing与denominator eligibility分开；中栏用 $p_k-\mathbf1\{k=+\}$ 展示hard candidates如何获得更大gradient；右栏区分false、dependent与stale negatives。来源：依据 SimCLR、Chuang et al.、Saunshi et al.、CPC与FaceNet独立绘制；确定性 SVG，由 [[plot_representation_contrastive_v2.py]] 生成。

**怎样读图**：batch size、temperature与sampler共同决定softmax competition；如果negative law变了，gradient expectation与density-ratio解释也随之改变。

**图没有证明什么**：它没有证明所有same-class samples都应为positives，也没有证明debiasing或hard mining在任意representation/data distribution下改善downstream risk。

## 十七、Gradient Estimator Ledger

应分别问：

1. target population objective是什么？
2. batch estimator对它unbiased吗？
3. within-batch terms相关吗？
4. encoder-dependent sampler是否需要score-function/pathwise correction？
5. memory bank是否stale？
6. distributed aggregation是否改变scale？
7. selection是否反复使用validation？

“SGD无偏”不能只因代码调用mini-batch就成立。

## 十八、AI 场景

### 18.1 Sentence Embeddings

同document sentences可能被当negatives，却共享topic；random row split还会把near duplicates跨test泄漏。

### 18.2 Multilingual/Multimodal

不同language captions可描述同一content；false-negative rate随dataset重复与translation clusters变化。

### 18.3 Recommender Retrieval

in-batch negatives受exposure/logging policy影响；unseen item不是用户真正不喜欢。应区分unobserved与negative feedback。

### 18.4 Code Retrieval

不同implementations可语义等价；exact-string/仓库duplicate filtering决定false negatives与test leakage。

## 十九、审计清单

- [ ] source unit与two-view law；
- [ ] eligible denominator、mask与positive indexing；
- [ ] local/global batch size与all-gather；
- [ ] similarity、normalization、temperature；
- [ ] sum/mean与learning-rate scale；
- [ ] hard/debiased sampler及target law；
- [ ] group/time/identity collision；
- [ ] queue size、age与momentum；
- [ ] stop-gradient graph；
- [ ] downstream outer split、subgroup与shift。

## 二十、常见错误

1. 把batch size只当variance knob；
2. 不记录denominator mask；
3. 把所有other examples称true negatives；
4. hard mining后仍引用marginal-negative theorem；
5. 忽略temperature的 $1/\tau$ gradient scale；
6. memory bank使用旧encoder却当iid current samples；
7. all-gather后loss/learning rate scale不审计；
8. 用row shuffle处理user/time dependence；
9. 用training collision correction自证semantic truth；
10. 把loss下降等同downstream risk下降。

## 二十一、最小记忆

1. **in-batch contrastive loss显式依赖其他batch items。**
2. **logit gradient是 $p_k-1\{k=+\}$。**
3. **small temperature和hard mining把gradient集中到最相似candidates。**
4. **same-class collision概率随class prior与negative count增长。**
5. **false、dependent、stale negatives是三种不同问题。**
6. **sampler、mask、queue与all-gather都是统计方法的一部分。**

## 二十二、掌握标准

- [ ] 能写two-view NT-Xent；
- [ ] 能手推logit与embedding gradient；
- [ ] 能计算collision probability；
- [ ] 能区分objective change/bias/variance；
- [ ] 能审计hard/debiased sampling；
- [ ] 能解释memory staleness与distributed candidates；
- [ ] 能设计group-aware sampler；
- [ ] 能写完整contrastive reproducibility contract。

## 二十三、练习与独立详解

- 练习：[[习题 - 正负样本、Batch 依赖与梯度估计]]
- 独立详解：[[解答 - 正负样本、Batch 依赖与梯度估计]]

## 参考来源

- [[S-2020-Chen-SimCLR]]
- [[S-2020-Chuang-Debiased-Contrastive]]
- [[S-2019-Saunshi-Contrastive-Theory]]
- [[S-2018-Oord-Li-Vinyals-CPC]]
- [[S-2015-Schroff-Kalenichenko-Philbin-FaceNet]]
