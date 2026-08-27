---
type: exercise
status: draft
area: [generative-models, diffusion, sde]
topic: "[[从离散扩散到 VP、VE 与 sub-VP SDE]]"
solution: "[[解答 - 从离散扩散到 VP、VE 与 sub-VP SDE]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 从离散扩散到 VP、VE 与 sub-VP SDE
## A. 识别与复述
### GEN49-A01
写出线性 SDE $dX_t=a(t)X_tdt+g(t)dW_t$ 的条件均值系数和条件方差，并说明各由什么决定。
### GEN49-A02
分别写出 VP、VE、sub-VP 的 drift、$g(t)^2$ 与 conditional variance。
### GEN49-A03
为什么离散一步的随机项必须是 $O(\sqrt h)$ 而不是 $O(h)$？
## B. 手算与建模
### GEN49-B01
取常数 $\beta=2,t=0.5$。计算 VP 与 sub-VP 的均值系数、条件方差，并比较大小。
### GEN49-B02
VE 取 $\sigma(t)=e^t$ 且以 $\Sigma(t)=\sigma(t)^2-\sigma(0)^2$ 为累计方差。求 $g(t)^2$ 和 $t=\log2$ 时的 $\Sigma(t)$。
### GEN49-B03
若 $a(t)=-1,g(t)=2$，求 $X_t\mid X_0=x_0$ 的均值和方差。
## C. 推导与证明
### GEN49-C01
用积分因子推导一般线性 SDE 的闭式边缘。
### GEN49-C02
从 $\beta_k=\beta(t_k)h$ 的 DDPM 一步推导 VP SDE，并解释 $\log\bar\alpha\to-B(t)$。
### GEN49-C03
验证 $V_{subVP}=(1-e^{-B})^2$ 满足对应方差 ODE。
## D. 边界、反例与纠错
### GEN49-D01
纠正 Euler–Maruyama 中把噪声写成 $g(t)h\epsilon$ 的实现。
### GEN49-D02
反驳“VP、VE、sub-VP 在同一数值 $t$ 上具有相同 noise level”。
### GEN49-D03
为什么 $B(1)$ 很大仍不等于 terminal marginal 严格是标准正态？
## E. AI 迁移
### GEN49-E01
为 VP/VE/sub-VP 系数表设计至少八项自动 assertion。
### GEN49-E02
设计一个 Monte Carlo 实验，同时验证闭式边缘和 Euler–Maruyama 的弱收敛趋势。
### GEN49-E03
给出把离散 DDPM schedule 转为连续 $\beta(t)$ 时必须记录的复现字段。
## 解答入口
[[解答 - 从离散扩散到 VP、VE 与 sub-VP SDE]]
