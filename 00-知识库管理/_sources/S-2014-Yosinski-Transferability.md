---
type: source
status: active
area: [sources, transfer-learning, feature-transfer, fine-tuning]
source_type: paper
title: "How Transferable Are Features in Deep Neural Networks?"
author: [Jason Yosinski, Jeff Clune, Yoshua Bengio, Hod Lipson]
year: 2014
url: "https://proceedings.neurips.cc/paper/2014/hash/532a2f85b6977104bc93f8580abbb330-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and experimental conditions"
venue: "NeurIPS 2014"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Linear Probe、Fine-Tuning 与迁移评估]]", "[[表示学习的任务、表示与下游风险]]"]
created: 2026-08-23
updated: 2026-08-23
---

# How Transferable Are Features in Deep Neural Networks?

> [!abstract] 来源定位
> 实验分离 layer specialization 与 co-adaptation/optimization difficulty，并考察 source–target 距离。本库调用其“冻结层数本身定义干预”的视角，不把单一 CNN/ImageNet 结论当作所有架构的规律。

## 本库调用

1. transferability 随 layer 与 task distance 变化；
2. frozen feature quality 与 fine-tuning optimization 是不同对象；
3. co-adaptation 使截断位置成为 protocol；
4. random initialization baseline 不能省略；
5. pretraining 可能改变优化路径而非只改变可表达函数类。
