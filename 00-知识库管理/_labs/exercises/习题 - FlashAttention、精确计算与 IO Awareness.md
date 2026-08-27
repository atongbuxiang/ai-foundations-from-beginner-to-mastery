---
type: exercise
status: draft
area: [architecture, efficient-attention, flashattention, systems]
topic: "[[FlashAttention、精确计算与 IO Awareness]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - FlashAttention、精确计算与 IO Awareness]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - FlashAttention、精确计算与 IO Awareness

## A. 识别与复述

### ARCH-FLASH-A01
说明 naive attention 为什么会把 scores/probabilities 作为大型中间量写入 HBM。

### ARCH-FLASH-A02
FlashAttention 的“exact”指什么？它不意味着哪些更强的等价性？

### ARCH-FLASH-A03
写出 online softmax 需要维护的行状态 $(m,\ell,u)$ 及输出关系。

## B. 手算与建模

### ARCH-FLASH-B01
对 scores $(1,3,-2)$ 与 scalar values $(2,4,10)$，用两个 tiles $(1,3)$、$(-2)$ 手算 online merge，并与 dense softmax 输出比较。

### ARCH-FLASH-B02
若 $B=2,h=16,n=4096$、每标量 2 bytes，计算只保存 score tensor 需要多少 GiB；说明这还未计什么。

### ARCH-FLASH-B03
给定两个块状态 $(m_1,\ell_1,u_1)$、$(m_2,\ell_2,u_2)$，写出通用合并公式。

## C. 推导与证明

### ARCH-FLASH-C01
证明 online merge 后的 $(m,\ell,u)$ 与把两个 score/value 块拼接后直接计算的稳定 softmax 状态相同。

### ARCH-FLASH-C02
解释 backward 如何通过保存 log-sum-exp/输出并重算局部 scores，换取更少 activation storage；列出被交换的成本。

### ARCH-FLASH-C03
从“每个 output row 都依赖所有 keys”说明 FlashAttention 没把 dense attention 的 pairwise 算术变成 $O(n)$。

## D. 边界、反例与纠错

### ARCH-FLASH-D01
反驳：“exact 算法应与 naive 实现逐 bit 相同。”

### ARCH-FLASH-D02
构造一个 shape 很小或 layout 不利，使 kernel launch/transpose 开销抵消 IO 优势的场景。

### ARCH-FLASH-D03
解释 causal mask、padding mask、dropout 与 variable-length packing 各会给 correctness contract 增加什么状态。

## E. AI 迁移

### ARCH-FLASH-E01
写一套 forward/backward 正确性测试，覆盖极端 logits、不同 dtype、mask、非整 tile 长度与 dropout。

### ARCH-FLASH-E02
设计性能 benchmark，区分 kernel 时间、端到端时间、峰值显存、HBM throughput 与 achieved FLOPs。

### ARCH-FLASH-E03
审查一个声称“用了 FlashAttention 所以上下文长度无限”的系统结论，列出至少五个仍随长度增长的资源或风险。

## 解答入口

[[解答 - FlashAttention、精确计算与 IO Awareness]]
