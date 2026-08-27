---
type: solution
status: draft
area: [math/numerical-linear-algebra, math/randomized-linear-algebra]
topic: "[[随机化低秩近似与随机 SVD]]"
exercise: "[[习题 - 随机化低秩近似与随机 SVD]]"
prerequisites: ["[[奇异值分解]]", "[[SVD 算法与谱范数估计]]"]
related: ["[[实验 - 随机 SVD 的过采样、幂步与概率证书]]", "[[有效秩]]"]
sources: ["[[S-2011-Halko-Martinsson-Tropp-随机低秩]]", "[[S-2020-Martinsson-Tropp-随机数值线性代数]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - 随机化低秩近似与随机 SVD

> [!warning] 概率纪律
> 期望、某个 seed 的观测、跨 seed 经验分位数和带名义失败概率的后验证书是四种不同陈述；以下解答始终标明所用层级。

## A. 识别与复述

### NLA-RLA-A01

Stage A 构造 \(Q\)，使 \(A\approx QQ^TA\)，解决“主要值域在哪里”；Stage B 对 \(B=Q^TA\) 做小型确定性分解并提升回原空间。经典 Gaussian randomized SVD 的核心随机性位于 Stage A；后验验证另用独立随机性。

### NLA-RLA-A02

- \(k\)：最终希望保留的 rank；
- \(p\)：额外采样维数，用于降低漏方向和病态风险；
- \(\ell=k+p\)：值域基的工作维数；
- \(q\)：幂方案次数，用额外 pass 放大谱隙。

\(p\) 增加横向冗余，\(q\) 增加纵向迭代深度，二者成本与作用不同。

### NLA-RLA-A03

谱范数看最坏输入方向；Frobenius 范数累计所有方向能量；子空间角看近似/真实主子空间是否对齐，在谱簇中应比较整个子空间；下游误差看任务对被删方向的敏感性。一个指标小不能普遍推出其余指标小。

### NLA-RLA-A04

Gaussian 旋转不变且理论简洁，但 sketch 稠密；Rademacher 生成便宜但保证常数不同；SRHT 借快速变换降低乘法成本，却有维度/padding/coherence 约束；CountSketch 能保持输入稀疏并流式更新，但常需更大 sketch 维数。

### NLA-RLA-A05

truncated SVD 因子为抽象标准正交奇异向量，给任意矩阵的最佳酉不变范数低秩近似；Nyström 面向 PSD/核矩阵并保持 \(CW^\dagger C^T\) 结构；CUR 用真实列和行；ID 用真实列子集插值其余列，解释性更强。

## B. 手算与构造

### NLA-RLA-B01

$$
Y=A\Omega=(5,2,0)^T,\qquad
Q=\frac1{\sqrt{29}}(5,2,0)^T.
$$

在前两维，

$$
P=QQ^T=\frac1{29}
\begin{bmatrix}25&10\\10&4\end{bmatrix}.
$$

所以

$$
(I-P)A
=
\frac1{29}
\begin{bmatrix}
20&-20\\
-50&50
\end{bmatrix}
\oplus[1].
$$

二维部分是外积

$$
\frac1{29}(2,-5)^T(10,-10),
$$

其唯一非零奇异值为

$$
\frac{\sqrt{29}\sqrt{200}}{29}
=\sqrt{\frac{200}{29}}
\approx2.626.
$$

与第三方向残差 \(1\) 比较，故总谱误差约 \(2.626\)。目标 rank-1 最优误差本为 \(2\)，单个随机方向尚未达到最优。

### NLA-RLA-B02

$$
Y=
\begin{bmatrix}
5&0\\2&2\\0&1
\end{bmatrix}
$$

两列线性无关，值域维数为 \(2\)。同时正交于 \((5,2,0)^T\) 和 \((0,2,1)^T\) 的向量可取

$$
z=(2,-5,10)^T,
\qquad \widehat z=z/\sqrt{129}.
$$

投影补空间是一维，因此

$$
(I-QQ^T)A=\widehat z\widehat z^TA
$$

且

$$
\|(I-QQ^T)A\|_2
=\|\widehat z^TA\|_2
=\sqrt{\frac{100+100+100}{129}}
=\sqrt{\frac{100}{43}}
\approx1.525.
$$

### NLA-RLA-B03

最佳 rank-2 谱误差：

$$
\sigma_3=2.
$$

Frobenius 误差：

$$
\sqrt{2^2+1^2+0.5^2}
=\sqrt{5.25}\approx2.291.
$$

\(q=1\) 后奇异值变为三次幂：

$$
[1000,125,8,1,0.125].
$$

### NLA-RLA-B04

上界为

$$
10\sqrt{\frac2\pi}(0.012)
\approx0.09575.
$$

名义失败概率为

$$
10^{-6}.
$$

这是对固定 \(R\)、独立 Gaussian 探针的概率陈述。

### NLA-RLA-B05

\(\ell=50\)。形成 \(A\Omega\) 约

$$
O(mn\ell)=O(10^6\cdot10^4\cdot50)
=O(5\times10^{11})
$$

次标量工作；正交化约

$$
O(m\ell^2)=O(2.5\times10^9).
$$

完整 SVD 在 \(m\gg n\) 时主量级约 \(O(mn^2)=O(10^{14})\)。当只需 \(k\ll n\)、少数 pass 可承受且谱有可利用低秩结构时，随机路线有数量级优势；若最终仍需全部奇异向量，则优势消失。

## C. 推导与证明

### NLA-RLA-C01

由定义

$$
QB=Q(Q^TA)=QQ^TA.
$$

若 \(Q^TQ=I\)，则

$$
P^T=(QQ^T)^T=QQ^T,
$$

$$
P^2=QQ^TQQ^T=QQ^T=P.
$$

对称且幂等，所以 \(P=QQ^T\) 是到 \(\mathcal R(Q)\) 的正交投影。

### NLA-RLA-C02

- \(\Sigma_2\)：最佳 rank-\(k\) 之外不可避免的谱尾；
- \(\Omega_2\)：随机探针在尾部右奇异子空间中的分量；
- \(\Omega_1^\dagger\)：从主子空间随机坐标恢复主方向所需的放大。

若 \(\Omega_1\) 近秩亏，伪逆很大，尾部污染被放大；过采样主要改善这一风险。

### NLA-RLA-C03

由 \(A=U\Sigma V^T\)：

$$
AA^T=U\Sigma^2U^T.
$$

于是

$$
(AA^T)^qA
=U\Sigma^{2q}U^TU\Sigma V^T
=U\Sigma^{2q+1}V^T.
$$

大动态范围使弱方向在连续乘法中被舍入吞没。交替乘 \(A,A^T\) 后正交化，可把各方向重新缩放到可表示范围并防止基向量塌缩到首个方向。

### NLA-RLA-C04

任意列空间含于 \(\mathcal R(Q)\) 的候选可写为 \(QX\)。分解

$$
A=QQ^TA+(I-QQ^T)A.
$$

两部分列空间正交，因此对 Frobenius 范数

$$
\|A-QX\|_F^2
=\|(I-QQ^T)A\|_F^2+\|Q(Q^TA-X)\|_F^2.
$$

又因 \(Q\) 等距，

$$
\|Q(B-X)\|_F=\|B-X\|_F.
$$

第一项与 \(X\) 无关，故由 Eckart–Young–Mirsky 定理，对 \(B\) 取最佳 Frobenius 范数 rank-\(k\) 截断即可。谱范数下仍可由该构造得到标准误差界，但上述平方可加证明不能原样照搬成“受限问题的唯一最优性”证明。

### NLA-RLA-C05

\(\alpha=10\) 时失败上界 \(10^{-r}\)。要求

$$
10^{-r}\le10^{-9}
$$

故最少 \(r=9\)。它仍不是确定性证书，因为存在概率至多 \(10^{-9}\) 的探针全部错过近最大放大方向；同时结论还依赖 Gaussian、独立性和固定 \(R\) 的假设。

## D. 边界、反例与纠错

### NLA-RLA-D01

概率 \(1\) 满秩只是说 \(\det\Omega_1\ne0\) 几乎处处，不控制最小奇异值离零多远。\(p=0\) 时 \(\Omega_1^\dagger\) 可能很大，误差分布有长尾；\(p>0\) 的矩形冗余改善典型条件性并吸收尾部。

### NLA-RLA-D02

取

$$
A=I_n
$$

或奇异值全部等于 \(1\) 的正交矩阵。任何 rank-\(k<n\) 近似的最佳谱误差都是 \(1\)，Frobenius 最佳误差是 \(\sqrt{n-k}\)。随机算法给出相同量级不是失败，而是数据不存在更好的低秩结构。

### NLA-RLA-D03

显式 \(AA^T\)：

- 可能把稀疏矩阵变稠；
- 平方条件数；
- 需要巨大存储；
- 丢失只需 matvec 的 operator 接口。

显式矩阵幂进一步放大动态范围和舍入。正确实现用 \(A\) 与 \(A^T\) 交替作用，并在中间重正交。

### NLA-RLA-D04

构造阶段已选择 \(Q\) 使同一批 \(\Omega\) 的投影残差小，因此这些方向不是独立抽样，估计向乐观偏。修正为：冻结 \(Q\)，生成全新 seed 的 Gaussian 探针；预先设定 \(\alpha,r\)，再一次性计算证书，不按验证结果反复调参而不重置概率预算。

### NLA-RLA-D05

至少缺少：

1. 谱范数或最坏方向误差；
2. 与最佳 rank-\(k\) 误差的比值；
3. \(k,p,q\)；
4. pass 和总时间/内存；
5. \(Q\) 的正交缺陷；
6. 多 seed 中位数、分位数、最坏值；
7. 失败阈值和频率；
8. 独立后验证书；
9. dtype 与重正交；
10. 下游任务与分布外表现。

## E. AI 迁移

### NLA-RLA-E01

先明确全局均值：分布式/流式中心化必须用一致统计量，不能每 shard 各自中心化后混同。比较确定性小基线与不同 \(p,q\)，报告：

- explained variance ratio 与 hold-out 重构；
- 投影谱/Frobenius 误差；
- 真主子空间可得时的 principal angles；
- 多 seed 分位数；
- pass、通信、峰值内存和时间；
- 数据顺序/漂移下的稳定性；
- 独立残差探针。

### NLA-RLA-E02

随机 SVD 初始化能说明：初始低秩因子逼近了所分析矩阵的主子空间。它不能证明训练更新始终低秩、这些方向对任务最优，或优化一定更快。

公平对照固定 rank、参数量、缩放、优化器、训练预算和 seed 集合；比较初始函数扰动、收敛曲线、最终质量、更新谱、稳定性与额外分解成本。

### NLA-RLA-E03

合同可写为：

$$
\text{在延迟}\le T,\ \text{额外内存}\le M
\text{下，使输出/任务误差}\le\varepsilon.
$$

报告在线 sketch 更新时间、每 token 延迟、缓存、重构误差、最坏输出偏差、分布漂移和重建周期。离线最优假设矩阵固定且可多遍访问，不能处理因果到达、未来不可见和子空间漂移。

### NLA-RLA-E04

取 \(S\)，构造

$$
C=AS,\quad W=S^TAS,\quad
\widehat A=CW^\dagger C^T.
$$

若 \(A\succeq0\) 且伪逆按 PSD 谱截断计算，则 \(\widehat A\succeq0\)。检查采样是否偏向高 leverage 区、未采到重要簇的失败率、\(W\) 的谱/数值秩、伪逆阈值、PSD 残差和下游核任务。

### NLA-RLA-E05

每个 worker 对本地 shard 计算 \(Y_s=A_s\Omega\)，共同 seed 使 \(\Omega\) 一致；按行分片时可本地 QR 后做 TSQR/树归约得到全局 \(Q\)。第二遍形成并归约 \(B=Q^TA\) 或所需小核心。认证用另一独立 seed 的探针，局部算 \(R_s\omega_i\) 后归约平方范数。

报告两次数据 pass、TSQR 和核心归约轮数/字节、worker 负载、sketch 内存、多 seed 质量及名义失败概率。若 \(Q\) 的形成需要第一遍结果广播，也必须计入同步。

## 结语

randomized SVD 的可靠性来自四个彼此独立的部件：最佳低秩基线说明问题可压缩；随机 range finder 发现子空间；稳定正交和小型确定性 SVD 完成计算；独立探针验证本次输出。缺少其中任何一层，都只能称为“跑出一个低秩分解”，还不能称为受控算法。
