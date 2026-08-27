---
type: exercise
status: draft
area: [generative-models, langevin, mcmc]
topic: "[[Langevin、ULA、MALA 与平稳分布]]"
solution: "[[解答 - Langevin、ULA、MALA 与平稳分布]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Langevin、ULA、MALA 与平稳分布
## A. 识别与复述
### GEN30-A01
写出本节尺度下的 Langevin SDE、Fokker–Planck current 与 ULA 更新。
### GEN30-A02
区分 invariant、ergodic、mixing rate 与 finite-budget accuracy。
### GEN30-A03
写出 MALA proposal 与 acceptance probability；为何未知 $Z$ 消去？
## B. 手算与建模
### GEN30-B01
对标准正态 target 推导 ULA 稳定区间与平稳方差。
### GEN30-B02
取 $h=1$、标准正态 target、当前 $x=0$、proposal $y=1$。按本节尺度计算 MALA acceptance probability。
### GEN30-B03
两状态 kernel $K=\begin{pmatrix}.9&.1\\.2&.8\end{pmatrix}$。求 invariant distribution，并验证一次 $\pi K=\pi$。
## C. 推导与证明
### GEN30-C01
将 $\pi\propto e^{-E}$ 代入 probability current，证明 zero current。
### GEN30-C02
解 AR(1) 方差递推，证明 ULA 的 Gaussian stationary variance 为 $1/(1-h/2)$。
### GEN30-C03
证明 MALA 的 MH kernel 满足 detailed balance（可用 accepted move + rejection 分解）。
## D. 边界、反例与纠错
### GEN30-D01
反驳“energy 每步下降，所以迭代在从 Gibbs 分布采样”。
### GEN30-D02
给出 target invariant 但给定初值在有限预算内完全未覆盖另一模式的例子。
### GEN30-D03
反驳“MALA invariant 精确，所以输出样本 iid 且无需诊断”。
## E. AI 迁移
### GEN30-E01
为 neural EBM 的 ULA sampler 写出最小收敛/偏差审计。
### GEN30-E02
设计 ULA 与 MALA 的 compute-matched Gaussian/双峰比较。
### GEN30-E03
审计 replay buffer、随机重启与低温 sampling 对部署分布的影响。
## 解答入口
[[解答 - Langevin、ULA、MALA 与平稳分布]]

