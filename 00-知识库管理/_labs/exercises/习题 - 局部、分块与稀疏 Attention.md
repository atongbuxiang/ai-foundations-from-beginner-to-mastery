---
type: exercise
status: draft
area: [architecture, efficient-attention, sparse-attention, graph]
topic: "[[局部、分块与稀疏 Attention]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 局部、分块与稀疏 Attention]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 局部、分块与稀疏 Attention

## A. 识别与复述

### ARCH-SPARSE-A01
把稀疏 attention 写成有向 relation graph，并说明 query 行的邻域 $\mathcal N(i)$ 如何进入 softmax 分母。

### ARCH-SPARSE-A02
区分 local、dilated、block-sparse、global-token 与 random-edge 五类 pattern 的主要目的。

### ARCH-SPARSE-A03
为什么“dense scores 加 $-\infty$ mask”是功能稀疏，却未必是系统稀疏？

## B. 手算与建模

### ARCH-SPARSE-B01
长度 $n=12$，双向 local radius $r=2$。写出 token 0、5、11 的邻域，并计算全部有向边的精确数量。

### ARCH-SPARSE-B02
对 causal local window $w=4$、长度 $n=10$，计算总可见边数 $\sum_i|\mathcal N(i)|$。

### ARCH-SPARSE-B03
长度 16，以 4 为 block size。若每个 query block 只看自身与前一 block，画出 block adjacency，并数出实际 token-pair 上界。

## C. 推导与证明

### ARCH-SPARSE-C01
证明无 dilation 的一维 local radius $r$ 经过 $L$ 层后，内部 token 的最远信息传播距离至多为 $Lr$。

### ARCH-SPARSE-C02
在每个普通 token 都能读写一个 global token 的双向图中，证明任意两普通 token 的图距离至多为 2；说明这不等于无损传递全部信息。

### ARCH-SPARSE-C03
证明 sparse softmax 必须在可见邻域内重新归一化；直接从 dense softmax 删除不可见项而不重归一化一般不是同一算子。

## D. 边界、反例与纠错

### ARCH-SPARSE-D01
构造两个 sparse patterns：边数相同但图直径显著不同，说明只比较 edge count 不够。

### ARCH-SPARSE-D02
给出一个 causal block mask 的未来泄漏反例，并指出单看 block shape 为什么抓不到它。

### ARCH-SPARSE-D03
反驳：“稀疏 attention 有 $O(nw)$ 条边，因此任何 GPU 上都比 dense attention 快。”

## E. AI 迁移

### ARCH-SPARSE-E01
为长文档问答设计一个 local+global pattern，并说明 global token 选择、路径证书与失败任务。

### ARCH-SPARSE-E02
写一个 sparse kernel 正确性测试：应怎样与 dense masked reference 比较，覆盖哪些 padding、packing 与 causal 边界？

### ARCH-SPARSE-E03
设计公平比较 Longformer/BigBird 类 sparse pattern 与 dense baseline 的协议，明确控制变量与报告项。

## 解答入口

[[解答 - 局部、分块与稀疏 Attention]]
