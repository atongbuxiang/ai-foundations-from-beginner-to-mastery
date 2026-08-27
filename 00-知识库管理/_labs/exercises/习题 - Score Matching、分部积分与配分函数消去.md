---
type: exercise
status: draft
area: [generative-models, score-matching]
topic: "[[Score Matching、分部积分与配分函数消去]]"
solution: "[[解答 - Score Matching、分部积分与配分函数消去]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Score Matching、分部积分与配分函数消去
## A. 识别与复述
### GEN27-A01
区分 parameter score 与 data score；本节使用哪一个？
### GEN27-A02
为什么 $x$-score 会消去 $Z_\theta$？
### GEN27-A03
写出 Fisher divergence 与 Hyvärinen objective，并列出边界条件角色。
## B. 手算与建模
### GEN27-B01
一维模型 $E_a(x)=ax^2/2$。写出 $s_a(x)$、$\partial_xs_a(x)$ 与单样本 Hyvärinen loss。
### GEN27-B02
若数据 $X\sim N(0,\tau^2)$，求上一题总体 objective 的最优 $a$。
### GEN27-B03
给 $J=\begin{pmatrix}2&1\\0&3\end{pmatrix}$，计算精确 trace，并用 Rademacher $v=(1,-1)$ 的 $v^T Jv$ 作一次 Hutchinson 估计。
## C. 推导与证明
### GEN27-C01
在一维上完整推导 score matching 分部积分公式，显式保留边界项。
### GEN27-C02
证明在连通区域上两个正密度 score 相同，则归一化后密度相同。
### GEN27-C03
从 $s_\theta=-\nabla E_\theta$ 推出 energy 形式 $\frac12\|\nabla E\|^2-\Delta E$。
## D. 边界、反例与纠错
### GEN27-D01
构造不连通 support，使两个分布在各分量内部 score 相同但分量质量不同。
### GEN27-D02
为何不能把连续欧氏 score matching 原式直接用于有限离散 token？
### GEN27-D03
反驳“score matching 消去 $Z$，所以训练没有高阶导数与方差问题”。
## E. AI 迁移
### GEN27-E01
写出使用 Hutchinson trace 的 neural EBM 最小训练协议。
### GEN27-E02
针对 $x\in[0,1]^d$ 图像，说明边界问题，并提出一种谨慎处理方案。
### GEN27-E03
设计一个检验 learned vector score 是否近似可积为 scalar energy 的实验。
## 解答入口
[[解答 - Score Matching、分部积分与配分函数消去]]

