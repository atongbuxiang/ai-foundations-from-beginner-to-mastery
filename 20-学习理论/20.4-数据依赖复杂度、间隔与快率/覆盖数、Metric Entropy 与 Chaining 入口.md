---
type: theorem
status: draft
area: [learning-theory/metric-entropy, empirical-process/chaining]
aliases: [Covering Number, Metric Entropy, Dudley Entropy Integral, 链式法入口]
node_id: LT-30
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]", "[[度量空间、拓扑与连续映射]]", "[[有限假设类、Union Bound 与一致收敛]]"]
related: ["[[局部 Rademacher 复杂度与快收敛率]]", "[[Fat-Shattering、回归与 Lipschitz 风险]]", "[[核岭回归与 Gaussian Process 接口]]", "[[神经网络容量与 Norm-Based Bound]]"]
sources: ["[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]", "[[S-1996-Bartlett-Long-Williamson-Fat-Shattering]]"]
exercises: ["[[习题 - 覆盖数、Metric Entropy 与 Chaining 入口]]"]
solutions: ["[[解答 - 覆盖数、Metric Entropy 与 Chaining 入口]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-covering-entropy-chaining-v2.svg]]"
created: 2026-08-23
updated: 2026-08-28
---

# 覆盖数、Metric Entropy 与 Chaining 入口

> [!abstract] 本章主问题
> 无限函数类不能直接用 $\log|\mathcal F|$ 计数，但在给定 metric 和 resolution $\varepsilon$ 下，可能只需有限个代表。最小代表数是 covering number
> $$
> N(\varepsilon,\mathcal F,d),
> $$
> 其对数 $\log N$ 是 metric entropy。单尺度网格只把函数近似一次；chaining 在 $\varepsilon_0>\varepsilon_1>\cdots$ 的嵌套网格间写 telescoping increments，并把每层有限 maximum 的代价相加。对经验 $L_2$ pseudometric，一条常用安全版本是
> $$
> \widehat{\mathfrak R}_S(\mathcal F)
> \le
> \inf_{\alpha>0}
> \left[
> 4\alpha+
> \frac{12}{\sqrt m}
> \int_\alpha^{D/2}
> \sqrt{\log N(\varepsilon,\mathcal A,d_S)}\,d\varepsilon
> \right],
> $$
> 其中 $\mathcal A=\mathcal F\cup(-\mathcal F)\cup\{0\}$，$D=\operatorname{diam}(\mathcal A,d_S)$。常数依 convention；核心是“每个尺度的几何”而非单一参数个数。

> [!question] 初学者读完必须能回答
> 1. cover、packing 与 net 的中心是否必须属于原集合？
> 2. 为什么不声明 metric 就不能谈 covering number？
> 3. empirical $d_S$ 为什么只是 pseudometric？
> 4. 单尺度近似损失在哪里，chaining 怎样把它分散到多尺度？
> 5. entropy integral 发散时，cutoff $\alpha$ 为什么不能直接取 0？

## 一、学习目标

1. 定义 cover、covering number、packing number 与 metric entropy；
2. 证明基本单调性、缩放性与 packing–covering 关系；
3. 在样本 restriction 上定义经验 $L_2$ pseudometric；
4. 从有限类 Massart lemma 推出单尺度 entropy bound；
5. 用 telescoping nets 解释 chaining 的每一层；
6. 陈述并读取 truncated Dudley entropy integral；
7. 由 entropy growth 计算典型 $m$-rate；
8. 把 parameter-space cover 合法传到 function-space cover；
9. 识别 metric mismatch、data-dependent net 与 vector/output geometry 的边界。

## 二、Covering Number：用有限代表逼近无限集合

设 $(T,d)$ 是 metric 或 pseudometric space。半径 $\varepsilon>0$ 的闭球为

$$
B_d(t,\varepsilon)
=\{u\in T:d(u,t)\le\varepsilon\}.
$$

集合 $C\subseteq T$ 称为 $T$ 的一个 $\varepsilon$-cover，若

$$
T\subseteq\bigcup_{c\in C}B_d(c,\varepsilon).
$$

covering number 定义为最小中心数：

$$
N(\varepsilon,T,d)
=\min\{|C|:C\text{ 是 }T\text{ 的 }\varepsilon\text{-cover}\}.
$$

若不存在有限 cover，则取 $N=\infty$。

### 2.1 Internal 与 external cover

- internal cover 要求 centers $C\subseteq T$；
- external cover 允许 centers 位于 ambient space。

两者常只差常数尺度，但定理必须说明采用哪一种。本节默认 internal cover，方便把每个中心仍看作一个函数。

### 2.2 Metric entropy

定义

$$
H(\varepsilon,T,d)=\log N(\varepsilon,T,d).
$$

它不是 Shannon entropy：

- 没有 probability mass；
- 依赖 metric；
- 依赖 resolution；
- 描述几何逼近所需的 log-cardinality。

## 三、Packing Number 与 Cover 的关系

$A\subseteq T$ 称为 $\varepsilon$-packing，若任意不同 $a,a'\in A$ 满足

$$
d(a,a')>\varepsilon.
$$

最大 packing cardinality 记作 $M(\varepsilon,T,d)$。

在常见 convention 下：

$$
\boxed{
M(2\varepsilon,T,d)
\le N(\varepsilon,T,d)
\le M(\varepsilon,T,d).}
$$

### 3.1 左不等式

一个半径 $\varepsilon$ 的球不可能同时覆盖两个距离 $>2\varepsilon$ 的 packing points，否则 triangle inequality 给出它们距离至多 $2\varepsilon$。所以每个 cover ball 最多负责一个 $2\varepsilon$-packing point。

### 3.2 右不等式

取 maximal $\varepsilon$-packing。若存在 $t\in T$ 离所有 packing point 都 $>\varepsilon$，就可以把 $t$ 加进去，与 maximality 矛盾。因此 maximal packing 同时是一个 $\varepsilon$-cover。

> [!warning] $>$ 与 $\ge$ 的 convention
> packing 定义用 strict 还是 non-strict 会影响端点而非主要 rate。做有限例题时必须对齐。

## 四、函数类在样本上的经验 Pseudometric

固定样本 $S_X=(X_1,\ldots,X_m)$，定义

$$
d_S(f,g)
=\left(
\frac1m\sum_{i=1}^m(f(X_i)-g(X_i))^2
\right)^{1/2}.
$$

它等价于 restriction vectors

$$
v_f=(f(X_1),\ldots,f(X_m))\in\mathbb R^m
$$

之间的 normalized Euclidean distance。

称为 pseudometric，是因为不同函数可能在所有 $X_i$ 上相同：

$$
f\ne g,
\qquad
f(X_i)=g(X_i) \forall i,
\qquad
d_S(f,g)=0.
$$

Rademacher complexity 也只读取 restriction vectors，所以 quotient 掉这种差异恰好合适。

### 4.1 为什么 metric 选择决定结论

同一函数类可用：

- empirical $L_2$：$d_S$；
- empirical $L_\infty$：$\max_i|f(X_i)-g(X_i)|$；
- population $L_2(P)$；
- parameter norm $\|\theta-\theta'\|$；
- operator/spectral norm for matrix-valued maps。

covering number 没有脱离 metric 的绝对值。一个 class 在 parameter norm 下很大，却可能在当前 sample restriction 上高度重合。

## 五、基本性质

### 5.1 分辨率单调性

若 $0<\varepsilon_1\le\varepsilon_2$，则

$$
N(\varepsilon_2,T,d)
\le N(\varepsilon_1,T,d).
$$

球越大，所需中心不会更多。

### 5.2 集合单调性

若 $T_1\subseteq T_2$，则对 internal cover 需略注意 centers；允许 ambient centers 时直接有

$$
N(\varepsilon,T_1,d)
\le N(\varepsilon,T_2,d).
$$

对 internal cover 可在常数放大的尺度下得到同类关系。

### 5.3 缩放

对 norm metric 与 $a>0$，

$$
N(\varepsilon,aT,\|\cdot\|)
=N(\varepsilon/a,T,\|\cdot\|).
$$

这说明 function amplitude 与 resolution 必须成对报告。

## 六、图解：从一张网到一串网

先回答：**为什么最细网格的总中心数不应该在每个尺度重复支付？**

![[00-知识库管理/_assets/figures/learning-theory/fig-covering-entropy-chaining-v2.svg|900]]

> [!figure] 图 20.4.6｜Cover、逐尺度增量与 entropy integral
> 左栏显示固定 metric/resolution 的 cover；中栏把函数写成 coarse representative 加逐层 increments；右栏将离散层级和组织成 truncated entropy integral。来源：依据 empirical-process chaining 主线独立绘制；确定性 SVG，由 [[plot_rademacher_advanced_v2.py]] 生成。

**怎样读图。** 细网的每个点不从原点重新计费，只支付它相对上一层代表的短增量。coarse level 点少但步长大；fine level 点多但步长小。

**适用边界（图没有证明什么）。** 图没有给出最佳常数、generic chaining 的 $\gamma_2$ 等价、无界过程的 tail theorem 或任意 metric 下的 sub-Gaussian increments；这些需要更完整 empirical-process 条件。

## 七、单尺度 Cover Bound

固定一个 internal $\varepsilon$-net $C_\varepsilon\subseteq\mathcal F$。对每个 $f$，选最近代表 $\pi(f)\in C_\varepsilon$，使

$$
d_S(f,\pi(f))\le\varepsilon.
$$

Rademacher score 分解：

$$
\frac1m\sum_i\sigma_if(X_i)
=
\frac1m\sum_i\sigma_i\pi(f)(X_i)
+
\frac1m\sum_i\sigma_i(f-\pi(f))(X_i).
$$

对 residual，由 Cauchy–Schwarz：

$$
\begin{aligned}
\left|
\frac1m\sum_i\sigma_i(f-\pi(f))(X_i)
\right|
&\le
\sqrt{\frac1m\sum_i\sigma_i^2}
\sqrt{\frac1m\sum_i(f-\pi(f))^2(X_i)}\\
&\le\varepsilon.
\end{aligned}
$$

因此

$$
\widehat{\mathfrak R}_S(\mathcal F)
\le
\widehat{\mathfrak R}_S(C_\varepsilon)+\varepsilon.
$$

若所有 net restriction vectors 的 normalized $L_2$ norm 至多 $A$，Massart finite-class lemma 给出

$$
\widehat{\mathfrak R}_S(C_\varepsilon)
\le
A\sqrt{\frac{2\log N(\varepsilon,\mathcal F,d_S)}m}.
$$

故

$$
\boxed{
\widehat{\mathfrak R}_S(\mathcal F)
\le
\varepsilon
+A\sqrt{\frac{2\log N(\varepsilon,\mathcal F,d_S)}m}.}
$$

### 7.1 单尺度的 trade-off

- 大 $\varepsilon$：net 小，entropy 项小，但 approximation residual 大；
- 小 $\varepsilon$：residual 小，但 net 可能巨大。

优化 $\varepsilon$ 已比直接计数无限类更好，但所有细节仍被迫用同一个 resolution 描述。

## 八、Chaining 的 Telescoping 分解

取尺度

$$
\varepsilon_k=2^{-k}D,
\qquad k=0,1,\ldots,K,
$$

并在每层取 net $C_k$。令 $\pi_k(f)$ 是 $f$ 的最近 net point。则

$$
f
=\pi_0(f)
+\sum_{k=1}^K[\pi_k(f)-\pi_{k-1}(f)]
+[f-\pi_K(f)].
$$

这是纯代数 telescoping identity。

### 8.1 每层 increment 有多长

triangle inequality 给出

$$
d_S(\pi_k(f),\pi_{k-1}(f))
\le
d_S(\pi_k(f),f)+d_S(f,\pi_{k-1}(f))
\le\varepsilon_k+\varepsilon_{k-1}
\le3\varepsilon_k.
$$

### 8.2 每层有多少可能 increment

粗上界为

$$
|C_k|\,|C_{k-1}|,
$$

所以 log-cardinality 至多

$$
\log N(\varepsilon_k)+\log N(\varepsilon_{k-1}).
$$

对每层用 finite-class maximum bound，得到形如

$$
\frac1{\sqrt m}
\sum_{k=1}^K
\varepsilon_{k-1}
\sqrt{\log N(\varepsilon_k)}
$$

的离散和，再加 fine residual $O(\varepsilon_K)$。

这就是 chaining：**复杂的细网只乘很短的 increment；很长的 coarse increment 只乘很小的 entropy。**

## 九、Dudley Entropy Integral

令

$$
\mathcal A=\mathcal F\cup(-\mathcal F)\cup\{0\},
$$

并定义经验直径

$$
D=\operatorname{diam}(\mathcal A,d_S).
$$

在本节 signed $1/m$ convention 与 normalized empirical $L_2$ metric 下，一条常用版本为

$$
\boxed{
\widehat{\mathfrak R}_S(\mathcal F)
\le
\inf_{\alpha>0}
\left[
4\alpha
+\frac{12}{\sqrt m}
\int_\alpha^{D/2}
\sqrt{\log N(\varepsilon,\mathcal A,d_S)}\,d\varepsilon
\right].}
$$

若 $\alpha>D/2$，积分按 0 处理。

### 9.1 为什么要对称化集合 $\mathcal A$

加入 $-\mathcal F$ 与 0 使 process increments/diameter 的表示更统一，并对齐 absolute/signed comparisons。不同教材可能直接对 centered class 写定理；集合与常数必须一起引用。

### 9.2 为什么下限是 $\alpha>0$

极细尺度的 entropy 可能增长过快，使

$$
\int_0^{D/2}\sqrt{\log N(\varepsilon)}\,d\varepsilon
$$

发散。但有限样本上的 Rademacher complexity 仍可能有限。停止 chaining 于 $\alpha$，用 $4\alpha$ 粗控最后 residual，再优化 cutoff。

## 十、从 Entropy Growth 读取 Rate

### 10.1 有限维/参数型 entropy

若

$$
\log N(\varepsilon)
\lesssim d\log(A/\varepsilon),
$$

则 entropy integral 通常给出

$$
\widehat{\mathfrak R}_S(\mathcal F)
\lesssim
A\sqrt{\frac d m}
$$

（忽略常数与轻微 log 因子，具体取决于直径和 metric transfer）。

### 10.2 Polynomial entropy

若在小尺度

$$
\log N(\varepsilon)
\lesssim C\varepsilon^{-p},
$$

则 integrand 约为 $\sqrt C\varepsilon^{-p/2}$：

- $p<2$：积分在 0 附近有限，常保留 $m^{-1/2}$ 型；
- $p=2$：出现 $\log(1/\alpha)$ 临界因子；
- $p>2$：小尺度主导，优化 $\alpha$ 给出约 $m^{-1/p}$。

这只是上界 rate calculus；minimax optimality 还需要 matching lower bound。

## 十一、Parameter Cover 怎样传给 Function Cover

设 $f_\theta$ 由参数 $\theta\in\Theta$ 决定。若对当前样本能证明

$$
d_S(f_\theta,f_{\theta'})
\le L_S\|\theta-\theta'\|,
$$

则 parameter-space 的 $\varepsilon/L_S$ cover 映射成 function-space 的 $\varepsilon$ cover：

$$
\boxed{
N(\varepsilon,\mathcal F,d_S)
\le
N(\varepsilon/L_S,\Theta,\|\cdot\|).}
$$

### 11.1 这一步最容易被滥用

- neural network parameterization 有 permutations/rescalings，同一函数对应许多参数；parameter cover 可极松；
- $L_S$ 可能是 layer norms 的巨大乘积；
- local Lipschitz 不等于全参数域 uniform Lipschitz；
- learned representation 使 metric 也与训练过程耦合。

因此 parameter counting 是一种可用上界，不一定是 function geometry 的忠实描述。

## 十二、Data-Dependent Cover 是否“偷看数据”

经验 $d_S$ 和 net 都可依赖 $S$，因为 empirical Rademacher analysis 先条件于固定样本，再对 synthetic signs 取期望。合法性来自整个 high-probability theorem 已处理 sample randomness。

但不能无条件做以下替换：

1. 用 labels/validation performance 选择一个小子类；
2. 把它当作预先固定 class；
3. 忽略选择过程的 complexity。

metric 依赖 input sample 与 class restriction，和 data-adaptive hypothesis selection 是不同层次。

## 十三、AI 接口

### 13.1 神经网络 Norm-Based Cover

常见证明路线：

$$
\text{layer norm constraints}
\Rightarrow
\text{output perturbation bound}
\Rightarrow
\text{parameter/layer covers}
\Rightarrow
\text{network cover}
\Rightarrow
\text{entropy integral}.
$$

每个箭头都可能损失：depth product、width log、activation Lipschitz、input radius 或 output dimension。

### 13.2 Kernel 与 Random Features

RKHS ball 的 empirical geometry 由 Gram matrix eigenvalues 决定。比只用 $\operatorname{tr}K$ 更细的 spectral entropy 可读取 effective dimension；但 kernel/hyperparameter 若用同一数据自适应选择，需要额外 model-selection budget。

### 13.3 Generative Models 与 Vector Outputs

对 vector field、diffusion score 或 logits，需先选 output norm，再定义

$$
d_S(f,g)^2
=\frac1m\sum_i\|f(X_i)-g(X_i)\|_{\rm out}^2.
$$

不同 output norm 会改变 dual process、cover 与 contraction，不能把 scalar Dudley formula无修改搬过去。

## 十四、常见误区

> [!danger] 误区 1：covering number 是集合的固有大小
> 它还依赖 metric 与 $\varepsilon$；不写二者，数字没有意义。

> [!danger] 误区 2：net 越细越好
> 更细降低 approximation error，却提高 entropy；Dudley bound 还可能在 0 发散。

> [!danger] 误区 3：chaining 就是多取几张网
> 核心是 telescoping increments 和每层不同的长度–cardinality 配对。

> [!danger] 误区 4：参数个数就是 metric entropy
> 需要 parameter-to-function Lipschitz transfer；symmetry、flat directions 与 data geometry 都可能使粗计数失真。

> [!danger] 误区 5：经验 cover 小，所以分布外也小
> $d_S$ 只读当前样本 restrictions；distribution shift 需要新 metric/law 与覆盖证明。

## 十五、本节最小闭环

面对一个 function class，应能：

1. 声明 $T,d,\varepsilon$；
2. 构造或上界一个 cover；
3. 区分 internal/external 与 cover/packing；
4. 写单尺度 approximation + finite maximum bound；
5. 写 nets 的 telescoping decomposition；
6. 判断 entropy integral 是否在 0 收敛；
7. 若不收敛，选择并优化 cutoff $\alpha$；
8. 审计 parameter-to-function transfer 与 sample dependence；
9. 只在 theorem 条件完整时把 entropy 变成风险界。

## 十六、连接

- 前置：[[Rademacher 复杂度与经验复杂度]]、[[有限假设类、Union Bound 与一致收敛]]；
- 下一节：[[局部 Rademacher 复杂度与快收敛率]]；
- 尺度维：[[Fat-Shattering、回归与 Lipschitz 风险]]；
- 深网：[[神经网络容量与 Norm-Based Bound]]；
- 训练：[[习题 - 覆盖数、Metric Entropy 与 Chaining 入口]]；
- 解答：[[解答 - 覆盖数、Metric Entropy 与 Chaining 入口]]。
