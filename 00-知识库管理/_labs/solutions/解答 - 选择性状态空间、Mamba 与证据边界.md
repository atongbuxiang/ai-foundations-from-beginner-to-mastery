---
type: solution
status: draft
area: [architecture, state-space-models, mamba]
topic: "[[选择性状态空间、Mamba 与证据边界]]"
exercise: "[[习题 - 选择性状态空间、Mamba 与证据边界]]"
sources: ["[[S-2023-Gu-Mamba]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 选择性状态空间、Mamba 与证据边界

## A. 识别与复述

### ARCH-MAMBA-A01
抽象地令 $\Delta_t=s_\Delta(x_t)>0,B_t=s_B(x_t),C_t=s_C(x_t)$，$\bar A_t=e^{\Delta_tA}$，$\bar B_t=\int_0^{\Delta_t}e^{A\tau}B_td\tau$，$h_t=\bar A_th_{t-1}+\bar B_tx_t,y_t=C_th_t$。具体实现结构需回代码核对。

### ARCH-MAMBA-A02
$\Delta_t$ 调当前 retention/time scale，$B_t$ 调当前内容写入 state 的方向和幅度，$C_t$ 调当前读出哪些 state 维。它们是 learned mechanisms，不保证语义上总选对。

### ARCH-MAMBA-A03
参数随输入变化使 lag coefficient 不再固定，无法预生成单一 FFT kernel；但每步关于 state 仍是 affine map，pair composition 保持 associativity，故可做 selective parallel scan。

## B. 手算与建模

### ARCH-MAMBA-B01
$e^{-0.1}\approx0.9048$，$e^{-1}\approx0.3679$，$e^{-3}\approx0.0498$。$\Delta$ 越大，负 $A$ 下旧 state 保留越少。

### ARCH-MAMBA-B02
$h_1=2$，$h_2=0.1(2)+3=3.2$。Pair $p_2\otimes p_1=(0.1\cdot0.5,0.1\cdot2+3)=(0.05,3.2)$，作用于 $h_0=0$ 同样得 3.2。

### ARCH-MAMBA-B03
$LDN=4096\times512\times16=33,554,432$ 个核心标量状态更新量级。$L^2D=4096^2\times512=8,589,934,592$ 个 score 量级，约大 256 倍；这未含 projections、heads、kernel constants、IO，不能直接当速度比。

## C. 推导与证明

### ARCH-MAMBA-C01
若 $h_t=A_th_{t-1}+B_tx_t,y_t=C_th_t$，则 $x_j$ 对 $y_t$ 的线性化/给定参数路径系数为 $C_tA_tA_{t-1}\cdots A_{j+1}B_j$。每个 $A_k,B_j,C_t$ 由相应输入产生，因此系数依赖整段相关输入，不只依 lag $t-j$。

### ARCH-MAMBA-C02
无论 $A_t,b_t$ 怎样由输入预先计算，每步作为关于 state 的 pair 仍按 $(A_2,b_2)\otimes(A_1,b_1)=(A_2A_1,A_2b_1+b_2)$ 组合；矩阵乘法分配律给结合律。Parameter production 本身需先并行完成。

### ARCH-MAMBA-C03
每步 physical time 为 $\Delta$ 时 retention $r=e^{-\alpha\Delta}$。$r^n=1/2$ 给 $n_{1/2}=\log2/(\alpha\Delta)$ steps；对应连续时间 $n\Delta=\log2/\alpha$。

## D. 边界、反例与纠错

### ARCH-MAMBA-D01
线性 work 只限制计算增长。固定有限精度 state 对无界历史是压缩，信息可覆盖；selection/optimization/precision 和任务可识别性决定实际记忆。复杂度不是 information-preservation theorem。

### ARCH-MAMBA-D02
标量 state 先写入重要值 1；下一噪声 token 错误地产生 $\Delta=20$，retention $e^{-20}$ 几乎为零且写入噪声。之后任何读出都难恢复原值。架构允许学正确 gate，也允许学错。

### ARCH-MAMBA-D03
训练处理整段，可用大 batch、融合 scan 并摊薄 launch；单 token decode 每步输入小，可能受 kernel launch、projection 和内存访问主导。Transformer 有 KV cache 和高度优化 kernel。必须分别测目标 batch 的 p50/p95 latency。

## E. AI 迁移

### ARCH-MAMBA-E01
用同一生成的 $\Delta_t,B_t,C_t$，float64 sequential 作为 reference；比较 scan 多长度、chunk、非零初态、reset、padding、float32/bfloat16、forward/backward；覆盖极小/极大 $\Delta$、长乘积和 non-finite，报告 tolerance 而非 bitwise equality。

### ARCH-MAMBA-E02
固定 data/tokens、optimizer tuning budget、参数或 training compute；分别扫 length/batch/dtype；报告 quality–compute、training tokens/s、prefill、decode p50/p95、peak memory、state/KV bytes、能耗；用官方优化实现和版本 commit，包含 warm-up、多次重复与同硬件 baseline。

### ARCH-MAMBA-E03
拆为：核心 work 对 $L$ 线性（T）；固定 recurrent state bytes（T/H）；某 kernel 在指定 GPU 的训练吞吐（H/E）；指定模型/data 的 perplexity（E）；同预算 downstream 质量（E）；长上下文 retrieval/extrapolation（E）；所有硬件/任务普遍占优（O，当前不能由单论文证明）。

