---
type: exercise
status: draft
area: [architecture, attention, evidence]
topic: "[[Attention 失效模式、反例与证据地图]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Attention 失效模式、反例与证据地图]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Attention 失效模式、反例与证据地图

## A. 识别与复述

### ARCH-EVID-A01
列出 I/T/E/H/O 五级证据，并各给一个 Attention 示例。

### ARCH-EVID-A02
把“低 entropy”分别解释为症状、可能机制和不能推出的结论。

### ARCH-EVID-A03
区分内部读取描述、局部敏感性、反事实忠实性与人类语义解释。

## B. 手算与建模

### ARCH-EVID-B01
构造两组不同 attention weights 因相同 values 给同一输出，并说明其解释意义。

### ARCH-EVID-B02
某模型训练长 512，测试 1024/2048/4096 的 loss 分别为 2.1/2.3/3.0，而 key normalization 版本为 2.0/2.1/2.5。写出可以与不可以得出的结论。

### ARCH-EVID-B03
一次 head zeroing 只降 0.1% accuracy，但联合剪 80% 降 8%。说明单头与联合效应。

## C. 推导与证明

### ARCH-EVID-C01
解释为何 computational path length=1 不推出远程信息可恢复，给出 value/weight 反例。

### ARCH-EVID-C02
把 pure-attention rank-collapse 与 Transformer universal approximation 的假设和结论并列，说明不矛盾。

### ARCH-EVID-C03
说明为何渐近 $O(T)$ 方法可能在有限 T 比 $O(T^2)$ kernel 更慢，并写 crossover 不等式。

## D. 边界、反例与纠错

### ARCH-EVID-D01
反驳：“Attention is not Explanation 已证明所有 attention 可视化都无价值。”

### ARCH-EVID-D02
反驳：“很多 heads 可剪，所以训练时一个 head 足够。”

### ARCH-EVID-D03
反驳：“小模型从 512 外推到 4096 有效，所以更大 LLM 也必有效。”

## E. AI 迁移

### ARCH-EVID-E01
为“新 Attention 更快且同等质量”填写完整 evidence card 与否证实验。

### ARCH-EVID-E02
设计 attention explanation 的反事实测试，控制 values、后续层与替代权重。

### ARCH-EVID-E03
为一次长度外推失败建立症状—测量—干预—证据等级流水线。

## 解答入口

[[解答 - Attention 失效模式、反例与证据地图]]
