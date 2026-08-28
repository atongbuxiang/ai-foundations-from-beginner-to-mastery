---
type: solution
status: draft
area: [learning-theory/transfer-learning, linear-probe, fine-tuning, evaluation]
topic: "[[Linear Probe、Fine-Tuning 与迁移评估]]"
exercise: "[[习题 - Linear Probe、Fine-Tuning 与迁移评估]]"
prerequisites: ["[[Linear Probe、Fine-Tuning 与迁移评估]]"]
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - Linear Probe、Fine-Tuning 与迁移评估

> [!warning] 解题原则
> 先命名 estimand：oracle head、finite trained head，还是初始化依赖的 adaptation algorithm。任何 accuracy 都必须绑定 layer、labels、head、compute、selection 与 split。

## A. 识别与复述

### LT-TRN-A01

oracle linear risk：

$$
R_{\rm lin}^*(h)=\inf_{W,b}E\ell(Wh(X)+b,Y),
$$

随机性仅来自 population law（对象本身可确定）。finite probe 把 $S_n$、head初始化/optimizer seed、label subsample与hyperparameter selection都纳入 $E R(\mathcal A_{\rm probe}(h,S_n))$。fine-tuning 还包含pretraining checkpoint/seed、全部或部分参数更新、schedule、budget与nonconvex path。三者不能共用一个“表示分数”名称。

### LT-TRN-A02

zero-shot不更新或只选prompt，测pretrained interface但混杂template/calibration；kNN不更新，测chosen metric geometry但混杂normalization/gallery；linear只更新head，测linear accessibility；partial更新top blocks/adapter，测局部adaptability且依赖cut/rank；full更新全部，测initialization+algorithm；scratch同架构随机初始化，是数据/架构/预算baseline。每类必须有独立protocol card。

### LT-TRN-A03

三句均错误。低 linear score只说明在该head与训练程序下不易线性读出，XOR可保留全部信息；高fine-tune可能来自好的优化初始化，即使frozen geometry差；upstream与transfer关系依赖task distance、training regularization、architecture和protocol，单一相关性不能外推所有任务。

## B. 手算与局部推导

### LT-TRN-B01

一种概念分解：

$$
R(\widehat g\circ h)-R_{\rm raw}^*
=
\underbrace{R_{\rm lin}^*(h)-R_{\rm raw}^*}_{\text{representation/head approximation}}
+
\underbrace{R(g_{S_n}^*\circ h)-R_{\rm lin}^*(h)}_{\text{finite-label estimation}}
+
\underbrace{R(\widehat g\circ h)-R(g_{S_n}^*\circ h)}_{\text{optimization}}
+
\text{selection optimism}.
$$

增加labels主要降estimation；更多steps/更好solver降optimization；richer head可降approximation但增estimation和selection；独立validation/outer test控制selection，不能靠更多test reuse解决。

### LT-TRN-B02

四点为 $(1,1),(-1,-1)$ 属于 $Y=1$，$(1,-1),(-1,1)$ 属于 $Y=-1$。若 affine score $s=w_1x_1+w_2x_2+b$ 正确分类全部，则正类两式相加给 $2b>0$，故 $b>0$；负类要求 score $<0$，两式相加又给 $2b<0$，矛盾，因此不可全分。含 bias 的直线可以单独切出一个角，并把其余三点预测为另一类，从而正确3/4；结合不可全分，最佳 error 为 $1/4$。

若限制 $b=0$，对偶点 $x,-x$ 的 score 异号，但它们有相同 XOR label，因此每一对必错一个，最佳 error 为 $1/2$。加入第三维 $x_1x_2$ 后取 score 为第三维即可零错误。结论说明 bias 项属于 probe class 定义，不能省略。

### LT-TRN-B03

定义 gain $\Delta=R_{\rm scratch}-R_{\rm pre}$：

$$
(0.35-0.20,\;0.20-0.15,\;0.12-0.12)
=(0.15,0.05,0).
$$

低预算优势大、预算增加后归零，主要证据是 optimization/sample-efficiency speedup，而不是 persistent asymptotic gain。仍需置信区间和更大预算确认最后的0不是noise。

## C. 证明与反例

### LT-TRN-C01

若 $h_2=Ah_1$、$A$ 可逆，对任意 head $(W,b)$，令 $W'=WA^{-1}$，则

$$
W'h_2(x)+b=WA^{-1}Ah_1(x)+b=Wh_1(x)+b.
$$

两类可实现predictor集合相同，oracle risk相同。一般 nonlinear可逆 $\phi$ 的 $W\phi(z)+b$ 不能总写成 $\widetilde Wz+\widetilde b$，它可弯曲/拉直decision boundary，因此不保持linear-head class。

### LT-TRN-C02

构造：A直接输出one-hot source categories，与target高度相关，linear probe高；但其高层saturated、错误invariance删除fine-grained factor，full fine-tune在小数据/有限steps中难恢复。B输出保留局部结构的非线性code，linear head不易读，却未删除target factor，且parameter basin对适配友好，full fine-tune更好。排序测的是不同estimands：A有linear accessibility，B有adaptability；无矛盾。

### LT-TRN-C03

设每个候选的test estimate为真实值 $\mu_k$ 加零均值噪声 $\epsilon_k$。即使所有 $\mu_k=\mu$，

$$
E\max_{k\le KM}(\mu+\epsilon_k)
=
\mu+E\max_k\epsilon_k
>\mu
$$

（非退化噪声下）。正确数据流：train拟合每个layer/regularization；inner validation只选择组合；选择规则锁定后在未看的outer test评一次。若还选择pretraining方法，需再嵌套或使用独立final benchmark。

## D. 审计与诊断

### LT-TRN-D01

矩阵至少覆盖tasks（classification/localization等）、protocols、label budgets、in/temporal/subgroup/OOD shifts、FLOPs/steps与pretrain/probe seeds。可随机化label subsample、seed、task order；必须预注册task权重、outer splits、metrics、预算grid、layer/head search space与stop rule。只在validation上选择，test一次性评估；报告平均、worst/quantile与negative-transfer count。

### LT-TRN-D02

同split上的难度冲击同时影响两模型，paired difference $D_i=L_{Ai}-L_{Bi}$ 消去共同变异，方差

$$
\operatorname{Var}(D)=\operatorname{Var}(A)+\operatorname{Var}(B)-2\operatorname{Cov}(A,B)
$$

通常小于独立差。先在每task内用相同split/label/seed计算paired CI，再把task作为高层单位做equal-weight或预注册$\Pi$加权的hierarchical bootstrap；不能把所有examples跨task混成iid。

### LT-TRN-D03

A更新全网、B只更新head，estimand不同；100 epochs的per-step FLOPs、trainable params与memory不同；A/B可能有不同augmentation、BN mode、resolution；search space、early stopping和checkpoint次数不同；full与linear对label capacity和overfit不同。公平报告应在同一protocol内比较encoders，并另作protocol ladder；若跨protocol比较，只能说whole pipelines在披露预算下的风险不同。

## E. 研究与迁移

### LT-TRN-E01

tasks覆盖image classification、box/keypoint localization、semantic/instance segmentation、OCR、pose；每个有identity/group/time split与metric。protocol含frozen kNN/linear、task-specific shallow head、fixed-rank adapter、full tune、same-architecture scratch；label budgets对数grid。shift含resolution、lighting、rotation、new domain与rare subgroup。统一data preprocessing并披露task-specific必要变换，按FLOPs/search预算对齐；汇总平均、worst-task、low-shot AUC与negative transfer。

### LT-TRN-E02

固定checkpoint/layer/token position与文本split；probe ladder从linear到小MLP，限制参数量/steps并有random/untrained representation baseline。防memorization用lexical/template/identity-held-out splits；属性标签不能从prompt表面泄漏。probe可读性后再做activation intervention、counterfactual pair与causal mediation，但只对明确定义干预解释。多个layers×attributes×positions需inner selection与multiple-testing/FDR或独立outer确认。

### LT-TRN-E03

claim card包括model/data cutoff、task family、protocol matrix、label/compute/search、outer splits、uncertainty、calibration/latency与failed tasks。最强允许结论形如：“在预注册的任务权重、预算和shift下，该pipeline的paired risk低于baseline多少。”必须报告negative-transfer任务与scratch比较。明确拒绝：“普遍最好表示”“包含因果语义”“所有模态安全”“linear probe证明信息存在/不存在”等超出证据的结论。
