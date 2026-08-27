---
type: solution
status: draft
area: [architecture, efficient-attention, mla, latent-cache]
topic: "[[MLA、潜变量缓存与推理成本证据]]"
exercise: "[[习题 - MLA、潜变量缓存与推理成本证据]]"
sources: ["[[S-2024-DeepSeek-V2-MLA]]", "[[S-2024-Su-10091-MHA-MQA-GQA-MLA]]", "[[S-2025-Su-10907-MLA上]]", "[[S-2025-Su-11111-MLA下]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - MLA、潜变量缓存与推理成本证据

## A. 识别与复述

### ARCH-MLA-A01
Linformer 在 token/sequence 轴把 $n$ 个 K/V 投到 $k$ 个槽，矩阵依序列位置；MLA 对每个 token 独立把 feature 表示压成 $d_c$ 维 joint KV latent，再在需要时展开或吸收投影。MLA 缩每 token cache width，不直接减少历史 token 个数。

### ARCH-MLA-A02
抽象写法：$x_t\in\mathbb R^d$，$c_t^{KV}=W_D^{KV}x_t\in\mathbb R^{d_c}$；content K/V 由 $W_{UK}c_t,W_{UV}c_t$ 展开到各 heads；query 可先降维再展开，最终有 $h_q\times d_h$ content queries。实际 MLA 还缓存位置 key 支路 $k_t^R\in\mathbb R^{d_R}$。

### ARCH-MLA-A03
Content projection 对 token feature 是固定线性映射，可移到内积另一侧。RoPE 是 position-dependent rotation：$R_tWc_t$ 的 $R_t$ 随 token 变，不能作为一个固定 $W$ 无条件吸收进所有 queries。故常分离小型 decoupled RoPE K/Q 支路。

## B. 手算与建模

### ARCH-MLA-B01
MHA 每 token 每层为 $2h_qd_h=2\cdot128\cdot128=32768$ 标量；MLA 为 $d_c+d_R=576$。比例 $576/32768=0.017578125$，约 1.76%，即 payload 约小 56.9 倍。这里只是抽象 payload。

### ARCH-MLA-B02
$q^\top k=(xW_Q)^\top(cW_{UK})$（按行/列约定调整转置）。以列向量记即 $q^TW_{UK}c=(W_{UK}^Tq)^Tc$。吸收后 query $q'=W_{UK}^Tq\in\mathbb R^{d_c}$，直接与 cached $c$ 点积。

### ARCH-MLA-B03
差异来源包括：浮点矩阵乘法结合次序不同；BF16 rounding/accumulation dtype；fused kernel 使用不同 reduction/order；权重/activation quantization scale；RoPE 支路 concat 顺序；不同 epilogue/bias。故应测容差等价而非预设 bitwise。

## C. 推导与证明

### ARCH-MLA-C01
标量内积满足 $q^T(W_{UK}c)=(W_{UK}^Tq)^Tc$。若 value 为 $v=W_{UV}c$，加权后再经 $W_O$：$W_O\sum_j a_jW_{UV}c_j=(W_OW_{UV})\sum_ja_jc_j$，可把固定线性展开与输出投影合并。若权重本身依展开 K，先按前式吸收到 query。

### ARCH-MLA-C02
MHA 每 token 每层 K/V payload 为 $2h_qd_h$；MLA 缓存 joint latent $d_c$ 与 RoPE key $d_R$，故比例
$$\rho=\frac{d_c+d_R}{2h_qd_h}.$$
它忽略 batch/layer 公共因子、dtype 后相同缩放，也忽略 allocator、scale/metadata、padding、通信、workspace 和可能额外 cache 分支。

### ARCH-MLA-C03
若 $k=\sigma(Wc)$，一般 $q^T\sigma(Wc)$ 不能写成某个固定线性 $Aq$ 与 $c$ 的点积。又若 $k_t=R_tWc_t$，吸收矩阵会变为 $W^TR_t^Tq$，依 key position $t$；单个 query 不能预先生成一个对所有历史 t 通用的 latent query。

## D. 边界、反例与纠错

### ARCH-MLA-D01
MLA 可能增加 query latent projections、位置支路、重参数化或不成熟 kernel；若模型是 compute/launch/communication-bound，cache bytes 不支配延迟。不同 $d_c,d_R$ 还可能大于某 GQA payload；质量要求、batch 与量化也改变 Pareto。

### ARCH-MLA-D02
消融只观察给定参数规模、训练 token、数据、head dimension、优化与实现下的样本结果；未遍历所有架构/预算/硬件，也常无法完全匹配参数。它是经验支持 `E`，理论解释可作为 `H/T` 的有限条件结果，不是普遍最优定理。

### ARCH-MLA-D03
例如 GQA $h_{kv}=4,d_h=64$，K/V payload 为 $2\cdot4\cdot64=512$；若 MLA $d_c=512,d_R=64$，总 576，反而更大。MLA 优势取决于具体 config，而不来自名称。

## E. AI 迁移

### ARCH-MLA-E01
同一 weights/input，在 fp32 先比较显式展开 K/V 的 full causal output与吸收 query/value-output 的 latent decode；RoPE content/position scores分别比，再比总 score、softmax、output/logits。随后 bf16/fp16 用分层容差；覆盖 prefill/chunk/cache offset、不同 lengths，并使漏位置支路负对照失败。

### ARCH-MLA-E02
固定数据、训练 tokens、optimizer、参数预算和多 seed；显式记录无法精确匹配的 head dimension/参数。Serving 固定 cache dtype/quant、kernel版本、batch/并发/prompt/output 网格和硬件；报告质量、payload/allocated bytes、TTFT/ITL/throughput、HBM/compute/通信以及调参成本。

### ARCH-MLA-E03
`I`：projection absorption、shape、payload公式；`T`：在明确模型族与假设下的表示/下界结果；`E`：DeepSeek 整模型系统数值与受控消融；`H`：为何 joint latent/partial RoPE/短卷积可能有效的机制解释；`O`：不同硬件、量化、MTP、并行与 kernel 下的全局 Pareto。每条结论必须带适用 config 与不可推出项。
