---
type: source
status: draft
area: [sources, math/information-theory, ai/nlp]
source_type: blog
title: "GlobalPointer下的“KL散度”应该是怎样的？"
author: 苏剑林
year: 2022
url: "https://spaces.ac.cn/archives/9039"
accessed: 2026-08-19
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
site_category: [自然语言处理]
series: "GlobalPointer"
scope_role: core
temporal_role: method-analysis
related: ["[[交叉熵与 KL 散度]]", "[[f-散度、Bregman 散度与概率度量]]"]
created: 2026-08-19
updated: 2026-08-19
---

# GlobalPointer 下的“KL 散度”应该怎样定义

> [!abstract] 来源定位
> 文章从一个关键对象错误出发：GlobalPointer 的整体输出不是归一化概率分布，因此不能把两个输出张量直接代入标准 categorical KL。作者转而构造基于 sigmoid/logit 的对称一致性 surrogate。课程采用这个边界案例训练“先确认概率空间，再命名散度”。

## 元数据与纳入

- 正式引用：苏剑林，2022-04-15，《GlobalPointer下的“KL散度”应该是怎样的？》；
- 原始页面：[https://spaces.ac.cn/archives/9039](https://spaces.ac.cn/archives/9039)；
- 当前调用者：[[交叉熵与 KL 散度]]；
- 方法背景涉及 R-Drop/一致性正则，但本卡不把所提 surrogate 宣称为标准 KL 的唯一延拓。

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | 整体 logits/多标签分数不一定构成一个 categorical distribution | 对象审计 | 看归一化轴与任务语义 | 已核验 |
| C2 | 标准 $D_{\rm KL}(P\|Q)$ 要求两个 probability measures | 定义边界 | 同一可测空间且 $P\ll Q$ 才有限 | 已核验 |
| C3 | 可对每个 Bernoulli marginal 定义 KL，或构造 logit surrogate | 方法选择 | 二者代表不同 joint 假设和目标 | 有条件成立 |
| C4 | 对称化有利于一致性正则 | 经验/优化建议 | 不保证 calibration、metric 或原 KL 语义 | 待任务验证 |

## 课程采用的对象审计

在写“KL loss”前必须回答：

1. 每个张量对应哪个随机变量？
2. 哪个轴归一化，总质量是否为 $1$？
3. 是 mutually exclusive categorical，还是多个 Bernoulli label？
4. 两个 distribution 的 support 是否一致？
5. 若只是 logits，所用函数是 standard KL、Bernoulli KL、Bregman divergence，还是自定义 surrogate？

若 $a_i,b_i$ 是独立 Bernoulli 的 logits，可先令 $p_i=\sigma(a_i)$、$q_i=\sigma(b_i)$，再按显式 independence 假设求各维 Bernoulli KL 之和。若直接在 logits 上构造对称项，则应按其公式命名，不应只写 “KL” 掩盖对象变化。

## 限制与保留意见

- marginal Bernoulli 概率不唯一决定 labels 的 joint law；
- symmetric KL 仍通常不满足 triangle inequality；
- 一致性 penalty 的数值下降不等于预测分布已校准；
- stop-gradient、temperature、mask 和 reduction 都会改变优化含义；
- 文章给出的是特定模型的目标设计，不是普遍信息论定理。

## 已生成与后续调用

- [x] [[交叉熵与 KL 散度]]：非概率输出与 surrogate 命名边界；
- [ ] [[f-散度、Bregman 散度与概率度量]]：对称化和 metric 条件；
- [ ] 实验：categorical KL、Bernoulli KL 与 logit surrogate 的曲率比较。

## 交叉验证

- Kullback & Leibler (1951)：相对信息的正式定义；
- MIT 6.441 / Stanford EE376A：KL、绝对连续与 Gibbs inequality；
- 具体 GlobalPointer/R-Drop 实验结论需由原始实现和数据协议另行复核。
