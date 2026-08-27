---
type: solution
status: draft
area: [generative-models, vae, variational-inference]
topic: "[[VAE 的 ELBO、变分后验与重参数化梯度]]"
exercise: "[[习题 - VAE 的 ELBO、变分后验与重参数化梯度]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - VAE 的 ELBO、变分后验与重参数化梯度

## A. 识别与复述

### GEN11-A01
三式为
$$
\mathcal L=E_q[\log p_\theta(x,z)-\log q_\phi(z\mid x)]
=E_q\log p_\theta(x\mid z)-KL(q_\phi\|p(z)),
$$
以及
$$
\log p_\theta(x)=\mathcal L+
KL(q_\phi(z\mid x)\|p_\theta(z\mid x)).
$$

### GEN11-A02
在 $p_\theta(x,z)$ 有正质量的相关区域，$q_\phi(z\mid x)$ 不能为零，否则 ratio/proposal 覆盖失败。Jensen 取等当 weight 在 $q$ 下为常数，等价于 $q_\phi=p_\theta(z\mid x)$ 几乎处处。

### GEN11-A03
score-function 用 $f(z)\nabla_\phi\log q_\phi(z)$，对离散分布也适用但常高方差。pathwise 要能写 $z=T_\phi(\epsilon)$ 且 $T$ 可微、base noise 不依赖 $\phi$；通常方差较低。

## B. 手算与建模

### GEN11-B01
joint contributions 为 $.27,.14$，evidence $.41$。proposal 各 $.5$，weights 为 $.54,.28$。故
$$
\mathcal L=\tfrac12\log.54+\tfrac12\log.28
\approx-0.9445,
$$
$\log p(x)=\log.41\approx-0.8916$，gap 约 $.0529$，等于 $KL(q\|posterior)$。

### GEN11-B02
$z=1+2(-.5)=0$。单样本
$$
\partial_\mu z^2=2z=0,\qquad
\partial_\sigma z^2=2z\epsilon=0.
$$
单次为零不表示期望梯度为零；解析期望梯度为 $(2,4)$。

### GEN11-B03
期望 log likelihood 的估计为 $(-2-4)/2=-3$。ELBO 为 $-3-.7=-3.7$，negative ELBO 为 $3.7$。

## C. 推导与证明

### GEN11-C01
插入 $q/q$：
$$
\log p(x)=\log E_q[p(x,Z)/q(Z\mid x)]
\ge E_q\log[p(x,Z)/q(Z\mid x)]=\mathcal L.
$$
等号当 ratio 为常数；归一化后该常数为 $p(x)$，故 $q=p(z\mid x)$。

### GEN11-C02
由 $\log p(z\mid x)=\log p(x,z)-\log p(x)$，
$$
KL(q\|p(z\mid x))
=E_q[\log q-\log p(x,z)]+\log p(x)
=\log p(x)-\mathcal L.
$$
移项即得结论。

### GEN11-C03
$E z^2=\mu^2+\sigma^2$，解析梯度 $(2\mu,2\sigma)$。pathwise 梯度为 $(2z,2z\epsilon)$；取期望：
$$
E[2z]=2\mu,\quad E[2z\epsilon]=2\mu E\epsilon+2\sigma E\epsilon^2=2\sigma.
$$

## D. 边界、反例与纠错

### GEN11-D01
令 $Z=\pm1$ 等概率，$p(x\mid z)=e^{-z^2}$ 不够区分；更直接取正值函数 $r(Z)$ 为 $.1,.9$。则 $E\log r=.5\log.09=\log.3$，而 $\log E r=\log.5$，不相等。decoder 非线性同样受 Jensen 影响。

### GEN11-D02
训练 ELBO 可因 encoder 更贴合训练 posterior 而升高，但 test 分布上过拟合；也可提高 likelihood 却出现感知样本下降，或只缩小 bound gap 而 $\theta$ 几乎不变。需独立 test likelihood estimator、prior-sample 质量/覆盖与多 seed。

### GEN11-D03
真 posterior 在 $z\in\{0,1\}$ 都有质量，而 proposal 令 $q(1\mid x)=0$。来自 $z=1$ 的 joint mass 永不被采到，importance estimator 只估部分 evidence；ratio 在漏失区域不可用，有限结果可看似稳定却系统错误。

## E. AI 迁移

### GEN11-E01
记录 encoder 输出含义（mean/logvar）、base noise/shape、重参数化式、decoder likelihood 参数、analytic KL 的两端与方向、latent samples 数、data/batch reduction、单位、optimizer 与 evaluation path。

### GEN11-E02
类别少时枚举给 exact 低方差期望；Gumbel 提供可微但温度相关、有 relaxed bias；score-function 无 relaxation bias、适用广但高方差。应同预算报告 bias proxy、gradient variance、温度与离散 test sampling。

### GEN11-E03
训练保存 posterior samples 和 ELBO components；评价冻结模型，用大 $K$ importance estimate；生成完全绕过 encoder，从 prior 开始。设置断言：生成函数不得读训练 $x$；评价不得更新权重；部署 mean/sample 选择明确。

