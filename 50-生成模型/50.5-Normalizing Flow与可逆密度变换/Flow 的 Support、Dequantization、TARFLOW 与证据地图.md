---
type: concept
status: verified
area: [generative-models, normalizing-flows, evaluation]
node_id: GEN-40
prerequisites: ["[[变量替换、基分布与 Exact Likelihood Flow]]", "[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]", "[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]"]
related: ["[[自回归模型的表达、成本、失效模式与证据地图]]", "[[EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"]
sources: ["[[S-2019-Ho-FlowPlusPlus]]", "[[S-2025-Su-10667-TARFLOW]]", "[[S-2025-Zhai-TARFlow]]", "[[S-2015-Theis-Generative-Evaluation]]"]
exercises: ["[[习题 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
solutions: ["[[解答 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-support-dequantization-evidence-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Flow 的 Support、Dequantization、TARFLOW 与证据地图

> [!abstract] 一句话结论
> Flow 的 exact density 仍受 support/topology、离散数据口径与部署后处理约束。对量化图像，continuous density 必须在每个 quantization bin 上积分才得到 pmf；dequantization 训练的是这个离散 log-mass 的下界。TARFlow 说明强架构能显著推进 flow，但其 Gaussian augmentation、post-denoise 和 guidance 必须与 core likelihood 分账。

## 一、support：双射能搬运什么

设 base $p_Z(z)>0$ 对所有 $z\in\mathbb R^d$ 成立，$g$ 是 $\mathbb R^d$ 上 diffeomorphism。则

$$p_X(x)=p_Z(f(x))|\det J_f(x)|>0$$

也对所有 $x$ 成立。模型可以在某些区域给极小但非零 density，却不能产生真正零密度空洞。

此外 homeomorphism 保持连通性等拓扑性质；低维 manifold 上的奇异数据分布也没有相对于 $d$ 维 Lebesgue measure 的普通 density。有限噪声、增广维度、surjective/stochastic flows 或 mixture 可缓解，但它们改变了经典同维 diffeomorphism 合同。

> [!warning] “数据流形”要精确
> 有限样本看起来落在曲面附近，不足以证明真实分布严格支持在零测度流形上。实际传感器噪声可能使分布 full-dimensional。拓扑限制是条件结论，不是对所有图像数据的直接事实判断。

## 二、离散像素不能直接代入 continuous density

设离散 $x\in\{0,1,\ldots,255\}^d$，把每个离散值对应连续 bin $x+[0,1)^d$。continuous model $p_c$ 所诱导的离散质量是

$$
\boxed{P_\theta(x)=\int_{[0,1)^d}p_c(x+u)du.}
$$

$p_c(x)$ 是带单位的 density 值，不是 $P_\theta(x)$；前者还会随坐标尺度改变。

## 三、uniform dequantization 的 Jensen 下界

取 $U\sim\operatorname{Unif}([0,1)^d)$，令 $Y=x+U$。因为 bin 体积为 1，

$$P_\theta(x)=\mathbb E_U[p_c(x+U)].$$

由 $\log$ 的凹性，

$$
\boxed{\log P_\theta(x)
=\log\mathbb E_U[p_c(x+U)]
\ge \mathbb E_U[\log p_c(x+U)].}
$$

训练随机加 uniform noise 并最大化 continuous log-density，最大化的是离散 log-mass 的 lower bound。它不是“把离散数据无损变连续”。

## 四、variational dequantization

更一般地取条件密度 $q_\phi(u\mid x)$ 支持在 $[0,1)^d$：

$$
P_\theta(x)=
\mathbb E_{q_\phi}\left[
\frac{p_c(x+u)}{q_\phi(u\mid x)}
\right].
$$

再用 Jensen：

$$
\boxed{\log P_\theta(x)\ge
\mathbb E_{q_\phi(u\mid x)}
[\log p_c(x+u)-\log q_\phi(u\mid x)].}
$$

第二项不是可选装饰；它校正 learned noise density。若 $q$ 是单位立方体上的 uniform，$\log q=0$，退化为上一式。[[S-2019-Ho-FlowPlusPlus]]用此思想改善 dequantization。

## 五、bits/dim 的口径

常报告

$$\operatorname{bpd}(x)=-\frac{\log_2 P_\theta(x)}{d}.$$

实际可能报告 dequantization lower bound 对应的 upper estimate。比较前必须统一：像素位深、缩放、uniform/variational noise、logit transform 及其 Jacobian、颜色空间、数据 split 和是否 ensemble。小数点后的优势若小于 estimator/implementation 差异，不能当作模型家族定论。

## 六、likelihood 与语义为什么可以分离

Likelihood 按像素空间概率质量评价，可能强烈响应背景、局部平滑度和低层统计；人类质量更关心语义结构。高 likelihood 不保证：

- OOD 样本获得低 density；
- 典型集位置与单点高 density 一致；
- samples 覆盖所有语义模式；
- latent 线性方向具有可解释因果语义。

因此评价至少并列 likelihood/bpd、质量、coverage、条件一致性和 compute，且说明 evaluator 的训练域。

## 七、TARFlow 的四组件证据账

[[S-2025-Zhai-TARFlow]]的 core 是 patch-level Transformer autoregressive flow，并交替序列方向。强生成结果还组合：

1. **Gaussian augmentation**：训练 noisy continuous density，缓和离散/流形问题；
2. **post-training denoise**：用 noisy-density score/Tweedie 型更新得到更干净输出；
3. **guidance**：改变条件/无条件分数或预测组合，移动部署分布；
4. **autoregressive inversion**：生成方向仍有串行 Transformer 调用。

因此应至少报告四个分布：clean data、augmented training target、core flow samples、denoised/guided deployment samples。后两种后处理输出不必保留 core flow 的 tractable likelihood。

[[S-2025-Su-10667-TARFLOW]]提供了这套组合的中文推导入口，并明确提醒串行 inverse。课程把“flow 满血归来？”保留为研究问题，不改写成普遍家族胜负。

## 八、前沿时间线与证据等级

- **TARFlow（ICML 2025）**：已同行评审方法及其指定 benchmark 结果；
- **STARFlow（2025）**：把 autoregressive flow 推向 scalable/high-resolution 路线的后续预印本；
- **iTARFlow（2026）**：当前后续预印本，进一步针对 inverse/效率问题；截至本笔记日期，其新主张应按预印本证据处理。

时间更新不改变基本审计：数据口径、参数/compute matching、后处理分布、latency 与 evaluator 必须同时对齐。后续工作不能回写成 TARFlow 原论文已经证明的结论。

## 九、图：从 exact density 到部署样本隔着哪些门

先看图回答：哪一步建立离散 pmf 下界，哪两步会让最终样本不再直接对应 core flow likelihood？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-support-dequantization-evidence-v1.svg|900]]

> [!figure] 图 50.5-08　Support、dequantization 与 TARFlow 部署分布的证据账
> 左侧从离散 bin mass 到 dequantization lower bound，中间列 classical flow support 门，右侧拆开 core TARFlow、denoise 与 guidance。来源：据 Flow++、TARFlow 与变量替换公式独立绘制。

**怎样读图**：先沿离散 $x\to y=x+u$ 看训练目标的 lower-bound 关系，再沿部署链看每次后处理究竟作用于哪个分布。箭头“改善样本”不是 likelihood 等号。

**图没有证明什么**：图不证明真实图像严格位于低维流形，不证明 TARFlow 普遍优于 diffusion，也不证明 denoise/guidance 在所有条件和预算下改善质量—覆盖折中。

## 十、课程结论与研究清单

面对任何新 flow 论文，至少问：

1. base/data 的维度、support 和 preprocessing 是什么？
2. density 是 exact、bound 还是随机/数值估计？
3. 哪个方向串行，wall time 和硬件如何？
4. training target 与 deployment output 是否同一分布？
5. likelihood、quality、coverage 和 compute 是否共同报告？
6. 结论是 identity、theorem、指定实验、解释性假说还是开放问题？

- [[习题 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]
- [[解答 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]
