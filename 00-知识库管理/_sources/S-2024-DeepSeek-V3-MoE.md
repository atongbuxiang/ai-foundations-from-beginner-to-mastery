---
type: source
status: draft
area: [sources, ai/moe, loss-free-balancing, system]
source_type: technical-report
title: "DeepSeek-V3 Technical Report"
author: "DeepSeek-AI"
year: 2024
url: "https://arxiv.org/abs/2412.19437"
accessed: 2026-08-24
source_tier: A
license: "arXiv/project repository; independent summary only"
scope_role: contemporary-system-report
related: ["[[Loss-Free 路由、偏置更新与分配视角]]", "[[细粒度专家、共享专家与动态激活]]", "[[Expert Parallel、All-to-All 与通信成本]]"]
created: 2026-08-24
updated: 2026-08-24
---

# DeepSeek-V3：Auxiliary-Loss-Free Balancing

> [!abstract] 来源定位
> DeepSeek-V3 报告 671B total / 37B activated 参数的 MoE 系统，使用 auxiliary-loss-free load balancing、DeepSeekMoE 与多层系统优化。

## 调用边界

- bias feedback 改 route selection，即便不进 main loss 也会改变优化轨迹；
- 14.8T tokens、H800 hours、稳定训练与 benchmark 都是整模型 `E`，无法隔离单个路由技巧；
- 通信、节点限制路由、冗余 Expert 和 infra 联合决定端到端效率。
