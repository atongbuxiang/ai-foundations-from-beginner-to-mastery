---
type: source
status: active
area: [sources, self-distillation, vision-transformer, teacher-student]
source_type: paper
title: "Emerging Properties in Self-Supervised Vision Transformers"
author: [Mathilde Caron, Hugo Touvron, Ishan Misra, Hervé Jégou, Julien Mairal, Piotr Bojanowski, Armand Joulin]
year: 2021
url: "https://openaccess.thecvf.com/content/ICCV2021/html/Caron_Emerging_Properties_in_Self-Supervised_Vision_Transformers_ICCV_2021_paper.html"
accessed: 2026-08-23
source_tier: A
license: "CVF open access; retain citation and method conditions"
venue: "ICCV 2021"
scope_role: primary
temporal_role: modern-method
related: ["[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Emerging Properties in Self-Supervised Vision Transformers

> [!abstract] 来源定位
> DINO 以 EMA teacher、student cross-entropy、centering、sharpening 与 multi-crop 构成无标签 self-distillation。本库把这些全部视为 target-generation contract，而不把 attention map 的语义现象写成一般定理。

## 本库调用

1. teacher target 是随训练变化的 distribution；
2. teacher temperature 控制 target entropy；
3. centering 与 sharpening 分别针对不同 collapse mode；
4. multi-crop 定义哪些 view pairs 被匹配；
5. EMA target 不是独立 ground truth。
