---
type: exercise
status: draft
area: [math/probability, math/statistics, ai/uncertainty]
topic: "中心极限定理与 Delta 方法"
difficulty: [A, B, C, D, E]
prerequisites: ["[[中心极限定理与 Delta 方法]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 中心极限定理与 Delta 方法]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 中心极限定理与 Delta 方法

> [!abstract] 训练目标
> 检查能否正确标准化、辨别渐近与有限样本、重建 CLT/Delta 证明路线，处理多元协方差和一阶退化，并审计 AI 中 Gaussian-noise 声明。

## 使用方式

1. 每道 CLT 题先写均值、方差和标准化尺度；
2. 每个 $\approx$ 必须说明误差对象与近似条件；
3. Delta 题先算真参数处导数/Jacobian，再判断是否退化；
4. 每题记录状态、用时和错误类型。

## A. 识别与复述

### PROB-CLT-A01

准确陈述 iid Lindeberg–Lévy CLT 的假设和两种等价结论（和、样本平均）。解释为何方差必须非零且有限。

### PROB-CLT-A02

比较 LLN、CLT、Gaussian 线性闭包、Berry–Esseen 与浓缩不等式：分别回答研究对象、结论类型和不能提供的内容。

### PROB-CLT-A03

陈述一维和多元 Delta 方法，给出 Jacobian 形状。说明 $g'(\theta)=0$、真参数在边界或 $g$ 不可微时为什么不能机械使用一阶公式。

## B. 手算与构造

### PROB-CLT-B01

$S\sim\operatorname{Binomial}(100,0.5)$。用带连续性修正的正态近似计算 $P(45\le S\le55)$，写出两个 $z$ 值和近似结果。

### PROB-CLT-B02

$X_i\overset{iid}{\sim}\operatorname{Exp}(\lambda)$（rate），$\overline X_n$ 用来估计 $1/\lambda=\mu$。求 $\log\overline X_n$ 的渐近分布和近似标准误；说明定义域风险。

### PROB-CLT-B03

已知

$$
\sqrt n\left(
\begin{bmatrix}A_n\\B_n\end{bmatrix}
-\begin{bmatrix}2\\4\end{bmatrix}
\right)
\xrightarrow d\mathcal N\left(0,
\begin{bmatrix}4&1\\1&9\end{bmatrix}\right).
$$

用多元 Delta 求 $A_n/B_n$ 的渐近方差，保留协方差交叉项。

## C. 推导与证明

### PROB-CLT-C01

对标准化 iid 变量 $Y_i$，从 $\varphi_Y(t)=1-t^2/2+o(t^2)$ 出发，逐步推出标准化和的特征函数趋于 $e^{-t^2/2}$。指出 iid 和有限二阶矩的使用位置。

### PROB-CLT-C02

用 Cramér–Wold 装置从标量 CLT 推导固定维度多元 CLT。对任意 $a\in\mathbb R^d$ 计算投影均值与方差，并处理 $a^\top\Sigma a=0$。

### PROB-CLT-C03

证明一维 Delta 方法。随后在 $g'(\theta)=0,g''(\theta)\ne0$ 时推导二阶 Delta 的尺度与极限。

## D. 边界、反例与纠错

### PROB-CLT-D01

用 Cauchy 分布反驳“任何 iid 样本平均都渐近 Gaussian”。写出样本平均的分布不变性，并定位经典 CLT 失效条件。

### PROB-CLT-D02

令 $T_n=1/n\to0$，$g(x)=\mathbf1_{\{x>0\}}$。解释连续映射/Delta 方法为什么不能给出 $g(T_n)\to g(0)$，并给出实际极限。

### PROB-CLT-D03

反驳：“batch 中每个梯度坐标看起来近似 Gaussian，所以整个 $p$ 维梯度噪声是 iid isotropic Gaussian。”列出至少四个逻辑缺口。

## E. AI 迁移

### PROB-CLT-E01

固定参数 $\theta$ 和方向 $v\in\mathbb R^p$，单样本梯度 $g_i(\theta)$ 条件 iid、均值 $\nabla R(\theta)$、协方差 $\Sigma_g$。写出 batch size $B$ 下方向投影 CLT；说明它不能推出哪些更强结论。

### PROB-CLT-E02

测试集 token loss 平均为 $\bar\ell$，perplexity $P=e^{\bar\ell}$。用 Delta 给出标准误传播。若 token 按文档聚类相关，说明为何不能用 token 数作 iid $n$，并给出两种修正方向。

### PROB-CLT-E03

神经元 preactivation $h_d=\sum_{i=1}^dW_ix_i$。提出一组足以支持标量 CLT 的尺度/独立条件，并构造一个“单坐标支配”序列使 Lindeberg 机制失败。解释单输入标量 CLT 到多输入 GP 极限还缺什么。

## 分级提示

### 方向提示

- `B02`：Exponential 的均值/方差是 $1/\lambda,1/\lambda^2$；$g'(\mu)=1/\mu$。
- `B03`：$\nabla(a/b)=(1/b,-a/b^2)^\top$。
- `C03`：写 $g(T_n)-g(\theta)=g'(\theta)(T_n-\theta)+o_P(|T_n-\theta|)$。
- `E03`：要求最大单项方差占总方差的比例趋零。

### 结构提示

- `C01`：独立性给 $[\varphi_Y(t/\sqrt n)]^n$，再取极限。
- `E02`：按文档 cluster sandwich 或 cluster bootstrap。

## 解答入口

完成独立尝试后再打开：[[解答 - 中心极限定理与 Delta 方法]]。

## 本轮复盘

- 是否把渐近分布写成有限样本等号？
- 是否漏掉 $\sqrt n$、协方差交叉项或连续性修正？
- 是否在导数为零/不连续处仍套一阶 Delta？
- 计划何时无提示重做？

