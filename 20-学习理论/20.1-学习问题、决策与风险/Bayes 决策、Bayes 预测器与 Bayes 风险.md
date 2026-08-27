---
type: concept
status: draft
area: [learning-theory/foundations, statistical-decision-theory, probability]
aliases: [Bayes Decision Rule, Bayes Predictor, Bayes Risk, 贝叶斯决策]
node_id: LT-06
prerequisites: ["[[损失、总体风险与经验风险]]", "[[条件概率、全概率与 Bayes 公式]]", "[[联合分布、边缘分布与独立性]]", "[[期望、方差与矩]]"]
related: ["[[经验风险最小化、近似 ERM 与超额风险分解]]", "[[可实现、不可知、相合性与可学习性]]", "[[Bayesian 推断与后验预测]]", "[[逻辑回归、复合损失与概率分类]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - Bayes 决策、Bayes 预测器与 Bayes 风险]]"]
solutions: ["[[解答 - Bayes 决策、Bayes 预测器与 Bayes 风险]]"]
created: 2026-08-20
updated: 2026-08-23
---

# Bayes 决策、Bayes 预测器与 Bayes 风险

> [!abstract] 本章主问题
> Bayes predictor 不是“使用了 Bayesian prior 的模型”，而是在真实联合分布 $P$ 已知时，对每个输入 $x$ 最小化条件风险的 oracle 决策规则；0–1、成本敏感、平方、绝对和 log loss 分别导出 posterior mode/阈值、条件均值、中位数与完整条件分布。Bayes risk 是当前 observation 与 loss 下不可再降低的风险，不等于所有现实不确定性的永恒下限。

> [!question] 初学者读完必须能回答
> 1. 总体风险怎样通过 tower property 化为逐点 conditional-risk minimization？
> 2. Bayes decision rule、Bayesian inference 与 MAP parameter estimation 有何区别？
> 3. 0–1、cost-sensitive、square、absolute 与 log loss 分别产生什么 Bayes action？
> 4. 为什么 observation、action space 或 loss 一变，Bayes risk 也会变？
> 5. Bayes risk、label noise、approximation error 与 estimation error 如何区分？
> 6. 已估计 posterior 后，为什么 calibration 与 downstream decision 仍要分账？

先用下图回答一个视觉问题：**同一个条件分布为什么会在不同损失下产生不同最优动作，Bayes risk 又为何只是相对于当前信息与任务的下界？**

![[00-知识库管理/_assets/figures/learning-theory/fig-bayes-conditional-risk-action-v2.svg|880]]

> [!figure] 图 20.1.6｜Conditional law、loss 与 Bayes action
> A 从 joint law 经 $P(Y\mid X=x)$ 形成 conditional risk $r(a\mid x)$，再逐点选择 $h^*(x)$；B 把 0–1/cost、square、absolute、log loss 分别映到 mode/threshold、mean、median 与 full conditional law；C 将 Bayes risk 的依赖拆为 observation、action space、loss 与未知 $P$。来源：独立绘制；理论接口参考 statistical decision theory 与 Bayes rules；生成脚本：[[plot_learning_problem_decision_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先用 tower property 把总体期望按 $X$ 条件化，在几乎每个 $x$ 上比较 action；B 再固定同一个 $P(Y\mid x)$，只改变 loss，观察 optimal functional 随之改变；C 最后审计“不可约误差”说法，增加 observation information、允许拒绝动作或改变成本矩阵都会改变可达到的 minimum。

**适用边界（图没有证明什么）。** 图默认 regular conditional law、measurable selection 与所需 moments/minimizers 存在，未覆盖无界动作、causal intervention、partial identification 或 adversarial decision。Bayes rule 是已知真实 $P$ 的 oracle，不给 posterior estimator 的统计误差；Bayes predictor 也不等于带 Bayesian prior 训练的任意模型。

## 一、学习目标

1. 从总体风险推导 pointwise conditional-risk minimization；
2. 区分 Bayes decision rule、Bayesian inference 与 MAP parameter estimation；
3. 推导二分类 0–1 Bayes classifier 及最小风险；
4. 推导 cost-sensitive threshold 与 reject option；
5. 证明平方损失下条件均值最优；
6. 证明绝对损失下条件中位数最优；
7. 用 entropy + KL 分解证明 log loss 下真实条件分布最优；
8. 区分 Bayes risk、noise、approximation error 与 estimation error；
9. 解释 posterior estimation、calibration 与 downstream decision 的接口；
10. 审计现实任务中 observation 不足、label ambiguity 与 causal action 的边界。

## 二、从总体风险降到每个输入的条件风险

给定预测器 $h:\mathcal X\to\mathcal A$，

$$
R_P(h)=\mathbb E[\ell(h(X),Y)].
$$

由 tower property：

$$
\begin{aligned}
R_P(h)
&=\mathbb E_X
\left[
\mathbb E[\ell(h(X),Y)\mid X]
\right]\\
&=\mathbb E_X[r(h(X)\mid X)],
\end{aligned}
$$

其中条件风险

$$
r(a\mid x)=\mathbb E[\ell(a,Y)\mid X=x].
$$

若对几乎每个 $x$ 能选到可测 minimizer

$$
h^*(x)\in\arg\min_{a\in\mathcal A}r(a\mid x),
$$

则对任意 $h$：

$$
r(h^*(x)\mid x)\le r(h(x)\mid x)\quad P_X\text{-a.s.}
$$

积分后得到

$$
R_P(h^*)\le R_P(h).
$$

这就是 Bayes decision principle。

> [!note] 可测选择边界
> “对每个 $x$ 取 argmin”在一般空间中还需 argmin 存在且能组成可测函数。有限动作空间通常没有困难；无限维 action 或非紧空间需要 measurable selection 与 integrability 条件。本章不隐藏这一步，但初级例子默认条件满足。

## 三、二分类 0–1 loss

令 $Y\in\{0,1\}$，定义 posterior class probability

$$
\eta(x)=\Pr(Y=1\mid X=x).
$$

若预测动作 $a=1$：

$$
r(1\mid x)=\Pr(Y=0\mid X=x)=1-\eta(x).
$$

若预测 $a=0$：

$$
r(0\mid x)=\Pr(Y=1\mid X=x)=\eta(x).
$$

因此选择风险较小者：

$$
\boxed{
h^*_{01}(x)=\mathbf1\{\eta(x)\ge1/2\}
}
$$

（$\eta=1/2$ 时任意 tie-breaking）。条件 Bayes risk 为

$$
r^*(x)=\min\{\eta(x),1-\eta(x)\},
$$

总体 Bayes risk：

$$
\boxed{
R^*_{01}=\mathbb E_X\min\{\eta(X),1-\eta(X)\}.
}
$$

若 $Y$ 在给定 $X$ 后仍随机，这个风险可以严格大于 0；模型容量再大也无法用同一 observation 消除它。

## 四、多分类 0–1 loss

令

$$
\eta_k(x)=\Pr(Y=k\mid X=x),
\qquad k=1,\ldots,K.
$$

预测 $a$ 的条件错误率为

$$
r(a\mid x)=1-\eta_a(x).
$$

所以

$$
h^*(x)\in\arg\max_k\eta_k(x),
$$

以及

$$
R^*_{01}=\mathbb E_X[1-\max_k\eta_k(X)].
$$

Bayes classifier 只需 posterior 的最大类；但若后续成本、阈值或 abstention 改变，完整 posterior 仍有价值。

## 五、成本敏感分类：阈值不是永远 $1/2$

令 false positive 成本 $c_{FP}>0$，false negative 成本 $c_{FN}>0$，正确预测成本 0。

预测 1 的条件风险：

$$
r(1\mid x)=c_{FP}[1-\eta(x)].
$$

预测 0 的条件风险：

$$
r(0\mid x)=c_{FN}\eta(x).
$$

选择 1 当且仅当

$$
c_{FP}(1-\eta)\le c_{FN}\eta,
$$

即

$$
\boxed{
\eta(x)\ge
\frac{c_{FP}}{c_{FP}+c_{FN}}.
}
$$

若漏诊成本 $c_{FN}$ 很大，阈值下降；这不是“牺牲数学正确性”，而是决策问题本来就不同。

### 手算

若 $c_{FP}=1,c_{FN}=9$，阈值是

$$
\frac{1}{1+9}=0.1.
$$

posterior $\eta(x)=0.2$ 虽低于 $1/2$，仍应判为正类，因为：

$$
r(1\mid x)=1\times0.8=0.8,
\qquad
r(0\mid x)=9\times0.2=1.8.
$$

## 六、reject/abstain option

令误分类成本为 1，正确为 0，拒绝并转人工成本为 $c\in(0,1/2)$。

三种动作风险：

$$
r(0\mid x)=\eta(x),
$$

$$
r(1\mid x)=1-\eta(x),
$$

$$
r(\bot\mid x)=c.
$$

因此：

$$
h^*(x)=
\begin{cases}
0,&\eta(x)\le c,\\
\bot,&c<\eta(x)<1-c,\\
1,&\eta(x)\ge1-c.
\end{cases}
$$

高不确定区域不是“硬猜”，而是进入人工/更多检测流程。coverage 与 selective risk 必须同时报告。

## 七、平方损失：条件均值

令 $Y\in\mathbb R$，$\ell(a,Y)=(a-Y)^2$，假设二阶矩有限。记

$$
\mu(x)=\mathbb E[Y\mid X=x].
$$

加入并减去 $\mu$：

$$
\begin{aligned}
\mathbb E[(Y-a)^2\mid X=x]
&=\mathbb E[(Y-\mu+\mu-a)^2\mid X=x]\\
&=\mathbb E[(Y-\mu)^2\mid X=x]
+(a-\mu)^2\\
&\quad+2(a-\mu)\mathbb E[\mu-Y\mid X=x].
\end{aligned}
$$

交叉项为 0，所以

$$
\boxed{
r(a\mid x)=\operatorname{Var}(Y\mid X=x)+(a-\mu(x))^2.
}
$$

唯一最优动作是

$$
h^*(x)=\mathbb E[Y\mid X=x],
$$

Bayes risk 为

$$
R^*_{2}=\mathbb E[\operatorname{Var}(Y\mid X)].
$$

这给出“不可约噪声”的一个精确含义，但只针对当前 $X$ 与平方损失。

## 八、绝对损失：条件中位数

对 $\ell(a,Y)=|a-Y|$，令 $F_x(a)=\Pr(Y\le a\mid X=x)$。在连续情形，目标的导数/次梯度满足

$$
\partial_a\mathbb E[|a-Y|\mid X=x]
=\Pr(Y<a\mid x)-\Pr(Y>a\mid x)
$$

并在原子处分成区间。最优条件为

$$
\Pr(Y\le a\mid x)\ge\frac12,
\qquad
\Pr(Y\ge a\mid x)\ge\frac12.
$$

即任意 conditional median 最优。

平均数与中位数不同，说明换 loss 会改变 Bayes target；不能只说“回归的真函数”。

## 九、log loss：真实条件分布

对离散 $Y\in\{1,\ldots,K\}$，动作是概率向量 $q(x)\in\Delta^{K-1}$，真实条件分布是

$$
p_k(x)=\Pr(Y=k\mid X=x).
$$

条件 log risk：

$$
r(q\mid x)
=-\sum_{k=1}^Kp_k(x)\log q_k(x).
$$

加入减去 $-\sum_kp_k\log p_k$：

$$
\begin{aligned}
r(q\mid x)
&=H(p(\cdot\mid x))
+\sum_kp_k(x)\log\frac{p_k(x)}{q_k(x)}\\
&=H(p(\cdot\mid x))
+\operatorname{KL}(p(\cdot\mid x)\|q(\cdot\mid x)).
\end{aligned}
$$

由 KL 非负：

$$
\boxed{q^*(\cdot\mid x)=p(\cdot\mid x)}
$$

（在 $p$ 的支持上几乎处处唯一）。Bayes log risk 是 conditional entropy：

$$
R^*_{\log}=H(Y\mid X).
$$

这就是 log loss 作为 strictly proper scoring rule 的核心；但有限模型与数据得到的 $q_\theta$ 仍可能未校准。

## 十、Bayes risk 到底“不可约”到什么程度

Bayes risk 依赖完整合同：

$$
R^*=R^*(P,\mathcal X,\mathcal A,\ell).
$$

改变下列任一项，下限都会改变：

- 加入更有信息的 observation，例如额外医学检查；
- 改变 action，例如允许 abstain 或序贯查询；
- 改变 loss/cost；
- 改变 target population；
- 从预测问题改成可干预的 causal decision problem。

所以“Bayes error 是数据集固有噪声”过于粗糙。它是当前 information/action/loss 合同下的 oracle risk。

## 十一、Bayes decision 不等于 Bayesian learning

| 术语 | 对什么取概率 | 输出 |
|---|---|---|
| Bayes decision rule | 假设真实 $P(Y\mid X)$ 已知 | 最小 conditional risk 的动作 |
| Bayesian parameter inference | 给参数先验与 likelihood | posterior $p(\theta\mid S)$ |
| posterior predictive | 对参数 posterior 积分 | $p(y\mid x,S)$ |
| MAP | 最大化 posterior density | 一个参数 mode |

frequentist 方法若一致估计 $P(Y\mid X)$，也可趋近 Bayes decision；Bayes classifier 这个名字不要求训练时使用 parameter prior。反过来，使用 Bayesian posterior 也不保证模型类/likelihood 正确或 decision loss 对齐。

## 十二、posterior estimate 与动作的分层

现代概率分类推荐两步：

1. 估计或产生预测分布 $q(y\mid x)$；
2. 给定业务 loss，计算

$$
a_q(x)\in\arg\min_a\sum_y q(y\mid x)\ell(a,y).
$$

同一 $q$ 可以支持不同成本、阈值与 abstention。若只训练硬分类边界，成本变化后可能无法重用；若 $q$ 未校准，理论 Bayes threshold 也会产生错误决策。

## 十三、边界与常见误解

> [!danger] 不要把 Bayes 当成形容词
> - Bayes risk 不是“Bayesian 模型的测试误差”；
> - posterior mode 只对应 0–1 类别动作，不是所有 loss 的最优动作；
> - conditional mean 不是任意回归损失下的真值；
> - $R^*>0$ 不自动意味着标签错误，可能是 observation 不完整；
> - $R^*=0$ 也不意味着有限样本 learner 能找到零风险函数；
> - 估计概率 accuracy 高不等于 calibration 好。

## 十四、AI 应用映射

| AI 场景 | 条件律/score | action | 关键 loss |
|---|---|---|---|
| 医疗诊断 | disease posterior | 治疗/复查/拒绝 | 不对称成本与安全约束 |
| 垃圾邮件 | spam probability | block/inbox/review | 用户特异成本 |
| LLM next-token | token conditional distribution | sample/argmax/search | token log loss并非帮助性 utility |
| 风险评分 | event probability | threshold/resource allocation | capacity、cost、fairness constraints |
| selective prediction | confidence/posterior | answer/abstain | risk–coverage trade-off |

生成模型的 log-likelihood Bayes target 是数据条件分布；实际 decoding 又定义新的 action rule，质量、安全与多样性不由 token log loss 单独决定。

## 十五、复习清单

- [ ] 我能从 tower property 推到 pointwise conditional minimization；
- [ ] 我能推导 0–1 与成本敏感阈值；
- [ ] 我能推导 reject region；
- [ ] 我能证明平方损失取条件均值、绝对损失取中位数；
- [ ] 我能写出 cross-entropy = entropy + KL；
- [ ] 我能解释 Bayes decision 与 Bayesian inference 的区别；
- [ ] 我知道 Bayes risk 依赖 observation、action、loss 与 population。

## 来源

- [[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]：Bayes optimal predictor、risk 与 learnability 接口；
- [[Bayesian 推断与后验预测]]：parameter posterior 与 posterior predictive 的区别；
- 图示脚本：`00-知识库管理/_labs/code/plot_risk_decision_evaluation_contract.py`。
