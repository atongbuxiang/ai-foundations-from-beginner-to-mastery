---
type: exercise
status: draft
area: [learning-theory/pac, machine-learning/erm, classification]
topic: "[[可实现情形的一致 ERM 保证]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[PAC 学习定义与样本复杂度]]", "[[有限假设类、Union Bound 与一致收敛]]"]
related: ["[[解答 - 可实现情形的一致 ERM 保证]]", "[[不可知 PAC、ERM 与双侧一致收敛]]"]
solution: "[[解答 - 可实现情形的一致 ERM 保证]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - 可实现情形的一致 ERM 保证

> [!abstract] 训练目标
> 能从版本空间与坏假设生存概率独立重建 finite realizable PAC theorem，并清楚知道 $1/\varepsilon$ 快率依赖哪些强条件。

## A. 识别与复述

### LT-REA-A01

定义 realizability、training consistency、版本空间 $V(S)$ 与 $\varepsilon$-坏假设集。

### LT-REA-A02

为什么 realizable 0–1 setting 中任何 exact ERM 都 consistent？证明使用了 loss 的哪些性质？

### LT-REA-A03

陈述 finite realizable class 的 failure bound 与 sample complexity bound，并解释保证为何覆盖任意 consistent tie-breaking。

## B. 手算与构造

### LT-REA-B01

固定坏假设的真实错误率为 $p=0.08$，样本数 $m=50$。计算它零训练错误的精确概率、$(1-0.05)^{50}$ 上界和 $e^{-50\cdot0.05}$ 上界（假设坏阈值 $\varepsilon=0.05$）。

### LT-REA-B02

令 $M=2000,\varepsilon=0.03,\delta=0.05$。分别计算 simplified bound 与保留 $-\log(1-\varepsilon)$ 的样本量，向上取整并比较。

### LT-REA-B03

一个版本空间初有 16 个假设；给定样本后剩下 5 个，其中总体错误率分别为 $0,0.01,0.04,0.12,0.30$。当 $\varepsilon=0.05$ 时哪些是假设层面的坏存活者？若算法在版本空间均匀随机选择，条件于此 $S$ 的失败概率是多少？本节 theorem 控制的是哪个更强事件？

## C. 推导与证明

### LT-REA-C01

证明固定 $h$ 满足

$$
\Pr(R_S(h)=0)=(1-R_P(h))^m,
$$

并说明 iid 在哪一步使用。

### LT-REA-C02

从 bad-output event inclusion 开始，逐步证明

$$
\Pr(R_P(h_S)>\varepsilon)
\le M(1-\varepsilon)^m
\le Me^{-m\varepsilon}.
$$

### LT-REA-C03

从 $M(1-\varepsilon)^m\le\delta$ 推导 exact sample bound。证明 simplified $1/\varepsilon$ bound 确实更保守，并给出小 $\varepsilon$ 的 Taylor 解释。

## D. 边界、反例与纠错

### LT-REA-D01

给出一个带标签噪声的分布，使任何确定性 $h$ 的总体风险都大于零，并说明版本空间随 $m$ 增长为何可能为空。

### LT-REA-D02

纠正：“深度网络达到零训练错误，所以可直接使用 finite realizable ERM theorem。”至少审计 class cardinality、population realizability、iid 与 optimizer output 四项。

### LT-REA-D03

若算法只保证 $R_S(h_S)\le\tau>0$，指出 proof 中哪条等式失效；写出正确的 Binomial lower-tail event，并说明需要何种替代工具。

## E. AI 迁移

### LT-REA-E01

为一个有限医学诊断规则库判断 realizability 是否可信：区分标注噪声、特征不足、distribution shift 和 class misspecification，并决定应使用 realizable 还是 agnostic 分析。

### LT-REA-E02

把离散 prompt 库视为版本空间：给出能够使用本 theorem 的完整条件，并分析自然语言 ambiguity 会破坏哪一项。

### LT-REA-E03

比较“扩大 $M$ 十倍”和“把 $\varepsilon$ 减半”对 simplified sample complexity 的影响。将结果解释为模型选择自由度与目标精度的不同成本。

## 分级提示

- `B01`：精确概率是 $0.92^{50}$；
- `B03`：theorem 控制版本空间中根本不存在坏假设；
- `C03`：$-\log(1-\varepsilon)\ge\varepsilon$；
- `D01`：同一输入以正概率得到两个不同标签；
- `E03`：$M$ 在对数内，$\varepsilon$ 在分母中。

## 解答入口

完成独立尝试后再打开：[[解答 - 可实现情形的一致 ERM 保证]]。
