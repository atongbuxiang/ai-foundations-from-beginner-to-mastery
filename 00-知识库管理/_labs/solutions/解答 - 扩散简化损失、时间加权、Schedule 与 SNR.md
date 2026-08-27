---
type: solution
status: draft
topic: "[[扩散简化损失、时间加权、Schedule 与 SNR]]"
exercise: "[[习题 - 扩散简化损失、时间加权、Schedule 与 SNR]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 扩散简化损失、时间加权、Schedule 与 SNR
## A. 识别与复述
### GEN44-A01
$w_t^{VLB}=\beta_t^2/[2\sigma_{rev,t}^2\alpha_t(1-\bar\alpha_t)]$。其中 $\sigma_{rev,t}^2$ 是 model reverse variance；取 $\beta_t$、$\tilde\beta_t$ 或 learned variance 会改变权重/额外项。
### GEN44-A02
$E_{t\sim Unif,x_0,\epsilon}\|\epsilon-\epsilon_\theta(x_t,t)\|^2$。它是 denoising regression，并与 DDPM/score 目标相关；但删改 VLB 权重且不含全部 terminal/reconstruction/variance 项，数值不是负 ELBO。
### GEN44-A03
$\pi_t$ 定义 population objective 各时刻重要性；$r_t$ 定义 Monte Carlo 抽哪个时刻。用 $\pi_t/r_t$ correction 可换 proposal 而保持 estimand；不 correction 就改目标。
## B. 手算与建模
### GEN44-B01
$c^*=10w_2/(w_1+w_2)$；$(1,1)$ 得 5，$(9,1)$ 得 1。
### GEN44-B02
$0.8$ 时 SNR $=4$、log-SNR $=\log4$；$0.2$ 时 SNR $=0.25$、log-SNR $=-\log4$。
### GEN44-B03
weights 为 $0.8/0.5=1.6$ 与 $0.2/0.5=0.4$。
## C. 推导与证明
### GEN44-C01
$E_{t\sim r}[\pi_t\ell_t/r_t]=\sum_tr_t(\pi_t/r_t)E[\ell_t|t]=\sum_t\pi_tE[\ell_t|t]$，要求所有 $\pi_t>0$ 处 $r_t>0$。
### GEN44-C02
若函数可为每个 $t,x_t$ 独立取值且权重严格正，逐条件平方损失都由 conditional mean 最小化，权重不改该函数。共享参数/容量/regularization 让不同 $t$ 竞争，同一参数的加权 compromise 会随权重变。
### GEN44-C03
给离散累计值，$\alpha_t=\bar\alpha_t/\bar\alpha_{t-1}$，再 $\beta_t=1-\alpha_t$。若 clip $\beta_t$，实际累计乘积不再严格等于未 clip 的 analytic curve，须以最终 table 为准。
## D. 边界、反例与纠错
### GEN44-D01
在精确 full-batch SGD 中常数缩放可配 learning rate；但 Adam moments、weight decay、gradient clipping、loss scaling、overflow/underflow、early-stop threshold 与多 loss 相对权重不同比例不变。因此实现中需声明 reduction。
### GEN44-D02
Cosine 是特定模型/数据上的设计与经验改进；最优性需定义 objective、data spectrum、steps 和 solver。换分辨率、参数化或采样预算可能改变比较。
### GEN44-D03
实际优化变为 $\sum_tr_tE\ell_t$（或含其他错误 weight），高 proposal 时刻被过度强调；梯度估计对原目标有偏，即使 sampling variance 看起来更低。
## E. AI 迁移
### GEN44-E01
至少交叉 linear/cosine schedule、epsilon/x0/v head、VLB/simple/SNR weight；统一参数、t proposal/importance、optimizer、训练 compute 和 sampler，报告 log-SNR 分箱 error、NLL bound、quality/coverage、NFE，多 seed 分析 interaction。
### GEN44-E02
记录每时刻 loss second moment 的在线 estimator、warmup/floor、更新滞后、proposal entropy、importance weight extrema/effective sample size、gradient variance和 unbiasedness test；防止少数时刻概率塌缩。
### GEN44-E03
核对数据归一化和每维 variance、像素相关长度/分辨率、同一 noise 是否按像素独立、architecture receptive field、log-SNR coverage 和 sampling NFE；同名 schedule 的名义 SNR 未必对应相同任务难度。

