---
type: moc
status: active
area: [generative-models, diffusion, ddpm]
aliases: [生成模型第六卷, 离散扩散课程地图]
prerequisites: ["[[常用连续分布与指数族]]", "[[Gaussian VAE 的闭式 KL、解码似然与尺度合同]]", "[[去噪 Score Matching、Tweedie 公式与条件期望]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# DDPM、DDIM 与离散时间扩散 MOC

> [!abstract] 分卷目标
> 本卷从固定 Gaussian forward Markov chain 出发，闭式求任意噪声时刻和 one-step posterior，再把整条 reverse generative chain 的 ELBO 拆成逐步 KL。随后严格换算 $x_0/\epsilon/v/score$ 参数化，区分 ELBO 与 simplified loss，处理 variance、DDIM 与一般边缘一致性，最后把全部公式落到一个可审计的最小实现。

## 一、八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| GEN-41 | [[DDPM 前向 Markov 加噪与闭式边缘]] | 从单步 kernel 推出任意 $q(x_t\mid x_0)$ 并一次采样 | verified |
| GEN-42 | [[DDPM 反向后验、ELBO 与逐步 KL]] | 手算 posterior mean/variance，重建整条 VLB | verified |
| GEN-43 | [[数据、噪声、速度与 Score 参数化]] | 无误换算 $x_0/\epsilon/v/score$ 并分离 loss weighting | verified |
| GEN-44 | [[扩散简化损失、时间加权、Schedule 与 SNR]] | 分清总体最优点、ELBO 权重、采样分布和有限训练 | verified |
| GEN-45 | [[反向均值、固定方差、学习方差与 Analytic-DPM]] | 区分 posterior variance、reverse mixture 与 mean-error variance | verified |
| GEN-46 | [[DDIM、非 Markov 前向族与确定性采样]] | 从共享边缘构造 stochastic/deterministic skip sampler | verified |
| GEN-47 | [[条件核、边缘一致性与统一离散扩散框架]] | 检查任意 corruption/reverse kernel 是否 marginal-consistent | verified |
| GEN-48 | [[最小 DDPM 的张量合同、复现门与证据地图]] | 从数据缩放到采样循环逐行验收 | verified |

## 二、全卷统一符号

本卷固定原 DDPM 常用约定：

$$
\beta_t\in(0,1),\qquad
\alpha_t=1-\beta_t,\qquad
\bar\alpha_t=\prod_{s=1}^t\alpha_s,
$$

$$
a_t\triangleq\sqrt{\bar\alpha_t},\qquad
\sigma_t\triangleq\sqrt{1-\bar\alpha_t}.
$$

于是 $x_t=a_tx_0+\sigma_t\epsilon$。注意：科学空间前三篇常把一步 signal/noise coefficients 直接记为 $\alpha_t,\beta_t$，并令平方和为 1；阅读框中必须先做符号翻译，不能把博客的 $\beta_t$ 直接代入本卷的 variance schedule。

## 三、五本账

| 账 | 对象 | 必问 |
|---|---|---|
| forward | 固定 $q(x_{1:T}\mid x_0)$ | 单步与累计系数是否 off-by-one？ |
| posterior | $q(x_{t-1}\mid x_t,x_0)$ | 为什么 tractable，和 $q(x_{t-1}\mid x_t)$ 是否混淆？ |
| parameter | $x_0,\epsilon,v,score$ | 公式可换后 loss 权重怎样变？ |
| reverse | $p_\theta(x_{t-1}\mid x_t)$ | mean、variance、clipping 与随机性是什么？ |
| program | timestep sampler、network calls、dtype | 训练/采样的形状、边界和 NFE 是否一致？ |

## 四、科学空间—一级来源

- [[S-2022-Su-9119-DDPM拆楼建楼]]：forward/reverse 直觉；
- [[S-2022-Su-9152-DDPM自回归式VAE]]：hierarchical latent/ELBO 视角；
- [[S-2022-Su-9164-DDPM贝叶斯去噪]]：Gaussian posterior 与去噪参数化；
- [[S-2022-Su-9181-DDIM]]：shared marginals 与 skip sampling；
- [[S-2022-Su-9245-最优扩散方差估计]]、[[S-2022-Su-9246-最优扩散方差估计下]]：reverse variance；
- [[S-2022-Su-9262-统一扩散模型理论篇]]、[[S-2022-Su-9271-统一扩散应用篇]]：marginal consistency。

一级证据：[[S-2015-SohlDickstein-Diffusion]]、[[S-2020-Ho-DDPM]]、[[S-2021-Nichol-Dhariwal-Improved-DDPM]]、[[S-2021-Song-DDIM]]、[[S-2022-Bao-Analytic-DPM]]、[[S-2021-Kingma-VDM]]与[[S-2022-Salimans-Ho-Progressive-Distillation]]。

## 五、当前出口

- 前置卷：[[Normalizing Flow 与可逆密度变换 MOC]]
- 数学底座：[[时间反演、score 与扩散生成动力学]]
- 数值审计：[[实验 - DDPM、DDIM 与离散扩散最小数值审计]]
- 本卷累计门：[[50.6 分卷累计测验与复现门]]
- 后继：[[生成模型完整课程地图与掌握标准#十、50.7 SDE、概率流 ODE 与 Flow Matching（GEN-49—56）|50.7 连续时间生成]]
