---
type: source
status: draft
area: [sources, ai/attention, ai/efficient-transformers, math/kernels]
source_type: paper
title: "Rethinking Attention with Performers"
author: "Krzysztof Choromanski et al."
year: 2021
url: "https://openreview.net/forum?id=Ua6zuk0WRH"
accessed: 2026-08-24
source_tier: A
license: "OpenReview paper; independent summary only"
scope_role: core
temporal_role: modern
related: ["[[Attention 的几何、核与概率视角]]", "[[Attention 失效模式、反例与证据地图]]", "[[S-2021-Su-8338-Performer到线性Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Performer：正随机特征近似 Softmax Attention

> [!abstract] 来源定位
> Performer 以 FAVOR+ 正随机特征近似 softmax kernel，从而借矩阵结合律避免显式存储完整 $T\times T$ attention 矩阵。课程把它作为“核近似—复杂度—误差”案例，而不把线性复杂度误写为精确等价或无条件更快。

## 核心结构

若 $\exp(q^\top k)$ 可由 $\phi(q)^\top\phi(k)$ 近似，则

$$
\frac{\sum_j e^{q_i^\top k_j}v_j}{\sum_j e^{q_i^\top k_j}}
\approx
\frac{\phi(q_i)^\top\sum_j\phi(k_j)v_j^\top}
{\phi(q_i)^\top\sum_j\phi(k_j)}.
$$

右式不必显式构造二次规模 affinity；但随机特征维数、归一化分母、causal prefix、dtype 与 kernel implementation 仍决定误差和真实成本。

## 证据边界

| 断言 | 类型 | 边界 |
|---|---|---|
| 正随机特征可无偏/近似表示 softmax kernel | 定理/构造 `T` | 依论文特征构造与采样假设 |
| 结合律可把 token 维二次中间量改成 feature sufficient statistics | 恒等/算法 `I` | 先替换 kernel；复杂度含 feature width |
| 完整 normalized output 与 exact softmax 无误差 | 错误外推 | 分子、分母误差均需控制 |
| 所有长度、硬件与任务上更快更好 | 错误外推 | 需版本化系统与任务实验 `E` |

## 调用

- [[Attention 的几何、核与概率视角]]：指数 dot-product 的 feature-map 视角；
- [[Attention 失效模式、反例与证据地图]]：denominator amplification 与系统证据；
- 后续高效 Attention 专题：FAVOR+、causal prefix sums、memory ledger。
