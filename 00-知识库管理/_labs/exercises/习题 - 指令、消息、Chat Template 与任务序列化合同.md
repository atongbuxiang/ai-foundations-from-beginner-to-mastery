---
type: exercise
status: verified
area: [language-models, instruction-tuning, chat-template]
topic: "[[指令、消息、Chat Template 与任务序列化合同]]"
solution: "[[解答 - 指令、消息、Chat Template 与任务序列化合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 指令、消息、Chat Template 与任务序列化合同

## A. 识别与复述

### LM25-A01
区分语义任务、结构化 messages、rendered text、token IDs 与 generation boundary。

### LM25-A02
为什么 Chat Template 是模型接口/编译器，而非纯排版？

### LM25-A03
区分 add-generation-prompt 与 continue-final-message。

## B. 手算与构造

### LM25-B01
给模板 BOS + 每条 role:content + EOT，手工编译 system=s、user=q、assistant=a，并标回答起点。

### LM25-B02
模板已输出 BOS/EOS，tokenizer 又自动加各一个；写最终控制 token 序列并指出错误。

### LM25-B03
构造 assistant tool-call→tool result→assistant final 的最小合法状态路径。

## C. 推导与证明

### LM25-C01
写消息到输出消息的 compiler–model–parser 复合，并列各版本参数。

### LM25-C02
给出 train-prefix 与 inference-prefix 相等的可执行不变量。

### LM25-C03
说明 rendered string 相同为何仍未必能证明 token 序列相同。

## D. 边界、反例与纠错

### LM25-D01
反驳“模型名相同，所以换 chat template 不影响比较”。

### LM25-D02
构造 role marker 出现在 content 中导致未转义 parser 混淆的例子。

### LM25-D03
反驳“保存最终 prompt 字符串即可完整复现消息系统”。

## E. AI 迁移

### LM25-E01
设计 template golden-ID、round-trip 与 version-diff 测试。

### LM25-E02
审计只公布 system prompt、未公布模板/tokenizer/flags 的评测。

### LM25-E03
为带 tool schema 的多轮训练样本写最小 manifest。

独立完成后查看[[解答 - 指令、消息、Chat Template 与任务序列化合同]]。

