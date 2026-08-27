---
type: exercise
status: draft
area: [math/optimization, math/information-geometry, ai/training]
topic: "镜像下降、Bregman 几何与自然梯度"
difficulty: [A, B, C, D, E]
prerequisites: ["[[镜像下降、Bregman 几何与自然梯度]]"]
related: ["[[优化与凸分析 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 镜像下降、Bregman 几何与自然梯度]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 镜像下降、Bregman 几何与自然梯度

> [!abstract] 训练目标
> 能用 Bregman/Fisher 几何推 update 与 proof，严格审计坐标、采样分布、近似与 damping，并区分不同 optimizer 的 geometry。

## A. 识别与复述

### OPT-MIRROR-A01

定义 Bregman divergence、mirror map、dual coordinate 与 mirror-descent subproblem。说明 divergence 与 metric 的区别。

### OPT-MIRROR-A02

定义 exact/model Fisher、empirical Fisher 与 generalized Gauss–Newton。写出各自 expectation/sampling distribution，并列出可能相等所需的条件。

### OPT-MIRROR-A03

比较 Euclidean gradient、preconditioned gradient、mirror descent、natural gradient、AdaGrad 和 Muon：分别由什么 movement geometry 或 statistics 定义？

## B. 手算与构造

### OPT-MIRROR-B01

取 $\psi(x)=\frac12x^THx$、$H\succ0$，推无约束与 constrained mirror step。令

$$
H=\operatorname{diag}(1,4),\quad
x_t=(1,1)^T,\quad g_t=(2,-4)^T,\quad\eta=\frac12,
$$

计算无约束新点。

### OPT-MIRROR-B02

在三维 simplex 上令 $x_t=(1/2,1/3,1/6)$、$g_t=(1,0,-1)$。用 negative entropy 和 $\eta=\log2$ 计算 exponentiated-gradient update，并验证归一化。

### OPT-MIRROR-B03

二分类 Bernoulli model 以 logit $\theta$ 参数化，$p_\theta(y=1)=\sigma(\theta)$。推导 Fisher；给 $p=1/4$、ordinary gradient $g=3/8$，计算 undamped natural direction。再换成 probability parameter $p$ 验证 tangent direction 一致。

## C. 推导与证明

### OPT-MIRROR-C01

证明 Bregman three-point identity，并由 constrained mirror optimality 推 one-step inequality。

### OPT-MIRROR-C02

假设 $\psi$ 对 $\|\cdot\|$ $\sigma$-strongly convex、$\|g_t\|_*\le G$、$D_\psi(x,x_1)\le R^2$，完整推导 $O(RG\sqrt{T/\sigma})$ regret bound并优化常数步长。

### OPT-MIRROR-C03

从 local KL trust region 推 natural-gradient direction；再证明在 smooth invertible reparameterization 下 exact infinitesimal natural tangent vector 的 transformation law。

## D. 反例与失败边界

### OPT-MIRROR-D01

用 $\psi(x)=\frac12x^2$ 或 negative entropy 验证 Bregman divergence 一般不满足 metric 公理；给出明确的 symmetry 或 triangle-inequality 反例。

### OPT-MIRROR-D02

构造 redundant parameterization 使 Fisher singular。比较 inverse 不存在、pseudoinverse solution 与 $(F+\lambda I)^{-1}g$；解释 damping 为什么破坏 exact reparameterization invariance。

### OPT-MIRROR-D03

构造 dataset/model mismatch，使 empirical Fisher 与 exact Fisher 明显不同。说明用 empirical Fisher 做 preconditioner 仍可有工程价值，但不能声称使用了 exact KL metric。

## E. AI 迁移

### OPT-MIRROR-E01

为 mixture-of-experts gating weights 设计 entropy mirror update。处理 zero support、load-balancing constraints、log-domain stability、stochastic gradients 与 held-out routing audit。

### OPT-MIRROR-E02

为 policy optimization 写 natural/TRPO-style implementation contract：state distribution、KL orientation、Fisher-vector product、CG、damping、line search、measured KL 与 advantage estimation error。

### OPT-MIRROR-E03

审计一个声称“Muon 是 natural-gradient/mirror-descent”的论断。给出要证明 natural gradient、mirror descent、spectral steepest descent 各自需要的数学对象，并提出可证伪实验。

