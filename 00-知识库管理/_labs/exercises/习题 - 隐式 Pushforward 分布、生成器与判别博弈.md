---
type: exercise
status: draft
area: [generative-models, gan]
topic: "[[隐式 Pushforward 分布、生成器与判别博弈]]"
solution: "[[解答 - 隐式 Pushforward 分布、生成器与判别博弈]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 隐式 Pushforward 分布、生成器与判别博弈
## A. 识别与复述
### GEN17-A01
定义 $G_{\theta\#}P_Z$，并区分可采样与可算 density。
### GEN17-A02
写出等类先验的 real/fake 二分类实验与 GAN value。
### GEN17-A03
列出 population、restricted、empirical、optimized、deployed 五层对象。
## B. 手算与建模
### GEN17-B01
$Z\sim U[-1,1],G(z)=z^2$，求生成分布 CDF 与 $(0,1)$ 上 density。
### GEN17-B02
Bayes 判别器 $D^*(x)=.8$，求 density ratio $p_*/p_g$。
### GEN17-B03
real/fake 类先验为 $(.7,.3)$，推导 Bayes classifier。
## C. 推导与证明
### GEN17-C01
证明 pushforward 是概率测度。
### GEN17-C02
证明等类先验下 Bayes classifier 给 $p/(p+q)$。
### GEN17-C03
说明 $m<d$ 的 regular generator pushforward 为何可能对 ambient Lebesgue 测度奇异。
## D. 边界、反例与纠错
### GEN17-D01
反驳“判别器 accuracy 高，所以 density-ratio estimate 精确”。
### GEN17-D02
构造 conditional GAN 中 discriminator 只读条件比例的 shortcut。
### GEN17-D03
反驳“GAN 不算 likelihood，所以没有模型分布”。
## E. AI 迁移
### GEN17-E01
为文本 GAN 写 latent→sequence pushforward 与不可微采样难点。
### GEN17-E02
设计 held-out critic calibration/density-ratio 审计。
### GEN17-E03
审计 latent truncation 如何使部署分布偏离训练生成分布。
## 解答入口
[[解答 - 隐式 Pushforward 分布、生成器与判别博弈]]

