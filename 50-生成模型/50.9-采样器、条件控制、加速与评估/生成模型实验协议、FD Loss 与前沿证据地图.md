---
type: synthesis
status: verified
area: [generative-models, evaluation, experimental-design, frechet-loss, evidence]
node_id: GEN-72
prerequisites: ["[[Likelihood、FID、KID、Precision–Recall 与人类评估]]", "[[扩散蒸馏、一致性模型与 Shortcut]]", "[[平均速度、MeanFlow 与有限步生成]]"]
related: ["[[采样器、条件控制、加速与评估 MOC]]", "[[生成模型完整课程地图与掌握标准]]"]
sources: ["[[S-2026-Su-11738-FD-Loss]]", "[[S-2026-Yang-Representation-Frechet-Loss]]", "[[S-2022-Parmar-CleanFID]]", "[[S-2017-Heusel-FID]]", "[[S-2018-Binkowski-KID]]"]
exercises: ["[[习题 - 生成模型实验协议、FD Loss 与前沿证据地图]]"]
solutions: ["[[解答 - 生成模型实验协议、FD Loss 与前沿证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-fd-loss-protocol-evidence-map-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 生成模型实验协议、FD Loss 与前沿证据地图

> [!abstract] 一句话结论
> 一个评价指标一旦变成训练损失，就不再是被动尺子，而是优化器会主动利用的目标。FD Loss 的可导性来自均值、协方差和矩阵平方根都可微；难点是大 population moments、秩亏、流式梯度和 representation dependence。可靠实验必须把训练表示、选择表示、最终评价与人评隔离，并预先声明比较预算和否证标准。

## 一、从评价到训练发生了什么

评价阶段：给定固定生成器 $G_\theta$，估计

$$M(\theta)=D(\phi_\#p_{data},\phi_\#p_\theta).$$

训练阶段：直接优化

$$\min_\theta M(\theta).$$

这会产生 Goodhart 风险：当 $M$ 成为目标，模型会寻找任何能改善 encoder-space statistics 的路径，而这些路径未必改善未被 $\phi$ 表示的人类关心维度。

因此必须区分：

- $\phi_{train}$：FD Loss 的 encoder；
- $\phi_{select}$：选超参/checkpoint 的 encoder/metric；
- $\phi_{test}$：只在最终冻结后使用的 held-out encoders；
- human/task evaluation：独立外部效标。

若四者相同，test score 已被反复优化，不再是干净验证。

## 二、FD Loss 的 population 对象

真实/生成 representation

$$z_r=\phi(x_r),\qquad z_g=\phi(G_\theta(\xi)).$$

定义 population moments

$$
\mu_r=\mathbb E[z_r],
\quad \Sigma_r=\mathbb E[(z_r-\mu_r)(z_r-\mu_r)^\top],
$$

$$
\mu_g(\theta)=\mathbb E[z_g],
\quad \Sigma_g(\theta)=\mathbb E[(z_g-\mu_g)(z_g-\mu_g)^\top].
$$

FD objective

$$
\mathcal F(\theta)
=\|\mu_r-\mu_g\|^2
+\operatorname{tr}\left[
\Sigma_r+\Sigma_g
-2(\Sigma_r^{1/2}\Sigma_g\Sigma_r^{1/2})^{1/2}
\right].
$$

它匹配 representation 的一二阶 moments；即使 $\mathcal F=0$，非 Gaussian feature distributions 仍可能不同。

## 三、矩阵梯度：哪里需要正定条件

均值梯度直接为

$$
\nabla_{\mu_g}\mathcal F=2(\mu_g-\mu_r).
$$

令

$$S=\Sigma_r^{1/2}\Sigma_g\Sigma_r^{1/2}.$$

若 $S\succ0$，利用

$$\nabla_S\operatorname{tr}(S^{1/2})=\frac12S^{-1/2},$$

链式法则给

$$
\boxed{
\nabla_{\Sigma_g}\mathcal F
=I-\Sigma_r^{1/2}S^{-1/2}\Sigma_r^{1/2}.
}
$$

当 empirical covariance 秩亏或特征值接近零时，$S^{-1/2}$ 不稳定。常见数值处理包括更大 population、$\epsilon I$ regularization、double precision/eigendecomposition 与 eigenvalue floor；每项都会改变实际 objective/gradient，必须记录。

## 四、为什么普通 gradient accumulation 不等于大 batch FD

一般 per-sample loss 满足

$$
\nabla\frac1B\sum_i\ell(x_i)=\frac1B\sum_i\nabla\ell(x_i),
$$

所以小 batch accumulation 可模拟大 batch。但 FD 是

$$
\mathcal F\left(\frac1B\sum_i z_i,
\frac1B\sum_i z_iz_i^\top-\mu\mu^\top\right),
$$

在平均 moments 后还有 nonlinear matrix square root。逐个小 batch 算 FD 再平均，通常不等于先合并 moments 再算一次 FD。

## 五、population 与 backward batch 解耦

[[S-2026-Su-11738-FD-Loss]] 解释一种核心思路：

1. 用许多小批前向累计/流式估计大 population 的 $\mu_g,V_g=\mathbb E[zz^\top]$；
2. 得到稳定的 global moment context；
3. 重放或用 stop-gradient context，使每个小批承担它对全局 moments 的正确局部梯度；
4. 累加梯度后更新模型。

抽象地，若 global moment $m=B^{-1}\sum_i m_i$，对当前 microbatch $i$ 构造

$$
\tilde m_i
=\operatorname{sg}\left(m-\frac{m_i}{B}\right)+\frac{m_i}{B},
$$

则 value 仍等于 global context，而梯度只流经 $m_i/B$。实际论文还可使用历史/EMA statistics 形成在线近似；这引入 staleness bias，必须与 exact replay 版本比较。

## 六、2026 Representation Fréchet Loss 的证据边界

[[S-2026-Yang-Representation-Frechet-Loss]] 报告：通过 decouple population size 与 gradient batch，可用不同 representation 的 FD 做 post-training，并把多步 generator 转为强一步模型；同时观察 Inception FID 可能误排现代 representation 下的视觉质量。

课程判断：

- `I`：FD 的矩阵公式、可微条件、moment decomposition；
- `A/E`：论文算法与报告的 ImageNet 结果；
- `H`：哪些 encoder 组合最能代表人类偏好、为何某模型改善；
- `O`：长期训练稳定性、跨域复现、adaptive metric gaming 与标准 benchmark 影响。

在更多独立复现前，不把 2026 数值写成通用基线常数。

## 七、metric gaming 的最小反例

设 encoder 只保留均值颜色和粗纹理，忽略文字拼写。生成器可以匹配这些 moments，使 FD 很低，却持续生成错误文字。又如只匹配一二阶 moments 的非 Gaussian mixture：两个分布可有相同均值协方差但 mode structure 完全不同。

所以至少需要：

- held-out encoder FD/KID；
- P/R 或 mode/attribute coverage；
- task-specific failure suites；
- blind human evaluation；
- memorization/copy audit。

## 八、可复现生成实验的预注册模板

### 8.1 Claim

写成可证伪句子，例如：“在固定 ImageNet split、模型参数量和 4 NFE 下，方法 A 的 CleanFID 与 recall 的 Pareto 不劣于 B。”不要写“效果更好”。

### 8.2 Objects

- data distribution/split；
- conditioning distribution；
- model output parameterization；
- sampler/solver 与 guidance；
- evaluator representations。

### 8.3 Budget

- training FLOPs/steps/data exposures；
- distillation teacher cost 是否计入；
- inference NFE、classifier/JVP/VJP；
- wall-time hardware、batch、precision；
- hyperparameter search budget。

### 8.4 Randomization

- seeds 与 paired initial noises；
- prompt ordering；
- checkpoint selection；
- evaluator bootstraps；
- human left/right randomization。

### 8.5 Primary and falsifying metrics

预先指定 primary metric 与最小 effect size；同时指定会否定结论的 coverage、conditionality、latency 或 human metric。禁止看到结果后只保留有利指标。

### 8.6 Missingness and failures

记录 NaN、OOM、solver failure、content filter rejection、invalid images 和人工剔除；不能静默丢掉失败样本。

## 九、50.9 前沿证据地图

| 主张 | identity/theory | 原始实验 | 最小复现 | 开放问题 |
|---|---|---|---|---|
| classifier guidance 是 conditional score | Bayes identity | ImageNet guidance scale | 1D Gaussian tilt | classifier gradient robustness |
| CFG 两支差是 evidence direction | exact-score identity | quality/diversity sweep | paired score vectors | large-scale extrapolation law |
| DPS 近似 posterior | posterior score decomposition | inverse benchmarks | linear Gaussian exact vs plug-in | calibration under misspecification |
| 高阶 solver 少 NFE | numerical order under assumptions | DPM-Solver benchmarks | linear/nonlinear ODE convergence | model-error-dominated regime |
| consistency/Shortcut 一步生成 | trajectory/composition identities | image generation | toy flow composition | off-trajectory/general interval |
| MeanFlow 学 average velocity | integral/JVP identity | 1-NFE ImageNet | affine/exponential flow | target self-dependence/stability |
| FD 可作 loss | matrix differentiability | 2026 post-training | moment-gradient finite difference | encoder gaming/cross-domain |

## 十、审计工作流

1. 写 claim 与对象合同；
2. 冻结 split、budget、primary/falsifying metrics；
3. 在 toy oracle 上验证公式和梯度；
4. 小规模检查数值稳定、NFE 与 logging；
5. 执行完整训练/采样，不改 test protocol；
6. 报 point estimate、CI、failures 与 negative results；
7. 用 held-out evaluator 与人评复核；
8. 发布 config、hash、environment、seeds 与原始 summary statistics。

## 十一、图：当尺子变成损失

先回答：训练 encoder、选择 encoder 与 test encoder 为什么要分开？global moments 怎样跨 microbatches 传递 value 而只让局部梯度回流？

![[00-知识库管理/_assets/figures/generative-models/fig-fd-loss-protocol-evidence-map-v1.svg|900]]

> [!figure] 图 50.9-08　FD Loss 的流式梯度与证据隔离
> 图左展示 population moments—microbatch backward，右展示 train/select/test/human 四层隔离与证据标签。来源：据 2026 Representation Fréchet Loss、科学空间 11738 与本节实验协议独立绘制。

**怎样读图**：先看 moment statistics 是跨样本对象，再沿 stop-gradient 查看哪条路径传 value/gradient；最后检查 evaluator 是否真正 held out。

**图没有证明什么**：图不证明 FD Loss 无偏、不证明 EMA statistics 等于当前 population，也不证明多表示 FD 消除了 metric gaming 或人类价值冲突。

## 十二、学习出口

- 能推 FD 对 $\mu_g,\Sigma_g$ 的梯度及正定条件；
- 能解释普通 gradient accumulation 为何失效；
- 能设计 train/select/test evaluator 隔离；
- 能把 GEN-65—72 的 claim 放进 I/A/E/H/O 证据层；
- [[习题 - 生成模型实验协议、FD Loss 与前沿证据地图]]
- [[解答 - 生成模型实验协议、FD Loss 与前沿证据地图]]
