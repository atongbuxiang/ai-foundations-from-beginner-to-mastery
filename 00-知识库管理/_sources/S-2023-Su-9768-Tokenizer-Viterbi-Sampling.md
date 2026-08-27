---
type: source
status: verified
area: [sources, scientific-spaces, tokenization, viterbi, sampling]
source_type: blog
title: "基于 Viterbi 的 Tokenizer 随机采样"
author: "苏剑林"
year: 2023
url: "https://spaces.ac.cn/archives/9768"
accessed: 2026-08-26
source_tier: P3
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、短公式与链接"
scope_role: core-exposition
temporal_role: sampling-algorithm
related: ["[[Unigram LM、Viterbi、EM 与 Subword Regularization]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间：Tokenizer 的 Viterbi 随机采样

> [!abstract] 来源定位
> 文章从最优路径动态规划推广到随机分段，为“不能把 Viterbi、局部随机扰动和目标后验采样混写”提供中文推导入口。课程以枚举小 lattice 检查输出路径的经验频率。

## 课程补严

- 明确目标分布是 $q_\alpha(s\mid x)\propto p(s)^\alpha$ 还是另一种扰动分布；
- 每条路径的概率应与 exact enumeration 对齐；
- log-space 动态规划防止长序列下溢；
- 完美采样的进一步讨论见 [9811](https://spaces.ac.cn/archives/9811)，建立独立来源卡前需逐式复核。
