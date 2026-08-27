---
type: source
status: verified
area: [sources, language-models, sampling]
source_type: paper
title: "Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs"
author: "Minh Nguyen et al."
year: 2024
url: "https://arxiv.org/abs/2407.01082"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: min-p-definition
related: ["[[Top-k、Top-p、Typical 与 Min-p 截断采样]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Min-p：相对最大 token 概率的动态阈值

> [!abstract] 来源定位
> Min-p 保留满足 $p(v)\ge \alpha p_{\max}$ 的 token，再重归一化。课程采用相对阈值定义和高/低置信分布下候选集变化，不把论文的质量优势主张视为已普遍复现。

参数 $\alpha$、temperature、处理器顺序和实现细节共同决定最终集合。
