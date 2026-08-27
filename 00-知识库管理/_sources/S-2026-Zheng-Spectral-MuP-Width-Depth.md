---
type: source
status: verified
area: [sources, mup, spectral-condition, width-depth-scaling]
source_type: preprint
title: "Spectral Condition for μP under Width-Depth Scaling"
author: [Chenyu Zheng, Rongzhen Wang, Xinyu Zhang, Chongxuan Li]
year: 2026
url: "https://arxiv.org/abs/2603.00541"
accessed: 2026-08-26
source_tier: B
scope_role: frontier-theory-and-evidence
temporal_role: current-frontier
related: ["[[谱条件、高阶 μP 与参数更新稳定性]]", "[[Scale-up 协议、μP 证据与失效边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Width–Depth Scaling 下的谱 μP 条件

> [!abstract] 来源定位
> 该 2026 预印本为 residual networks 的宽度—深度联合扩展提出谱条件，并把它映射到若干 optimizer 的参数化规则；GPT-2 风格实验用于检验稳定 feature learning 与超参数迁移。本卷把它列为前沿扩展，不把它倒灌为原始 μP 对所有深度路径的既有定理。

## 正文采用

- 同时改变宽度 $n$ 与 block depth $L$ 时，必须显式声明联合极限路径；
- 权重和逐步更新的 operator norm 需要同时满足宽度与深度尺度合同；
- residual accumulation、branch scale 与 optimizer update geometry 共同决定 feature change；
- 可以用该谱框架组织 SGD、AdamW 等规则的对照表，但每条都要保留架构与 optimizer 条件。

## 前沿边界

这是访问日仍为预印本的近期结果。课程只把论文内证明与实验限定在其 residual/GPT-2-style 设置；对 MoE、状态空间模型、任意 attention 变体、极深归一化结构与长时训练的外推均记为开放验证。

