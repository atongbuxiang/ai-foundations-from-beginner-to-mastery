---
type: exercise
status: draft
area: [generative-models, vae, hierarchy, flow]
topic: "[[层次 VAE、表达性先验与近似后验 Flow]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 层次 VAE、表达性先验与近似后验 Flow]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - 层次 VAE、表达性先验与近似后验 Flow

## A. 识别与复述

### GEN15-A01
列出增强 VAE 的 prior、likelihood、posterior、hierarchy 四类对象及直接责任。

### GEN15-A02
写出两层 top-down joint 与祖先采样顺序。

### GEN15-A03
posterior flow 与 generative flow 在对象和采样/密度成本上有何不同？

## B. 手算与建模

### GEN15-B01
一维 flow $z_1=2z_0+1$，base density 在 $z_0$ 为 $.3$。求 $q_1(z_1)$ 与 log-density correction。

### GEN15-B02
两层 joint $p(z_2)p(z_1\mid z_2)p(x\mid z_1,z_2)$，给定三项 log probability $(-1,-.5,-2)$，求 joint log-density。

### GEN15-B03
若 rate 为 2.5 nats、MI 为 1.0，求 aggregate-prior KL；更强 prior 将其降至 .2 而 MI 不变时新 rate 为何？

## C. 推导与证明

### GEN15-C01
推导可逆 posterior flow 的 log-density 换元式并代入 ELBO。

### GEN15-C02
在匹配 factorization 下推导层次 joint KL 的条件 KL chain rule。

### GEN15-C03
证明固定 vMF 的 $\kappa,d$ 使 KL 对均值方向 $\mu$ 不变，并说明为何不推出 MI 正。

## D. 边界、反例与纠错

### GEN15-D01
反驳“posterior flow 更强，所以无条件生成采样也更强”。

### GEN15-D02
反驳“NVAE 样本清晰证明层次 latent 是唯一原因”。

### GEN15-D03
构造固定正 KL 但 encoder 对所有 $x$ 输出同一 vMF 的无信息例子。

## E. AI 迁移

### GEN15-E01
为多尺度图像 VAE 写 group-wise KL/use audit 与祖先采样伪协议。

### GEN15-E02
为 UniVAE 风格文本模型设计 length leakage、mask 与 EOS 审计。

### GEN15-E03
给一篇同时改 prior、posterior flow 与 decoder 的论文设计最小消融矩阵。

## 解答入口

[[解答 - 层次 VAE、表达性先验与近似后验 Flow]]

