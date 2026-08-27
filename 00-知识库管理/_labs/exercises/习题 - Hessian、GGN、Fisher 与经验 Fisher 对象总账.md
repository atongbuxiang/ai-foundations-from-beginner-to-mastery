---
type: exercise
status: verified
area: [training, optimization, curvature]
topic: "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"
solution: "[[解答 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Hessian、GGN、Fisher 与经验 Fisher 对象总账

> [!abstract] 训练目标
> 先写清求导对象、标签来源与期望测度，再比较矩阵；能从复合函数链式法则推出 Hessian 分解，并用最小模型删除不成立的等号。

## A. 识别与复述

### TRN17-A01
分别给出 Hessian、generalized Gauss–Newton（GGN）、true Fisher 与 empirical Fisher 的定义，并写出各自依赖的随机变量与期望测度。

### TRN17-A02
为什么“同为 $P\times P$、对称、PSD”不足以证明两个曲率对象相同？至少指出还必须核对的四个字段。

### TRN17-A03
说明 true Fisher 中“模型采样标签”是什么意思；它与固定训练标签上的 empirical Fisher 有何根本区别？

## B. 手算与构造

### TRN17-B01
二元 logistic 模型取 $p_\theta(y=1\mid x)=\sigma(\theta x)$，$x=2$，当前 $p=0.8$。计算单输入下的 true Fisher；再分别对观测标签 $y=1$ 与 $y=0$ 计算 empirical-Fisher 单样本 outer product。

### TRN17-B02
令 $f_\theta=\theta^2$，$\ell(z)=\tfrac12(z-1)^2$。计算 $J$、输出层 Hessian、GGN、模型二阶残差与真实 Hessian；在 $\theta=0$ 比较它们。

### TRN17-B03
一维 Gaussian 均值模型 $y\sim\mathcal N(\theta,1)$，loss 为 $\tfrac12(\theta-y)^2$。当唯一观测满足 $y=\theta$ 时，求 Hessian、GGN、true Fisher 与 empirical Fisher。

## C. 推导与证明

### TRN17-C01
对 $L(\theta)=\ell(f_\theta(x),y)$，逐指标推出
$$\nabla_\theta^2L=J^\top H_z\ell J+\sum_k\frac{\partial\ell}{\partial z_k}\nabla_\theta^2 f_k.$$
并说明 GGN 删除了哪一项。

### TRN17-C02
证明正则似然模型在可交换微分与积分、支持集不随参数变化等条件下，score 的模型期望为零，并推出 Fisher 的 outer-product 与 expected negative log-likelihood Hessian 两种表达。

### TRN17-C03
对 Bernoulli 自然参数 $a$ 推导 $F(a)=p(1-p)$，并证明交叉熵的输出 Hessian 与它相等；指出这一步为何不能无条件推广到任意 loss 与输出坐标。

## D. 边界、反例与纠错

### TRN17-D01
反驳：“empirical Fisher 是 PSD，所以它一定是可靠的 Hessian 近似。”要求给出一个在最优点退化或尺度错误的明确例子。

### TRN17-D02
构造两个同 shape 且均 PSD 的矩阵估计量，但让它们的 expectation measure 不同；解释为何增加 batch size 也不能自动消除该对象错配。

### TRN17-D03
“交叉熵下 Fisher 总等于 Hessian”缺少哪些量词和条件？把它改写成一条可审计、不过度概括的命题。

## E. AI 迁移

### TRN17-E01
为语言模型的 curvature logger 设计最小 schema，使读者能区分 true Fisher、empirical Fisher、batch-mean outer product 与 GGN。

### TRN17-E02
设计一个自动测试，用有限维 toy model 验证 Hessian 分解、GGN 的 PSD 性和 empirical-Fisher 标签依赖；写出断言而非只写“画图比较”。

### TRN17-E03
在论文或博客声称“用 Fisher 近似 Hessian”时，列出你会追问的证据问题，并给出哪些回答会使结论降级为 heuristic。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`、用时与错误类型。先独立写完“对象—测度—条件”三列表，再打开 [[解答 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]。
