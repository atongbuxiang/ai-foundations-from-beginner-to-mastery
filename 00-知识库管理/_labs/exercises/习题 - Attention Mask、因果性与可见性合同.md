---
type: exercise
status: draft
area: [architecture, attention, masking]
topic: "[[Attention Mask、因果性与可见性合同]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Attention Mask、因果性与可见性合同]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Attention Mask、因果性与可见性合同

## A. 识别与复述

### ARCH-MASK-A01
把 attention mask 定义为二元关系，并写出 query $i$ 的可见集合。

### ARCH-MASK-A02
区分 key padding、query padding 与 causal mask 的轴和用途。

### ARCH-MASK-A03
解释 inclusive causal 与 strict causal 的差异，以及为何必须与 label shift 联合定义。

## B. 手算与建模

### ARCH-MASK-B01
画出长度 4 的 inclusive causal boolean mask（用 1 表示可见）。

### ARCH-MASK-B02
未屏蔽 softmax 权重为 $(0.5,0.3,0.2)$，第三项禁止。计算后乘 0 的结果与正确重归一结果。

### ARCH-MASK-B03
两个 batch 样本有效长度分别为 3、5，padding 到 5。写出 key padding mask shapes/内容和与 causal mask 合成后的可见条件。

## C. 推导与证明

### ARCH-MASK-C01
证明加 $0/-\infty$ mask 后 row-softmax 等价于只在可见集合上归一化。

### ARCH-MASK-C02
证明 inclusive causal softmax attention 在有限 diagonal logits 下严格满秩。

### ARCH-MASK-C03
证明若 self-attention 输入按 P 重排且 mask 同步变为 $PMP^\top$，输出等变；说明固定 causal mask 为何破坏任意置换对称。

## D. 边界、反例与纠错

### ARCH-MASK-D01
构造全遮蔽行，说明 stable softmax 为什么仍可能 NaN。

### ARCH-MASK-D02
反驳：“用 -1e9 填 mask 在所有 dtype/kernel 中都等价于 $-\infty$。”

### ARCH-MASK-D03
给出一个 causal attention 实现仍发生标签泄漏的非 attention 原因。

## E. AI 迁移

### ARCH-MASK-E01
写一个 future-pulse leakage test：输入怎样改、应比较哪些输出、通过标准是什么。

### ARCH-MASK-E02
为 block-sparse local+global attention 写可见关系与每行非空条件。

### ARCH-MASK-E03
设计 boolean convention、broadcast、padding、all-masked 与 shifted-label 的最小 mask test suite。

## 解答入口

[[解答 - Attention Mask、因果性与可见性合同]]
