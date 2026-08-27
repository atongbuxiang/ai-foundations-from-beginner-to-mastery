---
type: concept
status: verified
area: [generative-models, autoregressive, sequence-learning]
aliases: [Teacher Forcing与Exposure Bias, 生成时前缀漂移]
node_id: GEN-05
prerequisites: ["[[概率链式分解、顺序选择与自回归生成]]", "[[数据生成分布与采样假设]]"]
related: ["[[生成建模对象、似然与自回归 MOC]]", "[[祖先采样、温度、截断与自回归解码分布]]", "[[Transformer Decoder 与自回归因果结构]]"]
sources: ["[[S-2020-Su-7259-Exposure-Bias]]", "[[S-2015-Huszar-Scheduled-Sampling批判]]"]
exercises: ["[[习题 - Teacher Forcing、暴露偏差与生成时分布漂移]]"]
solutions: ["[[解答 - Teacher Forcing、暴露偏差与生成时分布漂移]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gen-teacher-rollout-shift-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Teacher Forcing、暴露偏差与生成时分布漂移

> [!abstract] 本节主问题
> Teacher Forcing 在真实前缀下最大化每一步条件似然；自由生成则在模型自己诱导的前缀下继续预测。两种前缀分布一般不同，这就是可精确定义的 train–rollout shift。它不等于“MLE 在理想条件下不一致”，而常见 Scheduled Sampling 也不因输入更像推理就自动成为一致估计器。

## 一、先把“老师强制”写成概率期望

对真实序列 $X_{1:T}\sim P_*$，Teacher Forcing 的总体风险为

$$
R_{\mathrm{TF}}(\theta)
=\sum_{t=1}^T
\mathbb E_{X_{<t}\sim P_*}
\mathbb E_{X_t\sim P_*(\cdot\mid X_{<t})}
[-\log p_\theta(X_t\mid X_{<t})].
$$

训练时第 $t$ 步读到真实 $X_{<t}$。这不是额外近似，而正是联合 MLE 的 chain-rule 展开：

$$
R_{\mathrm{TF}}(\theta)=\mathbb E_{P_*}[-\log p_\theta(X_{1:T})].
$$

因此在模型可实现、无限数据、全局优化等理想条件下，$P_\theta=P_*$ 是正确总体最优；不能说 Teacher Forcing 本身使 MLE 统计不一致。

## 二、自由生成使用另一个前缀分布

给解码规则 $\phi$，实际单步核记为 $q_{\theta,\phi}(x_t\mid x_{<t})$。rollout joint 为

$$
Q_{\theta,\phi}(x_{1:T})
=\prod_{t=1}^Tq_{\theta,\phi}(x_t\mid x_{<t}).
$$

第 $t$ 步的前缀分布是它的边缘 $Q_{\theta,\phi}^{<t}$，而非 $P_*^{<t}$。若想评价模型在自身前缀上的一步损失，会得到

$$
R_{\mathrm{roll}}(\theta;\phi)
=\sum_t\mathbb E_{H_t\sim Q_{\theta,\phi}^{<t}}
\mathbb E_{X_t\sim P_*(\cdot\mid H_t)}
[-\log p_\theta(X_t\mid H_t)],
$$

但对 $P_*$ 从未产生或极少产生的 $H_t$，$P_*(\cdot\mid H_t)$ 可能没有足够监督甚至只在几乎处处意义下定义。这正是 off-distribution recovery 难题。

## 三、最小例子：一步小错怎样改变后续输入

真实序列只可能是 $00$ 或 $11$，各概率 $1/2$。所以

$$
P_*(X_2=X_1)=1.
$$

假设模型第一步以 0.49/0.51 产生 0/1，第二步在真实前缀 0、1 下都学得完美。Teacher-forced 第二步 loss 为 0；rollout joint 仍因第一步边缘有 0.01 偏差而与真实 joint 不同，但不会进一步放大。

现在再假设模型在训练从未覆盖的特殊前缀 $\bot$ 上会进入重复循环；如果解码器、噪声或前一步错误可能产生 $\bot$，则 TF risk 完全看不到它。两种现象要分开：

- 正常可达前缀上的条件误差；
- 数据支持之外前缀上的恢复行为。

## 四、误差积累能说到什么程度

若对**所有可达前缀**都有条件核总变差误差

$$
\operatorname{TV}\bigl(P_*(\cdot\mid h),P_\theta(\cdot\mid h)\bigr)\le\varepsilon,
$$

可逐步最大耦合，并用 union bound 得到长度 $T$ joint 的粗界

$$
\operatorname{TV}(P_*,P_\theta)\le T\varepsilon.
$$

若界只在 $H_t\sim P_*^{<t}$ 的平均意义成立，就不能直接控制模型偏离数据支持后的条件。反过来，$T\varepsilon$ 是上界，不代表误差必然线性爆炸；有些动力具有恢复/收缩性。

> [!warning] “Exposure Bias 导致误差指数增长”不是无条件定理
> 增长率取决于条件核对前缀扰动的稳定性、任务 loss、解码规则和是否有吸收/恢复状态。必须给具体递推或敏感性假设。

## 五、Scheduled Sampling 改变了什么

Scheduled Sampling 以一定概率把真实前缀 token 替换为模型 token，再继续预测真实 target。直觉是让训练输入接近 rollout；但 estimator 的 joint pair 已改变。

以两步序列为例，若第二步前缀完全从模型边缘 $Q_\theta(x_1)$ 采，而 target $x_2$ 仍来自数据样本，则训练 pair 接近

$$
Q_\theta(x_1)P_*(x_2),
$$

而不是 $P_*(x_1,x_2)$。此时最优 $p_\theta(x_2\mid x_1)$ 可能趋向边缘 $P_*(x_2)$，丢失真实依赖。[[S-2015-Huszar-Scheduled-Sampling批判]]用此类结构说明它一般不是 proper、consistent 的 joint estimator。

这不证明 scheduled sampling 在任何有限 benchmark 都无效；它说明经验收益与概率估计正确性是两本证据账。

## 六、缓解策略应按“改哪本账”分类

| 方法 | 改变 | 主要风险 |
|---|---|---|
| Scheduled sampling / token replacement | 训练前缀分布与 estimator | objective inconsistency、不可微采样 |
| Sequence-level risk / RL | 目标改为 rollout task reward | 高方差、reward misspecification |
| Professor/adversarial forcing | 隐状态轨迹匹配 | game optimization、匹配对象不完备 |
| Data augmentation / perturbation | 扩展恢复前缀覆盖 | 扰动是否真实、强度选择 |
| Better decoding | 改 $Q_{\theta,\phi}$ | 不修复 $P_\theta$，可能损覆盖 |
| Calibration/regularization | 改条件概率或稳健性 | 与长序列风险关系需验证 |

因此问“是否解决 Exposure Bias”过于粗糙；应问在什么前缀分布、目标、指标和预算下改善了什么。

## 七、与 shift、mask 和并行训练的边界

Teacher Forcing 的实现需右移 input 并用 causal mask；未右移而允许 diagonal 会泄漏 target，这属于程序错误，不是 exposure bias。训练位置并行只是一次计算所有真实前缀 conditional；不会让模型看到未来。具体张量合同复用[[Transformer Decoder 与自回归因果结构]]。

## 八、科学空间研读框

[[S-2020-Su-7259-Exposure-Bias]]用“老师铺好前路”的直觉解释真实前缀训练，并提出随机替换/对抗扰动，适合建立问题意识。本节保留文章的实验性定位，并与 [[S-2015-Huszar-Scheduled-Sampling批判]] 交叉：输入更像推理分布不推出 estimator 更接近真实 joint；缓解方法要同时审计统计目标、梯度估计和 rollout 指标。

## 九、图：两条前缀路径与一次目标改变

先看图回答：蓝色训练路径和红色 rollout 路径从哪一步开始可能分叉；Scheduled Sampling 又把哪两个来源错误地拼成了一个训练 pair？

![[00-知识库管理/_assets/figures/generative-models/fig-gen-teacher-rollout-shift-v1.svg|900]]

> [!figure] 图 50.1-05　Teacher Forcing、模型 rollout 与 Scheduled Sampling 的分布账
> 左栏展示真实前缀监督，中栏展示模型选择进入新前缀，右栏展示混合前缀与真实 target 可能破坏 joint dependency。来源：依据条件 MLE、科学空间 7259 与 Huszár 两步反例独立绘制。

**怎样读图**：逐步看 prefix 的来源标签；同一个 target loss 只有在 pair 确实来自所声明 joint 时才是该 joint 的 cross-entropy estimator。红色箭头表示分布来源改变，不表示误差必然增加。

**图没有证明什么**：图不证明 Scheduled Sampling 在所有任务上降低指标，也不证明 Teacher Forcing 的自由生成必然失败；它给出 estimator 审计与一个反例机制。

## 十、本节回顾

- Teacher Forcing 是自回归 joint MLE 的正确展开；
- rollout 前缀来自 $Q_{\theta,\phi}$，与训练前缀 $P_*$ 一般不同；
- 只在数据前缀上小的一步误差不足以控制所有偏离前缀；
- error compounding 需要稳定性/全前缀误差等条件，不能口号化；
- Scheduled Sampling 可改善经验任务，却一般改变总体 estimand，不自动一致。

## 十一、练习与独立详解

- [[习题 - Teacher Forcing、暴露偏差与生成时分布漂移]]
- [[解答 - Teacher Forcing、暴露偏差与生成时分布漂移]]
