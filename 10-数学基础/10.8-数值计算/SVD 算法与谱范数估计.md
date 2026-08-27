---
type: concept
status: draft
area: [math/numerical-linear-algebra, math/low-rank-methods]
aliases: [数值 SVD, Golub-Kahan 双对角化, 谱范数幂迭代, 随机 SVD]
prerequisites: ["[[奇异值分解]]", "[[Householder 与 Givens 变换]]", "[[稳定最小二乘与正规方程的风险]]", "[[Lanczos 方法]]", "[[Arnoldi 方法]]", "[[矩阵扰动]]"]
related: ["[[低秩近似]]", "[[Moore-Penrose 伪逆]]", "[[矩阵的秩]]", "[[有效秩]]", "[[数值线性代数 MOC]]", "[[实验 - SVD 双对角化、谱范数与随机子空间]]"]
sources: ["[[S-1965-Golub-Kahan-SVD算法]]", "[[S-2025-LAPACK-SVD驱动与双对角化]]", "[[S-2011-Halko-Martinsson-Tropp-随机低秩]]", "[[S-2024-Su-10407-低秩近似之路（二）SVD]]", "[[S-2025-Su-10878-SVD的导数]]"]
exercises: ["[[习题 - SVD 算法与谱范数估计]]"]
solutions: ["[[解答 - SVD 算法与谱范数估计]]"]
created: 2026-08-15
updated: 2026-08-23
---

# SVD 算法与谱范数估计

> [!abstract] 本章主问题
> 数学定理保证任意矩阵都有 SVD，数值算法则必须选择：完整稠密 SVD 通常先用双侧 Householder 把矩阵约化为双对角，再解小结构问题；只求少数奇异值时可用 Golub–Kahan/Lanczos、幂迭代或随机子空间，但必须避免显式正规方程、报告双侧残差，并把谱隙、数据遍历和有限精度纳入承诺。

先用下图回答一个视觉问题：**完整 SVD、top-$k$、谱范数和随机值域为何是四种不同任务，它们怎样共享同一验收语言？**

![[00-知识库管理/_assets/figures/numerical-analysis/fig-svd-algorithms-certificates-v2.svg|880]]

> [!figure] 图 10.8.14｜SVD 任务分流、双对角化与双侧 residual 证书
> A 按完整/经济 SVD、前 $k$ 个奇异三元组、仅 $\sigma_1$ 和随机值域 $Q$ 分流到双对角驱动、Golub–Kahan/块 Krylov、交替幂迭代/Lanczos 与 randomized range finder；B 表示双侧正交变换 $U_0^TAV_0=B$ 把稠密矩阵约化为双对角，避免显式形成 $A^TA$；C 对候选 $(\sigma,u,v)$ 同时检查 $Av-\sigma u$、$A^Tu-\sigma v$、正交性、重构、rank tolerance 与成本。来源：独立绘制；理论接口参考 Golub–Kahan、LAPACK 与 Halko–Martinsson–Tropp；生成脚本：[[plot_numerical_iterative_methods_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** 先在 A 明确交付物：是否要全部向量、少量三元组、一个范数估计，还是只要低秩值域；再在 B 看计算路径，正交左右变换保留奇异值并把困难压缩到小型双对角问题；最后在 C 回到原矩阵，用双侧 residual 分别检验左右奇异方程，再补充 $U,V$ 正交缺陷、重构误差、数值秩容差、matvec/data pass 和随机种子。

**适用边界（图没有证明什么）。** 图没有比较 QR iteration、divide-and-conquer、MRRR 类思想、Jacobi SVD 或具体 GPU 驱动的实际性能；算法选择仍依赖形状、精度、向量需求与硬件。避免“显式形成 $A^TA$”不等于任何交替 $A/A^T$ 作用都不允许。随机值域的过采样 $p$ 与幂步 $q$ 给概率—数据遍历权衡，必须用独立后验验证，不能由一张机制图给出失败概率。

## 一、学习目标

完成本章后，你应能：

1. 区分 SVD 存在定理、完整分解算法、部分奇异值算法和范数估计器；
2. 从左右 Householder 变换推导双对角化；
3. 手算一个 $3\times2$ 双对角化例子；
4. 解释双对角 QR、分治与 Jacobi 路线解决的不同子问题；
5. 推导 Golub–Kahan 双对角递推及其与 $A^TA,AA^T$ 的关系；
6. 推导谱范数幂迭代收敛因子并识别小 gap；
7. 设计 randomized range finder，区分过采样 $p$ 与幂步 $q$；
8. 用双侧残差、正交缺陷、重构误差和数据 pass 验收 AI 低秩计算。

> [!question] 初学者读完必须能回答
> 1. 完整 SVD、top-$k$、谱范数估计和低秩值域的交付物有何不同？
> 2. 双侧 Householder 为什么产生双对角矩阵并保留奇异值？
> 3. 显式 $A^TA$ 为什么会平方条件数并损伤小奇异值？
> 4. Golub–Kahan 与交替幂迭代怎样在不形成正规矩阵时利用其谱？
> 5. 谱隙怎样控制 $\sigma_1$ 与奇异向量估计的收敛？
> 6. Randomized range finder 中 $p$、$q$ 与 data pass 各控制什么？
> 7. 为什么候选奇异三元组必须同时检查左右 residual、正交性与 rank tolerance？

## 二、先区分四个任务

给定 $A\in\mathbb R^{m\times n}$，SVD 为

$$
A=U\Sigma V^T,\qquad
\sigma_1\ge\sigma_2\ge\cdots\ge0.
$$

但“求 SVD”至少有四种不同产品：

| 任务 | 输出 | 常见规模 | 合适入口 |
|---|---|---|---|
| 完整/经济 SVD | 全部奇异值与所需奇异向量 | 稠密中小型 | 双对角化 + 结构化 SVD 驱动 |
| 截断 SVD | 前 $k$ 个三元组 | 大型稀疏/隐式 | Golub–Kahan、块 Krylov、随机 SVD |
| 只估谱范数 | $\sigma_1$ 或上下界 | 训练内循环 | 交替幂迭代、Lanczos bidiagonalization |
| 低秩值域 | $Q$ 使 $A\approx QQ^TA$ | 数据/加速任务 | randomized range finder |

输出目标不同，计算和误差承诺也不同。若只要 $\sigma_1$，构造全部 $U,V$ 是浪费；若要最小奇异值，简单幂法又根本不对准目标。

## 三、为什么不应从显式 $A^TA$ 开始

理论上

$$
A^TAv_i=\sigma_i^2v_i,\qquad
AA^Tu_i=\sigma_i^2u_i.
$$

这证明奇异向量与特征问题的关系，却不等于推荐显式形成正规方程：

1. 条件数平方：$\kappa_2(A^TA)=\kappa_2(A)^2$；
2. 形成 $A^TA$ 引入额外舍入并可能丢失小奇异值信息；
3. 稀疏 $A$ 的 $A^TA$ 可能显著填充；
4. 左奇异向量还需再由 $u_i=Av_i/\sigma_i$ 恢复，小 $\sigma_i$ 时放大误差。

> [!tip] 正确区分
> “不显式形成 $A^TA$”不等于“算法从不作用 $A^TA$”。交替执行 $v\mapsto Av\mapsto A^Tu$ 在代数上等价于正规算子作用，但保留了矩阵结构和更好的舍入/存储路径。

## 四、完整稠密 SVD 的两阶段路线

经典路线把困难分成：

$$
A
\xrightarrow[\text{左右 Householder}]{U_0^TAV_0=B}
B
\xrightarrow[\text{结构化迭代}]{B=\widehat U\Sigma\widehat V^T}
\Sigma.
$$

最终

$$
U=U_0\widehat U,\qquad V=V_0\widehat V.
$$

第一阶段把一般矩阵约化为双对角；第二阶段只处理对角与一条相邻带，便于稳定、快速地迭代和追踪奇异向量。

## 五、Householder 双对角化

先设 $m\ge n$。第 $j$ 步：

1. 左 Householder $P_j$ 把第 $j$ 列在第 $j$ 行以下清零；
2. 右 Householder $R_j$ 把第 $j$ 行在第 $j+1$ 列以后清零；
3. 只更新剩余尾部子矩阵。

累计正交矩阵

$$
U_0=P_1P_2\cdots,\qquad
V_0=R_1R_2\cdots,
$$

得到上双对角

$$
B=
\begin{bmatrix}
d_1&e_1&&\\
&d_2&e_2&\\
&&\ddots&\ddots\\
&&&d_n\\
&&&0
\end{bmatrix}.
$$

实现中通常不显式构造每个稠密反射矩阵，而存 Householder 向量和标量因子，按块更新以利用 BLAS-3。

### 5.1 形状变体

- $m\ge n$：常约化为上双对角；
- $m<n$：可得到下双对角或转置问题；
- 极端长瘦矩阵：有时先做 QR，再对较小 $R$ 做 SVD，但必须根据驱动和所需向量决定。

## 六、完整手算：$3\times2$ 双对角化

取

$$
A=
\begin{bmatrix}
3&0\\
4&1\\
0&2
\end{bmatrix}.
$$

### 6.1 第一列左反射

对 $x=(3,4,0)^T$，选择把它映到 $-5e_1$ 的 Householder：

$$
P_1=
\begin{bmatrix}
-3/5&-4/5&0\\
-4/5&3/5&0\\
0&0&1
\end{bmatrix}.
$$

它满足 $P_1^TP_1=I$ 且

$$
P_1A=
\begin{bmatrix}
-5&-4/5\\
0&3/5\\
0&2
\end{bmatrix}.
$$

第一行只剩一个尾列，所以无需非平凡右反射。

### 6.2 第二列尾部左反射

需要把

$$
x_2=(3/5,2)^T
$$

映到 $-(\sqrt{109}/5)e_1$。令嵌入行 $2,3$ 的 Householder 为 $P_2$，则

$$
P_2P_1A=
\begin{bmatrix}
-5&-4/5\\
0&-\sqrt{109}/5\\
0&0
\end{bmatrix}=B.
$$

这已是上双对角。因为左右变换正交，

$$
\sigma_i(A)=\sigma_i(B),\qquad
\|A\|_2=\|B\|_2,\qquad
\|A\|_F=\|B\|_F.
$$

> [!warning] 符号并非数学本质
> 反射可映到 $+\|x\|e_1$ 或 $-\|x\|e_1$；数值实现选择能避免灾难性消去的符号。最后双对角元的符号不改变奇异值。

## 七、双对角矩阵怎样变成 SVD

双对角 $B$ 仍需迭代。常见路线包括：

### 7.1 隐式 QR 型迭代

对双对角结构施加隐式移位与 Givens 旋转，追逐 bulge，直到超对角元可 deflate。若积累左右旋转即可得到奇异向量。它与对称三对角 QR 密切相关，但直接在 $B$ 上组织可避免粗暴形成 $B^TB$ 的精度损失。

### 7.2 分治

把双对角问题拆成子问题，再通过低秩 secular equation 合并。求大量奇异向量时常有优秀性能，但工作空间和具体形状会影响实际优势。

### 7.3 Jacobi 型 SVD

通过成对列/行旋转逐步正交化。在某些高相对精度任务上有优势，代价和并行形态不同。不能只按渐近 FLOPs 选算法，应以库实现、形状、所需向量和精度目标为准。

### 7.4 LAPACK 语言

- `xGEBRD`：一般稠密矩阵到双对角；
- `xBDSQR`：双对角 QR 迭代并可更新奇异向量；
- `xGESVD`：标准 SVD 驱动；
- `xGESDD`：分治驱动。

这些名称描述可复核的软件接口，不表示所有厂商实现、所有矩阵形状下的性能排序相同。

## 八、Golub–Kahan–Lanczos 双对角递推

大型稀疏/隐式矩阵只求少数奇异三元组时，不做完整稠密约化。从非零左起点 $b$ 开始，令

$$
\beta_1=\|b\|_2,\qquad u_1=b/\beta_1,\qquad v_0=0,
$$

再递推：

$$
\alpha_j v_j=A^Tu_j-\beta_jv_{j-1},
$$

$$
\beta_{j+1}u_{j+1}=Av_j-\alpha_ju_j,
$$

每次归一化使 $\alpha_j,\beta_{j+1}\ge0$。若 $B_k$ 是以 $\alpha_j$ 为主对角、$\beta_{j+1}$ 为次对角的下双对角矩阵，合并后有

$$
AV_k=U_kB_k+\beta_{k+1}u_{k+1}e_k^T,
$$

以及

$$
A^TU_k=V_kB_k^T.
$$

求 $B_k$ 的 SVD，再把小奇异向量分别提升到 $U_k,V_k$。也可从右起点写出转置的上双对角版本，但索引和尾项位置必须随之一起改变，不能混用两套约定。

### 8.1 与 Lanczos 的关系

可在对称增广矩阵

$$
\mathcal A=
\begin{bmatrix}0&A\\A^T&0\end{bmatrix}
$$

上看 Lanczos。若 $A v_i=\sigma_i u_i$、$A^Tu_i=\sigma_i v_i$，则

$$
\mathcal A\frac1{\sqrt2}\binom{u_i}{\pm v_i}
=\pm\sigma_i\frac1{\sqrt2}\binom{u_i}{\pm v_i}.
$$

所以非零奇异值成为成对特征值 $\pm\sigma_i$。Golub–Kahan 利用块结构，避免显式构造增广矩阵。

### 8.2 有限精度

理论短递推不意味着基在浮点中自动保持双正交。已收敛奇异方向可重新进入并产生伪重复，仍需部分/选择性/全重正交、锁定和重启。

## 九、奇异三元组残差

候选三元组 $(\widehat\sigma,\widehat u,\widehat v)$ 应满足

$$
r_u=A\widehat v-\widehat\sigma\widehat u,
$$

$$
r_v=A^T\widehat u-\widehat\sigma\widehat v.
$$

把两者合并，正是增广矩阵特征残差：

$$
\begin{bmatrix}0&A\\A^T&0\end{bmatrix}
\binom{\widehat u}{\widehat v}
-\widehat\sigma\binom{\widehat u}{\widehat v}
=\binom{r_u}{r_v}.
$$

因此可信报告至少给

$$
\eta_i=
\frac{\sqrt{\|r_u\|_2^2+\|r_v\|_2^2}}
{\widehat{\|A\|}_2+|\widehat\sigma_i|},
$$

以及 $\|\widehat U^T\widehat U-I\|$、$\|\widehat V^T\widehat V-I\|$。只检查 $Av\approx\sigma u$ 是单侧且不完整的。

## 十、谱范数的交替幂迭代

因为 $\|A\|_2=\sigma_1(A)$，可从随机单位 $v_0$ 开始：

$$
u_{t+1}=\frac{Av_t}{\|Av_t\|},
\qquad
v_{t+1}=\frac{A^Tu_{t+1}}{\|A^Tu_{t+1}\|}.
$$

估计量可取

$$
\widehat\sigma_t=u_{t+1}^TAv_{t+1}
$$

或一致定义下的 $\|Av_t\|$。一次完整 $A,A^T$ 更新等价于对 $A^TA$ 做幂迭代，所以方向误差的主因子为

$$
\left(\frac{\sigma_2}{\sigma_1}\right)^{2t}.
$$

### 10.1 何时很慢

若 $\sigma_1\approx\sigma_2$，主方向不唯一或难分，单向量幂法收敛慢；但这不一定妨碍估计“顶端子空间”或近似谱范数。若训练中 $A$ 每步变化，一步 warm-start 幂迭代追踪的是动态算法状态，其偏差还取决于权重变化速度。

### 10.2 停止与承诺

监控双侧残差和相邻估计变化。仅运行固定一步时，应称“谱范数估计/下界”而非精确谱范数，并记录迭代状态是否跨训练步复用。

## 十一、随机值域查找与随机 SVD

目标是找 $Q\in\mathbb R^{m\times\ell}$，$\ell=k+p$，使

$$
A\approx QQ^TA.
$$

基础算法：

1. 采样 $\Omega\in\mathbb R^{n\times\ell}$；
2. $Y=A\Omega$；
3. $Q=\operatorname{orth}(Y)$；
4. $B=Q^TA$；
5. 对小矩阵 $B=\widetilde U\Sigma V^T$ 做 SVD；
6. $U=Q\widetilde U$，再截断到 $k$。

### 11.1 过采样 $p$

$p$ 给目标秩周围更多随机试探方向，降低漏掉重要子空间的概率。它增加块宽、内存和通信，但通常只需小常数级余量。

### 11.2 幂步 $q$

使用

$$
Y=(AA^T)^qA\Omega.
$$

奇异值权重从 $\sigma_i$ 变为 $\sigma_i^{2q+1}$，放大谱分离。实际必须交替做

```text
Y = orth(A Ω)
repeat q times:
    Z = orth(Aᵀ Y)
    Y = orth(A Z)
```

若直接连乘而不正交，小奇异方向会在浮点中被主方向吞没。

### 11.3 两类误差不要混淆

- 值域误差：$\|(I-QQ^T)A\|$，由 $\ell,p,q$ 和随机性决定；
- 最终 rank-$k$ 截断误差：$\|A-U_k\Sigma_kV_k^T\|$，在已捕获值域内再做最优截断。

实验面板 C 以 $\sigma_{k+p+1}$ 归一化，是比较“同样值域维数 $k+p$ 的最优下界”，不是把 rank-$k$ 最优误差偷偷换成更小分母。

## 十二、数据 pass 与硬件现实

对外存/分布式矩阵，一次 $A\Omega$ 的数据 pass 可能比额外 FLOPs 更贵。算法报告应计数：

- $A$ 与 $A^T$ 的 passes；
- 块宽 $\ell$；
- 全局归约次数；
- 峰值内存；
- 是否能单遍或流式；
- 压缩/量化是否改变误差。

随机方法的优势常来自块乘和较少 pass，而不只是渐近复杂度。

## 十三、最小/内部奇异值

最大奇异值适合幂式方法；最小奇异值对应 $A^TA$ 的最小特征值，直接幂法无效。可选：

- 稠密矩阵直接完整/分治/Jacobi SVD；
- 增广矩阵的 shift-and-invert；
- 对正规方程的反幂，但必须面对条件数平方与线性求解；
- 专用部分 SVD/双对角 Lanczos 的内部目标变体。

若 $A$ 近秩亏，目标本身条件差。小 $\sigma_{min}$ 的相对误差比绝对误差更难，不能仅由普通后向稳定保证。

## 十四、数值秩与截断

数学秩对任意非零扰动都可能跳变。数值秩需要显式阈值，例如

$$
r_\tau=\#\{i:\sigma_i>\tau\},
$$

其中 $\tau$ 应结合

$$
\tau\approx c\,u\,\max(m,n)\sigma_1
$$

的舍入尺度、观测噪声和任务误差预算，而不是固定 `1e-6`。谱隙能帮助稳定选秩；无明显 gap 时应报告敏感区间或有效秩，而非伪装成唯一整数。

## 十五、算法选择表

| 场景 | 首选思路 | 主要风险 | 验收 |
|---|---|---|---|
| 中小稠密、全谱 | 库 SVD 驱动 | 工作空间/向量成本 | 重构、正交、双侧残差 |
| 大型稀疏、少数最大 | Golub–Kahan/块 Krylov | 正交性、重启 | 双侧残差、ghost |
| 训练中谱归一化 | warm-start 交替幂法 | 小 gap、时变偏差 | 残差、偶发高精度校准 |
| 大数据低秩近似 | 随机值域 + 小 SVD | 随机失败、pass | 投影误差、种子、passes |
| 最小/内部奇异值 | direct 或 shift-invert | 条件数、内层求解 | 原问题双侧残差 |
| 高相对精度小值 | 适合的高精度/Jacobi 路线 | 成本 | 分量相对误差与缩放 |

## 十六、AI 中的核心应用

### 16.1 谱归一化与 Lipschitz 控制

对权重 $W$，把 $W/\widehat\sigma_1(W)$ 用作约束。若 $\widehat\sigma_1$ 是低估，实际 Lipschitz 上界可能比预期大；固定一步幂法的速度换来了近似承诺。卷积算子的矩阵表示与 padding/stride 边界也必须和实现一致。

### 16.2 PCA、LoRA 与模型压缩

PCA 可对中心化数据或协方差做 SVD；LoRA/权重压缩用截断 SVD 给 Frobenius/谱范数下的最优低秩基线。但训练可塑性、量化和下游损失不等于静态矩阵范数，SVD 基线不是自动最优部署方案。

### 16.3 Jacobian 奇异值

JVP 提供 $Jv$，VJP 提供 $J^Tu$，无需显式 Jacobian 即可运行交替幂或 Golub–Kahan。最大奇异值衡量最坏局部放大；与 Arnoldi 的最大实部/最大模特征值回答不同问题。

### 16.4 注意力与长序列算子

低秩近似能压缩注意力核或状态映射，但谱随样本、位置和 mask 变化。报告应说明在哪个算子、哪批数据、哪种归一化上估计，避免把局部谱当全局常数。

## 十七、SVD 的可微边界

简单且分离的奇异值有

$$
d\sigma_i=u_i^T(dA)v_i.
$$

奇异向量导数含类似

$$
\frac1{\sigma_i^2-\sigma_j^2}
$$

的间隙分母；重复或近重复奇异值时，单个基向量不稳定，稳定对象是奇异子空间。还要区分：

- 对数学上精确 SVD 的隐式导数；
- 对固定步幂/随机算法计算图的导数；
- 排序、截断、符号/相位选择造成的不光滑。

实际损失若只依赖子空间投影 $U_kU_k^T$，通常比依赖每一列的符号和顺序更稳。

## 十八、可信实验报告模板

```text
matrix/operator: m×n、dtype、dense/sparse/JVP-VJP、scale
target: full/economy/rank-k/sigma-max/interior
algorithm: driver、bidiagonal Krylov、power、randomized
parameters: k、p、q、restart、seed、tolerance
orthogonalization: passes、U/V defects
residuals: ‖Av-σu‖、‖Aᵀu-σv‖、scaled combined residual
approximation: spectral/Frobenius projection and reconstruction error
cost: A/Aᵀ passes、matvec/block width、reductions、memory
rank decision: threshold、noise model、gap sensitivity
exceptions: unconverged、zero vector、ghost、NaN/overflow
```

## 十九、常见失败模式

| 失败 | 原因 | 修正 |
|---|---|---|
| 显式 $A^TA$ 后求特征分解 | 条件数平方与填充 | 直接 SVD/Golub–Kahan |
| 只检查 $Av=\sigma u$ | 单侧关系不足 | 同时检查 $A^Tu=\sigma v$ |
| 一步幂法称“精确谱范数” | gap 与起点未控制 | 称估计并做校准/残差 |
| 随机幂步不正交 | 主方向吞噬次方向 | 每个 $A,A^T$ pass 后 QR |
| 用固定阈值判秩 | 缺少尺度/噪声 | 相对尺度 + 任务模型 |
| 只报 rank-$k$ 重构误差 | 隐藏随机值域质量 | 另报投影误差与种子 |
| 重根处依赖单列梯度 | 基不唯一 | 子空间/投影损失 |

## 二十、实验与掌握检查

[[实验 - SVD 双对角化、谱范数与随机子空间]]验证：

1. 左右 Householder 双对角化的重构与正交误差接近双精度舍入；
2. $\sigma_2/\sigma_1=0.98$ 时，30 步谱范数迭代仍明显慢于 $0.2,0.8$；
3. 随机值域的过采样与一次幂步改善相对同维最优基线的投影误差。

你应能独立完成：

- [ ] 手算本章 $3\times2$ 双对角化；
- [ ] 解释为何不显式形成 $A^TA$；
- [ ] 写出 Golub–Kahan 递推与双侧残差；
- [ ] 推导谱范数幂法的平方谱比；
- [ ] 区分随机值域误差与最终 rank-$k$ 误差；
- [ ] 为稠密、稀疏、训练内循环和大数据场景选算法。

## 二十一、课程闭环

- 习题：[[习题 - SVD 算法与谱范数估计]]；
- 独立解答：[[解答 - SVD 算法与谱范数估计]]；
- 实验：[[实验 - SVD 双对角化、谱范数与随机子空间]]；
- 理论基础：[[奇异值分解]]、[[低秩近似]]、[[Moore-Penrose 伪逆]]；
- Krylov 基础：[[Lanczos 方法]]、[[Arnoldi 方法]]；
- 后继：[[有效秩]]与随机化数值线性代数。

## 来源与证据边界

- [[S-1965-Golub-Kahan-SVD算法]]：双对角化和经典 SVD 计算框架；
- [[S-2025-LAPACK-SVD驱动与双对角化]]：`GEBRD/GESVD/GESDD/BDSQR` 的当前接口边界；
- [[S-2011-Halko-Martinsson-Tropp-随机低秩]]：随机值域、过采样与幂方案；
- [[S-2024-Su-10407-低秩近似之路（二）SVD]]：低秩近似的 AI 语境；
- [[S-2025-Su-10878-SVD的导数]]：可微 SVD 与谱隙边界。

具体驱动性能依赖库版本、硬件与形状；随机误差是概率陈述；实验只验证确定性构造和固定种子下的机制，不能替代目标数据上的验收。
