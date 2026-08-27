---
type: exercise
status: draft
area: [math/probability, math/stochastic-processes, math/sde, ai/generative-modeling]
topic: "随机过程、Brownian 运动与二次变差"
difficulty: [A, B, C, D, E]
prerequisites: ["[[随机过程、Brownian 运动与二次变差]]", "[[联合分布、边缘分布与独立性]]", "[[协方差、相关性与条件期望]]", "[[多元高斯分布]]", "[[中心极限定理与 Delta 方法]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]"]
solution: "[[解答 - 随机过程、Brownian 运动与二次变差]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 随机过程、Brownian 运动与二次变差

> [!abstract] 训练目标
> 从“知道 $W_t\sim\mathcal N(0,t)$”升级为能够区分 marginal、transition、FDD 与 path law；能够从独立 Gaussian increments 推导 covariance、martingale、Brownian bridge 和 quadratic variation；能够审计扩散模型的时间耦合、$\sqrt{\Delta t}$ 缩放与随机流复用。

> [!warning] 作答约定
> 每次写极限必须注明 convergence mode；每次写 quadratic variation 必须说明 partition sequence；每次声称 Brownian 必须检查 joint-time law 而非只看 marginals；每次做跨步长实验必须说明是否使用同一 underlying Brownian path。

## A. 定义、对象与合同

### DYN-BM-A01

建立随机过程对象表，逐一说明：

1. probability space、time index 与 state space；
2. random variable $X_t$、sample path $t\mapsto X_t(\omega)$；
3. marginal、FDD、transition kernel 与 path law；
4. modification 与 indistinguishability；
5. filtration、natural filtration、adaptedness；
6. stopping time 与 martingale；
7. continuous、càdlàg、Hölder、finite variation。

构造两个过程，使每个固定时刻 marginal 完全相同，但两时刻 joint law 不同。解释为什么逐时 histogram 无法区分它们。

### DYN-BM-A02

写出 standard Brownian motion 的完整定义，并制作 claim ladder：

1. $W_t\sim\mathcal N(0,t)$；
2. stationary Gaussian increments；
3. independent increments；
4. Gaussian process covariance kernel $\min(s,t)$；
5. continuous modification；
6. almost-sure path theorem；
7. martingale/Markov/strong Markov。

说明哪些结论可由哪些条件推出，哪些不能反推。特别解释“levels 相关但 increments 独立”以及 usual augmentation 为什么属于 filtration contract。

### DYN-BM-A03

为一个 continuous-time diffusion model 写 process/noise card，至少包含：

1. fixed-time noising marginal；
2. multi-time joint law 或 transition kernel；
3. forward filtration 与 adaptedness；
4. drift/diffusion coefficient的单位；
5. $\sqrt{\Delta t}$ noise scaling；
6. component covariance 与 cross variation；
7. PRNG/key/device stream policy；
8. Brownian tree 或 nested refinement policy；
9. training marginal sampling 与 reverse path dynamics 的区别；
10. pathwise/weak/final-distribution验收指标。

解释为什么“每个噪声水平的样本都像正确 Gaussian”不能证明 forward process 或 reverse sampler 正确。

## B. 联合 Gaussian、条件分布与随机游走

### DYN-BM-B01

设 $W$ 为标准 Brownian motion，取

$$
0<s<t<u.
$$

1. 写出 $(W_s,W_t,W_u)$ 的 covariance matrix；
2. 求 $\operatorname{Cov}(W_t-W_s,W_u-W_t)$；
3. 求 $W_t\mid W_u=b$ 的分布；
4. 求 $W_t-W_s\mid W_u=b$ 的均值与方差；
5. 验证 $\mathbb E[W_u\mid\mathcal F_t]=W_t$；
6. 验证 $W_t^2-t$ 是 martingale；
7. 解释 Brownian bridge 的条件均值是直线却仍有随机波动；
8. 取 $s=1/4,t=1/2,u=1,b=2$ 数值化全部结果。

### DYN-BM-B02

对标准 Brownian motion 研究以下过程：

$$
X_t=aW_{bt},
\qquad
Y_t=W_{t+c}-W_c,
\qquad
R_t=W_T-W_{T-t}.
$$

1. $a,b$ 满足什么关系时 $X$ 是标准 Brownian？
2. $Y$ 是否为 Brownian？它与 $\mathcal F_c$ 什么关系？
3. $R$ 在 $[0,T]$ 上是否有 Brownian law？
4. $R$ 相对于原 forward filtration 是否 adapted？
5. 若 $Z_t=LW_t+\mu t$，求 increment mean/covariance；
6. $L$ 与 $LQ$（$Q$ 正交）是否给同一 law？
7. 为什么 same law 不代表与其他随机变量的 coupling 相同？
8. 进行单位检查：$a,b,L,\mu$ 的量纲是什么？

### DYN-BM-B03

令 $\xi_k$ 为 i.i.d. Rademacher variables，$S_n=\sum_{k=1}^n\xi_k$，定义

$$
X_t^{(n)}
=n^{-\gamma}S_{\lfloor nt\rfloor}.
$$

1. 计算固定 $t$ 的均值与方差；
2. 只有哪个 $\gamma$ 给非退化方差极限？
3. 对该 $\gamma$ 用 CLT 求固定 $t$ 的极限；
4. 求两个时刻 $s<t$ 的 covariance 极限；
5. 说明得到 FDD convergence 还缺哪些步骤；
6. 比较阶梯插值与线性插值所在的 path space；
7. 陈述 Donsker theorem 的对象、拓扑与 convergence mode；
8. 解释“随机游走等价于 Brownian motion”怎样说才不越界。

## C. 二次变差、有限变差与信息流推导

### DYN-BM-C01

固定 $T$ 与 deterministic partition $\Pi$，令

$$
Q_\Pi=\sum_i(\Delta_iW)^2.
$$

1. 推导 $\mathbb E[Q_\Pi]=T$；
2. 推导 $\operatorname{Var}(Q_\Pi)=2\sum_i(\Delta_it)^2$；
3. 证明 mesh $\to0$ 时 $Q_\Pi\to T$ in $L^2$；
4. 对 uniform $n$-partition 求 exact RMSE；
5. 对 dyadic partitions 用 Chebyshev 与 Borel–Cantelli 推出 almost-sure convergence；
6. 若 partition 随路径自适应，上述证明哪一步不能直接照搬？
7. 解释单步 $(\Delta W)^2\ne\Delta t$ 与极限 $[W]_T=T$ 不矛盾；
8. 推导 $\sum_i|\Delta_iW|$ 的期望并给出 $\sqrt n$ 增长率。

### DYN-BM-C02

1. 证明连续有限 total variation 路径沿任意 mesh $\to0$ partitions 的平方增量和趋于0；
2. 由 Brownian quadratic variation 推出其 total variation almost surely 无限；
3. 说明这一步为何还不等于完整证明 nowhere differentiable；
4. 对两个独立 Brownian motions 推导 cross-variation 的 $L^2$ 极限为0；
5. 对相关系数 $\rho$ 的二维 Brownian 推导 cross variation；
6. 若 $X_t=LW_t$，求 matrix quadratic covariation；
7. 区分 quadratic variation 与 $2$-variation supremum；
8. 说明误复用随机流会怎样出现在 realized cross variation 中。

### DYN-BM-C03

设 $\mathcal F_t^W$ 为 Brownian natural filtration。

1. 证明 $W_t$ adapted；
2. 证明 $W_t$ 是 martingale；
3. 证明 $W_t^2-t$ 是 martingale；
4. 判断 $\tau_a=\inf\{t:W_t=a\}$ 是否为 stopping time；
5. 判断“$T$ 前最后一次过0”是否显然为 stopping time；
6. 给出一个均值恒定但不是 martingale 的过程；
7. 解释 independent increments、Markov 与 martingale 三个性质的逻辑差异；
8. 若扩散网络在时刻 $t$ 使用未来噪声 key，哪个合同被破坏？

## D. 复现、失败注入与数值判断

### DYN-BM-D01

复现[[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]，并完成：

1. 检查 $\operatorname{Var}(W_t)\approx t$；
2. 检查 covariance kernel $\min(s,t)$；
3. 检查不重叠 increments covariance；
4. 扫描 dyadic $n$ 的 mean/RMSE quadratic variation；
5. 拟合 total variation 关于 $n$ 的 log-log slope；
6. 与 $T\sqrt{2/n}$ 和 $\sqrt{2nT/\pi}$ 理论式比较；
7. 换 seed、path count 与非均匀 partition；
8. 解释哪些误差是 Monte Carlo，哪些是 partition approximation。

### DYN-BM-D02

固定 $t_0>0$，比较

$$
B_t=W_t,\qquad
S_t=\sqrt tZ,\qquad
I_t=\sqrt tZ_t.
$$

1. 验证三者 fixed-time marginal 相同；
2. 推导三者 $t_0$ 到 $t_0+h$ 的 increment MSE；
3. 求 $h\downarrow0$ 的阶；
4. 判断各自是否 mean-square continuous；
5. 哪个具有 Brownian independent increments？
6. $S_t$ 在 $t_0>0$ 附近的 quadratic variation是什么？
7. 为什么 $I_t$ 没有连续 modification？
8. 把结论迁移到 diffusion model 中“每个时间重采 $\varepsilon$”与“所有时间共用 $\varepsilon$”的两种错误。

### DYN-BM-D03

设计 Brownian simulation/refinement protocol：

1. arbitrary nonuniform grid 的 exact increment sampler；
2. fine-to-coarse nested increments；
3. 端点间 Brownian bridge refinement；
4. multi-device independent stream；
5. paired common-random-number comparison；
6. barrier crossing correction；
7. fp32/fp64 和 very small $\Delta t$；
8. pathwise、weak 与 endpoint-distribution三类指标。

给出一个会让 coarse/fine error 被独立路径噪声淹没的错误实现，并给出修复。

## E. 研究迁移与声明审计

### DYN-BM-E01

审计以下“证明”：

> 对每个固定 $t$，Brownian path 在 $t$ 可微的概率为0；把所有 $t\in[0,T]$ 做并集，所以路径 almost surely nowhere differentiable。

1. 找出量词/测度错误；
2. 固定时刻差商为什么不可能收敛到有限导数？
3. 为什么有理时刻不可微仍不足以推出处处不可微？
4. 给出 nowhere-differentiability 正式证明需要的可数化思路；
5. 非零 quadratic variation 能严格推出什么？
6. Kolmogorov continuity/Hölder theorem 能严格推出什么？
7. 说明“连续但粗糙”的不同定理不能互相代替；
8. 为论文写一条不过界的 path-regularity claim。

### DYN-BM-E02

设 $X$ 是 centered Gaussian process，covariance kernel 为 $K(s,t)$。

1. 说明为什么 $K$ 决定全部 FDD；
2. $K(s,t)=\min(s,t)$ 为什么给 Brownian FDD？
3. $K(s,t)=st$ 对应什么显式 process？
4. 比较两者 marginals 与 increments；
5. $K(s,t)=e^{-|t-s|}$ 的过程为何不是从0开始的 Brownian？
6. 写出 kernel 必须满足的 positive-semidefinite 条件；
7. 只拟合 diagonal $K(t,t)$ 会遗漏什么？
8. 设计一个用 empirical covariance matrix 区分三类过程的测试。

### DYN-BM-E03

某论文声称：

> 我们在每个 noise level 都匹配了正确 Gaussian corruption，并使用高精度 ODE/SDE solver，因此模型学到了正确连续扩散过程。

建立 claim–evidence matrix，至少审计：

1. fixed-time marginal 与 multi-time transition；
2. score approximation 与 true score；
3. forward SDE 与 reverse-time equation；
4. Brownian coupling 与 PRNG stream；
5. $\sqrt{\Delta t}$ scaling；
6. solver discretization 与 field/model error；
7. endpoint sample metric 与 path functional；
8. probability-flow ODE 与 reverse SDE 的对象差异；
9. finite-NFE、precision 与 seed uncertainty；
10. 哪些结论必须留给 DYN-10—12。

最后把原声明改写成一条当前证据真正支持的、可证伪的结论。

## 作答后的状态规则

- 首次作答前不打开[[解答 - 随机过程、Brownian 运动与二次变差]]；
- A—C 要求闭卷重建定义与推导，D 要求独立运行和至少一次失败注入，E 要求形成书面 claim audit；
- 题卷存在只表示 composed / not-attempted，不升级正文状态；
- 首次通过后仍需48小时重做 C01/C02、14天迁移 E03，才讨论 verified。
