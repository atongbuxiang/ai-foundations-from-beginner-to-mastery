---
type: exercise
status: verified
area: [training, quantization, optimization]
topic: "[[训练量化、优化器状态压缩与 QAT]]"
solution: "[[解答 - 训练量化、优化器状态压缩与 QAT]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 训练量化、优化器状态压缩与 QAT

> [!abstract] 训练目标
> 能逐对象声明量化器，手算 affine quantization 与显存账，解释 STE 和 optimizer-state 误差传播，并把 bit-width 声称转成 time-to-quality 证据。

## A. 识别与复述

### TRN60-A01
列出训练中五类可量化对象，并说明为什么“8-bit training”至少有五种不同含义。

### TRN60-A02
区分 PTQ、QAT 与真实低精度训练。fake quant、master copy 和硬件整数 kernel 各出现在哪些路径？

### TRN60-A03
一个完整量化器合同至少包含哪些字段？解释 object、granularity、range estimator、clipping、rounding 与 dequant dtype。

## B. 手算与构造

### TRN60-B01
用 unsigned 2-bit affine quantizer $q\in\{0,1,2,3\}$ 覆盖 $[-1,2]$。求 scale、zero point，并量化/反量化 $x=-1,0,0.6,2.4$（先 clip，再四舍五入）。

### TRN60-B02
对 10 亿参数的理想 mixed-precision Adam，按 BF16 weight 2 B、BF16 gradient 2 B、FP32 master 4 B、FP32 $m,v$ 各 4 B 计算持久 model-state bytes。若 $m,v$ 都降到 1 B，理想节省多少？

### TRN60-B03
一个 100 MB gradient bucket 先量化成 8 bit，并额外发送每 256 个元素一个 FP32 scale。忽略 padding，计算相对 FP32 payload 的近似压缩比。

## C. 推导与证明

### TRN60-C01
写出 affine quantizer $q=\operatorname{clip}(\operatorname{round}(x/s)+z)$ 与 $\hat x=s(q-z)$；把总误差分成 clipping 与 in-range rounding 两种情形。

### TRN60-C02
round 几乎处处导数为 0。解释 QAT 的 STE 为什么是人为选择的 surrogate，并写出一种区间内 identity、区间外 0 的反传规则。

### TRN60-C03
Adam 更新为 $\Delta w=-\eta\hat m/(\sqrt{\hat v}+\epsilon)$。对小状态扰动 $\delta m,\delta v$ 做一阶展开，判断 $v$ 很小时哪一项可能被放大。

## D. 边界、反例与纠错

### TRN60-D01
反驳：“权重、activation 与 optimizer state 都是 int8，所以整个训练计算就是整数运算。”指出 dequant、accumulate、master 与 nonlinear op。

### TRN60-D02
反驳：“参数字节除以四，就能预测显存和速度都提升四倍。”列出 peak activation、temporary buffer、scale metadata、bandwidth 与 kernel 支持边界。

### TRN60-D03
反驳：“STE 给出了 round 的正确梯度。”说明 forward operator、真实导数与优化 surrogate 三者差异。

## E. AI 迁移

### TRN60-E01
为一个 QAT Transformer 写 quantization manifest，至少声明八项，并区分训练 fake-quant graph 与部署 graph。

### TRN60-E02
设计 8-bit optimizer state 的稳定性实验：包含高精度 reference、block size/scale/rounding 消融、早期与尾部指标及 failure denominator。

### TRN60-E03
把“4-bit optimizer 训练无损且省显存”改写成带任务、规模、质量区间、peak-memory 与 wall-clock 边界的合格结论。

## 作答与复盘

先画出五对象量化图并手算字节，再查看 [[解答 - 训练量化、优化器状态压缩与 QAT]]。若只写 bit-width 而未写 object 或 kernel，本题视为未完成。
