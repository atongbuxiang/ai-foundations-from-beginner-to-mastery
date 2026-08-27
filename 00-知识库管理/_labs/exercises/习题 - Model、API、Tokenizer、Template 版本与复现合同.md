---
type: exercise
status: verified
area: [language-models, reproducibility, versioning]
topic: "[[Model、API、Tokenizer、Template 版本与复现合同]]"
solution: "[[解答 - Model、API、Tokenizer、Template 版本与复现合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Model、API、Tokenizer、Template 版本与复现合同

## A. 识别与复述

### LM70-A01
列出语言模型运行 bundle 的至少八个版本化组件。

### LM70-A02
解释 rendered text 相同与 token IDs 相同为什么都需分别核验。

### LM70-A03
区分 R0 工件复算、R1 同栈重放、R2 独立重实现与 R3 外部复验。

## B. 手算与构造

### LM70-B01
两个模板把同一三条消息分别编码为 47 和 52 tokens。若模型最大上下文为 50，说明这会造成哪些可观察差异。

### LM70-B02
原实验指标 $.812$，五次同栈重放为 $(.810,.813,.809,.814,.811)$。计算重放均值、最大绝对差，并按容差 $.005$ 判断。

### LM70-B03
构造一个 bundle manifest 的最小 JSON 字段表（只写字段，不必写代码）。

## C. 推导与证明

### LM70-C01
解释哈希的雪崩性为什么适合变更检测，却不能证明 artifact 正确或可信。

### LM70-C02
说明固定随机种子仍不能推出 GPU/API bitwise 复现。

### LM70-C03
把一次多组件供应商升级表示为 treatment bundle，说明为何不能归因到权重。

## D. 边界、反例与纠错

### LM70-D01
反驳“endpoint 名称没变，所以模型没变”。

### LM70-D02
构造“文本输出不同但任务结论复现”和“文本相同但系统结论未复现”的例子。

### LM70-D03
只保存最终平均分而不保存 raw outputs，会失去哪些复验能力？

## E. AI 迁移

### LM70-E01
为 chat template 写 golden test 集。

### LM70-E02
为无法固定 snapshot 的 API 设计可观察漂移 probe。

### LM70-E03
设计一次版本变更的影响分析与 release gate。

独立完成后查看[[解答 - Model、API、Tokenizer、Template 版本与复现合同]]。
