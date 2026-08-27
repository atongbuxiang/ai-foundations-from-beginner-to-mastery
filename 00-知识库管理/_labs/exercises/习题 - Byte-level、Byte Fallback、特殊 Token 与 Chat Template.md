---
type: exercise
status: verified
area: [language-models, tokenization, special-tokens]
topic: "[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"
solution: "[[解答 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template

## A. 识别与复述

### LM07-A01
区分 fully byte-level、byte fallback 与 UNK。

### LM07-A02
列出 BOS/EOS/PAD/UNK/MASK/role token 的作用与一项非自动语义。

### LM07-A03
为什么 chat template 应看作编译器？

## B. 手算与构造

### LM07-B01
`中` 的 UTF-8 为 3 bytes。若无多 byte piece，fully byte-level 输出几个基本 token？Unicode piece 命中时又是多少？

### LM07-B02
把 system/user/assistant 两轮消息构造成一个含 role token、separator、generation prefix 的示意序列。

### LM07-B03
词表从 32,000 增加 8 个 special token，$d=4096$、tied embedding，新增多少参数；untied 呢？

## C. 推导与证明

### LM07-C01
证明 256-byte alphabet 加确定 decode 可覆盖任意有限 byte stream。

### LM07-C02
说明 PAD=EOS 时语义为何依赖 attention/loss/stop masks，而非仅 ID。

### LM07-C03
形式化 train template 与 inference template 不同如何造成条件分布 covariate shift。

## D. 边界、反例与纠错

### LM07-D01
反驳“special=True 就自动从 loss 移除”。

### LM07-D02
反驳“byte fallback 保证所有管线 byte-round-trip”。

### LM07-D03
构造用户字面 role token 被错误提升为控制 ID 的注入例子。

## E. AI 迁移

### LM07-E01
写 tokenizer/checkpoint/template 三方一致性断言。

### LM07-E02
设计双 BOS/EOS 与 left/right padding 回归测试。

### LM07-E03
为 tool output 中的特殊字符串、零宽字符和 invalid bytes 写 trust-boundary 处理协议。

独立完成后查看[[解答 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]。

