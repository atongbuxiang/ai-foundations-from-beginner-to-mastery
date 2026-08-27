---
type: solution
status: draft
area: [math/statistics, ai/bayesian-computation]
topic: "MCMC 与随机模拟诊断"
exercise: "[[习题 - MCMC 与随机模拟诊断]]"
prerequisites: ["[[MCMC 与随机模拟诊断]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
sources: ["Hastings-1970", "Vehtari-et-al-2021-Rhat-ESS", "Stan-Reference-Manual-MCMC"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - MCMC 与随机模拟诊断

> [!warning] 使用边界
> “kernel 以 posterior 为 invariant distribution”是渐近正确性的结构声明；“有限次计算已充分探索 posterior”是另一个必须靠初始化、跨链比较、ESS、MCSE、几何诊断与问题特定检查支持的经验声明。

## A. 识别与复述

### PROB-MCMC-A01

Markov kernel $K(x,A)$ 给出当前状态 $x$ 到集合 $A$ 的一步转移概率。分布 $\pi$ invariant 是指

$$
\int \pi(dx)K(x,A)=\pi(A)
$$

对所有 measurable $A$ 成立。detailed balance 是更强且易验证的充分条件：

$$
\pi(dx)K(x,dy)=\pi(dy)K(y,dx).
$$

- invariance/detailed balance 解决“若已经处于 $\pi$，一步后是否仍为 $\pi$”；
- irreducibility 排除 target 的正质量区域彼此不可达；
- aperiodicity 排除状态按固定周期振荡；
- ergodicity 指从允许的初值出发，分布/时间平均以适当意义收敛到 $\pi$；
- mixing 描述有限时间靠近 $\pi$ 的速度，而不只是最终是否收敛。

所以 detailed balance 不是 convergence 的必要条件，invariance 也不保证一般初值会收敛。实际还需相应 state-space 上的 recurrence、irreducibility 等正则条件。

### PROB-MCMC-A02

| 量 | 回答的问题 |
|---|---|
| posterior SD | target distribution 对参数/functional 的实质不确定性多大 |
| MCMC MCSE | 有限相关 draws 对某个 Monte Carlo estimate 额外引入多少数值误差 |
| bulk ESS | distribution 中心位置相关 summaries 的等效独立样本量 |
| tail ESS | quantiles/tails 是否有足够有效 draws |
| weight ESS | importance/SMC weights 是否退化，通常是 $(\sum w)^2/\sum w^2$ |
| $\widehat R$ | 多链之间与链内变异是否相容，是未收敛预警而非充分证明 |

posterior SD 不会随保存更多 MCMC draws 消失；MCSE 应随有效计算量下降。高 bulk ESS 不能保证 tails，高 $\widehat R$ 是问题证据而低 $\widehat R$ 不是全局探索证明。MCMC ESS 与 weight ESS 来自不同依赖机制，数值相同也不等价。

### PROB-MCMC-A03

- adaptation：用早期轨迹调 proposal scale、mass matrix、step size 等；为保持目标性质，通常不把这些 draws 当固定-kernel samples；
- warmup：包含进入典型集和 adaptation 的运行阶段；
- burn-in：传统上指丢弃初始非平稳 draws，但单纯删除没有验证收敛；
- sampling：固定或满足合法 adaptation 条件后，用于估计的阶段；
- thinning：每隔 $k$ 个 draws 保存一个，主要缓解存储/昂贵后处理，不会创造原轨迹中不存在的信息。

丢掉一半 draws 只改变一个人为截点。慢 mode、funnel、不同对称 mode 或错误几何都可能在后半段继续存在；因此它不是 convergence proof。应以多条分散初始化的 chains、rank-normalized split-$\widehat R$、bulk/tail ESS、MCSE、trace/rank plots 与 sampler-specific diagnostics 联合判断。

## B. 手算与构造

### PROB-MCMC-B01

令 $\pi=(\pi_0,\pi_1)$。stationary flow 满足

$$
0.1\pi_0=0.2\pi_1,
\qquad \pi_0+\pi_1=1,
$$

故

$$
\pi=\left(\frac23,\frac13\right).
$$

二维 stochastic matrix 的一个特征值为 1，另一个是 trace 减 1：

$$
\lambda_2=0.9+0.8-1=0.7.
$$

写 $p_t=P(X_t=1\mid X_0=0)$，则

$$
p_{t+1}=0.1(1-p_t)+0.8p_t=0.1+0.7p_t.
$$

固定点为 $1/3$，$p_0=0$，所以

$$
p_t=\frac13\left(1-0.7^t\right).
$$

与 stationary probability 的误差按 $0.7^t$ 衰减。此例中 spectral gap $1-|\lambda_2|=0.3$；第二特征值绝对值越靠近 1，最慢线性 mode 越持久。一般非可逆/高维 chain 不能只靠一个实特征值概括 mixing。

### PROB-MCMC-B02

random-walk Gaussian proposal 对称：$q(y\mid x)=q(x\mid y)$。因此

$$
\alpha(x,y)
=\min\left\{1,\frac{\pi(y)}{\pi(x)}\right\}
=\min\{1,e^{-(y^2-x^2)/2}\}.
$$

从 $x=2$ 到 $y=1$：

$$
e^{-(1-4)/2}=e^{1.5}>1,
$$

故接受概率为 1。从 $x=1$ 到 $y=2$：

$$
\alpha=e^{-1.5}\approx0.2231.
$$

非对称 proposal 必须使用 Hastings correction：

$$
\alpha(x,y)=\min\left\{1,
\frac{\pi(y)q(x\mid y)}{\pi(x)q(y\mid x)}
\right\}.
$$

遗漏 proposal ratio 后，forward/backward probability flow 不再匹配 $\pi$；chain 通常收敛到错误分布。target normalization constant 仍会抵消，但 proposal asymmetry 不会自动抵消。

### PROB-MCMC-B03

integrated autocorrelation time：

$$
\tau_f=1+2\sum_{k=1}^\infty\rho_k
=1+2\sum_{k=1}^\infty0.8^k
=1+2(4)=9.
$$

于是

$$
\operatorname{ESS}_f=\frac{10{,}000}{9}\approx1111.1.
$$

posterior mean estimate 的 MCSE：

$$
\operatorname{MCSE}(\bar f)
\approx\frac{2}{\sqrt{1111.1}}
\approx0.060.
$$

若 draws 独立，ESS 为 10,000，

$$
\operatorname{MCSE}_{\rm iid}=\frac2{100}=0.020.
$$

这里相关性把 variance 放大 9 倍、standard error 放大 3 倍。

## C. 推导与证明

### PROB-MCMC-C01

由 detailed balance，对任意 measurable $A$：

$$
\begin{aligned}
\int\pi(dx)K(x,A)
&=\int_A\int\pi(dx)K(x,dy)\\
&=\int_A\int\pi(dy)K(y,dx)\\
&=\int_A\pi(dy)\\
&=\pi(A),
\end{aligned}
$$

所以 $\pi$ invariant。

MH 的 accepted off-diagonal flow 为

$$
\pi(x)q(y\mid x)\alpha(x,y).
$$

令

$$
r(x,y)=\frac{\pi(y)q(x\mid y)}{\pi(x)q(y\mid x)}.
$$

则

$$
\begin{aligned}
\pi(x)q(y\mid x)\min\{1,r(x,y)\}
&=\min\{\pi(x)q(y\mid x),\pi(y)q(x\mid y)\}\\
&=\pi(y)q(x\mid y)\min\{1,r(y,x)\},
\end{aligned}
$$

故 accepted moves 可逆；rejection 的 self-loop flow 也天然对称。若 $\pi(x)=\widetilde\pi(x)/Z$，ratio 中同一个 $Z$ 分子分母抵消，因此只需 unnormalized target。

### PROB-MCMC-C02

更新第 $j$ 个坐标时，保留 $x_{-j}$，proposal 为

$$
q(y\mid x)=p(y_j\mid x_{-j})\mathbf1\{y_{-j}=x_{-j}\}.
$$

在共同支持上，target 分解为

$$
\pi(x)=\pi(x_{-j})p(x_j\mid x_{-j}).
$$

MH ratio：

$$
\frac{\pi(y)q(x\mid y)}{\pi(x)q(y\mid x)}
=\frac{\pi(x_{-j})p(y_j\mid x_{-j})p(x_j\mid x_{-j})}
{\pi(x_{-j})p(x_j\mid x_{-j})p(y_j\mid x_{-j})}
=1.
$$

所以 full-conditional Gibbs proposal 总被接受。

但 acceptance one 不等于 independent sampling。强相关坐标逐个更新时，每步只沿狭窄 conditional 移动；blocked update 可一起跨越相关方向。systematic/random scan 的 transition kernel 不同，虽都保持同一 target，却可有截然不同的 spectrum、自相关与有限时间 mixing。

### PROB-MCMC-C03

在适当 ergodicity 与矩条件下，Markov-chain CLT 给出

$$
\sqrt N(\bar f_N-E_\pi f)
\Rightarrow N(0,\sigma_f^2),
$$

其中

$$
\sigma_f^2
=\gamma_0+2\sum_{k=1}^\infty\gamma_k
=\gamma_0\left(1+2\sum_{k=1}^\infty\rho_k\right)
=\gamma_0\tau_f.
$$

故

$$
\operatorname{Var}(\bar f_N)\approx\frac{\gamma_0\tau_f}{N}
=\frac{\gamma_0}{N/\tau_f}.
$$

据此定义

$$
\operatorname{ESS}_f=\frac N{\tau_f},
\qquad
\operatorname{MCSE}(\bar f_N)
\approx\sqrt{\frac{\widehat{\gamma_0}}{\widehat{\operatorname{ESS}}_f}}.
$$

不同 $f$ 投影到 chain 的慢 mode 程度不同，故 ESS 必须带下标；parameter mean 的 ESS 不能替代 tail indicator、log density 或 predictive functional 的 ESS。若一段 lag autocorrelations 为负，使 $\tau_f<1$，时间平均可比 iid draws 更稳定，于是 function-specific ESS 可大于 $N$；这不代表拥有超过 $N$ 个独立原始 states。

## D. 边界、反例与纠错

### PROB-MCMC-D01

对任意 $\pi$，identity kernel

$$
K(x,A)=\mathbf1\{x\in A\}
$$

保持每一个分布，因而也保持 $\pi$。但从 $X_0=x_0$ 出发，$X_t=x_0$ 永远不变；除非初值本就按 $\pi$ 抽取，否则 marginal 不会趋向 $\pi$。它缺少跨状态的 irreducibility。

再取两状态 deterministic flip：$K(0,1)=K(1,0)=1$。它以 $(1/2,1/2)$ 为 invariant distribution，且两状态互相可达，但 period 为 2。从固定初值出发，marginal 在两个点质量间振荡，不逐步收敛。它说明 irreducible 仍不够，还需 aperiodicity；加入正概率 self-loop 可打破周期。

### PROB-MCMC-D02

令

$$
\pi(x)=\tfrac12N(-20,1)+\tfrac12N(20,1).
$$

四条 random-walk chains 若全从 $-20$ 附近启动且 proposal scale 约为 1，在现实运行长度内可能都只探索左峰。它们彼此相似，local trace 看似稳定，rank-$\widehat R$ 可接近 1，local ESS 也可很高；但 estimated mean 接近 $-20$，真 mean 是 0。

更强方案：

1. 从 overdispersed initializations 启动，包括两个峰及低密度区域；
2. 用不同算法/温度：parallel tempering、tempered transitions、SMC 或 mode-jumping proposals；
3. 画 energy/log-density、mode occupancy 与跨链 rank，而不只看单参数局部 trace；
4. 若对称来自 label switching，用 permutation-invariant 或 function-space summaries；
5. 用已知模拟 truth 做 SBC，或在低维问题用 quadrature/独立算法交叉核验；
6. 报告没有观察到跨峰转换这一有限时间事实，不能用低 $\widehat R$ 把它抹掉。

### PROB-MCMC-D03

**“thinning 修复 autocorrelation”**：每隔 $k$ 步保留一次会降低保存样本的相邻相关，却丢弃中间信息。在固定计算预算下，保留全部 draws 后正确估计 spectral variance/ESS 通常更有效。只有存储、I/O 或单 draw 后处理极昂贵时，thinning 才可能是工程折中。

**“提高 acceptance 总能改善 MH”**：proposal 极小可使 acceptance 接近 1，却几乎原地踏步，ESS 很低；proposal 太大又会频繁拒绝。目标是每单位计算成本的有效探索，不是最大 acceptance。应调 proposal geometry/scale，比较 ESS/sec、jump distance 和 mode traversal。

**“HMC divergence draws 删除即可”**：divergence 表明数值积分无法可靠穿过 posterior 的高曲率几何；它们常集中在 funnel 等关键区域。删掉只是选择性移除困难区域，会加重 bias。正确措施是检查 divergence 位置，重参数化、标准化、使用更合理 prior，必要时提高 target acceptance/减小 step size，并重新运行；若仍存在，不能把结果称为已验证。

## E. AI 迁移

### PROB-MCMC-E01

考虑 group-level neural parameters：

$$
w_j\sim N(\mu,\tau^2),
\qquad y_j\sim p(y_j\mid w_j).
$$

centered parameterization 直接采 $(\mu,\tau,w_j)$：

$$
w_j=\text{parameter},\qquad w_j\sim N(\mu,\tau^2).
$$

noncentered 写成

$$
z_j\sim N(0,1),
\qquad w_j=\mu+\tau z_j.
$$

当数据对各 $w_j$ 信息弱、$\tau$ 可接近 0 时，centered posterior 易形成 funnel；noncentering 把 prior geometry 近似球化。诊断/修复流程：

1. 至少四条分散 chains，足够 warmup，检查 step size 与 mass-matrix adaptation；
2. 查 rank-$\widehat R$、bulk/tail ESS、MCSE、divergences、maximum treedepth 与 energy/BFMI 类诊断；
3. 将 divergences 映射到 $\tau,w_j,z_j$ 和 log density；
4. 尝试 noncentering/partial noncentering、predictor scaling 与更有信息且科学合理的 scale priors；
5. 重新运行并比较 function-space predictions、PPC 与 SBC。

若每组数据非常强，$w_j$ 已被 likelihood 紧密识别，centered coordinates 可能更接近 posterior geometry；完全 noncentered 反而引入强 posterior dependence。不存在对所有数据强度都最优的参数化。

### PROB-MCMC-E02

Bayesian neural classifier 的最低可复核报告应包含：

- target：完整 prior、likelihood、数据预处理、constraint/Jacobian 与代码/版本；
- computation：chain 数、每链 seed/initialization、warmup 与 sampling draws、adaptation 配置；
- convergence：所有关键 scalar 与 predictive functionals 的 rank-$\widehat R$，bulk/tail ESS 和 MCSE；
- HMC：divergence 数及位置、treedepth saturation、energy diagnostics、step size 与 mass matrix；
- symmetry：hidden-unit permutation/sign/scale symmetries 如何处理；weight-space 均值若无意义，则报告 invariant/function-space quantities；
- predictive：test points 上 probability、calibration、decision loss 与 posterior predictive intervals；
- model checking：prior predictive check 与 posterior predictive check；
- algorithm validation：在可模拟模型下 SBC，必要时用较小网络/替代算法交叉核验；
- limitations：未跨越的 modes、低 tail ESS、MCSE 相对科学误差的比例，以及哪些结论因此不能下。

仅给 loss curve 或一张看似平稳的 trace 不能证明 posterior computation 可靠。

### PROB-MCMC-E03

令文本 $x$ 的 target 为 $\pi_T(x)\propto e^{-E(x)/T}$，并用 move-type probability $r_m(x)$：

- add：选 insertion position 与 token，$q_{\rm add}(y\mid x)=r_{\rm add}(x)/(L+1)\cdot g(a\mid x)$；reverse 是从 $y$ 中删对应位置；
- delete：选一个可删位置，$q_{\rm del}(y\mid x)=r_{\rm del}(x)/L$；reverse 是在指定位置加回原 token；
- replace：选位置与新 token，$q_{\rm rep}(y\mid x)=r_{\rm rep}(x)/L\cdot g(a'\mid x,i)$。

每个 move 都用

$$
\alpha(x,y)=\min\left\{1,
e^{-[E(y)-E(x)]/T}
\frac{q(x\mid y)}{q(y\mid x)}
\right\}.
$$

长度改变时，position count、token proposal、move-type probability 和 reverse feasibility 都进入 Hastings ratio；遗漏任何一项都可能改变 stationary distribution。还要确保约束集合内 irreducible，例如不能因 grammar filter 把合法文本分成不可达 components。

四个对象必须分开：

1. 固定 $T$、合法 kernel 的 stationary sampling，目标是 $\pi_T$；
2. 随时间降温的 simulated annealing 是非齐次 chain，目标偏向 optimization，不等于从某个固定 posterior 抽样；
3. 运行中能量最低的 best sample 是极值选择，不是 posterior draw；
4. uncertainty report 需要固定、明确的 target 和经诊断的 representative draws，不能用 annealing 的 best-of-run 集合冒充概率质量。

## 本章验收

- 能从 invariant flow 推导 MH 与 Gibbs，而不把 detailed balance 误当必要条件；
- 能计算 IACT、function-specific ESS 与 MCSE，并与 posterior uncertainty 分离；
- 能用反例说明 invariance、低 $\widehat R$、高 acceptance 都不是有限时间正确性证明；
- 能诊断 multimodality、funnel、divergence、tail failure 与 symmetry；
- 能为连续 HMC 和离散文本 MH 写出可复核的 target、proposal、diagnostics 与报告边界。

