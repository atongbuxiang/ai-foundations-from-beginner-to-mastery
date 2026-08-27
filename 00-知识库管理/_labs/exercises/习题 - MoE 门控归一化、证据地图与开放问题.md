---
type: exercise
status: draft
area: [architecture, moe, gating, evidence]
topic: "[[MoE 门控归一化、证据地图与开放问题]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - MoE 门控归一化、证据地图与开放问题]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - MoE 门控归一化、证据地图与开放问题

## A. 识别与复述

### ARCH-GATE-A01
解释 Softmax simplex 与 Sigmoid 独立 score 的几何差别。

### ARCH-GATE-A02
分别定义 I、T、E、H、O 五级证据。

### ARCH-GATE-A03
说明固定 Hash routing 相对 learned Router 消除了什么、牺牲了什么。

## B. 手算与建模

### ARCH-GATE-B01
对 $z=[1,0]$ 计算 Softmax 与 Sigmoid score，并比较总和。

### ARCH-GATE-B02
对任意正 score $[a,b,c]$ 做 Top-1 Re-Norm，求选中权重与普通导数。

### ARCH-GATE-B03
总 token 数 $N=1000,E=10$，某 token 出现 180 次且固定映射单专家。证明完美均衡不可行并给出最大负载下界。

## C. 推导与证明

### ARCH-GATE-C01
证明严格单调变换在无 tie 时保持 Top-k index。

### ARCH-GATE-C02
推导 Softmax Jacobian，并与 Sigmoid 的对角 Jacobian 比较耦合。

### ARCH-GATE-C03
说明选中后 Re-Norm 在 $k=E$、$k=1$ 两端分别退化为什么。

## D. 边界、反例与纠错

### ARCH-GATE-D01
把“共享专家学习公共知识”正确改写为可证伪假说。

### ARCH-GATE-D02
解释为何近期整体系开发报告不能证明单个组件因果收益。

### ARCH-GATE-D03
给出一个 selection index 相同但模型输出不同的门控反例。

## E. AI 迁移

### ARCH-GATE-E01
用 I/T/E/H/O 审计一条“Sigmoid gate 更优”的主张。

### ARCH-GATE-E02
设计 learned routing 与 frequency-hash routing 的公平对照。

### ARCH-GATE-E03
从 40.8 开放问题中选一项，写出可在小模型上执行的研究计划。

## 解答入口

[[解答 - MoE 门控归一化、证据地图与开放问题]]

