---
type: exercise
status: draft
area: [generative-models, reverse-time, score]
topic: "[[Reverse-time SDE、时间反演与 Score Drift]]"
solution: "[[解答 - Reverse-time SDE、时间反演与 Score Drift]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Reverse-time SDE、时间反演与 Score Drift
## A. 识别与复述
### GEN50-A01
写出 $t:1\downarrow0$ 与 $\tau=1-t:0\uparrow1$ 两种 reverse SDE 公式。
### GEN50-A02
解释 reverse-time SDE 与逐样本 inverse map 的区别。
### GEN50-A03
为什么反向噪声使用新的 Brownian motion，而不是 $-dW_t$？
## B. 手算与建模
### GEN50-B01
对平稳 VP SDE $dX=-\beta Xdt/2+\sqrt\beta dW$、$p_t=N(0,I)$，求正向反时钟 drift。
### GEN50-B02
对 $dX_t=dW_t,X_0\sim N(0,4)$，求 $s_t(x)$ 与 $\tau$-clock reverse drift。
### GEN50-B03
递减网格一步 $h=-0.01$，给定 $f=0.4,g=2,s=-0.3,x=1,z=0.5$，计算 Euler–Maruyama 新状态。
## C. 推导与证明
### GEN50-C01
用小 Gaussian corruption/Tweedie 思路推导 $\tau$-clock drift $-f+g^2s$。
### GEN50-C02
从 $t$-clock 公式通过 $\tau=1-t$ 推出第二种记法。
### GEN50-C03
写出 state-dependent diffusion matrix 的 reverse drift，并说明标量公式何时成立。
## D. 边界、反例与纠错
### GEN50-D01
诊断把 $f-g^2s$ 放进递增 $\tau$ 网格而不换号会造成什么错误。
### GEN50-D02
反驳“保存 forward noise 后逐项取负就是生成 sampler”。
### GEN50-D03
为什么 exact time-reversal theorem 不保证 learned-score finite-step sampler 正确？
## E. AI 迁移
### GEN50-E01
列出 reverse Euler–Maruyama 实现的最小单元测试。
### GEN50-E02
score error 为 $e_t$ 时 drift error 是什么？据此设计 time-wise error report。
### GEN50-E03
设计一个平稳 OU 符号回归测试，专门捕获时间方向 bug。
## 解答入口
[[解答 - Reverse-time SDE、时间反演与 Score Drift]]
