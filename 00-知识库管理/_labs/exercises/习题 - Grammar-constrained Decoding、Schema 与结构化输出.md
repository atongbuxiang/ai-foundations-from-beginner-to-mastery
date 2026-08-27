---
type: exercise
status: verified
area: [language-models, constrained-generation]
topic: "[[Grammar-constrained Decoding、Schema 与结构化输出]]"
solution: "[[解答 - Grammar-constrained Decoding、Schema 与结构化输出]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Grammar-constrained Decoding、Schema 与结构化输出

## A. 识别与复述

### LM53-A01
区分 $L$、$\operatorname{Pref}(L)$、accepting state 与 live state。

### LM53-A02
定义 token-level valid set $A(q)$，解释为何要读取完整 token bytes。

### LM53-A03
列出语法、schema、语义和行为安全四层保证。

## B. 手算与构造

### LM53-B01
目标语言只有字符串“ab”与“ac”。列出前缀闭包，并判断空串、“a”、“ab”、“ad”的 accepting/live 状态。

### LM53-B02
当前模型概率为“b”:.4、“c”:.3、“d”:.2、EOS:.1；parser 在前缀“a”只允许完成“ab”或“ac”。求 valid set、$Z$ 与约束后概率。

### LM53-B03
构造一个 token 首字符合法、但完整 token 会进入 dead end 的例子。

## C. 推导与证明

### LM53-C01
证明 mask-and-renormalize 在 $A(q)\ne\varnothing$ 时是合法概率分布。

### LM53-C02
构造反例，证明逐步局部合法 mask 一般不等于原模型对完整语言事件的条件分布。

### LM53-C03
说明如何由自动机反向可达性求 $Q_{\mathrm{live}}$。

## D. 边界、反例与纠错

### LM53-D01
反驳“通过 JSON Schema 就说明字段内容真实”。

### LM53-D02
审计只按 token 第一个 Unicode 字符过滤的约束器。

### LM53-D03
审计遇到空 valid set 后静默关闭 grammar 的 API。

## E. AI 迁移

### LM53-E01
为带金额与收款人的工具调用设计分层验证链。

### LM53-E02
为 grammar decoder 写 tokenizer/grammar/version 复现合同。

### LM53-E03
设计结构合法率与语义正确率分离的实验。

独立完成后查看[[解答 - Grammar-constrained Decoding、Schema 与结构化输出]]。
