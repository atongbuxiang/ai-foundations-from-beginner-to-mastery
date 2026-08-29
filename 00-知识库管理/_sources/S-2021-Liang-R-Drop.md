---
type: source
status: active
area: [sources, neural-networks, r-drop, dropout, consistency-regularization]
source_type: paper
title: "R-Drop: Regularized Dropout for Neural Networks"
author: "Xiaobo Liang; Lijun Wu; Juntao Li; Yue Wang; Qi Meng; Tao Qin; Wei Chen; Min Zhang; Tie-Yan Liu"
year: 2021
url: "https://proceedings.neurips.cc/paper_files/paper/2021/hash/5a66b9200f29ac3fa0ae244cc2a51b39-Abstract.html"
venue: "NeurIPS 2021"
accessed: 2026-08-24
source_tier: A
license: "NeurIPS proceedings paper；本库仅保存独立摘要、必要公式与链接"
scope_role: interaction-case-study
temporal_role: modern-method
related: ["[[网络级正则化的交互、消融与证据地图]]", "[[Dropout 的方差、共适应解释与 Bayesian 边界]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Liang et al.：R-Drop

> [!abstract] 来源定位
> 论文对同一样本做两次独立 Dropout forward，在各自 task loss 之外加入双向 KL consistency。它承担“两个正则部件形成新联合目标”的案例；两个 forward 并非普通 batch duplication，KL 权重、stop-gradient、mask 独立性和 reduction 都需声明。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| RD-C1 | 两个 Dropout predictors 以 symmetric/bidirectional KL 耦合 | 定义 | 同样本、独立 masks、方向/reduction 声明 | 精确 |
| RD-C2 | 目标含 task fit 与 stochastic consistency 两部分 | 代数 | implementation 与系数一致 | 精确 |
| RD-C3 | 两次 forward 自动等价 ensemble training | 概念外推 | 参数共享、KL coupling | 错误 |
| RD-C4 | 原论文多任务效果保证所有设置受益 | 经验外推 | rate、task、budget 依赖 | 不成立 |
