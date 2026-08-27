---
type: assessment-solution
status: draft
area: [math/foundations, ai/theory, curriculum/capstone]
assessment_id: MATH-FND-CAP-01-SOL
solves: "[[数学基础十卷总验收 - 跨卷理论与 AI 迁移]]"
related: ["[[数学基础完整课程地图与掌握标准]]", "[[数学基础十卷完备性审计与学习状态总表]]", "[[实验 - 数学基础十卷跨章累计复现门]]", "[[练习与测验 MOC]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 数学基础十卷总验收解答 - 跨卷理论与 AI 迁移

> [!warning] 使用顺序
> 先冻结[[数学基础十卷总验收 - 跨卷理论与 AI 迁移|两场原卷]]、随机实验轨和事前预测。能读懂这份解答，只说明答案可读；只有在陌生对象上独立重建对象合同、证明与证据边界，才接近课程出口能力。

## 0. 评分总则

- 一条答案若跨越四层证据，按它**最早发生的越界**扣分，而不只看最终公式；
- 正确公式套在错误对象上不得主要步骤分，例如把 marginal-law 等价写成 pathwise 等价；
- 忘记条件数、谱隙、正则性、步长域或 topology 时，相关“稳定/收敛”结论不得满分；
- 算术误差只扣第一次；其后若对象、方向和推理一致可给过程分；
- 研究合同以“能否失败”为合格线：只有成功指标、没有 falsifier 和 failure state 的方案不合格。

## 1. A 区：对象、量词与证据分层

### 第 1 题

1. **错误。** 有限随机测试只能提供所测试分布与实现下的经验反例搜索。要证明全称命题需解析证明；一个未抽到的输入就是可能反例。
2. **错误。** intrinsic object 是 differential $df_x$。若 metric matrix 为 $G\succ0$，同一 $df$ 的 gradient 为 $G^{-1}\nabla_{\rm Euclid}f$。
3. **错误。** 实对称矩阵才保证实标准正交 eigenbasis。旋转矩阵可无实特征向量；Jordan block 不可对角化。
4. **错误。** 前向误差通常至多由 condition number 乘 backward error/residual scale 控制；病态系统可小残差而大解误差。
5. **错误。** $X\sim\mathcal N(0,1)$、$Y=X^2$ 有 $\operatorname{Cov}(X,Y)=0$，但显然依赖。联合 Gaussian 时零协方差才推出独立。
6. **错误。** KL 非负但通常不对称，也不满足三角不等式；它是 divergence，不是 metric。
7. **错误。** $f(x)=x^3$ 在 0 梯度为零但不是极小。还需凸性、二阶充分条件或更高阶/邻域分析。
8. **错误。** 对 $x'=-ax$，Euler multiplier 为 $1-ha$；连续系统对 $a>0$ 稳定，但 Euler 要 $|1-ha|<1$，即 $0<h<2/a$。
9. **错误。** kernel PSD 要求对任意 $n$、任意样本点和任意系数都非负。一张 finite Gram matrix 只能验证一个有限实例。
10. **错误。** AD 对实际 program 应用局部 rule，并以浮点执行；custom VJP、控制流、overflow、condition 和 nondifferentiable convention 都可能出错，需 Taylor/adjoint/reference tests。

### 第 2 题

一份合格合同可写成：

| 层 | 对象 |
|---|---|
| 数据 | 固定样本 $(h_i,y_i)$，$h_i\in\mathbb R^d$，$y_i\in\{1,\ldots,C\}$；若谈 population risk，另声明 $(H,Y)\sim P$ |
| 参数 | $W\in\mathbb R^{m\times m}$、$U\in\mathbb R^{m\times d}$、$V\in\mathbb R^{C\times m}$；batch $H\in\mathbb R^{B\times d}$ |
| primal maps | $T_h:\mathbb R^m\to\mathbb R^m$，$T_h(z)=\phi(Wz+Uh)$；$z^*(h)$ 是其 fixed point；$Vz^*\in\mathbb R^C$ |
| probability | softmax 给 categorical conditional law；经验交叉熵不是 population entropy，也不是模型正确性的证明 |
| differential | $dL$ 是参数空间上的 covector；Euclidean/Frobenius metric 下用 gradient arrays 表示 |
| propagation | JVP 为 Jacobian 对 tangent 的作用；VJP/adjoint 把 output cotangent pull back；不需要物化完整 Jacobian |

若 $D=\operatorname{diag}(\phi')$，参数扰动引起的 state tangent 需解

$$
(I-DW)\,\dot z=D(\dot Wz+\dot Uh).
$$

scalar loss 的 adjoint 则解 $(I-DW)^T\lambda=\nabla_zL$，shape 均为 $m$。这里默认 Euclidean state metric 与 Frobenius parameter metric；换 metric 时 gradient representation 改变。

必须分开四个程序/对象：

1. $z^*$：无限精度方程的 exact local/global fixed point；
2. $z_K$：具体初始化、容差与 $K$ 步迭代定义的实际 primal output；
3. implicit derivative：exact branch 满足正则条件时的数学导数；
4. $\widehat g$：以有限精度和不完全 linear solve 得到的 gradient estimate。

充分的基本条件包括：$T_h$ 是 contraction 或用其他定理保证 branch；$\phi$ 在所需点可微；$I-DW$ nonsingular 且不过度病态；softmax/log 的 label support 与稳定 log-sum-exp 实现正确；primal 与 adjoint residual、dtype、stopping 和 non-finite state 可审计。

四层合法声明示例：定理层“若 $\|W\|<1$ 且 $\phi$ 1-Lipschitz，则 fixed point 唯一”；近似层“在给定 contraction 下 $\|z_K-z^*\|\le q^K\|z_0-z^*\|$”；数值层“当前 dtype 与 tolerance 下 true residual 为某值”；经验层“在预注册数据/seed 下 validation loss 的区间为某值”。越界例分别是：有限 run 证明所有参数 contraction；training loss 下降证明 implicit derivative 正确；小 residual 在病态问题上证明小 forward error；单数据集提升证明 population 普遍改进。

## 2. B 区：跨卷手算与尺度追踪

### 第 3 题

因为 $c^T\Sigma c=5$ 且 noise variance 为 1，

$$
\operatorname{Var}(Z)=6,\qquad
\operatorname{Cov}(X,Z)=\Sigma c=\begin{bmatrix}4\\1\end{bmatrix}.
$$

联合 Gaussian conditioning 给出

$$
\mathbb E[X\mid Z=z]=\frac16\begin{bmatrix}4\\1\end{bmatrix}z,
$$

$$
\operatorname{Cov}(X\mid Z)
=\Sigma-\frac16
\begin{bmatrix}4\\1\end{bmatrix}
\begin{bmatrix}4&1\end{bmatrix}
=\begin{bmatrix}4/3&-2/3\\-2/3&5/6\end{bmatrix}.
$$

linear Gaussian channel 的信息为

$$
I(X;Z)=h(Z)-h(\varepsilon)=\frac12\log\frac6{1}=\frac12\log6.
$$

$Z$ 同时混合 $X_1,X_2$ 并共享同一 noise；一般 $I((X_1,X_2);Z)$ 不是 $I(X_1;Z)+I(X_2;Z)$。chain rule 是 $I(X_1;Z)+I(X_2;Z\mid X_1)$，第二项含条件而不是边缘 MI。

将 trace 移动到 $W$：

$$
R(W)=\frac12\operatorname{tr}((W-I)\Sigma(W-I)^T),
\qquad \nabla_WR=(W-I)\Sigma.
$$

rank-one orthogonal projector $W=uu^T$ 保留一个 eigendirection。Eckart–Young/PCA 变分原理要求保留 eigenvalue 4 的第一坐标，故

$$
W_*=\begin{bmatrix}1&0\\0&0\end{bmatrix},
\qquad R(W_*)=\frac12\cdot1=\frac12.
$$

matrix determinant lemma 或 log-det differential 给出

$$
\left.\frac d{d\theta}\log\det(\Sigma+\theta vv^T)\right|_0
=\operatorname{tr}(\Sigma^{-1}vv^T)=v^T\Sigma^{-1}v.
$$

接近奇异时 $\Sigma^{-1}$ 放大扰动，显式 inverse 和直接 determinant 都不可靠；应使用 Cholesky/solve、condition estimate 与稳定 log-det。

### 第 4 题

$\nabla f=Hx-b$，所以 $x_*=H^{-1}b=(1,1)^T$。$H$ 的 eigenvalues 为 1 和 9，因此 $\mu=1,L=9,\kappa_2(H)=9$。

令 $e_k=x_k-x_*$，则

$$
e_{k+1}=(I-\eta H)e_k.
$$

对两方向同时严格收敛需 $|1-\eta\lambda_i|<1$，故 $0<\eta<2/9$。$\eta=0.2$ 时 multipliers 为 $0.8$ 与 $-0.8$，谱半径 $0.8$；第二方向符号交替，故振荡但包络收缩。

固定正步长的 worst-case contraction 为

$$
\rho(\eta)=\max\{|1-\eta\mu|,|1-\eta L|\}.
$$

最优点平衡两个端点：$1-\eta\mu=-(1-\eta L)$，得到

$$
\eta_*=\frac2{L+\mu}=0.2,
\qquad \rho_*=\frac{L-\mu}{L+\mu}=0.8.
$$

gradient flow 满足 $e'=-He$，所以

$$
e(t)=e^{-Ht}e(0)=\operatorname{diag}(e^{-t},e^{-9t})e(0).
$$

对该 ODE 做 forward Euler 得 $e_{k+1}=(I-hH)e_k$，即 $h=\eta$ 的 GD。连续 exponential 对任意 $t>0$ 衰减，不代表 Euler stability function $1+h\lambda$ 对任意 $h$ 位于 unit disk。

$A=\operatorname{diag}(1,3)$ 时 $\kappa_2(A)=3$，而 normal-equation Hessian $A^TA$ 的 condition 为 9；形成正规方程平方条件数。停止至少报告 true/relative residual、condition/backward-to-forward budget，以及 validation loss、prediction change 或 downstream gradient error 等 task quantity。

## 3. C 区：统一证明链

### 第 5 题

对三变量 mutual information 使用两种 chain-rule 展开：

$$
I(X;Y,Z)=I(X;Z)+I(X;Y\mid Z)
=I(X;Y)+I(X;Z\mid Y).
$$

因此

$$
I(X;Z)-I(X;Y)=I(X;Z\mid Y)-I(X;Y\mid Z).
$$

Markov chain $X\to Z\to Y$ 等价于给定 $Z$ 后 $X,Y$ 条件独立，所以 $I(X;Y\mid Z)=0$。于是

$$
I(X;Z)-I(X;Y)=I(X;Z\mid Y)\ge0,
$$

即数据处理不等式。等号当且仅当 $I(X;Z\mid Y)=0$，也就是在已有 $Y$ 后 $Z$ 不再含关于 $X$ 的额外信息；结合原 Markov 条件，$X\to Y\to Z$ 也成立。若 $X$ 是任务变量，这表达 $Y$ 对 $Z$ 中关于 $X$ 的信息充分，但不是无条件声称 $Y$ 保留 $Z$ 的所有信息。

InfoNCE 常只是指定 sampling/proposal/class 下的 lower bound；finite-sample MI estimator 有 bias/variance 和 dimension dependence；classification accuracy 只对应一个 task、hypothesis class 与 decision threshold。可做的敏感性检查包括：加入与任务无关但高熵 nuisance，比较 MI proxy 与 task accuracy；改变 negative count；用已知 Gaussian MI 的 synthetic truth 做 sample-size/seed sweep。任何有限实验都不能单独证明普遍 DPI 或表示充分性。

### 第 6 题

定义 $T_\theta(z)=\phi(Wz+b\theta)$。逐坐标 1-Lipschitz 与 $\|W\|_2\le q$ 给出

$$
\|T_\theta(z)-T_\theta(\tilde z)\|_2\le q\|z-\tilde z\|_2.
$$

$\mathbb R^m$ 完备，故 Banach 定理给唯一 fixed point。对 $z_{k+1}=T(z_k)$，

$$
\|z_k-z^*\|\le q^k\|z_0-z^*\|
\le\frac{q^k}{1-q}\|z_1-z_0\|.
$$

对 fixed-point equation 求导：

$$
z_\theta'=D(Wz_\theta'+b),
\qquad (I-DW)z_\theta'=Db.
$$

因为 $\|DW\|\le q<1$，Neumann series 收敛且

$$
(I-DW)^{-1}=\sum_{j=0}^\infty(DW)^j,
\qquad \|(I-DW)^{-1}\|\le\frac1{1-q}.
$$

令 $A=I-DW$。对 $L(z^*(\theta),\theta)$，解

$$
A^T\lambda=\nabla_zL.
$$

则

$$
\frac{dL}{d\theta}=\partial_\theta L+\lambda^TDb.
$$

对其他参数方向，只需把 $Db$ 换成 $D(\dot Wz+\dot b\,\theta+\cdots)$。显式 $A^{-1}$ 比 solve 更贵、更不稳定，也破坏 matrix-free structure。

若 $A\widehat u=r_0-\rho$，linear residual 为 $\rho=r_0-A\widehat u$，exact solution $u$ 满足

$$
\|u-\widehat u\|\le\|A^{-1}\|\,\|\rho\|,
$$

相对界还要带 $\kappa(A)$ 与恰当 scaling。误差账必须分开：$z_K-z^*$ 的 primal truncation；$\widehat u-u$ 的 linear-solve error；每个 matvec/reduction 的 floating error；以及 fixed-point model 本身与真实机制之间的 misspecification。小 linear residual 不修复其他三层。

### 第 7 题

令 $S=\operatorname{span}\{k(x_i,\cdot)\}_{i=1}^n$。任意 $f=f_S+f_\perp$，且 $f_\perp\perp S$。reproducing property 给

$$
f_\perp(x_i)=\langle f_\perp,k(x_i,\cdot)\rangle=0.
$$

因此 data-fit term 对 $f$ 与 $f_S$ 相同，而

$$
\|f\|_\mathcal H^2=\|f_S\|_\mathcal H^2+\|f_\perp\|_\mathcal H^2.
$$

$\lambda>0$ 时任何非零 $f_\perp$ 严格增大目标，所以 minimizer 在 $S$ 中。

对任意 $a\in\mathbb R^n$，

$$
a^TKa=\left\|\sum_i a_i k(x_i,\cdot)\right\|_\mathcal H^2\ge0.
$$

写 $f=\sum_i\alpha_i k(x_i,\cdot)$，predictions 为 $K\alpha$，目标为

$$
\|K\alpha-y\|_2^2+\lambda\alpha^TK\alpha.
$$

可取 $(K+\lambda I)\alpha=y$ 得到唯一 prediction/function；若 $K$ singular，coefficient representation 可能有冗余，但 $\lambda\|f\|^2$ 使 Hilbert-space objective 严格凸，从而预测函数唯一。

四层必须分开：kernel PSD 是对所有有限点集的全量词定义；一次 eigensolver 检查只验证一个 finite $K$ 且受 rounding；$K+\lambda I$ 的 condition 决定 coefficient solve 敏感性；泛化还需要 sampling、function-class complexity/noise 等统计条件。输入在流形时 ambient chord distance 可能把测地上远近或对称性表达错；可选 intrinsic/geodesic kernel、heat kernel，或证明 ambient embedding 在所研究尺度上 bi-Lipschitz 并做 chart/group transform audit。

## 4. D 区：AI 系统审计与迁移

### 第 8 题

单 head 可写 $Q,K\in\mathbb R^{n\times d_k}$、$V\in\mathbb R^{n\times d_v}$，logits $L=QK^T/\sqrt{d_k}\in\mathbb R^{n\times n}$，故 $\operatorname{rank}L\le d_k$。mask 后 row-softmax $A\in\mathbb R^{n\times n}$，output $AV\in\mathbb R^{n\times d_v}$。LoRA 对某 weight $W_0\in\mathbb R^{d_{out}\times d_{in}}$ 用 $\Delta W=BA$，$B\in\mathbb R^{d_{out}\times r}$、$A\in\mathbb R^{r\times d_{in}}$，只保证 update rank 至多 $r$。

elementwise exponential 和 row normalization 不是 rank-preserving linear maps。即使 logits rank 1，取两行不成比例的 softmax probability vectors 就可得到 rank 2；例如 logits rows $(0,0)$ 与 $(0,a)$（它们组成的 logits matrix rank 1）在 $a\ne0$ 时 softmax rows 不相同也不成比例，所得 $2\times2$ stochastic matrix rank 2。algebraic rank 是 exact nonzero singular values 数；numerical/effective rank 依 threshold/entropy/stable-rank 定义；task dimension 还依 label/function，而非只依 spectrum。

验证可用 directional Taylor test 或 adjoint pairing

$$
\langle J\Delta\theta,u\rangle=\langle\Delta\theta,J^*u\rangle,
$$

覆盖 causal/padding masks、shared parameters、batch/head broadcast、sum-vs-mean reduction 与 all-masked rows。联合报告 logits/attention/update 的 spectra、rank-$r$ approximation residual、held-out loss/calibration、softmax max shift、non-finite/underflow counts、accumulator dtype 与 seed interval。当前最多可说“在指定任务、预算、dtype 和 seeds 下，rank-$r$ update 达到给定误差/性能”；不能推出无损等价 full fine-tuning，也不能由 loss 下降推出 VJP 正确或所有部署输入数值稳定。

### 第 9 题

sample path 是一次 $t\mapsto X_t(\omega)$；marginal law 是固定 $t$ 的 $p_t$；path law 是整个轨迹空间上的概率律；current 描述密度通量；deterministic flow map 把初值映到状态。probability-flow ODE 可与 SDE 共享每个时间的 marginals，但没有 Brownian quadratic variation，通常 path law 与单条路径均不同。

对 state-independent scalar diffusion，forward FPE 为

$$
\partial_t p=-\nabla\cdot(fp)+\frac12g(t)^2\Delta p.
$$

以反向物理时间书写 reverse SDE drift 时必须固定时钟 convention；常见从 $T$ 向 0 积分的形式为

$$
dX=[f-g^2\nabla\log p_t]dt+g\,d\bar W_t,
$$

其中 $dt<0$ 对应反向积分约定。probability-flow ODE 为

$$
dX=[f-\tfrac12g^2\nabla\log p_t]dt.
$$

前者是 full-score coefficient，后者是 half-score。state-dependent diffusion 还需 divergence/correction 项，不能机械套式。

实验账可分为：固定 exact score/解析 marginal 改 terminal prior；固定 terminal 与 solver 扫 score bias；固定 exact score 扫 step/tolerance/order；固定数学算法扫 dtype/tolerance/true residual；固定生成器用 independent samples 报 Monte Carlo interval/ESS。单条 FID/quality curve 混合了这些来源，既不证明 reverse formula，也不证明 likelihood 或 path-law 等价。

### 第 10 题

至少应声明：输入空间如 $H^s(M)$ 或 $L^2(M,\mu)$；输出/solution space 和 norm；目标 operator $\mathcal G$ 的 continuity topology；PDE 是 strong/weak/variational 哪种 solution；$M$ 的 metric、measure、charts/boundary；mesh-to-function 与 function-to-grid maps；训练/测试 population law。

逻辑跳跃包括：$L^2$ equivalence class 没有稳定 point evaluation；低网格误差不推出 continuum operator norm 小；fixed chart 表现不推出 coordinate invariance/equivariance；一致性没有 stability 不能推出 convergence；弱解正则性不足时 strong residual 无定义或不可靠；有限训练分布不推出任意输入；有限维紧性直觉不可直接搬到 infinite-dimensional unit ball。

合格测试包括：嵌套 mesh 上相同 continuum input 的 refinement curve；chart/group transform 前后比较 equivariance defect；weak residual、energy/Sobolev norm 而非只看 pointwise MSE；对一组规范化 directions 估计 operator error proxy；在预注册 frequency/geometry/distribution shifts 上外推。它们分别只支持所选 mesh family、transforms、test function class 和 sampled directions；即使全部通过，也不证明对整个 infinite-dimensional unit ball 的 uniform operator-norm convergence。

## 5. E 区：研究合同评分样例

第 11 题没有唯一措辞，但满分答案必须形成以下闭环。

### 5.1 以 preconditioned implicit layer 为例

**对象。** 声明 $F(z,\theta,x)=0$、state/parameter spaces、data law、Euclidean或加权 metric、forward/adjoint operators、baseline solver、FLOP/byte/NFE budget 和随机性。

**定理候选。** 例如：若 $F_z$ 在邻域 nonsingular、$\|I-M^{-1}F_z\|\le\rho<1$ 且 matvec/preconditioner 满足给定 perturbation bound，则 preconditioned correction 的 exact-arithmetic error 以 $\rho$ 收缩，并可把 adjoint forward error 由 residual 乘 $\|F_z^{-T}\|$ 控制。proof skeleton 是 error equation、operator-norm contraction 与 perturbation bound。边界包括 $M$ setup 过贵、非正规 transient、branch crossing、inexact/nonlinear preconditioner 和条件为空。

**近似。** 分开 finite-depth model bias、fixed-point truncation、training-sample generalization、preconditioner class restriction 和 linear-solve tolerance；不得把它们都称 solver error。

**计算。** 报 primal/adjoint true residual、backward error、condition proxy、iteration/matvec/preconditioner cost、dtype/accumulator、memory 与 failure states（stagnation、non-finite、budget、symmetry violation、negative curvature）。

**实验。** primary endpoint 可为在相同 wall-clock/energy 下的 held-out gradient directional error；多个 condition/non-normality families、seeds 和 dtypes；ablate preconditioner quality/setup reuse；预注册 tolerance 和 failure rate；保留预条件更慢或更差的结果。

**边界。** theorem 只覆盖 hypotheses 下的 mathematical iteration；simulation 可检验机制而不证明 population 普遍性；benchmark 支持指定硬件/数据/预算；case study 只给可迁移线索。完整来源需区分教材定理、原论文算法与博客线索，记录 environment lock、code revision、data license、SVG/hash 和失败 artifacts。

另两个选题也按同一七层评分：information bottleneck 必须区分 true MI、variational bound、task sufficiency 和 nuisance definition；symmetry-aware operator 必须区分 exact group action、discrete equivariance、mesh consistency/stability、continuum topology 与 distribution shift。

## 6. 跨卷错题路由

| 首个错误 | 先回链 | 随后用什么陌生题验证 |
|---|---|---|
| 全称量词被实验替代 | [[命题、量词与逻辑等价]]、[[必要条件、充分条件与证明方法]] | 给一个有限测试全通过但全称命题假的反例 |
| shape / map / metric 错 | [[线性映射]]、[[伴随算子]]、[[梯度、方向导数与最陡方向]] | 在非 Euclidean metric 下重写 fixed-point adjoint |
| Gaussian / MI 对象混淆 | [[多元高斯分布]]、[[互信息与依赖性]] | 改变 observation direction 与 noise 后重算 |
| condition / residual 混淆 | [[条件数]]、[[前向误差与后向误差]] | 构造小 residual、大 forward error 的方向 |
| 连续 / 离散稳定混淆 | [[Lyapunov 稳定性与能量函数]]、[[Euler、Runge-Kutta 与离散化误差]] | 对 stiff 两尺度系统画 stability threshold |
| implicit / adjoint 错 | [[逆矩阵、线性求解与隐式微分]]、[[逆函数定理与隐函数定理]] | 对新 nonlinear fixed point 写 primal 与 adjoint residual |
| kernel / finite Gram 越界 | [[正定核、RKHS 与表示定理]]、[[有界算子、紧算子与谱理论基础]] | 比较 finite matrix certificate 与 operator claim |
| diffusion 路径 / 边缘混淆 | [[Fokker-Planck 方程与概率流 ODE]]、[[时间反演、score 与扩散生成动力学]] | 构造同 marginals、不同 quadratic variation 的过程 |
| 网格 / 连续算子越界 | [[弱导数、Sobolev 空间与神经算子接口]] | 对同一 PDE 做 mesh、weak residual 与 norm 三重审计 |

## 7. 完成判据

本详解不会改变任何状态。只有十份分卷成绩、本卷原稿、[[实验 - 数学基础十卷跨章累计复现门]]、参数干预、48 小时重做、14 天迁移和口头答辩均留下真实证据，才可把课程状态从 `composed / not-attempted` 改为相应学习状态。课程总出口不是“公式都见过”，而是面对陌生 AI 论证时能主动建立：

$$
\boxed{\text{object}\to\text{hypothesis}\to\text{claim}\to\text{proof/algorithm}\to\text{evidence}\to\text{boundary}}.
$$
