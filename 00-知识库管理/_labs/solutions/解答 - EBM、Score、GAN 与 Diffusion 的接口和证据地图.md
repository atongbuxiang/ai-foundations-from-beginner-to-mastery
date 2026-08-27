---
type: solution
status: draft
topic: "[[EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"
exercise: "[[习题 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - EBM、Score、GAN 与 Diffusion 的接口和证据地图
## A. 识别与复述
### GEN32-A01
Energy—score：同一正、可微、可归一化 density，$s=-\nabla E$。Denoiser—score：Gaussian corruption、posterior mean/MSE 总体最优，$r^*=y+\sigma^2s_\sigma$。GAN：固定 $G$、population、无限/充分判别器 best response，$\operatorname{logit}D^*=\log p_* -\log p_g$。
### GEN32-A02
Forward noising 产生随 $t$ 变化的 $p_t$；reverse dynamics 在每个时刻需要 $\nabla\log p_t$。单一 $p_0$ score 不包含路径上的噪声 marginals、schedule 或 solver 信息。
### GEN32-A03
定义恒等式：EBM 的 $s=-\nabla E$；总体最优等价：DSM 与 marginal score MSE；算法接口：score 交给 Langevin sampler；经验类比：critic landscape 像“挖坑”。
## B. 手算与建模
### GEN32-B01
$\log p_*(x)-\log p_g(x)=-x^2/2+(x-1)^2/2=1/2-x$。它是线性 density ratio logit；$\log p_*(x)=-x^2/2-\frac12\log2\pi$，二者显然不同。
### GEN32-B02
$\partial_y s_1=-1$，$\partial_xs_2=1$，Jacobian 不对称，curl 为 2，不可能在单连通 $\mathbb R^2$ 上等于 $-\nabla E$。
### GEN32-B03
$s(x)=-x$；ULA 为 $x^+=(1-h)x+\sqrt{2h}\xi$，是相关多步 Markov transition。One-pass generator 是 $x=G(z)$ 一次 pushforward；除特殊构造外二者既无相同 transition 也无相同计算成本。
## C. 推导与证明
### GEN32-C01
$\log p=-E-\log Z$，对 $x$ 求梯度得 $s=-\nabla E$。$E+c$ 的 $x$-gradient 与 $E$ 相同，所以 score 也具有看不见 energy offset 的 gauge invariance。
### GEN32-C02
$D^*=p_*/(p_*+p_g)$，$1-D^*=p_g/(p_*+p_g)$，相除得 $D^*/(1-D^*)=p_*/p_g$，取 log 即结论。
### GEN32-C03
若 $s=-\nabla E$ 且 $E\in C^2$，则 $\partial_js_i=-\partial_{ji}E=-\partial_{ij}E=\partial_is_j$。在单连通域此 curl-free 条件也与存在势函数密切相关。有限点检查可能漏掉点间 curl、拓扑洞与测量/网络误差。
## D. 边界、反例与纠错
### GEN32-D01
旋转场 $(-y,x)$ 已是反例；即使可积，$e^{-E}$ 还可能不可积，如 $E=-x^2$。所以还需 integrability、基准测度和 normalizer。
### GEN32-D02
GAN 是二人 variational game，MLE EBM 含模型相，score model 做局部 field regression，diffusion 还含 time path。它们可共享局部直觉或接口，但 objective、gradient estimator 和 sampler 不同。
### GEN32-D03
FID 依赖 feature encoder，只测有限样本的均值/协方差近似，且受 sampler/temperature/NFE 影响；不能识别 likelihood、score MSE、mode coverage 或理论近似误差。需要受控多指标证据。
## E. AI 迁移
### GEN32-E01
逐条标注：数学等式、条件、population/finite class、sampler、实验协议、外推范围。特别检查“energy”是否有 density、critic 是否 best response、有限链是否 equilibrium、性能是否只是特定 benchmark。
### GEN32-E02
固定数据/preprocess、参数量区间、训练 FLOPs、采样 wall time/NFE、样本数和 evaluator；分别调优但预注册预算；报告 FID、precision/recall、mode toy、likelihood/score proxy、失败率、seeds 与内存。另给各家族特有误差诊断。
### GEN32-E03
6331 负责正负相与分析—采样桥；6612 负责 neural EBM/Langevin 工程案例；7038 负责 denoiser—score—生成桥；9509 负责 conditional/marginal score 投影。Hyvärinen、Vincent、NCE、NCSN、Roberts–Tweedie、Du–Mordatch、Song SDE 分别补定义、定理、原算法、实验协议和有限步边界。

