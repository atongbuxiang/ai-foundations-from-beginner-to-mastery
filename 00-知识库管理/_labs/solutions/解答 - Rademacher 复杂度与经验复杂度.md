---
type: solution
status: draft
area: [learning-theory/empirical-process, learning-theory/complexity]
topic: "[[习题 - Rademacher 复杂度与经验复杂度]]"
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]"]
related: ["[[收缩引理与 Lipschitz 损失复合]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - Rademacher 复杂度与经验复杂度

> [!warning] 使用边界
> 经验 complexity 是随机 certificate 的一个组成部分，不是单独的泛化结论。任何数值都要同时报告 loss range、confidence 与 supremum/optimization 精度。

## A. 识别与复述

### LT-RAD-A01

$$
\widehat{\mathfrak R}_S(\mathcal F)
=\mathbb E_\sigma\sup_fm^{-1}\sum_i\sigma_if(Z_i)
$$

条件于当前样本，只对 signs 取 expectation。

$$
\mathfrak R_m(\mathcal F)
=\mathbb E_{S\sim P^m}\widehat{\mathfrak R}_S(\mathcal F)
$$

再对 iid sample 取 expectation，因此依赖未知 $P$。

### LT-RAD-A02

- signed：$\mathbb E_\sigma\sup_f m^{-1}\sum\sigma_if_i$；
- absolute：在 supremum/求和外加绝对值；
- symmetric hull：把 $-\mathcal F$ 加入类，使 signed supremum同时覆盖正负方向。

若定义使用 $2/m$，complexity 整体翻倍；若 class 不对称，absolute 与 signed 也不同。故 theorem 中的 2、3 等常数必须和定义一起引用。

### LT-RAD-A03

对 $\mathcal F\subseteq[0,1]^{\mathcal Z}$，以至少 $1-\delta$ 概率，对所有 $f$：

$$
Pf\le P_mf+2\widehat{\mathfrak R}_S(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

$P_mf$ 是 empirical performance，$2\hat R$ 支付 class/data-dependent selection，最后一项支付 gap 与 complexity estimator 的 sample fluctuation。

## B. 手算与数值判断

### LT-RAD-B01

四组 signs 的最大未归一化内积为 $1,1,1,0$，除以 $m=2$ 后为 $1/2,1/2,1/2,0$。故

$$
\widehat{\mathfrak R}_S
=\frac14\left(\frac12+\frac12+\frac12+0\right)
=\frac38=0.375.
$$

### LT-RAD-B02

$$
\frac Rm\sqrt{2\log M}
=\frac{\sqrt{500}}{500}\sqrt{2\log100}
=\sqrt{\frac{2\log100}{500}}
\approx0.1357.
$$

### LT-RAD-B03

$$
3\sqrt{\frac{\log40}{20000}}
\approx3(0.01358)
\approx0.0407.
$$

因此

$$
Pf\le0.12+2(0.03)+0.0407\approx0.2207.
$$

若 risk 本身落在 $[0,1]$，该 certificate非平凡但仍可能远大于 observed empirical risk。

## C. 推导与证明

### LT-RAD-C01

**单调性：**supremum over subset 不超过 supremum over superset。

**缩放：**$a\ge0$ 时

$$
\sup_{af}\sum\sigma_i(af_i)=a\sup_f\sum\sigma_if_i.
$$

**平移：**

$$
\sup_f\sum_i\sigma_i(f_i+g_i)
=\sup_f\sum_i\sigma_if_i+\sum_i\sigma_ig_i,
$$

第二项 expectation 为 0。

**Convex hull：**对固定 $\sigma$，$L_\sigma(f)=\sum_i\sigma_if_i$ 是线性泛函；任意 convex combination 的值是 extreme values 的 convex combination，不超过最大 extreme value。原类包含于 hull，故两边相等。

### LT-RAD-C02

令 $A$ 为 $M$ 个 restriction vectors，$\|a\|_2\le R$。对 $\lambda>0$：

$$
\begin{aligned}
\lambda\mathbb E\max_a\langle\sigma,a\rangle
&\le\log\mathbb Ee^{\lambda\max_a\langle\sigma,a\rangle}\\
&\le\log\sum_a\mathbb Ee^{\lambda\langle\sigma,a\rangle}\\
&\le\log M+\frac{\lambda^2R^2}{2}.
\end{aligned}
$$

最后一步用

$$
\mathbb Ee^{\lambda\sum_i\sigma_ia_i}
=\prod_i\cosh(\lambda a_i)
\le e^{\lambda^2\|a\|_2^2/2}.
$$

除以 $\lambda$，优化

$$
\frac{\log M}{\lambda}+\frac{\lambda R^2}{2}
$$

得 $\lambda^*=\sqrt{2\log M}/R$，值 $R\sqrt{2\log M}$。最后除以 $m$。

### LT-RAD-C03

令 $\Phi(S)=\sup_f(Pf-P_mf)$。

1. symmetrization：$\mathbb E\Phi\le2\mathfrak R_m$；
2. changing one $Z_i$ 使 $\Phi$ 至多变 $1/m$，McDiarmid 控制 $\Phi-\mathbb E\Phi$；
3. changing one $Z_i$ 使 $\widehat{\mathfrak R}_S$ 至多变 $1/m$，McDiarmid 控制 $\mathfrak R_m-\widehat{\mathfrak R}_S$；
4. 为两事件各分配 $\delta/2$，Union Bound 后同时成立；
5. 将第二个不等式代入第一个，收集 confidence terms，得到安全常数 3。

严格常数随 bounded-difference 版本和 log allocation略变，正文 theorem 已固定一套可用形式。

## D. 边界、反例与纠错

### LT-RAD-D01

singleton：

$$
\hat R_S(\{f_0\})
=m^{-1}\sum_if_0(z_i)\mathbb E\sigma_i=0.
$$

但取 $f_0(Z)=Z$、$Z\sim\operatorname{Bernoulli}(1/2)$，$P_mf_0$ 是 Binomial$(m,1/2)/m$，方差 $1/(4m)$，并不等于 $1/2$ 几乎处处。confidence term正控制这类 fixed-query noise。

### LT-RAD-D02

SGD 给出某个 $f_{\rm SGD}$，所以

$$
m^{-1}\sum_i\sigma_if_{\rm SGD}(z_i)
\le\sup_{f\in\mathcal F}m^{-1}\sum_i\sigma_if(z_i).
$$

这是下界。generalization theorem 需要 complexity 的上界；用更小的下界会低估 penalty，破坏 coverage。合法做法是对线性/convex class 精确求 supremum，给优化 oracle 的 certified upper gap，或使用解析 upper bound。

### LT-RAD-D03

取两个函数在样本点上都为 0，但在未见集合 $A$ 上分别为 0 与 1。当前 sample restrictions 相同，因此 empirical complexity不因第二个函数增加。

theorem 不错：若 $P(A)$ 大而样本完全漏掉 $A$，这是低概率 bad sample，由 confidence event支付；若这种漏检常见，则相应 $m,\delta$ 下不能同时保证很小 confidence radius。empirical complexity只测 observed geometry，不能单独担保 sample coverage。

## E. AI 迁移

### LT-RAD-E01

实验合同：

- 固定 $S$、feature preprocessing 与 norm constraint；
- 记录 $B$ 组 signs、seed/PRNG 与 normalization；
- 每组用解析 dual norm或 certified solver求 supremum，报告 optimization gap；
- 记录 sample mean、standard deviation 与 Monte Carlo SE；
- 再用 concentration theorem加 statistical confidence term；
- 保存代码、环境、输入 hash 与完整 sign results。

### LT-RAD-E02

随机-label训练准确率不等于定义中的 complexity，因为：

1. accuracy/0–1 objective 与 signed linear correlation不同；
2. optimizer只找到某个函数，不是 class supremum；
3. 随机 labels可能是 $K$ 类而非 Rademacher signs；
4. 训练含 regularization/augmentation/early stopping，测的是 algorithm class；
5. 通常只跑少量 seeds，没有取准确 sign expectation；
6. network outputs/range normalization与 $1/m$ convention不同。

它仍可作为 noise-fitting diagnostic，但不能直接代入 theorem。

### LT-RAD-E03

不够。winner由同一 sample 的搜索结果决定，只给 winner 单独 certificate忽略 selection。修复：预先定义层级 $\mathcal F_k$ 与 weights $\pi_k$，对每层用 failure budget $\delta\pi_k$ 建 simultaneous empirical Rademacher bound，再最小化 empirical risk + penalty；或对整个 union class计算 complexity；或冻结搜索后用 fresh holdout确认。
