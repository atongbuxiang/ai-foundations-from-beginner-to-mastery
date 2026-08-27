---
type: derivation
status: verified
area: [training, optimization, automatic-differentiation, krylov]
node_id: TRN-19
aliases: [HVP 与 CG, Hessian-free 二阶步]
prerequisites: ["[[共轭梯度法]]", "[[Gradient Checking、Checkpointing 与高阶微分边界]]", "[[Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"]
related: ["[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[K-FAC、Kronecker 分块与阻尼合同]]", "[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]"]
sources: ["[[S-1994-Pearlmutter-Fast-Exact-HVP]]", "[[S-1983-Steihaug-Trust-Region-CG]]", "[[S-2026-PyTorch-Higher-Order-AD]]", "[[S-2006-Nocedal-Wright-Numerical-Optimization]]"]
exercises: ["[[习题 - Hessian-vector Product、共轭梯度与隐式二阶步]]"]
solutions: ["[[解答 - Hessian-vector Product、共轭梯度与隐式二阶步]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-hvp-cg-residual-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Hessian-vector Product、共轭梯度与隐式二阶步

> [!abstract] 一句话结论
> 二阶方向通常不需要显式保存 $P\times P$ Hessian：只要能计算线性算子 $v\mapsto(B+\lambda I)v$，Krylov 方法就能近似解线性系统。真正的验收对象不是“跑了几轮 CG”，而是 residual、curvature、boundary、预条件器和 HVP 的数值一致性。

## 一、为什么 full Hessian 不可行

$P$ 个参数的 dense Hessian 有 $P^2$ 元素。若 $P=10^9$，即使每项 2 bytes 也需 $2\times10^{18}$ bytes，远超训练系统；形成它还要大量二阶导计算。

但 Newton/CG 每步只需要 $Hv$。Hessian-vector product 是 gradient 的方向导数：

$$
Hv=\left.\frac{d}{d\epsilon}\nabla L(\theta+\epsilon v)\right|_{\epsilon=0}.
$$

Pearlmutter 的 $R$-operator 与现代 forward-over-reverse AD 都直接利用这条身份，不物化 $H$。

> [!warning] “Exact HVP”的准确含义
> Exact 指对给定计算图应用链式法则，而不是 finite difference；它仍受浮点舍入、非光滑算子、随机状态、低精度 kernel 和框架高阶导覆盖影响。

## 二、三种 HVP 路径

### 2.1 Forward-over-reverse

先用 reverse mode 得 $g(\theta)$，再对 gradient 做 JVP：

$$
\operatorname{JVP}(\nabla L,\theta;v)=Hv.
$$

内存通常较好，但需要 forward-mode operator coverage。

### 2.2 Reverse-over-reverse

先算标量 $g^Tv$，再对参数求 gradient：

$$
\nabla_\theta(g(\theta)^Tv)=H^Tv=Hv
$$

（光滑标量 loss 下 $H$ 对称）。它覆盖面常更广，但需构建高阶反向图。

### 2.3 Finite difference 只作诊断

$$
Hv\approx\frac{g(\theta+hv)-g(\theta)}h.
$$

截断误差随 $h$ 降低，舍入/相消误差却随 $h$ 过小增大。它适合小模型交叉检查，不应作为生产 HVP 的默认实现。

## 三、用 CG 解 damped Newton system

目标是

$$
Ap=b,\qquad A=B+\lambda I\succ0,\qquad b=-g.
$$

从 $p_0$ 开始，residual $r_0=b-Ap_0$，direction $d_0=r_0$。标准 CG：

$$
\alpha_k=\frac{r_k^Tr_k}{d_k^TAd_k},\quad
p_{k+1}=p_k+\alpha_kd_k,
$$

$$
r_{k+1}=r_k-\alpha_kAd_k,\quad
\beta_{k+1}=\frac{r_{k+1}^Tr_{k+1}}{r_k^Tr_k},\quad
d_{k+1}=r_{k+1}+\beta_{k+1}d_k.
$$

精确算术下，CG 在 Krylov subspace

$$
\mathcal K_k(A,r_0)=\operatorname{span}\{r_0,Ar_0,\ldots,A^{k-1}r_0\}
$$

中最小化 $A$-norm error/对应 quadratic；有限精度会丢 conjugacy。

## 四、Residual 不等于 solution error

若 $p^*=A^{-1}b$，则

$$
p_k-p^*=-A^{-1}r_k.
$$

因此

$$
\|p_k-p^*\|\le\|A^{-1}\|\,\|r_k\|.
$$

当 $A$ 病态，small residual 仍可对应较大 solution error；反之对训练 direction 可能只需 quadratic decrease 足够，不必高精度解。停止门至少同时看 relative residual、model decrease、iteration/HVP budget 与 trust-region boundary。

经典 SPD bound 为

$$
\frac{\|e_k\|_A}{\|e_0\|_A}
\le2\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^k,
$$

但实际收敛还受 eigenvalue clustering，不能只用 $\kappa$ 预测每一步。

## 五、Preconditioned CG

若 $M\approx A$ 且易解，使用 $z_k=M^{-1}r_k$ 改善谱。验收不能只报告 CG iterations，因为 preconditioner build/apply 也有成本：

$$
\text{total time}
=\text{statistics/build}
+k(\text{HVP} + \text{preconditioner apply} + \text{reductions}).
$$

对分布式训练，每轮 CG 的 dot products 可能触发 global reduction，通信 latency 会压过 FLOPs。

## 六、不定 Hessian 与 Steihaug CG

若 $B$ 不定，可能出现

$$
d_k^TBd_k\le0.
$$

标准 CG 的 SPD 解释失效。Trust-region Steihaug 法在这种情况下沿 $d_k$ 走到 $\|p\|=\Delta$；若正常一步会越界，也求与球面的交点后停止。三个出口必须独立记录：

1. residual 达标；
2. negative curvature；
3. boundary hit。

把负曲率简单当“数值错误”会删除非凸结构；无界地沿负曲率走又会离开可信局部模型。

## 七、HVP 的最小一致性测试

### 7.1 Bilinear symmetry

随机 $u,v$ 检查

$$
u^T(Hv)\approx v^T(Hu).
$$

它能发现 graph detach、随机 batch/state 不一致和 transpose convention 错误。

### 7.2 Directional finite difference

扫一组 $h$，观察

$$
\frac{\|Hv-[g(\theta+hv)-g(\theta)]/h\|}{\|Hv\|+\delta}
$$

先下降后上升的 U-shaped 区间。只用一个 $h$ 可能偶然通过。

### 7.3 Quadratic exact case

$L=\tfrac12\theta^TA\theta-b^T\theta$ 时 HVP 必须精确等于 $Av$；CG residual 可与直接小矩阵解对齐。

## 八、随机训练状态必须冻结

在一次 Krylov solve 内，如果每个 HVP 换 batch、dropout mask、BatchNorm statistics 或 augmentation，算子从 $A$ 变成 $A_k$，Krylov subspace 与 conjugacy 不再对应同一系统。可选择 stochastic curvature 方法，但必须明确那是另一个算法，而不是“带噪 CG 仍精确解同一方程”。

当前 PyTorch 可用 `jvp(grad(f))` 表达 forward-over-reverse HVP；forward AD coverage 不足时可用 `vjp`/reverse-over-reverse。模型需通过 functional parameters/buffers 显式化，避免 module mutation 和隐藏 RNG。

## 九、图：从 HVP oracle 到可验收二阶步

先看图回答：每轮 CG 依赖的算子状态必须冻结哪些量？停止时留下哪种证书？

![[00-知识库管理/_assets/figures/training-optimization/fig-hvp-cg-residual-contract-v1.svg|900]]

> [!figure] 图 TRN-19　HVP、Krylov 子空间、CG residual 与三出口
> 左侧展示 forward-over-reverse/reverse-over-reverse；中间是固定线性算子的 Krylov 递推；右侧区分 residual、negative curvature 和 boundary hit，并补上 build/HVP/reduction 成本账。来源：依据 [[S-1994-Pearlmutter-Fast-Exact-HVP]]、[[S-1983-Steihaug-Trust-Region-CG]] 与 [[S-2026-PyTorch-Higher-Order-AD]] 独立绘制。

**怎样读图**：先验 HVP oracle，再看 solver；若算子每轮漂移，后面的 residual 和 conjugacy 证书都失去原定义。

**图没有证明什么**：图不保证 HVP 比一阶 optimizer 更快，也没有给出所有硬件/模型上的最佳 CG tolerance。

## 十、练习与独立解答

- [[习题 - Hessian-vector Product、共轭梯度与隐式二阶步]]
- [[解答 - Hessian-vector Product、共轭梯度与隐式二阶步]]
