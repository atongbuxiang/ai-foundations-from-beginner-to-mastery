---
type: exercise
status: draft
area: [neural-networks/activations, glu, gating]
topic: "[[GLU、GeGLU、SwiGLU 与乘性门]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - GLU、GeGLU、SwiGLU 与乘性门]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - GLU、GeGLU、SwiGLU 与乘性门
## A
### NN-GLU-A01
写出 GLU、ReGLU、GEGLU、SwiGLU、Bilinear 的统一定义。
### NN-GLU-A02
解释为何 GEGLU/SwiGLU 的“gate”不是 probability gate。
### NN-GLU-A03
比较标准 FFN 与 gated FFN 的矩阵数、参数和 intermediate tensors。
## B
### NN-GLU-B01
从 differential 推导 $H=V\odot\phi(G)$ 对 $V,G$ 的 VJP。
### NN-GLU-B02
继续推出对 $X,W_v,W_g,b_v,b_g$ 的梯度。
### NN-GLU-B03
标准 FFN hidden width 为 $h$；推导 gated FFN 参数匹配的 $h_g$。
## C
### NN-GLU-C01
证明 bilinear gate 每个 coordinate 是输入的 quadratic form。
### NN-GLU-C02
给出 GLU value-path 梯度下界不存在的反例。
### NN-GLU-C03
分析两支 projection 共享输入时 output variance 为什么不能直接乘独立 moments。
## D
### NN-GLU-D01
反驳“参数匹配就等于计算和延迟匹配”。
### NN-GLU-D02
构造 gate 饱和使两支梯度都很小的例子。
### NN-GLU-D03
审计把 GELU-FFN 同宽替换为 SwiGLU 后的准确率提升。
## E
### NN-GLU-E01
为 fused SwiGLU kernel 设计 shape、数值和 backward 验收。
### NN-GLU-E02
设计 baseline/GLU/GEGLU/SwiGLU 三轨公平实验。
### NN-GLU-E03
为 tensor-parallel gated FFN 写通信与 activation-memory 账本。
## 解答入口
[[解答 - GLU、GeGLU、SwiGLU 与乘性门]]
