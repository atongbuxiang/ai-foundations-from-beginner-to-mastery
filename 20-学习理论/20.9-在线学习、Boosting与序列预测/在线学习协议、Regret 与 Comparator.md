---
type: theorem
status: draft
area: [learning-theory/online-learning, regret, sequential-prediction]
aliases: [Online Learning Protocol, External Regret, Hannan Consistency]
node_id: LT-69
prerequisites: ["[[统计学习问题的对象合同]]", "[[损失、总体风险与经验风险]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[Experts、Weighted Majority 与 Multiplicative Weights]]", "[[Online Gradient Descent 与 Mirror Descent]]", "[[Online-to-Batch Conversion]]", "[[Bandit Feedback 与强化学习接口]]"]
sources: ["[[S-2006-CesaBianchi-Lugosi-Prediction-Games]]", "[[S-2012-Shalev-Online-Learning-OCO]]", "[[S-2015-Rakhlin-Sequential-Complexities]]"]
exercises: ["[[习题 - 在线学习协议、Regret 与 Comparator]]"]
solutions: ["[[解答 - 在线学习协议、Regret 与 Comparator]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-online-protocol-regret-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 在线学习协议、Regret 与 Comparator

> [!abstract] 本章主问题
> 在线学习不先假设一份固定 iid distribution，而是逐轮规定谁先行动、谁看到什么、何时揭示 loss。regret 不问“是否恢复真参数”，而问算法累计损失比一个预先声明的 hindsight comparator 多多少。

## 一、学习目标

完成本章后，应能：

1. 写出完整 full-information online protocol；
2. 区分 action、decision、prediction 与 loss vector；
3. 定义 static external regret 与 average regret；
4. 解释 comparator 为何在事后选择却不随时间切换；
5. 区分 regret、mistake、population risk 与 optimization error；
6. 说明 regret 可为负；
7. 区分 full、bandit 与 partial feedback；
8. 说明 randomized algorithm 的 expectation 对谁取；
9. 识别 policy regret、dynamic regret 等不同 benchmark；
10. 为真实序列系统建立 filtration/data contract。

## 二、最小 Full-Information Protocol

给决策集 $\mathcal W$。第 $t=1,\ldots,T$ 轮：

1. learner 根据历史 $H_{t-1}$ 选择 $w_t\in\mathcal W$；
2. environment 揭示 loss function $\ell_t:\mathcal W\to\mathbb R$；
3. learner 承受 $\ell_t(w_t)$；
4. full information 下观察整函数/足够计算所有 actions loss 的信息。

关键顺序是 learner 选 $w_t$ 时不能看当前 $\ell_t$；否则问题退化为逐轮最小化。

## 三、带 Context 的预测协议

监督式在线预测常写为：

1. environment 给 $x_t$；
2. learner 给 $\widehat y_t$ 或 distribution；
3. environment 给 $y_t$；
4. 承受 $\ell(\widehat y_t,y_t)$ 并更新。

此时 $x_t$ 可在预测前看到，而 $y_t$ 不可。把“当前有哪些变量已知”写进 filtration，比笼统说 online 更重要。

## 四、Static External Regret

对 comparator class $\mathcal U\subseteq\mathcal W$：

$$
\boxed{
\operatorname{Reg}_T(\mathcal U)
=
\sum_{t=1}^T\ell_t(w_t)
-
\inf_{u\in\mathcal U}
\sum_{t=1}^T\ell_t(u).
}
$$

右边的 $u$ 在看完整序列后选择，但必须用同一个 $u$ 服务所有轮次。它是“best fixed action in hindsight”，不是每轮 oracle。

## 五、为什么 Comparator 必须声明

若 comparator 是单一常数 action，regret 容易；若允许任意 sequence $u_{1:T}$：

$$
\sum_t\ell_t(w_t)-\inf_{u_{1:T}}\sum_t\ell_t(u_t),
$$

环境可每轮让另一个 action 最优，learner 在看 loss 前无法普遍追上。可学习性来自限制 comparator 的容量、路径长度、switch 次数或 policy class。

## 六、No-Regret 与 Hannan Consistency

若

$$
\operatorname{Reg}_T=o(T),
$$

则平均 regret

$$
\frac{\operatorname{Reg}_T}{T}\to0.
$$

这说明长期平均损失不劣于 best fixed comparator；不说明最后一步 loss 小、不说明每个前缀都好，也不说明恢复真实 mechanism。

## 七、Regret 可以为负

两个 actions，loss sequence 交替：

$$
(0,1),(1,0),(0,1),(1,0),\ldots
$$

best fixed action 平均 loss $1/2$。若 learner 能利用可见结构在每轮选下一最优 action，总 loss 可接近 0，regret 为负。regret 是相对 benchmark 的差，不是非负 distance。

## 八、Regret 与 Population Risk

batch 统计学习：

$$
R(f)=E_{(X,Y)\sim P}\ell(f(X),Y)
$$

依赖 distribution $P$。online regret 对任意允许 loss sequence 给 pathwise/expected comparison。二者通过 online-to-batch、stochastic assumptions 或 martingale concentration 连接，不能直接替换符号。

## 九、Regret 与 Optimization Error

offline optimization 关心

$$
F(\widehat w)-\inf_wF(w).
$$

online regret 的函数 $\ell_t$ 随轮变化，$w_t$ 在当前函数揭示前选择。把同一个 objective 重复 $T$ 次可把 OCO algorithm 变成 optimization method，但 object contract 已改变。

## 十、四种 Feedback

| feedback | 轮后观察 | 难度 |
|---|---|---|
| full information | 全 loss vector/function | experts/OCO |
| gradient | $\nabla\ell_t(w_t)$ | first-order OCO |
| bandit | 只看 $\ell_t(w_t)$ | 需探索/importance estimate |
| delayed/censored | 晚到或部分 label | filtration/credit 更复杂 |

同一个 update 在不同 feedback 下可能不可实现。

## 十一、Randomized Learner

learner 选择 distribution $p_t$，再采样 $I_t\sim p_t$。expected regret：

$$
E_{\xi}
\left[
\sum_t\ell_t(I_t)
-
\min_i\sum_t\ell_t(i)
\right].
$$

必须说明 loss sequence 是否在随机种子前固定、是否可依赖过去 actions，以及 comparator 是否也随机。

## 十二、High-Probability Regret

若 conditional expected loss 为

$$
\bar\ell_t=E[\ell_t(I_t)\mid H_{t-1}],
$$

则 realized–expected difference 常形成 martingale difference。Azuma/Freedman 可把 expected bound 升级为 high probability，但需要 bounded increments/conditional variance 与 non-anticipating adversary。

## 十三、其他 Comparator

- internal/swap regret：替换某 action 的规则；
- dynamic regret：对变化 comparator $u_t$；
- shifting experts：限制 switch 次数；
- policy regret：考虑 learner action 改变未来 losses；
- adaptive regret：每个 time interval 的局部 regret。

它们不是 static regret 的“更多指标”，而是不同学习问题。

## 十四、一个两专家手算

losses：

$$
\ell_1=(0,1),\quad
\ell_2=(1,1),\quad
\ell_3=(1,0).
$$

若 learner actions 为 $(1,1,2)$，累计 loss $0+1+0=1$。专家 1 累计 2，专家 2 累计 2，因此 regret $=-1$。算法利用切换超过 best fixed expert，不矛盾。

## 十五、图：Protocol 先于 Bound

先看图回答：若 environment 在 learner 抽到 action 后才设置当前 loss，原 static-regret theorem 哪一步失效？

![[00-知识库管理/_assets/figures/learning-theory/fig-online-protocol-regret-v2.svg|900]]

> [!figure] 图 20.9-01　在线时序、comparator 与 feedback
> 左栏给出 history→decision→loss→feedback；中栏分开 cumulative learner loss 与 best fixed hindsight comparator；右栏展示 feedback、随机化与替代 regret。来源：依据 Cesa-Bianchi–Lugosi、Shalev-Shwartz 与 Rakhlin–Sridharan–Tewari 独立绘制；由 [[plot_online_learning_v2.py]] 确定性生成。

**怎样读图**：先锁定每轮可见信息，再写 comparator 和概率量词，最后选择 algorithm/bound。

**图没有证明什么**：图没有证明任意 adaptive environment 下都可 no-regret，也没有把 static regret 等同于 dynamic/policy regret。

## 十六、AI 接口

- 推荐/广告：action 改变未来反馈，static regret 可能不够；
- LLM serving：prompt/query sequence 可自适应选择，feedback 延迟；
- continual learning：distribution drift 与 comparator path length；
- monitoring agents：多次查看/干预使 sequence 非 iid。

## 十七、常见错误

1. 不写行动顺序；
2. comparator 每轮切换却仍称 static；
3. expected bound 不说明随机性；
4. full-information update 用在 bandit feedback；
5. no-regret 外推最后一步好；
6. regret 当 population generalization；
7. environment 看当前 coin 后仍套 oblivious theorem；
8. feedback loop 仍用 exogenous loss sequence。

## 十八、最小记忆与掌握标准

> [!summary]
> - protocol 决定 theorem；
> - static regret 比 best fixed action in hindsight；
> - $o(T)$ 意味平均差趋零；
> - comparator 越强，必须增加结构限制；
> - feedback 与 adversary information 决定可实现算法；
> - risk、optimization gap 与 regret 不可混写。

能写协议（A）、手算 regret（B）、构造 comparator/adversary 反例（C）、审计 filtration（D），并把真实 AI feedback 映射到正确 regret（E）。

## 十九、练习与独立详解

- [[习题 - 在线学习协议、Regret 与 Comparator]]
- [[解答 - 在线学习协议、Regret 与 Comparator]]

## 参考来源

- [[S-2006-CesaBianchi-Lugosi-Prediction-Games]]
- [[S-2012-Shalev-Online-Learning-OCO]]
- [[S-2015-Rakhlin-Sequential-Complexities]]
