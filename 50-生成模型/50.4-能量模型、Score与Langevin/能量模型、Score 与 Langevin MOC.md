---
type: moc
status: active
area: [generative-models, energy-based-models, score-matching, langevin]
aliases: [生成模型第四卷, EBM与Score课程地图]
prerequisites: ["[[GAN、分布差异与对抗训练 MOC]]", "[[Fokker-Planck 方程与概率流 ODE]]", "[[时间反演、score 与扩散生成动力学]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# 能量模型、Score 与 Langevin MOC

> [!abstract] 分卷目标
> 本卷从未归一化密度出发，依次回答：配分函数为什么难、最大似然为什么出现正相—负相、score matching 怎样消去 $Z_\theta$、Gaussian 去噪为什么能学习 marginal score、为什么需要多噪声尺度，以及连续 Langevin、ULA、MALA 和 Predictor–Corrector 分别保证什么。学完后，你应能把“density 定义—训练目标—score 估计—Markov kernel—有限步输出”逐层审计。

## 一、八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| GEN-25 | [[能量模型、未归一化密度与配分函数]] | 判断 energy 是否定义合法 density，并建立 gauge/temperature 账 | verified |
| GEN-26 | [[最大似然的正相负相、对比散度与噪声对比估计]] | 推导 MLE 梯度，区分 CD、PCD、NCE 与负采样 | verified |
| GEN-27 | [[Score Matching、分部积分与配分函数消去]] | 从 Fisher divergence 推出 Hyvärinen objective 与边界项 | verified |
| GEN-28 | [[去噪 Score Matching、Tweedie 公式与条件期望]] | 证明 denoiser、conditional score 与 marginal score 的投影关系 | verified |
| GEN-29 | [[多噪声尺度、退火去噪与 Score 网络]] | 设计 noise ladder、权重和 annealed sampler 合同 | verified |
| GEN-30 | [[Langevin、ULA、MALA 与平稳分布]] | 分清 invariant law、mixing、discretization bias 与 MH 校正 | verified |
| GEN-31 | [[Predictor–Corrector 与 Score-based 生成程序]] | 分离路径推进误差与固定噪声层的 MCMC 校正 | verified |
| GEN-32 | [[EBM、Score、GAN 与 Diffusion 的接口和证据地图]] | 识别严格等价、目标等价、算法接口与仅为类比的关系 | verified |

静态状态不等于个人通过；出口由[[50.4 分卷累计测验与复现门]]记录。

## 二、全卷五本账

$$
\tilde p_\theta(x)=e^{-E_\theta(x)},\qquad
Z_\theta=\int\tilde p_\theta,d\nu,
\qquad p_\theta=\tilde p_\theta/Z_\theta,
$$

$$
s_\theta(x)=\nabla_x\log p_\theta(x)=-\nabla_xE_\theta(x).
$$

| 账 | 对象 | 典型问题 |
|---|---|---|
| density | $p_\theta$ 与基准测度 $\nu$ | $Z_\theta$ 是否有限，likelihood 是否可算？ |
| objective | MLE、NCE、SM、DSM | estimand 与总体最优点是什么？ |
| estimator | 数据 batch、noise、Hutchinson、短链 | 无偏、有偏，方差多大？ |
| dynamics | diffusion、ULA/MALA、reverse solver | invariant、mixing 与数值稳定是否成立？ |
| deployment | 有限 NFE、temperature、最后去噪 | 最终输出究竟是哪一个分布？ |

## 三、科学空间—一级来源路径

1. [[S-2019-Su-6331-GAN分析与采样]]：正相—负相与“分析/采样”矛盾；
2. [[S-2019-Su-6612-生成模型等于能量模型]]：Langevin + replay buffer 的 neural EBM 案例；
3. [[S-2018-Su-5617-噪声对比估计与配分函数]]：NCE 的中文问题入口；
4. [[S-2019-Su-7038-从去噪自编码器到生成模型]]：denoiser—score—Langevin 主桥；
5. [[S-2023-Su-9509-得分匹配与条件得分匹配]]：条件期望投影解释。

严格结论分别对照 [[S-2010-Gutmann-Hyvarinen-NCE]]、[[S-2005-Hyvarinen-Score-Matching]]、[[S-2011-Vincent-Denoising-Score-Matching]]、[[S-2019-Song-Ermon-NCSN]]、[[S-1996-Roberts-Tweedie-Langevin]]、[[S-2019-Du-Mordatch-EBM]]与[[S-2021-Song-Score-SDE]]。

## 四、通过标准

- 从 $Z_\theta$ 独立推导 maximum-likelihood 正负相并检查符号；
- 说明 CD-$k$ 为何通常不是 exact MLE gradient，NCE 又为何不是 CD；
- 写出 score matching 的逐坐标分部积分与 boundary term；
- 证明 Gaussian Tweedie 公式和 conditional/marginal score 的 $L^2$ 分解；
- 用双峰 mixture 解释单一小噪声的低密度区困难；
- 手算 Gaussian target 下 ULA 的平稳方差偏差，并写出 MALA acceptance ratio；
- 对 PC sampler 做 score/solver/mixing/NFE 四账审计；
- 运行并改写[[实验 - EBM、Score 与 Langevin 最小数值审计]]。

## 五、入口与出口

- 前置：[[GAN、分布差异与对抗训练 MOC]]
- 数学底座：[[Fokker-Planck 方程与概率流 ODE]]
- 累计门：[[50.4 分卷累计测验与复现门]]
- 下一卷：[[Normalizing Flow 与可逆密度变换 MOC]]

