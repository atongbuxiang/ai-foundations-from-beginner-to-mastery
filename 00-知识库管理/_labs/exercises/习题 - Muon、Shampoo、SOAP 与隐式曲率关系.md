---
type: exercise
status: verified
area: [training, optimization, muon, preconditioning]
topic: "[[Muon、Shampoo、SOAP 与隐式曲率关系]]"
solution: "[[解答 - Muon、Shampoo、SOAP 与隐式曲率关系]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Muon、Shampoo、SOAP 与隐式曲率关系

> [!abstract] 训练目标
> 用“随机对象—state—变换—几何声明—成本”比较矩阵优化器；能用最小反例拆掉 Muon=Shampoo=SOAP=K-FAC 的错误等价。

## A. 识别与复述

### TRN30-A01
分别给出 Muon、matrix Shampoo、SOAP 与 K-FAC 的 instantaneous signal、persistent state 和核心 transformation。

### TRN30-A02
四种方法中，哪些直接积累 gradient Gram，哪些使用 activation/backprop covariance，哪些只对当前 momentum matrix 做 polar？

### TRN30-A03
为什么“隐式曲率”必须指定所近似的 Hessian、GGN、Fisher 或其他 metric？列出对象相等至少要核对的字段。

## B. 手算与构造

### TRN30-B01
当前梯度为 $G_2=I_2$。历史一取 $G_1=\operatorname{diag}(10,1)$，历史二取 $G_1=\operatorname{diag}(1,10)$。忽略 damping，计算两条历史的 Shampoo 左右 diagonal factors 的相对大小，并与重置 momentum 的 Muon update 比较。

### TRN30-B02
令单样本 gradient $G=x^T\delta$。把 $x$ 乘 $c$、$\delta$ 除以 $c$，证明 $G$ 不变而 K-FAC factors 按 $c^2$ 与 $c^{-2}$ 改变；讨论 damping 为何破坏简单抵消。

### TRN30-B03
对 diagonal gradients，写出 Shampoo update $L^{-1/4}GR^{-1/4}$ 的逐坐标形式。比较它与 polar$(G)$ 的 sign-like 形式，给出二者相等和不相等的例子。

## C. 推导与证明

### TRN30-C01
从矩阵 gradient history 定义推导 Shampoo 的 $L_t,R_t$ shape 与 $-1/4$ 双侧 exponent 如何合成 coordinate scaling。

### TRN30-C02
对线性层 $y=xW$ 推导单样本 vectorized gradient 的 Kronecker outer-product 结构，并说明 K-FAC 在哪一步使用 expectation factorization。

### TRN30-C03
证明只知道当前 $G_t$ 一般无法恢复 Shampoo history state 或 K-FAC activation/backprop factors；用信息丢失/多对一映射表述。

## D. 边界、反例与纠错

### TRN30-D01
反驳“Muon 内部计算 $G^TG$，所以它估计了 Fisher”。区分临时 polynomial algebra 与跨样本 expectation state。

### TRN30-D02
反驳“Shampoo 和 SOAP 只差是否做 SVD”。指出 SOAP 在旋转基中额外维护的 state、时钟与非线性。

### TRN30-D03
把“Muon 是便宜的二阶优化器”改写为三个证据等级：可严格支持、合理机制假说、目前不能宣称。

## E. AI 迁移

### TRN30-E01
设计一个 toy experiment，使当前 gradient 相同但 gradient history、activation covariance 或 label law 不同，以同时区分四种方法。

### TRN30-E02
设计同预算 benchmark 比较四种方法。列出 state bytes、matrix ops、refresh frequency、communication、调参预算与 quality 轴。

### TRN30-E03
阅读一篇声称“optimizer X approximates natural gradient”的论文时，写出审计清单：从 random object 到 inverse solve 和 empirical evidence 至少包含十项。

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。答案若只写“都是预条件”而没有 state equation，视为未完成；之后打开 [[解答 - Muon、Shampoo、SOAP 与隐式曲率关系]]。
