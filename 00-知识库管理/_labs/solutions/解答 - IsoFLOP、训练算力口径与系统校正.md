---
type: solution
status: verified
area: [training, scaling-laws, systems]
topic: "[[IsoFLOP、训练算力口径与系统校正]]"
exercise: "[[习题 - IsoFLOP、训练算力口径与系统校正]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - IsoFLOP、训练算力口径与系统校正

> [!warning] 使用边界
> $6ND$ 是 dense Transformer 训练的规划近似，不是 profiler 读数；attention、embedding、稀疏、重算和通信须单独校正。

## A. 识别与复述

### TRN52-A01
model FLOPs 是按声明算子边界计数的算法工作；executed hardware FLOPs 包含重算、padding、融合差异等实际执行；peak FLOPs 是设备理论吞吐上限；wall time 是日历时间；energy 是功率积分；carbon 还乘时空相关电网强度。后四者至少需要硬件/系统/能源遥测，不能由 $N,D$ 唯一推出。

### TRN52-A02
total 计所有存储参数；non-embedding 排除常被词表主导的嵌入；active 是一次 token/forward 真正调用的参数；trainable 是参与梯度更新的参数。dense 预训练中 total 与 active 接近但 embedding 仍影响小模型；MoE 用 total 估每-token compute 易高估；冻结微调用 trainable 估 forward/backward 与内存又会低估。

### TRN52-A03
MFU 通常为有用 model FLOPs 除以峰值 FLOPs × 时间；HFU 为实际执行硬件 FLOPs除以同一分母。checkpointing 为省显存重算 forward activation，使 executed FLOPs 增加而 model useful work 不变，所以 HFU 可明显高于 MFU；定义必须随报告给出。

## B. 手算与构造

### TRN52-B01
$$
C_{model}\approx6\times10^9\times3\times10^{11}
=18\times10^{20}=1.8\times10^{21}\ \text{FLOPs}.
$$

### TRN52-B02
有效 model 吞吐为 $2\times10^{18}\times0.45=9\times10^{17}$ FLOP/s，故
$$
t=\frac{1.8\times10^{21}}{9\times10^{17}}=2000\text{ s}
\approx0.556\text{ h}.
$$
这是忽略启动、故障与非计数阶段的近似。

### TRN52-B03
IT 能耗为 $1.2\text{ MW}\times100\text{ h}=120\text{ MWh}$。设施能耗为 $120\times1.15=138$ MWh，即 138,000 kWh。碳排为
$$
138000\times0.35=48300\text{ kgCO}_2\text{e}=48.3\text{ tCO}_2\text{e}.
$$

## C. 推导与证明

### TRN52-C01
粗略地，每个被使用参数、每个 token 在 forward 参与一次乘加，若把乘和加各算一 FLOP，约为 $2ND$；backward 对输入梯度与权重梯度各做一个同阶矩阵乘，再加约 $4ND$，总计 $6ND$。attention 的 $S^2d$、softmax/norm、embedding/output、稀疏路由、参数共享、重算和 padding 都会破坏这个常数或 $ND$ 结构。

### TRN52-C02
由定义 $MFU=C_{model}/(P_{peak}t)$，移项得
$$
t=\frac{C_{model}}{P_{peak}MFU}.
$$
若平均 IT 功率为 $P_{IT}$，则 $E_{IT}=P_{IT}t$，设施能耗 $E_{fac}=PUE\cdot E_{IT}$，碳排 $G=E_{fac}\cdot I_{grid}$。单位应统一为 kWh 与 kgCO$_2$e/kWh。

### TRN52-C03
$$
HFU=\frac{C_{hw}}{P_{peak}t}=r\frac{C_{model}}{P_{peak}t}=r\,MFU.
$$
若把 HFU 填入 model-time 公式，得到 $\hat t=C_{model}/(P_{peak}HFU)=t/r$，即时间被低估 $r$ 倍；反过来混用也会高估。必须同时声明分子算子边界。

## D. 边界、反例与纠错

### TRN52-D01
相同 model FLOPs 可因 kernel、精度、并行、通信、重算、故障率与 MFU 不同而有不同 wall time/GPU-hours；硬件价格和利用率决定美元；功率、PUE 与电网决定能耗/碳排。因此只能说算法工作量近似相同，不能推出其他成本层级相同。

### TRN52-D02
每 token 只激活 50B 专家参数时，主干矩阵计算更接近 active 而非 1T total，直接代入会高估。但 all-to-all、负载不均、路由、容量 padding、专家复制和低 batch 利用率不在简单 active-parameter 近似中，可能增加 executed FLOPs 与时间。因此 total 和 active 都要报告并用 profiler 校正。

### TRN52-D03
低 FLOPs 方案可能运行在低利用率旧硬件上，耗时和能耗更高；也可能在高碳电网/高峰时段执行，而较高 FLOPs 在低碳地区或可再生富余时段执行；PUE 和失败重跑也可反转排序。碳排是计算、系统与能源三层的乘积结果。

## E. AI 迁移

### TRN52-E01
manifest 至少记录：total/nonembedding/active/trainable 参数；raw/seen/nonpadding token；包含哪些 forward/backward 算子；FLOP 计数约定；dtype 与稀疏；sequence/packing；activation checkpointing；硬件型号/数量与峰值定义；并行拓扑；MFU/HFU/吞吐；编译和预热；失败/重跑；平均功率、PUE、电网强度。

### TRN52-E02
先冻结数据顺序、模型语义、目标质量与评估 cadence；两系统用相同超参协议或等额搜索预算，预热后计时且编译是否计入须预注册。以达到质量阈值的所有计划运行为分母，报告 time-to-quality 分布、失败率、model/executed FLOPs、能耗和置信区间；未达标运行按 censoring/惩罚规则处理。

### TRN52-E03
追问：40% 的分子和基线是什么；是否含搜索、失败、编译和数据处理；用 model 还是 executed FLOPs；GPU-hours 的型号是否一致；美元含折旧/云折扣吗；能耗来自测量还是 TDP；PUE 与电网强度是什么；质量与 latency 是否相等。只有对象与边界齐全，百分比才可解释。

## 无提示重做

- [ ] 从 MFU 定义重推 time、energy、carbon 链。
- [ ] 为一个 MoE 训练分别写 total/active/hardware 三套账本。
