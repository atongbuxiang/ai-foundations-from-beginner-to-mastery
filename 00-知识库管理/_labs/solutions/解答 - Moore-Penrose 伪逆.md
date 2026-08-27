---
type: solution
status: draft
area: [labs, math/matrix-analysis, math/optimization, ai/foundations]
topic: "[[Moore-Penrose 伪逆]]"
exercise: "[[习题 - Moore-Penrose 伪逆]]"
related: ["[[正交投影]]", "[[条件数]]", "[[练习与测验 MOC]]"]
sources: ["Penrose-1955", "GolubVanLoan-MC4e-Ch5"]
created: 2026-08-18
updated: 2026-08-18
---
# 解答 - Moore-Penrose 伪逆

## A
### LA-PINV-A01
$AA^\dagger A=A,A^\dagger AA^\dagger=A^\dagger,(AA^\dagger)^*=AA^\dagger,(A^\dagger A)^*=A^\dagger A$。前两条规定有效子空间上的逆，后两条把两个幂等算子限定为正交而非斜投影。
### LA-PINV-A02
$A^\dagger:n\times m$；$AA^\dagger:m\times m=P_{\mathcal R(A)}$；$A^\dagger A:n\times n=P_{\mathcal R(A^*)}=P_{\mathcal N(A)^\perp}$。
### LA-PINV-A03
可逆方阵：$A^{-1}$；满列秩：$(A^*A)^{-1}A^*$；满行秩：$A^*(AA^*)^{-1}$。相应 Gram 矩阵可逆性由列/行满秩保证。

## B
### LA-PINV-B01
$A^\dagger=\operatorname{diag}(1/2,0)$。$x^\dagger=(2,0)^T$，预测 $(4,0)^T$，残差 $(0,3)^T$。全部 LS 解 $(2,t)^T$；范数 $4+t^2$ 在 $t=0$ 唯一最小。
### LA-PINV-B02
$A^\dagger=(1/2,1/2)^T$。方程 $x_1+x_2=2$，全部解 $(1+t,1-t)^T$，最小范数解 $(1,1)^T=A^\dagger b$。
### LA-PINV-B03
$A^\dagger=\begin{bmatrix}1&0&0\\0&0&0\end{bmatrix}$。$AA^\dagger=\operatorname{diag}(1,0,0)$ 投影输出空间；$A^\dagger A=\operatorname{diag}(1,0)$ 投影输入空间。

## C
### LA-PINV-C01
令 $A=U_r\Sigma_rV_r^*$、$A^\dagger=V_r\Sigma_r^{-1}U_r^*$。则 $AA^\dagger=U_rU_r^*$、$A^\dagger A=V_rV_r^*$ 自伴；插入 $U_r^*U_r=V_r^*V_r=I$ 即得前两条复原恒等式。
### LA-PINV-C02
$AX$ 自伴且由 $AXA=A$ 得幂等，值域恰为 $\mathcal R(A)$，故是该空间唯一正交投影。类似地 $XA$ 自伴幂等且核等于 $\mathcal N(A)$，故投到 $\mathcal R(A^*)$。于是 $Xb$ 对每个 $b$ 都是唯一最小范数原像，算子唯一。
### LA-PINV-C03
$I-A^\dagger A$ 投到 $\mathcal N(A)$，所以所有给同一预测的解为所给形式。$A^\dagger b\in\mathcal R(A^*)\perp\mathcal N(A)$，勾股式给唯一最小范数。

## D
### NLA-PINV-D01
$\varepsilon\ne0$ 时 $A_\varepsilon^\dagger=\operatorname{diag}(1,1/\varepsilon)$，$\kappa_2=1/|\varepsilon|$（假设 $|\varepsilon|<1$）。当 $\varepsilon\to0$，范数爆炸；在 $\varepsilon=0$ 伪逆第二项突然为 0，跨秩不连续。
### LA-PINV-D02
$AB=[1]$，故 $(AB)^\dagger=1$。$B^\dagger=[1\ 0]$，$A^\dagger=(1/2,1/2)^T$，乘积为 $1/2$。
### NLA-PINV-D03
精确：$1/\sigma$，无偏但放大小值；TSVD：阈值上用 $1/\sigma$、下方为 0，硬偏置且阈值不连续；Ridge：$\sigma/(\sigma^2+\lambda)$，平滑有偏并限制放大。

## E
### AI-PINV-E01
$H^\dagger:d\times N$，$W=H^\dagger Y:d\times c$ 是最小 Frobenius 范数 LS 权重。小奇异值放大标签噪声，需截断/正则并报告容差。
### AI-PINV-E02
固定右因子时，目标对左因子是线性 LS，反之亦然，可用伪逆写规范更新；两侧同时变化时乘积双线性、gauge 不唯一且非凸。
### AI-PINV-E03
对目标输出改动 $\delta y$，规范局部解 $\delta\theta=J^\dagger\delta y$。它只对当前线性化与选定样本最小范数；分布外副作用、非线性有限步和小奇异值需另行控制。
