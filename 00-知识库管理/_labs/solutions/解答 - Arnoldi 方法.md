---
type: solution
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[Arnoldi 方法]]"
exercise: "[[习题 - Arnoldi 方法]]"
prerequisites: ["[[Lanczos 方法]]", "[[Schur 分解]]"]
related: ["[[实验 - Arnoldi 非正规性、重正交与重启]]", "[[非正规矩阵]]"]
sources: ["[[S-2023-Demmel-Krylov-Arnoldi-Lanczos]]", "[[S-2000-Netlib-Krylov-Eigensolver-Templates]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - Arnoldi 方法

> [!warning] 使用边界
> 以下投影恒等式以精确正交为起点；涉及特征值前向误差时，必须显式考虑非正规性，不能把对称矩阵的 gap 结论原样搬来。

## A. 识别与复述

### NLA-ARN-A01

| 维度 | Arnoldi | Lanczos |
|---|---|---|
| 算子 | 一般方阵 | 对称/Hermitian |
| 小矩阵 | 上 Hessenberg $H_k$ | 对称三对角 $T_k$ |
| 递推 | 与全部旧基正交，长递推 | 理论三项递推 |
| 正交成本 | 累计 $O(nk^2)$ | 纯递推低，但稳健实现仍可能重正交 |
| 存储 | 通常 $O(nk)$ | 只求值可短存储；求向量/重正交仍常为 $O(nk)$ |
| 前向理论 | 受非正规性、左右向量与伪谱影响 | 可用实谱、交错、gap 与变分原理 |

Lanczos 是 Arnoldi 在自伴算子上的结构化特例，不是一个无条件更便宜的替代品。

### NLA-ARN-A02

$$
AQ_k=Q_{k+1}\bar H_k,
$$

其中 $Q_k\in\mathbb C^{n\times k}$、$Q_{k+1}\in\mathbb C^{n\times(k+1)}$、$\bar H_k\in\mathbb C^{(k+1)\times k}$。等价地，

$$
AQ_k=Q_kH_k+h_{k+1,k}q_{k+1}e_k^T,
$$

$H_k\in\mathbb C^{k\times k}$。第 $j$ 步的 $Aq_j$ 只由 $q_1,\ldots,q_{j+1}$ 表示，所以第 $j$ 列在 $j+1$ 行以下为零，即 $h_{ij}=0$ 对 $i>j+1$。

### NLA-ARN-A03

- 普通 Ritz：$H_k$ 的特征对，常优先外缘谱；
- Schur 向量：提升小 Schur 子空间，聚簇/非正规时比逐个特征向量稳定，也便于重排锁定；
- harmonic Ritz：改变 Petrov–Galerkin 测试空间，使内部/近移位目标更突出；
- shift-and-invert：改变算子谱，把近 $\sigma$ 的目标变成外部最大模，但引入线性求解；
- refined Ritz vector：固定近似值后，在当前子空间中最小化原问题残差，缓解病态小特征向量带来的方向质量问题。

## B. 手算与构造

### NLA-ARN-B01

第一步：

$$
Aq_1=\frac1{\sqrt2}(1,1,3)^T,\quad
h_{11}=2,\quad
w=\frac1{\sqrt2}(-1,1,1)^T.
$$

故

$$
h_{21}=\sqrt{3/2},\qquad q_2=\frac1{\sqrt3}(-1,1,1)^T.
$$

第二步：

$$
Aq_2=\frac1{\sqrt3}(0,3,3)^T,\quad
h_{12}=\sqrt{3/2},\quad h_{22}=2.
$$

两次投影后的余量为

$$
w=\frac1{\sqrt3}(1/2,1,-1/2)^T,
$$

所以

$$
h_{32}=1/\sqrt2,\qquad q_3=(1,2,-1)^T/\sqrt6.
$$

$$
\bar H_2=
\begin{bmatrix}
2&\sqrt{3/2}\\
\sqrt{3/2}&2\\
0&1/\sqrt2
\end{bmatrix}.
$$

### NLA-ARN-B02

$H_2$ 的特征值为

$$
\theta_{\pm}=2\pm\sqrt{3/2}\approx3.224745, 0.775255.
$$

$A$ 的谱是 $1,2,3$。对称 Rayleigh–Ritz 才有 Ritz 值位于谱区间及交错性质。一般矩阵的 Rayleigh 商位于数值域 $W(A)$，而非正规矩阵的数值域可以越出谱凸包；因此无矛盾。

### NLA-ARN-B03

$$
|e_k^Ty|=\sqrt{0.15^2+0.20^2}=0.25,
$$

所以

$$
\|r\|=0.02\times0.25=5\times10^{-3}.
$$

### NLA-ARN-B04

基存储为

$$
2\times10^5\times80\times8=1.28\times10^8\text{ bytes}
$$

约 $128$ MB（$122$ MiB）。第 80 步一次 MGS 对 80 个旧向量各做一次内积和一次 axpy，即约 160 次长度 $n$ 的向量遍历；若二次 MGS 约翻倍。在分布式环境，每批内积涉及全局归约，延迟/同步常比局部 FLOPs 更贵，故需要融合内积、块方法或通信规避设计。

### NLA-ARN-B05

模分别为

$$
|1+4i|=\sqrt{17}\approx4.123,\quad |2|=2,\quad|3-i|=\sqrt{10}\approx3.162.
$$

最大模排序：$1+4i,3-i,2$。实部分别为 $1,2,3$，最大实部排序：$3-i,2,1+4i$。连续时间 $e^{tA}$ 的渐近指数增长首先由最大实部决定；非正规暂态还需额外检查，不能只用这一标量。

### NLA-ARN-B06

写 $J=I+N$，$N^2=0$，故

$$
J^k=I+kN=
\begin{bmatrix}1&kM\\0&1\end{bmatrix}.
$$

所有特征值始终为 $1$，谱半径为 $1$；但 $J^ke_2=(kM,1)^T$，$M=100$ 时范数至少约 $100k$。谱只描述渐近指数率，Jordan/非正规结构产生多项式暂态。

## C. 推导与证明

### NLA-ARN-C01

第 $j$ 步开始 $w=Aq_j$，MGS 产生

$$
w_{\rm final}=Aq_j-\sum_{i=1}^jq_ih_{ij}.
$$

归一化给 $w_{\rm final}=q_{j+1}h_{j+1,j}$，故

$$
Aq_j=\sum_{i=1}^{j+1}q_ih_{ij}.
$$

把 $j=1,\ldots,k$ 拼接即得 $AQ_k=Q_{k+1}\bar H_k$。因第 $j$ 列根本不含 $q_{j+2},q_{j+3},\ldots$，所以对应系数 $h_{ij}=0$ 对 $i>j+1$。

### NLA-ARN-C02

对 $H_ky=\theta y$、$x=Q_ky$：

$$
r=AQ_ky-\theta Q_ky
=Q_k(H_ky-\theta y)+h_{k+1,k}q_{k+1}e_k^Ty
=h_{k+1,k}q_{k+1}e_k^Ty.
$$

因 $\|q_{k+1}\|=1$，

$$
\|r\|=|h_{k+1,k}e_k^Ty|.
$$

又因 $Q_k^*q_{k+1}=0$，有 $Q_k^*r=0$，即 Galerkin 条件。

### NLA-ARN-C03

若 $h_{j+1,j}=0$，Arnoldi 分解退化为

$$
AQ_j=Q_jH_j.
$$

任取 $x\in\mathcal K_j=\mathcal R(Q_j)$，写 $x=Q_jy$，则

$$
Ax=AQ_jy=Q_jH_jy\in\mathcal R(Q_j).
$$

所以 $A\mathcal K_j\subseteq\mathcal K_j$。

### NLA-ARN-C04

多项式 $p(t)=\sum_{j=0}^dc_jt^j$。由 $A^j=V\Lambda^jV^{-1}$，

$$
p(A)=\sum_jc_jV\Lambda^jV^{-1}=Vp(\Lambda)V^{-1}.
$$

因此

$$
\|p(A)\|\le\|V\|\|V^{-1}\|\max_i|p(\lambda_i)|
=\kappa(V)\max_i|p(\lambda_i)|.
$$

当 $V$ 病态，即使多项式在所有非目标谱点很小，算子作用仍可被 $\kappa(V)$ 放大；近缺陷矩阵还需伪谱/数值域分析。

### NLA-ARN-C05

令 $r_0=b-Ax_0=\beta q_1$、$x_k=x_0+Q_ky$。则

$$
\begin{aligned}
r_k&=r_0-AQ_ky\\
&=Q_{k+1}\beta e_1-Q_{k+1}\bar H_ky\\
&=Q_{k+1}(\beta e_1-\bar H_ky).
\end{aligned}
$$

因 $Q_{k+1}$ 列正交，保持二范数，故

$$
\min_{x_k\in x_0+\mathcal K_k}\|r_k\|
=\min_y\|\beta e_1-\bar H_ky\|.
$$

### NLA-ARN-C06

对任何次数不超过 $k-1$ 的多项式 $p$，Krylov 投影在相应可达空间中给出

$$
p(A)q_1=Q_kp(H_k)e_1
$$

（在无提前 breakdown、并按次数解释时）。用多项式 $p$ 在相关谱/数值域上逼近 $f$，得到

$$
f(A)b=\|b\|f(A)q_1
\approx\|b\|Q_kf(H_k)e_1.
$$

$b=\|b\|q_1$、Arnoldi 分解和低次多项式传递是代数结构；用有限维 $k$ 代替一般 $f$ 是截断/逼近步骤，其误差受函数、区域、非正规性与 $k$ 影响。

## D. 边界、反例与纠错

### NLA-ARN-D01

可取上移位矩阵

$$
A=\begin{bmatrix}0&1&0\\0&0&1\\0&0&0\end{bmatrix}
$$

并选一般起点，例如 $(1,1,1)^T/\sqrt3$。投影系数 $q_i^TAq_j$ 没有对称关系，$H_k$ 的多个远上三角元一般非零。若只减去最近两个方向，余量仍含更早基向量，$Q^*Q=I$ 和 $H=Q^*AQ$ 都被破坏，廉价残差也失去依据。

### NLA-ARN-D02

残差 $10^{-10}$ 表示 $(\theta,x)$ 是某个邻近矩阵的精确特征对，属于后向陈述。对 $A=V\Lambda V^{-1}$，特征值前向误差可被 $\kappa(V)$ 放大；简单特征值的左右向量若满足 $|z^*x|\ll1$，条件数很大。

应补充算子尺度化残差、左 Ritz 向量/左右夹角、Schur 子空间残差、伪谱或随机扰动稳定性；只有在良好分离与良态条件下才能把残差转成位数声明。

### NLA-ARN-D03

CGS 一次性用原始向量计算全部投影，再统一相减；MGS 每减一个方向就更新余量，后续内积使用更新值。实数代数中二者等价，浮点舍入路径不同；当列近相关，CGS 一次通常损失更多正交性。二次 MGS 再投影一次，可把残留旧分量压回舍入尺度，但代价和同步约翻倍。正确选择依赖 $\|Q^*Q-I\|$ 验收，不依赖“公式看起来一样”。

### NLA-ARN-D04

随机换起点会丢掉已构造的谱滤波多项式并可能重复学习。重启至少应保留：

1. 已收敛 Schur/Ritz 子空间并锁定；
2. 未收敛但最接近目标的若干方向（厚重启）；
3. 目标选择信息，如隐式 QR 移位形成的过滤多项式；
4. 内部目标时的 harmonic/refined 提取信息。

### NLA-ARN-D05

谱半径 $\rho(J)<1$ 只控制固定矩阵 $J^k$ 的渐近指数率。非正规 $J$ 可有很大的 $\|J^k\|_2$ 暂态；单步最坏放大由 $\sigma_{\max}(J)$ 衡量，多步则需 $\sigma_{\max}(J^k)$ 或 resolvent/伪谱。循环网络还存在时变 Jacobian 乘积，单一平均谱半径更不足。应同时监控奇异值、乘积范数与实际梯度传播。

## E. AI 迁移

### NLA-ARN-E01

实现算子 $v\mapsto Jv$ 的确定性 JVP；Arnoldi 小矩阵用 `real_part` 排序而非模排序，重启保留最大实部 Schur block。停止报告直接尺度化残差 $\|Jx-\theta x\|/(\widehat{\|J\|}+|\theta|)$、正交缺陷和多起点稳定性。

因为只有 JVP，不能直接计算左向量条件数；至少对参数/批次/JVP 容差做小扰动，观察 Ritz 点和 Schur 子空间是否稳定，并明确这是局部固定状态的线性化。若目标出现复共轭对，实数实现应锁定二维实 Schur block。

### NLA-ARN-E02

JVP 给 $Jv$，VJP 给 $J^*z$。分别运行右 Arnoldi 与左 Arnoldi，在匹配的简单特征值处归一化 $\|x\|=\|z\|=1$。简单特征值条件数近似

$$
\kappa(\lambda)=\frac1{|z^*x|}.
$$

同时检查右残差 $\|Jx-\lambda x\|$ 和左残差 $\|J^*z-\bar\lambda z\|$。小 $|z^*x|$ 会把微小算子/采样误差放大，这比仅有右残差更能判断前向可信度。

### NLA-ARN-E03

在一步长度 $\Delta t$ 上计算

$$
e^{\Delta tJ}v\approx\|v\|Q_m e^{\Delta tH_m}e_1.
$$

可用扩展一维后的尾项、相邻 $m$ 结果差或残差型估计作误差代理。若 $m$ 达内存上限仍失败，缩短 $\Delta t$ 并分步；若矩阵作用昂贵而正交便宜，可先增加 $m$。自适应应联合选择 $(m,\Delta t)$，并累计全局误差，不应只固定一个旋钮。

### NLA-ARN-E04

- 最大模特征值：固定离散线性迭代的渐近增长/衰减；
- 最大实部特征值：连续流 $e^{tA}$ 的渐近指数率；
- 最大奇异值：单步最坏欧氏范数放大，与方向无关且适用于非正规算子。

离散长期主看谱半径，连续长期主看谱横坐标；两者若关心有限时鲁棒性，必须补充 $\|A^k\|$、$\|e^{tA}\|$ 或奇异值/伪谱。

### NLA-ARN-E05

排查顺序：先在留出数据上重建算子/评估模态，排除过拟合；用原算子残差排除仅在小投影里成立的点；改变 $m$、重启策略和起点，观察 Ritz/Schur 子空间稳定性；对样本 bootstrap 得到统计波动；对聚簇点比较有序 Schur 子空间而非逐向量；最后用 resolvent/伪谱或小扰动测试区分真实敏感谱与数值假象。只有同时跨数据、算法与扰动稳定的结构才宜解释为动力学模态。

## 验收清单

- [x] 25 题逐题解答；
- [x] 手算含完整 $\bar H_2$；
- [x] 推导覆盖 Ritz、GMRES 与矩阵函数；
- [x] 反例覆盖非正规、正交化、重启和暂态；
- [x] AI 迁移明确区分模、实部和奇异值目标。
