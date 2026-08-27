---
type: exercise
status: draft
area: [neural-networks/differentiation, jvp, vjp]
topic: "[[局部微分、Jacobian、JVP 与 VJP]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - 局部微分、Jacobian、JVP 与 VJP]]", "[[标量链式法则与反向传播递推]]"]
solution: "[[解答 - 局部微分、Jacobian、JVP 与 VJP]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 局部微分、Jacobian、JVP 与 VJP
## A. 识别与复述
### NN-JVP-A01
区分 Fréchet derivative、Jacobian matrix、JVP 与 VJP，标出形状。
### NN-JVP-A02
解释为何么 VJP 是 cotangent pullback，而不是 Jacobian 求逆。
### NN-JVP-A03
说明 per-example Jacobian、batch-aggregated gradient 与 full Jacobian 的区别。
## B. 手算与建模
### NN-JVP-B01
对 $f(x_1,x_2)=(x_1x_2,\sin x_1)$，在 $(2,3)$ 计算 $J$、$v=(1,-1)^T$ 的 JVP 和 $u=(4,5)^T$ 的 VJP。
### NN-JVP-B02
对 $f(x)=(x_1^2+x_2,e^{x_1-x_2},x_1x_2)$，在 $(1,2)$ 计算 $Jv$，其中 $v=(2,-1)^T$；不必先写完整 Jacobian。
### NN-JVP-B03
对 broadcast $Y_{btd}=X_{btd}+c_d$ 和 reduction $s_d=\sum_{b,t}Y_{btd}$，写出两个算子的 JVP/VJP。
## C. 推导与证明
### NN-JVP-C01
从 differential pairing 证明 $u^T(Jv)=(J^Tu)^Tv$，并说明 dot test 能检测什么。
### NN-JVP-C02
对 $h=g\circ f$ 分别推出 JVP 的正序组合和 VJP 的逆序组合。
### NN-JVP-C03
比较得到 full $m\times n$ Jacobian 时 forward seeds 与 reverse seeds 的数量，给出两种模式的选择原则。
## D. 边界、反例与纠错
### NN-JVP-D01
给出“所有坐标偏导存在但不 Fréchet 可微”的二元函数，并验证。
### NN-JVP-D02
分析 ReLU 在 $0$、max 在 tie 处和 discrete branch 的 AD 返回值为何不能自动视为 classical derivative。
### NN-JVP-D03
反驳：“一次有限差分通过，就证明 VJP 实现在所有输入和方向都正确。”
## E. AI 迁移
### NN-JVP-E01
为大语言模型的 scalar loss 与参数梯度选择 JVP/VJP 模式，并说明原因。
### NN-JVP-E02
设计一个不物化 full Jacobian 的 Jacobian spectral-norm 估计思路。
### NN-JVP-E03
为 custom operator 的 JVP/VJP 制定 shape、dot-test、finite-difference 与 nondifferentiable-boundary 验收。
## 解答入口
[[解答 - 局部微分、Jacobian、JVP 与 VJP]]
