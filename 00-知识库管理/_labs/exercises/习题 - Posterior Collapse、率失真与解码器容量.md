---
type: exercise
status: draft
area: [generative-models, vae, information-theory]
topic: "[[Posterior Collapse、率失真与解码器容量]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Posterior Collapse、率失真与解码器容量]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - Posterior Collapse、率失真与解码器容量

## A. 识别与复述

### GEN14-A01
定义完整、维度级、近似 collapse 与 decoder-ignore latent。

### GEN14-A02
定义 rate、distortion、aggregate posterior 与互信息。

### GEN14-A03
结构性 collapse 与 lagging-inference 动力学 collapse 有何区别？

## B. 手算与建模

### GEN14-B01
若 $I_q(X;Z)=.7$、$\mathrm{KL}(q(z)\|p(z))=.3$，求 rate；若只观测 rate 能否反推出 MI？

### GEN14-B02
对所有 $x$，$q(z\mid x)=N(2,1),p(z)=N(0,1)$。求 MI、aggregate KL 与 rate。

### GEN14-B03
两个模型 $(D,R)$ 分别为 $(100,0)$、$(80,30)$。在 $\beta=.5,1$ 时比较 $D+\beta R$。

## C. 推导与证明

### GEN14-C01
完整证明 $R=I_q(X;Z)+\mathrm{KL}(q(z)\|p(z))$。

### GEN14-C02
证明若 decoder 可完全忽略 $z$ 且不损失 likelihood，则 $q(z\mid x)=p(z)$ 不劣于任意正-rate encoder。

### GEN14-C03
证明 rate 是 MI 上界，并写出等号条件。

## D. 边界、反例与纠错

### GEN14-D01
用正 KL、零 MI 反例驳斥“BN 保证 KL 正就保证 latent 有用”。

### GEN14-D02
给出 MI 正但 decoder 完全不使用 latent 的联合/模型构造。

### GEN14-D03
反驳“KL warm-up 后 KL 较大，所以模型已解决 collapse 且 likelihood 更优”。

## E. AI 迁移

### GEN14-E01
为 Transformer 文本 VAE 设计四类 collapse 诊断与按长度分层报告。

### GEN14-E02
比较 warm-up、free bits、弱 decoder、lagging updates、rich prior 的直接作用对象与消融。

### GEN14-E03
设计 latent swap/intervention 实验，区分 encoder 存有信息与 decoder 实际使用信息。

## 解答入口

[[解答 - Posterior Collapse、率失真与解码器容量]]

