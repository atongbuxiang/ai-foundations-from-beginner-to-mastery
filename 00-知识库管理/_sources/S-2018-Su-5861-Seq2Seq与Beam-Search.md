---
type: source
status: verified
area: [sources, ai/text-generation, algorithms/search, math/combinatorics]
source_type: blog
title: "玩转Keras之seq2seq自动生成标题"
author: 苏剑林
year: 2018
url: "https://spaces.ac.cn/archives/5861"
accessed: 2026-08-26
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [信息时代]
scope_role: bridge
temporal_role: classical-exposition
related: ["[[数学归纳、递归与组合计数]]", "[[S-2021-Su-8062-从文本生成到搜索采样]]"]
created: 2026-08-19
updated: 2026-08-26
---

# 玩转Keras之seq2seq自动生成标题：Beam Search接口

> [!abstract] 来源定位
> 文章以Seq2Seq标题生成为背景，写出逐token条件概率分解，并比较greedy、完整路径枚举与beam search；同时指出朴素解码实现若每步重跑完整prefix，会把原可缓存的线性step结构推向更高累计成本。MATH-05只采用其搜索树、top-$K$剪枝和实现成本问题，不采用旧Keras API作为当前软件证据。

## 元数据与纳入

- 正式引用：苏剑林，2018-09-01，《玩转Keras之seq2seq自动生成标题》；
- 页面：[https://spaces.ac.cn/archives/5861](https://spaces.ac.cn/archives/5861)；
- 范围角色：自回归条件分解、beam search与prefix计算成本的中文AI案例；
- Formal induction/counting由Hammack与MIT课程承担。

## 核心结构

自回归条件分解：

$$
p(y_{1:T}\mid x)
=\prod_{t=1}^{T}p(y_t\mid x,y_{<t}).
$$

Greedy每步保留一个best prefix；beam size $K$每步从当前至多$K$个prefix扩展候选，再按累计score只保留top $K$。

固定vocabulary size $V$、无EOS与grammar约束时：

- 完整长度$T$路径：$V^T$；
- Beam稳定阶段每步candidate extensions上界：$KV$；
- Retained prefixes上界：$K$。

这些是本课程基于文章问题设置补写的组合合同，不是对所有实现的runtime定理。

## 核心断言与课程判断

| ID | 断言 | 条件/边界 | 判断 |
|---|---|---|---|
| C1 | Greedy局部最优不保证sequence全局score最大 | 条件概率乘积依prefix | 已核验 |
| C2 | 完整枚举随长度指数增长 | 固定$V$、全分支、固定长度 | 条件结论 |
| C3 | Beam以固定宽度保留多个prefix，折中搜索成本 | Ranking、EOS、ties需声明 | 已核验 |
| C4 | Beam等价于exact dynamic programming | 一般无exact state merging | 不采用 |
| C5 | 每步重算全部prefix会提高累计推理成本 | 是否有cache/state reuse依实现 | 有条件采用 |
| C6 | 更大beam一定带来更好task metric | Score/metric mismatch、length/exposure bias | 不采用 |

## 课程补严

- 区分candidate-space size、visited prefixes、model forward FLOPs与retained memory；
- 把EOS/max length作为termination contract；
- 把beam标为heuristic pruning，除非另证exact state merging；
- 区分model log-score、search optimality和external evaluation metric；
- 说明KV cache/RNN state cache改变implementation cost，不改变序列空间计数；
- 旧Keras实现只用于历史问题入口，不作为当前API建议。

## 已生成与后续调用

- [x] [[数学归纳、递归与组合计数]]：自回归树、beam width、termination与DP边界；
- [x] [[习题 - 数学归纳、递归与组合计数]]：MATH-IND-E01；
- [x] [[实验 - 归纳覆盖、递归调用与组合计数审计]]：$V=4,K=3$的exact prefix count；
- [ ] 文本生成专题：length normalization、diverse beam与sampling解码。

## 交叉验证

- [[S-2021-Su-8062-从文本生成到搜索采样]]；
- [[S-2025-Hammack-Book-of-Proof-Induction-Counting]]；
- MIT 6.1200J counting与recurrence讲义。
