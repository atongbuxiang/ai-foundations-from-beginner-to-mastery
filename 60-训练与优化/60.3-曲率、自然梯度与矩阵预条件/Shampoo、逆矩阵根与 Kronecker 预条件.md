---
type: derivation
status: verified
area: [training, optimization, shampoo, matrix-functions]
node_id: TRN-23
aliases: [Shampoo Optimizer, Tensor Preconditioning]
prerequisites: ["[[矩阵函数与矩阵指数]]", "[[Kronecker 积、向量化与矩阵方程]]", "[[AdaGrad、累计平方梯度与稀疏几何]]"]
related: ["[[SOAP、二阶混合优化器与成本证据地图]]", "[[K-FAC、Kronecker 分块与阻尼合同]]", "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
sources: ["[[S-2018-Gupta-Shampoo]]", "[[S-2020-Anil-Scalable-Shampoo]]", "[[S-2006-Guo-Higham-Matrix-Inverse-Root]]"]
exercises: ["[[习题 - Shampoo、逆矩阵根与 Kronecker 预条件]]"]
solutions: ["[[解答 - Shampoo、逆矩阵根与 Kronecker 预条件]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-shampoo-mode-root-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Shampoo、逆矩阵根与 Kronecker 预条件

> [!abstract] 一句话结论
> Shampoo 把参数张量的每个 mode 当作一个结构轴，为该轴累计 gradient Gram matrix，再用多侧 inverse roots 预条件更新。算法价值来自保留非对角相关性；算法风险也来自这里：矩阵根的定义、damping、block size、root refresh、grafting、精度和通信都比逐元素 Adam 更重。

## 一、从 full-matrix AdaGrad 到 tensor structure

把 $P$ 个参数拉平后，full-matrix AdaGrad 会累计

$$
H_t=\epsilon I_P+\sum_{s\le t}g_sg_s^T
$$

并使用 $H_t^{-1/2}g_t$。它保留全部坐标相关性，但需 $P^2$ 状态和昂贵 inverse square root。

若参数本来是张量 $W\in\mathbb R^{d_1\times\cdots\times d_k}$，Shampoo 为每个 mode 建一个 $d_i\times d_i$ 统计量，状态从 $(\prod_id_i)^2$ 降至

$$
\sum_{i=1}^k d_i^2.
$$

这仍可能很大，却保留了张量轴的非对角结构。

## 二、Mode-wise Gram statistics

令 $G_t^{(i)}$ 是 gradient 沿第 $i$ 个 mode 展开的 matricization，shape 为 $d_i\times(P/d_i)$。累计

$$
L_t^{(i)}=\epsilon I_{d_i}+\sum_{s\le t}
G_s^{(i)}G_s^{(i)T}.
$$

对 order-$k$ tensor，经典 Shampoo 用每个 mode 的 inverse $2k$-th root：

$$
\widetilde G_t
=G_t\times_1 L_t^{(1)-1/(2k)}
\times_2\cdots
\times_k L_t^{(k)-1/(2k)}.
$$

矩阵是 $k=2$，所以左右各用 inverse fourth root：

$$
\widetilde G=L^{-1/4}GR^{-1/4}.
$$

两个 fourth-root factors 合成整体 half-power 的结构化近似；把每侧误写成 inverse square root 会过度预条件。

## 三、矩阵例子的逐项手算

设

$$
L=\operatorname{diag}(16,1),\qquad
R=\operatorname{diag}(1,81),\qquad
G=\begin{pmatrix}1&1\\1&1\end{pmatrix}.
$$

则

$$
L^{-1/4}=\operatorname{diag}(1/2,1),\qquad
R^{-1/4}=\operatorname{diag}(1,1/3),
$$

所以

$$
\widetilde G
=\begin{pmatrix}1/2&1/6\\1&1/3\end{pmatrix}.
$$

左 factor 缩放 row-space，右 factor 缩放 column-space；结果通常不与原 gradient 共线。

## 四、Principal inverse root 与 damping

对 SPD $A=Q\operatorname{diag}(\lambda_i)Q^T$，principal inverse root 定义为

$$
A^{-1/p}=Q\operatorname{diag}(\lambda_i^{-1/p})Q^T.
$$

若 $\lambda_i\to0$，增益爆炸。通常先形成 $A+\epsilon I$ 或做 eigenvalue floor。这里的 $\epsilon$ 单位与 Gram eigenvalue 相同，并会改变 root residual 与有效 update；不能从 Adam epsilon 直接复制数值。

### 4.1 数值证书

若 $X\approx A^{-1/p}$，可检查：

$$
r_{inv}=\frac{\|X^pA-I\|}{\|I\|},\qquad
r_{comm}=\frac{\|XA-AX\|}{\|A\|\|X\|}.
$$

还要监控 symmetry、finite values、eigenvalue floor 和 update norm。只报告迭代次数不是精度证书。

## 五、Eigendecomposition 与 iterative root

### 5.1 EVD

对对称 block 做 $A=Q\Lambda Q^T$ 后逐 eigenvalue 取根，易理解且可给 residual；成本约 cubic in block dimension，低精度 eigensolver/重复 eigenvalues 需审计。

### 5.2 Newton/Schur/coupled iterations

某些 root/inverse-root 迭代主要用 matrix multiplication，适合 accelerator，但 [[S-2006-Guo-Higham-Matrix-Inverse-Root]] 强调 basic Newton iteration 可数值不稳定；初始 scaling、谱收敛域与 coupled stabilization 是算法的一部分。

因此“GEMM-only”不等于“自动稳定”，也不表示比 EVD 总时间更低。

## 六、三个时钟与 amortized cost

Scalable Shampoo 常拆为：

1. 每步更新 Gram/EMA；
2. 每 $K$ 步重算 inverse roots；
3. 每步用最近 roots 预条件 gradient。

平均单步成本应写

$$
C_{avg}=C_{stats}+C_{apply}+\frac1K C_{root}+C_{comm}.
$$

增大 $K$ 降低 root cost，却增加 basis/root staleness。应同时报告 time-to-quality，而非只比较 optimizer step 数。

## 七、Block size、grafting 与 fallback

- **Block size**：大轴切成 blocks 限制 $d_i^2/d_i^3$ 成本，也删除跨 block correlation；
- **Grafting**：用 SGD/Adam/AdaGrad 的 update norm 调整 Shampoo direction 长度，改变的是 magnitude contract，不应隐藏；
- **Fallback**：vector/scalar/sparse 参数可能用 diagonal optimizer；
- **Momentum/decay**：在 raw gradient、preconditioned direction 或 parameter delta 的哪个位置应用必须声明；
- **Precision**：statistics、root compute、root storage、apply 与 communication 可用不同 dtype。

## 八、Shampoo 是否“近似 Hessian”

原始 Shampoo 更直接属于结构化 adaptive-gradient/full-matrix AdaGrad 家族，statistics 是 gradient Gram。某些模型与假设下可从 Gauss–Newton/gradient whitening 解释它的 preconditioner，但这不是 exact Hessian identity。必须保留：data trajectory、non-central moment、Kronecker/tensor approximation、root exponent 和 damping。

## 九、图：每个 tensor mode 的统计—根—应用流水线

先看图回答：矩阵为何每侧是 fourth root？root refresh 变慢后哪部分 state 仍每步更新？

![[00-知识库管理/_assets/figures/training-optimization/fig-shampoo-mode-root-ledger-v1.svg|900]]

> [!figure] 图 TRN-23　Shampoo mode Gram、inverse root 与系统时钟
> 左侧将 tensor gradient 展开成各 mode Gram；中间展示 $-1/(2k)$ roots 与 mode products；右侧分开 statistics、root refresh、apply、grafting 和 distributed cost。来源：依据 [[S-2018-Gupta-Shampoo]]、[[S-2020-Anil-Scalable-Shampoo]] 与 [[S-2006-Guo-Higham-Matrix-Inverse-Root]] 独立绘制。

**怎样读图**：沿单个 mode 追踪 shape 与单位，再把多个 mode 的作用组合；不要从最终 update 反推每侧都用了同一 familiar square root。

**图没有证明什么**：图不证明 Shampoo 恢复真实 Hessian，也不保证 root 低频更新在任意非平稳训练中无损。

## 十、验收字段

逐参数记录 order/shape、block partition、Gram reduction、statistics decay、root exponent、damping/floor、root solver/tolerance/precision、refresh period、grafting、momentum/decay order、fallback、state bytes、root/apply/communication time 和失败 artifacts。

## 练习与独立解答

- [[习题 - Shampoo、逆矩阵根与 Kronecker 预条件]]
- [[解答 - Shampoo、逆矩阵根与 Kronecker 预条件]]
