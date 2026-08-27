---
type: exercise
status: draft
area: [generative-models, score-matching, denoising]
topic: "[[Marginal Score、Conditional Score 与去噪等价]]"
solution: "[[解答 - Marginal Score、Conditional Score 与去噪等价]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Marginal Score、Conditional Score 与去噪等价
## A. 识别与复述
### GEN52-A01
定义 marginal score 与 conditional score，并写出二者的条件期望恒等式。
### GEN52-A02
精确解释“得分匹配 = 条件得分匹配”中的等号。
### GEN52-A03
Gaussian corruption 下写出 conditional score、noise target 与 denoiser 的换算。
## B. 手算与建模
### GEN52-B01
$X_0\sim N(0,4),X_t=2X_0+3\epsilon$。求 marginal score 与 conditional score。
### GEN52-B02
在上一题中计算 conditional loss 与 marginal loss 的常数差 $C$。
### GEN52-B03
$a=0.8,\sigma=0.6,x_t=1,\epsilon_\theta=0.5$。求 score prediction 与 $x_0$ prediction。
## C. 推导与证明
### GEN52-C01
由 $p_t(x)=\int p_0q_tdx_0$ 推导 score identity。
### GEN52-C02
证明 conditional MSE 的 Pythagorean 分解。
### GEN52-C03
证明输入可测权重 $w(X_t,t)$ 下分解仍成立，并指出何种权重可能破坏它。
## D. 边界、反例与纠错
### GEN52-D01
反驳“两种 loss 在每个 minibatch 上数值相同”。
### GEN52-D02
纠正“有限模型类会自动破坏标准 population 常数差”的说法。
### GEN52-D03
为什么直接用 batch ratio 估计 marginal score 可能有偏且昂贵？
## E. AI 迁移
### GEN52-E01
设计 Gaussian mixture 上验证 score identity 的 Monte Carlo 实验。
### GEN52-E02
设计实验比较 conditional target 与 oracle marginal target 的梯度均值/方差。
### GEN52-E03
审计“score loss 降低必使 Wasserstein/FID 同步降低”的主张。
## 解答入口
[[解答 - Marginal Score、Conditional Score 与去噪等价]]
