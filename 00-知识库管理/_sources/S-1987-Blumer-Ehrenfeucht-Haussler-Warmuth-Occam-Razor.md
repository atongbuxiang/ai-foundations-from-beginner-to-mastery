---
type: source
status: active
area: [sources, learning-theory, description-length]
source_type: paper
title: "Occam's Razor"
author: "Anselm Blumer, Andrzej Ehrenfeucht, David Haussler, Manfred K. Warmuth"
year: 1987
url: "https://doi.org/10.1016/0020-0190(87)90114-1"
accessed: 2026-08-20
source_tier: A
license: "Publisher-copyrighted article; retain citation, independent derivations and DOI link only"
venue: Information Processing Letters 24(6), 377–380
scope_role: historical-backbone
temporal_role: classical-foundation
related: ["[[Occam 界、编码长度与先验权重]]", "[[PAC 学习定义与样本复杂度]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Occam's Razor

> [!abstract] 来源定位
> Blumer–Ehrenfeucht–Haussler–Warmuth 1987 把“寻找短的一致假设”连接到 Valiant 式可学习性，是 Occam algorithm 的经典历史来源。本库用它解释 compression/description length 为什么能转化为 sample complexity；本节采用的逐假设 weighted Hoeffding 与 prefix-free/Kraft 显式常数由标准教材形式校准，不把原论文的特定 polynomial compression 条件与所有现代 MDL/PAC-Bayes 版本混为一谈。

## 元数据与纳入

- DOI：[10.1016/0020-0190(87)90114-1](https://doi.org/10.1016/0020-0190(87)90114-1)；
- 正式引用：Blumer, A., Ehrenfeucht, A., Haussler, D. & Warmuth, M. K. (1987), *Occam's Razor*, IPL 24(6), 377–380；
- 历史命题：若能多项式时间地产生相对短且与 observations 一致的 hypothesis，可得到 Valiant 意义下的 polynomial learner；
- 当前调用者：[[Occam 界、编码长度与先验权重]]。

## 课程采用与不采用

| 断言 | 判断 |
|---|---|
| 短描述可通过 counting/encoding 降低选择复杂度 | 采用 |
| prefix-free code 给出 $\sum_h2^{-L(h)}\le1$ | 采用，由 Kraft inequality 形式化 |
| 任意压缩文件长度都是客观、坐标无关的模型复杂度 | 否定 |
| “更短必然更真”是无条件定理 | 否定；必须固定语言、sample protocol、loss 与概率命题 |
| Occam bound 与 PAC-Bayes 完全相同 | 否定；二者有 prior/complexity 类比，但对象和证明不同 |

## 已生成与后续调用

- [x] [[Occam 界、编码长度与先验权重]]：weighted union、Kraft、MDL 与 AI compression 边界；
- [ ] [[样本压缩方案与泛化]]：短样本证书而非纯 bit code；
- [ ] [[PAC-Bayes Bound 的测度变换主线]]：从点质量 penalty 推广到 posterior/KL。
