---
type: exercise
status: draft
area: [neural-networks/embedding-output, padding, masking, special-tokens, vocabulary]
topic: "[[Padding、Mask、特殊符号与词表边界]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Padding、Mask、特殊符号与词表边界]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Padding、Mask、特殊符号与词表边界

## A

### NN-PMS-A01
区分 `padding_idx`、attention padding mask、loss `ignore_index` 与 generation stop condition。分别指出它们作用的对象与典型 shape。

### NN-PMS-A02
说明 BOS、EOS、PAD、UNK、MASK、SEP 六种角色。为什么“注册为 special token”不自动决定 attention、loss 与解码语义？

### NN-PMS-A03
一个可复现的 tokenizer–vocabulary–model checkpoint 至少应绑定哪些版本、ID、shape 与 row-order 信息？

## B

### NN-PMS-B01
原序列为 $(a,b,c)$。写出带 BOS/EOS 的 causal teacher-forcing input 与 target；再把 batch 补到长度 6，给出 target loss-valid mask。

### NN-PMS-B02
两条序列的有效 token losses 为 $(0.2,0.4)$ 与 $(0.3,0.5,0.7)$。计算 valid-token mean 与 sequence-equal mean，并解释默认 `mean` 更接近哪一个。

### NN-PMS-B03
对 scores $(2,1,0)$，第三项分别加 $-\infty$ 与 $-10$。计算两种 Softmax，说明有限 mask 为什么不等于精确删除。

## C

### NN-PMS-C01
设 unreduced losses 为 $\ell_i$、valid indicator 为 $m_i$。推导 ignored-token mean
$$
L=\frac{\sum_i m_i\ell_i}{\sum_i m_i}
$$
对每个 $\ell_i$ 的梯度；再说明多 rank 训练为何必须聚合全局 numerator 与 count。

### NN-PMS-C02
把 causal、key-padding 与 segment constraints 写成一个允许边 indicator。对两条长度分别为 2、3 的样本 packed 成长度 5，画出 $5\times5$ self-attention 允许矩阵。

### NN-PMS-C03
分析全被 mask 的 attention row：为什么标准 stable Softmax 未定义？给出三种合法实现合同，并说明各自对输出与梯度的定义。

## D

### NN-PMS-D01
设计 left-padding 与 right-padding 等价测试，覆盖 position IDs、last-valid logit、KV cache 和 generation stop。

### NN-PMS-D02
系统令 `PAD_ID=EOS_ID`。指出按 ID 构造 loss mask 的错误，并设计同时保留真实 EOS 监督、忽略补齐位置的 label/mask 构造。

### NN-PMS-D03
新增 128 个 tokens 后，只调用 tokenizer 的 `add_tokens`，未改模型与 optimizer。列出会发生的显式错误和 silent errors，并给出原子迁移清单。

## E

### NN-PMS-E01
设计一个针对 padding/mask/special-token 的最小 property-based test suite，覆盖 eager/fused、FP32/低精度、训练/生成与 save/load。

### NN-PMS-E02
反驳：“只要 attention mask 正确，padding 就不会影响训练。”从 lookup、loss reduction、position、normalization、optimizer 与指标统计六方面说明。

### NN-PMS-E03
设计 packed-sequence 数据管线的验收协议，使 packed 与逐样本执行在定义的有效 logits、loss 和 gradient 上等价。
