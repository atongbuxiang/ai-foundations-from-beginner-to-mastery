---
type: exercise
status: draft
area: [learning-theory/pac, machine-learning/foundations]
topic: "[[PAC 学习定义与样本复杂度]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[可实现、不可知、相合性与可学习性]]", "[[命题、量词与逻辑等价]]"]
related: ["[[解答 - PAC 学习定义与样本复杂度]]", "[[可实现情形的一致 ERM 保证]]"]
solution: "[[解答 - PAC 学习定义与样本复杂度]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - PAC 学习定义与样本复杂度

> [!abstract] 训练目标
> 能把任何“模型可以可靠学会”的自然语言声称重写成包含 class、distribution、loss、comparator、精度、置信、样本与算法随机性的 PAC 合同。

## A. 识别与复述

### LT-PAC-A01

分别写出 realizable binary PAC 与 bounded-loss agnostic PAC 的正式定义；指出 comparator 的区别。

### LT-PAC-A02

解释 $\varepsilon$、$\delta$、$m$ 各自控制什么。为什么 $\delta$ 既不是单点分类错误率，也不是模型校准置信度？

### LT-PAC-A03

区分：某次输出成功、某个算法 PAC、某个 class PAC learnable、某个 class efficiently PAC learnable。

## B. 手算与构造

### LT-PAC-B01

某 theorem 给出

$$
m(\varepsilon,\delta)=\left\lceil\frac{3\log(2/\delta)+5d}{\varepsilon^2}\right\rceil.
$$

计算 $d=20,\varepsilon=0.1,\delta=0.05$ 的充分样本量，并说明这是何种精度层次的声称。

### LT-PAC-B02

若有 bounded excess random variable $\mathcal E\in[0,1]$，且 $\Pr(\mathcal E>0.03)\le0.02$，给出 $\mathbb E\mathcal E$ 的简单上界。反之若只知 $\mathbb E\mathcal E\le10^{-4}$，用 Markov 控制 $\Pr(\mathcal E>0.01)$。

### LT-PAC-B03

构造一个 randomized learner：对任意样本，以概率 $0.99$ 输出完美预测器，以概率 $0.01$ 输出错误率 1 的预测器。计算它在 $(\varepsilon,delta)=(0.1,0.02)$ 与 $(0.1,0.005)$ 下是否满足 PAC event。

## C. 推导与证明

### LT-PAC-C01

把 agnostic PAC 定义完整展开成量词式，并证明把 $\exists A$ 与 $\forall P$ 交换会得到更弱、甚至平凡的命题。

### LT-PAC-C02

假设对所有 $\varepsilon,\delta$ 有 PAC guarantee。选择一列 $(\varepsilon_m,\delta_m)$，说明怎样推出 excess risk 依概率趋于零；再解释为什么仅有相合性未给出显式 sample complexity。

### LT-PAC-C03

若算法对 $m_0$ 个样本满足 PAC 合同，证明一个可以忽略多余样本的算法对所有 $m\ge m_0$ 仍满足合同。指出原算法若随 $m$ 改变行为，结论为何不是自动的。

## D. 边界、反例与纠错

### LT-PAC-D01

纠正：“distribution-free PAC 没有任何数据分布假设。”列出至少五个仍被固定的协议条件。

### LT-PAC-D02

给出一个 class 统计上可学习但朴素 ERM 计算代价指数级的例子框架。说明 sample efficiency 与 computational efficiency 为什么必须分账。

### LT-PAC-D03

纠正：“一个模型在 benchmark 上达到 $98\%$ accuracy，所以已经以 $98\%$ confidence PAC 学会。”列出从单次结果到 PAC theorem 缺失的全部主要环节。

## E. AI 迁移

### LT-PAC-E01

为“从有限 prompt 库学习一个客服回复策略”写 realizable 和 agnostic 两份 PAC 合同，并说明现实中哪份更可信。

### LT-PAC-E02

审计一个 foundation model 下游线性探针的 PAC 声称：区分预训练数据、冻结表示、下游 class、训练样本和测试分布分别进入哪个条件。

### LT-PAC-E03

面对部署分布 $Q\ne P$，证明原本对 $R_P$ 的 PAC 界不能单独推出 $R_Q$ 界；提出一个加入 total variation 距离假设后的可用桥梁。

## 分级提示

- `B01`：使用自然对数；
- `B02`：好事件上最多 0.03，坏事件上最多 1；
- `C01`：知道 $P$ 的专用算法可以直接输出 $P$-oracle；
- `C02`：可令目标精度和失败概率都随 $m$ 趋零；
- `E03`：对 $[0,1]$ loss，期望差可由 total variation 控制。

## 解答入口

完成独立尝试后再打开：[[解答 - PAC 学习定义与样本复杂度]]。
