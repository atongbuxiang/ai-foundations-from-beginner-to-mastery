---
type: solution
status: draft
area: [math/numerical-linear-algebra, math/low-rank-methods]
topic: "[[SVD 算法与谱范数估计]]"
exercise: "[[习题 - SVD 算法与谱范数估计]]"
prerequisites: ["[[奇异值分解]]", "[[Householder 与 Givens 变换]]", "[[Lanczos 方法]]"]
related: ["[[实验 - SVD 双对角化、谱范数与随机子空间]]", "[[低秩近似]]"]
sources: ["[[S-1965-Golub-Kahan-SVD算法]]", "[[S-2025-LAPACK-SVD驱动与双对角化]]", "[[S-2011-Halko-Martinsson-Tropp-随机低秩]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - SVD 算法与谱范数估计

> [!warning] 使用边界
> 请先独立作答。随机算法的结论带概率，幂法的速度依赖谱隙，双对角短递推在有限精度中仍需正交性管理。

## A. 识别与复述

### NLA-SVA-A01

| 任务 | 典型输出 | 主成本/数据访问 |
|---|---|---|
| 完整 SVD | 全 $\Sigma$，可选全 $U,V$ | 稠密约化与结构化迭代，约立方级 |
| 经济 SVD | 只保留 $\min(m,n)$ 个必要列 | 与完整奇异值相近，减少向量存储/回代 |
| 截断 SVD | 前 $k$ 个三元组 | 若用 Krylov，若干 $A,A^T$ 乘与正交 |
| 谱范数估计 | $\widehat\sigma_1$ 及方向 | 每步一次 $A$ 和一次 $A^T$ |
| 随机值域 | $Q$ 使 $A\approx QQ^TA$ | 块乘、少量数据 passes、QR |

“经济”是输出形状，“截断”是只求目标谱部分；二者不能混称。

### NLA-SVA-A02

第一阶段用左右正交矩阵把 $A$ 约化：

$$
U_0^TAV_0=B
$$

为双对角。第二阶段求

$$
B=\widehat U\Sigma\widehat V^T,
$$

再回乘 $U=U_0\widehat U,V=V_0\widehat V$。因为

$$
B^TB=V_0^TA^TAV_0,
$$

$B^TB$ 与 $A^TA$ 正交相似，特征值相同，故奇异值相同。

### NLA-SVA-A03

- `GEBRD`：双侧 Householder 双对角化的计算例程；
- `BDSQR`：对双对角矩阵做 QR 型 SVD，并可更新奇异向量；
- `GESVD`：面向一般稠密矩阵的标准高层 SVD 驱动；
- `GESDD`：使用分治核心路线的高层驱动。

性能还取决于 $m/n$ 形状、是否求左右向量、工作空间、BLAS、线程、缓存和厂商优化。API 算法族不等于跨硬件排序定理，应基准测试并验证精度。

## B. 手算与构造

### NLA-SVA-B01

第一反射

$$
P_1=
\begin{bmatrix}
-3/5&-4/5&0\\
-4/5&3/5&0\\
0&0&1
\end{bmatrix}
$$

满足 $P_1^TP_1=I$，直接乘得

$$
P_1A=
\begin{bmatrix}
-5&-4/5\\
0&3/5\\
0&2
\end{bmatrix}.
$$

对尾向量 $(3/5,2)^T$ 做第二左 Householder，使其变成 $(-\sqrt{109}/5,0)^T$，故

$$
B=
\begin{bmatrix}
-5&-4/5\\
0&-\sqrt{109}/5\\
0&0
\end{bmatrix}.
$$

矩阵只有两列，所以第一行清除第一超对角线以右元素的右反射是平凡的。

### NLA-SVA-B02

$$
\|A\|_F^2=3^2+4^2+1^2+2^2=30.
$$

$$
\|B\|_F^2=25+\frac{16}{25}+\frac{109}{25}=30.
$$

并且

$$
B^TB=
\begin{bmatrix}
25&4\\
4&5
\end{bmatrix}.
$$

其迹 $30$ 也等于奇异值平方和。

### NLA-SVA-B03

合并残差

$$
r=\sqrt{(3\times10^{-4})^2+(4\times10^{-4})^2}
=5\times10^{-4}.
$$

按分母 $\|A\|+\widehat\sigma\approx10$，尺度化指标为

$$
\eta\approx5\times10^{-5}.
$$

如果用户要求 $10^{-6}$，该候选尚不合格。

### NLA-SVA-B04

由 $r^{2t}\le10^{-6}$，

$$
t\ge\frac{\log10^{-6}}{2\log r}.
$$

- $r=0.2$：$t\ge4.29$，至少 $5$ 步；
- $r=0.8$：$t\ge30.96$，至少 $31$ 步；
- $r=0.98$：$t\ge341.92$，至少 $342$ 步。

这是方向误差主项估计；估计值误差和实际常数还与起点有关。

### NLA-SVA-B05

块宽

$$
\ell=k+p=28.
$$

值域构造顺序为

$$
\Omega\xrightarrow{A}Y_0
\xrightarrow{A^T}Z_1
\xrightarrow{A}Y_1
\xrightarrow{A^T}Z_2
\xrightarrow{A}Y_2,
$$

每箭头后正交化，合计 $3$ 次 $A$ pass、$2$ 次 $A^T$ pass。要完成随机 SVD，还需形成 $B=Q^TA$，等价于再做一次 $A^TQ$ pass；所以在不复用/缓存数据时总计 $6$ 次 pass，然后才是小矩阵 SVD。

### NLA-SVA-B06

相对第一奇异值的比例为 $0.3,0.09,0.01$。幂方案指数 $2q+1$：

| $q$ | 第二 | 第三 | 第四 |
|---:|---:|---:|---:|
| 0 | $3\times10^{-1}$ | $9\times10^{-2}$ | $10^{-2}$ |
| 1 | $2.7\times10^{-2}$ | $7.29\times10^{-4}$ | $10^{-6}$ |
| 2 | $2.43\times10^{-3}$ | $5.9049\times10^{-6}$ | $10^{-10}$ |

分离确实增强，但小方向快速接近/低于舍入和噪声尺度；若中间不 QR，它们会不可逆地被主方向吞没。

## C. 推导与证明

### NLA-SVA-C01

令 $P,R$ 正交，$B=P^TAR$。则

$$
B^TB=R^TA^TPP^TAR=R^TA^TAR.
$$

所以 $B^TB$ 与 $A^TA$ 正交相似，特征值相同，奇异值相同。Frobenius 范数由迹给出：

$$
\|B\|_F^2=\operatorname{tr}(B^TB)
=\operatorname{tr}(R^TA^TAR)
=\operatorname{tr}(A^TA)=\|A\|_F^2.
$$

### NLA-SVA-C02

对

$$
\mathcal A=\begin{bmatrix}0&A\\A^T&0\end{bmatrix}
$$

有

$$
\mathcal A\binom{u_i}{v_i}
=\binom{Av_i}{A^Tu_i}
=\sigma_i\binom{u_i}{v_i},
$$

以及

$$
\mathcal A\binom{u_i}{-v_i}
=\binom{-Av_i}{A^Tu_i}
=-\sigma_i\binom{u_i}{-v_i}.
$$

归一化可再乘 $1/\sqrt2$。零奇异值还与左右零空间产生零特征值。

### NLA-SVA-C03

忽略归一化标量，一轮先 $u\propto Av$，再

$$
v_+\propto A^Tu\propto A^TAv.
$$

令 $v_0=\sum_ic_iv_i$，则

$$
(A^TA)^tv_0=\sum_ic_i\sigma_i^{2t}v_i
=\sigma_1^{2t}\left[c_1v_1+
\sum_{i\ge2}c_i\left(\frac{\sigma_i}{\sigma_1}\right)^{2t}v_i\right].
$$

若 $c_1\ne0$ 且 $\sigma_1>\sigma_2$，非主方向以 $(\sigma_2/\sigma_1)^{2t}$ 为主衰减。

### NLA-SVA-C04

$A=U\Sigma V^T$，故

$$
AA^T=U\Sigma^2U^T.
$$

于是

$$
(AA^T)^qA\Omega
=U\Sigma^{2q}U^TU\Sigma V^T\Omega
=U\Sigma^{2q+1}V^T\Omega.
$$

因此第 $i$ 个左奇异方向 $u_i$ 的随机系数被 $\sigma_i^{2q+1}$ 加权。

### NLA-SVA-C05

对任意 $B$，

$$
A-QB=(I-QQ^T)A+Q(Q^TA-B).
$$

两项列空间分别在 $\mathcal R(Q)^\perp$ 与 $\mathcal R(Q)$，Frobenius 内积为零。因此

$$
\|A-QB\|_F^2
=\|(I-QQ^T)A\|_F^2+\|Q^TA-B\|_F^2.
$$

第二项在 $B=Q^TA$ 时唯一取最小零值，最小误差即投影误差。

### NLA-SVA-C06

$A^TA$ 的非零特征值为 $\sigma_i^2$，故

$$
\kappa_2(A^TA)=\frac{\sigma_1^2}{\sigma_n^2}=\kappa_2(A)^2.
$$

$\kappa(A)=10^8$ 时平方为 $10^{16}$；双精度 $u\approx10^{-16}$ 给 $u\kappa(A^TA)\approx1$。这意味着最小方向可能完全处于舍入放大尺度，不能期待正规方程保留其相对精度；而直接 SVD 的后向稳定路径避免先人为平方问题难度。

## D. 边界、反例与纠错

### NLA-SVA-D01

显式 $A^TA$：条件数平方；点积形成阶段会对小差异发生消去；稀疏图二跳连接导致填充；只得到右向量，恢复 $u=Av/\sigma$ 时小 $\sigma$ 放大误差；还失去直接利用矩形结构的机会。对只求最大奇异值，可隐式交替 $A,A^T$；对全谱用稳定库 SVD；对部分谱用 Golub–Kahan。

### NLA-SVA-D02

取 $A=I_2$。$\sigma_1=\sigma_2=1$，任意单位向量 $v$ 都是右奇异向量，$u=v$。幂迭代每步保持初始方向，微小扰动会选择不同方向；不存在应收敛到的唯一“第一列”。但谱范数

$$
\|A\|_2=1
$$

仍是唯一标量，顶端二维奇异子空间也是稳定对象。

### NLA-SVA-D03

增大 $q$ 每次增加一对 $A^T,A$ passes 与 QR，成本和通信上升；幂权重会把小方向压到舍入地板，若不频繁正交便丢失秩；数据噪声中的主模也会被强化；时变/流式数据还可能在多 pass 间不一致。因此 $q$ 应通过目标误差与 pass 预算选择，常为小整数，并以实际投影误差验证。

### NLA-SVA-D04

一个小 Frobenius 重构误差可隐藏：单个三元组不满足方程、$U/V$ 不正交、谱范数尾误差很大、随机运行不稳定或迭代未收敛。还应报告双侧残差、$U^TU-I,V^TV-I$、谱范数与 Frobenius 误差、奇异值排序/非负性、随机种子/置信性、数据 passes、停止标志；若关心子空间，再报主角或投影差。

### NLA-SVA-D05

阈值必须有单位与尺度。可从

$$
\tau=c\,u\,\max(m,n)\sigma_1
$$

得到舍入基线，再与观测噪声范数、下游允许误差和显著 gap 比较。例如矩阵整体乘 $10^9$ 后，固定 $10^{-6}$ 会改变“秩”但数学相对结构不变。无 gap 时应报告阈值—秩曲线或有效秩，而非唯一真值。

## E. AI 迁移

### NLA-SVA-E01

持久化单位右向量 $v$。每个训练步执行

$$
u\leftarrow Wv/\|Wv\|,\qquad
v\leftarrow W^Tu/\|W^Tu\|,\qquad
\widehat\sigma=u^TWv.
$$

warm start 追踪缓慢变化的主方向。它通常低估尚未收敛的 $\sigma_1$，小 gap、权重突变、零向量或低精度会恶化。可每隔若干步做多步/块 Lanczos 校准，监控双侧残差、估计跳变和 $\|Wv\|=0$，并明确归一化使用的是估计值。

### NLA-SVA-E02

以宽度至少 $3+p$ 的随机右块开始，交替用 JVP 得 $JV$、QR 得左块 $U$，VJP 得 $J^TU$、QR 得右块；可组织为块 Golub–Kahan/子空间迭代并对小投影做 SVD。对每个候选检查

$$
r_{u,i}=Jv_i-\sigma_i u_i,\qquad
r_{v,i}=J^Tu_i-\sigma_i v_i.
$$

同时报告块正交缺陷、随机种子、谱隙和 JVP/VJP 一致性；若自动微分算子含随机状态，应固定状态。

### NLA-SVA-E03

离线验收三层：

1. 矩阵层：$\|W-\widetilde W\|_2,\|\cdot\|_F$、双侧残差和秩；
2. 层输出层：在校准/留出激活 $X$ 上比较 $\|XW-X\widetilde W\|$，覆盖真实输入分布；
3. 任务层：端到端准确率、损失、鲁棒性与延迟/内存。

截断 SVD 只保证第一层的无约束最佳 rank-$k$ 近似，不自动保证后两层。

### NLA-SVA-E04

Eckart–Young–Mirsky 保证：对固定权重差或目标矩阵 $\Delta W$，截断 SVD 在二范数与所有酉不变范数（包括 Frobenius）下给出最佳 rank-$k$ 静态近似。用其拆成 $BA$ 可作为 LoRA 初始化。

它不保证后续非凸训练收敛更快、不保证最终验证损失最优，也不纳入优化器、数据曲率、正则化或参数化缩放。随机初始化可能给探索自由度；SVD 初始化给较好静态起点，需实验比较。

### NLA-SVA-E05

单个奇异向量在符号/相位上不唯一；$\sigma_i\approx\sigma_j$ 时列可在子空间内任意旋转，导数含 $(\sigma_i^2-\sigma_j^2)^{-1}$；截断边界的排序交换不光滑；固定步算法梯度又是算法输出而非精确 SVD 导数。

更稳定的目标可依赖

$$
P_U=U_kU_k^T,\qquad P_V=V_kV_k^T
$$

或低秩重构 $U_k\Sigma_kV_k^T$，并在 $\sigma_k-\sigma_{k+1}$ 太小时对整个谱簇处理、使用软谱滤波或停止对不稳定列反传。

## 验收清单

- [x] 25 题均有完整答案；
- [x] 双对角手算、Frobenius 与 $B^TB$ 相互校验；
- [x] 幂迭代、随机幂和最佳投影均有推导；
- [x] 反例覆盖重根、正规方程、数值秩和随机 pass；
- [x] AI 题区分静态矩阵、层输出与端到端承诺。
