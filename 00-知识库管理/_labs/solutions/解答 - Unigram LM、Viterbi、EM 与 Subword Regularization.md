---
type: solution
status: verified
area: [language-models, tokenization, unigram-lm]
topic: "[[Unigram LM、Viterbi、EM 与 Subword Regularization]]"
exercise: "[[习题 - Unigram LM、Viterbi、EM 与 Subword Regularization]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Unigram LM、Viterbi、EM 与 Subword Regularization

## A. 识别与复述

### LM06-A01
$p(s)=\prod p(v)$ 是一条分段路径；$p(x)=\sum_{s\in S(x)}p(s)$ 汇总所有路径；$p(s|x)=p(s)/p(x)$ 是给定字符串后的分段不确定性。

### LM06-A02
Viterbi 返回 MAP 路径/分数；forward 返回所有路径概率和（log-space 为 log marginal）；sampling 按声明的后验/温度分布输出随机路径。

### LM06-A03
Unigram 是 tokenizer 内部的分段评分器；Transformer 得到 token 序列后建模 $p(z_t|z_{<t})$，具有上下文依赖。前者的独立假设不约束后者结构。

## B. 手算与构造

### LM06-B01
`[a,b]` 概率 .12，`[ab]` .2；marginal .32，MAP `[ab]`。后验分别 .12/.32=.375 与 .2/.32=.625。

### LM06-B02
`[a,a]` 概率 .25、cost $-\ln.25\approx1.3863$；`[aa]` 概率 .3、cost $-\ln.3\approx1.2040$，故 MAP `[aa]`。

### LM06-B03
权重为 $\sqrt{.25}=.5$、$\sqrt{.3}\approx.5477$；归一化和 1.0477，概率约 .4772 与 .5228。

## C. 推导与证明

### LM06-C01
任何到 j 的路径最后经过某个 i→j，故 $\alpha[j]=\sum_i\alpha[i]p(x_{i:j})$。边被使用的路径质量分解为“到 i”×“边”×“从 j 到尾”，除总质量 $p(x)=\alpha[n]$ 得 $\gamma_{ij}=\alpha[i]p(v)\beta[j]/p(x)$。

### LM06-C02
$Q=\sum_v\hat c(v)\log p(v)+\lambda(\sum_vp(v)-1)$。求导 $\hat c(v)/p(v)+\lambda=0$，得 $p(v)\propto\hat c(v)$；归一化即 $p(v)=\hat c(v)/\sum_u\hat c(u)$。

### LM06-C03
$p(x)=\sum_sp(s)\ge\max_sp(s)$。负对数单调递减，故 $-\log p(x)\le-\log\max_sp(s)$。

## D. 边界、反例与纠错

### LM06-D01
LM06-B01 中 Viterbi .2 而字符串概率 .32，差值来自另一合法路径 .12。

### LM06-D02
$\alpha\to0$ 使每条**合法路径**权重趋 1；含 token 多的路径并不会让每个 token 边均匀，边的 marginal 由它出现在多少路径决定。

### LM06-D03
词表 `{a}`，输入 `ab` 在位置 1 无覆盖到终点的边；forward $\alpha[2]=0$，log probability $-\infty$，Viterbi 无路径。需 byte/character fallback 或 UNK。

## E. AI 迁移

### LM06-E01
取长度≤5、可枚举全部路径的小词表；精确算 $q_\alpha$；固定 seed 抽样 N 次，比较每路径频率与 multinomial 标准误差，并断言不可能路径频率 0、概率和 1。

### LM06-E02
相同模型/数据/FLOPs/steps/seeds，对照 deterministic MAP 与多个 $\alpha$/nbest；primary metric 预注册，测 in-domain、domain shift、拼写扰动和 length；同时报告实际 token 长度/compute，避免把增强与预算混杂。

### LM06-E03
记录 piece expected count、移除后的 log-likelihood/code-length change、覆盖/byte fallback、词表大小、语言切片、held-out marginal NLL、训练/编码速度与下游差异；剪枝后重新估计而非只删文件行。

## 无提示重做

- [ ] 对长度 3 串手算 forward/backward/edge posterior。
- [ ] 从枚举概率验证一次随机采样器。

