---
type: exercise
status: draft
area: [generative-models, gan, optimal-transport]
topic: "[[IPM、Wasserstein-1 与 Kantorovich 对偶]]"
solution: "[[解答 - IPM、Wasserstein-1 与 Kantorovich 对偶]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - IPM、Wasserstein-1 与 Kantorovich 对偶
## A. 识别与复述
### GEN20-A01
定义 IPM、$W_1$ primal 与 KR dual。
### GEN20-A02
TV、MMD、$W_1$ 分别选择什么函数类？
### GEN20-A03
列出 population $W_1$ 到 current neural critic 的四层近似。
## B. 手算与建模
### GEN20-B01
求 $W_1(\delta_2,\delta_{-1})$。
### GEN20-B02
求 $\theta\ne0$ 时 $JS(\delta_0,\delta_\theta)$。
### GEN20-B03
$P=(.5,.5)$ 在 $0,2$，$Q=\delta_1$，求一维 $W_1$。
## C. 推导与证明
### GEN20-C01
证明任意 1-Lipschitz $f$ 给 $E_Pf-E_Qf\le W_1$。
### GEN20-C02
证明点质量 $W_1=|\theta|$。
### GEN20-C03
说明 $W_1\to0$ 对点质量而 JS 不连续。
## D. 边界、反例与纠错
### GEN20-D01
反驳“$W_1$ 连续所以 neural WGAN 必稳定”。
### GEN20-D02
构造受限 critic 无法区分两个不同分布。
### GEN20-D03
反驳“WGAN loss 数值就是 exact Wasserstein distance”。
## E. AI 迁移
### GEN20-E01
为图像选择 ground metric 并讨论其语义问题。
### GEN20-E02
设计 point-mass 数值实验比较 JS proxy 与 $W_1$。
### GEN20-E03
写出 empirical/restricted/optimized critic gap 报告。
## 解答入口
[[解答 - IPM、Wasserstein-1 与 Kantorovich 对偶]]

