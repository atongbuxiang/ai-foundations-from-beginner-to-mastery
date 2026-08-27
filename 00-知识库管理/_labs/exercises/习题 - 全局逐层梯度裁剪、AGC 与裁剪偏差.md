---
type: exercise
status: verified
area: [training, optimization, gradient-clipping, estimator-bias]
topic: "[[全局逐层梯度裁剪、AGC 与裁剪偏差]]"
solution: "[[解答 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 全局逐层梯度裁剪、AGC 与裁剪偏差

> [!abstract] 训练目标
> 会区分裁剪对象、分组、阈值单位和状态顺序；能手算非交换性与随机偏差，并把“更稳定”拆成可证伪的中介量。

## A. 识别与复述

### TRN37-A01
写出 global norm clipping、layerwise norm clipping、value clipping 与 AGC 的定义。哪些方法保持全局方向，哪些会改变层间或坐标方向？

### TRN37-A02
解释 $\operatorname{clip}(\operatorname{mean}g_i)\ne\operatorname{mean}(\operatorname{clip}g_i)$。在数据并行训练中，这对应哪些实现位置？

### TRN37-A03
为什么阈值“1”没有自然通用单位？至少联系 loss reduction、batch、optimizer direction 与 parameter scale 中三项。

## B. 手算与构造

### TRN37-B01
$g=(3,4)^T$，global threshold $\tau=2$。求裁剪后梯度、缩放率和方向余弦。

### TRN37-B02
两层梯度分别为 $(6,8)$ 与 $(0.6,0.8)$，阈值均为 5。比较 global clipping 与逐层 clipping 的结果和层间范数比。

### TRN37-B03
随机梯度以 0.1 概率取 10、0.9 概率取 $-1$，阈值为 1。计算裁剪前后期望，解释方向反转。

## C. 推导与证明

### TRN37-C01
证明 global norm clipping 是 $\ell_2$ 球上的 Euclidean projection，并由此说明它对单个样本方向保持共线。

### TRN37-C02
对标量随机变量 $G$ 写出 clipping bias $E[C_\tau(G)]-E[G]$，给出 bias 为零的充分条件和并非必要的对称例。

### TRN37-C03
构造两个 microbatch 梯度，使先平均后裁剪与先裁剪后平均不仅范数不同，方向也不同；完整计算。

## D. 边界、反例与纠错

### TRN37-D01
反驳“global norm clipping 总能防止训练发散”。给出 NaN-before-clip、状态累积或曲率震荡中的一个明确反例。

### TRN37-D02
比较 clip-before-momentum 与 momentum-before-clip。为什么两者即使当步参数位移相同，未来轨迹也可能不同？

### TRN37-D03
反驳“clip rate 越低越好”。给出从 0%、适度到接近 100% 三个区间的不同解释。

## E. AI 迁移

### TRN37-E01
写分布式裁剪 manifest：microbatch reduction、accumulation、all-reduce、group/unit axis、阈值、epsilon、state order 与 precision 都必须明确。

### TRN37-E02
设计 global、layerwise、AGC 三组机制实验。至少报告 clip rate、scale quantile、方向余弦、update RMS、overflow 与最终指标。

### TRN37-E03
审计“裁剪提高泛化”声明：给出随机偏差、稳定性中介、训练失败删失和调参预算四方面的证据要求。

## 作答与复盘

先明确“clip 的输入对象和执行位置”，再查看 [[解答 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]。
