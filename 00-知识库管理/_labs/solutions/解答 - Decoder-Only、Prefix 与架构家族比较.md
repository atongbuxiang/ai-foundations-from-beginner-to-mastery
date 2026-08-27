---
type: solution
status: draft
area: [architecture, transformer, decoder-only, prefix-lm]
topic: "[[Decoder-Only、Prefix 与架构家族比较]]"
exercise: "[[习题 - Decoder-Only、Prefix 与架构家族比较]]"
sources: ["[[S-2019-Devlin-BERT]]", "[[S-2018-Radford-GPT]]", "[[S-2020-Raffel-T5]]", "[[S-2023-Su-9529-DecoderOnly低秩猜想]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Decoder-Only、Prefix 与架构家族比较

## A. 识别与复述

### ARCH-FAM-A01
Relation 规定 query $i$ 可读哪些 key $j$；Q/K/V source 规定 self stream 还是 target-to-source memory；objective 规定输入破坏、条件分解和哪些 positions计 loss；outlet 规定逐 token、pooling 或 autoregressive distribution。四栏比单个架构名称更可核验。

### ARCH-FAM-A02
Encoder-only 对有效 token通常 $R_{ij}=1$。Decoder-only 为 $R_{ij}=\mathbf1[j\le i]$。Encoder–decoder 同时有 source encoder 全双向、target self causal 和 target-to-source cross relation；三张矩阵的轴不同。

### ARCH-FAM-A03
单栈只表示共用一条 stack。Prefix LM 可让 prefix 内全双向、suffix 对 prefix 全可见且对 suffix 因果，因此不是整条序列统一下三角。Mask、segment relation 与 loss region仍需显式定义。

## B. 手算与建模

### ARCH-FAM-B01
$$
R=
\begin{bmatrix}
1&1&0&0&0\\
1&1&0&0&0\\
1&1&1&0&0\\
1&1&1&1&0\\
1&1&1&1&1
\end{bmatrix}.
$$
前两行只读 prefix；后三行读全部 prefix 与截至自身的 suffix。

### ARCH-FAM-B02
全序列 causal 下，target 第一个 row 可读 source 1–3 和该行的右移 target-input 槽位；第二个还可读前一个 target input。按位置 relation 为下三角。若只监督两个 target labels，loss mask 可写 $(0,0,0,1,1)$；严格实现还需说明 separator/BOS 与 label shift。

### ARCH-FAM-B03
下三角矩阵行列式等于对角元素乘积。若 $A_{ii}>0$，则
$$
\det A=\prod_iA_{ii}>0,
$$
故代数秩为 $T$。但若一些对角权重极小或奇异值快速衰减，矩阵可病态，stable/effective/numerical rank 接近低值；满秩不表示各方向同样有效。

## C. 推导与证明

### ARCH-FAM-C01
$$
R=
\begin{bmatrix}
\mathbf1_{P\times P}&0_{P\times S}\\
\mathbf1_{S\times P}&L_S
\end{bmatrix}.
$$
Prefix query rows 对 suffix key columns 的 mask 为零，softmax 后权重也为零，输出分子不含 suffix values。因此固定 prefix inputs时，仅改 suffix values不改变 prefix attention outputs；逐层 relation保持时可归纳到整栈。

### ARCH-FAM-C02
拼接单栈：source states在共享 causal/prefix stack中逐层更新，target在同层读取历史 K/V，source/target共享参数和 context/cache。Encoder–decoder：source先经独立双向 encoder形成 final memory，每个 decoder layer用独立 cross projections读取，target另有 self cache；source cross K/V可在层内跨 steps复用。两者的读取深度、参数分配和生命周期不同。

### ARCH-FAM-C03
最小例：一个 source scalar $s$、一个 target query $y$。拼接单层可令 target直接 attention 到由共享 $W_V$ 投影的 $s$；encoder–decoder可先以 $g_{\theta_e}(s)$ 非线性编码，再由独立 $W_V^c$ 读取。两者都“可见 $s$”，但函数分别受共享投影与独立 encoder/cross 参数约束，梯度路径也不同。

## D. 边界、反例与纠错

### ARCH-FAM-D01
满秩只是单个 attention weight matrix 的代数性质；encoder 的多头、residual、FFN 和跨层组合也能有高表达。满秩不保证条件良好、优化容易、目标匹配或泛化。Decoder-only优势还可能来自 next-token 数据密度、统一接口、规模、参数分配和 serving；需受控实验，不能由 determinant 裁决。

### ARCH-FAM-D02
两模型都用相同 causal attention。模型甲对每个 next token计 loss；模型乙把前 80% 当 prompt，只对后 20% response计 loss。前向可见关系相同，gradient supervision density和条件任务却不同，最终模型不是同一训练目标。

### ARCH-FAM-D03
同层数时 encoder–decoder 还含整套 encoder，且每个 decoder layer多 cross MHA，参数/FLOPs/cache都更大；反之若强行等宽，参数分配不同。公平性应固定总参数、训练 FLOPs/token/data/调参预算或明确比较目标，而非只固定层数。

## E. AI 迁移

### ARCH-FAM-E01
离线 token/句子理解：优先比较双向 encoder的全 token表示与低 latency。条件生成：比较 encoder–decoder的 source memory复用和 decoder-only的统一序列化。在线开放生成：重点看 decoder cache、throughput与统一接口。每格再填数据/目标适配、总参数、source/target长度、质量、首 token与逐 token latency；表给候选而非普遍赢家。

### ARCH-FAM-E02
在匹配参数、数据、objective密度和训练 FLOPs下训练 causal、bidirectional/prefix variants；逐层逐头测代数秩、奇异谱、stable/effective rank、condition number，并同步测 representation rank、梯度、loss与下游质量。干预 diagonal/mask但保持其他预算，做多 seed。检验“秩差异存在”与“秩差异中介性能”两条不同 claim。

### ARCH-FAM-E03
预注册模型总参数与 FFN/embedding分配、训练 token/FLOPs、数据顺序/tokenizer、context与source/target长度、objective/loss tokens、optimizer/搜索预算。报告质量、鲁棒、source utilization、training throughput、prefill/decode latency、cache/峰值显存和多 seed；对每个指标注明 matched-parameter、matched-FLOP或matched-latency。
