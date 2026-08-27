---
type: source
status: verified
area: [sources, optimization, muon, scaling, distributed-training]
source_type: paper
title: "Muon is Scalable for LLM Training"
author: [Jingyuan Liu, Jianlin Su, Xingcheng Yao, Zhejun Jiang, Guokun Lai, Yulun Du, Yidao Qin, Weixin Xu, Enzhe Lu, Junjie Yan, Yanru Chen, Huabin Zheng, Yibo Liu, Shaowei Liu, Bohong Yin, Weiran He, Han Zhu, Yuzhi Wang, Jianzhou Wang, Mengnan Dong, Zheng Zhang, Yongsheng Kang, Hao Zhang, Xinran Xu, Yutao Zhang, Yuxin Wu, Xinyu Zhou, Zhilin Yang]
year: 2025
url: "https://arxiv.org/abs/2502.16982"
code: "https://github.com/MoonshotAI/Moonlight"
accessed: 2026-08-26
source_tier: B
scope_role: large-scale-primary-evidence
temporal_role: current-scaling-reference
related: ["[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
---

# S-2025 Liu et al. - Muon is Scalable

## 核心贡献

- 把 weight decay 与 per-parameter update-scale adjustment 作为扩展 Muon 的关键合同；
- 报告 compute-optimal scaling 实验以及 3B/16B MoE、5.7T tokens 的 Moonlight 训练；
- 提供分布式实现和模型/checkpoint 资源。

## 采用边界

“约 2× compute efficiency”只按论文的拟合、模型族、训练预算和 baseline 协议引用。外部模型表存在数据、架构和训练配方混杂；不能作为单因素 optimizer 因果证据。
