---
type: solution-set
status: draft
area: [labs, math/matrix-analysis]
prerequisites: ["[[Rayleigh 商与极值表征]]", "[[习题 - Rayleigh 商与极值表征]]"]
related: ["[[练习与测验 MOC]]", "[[特征向量与子空间扰动定理]]"]
sources: ["Axler-LADR4e-7B-7C", "MIT-18.409-Courant-Fischer"]
created: 2026-08-16
updated: 2026-08-16
---

# 解答 - Rayleigh 商与极值表征

> [!warning] 使用方式
> 先独立完成[[习题 - Rayleigh 商与极值表征]]并记录卡点，再查看本页。每题不仅给出结果，也标出使用的假设、证明发动机和常见错误。

## A 级解答

### MA-RQ-A01

1. Rayleigh 商为
   $$
   \rho_A(x)=\frac{x^*Ax}{x^*x},
   \qquad x\ne0.
   $$

2. 对 $c\ne0$，
   $$
   \begin{aligned}
   \rho_A(cx)
   &=\frac{(cx)^*A(cx)}{(cx)^*(cx)}\\
   &=\frac{\overline c c\,x^*Ax}{\overline c c\,x^*x}\\
   &=\rho_A(x).
   \end{aligned}
   $$
   所以它只依赖一维方向，不依赖向量长度与整体相位。

3. 若 $A=A^*$，则
   $$
   \overline{x^*Ax}=x^*A^*x=x^*Ax,
   $$
   因而分子为实数；分母 $x^*x>0$，所以商为实数。反过来，在标准复内积下，若 $x^*Ax$ 对所有 $x$ 都为实数，则可推出 $A$ Hermitian。

4. 因为
   $$
   (cx)^*A(cx)=|c|^2x^*Ax.
   $$
   同一方向只要换长度，数值就会变化。分母 $x^*x$ 消除了这项尺度。

### MA-RQ-A02

1. **错误。** 本章极值结论要求 Hermitian；即使 Hermitian，最大 Rayleigh 商是最大代数特征值 $\lambda_1$，而最大模特征值可能是最负特征值。例如 $\operatorname{diag}(1,-5)$ 的最大 Rayleigh 商为 $1$，谱范数为 $5$。

2. **正确。** 谱展开给出
   $$
   \rho_A(x)=\sum_iw_i\lambda_i,
   \qquad w_i\ge0,\quad\sum_iw_i=1.
   $$

3. **错误。** 全部特征向量都是驻点；顶端是最大值，底端是最小值，中间特征方向通常是鞍点。

4. **正确。** 对任意酉矩阵 $R$，
   $$
   \operatorname{tr}((QR)^*A(QR))
   =\operatorname{tr}(R^*Q^*AQR)
   =\operatorname{tr}(Q^*AQ).
   $$
   而 $Q$ 与 $QR$ 有相同列空间。

5. **错误。** 小残差保证 Rayleigh 商靠近某个特征值；若附近是重谱或密集谱簇，不能识别某个指定向量。还需要谱间隙。

### MA-RQ-A03

1. 形状为
   $$
   Q^TAQ\in\mathbb R^{k\times k},
   \qquad
   Q^TBQ\in\mathbb R^{k\times k},
   $$
   而
   $$
   \operatorname{tr}(Q^TAQ)\in\mathbb R.
   $$

2. $B\succ0$ 保证对所有 $x\ne0$，
   $$
   x^TBx>0,
   $$
   从而商处处有定义；它还保证存在可逆 $B^{1/2}$，可把问题白化为标准 Hermitian 特征值问题。若 $B$ 奇异或不定，分母可为零或变号，标准紧致极值论会失效。

3. $Q^TQ=I_k$ 表示列向量在欧氏内积中标准正交；$Q^TBQ=I_k$ 表示在
   $$
   \langle x,y\rangle_B=x^TBy
   $$
   中标准正交，前提是 $B\succ0$。

## B 级解答

### MA-RQ-B01

因为 $x(\theta)$ 已归一化，

$$
\begin{aligned}
\rho_A(x(\theta))
&=2\cos^2\theta+2\sin\theta\cos\theta+2\sin^2\theta\\
&=2+\sin2\theta.
\end{aligned}
$$

求导：

$$
\frac{d}{d\theta}\rho_A(x(\theta))=2\cos2\theta.
$$

驻点满足

$$
\cos2\theta=0,
$$

所以

$$
\theta=\frac\pi4+\frac{k\pi}{2},
\qquad k\in\mathbb Z.
$$

当 $\sin2\theta=1$ 时取得最大值

$$
\rho_{\max}=3,
$$

对应一维方向

$$
\operatorname{span}\{(1,1)^T\}.
$$

当 $\sin2\theta=-1$ 时取得最小值

$$
\rho_{\min}=1,
$$

对应

$$
\operatorname{span}\{(1,-1)^T\}.
$$

$A$ 的特征值为 $3,1$，所以

$$
\|A\|_2=\max\{|3|,|1|\}=3.
$$

本例中它等于最大 Rayleigh 商；这是因为最大模特征值恰是正的最大特征值，不是一般恒等式。

### MA-RQ-B02

首先

$$
q_1^Tq_1=1,
\qquad
q_2^Tq_2=1,
\qquad
q_1^Tq_2=0,
$$

所以 $Q^TQ=I_2$。

计算

$$
Aq_1
=\frac1{\sqrt2}(7e_1+e_3),
\qquad
Aq_2=4e_2.
$$

于是

$$
q_1^TAq_1=\frac{7+1}{2}=4,
$$

$$
q_2^TAq_2=4,
$$

并且交叉项为零。因此

$$
H=Q^TAQ=
\begin{bmatrix}4&0\\0&4\end{bmatrix}.
$$

两个 Ritz 值都是 $4$。对任意 $y\ne0$，

$$
\rho_A(Qy)
=\frac{y^THy}{y^Ty}
=4,
$$

所以

$$
\min_{0\ne x\in\operatorname{col}(Q)}\rho_A(x)=4=\lambda_2(A).
$$

该子空间达到 Courant–Fischer 最大值，但

$$
\operatorname{col}(Q)
=\operatorname{span}\left\{\frac{e_1+e_3}{\sqrt2},e_2\right\}
\ne\operatorname{span}\{e_1,e_2\}.
$$

这不矛盾。Courant–Fischer 保证最优**值**为 $\lambda_2$，并给出一个自然最优空间；它不宣称所有最优 $k$ 维空间都必须唯一。该题也提醒我们：目标值唯一并不自动推出优化变量唯一。

### MA-RQ-B03

因为

$$
B^{-1/2}=\begin{bmatrix}1&0\\0&1/2\end{bmatrix},
$$

所以

$$
B^{-1/2}AB^{-1/2}
=\begin{bmatrix}5&0\\0&1/2\end{bmatrix}.
$$

因此广义 Rayleigh 商的最大值和最小值分别为

$$
5,
\qquad
\frac12.
$$

直接解

$$
Ax=\lambda Bx
$$

得到

$$
5x_1=\lambda x_1,
\qquad
2x_2=4\lambda x_2.
$$

所以广义特征对可以取

$$
(\lambda_1,x_1)=(5,e_1),
$$

$$
(\lambda_2,x_2)=\left(\frac12,e_2\right).
$$

为了 $B$-归一化，取

$$
q_1=e_1,
\qquad
q_2=\frac12e_2.
$$

则

$$
q_1^TBq_1=1,
\qquad
q_2^TBq_2=1,
\qquad
q_1^TBq_2=0.
$$

## C 级解答

### MA-RQ-C01

由谱定理，存在标准正交特征基 $u_1,\ldots,u_n$。写

$$
x=\sum_{i=1}^nc_iu_i.
$$

则

$$
x^*x=\sum_i|c_i|^2
$$

并且

$$
x^*Ax=\sum_i\lambda_i|c_i|^2.
$$

定义

$$
w_i=\frac{|c_i|^2}{\sum_j|c_j|^2}.
$$

显然 $w_i\ge0$ 且 $\sum_iw_i=1$，所以

$$
\rho_A(x)=\sum_iw_i\lambda_i.
$$

这是特征值的凸组合，故

$$
\lambda_n\le\rho_A(x)\le\lambda_1.
$$

现在假设

$$
\lambda_1=\cdots=\lambda_r>\lambda_{r+1}.
$$

若 $x$ 只含 $u_1,\ldots,u_r$ 分量，则所有有权重的特征值都等于 $\lambda_1$，故 $\rho_A(x)=\lambda_1$。

反过来，若 $x$ 在某个 $j>r$ 上有非零分量，则 $w_j>0$ 且 $\lambda_j<\lambda_1$，凸组合严格小于 $\lambda_1$。因此全部等号向量正是

$$
x\in\operatorname{span}\{u_1,\ldots,u_r\}\setminus\{0\}.
$$

### MA-RQ-C02

记

$$
S_\star=\operatorname{span}\{u_1,\ldots,u_k\}.
$$

对任意 $0\ne x\in S_\star$，Rayleigh 商只混合 $\lambda_1,\ldots,\lambda_k$，所以

$$
\rho_A(x)\ge\lambda_k.
$$

取 $x=u_k$ 达到等号，因此

$$
\min_{0\ne x\in S_\star}\rho_A(x)=\lambda_k.
$$

所以总最大值至少是 $\lambda_k$。

任取 $k$ 维子空间 $S$，令

$$
L=\operatorname{span}\{u_k,u_{k+1},\ldots,u_n\}.
$$

其维数为 $n-k+1$。由维数不等式，

$$
\dim(S\cap L)
\ge k+(n-k+1)-n
=1.
$$

故存在 $0\ne y\in S\cap L$。$y$ 只含 $u_k,\ldots,u_n$ 分量，所以

$$
\rho_A(y)\le\lambda_k.
$$

于是

$$
\min_{0\ne x\in S}\rho_A(x)
\le\rho_A(y)
\le\lambda_k.
$$

这对任意 $S$ 成立，故总最大值不超过 $\lambda_k$。与前一半合并：

$$
\lambda_k
=\max_{\dim S=k}\min_{0\ne x\in S}\rho_A(x).
$$

### MA-RQ-C03

写 $A=U\Lambda U^*$，其中 $u_i$ 是 $U$ 的第 $i$ 列。利用 trace 循环性：

$$
\begin{aligned}
\operatorname{tr}(Q^*AQ)
&=\operatorname{tr}(Q^*U\Lambda U^*Q)\\
&=\operatorname{tr}(\Lambda U^*QQ^*U)\\
&=\sum_{i=1}^n\lambda_i u_i^*QQ^*u_i\\
&=\sum_{i=1}^n\lambda_i\|Q^*u_i\|_2^2.
\end{aligned}
$$

令 $P=QQ^*$。$P$ 是正交投影，所以

$$
0\preceq P\preceq I.
$$

因此

$$
0\le p_i=u_i^*Pu_i\le1.
$$

又有

$$
\sum_i p_i
=\operatorname{tr}(U^*PU)
=\operatorname{tr}(P)
=\operatorname{rank}(P)
=k.
$$

所以目标变成

$$
\sum_i\lambda_ip_i,
\qquad
0\le p_i\le1,\quad \sum_i p_i=k.
$$

因 $\lambda_1\ge\cdots\ge\lambda_n$，最大值通过把权重 $1$ 放在前 $k$ 个位置达到：

$$
\operatorname{tr}(Q^*AQ)
\le\sum_{i=1}^k\lambda_i.
$$

取 $Q=[u_1,\ldots,u_k]$ 达到等号。

若 $\lambda_k=\lambda_{k+1}$，边界重特征空间中可以选择不同的 $k$ 维切片；即使子空间固定，$Q\mapsto QR$ 也给出无穷多组最优基。因此不能把某组列向量当作唯一答案。

## D 级解答

### MA-RQ-D01

特征多项式为

$$
\det(\lambda I-A)
=\lambda^2+1,
$$

所以特征值为

$$
\lambda=\pm i.
$$

对任意实向量 $x=(x_1,x_2)^T$，

$$
x^TAx
=-x_1x_2+x_2x_1
=0.
$$

故对所有非零实 $x$，

$$
\rho_A(x)=0.
$$

这与复特征值 $\pm i$ 没有极值对应。原因是实二次型只看到

$$
\frac{A+A^T}{2};
$$

本题矩阵完全是反对称部分。

若研究长度放大率，应最大化

$$
\frac{\|Ax\|_2}{\|x\|_2},
$$

其最大值是 $\sigma_1(A)$。本题 $A$ 是正交旋转，所有奇异值都为 $1$。

### MA-RQ-D02

最大特征值是 $5$，对应二维特征子空间

$$
\mathcal U=\operatorname{span}\{e_1,e_2\}.
$$

所以最大 Rayleigh 商为 $5$，全部最大化方向是 $\mathcal U\setminus\{0\}$。

对 $k=2$，Ky Fan 最大值为

$$
\lambda_1+\lambda_2=10.
$$

一组最优基是

$$
Q_1=[e_1,e_2].
$$

另一组可以取

$$
Q_2=
\left[
\frac{e_1+e_2}{\sqrt2},
\frac{-e_1+e_2}{\sqrt2}
\right].
$$

二者满足

$$
Q_1Q_1^T=Q_2Q_2^T
=\operatorname{diag}(1,1,0).
$$

若逐列命名“第一方向”“第二方向”，两个完全相同的最优子空间会被误判成旋转了 $45^\circ$。稳定对象是投影或子空间，不是基列编号。

### MA-RQ-D03

对 $x=(x_1,x_2)^T$，

$$
\rho_{A,B}(x)
=\frac{x_1^2+x_2^2}{x_1^2-x_2^2}.
$$

取 $x(t)=(1,t)^T$。则

$$
\rho_{A,B}(x(t))
=\frac{1+t^2}{1-t^2}.
$$

当 $t\to1^-$，分母趋于 $0^+$，商趋于 $+\infty$；当 $t\to1^+$，分母趋于 $0^-$，商趋于 $-\infty$。所以不存在有限最大值或最小值。

标准证明失效在两个位置：

1. $x^TBx$ 对非零 $x$ 不总为正，商甚至在零锥 $x_1^2=x_2^2$ 上无定义；
2. 不存在 Hermitian 正定的 $B^{1/2}$ 将约束白化成紧致单位球面。

## E 级解答

### AI-RQ-E01

对单位方向 $q\in\mathbb R^d$，每个样本的标量投影组成

$$
Hq\in\mathbb R^m.
$$

平均平方激活为

$$
\frac1m\|Hq\|_2^2
=\frac1mq^TH^THq
=q^TCq.
$$

前 $k$ 维表示子空间问题为

$$
\max_{Q^TQ=I_k}\operatorname{tr}(Q^TCQ).
$$

由 Ky Fan，最优值为

$$
\sum_{i=1}^k\lambda_i(C),
$$

即投影到最优 $k$ 维子空间后保留的总方差。若除以总方差

$$
\operatorname{tr}(C)=\sum_{i=1}^d\lambda_i(C),
$$

就得到累计解释方差比例。

若 $\lambda_k=\lambda_{k+1}$，选择 $k$ 维空间时必须从边界重特征空间中只取部分方向；不同选择有相同目标值。因此不仅基不唯一，前 $k$ 子空间本身也可能不唯一。此时应扩展到完整谱簇或承认 rank 截断边界不可识别。

### AI-RQ-E02

对单位方向 $d$，

$$
-0.8\le d^THd\le12.
$$

Taylor 二阶项是

$$
\frac12d^THd,
$$

所以范围为

$$
-0.4\le\frac12d^THd\le6.
$$

存在负特征值 $-0.8$，因此 Hessian 不是 PSD；仅从二阶局部模型看，该点不满足局部凸的必要曲率条件。

若只允许 $d\in\operatorname{col}(Q)$ 且 $Q^TQ=I$，写 $d=Qy$，应分析压缩 Hessian

$$
Q^THQ.
$$

仅凭两个极端特征值不能判断：

- 实际训练步是否下降，因为还有一阶梯度和高阶项；
- SGD 噪声、学习率和预条件后的动态；
- 特征方向是否稳定，因为未给 gap 与残差；
- 大部分谱的分布与有效秩。

写出其中任一项并说明理由即可。

### AI-RQ-E03

1. **LDA。** 典型目标为
   $$
   \max_{x\ne0}\frac{x^TS_Bx}{x^TS_Wx},
   $$
   或多方向广义 trace 版本。关键条件是 $S_W\succ0$；若奇异，需要正则化、限制到像空间或使用适当广义逆。

2. **图谱聚类。** 对未归一化 Laplacian $L$，典型第二特征方向解
   $$
   \min_{\substack{x\ne0\\x\perp\mathbf1}}
   \frac{x^TLx}{x^Tx}.
   $$
   对归一化问题会出现度矩阵 $D$ 的广义商，并需检查零度节点、图连通分量和零特征值重数。

3. **表示压缩/PCA。** 目标为
   $$
   \max_{Q^TQ=I_k}\operatorname{tr}(Q^TCQ).
   $$
   需检查 $C$ 的构造、中心化、rank、$\lambda_k-\lambda_{k+1}$ 和样本扰动；边界重谱使最优截断子空间不唯一。

## 总结性判分标准

本套题真正要形成的能力不是背三条公式，而是能稳定执行以下链条：

$$
\text{Hermitian/度量条件}
\to
\text{Rayleigh 商}
\to
\text{方向或子空间极值}
\to
\text{残差与 gap}
\to
\text{AI 对象解释}.
$$

若 C02、C03 仍无法闭卷重建，应回到[[Rayleigh 商与极值表征#七、Courant–Fischer 极小极大原理]]与[[Rayleigh 商与极值表征#十、Ky Fan 最大原理：一次选择 $k$ 个方向]]；若 D01、D03 出错，应复习本章的 Hermitian 与 $B\succ0$ 边界。
