---
type: source
status: verified
area: [sources, ai/transformers, ai/text-to-text]
source_type: paper
title: "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"
author: "Colin Raffel et al."
year: 2020
url: "https://www.jmlr.org/papers/v21/20-074.html"
accessed: 2026-08-26
source_tier: A
license: "JMLR paper; independent summary only"
scope_role: core
temporal_role: encoder-decoder-unification
related: ["[[Encoder–Decoder 与 Cross-Attention]]", "[[Decoder-Only、Prefix 与架构家族比较]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
created: 2026-08-24
updated: 2026-08-26
---

# T5：统一 Text-to-Text 的 Encoder–Decoder

> [!abstract] 来源定位
> T5 把多类文本任务统一成 text-to-text，并系统比较预训练目标、架构、数据与迁移方式。课程用它展示 encoder–decoder 如何把双向 source representation 与 causal target generation 组合；实验优劣只在论文控制变量和数据协议内成立。

## 架构接口

- encoder：source 内双向 self-attention；
- decoder：target 内 causal self-attention；
- cross-attention：每个 target query 读取 encoder memory；
- 输出：自回归 text sequence；
- T5 还采用相对位置 bias、pre-norm 风格等具体选择，不能把所有 encoder–decoder 都称为同一实现。

## 课程边界

“所有任务表示为文本”是接口统一，不表示任务损失、评价或信息结构完全相同。架构比较必须对齐参数、训练 token、objective、输入/输出长度和解码成本。
