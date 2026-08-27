---
type: solution
status: verified
area: [training, optimization, gradient-clipping, estimator-bias]
topic: "[[全局逐层梯度裁剪、AGC 与裁剪偏差]]"
exercise: "[[习题 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 全局逐层梯度裁剪、AGC 与裁剪偏差

> [!warning] 使用边界
> 裁剪能限制某个被定义对象的范数；它不自动保证梯度估计无偏、optimizer state 安全或最终泛化改善。

## A. 识别与复述

### TRN37-A01
global norm clipping 用一个因子 $a=\min(1,\tau/\|g\|)$ 乘完整梯度，保持该次全局方向；layerwise clipping 对每层用不同 $a_\ell$，改变层间比例；value clipping 对各坐标截断到 $[-\tau,\tau]$，通常改变向量方向。AGC 对 unit $i$ 约束 $\|g_i\|\le\lambda\max(\|w_i\|,\epsilon)$，不同 unit 的尺度不同，既依赖参数半径也依赖 unit 轴定义。

### TRN37-A02
clipping 是非线性投影，故一般不能穿过求和/平均号。`clip(mean)` 对应 microbatch/worker 梯度完成 accumulation 与 all-reduce 后再裁剪；`mean(clip)` 对应样本、microbatch 或各 worker 先裁剪再聚合。二者既可能大小不同，也可能方向不同。

### TRN37-A03
阈值与被裁对象同单位。mean 改 sum 会按 batch/token 缩放梯度；batch 和 accumulation 改变噪声与聚合位置；Adam/Muon 的 raw gradient 与预条件方向尺度不同；AGC 又把阈值绑定到 parameter norm。故“1”只有在完整 reduction、scope、order 和 dtype 合同下才有含义。

## B. 手算与构造

### TRN37-B01
$\|g\|_2=5$，缩放率为 $a=2/5=0.4$，故
$$
g_{clip}=(1.2,1.6)^T.
$$
因它是正标量倍数，方向余弦为 1。这里“保持方向”只针对整个向量的一次 global projection。

### TRN37-B02
拼接后的 global norm 是 $\sqrt{10^2+1^2}=\sqrt{101}$，共同缩放率 $5/\sqrt{101}\approx0.4975$。两层范数变为约 $4.975$ 与 $0.4975$，比值仍为 10。逐层裁剪则第一层乘 $0.5$ 得 $(3,4)$，第二层不变 $(0.6,0.8)$；层范数为 5 与 1，比值改成 5。逐层方法改变了模型级方向。

### TRN37-B03
裁剪前
$$
E[G]=0.1\cdot10+0.9(-1)=0.1>0.
$$
阈值 1 后，10 变 1、$-1$ 不变：
$$
E[C_1(G)]=0.1(1)+0.9(-1)=-0.8<0.
$$
稀有大正事件的幅度被截去，常见负事件不变，期望方向因此反转。

## C. 推导与证明

### TRN37-C01
投影问题
$$
\min_{z:\|z\|_2\le\tau}\frac12\|z-g\|_2^2
$$
在 $\|g\|\le\tau$ 时解为 $g$。否则 KKT 给 $z-g+\mu z=0$，所以 $z=g/(1+\mu)$；活跃约束 $\|z\|=\tau$ 给 $z=\tau g/\|g\|$。因此 global clipping 恰是 Euclidean projection，并对固定非零 $g$ 保持共线。

### TRN37-C02
标量 clip $C_\tau(g)=\operatorname{sign}(g)\min(|g|,\tau)$，偏差为
$$
b=E[(\tau\operatorname{sign}G-G)\mathbf1\{|G|>\tau\}].
$$
若 $P(|G|>\tau)=0$，充分有 $b=0$。也可能超阈尾部正负贡献恰好抵消，例如关于 0 对称的分布有 $E[G]=E[C_\tau(G)]=0$；因此“不触发”充分但非必要。

### TRN37-C03
取 $g_1=(10,0),g_2=(0,2)$，阈值 1。先平均得 $(5,1)$，再裁为
$$
\frac{(5,1)}{\sqrt{26}}\approx(0.9806,0.1961).
$$
先各自裁为 $(1,0),(0,1)$，再平均得 $(0.5,0.5)$。前者斜率 0.2，后者斜率 1，方向和范数均不同。

## D. 边界、反例与纠错

### TRN37-D01
若 attention logits 在 forward 已溢出，loss 与 gradient 为 NaN；norm 也是 NaN，后续 clipping 无法恢复有限方向。另一个反例是每步 clipped gradient 有界但在高曲率方向持续振荡，参数仍可不收敛。裁剪只给局部范数上界，不给整个闭环稳定性证明。

### TRN37-D02
clip-before-momentum 把裁剪后的梯度写入 $m_t$；momentum-before-clip 先把极端梯度写入 $m_t$，再只限制当步输出。即使人为调阈值让当步 $\Delta\theta$ 相同，第二种状态仍记住极端事件，未来无极端梯度时也会产生不同方向。顺序必须进 checkpoint/算法版本。

### TRN37-D03
0% 可能表示阈值宽松且训练健康，也可能表示裁剪代码没有作用到正确对象；适度触发可能正好抑制罕见 outlier；接近 100% 表示 optimizer 长期运行在归一化/饱和机制下，阈值已重定义有效算法。好坏需结合 scale quantile、方向、loss 和失败率，而非单调判断。

## E. AI 迁移

### TRN37-E01
manifest 应含 `loss reduction, per-sample/microbatch input, accumulation count, all-reduce sum/mean, clip location, global/group/layer/unit axis, norm type, threshold schedule, AGC epsilon, unscale order, momentum/Adam state order, dtype, overflow behavior, sharding ownership`。分布式复现还要断言不同 world size 下聚合对象一致。

### TRN37-E02
固定 seed、数据、LR/WD、token/FLOP 与调参次数；三法各在等预算阈值网格内选择。逐 step/层记录触发率、缩放率分位数、clip 前后 cosine、raw/update RMS、moments、overflow/skip；最终报告训练失败分母和验证/测试。用同一 telemetry 检查机制预测，而非只比较终点。

### TRN37-E03
需要证明：收益不是删掉发散 run 后的幸存者偏差；阈值搜索预算相同；中介上确有 outlier/update 限制；随机偏差没有破坏目标方向到不可接受程度；多 seeds 和失败率支持稳定性结论。最终只能写在给定模型、数据、optimizer、预算和裁剪位置内的经验增益。

## 无提示重做

- [ ] 48 小时后手算方向反转例。
- [ ] 一周后从分布式配置还原 clip(mean) 或 mean(clip)。
