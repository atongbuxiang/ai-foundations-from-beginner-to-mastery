---
type: exercise-set
status: draft
area: [labs, math/matrix-analysis, ai/foundations]
topic: "[[定理 - Eckart–Young–Mirsky]]"
solution: "[[解答 - Eckart–Young–Mirsky]]"
prerequisites: ["[[奇异值分解]]", "[[矩阵范数]]"]
related: ["[[有效秩]]", "[[随机化低秩近似与随机 SVD]]", "[[练习与测验 MOC]]"]
sources: ["Eckart-Young-1936", "Mirsky-1960"]
created: 2026-08-18
updated: 2026-08-18
---
# 习题 - Eckart–Young–Mirsky

## A. 识别与复述
### MA-EYM-A01
陈述谱范数与 Frobenius 范数版本，说明可行集合、最优矩阵和最优值。
### MA-EYM-A02
解释酉不变范数、截断点谱隙与唯一性的关系；为什么谱范数最佳解可能仍不唯一？
### MA-EYM-A03
判断定理能否直接用于元素加权误差、缺失观测、核范数误差和任务损失，并说明理由。

## B. 手算与构造
### MA-EYM-B01
对 $A=\operatorname{diag}(5,3,1)$，分别求 $k=1,2$ 的 $A_k$、谱误差和 Frobenius 误差。
### MA-EYM-B02
对 $I_3$、$k=1$ 构造至少两个不同最优秩一近似，说明最优值与最优矩阵的区别。
### MA-EYM-B03
把 $A_k=U_k\Sigma_kV_k^*$ 写成 $LR$ 的两种因子化，并展示可逆 gauge 变换。

## C. 推导与证明
### MA-EYM-C01
完整证明谱范数下界：使用 $\operatorname{span}(v_1,\dots,v_{k+1})\cap\mathcal N(B)$。
### MA-EYM-C02
用投影分解和 Ky Fan 权重论证证明 Frobenius 下界。
### MA-EYM-C03
证明任意秩不超过 $k$ 的矩阵都可写成 $LR$，并说明因子优化与秩约束乘积优化的等价和非唯一性。

## D. 边界与计算
### MA-EYM-D01
构造一个元素加权 Frobenius 误差，使标准截断 SVD 不再最优，或严谨说明构造策略。
### NLA-EYM-D02
当 $\sigma_k\approx\sigma_{k+1}$ 时，最优值、选定子空间与浮点算法分别可能怎样变化？
### NLA-EYM-D03
随机 SVD 返回 $\tilde A_k$。设计验收：区分不可约尾误差与算法附加误差，并列出需报告的随机参数。

## E. AI 迁移
### AI-EYM-E01
权重 $W$ 的截断满足什么单输入与 batch 输出误差界？为何不等于端到端损失界？
### AI-EYM-E02
从中心化数据矩阵 SVD 推导 PCA 最佳线性重构，并说明样本按行/列时的方向形状。
### AI-EYM-E03
比较训练后截断、直接训练 LoRA 因子和结构化低秩近似的可行集与优化目标。

独立解答：[[解答 - Eckart–Young–Mirsky]]。
