---
type: solution
status: draft
area: [learning-theory/pac, probability/union-bound]
topic: "[[有限假设类、Union Bound 与一致收敛]]"
exercise: "[[习题 - 有限假设类、Union Bound 与一致收敛]]"
prerequisites: ["[[泛化间隙与浓缩不等式接口]]", "[[浓缩不等式]]"]
related: ["[[不可知 PAC、ERM 与双侧一致收敛]]", "[[Occam 界、编码长度与先验权重]]"]
sources: ["[[S-1963-Hoeffding-Bounded-Random-Variables]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - 有限假设类、Union Bound 与一致收敛

> [!warning] 使用边界
> 简单 $\log M$ 结论要求候选类对评价样本预先固定。观察到一个很小的 data-dependent candidate set，不能倒推选择自由度很小。

## A. 识别与复述

### LT-FIN-A01

uniform event 为

$$
G_\varepsilon
=\left\{S:\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|\le\varepsilon\right\}.
$$

若 $|\mathcal H|=M$、loss 在 $[0,1]$、样本 iid：

$$
\Pr(G_\varepsilon^c)
\le2Me^{-2m\varepsilon^2}.
$$

### LT-FIN-A02

逐个样本结果 $\omega$ 上都有

$$
\mathbf1\left\{\bigcup_jB_j\right\}(\omega)
\le\sum_j\mathbf1\{B_j\}(\omega).
$$

取期望：

$$
\Pr(\cup_jB_j)
\le\sum_j\Pr(B_j).
$$

没有任何乘法分解，所以不要求事件独立。

### LT-FIN-A03

pointwise：对每个固定 $h$，$|R_S(h)-R_P(h)|\to0$。uniform：最大偏差

$$
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|\to0.
$$

学习器可随 $S$ 挑出偏差最大的函数；uniform event 覆盖这种选择。若不用 uniform convergence，就需 stability、compression、PAC-Bayes 等直接限制算法的数据依赖。

## B. 手算与构造

### LT-FIN-B01

$$
\alpha
=\sqrt{\frac{\log(2M/\delta)}{2m}}
=\sqrt{\frac{\log(200000)}{16000}}
\approx0.02762.
$$

### LT-FIN-B02

$$
m\ge
\frac{\log(2\cdot10^4/0.01)}{2(0.04)^2}
=\frac{\log(2,000,000)}{0.0032}
\approx4533.956.
$$

取 $m=4534$。

### LT-FIN-B03

4 组重复对每组只贡献一个函数，共 4 个；其余 4 个不同函数再贡献 4 个，因此 $M=8$。误用 $M=12$ 会把 $\log(2M/\delta)$ 增大，得到更大的半径；保证仍保守有效，但没有利用函数重复。

## C. 推导与证明

### LT-FIN-C01

令

$$
B_h=\{|R_S(h)-R_P(h)|>\varepsilon\}.
$$

则

$$
\left\{\sup_h|R_S(h)-R_P(h)|>\varepsilon\right\}
=\bigcup_{h\in\mathcal H}B_h.
$$

所以

$$
\begin{aligned}
\Pr\left(\sup_h|R_S-R_P|>\varepsilon\right)
&\le\sum_{h\in\mathcal H}\Pr(B_h)\\
&\le\sum_{h\in\mathcal H}2e^{-2m\varepsilon^2}\\
&=2Me^{-2m\varepsilon^2}.
\end{aligned}
$$

第一步是事件等价，第二步是 Union Bound，第三步对预先固定的每个 $h$ 使用 Hoeffding。

### LT-FIN-C02

在 uniform event 上，设 $h^*_{\mathcal H}$ 是 class minimizer：

$$
\begin{aligned}
R_P(\widetilde h)
&\le R_S(\widetilde h)+\alpha\\
&\le R_S(h^*_{\mathcal H})+\rho+\alpha\\
&\le R_P(h^*_{\mathcal H})+2\alpha+\rho.
\end{aligned}
$$

故 class excess 至多 $2\alpha+\rho$。exact ERM 时 $\rho=0$，要使 excess $\le\varepsilon$，令 $\alpha=\varepsilon/2$。充分样本量：

$$
m\ge
\frac{\log(2M/\delta)}{2(\varepsilon/2)^2}
=\frac{2\log(2M/\delta)}{\varepsilon^2}.
$$

### LT-FIN-C03

对固定 $h_j$，以失败预算 $\delta_j$ 反解 Hoeffding：

$$
\Pr\left(
|R_S(h_j)-R_P(h_j)|>
\sqrt{\frac{\log(2/\delta_j)}{2m}}
\right)
\le\delta_j.
$$

对所有 $j$ 的失败事件 Union Bound：

$$
\Pr(\exists j:\text{第 }j\text{ 个界失败})
\le\sum_j\delta_j\le\delta.
$$

若令 $\delta_j=\delta\pi_j$，其中 $\sum_j\pi_j\le1$，半径含

$$
\log\frac{2}{\delta\pi_j}
=\log\frac2\delta+\log\frac1{\pi_j}.
$$

$-\log\pi_j$ 就像假设的非均匀描述长度，预告 Occam/prior-weighted bound。

## D. 边界、反例与纠错

### LT-FIN-D01

若模型在观察 validation 前预先指定，确实是 $M=1$ 的一次查询。若先比较 $M$ 个候选再发布最高分者，最终输出依赖 validation；选择事件可能利用任何候选的偶然偏差，必须控制整个搜索 family。发布数量为 1 不会抹掉选择历史。

### LT-FIN-D02

使用 LT-CON-D01 的记忆器：观察 $S$ 后构造唯一候选

$$
\mathcal H_S=\{h_{T_S}\},
$$

其中 $h_{T_S}$ 在训练点预测正确、其他点全错。虽 $|\mathcal H_S|=1$，却有 $R_S=0,R_P=1$。fixed-class theorem 要求候选在抽样前固定；这里唯一候选已经编码全部 $S$。

### LT-FIN-D03

$p$ 个实参数的 parameter set 通常与 $\mathbb R^p$ 同样不可数，函数 class 也可能无限；$M=p$ 没有依据。不同参数还可能因 permutation/rescaling 表示同一函数。若每个参数量化为有限 bits，可得到有限 $M$，但需同时证明量化函数接近原函数，并把产生的 approximation error 加入风险账本。

## E. AI 迁移

### LT-FIN-E01

在查看 validation 前冻结 100 个 checkpoint、preprocessing、decoding、loss 与 sampling unit。对每个模型报告共同半径

$$
\sqrt{\frac{\log(200/\delta)}{2m_{\rm val}}}.
$$

在共同覆盖事件内，可按 validation risk 选择任一个模型。选择完成后冻结所有决定，只用一次从未参与选择的 independent test 对最终模型做 pointwise interval；test 不再承担调参。

### LT-FIN-E02

最保守 family size 是

$$
M=20\times15\times4=1200.
$$

不同任务、指标和模型的统计量可能高度相关，但 Union Bound 不要求独立，所以仍有效。相关性意味着许多坏事件重叠，直接相加可能明显过松；更细方法可利用 covariance、hierarchy 或预先指定 primary endpoints。

### LT-FIN-E03

新 prompt 由 validation feedback 生成，候选 family 是 adaptive、data-dependent 的，事先没有固定有限 $M$。可恢复保证的设计包括：

1. 用一份数据生成 prompts，另一份独立 validation 只做一次固定集合选择；
2. 预先设置有限 rounds 与每轮候选上限，对完整 transcript/family 分配失败预算；
3. 使用 reusable holdout、differential privacy 或 adaptive data analysis 机制限制反馈信息；
4. 最终保留全新独立 test，只在所有搜索结束后开启一次。
