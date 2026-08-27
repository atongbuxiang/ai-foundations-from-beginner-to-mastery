---
type: solution
status: verified
area: [training, optimization, matrix-preconditioning]
topic: "[[Shampoo、逆矩阵根与 Kronecker 预条件]]"
exercise: "[[习题 - Shampoo、逆矩阵根与 Kronecker 预条件]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Shampoo、逆矩阵根与 Kronecker 预条件

> [!warning] 使用边界
> Root exponent、damping、block convention 与数值 residual 是算法定义的一部分；“用了 Shampoo”不能替代这些字段。

## A. 识别与复述

### TRN23-A01
Flatten 后 full-matrix AdaGrad 保存 $P\times P$ second moment，即 $P^2$ 元素。Shampoo 对 tensor 的每个 mode 展开 gradient，并保存 $L^{(i)}\in\mathbb R^{d_i\times d_i}$，总计 $\sum_i d_i^2$；它保留各轴内部 correlation，同时删除无法由 mode-wise separable structure 表达的完整坐标耦合。

### TRN23-A02
经典形式是 $\widetilde G=G\times_1L_1^{-1/(2k)}\cdots\times_kL_k^{-1/(2k)}$。矩阵 $k=2$，两侧各贡献 $-1/4$ 的齐次缩放；两侧合起来对整体 gradient scale 形成 half-power normalization。每侧若误用 $-1/2$，总缩放会过强。

### TRN23-A03
Statistics 每步/高频累计 Gram，root 每 $K$ 步低频重算 inverse roots，apply 每步使用最新可用 roots。平均成本 $C_{avg}=C_{stats}+C_{apply}+C_{root}/K+C_{comm}$；$K$ 越大 root 摊销越小，但当前 statistics 与旧 root 的偏差越大。

## B. 手算与构造

### TRN23-B01
$L^{-1/4}=\operatorname{diag}(1/2,1)$、$R^{-1/4}=\operatorname{diag}(1,1/3)$，故
$$\widetilde G=\begin{bmatrix}1/2&1/6\\1&1/3\end{bmatrix}.$$
左 factor 缩放 rows，右 factor 缩放 columns，结果不与全 1 的原矩阵共线。

### TRN23-B02
$P=24$。三个 matricization shape 为 $2\times12$、$3\times8$、$4\times6$；Grams 为 $2\times2$、$3\times3$、$4\times4$，共 $4+9+16=29$ 个元素。Flatten full matrix 是 $24\times24$，需 576 个元素。

### TRN23-B03
$X^4=\operatorname{diag}(1/16,1)$，故 $X^4A=I$，inverse residual matrix 为零；两者 diagonal，所以 commutator 也为零。误用 $X=\operatorname{diag}(1/4,1)$ 时 $X^4A-I=\operatorname{diag}(-15/16,0)$，但 commutator 仍为零，说明 $r_{comm}$ 不能替代 $r_{inv}$。

## C. 推导与证明

### TRN23-C01
做齐次尺度检查：若 $G\mapsto cG$，每个 mode Gram $L_i\mapsto c^2L_i$，故每个 $L_i^{-1/(2k)}$ 缩放为 $c^{-1/k}$。$k$ 个 mode products 合计 $c^{-1}$，恰好抵消原 gradient 的 $c$；这就是各 mode 分担整体 half-power 的意义。$k=1$ 得 inverse square root，$k=2$ 得左右 inverse fourth roots；它不是把每个 mode 都当作独立 full inverse square root。

### TRN23-C02
$A^{-1/p}=Q\operatorname{diag}(\lambda_i^{-1/p})Q^T$，其 eigenvalues 为正，故对称正定；它与 $A$ 共享 eigenvectors，乘法可交换。Repeated eigenvalue 的 basis 虽不唯一，但在该 eigenspace 上函数值同为标量 $\lambda^{-1/p}$，所以重组后的 matrix function 唯一。

### TRN23-C03
在 $T$ 步中，statistics、apply、communication 付 $T$ 次，root 约付 $T/K$ 次；总成本除以 $T$ 得公式。平均值把 refresh step 的 $C_{root}$ 峰值摊薄，无法表示同步等待、workspace 峰值、allocator 抖动或 p99 step time，故仍需 tail 与 peak 指标。

## D. 边界、反例与纠错

### TRN23-D01
GEMM-only iteration 仍需合适 initial scaling 与谱收敛域，有限 precision 下可能失稳或停滞；迭代数随 conditioning 与容差变化。EVD 与迭代法的真实速度还依 block size、kernel quality、workspace、通信和 refresh frequency，稳定性必须由 residual/repair 实测，不能由算子类型推断。

### TRN23-D02
若 $A=\operatorname{diag}(10^{-12},1)$，inverse fourth root 的第一增益是 $10^3$，会显著放大该方向噪声。$A+\epsilon I$ 平滑移动全部 eigenvalues，eigenvalue floor 则逐项截断到阈值；二者给不同谱函数和 bias，需记录阈值单位与修复方式。

### TRN23-D03
Block splitting 删除跨 block correlation；grafting 保留 Shampoo direction 但用另一优化器规定 update norm；fallback 对特定 shape/sparse 参数直接换算法。再叠加 momentum/decay/dtype 顺序后，transition 已由完整 policy 决定，所以方法名必须附 block、graft、fallback 与 clocks。

## E. AI 迁移

### TRN23-E01
每 block 记录 dimension、damping/floor、root exponent/solver/iterations、dtype、symmetry error、finite flag、$\|X^pA-I\|/\|I\|$、commutator residual、min/max eigenvalue、repair count、root age、input/output norm 与 direction cosine。

### TRN23-E02
Persistent 至少含各 mode Gram/EMA、roots 或 eigenvectors、momentum/graft state，按 dtype 与 shard/replica 计算。峰值还含 eigensolver workspace、临时矩阵副本、all-gather/reduce buffers、padding blocks、mixed-precision cast、checkpoint staging 和 allocator fragmentation；这些不会出现在 $\sum d_i^2$ 的纸面状态里。

### TRN23-E03
预注册 block size × refresh period 的搜索网格，并给 AdamW 等额 trial/算力；统一 seed、token、batch、停止和 checkpoint。报告训练质量、time-to-quality、平均/p95 step time、peak/state memory、通信、失败 trials 与置信区间；不能只挑 Shampoo 的最佳网格却只跑一个 AdamW 默认点。

## 无提示重做

- [ ] 48 小时后从齐次尺度重建 $-1/(2k)$ 指数。
- [ ] 一周后写出同时需要 inverse residual 与 commutator residual 的例子。
