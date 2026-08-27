---
type: exercise
status: verified
area: [training, numerical-computing, low-precision]
topic: "[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]"
solution: "[[解答 - FP32、TF32、FP16、BF16 与 FP8 数值合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - FP32、TF32、FP16、BF16 与 FP8 数值合同

> [!abstract] 训练目标
> 能从字段推断 range、spacing 与舍入风险；能为真实训练逐张量写 storage—multiply—accumulate—reduce—update—checkpoint 六栏合同，而不以一个 dtype 标签替代算法。

## A. 识别与复述

### TRN57-A01
写出六栏 dtype 合同，并分别说明每一栏回答什么问题。为什么“全程 BF16”通常不是可复核描述？

### TRN57-A02
比较 FP16 与 BF16 的 exponent/fraction 位：哪一个通常有更大 range，哪一个在同一数量级附近有更细 spacing？

### TRN57-A03
解释 TF32 为什么更像 GEMM/conv 的执行 policy，而不是用户把 tensor 显式存成的一种通用 dtype。

## B. 手算与构造

### TRN57-B01
忽略 subnormal。对 precision 为 $p$ 的二进制格式，求 $[1,2)$ 中的 ulp。分别计算 FP32（$p=24$）、FP16（$p=11$）与 BF16（$p=8$）在该区间的 ulp。

### TRN57-B02
参数 $w=1$，更新 $Delta w=-10^{-4}$。按 half-ulp 判据判断：若直接以 FP16 或 BF16 round-to-nearest 更新，哪一种更可能把更新吞掉？FP32 呢？

### TRN57-B03
FP8 kernel 的最大有限量级取 $q_{max}=448$，一组 activation 的 $max|x|=716.8$。若要求刚好不 saturation，求最小 scale $s$；若把 $s$ 错设为 $1$，会发生什么？

## C. 推导与证明

### TRN57-C01
由 $x=(-1)^s(1.f)_2 2^e$ 证明同一 binade $[2^e,2^{e+1})$ 内相邻正规格点距离为 $2^{e-(p-1)}$，并写出相对 spacing 上界。

### TRN57-C02
把点积误差拆成“输入/乘法量化”与“累加舍入”两项，解释为什么 FP16/BF16 multiply + FP32 accumulate 不能消除输入量化误差。

### TRN57-C03
设 scale 后量化为 $\hat x=sQ(x/s)$。证明量化格距会随 $s$ 线性变化，并说明 scale 同时控制 saturation 风险与小量分辨率的原因。

## D. 边界、反例与纠错

### TRN57-D01
反驳：“BF16 和 FP32 都有 8 个 exponent bits，所以 BF16 与 FP32 一样精确。”给出 range 与 precision 分账。

### TRN57-D02
反驳：“tensor 的 storage dtype 是 FP32，因此所有乘法一定使用 24-bit significand precision。”指出至少两个反例路径。

### TRN57-D03
反驳：“E4M3 比 E5M2 多一个 fraction bit，所以训练时永远应该选 E4M3。”构造需要更大动态范围的 gradient 场景。

## E. AI 迁移

### TRN57-E01
为一个 BF16 Transformer step 写最小 tensor precision manifest：至少覆盖 embedding、attention GEMM、softmax/norm、gradient reduction、optimizer 与 checkpoint。

### TRN57-E02
设计一个定位低精度 Attention collapse 的最小消融：只改变 rounding、accumulation 或 scale 中一个因素，并列出时间先后证据。

### TRN57-E03
某报告称“FP8 比 BF16 快 1.8×且精度无损”。列出复核该结论所需的数值、kernel、硬件、质量与失败分母证据。

## 作答与复盘

先手算 ulp 与 scale，再查看 [[解答 - FP32、TF32、FP16、BF16 与 FP8 数值合同]]。每题标记 independent / hinted / copied / blocked；若答错，记录混淆发生在 range、precision、执行边界还是证据强度。
