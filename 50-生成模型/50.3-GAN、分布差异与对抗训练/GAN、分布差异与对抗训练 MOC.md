---
type: moc
status: active
area: [generative-models, gan, game-theory]
aliases: [生成模型第三卷, GAN课程地图]
prerequisites: ["[[生成建模对象、似然与自回归 MOC]]", "[[f-散度、Bregman 散度与概率度量]]", "[[非凸优化、鞍点与深度网络损失地形]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# GAN、分布差异与对抗训练 MOC

> [!abstract] 分卷目标
> 本卷把 GAN 拆成四层：生成器诱导的隐式分布、population variational objective、有限 critic 的估计与优化、交替 game dynamics。学完后，你应能推导原始 GAN 的最优判别器与 JS，比较 f-divergence/IPM/$W_1$，审计 Lipschitz enforcement，并用动力学与覆盖指标诊断稳定性和 mode collapse。

## 一、八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| GEN-17 | [[隐式 Pushforward 分布、生成器与判别博弈]] | 从 latent map 定义样本分布与二分类 game | verified |
| GEN-18 | [[原始 GAN、最优判别器与 Jensen–Shannon 散度]] | 逐点推出 $D^*$ 与 JS value | verified |
| GEN-19 | [[饱和、非饱和生成器损失与 f-GAN]] | 区分相同 equilibrium 与不同 gradient field | verified |
| GEN-20 | [[IPM、Wasserstein-1 与 Kantorovich 对偶]] | 用 coupling/dual 和点质量反例理解 topology | verified |
| GEN-21 | [[Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]] | 分清 global constraint、upper bound 与 sampled penalty | verified |
| GEN-22 | [[Minimax 动力学、旋转、阻尼与局部收敛]] | 手算 bilinear rotation，区分 stationarity 与 Nash | verified |
| GEN-23 | [[Mode Collapse、模式覆盖与生成器熵]] | 将清晰度、覆盖、熵和 latent collision 分账 | verified |
| GEN-24 | [[GAN 稳定化方法、受控比较与证据地图]] | 按 objective/constraint/optimizer/architecture 做公平比较 | verified |

静态状态不等于个人通过；出口由[[50.3 分卷累计测验与复现门]]记录。

## 二、全卷对象账

$$
Z\sim P_Z,\quad X_g=G_\theta(Z),\quad P_\theta=G_{\theta\#}P_Z,
\quad D_\psi:\mathcal X\to(0,1)\ \text{或}\ f_\psi:\mathcal X\to\mathbb R.
$$

| 层 | 对象 | 不得混同 |
|---|---|---|
| population | $P_*,P_\theta$ 与无限函数类 supremum | 理论 divergence/IPM |
| empirical | $\widehat P_n,\widehat P_{\theta,m}$ | 有限样本估计 |
| restricted | neural critic class $\mathcal F_\Psi$ | 通常只给 lower bound/受限 IPM |
| optimized | 若干 SGD 步得到的 $\psi_t$ | 不等于 best response |
| deployed | $G_{\theta_t}$ 与 latent/truncation protocol | 不等于训练 objective |

## 三、科学空间—一级来源路径

1. [[S-2018-Su-6016-fGAN与变分散度]]：Fenchel variational representation；
2. [[S-2019-Su-6280-Wasserstein距离与WGAN]]：coupling、KR dual 与 WGAN；
3. [[S-2018-Su-6051-Lipschitz约束]]：operator/network constraint；
4. [[S-2019-Su-6316-GAN能量视角]]：能量/挖坑跳坑直觉；
5. [[S-2021-Su-8244-WGAN成功与距离近似]]：训练成功不反证 critic 精确估计 $W_1$。

与 [[S-2014-Goodfellow-GAN]]、[[S-2017-Arjovsky-WGAN]]、[[S-2017-Gulrajani-WGAN-GP]]、[[S-2018-Miyato-Spectral-Normalization]]、[[S-2018-Mescheder-GAN-Convergence]]、[[S-2017-Heusel-TTUR]]、[[S-2016-Salimans-Improved-GAN]]、[[S-2016-Metz-Unrolled-GAN]]和[[S-2015-Theis-Generative-Evaluation]]对照。

## 四、通过标准

- 从二分类 log score 独立推 $D^*$ 与 $-\log4+2JS$；
- 用 logits 导数解释 saturating/non-saturating gradient；
- 手算 $\delta_0,\delta_\theta$ 的 JS 与 $W_1$；
- 从 layer spectral norms 给 network Lipschitz 上界，并说明为何 GP 非全域证书；
- 分析 bilinear game 的同步 GDA 特征值；
- 设计 mode coverage/precision-recall 与 latent collision 审计；
- 运行并改写[[实验 - GAN 目标、Wasserstein 与博弈动力学最小数值审计]]。

## 五、入口与出口

- 前置：[[自编码器、隐变量模型与 VAE MOC]]
- 累计门：[[50.3 分卷累计测验与复现门]]
- 下一卷：[[能量模型、Score 与 Langevin MOC]]
