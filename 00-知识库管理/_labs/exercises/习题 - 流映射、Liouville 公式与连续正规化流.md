---
type: exercise
status: draft
area: [math/ode, math/dynamical-systems, math/probability, ai/generative-modeling]
topic: "流映射、Liouville 公式与连续正规化流"
difficulty: [A, B, C, D, E]
prerequisites: ["[[流映射、Liouville 公式与连续正规化流]]", "[[随机变量变换与密度换元]]", "[[迹、行列式与体积]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - 流映射、Liouville 与随机迹审计]]"]
solution: "[[解答 - 流映射、Liouville 公式与连续正规化流]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 流映射、Liouville 公式与连续正规化流

> [!abstract] 训练目标
> 从“会背 $d\log p/dt=-\operatorname{tr}J_f$”升级为能逐层证明和审计：知道在哪个定义域上有 flow，何时只有单射/局部逆，能从变分方程推出 Liouville，能把 exact density law、finite solver 与 stochastic trace 三本账分开，并能判断 CNF/FFJORD 的 topology、support、likelihood 与 gradient claim 是否越界。

> [!warning] 作答约定
> 每次写“可逆”必须说明 domain、codomain、时间方向和 exact/numerical 对象；每次写“无偏”必须说明对哪个随机量、条件在哪一层；每次写 density 必须说明相对于哪个基准测度以及变换是否同维。

## A. 定义、条件与对象分层

### DYN-FLOW-A01

建立 flow 术语表，并逐项说明最小条件与不能推出的结论：

1. solution curve $x(t;s,x_s)$；
2. nonautonomous two-parameter flow/process $\phi_{s,t}$；
3. autonomous local flow、semigroup 与 global one-parameter group；
4. common existence domain $D_{s,t}$；
5. injective、local diffeomorphism、diffeomorphism onto image、global diffeomorphism of $\mathbb R^d$；
6. pushforward $(\phi_{s,t})_\#\mu_s$；
7. numerical flow/map $\Psi_h$。

证明 composition law，指出证明中 uniqueness 出现在哪里；再解释 existence、uniqueness、$C^1$ 初值依赖、forward completeness 与 two-sided completeness 分别承担哪一层责任。

### DYN-FLOW-A02

围绕 volume 与 density 区分以下对象：

1. $D_xf$、$D\phi_{s,t}$ 与 $D_\theta x(t)$；
2. determinant、trace、divergence 与 singular values；
3. $d\log p_t(x_t)/dt$ 与 $\partial_t\log p_t(x)$；
4. local volume contraction 与 trajectory stability；
5. density relative to Lebesgue measure 与 singular distribution；
6. finite change-of-variables 与 instantaneous change-of-variables；
7. continuity equation 与 Liouville trajectory formula。

最后给出一个 divergence 为零但状态持续变化的例子，以及一个 divergence 为负但某方向会暂时拉伸的例子。

### DYN-FLOW-A03

为一个 FFJORD/CNF 实现写一张最小 solver card，至少包含：

1. state、time interval、base law、context 与 target data preprocessing；
2. vector field regularity/architecture 与是否 augmentation；
3. exact/structured/Hutchinson divergence；
4. probe distribution、probe count、reuse/resampling policy；
5. forward/backward solver、step/tolerance/precision；
6. sampling、likelihood 与 training 三种 task；
7. NFE、VJP/JVP、rejection、wall time 与 memory；
8. state、log-density、trace Monte Carlo 与 round-trip error；
9. continuous/discrete/checkpoint gradient object；
10. support/topology 与 global-existence claim。

解释为什么只写“dopri5, rtol=$10^{-5}$, NFE=80”不足以复现实验。

## B. 精确流、Jacobian 与密度手算

### DYN-FLOW-B01

考虑一维非自治 affine ODE

$$
\dot x=-2x+e^t,
\qquad x(s)=x_s.
$$

1. 求 $\phi_{s,t}(x_s)$；
2. 证明 composition law；
3. 求 $J_{s,t}=\partial\phi_{s,t}/\partial x_s$；
4. 用 Liouville 公式独立验证 determinant；
5. 若 $X_s\sim\mathcal N(m_s,\sigma_s^2)$，求 $X_t$ 的均值与方差；
6. 分别用 Gaussian density 与 change of variables 验证 log-density correction；
7. 若只知道 $X_t=x_t$，写出反向恢复 $x_s$ 的公式；
8. 该 flow 是否为 $\mathbb R\to\mathbb R$ 的 global diffeomorphism？说明时间条件。

### DYN-FLOW-B02

考虑

$$
\dot x=-x^3,
\qquad x(0)=x_0.
$$

1. 推导 $\phi_t(x_0)$；
2. 求其像集；
3. 求 $J_t(x_0)$ 并证明为正；
4. 沿轨迹积分 divergence，验证 Liouville；
5. 若 $X_0\sim\mathcal N(0,1)$，写出 $x=\phi_t(x_0)$ 处的 $\log p_t(x)$；
6. 将 $x_0$ 表示成 $x$，写出仅用 $x,t$ 的 density 公式及其支持集；
7. 研究 $x$ 接近支持集边界时 $p_t(x)$ 的行为；
8. 解释该例怎样同时推翻“$J>0$ 自动给 onto $\mathbb R$”与“Gaussian base 经光滑单射后仍必有全空间支持”两种说法。

### DYN-FLOW-B03

令

$$
A=\begin{bmatrix}-1&8\\0&-2\end{bmatrix},
\qquad \dot x=Ax.
$$

1. 计算 $e^{tA}$；
2. 求 trace、determinant 与 Liouville 体积因子；
3. 求单位正方形四个顶点在 $t=1/2$ 时的像；
4. 用二维叉积/行列式计算像平行四边形面积；
5. 对初始向量 $v=(0,1)^T$，计算 $\|e^{tA}v\|_2$，判断是否存在暂时大于1的时刻；
6. 这是否与所有 eigenvalues 实部为负矛盾？
7. 若 $X_0\sim\mathcal N(0,I)$，写出 $X_t$ 的 covariance 和 log-determinant correction；
8. 解释为何 $\operatorname{tr}A=-3$ 不足以重建 covariance shape。

## C. 定理推导与反例

### DYN-FLOW-C01

设 $f(t,x)$ 对 $x$ 为 $C^1$，且在所讨论 tube 上 IVP 唯一并共同存在。完整证明：

1. $J_{s,t}=D_{x_s}\phi_{s,t}$ 满足变分方程；
2. Jacobian composition law；
3. Jacobi determinant formula 如何应用于 $J_{s,t}$；
4. $d\log\det J_{s,t}/dt=\operatorname{tr}D_xf$；
5. $\det J_{s,t}>0$；
6. local inverse theorem 的结论；
7. 为什么上述证明仍不自动给 $\phi_{s,t}(\mathbb R^d)=\mathbb R^d$；
8. 在 density 换元额外条件下推出 instantaneous log-density equation。

要求每一步标注使用的是 chain rule、uniqueness、Jacobi formula、trace cyclicity、inverse function theorem 还是 change of variables。

### DYN-FLOW-C02

令 $A\in\mathbb R^{d\times d}$，$S=(A+A^T)/2$。

1. 证明 $\varepsilon^TA\varepsilon=\varepsilon^TS\varepsilon$；
2. 对满足 $\mathbb E\varepsilon\varepsilon^T=I$ 的 probe 证明无偏性；
3. 对独立 Rademacher probe 推导

   $$
   \operatorname{Var}(\varepsilon^TA\varepsilon)
   =4\sum_{i<j}S_{ij}^2;
   $$

4. 对 standard Gaussian probe 推导 $2\|S\|_F^2$；
5. 证明 $m$ 个独立 probe 平均的方差除以 $m$；
6. 给出 Rademacher 方差为零但 Gaussian 方差非零的矩阵；
7. 给出单 probe 绝对误差很大但估计仍无偏的矩阵；
8. 说明“unbiased trace”不能无条件升级为“unbiased trained likelihood”。

### DYN-FLOW-C03

设 $f:\mathbb R^d\to\mathbb R^d$ 全局 $L$-Lipschitz，Euler residual map 为

$$
\Psi_h(x)=x+hf(x).
$$

1. 证明 $hL<1$ 时

   $$
   \|\Psi_h(x)-\Psi_h(y)\|\ge(1-hL)\|x-y\|;
   $$

2. 推出单射；
3. 用 Banach fixed point 证明对每个 $z$ 方程 $\Psi_h(x)=z$ 有唯一解；
4. 推出 inverse 的 Lipschitz 上界；
5. 说明这是一条充分条件而非必要条件；
6. 对 $f(x)=-x^3$ 找出 Euler map 的临界点与折叠区；
7. 比较 exact flow 的 derivative 与 Euler derivative；
8. 解释 solver refinement 怎样把 discrete map 拉回 exact-flow regime，却不意味着任意有限 $h$ 都继承拓扑性质。

## D. 数值实现、实验与程序语义

### DYN-FLOW-D01

为 $x'=-x^3$ 设计 state–log-density 增广积分实验：

$$
\dot x=-x^3,
\qquad
\dot\ell=3x^2.
$$

1. 给出 $x(t)$ 与 $\ell(t)$ 的解析解；
2. 从 standard normal base 写出 $\ell(0)$；
3. 用 RK4 在 $t\in[0,1]$ 上计算，步数取 $N=10,20,40,80,160$；
4. 同时记录 endpoint state 与 log-density error；
5. 估计 observed order；
6. 检查 $\ell(t)-\ell(0)=-\log J_t$；
7. 解释为什么只验证 state order 不足以验证 CNF likelihood；
8. 给出 floating-point floor、stiffness 与过紧 tolerance 时的预期现象。

### DYN-FLOW-D02

设 CNF 用 Rademacher Hutchinson estimator。比较三种 probe policy：

1. 每条 trajectory 整次 solve 固定一个 probe；
2. 每个 accepted step 重采样；
3. 每次 RHS evaluation，包括 rejected trial，都重采样。

对每种 policy 回答：solver conditional on randomness 看见的是不是固定的平滑 ODE；step rejection 是否可重复；classical local error estimator 在测什么；forward/backward 是否可能复用随机对象；最终 log-density 的随机性来自哪里。设计一个小维 exact-trace reference protocol，至少含 dimension、matrix/vector field、seed、probe sweep、solver refinement 与 confidence interval。

### DYN-FLOW-D03

你收到以下实验表：

| model | NFE | probes | NLL | round-trip | wall time |
|---|---:|---:|---:|---:|---:|
| A | 60 | 1 | 1.02 | $10^{-2}$ | 1.0 |
| B | 100 | exact | 1.00 | $10^{-7}$ | 3.5 |
| C | 45 | 4 | 0.99 | $10^{-3}$ | 2.1 |

但没有 error bars、tolerance、architecture、preprocessing 或同一 checkpoint 信息。

1. 列出至少十二个不能由表格直接推出的结论；
2. 设计 equal-error 与 equal-budget 两套比较；
3. 说明 NFE 怎样转换为真正的 RHS/VJP 成本；
4. 给出 likelihood evaluation 的 probe uncertainty 报告方式；
5. 区分 round-trip error、state endpoint error 与 NLL error；
6. 指出若系统 stiff，还要增加哪些统计；
7. 说明如何检查 gradient objective；
8. 写出一段不越界的结论。

## E. AI 迁移、研究设计与综合审计

### DYN-FLOW-E01

审计下述论文式表述：

> “Our neural ODE is exactly invertible, computes exact likelihoods with an unbiased trace estimator, and can represent arbitrary continuous transformations. It uses constant memory and is more efficient because NFE is lower.”

逐句拆成 claim，分别判断需要哪些条件/实验：

1. exact mathematical invertibility；
2. numerical round-trip；
3. exact likelihood；
4. unbiased trace 与 likelihood 的关系；
5. arbitrary transformation 与 topology；
6. constant memory 的 adjoint/solver 含义；
7. lower NFE 与 total efficiency；
8. 若使用 ReLU、clipping、event 或 finite precision，定理需要怎样改写。

最后将原表述重写成一段可检验、量词完整的摘要。

### DYN-FLOW-E02

设计一个从二维 standard Gaussian 学习“近似两条细圆环”的生成模型。比较：

1. 同维 CNF；
2. augmented Neural ODE 后 projection；
3. 给数据加 observation noise 的 density model；
4. 直接建低维 latent + observation model。

对每个方案回答：目标 law 是否对二维 Lebesgue measure 有 density；support/topology 障碍是什么；能否 exact likelihood；需要积分/边缘化什么；sample quality 与 density quality 怎样分别评价。解释有限样本看见两条分离圆环为什么不足以证明真实 density support 不连通。

### DYN-FLOW-E03

为一篇声称“新 divergence estimator 显著改进高维 CNF”的论文设计复核方案。至少包含：

1. theorem target 与无偏/偏差/方差量词；
2. synthetic matrices 的 diagonal、dense symmetric、skew、low-rank 与 nonnormal 族；
3. exact-trace small/medium benchmark；
4. dimension、probe、seed、precision 与 VJP budget sweep；
5. 与 Hutchinson/Rademacher、Gaussian 和 exact structured trace 的基线；
6. 固定 trajectory 与 coupled trajectory 两层实验；
7. solver adaptivity、probe reuse 与 stochastic gradient protocol；
8. likelihood、sample、wall-time、memory 与 energy 指标；
9. failure cases 与 negative results；
10. 从 L0 公式到 L6 general claim 的证据升级路径。

要求最终产出一张 claim–evidence matrix，而不是只列 benchmark 名称。

## 提交与评分建议

- A 组：术语与条件，每题 10 分；缺 domain/time/object 任一项不得满分。
- B 组：精确计算，每题 12 分；只有最终答案、没有换元/支持集说明最多 60%。
- C 组：证明，每题 16 分；定理名与使用条件必须对应。
- D 组：程序审计，每题 14 分；必须报告可复现参数和误差分账。
- E 组：研究迁移，每题 18 分；不允许把 finite benchmark 提升为一般定理。

建议先闭卷完成 A、B、C，再运行实验；最后对照[[解答 - 流映射、Liouville 公式与连续正规化流]]评分。题卷状态为 `not-attempted`，文档存在不代表学习者已经掌握。
