---
type: source
status: draft
area: [sources, neural-networks/normalization]
source_type: paper
title: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"
author: "Sergey Ioffe; Christian Szegedy"
year: 2015
url: "https://proceedings.mlr.press/v37/ioffe15.html"
arxiv: "1502.03167"
venue: "ICML 2015, PMLR 37:448–456"
accessed: 2026-08-23
source_tier: A
license: "PMLR author paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[归一化的对象、轴与不变性]]", "[[BatchNorm 前向统计与训练—推理差异]]", "[[BatchNorm 反向传播、尺度不变性与噪声]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Ioffe–Szegedy：Batch Normalization

> [!abstract] 来源定位
> BatchNorm 原始论文定义了 mini-batch 标准化、可学习的 gain/shift、卷积特征图上的归约集合，以及训练时 batch statistics 与推理时 population estimates 的双路径。论文以 internal covariate shift 作为主要动机；这一机制解释后来受到直接实验挑战，因此本库把“方法定义与历史实验”同“为何有效”分账。

## 元数据与原始入口

- 正式页面：[PMLR 论文页](https://proceedings.mlr.press/v37/ioffe15.html)；
- arXiv：[1502.03167](https://arxiv.org/abs/1502.03167)；
- 原始算法：第 3 节 Algorithm 1/2；卷积扩展：第 3.2 节；
- 当前调用者：[[BatchNorm 前向统计与训练—推理差异]]、[[BatchNorm 反向传播、尺度不变性与噪声]]。

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | 对一个 mini-batch 的标量 feature，以 batch mean 与 $m^{-1}$ 方差标准化，再施加 $gamma,\beta$ | 定义/算法 | 归约集合与 estimator 必须声明 | 课程定义主来源 |
| C2 | 卷积 BN 对同一 channel 的 batch 与 spatial locations 联合归约 | 定义/算法 | effective count 为 $N H W$；参数仍 per-channel | 已核验 |
| C3 | 训练用 mini-batch statistics，推理用固定 population estimates | 算法语义 | population 量实际由训练期统计估计；框架更新规则可不同 | 已核验 |
| C4 | $gamma,\beta$ 允许归一化层恢复必要的尺度和平移 | 表达能力说明 | 不等于恢复被 group statistics 删除的全部依赖 | 有条件成立 |
| C5 | BN 通过减少 internal covariate shift 改善训练 | 原始解释/经验假说 | 论文中的定义和因果链并非最终共识 | 保留为历史解释 |
| C6 | 原论文的 Inception 设置中 BN 允许更大学习率并显著减少达到目标精度的 steps | 实验 | 同时改变 LR、dropout、weight decay、shuffle 等；不可外推为普遍倍率 | 设置内成立 |

## 课程采用的最小公式

对归约组 $\mathcal B=\{x_1,\ldots,x_m\}$，论文使用

$$
\mu_{\mathcal B}=\frac1m\sum_{i=1}^m x_i,
\qquad
\sigma_{\mathcal B}^2=\frac1m\sum_{i=1}^m(x_i-\mu_{\mathcal B})^2,
$$

$$
\widehat x_i=\frac{x_i-\mu_{\mathcal B}}
{\sqrt{\sigma_{\mathcal B}^2+\varepsilon}},
\qquad
y_i=\gamma\widehat x_i+\beta.
$$

这里的 $m$ 是归约组大小，不必等于数据加载器的 batch size。卷积输入 $N\times C\times H\times W$ 对每个 channel 有 $m=NHW$。

## 需要与现代实现分开的地方

- 原论文给出方法合同，不固定所有框架的 running-statistic momentum 记号；
- forward normalization 的 biased variance 与 running buffer 是否使用 bias correction 是实现层选择；
- 推理折叠、mixed precision、SyncBN 与 microbatch accumulation 属于后续系统语义；
- “某批归一后 mean 近零、variance 近一”不等于总体分布 Gaussian，也不等于 features 独立。

## 机制争议与证据边界

原论文把输入分布随上游参数变化称为 internal covariate shift，并以减少这种变化解释训练改善。[[S-2018-Santurkar-BatchNorm-Optimization]] 设计 noisy-BN 等实验，显示按一阶、二阶统计稳定性理解的 ICS 与性能并不充分对应，并提出 loss/gradient smoothness 视角。课程因此只把 C1—C4 当作稳定方法定义；C5 是历史假说，不能写成定理。

## 后续调用

- NN-34：Algorithm 1/2、卷积归约与 train/eval 双语义；
- NN-35：batch coupling、尺度不变性与反向 Jacobian；
- NN-40：small batch、SyncBN、distributed aggregation 与有限精度边界。

