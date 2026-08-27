---
type: exercise
status: draft
area: [architecture, moe, routing]
topic: "[[Router、Gate、Top-k 与稀疏组合]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Router、Gate、Top-k 与稀疏组合]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Router、Gate、Top-k 与稀疏组合

## A. 识别与复述

### ARCH-ROUTER-A01
列出完整路由合同中至少七个必须声明的接口。

### ARCH-ROUTER-A02
区分 score activation、selection 与 selected-weight normalization。

### ARCH-ROUTER-A03
说明严格单调 score 变换保持什么、不保持什么。

## B. 手算与建模

### ARCH-ROUTER-B01
对 $z=[2,1,-1]$ 计算三分类 softmax，再取 Top-2 并 Re-Norm。

### ARCH-ROUTER-B02
若两个选中专家输出为 $[4,-1]$，分别计算 Re-Norm 与不 Re-Norm 的 mixture 输出。

### ARCH-ROUTER-B03
对 $z=[0,0,0]$、$k=2$，列出至少两种合法 tie-break 及其复现影响。

## C. 推导与证明

### ARCH-ROUTER-C01
证明“全局 softmax 后取 Top-k 再 Re-Norm”等价于只在选中 logits 上 softmax。

### ARCH-ROUTER-C02
证明 Top-1 Re-Norm 后选中 gate 恒为 1，并求普通权重路径导数。

### ARCH-ROUTER-C03
说明 hard Top-k 为何几乎处处分段常数，并指出边界在哪里。

## D. 边界、反例与纠错

### ARCH-ROUTER-D01
反驳：“Softmax 与 Sigmoid 排名相同，所以两种 Router 完全等价。”

### ARCH-ROUTER-D02
给出 Router 在 Top-1 Re-Norm 下仍能更新的三条可能路径。

### ARCH-ROUTER-D03
解释训练时加 noisy gating、推理时去噪为何需要单独审计。

## E. AI 迁移

### ARCH-ROUTER-E01
为一个 MoE 实现设计 forward contract 单元测试。

### ARCH-ROUTER-E02
设计 Softmax/Sigmoid × Re-Norm on/off 的因子实验。

### ARCH-ROUTER-E03
写出审查论文中“Top-k routing”可复现性的提问清单。

## 解答入口

[[解答 - Router、Gate、Top-k 与稀疏组合]]

