---
type: source
status: draft
area: [sources, ai/attention, ai/efficient-transformers]
source_type: blog
title: "Transformer升级之路：3、从Performer到线性Attention"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8338"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、短公式与链接"
scope_role: bridge
temporal_role: modern-exposition
related: ["[[Attention 的几何、核与概率视角]]", "[[S-2021-Choromanski-Performer]]", "[[S-2021-Su-8601-无限维线性Attention与核特征]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 从 Performer 到线性 Attention

> [!abstract] 来源定位
> 文章沿正随机特征、一般非负 feature map 和矩阵结合律，把 Performer 放进线性 Attention 的统一问题链。课程采用其中文推导直觉；随机特征保证、误差界与系统结论回到 Performer 原论文和版本化实验。

## 核心桥接式

$$
o_i=
\frac{\sum_j\phi(q_i)^\top\varphi(k_j)v_j}
{\sum_j\phi(q_i)^\top\varphi(k_j)}
=
\frac{\phi(q_i)^\top\left(\sum_j\varphi(k_j)v_j^\top\right)}
{\phi(q_i)^\top\left(\sum_j\varphi(k_j)\right)}.
$$

前式说明对象，后式说明可重排计算。$\phi,\varphi$ 的非负性有助于保持 normalized weights 的概率语义；但近似 softmax 的质量还依赖 feature dimension、输入范数、随机性和分母稳定性。

## 证据边界

- `I`：在分母非零且 feature pairing 已定义时，结合律重排精确；
- `T`：Performer 的随机特征性质由原论文承担；
- `E/H`：哪种 activation/feature 最好、稀疏性是否充分，需按任务实验判断；
- 不能从渐近 $O(T)$ 直接推出现代硬件 wall-clock 优势。
