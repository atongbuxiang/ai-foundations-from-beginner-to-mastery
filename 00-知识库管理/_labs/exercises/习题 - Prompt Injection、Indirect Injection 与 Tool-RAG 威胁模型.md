---
type: exercise
status: verified
area: [language-models, security, prompt-injection, tools]
topic: "[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"
solution: "[[解答 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型

## A. 识别与复述

### LM67-A01
区分 direct injection、indirect injection 与 jailbreak。

### LM67-A02
写出 threat model 六元组的每个分量，并解释攻击预算为何属于定义。

### LM67-A03
解释 semantic authority 与 execution authority 的区别。

## B. 手算与构造

### LM67-B01
一个静态测试中 200 个 attack cases 有 18 个达到后果，300 个 benign cases 有 276 个正常完成。计算 ASR 与 benign utility。

### LM67-B02
若理想化地认为单次独立攻击成功率 $p=.03$，计算 20 次内至少一次成功的概率；说明它只能作什么基线。

### LM67-B03
为“读文档并草拟邮件、但不得自动发送”的助手画文字版数据流，标出至少三个 trust boundaries。

## C. 推导与证明

### LM67-C01
说明为什么让模型在输出中声明“已检查安全”不能成为独立 reference monitor。

### LM67-C02
构造一个服务端 allow predicate，包含 identity、schema、scope、policy 和 confirmation，并说明短路顺序。

### LM67-C03
证明“全部拒绝外部文档”可使 ASR 降低却不能称为优良防御。

## D. 边界、反例与纠错

### LM67-D01
反驳“system role 优先级更高，所以 prompt injection 已被模板解决”。

### LM67-D02
一个过滤器删除所有包含某些祈使词的文档。指出两类假阳性和两类假阴性来源。

### LM67-D03
模型只能调用 read-only 搜索工具，且返回经签名。说明仍存在的风险与已降低的风险。

## E. AI 迁移

### LM67-E01
为 Tool-RAG 写最小 least-privilege control stack。

### LM67-E02
设计固定攻击集与 adaptive red team 的分离协议，不写任何可复用载荷。

### LM67-E03
为一次被拒绝和一次被执行的工具提案设计审计日志 schema。

独立完成后查看[[解答 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]。
