---
type: source
status: verified
area: [sources, language-models, prompt-sensitivity, robustness]
source_type: paper
title: "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design"
author: "Melanie Sclar et al."
year: 2024
url: "https://proceedings.iclr.cc/paper_files/paper/2024/hash/6c0e99d736da621403018ca7b32b1a4d-Abstract-Conference.html"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: prompt-format-robustness
related: ["[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Prompt Formatting Sensitivity：不应相关的设计特征

> [!abstract] 来源定位
> 论文系统改变分隔符、空白、选项格式等不应改变任务含义的 prompt 特征，量化语言模型表现波动。本库据此把 prompt 视为采样因子，而不是挑一个最佳模板后隐藏选择过程。

> [!check] 标识说明
> OpenReview 的搜索与引文页面曾暴露不一致的论坛标识；这里改用 ICLR 2024 官方 proceedings 的稳定论文页，并以标题、作者和 arXiv:2310.11324 交叉核对。

格式敏感度依模型、任务、模板族和 decoding；多模板均值、worst-case 与方差回答不同 estimand，不能以一次最优 prompt 代表稳健能力。
