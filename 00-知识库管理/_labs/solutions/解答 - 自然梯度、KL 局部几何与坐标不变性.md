---
type: solution
status: verified
area: [training, optimization, information-geometry]
topic: "[[自然梯度、KL 局部几何与坐标不变性]]"
exercise: "[[习题 - 自然梯度、KL 局部几何与坐标不变性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 自然梯度、KL 局部几何与坐标不变性

> [!warning] 使用边界
> 不变的是 exact local tangent 的几何意义，不是任意 damping、有限 Euler 轨迹、近似矩阵和实现状态都自动不变。

## A. 识别与复述

### TRN20-A01
$dL$ 对位移给线性响应，是坐标变换下按 pullback 变化的 covector；要把它变成“最陡方向”，必须选 metric。Euclidean gradient 隐含单位矩阵 metric，而非正交重参数化会改变该单位矩阵的含义。自然梯度用 Fisher 的逆把 covector $g$ 转为 tangent vector $F^{-1}g$。

### TRN20-A02
自然下降方向为 $-F^{-1}g$。它来自 $\min_s g^Ts$ subject to $\tfrac12s^TFs\le\epsilon$；Fisher 定义局部 KL 长度。KL 半径决定该局部模型中步的 metric length，学习率则在 unconstrained 写法中人为缩放方向；二者可换算但不是同一日志字段。

### TRN20-A03
严谨说法是：在 smooth invertible reparameterization 下，若使用同一分布族上的 exact Fisher metric、exact linear solve，并比较 infinitesimal tangent，则自然梯度向量按 Jacobian pushforward 一致。它不直接保证 finite-step Euler endpoints 或近似优化器轨迹完全相同。

## B. 手算与构造

### TRN20-B01
负对数似然对 logit 的梯度 $g_a=p-y=-0.2$，Fisher $F_a=p(1-p)=0.16$。自然下降方向 $-g_a/F_a=1.25$；诱导 $dp=(dp/da)\,da=0.16\times1.25=0.2$。

### TRN20-B02
在概率坐标，$g_p=-1/p=-1.25$，Fisher $F_p=1/[p(1-p)]=6.25$，所以自然下降方向 $-g_p/F_p=0.2$。它正好等于上一题的 infinitesimal $dp$，尽管两个坐标中的普通 gradient 与 Fisher 数字均不同。

### TRN20-B03
未归一化方向 $d=-F^{-1}g=(-2,-1/3)$，且 $d^TFd=g^TF^{-1}g=5$。令 $s=\alpha d$，边界要求 $\tfrac12\alpha^2\times5=0.02$，故 $\alpha=\sqrt{0.008}\approx0.08944$，$s\approx(-0.17889,-0.02981)$。

## C. 推导与证明

### TRN20-C01
令 score $s_\theta(y)=\nabla_\theta\log p_\theta(y)$。KL 在零位移处为零且达到局部极小，一阶项为 $-\mathbb E_p[s_\theta]=0$；在正则条件下二阶项是 $\mathbb E_p[s s^T]=F$。于是 $\mathrm{KL}(p_\theta\|p_{\theta+s})=\tfrac12s^TFs+O(\|s\|^3)$。

### TRN20-C02
Lagrangian 为 $g^Ts+\lambda(\tfrac12s^TFs-\epsilon)$。Stationarity 给 $g+\lambda Fs=0$，故 $s=-\lambda^{-1}F^{-1}g$。约束活跃时
$$\lambda=\sqrt{\frac{g^TF^{-1}g}{2\epsilon}},\qquad s=-\sqrt{\frac{2\epsilon}{g^TF^{-1}g}}F^{-1}g.$$

### TRN20-C03
链式法则给 $g_\xi=J^Tg_\theta$，metric pullback 给 $F_\xi=J^TF_\theta J$。若 $J$ 方且可逆，
$$J(-F_\xi^{-1}g_\xi)=-J(J^TF_\theta J)^{-1}J^Tg_\theta=-F_\theta^{-1}g_\theta.$$
因此两套坐标描述同一 tangent；奇异或非双射映射需改用子空间/广义逆分析。

## D. 边界、反例与纠错

### TRN20-D01
在 $p=0.8,y=1$，取尺度 $\eta=0.1$。Logit 端点是 $\sigma(\operatorname{logit}(0.8)+0.125)\approx0.8193$；概率坐标直接加步得到 $0.8+0.02=0.82$。一阶变化都约为 $0.02$，差异来自坐标映射 Taylor 展开的二阶及更高项。

### TRN20-D02
一维缩放 $\theta=c\xi$ 下，$F_\xi=c^2F_\theta$，但 $F_\xi+\lambda$ 不是 $c^2(F_\theta+\lambda)$，除非同步按坐标变换调整 damping。固定 Euclidean $\lambda I$ 因而选定了坐标单位，破坏 exact metric 的协变关系。

### TRN20-D03
Diagonal/K-FAC 改写了 metric，有限 CG 又只近似求逆；clipping、momentum、weight decay、finite step 与 state transport 继续改变 transition。它们可在限定参数变换族下保留某些近似性质，但不能从“Fisher-like”名称推出自然梯度的完整不变性定理。

## E. AI 迁移

### TRN20-E01
记录 score 标签/trajectory source、Fisher estimator、正向与反向 KL、局部预测 $s^TFs/2$、实测 KL、CG residual/HVP 数、damping、step scale、line-search 接受、RNG 与 batch。正反 KL 不对称，不能只写一个未标方向的 `kl`。

### TRN20-E02
固定 $p,y$，分别在 $a=\operatorname{logit}(p)$ 与 $p$ 坐标计算 ordinary/natural direction；断言 $dp/da\cdot d_a=d_p$。再用一组逐渐减小的 $\eta$ 比较两个有限端点，断言差值按 $O(\eta^2)$ 缩小，而不是断言任意有限步完全相等。

### TRN20-E03
Newton 用训练目标 Hessian 定义局部二次曲率；自然梯度用模型分布 Fisher 定义 KL metric；mirror descent 用选定势函数的 Bregman divergence 定义 proximal geometry。在线性/指数族、匹配 loss 与特定势函数等条件下它们可能给相同方向，但对象与成立理由仍要分别陈述。

## 无提示重做

- [ ] 48 小时后独立推导 KL-constrained direction 的尺度。
- [ ] 一周后在两套 Bernoulli 坐标重做 infinitesimal 与 finite-step 对照。
