---
type: exercise
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/pde, ai/generative-modeling]
topic: "Fokker-Planck 方程与概率流 ODE"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Fokker-Planck 方程与概率流 ODE]]", "[[Itô 引理与随机微分方程]]", "[[连续性方程与守恒律]]", "[[流映射、Liouville 公式与连续正规化流]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - Fokker-Planck、概率流与score误差审计]]"]
solution: "[[解答 - Fokker-Planck 方程与概率流 ODE]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Fokker-Planck 方程与概率流 ODE

> [!abstract] 训练目标
> 从“会写 Fokker–Planck 公式”升级为能沿 transition—generator—adjoint—current—continuity 的完整链推导；能处理 state-dependent diffusion、boundary 与 stationary current；能证明 probability-flow ODE 只共享 marginals，并把 score/model/solver error 分账。

> [!warning] 作答约定
> 每道 PDE 题必须写 weak/classical 层级与 boundary term；每道 probability-flow 题必须写 $D=BB^\top$ 的形状及 density positivity；每次声称“等价”必须说明是 marginal、transition 还是 path law；每道数值题必须分别检查 mass、positivity 与 convergence。

## A. 对象、generator 与 Kolmogorov 方程

### DYN-FP-A01

对 time-inhomogeneous Markov diffusion

$$
dX_t=a(t,X_t)dt+B(t,X_t)dW_t
$$

建立对象表，逐一说明：

1. transition kernel $P_{s,t}(x,dy)$；
2. transition density $p(s,x;t,y)$；
3. Markov evolution operator；
4. generator $\mathcal L_t$ 与 domain；
5. formal adjoint $\mathcal L_t^\ast$；
6. marginal law $\mu_t$ 与 density $p_t$；
7. probability current $J_t$；
8. score $s_t$；
9. canonical probability-flow velocity $v_t$；
10. SDE path law 与 ODE path law。

为每两个相邻对象写出连接公式，并指出哪些对象不存在时仍可保留 weak formulation。

### DYN-FP-A02

设 scalar Itô diffusion

$$
dX_t=(\alpha+\beta X_t)dt+(\gamma+\delta X_t)dW_t.
$$

1. 写 generator；
2. 对 $\varphi(x)=1,x,x^2,x^3$ 计算 $\mathcal L\varphi$；
3. 用 Dynkin formula 推导前三阶 moment equations；
4. 判断 moment hierarchy 在哪些参数下闭合；
5. 写出对应 Fokker–Planck differential expression；
6. 说明 generator domain 与 boundary conditions 为什么不能从 differential expression 自动恢复；
7. 对 $\delta=0$ 解 mean/variance ODE。

### DYN-FP-A03

固定 terminal time $T$，定义

$$
u(t,x)=\mathbb E[\psi(X_T)\mid X_t=x].
$$

1. 从 Markov property 证明 $u(t,X_t)$ 是 martingale；
2. 用 Itô formula 推导 backward Kolmogorov equation；
3. 写 terminal condition；
4. 对 transition density 标出 backward equation 作用的变量；
5. 写 forward equation 及其作用变量；
6. 比较 backward PDE、Fokker–Planck 与 reverse-time SDE；
7. 对 arithmetic Brownian motion 和 $\psi(x)=x^2$ 解出 $u$ 并验证 PDE。

## B. Adjoint、弱形式与 boundary

### DYN-FP-B01

令 $X_t\in\mathbb R^d$ 满足

$$
dX_t=a(t,X_t)dt+B(t,X_t)dW_t,
\qquad
D=BB^\top.
$$

1. 从 Dynkin identity 写出 test-function weak form；
2. drift 项做一次分部积分；
3. diffusion 项做两次分部积分；
4. 推导完整多维 Fokker–Planck；
5. 写成 current form；
6. 展开 state-dependent $D$ 的 product terms；
7. 构造一个反例说明 $D_{ij}\partial_{ij}p$ 不能替代 $\partial_{ij}(D_{ij}p)$；
8. 说明 compact support、whole-space decay 与 bounded-domain boundary 的不同责任。

### DYN-FP-B02

在 bounded smooth domain $\Omega$ 上设

$$
\partial_tp+\nabla\cdot J=0.
$$

分别研究：

1. reflecting/no-flux；
2. periodic；
3. absorbing/killed；
4. prescribed inflow/outflow。

对每种情形推导总质量 balance。解释 absorbing density 的积分为何是 survival probability，并给出加入 cemetery state 后的总概率。再设计一个 finite-volume boundary flux audit，能发现把 reflecting boundary 误写成 $p=0$ 的实现错误。

### DYN-FP-B03

对一维 SDE

$$
dX_t=a(X_t)dt+b(X_t)dW_t
$$

1. 写 Fokker–Planck 与 current；
2. 证明 stationary 只推出 current 为常数；
3. 在 zero-current 条件下推导
   $$
   p_\infty(x)\propto b(x)^{-2}
   \exp\left(\int^x2a/b^2\right);
   $$
4. 列出归一化、boundary 与 $b=0$ 的条件；
5. 取 $a(x)=-\kappa x,b(x)=\sigma(1+x^2)^{1/2}$ 求形式 stationary density；
6. 判断其 tail 何时可积；
7. 解释 periodic domain 上 nonzero stationary current 的可能性。

## C. 可解模型与 equilibrium

### DYN-FP-C01

对

$$
dX_t=\mu dt+\sigma dW_t,
\qquad X_0=x_0,
$$

1. 写 transition Gaussian density；
2. 直接微分验证 forward PDE；
3. 验证 weak initial condition 为 Dirac；
4. 写 probability current；
5. 对 $\varphi(x)=x,x^2,e^{i\xi x}$ 验证 Dynkin/characteristic-function演化；
6. 写 backward equation；
7. 解释 $\sigma\to0$ 如何退化为 continuity equation；
8. 说明 pointwise $t\downarrow0$ 为什么不能表示完整 initial convergence。

### DYN-FP-C02

对 OU：

$$
dX_t=\kappa(m-X_t)dt+\sigma dW_t.
$$

1. 写 Fokker–Planck；
2. 从 exact transition law 验证 mean/variance evolution；
3. 把 Gaussian ansatz 代入 PDE；
4. 用 zero current 求 stationary density；
5. 证明 stationary covariance kernel；
6. 写 backward generator；
7. 推导 stationary probability-flow velocity；
8. 解释 stationary density 下 canonical velocity为何为0，但 SDE path 仍有非零 QV。

### DYN-FP-C03

对 overdamped Langevin

$$
dX_t=-M\nabla U(X_t)dt+\sqrt{2\beta^{-1}M}\,dW_t,
$$

其中 $M$ 为常数 SPD。

1. 写 $D$ 与 Fokker–Planck；
2. 写 current；
3. 证明 $\pi\propto e^{-\beta U}$ 给 zero current；
4. 区分 invariance、reversibility、ergodicity 与 convergence rate；
5. 若 $M=M(x)$，指出 Itô drift 需要怎样的 correction 才能保持目标 law；
6. 解释 preconditioned Langevin 与 natural-gradient intuition 的边界；
7. 设计一个只验证 histogram 仍不足的 equilibrium audit。

## D. Probability flow 与数值

### DYN-FP-D01

对一般 $D(t,x)=B B^\top$：

1. 从 current 推导
   $$
   v=a-\frac1{2p}\nabla\cdot(Dp);
   $$
2. 展开为 $a-\frac12\nabla\cdot D-\frac12D\nabla\log p$；
3. 检查所有向量/矩阵形状；
4. 把 $\partial_tp=\mathcal L^\ast p$ 改写成 continuity equation；
5. 写出 SDE/PF ODE 同 marginal 的四步证明责任；
6. 说明 density 为0时的困难；
7. 构造 $u$ 满足 $\nabla\cdot(up)=0$，展示同 density velocity 的非唯一性；
8. 对 scalar $b(x)$ 写出不能遗漏的 $-\frac12(b^2)'$。

### DYN-FP-D02

设

$$
X_0\sim\mathcal N(0,v_0),
\qquad
dX_t=\sigma dW_t.
$$

1. 求 $p_t$ 与 score；
2. 推导 probability-flow ODE；
3. 求 ODE exact solution；
4. 证明 SDE 与 ODE 的 fixed-time marginals相同；
5. 分别求两者 $\operatorname{Cov}(X_s,X_t)$；
6. 比较 quadratic variation；
7. 比较 conditional transition law；
8. 比较 hitting probability；
9. 说明哪些训练/evaluation指标无法区分二者；
10. 设计最小 path-law audit。

### DYN-FP-D03

对一维 current

$$
J=ap-D\partial_xp,
\qquad D>0,
$$

建立 finite-volume scheme：

1. 用 upwind drift 与 centered diffusion 写 face flux；
2. 证明 interior flux telescope；
3. 写 no-flux boundary；
4. 推导 positivity 的充分 CFL 型条件；
5. 区分 advection 与 diffusion step restriction；
6. 定义 $L^1$ density error、mass drift、negative mass 与 moment error；
7. 对 OU exact Gaussian 设计 refinement study；
8. 比较 PDE grid error、particle Monte Carlo error 与 PF ODE step error；
9. 说明高维 curse 与 particle alternative。

## E. AI、likelihood 与研究审计

### DYN-FP-E01

对 isotropic diffusion probability flow

$$
\dot Z=f(t,Z)-\frac12g(t)^2s_t(Z),
$$

实际用 $\widehat s=s+e$。

1. 推导 velocity error；
2. 推导把 true $p$ 代入 learned continuity equation 的 residual；
3. 解释 small score MSE 为何不自动给 small density error；
4. 把 error 分成 score/model、continuous-flow 与 finite-step solver；
5. 设计 exact-score/step-sweep；
6. 设计 perturbed-score/accurate-solver sweep；
7. 对 Gaussian noising 的 multiplicative score error求最终 variance；
8. 写出可证伪的 acceptance thresholds。

### DYN-FP-E02

沿 learned probability-flow ODE：

$$
\dot Z_t=v_\theta(t,Z_t).
$$

1. 推导 instantaneous change-of-variables；
2. 写 terminal/base likelihood relation；
3. 展开 $\nabla\cdot v_\theta$ 对 score Jacobian 的需求；
4. 说明 Hutchinson trace estimator估计什么；
5. 区分 probe Monte Carlo error、state solver error、log-density quadrature error与score error；
6. 解释 adaptive rejection 下 probe reuse/resampling 的程序语义；
7. 设计 exact linear-Gaussian likelihood baseline；
8. 说明 finite-tolerance likelihood为何不能无条件称 exact。

### DYN-FP-E03

设计一个 score-based continuous-time generative model 的 DYN-11 级研究方案。要求：

1. 明确 forward SDE、$D$、marginal density/score对象；
2. 推导 Fokker–Planck current；
3. 推导 probability-flow velocity；
4. 处理 $t=0$ singular/noise floor；
5. 给出 FPE/PF 的 analytical toy baseline；
6. 分别验收 marginal、transition 与 path metrics；
7. 分离 score、ODE solver、divergence estimator 与 MC error；
8. 报告 mass/normalization 与 likelihood ledger；
9. 做 score perturbation 和 step/tolerance ablation；
10. 写明哪些主张必须留到 reverse-time DYN-12；
11. 给出失败停止条件；
12. 形成一页 research acceptance checklist。
