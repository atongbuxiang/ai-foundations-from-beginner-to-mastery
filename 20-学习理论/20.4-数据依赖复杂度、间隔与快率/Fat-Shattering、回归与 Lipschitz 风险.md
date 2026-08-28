---
type: concept
status: draft
area: [learning-theory/scale-sensitive-dimension, regression/generalization]
aliases: [Fat-Shattering Dimension, Scale-Sensitive Dimension, 实值函数尺度容量]
node_id: LT-32
prerequisites: ["[[实值函数类、伪维与阈值化]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]", "[[收缩引理与 Lipschitz 损失复合]]"]
related: ["[[分类间隔、Margin Bound 与 SVM 接口]]", "[[核岭回归与 Gaussian Process 接口]]", "[[随机变量、分布与分位数]]", "[[神经网络容量与 Norm-Based Bound]]"]
sources: ["[[S-1996-Bartlett-Long-Williamson-Fat-Shattering]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]", "[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]"]
exercises: ["[[习题 - Fat-Shattering、回归与 Lipschitz 风险]]"]
solutions: ["[[解答 - Fat-Shattering、回归与 Lipschitz 风险]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-fat-shattering-regression-bridge-v2.svg]]"
created: 2026-08-23
updated: 2026-08-28
---

# Fat-Shattering、回归与 Lipschitz 风险

> [!abstract] 本章主问题
> VC dimension 只问 binary patterns 能否实现；pseudo-dimension 允许逐点 thresholds，却没有记录实现模式时离阈值多远。对实值类 $\mathcal F$ 与尺度 $\gamma>0$，若存在 $x_1,\ldots,x_d$ 和 thresholds $r_1,\ldots,r_d$，使每个 sign pattern $s\in\{-1,+1\}^d$ 都有 $f_s\in\mathcal F$ 满足
> $$
> s_i(f_s(x_i)-r_i)\ge\gamma,
> \quad i=1,\ldots,d,
> $$
> 就称这些点被 $\gamma$-fat-shattered。本课程采用“每侧 margin 为 $\gamma$”的 convention；有些文献把总 gap $\gamma$ 分成两侧 $\gamma/2$。fat-shattering function $\operatorname{fat}_\gamma(\mathcal F)$ 是实值类在分辨率 $\gamma$ 下的容量。它经 packing/covering 与 entropy integral 控制 Rademacher complexity，再经 Lipschitz loss contraction 进入回归风险。

> [!question] 初学者读完必须能回答
> 1. thresholds $r_i$ 何时选，为什么不能随 sign pattern 改变？
> 2. fat-shattering 与 pseudo-dimension 的共同点和尺度差异是什么？
> 3. 为什么 $\operatorname{fat}_\gamma$ 随 $\gamma$ 增大而不增？
> 4. 线性 $\ell_2$ 球为什么出现 $(BR/\gamma)^2$？
> 5. 从 fat dimension 到 regression risk 中间还缺哪三座桥？

## 一、学习目标

1. 严格陈述 $\gamma$-fat-shattering definition 与量词顺序；
2. 构造一维、有限函数类与 binary class 例子；
3. 证明尺度单调性、class 单调性与 amplitude scaling；
4. 比较 VC、pseudo-dimension 与 fat profile；
5. 由 fat-shattering 推出 Rademacher lower bound；
6. 合成线性球 complexity upper bound 得到 $(BR/\gamma)^2$ 维数界；
7. 说明 fat → packing/covering → Rademacher → Lipschitz risk 的链；
8. 审计 absolute、quantile、squared、multiclass 与 neural regression 的不同合同。

## 二、正式定义与量词顺序

给定实值函数类

$$
\mathcal F\subseteq\mathbb R^{\mathcal X}.
$$

点集 $\{x_1,\ldots,x_d\}$ 被 $\gamma$-fat-shattered，如果存在一组固定 thresholds

$$
r_1,\ldots,r_d\in\mathbb R
$$

使得：对每个 sign vector

$$
s=(s_1,\ldots,s_d)\in\{-1,+1\}^d,
$$

都存在一个函数 $f_s\in\mathcal F$，满足所有坐标

$$
\boxed{
s_i(f_s(x_i)-r_i)\ge\gamma.}
$$

量词结构是

$$
\exists x_{1:d},\exists r_{1:d},
\forall s\in\{-1,+1\}^d,
\exists f_s\in\mathcal F,
\forall i.
$$

### 2.1 正负 sign 的含义

- 若 $s_i=+1$，则 $f_s(x_i)\ge r_i+\gamma$；
- 若 $s_i=-1$，则 $f_s(x_i)\le r_i-\gamma$。

同一点的高、低两种要求之间至少相隔 $2\gamma$。

> [!warning] Convention 差异
> 有些书定义高侧 $r_i+\gamma/2$、低侧 $r_i-\gamma/2$，把总 separation 记为 $\gamma$。两种定义只差尺度 2，但所有 bound 的下标必须同步替换。

## 三、Fat-Shattering Dimension

定义

$$
\operatorname{fat}_\gamma(\mathcal F)
=\sup\{d:\exists d\text{ 个点被 }\gamma\text{-fat-shattered}\}.
$$

若任意 $d$ 都可实现，取 $\infty$。

它不是一个单独整数，而是一条 scale profile：

$$
\gamma\mapsto\operatorname{fat}_\gamma(\mathcal F).
$$

粗 resolution 下容量可能很小；精细 resolution 下容量可能很大甚至无限。

## 四、最小例子

### 4.1 常数函数区间

令

$$
\mathcal F=\{f_c(x)\equiv c:c\in[-B,B]\}.
$$

单点 $x_1$ 可在 $\gamma\le B$ 时被 fat-shatter：取 $r_1=0$，正 pattern 用 $c=B$，负 pattern 用 $c=-B$。

但两个点不能被 fat-shatter，因为同一个 constant $c$ 无法同时实现 $(+,-)$ pattern 的一高一低要求。因此

$$
\operatorname{fat}_\gamma(\mathcal F)=1
$$

在可行尺度内，而非由连续参数个数“无限”。

### 4.2 单点上的有限值集合

若在某点 $x$，所有函数值都落在 interval $[a,b]$，要实现正负两侧，必须有

$$
b-a\ge2\gamma.
$$

这给出最直接的 range-resolution 必要条件。

### 4.3 Binary Class

若 $\mathcal F\subseteq\{0,1\}^{\mathcal X}$，对 $0<\gamma\le1/2$，取 threshold $r_i=1/2$，VC-shattering 就给出 fat-shattering。反过来，能 fat-shatter 必须在每点实现 0 和 1 两种值，因此在这个 convention 下

$$
\operatorname{fat}_\gamma(\mathcal F)
=\operatorname{VCdim}(\mathcal F),
\qquad0<\gamma\le1/2.
$$

所以 fat dimension 真正推广了 binary VC，并在实值情形保留分辨率。

## 五、图解：从阈值模式到风险

先回答：**如果把所有函数值与 thresholds 同时乘以 $c>0$，横轴 $\gamma$ 应怎样变化才比较同一几何？**

![[00-知识库管理/_assets/figures/learning-theory/fig-fat-shattering-regression-bridge-v2.svg|900]]

> [!figure] 图 20.4.8｜逐点 thresholds、fat profile 与 regression risk bridge
> 左栏展示固定 thresholds 上下的 $\gamma$ margin；中栏显示 $\operatorname{fat}_\gamma$ 随 resolution 变粗而下降；右栏强调 fat dimension 必须经 entropy、Rademacher 与 loss contract 才成为风险结论。来源：依据 scale-sensitive learnability 主线独立绘制；确定性 SVG，由 [[plot_rademacher_advanced_v2.py]] 生成。

**怎样读图。** fat-shattering 允许为每个 sign pattern 选择不同函数，但 thresholds 必须在看到 pattern 前固定。$\gamma$ 越大，实现所有模式越难。

**适用边界（图没有证明什么）。** 图没有给出最优 covering constants、所有实值类的完整 learnability 等价细节、unbounded/heavy-tailed regression 或 vector output 的专门 dimension。

## 六、基本性质

### 6.1 尺度单调性

若 $0<\gamma_1\le\gamma_2$，则

$$
\boxed{
\operatorname{fat}_{\gamma_2}(\mathcal F)
\le
\operatorname{fat}_{\gamma_1}(\mathcal F).}
$$

因为能以更大 margin $\gamma_2$ 实现的同一 witnesses，也能以较小 margin $\gamma_1$ 实现。

### 6.2 Class 单调性

若 $\mathcal F\subseteq\mathcal G$，则

$$
\operatorname{fat}_\gamma(\mathcal F)
\le
\operatorname{fat}_\gamma(\mathcal G).
$$

更大的 class 至少保留原来的 witnesses。

### 6.3 Amplitude Scaling

对 $a>0$，令

$$
a\mathcal F=\{af:f\in\mathcal F\}.
$$

thresholds 同时乘 $a$，得到

$$
\boxed{
\operatorname{fat}_\gamma(a\mathcal F)
=\operatorname{fat}_{\gamma/a}(\mathcal F).}
$$

所以只报 fat dimension 而不报 output scale 仍会误导。

### 6.4 Translation

对固定函数 $g$，类

$$
\mathcal F+g=\{f+g:f\in\mathcal F\}
$$

有相同 fat profile，因为 thresholds 可改为 $r_i+g(x_i)$。

## 七、与 Pseudo-Dimension 的关系

pseudo-dimension 要求存在 thresholds $r_i$，对每个 binary pattern 实现

$$
f_s(x_i)>r_i
\quad\text{或}\quad
f_s(x_i)<r_i,
$$

但没有统一 positive margin。因此：

$$
\operatorname{fat}_\gamma(\mathcal F)
\le\operatorname{Pdim}(\mathcal F),
\qquad\forall\gamma>0.
$$

有限 pseudo-dimension 给出所有尺度的统一 ceiling；但它可能看不见 coarse scale 上 class 实际简单得多。

> [!important] 不把 $\gamma\downarrow0$ 写成无条件数值等式
> pseudo-dimension 是 strict-threshold、scale-free combinatorial notion。对具体 finite witness，strict inequalities 常能产生某个 positive minimum margin；但无限类、supremum、端点 convention 下仍应通过正式 theorem说明 limit/等价，而非把“$\gamma=0$”直接代入 fat definition。

## 八、Fat-Shattering 蕴含 Rademacher Lower Bound

假设 $x_1,\ldots,x_d$ 被 $\gamma$-fat-shattered，witness thresholds 为 $r_i$。对每组 signs $\sigma\in\{-1,+1\}^d$，选 $f_\sigma$ 使

$$
\sigma_i(f_\sigma(x_i)-r_i)\ge\gamma.
$$

求和：

$$
\sum_i\sigma_if_\sigma(x_i)
\ge
\gamma d+\sum_i\sigma_i r_i.
$$

因此

$$
\sup_{f\in\mathcal F}
\frac1d\sum_i\sigma_if(x_i)
\ge
\gamma+\frac1d\sum_i\sigma_i r_i.
$$

对 $\sigma$ 取期望，threshold 项消失：

$$
\boxed{
\widehat{\mathfrak R}_{x_{1:d}}(\mathcal F)
\ge\gamma.}
$$

这是一座极重要的桥：**若 class 能在 $d$ 点上以 margin $\gamma$ 实现所有符号，它至少能以强度 $\gamma$ 拟合随机 signs。**

## 九、线性球的 $(BR/\gamma)^2$ Bound

考虑 Hilbert/$\ell_2$ 线性类

$$
\mathcal F_B
=\{x\mapsto\langle w,x\rangle:\|w\|_2\le B\},
$$

输入满足 $\|x\|_2\le R$。

若 $d$ 个点被 $\gamma$-fat-shattered，则上一节给出

$$
\gamma
\le\widehat{\mathfrak R}_{x_{1:d}}(\mathcal F_B).
$$

线性复杂度上界给出

$$
\widehat{\mathfrak R}_{x_{1:d}}(\mathcal F_B)
\le\frac{BR}{\sqrt d}.
$$

合并：

$$
\gamma\le\frac{BR}{\sqrt d}
\quad\Longrightarrow\quad
d\le\left(\frac{BR}{\gamma}\right)^2.
$$

因此

$$
\boxed{
\operatorname{fat}_\gamma(\mathcal F_B)
\le
\left(\frac{BR}{\gamma}\right)^2.}
$$

若 ambient dimension 为有限 $p$，还可结合 pseudo-dimension ceiling，写成常数量级

$$
\operatorname{fat}_\gamma(\mathcal F_B)
\lesssim
\min\left\{p,\left(\frac{BR}{\gamma}\right)^2\right\}.
$$

这说明小 scale 下 dimension ceiling 主导，大 scale 下 norm/radius 主导。

## 十、Fat → Packing/Covering → Rademacher

对 bounded real-valued class，scale-sensitive combinatorics 可控制 empirical packing/covering numbers。典型形式是

$$
\log N(\varepsilon,\mathcal F,d_S)
\lesssim
\operatorname{fat}_{c\varepsilon}(\mathcal F)
\cdot
\operatorname{polylog}\left(\frac B\varepsilon,m\right),
$$

其中 $c$、log 次数、metric 与 range 假设依具体 theorem。

再代入 Dudley integral：

$$
\widehat{\mathfrak R}_S(\mathcal F)
\lesssim
\inf_{\alpha>0}
\left[
\alpha+\frac1{\sqrt m}
\int_\alpha^B
\sqrt{\operatorname{fat}_{c\varepsilon}(\mathcal F)\cdot\operatorname{polylog}(B/\varepsilon,m)}
\,d\varepsilon
\right].
$$

> [!warning] 为什么这里只写结构式
> fat-to-cover 定理在 $L_2(P_m)$、$L_\infty$、bounded range、sample size 与 scale convention 上有多种版本。把某篇论文的 log power 与另一篇的 metric 拼接，容易得到假公式。应用时应引用完整 theorem。

## 十一、从 Function Complexity 到 Regression Risk

设 loss 对 prediction 是 $L$-Lipschitz，且 composed loss 落在 $[0,1]$。按本课程安全 contraction convention，以至少 $1-\delta$ 的概率，对所有 $f$：

$$
P\ell_f
\le P_m\ell_f
+4L\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

于是完整链为

$$
\boxed{
\text{fat profile}
\Rightarrow
\text{cover/entropy}
\Rightarrow
\widehat{\mathfrak R}(\mathcal F)
\Rightarrow
\widehat{\mathfrak R}(\ell\circ\mathcal F)
\Rightarrow
\text{risk certificate}.}
$$

任何中间箭头的 metric、range 或 Lipschitz 条件缺失，都不能直接跳到风险。

## 十二、常见回归损失合同

### 12.1 Absolute Loss

$$
\ell(t,y)=|t-y|
$$

对 $t$ 全局 1-Lipschitz。但若 $t,y$ 无界，loss 仍无界；high-probability theorem 需 range/tail。

### 12.2 Quantile / Pinball Loss

对 quantile level $\tau\in(0,1)$，令 residual $u=y-t$：

$$
\rho_\tau(u)
=u(\tau-\mathbf1\{u<0\}).
$$

对 prediction $t$ 的 slope 绝对值至多

$$
\max\{\tau,1-\tau\}\le1,
$$

所以是 1-Lipschitz。要得到 conditional quantile consistency，还需 proper target/identifiability argument。

### 12.3 Squared Loss

$$
\ell(t,y)=(t-y)^2
$$

不是全局 Lipschitz。若 $|t|,|y|\le B$，则对 prediction 可取 $L=4B$，loss range 至多 $4B^2$；应用 risk theorem 时要按 range 重标度或使用相应 bounded interval constant。

### 12.4 Huber Loss

Huber loss 在 residual 小时为 quadratic、大时为 linear，因此 gradient 被阈值截住，对 prediction 全局 Lipschitz（常数等于 threshold，依 normalization）。但 robust statistical guarantee 仍需 noise/tail model；“loss 梯度有界”不是自动 robust consistency。

## 十三、与 Margin Classification 的统一视角

classification margin ramp 实际也是实值 score 的 scale-sensitive analysis：

- score class 的 $\gamma$-scale capacity；
- ramp 的 $1/\gamma$ contraction；
- empirical low-margin proportion；
- fat dimension/covering 可替代直接 Rademacher 计算。

所以 margin bound 与 fat-shattering 不是两条无关理论：前者用 task-specific threshold loss，后者提供实值 class 的通用 scale capacity。

## 十四、AI 应用接口

### 14.1 Neural Regression Head

若 encoder 固定，head class 的 fat profile 可由 norm 与 embedding radius 控制。若 end-to-end 学习，需整个 network score class 的 scale-sensitive cover/norm bound。

### 14.2 Reward Model / Preference Score

reward score 通常只在 pairwise differences 上可识别，公共 additive shift 不影响 preference probability。应对 difference class

$$
(x^+,x^-)\mapsto f(x^+)-f(x^-)
$$

定义 metric/fat profile，而不是把不可识别绝对分数当作监督回归真值。

### 14.3 Diffusion Score Regression

score matching output 是向量，loss 常为 squared norm：

$$
\|s_\theta(x,t)-u(x,t)\|_2^2.
$$

scalar fat dimension 与 scalar contraction 不足；需 vector-valued complexity、time/noise sampling unit、output norm、target tail 与 loss clipping/localization。

### 14.4 Calibration/Probability Regression

预测概率若限制在 $[0,1]$，range contract 较干净；但 log loss 在靠近 0/1 时无界且 gradient 爆大。需 probability clipping、logit geometry 或 exp-concave/local analysis，不能只因 output bounded 就宣称 loss bounded。

## 十五、常见误区

> [!danger] 误区 1：fat dimension 就是带 $\gamma$ 下标的 pseudo-dimension
> thresholds 语言相似，但 fat 要求统一 positive margin，保留 scale profile。

> [!danger] 误区 2：$\gamma$ 是允许的预测误差
> 它首先是 shattering resolution；怎样转成 task risk 取决于 loss 与 theorem。

> [!danger] 误区 3：fat dimension 有限就已得到数值 bound
> 还需具体 $\gamma$ profile、cover theorem、integral、loss range/Lipschitz 和 confidence。

> [!danger] 误区 4：连续参数意味着 fat dimension 无限
> norm/range 和 resolution 可使 scale capacity 有限；常数函数区间就是反例。

> [!danger] 误区 5：squared loss 可直接用 $L=1$
> 它不全局 Lipschitz；必须控制 predictions/labels 或换 tail/local theorem。

## 十六、本节最小闭环

面对实值学习问题，应能：

1. 写清 $\gamma$ convention；
2. 写出完整 $\exists r\,\forall s\,\exists f_s$ 量词；
3. 计算/上界 fat profile；
4. 检查 amplitude/range scaling；
5. 选择 fat-to-cover theorem 的 metric；
6. 用 entropy integral 或其他工具得到 Rademacher bound；
7. 核对 loss Lipschitz 与 range/tail；
8. 对 vector/structured output 换用相应 complexity；
9. 区分 scale capacity、learnability 与具体算法效率。

## 十七、20.4 卷总结

本卷形成一条完整的 data-dependent complexity 主线：

$$
\text{ghost sample}
\Rightarrow
\text{symmetrization}
\Rightarrow
\text{Rademacher complexity}
\Rightarrow
\text{loss contraction}
\Rightarrow
\begin{cases}
\text{norm/margin certificate},\\
\text{covering/chaining},\\
\text{localized fixed point},\\
\text{fat-scale regression}.
\end{cases}
$$

它比 global VC counting 更贴近数据与尺度，但没有消除 assumptions：sample law、loss range、norm geometry、selection、confidence 与 computation 仍必须逐项验收。

## 十八、连接

- 前置：[[实值函数类、伪维与阈值化]]、[[覆盖数、Metric Entropy 与 Chaining 入口]]；
- 回看：[[分类间隔、Margin Bound 与 SVM 接口]]、[[局部 Rademacher 复杂度与快收敛率]]；
- 下一卷：[[稳定性、压缩、PAC-Bayes 与信息泛化 MOC]]；
- 模型：[[核岭回归与 Gaussian Process 接口]]；
- 深网：[[神经网络容量与 Norm-Based Bound]]；
- 训练：[[习题 - Fat-Shattering、回归与 Lipschitz 风险]]；
- 解答：[[解答 - Fat-Shattering、回归与 Lipschitz 风险]]。
