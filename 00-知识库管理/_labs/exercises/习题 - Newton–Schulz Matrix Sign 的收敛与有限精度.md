---
type: exercise
status: verified
area: [training, optimization, numerical-linear-algebra, muon]
topic: "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"
solution: "[[解答 - Newton–Schulz Matrix Sign 的收敛与有限精度]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Newton–Schulz Matrix Sign 的收敛与有限精度

> [!abstract] 训练目标
> 把矩阵多项式化为 singular-value scalar map，掌握经典 Newton–Schulz 的局部误差递推，并能为 finite-step、rank-deficient 与 mixed-precision 输出设计多残差审计。

## A. 识别与复述

### TRN28-A01
区分 exact polar target、经典 Newton–Schulz 迭代、Muon Jordan 五次多项式和某次 finite-precision kernel output。

### TRN28-A02
为什么对 $X=U\Sigma V^T$ 的奇矩阵多项式可化为逐奇异值映射？这在 floating-point arithmetic 中保留到什么程度？

### TRN28-A03
定义 orthogonality residual、polar residual、direction cosine 与 dual-gap residual；说明每个量能发现什么、又可能漏掉什么。

## B. 手算与构造

### TRN28-B01
对经典标量映射 $\phi(s)=\tfrac12s(3-s^2)$，从 $s_0=0.5$ 计算 $s_1,s_2$ 和 $e_k=1-s_k^2$；验证误差递推。

### TRN28-B02
对 $G=\operatorname{diag}(1,0)$，从任意标量归一化 $X_0=\alpha G$ 出发，证明所有奇多项式迭代的第二个 singular value 始终为 0。应使用哪个 projector 作为 orthogonality target？

### TRN28-B03
令 $G=\operatorname{diag}(4,1)$，候选 $\widehat Q=-I$。计算其 orthogonality residual、与 exact polar $Q=I$ 的 direction cosine 和 pairing。说明为何只检查正交性会接受错误方向。

## C. 推导与证明

### TRN28-C01
从矩阵迭代
$$
X_+=aX+bXX^TX+cXX^TXX^TX
$$
严格推出 $s_+=as+bs^3+cs^5$，并说明 tall/wide 两种乘法排列的维度。

### TRN28-C02
对经典映射证明
$$
e_{k+1}=\frac14e_k^2(3+e_k),\qquad e_k=1-s_k^2,
$$
并给出 $0<s_0<\sqrt2$ 下趋向 1 的论证轮廓。

### TRN28-C03
证明 Frobenius normalization $X_0=G/\lVert G\rVert_F$ 保证 $\lVert X_0\rVert_2\le1$；再对 rank-$r$ flat spectrum 计算所有初始非零 singular values。

## D. 边界、反例与纠错

### TRN28-D01
反驳“五步 Newton–Schulz 总能得到正交矩阵”。用极小非零 singular value 或 rank deficiency 给出 exact-arithmetic 反例机制。

### TRN28-D02
为什么未收敛 power iteration 的 Rayleigh/singular estimate 通常不能直接作为严格上界做归一化？说明低估谱范数如何把初值推离设计区间。

### TRN28-D03
反驳“FP32 reference 通过，所以 BF16 kernel 必然安全”。列出至少六个必须单独控制的数值与系统变量。

## E. AI 迁移

### TRN28-E01
设计 singular-value sweep：包含 flat、geometric decay、clustered、rank-deficient 与 condition number 网格，写出输入、reference、metrics 与 pass/fail assertions。

### TRN28-E02
设计一次 0—8 steps 的 residual trajectory 实验，比较经典系数与 Jordan 系数；怎样避免只挑对某一组系数有利的 spectrum？

### TRN28-E03
为一个 fused low-precision NS kernel 写验收清单：覆盖数学残差、NaN/Inf、determinism、shape/layout、peak memory、throughput 与 fallback。

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。必须写出 reference target 和 residual denominator；完成后再打开 [[解答 - Newton–Schulz Matrix Sign 的收敛与有限精度]]。
