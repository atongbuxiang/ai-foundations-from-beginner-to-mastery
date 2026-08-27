---
type: exercise
status: verified
area: [training, optimization, muon, scaling]
topic: "[[Muon 形状缩放、Update RMS 与版本差异]]"
solution: "[[解答 - Muon 形状缩放、Update RMS 与版本差异]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Muon 形状缩放、Update RMS 与版本差异

> [!abstract] 训练目标
> 从 rank 与奇异值推导 partial-isometry update RMS，逐式翻译 current PyTorch 三种 adjustment，并把 parameter RMS、relative update、average output change 与 worst-case change 分账。

## A. 识别与复述

### TRN29-A01
在 $y=xW$、$W\in\mathbb R^{A\times B}$ 约定下，$A,B$ 各表示什么？若改写成 column-vector $y=W x$，为什么不能原样搬用 $A/B$？

### TRN29-A02
给出 rank-$r$ partial isometry $Q=U_rV_r^T$ 的 spectral norm、Frobenius norm 与 element RMS。

### TRN29-A03
写出 current PyTorch 的 original、match_rms_adamw、spectral_unclamped 三种 adjustment，并说明每个公式需绑定哪些版本字段。

## B. 手算与构造

### TRN29-B01
对 $A=4096,B=1024$ 与 $A=1024,B=4096$，分别计算 full-rank $Q$ 的未缩放 RMS，以及三种 adjustment 后的 RMS。

### TRN29-B02
令 $A=8,B=4$，但 $Q$ 的有效 rank 只有 $r=2$。计算未缩放 RMS、original 的 nominal full-rank 预测与实际 RMS；求二者比例。

### TRN29-B03
若 finite-step output 的 singular values 为 $(1.1,0.9,0.4,0)$，shape 为 $4\times4$，计算实际 Frobenius norm 与 RMS，并与 exact full-rank polar 的值比较。

## C. 推导与证明

### TRN29-C01
从 singular values 证明
$$
\operatorname{RMS}(U_rV_r^T)=\sqrt{\frac r{AB}},
$$
并推出 full-rank 时 $1/\sqrt{\max(A,B)}$。

### TRN29-C02
逐个分情况证明 current original adjustment 使 full-rank ideal update 的 RMS 等于 $1/\sqrt B$；再推导 spectral_unclamped 在 $A<B$ 时的 RMS。

### TRN29-C03
设输入 covariance 为 $C_x=\mathbb E[x^Tx]$。推导
$$
\mathbb E\lVert x\Delta W\rVert_2^2
=\operatorname{tr}(\Delta W^TC_x\Delta W),
$$
并给出它可化为 $\sigma_x^2\lVert\Delta W\rVert_F^2$ 的充分条件。

## D. 边界、反例与纠错

### TRN29-D01
反驳“spectral norm 为 1，所以每元素更新大小为 1”。用 $4096\times1024$ full-rank partial isometry 给出数量级。

### TRN29-D02
说明用 local tensor-parallel shard shape 计算 scaling 为什么可能偏离 global formula。构造一个 global $4096\times4096$、按列四分片的例子。

### TRN29-D03
反驳“同 update RMS 就有同 function-space trust region”。构造两个 covariance $C_x$，使相同 Frobenius norm 的两个 update 产生显著不同的平均输出变化。

## E. AI 迁移

### TRN29-E01
设计 layerwise scaling logger：至少记录 global/local shape、effective rank、actual singular-value moments、nominal/actual RMS、relative update 与 output probe。

### TRN29-E02
为三种 adjustment 设计公平 ablation。哪些超参数应共享，哪些必须重新搜索？如何避免把 decay strength 的变化混入 scaling 比较？

### TRN29-E03
审计一个旧 checkpoint 配置只写了 adjust_lr_fn=original 的情况。列出你需要恢复的版本、shape 与 update-order 信息，并说明无法恢复时应如何标记证据。

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。每个 shape 公式先声明 $xW$ 或 $Wx$；完成后再打开 [[解答 - Muon 形状缩放、Update RMS 与版本差异]]。
