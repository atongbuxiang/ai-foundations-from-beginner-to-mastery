---
type: exercise
status: verified
area: [training, optimization, mup, spectral-norm, width-depth]
topic: "[[谱条件、高阶 μP 与参数更新稳定性]]"
solution: "[[解答 - 谱条件、高阶 μP 与参数更新稳定性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 谱条件、高阶 μP 与参数更新稳定性

> [!abstract] 训练目标
> 能把 entry RMS、数据加权平均能量与谱范数分开；能从输入—输出对象合同推导 shape scale，并能识别“逐坐标稳定但最坏方向失稳”的训练风险。

## A. 识别与复述

### TRN47-A01
分别定义并解释矩阵的 entry RMS、数据加权输出能量
$$
\mathbb E\lVert xW\rVert_2^2
$$
与谱范数 $\lVert W\rVert_2$。三者分别回答什么问题？

### TRN47-A02
在线性层 $y=xW$、$W\in\mathbb R^{d_{in}\times d_{out}}$ 中，若输入和输出的坐标 RMS 都应为 $O(1)$，写出自然的谱尺度条件。为什么它是 shape ratio，而不只是“统一令谱范数为 1”？

### TRN47-A03
区分以下四个对象：μP、Muon 或 matrix-sign 型更新方向、shape multiplier、有限步 Newton–Schulz。为什么把它们统称为“Muon 参数化”会造成实验歧义？

## B. 手算与构造

### TRN47-B01
令
$$
A=\frac1n\mathbf1\mathbf1^\top,\qquad
B_{ij}=\frac{\varepsilon_{ij}}n,
$$
其中 $\varepsilon_{ij}$ 为独立随机符号。计算两者的 entry RMS；计算 $\lVert A\rVert_2$，并写出 $\lVert B\rVert_2$ 的典型量级。两者的谱风险相差多少？

### TRN47-B02
对 $W\in\mathbb R^{1024\times4096}$ 的 iid Gaussian 初始化，使用近似
$$
\lVert W\rVert_2\asymp\sigma(\sqrt{d_{in}}+\sqrt{d_{out}})
$$
并要求 $\lVert W\rVert_2\asymp\sqrt{d_{out}/d_{in}}$。求 $\sigma$。与 fan-in 标准差 $1/\sqrt{d_{in}}$ 比较。

### TRN47-B03
残差网络有 $L$ 个分支，每个未缩放分支更新向量的范数为 $c$。分别在所有更新完全同向和两两近似正交时，估计总更新的量级。为使总量为 $O(c)$，$\alpha_L$ 各应取什么量级？

## C. 推导与证明

### TRN47-C01
从
$$
\lVert xW\rVert_2\le \lVert x\rVert_2\lVert W\rVert_2
$$
以及坐标 RMS 合同，推导
$$
\lVert W\rVert_2=O\!\left(\sqrt{d_{out}/d_{in}}\right).
$$
为什么这一步只直接给出充分的上界尺度，而不能在没有额外假设时证明对应的 $\Theta$ 下界？

### TRN47-C02
设局部目标的一阶变化为 $\langle G,\Delta W\rangle_F$，约束 $\lVert\Delta W\rVert_2\le\rho$。利用谱范数—核范数对偶，证明最优值是 $-\rho\lVert G\rVert_*$，并给出 $G=U\Sigma V^\top$ 时的一个最速方向。

### TRN47-C03
由
$$
W_t=W_0+\sum_{s<t}\Delta W_s
$$
证明谱范数上界。再构造两条每步均满足 $\lVert\Delta W_s\rVert_2=\rho$ 的更新序列：一条使参数谱范数线性增长，另一条使两步后回到初始值。

## D. 边界、反例与纠错

### TRN47-D01
构造两个 $n\times n$ 矩阵，使它们具有相同 entry RMS $1/n$，但谱范数分别为 $1$ 与典型 $O(n^{-1/2})$。这反驳了什么常见诊断？

### TRN47-D02
给出一个“所有层的归一化谱范数都稳定，但模型性能很差”的具体情形。说明为什么 operator stability 是安全门，而不是充分的学习保证。

### TRN47-D03
一篇 width–depth 联合缩放预印本在特定残差架构、优化器与训练时域上得到稳定性结论。哪些条件未验证时，不能把结果写成“任意深度 Transformer 都满足该定律”？

## E. AI 迁移

### TRN47-E01
为 Transformer 的 embedding、Q/K/V/O、FFN up/down、readout 与 norm 参数组设计谱遥测清单。至少包含 shape、entry RMS、Frobenius norm、spectral estimate、update spectral ratio、effective rank 与数据加权 feature change。

### TRN47-E02
设计一个 power iteration 审计，验证日志里的谱范数估计没有因迭代不足而系统偏低。规定初始化、迭代次数梯度、残差或收敛指标、精确 SVD 对照子集与允许误差。

### TRN47-E03
设计一个 width–depth 联合实验，区分 width parameterization 失误、residual multiplier 失误与长时同向累积。写出最小网格、控制变量、三类遥测和预注册失败门。

## 作答与复盘

查看 [[解答 - 谱条件、高阶 μP 与参数更新稳定性]] 前，对每个结论标出它属于“典型随机方向”“数据分布上的平均方向”还是“最坏方向”。
