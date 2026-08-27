---
type: solution
status: draft
area: [math/numerical-linear-algebra]
topic: "[[Hessenberg 化与 QR 特征值算法]]"
exercise: "[[习题 - Hessenberg 化与 QR 特征值算法]]"
related: ["[[实验 - Hessenberg 约化、移位与 QR deflation]]", "[[Schur 分解]]", "[[Householder 与 Givens 变换]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - Hessenberg 化与 QR 特征值算法

> [!important] 使用方式
> 先写出自己的相似变换、残差或反例，再对照本页。只记住“先 Hessenberg、再 QR”还不够；真正的掌握标准是能解释为什么保持特征值、为什么每步只需 $O(n^2)$、何时可以 deflate，以及算法失败时哪些结果仍然有效。

## A. 识别与复述

### NLA-HQR-A01

1. **上 Hessenberg 矩阵**：$H=(h_{ij})$ 满足 $h_{ij}=0$（$i>j+1$）。也就是第一条次对角线以下全为零。它是一般稠密矩阵进入 QR 特征值迭代前的标准结构。
2. **未约化 Hessenberg 矩阵**：除 Hessenberg 条件外，所有次对角元 $h_{i+1,i}$ 都非零。若某个次对角元为零，矩阵已可分成两个较小的块上三角问题。
3. **实 Schur 形式**：实矩阵 $A$ 可写成 $A=QTQ^T$，$Q$ 正交，$T$ 为准上三角矩阵；其对角块为 $1\times1$ 实特征值块或表示复共轭对的 $2\times2$ 实块。它是实 QR 算法的正确终点。
4. **deflation**：当某个次对角元相对邻近尺度足够小时，把它置零并把问题分裂为两个子问题。它负责把“渐近收敛”变成可结束的有限计算。
5. **bulge chasing**：隐式移位在 Hessenberg 带宽外产生一个小“鼓包”，再用一串局部正交相似变换把鼓包沿矩阵向下追赶并排出。它让移位 QR 保持 Hessenberg 结构和 $O(n^2)$ 单步复杂度。

算法链为

$$
A\xrightarrow{\text{双侧 Householder}}H
\xrightarrow{\text{隐式移位与 bulge chasing}}H_k
\xrightarrow{\text{deflation}}T.
$$

### NLA-HQR-A02

| 对象 | 输入输出等式 | 目的 |
|---|---|---|
| 一次 QR 分解 | $A=QR$ | 把一个矩阵分成正交因子与上三角因子 |
| 无移位 QR 迭代 | $A_k=Q_kR_k$，$A_{k+1}=R_kQ_k$ | 通过正交相似逐步逼近 Schur 形式 |
| 移位 QR 迭代 | $A_k-\mu_kI=Q_kR_k$，$A_{k+1}=R_kQ_k+\mu_kI$ | 用接近尾部特征值的移位加速 deflation |
| Hessenberg 约化 | $H=U^TAU$，$U$ 正交，$H$ 上 Hessenberg | 一次性支付 $O(n^3)$，把以后每个 QR 步降为 $O(n^2)$ |

关键区别是：QR **分解**只是因子分解；QR **迭代**把因子次序反转，从而形成相似变换；Hessenberg **约化**必须左右同时变换，不能只做左消元。

### NLA-HQR-A03

- `DGEHRD` 用正交相似变换把实一般矩阵约化为上 Hessenberg 形式。反射向量紧凑存入输入数组的下三角部分，`TAU` 保存反射系数；若需要显式 $Q$，还要由相应生成例程构造。
- `DHSEQR` 在 Hessenberg 矩阵上做 QR 迭代，计算全部特征值，并可选计算 Schur 形式和 Schur 向量。
- `COMPZ='N'`：不需要 Schur 向量；`'I'`：从单位阵开始累计 QR 变换，得到 Hessenberg 矩阵的 Schur 向量；`'V'`：把已有约化矩阵 $Q$ 继续右乘 QR 变换，最终得到原矩阵的 Schur 向量。
- `INFO>0` 表示并非所有特征值都收敛。调用者不能把全部输出标记为成功；必须报告 `INFO`、已收敛区间、未收敛活动块、迭代/容差信息，并只把文档保证有效的输出作为可信结果。

## B. 手算与构造

### NLA-HQR-B01

令 $x=(3,4)^T$。题给方向要求 $Px=(-5,0)^T$，可取

$$
P=
\begin{bmatrix}
-0.6&-0.8\\
-0.8&0.6
\end{bmatrix}.
$$

直接检查 $P^T=P$、$P^TP=I$，且

$$
P\begin{bmatrix}3\\4\end{bmatrix}
=\begin{bmatrix}-5\\0\end{bmatrix}.
$$

嵌入

$$
U=1\oplus P=
\begin{bmatrix}
1&0&0\\
0&-0.6&-0.8\\
0&-0.8&0.6
\end{bmatrix}.
$$

先左乘：

$$
U^TA=
\begin{bmatrix}
1&2&3\\
-5&-7.2&-8.6\\
0&0.4&0.2
\end{bmatrix}.
$$

再右乘：

$$
H=U^TAU=
\begin{bmatrix}
1&-3.6&0.2\\
-5&11.2&0.6\\
0&-0.4&-0.2
\end{bmatrix}.
$$

因此 $h_{31}=0$。同时

$$
\operatorname{tr}(H)=1+11.2-0.2=12
=\operatorname{tr}(A),
$$

这正是相似变换保持迹的具体检查。有限精度实现还应检查 $\|U^TU-I\|$ 与 $\|AU-UH\|$。

### NLA-HQR-B02

第一列 $(2,1)^T$ 的归一化给出

$$
Q=\frac1{\sqrt5}
\begin{bmatrix}
2&-1\\
1&2
\end{bmatrix},
$$

其中第二列符号选得使 $R$ 对角为正。于是

$$
R=Q^TA_0=
\begin{bmatrix}
\sqrt5&4/\sqrt5\\
0&3/\sqrt5
\end{bmatrix}.
$$

反转因子次序：

$$
A_1=RQ=
\begin{bmatrix}
14/5&3/5\\
3/5&6/5
\end{bmatrix}.
$$

因为 $A_0=QR$，

$$
Q^TA_0Q=Q^T(QR)Q=RQ=A_1.
$$

不变量检查：

$$
\operatorname{tr}(A_1)=4=\operatorname{tr}(A_0),
\qquad
\det(A_1)=3=\det(A_0).
$$

注意非对角元只从 $1$ 降到 $0.6$；QR 迭代通常需要多步，而不是一次完成对角化。

### NLA-HQR-B03

特征多项式为

$$
\lambda^2-4\lambda+2.84=0,
$$

故

$$
\lambda_{\pm}=2\pm\sqrt{1.16}
\approx3.07703296,\;0.92296704.
$$

Wilkinson 稳定公式令

$$
\delta=\frac{a-d}{2}=1,
\qquad
\mu=d-\frac{b^2}{\delta+\operatorname{sign}(\delta)
\sqrt{\delta^2+b^2}}.
$$

代入 $d=1,b=0.4$：

$$
\mu=1-\frac{0.16}{1+\sqrt{1.16}}
\approx0.92296704.
$$

它确实是离尾对角元 $d=1$ 更近的特征值。分母写成上式是为了避免在 $\delta$ 很大时发生灾难性消去。

### NLA-HQR-B04

阈值为

$$
100u(|h_{11}|+|h_{22}|)
=100(1.1\times10^{-16})(1+4)
=5.5\times10^{-14}.
$$

因为 $10^{-14}<5.5\times10^{-14}$，所以按该简化判据可以 deflate。

若整体乘 $10^{12}$，左边变为 $10^{-2}$，右边也乘 $10^{12}$，变为 $5.5\times10^{-2}$，判断不变。这说明判据比较的是相对于局部矩阵尺度的扰动，而不是依赖单位的绝对数值。

### NLA-HQR-B05

特征多项式为

$$
(1-\lambda)^2+4=0,
$$

所以特征值是 $1\pm2i$。实上三角矩阵的对角元必为实数，因此不可能在实数域内把这个矩阵正交相似为纯上三角且仍保留这对非实特征值。实 Schur 形式允许保留原来的 $2\times2$ 块，由该块的迹与行列式编码复共轭对。这不是“尚未收敛”，而是实数算术下的正确终态。

### NLA-HQR-B06

代理比值为

$$
\frac{n^3}{6n^2}=\frac n6.
$$

因此

| $n$ | 比值 $n/6$ |
|---:|---:|
| 64 | $10.67$ |
| 256 | $42.67$ |
| 1024 | $170.67$ |

它只展示数量级随 $n$ 的增长，不是某个实现的精确测速：真实常数受双移位、多移位、缓存、分块、并行通信、AED 和所求输出（仅特征值或还要向量）影响。可靠结论是“约化后每个结构化 QR 步从三次降为二次”，而不是“必然快恰好 $n/6$ 倍”。

## C. 推导与证明

### NLA-HQR-C01

由

$$
A_k-\mu I=QR
$$

及 $Q^TQ=I$，有

$$
\begin{aligned}
Q^TA_kQ
&=Q^T(QR+\mu I)Q\\
&=RQ+\mu Q^TQ\\
&=RQ+\mu I\\
&=A_{k+1}.
\end{aligned}
$$

所以每一步都是正交相似变换，精确算术下保持特征多项式、迹、行列式和全部特征值。移位改变收敛速度，不改变目标谱。

### NLA-HQR-C02

在第 $k$ 步，前 $k-1$ 列已经满足 Hessenberg 结构。取

$$
U_k=I_k\oplus P_k,
$$

其中 $P_k$ 只作用于坐标 $k+1,ldots,n$。

- 左乘 $U_k^T$ 只混合第 $k+1$ 行及其以下各行，用来把第 $k$ 列中 $k+2,ldots,n$ 行消成零。
- 对任意先前列 $j<k$，其在这些行上本来已经全为零；零向量经 $P_k$ 混合仍是零，因此旧结构不被破坏。
- 右乘 $U_k$ 是恢复相似性的必要配对操作。它只混合后部各列，不会改变前 $k$ 列的位置关系。

因此双侧更新 $A\leftarrow U_k^TAU_k$ 同时完成“制造新零”和“保持全部旧零”。

### NLA-HQR-C03

设 $H=QR$，其中 $Q=G_1^T\cdots G_{n-1}^T$，每个 $G_i$ 只在相邻行 $i,i+1$ 上作用并依次消去 $h_{i+1,i}$。由于 $H$ 只有一条次对角线，消去第 $i$ 个次对角元时不会出现更深的非零，最终 $R$ 上三角。

现在看

$$
RQ=RG_1^T\cdots G_{n-1}^T.
$$

右乘 $G_i^T$ 只混合相邻列 $i,i+1$。对上三角 $R$ 而言，第一次混合至多在 $(i+1,i)$ 位置产生一个非零；按从上到下的乘积继续作用时，这个局部非零被向下传递，却不会越过第一条次对角线。因此最终 $RQ$ 仍为上 Hessenberg。

等价地，由 $RQ=Q^THQ$ 与相邻旋转的嵌套支撑，可以证明第 $j$ 列落在 $\operatorname{span}(e_1,\ldots,e_{j+1})$ 中，这正是 Hessenberg 条件。

### NLA-HQR-C04

正交迭代满足

$$
AZ_k=Z_{k+1}R_{k+1},\qquad Z_0=I.
$$

令 $T_k=Z_k^TAZ_k$。则

$$
T_k=Z_k^TZ_{k+1}R_{k+1}.
$$

由于 $Z_k^TZ_{k+1}$ 正交，而 $R_{k+1}$ 上三角，在固定正对角符号约定下，这就是 $T_k$ 的唯一 QR 分解：

$$
T_k=\widetilde Q_kR_{k+1},
\qquad
\widetilde Q_k=Z_k^TZ_{k+1}.
$$

QR 迭代的下一矩阵为

$$
\begin{aligned}
R_{k+1}\widetilde Q_k
&=R_{k+1}Z_k^TZ_{k+1}\\
&=Z_{k+1}^TAZ_kZ_k^TZ_{k+1}\\
&=Z_{k+1}^TAZ_{k+1}\\
&=T_{k+1}.
\end{aligned}
$$

基例 $T_0=A$，故归纳得两列矩阵序列一致。QR 迭代可以理解为“把正交迭代换到不断更新的坐标系里”。

### NLA-HQR-C05

若把 $h_{i+1,i}$ 置零，相当于把原矩阵 $H$ 改为 $H+E$，其中

$$
E=-h_{i+1,i}e_{i+1}e_i^T.
$$

它只有一个非零元素，所以

$$
\|E\|_F=|h_{i+1,i}|.
$$

若

$$
|h_{i+1,i}|\lesssim u(|h_{ii}|+|h_{i+1,i+1}|),
$$

则“置零”可解释为对输入施加一个机器精度量级、与局部尺度相称的扰动。算法随后精确求解这个邻近问题，因此 deflation 判据本质上是局部后向误差判定。实际库会加入更稳健的安全检查，不能把上式当作所有实现的唯一细节。

### NLA-HQR-C06

给定计算结果 $\widehat Q,\widehat T$，定义归一化 Schur 后向残差

$$
\eta_{\mathrm{Schur}}
=\frac{\|A-\widehat Q\widehat T\widehat Q^T\|_F}
{\|A\|_F}.
$$

还可报告分量缩放版本

$$
\eta_{\mathrm{scaled}}
=\frac{\|A-\widehat Q\widehat T\widehat Q^T\|_F}
{n u\|A\|_F},
$$

其中 $n$ 是阶数、$u$ 是单位舍入误差；它帮助判断误差是否处在合理的 $O(nu)$ 量级。

必须单独报告

$$
\eta_Q=\|\widehat Q^T\widehat Q-I\|_F,
$$

因为小重构残差本身不能保证 $\widehat Q$ 真正正交。例如病态、缩放不当或错误累计变换可能让两个误差来源互相抵消。还应检查 $\widehat T$ 的准上三角结构残差和 `INFO`。

## D. 边界、反例与纠错

### NLA-HQR-D01

取

$$
A=\begin{bmatrix}1&0\\0&2\end{bmatrix},
\qquad
U=\begin{bmatrix}0&1\\1&0\end{bmatrix}.
$$

只左乘得到

$$
U^TA=\begin{bmatrix}0&2\\1&0\end{bmatrix}.
$$

其迹为 $0$，而 $A$ 的迹为 $3$；其特征值为 $\pm\sqrt2$，也不是 $1,2$。双侧变换则为

$$
U^TAU=\begin{bmatrix}2&0\\0&1\end{bmatrix},
$$

仍有迹 $3$、特征值集合 $\{1,2\}$。左乘是改变坐标表示的一半；只有左右配对才是相似变换。

### NLA-HQR-D02

设 $|h_{i+1,i}|=10^{-13}$。绝对阈值 $10^{-12}$ 会判定可 deflate；把整个矩阵乘 $10^6$ 后，该元素变成 $10^{-7}$，又判定不可 deflate。两矩阵只差单位尺度，却得到相反结论。

尺度感知形式应类似

$$
|h_{i+1,i}|\le c u
\bigl(|h_{ii}|+|h_{i+1,i+1}|\bigr),
$$

并配合安全最小数和邻近元素检查。整体缩放时两边同比例变化，判断保持不变。

### NLA-HQR-D03

取平面旋转

$$
A=\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

其特征值为 $\pm i$。若它能经实正交相似变为实上三角矩阵，那么特征值必须等于该三角矩阵的实对角元，产生矛盾。正确目标是实 Schur 准上三角形式，允许这个不可约 $2\times2$ 块；若使用复数算术，才可得到复上三角 Schur 形式。

### NLA-HQR-D04

对 $\lambda_1=1$，可取 $v_1=(1,0)^T$。对 $\lambda_2=1+\varepsilon$，解

$$
\begin{bmatrix}-\varepsilon&1\\0&0\end{bmatrix}v_2=0
$$

得 $v_2=(1,\varepsilon)^T$，归一化后

$$
\widehat v_2=\frac{(1,\varepsilon)^T}{\sqrt{1+\varepsilon^2}}.
$$

两向量夹角的正弦约为 $|\varepsilon|$，故 $\varepsilon\to0$ 时近乎平行，特征向量矩阵条件数发散。后向稳定只保证计算结果是某个 $A+E$ 的精确谱数据，$\|E\|$ 很小；当问题本身的特征向量映射条件数巨大时，小 $E$ 仍能造成大的前向方向变化。这不是算法失稳，而是问题敏感。

### NLA-HQR-D05

`INFO=37` 不能包装成“全部成功”。程序至少应：

1. 保留原始 `INFO=37` 与例程名、矩阵阶数、活动索引区间；
2. 按例程文档区分哪些 `WR/WI` 已收敛、哪些未得到保证；
3. 若请求了 Schur 形式/向量，说明相应输出的有效范围；
4. 保存平衡、缩放、容差、最大迭代数和后端版本等可复现元数据；
5. 对可信子集计算残差，对未收敛块给出范数、次对角元轨迹或重试策略；
6. 向上层返回“部分收敛”状态，而非伪造完整成功。

核心契约是：失败状态也是数值结果的一部分，不能被接口吞掉。

## E. AI 与科学计算迁移

### NLA-HQR-E01

Arnoldi 关系可拆为

$$
AQ_k=Q_kH_k+h_{k+1,k}q_{k+1}e_k^T.
$$

若 $H_ky=\theta y$，Ritz 向量 $v=Q_ky\in\mathbb R^n$，则

$$
Av-\theta v
=h_{k+1,k}q_{k+1}(e_k^Ty).
$$

所以残差是 $n$ 维向量，却只沿新方向 $q_{k+1}$；其范数为

$$
\|Av-\theta v\|_2
=|h_{k+1,k}|\,|e_k^Ty|.
$$

大矩阵只通过矩阵—向量积进入 Arnoldi；昂贵的 Schur/QR 只对 $k\times k$ 的 $H_k$ 进行。若 $k\ll n$，这把稠密 $O(n^3)$ 谱分解变成 Krylov 构造加小型稠密问题。

### NLA-HQR-E02

一条可审计的 DMD 链是：

1. 对 $X=U_r\Sigma_rV_r^T$ 做带截断的 SVD，并用奇异值、残差或验证集选择 $r$；
2. 构造低维算子
   $$
   \widetilde A=U_r^TYV_r\Sigma_r^{-1};
   $$
3. 求实 Schur 分解 $\widetilde A=STS^T$，优先分析不变子空间而非脆弱的单个特征向量；
4. 将 Schur 子空间提升回状态空间 $U_rS$，用一步/多步预测残差、子空间残差和正交缺陷验收；
5. 报告截断阈值、谱间隙、条件数代理以及重采样稳定性。

非正规时，即便所有特征值都在单位圆内，$\|\widetilde A^k\|$ 仍可能先剧烈增长；模态可能高度非正交。因此还应看 Schur 上三角耦合、瞬态放大、伪谱或 resolvent，而不能只读特征值模长。

### NLA-HQR-E03

对投影 $H=Q_k^TJQ_k$，小型实 Schur 分解给出正交基和可排序的不变子空间。相较显式特征向量，它避免把近重或近缺陷特征值强行拆成极敏感的单方向，也让残差

$$
\|J(Q_kS)-(Q_kS)T\|
$$

可以直接验证。

但谱半径 $\rho(J)<1$ 只描述渐近离散稳定性。非正规 $J$ 可有 $\|J^t\|\gg1$ 的短期放大，使梯度、扰动或状态先爆发。完整报告应再包含 $\|J^t\|$ 的有限时域估计、Schur 非对角耦合、数值半径或 resolvent 代理。

### NLA-HQR-E04

Schur 路线先写 $A=QTQ^*$，再计算

$$
e^A=Qe^TQ^*.
$$

正交/酉变换条件良好，而三角或准三角 $T$ 适合用缩放—平方与 Padé、分块递推等稳定算法；这比显式 $A=V\Lambda V^{-1}$ 避免了病态 $V$。

反向传播时必须记录：

- 聚簇或重根会使单个 Schur 向量/特征向量的导数不唯一或巨大；
- 重排 Schur 块需要足够的谱分离，否则 Sylvester 方程病态；
- 实 $2\times2$ 块要作为整体传播，不能任意拆开共轭对；
- 前向残差小不推出梯度条件良好，应报告谱分离或 Fréchet 导数范数代理；
- 若损失只依赖 $e^A$，应优先对矩阵函数本身求 Fréchet 导数，避免穿过非唯一的中间分解坐标。

### NLA-HQR-E05

评审结论：教学原型可以保留，但不能把“每步 dense QR + RQ”当作生产 eigensolver。最小可接受方案应覆盖：

1. **复杂度**：先一次 $O(n^3)$ 约化；后续每步应为 $O(n^2)$，不能反复支付 dense QR 的 $O(n^3)$。
2. **Hessenberg**：用双侧 Householder 约化，并紧凑存储反射器；对称输入则进一步利用三对角结构。
3. **移位**：至少支持稳健单/双移位和 exceptional shift；实矩阵复共轭对用 Francis 双移位保持实算术。
4. **AED/deflation**：采用尺度感知 deflation；大规模实现应有 aggressive early deflation 与多移位窗口，而不是只盯最后一个次对角元。
5. **状态**：暴露迭代次数、活动块、部分收敛、`INFO`、NaN/Inf、后端和容差；不能静默返回。
6. **验证**：报告 Schur 重构残差、正交缺陷、准上三角结构、已收敛块残差，并与成熟供应商库和困难矩阵集交叉验证。

GPU 性能还取决于批量矩阵大小、内存通信和分块内核。通常应优先调用经过测试的供应商库，把手写代码用于教学、特定小矩阵批处理或明确的研究假设。

## 常见错误模式

- 把 $U^TA$ 当成相似变换，忘了右乘 $U$；
- 每次在稠密矩阵上重新 QR，却没有先约化为 Hessenberg；
- 把复共轭 $2\times2$ 实 Schur 块误判成未收敛；
- 用绝对阈值 deflate，导致结果依赖量纲；
- 只报告特征值，不报告 `INFO`、残差与正交缺陷；
- 把后向稳定误解成非正规特征向量必然前向准确；
- 只凭谱半径判断短时间动力学或梯度传播。

## 无提示重做

闭卷时至少应能重新完成：

1. 从 $A_k-\mu I=QR$ 推出 $A_{k+1}=Q^TA_kQ$；
2. 手算 `B01` 的双侧 Householder 更新；
3. 解释 Hessenberg 结构如何把 QR 单步降至 $O(n^2)$；
4. 写出相对 deflation 判据及其后向误差解释；
5. 区分“Schur 后向残差小”和“单个非正规特征向量前向准确”。

返回：[[习题 - Hessenberg 化与 QR 特征值算法]] · [[Hessenberg 化与 QR 特征值算法]]
