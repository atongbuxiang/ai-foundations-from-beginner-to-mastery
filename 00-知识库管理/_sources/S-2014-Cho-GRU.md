---
type: source
status: draft
area: [sources, architecture/rnn, memory]
source_type: paper
title: "Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation"
author: "Kyunghyun Cho et al."
year: 2014
url: "https://aclanthology.org/D14-1179/"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[GRU、门控递推与 RNN 结构比较]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation

> [!abstract] 来源定位
> 该论文引入常称为 GRU 的 gated hidden unit。课程采用其 update/reset 思路，并专门标出不同论文和框架对 $z_t$ 的“保留旧状态”或“写入新候选”命名相反，比较时以显式方程为准。

## 课程采用的断言

- update gate 在旧状态与候选状态间逐维插值；
- reset gate 改变生成候选时可见的旧状态；
- GRU 没有与 hidden state 分离的 cell state，参数和状态接口通常比 LSTM 紧凑；
- 结构差异不自动推出任何数据集上的优劣。

## 实现审计

核对 `reset-before` / `reset-after`、bias 切分、gate 排列、候选激活和 update convention。仅凭“GRU”名称不能保证逐元素数值相同。

