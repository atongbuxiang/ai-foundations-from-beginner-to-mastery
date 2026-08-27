---
type: exercise
status: verified
area: [language-models, safety, jailbreak, bias, red-teaming]
topic: "[[Jailbreak、Toxicity、Bias 与安全评估]]"
solution: "[[解答 - Jailbreak、Toxicity、Bias 与安全评估]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Jailbreak、Toxicity、Bias 与安全评估

## A. 识别与复述

### LM68-A01
区分 policy violation、content property、system action 与 realized harm。

### LM68-A02
列出一个 jailbreak 结果必须绑定的五项 threat/evaluation 条件。

### LM68-A03
解释 toxicity classifier score 为什么不等于真实伤害概率。

## B. 手算与构造

### LM68-B01
有 120 个 harmful 请求，其中 102 个拒答；有 300 个 benign 请求，其中 42 个误拒。计算 harmful recall、unsafe answer rate、benign utility 与 over-refusal。

### LM68-B02
三个 prompt family 各有 5、20、100 个变体，成功数分别为 1、4、10。计算 query-micro ASR 与 family-macro ASR。

### LM68-B03
为歧义/消歧 bias 测试构造一个不含敏感群体实例的抽象二乘二表，并说明各格诊断什么。

## C. 推导与证明

### LM68-C01
说明同一 prompt family 的多个变体为何不能当独立样本估计极窄区间。

### LM68-C02
证明只优化 harmful recall 会把“全拒绝”作为一个最优解。

### LM68-C03
解释 max-over-$k$ toxicity 与 mean toxicity 为什么测不同 estimand。

## D. 边界、反例与纠错

### LM68-D01
构造“低 toxicity 但高 harm”与“高 toxicity score 但低 harm”的例子。

### LM68-D02
反驳“模型在公开 safety benchmark 上 99%，因此已经安全上线”。

### LM68-D03
模型文字拒答，但工具日志显示动作已执行。安全标签应如何记，为什么？

## E. AI 迁移

### LM68-E01
设计一个含语言、攻击族、工具权限与 severity 的红队矩阵。

### LM68-E02
为 LLM judge 安全判定设计人类锚点和交换/盲化审计。

### LM68-E03
写一次防御更新的版本化 adaptive evaluation 流程。

独立完成后查看[[解答 - Jailbreak、Toxicity、Bias 与安全评估]]。
