---
type: solution
status: draft
area: [generative-models, likelihood, image-generation]
topic: "[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]"
exercise: "[[习题 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - 离散似然、连续似然、Dequantization 与 Bits-per-dim

## A. 识别与复述

### GEN06-A01
离散 mass 是 $P(X=x)$；连续 point density 是相对参考测度的局部概率率，可大于 1 且有单位；bin probability 是 $\int_{B_x}p(y)dy$。只有最后者能对应被量化为 $x$ 的连续区域概率。

### GEN06-A02
Uniform dequantization 优化

$$
E_{U\sim Unif}\log p_\theta(x+U)\le\log P_\theta(x),
$$

是离散 log mass 下界。若模型 density 在该 unit bin 几乎处处为常数，Jensen 取等；一般不是 exact discrete likelihood。

### GEN06-A03
$\mathrm{BPD}=-\log P(x)/(D\log2)$（若 numerator 用自然对数）。$D$ 通常包含每个 channel scalar；bin width/缩放带来 Jacobian 常数；log-likelihood 下界取负后给 BPD 上界，越低越好。

## B. 手算与建模

### GEN06-B01
两个 unit bins 的积分就是 $P(0)=0.3,P(1)=0.7$。一维 BPD 分别

$$
-\log_2 0.3\approx1.737,\qquad -\log_2 0.7\approx0.515.
$$

### GEN06-B02
$D=2\cdot2\cdot3=12$，所以 BPD $=60/12=5$。误按 4 个 spatial pixels 归约会报 $60/4=15$，整整大三倍。

### GEN06-B03
$Z=Y/256$，所以 $p_Z(z)=256^Dp_Y(256z)$，即

$$
\log p_Y(y)=\log p_Z(z)-D\log256.
$$

每维换成 bits 的常数为 $\log_2 256=8$ bits/dim；符号取决于从哪一尺度换回哪一尺度，必须写出变量关系再判断。

## C. 推导与证明

### GEN06-C01
Unit cube volume 为 1，

$$
P_\theta(x)=\int_{[0,1)^D}p_\theta(x+u)du=E_U[p_\theta(x+U)].
$$

$\log$ 为凹函数，Jensen 给

$$
\log E_U[p]\ge E_U[\log p].
$$

要求 $p>0$ 处 log 可积；零值按扩展实数处理。

### GEN06-C02
插入任意合法 $q(u|x)$：

$$
P(x)=E_q\left[\frac{p(x+U)}{q(U|x)}\right],
$$

Jensen 得 $\mathcal L=E_q[\log p(x+U)-\log q(U|x)]$。定义 bin posterior $p(u|x)=p(x+u)/P(x)$，则

$$
\log P(x)-\mathcal L
=E_q\log\frac{q(u|x)P(x)}{p(x+u)}
=D_{KL}(q(u|x)\Vert p(u|x)).
$$

故 gap 非负。

### GEN06-C03
$\mathcal L(x)\le\log P(x)$。乘负数 $-1/(D\log2)$ 会反向：

$$
-\frac{\mathcal L(x)}{D\log2}\ge-\frac{\log P(x)}{D\log2}=\mathrm{BPD}(x).
$$

因此用 lower bound 报的是 true BPD 的上界。

## D. 边界、反例与纠错

### GEN06-D01
在每个整数训练点 $x_i$ 周围放宽度 $\varepsilon$、总质量固定 $m_i$ 的窄核，峰值约 $m_i/\varepsilon$，故 $\varepsilon\to0$ 时 point density 发散。只要核仍落在同一 bin，bin integral 始终 $m_i$；point likelihood 可无界增加而离散 mass 不变。

### GEN06-D02
若对 $x=0$ 加 $U\in[-0.2,1.2]$，可能得到 $Y=1.1$，floor 后解码为 1；同时 $x=1$ 加负噪声也可落入相同区域。不同类别 support 重叠，连续 $Y$ 不再无歧义对应原 $x$，简单的 bin integral/下界对象改变。

### GEN06-D03
至少对齐：数据是 `[0,255]` 还是 `[0,1]`；uniform 还是 variational dequantizer；是否含 $-\log q$；维度含 channel 与否；log base；exact discrete mass 还是 bound/importance estimate；test-time noise samples；域外处理。未对齐时 continuous NLL 排名不推出 discrete BPD 排名。

## E. AI 迁移

### GEN06-E01
建立表：原始 bit depth、data scaling/logit transform、noise support、$q_\phi$ 架构、训练 bound、test importance samples、$D=HWC$、natural-log 到 bits 常数、是否加 $D\log256$、平均/置信区间、官方代码 commit。只有全部一致才直接比较。

### GEN06-E02
在低维 toy data 上为每个 $x$ 用高精度 quadrature/密集 Monte Carlo 近似 $P_\theta(x)=\int_{B_x}p(y)dy$；分别估计 uniform 和 learned $q$ bound，计算 $\log P-\mathcal L$。同步估计 $D_{KL}(q||p(u|x))$ 验证相等；报告 MC 标准误与多样本 tightening。

### GEN06-E03
先从 continuous model 得 $Y$；验证域范围。Unit-bin 训练用 floor，中心化噪声可能需 round；超域是 clip（会堆积边界质量）、reject-resample（改变成本但保持条件目标）或显式 overflow 类。最后转 uint8 前说明色域和 gamma；用 round-trip test 确认每个合法 bin 回到原像素。

