---
type: exercise
status: draft
area: [generative-models, probability-flow, ode]
topic: "[[Probability-flow ODE 与共享边缘分布]]"
solution: "[[解答 - Probability-flow ODE 与共享边缘分布]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Probability-flow ODE 与共享边缘分布
## A. 识别与复述
### GEN51-A01
写出各向同性 SDE 的 Fokker–Planck 方程与 PF ODE velocity。
### GEN51-A02
“共享边缘分布”精确指什么？列出三项它不能推出的对象。
### GEN51-A03
为什么 PF score 系数是 $1/2$，reverse SDE correction 却是 $1$？
## B. 手算与建模
### GEN51-B01
对 $dX=dW,X_0\sim N(0,I)$ 解出 PF ODE，并验证其方差为 $1+t$。
### GEN51-B02
比较上一题 SDE/ODE 给定 $X_0=x_0$ 的 conditional law。
### GEN51-B03
给定 $D(x)=\operatorname{diag}(1+x_1^2,2)$，写出一般 PF velocity 中的 $\nabla\cdot D$。
## C. 推导与证明
### GEN51-C01
把 Fokker–Planck 的 Laplacian 项改写为 score 通量并推出 PF ODE。
### GEN51-C02
用 quadratic variation 证明非退化 SDE 与常规 ODE 不同 path law。
### GEN51-C03
推导 CNF 的沿轨迹 log-density 变化式。
## D. 边界、反例与纠错
### GEN51-D01
构造 $w$ 满足 $\nabla\cdot(pw)=0$，说明同一 density path 的 velocity 不唯一。
### GEN51-D02
反驳“把 ODE tolerance 调到零即可恢复真实数据分布”。
### GEN51-D03
诊断把 DDIM 与任意 PF ODE solver 直接画等号的问题。
## E. AI 迁移
### GEN51-E01
设计 SDE/PF ODE 的同边缘—异路径最小数值实验。
### GEN51-E02
给出 likelihood 计算需要分账的 estimator 与 solver 字段。
### GEN51-E03
如何分别测 score/model error 与 ODE discretization error？
## 解答入口
[[解答 - Probability-flow ODE 与共享边缘分布]]
