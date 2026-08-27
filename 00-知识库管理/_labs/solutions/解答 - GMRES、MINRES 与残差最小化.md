---
type: solution
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[GMRES、MINRES 与残差最小化]]"
exercise: "[[习题 - GMRES、MINRES 与残差最小化]]"
prerequisites: ["[[Arnoldi 方法]]", "[[Lanczos 方法]]"]
related: ["[[实验 - GMRES 重启、MINRES 结构与残差最小化]]", "[[稀疏矩阵计算与存储复杂度]]"]
sources: ["[[S-1986-Saad-Schultz-GMRES]]", "[[S-2011-Choi-Paige-Saunders-MINRESQLP]]", "[[S-1994-Barrett-线性系统迭代模板]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - GMRES、MINRES 与残差最小化

> [!warning] 前提纪律
> 以下精确正交、单调与有限终止先在精确算术中成立；有限精度题必须额外检查真残差和结构。

## A. 识别与复述

### NLA-MR-A01

| 方法 | $A$ | 最优量 | 基过程 | 存储 |
|---|---|---|---|---|
| CG | SPD | $A$-能量误差 | Lanczos | 常数向量 |
| MINRES | 对称/Hermitian，可不定 | $\|r_k\|_2$ | Lanczos | 常数向量 |
| GMRES | 一般方阵 | $\|r_k\|_2$ | Arnoldi | 随 $k$ 增长 |

CG 与 MINRES 有短递推源于对称性；一般 GMRES 必须与所有旧基正交。

### NLA-MR-A02

搜索空间是 $x_0+\mathcal K_k(A,r_0)$。最小化 $\|r_0-As\|_2$ 的一阶条件是

$$
r_k\perp A\mathcal K_k.
$$

FOM 要求 $r_k\perp\mathcal K_k$；两者测试空间不同。

### NLA-MR-A03

- happy breakdown：新 Arnoldi/Lanczos 向量范数为零且当前空间已给出精确解；
- 数值 breakdown：分母或正交化因舍入、错误结构或近线性相关而不可可靠继续；
- 停滞：未达容差但残差长期无显著下降；
- 达到容差：指定监控量通过阈值，仍需最终真残差验收。

### NLA-MR-A04

建议列：$m$、cycle、累计 matvec、累计预条件应用、真相对残差、内部残差、基向量峰值、正交内积或归约、墙钟、setup、退出原因。比较时固定问题、容差、硬件和真残差定义。

### NLA-MR-A05

右预条件写成

$$
AM^{-1}z=r_0,\qquad x=x_0+M^{-1}z.
$$

若 $z_k$ 最小化

$$
\|r_0-AM^{-1}z\|_2,
$$

该量正是 $\|b-Ax_k\|_2$。恢复式为 $x_k=x_0+M^{-1}z_k$。

## B. 手算与构造

### NLA-MR-B01

$$
q_1=(1,1)^T/\sqrt2,\quad
Aq_1=(3,1)^T/\sqrt2.
$$

$$
h_{11}=2,\quad q_2=(1,-1)^T/\sqrt2,\quad h_{21}=1.
$$

第一步

$$
y_1=\frac{[2,1]\cdot[\sqrt2,0]}{5}=\frac{2\sqrt2}{5},
$$

$$
x_1=(2/5,2/5)^T,\quad r_1=(-1/5,3/5)^T.
$$

第二步 $Aq_2=q_2$，所以

$$
Q_2=\frac1{\sqrt2}
\begin{bmatrix}1&1\\1&-1\end{bmatrix},
\quad
H_2=\begin{bmatrix}2&0\\1&1\end{bmatrix}.
$$

解 $H_2y=\sqrt2e_1$ 得

$$
y=(\sqrt2/2,-\sqrt2/2)^T,
\quad x_2=(0,1)^T,\quad r_2=0.
$$

### NLA-MR-B02

正规方程为

$$
\begin{bmatrix}5&4\\4&6\end{bmatrix}y
=
\begin{bmatrix}2\\1\end{bmatrix}.
$$

行列式为 $14$，所以

$$
y=\frac1{14}\begin{bmatrix}8\\-3\end{bmatrix}
=\begin{bmatrix}4/7\\-3/14\end{bmatrix}.
$$

实现不用正规方程，因为它平方 $\kappa(\bar H_2)$；Givens/Householder QR 更稳定且可在线更新。

### NLA-MR-B03

$$
p_0^TAp_0=(1,1)\cdot(1,-1)=0,
$$

所以 CG 首步分母为零。$\mathcal K_1=\operatorname{span}\{b\}$，候选 $x=\alpha b$：

$$
\|b-\alpha Ab\|_2^2
=(1-\alpha)^2+(1+\alpha)^2=2+2\alpha^2.
$$

最优 $\alpha=0$，残差不降。$\mathcal K_2=\mathbb R^2$，可取 $x=A^{-1}b=(1,-1)^T$，残差为零。

### NLA-MR-B04

一个 float32 向量为

$$
4\times10^7\text{ bytes}\approx40\text{ MB}.
$$

约 101 个基向量需 $4.04$ GB，尚未计工作向量、Hessenberg 和对齐。累计内积数

$$
\sum_{j=1}^{100}j=5050.
$$

若重正交一次，正交内积大致翻倍。

### NLA-MR-B05

$$
\|r\|_2=\sqrt2,
$$

$$
M^{-1}r=(10^{-6},10^3)^T,\qquad
\|M^{-1}r\|_2\approx10^3.
$$

预条件残差把第二分量放大 $10^3$、第一分量压低 $10^6$，与真残差二范数不在同一尺度。只用 $\|M^{-1}r\|_2$ 停止可能过度追逐某些方向或忽略另一些方向；最终仍要验收原方程真残差。

## C. 推导与证明

### NLA-MR-C01

$r_0=\beta q_1$、$x=x_0+Q_ky$，由

$$
AQ_k=Q_{k+1}\bar H_k
$$

得

$$
r=Q_{k+1}(\beta e_1-\bar H_ky).
$$

$Q_{k+1}$ 列正交，故范数相等。最小二乘一阶条件：

$$
\bar H_k^*(\beta e_1-\bar H_ky_k)=0.
$$

又 $\mathcal R(AQ_k)=\mathcal R(Q_{k+1}\bar H_k)$，提升到原空间即

$$
(AQ_k)^*r_k=0,
$$

所以 $r_k\perp A\mathcal K_k$。

### NLA-MR-C02

$$
x_0+\mathcal K_k\subseteq x_0+\mathcal K_{k+1}.
$$

下一轮至少可以选择旧 $x_k$，故 $\|r_{k+1}\|\le\|r_k\|$。若新方向没有提供可降低残差的分量，等号成立，因而不保证严格下降。

### NLA-MR-C03

$x_k=x_0+q_{k-1}(A)r_0$，所以

$$
r_k=[I-Aq_{k-1}(A)]r_0=p_k(A)r_0,
\quad p_k(0)=1.
$$

若相对最小多项式 $m$ 满足 $m(A)r_0=0$ 且 $m(0)\ne0$，则 $p=m/m(0)$ 是合法残差多项式，并在次数 $\deg m$ 时给出零残差。

### NLA-MR-C04

$$
p(A)=Vp(\Lambda)V^{-1},
$$

因此

$$
\|p(A)\|_2
\le\|V\|_2\|V^{-1}\|_2\max_i|p(\lambda_i)|
=\kappa_2(V)\max_i|p(\lambda_i)|.
$$

$\kappa(V)$ 衡量特征向量基的非正交性；巨大时，只在谱点上构造小多项式不足以控制算子。

### NLA-MR-C05

Arnoldi 中 $h_{ij}=q_i^*Aq_j$。若 $A=A^*$，当 $i<j-1$，

$$
h_{ij}=q_i^*Aq_j=(Aq_i)^*q_j=0,
$$

因为 $Aq_i$ 只含相邻 Lanczos 方向。Hessenberg 同时 Hermitian，只能三对角。MINRES 因而求

$$
\min_y\|\beta e_1-\bar T_ky\|_2.
$$

## D. 边界、反例与纠错

### NLA-MR-D01

完整 GMRES 保留整个正交基，并在不断扩大的空间中优化。重启只把当前残差传给下一周期，旧 Ritz/Schur 方向和此前构造的残差多项式被丢弃，因此不是同一个数学算法的纯内存优化。

### NLA-MR-D02

比较 $A_1=\lambda I$ 与

$$
A_2=\begin{bmatrix}\lambda&M\\0&\lambda\end{bmatrix}.
$$

两者特征值相同，但 $A_2$ 的 $p(A_2)$ 还含 $Mp'(\lambda)$ 项；非正规暂态和 GMRES 曲线可完全不同。

### NLA-MR-D03

MINRES 依赖预条件后算子仍自伴。一般 ILU 的 $M$ 非对称，不能保证这一点。需要固定线性 SPD 预条件器，并以对称变换或等价加权内积方式作用。

### NLA-MR-D04

显式重算 $b-Ax$；检查 Arnoldi 正交缺陷；核对内部 norm type 和左右预条件；检查解是否只在周期末更新；提高残差精度；检查 matvec 是否固定线性；必要时替换残差或重启；最终报告后向误差。

### NLA-MR-D05

最小残差解只要求 $\|Ax-b\|$ 最小，通常不唯一；最小长度解在这些解中再最小化欧氏 $\|x\|$。变量预条件后，算法可能最小化加权范数，映回原坐标不一定是欧氏最小长度解。

## E. AI 迁移

### NLA-MR-E01

用 VJP 实现 $v\mapsto(I-J_f^T)v$；右预条件以近似块 Jacobian solve 提供。固定预条件用 GMRES，可变内层用 FGMRES。扫描 $m$，记录 VJP、基内存、归约、内部和真残差；最终对原伴随方程验收。

### NLA-MR-E02

以

$$
M=\operatorname{blkdiag}(\widehat H,\widehat S)
$$

近似 KKT 能量，两个块都需 SPD，且整体保持对称。否则 MINRES 的 Lanczos 自伴结构失效。报告块 solve 成本、真残差和约束残差。

### NLA-MR-E03

不同内层步数产生 $M_j^{-1}$，普通 GMRES 的固定映射假设失效。FGMRES 保存每步 $z_j=M_j^{-1}v_j$，即整个 $Z_k$，并用 $x=x_0+Z_ky$ 更新。

### NLA-MR-E04

小线性残差只说明近似满足 Newton 方程；Hessian 负曲率可能使方向不是下降方向，模型也可能只在局部可信。还需检查 $g^Td$、$d^THd$、信赖域、实际与预测下降比、步长和外层目标。

### NLA-MR-E05

固定硬件、矩阵、预条件和真残差阈值；报告 matvec、预条件调用、全局归约、字节通信、峰值基内存、墙钟、正交缺陷和最终后向误差。流水方法增加的漂移与可靠更新成本必须计入。
