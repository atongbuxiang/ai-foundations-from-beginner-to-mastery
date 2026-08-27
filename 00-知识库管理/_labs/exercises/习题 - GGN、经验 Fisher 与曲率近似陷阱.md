---
type: exercise
status: verified
area: [training, optimization, curvature]
topic: "[[GGN、经验 Fisher 与曲率近似陷阱]]"
solution: "[[解答 - GGN、经验 Fisher 与曲率近似陷阱]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - GGN、经验 Fisher 与曲率近似陷阱

> [!abstract] 训练目标
> 用最小反例逐一审计“GGN≈Hessian”“empirical Fisher≈Fisher”“batch gradient outer product≈per-sample second moment”，并把近似质量落实为可量化证书。

## A. 识别与复述

### TRN21-A01
把“近似 Hessian”拆成对象近似、统计估计与数值求解三个层次；每层各举一个可能失败的环节。

### TRN21-A02
区分 `mean(g_i g_i^T)`、`mean(g_i) mean(g_i)^T` 与 centered gradient covariance。它们各保留或删除了什么？

### TRN21-A03
列出 $F=G$、population Hessian $=F$、$F_{emp}\approx F$ 三个命题各自需要的条件；不要把条件合并成一句“大样本下都相等”。

## B. 手算与构造

### TRN21-B01
对 $f_\theta=\theta^2$、$L=\tfrac12(\theta^2-1)^2$，在 $\theta=0,1/2,1$ 分别计算 GGN、模型二阶残差与 Hessian，并标出负曲率区间。

### TRN21-B02
Gaussian 均值模型中取 observed $y=2$。在 $\theta=2,1,0$ 计算 Hessian、true Fisher 与 empirical Fisher；说明 EF 的尺度如何随 residual 变化。

### TRN21-B03
二维 per-sample gradients 为 $g_1=(1,1)$、$g_2=(1,-1)$。计算 per-sample second moment、batch-mean outer product 与 centered covariance，并比较 rank。

## C. 推导与证明

### TRN21-C01
对 scalar residual $r(\theta)$ 的 $L=\tfrac12r^2$ 推导 $H=(r')^2+rr''$ 与 $G=(r')^2$；给出 $G=H$ 的充分条件与非必要条件例子。

### TRN21-C02
证明
$$\mathbb E[gg^T]=\operatorname{Cov}(g)+\mathbb E[g]\mathbb E[g]^T,$$
并用它解释 non-central second moment 既可能反映 noise，也可能含 gradient signal。

### TRN21-C03
设 $C,H\succ0$。定义方向二次型比、Frobenius 相对误差和 damped inverse-step cosine；说明为何任一单指标都不足以成为完整近似证书。

## D. 边界、反例与纠错

### TRN21-D01
构造一个 PSD 但 rank-1 的矩阵，使它完全遗漏 Hessian 的一个重要方向；计算该方向上的 Rayleigh quotient ratio。

### TRN21-D02
说明 batch size 趋于无穷为何只能减少 estimator variance，不能修复错误 label law、错误 reduction 或结构性 block deletion。

### TRN21-D03
反驳：“若 empirical Fisher 在训练后期变小，说明损失面变平。”至少给出 residual interpolation、真实 Fisher 和 Hessian 三者的对照。

## E. AI 迁移

### TRN21-E01
为 curvature approximation benchmark 设计最小 toy suite，使 nonlinear model term、label-measure mismatch、reduction/rank 三类错误各有独立测试。

### TRN21-E02
在不能显式形成 Hessian 的大模型中，如何用随机方向 HVP、quadratic forms、inverse-step cosine 与 model ratio 审计 proxy？

### TRN21-E03
阅读代码中名为 `fisher` 的张量时，写出从数据管道到最终 preconditioned update 的逐层检查表。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。每个反例必须写清“删除哪条等号、没有否定什么”，完成后打开 [[解答 - GGN、经验 Fisher 与曲率近似陷阱]]。
