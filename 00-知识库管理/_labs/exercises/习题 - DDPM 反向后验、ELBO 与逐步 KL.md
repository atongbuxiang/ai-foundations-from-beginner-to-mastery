---
type: exercise
status: draft
area: [generative-models, diffusion]
topic: "[[DDPM 反向后验、ELBO 与逐步 KL]]"
solution: "[[解答 - DDPM 反向后验、ELBO 与逐步 KL]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - DDPM 反向后验、ELBO 与逐步 KL
## A. 识别与复述
### GEN42-A01
区分 $q(x_{t-1}|x_t,x_0)$ 与 $q(x_{t-1}|x_t)$。
### GEN42-A02
写出 $\tilde\mu_t,\tilde\beta_t$。
### GEN42-A03
列出负 ELBO 的三类项。
## B. 手算与建模
### GEN42-B01
$\bar\alpha_{t-1}=0.8,\alpha_t=0.75,\beta_t=0.25$。求 $\bar\alpha_t,\tilde\beta_t$。
### GEN42-B02
用 $\beta_1=0.1,\beta_2=0.2$ 求 $t=2$ posterior mean 对 $x_0,x_2$ 的系数。
### GEN42-B03
两个一维 Gaussian 方差同为 $0.5$，均值差 $0.2$。求 mean 部分 KL。
## C. 推导与证明
### GEN42-C01
用 precision 相加推导 $\tilde\beta_t$。
### GEN42-C02
把 $\tilde\mu_t$ 改写为 noise 形式。
### GEN42-C03
从 Jensen 与 joint factorization 推出三类 ELBO 项。
## D. 边界、反例与纠错
### GEN42-D01
反驳“真实 reverse conditional 一定是单 Gaussian”。
### GEN42-D02
反驳“posterior mean 中两个系数必须和为 1”。
### GEN42-D03
反驳“simple noise MSE 数值就是 negative ELBO”。
## E. AI 迁移
### GEN42-E01
设计 posterior mean/variance 的 Monte Carlo 或代数测试。
### GEN42-E02
给出 reverse model 输出 mean/variance 的最小 shape 合同。
### GEN42-E03
审计 hierarchical-VAE 类比的正确与错误部分。
## 解答入口
[[解答 - DDPM 反向后验、ELBO 与逐步 KL]]

