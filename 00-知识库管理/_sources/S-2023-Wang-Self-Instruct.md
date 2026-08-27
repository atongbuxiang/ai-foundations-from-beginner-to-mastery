---
type: source
status: verified
area: [sources, instruction-data, synthetic-data]
source_type: paper
title: "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
author: "Yizhong Wang et al."
year: 2023
url: "https://aclanthology.org/2023.acl-long.754/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: synthetic-instruction-pipeline
temporal_role: foundational-study
related: ["[[指令数据质量、混合、多轮状态与选择偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Self-Instruct

> [!abstract] 来源定位
> Self-Instruct 从种子任务出发生成 instruction/input/output，再过滤无效或相似样本并用于微调。课程调用其生成—过滤—再训练闭环，分析 teacher bias、错误继承、模板集中、去重对象和 selection-on-generator。

论文中的人工评估与性能结果不证明 synthetic data 无偏或可替代所有人类数据；复现需固定生成模型/API、prompt、sampler、过滤器、去重与时间版本。

