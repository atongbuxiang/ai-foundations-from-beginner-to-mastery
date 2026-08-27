---
type: exercise
status: draft
area: [math/riemannian-geometry, math/manifold-optimization, ai/geometric-learning]
topic: "Riemann 几何、测地线与流形优化"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Riemann 几何、测地线与流形优化]]", "[[光滑流形、切空间与余切空间]]", "[[投影、约束与可行方向]]"]
related: ["[[几何、泛函分析、核与算子基础 MOC]]", "[[练习与测验 MOC]]", "[[实验 - 坐标度量、测地能量与球面 Retraction 审计]]"]
solution: "[[解答 - Riemann 几何、测地线与流形优化]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Riemann 几何、测地线与流形优化

> [!abstract] 训练目标
> 从“弯曲空间上的最短路”直觉升级为可审计的 Riemannian geometry 与 optimization：能追踪 metric 的坐标变换，能从 $g$ 推导 gradient/connection/geodesic，能区分 length、energy、distance、Exp 与 retraction，并能审计 decoder pullback、natural gradient 和 matrix-manifold update 的条件。

> [!warning] 作答合同
> 每次使用 metric、gradient、geodesic、distance、projection、Exp/Log、retraction 或 convergence，必须写清 underlying manifold、base point、tangent space、所选 metric、local/global 范围与数值近似。不得用“几何上显然”跳过对象类型和适用条件。

## A. 定义、对象与边界

### GEO-RIE-A01

建立以下对象的“domain—codomain—依赖结构—坐标表示—global boundary”表：

1. Riemannian metric $g$；
2. induced point distance $d_g$；
3. differential $df_p$；
4. Riemannian gradient $\operatorname{grad}f(p)$；
5. connection $\nabla$ 与 Christoffel symbols；
6. exponential/logarithmic map；
7. retraction；
8. vector transport。

证明或反驳：

1. smooth structure 唯一决定 Riemannian metric；
2. $df_p$ 不依赖 metric，但 $\operatorname{grad}f(p)$ 依赖；
3. $d_g$ 可直接作用于 tangent vectors；
4. $\operatorname{Exp}_p$ 总是全局 bijection；
5. 每个 retraction 都等于某个 Riemannian exponential map；
6. Christoffel symbols 在一个 chart 中为零就说明 curvature 为零。

### GEO-RIE-A02

比较并给出最小反例：

1. curve image、parametrized curve、constant-speed curve；
2. length-critical、energy-critical、locally minimizing、globally minimizing geodesic；
3. metric completeness、geodesic completeness、compactness；
4. ambient distance、intrinsic Riemannian distance、learned semantic similarity；
5. Riemannian gradient、natural gradient、preconditioned gradient、mirror-descent direction。

要求准确陈述 Hopf–Rinow 的有限维 connected Riemannian 条件，并说明 infinite-dimensional 情形为什么不能直接调用。

### GEO-RIE-A03

对一个 embedded constraint $M=\{x:c(x)=0\}$ 和一个 latent decoder $g:\mathcal Z\to\mathcal X$，分别写完整 object contract：

1. intrinsic/ambient dimensions；
2. tangent and cotangent objects；
3. metric 来源；
4. gradient 计算；
5. finite update map；
6. rank/regularity condition；
7. 哪些 quantity coordinate invariant；
8. 哪些结论只是 finite-sample/numerical evidence。

解释为什么“$J_g^\top J_g$ 可计算”仍不保证它是条件良好的 Riemannian metric。

## B. 坐标、metric 与 geodesic 手算

### GEO-RIE-B01

在 Euclidean plane 的 polar chart

$$
F(r,\theta)=(r\cos\theta,r\sin\theta),
\qquad r>0
$$

中完成：

1. 从 $J_F^\top J_F$ 推导 $G=\operatorname{diag}(1,r^2)$；
2. 推导 metric 在 Cartesian/polar components 间的变换律；
3. 计算全部非零 Levi–Civita Christoffel symbols；
4. 写出 geodesic equations；
5. 验证 radial line $\theta=\theta_0$ 是 geodesic；
6. 判断 circle $r=R$ 是否 geodesic；
7. 解释 $G$ 非常数、$\Gamma\ne0$ 与 plane curvature 为零为何不矛盾；
8. 解释 $r=0$ 处 $\det G=0$ 是 chart failure 而不是 geometry degeneracy。

### GEO-RIE-B02

在 unit sphere $S^{n-1}$ 配 induced metric，取 $x\in S^{n-1}$、$v\in T_xS^{n-1}$：

1. 证明 $T_xS^{n-1}=\{v:x^\top v=0\}$；
2. 求 ambient vector $a$ 的 tangent/normal decomposition；
3. 对 $f(x)=-c^\top x$ 求 $\operatorname{grad}f(x)$；
4. 推导 $\operatorname{Exp}_x(v)$；
5. 验证 normalization $R_x(v)=(x+v)/\|x+v\|$ 是 retraction；
6. 展开到三阶并证明 $\|R_x(tv)-\operatorname{Exp}_x(tv)\|=O(t^3)$；
7. 求直接 Euler point $x+tv$ 的 norm residual 阶；
8. 分类 $f$ 的所有 stationary points，并用 Hessian/直接比较区分极小与极大。

### GEO-RIE-B03

考虑 conformal metric

$$
g_{ij}(x)=e^{2\phi(x)}\delta_{ij}
$$

定义在 $U\subset\mathbb R^d$：

1. 求 $g^{ij}$、volume density 与 $\operatorname{grad}_g f$；
2. 从 Christoffel formula 推导

$$
\Gamma^k_{ij}
=\delta^k_j\partial_i\phi
+\delta^k_i\partial_j\phi
-\delta_{ij}\partial^k\phi;
$$

3. 写出 geodesic equation；
4. 当 $\phi$ 常数时解释 geometry；
5. 当 $d=1$ 时构造坐标变换把 metric 拉直；
6. 说明 $d\ge2$ 时逐点分解 $G=H^\top H$ 为什么不自动给一个 flattening coordinate map。

## C. 定理与证明链

### GEO-RIE-C01

设 $\gamma:[a,b]\to M$ piecewise smooth：

1. 严格证明 length 在 orientation-preserving smooth reparameterization 下不变；
2. 推导

$$
E(\gamma)\ge\frac{L(\gamma)^2}{2(b-a)};
$$

3. 给出等号条件；
4. 构造同一 curve image 的两个 parametrizations，使 length 相同而 energy 不同；
5. 解释为什么用 energy 做 geodesic optimization 时要控制 speed/parameter；
6. orientation-reversing reparameterization 对 length 有何影响，对 initial/final endpoint 和 velocity 有何影响。

### GEO-RIE-C02

从 torsion-free 和 metric compatibility 推导 Koszul formula，并完成：

1. 用公式证明 Levi–Civita connection 的唯一性；
2. 在 coordinate frame 中推 Christoffel formula；
3. 证明 geodesic speed 恒定；
4. 推导 fixed-endpoint energy first variation；
5. 证明 energy-critical curve 满足 $\nabla_{\dot\gamma}\dot\gamma=0$；
6. 指出每一步使用了 torsion-free、metric compatibility、fixed endpoints 或 smoothness 中的哪项。

### GEO-RIE-C03

设 $M\subset\mathbb R^D$ 是 embedded submanifold、配 induced metric，$f=\bar f|_M$：

1. 证明 $\operatorname{grad}f=P_x\nabla\bar f$；
2. 证明 local minimizer 必满足 $\operatorname{grad}f=0$；
3. 对 retraction-smooth upper model

$$
f(R_x(\eta))
\le f(x)+\langle\operatorname{grad}f,\eta\rangle
+\frac L2\|\eta\|^2
$$

推导 fixed-step RGD 的下降式；
4. 在 $f\ge f_{\inf}$、$0<\alpha\le1/L$ 下推导

$$
\min_{k<K}\|\operatorname{grad}f(x_k)\|^2
\le\frac{2(f(x_0)-f_{\inf})}{\alpha K};
$$

5. 说明此结果为什么只给 first-order stationarity；
6. 删除 upper-model 或 lower-bound 条件，各构造一种失败机制。

## D. 反例、条件删除与声明审计

### GEO-RIE-D01

逐条判定并修正：

1. “metric matrix 的 entries 随位置变化，所以 manifold 是弯的。”
2. “所有 geodesics 都是全局 shortest paths。”
3. “$\Gamma^k_{ij}(p)=0$，所以 $R(p)=0$。”
4. “$J_g(z)$ full rank at sampled points，所以 decoder globally embeds latent space。”
5. “$G=J_g^\top J_g$ 是 PSD，所以一定能作 Riemannian metric。”
6. “直接沿 tangent gradient 走一步，constraint 仍精确成立。”
7. “Natural gradient 对任何 neural network 都 parameterization invariant 且可逆。”
8. “Retraction 和 Exp 都回到 manifold，所以算法完全相同。”

每条必须给：判定、缺失条件、最小反例、修正版与可计算诊断。

### GEO-RIE-D02

构造和分析以下三个独立例子：

1. 完备但非 compact 的 Riemannian manifold；
2. 非完备 manifold 上两个点间 distance infimum 或 geodesic extension 的边界；
3. sphere 上同一端点间多条 geodesics，其中只有部分 segment minimizing。

再解释：closed and bounded implies compact 为什么可由 Hopf–Rinow 在 finite-dimensional complete Riemannian manifold 中恢复，却不能从一般 metric-space 常识无条件推出。

### GEO-RIE-D03

审计一篇假想论文的声明：

> “我们训练一个 VAE，用 $G(z)=J_g(z)^\top J_g(z)$ 计算 geodesic。因为 path energy 低于直线插值，证明 learned manifold 正确恢复了真实 data geometry，并且语义插值全局最优。”

按六本账拆解：

1. decoder map/rank；
2. output metric 与 stochastic decoder；
3. numerical BVP solver；
4. local vs global geodesic；
5. population/data geometry identifiability；
6. semantic evaluation。

给出最小复现实验、negative controls、uncertainty report 与可允许的降级结论。

## E. AI 综合建模与研究设计

### GEO-RIE-E01

设计一个 decoder pullback geodesic benchmark，比较 straight latent line、decoded-chord path、Riemannian energy minimization 和 graph-initialized refinement。必须规定：

1. analytic synthetic decoder 与 ground-truth metric；
2. regular 与 rank-collapse regions；
3. endpoint pairs 跨度、cut/obstacle-like geometry 与 multiple starts；
4. length/energy、endpoint/ODE residual、speed variance 与 solver cost；
5. metric eigenvalue/condition audit；
6. discretization refinement 与 convergence；
7. deterministic artifact、seed、hash 与 assertions；
8. 哪些结果支持 numerical correctness，哪些不能支持 semantic superiority。

### GEO-RIE-E02

为 orthogonality-constrained representation learning 设计 Euclidean projected GD、QR-retracted RGD、polar-retracted RGD 与 penalty method 的比较：

1. 明确 Stiefel/Grassmann object 与 metric；
2. 推导 tangent projection；
3. 定义 retractions 和 sign convention；
4. 记录 loss、gradient norm、orthogonality residual、step norm 与 wall-clock；
5. 扫 condition、rank、batch noise 与 learning rate；
6. 分离 exact constraint、algorithmic stationarity 与 downstream generalization；
7. 设计 gauge-invariant subspace error；
8. 说明不能由一次任务胜负推出普适算法优越性。

### GEO-RIE-E03

设计 natural-gradient claim audit。比较 exact Fisher（小模型可枚举）、empirical Fisher、GGN、damped Fisher 与 block approximation：

1. 写出 statistical model 与 identifiable/redundant parameterization；
2. 对 reparameterization 前后比较 function-space update；
3. 报告 spectrum、rank、damping 与 solve residual；
4. 区分 direction invariance 与 finite-step invariance；
5. 比较 loss decrease、KL trust-region size、compute/memory；
6. 用 symmetry 构造 singular Fisher；
7. 给 failure assertions 与 approximation error；
8. 说明它与 constrained manifold optimization、ordinary preconditioning、mirror descent 的边界。
