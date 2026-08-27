---
type: concept
status: verified
area: [generative-models, energy-based-models, score-based-models, evidence]
node_id: GEN-32
prerequisites: ["[[Predictor–Corrector 与 Score-based 生成程序]]", "[[GAN、分布差异与对抗训练 MOC]]"]
related: ["[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[生成模型 MOC]]"]
sources: ["[[S-2019-Su-6331-GAN分析与采样]]", "[[S-2019-Su-6612-生成模型等于能量模型]]", "[[S-2019-Su-7038-从去噪自编码器到生成模型]]", "[[S-2023-Su-9509-得分匹配与条件得分匹配]]"]
exercises: ["[[习题 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"]
solutions: ["[[解答 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ebm-score-gan-diffusion-interfaces-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# EBM、Score、GAN 与 Diffusion 的接口和证据地图

> [!abstract] 本节主问题
> EBM、score model、denoiser、GAN critic 与 diffusion network 都能输出“让样本往更真实方向移动”的信号，但其概率对象并不相同。本节把关系分为四级：定义恒等式、总体最优等价、算法接口和启发式类比；只有前两级能用等号，且必须带条件。

## 一、最可靠的恒等式：Energy 与 Score

若

$$
p_\theta(x)=Z_\theta^{-1}e^{-E_\theta(x)}
$$

是可微正密度，则

$$
\boxed{\nabla_x\log p_\theta(x)=-\nabla_xE_\theta(x).}
$$

这是同一个 density 的两种局部表示。反向则需注意：任意 learned vector field $s_\theta(x)$ 不一定是某个标量势的梯度。若 Jacobian 不对称、curl 非零，便不存在全局 $E$ 使 $s=-\nabla E$（在单连通光滑区域内）。Score-based sampling 可直接使用向量场，不必显式恢复 energy 或 $Z$。

## 二、Denoiser 与 Score：总体最优关系

Gaussian corruption 下，

$$
r^*(y,\sigma)=y+\sigma^2s_\sigma(y).
$$

这是 posterior-mean denoiser 与 noisy marginal score 的恒等式。有限网络的 $r_\phi$ 与 $s_\theta$ 若使用不同 parameterization、weighting 和 optimizer，不能只靠公式声称训练轨迹相同。

## 三、GAN critic 与 density ratio

原始 logistic GAN 在固定生成器、无限容量、population best response 下：

$$
D^*(x)=\frac{p_*(x)}{p_*(x)+p_g(x)},
$$

因此 logit

$$
\log\frac{D^*(x)}{1-D^*(x)}
=\log p_*(x)-\log p_g(x)
$$

是 log-density ratio。它不是单独的 $\log p_*(x)$；有限 critic、有限数据和未优化 best response 时更不能当 exact energy。把 $-\operatorname{logit}D$ 画成“能量地形”可以提供直觉，却不自动定义 normalized generative density。

## 四、Diffusion 是一族 time-indexed scores

Diffusion/score-based model 学习

$$
s_\theta(x,t)\approx\nabla_x\log p_t(x),
$$

其中 $p_t$ 是数据经指定 forward noising 后的 marginal family。它不是只学一个静态 $p_0$ energy；生成还需要路径、reverse dynamics 与 solver。Exact score family + exact dynamics 的结论不能直接外推到有限网络和有限 NFE。

## 五、训练与采样总表

| 家族 | 学习对象 | 是否需训练期 model sampling | 部署采样 | 主要 normalization |
|---|---|---:|---|---|
| MLE EBM | $E_\theta(x)$ | 通常需要模型相/MCMC | MCMC | $Z_\theta$ 难 |
| NCE EBM | unnormalized density + normalizer | 否，需 known noise | 仍需 sampler | 训练可估 $c$，采样未解决 |
| Score/DSM | $s_\theta(x,\sigma)$ | 否 | Langevin/reverse solver | score 消去 $Z$ |
| GAN | implicit $G_\theta$ + critic | generator 直接给 fake | 单次 forward | 通常无显式 density |
| Diffusion | time-indexed score/noise/clean target | 否 | 多步 reverse chain/ODE | 路径定义 marginal |

## 六、“生成模型 = 能量模型”的三种读法

1. **合法读法**：EBM 是生成模型家族，因为配备 sampler 后能生成；
2. **有条件接口**：某些 implicit generator/critic 训练可解释为近似 energy fitting + sampler learning；
3. **错误强读法**：任意 GAN/VAE/diffusion 都存在唯一、可算且训练等价的静态 energy。

科学空间系列最有价值的是第二种研究视角；课程必须防止它滑向第三种本体论等号。

## 七、证据等级地图

| Claim | 等级 | 需要什么才升级 |
|---|---|---|
| $s=-\nabla E$ | 定义恒等式 T | 正密度、可微、同一模型 |
| DSM 与 marginal score MSE 同 minimizer | 定理 T | Gaussian kernel、总体 $L^2$、可积性 |
| Langevin 的 Gibbs invariant law | 定理 T | 正则/边界/非爆炸；不含 mixing |
| replay buffer 使 neural EBM 可训练 | 实验 E | 指定论文协议与复现 |
| WGAN 成功主要来自 energy regularization | 假说 H | 受控消融与跨数据重复 |
| PC 优于所有同预算 solvers | 未支持 U | compute-matched 广泛实验/理论 |

## 八、一个陌生论文的审计顺序

遇到“我们的 critic/denoiser/score 是 energy”时，逐问：

1. 标量还是向量？关于 $x$ 还是 $\theta$ 求导？
2. 是否定义了基准测度、$Z$ 与合法 density？
3. 等号是逐点、总体最优、同 equilibrium，还是仅训练直觉？
4. sampler 的目标 invariant law 是谁？有限步输出是谁？
5. 有无 score integrability/curl 检查？
6. 评价是否同时覆盖质量、模式、likelihood 与 compute？

## 九、科学空间综合研读框

- [[S-2019-Su-6331-GAN分析与采样]]：energy density 与 implicit sampler 的互补；
- [[S-2019-Su-6612-生成模型等于能量模型]]：finite Langevin neural EBM 案例；
- [[S-2019-Su-7038-从去噪自编码器到生成模型]]：denoiser—score—sampler；
- [[S-2023-Su-9509-得分匹配与条件得分匹配]]：最优目标等价。

它们共同提供研究问题和中文推导桥；各自标题中的“=”必须映射到本节的证据等级。

## 十、图：四个家族怎样共享接口而不被抹平

先看图回答：图中哪些连线是数学等号，哪些只是把一个家族的输出交给另一个算法？

![[00-知识库管理/_assets/figures/generative-models/fig-ebm-score-gan-diffusion-interfaces-v1.svg|900]]

> [!figure] 图 50.4-08　EBM、Score、Denoiser、GAN 与 Diffusion 的关系分级
> 实线表示定义/定理，虚线表示算法接口，点线表示需实验检验的类比；右侧列出各自 sampler 与缺口。来源：依据本卷公式与来源证据独立绘制。

**怎样读图**：先认线型再读概念。Energy—score 和 Gaussian denoiser—score 有明确条件；critic—energy 与 generator—model phase 多为受限接口；diffusion 还多出 time-indexed path。

**图没有证明什么**：图不证明所有向量 score 可积分成 energy，不证明各家族训练/采样复杂度相同，也不支持用单一 FID 排出普遍优劣。

## 十一、本节回顾

- Energy—score 是同一可微 density 下的恒等式；
- denoiser—score 是 Gaussian corruption 下的 posterior-mean关系；
- optimal GAN logit 是 density ratio，不是单独数据 log-density；
- diffusion 学 time-indexed score family 与 reverse path；
- “等价”必须标注逐点、最优点、equilibrium、algorithm interface 或 hypothesis。

## 十二、练习与独立详解

- [[习题 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]
- [[解答 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]

