---
type: solution
status: draft
area: [architecture, efficient-attention, flashattention, systems]
topic: "[[FlashAttention、精确计算与 IO Awareness]]"
exercise: "[[习题 - FlashAttention、精确计算与 IO Awareness]]"
sources: ["[[S-2022-Dao-FlashAttention]]", "[[S-2023-Dao-FlashAttention2]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - FlashAttention、精确计算与 IO Awareness

## A. 识别与复述

### ARCH-FLASH-A01
Naive 实现常分为写出 $S=QK^\top$、读写 softmax probabilities、再读它与 V 相乘。$S,P$ 均为 $B\times h\times n\times n$，会在 HBM 往返。高算力 GPU 上，搬运这些大中间量可能比算术更限制性能。

### ARCH-FLASH-A02
“Exact”指在实数算术和相同 mask/normalization/dropout 语义下计算同一个 dense attention 函数，不做稀疏/低秩/kernel 近似。它不承诺浮点逐 bit 相同、不把算术阶降为线性，也不保证任意硬件、shape、库版本上都更快。

### ARCH-FLASH-A03
对一行已见 scores，维护最大值 $m$、稳定指数和 $\ell=\sum_j e^{s_j-m}$、加权值和 $u=\sum_j e^{s_j-m}v_j$，最终输出 $o=u/\ell$。更新新 tile 时必须把旧、新状态都重标度到合并最大值。

## B. 手算与建模

### ARCH-FLASH-B01
第一 tile $(1,3)$：$m_1=3$，$\ell_1=e^{-2}+1$，$u_1=2e^{-2}+4$。第二 tile：$m_2=-2$，$\ell_2=1$，$u_2=10$。合并 $m=3$：
$$\ell=\ell_1+e^{-5},\quad u=u_1+10e^{-5},$$
$$o=\frac{2e^{-2}+4+10e^{-5}}{e^{-2}+1+e^{-5}},$$
与直接对 $(1,3,-2)$ 减最大值 3 后 softmax 完全相同，数值约 $3.781$。

### ARCH-FLASH-B02
标量数 $2\cdot16\cdot4096^2=536{,}870{,}912$；2 bytes 共 $1{,}073{,}741{,}824$ bytes，即 1 GiB。尚未计 probability、Q/K/V/O、gradients、dropout mask、其他层与 allocator/workspace。

### ARCH-FLASH-B03
$$m=\max(m_1,m_2),$$
$$\ell=e^{m_1-m}\ell_1+e^{m_2-m}\ell_2,$$
$$u=e^{m_1-m}u_1+e^{m_2-m}u_2.$$
向量 $u$ 的每一维使用相同标量重权。

## C. 推导与证明

### ARCH-FLASH-C01
块 $b$ 的状态满足 $e^{m_b} \ell_b=\sum_{j\in b}e^{s_j}$、$e^{m_b}u_b=\sum_{j\in b}e^{s_j}v_j$。合并公式乘 $e^m$ 后分别等于两块原始和相加，因此得到并集的指数和与加权和；除法 $u/\ell$ 即拼接后的 softmax output。

### ARCH-FLASH-C02
Backward 不保存完整 score/probability，而保存每行 log-sum-exp 或 $(m,\ell)$、output 等小状态；反向重新从 Q/K 与 tiles 生成局部 scores/probabilities，再累加 gradients。这用额外算术/重算、kernel 设计复杂度交换 HBM activation storage/traffic。

### ARCH-FLASH-C03
每个 $q_i$ 的精确输出依赖所有 $k_j,v_j$；一般输入下缺少可复用有限维 sufficient statistic。因此算法仍计算 $n^2$ 个 query-key dot-product 对，主 MAC 为 $\Theta(n^2d)$；只改变 tile/order 与中间驻留层级。

## D. 边界、反例与纠错

### ARCH-FLASH-D01
浮点加法不满足结合律，tiling 改变归约顺序，可能使用不同累加精度、fused instructions 或 exp 近似；所以结果应在误差容差内等价，不必 bitwise 相同。bitwise 不同也不等于数学算法近似。

### ARCH-FLASH-D02
例如 $n=32$、batch/head 很小且 Q/K/V layout 需先 transpose；专用 kernel 的 launch、packing 与不满 tile 浪费可超过省下的几 KB HBM traffic，成熟 dense fused kernel 可能更快。故必须扫真实 shapes。

### ARCH-FLASH-D03
Causal 需 tile 内精确 $j\le i$；padding 需保证无效 key 不进 max/分母且无效 query 输出规则固定；dropout 需确定随机 mask/scale 并在 backward 可重建；varlen packing 需 segment boundaries，阻止跨样本读写。

## E. AI 迁移

### ARCH-FLASH-E01
以高精度 dense reference 比 forward 与 dQ/dK/dV；覆盖 fp32/bf16/fp16、极大/极小/全相等 logits、causal/padding/组合 mask、长度 0/1 与非整 tile、非连续 layout。Dropout 固定 seed/offset，比同一 mask 语义；报告绝对/相对误差和 NaN/Inf。

### ARCH-FLASH-E02
预热后用同步计时，扫 B/h/n/d/dtype/mask；profiler 分出 attention kernel、layout/launch 与端到端 block/model 时间。记录峰值 allocated/reserved memory、HBM bytes/throughput、achieved FLOPs/occupancy，并报告 p50/p95、软件版本和 crossover。

### ARCH-FLASH-E03
仍增长的包括 pairwise FLOPs、每层 Q/K/V/O 与 FFN 计算、KV cache、decode 历史读取、RoPE/mask 元数据、跨卡通信、训练 backward 时间，以及长上下文数据/质量/位置外推风险。减少 score activation 不等于无限上下文。
