---
type: source
status: verified
area: [sources, experimentation, hyperparameter-tuning, reproducibility]
source_type: official-research-guide
title: "Deep Learning Tuning Playbook"
author: "Godfrey et al., Google Research"
year: 2023
url: "https://github.com/google-research/tuning_playbook"
accessed: 2026-08-26
source_tier: B
scope_role: experimental-workflow
related: ["[[单因素、全因子消融与交互效应]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Google Research：Deep Learning Tuning Playbook

> [!abstract] 来源定位
> 一套把目标、探索、开发、比较和 pipeline 变更组织为科学过程的实践指南。本卷采用其“先写问题与预算，再解释 trial”的工作流，不把经验配方当统计定理。

## 本卷调用

- 区分 exploration、exploitation 与最终确认；
- 为每次 study 保存 search space、sampling rule、trial budget、失败和 selection rule；
- pipeline 变化视为新的实验版本，不能与旧 trial 静默混池；
- 诊断 study 与性能 leaderboard 使用不同成功判据。

## 边界

指南提供研究流程，不替代随机化、置信区间、因果识别或特定任务的功效分析。
