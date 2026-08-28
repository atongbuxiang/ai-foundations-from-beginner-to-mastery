---
type: solution
status: draft
area: [learning-theory/algorithmic-stability, regularization, convex-optimization]
topic: "[[正则化 ERM 的稳定性]]"
exercise: "[[习题 - 正则化 ERM 的稳定性]]"
prerequisites: ["[[正则化 ERM 的稳定性]]"]
related: ["[[算法稳定性与替换一个样本]]", "[[随机梯度算法的稳定性接口]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - 正则化 ERM 的稳定性

> [!warning] 归一化
> 本解答固定 $F_S=m^{-1}\sum_i\ell_i+\lambda\|w\|^2/2$ 与 direct replacement adjacency。

## A. 识别与复述

### LT-RERM-A01

假设 $\mathcal W$ convex，每个 $\ell(\cdot,z)$ convex 且关于 $\|\cdot\|_2$ 为 $L$-Lipschitz，$\lambda>0$，exact minimizer 存在。则 $F_S$ 为 $\lambda$-strongly convex、minimizer 唯一，且对 $S\simeq S'$：

$$
\|w_S-w_{S'}\|_2
\le\frac{2L}{\lambda m}.
$$

再由 test loss Lipschitzness：

$$
\beta_m
\le\frac{2L^2}{\lambda m}.
$$

### LT-RERM-A02

- $L$-Lipschitz：函数值变化至多线性随距离变化；等价地控制 gradient norm；
- $\gamma$-smooth：gradient 变化至多 $\gamma$ 倍距离，是 curvature 上界；
- $\lambda$-strongly convex：函数高于其切平面加 $\lambda\|v-w\|^2/2$，是 curvature 下界。

主 proof 使用 strong convexity 和 Lipschitzness，不需要 smoothness。smoothness在迭代求解/SGD proof 中才常进入。

### LT-RERM-A03

普通 optimality 只给非负 objective gap：

$$
F_S(w_{S'})-F_S(w_S)\ge0.
$$

它不把 gap 与 $\|w_S-w_{S'}\|$ 定量连接。strong convexity 提供

$$
F_S(w_{S'})-F_S(w_S)
\ge\frac\lambda2\|w_S-w_{S'}\|^2,
$$

使左边出现二次 displacement；右边 replacement effect 是 $O(L\|\Delta\|/m)$，二者平衡才能解出 $O(1/(\lambda m))$。

## B. 手算与数值判断

### LT-RERM-B01

$$
\|w_S-w_{S'}\|
\le\frac{2(3)}{0.2(500)}
=\boxed{0.06}.
$$

$$
\beta_m
\le\frac{2(3^2)}{0.2(500)}
=\boxed{0.18}.
$$

### LT-RERM-B02

logistic loss 可取 $L=R=5$。要求

$$
\frac{2R^2}{\lambda m}
=\frac{50}{2000\lambda}
=\frac{0.025}{\lambda}
\le0.01.
$$

因此

$$
\boxed{\lambda\ge2.5}.
$$

数值很大也提醒我们：上界可能保守，且较大 $\lambda$ 会增加 bias。

### LT-RERM-B03

exact term：

$$
\frac{2L^2}{\lambda m}
=\frac8{500}
=0.016.
$$

approximate term：

$$
2L\sqrt{\frac{2\varepsilon_{\rm opt}}\lambda}
=4\sqrt{\frac{2\times10^{-8}}{0.5}}
=4\sqrt{4\times10^{-8}}
=0.0008.
$$

总上界为

$$
\boxed{0.0168}.
$$

## C. 推导与证明

### LT-RERM-C01

令 $w=w_S,w'=w_{S'}$。strong convexity 给

$$
F_S(w')-F_S(w)\ge\frac\lambda2\|w'-w\|^2,
$$

$$
F_{S'}(w)-F_{S'}(w')\ge\frac\lambda2\|w'-w\|^2.
$$

相加后 regularizer 的差正负抵消。对 $j\ne i$ 的共享样本，

$$
[\ell(w',Z_j)-\ell(w,Z_j)]
+[\ell(w,Z_j)-\ell(w',Z_j)]=0.
$$

只剩

$$
\lambda\|w'-w\|^2
\le\frac1m[
\ell(w',Z_i)-\ell(w,Z_i)
+\ell(w,Z_i')-\ell(w',Z_i')].
$$

右边每项至多 $L\|w'-w\|$。若 displacement 非零，除去一阶因子得到

$$
\|w'-w\|\le\frac{2L}{\lambda m}.
$$

零 displacement 情形结论显然。

### LT-RERM-C02

令 $\Omega$ 关于 $\|\cdot\|$ 为 $\lambda$-strongly convex，并令

$$
F_S(w)=\frac1m\sum_i\ell(w,Z_i)+\Omega(w).
$$

若 $\ell(\cdot,z)$ 关于该 norm 为 $L$-Lipschitz，等价于可微情形的

$$
\|\nabla\ell(w,z)\|_*\le L,
$$

则上一题全部步骤只需把 Euclidean norm 换成 $\|\cdot\|$。结论仍为

$$
\|w_S-w_{S'}\|
\le\frac{2L}{\lambda m},
\qquad
\beta_m\le\frac{2L^2}{\lambda m}.
$$

dual norm 通过 Hölder inequality 控制

$$
|\langle\nabla\ell,\Delta\rangle|
\le\|\nabla\ell\|_*\|\Delta\|.
$$

### LT-RERM-C03

strong convexity 分别给

$$
\|\widetilde w_S-w_S\|
\le\sqrt{\frac{2\varepsilon_S}{\lambda}},
$$

$$
\|\widetilde w_{S'}-w_{S'}\|
\le\sqrt{\frac{2\varepsilon_{S'}}{\lambda}}.
$$

三角不等式：

$$
\|\widetilde w_S-\widetilde w_{S'}\|
\le
\sqrt{\frac{2\varepsilon_S}{\lambda}}
+\frac{2L}{\lambda m}
+\sqrt{\frac{2\varepsilon_{S'}}{\lambda}}.
$$

乘以 test-loss Lipschitz constant $L$：

$$
\boxed{
\widetilde\beta_m
\le\frac{2L^2}{\lambda m}
+L\sqrt{\frac{2\varepsilon_S}{\lambda}}
+L\sqrt{\frac{2\varepsilon_{S'}}{\lambda}}.}
$$

## D. 边界、反例与纠错

### LT-RERM-D01

平方损失 gradient 为

$$
\nabla_w\ell=2(\langle w,x\rangle-y)x.
$$

固定非零 $x$，令 $\|w\|\to\infty$，gradient norm 无界，所以不存在全域统一 Lipschitz constant。

若限制 $\|w\|\le B,\|x\|\le R,|y|\le Y$，则

$$
|\langle w,x\rangle-y|
\le BR+Y,
$$

因此

$$
\|\nabla\ell\|
\le2R(BR+Y).
$$

在 convex ball 上可取

$$
\boxed{L=2R(BR+Y)}.
$$

### LT-RERM-D02

加二次项后的 Hessian 为

$$
\nabla^2 f(w)+\lambda I.
$$

只有当 $\lambda_{\min}(\nabla^2 f(w))\ge0$（原 $f$ convex）时，才能保证下界至少 $\lambda I$。若原 Hessian 有小于 $-\lambda$ 的 eigenvalue，和仍非凸。

一维例子：

$$
f(w)=-\frac{\lambda+1}{2}w^2.
$$

加 $\lambda w^2/2$ 后为 $-w^2/2$，仍严格 concave。

### LT-RERM-D03

当 $\lambda\to\infty$，stability term $2L^2/(\lambda m)\to0$。但 minimizer 往往趋向最小 norm point（Euclidean 情形通常是 $w=0$），预测器近似固定，不再拟合数据。

若标签总为 1 而 $w=0$ 对应预测 0，risk 可接近 1。稳定性变好与 approximation/bias error 变差可同时发生。

## E. AI 迁移

### LT-RERM-E01

RKHS evaluation inequality：

$$
|f(x)-g(x)|
\le\sqrt{k(x,x)}\|f-g\|_{\mathcal H_k}
\le\kappa\|f-g\|_{\mathcal H_k}.
$$

scalar loss 对 prediction 为 $\sigma$-Lipschitz，因此 composite loss 关于 RKHS norm 为 $L=\sigma\kappa$。若 regularizer 为 $\lambda\|f\|_{\mathcal H_k}^2/2$，则

$$
\boxed{
\beta_m\le\frac{2\sigma^2\kappa^2}{\lambda m}.}
$$

### LT-RERM-E02

不能直接套用，因为：network loss 非凸；weight decay 未使全 objective strong convex；BatchNorm 让单样本 loss/update batch-coupled；参数尺度/置换产生 function equivalence；loss 对 parameters 未必 global Lipschitz；早停输出不是 exact minimizer；optimizer path、randomness 与 tolerance 未进入 exact RERM proof。

可把本章作为审计模板，但每个缺口都需新 theorem，而不是经验上“差不多”。

### LT-RERM-E03

建议每个 $\lambda$ 报告：

- training/validation risk；
- parameter/function norm；
- 可验证的 $L$ 或 gradient-norm envelope；
- strong-convexity modulus/最小 curvature（若适用）；
- $2L^2/(\lambda m)$ 数值；
- optimization objective gap 或 residual；
- approximate-stability correction；
- replace-one empirical sensitivity；
- 多次 seeds 的 spread；
- validation selection protocol 与总置信预算。

这样才能看出 fit、stability、bias 与 optimization 中哪一项主导。
