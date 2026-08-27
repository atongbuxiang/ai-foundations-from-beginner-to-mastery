---
type: source
status: draft
area: [sources, ai/attention, ai/sequence-models]
source_type: paper
title: "Neural Machine Translation by Jointly Learning to Align and Translate"
author: "Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio"
year: 2015
url: "https://arxiv.org/abs/1409.0473"
accessed: 2026-08-24
source_tier: A
license: "arXiv metadata; independent summary only"
scope_role: foundational
temporal_role: historical-origin
related: ["[[内容寻址、Query、Key 与 Value]]", "[[Self-Attention、Cross-Attention 与张量形状]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Bahdanau Attention：可学习对齐与内容寻址入口

> [!abstract] 来源定位
> 论文针对固定长度编码瓶颈，让译码器在每一步对编码器各位置计算可学习对齐分数并形成加权上下文。课程用它解释“query 提出当前需求、key 参与匹配、value 提供被读取内容”的历史原型；Q/K/V 矩阵写法与 scaled dot-product 仍以 Transformer 原论文为准。

## 核心对象

在译码时刻 $i$，以译码状态和第 $j$ 个源表示计算能量 $e_{ij}$，归一化为

$$
\alpha_{ij}=\frac{\exp e_{ij}}{\sum_{j'}\exp e_{ij'}},\qquad
c_i=\sum_j\alpha_{ij}h_j.
$$

$c_i$ 是对源表示的软读取，而不是先把整个源句压成单个固定向量。权重可被观察，但论文并未证明它们等于人类对齐或因果解释。

## 课程采用与边界

| 断言 | 类型 | 采用边界 |
|---|---|---|
| 解码状态可依内容动态读取源序列 | 模型定义 `I` | 采用 |
| 权重非负且和为 1 时，上下文是 value 的凸组合 | 数学恒等 `I` | 采用 |
| attention 权重就是忠实解释 | 解释主张 | 不采用；须另做反事实/因果验证 |
| Bahdanau 形式等同 Transformer dot-product attention | 架构等同 | 不采用；score 与整体结构不同 |

## 调用

- [[内容寻址、Query、Key 与 Value]]：软寻址的历史问题；
- [[Self-Attention、Cross-Attention 与张量形状]]：encoder–decoder cross-attention 原型；
- [[Attention 失效模式、反例与证据地图]]：对齐权重与解释证据的分离。
