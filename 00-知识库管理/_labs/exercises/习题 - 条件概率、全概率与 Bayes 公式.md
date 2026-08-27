---
type: exercise-set
status: draft
area: [math/probability, math/statistics, ai/probabilistic-modeling]
aliases: [条件概率习题, Bayes 公式习题]
prerequisites: ["[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[解答 - 条件概率、全概率与 Bayes 公式]]", "[[练习与测验 MOC]]"]
sources: ["MIT-6.041SC-Lecture-2", "MIT-6.436J-Lecture-3", "Harvard-Stat110-Conditioning"]
created: 2026-08-18
updated: 2026-08-18
---

# 习题 - 条件概率、全概率与 Bayes 公式

> [!abstract] 训练目标
> 15 题检查筛选归一化、乘法/链式、全概率、Bayes、odds、连续密度、base rate、相关证据、选择与因果边界，以及分类和潜变量模型中的具体调用。

## A. 对象与条件（3 题）

### PROB-CB-A01：四个角色

在假设集合 $H_1,\ldots,H_k$ 与观测 $E$ 中，分别说明 $P(H_i)$、$P(E\mid H_i)$、$P(E)$、$P(H_i\mid E)$ 的名称、归一化变量和类型。为什么 likelihood 作为 $H_i$ 的函数时不必对 $i$ 求和为 1？

### PROB-CB-A02：条件方向

构造一个 $2\times2$ 频数表，使 $P(A\mid B)=0.9$ 但 $P(B\mid A)=0.1$。说明两者分母分别是什么，并验证联合概率双路公式。

### PROB-CB-A03：公式的合法条件

逐条写出条件：

1. $P(A\mid B)=P(A\cap B)/P(B)$；
2. $P(E)=\sum_iP(E\mid H_i)P(H_i)$；
3. Bayes 公式；
4. 多条 likelihood ratio 直接相乘。

特别指出分割、正概率与条件独立分别出现在哪里。

## B. 手算与表示（3 题）

### PROB-CB-B01：垃圾邮件过滤

$P(S)=0.2$。词语 `offer` 在垃圾邮件和正常邮件中出现的概率分别为 $0.7$ 与 $0.1$。计算 $P(S\mid\text{offer})$，并用 1000 封邮件频数表核对。若部署环境中 $P(S)=0.05$ 而类条件概率不变，后验变为多少？

### PROB-CB-B02：有偏主持人

Monty Hall 中你先选门 1。车若在门 1，主持人以概率 $0.9$ 开门 3、概率 $0.1$ 开门 2；车若在门 2 必开门 3；车若在门 3 必开门 2。观察到他打开门 3。求车在门 1 与门 2 的后验，并判断是否换门。

### PROB-CB-B03：odds 顺序更新

某假设先验概率 $P(H)=0.01$。两条证据的 likelihood ratio 分别为 $20$ 与 $5$，并假设它们在每个假设下条件独立。用 odds 计算后验。再去掉条件独立假设，写出正确但不能继续数值化的更新式。

## C. 推导与连续情形（3 题）

### PROB-CB-C01：条件概率仍是概率测度

固定 $B$ 且 $P(B)>0$，从三条概率公理证明 $Q(A)=P(A\mid B)$ 是概率测度。可列可加性的证明必须显示交集如何分配到并集。

### PROB-CB-C02：全概率与 Bayes

从 $E=\dot\bigcup_i(E\cap H_i)$ 开始，逐步推导可数全概率公式和 Bayes 公式。说明若 $P(E)=0$，哪一步失败；若某个 $P(H_i)=0$，该假设后验会怎样？

### PROB-CB-C03：Gaussian likelihood 的 odds

二元假设先验为 $P(H_0)=0.9,P(H_1)=0.1$。在 $H_0$ 下 $X\sim\mathcal N(0,1)$，在 $H_1$ 下 $X\sim\mathcal N(2,1)$。观察 $x=2$：计算 likelihood ratio、posterior odds 与 $P(H_1\mid x)$。说明这里使用的是 density ratio，不是 $P(X=2\mid H_i)$ 之比。

## D. 边界与纠错（3 题）

### PROB-CB-D01：零概率条件化

$X\sim\operatorname{Unif}(0,1)$。解释为什么事件分式不能定义 $P(X\le1/2\mid X=1/3)$。若给定 $Y=X$，一个 regular conditional version 会给什么直觉结果？为什么它只需几乎处处定义，不能把任意零测点版本升级为物理事实？

### PROB-CB-D02：base-rate fallacy

某罕见事件先验 $10^{-4}$，检测灵敏度 $0.99$、假阳性率 $0.01$。有人宣称“阳性后有 $99\%$ 概率为真”。计算正确后验，并说明最少需要把假阳性率降到多少以下，才能使后验超过 $1/2$（灵敏度与先验固定）。

### PROB-CB-D03：重复证据

证据 $E_2$ 是 $E_1$ 的完全复制，单条证据的 LR 为 10。为什么把两条 LR 相乘得到 100 是错的？写出 $P(E_2\mid H,E_1)$ 与竞争假设下的对应值，并求联合 LR。

## E. AI 迁移（3 题）

### PROB-CB-E01：label shift 纠偏

训练先验为 $(0.8,0.2)$，测试先验为 $(0.5,0.5)$。某样本的训练后验为 $(0.9,0.1)$。在 $p_{test}(x\mid y)=p_{train}(x\mid y)$ 假设下，重加权并归一化得到测试后验。列出该纠偏失败的三种情形。

### PROB-CB-E02：VAE 角色审计

给定 $p_\theta(z)$、$p_\theta(x\mid z)$、$q_\phi(z\mid x)$，写出模型联合、evidence、真实 posterior 和近似 posterior。说明为什么 $q_\phi$ 不能仅因符号中有条件竖线就叫“真实 Bayes 后验”。

### PROB-CB-E03：高置信度筛选与因果误读

模型只在 $C=1$（置信度过阈值）时预测。观察到 $P(Y=\widehat Y\mid C=1)$ 很高。说明这不能推出总体准确率、提高阈值会改善所有人群，也不能推出“置信度导致正确”。写出还需报告的概率和至少一个选择偏差诊断。

## 提交规范

每题至少用一次自然语言读取条件方向。Bayes 题必须给 evidence；AI 题必须写出训练/测试或生成/推断两个方向，不能只列公式。
