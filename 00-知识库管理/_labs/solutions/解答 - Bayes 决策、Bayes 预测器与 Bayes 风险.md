---
type: solution
status: draft
area: [learning-theory/foundations, statistical-decision-theory]
topic: "[[Bayes 决策、Bayes 预测器与 Bayes 风险]]"
exercise: "[[习题 - Bayes 决策、Bayes 预测器与 Bayes 风险]]"
prerequisites: ["[[条件概率、全概率与 Bayes 公式]]", "[[期望、方差与矩]]"]
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[逻辑回归、复合损失与概率分类]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - Bayes 决策、Bayes 预测器与 Bayes 风险

> [!warning] 使用边界
> Bayes rule 是“真实 conditional law 已知”的 oracle。实际系统还要估计 posterior、处理 shift、满足全局约束，并验证 loss 是否代表现实代价。

## A. 识别与复述

### LT-BAY-A01

$$
r(a\mid x)=\mathbb E[\ell(a,Y)\mid X=x]
$$

依 conditional law、action 与 loss。Bayes rule

$$
h^*(x)\in\arg\min_a r(a\mid x)
$$

还依 observation $X$ 的定义。Bayes risk

$$
R^*=\mathbb E_X\min_a r(a\mid X)
$$

依完整 $P$、$\mathcal X,\mathcal A,\ell$。改变 observation/action/loss/population 都可能改变它。

### LT-BAY-A02

Bayes classifier 用真实 $P(Y\mid X)$ 最小化分类风险；Bayesian posterior 是给定 prior/likelihood 后的 $p(\theta\mid S)$；posterior predictive 对参数后验积分得到 $p(y\mid x,S)$；MAP 是 posterior density 的 mode。Bayes classifier 是 decision-theoretic oracle，不要求参数 prior；MAP 是参数估计规则，也不等于任意 task loss 的最优动作。

### LT-BAY-A03

- 二分类 0–1：$\mathbf1\{\eta(x)\ge1/2\}$；
- 多分类 0–1：$\arg\max_kP(Y=k\mid x)$；
- 平方：$\mathbb E[Y\mid x]$；
- 绝对：任意 conditional median；
- log：完整真实 conditional distribution $P(Y=\cdot\mid x)$。

## B. 手算与构造

### LT-BAY-B01

普通 0–1：

$$
r(0\mid x)=0.3,\qquad r(1\mid x)=0.7,
$$

故预测 0。成本敏感：

$$
r(0\mid x)=8(0.3)=2.4,
$$

$$
r(1\mid x)=2(0.7)=1.4,
$$

故预测 1。等价阈值是 $2/(2+8)=0.2$，而 $0.3>0.2$。

### LT-BAY-B02

$c=0.2$ 时：

- $\eta=0.1$：$r(0)=0.1,r(\bot)=0.2,r(1)=0.9$，选 0，风险 0.1；
- $\eta=0.35$：三者为 $0.35,0.2,0.65$，拒绝，风险 0.2；
- $\eta=0.85$：三者为 $0.85,0.2,0.15$，选 1，风险 0.15。

### LT-BAY-B03

0–1 Bayes action 是第 2 类，条件风险

$$
1-0.5=0.5.
$$

$q_1=p$ 的 log risk 是 entropy：

$$
H(p)
=-[0.2\ln0.2+0.5\ln0.5+0.3\ln0.3]
\approx1.029653.
$$

$q_2$ 的 cross-entropy：

$$
-\left[0.2\ln0.1+0.5\ln0.7+0.3\ln0.2\right]
\approx1.121686.
$$

差值

$$
1.121686-1.029653\approx0.092033
=\operatorname{KL}(p\|q_2).
$$

## C. 推导与证明

### LT-BAY-C01

对任意 $h$，条件最优给

$$
r(h^*(x)\mid x)\le r(h(x)\mid x)\quad P_X\text{-a.s.}
$$

利用 tower property：

$$
R_P(h^*)=\mathbb E_Xr(h^*(X)\mid X)
\le\mathbb E_Xr(h(X)\mid X)=R_P(h).
$$

还需 $h^*$ 可测、风险可积；有限 action 空间中通常可通过固定 tie-breaking 满足。

### LT-BAY-C02

令 $\mu(X)=\mathbb E[Y\mid X]$：

$$
Y-a=(Y-\mu)+(\mu-a).
$$

平方并条件期望：

$$
\mathbb E[(Y-a)^2\mid X]
=\mathbb E[(Y-\mu)^2\mid X]
+(\mu-a)^2
+2(\mu-a)\mathbb E[Y-\mu\mid X].
$$

最后一项为 0，因此条件风险由 $a=\mu$ 最小化，最小值为 $\operatorname{Var}(Y\mid X)$。再对 $X$ 平均：

$$
R_2^*=\mathbb E\operatorname{Var}(Y\mid X).
$$

### LT-BAY-C03

$$
\begin{aligned}
-\sum_kp_k\log q_k
&=-\sum_kp_k\log p_k
+\sum_kp_k\log\frac{p_k}{q_k}\\
&=H(p)+\operatorname{KL}(p\|q).
\end{aligned}
$$

约定 $p_k=0$ 的项为 0；若 $p_k>0,q_k=0$，则 $-p_k\log q_k=+\infty$，KL 也为无穷。Gibbs inequality 给 KL 非负，且在 $p$ 支持上 $q=p$ 时取零。

## D. 边界、反例与纠错

### LT-BAY-D01

可用 kernel、nearest neighbors、logistic regression、boosting 或 neural network 估计 $\eta(x)$，这些方法不必给参数先验。如果估计 $\widehat\eta_m(x)$ 在适当意义下收敛到真实 $\eta(x)$，plug-in classifier $\mathbf1\{\widehat\eta_m\ge1/2\}$ 可趋近 Bayes risk。Bayes 指 decision optimum，不限定 inference philosophy。

### LT-BAY-D02

加入更有信息的检查 $W$ 后，Bayes risk 变为基于 $(X,W)$ 的条件风险，通常不高于只用 $X$；允许 abstain 增加 action，可降低给定成本下风险；改变 loss 会把 mode 换成 mean/median/threshold；population shift 改变 conditional law。它不是某个文件数据集的永恒常数，而是完整合同的函数。

### LT-BAY-D03

设模型每次都给预测类概率 0.99，但在 100 个样本中只正确 90 个，accuracy 为 90%。对所有“0.99 confidence”事件，真实正确频率却是 0.90，严重 overconfident。若 cost threshold 要求 posterior $>0.97$ 才自动批准，该模型会批准大量实际风险高于预期的案例。accuracy 只检查 argmax，不验证概率尺度。

## E. AI 迁移

### LT-BAY-E01

第一阶段在 training population 上估计 $q(Y=1\mid X)$，用独立 validation/calibration set 做 temperature/isotonic/conformal 等合适校准并按 subgroup 审计。第二阶段按 $c_{FN},c_{FP},c_{abstain}$ 求动作；灰区转人工。部署时监控 prevalence/conditional shift、coverage、selective risk 与 subgroup cost，而不只报 AUROC。

### LT-BAY-E02

token log loss 的 Bayes target 是语料生成过程的 $P(next\ token\mid context)$。最终系统 action 还包含 decoding/search、工具调用、拒答、对话记忆；帮助性 loss 涉及 factuality、instruction fulfillment、long-horizon utility；安全还涉及 forbidden action 与 uncertainty-aware abstention。较好 next-token KL 不自动优化这些 action-level costs。

### LT-BAY-E03

5% capacity 把个体决策耦合：不能对每个 $x$ 独立使用固定阈值而忽略总量。可解

$$
\max_{a_i\in\{0,1\}}
\sum_i a_i\,b(q_i)
\quad\text{s.t.}\quad
\sum_i a_i\le0.05n,
$$

其中 $b(q_i)$ 是复核的预期净收益。等价地按收益排序取 top 5%，或通过 Lagrange multiplier 产生由资源影子价格决定的阈值。还需审计 calibration、group constraints 与 temporal capacity。

