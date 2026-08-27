---
type: source
status: verified
area: [sources, peft, ia3]
source_type: paper
title: "Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning"
author: "Haokun Liu et al."
year: 2022
url: "https://arxiv.org/abs/2205.05638"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS paper; independent summary"
scope_role: ia3-definition
temporal_role: foundational-method
related: ["[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
created: 2026-08-26
updated: 2026-08-26
---

# IA3 与 T-Few

> [!abstract] 来源定位
> 论文提出以学习向量缩放 key、value 或 feed-forward 激活的 IA3，并在少样本协议中比较 PEFT 与 ICL。课程调用逐通道乘法、参数量和 mixed-task serving 的方法定义。

“better and cheaper”绑定模型、RAFT/任务、示例数、训练与推理调用次数；比较成本必须摊销训练、重复推理与存储，而不是只数 trainable parameters。

