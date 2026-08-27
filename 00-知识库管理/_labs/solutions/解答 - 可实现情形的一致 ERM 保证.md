---
type: solution
status: draft
area: [learning-theory/pac, machine-learning/erm, classification]
topic: "[[可实现情形的一致 ERM 保证]]"
exercise: "[[习题 - 可实现情形的一致 ERM 保证]]"
prerequisites: ["[[PAC 学习定义与样本复杂度]]", "[[有限假设类、Union Bound 与一致收敛]]"]
related: ["[[不可知 PAC、ERM 与双侧一致收敛]]", "[[打散、增长与 VC 维]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - 可实现情形的一致 ERM 保证

> [!warning] 使用边界
> $1/\varepsilon$ rate 依赖 realizability、0–1 zero error、iid 与有限/可计数复杂度。删掉任何一项，都必须重新分析坏假设的生存事件。

## A. 识别与复述

### LT-REA-A01

realizability：存在 $h^*\in\mathcal H$ 使 $R_P(h^*)=0$。training consistency：$R_S(h_S)=0$。版本空间：

$$
V(S)=\{h\in\mathcal H:R_S(h)=0\}.
$$

$\varepsilon$-坏集：

$$
\mathcal H_{\rm bad}(\varepsilon)
=\{h\in\mathcal H:R_P(h)>\varepsilon\}.
$$

### LT-REA-A02

$R_P(h^*)=0$ 蕴含 $R_S(h^*)=0$ almost surely。0–1 empirical risk 非负，所以经验最小值为零；任何 exact ERM 都达到零，即 consistent。这里使用了 realizability、非负 loss，以及总体零风险推出样本上零 loss 的性质。

### LT-REA-A03

若 $|\mathcal H|=M$，任何 consistent learner 满足

$$
\Pr(R_P(h_S)>\varepsilon)
\le M(1-\varepsilon)^m
\le Me^{-m\varepsilon}.
$$

因此

$$
m\ge\frac{\log(M/\delta)}{\varepsilon}
$$

足够。证明控制的是版本空间中存在任何坏假设的事件，所以无论算法怎样在版本空间 tie-break 都被覆盖。

## B. 手算与构造

### LT-REA-B01

精确生存概率：

$$
(1-0.08)^{50}=0.92^{50}\approx0.01547.
$$

只使用 $p>\varepsilon=0.05$：

$$
0.95^{50}\approx0.07694.
$$

再指数化：

$$
e^{-50\cdot0.05}=e^{-2.5}\approx0.08208.
$$

依次变松，因为每一步丢掉信息：先把真实 $p=0.08$ 换成阈值 0.05，再把 $(1-\varepsilon)^m$ 换成指数上界。

### LT-REA-B02

simplified：

$$
m\ge\frac{\log(2000/0.05)}{0.03}
\approx353.221,
$$

取 $354$。exact：

$$
m\ge
\frac{\log40000}{-\log0.97}
\approx347.896,
$$

取 $348$。exact 版本节省 6 个样本；simplified 更保守。

### LT-REA-B03

当 $\varepsilon=0.05$，错误率 $0.12,0.30$ 的两个假设是坏存活者。条件于这个 $S$，均匀随机选择失败概率为 $2/5$。theorem 控制更强事件

$$
V(S)\cap\mathcal H_{\rm bad}=\varnothing,
$$

即版本空间根本没有坏假设；在该事件上所有 tie-breaking 都成功。

## C. 推导与证明

### LT-REA-C01

记 $p=R_P(h)$。对每个 iid 样本点，$h$ 不出错的概率为 $1-p$。事件 $R_S(h)=0$ 等于所有 $m$ 个点均不出错。独立性给乘法：

$$
\Pr(R_S(h)=0)
=\prod_{i=1}^m\Pr(h(X_i)=Y_i)
=(1-p)^m.
$$

若样本相关，联合零错概率一般不能分解成幂。

### LT-REA-C02

因为 $h_S\in V(S)$：

$$
\{R_P(h_S)>\varepsilon\}
\subseteq
\{\exists h\in\mathcal H_{\rm bad}:R_S(h)=0\}.
$$

于是

$$
\begin{aligned}
\Pr(R_P(h_S)>\varepsilon)
&\le\sum_{h\in\mathcal H_{\rm bad}}
\Pr(R_S(h)=0)\\
&=\sum_{h\in\mathcal H_{\rm bad}}(1-R_P(h))^m\\
&\le|\mathcal H_{\rm bad}|(1-\varepsilon)^m\\
&\le M(1-\varepsilon)^m\\
&\le Me^{-m\varepsilon}.
\end{aligned}
$$

最后一步由 $1-x\le e^{-x}$。

### LT-REA-C03

从

$$
M(1-\varepsilon)^m\le\delta
$$

取对数：

$$
\log M+m\log(1-\varepsilon)\le\log\delta.
$$

因 $\log(1-\varepsilon)<0$，整理得

$$
m\ge\frac{\log(M/\delta)}{-\log(1-\varepsilon)}.
$$

又有 $-\log(1-\varepsilon)\ge\varepsilon$，故

$$
\frac{1}{-\log(1-\varepsilon)}\le\frac1\varepsilon.
$$

所以用 $1/\varepsilon$ 的要求更大、更保守。Taylor 展开

$$
-\log(1-\varepsilon)
=\varepsilon+\varepsilon^2/2+O(\varepsilon^3)
$$

说明小 $\varepsilon$ 时两者一阶相同。

## D. 边界、反例与纠错

### LT-REA-D01

令 $X=x_0$ 恒定，$Y\sim\operatorname{Bernoulli}(0.1)$，$\mathcal H$ 含两个常数分类器。预测 0 的 risk 为 0.1，预测 1 的 risk 为 0.9，没有零 risk 函数。只要样本同时出现 0 和 1，两个常数函数都不能零训练错误，版本空间为空；该事件概率随 $m$ 增长趋于 1。

### LT-REA-D02

零训练错误只验证 consistency。仍需：

- class cardinality/complexity：实参数网络通常无限，不能代 $M$；
- population realizability：必须存在网络总体风险恰为零，而非仅能插值有限样本；
- iid：数据增强、用户聚类与序列 token 会引入依赖；
- optimizer output：需确认训练规则总返回协议中的 consistent hypothesis；
- train/deploy distribution 一致与 0–1 loss 也不能省略。

因此深网插值不单独推出 finite realizable theorem。

### LT-REA-D03

等式

$$
\Pr(R_S(h)=0)=(1-p)^m
$$

不再描述允许事件。正确事件是

$$
\Pr\left(
\frac1m\operatorname{Binomial}(m,p)\le\tau
\right).
$$

若 $p>\varepsilon>\tau$，可用 Chernoff/KL lower-tail bound，例如指数 $e^{-mD(\tau\|p)}$；若 $\tau$ 接近或超过 $p$，事件甚至不稀有。随后仍需对 class complexity 做控制。

## E. AI 迁移

### LT-REA-E01

医学规则库很难相信 realizable：reader disagreement/measurement error 产生标签噪声；缺失生物标志物造成 feature insufficiency；医院/人群变化造成 $P\to Q$；规则库不含正确决策边界造成 misspecification。只要任何一项使 $R_{\mathcal H}^*>0$，就应采用 agnostic comparator，并另外做 shift/robustness 分析；只有经领域证据支持的 deterministic noiseless protocol 才适合 realizable 基准。

### LT-REA-E02

需要：预先固定且有限的 prompt 函数库；iid 对话样本；固定 0–1 judge；库中存在 population 零错 prompt；选择器总返回零训练错 prompt；训练与部署同分布。自然语言 ambiguity 使同类输入可能有多个合理/冲突标签，通常破坏 population realizability，也可能使 judge 本身随机，因此版本空间会空或零错只是偶然插值。

### LT-REA-E03

原上界

$$
m\ge\frac{\log(M/\delta)}{\varepsilon}.
$$

$M$ 扩大十倍只增加

$$
\frac{\log10}{\varepsilon}
$$

个样本；$\varepsilon$ 减半则把整个上界乘 2。选择自由度以对数收费，精度以倒数收费：有限类中大幅增加候选相对便宜，但追求更低错误阈值会线性增加样本需求。
