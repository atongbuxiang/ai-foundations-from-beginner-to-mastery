---
type: source
status: draft
area: [sources, ai/transformers, ai/residual-routing]
source_type: paper
title: "Attention Residuals"
author: "Guangyu Chen, Yu Zhang, Jianlin Su et al. (Kimi Team)"
year: 2026
url: "https://arxiv.org/abs/2603.15031"
accessed: 2026-08-24
source_tier: A
license: "arXiv paper; independent summary only"
scope_role: frontier
temporal_role: current-research
related: ["[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]", "[[S-2026-Su-11664-Attention-Residuals]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Attention Residuals：沿深度的内容依赖聚合

> [!abstract] 来源定位
> AttnRes 把标准 residual stream 对历层输出的固定单位权累加，改成对先前层表示的 softmax depth-attention；Block AttnRes 用块级状态降低存储与流水通信。课程把它作为 2026 年前沿分支，不改写成传统 residual 已被普遍取代。

## 结构对比

标准 residual 递推展开为

$$
x_l=x_0+\sum_{j<l}F_j(x_j),
$$

各历史分支固定权重 1。AttnRes 让层 $l$ 依据当前内容产生对历史层输出的归一化权重，再聚合深度方向 memory。它引入新的：depth keys/queries、history storage、normalizer、pipeline communication 与可解释性问题。

## 证据边界

- 算法定义和固定和/可学习权比较为 `I`；
- 论文 scaling-law、消融及 48B-total/3B-activated、1.4T-token 训练结果为版本化 `E`；
- 对未测架构、任务与更大规模的优势为 `O`；
- depth attention weights 也不自动是因果解释。
