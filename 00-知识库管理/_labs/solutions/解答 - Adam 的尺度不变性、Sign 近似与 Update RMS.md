---
type: solution
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"
exercise: "[[习题 - Adam 的尺度不变性、Sign 近似与 Update RMS]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Adam 的尺度不变性、Sign 近似与 Update RMS

> [!warning] 使用边界
> 一条漂亮公式可能是恒等式、渐近近似或统计平均。必须保存量词和单位，不能只保存结论数字。

## A. 识别与复述

### TRN14-A01
若从开始到当前的每个坐标梯度都乘同一正数 $c$，初始化相应，得到 $m_t'=cm_t,v_t'=c^2v_t$；当 $\epsilon=0$ 时 $m_t'/\sqrt{v_t'}=m_t/\sqrt{v_t}$。这不覆盖 $c<0$、中途缩放、未变换旧 state、固定 epsilon 主导、clipping/decay 或任意坐标重参数化。

### TRN14-A02
若当前/局部一阶状态 $m_t\approx g_t$、二阶状态 $v_t\approx g_t^2$ 且 epsilon 可忽略，则 $u_t\approx g_t/|g_t|$。有 momentum 时 $m_t$ 是带符号历史平均，可能与当前 $g_t$ 异号；$v_t$ 也有不同时间尺度，因此不是无条件 current sign。

### TRN14-A03
Direction RMS 是 $\operatorname{RMS}(u_t)$，不含 LR；parameter-delta RMS 是 $\operatorname{RMS}(\eta_tu_t)$，单位是参数；AdamW 完整位移为 $-\eta_t(u_t+\lambda_t\theta_t)$（依合同），其 RMS 含交叉项，不能由两项 RMS 简单相加。

## B. 手算与构造

### TRN14-B01
$u=(2/2,-3/3)=(1,-1)$。缩放后 $m'=(14,-21),v'=(196,441)$，$u'=(14/14,-21/21)=(1,-1)$，验证 exact identity。

### TRN14-B02
$$\sqrt{\frac{0.1}{1.9}}=\sqrt{0.0526316}\approx0.2294.$$
这是低 SNR、稳态和 mean-field 分母近似下的 direction RMS，不含 LR 或 decay。

### TRN14-B03
$\beta_1=0$ 得 1；$0.9$ 得 0.2294；$0.99$ 得 $\sqrt{0.01/1.99}\approx0.0709$。较长一阶平均压低零均值噪声的 RMS；这不代表信号响应或优化速度按同一比例变化。

## C. 推导与证明

### TRN14-C01
独立零均值使交叉协方差为零：
$$\operatorname{Var}(m_t)=(1-\beta_1)^2\sigma^2\sum_{k=0}^{\infty}\beta_1^{2k}
=\sigma^2\frac{(1-\beta_1)^2}{1-\beta_1^2}
=\sigma^2\frac{1-\beta_1}{1+\beta_1}.$$

### TRN14-C02
若高维/mean-field 允许把随机 denominator 近似为 $\sqrt{\mathbb E v}=\sigma$，则 $u\approx m/\sigma$，所以
$$\operatorname{RMS}(u)\approx\sqrt{\mathbb E m^2/\sigma^2}=\sqrt{\frac{1-\beta_1}{1+\beta_1}}.$$
条件包括零均值或低 SNR、平稳二阶矩、弱时间相关、稳态、epsilon 可忽略，以及用 ratio-of-expectations/集中性替换随机比值。

### TRN14-C03
$\theta=a\phi$ 时 $\nabla_\phi L=a\nabla_\theta L$。即使 normalized direction 在两坐标中数值相同，$\Delta\theta=a\Delta\phi$；若两边使用同一 LR，则物理参数位移相差 $a$。要保持同一 $\theta$ 轨迹还需变换 LR、decay 和 state。故梯度缩放身份不是参数化不变性。

## D. 边界、反例与纠错

### TRN14-D01
令上一时刻 $m_{t-1}=-10$，$\beta_1=0.9$，当前 $g_t=1$，则 $m_t=-9+0.1=-8.9<0$。Adam direction 仍向负号，而 current sign 为正；历史一阶矩不能省略。

### TRN14-D02
在分母被替换为稳定常数 $\sigma$ 的近似里，$\beta_2$ 的波动作用被平均掉，所以公式不显含它。有限维、非平稳、重尾、epsilon 区和瞬态中，$v_t$ 的方差、响应速度及与 $m_t$ 的相关性都依赖 $\beta_2$。

### TRN14-D03
若 direction RMS 为 0.23，参数 delta RMS 还要乘 group-specific $\eta_t$；若 $\eta=10^{-4}$，仅 task delta 约 $2.3\times10^{-5}$。再加 AdamW decay、不同参数组和 clipping 后 full delta 又不同，且单位从无量纲变为参数单位。

## E. AI 迁移

### TRN14-E01
可定义：①`direction_rms = RMS(mhat/(sqrt(vhat)+eps))`，无 LR/decay；②`task_delta_rms = RMS(eta * direction)`，参数单位；③`relative_full_delta = RMS(delta_total)/(RMS(theta)+delta_floor)`，无量纲。按参数组与层分别求元素 RMS，再报告分位数，避免把大小悬殊的张量简单平均。

### TRN14-E02
固定 seed 生成 $g_t=\mu+\xi_t$；扫 $\beta_1$、$\mu/\sigma$、维度和 AR(1) 相关系数，运行足够 burn-in；比较实测 $\sqrt{\mathbb E u^2}$ 与理论线，报告 Monte Carlo 误差。再扫 $\beta_2,\epsilon$ 作为失效诊断，而不是预先假设它们无关。

### TRN14-E03
先写 exact 层：从递推可逐步证明的恒等式；再写 approximation 层：平稳、独立、低 SNR、集中性、忽略 epsilon 等；最后写 diagnostics：SNR、$\epsilon/\sqrt v$、state stationarity、维度、相关时间、实测 RMS 与残差。这样博客线索可以进入课程，但不会冒充无条件定理。

## 无提示重做

- [ ] 48 小时后从 EMA 方差推导 0.2294。
- [ ] 一周后解释为何梯度缩放身份不等于重参数化不变性。
