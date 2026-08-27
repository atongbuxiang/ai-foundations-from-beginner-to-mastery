---
type: solution
status: verified
area: [training, numerical-computing, low-precision]
topic: "[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]"
exercise: "[[习题 - FP32、TF32、FP16、BF16 与 FP8 数值合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - FP32、TF32、FP16、BF16 与 FP8 数值合同

> [!warning] 使用边界
> 字段级计算给出可表示性，不自动给出 kernel 的逐指令误差或真实速度；subnormal、FTZ、融合、scale 与 accumulation policy 必须另行声明。

## A. 识别与复述

### TRN57-A01
六栏为：storage（内存表示）、multiply input（乘法实际读入的有效位）、accumulate（部分积求和精度）、reduce（token/rank 归约精度）、update/state（master weight 与 optimizer state 精度）、checkpoint（持久化与恢复对象）。同一 BF16 storage 可配 FP32 accumulate、BF16/FP32 collective 和 FP32 state；故“全程 BF16”既没有指明算子，也无法复现实验。

### TRN57-A02
FP16 为 5 exponent/10 fraction，BF16 为 8/7。BF16 继承接近 FP32 的数量级范围；FP16 在同一正规 binade 有 $p=11$，比 BF16 的 $p=8$ 格点更密。前者 precision 更好但 range 小，后者 range 大但舍入粗。

### TRN57-A03
TF32 通常让 FP32 storage 的 GEMM/conv 输入按较少 fraction bits 参与 multiply，再以较高精度 accumulate；tensor 仍可显示为 FP32，逐元素算子也未必走 TF32。因此它是 backend/kernel 的执行选择，必须记录开关、算子覆盖和硬件，而不是只记 tensor dtype。

## B. 手算与构造

### TRN57-B01
在 $[1,2)$ 中指数固定，$p$ 位 significand 产生格距 $2^{-(p-1)}$：
$$
\operatorname{ulp}_{FP32}=2^{-23},\quad
\operatorname{ulp}_{FP16}=2^{-10},\quad
\operatorname{ulp}_{BF16}=2^{-7}.
$$
约为 $1.19\times10^{-7},9.77\times10^{-4},7.8125\times10^{-3}$。在 binade 边界的向上/向下格距可不同，实际判断要用更新方向上的邻点。

### TRN57-B02
$10^{-4}$ 小于 FP16 在 1 附近向下半格阈值约 $2^{-12}=2.44\times10^{-4}$，也远小于 BF16 的约 $2^{-9}=1.95\times10^{-3}$，两者都可能回到 1。FP32 向下半格约 $2^{-25}=2.98\times10^{-8}$，该更新足够大，不会仅因参数 storage 的一次舍入被吞掉。

### TRN57-B03
不 saturation 要求 $716.8/s\le448$，故 $s_{min}=1.6$。若 $s=1$，最大 activation 超过格式上限；结果依实现成为 saturation、Inf 或其他异常值。即使不崩溃，clipping bias 也已进入计算。

## C. 推导与证明

### TRN57-C01
同一 binade 可写为 $2^e(1+k2^{-(p-1)})$。相邻 $k$ 差 1，所以绝对格距为 $2^{e-(p-1)}$。因 $x\ge2^e$，相对格距不超过 $2^{-(p-1)}$；round-to-nearest 的相对误差上界约再除 2，即 unit roundoff $2^{-p}$。

### TRN57-C02
令输入先变为 $a_i(1+\delta_i)$、$b_i(1+\epsilon_i)$，其误差在乘法前已经产生；随后高精度累加只能降低对部分积求和时的新舍入。粗略地，前者贡献 $O(u_m)\sum|a_ib_i|$，后者贡献 $\gamma_{n-1}(u_a)\sum|a_ib_i|$。令 $u_a$ 很小不会让 $u_m$ 项消失。

### TRN57-C03
若 $Q$ 的无缩放格距为 $\Delta_q$，则相邻反量化值相差 $s\Delta_q$。增大 $s$ 扩大可覆盖的 $x$ 范围，却让绝对格距同步变粗；减小 $s$ 提高小量分辨率，却使 $|x|/s$ 更易越过 $q_{max}$。scale 因而是 range—resolution 交换参数。

## D. 边界、反例与纠错

### TRN57-D01
8 exponent bits只说明 BF16 与 FP32 的正规数量级范围近似；FP32 有 23 fraction bits，BF16 只有 7。1 附近两者 ulp 分别约 $2^{-23}$ 与 $2^{-7}$，差 $2^{16}$ 倍。range 相近绝不等于 precision 相近。

### TRN57-D02
第一，启用 TF32 时，FP32 tensor 可在 GEMM multiply 上只保留约 10 fraction bits。第二，硬件可能把 FP32 输入转换到 tensor-core 的较低精度路径，或 fused kernel 在某些中间量用不同 dtype。相反，某些 reduction/norm 又会显式升精度；storage 标签不能唯一决定执行链。

### TRN57-D03
E4M3 spacing 较细但 range 小；E5M2 range 更大。若 backward gradient 有少量大 outlier，E4M3 在同一 scale 下可能 saturation，而 E5M2 可保留它们。最终选择还依赖 per-tensor scale、异常值策略与误差容忍，不能由 fraction bits 单独排序。

## E. AI 迁移

### TRN57-E01
合格 manifest 示例：embedding/weight BF16 storage；QKV/FFN GEMM BF16 multiply + FP32 accumulate；softmax logits、概率归一化与 LayerNorm statistics FP32；activation 输出 BF16；gradient bucket BF16 storage、声明 FP32 或 BF16 collective；FP32 master/moments；BF16 model + FP32 optimizer/scaler/RNG checkpoint，并记录 TF32/FTZ 开关与软件硬件版本。

### TRN57-E02
固定 initialization、data order、kernel 与 scale，只把 attention probability/value aggregation 的 RN 换成 SR；或固定 rounding 只把 accumulation 升到 FP32。每 step 保存局部条件 bias、amax/zero/subnormal、entropy/concentration、loss 与 collapse 指标，检验偏差是否先出现、干预是否先改变中介再改变结局。一次只动一个因素才能区分竞争解释。

### TRN57-E03
至少需要：逐张量六栏合同；FP8 格式与 scale recipe；实际 kernel/accumulation；硬件、驱动、库与 compiler；batch/shape 与 warmup；tokens/s 分布和 peak memory；compute/wall-clock-matched 多 seed 质量区间；overflow/NaN/重启分母；reference 与回退路径。否则 1.8× 可能只是 shape 或 kernel 差异，“无损”也可能只是单 seed 终点。

## 无提示重做

- [ ] 48 小时后由字段重算三种 ulp。
- [ ] 一周后看到一条“FP8 训练”新闻时，独立写出六栏审计表。
