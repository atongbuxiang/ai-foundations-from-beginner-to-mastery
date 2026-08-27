---
type: concept
status: verified
area: [generative-models, diffusion, training-objectives]
node_id: GEN-44
prerequisites: ["[[数据、噪声、速度与 Score 参数化]]", "[[DDPM 反向后验、ELBO 与逐步 KL]]"]
related: ["[[反向均值、固定方差、学习方差与 Analytic-DPM]]", "[[最小 DDPM 的张量合同、复现门与证据地图]]"]
sources: ["[[S-2020-Ho-DDPM]]", "[[S-2021-Nichol-Dhariwal-Improved-DDPM]]", "[[S-2021-Kingma-VDM]]"]
exercises: ["[[习题 - 扩散简化损失、时间加权、Schedule 与 SNR]]"]
solutions: ["[[解答 - 扩散简化损失、时间加权、Schedule 与 SNR]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddpm-loss-snr-schedule-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 扩散简化损失、时间加权、Schedule 与 SNR

> [!abstract] 一句话结论
> DDPM 的逐步 KL 在固定 reverse variance 下等于 timestep-dependent weighted denoising MSE 加常数；常用 simplified loss 改为更简单的 timestep sampling 与权重。若每个 $t$ 能独立达到 Bayes optimum，正权重不改最优函数；共享有限网络、mini-batch 与 optimizer 下，权重和 schedule 会改变梯度预算、方差和最终折中。

## 一、从逐步 KL 到 weighted noise MSE

对 $t\ge2$，teacher 与 model 都为 Gaussian。若 model variance 固定 $\sigma_{rev,t}^2I$，并用 noise parameterization，上一节给

$$
L_{t-1}=E\left[w_t^{VLB}
\|\epsilon-\epsilon_\theta(x_t,t)\|^2\right]+C_t,
$$

其中

$$
w_t^{VLB}=
\frac{\beta_t^2}{2\sigma_{rev,t}^2\alpha_t(1-\bar\alpha_t)}.
$$

若取 $\sigma_{rev,t}^2=\beta_t$ 或 $\tilde\beta_t$，权重不同。写“VLB weight”时必须同时声明 variance convention。

## 二、simplified objective 改了什么

经典简化形式是

$$
\boxed{L_{simple}=E_{t\sim Unif\{1,\ldots,T\},x_0,\epsilon}
\|\epsilon-\epsilon_\theta(x_t,t)\|^2.}
$$

它删除逐步 VLB 的显式 $w_t^{VLB}$，常带来更好的感知样本训练。严格说：

- 它仍是合法的 denoising regression objective；
- 它一般不等于负 ELBO，也不能直接当 bits/dim；
- 若每个 $t$ 的函数可独立任意选择，所有正权重有相同 conditional-mean optimum；
- 共享参数、容量有限、regularization/early stop 下，不同权重给不同 compromise。

## 三、timestep sampling 与 loss weighting 是一件事的两种实现

目标

$$L=\sum_{t=1}^T\pi_tE[\ell_t]$$

可从 proposal $r_t>0$ 采样并用 importance weight：

$$
L=E_{t\sim r}\left[\frac{\pi_t}{r_t}\ell_t\right].
$$

若忘记 $\pi_t/r_t$，estimand 已改变。选择 $r_t$ 可降 gradient variance；[[S-2021-Nichol-Dhariwal-Improved-DDPM]]研究 loss-second-moment 采样等方法。unbiased objective 与低方差 estimator 仍是两本账。

## 四、SNR 是 schedule 的共同语言

$$
\operatorname{SNR}_t=\frac{\bar\alpha_t}{1-\bar\alpha_t},
\qquad
\lambda_t=\log\operatorname{SNR}_t.
$$

高 SNR 时 data 容易恢复但 noise 是小 residual；低 SNR 时 data 信息稀少。schedule 决定训练在 log-SNR 轴上放了多少离散点，也决定 sampler 相邻状态的跨度。

若把 $x_0$ 从 $[-1,1]$ 改为标准差不同的尺度，名义 SNR 不再反映真实数据 variance；schedule 不能脱离 preprocessing 比较。

## 五、linear beta 与 cosine $\bar\alpha$

Linear beta 直接令 $\beta_t$ 线性增长，简单但在某些分辨率/步数下可能过早破坏 signal。Improved DDPM 的 cosine-style 累计 schedule 可写成

$$
\bar\alpha(t)=
\frac{\cos^2\left(\frac{t/T+s}{1+s}\frac\pi2\right)}
{\cos^2\left(\frac{s}{1+s}\frac\pi2\right)},
$$

再由 $\alpha_t=\bar\alpha_t/\bar\alpha_{t-1}$、$\beta_t=1-\alpha_t$ 得单步 schedule，并通常 clip $\beta_t$ 避免最后一步为 1。这个 clip 改变精确端点，必须记录。

## 六、参数化与权重必须联读

由 GEN-43，

$$\|\hat\epsilon-\epsilon\|^2
=\operatorname{SNR}_t\|\hat x_0-x_0\|^2.$$

因此 uniform-$t$ unweighted epsilon loss 等价于 SNR-weighted data error，而不是 unweighted data loss。选择 output head、显式 weight 和 timestep proposal 共同决定实际 gradient allocation；只比较“预测噪声还是数据”而不统一另两项，无法归因。

## 七、一个两时刻容量冲突例

假设共享 scalar parameter $c$ 同时拟合两时刻 target $m_1=0,m_2=10$：

$$L(c)=w_1(c-0)^2+w_2(c-10)^2.$$

最优

$$c^*=\frac{10w_2}{w_1+w_2}.$$

若 $(w_1,w_2)=(1,1)$，$c^*=5$；若 $(9,1)$，$c^*=1$。每个时刻单独的 Bayes target 没变，但共享有限模型的最优 compromise 改变。这是“正权重不改最优点”需要函数可按 $t$ 独立表达的最小反例。

## 八、数值与优化合同

- 记录 loss 是 per-element mean、per-sample sum 还是 batch sum；常数缩放在 exact gradient descent 可由 learning rate 吸收，但会影响 mixed precision、clipping、weight decay 和 optimizer states；
- 记录 timestep proposal、importance weight、P2/Min-SNR 类显式 weight（若使用）；
- 按 log-SNR bins 报告 loss/gradient norm，而非只报全局平均；
- schedule table 用高精度生成，检查 $0<\beta_t<1$、$\bar\alpha_t$ 单调和端点。

## 九、科学空间与来源边界

科学空间前几篇给出“噪声层难度不同”的直觉和实现经验；本节以[[S-2020-Ho-DDPM]]区分 VLB/simple objective，以[[S-2021-Nichol-Dhariwal-Improved-DDPM]]核对 cosine schedule、learned variance 和 timestep estimator，以[[S-2021-Kingma-VDM]]建立 log-SNR 语言。单个博客实验不决定普遍 schedule 优劣。

## 十、图：schedule 怎样通过 SNR 改变训练预算

先看图回答：改变 beta schedule、timestep sampling 和 explicit weight，分别作用在数据分布、估计器还是目标函数哪一层？

![[00-知识库管理/_assets/figures/generative-models/fig-ddpm-loss-snr-schedule-v1.svg|900]]

> [!figure] 图 50.6-04　Schedule→log-SNR→parameterization error→gradient budget
> 左侧是累计 signal/noise，中间区分 VLB/simple weight，右侧区分 timestep proposal 与 importance correction。来源：据 DDPM、Improved DDPM 与 VDM 独立绘制。

**怎样读图**：先由 schedule 得每个 $t$ 的 $a_t,\sigma_t$，再问输出参数化把误差怎样缩放，最后问 $t$ 如何抽样及是否 importance correction。三处都可改变看到的训练曲线。

**图没有证明什么**：图不证明 cosine 总优于 linear，不证明相同 Bayes optimum 给相同有限模型，也不证明降低 training MSE 必然改善 likelihood、FID 与 coverage。

## 十一、本节回顾与训练

- VLB noise loss 有由 variance convention 决定的 timestep weights；
- simplified loss 是改权后的 regression，不是逐项 ELBO；
- proposal 改变 estimator，漏 correction 会改变 objective；
- schedule、parameterization、weighting 必须联合比较；
- [[习题 - 扩散简化损失、时间加权、Schedule 与 SNR]]
- [[解答 - 扩散简化损失、时间加权、Schedule 与 SNR]]

