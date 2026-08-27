---
type: solution
status: verified
area: [training, quantization, optimization]
topic: "[[训练量化、优化器状态压缩与 QAT]]"
exercise: "[[习题 - 训练量化、优化器状态压缩与 QAT]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 训练量化、优化器状态压缩与 QAT

> [!warning] 使用边界
> bit-width 是表示属性，不自动等于显存、速度或训练质量；必须把被量化对象、代理梯度和实际 kernel 分账。

## A. 识别与复述

### TRN60-A01
五类对象是 forward weights、activations、backward gradients、optimizer states 与 collective payload。只压 state 可省持久显存却不改变 GEMM；只压 communication 可减链路 bytes；QAT 可在 forward 模拟权重/activation 量化。都叫“8-bit”会把完全不同的 estimator 和瓶颈混为一谈。

### TRN60-A02
PTQ 在训练后校准/量化已有模型；QAT 在训练 forward 注入 fake quant，并用 surrogate backward 学习对量化鲁棒的参数；真实低精度训练还改变 backward/state/collective 的实际 dtype。QAT 常保留 FP master，部署 graph 才可能调用整数 kernel；fake quant 本身通常仍由浮点算子执行。

### TRN60-A03
至少记录 object/tensor group、signedness/bit-width、symmetric/asymmetric、per-tensor/channel/block granularity、scale/zero point、range estimator 与时间窗口、clipping、rounding、dequant/accumulation dtype、STE、master copy、异常值处理与实际 kernel。

## B. 手算与构造

### TRN60-B01
$s=(2-(-1))/(3-0)=1$，$z=round(0-(-1)/1)=1$。于是 $q=clip(round(x)+1,0,3)$：$-1\to0\to-1$；$0\to1\to0$；$.6\to2\to1$；$2.4$ 先 clip 为 2，故 $3\to2$。最后一项有 clipping error，$.6$ 有 in-range rounding error。

### TRN60-B02
每参数 $2+2+4+4+4=16$ B，10 亿参数约 16 GB（十进制，不含 activation/buffer）。把 $m,v$ 从共 8 B 降到 2 B，新账约 10 GB，理想节省 6 GB，即持久 model state 的 37.5%，不是整个 peak memory 的 37.5%。

### TRN60-B03
100 MB FP32 含约 25M 元素。int8 payload 约 25 MB；scale 数约 $25M/256=97656$，FP32 scales 约 .391 MB，总计约 25.391 MB。压缩比约 $100/25.391=3.94\times$，还未计 header、padding 和通信协议。

## C. 推导与证明

### TRN60-C01
$$
q=clip(round(x/s)+z,q_{min},q_{max}),\qquad \hat x=s(q-z).
$$
若 $x$ 在 representable range 内，误差主要是 rounding，理想上 $|\hat x-x|\le s/2$；若越界，$q$ 卡在端点，误差含随越界距离增长的 clipping bias，不能再用半格上界。

### TRN60-C02
真实 $round$ 在非跳点局部常数，导数为 0，跳点又不可导；直接反传几乎学不动。常见 STE 人为设
$$
\frac{\partial \hat x}{\partial x}\approx\mathbf1\{x\in[x_{min},x_{max}]\}.
$$
它是优化算法的 surrogate，不是微积分算出的真实导数，因而也要做稳定性与偏差验证。

### TRN60-C03
令 $d=\sqrt v+\epsilon$，$u=m/d$。一阶扰动
$$
\delta u\approx\frac{\delta m}{d}-\frac{m}{2\sqrt v\,d^2}\delta v,\qquad
\delta(\Delta w)=-\eta\delta u.
$$
当 $v$ 小时，$1/\sqrt v$ 使第二项敏感；$\epsilon$、状态 scale、block outlier 与 quantization floor 决定实际放大程度。

## D. 边界、反例与纠错

### TRN60-D01
int8 weight/activation 常先 dequant 或由 mixed integer/floating kernel accumulate 到 int32/FP16/FP32；softmax/norm/nonlinear op 多为浮点；optimizer 可能在 FP master 上更新；scale 也是浮点。对象存储为 int8 不等于整条计算图为整数。

### TRN60-D02
peak 还含 activation、gradient bucket、all-gather、temporary workspace、allocator fragmentation 与 scale metadata。速度受 memory traffic、dequant overhead、shape、kernel availability 和硬件吞吐决定；若无相应 kernel，压缩表示甚至可能更慢。

### TRN60-D03
真实 derivative 为 0/不存在；STE 把 backward 换成选定的 identity 或 clipped identity。它可能有效，但优化的是 surrogate dynamics。正确说法是“使用某 STE 获得某任务区间内的质量”，而不是“求得 round 的正确梯度”。

## E. AI 迁移

### TRN60-E01
manifest 应含：对象/层范围、bit/格式、signedness、granularity、scale/zero point estimator、clipping percentile/learned bound、rounding、fake-quant placement、STE、FP master/state、accumulation、observer freeze、部署图的 fuse/dequant 与实际 kernel。训练 graph 与导出/部署 graph 分别做数值 oracle。

### TRN60-E02
固定 init/data，比较 FP32 states 与多个 block size、scale estimator、RN/SR、outlier fallback；跟踪早期 state quantization error、update cosine/norm、loss，尾部 quality、失败率、重启与 wall time。所有 planned runs 进入分母，并报告 peak allocated/reserved 而非只算理论 state bytes。

### TRN60-E03
合格表述示例：在指定 1.5B decoder、数据/训练长度和硬件上，某 4-bit state scheme 相对 FP32-state reference，在预注册 seeds 的 validation loss 差区间内达标，peak allocated memory 降低 X%、达到同 quality 的 wall time 改变 Y%，失败 a/b；结论不外推到权重/gradient 都为 4 bit 或其他规模/kernel。

## 无提示重做

- [ ] 48 小时后重算 1B Adam 字节账。
- [ ] 一周后从一句“4-bit training”还原完整量化 manifest。
