---
type: solution
status: draft
area: [math/statistics, ai/probabilistic-modeling, ai/optimization]
topic: "最大似然估计与 MAP"
exercise: "[[习题 - 最大似然估计与 MAP]]"
prerequisites: ["[[最大似然估计与 MAP]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.655-Lecture-9-10-Methods-of-Estimation", "Casella-Berger-Statistical-Inference", "Su-2018-5239-MLE-to-EM", "Su-2020-7681-L2-Scale-Invariance"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 最大似然估计与 MAP

> [!warning] 使用边界
> 先写 joint/conditional model、support 与 parameter space，再谈优化。一个 loss 形似 NLL/L2，不足以证明它就是某个规范概率模型的 MLE/MAP。

## A. 识别与复述

### PROB-MLE-A01

- PMF/PDF $p_\theta(x)$：固定 $\theta$，在数据空间上求和/积分为 1；
- likelihood $L(\theta;x)=p_\theta(x)$：固定观测 $x$，比较参数，通常不在 $\theta$ 上归一化；
- log-likelihood $\ell(\theta;x)=\log L(\theta;x)$：保留 argmax，并把乘积变和；
- prior $\pi(\theta)$：观察当前数据前，对参数坐标定义的概率分布/密度；
- posterior：

$$
\pi(\theta\mid x)
=\frac{p_\theta(x)\pi(\theta)}
{\int p_\vartheta(x)\pi(\vartheta)d\vartheta};
$$

- posterior predictive：

$$
p(x_{\rm new}\mid x)
=\int p_\theta(x_{\rm new})\pi(\theta\mid x)d\theta.
$$

$L(\theta;x)$ 没有 prior，也没有对参数归一化，所以不能读作 $P(\theta\mid x)$。MLE 输出 likelihood maximizer，MAP 输出 posterior density mode；二者都是点估计。它们没有自动输出 posterior mass、credible interval、parameter sampling uncertainty 或 posterior predictive，多个 maximizer 时还只是一个集合。

### PROB-MLE-A02

score equation

$$
\nabla_\theta\ell(\widehat\theta)=0
$$

只适用于参数空间内点、目标可微且极值有限存在的候选解；还需用 Hessian、convexity/concavity、边界比较和全局分析判断。

例子：

- 边界：Bernoulli 样本全零时 $\widehat p=0$；
- 不存在：完全分离 logistic regression 的有限 MLE 不存在；
- 不唯一：overparameterized linear model 的多个参数给同一 fitted values；
- 不可辨识：mixture label permutation；
- support 依参数：$U(0,\theta)$，MLE 是 sample maximum。

### PROB-MLE-A03

“L2 = Gaussian prior”必须同时满足：

1. likelihood 的 NLL 真的是代码中 data loss；
2. 若 prior 是 $N(0,\tau^2I)$，negative log-prior 恰为 $\|\theta\|^2/(2\tau^2)$ 加常数；
3. sum NLL 对应 penalty $1/(2\tau^2)$，mean NLL 对应 $1/(2n\tau^2)$；
4. optimizer 的 weight decay 更新是否等价于对 objective 加 L2；AdamW 的 decoupled shrinkage 一般不等于 adaptive-gradient loss L2；
5. prior 定义在哪个参数坐标；非线性变换后密度要乘 Jacobian；
6. 被惩罚参数是否包含 bias、normalization scale 等，代码 mask 要一致；
7. prior 是否 proper；所谓 flat prior 在无界空间可能 improper；
8. 模型是否有 layer rescaling symmetry。功能相同的网络可能有不同 $\|\theta\|$，因此 parameter L2 并非函数空间不变 prior。

缺任何一项，都只能说“目标含 L2 penalty”，不能无条件宣称完整 Bayesian/MAP 解释。

## B. 手算与构造

### PROB-MLE-B01

令 $S=\sum_iX_i$。likelihood

$$
L(p)\propto p^S(1-p)^{n-S},\qquad0\le p\le1.
$$

所以

$$
\widehat p_{\rm MLE}=S/n,
$$

包括 $S=0,n$ 的边界。

Beta prior 后 posterior 是

$$
p\mid x\sim\operatorname{Beta}(\alpha,\beta),
\quad
\alpha=S+a,\quad\beta=n-S+b.
$$

若 $\alpha>1,\beta>1$，unique interior MAP：

$$
\widehat p_{\rm MAP}
=\frac{\alpha-1}{\alpha+\beta-2}
=\frac{S+a-1}{n+a+b-2}.
$$

边界必须按 density 形状处理：

- $\alpha\le1,\beta>1$：mode 在 0；
- $\alpha>1,\beta\le1$：mode 在 1；
- $\alpha=\beta=1$：posterior uniform，每点都是 mode；
- $\alpha<1,\beta<1$：density 在 0 与 1 都发散，两个边界都是 extended modes；
- 若一个 shape 等于 1、另一个小于 1，mode 在后者对应的 singular boundary。

posterior mean 始终在 proper posterior $\alpha,\beta>0$ 时存在：

$$
E[p\mid x]=\frac{\alpha}{\alpha+\beta}
=\frac{S+a}{n+a+b}.
$$

它一般不同于 MAP，并且在极端样本下仍可位于内部；这说明 mode 与 posterior average 回答不同决策问题。

### PROB-MLE-B02

log-likelihood 忽略常数：

$$
\ell(\mu,\sigma^2)
=-\frac n2\log\sigma^2
-\frac1{2\sigma^2}\sum_i(x_i-\mu)^2.
$$

固定 $\sigma^2$ 对 $\mu$ 最大化，得到

$$
\widehat\mu=\bar x.
$$

代回并对 $\sigma^2$ 求导：

$$
\widehat\sigma^2_{\rm MLE}
=\frac1n\sum_i(x_i-\bar x)^2.
$$

由

$$
E\sum_i(X_i-\bar X)^2=(n-1)\sigma^2,
$$

得

$$
E[\widehat\sigma^2_{\rm MLE}]
=\frac{n-1}{n}\sigma^2,
$$

所以 bias 为 $-\sigma^2/n$。无偏 sample variance 用分母 $n-1$：

$$
S^2=\frac1{n-1}\sum_i(X_i-\bar X)^2.
$$

若所有 $x_i=c$，取 $\mu=c$ 后 residual sum of squares 为零，

$$
L(c,\sigma^2)=(2\pi\sigma^2)^{-n/2}\to\infty
\quad(\sigma^2\downarrow0).
$$

在参数空间 $\sigma^2>0$ 内没有有限 maximizer；若强行允许 $\sigma^2=0$，得到的是退化分布，不再是原 Lebesgue-density model。

### PROB-MLE-B03

设 $M=X_{(n)}=\max_iX_i$。联合 likelihood：

$$
L(\theta;x)
=\theta^{-n}\mathbf1\{\theta\ge M\}.
$$

在可行区 $\theta\ge M$ 上它单调递减，因此

$$
\widehat\theta_{\rm MLE}=M.
$$

对 $0\le m\le\theta$，

$$
P(M\le m)
=P(X_1\le m,\ldots,X_n\le m)
=\left(\frac m\theta\right)^n.
$$

所以 density 为 $nm^{n-1}/\theta^n$，并且

$$
E[M]=\frac n{n+1}\theta.
$$

无偏修正为

$$
\widetilde\theta=\frac{n+1}{n}M.
$$

若只在“内部”写 $\ell=-n\log\theta$，score $-n/\theta$ 永远不为零，似乎无解；真正 maximizer 由参数依赖的 indicator support 所定义的边界产生。这正是 score=0 不是通用算法的例子。

## C. 推导与证明

### PROB-MLE-C01

若真实密度为 $p_{\theta_0}$，则

$$
\begin{aligned}
E_{\theta_0}[\log p_\theta(X)]
&=E_{\theta_0}[\log p_{\theta_0}(X)]
-E_{\theta_0}\left[
\log\frac{p_{\theta_0}(X)}{p_\theta(X)}
\right]\\
&=E_{\theta_0}[\log p_{\theta_0}(X)]
-D_{\rm KL}(p_{\theta_0}\|p_\theta).
\end{aligned}
$$

第一项与 $\theta$ 无关，KL 非负，所以最大化 expected log-likelihood 等价于最小化 forward KL。若模型可辨识，唯一 maximizer 是 $\theta_0$。

若真实分布为 $Q$ 且不在模型中，定义

$$
\theta^*
\in\arg\max_\theta E_Q[\log p_\theta(X)]
=\arg\min_\theta D_{\rm KL}(Q\|P_\theta).
$$

$\theta^*$ 是 pseudo-true parameter/KL projection，不是“真实生成参数”。若 minimizer 不唯一，还需把目标定义为集合或增加 identification rule。

### PROB-MLE-C02

iid negative log-likelihood 为

$$
L_{\rm sum}(\theta)
=-\sum_{i=1}^n\log p_\theta(x_i).
$$

Gaussian prior

$$
\pi(\theta)\propto
\exp\left(-\frac{\|\theta\|^2}{2\tau^2}\right).
$$

negative log-posterior 忽略常数：

$$
L_{\rm MAP,sum}(\theta)
=L_{\rm sum}(\theta)+\frac1{2\tau^2}\|\theta\|^2.
$$

若代码使用 mean NLL

$$
L_{\rm mean}(\theta)=\frac1nL_{\rm sum}(\theta),
$$

把整个 posterior objective 除以 $n$ 才保留同一 argmin：

$$
L_{\rm MAP,mean}(\theta)
=L_{\rm mean}(\theta)
+\frac1{2n\tau^2}\|\theta\|^2.
$$

因此

$$
\lambda_{\rm sum}=\frac1{2\tau^2},
\qquad
\lambda_{\rm mean}=\frac1{2n\tau^2}.
$$

若 mean loss 下固定 $\lambda$ 而改变 $n$，隐含 prior variance 是

$$
\tau^2=\frac1{2n\lambda},
$$

随样本量变窄；这不是“同一个 fixed prior 下更多数据自然压倒 prior”的 Bayesian scaling。

### PROB-MLE-C03

设 $\phi=g(\theta)$ 是一一映射。若

$$
\widehat\theta\in\arg\max_\theta L(\theta;x),
$$

则任意 $\phi$ 对应唯一 $\theta=g^{-1}(\phi)$，所以

$$
\arg\max_\phi L(g^{-1}(\phi);x)
=g(\arg\max_\theta L(\theta;x)).
$$

故 MLE equivariant：

$$
\widehat\phi_{\rm MLE}=g(\widehat\theta_{\rm MLE}).
$$

MAP 针对 density mode，而 density 随坐标带 Jacobian。令 $\Theta>0$ 有 posterior density

$$
p_\Theta(\theta)=e^{-\theta},\qquad\theta>0.
$$

在 $\theta$ 坐标中密度严格递减，supremum 位于 $\theta\downarrow0$；若把边界纳入，则 mode 为 0。

令 $\Phi=\log\Theta$。因为 $\theta=e^\phi$ 且 $d\theta/d\phi=e^\phi$，

$$
p_\Phi(\phi)
=p_\Theta(e^\phi)e^\phi
=\exp(\phi-e^\phi).
$$

其 log-density 导数为

$$
\frac d{d\phi}[\phi-e^\phi]=1-e^\phi,
$$

unique mode 是 $\phi=0$，对应 $\theta=1$，而不是原坐标的边界 mode。概率测度未变，density mode 变了；因此 MAP 不具一般坐标不变性。

## D. 边界、反例与纠错

### PROB-MLE-D01

用 $y_i\in\{-1,1\}$。若存在 $w$ 使所有 margin

$$
m_i=y_iw^\top x_i>0,
$$

考察参数 $\beta_t=tw$。log-likelihood：

$$
\ell(\beta_t)
=\sum_i\log\sigma(y_i\beta_t^\top x_i)
=\sum_i\log\sigma(tm_i).
$$

当 $t\to\infty$，每个 $\sigma(tm_i)\to1$，故 $\ell(\beta_t)\to0$。而任何有限 $t$ 时每项 $\log\sigma(tm_i)<0$，所以 0 是 supremum 但不能由有限参数达到，MLE 不存在。

加入 L2 penalty 后最大化

$$
\ell(\beta)-\lambda\|\beta\|^2,\qquad\lambda>0.
$$

当 $\|\beta\|\to\infty$，penalty 使目标趋 $-\infty$；在连续、适当设计下得到有限 maximizer，严格 concavity 时唯一。它定义的是 penalized/MAP-like 问题，不是恢复了原 unregularized MLE。

### PROB-MLE-D02

两分量 mixture：

$$
p(x)=\pi\varphi(x;\mu_1,\sigma_1^2)
+(1-\pi)\varphi(x;\mu_2,\sigma_2^2).
$$

固定 $0<\pi<1$，令 $\mu_1=x_1$、$\sigma_1\downarrow0$。对第一个样本，

$$
p(x_1)\ge
\frac{\pi}{\sqrt{2\pi}\sigma_1}\to\infty.
$$

把第二分量选择为对其余数据给有限正密度的 Gaussian，则其余 likelihood factors 有正下界；于是 joint likelihood product 无界，普通 MLE 不存在。

label switching：交换 $(\pi,\mu_1,\sigma_1)$ 与 $(1-\pi,\mu_2,\sigma_2)$ 得同一分布，造成全局多重等价参数。

component collision：若两个 components 参数相同，mixture weight 无法从分布辨识，局部 Fisher 退化；这是 singularity，不仅是离散标签重命名。variance collapse 又是 likelihood singularity。三者需分别诊断。

### PROB-MLE-D03

记

$$
\mathrm{CE}_{\rm sum}=\sum_i\ell_i,
\qquad
\mathrm{CE}_{\rm mean}=\frac1n\sum_i\ell_i.
$$

目标一：

$$
J_1=\mathrm{CE}_{\rm mean}+\lambda_{\rm mean}\|\theta\|^2.
$$

乘以 $n$ 不改变 argmin：

$$
nJ_1=\mathrm{CE}_{\rm sum}
+n\lambda_{\rm mean}\|\theta\|^2.
$$

因此要与

$$
J_2=\mathrm{CE}_{\rm sum}+\lambda_{\rm sum}\|\theta\|^2
$$

相同，必须

$$
\lambda_{\rm sum}=n\lambda_{\rm mean}.
$$

使用相同数值 $\lambda$ 时，mean objective 的 penalty 相对于单样本和强 $n$ 倍。

AdamW 更新含

$$
\theta_{t+1}
=\theta_t-\eta_t\,\mathrm{AdamDirection}_t
-\eta_t\lambda\theta_t.
$$

loss L2 则先把 $2\lambda\theta$ 加入 gradient，再经过 Adam 的坐标自适应归一化。两条更新一般不同；learning-rate schedule、parameter groups 与 mask 还会改变隐含 shrinkage。因此不能仅凭“有 weight decay”指定一个精确 Gaussian prior。

## E. AI 迁移

### PROB-MLE-E01

数据 $(x_i,y_i)$，$y_i\in\{1,\ldots,K\}$，logits $z_\theta(x)$：

$$
p_\theta(y=k\mid x)
=\frac{e^{z_k}}{\sum_je^{z_j}}.
$$

conditional log-likelihood

$$
\ell(\theta)=\sum_i
\left[z_{i,y_i}-\log\sum_je^{z_{ij}}\right].
$$

negative mean 是 one-hot cross-entropy。修改项：

- class weighting：变成 reweighted empirical distribution/risk；若权重来自 inverse prevalence，目标可能接近 class-balanced risk，而非原采样分布 MLE；
- label smoothing：one-hot target 换成软分布，等价于额外 cross-entropy/regularization，不是原观测标签 likelihood；
- focal loss：乘 $(1-p_y)^\gamma$，形成参数依赖权重，一般不再是规范 categorical log score；
- mixup：输入和 target 都插值，训练的是 augmented vicinal distribution 上的软标签风险。

这些目标可能改善特定 calibration、class balance 或 robustness，但必须用新 estimand 描述，不能仍声称是未经修改的数据 likelihood MLE。

### PROB-MLE-E02

对序列 $x_{1:T}$：

$$
p_\theta(x_{1:T})
=\prod_{t=1}^T p_\theta(x_t\mid x_{<t}),
$$

$$
\mathrm{NLL}_{\rm seq}
=-\sum_{t=1}^T\log p_\theta(x_t\mid x_{<t}).
$$

teacher forcing 在训练时使用真实 prefix。若 mask $m_{bt}\in\{0,1\}$：

$$
L_{\rm token}
=-\frac{\sum_{b,t}m_{bt}\log p_\theta(x_{bt}\mid x_{b,<t})}
{\sum_{b,t}m_{bt}}.
$$

- per-token mean：随机 token 加权，长序列贡献更多；
- per-sequence mean：先每序列求和再对 batch 平均，目标是平均 sequence NLL，长序列仍因 sum 权重大；
- length-normalized per-sequence：先除各自长度，每条序列等权，改变了原 joint log-likelihood scaling。

最低审计：padding/causal mask；BOS/EOS 与 tokenizer；log-softmax 数值稳定；ignore-index denominator；sequence truncation；duplicate/user dependence；token/sequence reduction；vocabulary support/zero probability；train–eval teacher-forcing gap；bits-per-token 与不同 tokenizer 不可直接比较。

### PROB-MLE-E03

$$
\log p_\theta(x)=-E_\theta(x)-\log Z_\theta,
\quad
Z_\theta=\int e^{-E_\theta(u)}du.
$$

由于

$$
\nabla_\theta\log Z_\theta
=-E_{U\sim p_\theta}[\nabla_\theta E_\theta(U)],
$$

所以

$$
\nabla_\theta\log p_\theta(x)
=-\nabla_\theta E_\theta(x)
+E_{U\sim p_\theta}[\nabla_\theta E_\theta(U)].
$$

第一项是 data/positive phase，第二项是 model/negative phase；后者需要从当前全局模型分布取期望，通常昂贵且受混合影响。

- NCE 把 density estimation 改写为 data-vs-noise classification，在条件满足时可一致估计未归一化模型，但有限噪声比下不是逐步精确 likelihood gradient；
- contrastive divergence 用从数据启动的短 MCMC 替代 equilibrium negative phase，通常有 bias；
- score matching 匹配 data score，利用分部积分绕开 $Z_\theta$，优化的是另一 proper discrepancy，需边界与可微条件。

所以应报告 objective、sampler/noise distribution、近似 bias 与诊断，而不能把三者统称为“精确 MLE”。

## 结论复盘

- likelihood 是固定数据后的参数函数，不是 posterior；
- score equation 只处理 interior differentiable candidate；
- MLE/MAP 都是点估计，MAP 还依赖参数坐标；
- regularization 与 prior 的对应必须核对 reduction、$n$、optimizer 和 symmetry；
- AI surrogate/approximate objective 应按实际 estimand 命名。
