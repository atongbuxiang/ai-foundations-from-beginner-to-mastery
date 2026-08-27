---
type: exercise
status: verified
area: [training, scaling-laws, statistics]
topic: "[[经验 Scaling Law、幂律拟合与不可约项]]"
solution: "[[解答 - 经验 Scaling Law、幂律拟合与不可约项]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 经验 Scaling Law、幂律拟合与不可约项

> [!abstract] 训练目标
> 能把经验幂律写成带对象、区间、不可约项和噪声模型的可证伪命题，并识别 log–log 直线在有限窗口中的系统偏差。

## A. 识别与复述

### TRN49-A01
区分“经验 Scaling Law”“渐近定理”和“机制解释”。式 $L(x)=E+Ax^{-\alpha}$ 的一次良好拟合分别能、不能支持什么结论？

### TRN49-A02
解释 $E,A,\alpha$ 的含义与量纲。为什么改变 loss 定义、tokenizer 或评测分布后，三者通常不能直接搬用？

### TRN49-A03
比较原尺度加性误差 $L_i=f(x_i)+\varepsilon_i$ 与对数尺度加性误差 $\log L_i=\log f(x_i)+\eta_i$。它们分别隐含怎样的误差权重？

## B. 手算与构造

### TRN49-B01
令 $L(x)=1+4x^{-1/2}$。计算 $x=1,4,16,64$ 时的 loss，并分别计算相邻两点的原始 loss 对数斜率。它们为何不等于 $-1/2$？

### TRN49-B02
真实模型为 $L(x)=2+8x^{-0.4}$。研究者忽略 $E$，用 $x=10^2$ 与 $10^4$ 两点拟合 $L\approx Kx^{-\hat\alpha}$。求 $\hat\alpha$，并判断偏差方向。

### TRN49-B03
构造两组在观测区间 $x\in[10^2,10^3]$ 很接近、但在 $x=10^8$ 外推显著不同的曲线：一条带 offset 的幂律，一条无 offset 幂律。说明有限窗口可辨识性问题。

## C. 推导与证明

### TRN49-C01
对 $L(x)=E+Ax^{-\alpha}$ 推导
$$
\frac{d\log L}{d\log x}=-\alpha\left(1-\frac{E}{L(x)}\right),
$$
并解释 $x\to\infty$ 时原始 loss 曲线为什么会变平。

### TRN49-C02
令 excess loss $R(x)=L(x)-E$。证明 $d\log R/d\log x=-\alpha$。若使用错误 offset $\widetilde E=E+\delta$，推导观察到的局部斜率。

### TRN49-C03
写出原尺度高斯误差与 log 尺度高斯误差对应的负对数似然（忽略常数），并说明为什么它们会给大 loss 点不同的影响力。

## D. 边界、反例与纠错

### TRN49-D01
反驳：“log–log 图的 $R^2=0.999$，因此该幂律在任意更大尺度都成立。”至少指出区间、函数族和 held-out 三个缺口。

### TRN49-D02
解释为什么把 $E$ 固定为 0 可能得到稳定却错误的指数；给出一个随着观测窗口右移、$\hat\alpha$ 持续下降的例子。

### TRN49-D03
某实验只报告每个尺度最优 seed 的 loss。说明这会如何改变噪声分布和幂律斜率，并给出更合适的报告对象。

## E. AI 迁移

### TRN49-E01
为“验证语言模型 validation cross-entropy 随训练 token 的幂律”写一个 fit manifest，至少包含八项字段。

### TRN49-E02
设计带 calibration scales、validation scales 与 held-out extrapolation scales 的实验；明确模型选择和最终评分各在哪一部分完成。

### TRN49-E03
把“模型 loss 遵循普遍幂律”改写成一条不过度外推、可复核且可被未来尺度否证的结论。

## 作答与复盘

先画原尺度与 log–log 两张图，再查看 [[解答 - 经验 Scaling Law、幂律拟合与不可约项]]。每题标记 independent / hinted / copied / blocked，并记录自己混淆的是 offset、窗口、噪声模型还是证据强度。
