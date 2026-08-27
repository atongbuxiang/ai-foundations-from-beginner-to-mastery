---
type: exercise
status: draft
area: [generative-models, gan, mode-collapse]
topic: "[[Mode Collapse、模式覆盖与生成器熵]]"
solution: "[[解答 - Mode Collapse、模式覆盖与生成器熵]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Mode Collapse、模式覆盖与生成器熵
## A. 识别与复述
### GEN23-A01
区分 exact、perceptual、semantic 与 conditional collapse。
### GEN23-A02
定义概念上的 precision/recall 分账。
### GEN23-A03
为什么 entropy 与 Jacobian 不是充分诊断？
## B. 手算与建模
### GEN23-B01
真实 8 均匀 modes，生成只覆盖 2，求两 entropy 与 mode recall。
### GEN23-B02
生成 1000 样本只有 10 个 unique outputs，求 naive duplicate rate。
### GEN23-B03
二类真实各 .5，生成比例 $(.95,.05)$，求 TV。
## C. 推导与证明
### GEN23-C01
证明 deterministic many-to-one map 可使不同 latent 区域同输出。
### GEN23-C02
说明局部 full-rank Jacobian 不推出全局 injective。
### GEN23-C03
证明高 entropy 可由远离数据的噪声取得。
## D. 边界、反例与纠错
### GEN23-D01
反驳高 precision 就没有 collapse。
### GEN23-D02
构造无 exact duplicates 但 semantic mode collapse。
### GEN23-D03
反驳高 generator differential entropy 必是好覆盖。
## E. AI 迁移
### GEN23-E01
设计 known-mode toy 与真实图像 coverage 联合协议。
### GEN23-E02
比较 minibatch discrimination、feature matching、unrolling 的直接作用。
### GEN23-E03
为 conditional GAN 按条件审计 diversity 与 rare modes。
## 解答入口
[[解答 - Mode Collapse、模式覆盖与生成器熵]]

