---
type: exercise
status: verified
area: [training, optimization, information-geometry]
topic: "[[自然梯度、KL 局部几何与坐标不变性]]"
solution: "[[解答 - 自然梯度、KL 局部几何与坐标不变性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 自然梯度、KL 局部几何与坐标不变性

> [!abstract] 训练目标
> 从 KL 二阶展开与约束最优化推出自然梯度；能在两套坐标中核对同一 distribution tangent，并准确限定“不变性”的成立条件。

## A. 识别与复述

### TRN20-A01
为什么 Euclidean gradient 不是坐标无关的向量？区分 differential/covector、metric 与由 metric 转换得到的 gradient vector。

### TRN20-A02
写出自然梯度方向、KL trust-region 形式和 Fisher metric。学习率与 KL 半径分别控制什么？

### TRN20-A03
把“自然梯度具有参数化不变性”改写成包含 smooth invertible map、exact metric、exact solve 与 infinitesimal step 的严谨命题。

## B. 手算与构造

### TRN20-B01
Bernoulli 模型以 logit $a$ 参数化，当前 $p=0.8$，观测 $y=1$。计算 ordinary gradient、Fisher、自然下降方向与诱导的 $dp$。

### TRN20-B02
改用概率坐标 $p$，对同一 $y=1$ 计算 ordinary gradient、Fisher 与自然下降方向，验证与上一题的 infinitesimal distribution move 相同。

### TRN20-B03
设二维 $F=\operatorname{diag}(1,9)$、$g=(2,3)^\top$，求未归一化自然下降方向；若约束 $\tfrac12s^\top Fs\le0.02$，求落在边界上的缩放系数与步。

## C. 推导与证明

### TRN20-C01
从 $\mathrm{KL}(p_\theta\|p_{\theta+s})$ 在 $s=0$ 的 Taylor 展开，说明一阶项为何为零、二阶项为何是 $\tfrac12s^\top Fs$。

### TRN20-C02
用拉格朗日乘子求解 $\min_s g^\top s$ subject to $\tfrac12s^\top Fs\le\epsilon$，给出方向和满足边界的尺度。

### TRN20-C03
设 $\theta=\phi(\xi)$、Jacobian 为 $J$。推导 $g_\xi=J^\top g_\theta$ 与 $F_\xi=J^\top F_\theta J$，并证明自然方向经 $J$ pushforward 后一致。

## D. 边界、反例与纠错

### TRN20-D01
用 Bernoulli 的 logit/probability 坐标构造一个有限 Euler step，展示两个参数空间直接加步后终点分布不完全相同；指出差异的阶数来源。

### TRN20-D02
证明加入 Euclidean damping $F+\lambda I$ 后一般不再满足精确坐标协变；可用一维非线性重参数化或非正交线性缩放说明。

### TRN20-D03
反驳：“K-FAC/diagonal Fisher 是 Fisher，因此继承自然梯度的全部不变性。”要求区分 exact metric、结构近似、有限 solve 与 optimizer machinery。

## E. AI 迁移

### TRN20-E01
为 policy 或语言模型中的 natural-gradient step 设计验收日志，至少包括 KL 方向、正反 KL、predicted/actual KL、CG residual、damping 与 sample source。

### TRN20-E02
设计一次坐标不变性单元测试：同一 Bernoulli 分布在 logit 与 probability 坐标各算一步，分别比较 infinitesimal tangent 与 finite endpoint。

### TRN20-E03
比较自然梯度、Newton 与 mirror descent 时，给出一个不会混淆“目标曲率”“分布几何”“Bregman geometry”的三列表述，并指出它们何时可能数值重合。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。完成后逐句标记 exact、local、approximate 或 empirical，再打开 [[解答 - 自然梯度、KL 局部几何与坐标不变性]]。
