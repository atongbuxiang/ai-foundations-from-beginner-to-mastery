---
type: exercise
status: draft
area: [math/functional-analysis, math/pde, math/numerical-analysis, ai/scientific-machine-learning, ai/neural-operators]
topic: "弱导数、Sobolev 空间与神经算子接口"
prerequisites: ["[[弱导数、Sobolev 空间与神经算子接口]]"]
related: ["[[练习与测验 MOC]]", "[[解答 - 弱导数、Sobolev 空间与神经算子接口]]", "[[实验 - 弱导数、变分残差与解算子频谱审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 弱导数、Sobolev 空间与神经算子接口

> [!abstract] 作答合同
> 共 15 题，A–E 每层 3 题。先闭卷保留原稿，再查正文。所有定理题都必须写 domain、function space、norm 与条件；所有 AI 题都必须区分 continuum object、discretization、sampling loss 和 deployment distribution。建议 A/B 90 分钟、C/D 180 分钟、E 150 分钟。

## A. 对象、定义与条件识别

### GEO-SOB-A01 分布、弱导数与 Sobolev 对象合同

逐项精确定义：

1. $C_c^\infty(\Omega)$ 与 distribution $\mathcal D'(\Omega)$；
2. locally integrable function 诱导的 regular distribution；
3. $D^\alpha T$ 的 distribution derivative；
4. $u\in L^1_{\rm loc}$ 的 weak derivative；
5. $W^{k,p}(\Omega)$、$H^k(\Omega)$ 与 $W_0^{1,p}(\Omega)$；
6. $H^{-1}(\Omega)$。

然后解释：为什么“每个 distribution 都可微”不推出“每个 $L^1_{\rm loc}$ 函数都属于 $W^{1,p}$”？弱导数的唯一性是哪一种唯一性？

### GEO-SOB-A02 四个 Sobolev 定理的条件表

为下列结论写出课程版条件、结论与一个删条件后的风险：

1. Trace theorem 与 $W_0^{1,p}=\ker\operatorname{Tr}$；
2. Poincaré inequality；
3. Sobolev/Morrey embedding：分别讨论 $p<d,p=d,p>d$；
4. Rellich–Kondrachov compact embedding。

特别解释：为什么 $H^1$ 元素的 point value 在高维中未必有意义？为什么 $H^1(\mathbb R^d)\to L^2(\mathbb R^d)$ 不是 compact？

### GEO-SOB-A03 三种“弱”与三类学习对象

完成下表，并为每一行给出一个典型公式：

| 概念 | 对象所在空间 | “弱”掉了什么 | 比较/检验方式 |
|---|---|---|---|
| weak derivative |  |  |  |
| weak PDE formulation |  |  |  |
| weak convergence |  |  |  |

再区分：

1. strong-form PINN；
2. Deep Ritz；
3. weak/variational PINN；
4. DeepONet/FNO operator learner。

说明它们分别学习一个函数还是函数到函数的映射，loss 属于哪一层。

## B. 手算与最小例子

### GEO-SOB-B01 $|x|$、Heaviside 与 ReLU 的分布导数

在 $(-1,1)$ 上：

1. 从测试函数定义推导 $D|x|=\operatorname{sign}(x)$；
2. 推导 $D^2|x|=2\delta_0$；
3. 对 $H(x)=\mathbf1_{(0,1)}(x)$ 推导 $DH=\delta_0$（测试函数支集在 $(-1,1)$）；
4. 推导 $D(x_+)=H$、$D^2(x_+)=\delta_0$；
5. 分别判断这些函数是否属于 $W^{1,p}$、$W^{2,p}$，$1\le p\le\infty$；
6. 解释为什么“跳跃函数 a.e. 导数为零”不能作为其弱导数。

### GEO-SOB-B02 一维 Poisson 的弱形式与能量

考虑

$$
-u''(x)=\pi^2\sin(\pi x),\quad x\in(0,1),
\qquad u(0)=u(1)=0.
$$

1. 从强形式推导 $H_0^1(0,1)$ 上的弱形式；
2. 写出 energy $J(v)$；
3. 验证 $u(x)=\sin(\pi x)$ 是 weak solution；
4. 计算 $\|u\|_{L^2}$、$|u|_{H^1}$ 和 $J(u)$；
5. 证明对任意 $v\in H_0^1$，$J(v)-J(u)=\frac12|v-u|_{H^1}^2$；
6. 若改为 pure Neumann $u'(0)=u'(1)=0$，判断原 forcing 是否满足 compatibility condition。

### GEO-SOB-B03 Fourier 模态、负阶 forcing 与 Poisson 平滑

在 $(0,1)$ 的 sine basis $e_k(x)=\sqrt2\sin(k\pi x)$ 上，设

$$
f=\sum_{k\ge1}f_ke_k,
\qquad -u''=f,\quad u|_{\partial\Omega}=0.
$$

1. 求 $u_k$；
2. 用 spectral weights 写出等价的 $H^s$ norm；
3. 证明形式上 $f\in H^{s-2}$ 推出 $u\in H^s$，并给出 norm estimate；
4. 对 $f=e_K$，比较 input $L^2$ norm、output $L^2$ norm 与 output $H^1$ seminorm；
5. 对只保留前 $m$ 个模态的 truncation operator，求 $L^2\to L^2$ operator-norm error；
6. 解释为何 high-mode OOD 样本可具有很小 absolute output error，却有 100% relative error。

## C. 证明与推导

### GEO-SOB-C01 弱导数唯一性、乘积规则与 mollification

1. 证明 weak derivative a.e. 唯一；
2. 若 $u\in W^{1,p}(\Omega)$、$\psi\in C_c^\infty(\Omega)$，证明 $\psi u\in W^{1,p}$ 且
   $$D_i(\psi u)=\psi D_i u+uD_i\psi;$$
3. 对 $u\in W^{1,p}(\mathbb R^d)$，证明 $D_i(\rho_\varepsilon*u)=\rho_\varepsilon*D_i u$；
4. 说明为何 $u_\varepsilon\to u$ in $W^{1,p}$ 对 $1\le p<\infty$；
5. 指出在有边界区域直接卷积会出现什么问题，以及 extension/local mollification 如何修复。

### GEO-SOB-C02 Lax–Milgram、能量与 Neumann kernel

令 $V=H_0^1(\Omega)$，$\Omega$ 为 bounded Lipschitz domain，$A(x)$ measurable、bounded 且 uniformly elliptic。定义

$$
a(u,v)=\int_\Omega \nabla u^\top A(x)\nabla v,
\qquad \ell\in H^{-1}(\Omega).
$$

1. 证明 $a$ continuous；
2. 在适当对称性条件下证明 coercive；
3. 用 Lax–Milgram 得到 weak solution 的存在、唯一和 stability estimate；
4. 当 $A=A^\top$ 时证明弱解是 energy minimizer；
5. 改为 pure Neumann space $H^1(\Omega)$ 后，指出 coercivity 为什么失效；
6. 在 quotient $H^1/\mathbb R$ 或 zero-mean subspace 中修复，并写 compatibility condition。

### GEO-SOB-C03 Galerkin orthogonality、Céa 与一维速率

设 $a$ 在 Hilbert space $V$ 上 continuous/coercive，$V_h\subset V$ conforming。

1. 推导 Galerkin orthogonality；
2. 完整证明 Céa 引理；
3. 对一维 uniform mesh 上的 continuous piecewise-linear interpolant $I_hu$，证明或引用并解释
   $$|u-I_hu|_{H^1}\le Ch|u|_{H^2};$$
4. 推出 energy error $O(h)$；
5. 说明 $L^2$ error $O(h^2)$ 还需要什么 duality/regularity；
6. 若区域角点使 $u\notin H^2$，解释哪一步断裂，而不是笼统说“有限元失效”。

## D. 反例、条件删除与数值陷阱

### GEO-SOB-D01 十二个错误命题

逐项判定并给证明、反例或缺失条件：

1. a.e. differentiable 且 classical derivative 在 $L^p$ 就一定属于 $W^{1,p}$；
2. 每个 distribution derivative 都由普通函数表示；
3. 修改 $L^p$ 函数在边界上的值就能施加 Dirichlet condition；
4. $C_c^\infty(\Omega)$ 总在 $W^{1,p}(\Omega)$ 中稠密；
5. $W^{1,d}$ 总嵌入 $L^\infty$；
6. $H^1(\Omega)$ bounded sequence 总有 $H^1$ strongly convergent subsequence；
7. weak convergence 加 norm convergence 与 strong convergence无关；
8. Lax–Milgram 自动给 $H^2$ classical solution；
9. Galerkin residual 在 $V_h$ 上为零说明 $u_h=u$；
10. finite collocation residual 为零说明连续 residual 为零；
11. AD 能证明真实 PDE 解具有网络所用导数阶数；
12. Neural operator 的 universal approximation theorem 保证训练算法在 OOD 网格上泛化。

### GEO-SOB-D02 分片线性有限元的“残差悖论”

对 B02 的 Poisson 问题，取 uniform mesh 和 conforming piecewise-linear FEM solution $u_h$。

1. 说明 $u_h''=0$ 在每个 open element 内成立；
2. 写出逐单元 interior strong residual；
3. 说明 $D^2u_h$ 作为 distribution 为什么包含 node deltas，并求其权重与 slope jumps 的关系；
4. 证明 $R(v_h)=0$ 对所有 $v_h\in V_h$；
5. 构造一个 residual functional $R\in H^{-1}$ 的表达，并解释为什么其 dual norm 才与 energy error自然相配；
6. 给出一个会误判 FEM 质量的 collocation evaluation protocol，并给出修正方案。

### GEO-SOB-D03 Embedding、compactness 与采样盲区

分别构造或解释下列机制：

1. 在 $\mathbb R^d$ 中用 translations 破坏 $H^1\to L^2$ compactness；
2. 用 concentrating/scaling sequence 说明临界 embedding 的 compactness为何危险；
3. 构造在所有有限 collocation points 取零、但在点间有窄峰的 smooth function；
4. 说明为何 empirical point residual loss 为零不控制 continuum $L^2$ residual；
5. 给出至少两种补救：random resampling、adaptive sampling、integral quadrature、weak tests 或 stability-based estimator；
6. 指出这些补救仍不能自动解决的一个问题。

## E. AI 接口、实验设计与研究审计

### GEO-SOB-E01 PINN、Deep Ritz 与 VPINN 的公平比较

为二维 variable-coefficient elliptic PDE

$$
-\nabla\cdot(a(x)\nabla u)=f,\qquad u|_{\partial\Omega}=0
$$

设计三条可复现实验管线：strong PINN、Deep Ritz、VPINN/VarNet。必须写明：

1. trial space 与 boundary enforcement；
2. strong/energy/weak loss 的精确公式；
3. 所需 derivative order；
4. sampling/quadrature 与 test basis；
5. 统一的 continuum-quality reference 与 $L^2/H^1$/boundary metrics；
6. 计算预算、seed 和 stopping rule；
7. 至少四个 failure probes；
8. 哪些比较结论只在当前实验分布上成立。

### GEO-SOB-E02 DeepONet/FNO 的解算子泛化合同

学习 $\mathcal G:a\mapsto u$，其中 $a$ 是 elliptic coefficient field。

1. 声明输入/输出 function spaces、ellipticity class 与 data distribution；
2. 为 DeepONet 设计 sensor audit，为 FNO 设计 Fourier mode/aliasing audit；
3. 区分 train resolution、test resolution 和 reference resolution；
4. 设计四类 OOD：频谱、相关长度、系数幅度、几何/边界；
5. 报告 absolute、relative、energy 与 conservation/residual metrics；
6. 解释“same parameters can run”为什么不是 resolution convergence；
7. 写出一个 falsification criterion：出现什么结果时必须撤回“学到了 continuum operator”的说法。

### GEO-SOB-E03 Sobolev training 与导数标签审计

考虑同时监督 $f(x_i)$ 与 $\nabla f(x_i)$ 的模型。

1. 写出带量纲归一化的 value/gradient objective；
2. 解释它近似哪个 empirical Sobolev-type norm；
3. 分析 finite-difference gradient label 的 noise amplification；
4. 对含 kink/interface 的目标说明 classical derivative label 哪里失效；
5. 设计 value-only、gradient-only、joint 三组 ablation；
6. 分别在 in-distribution、interpolation gap 与 OOD frequency 上评估；
7. 给出 calibration/uncertainty 与 derivative error 的联合报告；
8. 写出三条会让“导数监督更好”这一结论失效的证据。

