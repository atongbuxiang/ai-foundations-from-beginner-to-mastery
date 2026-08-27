---
type: solution
status: draft
topic: "[[最小 DDPM 的张量合同、复现门与证据地图]]"
exercise: "[[习题 - 最小 DDPM 的张量合同、复现门与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 最小 DDPM 的张量合同、复现门与证据地图
## A. 识别与复述
### GEN48-A01
六类接口是：数据尺度/离散化与增强；schedule 数值和索引；closed-form forward sample；network time condition、输出 target 与 loss reduction；reverse mean/variance、clipping、EMA 与最后一步；likelihood/quality/coverage、NFE、wall time 和 evaluator 版本。
### GEN48-A02
应 gather 为 `[B,1,1,1]`，再通过 broadcasting 作用到 `[B,C,H,W]`。每个 batch sample 有自己的 $t$，但同一 sample 的所有通道/空间位置共享该 scalar schedule coefficient；直接保持 `[B]` 可能与尾轴错误对齐。
### GEN48-A03
$t=1$ 的理想 posterior variance 边界为零，继续加噪会污染最终 $x_0$ estimate。离散图像 likelihood 常另有 decoder/reconstruction term，因此“无 reverse process noise”不等于没有 observation model；必须显式声明 decoder/dequantization。
## B. 手算与建模
### GEN48-B01
$\alpha_2=\bar\alpha_2/\bar\alpha_1=0.72/0.9=0.8$，$\beta_2=0.2$。若 off-by-one 取 index 1，会把 $\bar\alpha_1=0.9$ 当作当前累计量，而不是 0.72。
### GEN48-B02
gather 值为 $(0.95,0.6)$，reshape 后 tensor shape `[2,1,1,1]`；第一样本所有 feature 乘 0.95，第二样本乘 0.6。
### GEN48-B03
$t=1$ mask 为 0，输出 $2+0\cdot0.1\cdot5=2$；$t=2$ mask 为 1，输出 $3+0.2\cdot5=4$。若漏 mask，第一项会误成 2.5。
## C. 推导与证明
### GEN48-C01
$\alpha_t=1-\beta_t$，$\bar\alpha_0=1$，$\bar\alpha_t=\bar\alpha_{t-1}\alpha_t$，再取两个平方根。断言包括 $0<\alpha_t\le1$、$0<\bar\alpha_t\le\bar\alpha_{t-1}$、$\bar\alpha_t=\prod_{s=1}^t\alpha_s$、两平方系数之和为 1、所有值 finite，且由累计比值能恢复原 $\alpha_t$。
### GEN48-C02
令 $a^2+\sigma^2=1$，$x_t=ax_0+\sigma\epsilon$，$v=a\epsilon-\sigma x_0$。换算 $x_0'=ax_t-\sigma v=(a^2+\sigma^2)x_0=x_0$，$\epsilon'=\sigma x_t+av=(a^2+\sigma^2)\epsilon=\epsilon$。单测对随机 shapes/timesteps 检查三种任意起点的换算与 round-trip 在 dtype tolerance 内，并覆盖 $a$ 或 $\sigma$ 接近零的端点。
### GEN48-C03
$x_{t-1}=\mu_\theta+\mathbf1[t>1]\sigma_tz$。当 $t=1$，indicator 恒为零，故对任意新 $z,z'$ 输出都为同一 $\mu_\theta$。但 $\mu_\theta$ 的输入 $x_1$ 由先前随机 $x_T$ 和各步 noise 产生，所以最终样本仍可随机。
## D. 边界、反例与纠错
### GEN48-D01
确定性 bug 也可稳定复现：例如 schedule 全错一位、最后一步固定加入同一 seeded noise，重复运行仍完全一致。Seed 只审计随机程序可重复性；正确性需手算、分布 moment、round-trip 与独立实现交叉验证。
### GEN48-D02
Simple MSE 删除/改变 ELBO 的 timestep weights，且不含 terminal KL、decoder/reconstruction、learned variance 项与离散数据口径。它是有效 denoising regression objective，但其数值不能直接解释为 nats 或 bits/dim。
### GEN48-D03
U-Net 只定义函数族。若 training 使用错 $\bar\alpha_t$、网络输出 epsilon 而 sampler 当作 $x_0$、或 reverse variance/last-step 错误，再标准的 U-Net 也执行错误随机过程；概率和张量合同独立于 architecture 品牌。
## E. AI 迁移
### GEN48-E01
代数门：累计表、posterior 和参数化 round-trip；统计门：closed marginal Monte Carlo moments 与 last-step mask；过拟合门：单样本/极小集 loss 显著下降；分布门：toy Gaussian/mixture 的 mean、variance、mode coverage；成本门：train step、NFE、wall time、memory；证据门：公式—代码行—输出 artifact—来源卡可追踪。
### GEN48-E02
Manifest 至少保存数据版本/切分、scaling/augment、schedule 生成与最终数组 hash、数学—代码索引映射、architecture/time embedding、parameterization/weight/proposal/reduction、optimizer/precision/clipping/EMA、seed 与 checkpoint hash、sampler/variance/grid/clipping、batch/hardware/software版本，以及 evaluator model/version/sample count。
### GEN48-E03
固定同一 checkpoint、网络调用实现、preprocessing、condition、initial-noise bank、sample count、decoder 和 evaluator；只改变 reverse scheduler/time grid。报告实际 NFE（含 CFG 双调用）、wall time 和 memory，并配对比较相同 latent 的结果；不同训练 checkpoint 或评价器的对比不能归因于 sampler。
