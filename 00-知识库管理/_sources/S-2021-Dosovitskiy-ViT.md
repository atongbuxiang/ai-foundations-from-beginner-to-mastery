---
type: source
status: draft
area: [sources, ai/vision-transformers, ai/image-modeling]
source_type: paper
title: "An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale"
author: "Alexey Dosovitskiy et al."
year: 2021
url: "https://openreview.net/forum?id=YicbFdNTTy"
accessed: 2026-08-24
source_tier: A
license: "OpenReview/ICLR paper; independent summary only"
scope_role: foundational
temporal_role: vision-transformer
related: ["[[Vision Transformer、Patch Token 与二维结构]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Vision Transformer：图像 Patch 序列化

> [!abstract] 来源定位
> ViT 把图像切成固定大小 patches，将每个 patch 线性投影成 token，加入位置表示与 class token，再交给标准 Transformer encoder。课程用它推导 patchification 的 shape、token 数与二次 attention 成本；效果声明保留预训练数据、分辨率和迁移设置。

## Shape 主线

对 $H\times W\times C$ 图像与 $P\times P$ patch（整除情形），

$$
N=\frac HP\frac WP,
\qquad x_p\in\mathbb R^{N\times(P^2C)},
\qquad X=x_pE\in\mathbb R^{N\times d}.
$$

加入 class token 后序列长 $T=N+1$。Patch embedding 可等价实现为 kernel/stride 都为 $P$ 的卷积；这不等于 ViT 继承 CNN 的局部共享混合归纳偏置。

## 边界

- patch size 改变 token 数、细节与 $T^2$ 成本；
- 分辨率变化常需 position 处理；
- class token 是读出设计，不是唯一选择；
- 原论文的大数据预训练优势不能外推任意小数据与训练预算。
