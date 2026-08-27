---
type: exercise
status: draft
area: [generative-models, gan, lipschitz]
topic: "[[Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"
solution: "[[解答 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化
## A. 识别与复述
### GEN21-A01
定义 global $K$-Lipschitz 与 gradient sufficient condition。
### GEN21-A02
比较 clipping、GP、R1、SN 的对象与 target。
### GEN21-A03
写出 feedforward network 的 Lipschitz product upper bound。
## B. 手算与建模
### GEN21-B01
两层线性网络谱范数 3、2，ReLU，求上界。
### GEN21-B02
插值点 gradient norms 为 $(.5,1,2)$，求 target-1 GP 均值。
### GEN21-B03
real gradient norms 为 $(1,2)$、$\gamma=10$，求 R1 penalty。
## C. 推导与证明
### GEN21-C01
由线段积分证明全域 gradient bound 推 Lipschitz。
### GEN21-C02
证明复合函数 Lipschitz 常数至多相乘。
### GEN21-C03
说明 residual block $x+h(x)$ 的上界。
## D. 边界、反例与纠错
### GEN21-D01
构造只在有限采样点 gradient norm 为 1、别处很大的函数。
### GEN21-D02
反驳 weight clipping 等于 1-Lipschitz projection。
### GEN21-D03
反驳 SN 每层归一后完整网络必恰为 1-Lipschitz。
## E. AI 迁移
### GEN21-E01
审计 convolution/residual/normalization 的 Lipschitz 账。
### GEN21-E02
设计 GP sampling support 覆盖实验。
### GEN21-E03
公平比较 GP、R1、SN 的 compute 与目标差异。
## 解答入口
[[解答 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]

