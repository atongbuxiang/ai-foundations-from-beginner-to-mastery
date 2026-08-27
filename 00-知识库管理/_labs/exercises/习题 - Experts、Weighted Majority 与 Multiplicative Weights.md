---
type: exercise
status: draft
topic: "[[Experts、Weighted Majority 与 Multiplicative Weights]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Experts、Weighted Majority 与 Multiplicative Weights]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Experts、Weighted Majority 与 Multiplicative Weights
## A
### LT-MW-A01
写 Hedge 初始化、prediction distribution、loss 与 update。
### LT-MW-A02
区分 deterministic Weighted Majority、randomized WM 与 Hedge。
### LT-MW-A03
potential proof 的 comparator 下界与 learner 上界分别是什么？
## B
### LT-MW-B01
$\eta=\log2$、weights $(1,1,1)$、loss $(0,1,1/2)$，求新 weights 与 probabilities。
### LT-MW-B02
最小化 $\log N/\eta+\eta T/8$，求 $\eta^*$ 与 bound。
### LT-MW-B03
priors $(1/2,1/3,1/6)$，写各专家 complexity term 并比较。
## C
### LT-MW-C01
从 Hoeffding lemma 完整证明 Hedge regret bound。
### LT-MW-C02
证明 loss 从 $[0,1]$ 缩放到 $[a,b]$ 后 regret 如何变化。
### LT-MW-C03
构造 adversary 看见 sampled action 后惩罚它，使 Hedge 线性 realized regret。
## D
### LT-MW-D01
未知 horizon 却使用 $\eta(T)$。用 doubling trick 修复并核算量级。
### LT-MW-D02
审计 data-dependent prior：何时 $\log(1/\pi_i)$ 解释失效？
### LT-MW-D03
只有 chosen expert loss 时，为什么 full-information Hedge update不可实现？
## E
### LT-MW-E01
为多模型服务路由设计 latency+quality loss 与专家失效处理。
### LT-MW-E02
把 entropy-FTRL objective 推到 exponential weights。
### LT-MW-E03
写 MW claim card：range、horizon、prior、feedback、adversary 与 comparator。
