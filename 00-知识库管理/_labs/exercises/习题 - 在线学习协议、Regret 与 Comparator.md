---
type: exercise
status: draft
topic: "[[在线学习协议、Regret 与 Comparator]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 在线学习协议、Regret 与 Comparator]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 在线学习协议、Regret 与 Comparator
## A
### LT-ONL-A01
写 full-information online protocol，标出 learner 选择当前 action 时不可见的信息。
### LT-ONL-A02
定义 static external regret、average regret 与 no-regret。
### LT-ONL-A03
区分 population risk、offline optimization gap、mistake count 与 regret。
## B
### LT-ONL-B01
三轮两专家 losses 为 $(0,1),(1,1),(1,0)$，learner 选 $(1,1,2)$，计算 regret。
### LT-ONL-B02
算法 loss 为 $T/2-\sqrt T$，best fixed 为 $T/2$。regret 是否可为负？average regret 极限？
### LT-ONL-B03
给 $R_T\le3\sqrt T$，求保证 average regret ≤0.03 所需 $T$。
## C
### LT-ONL-C01
构造允许 comparator 每轮自由切换后，任何先行动 learner 都可能线性 regret 的两 action sequence。
### LT-ONL-C02
说明 static regret 为负不矛盾，并构造 learner 利用可预测切换超过所有 fixed actions。
### LT-ONL-C03
证明 full-information 与 bandit feedback 下同一 loss estimator 不可直接共用。
## D
### LT-ONL-D01
审计一个只写“adversarial regret”却未说明随机性、adversary 可见性和 comparator 的报告。
### LT-ONL-D02
推荐系统 action 改变未来 losses。为什么 external regret 的 hindsight comparator 不是完整 counterfactual？
### LT-ONL-D03
设计 delayed labels、clustered users 与 adaptive query 的 filtration。
## E
### LT-ONL-E01
为 LLM model routing 建 experts protocol、loss、feedback 与 comparator。
### LT-ONL-E02
为 continual deployment 选择 static、dynamic、shifting 或 policy regret，并说明理由。
### LT-ONL-E03
写 online-learning claim card：时序、feedback、adversary、randomness、comparator 与 guarantee。
