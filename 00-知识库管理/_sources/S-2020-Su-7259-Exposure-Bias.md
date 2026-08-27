---
type: source
status: verified
area: [sources, ai/text-generation, generative-models/autoregressive]
source_type: blog
title: "Seq2Seq中Exposure Bias现象的浅析与对策"
author: 苏剑林
year: 2020
url: "https://spaces.ac.cn/archives/7259"
accessed: 2026-08-25
source_tier: C
license: "CC BY-NC-SA（按站点页脚；本卡仅保存独立摘要、短公式与链接）"
site_category: [信息时代]
scope_role: core
temporal_role: classical-exposition
related: ["[[Teacher Forcing、暴露偏差与生成时分布漂移]]", "[[S-2015-Huszar-Scheduled-Sampling批判]]", "[[S-2018-Su-5861-Seq2Seq与Beam-Search]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Seq2Seq 中 Exposure Bias 现象的浅析与对策

> [!abstract] 来源定位
> 文章从条件链式分解解释 Teacher Forcing，再把训练时真实前缀与生成时模型前缀的分布错配称为 Exposure Bias，并讨论随机替换和对抗扰动。课程采用其中文直觉与问题构造；“错配必然导致性能下降”以及具体缓解策略的普遍有效性不由该文单独承担。

## 核心对象

对条件序列 $Y_{1:T}$ 与输入 $X$，

$$
p_\theta(y_{1:T}\mid x)=\prod_{t=1}^T p_\theta(y_t\mid x,y_{<t}).
$$

Teacher Forcing 的总体 MLE 期望在 $Y_{<t}\sim p_{\mathrm{data}}$ 下计算；自由生成的第 $t$ 步前缀则由模型过去的采样和解码规则共同诱导。二者不同是一个可精确定义的分布事实，但不是“MLE 不一致”的同义词。

## 断言审计

| ID | 断言 | 条件/边界 | 课程判断 |
|---|---|---|---|
| SU7259-C1 | Teacher Forcing 可并行计算各位置条件似然 | 模型允许 masked parallel evaluation | 成立 |
| SU7259-C2 | 训练与 rollout 的前缀分布一般不同 | 模型非完美、自由生成 | 成立 |
| SU7259-C3 | 前一步错误可改变后续条件输入 | 条件模型依赖前缀 | 成立，但误差增长需另证 |
| SU7259-C4 | 随机替换真实 token 可普遍解决 Exposure Bias | estimator、替换率、任务均相关 | 不采用为一般结论 |
| SU7259-C5 | Exposure Bias 是所有生成退化的主因 | 解码、目标、数据、校准亦可能致因 | 不采用 |

## 课程补严

- 区分真实前缀风险、模型前缀风险和最终序列级任务风险；
- 区分“prefix distribution shift”与“模型族/目标的不一致性”；
- 与 [[S-2015-Huszar-Scheduled-Sampling批判]] 对照，说明修复分布错配可能同时改变统计目标；
- 用两步 Bernoulli 反例展示同样的一步错误率可以产生不同 rollout 风险。

## 调用

- [[Teacher Forcing、暴露偏差与生成时分布漂移]]：中文主入口与反例问题；
- [[自回归模型的表达、成本、失效模式与证据地图]]：失效归因的证据边界。

