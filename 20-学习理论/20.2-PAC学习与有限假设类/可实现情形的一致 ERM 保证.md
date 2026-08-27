---
type: concept
status: draft
area: [learning-theory/pac, machine-learning/erm, classification]
aliases: [Realizable PAC Bound, Consistent ERM Guarantee, Version Space Bound]
node_id: LT-12
prerequisites: ["[[PAC 学习定义与样本复杂度]]", "[[有限假设类、Union Bound 与一致收敛]]", "[[可实现、不可知、相合性与可学习性]]", "[[经验风险最小化、近似 ERM 与超额风险分解]]"]
related: ["[[不可知 PAC、ERM 与双侧一致收敛]]", "[[打散、增长与 VC 维]]", "[[Occam 界、编码长度与先验权重]]", "[[在线学习协议、Regret 与 Comparator]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]"]
exercises: ["[[习题 - 可实现情形的一致 ERM 保证]]"]
solutions: ["[[解答 - 可实现情形的一致 ERM 保证]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 可实现情形的一致 ERM 保证

> [!abstract] 本章主问题
> 在有限二分类假设类 $\mathcal H$、0–1 loss、iid 样本与 realizability 下，任何返回零训练误差假设的一致学习器都满足
> $$
> \Pr(R_P(h_S)>\varepsilon)\le|\mathcal H|e^{-m\varepsilon}.
> $$
> 因而 $m\ge\log(|\mathcal H|/\delta)/\varepsilon$ 足以 PAC 学习。其 $1/\varepsilon$ 而非 $1/\varepsilon^2$ 的关键不是更强的 Hoeffding 常数，而是：真实错误率超过 $\varepsilon$ 的坏假设若想留在版本空间，必须连续 $m$ 次都避开自己的错误区域。

> [!question] 初学者读完必须能回答
> 1. Realizability、consistent learner 与 ERM 之间是什么逻辑关系？
> 2. 固定坏假设留在版本空间的精确概率为什么是 $(1-R_P(h))^m$？
> 3. 怎样从生存概率与 Union Bound 得到 $M e^{-m\varepsilon}$？
> 4. $1/\varepsilon$ 样本率来自什么特殊事件，而不是哪个 Hoeffding 常数？
> 5. 标签噪声、近似一致、无限类和“零训练误差”分别破坏或遗漏什么？

先用下图回答一个视觉问题：**可实现条件下，为什么风险超过 $\varepsilon$ 的坏假设会以 $e^{-m\varepsilon}$ 的速度从版本空间消失？**

![[00-知识库管理/_assets/figures/learning-theory/fig-realizable-version-space-survival-v2.svg|880]]

> [!figure] 图 20.2.4｜可实现情形的版本空间与坏假设生存
> A 展示版本空间随样本约束收缩而真实零风险假设始终保留；B 把固定坏假设的错误区域质量写成 $R_P(h)>\varepsilon$，其零错生存要求全部 $m$ 个样本避开该区域；C 对坏假设求并集并反解 $m\gtrsim(\log M+\log(1/\delta))/\varepsilon$。来源：独立绘制；理论接口参考 finite realizable PAC bound；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先确认 realizability 使版本空间非空，学习器只需从其中返回任意元素；B 对一个固定坏 $h$ 计算连续避开错误区域的概率；C 再把“输出很坏”包含在“至少一个坏 $h$ 幸存”的并集中。注意这里估计的不是两个接近均值，而是一个零错生存事件。

**适用边界（图没有证明什么）。** 图只覆盖有限二分类类、0–1 loss、iid 样本、严格 realizability 与一致输出；深网训练集插值不等于总体 realizability。标签噪声、approximate ERM、无限类、数据依赖类或非独立样本都需要修改事件和复杂度；图也不保证找到一致假设在计算上容易。

## 一、学习目标

1. 定义 realizable binary classification 与 consistent learner；
2. 证明 realizability 下 ERM 必为 consistent；
3. 计算固定坏假设在样本上零错的精确概率；
4. 推导 $Me^{-m\varepsilon}$ failure bound；
5. 反解 exact 与简化样本复杂度；
6. 解释保证为何覆盖任意 tie-breaking 的一致学习器；
7. 比较 $1/\varepsilon$ 与 uniform-convergence 的 $1/\varepsilon^2$；
8. 识别 label noise、approximate consistency 与 infinite class 的断点；
9. 用版本空间理解证明；
10. 把 theorem 翻译到有限规则、prompt 或离散模型选择场景。

## 二、设置与全部假设

令

$$
\mathcal Y=\{0,1\},
\qquad
\ell(h,(x,y))=\mathbf1\{h(x)\ne y\}.
$$

有限假设类

$$
\mathcal H=\{h_1,\ldots,h_M\},
\qquad M<\infty.
$$

样本

$$
S=((X_1,Y_1),\ldots,(X_m,Y_m))\sim P^m.
$$

总体错误率与训练错误率为

$$
R_P(h)=\Pr_{(X,Y)\sim P}(h(X)\ne Y),
$$

$$
R_S(h)=\frac1m\sum_{i=1}^m\mathbf1\{h(X_i)\ne Y_i\}.
$$

### 2.1 realizability

假设存在 $h^*\in\mathcal H$ 使

$$
R_P(h^*)=0.
$$

这意味着在 $P$-几乎处处意义下，$h^*(X)=Y$。因此对 iid 样本：

$$
R_S(h^*)=0
$$

以概率 $1$ 成立。

### 2.2 consistent learner

若学习算法对每个 realizable sample 返回某个

$$
h_S\in\mathcal H
$$

且满足

$$
R_S(h_S)=0,
$$

则称它与样本一致。

> [!note] “一致”有两个常见含义
> 本节 consistent 指 training consistency：零经验错误。统计学中 consistency 也常指 $m\to\infty$ 时 risk 收敛。上下文不同，不能混用。

## 三、为什么任意 ERM 都一致

realizability 保证存在 $h^*$ 且

$$
R_S(h^*)=0.
$$

0–1 经验风险非负，因此

$$
\inf_{h\in\mathcal H}R_S(h)=0.
$$

任何 exact ERM 输出 $\widehat h_S$ 都满足

$$
R_S(\widehat h_S)=0.
$$

所以在本节条件下：

$$
\text{ERM}\Longrightarrow\text{consistent}.
$$

但证明最终只使用输出零训练错误，并不使用它如何在所有零错假设中 tie-break。因此定理实际上覆盖所有 consistent learners。

## 四、版本空间

定义样本 $S$ 的版本空间

$$
V(S)
=\{h\in\mathcal H:R_S(h)=0\}.
$$

realizability 确保

$$
h^*\in V(S),
$$

所以版本空间非空。consistent learner 就是在 $V(S)$ 中选任意一个元素。

定义 $\varepsilon$-坏假设集合

$$
\mathcal H_{\rm bad}(\varepsilon)
=\{h\in\mathcal H:R_P(h)>\varepsilon\}.
$$

学习失败事件是

$$
\{R_P(h_S)>\varepsilon\}.
$$

只要版本空间中没有坏假设，任意一致输出都一定是好假设。因此

$$
\{R_P(h_S)>\varepsilon\}
\subseteq
\{V(S)\cap\mathcal H_{\rm bad}(\varepsilon)\ne\varnothing\}.
$$

这一步把对未知 tie-breaking 的分析，转成“是否还有坏假设存活”。

## 五、固定坏假设的生存概率

固定 $h\in\mathcal H$，记

$$
p=R_P(h).
$$

单个样本点上，$h$ 预测正确的概率是

$$
1-p.
$$

因为 $m$ 个样本 iid，$h$ 在全部样本上零错误的概率为

$$
\boxed{
\Pr(R_S(h)=0)=(1-p)^m.
}
$$

若 $h$ 是 $\varepsilon$-坏假设，即 $p>\varepsilon$，则

$$
(1-p)^m<(1-\varepsilon)^m.
$$

再用基本不等式

$$
1-x\le e^{-x}
\qquad(x\ge0),
$$

得到

$$
\boxed{
\Pr(R_S(h)=0)
\le(1-\varepsilon)^m
\le e^{-m\varepsilon}.
}
$$

### 5.1 直觉

坏假设有一个概率质量至少 $\varepsilon$ 的错误区域。每次独立抽样都有至少 $\varepsilon$ 概率击中该区域；要让它伪装成零训练错误，就必须连续 $m$ 次都避开错误区域，其概率指数衰减。

## 六、对所有坏假设做 Union Bound

失败蕴含至少一个坏假设仍一致：

$$
\begin{aligned}
\Pr(R_P(h_S)>\varepsilon)
&\le
\Pr\left(
\exists h\in\mathcal H_{\rm bad}(\varepsilon):R_S(h)=0
\right)\\
&\le
\sum_{h\in\mathcal H_{\rm bad}(\varepsilon)}
\Pr(R_S(h)=0)\\
&\le
|\mathcal H_{\rm bad}(\varepsilon)|(1-\varepsilon)^m\\
&\le
M(1-\varepsilon)^m\\
&\le
Me^{-m\varepsilon}.
\end{aligned}
$$

因此得到核心定理：

$$
\boxed{
\Pr_{S\sim P^m}
\left(R_P(h_S)>\varepsilon\right)
\le |\mathcal H|e^{-m\varepsilon}.
}
$$

若算法还有随机 tie-breaking $U$，只要它总在 $V(S)$ 中选择，上述 event inclusion 对每个 $U$ 都成立，所以 joint probability $\Pr_{S,U}$ 仍服从同一界。

## 七、反解样本复杂度

希望失败概率不超过 $\delta$，令

$$
Me^{-m\varepsilon}\le\delta.
$$

取对数：

$$
\log M-m\varepsilon\le\log\delta.
$$

整理：

$$
m\varepsilon
\ge\log M+\log\frac1\delta
=\log\frac M\delta.
$$

所以充分条件是

$$
\boxed{
m\ge
\frac{\log(|\mathcal H|/\delta)}{\varepsilon}.
}
$$

取整数可写为

$$
\boxed{
m_{\mathcal H}(\varepsilon,\delta)
\le
\left\lceil
\frac{\log(|\mathcal H|/\delta)}{\varepsilon}
\right\rceil.
}
$$

这正证明任何有限二分类假设类在 realizable setting 下可由 consistent learner PAC 学习。

## 八、保留 $(1-\varepsilon)^m$ 的更精确版本

若不用 $1-\varepsilon\le e^{-\varepsilon}$，要求

$$
M(1-\varepsilon)^m\le\delta.
$$

取对数得

$$
m\log(1-\varepsilon)
\le\log(\delta/M).
$$

由于 $\log(1-\varepsilon)<0$，除法时要反向：

$$
\boxed{
m\ge
\frac{\log(M/\delta)}{-\log(1-\varepsilon)}.
}
$$

又因为

$$
-\log(1-\varepsilon)\ge\varepsilon,
$$

所以简化式 $\log(M/\delta)/\varepsilon$ 更保守但更易读。

当 $\varepsilon$ 很小时：

$$
-\log(1-\varepsilon)
=\varepsilon+\frac{\varepsilon^2}{2}+O(\varepsilon^3),
$$

两者一阶相同。

## 九、为什么是 $1/\varepsilon$，不是 $1/\varepsilon^2$

LT-11 的双侧均值估计需要区分相差 $\varepsilon$ 的两个 risk，Hoeffding exponent 是

$$
e^{-cm\varepsilon^2}.
$$

本节不估计每个 risk 到 $\pm\varepsilon$。它只问：一个 risk 大于 $\varepsilon$ 的函数，能否在训练集上保持**恰好零错**？对应概率是

$$
(1-p)^m\le e^{-m\varepsilon}.
$$

所以 exponent 对 $\varepsilon$ 是一次而非二次。

> [!important] 没有违反统计下界
> $1/\varepsilon$ 快率使用了 realizability 与 exact zero empirical error。不可知噪声下，通常需要比较两个非零且接近的期望，$1/\varepsilon^2$ 会重新出现。

## 十、为什么定理覆盖“任何一致学习器”

证明没有使用算法偏好哪个零错假设，只使用

$$
h_S\in V(S).
$$

坏输出只能发生在

$$
V(S)\cap\mathcal H_{\rm bad}\ne\varnothing
$$

时。我们的 Union Bound 控制的是“版本空间里存在任何坏假设”的更强事件。因此：

- lexicographic tie-breaking 有保证；
- 随机 tie-breaking 有保证；
- 选择最短描述的 consistent hypothesis 有保证；
- 甚至 adversarially 在版本空间中挑最坏元素，也仍被覆盖。

这叫作 **all consistent hypotheses are good** 的证明策略。

## 十一、ERM 与 consistent learner 的逻辑关系

在 realizable 0–1 setting：

$$
\text{exact ERM}\Rightarrow\text{consistent}.
$$

但反向不必成立于一般 loss/非 realizable setting。即便在本节，所有 consistent hypotheses 都是 empirical minimizers，因为最小训练错误为零；于是两者集合恰好一致。

如果算法只是 $\rho$-approximate ERM 且 $\rho>0$，它可能容许若干训练错误，不能直接套“零错生存”事件。

## 十二、realizability 到底有多强

$R_P(h^*)=0$ 要求：

1. class 中存在正确标注规则；
2. 标签在给定输入下几乎处处无冲突；
3. train 与 target population 使用同一 $P$；
4. loss 确实是 0–1 exact correctness；
5. 数据没有会使同一 $x$ 出现互相矛盾标签的不可约噪声。

现实数据常不满足这些条件。因此 realizable theorem 更像“结构最清楚的基准定理”，而非所有系统的直接认证。

### 12.1 nearly realizable 不能直接假装 realizable

若只知存在 $h^*$ 使

$$
R_P(h^*)=\eta>0,
$$

则 $R_S(h^*)$ 通常不为零，版本空间甚至可能为空。必须转向 agnostic ERM、noise conditions 或 tolerant learning。

## 十三、若允许训练错误，会发生什么

假设输出只满足

$$
R_S(h_S)\le\tau
$$

而非零。对固定坏 $h$，事件变成 Binomial lower tail：

$$
\Pr\left(
\frac1m\operatorname{Binomial}(m,p)\le\tau
\right).
$$

当 $p>\varepsilon>\tau$ 时，可用 Chernoff/KL tail 控制，指数大致为

$$
e^{-mD(\tau\|p)}.
$$

这仍可能给快率，但依赖 $\tau$ 与 $p$ 的间隔；不能继续写 $(1-p)^m$。

## 十四、一个完整数值例子

设

$$
M=1000,
\qquad
\varepsilon=0.05,
\qquad
\delta=0.01.
$$

简化充分样本量为

$$
m\ge
\frac{\log(1000/0.01)}{0.05}
=\frac{\log(100000)}{0.05}
\approx230.3.
$$

所以取 $m=231$ 足够保证：对任意 realizable 分布，任何 consistent learner 以至少 $99\%$ 概率输出错误率至多 $5\%$ 的假设。

注意保证不是：

- 每个输出都必然小于 $5\%$；
- 每个单点以 $99\%$ 概率预测正确；
- 训练 231 个 gradient steps；
- 在任何 distribution shift 下仍成立。

## 十五、版本空间收缩的几何直觉

初始版本空间为 $V_0=\mathcal H$。观察第 $i$ 个样本后：

$$
V_i
=\{h\in V_{i-1}:h(X_i)=Y_i\}.
$$

每个样本删除与该观测矛盾的假设。一个错误质量为 $p$ 的假设每一步以概率 $p$ 被删除，所以存活 $m$ 步概率为 $(1-p)^m$。

该视角连接：

- candidate elimination；
- online mistake bounds；
- active learning 中主动选择最能切分版本空间的 query；
- Bayesian posterior 中不一致假设获得零 likelihood 的 noiseless 极限。

## 十六、无限类为什么不能直接令 $M=\infty$

若 $|\mathcal H|=\infty$，表达式

$$
|\mathcal H|e^{-m\varepsilon}
$$

没有信息。后续方法会替换“全局函数数量”：

- VC 维：只数有限样本上能产生多少 labelings；
- covering number：数精度 $\gamma$ 下需要多少代表；
- Occam/PAC-Bayes：按描述长度或 prior mass 分配失败预算；
- compression：按输出依赖的少数样本计数。

有限类 proof skeleton 仍然保留：控制一个坏对象的生存概率，再控制可能生存的对象数量/复杂度。

## 十七、AI 应用中的可用与不可用

### 17.1 有限规则库

从预先给定的有限分类规则库中寻找一个完全拟合 noiseless labels 的规则，本定理可直接应用，$M$ 是不同规则函数数。

### 17.2 离散 prompt 库

若任务确实可由某个固定 prompt 实现零 population error，且从 $M$ 个固定 prompt 中选择零训练错误者，数学结构匹配。但真实自然语言任务通常存在标注噪声与 irreducible ambiguity，realizability 往往不可信。

### 17.3 神经网络插值

训练误差为零不等于 realizability 假设已经满足：

- theorem 还要求有限/受控 class；
- 需要存在 population error 为零的 class member；
- optimizer 输出零错只是 consistency，不证明 class 中不存在大量坏的零错网络。

因此“深网插值”不能单独推出本节 bound 很紧。科学空间对深度泛化机制的讨论正提醒我们还需要 implicit bias、margin、norm、compression 或 data geometry。

## 十八、常见误解

> [!failure] “零训练错误就意味着零总体错误”
> 错。定理只说在样本足够大时，所有坏的一致假设同时存活的概率小。

> [!failure] “证明只适用于某个指定 ERM tie-breaker”
> 错。它控制所有 consistent hypotheses 都好的共同事件。

> [!failure] “$1/\varepsilon$ 总比 $1/\varepsilon^2$ 好，所以应永远使用 realizable bound”
> 错。更快 rate 是用更强且常不成立的假设换来的。

> [!failure] “标签有少量噪声，可以把它忽略”
> 错。任意正噪声都可能让版本空间为空，并破坏零错概率计算。

> [!failure] “$M$ 是网络参数数量”
> 错。$M$ 是候选函数数；连续参数 class 通常无限。

## 十九、证明模板

1. 写清 binary 0–1、finite class、iid 与 realizability；
2. 由 $h^*$ 得经验最优值为零；
3. 说明算法输出在版本空间中；
4. 定义 $\varepsilon$-bad set；
5. 对固定坏 $h$ 计算 $(1-R_P(h))^m$；
6. 用 $R_P(h)>\varepsilon$ 和 $1-x\le e^{-x}$；
7. 对所有坏假设 Union Bound；
8. 把 bad-output event 包含进 bad-survivor event；
9. 令 $Me^{-m\varepsilon}\le\delta$ 并反解；
10. 检查没有把 noise、approximate ERM 或 infinite class 偷带进来。

## 二十、本节边界与来源说明

- 现代 finite realizable class 样本复杂度与证明以标准学习理论教材为准；
- Valiant 论文用于 PAC 历史与“有效可学习”的思想起点，不宣称本节符号是原文逐字复刻；
- 深度网络的插值现象需要额外结构，本节不把 finite-class theorem 外推成深度泛化解释。

## 二十一、掌握检查

- [ ] 我能定义版本空间与 $\varepsilon$-坏假设集；
- [ ] 我能推导固定坏假设零错概率 $(1-p)^m$；
- [ ] 我能证明 $\Pr(R_P(h_S)>\varepsilon)\le Me^{-m\varepsilon}$；
- [ ] 我能反解 exact 与 simplified sample size；
- [ ] 我能解释 theorem 为何覆盖任何 consistent learner；
- [ ] 我能解释 $1/\varepsilon$ rate 的结构来源；
- [ ] 我能指出 label noise 与 approximate consistency 的断点；
- [ ] 我能说明 infinite class 需要什么替代复杂度。

## 二十二、进一步连接

- [[不可知 PAC、ERM 与双侧一致收敛]]：去掉 realizability，使用 uniform estimation 比较非零 risks；
- 版本空间与候选消除：把一致学习写成逐样本删除过程；
- [[打散、增长与 VC 维]]：把有限类证明推广到无限二分类类；
- [[Occam 界、编码长度与先验权重]]：用不同 code length 替代统一的 $\log M$。
