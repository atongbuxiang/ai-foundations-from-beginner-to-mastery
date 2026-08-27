---
type: solution
status: draft
topic: "[[DDIM、非 Markov 前向族与确定性采样]]"
exercise: "[[习题 - DDIM、非 Markov 前向族与确定性采样]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - DDIM、非 Markov 前向族与确定性采样
## A. 识别与复述
### GEN46-A01
一组单时刻 marginals 只规定每个时间切片的 law，不规定 $(x_1,ldots,x_T)|x_0$ 的 temporal coupling。Simplified training 抽 $x_0,t,\epsilon$ 并形成单个 $x_t=a_tx_0+\sigma_t\epsilon$；它未同时观察 $x_s,x_t$，因此不识别唯一 joint path。
### GEN46-A02
$\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\hat\epsilon_t)/\sqrt{\bar\alpha_t}$，再 $x_s=\sqrt{\bar\alpha_s}\hat x_0+\sqrt{1-\bar\alpha_s-\sigma_{t\to s}^2}\hat\epsilon_t+\sigma_{t\to s}z$。常用 $\sigma_{t\to s}=\eta\sqrt{(1-\bar\alpha_s)/(1-\bar\alpha_t)}\sqrt{1-\bar\alpha_t/\bar\alpha_s}$；$\eta$ 控制新注入噪声。
### GEN46-A03
确定性条件于 $x_T$、网络参数、conditioner/condition、time grid、数值实现及所有预后处理。它不推出不同 $x_T$ 输出相同、不需要 NFE、可以 exact inversion、保持 DDPM path law，或在 imperfect denoiser 下 exact sampling。
## B. 手算与建模
### GEN46-B01
$\hat x_0=(1-0.8(-0.5))/0.6=7/3$。$\eta=0$ 时 $x_s=0.8(7/3)+0.6(-0.5)=47/30\approx1.5667$。
### GEN46-B02
$\sigma=0.5\sqrt{0.2/0.5}\sqrt{1-0.5/0.8}=0.5\sqrt{0.4}\sqrt{0.375}=\sqrt{0.15}/2\approx0.19365$。噪声方向系数为 $\sqrt{0.2-0.0375}=\sqrt{0.1625}\approx0.40311$，根号内为正。
### GEN46-B03
NFE 由 1000 降至 50，网络调用数约降低 20 倍。它不计每步 scheduler/decoder 开销、batch size 与硬件利用率、conditioner/CFG 的额外调用、I/O 和 evaluator；wall-time speedup 未必正好 20 倍。
## C. 推导与证明
### GEN46-C01
对每个固定 $t$，只要 $\epsilon_t\sim N(0,I)$，线性变换就给 $x_t|x_0\sim N(a_tx_0,\sigma_t^2I)$。让所有 $\epsilon_t$ 相同、彼此独立或具有任意合法相关矩阵，都保留每个单变量标准正态 marginal，却改变 $\operatorname{Cov}(x_s,x_t|x_0)=\sigma_s\sigma_t\operatorname{Cov}(\epsilon_s,\epsilon_t)$，故 joint path 不同。
### GEN46-C02
基步：给定 $x_T$ 后已确定当前状态。归纳步：若 $x_t$ 确定，固定网络/condition 得 $\hat\epsilon_t$，继而 $\hat x_0$ 确定；$\eta=0$ 删除新随机变量，固定公式唯一给出 $x_s$。沿有限 time grid 归纳，所有状态确定。
### GEN46-C03
取 $s=t-1,\eta=1$：$\sigma^2=[(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)](1-\bar\alpha_t/\bar\alpha_{t-1})$。第二因子 $=(\bar\alpha_{t-1}-\bar\alpha_t)/\bar\alpha_{t-1}=1-\alpha_t=\beta_t$，故 $\sigma^2=\beta_t(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)=\tilde\beta_t$。
## D. 边界、反例与纠错
### GEN46-D01
确定性是条件于初始 $x_T$。从不同 $x_T\sim N(0,I)$ 出发仍可产生不同输出，正如 deterministic function $f(z)$ 可以把随机输入推成丰富分布。只有固定同一 latent 时路径才重复。
### GEN46-D02
训练监督单时刻 denoising field，不直接监督从 $t$ 到远处 $s$ 的 transition composition。大跳用一次局部预测近似更长演化；network error、time interpolation 与 discretization error 都可能积累，训练覆盖端点不等于任意步长 exact。
### GEN46-D03
正文例中未 clip 时 $\hat x_0=7/3$、$x_s=47/30$；若 clip 到 1，则 $x_s=0.8-0.3=0.5$。输出改变量超过 1，说明 clipping 改变 sampler vector field/transition law，不只是防 NaN。
## E. AI 迁移
### GEN46-E01
复用同一 checkpoint、preprocessing、初始 noise bank、condition、evaluator 和硬件；交叉 $\eta$、time-grid 生成法与 10/20/50/100/1000 NFE。报告 paired quality、coverage、likelihood proxy、wall time、memory、failure rate 与多 seed confidence interval；同时记录 clipping/thresholding。
### GEN46-E02
先固定编码/反演的 time grid、网络和数值规则，从真实 $x_0$ 得 latent，再 reverse reconstruction；分别报告 latent repeatability、pixel/perceptual cycle error、语义保持与对微扰敏感性。程序 deterministic 只是一项；exact inverse 要求 forward/reverse 组合误差趋近机器精度或有定理支持。
### GEN46-E03
建立显式映射 `math_t = code_i + 1` 或使用 dummy index；断言首末累计量、$\bar\alpha_t=\prod_{s\le t}\alpha_s$、训练 gather 和 sample loop 使用同一 mapping、posterior 读取前一累计量、subsequence 严格单调并含端点、$t=1$ mask 正确。用小表手算逐项比对。
