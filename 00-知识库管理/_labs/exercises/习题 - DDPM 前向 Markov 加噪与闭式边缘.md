---
type: exercise
status: draft
area: [generative-models, diffusion]
topic: "[[DDPM 前向 Markov 加噪与闭式边缘]]"
solution: "[[解答 - DDPM 前向 Markov 加噪与闭式边缘]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - DDPM 前向 Markov 加噪与闭式边缘
## A. 识别与复述
### GEN41-A01
定义 $\beta_t,\alpha_t,\bar\alpha_t$，写出单步 forward kernel。
### GEN41-A02
写出 $q(x_t\mid x_0)$ 与一次采样式，并解释“分布相等”不代表什么。
### GEN41-A03
为什么 $q(x_T\mid x_0)\approx N(0,I)$ 通常只是近似？
## B. 手算与建模
### GEN41-B01
$\beta_1=0.1,\beta_2=0.2$。求 $\alpha_1,\alpha_2,\bar\alpha_2$ 与 $q(x_2\mid x_0)$。
### GEN41-B02
$\bar\alpha_t=0.36,x_0=2,\epsilon=-0.5$。求 $x_t$ 与 SNR。
### GEN41-B03
若 $x_0\in\mathbb R^{3\times32\times32}$，batch size 8，写出 $t,a_t,\sigma_t,\epsilon,x_t$ 的形状。
## C. 推导与证明
### GEN41-C01
从两步递推推导噪声方差 $1-\alpha_1\alpha_2$。
### GEN41-C02
用归纳法证明一般闭式边缘。
### GEN41-C03
证明给定 $x_0$ 的 forward chain 满足一阶 Markov 性，并说明闭式边缘未删除 joint。
## D. 边界、反例与纠错
### GEN41-D01
纠正把 sampling noise 写成 $(1-\bar\alpha_t)\epsilon$ 的错误。
### GEN41-D02
纠正把科学空间早期文章的 amplitude $\beta_t$ 直接当本卷 variance $\beta_t$。
### GEN41-D03
给出 float16 cumprod 可能下溢而数学值仍非零的解释。
## E. AI 迁移
### GEN41-E01
设计 forward marginal 的均值/方差 Monte Carlo 测试。
### GEN41-E02
为 schedule table 写出至少六项 assertion。
### GEN41-E03
审计“训练每个 batch 必须真的运行 $t$ 次加噪”的说法。
## 解答入口
[[解答 - DDPM 前向 Markov 加噪与闭式边缘]]

