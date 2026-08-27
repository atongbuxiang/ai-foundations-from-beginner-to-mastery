---
type: solution
status: draft
area: [architecture, transformer, decoder, autoregressive]
topic: "[[Transformer Decoder 与自回归因果结构]]"
exercise: "[[习题 - Transformer Decoder 与自回归因果结构]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2018-Radford-GPT]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Transformer Decoder 与自回归因果结构

## A. 识别与复述

### ARCH-DEC-A01
$$
p(x_{1:T})=\prod_{t=1}^Tp(x_t\mid x_{<t}).
$$
Teacher forcing 把 model input 写成 $(\mathrm{BOS},x_1,\ldots,x_{T-1})$，targets 写成 $(x_1,\ldots,x_T)$。同一行只可见该 target 之前的真实前缀。

### ARCH-DEC-A02
训练已有完整右移输入，可同时计算所有 query rows；causal mask 保证第 $i$ 行不依赖未来 values。生成时未来 token 尚未知，$x_{t+1}$ 依赖已选择的 $x_t$，所以 token loop 串行。并行是执行调度，因果性是依赖关系，二者不矛盾。

### ARCH-DEC-A03
每层 cache 保存历史 token 的 K/V projections，通常不保存“可直接替代下一层计算”的最终 hidden state，也不缓存未知 token。它复用计算和增加内存，但在相同 position、mask、参数、eval 随机性与数值算法下不应改变 logits 语义。

## B. 手算与建模

### ARCH-DEC-B01
输入为 $[\mathrm{BOS},A,B,C]$，targets 为 $[A,B,C,D]$。可见矩阵为
$$
\begin{bmatrix}
1&0&0&0\\
1&1&0&0\\
1&1&1&0\\
1&1&1&1
\end{bmatrix}.
$$

### ARCH-DEC-B02
标量数
$$
2LBTd_{kv}=2\cdot24\cdot2\cdot1024\cdot1024
=100{,}663{,}296.
$$
FP16 两字节，共 $201{,}326{,}592$ bytes，约 $192$ MiB。未计 allocator、对齐、beam 和元数据。

### ARCH-DEC-B03
若九个 positions 依次对应 2 system、3 user、4 assistant，loss mask 可写 $(0,0,0,0,0,1,1,1,1)$，再结合右移后的 target index精确对齐。Attention relation 仍通常是全序列 causal 下三角：assistant 可读 system/user，前缀也按 causal 计算；loss mask 不是 attention mask。

## C. 推导与证明

### ARCH-DEC-C01
正确 mask 令 $j>i$ 的 logit 为 $-\infty$，softmax 权重 $a_{ij}=0$。输出
$$
o_i=\sum_{j\le i}a_{ij}v_j
$$
不含未来 value，因此只扰动任意 $v_j,j>i$ 时 $o_i$ 不变。若未来 key 也被扰动，合法 logits仍不依赖它；finite sentinel 必须足够实现零权重。

### ARCH-DEC-C02
条件包括：相同参数与 eval mode；相同 token/position IDs、RoPE offset 等；相同 inclusive causal relation；每层 cache 精确对应此前 K/V 并按 batch/beam 同步重排；无跨请求旧 cache；normalization 为逐 token 而非依赖未来序列统计；dropout 关闭或随机合同等价；数值 kernel 差异在容差内。

### ARCH-DEC-C03
从空序列生成到长度 $S$，无 cache 每步重算约 $t^2$ attention pairs，累计 $\sum_{t=1}^S t^2=O(S^3)$；cache 每步只算新 query 对 $t$ keys，累计 $\sum_t t=O(S^2)$。有 prompt $P$ 时分别是 $\sum_s(P+s)^2$ 与 $\sum_s(P+s)$；projection/FFN 也由整前缀重算降为只算新行。

## D. 边界、反例与纠错

### ARCH-DEC-D01
若输入直接是 $[A,B,C,D]$，target 也为 $[A,B,C,D]$，inclusive diagonal 让第 $i$ 行读到同一个 token embedding $x_i$。模型可学近似复制 identity 到输出 head，训练 loss 很低，却没有学习 $p(x_i\mid x_{<i})$。

### ARCH-DEC-D02
把样本一 $[A,B]$ 与样本二 $[C,D]$ 拼成 $[A,B,C,D]$，只使用全局 causal mask，则预测 C/D 时可读取 A/B。这既污染训练条件，也可能泄漏标签/文档。正确做法用 block-diagonal causal relation、segment-aware positions/cache，并分别计 loss。

### ARCH-DEC-D03
Teacher forcing 评价真实前缀条件下的一步分布；自由生成使用模型自己过去的采样，早期错误会改变后续输入分布。Decoding strategy、长度外推、数据覆盖与校准也影响长轨迹。低一步 loss 不提供“所有 rollouts 可靠”的联合概率保证。

## E. AI 迁移

### ARCH-DEC-E01
Future pulse：只改位置 $j$ 的 token/value，断言所有 $i<j$ logits 不变。Full-vs-cache：同一序列 eval 下逐步拼 logits，与一次 full causal logits逐位置比对。Reset：连续跑请求 A/B，B 在清 cache 后等于单独 B；不清时测试应暴露差异。再覆盖 padding、packing、position offset 和 dtype tolerance。

### ARCH-DEC-E02
每层 cache shape 应为 $(B\!\times\!beam,h_{kv},t,d_h)$；当 parent indices 为 $\pi$，所有层 K/V 的 batch-beam 轴必须同一 $\pi$ gather，token scores/finished flags 也同步。用两个 beam 写入明显不同 K/V，再交换 parent，检查下一步 logits与手工重排基准一致，并覆盖重复 parent。

### ARCH-DEC-E03
语义账：tokenizer/BOS、shift、causal/packing/loss mask、position offset、cache reset/reorder、eval 随机性、sampling 参数。性能账：prefill/decode 分开报告 batch、prompt/output length、dtype/quantization、cache bytes、tokens/s、首 token/逐 token latency、硬件/kernel。优化 cache 只有通过 full-vs-cache 语义测试后才可采纳。
