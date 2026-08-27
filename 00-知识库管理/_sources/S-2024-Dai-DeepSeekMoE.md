---
type: source
status: draft
area: [sources, ai/moe, fine-grained-experts, shared-experts]
source_type: paper
title: "DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models"
author: "Damai Dai et al."
year: 2024
url: "https://arxiv.org/abs/2401.06066"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: architecture-paper
related: ["[[细粒度专家、共享专家与动态激活]]", "[[条件计算、专家混合与稀疏激活]]"]
created: 2026-08-24
updated: 2026-08-24
---

# DeepSeekMoE：Fine-Grained 与 Shared Experts

> [!abstract] 来源定位
> DeepSeekMoE 将 N 个 Experts 细分成 mN、相应激活 mK，并隔离 shared Experts，目标是增加组合灵活性、承接共同知识和减少 routed redundancy。

## 调用边界

- 总参数、激活参数与 Expert MAC 可精确分账；“专门化”需实验指标而非由拆分定义推出；
- 2B/16B/145B 比较是具体训练配置的 `E`；
- shared/fine-grained 与 routing/balance/system kernel 交互，不能只按理论 MAC 断言收益。
