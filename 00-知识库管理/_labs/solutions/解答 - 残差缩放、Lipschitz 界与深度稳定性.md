---
type: solution
status: draft
area: [neural-networks/residual-stability, lipschitz, perturbation-analysis]
topic: "[[残差缩放、Lipschitz 界与深度稳定性]]"
exercise: "[[习题 - 残差缩放、Lipschitz 界与深度稳定性]]"
sources: ["[[S-2018-Haber-Ruthotto-Stable-Architectures]]", "[[S-2022-Su-8994-Why-Residual]]", "[[S-2018-Su-6051-Lipschitz约束]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 残差缩放、Lipschitz 界与深度稳定性

## A

### NN-RSL-A01

- global：对整个声明 domain 的所有 $x,y$ 成立；
- restricted-domain：只在集合 $\Omega$ 上成立；
- local-Jacobian：某点或邻域的 $\|J(x)\|$；
- empirical：有限样本、有限方向的观测；
- expected：对数据、参数或方向随机性取期望。

全局 composition theorem 可直接使用每层 global constants；若已证明 trajectory 始终在某 tube，也可使用该共同 restricted-domain uniform constants。有限 empirical/expected 值不能直接替代 uniform theorem premise。

### NN-RSL-A02

$$
\delta_{\ell+1}
=\delta_\ell+\alpha_\ell(F_\ell(x_\ell)-F_\ell(\widetilde x_\ell)).
$$

所以

$$
\|\delta_{\ell+1}\|
\le(1+|\alpha_\ell|L_\ell)\|\delta_\ell\|.
$$

若 $\alpha_\ell<0$，三角不等式中的 branch 大小仍是 $|\alpha_\ell|\|\Delta F\|$；漏绝对值会给出伪小甚至负的 upper bound。

### NN-RSL-A03
$1/N$ 使 worst-case 累积 $\sum\alpha L=O(1)$；$1/\sqrt N$ 在零均值、弱相关 increments 下使 $N\alpha^2=O(1)$，自然控制 variance。$1/N$ 只是一个 uniform-bound 充分缩放，不必对优化/表达最优；$1/\sqrt N$ 的 deterministic exponent 可为 $O(\sqrt N)$，一般不 uniform。

## B

### NN-RSL-B01
每层 $q=1.2$：

$$
d_1\le1.2(0.5)+0.01=0.61,
$$

$$
d_2\le1.2(0.61)+0.02=0.752,
$$

$$
d_3\le1.2(0.752)=0.9024.
$$

展开式：

$$
d_3
\le1.2^3(0.5)+1.2^2(0.01)+1.2(0.02)
=0.864+0.0144+0.024
=0.9024.
$$

### NN-RSL-B02
multiplier 是 $m=1-3\alpha$：

| $\alpha$ | $m$ | 类型 |
|---:|---:|---|
| $0$ | $1$ | 不衰减 |
| $0.2$ | $0.4$ | 同号衰减 |
| $1/3$ | $0$ | 一步塌缩 |
| $0.5$ | $-0.5$ | 振荡衰减 |
| $2/3$ | $-1$ | 临界、norm 不变 |
| $1$ | $-2$ | 振荡发散 |

### NN-RSL-B03

$$
\prod(1+|\alpha_\ell|L_\ell)=1.2^2=1.44.
$$

指数界：

$$
e^{0.2+0.2}=e^{0.4}\approx1.491825.
$$

因为 $1+z\le e^z$，exponential bound 更松，但容易按总 budget 概括。

## C

### NN-RSL-C01
令 $\delta=x-y,\Delta F=F(x)-F(y)$。上界：

$$
\|\delta+\alpha\Delta F\|
\le\|\delta\|+|\alpha|\|\Delta F\|
\le(1+|\alpha|L)\|\delta\|.
$$

反三角不等式：

$$
\|\delta+\alpha\Delta F\|
\ge\|\delta\|-|\alpha|\|\Delta F\|
\ge(1-|\alpha|L)\|\delta\|.
$$

若 $|\alpha|L<1$，$G(x)=G(y)$ 会强迫 $x=y$，故 injective。对 $u=G(x),v=G(y)$：

$$
\|G^{-1}(u)-G^{-1}(v)\|
\le\frac1{1-|\alpha|L}\|u-v\|.
$$

这是 inverse 在 $G$ 的像上的 Lipschitz bound。

### NN-RSL-C02

$$
\begin{aligned}
\|G(x)-G(y)\|^2
&=\|\delta\|^2+2\alpha\langle\delta,\Delta F\rangle+\alpha^2\|\Delta F\|^2\\
&\le(1+2\alpha\mu+\alpha^2L^2)\|\delta\|^2.
\end{aligned}
$$

要 contraction，需要 factor 小于 1：

$$
2\alpha\mu+\alpha^2L^2<0.
$$

当 $\mu<0,\alpha>0$ 时，

$$
0<\alpha<\frac{-2\mu}{L^2}.
$$

### NN-RSL-C03
递推两次可见 pattern：

$$
d_2\le q_1q_0d_0+q_1\xi_0+\xi_1.
$$

归纳得到

$$
d_N
\le\left(\prod_{j=0}^{N-1}q_j\right)d_0
+\sum_{k=0}^{N-1}
\left(\prod_{j=k+1}^{N-1}q_j\right)\xi_k.
$$

第 $k$ 步误差要经过所有 $j>k$ 的后续 map；越早发生，乘积尾通常越长。若后续是 contraction，早期误差也可能被更多衰减，所以“通常更大”仍取决于 $q_j$。

## D

### NN-RSL-D01

- $P$ orthogonal：$\|P\delta\|=\|\delta\|$，故 upper/lower 为 $1\pm|\alpha|L$；
- $P=0.5I$：upper 为 $0.5+|\alpha|L$，若 $0.5>|\alpha|L$，lower 为 $0.5-|\alpha|L$；
- rank-deficient $P$：一般 upper 为 $\|P\|+|\alpha|L$，但仅凭这些信息无正 lower bound；nullspace 方向可能丢失，除非 branch 对该方向有额外可证补偿。

### NN-RSL-D02
不能。诚实表述是：“在给定 1000 个样本和每样本 10 个随机方向、指定 dtype/mode 下，未观察到 gain 大于 1。”这是一项 empirical directional test。global contraction 需要对整个 domain 的 operator norm 上确界小于 1，可通过结构化 spectral certificate、覆盖误差界、interval/bound propagation 或可证明的一侧耗散条件支持。

### NN-RSL-D03

- absorption：$\alpha F$ 小于 residual stream 附近 half-ulp；
- cancellation：大而异号的 $x$ 与 branch 相加丢有效位；
- overflow/underflow：branch 内乘加或缩放越过 dtype range；
- reduction order：并行归约改变 branch/normalization rounding，形成 $\xi_\ell$。

诊断至少包括：记录 branch compute/accumulate/add dtype；比较 FP32 reference；扫 state-to-branch RMS 与 ulp ratio；检查 finite/nonzero fraction；改变 reduction topology；开启/关闭 fusion；做 deterministic replay 和 per-layer relative error。

## E

### NN-RSL-E01
若 $L_\ell\le C$：

$$
\alpha=N^{-1}
\Rightarrow
\sum\alpha L\le C
\Rightarrow
\operatorname{Lip}(G_{0:N})\le e^C.
$$

而

$$
\alpha=N^{-1/2}
\Rightarrow
\sum\alpha L\le C\sqrt N
\Rightarrow
\operatorname{Lip}(G_{0:N})\le e^{C\sqrt N}.
$$

若 increments 独立/不相关、零均值、每项 variance $\sigma^2$，则

$$
\operatorname{Var}\left(\sum\alpha F_\ell\right)
=N\alpha^2\sigma^2.
$$

$\alpha=1/N$ 给 $\sigma^2/N$，$\alpha=1/\sqrt N$ 给 $\sigma^2$。相关项非零时还必须加入 covariance sum。

### NN-RSL-E02

- adversarial robustness 还需分类 margin、威胁 norm/radius 与正确 label；
- generalization 还需数据分布、hypothesis/algorithm complexity 和 selection protocol；
- easy optimization 还需 parameter Jacobian/Hessian、conditioning、learning rate 与 trajectory。

input sensitivity upper bound 只控制一个函数属性，不包含这三个完整对象。

### NN-RSL-E03
在多个 depth/seed 上比较 $\alpha\in\{1,1/\sqrt N,1/N\}$ 与 learnable gate，记录：activation/branch RMS、gradient norm、parameter update-to-weight、JVP/VJP gain 与 singular estimates、ulp/absorption rate、training failure、time-to-loss、validation 和 wall time。

由于

$$
\nabla_\theta\mathcal L\propto\alpha,
$$

固定 optimizer learning rate 会改变 branch 的有效步长。应同时报告：

1. **natural protocol**：相同 optimizer/schedule；
2. **matched-update protocol**：调 learning rate 或 parameter group 使初始 update-to-weight 匹配；
3. 相同调参预算。

只有二者共同分析，才能区分 architecture scaling 与隐含 learning-rate scaling。
