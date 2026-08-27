---
type: exercise
status: verified
area: [training, optimization, parameterization, ntk, mean-field]
topic: "[[Standard、NTK 与 Mean-field 参数化]]"
solution: "[[解答 - Standard、NTK 与 Mean-field 参数化]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Standard、NTK 与 Mean-field 参数化

> [!abstract] 训练目标
> 能从 stored coordinate、initialization、forward multiplier 与 group LR 推断无限宽训练 regime，不把相同初始函数、无限宽与 fixed kernel 混为一谈。

## A. 识别与复述

### TRN42-A01
参数化四元组包含哪些对象？为什么只写“权重服从 He 初始化”还不能确定训练 regime？

### TRN42-A02
分别用一句话说明 standard、NTK-style、mean-field 与 μP 的主要极限目标和最常见误读。

### TRN42-A03
定义 empirical NTK、kernel drift、relative feature change 与 linearization error；它们各自排除不了什么？

## B. 手算与构造

### TRN42-B01
令 $z_i$ iid、均值 0、方差 9。对
$$
f_n=c_n\sum_{i=1}^nz_i
$$
分别取 $c_n=1,\ n^{-1/2},\ n^{-1}$，计算 $\operatorname{Var}(f_n)$ 及极限趋势。

### TRN42-B02
对
$$
f_n(x)=\frac1{\sqrt n}\sum_{i=1}^na_i\phi(w_i^\top x)
$$
和平方损失，假设 residual、$a_i,\phi,\phi',x$ 都为 $O(1)$。求 $\partial L/\partial a_i$、$\partial L/\partial w_i$ 的量级；$O(1)$ LR 下有限步 parameter motion 与聚合 output motion 各是什么量级？

### TRN42-B03
对 mean-field 形式 $f_n=n^{-1}\sum_i a_i\phi_i$，若单粒子 gradient 为 $O(1/n)$，分别求 LR 为 $1,\sqrt n,n$ 时单粒子一步 motion。哪一种给非退化 particle dynamics？

## C. 推导与证明

### TRN42-C01
令 $\widetilde a_i=\lambda_na_i$、$\widetilde c_n=c_n/\lambda_n$。证明初始函数相同；推导两坐标下梯度与等价 LR 的换算。

### TRN42-C02
平方损失下，若 $f(\theta)$ 在初始化附近线性化为 $f_0+J_0(\theta-\theta_0)$，推导连续时间
$$
\dot f_t=-K_0(f_t-y),\qquad K_0=J_0J_0^\top.
$$

### TRN42-C03
若 $K_0=Q\Lambda Q^\top$，求各 eigenmode residual 的时间演化。解释小 eigenvalue 模式为何收敛慢，但这本身不等于泛化差。

## D. 边界、反例与纠错

### TRN42-D01
反驳：“只要 width 趋于无穷，网络就等于 NTK。”给出 parameterization 和 feature-learning 极限两层纠正。

### TRN42-D02
构造两个表示同一函数的坐标系统，却在使用相同 raw LR 时产生不同一步输出的例子。

### TRN42-D03
为什么“kernel drift 小，所以模型没有学到任何东西”错误？为什么“kernel drift 大，所以 feature learning 一定有益”也错误？

## E. AI 迁移

### TRN42-E01
设计一个区分 lazy 与 feature-learning 的 width ladder，至少规定四个 width、三个时刻、四个统计量和一个线性化对照。

### TRN42-E02
审计框架默认 MLP 的“standard parameterization”：写出 input/hidden/output weight 的 shape、init、forward 和 LR；指出哪一项若缺失就不能跨宽比较。

### TRN42-E03
给一位初学者写一个安全结论模板，用来报告“某 Transformer 在宽度窗口内呈 NTK-like 趋势”，不得外推到无限训练时间或泛化。

## 作答与复盘

先在纸上推导 B02/B03，再查看 [[解答 - Standard、NTK 与 Mean-field 参数化]]。重点记录自己是否把“输出更新 $O(1)$”误当成“单元 feature 更新 $O(1)$”。
