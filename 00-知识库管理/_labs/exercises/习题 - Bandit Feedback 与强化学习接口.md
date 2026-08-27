---
type: exercise
status: draft
topic: "[[Bandit Feedback 与强化学习接口]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Bandit Feedback 与强化学习接口]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Bandit Feedback 与强化学习接口
## A
### LT-BND-A01
写 stochastic、adversarial 与 contextual bandit 的 protocol/comparator。
### LT-BND-A02
区分 realized regret、pseudo-regret 与 best-arm identification。
### LT-BND-A03
说明 bandit 与 MDP/RL 在 state、transition、horizon 和 credit 上的区别。
## B
### LT-BND-B01
$p=(0.8,0.2)$，采到 arm 2、loss 0.6，求 IPS loss vector 与其该坐标二阶矩。
### LT-BND-B02
两臂均值 $(0.7,0.5)$，期望抽 arm 2 共 30 次，求 pseudo-regret。
### LT-BND-B03
若 $K=10,T=10^4$，比较忽略常数的 $\sqrt{T\log K}$ 与 $\sqrt{TK\log K}$。
## C
### LT-BND-C01
证明 inverse-propensity loss estimator 条件无偏，并推导二阶矩。
### LT-BND-C02
由 $\overline R_T=\sum_i\Delta_iE[N_i(T)]$ 解释 stochastic regret 分解。
### LT-BND-C03
构造无 exploration 导致永久选错 arm 的正概率事件。
## D
### LT-BND-D01
审计把 UCB 直接用于 adversarial reward sequence 的报告。
### LT-BND-D02
offline logger 从不选择某类用户的 action 3。能否评价 target policy 在该类用户上选 action 3？
### LT-BND-D03
推荐会改变用户未来兴趣。为什么 contextual-bandit static regret 不足？
## E
### LT-BND-E01
为 LLM routing 选择 full-information、contextual bandit 或 RL，并给判据。
### LT-BND-E02
设计 reward regret、constraint cost、baseline 与 human override 的安全探索合同。
### LT-BND-E03
写 bandit/RL claim card：feedback、propensity、environment、comparator、horizon、overlap 与 safety。
