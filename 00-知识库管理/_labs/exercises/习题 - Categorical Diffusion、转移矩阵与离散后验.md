---
type: exercise
status: draft
area: [generative-models, discrete-diffusion]
topic: "[[Categorical Diffusion、转移矩阵与离散后验]]"
solution: "[[解答 - Categorical Diffusion、转移矩阵与离散后验]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Categorical Diffusion、转移矩阵与离散后验
## A. 识别与复述
### GEN57-A01
在本卷 row-vector convention 下，写出 $Q_t[i,j]$、$\bar Q_t$ 和 $q(x_t\mid x_0=k)$。
### GEN57-A02
为什么类别 ID 的数值差通常没有概率含义？结构化转移核需要额外指定什么？
### GEN57-A03
区分 Gumbel-max、Gumbel–Softmax 与 D3PM forward kernel。
## B. 手算与建模
### GEN57-B01
令 $Q=\begin{bmatrix}.8&.2\\.1&.9\end{bmatrix}$。计算 $Q^2$ 与 $q(x_2\mid x_0=1)$。
### GEN57-B02
均匀替换核 $Q=(1-\beta)I+\beta U$，$K=4,\beta=.2$。求真正改变标签的概率。
### GEN57-B03
三状态例中 $e_1Q=(.8,.1,.1)$、$e_1Q^2=(.66,.17,.17)$。求 $q(x_1\mid x_2=3,x_0=1)$。
## C. 推导与证明
### GEN57-C01
用 Chapman–Kolmogorov 证明 $q(x_t=\cdot\mid x_0=k)=e_kQ_1\cdots Q_t$。
### GEN57-C02
逐步推导 $q(x_{t-1}=i\mid x_t=j,x_0=k)$ 并证明归一化。
### GEN57-C03
证明均匀替换核的累计形式 $\bar Q_t=\bar\alpha_tI+(1-\bar\alpha_t)U$。
## D. 边界、反例与纠错
### GEN57-D01
纠正“直接采 $q(x_t\mid x_0)$ 就复现了逐步 forward 的整条路径”。
### GEN57-D02
为什么 posterior 分母为零时不能加一个很小 $\epsilon$ 后仍称为精确 Bayes 后验？
### GEN57-D03
反驳“辅助 clean-token CE 与纯 ELBO 是数值相同的目标”。
## E. AI 迁移
### GEN57-E01
给出 row-stochastic kernel 的最小自动检查清单。
### GEN57-E02
设计一个小状态空间实验，核对矩阵闭式、Monte Carlo 边缘与解析 posterior。
### GEN57-E03
比较直接预测 reverse logits 与预测 $x_0$ 后混合 analytic posterior 的复现字段。
## 解答入口
[[解答 - Categorical Diffusion、转移矩阵与离散后验]]
