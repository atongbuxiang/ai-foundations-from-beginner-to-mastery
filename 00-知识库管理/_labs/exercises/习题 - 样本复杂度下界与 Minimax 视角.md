---
type: exercise
status: draft
area: [learning-theory/lower-bounds, statistics/minimax]
topic: "[[样本复杂度下界与 Minimax 视角]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[No-Free-Lunch 与归纳偏置]]", "[[交叉熵与 KL 散度]]", "[[假设检验、置信区间与多重比较]]"]
related: ["[[解答 - 样本复杂度下界与 Minimax 视角]]", "[[二分类统计学习基本定理]]"]
solution: "[[解答 - 样本复杂度下界与 Minimax 视角]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - 样本复杂度下界与 Minimax 视角

> [!abstract] 训练目标
> 能把 estimation/learning 成功归约成 testing 成功，使用 Le Cam、Fano 与 rare-event construction 证明任何算法都无法越过的 rate。

## A. 识别与复述

### LT-MIN-A01

定义 expected minimax risk、high-probability minimax quantile 与 PAC sample complexity。三者的概率/期望对象有何不同？

### LT-MIN-A02

解释 Le Cam、Fano、Assouad 分别使用 two points、packing、hypercube 的哪种结构。

### LT-MIN-A03

为什么“某个算法失败”不是 minimax lower bound？一份合法 lower-bound construction 必须同时检查哪些条件？

## B. 手算与构造

### LT-MIN-B01

令 $P_0=\mathrm{Ber}(0.45),P_1=\mathrm{Ber}(0.55)$，$m=20$。计算 single-sample KL、用 Pinsker 上界 product TV，再给出 Le Cam absolute-error expected-risk lower bound。

### LT-MIN-B02

使用正文的保守 bound

$$
m\ge\frac{\log(1/(4\delta))}{16\varepsilon^2}
$$

计算 $\varepsilon=0.05,\delta=0.05$ 时的必要样本尺度。

### LT-MIN-B03

Fano construction 有 $N=64$ 个等可能 hypotheses，且 $I(V;S)\le0.25\log N$。计算任意 decoder 的错误率下界。

## C. 推导与证明

### LT-MIN-C01

从 $d(\theta_0,\theta_1)\ge2s$ 构造 nearest-parameter test，完整推导 Le Cam expected metric-risk 与 high-probability lower bound。

### LT-MIN-C02

陈述 Fano inequality；在 pairwise-separated packing 与 average KL 条件下，把 decoding error 转成 estimation lower bound，并解释 $\log N$ 的来源。

### LT-MIN-C03

构造两个只在质量 $2\varepsilon$ rare point 上标签不同的 realizable worlds，证明要把 excess-$>\varepsilon$ failure 压到 $\delta$，样本量需为 $\Omega(\log(1/\delta)/\varepsilon)$。

## D. 边界、反例与纠错

### LT-MIN-D01

某人展示 SGD 在一个分布上失败，就声称所有算法至少需要 $m$ 个样本。指出逻辑错误，并说明怎样改造成 algorithm-independent testing lower bound。

### LT-MIN-D02

纠正：“expected lower bound 与 PAC high-probability lower bound 完全等价。”给出稀有巨大损失的随机变量说明尾部形状的重要性。

### LT-MIN-D03

为什么不能仅由 $|\mathcal H|=M$ 就断言每个具体 class 都有 $\Omega(\log M/\varepsilon^2)$ lower bound？给出高度冗余/嵌套 class 的解释。

## E. AI 迁移

### LT-MIN-E01

为概率为 $p$ 的稀有安全失败设计一个 two-world lower-bound argument，解释为什么“测试中零事故”仍需约 $1/p$ 级独立 exposure 才有意义。

### LT-MIN-E02

两个 checkpoints 的真实平均评分差为 $0.01$、每例 bounded noise 为常数量级。用 testing 直觉估计可靠排序的样本尺度，并讨论 paired evaluation 可利用什么额外结构。

### LT-MIN-E03

比较 minimax、Bayes-average、local minimax 与 instance-dependent 四种评价大型模型学习难度的视角；分别说明适用问题。

## 分级提示

- `B01`：$\mathrm{KL}=0.1\log(0.55/0.45)$，Le Cam 中 $s=0.05$；
- `B03`：$\log2/\log64=1/6$；
- `C03`：未见 rare point 时两个 worlds 的 observed sample 完全相同；
- `D02`：让 loss 以很小概率取 1、其余为 0；
- `E02`：基本尺度是 $1/(0.01)^2$，paired difference 可降低 variance 常数。

## 解答入口

完成独立尝试后再打开：[[解答 - 样本复杂度下界与 Minimax 视角]]。
