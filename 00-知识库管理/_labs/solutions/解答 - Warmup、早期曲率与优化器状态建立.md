---
type: solution
status: verified
area: [training, optimization, warmup, stability]
topic: "[[Warmup、早期曲率与优化器状态建立]]"
exercise: "[[习题 - Warmup、早期曲率与优化器状态建立]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Warmup、早期曲率与优化器状态建立

> [!warning] 使用边界
> Warmup 是控制输入，不是单一机制的证据。下面每个解释都要用中介遥测和干预区分。

## A. 识别与复述

### TRN34-A01
一种完整写法是：对成功 optimizer update 计数 $k=0,\ldots,W$，
$$
\eta_k=\eta_{start}+\frac{k}{W}(\eta_{peak}-\eta_{start}),
$$
并声明第一个参数更新用 $k=0$ 还是 $k=1$、到达 peak 的 step 是否属于 warmup。还要给 $\eta_{start},\eta_{peak},W$、离散 endpoint、clock（attempt/success/token）和 overflow 时是否推进。只说“2000 steps”缺起终值和时钟，无法复现。

### TRN34-A02
六类机制与区分量：早期曲率看 top Hessian/HVP 与 $g^Tu$；optimizer state 看 $m,v$ 与 bias-corrected direction；相对/角/feature 更新看对应 ratio；早期噪声看 gradient covariance/noise scale；数值范围看 overflow、loss scale、非有限值位置；架构放大看 residual/attention/logit/activation scale。每项最好再有只针对该中介的干预。

### TRN34-A03
减少 early LR 在 $u_t$ 形成后缩小 $\Delta\theta_t$；bias correction 或 state priming 改变 $u_t=U(g,s)$ 本身；mixed-precision overflow 可能在 backward、unscale 或 reduction 中、尚未乘 LR 前发生。三者在因果链上的位置不同，互相不能自动替代。

## B. 手算与构造

### TRN34-B01
采用第 1—5 个成功 update 为 $0.01,0.02,0.03,0.04,0.05$ 的约定。稳定开区间为
$$
0<\eta<2/50=0.04.
$$
前三步严格稳定，第 4 步在边界（系数 $-1$，不收敛），第 5 步不稳定。无 warmup 直接用 $0.05$ 从首步起不稳定。此题也说明 warmup 长度 5 并不保证 peak 本身安全。

### TRN34-B02
第一步未校正 $m_1=0.2,v_1=0.04$，故 $m_1/\sqrt{v_1}=1$；校正后 $\hat m_1=2,\hat v_1=4$，比值仍为 1。第二步 $m_2=0.38,v_2=0.0796$，未校正比值约 $1.347$；校正后
$$
\hat m_2=0.38/(1-0.9^2)=2,
\quad
\hat v_2=0.0796/(1-0.99^2)=4,
$$
比值为 1。bias correction 修正状态初始化偏差；warmup 另外缩小外部 LR，不能视为同一操作。

### TRN34-B03
100 次尝试中的成功 update 期望为 $100(1-0.2)=80$。attempt-step schedule 已到 peak，optimizer 却平均只更新 80 次；success-step clock 此时只走到 warmup 的 80%。随机波动还会让不同 worker/run 的实际相位分叉，故必须保存成功计数器。

## C. 推导与证明

### TRN34-C01
一维时变二次步为 $\theta_{t+1}=(1-\eta_t\lambda_t)\theta_t$。逐步收缩的充分条件是
$$
0<\eta_t\lambda_t<2\quad\text{对所有 }t.
$$
若已知早期上界 $\lambda_t\le\bar\lambda_t$，linear warmup 满足 $\eta_t<2/\bar\lambda_t$ 即可。真实深网的局部曲率未知、方向非纯 SGD、曲率随轨迹改变，所以预热曲线本身不是稳定证明。

### TRN34-C02
从 $v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,v_0=0$ 递推得
$$
v_t=(1-\beta_2)\sum_{k=1}^t\beta_2^{t-k}g_k^2.
$$
若 $g_k=g$，则 $v_t=(1-\beta_2^t)g^2$，除以 $1-\beta_2^t$ 得 $g^2$。若早期 $g_k^2$ 特别大或分布快速变化，校正只消除零初始化的确定性因子，不能删除带权历史，状态仍滞后。

### TRN34-C03
若 $\|u_t\|\le U$，并暂用不显著变化的初始半径 $R_0$ 作分母，则
$$
\frac{\|\theta_W-\theta_0\|}{R_0}
\le\frac{U}{R_0}\sum_{t=1}^W\eta_t.
$$
对 $\eta_t=t\eta_{peak}/W$，和为 $\eta_{peak}(W+1)/2$。它约束累计相对位移；而二次稳定条件约束每一步的曲率乘积。一个可小而另一个可大，二者不能混同。

## D. 边界、反例与纠错

### TRN34-D01
例如 logits 在 FP16 中先溢出为 Inf，softmax 产生 NaN，backward 梯度已非有限；随后即使乘 $η=0$，IEEE 算术中的 $0\times\mathrm{NaN}$ 仍是 NaN。因果链是 activation overflow → nonfinite loss/gradient → LR intervention 太晚。应修数值内核、dtype、loss scaling 或归一化。

### TRN34-D02
替代机制一：Adam moments 尚未建立，warmup 只是限制早期预条件方向；可用 state priming 或不同 $\beta$ 干预。替代机制二：小权重导致 relative/angular update 过大；可调初始化尺度或 layer scale。若这些干预复制 warmup 收益而 Hessian telemetry 不随之变化，就不能把证据唯一归给“早期更尖”。

### TRN34-D03
同时改总步数会改变数据/compute；改 peak LR 会把 warmup 与主训练强度混在一起；改 decay 起点会改变整条面积和 final LR。观测差是多个处理的联合效应，不能识别 warmup 的单独主效应。应使用相同 peak、总 horizon、post-warmup 路径和预算，或用因子设计显式估计交互。

## E. AI 迁移

### TRN34-E01
矩阵可写六行：`curvature→top HVP→降低 early LR/曲率平滑→稳定界扩大`；`state→m/v transient→state priming/β change→方向尖峰消失`；`relative step→angular/feature ratio→改初始化/layer scale`；`noise→gradient covariance→改 batch 保持 step`；`numeric→overflow site→升 dtype/动态 loss scale`；`architecture→residual/logit scale→改 norm/residual scale`。每行预先写与预测相反时的拒绝条件。

### TRN34-E02
三组都固定 token、数据顺序、目标 peak 与成功更新预算。attempt clock 在 overflow 时仍推进；success clock 不推进；token clock 按有效 token 推进。报告 wall time、attempt/success/update、tokens、overflow 与 scheduler phase；主比较按同 token/FLOP，另做同 wall-time 敏感性分析。

### TRN34-E03
先定位非有限值最早出现位置，再核对 loss scale/unscale；随后按层看 raw grad 与 clip-before/after，确认 spike 是裁剪输入还是输出；再看 $m,v$、update RMS、relative/angular/feature step；最后用 HVP/架构尺度形成机制候选。只在提高/降低 LR 的配对干预同时移动预测中介时，才把“LR 过大”作为受限结论。

## 无提示重做

- [ ] 48 小时后重建六机制矩阵。
- [ ] 一周后从 overflow 日志判断 scheduler clock 是否分叉。
