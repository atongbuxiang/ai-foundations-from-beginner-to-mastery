---
type: solution
status: draft
area: [generative-models, vae, gaussian]
topic: "[[Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"
exercise: "[[习题 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - Gaussian VAE 的闭式 KL、解码似然与尺度合同

## A. 识别与复述

### GEN12-A01
Encoder 输出 $\mu,\ell=\log\sigma^2$；采样 $z=\mu+e^{\ell/2}\odot\epsilon$。对 $p=N(0,I)$，
$$
KL=\frac12\sum_j(\mu_j^2+e^{\ell_j}-\ell_j-1).
$$

### GEN12-A02
MSE 对应 isotropic Gaussian mean model。固定 $\tau^2$、数据维数和参考测度且只优化 mean 时可省 $D\log(2\pi\tau^2)/2$；学习方差、比较 likelihood 或改变单位时不能省。sum/mean 还改变系数。

### GEN12-A03
Bernoulli 给二值向量质量；categorical 给离散 0–255 每个 bin 的质量；Gaussian 给连续值相对 Lebesgue 测度的 density。三者样本空间、单位、归一化和数值不可直接比较。

## B. 手算与建模

### GEN12-B01
第一维贡献为 $1$，第二维为 $1+4-\log4-1=4-\log4$。故
$$
KL=\tfrac12(5-\log4)\approx1.8069.
$$

### GEN12-B02
SSE 为 $D\cdot MSE=2$。平方项为 $2/(2\tau^2)=2$。常数为
$$
50\log(2\pi\cdot.5)=50\log\pi\approx57.2365,
$$
总 NLL 约 $59.2365$ nats。

### GEN12-B03
$$
-\log.8-\log(1-.3)=-\log.56\approx.5798\text{ nats}.
$$

## C. 推导与证明

### GEN12-C01
写
$$
\log(q/p)=-\log\sigma-\frac{(z-\mu)^2}{2\sigma^2}+\frac{z^2}{2}.
$$
在 $q$ 下用 $E(z-\mu)^2=\sigma^2,E z^2=\mu^2+\sigma^2$，得
$$
KL=-\log\sigma-\tfrac12+\tfrac12(\mu^2+\sigma^2)
=\tfrac12(\mu^2+\sigma^2-\log\sigma^2-1).
$$

### GEN12-C02
Gaussian density 取负对数：
$$
-\log p(x\mid z)=\frac D2\log(2\pi\tau^2)
+\frac1{2\tau^2}\sum_j(x_j-m_j)^2.
$$
若 MSE 是 $D^{-1}$ 倍 SSE，则平方项为 $D\,MSE/(2\tau^2)$。

### GEN12-C03
$f(u)=u-\log u-1$ 在 $u>0$ 上，$f'(u)=1-1/u$，唯一驻点 $u=1$；$f''(u)=1/u^2>0$，故全局最小为 0。加上 $\mu^2$ 后，KL 非负，等号需 $\mu=0,u=\sigma^2=1$。

## D. 边界、反例与纠错

### GEN12-D01
实现 A 用 reconstruction SSE + KL；实现 B 用 mean MSE + KL。因 SSE=$D$·MSE，若要等价，B 的 KL 系数应为 $1/D$ 或重构乘 $D$。二者都写 $\beta=1$ 时，B 相对把 KL 放大 $D$ 倍。

### GEN12-D02
BCE 对 soft $x$ 可作为期望二值 loss，但连续 $x$ 的单点仍需相对参考测度的 density，且 Bernoulli 只在 $\{0,1\}$ 有质量。对 $[0,1]$ 任意实值归一化积分也不由 BCE 自动成立。

### GEN12-D03
Gaussian NLL 若只保留 SSE/$2\tau^2$ 而删除 $D\log\tau$，模型可令 $\tau\to\infty$ 使该项趋零，不受惩罚；或在变体中产生相反方差塌缩。log normalization term 是防止尺度作弊的必要部分。

## E. AI 迁移

### GEN12-E01
图像 uint8：discretized logistic/categorical，按 image sum，报告 bits/dim；文本：per-token categorical，先按序列 sum 再按样本 mean，报告 nats/token；音频 waveform：如 discretized mixture logistic 或明确 Gaussian，写采样率、幅度尺度、time-sample sum。

### GEN12-E02
固定 $\mu,\sigma$ 与 seed，抽大量 $z$，算 $\log q(z)-\log p(z)$ 平均，与闭式比较；覆盖多维、极端 logvar、不同 dtype，给置信误差和 finite-sample tolerance，断言闭式非负且 $\mu=0,\ell=0$ 为零。

### GEN12-E03
至少统一：数据离散/连续合同、预处理范围、维数/分辨率、likelihood family、decoder variance、reconstruction sum/mean、KL sum/mean、batch reduction、sequence mask/length、nats/bits、free bits/annealing、latent dimension。否则名义 $\beta$ 不可比。

