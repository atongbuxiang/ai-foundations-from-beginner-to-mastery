---
type: exercise
status: draft
area: [neural-networks/activations, smooth-rectifiers]
topic: "[[Softplus、GELU、SiLU 与平滑门控]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Softplus、GELU、SiLU 与平滑门控]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Softplus、GELU、SiLU 与平滑门控
## A
### NN-SMO-A01
写出 Softplus、GELU、SiLU 的定义、导数、值域与单调/凸性。
### NN-SMO-A02
区分 soft-max、self-gating 与 convolution smoothing。
### NN-SMO-A03
说明 exact/approximate GELU 为什么是实现合同而非无关细节。
## B
### NN-SMO-B01
证明 $\operatorname{ReLU}(x)\le\operatorname{softplus}_\beta(x)\le\operatorname{ReLU}(x)+\log2/\beta$。
### NN-SMO-B02
计算 GELU 的一、二阶导，并找出曲率变号点。
### NN-SMO-B03
对 $f_\beta=x\sigma(\beta x)$ 求导并分析 $\beta\to0,\infty$。
## C
### NN-SMO-C01
证明稳定 Softplus 恒等式并解释 `log1p` 的作用。
### NN-SMO-C02
证明 Gaussian convolution of ReLU 为 $x\Phi(x)+\varphi(x)$，从而不等于 GELU。
### NN-SMO-C03
推导 GELU/SiLU VJP，并指出 slope 可超出 $[0,1]$。
## D
### NN-SMO-D01
反驳“平滑激活一定更容易优化”。
### NN-SMO-D02
构造 forward 近似误差很小但 derivative 误差显著的情形。
### NN-SMO-D03
审计训练 exact GELU、推理 approximate GELU 的模型合同。
## E
### NN-SMO-E01
设计 FP16/BF16 smooth-activation kernel 验收。
### NN-SMO-E02
设计 ReLU/Softplus/GELU/SiLU 的 matched-budget 消融。
### NN-SMO-E03
为 positive scale output 比较 Softplus 与 exponential。
## 解答入口
[[解答 - Softplus、GELU、SiLU 与平滑门控]]
