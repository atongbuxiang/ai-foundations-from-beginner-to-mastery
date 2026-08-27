---
type: exercise
status: verified
area: [language-models, peft, lora]
topic: "[[LoRA 的低秩更新、初始化、缩放与合并]]"
solution: "[[解答 - LoRA 的低秩更新、初始化、缩放与合并]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - LoRA 的低秩更新、初始化、缩放与合并

## A. 识别与复述

### LM29-A01
写 $W_0,A,B$ 的形状与 LoRA 前向。

### LM29-A02
“低秩的是增量”排除了哪三种误解？

### LM29-A03
区分 LoRA 训练与对 full-update 做截断 SVD。

## B. 手算与构造

### LM29-B01
$m=6,n=4,r=2$，算 full/LoRA 参数与 rank 上界。

### LM29-B02
给 $A=[[1,0],[0,1]],B=[[2,0],[0,3]],s=.5$，算 $\Delta W$ 与 $x=(1,2)$ 的增量输出。

### LM29-B03
给两个 rank-1 adapters，构造其和为 rank 2 的例子。

## C. 推导与证明

### LM29-C01
由 $d\Delta W=s(dB\,A+B\,dA)$ 推导两因子梯度。

### LM29-C02
证明 A random/B=0 时首步只更新 B；双零时卡死。

### LM29-C03
证明精确算术下 merged/unmerged forward 等价。

## D. 边界、反例与纠错

### LM29-D01
反驳“rank 8 唯一确定 LoRA 配方”。

### LM29-D02
说明 $(B,A)$ 的尺度不唯一如何与 weight decay/不同学习率相互作用。

### LM29-D03
反驳“trainable parameters 减少 100 倍，峰值显存与时间也减少 100 倍”。

## E. AI 迁移

### LM29-E01
设计 merge/unmerge equivalence 测试。

### LM29-E02
写可复现 LoRA config 与内存日志。

### LM29-E03
审计只写 rank/alpha、未写 target modules/scale convention 的论文。

独立完成后查看[[解答 - LoRA 的低秩更新、初始化、缩放与合并]]。

