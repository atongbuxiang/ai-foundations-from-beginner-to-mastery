---
type: source
status: draft
area: [sources, architecture/gnn, message-passing]
source_type: paper
title: "Neural Message Passing for Quantum Chemistry"
author: "Justin Gilmer, Samuel S. Schoenholz, Patrick F. Riley, Oriol Vinyals, George E. Dahl"
year: 2017
url: "https://proceedings.mlr.press/v70/gilmer17a.html"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[消息传递神经网络的统一形式]]", "[[图级读出、异构图与任务接口]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Gilmer 等：MPNN

> [!abstract] 来源定位
> 将多个分子图模型统一为 message、sum aggregation、update 与 graph readout 框架，是本课程 MPNN 抽象的主要来源。

## 课程采用的断言

$$
m_v^{t+1}=\sum_{w\in\mathcal N(v)}M_t(h_v^t,h_w^t,e_{vw}),\qquad
h_v^{t+1}=U_t(h_v^t,m_v^{t+1}).
$$

邻居顺序不应进入结果；但有向边、edge type、自环、并行更新和 readout 必须另行声明。论文的量子化学设置不是所有图任务的默认评测合同。

