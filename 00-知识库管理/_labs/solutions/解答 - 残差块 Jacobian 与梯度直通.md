---
type: solution
status: draft
area: [neural-networks/residual-stability, jacobian, backpropagation]
topic: "[[残差块 Jacobian 与梯度直通]]"
exercise: "[[习题 - 残差块 Jacobian 与梯度直通]]"
sources: ["[[S-2016-He-Identity-Mappings]]", "[[S-2016-He-ResNet]]", "[[S-2022-Su-8994-Why-Residual]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 残差块 Jacobian 与梯度直通

## A

### NN-RJG-A01
若 $x,y\in\mathbb R^D,\theta\in\mathbb R^P$，则

$$
J_xF\in\mathbb R^{D\times D},
\qquad
J_\theta F\in\mathbb R^{D\times P},
\qquad
J_xy=I_D+J_xF\in\mathbb R^{D\times D}.
$$

对 $v\in\mathbb R^D,u\in\mathbb R^D$：

$$
J_xyv=v+J_xFv,
$$

$$
J_x y^\mathsf Tu=u+J_xF^\mathsf Tu,
$$

$$
J_\theta y^\mathsf Tu=J_\theta F^\mathsf Tu\in\mathbb R^P.
$$

### NN-RJG-A02
identity rail 存在只说明 $J=I+J_F$ 中有一个加法项。它不推出 $J=I$，后者还需 $J_F=0$；不推出 norm 保持，后者需 $J$ 在相关方向上等距；也不推出可逆，因 $J_F=-I$ 时 $J=0$。四个命题强度依次增加且没有自动蕴含。

### NN-RJG-A03
链式法则给出

$$
J_y(x)
=J_P(x)+\alpha J_F(N(x))J_N(x).
$$

直达项只有在 $P(x)=x$ 的局部与全局意义下才是 $I$。若 $P=\lambda I$、projection、pooling 或 gate，直达项分别为 $\lambda I,J_P$ 等。

## B

### NN-RJG-B01

$$
J_F^\mathsf T
=\begin{bmatrix}-1/2&0\\1&-1/2\end{bmatrix}.
$$

identity VJP：

$$
g_y=(1,-1)^\mathsf T.
$$

branch VJP：

$$
J_F^\mathsf Tg_y=(-1/2,3/2)^\mathsf T.
$$

总和：

$$
g_x=(1/2,1/2)^\mathsf T.
$$

### NN-RJG-B02
$y=(1+c)x$，forward/backward scalar gain 都是 $1+c$：

| $c$ | gain | 解释 |
|---:|---:|---|
| $0$ | $1$ | identity |
| $-1$ | $0$ | 完全消失 |
| $-2$ | $-1$ | norm 保持但变号 |
| $1/2$ | $3/2$ | 放大 |

### NN-RJG-B03
令 $a=0.2$：

$$
0.8\le\sigma_{\min}(I+J_F),
\qquad
\sigma_{\max}(I+J_F)\le1.2,
$$

$$
\kappa_2(I+J_F)\le\frac{1.2}{0.8}=1.5.
$$

这些通常是保守界。只有 $J_F$ 的极端方向与 $I$ 恰好同向/反向等特殊结构时才取等。

## C

### NN-RJG-C01
从

$$
dy=(I+J_xF)dx+J_\theta Fd\theta
$$

开始，loss differential 为

$$
d\mathcal L
=g_y^\mathsf Tdy
=g_y^\mathsf T(I+J_xF)dx
+g_y^\mathsf TJ_\theta Fd\theta.
$$

把系数改写为列向量内积：

$$
d\mathcal L
=\left[(I+J_xF)^\mathsf Tg_y\right]^\mathsf Tdx
+\left[J_\theta F^\mathsf Tg_y\right]^\mathsf Td\theta.
$$

故

$$
g_x=g_y+J_xF^\mathsf Tg_y,
\qquad
g_\theta=J_\theta F^\mathsf Tg_y.
$$

### NN-RJG-C02

$$
\begin{aligned}
(I+A_2)(I+A_1)(I+A_0)
={}&I\\
&+(A_0+A_1+A_2)\\
&+(A_1A_0+A_2A_0+A_2A_1)\\
&+A_2A_1A_0.
\end{aligned}
$$

长度分别为 0、1、2、3。矩阵顺序由 forward composition 决定，例如不能把 $A_2A_0$ 写成 $A_0A_2$。

### NN-RJG-C03
$M$ 为上三角，所以 eigenvalues 都是 $0.1$。

$$
M^\mathsf TM
=\begin{bmatrix}0.01&0.3\\0.3&9.01\end{bmatrix}.
$$

其 trace 为 $9.02$，determinant 为 $10^{-4}$。两个 eigenvalues 约为

$$
9.0199889,
\qquad
1.10865\times10^{-5}.
$$

因此 singular values 约为

$$
3.00333,
\qquad
0.0033296.
$$

eigenvectors 只描述 invariant directions；非正规矩阵的正交输入方向增益由 singular values 决定，可同时有强放大与强压缩。

## D

### NN-RJG-D01
例如 $x\in\mathbb R^{D}$，$P\in\mathbb R^{d\times D}$，$d<D$，且 $F(N(x))\in\mathbb R^d$。则

$$
J_P\in\mathbb R^{d\times D},
\quad
J_N\in\mathbb R^{D\times D},
\quad
J_F\in\mathbb R^{d\times D},
$$

总 Jacobian

$$
J_P+\alpha J_FJ_N\in\mathbb R^{d\times D}.
$$

任何从更高维到更低维的线性 Jacobian 都有非平凡 nullspace，所以最小全空间增益为 0；不能给正 lower bound。

### NN-RJG-D02
随机取 $u,v$，检查

$$
u^\mathsf T\operatorname{JVP}(v)
\approx
\operatorname{VJP}(u)^\mathsf Tv.
$$

两次计算必须复用相同 stochastic mask；BatchNorm 必须相同 batch/state/mode；in-place 不能覆盖 primal；detach 会删边；broadcast 参数的 VJP 必须沿复制轴求和。任一不一致都会破坏对偶。

### NN-RJG-D03
框架会为 ReLU 在 0 选一个约定导数，中心差分

$$
\frac{f(x+h)-f(x-h)}{2h}
$$

却跨过 kink，常得到左右导数平均，不必等于框架约定。可靠协议是把点移离 kink、做多个 step sweep、固定 dtype/RNG/state、比较 directional derivative，并对 kink 单列广义导数区间而非判实现错误。

## E

### NN-RJG-E01
标量取 $J_F=+a$ 与 $J_F=-a$，二者 operator norm 都是 $a$。residual gains 分别为 $1+a$ 与 $1-a$；当 $a=1$ 时一个 gain 2，另一个 gain 0。norm-only 诊断丢失 branch 相对 identity 的方向/符号。

二维也可取 $aI$ 与 $-aI$，结论相同；再加入 skew/nonnormal 部分会产生旋转与暂态。

### NN-RJG-E02
次乘法性给出

$$
\|J_{0\to N}\|_2
\le\prod_{\ell=0}^{N-1}(1+\|A_\ell\|_2)
\le\left(1+\frac cN\right)^N
\le e^c.
$$

若 $c/N<1$，单层 lower bound 给出

$$
\sigma_{\min}(J_{0\to N})
\ge\left(1-\frac cN\right)^N.
$$

固定 $c$、$N\to\infty$ 时趋向 $e^{-c}$。这是 worst-case 充分界，不说明真实 singular values 恰在该区间端点。

### NN-RJG-E03
仪表盘可包含：

1. 每层 $\|g_{rail}\|,\|g_{branch}\|$ 与 cosine；
2. 多个随机 $v$ 的 $\|Jv\|/\|v\|$ 分布；
3. 多个随机 $u$ 的 VJP gain；
4. block/chunk/full-network power iteration $\sigma_{\max}$ 与残差；
5. 小 singular value 的 Lanczos/solve-based estimate；
6. cumulative $\sum\log\|g_\ell\|/\|g_{\ell+1}\|$；
7. dtype、train/eval、mask 条件下的 finite-difference sweep；
8. JVP/VJP 对偶误差。

结果按 layer、seed、batch 和训练时刻保存，不能用单个平均数遮住极端方向。
