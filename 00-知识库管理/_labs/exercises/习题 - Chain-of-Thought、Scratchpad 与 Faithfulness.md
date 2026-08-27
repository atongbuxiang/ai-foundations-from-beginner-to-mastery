---
type: exercise
status: verified
area: [language-models, reasoning, faithfulness]
topic: "[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"
solution: "[[解答 - Chain-of-Thought、Scratchpad 与 Faithfulness]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Chain-of-Thought、Scratchpad 与 Faithfulness

## A. 识别与复述

### LM37-A01
区分 outcome correctness、local validity、executable sufficiency 与 causal faithfulness。

### LM37-A02
列出 CoT 可能提升表现的五种机制假说。

### LM37-A03
为什么可见 CoT 不等于模型全部内部计算？

## B. 手算与构造

### LM37-B01
写出 $p(r,y\mid x)$ 的链式分解和对 $r$ 的边缘化。

### LM37-B02
构造最终答案正确但 reasoning chain 不支持答案的最小例子。

### LM37-B03
给 truncate、paraphrase、error injection 各设计一个控制变量。

## C. 推导与证明

### LM37-C01
说明 greedy CoT 为什么不等于对全部 reasoning paths 边缘化。

### LM37-C02
形式化对可见 trace 的答案依赖干预。

### LM37-C03
说明可执行形式链保证的起点和终点，指出自然语言解析仍留下的错误界面。

## D. 边界、反例与纠错

### LM37-D01
反驳“准确率提升证明 CoT 忠实”。

### LM37-D02
构造流畅、局部合理但遗漏 bias cue 的解释。

### LM37-D03
审计一个 direct 与 CoT 未匹配 token 预算的实验。

## E. AI 迁移

### LM37-E01
设计 bias cue 的 answer flip × mention rate 审计。

### LM37-E02
设计 short/long/structured/scrambled/filler 的预算对照。

### LM37-E03
为高风险系统设计 trace、外部证据与确定性检查分账。

独立完成后查看[[解答 - Chain-of-Thought、Scratchpad 与 Faithfulness]]。
