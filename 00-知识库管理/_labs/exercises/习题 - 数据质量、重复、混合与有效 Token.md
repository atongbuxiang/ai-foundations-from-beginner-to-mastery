---
type: exercise
status: verified
area: [training, scaling-laws, data]
topic: "[[数据质量、重复、混合与有效 Token]]"
solution: "[[解答 - 数据质量、重复、混合与有效 Token]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 数据质量、重复、混合与有效 Token

> [!abstract] 训练目标
> 从“token 数”推进到 raw、unique、seen、repeat 与 effective token 账本，并把数据混合视为带目标权衡和迁移效应的实验问题。

## A. 识别与复述

### TRN53-A01
定义 raw tokens、unique tokens、seen tokens、repetition count 与 effective tokens；哪一个通常不是直接观测量？

### TRN53-A02
区分数据质量、数据多样性、目标相关性与污染。为什么它们不能压缩成一个无上下文的“质量分数”？

### TRN53-A03
设混合权重 $w\in\Delta^{K-1}$，解释 simplex 约束及域损失向量 $\ell(w)$ 的含义。

## B. 手算与构造

### TRN53-B01
某语料有 100B unique tokens，训练 5 epochs。若第 $j$ 次出现的边际权重为 $q^{j-1}$、$q=0.6$，计算 effective tokens。

### TRN53-B02
三域 validation loss 为 $(2.0,1.5,3.0)$。分别按目标权重 $(0.5,0.3,0.2)$ 与 $(0.1,0.2,0.7)$ 求聚合 loss，并说明“最佳混合”依赖部署目标。

### TRN53-B03
同一文本由 tokenizer A 切成 1.0B tokens，由 B 切成 1.3B tokens。若报告每 token loss 为 2.0 与 1.7，为什么不能据此直接判定 B 更好？还需什么共同单位？

## C. 推导与证明

### TRN53-C01
推导重复 $r$ 次、边际权重几何衰减时
$$
D_{eff}=U\frac{1-q^r}{1-q},
$$
并讨论 $r\to\infty$ 的上限。

### TRN53-C02
令 $M_{ij}=\partial\ell_i/\partial w_j$。解释对角与非对角元素各表示什么，并说明为何只看总 loss 无法恢复 $M$。

### TRN53-C03
若训练目标是 $J(w)=\sum_i v_i\ell_i(w)$，在 simplex 内部写出一阶方向导数条件；解释它为何不意味着所有域 loss 相等。

## D. 边界、反例与纠错

### TRN53-D01
反驳：“研究发现数据最多重复四轮，所以所有语料超过四 epoch 都无效。”

### TRN53-D02
构造一个总 validation loss 改善、但关键小域显著退化的例子。说明聚合指标如何隐藏伤害。

### TRN53-D03
为什么去重率高不自动意味着有效 token 少，也不自动意味着模型更差？区分冗余、强化与覆盖。

## E. AI 迁移

### TRN53-E01
为一个多域预训练数据集写 token ledger 与 provenance audit，至少列出十项字段。

### TRN53-E02
设计一个固定 compute 的 mixture 实验，能估计局部迁移矩阵而不把模型规模、tokenizer 和训练时长混入。

### TRN53-E03
设计 contamination audit：区分 exact match、near duplicate、模板泄漏与训练后评测自适应，并规定报告边界。

## 作答与复盘

先为每个 token 数加下标 raw / unique / seen / effective，再查看 [[解答 - 数据质量、重复、混合与有效 Token]]。
