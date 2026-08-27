---
type: solution-set
status: draft
area: [math/calculus, math/matrix-calculus, math/probability]
aliases: [行列式导数习题解答, logdet 习题解答]
prerequisites: ["[[习题 - 行列式、log-det 与迹的导数]]"]
related: ["[[行列式、log-det 与迹的导数]]", "[[练习与测验 MOC]]"]
sources: ["Su-2383-Determinant-Derivative", "Magnus-Neudecker-Matrix-Differential-Calculus", "Higham-Functions-of-Matrices"]
created: 2026-08-18
updated: 2026-08-18
---

# 解答 - 行列式、log-det 与迹的导数

## A. 概念与一阶直觉

### A1 解

置换展开

$$
\det(I+tB)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)
\prod_i(\delta_{i,\sigma(i)}+tB_{i,\sigma(i)}).
$$

常数项只来自恒等置换并全取 $\delta_{ii}$，等于 $1$。一阶项必须只取一个 $tB_{i,\sigma(i)}$，其余 $n-1$ 个因子取 Kronecker delta；这些 delta 强制其余索引固定，而置换性又迫使该索引也固定，所以只留下 $tB_{ii}$。总和为 $t\sum_iB_{ii}$；其余至少含两个 $t$，故为 $O(t^2)$。

### A2 解

$$
D\det(A)[E]=\sum_{ij}C_{ij}E_{ij}
=\operatorname{tr}(C^\top E).
$$

定义 $\operatorname{adj}(A)=C^\top$，故

$$
D\det(A)[E]=\operatorname{tr}(\operatorname{adj}(A)E).
$$

标准梯度配对为 $\operatorname{tr}(G^\top E)$，所以

$$
\boxed{\nabla_A\det A=\operatorname{adj}(A)^\top=C.}
$$

### A3 解

$\det A$ 对所有方阵定义，是元素多项式，奇异处仍处处可微。$\log|\det A|$ 在所有实可逆矩阵上定义，在奇异集合趋向 $-\infty$ 且无有限扩展导数；它允许负 det。实值 $\log\det A$ 只在 $\det A>0$ 的区域定义；负 det 处无实值。SPD 是其中最重要的连通子域。

## B. 核心推导

### B1 解

由 A1，

$$
\det(A+tE)=\det A\,[1+t\operatorname{tr}(A^{-1}E)+O(t^2)].
$$

故

$$
D\det(A)[E]=\det A\operatorname{tr}(A^{-1}E),
$$

$$
\boxed{\nabla_A\det A=\det(A)A^{-\top}.}
$$

链式法则给

$$
D\log|\det A|[E]=\operatorname{tr}(A^{-1}E),
\quad
\boxed{\nabla_A\log|\det A|=A^{-\top}.}
$$

全部要求 $A$ 可逆。

### B2 解

对 $2\times2$ 矩阵 $\begin{bmatrix}a&b\\c&d\end{bmatrix}$，

$$
\operatorname{adj}(A)=\begin{bmatrix}d&-b\\-c&a\end{bmatrix}.
$$

所以

$$
\operatorname{adj}(A_1)=\begin{bmatrix}0&0\\0&1\end{bmatrix},
\qquad
D\det(A_1)[E]=E_{22}.
$$

而 $\operatorname{adj}(A_2)=0$，故所有方向导数为零。一般秩 $n-1$ 时至少一个 $(n-1)$ 阶余子式非零；秩至多 $n-2$ 时所有这些余子式为零。

### B3 解

$$
d(A^4)=dA\,A^3+A\,dA\,A^2+A^2dA\,A+A^3dA.
$$

取迹并循环，每项都化为 $\operatorname{tr}(A^3dA)$，故

$$
d\operatorname{tr}(A^4)=4\operatorname{tr}(A^3dA),
\qquad
\boxed{\nabla_A\operatorname{tr}(A^4)=4(A^3)^\top.}
$$

未取迹时四个插入位置不能循环等同，除非 $A$ 与 $dA$ 交换。

## C. 统计与结构化模型

### C1 解

记 $r=x-\mu$。对均值：

$$
\boxed{\nabla_\mu\ell=-\Sigma^{-1}r.}
$$

对协方差，使用 $d\Sigma^{-1}=-\Sigma^{-1}(d\Sigma)\Sigma^{-1}$：

$$
\boxed{
\nabla_\Sigma\ell
=\frac12\left(\Sigma^{-1}-\Sigma^{-1}rr^\top\Sigma^{-1}\right).
}
$$

log-det 项惩罚协方差总体体积过大；二次项惩罚样本相对协方差尺度过远。两项平衡才有有限尺度估计。

### C2 解

$$
\boxed{\log\det\Sigma=2\sum_i\log L_{ii}.}
$$

在无约束可逆 $L$ 的环境空间，

$$
\boxed{\nabla_L=2L^{-\top}.}
$$

若 $L_{ii}=e^{s_i}$，则 $\partial\log\det\Sigma/\partial s_i=2$。纯 log-det 只依赖三角矩阵的对角乘积，所以严格下三角自由元导数为零；$2L^{-\top}$ 是上三角，投影到允许的下三角方向后只剩对角 $2/L_{ii}$。

### C3 解

$$
\boxed{
\log\det(D+UU^\top)
=\sum_i s_i+log\det(I_r+U^\top D^{-1}U).
}
$$

$D\succ0$，且 $U^\top D^{-1}U\succeq0$，所以小矩阵 $I_r+U^\top D^{-1}U\succ0$。形成小矩阵约 $O(dr^2)$，其 Cholesky 为 $O(r^3)$；另有 $O(d)$ 的对角操作。

## D. 数值与 AI 实现

### D1 解

SPD：做 Cholesky $A=LL^\top$，失败本身是非 SPD 诊断；返回 $2\sum_i\log L_{ii}$，符号固定为 $+1$。一般实矩阵：带主元 LU $PA=LU$，累积置换符号与 $U_{ii}$ 符号，返回 `(sign, logabsdet)`，其中 logabsdet 为 $\sum_i\log|U_{ii}|$；零/数值零 pivot 标记奇异。直接 det 乘积会先上溢、下溢或严重丢精度，之后取 log 无法恢复信息，负 det 还会令实 log 非法。

### D2 解

三角矩阵行列式是对角乘积，故

$$
\boxed{\log|\det J(x)|=\sum_i s_i(x_{<i}).}
$$

指数保证对角严格为正，不会为零。若改用普通 $a_i$，则 $a_i=0$ 时局部不可逆且 logabsdet 发散；跨过零时符号改变，导数 $1/a_i$ 在零附近爆炸。必须用非零约束参数化或显式处理符号与边界。

### D3 解

$$
\mathbb E[\xi^\top M\xi]
=\mathbb E[\operatorname{tr}(M\xi\xi^\top)]
=\operatorname{tr}(M\mathbb E[\xi\xi^\top])
=\operatorname{tr}M.
$$

对每个 probe $\xi_j$，算 $v_j=A'\xi_j$，解 $Au_j=v_j$，取 $q_j=\xi_j^\top u_j$，用 $N^{-1}\sum_jq_j$ 估计。报告至少：probe 分布（Rademacher/Gaussian）、数量 $N$、随机种子/重复次数、样本方差或置信区间、线性求解器/容差/残差、精度和预条件器。

## E. 证明与研究边界

### E1 解

$\operatorname{rank}(A)\le n-2$ 意味着所有 $(n-1)\times(n-1)$ 子式为零，所以 $\operatorname{adj}(A)=0$，由 Jacobi 通式 $D\det(A)[E]=0$。若零空间维数为 $k$，可经可逆左右基变换把 $A$ 化到含 $n-k$ 个非零主方向和 $k$ 个零方向的块形式。一般扰动必须在每个零方向提供一个一阶因子才能形成满秩体积，因此最早通常在 $t^k$ 阶出现；特殊方向可能使该系数也为零而更高阶。

### E2 解

$$
df=-\operatorname{tr}(X^{-1}dX),
\qquad
\boxed{\nabla f(X)=-X^{-1}}
$$

（$X$ 对称）。因 $d(X^{-1})=-X^{-1}(dX)X^{-1}$，

$$
\boxed{H_X[E]=X^{-1}EX^{-1}.}
$$

方向曲率

$$
\langle E,H_X[E]\rangle_F
=\operatorname{tr}(E X^{-1}E X^{-1})
=\|X^{-1/2}EX^{-1/2}\|_F^2\ge0
$$

（对称 $E$）。当任一特征值 $\lambda_i(X)\downarrow0$，$-\log\det X=-\sum_i\log\lambda_i\to+\infty$，因此有限目标的迭代被排斥在正定锥边界之外。

### E3 解

1. 一般为 $A^{-\top}$，且实 $\log\det A$ 还要求 $\det A>0$；SPD 时才等于 $A^{-1}$。
2. 错。det 是多项式；奇异处用 adjugate 公式。不可用的是 inverse 版本和 log-det。
3. 错。矩阵与扰动不交换；一般需矩阵函数 Fréchet 导数。只有取迹等特殊结构可简化。
4. 错。det 非零只给局部可逆；全局还需单射、适当性/边界等结构，flow 通常通过可逆构造保证。
5. 错。$\Sigma+\varepsilon I$ 改变协方差、似然和梯度；可以是明确的观测噪声/正则模型，也可以是数值近似，但必须披露并分析敏感性。

> [!success] 验收提示
> 若能在不查表时从 $\det(I+tB)$、adjugate 和逆矩阵微分三条路径互相核对公式，并能为 Gaussian/flow 选择稳定实现与边界诊断，才算真正掌握本章。
