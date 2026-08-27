---
type: exercise
status: draft
area: [neural-networks/gradient-checking, checkpointing, higher-order-differentiation]
topic: "[[Gradient Checking、Checkpointing 与高阶微分边界]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - Gradient Checking、Checkpointing 与高阶微分边界]]", "[[激活函数、门控与非线性 MOC]]"]
solution: "[[解答 - Gradient Checking、Checkpointing 与高阶微分边界]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Gradient Checking、Checkpointing 与高阶微分边界
## A. 识别与复述
### NN-GC-A01
区分方向中心差分、Taylor residual test 和 JVP/VJP dot test 的检查对象。
### NN-GC-A02
定义 activation checkpointing/rematerialization，说明它用什么资源换什么资源。
### NN-GC-A03
区分 full Hessian、Hessian–vector product 和不可微点的框架二阶 convention。
## B. 手算与建模
### NN-GC-B01
对 $f(x)=x^3$、$x=2$、$h=0.01$，计算中心差分，与真导数 12 比较。
### NN-GC-B02
对 $f(x)=\sin(x^2)$ 在 $x=1$，写出 Taylor residual $R(h)$ 和理想减半比率；说明何时比率会失效。
### NN-GC-B03
链长 $n=100$，每隔 $k=10$ 层 checkpoint。用 $n/k+k$ 账本估算 peak activation units，并与全保存比较。
## C. 推导与证明
### NN-GC-C01
从 $E(h)=C_1h^2+C_2u/h$ 推出最佳 $h$ 的 $u^{1/3}$ 量级。
### NN-GC-C02
最小化 $n/k+k$，推出 $k\approx\sqrt n$ 与 $O(\sqrt n)$ peak memory。
### NN-GC-C03
从 $Hv=\left.\frac d{d\varepsilon}\nabla f(x+\varepsilon v)\right|_0$ 解释 forward-over-reverse HVP，并推出对称 dot test。
## D. 边界、反例与纠错
### NN-GC-D01
反驳：“一个固定 `eps=1e-6` 在所有 dtype、输入 scale 和函数上都是正确 gradcheck 步长。”
### NN-GC-D02
给出 dropout checkpoint 重放不保存 RNG state 时 gradient 改变的逻辑链。
### NN-GC-D03
反驳：“ReLU 的框架 Hessian 在 0 处返回 0，因此 classical Hessian 存在且等于 0。”
## E. AI 迁移
### NN-GC-E01
为 custom fused kernel 设计四层 gradient-checking 漏斗。
### NN-GC-E02
为 Transformer 分析 checkpoint 分割，列出 activation bytes、FLOPs、skip/live tensors、RNG 和 communication 指标。
### NN-GC-E03
为 implicit layer 的 HVP 设计 forward residual、adjoint residual、step sweep、symmetry 与 solver-tolerance 验收。
## 解答入口
[[解答 - Gradient Checking、Checkpointing 与高阶微分边界]]
