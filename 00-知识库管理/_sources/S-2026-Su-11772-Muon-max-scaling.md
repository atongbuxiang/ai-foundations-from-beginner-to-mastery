---
type: source
status: verified
area: [sources, optimization, muon, scaling]
source_type: blog
title: "Muon的max scaling与MuP尺度"
author: 苏剑林
year: 2026
url: "https://spaces.ac.cn/archives/11772"
accessed: 2026-08-26
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要与链接"
site_category: [信息时代]
scope_role: current-scaling-analysis
temporal_role: frontier
related: ["[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Muon 的 max scaling 与 MuP 尺度

> [!abstract] 来源定位
> 文章比较当前 Muon 实现中的 shape-dependent scaling 与 MuP 风格宽度缩放，特别关注 `max(1, rows/cols)` 一类截断。由于发表于 2026 年且实现仍在演化，本库将其列为前沿尺度分析，而非定论。

## 核心问题

设权重采用 $xW$ 约定，$W\in\mathbb R^{A\times B}$。精确 partial isometry 的 element RMS 是

$$
\operatorname{RMS}(UV^T)=\sqrt{\frac{r}{AB}}=\frac1{\sqrt{\max(A,B)}}
$$

（满秩时 $r=\min(A,B)$）。因此 `original`、`match_rms_adamw`、`spectral_unclamped` 不是符号改写，而是在匹配不同目标量。

## 采用边界

- 当前 PyTorch `original` 规则按访问日源码记录为 $\sqrt{\max(1,A/B)}$；
- MuP 风格的 $\sqrt{A/B}$ 与上述截断在宽矩阵上不同；
- 文章提出的解释需在固定线性层约定、初始化、宽度极限和 optimizer state 下检验；
- “尺度更合理论证”不自动推出 finite-model quality 更好。

