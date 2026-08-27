---
type: exercise
status: draft
area: [generative-models, vae, gaussian]
topic: "[[Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - Gaussian VAE 的闭式 KL、解码似然与尺度合同

## A. 识别与复述

### GEN12-A01
写出 diagonal Gaussian encoder 的均值、log-variance、采样式与标准正态 KL。

### GEN12-A02
MSE 对应什么 observation likelihood？哪些常数在何种条件下可省？

### GEN12-A03
解释 Bernoulli BCE、256-way categorical 与连续 Gaussian density 的数据合同差异。

## B. 手算与建模

### GEN12-B01
$\mu=(1,-1),\log\sigma^2=(0,\log4)$，计算 KL。

### GEN12-B02
$D=100,\tau^2=.5$，mean MSE 为 $.02$。求 Gaussian NLL 的平方误差项及含常数的总 NLL。

### GEN12-B03
二值向量 $x=(1,0)$、decoder 概率 $(.8,.3)$，计算 BCE/NLL。

## C. 推导与证明

### GEN12-C01
从 density ratio 独立推导一维 Gaussian 到标准正态的 KL。

### GEN12-C02
推导固定方差 isotropic Gaussian decoder 的 NLL，并转换为 mean MSE 系数。

### GEN12-C03
证明 $u-\log u-1\ge0$，由此说明 Gaussian KL 非负与等号条件。

## D. 边界、反例与纠错

### GEN12-D01
构造两份都写 $\beta=1$、但因 sum/mean 而有效 KL 权重差 $D$ 倍的实现。

### GEN12-D02
反驳“对 $[0,1]$ 灰度用 BCE 就定义了连续数据密度”。

### GEN12-D03
说明学习 decoder variance 时删除 log-variance 项会导致怎样的退化。

## E. AI 迁移

### GEN12-E01
给图像、文本、音频各选择一个 observation model，并写出单位与 reduction。

### GEN12-E02
设计脚本自动核对 analytic KL 与 Monte Carlo log-density ratio。

### GEN12-E03
审计两篇 VAE 论文的 $\beta$ 是否可比，列出至少八项必须统一的协议。

## 解答入口

[[解答 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]

