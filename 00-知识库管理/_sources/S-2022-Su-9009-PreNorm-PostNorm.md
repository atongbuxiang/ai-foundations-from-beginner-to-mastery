---
type: source
status: draft
area: [sources, scientific-spaces, neural-networks/normalization, transformers]
source_type: blog
title: "为什么Pre Norm的效果不如Post Norm？"
author: 苏剑林
year: 2022
url: "https://spaces.ac.cn/archives/9009"
accessed: 2026-08-23
source_tier: C
license: "科学空间博客；本库仅保存独立摘要、短公式与链接"
site_category: [信息时代]
scope_role: core
temporal_role: classical-exposition
related: ["[[Pre-Norm、Post-Norm 与归一化放置]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 苏剑林：为什么 Pre-Norm 的效果不如 Post-Norm？

> [!abstract] 来源定位
> 文章把“同一训练设置下 Pre-Norm 往往更容易训练”与“充分调参后某些 Post-Norm 设置最终效果更好”分开，并用 Pre-Norm 残差和的展开提出“深度被稀释”的直觉。本库采用它作为问题入口与解释视角，不把该直觉升级为跨模型定理。

## 文章主线

Pre-Norm 展开为

$$
x_{L}=x_0+\sum_{\ell=0}^{L-1}F_\ell(N(x_\ell)).
$$

若各分支增量规模受控，而 residual stream 随累加变大，则相邻深层状态的相对变化可能变小。文章据此使用“浅而宽/深度有水分”解释某些最终性能差异。

## 断言审计

| ID | 文章断言 | 类型 | 缺少的普遍条件 | 本库处理 |
|---|---|---|---|---|
| SU9009-C1 | Pre-Norm 的恒等路径更突出 | 结构直觉 | 需看 Jacobian、分支尺度 | 用精确 Jacobian 补严 |
| SU9009-C2 | Pre-Norm 更容易训练 | 经验概括 | 架构、初始化、优化器、深度 | 不写成定理 |
| SU9009-C3 | residual sum 导致相对层增量变小 | 渐近直觉 | 增量大小、相关性与 residual growth | 标为有条件解释 |
| SU9009-C4 | Post-Norm 最终效果通常更好 | 经验概括 | 公平调参、任务与预算 | 需逐实验核验 |

## 与正式来源的分工

- Xiong et al. 2020 负责特定 mean-field 初始化下的梯度与 warm-up 分析；
- 一般 residual Jacobian 负责说明 identity path 的结构位置；
- 科学空间文章负责提出“训练容易度不等于最终表达/迁移效果”的中文问题框架；
- 当前节点明确区分恒等式、近似、经验和假说。

## 限制

- $x_L$ 写成分支和是精确的，但“等效变宽而非变深”不是由该恒等式自动推出；
- 相邻状态接近不等于函数复合没有增加表达能力；
- Pre/Post 的公平比较需要分别调学习率、warm-up、初始化和残差尺度；
- 文章中的经验概括不直接覆盖现代全部 LLM。
