---
type: exercise
status: draft
area: [neural-networks/normalization, batch-normalization, backpropagation]
topic: "[[BatchNorm 反向传播、尺度不变性与噪声]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - BatchNorm 反向传播、尺度不变性与噪声]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - BatchNorm 反向传播、尺度不变性与噪声

## A

### NN-BNB-A01
写出单 channel、组大小 $m$ 的 $d\beta,d\gamma,d x_i$ 闭式公式，并定义 $\overline g$ 与 $\overline{g\widehat x}$。

### NN-BNB-A02
写出 train-mode normalization Jacobian 元素，指出为何 $i\ne k$ 时也可能非零；再写 eval-mode 对应 Jacobian。

### NN-BNB-A03
列出 BatchNorm batch-statistic noise 的五个性质，并说明它与 Dropout 的 Bernoulli mask 有何结构差异。

## B

### NN-BNB-B01
对 $x=(-1,0,1)$、$\gamma=1,\beta=0,\varepsilon=0$、上游 $g=(1,0,0)$，计算 $\widehat x,\overline g,\overline{g\widehat x}$ 与全部 $dx$，检查 $\sum dx_i$ 和 $x^{\mathsf T}dx$。

### NN-BNB-B02
同一组取 $\widehat x=(-1,1)$、上游 $g=(3,-1)$。求 $d\beta,d\gamma$；若 $\gamma=2,q=1,\varepsilon=0$，再求 $dx$ 并解释为何可能全为零。

### NN-BNB-B03
某 scale-invariant weight 的 norm 从 2 放大到 10。忽略 epsilon、regularizer 与 optimizer state，比较 raw gradient norm 和相对 angular step 的倍率。

## C

### NN-BNB-C01
从 $d\mu,dq,dr$ 出发推导
$$d\widehat x=\frac1r\left(P-\widehat x\widehat x^{\mathsf T}/m\right)dx.$$
每一步注明使用了哪个正交关系。

### NN-BNB-C02
证明对任意 $\varepsilon$ 有 $\boldsymbol1^{\mathsf T}\nabla_xL=0$；再推导 radial eigenvalue
$$\varepsilon/(q+\varepsilon)^{3/2}.$$

### NN-BNB-C03
若 $L(a w)=L(w)$ 对所有 $a>0$ 成立，证明
$$w^{\mathsf T}\nabla_wL=0,\qquad
\nabla_{aw}L=a^{-1}\nabla_wL.$$
说明 finite-step SGD 的角度变化为何近似按 $a^{-2}$。

## D

### NN-BNB-D01
反驳：“BatchNorm 反向只是把上游梯度乘 $\gamma/\sqrt{q+\varepsilon}$。”

### NN-BNB-D02
反驳：“BatchNorm Jacobian 总有两个精确零奇异值。”分别讨论 $\varepsilon>0$、$q=0$ 与 $m=1$。

### NN-BNB-D03
反驳：“BN 使函数对 weight norm 不变，所以 weight decay、parameter norm 和 learning rate 都不再重要。”

## E

### NN-BNB-E01
设计 train/eval 双模式 gradcheck，规定 dtype、difference step、loss、batch shape、比较指标以及 constant/near-constant group。

### NN-BNB-E02
设计 companion-batch sensitivity 实验，区分 batch coupling 与普通 loss reduction 引入的 $1/m$ 因子，并测量输出/输入梯度的 cross-sample Jacobian。

### NN-BNB-E03
设计 scale scan：令 $w\mapsto aw$，记录 loss、raw gradient、$w^{\mathsf T}g$、angular update、weight decay 与 epsilon 区域；说明什么证据才支持近似尺度不变性。

## 解答入口

[[解答 - BatchNorm 反向传播、尺度不变性与噪声]]

