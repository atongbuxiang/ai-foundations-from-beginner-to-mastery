---
type: source
status: verified
area: [sources, generative-models, score-matching, denoising]
source_type: paper
title: "A Connection Between Score Matching and Denoising Autoencoders"
author: "Pascal Vincent"
year: 2011
url: "https://pubmed.ncbi.nlm.nih.gov/21492012/"
venue: "Neural Computation 23(7)"
accessed: 2026-08-25
source_tier: A
license: "论文元数据/摘要；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[去噪 Score Matching、Tweedie 公式与条件期望]]", "[[多噪声尺度、退火去噪与 Score 网络]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Vincent：去噪自编码器与 Score Matching 的连接

> [!abstract] 来源定位
> 论文说明去噪训练可等价为对 Parzen/扰动数据密度进行 score matching，并避免直接计算模型关于输入的二阶导数。课程进一步用条件期望正交分解写出 conditional-score 与 marginal-score 的共同最优解。

## 课程采用的边界

1. 等价对象是指定 corruption kernel 诱导的平滑密度，而非无条件恢复原始奇异密度；
2. 两个平方 loss 通常相差与 predictor 无关的常数，不是逐样本相等；
3. Gaussian corruption 给 $-(\tilde x-x)/\sigma^2$ 解析 conditional score；
4. finite network class、权重、数据和 optimizer 会改变实践差异；
5. “无需二阶导数”是 DSM 计算优势，不表示采样无需 score 导数或 solver。

