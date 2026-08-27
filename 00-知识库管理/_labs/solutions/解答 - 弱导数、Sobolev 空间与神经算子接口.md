---
type: solution
status: draft
area: [math/functional-analysis, math/pde, math/numerical-analysis, ai/scientific-machine-learning, ai/neural-operators]
topic: "弱导数、Sobolev 空间与神经算子接口"
exercise: "[[习题 - 弱导数、Sobolev 空间与神经算子接口]]"
prerequisites: ["[[弱导数、Sobolev 空间与神经算子接口]]"]
related: ["[[练习与测验 MOC]]", "[[实验 - 弱导数、变分残差与解算子频谱审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 弱导数、Sobolev 空间与神经算子接口

> [!abstract] 使用方式
> 本文逐题独立作答，不用“见正文”替代推导。比对时优先检查：distribution/weak derivative 是否分开，Sobolev 定理是否保留 domain 与指数条件，弱 PDE 是否写全 trial/test space，AI loss 是否与 continuum norm、quadrature、discretization 和 OOD 分账。

## A01 解答：分布、弱导数与 Sobolev 对象合同

1. $C_c^\infty(\Omega)$ 由支集 compactly contained in $\Omega$ 的光滑函数组成。Distribution 是该 test-function space 上的连续线性泛函，记 $T\in\mathcal D'(\Omega)$；连续性相对于标准 test-function topology。
2. $u\in L^1_{\rm loc}(\Omega)$ 诱导
   $$T_u(\varphi)=\int_\Omega u\varphi.$$
   这是 regular distribution；并非每个 distribution 都来自普通函数，例如 $\delta_{x_0}$。
3. 对任意 $T\in\mathcal D'$，
   $$\langle D^\alpha T,\varphi\rangle=(-1)^{|\alpha|}\langle T,D^\alpha\varphi\rangle.$$
4. 若 $u\in L^1_{\rm loc}$ 且 $D^\alpha T_u=T_v$ 对某个 $v\in L^1_{\rm loc}$ 成立，则 $v$ 是 $u$ 的 weak derivative。
5. 
   $$W^{k,p}=\{u\in L^p:D^\alpha u\in L^p,|\alpha|\le k\}.$$
   $H^k=W^{k,2}$。$W_0^{1,p}$ 是 $C_c^\infty(\Omega)$ 在 $W^{1,p}$ norm 下的 closure；在 Lipschitz domain 上可识别为 zero-trace subspace。
6. 对 $V=H_0^1(\Omega)$，$H^{-1}(\Omega)=V^*$，其中对象作用于 $H_0^1$ tests，而不一定是普通 $L^2$ 函数。

分布导数总存在，是因为导数被转移到任意光滑 test 上；但结果可能是 delta 或更奇异的 distribution，未必由 $L^p$ 函数表示。Weak derivative 的唯一性是 **a.e. 唯一**：两个代表函数可在 measure-zero set 上不同。

## A02 解答：四个 Sobolev 定理的条件表

| 定理 | 课程版条件 | 结论 | 删除条件的风险 |
|---|---|---|---|
| Trace | $\Omega$ Lipschitz，$1\le p<\infty$ | continuous $\operatorname{Tr}:W^{1,p}(\Omega)\to$ 合适的 boundary space；$W_0^{1,p}=\ker\operatorname{Tr}$ | 粗糙边界上 trace 可能需更精细定义或失效 |
| Poincaré | $\Omega$ bounded、connected、规则；$u\in W_0^{1,p}$ | $\|u\|_p\le C\|\nabla u\|_p$ | 无 zero trace/zero mean 时 constants 反例 |
| Sobolev | 有界 extension domain 等常用规则性 | $p<d$: $L^{p^*}$；$p=d$: 所有 finite $L^q$；$p>d$: Hölder/Morrey | 临界 $p=d$ 不一般给 $L^\infty$；非常规 domain 可能破坏结论 |
| Rellich | 有界规则 domain，目标指数严格 subcritical | $W^{1,p}\Subset L^q$ | 临界指数、无界域或 translations 可破坏 compactness |

$H^1=W^{1,2}$。当 $d\ge2$ 时 $1$ 阶、$p=2$ 不总超过连续嵌入阈值 $p>d$；一个 $H^1$ 等价类没有天然 point value。即便在一维可选 continuous representative，也要明确这是 embedding theorem 的结果。

在 $\mathbb R^d$ 中取 nonzero $\psi\in C_c^\infty$，令 $u_n(x)=\psi(x-ne_1)$。其 $H^1$ norm 恒定，任意两个足够远的平移在 $L^2$ 中近乎正交，所以没有 $L^2$ Cauchy subsequence，故 embedding 不 compact。

## A03 解答：三种“弱”与四类学习对象

| 概念 | 对象所在空间 | 弱化内容 | 检验方式 |
|---|---|---|---|
| weak derivative | $u,v\in L^1_{\rm loc}$ | 不要求 difference quotient 在每点收敛 | $\int v\varphi=-\int u\partial_i\varphi$ 对所有 tests |
| weak PDE | $u\in V$，residual in $V^*$ | 把 derivatives 分配给 tests，PDE 不逐点要求 | $a(u,v)=\ell(v)$ 对所有 $v\in V$ |
| weak convergence | $u_n,u\in X$ | 不要求 norm distance趋零 | $\ell(u_n)\to\ell(u)$ 对所有 $\ell\in X^*$ |

Strong PINN 学一个 $u_\theta(x)$，用 finite points 近似 strong residual norm；Deep Ritz 学一个 $u_\theta$，用 sampled energy；VPINN/VarNet 仍学一个 $u_\theta$，但检查 finite test functions 上的 weak residual。DeepONet/FNO 学的是 $\mathcal G_\theta:X\to Y$；训练 loss 对 input functions 的样本分布、output discretization 和 chosen $Y$ norm 做 empirical approximation。前面三者通常是 instance solver，最后一类是 family/operator learner。

## B01 解答：$|x|$、Heaviside 与 ReLU

对 $\varphi\in C_c^\infty(-1,1)$，

$$
\begin{aligned}
-\int_{-1}^1|x|\varphi'(x)dx
&=\int_{-1}^0x\varphi'(x)dx-\int_0^1x\varphi'(x)dx\\
&=-\int_{-1}^0\varphi(x)dx+\int_0^1\varphi(x)dx\\
&=\int_{-1}^1\operatorname{sign}(x)\varphi(x)dx.
\end{aligned}
$$

故 $D|x|=\operatorname{sign}(x)$ a.e. 再次分布微分：

$$
\langle D\operatorname{sign},\varphi\rangle
=-\int_{-1}^0(-1)\varphi'-\int_0^1(1)\varphi'
=2\varphi(0),
$$

所以 $D^2|x|=2\delta_0$。

对 $H=\mathbf1_{(0,1)}$，测试函数在 $1$ 附近可不为零吗？题目 domain 是 $(-1,1)$，支集 compactly contained in open interval，故 $\varphi$ 在 $1$ 的邻域为零：

$$
\langle DH,\varphi\rangle=-\int_0^1\varphi'=\varphi(0).
$$

所以 $DH=\delta_0$。又 $x_+=xH$，直接分段积分得 $D(x_+)=H$，继而 $D^2(x_+)=\delta_0$。

在 bounded interval 上：

- $|x|\in W^{1,p}$ 对所有 $p$，但不在任何 $W^{2,p}$；
- $H\in L^p$，但不在任何 $W^{1,p}$；
- $x_+\in W^{1,p}$ 对所有 $p$，但不在任何 $W^{2,p}$。

$H$ 的 classical derivative 在 $x\ne0$ 为零，却遗漏 jump 造成的 $\delta_0$；只有满足 test identity 的函数才能作为 weak derivative，因此零函数不是答案。

## B02 解答：一维 Poisson、能量与 compatibility

乘 $v\in H_0^1(0,1)$ 并分部积分：

$$
\int_0^1u'v'\,dx=\int_0^1\pi^2\sin(\pi x)v(x)\,dx.
$$

对应

$$
J(v)=\frac12\int_0^1|v'|^2dx
-\int_0^1\pi^2\sin(\pi x)v(x)dx.
$$

$u=\sin(\pi x)$ 满足 boundary condition，且 $-u''=\pi^2\sin(\pi x)$，故由分部积分是 weak solution。

$$
\|u\|_{L^2}^2=\int_0^1\sin^2(\pi x)dx=\frac12,
$$

$$
|u|_{H^1}^2=\int_0^1\pi^2\cos^2(\pi x)dx=\frac{\pi^2}{2}.
$$

因为 testing with $u$ 给 $\ell(u)=a(u,u)=\pi^2/2$，所以

$$
J(u)=\frac12a(u,u)-\ell(u)=-\frac{\pi^2}{4}.
$$

令 $e=v-u$。由 $\ell(e)=a(u,e)$，

$$
J(u+e)-J(u)
=\frac12a(e,e)+a(u,e)-\ell(e)
=\frac12|e|_{H^1}^2.
$$

Pure Neumann 的 compatibility 要求 $\int_0^1f=0$（homogeneous flux）。但

$$
\int_0^1\pi^2\sin(\pi x)dx=2\pi\ne0,
$$

所以该 forcing 与 homogeneous Neumann condition 不兼容。

## B03 解答：Fourier 模态与 Poisson 平滑

因为 $-e_k''=(k\pi)^2e_k$，

$$
u_k=\frac{f_k}{(k\pi)^2}.
$$

在 Dirichlet spectral scale 中可写

$$
\|v\|_{H^s_D}^2\asymp\sum_{k\ge1}(1+(k\pi)^2)^s|v_k|^2.
$$

于是

$$
\begin{aligned}
\|u\|_{H^s_D}^2
&\asymp\sum_k(1+(k\pi)^2)^s\frac{|f_k|^2}{(k\pi)^4}\\
&\le C\sum_k(1+(k\pi)^2)^{s-2}|f_k|^2
=C\|f\|_{H^{s-2}_D}^2.
\end{aligned}
$$

这给出二阶 elliptic smoothing；精确 domain regularity 仍依赖边界。

若 $f=e_K$，则 $\|f\|_2=1$，

$$
\|u\|_2=(K\pi)^{-2},\qquad |u|_{H^1}=(K\pi)^{-1}.
$$

令 $G_m$ 只保留 $k\le m$。$G-G_m$ 的最大 singular gain 在 $k=m+1$，故

$$
\|G-G_m\|_{L^2\to L^2}=\frac1{((m+1)\pi)^2}.
$$

对未保留的单一 high mode，模型输出零、真输出虽只有 $(K\pi)^{-2}$ 的小 absolute norm，但 error 等于真输出本身，所以 relative error 为 $1$。Absolute smoothing 不能替代 relative/OOD audit。

## C01 解答：唯一性、乘积规则与 mollification

若 $v,w$ 都是 $D_i u$，则

$$
\int_\Omega(v-w)\varphi=0\quad\forall\varphi\in C_c^\infty(\Omega).
$$

由 distribution 的基本引理，$v-w=0$ a.e.。

对 $\psi\in C_c^\infty$，

$$
\begin{aligned}
-\int\psi uD_i\varphi
&=-\int uD_i(\psi\varphi)+\int u(D_i\psi)\varphi\\
&=\int\psi(D_i u)\varphi+\int u(D_i\psi)\varphi.
\end{aligned}
$$

右端系数在 $L^p$，故 $D_i(\psi u)=\psi D_i u+uD_i\psi$。

在 $\mathbb R^d$，由 Fubini 与 distribution identity：

$$
D_i(\rho_\varepsilon*u)
=(D_i\rho_\varepsilon)*u
=\rho_\varepsilon*D_i u.
$$

Approximate identity theorem 给 $\rho_\varepsilon*u\to u$ in $L^p$，同时对每个 weak derivative 给

$$
\rho_\varepsilon*D_i u\to D_i u\quad\text{in }L^p,
$$

故在 $W^{1,p}$ 中收敛，$1\le p<\infty$。有边界时，zero extension 可能在边界制造 jump/delta；可先在 compactly contained subdomains 上局部卷积，或对 extension domain 使用 bounded extension operator 后再卷积。$p=\infty$ 的 norm convergence 不能无条件照抄 approximate-identity 结论。

## C02 解答：Lax–Milgram、能量与 Neumann kernel

设 $\|A(x)\|_{op}\le M_A$ a.e.，则 Cauchy–Schwarz 给

$$
|a(u,v)|\le M_A\|\nabla u\|_2\|\nabla v\|_2
\le C\|u\|_{H^1}\|v\|_{H^1}.
$$

若 symmetric part uniformly elliptic，

$$
a(v,v)\ge\lambda\|\nabla v\|_2^2.
$$

在 $H_0^1$ 上 Poincaré 使 $\|\nabla v\|_2$ 与 $H^1$ norm 等价，所以 $a$ coercive。Lax–Milgram 给唯一 $u\in H_0^1$ 且

$$
\|u\|_{H_0^1}\le C\lambda^{-1}\|\ell\|_{H^{-1}}.
$$

若 $A=A^\top$，令 $J(v)=\frac12a(v,v)-\ell(v)$。对任意 $w$，$DJ(u)[w]=a(u,w)-\ell(w)$；coercivity使 $J$ strictly convex，所以 weak solution 是唯一 minimizer。

Pure Neumann 时 constants 属于 $H^1$ 且 $a(c,c)=0$，故不 coercive；同时方程只能确定到 constants。可取

$$
V_\diamond=\left\{v\in H^1(\Omega):\int_\Omega v=0\right\}
$$

并用 zero-mean Poincaré，或在 quotient $H^1/\mathbb R$ 工作。若弱式右端为 $\ell(v)=\int_\Omega fv+\int_{\partial\Omega}gv$，兼容性是

$$
\ell(1)=\int_\Omega f+\int_{\partial\Omega}g=0.
$$

## C03 解答：Galerkin、Céa 与速率

连续和离散式分别为 $a(u,v_h)=\ell(v_h)$ 与 $a(u_h,v_h)=\ell(v_h)$，相减得

$$
a(u-u_h,v_h)=0\quad\forall v_h\in V_h.
$$

对任意 $w_h\in V_h$，$u_h-w_h\in V_h$，故

$$
\begin{aligned}
\alpha\|u-u_h\|_V^2
&\le a(u-u_h,u-u_h)\\
&=a(u-u_h,u-w_h)+a(u-u_h,w_h-u_h)\\
&=a(u-u_h,u-w_h)\\
&\le M\|u-u_h\|_V\|u-w_h\|_V.
\end{aligned}
$$

约去 error norm 并对 $w_h$ 取 infimum：

$$
\|u-u_h\|_V\le(M/\alpha)\inf_{w_h\in V_h}\|u-w_h\|_V.
$$

一维每个 element $K$ 上，interpolation error derivative 的均方可由 $u''$ 控制；scaling 到 reference interval 后求和得

$$
|u-I_hu|_{H^1(0,1)}\le Ch|u|_{H^2(0,1)}.
$$

取 $w_h=I_hu$ 即得 energy error $O(h)$。$L^2$ 的 $O(h^2)$ 通常用 Aubin–Nitsche：以 error 为 forcing 解 dual elliptic problem，并要求该 dual solution 有 $H^2$ regularity。若 corner singularity 使 primal 或 dual solution 不在 $H^2$，断裂的是 interpolation/regularity estimate，Galerkin orthogonality 和 Céa 本身仍成立；应采用降低速率、graded mesh 或 singular enrichment，而不是说方法完全失效。

## D01 解答：十二个错误命题

1. **错。** Cantor function a.e. derivative为零且在所有 $L^p$，但其 distribution derivative 是 singular Cantor measure，不是零函数，故不在 $W^{1,p}$。
2. **错。** $D H=\delta_0$ 不由 $L^1_{\rm loc}$ 函数表示。
3. **错。** Boundary 是 bulk measure-zero set，改值不改变 $L^p$ 等价类；需 trace/closure。
4. **错。** 其 closure 是 $W_0^{1,p}$，通常是带 zero trace 的 proper subspace；常数 $1$ 是直观反例。
5. **错。** 临界情形一般只嵌入所有 finite $L^q$ 或更精细的 Orlicz/BMO-type spaces，不自动到 $L^\infty$。
6. **错。** Infinite-dimensional unit ball 不 compact；即使 Rellich 给 $L^2$ strong subsequence，也不是 $H^1$ strong subsequence。
7. **错。** 在 uniformly convex/Hilbert space 中 weak convergence 加 norm convergence 推出 strong convergence；Hilbert proof 用 inner-product expansion。
8. **错。** Lax–Milgram只给 energy-space weak solution；$H^2$ 需 elliptic regularity。
9. **错。** Residual只对 finite $V_h$ tests消失；若 $u\notin V_h$ 仍有 approximation error。
10. **错。** 非零 smooth residual 可专门在有限 sample points 取零。
11. **错。** AD只对 chosen network expression 求导，不提供 true solution regularity theorem。
12. **错。** Universal approximation 是函数空间 compact set 上的参数存在性；不保证 finite data、optimization、OOD 或 resolution convergence。

## D02 解答：有限元残差悖论

Continuous piecewise-linear $u_h$ 在 element $K_j=(x_{j-1},x_j)$ 上是 affine，故 classical $u_h''=0$ there。若 PDE 写 $-u''=f$，interior strong residual 是

$$
r_K=-u_h''-f=-f\quad\text{inside }K.
$$

令 element slopes 为 $s_j$。Distribution derivative of $u_h'$ 含节点 jump：

$$
D^2u_h=\sum_{i=1}^{N-1}(s_{i+1}-s_i)\delta_{x_i}
$$

（边界项由 domain/test convention另行处理）。只在 element interior 做 AD/collocation 会漏掉这些 measures。

Galerkin equation 定义了 $u_h$，所以

$$
R(v_h):=\ell(v_h)-a(u_h,v_h)=0
\quad\forall v_h\in V_h.
$$

对一般 $v\in H_0^1$，

$$
R(v)=\ell(v)-a(u_h,v)
$$

是 $H^{-1}$ functional；若 $u$ 是精确解，$R(v)=a(u-u_h,v)$。因此

$$
\|R\|_{H^{-1}}\asymp\|u-u_h\|_{H_0^1}
$$

对 coercive elliptic operator成立到 continuity/coercivity constants。

错误 protocol：只在每个 element 的 interior uniformly sample strong residual，并以其 $L^2$ average 评价 linear FEM。这既忽略 interface delta，也用一个有限元 trial class本不具备的二阶 classical regularity要求它。修正可用 weak residual/dual norm、standard element residual加 flux-jump estimator，或比较 energy/$L^2$ error against refined reference；若研究 strong solution，则应选足够光滑 trial functions并包含边界/界面审计。

## D03 解答：compactness 与采样盲区

1. 取 $u_n(x)=\psi(x-ne_1)$。Norm恒定、质量逃向无穷远，没有 $L^2$ strong subsequence。
2. 临界 embedding 下可取保持源 norm 大致不变的缩放 bump
   $$u_\varepsilon(x)=\varepsilon^{-\gamma}\psi(x/\varepsilon),$$
   选择 $\gamma$ 平衡 scaling。它把质量集中到一点，weakly可能趋零但 target critical norm不趋零，破坏 compactness。
3. 给 finite points $x_i$，选不含任何 $x_i$ 的小 ball $B(x_0,r)$，取 nonzero $C_c^\infty$ bump $b$ supported there。则 $b(x_i)=0$，却 $\|b\|_{L^2}>0$；缩小 support、增大 amplitude 可制造窄高峰。
4. Empirical loss $N^{-1}\sum_i|r(x_i)|^2=0$ 只限制 evaluation vector，不能控制 points之间的 $\int|r|^2$。
5. Random resampling降低固定盲点，adaptive sampling针对大残差区，higher-order quadrature近似 integral，weak multi-scale tests聚合局部误差，stability-based estimator把 residual norm连到 solution error。
6. 这些都不能自动修复不适定 PDE、错误边界/物理模型、representation gap 或 optimization failure；仍需单独审计。

## E01 解答：三类 neural PDE solver 的公平比较

令 $a(x)\in[\lambda,\Lambda]$，$\Omega$ 固定为 bounded Lipschitz domain，reference 用独立高阶 FEM 并做 mesh convergence。

**共同 trial。** 用同一 base network width/depth/activation。Hard Dirichlet 可设 $u_\theta(x)=d(x)n_\theta(x)$，其中 $d|_{\partial\Omega}=0$；若用 penalty，三方法统一 boundary sample budget和权重搜索协议。

**Strong PINN：**

$$
L_s=Q_\Omega\big[|-\nabla\cdot(a\nabla u_\theta)-f|^2\big]+\lambda_bQ_{\partial\Omega}[|u_\theta|^2].
$$

需 $u_\theta$ 二阶导数和 $a$ 一阶导数（或展开方式匹配）；对 ReLU 不适合直接按 classical second derivative使用。

**Deep Ritz：**

$$
L_E=Q_\Omega\left[\frac12a|\nabla u_\theta|^2-fu_\theta\right]
$$

加 boundary enforcement，只需一阶导数；要求 symmetric coercive energy structure。

**VPINN/VarNet：** 取 multi-scale local/global tests $v_j$，

$$
L_w=\sum_jw_j|Q_\Omega[a\nabla u_\theta\cdot\nabla v_j-fv_j]|^2.
$$

只需 $u_\theta$ 一阶导数，但需 test design 与 quadrature。

公平性要求：相同 wall-clock/FLOP或明确两种预算；相同 train/validation coefficient fields；至少 10 seeds；同一 early-stopping rule；同时报 $L^2$ relative error、$H^1$ energy error、boundary error、continuum/refined-grid residual与耗时。Failure probes 至少包括：high contrast $a$、short correlation length、corner/interface、boundary layer、少样本 quadrature、loss-weight perturbation。结论只适用于声明的 $a$ distribution、domain、network和预算；不能从一个 benchmark 宣称某方法普遍更优。

## E02 解答：DeepONet/FNO 解算子泛化合同

可设

$$
X=\{a\in L^\infty(\Omega):0<\lambda\le a(x)\le\Lambda\},
\qquad Y=H_0^1(\Omega),
$$

并明确训练 $a$ 由何种随机场（例如 log-Gaussian、correlation length range、spectral cutoff）产生。若只在 finite grid上定义随机向量，就不能自动称作 continuum $X$ distribution。

DeepONet audit：增加 sensors、改变布局、检查两个 sensor-indistinguishable inputs、在新 query grid评估。FNO audit：vary retained modes，使用 de-aliased/high-resolution reference，检查 periodic padding、FFT normalization，并绘制 output error随 grid/mode 的曲线。

分三种 resolution：输入/标签生成的 reference grid $h_{ref}$，训练输入输出 grid $h_{train}$，部署 $h_{test}$。Reference应先证实 $h_{ref}$ refinement稳定。OOD axes：

- 输入含训练 cutoff外的高频；
- correlation length 更短/更长；
- $\Lambda/\lambda$ contrast超出训练；
- 新 domain shape 或 boundary condition。

Metrics至少含 absolute $L^2$、relative $L^2$、energy error、PDE weak residual/flux conservation，并按 input strata报告。Same parameters能接受不同 array sizes只说明 architecture/interface复用；若 $h_{test}\to0$ 时 error不趋于稳定 continuum limit，就没有 resolution convergence。

Falsification criterion示例：在固定 continuum input与不断 refined reference上，model predictions between grids 不一致，或 relative $H^1$ error随 refinement增长/停在不可解释高平台；此时必须撤回“学到 continuum operator”，改称“在特定离散分布上拟合良好”。

## E03 解答：Sobolev training 与导数标签

若 $f$ 与 coordinates有量纲，可写 standardized objective

$$
L=\frac1N\sum_i\frac{|f_\theta(x_i)-y_i|^2}{s_y^2}
+\lambda\frac1N\sum_i\sum_{j=1}^d
\frac{|\partial_jf_\theta(x_i)-g_{ij}|^2}{s_{g,j}^2}.
$$

它是 sampled/empirical $H^1$-type seminorm加 value norm，并不等于 continuum $H^1$ norm，除非 sampling/quadrature足够。

Centered finite difference

$$
g_h(x)=\frac{y(x+h)-y(x-h)}{2h}
$$

若两个 observations含 independent noise variance $\sigma^2$，gradient noise variance约为 $\sigma^2/(2h^2)$；$h$ 太小会严重放大 noise，太大则增加 truncation bias。含 kink/interface 时 classical derivative在界面不存在，左右 derivative不一致；把任意单值 label 当真值会错误平滑或扭曲目标，应使用 weak/interface conditions或避开并单独建模 singular set。

Ablation应保持 parameter、value sample、优化预算一致，比较 value-only、gradient-only和 joint，并扫描 $\lambda$。评估区分训练分布、sample gaps、超过训练 cutoff 的 OOD frequency；同时报告 value $L^2$、gradient error、worst-region error、calibration/error-vs-uncertainty与多 seed intervals。

下列证据足以否定笼统的“导数监督更好”：

1. 提高 in-sample derivative fit 却使 independent continuum value/$H^1$ error变差；
2. 优势只来自更大 label/compute budget，在 matched budget 下消失；
3. 对 noise、kink 或 OOD frequencies，joint model error/calibration显著恶化，且结论对 $\lambda$ 极不稳定。

