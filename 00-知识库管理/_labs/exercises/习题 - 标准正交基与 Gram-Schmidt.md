---
type: exercise
status: draft
area: [labs, math/linear-algebra]
topic: "[[标准正交基与 Gram-Schmidt]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[内积空间]]", "[[正交投影]]"]
related: ["[[QR 分解]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 标准正交基与 Gram-Schmidt]]"
created: 2026-08-14
updated: 2026-08-14
---

# 习题 - 标准正交基与 Gram-Schmidt

> [!abstract] 训练目标
> 检查是否能辨认矩形标准正交列、完整手算 Gram–Schmidt、证明输出性质、定位线性相关时的失败步骤，并区分“正交”与“统计独立”。

## 使用方式

先关闭正文和解答。每题都写出对象所在空间、关键中间式和检查；卡住时只看对应级别提示。

## A. 识别与复述

### LA-GS-A01

令

$$
\boldsymbol Q=
\frac1{\sqrt2}
\begin{bmatrix}
1&1\\
1&-1\\
0&0
\end{bmatrix}
\in\mathbb R^{3\times2}.
$$

1. 检查 $\boldsymbol Q^{\top}\boldsymbol Q$。
2. 判断 $\boldsymbol Q\boldsymbol Q^{\top}$ 是否等于 $\boldsymbol I_3$。
3. 用普通语言解释两个乘积分别表示什么。

## B. 手算与构造

### LA-GS-B01

对

$$
\boldsymbol a_1=
\begin{bmatrix}1\\1\\0\end{bmatrix},
\qquad
\boldsymbol a_2=
\begin{bmatrix}1\\1\\1\end{bmatrix}
$$

执行 Gram–Schmidt，求
$\boldsymbol q_1,\boldsymbol q_2$ 和
$r_{11},r_{12},r_{22}$。最后检查：

$$
\boldsymbol q_1^{\top}\boldsymbol q_2=0,
\qquad
\|\boldsymbol q_1\|_2=\|\boldsymbol q_2\|_2=1.
$$

## C. 推导与证明

### LA-GS-C01

证明：任意非零标准正交组
$\boldsymbol q_1,\ldots,\boldsymbol q_k$
都线性无关。

要求从

$$
\sum_{i=1}^{k}c_i\boldsymbol q_i=\boldsymbol0
$$

出发，通过与某个 $\boldsymbol q_j$ 做内积推出
$c_j=0$，不能只引用结论。

## D. 边界与反例

### LA-GS-D01

对

$$
\boldsymbol a_1=
\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\boldsymbol a_2=
\begin{bmatrix}2\\0\end{bmatrix}
$$

执行到 Gram–Schmidt 第二步。

1. 计算残差 $\boldsymbol v_2$；
2. 指出哪个除法无法进行；
3. 解释这与“输入向量线性无关”假设有什么关系；
4. 说明这不代表它们张成的空间没有标准正交基。

## E. AI 迁移

### LA-GS-E01

设低秩更新写成

$$
\Delta\boldsymbol W
=\boldsymbol L\boldsymbol R,
\qquad
\boldsymbol L\in\mathbb R^{d_{\text{out}}\times r},
\quad
\boldsymbol R\in\mathbb R^{r\times d_{\text{in}}},
$$

且 $\boldsymbol L$ 满列秩。对 $\boldsymbol L$ 做薄 QR：

$$
\boldsymbol L=\boldsymbol Q\boldsymbol T.
$$

1. 把 $\Delta\boldsymbol W$ 改写成以 $\boldsymbol Q$ 为左因子的形式；
2. 说明更新矩阵是否改变；
3. 说明列空间是否改变；
4. 为什么不能由 $\boldsymbol Q$ 列正交推出对应隐藏特征“统计独立”？

## 分级提示

### 方向提示

- LA-GS-A01：矩形正交列只保证 $\boldsymbol Q^{\top}\boldsymbol Q=\boldsymbol I$。
- LA-GS-C01：与 $\boldsymbol q_j$ 做内积会消掉除第 $j$ 项外的所有项。
- LA-GS-E01：利用矩阵乘法结合律，把 $\boldsymbol T$ 吸收到右因子。

### 结构提示

- LA-GS-B01：第二个向量沿 $\boldsymbol q_1$ 的投影恰好是 $(1,1,0)^{\top}$。
- LA-GS-D01：第二个向量完全位于第一个方向上。

### 计算提示

- LA-GS-A01：
  $$
  \boldsymbol Q\boldsymbol Q^{\top}
  =
  \begin{bmatrix}1&0&0\\0&1&0\\0&0&0\end{bmatrix}.
  $$
- LA-GS-B01：减去投影后的残差是 $(0,0,1)^{\top}$。

## 解答入口

完成独立尝试后再打开：[[解答 - 标准正交基与 Gram-Schmidt]]。

