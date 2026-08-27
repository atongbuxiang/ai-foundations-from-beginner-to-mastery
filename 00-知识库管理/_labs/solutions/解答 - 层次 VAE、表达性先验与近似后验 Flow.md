---
type: solution
status: draft
area: [generative-models, vae, hierarchy, flow]
topic: "[[层次 VAE、表达性先验与近似后验 Flow]]"
exercise: "[[习题 - 层次 VAE、表达性先验与近似后验 Flow]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - 层次 VAE、表达性先验与近似后验 Flow

## A. 识别与复述

### GEN15-A01
Prior 负责 latent 生成与 aggregate matching；likelihood/decoder 负责 observation distribution 与 distortion；posterior 负责逼近真后验和 bound/gradient；hierarchy 改 joint factorization、多尺度信息与祖先采样。四者可同时改，归因需消融。

### GEN15-A02
两层例：
$$
p(z_2)p_\theta(z_1\mid z_2)p_\theta(x\mid z_1,z_2).
$$
祖先采样依次 $z_2\to z_1\to x$；不能从 bottom-up encoder 的顺序反推生成顺序。

### GEN15-A03
Posterior flow 变换 $q_\phi(z\mid x)$，通常只在训练/推断时用，需正向采样与 log-Jacobian；generative flow 直接定义 $p_\theta(x)$ 的可逆变换，生成/密度方向成本由架构决定。前者不自动改 prior samples。

## B. 手算与建模

### GEN15-B01
$dz_1/dz_0=2$，故
$$
q_1(z_1)=q_0(z_0)|2|^{-1}=.15,
\qquad\log q_1=\log.3-\log2.
$$

### GEN15-B02
log joint 是三项和：$-1-.5-2=-3.5$。

### GEN15-B03
由 $R=I+KL_{agg}$，原 aggregate KL 为 $1.5$。降至 $.2$ 且 MI 不变时，新 rate 为 $1.0+.2=1.2$ nats。

## C. 推导与证明

### GEN15-C01
可逆 $z_K=f_K\circ\cdots\circ f_1(z_0)$。逐次换元：
$$
\log q_K(z_K\mid x)=\log q_0(z_0\mid x)
-\sum_k\log|\det J_{f_k}(z_{k-1})|.
$$
代入 $\mathcal L=E_{q_K}[\log p_\theta(x,z_K)-\log q_K(z_K\mid x)]$，用 base noise Monte Carlo。

### GEN15-C02
若 $q(z_{1:L}\mid x)=\prod_\ell q(z_\ell\mid z_{>\ell},x)$、$p(z_{1:L})=\prod_\ell p(z_\ell\mid z_{>\ell})$，则 log ratio 是各条件 log ratio 之和。对 joint $q$ 取期望，每项先对 $z_{\le\ell}$ 条件积分，得
$$
\sum_\ell E_{q(z_{>\ell}\mid x)}
KL(q(z_\ell\mid z_{>\ell},x)\|p(z_\ell\mid z_{>\ell})).
$$

### GEN15-C03
vMF density 形如 $C_d(\kappa)e^{\kappa\mu^\top z}$，uniform density 为常数。旋转对称使 $E_{\mathrm{vMF}}[\mu^\top Z]$ 只依赖 $d,\kappa$，故 KL 不依赖方向 $\mu$。但若 $\mu(x)\equiv\mu_0$，条件分布不随 $x$ 变，MI 仍为零。

## D. 边界、反例与纠错

### GEN15-D01
无条件生成通常从 $p(z)$ 采样，posterior flow $q(z\mid x)$ 不被调用。它可使 ELBO 更紧、训练 $\theta$ 更好，但这是间接经验效应，不是采样器本身更表达。

### GEN15-D02
NVAE 同时改变 hierarchy、网络 cell、normalization、posterior、训练稳定化和 likelihood。总结果只能证明组合系统可行。要归因层次 latent，需同预算逐项/交互消融和 group-use 证据。

### GEN15-D03
固定 $\mu(x)=\mu_0$、$\kappa>0$，对所有 $x$ 输出同一 vMF；到 uniform prior 的 KL 是固定正常数，但 $q(z\mid x)=q(z)$，所以 $I(X;Z)=0$。

## E. AI 迁移

### GEN15-E01
记录 top-down joint、每 group tensor shape、conditional prior/posterior、per-group KL/rate/active units；逐组置零、prior-resample、posterior-swap 测 distortion 和语义。生成按顶层到低层固定顺序，保存温度、decoder likelihood 与随机 seed。

### GEN15-E02
检查 encoder/decoder attention mask、target token 可见性、padding、position、原句长度是否传入；按长度报告 rate/NLL；generation 不给真实长度，审计 EOS 分布；做随机 padding、length-matched baseline 与去 CLS latent 消融。

### GEN15-E03
用全基础、仅 prior、仅 posterior flow、仅 decoder、两两组合、全部组件的阶乘子集；匹配参数量、训练步、NFE 与 likelihood family。报告 bound、large-$K$ likelihood、rate 分解、sample quality/coverage、速度和多 seed，才能看主效应与交互。

