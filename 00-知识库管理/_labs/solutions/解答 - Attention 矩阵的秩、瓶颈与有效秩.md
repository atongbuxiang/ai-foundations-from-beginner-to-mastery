---
type: solution
status: draft
area: [architecture, attention, matrix-rank]
topic: "[[Attention 矩阵的秩、瓶颈与有效秩]]"
exercise: "[[习题 - Attention 矩阵的秩、瓶颈与有效秩]]"
sources: ["[[S-2020-Bhojanapalli-LowRank-Attention]]", "[[S-2021-Dong-Pure-Attention-RankCollapse]]", "[[S-2025-Su-10847-矩阵的有效秩]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Attention 矩阵的秩、瓶颈与有效秩

## A. 识别与复述

### ARCH-RANK-A01
$L=QK^T$ 有 rank $\le d_k$。$A=\mathrm{rowsoftmax}(L+M)$ 经非线性后不能直接给 rank $\le d_k$；最多有 shape 上界 $\min(T_q,T_k)$。$O=AV$ 有 rank $\le\min(\mathrm{rank}A,\mathrm{rank}V,T_q,d_v)$。

### ARCH-RANK-A02
Stable rank $r_s=\sum\sigma_i^2/\sigma_1^2$；谱熵 effective rank 令 $p_i=\sigma_i/\sum_j\sigma_j$ 后为 $e^{-\sum p_i\log p_i}$。它们对谱尾和尺度集中的敏感性不同，零矩阵约定也不同，数值不能互称“effective rank”后直接比较。

### ARCH-RANK-A03
Strict rank 数非零奇异值；numerical rank 需阈值/精度；conditioning 常看 $\sigma_{max}/\sigma_{min}$，描述求逆/扰动敏感；effective rank 连续概括谱能量/熵集中。满 strict rank 可同时条件极差且 effective rank 近 1。

## B. 手算与建模

### ARCH-RANK-B01
L 只有第二行非零，rank 1。A 第一行为 $(1/2,1/2)$，第二行为 $(1/(1+e),e/(1+e))$；det $=(e-1)/[2(1+e)]>0$，故 rank 2。

### ARCH-RANK-B02
Strict rank 2。Stable rank $(16+4)/16=1.25$。$p=(2/3,1/3)$，熵 $H=-(2/3)\ln(2/3)-(1/3)\ln(1/3)\approx.6365$，effective rank $e^H\approx1.890$。

### ARCH-RANK-B03
V 两列共线，rank$(V)\le1$，所以 rank$(AV)\le1$。A 满秩不突破 value 列空间瓶颈；若 V 非零且未被 A 零化，最大可达 1。

## C. 推导与证明

### ARCH-RANK-C01
rank$(\Phi_Q\Phi_K^T)\le r$。D 可逆时左乘 $D^{-1}$ 不改变 rank，因此 rank$(A)=\mathrm{rank}(\Phi_Q\Phi_K^T)\le r$。若某 denominator 为 0，A 未定义/需另约定，不能用该证明。

### ARCH-RANK-C02
上三角位置被 mask 为 0，对角 softmax 权重严格正，故 determinant 为正对角乘积，满秩。病态族可令对角 $A_{ii}=\epsilon_i>0$ 极小、质量集中到早期列；det 非零但最小奇异值可趋 0、condition number 发散。

### ARCH-RANK-C03
拼接列空间满足 rank$([O_1|\cdots|O_h])\le\sum_r\mathrm{rank}(O_r)$，同时行数限制 rank$\le T_q$；合并得 min。若列空间重叠，实际 rank 严格低于和；后乘 $W_O$ 不能增加 rank。

## D. 边界、反例与纠错

### ARCH-RANK-D01
B01 的 $d_k=1<T=2$ 反例中 logit rank 1、softmax weight rank 2。正确的是 logit rank 界，不是 weight rank 界；softmax 的逐行非线性可增加矩阵秩。

### ARCH-RANK-D02
取 $A_\epsilon=\mathrm{diag}(1,\epsilon,\ldots,\epsilon)$，任意 $\epsilon>0$ 时 strict rank n；stable rank $[1+(n-1)\epsilon^2]/1\to1$。condition number $1/\epsilon\to\infty$，同时展示三种概念分离。

### ARCH-RANK-D03
定理的递推对象是无 skip/MLP 的 pure attention map，并依范数/参数假设。Residual 使 $H^{l+1}=H^l+F(H^l)$，不再是同一收缩递推；MLP/normalization/position/causal mask也改变映射。完整模型只能另证明或实测，不能名字相似就套用。

## E. AI 迁移

### ARCH-RANK-E01
固定样本/length/mask/dtype，逐层头保存 L、A、$A V$、attention branch、residual stream 与 block output；报 singular spectra、stable/entropy rank（公式明确）、threshold rank、condition proxy。对 batch/seed/length 分布报告，并用 uniform/identity/random/causal 基线；避免只测平均 A。

### ARCH-RANK-E02
扫描 feature r 与 head width，分别测 affinity/output rank/spectra、kernel/output error、task quality、参数/FLOP/state/memory/latency；exact softmax 为同 shape/训练预算基线。对每个 r 重调合理超参并给 equal-quality crossover；不能用一个 r 的失败宣判方法类。

### ARCH-RANK-E03
“正对角下三角所以满秩”是 `I`；关于特定 causal/bidirectional 模型的谱是 `E`；若有带假设的表示定理才是 `T`；“满秩带来 decoder-only 优势”是 `H`；跨任务/规模普适性是 `O`。需控制 objective、data、parameter allocation、position、cache 与 training budget 后实验，故原句不能作为定理成立。
