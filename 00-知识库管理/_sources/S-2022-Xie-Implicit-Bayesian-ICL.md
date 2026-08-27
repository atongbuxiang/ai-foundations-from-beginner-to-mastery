---
type: source
status: verified
area: [sources, in-context-learning, bayesian-inference]
source_type: paper
title: "An Explanation of In-context Learning as Implicit Bayesian Inference"
author: "Sang Michael Xie et al."
year: 2022
url: "https://arxiv.org/abs/2111.02080"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: theoretical-model
related: ["[[ICL 的 Bayesian、线性回归与元优化解释]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ICL 作为隐式 Bayesian 推断

> [!abstract] 来源定位
> 论文在预训练分布为隐概念 HMM 混合等设定下，把 prompt 视为更新潜概念后验的证据，并在合成 GINC 数据上观察模型行为。课程采用 posterior predictive 的严格分解和“任务识别—任务内推断”区分。

该结果是明确生成模型假设下的解释，不是对任意真实 LLM 内部算法的唯一鉴定；与线性回归、检索或梯度下降解释可能在不同抽象层同时成立。
