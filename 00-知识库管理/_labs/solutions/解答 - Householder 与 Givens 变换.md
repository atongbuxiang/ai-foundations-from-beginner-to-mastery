---
type: solution
status: draft
area: [math/numerical-analysis, math/numerical-linear-algebra, ai-systems]
topic: Householder 与 Givens 变换
exercise: "[[习题 - Householder 与 Givens 变换]]"
prerequisites: ["[[Householder 与 Givens 变换]]"]
related: ["[[实验 - Householder 符号、Givens 缩放与 QR 正交性]]", "[[稳定最小二乘与正规方程的风险]]", "[[数值稳定性]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - Householder 与 Givens 变换

> [!warning] 使用建议
> 先闭卷完成手算和证明。只会调用 `qr()` 不等于理解稳定 QR；只得到 $A\approx QR$ 而没有检查 $Q^TQ$、符号、尺度和下游 residual，也不算完成。

## A. 定义、对象与条件识别

### NLA-ORTH-A01

1. **正确。** $vv^T/(v^Tv)$ 是投影到 $\operatorname{span}(v)$ 的正交投影，反射平方为单位阵。
2. **错误。** 它保留超平面内分量，把法向分量变号；一般会改变向量本身。
3. **正确。** $H$ 对称且 $H^2=I$。
4. **错误。** 非平凡 Householder 只有一个 $-1$ 特征值，所以 $\det H=-1$。
5. **正确。** 正交变换保持二范数。
6. **错误。** 若 $x_1\approx\|x\|$，选择同号目标会在 $x_1-\|x\|$ 中消去。
7. **正确。** 取 $\alpha=-\operatorname{sign}(x_1)\|x\|$ 后，$|x_1-\alpha|=|x_1|+\|x\|$。
8. **错误。** 直接平方求范数仍可能 overflow/underflow，需缩放或安全 hypot。
9. **错误。** 应保存 $v,\tau$，用 rank-one 或 block update。
10. **正确。** 这是 `xGEQRF` 的典型紧凑布局。
11. **错误。** $R=H_r\cdots H_1A$，故 $A=H_1\cdots H_rR$，所以 $Q=H_1\cdots H_r$。
12. **正确。** $Q^T=H_r\cdots H_1$；作用到向量时右端的 $H_1$ 先执行。
13. **错误。** Givens 是旋转，$\det G=+1$。
14. **正确。** 一个二维旋转直接把一对分量中的一个变为零。
15. **错误。** 平方可能先溢出或下溢，即使最终半径可表示。
16. **正确。** 方阵主项约为 $\frac43n^3$ 对 $2n^3$。
17. **正确。** 局部两坐标操作能利用结构并支持更新。
18. **错误。** 误差仍逐步累加，只是不被后续正交矩阵进一步按大条件数放大。
19. **错误。** 后向稳定约束算法误差；近秩亏列空间本身仍敏感。
20. **错误。** 还要检查正交性、三角性和下游任务 residual。
21. **正确。** CGS 是典型反例。
22. **错误。** 无主元 QR 不排序重要方向；普通 QRCP 也不等于 strong RRQR。
23. **正确。** $\kappa_2(A^TA)=\kappa_2(A)^2$。
24. **正确。** $q_i,R_{i,:}$ 可同时变号而不改变乘积。
25. **正确。** compact WY 把矩阵—向量工作重组为高强度矩阵乘。
26. **正确。** $BA=(QR)A=Q(RA)$，精确函数值不变。

### NLA-ORTH-A02

| 对象 | 主层次 | 不能混淆的层次 |
|---|---|---|
| $H$ | 几何对象 | 不等于实际存储的 dense matrix |
| $(v,\tau)$ | 算法表示 | 其舍入会影响数值正交性 |
| $(c,s)$ | 算法表示 | 必须绑定旋转布局与符号约定 |
| $\|I-Q^TQ\|_F$ | 数值验收 | 不等于重构误差 |
| $\|A-QR\|_F/\|A\|_F$ | 数值验收 | 小值不保证 $Q$ 正交 |
| $\kappa_2(A)$ | 问题条件性 | 不是 QR 算法后向误差 |
| fill-in | 性能/结构 | 同时影响内存和实际舍入路径 |
| block size | 性能/实现 | 不改变精确 QR 定义 |
| $\|A^T(b-A\widehat x)\|$ | 下游任务 | 检查最小二乘一阶条件，不替代 factor residual |
| QR sign convention | 几何表示/接口 | 乘积不变但连续性、可复现性和梯度会变 |

## B. 手算、实现与指标

### NLA-ORTH-B01：完整 Householder 手算

$$
\|x\|_2=5,
\qquad
\alpha=-5.
$$

$$
v=x-\alpha e_1=(9,3,0)^T,
\qquad
v^Tv=90.
$$

$$
H=I-2\frac{vv^T}{v^Tv}
=
\begin{bmatrix}
-4/5&-3/5&0\\
-3/5&4/5&0\\
0&0&1
\end{bmatrix}.
$$

直接相乘得

$$
Hx=(-5,0,0)^T.
$$

$H$ 对称；左上 $2\times2$ 块的列标准正交，故 $H^TH=I$。

把 $v$ 除以 9：

$$
\widetilde v=(1,1/3,0)^T,
\qquad
\widetilde v^T\widetilde v=10/9.
$$

所以

$$
\tau=\frac2{10/9}=\frac95,
\qquad
H=I-\tau\widetilde v\widetilde v^T.
$$

### NLA-ORTH-B02：符号与消去尺度

$$
\|x_\varepsilon\|_2
=\sqrt{1+\varepsilon^2}
=1+\frac12\varepsilon^2+O(\varepsilon^4).
$$

同号目标：

$$
v_{1,+}
=1-\sqrt{1+\varepsilon^2}
=-\frac12\varepsilon^2+O(\varepsilon^4).
$$

反号目标：

$$
v_{1,-}
=1+\sqrt{1+\varepsilon^2}
=2+\frac12\varepsilon^2+O(\varepsilon^4).
$$

前者从两个约为 1 的数相减恢复 $O(\varepsilon^2)$，相对误差可被放大到 $O(u/\varepsilon^2)$，甚至直接舍入成 0；后者是同号相加。稳定选择为

$$
\alpha=-\operatorname{sign}(x_1)\|x\|_2=-\|x\|_2.
$$

### NLA-ORTH-B03：一步矩阵消元

用 B01 的 $H_1$：

$$
H_1A
=
\begin{bmatrix}
-5&-2\\
0&1\\
0&2
\end{bmatrix}.
$$

第二步只作用于第 2–3 行、第 2 列子向量

$$
x_2=(1,2)^T\in\mathbb R^2.
$$

完成后结构为

$$
R=
\begin{bmatrix}
\times&\times\\
0&\times\\
0&0
\end{bmatrix}.
$$

### NLA-ORTH-B04：紧凑应用

先算

$$
v^TB
=
\begin{bmatrix}5&5/3\end{bmatrix}.
$$

再乘 $\tau=9/5$：

$$
w^T=\tau v^TB
=\begin{bmatrix}9&3\end{bmatrix}.
$$

$$
vw^T
=
\begin{bmatrix}
9&3\\
3&1\\
0&0
\end{bmatrix}.
$$

所以

$$
HB=B-vw^T
=
\begin{bmatrix}
-5&-2\\
0&1\\
0&2
\end{bmatrix}.
$$

显式 $p\times p$ 的 $H$ 需 $O(p^2)$ 存储；紧凑表示只需 $p$ 个向量元素和一个标量。

### NLA-ORTH-B05：Givens 参数与嵌入

$$
r=5,
\qquad c=3/5,
\qquad s=4/5.
$$

嵌入第 $(1,3)$ 坐标：

$$
G_{13}=
\begin{bmatrix}
3/5&0&4/5\\
0&1&0\\
-4/5&0&3/5
\end{bmatrix}.
$$

$$
G_{13}(3,2,4)^T=(5,2,0)^T.
$$

### NLA-ORTH-B06：两次 Givens

第一次

$$
G_{12}=
\begin{bmatrix}
3/5&4/5&0\\
-4/5&3/5&0\\
0&0&1
\end{bmatrix},
$$

得到

$$
G_{12}A
=
\begin{bmatrix}
5&11/5\\
0&2/5\\
0&5
\end{bmatrix}.
$$

第二次对 $(2/5,5)^T$：

$$
r_2=\sqrt{(2/5)^2+5^2}=\frac{\sqrt{629}}5,
$$

$$
c_2=\frac2{\sqrt{629}},
\qquad
s_2=\frac{25}{\sqrt{629}}.
$$

嵌入第 2、3 行后，

$$
G_{23}G_{12}A
=
\begin{bmatrix}
5&11/5\\
0&\sqrt{629}/5\\
0&0
\end{bmatrix}.
$$

### NLA-ORTH-B07：成本比较

Householder：

$$
2(10^4)(64)^2-\frac23(64)^3
\approx8.17\times10^7
$$

flops。

Givens 对 $m\gg n$ 的主项约

$$
3mn^2
=3(10^4)(64)^2
\approx1.23\times10^8
$$

flops，约为 Householder 主项的 $1.5$ 倍。稀疏问题还必须测 fill-in、实际触碰非零数、内存流量、重排序和并行同步；稠密公式可能完全高估或错判局部旋转成本。

### NLA-ORTH-B08：验收两个 QR

- 纯重构压缩若下游只用 $QR$ 乘积，A 可能暂时可用，但必须说明 $Q$ 不能当正交基；
- 最小二乘依赖 $Q^T$ 保范数，优先 B；
- Krylov 基直接依赖方向正交，必须选 B；
- Stiefel 参数化要求 $Q^TQ\approx I$，必须选 B。

还缺：条件数/数值秩、三角性、下游 residual、矩阵尺度、dtype、最坏样本、内存和通信。时间 1.0 与 1.4 只能支持当前实现上的性能差异。

### NLA-ORTH-B09：QR 最小二乘

解

$$
\begin{bmatrix}2&1\\0&3\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=\begin{bmatrix}5\\6\end{bmatrix}.
$$

第二行给 $x_2=2$；第一行给 $2x_1+2=5$，故

$$
\widehat x=(3/2,2)^T.
$$

$\|c_2\|_2$ 是最小残差范数。数值验收包括 $A\widehat x-b$、$A^T(A\widehat x-b)$、QR 重构/正交性、$R$ 条件估计和 rank tolerance。

## C. 推导与证明

### NLA-ORTH-C01：谱结构

$$
H^T=I-2uu^T=H.
$$

$$
H^2
=I-4uu^T+4u(u^Tu)u^T
=I.
$$

故 $H$ 正交且自逆。对 $u$：

$$
Hu=u-2u(u^Tu)=-u.
$$

若 $u^Tx=0$，则 $Hx=x$。所以

$$
\mathbb R^p=\operatorname{span}(u)\oplus u^\perp
$$

分别是 $-1,+1$ 特征空间；行列式是全部特征值之积，即 $-1$。

### NLA-ORTH-C02：映轴公式

令 $v=x-\alpha e_1$ 且 $\alpha^2=\|x\|^2$：

$$
v^Tx=\|x\|^2-\alpha x_1,
$$

$$
v^Tv
=\|x\|^2-2\alpha x_1+\alpha^2
=2(\|x\|^2-\alpha x_1).
$$

因此 $2v^Tx/(v^Tv)=1$，于是

$$
Hx=x-v=\alpha e_1.
$$

若 $x=\|x\|e_1$ 且选 $\alpha=\|x\|$，则 $v=0$。稳定选择取相反符号，使 $|v_1|=|x_1|+\|x\|>0$。

### NLA-ORTH-C03：乘积顺序

逐步左乘：

$$
A_1=H_1A,
\quad A_2=H_2A_1=H_2H_1A,
$$

归纳得

$$
R=H_r\cdots H_1A.
$$

左乘 $H_1\cdots H_r$，利用 $H_k^2=I$，相邻项从内向外消去：

$$
A=H_1\cdots H_rR.
$$

故 $Q=H_1\cdots H_r$。

- 计算 $Qx$：矩阵右端最先作用，实际顺序 $H_r,H_{r-1},\ldots,H_1$；
- 计算 $Q^Tx=H_r\cdots H_1x$：实际顺序 $H_1,H_2,\ldots,H_r$。

### NLA-ORTH-C04：后向稳定骨架

三步展开：

$$
\begin{aligned}
\widehat B_1&=U_1A+E_1,\\
\widehat B_2&=U_2\widehat B_1+E_2
=U_2U_1A+U_2E_1+E_2,\\
\widehat B_3&=U_3U_2U_1A
+U_3U_2E_1+U_3E_2+E_3.
\end{aligned}
$$

推广得

$$
\widehat B_r=UA+E,
\qquad U=U_r\cdots U_1,
$$

且

$$
\|E\|
\le\sum_{k=1}^{r}\|E_k\|
$$

因为每个剩余左乘积都正交。再写成

$$
UA+E
=U(A+U^TE).
$$

令 $\Delta A=U^TE$，则 $\|\Delta A\|=\|E\|$，得到精确变换邻近输入的解释。

### NLA-ORTH-C05：flop 主项

令 $p_k=m-k+1,q_k=n-k+1$。形成 $v^TB$ 约 $2p_kq_k$ flops，rank-one update 再约 $2p_kq_k$，总计

$$
4\sum_{k=1}^{n}(m-k+1)(n-k+1).
$$

令 $j=n-k+1$：

$$
4\sum_{j=1}^{n}(m-n+j)j
=4(m-n)\frac{n(n+1)}2
+4\frac{n(n+1)(2n+1)}6.
$$

取三次和二次主项：

$$
2mn^2-\frac23n^3+O(mn+n^2).
$$

### NLA-ORTH-C06：安全缩放

若 $t>0$：

$$
t\sqrt{(f/t)^2+(g/t)^2}
=\sqrt{f^2+g^2}.
$$

因为 $|f/t|,|g/t|\le1$，内部平方不会 overflow。它们过小时其中一项可能下溢，但较大分量至少为 1，半径主尺度仍保留。若 $t=0$，则 $f=g=0$，取 $r=0,c=1,s=0$。

### NLA-ORTH-C07：薄 QR 微分

由

$$
d(Q^TQ)=dQ^TQ+Q^TdQ=0
$$

得

$$
S:=Q^TdQ,
\qquad S^T=-S.
$$

从

$$
dA=dQ\,R+Q\,dR
$$

得到

$$
X:=Q^TdA\,R^{-1}
=S+dR\,R^{-1}.
$$

$dR\,R^{-1}$ 上三角，所以 $i>j$ 时

$$
S_{ij}=X_{ij},
\qquad S_{ji}=-X_{ij},
\qquad S_{ii}=0.
$$

另一方面，

$$
(I-QQ^T)dA\,R^{-1}
=(I-QQ^T)dQ.
$$

$dQ$ 的列空间内分量是 $QQ^TdQ=QS$，故

$$
dQ=(I-QQ^T)dA\,R^{-1}+QS.
$$

当 $\sigma_{\min}(A)\to0$，$\|R^{-1}\|=1/\sigma_{\min}(A)$ 发散，导数可无界。

### NLA-ORTH-C08：compact WY

展开：

$$
\begin{aligned}
H_1H_2
&=(I-\tau_1v_1v_1^T)(I-\tau_2v_2v_2^T)\\
&=I-\tau_1v_1v_1^T-\tau_2v_2v_2^T
+\tau_1\tau_2v_1(v_1^Tv_2)v_2^T.
\end{aligned}
$$

给定题中 $V,T$，

$$
VTV^T
=\tau_1v_1v_1^T+\tau_2v_2v_2^T
-\tau_1\tau_2(v_1^Tv_2)v_1v_2^T.
$$

所以 $I-VTV^T$ 与上式完全一致。

## D. 反例、诊断与方法边界

### NLA-ORTH-D01：符号失效

$$
\|x\|_2
=\sqrt{1+2^{-2k}}
=1+2^{-2k-1}+O(2^{-4k}).
$$

当 $2^{-2k-1}$ 小于 1 附近半个 ulp，浮点 $\sqrt{1+2^{-2k}}$ 会舍入成 1，于是

$$
1-\operatorname{fl}(\|x\|_2)=0.
$$

可检测：$v=0$、$v^Tv=0$、应用后尾部相对残差不下降，或构造出的 $H$ 非有限。稳定符号改用 $1+\|x\|$。

### NLA-ORTH-D02：Givens 极端尺度

- $10^{300}$ 平方为 $10^{600}$，超出 binary64，朴素 $r=\infty$；真实值是 $\sqrt2\times10^{300}$，可表示。
- $10^{-300}$ 平方约 $10^{-600}$，下溢为 0，朴素 $r=0$；真实值是 $\sqrt2\times10^{-300}$。

缩放取 $t=10^{\pm300}$，内部两项均为 1，得到 $r=t\sqrt2$。

### NLA-ORTH-D03：小重构、大正交缺陷

取

$$
A_\varepsilon=\mathbf1\mathbf1^T+\varepsilon I.
$$

每个 $\varepsilon>0$ 时满秩，但列高度相关。CGS 可能把旧方向误差留在新列中；相同舍入同时进入 $R$，使 $QR$ 仍能很好重构 $A$，而 $Q^TQ-I$ 已很大。必须独立检查两项。

### NLA-ORTH-D04：不 rank revealing

最小例子：

$$
A=\begin{bmatrix}\varepsilon&0\\0&1\end{bmatrix}.
$$

无主元 QR 按原顺序得到 $R=\operatorname{diag}(\varepsilon,1)$，第一对角很小，却有一个重要方向在后。QRCP 先交换两列，得到对角顺序约 $(1,\varepsilon)$。它改善贪心排序，但一般矩阵上仍不保证全局最优列子集或 strong RRQR 界。

### NLA-ORTH-D05：Cholesky QR

$A_\varepsilon$ 的列在 $\varepsilon\to0$ 时近相关，故

$$
\kappa_2(A_\varepsilon)=\Theta(1/\varepsilon).
$$

而

$$
\kappa_2(A_\varepsilon^TA_\varepsilon)
=\kappa_2(A_\varepsilon)^2
=\Theta(1/\varepsilon^2).
$$

当 $\varepsilon$ 接近 $\sqrt{u_{32}}$ 或更小时，形成 Gram 矩阵可能丢失正定小方向，Cholesky 失败或 $Q^TQ-I$ 很大。

### NLA-ORTH-D06：符号不连续

正对角约定取

$$
r(t)=\sqrt{t^2+1}>0,
\qquad
q(t)=\frac{(t,1)^T}{r(t)},
$$

它在 $t=0$ 连续。若另一个实现强制 $q_1\ge0$，则可取

$$
r(t)=\operatorname{sign}(t)\sqrt{t^2+1},
\qquad q(t)=A(t)/r(t),
$$

$t$ 穿过 0 时整列翻转。两边都满足 $qr=A$，但第二种单独输出 $q$ 不连续。

### NLA-ORTH-D07：稀疏边界

应测量：

1. fill-in 与峰值非零数；
2. 内存峰值和数据移动；
3. 重排序/旋转选择时间；
4. 并行消息与同步；
5. 重构、正交性和 rank estimate；
6. 最坏列/块而非只有平均。

稠密 flop 模型假设触碰整个尾随块，在此不成立。

### NLA-ORTH-D08：满秩但梯度大

取

$$
A_\varepsilon=\operatorname{diag}(1,\varepsilon),
\qquad\varepsilon>0.
$$

QR 唯一且 $Q=I,R=A_\varepsilon$，但

$$
\|R^{-1}\|_2=1/\varepsilon\to\infty.
$$

存在性与唯一性只回答每个固定 $\varepsilon$ 有定义；数值可微稳定性还要求映射的导数有界。

## E. AI 迁移与研究设计

E 层允许不同方案，但必须覆盖以下最低证据。

### NLA-ORTH-E01：Muon/流式幂迭代

- 形状：$M_t\in\mathbb R^{d_1\times d_2}$、$V_{t-1}\in\mathbb R^{d_2\times r}$、$Y_t=M_t^TM_tV_{t-1}\in\mathbb R^{d_2\times r}$；
- 默认可靠路径：FP32/FP64 累加的 Householder QR；
- 快路径：SCQR，监控 Gram 正定性、$R$ 最小对角、$\|I-Q^TQ\|$；
- 回退：factor failure、orthogonality 超阈值、NaN/Inf、condition proxy 超阈值即转 Householder；
- 指标：谱子空间夹角、Muon update 相对误差、训练 loss、最坏 batch、吞吐、内存和回退率；
- 不能只用训练 loss 证明 QR 稳定。

### NLA-ORTH-E02：随机 SVD

固定 $A,\Omega,r,p$ 和 dtype，只替换正交化器。报告：

- $\|I-Q^TQ\|$；
- 投影误差 $\|(I-QQ^T)A\|$；
- 最终 $\|A-U_r\Sigma_rV_r^T\|$；
- 与高精度 SVD 的主角度；
- 时间、内存流量、通信和重正交次数；
- 条件数、谱衰减和 oversampling 分层。

### NLA-ORTH-E03：LoRA 重参数化

$$
B=QR
\quad\Longrightarrow\quad
BA=Q(RA).
$$

函数值精确不变；$Q$ 固定列尺度，把尺度/混合吸收到 $RA$。它可能改善参数可解释性或优化几何，但不消除 $B$ 近秩亏、符号自由度和 QR 梯度敏感性。实验应比较函数误差、梯度映射、condition、训练轨迹和符号规范。

### NLA-ORTH-E04：在线最小二乘

新增行后先形成

$$
\begin{bmatrix}R_k\\a_{k+1}^T\end{bmatrix}
$$

以及相同变换后的右端。用 $n$ 个左右 Givens 自底向上恢复上三角；每次同时旋转右端。单次更新 $O(n^2)$，存储 $O(n^2)$，长期监控 $R$ condition、真实 residual、正交漂移和 downdate 失败。

### NLA-ORTH-E05：GPU block QR

审计表至少包含：panel reflector 的生成精度、`V/T` 存储、GEMM 累加 dtype、block size、workspace、global memory bytes、同步、显式/隐式 $Q$、极端尺度、重构/正交性、重复运行差异、NaN/Inf、与 vendor reference 的最坏误差。

### NLA-ORTH-E06：TSQR

- flat tree：深度 $O(P)$，根进程/链路瓶颈；
- binary tree：深度 $O(\log P)$，更多并行；
- 每个叶子先局部 Householder QR，再对堆叠的小 $R$ 做 QR；
- 最终 $R$ 由树上归约得到，显式 $Q$ 需反向传播树中 reflectors；
- 不同树改变舍入结合顺序，通常数学等价但不位级一致；
- 报消息数、字节数、深度、orthogonality、reconstruction 和 scale 分布。

### NLA-ORTH-E07：可微 QR 层

测试矩阵族：随机满秩、$\sigma_{\min}$ 扫描、重复列尺度、rank collision、batch 少数极端矩阵。检查：正对角规范、forward reconstruction/orthogonality、VJP 与 finite difference、高精度 reference、adjoint consistency、BF16/FP32、NaN/Inf 和梯度分位数。近 rank-deficient 时应返回警告、阻尼/替代参数化或停止梯度，而非静默输出。

### NLA-ORTH-E08：证据等级

审稿意见：

1. 训练 loss 不能分离 QR 子程序误差；
2. 平均时间未报告矩阵形状、硬件、库、warm-up 和传输；
3. 未给 $\eta_{rec},\eta_{orth}$、condition/rank、最坏样本；
4. BF16 的乘法、累加、输出 dtype 未定义；
5. 未测试尺度、近秩亏、符号和 batch 极端值；
6. 没有对 Householder/MGS2/FP32 reference；
7. “稳定”若指理论，必须给输入类、误差模型和统一界。

补实验后：时间支持性能；训练曲线支持特定任务经验可用；受控矩阵族支持经验稳定区；只有明确量词的证明才支持稳定性定理。

## 复盘标准

- A 层：26 个判断至少 24 个正确并能修正；
- B 层：闭卷完成 B01–B06、B09；
- C 层：能重建 C02–C07；
- D 层：能现场构造符号、尺度、正交性三类失败；
- E 层：任选一题形成“形状—算法—dtype—误差—性能—回退”完整协议；
- 未达到时回到[[Householder 与 Givens 变换]]对应小节重新推导，而不是背诵答案。
