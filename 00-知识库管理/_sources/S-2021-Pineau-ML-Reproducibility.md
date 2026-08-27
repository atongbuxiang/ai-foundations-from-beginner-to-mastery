---
type: source
status: verified
area: [sources, reproducibility, machine-learning, reporting]
source_type: paper
title: "Improving Reproducibility in Machine Learning Research"
author: "Pineau et al."
year: 2021
url: "https://www.jmlr.org/papers/v22/20-303.html"
accessed: 2026-08-26
source_tier: A
venue: JMLR
scope_role: reproducibility-program
related: ["[[训练实验协议、事故记录与因果证据地图]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Pineau 等：改进机器学习研究的可复现性

> [!abstract] 来源定位
> 论文总结代码提交政策、reproducibility checklist 与 challenge 的制度实践。本卷据此把可复现性写成对象、材料和复核过程，而非一句“代码将公开”。

## 本卷调用

- 报 claim、algorithm、data、hyperparameters、compute、randomness 与 uncertainty；
- 区分结果复算、同代码复跑、独立重实现和跨环境复验；
- 记录未成功运行与 selection，而非只发布获胜 artifact；
- 对受限数据/算力给出可替代的小规模 oracle。

## 边界

checklist 提高透明度但不保证结论为真；材料齐全仍需检查 estimand、因果识别和统计功效。
