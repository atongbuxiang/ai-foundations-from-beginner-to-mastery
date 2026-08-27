---
type: concept
status: verified
area: [training, quantization, optimizer-state, qat]
course_id: TRN-60
prerequisites: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[随机舍入、无偏性与微小更新保留]]"]
related: ["[[ZeRO、FSDP、激活重计算与 Offload]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
sources: ["[[S-2018-Jacob-Integer-Quantization-QAT]]", "[[S-2022-Dettmers-8bit-Optimizers]]", "[[S-2015-Gupta-Limited-Numerical-Precision]]", "[[S-2022-Micikevicius-FP8-Formats]]", "[[S-2025-Su-11371-低精度Attention舍入偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 训练量化、优化器状态压缩与 QAT

> [!abstract] 本节目标
> 把 weight、activation、gradient、optimizer state 和 communication 五类量化对象分账；从 affine quantizer 推导 clip/round 两类误差，理解 fake quantization/STE 的代理梯度，并用 byte ledger 而不是“8 bit”宣传语评价内存与速度。

## 一、先问“量化什么、在哪个时刻”

| 对象 | 典型目的 | 直接风险 |
|---|---|---|
| forward weights | GEMM/存储加速 | 参数扰动、异常值、共享 scale |
| activations | 带宽/显存/GEMM | data-dependent range、outlier、非线性放大 |
| backward gradients | 通信/计算 | estimator bias/variance、small update 消失 |
| optimizer states | 降低 persistent memory | moment/history 被扰动、rare coordinate 丢失 |
| collective payload | 降低网络 bytes | 多 rank 压缩误差与 error feedback |

“训练用 INT8”若不指出五者中的哪几个、master copy 与 accumulation 仍是什么格式，就没有可复现含义。

## 二、Affine uniform quantization

给定整数区间 $[q_{min},q_{max}]$、scale $s>0$ 和 zero-point $z$，常见量化/解量化写成

$$
q=\operatorname{clip}\left(\operatorname{round}(x/s)+z, q_{min},q_{max}\right),
\tag{1}
$$

$$
\hat x=s(q-z).
\tag{2}
$$

误差可分成：

1. range 内的 rounding error，量级至多约 $s/2$；
2. range 外的 clipping/saturation error，可能任意大且有系统方向。

所以减小 $s$ 会细化格点却缩小覆盖范围；增大 $s$ 避免饱和却使 rounding 更粗。这是 calibration 的基本偏差—方差式权衡。

## 三、Symmetric、asymmetric 与 granularity

- symmetric 常取 $z=0$，适合近零对称权重，乘法实现简单；
- asymmetric 用非零 $z$ 覆盖偏移分布，适合非负/偏置 activation；
- per-tensor 只存一套 scale，元数据少但易被 outlier 支配；
- per-channel/per-row/per-block 更贴合局部范围，却增加 scale storage、kernel 和通信复杂度。

对一个 block $B$，若 scale 由 $\max_{i\in B}|x_i|$ 决定，单个异常值会让其余坐标只使用很少格点。缩小 block 能缓解，但也增加元数据和 kernel 开销。

## 四、PTQ、QAT 与低精度训练是三件事

### Post-training quantization

先训练高精度模型，再用 calibration data 估 range 并量化。训练轨迹没有适应量化误差。

### Quantization-aware training

forward 插入 fake quantizer：

$$
\hat x=\operatorname{dequant}(\operatorname{quant}(x)),
$$

但 master parameter/optimizer 通常仍为浮点。模型在训练中适应部署时的 clip/round。

### Low-precision training

训练计算本身的 weight/activation/gradient/state 使用较低格式，目标可能是训练吞吐/内存而非整数部署。

[[S-2018-Jacob-Integer-Quantization-QAT]] 主要承担第二类、面向整数推理；不能据此声称训练本身全程 int8。

## 五、Round 的导数与 STE

真正的 $\operatorname{round}$ 几乎处处导数为 0，在跳点无经典导数。直接反传会没有有用梯度。QAT 常用 straight-through estimator：

$$
\frac{\partial \hat x}{\partial x}\approx
\begin{cases}
1,&x\text{ 在 clip range 内},\\
0\text{ 或其他代理},&x\text{ 在范围外}.
\end{cases}
\tag{3}
$$

这不是 round 的真实导数，而是选择的 surrogate optimization rule。应分别报告 forward operator、backward surrogate、scale gradient 和 clip-bound gradient。

## 六、优化器状态为何值得单独压缩

经典 mixed-precision Adam 的简化 persistent ledger 可能是：

| 对象 | bytes/parameter |
|---|---:|
| low-precision forward weight | 2 |
| low-precision gradient | 2 |
| FP32 master weight | 4 |
| FP32 first moment | 4 |
| FP32 second moment | 4 |
| 合计 | 16 |

这里 optimizer/master 占 12 bytes。若把两个 moment 压到 8-bit，理想数据 payload 从 8 降到 2 bytes/parameter，但还要加 block scales、临时解量化 buffer、可能的高精度小张量与 allocator。

[[S-2022-Dettmers-8bit-Optimizers]] 使用 block-wise dynamic quantization，并为 embedding 稳定性加入额外策略。它不是“把 Adam 公式中的所有乘除改成 uint8”。

## 七、量化 moment 会怎样进入更新

设解量化状态为

$$
\hat m_t=m_t+e_t^m,\qquad \hat v_t=v_t+e_t^v.
$$

Adam-like direction 变成

$$
\hat d_t=\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
\tag{4}
$$

一阶展开给

$$
\Delta d_t\approx
\frac{e_t^m}{\sqrt{v_t}+\epsilon}
-\frac{m_t,e_t^v}{2\sqrt{v_t}(\sqrt{v_t}+\epsilon)^2}.
\tag{5}
$$

当 $v_t$ 很小，second-moment error 可被强烈放大；这解释了为何小张量、稀有 embedding、block scale 与 epsilon 需要专门保护。

## 八、通信压缩需要 estimator 合同

若每 rank 发送 $C(g_r)$ 而非 $g_r$，聚合量是

$$
\hat g=\frac1P\sum_{r=1}^PC(g_r).
\tag{6}
$$

要问：$C$ 是否条件无偏；scale 是 local 还是 global；不同 rank 如何对齐；是否有 error feedback；压缩/解压时间是否抵消网络节省。local per-rank scale 后直接整数求和通常不等价于量化全局梯度。

## 九、评估协议：四条曲线而不是一个终点

至少报告：

1. quality/loss 随 update 的轨迹与最终分布；
2. clip rate、zero rate、scale、SQNR/relative error 的逐层轨迹；
3. persistent、peak、temporary memory 的 byte ledger；
4. kernel time、communication bytes、wall time 与失败率。

对 QAT 还需部署真实整数 kernel；fake-quant graph 的速度不是部署速度。对 8-bit optimizer 还需测 time-to-quality；只证明能 fit 更大模型，不等于相同模型更快。

## 十、图解：“8 bit”落在哪个对象与哪条路径

带着一个问题读图：**一个方案声称“8-bit training”时，它量化的是 forward、backward、state 还是 collective，又是否真的调用低位 kernel？**

![[00-知识库管理/_assets/figures/training-optimization/fig-training-quantization-object-loop-v1.svg|900]]

> [!figure] 图 TRN-60-01　量化对象、QAT 代理梯度与持久字节账本
> 来源：自绘机制图；QAT 依据 [[S-2018-Jacob-Integer-Quantization-QAT]]，优化器状态压缩依据 [[S-2022-Dettmers-8bit-Optimizers]]。

**怎样读图**：先在 A 栏点名被量化对象；B 栏区分 fake-quant forward 与 STE backward；C 栏只计算理想化持久状态，再补 scale、临时 buffer、allocator 与 activation，防止把 steady bytes 误当 peak memory。

**图没有证明什么**：16 B/parameter 是特定 mixed-precision Adam 教学账，不覆盖所有 optimizer、parameter sharing 或 allocator；图也不证明 fake quant 会自动变成更快的整数训练 kernel。

## 十一、证据边界

量化是显式改变计算图与 estimator，不是无损编码。好的结论形式是：

> 在列明对象、granularity、range estimator、rounding、surrogate gradient、master/state policy、硬件 kernel 和任务区间内，目标方案以所报 quality interval 达到某 byte/time 改善。

禁止从单一 bit-width 推出跨硬件速度，或从某 CNN/1.5B LM 实验推出任意 LLM 的稳定性。
