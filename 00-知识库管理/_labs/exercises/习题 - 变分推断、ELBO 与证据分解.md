---
type: exercise
status: draft
area: [math/information-theory, math/statistics, ai/generative-models]
topic: "变分推断、ELBO 与证据分解"
difficulty: [A, B, C, D, E]
prerequisites: ["[[变分推断、ELBO 与证据分解]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 变分推断、ELBO 与证据分解]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 变分推断、ELBO 与证据分解

> [!abstract] 训练目标
> 从 joint model 和 arbitrary $q$ 重建 Jensen bound、evidence identity、mean-field update、VAE objective 与 stochastic gradients；能分离 family/amortization/optimization/Monte Carlo gap，并审计 posterior collapse、modified objectives 与 held-out likelihood evaluation。

## A. 识别与复述

### INFO-VI-A01

对 latent model 逐项定义 prior、likelihood、joint、evidence、model posterior、variational posterior 与 posterior predictive。指出哪些由 $p_\theta$ 唯一决定，哪些是 inference design。

### INFO-VI-A02

写出 ELBO 的 joint-ratio form、reconstruction–prior-KL form 与 evidence-gap identity。说明 equality、support 和 finite-value 条件。

### INFO-VI-A03

区分 approximation gap、amortization gap、optimization gap、Monte Carlo error 与 model misspecification。哪些属于同一 posterior KL identity，哪些是更外层的数据生成误差？

## B. 手算与构造

### INFO-VI-B01

使用[[实验 - ELBO 恒等式、变分族限制与摊销缺口]]的模型：$P(Z=1)=0.3$，$P(X=1\mid Z=1)=0.9$，$P(X=1\mid Z=0)=0.2$。对 $x=1$ 和 $q(Z=1)=0.8$，计算 evidence、posterior、ELBO、posterior KL，并验证 identity。

### INFO-VI-B02

$q(z\mid x)=N(\mu,\operatorname{diag}\sigma^2)$、$p(z)=N(0,I)$，其中

$$
\mu=(1,-0.5),\qquad \log\sigma^2=(\log0.25,\log4).
$$

计算 total KL 和 per-dimension contributions。若 batch size 为 32，解释 `sum latent, mean batch` 与 `mean all elements` 的数值关系。

### INFO-VI-B03

posterior target table 为

$$
r(z_1,z_2)=
\begin{array}{c|cc}
 &z_2=0&z_2=1\\\hline
z_1=0&0.1&0.2\\
z_1=1&0.3&0.4
\end{array}.
$$

用 mean-field $q_1q_2$，从 $q_2(1)=0.5$ 出发做一次 $q_1$ coordinate update，再做一次 $q_2$ update。报告 probabilities 与 ELBO 单调性的理论结论。

## C. 推导与证明

### INFO-VI-C01

分别用 Jensen 和 posterior KL expansion 推导 ELBO。证明两条推导的 equality condition 相同，并说明为什么标准 VI 自然得到 reverse KL。

### INFO-VI-C02

用 calculus of variations 推导

$$
\log q_j^*(z_j)=E_{q_{-j}}\log p(x,z)+\text{const}.
$$

说明 coordinate ascent 为何不降低 ELBO，以及为何仍不保证 global optimum。

### INFO-VI-C03

推导 score-function estimator 与 pathwise estimator。证明 baseline 不改变 score estimator 的 expectation；列出把 gradient 与 expectation 交换所需的正则条件和两类 estimator 的典型 bias/variance 边界。

## D. 边界、反例与纠错

### INFO-VI-D01

target posterior 是两个相距很远、等权、窄 Gaussian 的 mixture，variational family 是单 Gaussian。定性比较最小化 $D(q\|p)$ 与 $D(p\|q)$ 的候选，并解释为什么“reverse KL 必然只选一个 mode”仍不是无条件定理。

### INFO-VI-D02

判断并证明：$\beta$-VAE objective 在 $\beta>1$、$\beta=1$、$0<\beta<1$ 时是否一定是 $\log p(x)$ 的 lower bound。说明“仍是某个下界”和“仍是 canonical ELBO identity”为什么不同。

### INFO-VI-D03

构造一个 decoder 完全忽略 $z$ 的 latent model，使 $q(z\mid x)=p(z)$、KL=0 但 latent 对 $x$ 无信息。说明 posterior collapse 时 ELBO、reconstruction 与 representation quality 可以如何分离。

## E. AI 迁移

### INFO-VI-E01

审计一个图像 VAE：作者对 $[0,255]$ continuous pixels 使用 elementwise BCE，KL 对 latent 求 mean，BCE 对 pixels 求 sum，再把两者直接相加。写出至少八项对象、单位和 reduction 检查，并给出两种 coherent likelihood 方案。

### INFO-VI-E02

某论文用训练集 $K=5000$ 的 IWAE value 比较两个模型，却用 $K=1$ 训练另一个模型、不同 encoder family、不同 tokenizer，并宣称“模型 A 的真实 log-likelihood 更高”。设计公平 evaluation protocol，包含 held-out data、proposal、ESS/log-weight、$K$ sensitivity 与 compute budget。

### INFO-VI-E03

为 categorical latent VAE 比较 REINFORCE、Gumbel–Softmax 与 straight-through estimator。逐项说明目标、gradient bias、variance、temperature、train/eval mismatch 和 reproducibility report。

## 分级提示

- `B01`：$p(x=1)=0.41$，posterior parameter 为 $0.27/0.41$；
- `B02`：每维为 $\tfrac12(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2)$；
- `B03`：$q_1(z_1)\propto\exp E_{q_2}\log r(z_1,Z_2)$；
- `C03`：使用 $\nabla q=q\nabla\log q$ 与 $E_q\nabla\log q=0$；
- `D02`：与 canonical ELBO 比较多出的 $(\beta-1)D(q\|p)$；
- `D03`：令 $p_\theta(x\mid z)=p_\theta(x)$。

## 解答入口

完成独立尝试后再打开：[[解答 - 变分推断、ELBO 与证据分解]]。
