---
type: source
status: verified
area: [sources, ai/long-context, evaluation, synthetic-tasks]
source_type: paper
title: "RULER: What's the Real Context Size of Your Long-Context Language Models?"
author: "Cheng-Ping Hsieh et al."
year: 2024
url: "https://arxiv.org/abs/2404.06654"
accessed: 2026-08-24
source_tier: A
license: "arXiv/NVIDIA; independent summary only"
scope_role: benchmark
temporal_role: long-context-evaluation
related: ["[[位置分辨率、混叠与长度外推评测]]", "[[长上下文利用、Lost-in-the-Middle 与推理证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# RULER：声明窗口与有效窗口分离

> [!abstract] 来源定位
> RULER 通过 retrieval、multi-hop tracing、aggregation 与 question answering 等可控 synthetic tasks，随长度扫描实际可利用能力，而不是把“模型接受 N tokens”当作“有效 N-token context”。

## 课程采用

对每个长度 $T$ 报任务准确率曲线，并扫描 needle 数、位置、干扰、依赖跳数与输出约束；以预注册阈值定义某任务的 effective context，而非给模型一个无条件单值。

## 边界

Synthetic success 不等于真实文档理解；失败也可能来自 prompt、tokenization 或 decoding。需与真实多任务 benchmark、PPL 和干预结合。
