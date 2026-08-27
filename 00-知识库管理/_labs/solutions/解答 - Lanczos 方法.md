---
type: solution
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[Lanczos 方法]]"
exercise: "[[习题 - Lanczos 方法]]"
prerequisites: ["[[定理 - 有限维谱定理]]", "[[标准正交基与 Gram-Schmidt]]"]
related: ["[[实验 - Lanczos Ritz 收敛、残差与正交性]]", "[[Arnoldi 方法]]"]
sources: ["[[S-2023-Demmel-Krylov-Arnoldi-Lanczos]]", "[[S-2000-Netlib-Krylov-Eigensolver-Templates]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - Lanczos 方法

> [!warning] 使用边界
> 请先独立推导。以下关于三项递推、交错和残差—谱距离的简洁结论以实对称/Hermitian 算子为前提；一般非正规矩阵不能照搬。

## A. 识别与复述

### NLA-LAN-A01

给定 $q_1\ne0$，

$$
\mathcal K_k(A,q_1)=\operatorname{span}\{q_1,Aq_1,\ldots,A^{k-1}q_1\}
$$

是搜索空间。Lanczos 基 $Q_k=[q_1,\ldots,q_k]$ 是该空间的一组标准正交坐标基，不是另一个空间。小矩阵

$$
T_k=Q_k^TAQ_k
$$

的特征值 $\theta$ 是 Ritz 值；若 $T_ky=\theta y$，则 $x=Q_ky$ 是原空间 Ritz 向量。层次是

$$
\text{算子与起点}\to\text{搜索空间}\to\text{正交坐标}\to\text{小特征问题}\to\text{原空间近似}.
$$

### NLA-LAN-A02

若 $A\in\mathbb R^{n\times n}$、$Q_k\in\mathbb R^{n\times k}$，则

- $T_k\in\mathbb R^{k\times k}$；
- $q_{k+1}\in\mathbb R^n$、$e_k\in\mathbb R^k$；
- $\beta_k$ 是标量；
- 等式两边均为 $n\times k$。

逐步正交化使投影矩阵先呈上 Hessenberg；$A=A^T$ 又给出 $T_k=T_k^T$。对称上 Hessenberg 在第一条副对角线以外上下两侧都为零，故为对称三对角。

### NLA-LAN-A03

- lucky breakdown：精确算术中 $\beta_j=0$，当前 Krylov 空间已成不变子空间，是成功终止；
- 数值 breakdown：$\beta_j$ 很小但非零，需相对尺度判定，不能用固定绝对阈值；
- 正交性丢失：浮点递推的 $Q^TQ\ne I$，是误差机制；
- ghost Ritz value：已收敛方向重新进入基，造成伪重复值，是需诊断的症状；
- 锁定：把已收敛方向从活动空间隔离，是处置；
- 重启：压缩子空间、保留目标信息后继续，是内存/成本管理策略。

## B. 手算与构造

### NLA-LAN-B01

首先

$$
\alpha_1=q_1^TAq_1=\frac{4+2+1}{3}=\frac73.
$$

于是

$$
w_1=Aq_1-\alpha_1q_1
=\frac1{3\sqrt3}(5,-1,-4)^T,
$$

$$
\beta_1=\|w_1\|=\frac{\sqrt{42}}{3\sqrt3}=\frac{\sqrt{14}}3,
\qquad
q_2=\frac1{\sqrt{42}}(5,-1,-4)^T.
$$

第二个对角系数

$$
\alpha_2=q_2^TAq_2
=\frac{4\cdot25+2\cdot1+1\cdot16}{42}
=\frac{59}{21}.
$$

代入三项递推并化简得到

$$
w_2=Aq_2-\beta_1q_1-\alpha_2q_2,
\qquad
\beta_2=\frac{3\sqrt3}{7},
\qquad
q_3=\frac1{\sqrt{14}}(1,-3,2)^T.
$$

最后

$$
\alpha_3=q_3^TAq_3
=\frac{4+18+4}{14}=\frac{13}{7}.
$$

故

$$
T_3=
\begin{bmatrix}
7/3&\sqrt{14}/3&0\\
\sqrt{14}/3&59/21&3\sqrt3/7\\
0&3\sqrt3/7&13/7
\end{bmatrix}.
$$

三维无 breakdown 时 $Q_3$ 为完整正交矩阵，所以 $T_3=Q_3^TAQ_3$ 与 $A$ 正交相似；校验 $\operatorname{tr}T_3=7=\operatorname{tr}A$。

### NLA-LAN-B02

$$
T_2=
\begin{bmatrix}7/3&\sqrt{14}/3\\\sqrt{14}/3&59/21\end{bmatrix}.
$$

二阶特征公式给出

$$
\theta_{1,2}=\frac{18\pm\sqrt{79}}7
\approx3.8413,\ 1.3020.
$$

它们位于 $[1,4]$，并分别已偏向两端，但“每个 Ritz 值都必须靠近某个真特征值”的定量精度仍需残差；仅由落在谱包络内不能得出准确性。

### NLA-LAN-B03

$$
\|r\|=|\beta_ke_k^Ty|=0.04\times0.03=1.2\times10^{-3}.
$$

以 $\|x\|=1$ 的尺度化条件

$$
\frac{\|r\|}{\|A\|+|\theta|}\le\varepsilon
$$

判断。即使忽略分母中的 $|\theta|$，也有

$$
\frac{1.2\times10^{-3}}{20}=6\times10^{-5}>10^{-5},
$$

所以尚不能宣称满足；加入非负 $|\theta|$ 后结论可能改变，实际必须报告该值而非猜测。

### NLA-LAN-B04

matvec 浮点量约为

$$
50\times2\times7\times10^6=7\times10^8.
$$

保存 $Q_{50}$ 需

$$
10^6\times50\times8=4\times10^8\text{ bytes}\approx400\text{ MB}
$$

（约 $381$ MiB）。若只传播三项递推，活动向量可降到少数几个，约几十 MB；但形成很多 $Q_ky_i$ 或做全重正交需要基，除非采用二次遍历重构。因此“递推短”不是“所有输出都常数内存”。

### NLA-LAN-B05

变换特征值为

$$
\mu_i=\frac1{\lambda_i-2.1}
=\left\{-\frac{10}{11},-10,\frac{10}{29}\right\}.
$$

最大模 $-10$ 对应原特征值 $2$。第二大模是 $10/11$，所以理想幂式收敛因子

$$
\left|\frac{-10/11}{-10}\right|=\frac1{11}.
$$

### NLA-LAN-B06

按升序，交错为

$$
0.9\le1.2\le2.1\le3.7\le3.9,
$$

满足 $\theta_i^{(3)}\le\theta_i^{(2)}\le\theta_{i+1}^{(3)}$。这只描述嵌套投影小矩阵之间的关系。$3.9$ 是否接近 $\lambda_{\max}(A)$ 还需 Ritz 残差或额外谱界；单凭单调/交错不能认证精度。

## C. 推导与证明

### NLA-LAN-C01

上 Hessenberg 意味着 $h_{ij}=0$ 当 $i>j+1$。若 $H=H^T$，对 $j>i+1$ 有

$$
h_{ij}=h_{ji}=0,
$$

因为转置位置满足 $j>i+1$，落在下方远带。故只有 $i=j$ 或 $|i-j|=1$ 可能非零，恰为三对角。

### NLA-LAN-C02

归纳假设对 $i\le j-2$，已有 $Aq_i\in\operatorname{span}\{q_{i-1},q_i,q_{i+1}\}\subseteq\operatorname{span}\{q_1,\ldots,q_{j-1}\}$。于是

$$
q_i^TAq_j=(Aq_i)^Tq_j=0,
$$

因为 $q_j$ 与前 $j-1$ 个基向量正交。因此在 $Aq_j$ 上，除 $q_{j-1}$ 与 $q_j$ 外所有旧方向系数都为零。记

$$
\alpha_j=q_j^TAq_j,
\qquad
\beta_{j-1}=q_{j-1}^TAq_j,
$$

再令

$$
w=Aq_j-\beta_{j-1}q_{j-1}-\alpha_jq_j,
\quad
\beta_j=\|w\|,
\quad q_{j+1}=w/\beta_j,
$$

就得

$$
Aq_j=\beta_{j-1}q_{j-1}+\alpha_jq_j+\beta_jq_{j+1}.
$$

### NLA-LAN-C03

令 $x=Q_ky$。由分解

$$
\begin{aligned}
Ax-\theta x
&=AQ_ky-\theta Q_ky\\
&=Q_k(T_ky-\theta y)+\beta_kq_{k+1}e_k^Ty\\
&=\beta_kq_{k+1}e_k^Ty.
\end{aligned}
$$

因 $\|q_{k+1}\|=1$，取范数得等式。若 $q_{k+1}$ 未归一化或递推关系已被有限精度严重破坏，最后一步不再是精确认证；生产代码可抽查直接残差。

### NLA-LAN-C04

$$
\begin{aligned}
Q_k^T(AQ_ky-\theta Q_ky)
&=(Q_k^TAQ_k)y-\theta(Q_k^TQ_k)y\\
&=T_ky-\theta y=0.
\end{aligned}
$$

因此残差没有搜索空间内的分量：在当前子空间允许的所有一阶试探方向上，小特征问题已经把误差投影消掉；未解释的信息只在其正交补中。

### NLA-LAN-C05

写 $x=\sum_ic_iu_i$，其中 $A u_i=\lambda_i u_i$、$\sum_i|c_i|^2=1$。则

$$
\|r\|^2
=\sum_i|c_i|^2|\lambda_i-\theta|^2
\ge\min_i|\lambda_i-\theta|^2.
$$

所以存在 $i$ 使 $|\lambda_i-\theta|\le\|r\|$。但若多个 $\lambda_i$ 聚在 $\theta$ 附近，$x$ 可以是对应子空间内任意混合。要界定到某一唯一 $u_j$ 的角度，需 $\operatorname{gap}_j=\min_{i\ne j}|\lambda_i-\lambda_j|$，典型界形如 $\sin\angle(x,u_j)\lesssim\|r\|/\operatorname{gap}_j$。

### NLA-LAN-C06

按定义，任意 $v\in\mathcal K_k$ 可写为

$$
v=\sum_{j=0}^{k-1}c_jA^jq_1=p_{k-1}(A)q_1,
\quad
p_{k-1}(t)=\sum_{j=0}^{k-1}c_jt^j.
$$

反向也显然成立。若 $A=U\Lambda U^T$，则

$$
p(A)q_1=U p(\Lambda)U^Tq_1,
$$

即每个特征分量乘以 $p(\lambda_i)$。Rayleigh–Ritz 在这一多项式可达空间中选最佳近似方向，所以滤波多项式并非预先逐系数指定，而由投影小问题隐式决定。

## D. 边界、反例与纠错

### NLA-LAN-D01

$Aq_1=Ae_2=e_1$，可取 $q_2=e_1$。但

$$
q_2^TAq_1=1,
\qquad
q_1^TAq_2=0.
$$

故投影矩阵的上下相邻元不相等。三项 Lanczos 把二者视为同一个 $\beta$ 的推导依赖 $A=A^T$，此处被直接破坏；应使用 Arnoldi 的上 Hessenberg关系。

### NLA-LAN-D02

精确算术里，新向量与全部旧基正交；浮点短递推只显式消去最近两个方向。某 Ritz 向量收敛后，其对应模式对舍入扰动很敏感，微小分量可再次被多项式放大并进入新基，于是小矩阵中像是同一特征值再次出现。

诊断包括：检查 $\|Q^TQ-I\|$、比较重复 Ritz 向量在原空间的夹角、抽查直接残差。处置包括：全/选择性重正交、锁定已收敛向量、厚重启或经过验证的部分重正交。真重根应表现为多个互相正交且各自残差小的方向，不能只按数值重复判定。

### NLA-LAN-D03

$$
\theta=1+\frac\delta2,
$$

$$
r=Ax-\theta x
=\frac1{\sqrt2}\left(-\frac\delta2,\frac\delta2\right)^T,
\qquad
\|r\|=\frac{|\delta|}{2}.
$$

但 $x$ 与 $e_1,e_2$ 的夹角都为 $45^\circ$。当 gap 也只有 $|\delta|$ 时，残差变小只是整个二维谱簇近似不变，不能选择一个唯一向量；稳定对象是簇的不变子空间。

### NLA-LAN-D04

$\beta_k$ 随 $A$ 的整体缩放而缩放，所以固定 $10^{-12}$ 不具尺度不变性；而且 Ritz 残差还乘 $|e_k^Ty|$。可使用

$$
\eta=\frac{|\beta_ke_k^Ty|}{\|A\|_2+|\theta|}
$$

（单位 Ritz 向量），或分母取可计算的 $\|A\|$ 估计与安全下界。停止需 $\eta\le\tau$，并报告直接残差抽查、正交缺陷及是否达到用户要求的绝对/相对精度。

### NLA-LAN-D05

不应显式形成逆。固定移位可对 $A-\sigma I$ 做一次稀疏 $LDL^T$/LU 分解并反复三角求解，或用带预条件的迭代内层求解。显式逆通常更稠密、存储更大，而且一次 matvec 不比因子求解更可靠。

shift-and-invert 的代价可能由填充和内层同步主导；内层误差使外层不再作用于精确的 $(A-\sigma I)^{-1}$。最终必须回到原算子验收

$$
\|Ax-\theta x\|,
$$

不能只报告变换问题残差。

## E. AI 迁移

### NLA-LAN-E01

算子定义为 $v\mapsto Hv=\nabla^2L(w)v$，每次 HVP 不形成 Hessian。运行对称 Lanczos，目标同时取最大代数与最小代数 Ritz 值，而非只取最大模；随机起点记录种子，若关心多重/聚簇方向用 block 起点。以尺度化原问题残差、$\|Q^TQ-I\|$ 和重复运行稳定性停止/诊断。

输出至少含两端 Ritz 值、Ritz 向量或方向乘积、直接 HVP 残差、matvec 数和未收敛标志。若自动微分 HVP 不对称（随机层、状态更新、容差差异），先做双线性对称性抽检 $u^THv\approx(Hu)^Tv$；失败时不能宣称对称 Lanczos 保证。

### NLA-LAN-E02

不形成 $C$，而实现

$$
v\mapsto Cv=\frac1N X^T(Xv).
$$

一次调用需要读 $X$ 做两次矩阵—向量乘；若不能缓存数据，$k$ 步约需 $k$ 次全数据 pass（实现融合时仍包含等价读量）。Lanczos 适合少数协方差特征对和对称谱函数；随机 SVD 用块矩阵乘更适合 GPU/分布式吞吐、一次求多个奇异方向和低秩近似。比较时应按 data pass、块宽、通信与残差，而不只按 matvec 数。

### NLA-LAN-E03

组合 Laplacian 的常数向量在连通图上给出已知零特征值；多连通分量对应多维零空间。若要 Fiedler 向量，应把起点及每次结果投影到已知零空间正交补，或锁定全部零模。最小非零值是内部/近零目标，直接 Lanczos 可能慢；shift-and-invert 可加速，但 $L$ 在全空间奇异，需在约束子空间求解或加合适移位。最终以 $\|Lx-\theta x\|$、$x\perp\ker L$ 和连通性假设验收。

### NLA-LAN-E04

对随机探针 $z$，归一化 $q_1=z/\|z\|$ 后，Lanczos 小矩阵近似谱测度的 Gauss 求积：

$$
z^Tf(A)z
=\|z\|^2q_1^Tf(A)q_1
\approx\|z\|^2e_1^Tf(T_k)e_1.
$$

对多个满足 $\mathbb E[zz^T]=I$ 的探针取平均，期望为 $\operatorname{tr}f(A)$。$k$ 控制每个二次型的 Krylov/求积偏差；探针数控制随机方差。增加探针不能修复过小 $k$ 的系统偏差，增加 $k$ 也不能消除有限探针方差，报告必须分开两项预算。

### NLA-LAN-E05

固定 $k$ 步程序的梯度是“初始化、舍入、正交化和有限迭代输出”这一计算图的导数；精确简单特征值的导数则是 $u^T(dA)u$，要求目标简单且求解收敛。有限 $k$ 时两者一般不同。

重根/谱碰撞使单个向量和排序不光滑；锁定、阈值停止与重启包含离散分支。反向保存 $Q_k$ 会把前向三向量内存变成 $O(nk)$，重算则增加 matvec。更稳健的设计常对谱簇投影或平滑谱函数求导，并明确“算法梯度”还是“隐式精确量梯度”。

## 验收清单

- [x] 所有 25 题均有独立编号与答案；
- [x] 手算例含系数、基和小矩阵；
- [x] 证明题标明对称性与正交性使用位置；
- [x] 反例覆盖非对称、聚簇、尺度和显式逆；
- [x] AI 题给出算子、成本、停止与结论边界。
