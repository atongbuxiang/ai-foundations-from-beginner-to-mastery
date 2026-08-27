---
type: exercise
status: draft
area: [math/statistics, ai/probabilistic-modeling, ai/optimization]
topic: "最大似然估计与 MAP"
difficulty: [A, B, C, D, E]
prerequisites: ["[[最大似然估计与 MAP]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 最大似然估计与 MAP]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 最大似然估计与 MAP

> [!abstract] 训练目标
> 能从联合/条件概率模型推导 likelihood 和稳定 NLL，处理 support、边界与不存在的极大值；准确说明 MLE、MAP、L1/L2、weight decay 与 cross-entropy 之间有条件的对应。

## 使用方式

1. 先写完整密度及其 support，再取对数；
2. score equation 只能作为候选点生成器，仍需检查边界、存在、唯一与全局性；
3. MAP 题必须写 prior 定义在哪个参数坐标；
4. AI 题必须核对 sum/mean reduction、mask、weight 与 deployment estimand。

## A. 识别与复述

### PROB-MLE-A01

区分 PMF/PDF、likelihood、log-likelihood、prior、posterior 与 posterior predictive。为什么 $L(\theta;x)$ 一般不能读作 $P(\theta\mid x)$？MLE 和 MAP 各自输出什么、没有输出什么？

### PROB-MLE-A02

陈述 score equation 适用的条件。分别列举 MLE 在边界、不存在、不唯一、不可辨识和 support 依赖参数时的一个例子。

### PROB-MLE-A03

解释“L2 regularization 等于 Gaussian prior”需要核对的条件：loss sum/mean、样本量 scaling、优化器 weight decay、参数坐标、Jacobian、模型尺度对称与 prior properness。

## B. 手算与构造

### PROB-MLE-B01

$X_i\overset{iid}\sim\operatorname{Bernoulli}(p)$。求 MLE。若 $p\sim\operatorname{Beta}(a,b)$，求 interior MAP，并完整处理 $a\le1$、$b\le1$ 时的边界/非唯一情形。比较 posterior mean。

### PROB-MLE-B02

$X_i\overset{iid}\sim N(\mu,\sigma^2)$，$\mu,\sigma^2$ 都未知。推导二者的 joint MLE；证明 variance MLE 有偏，并比较无偏 sample variance。若所有 $x_i$ 完全相同，likelihood 会发生什么？

### PROB-MLE-B03

$X_i\overset{iid}\sim U(0,\theta)$，$\theta>0$。推导 likelihood、MLE、其 CDF/期望与一个无偏修正。指出为何仅解普通 score equation 会漏掉答案。

## C. 推导与证明

### PROB-MLE-C01

证明在模型正确且可积时，最大化 population expected log-likelihood 等价于最小化 $D_{\rm KL}(p_{\theta_0}\|p_\theta)$。再给出模型错设 $Q\notin\{P_\theta\}$ 时 pseudo-true parameter 的定义。

### PROB-MLE-C02

从 iid likelihood 与 $N(0,\tau^2I)$ prior 推导 MAP。分别在使用 sum NLL 和 mean NLL 时写 penalty coefficient，解释为何代码中固定 `lambda` 的含义会随 $n$ 变化。

### PROB-MLE-C03

证明 MLE 在一一重参数化下具有 equivariance。随后用 $\theta>0$ 的 exponential posterior density $p_\Theta(\theta)=e^{-\theta}$ 与变换 $\phi=\log\theta$ 构造 MAP mode 坐标依赖的具体反例。

## D. 边界、反例与纠错

### PROB-MLE-D01

对完全线性可分的 binary logistic regression，证明沿某个分离方向增大参数范数时 log-likelihood 趋近 supremum 但没有有限 maximizer。L2 penalty 如何改变问题？

### PROB-MLE-D02

考虑两分量 Gaussian mixture，两个 component 的 variance 都可自由趋近零。构造一个参数序列使 likelihood 无界，并解释 label switching 与 component collision 分别造成什么不可辨识/奇异性。

### PROB-MLE-D03

一份代码把 mean cross-entropy 写成 `CE_mean + lambda * ||theta||^2`，另一份把 sum cross-entropy 写成 `CE_sum + lambda * ||theta||^2`，却使用同一个 $\lambda$。证明两者不是同一 MAP objective；给出转换关系，并说明 AdamW 仍不自动等于二者中的 loss penalty。

## E. AI 迁移

### PROB-MLE-E01

对 $K$ 类 softmax classifier 推导 conditional log-likelihood 与 cross-entropy。说明 class weighting、label smoothing、focal loss 和 mixup 分别在哪一步改变了原始 MLE 解释，以及这些修改可能对应什么新目标。

### PROB-MLE-E02

对 autoregressive language model 写出 sequence likelihood、teacher-forced token NLL 与 padding mask 后的 mean loss。比较 per-token、per-sequence 和 length-normalized 三种 reduction 对 estimand 的改变，并列出五项数值/数据审计。

### PROB-MLE-E03

对 energy-based model $p_\theta(x)=e^{-E_\theta(x)}/Z_\theta$，推导 log-likelihood gradient。解释为何负相位需要从模型分布取期望；再说明 NCE、contrastive divergence 或 score matching 改变/近似了什么，不能笼统称为“精确 MLE”。

## 分级提示

- `B01`：posterior 为 $\operatorname{Beta}(S+a,n-S+b)$；mode 公式只在两个 shape 都大于 1 时直接适用；
- `B02`：先对 $\mu$ 优化，再代回 $\sigma^2$；
- `B03`：indicator $\mathbf1\{\theta\ge x_{(n)}\}$ 决定可行域；
- `C03`：density 变换必须带 Jacobian；
- `D01`：若 $y_iw^\top x_i>0$，考察 $tw$；
- `E03`：$\nabla\log Z=-E_{p_\theta}[\nabla E]$ 的符号要仔细。

## 解答入口

完成独立尝试后再打开：[[解答 - 最大似然估计与 MAP]]。

## 本轮复盘

- 是否把 likelihood 当参数概率？
- 是否检查 support 与边界？
- 是否把 stationary point 当成唯一全局 MLE？
- 是否核对 regularization 的尺度、参数化和 optimizer 实现？

