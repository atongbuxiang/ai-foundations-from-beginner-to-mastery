---
type: exercise
status: draft
area: [generative-models, gan]
topic: "[[饱和、非饱和生成器损失与 f-GAN]]"
solution: "[[解答 - 饱和、非饱和生成器损失与 f-GAN]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 饱和、非饱和生成器损失与 f-GAN
## A. 识别与复述
### GEN19-A01
写出 saturating 与 non-saturating generator losses。
### GEN19-A02
区分 equilibrium、population scalar 与 parameter vector field。
### GEN19-A03
写出 f-divergence 与 Fenchel variational lower bound。
## B. 手算与建模
### GEN19-B01
$D=.01$ 时求两种 loss 对 logit 的梯度系数。
### GEN19-B02
$D=.8$ 时重复上题并解释。
### GEN19-B03
$f(u)=u\log u$，求 conjugate $f^*(t)$。
## C. 推导与证明
### GEN19-C01
推导两种 logistic logit derivatives。
### GEN19-C02
由 Fenchel dual 推导 f-GAN lower bound。
### GEN19-C03
证明受限 critic supremum 不超过真实 divergence。
## D. 边界、反例与纠错
### GEN19-D01
反驳“non-saturating loss 每步精确最小化 JS”。
### GEN19-D02
构造 logit 系数强但完整 generator gradient 为零的情形。
### GEN19-D03
说明错误 critic output domain 如何破坏 f-GAN objective。
## E. AI 迁移
### GEN19-E01
审计论文采用何 $f$、方向、domain、critic transform 与 surrogate。
### GEN19-E02
设计同 critic 下 saturating/non-saturating 梯度对照。
### GEN19-E03
为离散生成说明为何还需 gradient estimator。
## 解答入口
[[解答 - 饱和、非饱和生成器损失与 f-GAN]]

