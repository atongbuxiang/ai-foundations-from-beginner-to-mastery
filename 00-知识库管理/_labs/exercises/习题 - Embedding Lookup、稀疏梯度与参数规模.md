---
type: exercise
status: draft
area: [neural-networks/embedding-output, embedding, sparse-gradients]
topic: "[[Embedding Lookup、稀疏梯度与参数规模]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Embedding Lookup、稀疏梯度与参数规模]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Embedding Lookup、稀疏梯度与参数规模

## A

### NN-ELS-A01
设词表大小为 $V$、embedding dimension 为 $d$，索引张量 $I$ 的 shape 是 $[B,T]$。分别写出参数表、单个 token 输出与批量输出的 shape；解释为什么 embedding 追加的是表示维而不是把序列维合并掉。

### NN-ELS-A02
区分以下三句话：某行的数学梯度为零、梯度使用稀疏存储、该行在整个 optimizer step 中完全不变。它们为什么不等价？

### NN-ELS-A03
说明 `padding_idx`、`scale_grad_by_freq`、`max_norm` 与 `sparse=True` 分别改变哪一份合同：前向值、反向梯度、参数更新或存储格式。

## B

### NN-ELS-B01
令
$$
E=\begin{bmatrix}1&0\\0&1\\2&-1\\-1&3\end{bmatrix},
\qquad I=(2,1,2).
$$
写出 selection matrix $S$，并计算 $SE$。

### NN-ELS-B02
沿用 B01。若三个位置的上游梯度依次为 $(1,2),(-1,0.5),(3,-1)$，计算完整的 $\nabla_E\mathcal L$；再计算按 batch 内 token 频次平均后的结果。

### NN-ELS-B03
取 $V=50{,}000,d=1024$。计算参数量，以及只计参数本体时 FP32、FP16/BF16 各占多少十进制 MB；若 Adam 另保留一份 FP32 master weight、两个 FP32 moment，再估算每参数总字节数和总量。

## C

### NN-ELS-C01
用标准基向量证明单个 lookup 等于 $E^\mathsf Tq_i$，并由微分/Frobenius 配对推导 $\nabla_E\mathcal L=q_i g^\mathsf T$。

### NN-ELS-C02
对展平后的索引 $(i_1,\ldots,i_n)$ 与上游矩阵 $G\in\mathbb R^{n\times d}$，证明 $\nabla_E\mathcal L=S^\mathsf TG$，并由此推出重复索引必须 scatter-add。

### NN-ELS-C03
令 loss reduction 从 token-sum 改为 token-mean。推导 embedding 梯度的尺度变化；说明它与按每种 token 的出现频次再平均为何不是同一操作。

## D

### NN-ELS-D01
某训练任务设置 `sparse=True`，同时使用 AdamW、对所有参数做 dense weight decay，并在多卡间执行 dense all-reduce。逐项审计“训练成本已经按被访问行数缩放”的说法。

### NN-ELS-D02
解释为什么在 forward 内对 embedding 权重执行 `max_norm` 的原地重整化，可能与此前基于该权重构造的可微计算发生冲突。给出安全的计算顺序或复制策略。

### NN-ELS-D03
输入 embedding 与全词表输出分类器共享同一参数。分析 lookup 端的行稀疏梯度是否还能使共享参数的总梯度保持稀疏，并给出应监控的三个量。

## E

### NN-ELS-E01
设计一个验证重复 token 梯度累加、`padding_idx` 与 frequency scaling 的最小实验。写出输入、可手算 loss、预期梯度与至少一个会抓住 silent bug 的断言。

### NN-ELS-E02
大词表系统中，比较 dense embedding、稀疏 row update 与参数分片三种方案。给出一个同时记录模型质量、显存、通信、热点负载与恢复语义的公平协议。

### NN-ELS-E03
反驳：“Embedding 只是无计算量的查表，所以增大 $V$ 和 $d$ 几乎没有系统代价。”至少从参数、带宽、optimizer state、checkpoint、分布式路由与输出层六方面作答。
