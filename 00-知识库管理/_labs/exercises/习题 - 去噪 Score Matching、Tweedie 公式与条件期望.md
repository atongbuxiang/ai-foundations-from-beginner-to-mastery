---
type: exercise
status: draft
area: [generative-models, score-matching, denoising]
topic: "[[去噪 Score Matching、Tweedie 公式与条件期望]]"
solution: "[[解答 - 去噪 Score Matching、Tweedie 公式与条件期望]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 去噪 Score Matching、Tweedie 公式与条件期望
## A. 识别与复述
### GEN28-A01
写出 Gaussian corruption、conditional score 与 marginal noisy density。
### GEN28-A02
陈述 conditional score identity 与 $L^2$ 投影分解。
### GEN28-A03
写出 Tweedie 公式及 score、noise、clean 三种参数化关系。
## B. 手算与建模
### GEN28-B01
$X\in\{-a,a\}$ 等概率，$Y=X+N(0,\sigma^2)$。求 $Y=0$ 时的 posterior mean 与 marginal score。
### GEN28-B02
$X\sim N(0,\tau^2)$、$Y=X+N(0,\sigma^2)$。求 $s_Y(y)$，并用 Tweedie 公式求 $E[X\mid Y=y]$。
### GEN28-B03
若网络预测 $\varepsilon_\theta(y,\sigma)=0.4$、$y=1.2,\sigma=0.5$（一维），求 score 预测和 clean 预测。
## C. 推导与证明
### GEN28-C01
从卷积积分推导 $s_\sigma(y)=E[\nabla_y\log q(y\mid X)\mid Y=y]$。
### GEN28-C02
证明 conditional-score MSE 等于 marginal-score MSE 加一个与 predictor 无关的项。
### GEN28-C03
推导一般 covariance $\Sigma$ 下 $E[X\mid Y=y]=y+\Sigma\nabla_y\log p_Y(y)$。
## D. 边界、反例与纠错
### GEN28-D01
反驳“posterior-mean denoiser 一定恢复生成这次观测的真实 clean sample”。
### GEN28-D02
反驳“两个 DSM/score loss 同最优解，所以有限网络下训练曲线和样本质量必相同”。
### GEN28-D03
为何 Laplace noise 下不能直接使用 $y+\sigma^2s(y)$？
## E. AI 迁移
### GEN28-E01
设计二维 Gaussian-mixture 数值实验核验 Tweedie 公式。
### GEN28-E02
审计一个同时比较 $\varepsilon$-prediction 与 score-prediction 的实验，需控制哪些 scaling？
### GEN28-E03
解释 DSM 为什么可在训练时不跑 MCMC，但部署生成仍需要 sampler。
## 解答入口
[[解答 - 去噪 Score Matching、Tweedie 公式与条件期望]]

