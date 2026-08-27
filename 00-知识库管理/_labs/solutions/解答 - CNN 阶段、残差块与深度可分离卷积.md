---
type: solution
status: draft
area: [architecture, cnn]
topic: "[[CNN 阶段、残差块与深度可分离卷积]]"
exercise: "[[习题 - CNN 阶段、残差块与深度可分离卷积]]"
sources: ["[[S-2016-He-ResNet]]", "[[S-2017-Howard-MobileNet]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - CNN 阶段、残差块与深度可分离卷积

## A. 识别与复述
### ARCH-CNN-A01
输入/输出 shape、channels、resolution、repeat、block、kernel/stride/dilation/groups、shortcut/projection、parameters、MACs、activation bytes、RF/jump、latency 可作为基本列。
### ARCH-CNN-A02
空间 stride 改变、$C_{in}\ne C_{out}$、layout 或语义空间不相容时不能直接相加，需要 $1\times1$ stride projection、pool+channel pad 等明确映射。
### ARCH-CNN-A03
Classic bottleneck 是 $1\times1$ 压缩—$3\times3$—$1\times1$ 恢复；separable 用 depthwise 空间 filtering + pointwise 通道 mixing，连接 factorization 不同。

## B. 手算与建模
### ARCH-CNN-B01
$56^2\cdot64^2\cdot9=115,605,504$ MACs。第二层 $28^2\cdot128^2\cdot9$ 也是 115,605,504，忽略边界/batch，正好相同。
### ARCH-CNN-B02
比值 $1/64+1/9\approx0.1267$，即约 12.7%；含 bias/中间宽度会略变。
### ARCH-CNN-B03
$1\times1:64^2=4096$；3×3：$64^2\cdot9=36,864$；最后 $64\cdot256=16,384$；总 $57,344$。若 shortcut 从 64 到 256，还需 projection $16,384$。

## C. 推导与证明
### ARCH-CNN-C01
Depthwise $D[c,a,b]$ 后 pointwise $P[o,c]$，线性复合给 $K[o,c,a,b]=P[o,c]D[c,a,b]$。固定 $c$，所有 $o$ 的空间 slices 共线，故不能表示任意独立 slices。
### ARCH-CNN-C02
MACs $HW C_{in}C_{out}K^2$；宽度都乘 $\alpha$ 得 $\alpha^2$，两轴分辨率乘 $\rho$ 得 $\rho^2$，合为 $\alpha^2\rho^2$。首尾层和取整不精确遵守。
### ARCH-CNN-C03
Tensor addition逐元素定义，索引集合必须一致，因此 batch/channel/spatial shape 相同。可用 learned $1\times1$ conv（含 stride）、pool 后 projection、或预定义 pad/crop，但每种都改变函数和证据。

## D. 边界、反例与纠错
### ARCH-CNN-D01
对输入通道 1，希望输出1空间核 $[1,0]$、输出2为 $[0,1]$。Depthwise 对通道1只有同一 $D_1=[a,b]$，两输出只能是其标量倍数，不能同时得到不共线的两核；standard 可直接设置。
### ARCH-CNN-D02
模型文件还含其他层/量化元数据；训练显存常由 activations/optimizer states 主导；低 FLOPs depthwise 可能 memory-bound；latency 受 kernel、batch、fusion、设备影响，比例没有必然关系。
### ARCH-CNN-D03
任务所需空间精度、channel capacity、stage repeat、memory 与硬件不同；翻倍只是维持 standard conv 粗略 MAC 的启发式。过宽后期可能浪费，过早下采样会损小目标。

## E. AI 迁移
### ARCH-CNN-E01
固定数据/preprocess/训练预算和 accuracy target；逐层参数/MAC/activation；在目标芯片用相同 batch/dtype/threads 测 warm latency、throughput、energy、peak memory；报告 operator coverage/fusion/quantization，多个 seeds 和端到端而非单算子。
### ARCH-CNN-E02
计算每个 layer/block 需保存的 $NCHW\times bytes$，加 residual 两支和 backward saved tensors；通常 early high-resolution、较宽 expansion 或 concat 处形成峰值，再用 profiler 验证 workspace。
### ARCH-CNN-E03
CNN stem 用 overlapping small kernels、共享局部 bias、渐进下采样；patch embedding 常用大 kernel=stride，直接形成不重叠 tokens，局部先验更弱且 sampling 更激进。应匹配 token count/FLOPs 比 shift consistency、小目标和吞吐。
