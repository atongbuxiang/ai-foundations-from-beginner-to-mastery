---
type: solution
status: draft
area: [architecture, attention, multi-head]
topic: "[[Multi-Head Attention、投影子空间与参数量]]"
exercise: "[[习题 - Multi-Head Attention、投影子空间与参数量]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2019-Michel-Head-Pruning]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Multi-Head Attention、投影子空间与参数量

## A. 识别与复述

### ARCH-MHA-A01
$H_r=\operatorname{Attn}(X_qW_Q^{(r)},X_mW_K^{(r)},X_mW_V^{(r)})$，$\operatorname{MHA}=\operatorname{Concat}(H_1,\ldots,H_h)W_O$。Self 情形令 $X_q=X_m$。

### ARCH-MHA-A02
固定 $hd_h=d_{model}$，h 增加使每头宽 $d_h=d_{model}/h$ 下降；标准 Q/K/V/O 主投影参数仍约 $4d_{model}^2$；显式 score 元素 $BhT_qT_k$ 随 h 线性增。

### ARCH-MHA-A03
Packed matrix 的不同列块就是不同 heads 的 $W_Q^{(r)}$ 等参数。reshape 只是把合并的 $hd_h$ 轴重新解释为 $(h,d_h)$；同一次 GEMM 不表示列块数值共享。

## B. 手算与建模

### ARCH-MHA-B01
每个 packed Q/K/V 是 $512^2=262,144$，三者共 786,432；O 再 262,144；总 1,048,576。等价地 8 个 $512\times64$ 小块每类仍为 $512^2$。

### ARCH-MHA-B02
12 heads 每头 64，24 heads 每头 32。显式 score：12 头为 $4\cdot12\cdot1024^2=50,331,648$；24 头为 100,663,296，恰加倍。

### ARCH-MHA-B03
Q $(2,8,16,64)$；K/V $(2,8,128,64)$；S $(2,8,16,128)$；H $(2,8,16,64)$；转置拼接 $(2,16,512)$；若 $W_O:512\to512$，output $(2,16,512)$。

## C. 推导与证明

### ARCH-MHA-C01
一般参数为 $d_q(hd_k)+d_m(hd_k)+d_m(hd_v)+(hd_v)d_o$，分别对应 Q、K、V、O。Self 标准取 $d_q=d_m=d_o=d$ 且 $hd_k=hd_v=d$，得 $d^2+d^2+d^2+d^2=4d^2$；bias 另为 $2hd_k+hd_v+d_o$（视实现融合约定）。

### ARCH-MHA-C02
每头 $QK^T$ work 约 $BT_qT_kd_k$，h 头为 $BhT_qT_kd_k=BT_qT_k(hd_k)=BT_qT_kd$。但每头保存一个 $T_q\times T_k$ score，故元素为 $BhT_qT_k$，不乘 $d_k$，h 不消去。

### ARCH-MHA-C03
将拼接向量的 head blocks 用块置换矩阵 $P_h$ 重排，得到 $H'_{cat}=H_{cat}P_h^T$。相应令 $W'_O=P_hW_O$，则 $H'_{cat}W'_O=H_{cat}P_h^TP_hW_O=H_{cat}W_O$。所以编号本身不可辨识。

## D. 边界、反例与纠错

### ARCH-MHA-D01
固定总宽时参数量不随 h 主阶增加，每头反而变窄；表达集合如何变化需考虑多个 distributions 与更低 per-head rank 的权衡，并非单调严格包含。极端 h=d 时每头一维，可能受瓶颈；训练也可能令 heads 重复。

### ARCH-MHA-D02
令所有 heads 的 $W_Q^{(r)},W_K^{(r)},W_V^{(r)}$ 完全相同且输入相同，则 $H_1=\cdots=H_h$。Concat 只是重复同一向量，$W_O$ 可将重复块合并；功能上没有多个独立寻址模式。

### ARCH-MHA-D03
单头 zeroing 的剩余 heads 可补偿，而且影响可能非加性。两个 heads 各自可由对方替代，单独剪任一无损，但同时剪两者丢失功能。联合剪枝还改变 normalization/残差分布，必须直接测 curve。

## E. AI 迁移

### ARCH-MHA-E01
冻结 checkpoint，按预定义 importance 或随机顺序分别做：(a) 单头 mask；(b) 累计联合 mask；(c) 真正删除权重并重编 kernel；(d) 删除后微调。多 seed 报 quality、OOD、latency、memory 与 confidence interval。Zeroing 不自动减少 wall-clock；结构删除才测系统收益。

### ARCH-MHA-E02
登记 MHA 的 h_q=h_kv 与 GQA 的 h_q>h_kv；重算 W_K/W_V 参数与 decode KV cache $O(BT h_{kv}d_h)$，Q/O 与 score work；在同参数或同训练 FLOP两种公平口径下比较 quality。固定 batch/length/dtype/kernel/hardware，报告 prefill/decode latency，防止只用理论 cache 比例。

### ARCH-MHA-E03
训练多 seed 后，不直接按 head index 比较。以 attention outputs/score pattern/gradient intervention 构造 head 间距离，用 Hungarian matching 对齐；再报告匹配稳定性、功能干预和置信区间。对齐本身的 metric 也版本化，避免用一张 heatmap 声称语义一致。
