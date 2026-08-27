---
type: theorem
status: draft
area: [learning-theory/bandits, partial-feedback, reinforcement-learning-interface]
aliases: [Multi-Armed Bandit, EXP3, Bandit Feedback, RL Interface]
node_id: LT-76
prerequisites: ["[[在线学习协议、Regret 与 Comparator]]", "[[Experts、Weighted Majority 与 Multiplicative Weights]]", "[[重要性加权与 Covariate Shift 校正]]"]
related: ["[[随机、对抗与自适应序列的区别]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[强化学习与智能体 MOC]]"]
sources: ["[[S-2002-Auer-Adversarial-Bandit]]", "[[S-2020-Lattimore-Szepesvari-Bandits]]", "[[S-2018-Sutton-Barto-RL]]"]
exercises: ["[[习题 - Bandit Feedback 与强化学习接口]]"]
solutions: ["[[解答 - Bandit Feedback 与强化学习接口]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-bandit-rl-interface-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Bandit Feedback 与强化学习接口

> [!abstract] 本章主问题
> full information 中可见所有 action loss；bandit 中只看所选 action 的结果。缺失反馈迫使算法主动探索，并用 inverse-propensity estimator 重建不可见损失。强化学习又多出 state transition、长期回报和 action 改变未来数据，不能把 bandit regret 直接改名为 RL。

## 一、学习目标

完成本章后，应能：

1. 区分 stochastic、adversarial 与 contextual bandit；
2. 定义 realized regret、pseudo-regret 与 best-arm identification；
3. 解释 exploration–exploitation；
4. 推导 bandit loss estimator 的条件无偏性；
5. 说明 $1/p_{t,i}$ 为什么带来方差；
6. 写出 EXP3 的基本更新与量级；
7. 解释 UCB 的 optimism 原理与 gap-dependent regret；
8. 区分 bandit、contextual bandit 与 MDP/RL；
9. 说明 offline logs 为什么需要 overlap；
10. 为 LLM routing、推荐和安全探索建立反馈合同。

## 二、Multi-Armed Bandit Protocol

有 $K$ 个 arms。第 $t$ 轮：

1. learner 根据历史选择 distribution $p_t$；
2. 采样 $I_t\sim p_t$；
3. environment 产生 reward $r_{t,I_t}$ 或 loss $\ell_{t,I_t}$；
4. learner 只观察所选 arm 的结果。

与 experts full information 的差异是：$\ell_{t,j}$ 对 $j\ne I_t$ 不可见，故不能直接更新所有专家权重。

## 三、Stochastic Bandit

每个 arm $i$ 的 rewards 独立来自固定分布，均值 $\mu_i$。令

$$
\mu^*=\max_i\mu_i,\qquad \Delta_i=\mu^*-\mu_i.
$$

pseudo-regret 为

$$
\overline R_T
=T\mu^*-E\sum_{t=1}^Tr_{t,I_t}
=\sum_{i=1}^K\Delta_iE[N_i(T)].
$$

最后等式显示：regret 来自抽取次优 arm 的次数。

## 四、UCB：对不确定性保持乐观

一种经典 UCB index 是

$$
\operatorname{UCB}_{t,i}
=\widehat\mu_{t-1,i}
+\sqrt{\frac{2\log t}{N_i(t-1)}}.
$$

选择 index 最大的 arm。第二项在样本少时大，强制探索；样本多后收缩。典型 gap-dependent bound 为

$$
E[R_T]
=O\left(\sum_{i:\Delta_i>0}\frac{\log T}{\Delta_i}\right),
$$

常数与 reward range/sub-Gaussian 条件有关。$\Delta_i$ 很小时该形式变差，gap-free bound 则是 $O(\sqrt{KT\log T})$ 一类量级。

## 五、Adversarial Bandit

environment 给任意 loss vector $\ell_t\in[0,1]^K$，但 learner 只看 $\ell_{t,I_t}$。比较 best fixed arm：

$$
R_T=E\sum_t\ell_{t,I_t}-\min_i\sum_t\ell_{t,i}.
$$

这里不假设固定 arm mean；UCB 的 empirical-mean concentration 故事不再适用。

## 六、Inverse-Propensity Loss Estimator

对每个 arm 定义

$$
\boxed{
\widehat\ell_{t,i}
=\frac{\mathbf1\{I_t=i\}\ell_{t,i}}{p_{t,i}}.
}
$$

若 $p_{t,i}>0$ 且 $\ell_t$ 在采样 $I_t$ 前已确定，则

$$
E[\widehat\ell_{t,i}\mid\mathcal F_{t-1},\ell_t]
=p_{t,i}\frac{\ell_{t,i}}{p_{t,i}}
=\ell_{t,i}.
$$

所以它逐坐标条件无偏。

## 七、无偏不等于低方差

二阶矩为

$$
E[\widehat\ell_{t,i}^2\mid\mathcal F_{t-1},\ell_t]
=\frac{\ell_{t,i}^2}{p_{t,i}}.
$$

$p_{t,i}$ 很小时方差爆炸；$p_{t,i}=0$ 时该 arm 永远不可识别。显式 exploration、implicit exploration 或 variance-aware estimator 的任务，是控制这个 denominator，而不仅是“尝试新东西”。

## 八、EXP3 的骨架

EXP3 可写成：

$$
q_{t,i}=\frac{w_{t,i}}{\sum_jw_{t,j}},\qquad
p_{t,i}=(1-\gamma)q_{t,i}+\frac\gamma K,
$$

采样 $I_t$、构造 $\widehat\ell_{t,i}$，再更新

$$
w_{t+1,i}=w_{t,i}e^{-\eta\widehat\ell_{t,i}}.
$$

适当选择 $\eta,\gamma$ 可得 expected regret

$$
R_T=O(\sqrt{TK\log K}).
$$

相较 full-information Hedge 的 $O(\sqrt{T\log K})$，多出的 $\sqrt K$ 体现部分反馈的统计代价。

## 九、Realized 与 Pseudo-Regret

stochastic bandit 中 pseudo-regret 比较 expected means；realized regret 会包含 reward noise。adversarial bandit 中 expectation 常对 learner 随机性取；若要 high-probability realized bound，还需控制 importance estimator 的重尾/conditional variance。

“平均 regret 小”也不等于最后推荐的 arm 正确；best-arm identification 是固定置信/固定预算的纯探索问题，评价指标是识别错误概率或 sample complexity。

## 十、Contextual Bandit

每轮先看到 context $x_t$，再选 action $a_t$，只观察 $r_t(a_t)$。comparator 是 policy class $\Pi$：

$$
R_T(\Pi)
=\max_{\pi\in\Pi}\sum_tr_t(\pi(x_t))
-\sum_tr_t(a_t).
$$

它比普通 MAB 多了 context-to-action generalization，但仍通常把每轮结果视为单步反馈。

## 十一、Bandit 与强化学习的边界

MDP/RL 增加 state $S_t$、transition

$$
P(S_{t+1},R_{t+1}\mid S_t,A_t),
$$

以及长期 return

$$
G_t=\sum_{k\ge0}\gamma^kR_{t+k+1}.
$$

当前 action 改变未来 state distribution，因此需要 credit assignment、value/Bellman equation、occupancy measure 与 policy evaluation。普通 bandit 可看成 horizon-1、无持久 state 的特殊决策问题；contextual bandit 也不自动处理跨轮状态影响。

## 十二、Offline Logs、Overlap 与反事实

若日志由 behavior policy $b(a\mid x)$ 生成，target policy $\pi$ 的单步价值可用 IPS：

$$
\widehat V_{\rm IPS}(\pi)
=\frac1n\sum_{t=1}^n
\frac{\pi(a_t\mid x_t)}{b(a_t\mid x_t)}r_t.
$$

必须有 overlap：$\pi(a\mid x)>0\Rightarrow b(a\mid x)>0$，并且 propensity 已知/可可靠估计、无隐藏 action confounding。序列 RL 中还要处理轨迹 likelihood ratio 或 occupancy mismatch，方差更严重。

## 十三、安全与约束

探索可能造成真实损害。部署前需区分：

- reward regret；
- constraint violation/cumulative cost；
- conservative baseline guarantee；
- off-policy uncertainty；
- human override 与 forbidden actions。

一个低 regret theorem 不自动满足安全约束。

## 十四、一个两臂估计例子

若 $p_t=(0.8,0.2)$，采到 arm 2 且观察 loss $0.6$，则

$$
\widehat\ell_t=(0,0.6/0.2)=(0,3).
$$

虽然原 loss 在 $[0,1]$，估计值可大于 1。条件期望仍正确，但 exponent update 与浓缩必须使用 estimator 的实际范围/方差。

## 十五、图：Feedback Ladder 到 State Dynamics

先看图回答：为什么把未选 action loss 填成 0 会产生偏差，而除以 $p_{t,i}$ 能修正一阶期望却放大二阶矩？

![[00-知识库管理/_assets/figures/learning-theory/fig-bandit-rl-interface-v2.svg|900]]

> [!figure] 图 20.9-08　部分反馈、探索估计与 RL 边界
> 左栏比较 full、bandit 与 contextual feedback；中栏展示 propensity、无偏性和方差账；右栏从 horizon-1 bandit 过渡到 stateful MDP，并标出 offline overlap 与安全约束。来源：依据 Auer et al.、Lattimore–Szepesvári 与 Sutton–Barto 独立绘制；由 [[plot_online_learning_part2_v2.py]] 确定性生成。

**怎样读图**：先问“未选 action 的结果是否可见”，再问“action 是否改变未来 state”，由此选择 experts、bandit 或 RL 理论。

**图没有证明什么**：图没有证明任意 adaptive/current-action-aware adversary 下 EXP3 成立，也没有把单步 IPS 自动推广到长期 RL。

## 十六、AI 接口

- LLM routing：只调用一个模型时通常是 contextual bandit，而非 full-information experts；
- 推荐系统：若推荐改变用户兴趣，需 stateful/policy analysis；
- RLHF 数据选择：query/pair sampling 影响可观察 preference 与覆盖；
- agent tool use：action 改变后续 observation，已进入 partial-observable sequential decision；
- online safety：探索概率必须和风险预算共同设计。

## 十七、常见错误

1. 用 full-information Hedge 更新不可见 arms；
2. 令某 arm 概率为零后仍声称可学习；
3. 只证明 estimator 无偏而不查方差；
4. 把 UCB 的 stochastic 假设用于 adversarial rewards；
5. 把 low regret 当 best-arm identification；
6. 把 contextual bandit 当完整 RL；
7. offline evaluation 忘记 propensity/overlap；
8. 以 reward regret 代替安全保证。

## 十八、最小记忆与掌握标准

> [!summary]
> - bandit 只观察 chosen-action feedback；
> - exploration 保证 overlap，IPS 恢复条件无偏；
> - 方差按 $1/p$ 放大；
> - stochastic UCB 与 adversarial EXP3 的假设不同；
> - contextual bandit 比较 policy，RL 还建模 state transition 与长期 return；
> - offline overlap、长期 credit 与安全约束不能由 regret 自动解决。

能写三类 protocol（A）、手算 IPS/UCB（B）、证明无偏与 regret 代价来源（C）、审计 offline/safety/RL 外推（D），并为真实 AI 部署选择正确交互模型（E）。

## 十九、练习与独立详解

- [[习题 - Bandit Feedback 与强化学习接口]]
- [[解答 - Bandit Feedback 与强化学习接口]]

## 参考来源

- [[S-2002-Auer-Adversarial-Bandit]]
- [[S-2020-Lattimore-Szepesvari-Bandits]]
- [[S-2018-Sutton-Barto-RL]]
