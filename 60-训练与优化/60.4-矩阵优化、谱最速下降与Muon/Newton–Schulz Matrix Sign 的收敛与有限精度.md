---
type: derivation
status: verified
area: [training, optimization, numerical-linear-algebra, muon]
node_id: TRN-28
aliases: [Muon Newton Schulz 数值审计, Matrix Sign Iteration]
prerequisites: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[浮点数与舍入误差]]"]
related: ["[[Muon 的动量、正交化与参数分组合同]]", "[[SVD 算法与谱范数估计]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
sources: ["[[S-2025-Su-10922-msign-Newton-Schulz]]", "[[S-1986-Higham-Polar-Decomposition]]", "[[S-2012-Nakatsukasa-Higham-Polar-Stability]]", "[[S-2024-Jordan-Muon]]", "[[S-2026-PyTorch-Muon]]"]
exercises: ["[[习题 - Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
solutions: ["[[解答 - Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-newton-schulz-singular-map-audit-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Newton–Schulz Matrix Sign 的收敛与有限精度

> [!abstract] 一句话结论
> Newton–Schulz 型正交化的核心不是神秘矩阵操作，而是对每个奇异值反复应用一个标量奇多项式。精确 polar、经典收敛迭代与 Muon 的固定五步经验多项式是三种对象；必须用收敛域、残差、rank 与浮点格式共同审计。

## 一、为什么矩阵迭代可以降成标量图

设

$$
X_0=U\Sigma_0V^T,
$$

并考虑

$$
X_{k+1}
=aX_k+bX_kX_k^TX_k+cX_kX_k^TX_kX_k^TX_k.
\tag{1}
$$

因为

$$
X_kX_k^TX_k
=U\Sigma_k^3V^T,
$$

五次项同理，所以左右奇异向量保持不变，而每个奇异值独立演化：

$$
s_{k+1}=\phi(s_k)
=as_k+bs_k^3+cs_k^5.
\tag{2}
$$

于是矩阵问题的第一张诊断图就是 $\phi(s)$ 与直线 $s$ 的关系。

> [!important] 这是 exact-arithmetic 结构
> 浮点矩阵乘会扰动奇异向量与奇异值；当奇异值聚集、矩阵病态或低精度乘法误差大时，不能把式 (2) 当作逐元素完全独立的实际轨迹。

## 二、经典 polar Newton–Schulz 与局部收敛

经典迭代的一种形式为

$$
X_{k+1}
=\frac12X_k(3I-X_k^TX_k),
\tag{3}
$$

对应标量映射

$$
\phi_{NS}(s)=\frac12s(3-s^2).
\tag{4}
$$

令误差写成

$$
e_k=1-s_k^2.
$$

由 (4) 可算得

$$
e_{k+1}
=1-\frac14s_k^2(3-s_k^2)^2
=\frac14e_k^2(3+e_k).
\tag{5}
$$

当 $|e_k|<1$ 时，误差呈二次收缩的局部行为。常见做法先缩放 $X_0=\alpha G$，使所有非零奇异值进入安全区间。

但注意：

- $s=0$ 是固定点，rank deficiency 不会被多项式凭空修复；
- 初值过大可越出 attraction region；
- “二次收敛”描述靠近 fixed point 的渐近阶段，不等于任意初值五步足够；
- 矩形矩阵应使用与 shape 相容的 Gram 乘法顺序。

## 三、Muon 的 Jordan 系数解决的是有限步近似

Muon 常用

$$
(a,b,c)=(3.4445,-4.7750,2.0315)
\tag{6}
$$

并做约五步迭代。相应

$$
\phi_J(s)
=3.4445s-4.7750s^3+2.0315s^5.
\tag{7}
$$

这组系数为有限步、低精度、训练吞吐目标设计；它不等同于经典式 (4)，也不要求每一步把每个 $s$ 单调推近 1。正确的问题不是“跑了五步吗”，而是：

1. 初始奇异值落在哪个区间？
2. 五步后的 $\phi_J^{\circ5}(s)$ 在该区间误差多大？
3. 是否出现 overshoot、oscillation 或 dynamic-range 风险？
4. 在实际 dtype/GEMM 上残差与 exact polar 相差多少？

## 四、初始化缩放是收敛合同的一部分

常见参考实现用

$$
X_0=\frac{G}{\lVert G\rVert_F+\varepsilon}.
\tag{8}
$$

因为 $\lVert G\rVert_2\le\lVert G\rVert_F$，故 $\lVert X_0\rVert_2\le1$。优点是计算便宜、给出保守上界；代价是当 rank 高且谱较平坦时，所有奇异值约为 $1/\sqrt r$，离 1 较远。

也可用谱范数估计做

$$
X_0=\frac{G}{\widehat{\lVert G\rVert_2}},
\tag{9}
$$

但若估计低于真实谱范数，最大奇异值可能超过设计区间。power iteration 的未收敛输出通常不是严格上界，不能不加 guard 就当 certificate。

## 五、四类残差必须分开

设 exact compact polar factor $Q=U_rV_r^T$，approximation 为 $\widehat Q$。

### 5.1 正交残差

列满秩且 $m\ge n$ 时：

$$
r_{orth}
=\frac{\lVert\widehat Q^T\widehat Q-I\rVert_F}{\sqrt n}.
\tag{10}
$$

若矩阵为宽矩阵，则改审计 $\widehat Q\widehat Q^T-I$。rank-deficient 时目标应是 support projector，而不是完整 identity。

### 5.2 polar residual

$$
r_{polar}
=\frac{\lVert G-\widehat Q(\widehat Q^TG)\rVert_F}
{\lVert G\rVert_F}.
\tag{11}
$$

还需检查 $\widehat Q^TG$ 是否近似 symmetric PSD。仅正交不保证方向与 $G$ 对齐。

### 5.3 direction cosine

$$
\cos_F(\widehat Q,Q)
=\frac{\langle\widehat Q,Q\rangle_F}
{\lVert\widehat Q\rVert_F\lVert Q\rVert_F}.
\tag{12}
$$

它检查方向，但可能掩盖 scale error。

### 5.4 谱最速下降缺口

$$
\delta_{dual}
=1-\frac{\langle G,\widehat Q\rangle_F}
{\lVert G\rVert_*\,\max(1,\lVert\widehat Q\rVert_2)}.
\tag{13}
$$

该量直接测量 approximate direction 离对偶极值还有多远。

## 六、rank、condition number 与零奇异值

若

$$
G=U\operatorname{diag}(10^{-8},1)V^T,
$$

Frobenius 归一化后小奇异值仍约 $10^{-8}$。即使标量映射在零附近斜率 $a>1$，有限步后也可能远小于 1。精确 polar 会把所有正奇异值变成 1，但有限步算法的有效数值 rank 取决于：

- 初始最小非零奇异值；
- 迭代步数；
- dtype 的 unit roundoff 和 underflow；
- GEMM accumulation precision；
- 是否有显式截断或 regularization。

所以病态矩阵上“正交化”可能只正交化可解析的高能子空间。

## 七、低精度为什么需要单独实验

矩阵迭代每步包含多次 GEMM，误差会以 backward/forward error 的方式传播。条件稳定的数学迭代不表示任意低精度实现稳定。应至少比较：

| 维度 | 审计项 |
|---|---|
| dtype | BF16/FP16/TF32/FP32 输入、乘法、累积分别是什么 |
| scaling | Frobenius、spectral estimate、额外 $\varepsilon$ |
| spectrum | flat、geometric decay、rank-deficient、clustered |
| steps | 0 到 $K$ 的残差轨迹，而非只看终点 |
| reference | FP64 SVD/polar 或高精度基准 |
| failure | NaN/Inf、残差反弹、direction cosine 下降 |

[[S-2012-Nakatsukasa-Higham-Polar-Stability]] 提醒我们：Newton–Schulz 类方法的稳定性是有条件的，不能只凭 exact-arithmetic fixed point 下结论。

## 八、计算成本：选择较小 Gram 矩阵

对 $X\in\mathbb R^{m\times n}$：

- 若 $m\ge n$，优先形成 $X^TX\in\mathbb R^{n\times n}$；
- 若 $m<n$，可形成 $XX^T\in\mathbb R^{m\times m}$。

这改变 FLOPs 和临时显存，但在精确算术下相应 polynomial 可代数等价。实际 kernel layout、transpose、sharding 和 accumulation 仍可能使速度与误差不同。

## 九、图：一张图同时看 scalar map、残差和浮点护栏

先看图回答：为什么相同的五步迭代，在 flat、病态与 rank-deficient spectrum 上可能得到完全不同的有效正交化质量？

![[00-知识库管理/_assets/figures/training-optimization/fig-newton-schulz-singular-map-audit-v1.svg|900]]

> [!figure] 图 TRN-28　Newton–Schulz 奇异值映射与三层数值审计
> 左侧对比经典映射与 Muon 五次多项式，中间显示矩阵迭代保持奇异向量的 exact-arithmetic 机制，右侧列出正交、polar、方向和 dual-gap 残差。来源：依据 [[S-1986-Higham-Polar-Decomposition]]、[[S-2012-Nakatsukasa-Higham-Polar-Stability]]、[[S-2025-Su-10922-msign-Newton-Schulz]] 独立绘制。

**怎样读图**：先在左图定位初始 $s$，沿映射迭代；再到右栏检查实际矩阵输出是否同时满足四种残差。

**图没有证明什么**：曲线是 exact scalar polynomial 的示意，不代表 BF16 大矩阵的真实误差，也不证明五步对所有 spectrum 足够。

## 十、本节出口

你应能从矩阵多项式推导标量 singular-value map，证明经典局部误差递推，设计包含 rank/condition/dtype 的残差实验，并明确 finite-step NS output 与 exact polar factor 的差别。

## 练习与独立解答

- [[习题 - Newton–Schulz Matrix Sign 的收敛与有限精度]]
- [[解答 - Newton–Schulz Matrix Sign 的收敛与有限精度]]
