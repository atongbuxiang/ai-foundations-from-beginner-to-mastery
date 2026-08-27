---
type: exercise
status: draft
area: [generative-models, diffusion, ddim]
topic: "[[DDIM、非 Markov 前向族与确定性采样]]"
solution: "[[解答 - DDIM、非 Markov 前向族与确定性采样]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - DDIM、非 Markov 前向族与确定性采样
## A. 识别与复述
### GEN46-A01
解释“same marginals do not determine the same joint”，并指出 simplified DDPM training 看到了哪些随机变量。
### GEN46-A02
写出从 $t$ 跳到 $s<t$ 的一般 DDIM 更新和 $\eta$ 的作用。
### GEN46-A03
“$\eta=0$ 时确定”究竟条件于哪些对象？它不推出哪些更强结论？
## B. 手算与建模
### GEN46-B01
复算正文标量例：$a_t=0.6,\sigma_t=0.8,a_s=0.8,x_t=1,\hat\epsilon=-0.5,\eta=0$，求 $\hat x_0,x_s$。
### GEN46-B02
$\bar\alpha_s=0.8,\bar\alpha_t=0.5,\eta=0.5$，计算 $\sigma_{t\to s}^{DDIM}$ 与噪声方向系数 $\sqrt{1-\bar\alpha_s-\sigma^2}$。
### GEN46-B03
原训练有 $T=1000$ 步，采样子序列有 50 个 reverse transitions。若每步调用网络一次，NFE 降低多少倍？这个数不包含哪些成本？
## C. 推导与证明
### GEN46-C01
证明对任意 $t$，构造 $x_t=a_tx_0+\sigma_t\epsilon_t$ 且每个 $\epsilon_t\sim N(0,I)$ 即可保持同一 marginal，而不同的 $(\epsilon_1,\ldots,\epsilon_T)$ joint 会给不同路径。
### GEN46-C02
用归纳法证明：固定 $x_T$、网络、condition、time grid 和 $\eta=0$ 后，整个离散轨迹确定。
### GEN46-C03
将 $s=t-1,\eta=1$ 代入 DDIM 方差公式，证明其平方等于 DDPM posterior variance $\tilde\beta_t$。
## D. 边界、反例与纠错
### GEN46-D01
反驳“deterministic sampler 没有样本多样性”。
### GEN46-D02
反驳“网络在所有训练时刻训练过，所以任意大跳步都是 exact”。
### GEN46-D03
说明 $\hat x_0$ clipping 为什么不是无害的数值保护，并给一个标量反例。
## E. AI 迁移
### GEN46-E01
设计 DDPM 与多组 DDIM 子序列的公平速度—质量实验。
### GEN46-E02
为图像 inversion/reconstruction 设计协议，区分 deterministic、cycle consistency 与 exact inverse。
### GEN46-E03
将一个使用 $0\ldots T-1$ 代码索引的 scheduler 映射到数学 $1\ldots T$，列出必须通过的断言。
## 解答入口
[[解答 - DDIM、非 Markov 前向族与确定性采样]]
