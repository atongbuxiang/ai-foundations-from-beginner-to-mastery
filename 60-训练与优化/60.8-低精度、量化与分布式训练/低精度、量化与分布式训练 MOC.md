---
type: moc
status: active
area: [training, numerical-computing, distributed-systems]
prerequisites: ["[[浮点数与舍入误差]]", "[[数值稳定性]]", "[[稳定求和、点积与矩阵乘法]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]", "[[科学空间 - 第六章训练与优化专题来源地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 低精度、量化与分布式训练 MOC

> [!abstract] 分卷目标
> 把 mixed precision 与 distributed training 从配置缩写还原成可推导的数值系统：逐张量核对 storage、multiply、accumulate、reduce、update/state 与 checkpoint，逐 rank 核对 estimator、时钟、shape、collective、生命周期和关键路径，并以 matched quality 与复现等级约束“更快/等价”结论。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-57 | [[FP32、TF32、FP16、BF16 与 FP8 数值合同]] | 比较 range/precision 并写六栏 dtype 合同 | 静态验收通过；个人掌握另计 |
| TRN-58 | [[Loss Scaling、Master Weight 与低精度梯度累积]] | 审计 unscale 顺序、overflow consensus 与多时钟 | 静态验收通过；个人掌握另计 |
| TRN-59 | [[随机舍入、无偏性与微小更新保留]] | 区分 local/step/trajectory/decision bias | 静态验收通过；个人掌握另计 |
| TRN-60 | [[训练量化、优化器状态压缩与 QAT]] | 分账五类量化对象、STE 与真实 kernel | 静态验收通过；个人掌握另计 |
| TRN-61 | [[数据并行、All-Reduce 与全局 Batch 语义]] | 对齐 sample/token count、reduction 与 DP degree | 静态验收通过；个人掌握另计 |
| TRN-62 | [[Tensor、Pipeline、Sequence 与 Expert Parallel]] | 从 tensor shape 写 process mesh 与 collective | 静态验收通过；个人掌握另计 |
| TRN-63 | [[ZeRO、FSDP、激活重计算与 Offload]] | 从对象生命周期计算 steady/peak memory | 静态验收通过；个人掌握另计 |
| TRN-64 | [[通信 Roofline、非确定性与分布式训练证据地图]] | 比较关键路径、quality 与复现/因果证据 | 静态验收通过；个人掌握另计 |

本卷的 25 张一级/官方来源卡覆盖 IEEE 754、mixed precision、BF16/FP8、QAT/8-bit optimizer、DDP/NCCL、Megatron/GPipe/sequence parallel、MoE、ZeRO/FSDP/checkpointing/offload、Roofline 与复现性。科学空间低精度 Attention 文章作为中文问题入口和候选因果解释，不承担普遍低精度崩溃定理。

## 卷级实验与验收

- [[实验 - 低精度数值、分布式语义与系统证据审计]]：10 条解析/合成轨道、38 项机器断言、10 CSV 与 3 张实验图；
- [[60.8 分卷累计测验与复现门]]：闭卷数值—分布式推导、开卷确定性复现和真实小模型 pilot；
- [[60.8 静态完成与质量审计]]：题号、来源、链接、公式、SVG、实验和状态的最终审计。

## 题库入口

| 节点 | 习题 | 独立解答 |
|---|---|---|
| TRN-57 | [[习题 - FP32、TF32、FP16、BF16 与 FP8 数值合同]] | [[解答 - FP32、TF32、FP16、BF16 与 FP8 数值合同]] |
| TRN-58 | [[习题 - Loss Scaling、Master Weight 与低精度梯度累积]] | [[解答 - Loss Scaling、Master Weight 与低精度梯度累积]] |
| TRN-59 | [[习题 - 随机舍入、无偏性与微小更新保留]] | [[解答 - 随机舍入、无偏性与微小更新保留]] |
| TRN-60 | [[习题 - 训练量化、优化器状态压缩与 QAT]] | [[解答 - 训练量化、优化器状态压缩与 QAT]] |
| TRN-61 | [[习题 - 数据并行、All-Reduce 与全局 Batch 语义]] | [[解答 - 数据并行、All-Reduce 与全局 Batch 语义]] |
| TRN-62 | [[习题 - Tensor、Pipeline、Sequence 与 Expert Parallel]] | [[解答 - Tensor、Pipeline、Sequence 与 Expert Parallel]] |
| TRN-63 | [[习题 - ZeRO、FSDP、激活重计算与 Offload]] | [[解答 - ZeRO、FSDP、激活重计算与 Offload]] |
| TRN-64 | [[习题 - 通信 Roofline、非确定性与分布式训练证据地图]] | [[解答 - 通信 Roofline、非确定性与分布式训练证据地图]] |

> [!success] 当前状态
> 八个核心节点、八张机制图、120 道题与逐题解答、十轨道卷级实验、三张实验图和累计测验均已通过静态质量审计。本状态只表示教材 artifact 完整；学习者仍需完成题库、闭卷推导与真实 mixed-precision/distributed pilot。
