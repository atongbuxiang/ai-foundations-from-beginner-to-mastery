---
type: exercise
status: verified
area: [language-models, tokenization, information-theory]
topic: "[[Tokenizer 作为码本、分段路径与压缩接口]]"
solution: "[[解答 - Tokenizer 作为码本、分段路径与压缩接口]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Tokenizer 作为码本、分段路径与压缩接口

## A. 识别与复述

### LM03-A01
解释 tokenizer 七元组 $(N,\Sigma,V,C,A,id,D)$。

### LM03-A02
区分完备覆盖、返回 UNK 与无损 round-trip。

### LM03-A03
为什么同一个词表集合不能唯一确定 encode？

## B. 手算与构造

### LM03-B01
$V=\{a,b,c,ab,bc,abc\}$，枚举 `abc` 的全部合法分段路径。

### LM03-B02
语料 1200 bytes，A 输出 400 tokens，B 输出 300 tokens。算 bytes/token 与 tokens/byte；词表分别 256、1024 时算固定宽 ID 下界。

### LM03-B03
模型 $d=512$，untied input/output embedding。词表从 32k 增到 50k，新增多少参数？

## C. 推导与证明

### LM03-C01
证明确定可逆 tokenizer 下 $p_X(x)=p_Z(A(x))$，并指出随机/多对一时为何失效。

### LM03-C02
推导 BPB 与自然对数序列 NLL 的换算。

### LM03-C03
若 token 长度从 $T$ 降为 $rT$，写 dense attention pairwise 项与线性项的缩放，不夸大总 FLOPs。

## D. 边界、反例与纠错

### LM03-D01
构造 normalize 后 round-trip 成立但原始 bytes round-trip 失败的例子。

### LM03-D02
反驳“token 越少 tokenizer 越好”。

### LM03-D03
反驳“token perplexity 更低所以跨 tokenizer 更好”。

## E. AI 迁移

### LM03-E01
写 tokenizer model card 的最小字段。

### LM03-E02
设计固定 raw bytes 与固定 token budget 两种模型比较，说明 estimand 差异。

### LM03-E03
为代码、中文、emoji 混合语料设计 coverage 与 tail-length 审计。

独立完成后查看[[解答 - Tokenizer 作为码本、分段路径与压缩接口]]。

