---
type: exercise
status: draft
area: [learning-theory/transfer-learning, linear-probe, fine-tuning, evaluation]
topic: "[[Linear Probe、Fine-Tuning 与迁移评估]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Linear Probe、Fine-Tuning 与迁移评估]]"]
related: ["[[解答 - Linear Probe、Fine-Tuning 与迁移评估]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
solution: "[[解答 - Linear Probe、Fine-Tuning 与迁移评估]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Linear Probe、Fine-Tuning 与迁移评估

> [!abstract] 训练目标
> 能区分 oracle/finite probe 与 fine-tuning estimand，用反例解释 linear accessibility，设计 label/head/compute/task/shift 矩阵，并对 selection、uncertainty 与 compute fairness 做严格审计。

## A. 识别与复述

### LT-TRN-A01

分别定义 oracle linear risk、finite-label probe risk 与 finite-budget fine-tuning risk；每个对象有哪些随机性？

### LT-TRN-A02

列出 zero-shot、kNN、linear probe、partial fine-tune、full fine-tune 与 scratch 的更新参数、主要 estimand 和主要混杂。

### LT-TRN-A03

判断并解释：“linear probe 低说明标签信息不存在”“fine-tuning 高说明 frozen representation 好”“upstream accuracy 高说明所有任务迁移好”。

## B. 手算与局部推导

### LT-TRN-B01

把 finite probe excess risk 分为 representation approximation、head estimation、optimization 与 selection 四项；说明哪些项可通过增加 labels、steps 或 richer head 改善。

### LT-TRN-B02

对 $X_i\in\{-1,+1\}$ 与 $Y=X_1X_2$，分别求 $(X_1,X_2)$ 上 homogeneous linear classifier 与含 bias 的 affine classifier 的最佳错误率；再证明加入 feature $X_1X_2$ 后线性可分。

### LT-TRN-B03

给定三个 compute budgets 下 scratch risks $(0.35,0.20,0.12)$、pretrained risks $(0.20,0.15,0.12)$，计算 transfer gains 并判断主要是 speedup 还是 persistent gain。

## C. 证明与反例

### LT-TRN-C01

证明若 $h_2=Ah_1$ 且 $A$ 可逆，affine-head oracle risk 不变。为什么一般 nonlinear invertible $\phi$ 不保持 linear risk？

### LT-TRN-C02

构造两个表示：A 在线性 probe 上更好，B 在 full fine-tune 上更好。给出可能的数据几何与优化原因，说明排序反转不矛盾。

### LT-TRN-C03

证明在同一 test set 上从 $K$ 个 layers 与 $M$ 个 regularization values 中取最高分会产生 optimistic selection；给出 nested validation 的数据流。

## D. 审计与诊断

### LT-TRN-D01

设计 task × protocol × label budget × shift × compute × seed 的 transfer matrix；哪些 axes 可随机化，哪些必须预注册？

### LT-TRN-D02

两个模型在相同 10 个 downstream splits 上比较。说明为何 paired difference 优于分别计算两个独立区间，并给出 task-level aggregation 方案。

### LT-TRN-D03

报告 A 用 100 epochs full fine-tune，B 用 100 epochs linear probe，便声称 A 的表示更好。列出 compute、trainable parameters、search、preprocessing 与 estimand 层面的不公平。

## E. 研究与迁移

### LT-TRN-E01

为通用图像 encoder 设计包含分类、定位、分割、OCR 与 pose 的 transfer benchmark；规定 frozen、adapter、full、scratch 和 shift protocols。

### LT-TRN-E02

为 LLM hidden states 设计“属性是否可读”的 probe 研究。如何控制 probe capacity、token position、memorization、causal intervention 与 multiple testing？

### LT-TRN-E03

写一份 foundation-model transfer claim card：给出允许的最强结论、必要证据、negative-transfer 报告和哪些结论必须明确拒绝。
