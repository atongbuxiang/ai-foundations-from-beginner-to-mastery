---
type: exercise
status: verified
area: [language-models, evaluation, llm-as-judge]
topic: "[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"
solution: "[[解答 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差

## A. 识别与复述

### LM62-A01
把 pairwise judge 写成依赖题目、答案、顺序、rubric 与随机性的测量函数。

### LM62-A02
定义位置一致率、交换翻转率、win rate 与 tie rate。

### LM62-A03
解释答案长度为什么既可能是质量 mediator，也可能是不相关偏差来源。

## B. 手算与构造

### LM62-B01
100 个配对各做 AB/BA 两次：70 对都选同一内容，20 对随位置翻转，10 对至少一次 tie。按题面约定计算 content-consistency、position-flip 与 tie-pair 比例。

### LM62-B02
A 胜 45、B 胜 35、tie 20。分别计算 ties 计半胜和排除 ties 的 A win rate。

### LM62-B03
judge 与人类在 80 个非 tie 配对上一致 60 次；两者各自的 A/B 标签比例都各半。计算 observed agreement 与在独立同边际假设下的 chance agreement。

## C. 推导与证明

### LM62-C01
写出 Bradley–Terry 模型的 pairwise 概率，并说明连通比较图为何关系到可识别性。

### LM62-C02
用因果路径 system→length→quality/judge 说明“回归中控制长度”可能改变 estimand。

### LM62-C03
说明随机交换答案位置如何识别平均位置效应，需要哪些稳定性假设。

## D. 边界、反例与纠错

### LM62-D01
构造 judge-human 总体 agreement 高但某安全 slice 极差的例子。

### LM62-D02
反驳“judge temperature=0 就没有测量误差”。

### LM62-D03
解释用同一个 judge 调 prompt、选 checkpoint 并最终报告 test win rate 的泄漏。

## E. AI 迁移

### LM62-E01
设计 AB/BA、匿名化、tie 与 parse failure 完整的 judge 审计表。

### LM62-E02
设计 length-matched sensitivity analysis，同时保留原始总效应。

### LM62-E03
设计小规模人类锚点研究，验证 judge 在语言、长度和安全 slices 上的可靠性。

独立完成后查看[[解答 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]。
