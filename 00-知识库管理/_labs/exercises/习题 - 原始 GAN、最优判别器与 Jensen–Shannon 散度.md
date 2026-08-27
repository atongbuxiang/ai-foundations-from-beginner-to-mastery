---
type: exercise
status: draft
area: [generative-models, gan]
topic: "[[原始 GAN、最优判别器与 Jensen–Shannon 散度]]"
solution: "[[解答 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 原始 GAN、最优判别器与 Jensen–Shannon 散度
## A. 识别与复述
### GEN18-A01
写出 $D^*$、GAN value 与 JS 的关系。
### GEN18-A02
三条等式分别需要哪些 best-response/population 条件？
### GEN18-A03
为什么 $D\approx1/2$ 不是充分的成功证据？
## B. 手算与建模
### GEN18-B01
$p=(.8,.2),q=(.4,.6)$，求逐点 $D^*$。
### GEN18-B02
对上题求 $M$、两项 KL、JS 与 $V(D^*)$。
### GEN18-B03
$P,Q$ 支持不交，求 JS 与 GAN optimal value。
## C. 推导与证明
### GEN18-C01
用一二阶导数推出 $D^*$。
### GEN18-C02
完整推导 $V(D^*)=-\log4+2JS$。
### GEN18-C03
用共同支配测度重写推导。
## D. 边界、反例与纠错
### GEN18-D01
构造 $D=1/2$ 但 $P\ne Q$ 的 underfit critic。
### GEN18-D02
反驳“实际 generator 每一步都沿 JS 最速下降”。
### GEN18-D03
说明 empirical 100% accuracy 不推出 population supports 分离。
## E. AI 迁移
### GEN18-E01
为一个 toy mixture 数值枚举 $D^*$ 与 JS。
### GEN18-E02
设计区分 equilibrium 与 discriminator undertraining 的实验。
### GEN18-E03
审计不等类先验/label smoothing 对 $D^*$ 的改变。
## 解答入口
[[解答 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]

