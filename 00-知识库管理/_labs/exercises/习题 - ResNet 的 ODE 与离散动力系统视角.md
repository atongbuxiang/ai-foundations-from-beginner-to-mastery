---
type: exercise
status: draft
area: [neural-networks/residual-stability, ode, numerical-analysis]
topic: "[[ResNet 的 ODE 与离散动力系统视角]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - ResNet 的 ODE 与离散动力系统视角]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - ResNet 的 ODE 与离散动力系统视角

## A

### NN-ROD-A01
把 $x_{k+1}=x_k+h f(x_k,t_k;\theta_k)$ 中的 state、depth time、step、vector field 与 residual branch 一一对应，并写出 shape/单位合同。

### NN-ROD-A02
为什么“层数翻倍”可能表示 horizon 翻倍，也可能表示 step 减半？要声称固定 $[0,T]$ 上网格加密，必须怎样设置 $h$ 与 branch magnitude？

### NN-ROD-A03
分别定义 continuous dynamical stability、absolute numerical stability、discrete perturbation stability 与 optimization stability；给出不能互相替代的原因。

## B

### NN-ROD-B01
对 $\dot x=-2x,x(0)=1,T=1$，计算 Euler 在 $N=1,2,4,10$ 时的结果并与 $e^{-2}$ 比较。

### NN-ROD-B02
对 $\dot x=\lambda x$，推导 Euler multiplier 与 absolute stability condition。判断 $(h,\lambda)=(1,-3),(1,-1),(0.1,-20),(0.1,-5+8i)$ 是否稳定。

### NN-ROD-B03
对光滑 exact trajectory 推导单步 defect。若 $\sup\|\ddot x\|=6,h=0.05$，给出 $\|\tau_k\|$ 上界。

## C

### NN-ROD-C01
在 $f$ 对 state 为 $L_f$-Lipschitz、$\|\tau_k\|\le Ch^2$、$e_0=0$ 下，完整推导 Euler global error bound，不得只写“由 Gronwall”。

### NN-ROD-C02
对线性 time-varying ODE $\dot x=A(t)x$ 写出 Euler discrete backprop 与 continuous adjoint。说明有限步时二者的计算对象为何不同。

### NN-ROD-C03
构造一个非 injective residual Euler map，并解释它为何不能是满足唯一性条件的同维 exact ODE flow 在正时间的映射。

## D

### NN-ROD-D01
每层参数独立是否排除 ODE 解释？用 piecewise-constant $\theta_N(t)$ 回答，并列出跨深度族收敛还需要的三个条件。

### NN-ROD-D02
为 adaptive Neural ODE 设计系统审计表，至少包括 solver、rtol/atol、NFE、rejected steps、最大步数、failure、dtype、wall time 与 gradient route。

### NN-ROD-D03
普通 ResNet 在 stage 边界把 $32\times32\times64$ 改为 $16\times16\times128$。给出三种解释：hybrid jump、augmented/embedded state、纯离散 map；各自不能保留哪些普通 ODE 性质？

## E

### NN-ROD-E01
反驳：“任何写成 $x+F(x)$ 的网络都是 Neural ODE，因此自动可逆且数值稳定。”至少给出 step scale、injectivity 和 stability region 三个反例。

### NN-ROD-E02
设计一个验证 ResNet 是否形成固定-horizon ODE 极限的实验：规定跨深度参数插值、reference solver、误差率、Jacobian 与 compute 报告。

### NN-ROD-E03
一个 continuous adjoint 实现比 discrete backprop 省内存，却与有限差分梯度不符。列出 trajectory reconstruction、solver tolerance、adaptive control flow、stiffness 和 RNG/state 五条排查路径。

