---
type: source
status: verified
area: [sources, ai/generative-models, math/probability]
source_type: blog
title: "漫谈重参数：从正态分布到Gumbel Softmax"
author: 苏剑林
year: 2019
url: "https://spaces.ac.cn/archives/6705"
accessed: 2026-08-25
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [数学研究, 信息时代]
series: "重参数"
scope_role: core
temporal_role: classical-exposition
related: ["[[常用离散分布]]", "[[常用连续分布与指数族]]", "[[多元高斯分布]]", "[[S-2018-Su-5253-变分自编码器一|变分自编码器]]"]
created: 2026-08-19
updated: 2026-08-25
---

# 漫谈重参数：从正态分布到 Gumbel–Softmax

> [!abstract] 来源定位
> 文章从含参数分布下的期望梯度出发，连接 Gaussian pathwise reparameterization、Categorical 的 Gumbel-max 表示、Gumbel–Softmax 连续松弛与梯度估计。课程采用它作为“采样、目标与梯度估计器必须分层”的 AI 问题入口；无偏性、方差比较、温度极限和微分—期望交换由正式概率与 Monte Carlo 来源补严。

## 元数据与纳入

- 正式引用：苏剑林，2019-06-10，《漫谈重参数：从正态分布到Gumbel Softmax》；
- 原始页面：[https://spaces.ac.cn/archives/6705](https://spaces.ac.cn/archives/6705)；
- 范围角色：`core`；当前调用者：[[常用离散分布]]、[[常用连续分布与指数族]]、[[多元高斯分布]]、[[Categorical Diffusion、转移矩阵与离散后验]]；
- 2026-08-25 已逐段核读正文，并与 Gumbel–Softmax、Concrete 原论文交叉核验。

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | Gaussian 可写为参数化仿射变换与固定标准噪声 | 恒等构造 | scale 非负；退化与可微边界单独处理 | 已核验 |
| C2 | pathwise 表示可让梯度通过随机样本路径 | 梯度方法 | 可微、可积且允许交换梯度与期望 | 有条件成立 |
| C3 | Categorical 可用 Gumbel-max 采样 | 分布恒等式 | 独立标准 Gumbel，logit/概率合法 | 已由原始来源核验 |
| C4 | Gumbel–Softmax 用有限温度连续化 one-hot | 松弛方法 | 有限温度改变支持与目标 | 成立 |
| C5 | 重参数通常降低梯度估计方差 | 经验/方法比较 | 不存在对所有函数和参数的普遍支配 | 只能写“常见但非绝对” |

## 课程采用的对象分层

原离散目标：

$$
L(\theta)=\mathbb E_{Z\sim p_\theta}[f_\theta(Z)].
$$

Gaussian pathwise：

$$
Z=\mu_\theta+\sigma_\theta\varepsilon,
\qquad \varepsilon\sim\mathcal N(0,1).
$$

Gumbel-max：

$$
Z=\arg\max_k(a_k+G_k).
$$

文章还直接积分验证：若 $G_k$ 独立服从标准 Gumbel，则第 $i$ 类胜出的概率是 $e^{a_i}/\sum_j e^{a_j}$。这一步证明的是 **hard argmax 样本的精确 Categorical law**。

Gumbel–Softmax 松弛：

$$
\widetilde Z_k
=\frac{e^{(a_k+G_k)/\tau}}
{\sum_je^{(a_j+G_j)/\tau}}.
$$

必须区分：原随机变量、松弛随机变量、对哪个目标求梯度、估计器是否无偏。

## 限制与保留意见

- $\tau\downarrow0$ 的分布极限不保证梯度数值良好；
- finite-temperature pathwise gradient 针对松弛目标，不自动等于原离散目标梯度；
- straight-through 反向规则一般不是前向离散函数的真实导数；
- pathwise 与 score-function 的方差排序依赖目标和控制变量；
- 文章同时给出 score-function/REINFORCE 入口；“pathwise 常有较低方差”保留为常见经验，不写成对所有目标的方差支配定理。

## 已生成与后续调用

- [x] [[常用离散分布]]：Categorical、Gumbel–Softmax 与梯度边界；
- [x] [[常用连续分布与指数族]]：Gaussian reparameterization；
- [x] [[多元高斯分布]]：$\mu+L\varepsilon$；
- [ ] [[Monte Carlo、重要性采样与方差缩减]]：梯度估计器方差与控制变量。

## 交叉验证

- Kingma & Welling, *Auto-Encoding Variational Bayes*；
- Rezende et al., *Stochastic Backpropagation*；
- Jang et al., *Categorical Reparameterization with Gumbel-Softmax*；
- Maddison et al., *The Concrete Distribution*。
