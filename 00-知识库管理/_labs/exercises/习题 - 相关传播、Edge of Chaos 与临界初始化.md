---
type: exercise
status: draft
area: [neural-networks/initialization, correlation-propagation, edge-of-chaos]
topic: "[[相关传播、Edge of Chaos 与临界初始化]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 相关传播、Edge of Chaos 与临界初始化]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 相关传播、Edge of Chaos 与临界初始化

## A

### NN-EOC-A01
区分单输入 second moment $q_\ell$、两输入 covariance $q_{12}^{(\ell)}$ 与 normalized correlation $c_\ell$；各自回答什么问题？

### NN-EOC-A02
写出 equal-variance 情形下 correlation map $\mathcal C(c)$，并解释 bias 项为何为 $+\sigma_b^2$。

### NN-EOC-A03
定义 $\chi_1$，给出 ordered、critical、chaotic 三个局部制度。

## B

### NN-EOC-B01
令 $U=\sqrt q Z_1$、$V=\sqrt q(cZ_1+\sqrt{1-c^2}Z_2)$。直接计算 $U,V$ 的两个 variance 与 covariance。

### NN-EOC-B02
给定线性 activation、$q_*=1$、$\sigma_w^2=0.8,\sigma_b^2=0.2$，求 $\mathcal C(c)$、固定点、$\chi_1$ 与 correlation depth $\xi_c$。

### NN-EOC-B03
对 zero-bias ReLU、$\sigma_w^2=2$，用给定 closed form 计算 $\mathcal C(0)$、$\mathcal C(1/2)$ 与 $\mathcal C'(1)$。

## C

### NN-EOC-C01
从共享权重的两条前向路径展开 $\mathbb E[z(x)z(x')]$，推导 covariance recurrence。

### NN-EOC-C02
证明：若 $q_*$ 满足单输入 fixed-point equation，则 $c=1$ 是 correlation map 的 fixed point。

### NN-EOC-C03
从 $\varepsilon_{\ell+1}\approx\chi_1\varepsilon_\ell$ 推导 $\xi_c=-1/\log\chi_1$，并解释 $\chi_1\uparrow1$ 时为何需高阶分析。

## D

### NN-EOC-D01
构造两个网络，使每层单输入 second moment 都为 1，但一个把两个输入 correlation 推向 1，另一个在某邻域放大差异。说明 variance 证据为何不足。

### NN-EOC-D02
反驳：“$\chi_1=1$，所以任意两个输入在任意深度都保持原 correlation。”

### NN-EOC-D03
反驳：“ReLU + He 初始化处在 Edge of Chaos，因此具有 dynamical isometry。”

## E

### NN-EOC-E01
设计一个 finite-width correlation-map 实验，分离 Monte Carlo integral error、width error 与 seed variation。

### NN-EOC-E02
为 residual block $x\mapsto x+F(x)$ 写出两输入 covariance 的完整展开，指出需要额外估计的 cross terms。

### NN-EOC-E03
设计一个证据阶梯实验，同时记录 correlation trajectory、JVP/VJP gain 与 extreme singular estimate，并规定结论边界。

## 解答入口

[[解答 - 相关传播、Edge of Chaos 与临界初始化]]
