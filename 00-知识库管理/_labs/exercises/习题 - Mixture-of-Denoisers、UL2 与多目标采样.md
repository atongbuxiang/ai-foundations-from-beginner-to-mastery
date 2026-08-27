---
type: exercise
status: verified
area: [language-models, mixture-objectives, ul2]
topic: "[[Mixture-of-Denoisers、UL2 与多目标采样]]"
solution: "[[解答 - Mixture-of-Denoisers、UL2 与多目标采样]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Mixture-of-Denoisers、UL2 与多目标采样

## A. 识别与复述

### LM14-A01
写出 mode→corruption→loss 的层级生成过程。

### LM14-A02
区分 sample、target-token、compute 与 gradient share。

### LM14-A03
用谨慎语言描述 UL2 的 R、S、X denoiser。

## B. 手算与构造

### LM14-B01
R/X 各抽 50 个样本，平均 target 长度 20/80；算 sample share 与 target-token share。

### LM14-B02
$R_R=1.0,R_X=2.0,\pi=(0.7,0.3)$，算总体风险；若交换概率再算。

### LM14-B03
目标权重 $w=(0.5,0.5)$，proposal $r=(0.8,0.2)$；写两种 mode 的重要性权重。

## C. 推导与证明

### LM14-C01
证明按 $\pi$ 抽 mode 的单样本梯度对加权总体梯度无偏。

### LM14-C02
推导总梯度协方差的 mode 内与 mode 间分解。

### LM14-C03
证明先 per-example mean 与全 target-token mean 通常优化不同风险。

## D. 边界、反例与纠错

### LM14-D01
构造 `1:1:1` mode 概率但梯度贡献极不均衡的例子。

### LM14-D02
反驳“目标种类越多，能力必然单调增加”。

### LM14-D03
指出训练带 mode tag、推理省略 tag 的 distribution mismatch。

## E. AI 迁移

### LM14-E01
设计一张 per-mode 训练日志 schema。

### LM14-E02
给出发现两 mode 梯度冲突的实验，并说明余弦相似度的局限。

### LM14-E03
审计一个只对齐 step 数、不对齐 target tokens/FLOPs 的 UL2 消融。

独立完成后查看[[解答 - Mixture-of-Denoisers、UL2 与多目标采样]]。

