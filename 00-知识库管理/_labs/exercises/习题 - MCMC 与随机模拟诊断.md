---
type: exercise
status: draft
area: [math/statistics, ai/bayesian-computation]
topic: "MCMC 与随机模拟诊断"
difficulty: [A, B, C, D, E]
prerequisites: ["[[MCMC 与随机模拟诊断]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - MCMC 与随机模拟诊断]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - MCMC 与随机模拟诊断

> [!abstract] 训练目标
> 从 invariant kernel 和 detailed balance 推导 MH/Gibbs，计算相关样本 MCSE，并能用多链、R-hat、ESS、HMC diagnostics 和模型重参数化诊断有限时间 bias。

## A. 识别与复述

### PROB-MCMC-A01

定义 Markov kernel、invariant distribution、detailed balance、irreducibility、aperiodicity、ergodicity 与 mixing。哪些是构造正确 target 的条件，哪些涉及从初值收敛？

### PROB-MCMC-A02

区分 posterior SD、MCMC MCSE、bulk ESS、tail ESS、weight ESS 与 $\widehat R$。为什么它们不能互相替代？

### PROB-MCMC-A03

比较 warmup、adaptation、burn-in、sampling 和 thinning。解释“丢掉一半 draws”为什么不是 convergence proof。

## B. 手算与构造

### PROB-MCMC-B01

两状态 chain 的 transition matrix

$$
K=\begin{pmatrix}0.9&0.1\\0.2&0.8\end{pmatrix}.
$$

求 invariant distribution、第二特征值，并从 $X_0=0$ 求 $P(X_t=1)$。解释 spectral factor 与 mixing。

### PROB-MCMC-B02

target $\pi(x)\propto e^{-x^2/2}$，random-walk proposal $Y=X+\varepsilon$、$\varepsilon\sim N(0,s^2)$。写 acceptance；分别分析 $x=2,y=1$ 与 $x=1,y=2$。若改成 asymmetric proposal，指出遗漏 proposal ratio 的后果。

### PROB-MCMC-B03

某 stationary chain 对 functional $f$ 的 autocorrelation 为 $\rho_k=0.8^k$，保存 $N=10\,000$ draws，posterior SD 为 2。求 IACT、ESS 和 posterior mean 的 MCSE。若独立 draws，MCSE 是多少？

## C. 推导与证明

### PROB-MCMC-C01

证明 detailed balance 推出 invariance；再证明 MH accepted flow 满足 detailed balance，说明 normalization constant 为什么抵消。

### PROB-MCMC-C02

证明单坐标 Gibbs update 可视作 acceptance-one MH。解释 scan order/blocked update 为什么仍会影响 autocorrelation，尽管 target 不变。

### PROB-MCMC-C03

从 Markov-chain CLT 推导 asymptotic variance、IACT、ESS 与 MCSE 的关系。说明 ESS 为什么依赖 $f$，以及负 autocorrelation 时 ESS 可能大于 $N$。

## D. 边界、反例与纠错

### PROB-MCMC-D01

构造一个以任意 $\pi$ 为 invariant distribution、却从一般初值永不收敛的 kernel；再构造 periodic chain。指出 invariant、irreducible、aperiodic 分别缺什么。

### PROB-MCMC-D02

构造双峰 target，使四条 chains 若都从同一 mode 启动可有漂亮 trace、$\widehat R\approx1$ 与高局部 ESS，却给出错误 global mean。设计更强诊断/算法。

### PROB-MCMC-D03

反驳三句话：“thinning 修复 autocorrelation”“提高 acceptance 总能改善 MH”“HMC divergence draws 删除即可”。分别给出原理和正确措施。

## E. AI 迁移

### PROB-MCMC-E01

对 hierarchical neural model 的 funnel 写 centered/noncentered parameterization，设计 HMC 诊断与修复流程，并说明何时 noncentering 也可能不优。

### PROB-MCMC-E02

为 Bayesian neural classifier 的 MCMC 结果写最低报告：chains、initialization、warmup、R-hat、bulk/tail ESS、MCSE、divergence/energy、symmetry、function-space summary、PPC 与 SBC。

### PROB-MCMC-E03

对受限文本生成的离散 energy target，设计 MH 的增/删/改 proposals 与 Hastings ratio。解释退火 schedule、stationary sampling、optimization best sample 和 uncertainty report 为什么是四个不同对象。

## 提示

- B01：stationary ratio 满足 $\pi_0(0.1)=\pi_1(0.2)$；
- B03：$\sum_{k\ge1}0.8^k=4$；
- C02：proposal density 就是对应 full conditional；
- D01：identity kernel 与 deterministic two-cycle；
- D02：让 mode separation 远大于 proposal scale。

## 解答入口

完成独立尝试后再打开：[[解答 - MCMC 与随机模拟诊断]]。
