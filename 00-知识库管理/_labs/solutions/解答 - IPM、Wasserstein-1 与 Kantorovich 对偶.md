---
type: solution
status: draft
topic: "[[IPM、Wasserstein-1 与 Kantorovich 对偶]]"
exercise: "[[习题 - IPM、Wasserstein-1 与 Kantorovich 对偶]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - IPM、Wasserstein-1 与 Kantorovich 对偶
## A. 识别与复述
### GEN20-A01
$\sup_{f\in F}|E_Pf-E_Qf|$；$W_1=\inf_{\pi\in\Pi}\int d\,d\pi=\sup_{\|f\|_{Lip}\le1}(E_Pf-E_Qf)$。
### GEN20-A02
TV 用有界函数 ball，MMD 用 RKHS unit ball，$W_1$ 用 1-Lipschitz ball。
### GEN20-A03
population full Lipschitz→regularized neural class→finite empirical supremum→current finite-step critic。
## B. 手算与建模
### GEN20-B01
唯一运输距离 $|2-(-1)|=3$。
### GEN20-B02
支持互斥，JS=$\log2$。
### GEN20-B03
两边各 .5 质量搬到 1，成本 $.5(1)+.5(1)=1$。
## C. 推导与证明
### GEN20-C01
任意 coupling 下 $f(x)-f(y)\le d(x,y)$；积分得期望差不超过运输成本，再对 coupling 取 inf。
### GEN20-C02
唯一 coupling 是 $(0,\theta)$，成本 $|\theta|$；dual 取 $f(x)=-\operatorname{sign}(\theta)x$ 或相反方向达到。
### GEN20-C03
$|\theta|\to0$；而 $\theta\ne0$ 时 JS 恒 $\log2$，在 0 才为 0，故不连续。
## D. 边界、反例与纠错
### GEN20-D01
continuity 不给 differentiability、critic approximation、sample complexity 或 game convergence；bilinear dynamics即反例。
### GEN20-D02
若 critic class 只有常函数，则任意 $P,Q$ 的期望差均 0。
### GEN20-D03
实际数值是有限样本、受限 regularized class、未优化 iterate，通常只是 neural IPM train score。
## E. AI 迁移
### GEN20-E01
像素 Euclidean 对小平移敏感且不等语义距离；feature metric 又依赖 encoder/bias。ground metric 是模型假设。
### GEN20-E02
移动 $\theta$，exact 算 $|\theta|$ 与 JS；训练固定容量 classifier/critic并比较 empirical curve及 gap。
### GEN20-E03
报告 ground metric、Lipschitz method、class architecture、sample size/CI、critic updates、held-out objective、independent OT proxy。

