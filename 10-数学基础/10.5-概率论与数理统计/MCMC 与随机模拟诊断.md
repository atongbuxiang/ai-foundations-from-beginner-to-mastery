---
type: concept
status: draft
area: [math/statistics, ai/bayesian-computation, ai/sampling]
aliases: [Markov chain Monte Carlo, MCMC, Metropolis-Hastings, Gibbs sampling, HMC, R-hat, effective sample size]
prerequisites: ["[[Bayesian 推断与后验预测]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[条件概率、全概率与 Bayes 公式]]", "[[随机变量的收敛与大数定律]]"]
related: ["随机过程与 Markov 链基础（待 10.9 扩展）", "Hamiltonian Monte Carlo（本章含基础介绍）", "[[概率论与数理统计 MOC]]"]
sources: ["Hastings-1970-Monte-Carlo-Markov-Chains", "Gelman-et-al-Bayesian-Data-Analysis", "Vehtari-et-al-2021-Rhat-ESS", "Stan-Reference-Manual-Posterior-Analysis", "Stan-Reference-Manual-MCMC", "Su-2021-8084-MCMC-Annealing"]
created: 2026-08-19
updated: 2026-08-27
---

# MCMC 与随机模拟诊断

> [!abstract] 本章主问题
> MCMC 不直接产生 iid target samples，而是设计一个以目标分布为 invariant distribution 的 Markov chain，再用 ergodic average 近似期望。stationarity 只说明目标分布在转移下保持不变，不保证从任意初值快速到达；因此任何 posterior summary 都必须同时报告多链混合、rank-normalized $\widehat R$、bulk/tail ESS、MCSE 与算法特有诊断，且这些诊断没有任何一个能单独证明全局收敛。

## 学习目标

完成本节后，你应当能够：

1. 定义 Markov kernel、invariant/stationary distribution、detailed balance 与 ergodicity；
2. 区分“目标 invariant”与“链已从当前初值混合到目标”；
3. 从 detailed balance 推导 Metropolis–Hastings acceptance probability；
4. 推导 Gibbs sampling 是 MH 的 acceptance-one 特例；
5. 解释 MCMC ergodic theorem、autocorrelation、integrated autocorrelation time、ESS 与 MCSE；
6. 区分 warmup、adaptation、burn-in、sampling 与 thinning；
7. 使用多条过分散 chains、rank/folded split-$\widehat R$、bulk/tail ESS、trace/rank plots；
8. 解释 HMC/NUTS、leapfrog、Metropolis correction、divergence 与 energy diagnostics；
9. 识别 multimodality、funnel、label switching、heavy tail、boundary 与 discrete structure 的失败；
10. 把 posterior uncertainty、data uncertainty、model error 与 MCMC numerical error 分开。

> [!question] 初学者读完必须能回答
> 1. Markov kernel、invariant distribution、detailed balance 与 ergodicity 分别是什么？
> 2. 为什么 $\pi K=\pi$ 不等于当前初值出发的链已经接近 $\pi$？
> 3. Metropolis–Hastings acceptance ratio 怎样保证 detailed balance，Gibbs 又为何可视为 acceptance-one 特例？
> 4. MCMC ergodic average 与 iid Monte Carlo 的方差、CLT 和误差估计有何不同？
> 5. autocorrelation time、ESS 与 MCSE 如何连接，为什么 ESS 依赖目标函数或分布区域？
> 6. warmup、adaptation、sampling 与 thinning 应怎样区分？
> 7. 多链 $\widehat R$、bulk/tail ESS、trace/rank、divergence 与 energy 诊断为什么必须联合使用？

## 阅读前检查

- [[Bayesian 推断与后验预测]]：目标 posterior 与要估的 posterior functional；
- [[Monte Carlo、重要性采样与方差缩减]]：MCSE、ESS、support 与 independent Monte Carlo；
- [[随机变量的收敛与大数定律]]：ergodic average 也是一种 LLN，但条件不再是 iid；
- [[条件概率、全概率与 Bayes 公式]]：Gibbs full conditional 与 Bayesian factorization。

## 零、为什么需要 MCMC

目标 density 常只知道到归一化常数：

$$
\pi(x)=\frac{\widetilde\pi(x)}Z,
\qquad
Z=\int\widetilde\pi(x)dx.
$$

Bayesian posterior 中：

$$
\widetilde\pi(\theta)
=p(y\mid\theta)p(\theta),
$$

evidence $Z=p(y)$ 可能高维难算。我们希望估计

$$
\mu=E_\pi[f(X)]
=\int f(x)\pi(x)dx.
$$

直接 iid sampling 不可行时，构造相关序列

$$
X_0,X_1,\ldots,X_N
$$

使其长期访问频率服从 $\pi$，再用

$$
\widehat\mu_N=\frac1N\sum_{t=1}^Nf(X_t).
$$

先用下图回答一个视觉问题：**目标分布不变性、相关样本的有效样本量与多链诊断为什么是三层不同的可信度问题？**

![[00-知识库管理/_assets/figures/probability/fig-mcmc-kernel-diagnostics-v2.svg|880]]

> [!figure] 图 10.5.20｜MCMC 不变性、自相关 ESS 与多链诊断组合
> A 区分 $\pi K=\pi$ 的不变性与从初始分布 $\nu_0$ 到 $\pi$ 的实际混合；B 用黏滞 trace 与缓慢衰减的 autocorrelation 表示 $N$ 次迭代只对应更小 ESS；C 将 rank/folded split-$\widehat R$、bulk/tail ESS、MCSE、trace/rank 与算法失败信号并列。来源：独立绘制；生成脚本：[[plot_statistical_inference_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 分别沿上下两条链读“保持目标”和“接近目标”，不要从前者推出后者；B 同时看 trace 的长程结构与 ACF 衰减，再用目标函数相关的长程方差解释 ESS/MCSE；C 要求多个过分散初值的链在中心与尾部均有足够混合，并与 sampler-specific 诊断交叉核对。

**适用边界（图没有证明什么）。** 平滑 trace 是构造示意，不能用视觉平稳证明遍历性；截断 ACF 和 ESS 都是估计量，重尾、多峰与非平稳链会使其不可靠；$\widehat R\approx1$ 也不能证明链发现了未访问模态，HMC divergence 消失更不等于模型几何良好。

## 进入正文前：先区分“目标正确”与“这次计算已经可靠”

> [!info] 课程位置
> 前三章分别给出局部渐近精度、完整 posterior 和重复抽样检验；本章处理计算层：当 posterior 只知道到归一化常数且不能直接采样时，怎样构造相关 Markov chain 近似期望。它是概率卷的收口节点，但 MCMC 误差不能替代模型不确定性、数据误差或检验设计。

> [!tip] 建议两遍阅读
> - 第一遍只理解 Metropolis–Hastings 的 proposal、接受率与详细平衡，并用可解析 Beta posterior 校准均值和尾概率。
> - 第二遍再学习 invariant kernel、ergodicity、autocorrelation time、ESS/MCSE、warmup/adaptation、rank-normalized $\widehat R$、HMC/NUTS 和多峰/funnel 边界。任何单一诊断都不构成收敛证明。

> [!question] 本章的推导问题链
> 1. 为什么知道未归一化 target 就足以构造 MH？
> 2. detailed balance 怎样保证 target invariant？
> 3. target invariant 为什么不表示当前初值已经混合？
> 4. 相关样本的 Monte Carlo 方差为何不能按 iid 样本数计算？
> 5. ESS、MCSE、$\widehat R$、trace/rank 和算法诊断分别检查什么？
> 6. 高接受率为什么可能只是 proposal 步长过小？
> 7. 怎样用解析真值校准 sampler，而不是只凭图形“看起来不错”？

### 贯穿例：用 prior 作为 independence proposal 采 Beta posterior

目标 posterior 为

$$
\pi(q)=\operatorname{Beta}(5,9),
\qquad
\widetilde\pi(q)=q^4(1-q)^8,
\qquad 0<q<1.
$$

这个例子可以直接采样，但我们故意使用 MCMC，因为解析真值能成为严格校准门：

$$
\mathbb E_\pi[Q]=\frac5{14},
\qquad
\operatorname{Var}_\pi(Q)=\frac3{196},
$$

$$
P_\pi(Q>1/2)=\frac{1093}{8192},
\qquad
P(M_{\mathrm{new}}=2\mid y)=\frac17.
$$

选择与当前状态无关的 independence proposal

$$
q'\sim g=\operatorname{Beta}(2,2),
\qquad
g(q)\propto q(1-q).
$$

Metropolis–Hastings 接受概率为

$$
\alpha(q,q')
=\min\left\{
1,
\frac{\widetilde\pi(q')g(q)}
{\widetilde\pi(q)g(q')}
\right\}.
$$

由于 proposal 就是 prior，而 posterior kernel 等于 likelihood 乘 prior，prior 因子消去：

$$
\alpha(q,q')
=\min\left\{
1,
\frac{(q')^3(1-q')^7}
{q^3(1-q)^7}
\right\}.
$$

归一化常数 $B(5,9)$ 和 $B(2,2)$ 都消失，这正是 MCMC 适合只知道 target 到常数的原因。

一次转移为：

1. 从 $g$ 独立提出 $q'$；
2. 计算 $\alpha(q,q')$；
3. 以概率 $\alpha$ 接受 $q'$，否则保留 $q$。

接受/拒绝机制产生自相关，因为拒绝时状态重复。对函数 $f(q)$，链平均

$$
\widehat\mu_N=\frac1N\sum_{t=1}^Nf(Q_t)
$$

的渐近方差涉及整条 autocorrelation：

$$
\operatorname{Var}(\widehat\mu_N)
\approx
\frac{\sigma_f^2}{N}
\left(1+2\sum_{k\ge1}\rho_k\right).
$$

因此定义

$$
N_{\mathrm{eff}}
\approx
\frac{N}{1+2\sum_{k\ge1}\rho_k}.
$$

同一条链对 posterior mean、尾部 indicator $\mathbf1_{\{q>1/2\}}$ 和 predictive functional 的 ESS 可以不同；只报一个统一 ESS 会丢掉目标函数差异。

#### 本例的数值验真合同

至少运行多条从分散初值出发的 chains，并同时检查：

- 各链是否访问 posterior 主体与 $q>1/2$ 尾部；
- rank/folded split-$\widehat R$ 是否接近 $1$；
- bulk 与 tail ESS 是否足以支持目标摘要；
- posterior mean 是否接近 $5/14$；
- posterior variance 是否接近 $3/196$；
- tail probability 是否接近 $1093/8192$；
- MCSE 是否小于希望报告的有效数字；
- 接受率、trace/rank 和 sampler-specific failures 是否相互一致。

高接受率本身不是好消息。极小步长 random-walk proposal 可能几乎每步都接受，却只在狭小局部缓慢移动，导致 autocorrelation 高、ESS 低。相反，适度拒绝但能跨越 posterior 主体的 proposal 可能更有效。

> [!note] 本轮对象账本
> | 对象 | 类型 | 本例 |
> |---|---|---|
> | $\widetilde\pi$ | 未归一化 target | $q^4(1-q)^8$ |
> | $g$ | proposal density | Beta$(2,2)$ |
> | $K(q,dq')$ | Markov transition kernel | proposal 加 MH 接受/拒绝 |
> | $\pi K=\pi$ | 不变性恒等式 | target 在一步转移下保持不变 |
> | $Q_t$ | 相关随机序列 | chain 第 $t$ 个状态 |
> | ESS/MCSE | 目标函数相关的估计诊断 | 有效信息量与数值标准误 |
> | $\widehat R$ | 多链诊断 | 链间与链内尺度是否相容 |

> [!analysis] Metropolis–Hastings 接受率的公式七问
> 1. **为什么引入？** proposal 便于采样但不是 target，接受率校正其方向性和密度差异。
> 2. **对象是什么？** 当前状态 $q$、候选 $q'$、未归一化 target $\widetilde\pi$ 和 proposal kernel $g(q'\mid q)$。
> 3. **条件是什么？** proposal 必须使 target 支持可达，并配合不可约性、非周期性/遍历条件；公式正确不保证快速混合。
> 4. **怎样推出？** 令正反概率流 $\pi(q)g(q'\mid q)\alpha(q,q')$ 满足 detailed balance，取比率截断于 $1$。
> 5. **为什么不需要 evidence？** target 正反比值中的共同归一化常数完全消去。
> 6. **边界在哪里？** 支持断裂、多峰、重尾、funnel 和高维尺度失配会使链极慢；$\widehat R\approx1$ 也可能遗漏所有链都未访问的模态。
> 7. **AI 中对应什么？** Bayesian neural network、energy-based model 和 latent posterior 可能用 MCMC；必须把 posterior uncertainty 与有限链 MCSE、warmup bias 和算法失败信号分开报告。

> [!success] 第一遍停靠线
> 应能写出 Beta$(5,9)$ target 与 Beta$(2,2)$ independence proposal 的 MH ratio，并解释 prior 因子为何消去；能区分 invariant、mixed 与 iid；还能列出均值 $5/14$、方差 $3/196$、尾概率 $1093/8192$ 三个解析校准目标，以及为什么接受率不能替代 ESS、$\widehat R$ 和多链图。

## 一、Markov kernel

Markov property：

$$
P(X_{t+1}\in A\mid X_0,\ldots,X_t)
=P(X_{t+1}\in A\mid X_t).
$$

transition kernel：

$$
K(x,A)=P(X_{t+1}\in A\mid X_t=x).
$$

若当前 distribution 为 $\nu$，一步后的 distribution：

$$
(\nu K)(A)=\int K(x,A)\nu(dx).
$$

$t$ 步 kernel 记 $K^t$。

## 二、Invariant distribution 不等于已经收敛

$\pi$ invariant/stationary 若

$$
\pi K=\pi,
$$

即

$$
\pi(A)=\int K(x,A)\pi(dx).
$$

含义：

> 若 $X_t\sim\pi$，则 $X_{t+1}\sim\pi$。

它没有说明：

$$
\delta_{x_0}K^t\to\pi
$$

对所有初值成立，更没有说明有限 $t$ 已经足够接近。

反例：identity kernel

$$
K(x,A)=1\{x\in A\}
$$

让每个 distribution 都 invariant，但链永远停在初值，无法采样。

## 三、从 invariant 到 convergence 还需要什么

有限状态直觉中通常需要：

- irreducible：任意有正 target probability 的区域最终可到达；
- aperiodic：不被固定周期锁住；
- positive recurrent：返回时间适当有限；
- unique invariant distribution。

一般状态空间使用 $\pi$-irreducibility、Harris recurrence、drift/minorization 等更严格条件。

convergence 常表示 total variation：

$$
\|K^t(x,\cdot)-\pi\|_{\rm TV}\to0.
$$

mixing rate 可能 geometric、polynomial，甚至慢到实践不可用。理论 ergodic 并不等于计算可行。

## 四、Detailed balance：充分但非必要

若

$$
\pi(dx)K(x,dy)
=\pi(dy)K(y,dx),
$$

称 reversible/detailed balance。

对 $y$ 积分：

$$
\int\pi(dx)K(x,dy)
=\pi(dy)\int K(y,dx)
=\pi(dy),
$$

故 $\pi$ invariant。

detailed balance 是构造 invariant kernel 的方便充分条件，不是必要条件。nonreversible chains 也可有正确 invariant distribution，且有时 mixing 更快。

## 五、Metropolis–Hastings 算法

当前状态 $x$：

1. proposal

$$
y\sim q(y\mid x);
$$

2. acceptance probability

$$
\alpha(x,y)
=\min\left\{
1,
\frac{\widetilde\pi(y)q(x\mid y)}
{\widetilde\pi(x)q(y\mid x)}
\right\};
$$

3. 以概率 $\alpha(x,y)$ 接受 $X_{t+1}=y$，否则 $X_{t+1}=x$。

$Z$ 在 ratio 中抵消，这是 MCMC 能处理 unnormalized density 的关键。

### 数值实现

在 log domain：

$$
\log r
=\log\widetilde\pi(y)-\log\widetilde\pi(x)
+\log q(x\mid y)-\log q(y\mid x).
$$

生成 $\log U$，$U\sim U(0,1)$，接受当

$$
\log U<\min(0,\log r).
$$

避免直接 exponentiate 巨大/极小 density。

## 六、为什么 MH 满足 detailed balance

off-diagonal transition flow：

$$
\pi(x)q(y\mid x)\alpha(x,y).
$$

代入 acceptance：

$$
\begin{aligned}
\pi(x)q(y\mid x)\alpha(x,y)
&=\min\{
\pi(x)q(y\mid x),
\pi(y)q(x\mid y)
\}\\
&=\pi(y)q(x\mid y)\alpha(y,x).
\end{aligned}
$$

所以 accepted moves 的双向 flow 相等；rejection 只在对角线上保留质量，也满足 balance。故 $\pi$ invariant。

> [!warning] 正确 invariant 仍不保证可用
> proposal 若跨不过 mode、步长极小或 support 不连通，MH 可理论正确但有限计算中严重 bias。

## 七、Random-walk MH

对称 proposal：

$$
y=x+\varepsilon,
\qquad
\varepsilon\sim q_0,\quad q_0(u)=q_0(-u).
$$

$q$ ratio 消失：

$$
\alpha(x,y)
=\min\left\{1,\frac{\widetilde\pi(y)}{\widetilde\pi(x)}\right\}.
$$

步长权衡：

- 太小：acceptance 高但移动慢，autocorrelation 大；
- 太大：proposal 到低 density 区，rejection 多；
- 高维：局部 random walk 常需缩小 step，mixing 恶化；
- anisotropic posterior：单一 isotropic scale 无法同时适应所有方向。

acceptance rate 不是目标本身；相同 rate 可对应完全不同的 global exploration。

## 八、Independence MH

proposal 不依赖当前状态：

$$
y\sim q(y).
$$

acceptance：

$$
\alpha(x,y)
=\min\left\{
1,
\frac{\widetilde\pi(y)q(x)}
{\widetilde\pi(x)q(y)}
\right\}.
$$

它像 importance sampling ratio 的动态比较。若 $q$ 比 target 尾更轻或漏 mode，链可能长时间卡住；理想 proposal 需覆盖 target 全部重要区域。

## 九、Gibbs sampling

对

$$
\pi(x_1,\ldots,x_d),
$$

依次从 full conditionals 抽：

$$
X_j^{(t+1)}
\sim
\pi(x_j\mid x_1^{(t+1)},\ldots,
x_{j-1}^{(t+1)},x_{j+1}^{(t)},\ldots,x_d^{(t)}).
$$

若把只更新坐标 $j$ 的 proposal 设为其 exact full conditional，MH ratio 化为 1，因此接受率 100%。

### 100% 接受不等于高效

高度相关 Gaussian 中逐坐标 Gibbs 可能沿窄斜谷缓慢移动。改进：

- block correlated variables；
- rotate/whiten；
- collapsed Gibbs 积分掉 nuisance variables；
- noncentered parameterization；
- interweaving。

## 十、一个二维 Gaussian 的 Gibbs 直觉

设

$$
\begin{pmatrix}X\\Y\end{pmatrix}
\sim N\left(
0,
\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}
\right).
$$

conditionals：

$$
X\mid Y=y\sim N(\rho y,1-\rho^2),
$$

$$
Y\mid X=x\sim N(\rho x,1-\rho^2).
$$

当 $|\rho|\to1$，conditional variance 趋零，链每步只沿极窄方向移动，autocorrelation 接近 1。marginals 虽标准 Gaussian，坐标 Gibbs 仍会很慢；geometry 比“每步能抽 exact conditional”更关键。

## 十一、Ergodic theorem

在适当 Harris ergodicity 与 $E_\pi|f|<\infty$ 下：

$$
\frac1N\sum_{t=1}^Nf(X_t)
\xrightarrow{\text{a.s.}}
E_\pi[f(X)].
$$

这是 MCMC consistency。它不要求每个 $X_t$ 独立，也不意味着有限 $N$ 误差小。

若还满足 Markov chain CLT 条件：

$$
\sqrt N(\widehat\mu_N-\mu)
\xrightarrow dN(0,\sigma_f^2),
$$

其中 asymptotic variance：

$$
\sigma_f^2
=\gamma_0+2\sum_{k=1}^\infty\gamma_k,
$$

$$
\gamma_k
=\operatorname{Cov}_\pi(f(X_0),f(X_k)).
$$

## 十二、IACT、ESS 与 MCSE

若 $\gamma_0=\operatorname{Var}_\pi(f)>0$，autocorrelation

$$
\rho_k=\gamma_k/\gamma_0.
$$

integrated autocorrelation time：

$$
\tau_f
=1+2\sum_{k=1}^\infty\rho_k.
$$

于是

$$
\sigma_f^2=\gamma_0\tau_f.
$$

function-specific ESS：

$$
N_{\rm eff,f}
=\frac N{\tau_f}.
$$

mean 的 MCSE：

$$
\operatorname{MCSE}(\widehat\mu)
\approx
\sqrt{\frac{\gamma_0\tau_f}{N}}
=\sqrt{\frac{\gamma_0}{N_{\rm eff,f}}}.
$$

### ESS 依赖 estimand

同一链对 mean、tail probability、quantile、rare event 有不同 autocorrelation/ESS。不能只报告一个 parameter mean ESS 就宣称所有 posterior functional 精确。

## 十三、MCMC ESS 与权重 ESS 不同

MCMC ESS：

$$
N/(1+2\sum\rho_k)
$$

来自 temporal autocorrelation。

importance-weight ESS：

$$
1/\sum_s\widetilde w_s^2
$$

来自 weight concentration。

二者都叫 ESS，但定义、目标和失败模式不同；不能互换。

## 十四、Warmup、adaptation 与 burn-in

### Warmup/adaptation

用于：

- 调整 proposal scale；
- 学 covariance/mass matrix；
- HMC step size；
- 从初值走向典型集合。

若 transition kernel 在 sampling 阶段持续任意 adaptation，固定 invariant distribution 理论可能失效。现代自适应 MCMC 需 diminishing adaptation 等条件；实践中常在 warmup 后冻结。

### Burn-in

丢弃前 $B$ 个 draws 可减初值影响，但没有有限 $B$ 能证明剩余 draws 已来自 stationarity。

### 保留 warmup 做 posterior inference？

通常不应。warmup kernel 参数在变化，draws 不来自最终固定 transition。

## 十五、Thinning 通常不是混合修复

每隔 $k$ 步保留一个 draw 会降低保存 draws 的 autocorrelation，但也丢掉信息。若计算成本由 transition 主导，通常保留全部 post-warmup draws 并用 ESS/MCSE 处理相关性更有效。

thinning 可能合理：

- storage/IO 是主要限制；
- downstream 处理每个 draw 很昂贵；
- 需近似独立的可视化子样本。

它不能让未跨 mode 的链突然正确。

## 十六、为什么必须多链

单链 trace 看似稳定，可能只是在一个 mode 内稳定。

应从过分散初值运行多条独立 chains：

- 比较 within-chain 与 between-chain variation；
- 发现不同 mode/scale；
- 估计 rank-normalized split-$\widehat R$；
- 估计 bulk/tail ESS；
- 检查不同初值是否到同一典型集合。

多链都从同一点启动会削弱诊断能力。

## 十七、$\widehat R$ 的思想

设 $M$ 条 chains，各 $N$ draws。传统 potential scale reduction 比较：

- within-chain variance $W$；
- between-chain variance $B$；
- pooled overdispersed variance estimate $\widehat V$。

大致：

$$
\widehat R=\sqrt{\widehat V/W}.
$$

若 chains 尚未探索同一 distribution，between variation 大，$\widehat R>1$。

现代推荐：

- split chains：发现单链前后不平稳；
- rank normalization：对 heavy tail 更稳；
- folding：对不同 scale/tail 敏感；
- 报告 rank-normalized split 与 folded split 的最大值。

经验上 $\widehat R<1.01$ 常作必要检查，但不是充分证明。局部 mode 内多链、对所有 chain 同样错误、非 identifiable summary 都可让 $\widehat R$ 误导。

## 十八、Bulk ESS、tail ESS 与 MCSE

- bulk ESS：中心位置/秩分布效率；
- tail ESS：常关注 5%/95% quantiles；
- quantile MCSE：interval endpoints 的数值误差；
- mean MCSE：posterior mean 的 Monte Carlo error。

应把：

$$
\text{posterior SD}
$$

与

$$
\text{MCSE of estimated posterior mean}
$$

分开。前者是模型给定后的 parameter uncertainty，后者是有限 draws 估 posterior summary 的数值误差。

更多数据可缩 posterior；更多 MCMC draws 只缩 MCSE，不缩真实 posterior uncertainty。

## 十九、Trace、rank、autocorrelation 与 pair plots

### Trace plot

检查：

- chains 是否重叠；
- drift/trend；
- sticky regions；
- mode switching；
- warmup 后 variance 是否稳定。

“毛毛虫图”不是数学证明。

### Rank plot

把 pooled draws 排名，查看各 chain 的 rank histogram。若 chains exchangeable，rank 分布应相近；U-shape/倾斜提示 location/scale mismatch。

### Autocorrelation

显示 local dependence，但短 ACF 不保证 global modes 都访问。

### Pair plot

结合 divergences/high energy 标记，定位 funnel、boundary 与 curvature pathology。

## 二十、Hamiltonian Monte Carlo

对 continuous parameter $q$，定义 potential：

$$
U(q)=-\log\widetilde\pi(q).
$$

引入 momentum

$$
p\sim N(0,M),
$$

kinetic energy：

$$
K(p)=\frac12p^\top M^{-1}p.
$$

joint density：

$$
\pi(q,p)\propto e^{-H(q,p)},
\qquad
H=U+K.
$$

Hamilton equations：

$$
\frac{dq}{dt}=M^{-1}p,
\qquad
\frac{dp}{dt}=\nabla_q\log\widetilde\pi(q).
$$

理想 dynamics 保体积、可逆、保 $H$，能沿典型集合远距离移动而不做 random walk。

## 二十一、Leapfrog 与 Metropolis correction

数值积分用 leapfrog：

$$
p_{t+1/2}=p_t-\frac\epsilon2\nabla U(q_t),
$$

$$
q_{t+1}=q_t+\epsilon M^{-1}p_{t+1/2},
$$

$$
p_{t+1}=p_{t+1/2}-\frac\epsilon2\nabla U(q_{t+1}).
$$

离散化不精确保能量，末端用 MH：

$$
\alpha
=\min\{1,\exp[-H(q',p')+H(q,p)]\}.
$$

step size $\epsilon$ 太大导致能量误差与 rejection/divergence；太小增加 gradient evaluations。

## 二十二、NUTS 与 adaptation

轨迹长度太短会 random walk，太长会折返浪费。No-U-Turn Sampler 自适应构建轨迹并在开始回头前停止，同时保持正确的 transition construction。

warmup 常学习：

- step size；
- diagonal/dense mass matrix；
- typical set。

sampling 后应冻结这些 adaptation parameters。

NUTS 不是“不需要诊断的 HMC”，仍需 divergences、max treedepth、energy/BFMI、R-hat、ESS 与 posterior geometry 检查。

## 二十三、Divergence

HMC divergence 表示数值 trajectory 的 Hamiltonian error 过大，常出现在：

- funnel neck；
- extreme curvature；
- boundary；
- weak identifiability；
- heavy-tailed scale；
- centered hierarchy。

divergence 可能导致 posterior 某些区域系统性欠探索和 bias。简单增加 target acceptance/减 step size 有时缓解，但若 geometry 根本病态，应重参数化、加入合理 prior、改变 model。

不能把 divergence draws 直接删除后当问题解决。

## 二十四、Funnel 与 noncentering

hierarchical model：

$$
\theta_j\mid\mu,\tau\sim N(\mu,\tau^2).
$$

centered parameterization 在 $\tau\to0$ 时形成狭窄 funnel：

$$
\theta_j-\mu
$$

必须同时非常小，curvature 跨数量级。

noncentered：

$$
z_j\sim N(0,1),
\qquad
\theta_j=\mu+\tau z_j.
$$

把标准化 latent 与 scale 分开，弱数据 group 常显著改善 geometry。强数据情形 centered 也可能更好；应根据信息结构和 diagnostics 选择。

## 二十五、Multimodality 与 label switching

若 modes 间低-density barrier 很高，chains 可各困在一处：

- $\widehat R$ 对 mode-sensitive quantity 变大；
- 若所有 chains 同 mode 启动，可能看不出；
- local ESS 可高但 global expectation 错。

mixture label switching 中多个 modes 表示同一 unlabeled distribution。逐 component mean 可能无意义；可：

- 报告 permutation-invariant functional；
- impose identified ordering（会改变 parameterization）；
- post-process relabel；
- 使用 tempering/SMC 跨 mode。

## 二十六、Discrete parameters

HMC 需要 continuous differentiable parameter，不能直接更新离散 latent。常用：

- analytically marginalize discrete variables；
- Gibbs/MH 更新离散 blocks；
- particle MCMC；
- reversible-jump 处理维数改变；
- continuous relaxation 只是一种近似，目标可能改变。

把 argmax class 或 hard token 当可微参数交给 HMC 不合法。

## 二十七、Constraints 与 Jacobian

sampler 常在 unconstrained $u\in\mathbb R^d$ 运行，通过 transform

$$
\theta=T(u)
$$

映射到 positive/simplex/correlation constraint。unconstrained log density 必须包含

$$
\log|\det J_T(u)|.
$$

漏 Jacobian 会采错 target。posterior summary 应回到 constrained/original coordinates；R-hat/ESS 也要对科学 estimands 检查。

## 二十八、模拟退火不是 stationary posterior sampling

tempered target：

$$
\pi_T(x)\propto\exp[-E(x)/T].
$$

$T$ 小时更集中到低 energy。若随迭代改变 $T_t\downarrow0$，kernel target 也在变，目标是 optimization/global-mode search，而非从固定 $\pi_T$ 产生 stationary draws。

科学空间的 MCMC—模拟退火接口适合解释离散文本搜索，但最终样本若来自退火 schedule，不能当作原 target posterior draws 做普通 uncertainty estimation。

## 二十九、与其他 Monte Carlo 方法比较

| 方法 | draws/weights | 核心条件 | 主要失败 |
|---|---|---|---|
| direct MC | iid target | 能直接采样 | target sampler 不可得 |
| rejection | iid accepted target | global envelope | 高维接受率低 |
| importance sampling | iid proposal + weights | support、有限 weight moments | weight collapse |
| MCMC | correlated chain | invariant + ergodicity + mixing | mode trapping/autocorrelation |
| SMC | weighted particles over targets | path/resampling/mutation | particle degeneracy |
| VI | optimized approximate distribution | expressive family/optimization | approximation bias |

MCMC 的优势是归一化常数抵消、可利用局部结构；代价是相关性、初始化与无法有限时间证明 convergence。

## 三十、Posterior uncertainty 与 Monte Carlo error

假设 posterior mean $\mu=E[\Theta\mid y]$，posterior SD $s_{\rm post}$。

MCMC 给 estimate $\widehat\mu$ 与 MCSE：

$$
\widehat{\rm MCSE}
\approx\frac{s_{\rm post}}{\sqrt{N_{\rm eff}}}.
$$

要报告：

$$
\widehat\mu
\quad
(\text{posterior SD/credible interval})
\quad
[\text{MCSE}].
$$

例：posterior SD 0.5、MCSE 0.01 表示 posterior 本身仍宽 0.5，只是 mean 的数值积分算到约 0.01 精度。两者不可相加或互换。

## 三十一、端到端 MCMC 工作流

### 建模前

1. 定义 estimand 与 joint model；
2. prior predictive；
3. parameterization 与 constraints；
4. simulation recovery/SBC。

### 运行

1. 多条过分散 chains；
2. 足够 warmup；
3. 保存 adaptation/sampler diagnostics；
4. 固定 random seeds 与软件版本；
5. 不用 thinning 掩盖 autocorrelation。

### 诊断

1. rank-normalized split/folded $\widehat R$；
2. bulk/tail ESS；
3. mean/quantile MCSE；
4. trace/rank/ACF/pair plots；
5. divergences、treedepth、energy/BFMI；
6. chains 对初始化与 parameterization 的敏感性。

### 模型检查

1. posterior predictive checks；
2. prior/posterior sensitivity；
3. held-out predictive evaluation；
4. identifiable scientific functional；
5. deployment shift。

## 三十二、常见误区

### 误区 1：接受率高说明链好

可能只是步长极小、chain 几乎不动。

### 误区 2：$\widehat R=1.00$ 证明收敛

它只是不曾检测到所看 marginal 的某类 between/within mismatch。

### 误区 3：烧掉前 50% 就会 stationary

burn-in 比例没有普遍理论；mode trapping 可持续整个 run。

### 误区 4：ESS=1000 表示有 1000 个 iid posterior draws

ESS 是特定 functional 的 asymptotic variance 等效量，不赋予 draws 独立性。

### 误区 5：多跑 iterations 能修所有问题

结构不可辨识、错误 target/Jacobian、divergence 和未连通 proposal 需修 model/algorithm。

### 误区 6：链图看起来像噪声就混合了

局部随机波动可发生在错误 mode。

### 误区 7：MCMC posterior 很精确说明现实预测可靠

MCMC 只解决指定 model 内的积分；不解决 model misspecification 与 OOD。

## 三十三、MCMC 报告模板

1. target density 与 normalization-free form；
2. scientific estimands；
3. sampler/kernel 与版本；
4. constrained transform/Jacobian；
5. chain 数、initialization；
6. warmup、sampling draws、adaptation；
7. step size/mass matrix/proposal scale；
8. acceptance、divergence、treedepth、energy diagnostics；
9. rank/folded split-$\widehat R$；
10. bulk/tail ESS；
11. mean/quantile MCSE；
12. trace/rank/pair plots；
13. reparameterization/sensitivity runs；
14. PPC/SBC；
15. known failures、compute cost 与 reproducibility。

## 三十四、概率卷闭环

本章把前面三类随机误差接起来：

1. **数据抽样误差**：不同 dataset 产生不同 estimator/posterior；
2. **posterior uncertainty**：给定数据和模型，对 parameter/prediction 的条件不确定性；
3. **MCMC error**：有限相关 draws 估 posterior functional 的数值误差。

再外加：

4. model misspecification；
5. approximation/optimization error；
6. deployment distribution shift。

可信 AI 统计报告不能只给其中一个。

## 本章自检

- [ ] 能定义 kernel、invariant、reversible 与 ergodic；
- [ ] 能构造 invariant 但不混合的反例；
- [ ] 能推导 MH acceptance 与 detailed balance；
- [ ] 能解释 Gibbs acceptance-one；
- [ ] 能推导 IACT、ESS 与 MCSE；
- [ ] 能区分 warmup、burn-in、adaptation 与 thinning；
- [ ] 能解释 rank/folded split-R-hat 与 bulk/tail ESS；
- [ ] 能说明 HMC leapfrog、MH correction 与 divergence；
- [ ] 能诊断 funnel、multimodality 与 label switching；
- [ ] 能区分 MCMC ESS 与 importance ESS；
- [ ] 能把 posterior SD 与 MCSE 分开报告。

## 练习与解答

- [[习题 - MCMC 与随机模拟诊断]]
- [[解答 - MCMC 与随机模拟诊断]]

## 参考文献与延伸

- Hastings (1970), “Monte Carlo Sampling Methods Using Markov Chains and Their Applications”；
- Gelman et al., *Bayesian Data Analysis*；
- Vehtari et al. (2021), improved rank-normalized $\widehat R$ and ESS；
- Stan Reference Manual, MCMC Sampling and Posterior Analysis；
- [[S-2021-Su-8084-从MCMC到模拟退火]]。
