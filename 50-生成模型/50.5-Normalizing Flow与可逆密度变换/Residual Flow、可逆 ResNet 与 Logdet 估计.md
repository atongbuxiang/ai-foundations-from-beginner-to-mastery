---
type: model
status: verified
area: [generative-models, normalizing-flows, invertible-networks]
node_id: GEN-37
prerequisites: ["[[光滑性、强凸性与条件数]]", "[[残差块 Jacobian 与梯度直通]]", "[[流映射、Liouville 公式与连续正规化流]]"]
related: ["[[Continuous Normalizing Flow、Liouville 与 FFJORD]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
sources: ["[[S-2019-Su-6482-可逆ResNet]]", "[[S-2019-Behrmann-iResNet]]", "[[S-2018-Su-6051-Lipschitz约束]]"]
exercises: ["[[习题 - Residual Flow、可逆 ResNet 与 Logdet 估计]]"]
solutions: ["[[解答 - Residual Flow、可逆 ResNet 与 Logdet 估计]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-residual-error-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Residual Flow、可逆 ResNet 与 Logdet 估计

> [!abstract] 一句话结论
> 对 residual map $F(x)=x+g(x)$，$\operatorname{Lip}(g)<1$ 是一个清楚、可组合的充分可逆条件：逆可由压缩迭代求出，logdet 可用 trace power series 表示。但实际 likelihood 同时承担 Lipschitz 证书松弛、有限逆迭代、级数截断和随机迹估计四类误差，不能把“数学双射”直接写成“数值精确”。

## 一、为什么 residual block 可能可逆

给定 $y=F(x)=x+g(x)$，求逆等价于找不动点

$$x=T_y(x)\triangleq y-g(x).$$

若 $g:\mathbb R^d\to\mathbb R^d$ 满足

$$\|g(x)-g(x')\|\le L\|x-x'\|,\qquad 0\le L<1,$$

则 $T_y$ 也是 Lipschitz 常数 $L$ 的压缩映射。Banach 不动点定理给出：每个 $y$ 有唯一 $x^*$，并且迭代

$$x_{k+1}=y-g(x_k)$$

从任意初值收敛到它。因此 $F$ 是一一且满到其像；在全空间适当条件下给出全局双射。

### 1.1 几何误差界

由压缩性，

$$\|x_{k+1}-x^*\|\le L\|x_k-x^*\|\le L^{k+1}\|x_0-x^*\|.$$

若不知道 $x^*$，可用后验 bound

$$
\|x_k-x^*\|\le \frac{L}{1-L}\|x_k-x_{k-1}\|.
$$

$L=0.5$ 时误差大约每步减半；$L=0.99$ 时虽仍有定理保证，却可能需要数百步。这说明“严格小于 1”与“工程上快速”不是同一个门槛。

## 二、一个标量手算

令 $g(x)=ax$，$|a|<1$。则 $F(x)=(1+a)x$，精确逆 $x^*=y/(1+a)$。从 $x_0=0$ 出发，

$$x_1=y,\quad x_2=y-ay,\quad x_3=y-ay+a^2y,$$

是几何级数的部分和，最终收敛到 $y/(1+a)$。若 $a=-0.99$，$F'(x)=0.01$，映射虽可逆却极度压缩，逆会放大误差 100 倍；round-trip 还需条件数账。

## 三、logdet 的 trace power series

若 $g$ 可微且 $\rho(J_g)<1$，矩阵对数级数收敛：

$$
\log(I+J_g)=\sum_{k=1}^{\infty}\frac{(-1)^{k+1}}{k}J_g^k.
$$

取 trace，并用 $\log\det A=\operatorname{tr}\log A$（在所选实数分支和正 determinant 条件下），得到

$$
\boxed{\log\det(I+J_g)
=\sum_{k=1}^{\infty}\frac{(-1)^{k+1}}{k}\operatorname{tr}(J_g^k).}
$$

不能只因 $I+J_g$ 可逆就使用这一级数；级数需要谱半径小于 1。$\|J_g\|_2\le L<1$ 是更强但易用的充分条件。

## 四、Hutchinson 怎样避免显式 Jacobian

对满足 $\mathbb E[vv^\top]=I$ 的随机向量（如 Rademacher 或标准 Gaussian），

$$\mathbb E_v[v^\top A v]=\operatorname{tr}(A).$$

因此

$$\operatorname{tr}(J_g^k)\approx
\frac1M\sum_{m=1}^M(v^{(m)})^\top J_g^k v^{(m)}.$$

$J_g^k v$ 可通过连续 $k$ 次 JVP/VJP 型运算得到，无需构造 $d\times d$ Jacobian。条件在固定状态与固定 $A$ 时，probe estimator 对 trace 无偏；有限 $M$ 有方差。

## 五、四种误差必须分账

| 层次 | 误差 | 典型诊断 |
|---|---|---|
| 可逆证书 | 实际 Lipschitz 上界估计松或被违反 | spectral estimate、随机方向 Jacobian norm |
| inverse | fixed-point 只迭代 $K_{inv}$ 步 | residual $\|F(x_K)-y\|$、后验误差界 |
| series | 截到 $K_{tr}$ 项 | 随 $K_{tr}$ 的稳定曲线、几何 remainder bound |
| trace | 只用 $M$ 个 probes | 多 seed 方差、confidence interval |

固定阶截断通常有 bias；Hutchinson 对每一项的 trace 可无偏但有 variance。若使用随机截断/Russian roulette，可在附加可积条件下构造无偏 series estimator，却可能增加 variance 和尾部计算。不能笼统说“logdet estimator 无偏”。

## 六、如何约束 $\operatorname{Lip}(g)$

对层复合，可用各线性层 operator norm 与激活 Lipschitz 常数的乘积作上界。谱归一化常用 power iteration 估计最大奇异值，再缩放权重。但：

- 一两步 power iteration 是估计，不是精确 certificate；
- product bound 可能远大于真实 network Lipschitz；
- convolution operator norm 不能总由 kernel reshaping 的 matrix norm 精确代表；
- $L$ 留得越小，逆更快但 residual branch 表达幅度受限。

## 七、AI 计算合同

训练/评价至少报告：$L$ target、谱估计迭代数、inverse tolerance 与最大步数、series truncation/随机截断、probe distribution/数量、forward/inverse residual、logdet variance、wall time。`exact bijection` 与 `approximate likelihood evaluation` 应分别标注。

## 八、科学空间研读框

[[S-2019-Su-6482-可逆ResNet]]把 $I+g$、不动点逆与 trace series 串成直观主线；[[S-2019-Behrmann-iResNet]]承担正式方法和原始实验；[[S-2018-Su-6051-Lipschitz约束]]补充网络 Lipschitz 约束视角。本节额外把四种误差拆开，避免“可逆”吞掉数值近似。

## 九、图：证书、逆与 likelihood 不是一张通行证

先看图回答：哪一条链证明唯一 inverse，哪两条近似链只控制计算误差而不改变数学定义？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-residual-error-ledger-v1.svg|900]]

> [!figure] 图 50.5-05　Residual flow 的可逆性证书、逆迭代与 logdet 估计误差账
> 左侧是 $L<1$ 的定理链，中间是 fixed-point residual，右侧分开 series truncation 与 Hutchinson probes。来源：据压缩映射定理与 i-ResNet 机制独立绘制。

**怎样读图**：绿色链只说明唯一解与几何收敛；琥珀色框提醒有限 $K$、有限 probes 产生近似。先验证证书，再报告 inverse，再报告 likelihood estimator。

**图没有证明什么**：图不证明训练得到的网络实际满足全局 Lipschitz 上界，不证明低方差，也不证明残差架构在同预算下优于 coupling。

## 十、本节回顾与训练

- $\operatorname{Lip}(g)<1$ 是充分条件，不是所有可逆 residual map 的必要条件；
- fixed-point inverse 的速率由 $L$ 控制；
- trace series 的收敛条件不能省；
- truncation bias 与 probe variance 是不同误差；
- 数学可逆、有限步 inverse、近似 logdet 和浮点稳定必须分别验收。

- [[习题 - Residual Flow、可逆 ResNet 与 Logdet 估计]]
- [[解答 - Residual Flow、可逆 ResNet 与 Logdet 估计]]
