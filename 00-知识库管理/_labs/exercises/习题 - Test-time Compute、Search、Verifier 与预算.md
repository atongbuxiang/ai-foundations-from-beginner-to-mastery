---
type: exercise
status: verified
area: [language-models, reasoning, search, test-time-compute]
topic: "[[Test-time Compute、Search、Verifier 与预算]]"
solution: "[[解答 - Test-time Compute、Search、Verifier 与预算]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Test-time Compute、Search、Verifier 与预算

## A. 识别与复述

### LM39-A01
列出搜索式推理的七元合同。

### LM39-A02
区分 outcome verifier 与 process verifier。

### LM39-A03
为什么 token、FLOPs、调用数、延迟和显存不能互换？

## B. 手算与构造

### LM39-B01
分支 $b=2$、深度 $d=3$ 的完整树有多少节点？

### LM39-B02
步骤分数 0.9、0.8、0.4；计算 min、product 与 log-sum 的排序信息。

### LM39-B03
构造同 token 总量但串行深度不同的两种推理方案。

## C. 推导与证明

### LM39-C01
推导完整 $b$ 叉树节点数。

### LM39-C02
写出 proposal、transition、value、queue、pruning、stop 的状态递推。

### LM39-C03
说明自适应预算为何必须用不看真值的难度估计。

## D. 边界、反例与纠错

### LM39-D01
反驳“输出更长等于总 compute 更高且更有效”。

### LM39-D02
构造 verifier 静态准确率高但在搜索中被 exploit 的例子。

### LM39-D03
审计一个小模型加 verifier 与大模型 greedy 但未计 verifier 成本的比较。

## E. AI 迁移

### LM39-E01
设计 greedy/long-CoT/sampling/Best-of-N/search/oracle 六路对照。

### LM39-E02
设计 difficulty-stratified adaptive compute 报告。

### LM39-E03
为 Tree-of-Thought 系统写复现 manifest 与失败日志字段。

独立完成后查看[[解答 - Test-time Compute、Search、Verifier 与预算]]。
