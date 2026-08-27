---
type: concept
status: verified
area: [training, numerical-computing, low-precision]
course_id: TRN-57
prerequisites: ["[[浮点数与舍入误差]]", "[[稳定求和、点积与矩阵乘法]]"]
related: ["[[Loss Scaling、Master Weight 与低精度梯度累积]]", "[[随机舍入、无偏性与微小更新保留]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
sources: ["[[S-2019-IEEE-754]]", "[[S-2017-Micikevicius-Mixed-Precision-Training]]", "[[S-2019-Kalamkar-BFLOAT16-Training]]", "[[S-2022-Micikevicius-FP8-Formats]]", "[[S-2026-NVIDIA-浮点与IEEE754]]", "[[S-2026-PyTorch-数值精度]]", "[[S-2025-Su-11371-低精度Attention舍入偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# FP32、TF32、FP16、BF16 与 FP8 数值合同

> [!abstract] 本节目标
> 不把 dtype 当成一个标签，而是逐张量声明 storage、multiply、accumulation、reduction、optimizer 与 checkpoint 精度；能从 exponent/fraction 位数判断 range 与 relative precision，并解释为何“输入是 FP16”不等于“点积用 FP16 累加”。

## 一、先建立六栏 dtype 合同

一个训练张量至少有六个可能不同的数值角色：

| 角色 | 问题 | 例子 |
|---|---|---|
| storage dtype | 内存中以什么格式驻留？ | activation 存 BF16 |
| multiply/input dtype | 乘法读入多少有效位？ | FP32 storage 的 GEMM 允许 TF32 multiply |
| accumulation dtype | 部分积在哪种格式累加？ | BF16 multiply、FP32 accumulate |
| reduction dtype | 跨 token/rank 的和用什么格式？ | gradient All-Reduce 用 BF16 或 FP32 |
| update/state dtype | master weight、moment 在什么格式更新？ | FP32 master + FP32 Adam states |
| checkpoint dtype | 保存/恢复什么对象？ | BF16 model + FP32 optimizer shard |

所以“模型用 BF16 训练”不是完整陈述。完整陈述应像：

> 权重和 activation 以 BF16 storage，矩阵乘在 BF16 input/FP32 accumulation 的 kernel 上执行，softmax 与 norm statistics 升到 FP32，gradient bucket 用 BF16 reduction，optimizer master/state 为 FP32，checkpoint 同时保存两套状态。

## 二、二进制浮点：range 与 precision 来自不同字段

对一个正规二进制浮点数，抽象写成

$$
x=(-1)^s(1.f)_2,2^{e-b},
\tag{1}
$$

其中 $s$ 是符号位，$e$ 是 exponent 字段，$b$ 是 bias，$f$ 是 fraction。两类位数承担不同职责：

- exponent bits 主要决定可表示数量级范围；
- significand precision $p=1+$ fraction bits 主要决定相邻格点的相对间距。

在 round-to-nearest、结果保持正规且没有 overflow/underflow 时，常用模型是

$$
\operatorname{fl}(x)=x(1+\delta),\qquad |\delta|\le u,
\tag{2}
$$

其中 unit roundoff 约为 $u=2^{-p}$。式 (2) 不是全域定理：接近 0 的 subnormal、flush-to-zero、饱和、NaN/Inf 和非标准 FP8 都需单独处理。

## 三、常见格式的核心差异

| 模式 | exponent/fraction | precision $p$ | 典型最大有限值 | 最小正规量级 | 首要风险 |
|---|---:|---:|---:|---:|---|
| FP32 | 8 / 23 | 24 | $3.4\times10^{38}$ | $1.18\times10^{-38}$ | 长归约、病态问题仍会积误差 |
| TF32 multiply | 8 / 10 | 11 | 使用 FP32 range | 使用 FP32 range | storage 是 FP32，乘法有效位减少 |
| FP16 | 5 / 10 | 11 | $65504$ | $6.10\times10^{-5}$ | gradient underflow/overflow |
| BF16 | 8 / 7 | 8 | 约 $3.39\times10^{38}$ | 约 $1.18\times10^{-38}$ | range 大但舍入较粗 |
| FP8 E4M3 | 4 / 3 | 4 | 论文格式约 $448$ | 约 $1.56\times10^{-2}$ | range 小，强依赖 scale |
| FP8 E5M2 | 5 / 2 | 3 | 论文格式约 $57344$ | 约 $6.10\times10^{-5}$ | precision 更粗，适合更大 range |

[[S-2019-IEEE-754]] 是 FP16/FP32 等标准语义入口；BF16、TF32 和论文中的 FP8 不能不加说明地称为 IEEE 基本格式。[[S-2022-Micikevicius-FP8-Formats]] 还指出 E4M3/E5M2 对 NaN/Inf 编码并不完全相同。

## 四、一个 ulp 能否吞掉更新

若某 binade 中相邻可表示数的距离为 $\operatorname{ulp}(w)$，round-to-nearest 下

$$
|\Delta w|<\tfrac12\operatorname{ulp}(w)
\quad\Longrightarrow\quad
\operatorname{fl}(w+\Delta w)=w
\tag{3}
$$

是可能的。以 $w\approx1$ 为例：

- FP32 的 ulp 约 $2^{-23}$；
- FP16/TF32 multiply precision 约 $2^{-10}$；
- BF16 的 ulp 约 $2^{-7}$。

因此 BF16 range 很大，却更容易在参数 storage/update 中吞掉相对微小的改变量。这解释了为什么 range 与 update precision 必须分账，也为下一节的 master weight 建立动机。

## 五、点积有三次精度决策

设

$$
y=\sum_{i=1}^n a_ib_i.
$$

至少要问：$a_i,b_i$ 怎样量化；乘积在哪个格式形成；$n$ 个部分积怎样累加。若乘法输入先有相对误差 $u_m$、累加在精度 $u_a$，粗略前向误差包含

$$
O(u_m)\sum_i|a_ib_i|+\gamma_{n-1}(u_a)\sum_i|a_ib_i|,
\qquad
\gamma_k(u)=\frac{ku}{1-ku}.
\tag{4}
$$

这不是所有 tensor-core kernel 的逐指令定理，却准确揭示：低精度 multiply 与高精度 accumulate 解决的是两项不同误差；当 cancellation 严重时，相对误差还会被条件数放大。

## 六、TF32 不是“把 tensor 变成一种 19-bit dtype”

TF32 通常是某些 NVIDIA GEMM/conv 对 FP32 输入采用较少 fraction bits 的 multiply path，并在更高精度累加。张量内存仍可为 FP32，非 GEMM 算子也未必使用同一 policy。

所以实验必须记录：

- 输入 storage dtype；
- backend 是否允许 TF32；
- 哪些算子走 tensor core；
- accumulation 与 output dtype；
- 与 full FP32 multiply 的误差/速度对照。

[[S-2026-PyTorch-数值精度]] 还提醒：batch calculation、slice calculation、CPU/GPU 和不同 backend 不保证逐比特相同。

## 七、FP8 的 scale 是格式合同的一部分

令低精度格式最大有限值为 $q_{max}$，常见缩放可抽象成

$$
\hat x=s,Q(x/s),
\qquad
s\gtrsim \frac{\max|x|}{q_{max}}.
\tag{5}
$$

$s$ 太小会 saturation/overflow，太大则大量数落在稀疏格点或下溢。实际 recipe 可能按 tensor/channel/block、当前 amax 或历史窗口选 scale，并对 forward activation、backward gradient 分别使用 E4M3/E5M2。

因此“FP8 训练成功”至少要报告格式、scale granularity、amax history、delayed/current scaling、accumulation、异常值策略和保留高精度的张量组。

## 八、Subnormal、FTZ 与特殊值

subnormal 用隐含 leading 0 扩展 0 附近的表示，但相对精度逐渐恶化。部分硬件/路径可能 flush subnormal to zero；这会把渐进下溢改成硬截断。Inf 表示 overflow 或除零等结果，NaN 表示无效传播，但 fused kernel 可能直到更晚才暴露首个异常。

诊断时必须保存：

- 首个非有限 tensor、op 与 step；
- 输入/输出 amax 与最小非零值；
- subnormal/zero 比率；
- scale、backend、kernel 和是否启用 FTZ；
- FP32 reference 的相同中间点。

## 九、科学空间研读框：有偏是局部条件命题

[[S-2025-Su-11371-低精度Attention舍入偏差]] 讨论低精度 Attention 在概率集中条件下的舍入偏差，并明确提出“偏差是崩溃的因还是果”。课程将它改写为三个可检验问题：

1. 给定真实输入分布，条件舍入误差 $\mathbb E[Q(x)-x\mid x\in A]$ 是否非零？
2. 偏差是否先于 loss/attention collapse 出现？
3. 改 rounding/accumulation/scale 时，中介指标与最终训练是否同步改变？

单个干预改善现象，不足以证明任意低精度 Attention 都有同一根因。

## 十、图解：从格式平面走到训练合同

带着一个问题读图：**当实验只写“BF16/FP8 训练”时，究竟遗漏了哪些能改变数值结果的边界？**

![[00-知识库管理/_assets/figures/training-optimization/fig-dtype-range-precision-contract-v1.svg|900]]

> [!figure] 图 TRN-57-01　Range、precision 与六栏 dtype 合同
> 来源：自绘机制图；格式字段与语义依据 [[S-2019-IEEE-754]]、[[S-2019-Kalamkar-BFLOAT16-Training]]、[[S-2022-Micikevicius-FP8-Formats]]，执行边界依据 [[S-2026-NVIDIA-浮点与IEEE754]] 与 [[S-2026-PyTorch-数值精度]]。

**怎样读图**：先看左栏的纵轴 range 与横轴 precision，确认“指数位多”不等于“有效位多”；再沿右栏依次审计 storage、multiply、accumulate、reduce、update/state 与 checkpoint，而不要让一个 dtype 标签替代整条计算链。

**图没有证明什么**：散点位置是字段级教学示意，不刻画 subnormal、特殊值、scale recipe 或任一具体 kernel 的逐指令行为；它也没有证明某种格式在所有任务上更快或更准。

## 十一、教授视角的验收

真正掌握本节意味着你能看到任意“BF16/FP8 训练”配置时，先画出每个张量的六栏合同，再计算 range、ulp、scale 和 reduction 风险；能解释 BF16 为什么通常少 overflow 却不比 FP16 更精细；也能说明 TF32/FP8 的速度结果为何必须绑定具体 backend，而不是由 bit 数直接推出。
