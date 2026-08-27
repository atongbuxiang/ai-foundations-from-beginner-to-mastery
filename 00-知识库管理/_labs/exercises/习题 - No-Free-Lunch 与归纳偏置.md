---
type: exercise
status: draft
area: [learning-theory/foundations, no-free-lunch]
topic: "[[No-Free-Lunch 与归纳偏置]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[PAC 学习定义与样本复杂度]]", "[[命题、量词与逻辑等价]]"]
related: ["[[解答 - No-Free-Lunch 与归纳偏置]]", "[[样本复杂度下界与 Minimax 视角]]"]
solution: "[[解答 - No-Free-Lunch 与归纳偏置]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - No-Free-Lunch 与归纳偏置

> [!abstract] 训练目标
> 能重建 $2m$ 点 NFL proof，熟练审计量词，并把“归纳偏置不可避免”转成可检查的 architecture、representation、data 与 evaluation 合同。

## A. 识别与复述

### LT-NFL-A01

写出教材版 $1/7$—$1/8$ No-Free-Lunch theorem 的全部量词。困难分布可依赖哪些对象？

### LT-NFL-A02

为什么 theorem 的困难分布仍 realizable？困难来自噪声、优化还是未见标签信息不足？

### LT-NFL-A03

区分 restriction、preference、representation、data/augmentation 与 evaluation 五类归纳偏置，各给一个 AI 例子。

## B. 手算与构造

### LT-NFL-B01

令 $m=2$，取 $|C|=4$。共有多少种 target labelings？任意长度 2 的 sample 至少留下多少未见点？对 targets 均匀平均时，这些点贡献的 expected population risk 至少多少？

### LT-NFL-B02

若 $Z\in[0,1]$ 且 $\mathbb EZ\ge0.3$，证明

$$
\Pr(Z\ge0.1)\ge2/9.
$$

### LT-NFL-B03

输入域大小为 100、样本量为 40。教材 NFL 的条件是否满足？它能保证存在怎样的 realizable distribution 与 failure event？

## C. 推导与证明

### LT-NFL-C01

从选取 $2m$ 个点开始，完整证明 target-average expected risk 至少 $1/4$，不得省略 conditioning on seen/unseen labels。

### LT-NFL-C02

由 `C01` 推出存在固定 target $\bar f$，再把 expectation lower bound 转成

$$
\Pr(R_P(A(S))\ge1/8)\ge1/7.
$$

### LT-NFL-C03

用反证法证明：无限域上所有二分类函数组成的 class 不可 PAC 学习。明确选择 $\varepsilon, \delta$ 和 PAC threshold 后如何调用 NFL。

## D. 边界、反例与纠错

### LT-NFL-D01

纠正：“NFL 说明所有算法在每个任务上都一样。”给出一个特定结构 task family，使一个匹配偏置的算法明显优于反向偏置算法。

### LT-NFL-D02

随机化能否逃脱 NFL？分析 algorithm seed 为什么不能提供未见 target labels 的信息。

### LT-NFL-D03

解释 NFL 与某个 memorizer 对每个固定离散 $P$ pointwise consistent 为什么不矛盾；写出两者不同的量词顺序。

## E. AI 迁移

### LT-NFL-E01

审计 Transformer 的归纳偏置：至少从 tokenization、attention、parameter sharing、pretraining distribution、objective 和 optimizer 六方面说明排除了哪些任意函数。

### LT-NFL-E02

一个图像分类器使用 rotation augmentation。说明这是何种偏置；构造一个 rotation 会改变标签的任务，展示 beneficial bias 如何变成 harmful bias。

### LT-NFL-E03

评议：“大模型在许多 benchmark 上都更好，已证明它是 universal learner。”把经验事实、task-family 假设、selection bias 与 NFL 不允许的外推分开。

## 分级提示

- `B01`：target 数为 $2^4$；
- `B02`：上界 $\mathbb EZ\le0.1(1-q)+q$；
- `C01`：每个未见点质量 $1/(2m)$、平均错误 $1/2$；
- `D03`：比较 $\forall m\exists P_m$ 与 $\forall P\exists m_P$；
- `E02`：数字 6/9、方向箭头或医学影像 orientation 都可构造反例。

## 解答入口

完成独立尝试后再打开：[[解答 - No-Free-Lunch 与归纳偏置]]。
