---
type: source
status: verified
area: [sources, sequence-packing, attention-mask, efficiency]
source_type: paper
title: "Efficient Sequence Packing without Cross-contamination"
author: "Mario Michael Krell, Matej Kosec, Sergio P. Perez, Andrew Fitzgibbon"
year: 2021
url: "https://arxiv.org/abs/2107.02027"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: packing-algorithms
temporal_role: systems-foundation
related: ["[[Packing、文档边界、Position ID 与 Loss Mask]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Efficient Sequence Packing without Cross-contamination

> [!abstract] 来源定位
> 论文把变长序列 packing 表述为 bin packing，并通过 attention/position 等调整追求与未 pack 样本的数学等价。课程用它区分“减少 padding 的装箱算法”与“防跨样本信息/目标污染的模型合同”。

吞吐增益绑定长度分布、硬件、kernel 和 batch；packing efficiency 高不保证 wall time 等比例提升，也不允许省略 relation 与 loss 边界测试。

