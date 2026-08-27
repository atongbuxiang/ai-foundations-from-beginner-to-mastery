---
type: solution
status: draft
area: [architecture, transformer, encoder-decoder, cross-attention]
topic: "[[Encoder–Decoder 与 Cross-Attention]]"
exercise: "[[习题 - Encoder–Decoder 与 Cross-Attention]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2015-Bahdanau-Attention]]", "[[S-2020-Raffel-T5]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Encoder–Decoder 与 Cross-Attention

## A. 识别与复述

### ARCH-ED-A01
$$
H_e=\operatorname{Encoder}(s_{1:T_s})\in\mathbb R^{B\times T_s\times d},
\qquad
p(y\mid s)=\prod_{t=1}^{T_t}p(y_t\mid y_{<t},H_e).
$$
Encoder memory 在生成目标序列期间固定，decoder prefix 随步增长。

### ARCH-ED-A02
顺序为 causal target self-attention、target-to-source cross-attention、position-wise FFN；每个子层通常各有 norm、residual 和 dropout。Decoder layer 外部输入/输出都为 $(B,T_t,d)$。

### ARCH-ED-A03
Source padding mask 屏蔽 cross-attention 的无效 source key columns；target causal mask 屏蔽 decoder self-attention 的未来 target；target loss mask 决定哪些 target rows/labels计入目标。三者的矩阵轴与作用阶段不同。

## B. 手算与建模

### ARCH-ED-B01
总宽 $d=hd_h=64$。分头后 $Q:(2,4,5,16)$，$K,V:(2,4,7,16)$；score/weights 为 $(2,4,5,7)$；每头输出 $(2,4,5,16)$，concat + O projection 后为 $(2,5,64)$。

### ARCH-ED-B02
四个 target queries 都可读三个有效 source keys：
$$
\begin{bmatrix}
1&1&1&0&0\\
1&1&1&0&0\\
1&1&1&0&0\\
1&1&1&0&0
\end{bmatrix}.
$$
它是 $4\times5$ 长方形 relation，不是 target causal triangle。

### ARCH-ED-B03
QK 与 AV 合计
$$
2BT_tT_sd=2\cdot1\cdot32\cdot128\cdot512
=4{,}194{,}304
$$
MACs。未计 Q/K/V/O projections、softmax、mask 与 data movement。

## C. 推导与证明

### ARCH-ED-C01
$QK^\top$ 为 $(T_t,d_k)(d_k,T_s)=(T_t,T_s)$；再乘 $V:(T_s,d_v)$ 得
$$
(T_t,T_s)(T_s,d_v)=(T_t,d_v).
$$
Source 轴 $T_s$ 被 contraction，每个 target query 留一行，故输出回到 target 轴。

### ARCH-ED-C02
固定 $H_e$ 与每层 $W_K,W_V$ 时，$K_e=H_eW_K,V_e=H_eW_V$ 与生成步 $t$ 无关，可在 decoder 开始前算一次，后续仅新 Q 读取。若 source memory 随 target 更新、cross K/V 权重按步动态变化、source 被追加的 streaming encoder、训练时参数在同一生成循环更新，或 stochastic projection 每步变化，则原缓存需失效/追加。

### ARCH-ED-C03
Decoder-only layer 有一组 MHA 主权重 $4d^2$；标准 encoder–decoder decoder layer多一组 cross MHA，增加 Q/K/V/O 共约 $4d^2$。FFN 与 self-attention 不变；bias/norm为低阶项。若 cross 使用不同 $d_k,d_v$，按实际 shapes 重算。

## D. 边界、反例与纠错

### ARCH-ED-D01
设 source 长 5、target 第一个 query。错误地按 $j\le i$ 只让它读 source 1，屏蔽 source 2–5；但翻译第一个 target token本应可用完整 source句子。Target index 与 source index没有这种因果对应。

### ARCH-ED-D02
权重是给定参数化计算中的 mixing coefficient；多个 value 可冗余、O/FFN 可重写结果，且不同权重组合可能输出相同。构造两个相同 values 时，任意 attention 分配输出都相同。忠实因果使用需做 source deletion/replacement、梯度/干预和输出变化验证，不能只读热图。

### ARCH-ED-D03
拼接单栈的 source states按同一 stack relation逐层演化，source/target共享参数和 context；标准架构先产生独立双向 encoder final memory，每个 decoder layer再读取它。二者的 layer access、parameter allocation、position、cache和 memory生命周期不同，能看同一信息不等于计算图相同。

## E. AI 迁移

### ARCH-ED-E01
Source：改变 padding values/长度不改变 target logits；每个 target row可读全部有效 source。Target：future pulse 不影响此前 logits，shift gold正确。Cache：encoder只算一次；cross K/V复用与重算基准一致；target self cache逐步追加；beam reorder同步。再测试空/长 source、packed target、loss token count 与 full-vs-incremental。

### ARCH-ED-E02
先把 source 全部 mask/置空，测质量下降；再只替换关键事实、保持长度/风格，检查输出是否随事实改变；交换无关片段作为控制。对要求引用的任务，验证生成 claim 与 source span 的 entailment/字符串证据，并报告拒答。热图只作描述，主要结论来自干预效果与多 seed。

### ARCH-ED-E03
固定总参数而非层数、训练 token/FLOPs、source/target tokenizer与数据、objective target密度、context/长度分布、优化调参预算和解码规则。分别报告质量、source利用干预、prefill/decode latency、memory/cache、吞吐与多 seed。明确一方是否可双向编码 source、参数如何在 stacks间分配，以及服务硬件/kernel。
