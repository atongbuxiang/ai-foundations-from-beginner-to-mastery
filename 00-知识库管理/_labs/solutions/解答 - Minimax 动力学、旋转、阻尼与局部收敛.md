---
type: solution
status: draft
topic: "[[Minimax 动力学、旋转、阻尼与局部收敛]]"
exercise: "[[习题 - Minimax 动力学、旋转、阻尼与局部收敛]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Minimax 动力学、旋转、阻尼与局部收敛
## A. 识别与复述
### GEN22-A01
$F=(\nabla_\theta V,-\nabla_\psi V)$；stationary 为 $F=0$；local Nash 是各方局部 best response；dynamic stability依指定算法扰动回归。
### GEN22-A02
Jacobian 的 cross blocks形成反对称旋转，通常不满足保守场所需的对称 Jacobian。
### GEN22-A03
需快慢步长序列、随机噪声/有界性、正则性、局部稳定等 stochastic approximation 假设；不同 Adam rates 不自动证明。
## B. 手算与建模
### GEN22-B01
$A=\begin{pmatrix}1&-\eta\\\eta&1\end{pmatrix}$，特征值 $1\pm i\eta$。
### GEN22-B02
radius-squared 乘 $|1+i\eta|^2=1+\eta^2=1.01$。
### GEN22-B03
$\dot x=-y,\dot y=x$，导数 $2x(-y)+2yx=0$。
## C. 推导与证明
### GEN22-C01
谱半径 $\sqrt{1+\eta^2}>1$，除原点外模按此因子增长。
### GEN22-C02
$\dot x=-(y+\lambda x),\dot y=x-\lambda y$，Jacobian $\begin{pmatrix}-\lambda&-1\\1&-\lambda\end{pmatrix}$，特征值 $-\lambda\pm i$；$\lambda>0$ 连续局部稳定。
### GEN22-C03
预测 $\tilde u=(I-\eta J)u$（按 game field符号），修正 $u^+=(I-\eta J+\eta^2J^2)u$；bilinear $J^2=-I$，产生 $1-\eta^2$ 的 inward 分量。
## D. 边界、反例与纠错
### GEN22-D01
$V(x,y)=x^3-y^3$ 在原点 stationary，但对各方都不是局部 optimum。
### GEN22-D02
周期轨道上 loss 可周期/均值平稳，gradient非零；饱和也可 loss平坦。需参数轨迹和 residual。
### GEN22-D03
Mescheder 等给有限 critic updates 的反例；GP sampling/参数与局部条件不足以普遍保证。
## E. AI 迁移
### GEN22-E01
记录两方 gradients、cosine/cross-correlation、update norm、参数半径、Jacobian-vector local spectrum与cycle autocorrelation。
### GEN22-E02
同初始化、oracle calls、wall-clock、batch/regularizer；多步长多 seed，报告 residual、distance与failure。
### GEN22-E03
EMA 生成器是参数时间平均的部署模型，可能样本更好；原训练 iterates仍可能绕圈，不能据此宣称 game收敛。

