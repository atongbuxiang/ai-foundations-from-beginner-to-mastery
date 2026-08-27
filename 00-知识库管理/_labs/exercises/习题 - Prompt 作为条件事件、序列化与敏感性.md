---
type: exercise
status: verified
area: [language-models, prompting, in-context-learning]
topic: "[[Prompt 作为条件事件、序列化与敏感性]]"
solution: "[[解答 - Prompt 作为条件事件、序列化与敏感性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Prompt 作为条件事件、序列化与敏感性

## A. 识别与复述

### LM33-A01
区分任务语义、rendered bytes、token IDs 与输出 parser。

### LM33-A02
为什么语义等价 prompt 不保证条件概率相同？

### LM33-A03
区分 contextual calibration 与统计意义的概率 calibration。

## B. 手算与构造

### LM33-B01
标签 red fox 与 red panda 共享首 token；第二 token 条件概率为 0.7 与 0.2。说明首 token scorer 和完整序列 scorer 的结果。

### LM33-B02
四个语义保持模板的逐样本翻转数为 0、3、2、1，总样本数各为 10；计算各翻转率与平均翻转率。

### LM33-B03
构造一个 bytes 相似但因前导空格得到不同 label token IDs 的最小 prompt manifest。

## C. 推导与证明

### LM33-C01
推导多 token verbalizer 的 log-prob，并解释长度归一化的协议地位。

### LM33-C02
证明准确率差为零不推出逐样本 prediction flip 为零。

### LM33-C03
写出尝试 $M$ 个模板后取最大验证分数的估计对象，并说明选择偏差来源。

## D. 边界、反例与纠错

### LM33-D01
反驳“UI 中看起来一样，所以模型输入一样”。

### LM33-D02
构造只比较 label 首 token 会平局或反转的反例。

### LM33-D03
审计一项只保存 prompt 字符串、不保存 tokenizer/template/parser 的实验。

## E. AI 迁移

### LM33-E01
设计 format、paraphrase、label 与 decoding 四轴 sensitivity sweep。

### LM33-E02
为 API 模型写最小可复现 prompt manifest。

### LM33-E03
设计配对 bootstrap 与预测翻转报告，避免只给最佳 prompt。

独立完成后查看[[解答 - Prompt 作为条件事件、序列化与敏感性]]。
