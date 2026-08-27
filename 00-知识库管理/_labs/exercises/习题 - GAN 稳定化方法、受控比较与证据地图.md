---
type: exercise
status: draft
area: [generative-models, gan, reproducibility]
topic: "[[GAN 稳定化方法、受控比较与证据地图]]"
solution: "[[解答 - GAN 稳定化方法、受控比较与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - GAN 稳定化方法、受控比较与证据地图
## A. 识别与复述
### GEN24-A01
列出六类稳定化干预及直接对象。
### GEN24-A02
写出 hinge discriminator/generator losses。
### GEN24-A03
给“稳定”写至少五个 operational criteria。
## B. 手算与建模
### GEN24-B01
real scores $(2,.5)$、fake scores $(-2,0)$，求 hinge $L_D$。
### GEN24-B02
A 每步 1 critic update、B 每步 5 次；各 100k generator steps，求 critic updates。
### GEN24-B03
五个 seed FID $(10,11,12,30,9)$，求均值、中位数与 failure rate（阈值20）。
## C. 推导与证明
### GEN24-C01
推 hinge loss 对 score 的分段梯度。
### GEN24-C02
说明 matched factorial ablation 如何估主效应与交互。
### GEN24-C03
证明同时改六项时单组件因果不可识别。
## D. 边界、反例与纠错
### GEN24-D01
反驳“loss 曲线平滑所以稳定”。
### GEN24-D02
反驳“FID 更低证明 $W_1$ 估计更准”。
### GEN24-D03
构造最佳 checkpoint 报告掩盖高 failure rate。
## E. AI 迁移
### GEN24-E01
设计 logistic/R1 与 WGAN-GP 的公平比较表。
### GEN24-E02
审计 evaluator version、preprocess、sample count 与 CI。
### GEN24-E03
把科学空间的 WGAN 反例性评论转成可证伪实验。
## 解答入口
[[解答 - GAN 稳定化方法、受控比较与证据地图]]

