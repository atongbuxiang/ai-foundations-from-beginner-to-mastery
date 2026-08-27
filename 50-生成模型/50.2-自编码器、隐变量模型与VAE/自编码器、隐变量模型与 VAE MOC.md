---
type: moc
status: active
area: [generative-models, vae, latent-variable-models]
aliases: [生成模型第二卷, VAE课程地图]
prerequisites: ["[[生成建模对象、似然与自回归 MOC]]", "[[变分推断、ELBO 与证据分解]]", "[[多元高斯分布]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# 自编码器、隐变量模型与 VAE MOC

> [!abstract] 分卷目标
> 本卷从普通自编码器的“重构成功但不可采样”出发，建立隐变量生成模型 $p_\theta(x,z)$，逐式推导 VAE 的 ELBO 与重参数化梯度，再分清 likelihood、IWAE、rate、互信息、posterior collapse、层次结构和解耦证据。学完后，你应能从一段 VAE 代码反推出完整概率合同，并判断它究竟优化了什么、估计了什么、还没有证明什么。

## 一、为什么不能只记“重构项 + KL 项”

这个口诀隐藏了最关键的选择：重构项究竟是哪种观测似然，KL 比较哪两个分布，encoder 是模型的一部分还是推断工具，训练 loss 是 exact likelihood、下界还是 Monte Carlo 估计。不同答案会改变单位、最优解、采样程序与科学结论。本卷始终维护五本局部账：

$$
\underbrace{p(z)}_{\text{先验}},\quad
\underbrace{p_\theta(x\mid z)}_{\text{生成/观测模型}},\quad
\underbrace{p_\theta(x)}_{\text{证据}},\quad
\underbrace{p_\theta(z\mid x)}_{\text{模型真后验}},\quad
\underbrace{q_\phi(z\mid x)}_{\text{近似后验}}.
$$

## 二、八个核心节点

| ID | 节点 | 主要出口 | 正文 | 题解 |
|---|---|---|---|---|
| GEN-09 | [[自编码器、重构与生成缺口]] | 用三个反例说明重构好不等于可生成 | verified | 已配套 |
| GEN-10 | [[隐变量模型的联合分布、边缘似然与后验]] | 从 joint 推出 evidence、posterior 与可计算瓶颈 | verified | 已配套 |
| GEN-11 | [[VAE 的 ELBO、变分后验与重参数化梯度]] | 两条路线推导 ELBO，并写出低方差 pathwise gradient | verified | 已配套 |
| GEN-12 | [[Gaussian VAE 的闭式 KL、解码似然与尺度合同]] | 独立推导 diagonal Gaussian KL，审计 MSE/BCE 尺度 | verified | 已配套 |
| GEN-13 | [[IWAE、重要性权重与推断缺口]] | 区分 bound、density estimator 和四类 gap | verified | 已配套 |
| GEN-14 | [[Posterior Collapse、率失真与解码器容量]] | 用 rate decomposition 判断 KL 消失与信息失用 | verified | 已配套 |
| GEN-15 | [[层次 VAE、表达性先验与近似后验 Flow]] | 按“改 prior/likelihood/posterior/层次”比较方法 | verified | 已配套 |
| GEN-16 | [[VAE 的条件、聚类、解耦主张与证据地图]] | 区分条件生成、聚类与可识别解耦的证据强度 | verified | 已配套 |

静态状态只表示材料和审计齐备；个人是否掌握仍以[[50.2 分卷累计测验与复现门]]的独立作答为准。

## 三、认知顺序

GEN-09（重构不等于生成）→ GEN-10（joint/evidence/posterior）→ GEN-11（ELBO/reparameterization）→ GEN-12（Gaussian 实现合同）与 GEN-13（IWAE/gap）→ GEN-14（collapse/rate-distortion）→ GEN-15（hierarchy/prior/flow）→ GEN-16（condition/cluster/disentangle）。

## 四、全卷符号合同

| 符号 | 含义 | 最常见误读 |
|---|---|---|
| $p(z)$ 或 $p_\lambda(z)$ | 生成先验 | 不是训练样本 encoder 输出的直方图 |
| $p_\theta(x\mid z)$ | decoder/观测似然 | decoder 的均值图不是整个概率分布 |
| $p_\theta(x,z)$ | 生成联合分布 | 不包含 $q_\phi$ |
| $p_\theta(x)$ | evidence/marginal likelihood | 通常需要积分，不能由一次重构读出 |
| $p_\theta(z\mid x)$ | 由 joint 唯一决定的模型后验 | 通常不可直接算 |
| $q_\phi(z\mid x)$ | amortized variational posterior | 是推断分布，不是生成先验 |
| $q_\phi(z)=\int p_*(x)q_\phi(z\mid x)dx$ | aggregate posterior | 不等于每个条件后验 |
| $R=\mathbb E_x\mathrm{KL}(q_\phi(z\mid x)\|p(z))$ | rate | 不必等于互信息 |

科学空间早期 VAE 文章有时把生成分布与识别分布的字母角色写成另一套约定。本卷不判断哪套“更正统”，只要求每次出现都映射到上表，禁止同页漂移。

## 五、科学空间研读路径

1. [[S-2018-Su-5253-变分自编码器一]]：从 AE 到“编码为分布”的直觉入口；
2. [[S-2018-Su-5343-VAE从贝叶斯观点出发]]与[[S-2018-Su-5383-变分自编码器三]]：joint、近似后验和重参数化桥梁；
3. [[S-2021-Su-8791-VAE估计样本概率密度]]：importance likelihood 与 IWAE 评价；
4. [[S-2018-Su-6088-VAE最小化先验与最大化互信息]]、[[S-2018-Su-6181-变分编码与信息瓶颈]]：rate、互信息和 bottleneck；
5. [[S-2020-Su-7381-VAE-BN防KL消失]]、[[S-2020-Su-7725-VAE几何视角]]、[[S-2021-Su-8404-vMF-VAE]]：collapse 与潜空间几何；
6. [[S-2018-Su-5887-VAE聚类]]、[[S-2020-Su-7574-NVAE]]、[[S-2021-Su-8475-UniVAE]]：聚类、层次和文本 VAE 案例。

这些入口分别与 [[S-2013-Kingma-Welling-AEVB]]、[[S-2014-Rezende-Stochastic-Backprop]]、[[S-2015-Burda-IWAE]]、[[S-2019-He-Lagging-Inference]]、[[S-2020-Vahdat-NVAE]]、[[S-2018-Davidson-Hyperspherical-VAE]]、[[S-2017-Higgins-BetaVAE]]、[[S-2017-Zhao-InfoVAE]]和[[S-2018-Locatello-Disentanglement-Impossibility]]对照。博客负责可读性，原论文负责定义与直接证据，本卷负责补齐条件、反例和独立计算。

## 六、通过标准

- 能从 joint 独立推出 posterior、evidence 与 ELBO identity；
- 能推 diagonal Gaussian KL，并从 likelihood 写出 MSE/BCE 的系数与 reduction；
- 能区分 exact evidence、ELBO、IWAE bound、importance density estimate 与 log estimate；
- 能证明 $R=I_q(X;Z)+\mathrm{KL}(q(z)\|p(z))$；
- 能构造“KL 正但 $Z$ 无用”和“重构好但 prior sampling 坏”的反例；
- 能对 conditional/clustering/disentanglement 声明建立数据、指标、干预和可识别性证据表；
- 能运行并改写[[实验 - VAE、ELBO 与潜变量最小数值审计]]。

## 七、入口与出口

- 前置卷：[[生成建模对象、似然与自回归 MOC]]
- 累计门：[[50.2 分卷累计测验与复现门]]
- 下一卷：[[GAN、分布差异与对抗训练 MOC]]
