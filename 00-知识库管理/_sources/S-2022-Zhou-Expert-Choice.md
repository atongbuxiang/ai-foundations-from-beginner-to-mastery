---
type: source
status: draft
area: [sources, ai/moe, expert-choice, dynamic-routing]
source_type: paper
title: "Mixture-of-Experts with Expert Choice Routing"
author: "Yanqi Zhou et al."
year: 2022
url: "https://arxiv.org/abs/2202.09368"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: routing-alternative
related: ["[[Router、Gate、Top-k 与稀疏组合]]", "[[细粒度专家、共享专家与动态激活]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Expert Choice：由 Expert 选择 Tokens

> [!abstract] 来源定位
> Expert Choice 反转 token-top-k：每个 Expert 选择固定 bucket 的 tokens，使 Expert 负载受控、每 token 激活 Expert 数可变。

## 调用边界

- 固定 Expert capacity 不保证每 token 至少/至多被选多少，语义与 token-choice 不同；
- 论文的收敛速度和任务优势限定同 compute 协议；
- 训练 routing 与 autoregressive serving/batching 的接口需另行设计。
