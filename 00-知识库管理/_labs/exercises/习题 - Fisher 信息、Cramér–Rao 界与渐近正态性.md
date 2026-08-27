---
type: exercise
status: draft
area: [math/statistics, ai/information-geometry]
topic: "Fisher 信息、Cramér–Rao 界与渐近正态性"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Fisher 信息、Cramér–Rao 界与渐近正态性]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - Fisher 信息、Cramér–Rao 界与渐近正态性]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Fisher 信息、Cramér–Rao 界与渐近正态性

> [!abstract] 训练目标
> 从 score 与 normalization 自行重建 information identity 和 CRLB；能完成 MLE 的 Taylor–CLT–LLN–Slutsky 推导，并在非正则、错设、高维及深度网络中准确限制结论。

## 使用方式

1. 每次写 $I$ 都标明单样本/全样本、参数化和取期望的分布；
2. 使用 $E[s]=0$ 或 $I=-E[H]$ 前先检查 support 与交换条件；
3. 下界题要写无偏/有偏、标量/向量、finite-sample/asymptotic 的版本；
4. AI 题必须区分 model Fisher、empirical Fisher、observed Hessian 与 GGN。

## A. 识别与复述

### PROB-FI-A01

定义 score、sample score、expected Fisher、observed information、empirical Fisher 和 GGN。逐一说明哪些依赖已观测数据、哪些保证 PSD、哪些在什么条件下相等。

### PROB-FI-A02

完整陈述标量无偏 Cramér–Rao bound、$g(\theta)$ 版本、有偏版本与向量版本。为什么它不是“所有 estimator 的 MSE 都不能更低”？

### PROB-FI-A03

列出经典 MLE 渐近正态性至少八项 regularity condition，并说明 fixed support、interior truth、identifiability、nonsingular information 与 fixed dimension 各自阻止哪类失败。

## B. 手算与构造

### PROB-FI-B01

$X_i\overset{iid}\sim\operatorname{Bernoulli}(p)$，$0<p<1$。计算 score、$I_1(p)$、$I_n(p)$ 和估计 $p$ 的 CRLB；证明 $\bar X$ 达界。再用 $\eta=\log[p/(1-p)]$ 重参数化并求 $I_1(\eta)$。

### PROB-FI-B02

$X_i\overset{iid}\sim N(\mu,sigma^2)$，$\sigma^2$ 已知。计算关于 $\mu$ 的 Fisher 和 CRLB。对 $g(\mu)=e^\mu$ 写无偏估计量，计算其方差，并判断是否有限样本达到 CRLB。

### PROB-FI-B03

$X\sim N(\mu,v)$，参数为 $(\mu,v)$。推导 joint Fisher matrix。再把 $v$ 改为 $\rho=\log v$，用 Jacobian 变换和直接求导各算一次新 Fisher，并解释零交叉项的含义与边界。

## C. 推导与证明

### PROB-FI-C01

在共同支持与交换条件下证明 $E_\theta[s_\theta(X)]=0$ 和

$$
I(\theta)=E[s_\theta s_\theta^\top]
=-E[\nabla^2\log p_\theta(X)].
$$

再证明 iid information additivity，并指出依赖样本多出的 cross-covariance 项。

### PROB-FI-C02

从 $\operatorname{Cov}(T,S)=g'(\theta)$ 与 Cauchy–Schwarz 推导 scalar CRLB，并写出等号条件。随后用 block information 和 Schur complement 推导 nuisance parameter 未知时目标参数的有效信息。

### PROB-FI-C03

从 MLE score equation 出发，完整给出 $\sqrt n(\widehat\theta-\theta_0)$ 渐近正态性的证明骨架：Taylor 展开、中间点控制、score CLT、Hessian uniform LLN、matrix inverse 连续性和 Slutsky。每一步标注所需假设。

## D. 边界、反例与纠错

### PROB-FI-D01

对 $X_i\sim U(0,\theta)$，证明 MLE 为 $X_{(n)}$，并求

$$
n(\theta-X_{(n)})/\theta
$$

的极限分布。解释该结果为何不服从普通 $\sqrt n$ MLE 正态理论，且不能通过把“内部 score”硬代入 Fisher 公式修复。

### PROB-FI-D02

以 Gaussian mean 为例，构造有偏 shrinkage estimator 在某些 $\theta$ 上 MSE 小于无偏 CRLB。再说明 Hodges/super-efficiency 的“单点更快”为什么不推翻 regular local asymptotic efficiency。

### PROB-FI-D03

给出 neural network Fisher 奇异的至少两种结构原因，并分析直接使用 pseudoinverse 或 damping 后，所得方向/“uncertainty”分别依赖哪些额外选择。为什么更多训练样本不一定消除这些零方向？

## E. AI 迁移

### PROB-FI-E01

对 $K$ 类 softmax 输出证明 logit-space conditional Fisher 为

$$
F_z=\operatorname{Diag}(p)-pp^\top.
$$

证明 $F_z\mathbf1=0$，再通过 network Jacobian 写 parameter Fisher。比较用模型采样标签与真实标签形成的 outer product。

### PROB-FI-E02

某研究把 mini-batch empirical Fisher 的逆对角线称为“参数置信区间”。写一份审稿意见：至少检查模型正确性、标签期望、参数可辨识、数据依赖、optimizer point、damping、batch noise、sandwich 与目标 functional。

### PROB-FI-E03

对错设 conditional model，定义

$$
H=-E_Q[\nabla^2\ell_{\theta^*}],
\qquad J=E_Q[s_{\theta^*}s_{\theta^*}^\top].
$$

推导 sandwich covariance 的 estimating-equation 线性化。再设计一个 simulation，比较 inverse Hessian 与 sandwich interval 的 coverage，并说明 clustered token/user 数据如何修改 $J$。

## 分级提示

- `B01`：$dp/d\eta=p(1-p)$；
- `B02`：利用 Gaussian MGF 构造 $e^{\bar X-c}$ 的无偏修正；
- `B03`：$I_v=1/(2v^2)$，$dv/d\rho=v$；
- `C02`：向量 block inverse 的目标块等于 Schur complement 的逆；
- `D01`：$P(X_{(n)}\le x)=(x/\theta)^n$；
- `E01`：one-hot $Y$ 的 covariance 即 categorical covariance。

## 解答入口

完成独立尝试后再打开：[[解答 - Fisher 信息、Cramér–Rao 界与渐近正态性]]。

## 本轮复盘

- 是否先检查正则条件再使用信息恒等式？
- 是否把 CRLB 的无偏方差界误写成通用 MSE 界？
- 是否完整连接 Taylor、CLT、LLN 与 Slutsky？
- 是否明确所算 Fisher 的采样分布、尺度与近似？
