---
type: derivation
status: verified
area: [training, optimization, adam, scaling]
node_id: TRN-14
aliases: [Adam Scale Invariance, Adam Update RMS, Sign Adam]
prerequisites: ["[[Adam 的 Epsilon、数值稳定与实现分歧]]", "[[Adam 收敛反例、AMSGrad 与条件化保证]]", "[[期望、方差与矩]]"]
related: ["[[镜像下降、Bregman 几何与自然梯度]]", "[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Update-to-Weight Ratio、谱与尺度诊断]]"]
sources: ["[[S-2015-Kingma-Ba-Adam]]", "[[S-2025-Su-11267-Adam-Update-RMS]]", "[[S-2025-Su-11280-学习率与Batch-Size平均场]]", "[[S-2024-Su-10563-Adam-Epsilon-Scaling]]"]
exercises: ["[[习题 - Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
solutions: ["[[解答 - Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-adam-scale-sign-rms-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Adam 的尺度不变性、Sign 近似与 Update RMS

> [!abstract] 一句话结论
> 在 epsilon 为零且完整 gradient history 同步缩放时，Adam direction 对正的逐坐标梯度缩放不变；这不等于对任意参数重写或函数空间位移不变。Adam 只在特定时标/SNR regime 近似 sign update；Update RMS 的 0.2—0.3 现象可由平均场解释，但依赖 $\beta_1$、SNR、stationarity、epsilon 和 denominator concentration。

## 一、精确的 gradient-scale 恒等式

设一条完整梯度序列逐坐标乘正数 $c_i$：

$$g'_{t,i}=c_i g_{t,i},\qquad c_i>0.$$

若 $m_0=v_0=0$、betas 相同，逐步归纳得

$$
m'_{t,i}=c_i m_{t,i},
\qquad
v'_{t,i}=c_i^2v_{t,i}.
$$

bias correction 不改变缩放，因此 epsilon 为零时

$$
\boxed{
\frac{\widehat m'_{t,i}}{\sqrt{\widehat v'_{t,i}}}
=\frac{\widehat m_{t,i}}{\sqrt{\widehat v_{t,i}}}
}.
$$

若 $c_i<0$，方向相应翻转符号。这个 identity 解释了 loss 整体缩放或坐标 gradient 单位改变时的理想鲁棒性。

## 二、为什么这不等于“坐标无关”

令参数重写 $\theta=D\phi$。链式法则给

$$
g_\phi=D^\top g_\theta.
$$

即使 Adam 在 $\phi$ 坐标中把该 gradient magnitude 归一化，映回原参数的位移是

$$
\Delta\theta=D\Delta\phi,
$$

又多出一个 $D$。因此 gradient direction 的逐坐标缩放不变，不代表参数轨迹、函数变化或 generalization 对任意 reparameterization 不变。真正坐标不变的几何需要明确 metric transformation，例如 [[镜像下降、Bregman 几何与自然梯度]]；60.3 将进一步讨论 KL metric。

## 三、四个会打破理想恒等式的因素

1. **epsilon**：缩放后相对 epsilon 变成 $\epsilon/c_i$；
2. **中途切换**：已有 $m,v$ 未同步翻译；
3. **coupled L2**：gradient 中的 $\lambda\theta$ 不随 loss scaling 同比变化；
4. **clipping/quantization**：非线性处理不与任意尺度交换。

所以“Adam 不怕 loss scaling”必须附上算法状态与处理链条件。

## 四、何时近似 SignSGD

若某一时刻 $m_t\approx g_t$、$v_t\approx g_t^2$ 且 epsilon 很小，则

$$
u_t\approx\frac{g_t}{|g_t|}=\operatorname{sign}(g_t).
$$

这个近似在第一步 bias correction 后尤其直接，也可能在方向稳定、二阶状态快速跟踪时成立。但一般情况下

$$
m_t=(1-\beta_1)\sum_s\beta_1^{t-s}g_s,
\qquad
v_t=(1-\beta_2)\sum_s\beta_2^{t-s}g_s^2
$$

使用不同历史核；$m_t/\sqrt{v_t}$ 可以小于 1、接近 1，甚至因滞后短暂超过 1。Adam 不是逐步 clip 到 $[-1,1]$ 的算法。

## 五、Update RMS 是哪个量

定义未乘 LR、未加 decay 的 adaptive direction

$$
u_t=\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon},
$$

则

$$
\operatorname{RMS}(u_t)
=\sqrt{\frac1d\sum_{i=1}^d u_{t,i}^2}.
$$

参数实际位移若无其他控制是 $\operatorname{RMS}(\Delta\theta_t)=\eta_t\operatorname{RMS}(u_t)$；有 AdamW decay、clipping 或 parameter groups 时还要把对应项分开。日志里名为 `update_rms` 的量必须说明是否含 LR/decay。

## 六、低 SNR 稳态近似

[[S-2025-Su-11267-Adam-Update-RMS]]考虑单坐标平稳 i.i.d. gradient：

$$
\mathbb E[g]=\mu,
\qquad
\operatorname{Var}(g)=\sigma^2.
$$

在 $t\to\infty$、epsilon 可忽略时：

$$
\mathbb E[m_t^2]
=\mu^2+\frac{1-\beta_1}{1+\beta_1}\sigma^2,
\qquad
\mathbb E[v_t]=\mu^2+\sigma^2.
$$

采用平均场近似

$$
\mathbb E\!\left[\frac{m_t^2}{v_t}\right]
\approx
\frac{\mathbb E[m_t^2]}{\mathbb E[v_t]},
$$

并再对高维坐标平均，得到

$$
\operatorname{RMS}(u_t)^2
\approx
\frac{r+(1-\beta_1)/(1+\beta_1)}{r+1},
\qquad
r=\frac{\|\mu\|^2}{\|\sigma\|^2}.
$$

当低 SNR，$r\approx0$：

$$
\operatorname{RMS}(u_t)
\approx\sqrt{\frac{1-\beta_1}{1+\beta_1}}.
$$

$\beta_1=0.9$ 时为 $0.2294\ldots$，解释了特定大模型配方中约 0.2—0.3 的观察。

## 七、为什么公式里近似没有 beta2

稳态下 $\mathbb E[v_t]=\mathbb E[g^2]$ 与 $\beta_2$ 无关；平均场又把随机 denominator 替换成其期望，所以 $\beta_2$ 消失。但 exact ratio 的分布、$m_t$ 与 $v_t$ 相关性、denominator concentration 和非平稳 lag 都依赖 $\beta_2$。数值模拟通常在较大 $\beta_2$ 时更贴近近似，小 $\beta_2$ 时误差更明显。

因此“Update RMS 只由 $\beta_1$ 决定”是该近似 regime 内的结论，不是 Adam identity。

## 八、SNR 反推为什么只是诊断

形式上可从观测的 $q=\operatorname{RMS}(u_t)^2$ 解出

$$
r\approx\frac{q-(1-\beta_1)/(1+\beta_1)}{1-q}.
$$

但相同 Update RMS 可能来自非平稳均值、时间相关、重尾坐标、epsilon floor、clipping 或参数混合；只凭一个标量不能识别真实 gradient SNR。应用时应按层/参数组记录，并与直接跨 batch/跨 seed 估计对照。

## 九、图：identity、approximation 与 observable 分三层

先看图回答：哪条箭头是严格缩放恒等式，哪条只在低 SNR 平均场下成立，Update RMS 是否已经包含 LR？

![[00-知识库管理/_assets/figures/training-optimization/fig-adam-scale-sign-rms-v1.svg|900]]

> [!figure] 图 TRN-14　Adam 的尺度消去、sign 近似与 Update RMS 证据梯
> 左侧给出 $m\mapsto cm,v\mapsto c^2v$ 的 exact cancellation；中间列出 sign-like 成立条件和 epsilon 断点；右侧把 direction RMS、parameter delta RMS 与 mean-field estimate 分开。来源：据 [[S-2015-Kingma-Ba-Adam]] 与 [[S-2025-Su-11267-Adam-Update-RMS]] 独立绘制。

**怎样读图**：从左到右逐层降级 claim：identity 可代数证明，sign 是 regime approximation，0.229 是带分布假设的统计估计。

**图没有证明什么**：图不证明 Adam 对任意 reparameterization 不变，也不证明 0.2 是最佳 update RMS 或跨模型常数。

## 十、本节回顾

- gradient history 的正对角缩放在 epsilon=0 时被精确消去；
- 这不是一般 coordinate invariance；
- sign 近似依赖 numerator/denominator 时标和 epsilon；
- Update RMS 要分清是否含 LR/decay；
- 0.229 公式是低 SNR 稳态平均场近似，可实验反查但不可神化；
- 下一节 [[L2 正则、Coupled Decay 与 AdamW]]处理 decay 是否进入自适应状态。

## 练习与独立解答

- [[习题 - Adam 的尺度不变性、Sign 近似与 Update RMS]]
- [[解答 - Adam 的尺度不变性、Sign 近似与 Update RMS]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]
