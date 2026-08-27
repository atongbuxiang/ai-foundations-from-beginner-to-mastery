---
type: exercise
status: draft
area: [neural-networks/residual-stability, lipschitz, perturbation-analysis]
topic: "[[残差缩放、Lipschitz 界与深度稳定性]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 残差缩放、Lipschitz 界与深度稳定性]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 残差缩放、Lipschitz 界与深度稳定性

## A

### NN-RSL-A01
定义 global、restricted-domain、local-Jacobian、empirical 与 expected Lipschitz/sensitivity 对象。哪一种可以直接代入全局 composition theorem？

### NN-RSL-A02
对 $x_{\ell+1}=x_\ell+\alpha_\ell F_\ell(x_\ell)$ 写出 two-trajectory recurrence，并说明 $|\alpha_\ell|$ 为什么不能漏掉。

### NN-RSL-A03
分别说明 $\alpha=1/N$ 与 $\alpha=1/\sqrt N$ 自然控制的量。前者是否必然最优？后者是否给 deterministic uniform bound？

## B

### NN-RSL-B01
设三层都有 $|\alpha|L=0.2$，$\|\delta_0\|=0.5$，additive errors 为 $(0.01,0.02,0)$。逐层计算递推上界并用展开公式复核最终值。

### NN-RSL-B02
令 $F(x)=-3x$。按 $\alpha=0,0.2,1/3,0.5,2/3,1$ 计算 residual multiplier，判断同号衰减、零映射、振荡衰减、临界与发散。

### NN-RSL-B03
两层分别有 $(|\alpha_0|L_0,|\alpha_1|L_1)=(0.2,0.2)$。计算 product bound 与 exponential bound，并比较松紧。

## C

### NN-RSL-C01
证明 $G=I+\alpha F$ 的 upper/lower Lipschitz bounds，并说明 $|\alpha|L<1$ 如何推出 injective 与 inverse-on-range bound。

### NN-RSL-C02
在 one-sided Lipschitz 常数为 $\mu$、普通 Lipschitz 常数为 $L$ 时，推导 squared-distance factor，并给出 $\mu<0$ 下的 contraction step 区间。

### NN-RSL-C03
从 $d_{\ell+1}\le q_\ell d_\ell+\xi_\ell$ 推导一般 forcing 展开式。为什么早期误差通常比晚期误差有更长 amplification tail？

## D

### NN-RSL-D01
对 $x^+=Px+\alpha F(x)$，分别讨论 $P$ 为 orthogonal、$P=0.5I$、rank-deficient projection 时的 upper/lower 界和信息保持。

### NN-RSL-D02
某模型在 1000 个验证样本、每样本 10 个随机方向上观测到 JVP gain 均小于 1。能否声称 global contraction？给出更诚实的报告文本与进一步证书需求。

### NN-RSL-D03
解释 residual update 在低精度中的 absorption、cancellation、overflow/underflow 和 reduction-order forcing。提出至少四项 dtype/数值诊断。

## E

### NN-RSL-E01
假设 $L_\ell\le C$。分别推导 $\alpha=N^{-1}$ 与 $N^{-1/2}$ 的 deterministic exponential upper bound；再在不相关零均值 branch 假设下推导 increment variance 量级。

### NN-RSL-E02
反驳：“网络 Lipschitz 上界小，所以它必然 adversarially robust、泛化好且易优化。”为三个结论分别指出缺失对象。

### NN-RSL-E03
设计一个 residual-scaling 消融：比较 $1,1/\sqrt N,1/N$ 与可学习 scale，记录 forward/gradient/update/Jacobian/roundoff/性能。怎样避免把不同有效学习率误归因于架构？
