---
type: exercise
status: draft
area: [generative-models, diffusion]
topic: "[[扩散简化损失、时间加权、Schedule 与 SNR]]"
solution: "[[解答 - 扩散简化损失、时间加权、Schedule 与 SNR]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 扩散简化损失、时间加权、Schedule 与 SNR
## A. 识别与复述
### GEN44-A01
写出 VLB noise-MSE weight，并说明依赖哪一 variance convention。
### GEN44-A02
写出 simplified epsilon objective；它与 ELBO 是什么关系？
### GEN44-A03
区分 objective timestep weight $\pi_t$ 与 sampling proposal $r_t$。
## B. 手算与建模
### GEN44-B01
两时刻共享 scalar $c$ 拟合 targets $(0,10)$，权重 $(1,1)$ 与 $(9,1)$ 时分别求 optimum。
### GEN44-B02
$\bar\alpha=0.8$ 与 $0.2$ 时分别求 SNR 和 log-SNR。
### GEN44-B03
目标 $\pi=(0.8,0.2)$，proposal $r=(0.5,0.5)$。写出两时刻 importance weights。
## C. 推导与证明
### GEN44-C01
证明 $E_{t\sim r}[\pi_t\ell_t/r_t]=\sum_t\pi_tE\ell_t$。
### GEN44-C02
说明正权重何时不改每时刻 Bayes optimum，何时会改共享模型 optimum。
### GEN44-C03
由累计 cosine $\bar\alpha_t$ 推出单步 $\alpha_t,\beta_t$。
## D. 边界、反例与纠错
### GEN44-D01
反驳“sum loss 与 mean loss 永远完全一样”。
### GEN44-D02
反驳“cosine schedule 是定理上普遍最优”。
### GEN44-D03
解释改变 proposal 却漏 importance correction 的后果。
## E. AI 迁移
### GEN44-E01
设计 schedule×parameterization×weight 的 factorial experiment。
### GEN44-E02
为 loss-second-moment timestep sampler 建立估计账。
### GEN44-E03
审计跨分辨率复用同一 SNR schedule 的主张。
## 解答入口
[[解答 - 扩散简化损失、时间加权、Schedule 与 SNR]]

