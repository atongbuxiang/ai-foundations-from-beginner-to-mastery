---
type: solution
status: draft
area: [neural-networks/residual-stability, ode, numerical-analysis]
topic: "[[ResNet 的 ODE 与离散动力系统视角]]"
exercise: "[[习题 - ResNet 的 ODE 与离散动力系统视角]]"
sources: ["[[S-2018-Lu-Numerical-ODE-Networks]]", "[[S-2018-Chen-Neural-ODE]]", "[[S-2018-Haber-Ruthotto-Stable-Architectures]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - ResNet 的 ODE 与离散动力系统视角

## A

### NN-ROD-A01

- $x_k\in\mathbb R^D$：第 $k$ 层 state；batch 形式可为 $(B,D)$ 或更高阶固定 state shape；
- $t_k$：depth-time；
- $h=t_{k+1}-t_k$：step，带 time 单位；
- $f(x_k,t_k;\theta_k)$：vector field，shape 与 $x_k$ 相同但单位为 state/time；
- $F_k(x_k)=hf(x_k,t_k;\theta_k)$：residual branch，shape/单位与 $x_k$ 相同。

addition 还要求 dtype/device/layout 可执行兼容。

### NN-ROD-A02
若 $h$ 不变，层数从 $N$ 变 $2N$，终止时间从 $Nh$ 变 $2Nh$；若固定 $T$，则必须令

$$
h_N=T/N,
$$

并让单层 residual 为

$$
F_{N,k}=h_Nf_{N,k}=O(1/N).
$$

否则不是同一 horizon 的 grid refinement。

### NN-ROD-A03

- continuous dynamical stability：exact trajectories 对初值/forcing 的连续依赖；
- absolute numerical stability：test equation 的离散 multiplier 是否受控；
- discrete perturbation stability：有限层 map 对输入和每步误差的放大；
- optimization stability：参数更新中的 loss/gradient/update 是否受控。

它们作用在不同变量与算法上。例如 exact ODE 稳定而 Euler step 太大可数值不稳；forward contraction 也不让参数 loss 变 convex。

## B

### NN-ROD-B01
Euler multiplier 为 $1-2/N$：

| $N$ | $x_N=(1-2/N)^N$ | 与 $e^{-2}\approx0.135335$ 的绝对误差 |
|---:|---:|---:|
| 1 | $-1$ | $1.135335$ |
| 2 | $0$ | $0.135335$ |
| 4 | $0.5^4=0.0625$ | $0.072835$ |
| 10 | $0.8^{10}=0.1073741824$ | $0.027961$ |

这里 $N$ 增大同时令 $h=1/N$，所以是在固定 horizon 上加密。

### NN-ROD-B02
Euler：

$$
x_{k+1}=(1+h\lambda)x_k.
$$

绝对稳定圆盘为 $|1+h\lambda|\le1$；严格衰减用 $<1$。

- $(1,-3)$：multiplier $-2$，模 2，不稳定；
- $(1,-1)$：multiplier 0，稳定；
- $(0.1,-20)$：multiplier $-1$，位于边界，norm 不衰减；
- $(0.1,-5+8i)$：multiplier $0.5+0.8i$，模 $\sqrt{0.89}\approx0.943<1$，稳定。

### NN-ROD-B03
Taylor 公式给

$$
\tau_k=\frac{h^2}{2}\ddot x(\xi_k),
$$

所以

$$
\|\tau_k\|
\le\frac12\cdot6\cdot0.05^2
=3\cdot0.0025
=0.0075.
$$

## C

### NN-ROD-C01
误差递推：

$$
\begin{aligned}
e_{k+1}
&=x(t_{k+1})-x_{k+1}\\
&=e_k+h[f(x(t_k),t_k)-f(x_k,t_k)]+\tau_k.
\end{aligned}
$$

取 norm 并用 Lipschitz：

$$
d_{k+1}\le(1+hL_f)d_k+Ch^2,
\qquad d_k=\|e_k\|.
$$

$d_0=0$，展开几何和：

$$
d_k
\le Ch^2\sum_{j=0}^{k-1}(1+hL_f)^j
=Ch^2\frac{(1+hL_f)^k-1}{hL_f}.
$$

故

$$
d_k
\le\frac{Ch}{L_f}\left[(1+hL_f)^k-1\right]
\le\frac{Ch}{L_f}(e^{L_ft_k}-1).
$$

固定 $T$ 时右边为 $O(h)$。若 $L_f=0$，直接由求和得 $d_k\le CT h$。

### NN-ROD-C02
Euler forward：

$$
x_{k+1}=(I+hA_k)x_k.
$$

离散 reverse mode：

$$
a_k=(I+hA_k)^\mathsf Ta_{k+1}.
$$

连续 adjoint：

$$
\dot a(t)=-A(t)^\mathsf Ta(t),
$$

从终点向前述时间的反方向求解。有限 $h$ 时，离散对象是 $\prod_k(I+hA_k)$ 的精确导数；连续对象是 fundamental solution 的伴随，再由某 solver 近似。除非误差趋零且轨迹/参数插值一致，两者不完全相同。

### NN-ROD-C03
取

$$
F(x)=-x/h.
$$

则 Euler residual map

$$
G(x)=x+hF(x)=0
$$

把所有初值映到同一点，不 injective。满足局部 Lipschitz 与唯一性的同维 ODE flow 在有限时间可由反向 flow 恢复初值，因此其 time-$t$ map 是 injective；该塌缩 map 不能是这种 exact flow。

## D

### NN-ROD-D01
不排除。定义

$$
\theta_N(t)=\theta_{N,k},
\qquad t\in[t_k,t_{k+1})
$$

即可得到 time-dependent piecewise-constant field。要让跨深度模型趋向同一极限，还至少需要：

1. $h_N=T/N\to0$ 且 residual 为 $h_Nf_N$；
2. $f_N$ 对 state 有统一 Lipschitz/growth bound；
3. $\theta_N$ 或 $f_N$ 在适当函数空间收敛/紧致，并有一致初值和 horizon。

### NN-ROD-D02
报告表至少包括：solver 名称与 method order；`rtol/atol`；每样本/批次 NFE 分布；accepted/rejected steps；min/max/mean step；max steps 与 termination reason；failure/NaN rate；forward/backward dtype；wall time 与 memory；discrete backprop、continuous adjoint 或 checkpoint adjoint；reference tolerance 下的 state/gradient error。

### NN-ROD-D03

- hybrid jump：stage 内是 ODE，边界用离散 jump map；跨 jump 的同一 flow 可逆性/维度保持不适用；
- augmented/embedded state：先嵌入更大固定 state，再用 mask/readout 表示 shape 变化；需要额外坐标，原网络未必等价；
- 纯离散 map：承认 stage boundary 是一般投影；不再声称全网是一条经典 ODE flow。

下采样通常丢信息，不能保留同维 flow 的 injectivity。

## E

### NN-ROD-E01

1. step scale：$x+F(x)$ 若 $F$ 不随 depth 缩小，不是固定 horizon 的 $h\to0$ family；
2. injectivity：$F(x)=-x$ 给 $x^+=0$；
3. stability：$F(x)=-3x$ 给 multiplier $-2$，虽然对应连续 $\dot x=-3x$ 衰减，$h=1$ Euler 却爆炸。

所以 residual form 只给 Euler-like algebra，不自动给 Neural ODE 极限、可逆或稳定。

### NN-ROD-E02
可取同一个平滑 $f_\theta(x,t)$ 与固定 $T$，在 $N=8,16,32,64$ 用 $h=T/N$、按 $t_k$ 采样共享参数插值。用高精度自适应 solver 作 reference，报告 final-state error 与 trajectory error 的 log-log slope 是否趋近 1；比较 discrete Jacobian product 与 continuous variational solution；同时报告 NFE/FLOPs、memory、wall time。训练比较必须固定数据、目标与参数函数容量，不能让每个深度独立改变 $f$ 后仍声称 discretization convergence。

### NN-ROD-E03
排查顺序：

1. 保存 forward checkpoints，比较 backward reconstruction trajectory；
2. 同时收紧 forward/backward tolerance，画 gradient error curve；
3. 固定 step 关闭 adaptive control，隔离 step-selection 不连续；
4. 检查 stiffness、反向不稳定和最大步失败；
5. 固定 dropout/RNG、normalization state 与事件处理。

再用 small problem 的 discrete backprop 和中心差分作 reference；省内存不构成正确性证据。
