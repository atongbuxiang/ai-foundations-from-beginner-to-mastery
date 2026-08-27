---
type: theorem
status: draft
area: [learning-theory/empirical-process, learning-theory/complexity]
aliases: [Rademacher Complexity, Empirical Rademacher Complexity, 随机符号复杂度]
node_id: LT-26
prerequisites: ["[[Ghost Sample、对称化与经验过程入口]]", "[[浓缩不等式]]", "[[矩阵范数]]", "[[线性泛函与对偶空间]]"]
related: ["[[收缩引理与 Lipschitz 损失复合]]", "[[范数约束线性类的复杂度]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]", "[[局部 Rademacher 复杂度与快收敛率]]"]
sources: ["[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]"]
exercises: ["[[习题 - Rademacher 复杂度与经验复杂度]]"]
solutions: ["[[解答 - Rademacher 复杂度与经验复杂度]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-rademacher-empirical-complexity-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Rademacher 复杂度与经验复杂度

> [!abstract] 本章主问题
> 固定真实样本 $S=(z_1,\ldots,z_m)$ 后，给每个坐标独立 Rademacher sign $\sigma_i\in\{-1,+1\}$。函数类与纯随机 signs 的最大平均相关
> $$
> \widehat{\mathfrak R}_S(\mathcal F)
> =\mathbb E_\sigma\sup_{f\in\mathcal F}
> \frac1m\sum_{i=1}^m\sigma_if(z_i)
> $$
> 是 empirical Rademacher complexity；再对 $S$ 平均得到 $\mathfrak R_m(\mathcal F)$。对 $[0,1]$ 值函数类，一条可直接使用的 high-probability 版本是：以至少 $1-\delta$ 的概率，对所有 $f\in\mathcal F$，
> $$
> Pf
> \le P_mf
> +2\widehat{\mathfrak R}_S(\mathcal F)
> +3\sqrt{\frac{\log(2/\delta)}{2m}}.
> $$
> 复杂度项支付数据依赖选择，confidence 项支付当前样本对期望的随机波动；两者不能互相省略。

> [!question] 初学者读完必须能回答
> 1. supremum 为什么在 $\sigma$ expectation 里面？
> 2. empirical 与 population Rademacher complexity 哪一个可由当前样本估计？
> 3. singleton class 的 signed complexity 为什么为 0，却仍需 confidence term？
> 4. Massart lemma 怎样从有限 restrictions 得到 $\sqrt{\log M/m}$？
> 5. data-dependent bound 为什么不等于不需要 iid、bounded loss 或置信修正？

## 一、学习目标

1. 熟练计算小型 restrictions 的经验复杂度；
2. 区分 signed、absolute 与 symmetric-hull conventions；
3. 证明平移、缩放、单调性与 convex-hull 不变性；
4. 推导 finite-class Massart bound；
5. 从 symmetrization 与 McDiarmid 重建 risk certificate；
6. 解释 empirical complexity 自身为什么还需要 concentration；
7. 设计 Monte Carlo signs 估计并单列数值误差；
8. 判断实际 loss class 是否适合直接代入。

## 二、定义与随机对象

固定样本 $S=(z_1,\ldots,z_m)$。定义

$$
\widehat{\mathfrak R}_S(\mathcal F)
=
\mathbb E_{\sigma_1,\ldots,\sigma_m}
\left[
\sup_{f\in\mathcal F}
\frac1m\sum_{i=1}^m\sigma_if(z_i)
\right].
$$

顺序是：

1. 固定真实样本 locations/observations；
2. 抽 signs；
3. 看过 signs 后选择相关性最大的 $f$；
4. 对 signs 平均最优相关。

population Rademacher complexity 为

$$
\mathfrak R_m(\mathcal F)
=
\mathbb E_{S\sim P^m}
\widehat{\mathfrak R}_S(\mathcal F).
$$

前者是 $S$ 的函数；后者依赖未知 $P$。

### 2.1 为什么没有 absolute value

本节采用 signed supremum convention。若需要 absolute gap，可使用

$$
\mathcal F_\pm=\mathcal F\cup(-\mathcal F)
$$

或定义 absolute complexity。对称类 $\mathcal F=-\mathcal F$ 时，signed supremum 已等于对 absolute signed sum 的 supremum。

## 三、图解：随机符号、样本几何与风险证书

先读图并回答：**图中的 signs 与真实 labels 有何关系？中栏变化的是类还是样本 restrictions？**

![[00-知识库管理/_assets/figures/learning-theory/fig-rademacher-empirical-complexity-v2.svg|900]]

> [!figure] 图 20.4.2｜经验 Rademacher complexity 的定义、数据依赖性与风险账本
> 左栏固定真实样本后拟合 synthetic signs；中栏说明同一类在不同样本几何上可有不同 restrictions；右栏把 empirical loss、complexity penalty 与 confidence term 分账。来源：依据 Bartlett–Mendelson 与现代教材独立绘制；确定性 SVG，由 [[plot_rademacher_core_v2.py]] 生成。

**怎样读图。** 类不是在真实 labels 上训练，而是在固定 sample values 上与独立 signs 做最大相关；这测量“如果把方向随机打乱，类还能多好地追随”。risk certificate 必须对实际 loss class 计算 complexity。

**适用边界（图没有证明什么）。** 图没有证明当前 Monte Carlo complexity estimate 精确，也没有覆盖无界 loss、dependent observations、adaptive sample collection 或 vector-valued contraction。

## 四、四个结构性质

以下均对固定 $S$ 成立。

### 4.1 单调性

若 $\mathcal F\subseteq\mathcal G$，则

$$
\widehat{\mathfrak R}_S(\mathcal F)
\le\widehat{\mathfrak R}_S(\mathcal G),
$$

因为 supremum 的可选集合扩大。

### 4.2 正缩放

对 $a\ge0$，

$$
\widehat{\mathfrak R}_S(a\mathcal F)
=a\widehat{\mathfrak R}_S(\mathcal F).
$$

若 $a<0$，signed class 是否对称会影响写法；通常改用 $|a|$ 与 $-\mathcal F$。

### 4.3 加固定函数不变

令

$$
\mathcal F+g=\{f+g:f\in\mathcal F\}
$$

其中 $g$ 固定，不依赖 $f$ 或 $\sigma$。则

$$
\begin{aligned}
\widehat{\mathfrak R}_S(\mathcal F+g)
&=\mathbb E_\sigma\left[
\sup_f\frac1m\sum_i\sigma_i(f(z_i)+g(z_i))
\right]\\
&=\widehat{\mathfrak R}_S(\mathcal F)
+\mathbb E_\sigma\frac1m\sum_i\sigma_ig(z_i)\\
&=\widehat{\mathfrak R}_S(\mathcal F).
\end{aligned}
$$

这使 contraction lemma 可先减去 $\phi(0)$。

### 4.4 Convex hull 不增加复杂度

对固定 $\sigma$，线性泛函

$$
f\mapsto\sum_i\sigma_if(z_i)
$$

在 convex hull 上的 supremum 由 extreme points 达到。因此

$$
\widehat{\mathfrak R}_S(\operatorname{conv}\mathcal F)
=\widehat{\mathfrak R}_S(\mathcal F).
$$

这对 mixtures/ensembles 很重要：仅允许 convex averaging 不会比 base restrictions 增加这项复杂度，但训练权重、loss 与 base class 本身仍要另审。

## 五、Singleton Class 为什么 Complexity 为 0

若 $\mathcal F=\{f_0\}$，

$$
\widehat{\mathfrak R}_S(\mathcal F)
=\mathbb E_\sigma\frac1m\sum_i\sigma_if_0(z_i)
=0.
$$

因为没有 data-dependent selection：无论 signs 怎样，只能选同一个 $f_0$。

但 $P_mf_0$ 仍是随机均值，可能偏离 $Pf_0$。因此 generalization bound 仍有

$$
O\left(\sqrt{\frac{\log(1/\delta)}m}\right)
$$

confidence term。Rademacher complexity 控制选择/函数类自由度，不取代固定函数的 sampling noise。

## 六、Massart Finite-Class Lemma

固定样本后，把每个 function restriction 写成向量

$$
a_f=(f(z_1),\ldots,f(z_m))\in\mathbb R^m.
$$

设 distinct restriction set

$$
A=\{a_f:f\in\mathcal F\}
$$

有限，$|A|=M$，且

$$
\max_{a\in A}\|a\|_2\le R.
$$

对任意 $\lambda>0$，

$$
\exp\left(\lambda\mathbb E_\sigma\max_{a\in A}\langle\sigma,a\rangle\right)
\le
\mathbb E_\sigma\exp\left(\lambda\max_a\langle\sigma,a\rangle\right)
$$

由 Jensen。再用 maximum 的指数不超过指数和：

$$
\mathbb E e^{\lambda\max_a\langle\sigma,a\rangle}
\le
\sum_{a\in A}\mathbb E e^{\lambda\langle\sigma,a\rangle}.
$$

Rademacher MGF 与 Hoeffding lemma 给出

$$
\mathbb E e^{\lambda\langle\sigma,a\rangle}
=\prod_i\cosh(\lambda a_i)
\le e^{\lambda^2\|a\|_2^2/2}
\le e^{\lambda^2R^2/2}.
$$

取对数并除以 $\lambda$：

$$
\mathbb E_\sigma\max_a\langle\sigma,a\rangle
\le\frac{\log M}{\lambda}+\frac{\lambda R^2}{2}.
$$

最优

$$
\lambda=\frac{\sqrt{2\log M}}R
$$

给出

> [!lemma] Massart finite-class lemma
> $$
> \boxed{
> \widehat{\mathfrak R}_S(\mathcal F)
> \le\frac Rm\sqrt{2\log M}.
> }
> $$

若 $f(z)\in[0,1]$，则 $R\le\sqrt m$，所以

$$
\widehat{\mathfrak R}_S(\mathcal F)
\le\sqrt{\frac{2\log M}{m}}.
$$

$M$ 应是样本上 distinct restrictions 数，不一定等于参数文件或 nominal hypothesis 数。

## 七、High-Probability Risk Bound

> [!theorem] 本课程采用的 empirical Rademacher bound
> 设 $\mathcal F\subseteq[0,1]^{\mathcal Z}$，样本 $S\sim P^m$，并满足常规可测性。则以至少 $1-\delta$ 的概率，对所有 $f\in\mathcal F$，
> $$
> \boxed{
> Pf
> \le P_mf
> +2\widehat{\mathfrak R}_S(\mathcal F)
> +3\sqrt{\frac{\log(2/\delta)}{2m}}.
> }
> $$

### 7.1 证明账本

1. 对称化给
   $$
   \mathbb E\sup_f(Pf-P_mf)
   \le2\mathfrak R_m(\mathcal F).
   $$
2. $f\in[0,1]$ 使 supremum gap 对每个 sample coordinate 的 sensitivity 至多 $1/m$；McDiarmid 把随机 gap 控制到其期望附近。
3. $\widehat{\mathfrak R}_S$ 自身 changing-one-sample sensitivity 也至多 $1/m$；再用 concentration 把未知 $\mathfrak R_m$ 换成 observable $\widehat{\mathfrak R}_S$。
4. 对两个 failure events 分配例如 $\delta/2$ 并合并，得到上面的安全常数 3。

不同教材可能给 $2,3$ 的稍异组合，原因包括 one/two-sided、range $[a,b]$、definition factor 与 concentration sharpening；不可混用。

### 7.2 ERM Excess Risk

若 $\widehat f$ 是 exact ERM，并对 loss class 使用 two-sided common event radius $\Gamma_S$，则

$$
P\widehat f-\inf_{f\in\mathcal F}Pf
\le2\Gamma_S.
$$

若只用 one-sided bound，需检查 comparator direction 是否也覆盖；最稳妥做法是对 $\mathcal F_\pm$ 或双侧 gap 建证书。

## 八、Monte Carlo 估计 Empirical Complexity

当 supremum 可通过优化 oracle 计算时，抽 $B$ 组 signs：

$$
\widehat r_B
=\frac1B\sum_{b=1}^B
\left[
\sup_{f\in\mathcal F}
\frac1m\sum_i\sigma_i^{(b)}f(z_i)
\right].
$$

它估计 $\widehat{\mathfrak R}_S$。但要报告：

- sign seed 与 $B$；
- 每次 supremum 是否 exact，优化 gap 多大；
- score 的 range/tail；
- Monte Carlo standard error；
- 是否用同一 signs 调超参数造成乐观偏差。

若 neural optimizer 只能找到局部较大相关，得到的是 supremum 的**下界**，不能直接作为有效 upper-bound complexity certificate。

## 九、一个 3-函数手算例子

固定 $m=2$，restriction vectors

$$
A=\{(0,0),(1,0),(0,1)\}.
$$

对四个 signs，最大未归一化内积为：

| $\sigma$ | 三个内积 | max |
|---|---|---:|
| $(+,+)$ | $0,1,1$ | 1 |
| $(+,-)$ | $0,1,-1$ | 1 |
| $(-,+)$ | $0,-1,1$ | 1 |
| $(-,-)$ | $0,-1,-1$ | 0 |

所以

$$
\widehat{\mathfrak R}_S
=\frac14\left(\frac12+\frac12+\frac12+0\right)
=\frac38.
$$

Massart 上界用 $R=1,M=3,m=2$：

$$
\frac12\sqrt{2\log3}\approx0.741,
$$

有效但较松。小例子说明 general lemma 的常数不必等于精确 complexity。

## 十、Data-Dependent 的准确含义

$\widehat{\mathfrak R}_S$ 使用真实 sample restrictions，因此可能比只依赖 worst-case VC 维更细。但它仍然：

1. 假设 $S\sim P^m$ 或另有明确依赖结构；
2. 需要 loss range/tail；
3. 是随机量，必须连同 confidence term 使用；
4. 只观察样本上的函数值，不知道 sample 外行为；
5. 对巨大 class 的 supremum 可能难以计算；
6. 可能数值上仍然 vacuous。

## 十一、AI 中的对象映射

### 11.1 线性 probing

固定 representation 后，随机 signs optimization 常退化为对偶范数，能精确/上界计算；[[范数约束线性类的复杂度]]将推导。

### 11.2 深网训练

在完整网络上对随机 signs 重新训练，所得 train correlation 受 optimizer、initialization 和 step budget 限制。它测量“该训练协议找到的噪声拟合”，不必等于 nominal network class supremum。

### 11.3 Loss class 而非 predictor class

若 risk 是 cross-entropy，应控制

$$
\{z\mapsto\ell(f_\theta,z):\theta\in\Theta\},
$$

而不是只控制 argmax predictions。需要[[收缩引理与 Lipschitz 损失复合]]或 vector-valued extension。

### 11.4 模型选择

可为每个 architecture/hyperparameter 层计算 empirical complexity，但若层级根据同一 sample 自适应生成，仍需 simultaneous control；不能只给最终赢家单独算一个 bound。

## 十二、常见错误

> [!warning] “supremum 应该在 expectation 外，因为函数类固定”
> 类固定不等于选择固定。Rademacher complexity正要测量看过 signs 后在类内选择的能力，所以 supremum 在 $\mathbb E_\sigma$ 内。

> [!warning] “singleton complexity 为 0，所以它没有泛化误差”
> 0 只表示没有 selection complexity；固定函数的 empirical mean 仍有 sampling noise，由 confidence term控制。

> [!warning] “empirical complexity 是从数据算的，所以不需要概率假设”
> 从数据算出的随机量要变成 population risk certificate，仍需 sampling law、concentration 与 range。

> [!warning] “用 SGD 拟合 signs 得到的值就是 class complexity”
> 只有 exact supremum 或有证明的 upper-bounding oracle 才能直接代入上界；普通优化结果通常只是下界。

## 十三、本节回顾

1. empirical complexity 的四步随机顺序是什么？
2. 为什么加一个固定函数不改变 signed complexity？
3. convex hull 为什么不增加线性 functional supremum？
4. singleton complexity 为 0 时 confidence term承担什么？
5. Massart lemma 的 $R$ 与 $M$ 分别是什么？
6. empirical risk bound 中 2 与 3 的来源是什么？
7. Monte Carlo signs 估计还需哪两类误差预算？
8. 为什么 loss class 选错会使数值 complexity 无效？

## 十四、来源与后继

- 主要来源：[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]；
- 教材与常数交叉核对：[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]；
- 下一步：[[收缩引理与 Lipschitz 损失复合]]与[[范数约束线性类的复杂度]]；
- 训练闭环：[[习题 - Rademacher 复杂度与经验复杂度]]与[[解答 - Rademacher 复杂度与经验复杂度]]。
