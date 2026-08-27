---
type: exercise
status: draft
area: [generative-models, diffusion]
topic: "[[反向均值、固定方差、学习方差与 Analytic-DPM]]"
solution: "[[解答 - 反向均值、固定方差、学习方差与 Analytic-DPM]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 反向均值、固定方差、学习方差与 Analytic-DPM
## A. 识别与复述
### GEN45-A01
区分 forward variance、知道 $x_0$ 的 posterior variance 与 model reverse variance；分别写出条件对象。
### GEN45-A02
写出给定模型均值时 Gaussian NLL 的最优 isotropic variance，并解释两项误差来源。
### GEN45-A03
为什么 Analytic-DPM 的“解析最优方差”仍需区分 identity、score approximation、Monte Carlo 与 clipping？
## B. 手算与建模
### GEN45-B01
给定 $eta_t=0.1,ar\alpha_{t-1}=0.8,ar\alpha_t=0.72$，计算 $\tilde\beta_t$ 并与 $eta_t$ 比较。
### GEN45-B02
二维 $Y|x_t$ 的 covariance 为 $\operatorname{diag}(0.25,1)$，真实条件均值为 $(1,2)$，模型均值为 $(0,2.5)$。求最优 isotropic variance。
### GEN45-B03
$\beta_t=0.02,\tilde\beta_t=0.005$，learned-range 系数 $r=0.25$。按 $\log\sigma^2=r\log\beta+(1-r)\log\tilde\beta$ 计算 $\sigma^2$。
## C. 推导与证明
### GEN45-C01
从 conditional expected Gaussian NLL 推导最优 isotropic variance，并验证该驻点是极小值。
### GEN45-C02
用全协方差公式说明 $q(x_{t-1}|x_t)$ 的 covariance 为什么不只含 $\tilde\beta_tI$。
### GEN45-C03
在 $0<\alpha_t<1$ 下证明 $\tilde\beta_t\le\beta_t$，并说明何时严格小于。
## D. 边界、反例与纠错
### GEN45-D01
纠正“$\tilde\beta_t$ 就是真实 $q(x_{t-1}|x_t)$ 方差”。
### GEN45-D02
构造一个例子反驳“把 variance 学大即可修复错误 reverse mean”。
### GEN45-D03
若允许 diagonal covariance，isotropic optimum 还能逐维直接使用吗？说明对象变化。
## E. AI 迁移
### GEN45-E01
设计 fixed-$\beta$、fixed-$\tilde\beta$、learned-range 与 analytic variance 的公平消融。
### GEN45-E02
为 score-based variance estimator 建立误差账与最小记录表。
### GEN45-E03
设计一个 toy conditional experiment，检验 learned variance 是否主要补偿 mean error 而非真实 aleatoric uncertainty。
## 解答入口
[[解答 - 反向均值、固定方差、学习方差与 Analytic-DPM]]
