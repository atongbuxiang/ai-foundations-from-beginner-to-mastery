---
type: exercise
status: draft
topic: "[[Mean-Field、Feature Learning 与训练 Regime]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Mean-Field、Feature Learning 与训练 Regime]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Mean-Field、Feature Learning 与训练 Regime
## A
### LT-MF-A01
定义 neuron 参数经验测度，并把两层网络写成积分。
### LT-MF-A02
写出 mean-field continuity equation 的速度场形式。
### LT-MF-A03
为什么 $f_\rho$ 对 $\rho$ 线性，而训练 dynamics 对 $\rho$ 非线性？
## B
### LT-MF-B01
给三个粒子 $\vartheta_1,\vartheta_2,\vartheta_3$，写出 $\rho_3$ 以及对测试函数 $g$ 的积分。
### LT-MF-B02
若所有粒子以常速度 $v$ 平移，初始为 $\rho_0$，写出 $\rho_t$ 的 pushforward。
### LT-MF-B03
比较 $m=100$ 时 $1/m$ 与 $1/\sqrt m$ 的输出前因子。
## C
### LT-MF-C01
从粒子守恒推导 continuity equation 的弱形式。
### LT-MF-C02
解释 learning-rate/time rescaling 为什么是 mean-field limit 的组成部分。
### LT-MF-C03
说明 propagation of chaos 如何桥接有限网络与 PDE。
## D
### LT-MF-D01
审计“参数移动很大，所以网络学到了有用表示”。
### LT-MF-D02
审计“两层 mean-field global convergence 证明了 Transformer SGD 找到全局最优”。
### LT-MF-D03
为什么先取宽度无穷与先训练到无穷久可能不同？
## E
### LT-MF-E01
设计区分 lazy 与 feature-learning regime 的多指标实验。
### LT-MF-E02
设计检验 feature learning 是否改善 transfer 而非只改善训练拟合的实验。
### LT-MF-E03
写 mean-field claim card：scaling、PDE、finite-width bridge、风险与外推边界。

