---
type: exercise
status: draft
area: [architecture, transformer, decoder, autoregressive]
topic: "[[Transformer Decoder 与自回归因果结构]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Transformer Decoder 与自回归因果结构]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Transformer Decoder 与自回归因果结构

## A. 识别与复述

### ARCH-DEC-A01
写出长度 $T$ 序列的自回归概率分解，并说明 teacher forcing 输入如何右移。

### ARCH-DEC-A02
区分训练时行并行、生成时 token 串行与统计因果性。

### ARCH-DEC-A03
说明 KV cache 保存什么、没有保存什么，以及它不改变的语义。

## B. 手算与建模

### ARCH-DEC-B01
对 tokens [A,B,C,D] 写出 BOS 右移输入、targets 与 $4\times4$ inclusive causal mask。

### ARCH-DEC-B02
对 $L=24,B=2,T=1024,d_{kv}=1024$、FP16 cache，计算 K/V 标量数与字节数（忽略元数据）。

### ARCH-DEC-B03
一条 chat 样本含 system 2 token、user 3 token、assistant 4 token。若只监督 assistant，写出 9 个位置的 loss mask，并说明 attention mask 是否相同。

## C. 推导与证明

### ARCH-DEC-C01
证明正确 causal mask 下，第 $i$ 行输出对任何 $j>i$ 的 value 扰动不变。

### ARCH-DEC-C02
给出 full causal forward 与逐步 cached decoding logits 等价所需的条件。

### ARCH-DEC-C03
比较无 cache 重算 prefix 与有 cache 逐步生成 $S$ 个 token 的主要 attention pair 累计阶。

## D. 边界、反例与纠错

### ARCH-DEC-D01
构造未右移但保留 inclusive diagonal 的标签泄漏例子。

### ARCH-DEC-D02
构造 packed sequence 未做 block isolation 导致跨样本泄漏的例子。

### ARCH-DEC-D03
反驳：“Teacher-forcing loss 很低，所以 free-running 长生成必然可靠。”

## E. AI 迁移

### ARCH-DEC-E01
写一个 future-pulse、full-vs-cache、cache-reset 三部分 decoder 测试套件。

### ARCH-DEC-E02
为 beam search 的 cache reorder 写 shape/索引不变量和最小测试。

### ARCH-DEC-E03
为一个自回归服务写语义—性能双账，覆盖 position offset、dtype、cache 与 sampling。

## 解答入口

[[解答 - Transformer Decoder 与自回归因果结构]]
