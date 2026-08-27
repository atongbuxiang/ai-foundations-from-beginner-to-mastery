---
type: source
status: draft
area: [sources, math/calculus, ai/attention, ai/numerical-stability]
source_type: blog
title: "LogSumExp和Softmax的泰勒展开"
author: 苏剑林
year: 2026
url: "https://spaces.ac.cn/archives/11814"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、短公式与链接"
scope_role: bridge
temporal_role: current
related: ["[[Taylor 展开与余项]]", "[[Softmax–Cross-Entropy 的稳定融合反向]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[Attention 的几何、核与概率视角]]"]
created: 2026-08-24
updated: 2026-08-24
---

# LogSumExp 与 Softmax 的 Taylor 展开

> [!abstract] 来源定位
> 文章从 LogSumExp 展开及其梯度关系推导 Softmax 的级数表达，为“局部线性化 attention”提供近期中文入口。课程只使用可逐项核验的展开，并为展开点、收敛/余项、归一化与非负性建立审计。

## 数学入口

$$
\operatorname{LSE}(z)=\log\sum_j e^{z_j},\qquad
\nabla\operatorname{LSE}(z)=\operatorname{softmax}(z).
$$

若对 LSE 在指定展开点作 Taylor 展开，再在合法条件下逐项微分，可得到 softmax 的局部多项式近似。截断多项式一般不会自动保持每项非负、总和为 1 或对大 logit 差稳定。

## 课程边界

- 必须写展开点、阶数、适用邻域和余项；
- softmax 的平移不变性应在近似中单独检查；
- “可展开”不等于低阶截断在全域精确；
- 用于 Attention 时还要传播到 normalized output、mask 与 dtype；
- 2026 年后续架构联想属于 `H/E`，不替代正式算法与实验。

## 已调用

- [x] [[Taylor 展开与余项]]：展开点、余项、概率约束与全域失效边界；
- [x] [[Softmax–Cross-Entropy 的稳定融合反向]]：fused exact identity 与局部多项式替代分账；
- [x] [[Scaled Dot-Product Attention 与 Softmax 数值语义]]：mask、归一化输出与低精度误差接口。
