---
type: source
status: verified
area: [sources, scientific-spaces, language-modeling, proper-scoring]
source_type: blog
title: "除了交叉熵，LM Loss 还有什么选择？"
author: "苏剑林"
year: 2026
url: "https://spaces.ac.cn/archives/11854"
accessed: 2026-08-26
source_tier: P3
license: "科学空间 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: frontier-exposition
temporal_role: current-active
related: ["[[概率语言模型、链式法则与自回归因子化]]", "[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间：LM Loss 与 Proper Scoring Rules

> [!abstract] 来源定位
> 文章从“只有目标分布样本、仍需学习完整分布”出发，把可采样估计的 loss 写为 $\mathbb E_{i\sim p}S(q,i)$，连接 proper scoring rules、凹熵和 Fenchel–Young 结构，并比较 log/Brier/Tsallis/spherical/Rényi scores 的梯度。它是 2026 年前沿推导入口；一般定理需回查 proper scoring/Fenchel–Young 一级文献。

## 课程采用与保留

- 逐 token cross-entropy 是 log score 的 Monte Carlo 样本形式；
- strictly proper 表示 population optimum 在 $q=p$，不等于有限模型/有限优化可恢复真实分布；
- 若 local score 只依赖观测类别概率，在适当正则条件下 log score 有特殊唯一性；约束细节不能省略；
- Brier 等替代 score 的梯度/饱和性质是候选机制，真实 LLM 优劣仍需预算匹配实验；
- 换 loss 后 NLL/PPL 不再是同一训练目标，必须保留 held-out log score 与下游评估。

页面日期：2026-08-09。本文在课程中标为 `P3/H/T?` 混合来源，不能单独承担历史优先权或完整严谨证明。
