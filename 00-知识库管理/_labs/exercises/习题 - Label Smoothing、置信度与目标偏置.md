---
type: exercise
status: draft
area: [neural-networks/regularization, label-smoothing, cross-entropy, calibration]
topic: "[[Label Smoothing、置信度与目标偏置]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Label Smoothing、置信度与目标偏置]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Label Smoothing、置信度与目标偏置

## A

### NN-LSM-A01
写出 inclusive uniform Label Smoothing 与 exclude-true convention 的 target vectors，并给出两种 $\epsilon$ 的换算关系。

### NN-LSM-A02
区分 confidence、calibration 与 epistemic uncertainty。Label Smoothing 直接改变其中哪一个数学对象？

### NN-LSM-A03
解释为什么默认 Label Smoothing 的附加项是 $\operatorname{KL}(u\|p)$，而不是 $\operatorname{KL}(p\|u)$ 或直接 entropy penalty。

## B

### NN-LSM-B01
取 $K=5,\epsilon=0.2$、true class 为 3，计算 inclusive uniform target、target entropy，并求最优 true-vs-wrong logit margin。

### NN-LSM-B02
取 $K=3,\epsilon=0.1$、$p=(0.8,0.1,0.1)$。计算 smoothed CE、logit gradient，并与 hard-label gradient 比较。

### NN-LSM-B03
真实 conditional distribution 为 $\eta=(0.7,0.2,0.1)$，$\epsilon=0.2$、$u=(1/3,1/3,1/3)$。计算 population optimal prediction $r_\epsilon$、argmax 与形式反变换。

## C

### NN-LSM-C01
从 cross-entropy 对 target 的线性出发，完整推导 hard-fit/prior-fit 分解与 uniform-prior KL 分解。

### NN-LSM-C02
推导 $\nabla_zH(t,p)=p-t$，并由 $p=t_\epsilon$ 推导 uniform smoothing 的有限 optimal margin。

### NN-LSM-C03
证明 uniform smoothing 在 $\epsilon<1$ 时保持 $\eta$ 的 class ranking；构造 nonuniform prior 改变 argmax 的例子。

## D

### NN-LSM-D01
审计命题：“Label Smoothing 降低 maximum probability，因此模型一定更 calibrated，也更懂得自己不知道什么。”

### NN-LSM-D02
比较 Label Smoothing 与 symmetric label noise transition。分别说明 inclusive 与 exclude-true convention 对应的随机标注机制及抗噪结论边界。

### NN-LSM-D03
分析 class weighting、`ignore_index`、probability targets 与大词表 sampled loss 下的实现歧义；给出小张量验收清单。

## E

### NN-LSM-E01
设计 $\epsilon$、prior 与 convention 的公平实验，要求同时测 accuracy、NLL、Brier、可靠性、classwise risk 与 shift。

### NN-LSM-E02
设计 teacher smoothing 对 knowledge distillation 的三段实验，区分 teacher quality、transfer information 与 student optimization。

### NN-LSM-E03
把“Label Smoothing 能抗标签噪声”改写成三条可证伪窄命题，分别指定 corruption model、estimand 与结论边界。

## 解答入口

[[解答 - Label Smoothing、置信度与目标偏置]]
