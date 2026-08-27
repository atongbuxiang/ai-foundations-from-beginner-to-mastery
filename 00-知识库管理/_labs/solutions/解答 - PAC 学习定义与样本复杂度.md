---
type: solution
status: draft
area: [learning-theory/pac, machine-learning/foundations]
topic: "[[PAC 学习定义与样本复杂度]]"
exercise: "[[习题 - PAC 学习定义与样本复杂度]]"
prerequisites: ["[[可实现、不可知、相合性与可学习性]]", "[[命题、量词与逻辑等价]]"]
related: ["[[可实现情形的一致 ERM 保证]]", "[[渐近记号、增长率与复杂度]]"]
sources: ["[[S-1984-Valiant-Theory-of-the-Learnable]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - PAC 学习定义与样本复杂度

> [!warning] 使用边界
> PAC 是协议内的 class-level finite-sample 合同。任何答案都必须说明 distribution family、comparator、loss、sampling 和概率来源。

## A. 识别与复述

### LT-PAC-A01

realizable binary PAC：存在 $A,m_{\mathcal H}$，使对任意 $\varepsilon,\delta\in(0,1)$、任意满足 $\inf_{h\in\mathcal H}R_P(h)=0$ 的 $P$，当 $m\ge m_{\mathcal H}(\varepsilon,\delta)$ 时：

$$
\Pr_{S,U}(R_P(A(S,U))\le\varepsilon)\ge1-\delta.
$$

agnostic PAC：对任意允许 $P$：

$$
\Pr_{S,U}\left(R_P(A(S,U))\le\inf_{h\in\mathcal H}R_P(h)+\varepsilon\right)\ge1-\delta.
$$

前者 comparator risk 因 realizability 为零；后者比较一般的类内最优 risk。

### LT-PAC-A02

$\varepsilon$ 是允许的 risk/excess-risk 误差；$\delta$ 是随机训练运行违反该质量阈值的概率上界；$m$ 是达到二者所需的 sampling units 数。单点分类错误由 $R_P$ 描述；校准 confidence 是预测概率与条件频率的关系，均不同于“算法因抽到坏训练集而失败”的 $\delta$。

### LT-PAC-A03

- 单次输出成功：一个观察到的 event；
- 算法 PAC：同一 $A$ 对所有协议内 $P,\varepsilon,\delta$ 满足合同；
- class learnable：存在至少一个 PAC 算法；
- efficiently learnable：除 sample complexity 外，表示、运行时间与内存也按相关参数多项式增长。

## B. 手算与构造

### LT-PAC-B01

$$
\begin{aligned}
m&=\left\lceil
\frac{3\log40+5\cdot20}{0.1^2}
\right\rceil\\
&=\lceil11106.664\ldots\rceil=11107.
\end{aligned}
$$

这是 theorem 给出的 explicit sufficient upper bound；除非另有 lower bound，不能称为最小或最优样本复杂度。

### LT-PAC-B02

好事件上 $\mathcal E\le0.03$，坏事件上最多 1，因此

$$
\mathbb E\mathcal E
\le0.03(0.98)+1(0.02)=0.0494.
$$

反向由 Markov：

$$
\Pr(\mathcal E>0.01)
\le\frac{10^{-4}}{10^{-2}}=0.01.
$$

### LT-PAC-B03

当 $\varepsilon=0.1$，只有错误率 1 的输出失败，概率为 $0.01$。对 $\delta=0.02$，$0.01\le0.02$，满足 event；对 $\delta=0.005$，$0.01>0.005$，不满足。增加样本在这个人为算法中不会减少内部失败概率，因此它不能满足任意小 $\delta$ 的完整 PAC 定义。

## C. 推导与证明

### LT-PAC-C01

agnostic 定义骨架：

$$
\exists A,\exists m_{\mathcal H},
\forall\varepsilon,\delta,
\forall P,
\forall m\ge m_{\mathcal H}(\varepsilon,\delta):
\Pr_{S,U}(R_P(A(S,U))-R_{\mathcal H}^*\le\varepsilon)
\ge1-\delta.
$$

若交换为 $\forall P\exists A_P$，算法可以预先知道 $P$ 并直接输出

$$
h_P\in\arg\min_{h\in\mathcal H}R_P(h),
$$

甚至不看数据。这只说明每个分布有一个 oracle，不说明一个未知分布下可运行的统一学习规则。

### LT-PAC-C02

对 $k=1,2,\ldots$ 取 $\varepsilon_k=\delta_k=1/k$，令

$$
n_k=\max_{j\le k}m_{\mathcal H}(1/j,1/j)
$$

并使 $n_k$ 严格递增。对 $n_k\le m<n_{k+1}$ 使用参数 $1/k$，则

$$
\Pr(\mathcal E_m>1/k)\le1/k.
$$

随着 $m\to\infty$，$k\to\infty$，故 $\mathcal E_m\to0$ in probability。反之，仅知依概率收敛只说对每个固定 $\varepsilon,\delta$ 终究存在某阈值；若没有 rate，就不知道阈值怎样依赖参数，也无法做资源规划。

### LT-PAC-C03

构造 $A'$：当收到 $m\ge m_0$ 个样本，只把前 $m_0$ 个交给已保证的 $A$，忽略其余样本。前 $m_0$ 个仍是 $P^{m_0}$，因此成功概率不变。这证明**存在**一个阈值以上保持保证的算法。

若原算法 $A_m$ 会随输入长度改变输出，它可能在 $m_0$ 时良好、在更大 $m$ 时故意输出坏函数，所以“更多数据自动更好”不是任意算法的逻辑定理。

## D. 边界、反例与纠错

### LT-PAC-D01

distribution-free 仍固定：假设类 $\mathcal H$、loss、输入输出空间、iid sampling、train/target 同分布、realizability 或 bounded-loss 条件、可测性、comparator 以及算法可访问的信息。它只表示 theorem 对这个协议允许的所有 $P$ 统一成立，不表示 assumption-free。

### LT-PAC-D02

令 class 由 $d$ bit 描述的 $2^d$ 个候选组成。有限类结果只需 $O((d+\log(1/\delta))/\varepsilon^q)$ 个样本，但逐一计算 empirical risk 的朴素 ERM 要 $2^d$ 次评估。这个例子说明 sample bound 不等于 runtime bound；若要证明没有更快算法，还需计算复杂性假设或 reduction，不能仅凭枚举慢下结论。

### LT-PAC-D03

单次 $98\%$ 缺少：预先指定的 class/algorithm、population distribution family、iid 协议、loss 与 comparator、训练随机性概率、$\varepsilon$ 与 $\delta$ 的区分、跨所有 $P$ 的统一性、样本复杂度函数、benchmark selection correction、独立 test coverage 以及 distribution shift 条件。accuracy 数值本身不是 confidence，也不是 class learnability theorem。

## E. AI 迁移

### LT-PAC-E01

realizable 合同：假设固定 prompt 库 $\mathcal H$ 中存在一个在客服分布 $P$ 上零 0–1 policy violation 的 prompt，要求

$$
\Pr(R_P(A(S))\le\varepsilon)\ge1-\delta.
$$

agnostic 合同不作零风险假设，要求

$$
\Pr(R_P(A(S))\le\min_{h\in\mathcal H}R_P(h)+\varepsilon)\ge1-\delta.
$$

真实客服有歧义、judge noise、不可观测信息与长尾请求，agnostic 合同通常更可信。两者都要求 prompt 库和评价 protocol 在抽样前固定。

### LT-PAC-E02

预训练数据决定 representation，若与 downstream sample/test 重叠会破坏独立性。冻结后的表示与线性 head class 共同定义下游 $\mathcal H$；下游训练集是 $S\sim P^m$；loss/comparator 定义 PAC target；测试分布必须与声称中的 $P$ 一致。若 representation 也用 downstream $S$ 调整，则不能只分析一个预先固定的线性类，需把表示学习算法一起纳入输出或做 sample splitting。

### LT-PAC-E03

仅有 $R_P(h)$ 小，$R_Q(h)$ 可任意大：令 $P$ 全部质量落在 $h$ 正确区域、$Q$ 全部质量落在错误区域即可。

若对联合样本分布有

$$
\operatorname{TV}(P,Q)\le\eta
$$

且 loss 在 $[0,1]$，则任意 $h$ 有

$$
|R_P(h)-R_Q(h)|\le\eta.
$$

因此若 $P$-class excess 至多 $\varepsilon$：

$$
\begin{aligned}
R_Q(h)
&\le R_P(h)+\eta\\
&\le R_{\mathcal H,P}^*+\varepsilon+\eta\\
&\le R_{\mathcal H,Q}^*+\varepsilon+2\eta.
\end{aligned}
$$

于是原 high-probability event 可转成 $Q$ 上 excess 至多 $\varepsilon+2\eta$；代价来自输出和 comparator 各一次分布转换。
