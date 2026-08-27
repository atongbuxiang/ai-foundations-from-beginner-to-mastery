---
type: exercise
status: draft
area: [generative-models, ctmc, discrete-score]
topic: "[[连续时间 Markov 链、离散 Score 与采样]]"
solution: "[[解答 - 连续时间 Markov 链、离散 Score 与采样]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 连续时间 Markov 链、离散 Score 与采样
## A. 识别与复述
### GEN59-A01
写出 CTMC generator 的符号条件和 forward equation。
### GEN59-A02
定义离散 ratio score 与 log-ratio score；为什么不是 $\nabla$？
### GEN59-A03
写出 reverse off-diagonal rate，并说明每个因子的方向。
## B. 手算与建模
### GEN59-B01
$R=\begin{bmatrix}-2&2\\1&-1\end{bmatrix}$，$p_t=(.75,.25)$。求两个 reverse off-diagonal rates。
### GEN59-B02
当前状态 $i$ 的 outgoing rates 为 $(.3,.2,.5)$。求总离开率、平均等待时间和跳到各目标的条件概率。
### GEN59-B03
若最大离开率为 12，tau-leap 步长 $h=.1$ 是否保证 $I+hR$ 非负？给出安全上界。
## C. 推导与证明
### GEN59-C01
由 $Q=I+hR+o(h)$ 推导 $p'_t=p_tR_t$。
### GEN59-C02
用 infinitesimal joint probability 推导 reverse rate。
### GEN59-C03
证明真实 log-ratios 沿任意闭环之和为零。
## D. 边界、反例与纠错
### GEN59-D01
为什么 learned edge ratios 未必来自某个全局分布？
### GEN59-D02
反驳“减小 tau-leap 步长可以修复 ratio network 的系统偏差”。
### GEN59-D03
为什么 network evaluation 数、jump event 数与 wall-clock 不能互换？
## E. AI 迁移
### GEN59-E01
给出 generator 和 reverse-rate 的自动 assertion。
### GEN59-E02
设计两状态 CTMC 的 exact-matrix-exponential 与 event-simulation 对照。
### GEN59-E03
比较 $x_0$ prediction 与 ratio prediction 时必须控制的预算和输出结构。
## 解答入口
[[解答 - 连续时间 Markov 链、离散 Score 与采样]]
