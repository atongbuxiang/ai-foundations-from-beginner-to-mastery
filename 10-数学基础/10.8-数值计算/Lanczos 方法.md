---
type: concept
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
aliases: [Lanczos 迭代, 对称 Lanczos]
prerequisites: ["[[幂法、反幂法与 Rayleigh 商迭代]]", "[[Hessenberg 化与 QR 特征值算法]]", "[[定理 - 有限维谱定理]]", "[[标准正交基与 Gram-Schmidt]]", "[[矩阵扰动]]"]
related: ["[[Arnoldi 方法]]", "[[共轭梯度法]]", "[[SVD 算法与谱范数估计]]", "[[矩阵函数与矩阵指数]]", "[[数值线性代数 MOC]]", "[[实验 - Lanczos Ritz 收敛、残差与正交性]]"]
sources: ["[[S-2023-Demmel-Krylov-Arnoldi-Lanczos]]", "[[S-2000-Netlib-Krylov-Eigensolver-Templates]]", "[[S-2002-Higham-数值算法准确性与稳定性]]"]
exercises: ["[[习题 - Lanczos 方法]]"]
solutions: ["[[解答 - Lanczos 方法]]"]
created: 2026-08-15
updated: 2026-08-27
---

# Lanczos 方法

> [!abstract] 本章主问题
> 对实对称或复 Hermitian 大矩阵，Lanczos 只用矩阵—向量乘和三项递推，就把高维算子投影成小型实对称三对角矩阵；小矩阵的 Ritz 值、Ritz 向量与矩阵函数可近似原问题，但浮点中短递推会丢失全局正交性，必须用残差、重正交化、锁定和重启组成完整算法。

先用下图回答一个视觉问题：**对称性为何把 Arnoldi 压缩成三项递推，而可靠 Lanczos 实现为什么仍离不开 residual 与正交性管理？**

![[00-知识库管理/_assets/figures/numerical-analysis/fig-lanczos-ritz-orthogonality-v2.svg|880]]

> [!figure] 图 10.8.12｜Lanczos 三项递推、Ritz residual 与 ghost 管理
> A 从 $q_{k-1},q_k,Aq_k,q_{k+1}$ 的局部关系和三对角非零模式说明对称性把长 Arnoldi 递推压缩为三项；B 从小矩阵特征对 $T_ky=\theta y$ 构造 Ritz 向量 $u=Q_ky$，并给出 $\|Au-\theta u\|=|\beta_ke_k^Ty|$ 的廉价残差；C 表示有限精度正交性损失使已收敛方向重新进入基并产生 ghost Ritz values，列出重正交、锁定和重启补救。来源：独立绘制；理论接口参考 Demmel、Netlib Krylov Templates 与 Higham；生成脚本：[[plot_numerical_spectral_methods_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先把 Lanczos 理解为“在 Krylov 子空间中维护正交坐标”，三项递推来自 $A=A^T$ 与 Galerkin 正交条件；B 再从小型 $T_k$ 的 Ritz 对回到高维向量，并用最后一个递推系数计算真正的高维 residual；C 最后提醒精确算术的全局正交性不是浮点实现的永久不变量，监测 $Q_k^TQ_k-I$、重复 Ritz 值与已收敛方向回流后再选择重正交/锁定/重启。

**适用边界（图没有证明什么）。** 三项递推要求实对称或复 Hermitian 算子；一般非对称问题应转向 Arnoldi。小 Ritz residual 在有谱间隙时才直接支持向量误差解释；聚簇或重特征值应讨论不变子空间。图也不等于具体内存、通信与 restart 策略，实际 eigensolver 还需定义目标谱段、容差、最大子空间与 breakdown 处理。

## 一、学习目标

完成本章后，你应能：

1. 定义 Krylov 子空间并解释原始幂基为何数值病态；
2. 从 Arnoldi 关系和对称性逐步推出 Lanczos 三项递推；
3. 手算一个 $3\times3$ 例子并构造 $T_k$；
4. 从 Lanczos 分解推导 Ritz 残差公式；
5. 用交错定理解释极端 Ritz 值的单调趋近；
6. 区分 lucky breakdown、数值 breakdown、ghost Ritz value 与真正重特征值；
7. 比较全重正交化、选择性重正交化、锁定和重启；
8. 为 Hessian、协方差、图 Laplacian 和矩阵函数任务写出可验收的算法契约。

> [!question] 初学者读完必须能回答
> 1. Krylov 子空间为什么有信息，而原始幂基为什么容易病态？
> 2. 对称性怎样把 Arnoldi 的长正交化化为 Lanczos 三项递推？
> 3. $T_k=Q_k^TAQ_k$ 为什么是实对称三对角矩阵？
> 4. Ritz residual 公式为何只需要 $\beta_k$ 与 $e_k^Ty$？
> 5. Residual 小到什么程度才可结合 spectral gap 解释向量准确性？
> 6. Ghost Ritz value 怎样由有限精度正交性损失产生？
> 7. 全/选择性重正交、locking 与 thick/implicit restart 分别解决什么问题？

> [!note] 课程位置
> NUM-11 用双侧正交相似把整张稠密矩阵约化并计算全部 Schur 谱；本章在只允许 matvec 的大规模情形中，从一个起点逐步建立 Krylov 正交基。对称性让 projected Hessenberg 自动三对角，因此 NUM-11 的 $T$ 会在这里由三项递推重新出现。

> [!tip] 建议两遍阅读
> 第一遍只手算统一 $3\times3$ Gram 矩阵的两步 Lanczos，得到 $\alpha_1,\beta_1,\alpha_2,\beta_2$、$T_2$ 和 Ritz residual；第二遍再进入交错定理、ghost、重正交、locking、restart 与矩阵函数。先分清高维 residual 与小矩阵 eigenproblem，才不会把 Ritz value 当成无条件真特征值。

## 本章的推导问题链

1. 幂法为什么最终只剩一个方向，而 Krylov 方法希望保留多个多项式方向？
2. 怎样在不存储病态幂基的前提下张成同一子空间？
3. 对称性为何让 $Gv_k$ 只需减去当前和前一个基向量？
4. 两步递推产生的小矩阵 $T_2$ 怎样近似原矩阵谱？
5. 小矩阵 eigenpair 如何提升成高维 Ritz pair？
6. 为什么高维 residual 只需要最后一个 $\beta_k$ 和 eigenvector 的末分量？
7. 精确算术中的三项递推为何在浮点中仍可能产生 ghost？

## 贯穿算例：两次 matvec 得到什么谱信息

沿用

$$
G=Q\operatorname{diag}\!\left(1,\frac14,\frac1{16}\right)Q^T.
$$

选择 NUM-11 中的起点

$$
v_1=Qc_1,
\qquad
c_1=\frac1{\sqrt3}(1,1,1)^T.
$$

这等价于在三个特征方向上放置相同初始分量，但实际 Lanczos 只调用 $v\mapsto Gv$，不需要知道 $Q$。

### 符号与对象账本

| 对象 | 定义 | 本例中的值/作用 |
|---|---|---|
| $\mathcal K_k$ | $\operatorname{span}\{v_1,Gv_1,\ldots,G^{k-1}v_1\}$ | 搜索子空间 |
| $V_k$ | $[v_1,\ldots,v_k]$ | Krylov 标准正交基 |
| $\alpha_k$ | $v_k^TGv_k$ | 三对角主对角 |
| $\beta_k$ | 新 residual 的范数 | 三对角次对角/下一基向量尺度 |
| $T_k$ | $V_k^TGV_k$ | 小型 Ritz 矩阵 |
| $(\theta,y)$ | $T_ky=\theta y$ | 小空间 eigenpair |
| $u=V_ky$ | Ritz vector | 提升回原空间的近似方向 |
| $\|Gu-\theta u\|$ | Ritz residual | 近似特征对后验证书 |

### 第一步：第一次 matvec 产生 $\alpha_1$ 与新方向

$$
\alpha_1=v_1^TGv_1
=\frac13\left(1+\frac14+\frac1{16}\right)
=\frac7{16}.
$$

减去当前方向：

$$
w_1=Gv_1-\alpha_1v_1.
$$

在特征坐标中归一化可得

$$
\beta_1=\|w_1\|_2=\frac{\sqrt{42}}{16},
\qquad
v_2=Qc_2,
\qquad
c_2=\frac1{\sqrt{14}}(3,-1,-2)^T.
$$

于是

$$
Gv_1=\alpha_1v_1+\beta_1v_2.
$$

### 第二步：对称性让第二次只需三项

计算

$$
\alpha_2=v_2^TGv_2
=\frac{19}{28},
$$

再令

$$
w_2=Gv_2-\beta_1v_1-\alpha_2v_2.
$$

可得

$$
\beta_2=\|w_2\|_2=\frac{5\sqrt3}{56},
\qquad
v_3=Qc_3,
\qquad
c_3=\frac1{\sqrt{42}}(1,-5,4)^T.
$$

对称性保证 $w_2$ 与更早基向量的内积在精确算术中自动为零；一般非对称矩阵没有这条短递推，要进入 Arnoldi。

### 第三步：两次 matvec 得到一个 $2\times2$ Ritz 问题

$$
T_2=V_2^TGV_2
=\begin{bmatrix}
\frac7{16}&\frac{\sqrt{42}}{16}\\
\frac{\sqrt{42}}{16}&\frac{19}{28}
\end{bmatrix}.
$$

其两个 Ritz values 为

$$
\theta_\pm
=\frac{125\pm\sqrt{8961}}{224},
$$

数值上约为

$$
\theta_+\approx0.980636,
\qquad
\theta_-\approx0.135435.
$$

它们分别向外侧特征值 $1$ 与内侧区间 $[1/16,1/4]$ 提供近似，并满足对称 Ritz 值的交错关系。

### 第四步：不用再做高维 matvec也能算 Ritz residual

Lanczos 关系为

$$
GV_2
=V_2T_2+\beta_2v_3e_2^T.
$$

若 $T_2y=\theta y$ 且 $\|y\|=1$，令 $u=V_2y$，则

$$
\begin{aligned}
Gu-\theta u
&=GV_2y-V_2T_2y\\
&=\beta_2v_3e_2^Ty.
\end{aligned}
$$

因此

$$
\boxed{
\|Gu-\theta u\|_2
=\beta_2|e_2^Ty|
}.
$$

对 $\theta_+$，取归一化 eigenvector 与 $(\beta_1,\theta_+-\alpha_1)^T$ 同向，得到 residual 约 $0.123970$；对 $\theta_-$ 则约 $0.092451$。Ritz value 已接近某个真特征值，并不意味着方向误差可以脱离 gap 单独认证。

### 第五步：第三步为何出现 lucky breakdown

加入 $v_3$ 后，$V_3=[v_1,v_2,v_3]$ 已是整个三维空间的正交基，且

$$
T_3=V_3^TGV_3
=\begin{bmatrix}
\frac7{16}&\frac{\sqrt{42}}{16}&0\\
\frac{\sqrt{42}}{16}&\frac{19}{28}&\frac{5\sqrt3}{56}\\
0&\frac{5\sqrt3}{56}&\frac{11}{56}
\end{bmatrix}.
$$

下一 residual 为零，即 $\beta_3=0$；Krylov 子空间已经成为不变子空间，$T_3$ 的特征值精确等于 $1,1/4,1/16$。这叫 lucky breakdown，而不是故障。

### 核心公式七问：$\|Gu-\theta u\|=\beta_k|e_k^Ty|$

1. **从哪来？** 把小矩阵 eigenpair 代入 Lanczos 分解，$V_kT_ky$ 项完全抵消。
2. **为何廉价？** $\beta_k$ 已由递推得到，$e_k^Ty$ 只是小 eigenvector 的最后分量。
3. **Residual 小保证什么？** 至少存在真特征值靠近 $\theta$；方向误差还需谱隙。
4. **聚簇时怎么办？** 认证整个不变子空间，而不是强行区分单个 eigenvector。
5. **为什么会有 ghost？** 浮点中 $V_k^TV_k=I$ 会逐渐失效，已收敛方向重新进入 Krylov 基。
6. **怎样处理？** 监测正交缺陷，按需 full/selective reorthogonalization，并对收敛方向 locking/restart。
7. **AI 中如何用？** Hessian 极端谱、covariance PCA、图 Laplacian 和 matrix-function action 都可只用 matvec 建立 Ritz 证书。

> [!warning] 教学模型边界
> 三维模型在第三步必然耗尽空间，无法展示大规模 restart、通信成本或长期 ghost；给出的 residual 也不是“必须接受/拒绝”的统一阈值。实际停止应按矩阵尺度、目标 gap、任务预算和有限精度正交性共同决定。

> [!success] 第一遍停靠线
> 应能算出 $\alpha_1=7/16$、$\beta_1=\sqrt{42}/16$、$\alpha_2=19/28$、$\beta_2=5\sqrt3/56$，写出 $T_2$，再从 Lanczos 分解推出廉价 residual 公式；还要能解释为什么 $\beta_3=0$ 是不变子空间已经闭合，而不是算法崩溃。

## 二、前置检查

### 2.1 对称性为什么关键

本章默认

$$
A\in\mathbb R^{n\times n},\qquad A=A^T.
$$

复数情形把转置换成共轭转置，要求 $A=A^*$。由[[定理 - 有限维谱定理]]，$A$ 有实特征值和标准正交特征向量基。

### 2.2 已知工具

- [[幂法、反幂法与 Rayleigh 商迭代]]：多项式 $A^kq_1$ 会放大某些谱方向；
- [[标准正交基与 Gram-Schmidt]]：一组张成相同空间但条件更好的正交基；
- [[Hessenberg 化与 QR 特征值算法]]：一般正交投影产生 Hessenberg，小型对称 Hessenberg 必为三对角；
- [[矩阵扰动]]：残差、谱间隙和方向误差不是同一个量。

## 三、为什么不能直接保存幂序列

给定非零起点 $q_1$，第 $k$ 阶 Krylov 子空间定义为

$$
\mathcal K_k(A,q_1)
=\operatorname{span}\{q_1,Aq_1,A^2q_1,\ldots,A^{k-1}q_1\}.
$$

若 $A=U\Lambda U^T$，$q_1=Uc$，则

$$
A^jq_1=U\Lambda^jc
=\sum_{i=1}^n c_i\lambda_i^ju_i.
$$

这解释了两个相反现象：

1. **信息提取**：不同次数的多项式会以不同权重过滤谱；
2. **幂基病态**：若 $|\lambda_1|>|\lambda_2|$，高次向量逐渐平行于 $u_1$，显式矩阵
   $$
   K_k=[q_1,Aq_1,\ldots,A^{k-1}q_1]
   $$
   很快病态。

Lanczos 不放弃 $\mathcal K_k$，而是放弃病态幂基，改为构造标准正交基

$$
Q_k=[q_1,\ldots,q_k],\qquad Q_k^TQ_k=I_k.
$$

> [!warning] 子空间与基不是一回事
> Krylov 子空间是数学对象；幂基与 Lanczos 基只是它的两种坐标。说“幂基病态”不等于子空间本身无意义。

## 四、投影思想：先在小空间里问问题

在子空间 $\mathcal K_k$ 中取 $x=Q_ky$。若希望 $x$ 近似满足

$$
Ax=\theta x,
$$

可以要求残差

$$
r=Ax-\theta x
$$

与整个搜索空间正交：

$$
Q_k^Tr=0.
$$

代入 $x=Q_ky$：

$$
Q_k^TAQ_ky-\theta Q_k^TQ_ky=0.
$$

因为 $Q_k^TQ_k=I$，得到小型特征问题

$$
T_ky=\theta y,
\qquad
T_k=Q_k^TAQ_k\in\mathbb R^{k\times k}.
$$

这叫 **Rayleigh–Ritz 投影**：

- $\theta$ 是 Ritz value；
- $x=Q_ky$ 是 Ritz vector；
- $T_k$ 是 $A$ 在 Krylov 子空间中的压缩表示。

## 五、从 Arnoldi 到三对角

对一般矩阵，逐列正交化给出 Arnoldi 关系

$$
AQ_k=Q_kH_k+h_{k+1,k}q_{k+1}e_k^T,
$$

其中 $H_k$ 上 Hessenberg。若 $A=A^T$，则

$$
H_k=Q_k^TAQ_k
$$

也对称，因为

$$
H_k^T=Q_k^TA^TQ_k=Q_k^TAQ_k=H_k.
$$

一个矩阵若既对称又上 Hessenberg，就只能在主对角和第一条上下副对角线上非零。因此

$$
H_k=T_k=
\begin{bmatrix}
\alpha_1&\beta_1\\
\beta_1&\alpha_2&\ddots\\
&\ddots&\ddots&\beta_{k-1}\\
&&\beta_{k-1}&\alpha_k
\end{bmatrix}.
$$

这一步是 Lanczos 短递推的根源：不是“神奇地只需两个旧向量”，而是**对称性把投影矩阵的带宽压缩到三对角**。

## 六、逐步推导三项递推

矩阵关系的第 $j$ 列是

$$
Aq_j
=\beta_{j-1}q_{j-1}+\alpha_jq_j+\beta_jq_{j+1},
$$

约定 $q_0=0,\beta_0=0$。

### 6.1 求 $\alpha_j$

左乘 $q_j^T$：

$$
q_j^TAq_j
=\beta_{j-1}q_j^Tq_{j-1}
+\alpha_jq_j^Tq_j
+\beta_jq_j^Tq_{j+1}.
$$

正交性使第一、三项为零，中间项为 $\alpha_j$，所以

$$
\boxed{\alpha_j=q_j^TAq_j}.
$$

### 6.2 求新方向

移项得到

$$
z_j=Aq_j-\alpha_jq_j-\beta_{j-1}q_{j-1}.
$$

精确算术下，$z_j$ 自动与 $q_1,\ldots,q_j$ 全部正交。令

$$
\beta_j=\|z_j\|_2,
\qquad
q_{j+1}=z_j/\beta_j,
$$

就得到下一列。

### 6.3 为什么更早的向量系数为零

对 $i\le j-2$，

$$
q_i^TAq_j=(Aq_i)^Tq_j.
$$

而 $Aq_i\in\operatorname{span}(q_{i-1},q_i,q_{i+1})\subseteq
\operatorname{span}(q_1,\ldots,q_{j-1})$，与 $q_j$ 正交，故

$$
q_i^TAq_j=0.
$$

这里明确使用了 $A=A^T$。删除对称性后，第一行等号一般不成立，必须回到长 Arnoldi 正交化。

## 七、基本算法

```text
输入：对称算子 v ↦ Av，非零起点 v₁，最大维数 m
q₀ = 0，β₀ = 0，q₁ = v₁ / ‖v₁‖₂
for j = 1, …, m
    z = Aqⱼ − βⱼ₋₁qⱼ₋₁
    αⱼ = qⱼᵀz
    z = z − αⱼqⱼ
    [按策略重正交化 z]
    βⱼ = ‖z‖₂
    if βⱼ 足够小：停止或判定 breakdown
    qⱼ₊₁ = z / βⱼ
end
输出：Qₘ、α₁:ₘ、β₁:ₘ 和三对角 Tₘ
```

实践中不应把“足够小”写成无尺度常数；至少要相对 $\|A\|$、局部递推量和机器精度判断。

## 八、完整手算：$3\times3$ 对角矩阵

取

$$
A=\operatorname{diag}(4,2,1),
\qquad
q_1=\frac1{\sqrt3}(1,1,1)^T.
$$

### 8.1 第一步

$$
\alpha_1=q_1^TAq_1=\frac{4+2+1}{3}=\frac73.
$$

于是

$$
z_1=Aq_1-\alpha_1q_1
=\frac1{3\sqrt3}(5,-1,-4)^T.
$$

所以

$$
\beta_1=\|z_1\|_2=\frac{\sqrt{14}}3,
\qquad
q_2=\frac1{\sqrt{42}}(5,-1,-4)^T.
$$

检查 $q_1^Tq_2=(5-1-4)/\sqrt{126}=0$。

### 8.2 第二步

$$
\alpha_2=q_2^TAq_2
=\frac{4\cdot25+2\cdot1+1\cdot16}{42}
=\frac{59}{21}.
$$

再算

$$
z_2=Aq_2-\alpha_2q_2-\beta_1q_1
=\frac9{7\sqrt{42}}(1,-3,2)^T.
$$

故

$$
\beta_2=\frac{3\sqrt3}{7},
\qquad
q_3=\frac1{\sqrt{14}}(1,-3,2)^T.
$$

### 8.3 第三步与完整投影

$$
\alpha_3=q_3^TAq_3
=\frac{4+18+4}{14}=\frac{13}{7}.
$$

因此

$$
T_3=
\begin{bmatrix}
7/3&\sqrt{14}/3&0\\
\sqrt{14}/3&59/21&3\sqrt3/7\\
0&3\sqrt3/7&13/7
\end{bmatrix}.
$$

因为三步后 $Q_3$ 是整个 $\mathbb R^3$ 的标准正交基，$T_3=Q_3^TAQ_3$ 与 $A$ 正交相似，特征值正好是 $1,2,4$。迹检查：

$$
\frac73+\frac{59}{21}+\frac{13}{7}=7=\operatorname{tr}(A).
$$

只做两步时，

$$
\lambda(T_2)=\frac{18\pm\sqrt{79}}7
\approx3.8413,\;1.3020,
$$

已经从内部逼近最大值 $4$ 与最小值 $1$。

## 九、Lanczos 分解与维度

完成 $k$ 步后：

$$
AQ_k=Q_kT_k+\beta_kq_{k+1}e_k^T.
$$

维度逐项检查：

| 对象 | 维度 |
|---|---:|
| $A$ | $n\times n$ |
| $Q_k$ | $n\times k$ |
| $T_k$ | $k\times k$ |
| $q_{k+1}$ | $n$ |
| $e_k$ | $k$ |
| $\beta_kq_{k+1}e_k^T$ | $n\times k$ |

右侧最后一项是“子空间尚未闭合”的唯一出口；若 $\beta_k=0$，则 $AQ_k=Q_kT_k$，$\mathcal K_k$ 已为不变子空间。

## 十、Ritz 对与廉价残差

设

$$
T_ky=\theta y,
\qquad \|y\|_2=1,
$$

令 $x=Q_ky$。由于 $Q_k$ 列正交，$\|x\|_2=1$。由 Lanczos 分解：

$$
\begin{aligned}
Ax
&=AQ_ky\\
&=(Q_kT_k+\beta_kq_{k+1}e_k^T)y\\
&=Q_k\theta y+\beta_kq_{k+1}e_k^Ty\\
&=\theta x+\beta_k(e_k^Ty)q_{k+1}.
\end{aligned}
$$

所以

$$
\boxed{
\|Ax-\theta x\|_2
=|\beta_k|\,|e_k^Ty|
}.
$$

右侧只需要：

- 最后一个递推系数 $\beta_k$；
- 小矩阵特征向量 $y$ 的最后一个分量。

不必每次形成高维 $x$ 再做额外一次 $Ax$。但在最终报告中，仍建议对已返回的 Ritz 向量做一次独立直接残差复核。

## 十一、残差能保证什么

对称矩阵有一个强结论：若 $\|x\|=1$，则至少存在某个 $\lambda\in\Lambda(A)$ 满足

$$
\min_i|\theta-\lambda_i|
\le\|Ax-\theta x\|_2.
$$

若还能确认目标特征值与其余谱的分离

$$
\operatorname{gap}
=\min_{j\ne i}|\lambda_j-\theta|,
$$

则方向误差受 residual/gap 控制。没有 gap 时，小残差只说明接近某个不变子空间，不保证接近唯一单向量。

因此停止准则应至少报告缩放残差，例如

$$
\eta=
\frac{\|Ax-\theta x\|_2}
{(\|A\|_2+|\theta|)\|x\|_2},
$$

而不是只看 $|\theta_k-\theta_{k-1}|$。

## 十二、交错与极端 Ritz 值

因为 $T_k$ 是 $T_{k+1}$ 的首要主子矩阵，Cauchy 交错定理给出

$$
\theta_1^{(k+1)}
\ge\theta_1^{(k)}
\ge\theta_2^{(k+1)}
\ge\cdots.
$$

特别地，按降序排列时：

$$
\theta_{\max}^{(k)}\nearrow\lambda_{\max}(A),
\qquad
\theta_{\min}^{(k)}\searrow\lambda_{\min}(A)
$$

在精确算术和嵌套 Krylov 空间下成立。这解释了为何极端值常先收敛，也提供了额外的单调性诊断。

> [!warning] 单调性不能替代残差
> 浮点正交性丢失、重启或改变子空间后，简单嵌套论证可能不再直接适用。生产停止仍以残差和状态为准。

## 十三、多项式过滤视角

任何 $x\in\mathcal K_k(A,q_1)$ 都可写成

$$
x=p_{k-1}(A)q_1,
$$

其中 $p_{k-1}$ 次数不超过 $k-1$。若 $q_1=\sum c_iu_i$，则

$$
p(A)q_1=\sum_i c_ip(\lambda_i)u_i.
$$

所以 Krylov 法是在寻找一个低次多项式：在目标特征值上大，在非目标谱上小。相比幂法固定使用 $p(t)=t^{k-1}$，Lanczos 通过 Rayleigh–Ritz 从整个多项式空间中自适应选取方向，因此常显著更快。

这也解释：

- 极端孤立特征值容易被低次多项式分离；
- 聚簇目标、内部特征值或狭窄谱间隙更困难；
- shift-invert、Chebyshev 过滤和预条件本质上是在改变可用过滤器。

## 十四、breakdown：好事还是坏事

### 14.1 lucky breakdown

若精确算术下 $\beta_j=0$，则

$$
AQ_j=Q_jT_j,
$$

$\mathcal K_j$ 已是不变子空间，$T_j$ 的特征对提升后是 $A$ 的精确特征对。这通常是“幸运终止”。

### 14.2 数值 near-breakdown

浮点中 $\beta_j$ 很小可能来自：

- 真正接近不变子空间；
- 消去和下溢；
- 正交性污染；
- 起点几乎缺失某个方向。

因此不能只因 $\beta_j<10^{-12}$ 就宣布成功；必须结合尺度、Ritz 残差、正交缺陷和重复值诊断。

## 十五、浮点中的正交性丢失

精确算术证明“$z_j$ 自动与所有旧 $q_i$ 正交”使用了一连串精确等号。浮点中只显式减去了 $q_j,q_{j-1}$，更早方向的小舍入分量不会被清除。

特别是某 Ritz 对收敛后，该方向会通过舍入误差重新进入新向量；随后 $T_k$ 可能出现同一已收敛特征值的重复副本，称为 **ghost Ritz value**。

必须区分：

- 真正的重特征值：原矩阵不变子空间维数确实大于一；
- ghost：同一数值方向因正交性丢失被重复计算；
- 聚簇：不同但相近的特征值需要子空间级判断。

## 十六、重正交化策略

| 策略 | 做法 | 主要成本 | 适用场景 |
|---|---|---|---|
| 无重正交 | 只执行三项递推 | 每步 $O(n)$ 向量运算 | 短运行、允许专门 ghost 检测 |
| full reorthogonalization | 对全部旧 $q_i$ 做一遍或两遍 MGS | 总计 $O(nk^2)$、存储 $O(nk)$ | 教学基线、可靠小中型子空间 |
| selective reorthogonalization | 只对已收敛/危险方向重正交 | 依赖监测 | 经典高性能 Lanczos |
| partial reorthogonalization | 估计正交性并按阈值触发 | 额外状态 | 大型对称谱问题 |

“Lanczos 每步只有三项”描述递推结构，不表示实现永远只需保存三个向量。若要返回 Ritz 向量、重正交、锁定或重启，通常必须保存或可重建更多基向量。

## 十七、锁定、厚重启与隐式重启

随着 $k$ 增大：

- 基存储为 $O(nk)$；
- 重正交为 $O(nk^2)$；
- 小型三对角问题也不断增长。

因此生产算法会限制子空间维数 $m$。

### 17.1 locking

把已达到残差阈值的 Ritz 向量移出活动迭代并保持与新基正交，避免重新计算同一方向。

### 17.2 thick restart

不只保留一个向量，而是保留若干目标 Ritz 向量/子空间，再从它们继续扩展。它比“只留当前最好向量”保留更多谱信息。

### 17.3 implicit restart

通过对小型投影问题做隐式移位 QR，把不想要的方向过滤掉，同时把所需信息压回固定宽度 Krylov 表示。思想上是“在小矩阵里做多项式过滤”，而不是从零重来。

重启控制内存，但会改变子空间嵌套和收敛轨迹；它不是免费的工程细节。

## 十八、内部特征值与 shift-invert

直接 Lanczos 通常先得到谱端点。若需要靠近 $\sigma$ 的内部特征值，可对

$$
C=(A-\sigma I)^{-1}
$$

做 Lanczos。若 $Aq_i=\lambda_iq_i$，则

$$
Cq_i=\frac1{\lambda_i-\sigma}q_i.
$$

离 $\sigma$ 最近的 $\lambda_i$ 被映为最大模特征值。

但每个“matvec”现在其实是解线性系统

$$
(A-\sigma I)y=x.
$$

必须记录：

- 分解/预条件成本；
- 内层求解容差；
- $\sigma$ 接近谱时的病态性；
- 从变换后 Ritz 值 $\mu$ 恢复 $\lambda=\sigma+1/\mu$ 的误差传播。

不能形成显式逆矩阵。

## 十九、block Lanczos

用起始块 $Q_1\in\mathbb R^{n\times b}$ 代替单向量，可构造 block Krylov 空间

$$
\mathcal K_k(A,Q_1)
=\operatorname{span}\{Q_1,AQ_1,\ldots,A^{k-1}Q_1\}.
$$

优点：

- 更适合重根和谱簇；
- 能利用矩阵—矩阵乘和现代硬件；
- 随机块降低完全漏掉目标子空间的风险。

代价是块正交化、小型块三对角问题、rank loss 和 deflation 逻辑更复杂。

## 二十、成本、存储与通信

设每次 $Av$ 成本为 $C_A$，运行 $k$ 步：

| 组成 | 无全重正交 | 全重正交 |
|---|---:|---:|
| matvec | $kC_A$ | $kC_A$ |
| 向量递推 | $O(nk)$ | $O(nk)$ |
| 正交化 | 局部 $O(nk)$ | 总计 $O(nk^2)$ |
| 基存储 | 理论最少 $O(n)$ | $O(nk)$ |
| $T_k$ 存储 | $O(k)$ | $O(k)$ |

在 GPU/分布式环境中，内积引发的全局归约和基向量读取可能比 flop 更贵。算法报告应把以下量分开：

1. matvec 次数；
2. 对 $A$ 的数据 passes；
3. 全局同步次数；
4. 保存的 $n$ 维向量数；
5. 小型特征问题成本。

## 二十一、与共轭梯度的关系

对 SPD 线性系统 $Ax=b$，从 $q_1=b/\|b\|$ 生成的同一 Lanczos 三对角投影可写出 Krylov 近似

$$
x_k=Q_kT_k^{-1}e_1\|b\|_2.
$$

[[共轭梯度法]]用更适合线性求解的递推实现相同 Galerkin 条件。两者共享 Krylov 几何，但目标不同：

- Lanczos 特征算法关注 $T_k$ 的 Ritz 对；
- CG 关注 $Ax=b$ 的能量范数最优近似与残差。

不要把“共用三项递推”误写成两算法输出相同对象。

## 二十二、矩阵函数与随机 Lanczos quadrature

若要近似

$$
q_1^Tf(A)q_1,
$$

Lanczos 给出高斯求积型近似

$$
q_1^Tf(A)q_1
\approx e_1^Tf(T_k)e_1.
$$

结合随机探针还可估计

$$
\operatorname{tr}f(A),
$$

用于 log-determinant、谱密度和不确定性计算。但误差同时包含 Krylov 截断与随机 trace 误差；本章只建立接口，不展开完整求积定理。

## 二十三、AI 与科学计算接口

### 23.1 Hessian 极端曲率

对参数 $w\in\mathbb R^n$，Hessian $H=\nabla^2L(w)$ 通常不能显式存储，但自动微分可计算 Hessian–vector product

$$
v\mapsto Hv.
$$

若 $H$ 近似对称，Lanczos 可估计最大/最小曲率、负曲率方向和谱密度。必须报告：mini-batch、阻尼、HVP 精度、参数子空间和残差。

### 23.2 PCA 与协方差

激活矩阵 $X\in\mathbb R^{N\times d}$ 的协方差算子

$$
C v=\frac1N X^T(Xv)
$$

可在不形成 $d\times d$ Gram 矩阵时做 Lanczos。它减少存储，但每步需要一次 $Xv$ 和 $X^Tu$；若数据流只能单遍访问，应考虑随机范围方法。

### 23.3 图 Laplacian 与表示平滑

对稀疏图 Laplacian $L\in\mathbb R^{n\times n}$，小特征值描述连通与低频子空间。直接 Lanczos 先找极端值；最小非零内部值常需 shift-invert、谱变换或专门约束去除常数向量。

### 23.4 神经网络 Jacobian 的边界

一般 Jacobian $J$ 不对称，不能直接用对称 Lanczos。可选择：

- 对 $J^TJ$ 做 Lanczos 估计奇异值，但条件数被平方且每步需 JVP/VJP；
- 使用 [[Arnoldi 方法]]处理 $J$ 的特征值；
- 使用 Golub–Kahan 双对角化直接处理奇异值。

“代码能运行”不等于对称性假设成立。

## 二十四、可微计算边界

若下游损失依赖简单、分离的 Ritz 值，有限步计算图可以反向传播。但需要区分：

- 目标数学量 $\lambda_i(A)$ 的导数；
- 固定步 Lanczos 程序输出的导数；
- 重启、排序、锁定、阈值和随机起点造成的分段/离散变化。

重根或谱碰撞时单个特征向量不可唯一微分，应改用谱投影或不变子空间损失。反向传播还可能需要保存全部基，破坏前向短递推的内存优势。

## 二十五、实验：三个不同问题

[[实验 - Lanczos Ritz 收敛、残差与正交性]]分别验证：

1. 极端 Ritz 值比另一端更早达到舍入地板；
2. 直接残差与 $|\beta_ke_k^Ty|$ 一致；
3. 在显式 9 位运算模拟中，聚簇谱使无重正交的基缺陷快速升高，而全重正交保持在模拟舍入量级。

图形与原始数值由 [plot_lanczos_ritz_orthogonality.py](</Users/tong/Nodes/basic/00-知识库管理/_labs/code/plot_lanczos_ritz_orthogonality.py>) 生成。

## 二十六、可信 Lanczos 报告模板

至少记录：

```text
operator: 维度、dtype、对称性检查、matvec 实现
target: largest/smallest/interior，所需数量 nev
start: 随机种子或确定性起点，block size
subspace: 最大维数、restart/locking 策略
transform: none / shift-invert / polynomial filter
orthogonalization: none / full / selective / partial
stopping: 缩放 Ritz 残差与容差
output: Ritz values、直接残差、正交缺陷、收敛标志
cost: matvec、线性求解、passes、同步、峰值内存
exceptions: breakdown、未收敛、重复/ghost 诊断
```

## 二十七、常见失败模式

| 失败 | 错误原因 | 修正 |
|---|---|---|
| 对非对称 $A$ 直接用三项 Lanczos | 三对角推导依赖 $A=A^T$ | 改用 Arnoldi 或对称化任务 |
| 显式形成 $A^kq$ | 幂基迅速病态 | 边乘边正交 |
| 只看 Ritz 值变化 | 停滞不等于残差小 | 用缩放 Ritz 残差 |
| 把重复 Ritz 值全当真重根 | 可能是正交性丢失 ghost | 检查 $Q^TQ$、锁定和重正交 |
| interior target 仍用原始算子 | 端点通常先收敛 | shift-invert/过滤，并报告内层误差 |
| 宣称只存三个向量却返回很多 Ritz 向量 | 向量恢复需要基或二次遍历 | 报告真实存储/重构策略 |
| 对 $J^TJ$ 估奇异值却忽略平方条件数 | 微小方向更难 | Golub–Kahan 或稳定 SVD 路线 |

## 二十八、掌握检查

你应能在不看正文时完成：

- [ ] 从 $H_k=Q_k^TAQ_k$ 的对称+Hessenberg 推出三对角；
- [ ] 推导 $Aq_j=\beta_{j-1}q_{j-1}+\alpha_jq_j+\beta_jq_{j+1}$；
- [ ] 手算本章 $3\times3$ 例子前两步；
- [ ] 从 Lanczos 分解推出廉价残差公式；
- [ ] 解释小残差、gap 与方向准确性的关系；
- [ ] 给出 ghost Ritz value 的有限精度来源；
- [ ] 为一个 HVP/PCA/图 Laplacian 任务选择目标、变换、重启和验收指标。

## 二十九、课程闭环与后继

- 习题：[[习题 - Lanczos 方法]]；
- 独立解答：[[解答 - Lanczos 方法]]；
- 实验：[[实验 - Lanczos Ritz 收敛、残差与正交性]]；
- 一般矩阵推广：[[Arnoldi 方法]]；
- 线性系统后继：[[共轭梯度法]]；
- 奇异值后继：[[SVD 算法与谱范数估计]]。

## 来源与证据边界

- [[S-2023-Demmel-Krylov-Arnoldi-Lanczos]]：Krylov、Arnoldi、Lanczos、成本和 Ritz 残差主推导；
- [[S-2000-Netlib-Krylov-Eigensolver-Templates]]：重正交化、ghost、重启、shift-invert 与生产验收；
- [[S-2002-Higham-数值算法准确性与稳定性]]：浮点与后向稳定的通用语言。

正文中的三项递推和残差恒等式是经典精确算术结论；具体收敛速度依赖谱分布、起点和变换；有限精度策略与性能必须按实际实现验证。
