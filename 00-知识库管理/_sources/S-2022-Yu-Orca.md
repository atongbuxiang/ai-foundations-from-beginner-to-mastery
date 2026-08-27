---
type: source
status: verified
area: [sources, language-models, serving]
source_type: paper
title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
author: "Gyeong-In Yu et al."
year: 2022
url: "https://www.usenix.org/conference/osdi22/presentation/yu"
accessed: 2026-08-26
source_tier: P1
license: "USENIX open-access paper; independent summary"
scope_role: iteration-level-scheduling
related: ["[[Prefill、Decode、KV Cache 与 Continuous Batching]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Orca：iteration-level scheduling 与 selective batching

> [!abstract] 来源定位
> Orca 针对生成请求的多迭代性质，以 iteration 而非完整 request 为调度粒度，使已完成请求退出、新请求进入，并对部分算子选择性 batching。

论文吞吐数字绑定 GPT-3 175B、硬件和基线；课程采用调度状态机，不复用倍数为通用承诺。
