---
type: exercise
status: draft
area: [math/numerical-analysis, math/numerical-linear-algebra, ai-systems]
topic: Householder 与 Givens 变换
prerequisites: ["[[Householder 与 Givens 变换]]", "[[QR 分解]]", "[[浮点数与舍入误差]]"]
related: ["[[解答 - Householder 与 Givens 变换]]", "[[实验 - Householder 符号、Givens 缩放与 QR 正交性]]", "[[稳定最小二乘与正规方程的风险]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Householder 与 Givens 变换

> [!abstract] 训练目标
> 这组题不只要求“算出 QR”，还要求辨认符号、变换顺序、正交性、后向误差、极端尺度、结构成本和 AI 调用边界。请先独立完成，再查看[[解答 - Householder 与 Givens 变换]]。

## A. 定义、对象与条件识别

### NLA-ORTH-A01：判断并修正

逐条判断正误；错误项写出最小修正。

1. 对任意非零 $v$，$H=I-2vv^T/(v^Tv)$ 都是正交矩阵。
2. Householder 反射保持所有向量不变，只改变坐标表示。
3. $H^T=H$ 且 $H^{-1}=H$。
4. Householder 的行列式总是 $+1$。
5. 把 $x$ 映到 $\alpha e_1$ 时，$|\alpha|$ 必须等于 $\|x\|_2$。
6. $\alpha=+\|x\|_2$ 与 $\alpha=-\|x\|_2$ 在浮点中永远同样稳定。
7. 稳定符号选择使 $|x_1-\alpha|\ge\|x\|_2$。
8. 安全 Householder 只需避免除以零，不必考虑范数 overflow。
9. 实现 Householder QR 时应显式形成每个 $m\times m$ 反射矩阵。
10. 紧凑 QR 可把 $R$ 和 reflector 向量尾部存进同一数组。
11. 若 $R=H_r\cdots H_1A$，则 $Q=H_r\cdots H_1$。
12. 为计算 $Q^Tb$，可以按 $H_1,H_2,\ldots,H_r$ 的操作顺序作用到 $b$。
13. Givens 旋转的行列式为 $-1$。
14. 一次 Givens 旋转只能直接消掉一个指定元素。
15. 直接计算 $\sqrt{f^2+g^2}$ 对所有有限 $f,g$ 都安全。
16. Householder QR 在一般稠密矩阵上通常比逐元素 Givens QR 少 flops。
17. Givens 在稀疏、在线更新和 bulge chasing 中可能更合适。
18. 正交变换序列的误差不会累加，因为每步条件数为 1。
19. Householder QR 后向稳定意味着 $A$ 近秩亏时 $Q$ 仍对输入高度不敏感。
20. QR 验收只需检查 $\|A-QR\|$。
21. 小重构残差不保证 $Q^TQ\approx I$。
22. 无列主元 Householder QR 必然是强 rank-revealing QR。
23. Cholesky QR 形成 $A^TA$，因此近秩亏时更敏感。
24. 若不固定 $R$ 对角符号，可微 QR 的 $Q$ 可能发生离散翻转。
25. block Householder 的主要收益可能来自减少数据移动，而非减少主阶 flops。
26. LoRA 因子 $B=QR$ 后把 $R$ 吸收到另一个因子，不改变精确的低秩更新。

### NLA-ORTH-A02：把量放回正确层次

把下列对象归入“几何对象、算法表示、数值验收、性能/结构、下游任务”中的主层次，并说明不能混淆的相邻层次：

$$
H,\quad (v,\tau),\quad (c,s),\quad
\|I-Q^TQ\|_F,\quad
\|A-QR\|_F/\|A\|_F,\quad
\kappa_2(A),\quad
\text{fill-in},\quad
\text{block size},\quad
\|A^T(b-A\widehat x)\|,\quad
\text{QR sign convention}.
$$

## B. 手算、实现与指标

### NLA-ORTH-B01：完整 Householder 手算

对

$$
x=(4,3,0)^T
$$

使用稳定符号构造 $\alpha,v,H$，验证 $Hx=\alpha e_1$、$H^TH=I$，并写出首分量归一化后的 $(\widetilde v,\tau)$ 表示。

### NLA-ORTH-B02：符号与消去尺度

令

$$
x_\varepsilon=(1,\varepsilon)^T,
\qquad 0<\varepsilon\ll1.
$$

分别取 $\alpha_+=\|x_\varepsilon\|_2$ 与 $\alpha_-=-\|x_\varepsilon\|_2$：

1. 推导两种 $v_1=1-\alpha$ 的渐近量级；
2. 说明为什么固定取 $\alpha_+$ 会丢失方向信息；
3. 给出稳定选择。

### NLA-ORTH-B03：矩阵的一步 Householder 消元

对

$$
A=
\begin{bmatrix}
4&1\\
3&2\\
0&2
\end{bmatrix},
$$

使用 B01 的 $H_1$ 左乘 $A$：

1. 算出 $H_1A$；
2. 指出下一步 reflector 作用的子向量和尺寸；
3. 不必算完第二步，但画出第二步之后的零结构。

### NLA-ORTH-B04：不形成 $H$ 的应用

给定

$$
v=(1,1/3,0)^T,
\qquad
\tau=9/5,
\qquad
B=
\begin{bmatrix}4&1\\3&2\\0&2\end{bmatrix}.
$$

用

$$
HB=B-v(\tau v^TB)
$$

分两步计算，验证与 B03 一致，并比较显式 $H$ 与紧凑应用的存储量。

### NLA-ORTH-B05：Givens 参数与嵌入

为 $(f,g)=(3,4)$ 生成 $c,s,r$。再把旋转嵌入 $\mathbb R^3$ 的第 $(1,3)$ 坐标平面，计算它对 $(3,2,4)^T$ 的作用。

### NLA-ORTH-B06：两次 Givens 得到三角结构

对

$$
A=
\begin{bmatrix}
3&1\\
4&2\\
0&5
\end{bmatrix},
$$

先用 $G(1,2)$ 消去 $a_{21}$，再用作用于第 2、3 行的旋转消去更新后的 $a_{32}$。写出两个旋转与最终上三角 $R$。

### NLA-ORTH-B07：成本比较

令 $m=10^4,n=64$：

1. 用 $2mn^2-\frac23n^3$ 估计 Householder factorization flops；
2. 用
   $$
   6\sum_{j=1}^{n}(m-j)(n-j+1)
   $$
   估计稠密 Givens flops 的主量级；
3. 解释为什么稀疏矩阵上不能只用这两个稠密公式选算法。

### NLA-ORTH-B08：验收两个候选 QR

某 $1000\times50$ 矩阵在 double 中得到：

| 方法 | $\eta_{rec}$ | $\eta_{orth}$ | 时间 |
|---|---:|---:|---:|
| A | $2\times10^{-16}$ | $4\times10^{-2}$ | 1.0 |
| B | $8\times10^{-16}$ | $3\times10^{-14}$ | 1.4 |

分别判断：作为重构压缩、最小二乘、Krylov 基、Stiefel 参数化时应如何选择，还缺哪些指标。

### NLA-ORTH-B09：QR 最小二乘一步到三角方程

设

$$
A=Q\begin{bmatrix}R\\0\end{bmatrix},
\qquad
Q^Tb=\begin{bmatrix}c_1\\c_2\end{bmatrix},
\quad
R=\begin{bmatrix}2&1\\0&3\end{bmatrix},
\quad
c_1=\begin{bmatrix}5\\6\end{bmatrix}.
$$

求最小二乘解，说明 $c_2$ 决定什么，并列出数值验收项。

## C. 推导与证明

### NLA-ORTH-C01：反射的完整谱结构

证明 $H=I-2uu^T$（$\|u\|_2=1$）满足：对称、正交、自逆；$u$ 是 $-1$ 特征向量，$u^\perp$ 是 $+1$ 特征空间；$\det H=-1$。

### NLA-ORTH-C02：映轴公式

从 $v=x-\alpha e_1$、$\alpha^2=\|x\|_2^2$ 出发，逐步证明

$$
\left(I-2\frac{vv^T}{v^Tv}\right)x=\alpha e_1.
$$

指出哪种情形会使 $v=0$，以及稳定符号如何避免。

### NLA-ORTH-C03：Householder QR 的乘积顺序

已知第 $k$ 步左乘 $H_k$，证明

$$
R=H_r\cdots H_1A,
\qquad
A=(H_1\cdots H_r)R.
$$

分别给出计算 $Qx$ 与 $Q^Tx$ 时 reflector 的实际应用顺序。

### NLA-ORTH-C04：正交变换序列的后向稳定骨架

设第 $k$ 步满足

$$
\operatorname{fl}(U_kB)=U_kB+E_k,
\qquad
\|E_k\|\le\epsilon_k\|B\|,
$$

其中 $U_k$ 正交。展开三步并推广到 $r$ 步，证明早期误差不会被后续正交矩阵放大，并写成“精确变换邻近输入”的形式。

### NLA-ORTH-C05：Householder flop 公式

把第 $k$ 步尾随矩阵尺寸写成 $(m-k+1)\times(n-k+1)$，按一次点积块与一次 rank-one update 计数，推导主项

$$
2mn^2-\frac23n^3.
$$

### NLA-ORTH-C06：安全 Givens 缩放

令 $t=\max(|f|,|g|)$，证明

$$
\rho=t\sqrt{(f/t)^2+(g/t)^2}
$$

在精确算术中等于 $\sqrt{f^2+g^2}$；解释为什么内部平方不 overflow，并处理 $t=0$。

### NLA-ORTH-C07：薄 QR 的微分

对满列秩 $A=QR$、$Q^TQ=I$、$R$ 正对角：

1. 证明 $S=Q^TdQ$ 斜对称；
2. 令 $X=Q^TdA\,R^{-1}$，说明如何从 $X$ 的严格下三角恢复 $S$；
3. 推导
   $$
   dQ=(I-QQ^T)dA\,R^{-1}+QS;
   $$
4. 解释 $\sigma_{\min}(A)\to0$ 时的梯度边界。

### NLA-ORTH-C08：两个反射器的 compact WY

设

$$
H_1=I-\tau_1v_1v_1^T,
\qquad
H_2=I-\tau_2v_2v_2^T.
$$

展开 $H_1H_2$，构造

$$
V=[v_1,v_2],
\qquad
T=
\begin{bmatrix}
\tau_1&-\tau_1\tau_2v_1^Tv_2\\
0&\tau_2
\end{bmatrix},
$$

并验证 $H_1H_2=I-VTV^T$。

## D. 反例、诊断与方法边界

### NLA-ORTH-D01：构造符号失效

在 binary64 中取 $x=(1,2^{-k})^T$。说明当 $k$ 足够大时，朴素 $1-\|x\|_2$ 为什么舍入为零；给出一个可以实际检测失效的指标。

### NLA-ORTH-D02：构造 Givens overflow 与 underflow

分别取 $(f,g)=(10^{300},10^{300})$ 与 $(10^{-300},10^{-300})$，分析朴素平方和、真实 $r$ 和缩放公式的行为。

### NLA-ORTH-D03：重构正确但不正交

构造或引用一个近相关满秩矩阵族，说明为什么算法可能给出很小 $\|A-QR\|$ 却有很大 $\|I-Q^TQ\|$。指出哪个方法最典型。

### NLA-ORTH-D04：稳定 QR 不等于 rank revealing

给出一个列顺序使无主元 QR 的前几个 $r_{ii}$ 不能反映最重要列方向的简单例子；说明列主元改变了什么、仍未保证什么。

### NLA-ORTH-D05：Cholesky QR 的平方条件数

令

$$
A_\varepsilon=
\begin{bmatrix}
1&1\\
0&\varepsilon
\end{bmatrix}.
$$

比较 $\kappa_2(A_\varepsilon)$ 与 $\kappa_2(A_\varepsilon^TA_\varepsilon)$ 的量级，并解释 float32 中可能发生的失败。

### NLA-ORTH-D06：QR 符号不连续

考虑

$$
A(t)=\begin{bmatrix}t\\1\end{bmatrix}.
$$

比较两种 QR 符号约定在 $t$ 穿过 0 时的 $Q(t)$；说明仅保证 $QR=A$ 为什么不足以保证可微调用连续。

### NLA-ORTH-D07：稀疏方法选择

一个 $10^6\times10^4$ 稀疏矩阵每列仅 8 个非零，但无序 Householder 造成巨大 fill-in。说明为什么“Householder 稠密 flop 更少”不能决定选择，并给出至少四个应测量的量。

### NLA-ORTH-D08：满秩但 QR 梯度巨大

构造满列秩 $A_\varepsilon$ 使 $\|R^{-1}\|\to\infty$，却每个 $\varepsilon>0$ 时 QR 都唯一。解释“存在且唯一”与“数值可微稳定”的差别。

## E. AI 迁移与研究设计

### NLA-ORTH-E01：Muon/流式幂迭代 QR 合约

为

$$
V_t=\operatorname{QR}(M_t^TM_tV_{t-1})
$$

设计 Householder、SCQR 与 fallback 的完整选择协议。必须写出形状、dtype、条件/秩检测、正交性指标、性能指标和回退触发。

### NLA-ORTH-E02：随机 SVD 正交化消融

设计实验比较 CGS、MGS2、Householder、TSQR 对随机 SVD 的影响。要求区分子空间误差、正交性、最终低秩误差、通信与时间。

### NLA-ORTH-E03：LoRA 因子 QR 重参数化

对 $\Delta W=BA$ 推导 $B=QR$ 后的等价参数，分析对函数值、优化几何、scale ambiguity、rank deficiency 和梯度的影响；给出验收实验。

### NLA-ORTH-E04：在线最小二乘

已有 $A_k=Q_kR_k$，新增一行 $a_{k+1}^T$。说明怎样用 Givens 更新 $R$ 和变换后的右端，给出每步状态、复杂度和长期误差监控。

### NLA-ORTH-E05：GPU block QR 内核审计

给出一个 block Householder QR 的审计表：panel、GEMM、reflector 生成、精度、通信、正交性、重构、极端尺度和重复性均需覆盖。

### NLA-ORTH-E06：分布式 TSQR 归约树

比较 flat tree 与 binary tree TSQR。要求讨论并行深度、消息数、局部 QR、最终 $R$、显式 $Q$ 成本、误差累积和不同树导致的非位级可重复性。

### NLA-ORTH-E07：可微 QR 层

设计一个将 QR 用作 Stiefel retraction 的可微层测试：覆盖满秩、近秩亏、重复尺度、符号翻转、finite difference/VJP、前向与反向 residual、低精度和 batch 极端样本。

### NLA-ORTH-E08：陌生 QR 实现的证据等级

某论文称“我们的 BF16 QR 稳定且比标准库快 3 倍”，只给训练损失与平均时间。写出审稿意见和最小补实验，并区分哪些证据只能支持性能、经验可用性、经验稳定区或稳定性定理。

## 建议完成顺序

1. A01–A02：先把对象与层次分清；
2. B01–B06：闭卷完成两种变换的手算；
3. C01–C06：重建核心理论；
4. D01–D06：建立有限精度与条件边界；
5. E 层任选两题写成完整实验协议；
6. 最后运行[[实验 - Householder 符号、Givens 缩放与 QR 正交性]]，对照自己的预测。
