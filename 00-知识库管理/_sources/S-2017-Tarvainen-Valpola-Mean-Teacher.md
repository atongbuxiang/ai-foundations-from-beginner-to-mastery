---
type: source
status: verified
area: [sources, semi-supervised-learning, consistency, teacher-student]
source_type: paper
title: "Mean Teachers Are Better Role Models: Weight-Averaged Consistency Targets Improve Semi-Supervised Deep Learning Results"
author: [Antti Tarvainen, Harri Valpola]
year: 2017
url: "https://proceedings.neurips.cc/paper/2017/hash/68053af2923e00204c3ca7c6a3150cf7-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and method conditions"
venue: "NeurIPS 2017"
scope_role: primary
temporal_role: modern-foundation
related: ["[[遮蔽预测、Teacher–Student 与自监督目标]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Mean Teachers Are Better Role Models

> [!abstract] 来源定位
> 在半监督学习中以 student weights 的 EMA 生成 teacher prediction，并对随机扰动下输出施加 consistency。本库用它区分 label loss、consistency target、parameter averaging 与 prediction averaging。

## 本库调用

1. labeled 与 unlabeled terms 的 sampling/weight 必须分开；
2. teacher 参数是 student 历史的低通平均；
3. consistency 需要 task-valid perturbations；
4. teacher error 可被 student 继承或放大；
5. EMA 改善是算法证据，不是 teacher 无偏性的证明。
