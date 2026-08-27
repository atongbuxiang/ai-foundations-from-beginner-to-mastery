---
type: concept
status: verified
area: [training, distributed-training, performance, reproducibility]
course_id: TRN-64
prerequisites: ["[[数值稳定性]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[ZeRO、FSDP、激活重计算与 Offload]]"]
related: ["[[训练 Telemetry、损失梯度更新与激活总账]]", "[[随机种子、配对比较、置信区间与序贯决策]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2009-Williams-Roofline]]", "[[S-2009-Patarasuk-Bandwidth-Optimal-AllReduce]]", "[[S-2026-NVIDIA-NCCL-Collectives]]", "[[S-2026-PyTorch-Reproducibility]]", "[[S-2026-PyTorch-数值精度]]", "[[S-2026-PyTorch-DDP]]", "[[S-2026-PyTorch-FSDP]]", "[[S-2025-Su-11371-低精度Attention舍入偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 通信 Roofline、非确定性与分布式训练证据地图

> [!abstract] 本节目标
> 用 FLOPs/byte、latency–bandwidth 与 critical path 解释吞吐上界；区分代数、数值、逐比特和统计复现；为“多卡更快且训练等价”建立同时覆盖性能、内存、质量、失败和环境的证据门。

## 一、经典 Roofline：先判断算力还是带宽

对一个 kernel，设 FLOPs 为 $F$，从目标内存层级移动 bytes 为 $M$，arithmetic intensity

$$
I=\frac{F}{M}\quad\text{FLOPs/byte}.
\tag{1}
$$

若硬件峰值计算吞吐 $P_{peak}$、带宽 $B_{mem}$，[[S-2009-Williams-Roofline]] 给出上界

$$
P\le\min(P_{peak},B_{mem}I).
\tag{2}
$$

ridge point

$$
I^*=\frac{P_{peak}}{B_{mem}}
\tag{3}
$$

左侧通常 bandwidth-bound，右侧可能 compute-bound。它是上界和诊断坐标，不保证达到 roof；occupancy、cache、shape、fusion 与调度仍会降低效率。

## 二、通信的 latency–bandwidth 模型

对 $n$ 条消息、总 payload $M$，简化下界为

$$
T_{comm}\gtrsim n\alpha+\frac{M}{B_{net}},
\tag{4}
$$

其中 $\alpha$ 是启动/同步 latency，$B_{net}$ 是有效带宽。小 bucket 受第一项限制，大消息受第二项限制。跨 NVLink、PCIe、NIC、交换机层级时，应分层写多个 $\alpha,B$，而非一个“网络带宽”。

对 ring All-Reduce，进一步代入

$$
T\approx2(P-1)\alpha+2\frac{P-1}{P}\frac{M}{B_{eff}}.
\tag{5}
$$

tree 可能降低 latency 阶数，ring 对大消息带宽有利；现代 collective library 会按 topology/message size 选择。

## 三、分布式 step 的关键路径

总时间不是所有局部耗时简单相加。令可重叠 compute/comm 为 $C_o,M_o$，不可重叠尾部为 $C_t,M_t$：

$$
T_{step}\gtrsim T_{input}+\max(C_o,M_o)+C_t+M_t+T_{optimizer}+T_{sync}.
\tag{6}
$$

增加通信 bytes 不必增加同量 wall time，若被 compute 隐藏；减少 bytes 也不保证提速，若 compression kernel 或 latency 落在关键路径。profiler 需显示 stream、dependency 与 exposed tail。

## 四、Parallel efficiency 的分母必须真实

strong-scaling efficiency 常写

$$
\eta_P=\frac{T_1}{P T_P},
\tag{7}
$$

但若单设备 baseline OOM、使用不同 batch/kernel/precision，$T_1$ 不存在或不公平。可改用最小可行 $P_0$：

$$
\eta_{P;P_0}=\frac{P_0T_{P_0}}{PT_P}.
\tag{8}
$$

weak scaling 则固定每 device 工作量，回答不同问题。吞吐必须同时报 samples/tokens per second、model FLOPs utilization、有效非 padding tokens 和目标 quality。

## 五、浮点非结合律怎样进入 collective

数学 All-Reduce 假设 reduction 结合/交换；浮点加法近似满足交换却不满足结合：

$$
\operatorname{fl}(\operatorname{fl}(a+b)+c)
\ne
\operatorname{fl}(a+\operatorname{fl}(b+c)).
\tag{9}
$$

改变 world size、ring/tree、bucket 或 ready order，会改变 reduction tree；low-precision reduction 进一步放大差异。若梯度落在不稳定/混沌区域，小数值差异可随训练放大，但这仍不等于某个实现“违反真实数代数”。

## 六、非确定性的来源树

| 层 | 来源 | 最小遥测 |
|---|---|---|
| RNG | initialization、dropout、data workers、SR | 每个 generator/key/state |
| data | sampler、shuffle、packing、uneven join | sample/token IDs 与 epoch cursor |
| kernel | atomics、algorithm selection、fusion | backend、kernel/config hash |
| numerical | dtype、TF32、FTZ、reduction order | 六栏 dtype + collective tree |
| distributed | async ready order、routing、failure/restart | rank timeline、group、retry |
| selection | early stop、best checkpoint、failed-run deletion | 预注册规则与完整分母 |

[[S-2026-PyTorch-Reproducibility]] 明确不保证跨 release、commit、platform 或 CPU/GPU 的完全复现；deterministic algorithms 还可能降低性能。

## 七、四级复现目标

1. **Bitwise**：同环境下每个 checkpoint 字节相同；最严格、最脆弱。
2. **Numerical tolerance**：关键 tensor/gradient/loss 在预注册绝对/相对容差内。
3. **Trajectory distribution**：多 seed 的 loss、失败、更新时间与统计区间一致。
4. **Decision/quality**：最终质量、成本和选择 regret 达到门。

不同研究问题选择不同层级。只因 bitwise 不同不能宣称质量不可复现；只因平均质量相同也不能忽略失败尾部或成本差异。

## 八、低精度 Attention 偏差的因果证据门

[[S-2025-Su-11371-低精度Attention舍入偏差]] 的问题可以嵌入完整时间线：

$$
\text{dtype/rounding intervention}
\to \text{local attention error}
\to \text{concentration/activation}
\to \text{gradient/update}
\to \text{loss/failure}.
$$

要支持因果链，需证明中介按顺序改变，并与 optimizer/data/system 替代解释比较；如果 attention concentration 先异常、舍入偏差后出现，因果方向可能相反。

## 九、性能—质量联合证据地图

| 等级 | 已完成 | 允许结论 |
|---|---|---|
| E0 | collective/shape/dtype 代数推导 | “在精确模型中语义一致” |
| E1 | 单机/小规模数值 oracle | “实现回收参考并在容差内” |
| E2 | kernel/collective microbenchmark | “在该硬件 shape 上达到所报 roof 比例” |
| E3 | 多规模完整 step profile | “瓶颈与扩展效率在所测 mesh 成立” |
| E4 | 多 seed time-to-quality | “资源改善未越过预注册质量/失败门” |
| E5 | 故障恢复与跨环境复验 | “在列明环境范围内具工程稳健性” |

只有 E2 不能说训练更快，只有 throughput 不能说 time-to-quality 更好，只有单 seed quality 不能说数值等价。

## 十、公平比较清单

比较两个分布式方案必须固定或显式分账：模型/数据/tokenizer、global samples/tokens、optimizer update count、precision policy、checkpoint/recompute、quality threshold、hardware/topology、编译预热、调参预算、失败重跑与测量窗口。报告：

- global/local shapes 与 process groups；
- model/executed FLOPs、bytes、message count；
- peak/steady memory；
- compute/comm/idle/overlap timeline；
- tokens/s、step time 分位数、MFU/HFU；
- loss/quality 多 seed 区间与 failure denominator；
- determinism policy、软件/驱动/firmware hash。

## 十一、图解：从瓶颈定位到可决策证据

带着一个问题读图：**tokens/s 上升时，我们凭什么判断它来自通信优化，并且没有破坏训练质量？**

![[00-知识库管理/_assets/figures/training-optimization/fig-communication-roofline-evidence-v1.svg|900]]

> [!figure] 图 TRN-64-01　通信 Roofline 与分布式证据阶梯
> 来源：自绘机制图；Roofline 依据 [[S-2009-Williams-Roofline]]，通信模型结合 [[S-2009-Patarasuk-Bandwidth-Optimal-AllReduce]]，复现边界依据 [[S-2026-PyTorch-Reproducibility]]。

**怎样读图**：左栏先用 intensity 与不同 ceiling 定位候选瓶颈，再用 profiler 检查未遮蔽通信尾；右栏从 E0 manifest 逐级上升到 counters、critical path、matched learning curve、paired repeats 与因果干预。

**图没有证明什么**：Roofline 是上界/诊断模型，不保证测量点一定落在某条简单直线上；证据阶梯也不是“做到 E5 就普遍成立”，每一级仍受任务、规模、硬件和时间窗口限制。

## 十二、核心结论

分布式训练的“等价”先是一个代数合同，再是数值容差命题，最后才是统计与决策结论；“更快”先是 critical-path 结果，再是 time-to-quality 结果。把这两条证据链交叉起来，才能避免以峰值 FLOPs、单次吞吐或同 seed 终点替代完整判断。
