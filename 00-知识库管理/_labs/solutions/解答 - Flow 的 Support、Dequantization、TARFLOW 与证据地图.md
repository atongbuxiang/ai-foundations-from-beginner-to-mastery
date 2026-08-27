---
type: solution
status: draft
topic: "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"
exercise: "[[习题 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Flow 的 Support、Dequantization、TARFLOW 与证据地图
## A. 识别与复述
### GEN40-A01
$P_\theta(x)=\int_{[0,1)^d}p_c(x+u)du$（按选定量化 bin/缩放调整）。这是 probability mass；单点 $p_c(x)$ 只是 density。
### GEN40-A02
Uniform：$\log P(x)\ge E_{U\sim Unif}\log p_c(x+U)$。Variational：$\log P(x)\ge E_{q(u\mid x)}[\log p_c(x+u)-\log q(u\mid x)]$。
### GEN40-A03
Core 是 autoregressive invertible density model；Gaussian augmentation 把训练对象变成 noisy density；post-denoise 把 noisy sample 映向 clean estimate；guidance 再改变条件/无条件组合与部署分布。后两者不必保留 core tractable density。
## B. 手算与建模
### GEN40-B01
$P(0)=\int_0^1 2y,dy=1$；$p_c(1/2)=1$，此例数值碰巧相等，但一个是无单位 mass、一个是 density。换点 $p_c(1/4)=1/2$ 即不同，故不能由巧合等同对象。
### GEN40-B02
$\operatorname{bpd}=-\log_2P/d=-(-4)/2=2$ bits/dim。
### GEN40-B03
Integrand $\log(3u^2)-\log(2u)=\log(3/2)+\log u$。在 $q=2u$ 下 $E_q\log u=\int_0^1 2u\log u,du=-1/2$，故 bound 为 $\log(3/2)-1/2$。
## C. 推导与证明
### GEN40-C01
单位 bin 上 $P(x)=E_U[p_c(x+U)]$。$\log$ 凹，故 $\log E[p]\ge E\log p$。若 bin 体积不是 1，uniform density/尺度常数需保留。
### GEN40-C02
$P=\int p_c(x+u)du=E_q[p_c(x+u)/q(u\mid x)]$，要求 $q$ 支持覆盖积分区域且在需要处为正。对正随机变量用 Jensen，得期望的 log ratio 下界。
### GEN40-C03
任意 $x$ 有唯一 $z=f(x)$。Full-support density 给 $p_Z(z)>0$，diffeomorphism 给 $|\det J_f(x)|>0$，所以 $p_X(x)>0$。连续正密度进一步给每个开邻域正质量。
## D. 边界、反例与纠错
### GEN40-D01
模型可能因背景平滑/低层统计给某些语义异常图高 density；likelihood 是全像素 mass，不是人类语义函数。质量与 coverage 还可沿不同方向变化，需独立 evaluator/人工与受控样本审计。
### GEN40-D02
若 $Y\sim p_{core}$，输出 $X=D(Y)$ 的分布是 $D_\#p_{core}$。除非 $D$ 可逆且补计 Jacobian，不能用 $p_{core}(X)$ 当其 density；Tweedie 型 deterministic denoise 一般不是 core flow 的一层已计双射。
### GEN40-D03
TARFlow 的 inverse/sample direction 有 autoregressive patch dependency，可能需序列长度级 Transformer calls。`one-step` 只表示没有扩散时间网格，不能消除 serial critical path。
## E. AI 迁移
### GEN40-E01
统一位深/缩放、bin 定义、uniform/variational q、logit transform及 Jacobian、数据 split、dimension count、bound vs exact mass、importance samples、augmentation、ensemble、dtype 和 error bars；再对齐参数/FLOPs/wall time。
### GEN40-E02
至少四臂：clean/core（若合法）、Gaussian augmented core、+denoise、+guidance；另扫 noise/guidance。每臂记录训练目标分布、部署 pushforward、NLL/bpd 是否仍可算、quality、coverage、conditional accuracy、network calls、latency；保持模型/预算/seed 对齐。
### GEN40-E03
把 TARFlow 的同行评审方法与当时实验列为 2025 已建立证据；STARFlow 作为 2025 后续工作，iTARFlow 作为 2026 当前预印本，各自只记录自己直接支持的主张、设置和状态。后作结果不能修改前作原始 claim，只能建立“后来扩展/修正”的有向链接。

