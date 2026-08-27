---
type: concept
status: draft
area: [math/statistics, ai/information-geometry, ai/optimization]
aliases: [Fisher information, score function, Cramér-Rao bound, CRLB, asymptotic normality, Fisher 信息]
prerequisites: ["[[统计模型、估计量与偏差方差]]", "[[最大似然估计与 MAP]]", "[[中心极限定理与 Delta 方法]]", "[[Hessian、二阶微分与曲率]]"]
related: ["[[Bayesian 推断与后验预测]]", "[[假设检验、置信区间与多重比较]]", "[[自然梯度、KL 局部几何与坐标不变性]]", "[[概率论与数理统计 MOC]]"]
sources: ["MIT-18.655-Lecture-13-Information-Inequality", "MIT-18.655-Lecture-17-Asymptotic-Normality", "Casella-Berger-Statistical-Inference", "van-der-Vaart-Asymptotic-Statistics", "Amari-Information-Geometry", "Martens-2020-New-Insights-Natural-Gradient"]
created: 2026-08-19
updated: 2026-08-27
---

# Fisher 信息、Cramér–Rao 界与渐近正态性

> [!abstract] 本章主问题
> 在正则、可辨识的参数模型中，score 是数据对参数的局部敏感度，Fisher 信息是这种敏感度的平均平方，也是 expected log-likelihood curvature。它给无偏估计量设置 Cramér–Rao 方差下界，并决定 regular MLE 的一阶渐近协方差；但这套结论不是“任何模型、任何神经网络、任何有限样本”的通行证，固定支持、内点真值、非奇异信息和一致性等条件一旦失败，速率、极限分布乃至参数本身都可能改变。

## 学习目标

完成本节后，你应当能够：

1. 定义 score、observed information、expected Fisher information，并说明它们是随机对象还是总体对象；
2. 在正则条件下证明 $\mathbb E_\theta[s_\theta(X)]=0$ 与 information identity；
3. 计算 Bernoulli、Gaussian 均值和 Gaussian 方差参数的 Fisher 信息；
4. 证明 iid 信息可加，并推导参数重参数化下的变换律；
5. 从 KL 的二阶展开解释 Fisher 信息的局部几何意义；
6. 用 Cauchy–Schwarz 推导标量 Cramér–Rao 下界，理解等号条件；
7. 正确陈述有偏估计、向量参数和 nuisance parameter 的版本；
8. 从 score equation 的 Taylor 展开推导 MLE 渐近正态性；
9. 区分 model Fisher、empirical Fisher、observed Hessian 与 generalized Gauss–Newton；
10. 识别 Uniform、边界参数、mixture、separation、神经网络对称性等非正则情形。

> [!question] 初学者读完必须能回答
> 1. score、observed information 与 expected Fisher 分别依赖当前数据还是总体分布？
> 2. $\mathbb E_\theta[s_\theta(X)]=0$ 和 information identity 需要哪些支持与交换条件？
> 3. iid 信息为什么可加，重参数化时 Fisher 矩阵怎样变换？
> 4. KL 的局部二阶展开为什么把 Fisher 解释成参数分布族上的局部度量？
> 5. 标量和向量 Cramér–Rao 界约束哪一类估计器，等号何时可能达到？
> 6. score CLT、Hessian LLN、Taylor 展开与一致性怎样共同推出 MLE 渐近正态性？
> 7. 边界、奇异信息、不可辨识和支持依赖参数会破坏证明链的哪一步？

## 阅读前检查

- [[最大似然估计与 MAP]]：likelihood、score equation、interior optimum；
- [[中心极限定理与 Delta 方法]]：独立和的渐近正态性、Slutsky 与非线性变换；
- [[统计模型、估计量与偏差方差]]：sampling distribution、risk、bias 与 efficiency；
- [[Hessian、二阶微分与曲率]]：局部二次近似、正定与奇异曲率。

## 零、先看对象：数据变了，score 也会变

设统计模型为

$$
\mathcal P=\{P_\theta:\theta\in\Theta\subseteq\mathbb R^d\},
$$

并假设 $P_\theta$ 对共同支配测度有密度 $p_\theta(x)$。单个观测的 log-density 是

$$
\ell(\theta;x)=\log p_\theta(x).
$$

### Score

score vector 定义为

$$
s_\theta(x)
=\nabla_\theta\ell(\theta;x)
=\nabla_\theta\log p_\theta(x).
$$

若 $X\sim P_\theta$，则 $s_\theta(X)$ 是随机向量。它回答：

> 对当前样本 $X$ 而言，参数向哪个局部方向移动会最快提高 log-density？

它不是“模型得分高低”，也不是预测类别的 logit。

### 样本 score

若 $X_1,\ldots,X_n$ iid，

$$
\ell_n(\theta)=\sum_{i=1}^n\ell(\theta;X_i),
\qquad
s_n(\theta)=\nabla\ell_n(\theta)
=\sum_{i=1}^n s_\theta(X_i).
$$

内点 MLE 若可微，通常满足 $s_n(\widehat\theta)=0$。但边界解、不可微点、无有限极大值或多个极大值不必满足这一叙述。

先用下图回答一个视觉问题：**score 的随机性怎样平均成 Fisher 信息，再分别进入 Cramér–Rao 下界与 MLE 渐近正态性的证明链？**

![[00-知识库管理/_assets/figures/probability/fig-fisher-crlb-asymptotic-v2.svg|880]]

> [!figure] 图 10.5.17｜Score、Fisher 信息、Cramér–Rao 与 MLE 渐近链
> A 把不同样本产生的 score 画在零均值轴上，并区分随机 observed information 与总体 Fisher；B 用两种 sampling spread 表示 CRLB 是声明估计器类别内的方差下界；C 把 score CLT、Hessian LLN、局部 Taylor 与 MLE 极限连接起来。来源：独立绘制；生成脚本：[[plot_statistical_estimation_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先对数据随机性取平均再谈 $I(\theta)$，不要把单批 observed Hessian 直接叫总体 Fisher；B 先核对无偏/正则等适用类别，再比较方差；C 从上到下逐项检查 CLT、曲率收敛、展开点一致性和余项控制，缺一项都不能只凭最终公式补回。

**适用边界（图没有证明什么）。** score 点列不证明均值必为零，相关恒等式需要固定支持与微分积分可交换；CRLB 不禁止有偏估计以偏差换取更小 MSE；渐近正态图不覆盖有限样本、边界真值、奇异 mixture、separation 或神经网络参数对称导致的非正则情形。

## 进入正文前：从单个样本的局部敏感度走到估计精度

> [!info] 课程位置
> 上一章已经得到 Bernoulli MLE；本章解释它的局部精度为何由 likelihood 曲率控制。score 是随数据变化的局部斜率，Fisher 是其总体平方尺度，Cramér–Rao 在指定估计器类别中给下界，而 MLE 渐近正态性还需要 CLT、LLN、一致性与 Taylor 余项共同闭合。下一章会从点估计转向完整 posterior。

> [!tip] 建议两遍阅读
> - 第一遍只计算 Bernoulli score、Fisher、CRLB 和样本均值的方差，观察下界何时取等。
> - 第二遍再学习 information identity、KL 局部几何、重参数化、向量/nuisance 版本、MLE 渐近证明和非正则边界。不要把单批 Hessian、empirical Fisher 与总体 Fisher 混为一谈。

> [!question] 本章的推导问题链
> 1. score 为什么随观测变化，而 Fisher 是固定参数下的总体量？
> 2. score 均值为零需要哪些支持与交换条件？
> 3. iid 样本的信息为什么按 $n$ 相加？
> 4. Cramér–Rao 下界限制的是方差还是任意意义下的误差？
> 5. 样本均值为何在 Bernoulli 模型中恰好达到无偏 CRLB？
> 6. Fisher 曲率怎样与 MLE 的 $\sqrt n$ 渐近正态性连接？
> 7. 边界参数、不可辨识或奇异信息会让哪一步失效？

### 贯穿例：Bernoulli 信息与样本均值的精度

设单个观测

$$
Y\sim\operatorname{Bernoulli}(q),
\qquad 0<q<1.
$$

log-likelihood 为

$$
\ell(q;Y)=Y\log q+(1-Y)\log(1-q).
$$

score 是

$$
s_q(Y)
=\frac{\partial}{\partial q}\ell(q;Y)
=\frac{Y}{q}-\frac{1-Y}{1-q}
=\frac{Y-q}{q(1-q)}.
$$

它在两种观测下取不同值：

$$
s_q(1)=\frac1q,
\qquad
s_q(0)=-\frac1{1-q}.
$$

总体均值为

$$
\mathbb E_q[s_q(Y)]
=q\frac1q+(1-q)\left(-\frac1{1-q}\right)
=0.
$$

单观测 Fisher 信息为

$$
\begin{aligned}
I_1(q)
&=\mathbb E_q[s_q(Y)^2]\\
&=q\frac1{q^2}+(1-q)\frac1{(1-q)^2}\\
&=\frac1{q(1-q)}.
\end{aligned}
$$

在贯穿真值 $q_\star=3/10$ 处，

$$
I_1(q_\star)=\frac{100}{21}.
$$

对 $n$ 个 iid 观测，sample score 是单观测 score 之和。独立性和零均值使信息相加：

$$
I_n(q)=nI_1(q)=\frac{n}{q(1-q)}.
$$

因此任意满足相应正则条件的无偏估计器 $T$ 都服从

$$
\operatorname{Var}_q(T)
\ge\frac1{I_n(q)}
=\frac{q(1-q)}n.
$$

而 Bernoulli MLE/样本均值

$$
\widehat q=\frac1n\sum_{i=1}^nY_i
$$

恰好满足

$$
\mathbb E_q[\widehat q]=q,
\qquad
\operatorname{Var}_q(\widehat q)
=\frac{q(1-q)}n.
$$

所以它在这个正则标量问题中有限样本就达到 CRLB。这个结论依赖具体模型和估计目标，不能推广成“任何 MLE 都有限样本最优”。

对观测 $n=10,K=3$，observed information 是

$$
j_n(q)
=-\ell_n''(q)
=\frac{K}{q^2}+\frac{n-K}{(1-q)^2}.
$$

在 $\widehat q=3/10$ 处，

$$
\begin{aligned}
j_n(\widehat q)
&=\frac3{(3/10)^2}+\frac7{(7/10)^2}\\
&=\frac{100}{3}+\frac{100}{7}
=\frac{1000}{21}.
\end{aligned}
$$

这一次恰好等于 $I_{10}(\widehat q)$，但 observed information 一般随数据变化，expected Fisher 则在固定参数下对数据平均，二者不能靠名称直接等同。

最后，CLT 给出

$$
\sqrt n(\widehat q-q)
\xrightarrow d
\mathcal N(0,q(1-q)).
$$

在 $q_\star=3/10$ 处，渐近方差为 $21/100$，$\widehat q$ 的渐近标准误为

$$
\sqrt{\frac{21}{100n}}.
$$

有限 $n=10$ 时这个标准误约为 $0.145$，但近似质量仍需单独检查；参数靠近 $0$ 或 $1$ 时，Gaussian 近似会越过合法参数区间，正则内点叙述也逐渐失真。

> [!note] 本轮对象账本
> | 对象 | 是否随机 | 本例 |
> |---|---|---|
> | $s_q(Y)$ | 是 | 单个观测产生的 likelihood 局部斜率 |
> | $j_n(q)$ | 是 | 给定样本后的负 Hessian |
> | $I_1(q)$ | 否 | 固定 $q$ 下 score 平方的总体期望 |
> | $I_n(q)$ | 否 | $n$ 个 iid 样本的总体信息 |
> | CRLB | 否 | 指定无偏正则估计器类别中的方差下界 |
> | $\widehat q$ | 是 | 数据函数及其 sampling distribution |

> [!analysis] Cramér–Rao 与 MLE 渐近链的公式七问
> 1. **为什么引入？** Fisher 描述模型对参数局部变化的可辨认程度，CRLB 把它转成估计精度基准。
> 2. **对象是什么？** score 是随机变量，Fisher 是总体二阶矩，CRLB 比较固定参数下估计器的 sampling variance。
> 3. **条件是什么？** 固定支持、可交换微分积分、可辨识、有限非零信息；经典标量式还限制无偏正则估计器。
> 4. **下界怎样推出？** 将估计器中心化误差与 score 的协方差恒等式代入 Cauchy–Schwarz。
> 5. **MLE 渐近式怎样推出？** 在真值附近展开 score equation，以 score CLT 给分子、Hessian LLN 给分母，再用一致性和 Slutsky。
> 6. **边界在哪里？** 有偏收缩可获得更小 MSE；边界、mixture、separation、参数对称和奇异 Fisher 会改变速率或极限分布。
> 7. **AI 中对应什么？** natural gradient、Laplace 近似和二阶优化都借用局部信息几何；empirical Fisher 或 mini-batch Hessian 不是自动有效的统计 Fisher。

> [!success] 第一遍停靠线
> 应能从 Bernoulli log-likelihood 推出 $s_q(Y)=(Y-q)/(q(1-q))$ 与 $I_1(q)=1/[q(1-q)]$；在 $q=3/10,n=10$ 处得到总信息 $1000/21$ 和 CRLB $21/1000$；还能说明样本均值为何取等，以及这一点为何不代表任意模型中的 MLE 都有限样本有效。

## 一、为什么 score 的期望通常为零

先看连续情形。若支持集不随 $\theta$ 改变，且允许把微分移入积分，则

$$
\begin{aligned}
\mathbb E_\theta[s_\theta(X)]
&=\int \nabla_\theta\log p_\theta(x)\,p_\theta(x)\,dx\\
&=\int \frac{\nabla_\theta p_\theta(x)}{p_\theta(x)}p_\theta(x)\,dx\\
&=\int \nabla_\theta p_\theta(x)\,dx\\
&=\nabla_\theta\int p_\theta(x)\,dx\\
&=\nabla_\theta 1=0.
\end{aligned}
$$

离散情形把积分换成求和即可，但仍要有交换求和与微分的条件。

> [!warning] “通常”为零不是无条件定理
> 若支持依赖参数，边界项可能出现。例如 $X\sim\operatorname{Unif}(0,\theta)$，密度含 $\mathbf 1\{0<x<\theta\}$；只对区间内部写 $\partial_\theta\log p=-1/\theta$ 会得到非零均值。问题不是算术错误，而是忽略了移动支持边界，经典正则推导已经失效。

## 二、Fisher 信息的三个面孔

### 2.1 Score covariance

单样本 Fisher information matrix 定义为

$$
I(\theta)
=\mathbb E_\theta\!\left[
s_\theta(X)s_\theta(X)^\top
\right].
$$

在 score 均值为零时，它就是 score 的协方差矩阵：

$$
I(\theta)=\operatorname{Cov}_\theta(s_\theta(X)).
$$

因此 $I(\theta)$ 必为对称半正定矩阵：对任意 $v$，

$$
v^\top I(\theta)v
=\mathbb E[(v^\top s_\theta(X))^2]\ge 0.
$$

### 2.2 Negative expected Hessian

对 identity $\mathbb E_\theta[s_\theta(X)]=0$ 再求导。第 $j,k$ 个分量满足

$$
0
=\partial_{\theta_k}\mathbb E_\theta[s_j(X)]
=\mathbb E_\theta[\partial_{\theta_k}s_j(X)]
+\mathbb E_\theta[s_j(X)s_k(X)].
$$

故在足够正则时

$$
I(\theta)
=-\mathbb E_\theta[
\nabla_\theta^2\log p_\theta(X)
].
$$

这称 information identity。它把两件事连在一起：

- score 在重复样本间波动多大；
- expected log-likelihood 在真参数附近弯得多厉害。

### 2.3 局部 KL 几何

设 $\delta$ 很小，展开

$$
D_{\mathrm{KL}}(P_\theta\|P_{\theta+\delta})
=\mathbb E_\theta[
\log p_\theta(X)-\log p_{\theta+\delta}(X)
].
$$

对第二项作 Taylor 展开：

$$
\log p_{\theta+\delta}(X)
=\log p_\theta(X)
+s_\theta(X)^\top\delta
+\frac12\delta^\top
\nabla^2\log p_\theta(X)\delta
+o(\|\delta\|^2).
$$

取期望，线性项因 score mean zero 消失，得到

$$
D_{\mathrm{KL}}(P_\theta\|P_{\theta+\delta})
=\frac12\delta^\top I(\theta)\delta
+o(\|\delta\|^2).
$$

所以 Fisher information 是模型分布空间的局部度量张量：参数坐标距离相同，不表示分布变化相同；$\delta^\top I\delta$ 衡量的是可区分程度。

## 三、四个“信息/曲率”对象必须分开

设 negative log-likelihood 为 $L_n(\theta)=-\ell_n(\theta)$。

### Expected/model Fisher

$$
I(\theta)=
\mathbb E_{X\sim p_\theta}[s_\theta(X)s_\theta(X)^\top].
$$

期望是在模型自身 $p_\theta$ 下取的，是总体对象。

### Observed information

$$
J_n(\theta)
=-\nabla^2\ell_n(\theta)
=\nabla^2 L_n(\theta).
$$

它依赖当前数据，可不处处半正定；通常在 MLE 附近并在良好情形下近似 $nI(\theta_0)$。

### Empirical Fisher

常见实现把逐样本梯度外积平均：

$$
\widehat F_{\rm emp}(\theta)
=\frac1n\sum_{i=1}^n
s_\theta(x_i)s_\theta(x_i)^\top.
$$

它在固定训练标签上取经验平均，不等于对模型生成标签取期望的 model Fisher。仅在模型正确、样本足够、score 定义和采样层次匹配时，二者才可能靠近。

### Generalized Gauss–Newton

对复合损失 $L(\theta)=\ell(f_\theta(x),y)$，GGN 保留输出损失的 Hessian，忽略网络输出映射的某些二阶项：

$$
G=J_f^\top H_{\ell,f}J_f.
$$

对某些 exponential-family likelihood 与 canonical output，GGN 可与 model Fisher 对齐；一般不能把所有这些矩阵都简称“Fisher”。

| 对象 | 平均/随机性来源 | 必为 PSD？ | 常见用途 |
|---|---|---:|---|
| $I(\theta)$ | 模型分布总体期望 | 是 | 理论下界、局部几何 |
| $J_n(\theta)$ | 已观测数据的 Hessian | 否 | 局部标准误、Newton |
| empirical Fisher | 已观测逐样本梯度外积 | 是 | 可计算预条件近似 |
| GGN | 输出 Jacobian 与 loss curvature | 常为是 | 二阶优化近似 |

## 四、iid 样本的信息为什么可加

独立样本 score 为

$$
s_n(\theta)=\sum_{i=1}^n s_i(\theta).
$$

因此

$$
I_n(\theta)
=\mathbb E[s_ns_n^\top]
=\sum_i\mathbb E[s_is_i^\top]
+\sum_{i\ne j}\mathbb E[s_i]\mathbb E[s_j]^\top.
$$

正则情形下每项 score mean 为零，故交叉项消失：

$$
I_n(\theta)=nI_1(\theta).
$$

这解释了 standard error 常按 $n^{-1/2}$ 缩小，而 variance 按 $n^{-1}$ 缩小。

> [!warning] 依赖数据不能直接乘 $n$
> 时间序列、cluster、重复增强样本或同一用户的多个 token 会产生 score cross-covariance。此时信息与方差需要依赖结构、cluster-robust 或 long-run covariance，而不是假装观测 iid。

## 五、经典模型的 Fisher 信息

### 5.1 Bernoulli 参数 $p$

若 $X\sim\operatorname{Bernoulli}(p)$，

$$
\ell(p;X)=X\log p+(1-X)\log(1-p).
$$

score 为

$$
s_p(X)
=\frac{X}{p}-\frac{1-X}{1-p}
=\frac{X-p}{p(1-p)}.
$$

所以

$$
I_1(p)
=\frac{\operatorname{Var}(X)}{p^2(1-p)^2}
=\frac1{p(1-p)}.
$$

$n$ 个 iid 样本的信息是

$$
I_n(p)=\frac{n}{p(1-p)}.
$$

这并不表示边界 $p\to0$ 时推断一定“无限容易”；边界处 regular interior asymptotics 失效，局部参数尺度也改变。

### 5.2 Gaussian 均值，方差已知

若 $X\sim\mathcal N(\mu,\sigma^2)$，$\sigma^2$ 已知，

$$
s_\mu(X)=\frac{X-\mu}{\sigma^2}.
$$

故

$$
I_1(\mu)=\frac1{\sigma^2},
\qquad
I_n(\mu)=\frac n{\sigma^2}.
$$

样本均值方差为 $\sigma^2/n=1/I_n(\mu)$，正好达到后文的 Cramér–Rao 下界。

### 5.3 Gaussian 方差参数 $v=\sigma^2$，均值已知

$$
\ell(v;X)
=-\frac12\log(2\pi v)-\frac{(X-\mu)^2}{2v},
$$

$$
s_v(X)
=-\frac1{2v}+\frac{(X-\mu)^2}{2v^2}.
$$

利用 $\operatorname{Var}((X-\mu)^2)=2v^2$，

$$
I_1(v)=\frac1{2v^2}.
$$

若改用 $\eta=\log v$，链式法则给

$$
s_\eta=s_v\frac{dv}{d\eta}=v s_v,
\qquad
I_1(\eta)=v^2I_1(v)=\frac12.
$$

同一模型在不同参数坐标中的矩阵数值不同，但诱导的局部 KL 二次型不变。

### 5.4 Gaussian 的 $(\mu,v)$ 联合参数

可以验证交叉信息为零：

$$
I_1(\mu,v)
=\begin{pmatrix}
1/v & 0\\
0 & 1/(2v^2)
\end{pmatrix}.
$$

零交叉项称局部 orthogonality，不等于两个估计量在所有有限样本下都独立。

## 六、重参数化：信息矩阵怎样变换

设旧参数 $\theta=g(\phi)$，Jacobian 为

$$
J=\frac{\partial\theta}{\partial\phi^\top}.
$$

链式法则给

$$
s_\phi=J^\top s_\theta.
$$

于是

$$
I_\phi(\phi)=J^\top I_\theta(\theta)J.
$$

若参数变换局部可逆，则

$$
d\phi^\top I_\phi d\phi
=d\theta^\top I_\theta d\theta.
$$

因此 Fisher matrix 的元素依赖坐标，而分布空间的局部长度不依赖坐标。这正是 information geometry 与 natural gradient 的出发点。

## 七、Cramér–Rao 下界：先陈述正确版本

设标量参数 $\theta$，统计量 $T=T(X_{1:n})$ 的均值为

$$
m(\theta)=\mathbb E_\theta[T].
$$

在可交换微分与积分且二阶矩有限等正则条件下，

$$
\operatorname{Var}_\theta(T)
\ge
\frac{[m'(\theta)]^2}{I_n(\theta)}.
$$

若 $T$ 是 $g(\theta)$ 的无偏估计量，即 $m(\theta)=g(\theta)$，则

$$
\operatorname{Var}_\theta(T)
\ge
\frac{[g'(\theta)]^2}{I_n(\theta)}.
$$

特别地，对 $\theta$ 本身无偏时：

$$
\operatorname{Var}_\theta(T)
\ge\frac1{I_n(\theta)}
=\frac1{nI_1(\theta)}.
$$

## 八、Cramér–Rao 的证明

令联合 score 为 $S=s_n(\theta)$。先算 covariance：

$$
\begin{aligned}
\mathbb E_\theta[T S]
&=\int T(x)\,\partial_\theta\log p_\theta^{(n)}(x)
\,p_\theta^{(n)}(x)dx\\
&=\int T(x)\,\partial_\theta p_\theta^{(n)}(x)dx\\
&=\partial_\theta\int T(x)p_\theta^{(n)}(x)dx\\
&=m'(\theta).
\end{aligned}
$$

又因为 $\mathbb E[S]=0$，所以

$$
\operatorname{Cov}(T,S)=m'(\theta).
$$

由 covariance 版 Cauchy–Schwarz，

$$
\operatorname{Cov}(T,S)^2
\le \operatorname{Var}(T)\operatorname{Var}(S).
$$

而 $\operatorname{Var}(S)=I_n(\theta)$，故

$$
[m'(\theta)]^2
\le \operatorname{Var}(T)I_n(\theta),
$$

整理即得下界。

### 何时等号成立

Cauchy–Schwarz 取等要求中心化估计误差与 score 几乎处处线性相关：

$$
T-m(\theta)=a(\theta)S.
$$

这是一项很强的结构要求，所以不是每个模型都存在有限样本达到 CRLB 的估计器。

## 九、CRLB 不是“所有估计器 MSE 的地板”

### 9.1 有偏估计器

若 bias 为 $b(\theta)=m(\theta)-\theta$，则

$$
m'(\theta)=1+b'(\theta).
$$

广义方差界为

$$
\operatorname{Var}(T)
\ge\frac{[1+b'(\theta)]^2}{I_n(\theta)}.
$$

而 MSE 是

$$
\operatorname{MSE}(T)
=\operatorname{Var}(T)+b(\theta)^2.
$$

所以 shrinkage、regularization 或 Bayes estimator 可以通过引入小偏差换取更大的方差下降，在 MSE 上优于无偏估计器的方差下界。这不违反 CRLB，因为比较对象改变了。

### 9.2 CRLB 是逐点结论

它在每个固定 $\theta$ 处陈述。一个估计器可能在某个点表现特别好，却在其邻域付出代价；不能把逐点下界自动升级成 uniform/minimax 结论。

### 9.3 有限样本与渐近效率不同

“MLE 渐近达到 $I^{-1}$”不意味着任意 $n$ 都无偏、高斯或最优。有限样本偏差、多峰、边界和长尾可能很明显。

## 十、向量参数的 information inequality

设 $T\in\mathbb R^k$ 估计 $g(\theta)\in\mathbb R^k$，其中 $\theta\in\mathbb R^d$。记

$$
G(\theta)=\frac{\partial g(\theta)}{\partial\theta^\top}
\in\mathbb R^{k\times d}.
$$

在无偏与正则条件下，

$$
\operatorname{Cov}_\theta(T)
\succeq
G(\theta)I_n(\theta)^{-1}G(\theta)^\top.
$$

$A\succeq B$ 表示 $A-B$ 半正定，也就是任意线性方向 $a$ 上都有

$$
\operatorname{Var}(a^\top T)
\ge
a^\top G I_n^{-1}G^\top a.
$$

若 $I$ 奇异，普通逆不存在；这通常提示局部不可辨识、冗余参数或模型对称性。直接写 $I^{-1}$ 已经不合法，需先明确 identifiable quotient、约束、目标函数或广义逆的含义。

## 十一、Nuisance parameter 与 Schur 补

把参数分为目标 $\psi$ 和 nuisance $\lambda$：

$$
I(\theta)=
\begin{pmatrix}
I_{\psi\psi}&I_{\psi\lambda}\\
I_{\lambda\psi}&I_{\lambda\lambda}
\end{pmatrix}.
$$

若 $\lambda$ 已知，关于 $\psi$ 的信息是 $I_{\psi\psi}$。若 $\lambda$ 未知且需共同估计，有效信息变为 Schur complement：

$$
I_{\psi\cdot\lambda}
=I_{\psi\psi}
-I_{\psi\lambda}I_{\lambda\lambda}^{-1}I_{\lambda\psi}.
$$

由于减去半正定项，未知 nuisance 通常降低目标参数的有效信息。相应协方差下界是

$$
\operatorname{Cov}(\widehat\psi)
\succeq
\frac1n I_{\psi\cdot\lambda}^{-1}.
$$

## 十二、MLE 渐近正态性：证明骨架

设真参数为内点 $\theta_0$，$\widehat\theta_n$ 是一致的局部 MLE。score equation 为

$$
s_n(\widehat\theta_n)=0.
$$

在 $\theta_0$ 附近 Taylor 展开：

$$
0=s_n(\theta_0)
+H_n(\widetilde\theta_n)
(\widehat\theta_n-\theta_0),
$$

其中

$$
H_n(\theta)=\nabla^2_\theta\ell_n(\theta).
$$

移项并乘 $\sqrt n$：

$$
\sqrt n(\widehat\theta_n-\theta_0)
=-\left[\frac1nH_n(\widetilde\theta_n)\right]^{-1}
\left[\frac1{\sqrt n}s_n(\theta_0)\right].
$$

接下来分别处理两个括号。

### Score 的 CLT

score iid、均值零、协方差 $I(\theta_0)$，故

$$
\frac1{\sqrt n}s_n(\theta_0)
=\frac1{\sqrt n}\sum_{i=1}^n s_{\theta_0}(X_i)
\xrightarrow d
\mathcal N(0,I(\theta_0)).
$$

### Hessian 的 LLN

若 Hessian 可积、局部一致收敛且估计量一致，则

$$
-\frac1nH_n(\widetilde\theta_n)
\xrightarrow p I(\theta_0).
$$

### Slutsky 合并

所以

$$
\boxed{
\sqrt n(\widehat\theta_n-\theta_0)
\xrightarrow d
\mathcal N(0,I(\theta_0)^{-1})
}.
$$

等价地，对大样本可写近似

$$
\widehat\theta_n
\approx
\mathcal N\!\left(
\theta_0,\frac1n I(\theta_0)^{-1}
\right).
$$

> [!important] 这不是“loss 二次，所以参数必 Gaussian”
> 真正逻辑是：score 的随机和由 CLT 变 Gaussian；Hessian 的归一化由 LLN 稳定为确定矩阵；一致性保证展开点留在真值邻域；最后才由线性化和 Slutsky 得出参数误差的渐近 Gaussian。

## 十三、正则条件清单

不同教材技术条件略有差异，但使用上至少要审计：

1. **真值与模型**：$P_0=P_{\theta_0}$，或明确是在错设模型下讨论 pseudo-true parameter；
2. **内点**：$\theta_0$ 位于参数空间内部，不在概率、方差、稀疏度等边界；
3. **可辨识**：$P_\theta=P_{\theta_0}$ 能推出目标参数相同；
4. **共同支持**：密度支持在真值邻域不随参数移动；
5. **平滑性**：log-density 有足够阶数导数；
6. **交换合法**：可以交换求导与积分/期望；
7. **矩条件**：score 有有限二阶矩，Hessian 受可积函数控制；
8. **非奇异信息**：$I(\theta_0)$ 正定；
9. **一致性**：选到的 MLE 分支确实收敛到 $\theta_0$；
10. **局部唯一性**：真值邻域内有稳定 stationary solution；
11. **LLN/CLT 条件**：依赖、重尾与非平稳性没有破坏所用极限定理；
12. **固定维数**：经典结论通常令 $d$ 固定、$n\to\infty$，不自动覆盖 $d/n$ 不消失的现代高维极限。

把“常见条件下”删掉而只抄结论，是统计推断里最危险的压缩方式之一。

## 十四、标准误与三个经典检验接口

在正则 MLE 下，可用 observed information 或 plug-in expected information：

$$
\widehat{\operatorname{Cov}}(\widehat\theta)
\approx J_n(\widehat\theta)^{-1}
\approx \frac1n I(\widehat\theta)^{-1}.
$$

某坐标标准误为协方差矩阵相应对角元的平方根。

这导向三种一阶等价的 classical inference：

- **Wald**：估计值离 null 多远，以估计 standard error 标准化；
- **Score**：只在 null 参数处看 score 与 Fisher 信息；
- **Likelihood ratio**：比较约束与非约束 maximized log-likelihood。

它们在正则大样本下常渐近等价，但有限样本、边界或弱可辨识时可明显分歧。正式的区间、$p$ 值与多重比较见[[假设检验、置信区间与多重比较]]。

## 十五、模型错设：为什么出现 sandwich covariance

若真实分布 $Q$ 不在 $\{P_\theta\}$ 中，MLE 通常收敛到 KL projection

$$
\theta^*=\arg\min_\theta D_{\rm KL}(Q\|P_\theta).
$$

在 $Q$ 下定义

$$
H=-\mathbb E_Q[\nabla^2\ell(\theta^*;X)],
\qquad
J=\mathbb E_Q[s_{\theta^*}(X)s_{\theta^*}(X)^\top].
$$

模型正确时 information identity 给 $H=J=I$。错设时一般 $H\ne J$，于是

$$
\sqrt n(\widehat\theta-\theta^*)
\xrightarrow d
\mathcal N(0,H^{-1}JH^{-\top}).
$$

形如“bread–meat–bread”的结构称 sandwich covariance。若仍盲用 inverse Hessian $H^{-1}$，standard error 可能错误。

对于 cluster/dependent data，$J$ 还要替换成 score 的 cluster 或 long-run covariance。

## 十六、非正则例 1：Uniform 的极值统计量

令 $X_i\stackrel{iid}\sim\operatorname{Unif}(0,\theta)$。likelihood 为

$$
L(\theta;x)=\theta^{-n}\mathbf 1\{\theta\ge X_{(n)}\},
$$

故

$$
\widehat\theta_{\rm MLE}=X_{(n)}.
$$

它有偏：

$$
\mathbb E[X_{(n)}]=\frac n{n+1}\theta.
$$

更关键的是其误差尺度为 $1/n$，不是 $1/\sqrt n$。对 $t\ge0$，

$$
\Pr\!\left(
n\frac{\theta-X_{(n)}}{\theta}>t
\right)
=\Pr\left(X_{(n)}<\theta(1-t/n)\right)
=(1-t/n)^n\to e^{-t}.
$$

因此

$$
n\frac{\theta-X_{(n)}}\theta
\xrightarrow d \operatorname{Exp}(1).
$$

这不是 MLE 理论“失败得更差”，而是移动支持边界提供了不同种类的信息，产生更快但非 Gaussian 的极限。

## 十七、更多非正则与现代模型边界

### 参数在边界

Bernoulli $p=0/1$、variance component 为零、mixture weight 为零时，局部邻域不是完整 Euclidean 空间；Wald normal approximation 和标准 $\chi^2$ likelihood-ratio 极限可失效。

### Logistic separation

线性可分数据使 logistic log-likelihood 沿某方向持续上升，有限 MLE 不存在。此时不能在“MLE 点”计算常规 inverse information；regularization/Firth correction/先验会定义不同估计问题。

### Mixture singularity

component 重合或权重趋零时参数不可辨识，Fisher 信息退化；label permutation 还造成多个等价参数点。经典 $\sqrt n$ Gaussian 只可能在避开 singular set 的局部正则区域成立。

### 神经网络对称性

hidden-unit permutation、ReLU 层间缩放、冗余宽度会让多个参数代表同一函数。全参数 Fisher 可奇异；“参数置信区间”也未必是有意义的目标。预测函数或某个 identifiable functional 往往更合理。

### 高维与插值

当参数维数随样本增长、$d\ge n$、training loss 可插值时，固定维经典 MLE 渐近理论不自动适用。需使用高维统计、随机矩阵、隐式正则化或函数空间理论。

## 十八、超效率：在一个点击败下界为什么不够

Hodges 型估计器可在某个特殊点以比 $n^{-1/2}$ 更快的速度收敛，看似击败 regular efficient estimator。但代价是该点附近有一圈越来越窄、风险却更差的参数区域。

这提醒我们区分：

- fixed-$\theta$ pointwise asymptotics；
- local alternatives，如 $\theta_n=\theta_0+h/\sqrt n$；
- uniform risk 与 minimax risk；
- regular estimator class。

现代渐近效率理论用 local asymptotic normality、convolution theorem 等更精确地说明：在 regular estimator 类中，$I^{-1}$ 是局部 Gaussian noise 的不可消除部分。初学阶段先记住：单点漂亮不能替代邻域稳定。

## 十九、Natural gradient：从坐标梯度到分布步长

普通 gradient step

$$
\delta=-\eta\nabla_\theta L
$$

取决于参数坐标尺度。若约束一步造成的局部 KL 改变量：

$$
\frac12\delta^\top I(\theta)\delta\le\varepsilon,
$$

并在线性近似下最大化目标下降，Lagrange multiplier 推出方向

$$
\delta\propto-I(\theta)^{-1}\nabla_\theta L.
$$

这称 natural gradient。它尝试让一步的大小按“模型分布改变多少”而不是“参数坐标移动多少”计量。

> [!warning] 公式短，实现不短
> 深度网络的 $I$ 巨大且常奇异。对角、block、K-FAC、low-rank、damping 和 empirical Fisher 都是在改变近似。必须报告所用对象、采样方式、阻尼和线性求解误差，不能只写“使用 Fisher”。

## 二十、分类与语言模型中的条件 Fisher

对条件模型 $p_\theta(y\mid x)$，固定输入 $x$ 的 model Fisher 可写为

$$
F_x(\theta)
=\mathbb E_{Y\sim p_\theta(\cdot\mid x)}
[\nabla\log p_\theta(Y\mid x)
\nabla\log p_\theta(Y\mid x)^\top].
$$

再对输入分布平均：

$$
F(\theta)=\mathbb E_{X\sim q(x)}[F_X(\theta)].
$$

这里至少有三个选择：

1. $Y$ 从模型采样，还是使用数据标签？
2. $X$ 从训练经验分布、目标部署分布，还是某个生成模型采样？
3. 对 token/sequence 是逐条件项，还是保留同一序列 score 的 cross-covariance？

不同选择得到不同矩阵。

### Softmax logit 空间

若类别概率 $p=\operatorname{softmax}(z)$，对 logit $z$ 的 Fisher/Hessian 为

$$
F_z=\operatorname{Diag}(p)-pp^\top.
$$

它半正定且有零方向 $\mathbf 1$，因为所有 logits 同加常数不改变 softmax。这是局部不可辨识的具体例子。

通过网络 Jacobian $J_z=\partial z/\partial\theta^\top$ 拉回参数空间：

$$
F_\theta=J_z^\top F_zJ_z.
$$

## 二十一、数值计算与诊断

### 不显式形成大矩阵

若参数上亿，$d\times d$ 矩阵不可存。常用：

- Fisher-vector product：先算 $Jv$ 再算 $J^\top(F_zJv)$；
- Hessian-vector product：自动微分 Pearlmutter trick；
- conjugate gradient 解 $(F+\lambda I)u=g$；
- diagonal/block/Kronecker/low-rank approximation；
- Hutchinson trace estimator 估计 trace，但需报告 probe 数和随机误差。

### 必做检查

1. 梯度是 log-likelihood、mean loss 还是 sum loss？缩放是否一致？
2. score 是否按独立单元定义？一个 user、sequence 还是 token？
3. empirical outer product 是否中心化？正则理论下均值为零，但错设/非最优时未必；
4. 矩阵是否对称化，最小特征值是否受数值误差影响？
5. 阻尼 $\lambda$ 是否主导了几何？
6. inverse 是显式逆、线性求解还是 pseudoinverse？容差是什么？
7. 信息估计的 Monte Carlo/mini-batch variance 多大？
8. observed Hessian 与 score outer product 相差多大？这可提示错设或有限样本问题；
9. 对标准误，是否需要 robust/cluster sandwich？
10. 对预测不确定性，parameter covariance 是否传播到真正 estimand？

## 二十二、一个贯通示例：Bernoulli 比例

令 $X_i\sim\operatorname{Bernoulli}(p)$，MLE 为

$$
\widehat p=\bar X.
$$

### 精确有限样本性质

$$
\mathbb E[\widehat p]=p,
\qquad
\operatorname{Var}(\widehat p)=\frac{p(1-p)}n.
$$

### Fisher 与 CRLB

$$
I_n(p)=\frac n{p(1-p)},
\qquad
\frac1{I_n(p)}=\frac{p(1-p)}n.
$$

所以 $\bar X$ 是无偏且有限样本达到 CRLB 的估计器。

### 渐近正态

对固定内点 $0<p<1$，

$$
\sqrt n(\widehat p-p)
\xrightarrow d
\mathcal N(0,p(1-p)).
$$

plug-in standard error 为

$$
\widehat{\rm se}(\widehat p)
=\sqrt{\frac{\widehat p(1-\widehat p)}n}.
$$

### 边界警告

若真实 $p$ 随 $n$ 逼近零，normal approximation 可很差；若样本中全是零，plug-in standard error 甚至给零。这正说明渐近公式的固定内点假设不能隐藏。

## 二十三、AI 研究中的五层翻译

看到“Fisher / curvature / uncertainty”时依次问：

1. **概率层**：完整的 $p_\theta(y\mid x)$ 或 $p_\theta(x)$ 是什么？
2. **抽样层**：哪些观测独立？输入是否随机？部署分布是什么？
3. **参数层**：哪些方向 identifiable？是否有 permutation/scale/gauge symmetry？
4. **计算层**：实际算的是 model Fisher、empirical Fisher、GGN 还是 Hessian？
5. **推断层**：要估计参数、函数、预测还是某个标量效应？所报 standard error 覆盖哪个随机性？

只有五层都对齐，inverse curvature 才可能被解释为 uncertainty；否则它最多是一个 optimizer preconditioner。

## 二十四、常见误区

### 误区 1：Fisher 信息是数据集本身携带的绝对信息

它依赖模型、参数点、观测单位和参数化。相同数据在不同模型下有不同 Fisher 信息。

### 误区 2：信息越大，参数一定越容易估

需目标可辨识、正则且尺度一致；矩阵病态意味着某些组合清楚、另一些组合模糊。

### 误区 3：inverse Hessian 就是 posterior covariance

只有在 Laplace approximation、合适 prior、mode 邻域、参数化与正则条件下才有近似关系；frequentist sandwich、Bayesian posterior 与 optimizer curvature 不是同一对象。

### 误区 4：CRLB 禁止任何估计器更准

经典版本约束无偏和正则估计器；有偏 shrinkage 可在 MSE 上改进，非正则模型可有不同速率。

### 误区 5：MLE 总是渐近有效

需要正确模型和 regularity；错设时 covariance 是 sandwich，边界/奇异模型甚至没有经典 Gaussian 极限。

### 误区 6：样本多就能忽略不可辨识

结构对称性不会被更多数据自动消除。更多数据只能识别分布决定的等价类。

### 误区 7：empirical Fisher 是 Fisher 的无害实现细节

它改变标签平均方式，远离 optimum 或模型错设时可与 model Fisher/Hessian 差异巨大。

## 二十五、推断审计模板

1. parameter/estimand 是什么，是否 identifiable？
2. 数据单元与依赖结构是什么？
3. 真值是否内点，support 是否固定？
4. score mean-zero 与 information identity 的交换条件是否合理？
5. $I(\theta)$ 是否有限且非奇异？
6. MLE 是否存在、局部唯一并一致？
7. 维数是否固定，$d/n$ 是否可忽略？
8. 模型正确还是只到 pseudo-true target？
9. 用 expected、observed、empirical Fisher 还是 GGN？
10. sum/mean loss 与 $n$ 的缩放是否一致？
11. standard error 用 inverse information 还是 robust sandwich？
12. nuisance parameter 是否通过 Schur complement 计入？
13. 线性求解、阻尼与低秩近似误差是否报告？
14. normal approximation 是否用 simulation/bootstrap/coverage 检查？
15. 结论是 pointwise、local、uniform 还是 finite-sample？

## 二十六、与后续章节的接口

- [[Bayesian 推断与后验预测]]：Fisher curvature 与 likelihood concentration 可帮助理解 Bernstein–von Mises/Laplace，但 posterior 还包含 prior 与完整不确定性；
- [[假设检验、置信区间与多重比较]]：Wald、score、likelihood-ratio 三条路线从这里取得标准化尺度；
- [[MCMC 与随机模拟诊断]]：非 Gaussian posterior 不能靠 inverse Hessian 代替，需采样与诊断；
- [[自然梯度、KL 局部几何与坐标不变性]]：把 Fisher 当局部 metric，而非仅作 standard-error 工具；
- [[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]与[[共轭梯度法]]：区分曲率对象、线性求解与可计算 preconditioner。

## 本章自检

- [ ] 能从 normalization 证明 score mean zero；
- [ ] 能推导 information identity，并说出交换条件；
- [ ] 能计算 Bernoulli 与 Gaussian Fisher 信息；
- [ ] 能证明 iid information additivity；
- [ ] 能解释重参数化与 KL 二阶几何；
- [ ] 能从 covariance Cauchy–Schwarz 推导 CRLB；
- [ ] 能处理有偏、向量与 nuisance parameter 版本；
- [ ] 能完整重建 MLE 渐近正态性的 Taylor–CLT–LLN–Slutsky 链；
- [ ] 能说出至少六项 regularity condition；
- [ ] 能区分 expected/observed/empirical Fisher 与 GGN；
- [ ] 能用 Uniform、boundary、mixture 或 neural symmetry 说明非正则失败；
- [ ] 能解释 misspecification 下 sandwich covariance。

## 练习与解答

- [[习题 - Fisher 信息、Cramér–Rao 界与渐近正态性]]
- [[解答 - Fisher 信息、Cramér–Rao 界与渐近正态性]]

## 参考文献与延伸

- MIT 18.655, Lecture 13：score、Fisher information、information inequality 与 Cramér–Rao bound；
- MIT 18.655, Lecture 17：M-estimator/MLE asymptotic normality 与 super-efficiency；
- Casella & Berger, *Statistical Inference*；
- A. W. van der Vaart, *Asymptotic Statistics*；
- Shun-ichi Amari, *Information Geometry and Its Applications*；
- James Martens, “New Insights and Perspectives on the Natural Gradient Method”。
