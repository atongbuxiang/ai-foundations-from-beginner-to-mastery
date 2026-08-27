---
type: source
status: verified
area: [sources, language-models, degeneration]
source_type: paper
title: "Neural Text Generation with Unlikelihood Training"
author: "Sean Welleck et al."
year: 2020
url: "https://openreview.net/forum?id=SJeYe0NtvH"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: repetition-and-training
related: ["[[EOS、停止规则、重复惩罚与退化循环]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Unlikelihood Training：重复不只属于解码后处理

> [!abstract] 来源定位
> 论文认为标准似然训练可给重复/高频序列过多概率，并以 token/sequence unlikelihood 训练压低负候选。课程用它说明 repetition 可来自模型分布、训练数据、解码与停止的交互。

后处理 repetition penalty 与训练目标不同；降低某种重复也不保证事实、连贯和任务质量同时提高。
