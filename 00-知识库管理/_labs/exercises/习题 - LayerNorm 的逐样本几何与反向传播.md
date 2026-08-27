---
type: exercise
status: draft
area: [neural-networks/normalization, layer-normalization, geometry]
topic: "[[LayerNorm 的逐样本几何与反向传播]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - LayerNorm 的逐样本几何与反向传播]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - LayerNorm 的逐样本几何与反向传播

## A

### NN-LN-A01
对输入 $(B,T,D)$ 与 LayerNorm$(D)$，写出统计组数、每组大小、mean/variance shape、gain/bias shape、参数量与输出 shape。

### NN-LN-A02
写出一个 token 的 LayerNorm forward、vector-gain backward 与参数梯度；说明 $\gamma$ 为向量时为何不能直接提到投影括号外。

### NN-LN-A03
用一句精确陈述区分“LayerNorm 不依赖 batch size”“LayerNorm Jacobian 是 diagonal”“含 LayerNorm 的模型 train/eval 相同”三句话的真假。

## B

### NN-LN-B01
对 $x=(1,2,3)$、$\gamma=(1,2,1)$、$\beta=(0,1,0)$、$\varepsilon=0$ 完整计算 forward，并检查 affine 前后的 mean。

### NN-LN-B02
沿用 B01，取上游 $g=(1,1,0)$，计算 $u,\overline u,\overline{u\widehat x},dx,d\gamma,d\beta$，检查两个正交关系。

### NN-LN-B03
分别计算 $D=1$ 的 LayerNorm 输出/Jacobian，以及 $D=2,\varepsilon=0,x_1\ne x_2$ 的 normalized output；解释局部 Jacobian。

## C

### NN-LN-C01
证明 $\varepsilon=0,q>0$ 时 normalized vector 位于
$$\boldsymbol1^\perp\cap\{\|z\|=\sqrt D\},$$
并解释该流形为何有 $D-2$ 个局部自由度。

### NN-LN-C02
推导无 affine Jacobian 在 $\boldsymbol1$、$\widehat x$ 和二者正交补上的 eigenvalue；再说明非均匀 vector gain 后为什么应讨论奇异值而非直接沿用 eigenvalue。

### NN-LN-C03
证明 LayerNorm 对共同平移精确不变；对正尺度在 $\varepsilon=0$ 精确不变；给出 $\varepsilon>0$ 的误差表达式。

## D

### NN-LN-D01
反驳：“LayerNorm 不跨样本，因此每个 feature 的梯度只依赖自己的上游梯度。”

### NN-LN-D02
反驳：“LayerNorm train/eval 统计公式相同，所以 Transformer 的训练和推理前向一定完全一致。”

### NN-LN-D03
某人把图像 $(N,C,H,W)$ 直接设 LayerNorm normalized shape 为 $(C,H,W)$，却声称这等价于每像素只归一化 channel。指出轴错误并写出两个算子的真实统计组。

## E

### NN-LN-E01
为 autoregressive Transformer 审计 LayerNorm normalized shape 与 causality：列出不会跨 token 的安全合同、会泄漏未来的错误合同和对应最小反例。

### NN-LN-E02
设计 LayerNorm 数值稳定实验，扫描 offset、variance、epsilon、D、fp32/fp16/bf16 与 accumulation dtype；规定 forward/backward 检查量。

### NN-LN-E03
Conditional LayerNorm 令 $\gamma(c),\beta(c)\in\mathbb R^D$。画出文字版计算图，给出 condition batch/token shape、广播规则、参数梯度路径与一个 zero-initialized conditioning head 的第一步学习边界。

## 解答入口

[[解答 - LayerNorm 的逐样本几何与反向传播]]

