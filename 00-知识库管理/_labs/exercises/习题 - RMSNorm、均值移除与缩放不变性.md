---
type: exercise
status: draft
area: [neural-networks/normalization, rmsnorm, geometry]
topic: "[[RMSNorm、均值移除与缩放不变性]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - RMSNorm、均值移除与缩放不变性]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - RMSNorm、均值移除与缩放不变性

## A

### NN-RMS-A01
对 $X\in\mathbb R^{B\times T\times D}$ 与 RMSNorm$(D)$，写出统计组数、组大小、$q/r$ keepdim shape、gain shape、参数量、state 与输出 shape。

### NN-RMS-A02
分别判断 RMSNorm core 对共同平移、正尺度、负尺度和逐 feature scale 是否不变；每项注明 $\varepsilon=0$ 或 $\varepsilon>0$。

### NN-RMS-A03
比较访问日 PyTorch RMSNorm 与 LayerNorm 的 affine 参数和默认 epsilon 语义。为什么公平实验应显式设置 epsilon？

## B

### NN-RMS-B01
对 $x=(1,2,2)$、$\gamma=(1,2,1)$、$\varepsilon=0$，完整手算 $q,r,\widehat x,y$，并检查 affine 前平方均值与普通均值。

### NN-RMS-B02
沿用 B01，令上游 $g=(1,1,0)$。手算 $u=\gamma\odot g$、$\overline{u\widehat x}$、$dx$ 与 $d\gamma$，检查 $x^{\mathsf T}dx$ 和 $\boldsymbol1^{\mathsf T}dx$。

### NN-RMS-B03
对 $D=1$，推导 $f(x)=x/\sqrt{x^2+\varepsilon}$ 的导数，并分别讨论 $\varepsilon=0$、$x=0$ 和 $x\ne0$。

## C

### NN-RMS-C01
从 differential 推导
$$
J=\frac1r\left(I-\frac1D\widehat x\widehat x^{\mathsf T}\right),
$$
不得直接引用结论。

### NN-RMS-C02
证明 RMSNorm core 的 $D-1$ 个切向 eigenvalues 与径向 eigenvalue，并说明 $\varepsilon=0$ 时秩。

### NN-RMS-C03
若 $S$ 是从 $D$ 个坐标中均匀无放回抽取的 $k$ 元子集，证明 $q_S=k^{-1}\sum_{j\in S}x_j^2$ 对完整 $q$ 无偏；再解释为什么 normalized output 一般仍有偏。

## D

### NN-RMS-D01
反驳“RMSNorm 输出均值为 0”。给出最小非零反例，并解释 LayerNorm 为什么不同。

### NN-RMS-D02
反驳“fp16 中 RMSNorm 最终输出约为 1，所以中间不会 overflow”。给出 magnitude 阈值与稳定缩放方案。

### NN-RMS-D03
某实现把 denominator 写成 $\sqrt q+\varepsilon$，并称与 $\sqrt{q+\varepsilon}$ 等价。用 $q=0$、$q\ll\varepsilon$ 或导数反驳。

## E

### NN-RMS-E01
为 Transformer 的 LayerNorm→RMSNorm 消融写一份最小公平合同：轴、gain/bias、epsilon、初始化、训练预算、kernel 与评价指标至少各写一项。

### NN-RMS-E02
一个 tensor-parallel 模型把 feature 轴 $D$ 切到四张卡。说明 local RMS 与 global RMS 是不同算子，并设计所需 collective sufficient statistic。

### NN-RMS-E03
设计一个 finite-difference 与极端值测试矩阵，验证自定义 fused RMSNorm 的 forward、VJP、尺度不变性、零输入和 mixed-precision 边界。

