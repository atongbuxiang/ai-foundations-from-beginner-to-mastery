---
type: exercise
status: draft
area: [architecture, graph-neural-networks, expressivity, evidence]
topic: "[[WL 表达界、反例与 GNN 证据地图]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - WL 表达界、反例与 GNN 证据地图]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - WL 表达界、反例与 GNN 证据地图

## A. 识别与复述

### ARCH-WL-A01
写出 1-WL/color refinement 的一轮更新，并说明 hash 的条件。

### ARCH-WL-A02
1-WL 区分两图与未区分两图分别能得出什么结论？

### ARCH-WL-A03
解释“常见 MPNN 不超过 1-WL”与“合条件 GIN 达到 1-WL”的区别。

## B. 手算与建模

### ARCH-WL-B01
对三节点路径从统一初始颜色运行两轮 1-WL，写每类节点的颜色签名。

### ARCH-WL-B02
对 $C_6$ 与 $C_3\sqcup C_3$ 从统一颜色运行两轮，说明为什么 histogram 相同。

### ARCH-WL-B03
若初始颜色加入节点 degree，B02 的结果是否改变？解释。

## C. 推导与证明

### ARCH-WL-C01
用归纳法证明 1-WL 同色节点在标准 MPNN 中保持同表示。

### ARCH-WL-C02
说明 injective aggregation/update/readout 怎样给出达到 1-WL 的充分条件。

### ARCH-WL-C03
分析 k-tuple higher-order 方法的状态数量为何可达 $O(n^k)$。

## D. 边界、反例与纠错

### ARCH-WL-D01
反驳：“1-WL 未区分两图，所以它们同构。”

### ARCH-WL-D02
反驳：“理论表达力更强，所以测试集一定更好。”

### ARCH-WL-D03
说明加入 unique node ID 为什么改变原问题，并可能损害跨图泛化。

## E. AI 迁移

### ARCH-WL-E01
设计一个同时含 WL-easy 与 WL-hard 图对的表达测试集。

### ARCH-WL-E02
为“某模型超越 1-WL”写最小理论与实验核验清单。

### ARCH-WL-E03
把一句“新 GNN 更强”拆成表达、优化、泛化、鲁棒、效率和构图六类可核验断言。

## 解答入口

[[解答 - WL 表达界、反例与 GNN 证据地图]]

