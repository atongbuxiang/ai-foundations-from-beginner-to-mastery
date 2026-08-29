---
type: assessment-solution
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/online-learning, learning-theory/boosting, learning-theory/bandits]
assessment_id: ONLINE-CUM-01
assessment: "[[阶段测验 - 在线学习、Boosting 与序列预测（20.9）]]"
experiment: "[[实验 - 在线学习、Boosting 与序列预测累计复现门]]"
code: "[[00-知识库管理/_labs/code/online_boosting_cumulative_gate.py]]"
related: ["[[在线学习、Boosting 与序列预测 MOC]]", "[[学习理论完整课程地图与掌握标准]]"]
created: 2026-08-29
updated: 2026-08-29
---

# 阶段测验解答 - 在线学习、Boosting 与序列预测（20.9）

> [!danger] 答案隔离
> 未封存口试、闭卷、prediction sheet 与原稿 hash 时不要阅读。canonical 或 blind 数值一旦暴露，本次尝试便不能再算 blind。

> [!abstract] 总原则
> 先写“这一轮谁先行动、谁能看到什么”，再写更新式。同一个算法名字，换了 feedback、comparator、adversary visibility 或概率对象，定理就可能已经换了。

## 第 1 题解答：八层序列学习账本（5 分）

| 层 | 必须记录 | 模型路由示例 |
|---|---|---|
| protocol | $x_t$、决策、环境响应和更新的先后 | 先到请求，路由器选模型，再显示结果并等待反馈 |
| filtration | 第 $t$ 轮决策可测于哪个 $\sigma$-代数 | 路由器只能使用过去日志和当前 context，不能看未来用户评分 |
| feedback | 当轮看到所有 action 还是只看所选 action | 若只部署一个模型，通常是 bandit，不是 full information |
| comparator | fixed expert、switching sequence、policy 还是 oracle | 与全期最佳固定模型比，不偷换成每轮 oracle |
| potential | 哪个非负量负责望远镜 | Hedge 的 log-total-weight，OGD 的到 comparator 距离 |
| probability | pathwise、expectation 还是 high probability；对哪个随机性 | 分开路由器 fresh coin、环境随机性和日志采样 |
| conversion | online loss 怎样转成新请求上的 risk | iid next-example、random iterate 或独立 holdout；不直接拿 regret 当 risk |
| boundary | delay、drift、overlap、safety 与状态动力学 | 用户会被模型回答改变时，可能已进入 RL/policy-regret 问题 |

满分答案必须把“后见最佳”的可见信息和日志字段也写清，否则 comparator 可能是不可实现的。

## 第 2 题解答：Protocol、Comparator 与 Regret（5 分）

full-information 的最小协议是：学习者在过去 history 上选 $a_t$ 或分布 $p_t$；环境揭示当轮整个 loss vector $\ell_t$；学习者承担 $\ell_t(a_t)$ 或 $\langle p_t,\ell_t\rangle$。对 fixed action 集合 $\mathcal A$，

$$
R_T^{\mathrm{ext}}
=\sum_{t=1}^T\ell_t(a_t)
-\min_{a\in\mathcal A}\sum_{t=1}^T\ell_t(a).
$$

Regret 可为负：例如两轮允许学习者换 action，loss 为 $(0,1)$ 和 $(1,0)$，学习者每轮选零 loss action，累计为 0；任一 fixed action 累计为 1，所以 regret $=-1$。

$R_T=o(T)$ 精确表示

$$
\frac1T\sum_t\ell_t(a_t)
-\min_a\frac1T\sum_t\ell_t(a)\to0.
$$

它不表示累计 loss 趋零、不表示恢复真实参数，也不自动表示 iid population risk 小。Switching comparator 可以随时间改变但必须限制 switch budget/path variation；policy comparator 在 action 会改变后续观测时比较反事实 trajectory，不能由 static external regret 替代。

## 第 3 题解答：Hedge Potential 证明（5 分）

令 $L_{t,i}=\sum_{s=1}^t\ell_{s,i}$，$W_t=\sum_i e^{-\eta L_{t-1,i}}$，所以 $W_1=N$。对任意固定专家 $i$，

$$
W_{T+1}\ge e^{-\eta L_{T,i}},
\qquad
\log\frac{W_{T+1}}{W_1}
\ge-\eta L_{T,i}-\log N.
$$

这是 potential 下界：总权重至少保留了专家 $i$ 的那一项。另一方面，

$$
\frac{W_{t+1}}{W_t}
=\sum_i p_{t,i}e^{-\eta\ell_{t,i}}.
$$

将 $\ell_{t,I}$ 看成在 $I\sim p_t$ 下取 $[0,1]$ 值的随机变量，Hoeffding lemma 给出

$$
\log\sum_i p_{t,i}e^{-\eta\ell_{t,i}}
\le-\eta\langle p_t,\ell_t\rangle+\frac{\eta^2}{8}.
$$

对 $t$ 求和时左边望远镜：

$$
\log\frac{W_{T+1}}{W_1}
\le-\eta\sum_t\langle p_t,\ell_t\rangle+\frac{\eta^2T}{8}.
$$

与 lower potential 合并并对任意 $i$ 重排：

$$
\sum_t\langle p_t,\ell_t\rangle-L_{T,i}
\le\frac{\log N}{\eta}+\frac{\eta T}{8}.
$$

取最佳 fixed expert 得结论。这个常数使用了 loss range $[0,1]$；换 range 必须重新缩放。

## 第 4 题解答：OGD/OMD 与对手信息（5 分）

对 $x_{t+1}=\Pi_K(x_t-\eta g_t)$ 和任意 $u\in K$，投影非扩张性给出

$$
\begin{aligned}
\|x_{t+1}-u\|^2
&\le\|x_t-\eta g_t-u\|^2\\
&=\|x_t-u\|^2-2\eta\langle g_t,x_t-u\rangle+\eta^2\|g_t\|^2.
\end{aligned}
$$

凸性给 $f_t(x_t)-f_t(u)\le\langle g_t,x_t-u\rangle$，因而

$$
\sum_t(f_t(x_t)-f_t(u))
\le\frac{\|x_1-u\|^2}{2\eta}
+\frac\eta2\sum_t\|g_t\|^2.
$$

OMD 把 $\frac12\|u-x_t\|^2$ 换成 $D_\psi(u,x_t)$，一步不等式的典型形式是

$$
\langle g_t,x_t-u\rangle
\le\frac{D_\psi(u,x_t)-D_\psi(u,x_{t+1})}{\eta}
+\frac\eta{2\sigma}\|g_t\|_*^2,
$$

其中 $\psi$ 相对 primal norm $\sigma$-强凸，gradient 用对偶范数。

对手反例：两 action 中，对手看到 realized $a_t$ 后设 $\ell_t(a_t)=1$、$\ell_t(3-a_t)=0$。学习者 loss 恒为 $T$；两 fixed action 的 loss 分别是学习者选它的次数 $n_1,n_2$，最佳为 $\min(n_1,n_2)\le T/2$，故 regret 至少 $T/2$。这不违反 Hedge 定理：它违反了 loss 不能看当轮 fresh action 的信息合同。

## 第 5 题解答：A 轨 Hedge 手算（8 分）

因 $e^{-\eta}=1/2$，每累积 1 单位 loss，权重减半：

| 轮 | 轮前累计 loss | $p_t$ | 当轮 loss | 算法 loss |
|---:|---|---|---|---:|
| 1 | $(0,0,0)$ | $(1/3,1/3,1/3)$ | $(0,1,1)$ | $2/3$ |
| 2 | $(0,1,1)$ | $(1/2,1/4,1/4)$ | $(1,0,1)$ | $3/4$ |
| 3 | $(1,1,2)$ | $(2/5,2/5,1/5)$ | $(0,1,0)$ | $2/5$ |
| 4 | $(1,2,2)$ | $(1/2,1/4,1/4)$ | $(1,1,0)$ | $3/4$ |

因此

$$
L_{\mathrm{alg}}=\frac23+\frac34+\frac25+\frac34
=\frac{77}{30}=2.566667.
$$

最终 expert losses 为 $(2,3,2)$，最佳 loss $2$，regret

$$
\frac{77}{30}-2=\frac{17}{30}=0.566667.
$$

最终未归一权重 $(1/4,1/8,1/4)$，归一化为 $(0.4,0.2,0.4)$。理论界为

$$
\frac{\log3}{\log2}+\frac{4\log2}{8}
=1.931536.
$$

上界不要求对每个有限序列取等；“实际 regret 更小”只说这个 instance 没有耗尽 worst-case 预算。

## 第 6 题解答：A 轨 OGD 与可见性（7 分）

| $t$ | $g_t$ | 轮前 $x_t$ | $g_tx_t$ | 更新后 |
|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | $-1/2$ |
| 2 | -2 | $-1/2$ | 1 | $1/2$ |
| 3 | 1 | $1/2$ | $1/2$ | 0 |
| 4 | 2 | 0 | 0 | $-1$ |
| 5 | -1 | $-1$ | 1 | $-1/2$ |

算法累计 loss $=2.5$。因 $\sum_tg_t=1$，$[-1,1]$ 上 best fixed comparator 为 $u=-1$，loss $=-1$，regret $=3.5$。Comparator-specific bound 使用 $\lvert x_1-u\rvert=1$与 $\sum_tg_t^2=11$：

$$
\frac{1}{2(1/2)}+\frac{1/2}{2}\,11
=1+2.75=3.75.
$$

在 current-action-aware 反例中，六轮学习者 loss $=6$，两 action 都各被选 3 次，所以 best fixed loss $=3$，regret $=3$。

## 第 7 题解答：B 轨 Perceptron（8 分）

采用零 margin 也更新的约定：

| 样本 | 更新前 $w$ | $y\langle w,x\rangle$ | 是否更新 | 更新后 $w$ |
|---|---|---:|---|---|
| $((1,0),+1)$ | $(0,0)$ | 0 | 是 | $(1,0)$ |
| $((0,1),+1)$ | $(1,0)$ | 0 | 是 | $(1,1)$ |
| $((-1,-1),-1)$ | $(1,1)$ | 2 | 否 | $(1,1)$ |

因此 $M=2$。对 $u=(1,1)/\sqrt2$，三个 signed margins 为 $(1/\sqrt2,1/\sqrt2,\sqrt2)$，故 $\gamma=1/\sqrt2$；$R=\sqrt2$。界为

$$
M\le\left(\frac{R}{\gamma}\right)^2
=\left(\frac{\sqrt2}{1/\sqrt2}\right)^2=4.
$$

一般证明只在 mistake rounds $k=1,…,M$ 上索引。每次更新都有

$$
\langle w_{k+1},u\rangle
=\langle w_k,u\rangle+y_k\langle x_k,u\rangle
\ge\langle w_k,u\rangle+\gamma,
$$

所以 $\langle w_M,u\rangle\ge M\gamma$。同时 mistake 条件给出

$$
\|w_{k+1}\|^2
=\|w_k\|^2+2y_k\langle w_k,x_k\rangle+\|x_k\|^2
\le\|w_k\|^2+R^2,
$$

故 $\|w_M\|\le R\sqrt M$。再由 Cauchy，$M\gamma\le\langle w_M,u\rangle\le\|w_M\|$，得界。它只控制满足共同 margin separator 的那条序列上的 mistake 数；没有 sampling law 和新样本概率，因而不是 population-risk theorem。

## 第 8 题解答：B 轨 AdaBoost（7 分）

第一轮 $\varepsilon_1=1/4$，

$$
\alpha_1=\frac12\log3=0.549306,
\qquad
Z_1=2\sqrt{\frac14\frac34}=\frac{\sqrt3}{2}=0.866025.
$$

更新后

$$
D_2=(1/6,1/6,1/6,1/2).
$$

第二轮错在前两个样本，所以 $\varepsilon_2=1/3$，

$$
\alpha_2=\frac12\log2=0.346574,
\qquad
Z_2=\frac{2\sqrt2}{3}=0.942809,
$$

且

$$
D_3=(1/4,1/4,1/8,3/8).
$$

两轮 ensemble margins 为

$$
(\alpha_1-\alpha_2,\alpha_1-\alpha_2,
\alpha_1+\alpha_2,-\alpha_1+\alpha_2)
$$

$$
=(0.202733,0.202733,0.895880,-0.202733).
$$

因此 training error $=1/4$，minimum margin $=-0.202733$。展开权重递推：

$$
D_{T+1}(i)
=\frac{D_1(i)e^{-\sum_t\alpha_ts_{t,i}}}{\prod_tZ_t}.
$$

对 $i$ 求和并用 $D_1(i)=1/m$、$\sum_iD_{T+1}(i)=1$，得

$$
\frac1m\sum_i e^{-y_iF_T(x_i)}=\prod_tZ_t
=\frac{\sqrt6}{3}=0.816497.
$$

由 $\mathbf1\{z\le0\}\le e^{-z}$，training error 至多这个 product。它不是 test error 界：还没有对样本外风险做任何 complexity/stability/margin-distribution 论证。

## 第 9 题解答：C 轨 Online-to-Batch（8 分）

因 $h_t$ 只依赖 $Z_{<t}$，在给定过去后它是固定的；又因 $Z_t$ 与 $Z_{<t}$ iid，

$$
\mathbb E[\ell(h_t,Z_t)\mid Z_{<t}]
=\mathbb E_{Z\sim P}[\ell(h_t,Z)]
=R(h_t).
$$

取期望并对 $t$ 求和，在 $I\sim\mathrm{Unif}\{1,…,T\}$ 与数据独立时，

$$
\mathbb E R(h_I)
=\frac1T\sum_t\mathbb E R(h_t)
=\frac1T\sum_t\mathbb E\ell(h_t,Z_t).
$$

如果 online regret 与 comparator $h^*$ 比较，则可得

$$
\mathbb E R(h_I)-R(h^*)
\le\frac{\mathbb E R_T}{T}.
$$

对 convex prediction set 和 convex loss，$\bar h=T^{-1}\sum_th_t$ 还可由 Jensen 满足 $R(\bar h)\le T^{-1}\sum_tR(h_t)$。

本题数值：

$$
\frac{0.2+0.4+0.1+0.3}{4}=0.25,
$$

$$
R_T=\sum_t(R(h_t)-0.1)=0.6,
\qquad
R_T/T=0.15=0.25-0.1.
$$

Last iterate $h_T$ 不是均匀平均，它可以在最后一轮很差；drift 破坏共同 $P$；adaptive selection 若再看评价数据挑 iterate，会引入额外 selection bias。

## 第 10 题解答：C 轨 UCB、IPS 与 Overlap（8 分）

UCB 使用 reward means，两个 index 为

$$
U_1=0.6+\sqrt{\frac{2\log30}{20}}=1.183198,
$$

$$
U_2=0.5+\sqrt{\frac{2\log30}{10}}=1.324766,
$$

因而选第 2 臂。这个选择来自第 2 臂的 exploration bonus 更大，不是它的 empirical mean 更大。

IPS 子题使用 loss。观察到 $A=3$时，整个 loss vector 的无偏估计为

$$
\widehat\ell=(0,0,0.9/0.2)=(0,0,4.5).
$$

target policy 的单次估计为

$$
\widehat R_\pi
=\frac{\pi_3\ell_3}{p_3}
=\frac{0.6\times0.9}{0.2}=2.7.
$$

它可超过 1，因为这是高方差加权估计，不是单个原始 loss。真实 target risk 是

$$
R_\pi=0.2(0.2)+0.2(0.6)+0.6(0.9)=0.7.
$$

方差为

$$
\operatorname{Var}(\widehat R_\pi)
=\sum_i\frac{\pi_i^2\ell_i^2}{p_i}-R_\pi^2
=1.0192,
$$

最大 density/propensity ratio 是 $\max_i\pi_i/p_i=3$。无偏性直接由

$$
\mathbb E_{A\sim p}
\left[\frac{\pi_A\ell_A}{p_A}\right]
=\sum_i p_i\frac{\pi_i\ell_i}{p_i}
=\sum_i\pi_i\ell_i
$$

得到。若存在 $p_i=0$ 而 $\pi_i>0$，log 中永远没有 action $i$ 的 outcome，两个在该 action 上 loss 不同的世界生成完全相同的数据，target value 不可识别。

Bandit 中 action 影响当轮 outcome；RL 中 action 还改变未来 state distribution 和 long-horizon return。单步 IPS 没有解决 state occupancy ratio、credit assignment 或 policy-induced feedback loop。

## 第 11 题解答：八节点路由表（7 分）

| ID | target | 关键条件/势能 | statement | 不能推出 |
|---|---|---|---|---|
| LT-69 | sequence external regret | move order + fixed comparator | 常为 pathwise 或对 learner coin 取期望 | population risk |
| LT-70 | Hedge regret | full loss vector、$[0,1]$、log $W_t$ | deterministic mixture loss 或 randomized expected loss | switching/policy regret |
| LT-71 | OCO regret | convexity、bounded geometry/dual gradient、distance/Bregman | pathwise first-order bound | 任意 nonconvex neural loss 结论 |
| LT-72 | realized/pseudo-regret | adversary 不观测当轮 fresh coin；martingale | expectation 或 high probability 必须标明 | current-action-aware 下 no-regret |
| LT-73 | sequence mistakes | common normalized margin separator；progress/norm | deterministic finite mistake certificate | iid generalization |
| LT-74 | empirical exponential loss/training error | weak edge on current $D_t$；$\prod Z_t$ | training-sample identity/bound | test error/noise robustness |
| LT-75 | population risk | iid fresh next example、past-measurability、random iterate/Jensen | expected；high probability 需 martingale 升级 | free last-iterate/drift guarantee |
| LT-76 | bandit regret/value | exploration/overlap、IPS/UCB potential | stochastic/adversarial 版本不同 | RL long-horizon return/safety |

## 第 12 题解答：删条件反例（7 分）

1. **当轮 action-aware**：用第 4/6 题的对手，直接得线性 regret。
2. **nonconvex OGD**：凸性线性化 $f_t(x_t)-f_t(u)\le\langle g_t,x_t-u\rangle$ 失效；例如在 stationary point $x_t=0$ 取梯度为零但 comparator loss 更小的 nonconvex loss。
3. **Perceptron**：定理只看给定序列。可令训练序列只出现一个易分点，部署分布却把大部分质量放在未见且被错分的点上。
4. **AdaBoost**：指数 loss 会持续放大 mislabeled/outlier 权重；training identity 不包含 test law 或 robust-noise assumption。
5. **last iterate**：一个算法可以前 $T-1$ 轮全好、最后一轮输出任意差 predictor，平均 regret 仍为 $O(1/T)$ 而 last iterate risk 很差。
6. **零探索**：$p_i=0,\pi_i>0$ 时 IPS 分母无定义，且 target action outcome 不可识别。
7. **bandit 不是 RL**：两个 action 可有相同 immediate reward，却转移到不同未来 state；单步 bandit 指标无法区分 long-horizon value。

## 第 13 题解答：Nonce Blind 复现（10 分）

> [!warning] 以下数值只能在 prediction sheet 封存后使用

固定 blind 命令为：

```bash
python3 00-知识库管理/_labs/code/online_boosting_cumulative_gate.py \
  --hedge-losses '0,1,0;1,0,1;1,1,0;0,0,1;1,0,0' \
  --hedge-eta 1.0986122886681098 \
  --ogd-gradients '2,-1,-1,2,-2,1' --ogd-eta 0.25 \
  --adaptive-actions '1,1,2,2,1' \
  --perceptron-examples '2,0,1;0,1,1;-1,-2,-1' --separator '1,1' \
  --boost-margins '1,1,1,-1,-1;-1,-1,1,1,1' \
  --online-risks '0.15,0.35,0.25,0.05,0.2' --comparator-risk 0.05 --delta 0.1 \
  --ucb-counts '12,18' --ucb-means '0.55,0.48' \
  --logging-probabilities '0.4,0.4,0.2' \
  --target-probabilities '0.1,0.3,0.6' \
  --bandit-losses '0.3,0.5,0.8' --chosen-action 2 \
  --output /tmp/online-cum-blind.svg
```

期望 stdout 为：

```text
TRACK A T=5 eta=1.098612 hedge_loss=2.790476 best=2.000000 regret=0.790476 bound=1.686633 final_probs=0.142857,0.428571,0.428571 ogd_T=6 ogd_eta=0.250000 ogd_loss=1.750000 comparator=-1.000000 ogd_regret=2.750000 ogd_bound=3.875000 adaptive_T=5 adaptive_regret=3.000000
TRACK B mistakes=2 final_w=2.000000,1.000000 R=2.236068 gamma=0.707107 mistake_bound=10.000000 progress=2.121320 norm=2.236068 boost_errors=0.400000,0.333333 alphas=0.202733,0.346574 Z=0.979796,0.942809 product=0.923760 training_error=0.400000 min_margin=-0.143841
TRACK C T=5 random_risk=0.200000 comparator=0.050000 online_regret=0.750000 excess=0.150000 radius=0.479853 ucb=1.302905,1.094745 ucb_choice=1 ips=0.000000,1.250000,0.000000 target_risk=0.660000 observed_estimate=0.375000 ips_variance=0.774900 max_ratio=3.000000
```

blind SVG SHA-256：

```text
2f54d14536bf71f86c76a57011d33456c91173d5d808b6f97b8eb3d92ff24960
```

评分不只比字符串：必须说明 Hedge 的最终重量为什么转向专家 2/3，Perceptron 的 $R$ 增大为什么使 worst-case bound 变松，以及观察到第 2 臂时 IPS sample 为何可低于 true target risk。

## 第 14 题解答：陌生 AI 迁移（10 分）

本题没有唯一系统，但满分交付必须包含以下证据。以实时 LLM 路由为例：

1. **时序**：context 到达 $\to$ 用过去日志选 model $\to$ 产生回答 $\to$ 获得延迟/成本/部分质量反馈 $\to$ 更新；
2. **comparator**：best fixed model 是最弱基线；contextual policy class 更实用，但需要明确类容量和 offline identifiability；
3. **feedback**：只部署一个 model 时是 contextual bandit；若用户未来请求被当前回答改变，升级为 stateful/RL 问题；
4. **主副指标**：主指标可为 cost-sensitive contextual regret；副指标必须包含 safety violation/worst-group quality，不能只有平均 reward；
5. **失效检查**：监测 minimum propensity、IPS effective sample size、feedback delay/censoring、context drift 和用户对已选 model 的反应；
6. **上线规则**：只在预注册的 holdout/off-policy lower confidence bound 改善且 safety upper bound 不变差时小流量上线；任一 guard 失败立即回滚；
7. **不能推出**：online reward 改善不证明因果长期收益、不证明未探索 action 安全，也不证明所有群体质量改善。

## Canonical 回归输出

```text
TRACK A T=4 eta=0.693147 hedge_loss=2.566667 best=2.000000 regret=0.566667 bound=1.931536 final_probs=0.400000,0.200000,0.400000 ogd_T=5 ogd_eta=0.500000 ogd_loss=2.500000 comparator=-1.000000 ogd_regret=3.500000 ogd_bound=3.750000 adaptive_T=6 adaptive_regret=3.000000
TRACK B mistakes=2 final_w=1.000000,1.000000 R=1.414214 gamma=0.707107 mistake_bound=4.000000 progress=1.414214 norm=1.414214 boost_errors=0.250000,0.333333 alphas=0.549306,0.346574 Z=0.866025,0.942809 product=0.816497 training_error=0.250000 min_margin=-0.202733
TRACK C T=4 random_risk=0.250000 comparator=0.100000 online_regret=0.600000 excess=0.150000 radius=0.611937 ucb=1.183198,1.324766 ucb_choice=2 ips=0.000000,0.000000,4.500000 target_risk=0.700000 observed_estimate=2.700000 ips_variance=1.019200 max_ratio=3.000000
```

Canonical SVG SHA-256：

```text
2c61d35ce6dc1acedec1e6e62dea4ca62797ece325edc4787ca06eb055c45181
```

> [!important] 状态边界
> 详解、stdout 和哈希可复现只证明题卷材料自洽。它们不是学习者的口试、闭卷、blind 或延迟迁移证据；个人状态仍为 `not-attempted`。
