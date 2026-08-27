---
type: exercise-set
status: draft
area: [labs, math/matrix-analysis, math/optimization, ai/foundations]
topic: "[[Moore-Penrose 伪逆]]"
solution: "[[解答 - Moore-Penrose 伪逆]]"
prerequisites: ["[[最小二乘]]", "[[奇异值分解]]"]
related: ["[[正交投影]]", "[[条件数]]", "[[练习与测验 MOC]]"]
sources: ["Penrose-1955", "GolubVanLoan-MC4e-Ch5"]
created: 2026-08-18
updated: 2026-08-18
---
# 习题 - Moore-Penrose 伪逆

## A. 识别与复述
### LA-PINV-A01
写出四个 Penrose 条件，解释前两条和后两条的几何分工。
### LA-PINV-A02
对 $A:m\times n$，写出 $A^\dagger$、$AA^\dagger$、$A^\dagger A$ 的形状和值域/零空间。
### LA-PINV-A03
列出可逆、满列秩、满行秩三个特例；说明各普通逆的存在条件。

## B. 手算与构造
### LA-PINV-B01
对 $A=\operatorname{diag}(2,0)$、$b=(4,3)^T$ 求 $A^\dagger$、最优预测、残差、全部 LS 解和最小范数解。
### LA-PINV-B02
对 $A=[1\ 1]$ 求 $A^\dagger$；对标量 $b=2$ 求全部精确解和最小范数解。
### LA-PINV-B03
对 $A=\begin{bmatrix}1&0\\0&0\\0&0\end{bmatrix}$ 求两个投影 $AA^\dagger,A^\dagger A$ 并解释不同形状。

## C. 推导与证明
### LA-PINV-C01
由紧致 SVD 构造 $A^\dagger$ 并逐条验证 Penrose 条件。
### LA-PINV-C02
证明任一满足四条件的 $X$ 都使 $AX=P_{\mathcal R(A)}$、$XA=P_{\mathcal R(A^*)}$，据此证明唯一性。
### LA-PINV-C03
证明全部最小二乘解为 $A^\dagger b+(I-A^\dagger A)z$，且第一项唯一最小范数。

## D. 数值与反例
### NLA-PINV-D01
对 $A_\varepsilon=\operatorname{diag}(1,\varepsilon)$ 分析 $A_\varepsilon^\dagger$、条件数和 $\varepsilon\to0$ 的连续性。
### LA-PINV-D02
用 $A=[1\ 1],B=(1,0)^T$ 验证 $(AB)^\dagger\ne B^\dagger A^\dagger$。
### NLA-PINV-D03
比较精确伪逆、截断 SVD、Ridge 的滤波因子、偏差、连续性和噪声放大。

## E. AI 迁移
### AI-PINV-E01
冻结表示 $H:N\times d$、标签 $Y:N\times c$。写出 $H^\dagger Y$ 的形状、意义与近秩亏风险。
### AI-PINV-E02
低秩因子化中固定一侧时怎样出现伪逆闭式更新？为什么两侧同时训练不能由一次伪逆解决？
### AI-PINV-E03
局部模型编辑用 Jacobian $J:m\times p$ 求最小范数参数改动。写出解并说明局部性、样本覆盖与截断边界。

独立解答：[[解答 - Moore-Penrose 伪逆]]。
