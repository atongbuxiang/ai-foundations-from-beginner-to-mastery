---
type: source
status: verified
area: [sources, optimization, large-batch, generalization]
source_type: paper
title: "Train Longer, Generalize Better: Closing the Generalization Gap in Large Batch Training of Neural Networks"
author: [Elad Hoffer, Itay Hubara, Daniel Soudry]
year: 2017
url: "https://papers.neurips.cc/paper_files/paper/2017/hash/a5e0ff62be0b08456fc7f1e88812af3d-Abstract.html"
accessed: 2026-08-26
source_tier: A
venue: "NeurIPS 2017"
scope_role: primary
related: ["[[Critical Batch、隐式偏置与 SGD 证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Hoffer、Hubara、Soudry 2017：大批量比较中的 update-budget 混杂

> [!abstract] 来源定位
> 论文提出 large-batch gap 可能主要来自较少的 parameter updates，并在若干视觉任务上通过调整训练长度和 Ghost Batch Normalization 缩小/关闭 gap。课程用它提醒：固定 epoch 并不等于固定 step，也不等于 compute-matched 因果比较。

## 课程调用

- 区分 epoch、examples、optimizer steps、FLOPs 与 wall time；
- 把 BatchNorm statistics 视为独立于 optimizer batch 的实验变量；
- 说明单篇实证不能把 batch size 的总效应分解为噪声、步数、归一化与调度的各自因果效应。

