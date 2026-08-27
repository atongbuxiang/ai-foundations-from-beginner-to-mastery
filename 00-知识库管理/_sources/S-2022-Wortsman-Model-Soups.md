---
type: source
status: verified
area: [sources, model-merging, weight-averaging]
source_type: paper
title: "Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time"
author: "Mitchell Wortsman et al."
year: 2022
url: "https://proceedings.mlr.press/v162/wortsman22a.html"
accessed: 2026-08-26
source_tier: P1
license: "ICML/PMLR paper; independent summary"
scope_role: same-task-weight-averaging
temporal_role: foundational-method
related: ["[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Model Soups

> [!abstract] 来源定位
> Model soups 对同一预训练起点、不同 fine-tuning hyperparameters 的 checkpoints 做 uniform 或 validation-greedy weight averaging，研究同 basin 条件下的效果。课程用它区分单模型权重平均与输出 ensemble。

平均参数只有在架构、参数语义、坐标对齐且插值路径可用时才有希望；greedy soup 使用 validation 选择，必须计入搜索与选择偏差。

