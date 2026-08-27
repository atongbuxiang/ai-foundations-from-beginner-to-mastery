---
type: solution
status: draft
area: [math/ode, math/dynamical-systems, ai/optimization, ai/safety]
topic: "Lyapunov 稳定性与能量函数"
exercise: "[[习题 - Lyapunov 稳定性与能量函数]]"
related: ["[[Lyapunov 稳定性与能量函数]]", "[[ODE、动力系统与 SDE MOC]]", "[[实验 - Lyapunov 度量、LaSalle 与离散能量边界]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Lyapunov 稳定性与能量函数

> [!warning] 阅读方式
> 先独立写出“条件—推理—结论强度”，再核对解答。Lyapunov 题最危险的错误通常不是求导，而是把 nonincrease 写成 convergence、把 regional 写成 global、把 energy decay 写成 state decay，或把 continuous certificate 直接移植到 numerical solver。

## A. 识别、定义与定理边界

### DYN-LYAP-A01

不失一般性先平移坐标，令 $x_*=0$。

**1. 定号性**

- $V$ positive definite：$V(0)=0$，且对研究区域中每个 $x\ne0$ 有 $V(x)>0$；
- positive semidefinite：$V(0)=0$，且 $V(x)\ge0$，但可能在非零点也等于零；
- negative definite：$V(0)=0$，且 $x\ne0$ 时 $V(x)<0$。

正定性把标量 $V$ 与“离平衡点有多远”联系起来；半正定函数通常只能控制一部分坐标或到某个集合的距离。

**2. Local 与 global**

Local positive definite 只要求上述符号在 $0$ 的某邻域成立；globally positive definite 要求在整个 $\mathbb R^n$ 成立。符号成立的区域决定 direct method 最多能给出多大范围的证书。

**3. Proper / radially unbounded**

有限维欧氏空间中，对连续函数常用条件

$$
\|x\|\to\infty
\quad\Longrightarrow\quad
V(x)\to\infty.
$$

它等价于所有 sublevel sets

$$
\Omega_c=\{x:V(x)\le c\}
$$

都是 compact。这个条件负责把“$V$ 有界”翻译为“state 有界”，是 global 结论中常被漏掉的一环。

**4. Class-$\mathcal K$ functions**

$\alpha:[0,a)\to[0,\infty)$ 属于 class $\mathcal K$，若它连续、严格递增且 $\alpha(0)=0$。若定义域为 $[0,\infty)$ 且 $\alpha(r)\to\infty$，则属于 $\mathcal K_\infty$。

典型 energy–state bounds 为

$$
\alpha_1(\|x\|)
\le V(x)
\le\alpha_2(\|x\|).
$$

下界防止“state 很远但 energy 很小”，上界允许用初始状态控制初始 energy。

**5. Lie derivative**

若 $V\in C^1$，则

$$
L_fV(x)
=\nabla V(x)^\top f(x).
$$

沿任意经典解 $x(t)$，

$$
\frac d{dt}V(x(t))=L_fV(x(t)).
$$

它不是普通的“时间偏导”，而是 $V$ 沿 vector field 方向的 directional derivative。

**6. Sublevel set**

$\Omega_c$ 是 energy 不超过 $c$ 的状态集合。若边界上不能向外穿越，或更强地在整个 $\Omega_c$ 上 $L_fV\le0$，则它可成为 forward-invariant containment certificate。

**7. Forward invariance**

集合 $S$ forward invariant，指

$$
x(0)\in S
\quad\Longrightarrow\quad
x(t)\in S
$$

对解存在的所有 $t\ge0$ 成立。它是把点态导数不等式变成“整条轨道不逃离验证区域”的桥。

**8. Basin 与 inner approximation**

原点的 basin of attraction 是所有满足 forward solution 存在且

$$
x(t;x_0)\to0
$$

的初值 $x_0$ 的集合。若某 compact sublevel $\Omega_c$ forward invariant，且可证明其中所有轨道趋于原点，那么

$$
\Omega_c\subseteq\mathcal B(0).
$$

它通常只是 certified inner approximation，不等于完整 basin。

最后的命题为假。反例

$$
V(x)=\frac{x^2}{1+x^2}
$$

连续且 globally positive definite，但

$$
V(x)\to1
\quad(\lvert x\rvert\to\infty),
$$

所以不 proper。例如 $c=1$ 时 $\Omega_c=\mathbb R$，并不 compact。正定性只分辨零点，properness 才控制无穷远。

---

### DYN-LYAP-A02

下面给出一个常用的 local 版本。令 $f$ locally Lipschitz，$f(0)=0$，$V\in C^1(D)$，其中 $D$ 是含原点的邻域。

**Direct method：stability**

若

$$
V(0)=0,\qquad V(x)>0\ (x\ne0),
\qquad L_fV(x)\le0
$$

在 $D$ 内成立，则原点 locally Lyapunov stable。Local Lipschitz 保证 IVP 的 local uniqueness；证明还要选一个完全落在 $D$ 内的 sublevel。

**Strict decrease：asymptotic stability**

若进一步

$$
L_fV(x)<0,\qquad x\in D\setminus\{0\},
$$

则原点 locally asymptotically stable。严格负定只给 asymptotic，不自动给 exponential；后者需要定量比较式。

**LaSalle：regional convergence**

令 $\Omega$ compact 且 forward invariant，$V\in C^1$，并且

$$
L_fV\le0\quad\text{on }\Omega.
$$

定义

$$
E=\{x\in\Omega:L_fV(x)=0\}.
$$

若 $M$ 是 $E$ 中的 largest invariant subset，则每条从 $\Omega$ 出发的轨道都满足

$$
\operatorname{dist}(x(t),M)\to0.
$$

$E$ 只是瞬时零导数点集；点在 $E$ 上并不代表后续仍留在 $E$。$M$ 要求整条 forward/backward orbit 在允许意义下都留在 $E$。阻尼振子中

$$
E=\{(q,p):p=0\},
$$

但 $q\ne0,p=0$ 时 $\dot p=-q\ne0$，会立即离开 $E$，所以

$$
M=\{(0,0)\}.
$$

$\dot V\le0$ 只给单调性与极限值 $V_\infty$ 的存在；它没有排除沿 level set 运动、趋向一条 equilibrium manifold 或永远旋转。若 $M$ 不是 singleton，LaSalle 一般只给

$$
\operatorname{dist}(x(t),M)\to0,
$$

而不能声称收敛到预先指定的点。

---

### DYN-LYAP-A03

| 对象 | 演化 | 正确的一步/瞬时算子 | 典型严格条件 | 额外风险 |
|---|---|---|---|---|
| continuous ODE | $\dot x=f(x)$ | $L_fV=\nabla V^\top f$ | $L_fV<0$ | domain、forward completeness |
| discrete map | $x_{k+1}=F(x_k)$ | $\Delta V=V(F(x))-V(x)$ | $\Delta V<0$ | step size、update rule |
| Itô SDE | $dX=b(X)dt+\sigma(X)dW$ | generator $\mathcal LV$ | 依所求 moment/probability 结论选择 drift 条件 | diffusion、stopping time、integrability |

SDE 的 generator 为

$$
\mathcal LV
=\nabla V^\top b
+\frac12\operatorname{tr}
\left(\sigma\sigma^\top\nabla^2V\right).
$$

第二阶项表明：deterministic drift 上 energy 下降，不代表 noise 下仍下降。

对 explicit Euler，

$$
F_h(x)=x+hf(x).
$$

即使 $L_fV<0$，有限 $h$ 下

$$
V(x+hf(x))-V(x)
$$

还包含高阶项。以 $\dot x=-x$、$V=x^2/2$ 为例，

$$
\Delta V
=\frac12\left((1-h)^2-1\right)x^2
=\frac12h(h-2)x^2.
$$

因此 continuous flow 对所有 $t>0$ 稳定，而 Euler 只有 $0<h<2$ 时严格下降。

Sample loss 如

$$
\frac1N\sum_i
\max\{0,L_fV(x_i)+m\}
$$

只检查有限集合。它既不是全区域 proof，也不自动控制网络在 samples 之间的行为。

EBM 的 energy $E_\theta(x)$ 通常用于定义密度、ranking 或 sampling landscape。它只有在额外指定 dynamics $f$ 且验证

$$
\nabla E_\theta(x)^\top f(x)\le0
$$

及定号/目标集条件后，才可能同时充当 Lyapunov function。名称相同不等于逻辑角色相同。

## B. 手算、构造与定量界

### DYN-LYAP-B01

有

$$
\dot V
=x\dot x
=x^2(x^2-1)
=-x^2(1-x^2)
=-2(1-x^2)V.
$$

因此：

- $0<|x|<1$ 时 $\dot V<0$；
- $x=0,\pm1$ 时 $\dot V=0$；
- $|x|>1$ 时 $\dot V>0$。

若 $0<c<1/2$，则

$$
\Omega_c
=\left[-\sqrt{2c},\sqrt{2c}\right]
\subset(-1,1).
$$

它 closed 且 bounded，因而 compact；在其中 $\dot V\le0$，所以从 $\Omega_c$ 出发时

$$
V(x(t))\le V(x_0)\le c.
$$

于是 $\Omega_c$ forward invariant。由于其中除原点外 $\dot V<0$，direct method 给原点 local asymptotic stability。

系统的 phase line 为

$$
\begin{array}{c|ccccccc}
x&(-\infty,-1)&-1&(-1,0)&0&(0,1)&1&(1,\infty)\\
\hline
\dot x&-&0&+&0&-&0&+
\end{array}
$$

所以精确 basin 是

$$
\mathcal B(0)=(-1,1).
$$

当 $c=1/2$，

$$
\Omega_{1/2}=[-1,1].
$$

它虽 forward invariant，但两个边界点 $\pm1$ 自身是 equilibria，不收敛到 $0$。故它不是“其中所有点收敛到原点”的闭集证书。可以说其 interior 落在 basin 中，但不能把整个闭 sublevel 包进去。

$V=x^2/2$ 的确 proper，但 $\dot V$ 在 $|x|>1$ 为正。Properness 只负责无穷远控制，不会替代 derivative sign，因此不能推出 global asymptotic stability。

在 $|x|\le r<1$ 上，

$$
\dot V=-2(1-x^2)V
\le-2(1-r^2)V.
$$

最大的统一常数为

$$
\alpha_r=2(1-r^2),
$$

因为在 $|x|=r$ 处取到最弱下降率。于是只要轨道从该 invariant interval 出发，

$$
V(t)\le e^{-2(1-r^2)t}V(0),
$$

从而

$$
|x(t)|
\le e^{-(1-r^2)t}|x(0)|.
$$

这给的是每个严格内区间上的 regional exponential bound，并不与 basin 边界附近速率退化矛盾。

---

### DYN-LYAP-B02

对

$$
E=\frac12(q^2+p^2)
$$

求导：

$$
\dot E
=q\dot q+p\dot p
=qp+p(-q-\gamma p)
=-\gamma p^2\le0.
$$

$E$ proper，所以每个 $\Omega_c$ compact；其 nonincrease 使 $\Omega_c$ forward invariant，也排除了 finite escape。零导数集为

$$
E_0=\{(q,p):p=0\}.
$$

若 $p=0$ 且要一直留在此直线上，还必须有

$$
\dot p=-q=0.
$$

因此 largest invariant subset 是

$$
M=\{(0,0)\}.
$$

LaSalle 给所有初值的轨道趋于原点；结合 $E$ positive definite，原点 global asymptotically stable。

现在令

$$
V_\varepsilon
=\frac12(q^2+p^2)+\varepsilon qp
=\frac12
\begin{pmatrix}q&p\end{pmatrix}
\begin{pmatrix}1&\varepsilon\\
\varepsilon&1
\end{pmatrix}
\begin{pmatrix}q\\p\end{pmatrix}.
$$

其 eigenvalues 为 $(1\pm\varepsilon)/2$，故 $|\varepsilon|<1$ 时 positive definite，并且

$$
\frac{1-|\varepsilon|}{2}\|(q,p)\|^2
\le V_\varepsilon
\le
\frac{1+|\varepsilon|}{2}\|(q,p)\|^2.
$$

沿流求导：

$$
\begin{aligned}
\dot V_\varepsilon
&=-\gamma p^2
+\varepsilon\left(p^2-q^2-\gamma qp\right)\\
&=-\begin{pmatrix}q&p\end{pmatrix}
W_\varepsilon
\begin{pmatrix}q\\p\end{pmatrix},
\end{aligned}
$$

其中

$$
W_\varepsilon=
\begin{pmatrix}
\varepsilon&\varepsilon\gamma/2\\
\varepsilon\gamma/2&\gamma-\varepsilon
\end{pmatrix}.
$$

由 Sylvester criterion，

$$
W_\varepsilon\succ0
\iff
\varepsilon>0,
\qquad
\varepsilon(\gamma-\varepsilon)
-\frac{\varepsilon^2\gamma^2}{4}>0.
$$

所以可取

$$
0<\varepsilon<
\frac{\gamma}{1+\gamma^2/4}.
$$

这个上界总不超过 $1$，因为

$$
\frac{\gamma}{1+\gamma^2/4}\le1
\iff(\gamma-2)^2\ge0.
$$

令

$$
m_\varepsilon=\frac{1-\varepsilon}{2},
\qquad
M_\varepsilon=\frac{1+\varepsilon}{2},
$$

以及

$$
\beta_\varepsilon
=\lambda_{\min}(W_\varepsilon)
=\frac12\left[
\gamma-
\sqrt{(2\varepsilon-\gamma)^2
+\varepsilon^2\gamma^2}
\right]>0.
$$

便有

$$
m_\varepsilon\|z\|^2
\le V_\varepsilon(z)
\le M_\varepsilon\|z\|^2,
\qquad
\dot V_\varepsilon\le-\beta_\varepsilon\|z\|^2
\le-\frac{\beta_\varepsilon}{M_\varepsilon}V_\varepsilon.
$$

Grönwall inequality 给

$$
V_\varepsilon(t)
\le
e^{-\beta_\varepsilon t/M_\varepsilon}
V_\varepsilon(0),
$$

因此

$$
\|z(t)\|
\le
\sqrt{\frac{M_\varepsilon}{m_\varepsilon}}
\exp\left(
-\frac{\beta_\varepsilon}{2M_\varepsilon}t
\right)
\|z(0)\|.
$$

物理能量 $E$ 直接来自系统结构、解释最自然，但导数只半负定，需 LaSalle 才能排除 $p=0,q\ne0$。交叉项把 $q$ 与 $p$ 的耦合写入度量，使 derivative 变为负定，从而直接得到定量速率。这正说明 Lyapunov function 不必等于物理能量。

---

### DYN-LYAP-B03

$A$ 是 upper triangular，eigenvalues 为

$$
\lambda_1=-1,\qquad\lambda_2=-2,
$$

故 $A$ Hurwitz。

直接验证

$$
P=
\begin{pmatrix}
1/2&1\\
1&13/4
\end{pmatrix}
$$

可得

$$
A^\top P+PA
=
\begin{pmatrix}-1&0\\0&-1\end{pmatrix}.
$$

又因为

$$
P_{11}=\frac12>0,
\qquad
\det P
=\frac12\frac{13}{4}-1
=\frac58>0,
$$

所以 $P\succ0$。取

$$
V(x)=x^\top Px,
$$

则

$$
\dot V
=x^\top(A^\top P+PA)x
=-\|x\|_2^2.
$$

$P$ 的 eigenvalues 为

$$
\lambda_{\min}(P)=\frac{15-\sqrt{185}}8,
\qquad
\lambda_{\max}(P)=\frac{15+\sqrt{185}}8.
$$

因此

$$
\lambda_{\min}(P)\|x\|^2
\le V(x)
\le\lambda_{\max}(P)\|x\|^2,
$$

且

$$
\dot V
\le-\frac1{\lambda_{\max}(P)}V.
$$

于是

$$
\|x(t)\|
\le
\sqrt{
\frac{15+\sqrt{185}}
{15-\sqrt{185}}
}
\exp\left(
-\frac{4}{15+\sqrt{185}}t
\right)\|x(0)\|.
$$

对欧氏 norm square，

$$
\frac d{dt}\|x\|^2
=x^\top(A+A^\top)x.
$$

取 $x_0=2^{-1/2}(1,1)^\top$，

$$
A+A^\top
=
\begin{pmatrix}-2&6\\6&-4\end{pmatrix},
$$

故

$$
x_0^\top(A+A^\top)x_0
=\frac12(-2+6+6-4)
=3>0.
$$

所以欧氏范数最初增长。矛盾并不存在：$A$ 的 eigenvalues 控制 long-time exponential modes，但非正交 eigenvectors 可使 modes 在短时叠加放大；$V=x^\top Px$ 使用一个倾斜椭圆度量，在该度量中始终严格下降。Lyapunov certificate 保证存在合适的 geometry，不保证用户任意指定的 norm 都逐时刻单调。

## C. 证明、推广与结构联系

### DYN-LYAP-C01

取足够小的 $\varepsilon>0$，使 closed ball

$$
\overline B_\varepsilon
\subset D.
$$

由于 sphere

$$
S_\varepsilon=\{x:\|x\|=\varepsilon\}
$$

compact，$V$ continuous，最小值

$$
m_\varepsilon
=\min_{\|x\|=\varepsilon}V(x)
$$

存在。又因 sphere 不含原点且 $V$ positive definite，

$$
m_\varepsilon>0.
$$

由 $V(0)=0$ 与 continuity，存在 $0<\delta<\varepsilon$，使

$$
\|x_0\|<\delta
\quad\Longrightarrow\quad
V(x_0)<m_\varepsilon.
$$

沿解 $L_fV\le0$，所以只要解留在 $D$，

$$
V(x(t))\le V(x_0)<m_\varepsilon.
$$

若轨道首次到达 sphere $\|x\|=\varepsilon$，则该时刻应有

$$
V(x(t))\ge m_\varepsilon,
$$

与上式矛盾。因此 $\|x(t)\|<\varepsilon$，得到 Lyapunov stability。

“sublevel 留在 $D$ 内”不是装饰。导数 inequality 只在 $D$ 已验证；若轨道能先离开 $D$，便不能继续使用 sign condition。上述 first-exit 论证同时保证它不能触及内选 sphere。

现在假设 $L_fV<0$ 对 $x\ne0$。固定 $0<\eta<\varepsilon$，考虑 compact annulus

$$
A_{\eta,\varepsilon}
=\{x:\eta\le\|x\|\le\varepsilon\}.
$$

连续函数 $-L_fV$ 在其上为正，故存在

$$
c_{\eta,\varepsilon}
=\min_{A_{\eta,\varepsilon}}(-L_fV)>0.
$$

如果某条已被困在小 sublevel 中的轨道从某时刻起永远满足 $\|x(t)\|\ge\eta$，则

$$
\dot V(x(t))
\le-c_{\eta,\varepsilon}.
$$

积分得到

$$
V(x(t))
\le V(x(T))
-c_{\eta,\varepsilon}(t-T),
$$

右侧最终为负，与 $V\ge0$ 矛盾。因此轨道必须进入任意小的 $\eta$-ball；结合 stability，可得 $x(t)\to0$。

这是 local 证明，因为：

- 正定性和 derivative sign 只在 $D$ 假设；
- 初值被限制在一个小 sublevel；
- 没有证明任意远处轨道 bounded 或 forward complete。

一组常用的 global 充分条件是：

1. $f$ locally Lipschitz，解在 bounded sets 上可延拓；
2. $V\in C^1(\mathbb R^n)$ globally positive definite；
3. $V$ proper；
4. $L_fV(x)<0$ 对所有 $x\ne0$。

则每条轨道被困在 compact initial sublevel，故 forward complete；再用任意 compact annulus 上的严格下降证明，得到 global asymptotic stability。

---

### DYN-LYAP-C02

**第一步：Hurwitz 推出积分构造**

若 $A$ Hurwitz，则存在 $M,\alpha>0$ 使

$$
\|e^{At}\|\le Me^{-\alpha t}.
$$

对任意 $Q\succ0$，定义

$$
P=\int_0^\infty e^{A^\top t}Qe^{At}\,dt.
$$

被积矩阵 norm 至多为

$$
\|Q\|M^2e^{-2\alpha t},
$$

故积分绝对收敛。它显然 symmetric。对任意 $x\ne0$，

$$
x^\top Px
=\int_0^\infty
(e^{At}x)^\top Q(e^{At}x)\,dt>0,
$$

因为 $t=0$ 时 integrand 已为 $x^\top Qx>0$，由 continuity 在一小段时间内仍为正。所以 $P\succ0$。

又有

$$
\begin{aligned}
A^\top P+PA
&=\int_0^\infty
\frac d{dt}
\left(e^{A^\top t}Qe^{At}\right)dt\\
&=\lim_{T\to\infty}
e^{A^\top T}Qe^{AT}-Q\\
&=-Q.
\end{aligned}
$$

**第二步：uniqueness**

若 $P_1,P_2$ 都解方程，令 $X=P_1-P_2$，则

$$
A^\top X+XA=0.
$$

因为 $A$ Hurwitz，

$$
\sigma(A^\top)\cap\sigma(-A)=\varnothing;
$$

任意和 $\overline{\lambda_i(A)}+\lambda_j(A)$ 的实部都严格为负，不可能为零。Sylvester equation 的 homogeneous kernel 因而只有 $X=0$。

也可沿 $x(t)=e^{At}x_0$ 观察：

$$
\frac d{dt}x(t)^\top Xx(t)=0.
$$

但 $x(t)\to0$，故常数必须为零。于是 $x_0^\top Xx_0=0$ 对所有 $x_0$ 成立；对 symmetric $X$ 得 $X=0$。

**第三步：某对 $P,Q$ 推出 Hurwitz**

若 $P,Q\succ0$ 且

$$
A^\top P+PA=-Q,
$$

取 $V=x^\top Px$，则

$$
\dot V=-x^\top Qx
\le-\lambda_{\min}(Q)\|x\|^2
\le
-\frac{\lambda_{\min}(Q)}
{\lambda_{\max}(P)}V.
$$

所以

$$
V(t)\le
\exp\left(
-\frac{\lambda_{\min}(Q)}
{\lambda_{\max}(P)}t
\right)V(0).
$$

再用

$$
\lambda_{\min}(P)\|x\|^2
\le V(x)
\le\lambda_{\max}(P)\|x\|^2
$$

得到

$$
\|x(t)\|_2
\le
\sqrt{\frac{\lambda_{\max}(P)}{\lambda_{\min}(P)}}
\exp\left(
-\frac{\lambda_{\min}(Q)}
{2\lambda_{\max}(P)}t
\right)
\|x(0)\|_2.
$$

线性系统所有解指数趋零等价于 $A$ Hurwitz，从而完成三者等价。

Prefactor

$$
\sqrt{\kappa_2(P)}
$$

衡量 Lyapunov ellipsoid 相对欧氏 ball 的扭曲。$P$ 很 ill-conditioned 时，证书仍证明 asymptotic rate，却可能给出很大的 transient envelope；这可能是系统 nonnormality，也可能只是 $Q$ 选择造成的保守性。

---

### DYN-LYAP-C03

先指出一处隐藏的 well-posedness 条件：只写 $U\in C^1$ 可保证 $\nabla U$ continuous，却不必保证 vector field locally Lipschitz。为了使用唯一 flow 与标准 LaSalle，可补充

$$
\nabla U\ \text{locally Lipschitz}
$$

例如假设 $U\in C^2$。

取

$$
E(q,v)
=U(q)-U(q_*)+\frac12\|v\|^2.
$$

则

$$
\begin{aligned}
\dot E
&=\nabla U(q)^\top\dot q+v^\top\dot v\\
&=\nabla U(q)^\top v
+v^\top(-\nabla U(q)-\gamma v)\\
&=-\gamma\|v\|^2\le0.
\end{aligned}
$$

由于 $U(q)-U(q_*)$ positive definite 且 proper，$E$ 对 $(q,v)$ globally positive definite 且 proper。故 initial sublevel

$$
\Omega_{E(q_0,v_0)}
$$

compact。Energy nonincrease 使它 forward invariant；轨道 bounded，而 locally Lipschitz vector field 的 maximal solution 只可能因 state 逃离所有 compact sets 才 finite-time 终止，因此解 forward complete。

零导数集是

$$
Z=\{(q,v):v=0\}.
$$

要在 $Z$ 中保持，必须

$$
\dot v=-\nabla U(q)=0.
$$

若 $q_*$ 是唯一 critical point，则 largest invariant subset 为

$$
M=\{(q_*,0)\}.
$$

LaSalle 对任一 compact initial sublevel 给

$$
(q(t),v(t))\to(q_*,0).
$$

再结合 $E$ 的正定性，得到 global asymptotic stability。

若 critical points 不唯一，则一般只能得到

$$
\operatorname{dist}
\left(
(q(t),v(t)),
\{(q,0):\nabla U(q)=0\}
\right)\to0.
$$

是否收敛到单个 critical point 还需额外结构，如 isolated equilibria、Łojasiewicz inequality 等。

对

$$
U(q)=\frac14(q^2-1)^2,
\qquad
U'(q)=q(q^2-1),
$$

critical points 为

$$
q=-1,0,1.
$$

因此 equilibria 为

$$
(-1,0),\quad(0,0),\quad(1,0).
$$

$q=\pm1$ 是 minima，$q=0$ 是 local maximum。Energy decrease 排除 sustained gain，却不决定落入哪个 basin；从两个 minima 精确出发甚至一直停在那里。因此“energy 下降”不是“所有初值到同一个 minimizer”。

## D. 诊断、反例与证书审计

### DYN-LYAP-D01

**1. 假。** 取二维纯旋转

$$
\dot x=-y,\qquad\dot y=x,
\qquad
V=x^2+y^2.
$$

$V$ positive definite 且 $\dot V=0$，但非零轨道为周期圆，不趋于原点。

**2. 真，但要保留 continuity 与 proper 的标准定义。** Proper 意味着 compact sets 的 preimage compact；$(-\infty,c]$ 与值域相交后可用 sublevel 版本。对连续 radially-unbounded $V$，$\Omega_c$ closed 且 bounded，有限维中即 compact。

**3. 假。** $\dot x=-x^3$，$V=x^2/2$，则 $\dot V=-x^4<0$，但

$$
x(t)=\frac{x_0}{\sqrt{1+2x_0^2t}}
$$

只有 polynomial decay，不是 exponential。

**4. 假。** B03 的 $A$ eigenvalues 都在左半平面，但特定 $x_0$ 上

$$
\frac d{dt}\|x(t)\|^2\bigg|_{0}=3>0.
$$

**5. 真。** 这正是 continuous Lyapunov theorem；积分构造给 existence/positive definiteness，Sylvester spectrum 给 uniqueness。

**6. 假。** Objective nonincrease 只给标量值收敛。Minimizer 可能不唯一，trajectory 也可能沿 flat directions 保持不变。还需 compactness、gradient structure、PL/convexity 或其他几何条件才能加强结论。

**7. 基本正确，但必须连同定号性与区域条件。** 对 discrete map $x_{k+1}=F(x_k)$，严格条件是

$$
V(F(x))-V(x)<0
$$

对验证区域内每个 $x\ne0$ 成立，且 $V$ positive definite、$F(0)=0$。

**8. 原句不充分。** 若“下降”只有 $\le0$，通常只给 uniform stability；若要 uniform asymptotic/exponential stability，需要 common $V$ 具有对参数 uniform 的 state bounds 与 strict margin，例如

$$
\alpha_1(\|x\|)\le V(x)\le\alpha_2(\|x\|),
\qquad
L_{f_\rho}V(x)\le-\alpha_3(\|x\|)
$$

对所有 $\rho$ 同时成立。

**9. 假。** 有限 samples 不覆盖 continuum，网络或 polynomial 可在样本之间翻正。

**10. 假。** EBM energy 本身只定义 landscape。还需指定 sampling dynamics；若用 Langevin dynamics，还存在 diffusion，正确对象是 generator，而不是只看 energy minima。

---

### DYN-LYAP-D02

**1. 半正定函数丢失坐标**

取

$$
\dot x_1=-x_1,\qquad\dot x_2=0,
\qquad
V(x)=x_1^2.
$$

则

$$
V\ge0,\qquad\dot V=-2x_1^2\le0,
$$

但 $V(0,x_2)=0$ 对任意 $x_2$ 成立，完全不控制 $x_2$。轨道只趋向 equilibrium line $x_1=0$，不必趋向原点。

**2. 零导数与无 attraction**

取纯旋转

$$
\dot x=-y,\qquad\dot y=x,
\qquad V=x^2+y^2.
$$

所有非零轨道保持固定半径。原点 Lyapunov stable，但不 attractive。

**3. 非 proper 与 escape**

考察

$$
\dot x=x(x^2-1),
\qquad
V=x^2e^{-x^2}.
$$

$V(0)=0$ 且 $x\ne0$ 时 $V(x)>0$，所以 globally positive definite；但

$$
V(x)\to0
\quad(|x|\to\infty),
$$

因而不 proper。求导：

$$
V'(x)=2xe^{-x^2}(1-x^2),
$$

从而

$$
\dot V
=-2x^2e^{-x^2}(x^2-1)^2
\le0.
$$

然而 $x_0>1$ 时 $\dot x>0$，且大 $x$ 时 $\dot x\sim x^3$，解会 finite-time blow up。这里“energy 下降”既不保证 state bounded，也不保证 forward completeness。这个 $V$ 仍可证明原点 local stability；失败的是 global 升级。

**4. Continuous stable，Euler unstable**

对

$$
\dot x=-x
$$

exact flow 为 $x(t)=e^{-t}x_0$。Explicit Euler 给

$$
x_{k+1}=(1-h)x_k.
$$

离散稳定当且仅当

$$
|1-h|<1
\iff0<h<2.
$$

$h>2$ 时幅值增长；$h=2$ 时等幅振荡。Continuous derivative 不能代替 discrete difference。

**5. Samples 之间的 violation**

令 sample set

$$
S=\{-1,0,1\}
$$

并取

$$
g(x)=-0.1+0.2\sin^2(\pi x).
$$

对所有 $s\in S$，

$$
g(s)=-0.1<0,
$$

但

$$
g(1/2)=0.1>0.
$$

若 $g=L_fV$，需要 region-wide 工具，例如：

- 解析求全局 maximum；
- Lipschitz constant 配合足够细的 covering net 与 margin；
- interval bound propagation；
- branch-and-bound；
- SMT/MILP verifier；
- polynomial 情形的 SOS certificate。

只有 sample points 与 margin、覆盖半径、regularity bound 共同出现时，才可能升级为全区域结论。

---

### DYN-LYAP-D03

这份报告目前只能支持“sampled candidate training 与 numerical stress test”，不能支持 global exponential theorem。

**1. Candidate 本体**

至少要声明：

$$
f_\theta(0)=0,\qquad
V_\phi(0)=0,
$$

以及 $V_\phi$ 的 differentiability。若用 arbitrary neural network 输出，$V(0)=0$ 与非负性不会自动成立。常见结构是

$$
V_\phi(x)=\|\psi_\phi(x)-\psi_\phi(0)\|^2+\epsilon\|x\|^2,
$$

但仍需验证上界、properness 与 derivative。

**2. Domain**

必须给出明确 compact region

$$
\Omega\subset\mathbb R^n
$$

或 certified sublevel $\Omega_c$。训练分布的 support、bounding box 与实际 reachable set 不能含糊混用。

**3. Samples 不是 proof**

$10^6$ 仍是 finite。Optimizer 返回低 loss 也不能证明约束处处成立；RK4 仿真只探索有限 trajectories、有限时域和一种 solver。

**4. Learner–falsifier**

可以循环：

1. learner 最小化 task loss 与 certificate violation；
2. falsifier 在 $\Omega$ 最大化

$$
-V_\phi(x)+m_1\|x\|^2
$$

或

$$
L_{f_\theta}V_\phi(x)+m_2\|x\|^2;
$$

3. 把 counterexample 加入训练集；
4. 重训后再找；
5. 最后由独立 formal verifier 封闭整个 region。

Adversarial search 能找错，不能因“没找到”就替代 proof。

**5. Activation 差异**

- ReLU：piecewise affine，$V$ 可能 nonsmooth；经典 $C^1$ Lie derivative 要改用 generalized derivative，或构造 smooth outer form；MILP 可利用分段线性结构但组合爆炸；
- smooth activation：Lie derivative经典可用，但 global nonlinear bounds 与 transcendental verification 更难；
- normalization：可能引入 division、data-dependent statistics、train/eval mismatch 或 singular denominator，必须固定运行模式并验证 denominator bounds。

**6. Exponential margin**

需要类似

$$
c_1\|x\|^2
\le V_\phi(x)
\le c_2\|x\|^2,
\qquad
L_fV_\phi(x)
\le-c_3\|x\|^2
$$

或

$$
L_fV_\phi\le-\alpha V_\phi.
$$

前一种给

$$
\|x(t)\|
\le
\sqrt{\frac{c_2}{c_1}}
e^{-c_3t/(2c_2)}\|x_0\|.
$$

只有 positivity 与 strict negativity、没有 quantitative uniform margins，不足以声称 exponential。

**7. 三个演化对象**

- Continuous field：验证 $L_fV$；
- RK4 map $F_h$：验证 $V(F_h(x))-V(x)$，并声明 $h$、adaptive policy 与 truncation assumptions；
- implementation：还需考虑 rounding、overflow、quantization 与 library semantics，可把误差建模为 disturbance。

**8. Global claim**

需要 global state bounds / properness、global derivative inequality、forward completeness，以及网络在无界域上的行为控制。只在 bounded training box 中验证，最多是 regional certificate。

**9. Disturbance**

对

$$
\dot x=f(x,w)
$$

更诚实的目标可能是 ISS-like inequality

$$
\dot V
\le-\alpha(\|x\|)+\sigma(\|w\|),
$$

它导向 practical/ultimate boundedness，而不是无扰动原点 convergence。

**10. 六级证据阶梯**

1. sampled training loss；
2. adversarial falsification；
3. local analytic certificate；
4. formal regional continuous-time certificate；
5. formal discrete/implementation-aware certificate；
6. uncertainty-aware system-level guarantee。

该团队目前处于 Level 1，加上有限 numerical stress test；若使用有效 adversarial search，可接近 Level 2，但仍没有 formal regional proof。

## E. AI 迁移、综合推导与研究设计

### DYN-LYAP-E01

对 gradient flow，

$$
\dot\theta=-\nabla L(\theta),
$$

取 $V=L-L_*$，则

$$
\dot V
=\nabla L(\theta)^\top\dot\theta
=-\|\nabla L(\theta)\|^2.
$$

若 PL inequality 成立，

$$
\frac12\|\nabla L\|^2\ge\mu V,
$$

则

$$
\dot V\le-2\mu V.
$$

由 Grönwall inequality，

$$
L(\theta(t))-L_*
\le
e^{-2\mu t}
\left(L(\theta(0))-L_*\right).
$$

这是 objective gap 的 exponential decay。PL 本身不要求 convexity，也不自动保证 minimizer 唯一；因此不能仅从 gap decay 得到 $\theta(t)$ 到某个预指定 parameter 的距离界。

若 $L$ 是 $\mu$-strongly convex，则 minimizer $\theta_*$ 唯一，且

$$
L(\theta)-L_*
\ge\frac\mu2\|\theta-\theta_*\|^2.
$$

若又 $L_s$-smooth，则

$$
L(\theta)-L_*
\le\frac{L_s}{2}\|\theta-\theta_*\|^2.
$$

结合 gap decay：

$$
\frac\mu2\|\theta(t)-\theta_*\|^2
\le
e^{-2\mu t}
\frac{L_s}{2}\|\theta(0)-\theta_*\|^2.
$$

所以

$$
\|\theta(t)-\theta_*\|
\le
\sqrt{\frac{L_s}{\mu}}
e^{-\mu t}
\|\theta(0)-\theta_*\|.
$$

对

$$
L(\theta)=\frac14\theta^4,
$$

gradient flow 为

$$
\dot\theta=-\theta^3.
$$

非零初值的解是

$$
\theta(t)
=\frac{\theta_0}
{\sqrt{1+2\theta_0^2t}}.
$$

它趋于零，所以原点 asymptotically stable；但 decay 为 $t^{-1/2}$。若存在 uniform $M,\alpha>0$ 使

$$
|\theta(t)|
\le Me^{-\alpha t}|\theta_0|,
$$

则 polynomial/exponential 比值在大 $t$ 发散，矛盾。因此不是 exponentially stable。

对 preconditioned flow，

$$
\dot\theta=-G(\theta)^{-1}\nabla L(\theta),
$$

若 $G(\theta)$ symmetric positive definite，则

$$
\dot L
=-\nabla L^\top G^{-1}\nabla L
\le0.
$$

若要 uniform rate，通常还需

$$
mI\preceq G(\theta)\preceq MI.
$$

$G$ 选择了 parameter space 的 Riemannian metric；natural gradient 用 Fisher-like metric，使“steepest”相对于模型分布 geometry 而非原始 Euclidean coordinates 定义。

最后要严格分账：

- training loss 下降：关于训练 objective；
- parameter convergence：关于 trajectory 在 parameter space；
- test performance：关于未知数据分布上的 task metric；
- flat-minimum selection：关于 implicit bias 与 geometry。

Lyapunov 对第一、二类可能给结论，但不会凭空证明 generalization。

---

### DYN-LYAP-E02

取 total mechanical energy

$$
E(q,v)
=L(q)-L_{\inf}
+\frac12\|v\|^2.
$$

若 $L_{\inf}$ 是 lower bound，则 $E\ge0$，且

$$
\dot E
=\nabla L(q)^\top v
+v^\top(-\nabla L(q)-\gamma v)
=-\gamma\|v\|^2\le0.
$$

因此

$$
L(q(t))+\frac12\|v(t)\|^2
\le
L(q_0)+\frac12\|v_0\|^2.
$$

若 $L$ 的 sublevel sets compact，则 $q(t)$ bounded；上式也使 $v(t)$ bounded。配合 locally Lipschitz vector field，轨道 forward complete。

零导数集为 $v=0$。留在其中还要求

$$
\dot v=-\nabla L(q)=0.
$$

故 LaSalle 给

$$
\operatorname{dist}
\left(
(q(t),v(t)),
\{(q,0):\nabla L(q)=0\}
\right)\to0.
$$

这个集合包含 local minima、saddles、maxima 与可能的 critical manifolds。LaSalle 不替优化算法选择 global minimizer，也不自动把 set convergence 加强为 point convergence。

对 double well，

$$
L(q)=\frac14(q^2-1)^2,
\qquad
L''(q)=3q^2-1.
$$

三个 equilibria 是

$$
(-1,0),\quad(0,0),\quad(1,0).
$$

$q=\pm1$ 时 $L''=2>0$，linearized matrix

$$
\begin{pmatrix}
0&1\\-2&-\gamma
\end{pmatrix}
$$

Hurwitz，所以两个 minima locally asymptotically stable。$q=0$ 时 $L''=-1$，linearized characteristic polynomial

$$
\lambda^2+\gamma\lambda-1
$$

有一正一负根，所以为 saddle。精确处于其 stable manifold 的初值仍可能趋向 saddle；一般初值则落入两个 minima 的某个 basin。

在 strict local minimizer $q_*$ 附近，令 $e=q-q_*$，$H=\nabla^2L(q_*)\succ0$。Linearized heavy-ball system 为

$$
\frac d{dt}
\begin{pmatrix}e\\v\end{pmatrix}
=
\begin{pmatrix}
0&I\\
-H&-\gamma I
\end{pmatrix}
\begin{pmatrix}e\\v\end{pmatrix}.
$$

它 Hurwitz，因此可解 Lyapunov equation 得 local quadratic candidate

$$
V_{\rm lin}(e,v)
=
\begin{pmatrix}e\\v\end{pmatrix}^\top
P
\begin{pmatrix}e\\v\end{pmatrix}.
$$

也可从

$$
L(q)-L(q_*)+\frac12\|v\|^2+\varepsilon e^\top v
$$

出发，选择足够小的 $\varepsilon>0$。交叉项吸收 position–velocity coupling，Hessian 正定性提供 local restoring force。非线性 Taylor remainder 足够小时，可保留 strict derivative。

三种陈述互不等价：

- objective decrease：$L(q(t))$ 单调；
- total energy decrease：$L(q(t))+\|v(t)\|^2/2$ 单调；
- parameter norm decrease：$\|q(t)-q_*\|$ 单调。

Momentum 中 objective 可暂时上升而 kinetic energy 转换为 potential energy；total energy 仍下降。即使 total energy 下降，position norm 也可能振荡。

---

### DYN-LYAP-E03

下面给出一个可复用的研究方案，以 Neural ODE

$$
\dot x=f_\theta(x)
$$

为例。

#### 1. Mathematical contract

先固定：

- state $x\in\mathbb R^n$；
- target equilibrium $x_*=0$ 或 target set $\mathcal A$；
- verification domain $\Omega$；
- autonomous / time-varying；
- vector field regularity 与 forward solution 的定义；
- deployment solver $F_{h,\theta}$。

若 $f_\theta(0)\ne0$，任何关于原点 equilibrium stability 的后续讨论都无效。

#### 2. Candidate selection

- 局部近线性：quadratic $x^\top Px$；
- polynomial dynamics：SOS；
- 已知机械/优化结构：physical/objective energy 加 cross terms；
- 高维复杂 dynamics：structured neural candidate，例如强制 $V(0)=0$ 和基础 quadratic lower bound。

Candidate choice 要服务于可验证性，而不仅是表达能力。

#### 3. Quantitative certificate

在 $\Omega$ 上目标为

$$
c_1\|x\|^2
\le V_\phi(x)
\le c_2\|x\|^2,
$$

$$
\nabla V_\phi(x)^\top f_\theta(x)
\le-c_3\|x\|^2,
\qquad x\ne0,
$$

其中 $c_1,c_2,c_3>0$。同时报告验证到的 numerical margins，而不是只报告 sign。

#### 4. Learner–falsifier–verifier

1. Learner 同时优化 task loss 与 violation penalties；
2. gradient-based / global falsifier 搜索最坏状态；
3. counterexamples 回流训练；
4. 独立 branch-and-bound、SMT、MILP、interval 或 SOS verifier 覆盖整个 $\Omega$；
5. 若失败，保存 counterexample 与未证区域。

#### 5. Regional basin certificate

寻找最大可验证 $c$，使

$$
\Omega_c=\{x:V_\phi(x)\le c\}
\subset\Omega
$$

且 derivative inequality 在 $\Omega_c$ 成立。则 $\Omega_c$ 是 basin 的 certified inner approximation，而不是精确 basin。

#### 6. Discrete solver

对实际部署 map 单独验证

$$
V_\phi(F_{h,\theta}(x))-V_\phi(x)
\le-\tilde c_3\|x\|^2.
$$

必须声明 fixed/adaptive step、容差、最大步长和 solver failure policy。Continuous certificate 仅作设计先验，不能替换此步。

#### 7. Model error 与 disturbance

若真实 dynamics 为

$$
\dot x=f_\theta(x)+d(x,t),
$$

目标改为

$$
\dot V
\le-\alpha\|x\|^2+\beta\|d\|^2.
$$

由此导出 ultimate bound 或 ISS claim；不要继续声称无扰动式 exact convergence。

#### 8. 变体

- 参数/模式 switching：寻找 common Lyapunov function；
- time-varying dynamics：验证 $\partial_tV+\nabla V^\top f$；
- SDE：使用 Itô generator；
- target manifold：改用到集合的 bounds 与 set invariance。

#### 9. Ablation

| 版本 | Training | Region-wide proof | Discrete proof | 可声称结论 |
|---|---:|---:|---:|---|
| no certificate | task only | no | no | empirical task result |
| sample-only | sampled Lyapunov penalty | no | no | sampled constraint fit |
| formal regional | penalty + verifier | yes | no | continuous regional theorem |
| formal + discrete | 同上 | yes | yes | 指定 solver/step 的 regional theorem |

#### 10. Failure reporting

报告：

- verifier timeout 与“找到反例”的区别；
- 未覆盖 cells；
- 最小 positivity/negativity margin；
- worst counterexample；
- solver step sensitivity；
- distribution shift stress test；
- certificate 与 task accuracy 的 trade-off。

#### 11. Task interface

稳定性只约束 trajectory behavior。还要单独报告 classification、control cost、generation quality、calibration 或 robustness。一个稳定但始终趋向错误 equilibrium 的模型仍然无用。

#### 12. 不夸大的 theorem template

> 假设 $f_\theta$ 在 compact region $\Omega$ 上 locally Lipschitz，$f_\theta(0)=0$。Formal verifier 证明 $c_1\|x\|^2\le V_\phi(x)\le c_2\|x\|^2$ 且 $L_{f_\theta}V_\phi(x)\le-c_3\|x\|^2$ 对所有 $x\in\Omega_c\setminus\{0\}$ 成立，其中 $\Omega_c\subset\Omega$ compact。则 continuous-time model 的原点在 $\Omega_c$ 内 exponentially stable，并满足指定 state bound。该结论不覆盖 $\Omega_c$ 外初值、未建模 disturbance、随机 dynamics、数值 solver 或 finite-precision implementation；这些对象另行验证。

### Certificate card

| 字段 | 必填内容 |
|---|---|
| Model | $f_\theta$ 版本、权重 hash、activation |
| Evolution object | continuous flow / RK map / SDE |
| Target | equilibrium 或 invariant set |
| Domain | $\Omega$ 与 certified $\Omega_c$ |
| Candidate | $V_\phi$ 结构、版本、normalization |
| State bounds | $c_1,c_2$ 与 norm |
| Decrease margin | $c_3$ 或 class-$\mathcal K$ function |
| Verifier | 方法、精度、timeout、完整性假设 |
| Solver | method、step/tolerance、是否单独验证 |
| Robustness | disturbance/model-error bound |
| Result | local/regional/global；stable/asymptotic/exponential |
| Exclusions | 未覆盖区域、noise、implementation、task correctness |
| Counterexamples | worst found state 与复现入口 |
| Task metrics | 与 certificate 独立报告 |

这张卡的核心不是“证明稳定”四个字，而是让第三方准确回答：证明了哪个数学对象，在什么区域，用什么 margin，依赖哪些假设，以及结论没有覆盖什么。

## 复盘：15 题对应的能力

| 层级 | 核心能力 |
|---|---|
| A | 定义、定理条件、连续/离散/随机对象分账 |
| B | ROA、LaSalle、交叉项、Lyapunov 方程与速率手算 |
| C | direct theorem、矩阵等价定理、机械系统 global 证明 |
| D | 反例、缺条件诊断、neural certificate 证据审计 |
| E | gradient flow、momentum 与 verified learned dynamics 研究设计 |

> [!success] 最低掌握标准
> 不看正文，能够重建 C01 与 C02；面对新系统，先给验证区域和结论强度，再计算 $L_fV$；面对 AI 论文，能把 sample evidence、formal continuous certificate、discrete implementation guarantee 与 task performance 分为四张账。

