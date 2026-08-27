---
type: source
status: verified
area: [sources, privacy, membership-inference, statistics]
source_type: paper
title: "Membership Inference Attacks From First Principles"
author: "Nicholas Carlini et al."
year: 2022
url: "https://arxiv.org/abs/2112.03570"
accessed: 2026-08-26
source_tier: P1
license: "IEEE S&P paper; independent summary"
scope_role: low-fpr-membership-evaluation
related: ["[[Membership、隐私攻击、数据删除与 Unlearning 边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# LiRA 与低 FPR 成员推断

> [!abstract] 来源定位
> 论文从似然比检验出发构造成员推断，并强调隐私审计关心极低 FPR 下的 TPR，而非只看平均准确率或 AUC。课程据此推导 in/out score distribution 与 Neyman–Pearson 视角。

攻击性能依参考模型、目标记录和训练随机性；低 FPR 区域样本稀少，必须给分母和区间。
