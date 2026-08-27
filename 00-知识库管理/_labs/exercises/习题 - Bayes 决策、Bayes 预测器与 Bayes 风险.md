---
type: exercise
status: draft
area: [learning-theory/foundations, statistical-decision-theory]
topic: "[[Bayes 决策、Bayes 预测器与 Bayes 风险]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[损失、总体风险与经验风险]]", "[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[解答 - Bayes 决策、Bayes 预测器与 Bayes 风险]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
solution: "[[解答 - Bayes 决策、Bayes 预测器与 Bayes 风险]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - Bayes 决策、Bayes 预测器与 Bayes 风险

> [!abstract] 训练目标
> 从条件分布和 loss 推导最优 action；分清 posterior estimation、Bayes decision、Bayesian inference 与现实部署成本。

## A. 识别与复述

### LT-BAY-A01

定义 conditional risk、Bayes decision rule 与 Bayes risk。它们分别依赖哪些对象？

### LT-BAY-A02

区分 Bayes classifier、Bayesian parameter posterior、posterior predictive 与 MAP parameter。

### LT-BAY-A03

分别写出 0–1、平方、绝对、log loss 下的 Bayes action。

## B. 手算与构造

### LT-BAY-B01

某输入处 $\eta(x)=0.3$。计算 0–1 loss 下预测 0/1 的条件风险与 Bayes action。若 $c_{FP}=2,c_{FN}=8$，重新计算成本敏感动作。

### LT-BAY-B02

误分类成本为 1、abstain 成本为 $c=0.2$。对 $\eta=0.1,0.35,0.85$ 分别给出 Bayes action 与条件风险。

### LT-BAY-B03

三分类条件分布 $p=(0.2,0.5,0.3)$。计算 0–1 Bayes action/risk；再比较概率预测 $q_1=p$ 与 $q_2=(0.1,0.7,0.2)$ 的 conditional log risk，并写出两者差值。

## C. 推导与证明

### LT-BAY-C01

用 tower property 证明：若 $h^*(x)$ 几乎处处最小化 $r(a\mid x)$，则 $h^*$ 最小化总体风险。

### LT-BAY-C02

完整推导平方损失的条件均值分解，并由此得到 Bayes risk $\mathbb E\operatorname{Var}(Y\mid X)$。

### LT-BAY-C03

证明多分类 conditional log risk 等于 $H(p)+\operatorname{KL}(p\|q)$。讨论 $p_k=0$ 或 $q_k=0<p_k$ 的边界。

## D. 边界、反例与纠错

### LT-BAY-D01

纠正：“Bayes predictor 必须通过给参数设置 prior 得到。”给出 frequentist probability estimator 也能逼近 Bayes decision 的解释。

### LT-BAY-D02

纠正：“Bayes error 是数据集永远无法降低的固有常数。”说明新增 observation、允许 abstain、改变 loss 或 population 会怎样改变它。

### LT-BAY-D03

构造一个模型 accuracy 很高但 posterior 概率严重失准的例子；说明为什么成本阈值决策会受损。

## E. AI 迁移

### LT-BAY-E01

为疾病筛查设计 probability-estimation + decision 两阶段系统，包含不对称成本、abstain、calibration 与 subgroup shift。

### LT-BAY-E02

解释 next-token log-loss Bayes target 与 LLM 最终 decoding/帮助性决策的不同。列出至少三个额外 action/loss 组件。

### LT-BAY-E03

一个风控模型输出违约概率。部署资源限制只允许复核 5% 用户。说明 pointwise Bayes threshold 为何还不够，并给出带全局约束的决策形式。

## 分级提示

- `B01`：成本阈值为 $2/(2+8)=0.2$；
- `B02`：在 $(c,1-c)$ 内拒绝；
- `B03`：log-risk 差等于 $\operatorname{KL}(p\|q_2)$；
- `C03`：约定 $0\log(0/q)=0$，而 $p>0,q=0$ 时风险无穷；
- `E03`：约束把各个 $x$ 的决策耦合起来，可用 Lagrange multiplier/排序。

## 解答入口

完成独立尝试后再打开：[[解答 - Bayes 决策、Bayes 预测器与 Bayes 风险]]。

