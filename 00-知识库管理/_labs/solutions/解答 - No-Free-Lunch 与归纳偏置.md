---
type: solution
status: draft
area: [learning-theory/foundations, no-free-lunch]
topic: "[[No-Free-Lunch 与归纳偏置]]"
exercise: "[[习题 - No-Free-Lunch 与归纳偏置]]"
prerequisites: ["[[PAC 学习定义与样本复杂度]]", "[[命题、量词与逻辑等价]]"]
related: ["[[样本复杂度下界与 Minimax 视角]]", "[[打散、增长与 VC 维]]"]
sources: ["[[S-1996-Wolpert-Lack-of-A-Priori-Distinctions]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - No-Free-Lunch 与归纳偏置

> [!warning] 使用边界
> NFL 的结论只在明确的问题族、平均/最坏量词与 loss 下成立。把它压成“所有算法一样”会同时丢掉 theorem 和现实含义。

## A. 识别与复述

### LT-NFL-A01

$$
\forall A,\forall m<|\mathcal X|/2,
\exists P,\exists f:\mathcal X\to\{0,1\}:
R_P(f)=0
$$

且

$$
\Pr_{S\sim P^m,U}
\left(R_P(A(S,U))\ge1/8\right)
\ge1/7.
$$

$P$ 与 $f$ 可依赖算法 $A$ 和样本预算 $m$；不是先固定一个 universal hard distribution。

### LT-NFL-A02

每个困难分布 $P_f$ 只在 pairs $(x,f(x))$ 上有质量，所以 target $f$ 的 risk 恰为零。没有 label noise，且 proof 不依赖 optimization failure。困难来自样本最多观察一半 support points，任意 labeling family 让未见 labels 与已见信息独立。

### LT-NFL-A03

- restriction：线性 class 排除非线性边界；
- preference：weight decay/SGD 偏爱某些插值解；
- representation：CNN locality 或 tokenizer 决定易表达结构；
- data/augmentation：rotation augmentation 假设旋转保标签；
- evaluation：cross-entropy、BLEU 或 judge rubric 决定何谓好输出。

## B. 手算与构造

### LT-NFL-B01

labelings 数：

$$
2^{|C|}=2^4=16.
$$

sample 长 2，最多见 2 个 distinct points，所以至少 2 个未见。每点 population mass $1/4$，target-average error $1/2$：

$$
2\cdot\frac14\cdot\frac12=\frac14.
$$

### LT-NFL-B02

令 $q=\Pr(Z\ge0.1)$。boundedness 给

$$
\mathbb EZ
\le0.1(1-q)+1q
=0.1+0.9q.
$$

结合 $\mathbb EZ\ge0.3$：

$$
0.3\le0.1+0.9q
\Rightarrow
q\ge\frac{0.2}{0.9}=\frac29.
$$

### LT-NFL-B03

$40<100/2=50$，条件满足。因此对任意 algorithm，都存在一个由 deterministic target labeling 产生的 realizable distribution，使

$$
\Pr(R_P(A(S))\ge1/8)\ge1/7.
$$

定理只保证存在该分布，不声称所有 100-point distributions 都困难。

## C. 推导与证明

### LT-NFL-C01

选 $C$ 含 $2m$ 点，令 $F$ 在 $2^{2m}$ 个 labelings 中均匀。给定 target $f$，$P_f$ 在 graph $(x,f(x))$ 上均匀。固定 training input sequence $S_X$；它至多含 $m$ 个 distinct points，所以未见集合 $U$ 至少有 $m$ 点。

进一步固定 seen labels 和 algorithm seed。对每个 $x\in U$，$F(x)$ 在所有与 seen labels 一致的 targets 中仍是公平、相互独立的 bit，而 $A(S)(x)$ 不依赖 $F(x)$。故

$$
\mathbb E_F\mathbf1\{A(S)(x)\ne F(x)\}=1/2.
$$

每个点质量 $1/(2m)$，所以条件平均 risk 至少

$$
|U|\frac1{2m}\frac12
\ge m\frac1{2m}\frac12=1/4.
$$

再对 $S_X$、seen labels 和 seed 取期望，仍有联合 target–sample average risk $\ge1/4$。

### LT-NFL-C02

有限 targets 的平均至少 $1/4$，故存在 $\bar f$ 使

$$
\mathbb E_{S\sim P_{\bar f}^m}R_{P_{\bar f}}(A(S))\ge1/4.
$$

令 $Z$ 为该 risk、$q=\Pr(Z\ge1/8)$。因 $Z\in[0,1]$：

$$
1/4\le\mathbb EZ
\le(1/8)(1-q)+q
=1/8+7q/8.
$$

所以 $q\ge1/7$。

### LT-NFL-C03

假设无限域上 $\mathcal H=\{0,1\}^{\mathcal X}$ PAC learnable。取 $\varepsilon<1/8,\delta<1/7$，由定义存在有限 $m=m_{\mathcal H}(\varepsilon,\delta)$。无限域包含至少 $2m+1$ 个点，NFL 给一个 realizable $P$，使 risk $\ge1/8>\varepsilon$ 的概率至少 $1/7>\delta$，与 PAC guarantee 矛盾。因此该 class 不可 PAC 学习。

## D. 边界、反例与纠错

### LT-NFL-D01

令 task family 只有常数零 target。算法 $A_0$ 永远输出 0，risk 为 0；反向算法 $A_1$ 永远输出 1，risk 为 1。它们在这个结构 family 上显然不同。NFL 只在允许全部/对称 labelings 的 family 中取消无条件优势；真实先验不均匀时算法可被排序。

### LT-NFL-D02

seed $U$ 与未知未见 label 独立。固定 seen information 后，即使 prediction 是随机 bit，与均匀 target bit 的 match probability 仍为 $1/2$。对 seed 取平均不会产生 information。随机化可改善某些 adversarial-game constants，却不能从无观察中恢复 arbitrary label。

### LT-NFL-D03

NFL：

$$
\forall m\ \exists P_m:\text{algorithm 在预算 }m\text{ 失败}.
$$

pointwise consistency：

$$
\forall P\ \forall\varepsilon,\delta\ \exists m_P(\varepsilon,\delta):
\text{超过分布依赖阈值成功}.
$$

一个固定 $P$ 最终可被 memorizer 覆盖，不妨碍 adversary 随 $m$ 选择 support 更宽/尾部更难的新 $P_m$。PAC 需要不依具体 $P$ 的统一 threshold。

## E. AI 迁移

### LT-NFL-E01

tokenizer 把世界压成离散 tokens，偏爱可分词/有限上下文结构；attention 偏爱 content-addressable pair interactions；parameter sharing 假设位置/任务间可复用规律；pretraining distribution 偏爱互联网语言与其文化频率；next-token objective 偏爱预测性而非因果/价值充分性；optimizer、initialization 和 regularization 在众多插值解中偏爱可达、低范数或大 margin 解。它们共同排除任意 input-output functions，但也会在非语言、长尾和 shift 场景失配。

### LT-NFL-E02

rotation augmentation 是 data/invariance bias，假设旋转后 label 不变。对猫狗自然图像可能近似有利；对区分数字 6 与 9、上/下箭头、医学影像左右方向的任务，旋转会改变标签或临床含义。强制 invariance 会合并本应区分的 inputs，增加 approximation/target mismatch。

### LT-NFL-E03

事实：在所选 benchmarks/protocol 上，大模型平均更高。还需假设未来任务来自相似 meta-distribution，且 benchmark 没有 contamination、selection 和 metric gaming。NFL 禁止的是从有限 task evidence 外推“对所有 labelings/所有未来分布都优越”。合理结论是 task-family conditional superiority，并需用 transfer/shift experiments 描述边界。
