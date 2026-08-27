---
type: source
status: draft
area: [sources, architecture/gnn, weisfeiler-leman]
source_type: paper
title: "Weisfeiler and Leman Go Neural: Higher-Order Graph Neural Networks"
author: "Christopher Morris, Martin Ritzert, Matthias Fey, William L. Hamilton, Jan Eric Lenssen, Gaurav Rattan, Martin Grohe"
year: 2019
url: "https://ojs.aaai.org/index.php/AAAI/article/view/4384"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[WL 表达界、反例与 GNN 证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Morris 等：WL 与高阶 GNN

> [!abstract] 来源定位
> 从理论上连接标准 GNN 与 1-WL/color refinement，并提出使用节点元组的高阶 k-GNN 路线。

## 边界

- 1-WL 失败意味着相应局部聚合器无法靠训练恢复被表示类抹去的差异；
- higher-order 方法提高表达力也显著提高时间和内存；
- “同样表达力”的精确范围依 GNN 定义、初始化标签与 readout 条件。

