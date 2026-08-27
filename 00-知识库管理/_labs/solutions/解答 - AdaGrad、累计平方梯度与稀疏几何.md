---
type: solution
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[AdaGrad、累计平方梯度与稀疏几何]]"
exercise: "[[习题 - AdaGrad、累计平方梯度与稀疏几何]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - AdaGrad、累计平方梯度与稀疏几何

> [!warning] 使用边界
> 先手算累计器，再谈“自适应”。看到公式不等于会区分全程尺度变换、中途尺度漂移和坐标重参数化。

## A. 识别与复述

### TRN09-A01
Diagonal AdaGrad 保存 $G_t=G_{t-1}+g_t\odot g_t$，方向 $u_t=g_t/(\sqrt{G_t}+\epsilon)$，更新 $\theta_t=\theta_{t-1}-\eta u_t$。$G_{t,i}$ 是第 $i$ 坐标从开始至今的平方梯度总量；分母把历史尺度变成当前的预条件；$\epsilon$ 防止除零并控制小累计量区；$\eta$ 是全局无量纲步长倍率。若梯度单位是 loss/parameter，则 $\sqrt G$ 与梯度同单位，$u_t$ 无量纲，$\eta u_t$ 需按参数化约定解释。

### TRN09-A02
更新可写成 $-\eta H_t^{-1}g_t$，其中 $H_t=\operatorname{diag}(\sqrt{G_t}+\epsilon)\succ0$。它定义局部范数 $\|\Delta\|_{H_t}^2=\Delta^\top H_t\Delta$：历史梯度大的坐标移动代价更高。因为 $H_t$ 由观测梯度序列产生，所以叫数据依赖几何。

### TRN09-A03
前一句是更新规则的条件性结论：其他量相同，累计量较小的坐标分母较小。后一句是总体性能断言，还依赖目标、噪声、正则化、频次与标签的关联、调参和评测。局部更新机制不能直接推出优化速度或泛化必然更优。

## B. 手算与构造

### TRN09-B01
$G_1=9$，有效倍率 $1/3$，故 $\theta_1=2-3/3=1$。$G_2=9+16=25$，有效倍率 $1/5$，故 $\theta_2=1-4/5=0.2$。这里“有效学习率”指乘在原始梯度上的 $\eta/(\sqrt G+\epsilon)$，分别为 $1/3,1/5$。

### TRN09-B02
前两步后 $G_2=(9,16)$；第三个梯度平方为 $(9,0)$，所以 $G_3=(18,16)$。第三步位移
$$\Delta\theta_3=-\left(\frac3{\sqrt{18}},0\right)=\left(-\frac1{\sqrt2},0\right).$$
第二坐标的历史 $16$ 不会进入第一坐标分母；这正是 diagonal 而非 scalar 累计器。

### TRN09-B03
AdaGrad 更新为
$$-0.1(2/10,2/1)=(-0.02,-0.2).$$
SGD 的更新与 $(2,2)$ 共线，而 AdaGrad 经 diagonal preconditioner 后转向第二坐标。它不仅改变长度，也改变欧氏空间中的方向。

## C. 推导与证明

### TRN09-C01
目标关于 $\Delta$ 严格凸。求梯度得
$$g_t+\eta^{-1}H_t\Delta=0,$$
故唯一极小点 $\Delta^*=-\eta H_t^{-1}g_t$，逐坐标即 $-\eta g_{t,i}/(\sqrt{G_{t,i}}+\epsilon)$。所以“除以 RMS”也可读作在历史诱导范数中做一步最陡下降。

### TRN09-C02
若所有 $g_s'=cg_s$，则 $G_t'=c^2G_t$，$c>0$ 时
$$\frac{g_t'}{\sqrt{G_t'}}=\frac{cg_t}{c\sqrt{G_t}}=\frac{g_t}{\sqrt{G_t}}.$$
若只从 $k$ 时刻放大，旧历史仍是 $\sum_{s<k}g_s^2$，新累计器不是旧累计器的统一 $c^2$ 倍，抵消失败。

### TRN09-C03
$G_t=ta^2$，所以 $|g_t|/\sqrt{G_t}=a/(a\sqrt t)=1/\sqrt t$。总路程为 $\eta\sum_{t=1}^Tt^{-1/2}$，随 $T$ 约按 $2\eta\sqrt T$ 增长，不有界。这说明单步趋零并不自动给出有限总位移。

## D. 边界、反例与纠错

### TRN09-D01
取始终同号的外生梯度 $g_t=1$，则更新为 $-\eta/\sqrt t$，其级数发散，参数可趋向 $-\infty$。即使在目标梯度场中，也还需下界、光滑/凸性、噪声与步长条件才能证明收敛；“步长趋零”只是必要线索，不是充分条件。

### TRN09-D02
先运行 $10^6$ 步 $g_t=100$，则 $\sqrt G\approx10^5$；随后目标切换且梯度降为 1，每步归一化方向约 $10^{-5}$。旧任务留下的累计器压住新任务更新。滑动窗口方法正是试图减轻这种无限记忆。

### TRN09-D03
$G_t$ 是决定 $\mathcal T_t$ 的持久状态。重置后，同一 $\theta_t$ 和 $g_{t+1}$ 会得到不同分母与位移，随后参数又改变，因此未来梯度也改变。它等价于切换了一条新状态轨迹，而不只是修改一个静态标量。

## E. AI 迁移

### TRN09-E01
按 token 频次分桶，记录每桶的访问次数、$G_i$ 分布、有效倍率 $\eta/(\sqrt{G_i}+\epsilon)$、更新 RMS、embedding norm、训练/验证 token loss 与置信区间；同时分离未出现、低频和高频 token。只有总体 loss 会掩盖长尾坐标行为。

### TRN09-E02
固定初始化、数据版本和 batch 顺序；为两者给等额搜索次数/算力并预注册搜索空间；分别报告 sparse embedding 与 dense backbone；使用相同训练 token、早停信息和 checkpoint 选择规则；以多 seed 的优化、验证质量和资源曲线比较，而非只对默认 LR。

### TRN09-E03
AdaGrad 需为每个参数保存一个累计平方梯度，状态元素约 $P$；若 FP32，每份约 $4P$ bytes，分到 $W$ 个 shard 理想为 $4P/W$ bytes/设备。未包括参数、梯度、master weights、通信 buffer、allocator fragmentation、checkpoint 副本和临时张量。

## 无提示重做

- [ ] 48 小时后从 proximal 子问题重建更新式。
- [ ] 一周后用一个尺度切换反例解释无限记忆的代价。
