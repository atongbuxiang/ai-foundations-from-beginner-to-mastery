---
type: source
status: verified
area: [sources, generative-models, gan]
source_type: paper
title: "Generative Adversarial Nets"
author: "Ian Goodfellow et al."
year: 2014
url: "https://arxiv.org/abs/1406.2661"
venue: "NeurIPS 2014"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[隐式 Pushforward 分布、生成器与判别博弈]]", "[[原始 GAN、最优判别器与 Jensen–Shannon 散度]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Goodfellow et al.：原始 GAN

> [!abstract] 来源定位
> 原论文定义 generator–discriminator minimax game，并在无限容量、population、固定生成器且判别器达到最优等条件下推导 $D^*(x)=p_*(x)/(p_*(x)+p_g(x))$ 与 JS 目标。课程把这一定理与有限网络、交替 SGD、non-saturating surrogate 严格分开。

## 断言审计

| 断言 | 类型 | 条件/边界 | 课程判断 |
|---|---|---|---|
| 生成器将简单噪声 pushforward 成隐式分布 | 定义 | 可采样，不要求可算密度 | 精确 |
| 固定 $G$ 的 population 最优判别器有 density-ratio 闭式 | 定理 | 共同支配测度、逐点自由优化 | 精确 |
| 代回 minimax value 得 $-\log4+2JS(P_*\|P_g)$ | 定理 | 判别器确达最优 | 精确 |
| 实际交替 SGD 在一般神经网络中收敛到该解 | 工程外推 | 非凸非凹、有限数据/步数 | 原论文定理不覆盖 |

