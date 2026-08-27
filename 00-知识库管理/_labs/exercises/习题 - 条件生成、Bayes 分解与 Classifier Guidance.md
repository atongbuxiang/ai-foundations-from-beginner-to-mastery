---
type: exercise
status: draft
area: [generative-models, guidance]
topic: "[[条件生成、Bayes 分解与 Classifier Guidance]]"
solution: "[[解答 - 条件生成、Bayes 分解与 Classifier Guidance]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 条件生成、Bayes 分解与 Classifier Guidance
## A. 识别与复述
### GEN65-A01
写出 conditional score identity，并列出它成立所需的正性/可微条件。
### GEN65-A02
为什么分类器应估计 $p_t(y\mid x_t)$ 而不是只在干净图像上准确？
### GEN65-A03
区分 score modification、reverse SDE drift modification 与 Gaussian reverse mean shift。
## B. 手算与建模
### GEN65-B01
设 $p(x)=\mathcal N(0,1)$、$p(y\mid x)\propto e^{-(x-2)^2/8}$，求 $w=1,3$ 时 tilted Gaussian 的均值与方差。
### GEN65-B02
无条件 reverse kernel 为 $\mathcal N(\mu,\operatorname{diag}(1,4))$，classifier gradient 为 $(2,-1)$，$w=.5$。求 guided mean shift。
### GEN65-B03
forward SDE 的 $g(t)=2$。写出 classifier score term 对 reverse SDE 与 PF-ODE drift 的系数（使用本节 $b_{rev},b_{pf}$ 接口）。
## C. 推导与证明
### GEN65-C01
从 Bayes 公式逐步推导 $\nabla_x\log p_t(x\mid y)$。
### GEN65-C02
用配方证明 Gaussian kernel 乘局部线性 likelihood 后均值变为 $\mu+\Sigma g_y$。
### GEN65-C03
证明 $s+w\nabla\log p(y\mid x)$ 是 $p(x)p(y\mid x)^w$ 的 score，并说明归一化条件。
## D. 边界、反例与纠错
### GEN65-D01
反驳“分类准确率高就说明 guidance gradient 可靠”。
### GEN65-D02
解释为什么不能把 pixel-space classifier gradient 直接加到 latent diffusion 的 latent 上。
### GEN65-D03
纠正“$w>1$ 只是更精确地采样 $p(x\mid y)$”。
## E. AI 迁移
### GEN65-E01
设计 noisy classifier 的最小 gradient audit。
### GEN65-E02
为 classifier guidance 写一个包含质量、覆盖与计算的 scale-sweep 表头。
### GEN65-E03
给定新 sampler API，列出确认 guidance 系数和方向的五步检查。
## 解答入口
[[解答 - 条件生成、Bayes 分解与 Classifier Guidance]]
