---
type: source
status: verified
area: [sources, generative-models, evaluation, frechet-loss]
source_type: paper
title: "Representation Fréchet Loss for Visual Generation"
author: "Jiawei Yang; Zhengyang Geng; Xuan Ju; Yonglong Tian; Yue Wang"
year: 2026
url: "https://arxiv.org/abs/2604.28190"
accessed: 2026-08-25
source_tier: A
scope_role: frontier
temporal_role: current-research
related: ["[[生成模型实验协议、FD Loss 与前沿证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Yang et al.：Representation Fréchet Loss

> [!abstract] 来源定位
> 2026 预印本把 FD 的统计 population（如数万样本）与反向 batch 解耦，使 representation-space FD 可作为 post-training objective，并提出多表示评价。课程采用算法思想与报告结果，但把它标为当前前沿，不当作已稳定跨任务复现的标准。

关键边界：优化某一 encoder 的 FD 会直接对该 representation 施加激励；论文也报告 Inception FID 可能误排现代表示下的视觉质量。因此训练 encoder、selection encoder、held-out encoder 与人评必须分开。
